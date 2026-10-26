# Reference business feature: Task Tracking

This is the complete business example required in the boilerplate. It demonstrates the architecture and TDD flow from domain behavior to an API. Implement it inside the selected service, independently of unrelated existing services.

## Purpose and users

Provide a simple way to record work, track its progress, and identify overdue work. The example addresses scattered work records, unclear progress, missing overdue indicators, and changes to completed work that would undermine trustworthy history.

There is one general role: a user managing tasks. Authentication, user ownership, and assignment are not part of this example.

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

## Implementation responsibilities

- Domain owns validity rules, state transitions, finality, overdue behavior, and the domain meaning of system timestamps/events.
- Application coordinates loading/saving through ports and publishing completion events under the selected failure semantics.
- Infrastructure supplies actual runtime storage and event adapters as needed; test mocks are separate.
- Delivery validates/translates transport input and maps application results to explicit response DTOs and the standard error envelope.
- The composition root connects this example to the real runtime.

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
