# Official Webex Docs Lookup

Use official Webex Developer documentation as the source of truth when MCP setup details are missing, current UI labels matter, auth options may have changed, or the user provides a developer.webex.com link.

## Primary Docs

- Webex Developer docs home: `https://developer.webex.com/docs`
- Onboard an Agentic App: `https://developer.webex.com/mcp/docs/onboard-your-agentic-app`
- Provision Agentic Apps in Control Hub: `https://developer.webex.com/create/docs/provisioning-on-control-hub`
- Configure MCP actions in AI Agent Studio: `https://developer.webex.com/mcp/docs/mcp-ai-agent-studio`

The user may provide older or alternate paths such as `https://developer.webex.com/create/docs/onboard-your-mcp-server`. Resolve to the current canonical documentation before treating steps as stable.

## Lookup Rules

- Prefer official Webex Developer pages over memory for exact steps, current auth types, limitations, and UI labels.
- Cite the docs URL in user-facing answers when using current documentation.
- Do not paste long doc excerpts into the skill or final answer. Summarize the action and keep the docs URL as the durable reference.
- If docs and observed UI differ, treat the observed tenant UI as tenant-specific evidence and note the discrepancy.
- If docs list auth modes that the team does not currently support, follow the team-supported workflow and note the docs/team delta.
- Re-check docs before production-facing playbooks or customer/partner distribution.

## Current Lifecycle From Docs

At a high level, the current documented flow is:

1. Register the MCP server as an Agentic App in the Webex Developer Portal.
2. Provision/govern the Agentic App in Control Hub under Apps and Agentic Apps.
3. Add available MCP tools as actions in AI Agent Studio.
4. Verify tool status and run direct plus conversation-level tests.
