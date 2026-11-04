# Healthcare A2A Agent And Tool Configuration Reference

This reference describes the behavior and data contracts present in the three AI Agent Studio exports. It is intended for implementation review after import; the JSON exports remain the source of truth.

## Agent Responsibilities

### Healthcare Concierge

The Concierge agent:

- Collects patient ID, date of birth, and postal code.
- Calls `Authenticate_Patient` and continues only when `identityVerified` is `true`.
- Retains the returned `patientReference` for downstream actions.
- Sends referral, insurance, booking, rescheduling, and availability requests to Validation.
- Sends an authenticated cancellation directly to Scheduling.
- Uses human handoff after two failed authentication attempts, for unclear or unsupported requests, when the caller asks for a person, or when medical guidance is requested.

### Referral And Insurance Validation

The Validation agent:

- Requires `{{identityVerified}}` and `{{patientReference}}` from the voice flow.
- Collects exactly two caller-provided values: insurance member number and specialty.
- Calls `Validate_Referral_Insurance` with the trusted patient reference.
- Clears the caller only when:
  - `referralStatus` is `valid` or `not_required`;
  - `eligibilityStatus` is `eligible`;
  - `networkStatus` is `in_network`;
  - `priorAuthorizationRequired` is `false`; and
  - `validationReference` is present.
- Transfers a cleared booking or rescheduling request to Scheduling.
- Sends cancellation directly to Scheduling without running validation.

### Healthcare Scheduling

The Scheduling agent:

- Requires `{{identityVerified}}` and `{{patientReference}}`.
- Requires `{{validationReference}}` for every journey except cancellation.
- Uses `{{specialty}}` supplied by Validation for booking and rescheduling.
- Collects preferred location, date, and time for a new booking.
- Calls `Find_Appointment_Slots`, presents only returned options, and retains the selected slot reference.
- Confirms specialty, location, date, and time before calling `Manage_Appointment` with `operation` set to `book`.
- Uses demo-only spoken success responses for cancellation and rescheduling without calling a fulfillment tool.
- Transfers referral or insurance questions back to Validation.

## Transfer Payloads

### Concierge To Validation

```json
{
  "identityVerified": "true",
  "patientReference": "PATIENT-DEMO-10001"
}
```

### Concierge To Scheduling For Cancellation

```json
{
  "identityVerified": "true",
  "patientReference": "PATIENT-DEMO-10001"
}
```

### Validation To Scheduling

```json
{
  "identityVerified": "true",
  "patientReference": "PATIENT-DEMO-10001",
  "specialty": "Cardiology",
  "validationReference": "VALIDATION-10001"
}
```

### Scheduling To Validation

```json
{
  "identityVerified": "true",
  "patientReference": "PATIENT-DEMO-10001"
}
```

The voice flow passes these values to a receiving agent as event data. Inside the receiving agent's instructions and tools, values originating from the voice flow are referenced with bracket notation such as `{{patientReference}}`.

## Fulfillment Contracts

The playbook includes the corresponding Webex Connect workflow exports:

| Workflow export | Agent tool |
|---|---|
| [`98941.workflow`](../assets/98941.workflow) | `Authenticate_Patient` |
| [`99610.workflow`](../assets/99610.workflow) | `Validate_Referral_Insurance` |
| [`98942.workflow`](../assets/98942.workflow) | `Find_Appointment_Slots` |
| [`98943.workflow`](../assets/98943.workflow) | `Manage_Appointment` |

Import and publish these workflows before binding the AI Agent fulfillment tools. The numeric export filenames correspond to the source Webex Connect flow IDs; verify the imported workflow names when rebinding in the destination tenant.

### Authenticate Patient

Request:

```json
{
  "patientId": "DEMO-10001",
  "dateOfBirth": "1985-04-14",
  "postalCode": "27502"
}
```

Successful response:

```json
{
  "identityVerified": "true",
  "patientReference": "PATIENT-DEMO-10001"
}
```

Failed response:

```json
{
  "identityVerified": "false"
}
```

### Validate Referral And Insurance

Request:

```json
{
  "patientReference": "PATIENT-DEMO-10001",
  "insuranceMemberId": "MEMBER-123456",
  "specialty": "Cardiology"
}
```

Cleared response:

```json
{
  "referralStatus": "valid",
  "eligibilityStatus": "eligible",
  "networkStatus": "in_network",
  "priorAuthorizationRequired": "false",
  "validationReference": "VALIDATION-10001",
  "nextStep": "The patient is cleared to proceed with appointment scheduling."
}
```

Blocked example:

```json
{
  "referralStatus": "expired",
  "eligibilityStatus": "eligible",
  "networkStatus": "in_network",
  "priorAuthorizationRequired": "false",
  "validationReference": "VALIDATION-10002",
  "nextStep": "Ask the referring provider to submit a current referral before scheduling."
}
```

### Find Appointment Slots

Request:

```json
{
  "patientReference": "PATIENT-DEMO-10001",
  "specialty": "Cardiology",
  "location": "Apex",
  "preferredDate": "2026-11-02",
  "preferredTime": "10:00"
}
```

Available response:

```json
{
  "availabilityStatus": "available",
  "slotOptions": "SLOT-1001: Monday, November 2 at 10:00 AM Eastern at the Apex location with Dr. John Doe; SLOT-1002: Tuesday, November 3 at 2:30 PM Eastern at the Durham location with Dr. John Doe"
}
```

No-availability response:

```json
{
  "availabilityStatus": "none",
  "slotOptions": ""
}
```

The current export defines `slotOptions` as a string. If the backend returns a JSON array instead, update the tool output schema and agent instructions together.

### Manage Appointment

Booking request:

```json
{
  "operation": "book",
  "patientReference": "PATIENT-DEMO-10001",
  "selectedSlotReference": "SLOT-1001"
}
```

Confirmed response:

```json
{
  "operationStatus": "confirmed",
  "appointmentSummary": "Cardiology appointment on Monday, November 2 at 10:00 AM Eastern at the Apex location with Dr. John Doe.",
  "confirmationNumber": "DEMO-10001"
}
```

Failure response:

```json
{
  "operationStatus": "failed",
  "appointmentSummary": "",
  "confirmationNumber": ""
}
```

## Voice Flow Routing

The included voice flow uses this pattern:

1. Invoke the Concierge agent.
2. On `ESCALATE`, parse the agent's `MetaData`.
3. Read `$.escalation_trigger` into `escalationTrigger`.
4. Route `Transfer_To_Validation` to the Validation agent.
5. Route `Transfer_To_Scheduling` to the Scheduling agent.
6. Route the Case activity's default outcome to the human queue.
7. Disconnect when an agent returns `ENDED`.

The receiving-agent event data includes `agent_metadata.dynamic_welcome_message` set to `true`, allowing the receiving agent to continue the journey with context-aware messaging.

## Import-Time Review

| Item | Review required |
|---|---|
| AI Agent references | Rebind all three Virtual Agent V2 activities to the imported agents. |
| Fulfillment references | Rebind all Webex Connect flow IDs, service IDs, endpoints, and authentication settings. |
| Queue | Replace the imported queue reference with the target human-support queue. |
| Concierge transfer mapping | The edited export parses `identityVerified` and `patientReference` from both `Transfer_To_Validation` and `Transfer_To_Scheduling`; verify both paths after import. |
| Scheduling return mapping | Parse Scheduling's `Transfer_To_Validation` action, not `Transfer_To_Scheduling`. |
| Security | Mark `patientReference` secure where supported and verify that sensitive values are not exposed in logs or prompts. |
| Transcript and recording | Review transcript, recording, retention, and access settings under the healthcare organization's policy. |

## Current Demo Limits

- The included Webex Connect workflows retain source-environment references and must be imported, reviewed, and published in the destination tenant.
- Cancellation and rescheduling do not update a real scheduling backend.
- The voice flow contains tenant-bound AI Agent, queue, service, and flow references.
- The reference does not provide clinical guidance or replace approved emergency handling.
- Runtime behavior must be tested in the target tenant after every reference is rebound.

