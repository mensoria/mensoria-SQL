# 14. Schema definition and migration

M1 parses DDL into proposals. Accepted forms are CREATE TABLE, ALTER TABLE ADD COLUMN, CREATE INDEX, DROP INDEX and DROP TABLE under §14's restricted grammar. Each item targets the current public schema, with expected schema/mapping metadata outside SQL. A successful preview creates a proposal, not a live database change.

<a id="n039"></a>

**N039.** Only the existing Schema service, under current SchemaAdmin and fenced maintenance authority, may apply a DDL proposal. Query execution MUST NOT install native schema or grant itself management credentials.

## 14.1 Columns and constraints

CREATE TABLE must contain exactly one `id TEXT PRIMARY KEY` column. PRIMARY KEY is allowed only on id, implies NOT NULL and cannot appear as a table-level constraint. Platform revision/timestamps are binding-managed; users cannot declare them as business columns. Other declared columns are nullable unless NOT NULL is specified. For newly created bindings, column order is id, revision, then created_at/updated_at when qualified, then business columns in declaration order excluding id. Existing bindings retain their explicitly published order; ADD COLUMN appends the new business column.

`schema.literal_default` permits `DEFAULT <literal>` or a CAST of a literal, checked once against the target type. Parameters, functions, SQL expressions, sequences, DEFAULT keywords in INSERT, generated columns and volatile defaults are deferred. Defaults apply on omitted INSERT columns; a SET assignment of NULL remains NULL.

<a id="n040"></a>

**N040.** An ADD COLUMN marked NOT NULL on a nonempty relation MUST have an explicit qualified default/backfill source and actual verification before publication. If the proposal language cannot express an adequate safe backfill, it MUST reject the proposal and require a separate reviewed Schema migration.

ADD COLUMN without a default exposes SQL NULL for every existing row and is allowed only for nullable columns (or a proven empty relation). ADD COLUMN with a qualified literal default must materialize that default for every existing row, nullable or not, before the new binding is published. A default does not dynamically replace absent/null values during later reads. All mutation paths must then obey the published omitted-value/default contract.

Logical indexes live in the current `public` schema, with index-name uniqueness across that environment's logical SQL tables. Each index binds exactly one table identity and its immutable column list/type mapping. CREATE uses create-if-absent name reservation; any current conflicting name gives sanitized SQL_CONSTRAINT_CONFLICT, without its owner/table details. A same-original-operation proposal retry reconciles its original name reservation. DROP resolves `public.index_name` (or its unqualified equivalent), requires management permission on its owning table and expected index/binding revision, and uses the same SQL_REFERENCE_DENIED for a missing or unauthorized name. Logical names never identify caller-chosen physical indexes.

CREATE INDEX creates a nonunique index proposal on explicitly named qualified scalar columns. Index method, physical name and readiness are adapter-owned; lack of a qualified mapping rejects the proposal. DROP INDEX/TABLE uses explicit current resource versions and destructive review; no CASCADE/IF EXISTS/IF NOT EXISTS fast path is defined.

UNIQUE, FOREIGN KEY, CHECK, deferrable constraints, constraint validation hints and cascading actions are deferred. No accepted native declaration may be advertised as SQL-enforced unless every write interface and direct native-writer boundary respects it. SQL-only validation does not prove a database-wide invariant.

## 14.2 Publication and failure

<a id="n041"></a>

**N041.** The migration MUST use preview → expected-version check → admission close/drain → expand/backfill → actual schema/data/index verification → CAS binding publish → current-watermark reopen. Partial, incompatible or unknown state MUST remain unreleased/BLOCKED pending original-operation reconciliation.

Index preparation/readiness and binding publication are distinct. Removal/contract must respect retained artifacts, versions and active owners. A destructive change cannot be rolled back merely by running an old binary. Recovery must requalify mappings and invalidate old-incarnation artifacts/cursors.
