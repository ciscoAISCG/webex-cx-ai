# AI Agent Studio JSON Import Guidance

Use this guidance when generating a JSON file that can be imported into Webex AI Agent Studio. This structure is based on exported AI Agent Studio sample files.

## Top-Level Structure

Generate a JSON object with these top-level keys:

- `bot_type`: usually `virtualagent`.
- `configuration`: agent metadata, model settings, instructions, welcome message, and voice settings.
- `tools`: system tools and action tools.

## Configuration Object

Use these common fields:

```json
{
  "ai_engine": "PRO_US",
  "default_language": "en-US",
  "kb_ids": [],
  "llm_agent_description": "<Agent Goal>\n\n### INSTRUCTIONS:\n<Detailed AI Agent Instructions>",
  "llm_model": "1.0.0",
  "logo": "https://aiagent.webexbotbuilder.com/static/assets/img/bot-logo/default-virtualagent.svg",
  "timezone": "Europe/London",
  "voice_settings": {},
  "welcome_message": "<Suggested Greeting>"
}
```

For voice agents, include voice settings similar to the samples, but keep the selected voice as a placeholder because the user must choose or confirm the available voice in their tenant. A safe placeholder structure is:

```json
{
  "advance_settings": {
    "global": {
      "delays_and_interruptions": {
        "caller_turn_timeout": 1500,
        "custom_no_input": 10,
        "customer_interruption": true,
        "eos_sensitivity": 500,
        "fulfilment_timeout": 30,
        "slots_additional_delay": 800
      },
      "dtmf_settings": {
        "max_length": 16,
        "term_char": "#",
        "timeout_between_digits": 5,
        "turn_on_dtmf": true
      },
      "is_customized": false,
      "response_settings": {
        "custom_vocabulary": [],
        "include_disfluencies": true,
        "response_style": "ACTIVE"
      }
    }
  },
  "voices": [
    {
      "displayName": "<VOICE_DISPLAY_NAME_PLACEHOLDER>",
      "language": "<VOICE_LANGUAGE_PLACEHOLDER>",
      "locale": "<VOICE_LOCALE_PLACEHOLDER>"
    }
  ]
}
```

## Tools Array

Always include the handover system tool unless the user explicitly excludes escalation:

```json
{
  "capability": "slot_filling",
  "description": "Escalate the conversation to a human agent if the user asks for it or the request cannot be completed safely.",
  "enabled": true,
  "fulfillment": {},
  "id": "<unique_32_char_hex_id>",
  "name": "Agent handover",
  "slots": [],
  "slots_view": "table",
  "system_tool": true
}
```

For each business action, generate a tool entry:

```json
{
  "capability": "slot_filling_with_fulfillment",
  "description": "<action purpose and parameter sourcing guidance>",
  "enabled": true,
  "fulfillment": {
    "authentication": {
      "service_key": "",
      "type": "ci_bearer_token"
    },
    "code": "",
    "flow_id": 0,
    "flow_name": "<WEBEX_CONNECT_FLOW_NAME_PLACEHOLDER>",
    "output_entities": {
      "parameters": {
        "properties": {},
        "required": [],
        "type": "object"
      }
    },
    "output_entities_format": "table",
    "output_entities_text": "",
    "output_entities_view": "table",
    "service_id": "",
    "service_name": "<WEBEX_CONNECT_SERVICE_NAME_PLACEHOLDER>",
    "type": "flow",
    "webhook_url": "<WEBEX_CONNECT_WEBHOOK_URL_PLACEHOLDER>"
  },
  "id": "<unique_32_char_hex_id>",
  "input_entities": {
    "parameters": {
      "properties": {
        "<parameter_name>": {
          "description": "<plain-language parameter description>",
          "examples": [],
          "type": "string"
        }
      },
      "required": ["<required_parameter_name>"],
      "type": "object"
    }
  },
  "name": "<action_name>",
  "slots_view": "table",
  "system_tool": false
}
```

## Generation Rules

- Generate valid JSON only in the artifact file. Do not include comments or Markdown fences in the file.
- Always provide the full file location of any generated or updated JSON artifact in the final response.
- Populate `configuration.llm_agent_description` with both the agent goal and the detailed instructions.
- Format `configuration.llm_agent_description` as: agent goal text, then a blank line, then the literal separator `### INSTRUCTIONS:`, then the detailed AI agent instructions.
- Keep `configuration.welcome_message` aligned with the Suggested Greeting section.
- Always set `configuration.kb_ids` to `[]`. Do not include placeholder, guessed, or example KB IDs because invalid KB IDs can cause import or UI errors.
- Keep every referenced action name exactly the same in instructions and `tools[].name`.
- Always use placeholders for Webex Connect service name, Webex Connect service ID, flow IDs for each action, webhook URLs for each flow, preferred voice, and whether backend actions are real, mocked, or routed through Webex Connect flows.
- Use a valid IANA timezone value in `configuration.timezone`, such as `Europe/London` or `America/Los_Angeles`. Do not use a placeholder for timezone because AI Agent Studio validates this field during import.
- Use unique generated placeholder tool IDs so the JSON remains structurally valid.
- Use `flow_id: 0`, empty `service_id`, placeholder `webhook_url`, and descriptive placeholder `flow_name` values for Webex Connect details.
- Represent action parameters in `input_entities.parameters.properties`, using JSON Schema-compatible property definitions.
- Include optional parameters in `properties` but not in `required`.
- Do not invent real Epic, Webex Connect, service, flow, webhook, or knowledge base IDs.
- Tell the user that they must manually create the required Webex Connect flows, services, voice settings, and backend routing before replacing placeholders and using the JSON beyond a draft/demo import. If they need a different timezone or knowledge sources, they should update them manually in Studio after import.
