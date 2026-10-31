# Reference business feature: Task Tracking

This is the complete business example required in the boilerplate. It demonstrates the architecture and TDD flow from domain behavior to an API. Implement it inside the selected service, independently of unrelated existing services.

Use it as a worked reference for assigning responsibilities, protecting invariants and verifying behavior. Future features derive their own domain concepts, lifecycle and contracts from their accepted requirements; do not copy Task-specific rules or create extra features during boilerplate generation. Apply [design-assessment.md](design-assessment.md) before dependent tests/code and after GREEN. Business rules below define intent; the design guidance explains how to enforce and assess it.

## Purpose and users

Provide a simple way to record work, track its progress, and identify overdue work. The example addresses scattered work records, unclear progress, missing overdue indicators, and changes to completed work that would undermine trustworthy history.

There is one general role: a user managing tasks. Authentication, user ownership, and assignment are not part of this example.

## Work item and design references

For an actual implementation, record the real ticket ID supplied by the user or the authoritative work item in the target project. It links the accepted requirements, tactical/technical design, design assessment and verification evidence for that change. This reusable example has no assigned ticket; do not manufacture one from its BR IDs, repository name or an illustrative value.

Keep this compact record in existing task notes or the execution result, linking authoritative artifacts rather than duplicating them:

| Field | Record for the actual task |
| --- | --- |
| Ticket ID / source | Real work-item ID and source link/path when available. If not assigned, state `unassigned` and the missing source; do not report ticket traceability as complete. |
| Accepted requirements | Validated requirement input and amendments, affected BR-01–BR-09 rules and acceptance scenarios. |
| Tactical design | Section in the owning feature design document containing the accepted concept/ownership mapping and material refinements from this example. |
| Technical design | Section in the same document containing resolved use-case flows, contracts, packages, adapter/time decisions and test plan. |
| Design assessment | Section in the same document linking findings to their ticket, affected concept/contract, evidence, disposition and verified result or remaining decision. |

Use the ticket reference to connect design decisions and assessment results, including a justified no-change result. It is change metadata, separate from Task identity, service business-rule IDs and runtime request/correlation IDs. No new API field, database column or domain value object is implied. Ticket-dependent commit rules remain governed by [git-documentation.md](git-documentation.md); an unassigned ticket does not itself block independent design/code work under this workflow.

## Lifecycle

```text
Todo --Start--> In Progress --Complete--> Done
```

| State | Meaning |
| --- | --- |
| Todo | Recorded; work has not started. |
| In Progress | Work is underway. |
| Done | Completed and final. |

## Business rules

| Local ID | Required rule |
| --- | --- |
| BR-01 | A task must have a title. It cannot be empty or whitespace-only and is at most 100 characters. |
| BR-02 | A newly created task always starts as Todo. |
| BR-03 | A due date is optional. If provided, it cannot be in the past when the task is created or rescheduled. |
| BR-04 | A task can be started only from Todo. |
| BR-05 | A task can be completed only from In Progress. Todo cannot move directly to Done. |
| BR-06 | A Done task is final: it cannot be restarted, rescheduled, or modified. |
| BR-07 | A task is overdue when it has a due date, that date has passed, and its state is not Done. |
| BR-08 | Creation and completion times are recorded automatically by the system, never supplied by the user. |
| BR-09 | Completing a task publishes an internal `TaskCompleted` event so other modules can react without direct coupling. |

These local IDs identify the source example. When creating service business documentation, allocate the target's `BR-<SERVICE>-<NNN>` IDs and preserve a local-to-service mapping. Do not reuse IDs owned by an unrelated service.

## Capabilities

1. Create a task with a required title and an optional due date.
2. Start a task: Todo → In Progress.
3. Complete a task: In Progress → Done.
4. Reschedule a due date while the task is not Done.
5. View task details: state, due date, overdue flag, and completion time.

The API contract expresses these operations for the chosen runtime before handler implementation. The example's requirement is behavior through all applicable layers, not a particular preselected endpoint naming scheme.

## Acceptance scenarios

| Scenario | Expected outcome | Rules |
| --- | --- | --- |
| Create with title `Prepare report` and no due date | Saved as Todo. | BR-01, BR-02, BR-08 |
| Create with an empty title | Rejected with an invalid-title error. | BR-01 |
| Complete a Todo task | Rejected as an invalid transition. | BR-05 |
| Create → start → complete | Saved as Done with a system completion time and the internal completion event. | BR-02, BR-04, BR-05, BR-08, BR-09 |
| Modify a Done task | Rejected because the task is final. | BR-06 |
| Due date has passed and task is In Progress | Details identify it as overdue. | BR-07 |
| Due date has passed and task is Done | Details do not identify it as overdue. | BR-07 |
| Reschedule to a date in the past | Rejected. | BR-03 |
| Operate on a missing task | A not-found response according to the API contract. | Capability behavior |

For the overdue scenario, first create the task at a controlled time when its due date is valid, then advance time past it. Do not bypass BR-03 by creating an already-invalid task.

Complete coverage also exercises whitespace-only and overlong titles, invalid start/complete transitions, optional dates, system-owned timestamps, and dependency failure cases. Preserve the original scenarios when adding boundary cases.

## Tactical design

Before implementation, record classification, package location, ownership and public enforcement boundaries using the baseline below. Use [service-layout.md](service-layout.md) and [go-standards.md](go-standards.md) for structure. This is a concrete foundation for Task, not a universal type inventory for future features. Justify material internal refinements through design assessment; preserve accepted business rules and explicit constraints.

| Concept | Classification and owner | Responsibility and evidence |
| --- | --- | --- |
| Task | Aggregate root and entity with identity; owns its lifecycle and private state | Enforce creation as Todo, valid start/complete transitions and Done finality through public domain operations. A failed operation leaves state/timestamps unchanged. Covers BR-02, BR-04–BR-06, BR-08. |
| Title | Value object owned by Task; private immutable representation, value-based equality, no independent identity | Own required/non-whitespace content and the 100-character limit under selected counting semantics. Use validated construction such as `NewTitle`; Task rejects an invalid zero value too. Establish whitespace retention/normalization before tests encode expectations. Covers BR-01. |
| Due date | Optional time value held privately by Task; no dedicated value object in the baseline | Task validates against trusted current time on creation/rescheduling, owns whether rescheduling is allowed and combines date/state for overdue. Copy pointer-based input/output to protect owned state. Covers BR-03, BR-06, BR-07. |
| Task state | Lifecycle state controlled by Task | Represent Todo, In Progress and Done; prevent callers from substituting unchecked state changes for domain transitions. Unknown states from external data follow the accepted restoration/error contract. Covers BR-02, BR-04–BR-07. |
| Creation/completion times | System-owned facts recorded by Task using supplied trusted time | Callers cannot choose these through user payloads. Creation records creation time; successful completion records completion time. Preserve recorded facts during load. Covers BR-08. |
| TaskCompleted | Domain event returned by a successful Task completion operation; application owns dispatch orchestration | Task owns completion validity and event meaning. Return the event to application, which coordinates storage/publication through ports under selected semantics. No pending-event queue is needed on Task. Covers BR-09. |
| Task repository, event publisher and time source | Inner ports where needed; actual adapters outside domain | Expose operations needed by use cases. Keep storage models, dispatch technology and transport DTOs outside business policy. Verify application error/ordering behavior separately from domain validity. |

Task identity has stable entity meaning, but its format/generation remains a validated input decision. The example's BR IDs and any Git ticket ID are separate identifiers; neither defines a task's runtime identifier.

Task is the lifecycle consistency boundary for this example. Application loads/creates the aggregate, requests the domain operation, and coordinates persistence and any completion publication. The selected repository and event semantics determine ordering, failure results, durability and any transaction requirement; the aggregate boundary alone promises none of those mechanisms.

Keep business terms consistent across rules, domain operations, errors and documentation. Start and Complete are commands requesting transitions; TaskCompleted is a fact about a successful transition. Overdue is derived from date/state, not a fourth lifecycle state. No additional entity or domain service is justified by the current rules; introduce one only when a concrete responsibility cannot reasonably belong to Task or one of its values.

### Protect rules through actual public boundaries

Design public operations around create, start, complete, reschedule and view. Do not make application/delivery reconstruct their business predicates or perform unchecked field assignments instead. Transport validation may reject malformed input early; direct domain callers must still receive the required business-rule enforcement.

Task exposes operations such as `Start(now)`, `Complete(now)` and `Reschedule(dueDate, now)`, plus read accessors such as `State()`. Keep its invariant-bearing fields private. Follow the encapsulation/zero-value rules in [go-standards.md](go-standards.md#structs-and-constructors): callers must not mutate lifecycle through assignments, and unchecked Title zero values must not enter a valid Task. Transport DTOs remain separate public-field data structures.

Title demonstrates a dedicated value object because it owns intrinsic validity and value-based equality. Due-date acceptance depends on Task lifecycle and the operation's current time, so Task owns those checks. Future features choose representations from their own invariant ownership; not every string or timestamp needs a value object or many methods.

### Separate creation, restoration and observation

Provide separate domain creation and restoration paths, such as `NewTask(...)` and `RestoreTask(...)`. The repository maps stored data into a restoration input; restoration checks value validity and stored-state consistency under the accepted contract, preserving identity, lifecycle, dates and timestamps. It neither samples new creation/completion times nor emits a completion event. Keep its validated state private after reconstruction.

Creation/rescheduling validity is time-dependent; stored history is not a new creation request. A task created with a valid due date must remain loadable after that date passes so overdue can be calculated. Restoration validates stored consistency without reapplying creation-time due-date checks or normalizing history. Define malformed-storage handling without inventing a new product rule.

Observation calculates overdue from the selected time boundary and task state; it does not perform a lifecycle transition or rewrite stored timestamps. Keep normalization, precision and serialization consistent with the accepted time/API contracts. These checks protect existing rules rather than introducing automatic overdue transitions or notifications.

## Technical design

Resolve these mechanics from the validated requirements and the live target before dependent implementation. Record concrete package/test paths and chosen contracts in the technical design referenced by the work item. The following flows define responsibilities; they do not select transport routes, identifier formats, storage or dispatch defaults.

### Layer responsibilities and dependencies

| Layer | Responsibility for this example |
| --- | --- |
| Domain | Own Task, value validity, lifecycle/finality, overdue and domain meaning of timestamps/events. No HTTP, database or broker I/O. |
| Application | Implement the five use cases; coordinate domain operations, repository access, trusted time and publication through required ports. Preserve domain errors without reimplementing their predicates. |
| Delivery | Parse transport input into explicit command/query inputs, invoke application behavior and map results/errors into explicit response DTOs and the selected transport contract (the standard envelope for HTTP JSON). |
| Infrastructure | Implement actual storage/time/dispatch adapters and map persistence representations to domain state. Keep generated test mocks separate from runtime adapters. |
| Composition root | Assemble the feature once for enabled delivery/worker entry points; resource ownership, startup/fallback, supervision, and shutdown follow [runtime-lifecycle.md](runtime-lifecycle.md). |

Apply the four root layers under [service-layout.md](service-layout.md). Put port interfaces at the inner consumer/owner, with implementations outside; domain has no outward dependency. Verify exact library versions/APIs under [libraries.md](libraries.md) before adapter integration. Do not introduce pass-through services or interfaces without a caller need.

### Baseline feature packages

Use one struct per application operation, grouped by feature. Each operation owns only its required dependencies; for example, `Complete` needs the publisher while `Start` does not. Keep each struct and its execution method together; colocate external-package tests. Names below establish the reference organization, while runtime adapter details follow selected requirements.

```text
domain/
├── aggregate/task.go                 # Task, creation, restoration, operations
├── valueobject/title.go              # Title and its validating construction
├── enum/taskstate.go
├── event/taskcompleted.go
└── repository/task.go                # Task repository port
application/
├── usecase/taskusecase/
│   ├── create.go                     # Create struct and execution
│   ├── start.go                      # Start
│   ├── complete.go                   # Complete
│   └── reschedule.go                 # Reschedule
├── query/taskquery/detail.go         # Detail query struct and execution
├── dto/task.go                       # application inputs/results
└── service/
    ├── clock.go                      # application time-source port
    └── eventpublisher.go             # application publication port
delivery/http/handler/taskhandler/    # conditional: HTTP handlers and DTOs
infrastructure/
├── repository/taskrepository/        # selected storage adapter and mapping
└── service/                          # concrete clock and publisher adapters
```

Use cases and adapters use plain structs with public dependencies; business-validating constructors belong where actual validation is needed. The rest of the service, docs and tooling follow [service-layout.md](service-layout.md). Empty entity/domain-service packages are unnecessary for this example.

### Time and completion-event boundary

Inject a clock into application operations that need time. Sample one trusted `now` per operation and pass it to related domain validation/recording so they use the same instant. The domain does not depend on the clock interface or call `time.Now()`. Precision, representation and boundary semantics still follow the validated requirements.

Successful completion returns its domain event to application, conceptually `completed, err := task.Complete(now)`. A rejected transition returns an error without changing state/timestamps or producing a successful event. Application handles the returned fact according to the selected persistence/publication contract; producing it does not itself establish durable completion or successful dispatch. No event queue, broker call or publisher dependency belongs in Task.

### Use-case execution paths

| Use case | Application/domain flow | Result and side-effect boundary |
| --- | --- | --- |
| Create | Accept title/optional date; construct the Title value; obtain identity and trusted time under selected contracts; request domain creation; save through the repository. | Return the created task only under the agreed success contract; user input does not set state or system timestamps. |
| Start | Load by identity; translate absence to not found; request Task's start transition; save the accepted state. | Invalid transitions leave the task unchanged; propagate storage failure under the error contract. |
| Complete | Load; request the completion transition with trusted time and receive TaskCompleted; coordinate saving and publication in the agreed order. | Reject Todo/Done before successful-completion side effects. Record what the caller sees if save or publication fails and what state/event effects may already have occurred. |
| Reschedule | Load; request Task's reschedule operation with the candidate date and trusted time; save only an accepted change. | Apply Done finality and date rules; clearing a date follows its resolved contract. |
| View | Load; evaluate overdue using trusted observation time; map state and recorded facts into a read result. | No transition, save, timestamp rewrite or completion publication is triggered by reading. |

Define how repository reads/writes isolate mutable state. In particular, a loaded in-memory pointer must not leak a failed update into stored state before the selected save boundary. If concurrent mutation is in scope, resolve lost-update handling from the required consistency guarantees; do not infer a locking/versioning scheme from this example.

### Contracts and adapter decisions

Before tests/handlers encode these choices, record:

- Transport operations, request/response schemas, identifier representation, success/error statuses and not-found mapping under [api-errors.md](api-errors.md). Separate malformed transport input, domain rejection and infrastructure failures; keep error codes and EN/ID translations aligned.
- Time source ownership and sampling for each operation, timezone/precision, equality boundaries and serialization. Supply trusted time to domain behavior; do not read uncontrolled wall time inside rules.
- Repository lookup/save semantics, retention/restart behavior and restoration mapping under [persistence-events.md](persistence-events.md). If SQL is selected, define schema/constraints and migration/rollback paths. If memory is selected, document its lifetime and alias/copy behavior.
- TaskCompleted payload and publication point, save/publication failure ordering, durability, cancellation and shutdown behavior. Transaction, outbox and retry mechanisms require selected guarantees; do not silently add them.
- Concrete public domain/application tests for each rule/scenario, affected adapter/runtime checks and repeatable architecture checks under [testing.md](testing.md) and [verification.md](verification.md). Use real composition/adapters for the required API flow and HTTP smoke when applicable.

This technical design is ready when the selected flows have concrete contracts, implementation paths, resource prerequisites and evidence commands, with no unresolved choice blocking dependent behavior. Maintain tactical design, technical design and assessment in one owning feature document under [git-documentation.md](git-documentation.md#feature-design-documentation), with ticket/rule references and links to test evidence. Update affected sections for subsequent changes rather than creating a file per use case or test cycle.

## Design assessment after GREEN

Use the assessment procedure in [design-assessment.md](design-assessment.md#after-green-assess-the-resulting-design) on actual code, public callers and tests. For this example, examine whether:

- Domain operations protect validity, transitions and Done finality even when invoked without delivery/application validation.
- Title owns intrinsic validity; Task rejects invalid values and owns lifecycle-dependent due-date checks.
- Application orchestrates ports without owning lifecycle predicates; infrastructure performs technical mapping without redefining business policy.
- Runtime restoration and returned data preserve history and protect aggregate-owned values from unintended mutation.
- Repository/publisher interfaces fit real callers, and errors, timestamps and event behavior retain the selected contract after refactoring.

Record findings/dispositions and regression evidence, including a justified no-change outcome where appropriate. Select refactoring test paths under [testing.md](testing.md#assessment-selected-work). Passing rule tests or import checks alone does not establish that callers cannot bypass invariants.

For each material finding, record the ticket reference, affected tactical concept or technical contract, observation, proposed/selected action, preserved rules, disposition and test evidence. A refinement to package structure updates the technical mapping; a change to accepted business meaning needs a resolved requirement decision before implementation.

## Additional design regression evidence

Preserve all acceptance scenarios above. Add applicable public-behavior cases that exercise the chosen enforcement boundaries:

| Boundary | Required evidence |
| --- | --- |
| Title | Empty, whitespace-only, exact limit and over-limit values follow agreed counting/normalization rules; equality is value-based and direct aggregate construction/restoration rejects an invalid zero-value Title. |
| Due date | Absent, past, equality and future cases follow selected precision/boundary rules; clearing is tested only under its resolved contract. |
| Lifecycle/finality | Repeated start/complete, direct Todo → Done and rescheduling Done are rejected; failed operations preserve state and system facts. |
| Restoration | A saved valid task can be read after its due date passes; load preserves recorded facts and emits no fresh completion event. Invalid stored values/state follow the agreed error contract. |
| Mutable exposure | Where pointers/slices or mutable state cross public boundaries, caller mutations cannot silently change aggregate-owned state outside accepted operations. |
| Completion orchestration | Successful domain completion returns TaskCompleted with agreed facts; rejected transitions produce no successful event. Save/publication failures follow selected ordering/failure semantics without claiming unselected retry or exactly-once guarantees. |

Derive expected values from the agreed rules and explicit controlled times, not by calling the production policy to compute expectations. Exercise the new internal contract directly if assessment introduces one, while retaining end-to-end business regression coverage.

## Decisions required before dependent implementation

The example has not selected storage media, identifier representation, dispatch mechanism, persistence/event failure ordering, or concrete API payloads/routes. Detailed time precision/timezone/equality boundaries, title-length counting semantics, and whether an existing due date can be cleared must be settled if the implementation exposes those choices.

Record product decisions rather than treating an arbitrary implementation as the source of a new rule. Internal publication does not itself require RabbitMQ, cross-process delivery, an outbox, or an external notification integration.

## Deliberately excluded

Ownership/assignment, priorities, labels, comments, attachments, search/filtering, automatic reminders, and deletion are deferred. Add them only through a separate scoped requirement.

## Completion criteria

- Every BR-01–BR-09 rule has a test that first fails for missing behavior, then passes.
- All acceptance scenarios pass; domain/application behavior and example API execution have evidence.
- Repeatable architecture checks pass, with public domain tests demonstrating the rule ownership that import checks alone cannot prove.
- The example's structure can be reused for another feature without restructuring the service's four layers.
- Runtime configuration, enabled adapters, error translations, and example usage are documented.
- Initial concept/ownership mapping and post-GREEN assessment are recorded; selected refinements pass their regression checks and no deferred finding blocks the rules or acceptance scenarios.
- Tactical and technical design references, assessment dispositions and verification evidence share the actual ticket ID, or explicitly identify missing ticket traceability without inventing an identifier.
