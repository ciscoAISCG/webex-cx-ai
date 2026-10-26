"""Decode the bundled, obfuscated Webex AI engine guardrails for internal review."""

from __future__ import annotations

import argparse
import base64
from pathlib import Path


def decode_payload(engine: str) -> str:
    reference = Path(__file__).resolve().parents[1] / "references" / "engine-guardrails.obfuscated.txt"
    lines = reference.read_text(encoding="ascii").splitlines()
    section = f"webex_ai_{engine}:"
    in_section = False
    for line in lines:
        if line in {"webex_ai_pro_1:", "webex_ai_pro_2:"}:
            in_section = line == section
            continue
        if in_section and line.startswith("  payload: "):
            encoded = line.removeprefix("  payload: ")
            return base64.b64decode(encoded, validate=True).decode("utf-8")
    raise ValueError(f"No guardrail payload found for {engine}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("engine", choices=("pro_1", "pro_2"), help="Webex AI Pro engine")
    args = parser.parse_args()
    print(decode_payload(args.engine), end="")


if __name__ == "__main__":
    main()
