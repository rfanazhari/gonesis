# Service layout and wiring

The layout retains four layers directly at the service root. The tree below defines the complete service structure and translation location.

## Directory structure

Paths below describe allowed locations. Create subdirectories/files when the example or an enabled component uses them; conditional paths are not mandatory empty scaffolding.

```text
<service>/
├── cmd/
│   ├── app/
│   │   ├── main.go
│   │   └── .env.example
│   └── migrate/                       # conditional: migration executable
├── domain/
│   ├── aggregate/
│   ├── entity/
│   ├── valueobject/
│   ├── enum/
│   ├── event/
│   ├── repository/                    # domain repository interfaces
│   └── service/
├── application/
│   ├── usecase/
│   ├── query/
│   ├── repository/                    # application-specific ports
│   ├── service/
│   ├── dto/
│   └── event/                         # application event handlers
├── delivery/
│   ├── http/                         # conditional: HTTP runtime
│   │   ├── handler/<domain>handler/
│   │   └── middleware/
│   └── rpc/                          # conditional: inbound RPC handlers
├── infrastructure/
│   ├── database/                     # conditional: database setup
│   ├── runtime/                      # composition, supervision, lifecycle
│   ├── repository/<x>repository/
│   │   └── model/                    # persistence models, when needed
│   └── service/                      # external clients/adapters
├── migrations/pgsql/                 # conditional: PostgreSQL schema
├── translations/
│   ├── errors.en.toml
│   └── errors.id.toml
├── pkg/errs/
│   └── codes.go
├── test/
│   ├── testdata/
│   │   └── testdata.go
│   └── infrastructure/               # conditional integration checks
├── docs/
│   ├── api/                          # contract, endpoint docs, changelog
│   └── design/<feature>.md            # default: one owning feature design doc
├── Makefile
├── .golangci.yml
├── .mockery.yml                      # conditional: mocks used by tests
├── sonar-project.properties          # conditional: target uses Sonar
├── go.mod
├── go.sum
└── AGENTS.md / CLAUDE.md              # follow target instruction conventions
```

The reference feature gives each of the four layers real responsibilities. Other unused subdirectories may remain absent. Git does not track empty directories; a short README can explain an otherwise empty structural directory when it is needed.

Use the concrete [Task feature package baseline](example-task.md#baseline-feature-packages) for this example: one struct per application operation grouped by feature, plus the detail query. Other features derive their own model and package needs from requirements and design assessment. Design-document locations follow [git-documentation.md](git-documentation.md#feature-design-documentation), reusing target conventions when present.

**Conditional:** gRPC/proto, CLI, web assets, or other package locations are added only for requested components. Packaging and deployment are outside the initial workflow.

## Module and dependency identity

- **Required:** use the actual agreed module path throughout imports and tooling; resolve skeleton names such as `boilerplate`, `goproject`, and `SERVICE` in runnable artifacts.
- Set the destination and module path from the validated user input and target conventions while retaining the same four root layers.
- Discover compatible Go/toolchain requirements from the target and dependency constraints; do not inherit a version pin from an unrelated project.
- **Conditional:** register a new module in an existing `go.work`. Standalone modules do not require a workspace file.
- Review `replace` paths against the actual filesystem and module graph. A relative replacement from the original boilerplate is not portable by default.

## Shared packages and standalone operation

The skill does not require a pre-existing shared `pkg` module or source boilerplate.

Before reusing a shared error, response, validation, or middleware package, inspect its exported API, import path, and behavior against these consolidated requirements. Use it only if available and compatible.

If it is absent or incompatible, provide the minimum service-local implementation under the appropriate layer or `pkg/errs`, preserving error classification, localization, envelope, and architecture behavior. Do not invent an import to a package that exists only in the original checkout. A broader shared-package change requires its own scope decision.

## Composition root

`cmd/app/main.go` is the process entry point. Keep signal handling, configuration/logging initialization, runtime invocation, and terminal error reporting thin. Put reusable composition and lifecycle coordination in `infrastructure/runtime/`, preserving applicable target conventions. Apply [runtime-lifecycle.md](runtime-lifecycle.md) before designing its dependency graph and lifecycle.

Keep business invariants inside domain behavior and application orchestration inside application packages. Wiring can use plain structs with public dependencies; it does not require infrastructure constructors.

Separate resource setup, feature wiring, and transport setup from the coordinator as their responsibilities grow. For example:

```text
infrastructure/runtime/
├── runtime.go       # startup order, supervision, shutdown coordination
├── resources.go     # shared resources and ownership
├── task.go          # Task adapters and application operation wiring
├── http.go          # conditional: HTTP server lifecycle
└── rpc.go           # conditional: RPC server lifecycle
```

These filenames illustrate responsibility boundaries, not a required file count. Colocate small cohesive wiring; split when it makes ownership and dependency assembly easier to follow. Create only enabled protocol files and use ordinary functions/plain structs before introducing shared lifecycle abstractions.

Outbound RPC clients live in infrastructure adapters, such as `infrastructure/service/`; their connection setup belongs to resource composition. Inbound RPC handlers live in delivery. HTTP and RPC entry points reuse feature assembly rather than each constructing a different application graph.

**Required:** expose the actual composition path for runtime verification. Smoke and business-flow harnesses use that path with explicit supported adapter/configuration selections; separate handler graphs do not establish composition correctness.

## Structural completion criteria

- Four layers are at the service root and subpackage paths match their responsibilities.
- Module/import/config identity is consistent and every enabled dependency resolves.
- The example has real domain/application/adapter/API wiring.
- Translation files have one authoritative location under `translations/`.
- Documentation and tooling describe the implemented layout; no executable placeholder or unused example integration remains.
