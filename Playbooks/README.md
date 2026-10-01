# Playbooks

Reusable, implementation-oriented Webex CX AI patterns. Each package includes its use-case guide and supporting assets; `manifest.yaml` supplies its searchable metadata.

Browse by searching or filtering the [website catalog](../Cookbooks/docs/playbooks.md), or open a playbook below. Entries are ordered newest first by their `date_added` manifest value.

| Playbook | Summary | Customer journey |
|---|---|---|
| [Configure Custom Data and Custom Events for AI Agents](configure-custom-data-custom-events-ai-agents/README.md) | Pass session data to an Autonomous Voice AI Agent, handle source-flow action exits through VAV2, parse MetaData, and return fulfillment data to continue the same conversation. | Customer Service, Self-Service, Routing & Transfer |
| [Retrieve AI Assistant Post-Call Summaries for Supervisor Reporting](post-call-ai-summary-reporting/README.md) | Retrieve AI Assistant wrap-up summaries after contact completion and expose selected fields through a historical Analyzer report for supervisor visibility. | Customer Service |
| [Send a Webex Contact Center Consult Summary to the Consulted Webex User](consult-transfer-summary-to-webex/README.md) | Resolve the user selected for a voice consult and send that person the MID_CALL AI summary as a direct Webex message. | Routing & Transfer |
| [Send Mid Call Consult Summaries to Webex Users with Flow Designer Event](consult-summary-to-webex-flow-designer-event/README.md) | Use a Webex Contact Center PreDial event and Webex Connect to resolve a consulted Webex user and send that person the MID_CALL summary as a direct Webex message. | Routing & Transfer |
| [ServiceNow-Hosted Incident MCP AI Agent](servicenow-hosted-incident-mcp-ai-agent/README.md) | Verify an employee and manage authorized ServiceNow incidents through a ServiceNow-hosted MCP server, with safe human handoff. | Case Management, Authentication |
| [Procedure-Guided AI Agent Pattern](procedure-guided-agent-pattern/README.md) | Select an approved procedure from a bounded catalogue, retrieve its guidance, and act through controlled, authoritative fulfillment results. | Customer Service |
| [Departmental Routing AI Agent (Scripted)](departmental-routing-ai-agent-scripted/README.md) | Collect and confirm a caller’s requested hospital department, then route the call to its matching queue with a scripted AI agent and voice flow. | Routing & Transfer |
| [Hospital Payment Agent (Scripted)](payment-ai-agent-scripted/README.md) | Collect payment intent and caller details, then use voice-flow state events and subflows for balance lookup and payment processing. | Payments, Authentication |
| [Order Tracking](order-tracking/README.md) | Retrieve order, delivery, and fulfillment status from a backend workflow and explain the result with human escalation when needed. | Order Management, Self-Service |
| [Concierge Routing Agent Template](concierge-ai-agent/README.md) | Classify incoming questions and route them to a specialist using an AI Agent Studio import, prompt template, and routing knowledge-base starter. | Routing & Transfer, Customer Service |
| [Appointment Scheduling](appointment-scheduling/README.md) | Schedule, review, and reschedule appointments with an autonomous voice AI agent and Webex Connect fulfillment workflows. | Scheduling |
| [Data-Driven Ordering](data-driven-ordering/README.md) | Guide callers through a structured menu, validate choices, place an order, and offer a digital fallback. | Self-Service, Order Management |
| [Directory Routing](directory-routing/README.md) | Classify a caller request as a person or department lookup, search directory resources, and transfer the caller to the matching destination. | Routing & Transfer |
| [ServiceNow Knowledge and Incident Agent with MCP](servicenow-kb-incident-ai-agent-with-mcp/README.md) | Search ServiceNow knowledge first, then create, find, update, or delete incidents through MCP-backed actions when needed. | Knowledge Support, Case Management |
| [User Identification and Verification](user-identification-verification/README.md) | Collect caller details, verify identity through a backend service, and continue protected journeys or escalate safely. | Authentication |
| [Visual Appointment Confirmation](visual-appointment-confirmation/README.md) | Send appointment details by SMS for caller review and confirm only after the caller approves or corrects them by voice. | Scheduling, Proactive Notifications |
| [Hospital Payment Line (Autonomous)](payment-ai-agent-autonomous/README.md) | Let patients check an outstanding hospital balance and pay by card through an autonomous voice AI agent with safe escalation. | Payments, Authentication |

## Folder name updates

Playbook folders use lowercase kebab-case. The original underscore-based paths are visible in the repository's rename history.
