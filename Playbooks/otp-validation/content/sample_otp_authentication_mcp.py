"""Demo credit-card voice-authentication MCP sample.

Sanitized sample source: no static API keys or credentials were present in the
provided file. This code is not production-ready: the phone tool accepts any
syntactically valid E.164 number, and the implementation does not send an OTP
to a registered device. See the playbook for the intended flow and current gaps.
"""

import hmac
import html
import secrets
import uuid
from typing import Annotated, Literal, NotRequired, TypedDict

import httpx
from botocore.exceptions import BotoCoreError
from mcp_app import mcp
from pydantic import Field

from services.playground_api import _request_json


class VerifyAccountPhoneResult(TypedDict):
    """Phone verification result; the verification ID is a UUID token."""

    status: Literal["verified", "no_match", "error"]
    verification_id: NotRequired[str]


class ValidateCredentialResult(TypedDict):
    """START Code or PIN validation outcome."""

    status: Literal["Verified", "NOT Verified", "error"]


def _verification_session_id(session_id: str) -> str:
    """Return the companion pane key used to retain the verification handle."""
    return f"{session_id}:verification"


async def _read_pane_value(session_id: str) -> str | None:
    """Read the expected value from the workspace-pane record."""
    result = await _request_json("GET", params={"sessionId": session_id})
    if not isinstance(result, dict):
        raise RuntimeError("Workspace-pane lookup returned an unexpected response.")
    value = result.get("value")
    if not isinstance(value, str) or not value.strip():
        return None
    return value.strip()


async def _read_pane_record(session_id: str) -> dict[str, object]:
    """Read a complete workspace-pane record for validation and update."""
    result = await _request_json("GET", params={"sessionId": session_id})
    if not isinstance(result, dict):
        raise RuntimeError("Workspace-pane lookup returned an unexpected response.")
    return result


async def _save_verification_reference(session_id: str, verification_id: str) -> None:
    """Retain the opaque handle in its own pane record for later checks."""
    await _request_json(
        "POST",
        payload={
            "sessionId": _verification_session_id(session_id),
            "kind": "text",
            "title": "Phone Verification Reference",
            "src": "MCP",
            "source": "MCP",
            "body": "A phone verification reference is active for this session.",
            "value": verification_id,
        },
    )


async def _save_phone_verification(
    session_id: str,
    account_phone: str,
    start_code: str,
    verification_id: str,
) -> None:
    """Show verification details in the user's pane and store the START Code as its value."""
    body = (
        "<div><h3>Phone Verification</h3>"
        "<strong>Verified:</strong> true<br>"
        f"<strong>Phone Number confirmed:</strong> {html.escape(account_phone)}<br>"
        f"<strong>START Code:</strong> {html.escape(start_code)}<br>"
        f"<strong>Verification ID:</strong> {html.escape(verification_id)}"
        "</div>"
    )
    await _request_json(
        "POST",
        payload={
            "sessionId": session_id,
            "kind": "html",
            "title": "Phone Verification",
            "src": "MCP",
            "source": "MCP",
            "body": body,
            "value": start_code,
        },
    )


async def _verification_reference_matches(session_id: str, verification_id: str) -> bool:
    """Confirm that the supplied handle belongs to this session."""
    if not verification_id.strip():
        return False
    saved_id = await _read_pane_value(_verification_session_id(session_id))
    return saved_id is not None and hmac.compare_digest(saved_id, verification_id.strip())


def _append_validation_result(
    body: str,
    status: str,
    *,
    pin_code: str | None = None,
) -> str:
    """Append a validation result inside the existing pane HTML container when possible."""
    result_html = f"<p><strong>{html.escape(status)}</strong></p>"
    if pin_code is not None:
        result_html += f"<p><strong>PIN Code:</strong> {html.escape(pin_code)}</p>"
    closing_div = body.lower().rfind("</div>")
    if closing_div >= 0:
        return f"{body[:closing_div]}{result_html}{body[closing_div:]}"
    return f"{body}{result_html}"


async def _save_validation_result(
    *,
    session_id: str,
    pane_record: dict[str, object],
    status: str,
    next_value: str,
    include_pin_in_body: bool = False,
) -> None:
    """Save the pane HTML with the result and the next expected code value."""
    body = pane_record.get("body")
    if not isinstance(body, str):
        raise RuntimeError("Workspace-pane record has no text body to update.")
    kind = pane_record.get("kind")
    title = pane_record.get("title")
    await _request_json(
        "POST",
        payload={
            "sessionId": session_id,
            "kind": kind if isinstance(kind, str) else "html",
            "title": title if isinstance(title, str) else "Phone Verification",
            "src": "MCP",
            "source": "MCP",
            "body": _append_validation_result(
                body,
                status,
                pin_code=(next_value if include_pin_in_body and status == "Verified" else None),
            ),
            "value": next_value,
        },
    )


@mcp.tool(
    name="verify_account_phone",
    description=(
        "For this demo, always mark the supplied E.164 account phone as verified and return "
        "a random UUID verification_id. Generate a five-digit START Code and save it to the "
        "session pane with HTML verification details; save the token for subsequent checks."
    ),
)
async def verify_account_phone(
    account_phone: Annotated[
        str,
        Field(
            description=(
                "The caller's account phone number normalized to E.164 format, "
                "for example +15551234567."
            ),
            pattern=r"^\+[1-9][0-9]{1,14}$",
        ),
    ],
    sessionId: Annotated[str, Field(description="Workspace-pane session ID for this verification.")],
) -> VerifyAccountPhoneResult:
    """Return a fresh successful verification result and retain its UUID for this session."""
    try:
        start_code = f"{secrets.randbelow(100_000):05d}"
        verification_id = str(uuid.uuid4())
        await _save_verification_reference(sessionId, verification_id)
        await _save_phone_verification(
            sessionId,
            account_phone,
            start_code,
            verification_id,
        )
        return {"status": "verified", "verification_id": verification_id}
    except (BotoCoreError, httpx.HTTPError, RuntimeError):
        return {"status": "error"}


async def _validate_code(
    *,
    session_id: str,
    verification_id: str,
    submitted_code: str,
    include_pin_in_body: bool = False,
) -> ValidateCredentialResult:
    """Compare a submitted code, append the result, and rotate the value on a match."""
    try:
        if not await _verification_reference_matches(session_id, verification_id):
            return {"status": "error"}

        pane_record = await _read_pane_record(session_id)
        expected_value = pane_record.get("value")
        if not isinstance(expected_value, str) or not expected_value:
            return {"status": "error"}

        is_valid = hmac.compare_digest(expected_value, submitted_code)
        status = "Verified" if is_valid else "NOT Verified"
        next_value = (
            f"{secrets.randbelow(100_000):05d}" if is_valid else expected_value
        )
        await _save_validation_result(
            session_id=session_id,
            pane_record=pane_record,
            status=status,
            next_value=next_value,
            include_pin_in_body=include_pin_in_body,
        )
        return {"status": status}
    except (BotoCoreError, httpx.HTTPError, RuntimeError):
        return {"status": "error"}


@mcp.tool(
    name="validate_start_code",
    description=(
        "Compare the caller's digit-only START Code with the workspace-pane value for "
        "sessionId. Save Verified or NOT Verified in the pane HTML; after a match, rotate "
        "the value to a new five-digit PIN. Requires the verification_id from phone check."
    ),
)
async def validate_start_code(
    verification_id: Annotated[
        str,
        Field(description="Short-lived reference returned by verify_account_phone."),
    ],
    start_code: Annotated[
        str,
        Field(
            description="The caller's START Code as digits only; preserved as a string.",
            pattern=r"^[0-9]+$",
        ),
    ],
    sessionId: Annotated[str, Field(description="Workspace-pane session ID for this verification.")],
) -> ValidateCredentialResult:
    """Validate the START Code against the pane value and save the result."""
    return await _validate_code(
        session_id=sessionId,
        verification_id=verification_id,
        submitted_code=start_code,
        include_pin_in_body=True,
    )


@mcp.tool(
    name="validate_pin_code",
    description=(
        "Compare the caller's digit-only PIN with the workspace-pane value for sessionId. "
        "Save Verified or NOT Verified in the pane HTML; after a match, rotate the value "
        "to a new five-digit PIN. Requires the verification_id from phone check."
    ),
)
async def validate_pin_code(
    verification_id: Annotated[
        str,
        Field(description="Short-lived reference returned by verify_account_phone."),
    ],
    pin_code: Annotated[
        str,
        Field(
            description="The caller's PIN Code as digits only; preserved as a string.",
            pattern=r"^[0-9]+$",
        ),
    ],
    sessionId: Annotated[str, Field(description="Workspace-pane session ID for this verification.")],
) -> ValidateCredentialResult:
    """Validate the PIN against the pane value and save the result."""
    return await _validate_code(
        session_id=sessionId,
        verification_id=verification_id,
        submitted_code=pin_code,
    )
