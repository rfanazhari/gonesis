# Persistence, SQL, and internal events

## Select persistence explicitly

The Task example requires a repository port and an actual runtime adapter that supports its capabilities. The storage medium has not been selected. State its lifecycle, data-retention behavior, and error/consistency behavior before implementation.

If the selected medium is in-memory, do not claim data survives process restart. If it is a database, include its configuration, connection lifecycle, schema, and relevant verification. Unit test mocks do not replace the runtime adapter.

**Conditional:** add database drivers/pools/migrations only when the selected storage requires them. Opening a connection does not itself justify creating a sample table. Keep infrastructure structs plain and expose their dependencies as fields.

## SQL implementation rules

- **Required when SQL is used:** raw SQL is the default. The source policy targets at least 70% raw SQL repository implementations; GORM is an exception, not a reason to add artificial repositories to satisfy a ratio.
- GORM is the allowed ORM. It may be used for queries joining at most two tables; queries joining more than two require raw SQL. Use raw SQL for complex subqueries, unions, calculations, and similar cases.
- Keep persistence models in infrastructure. Do not add `json` tags to those models or use them directly as API DTOs.
- Pass `context.Context` into every operation. Use context-aware query/exec APIs and GORM `WithContext` as appropriate.
- Parameterize query values, such as PostgreSQL `$1`, `$2`; never concatenate or format user-controlled values into SQL.
- Check query, scan, commit, rollback where relevant, and iteration errors such as `rows.Err()`; close owned resources.
- Prefer one joined query for a hierarchy and assemble it during scanning instead of issuing recursive N+1 queries.
- Configure connection pools and bounds appropriate to the selected workload.
- Select a driver compatible with the target database and project constraints; PostgreSQL pgx is one inspected option, not a required choice for every persistence medium.

## Schema conventions

| Element | Requirement |
| --- | --- |
| Table names | English, plural, snake_case; preserve established domain terms such as `ktp` where appropriate. |
| Many-to-many names | Double underscore between table names, such as `users__groups`. |
| Column names | snake_case. |
| Index names | snake_case base with `_INDEX` suffix; quote PostgreSQL names to preserve the uppercase suffix. |
| PostgreSQL primary keys | Integer, bigint, or UUID according to the model. |
| Other primary keys | Database-appropriate unsigned integer, integer/bigint, NanoID, or UUID under target rules. |
| Timestamps | `created_at` and `updated_at` required; `deleted_at` when soft deletion is needed. |
| Indexed columns | Foreign keys, unique columns, second identifiers, and supported text-search columns. |

Schema fields and repository statements must agree. Example identifiers such as `your_table` and an undefined `_id` primary key are not valid completed output.

## Migration artifacts

**Required when SQL schema changes:** use golang-migrate and provide both up/down files under `migrations/pgsql/` for PostgreSQL.

From the service root, the creation command has this form:

```sh
migrate create -ext sql -dir migrations/pgsql <description>
```

Names use the current `YYYYMMDDHHmmss_description.{up,down}.sql` timestamp, not an old copied timestamp or a placeholder. Use `date +%Y%m%d%H%M%S` when a timestamp must be generated explicitly.

Review reversibility, constraints, indexes, naming, and adapter/schema consistency. Verify real SQL behavior through a relevant optional integration check when mocks cannot establish it. Creating migration files does not authorize applying them to a remote database.

## Completion event

BR-09 requires the internal `TaskCompleted` event when completion succeeds. Domain events describe business facts; application handlers coordinate reactions; infrastructure supplies a transport adapter when one is needed.

Before implementing completion orchestration, specify:

- Which successful state/storage outcome makes the event eligible for publication.
- Whether publication is synchronous or asynchronous and how cancellation/lifetime is owned.
- What the caller observes if saving or dispatch fails, and what state has already changed.
- Whether retry, duplication, idempotency, or atomic persistence/publication guarantees are required.
- Which event fields and system-generated timestamps are part of the contract.

Those details are unresolved; consolidation must not silently choose an outbox, broker, delivery guarantee, or transaction boundary.

Rejected state transitions must not publish a successful completion event. Tests must verify the selected success/failure contract and keep event behavior outside direct coupling between unrelated business modules.

## Conditional transport library

`salt-pkg/eventmanager` is the preferred option when it fits the required mechanism, not a mandatory dependency for every domain event. The inspected version is a RabbitMQ adapter, not an assumed in-process bus.

If a broker is selected, verify configuration, context/tracing, cancellation, acknowledgement/retry behavior, delivery errors, and shutdown against the selected library version. Known API limitations are listed in [libraries.md](libraries.md).

Broker provisioning and deployment remain separate work. If required local resources are unavailable, report the affected verification as blocked rather than substituting a claim based on mocks.
