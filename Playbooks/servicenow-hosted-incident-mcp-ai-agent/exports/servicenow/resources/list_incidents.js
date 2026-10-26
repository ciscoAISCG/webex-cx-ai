/*
  MCP tool: get_incidents

  Purpose: List ServiceNow incidents owned by the authenticated employee.
  Endpoint: GET /incidents?caller_id={authenticated_caller_sys_id}

  Input:
  - caller_id: required query value containing the trusted, 32-character
    ServiceNow sys_user.sys_id for the authenticated caller. Inject this from
    trusted session or signed identity context; never generate or infer it.
    Employee ID and phone number are not accepted by this tool.

  Authorization and privacy: Every query is filtered by caller_id and uses
  GlideRecordSecure. The response contains only allowlisted incident fields.
  work_notes is the latest internal ServiceNow journal entry; do not expose it
  to the caller unless your organization explicitly approves that behavior.

  Ordering and limits: Results are sorted by sys_updated_on descending and
  capped at 100 incidents. There is no pagination parameter. An empty result
  is a successful 200 response with an empty array.

  Success response 200: an array of objects with incident_number,
  short_description, state, state_display, priority, priority_display,
  work_notes, and last_updated.

  Error response: 400 with an error message when caller_id is missing or is
  not a valid 32-character ServiceNow sys_id. Authentication and REST Endpoint
  ACLs are configured on the Scripted REST resource rather than by this
  script.
 */
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    function latestWorkNotes(record) {
        return record.isValidField('work_notes') ? record.work_notes.getJournalEntry(1) : '';
    }

    var callerId = request.queryParams.caller_id;
    if (!/^[0-9a-f]{32}$/i.test(callerId || '')) {
        response.setStatus(400);
        response.setBody({ error: 'caller_id must be a valid ServiceNow sys_id' });
        return;
    }

    var incidents = new GlideRecordSecure('incident');
    incidents.addQuery('caller_id', callerId);
    incidents.orderByDesc('sys_updated_on');
    incidents.setLimit(100);
    incidents.query();

    var results = [];
    while (incidents.next()) {
        results.push({
            incident_number: incidents.getValue('number'),
            short_description: incidents.getValue('short_description'),
            state: incidents.getValue('state'),
            state_display: incidents.getDisplayValue('state'),
            priority: incidents.getValue('priority'),
            priority_display: incidents.getDisplayValue('priority'),
            work_notes: latestWorkNotes(incidents),
            last_updated: incidents.getValue('sys_updated_on')
        });
    }

    response.setStatus(200);
    response.setBody(results);
})(request, response);
