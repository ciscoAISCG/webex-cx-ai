#!/usr/bin/env python3
"""Inspect Webex AI Agent Studio and Flow Designer playbook exports."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


SENSITIVE_RE = re.compile(
    r"(cvv|card|pan|expiry|expire|dob|birth|ssn|token|secret|password|auth|api[_-]?key|patient|account)",
    re.IGNORECASE,
)
DEMO_URL_RE = re.compile(r"(execute-api|example\.com|localhost|mock|demo)", re.IGNORECASE)
HTTP_REF_RE = re.compile(r"{{\s*([A-Za-z_][A-Za-z0-9_]*)\.httpStatusCode")


def load_json_files(paths: list[Path]) -> tuple[list[dict[str, Any]], list[str]]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.glob("*.json")))
        elif path.suffix.lower() == ".json":
            files.append(path)

    loaded: list[dict[str, Any]] = []
    errors: list[str] = []
    for file_path in files:
        try:
            with file_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            loaded.append({"path": str(file_path), "name": file_path.name, "data": data})
        except Exception as exc:  # noqa: BLE001 - report all bad artifacts cleanly.
            errors.append(f"{file_path}: {exc}")
    return loaded, errors


def classify_export(data: dict[str, Any]) -> str:
    if {"bot_type", "configuration", "tools"}.issubset(data.keys()):
        return "ai_agent"
    if data.get("flowType") in {"FLOW", "SUBFLOW"}:
        return "flow_designer"
    return "unknown"


def variable_name(variable: dict[str, Any]) -> str:
    return str(variable.get("name") or variable.get("id") or "")


def is_secure(variable: dict[str, Any]) -> bool:
    return bool(variable.get("secure") or variable.get("isSecure"))


def activity_entries(flow: dict[str, Any]) -> list[dict[str, Any]]:
    activities = flow.get("process", {}).get("activities", {})
    if not isinstance(activities, dict):
        return []

    entries = []
    for activity_id, activity in activities.items():
        props = activity.get("properties", {}) if isinstance(activity, dict) else {}
        entries.append(
            {
                "id": activity_id,
                "name": activity.get("name"),
                "group": activity.get("group"),
                "activityId": props.get("activityId"),
                "properties": props,
            }
        )
    return entries


def summarize_agent(item: dict[str, Any]) -> dict[str, Any]:
    data = item["data"]
    config = data.get("configuration", {})
    tools = []
    warnings: list[str] = []
    custom_event_names: list[str] = []

    for tool in data.get("tools", []) or []:
        name = str(tool.get("name", ""))
        input_entities = tool.get("input_entities", {})
        input_params = (
            input_entities.get("parameters", {})
            if isinstance(input_entities, dict)
            else {}
        )
        input_props = input_params.get("properties", {}) if isinstance(input_params, dict) else {}
        input_secure = set(input_params.get("secure", []) or []) if isinstance(input_params, dict) else set()
        fulfillment = tool.get("fulfillment", {}) if isinstance(tool.get("fulfillment"), dict) else {}
        fulfillment_type = fulfillment.get("type")
        if fulfillment_type == "custom_event":
            custom_event_names.append(name)

        sensitive_unsecured = [
            field
            for field in input_props.keys()
            if SENSITIVE_RE.search(str(field)) and field not in input_secure
        ]
        if sensitive_unsecured:
            warnings.append(
                f"{item['name']}: tool '{name}' has sensitive inputs not marked secure: "
                + ", ".join(sorted(sensitive_unsecured))
            )

        auth = fulfillment.get("authentication", {})
        tools.append(
            {
                "name": name,
                "enabled": tool.get("enabled"),
                "system_tool": tool.get("system_tool"),
                "capability": tool.get("capability"),
                "fulfillment_type": fulfillment_type,
                "auth_type": auth.get("type") if isinstance(auth, dict) else None,
                "required_inputs": input_params.get("required", []) if isinstance(input_params, dict) else [],
                "secure_inputs": sorted(input_secure),
                "input_fields": sorted(input_props.keys()),
            }
        )

    return {
        "file": item["name"],
        "path": item["path"],
        "bot_type": data.get("bot_type"),
        "language": config.get("default_language"),
        "timezone": config.get("timezone"),
        "model": config.get("llm_model"),
        "ai_engine": config.get("ai_engine"),
        "tool_count": len(tools),
        "custom_event_names": custom_event_names,
        "tools": tools,
        "warnings": warnings,
    }


def summarize_flow(item: dict[str, Any]) -> dict[str, Any]:
    data = item["data"]
    activities = activity_entries(data)
    activity_names = {str(activity["name"]) for activity in activities if activity.get("name")}
    warnings: list[str] = []

    variables = []
    for variable in data.get("variables", []) or []:
        name = variable_name(variable)
        secure = is_secure(variable)
        if name and SENSITIVE_RE.search(name) and not secure:
            warnings.append(f"{item['name']}: sensitive variable '{name}' is not marked secure")
        variables.append(
            {
                "name": name,
                "type": variable.get("type"),
                "source": variable.get("source"),
                "secure": secure,
            }
        )

    http_requests = []
    for activity in activities:
        props = activity["properties"]
        url = props.get("httpRequestUrl")
        if props.get("activityId") == "http-request-v2" or url:
            if url and DEMO_URL_RE.search(str(url)):
                warnings.append(f"{item['name']}: HTTP activity '{activity['name']}' uses demo-looking URL {url}")
            if props.get("authenticated") is False:
                warnings.append(f"{item['name']}: HTTP activity '{activity['name']}' has authentication disabled")
            http_requests.append(
                {
                    "name": activity["name"],
                    "method": props.get("httpRequestMethod"),
                    "url": url,
                    "authenticated": props.get("authenticated"),
                    "retryAttempts": props.get("retryAttempts"),
                    "timeout": props.get("httpResponseTimeout"),
                    "outputs": props.get("outputVariableArray") or [],
                }
            )

    case_statements = []
    state_event_names: list[str] = []
    for activity in activities:
        props = activity["properties"]
        if props.get("activityId") == "case-statement":
            menu_inputs = props.get("menuLinks_input") or props.get("menuLinks:input") or []
            state_event_names.extend([str(value) for value in menu_inputs])
            case_statements.append(
                {
                    "name": activity["name"],
                    "expression": props.get("expression"),
                    "values": menu_inputs,
                }
            )

    subflow_handoffs = []
    for activity in activities:
        props = activity["properties"]
        if props.get("activityId") == "subflow-handoff":
            subflow_handoffs.append(
                {
                    "name": activity["name"],
                    "subflowName": props.get("subflowName"),
                    "subflowId": props.get("subflowId"),
                    "inputs": props.get("subflowInputVariables") or [],
                    "outputs": props.get("subflowOutputVariables") or [],
                }
            )

    ai_agent_activities = []
    for activity in activities:
        props = activity["properties"]
        agent_ref = (
            props.get("aiAgentId")
            or props.get("agentId")
            or props.get("virtualAgentId")
            or props.get("botId")
            or props.get("botName")
        )
        activity_name = str(activity["name"]).lower()
        if agent_ref or activity_name.startswith("ai_") or "ai_agent" in activity_name:
            ai_agent_activities.append(
                {
                    "name": activity["name"],
                    "activityId": props.get("activityId"),
                    "agent_ref": agent_ref,
                }
            )

    for activity in activities:
        expression = str(activity["properties"].get("expression") or "")
        for match in HTTP_REF_RE.finditer(expression):
            ref = match.group(1)
            if ref not in activity_names:
                warnings.append(
                    f"{item['name']}: condition '{activity['name']}' references "
                    f"'{ref}.httpStatusCode', but no activity named '{ref}' was found"
                )

    sensitive_unsecured = [
        variable["name"]
        for variable in variables
        if variable["name"] and SENSITIVE_RE.search(variable["name"]) and not variable["secure"]
    ]

    return {
        "file": item["name"],
        "path": item["path"],
        "name": data.get("name"),
        "flowType": data.get("flowType"),
        "activity_count": len(activities),
        "activity_groups": dict(Counter(str(activity.get("group")) for activity in activities)),
        "variables": variables,
        "sensitive_variables_not_secure": sensitive_unsecured,
        "http_requests": http_requests,
        "case_statements": case_statements,
        "state_event_names": state_event_names,
        "subflow_handoffs": subflow_handoffs,
        "ai_agent_activities": ai_agent_activities,
        "warnings": warnings,
    }


def inspect(paths: list[Path]) -> dict[str, Any]:
    loaded, errors = load_json_files(paths)
    agents = []
    flows = []
    unknown = []
    warnings = list(errors)

    for item in loaded:
        kind = classify_export(item["data"])
        if kind == "ai_agent":
            summary = summarize_agent(item)
            agents.append(summary)
            warnings.extend(summary["warnings"])
        elif kind == "flow_designer":
            summary = summarize_flow(item)
            flows.append(summary)
            warnings.extend(summary["warnings"])
        else:
            unknown.append({"file": item["name"], "path": item["path"]})

    studio_events = sorted({event for agent in agents for event in agent["custom_event_names"]})
    flow_events = sorted({event for flow in flows for event in flow["state_event_names"]})
    missing_in_flows = sorted(set(studio_events) - set(flow_events))
    missing_in_studio = sorted(set(flow_events) - set(studio_events))

    for event in missing_in_flows:
        warnings.append(f"Studio custom event '{event}' has no matching Flow Designer case value")
    for event in missing_in_studio:
        warnings.append(f"Flow Designer case value '{event}' has no matching Studio custom event tool")

    return {
        "input_paths": [str(path) for path in paths],
        "files_seen": [item["name"] for item in loaded],
        "agents": agents,
        "flows": flows,
        "unknown_json": unknown,
        "cross_checks": {
            "studio_custom_events": studio_events,
            "flow_state_events": flow_events,
            "missing_in_flows": missing_in_flows,
            "missing_in_studio": missing_in_studio,
        },
        "warnings": warnings,
    }


def md_list(items: list[Any]) -> str:
    if not items:
        return "- None"
    return "\n".join(f"- {item}" for item in items)


def render_markdown(summary: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Webex Playbook Inspection")
    lines.append("")
    lines.append("## Files")
    lines.append(md_list(summary["files_seen"]))
    if summary["unknown_json"]:
        lines.append("")
        lines.append("Unknown JSON files:")
        lines.append(md_list([item["file"] for item in summary["unknown_json"]]))

    lines.append("")
    lines.append("## AI Agent Studio Exports")
    if not summary["agents"]:
        lines.append("- None")
    for agent in summary["agents"]:
        lines.append(f"### {agent['file']}")
        lines.append(f"- Language: {agent.get('language')}")
        lines.append(f"- Timezone: {agent.get('timezone')}")
        lines.append(f"- Model: {agent.get('model')}")
        lines.append(f"- Tools: {agent.get('tool_count')}")
        for tool in agent["tools"]:
            lines.append(
                f"  - {tool['name']}: {tool['capability']}, "
                f"fulfillment={tool['fulfillment_type']}, required={tool['required_inputs']}, "
                f"secure={tool['secure_inputs']}"
            )

    lines.append("")
    lines.append("## Flow Designer Exports")
    if not summary["flows"]:
        lines.append("- None")
    for flow in summary["flows"]:
        lines.append(f"### {flow['file']} ({flow.get('flowType')})")
        lines.append(f"- Flow name: {flow.get('name')}")
        lines.append(f"- Activities: {flow.get('activity_count')}")
        lines.append(f"- Activity groups: {flow.get('activity_groups')}")
        if flow["ai_agent_activities"]:
            lines.append("- AI agent activities:")
            for activity in flow["ai_agent_activities"]:
                lines.append(f"  - {activity['name']}: agent_ref={activity['agent_ref']}")
        if flow["case_statements"]:
            lines.append("- Event routers:")
            for case in flow["case_statements"]:
                lines.append(f"  - {case['name']}: {case['expression']} -> {case['values']}")
        if flow["subflow_handoffs"]:
            lines.append("- Subflow handoffs:")
            for handoff in flow["subflow_handoffs"]:
                lines.append(f"  - {handoff['name']} -> {handoff['subflowName']} ({handoff['subflowId']})")
        if flow["http_requests"]:
            lines.append("- HTTP requests:")
            for request in flow["http_requests"]:
                lines.append(
                    f"  - {request['name']}: {request['method']} {request['url']} "
                    f"auth={request['authenticated']}"
                )
        if flow["sensitive_variables_not_secure"]:
            lines.append("- Sensitive variables not marked secure:")
            for name in flow["sensitive_variables_not_secure"]:
                lines.append(f"  - {name}")

    lines.append("")
    lines.append("## Cross-Checks")
    checks = summary["cross_checks"]
    lines.append(f"- Studio custom events: {checks['studio_custom_events']}")
    lines.append(f"- Flow state events: {checks['flow_state_events']}")
    lines.append(f"- Missing in flows: {checks['missing_in_flows']}")
    lines.append(f"- Missing in Studio: {checks['missing_in_studio']}")

    lines.append("")
    lines.append("## Warnings")
    lines.append(md_list(summary["warnings"]))

    lines.append("")
    lines.append("## Build Recipe Seeds")
    lines.append("- Import Studio agents, Flow Designer subflows, then main flows.")
    lines.append("- Rebind tenant-specific agent, subflow, queue, endpoint, auth, and MCP references.")
    lines.append("- Replace demo endpoints and enable authentication before production testing.")
    lines.append("- Mark sensitive Studio tool inputs and Flow Designer variables secure where supported.")
    lines.append("- Run happy-path, fulfillment-failure, user-handoff, and out-of-scope tests.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect Webex AI Agent playbook exports.")
    parser.add_argument("paths", nargs="+", type=Path, help="Playbook folder or JSON export paths")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    summary = inspect(args.paths)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(render_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
