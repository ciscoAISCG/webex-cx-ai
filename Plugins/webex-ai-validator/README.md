# Webex AI Validator

Reviews Webex AI Agent instruction sets against the user's selected engine,
recommends improvements, identifies likely hallucination and other concern
areas, and proposes use-case-specific tests with expected results. Users
provide the applicable system guardrails separately for comparison with the
agent instruction set. Webex AI Pro 1 is reviewed for ChatGPT 4.1; Webex AI
Pro 2 is reviewed for ChatGPT 5.4. The review also captures the channel (Voice
or Digital). It is advisory: it does not execute tests or certify runtime
behavior.

## Installation

> [!IMPORTANT]
> Set the Codex task permission to `Ask for Approval`, then copy and paste:

```text
Install the Webex AI Validator plugin from the AI SCG marketplace in
ciscoAISCG/webex-cx-ai using branch main. Before beginning, confirm this task
can request approval to update the local Codex configuration. If protected-write
approval is unavailable, stop and tell me to set the task permission to Ask for
Approval. Do not use sudo, change filesystem permissions, or attempt another
workaround. Read the plugin README first and complete its required Codex setup.
Do not ask me to run terminal commands; perform the plugin-management and
configuration steps yourself. If the ai-scg marketplace is not configured, add
it. Install only webex-ai-validator, preserve unrelated configuration, verify the
installed source and version, and tell me whether a new task is needed to load
the plugin.
```

## Updates

Use the canonical [AI SCG marketplace update instructions](../README.md#update-my-plugins).
