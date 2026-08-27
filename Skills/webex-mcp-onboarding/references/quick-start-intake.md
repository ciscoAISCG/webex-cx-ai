# Quick Start Intake

Use this when a user says something like:

- "I want to add XYZ MCP server to my AI agent."
- "Can you help me connect this MCP server in Webex?"
- "Add this MCP tool to Studio."

Do not start with the full intake table. Make it easy. Ask only the few details needed to begin the Developer Portal onboarding form.

## Start Link

Use the direct Agentic App form link by default:

`https://developer.webex.com/my-apps/new/agentic-server`

Tell the user they may be prompted to log in. If the direct link changes or fails, fall back to `https://developer.webex.com` and navigate through My Webex Apps or Start Building Apps.

## First Response Pattern

Respond with:

1. One sentence confirming the goal.
2. A short MCP fit note.
3. The direct Agentic App link and a short note that login may be required.
4. Three or fewer questions, plus assumptions.

Example:

```markdown
Yes. We'll add `<server-name>` as an Agentic App, provision it in Control Hub, then add its MCP tools as actions in Studio.

MCP is a good fit if you already have a hosted MCP server and the security/data path is acceptable. If not, we may want Webex Connect for fulfillment instead.

Open this first and log in if prompted:
https://developer.webex.com/my-apps/new/agentic-server

I'll assume `Streamable HTTP` unless you tell me otherwise, and we do not need to pick the Studio agent until the Studio phase.

To start, I need:

1. What is the MCP server App URL?
2. What auth type should we use: OAuth2 client credentials, API key, or custom header?
3. Is the MCP server already hosted/approved, or are we only prototyping?
```

If the user does not know the answer to a question, continue with `TBD` and convert it into an open item in the build recipe.

If the user only knows the server name, create a draft onboarding checklist with `TBD` values and guide them to find the missing App URL and auth type.

If the user does not have a hosted MCP server or hosting owner, pause MCP onboarding and explain the options: build/host an MCP server first, use a lab/prototype server, or consider Webex Connect for fulfillment.

## New User Form-Fill Mode

When the user is new or says "walk me through it," guide the visible form line by line:

| Form field | Default guidance |
|---|---|
| Agentic App Module | Select or confirm `MCP`. |
| Agentic App URL | Enter the public HTTPS MCP server URL. |
| Transport Type | Keep `Streamable HTTP` unless the server requires `HTTP SSE`. |
| Agentic App Name | Use a short unique name derived from the server or use the user's preferred name. |
| Agentic App Description | Draft a concise capability description in user-safe language. |
| Agentic App Icon | Use a default icon unless the user has an approved 512x512 PNG/JPEG. |
| Agentic App auth type | Select only a team-supported option: OAuth2 client credentials, API key, or custom header. |
| Add Agentic App | Pause before clicking; confirm all required fields and auth/secret handling. |

If choosing an auth type reveals more fields, guide those fields next. Do not ask the user to paste secrets into chat; tell them to enter secrets directly into the GUI.

## Progressive Questions

After the first answers, ask only what is needed for the next phase.

### Developer Portal Phase

Ask for:

- Agentic App name.
- Description/purpose.
- Logo choice: approved 512x512 PNG/JPEG or default option.
- App URL.
- Transport type. Default to `Streamable HTTP`; use `HTTP SSE` only when the user or server requires it.
- Auth type. Current team-supported options are OAuth2 client credentials, API key, and custom header. Do not offer OAuth2 authorization code or user token unless the team confirms support has changed.

### Control Hub Phase

Ask for:

- Open `https://admin.webex.com/apps/agentic-servers` and log in if prompted.
- Control Hub org/tenant.
- Admin access confirmation.
- Whether the newly onboarded server is visible under Apps -> Agentic Apps.
- Whether the server shows Access `Blocked` with a red dot.
- Confirmation before selecting `Allowed for all users`, enabling `Authorize automatic server data updates`, and clicking Save.
- Confirm the Authentication tab type matches the Developer Portal auth choice.
- For custom headers, provide only the header key names in chat; enter header values directly in the GUI.
- Which tools/resources/prompts to enable.
- If the Tools tab is empty, stop and troubleshoot auth/server setup before Studio.
- Which visible tools should be made available to Studio.
- Whether any write/action tools should remain disabled.
- Whether `Allow signature change` should stay off or be enabled intentionally.
- Whether automatic server data updates should be allowed.
- Auth values owner, without asking for secrets in chat.

### Studio Phase

Ask for:

- Open `https://studio.aiagent-us1.cisco.com/static/core/viewbots` and log in if prompted.
- Target agent name.
- Which MCP tools to add as actions.
- Open the existing agent, then go to `Configuration` -> `Actions`.
- Click `+ Add actions`, choose `Select available`, and search for the MCP server or tool name.
- Confirm the available action row shows source `From <provider> • MCP`.
- Select the intended tools and pause before clicking `Add`.
- When the agent should call each tool.
- Whether the tools need orchestration, such as tool order, output handoff, or confirmation before action tools.
- What agent instructions should be added after the actions are attached.
- Safe test input.
- Expected success output.
- Expected failure behavior.

### Validation Phase

Ask for:

- Direct tool test result.
- Studio action status result.
- Conversation test transcript or screenshot.
- Production blockers.

## Default Assumptions

When not specified:

- Audience: `both`.
- Environment: `sandbox/lab` until confirmed otherwise.
- Transport type: `Streamable HTTP`.
- Logo: default option until an approved 512x512 PNG/JPEG is provided.
- Automation level: `guided`.
- Secrets: user-entered only, never pasted into chat.
- Playbook: optional output after one real walkthrough.

## Do Not Ask First

Avoid asking these until needed:

- Full schemas for every tool.
- Complete playbook details.
- Screenshots from all three platforms.
- Production deployment approvals.
- Credentials or token values.
- Target Studio agent before Developer Portal and Control Hub onboarding are complete.
