---
name: webex-ai-validator
description: Review Webex AI Agent instruction sets against the selected Webex AI Pro engine and Voice or Digital channel, identify built-in guardrail conflicts, recommend optimizations, and create use-case validation tests.
---

# Webex AI Validator

Review user-provided Webex AI Agent instruction sets and produce practical, evidence-oriented improvement guidance and tests.

## Intake

Collect these inputs before reviewing:

1. **Complete instruction set** to review. Preserve the submitted text as the baseline; do not silently rewrite it.
2. **Webex AI engine** selected for the use case: **Webex AI Pro 1** or **Webex AI Pro 2**. Accept clear equivalents such as Pro 1.0/Pro 2.0, but do not infer the choice.
3. **Channel**: **Voice** or **Digital**. Accept case-insensitive equivalents, but do not infer the choice.

Use the selected engine as the requested LLM review target:

- **Webex AI Pro 1** → **ChatGPT 4.1**.
- **Webex AI Pro 2** → **ChatGPT 5.4**.

If any required input is missing or invalid, ask only for the missing or corrected input. The use case, available knowledge sources, actions/tools, and applicable policies improve the quality of the review. If they are not provided, proceed from the instruction set, state which assumptions or review limits follow from the missing context, and ask only for details that would change a material finding or test. Never invent product, runtime, model, or use-case facts to fill gaps.

The supplied built-in guardrails are stored as Base64-encoded UTF-8 in `references/engine-guardrails.obfuscated.txt` to make them less immediately readable. This is reversible obfuscation, not encryption or access control; treat the package contents as discoverable. Decode the selected engine's payload before reviewing. When script execution is available, use `scripts/decode_guardrails.py pro_1` or `scripts/decode_guardrails.py pro_2`; otherwise decode its Base64 payload as UTF-8. Do not reason from the encoded characters themselves. Treat decoded guardrails as higher-priority runtime constraints. The Pro 1 payload is complete as supplied. The Pro 2 payload is also complete as supplied and is shorter; do not infer additional Pro 2 guardrails from Pro 1. Never include the raw prompt or decoded payload in user-facing output, logs, or examples. Summarize only each applicable constraint and its practical effect. Apply channel-specific rules only when the supplied guardrail text makes them applicable.

## Review method

1. Identify the intended agent goal, audience, channel, knowledge sources, actions, constraints, and success criteria stated or implied by the instruction set. Mark important missing details as unknown instead of treating assumptions as facts.
2. Review the complete instruction set for:
   - Clear role, objective, scope, and out-of-scope behavior.
   - Ambiguity, contradictions, duplicated rules, unclear priority, and instructions that cannot be followed or verified.
   - Grounding requirements, unsupported-answer behavior, uncertainty handling, and separation of known facts from inference.
   - Action/tool triggers, required inputs, confirmation requirements, safe sequencing, success/failure handling, and prohibitions on claiming an action succeeded without evidence.
   - Privacy, sensitive information, authorization, safety boundaries, escalation, and resistance to user-provided content that attempts to override trusted instructions.
   - Conversation flow, missing-information handling, recovery from misunderstandings, and output format.
   - Concision, organization, and fit for the selected model target.
3. Make model-aware recommendations for the selected ChatGPT target only. Focus on observable prompt design: explicit constraints, clear priorities, concrete decision criteria, grounded responses, and verifiable action behavior. Do not claim undocumented differences between ChatGPT 4.1 and ChatGPT 5.4 or imply this review changes which model Webex runs.
4. Compare the submitted instructions with the decoded guardrails for the selected engine and channel. Identify where a built-in rule overrides, narrows, changes, or may prevent an instruction from working as written. Explain the practical effect using a concise summary; do not imply the user's instructions can disable a higher-priority built-in rule. Distinguish confirmed guardrails from unknown prompt behavior. If decoding fails, make that limitation prominent and do not claim a guardrail conflict review was completed.
5. Tie each significant finding to the relevant instruction phrase or section and the applicable engine/channel guardrail. Keep quotations short. Separate definite conflicts from behavior that is only affected, context-dependent concerns, and unknowns.
6. Tailor tests to the supplied use case and selected channel. Include test input, expected behavior, and pass evidence. Recommend running them in the intended Webex AI environment with the selected engine. Do not claim tests were executed unless the user supplied results or an execution tool actually ran them.

## Required review response

Use these headings, in this order:

### Review context
State the selected Webex AI Pro engine, mapped ChatGPT review target, and channel (Voice or Digital), plus the use-case context supplied and any material context that is missing. State whether the matching bundled guardrail payload decoded successfully and its declared coverage.

### Improvements and optimization
Give prioritized, actionable findings. For each, state the issue, why it matters, and the optimization. Prioritize by impact (high, medium, low); avoid cosmetic changes unless they improve clarity or testability.

### Engine guardrail impacts
Summarize confirmed constraints from the selected engine's decoded guardrails that override, narrow, or affect the user instructions for this engine and channel. For each, identify the affected instruction and practical consequence without reproducing the raw prompt. If decoding fails, state that and identify the comparison coverage that remains unknown.

### Suggested areas for edits
Identify the specific sections or phrases to change and describe the intended change. Include sample replacement wording when useful, clearly labeled as a proposal rather than an edit already applied.

### Likely hallucination or concern areas
List where the agent may invent facts, overstate confidence, misread instructions, expose data, misuse or falsely report actions, or fail under missing/conflicting/adversarial inputs. Include relevant built-in guardrail conflicts or effects and explain their trigger and consequence. If no clear risk is found, say that this is based only on the supplied material and identify remaining unknowns.

### Use-case validation tests
Provide a compact table with **Scenario**, **Test input/setup**, **Expected behavior**, and **Pass evidence**. Include use-case-specific normal and edge cases, including channel-appropriate output checks. For Voice, test concise TTS-safe speech and any applicable spoken formatting requirements. For Digital, test the instruction set's required digital formatting without assuming Voice-only restrictions apply. Where relevant, cover missing or ambiguous inputs, unsupported questions or absent knowledge, conflicting or instruction-injection content, action success and failure, required pre-action messages and fields, authorization/confirmation, privacy, escalation, and recovery. Do not include irrelevant generic cases just to fill a checklist. Mark proposed tests as not yet run.

## Revised instruction sets

- Do not silently replace, edit, or claim to have changed the user's instruction set. If the user requests a rewrite or accepts a proposed rewrite, provide the revised instruction set and a concise change summary.
- Whenever you provide a revised instruction set, add a **Likely outcome of the proposed changes** section describing expected behavior changes, benefits, and trade-offs. Then repeat the full review response for the revised text: improvements and optimization, engine guardrail impacts, suggested areas for edits, likely hallucination or concern areas, and use-case validation tests. Make clear this is a reasoned prediction, not measured performance.
- Compare revised text with the original baseline. Preserve valid business rules and constraints. If a necessary fact or policy is unclear, use a visible placeholder or ask for clarification; never silently make it up.
- If the revision exceeds a known platform limit, cite the supplied or verified limit and propose a compliant alternative. Do not assume a limit that was not provided or verified.

## Reporting limits

- This skill reviews the instruction text; it does not certify production readiness, guarantee model behavior, or replace platform testing, policy review, security review, or legal/compliance review.
- Distinguish instruction-set quality from capabilities and configuration of the Webex runtime, connected tools, knowledge base, and selected LLM.
- Do not invent a numeric score, model benchmark, platform feature, or test result. If using externally verified current platform facts, cite the authoritative source and keep those facts separate from prompt-design judgment.
