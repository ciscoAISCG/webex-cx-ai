# Webex AI Agent Studio Setup Reference

Source:

- https://help.webexconnect.io/docs/getting-started-with-webex-ai-agent-studio

## Access Paths

Webex AI Agent Studio can be opened from Control Hub or Webex Connect.

From Control Hub:

1. Sign in at `https://admin.webex.com`.
2. Go to Services.
3. Select Contact Center.
4. In Quick Links, find Contact Center Suite.
5. Open Webex AI Agent Studio.

If the option is not visible, Cisco Support may need to enable the feature flag.

From Webex Connect:

1. Sign in to the Webex Connect tenant URL.
2. Open the App Tray from the left navigation pane.
3. Select Webex AI Agent Studio.

## Setup Guide Pattern

Use this setup flow in final answers, adapting labels to the user's tenant and use case:

1. Confirm access.
   - Confirm the user can access Webex AI Agent Studio from Control Hub or Webex Connect.
   - Confirm the tenant, environment, and target channel.

2. Create or open the AI agent.
   - Create a new agent for the use case or update an existing one.
   - Set the agent name, description, target audience, language, and channel.

3. Add instructions.
   - Paste the generated AI Agent Instructions into the agent instruction field.
   - Keep durable behavior in instructions and use case-specific records in systems or knowledge sources.

4. Configure knowledge, if needed.
   - Add approved knowledge sources for FAQs, policies, troubleshooting articles, or service details.
   - Instruct the agent to use knowledge only within the defined scope.

5. Configure actions.
   - Add each recommended action in the Actions tab.
   - Ensure action names match the generated instructions exactly.
   - Define required and optional parameters.
   - Connect each action to its fulfillment flow or backend API.

6. Configure fulfillment flows.
   - Use Webex Connect fulfillment flows or backend APIs to execute business operations.
   - Keep validation, branching, system calls, and record updates in the fulfillment layer when deterministic behavior is required.
   - Return clear success, no-match, validation-error, and system-error responses for the agent to handle.

7. Configure escalation.
   - Define when the agent should transfer to a human agent or create a support case.
   - Include failure thresholds and sensitive-case routing.

8. Test.
   - Test happy paths, missing inputs, invalid inputs, no-match responses, action failures, out-of-scope requests, and escalation.
   - Verify that the agent collects required parameters before action calls and never fabricates results.

9. Publish and monitor.
   - Publish only after tests pass.
   - Monitor conversation quality, action success rates, containment, escalations, and failure reasons.

## Action Table Columns

Use these columns when recommending actions:

- Action
- Purpose
- Trigger
- Required parameters
- Optional parameters
- Fulfillment flow/API
- Success response
- Failure handling

## Common Action Patterns

- `check_ticket_status`: ticket ID, requester email, or verified user ID.
- `create_ticket`: requester details, issue category, description, priority, attachments if supported.
- `book_appointment`: customer ID, appointment type, preferred date/time, location, contact details.
- `get_available_slots`: appointment type, location, date range, provider or team.
- `cancel_appointment`: appointment ID, verified customer ID, cancellation reason.
- `reschedule_appointment`: appointment ID, preferred date/time, location, appointment type.
- `lookup_customer`: customer identifier, authentication attributes.
- `transfer_to_agent`: reason, summary, customer details, transcript or context.
