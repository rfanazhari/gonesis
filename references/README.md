# Go service boilerplate: consolidated references

Consolidated on 2026-10-27. This directory contains supporting references for [Gonesis](../SKILL.md), a self-contained Go service boilerplate skill. Creating these documents does not implement a service or establish runtime validation.

## Scope and agreed outcome

Produce a runnable Go service foundation with configuration, structured logging, error localization, one Task Tracking reference feature, and verification evidence. For HTTP services, a local `/health` smoke test must pass.

The four Clean Architecture layers live directly at the service root: `domain/`, `application/`, `delivery/`, and `infrastructure/`. Use ordinary Go tooling. Packaging, image publication, provisioning, deployment, and additional business features are outside this initial workflow. Commit and MR creation follow the user's requested scope.

The Task example is mandatory. It supersedes the earlier decision that an empty business foundation was sufficient. Its implementation demonstrates domain rules, application orchestration, infrastructure adapters, and delivery through an API.

## How to use this set

Start with [SKILL.md](../SKILL.md); use [workflow.md](workflow.md) for detailed stages. Read the topic references when the corresponding stage or component applies. All operational references are included in this package.

| Reference | When to read it | Contents |
| --- | --- | --- |
| [workflow.md](workflow.md) | Before starting implementation | Ordered stages, dependencies, outputs, completion criteria. |
| [requirements.md](requirements.md) | Before accepting user input | Field definitions, completeness/consistency checks, and clarification rules. |
| [requirement.txt](requirement.txt) | When preparing the user's submission | Annotated input template with illustrative answers for every field. |
| [requirement.example.txt](requirement.example.txt) | When a completed submission example is useful | Filled example; its choices are not workflow defaults. |
| [go-standards.md](go-standards.md) | Before designing or editing Go packages | Architecture, Go style, configuration, security, performance. |
| [service-layout.md](service-layout.md) | Before creating directories or wiring | Complete scoped layout, package responsibilities, standalone/workspace handling. |
| [api-errors.md](api-errors.md) | Before writing transport contracts or handlers | Contract-first workflow, JSON envelope, HTTP errors, localization, health. |
| [testing.md](testing.md) | Before writing/editing tests or configuring tools | TDD, table-driven tests, factories, Mockery, coverage, architecture checks. |
| [example-task.md](example-task.md) | When planning or implementing the required example | All nine rules, capabilities, acceptance scenarios, exclusions. |
| [persistence-events.md](persistence-events.md) | When selecting storage or implementing completion events | Persistence decisions, SQL/migrations, event semantics and boundaries. |
| [libraries.md](libraries.md) | When selecting or integrating a library | Required/preferred libraries, version verification, known API gaps. |
| [verification.md](verification.md) | Before accepting or handing off results | Commands, API demonstration, smoke, failure handling, completion report. |
| [git-documentation.md](git-documentation.md) | Before workspace changes, business docs, commits, or MRs | Worktrees, naming, documentation shape and rule IDs. |
| [sources.md](sources.md) | Only when auditing or maintaining these references | Dependency evidence, rule ownership, and maintenance notes. |

## Requirement labels and precedence

- **Required:** applies whenever its subject is in scope.
- **Recommended:** the initial choice; another choice needs a recorded reason.
- **Conditional:** required when the stated trigger is present; otherwise record not applicable.
- **Proposed / unresolved:** not an agreed default. Settle it before dependent implementation.

Explicit user directions govern this workflow. Inspect applicable instructions in the target repository and directories. Resolve a new material conflict explicitly rather than silently copying an older example.

The conventions in these references form the skill's implementation baseline. Applicable target instructions and explicit user requirements determine any necessary adaptations.

## Runtime discovery is still necessary

Inspect the actual target's instructions, Git state, module/toolchain, dependency versions, existing contracts, and available commands. That is discovery of live project facts, not a prerequisite chain through the original design documents.

Use the agreed destination and module path for the target. Both standalone modules and workspace members retain the same four root layers.

## Inputs and unresolved choices

The user provides the five decision areas through `requirement.txt`; use the annotated template and filled example above. Discover supporting project facts from the target repository. Ask only for missing information that determines implementation. Validation rules are consolidated in `requirements.md`.

| Input | Required before |
| --- | --- |
| Service name, purpose, destination, new/existing status | Workspace and package creation. |
| Module path and compatible Go toolchain | Dependency setup and package creation. |
| Process type: HTTP, worker, or combined | Runtime wiring and API verification planning. |
| Accepted example scope and any requested variation | Domain/API design; Task Tracking is the current reference. |
| Persistence choice and its runtime behavior | Repository adapter and any schema work. |
| Internal event dispatch and failure semantics | Completion persistence/publication orchestration. |
| Time representation, precision, timezone, and relevant boundaries | Due-date validation, overdue calculation, API fields. |
| API operations, payloads, statuses, identifier representation | Handler implementation. |
| User-selected verification expectations, architecture constraints, and available resources | Verification planning; the agent supplies concrete harnesses and commands. |

Persistence, internal dispatch, detailed time semantics, API requirements, and verification expectations are user inputs, not workflow defaults. The agent creates the formal contracts and concrete smoke/architecture harnesses from the validated selections. A proposed `go test` smoke harness is described in verification.

Optional inputs include a ticket, requested Git actions, dependency constraints, framework alternatives, timeouts, OTEL, CORS, external integrations, and additional runtime components. They become required information when an enabled component depends on them. Store secret values in the local environment.

The example excludes authentication and ownership. Health is unauthenticated. Add protected-route or tenant configuration only when the target requirements include it.

## Maintenance and packaging boundary

Keep each operational rule in its relevant topic file and use sibling links for navigation. Upstream URLs in `sources.md` are optional dependency audit information, not required reading instructions.

This set contains design rules and previously recorded source inspections. It does not claim that a service, copied boilerplate, library integration, or future skill has passed runtime validation. Validate those artifacts when their implementation is authorized.
