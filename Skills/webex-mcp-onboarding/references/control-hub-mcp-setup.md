# Control Hub Agentic App Provisioning

Use this reference for the Control Hub portion of MCP setup after the MCP server has been registered as an Agentic App in the Webex Developer Portal.

The exact UI can vary by tenant, role, and release. Do not invent click paths. Capture screenshots or use a browser session to refine exact steps.

## Control Hub Entry

The official docs currently describe the entry as Control Hub -> Apps -> Agentic Apps. Use the current docs and observed UI before customer-facing work.

The Agentic Apps page can include public Agentic Apps plus private apps onboarded by users in the organization.

After Developer Portal onboarding, guide the user to sign into Control Hub with the same Cisco identity when appropriate.

Use the direct Control Hub Agentic Apps link by default:

`https://admin.webex.com/apps/agentic-servers`

If the deep link fails or redirects unexpectedly, start from `https://admin.webex.com` and navigate to Apps -> Agentic Apps.

## Observed Agentic Apps List

From the current observed Control Hub screen:

- Left navigation: Management -> Apps.
- Top app categories include General, Integrations, Bots, Embedded Apps, Assistant Skills, Service Apps, and Agentic Apps.
- `Agentic Apps` appears as a selected tab/chip.
- Secondary filters include All, Webex, and External.
- Table columns include Server name, Type, Access, and Last updated.
- External MCP rows show Type as `External MCP serv...`.
- Access status uses colored dots: green `Allowed`, red `Blocked`.
- A newly onboarded MCP server is expected to appear with Access `Blocked` until the admin configures/allows it.
- Click the server row/name to open its configuration.

If the newly onboarded server does not appear, check the active org, login identity, Developer Portal ownership, and whether approval/provisioning is still pending.

## Provisioning Checks

### 1. Find The Agentic App

Confirm:

- Active Control Hub org/tenant.
- Agentic App name from Developer Portal.
- The server row appears in Apps -> Agentic Apps.
- The Type shows an external MCP server.
- The Access status is initially `Blocked` with a red dot, unless it has already been configured.
- Public/private status.
- Whether the app is allowed or blocked for the org.
- Whether automatic server data updates are allowed.

### 2. Allow Access On The General Tab

From the current observed detail page:

- Header shows the Agentic App name, Access status, and server type.
- Tabs include General, Authentication, Tools, Resources, and Prompts.
- General tab has an Access panel with:
  - `Blocked for all users`
  - `Allowed for all users`
  - `Authorize automatic server data updates` toggle
- About panel shows Description, Server type, Server URL, Redirect URI, App Hub submission status, App Hub visibility, and Last updated.
- Bottom-right actions include Cancel and Save.

For a normal enablement walkthrough:

1. Confirm the selected server is the newly onboarded MCP server.
2. Confirm this is the correct org/tenant.
3. Select `Allowed for all users`.
4. Turn on `Authorize automatic server data updates`.
5. Pause and ask the user to confirm before saving, because this changes org access.
6. Click Save.
7. Verify the header/list status changes from `Blocked` to `Allowed`.

### 3. Configure Authentication

Confirm the authentication section matches the Developer Portal registration:

- OAuth 2.0 client credentials.
- API key.
- Custom headers.

Expected inputs vary by auth type. Pause before entering client secrets, API keys, custom headers, or production credentials.

From the current observed Authentication tab:

- The tab row remains General, Authentication, Tools, Resources, and Prompts.
- The panel explains that authorization secures access to sensitive resources and operations exposed by MCP servers.
- `Authentication type` displays the type selected during Developer Portal onboarding.
- For `Custom headers`, the UI allows up to 5 custom headers.
- Each custom header row includes `Key` and `Value` fields.
- An `Add header` button adds another key/value pair.
- A trash/delete icon removes a header row.

For a custom-header walkthrough:

1. Click the Authentication tab.
2. Confirm `Authentication type` is `Custom headers`.
3. Ask the user for the header key name only if it is not known from the server documentation.
4. Tell the user to enter the header value directly into Control Hub. Do not ask them to paste the secret into chat.
5. Use `Add header` only when the MCP server requires more than one header.
6. Pause before Save because this stores authentication material.
7. Click Save after confirmation.

For OAuth2 client credentials or API key, follow the same pattern: confirm the auth type matches Developer Portal, guide the visible required fields, and have the user enter secret values directly into the GUI.

### 4. Configure Capabilities

For MCP servers, expect capability areas for tools, resources, and prompts.

The Tools tab is the first practical authentication success check. If authentication is successful, Control Hub should list the tools exposed by the MCP server. If no tools appear, treat authentication or server connectivity/configuration as failed and troubleshoot before moving to Studio.

From the current observed Tools tab:

- The left panel explains that tools allow the LLM to invoke actions through the server, including operations that may modify data or trigger connected workflows.
- The tool table includes columns:
  - `Tool`
  - `Allow tool`
  - `Allow signature change`
  - `Details`
- Each tool row has an `Allow tool` toggle.
- Each tool row has an `Allow signature change` toggle.
- Each tool row has a `Review` button under Details.
- The observed example list includes account summary, transaction history, account transfer, and payment status style tools.

Confirm:

- Tool list shown in Control Hub.
- If no tools are shown, stop and troubleshoot authentication/server setup.
- Which tools should be enabled for the target AI agent.
- Which tools should remain disabled.
- Input schema, output schema, and annotations for each enabled tool.
- Whether a tool schema/signature changed after authorization.
- Whether reauthorization is required.

Document the visible tool names exactly as shown in the UI.

For a normal tools walkthrough:

1. Click the Tools tab.
2. Confirm the expected MCP tools are visible.
3. For each tool, decide whether it is needed by the target agent use case.
4. Toggle `Allow tool` on only for tools that should be available to Studio.
5. Treat write/action tools more carefully than read-only tools; require explicit user confirmation before enabling them.
6. Use `Review` to inspect details when a tool purpose, input schema, output schema, or risk is unclear.
7. Decide whether `Allow signature change` should be enabled. Prefer leaving it off unless the team wants the tool schema to update automatically.
8. Click Save after confirming the enabled tool list.
9. Record the exact enabled tool names; these are the tools to bring into AI Agent Studio.

### 5. Govern Access

Confirm:

- Org-level allow/block state.
- Least-privilege alignment.
- Any approval, trust, or verification status.

### 6. Validate Studio Visibility

Confirm:

- The target Studio agent can see the MCP server or selected tools.
- Tools appear with expected names/descriptions.
- Permission errors are not present.
- The setup can be tested without production data.

## Evidence Checklist

- Tenant/org name.
- Agentic App name and app ID, if visible.
- MCP server name.
- Transport and auth type.
- Tool names and enabled/disabled status.
- Enabled tools that should be added in Studio.
- Org allow/block and capability configuration.
- Automatic server data updates authorization state.
- Authentication tab type and confirmation that required auth fields were saved without recording secret values.
- Schema review or reauthorization status.
- Studio visibility result.
- Direct tool test result.
- Conversation test result.

## Automation Level

Default early work to `guided`. Move steps to `browser-assisted` only after the screen state is observed and repeatable. Treat secret entry, production enablement, and publish actions as confirmation gates.
