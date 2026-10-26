# Workflow: build a Go service boilerplate

Use the agreed scope, labels, and inputs in [README.md](README.md). The result includes the Task reference feature and evidence that it works.

Order: needs → isolated workspace → module/layout → foundations/contracts → TDD implementation/wiring → tooling/docs → verification/handoff.

Set the dependency version before using its API, the API contract before writing its handler, and the test scenarios before implementing their behavior. A later discovery that changes a contract or dependency returns work to the affected stage.

## 1. Establish needs and decisions

Dependency: the user request and read access to the target.

- **Required:** inspect target instructions, existing code/configuration, Git state, module files, and available tools. Use this reference set for consolidated workflow rules.
- **Required:** read the user's `requirement.txt` and validate identity plus all five decision areas using [requirements.md](requirements.md). Illustrative template/sample answers are not selected requirements.
- **Required:** identify every component as enabled, unnecessary, or unresolved; distinguish discovered facts from assumptions.
- **Required:** map the nine Task rules and acceptance scenarios to domain/application tests and API evidence. Settle storage, time, event, and API choices before dependent code.
- **Conditional:** obtain upstream contracts or target-specific business rules for an explicitly requested additional integration.
- **Required:** record conflicts, the governing decision, acceptance criteria, and verification commands.

Output: scope/component matrix, implementation decisions, rule-to-test map, artifact list, verification plan, and remaining questions.

Complete when service identity, destination, runtime, and the current implementation boundary are clear. Continue independent foundation work while a separate adapter decision is pending.

## 2. Prepare an isolated workspace

Dependency: destination and scope from stage 1.

- **Required for code implementation:** inspect status/diff and existing worktrees; create or reuse a dedicated task worktree with an appropriate branch.
- **Required:** preserve user changes and check for an existing service at the destination.
- **Conditional:** if the target exists, settle whether to extend its foundation or treat the request as a task on an existing service.
- **Conditional:** request access when the worktree destination is not writable.

Output: worktree location, branch, base revision, and pre-existing-change record.

Complete when code changes have an isolated location and no unresolved overwrite risk. Documentation consolidation itself does not create a service worktree.

## 3. Create the module and layout

Dependency: stages 1–2. Apply [service-layout.md](service-layout.md) and [go-standards.md](go-standards.md).

- **Required:** create the four root layers and the subdirectories required by the example and enabled components.
- **Required:** set the real module path/imports, compatible Go version, and only the dependencies actually used.
- **Required:** implement from these requirements; an available skeleton is optional input that must be inspected and adapted.
- **Conditional:** register the module in an existing `go.work`; review relative replacements and avoid unrelated module changes.
- **Recommended:** represent otherwise empty structural directories with short explanatory README files.

Output: consistent module identity, scoped directory tree, initial dependency list, and example package boundaries.

Complete when layer paths and dependency directions are correct, the identity has no unresolved placeholders, and each planned port/model/event has a concrete purpose.

## 4. Establish foundations and contracts

Dependency: stage 3 and verified APIs for selected dependencies.

- **Required:** document and validate enabled environment variables, including required values, formats, and defaults. Create a secret-free `.env.example`.
- **Required:** initialize JSON logging with the service identity, masking, context propagation, and startup failure reporting.
- **Required:** define service error codes, EN/ID translations, and safe transport mapping using [api-errors.md](api-errors.md).
- **Required:** establish the example API contract, repository/event ports, controllable time source, and business-rule documentation before their implementations.
- **Conditional HTTP:** establish GET `/health`, its standard envelope, lack of auth, and its limited readiness meaning.
- **Conditional:** define database connections, migrations, outbound clients, or broker configuration only for enabled requirements.
- **Required:** define startup cancellation, partial-startup cleanup, and shutdown for owned resources.

Output: contracts, foundation configuration, error catalog/localization, adapter decisions, and lifecycle plan.

Complete when wiring needs no hidden business/configuration decisions and selected library APIs have versioned evidence.

## 5. Implement the example and wire the runtime

Dependency: stage 4 contracts and the stage 1 test plan. Apply [example-task.md](example-task.md), [testing.md](testing.md), and relevant [persistence-events.md](persistence-events.md) rules.

- **Required:** implement one public scenario at a time: demonstrate RED for missing behavior, add the minimum implementation, reach GREEN, then refactor.
- **Required:** enforce title/date validity, lifecycle transitions, Done finality, overdue behavior, and system timestamps in the domain responsibilities. Application code orchestrates persistence and completion-event publication.
- **Required:** connect config → logging/i18n → resources → adapters → application → API/runtime in the composition root.
- **Required:** verify successful behavior, rejected rules, missing records, adapter failure, and the completion event through public interfaces.
- **Required:** log startup failures, close resources already opened, and implement bounded shutdown.
- **Conditional HTTP:** register health without auth; add only applicable middleware/CORS; adapt framework-generated responses to the agreed envelope.
- **Recommended:** keep `main` thin and make the real composition root reusable by a smoke harness.

Output: working reference feature, domain/application unit tests, RED/GREEN evidence, real adapters, runtime wiring, and cleanup.

Complete when every reference rule/scenario passes and the API invokes the real application behavior.

## 6. Complete tooling and documentation

Dependency: the actual packages and wiring from stages 3–5.

- **Required:** provide Go commands for all-package checking, domain/application tests, lint, security, architecture checks, and HTTP smoke when applicable.
- **Required:** verify command contents and tool versions; configuration presence alone is insufficient.
- **Conditional:** configure Mockery for interfaces used by tests and generate the required mocks.
- **Required:** provide repeatable dependency-direction checks and domain behavior evidence; document their commands.
- **Conditional:** configure Sonar if the target uses it; keep coverage focused on domain/application.
- **Required:** document environment setup, the example flow, verification commands, enabled components, and limitations using [git-documentation.md](git-documentation.md).

Output: working tooling, relevant generated artifacts, API/business documentation, and local usage instructions.

Complete when commands fit the actual structure and verification has no publication/deployment side effects.

## 7. Verify and hand off

Dependency: stages 1–6 and the local prerequisites for the required checks.

- **Required:** run [verification.md](verification.md), compare results with all reference rules/scenarios, and review the diff against scope.
- **Required:** demonstrate the example API flow; an HTTP service must also pass local health smoke and shutdown verification.
- **Required:** fix in-scope findings and rerun affected checks. Report blockers with evidence and preserve partial work.
- **Conditional:** commit or create an MR only within the user's requested scope.

Output: changed-file summary, rule/test evidence, command results, API/smoke evidence, decisions, and remaining limitations.

Complete only when all acceptance criteria and required checks pass. Conditional items need passing evidence or a reason they do not apply. Blocked required checks mean the result is unfinished.
