# Developer Portal Agentic App Registration

Use this reference for the Webex Developer Portal portion of MCP onboarding.

The current official docs place MCP server onboarding in the Webex Developer Portal as Agentic App registration. Check `references/official-webex-docs.md` before customer-facing work because labels and supported options can change.

## Prerequisites

- Access to `https://developer.webex.com`.
- A deployed MCP server reachable over HTTPS.
- Authentication details for the MCP app.
- App name, description, owner, and purpose.
- Logo plan: upload an approved 512x512 PNG/JPEG or use a provided default option.
- Transport choice: default to `Streamable HTTP`; use `HTTP SSE` only when required by the server or user.
- Auth type choice for the current team-supported workflow:
  - OAuth2 client credentials.
  - API key.
  - Custom header based auth.

Official Webex docs may list OAuth2 authorization code and user token. Do not offer them in the default workflow until the team confirms support has changed.

## Registration Flow

Use this as a guide, not a substitute for the current docs or observed UI:

1. Open `https://developer.webex.com/my-apps/new/agentic-server`.
2. Log in if prompted.
3. If the direct link fails, open `https://developer.webex.com`, then use Start Building Apps or My Webex Apps to create a new Agentic App.
4. Enter app details:
   - Module: MCP.
   - Agentic App URL.
   - Transport type.
   - Agentic App name.
   - Agentic App description.
   - Agentic App icon.
   - Agentic App auth type.
5. Add the Agentic App.
6. Capture the resulting details page, app ID, configuration, and any approval/provisioning prompts.

## Visible Form Fields

From the current observed form:

| Field | Notes |
|---|---|
| Agentic App Module | `MCP` radio option is visible. |
| Agentic App URL | Placeholder is `https://URL`; requires public HTTPS endpoint. |
| Transport Type | `Streamable HTTP` and `HTTP SSE` are visible; default to `Streamable HTTP`. |
| Agentic App Name | Unique name for the Agentic App. |
| Agentic App Description | Supports markdown; current form shows a 1024 character limit. |
| Agentic App Icon | Upload or choose Default 1, Default 2, or Default 3. Upload must be exactly 512x512 PNG/JPEG. |
| Agentic App auth type | Dropdown appears after icon choices. Team-supported defaults are OAuth2 client credentials, API key, and custom header. |
| Add Agentic App | Disabled until required fields are complete. Pause before clicking. |

## After Registration

From the details page, expect to manage or capture:

- App ID and configuration.
- Name, description, URL, transport type, and auth type.
- Public App Hub submission status, if relevant.
- Admin approval request for org/user-level use.
- Delete/edit options.

## Evidence

- Developer Portal URL and app details page.
- Agentic App name.
- App ID.
- Transport type.
- Auth type.
- App URL domain.
- Public/private status.
- Approval/provisioning status.
