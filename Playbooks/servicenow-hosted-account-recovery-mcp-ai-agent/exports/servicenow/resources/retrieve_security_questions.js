/**
 * ServiceNow Scripted REST API - Get Security Questions (Webex CC AI Agent)
 *
 * Purpose: Returns the active password-reset security questions enrolled for a user.
 *
 * Endpoint:
 * - Method: GET
 * - Path: /questions/{user_id}
 * - Authentication: required
 *
 * Request:
 *   GET /questions/<sys_user.sys_id>
 *   GET /questions?user_id=<sys_user.sys_id>
 *
 * Parameters:
 * - user_id (required): 32-character sys_id of the sys_user record, from lookup_user.
 *
 * Responses:
 * - 200: { "success": true, "user_sys_id": "<sys_user.sys_id>",
 *          "questions": [ { "sys_id": "<pwd_active_question.sys_id>", "question": "<text>" } ] }
 * - 400: user_id missing or not a valid sys_id.
 * - 404: user not found, user not enrolled, or no active questions.
 * - 500: unexpected error.
 *
 * Notes:
 * - user_id is accepted as a path parameter or a query parameter.
 * - Pass each returned question sys_id as question_id to verify_answers.
 */
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    var SYS_ID_PATTERN = /^[0-9a-f]{32}$/;

    try {
        // Get user sys_id from path parameter or query string
        var userId = String(request.pathParams.user_id || request.queryParams.user_id || '').trim();

        // Validate input
        if (!SYS_ID_PATTERN.test(userId)) {
            response.setStatus(400);
            response.setBody({
                error: 'Bad Request',
                message: 'A valid user_id (sys_user sys_id) parameter is required'
            });
            return;
        }

        // Step 1: Confirm user record exists
        var user = new GlideRecord('sys_user');
        if (!user.get(userId)) {
            response.setStatus(404);
            response.setBody({
                error: 'Not Found',
                message: 'No user found with user_id: ' + userId
            });
            return;
        }

        // Step 2: Get enrollment record for the user
        var enrollment = new GlideRecord('pwd_enrollment');
        enrollment.addQuery('user', userId);
        enrollment.addFields('sys_id');
        enrollment.setLimit(1);
        enrollment.query();

        if (!enrollment.next()) {
            response.setStatus(404);
            response.setBody({
                error: 'Not Found',
                message: 'No enrollment found for user',
                user_sys_id: userId
            });
            return;
        }

        var enrollmentId = enrollment.getValue('sys_id');

        // Step 3: Get active answers for the enrollment
        var answers = new GlideRecord('pwd_active_answer');
        answers.addQuery('enrollment', enrollmentId);
        answers.addFields('active_question');
        answers.query();

        // Build array of questions
        var questions = [];

        while (answers.next()) {
            var questionId = answers.getValue('active_question');

            if (questionId) {
                // Get question details from pwd_active_question
                var question = new GlideRecord('pwd_active_question');
                if (question.get(questionId)) {
                    questions.push({
                        sys_id: question.getValue('sys_id'),
                        question: question.getValue('question') || ''
                    });
                }
            }
        }

        // Check if any questions found
        if (questions.length === 0) {
            response.setStatus(404);
            response.setBody({
                error: 'Not Found',
                message: 'No active questions found for user',
                user_sys_id: userId
            });
            return;
        }

        // Return successful response
        response.setStatus(200);
        response.setBody({
            success: true,
            user_sys_id: userId,
            questions: questions
        });

    } catch (e) {
        // Handle errors
        response.setStatus(500);
        response.setBody({
            error: 'Internal Server Error',
            message: e.message || 'An unexpected error occurred',
            details: e.toString()
        });
    }

})(request, response);