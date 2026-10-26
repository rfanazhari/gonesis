# TDD, test structure, and tooling

## Required coverage and TDD

Domain and application unit tests are required for the Task example. Every BR-01–BR-09 rule must have public-behavior coverage and RED/GREEN evidence. An empty suite is not an acceptable completion result.

Use the loop: select one scenario → write the test → demonstrate failure caused by missing behavior → implement the minimum behavior → pass → refactor while keeping tests green. A syntax/toolchain failure alone does not demonstrate the intended RED behavior.

Test public behavior; do not test private functions directly. Domain tests prove business invariants independently of HTTP/database adapters. Application tests prove orchestration, persistence/error behavior, and event dispatch through appropriate ports.

**Conditional:** unit tests in delivery/infrastructure are optional and preferably not added unless requested. Additional integration checks are appropriate when real SQL, transactions, constraints, or broker behavior cannot be established with mocks; they are not a required merge gate by default.

Keep optional real-resource suites opt-in through an explicit command or the target's supported test-tag convention so ordinary package checking does not unintentionally require Docker or remote resources.

The user explicitly requires local health smoke for HTTP services and a verifiable example API flow. Those runtime checks remain necessary even though ordinary adapter unit tests are optional.

## Before editing any test

1. Read the entire test file.
2. Identify the exact table field names and their order.
3. Read factory signatures used by the function/tests before calling them.
4. Use exact replacement or complete-block rewriting for Go edits; do not use regex-based shell editing.

## Table structure and assertions

- **Required:** use a slice of a named test-case struct type. The source's anonymous-struct illustration does not override its named-struct rule.
- Put `name string` first. Include `wantErr bool` if the function under test returns an error.
- Iterate with `tt`; use `t.Run(tt.name, ...)`.
- Use an external `_test` package and colocate unit test files with the package being tested.
- Use `github.com/stretchr/testify`: `assert` for nonfatal comparisons and `require` when continuing would be meaningless.
- Put expected before actual, for example `assert.Equal(t, tt.expected, result)`.
- Check specific errors with `assert.ErrorIs(t, err, expectedErr)`; use `require.Error` when only error presence is the prerequisite.
- Use equality assertions rather than `assert.True(t, a == b)`.

When adding/updating cases, rewrite the entire table block, preserving all existing cases unless removal is explicitly requested. Preserve field order and trailing commas after final field values and entries.

## Factories, fixtures, and mocks

- **Required:** construct tested business objects using appropriate existing factories/constructors rather than raw literals.
- If no suitable factory exists and a raw struct literal would be necessary, ask before introducing it under the recorded project rule. Do not add infrastructure constructors merely to satisfy a test convenience.
- Reuse suitable fixtures in `test/testdata/testdata.go`. Fixture functions returning pointers/slices/arrays should return fresh values to avoid shared mutable state between cases.
- Test-table entries remain named test-case values; the object-construction rule governs the objects being tested and their dependencies.
- **Required:** generate mocks with Mockery according to `.mockery.yml`; do not handwrite mocks.
- Generate only mocks needed by actual tests. Verify module/package paths, output names, package mode, and compatibility with the installed Mockery version.
- Include generated mocks with the eventual code change. Generated mocks are excluded from lint according to the target's configuration.
- A test mock is not the runtime repository/event adapter.

## Deterministic time and event behavior

Use controllable time in tests rather than sleeps or arbitrary wall-clock assumptions. Create a task with a valid future due date, then advance time beyond it to test overdue behavior.

Test accepted and rejected transitions, timestamp ownership, immutable Done behavior, not found, dependency errors, and `TaskCompleted` under the chosen dispatch contract. Rejected transitions must not publish a successful-completion event.

Persistence/dispatch semantics, time boundaries, and API field formats must be settled before tests encode a purported product decision. Keep unresolved choices explicit.

## Commands and sequencing

From the service module, run the specific test after every test edit:

```sh
go test ./path/to/package/... -v -run TestFunctionName
```

If it passes, run the full service unit suite through `make test` or its explicitly provided equivalent. Fix a failed test before moving to the next task. If it fails twice without a clear cause, stop speculative changes and report observed/expected behavior and evidence.

Tooling must also check all packages, since a domain/application-only suite does not compile every delivery/infrastructure/cmd package. Full verification commands are consolidated in [verification.md](verification.md).

## Coverage and architecture checks

- Use `coverage.out` and `coverage.html`; do not create ad hoc per-package report names.
- Coverage collection and Sonar coverage scope focus on domain/application. Configure Sonar only if the target uses it; set a real project key and exclude mocks, generated code, and test fixtures appropriately.
- **Required:** provide a repeatable Go-tooling architecture check for prohibited dependency directions and document its command.
- Check domain independence from delivery/infrastructure, application boundaries, and adapter/port organization.
- Use domain public-behavior tests as evidence of a rich domain. An import check alone cannot prove business rules reside in the domain.
- The source example mentions archtest, but no reusable archtest command was found in the inspected repository. Tool/package selection is unresolved; do not claim such a command already exists.

The future implementation must supply an applicable command and passing result. This consolidation introduces no executable test harness.
