/*
  MCP tool: lookup_user

  Purpose: Resolve exactly one active ServiceNow user by the employee ID, so a
  trusted caller sys_id can be supplied to the incident tools.
  Endpoint: GET /users?employee_id=...

  Inputs:
  - employee_id: exactly six numeric digits matching ServiceNow's
    employee_number field. Employee ID is a lookup value, not a credential.
    Use an authenticated/OAuth session and do not treat a lookup result as
    proof of identity without the surrounding trusted authentication flow.

  Behavior: Only active sys_user records are considered. The lookup must
  resolve to one user; ambiguous matches are not selected automatically.

  Success response 200:
  { sys_id, user_name, display_name, phone, mobile_phone, employee_id }
  employee_id is mapped from ServiceNow's employee_number field. The returned
  sys_id is the value expected as caller_id by the incident resources.

  Error responses: 400 when employee_id is missing, invalid, or an unsupported
  query parameter is supplied; 404 when no active user matches; 409 when more
  than one user matches. Authentication and REST Endpoint ACLs are configured
  on the Scripted REST resource rather than by this script.
 */
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    function trim(value) {
        return value === null || value === undefined ? '' : String(value).replace(/^\s+|\s+$/g, '');
    }

    function send(code, payload) {
        response.setStatus(code);
        response.setBody(payload);
    }

    var employeeId = trim(request.queryParams.employee_id);
    var phoneInput = trim(request.queryParams.phone_number);

    if (phoneInput) {
        send(400, { error: 'Only employee_id is supported' });
        return;
    }
    if (!/^\d{6}$/.test(employeeId)) {
        send(400, { error: 'employee_id is invalid' });
        return;
    }

    var users = new GlideRecordSecure('sys_user');
    users.addQuery('active', true);
    users.addQuery('employee_number', employeeId);

    users.setLimit(2);
    users.query();

    var matches = [];
    while (users.next()) {
        matches.push(users.getUniqueValue());
    }

    if (matches.length > 1) {
        send(409, { error: 'User lookup is ambiguous' });
        return;
    }
    if (!matches.length) {
        send(404, {});
        return;
    }

    var user = new GlideRecordSecure('sys_user');
    if (!user.get(matches[0])) {
        send(404, {});
        return;
    }

    send(200, {
        sys_id: user.getUniqueValue(),
        user_name: user.getValue('user_name'),
        display_name: user.getDisplayValue('name'),
        phone: user.getValue('phone'),
        mobile_phone: user.getValue('mobile_phone'),
        employee_id: user.getValue('employee_number')
    });
})(request, response);
