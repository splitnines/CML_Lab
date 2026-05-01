# REST API Response Codes

## 2xx — Success

| Code | Meaning | Description |
|---|---|---|
| 200 | OK | Request succeeded. Common for `GET`, `PUT`, `PATCH`. |
| 201 | Created | Resource was created successfully. Common for `POST`. |
| 202 | Accepted | Request accepted for processing, but not completed yet. |
| 204 | No Content | Request succeeded, but response has no body. Common for `DELETE`. |

## 3xx — Redirection

| Code | Meaning | Description |
|---|---|---|
| 301 | Moved Permanently | Resource has permanently moved to a new URL. |
| 302 | Found | Resource temporarily available at another URL. |
| 304 | Not Modified | Cached version is still valid. |

## 4xx — Client Errors

| Code | Meaning | Description |
|---|---|---|
| 400 | Bad Request | Request is malformed or invalid. |
| 401 | Unauthorized | Authentication is missing or invalid. |
| 403 | Forbidden | Authenticated, but not allowed to access the resource. |
| 404 | Not Found | Resource does not exist. |
| 405 | Method Not Allowed | HTTP method is not supported for this resource. |
| 409 | Conflict | Request conflicts with the current resource state. |
| 410 | Gone | Resource used to exist but is no longer available. |
| 415 | Unsupported Media Type | Request body format is not supported. |
| 422 | Unprocessable Entity | Request is syntactically valid but semantically invalid. |
| 429 | Too Many Requests | Rate limit exceeded. |

## 5xx — Server Errors

| Code | Meaning | Description |
|---|---|---|
| 500 | Internal Server Error | Generic server-side failure. |
| 501 | Not Implemented | Server does not support the requested functionality. |
| 502 | Bad Gateway | Gateway or proxy received an invalid response from an upstream server. |
| 503 | Service Unavailable | Server is temporarily unavailable or overloaded. |
| 504 | Gateway Timeout | Gateway or proxy timed out waiting for an upstream server. |

## Common REST Usage Examples

| Operation | Typical Success Code |
|---|---|
| `GET /items` | `200 OK` |
| `GET /items/123` | `200 OK` or `404 Not Found` |
| `POST /items` | `201 Created` |
| `PUT /items/123` | `200 OK` or `204 No Content` |
| `PATCH /items/123` | `200 OK` or `204 No Content` |
| `DELETE /items/123` | `204 No Content` |

