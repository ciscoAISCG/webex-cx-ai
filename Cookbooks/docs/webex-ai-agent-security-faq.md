# Security FAQ

This FAQ summarizes common security, privacy, governance, and compliance questions that teams may ask when evaluating Webex Contact Center AI agents.

## 1. How are the models tested and validated?

Webex AI Agent is validated through Cisco’s Responsible AI governance process, including an AI Impact Assessment for AI-powered capabilities, along with ongoing human-led testing, review, and quality assurance.

For autonomous AI agents, models such as GPT-4o and GPT-4.1-mini have been selected based on Cisco research and benchmarking across factors such as:

- conversational quality
- latency
- cost efficiency

Cisco continues to evaluate third-party models over time to maintain and improve performance. However, the platform does not currently provide a fixed tested-version matrix or explicit pass/fail threshold documentation for the full end-to-end solution.

## 2. What third-party providers are involved?

Autonomous AI agents use Microsoft Azure OpenAI Service for large language model capabilities.

Depending on the AI engine selected, additional providers may be used for speech-related services. For example:

- ElevenLabs for text-to-speech
- Deepgram for speech-to-text

Cisco applies vendor review, security assessment, and safety evaluation processes when working with these providers. Cisco also states that customer data sent to these providers is not permitted to be used for model training or improvement, and is not retained beyond the immediate transaction.

For U.S.-based deployments, supported speech services are processed in U.S. regions.

## 3. How is model behavior monitored?

Cisco uses telemetry to monitor service performance, availability, and operational health of the underlying AI infrastructure. In some cases, requests can be rerouted when technical issues such as latency or regional degradation occur.

However, Webex AI Agent Studio is a platform that allows customers to define their own:

- goals
- prompts
- instructions
- knowledge sources
- actions

Because of that, customers remain responsible for validating and monitoring the behavior of the agents they configure.

Today, the platform provides visibility through session review and analytics capabilities, but it does not currently offer a formal Cisco-managed cadence for proactively reporting issues such as:

- hallucinations
- model drift
- safety degradation

Additional observability and analytics capabilities are planned on the roadmap.

## 4. How are fairness and bias handled?

Fairness and bias are considered within Cisco’s broader AI safety and governance framework.

For autonomous agents, the underlying third-party models may still reflect societal bias. For that reason, fairness-related review should include the transparency and responsible AI materials provided by the model provider.

For more deterministic or scripted agents, the risk of biased language generation is generally reduced because those experiences rely more heavily on customer-defined intents, rules, and training data.

Cisco’s governance framework applies to the platform, but there is not currently a published recurring bias-reporting cadence or statistical bias report specific to each autonomous or scripted deployment.

## 5. Where does processing happen and what about data locality?

Webex AI Agent can be deployed in supported regions, including U.S. deployments such as `produs1`.

For the use case covered in this material:

- speech-to-text and text-to-speech are U.S.-only
- telemetry and logs are stored in the U.S.

At the same time, Cisco operates as a global cloud service organization, so authorized support and engineering personnel outside the U.S. may access logs for support and operational purposes where needed.

Teams with strict residency requirements should confirm locality and support-access expectations during final security and privacy review.

## 6. How transparent are the inputs, outputs, and system behavior?

Customers can control important parts of the agent experience, including:

- business logic
- agent instructions
- allowed actions
- grounding content
- escalation design

However, customers do not currently have full visibility into system-level prompts or the ability to override guardrails directly.

The platform roadmap indicates that additional features are planned to help customers:

- manage safety and compliance policies
- control guardrails more directly
- define enterprise-level policies
- enforce agent-level security posture more consistently

## 7. What are the retention and deletion policies?

Retention depends on the service component.

For AI Agent Studio specifically:

- the default retention period is 90 days

For Contact Center-related content, retention may depend on the applicable customer setup, contractual policy, and service configuration.

In some cases, retention can be configured at the organization level. In other cases, changes may require Cisco support rather than self-service administration.

When deletion is requested, Cisco states that it endeavors to delete requested data from its systems within 30 days unless retention is required for legitimate business purposes.

For third-party model providers, Cisco states that customer data processed through those services is not used for model training or improvement and is not retained beyond the immediate transaction. If a deployment requires explicit zero-retention confirmation for every provider involved, that should be validated as part of the final security and privacy review.

## Practical Takeaway

When evaluating AI agent security, do not look only at the model. Review the full operating model, including:

- governance
- vendor dependencies
- observability
- retention
- locality
- compliance controls
- customer responsibilities after deployment

A secure deployment depends on both platform safeguards and disciplined customer configuration.
