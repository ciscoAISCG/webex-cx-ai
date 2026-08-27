---
name: webex-mcp-onboarding
description: Guide Webex MCP setup for Webex Autonomous AI Agents across the Webex Developer Portal, Control Hub Agentic Apps, and AI Agent Studio, including MCP readiness intake, Agentic App registration, org provisioning, tool authorization, Studio action binding, prompt/tool contracts, validation, troubleshooting, browser-assisted GUI workflows, official developer.webex.com documentation lookup, and MCP playbook packaging. Use when a user wants to add MCP tools to a Webex AI agent, onboard an MCP server as an Agentic App, provision MCP in Control Hub, verify MCP tool availability in Studio, create a repeatable MCP setup recipe, or turn an MCP setup into an internal/customer playbook.
---

# Webex MCP Onboarding

Use this skill to guide MCP setup for Webex AI agents from idea to validated tool use. Treat the skill as the live builder and the playbook as the packaged output.

## First Move

1. Restate the agent goal and what the MCP tool should let the agent do.
2. Identify the audience: `internal`, `customer/partner`, or `both`.
3. Identify the environment: sandbox, lab, customer test tenant, or production.
4. Classify the phase:
   - MCP fit and positioning
   - quick-start intake
   - readiness intake
   - Webex Developer Portal Agentic App registration
   - Control Hub provisioning, authentication, tool authorization, and access policy
   - AI Agent Studio binding
   - prompt/tool contract
   - validation and troubleshooting
   - browser-assisted setup
   - playbook packaging
5. If the user says "I want to add <MCP server> to my AI agent" or gives only a server name, use `references/quick-start-intake.md` and ask the smallest practical question set first.
6. If details are available as JSON, run `scripts/render_mcp_recipe.py <intake.json>` to produce a consistent build recipe.

## Core Model

Use a four-phase setup model unless the user provides a more specific tenant flow:

1. Register the MCP server as an Agentic App in the Webex Developer Portal.
2. Provision and govern the Agentic App in Control Hub.
3. Add the available MCP tool as an action in AI Agent Studio.
4. Validate direct tool behavior and full agent conversation behavior.

Developer Portal, Control Hub, and Studio are the primary platforms for MCP onboarding. MCP is only one slice of a full Webex AI agent build. Webex Connect or Flow Designer may be involved when the agent also needs fulfillment workflows, voice/DID routing, or contact-center orchestration.

Before pushing MCP as the answer, check whether MCP is a good fit. MCP usually requires a hosted MCP server and a security review for an externally hosted service. When the customer or team does not have a hosted MCP server, a server owner, or security approval path, Webex Connect may be the simpler action fulfillment path.

## Reference Selection

Use `references/mcp-readiness-intake.md` before setup, customer handoff, or playbook generation.

Use `references/quick-start-intake.md` when the user gives a minimal request and needs Codex to make the process easy by asking only the next useful questions.

Use `references/mcp-positioning-and-fit.md` when deciding whether MCP is the right approach, explaining why the flow has many moving parts, or comparing MCP with Webex Connect fulfillment.

Use `references/official-webex-docs.md` when details might have changed, when a user cites developer.webex.com, or when exact current docs are needed.

Use `references/developer-portal-agentic-app.md` for Webex Developer Portal Agentic App registration and MCP server onboarding.

Use `references/control-hub-mcp-setup.md` for Control Hub provisioning, authentication, authorization, tenant checks, and evidence capture.

Use `references/studio-tool-contract.md` for Studio binding, prompt/tool instructions, schemas, and agent behavior.

Use `references/validation-and-troubleshooting.md` for direct tool tests, Studio tests, conversation tests, and common failure modes.

Use `references/browser-assisted-workflow.md` when the user wants Codex to observe screenshots or help drive the GUI after login.

Use `references/mcp-playbook-package.md` when the output should become a reusable weekly playbook or customer-facing package.

## Output Modes

For a new MCP setup, output:

- Goal and target agent.
- Required Developer Portal, Control Hub, and Studio access.
- MCP server/tool inventory.
- Four-phase build order.
- Manual GUI steps and automation candidates.
- Security, auth, and data handling notes.
- Validation plan.
- Evidence to collect.
- Open questions.

For an existing setup, output:

- What appears configured.
- What is missing or ambiguous.
- Which tests prove the setup works.
- Which parts should be captured for a playbook.
- Risks before using the tool with real users.

For browser-assisted setup, output:

- The exact screen or platform the user should open.
- What Codex will inspect or click.
- Which actions require pause/confirmation.
- A change log and evidence checklist after each step.

Default to guided form-filling before browser automation: provide the link, the exact field values to enter, and a pause/verification point for each platform. Do not promise unattended Playwright automation until the relevant tenant UI has been observed and the user explicitly asks for browser-assisted action.

For a playbook, output:

- A reusable MCP onboarding package with audience, prerequisites, screenshots/evidence placeholders, setup sequence, validation, troubleshooting, and security notes.

## Guardrails

- Do not invent exact Control Hub click paths, labels, feature names, or MCP UI states that have not been captured. Mark them as UI-dependent and request screenshots or a browser session.
- Never ask for passwords, MFA codes, raw secrets, API keys, or bearer tokens in chat.
- Pause before entering secrets, changing production access, publishing an agent, enabling a tool for a production org, or exposing customer data.
- Keep internal-only details out of customer/partner playbooks unless the user explicitly approves.
- Separate facts from assumptions. Label tenant-specific findings clearly.
- Prefer least-privilege tool exposure and narrow agent/tool access.
- Validate direct MCP behavior before validating full agent conversation behavior.

## Script

Create a recipe from an intake JSON file:

```bash
python3 /path/to/webex-mcp-onboarding/scripts/render_mcp_recipe.py intake.json
```

Generate an example intake file:

```bash
python3 /path/to/webex-mcp-onboarding/scripts/render_mcp_recipe.py --example
```
