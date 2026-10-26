# Requirement file: fields and validation

The user supplies their choices through `requirement.txt` when invoking the skill. The input contract includes service identity and all five decision areas: persistence, internal events, time, API, and verification.

Use [requirement.txt](requirement.txt) as the annotated template. Its comment lines show possible answers. [requirement.example.txt](requirement.example.txt) is a consistent filled example, not a selected configuration or a workflow default.

## Submission and interpretation

- Replace each `<answer>` with an explicit selection, `none`, `not applicable` with a reason, or `unresolved`.
- The five decision areas must be answered by the user. Facts such as the existing module/toolchain and available commands may be discovered from the target repository and confirmed against the submission.
- Preserve existing user selections across the conversation; do not ask again when the answer is already available.
- Treat `#` lines as illustrative comments, not selected values. A template or sample file alone does not authorize its proposed settings or service creation.
- Treat relative target paths as relative to the identified target repository/worktree. Resolve the actual destination before changing files.
- Accept equivalent clear prose; this text format is a human-readable contract, not a strict parser/schema dependency.
- Keep secret values outside the file. Environment-variable names and resource requirements are sufficient input.

## Field definitions

| Area | Required meaning | Conditional detail |
| --- | --- | --- |
| Service | Name, purpose, destination/status, module path, and runtime. | Toolchain constraints, integration restrictions, ticket, and requested Git actions. |
| Persistence | Storage medium, retention/restart behavior, consistency, and failure expectations. | Driver, schema/migrations, and available database resources when a database is selected. |
| Internal events | Dispatch mechanism, publication point, event fields, save/publication failure behavior, and durability. | Retry, delivery, capacity, and lifecycle behavior needed by the chosen mechanism. |
| Time | Timezone/representation/precision, due-date boundaries, optional/cleared dates, and system timestamp ownership. | Ambiguous date-only versus instant behavior or API precision conversions. |
| API | Transport, operations/routes, identifiers/states, payload expectations, validation boundaries, success/error statuses, and health. | Existing consumer contracts or restrictions that the generated contract must preserve. |
| Verification | Business/API evidence, HTTP smoke/lifecycle expectations, architecture constraints, local resources, and limits. | Existing tool commands can be supplied but are not required user knowledge. |

The agent supplies the implementation plan, formal API documentation, test-package paths, compatible dependency choices, smoke harness, and repeatable architecture-check commands. Ask the user about observable requirements rather than requiring them to design these mechanics.

## Validation before dependent implementation

1. Check that identity and all five sections are present and have meaningful selections. A blank, `<answer>`, or `unresolved` is a pending decision, not a default.
2. Compare selections with the Task rules and workflow constraints. Preserve four root layers, the example feature, TDD, standard errors/translations, and required HTTP smoke unless the user explicitly changes scope.
3. Check cross-section consistency: storage retention versus durability promises; dispatch versus broker availability; save/event atomicity versus the selected runtime adapter; time precision versus comparisons and JSON; API states/errors versus business rules; verification expectations versus available resources.
4. Distinguish business decisions from discoverable repository facts and implementation choices. Discover the latter before requesting missing information.
5. Summarize accepted selections and ask focused questions only for missing/conflicting decisions that block the next work. Continue independent work where possible.
6. Implement only after the relevant decisions are settled. Revalidate affected requirements if a later choice changes the API, adapter, or verification plan.

Examples of blockers include requesting durable events with only volatile storage and no recovery mechanism, requiring a broker while forbidding every available broker resource, and selecting time boundaries that conflict with BR-03/BR-07. A proposed local resource in a sample is not evidence that it is available in the actual environment.

An incomplete file is not grounds to discard the request or silently choose alternatives. Report exactly which decision is missing and its implementation consequence.

## Evidence and maintenance

Keep the validated input and any subsequent user-approved amendments traceable in the implementation summary. Mark illustrative answers as examples when discussing them; do not report that the current user selected them.

Template/sample maintenance must keep section and field names aligned. Verify that filled examples answer every field without unresolved placeholders, and that every sample choice is consistent with the consolidated rules. These document checks do not establish runtime behavior.
