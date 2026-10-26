# Validation And Troubleshooting

Use this reference to prove an MCP setup works and isolate failures.

## Test Ladder

1. Control Hub status check.
2. Direct MCP server/tool test if available.
3. Studio visibility test.
4. Studio direct tool-use test.
5. Agent conversation happy path.
6. Agent conversation failure path.
7. Permission/least-privilege negative test.
8. Playbook reproducibility check.

## Test Matrix

| Scenario | Expected evidence |
|---|---|
| Tools visible in Control Hub | Tools tab lists the expected MCP tools after authentication is saved. |
| Tool visible in Studio | `Add actions` modal shows expected row with source `From <provider> • MCP`. |
| Tool added to agent | Agent Actions table shows the MCP action with type `MCP`. |
| Agent instructions updated | Agent instructions define when to call each MCP action and how to handle success/failure. |
| Orchestration defined | Instructions specify tool order, required inputs, output handoff, confirmation gates, and handoff behavior. |
| Tool hidden when not authorized | Expected permission denial or absence. |
| Happy path | Tool returns expected sample result. |
| Bad input | Agent asks for correction or returns safe fallback. |
| Tool failure | Agent gives bounded retry or escalation. |
| Sensitive data | No secrets or restricted fields appear in user-visible output. |
| Production gate | Human approval captured before enabling production use. |

## Common Failure Modes

| Symptom | Likely cause | Next check |
|---|---|---|
| No tools appear in Control Hub Tools tab | Authentication failed, server unreachable, wrong auth values, or MCP server tool discovery failed | Re-check Authentication tab, server URL, server logs, and Developer Portal auth type. |
| Tool appears in Control Hub but not Studio Add actions modal | Control Hub authorization, unsaved tool enablement, tenant mismatch, role issue, or Studio sync delay | Confirm org, saved Control Hub Tools state, target agent, and search by provider/action name. |
| Tool appears but call fails | Server URL, auth, schema, or network issue | Test server directly and inspect auth setup. |
| Agent never calls tool | Prompt lacks clear tool-use condition | Update Studio tool contract. |
| Agent calls tools in wrong order | Orchestration instructions are missing or ambiguous | Add explicit sequence, required inputs, and output handoff rules. |
| Agent calls tool too often | Prompt lacks boundaries | Add when-not-to-call rules. |
| Raw backend error shown | Prompt or tool response handling is too literal | Add user-safe failure language. |
| Works in lab but not customer tenant | Feature flag, role, or org policy mismatch | Compare tenant capabilities and access. |

## Validation Output

Summarize:

- What was tested.
- What passed.
- What failed.
- Evidence collected.
- Remaining risks.
- Playbook updates needed.
