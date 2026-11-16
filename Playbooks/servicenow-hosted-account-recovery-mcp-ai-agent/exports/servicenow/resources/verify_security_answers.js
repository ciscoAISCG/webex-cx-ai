/**
 * ServiceNow Scripted REST API - Verify Security Answers (Webex CC AI Agent)
 *
 * Purpose: Checks the caller's answers against the user's enrolled security questions.
 *
 * Endpoint:
 * - Method: POST
 * - Path: /answers
 * - Authentication: required
 *
 * Request:
 *   POST /answers
 *   {
 *     "user_id": "<sys_user.sys_id>",
 *     "questions_answers": [
 *       { "question_id": "<pwd_active_question.sys_id>", "user_answer": "<answer>" }
 *     ]
 *   }
 *
 * Parameters:
 * - user_id (required): 32-character sys_id of the sys_user record, from lookup_user.
 * - questions_answers (required): 3 entries using question sys_ids from get_questions;
 *   only the first 3 are checked.
 *
 * Responses:
 * - 200: { "success": true,  "message": "Verification succeeded." }
 * - 200: { "success": false, "message": "Verification failed. Incorrect question IDs: ..." }
 * - 400: missing parameters, num_reset undefined or not 3, too few answers, or a missing question/answer.
 *
 * Notes:
 * - Passes when at least 2 of the 3 answers are correct.
 * - verification_id is hard-coded in VERIFICATION_ID; its num_reset must be 3.
 * - Call reset_password with the same user_id only after success is true.
 */
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {
    // Configure webexccai.pwd_reset.verification_id with the target instance's Security Questions verification sys_id.
    var VERIFICATION_ID = gs.getProperty('webexccai.pwd_reset.verification_id', '');
    if (!/^[0-9a-f]{32}$/i.test(VERIFICATION_ID)) {
        response.setStatus(500);
        response.setBody({ success: false, message: 'Security-question verification is not configured.' });
        return;
    }

    var userId = request.body.data.user_id;
    var questionsAnswers = request.body.data.questions_answers || [];

    // Validate required parameters
    if (!userId || questionsAnswers.length === 0) {
        response.setStatus(400);
        response.setBody({
            success: false,
            message: 'Missing required parameters.'
        });
        return;
    }

    var numReset = new SNC.PwdVerificationManager().getVerificationParamValue(VERIFICATION_ID, 'num_reset');
    if (numReset === undefined) {
        response.setStatus(400);
        response.setBody({ success: false, message: 'num_reset is undefined.' });
        return;
    }
    numReset = parseInt(numReset);
    if (numReset !== 3) {
        response.setStatus(400);
        response.setBody({ success: false, message: 'This version expects exactly 3 questions.' });
        return;
    }
    if (questionsAnswers.length < numReset) {
        response.setStatus(400);
        response.setBody({ success: false, message: 'Not enough answers provided.' });
        return;
    }
    var correctCount = 0;
    var incorrectQuestionIds = [];
    for (var i = 0; i < numReset; i++) {
        var qa = questionsAnswers[i];
        var questionId = qa.question_id;
        var userAnswer = qa.user_answer;
        if (userAnswer) userAnswer = userAnswer.trim();
        if ((questionId === undefined) || (userAnswer === undefined)) {
            response.setStatus(400);
            response.setBody({ success: false, message: 'Question or answer is undefined at index ' + i });
            return;
        }
        var answer = new GlideRecord('pwd_active_answer');
        answer.addJoinQuery('pwd_enrollment', 'enrollment', 'sys_id');
        answer.addQuery('enrollment.verification', VERIFICATION_ID);
        answer.addQuery('enrollment.user', userId);
        answer.addQuery('active_question', questionId);
        answer.query();
        if (!answer.next()) {
            incorrectQuestionIds.push(questionId);
            continue;
        }
        var isCorrect = new SNC.PwdQAManager().compareAnswers(answer.sys_id, userAnswer, false);
        if (isCorrect) {
            correctCount++;
        } else {
            incorrectQuestionIds.push(questionId);
        }
    }
    if (correctCount >= 2) {
        response.setStatus(200);
        response.setBody({ success: true, message: 'Verification succeeded.' });
        return;
    } else {
        response.setStatus(200);
        response.setBody({ success: false, message: 'Verification failed. Incorrect question IDs: ' + incorrectQuestionIds.join(', ') });
        return;
    }
})(request, response);