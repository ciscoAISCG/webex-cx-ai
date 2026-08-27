#!/usr/bin/env python3
"""Validate and configure AWS SigV4-protected MCP connections without handling secrets."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Sequence
from urllib.parse import quote, unquote, urlencode, urlparse


DEFAULT_PROXY_VERSION = "1.6.0"
DEFAULT_SERVICE = "bedrock-agentcore"
SERVER_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
RUNTIME_ARN_RE = re.compile(
    r"^arn:(?P<partition>aws(?:-us-gov|-cn)?):bedrock-agentcore:"
    r"(?P<region>[a-z0-9-]+):(?P<account>\d{12}):runtime/(?P<runtime>[^/]+)$"
)
RUNTIME_PATH_RE = re.compile(r"^/runtimes/(?P<encoded_arn>[^/]+)/invocations/?$")
GATEWAY_PATH_RE = re.compile(r"^/[^/]+(?:/mcp)?/?$")


class ConfigError(RuntimeError):
    """Safe, user-correctable configuration error."""


@dataclass(frozen=True)
class Connection:
    server_name: str
    endpoint: str
    runtime_arn: str | None
    region: str
    profile: str
    service: str
    proxy_version: str
    read_only: bool
    endpoint_kind: str
    endpoint_arn: str | None
    runtime_account: str | None


def _require_executable(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise ConfigError(f"Required executable not found on PATH: {name}")
    return path


def _run(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        list(command),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise ConfigError(f"Command failed: {shlex.join(command)}\n{detail}")
    return result


def _parse_runtime_arn(value: str, label: str) -> re.Match[str]:
    match = RUNTIME_ARN_RE.fullmatch(value)
    if not match:
        raise ConfigError(f"{label} is not a valid AgentCore Runtime ARN: {value}")
    return match


def _runtime_endpoint(runtime_arn: str, qualifier: str | None = None) -> str:
    match = _parse_runtime_arn(runtime_arn, "Runtime ARN")
    region = match.group("region")
    partition = match.group("partition")
    domain = "amazonaws.com.cn" if partition == "aws-cn" else "amazonaws.com"
    endpoint = (
        f"https://bedrock-agentcore.{region}.{domain}/runtimes/"
        f"{quote(runtime_arn, safe='')}/invocations"
    )
    if qualifier:
        endpoint = f"{endpoint}?{urlencode({'qualifier': qualifier})}"
    return endpoint


def _runtime_mismatch_detail(
    supplied_match: re.Match[str], endpoint_match: re.Match[str]
) -> str:
    labels = {
        "partition": "AWS partition",
        "region": "AWS region",
        "account": "AWS account",
        "runtime": "runtime ID",
    }
    differences = []
    for field, label in labels.items():
        supplied = supplied_match.group(field)
        endpoint = endpoint_match.group(field)
        if supplied != endpoint:
            differences.append(
                f"- {label}: supplied ARN uses {supplied}; endpoint uses {endpoint}"
            )
    return "\n".join(differences)


def _validate(args: argparse.Namespace) -> Connection:
    if not SERVER_NAME_RE.fullmatch(args.server_name):
        raise ConfigError(
            "Server name must start with a lowercase letter or digit and contain only "
            "lowercase letters, digits, underscores, or hyphens (maximum 64 characters)"
        )
    if not re.fullmatch(r"[a-z]{2}(?:-gov)?-[a-z]+-\d", args.region):
        raise ConfigError(f"Invalid AWS region: {args.region}")
    if not args.profile.strip() or any(char.isspace() for char in args.profile):
        raise ConfigError("AWS profile must be a non-empty name without whitespace")
    if not re.fullmatch(r"[a-z0-9-]+", args.service):
        raise ConfigError(f"Invalid AWS SigV4 service name: {args.service}")
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[a-zA-Z0-9.+-]*)?", args.proxy_version):
        raise ConfigError(f"Invalid proxy version: {args.proxy_version}")

    parsed = urlparse(args.endpoint)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ConfigError("Endpoint must be a complete HTTPS URL")
    if parsed.username or parsed.password or parsed.fragment:
        raise ConfigError("Endpoint must not contain credentials or a URL fragment")

    expected_host = f"bedrock-agentcore.{args.region}.amazonaws.com"
    gateway_suffix = f".gateway.bedrock-agentcore.{args.region}.amazonaws.com"
    endpoint_kind: str
    endpoint_arn: str | None = None
    runtime_account: str | None = None

    if parsed.hostname == expected_host:
        path_match = RUNTIME_PATH_RE.fullmatch(parsed.path)
        if not path_match:
            raise ConfigError(
                "AgentCore Runtime endpoint path must be "
                "/runtimes/<URL-encoded-runtime-ARN>/invocations"
            )
        endpoint_kind = "agentcore-runtime"
        endpoint_arn = unquote(path_match.group("encoded_arn"))
        endpoint_match = _parse_runtime_arn(endpoint_arn, "ARN encoded in endpoint")
        if endpoint_match.group("region") != args.region:
            raise ConfigError(
                "Region mismatch: endpoint ARN uses "
                f"{endpoint_match.group('region')} but --region is {args.region}"
            )
        runtime_account = endpoint_match.group("account")
    elif parsed.hostname.endswith(gateway_suffix):
        if not GATEWAY_PATH_RE.fullmatch(parsed.path):
            raise ConfigError("AgentCore Gateway endpoint path is not recognized")
        endpoint_kind = "agentcore-gateway"
    else:
        raise ConfigError(
            f"Endpoint host {parsed.hostname} does not match AgentCore region {args.region}"
        )

    if args.runtime_arn:
        supplied_match = _parse_runtime_arn(args.runtime_arn, "Supplied runtime ARN")
        if supplied_match.group("region") != args.region:
            raise ConfigError(
                "Region mismatch: supplied runtime ARN uses "
                f"{supplied_match.group('region')} but --region is {args.region}"
            )
        if endpoint_kind != "agentcore-runtime":
            raise ConfigError("--runtime-arn is only valid with an AgentCore Runtime endpoint")
        if endpoint_arn != args.runtime_arn:
            detail = _runtime_mismatch_detail(supplied_match, endpoint_match)
            raise ConfigError(
                "Runtime mismatch: supplied ARN does not exactly match the ARN encoded "
                f"in the endpoint\n{detail}\n"
                "Stop and ask the AWS owner which complete runtime ARN is authoritative. "
                "After confirmation, use endpoint-from-arn --confirm-authoritative; "
                "do not repair the URL by guessing."
            )
        runtime_account = supplied_match.group("account")
    elif endpoint_kind == "agentcore-runtime":
        raise ConfigError(
            "Provide --runtime-arn so the public runtime identity can be cross-checked"
        )

    return Connection(
        server_name=args.server_name,
        endpoint=args.endpoint,
        runtime_arn=args.runtime_arn,
        region=args.region,
        profile=args.profile,
        service=args.service,
        proxy_version=args.proxy_version,
        read_only=args.read_only,
        endpoint_kind=endpoint_kind,
        endpoint_arn=endpoint_arn,
        runtime_account=runtime_account,
    )


def _proxy_args(connection: Connection) -> list[str]:
    args = [
        f"mcp-proxy-for-aws@{connection.proxy_version}",
        connection.endpoint,
        "--service",
        connection.service,
        "--profile",
        connection.profile,
        "--region",
        connection.region,
    ]
    if connection.read_only:
        args.append("--read-only")
    return args


def _codex_add_command(connection: Connection) -> list[str]:
    return [
        "codex",
        "mcp",
        "add",
        connection.server_name,
        "--",
        "uvx",
        *_proxy_args(connection),
    ]


def _generic_json(connection: Connection) -> dict[str, object]:
    return {
        "mcpServers": {
            connection.server_name: {
                "command": "uvx",
                "args": _proxy_args(connection),
            }
        }
    }


def _identity(connection: Connection) -> dict[str, str]:
    _require_executable("aws")
    result = _run(
        [
            "aws",
            "sts",
            "get-caller-identity",
            "--profile",
            connection.profile,
            "--region",
            connection.region,
            "--output",
            "json",
        ]
    )
    try:
        payload = json.loads(result.stdout)
        return {
            "account": str(payload["Account"]),
            "arn": str(payload["Arn"]),
            "user_id": str(payload["UserId"]),
        }
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ConfigError("AWS CLI returned an invalid caller identity response") from exc


def _summary(connection: Connection, identity: dict[str, str] | None) -> dict[str, object]:
    result: dict[str, object] = {
        "status": "ok",
        "server_name": connection.server_name,
        "endpoint_kind": connection.endpoint_kind,
        "endpoint": connection.endpoint,
        "runtime_arn": connection.endpoint_arn,
        "runtime_account": connection.runtime_account,
        "region": connection.region,
        "profile": connection.profile,
        "service": connection.service,
        "proxy": f"mcp-proxy-for-aws@{connection.proxy_version}",
        "read_only_filter": connection.read_only,
    }
    if identity:
        result["caller_identity"] = identity
        result["cross_account"] = (
            bool(connection.runtime_account)
            and identity["account"] != connection.runtime_account
        )
    return result


def command_check(args: argparse.Namespace) -> int:
    connection = _validate(args)
    _require_executable("uvx")
    identity = None if args.offline else _identity(connection)
    print(json.dumps(_summary(connection, identity), indent=2, sort_keys=True))
    return 0


def command_render(args: argparse.Namespace) -> int:
    connection = _validate(args)
    if args.client == "codex":
        print(shlex.join(_codex_add_command(connection)))
    else:
        print(json.dumps(_generic_json(connection), indent=2))
    return 0


def command_endpoint_from_arn(args: argparse.Namespace) -> int:
    if not args.confirm_authoritative:
        raise ConfigError(
            "Refusing to derive an endpoint until the AWS owner confirms the runtime "
            "ARN is authoritative. Re-run with --confirm-authoritative after confirmation."
        )
    print(_runtime_endpoint(args.runtime_arn, args.qualifier))
    return 0


def _configured_server_names() -> set[str]:
    result = _run(["codex", "mcp", "list"])
    names: set[str] = set()
    for line in result.stdout.splitlines():
        fields = line.split()
        if fields and fields[0].lower() not in {"name", "no"}:
            names.add(fields[0])
    return names


def command_install_codex(args: argparse.Namespace) -> int:
    connection = _validate(args)
    _require_executable("codex")
    _require_executable("uvx")
    identity = _identity(connection)

    if connection.server_name in _configured_server_names():
        raise ConfigError(
            f"Codex MCP server already exists: {connection.server_name}. "
            "Refusing to replace it."
        )

    command = _codex_add_command(connection)
    if args.dry_run:
        print(shlex.join(command))
        return 0

    _run(command)
    if connection.server_name not in _configured_server_names():
        raise ConfigError("Codex registration command succeeded but verification failed")

    print(
        json.dumps(
            {
                **_summary(connection, identity),
                "registration": "installed",
                "next_step": "Fully restart Codex and validate tools/list in a new task.",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _add_connection_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--server-name",
        required=True,
        help=(
            "Local MCP client label chosen by the operator, such as customer-webex; "
            "this is not a customer-provided AWS value"
        ),
    )
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--runtime-arn")
    parser.add_argument("--region", required=True)
    parser.add_argument(
        "--profile",
        required=True,
        help="Local AWS CLI profile name chosen or already configured on this workstation",
    )
    parser.add_argument("--service", default=DEFAULT_SERVICE)
    parser.add_argument("--proxy-version", default=DEFAULT_PROXY_VERSION)
    parser.add_argument("--read-only", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="Validate identifiers and AWS identity")
    _add_connection_arguments(check)
    check.add_argument(
        "--offline",
        action="store_true",
        help="Skip AWS identity resolution while still validating endpoint and ARN",
    )
    check.set_defaults(handler=command_check)

    render = subparsers.add_parser("render", help="Render client configuration")
    _add_connection_arguments(render)
    render.add_argument("--client", choices=("codex", "json"), required=True)
    render.set_defaults(handler=command_render)

    endpoint = subparsers.add_parser(
        "endpoint-from-arn",
        help="Derive an AgentCore invocation endpoint from an owner-confirmed runtime ARN",
    )
    endpoint.add_argument("--runtime-arn", required=True)
    endpoint.add_argument("--qualifier")
    endpoint.add_argument(
        "--confirm-authoritative",
        action="store_true",
        help="Confirm the AWS owner identified this complete runtime ARN as authoritative",
    )
    endpoint.set_defaults(handler=command_endpoint_from_arn)

    install = subparsers.add_parser(
        "install-codex",
        help="Validate identity and add a new Codex MCP registration",
    )
    _add_connection_arguments(install)
    install.add_argument("--dry-run", action="store_true")
    install.set_defaults(handler=command_install_codex)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.handler(args))
    except ConfigError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("ERROR: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
