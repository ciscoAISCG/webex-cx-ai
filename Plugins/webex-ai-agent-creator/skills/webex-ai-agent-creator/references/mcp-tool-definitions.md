# MCP Tool Definition Guidance

Use this reference only when the user opts to create MCP server tool definitions for the recommended agent actions. An MCP tool definition describes a server's callable interface; it is not an MCP server implementation, transport configuration, authentication setup, or backend fulfillment code.

## Output Contract

- Create one MCP Tool object for each action the user wants exposed through MCP.
- Keep the MCP definitions separate from any Webex AI Agent Studio JSON. Similar action names do not make the two formats interchangeable.
- Include `name`, `description`, `inputSchema`, and `outputSchema` on every generated tool. MCP permits `outputSchema` to be omitted, but this workflow requires it so the expected output entities and types are explicit.
- Use JSON Schema Draft 2020-12 for both schemas. Each schema must be a complete object schema with explicit `type`, `properties`, and `required` wherever relevant.
- Keep the tool name aligned with the action name used in the agent instructions and action table. Use a unique name with ASCII letters, digits, underscores, hyphens, or dots; avoid spaces.
- Write descriptions that explain the purpose and each property's meaning. Preserve the action's required and optional inputs.
- Define every input and output entity: primitive type, description, nested object properties, array item schema, required fields, and known constraints such as `enum`, `format`, `pattern`, `minimum`, `maximum`, `minLength`, or `maxLength`. Add constraints only when supported by the use case or confirmed by the user.
- Set `additionalProperties: false` on closed objects when the contract is intended to reject undeclared fields. Do not silently close objects when extension fields are expected.
- Model the expected successful structured result in `outputSchema`. Do not include MCP JSON-RPC envelopes, `CallToolResult` wrappers, or transport fields inside the business output schema.
- Represent execution failures through the MCP tool result error mechanism (`isError: true`) and describe the expected recovery behavior separately. Do not invent a business error object in `outputSchema` unless the action contract explicitly returns errors as structured data.
- If the result shape or a field's type is unknown, ask a focused question when that uncertainty changes the contract. Otherwise label the proposed shape as an assumption and make it easy for the user to correct; never present invented fields as confirmed backend behavior.
- Do not add `annotations`, security claims, authorization behavior, or destructive/read-only hints unless they are supported by the confirmed action semantics.

## Definition Shape

Return the tool objects directly, usually as a JSON array that can be used as the `tools` value in an MCP `tools/list` result. Do not wrap them in a JSON-RPC request or response unless the user asks for a complete protocol example.

```json
[
  {
    "name": "book_appointment",
    "description": "Books an appointment for a verified patient.",
    "inputSchema": {
      "$schema": "https://json-schema.org/draft/2020-12/schema",
      "type": "object",
      "properties": {
        "patient_id": {
          "type": "string",
          "description": "Identifier of the patient whose appointment is being booked."
        },
        "appointment_type": {
          "type": "string",
          "description": "Type of appointment requested.",
          "enum": ["consultation", "follow_up"]
        },
        "preferred_time": {
          "type": "string",
          "description": "Optional preferred appointment time in ISO 8601 date-time format.",
          "format": "date-time"
        }
      },
      "required": ["patient_id", "appointment_type"],
      "additionalProperties": false
    },
    "outputSchema": {
      "$schema": "https://json-schema.org/draft/2020-12/schema",
      "type": "object",
      "properties": {
        "appointment_id": {
          "type": "string",
          "description": "Identifier assigned to the booked appointment."
        },
        "start_time": {
          "type": "string",
          "description": "Confirmed appointment start time in ISO 8601 date-time format.",
          "format": "date-time"
        },
        "location": {
          "type": "object",
          "description": "Location where the appointment will take place.",
          "properties": {
            "name": {
              "type": "string",
              "description": "Display name of the clinic or facility."
            },
            "address": {
              "type": "string",
              "description": "Street address of the clinic or facility."
            }
          },
          "required": ["name", "address"],
          "additionalProperties": false
        }
      },
      "required": ["appointment_id", "start_time", "location"],
      "additionalProperties": false
    }
  }
]
```

The sample is illustrative. Do not copy its fields or enum values into a user's tool contract unless they fit the confirmed use case.

## Completeness Review

Before delivering MCP definitions, verify that:

1. Every selected action has exactly one definition and the names match the agent action names.
2. Both schemas are present and define all expected request and successful response entities, including nested objects and array items.
3. Each schema marks required and optional properties accurately; `required` contains only names present in that object's `properties`.
4. The JSON is syntactically valid and contains no invented IDs, credentials, backend details, or unconfirmed data fields.
5. The final response states any assumptions and distinguishes the interface definition from server implementation and deployment.

## MCP Specification

Follow the MCP server Tools specification for the Tool object, input and output schemas, structured results, and execution errors:

- <https://modelcontextprotocol.io/specification/2025-11-25/server/tools>
