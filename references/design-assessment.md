# Design assessment and justified refactoring

Read before implementing the reference feature or an agreed implementation slice. Confirm the design before dependent tests/code, assess the actual result after GREEN, and resolve findings before completion. For verification-only requests, preserve the requested scope. This reference owns design assessment and refinement authority; [testing.md](testing.md) owns test paths. Git actions remain conditional under [git-documentation.md](git-documentation.md).

## Before implementation: confirm the design

Reuse validated requirements, supplied technical designs and accepted decisions. Briefly map affected domain concepts, aggregate/lifecycle ownership, value rules, consistency rules, ports, preserved contracts and exclusions in the owning [feature design document](git-documentation.md#feature-design-documentation). Reference existing sections instead of reproducing them; a small slice may state “no domain-model changes” and identify its affected responsibility. Reuse the feature document rather than creating a document for each slice.

Compare this mapping with the actual code and governing instructions. The reference example supplies business intent and responsibility guidance, not an immutable inventory of files/types. Confirm that relevant invariants have an owner, scope and verification evidence are identified, and implementation-determining decisions are settled before dependent tests/code. Surface material conflicts and continue independent work.

Link the accepted requirements, tactical/technical mappings, findings and verification evidence through the actual ticket reference under [example-task.md](example-task.md#work-item-and-design-references). Preserve that reference through refinements. If unassigned, record the traceability gap without inventing an ID or turning it into a new implementation/commit gate.

## Authority to refine the design

| Decision | Execution authority |
| --- | --- |
| Business rules, accepted inputs, errors, lifecycle, consistency guarantees and compatibility | Preserve the accepted contract. Resolve changes before encoding them in tests/code. |
| Internal structure fulfilling those rules | Refine within scope with code/caller evidence, expected benefit and regression evidence. Record significant differences from the supplied design. |
| Explicit user or governing structural requirements | Honor them; surface conflicts before changing them. |
| Aggregate boundaries, transaction scope or consumers outside the authorized change | Identify the minimum required decision/scope; continue independent work. |

Retain compatible target conventions. Trace affected callers before changing an interface. A new file/package or directly affected caller may be justified by the responsibility; unrelated debt remains follow-up work. Assessment does not expand this boilerplate skill into a general existing-service feature workflow.

## After GREEN: assess the resulting design

Assess once per agreed implementation slice after verified GREEN, with a final review of the assembled feature. Do not repeat a full assessment per test. Revisit the initial mapping when findings materially change it. For assessment-selected restructuring, inspect the passing baseline before changes and reassess the final diff.

Inspect code, callers, tests and accepted design using **observation → design question → justified action → verification**.

| Observation | Question and possible action |
| --- | --- |
| Primitive represents a business concept | Does it own validation, normalization or equality rules? Consider a value object when it protects those rules and helps callers. |
| Rules spread across callers/layers | Who owns the rule? Put value validity in the appropriate domain concept and consistency/transitions in the aggregate. |
| Callers manipulate fields or orchestrate state transitions | Can they bypass invariants? Provide domain operations and reject invalid states at relevant public boundaries. |
| Duplication, large functions or mixed responsibilities | Is knowledge repeated or are unrelated reasons to change coupled? Extract only when clarity and locality improve. |
| Broad interface or pass-through abstraction | What do actual consumers need? Simplify or split when it reduces caller complexity. |
| Technical I/O mixed with business policy | Does a concrete need justify an inner port and an external adapter? |
| Naming conflicts with domain language | Can it be clarified while preserving contracts and callers? |
| Consistency enforced in several locations | Which aggregate owns it? Centralize enforcement without silently changing aggregate/transaction boundaries. |

Judge an anemic model by invariant ownership and bypass paths, not getter count or primitive storage. A value object may need only validated construction, immutable state and accessors. Apply [Go encapsulation rules](go-standards.md#structs-and-constructors), including private invariant-bearing state, zero-value rejection and protection against mutable aliases. A validating constructor or primitive alias alone does not protect invariants when callers can bypass it; identify and verify actual enforcement boundaries. Do not add wrappers, methods or patterns just to satisfy a checklist.

For each proposed change, establish:

1. The concrete problem and code/caller evidence.
2. The benefit to invariant ownership, callers or maintenance compared with retaining the design.
3. Preserved behavior and any new internal contract: accepted inputs, normalization, error identity/order/timing, state, timestamps, side effects, restoration and caller compatibility.
4. The appropriate path under [testing.md](testing.md#assessment-selected-work) and regression evidence. Use independently specified expected values for policy correctness; computing expectations with the production policy only proves integration with it.

Report findings as **refactored**, **retained with rationale**, or **deferred with reason and required decision/scope**. A brief overall no-change rationale suffices for a simple slice if it identifies what was assessed and why current ownership/structure is sufficient. Assessment does not require a refactor.

## Execute selected changes

Make small, coherent changes from a passing baseline; run affected tests after each step. Add characterization coverage first when existing coverage is insufficient. A failure requires diagnosis; repair or undo only that step while preserving user work. Keep the two-unexplained-failures rule under [verification.md](verification.md#failure-and-blocker-handling).

Check restoration explicitly when storage is enabled: trusted persisted state may legitimately bypass creation-time validation. Rejecting an elapsed due date during load, normalizing stored values or resetting timestamps may change behavior. Public renames and changed error timing also require compatibility assessment. Passing tests support only the behavior they cover.

## Completion and evidence

Assessment is complete when applicable concerns have been examined, each finding has a justified disposition, selected in-scope changes are verified, and no unresolved decision prevents acceptance criteria or governing contracts from being met. A deferred blocker leaves dependent work incomplete; unrelated improvements can remain follow-up work.

Keep the initial mapping, significant refinements, ticket-linked findings/dispositions, test paths and evidence together in the owning feature design document; link them from task notes or the handoff. Synchronize example/design/API/business documentation that became inaccurate under [git-documentation.md](git-documentation.md); preserve the boilerplate's required documentation scope.

Run applicable [verification.md](verification.md) checks on the final state. Reuse valid evidence for unchanged snapshots/scope; repeat affected checks after edits. Import checks and tests alone do not establish good domain modeling or complete behavioral equivalence. Use existing architecture tooling and conditional Sonar configuration; no new analysis framework or independent subagent is required.
