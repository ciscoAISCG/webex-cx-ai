# Pre-built templates

Templates are pre-built use cases that help teams move quickly from idea to execution.

They are designed to give consumers a practical starting point: the structure, flow, components, prompts, and configuration patterns needed to build a specific AI use case — without rebuilding the basics every time.

## When to use templates

Use a template when you need to:

- **Build a customer use case quickly** — skip the boilerplate and focus on what's unique to the customer.
- **Recreate a proven demo or workflow** — reuse something that has already been field-tested.
- **Standardise a repeatable solution pattern** — keep delivery consistent across teams and engagements.
- **Adapt a field-tested use case for a new customer or vertical** — re-skin and re-tune instead of re-architecting.

## What's in a template

Each template typically includes:

- **Flow / subflow exports** — the Webex Contact Center flow assets you can import directly.
- **AI agent exports** — the wording, parameters, and toggles that drive agent behavior.
- **README** — what the template does, how it's wired, how to deploy and test.

## Available templates

| Template | Description |
|---|---|
| [Data_Driven_Ordering](Data_Driven_Ordering/README.md) | Autonomous voice AI agent that uses a structured JSON menu to guide, validate, and place a configurable drink order, with Webex Connect fulfillment and digital-ordering fallback. |
| [User_Identification_Verification](User_Identification_Verification/README.md) | AI Agent pattern for collecting caller details, verifying identity with a backend service, and safely continuing or escalating based on the authentication result. |
| [Payment_AI_agent](Payment_AI_agent/README.md) | Autonomous voice AI agent ("Remy") that lets patients check a hospital balance and pay by credit card end-to-end, with safe escalation to a human billing specialist. |
| [ServiceNow KB + Incident AI Agent With MCP](ServiceNow_KB_Incident_AI_Agent_With_MCP/README.md) | Autonomous voice AI agent that uses MCP to search the ServiceNow Knowledge Base first, then create, search, update, or delete incidents when a ticket is needed. |
| [Visual_Appointment_Confirmation](Visual_Appointment_Confirmation/README.md) | Autonomous voice AI agent that collects appointment details, sends an SMS summary for visual review, and confirms the booking only after the caller approves or corrects the details. |

> Contributing a new template? Drop it in its own subfolder with a `README.md` that follows the same structure (overview, architecture, deployment steps, sample data, security notes).
