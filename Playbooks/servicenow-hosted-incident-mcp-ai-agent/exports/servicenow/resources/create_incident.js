/*
  MCP tool: create_incident

  Purpose: Create a ServiceNow incident for the authenticated employee after
  the employee explicitly confirms the final incident summary.
  Endpoint: POST /incidents
  Content-Type: application/json

  Identity and safety:
  - caller_id is the 32-character sys_user.sys_id from trusted AI-agent
    session context. The MCP model must not generate, infer, or alter it.
  - caller_id must identify an active ServiceNow user. The request is rejected
    unless caller_confirmed is the boolean value true (the string "true" is
    also accepted by this script).
  - Never send credentials, secrets, tokens, PINs, passwords, or unnecessary
    personal information. Common secret patterns are redacted before storage.

  Required JSON fields:
  - caller_id: trusted ServiceNow user sys_id.
  - short_description: issue summary, 5-160 characters.
  - description: redacted symptoms and troubleshooting details, 10-4000
    characters.
  - affected_scope: single_user, multiple_users, site_or_service, or unknown.
  - business_impact: work_blocked, work_degraded, not_blocked, or unknown.
  - caller_confirmed: true only after the caller confirms the summary and asks
    the agent to create the incident.

  Optional JSON fields:
  - work_notes: internal ServiceNow note, 2-4000 characters.
  - affected_item: caller-stated device, application, or service, up to 160
    characters; do not infer a configuration item.
  - error_message: caller-stated error text, up to 500 characters.
  - started_when: caller-stated start time or period, up to 100 characters.
  - attempted_steps: semicolon-delimited ordered troubleshooting steps already
    attempted. Arrays are also accepted for backward compatibility.
  - idempotency_key: client-generated retry key, up to 100 characters.
    X-Idempotency-Key or X-Request-ID headers may be used instead.

  Behavior: The script stores the supplied incident details, maps
  affected_scope to impact and business_impact to urgency, and associates the
  optional idempotency key with the incident. A repeated request with the same
  key for the same caller returns the existing incident instead of creating a
  second one.

  Success responses:
  - 201: { status: "CREATED", incident_number, caller_id, state_display }.
  - 200: { status: "DUPLICATE_CONFIRMED", incident_number, state_display }.

  Error responses: 400 for invalid fields, missing confirmation, or invalid
  content; 404 when caller_id is not an active user; 500 when ServiceNow
  cannot create the incident or the requested journal field is unavailable.
 */
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    function trim(value) {
        return value === null || value === undefined ? '' : String(value).replace(/^\s+|\s+$/g, '');
    }

    function readBody() {
        if (request.body && request.body.data) {
            return request.body.data;
        }
        try {
            return request.body && request.body.dataString ? JSON.parse(request.body.dataString) : {};
        } catch (ex) {
            return {};
        }
    }

    function redact(value) {
        var text = trim(value);
        text = text.replace(
            /\b(password|passwd|passcode|pin|otp|token|secret|api[_ -]?key)\b\s*[:=]\s*[^\s,;]+/gi,
            '$1: [REDACTED]'
        );
        return text.replace(/\bBearer\s+[A-Za-z0-9._~+\/-]+=*/gi, 'Bearer [REDACTED]');
    }

    function text(value, maxLength) {
        var valueText = trim(value);
        return valueText.length <= maxLength ? valueText : '';
    }

    function normalizeAttemptedSteps(value) {
        var rawSteps = [];
        var steps = [];
        var i;
        var step;

        if (Object.prototype.toString.call(value) === '[object Array]') {
            rawSteps = value;
        } else {
            value = trim(value);
            if (!value) {
                return steps;
            }
            rawSteps = value.split(';');
        }

        for (i = 0; i < rawSteps.length && steps.length < 10; i++) {
            step = text(rawSteps[i], 300);
            if (step) {
                steps.push(step);
            }
        }
        return steps;
    }

    function send(code, payload) {
        response.setStatus(code);
        response.setBody(payload);
    }

    var data = readBody();
    var callerId = trim(data.caller_id);
    if (!/^[0-9a-f]{32}$/i.test(callerId)) {
        send(400, { error: 'caller_id must be a valid ServiceNow sys_id' });
        return;
    }
    if (!(data.caller_confirmed === true || data.caller_confirmed === 'true')) {
        send(400, { error: 'caller_confirmed must be true' });
        return;
    }

    var caller = new GlideRecordSecure('sys_user');
    caller.addQuery('sys_id', callerId);
    caller.addQuery('active', true);
    caller.setLimit(1);
    caller.query();
    if (!caller.next()) {
        send(404, {});
        return;
    }

    var shortDescription = redact(text(data.short_description, 160));
    var description = redact(text(data.description, 4000));
    var workNotes = redact(text(data.work_notes, 4000));
    var attemptedSteps = normalizeAttemptedSteps(data.attempted_steps);
    if (shortDescription.length < 5 || description.length < 10) {
        send(400, { error: 'short_description and description are required' });
        return;
    }
    if (data.work_notes && (workNotes.length < 2 || workNotes.length > 4000)) {
        send(400, { error: 'work_notes is invalid' });
        return;
    }

    var requestId = trim(request.getHeader('X-Idempotency-Key') ||
        request.getHeader('X-Request-ID') || data.idempotency_key || '');
    if (requestId.length > 100) {
        send(400, { error: 'idempotency_key is too long' });
        return;
    }

    if (requestId) {
        var duplicate = new GlideRecordSecure('incident');
        if (duplicate.isValidField('correlation_id')) {
            duplicate.addQuery('correlation_id', requestId);
            duplicate.addQuery('caller_id', callerId);
            duplicate.setLimit(1);
            duplicate.query();
            if (duplicate.next()) {
                send(200, {
                    status: 'DUPLICATE_CONFIRMED',
                    incident_number: duplicate.getValue('number'),
                    state_display: duplicate.getDisplayValue('state')
                });
                return;
            }
        }
    }

    var incident = new GlideRecordSecure('incident');
    incident.initialize();
    incident.caller_id = callerId;
    incident.short_description = shortDescription;
    incident.description = description;
    if (workNotes) {
        if (!incident.isValidField('work_notes')) {
            send(500, { error: 'work_notes is not available on the incident table' });
            return;
        }
        incident.work_notes = workNotes;
    }

    if (data.affected_item) {
        incident.description += '\nAffected item: ' + redact(text(data.affected_item, 160));
    }
    if (data.error_message) {
        incident.description += '\nCaller-reported error: ' + redact(text(data.error_message, 500));
    }
    if (data.started_when) {
        incident.description += '\nStarted when: ' + redact(text(data.started_when, 100));
    }
    if (data.affected_scope) {
        incident.description += '\nAffected scope: ' + text(data.affected_scope, 40);
    }
    if (data.business_impact) {
        incident.description += '\nBusiness impact: ' + text(data.business_impact, 40);
    }
    if (attemptedSteps.length) {
        incident.description += '\nAttempted steps: ' + redact(attemptedSteps.join('; '));
    }

    if (incident.isValidField('impact')) {
        incident.impact = data.affected_scope === 'site_or_service' ? '1' :
            data.affected_scope === 'multiple_users' ? '2' : '3';
    }
    if (incident.isValidField('urgency')) {
        incident.urgency = data.business_impact === 'work_blocked' ? '1' :
            data.business_impact === 'work_degraded' ? '2' : '3';
    }
    if (requestId && incident.isValidField('correlation_id')) {
        incident.correlation_id = requestId;
    }
    if (requestId && incident.isValidField('correlation_display')) {
        incident.correlation_display = 'AI_AGENT_MCP_V3';
    }

    if (!incident.insert()) {
        send(500, { error: 'Incident could not be created' });
        return;
    }

    send(201, {
        status: 'CREATED',
        incident_number: incident.getValue('number'),
        caller_id: callerId,
        state_display: incident.getDisplayValue('state')
    });
})(request, response);
