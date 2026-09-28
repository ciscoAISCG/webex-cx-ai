# Webex AI Agent Knowledge Optimizer Codex Plugin

Create and optimize use-case-aware knowledge artifacts for Webex AI Agent Studio RAG from user-provided files, attachments, or public webpages.

## Installation

> [!IMPORTANT]
> Set the Codex task permission to `Ask for Approval`, then copy and paste:

```text
Install the Webex AI Agent Knowledge Optimizer plugin from the AI SCG
marketplace in ciscoAISCG/webex-cx-ai using branch main. Before beginning,
confirm this task can request protected-write approval to update the local
Codex configuration. If protected-write approval is unavailable, stop and tell
me to set the task permission to Ask for Approval. Do not use sudo, change
filesystem permissions, or attempt another workaround. Read the plugin README
first. Do not ask me to run terminal commands; perform the plugin-management
steps yourself. If the ai-scg marketplace is not configured, add it. Install
only webex-ai-agent-knowledgeoptimizer, preserve unrelated configuration,
verify the installed source and version, and tell me when a new task is needed
to load the plugin.
```

## Updates

Use the canonical [AI SCG marketplace update instructions](../../README.md#update-my-plugins).

## Included skill

- `webex-ai-agent-knowledgeoptimizer`: restructures, cleans, splits, rewrites, and validates source content for Webex AI Agent Studio knowledge bases while preserving meaning and grounding.
