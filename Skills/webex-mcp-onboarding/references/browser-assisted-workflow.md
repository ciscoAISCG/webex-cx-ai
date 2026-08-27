# Browser-Assisted Workflow

Use this reference when the user wants Codex to help with the Developer Portal, Control Hub, or Studio GUI.

## Current Automation Stance

Default to guided form-filling:

- Codex tells the user which page to open and which values to enter.
- Codex can prepare a field-by-field checklist and validate screenshots or visible results.
- Codex should not promise unattended Playwright automation yet.

Move to browser-assisted clicking only after the user explicitly asks, logs in, confirms the tenant, and the relevant UI has been observed. Treat Playwright-style automation as a later hardening step after repeatable selectors and pause gates are known.

## Safety Model

- User logs in and handles MFA.
- Codex observes page state before acting.
- Codex pauses before secrets, production changes, save/publish actions, enablement, deletion, or live data.
- User confirms the active tenant/org before edits.
- Codex records every material change.

## Browser Session Flow

1. If onboarding a new MCP server, ask the user to open `https://developer.webex.com/my-apps/new/agentic-server`.
2. Observe the Developer Portal app creation flow and register or inspect the Agentic App.
3. Ask the user to open `https://admin.webex.com/apps/agentic-servers` and log in if prompted.
4. Confirm tenant/org and environment.
5. Navigate or ask user to navigate to Apps -> Agentic Apps when available.
6. Confirm the newly onboarded server appears in the table, usually as an external MCP server with Access `Blocked` and a red dot before configuration.
7. Click or ask the user to click the server row/name to open configuration.
8. On the General tab, select `Allowed for all users` and turn on `Authorize automatic server data updates` only after confirming the org and server name.
9. Pause before Save because this changes org access; after approval, save and verify status changes to `Allowed`.
10. Click the Authentication tab and confirm the displayed auth type matches the Developer Portal choice.
11. For custom headers, guide the user through Key and Value fields; the user enters secret values directly in the UI.
12. Pause before Save because this stores authentication material; after approval, save and confirm no visible error.
13. Click the Tools tab and confirm the MCP server tools are visible; if no tools appear, stop and troubleshoot auth/server setup.
14. Toggle `Allow tool` only for the tools needed by the agent use case.
15. Use `Review` when tool details or risk are unclear.
16. Leave `Allow signature change` off unless the user/team explicitly wants automatic schema update behavior.
17. Pause before Save because enabled tools become available for Studio action binding; after approval, save.
18. Record enabled tool names; these are the tools to add in AI Agent Studio.
19. Observe visible UI labels, tables, server names, and status.
20. Capture unknown click paths as facts only after observation.
21. Confirm enabled tools, schemas, auth, and org allow/block state.
22. Cross-launch or open `https://studio.aiagent-us1.cisco.com/static/core/viewbots`.
23. Search for or select the existing target autonomous agent from the AI Agents card grid.
24. In the existing agent, open `Configuration` -> `Actions`.
25. Click `+ Add actions` and choose `Select available` when prompted.
26. In the `Add actions` modal, search by action name, description, provider, or MCP server name.
27. Confirm rows appear with source `From <provider> • MCP`; if no expected MCP actions appear, stop and troubleshoot Control Hub enablement, org mismatch, or Studio visibility.
28. Select only the intended MCP actions that were enabled in Control Hub.
29. Pause before clicking `Add` because this changes the target agent configuration; after approval, add the actions.
30. Confirm the added actions appear in the agent's Actions table with type `MCP`.
31. Return to the agent configuration area for profile/instructions. The exact editor label is UI-dependent until observed.
32. Add or update instructions for when to call each MCP action, required inputs, tool order when orchestrating, confirmation gates, retry limits, and safe failure language.
33. Pause before saving instructions because this changes agent behavior; after approval, save.
34. Run validation tests and capture evidence.

## Pause Gates

Pause for user approval before:

- Entering or revealing secrets.
- Adding the Agentic App in the Developer Portal.
- Saving MCP server config.
- Enabling tools for a production org.
- Changing access policy.
- Switching Access from blocked to allowed for all users.
- Saving authentication fields or custom header values.
- Enabling write/action tools.
- Enabling automatic signature changes.
- Adding MCP actions to a Studio agent.
- Saving Studio agent instructions or orchestration guidance.
- Publishing or deploying an agent.
- Running actions against real customer data.

## Change Log Template

```markdown
## GUI Change Log

| Time | Platform | Change | Evidence | User approval needed? |
|---|---|---|---|---|
```
