# Prompt Design Principles

Source: https://github.com/ciscoAISCG/webex-cx-ai/blob/main/Cookbooks/docs/prompt-design.md

Use these principles when generating Webex AI Agent Studio instructions.

## Core Prompt Ingredients

- Define the AI agent identity and persona.
- State the objective clearly.
- Provide relevant business context.
- Specify expected behavior, tone, boundaries, and priorities.
- Define constraints: what the agent must always do, should avoid, and must never do.
- Define output expectations and level of detail.
- Use Markdown headings and lists for readability.
- Add examples only when they reduce ambiguity.
- Plan fallback behavior for unclear input.
- Preserve conversation context where needed.
- Reference external actions explicitly and ensure those actions are enabled in the Actions tab.
- Add guardrails so the agent responds only within the goal.

## Specificity and Causality

Be specific about what the agent must do, how it should do it, and why each dependency matters.

Prefer causal logic over pure sequence. Instead of only saying "collect X, call Y, answer Z", say that X is required to call Y, and the result from Y is required before answering Z.

Example pattern:

```text
Ask for the customer identifier. Use that identifier to call [check_ticket_status]. Only provide the ticket status after the action returns a result. If the action fails or returns no match, ask the user to verify the identifier or offer escalation.
```

## Natural Language First

Use natural-language instructions rather than code-like pseudo-control-flow. Organize logic into semantic sections such as "Identity Verification", "Appointment Booking", and "Escalation".

Avoid prompts that depend on the model executing strict `if/else`, `goto`, or state-machine logic from free text.

## When Prompts Are Not Enough

Do not rely on prompts alone for mandatory steps, strict validation, conditional branching, or repeatable execution. When the workflow needs deterministic behavior, recommend moving control into:

- Webex Connect flows.
- Action fulfillment flows.
- Backend APIs.
- Database or JSON configuration.
- Other structured systems of record.

Use the model for interpretation, conversation, reasoning, and summarization. Use structured data or workflow systems for control, validation, and branching.

## Action Instructions

For every action, include:

- Exact action name.
- When to use it.
- Required inputs.
- Where those inputs come from.
- What result to expect.
- What the agent should do if the result is missing, ambiguous, or an error.
- A rule that the agent must not invent action results.
