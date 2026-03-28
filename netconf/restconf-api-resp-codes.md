# Common RESTCONF response codes

- `200 OK` — Request succeeded; response body returned.
- `201 Created` — Resource created successfully.
- `204 No Content` — Request succeeded; no response body.
- `400 Bad Request` — Malformed request or invalid input.
- `401 Unauthorized` — Authentication required or failed.
- `403 Forbidden` — Authenticated, but not allowed.
- `404 Not Found` — Resource does not exist.
- `405 Method Not Allowed` — HTTP method not valid for this resource.
- `406 Not Acceptable` — Requested response format not supported.
- `409 Conflict` — Conflict with current datastore/resource state.
- `412 Precondition Failed` — Conditional request check failed.
- `413 Payload Too Large` — Request body too large.
- `415 Unsupported Media Type` — Request content type not supported.
- `500 Internal Server Error` — Server-side processing failure.
- `501 Not Implemented` — Requested operation/capability not supported.
