# MCP Readiness Intake

Use this reference before planning setup, driving the GUI, or packaging a playbook.

For a minimal user request, read `quick-start-intake.md` first. Use this file only when moving from a lightweight conversation into a fuller recipe, customer handoff, or playbook package.

## Minimum Inputs

| Field | Why it matters |
|---|---|
| Audience | Internal, customer/partner, or both changes wording and safety boundaries. |
| Tenant/org | Control Hub changes must happen in the correct org. |
| Environment | Sandbox and production have different approval gates. |
| Target agent | MCP tools must be validated against a specific Studio agent or agent design. |
| MCP server name | Human-readable name for setup, tests, and playbooks. |
| MCP server purpose | Explains why the agent should use the server. |
| App URL | Public HTTPS endpoint for the deployed MCP server. |
| Hosting owner | MCP requires someone to host, monitor, update, and support the server. |
| Security approval path | External MCP services should be reviewed before production use. |
| Webex Connect alternative | Many fulfillment use cases may be simpler in Webex Connect. |
| Transport type | Default to `Streamable HTTP`; use `HTTP SSE` only when required. |
| Authentication method | Determines secret handling and setup owner. |
| Developer Portal owner | Determines who can register, edit, and request approval for the Agentic App. |
| Tool inventory | Tool names, descriptions, and expected use cases. |
| Input/output schemas | Needed for prompt contracts and validation. |
| Data classification | Drives privacy, logging, and least-privilege guidance. |
| Access policy | Which users, groups, orgs, or agents can use the tools. |
| Test data | Needed for repeatable validation. |

Use `TBD` for fields the user does not know yet. Do not block the conversation unless the missing field is required for the immediate next platform step.

## Intake Questions

Ask only what is missing:

- What should the AI agent accomplish with MCP?
- Which MCP server will provide the tool?
- Is the MCP server already hosted, and who owns it?
- Has security reviewed or approved the external service/data path?
- Would this be easier as Webex Connect fulfillment?
- Has the MCP server already been registered as an Agentic App on developer.webex.com?
- Is this a lab, sandbox, customer test, or production tenant?
- Which Studio agent should use the tool?
- Which authentication type should be used: OAuth2 client credentials, API key, or custom header?
- What tools should be exposed, and which should stay hidden?
- What auth method does the MCP server require?
- What sensitive data may pass through tool calls?
- What result proves the setup works?

## Red Flags

- Production tenant with unknown access policy.
- MCP server is not reachable over HTTPS.
- No owner for hosting, uptime, monitoring, updates, or incident response.
- Customer will not approve an externally hosted tool service.
- Webex Connect can handle the fulfillment with fewer moving parts.
- Developer Portal registration owner is unknown.
- Tool exposes broad write/delete/admin capability.
- Tool requires secrets but no owner or rotation plan is known.
- Tool schemas are unknown or loosely described.
- No direct MCP test exists before Studio testing.
- Customer/partner artifact includes Cisco-internal-only process details.
