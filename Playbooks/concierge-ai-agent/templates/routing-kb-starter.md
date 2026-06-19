# Routing KB Starter

Use this content as the first routing knowledge base for the concierge agent. The purpose of this KB is classification and handoff support, not deep product troubleshooting.

## Article 1: domain-contact-center-routing

### Domain definition

This domain owns Contact Center topics such as queue routing, agents, supervisors, IVR, reporting, and operational service flows.

### Common user goals

- Configure queue routing
- Set up an IVR
- Understand agent behavior
- Troubleshoot digital or voice routing
- Review supervisor visibility and reporting

### Typical phrases

- How do I configure queue routing?
- Why are agents not receiving chats?
- How do supervisors view reports?
- How do I set up an IVR?

### Strong routing indicators

- queue
- IVR
- agent
- supervisor
- routing
- report
- digital channel
- contact center

### Do not route here when

- the user is mainly asking about AI Agent Studio instructions
- the user is mainly asking about Webex Connect flows, APIs, or webhooks

### Route target

`contact_center_expert`

## Article 2: domain-webex-ai-agent-routing

### Domain definition

This domain owns Webex AI Agent topics such as AI Agent Studio, instructions, actions, tools, greetings, knowledge base use, and agent behavior design.

### Common user goals

- Write AI agent instructions
- Configure actions
- Design knowledge usage
- Tune greetings and handoff behavior
- Test and improve an AI agent

### Typical phrases

- How do I write AI Agent Studio instructions?
- How do I add actions to my AI agent?
- Why is my AI agent not using the knowledge base?
- How do I route from one AI agent to another?

### Strong routing indicators

- AI Agent Studio
- instructions
- prompt
- tool
- action
- knowledge base
- greeting
- handoff

### Do not route here when

- the user is mainly asking about Webex Connect orchestration
- the user is mainly asking about Contact Center operational routing or supervisor behavior

### Route target

`webex_ai_agent_expert`

## Article 3: domain-webex-connect-routing

### Domain definition

This domain owns Webex Connect topics such as flows, orchestration, APIs, webhooks, messaging journeys, fulfillment integration, and channel automation.

### Common user goals

- Build a Connect flow
- Trigger a webhook
- Orchestrate fulfillment
- Connect backend services
- Drive routing through structured flows

### Typical phrases

- How do I create a Webex Connect flow?
- How do I trigger a webhook from the bot?
- How do I integrate Connect with the AI agent?
- How do I orchestrate routing in Connect?

### Strong routing indicators

- flow
- webhook
- API
- orchestration
- journey
- trigger
- fulfillment
- integration

### Do not route here when

- the user is mainly asking about AI Agent Studio instructions
- the user is mainly asking about Contact Center queueing, IVR, or reporting

### Route target

`webex_connect_expert`

## Article 4: cross-domain-disambiguation

Use these rules when multiple domains appear in one request.

- If the user is asking about agent behavior, prompts, tools, or KB design, route to `webex_ai_agent_expert`.
- If the user is asking about flows, orchestration, APIs, or webhooks, route to `webex_connect_expert`.
- If the user is asking about queues, IVR, agents, supervisors, or reporting, route to `contact_center_expert`.
- If confidence is low, ask one concise clarifying question.
- If the request spans multiple domains, route based on the user's primary intended outcome.

## Article 5: unsupported-topics-and-fallback

If the request does not belong to Contact Center, Webex AI Agent, or Webex Connect:

- explain the supported domains briefly
- ask the user whether their request belongs to one of those areas
- offer human escalation if that is available

Do not guess a specialist domain when the topic is clearly unsupported.
