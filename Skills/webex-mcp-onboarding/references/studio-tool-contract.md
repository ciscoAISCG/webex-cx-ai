# Studio Tool Contract

Use this reference when binding MCP tools into AI Agent Studio and writing the agent instructions.

## Studio Entry

Use the AI Agent Studio agent list deep link by default:

`https://studio.aiagent-us1.cisco.com/static/core/viewbots`

This page can be cross-launched from Control Hub, but the deep link is useful for guided setup. Tell the user to log in if prompted.

For this skill's v1 walkthrough, assume the user is adding MCP tools to an existing autonomous agent rather than creating a new agent.

## Observed Agent List

From the current observed Studio screen:

- Page title: `AI Agents`.
- Left sidebar shows Webex/Studio navigation icons.
- Top controls include search by agent name, filter by type, and filter by creator.
- Top-right actions include `Import agent` and `Create agent`.
- Agents appear as cards.
- Each card shows agent name, `Autonomous` tag, last updated date, creator, overflow menu, and `Preview`.
- Use search/filter to find the target existing agent.
- Open or preview the target existing agent before adding MCP actions.

Do not ask for the target agent before Developer Portal and Control Hub setup are complete. Ask for the existing target agent name at this stage.

## Observed Existing Agent Actions Screen

After selecting an existing agent:

- The agent detail header shows the agent name, last updated metadata, `Preview`, overflow menu, and `Publish`.
- The left navigation includes `Configuration`, `Sessions`, `History`, and `Analytics`.
- In `Configuration`, open the `Actions` area/tab.
- The actions table shows enabled/disabled toggles, action names, descriptions, last updated values, action type such as `MCP`, and controls such as delete.
- The upper-right actions area includes `What is an action?` and `+ Add actions`.
- To add MCP tools, click `+ Add actions`, then choose `Select available` when prompted.

The observed `Add actions` modal includes:

- Title `Add actions`.
- Search field placeholder: `Search by action name, description, or provider`.
- Available action rows with checkbox, icon, action name, info icon, and source line such as `From <provider> • MCP`.
- Selected counter such as `Selected (0/5)`.
- `Cancel` and `Add` buttons.

Select only the MCP actions that were intentionally enabled in Control Hub. The `Add` button may remain disabled until at least one action is selected.

## Action Selection Pattern

When adding actions:

1. Search by tool name, server/provider name, description, or action keyword.
2. Check each action that should be available to the agent.
3. Confirm the selected count increases, such as `Selected (1/5)`.
4. Do not select extra tools just because they are available.
5. Click `Add` only after confirming the selected action list.
6. Back in the agent configuration, confirm each added action appears in the Actions table.

If the same MCP server exposes multiple tools, add only the subset needed for the current agent scenario. Prefer a smaller action set plus clear instructions over broad tool exposure.

## Agent Instructions After Actions

Adding MCP actions is not enough. Return to the agent configuration and add or update the agent instructions so the model knows how to use the tools.

For simple tools, include:

- The exact condition for calling the tool.
- Required information to collect before the call.
- What to summarize to the user.
- What not to reveal.
- Failure handling.

For complicated tools or orchestration, include:

- Tool order.
- Preconditions before each tool call.
- Which output from one tool becomes input to the next tool.
- Confirmation gates before write/action tools.
- Retry limits.
- Handoff or escalation rules.
- User-safe success and failure language.

Treat the exact Studio editor path for instructions as UI-dependent until observed in the tenant. Look for the agent profile, instruction, behavior, or configuration text area and pause before saving changes.

## Contract Fields

Define each MCP tool with:

- Tool name as shown in Studio.
- Business purpose.
- When the agent may call it.
- Required inputs.
- Optional inputs.
- Sensitive inputs.
- Expected success response.
- Expected failure response.
- User-safe response language.
- Retry and handoff behavior.
- Data the agent must never reveal.

## Prompt Pattern

Use concise sections:

```markdown
## MCP Tool Use

Use `<tool-name>` only when <condition>.

Before calling:
- Collect <required input>.
- Confirm <field> if needed.
- Do not request or expose <restricted data>.

On success:
- Summarize <safe output>.

On failure:
- Try <bounded retry or fallback>.
- If still failing, <handoff/escalation>.
```

## Validation Before Conversation Testing

- Open `https://studio.aiagent-us1.cisco.com/static/core/viewbots`.
- Select an existing autonomous agent.
- Confirm the tool was enabled on the Control Hub Tools tab first.
- Open `Configuration` -> `Actions`.
- Click `+ Add actions`, choose `Select available`, and confirm the MCP action appears in the modal.
- Search by action name, description, provider, or MCP server name if the list is long.
- Select only intended MCP actions and click `Add`.
- Return to the agent configuration and add/update instructions for when and how to use the MCP tools.
- For orchestrated scenarios, describe tool order, required inputs, confirmation gates, retries, and handoff behavior.
- Confirm the tool description matches the intended use.
- Confirm tool details were synchronized from the Developer Portal or Control Hub definition.
- Confirm the agent prompt tells the model when to call and when not to call.
- Test with safe sample inputs.
- Confirm failure messages do not leak raw backend errors or secrets.

## Studio Constraints To Check

- MCP actions may be read-only after creation. If settings are wrong, expect to create a new action or update the server definition at registration/provisioning.
- Tool name, description, input entities, and data types may be populated from the MCP server definition.
- Group-level access control may not be available; check current docs and tenant behavior before promising group scoping.
- Maximum actions per agent can be org-configuration dependent.
- Verify execution state, latency, server name/ID, and transaction ID when the UI exposes them.

## Common Design Mistakes

- Tool is enabled but prompt never tells the agent when to use it.
- Tool name differs between Control Hub, Studio, and documentation.
- Tool has broad capability but no guardrails.
- Agent can call a write/action tool without confirmation.
- Agent exposes raw tool output instead of a user-safe summary.
