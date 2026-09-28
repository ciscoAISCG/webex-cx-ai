# Scripted AI Agent Creation For Hospital Departmental Routing

This document describes the end-to-end functionality for the scripted hospital departmental routing use case.

The scripted AI Agent identifies the hospital department the caller wants to reach, confirms the department, and then sends the call back to the Webex Contact Center voice flow for queue routing. If the caller rejects the identified department twice, the flow escalates the call to a live agent.

## Components

| Component | Description |
|---|---|
| `scripted_departmental_routing_AI_Agent.json` | Export of the scripted AI Agent. |
| `scripted_departmental_routing_voice_flow_Draft.json` | Export of the Webex CC voice flow. |
| `scripted_departmental_routing_voice_flow` | Webex Contact Center voice flow that invokes the scripted AI Agent and routes the call based on the returned state event. |
| `scripted_departmental_routing_AI_Agent` | Scripted AI Agent that collects and confirms the department name. |
| `Case_State_event` | Voice-flow case node that checks `scripted_departmental_routing_AI_Agent.StateEventName`. |
| `Parse_department_name` | Voice-flow parse node that extracts `departmentName` from `scripted_departmental_routing_AI_Agent.MetaData`. |
| `QueueContact_e4i_d6h` | Voice-flow queue node that uses `queueName` to route the call. |

---

## Common Initial Flow

All scenarios start the same way:

1. The caller calls into the `scripted_departmental_routing_voice_flow` voice flow.

2. The voice flow reaches the Virtual Agent V2 node named `scripted_departmental_routing_AI_Agent`, which triggers the scripted AI Agent named `scripted_departmental_routing_AI_Agent`.

3. The voice flow sends the following event name and event data to the AI Agent:

   ```text
   eventName - state_update
   eventDataJson - {"intent":"Identify_Department"}
   ```

4. This triggers the `Identify_Department` intent.

5. The caller hears the response configured in `departmentName_entity_response` for the `departmentName` entity:

   ```text
   Hello, Welcome to SCG hospital. which department would you like to talk to ?
   ```

6. The `Identify_Department` intent also sets the exit context as `departmentIdentified`.

7. When the caller says `cardiology`, the `departmentName` entity slot is filled with `Cardiology`.

8. The AI Agent then triggers the response configured for the `Identify_Department` intent, which is `Identify_Department_Response`. It plays:

   ```text
   you would like to talk to ${entity.departmentName} department. is that right ?
   ```

   `${entity.departmentName}` contains the detected department, such as `Cardiology`.

---

## Scenario 1 - Caller Confirms The Department

In this scenario, the caller confirms the detected department on the first attempt.

1. The caller says `yes`.

2. This triggers the `yes` intent.

3. The `yes` intent has `departmentIdentified` as its entry context. Because `Identify_Department` set the `departmentIdentified` context, the AI Agent plays the `Yes_response` response:

   ```text
   Thank you, transferring you to ${entity.departmentName} now.
   ```

   `${entity.departmentName}` contains `Cardiology`.

4. The `Yes_response` response has a custom event configured with the name `yes` and the following event payload:

   ```json
   {"departmentName":"${entity.departmentName}"}
   ```

5. This transitions the call back to the Webex CC voice flow, `scripted_departmental_routing_voice_flow`.

6. The call exits the AI Agent and reaches the `Case_State_event` node.

7. The `Case_State_event` node checks the `scripted_departmental_routing_AI_Agent.StateEventName` variable. Because the custom event from the AI Agent has `Yes` in the state event, it matches the `Yes` condition and the call moves to the next node.

8. In the `Parse_department_name` node, the `scripted_departmental_routing_AI_Agent.MetaData` variable is used to extract the `departmentName` passed from the AI Agent.

9. The extracted `departmentName` is inserted into the `queueName` variable.

10. The `queueName` variable is used in the `QueueContact_e4i_d6h` node to queue the call.

11. A `Cardiology` queue is configured in the tenant, and the call is queued to `Cardiology`.

---

## Scenario 2 - Caller Rejects Once, Then Confirms

In this scenario, the caller rejects the first detected department, provides another department, and then confirms it.

1. The caller says `No`.

   Reset slots after completion is enabled in the `No` intent, so the entity slots will be cleared when `No` intent execution completes.

2. This triggers the `No` intent.

3. The `No` intent has `departmentIdentified` as its entry context. Because `Identify_Department` set the `departmentIdentified` context, the AI Agent plays the `No_response` response:

   ```text
   Let's try again.
   ```

4. The `No_response` response has a custom event configured with the name `No` and the following event payload:

   ```json
   {}
   ```

5. This transitions the call back to the Webex CC voice flow, `scripted_departmental_routing_voice_flow`.

6. The call exits the AI Agent and reaches the `Case_State_event` node.

7. The `Case_State_event` node checks the `scripted_departmental_routing_AI_Agent.StateEventName` variable. Because the custom event from the AI Agent has `No` in the state event, it matches the `No` condition and the call moves to the next node.

8. The `incrementCounter` set-variable node increments the counter value from `0` to `1`. The counter was initially set to `0`.

9. The `checkIfCounterMaxed` node checks whether the counter value is `2`.

10. In this scenario, the counter value is `1`, so the condition fails and the call exits from the false path.

11. The call then triggers the `findDepartmentAgain` node, which sets `eventDataJson` as follows:

    ```json
    {
      "intent":"Identify_Department",
      "context":{"findDepartmentAgain":"5"}
    }
    ```

12. The call goes back to the scripted AI Agent, `scripted_departmental_routing_AI_Agent`, and triggers the `Identify_Department` intent again.

13. The call reaches the `departmentName_entity_response` response.

14. This time, the conditional response checks whether `lastdfState.context.findDepartmentAgain` exists.

15. Because the voice flow sent `findDepartmentAgain` with `5` turns, the context exists for five conversational turns. The condition is met, so the AI Agent plays the retry prompt instead of the default prompt:

    ```text
    Could you tell me the department you would like to be transferred to?
    ```

16. The caller says `pediatrics`.

17. The `departmentName` entity slot is filled with `Pediatrics`.

18. The caller hears the `Identify_Department_Response` response again:

    ```text
    you would like to talk to ${entity.departmentName} department. is that right ?
    ```

    `${entity.departmentName}` contains `Pediatrics`.

19. The caller says `yes`.

20. This triggers the `yes` intent.

21. The `Yes_response` response plays:

    ```text
    Thank you, transferring you to ${entity.departmentName} now.
    ```

    `${entity.departmentName}` contains `Pediatrics`.

22. The `Yes_response` response sends the custom event named `yes` with the following event payload:

    ```json
    {"departmentName":"${entity.departmentName}"}
    ```

23. The call transitions back to the Webex CC voice flow, `scripted_departmental_routing_voice_flow`.

24. The call reaches the `Case_State_event` node.

25. The `Case_State_event` node checks `scripted_departmental_routing_AI_Agent.StateEventName`. Because the custom event from the AI Agent has `Yes` in the state event, it matches the `Yes` condition.

26. In the `Parse_department_name` node, the `scripted_departmental_routing_AI_Agent.MetaData` variable is used to extract the `departmentName` passed from the AI Agent.

27. The extracted `departmentName` is inserted into the `queueName` variable.

28. The `queueName` variable is used in the `QueueContact_e4i_d6h` node to queue the call.

29. A `Pediatrics` queue is configured in the tenant, and the call is queued to `Pediatrics`.

---

## Scenario 3 - Caller Rejects Twice And Is Escalated

In this scenario, the caller rejects the detected department twice, so the flow escalates the call to a live agent.

1. The caller says `No`.

   Reset slots after completion is enabled in the `No` intent, so the entity slots will be cleared when `No` intent execution completes.

2. This triggers the `No` intent.

3. The AI Agent plays the `No_response` response:

   ```text
   Let's try again.
   ```

4. The `No_response` response sends the custom event named `No` with the following event payload:

   ```json
   {}
   ```

5. The call transitions back to the Webex CC voice flow, `scripted_departmental_routing_voice_flow`.

6. The call reaches the `Case_State_event` node.

7. The `Case_State_event` node checks `scripted_departmental_routing_AI_Agent.StateEventName`. Because the custom event from the AI Agent has `No` in the state event, it matches the `No` condition.

8. The `incrementCounter` set-variable node increments the counter value from `0` to `1`.

9. The `checkIfCounterMaxed` node checks whether the counter value is `2`.

10. Since the counter value is `1`, the condition fails and the call exits from the false path.

11. The call triggers the `findDepartmentAgain` node, which sets `eventDataJson` as follows:

    ```json
    {
      "intent":"Identify_Department",
      "context":{"findDepartmentAgain":"5"}
    }
    ```

12. The call goes back to the scripted AI Agent and triggers the `Identify_Department` intent again.

13. Because `lastdfState.context.findDepartmentAgain` exists, the AI Agent plays the retry prompt:

    ```text
    Could you tell me the department you would like to be transferred to?
    ```

14. The caller says `pediatrics`.

15. The `departmentName` entity slot is filled with `Pediatrics`.

16. The AI Agent plays the `Identify_Department_Response` response:

    ```text
    you would like to talk to ${entity.departmentName} department. is that right ?
    ```

    `${entity.departmentName}` contains `Pediatrics`.

17. The caller says `No` again.

    Reset slots after completion is enabled in the `No` intent, so the entity slots will be cleared when `No` intent execution completes.

18. This triggers the `No` intent again.

19. The AI Agent plays the `No_response` response:

    ```text
    Let's try again.
    ```

20. The `No_response` response sends the custom event named `No` with the following event payload:

    ```json
    {}
    ```

21. The call transitions back to the Webex CC voice flow, `scripted_departmental_routing_voice_flow`.

22. The call reaches the `Case_State_event` node.

23. The `Case_State_event` node checks `scripted_departmental_routing_AI_Agent.StateEventName`. Because the custom event from the AI Agent has `No` in the state event, it matches the `No` condition.

24. The `incrementCounter` set-variable node increments the counter value from `1` to `2`.

25. The `checkIfCounterMaxed` node checks whether the counter value is `2`.

26. Because the current counter value is `2`, the condition is true and the call triggers the `Escalate` set-variable node.

27. The `Escalate` set-variable node sets the following data:

    ```text
    eventName - No_response
    eventDataJson - {
      "escalate":"yes"
    }
    ```

28. The call goes back to the AI Agent and triggers the `No_response` response.

29. In `No_response`, the `retryExceeded` condition checks whether `eventStore.escalate` equals `Yes`.

30. Since this condition is true, the AI Agent plays:

    ```text
    Sorry we are unable to identify your department, Let me transfer you to live agent to assist.
    ```

31. The AI Agent exits to the voice flow with the custom event name `customEscalation`.

32. The call reaches the `Case_State_event` node.

33. The `Case_State_event` node checks `scripted_departmental_routing_AI_Agent.StateEventName`. Because the custom event from the AI Agent has `customEscalation` in the state event, it matches the `customEscalation` condition.

34. The call goes to the queue contact node and is queued for live-agent assistance.
