import assert from "node:assert/strict";
import test from "node:test";

import {
  createSearchWindow,
  createCallingNumberLookup,
  formatWebexMessage,
  handler,
  isSupportedEventType,
  normalizeConsultDialedNumber,
  parseWebhook,
  selectConsultDestination,
  selectMidCallSummary,
  type TaskConsultingWebhook,
} from "../src/index.js";
import type { LambdaFunctionURLEvent } from "aws-lambda";

const webhook: TaskConsultingWebhook = {
  id: "event-1",
  type: "task:consulting",
  comciscoorgid: "org-1",
  data: {
    taskId: "interaction-1",
    destination: "+32470123456",
  },
};

test("parses a task-consulting webhook", () => {
  const parsed = parseWebhook(JSON.stringify(webhook));
  assert.deepEqual(parsed, webhook);
  assert.equal(parsed.comciscoorgid, "org-1");
});

test("allows only the task-consulting business trigger", () => {
  assert.equal(isSupportedEventType("task:consulting"), true);
  assert.equal(isSupportedEventType("task:conference-transferred"), false);
  assert.equal(isSupportedEventType("task:consult-done"), false);
  assert.equal(isSupportedEventType("task:created"), false);
});

test("creates a 24-hour Search API window ending at the current time", () => {
  assert.deepEqual(createSearchWindow(1_788_355_689_650, 1_788_355_700_000), {
    from: 1_788_269_289_650,
    to: 1_788_355_700_000,
  });
});

test("keeps the configured number of trailing digits as the extension", () => {
  assert.equal(normalizeConsultDialedNumber("011005", 4), "1005");
});

test("supports organizations with a different extension length", () => {
  assert.equal(normalizeConsultDialedNumber("01912345", 5), "12345");
});

test("preserves a digit-only PSTN number", () => {
  assert.equal(normalizeConsultDialedNumber("01234567890", 4), "01234567890");
});

test("preserves an international formatted PSTN number", () => {
  assert.equal(normalizeConsultDialedNumber("+15550100200", 4), "+15550100200");
});

test("selects a ConsultTransfer destination before other task legs", () => {
  assert.deepEqual(
    selectConsultDestination(
      [
        {
          id: "active-consult",
          createdTime: 200,
          isActive: true,
          status: "consulting",
          callLegType: "consult",
          nextDestination: { agent: { phoneNumber: "019999" } },
        },
        {
          id: "completed-transfer",
          createdTime: 100,
          isActive: false,
          status: "ConsultTransfer",
          callLegType: "main",
          nextDestination: { agent: { phoneNumber: "011005" } },
        },
      ],
      4,
    ),
    {
      dialedNumber: "011005",
      lookupNumber: "1005",
      taskLegId: "completed-transfer",
      status: "ConsultTransfer",
      callLegType: "main",
    },
  );
});

test("uses an active consult leg before ConsultTransfer is available", () => {
  assert.equal(
    selectConsultDestination(
      [
        {
          id: "main",
          createdTime: 100,
          isActive: true,
          status: "connected",
          callLegType: "main",
        },
        {
          id: "consult",
          createdTime: 200,
          isActive: true,
          status: "consulting",
          callLegType: "consult",
          nextDestination: { agent: { phoneNumber: "011005" } },
        },
      ],
      4,
    )?.lookupNumber,
    "1005",
  );
});

test("uses the extension filter for an exact four-digit destination", () => {
  const lookup = createCallingNumberLookup("org-1", "1005");
  assert.equal(lookup.queryParameter, "extension");
  assert.equal(lookup.query.get("orgId"), "org-1");
  assert.equal(lookup.query.get("extension"), "1005");
  assert.equal(lookup.query.get("phoneNumbers"), null);
});

test("uses the configured extension length for Calling lookup", () => {
  const lookup = createCallingNumberLookup("org-1", "12345", 5);
  assert.equal(lookup.queryParameter, "extension");
  assert.equal(lookup.query.get("extension"), "12345");
});

test("uses the phoneNumbers filter for a destination with at least 10 digits", () => {
  const lookup = createCallingNumberLookup("org-1", "+14155550100");
  assert.equal(lookup.queryParameter, "phoneNumbers");
  assert.equal(lookup.query.get("orgId"), "org-1");
  assert.equal(lookup.query.get("phoneNumbers"), "+14155550100");
  assert.equal(lookup.query.get("extension"), null);
});

test("rejects an ambiguous destination length", () => {
  assert.throws(
    () => createCallingNumberLookup("org-1", "123456"),
    /4-digit extension or a phone number containing at least 10 digits/,
  );
});

test("selects the last MID_CALL summary", () => {
  const selected = selectMidCallSummary({
    summaries: {
      MID_CALL: {
        first: { reasonForTransferOrConsult: "First" },
        second: { reasonForTransferOrConsult: "Second" },
      },
    },
  });
  assert.equal(selected?.reasonForTransferOrConsult, "Second");
});

test("formats a summary message", () => {
  const markdown = formatWebexMessage("interaction-1", {
    reasonForTransferOrConsult: "Customer needs billing help.",
    additionalContext: "Invoice 123 is disputed.",
    keyActionsTaken: "Identity verified.",
  });

  assert.match(markdown, /Customer needs billing help/);
  assert.match(markdown, /Invoice 123 is disputed/);
  assert.match(markdown, /Identity verified/);
  assert.match(markdown, /interaction-1/);
});

test("formats the no-summary fallback", () => {
  const markdown = formatWebexMessage("interaction-1", null);
  assert.match(markdown, /No mid-call summary was available/);
});

test("runs the complete dry-run handler flow with mocked Webex APIs", async () => {
  const originalFetch = globalThis.fetch;
  const originalConsoleLog = console.log;
  const originalEnvironment = { ...process.env };
  const requests: string[] = [];
  const structuredLogs: Record<string, unknown>[] = [];

  process.env.WXCC_API_BASE_URL = "https://api.wxcc-us1.cisco.com";
  process.env.WEBEX_ACCESS_TOKEN = "test-token";
  process.env.EXTENSION_LENGTH = "4";
  process.env.DRY_RUN = "true";
  process.env.LOG_WEBHOOK_BODY = "false";

  console.log = (...args: unknown[]) => {
    if (typeof args[0] !== "string") return;
    try {
      structuredLogs.push(JSON.parse(args[0]) as Record<string, unknown>);
    } catch {
      // This test only inspects structured JSON stage logs.
    }
  };

  globalThis.fetch = async (input) => {
    const url = String(input);
    requests.push(url);

    if (url.endsWith("/generated-summaries/search")) {
      return Response.json({
        summaries: {
          MID_CALL: {
            summary1: {
              reasonForTransferOrConsult: "Customer needs billing assistance.",
            },
          },
        },
      });
    }

    if (url.endsWith("/search")) {
      return Response.json({
        data: {
          taskLegDetails: {
            taskLegs: [
              {
                id: "interaction-1-call-leg",
                createdTime: 1_788_355_526_860,
                isActive: false,
                status: "ConsultTransfer",
                callLegType: "main",
                nextDestination: {
                  agent: { phoneNumber: "011005" },
                },
              },
            ],
          },
        },
      });
    }

    if (url.startsWith("https://webexapis.com/v1/telephony/config/numbers?")) {
      return Response.json({
        phoneNumbers: [
          {
            extension: "1005",
            owner: { id: "person-1", type: "PEOPLE" },
          },
        ],
      });
    }

    throw new Error(`Unexpected request: ${url}`);
  };

  const functionUrlEvent = {
    body: JSON.stringify(webhook),
    isBase64Encoded: false,
  } as LambdaFunctionURLEvent;

  try {
    const response = await handler(functionUrlEvent);
    assert.equal(typeof response, "object");
    if (typeof response !== "object") throw new Error("Expected an HTTP response object");
    assert.equal(response.statusCode, 200);
    assert.deepEqual(JSON.parse(response.body ?? "{}"), {
      accepted: true,
      dryRun: true,
      interactionId: "interaction-1",
      summaryAvailable: true,
      consultDestination: "1005",
      toPersonId: "person-1",
    });
    assert.equal(requests.length, 3);
    assert.equal(requests[1], "https://api.wxcc-us1.cisco.com/search");
    assert.match(requests[2], /extension=1005/);
    assert.ok(requests.every((url) => !url.endsWith("/v1/messages")));

    const summaryQueryLog = structuredLogs.find(
      (entry) => entry.stage === "summary.query",
    );
    assert.equal(summaryQueryLog?.interactionId, "interaction-1");

    const summaryLog = structuredLogs.find(
      (entry) => entry.stage === "summary.resolved",
    );
    assert.deepEqual(summaryLog?.midCallSummary, {
      reasonForTransferOrConsult: "Customer needs billing assistance.",
    });

    const destinationLog = structuredLogs.find(
      (entry) => entry.stage === "consult-destination.resolved",
    );
    assert.equal(destinationLog?.dialedNumber, "011005");
    assert.equal(destinationLog?.lookupNumber, "1005");
    assert.equal(destinationLog?.extensionLength, 4);
    assert.equal(destinationLog?.status, "ConsultTransfer");
  } finally {
    globalThis.fetch = originalFetch;
    console.log = originalConsoleLog;
    process.env = originalEnvironment;
  }
});
