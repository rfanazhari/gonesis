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
| Lifecycle | Startup failure cleans up opened resources; cancellation/shutdown completes within its bound. |
| Error/localization | Codes and EN/ID translations agree; technical causes remain internal; public responses use the required envelope. |
| All Go packages | Formatting is clean and `go test ./...` succeeds, including cmd/delivery/infrastructure compilation. |
| Domain/application suite | Specific edited tests and the full example unit suite pass. An empty suite does not pass. |
| Lint/security | The provided lint and vulnerability checks succeed with compatible tools. |
| Example API | The runtime's API demonstrates the agreed example behavior using real composition and adapters. |
| HTTP runtime | Local `/health` smoke passes, including JSON envelope and bounded shutdown. |
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
- Demonstrate create → start → complete → view through the actual API and a rejected direct Todo → Done transition. These runtime demonstrations complement, rather than replace, full domain/application scenario coverage.
- Document actual adapter settings and event semantics. A mocked repository or publisher proves only the tested application interaction, not real SQL/broker behavior.

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

Keep health smoke evidence and business API evidence distinct. Additional adapter unit tests are not automatically required. Optional real SQL/broker integration checks remain appropriate for behavior mocks cannot establish; their general optional status does not waive the explicitly required HTTP smoke.

**Conditional active input/error paths:** verify malformed JSON, method/path handling, business errors, infrastructure errors, and any enabled middleware responses against the contract. Framework defaults alone are not evidence of envelope compliance.

## Failure and blocker handling

| Condition | Required response | Result status |
| --- | --- | --- |
| Missing implementation-determining input | Inspect available target facts, then ask a focused question; continue independent work. | Dependent stage pending. |
| Destination collides with user work | Inspect state and isolate changes; settle any unavoidable overwrite decision. | Conflicting mutation not performed. |
| Dependency API cannot be verified | Record version/symbol/source gap and obtain needed access. | Integration not standardized. |
| Shared helper/library violates a requirement | Record the gap; use an in-scope service adapter if sufficient, otherwise obtain a scoped decision for broader changes. | Affected path not passed. |
| Toolchain, network, tool, or permission prevents execution | Capture command, working directory, error, and missing prerequisite; follow the environment's access process. | Blocked/not run, not passed. |
| Required smoke resources unavailable | Specify the needed local resource/setup; preserve implementation work. | HTTP boilerplate unfinished. |
| Test fails twice without a clear cause | Stop speculative edits; report expected/actual observations and evidence. | Failed check, diagnosis pending. |
| Fix requires out-of-scope changes | Describe the minimum expansion and its reason; obtain a decision for that expansion only. | Partial result with explicit boundary. |

## Handoff and completion

Report worktree/branch, relevant changed files, enabled components, implementation choices, rule/scenario evidence, commands and outcomes, API/smoke results, and limitations. Distinguish passed, failed, not run/blocked, and not applicable.

Completion requires all acceptance criteria and required checks to pass. Conditional checks need passing evidence or a valid not-applicable reason. Commit/MR actions follow the user's authorization; packaging/publication/deployment remain separate workflows.

## Reference-set portability check

When maintaining the skill, validate that all local Markdown links resolve inside the skill root, including links between `SKILL.md` and `references/`. Copy the complete skill directory to an isolated temporary location and repeat link/navigation checks. Source audit URLs are optional provenance, while reading live target facts and selected dependency source remains part of execution.

Document portability checks establish packaging consistency. They do not establish service behavior or future skill quality; those require a later authorized execution exercise.
