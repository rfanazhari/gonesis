# Final verification and blockers

Use this checklist when the service implementation is authorized. Consolidating these references does not establish any service test or runtime result.

## Required checks

| Area | Passing evidence |
| --- | --- |
| Scope/identity | Diff implements the foundation and one agreed example; module/import/config identity is consistent. |
| Layout | Four root layers follow the consolidated layout; enabled packages have real responsibilities. |
| Architecture | Repeatable dependency checks pass; domain tests prove business-rule ownership. |
| Design assessment | The owning feature document contains tactical/technical design and ticket-linked findings/dispositions under [design-assessment.md](design-assessment.md); selected changes are verified and no deferred finding blocks acceptance. |
| Business behavior | All nine Task rules and acceptance scenarios pass with RED/GREEN evidence. |
| Configuration | Enabled environment settings have required/default/format documentation; invalid config is rejected and secrets stay out of source/logs. |
| Runtime composition/lifecycle | Applicable scenarios in Runtime composition and lifecycle evidence below pass through the actual composition; enabled entry points are supervised and cleanup completes within one total shutdown budget. |
| Error/localization | Codes and EN/ID translations agree; technical causes remain internal; public responses use the required envelope. |
| All Go packages | Formatting is clean and `go test ./...` succeeds, including cmd/delivery/infrastructure compilation. |
| Domain/application suite | Specific edited tests and the full example unit suite pass. An empty suite does not pass. |
| Lint/security | The provided lint and vulnerability checks succeed with compatible tools. |
| Example API | The runtime's API demonstrates the agreed example behavior using real composition and adapters. |
| HTTP runtime, when enabled | Local `/health` smoke passes, including JSON envelope and bounded shutdown. |
| Artifacts/docs | Contracts, business rules, README, migrations if applicable, and generated mocks match implemented behavior. |

## Go commands and tooling

From the service root, provide and verify the actual commands, using these established shapes:

```sh
go test ./...
make test
make lint
make test.security
```

The inspected Makefile equivalents were:

```sh
go test ./domain/... ./application/... -coverprofile=coverage.out -race -v
golangci-lint run -v --timeout 12m
govulncheck ./...
go tool cover -html=coverage.out -o coverage.html
```

Make targets must match the generated service and installed tool versions. If a target uses an equivalent command, document it explicitly. Domain/application coverage alone is insufficient to compile every runtime package, so retain the all-package check.

Run formatting checks, the specific test after each edit, then the full service suite when it passes. Do not hide failures behind `|| true`. Verify through `go test`; do not substitute `go build`, `go run`, an image build, or an unexecuted command listing.

Provide the architecture-check command as part of implementation. The design has not selected an existing archtest package or command; merely mentioning archtest in the report is insufficient.

## Example feature evidence

- Preserve a rule → public test/scenario → RED/GREEN result mapping for BR-01–BR-09 and its service-doc IDs.
- Check title/date boundaries, initial status, valid/invalid transitions, Done finality, overdue behavior, system timestamps, missing records, dependency failures, and completion-event behavior.
- Use controlled time: create at a valid time, then advance beyond the due date for overdue tests.
- Demonstrate create → start → complete → view through the actual API and a rejected direct Todo → Done transition, using the same composition path as the executable. Supported test adapter/configuration selections and bootstrap fixtures may differ; rebuilding use cases, repositories, or routes in the harness does not prove production wiring. These runtime demonstrations complement, rather than replace, full domain/application scenario coverage.
- Document actual adapter settings and event semantics. A mocked repository or publisher proves only the tested application interaction, not real SQL/broker behavior.

## Runtime composition and lifecycle evidence

Apply [runtime-lifecycle.md](runtime-lifecycle.md) to the selected components. Provide finite `go test` harnesses for the following applicable scenarios; record a reason for branches that are not enabled. These are composition/lifecycle checks, separate from optional per-adapter unit coverage.

| Scenario | Required observation |
| --- | --- |
| Normal startup and feature flow | The executable's composition starts the selected entry points with their readiness contract satisfied, and the example API flow uses its assembled feature graph. |
| Partial startup failure | Fail later initialization/binding after an earlier acquisition; observe cleanup of owned acquisitions and any early-started work. Cover materially different reachable cleanup branches. |
| Startup cancellation | Cancel during pending initialization; verify cancellation/failure propagation and cleanup without subsequently reporting readiness or leaving owned work running. |
| Disabled component, when configurable | It opens no resource or listener; enabled dependent capabilities remain valid under the selected contract. |
| Fallback, when selected | The agreed replacement is usable and its mode is observable. A successfully initialized dependency still used by the graph remains open and usable when another dependency falls back. |
| Shutdown with active work | Use a controlled active request/job to verify the accepted drain/cancel behavior, rejection of new work, termination of owned work, closure of listeners/resources, and total elapsed shutdown time. Exercise the timeout/forced-stop path as well as graceful completion. |
| Unexpected server/worker exit | Its failure reaches the runtime's supervision path, produces the selected stop/degraded-mode outcome, and preserves the triggering error through cleanup. |
| Bootstrap, when required for an authorized feature | Initial data is usable through the composed API in every supported adapter mode exposing that feature. If authentication is enabled, health alone or a fixture-filled substitute router cannot establish login/bootstrap behavior. |

For RPC-only or worker entry points, use the corresponding local call/job probe; an outbound RPC client does not require an inbound RPC server or an HTTP health route. If multiple servers are enabled, verify they share the intended feature graph and all participate in shutdown.

Use controlled local resources or narrow dependency/lifecycle seams for deterministic failure injection while retaining the real composition path. Stand-ins can prove coordinator selection, ownership, and error propagation; they cannot establish an actual driver's cancellation, transaction, network, or close behavior. Real SQL/broker/upstream suites remain opt-in unless required by the accepted criteria. Document which claims need real-resource evidence; leave any required bound or behavior that cannot be established failed/blocked rather than inferring success from a stub.

## Local HTTP smoke: required for HTTP services

**Proposed execution path:** implement an integration smoke package invoked through `go test ./test/smoke/... -v`. Start the actual service composition with a local listener; this avoids the forbidden Go build/run verification commands.

The concrete bootstrap seam/package is still an implementation decision. The command above is a proposed shape, not an existing command supplied by the original boilerplate.

Required observations:

1. Use local test configuration and available enabled resources; set finite startup/request/shutdown timeouts and a usable port.
2. Start the real composition root, not a substitute health-only handler graph.
3. Request GET `/health` and assert HTTP 200, JSON Content-Type, `status: success`, `data` present, and `error` absent.
4. Prove the health endpoint requires no authentication. Include headers required by the actual target instructions when making local requests, and obtain their values if needed. Do not assume a project-specific identity-header scheme.
5. Cancel/shut down the runtime and assert that the listener/resources stop within the bound.

Health readiness covers only what its contract promises. It does not prove all business dependencies are available unless explicitly included in the health contract.

Keep health smoke evidence and business API evidence distinct, using the actual composition for both. Health alone does not complete the lifecycle scenarios above. Additional adapter unit tests are not automatically required. Optional real SQL/broker integration checks remain appropriate for behavior mocks cannot establish; their general optional status does not waive required composition/lifecycle checks or explicitly required real-resource evidence.

**Conditional active input/error paths:** verify malformed JSON, method/path handling, business errors, infrastructure errors, and any enabled middleware responses against the contract. Framework defaults alone are not evidence of envelope compliance.

## Failure and blocker handling

| Condition | Required response | Result status |
| --- | --- | --- |
| Missing implementation-determining input | Inspect available target facts, then ask a focused question; continue independent work. | Dependent stage pending. |
| Destination collides with user work | Inspect state and isolate changes; settle any unavoidable overwrite decision. | Conflicting mutation not performed. |
| Dependency API cannot be verified | Record version/symbol/source gap and obtain needed access. | Integration not standardized. |
| Shared helper/library violates a requirement | Record the gap; use an in-scope service adapter if sufficient, otherwise obtain a scoped decision for broader changes. | Affected path not passed. |
| Toolchain, network, tool, or permission prevents execution | Capture command, working directory, error, and missing prerequisite; follow the environment's access process. | Blocked/not run, not passed. |
| Required smoke resources unavailable | Specify the needed local resource/setup; preserve implementation work. | Affected runtime evidence remains unfinished. |
| Test fails twice without a clear cause | Stop speculative edits; report expected/actual observations and evidence. | Failed check, diagnosis pending. |
| Fix requires out-of-scope changes | Describe the minimum expansion and its reason; obtain a decision for that expansion only. | Partial result with explicit boundary. |

## Handoff and completion

Report worktree/branch, relevant changed files, enabled components, implementation choices, rule/scenario evidence, commands and outcomes, API/smoke results, and limitations. Distinguish passed, failed, not run/blocked, and not applicable.

Completion requires all acceptance criteria and required checks to pass. Conditional checks need passing evidence or a valid not-applicable reason. Commit/MR actions follow the user's authorization; packaging/publication/deployment remain separate workflows.

## Reference-set portability check

When maintaining the skill, validate that all local Markdown links resolve inside the skill root, including links between `SKILL.md` and `references/`. Copy the complete skill directory to an isolated temporary location and repeat link/navigation checks. Source audit URLs are optional provenance, while reading live target facts and selected dependency source remains part of execution.

Document portability checks establish packaging consistency. They do not establish service behavior or future skill quality; those require a later authorized execution exercise.
