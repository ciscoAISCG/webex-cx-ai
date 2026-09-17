/*
  MCP tool: update_incident

  Purpose: Add a caller-approved update, resolve an incident, or close an
  already-resolved incident owned by the authenticated employee.
  Endpoint: PUT /incidents/{incident_number}
  Content-Type: application/json

  Common inputs:
  - incident_number: path value in the form INC followed by 5-12 digits. A
    5-12 digit number without the INC prefix is also accepted; spaces and
    hyphens are ignored.
  - caller_id: required trusted 32-character ServiceNow sys_user.sys_id.
    The MCP model must not generate or infer it. The incident must belong to
    this caller_id.
  - operation: exactly one of update, resolve, or close.
  - idempotency_key: optional retry key up to 100 characters. The
    X-Idempotency-Key or X-Request-ID headers may be used instead.

  Operation-specific inputs and confirmation:
  - update: provide update_note (customer-visible comment), work_notes
    (internal ServiceNow note), or both. update_note is 2-2000 characters and
    work_notes is 2-4000 characters. caller_confirmed must be true after the
    caller confirms the requested update. Updates are rejected only when the
    incident is in the configured closed state.
  - resolve: provide resolution_summary (3-1000 characters), optional
    resolution_code, and caller_confirmed_resolved=true after the caller
    confirms the issue is resolved. The script sets the state to 6.
  - close: provide resolution_summary, close_code, and
    caller_confirmed_resolved=true. The incident must already be in state 6;
    the script then sets the state to 7. Verify these state values against the
    target instance because ServiceNow choices can be customized.

  Safety and behavior: Credentials, secrets, tokens, PINs, and passwords are
  redacted from update and work-note text before storage. A request with an
  idempotency key matching the incident's recorded correlation_id returns a
  duplicate result without applying the operation again. Do not use this tool
  to invent resolution facts or to bypass caller confirmation.

  Success response 200:
  { operation, incident_number, state_display }
  A recognized retry returns the same shape with duplicate: true.

  Error responses: 400 for invalid identity, operation, number, confirmation,
  content, or update state; 404 when the incident is not found for caller_id;
  409 when closing an already-closed incident or when the close preconditions
  are not met; 500 when ServiceNow cannot update the incident or a requested
  journal field is unavailable.
 */
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    var STATE_RESOLVED = '6';
    var STATE_CLOSED = '7';

    function trim(value) {
        return value === null || value === undefined ? '' : String(value).replace(/^\s+|\s+$/g, '');
    }

    function body() {
        if (request.body && request.body.data) {
            return request.body.data;
        }
        try {
            return request.body && request.body.dataString ? JSON.parse(request.body.dataString) : {};
        } catch (ex) {
            return {};
        }
    }

    function requestId(data) {
        var value = request.getHeader('X-Idempotency-Key') ||
            request.getHeader('X-Request-ID') ||
            data.idempotency_key || '';
        value = trim(value);
        return value.length <= 100 ? value : '';
    }

    function redact(value) {
        var text = trim(value);
        text = text.replace(
            /\b(password|passwd|passcode|pin|otp|token|secret|api[_ -]?key)\b\s*[:=]\s*[^\s,;]+/gi,
            '$1: [REDACTED]'
        );
        text = text.replace(/\bBearer\s+[A-Za-z0-9._~+\/-]+=*/gi, 'Bearer [REDACTED]');
        return text;
    }

    function send(code, payload) {
        response.setStatus(code);
        response.setBody(payload);
    }

    var data = body();
    var callerId = trim(data.caller_id);
    if (!/^[0-9a-f]{32}$/i.test(callerId)) {
        send(400, { error: 'caller_id must be a valid ServiceNow sys_id' });
        return;
    }

    var operation = trim(data.operation).toLowerCase();
    if (['update', 'resolve', 'close'].indexOf(operation) === -1) {
        send(400, { error: 'operation must be update, resolve, or close' });
        return;
    }

    var confirmed = operation === 'update' ? data.caller_confirmed : data.caller_confirmed_resolved;
    if (!(confirmed === true || confirmed === 'true')) {
        send(400, { error: 'Explicit confirmation is required' });
        return;
    }

    var number = trim(request.pathParams.incident_number).toUpperCase().replace(/[\s-]/g, '');
    if (/^[0-9]{5,12}$/.test(number)) {
        number = 'INC' + number;
    }
    if (!/^INC[0-9]{5,12}$/.test(number)) {
        send(400, { error: 'incident_number is invalid' });
        return;
    }

    var incident = new GlideRecordSecure('incident');
    incident.addQuery('number', number);
    incident.addQuery('caller_id', callerId);
    incident.setLimit(1);
    incident.query();
    if (!incident.next()) {
        send(404, {});
        return;
    }

    var idempotencyKey = requestId(data);
    if (idempotencyKey && incident.isValidField('correlation_id') &&
        incident.getValue('correlation_id') === idempotencyKey) {
        send(200, {
            operation: operation,
            incident_number: incident.getValue('number'),
            state_display: incident.getDisplayValue('state'),
            duplicate: true
        });
        return;
    }

    if (operation === 'update') {
        var note = redact(data.update_note);
        var workNotes = redact(data.work_notes);
        var invalidNote = data.update_note && (note.length < 2 || note.length > 2000);
        var invalidWorkNotes = data.work_notes && (workNotes.length < 2 || workNotes.length > 4000);
        if ((!note && !workNotes) || invalidNote || invalidWorkNotes ||
            incident.getValue('state') === STATE_CLOSED) {
            send(400, { error: 'update_note or work_notes is required and the incident must be open' });
            return;
        }
        if (note) {
            if (!incident.isValidField('comments')) {
                send(500, { error: 'comments is not available on the incident table' });
                return;
            }
            incident.comments = note;
        }
        if (workNotes) {
            if (!incident.isValidField('work_notes')) {
                send(500, { error: 'work_notes is not available on the incident table' });
                return;
            }
            incident.work_notes = workNotes;
        }
    } else {
        var resolution = redact(data.resolution_summary);
        if (resolution.length < 3 || resolution.length > 1000) {
            send(400, { error: 'resolution_summary is invalid' });
            return;
        }
        if (incident.getValue('state') === STATE_CLOSED) {
            send(409, { error: 'Incident is already closed' });
            return;
        }
        if (incident.isValidField('close_notes')) {
            incident.close_notes = resolution;
        }
        if (operation === 'resolve') {
            incident.state = STATE_RESOLVED;
            if (data.resolution_code && incident.isValidField('close_code')) {
                incident.close_code = trim(data.resolution_code);
            }
        } else {
            var closeCode = trim(data.close_code);
            if (!closeCode || incident.getValue('state') !== STATE_RESOLVED) {
                send(409, { error: 'A close_code is required and the incident must be resolved' });
                return;
            }
            incident.close_code = closeCode;
            incident.state = STATE_CLOSED;
        }
    }

    if (idempotencyKey && incident.isValidField('correlation_id')) {
        incident.correlation_id = idempotencyKey;
    }

    if (!incident.update()) {
        send(500, { error: 'Incident could not be updated' });
        return;
    }

    send(200, {
        operation: operation,
        incident_number: incident.getValue('number'),
        state_display: incident.getDisplayValue('state')
    });
})(request, response);
