# API contracts, errors, and localization

## Contract before handler

**Required:** design each endpoint contract before its handler. Record method/path, request fields, response DTOs, statuses, validation, headers, error cases, and compatibility effects.

Use the target's established contract location when available; the default service-local location is `docs/api/`. Include the specification, relevant endpoint documentation, and an API changelog entry for every contract change. A breaking change to an already-published endpoint requires a new version.

The Task example's concrete routes, identifier type, payload fields, and time format are unresolved inputs. Define them before writing handlers; the capability list alone is not a complete API contract.

## Required JSON envelope

```json
{
  "status": "success | error",
  "data": {},
  "error": {
    "message": "...",
    "code": "...",
    "errors": [{ "message": "...", "code": "..." }]
  },
  "meta": {
    "pagination": {
      "currentPage": 1,
      "perPage": 10,
      "total": 100,
      "totalPages": 10
    }
  }
}
```

- **Required:** `status` and `data` are always present; avoid `omitempty` on required envelope fields.
- `status` is `success` or `error`. There is no `fail` value.
- Include `error` only for an error response; omit it on success.
- Include `meta.pagination` for paginated lists with `currentPage`, `perPage`, `total`, and `totalPages`.
- Define the actual `data` type, including its error-response value, in the endpoint contract rather than assuming the illustration determines every DTO.
- All active HTTP response paths must obey the contract, including framework-generated malformed-input, method, and not-found responses where applicable.

## Error classification and transport mapping

| Failure | HTTP class | JSON status | Internal handling |
| --- | --- | --- | --- |
| Business rule / invalid input | 4xx | `error` | Stable dedicated code and localized safe message. |
| Missing resource / conflict / access rejection | Appropriate 4xx | `error` | Preserve the specific category and contract status. |
| Database/network/other infrastructure failure | 5xx | `error` | Log the raw cause; expose a dedicated safe error. |

Domain reports rule violations. Application orchestrates and preserves/maps dependency failures into the appropriate application error category. Delivery maps that category into transport status and localized response fields. Do not infer HTTP statuses from raw infrastructure text or expose that text to callers.

Service error codes live in `pkg/errs/codes.go` and use descriptive `UPPER_SNAKE_CASE` values. Include business and technical codes actually used by the example and runtime. Prefer descriptive identifiers over organization-prefixed numeric schemes.

An error representation must carry a stable code/category and support preserving the underlying cause internally. When a shared package is available, verify its real API; names such as `AppError` or `NewTechnicalError` from old examples are not assumed to exist.

## Localization

- **Required:** use `github.com/nicksnyder/go-i18n/v2` for localization.
- Maintain `translations/errors.en.toml` and `translations/errors.id.toml` as the single source of translation messages.
- Every service code and enabled validator/helper code needs both translations. Start messages with lowercase text.
- Load or embed the translation files consistently with runtime/package layout. Verify that the files are available through the actual startup path.
- HTTP localization follows `Accept-Language`; the inspected convention supports `en` by default and `id`.
- Verify exact code keys across the error producer, response mapper, and both languages. A fallback string is not proof of complete localization.
- Keep technical causes in internal logging/error chains, not in public translated messages.

## Request validation, auth, and headers

Use named request/response DTOs and the agreed `json`/validation tags. Structural request validation complements domain invariants; it does not replace domain tests or lifecycle checks.

The Task example has a single general user role and no authentication or per-user ownership feature. Do not attach production auth/tenant requirements to this reference example implicitly.

**Conditional protected routes:** obtain authentication, tenant context, header names, and permission requirements from the target contract. Define the appropriate 401/403 responses for those routes.

**Conditional local requests:** include any headers required by the target instructions and obtain unavailable values when needed. Do not invent project-specific identity headers. Independently prove that the public health endpoint requires no authentication.

Apply CORS only for the enabled client/origin requirement. `Content-Type: application/json` is appropriate for JSON request bodies.

## Health contract

**Conditional HTTP, required when enabled:** expose GET `/health` without authentication. When the HTTP process is ready, return HTTP 200, JSON, `status: success`, `data` present, and no `error` field.

This health check proves the HTTP runtime can serve its health contract. It does not imply database/upstream/broker readiness unless additional checks are explicitly part of the contract.

The inspected httpmanager health response does not match this envelope. Use a compatible configuration or service-owned adapter/health route and verify the actual response. Local health smoke and bounded shutdown must pass before an HTTP boilerplate is complete.
