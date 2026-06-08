# MCP Positioning And Fit

Use this reference when deciding whether MCP is the right path, explaining the moving parts, or helping a user compare MCP with Webex Connect fulfillment.

## Short Positioning

MCP can be useful when an AI agent needs reusable tool access through a hosted MCP server, but it is not the simplest fulfillment path today. It adds a separate server lifecycle, authentication setup, Control Hub governance, Studio action binding, prompt/tool instructions, and validation. Treat it as one specialized slice of the broader AI agent build, not the whole agent build.

## Why The Flow Feels Cumbersome

The user must coordinate:

- Hosted MCP server ownership.
- Developer Portal Agentic App registration.
- Control Hub approval, access, authentication, and tool enablement.
- Studio action selection and agent instructions.
- Security review for an external service.
- Testing across direct tool behavior and full conversation behavior.

This is difficult to explain manually because success depends on multiple platforms and each platform proves a different thing.

## Fit Questions

Ask these before recommending MCP for a customer or production build:

- Is there already a reachable hosted MCP server?
- Who owns hosting, uptime, monitoring, and updates for that MCP server?
- What data leaves Webex/Control Hub and reaches the external MCP service?
- Has the customer security team approved the external service pattern?
- Is the tool reusable across agents or channels?
- Does the agent need dynamic tool discovery or a reusable tool catalog?
- Would Webex Connect handle the fulfillment with fewer moving parts?
- Is this a lab/prototype, internal demo, customer pilot, or production deployment?

## Recommend MCP When

- A hosted MCP server already exists or the customer is willing to host one.
- The customer accepts the security and data-flow model.
- Tool capabilities are reusable across agents, teams, or use cases.
- The tools benefit from MCP-style discovery, schemas, or a shared server contract.
- The team can validate auth, tool discovery, Studio binding, and conversation behavior end to end.

## Prefer Webex Connect Or Another Fulfillment Path When

- No one owns MCP server hosting.
- The customer is not ready to approve an external service path.
- The action is a straightforward workflow/API fulfillment that Webex Connect can own.
- The use case needs orchestration, callbacks, notifications, or contact-center workflow steps already modeled in Webex Connect.
- The team needs the quickest path to a working playbook or customer demo.

## Security Framing

Do not dismiss security concerns. MCP servers may live outside Control Hub, so security review should cover hosting owner, authentication, data classification, logging, secret storage, rotation, network access, and incident ownership.

For customer/partner wording, avoid saying MCP is unsafe. Say:

> MCP introduces an externally hosted tool service that should be reviewed like any other customer integration. We need to confirm hosting ownership, authentication, data handling, and approval before production use.

## Skill Output Guidance

When a user asks to add MCP, include a brief fit note:

- `MCP fit: good candidate` when hosting, security, and tool ownership are clear.
- `MCP fit: prototype only` when the flow can be tested but hosting/security are not production-ready.
- `MCP fit: consider Webex Connect` when the user needs action fulfillment but does not have a hosted MCP server or security approval path.

Then continue with the smallest next step rather than overwhelming the user with every phase at once.
