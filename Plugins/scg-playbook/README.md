# SCG Playbook Codex Plugin

Create visual-first, reusable Webex CX AI Agent and Contact Center playbooks from working demos, exports, screenshots, MCP setup notes, and field documentation.

## Installation

> [!IMPORTANT]
> Set the Codex task permission to `Ask for Approval`, then copy and paste:

```text
Install the SCG Playbook plugin from the AI SCG marketplace in
ciscoAISCG/webex-cx-ai using branch main. Before beginning, confirm this task
can request protected-write approval to update the local Codex configuration.
If protected-write approval is unavailable, stop and tell me to set the task
permission to Ask for Approval. Do not use sudo, change filesystem permissions,
or attempt another workaround. Read the plugin README first. Do not ask me to
run terminal commands; perform the plugin-management steps yourself. If the
ai-scg marketplace is not configured, add it. Install only scg-playbook,
preserve unrelated configuration, verify the installed source and version, and
tell me when a new task is needed to load the plugin.
```

## Updates

Use the canonical [AI SCG marketplace update instructions](../../README.md#update-my-plugins).

## Included skill

- `scg-playbook`: packages Webex CX AI use cases as adoption-first playbooks with Try It Fast steps, visual guidance, rounded Mermaid diagrams, Skills links, customer-safe cleanup, and validation.

## Supporting files

- `scripts/inspect_playbook.py`: inspects AI Agent Studio and Flow Designer JSON exports.
- `skills/scg-playbook/references/`: style, visual, cleanup, packaging, and validation guidance.
