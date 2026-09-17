# ServiceNow Scripted REST API v3 Reference

V3 consolidates the self-contained v2 resources into five concise resources. No Script Include or in-script role lookup is used. The AI agent authenticates the employee and supplies that employee's ServiceNow `sys_user.sys_id` as `caller_id`.

## Resources

| Method | Resource path | Script | Result |
|---|---|---|---|
| GET | `/users?employee_id=...` | `resources/lookup_user.js` | One user object |
| POST | `/incidents` | `resources/create_incident.js` | Created incident object |
| PUT | `/incidents/{incident_number}` | `resources/update_incident.js` | Update, resolve, or close result |
| GET | `/incidents/{incident_number}?caller_id=...` | `resources/lookup_incident.js` | One incident object |
| GET | `/incidents?caller_id=...` | `resources/list_incidents.js` | Array of incident objects |

For the ServiceNow MCP Console Request Schema field, use [`create_incident.schema.json`](../exports/servicenow/schemas/create_incident.schema.json) for creation and [`update_incident.schema.json`](../exports/servicenow/schemas/update_incident.schema.json) for updates. These are OpenAPI 3.0.1 Schema Objects describing raw JSON request bodies, not complete OpenAPI documents. Do not associate a request schema with a GET resource: GET path and query inputs are configured on the resource separately. A complete OpenAPI document is intentionally not included in this reference package.

When creating the schema record in ServiceNow, set `API` to the same Scripted REST API record used by the `create_incident` resource:

- API name: `Customer AI Incident API v3`
- API ID: `customer_ai_incident_v3`
- OpenAPI Version: `3.0.1`
- Schema: paste the contents of `schemas/create_incident.schema.json`

After saving the creation schema, open the v3 `POST /incidents` resource and add it in its Request Schema related list. Do not associate the schema with a GET resource, the v1 or v2 API, or a resource belonging to a different Scripted REST API record. ServiceNow requires the schema's API reference and the selected resource's API reference to be the same.

Create a second schema record for `update_incident.schema.json` using the same v3 API record, then associate it with the v3 `PUT /incidents/{incident_number}` resource. The flat body schema exposes all operation fields so MCP clients can map them reliably; the scripted resource enforces the operation-specific rules:

- `update`: requires `caller_confirmed` and `update_note`, `work_notes`, or both.
- `resolve`: requires `resolution_summary` and `caller_confirmed_resolved`.
- `close`: requires `resolution_summary`, `close_code`, and `caller_confirmed_resolved`; the incident must already be resolved.

For the GET resources, define and associate query parameters instead of request schemas:

- `lookup_user.js`: define `employee_id` as required, with example `954750` and a description stating that it is exactly six numeric digits. Associate it only with the v3 `GET /users` resource.
- `lookup_incident.js`: define required `caller_id` as the trusted 32-character `sys_user.sys_id`. The `incident_number` value comes from the `{incident_number}` relative-path parameter. Associate `caller_id` only with the v3 `GET /incidents/{incident_number}` resource.
- `list_incidents.js`: define required `caller_id` as the trusted 32-character `sys_user.sys_id`. Associate it only with the v3 `GET /incidents` resource.

ServiceNow request schemas describe request bodies; they do not route requests to resources. Create each MCP REST API tool against the exact v3 resource, enable only its associated inputs, and configure query parameters through the resource's Query Parameters related list. GET requests should not contain a JSON request body.

## Deployment

Create a new versioned Scripted REST API, for example:

- Name: `Customer AI Incident API v3`
- API ID: `customer_ai_incident_v3`
- Version: `v3`

Create the five resources above and paste in the matching scripts. Enable authentication and REST Endpoint ACL authorization on every resource. V3 does not use `gs.getUserID()` for caller ownership because that value may be the MCP integration user. It uses the validated `caller_id` supplied by the trusted AI-agent authentication layer.

Do not expose `caller_id` as an unrestricted model-generated value. Inject it from trusted session context, a signed claim, or an equivalent identity gateway. If the MCP client cannot provide that integrity guarantee, use a ServiceNow/OIDC user session instead.

Verify `STATE_RESOLVED`, `STATE_CLOSED`, and the impact/urgency mappings in `update_incident.js` against the target instance. These are commonly `6` and `7`, but ServiceNow choices can be customized.

## Request examples

Get the authenticated user by employee ID:

```http
GET /api/customer_ai_incident_v3/v3/users?employee_id=954750
```

The `employee_id` query parameter must contain exactly six numeric digits. The resource returns `sys_id`, `phone`, `mobile_phone`, and `employee_id` mapped from ServiceNow's `employee_number` field.

Get one incident for a caller:

```http
GET /api/customer_ai_incident_v3/v3/incidents/INC0012345?caller_id=46d4c3b0e1a24c1a9b3b2d4e5f6a7b8c
```

Create an incident for a caller:

```http
POST /api/customer_ai_incident_v3/v3/incidents
Content-Type: application/json

{
  "caller_id": "46d4c3b0e1a24c1a9b3b2d4e5f6a7b8c",
  "short_description": "External monitor has no display",
  "description": "The monitor stopped displaying this morning.",
  "work_notes": "Initial triage was completed by the AI agent.",
  "affected_scope": "single_user",
  "business_impact": "work_degraded",
  "caller_confirmed": true
}
```

Get a caller's incidents:

```http
GET /api/customer_ai_incident_v3/v3/incidents?caller_id=46d4c3b0e1a24c1a9b3b2d4e5f6a7b8c
```

The example `caller_id` is synthetic. It must be the 32-character ServiceNow `sys_user.sys_id` produced by the AI agent's trusted authentication flow.

Incident responses include the latest `work_notes` journal entry. Work notes are internal ServiceNow data; do not expose them to callers unless your organization explicitly approves that behavior.

Use one update payload with an explicit operation. For `operation: "update"`, provide `update_note`, `work_notes`, or both:

```http
PUT /api/customer_ai_incident_v3/v3/incidents/INC0012345
Content-Type: application/json

{
  "caller_id": "46d4c3b0e1a24c1a9b3b2d4e5f6a7b8c",
  "operation": "update",
  "update_note": "The issue also occurs without the dock.",
  "work_notes": "Caller reports the issue occurs with a direct cable connection.",
  "caller_confirmed": true
}
```

For `resolve`, use `resolution_summary`, optional `resolution_code`, and `caller_confirmed_resolved: true`. For `close`, use `resolution_summary`, `close_code`, and `caller_confirmed_resolved: true`. Closing requires the configured Resolved state.

## MCP registration

Register each resource as a REST API tool in MCP Server Console. Expose only the documented query, path, and body inputs. Use OAuth/SSO for authentication; employee ID and phone number are lookup values, not credentials.

The scripts use `GlideRecordSecure`, `caller_id` ownership filters, allowlisted fields, confirmation flags, basic secret redaction, and correlation-based idempotency for repeated updates. Test all resources in a nonproduction instance before activation.
