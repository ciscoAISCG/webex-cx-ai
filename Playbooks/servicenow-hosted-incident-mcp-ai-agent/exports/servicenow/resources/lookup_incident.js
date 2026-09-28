/*
  MCP tool: get_incident

  Purpose: Retrieve one ServiceNow incident that belongs to the authenticated
  employee, using its incident number.
  Endpoint: GET /incidents/{incident_number}?caller_id={caller_sys_id}

  Inputs:
  - incident_number: path value in the form INC followed by 5-12 digits.
    A 5-12 digit number without the INC prefix is also accepted; spaces and
    hyphens are ignored.
  - caller_id: required query value containing the trusted, 32-character
    ServiceNow sys_user.sys_id for the authenticated caller. Do not generate
    or infer this value, and do not use employee ID or phone number here.

  Authorization and privacy: The query requires both the incident number and
  caller_id, so an employee can retrieve only that caller's incident. The
  response is limited to allowlisted incident fields. work_notes is the latest
  internal ServiceNow journal entry; do not read it back to the caller unless
  your organization explicitly approves that behavior.

  Success response 200:
  {
    incident_number, short_description, state, state_display, priority,
    priority_display, work_notes, last_updated, update_allowed, close_allowed
  }
  update_allowed is false only for the configured closed state (7). For the
  usual configuration, close_allowed is true only for the resolved state (6).
  Verify those state values against the target ServiceNow instance.

  Error responses: 400 for an invalid caller_id or incident_number; 404 with
  an empty object when the incident does not exist or is not owned by the
  supplied caller_id. Authentication and REST Endpoint ACLs are configured on
  the Scripted REST resource rather than by this script.
 */
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    function trim(value) {
        return value === null || value === undefined ? '' : String(value).replace(/^\s+|\s+$/g, '');
    }

    function send(code, payload) {
        response.setStatus(code);
        response.setBody(payload);
    }

    function latestWorkNotes(record) {
        return record.isValidField('work_notes') ? record.work_notes.getJournalEntry(1) : '';
    }

    var callerId = trim(request.queryParams.caller_id);
    if (!/^[0-9a-f]{32}$/i.test(callerId)) {
        send(400, { error: 'caller_id must be a valid ServiceNow sys_id' });
        return;
    }

    var incidentNumber = trim(request.pathParams.incident_number).toUpperCase().replace(/[\s-]/g, '');
    if (/^[0-9]{5,12}$/.test(incidentNumber)) {
        incidentNumber = 'INC' + incidentNumber;
    }
    if (!/^INC[0-9]{5,12}$/.test(incidentNumber)) {
        send(400, { error: 'incident_number is invalid' });
        return;
    }

    var incident = new GlideRecordSecure('incident');
    incident.addQuery('number', incidentNumber);
    incident.addQuery('caller_id', callerId);
    incident.setLimit(1);
    incident.query();

    if (!incident.next()) {
        send(404, {});
        return;
    }

    send(200, {
        incident_number: incident.getValue('number'),
        short_description: incident.getValue('short_description'),
        state: incident.getValue('state'),
        state_display: incident.getDisplayValue('state'),
        priority: incident.getValue('priority'),
        priority_display: incident.getDisplayValue('priority'),
        work_notes: latestWorkNotes(incident),
        last_updated: incident.getValue('sys_updated_on'),
        update_allowed: incident.getValue('state') !== '7',
        close_allowed: incident.getValue('state') === '6'
    });
})(request, response);
