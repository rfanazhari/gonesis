# Standard libraries and API verification

## Selection policy

| Need | Library | Requirement |
| --- | --- | --- |
| Operational logging/tracing | `github.com/SALT-Indonesia/salt-pkg/logmanager` | Required for service logging. |
| Outbound HTTP | `github.com/SALT-Indonesia/salt-pkg/clientmanager` | Required when outbound HTTP is implemented. |
| HTTP server/handlers/middleware | `github.com/SALT-Indonesia/salt-pkg/httpmanager` | Recommended when it fits; an alternative needs a recorded reason. |
| Event mechanism | `github.com/SALT-Indonesia/salt-pkg/eventmanager` | Recommended when it fits the chosen event mechanism. |

The Task example requires an internal completion event. That requirement does not automatically enable RabbitMQ or select eventmanager. Do not add outbound clients, database drivers, or broker dependencies solely to complete a library list.

Use `go-i18n/v2` for error localization. Request validation uses the relevant approved validator. Driver, migration, and test dependencies follow the enabled components and target versions.

## Verify before standardizing an integration

1. Inspect the target's `go.mod`, `go.sum`, optional workspace, replacements, and requested constraints. Determine the effective resolved version, which may differ from a single module's declaration.
2. Read the exported API/source for that version. Verify argument/return types, error behavior, context requirements, configuration, default responses, and lifecycle methods.
3. Compare behavior with the required API envelope and component contract. Identify missing features and any service-local adaptation needed.
4. When implementation is authorized, use `go test` to establish compilation and test the relevant behavior through the actual integration.
5. Record library/version or commit, symbols used, source, test evidence, and any remaining limitations.

Do not copy an unverified README example into a supposedly standard implementation. Do not automatically select the newest version. Review dependency upgrades and any effects on other modules.

API verification against the actual dependency is live project discovery. The workflow rules below are self-contained; separate library skills are not prerequisites.

## Logging foundation

- Initialize one logmanager application with the actual service identity and JSON output.
- Set the application name and configure masking for Authorization, Cookie, passwords, tokens, and relevant PII.
- Preserve request context/transactions across application and adapter calls. Background/worker calls must establish suitable transactions themselves.
- End transactions and segments according to the selected API. Review transaction safety when introducing concurrent work.
- Log raw technical errors internally and expose safe, localized errors separately.
- **Conditional OTEL:** enable from environment only when requested/configured; leave it inactive when no endpoint is configured. Verify URL/protocol/header handling for the selected API instead of assuming a bare host:port option accepts a URL.
- When supported by the selected version, `WithOTelFromEnv` follows standard `OTEL_EXPORTER_OTLP_*` configuration. Authentication headers are secrets.

## Recorded HTTP/client/logging source inspection

The following findings were recorded on 2026-10-26 and carried into this consolidation. They are not universal pins or fresh runtime-test results.

| Version inspected | Verified source behavior | Integration consequence |
| --- | --- | --- |
| httpmanager v0.16.11 | `NewServer(*logmanager.Application, ...OptionFunc)`, typed `NewHandler`, `ResponseError[T]`, `ResponseSuccess[T]`, and `Stop(context.Context)` are available. | Typed bodies and bounded shutdown have suitable API entry points, subject to implementation tests. |
| httpmanager v0.16.11 | `NewHandler[Req, Resp]` takes a method and `func(context.Context, *Req) (*Resp, error)`. | Handlers can return explicitly typed success/error envelopes. |
| httpmanager v0.16.11 | Built-in health returns `{"status":"ok"}`. Malformed input and method mismatch use `http.Error`; not-found uses `http.NotFound`. | Defaults do not satisfy the required response envelope; adapt the active response paths and verify them. |
| clientmanager v0.10.1 | `Call[Response](context.Context, string, ...Option)` returns `(*BaseResponse[Response], error)`; request context needs a logging transaction. | Logging/context setup precedes outbound calls, including worker/background calls. |
| logmanager v1.44.1 and v1.46.2 | `NewApplication(...Option)`, `StartOtherSegment(*Transaction, OtherSegment)`, and `StartOtherSegmentWithContext` exist. | A context passed directly to `StartOtherSegment` does not match these inspected signatures. |
| logmanager v1.46.2 | `WithOTelFromEnv()` exists; it was not found in inspected v1.44.1. | The original boilerplate logging version cannot assume that newer OTEL wiring API. |

These inspected versions are compatibility evidence only. Determine the target's effective dependency versions instead of inheriting a snapshot implicitly.

## Recorded eventmanager inspection

The recorded upstream source inspection used tag `eventmanager/v0.2.5`, commit `c4c0d0afe1cd32904846c2de48c78e4b9d4472e2`. That version has not been chosen as the example's dependency.

Verified exported shapes:

```text
Publish(ctx context.Context, exchange string, body any) error
Subscribe[Message any](ctx context.Context, queueName, exchange string, handlers []Handler[Message])
Handler[Message any] func(Message) (domainErr, infrastructureErr error)
```

This implementation uses RabbitMQ. Its handler has two error returns and no context argument; the README's one-error handler example does not match this inspected source.

Publisher configuration needs `RABBITMQ_URL` and a logmanager transaction in context. Consumer configuration includes channel count, reconnect delay, prefetch, refresh delay, retry count, and retry delay through the respective `RABBITMQ_*` variables; verify selected-version parsing/defaults before configuring them.

The inspected publish path ignores the error returned by `PublishWithContext`. Consumer lifetime/cancellation also needs scrutiny for service shutdown. Source inspection therefore does not establish reliable publish-success reporting or complete shutdown behavior.

Use a version/adapter/alternative that satisfies the actual contract. Document incompatibilities; do not promise delivery, retry, acknowledgement, or idempotency guarantees from a README illustration.

## Shared helper limitations

The inspected root response helper omitted `data` from its error response. Its validation helper path also used `FAILED_VALIDATION` while the example translation catalog used `VALIDATION_FAILED`. Verify exact producer/mapper/catalog agreement.

The shared errors implementation exposed `Error` and `CodeError`-based APIs; older documentation referred to `AppError` and `NewTechnicalError`. The consolidated requirement is typed classification, safe mapping, preserved internal cause, and localization—not those unverified symbol names.

A compatible shared package may be reused. Otherwise implement the minimum service-local behavior without introducing an unavailable project-specific import. Source audit locations and upstream identifiers are recorded in [sources.md](sources.md).
