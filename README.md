<p align="center">
  <img src="./ai-scg-logo/ai-scg-logo-final.svg" alt="AI SCG" width="360">
</p>

# Webex Customer Experience AI
### Reusable AI assets built from customer learnings

This repository is where reusable assets created from real customer engagements, field patterns and adoption learnings are published. This is maintained by the AI Solutions Consulting group but is contributed to by many different groups such as the Forward Deployed Engineering group, Cisco Sales and partners. This is an open-source community effort at the heart of it. 

The goal is to help Cisco teams and partners build faster, avoid starting from scratch, and apply proven AI patterns with more confidence.

[Start Here](#start-here) · [Templates](#templates) · [Cookbooks](#cookbooks) · [Skills](#skills-for-personal-assistants) · [Contributing](#contributing)

---

## Asset Library

The repository is organised around three asset types:

| Asset | What It Is | When To Use It |
| --- | --- | --- |
| Templates | Pre-built use cases and structures that help consumers build quickly. | Use when you want a working starting point for a customer scenario, demo, workflow, or solution pattern. |
| Cookbooks | Best practices, build guidance, examples, and how-to material. | Use when you need to understand how to build, adapt, validate, or improve an AI use case. |
| Skills for personal assistants | Instructions that turn your AI assistants into specialised experts who can build along with you. | Use when you want claude/codex/gemini to behave like to help in your config, best practices and other aspects of Webex CX AI portfolio. They will already know everything in the best practices, the cookbooks and so on. Let them build for you. |
| MCP Factory | Templates for MCP endpoints that can be used for demo, POC or production purposes. | Use when you want to have a reference implementation for an MCP integration with 3rd party systems. |

```text
templates/       Pre-built use cases and reusable starting points
cookbooks/       Best practices, how-to guides, and build patterns
skills shed/          Personal-assistant skills for specialist AI workflows
mcp factory/    MCP endpoints for various integrations
```

---

## Templates

Templates are pre-built use cases that help teams move quickly from idea to execution.

They are designed to give consumers a practical starting point: the structure, flow, components, prompts, or configuration pattern needed to build a specific AI use case without rebuilding the basics.

Use templates when you need to:

- Build a customer use case quickly.
- Recreate a proven demo or workflow.
- Standardise a repeatable solution pattern.
- Adapt a field-tested use case for a new customer or vertical.
- Give sales, SE, partner, or delivery teams a stronger starting point.

| Template | Description |
|---|---|
| [Directory_Routing](Directory_Routing/README.md) | Autonomous voice AI agent that classifies caller requests as person or department lookups, uses directory knowledge base resources, extracts the returned phone number, and transfers or falls back to the operator path. |
| [Data_Driven_Ordering](Data_Driven_Ordering/README.md) | Autonomous voice AI agent that uses a structured JSON menu to guide, validate, and place a configurable drink order, with Webex Connect fulfillment and digital-ordering fallback. |
| [User_Identification_Verification](User_Identification_Verification/README.md) | AI Agent pattern for collecting caller details, verifying identity with a backend service, and safely continuing or escalating based on the authentication result. |
| [Payment_AI_agent](Payment_AI_agent/README.md) | Autonomous voice AI agent ("Remy") that lets patients check a hospital balance and pay by credit card end-to-end, with safe escalation to a human billing specialist. |
| [ServiceNow KB + Incident AI Agent With MCP](ServiceNow_KB_Incident_AI_Agent_With_MCP/README.md) | Autonomous voice AI agent that uses MCP to search the ServiceNow Knowledge Base first, then create, search, update, or delete incidents when a ticket is needed. |
| [Visual_Appointment_Confirmation](Visual_Appointment_Confirmation/README.md) | Autonomous voice AI agent that collects appointment details, sends an SMS summary for visual review, and confirms the booking only after the caller approves or corrects the details. |

[Browse templates and playbooks](./playbooks)

---

## Cookbooks

Cookbooks explain how to build well.

They capture best practices, design guidance, implementation patterns, examples, lessons learned, and practical checks from customer work. A good cookbook should help someone understand not only what to build, but how to think about the build.

Use cookbooks when you need to:

- Understand the right build pattern for a use case.
- Apply best practices from previous customer engagements.
- Avoid common design or implementation mistakes.
- Learn how to scope, structure, test, or refine an AI workflow.
- Translate a customer requirement into a working AI pattern.

[Browse cookbooks](./cookbooks)

---

## Skills For Personal Assistants

Skills turn a personal AI assistant into a specialised expert for a repeatable task.

They package domain knowledge, instructions, guardrails, and working patterns so an assistant can help build with you, not just answer questions. The intent is to make personal assistants more useful in day-to-day AI work: faster to brief, more consistent in output, and better aligned to proven SCG patterns.

Use skills when you want an assistant to help with:

- Use case discovery
- Customer call preparation
- AI workflow design
- Prompt and instruction writing
- Demo planning
- Solution positioning
- Executive narrative drafting
- Build review and improvement

| Skill | Description |
| ---- | ---- |
| [Whatsapp](https://github.com/ciscoAISCG/webex-cx-ai/blob/main/Skills%20Shed/whatsapp) | Skill workspace for WhatsApp-related guidance and reusable assistant instructions. |
| [AI Calculator](https://github.com/ciscoAISCG/webex-cx-ai/blob/main/Skills%20Shed/AI%20Calculator/SKILL.md) | The AI Calculator quantifies the financial impact of AI in a contact center. It takes current-state metrics (call volume, AHT, agent salary, occupancy, FCR, digital volume) plus a set of AI optimization levers, and returns annual savings, agent (FTE) reduction, a per-lever savings breakdown, and a step-by-step calculation trace. Results render on screen and export to PDF/PPTX. |
| [Webex MCP Onboarding](https://github.com/ciscoAISCG/webex-cx-ai/blob/main/Skills%20Shed/webex-mcp-onboarding) | Guided assistant skill for onboarding MCP servers into Webex Developer Portal, Control Hub Agentic Apps, and AI Agent Studio. |

[Browse the Skills Shed](./Skills%20Shed)

---

## MCP Factory

Explore a number of MCP endpoints that you can use and deploy as part of your POCs or in production. This is a set of MCP endpoints that the team has used or developed and is shared here so that you can deploy this MCP endpoint yourself in your environment for your testing or production purposes 

[Browse the MCP Factory](./MCP%20Factory)

---

## Start Here

Choose the asset type based on the job you need to do.

| If you need to... | Start with... |
| --- | --- |
| Build from a proven starting point | `templates/` |
| Learn how to build or adapt something | `cookbooks/` |
| Make your AI assistant an expert in a repeatable task | `skills/` |
| Package a customer learning for others | `cookbooks/` or `templates/` |

Clone the repository:

```bash
git clone <REPOSITORY_URL>
cd ai-scg-assets
```

Then open the relevant asset folder:

```bash
cd templates
cd ../cookbooks
cd ../skills
```


## Contributing

Contributions should make the library more useful for the next consumer.

Good contributions usually come from:

- A customer engagement that produced a reusable pattern.
- A use case that should become easier to repeat.
- A demo that should become easier to rebuild.
- A best practice that should be applied consistently.
- A personal-assistant workflow that reliably improves build quality.

Before adding something new, check whether an existing asset should be improved instead. 

---

## About

This repository is maintained by AI SCG as a publishing library for reusable AI assets based on customer learnings.

It is built for teams that need to build, adapt and scale AI use cases faster.

---

## Licence

This project is licensed under the MIT License - use it, modify it, share it.

---

## Trademarks

This repository may reference Cisco products, services, trademarks, or logos. Use of Cisco trademarks or logos must follow Cisco brand and trademark guidance. Third-party trademarks remain the property of their respective owners.

---

Published by AI SCG.
