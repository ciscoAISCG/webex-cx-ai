# Webex AI Validator

Reviews Webex AI Agent instruction sets against the user's selected engine,
recommends improvements, identifies likely hallucination and other concern
areas, and proposes use-case-specific tests with expected results. Webex AI
Pro 1 is reviewed for ChatGPT 4.1; Webex AI Pro 2 is reviewed for ChatGPT 5.4.
The review also captures the channel (Voice or Digital) and reports where
confirmed built-in engine guardrails may override or affect the user's
instructions.

## Obfuscated guardrail data

The supplied built-in guardrails are included in
`skills/webex-ai-validator/references/engine-guardrails.obfuscated.txt` as
Base64-encoded UTF-8. The companion
`skills/webex-ai-validator/scripts/decode_guardrails.py` helper decodes the
selected engine's data for comparison. The Validator summarizes applicable
constraints without reproducing the raw prompt text. Base64 is reversible
obfuscation, not encryption: anyone with the plugin can decode the guardrails.
Do not use this packaging approach for data that must remain secret from plugin
recipients. The Pro 1 guardrails are complete as supplied. The shorter Pro 2
guardrails are also complete as supplied; the Validator must not extrapolate
Pro 1-only rules to Pro 2. The review is advisory: it does not execute tests or
certify runtime behavior.

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
