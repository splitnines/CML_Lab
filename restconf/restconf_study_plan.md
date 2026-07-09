# Two-Hour Study Plan: Interpreting REST API Response Codes and Payloads
 ## Cisco Catalyst Center and RESTCONF

 ## Objective

Understand how to quickly interpret REST API response codes and response payloads when working with Cisco Catalyst Center APIs and RESTCONF.

## Reference Links

- Cisco Catalyst Center API documentation: https://developer.cisco.com/docs/catalyst-center/
- Cisco Catalyst Center API Quick Start: https://developer.cisco.com/docs/catalyst-center/api-quick-start/
- Cisco NETCONF and RESTCONF documentation: https://developer.cisco.com/docs/cisco-netconf-and-rest-device-management-api-documentation/cisco-netconf-and-rest-device-management-api-documentaton/
- RESTCONF request and response examples: https://developer.cisco.com/docs/epnm/working-with-request-and-response-formats/

---

## Two-Hour Study Plan

### 0:00-0:20 — REST API Response Basics

Review the purpose of HTTP response codes and how they relate to API results.

Focus on:

- `200 OK` — Request succeeded
- `201 Created` — Resource was created
- `202 Accepted` — Request was accepted but may still be processing
- `204 No Content` — Request succeeded with no response body
- `400 Bad Request` — Request format, syntax, or parameters are incorrect
- `401 Unauthorized` — Authentication is missing or invalid
- `403 Forbidden` — User is authenticated but not authorized
- `404 Not Found` — Endpoint or resource does not exist
- `409 Conflict` — Request conflicts with the current state
- `500` / `503` — Server-side or service issue

Key takeaway:

> The HTTP status code tells you whether the API request was accepted or failed at the protocol/application layer, but the response payload often explains the actual result.

---

### 0:20-0:50 — Cisco Catalyst Center API Response Interpretation

Review Cisco Catalyst Center API behavior using the DevNet documentation.

Focus on:

- Authentication and token-based access
- Common response fields:
  - `response`
  - `version`
  - `message`
  - `errorCode`
  - `detail`
  - `taskId`
  - `url`
- Task-based responses

Important point:

> In Catalyst Center, a successful HTTP response does not always mean the requested network action is complete. If the response includes a `taskId`, you must check the task result.

Example interpretation process:

1. Check the HTTP status code.
2. Read the JSON response body.
3. Look for `response`, `message`, `errorCode`, or `detail`.
4. If a `taskId` is returned, query the task endpoint.
5. Confirm whether the task completed successfully or failed.

---

### 0:50-1:20 — RESTCONF Response Interpretation

Review Cisco RESTCONF documentation.

Focus on:

- RESTCONF uses YANG-modeled data.
- RESTCONF responses may return JSON or XML.
- Correct headers are important:
  - `Accept: application/yang-data+json`
  - `Content-Type: application/yang-data+json`
- A valid RESTCONF request depends on the correct YANG resource path.

Interpret RESTCONF responses by checking:

1. HTTP status code
2. Resource path
3. Returned YANG-modeled data
4. Error message or error tag
5. Whether the request targeted configuration or operational data

Common RESTCONF interpretation examples:

- `200 OK` with payload: data was returned.
- `204 No Content`: operation succeeded, but no body was returned.
- `400 Bad Request`: request body, syntax, or headers may be invalid.
- `404 Not Found`: the RESTCONF path or YANG resource may be incorrect.
- `409 Conflict`: requested change conflicts with current device state.

---

### 1:20-1:45 — Compare Catalyst Center and RESTCONF

| Area | Catalyst Center | RESTCONF |
|---|---|---|
| API type | Controller API | Device-level API |
| Data model | Catalyst Center API schema | YANG model |
| Authentication | Token-based | Device/API authentication |
| Response format | JSON | YANG-modeled JSON/XML |
| Key thing to check | Payload and task result | Path, YANG data, and error tags |
| Common issue | Task accepted but later fails | Incorrect YANG path or payload |

Key takeaway:

> Catalyst Center often separates request acceptance from task completion. RESTCONF usually gives a more direct response from the device or YANG-modeled resource.

---

### 1:45-2:00 — Hands-On Review Exercise

Review three example API responses and answer:

1. What is the HTTP status code?
2. Did the API request succeed?
3. Is there an error message in the payload?
4. Is a task ID present?
5. Is another API call needed to verify the result?
6. What should be checked next if the request failed?

Suggested examples:

- Catalyst Center authentication response
- Catalyst Center device inventory or task response
- RESTCONF interface query or invalid path response

---

## 15-Minute Review Plan

### 0:00-0:05 — Review HTTP Status Codes

Focus on:

- `2xx` = request succeeded or was accepted
- `4xx` = client-side issue
- `5xx` = server-side issue

### 0:05-0:10 — Review Payload Clues

Check for:

- `message`
- `detail`
- `errorCode`
- `response`
- `taskId`
- RESTCONF error tags or YANG-modeled data

### 0:10-0:15 — Review Decision Process

Use this quick checklist:

1. Was the HTTP code successful?
2. Does the payload confirm success or show an error?
3. For Catalyst Center, is there a `taskId` to follow?
4. For RESTCONF, is the YANG path and payload correct?
5. What is the next troubleshooting step?
