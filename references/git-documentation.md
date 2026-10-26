# Git workflow and documentation artifacts

## Workspace and authorization

**Required for service code changes:** inspect Git status/diff, preserve user changes, and work in a dedicated task worktree. Reuse a suitable existing task worktree when appropriate.

A worktree command has this shape:

```sh
git worktree add ../<repository>-<short-description> -b <type>/<short-description>
```

Adapt the worktree path to the target repository/location. If it requires filesystem permission, use the environment's approval mechanism. A request to prepare code does not automatically request commit, MR, publication, or deployment.

Branches use `<type>/<short-description>`, with a kebab-case description. Types are `feat`, `fix`, `test`, `refactor`, `chore`, `ci`, and `docs`.

## Commits and MRs: conditional on requested scope

Follow the target repository's commit convention. If it uses author/ticket/service brackets, the format is:

```text
<type>: [<author>][<ticket>][<service>] <description>
```

- When the target commit convention includes an author, obtain it from `git config user.name`.
- Include the service bracket when the change touches a service. Brackets have no intervening spaces.
- Use a lowercase imperative description without a trailing period. Keep one logical change per commit.
- Use a real ticket when supplied; follow the target convention for its absence rather than inventing a project-specific ticket. A missing ticket does not block implementation when no commit was requested.
- Include generated mocks and relevant configuration/artifacts in the eventual code change.

For an explicitly requested pull/merge request, discover the target hosting provider, CLI, base branch, and repository conventions. Prepare and inspect the request using the applicable tooling; do not assume a particular provider or branch name.

Post-merge cleanup removes the task worktree and local branch and updates the main checkout when that lifecycle action is in scope and safe for the user's working state. It is not part of initial boilerplate verification.

## Service usage and API documentation

Provide a service README explaining enabled components, environment variables and required/default/format behavior, local prerequisites, verification commands, the Task example flow, and limitations.

Document API contracts before handler implementation. Keep specification, endpoint docs, and changelog in the established target location, defaulting to service-local `docs/api/`. Published breaking changes require a new endpoint version.

Keep technical material such as payloads, SQL schema, and Go signatures out of business-rule prose. Store it in the API/schema/design documentation appropriate to the target.

## Business documentation layout and identifiers

When the target has no established business-documentation location, use this structure under its agreed documentation root:

```text
docs/services/<service>/business/
├── README.md
├── glossary.md                      # only for service-specific terms
├── capabilities/<capability>.md
└── policies/<policy>.md
```

Where a cross-service documentation index exists, register the service there. Use a maximum depth of two below `business/`, no subfolders under `capabilities/`, README indexes for created folders, and kebab-case capability-based filenames.

Adapt the documentation root to the selected repository while preserving the rule format and shape below.

- Allocate sequential `BR-<SERVICE>-<NNN>` IDs from the service index. Never reuse or renumber them.
- Define each ID under exactly one `###` rule heading in one file. Retired rules retain their IDs and refer to their successor when applicable.
- Map the example's local BR-01–BR-09 IDs to the allocated service IDs; preserve namespaces already owned by other services.
- Keep capability/policy files at or below 200 lines where possible; 300 is the hard cap. Split by capability when necessary.
- Keep the service business index at or below 80 lines where possible, with a 120-line hard cap. General Markdown references target about 150 lines per focused file.

## Required capability/policy shape

Front matter contains `id`, `service`, `status`, `rules`, `updated`, and `implementation`. Implementation entries identify the packages that actually enforce the rules.

Allowed statuses: `planned`, `partial`, `implemented`, and `retired`. A design-only example is planned until verified implementation exists.

Preserve these headings in this order:

1. Purpose
2. Ubiquitous language
3. Actors and triggers
4. Rules
5. Edge cases
6. Examples
7. Known gaps
8. Open questions
9. Related

Under Rules, each `### BR-<SERVICE>-<NNN> — <statement>` includes **Given**, **When**, **Then**, and **Why**. Use present-tense business vocabulary and concrete limits. The reason for the rule must be explicit.

Keep Known gaps and Open questions even when empty; write `None.` when appropriate. For unresolved questions, identify who must decide. Related includes implementation, API contract, sibling capabilities, and source references where applicable.

Behavior changes update matching business docs in the same change/MR. Compare the implementation with the intended rule; record deviations and consequences under Known gaps rather than deleting the agreed requirement or pretending it is implemented.

## Cross-service journeys: conditional

A single-service Task example does not require a cross-service journey. If a requested flow spans services, use the target's journey location, defaulting to `docs/business/journeys/` with `UJ-<NNN>` IDs. Journeys cite business rules instead of restating them.

Journey front matter contains `id`, `persona`, `goal`, `services`, `status`, `rules`, and `updated`. Headings are Goal, Persona, Preconditions, Steps, Alternate and failure paths, Outcome, Where this breaks today, and Related. Steps identify actor, service, effect, and cited rules; gaps link back to owning capability gaps.
