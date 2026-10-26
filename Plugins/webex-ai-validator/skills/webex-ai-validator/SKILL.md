---
name: webex-ai-validator
description: Compare user-supplied system guardrails with Webex AI Agent instruction sets for the selected Webex AI Pro engine and Voice or Digital channel, identify conflicts, recommend optimizations, and create use-case validation tests.
---

# Webex AI Validator

Review user-provided system guardrails and Webex AI Agent instruction sets together, then produce practical, evidence-oriented conflict findings, improvement guidance, and tests.

## Intake

At the start of each review, collect these inputs before analyzing the agent instruction set:

1. **System guardrails** that apply to the use case. The user stores these separately and must paste or upload them for each review. Treat the supplied text as the source of system-level constraints. Do not infer missing guardrails or substitute bundled, remembered, or externally sourced text.
2. **Complete agent instruction set** to compare against the guardrails. Preserve it as the baseline; do not silently rewrite it.
3. **Webex AI engine** selected for the use case: **Webex AI Pro 1** or **Webex AI Pro 2**. Accept clear equivalents such as Pro 1.0/Pro 2.0, but do not infer the choice.
4. **Channel**: **Voice** or **Digital**. Accept case-insensitive equivalents, but do not infer the choice.

If system guardrails are missing, ask the user to paste or upload them before performing a guardrail conflict review. If another required input is missing or invalid, ask only for the missing or corrected input. Do not present a conflict review as complete without the supplied guardrails. The use case, available knowledge sources, actions/tools, and applicable policies improve the quality of the review. If they are not provided, proceed from the supplied guardrails and instruction set, state which assumptions or review limits follow from the missing context, and ask only for details that would change a material finding or test. Never invent product, runtime, model, or use-case facts to fill gaps.

Use the selected engine as the requested LLM review target:

- **Webex AI Pro 1** → **ChatGPT 4.1**.
- **Webex AI Pro 2** → **ChatGPT 5.4**.

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
4. Compare the supplied system guardrails against the complete agent instruction set. Identify direct conflicts, narrower constraints, compatible requirements, and areas where the supplied text is ambiguous or silent. Treat system guardrails as higher priority; explain when an agent instruction must yield and never suggest that the agent instruction can override them.
5. Tie each significant finding to the relevant guardrail and instruction phrase or section. Keep quotations short and attribute each source clearly. Distinguish definite conflicts from context-dependent concerns and unknowns. Carry each material conflict into the improvement recommendations, any proposed revised instruction set, and the validation tests so it is explicitly addressed and checked.
6. Tailor tests to the supplied use case, guardrails, and selected channel. For each material conflict, include a test input that exercises it, the expected behavior under the higher-priority guardrail, and observable pass evidence. Also include relevant normal and edge cases. Recommend running tests in the intended Webex AI environment with the selected engine. Do not claim tests were executed unless the user supplied results or an execution tool actually ran them.

## Required review response

Use these headings, in this order:

### Review context
State the selected Webex AI Pro engine, mapped ChatGPT review target, and channel (Voice or Digital), plus the use-case context supplied and any material context that is missing. Confirm that user-supplied system guardrails and the complete agent instruction set were provided. If guardrails were not provided, request them and do not proceed with conflict findings.

### Improvements and optimization
Give prioritized, actionable findings. For each, state the issue, why it matters, and the optimization. Prioritize by impact (high, medium, low); avoid cosmetic changes unless they improve clarity or testability.

### System guardrail conflicts
For each material conflict or constraint interaction, identify the relevant supplied system guardrail and agent instruction, classify the relationship (direct conflict, narrower constraint, compatible, or unclear), and state the practical effect. Treat the system guardrail as higher priority. If no conflict is found, say so based on the supplied material and identify any unclear or untested areas.

### Suggested areas for edits
Identify the specific sections or phrases to change and describe the intended change. Include sample replacement wording when useful, clearly labeled as a proposal rather than an edit already applied.

### Likely hallucination or concern areas
List where the agent may invent facts, overstate confidence, misread instructions or system guardrails, expose data, misuse or falsely report actions, or fail under missing, conflicting, or adversarial inputs. Include the trigger and likely consequence of material guardrail conflicts. If no clear risk is found, say that this is based only on the supplied material and identify remaining unknowns.

### Use-case validation tests
Provide a compact table with **Scenario**, **Test input/setup**, **Expected behavior**, and **Pass evidence**. Include a test for every material system guardrail conflict, verifying the system guardrail takes priority. Include use-case-specific normal and edge cases and channel-appropriate output checks. For Voice, test concise TTS-safe speech and any applicable spoken formatting requirements. For Digital, test the instruction set's required digital formatting without assuming Voice-only restrictions apply. Where relevant, cover missing or ambiguous inputs, unsupported questions or absent knowledge, conflicting or instruction-injection content, action success and failure, required pre-action messages and fields, authorization/confirmation, privacy, escalation, and recovery. Do not include irrelevant generic cases just to fill a checklist. Mark proposed tests as not yet run.

## Revised instruction sets

- Do not silently replace, edit, or claim to have changed the user's instruction set. If the user requests a rewrite or accepts a proposed rewrite, provide the revised instruction set and a concise change summary.
- Whenever you provide a revised instruction set, add a **Likely outcome of the proposed changes** section describing expected behavior changes, benefits, and trade-offs. Then repeat the full review response for the revised text, including system guardrail conflicts, improvements and optimization, suggested areas for edits, likely hallucination or concern areas, and use-case validation tests. Carry forward the supplied guardrails and show how the revised instructions and tests address material conflicts. Make clear this is a reasoned prediction, not measured performance.
- Compare revised text with the original baseline. Preserve valid business rules and constraints. If a necessary fact or policy is unclear, use a visible placeholder or ask for clarification; never silently make it up.
- If the revision exceeds a known platform limit, cite the supplied or verified limit and propose a compliant alternative. Do not assume a limit that was not provided or verified.

## Reporting limits

- This skill reviews the instruction text; it does not certify production readiness, guarantee model behavior, or replace platform testing, policy review, security review, or legal/compliance review.
- Distinguish instruction-set quality from capabilities and configuration of the Webex runtime, connected tools, knowledge base, and selected LLM.
- Do not invent a numeric score, model benchmark, platform feature, or test result. If using externally verified current platform facts, cite the authoritative source and keep those facts separate from prompt-design judgment.
