# Scripted AI Agent Creation For Hospital Payment System

This document describes the end-to-end functionality for the scripted hospital payment use case.

## Components

| Component | Description |
|---|---|
| `Payment_Flow_Scripted` | Webex Contact Center voice flow. It internally calls two subflows for API calls. |
| `makePayment` | Webex Contact Center subflow for completing payment by calling an API. |
| `checkBalance` | Webex Contact Center subflow for checking balance. |
| `Payment_Agent_Scripted` | Webex CC AI Agent flow. |

---

## 1st Functionality - Check Balance

When a caller calls in and says they want to check their balance, the following sequence occurs:

1. The `Payment Balance` intent is triggered because it has utterances that detect the caller's intent as `Payment Balance`.

2. The agent collects two entities:
   - `patientID`
   - `dateOfBirth`

3. After the collection is successful, control moves to the `Payment_Balance_Response` response. It says:

   ```text
   Thank you for the details, Let me check your balance one moment
   ```

   The response then goes to the WXCC voice flow with the following state event name and metadata:

   ```text
   state_event - Payment_Balance_Response_custom_Event
   metadata - {"dateOfBirth":"${entity.dateOfBirth}","patientID":"${entity.patientID}"}
   ```

4. In the Webex CC voice flow, control comes out of the handled path in the `AI_Agent_payment` node with data like the following:

   ```text
   MetaData
   Map(patientID -> 1*****, dateOfBirth -> 04/15/1972)

   StateEventName
   Payment_Balance_Response_custom_Event
   ```

5. In the `state_event_decider` node, it matches the `Payment_Balance_Response_custom_Event` path.

6. The flow triggers the `Parse_checkBanalnceData` node to extract `patientID` and `dateOfBirth` from metadata using the JSON path expressions `$.patientID` and `$.dateOfBirth`, respectively.

7. It then triggers the `checkBalance` subflow and passes `patientID` and `dateOfBirth` as input variables.

8. The `checkBalance` subflow invokes the API call to get balance details in the `HTTPRequest_p83` node.

9. The subflow then uses a `setVariable` node to set the `paymentBalance` obtained from the API call, and it assigns that value to `outPutJSON`. It also has an `eventNameSubflow` output variable, which contains `announceBalanceResponse`. `announceBalanceResponse` is a response defined in the Webex CC AI Agent. There are also a couple of other output variables in this subflow, such as `accountNumber`, which will be used in subsequent API calls.

10. Control now goes back to the main flow, `Payment_Flow_Scripted`, where the following subflow variables are mapped to main-flow variables:

    | Subflow | Main flow |
    |---|---|
    | `outPutJSON` | `eventDataTOAIAgent` |
    | `accountNumber` | `MainFlowAccountNumber` |
    | `paymentBalance` | `MainFlowPaymentBalance` |
    | `eventNameSubflow` | `eventName` |

11. In the `dataBacktoAI` node, `eventName` is assigned with `{{eventName}}` coming from the subflow, and `eventDataJson` is assigned with `{{eventDataTOAIAgent}}` coming from the subflow.

    For example:

    ```text
    eventName - announceBalanceResponse
    eventDataJson - {"paymentBalance":"247.85"}
    ```

12. It then triggers `AI_Agent_payment` with the `Payment_Agent_Scripted` Webex CC AI Agent, using the data from step 11.

13. Control goes back to the AI Agent, and it triggers the `announceBalanceResponse` response.

    There are two conditions:

    - `checkIfbalanceIntent`
    - `checkIfPaymentIntent`

14. In this case, it triggers `checkIfbalanceIntent` because `lastdfState.model_state.intent.name` equates to `Payment Balance`. It then plays the balance using the following SSML:

    ```xml
    <speak>
       your balance is
      <say-as interpret-as="currency" language="en-US">USD${eventStore.paymentBalance}</say-as>. Thanks and have a great Day
    </speak>
    ```

    `${eventStore.paymentBalance}` contains the payment balance sent from the WXCC voice flow in step 11.

15. It then sends the custom state event `Bye` back to the voice flow. This eventually lands on the `state_event_decider` node, takes the `Bye` path, and disconnects the call.

---

## 2nd Functionality - Make Payment

When a caller calls in and says they want to make a payment, the following sequence occurs:

1. The `Make_Payment` intent is triggered because it has utterances that detect the caller's intent as `Make_Payment`.

2. The agent collects two entities:
   - `patientID`
   - `dateOfBirth`

   The design checks the balance before proceeding with the payment.

3. After the collection is successful, control moves to the `make_Payment_Response` response. It says:

   ```text
   Thanks for the details let me check your balance before processing payment.
   ```

   The response then goes to the WXCC voice flow with the following state event name and metadata:

   ```text
   state_event - make_Payment_Custom_Event
   metadata - {"dateOfBirth":"${entity.dateOfBirth}","patientID":"${entity.patientID}"}
   ```

4. In the Webex CC voice flow, control comes out of the handled path in the `AI_Agent_payment` node with data like the following:

   ```text
   MetaData
   Map(patientID -> 1*****, dateOfBirth -> 04/15/1972)

   StateEventName
   make_Payment_Custom_Event
   ```

5. In the `state_event_decider` node, it matches the `make_Payment_Custom_Event` path.

6. The flow triggers the `Parse_checkBanalnceData` node to extract `patientID` and `dateOfBirth` from metadata using the JSON path expressions `$.patientID` and `$.dateOfBirth`, respectively.

7. It then triggers the `checkBalance` subflow and passes `patientID` and `dateOfBirth` as input variables.

8. The `checkBalance` subflow invokes the API call to get balance details in the `HTTPRequest_p83` node.

9. The subflow then uses a `setVariable` node to set the `paymentBalance` obtained from the API call, and it assigns that value to `outPutJSON`. It also has an `eventNameSubflow` output variable, which contains `announceBalanceResponse`. `announceBalanceResponse` is a response defined in the Webex CC AI Agent. There are also a couple of other output variables in this subflow, such as `accountNumber`, which will be used in subsequent API calls.

10. Control now goes back to the main flow, `Payment_Flow_Scripted`, where the following subflow variables are mapped to main-flow variables:

    | Subflow | Main flow |
    |---|---|
    | `outPutJSON` | `eventDataTOAIAgent` |
    | `accountNumber` | `MainFlowAccountNumber` |
    | `paymentBalance` | `MainFlowPaymentBalance` |
    | `eventNameSubflow` | `eventName` |

11. In the `dataBacktoAI` node, `eventName` is assigned with `{{eventName}}` coming from the subflow, and `eventDataJson` is assigned with `{{eventDataTOAIAgent}}` coming from the subflow.

    For example:

    ```text
    eventName - announceBalanceResponse
    eventDataJson - {"paymentBalance":"247.85"}
    ```

12. It then triggers `AI_Agent_payment` with the `Payment_Agent_Scripted` Webex CC AI Agent, using the data from step 11.

13. Control goes back to the AI Agent, and it triggers the `announceBalanceResponse` response.

    There are two conditions:

    - `checkIfbalanceIntent`
    - `checkIfPaymentIntent`

14. In this case, it triggers `checkIfPaymentIntent` because `lastdfState.model_state.intent.name` equates to `Make_Payment`. It also has another condition to check whether the `paymentBalance` variable was returned from the voice flow by using `eventStore.paymentBalance` and the `exists` condition.

    It then plays the balance using the following SSML:

    ```xml
    <speak>
       your balance is
      <say-as interpret-as="currency" language="en-US">USD${eventStore.paymentBalance}</say-as>.
     Let me continue processing your payment.
    </speak>
    ```

    `${eventStore.paymentBalance}` contains the payment balance sent from the WXCC voice flow in step 11.

15. It then sends the custom state event `state_update` back to the voice flow. This eventually lands on the `state_event_decider` node and takes the `state_update` path.

    It also sends the following metadata:

    ```json
    {"intent":"collectPaymentDetails"}
    ```

16. The call eventually lands on the `state_event_decider` node in the WXCC voice flow, where it takes the `state_update` path. This triggers a set-variable node that sends the following data back to the AI Agent:

    ```text
    eventName
    state_update

    eventDataTOAIAgent
    {"intent":"collectPaymentDetails"}
    ```

17. Control goes back to the voice flow, and this time it triggers the `collectPaymentDetails` intent. Control directly hits the slot-filling response provided in that intent and starts collecting the `cardNumber` slot using the `cardNumberEntityCollectionResponse` response, where it plays:

    ```text
    Please provide your card number
    ```

    Similarly, it collects `CVV` and `dateOfBirth`.

18. Control now goes to the response configured for that intent, which is `collectPaymentDetailsResponse`. It plays:

    ```text
    Thanks for the details, one moment while I process your payment
    ```

    It then triggers the `collectPaymentDetails_customEvent` custom state event with the following payload:

    ```json
    {"CVV":"${entity.CVV}","CardNumber":"${entity.CardNumber}","expiryDate":"${entity.expiryDate}"}
    ```

19. Control goes back to the WXCC voice flow, which receives the following data:

    ```text
    Metadata - (Cardnumber -> 1234567812345678, CVV -> 125, dateOfBirth -> 125)
    state_event - collectPaymentDetails_customEvent
    ```

20. It takes the `collectPaymentDetails_customEvent` path in the `state_event_decider` node.

21. The flow triggers the `Parse_makePaymentData` node, where `cardNumber`, `CVV`, and `expiryDate` are extracted using the JSON path that came in from the AI Agent.

22. It then triggers the `makePayment` subflow with the following input variables:

    - `cardNumber`
    - `CVV`
    - `expiryDate` received from the AI Agent
    - `mainFlowAccoutnNumber`
    - `MainFlowPaymentBalance` obtained in the previous `checkBalance` subflow

23. The `makePayment` subflow makes the API call to fulfill the payment and returns the following data upon success:

    ```text
    outPutJSONFromMakePayment - {"status":"{{status}}",
    "currency":"{{currency}}",
    "amount":"{{subFlowBalanceAmount_makePayment}}"
    }
    subFlowEventName - PaymentResultResponse (this is a response defined in wxcc AI agent)
    ```

24. Control goes back to the main voice flow, where `dataBackToAIAgent` sends the following to the scripted AI Agent:

    ```text
    eventName
    paymentResultResponse

    eventDataJson
    {"status":"succeeded","currency":"USD","amount":"247.85"}
    ```

25. In `paymentResultResponse`, it plays:

    ```text
    Thankyou, your payment processing ${eventStore.status}, Good bye.
    ```

    `${eventStore.status}` contains `succeeded`, as shown in step 24.

26. After that, the AI Agent sends the `Bye` custom state event back to the WXCC voice flow.

27. The `state_event_decider` takes the `Bye` path, and the call is disconnected using the `DisconnectContact_gse` node.
