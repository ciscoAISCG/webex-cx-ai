---
name: webex-ai-agent-creator
description: Design Webex AI Agent Studio assistants from a user-provided business use case. Use when Codex should ask for an AI agent use case, confirm the agent goal and likely actions, apply the Cisco AI prompt-design best-practice guide, generate production-ready AI agent instructions, recommend actions with parameters, and provide step-by-step Webex AI Agent Studio setup guidance.
---

# Webex AI Agent Creator

## Overview

Use this skill to turn a user's Webex AI Agent Studio idea into an implementation-ready plan: confirmed use case, action design, AI agent instructions, and setup steps.

Read these references before producing the final artifact:

- `references/prompt-design-principles.md` for Cisco AI prompt-writing rules.
- `references/webex-ai-agent-studio-setup.md` for Webex AI Agent Studio access and setup guidance.
- `references/ai-agent-studio-json-import.md` when the user wants an import-ready AI Agent Studio JSON file.

## Workflow

1. Gather the use case.
   - Ask the user what AI agent use case they want to implement.
   - Ask only for missing essentials: target users, channel, business outcome, source systems, required authentication, escalation path, and success criteria.
   - Keep questions concise and grouped.

2. Confirm the use case and likely actions.
   - Restate the use case in plain language.
   - Identify the likely actions the agent needs, such as checking ticket status, booking appointments, fetching account details, creating cases, updating records, transferring to an agent, or sending confirmations.
   - Ask the user to confirm or correct the use case and action list before finalizing instructions.

3. Design action semantics.
   For each recommended action, capture:
   - Action name.
   - Purpose.
   - Trigger conditions.
   - Required parameters.
   - Optional parameters.
   - Source system or fulfillment flow.
   - Expected success response.
   - Failure and fallback behavior.
   - Whether human escalation is required.

4. Generate AI agent instructions.
   - Apply https://github.com/ciscoAISCG/webex-cx-ai/blob/main/Cookbooks/docs/prompt-design.md
   - Use natural-language instructions with clear sections, not brittle code-like control flow.
   - State the agent identity, goal, scope, constraints, conversational behavior, required action usage, escalation behavior, and output style.
   - Include a short goal summary that explains the business purpose and user benefit in one or two sentences.
   - Include a concise, channel-appropriate greeting the agent can use to welcome users and set expectations before collecting details.
   - Express causal dependencies explicitly: the agent must collect required inputs before calling an action, and must not invent action results.
   - For deterministic branching, recommend externalizing logic into action responses, JSON configuration, Webex Connect flows, or backend systems.
   - Instructions need to be under 5000 characters.
   - There can only be a maximum of 10 actions, if this is exceeded they will need to be logically split out into multiple agents.

## Goal Summary Guidance

When the user asks for the agent goal, provide a short summary that states what the agent does, who it helps, and why it matters. For the patient-friendly clinic booking use case, use or adapt:

```text
The goal of this AI agent is to help clinic patients book appointments in a calm, low-pressure way while reducing uncertainty before the visit. It connects to Epic to manage booking tasks, captures anxiety-friendly preferences, and follows up through the patient's chosen digital channel with practical preparation information.
```

## Greeting Guidance

When the user asks for a greeting, provide a short, natural opening that identifies the agent, explains what it can help with, and offers low-pressure choices. For the patient-friendly clinic booking use case, use or adapt:

```text
Hello, you have reached the clinic booking assistant. I can help you book an appointment, look for a time that feels easier for you, and send clear instructions before your visit. Would you prefer the soonest available appointment, a quieter time of day, or a specific clinician?
```

5. Provide Webex AI Agent Studio setup guidance.
   - Apply https://help.webexconnect.io/docs/getting-started-with-webex-ai-agent-studio
   - Include step-by-step setup from access through testing.
   - Mention both Control Hub and Webex Connect access paths when relevant.
   - Include where to configure actions and fulfillment flows.
   - Include the proposed actions and parameters in a concise table.

6. Generate an import-ready JSON file when requested.
   - Use the structure in `references/ai-agent-studio-json-import.md`.
   - Include `bot_type`, `configuration`, and `tools` top-level keys.
   - Put the agent goal and generated agent instructions in `configuration.llm_agent_description`.
   - Format `configuration.llm_agent_description` as: agent goal text, then a blank line, then the literal separator `### INSTRUCTIONS:`, then the detailed AI agent instructions.
   - Put the suggested greeting in `configuration.welcome_message`.
   - Include voice settings when the channel is voice.
   - Include an `Agent handover` system tool by default.
   - Convert each recommended action into a tool entry with `input_entities.parameters.properties` and `required` fields.
   - Always use placeholders for Webex Connect service name, Webex Connect service ID, flow IDs, webhook URLs, preferred voice, and whether backend actions are real, mocked, or routed through Webex Connect flows. The user must create flows and tenant-specific resources manually and replace these placeholders after generation.
   - Use a valid IANA timezone value in `configuration.timezone`, such as `Europe/London` or `America/Los_Angeles`. Do not use a placeholder for timezone because AI Agent Studio validates this field during import.
   - Always set `configuration.kb_ids` to an empty array. Do not generate placeholder knowledge base IDs because incorrect KB IDs can cause import or UI errors.
   - Keep action names exactly aligned between the instructions and JSON tools.
   - If creating a local artifact, name it with a safe slug such as `<agent-name>-ai-agent-studio-import.json`.
   - Always include the full file location of any generated or updated JSON artifact in the final response.

## Final Output

Deliver these sections:

1. Use Case Confirmation
2. Assumptions and Open Questions
3. Recommended Actions and Parameters
4. Goal Summary
5. Suggested Greeting
6. AI Agent Instructions
7. Webex AI Agent Studio Setup Guide
8. Import-Ready JSON File, when requested

Keep the final result practical and implementation-oriented. If key details are unknown, make reasonable placeholders explicit instead of blocking, unless the missing detail changes the action design materially. When a JSON file is generated or updated, always provide its full file location.
