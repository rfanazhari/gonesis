# Go implementation standards

These are the consolidated implementation rules for the workflow. Use the agreed requirement labels from the reference index.

## Architecture and design

- **Required:** use Clean Architecture with inward dependencies and SOLID responsibilities.
- Delivery translates transport input/output, invokes application behavior, and maps errors. It does not own business invariants.
- Application orchestrates domain behavior and required ports. Domain owns business rules and has no database, broker, or HTTP I/O.
- Infrastructure implements domain/application ports and maps persistence/external data to the appropriate inner types.
- **Required:** use DDD tactical patterns where real business rules justify them. The Task example has lifecycle and validity rules; keep these in domain behavior.
- **Required:** apply KISS, YAGNI, and SRP. Add only the patterns, packages, configuration, and abstractions required by the current example or enabled component.
- Keep database models inside infrastructure; use explicit API DTOs instead of serializing database models as responses.
- Use the four root layers and package paths specified in [service-layout.md](service-layout.md).

## Language and names

- **Required:** use `any` instead of `interface{}`.
- Package names are short, lowercase, single words without underscores or mixed capitals.
- Multiword Go identifiers use `MixedCaps` or `mixedCaps`.
- Keep identifiers private until callers outside the package need them.
- Getter-style methods use `Owner()` rather than `GetOwner()` when matching an owned field. Match established interface signatures such as `String() string` where applicable.
- Return errors last.
- Import types directly. Do not create cross-layer aliases such as `type Specifications = query.Specifications`.

## Structs and constructors

- **Required:** use named struct types with public fields; avoid anonymous structs.
- A service-owned `NewX` constructor is appropriate only when it performs business validation and returns an error. Apply validating construction to domain objects and use-case input/command objects where needed.
- **Required:** use plain structs for repositories and infrastructure; do not add constructors there.
- Calls to dependency-provided constructors follow the verified dependency API. This does not authorize adding service-owned wiring constructors that bypass the rule above.
- By default keep a struct, its constructor, and methods in one file.
- When it grows, keep the struct/constructor in its primary file and split methods by concern into `<struct>_<concern>.go`.
- Use one aggregate, entity, or value object per file.

## File organization and tools

- **Required:** put private variables/constants at the top, grouped in `var (...)` / `const (...)` blocks; put private functions before public functions.
- **Recommended:** keep non-test, non-generated Go files below 300 lines. At 500 lines, splitting by responsibility is required.
- Run `gofmt`; do not manually maintain field alignment.
- **Required:** pass `golangci-lint` with the target's compatible configuration; generated `*_mock.go` files are excluded from linting.
- Verify code with `go test`, not `go build` or `go run`. Full commands and smoke requirements are in [verification.md](verification.md).
- Edit Go files through complete-block rewrites or exact replacements. Do not use regex-based shell editing, including `sed`/`awk`, for Go source.

## Configuration and lifecycle

- **Required:** read runtime configuration from environment variables. Local dotenv loading may assist development; committed files contain examples, never secrets.
- Document required/default/format for every enabled variable and reject invalid configuration during startup.
- Include only enabled integrations in `.env.example`; remove unrelated sample hosts, Redis settings, or certificate names.
- Use the service identity consistently in module configuration, logs, and runtime documentation.
- Initialize required logging early enough to report startup failures without substituting standard-library logging.
- Propagate cancellation/deadlines into I/O. Close already-opened resources on startup failure and close owned resources during shutdown.
- Give startup, request, and shutdown verification finite time limits.

## Performance and concurrency

- **Required:** use maps for repeated in-memory lookups/deduplication where suitable; slices retain ordering and remain appropriate repository return types.
- Prefer one joined query to sequential database round trips and N+1 traversal.
- Parallelize independent I/O where appropriate; propagate context, bound concurrency, and manage worker lifetimes.
- Do not create unbounded goroutines per request. Background side effects need explicit cancellation and completion ownership.
- Configure connection pools for the selected adapter and workload.
- Cache repeated expensive responses only when the requirement or measured workload calls for it.
- Prefer direct infrastructure mappings over unnecessary intermediate representations while retaining layer boundaries.

## Security and transport-specific requirements

- **Required:** treat external input as untrusted; validate and sanitize applicable input. `go-playground/validator` is the recommended Go request-validation library.
- Keep authorization least-privileged when protected routes are in scope. The Task reference has no authentication or ownership feature.
- Apply relevant OWASP Top 10 protections, safe input/output handling, allowed-origin policies, and brute-force/rate controls for exposed functionality.
- Mask credentials, tokens, cookies, and applicable PII in logs; never commit secret values.
- Parameterize SQL and pass context to every query/command.
- **Conditional gRPC:** use proto3 and Buf for generation. gRPC Gateway is not allowed. Map transport errors to appropriate gRPC statuses in delivery.

Library requirements, version-sensitive APIs, and tracing behavior are consolidated in [libraries.md](libraries.md); HTTP contracts and safe error responses are in [api-errors.md](api-errors.md).
