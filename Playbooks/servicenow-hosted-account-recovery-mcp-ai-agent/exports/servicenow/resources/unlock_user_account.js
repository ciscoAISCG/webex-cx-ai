/**
 * ServiceNow Scripted REST API - Unlock User Account (Webex CC AI Agent)
 *
 * Purpose: Clears the locked_out flag for an eligible user after identity verification.
 *
 * Endpoint:
 * - Method: POST
 * - Path: /unlock
 * - Authentication: required; ACL authorization required (REST Endpoint ACL limited to the caller role).
 *
 * Request:
 *   POST /unlock
 *   { "user_id": "<sys_user.sys_id>" }
 *
 * Parameters:
 * - user_id (required): 32-character sys_id of the sys_user record, from lookup_user.
 *
 * Responses:
 * - 200: { "success": true, "state_reason": "account_unlocked", "message": "...",
 *          "password_needs_reset": false, "locked_out": false }
 * - 200: { "success": true, "state_reason": "account_not_locked", "message": "...",
 *          "password_needs_reset": false, "locked_out": false }
 * - 200: { "success": false, "state_reason": "account_unlock_failed", "reason": "<code>", "message": "..." } user not eligible.
 *          reason: user_not_found | user_inactive | web_service_access_only | internal_integration_user |
 *                  excluded_role | not_enrolled
 * - 400: user_id missing or not a valid sys_id.
 * - 403: caller lacks the caller role, or caller tried to unlock its own account.
 * - 500: account update failed or unexpected error.
 *
 * Notes:
 * - Trusts the caller: verify_security_answers must succeed first; this endpoint does not re-verify.
 * - Not eligible: inactive, web-service-only, internal integration, excluded role, or not enrolled.
 * - Does not change the password; failed_attempts is reset to 0 when the field exists.
 * - System properties (optional, defaults shown):
 *   - webexccai.pwd_reset.caller_role    = webexccai_pwd_reset
 *   - webexccai.pwd_reset.excluded_roles = admin,security_admin,maint,impersonator,user_admin,oauth_admin
 */

(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    var SYS_ID_PATTERN = /^[0-9a-f]{32}$/;

    function send(httpStatus, payload) {
        response.setHeader('Cache-Control', 'no-store');
        response.setHeader('Pragma', 'no-cache');
        response.setStatus(httpStatus);
        response.setBody(payload);
    }

    function fail(httpStatus, message) {
        send(httpStatus, {
            success: false,
            state_reason: 'account_unlock_failed',
            message: message
        });
    }

    function trimString(value) {
        return (typeof value === 'string' || value instanceof String) ? String(value).trim() : '';
    }

    function isTrue(gr, field) {
        var value = gr.getValue(field);
        return value === '1' || value === 'true';
    }

    function hasExcludedRole(userId) {
        var excluded = gs.getProperty('webexccai.pwd_reset.excluded_roles',
            'admin,security_admin,maint,impersonator,user_admin,oauth_admin');
        var roles = new GlideRecord('sys_user_has_role');
        roles.addQuery('user', userId);
        roles.addQuery('role.name', 'IN', excluded);
        roles.setLimit(1);
        roles.query();
        return roles.hasNext();
    }

    function isEnrolled(userId) {
        var enrollment = new GlideRecord('pwd_enrollment');
        enrollment.addQuery('user', userId);
        enrollment.addQuery('status', '1');
        enrollment.setLimit(1);
        enrollment.query();
        return enrollment.hasNext();
    }

    function getIneligibleReason(user, userId) {
        if (!isTrue(user, 'active')) return 'user_inactive';
        if (user.isValidField('web_service_access_only') && isTrue(user, 'web_service_access_only')) return 'web_service_access_only';
        if (user.isValidField('internal_integration_user') && isTrue(user, 'internal_integration_user')) return 'internal_integration_user';
        if (hasExcludedRole(userId)) return 'excluded_role';
        if (!isEnrolled(userId)) return 'not_enrolled';
        return '';
    }

    var data = (request.body && request.body.data) || {};
    var userId = trimString(data.user_id);

    try {
        var callerRole = gs.getProperty('webexccai.pwd_reset.caller_role', 'webexccai_pwd_reset');
        if (!gs.hasRole(callerRole)) {
            fail(403, 'Caller is not authorized.');
            return;
        }

        if (!SYS_ID_PATTERN.test(userId)) {
            fail(400, 'A valid user_id is required.');
            return;
        }

        if (userId === gs.getUserID()) {
            fail(403, 'Caller is not authorized.');
            return;
        }

        var user = new GlideRecord('sys_user');
        var ineligibleReason = user.get(userId) ? getIneligibleReason(user, userId) : 'user_not_found';
        if (ineligibleReason) {
            send(200, {
                success: false,
                state_reason: 'account_unlock_failed',
                reason: ineligibleReason,
                message: 'User is not eligible for self-service account unlock.'
            });
            return;
        }

        if (!isTrue(user, 'locked_out')) {
            send(200, {
                success: true,
                state_reason: 'account_not_locked',
                message: 'Account is not locked.',
                password_needs_reset: isTrue(user, 'password_needs_reset'),
                locked_out: false
            });
            return;
        }

        user.setValue('locked_out', false);
        if (user.isValidField('failed_attempts')) user.setValue('failed_attempts', 0);
        if (!user.update()) {
            fail(500, 'Account unlock failed.');
            return;
        }

        var lockedOut = isTrue(user, 'locked_out');
        if (lockedOut) {
            fail(500, 'Account unlock failed.');
            return;
        }

        send(200, {
            success: true,
            state_reason: 'account_unlocked',
            message: 'Account unlocked.',
            password_needs_reset: isTrue(user, 'password_needs_reset'),
            locked_out: false
        });
    } catch (e) {
        fail(500, 'Account unlock failed.');
    }
})(request, response);
