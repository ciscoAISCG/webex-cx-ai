#!/usr/bin/env python3
"""Render a Webex MCP onboarding build recipe from intake JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


EXAMPLE = {
    "title": "Customer Records MCP Agent",
    "audience": "both",
    "environment": "sandbox",
    "tenant_org": "Example Lab Org",
    "target_agent": "TBD after Developer Portal and Control Hub onboarding",
    "developer_portal_url": "https://developer.webex.com/my-apps/new/agentic-server",
    "control_hub_agentic_apps_url": "https://admin.webex.com/apps/agentic-servers",
    "studio_agents_url": "https://studio.aiagent-us1.cisco.com/static/core/viewbots",
    "agent_goal": "Let the agent look up customer account status using an approved MCP tool.",
    "mcp_server": {
        "name": "customer-records-mcp",
        "purpose": "Read-only customer account lookup",
        "app_url": "https://mcp.example.com/mcp",
        "transport_type": "Streamable HTTP",
        "authentication": "OAuth2 client credentials",
        "logo_plan": "Use approved default option for draft; upload customer logo before distribution.",
        "owner": "Customer integrations team",
        "hosting_owner": "Customer integrations team",
        "security_review": "Required before production because the MCP server is externally hosted.",
        "webex_connect_alternative": "Possible for single workflow fulfillment, but MCP is preferred for reusable customer lookup tools.",
    },
    "tools": [
        {
            "name": "lookupCustomer",
            "purpose": "Retrieve account status by customer ID",
            "allowed_actions": "read only",
            "sensitive_data": ["customerId", "accountStatus"],
            "required_inputs": ["customerId"],
            "expected_outputs": ["accountStatus", "nextBestAction"],
            "test_case": "Lookup sample customer CUST-1001",
        }
    ],
    "agent_instructions": {
        "when_to_call": "Call lookupCustomer only after the user provides or confirms the customer ID.",
        "orchestration": "Single read-only call; no multi-tool orchestration required.",
        "confirmation_gates": "No write actions. Do not ask for secrets.",
        "success_language": "Summarize account status and the next recommended step.",
        "failure_language": "Ask the user to verify the customer ID or offer handoff after one failed retry.",
    },
    "access_policy": "Expose only to the target sandbox agent and builder group.",
    "test_data": "Use synthetic customer records only.",
    "production_notes": "Requires security review before production enablement.",
}


REQUIRED_TOP_LEVEL = [
    "title",
    "audience",
    "environment",
    "tenant_org",
    "agent_goal",
    "mcp_server",
    "tools",
    "access_policy",
    "test_data",
]

REQUIRED_SERVER = ["name", "purpose", "app_url", "authentication", "owner"]
REQUIRED_TOOL = ["name", "purpose", "allowed_actions", "required_inputs", "expected_outputs", "test_case"]


def load_intake(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Intake JSON must be an object")
    return data


def missing_fields(data: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for key in REQUIRED_TOP_LEVEL:
        if not data.get(key):
            missing.append(key)

    server = data.get("mcp_server")
    if isinstance(server, dict):
        for key in REQUIRED_SERVER:
            if key == "app_url" and server.get("url_or_transport"):
                continue
            if not server.get(key):
                missing.append(f"mcp_server.{key}")
    elif server is not None:
        missing.append("mcp_server must be an object")

    tools = data.get("tools")
    if isinstance(tools, list) and tools:
        for index, tool in enumerate(tools, start=1):
            if not isinstance(tool, dict):
                missing.append(f"tools[{index}] must be an object")
                continue
            for key in REQUIRED_TOOL:
                if not tool.get(key):
                    missing.append(f"tools[{index}].{key}")
    elif tools is not None:
        missing.append("tools must be a non-empty list")

    return missing


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def bullet_list(items: list[str], indent: str = "") -> str:
    if not items:
        return f"{indent}- None provided"
    return "\n".join(f"{indent}- {item}" for item in items)


def server_value(server: dict[str, Any], key: str, fallback: str | None = None) -> Any:
    value = server.get(key)
    if value:
        return value
    if fallback:
        return server.get(fallback)
    return None


def render(data: dict[str, Any]) -> str:
    server = data.get("mcp_server") if isinstance(data.get("mcp_server"), dict) else {}
    tools = data.get("tools") if isinstance(data.get("tools"), list) else []
    missing = missing_fields(data)

    lines: list[str] = []
    title = data.get("title") or "Webex MCP Agent"
    lines.append(f"# {title} Build Recipe")
    lines.append("")
    lines.append("## Goal")
    lines.append(str(data.get("agent_goal") or "TBD"))
    lines.append("")
    lines.append("## Starting Links")
    lines.append(f"- Developer Portal Agentic App form: {data.get('developer_portal_url') or 'https://developer.webex.com/my-apps/new/agentic-server'}")
    lines.append(f"- Control Hub Agentic Apps: {data.get('control_hub_agentic_apps_url') or 'https://admin.webex.com/apps/agentic-servers'}")
    lines.append(f"- AI Agent Studio agents: {data.get('studio_agents_url') or 'https://studio.aiagent-us1.cisco.com/static/core/viewbots'}")
    lines.append("")
    lines.append("## Audience And Environment")
    lines.append(f"- Audience: {data.get('audience') or 'TBD'}")
    lines.append(f"- Environment: {data.get('environment') or 'TBD'}")
    lines.append(f"- Tenant/org: {data.get('tenant_org') or 'TBD'}")
    lines.append(f"- Target Studio agent: {data.get('target_agent') or 'TBD'}")
    lines.append("")
    lines.append("## MCP Server")
    lines.append(f"- Name: {server.get('name') or 'TBD'}")
    lines.append(f"- Purpose: {server.get('purpose') or 'TBD'}")
    lines.append(f"- App URL: {server_value(server, 'app_url', 'url_or_transport') or 'TBD'}")
    lines.append(f"- Transport type: {server.get('transport_type') or 'Streamable HTTP'}")
    lines.append(f"- Authentication: {server.get('authentication') or 'TBD'}")
    lines.append(f"- Logo plan: {server.get('logo_plan') or 'TBD'}")
    lines.append(f"- Owner: {server.get('owner') or 'TBD'}")
    lines.append("")
    lines.append("## MCP Fit Assessment")
    lines.append(f"- Hosting owner: {server.get('hosting_owner') or server.get('owner') or 'TBD'}")
    lines.append(f"- Security review: {server.get('security_review') or 'TBD'}")
    lines.append(f"- Webex Connect alternative: {server.get('webex_connect_alternative') or 'TBD'}")
    lines.append("- Recommendation: use MCP only when hosting ownership, auth, security, and tool value are clear; otherwise consider Webex Connect for fulfillment.")
    lines.append("")
    lines.append("## Tool Inventory")
    if tools:
        for tool in tools:
            if not isinstance(tool, dict):
                continue
            lines.append(f"### {tool.get('name') or 'Unnamed tool'}")
            lines.append(f"- Purpose: {tool.get('purpose') or 'TBD'}")
            lines.append(f"- Allowed actions: {tool.get('allowed_actions') or 'TBD'}")
            lines.append("- Required inputs:")
            lines.append(bullet_list(as_list(tool.get("required_inputs")), "  "))
            lines.append("- Expected outputs:")
            lines.append(bullet_list(as_list(tool.get("expected_outputs")), "  "))
            lines.append("- Sensitive data:")
            lines.append(bullet_list(as_list(tool.get("sensitive_data")), "  "))
            lines.append(f"- Test case: {tool.get('test_case') or 'TBD'}")
    else:
        lines.append("- No tools provided")
    lines.append("")
    instructions = data.get("agent_instructions") if isinstance(data.get("agent_instructions"), dict) else {}
    lines.append("## Agent Instruction Plan")
    lines.append(f"- When to call: {instructions.get('when_to_call') or 'TBD'}")
    lines.append(f"- Orchestration: {instructions.get('orchestration') or 'TBD'}")
    lines.append(f"- Confirmation gates: {instructions.get('confirmation_gates') or 'TBD'}")
    lines.append(f"- Success language: {instructions.get('success_language') or 'TBD'}")
    lines.append(f"- Failure language: {instructions.get('failure_language') or 'TBD'}")
    lines.append("")
    lines.append("## Four-Phase Build Order")
    lines.append("| Phase | Platform | Action | Evidence | Automation level |")
    lines.append("|---|---|---|---|---|")
    lines.append("| 1 | Webex Developer Portal | Register MCP server as an Agentic App | Details page, app ID, app URL, auth type | guided |")
    lines.append("| 2 | Control Hub | Open Apps -> Agentic Apps and click the new blocked MCP server row | External MCP server row, red Blocked status, detail page | guided |")
    lines.append("| 2a | Control Hub | On General, select Allowed for all users, enable automatic server data updates, then Save | Header/list status changes to Allowed | guided |")
    lines.append("| 2b | Control Hub | On Authentication, fill the auth fields matching Developer Portal; user enters secrets directly | Auth type confirmed and saved without recording secrets | guided |")
    lines.append("| 3 | Control Hub | Confirm tools appear; enable only selected tools and save | Tool list visible, selected tools allowed, enabled tool names recorded | guided |")
    lines.append("| 4 | AI Agent Studio | Open existing agent, go to Configuration -> Actions, click + Add actions, choose Select available, search/check intended MCP actions, and add them | Add actions modal rows from MCP provider and agent Actions table entries | guided |")
    lines.append("| 4a | AI Agent Studio | Update agent instructions for tool-use conditions, orchestration, confirmations, and failure handling | Saved instruction/prompt contract | guided |")
    lines.append("| 5 | AI Agent Studio | Run direct and conversation tests | Execution state, latency, transaction ID, transcript | guided |")
    lines.append("")
    lines.append("## Security And Access")
    lines.append(f"- Access policy: {data.get('access_policy') or 'TBD'}")
    lines.append(f"- Test data: {data.get('test_data') or 'TBD'}")
    lines.append(f"- Production notes: {data.get('production_notes') or 'TBD'}")
    lines.append("- Pause before entering secrets, enabling production access, or exposing customer data.")
    lines.append("- Prefer least-privilege tool exposure.")
    lines.append("")
    lines.append("## Validation Plan")
    lines.append("- Confirm Developer Portal Agentic App registration details.")
    lines.append("- Confirm Control Hub provisioning, authentication, and org governance.")
    lines.append("- Confirm Authentication tab saved without recording secret values.")
    lines.append("- Confirm Tools tab lists MCP tools; if empty, troubleshoot auth/server setup.")
    lines.append("- Confirm selected tools are enabled and scoped correctly.")
    lines.append("- Confirm expected MCP rows appear in the Studio Add actions modal.")
    lines.append("- Confirm selected MCP actions appear in the agent Actions table.")
    lines.append("- Confirm Studio instructions tell the agent when to call each tool and how to orchestrate complex flows.")
    lines.append("- Run a safe sample call for each tool.")
    lines.append("- Run a conversation happy path and one failure path.")
    lines.append("- Record evidence for the final playbook.")
    lines.append("")
    lines.append("## Missing Information")
    lines.append(bullet_list(missing))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a Webex MCP build recipe from intake JSON.")
    parser.add_argument("intake", nargs="?", type=Path, help="Path to intake JSON")
    parser.add_argument("--example", action="store_true", help="Print an example intake JSON")
    args = parser.parse_args()

    if args.example:
        print(json.dumps(EXAMPLE, indent=2))
        return 0

    if not args.intake:
        parser.error("provide an intake JSON path or use --example")

    data = load_intake(args.intake)
    print(render(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
