import type {
  LambdaFunctionURLEvent,
  LambdaFunctionURLResult,
} from "aws-lambda";

// =============================================================================
// SECTION 1: Types
// Responsibility: Describe the webhook and Webex API data used by this POC.
// =============================================================================

export interface TaskConsultingWebhook {
  id: string;
  specversion?: string;
  type: string;
  source?: string;
  comciscoorgid?: string;
  datacontenttype?: string;
  data?: {
    taskId?: string;
    origin?: string;
    destination?: string;
    direction?: string;
    channelType?: string;
    outboundType?: string | null;
    queueId?: string;
    createdTime?: number;
    [key: string]: unknown;
  };
  [key: string]: unknown;
}

export const SUPPORTED_EVENT_TYPES = [
  "task:consulting",
] as const;

const supportedEventTypeSet = new Set<string>(SUPPORTED_EVENT_TYPES);

export interface MidCallSummary {
  reasonForTransferOrConsult?: string;
  additionalContext?: string;
  keyActionsTaken?: string;
  [key: string]: unknown;
}

interface SummarySearchResponse {
  summaries?: {
    MID_CALL?: Record<string, MidCallSummary>;
    [key: string]: unknown;
  };
}

interface SearchTaskLeg {
  id?: string;
  createdTime?: number;
  isActive?: boolean;
  status?: string;
  callLegType?: string;
  nextDestination?: {
    agent?: {
      phoneNumber?: string | null;
    };
  };
}

interface TaskLegSearchResponse {
  data?: {
    taskLegDetails?: {
      taskLegs?: SearchTaskLeg[];
    };
  };
}

export interface ConsultDestination {
  dialedNumber: string;
  lookupNumber: string;
  taskLegId?: string;
  status?: string;
  callLegType?: string;
}

interface CallingNumberOwner {
  id?: string;
  type?: string;
  firstName?: string;
  lastName?: string;
}

interface CallingNumberEntry {
  phoneNumber?: string;
  extension?: string;
  owner?: CallingNumberOwner;
}

interface CallingNumbersResponse {
  phoneNumbers?: CallingNumberEntry[];
  items?: CallingNumberEntry[];
}

export interface CallingNumberLookup {
  queryParameter: "extension" | "phoneNumbers";
  value: string;
  query: URLSearchParams;
}

interface MessageResponse {
  id: string;
}

interface AppConfig {
  wxccApiBaseUrl: string;
  webexAccessToken: string;
  fallbackOrgId?: string;
  extensionLength: number;
  dryRun: boolean;
  logWebhookBody: boolean;
}

// =============================================================================
// SECTION 2: Configuration
// Responsibility: Read and validate Lambda environment variables.
// =============================================================================

function requiredEnvironmentVariable(name: string): string {
  const value = process.env[name]?.trim();
  if (!value) throw new Error(`Missing required environment variable: ${name}`);
  return value;
}

function readBoolean(name: string, defaultValue: boolean): boolean {
  const value = process.env[name]?.trim().toLowerCase();
  if (value === undefined || value === "") return defaultValue;
  if (value === "true") return true;
  if (value === "false") return false;
  throw new Error(`${name} must be either true or false`);
}

function readExtensionLength(name: string, defaultValue: number): number {
  const rawValue = process.env[name]?.trim();
  const value = rawValue ? Number(rawValue) : defaultValue;
  if (!Number.isInteger(value) || value < 1 || value > 9) {
    throw new Error(`${name} must be an integer between 1 and 9`);
  }
  return value;
}

export function loadConfig(): AppConfig {
  return {
    wxccApiBaseUrl: requiredEnvironmentVariable("WXCC_API_BASE_URL").replace(/\/$/, ""),
    webexAccessToken: requiredEnvironmentVariable("WEBEX_ACCESS_TOKEN"),
    fallbackOrgId: process.env.WEBEX_ORG_ID?.trim() || undefined,
    extensionLength: readExtensionLength("EXTENSION_LENGTH", 4),
    dryRun: readBoolean("DRY_RUN", true),
    logWebhookBody: readBoolean("LOG_WEBHOOK_BODY", true),
  };
}

// =============================================================================
// SECTION 3: Lambda entry point
// Responsibility: Coordinate the complete synchronous demo workflow.
// =============================================================================

export async function handler(
  event: LambdaFunctionURLEvent,
): Promise<LambdaFunctionURLResult> {
  try {
    const config = loadConfig();
    const rawBody = decodeFunctionUrlBody(event);

    if (config.logWebhookBody) {
      // POC requirement: log the complete incoming body. This may contain PII.
      console.log("[webhook-body]", rawBody);
    }

    const webhook = parseWebhook(rawBody);
    logStage("webhook.parsed", {
      eventId: webhook.id,
      eventType: webhook.type,
      orgId: webhook.comciscoorgid,
      taskId: webhook.data?.taskId,
    });

    if (!isSupportedEventType(webhook.type)) {
      logStage("webhook.ignored", { eventType: webhook.type });
      return jsonResponse(200, {
        accepted: false,
        reason: "Unsupported event type",
        supportedEventTypes: SUPPORTED_EVENT_TYPES,
      });
    }

    const interactionId = requireInteractionId(webhook);
    const orgId = requireOrganizationId(webhook, config);

    logStage("webhook.resolved", {
      eventId: webhook.id,
      interactionId,
      orgId,
      entryPointDnis: webhook.data?.destination,
    });

    const summary = await fetchMidCallSummary(config, orgId, interactionId);
    logStage("summary.resolved", {
      interactionId,
      summaryAvailable: summary !== null,
      midCallSummary: summary,
    });

    const consultDestination = await fetchConsultDestination(
      config,
      interactionId,
      webhook.data?.createdTime,
    );
    const owner = await resolveCallingUser(
      config,
      orgId,
      consultDestination.lookupNumber,
    );
    const markdown = formatWebexMessage(interactionId, summary);

    if (config.dryRun) {
      logStage("message.dry-run", {
        toPersonId: owner.id,
        ownerType: owner.type,
        consultDestination,
        markdown,
      });
      return jsonResponse(200, {
        accepted: true,
        dryRun: true,
        interactionId,
        summaryAvailable: summary !== null,
        consultDestination: consultDestination.lookupNumber,
        toPersonId: owner.id,
      });
    }

    const message = await sendWebexMessage(config, owner.id!, markdown);
    logStage("message.sent", {
      interactionId,
      consultDestination: consultDestination.lookupNumber,
      toPersonId: owner.id,
      messageId: message.id,
    });

    return jsonResponse(200, {
      accepted: true,
      dryRun: false,
      interactionId,
      summaryAvailable: summary !== null,
      consultDestination: consultDestination.lookupNumber,
      messageId: message.id,
    });
  } catch (error) {
    logStage("processing.failed", {
      error: error instanceof Error ? error.message : String(error),
    });
    return jsonResponse(500, {
      accepted: false,
      error: error instanceof Error ? error.message : "Unexpected error",
    });
  }
}

// =============================================================================
// SECTION 4: Webhook parsing and correlation
// Responsibility: Decode the Function URL request and extract task/org IDs.
// =============================================================================

export function decodeFunctionUrlBody(event: LambdaFunctionURLEvent): string {
  if (!event.body) throw new Error("Webhook request body is empty");
  return event.isBase64Encoded
    ? Buffer.from(event.body, "base64").toString("utf8")
    : event.body;
}

export function parseWebhook(rawBody: string): TaskConsultingWebhook {
  let parsed: unknown;
  try {
    parsed = JSON.parse(rawBody);
  } catch {
    throw new Error("Webhook body is not valid JSON");
  }

  if (!parsed || typeof parsed !== "object") {
    throw new Error("Webhook body must be a JSON object");
  }

  const webhook = parsed as TaskConsultingWebhook;
  if (!webhook.id || !webhook.type) {
    throw new Error("Webhook body must include id and type");
  }
  return webhook;
}

export function isSupportedEventType(eventType: string): boolean {
  return supportedEventTypeSet.has(eventType);
}

function requireInteractionId(webhook: TaskConsultingWebhook): string {
  const taskId = webhook.data?.taskId?.trim();
  if (!taskId) throw new Error("Webhook data.taskId is missing");
  return taskId;
}

function requireOrganizationId(
  webhook: TaskConsultingWebhook,
  config: AppConfig,
): string {
  const orgId = webhook.comciscoorgid?.trim() || config.fallbackOrgId;
  if (!orgId) {
    throw new Error("Webhook comciscoorgid and WEBEX_ORG_ID are both missing");
  }
  return orgId;
}

// =============================================================================
// SECTION 5: Consult-destination lookup
// Responsibility: Query call-leg data, select the consult-transfer target, and
// derive an internal extension using the configured extension length.
// =============================================================================

function createTaskLegSearchQuery(): string {
  return `
    query ConsultDestination($from: Long!, $to: Long!, $taskId: String!) {
      taskLegDetails(
        from: $from
        to: $to
        filter: { taskId: { equals: $taskId } }
      ) {
        taskLegs {
          id
          createdTime
          isActive
          status
          callLegType
          nextDestination {
            agent {
              phoneNumber
            }
          }
        }
      }
    }
  `;
}

export function createSearchWindow(
  webhookCreatedTime: number | undefined,
  now = Date.now(),
): { from: number; to: number } {
  const referenceTime =
    typeof webhookCreatedTime === "number" && Number.isFinite(webhookCreatedTime)
      ? Math.min(webhookCreatedTime, now)
      : now;
  return {
    from: referenceTime - 24 * 60 * 60 * 1_000,
    to: now,
  };
}

export function normalizeConsultDialedNumber(
  dialedNumber: string,
  extensionLength: number,
): string {
  const trimmed = dialedNumber.trim();
  if (
    !Number.isInteger(extensionLength) ||
    extensionLength < 1 ||
    extensionLength > 9
  ) {
    throw new Error("Extension length must be an integer between 1 and 9");
  }

  // Short digit-only values are internal dial strings. Keep the configured
  // number of trailing digits as the extension and treat preceding digits as
  // a dialing prefix. Preserve 10+ digit and formatted values as phone numbers.
  if (!/^\d+$/.test(trimmed) || trimmed.length >= 10) return trimmed;
  if (trimmed.length < extensionLength) return trimmed;
  return trimmed.slice(-extensionLength);
}

export function selectConsultDestination(
  taskLegs: SearchTaskLeg[],
  extensionLength: number,
): ConsultDestination | null {
  const candidates = taskLegs
    .map((taskLeg) => ({
      taskLeg,
      dialedNumber: taskLeg.nextDestination?.agent?.phoneNumber?.trim(),
    }))
    .filter(
      (candidate): candidate is { taskLeg: SearchTaskLeg; dialedNumber: string } =>
        Boolean(candidate.dialedNumber),
    )
    .sort((left, right) => {
      const rank = (taskLeg: SearchTaskLeg): number => {
        if (taskLeg.status === "ConsultTransfer") return 3;
        if (taskLeg.callLegType?.toLowerCase() === "consult" && taskLeg.isActive) {
          return 2;
        }
        if (taskLeg.callLegType?.toLowerCase() === "consult") return 1;
        return 0;
      };
      return (
        rank(right.taskLeg) - rank(left.taskLeg) ||
        (right.taskLeg.createdTime ?? 0) - (left.taskLeg.createdTime ?? 0)
      );
    });

  const selected = candidates[0];
  if (!selected) return null;
  return {
    dialedNumber: selected.dialedNumber,
    lookupNumber: normalizeConsultDialedNumber(
      selected.dialedNumber,
      extensionLength,
    ),
    taskLegId: selected.taskLeg.id,
    status: selected.taskLeg.status,
    callLegType: selected.taskLeg.callLegType,
  };
}

async function fetchConsultDestination(
  config: AppConfig,
  interactionId: string,
  webhookCreatedTime?: number,
): Promise<ConsultDestination> {
  const window = createSearchWindow(webhookCreatedTime);
  logStage("consult-destination.query", {
    interactionId,
    ...window,
  });

  const response = await requestJson<TaskLegSearchResponse>(
    `${config.wxccApiBaseUrl}/search`,
    {
      method: "POST",
      headers: authorizationHeaders(config.webexAccessToken),
      body: JSON.stringify({
        query: createTaskLegSearchQuery(),
        variables: {
          from: window.from,
          to: window.to,
          taskId: interactionId,
        },
      }),
    },
    "Consult destination Search API lookup",
  );

  const taskLegs = response.data?.taskLegDetails?.taskLegs ?? [];
  logStage("consult-destination.response", {
    interactionId,
    taskLegs,
  });

  const destination = selectConsultDestination(
    taskLegs,
    config.extensionLength,
  );
  if (!destination) {
    throw new Error(
      `Search API returned no consult destination for interaction ${interactionId}`,
    );
  }

  logStage("consult-destination.resolved", {
    interactionId,
    extensionLength: config.extensionLength,
    ...destination,
  });
  return destination;
}

// =============================================================================
// SECTION 6: MID_CALL summary lookup
// Responsibility: Retrieve and select the AI-generated mid-call summary.
// =============================================================================

async function fetchMidCallSummary(
  config: AppConfig,
  orgId: string,
  interactionId: string,
): Promise<MidCallSummary | null> {
  // Dedicated log entry for confirming the exact interaction queried.
  logStage("summary.query", { interactionId });

  const response = await requestJson<SummarySearchResponse>(
    `${config.wxccApiBaseUrl}/generated-summaries/search`,
    {
      method: "POST",
      headers: authorizationHeaders(config.webexAccessToken),
      body: JSON.stringify({
        searchType: "INTERACTION",
        orgId,
        interactionId,
      }),
    },
    "Agent Summaries lookup",
  );

  return selectMidCallSummary(response);
}

export function selectMidCallSummary(
  response: SummarySearchResponse,
): MidCallSummary | null {
  const summaries = Object.values(response.summaries?.MID_CALL ?? {});
  return summaries.length > 0 ? summaries[summaries.length - 1] : null;
}

// =============================================================================
// SECTION 7: Calling number owner lookup
// Responsibility: Choose extension/phone lookup and resolve a Webex person ID.
// =============================================================================

export function createCallingNumberLookup(
  orgId: string,
  destination: string,
  extensionLength = 4,
): CallingNumberLookup {
  if (
    !Number.isInteger(extensionLength) ||
    extensionLength < 1 ||
    extensionLength > 9
  ) {
    throw new Error("Extension length must be an integer between 1 and 9");
  }
  if (!/^[+\d\s().-]+$/.test(destination)) {
    throw new Error(`Transfer destination contains invalid characters: ${destination}`);
  }

  const digitCount = destination.replace(/\D/g, "").length;
  let queryParameter: CallingNumberLookup["queryParameter"];

  const extensionPattern = new RegExp(`^\\d{${extensionLength}}$`);
  if (extensionPattern.test(destination)) {
    queryParameter = "extension";
  } else if (digitCount >= 10) {
    queryParameter = "phoneNumbers";
  } else {
    throw new Error(
      `Transfer destination must be a ${extensionLength}-digit extension or a phone number containing at least 10 digits: ${destination}`,
    );
  }

  return {
    queryParameter,
    value: destination,
    query: new URLSearchParams({ orgId, [queryParameter]: destination }),
  };
}

async function resolveCallingUser(
  config: AppConfig,
  orgId: string,
  destination: string,
): Promise<CallingNumberOwner> {
  const lookup = createCallingNumberLookup(
    orgId,
    destination,
    config.extensionLength,
  );
  const response = await requestJson<CallingNumbersResponse>(
    `https://webexapis.com/v1/telephony/config/numbers?${lookup.query.toString()}`,
    {
      method: "GET",
      headers: authorizationHeaders(config.webexAccessToken, false),
    },
    "Calling Numbers lookup",
  );

  const entries = response.phoneNumbers ?? response.items ?? [];
  const matches = entries.filter((entry) =>
    lookup.queryParameter === "extension"
      ? entry.extension === lookup.value
      : entry.phoneNumber === lookup.value,
  );
  if (matches.length !== 1) {
    throw new Error(
      `Expected one Calling ${lookup.queryParameter} match for ${destination}; received ${matches.length}`,
    );
  }

  const owner = matches[0].owner;
  if (!owner?.id) {
    throw new Error(`Calling destination ${destination} has no owner ID`);
  }

  const ownerType = owner.type?.toUpperCase();
  if (ownerType && !["USER", "PEOPLE", "PERSON"].includes(ownerType)) {
    throw new Error(
      `Calling destination ${destination} belongs to unsupported owner type: ${owner.type}`,
    );
  }

  logStage("calling-owner.resolved", {
    destination,
    lookupType: lookup.queryParameter,
    ownerId: owner.id,
    ownerType: owner.type,
  });
  return owner;
}

// =============================================================================
// SECTION 8: Message formatting
// Responsibility: Build readable Markdown for summary and no-summary cases.
// =============================================================================

export function formatWebexMessage(
  interactionId: string,
  summary: MidCallSummary | null,
): string {
  if (!summary) {
    return [
      "### Call consultation",
      "",
      "No mid-call summary was available for this interaction.",
      "",
      `Interaction ID: \`${interactionId}\``,
    ].join("\n");
  }

  const sections: string[] = ["### Call consultation summary"];
  appendMarkdownSection(
    sections,
    "Reason for transfer",
    summary.reasonForTransferOrConsult,
  );
  appendMarkdownSection(sections, "Additional context", summary.additionalContext);
  appendMarkdownSection(sections, "Actions already taken", summary.keyActionsTaken);
  sections.push("", `Interaction ID: \`${interactionId}\``);
  return sections.join("\n");
}

function appendMarkdownSection(
  sections: string[],
  heading: string,
  value: unknown,
): void {
  if (typeof value !== "string" || !value.trim()) return;
  sections.push("", `**${heading}**`, value.trim());
}

// =============================================================================
// SECTION 9: Webex Messaging delivery
// Responsibility: Send the prepared Markdown to the resolved Webex user.
// =============================================================================

async function sendWebexMessage(
  config: AppConfig,
  toPersonId: string,
  markdown: string,
): Promise<MessageResponse> {
  return requestJson<MessageResponse>(
    "https://webexapis.com/v1/messages",
    {
      method: "POST",
      headers: authorizationHeaders(config.webexAccessToken),
      body: JSON.stringify({ toPersonId, markdown }),
    },
    "Webex message delivery",
  );
}

// =============================================================================
// SECTION 10: Shared HTTP, logging and response helpers
// Responsibility: Keep API behavior and structured logs consistent.
// =============================================================================

function authorizationHeaders(
  accessToken: string,
  includeContentType = true,
): Record<string, string> {
  return {
    Authorization: `Bearer ${accessToken}`,
    Accept: "application/json",
    ...(includeContentType ? { "Content-Type": "application/json" } : {}),
  };
}

async function requestJson<T>(
  url: string,
  init: RequestInit,
  operation: string,
): Promise<T> {
  const response = await fetch(url, {
    ...init,
    signal: AbortSignal.timeout(10_000),
  });
  const responseText = await response.text();

  if (!response.ok) {
    throw new Error(
      `${operation} failed with HTTP ${response.status}: ${responseText.slice(0, 500)}`,
    );
  }

  if (!responseText) return {} as T;
  try {
    return JSON.parse(responseText) as T;
  } catch {
    throw new Error(`${operation} returned invalid JSON`);
  }
}

function logStage(stage: string, details: Record<string, unknown>): void {
  console.log(
    JSON.stringify({
      timestamp: new Date().toISOString(),
      stage,
      ...details,
    }),
  );
}

function jsonResponse(statusCode: number, body: unknown): LambdaFunctionURLResult {
  return {
    statusCode,
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  };
}
