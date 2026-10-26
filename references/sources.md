# Dependency evidence and maintenance notes

This file is optional audit information for maintainers. Operational requirements are defined in the sibling references and the skill entry point; no originating repository or external design-document chain is required.

Reference consolidation date: 2026-10-27. Recorded dependency source inspections date from 2026-10-26. They establish version-specific API observations, not runtime behavior or universal dependency pins.

## Operational rule ownership

| Topic | Authoritative package reference |
| --- | --- |
| User input and the five selected decision areas | `requirements.md` and the requirement template/example. |
| Stage order, dependencies, and completion gates | `workflow.md`. |
| Architecture, Go style, configuration, security, and performance | `go-standards.md`. |
| Module identity, four root layers, and composition | `service-layout.md`. |
| Business behavior and acceptance scenarios | `example-task.md`. |
| API contracts, response envelope, safe errors, and localization | `api-errors.md`. |
| TDD, fixtures, generated mocks, and architecture checks | `testing.md`. |
| SQL/migrations and internal event requirements | `persistence-events.md`. |
| Library selection and version-sensitive APIs | `libraries.md`. |
| Runtime evidence, final checks, and blocker handling | `verification.md`. |
| Worktrees, conditional Git actions, and business-documentation shape | `git-documentation.md`. |

## Design decisions retained by this skill

- User-supplied requirements determine persistence, event dispatch, time, API, and verification selections. Example answers are not defaults.
- The service includes one Task Tracking reference feature with TDD and repeatable architecture evidence.
- Four Clean Architecture layers live directly at the service root; subdirectories follow actual needs.
- Ordinary Go tooling verifies the service. Packaging, publication, provisioning, and deployment are separate work.
- Responses include `status` and `data`; failures use `error`. Translation catalogs have one authoritative location under `translations/`.
- Domain/application unit tests are required. Other-layer unit tests are optional; HTTP services still require local health smoke.
- Applicable target instructions and explicit user directions govern repository-specific adaptations, including paths, headers, ticket identifiers, and hosting-provider commands.

## Compatibility pitfalls to check in reused code

- Placeholder module names and relative shared-module replacements must match the real target.
- Dependency direction follows architecture boundaries, not an inherited diagram or folder ordering.
- Startup logging, service identity, enabled adapters, configured pool settings, and cleanup must match the actual runtime.
- Required response fields must not disappear through serialization settings or framework defaults.
- Error producer, mapper, and both translation catalogs must agree on code keys.
- Schema definitions and repository statements must agree; migrations need valid keys, required fields, current timestamps, and paired up/down files.
- Mock generation, lint, test, and optional quality-analysis configuration must match the selected module and tools.

These checks apply when reusing a skeleton or shared helper. They do not require a particular source boilerplate to be available.

## Versioned upstream provenance

The following exact identifiers are dependency source references, not project branding:

- [httpmanager v0.16.11 source](https://github.com/SALT-Indonesia/salt-pkg/tree/httpmanager/v0.16.11/httpmanager).
- [clientmanager v0.10.1 source](https://github.com/SALT-Indonesia/salt-pkg/tree/clientmanager/v0.10.1/clientmanager).
- [logmanager v1.44.1 source](https://github.com/SALT-Indonesia/salt-pkg/tree/logmanager/v1.44.1/logmanager) and [v1.46.2 source](https://github.com/SALT-Indonesia/salt-pkg/tree/logmanager/v1.46.2/logmanager).
- Eventmanager tag `eventmanager/v0.2.5`, commit `c4c0d0afe1cd32904846c2de48c78e4b9d4472e2`: [handler](https://github.com/SALT-Indonesia/salt-pkg/blob/c4c0d0afe1cd32904846c2de48c78e4b9d4472e2/eventmanager/handler.go), [publisher](https://github.com/SALT-Indonesia/salt-pkg/blob/c4c0d0afe1cd32904846c2de48c78e4b9d4472e2/eventmanager/publish.go), [subscriber](https://github.com/SALT-Indonesia/salt-pkg/blob/c4c0d0afe1cd32904846c2de48c78e4b9d4472e2/eventmanager/subscribe.go).

The relevant findings are already summarized in `libraries.md`. Reverify the version selected for an actual implementation; these links and source inspections are not compilation or runtime proof.

## Maintenance rule

Edit a rule in its owning reference, update affected completion criteria, and review navigation when files move. Keep dependencies exact and project identity supplied by the target. Validate local links from an isolated copy of the entire skill root.
