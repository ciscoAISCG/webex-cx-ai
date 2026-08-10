# Skills

Personal-assistant skills for repeatable Webex CX AI workflows.

> **Marketplace or standalone?** Put a standalone, manually installed skill in
> `Skills/`. To distribute a skill through the AI SCG Plugin Marketplace,
> package it as a plugin by following the [Plugins contributor guide](../Plugins/README.md#contributors-publish-a-marketplace-plugin).

## Contributors: build a standalone skill

Use this folder when the contribution is a reusable skill that does not need
marketplace installation. Create:

```text
Skills/<skill-name>/
└── SKILL.md
```

- Use a short, lower-case, hyphenated folder name.
- Include `name` and a specific trigger-oriented `description` in the
  `SKILL.md` frontmatter.
- Add only the scripts, references, or assets the skill actually needs.
- Test the skill, remove secrets and customer data, and submit it through a
  feature branch and pull request.

Suggested Codex request:

> Create an AI SCG standalone skill named `<skill-name>` and prepare a pull
> request for the `Skills/` folder.

## Skills

| Skill | Purpose |
| --- | --- |
| [WhatsApp SIP Gateway](./whatsapp/) | Build, deploy, and troubleshoot a Meta WhatsApp Calling SIP gateway for Cisco Webex Contact Center and Webex AI Agents. |
| [AI Calculator](./AI%20Calculator/) | Skill workspace for ROI CC Calculations. |
| [Webex MCP Onboarding](./webex-mcp-onboarding/) | Guided assistant skill for onboarding MCP servers into Webex Developer Portal, Control Hub Agentic Apps, and AI Agent Studio. |
| [AWS SigV4 MCP Onboarding](./aws-sigv4-mcp-onboarding/) | Securely validate and connect AWS IAM SigV4-protected AgentCore MCP servers to Codex and other STDIO-capable MCP clients. |
| [AI Agent Creator](./webex-ai-agent-creator/) | A skill for helping create an AI Agent using all of the best practices. |
