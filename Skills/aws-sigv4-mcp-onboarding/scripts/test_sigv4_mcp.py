#!/usr/bin/env python3
"""Regression tests for public identifier validation and endpoint derivation."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("sigv4_mcp.py")
ARN = (
    "arn:aws:bedrock-agentcore:us-east-2:111122223333:"
    "runtime/example-runtime-abc123"
)
MATCHING_ENDPOINT = (
    "https://bedrock-agentcore.us-east-2.amazonaws.com/runtimes/"
    "arn%3Aaws%3Abedrock-agentcore%3Aus-east-2%3A111122223333%3A"
    "runtime%2Fexample-runtime-abc123/invocations"
)
MISMATCHED_ENDPOINT = MATCHING_ENDPOINT.replace("111122223333", "444455556666")


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        check=False,
        text=True,
    )


class SigV4McpTests(unittest.TestCase):
    def test_endpoint_derivation_requires_confirmation(self) -> None:
        result = run_script("endpoint-from-arn", "--runtime-arn", ARN)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--confirm-authoritative", result.stderr)

    def test_endpoint_derivation_matches_confirmed_arn(self) -> None:
        result = run_script(
            "endpoint-from-arn",
            "--runtime-arn",
            ARN,
            "--confirm-authoritative",
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), MATCHING_ENDPOINT)

    def test_mismatch_names_the_differing_account(self) -> None:
        result = run_script(
            "check",
            "--server-name",
            "customer-webex",
            "--endpoint",
            MISMATCHED_ENDPOINT,
            "--runtime-arn",
            ARN,
            "--region",
            "us-east-2",
            "--profile",
            "customer-mcp",
            "--offline",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn(
            "AWS account: supplied ARN uses 111122223333; "
            "endpoint uses 444455556666",
            result.stderr,
        )
        self.assertIn("do not repair the URL by guessing", result.stderr)

    def test_matching_identifiers_pass_offline_check(self) -> None:
        result = run_script(
            "check",
            "--server-name",
            "customer-webex",
            "--endpoint",
            MATCHING_ENDPOINT,
            "--runtime-arn",
            ARN,
            "--region",
            "us-east-2",
            "--profile",
            "customer-mcp",
            "--offline",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"status": "ok"', result.stdout)
        self.assertIn('"proxy": "mcp-proxy-for-aws@1.6.0"', result.stdout)


if __name__ == "__main__":
    unittest.main()
