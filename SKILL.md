---
name: gonesis
description: Build a Go service boilerplate with four root Clean Architecture layers and a tested Task Tracking reference feature. Use when creating a new Go service or initializing its foundation from user requirements, including requirement.txt. Existing-service feature tasks and releases use separate workflows.
---

# Gonesis — build a Go service boilerplate

Create a runnable service foundation and one working Task Tracking example, with configuration, logging, localized errors, tooling, and verification evidence. Follow the detailed stages and completion criteria in [workflow.md](references/workflow.md).

Resolve supporting paths relative to this `SKILL.md`. The `references/` directory contains the operational rules; this package requires no originating repository or pre-existing boilerplate. Inspect live target instructions, code, toolchain, dependency APIs, and available resources as execution facts.

## 1. Validate the user's requirements

Read [requirements.md](references/requirements.md) and the user's submitted `requirement.txt`, identified from their request or target project. Accept equivalent explicit requirements already supplied in the conversation; preserve subsequent user amendments.

Validate service identity and all five user-selected areas:

1. Persistence and restart/consistency behavior.
2. Internal event dispatch, publication point, failure semantics, and durability.
3. Time representation, precision, boundaries, and timestamp ownership.
4. API operations, payloads, identifiers, validation, and statuses.
5. Verification expectations, architecture constraints, resource availability, and limits.

The bundled [requirement.txt](references/requirement.txt) is an annotated template; [requirement.example.txt](references/requirement.example.txt) is an illustrative filled answer. Neither is the current user's selection unless they explicitly adopt it. Do not create the sample service simply because that example exists beside the skill.

If input is incomplete, discover available repository facts first, then ask focused questions for remaining implementation-determining choices. A blank, placeholder, or unresolved field is not permission to choose a default. Continue independent inspection/planning while dependent implementation waits.

The user chooses observable requirements; supply the formal API contract, concrete package/test paths, compatible library versions, and check commands yourself. Record the validated selections and enabled/unnecessary/unresolved components before their implementation.

## 2. Establish scope and workspace

Inspect the target's applicable instructions, Git status/diff, existing worktrees, destination, module files, contracts, and available tools. Explicit user directions govern; surface new material conflicts rather than silently overriding them with this skill.

For code changes, create or reuse a dedicated task worktree and preserve pre-existing user work. Apply [git-documentation.md](references/git-documentation.md) for branch, commit, documentation, and MR conventions. Settle an existing destination collision before changing affected files.

Retain these agreed workflow boundaries unless the user changes them:

- `domain/`, `application/`, `delivery/`, and `infrastructure/` live directly at the service root.
- Include the Task reference feature and its public domain/application tests; an empty business skeleton is insufficient.
- Use ordinary Go tooling. Packaging/image publication, provisioning, deployment, and additional business features are outside this initial workflow.
- Commit and MR creation follow the requested task scope; service implementation does not imply those actions.

Use the target's selected destination and module path. Discover any workspace and shared packages before relying on them.

## 3. Execute the staged workflow

Use [workflow.md](references/workflow.md) for stage dependencies, outputs, and completion gates. Read each supporting reference when its stage applies, rather than loading the whole package at once:

| Before this activity | Read and apply |
| --- | --- |
| Creating modules/packages or changing Go implementation | [service-layout.md](references/service-layout.md), [go-standards.md](references/go-standards.md) |
| Designing/implementing the mandatory business example | [example-task.md](references/example-task.md) |
| Selecting dependencies, configuring logging, or integrating library APIs | [libraries.md](references/libraries.md) |
| Defining API contracts, errors, localization, health, or handlers | [api-errors.md](references/api-errors.md) |
| Writing/editing tests, fixtures, mocks, or architecture checks | [testing.md](references/testing.md) |
| Implementing storage or internal completion events; adding SQL/migrations if selected | [persistence-events.md](references/persistence-events.md) |
| Writing business/API docs, configuring a worktree, or performing requested Git actions | [git-documentation.md](references/git-documentation.md) |
| Running final checks or handing off the service | [verification.md](references/verification.md) |

Set contracts before handlers and verify selected dependency APIs before integration. Source snapshots in the references are evidence about those versions, not universal pins or runtime proof.

Implement the example through TDD: demonstrate RED for missing public behavior, implement the minimum behavior, reach GREEN, then refactor. Preserve rule-to-test evidence for BR-01–BR-09 and all acceptance scenarios. Use controllable time and real runtime adapters; generated test mocks do not replace them.

Keep invariants in the domain, orchestration in application, transport translation in delivery, and external adapters in infrastructure. Wire the actual example and lifecycle in the composition root. Match persistence/event failure behavior to the validated requirements.

Apply the library policy conditionally: logmanager is required for logging; clientmanager is required for outbound HTTP when enabled; httpmanager and eventmanager are preferred when they fit. An internal domain event alone does not require a RabbitMQ dependency.

When using an available skeleton/shared helper, verify its real API and behavior. Supply a compliant service-local implementation when necessary; do not inherit missing imports, response-envelope gaps, stale translations, or executable placeholders from the original boilerplate.

## 4. Verify and hand off

Run [verification.md](references/verification.md) against the generated service and the validated input. Use `go test` for code verification, together with the service's lint/security commands and repeatable architecture checks. Demonstrate the real example API flow.

For HTTP services, local `/health` smoke and bounded shutdown must pass. Verify the standard JSON envelope rather than assuming framework defaults comply. A smoke harness started through `go test` is a proposed implementation path; supply the concrete harness and command instead of claiming one already exists.

If a required check cannot run, record its command, working directory, observed failure, and missing prerequisite. Keep the affected result unfinished. Follow the test rule that two failures without a clear cause stop speculative edits; continue only independent work while the blocker is resolved.

Return a concise handoff containing:

- Service/worktree location and branch, relevant changed artifacts, and accepted input choices.
- Enabled components, API/business documentation, and significant design/library decisions.
- Rule/scenario evidence, exact commands and results, architecture checks, example API results, and HTTP smoke results when applicable.
- Failed, blocked/not-run, or not-applicable checks and remaining limitations, clearly distinguished from passing checks.

Declare completion only when every acceptance criterion and required check passes; conditional checks need passing evidence or a valid not-applicable reason. Perform commit/MR actions only within the user's requested scope.
