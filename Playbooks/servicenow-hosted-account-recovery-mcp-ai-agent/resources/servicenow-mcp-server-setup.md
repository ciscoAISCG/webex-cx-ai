# Configure the ServiceNow MCP Server

This guide configures ServiceNow MCP Server Console to expose the account-recovery Scripted REST API resources as MCP tools for the Webex AI Agent.

## Production safety gate

The included reset and unlock scripts assume that the AI agent already called the security-answer verification tool. They do not independently enforce that verification succeeded for the same caller and session. A prompt rule or tool ordering is not an authorization control.

Do not add reset_user_password or unlock_user_account to a production MCP server until ServiceNow enforces a server-side, session-bound verification state (or an equivalent authorization check) before each mutation. The direct endpoints must reject a call that lacks proof of successful verification, even if the request comes from an authenticated MCP client. Add a negative test for this condition before enabling either tool.

## Prerequisites

- Confirm the ServiceNow family and installed MCP Server Console application support REST API tools.
- Use web_service_admin to create the Scripted REST API, resources, and schemas.
- Use sn_mcp_server.admin to create the server and sn_mcp_server.tools_admin or sn_mcp_server.admin to create REST API tools.
- Use oauth_admin, mi_admin, or admin only for the OAuth inbound integration setup.
- Build and validate in a nonproduction instance with synthetic employee data.

## 1. Create or confirm the Scripted REST API

In ServiceNow, open All > System Web Services > Scripted REST APIs. Create a purpose-specific API for account recovery, or select the existing API that contains these resources. The full REST URI includes the instance, namespace, optional version, API ID, and relative path:

https://<instance>.service-now.com/api/<namespace>/<version>/<api_id>/<resource_path>

The resource scripts in this package use these relative paths:

| MCP tool | Method and relative path | Inputs |
|---|---|---|
| lookup_user_record | GET /users | Query parameter employee_id, exactly six digits. |
| retrieve_security_questions | GET /questions/{user_id} or GET /questions | Path or query parameter user_id, returned by the user lookup. |
| verify_security_answers | POST /answers | Raw JSON body described by verify_security_answers.schema.json. |
| unlock_user_account | POST /unlock | Raw JSON body described by unlock_user_account.schema.json. |
| reset_user_password | POST /reset | Raw JSON body described by reset_user_password.schema.json. |

Create one REST API resource per method/path, paste the matching JavaScript from exports/servicenow/resources/, and define GET query/path parameters in the resource. Confirm the paths match the request parsing in each script.

## 2. Attach request schemas and protect the REST resources

For each POST resource, create an associated REST Schema using OpenAPI 3.0.1 and attach it as that resource's request structure. The three schema files in exports/servicenow/schemas/ contain schema objects for the raw HTTP request bodies; do not add a second request_body property to those bodies.

Require authentication and a REST Endpoint ACL on the API or each resource. Restrict access to the dedicated recovery role and grant the runtime identity only the minimum record/table permissions needed by the scripts. Do not make the API public or grant broad administrator roles to the runtime identity.

Configure the ServiceNow property webexccai.pwd_reset.caller_role to the approved narrow role if it differs from the script default. Configure webexccai.pwd_reset.verification_id to the target instance's security-question verification record. The answer-verification script fails closed when that value is missing or invalid. Confirm excluded-role and enrollment behavior against the target instance.

## 3. Create MCP tools from the REST resources

In MCP Server Console, create a tool for each eligible resource using the REST API tool category. Select the REST API, an active MCP app linked to that API, and the MCP server. Use specific descriptions that say when the tool should run and list required inputs and formats.

Use these tool names to match the Agent export:

| Tool name | Required description details | Access and behavior |
|---|---|---|
| lookup_user_record | Look up one active user by six-digit employee ID; an ID match is not identity verification. | Read-only, narrowly scoped access. |
| retrieve_security_questions | Retrieve enrolled questions for the user_id returned by lookup. | Read-only, narrowly scoped access. |
| verify_security_answers | Verify three question IDs and answers for the same user_id; never disclose answers or which answer failed. | Sensitive verification operation; expose only required body fields. |
| unlock_user_account | Unlock the verified user's account; require a server-side verification gate. | State-changing; keep disabled until the production safety gate passes. |
| reset_user_password | Reset the verified user's password and require a change at next sign-in; require a server-side verification gate. | Highly sensitive state change; keep disabled until the production safety gate passes. |

Set Required roles to the approved recovery role, mark read-only and state-changing/destructive annotations accurately, and disable inputs the tool does not need. Review the tool list before changing a tool already used by another MCP server.

## 4. Create a purpose-specific MCP server

In MCP Server Console, open Configuration > Servers and create a separate server for account recovery. Give it a clear label, name, and short description. Add only the intended account-recovery tools. Initially use a nonproduction server with lookup and verification tools; keep reset and unlock out until the server-side verification gate is implemented and tested.

Save as draft while configuring. After validation, activate the server. ServiceNow generates an endpoint in this form:

https://<instance>.service-now.com/sncapps/mcp-server/mcp/<server-name>

Use the generated endpoint in the Webex MCP registration; do not copy a tenant URL into this public playbook.

## 5. Resolve authentication compatibility before connecting Webex

The source Agent export uses OAuth 2.0 client credentials. Webex AI Agent Studio currently documents OAuth 2.0 client credentials, API key, and custom-header authentication for MCP actions, and says OAuth Authorization Code MCP tools are not selectable. ServiceNow's MCP Server Console client-connection procedure documents an OAuth inbound integration using Authorization Code grant and JWT tokens; the ServiceNow MCP Server Console FAQ says client-credentials grant is not currently supported for these connections.

Therefore, do not assume the native ServiceNow MCP Server Console and this Webex client can authenticate directly in every release combination. Confirm the exact ServiceNow MCP Server Console version and approved authentication path with both platform owners before configuring credentials. If they do not support a compatible method, stop and obtain an approved compatible integration design; do not disable authentication or expose the API publicly as a workaround.

When compatibility is confirmed, create a dedicated OAuth integration/identity for the Webex client, keep credentials in approved secret storage, and authorize only the required server and tools. The exact registration form depends on the supported flow and client redirect behavior.

## 6. Validate before production

- Confirm the MCP server discovers exactly the intended tool names and inputs.
- Verify unauthenticated requests and requests without the recovery role are denied.
- Use synthetic accounts to check lookup, question retrieval, answer verification, and error handling.
- Verify reset and unlock are denied unless ServiceNow confirms successful verification for the same caller/session.
- Confirm a caller cannot select another user's sys_id to reset or unlock that account.
- Ensure temporary passwords and security answers do not enter tool traces, transcripts, or logs beyond approved handling.
- Validate Webex action status, input mapping, OAuth binding, and handoff behavior in a nonproduction tenant before enabling the production server.

## Official references

- [Create a server](https://www.servicenow.com/docs/r/intelligent-experiences/create-mcp-server.html)
- [Create a tool from a REST API](https://www.servicenow.com/docs/r/intelligent-experiences/create-a-tool-from-rest-api.html)
- [Scripted REST APIs](https://www.servicenow.com/docs/r/api-reference/rest-api-explorer/c_CustomWebServices.html)
- [Define a REST API schema](https://www.servicenow.com/docs/r/api-reference/rest-api-explorer/define-scripted-rest-api-schema.html)
- [Create an OAuth inbound integration for an MCP client](https://www.servicenow.com/docs/r/intelligent-experiences/create-oauth-inbound-integration-mcp-client.html)
- [MCP Server Console FAQ](https://www.servicenow.com/community/servicenow-otto-articles/mcp-server-console-faq/ta-p/3550125)
- [Webex AI Agent Studio Administration Guide](https://help.webex.com/en-us/article/ncs9r37/Get-started-with-Webex-AI-Agent)
