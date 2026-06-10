# Table of Contents

- [Prompt Engineering for AI Agents](#prompt-engineering-for-ai-agents)
  - [Good Practices for Natural-Language Prompts](#good-practices-for-natural-language-prompts)
    - [Precise Instructions Change Behavior](#precise-instructions-change-behavior)
    - [Prefer Causal Logic Over Pure Sequence](#prefer-causal-logic-over-pure-sequence)
	- [Use Natural-Language Instructions, Not Code-Like Instructions](#use-natural-language-instructions-not-code-like-instructions)
  - [Important Limitation](#important-limitation)
- [When Prompts Are Not Enough](#when-prompts-are-not-enough)
  - [Problem Statement](#problem-statement)
  - [Why This Happens](#why-this-happens)
  - [Recommended Action](#recommended-action)
  - [Best Practices](#best-practices)
    - [Hybrid Control Model](#1-hybrid-control-model)



# Prompt Engineering for AI Agents

Prompt engineering is the practice of designing clear and effective instructions, written in human language, that guide how an AI Agent should behave.

This represents an important shift in system design: instead of relying only on traditional programming languages, behavior can now be influenced through natural language instructions.

Well-designed prompts can strongly improve tone, consistency, reasoning quality, and the overall user experience.

## Good Practices for Natural-Language Prompts

When prompts are written in human language, clarity becomes essential. Ambiguous or overly generic instructions often lead to inconsistent behavior.

Effective prompts usually include:

- **Clear objective**  
  Explain what the agent is expected to achieve.

- **Expected behavior**  
  Define tone, style, priorities, or boundaries.

- **Context**  
  Provide relevant background information.

- **Constraints**  
  Specify what the agent must always do, should avoid, or must never do.

- **Output expectations**  
  Describe the desired format or level of detail.

- **Prompt Engineering tips when writing instructions:**

	•	Keep It Simple: Use clear, concise language. Avoid technical jargon or overly complex sentences.  
	•	Use Markdown: Use headings and ordered/unordered list markdown for best results.  
	•	State Your AI Agent's Identity: Begin by clearly defining the agent's persona (e.g., “You are a helpful customer support agent…”).  
	•	Break It Down: Outline tasks step by step. For instance, “First, confirm your account number. Then, describe your issue.”  
	•	Plan for Errors: Include fallback phrases such as, “I'm sorry, could you please repeat that?” if the input isn't clear.  
	•	Preserve Context: Remind the agent to remember previous responses to ensure continuity in long conversations.  
	•	Reference Actions: Clearly instruct how to use external actions at different steps. Make sure the referenced actions are enabled in the Actions tab to avoid any unexpected behavior.  
	•	Add Guardrails: Instruct the AI Agent to respond only in the context of the goal.  
	•	Add Examples: To improve accuracy, add examples wherever needed.  

---
### Be Specific
Specify what the AI Agent must do, how it should do it, and any constraints that must be respected.
For instance, explicitly state whether a set of rules is part of an authentication procedure or an identity-verification process. Providing this context helps the AI Agent better understand the purpose of the workflow and apply the rules more consistently.

### Precise Instructions Change Behavior
Do not assume that an AI Agent behaves like a human agent. It may interpret instructions differently and produce unexpected outcomes.
#### Weak Prompt Example:

`Ask the user for first name. Then ask for last name, and finally the Employee ID.`

In this case, the AI Agent might ask all together with a single question, because it is not assumed that it has to wait for an answer before asking the next question.


#### Improved Prompt:

`Ask for first name, last name, and Employee ID one question at a time, waiting for each answer before asking the next one.`

---

### Prefer Causal Logic Over Pure Sequence

Prompts should express logical dependencies, not just sequence. “First do A, then do B” may be interpreted as guidance rather than a required condition. State why each step is needed and what must happen before the next one.

#### Weak Example:

`Collect the Employee ID, check the HR system, and inform the user of the PTO balance.`

In this example, the prompt describes a sequence of tasks but does not explicitly state the required dependencies between them. This flow might work well in most cases but fail in some, as the AI Agent may attempt to check the HR system before obtaining the Employee ID, or invent or assume the response without using the actual system result.

#### Stronger Example:

`Ask for the Employee ID, then use it to query the HR system to retrieve the PTO balance and provide the result to the user.`

In this example, causality is strengthened by explicitly stating that the Employee ID is used to retrieve the PTO balance.

### Use Natural-Language Instructions, Not Code-Like Instructions

You might think that an AI Agent, being fundamentally software, is more comfortable with instructions written in a code-like language. On the contrary, AI Agents process instructions as a whole, rather than executing them step by step, and may struggle with tasks that assume strict procedural logic.

#### Weak Prompt Example:

```
Step 1: validate the input using the knowledge base  
Step 2: if valid, continue to step 3. If it is not valid, go to step 5  
Step 3: Ask what issue the user is experiencing  
...
```
Here, the prompt assumes a program-like logic, including `if-then-else` and `goto` steps. But AI Agents do not maintain procedural state and do not execute control flow.

#### Stronger Example:

```
## SITE VALIDATION  
Before answering, verify that the site is valid using the document “sites.txt”.  
If the site is not valid, do not proceed and ask the user for clarification.
If the user cannot provide a valid site after multiple attempts, politely end the conversation. 

## ISSUE RETRIEVAL  
Once the site is validated, ask the user to describe the issue they’re experiencing.  
```

This formulation avoids relying on explicit state tracking or procedural control flow. It aligns with how LLMs actually reason: through semantic constraints, not procedural execution. The use of sections such as “Site Validation” and “Issue Retrieval” shows that the logic is organized semantically rather than as explicit control flow, relying on causal relationships instead of *if-then-else* structures.
In the next section, we will examine why LLMs exhibit these limitations and how to address them in practice.

## Important Limitation

Natural-language prompts are excellent for guidance, tone, reasoning, and intent recognition.

However, when a workflow requires mandatory steps, strict validation, conditional branching, or repeatable execution, prompts alone may not provide enough control.


# When Prompts Are Not Enough

A common design mistake in AI agents is assuming that a prompt alone can reliably enforce a step-by-step business procedure.

This becomes a problem when the agent is expected to behave intelligently in conversation while also following a **strict troubleshooting path**, **validation sequence**, or **policy-driven decision flow**.

## Problem Statement

In many customer contact center scenarios, the agent must do more than answer questions naturally. It must also follow a sequence of required checks, ask specific questions when certain conditions are met, and avoid skipping important steps.

Examples include:

- troubleshooting flows
- procedural workflows
- technical diagnostics
- policy-based routing or escalation

In these examples, the logic is very similar to programming code. 

---
**Risk**  
Large language models can generate code, but **cannot execute it reliably**.

---

The challenge is that large language models do not execute business logic in the same way that software does. Even when instructions are written clearly in a prompt or a knowledge base, the model may:

- skip steps
- ask too many questions
- ask questions out of order
- interpret instructions loosely
- fail to branch consistently
- hallucinate values when exact matching is required

This is especially risky when the workflow depends on **deterministic behavior**.

## Why This Happens

Language models are strong at understanding intent and generating natural responses, but they are less reliable when asked to follow **multi-step procedural logic** purely from free-form text.

A prompt may describe rules such as:

- if the user has provided an Employee ID, ask what issue they are experiencing
- if the issue is printer-related, ask printer-specific questions
- if the resource is shared, ask whether other users are affected
- if the issue is software-related, ask which application is involved

You might find that writing the above rules with a programming-language style might work better than using human language.

---
**Key Point**  
Flows like the one above implicitly require a **runtime environment**, **state variables**, and **causal branching**.

---

But flows like the first one above implicitly require procedural state: for example, whether `employee_id_check` is true or false, whether a previous step has been completed, and which branch should be executed next. The problem is that an LLM does not natively operate as a deterministic workflow engine with guaranteed state tracking, conditional execution, and control flow. It generates the next response token by token.

However, across the millions of documents seen during training, the model statistically captures different patterns associated with natural language and programming language data.

Human language is not strictly tied to exact wording. Word order may vary, synonyms often preserve the core meaning, and the same concept can be expressed in many different ways. Typos or minor errors are often tolerated without changing the intended meaning. Human language relies heavily on semantics, while allowing broader syntactic variation.

Programming languages, on the other hand, depend heavily on exact syntax. Specific keywords are required, punctuation matters, and a missing comma or bracket may break the entire program. Programming languages require strict syntax and tightly constrained semantics.

---
**Practical Consequence** 

Code-like formats make LLMs focus on syntax and follow instructions **more reliably**.

---


For this reason, when procedures are encoded as structured JSON workflow variables, the LLM tends to follow them more precisely than equivalent free-form natural language instructions.

Externalizing workflow logic into a JSON structure helps address both limitations: structured formats strengthen syntactic focus, while state, branching, and execution rules are shifted out of the LLM into an explicit machine-readable layer.


## Recommended Action

Use prompts for conversation, tone, intent recognition, summarization, and general reasoning.

---
**Do Not Rely on Prompts Alone**  

Prompts alone are **not enough** for reliable execution of multi-step or conditional workflows.

---

Do not rely on prompts alone to guarantee consistent execution of multi-step procedures, troubleshooting paths, or conditional workflows.

When interactions require mandatory steps, branching logic, state tracking, or repeatable outcomes, place that control logic in an external structured layer, such as a JSON workflow or database-driven flow definition.

In this model, the AI Agent focuses on language understanding and user interaction, while the external workflow layer controls sequence, decisions, and next-step execution.

This separation typically improves:

- reliability
- consistency
- maintainability
- operational control

## Best Practices

A good rule of thumb is:

- use the model for interpretation
- use structured data for control

Two implementation models can be considered:

1. **Hybrid Control Model**  
   Workflow logic is split between prompt instructions and an external JSON/database layer.

2. **Fully Externalized Control Model**   
   Workflow logic is moved almost entirely into an external JSON/database layer, while the LLM focuses on language understanding, reasoning, and interaction. Although this model is outside the scope of this document, it is included here for architectural completeness.

### Hybrid Control Model

Imagine an AI Agent used to triage IT issues. After identifying which resource is affected, the agent must ask additional questions depending on the issue type.

Possible follow-up questions are:

- Site location
- Whether other users are experiencing the same issue
- Which application is involved

These questions do not apply equally to every category.

Knowing the location of a printer may be important, while it may be irrelevant for access issues on a web application.

---
**Benefit of Structured Variables**  
JSON increases syntactic focus and makes the LLM more attentive to exact fields, conditions, and transitions.

---

If we describe this behavior only in human language, the AI Agent may behave inconsistently. However, if we convert the logic into variables stored in a database and retrieved as JSON, the structured format increases the syntactic focus of the interaction, making the LLM more attentive to exact fields, conditions, and transitions than it would typically be with plain natural language instructions.

Below is an example of a JSON variable that can be stored in Webex Connect or in an external database:

```json
{
  "id": "obj1",
  "category": "Web Application",
  "ask_site": false,
  "check_application": true,
  "check_other_users": false
}

{
  "id": "obj2",
  "category": "Printer",
  "ask_site": true,
  "check_application": false,
  "check_other_users": true
}
```

After identifying the category, the agent retrieves the corresponding configuration.

The following are the instructions for the AI Agent:

```text
1. Identify the user issue and use the [category_list] action to map it to a single category.
2. Use the mapped category to call the [selected_category] action and retrieve its configuration.

Then evaluate the following conditions:

- If `check_application` is `true` and no application has been specified, ask which application is involved.
- If `ask_site` is `true` and no site is confirmed, ask for the site and validate it.
- If `check_other_users` is `true` and you do not yet know whether other users are affected, ask the user whether anyone else is experiencing the same issue.
```
In this model, logic is partly encoded in the prompt and partly externalized in the JSON/database layer.
Natural language instructions leave broad room for interpretation.
Structured formats such as JSON reduce that ambiguity by constraining the decision space.
Externalizing workflow logic into machine-readable structures does not make the LLM a true executor, but it significantly improves reliability, consistency, and controllability.
It is also possible to externalize the logic almost entirely, while the LLM still provides language understanding, reasoning, and interaction skills.

