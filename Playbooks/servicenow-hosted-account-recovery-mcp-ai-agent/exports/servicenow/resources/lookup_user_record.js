/**
 * ServiceNow Scripted REST API - Lookup User (Webex CC AI Agent)
 *
 * Purpose: Resolves exactly one active sys_user by employee ID and returns its sys_id.
 *
 * Endpoint:
 * - Method: GET
 * - Path: /users
 * - Authentication: required; REST Endpoint ACLs are configured on the Scripted REST resource.
 *
 * Request:
 *   GET /users?employee_id=<6 digits>
 *
 * Parameters:
 * - employee_id (required): exactly six digits, matched against sys_user.employee_number.
 *
 * Responses:
 * - 200: { "sys_id": "<sys_user.sys_id>", "user_name": "...", "display_name": "...",
 *          "phone": "...", "mobile_phone": "...", "employee_id": "<employee_number>",
 *          "password_needs_reset": false, "locked_out": false }
 * - 400: employee_id missing or invalid, or phone_number supplied.
 * - 404: no active user matches (empty body).
 * - 409: more than one active user matches.
 *
 * Notes:
 * - Only active users are considered; ambiguous matches are never selected automatically.
 * - Employee ID is a lookup value, not a credential; a match is not proof of identity.
 * - Pass the returned sys_id as user_id to retrieve_security_questions, verify_security_answers,
 *   reset_user_password, and unlock_user_account.
 */
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    var EMPLOYEE_ID_PATTERN = /^\d{6}$/;

    function trimString(value) {
        return value === null || value === undefined ? '' : String(value).replace(/^\s+|\s+$/g, '');
    }

    function isTrue(gr, field) {
        var value = gr.getValue(field);
        return value === '1' || value === 'true';
    }

    function send(httpStatus, payload) {
        response.setStatus(httpStatus);
        response.setBody(payload);
    }

    var employeeId = trimString(request.queryParams.employee_id);
    var phoneNumber = trimString(request.queryParams.phone_number);

    if (phoneNumber) {
        send(400, { error: 'Only employee_id is supported' });
        return;
    }
    if (!EMPLOYEE_ID_PATTERN.test(employeeId)) {
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
        employee_id: user.getValue('employee_number'),
        password_needs_reset: isTrue(user, 'password_needs_reset'),
        locked_out: isTrue(user, 'locked_out')
    });
})(request, response);
