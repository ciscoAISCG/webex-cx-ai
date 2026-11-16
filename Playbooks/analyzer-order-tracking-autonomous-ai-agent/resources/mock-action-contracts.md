# Mock Action Contracts

These contracts describe the three fulfillment actions used by `Analyzer_Order_Tracking`. The generated agent JSON contains Webex Connect placeholders; create one mock fulfillment flow per action and return the documented response fields.

## `Verify_Customer`

Use this action before either order action.

### Request

```json
{
  "customerID": "CUST10001",
  "zipCode": "27502"
}
```

### Successful response

```json
{
  "verificationStatus": "verified",
  "customerReference": "CUSTOMER-REF-10001",
  "customerName": "Jordan Lee",
  "customerMessage": "Your identity has been verified."
}
```

### Unsuccessful response

```json
{
  "verificationStatus": "not_verified",
  "customerMessage": "We could not verify the information provided."
}
```

Return the same generic unsuccessful response for a wrong customer ID, wrong ZIP code, or unknown customer. Do not identify which value failed.

## `Get_Order_Status`

The fulfillment layer must confirm that `orderID` belongs to `customerReference`.

### Request

```json
{
  "customerReference": "CUSTOMER-REF-10001",
  "orderID": "12345"
}
```

### Successful response

```json
{
  "orderFound": "true",
  "orderStatus": "Shipped",
  "estimatedDelivery": "November 10, 2026",
  "latestUpdate": "The shipment departed the distribution center.",
  "customerMessage": "Your order has shipped and is expected to arrive on November 10, 2026."
}
```

### Not-found or unauthorized response

```json
{
  "orderFound": "false",
  "customerMessage": "We could not locate that order for the verified account."
}
```

Use the same response when an order does not exist and when it belongs to a different customer.

## `Cancel_Order`

The fulfillment layer must recheck customer ownership and require `callerConfirmation=confirmed` before making a state change.

### Request

```json
{
  "customerReference": "CUSTOMER-REF-10001",
  "orderID": "12345",
  "callerConfirmation": "confirmed"
}
```

### Successful response

```json
{
  "cancellationStatus": "cancelled",
  "cancellationReference": "CANCEL-70001",
  "customerMessage": "Your order has been cancelled."
}
```

### Cancellation unavailable response

```json
{
  "cancellationStatus": "not_cancelled",
  "customerMessage": "This order cannot be cancelled through self-service."
}
```

The mock backend should make cancellation idempotent. Repeating the same confirmed request must return the existing cancellation result rather than performing a second state change.
