# Runtime composition and lifecycle

Read before designing or implementing runtime wiring, resource selection, startup, or shutdown. This reference owns lifecycle behavior for every generated service. Package placement follows [service-layout.md](service-layout.md); evidence requirements follow [verification.md](verification.md#runtime-composition-and-lifecycle-evidence).

## Separate runtime responsibilities

The runtime owns the application's lifecycle across its enabled entry points and dependencies. HTTP is one possible entry point. Implement only the protocols, clients, workers, and resources selected by the requirements.

| Part | Responsibility |
| --- | --- |
| Entry point | Load validated configuration, initialize logging, handle process signals, invoke the composition, and report its terminal result. |
| Resource setup | Open database pools, broker connections, outbound clients, and other shared resources; register ownership and cleanup. |
| Feature wiring | Assemble concrete adapters and application operations for a feature, independent of its delivery protocols. |
| Transport/worker setup | Adapt the assembled application operations to each enabled server or worker and define its lifecycle. |
| Runtime coordinator | Sequence startup, track readiness, supervise running components, and coordinate shutdown and cleanup. |

Keep the coordinator readable as an ordered lifecycle. Move resource setup, feature assembly, and transport details into focused functions/files as their responsibilities grow. Use plain structs and ordinary calls under the existing constructor rules. Add shared lifecycle interfaces only when actual components benefit; a universal DI container, plugin registry, or one factory per dependency is unnecessary.

### Inbound RPC and outbound RPC

- An RPC server accepts requests and belongs with delivery entry points, alongside HTTP when both are enabled. Reuse the same feature assembly and application operations across those entry points.
- An RPC client calls another service. Its concrete adapter belongs in infrastructure and implements a port needed by its application/domain consumer. The runtime owns any client connection that requires closing.
- Enabling an outbound RPC client does not enable an RPC server. A service with no selected RPC clients or servers needs neither RPC dependencies nor placeholder RPC files.
- For an enabled RPC integration, verify its contract, effective library API, credentials/TLS configuration, deadlines, cancellation, error mapping, and connection lifecycle under [libraries.md](libraries.md) and [api-errors.md](api-errors.md). Retry and readiness behavior follow its accepted contract rather than a runtime-wide assumption.

## Component selection and fallback

Record each independently configurable component's selection, configuration requirements, dependent capabilities, and failure behavior in the technical design. Use environment settings appropriate to the actual choices; a global optional-infrastructure flag must not conceal different component policies.

| Selection | Required behavior |
| --- | --- |
| Disabled | Open no resource and start no server/worker for it. Validate enabled dependents so they cannot receive a missing dependency; explain any deliberately unavailable capability. |
| Enabled, required | Validate its configuration. Failure to initialize or meet its readiness contract fails startup and triggers cleanup. |
| Enabled, agreed fallback | State the failure conditions that permit fallback, the replacement adapter, retention/consistency implications, and available capabilities. Continue only with a valid dependency graph. |

Preserve explicit user and target instructions. A dependency failure alone does not authorize fallback to memory, discarded events, or a different upstream. Production and verification configurations may select different supported adapters through the same composition path; expose the resulting mode and safe failure reason in logs without credentials or connection secrets.

Fallback changes only the affected dependency and its explicitly affected dependents. Keep successfully opened resources alive when the remaining graph uses them. In particular, a broker fallback must not close a database still referenced by active repositories. Shared resource reuse also requires the selected library's concurrency and lifecycle guarantees to fit the consumers.

**Conditional bootstrap:** when an authorized feature needs initial data to be usable, define initialization for every supported adapter/mode that exposes that feature, including memory adapters. Make bootstrap idempotent where repeated startup requires it, honor the configured source of initial data, and settle initialization failures before reporting readiness. Authentication, seed accounts, and extra business features remain outside the default Task example.

## Startup and ownership

In the existing technical design, identify each owned resource/component, its dependents, readiness condition, startup cancellation/timeout, and stop/close mechanism. Verify whether the selected close API actually supports the agreed shutdown bound. Wrapping a non-cancellable operation in a goroutine does not establish that the operation or resource will terminate.

1. Validate the selected graph/configuration before opening resources where possible. Give startup a finite budget and propagate its cancellation/deadline into connection, handshake, and initialization operations through verified APIs.
2. Register cleanup immediately after each successful acquisition. Until startup succeeds, the startup owner releases all acquisitions on error or cancellation, including failures in bootstrap, later resources, listener binding, or readiness.
3. Assemble features and prepare enabled entry points after their required dependencies are usable. Bind required listeners and complete required readiness checks before reporting startup success; a successful goroutine launch alone is insufficient.
4. Transfer ownership to the running runtime only after successful startup. Cleanup follows reverse dependency order, normally reverse acquisition order; fallback branches preserve resources still in use. Keep startup and normal shutdown cleanup consistent and safe against repeated stop requests.

Give long-lived servers/workers a runtime-owned lifetime; a startup-only timeout that is cancelled when startup returns must not terminate successfully started components.

Partial readiness does not authorize reporting the entire selected runtime ready. If early-started components can accept work before readiness, define admission control and ensure a later startup failure stops them and cleans up their active work as well.

## Supervise running components

Collect terminal errors from enabled servers and workers through an explicit error/wait path. Distinguish expected exits caused by requested shutdown from unexpected failure; do not discard the result of a serving goroutine. Define whether failure of a component stops the whole runtime or permits a documented degraded mode, then notify the entry point and clean up as required by that decision. Automatic restarts need an accepted policy.

Own cancellation and completion of background goroutines. Cancellation requests alone are not evidence that they exited. Keep the configured readiness/health meaning accurate when a component stops; HTTP `/health` still promises only its explicit contract.

## Shutdown with one total budget

Use one shutdown deadline for the entire runtime, with each step receiving only the remaining time. Obtain a usable shutdown context when the process signal context is already cancelled. Distinguish startup cancellation, active-work lifetime, and shutdown control so a graceful drain can follow the accepted contract.

1. Stop admitting new requests/commands across enabled entry points and pause new external deliveries. Keep workers needed to drain already accepted internal work running until the drain/cancel decision is fulfilled.
2. Drain or cancel accepted work according to the event/request contract, keeping its dependencies available until that work finishes. Avoid cancelling all active work immediately if the contract requires a graceful drain.
3. Stop dependent workers and close outbound clients, broker connections, database pools, and other owned resources in dependency order. Preserve remaining time for required cleanup; an individual drain must not leave subsequent steps without a defined timeout action.
4. On deadline exhaustion, invoke supported cancellation/forced-stop/close paths, collect shutdown errors, and report incomplete cleanup honestly. For HTTP, define the forced-close path when graceful shutdown times out; for other protocols, verify their actual stop semantics. A caller that merely stops waiting cannot claim the underlying resources closed.

Propagate shutdown failure to the entry point and logs. Preserve the triggering runtime error together with relevant cleanup failures; do not silently replace it with success or omit later cleanup failures. The completion gate includes listeners closed, owned work terminated, and resource cleanup within the selected bound, or an explicit failed/blocked result.
