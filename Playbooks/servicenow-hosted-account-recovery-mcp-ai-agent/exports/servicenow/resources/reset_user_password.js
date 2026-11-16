/**
 * ServiceNow Scripted REST API - Reset Password (Webex CC AI Agent)
 *
 * Purpose: Sets a temporary password for an eligible user and requires a change at next sign-in.
 *
 * Endpoint:
 * - Method: POST
 * - Path: /reset
 * - Authentication: required; ACL authorization required (REST Endpoint ACL limited to the caller role).
 *
 * Request:
 *   POST /reset
 *   { "user_id": "<sys_user.sys_id>" }
 *
 * Parameters:
 * - user_id (required): 32-character sys_id of the sys_user record, from lookup_user.
 *
 * Responses:
 * - 200: { "success": true, "state_reason": "password_reset_succeeded", "message": "...",
 *          "temporary_password": "...", "required_change": true, "password_needs_reset": true, "locked_out": false }
 * - 200: { "success": false, "state_reason": "password_reset_failed", "reason": "<code>", "message": "..." } user not eligible.
 *          reason: user_not_found | user_inactive | web_service_access_only | internal_integration_user |
 *                  excluded_role | not_enrolled
 * - 400: user_id missing or not a valid sys_id.
 * - 403: caller lacks the caller role, or caller tried to reset its own password.
 * - 500: password update failed or unexpected error.
 *
 * Notes:
 * - Trusts the caller: verify_security_answers must succeed first; this endpoint does not re-verify.
 * - Not eligible: inactive, web-service-only, internal integration, excluded role, or not enrolled.
 * - Temporary password: two pronounceable mixed-case words, two digits, and a symbol (! or =).
 *   Returned in plain text only; never logged.
 * - System properties (optional, defaults shown):
 *   - webexccai.pwd_reset.caller_role    = webexccai_pwd_reset
 *   - webexccai.pwd_reset.excluded_roles = admin,security_admin,maint,impersonator,user_admin,oauth_admin
 */

(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    var SYS_ID_PATTERN = /^[0-9a-f]{32}$/;

    // Excludes l (I/l confusion) and q, x, y (awkward in generated syllables).
    var CONSONANTS = 'bcdfghjkmnprstvwz';
    var VOWELS = 'aeiou';
    var SYLLABLES_PER_WORD = 2;
    var WORD_COUNT = 2;
    // Voice-safe: no 0/1 (O/l confusion), specials match the existing agent prompt.
    var DIGITS = '23456789';
    var SPECIALS = ['!', '='];

    function send(httpStatus, payload) {
        response.setHeader('Cache-Control', 'no-store');
        response.setHeader('Pragma', 'no-cache');
        response.setStatus(httpStatus);
        response.setBody(payload);
    }

    function fail(httpStatus, stateReason, message) {
        send(httpStatus, {
            success: false,
            state_reason: stateReason,
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

    function secureIndex(length) {
        return GlideSecureRandomUtil.getSecureRandomIntBound(length);
    }

    function pick(chars) {
        return chars.charAt(secureIndex(chars.length));
    }

    function randomCase(letter) {
        return secureIndex(2) === 0 ? letter.toUpperCase() : letter;
    }

    // Each syllable is consonant + vowel, optionally followed by a consonant.
    function generateWord() {
        var word = '';
        for (var s = 0; s < SYLLABLES_PER_WORD; s++) {
            word += pick(CONSONANTS) + pick(VOWELS);
            if (secureIndex(2) === 0) word += pick(CONSONANTS);
        }
        var cased = '';
        for (var i = 0; i < word.length; i++) {
            cased += randomCase(word.charAt(i));
        }
        return cased;
    }

    function generateTemporaryPassword() {
        var letters;
        do {
            letters = '';
            for (var w = 0; w < WORD_COUNT; w++) {
                letters += generateWord();
            }
        } while (!/[A-Z]/.test(letters) || !/[a-z]/.test(letters));
        return letters + pick(DIGITS) + pick(DIGITS) + SPECIALS[secureIndex(SPECIALS.length)];
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
            fail(403, 'password_reset_failed', 'Caller is not authorized.');
            return;
        }

        if (!SYS_ID_PATTERN.test(userId)) {
            fail(400, 'password_reset_failed', 'A valid user_id is required.');
            return;
        }

        if (userId === gs.getUserID()) {
            fail(403, 'password_reset_failed', 'Caller is not authorized.');
            return;
        }

        var user = new GlideRecord('sys_user');
        var ineligibleReason = user.get(userId) ? getIneligibleReason(user, userId) : 'user_not_found';
        if (ineligibleReason) {
            send(200, {
                success: false,
                state_reason: 'password_reset_failed',
                reason: ineligibleReason,
                message: 'User is not eligible for self-service password reset.'
            });
            return;
        }

        var temporaryPassword = generateTemporaryPassword();
        user.user_password.setDisplayValue(temporaryPassword);
        user.setValue('password_needs_reset', true);
        if (!user.update()) {
            fail(500, 'password_reset_failed', 'Password reset failed.');
            return;
        }

        var requiredChange = isTrue(user, 'password_needs_reset');
        send(200, {
            success: true,
            state_reason: 'password_reset_succeeded',
            message: requiredChange
                ? 'Password reset succeeded. The user must change it at next sign-in.'
                : 'Password reset succeeded.',
            temporary_password: temporaryPassword,
            required_change: requiredChange,
            password_needs_reset: requiredChange,
            locked_out: isTrue(user, 'locked_out')
        });
    } catch (e) {
        fail(500, 'password_reset_failed', 'Password reset failed.');
    }
})(request, response);
