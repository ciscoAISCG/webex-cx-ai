# Generic Order Tracking Agent Workflow Response Contract

This document defines an example response shape for the `get_order_details` fulfillment flow used by the generic order tracking AI agent.

The goal of this contract is to give clients a realistic blueprint they can reuse and adapt in their own Webex Connect workflows. The flow can return hard-coded, generated, or live backend data, but keeping the response shape stable helps the AI agent answer consistently.

## Purpose

The `get_order_details` action is intended to provide a single rich payload that can support questions such as:

- What is the status of my order?
- Where is my order?
- When will my order arrive?
- Is my order delayed?
- What was the latest tracking update?

Example lookup inputs are:

- `order_number`, collected from the user when needed
- `customer_id`, injected from trusted voice-flow or channel context

The fulfillment flow should validate that the supplied `customer_id` is authorized to access the supplied `order_number`. If the combination does not match, one useful pattern is to return the same generic not-found style response rather than revealing whether the order exists for another customer.

## Design guidance

- Keep top-level field names stable across success, not-found, and error outcomes.
- Require both `order_number` and trusted `customer_id` as the lookup inputs for the workflow.
- Return only realistic values that a real order or shipment platform could provide.
- Use booleans such as `order_found`, `is_delayed`, and `human_handover_recommended` to make interpretation easier.
- Include a backend-authored `customer_message` when you want the workflow to control the primary customer-facing summary.
- If a value is unavailable, prefer a blank string, `false`, `[]`, or an empty object field rather than changing the shape of the response.
- If the workflow wants the agent to encourage escalation, set `human_handover_recommended` to `true`.

## Example response shape

```json
{
  "customer_id": "CUST-445566",
  "order_found": true,
  "order_number": "ORD-102938",
  "order_status": "In Transit",
  "status_description": "Your order has shipped and is currently in transit.",
  "customer_message": "Your order is in transit and is expected to arrive on June 24.",
  "estimated_delivery_date": "2026-06-24",
  "estimated_delivery_window": "By end of day",
  "is_delayed": false,
  "delay_reason": "",
  "current_location": "Birmingham, UK",
  "fulfillment_progress": "Shipped",
  "fulfillment_method": "Home Delivery",
  "carrier_name": "DHL",
  "tracking_number": "DHL123456789",
  "delivery_address_summary": "London, UK",
  "order_items_summary": "2 items",
  "latest_event": {
    "timestamp": "2026-06-22T09:15:00Z",
    "status": "Arrived at sorting facility",
    "description": "The package arrived at the regional sorting facility.",
    "location": "Birmingham, UK"
  },
  "tracking_history": [
    {
      "timestamp": "2026-06-22T09:15:00Z",
      "status": "Arrived at sorting facility",
      "description": "The package arrived at the regional sorting facility.",
      "location": "Birmingham, UK"
    },
    {
      "timestamp": "2026-06-21T18:40:00Z",
      "status": "Departed facility",
      "description": "The package departed the distribution center.",
      "location": "Manchester, UK"
    }
  ],
  "exception_code": "",
  "exception_message": "",
  "human_handover_recommended": false
}
```

## Field reference

- `order_found`
  Indicates whether the order number matched a known order.

- `customer_id`
  The trusted customer identifier used to authorize access to the order. This should come from voice-flow or channel context, not from the user during the conversation.

- `order_number`
  The order number used for lookup.

- `order_status`
  The current high-level state, for example `Processing`, `Shipped`, `In Transit`, `Out for Delivery`, `Delivered`, `Delayed`, or `Exception`.

- `status_description`
  A short human-readable explanation of the current state.

- `customer_message`
  An optional backend-authored summary that the AI agent can use as the main explanation.

- `estimated_delivery_date`
  The current best-known delivery date in `YYYY-MM-DD` format.

- `estimated_delivery_window`
  An optional delivery window such as `By end of day` or `2 PM - 6 PM`.

- `is_delayed`
  Indicates whether the workflow considers the order delayed.

- `delay_reason`
  A human-readable explanation of the delay when known.

- `current_location`
  The most relevant current package or order location when available.

- `fulfillment_progress`
  A short internal-business-process state such as `Picking`, `Packed`, or `Shipped`.

- `fulfillment_method`
  A delivery or pickup method such as `Home Delivery`, `Store Pickup`, or `Locker Pickup`.

- `carrier_name`
  The shipping carrier name when relevant.

- `tracking_number`
  The shipment tracking number when available.

- `delivery_address_summary`
  A minimal location summary suitable for conversation. Avoid exposing full address details unless your design explicitly requires it.

- `order_items_summary`
  A short summary such as `2 items` or `1 item: Wireless Headset`.

- `latest_event`
  The most recent tracking event. This is especially useful for concise answers.

- `tracking_history`
  Optional list of earlier tracking events for follow-up questions.

- `exception_code`
  Optional machine-friendly error or exception code such as `ORDER_NOT_FOUND` or `CARRIER_TIMEOUT`.

- `exception_message`
  Optional human-readable explanation of the exception.

- `human_handover_recommended`
  Indicates whether the workflow recommends offering escalation to a human agent.

## Example not-found response

```json
{
  "customer_id": "CUST-445566",
  "order_found": false,
  "order_number": "ORD-102938",
  "order_status": "",
  "status_description": "",
  "customer_message": "I couldn't find an order with that number.",
  "estimated_delivery_date": "",
  "estimated_delivery_window": "",
  "is_delayed": false,
  "delay_reason": "",
  "current_location": "",
  "fulfillment_progress": "",
  "fulfillment_method": "",
  "carrier_name": "",
  "tracking_number": "",
  "delivery_address_summary": "",
  "order_items_summary": "",
  "latest_event": {
    "timestamp": "",
    "status": "",
    "description": "",
    "location": ""
  },
  "tracking_history": [],
  "exception_code": "ORDER_NOT_FOUND",
  "exception_message": "No order was found for that order number.",
  "human_handover_recommended": false
}
```

This same response pattern can also be used when the order exists but does not belong to the supplied `customer_id`.

## Example error response

```json
{
  "customer_id": "CUST-445566",
  "order_found": false,
  "order_number": "ORD-102938",
  "order_status": "",
  "status_description": "",
  "customer_message": "I’m sorry, I couldn’t retrieve your order details right now.",
  "estimated_delivery_date": "",
  "estimated_delivery_window": "",
  "is_delayed": false,
  "delay_reason": "",
  "current_location": "",
  "fulfillment_progress": "",
  "fulfillment_method": "",
  "carrier_name": "",
  "tracking_number": "",
  "delivery_address_summary": "",
  "order_items_summary": "",
  "latest_event": {
    "timestamp": "",
    "status": "",
    "description": "",
    "location": ""
  },
  "tracking_history": [],
  "exception_code": "LOOKUP_FAILED",
  "exception_message": "The workflow could not retrieve order details from the tracking system.",
  "human_handover_recommended": true
}
```

## Notes for playbook reuse

- This contract is intentionally richer than a minimal demo so clients can see how one action can support multiple user questions.
- The same pattern can be reused for shipment tracking, return tracking, store pickup readiness, and service-order status with small field changes.
- If a client already has a different response contract, the AI agent prompt should be updated to match their actual returned fields.
