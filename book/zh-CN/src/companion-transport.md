# Mensoria SQL v1 interface contract

> 说明性工程参考，保留英文原文。它不增加可执行语言能力；历史章节编号指原始设计资料集，而非本书规范章号。

**Status:** proposed, 2026-10-29; no endpoint is implemented by this contract. [Normative language authority](preface.md). [Architecture and delivery](companion-architecture.md). [Acceptance and task traceability](acceptance-scenarios.md).

## 1. Routing and identity

All proposed paths are relative to `/v1/projects/{project}/environments/{environment}`. They extend the existing Data, QueryExecutor, Schema and Operation services. They do not create another execution ledger. Existing JSON query and native management routes retain their contracts.

The transport authenticates an existing public data principal, or the existing Studio Member-to-data ticket bridge. It derives the physical target, incarnation and authorization context server-side. No caller-provided actor, native token, role, physical table, namespace or database is accepted. Studio retains its existing Cookie/CSRF/Origin obligations.

| Method/path | Request and response | Authorization / ownership |
| --- | --- | --- |
| GET `/sql/capabilities` | Current enabled profiles/features/types, limits, fingerprint | Authorized scoped metadata; no hidden resources |
| POST `/sql/validate` | SQL + parameter type declarations → artifact or diagnostic | Current metadata and referenced-resource rights; does not execute |
| POST `/sql/explain` | Artifact reference → sanitized logical plan | Same current metadata/plan authorization; never ANALYZE |
| POST `/sql/execute` | Artifact + typed values + limits + original key | Current data actions and admission; one statement |
| POST `/sql/transactions` | Array of W1 artifact/parameter/precondition items + original key | Existing atomic command executor; one request, one environment |
| POST `/sql/migrations/preview` | DDL + expected Schema/mapping revision → proposal | Existing SchemaAdmin and management scope |
| Existing management workflow | Explicit proposal application and status | Original maintenance lease/guard/operation; no generic SQL DDL execution |
| Existing operation lookup/cancel | Original operation/key and optional read cursor | Current scoped authorization; does not replay SQL |

The exact reuse of existing operation URLs must be confirmed when transport is implemented. No new `/sql/operations` ledger is permitted. DDL preview stores a proposal but does not modify a schema or enter maintenance.

## 2. Capabilities and catalog

Example discovery response, with deliberately disabled runtime status:

```json
{
  "language": "mensoria-sql",
  "language_version": "1",
  "design_revision": "2026-10-29",
  "compiler_fingerprint": null,
  "backend_profile": null,
  "profiles": {"R1": false, "W1": false, "R2": false, "M1": false, "X1": false, "P1": false},
  "features": [],
  "types": [],
  "limits": {},
  "status": "not_qualified"
}
```

A real enabled manifest must pin parser/compiler versions, native SDK/server/storage profile, Schema adapter version, supported syntax/functions/types, constraints, parameter/column codecs and enforcement modes. Environment capability/entitlement/Policy/readiness and budget gates all apply. Parser support alone cannot populate an enabled entry. Candidate numeric ceilings are in the language design; each effective enabled limit must have a numeric value and an enforcement declaration.

Virtual catalog columns in R1:

| Relation | Columns | Row scope |
| --- | --- | --- |
| `information_schema.tables` | `table_schema TEXT`, `table_name TEXT`, `table_type TEXT` | Only current authorized published logical SQL tables; type `BASE TABLE` |
| `information_schema.columns` | `table_schema TEXT`, `table_name TEXT`, `column_name TEXT`, `ordinal_position BIGINT`, `data_type TEXT`, `is_nullable TEXT` | Only authorized SQL-visible columns; ordinal is published binding order; nullable `YES`/`NO` |
| `mensoria.sql_capabilities` | `feature_name TEXT`, `enabled BOOLEAN`, `profile TEXT`, `language_version TEXT` | Public feature names with current scope-effective enablement |

These are a documented subset of metadata views, not full INFORMATION_SCHEMA or `pg_catalog`. They use the same R1 predicate/projection rules; no arbitrary schema navigation. Omit protected rows/columns rather than reveal their types, counts or names. Direct unauthorized/unknown resource references use the same public error. Capability absence is safe to disclose only at the public feature-name level.

## 3. Validation and artifacts

Example:

```json
{
  "language_version": "1",
  "profile": "R1",
  "sql": "SELECT id, title, revision FROM public.notes WHERE status = $1 ORDER BY id LIMIT 50",
  "parameter_types": [{"position": 1, "type": "text"}]
}
```

On successful validation, return an immutable `artifact_id`, `artifact_revision`, source digest, canonical typed IR digest, parameter declarations, ordered result columns, statement/effect class, logical resource dependencies, required capabilities and protected plan reference. Bind actor authorization context, scope/incarnation/security sequence, Schema/mapping revisions, compiler/profile fingerprint and expiry. A validation receipt grants no execution authority. Revalidation after a semantic edit creates a new artifact revision; an old artifact is not silently recompiled at execution.

`SqlTableBinding` records `collection_id`, `schema_revision`, `mapping_revision`, public SQL name, ordered column definitions, envelope/business mappings, nullability/type codecs, policy obligations and constraint-readiness references. The Schema service owns its published revision.

`SqlArtifact` is owned by the existing query application service. `SqlExecution` is an execution view referencing the existing Operation, artifact, typed-binding digest, effective limits, cursor/result references and publication outcome. It is not an independently writable commit status. Read cursor/result retention is protected and expires independently of permanent operation receipts; expiry does not undo writes.

Every execution loads the exact artifact and repeats current authorization and compatibility checks. Changed policy denies execution or requires revalidation; changed schema/compiler/profile/incarnation yields `SQL_ARTIFACT_STALE`. A plan cache hit does not skip these checks. Function/extension declarations are explicit capability dependencies.

## 4. Typed parameters and results

Execution request example (`Idempotency-Key` supplied as an HTTP header):

```json
{
  "artifact_id": "qa_example",
  "artifact_revision": 1,
  "parameters": [{"position": 1, "value": {"type": "text", "value": "published"}}],
  "page_size": 50,
  "limits": {"wait_timeout_ms": 2000},
  "after": null
}
```

The wait value above is a caller preference, not a physical execution deadline. Installation ceilings may reduce caller budgets but may not silently change SQL LIMIT or semantics. Required plan budgets are selected before execution and returned as effective limits. A malformed, wrong-type or over-budget request fails before admission to execution.

A completed read example:

```json
{
  "operation_id": "op_example",
  "outcome": "succeeded",
  "publication": "authorized",
  "columns": [
    {"ordinal": 1, "name": "id", "type": "text", "nullable": false},
    {"ordinal": 2, "name": "title", "type": "text", "nullable": false},
    {"ordinal": 3, "name": "revision", "type": "bigint", "nullable": false}
  ],
  "rows": [[{"type":"text","value":"n1"},{"type":"text","value":"Example"},{"type":"bigint","value":"7"}]],
  "affected_rows": null,
  "page": {"next_cursor": null, "result_complete": true, "consistency": "live_keyset", "incomplete_reason": null}
}
```

Rows are arrays in column ordinal order, so duplicate output labels do not lose values through JSON object key collisions. Duplicate labels remain allowed for reads; artifact/adapter consumers must use ordinals. Alias requirements may be imposed by a named client profile but cannot silently rename columns.

Wire scalar tags are `boolean`, `bigint`, `text`, R2-required `numeric`, and enabled optional `uuid`, `double`, `timestamptz`. The `json` tag is reserved for a future registered extension and remains nonexecutable in this draft. NUMERIC parameter/column type metadata must include `precision` and `scale`; numeric values use the declared scale and exact decimal spelling. SQL NULL is the standalone `null` tag. BIGINT and NUMERIC use exact strings. Finite doubles are JSON numbers; timestamps have offset/precision validation and canonical UTC output. A mismatched backend type produces a typed conversion error, not a lossy fallback. Do not accept raw SurrealDB tagged values as an escape hatch.

`result_complete=true` means the logical result, including its SQL LIMIT, has been fully delivered; a page with a continuation is not complete. Budget/deadline truncation sets false with a reason; it does not mint a continuation unless exact resumability is qualified. A completed empty result has columns and `rows: []`. No total count is invented from page length. `affected_rows` is an exact decimal BIGINT string for DML and null for SELECT.

All execute/transaction requests require an original idempotency key because execution ownership and cost accounting persist. Repeating a read key attaches to its existing execution/result; it is not a fresh query or guaranteed replayable snapshot. If results have expired, return `SQL_RESULT_EXPIRED`; a deliberate new read uses a new key. Cursor continuation refers to that execution and keeps its original expiry; do not start another execution per page.

Return HTTP 200 for a synchronously completed, publishable result and 202 for an accepted pending or unknown outcome with its original operation reference. Validate returns 200 or a typed error. Operation status and result access always require current authorization. Content suppression after a committed write does not turn the operation into a rollback. Backend transport loss does not remove the operation key or give a client permission to resend under a new key.

## 5. Atomic W1 request batches

```json
{
  "items": [
    {"artifact_id":"qa_update_a","artifact_revision":1,"parameters":[
      {"position":1,"value":{"type":"text","value":"Reviewed"}},
      {"position":2,"value":{"type":"text","value":"n1"}},
      {"position":3,"value":{"type":"bigint","value":"7"}}
    ],"require_affected_rows":1}
  ]
}
```

Each item refers to a W1 statement artifact. The example artifact must have parameter order `$1=title, $2=id, $3=revision`; it is illustrative and does not reuse a different example artifact. Maximum 16 items, same environment/incarnation, one mutation per target row. Only W1 DML and its RETURNING are allowed. Item order determines result-set order; intermediate results are not published before batch commit. No dependency on a value returned by another item in v1.

One original key covers the complete ordered item list, exact typed values, expected Schema/mapping and optional affected-row assertions. The executor stores ordered outcomes in the same transaction as the mutations and original receipt. A failed assertion aborts the batch with no published partial RETURNING rows. An uncertain commit returns the original operation as unknown; checking item 1 separately is not batch reconciliation.

## 6. Diagnostics

Public errors contain `code`, five-character `sqlstate`, sanitized `message`, optional source span, `phase`, `retry_hint` and, once accepted, `operation_id`. SQLSTATE-like categories improve client handling; they do not establish PostgreSQL wire compatibility. Do not return native query text, object existence details, invisible names, values, paths, tokens or backend stack traces.

| Code / SQLSTATE | Meaning | Action |
| --- | --- | --- |
| SQL_SYNTAX_ERROR / 42601 | Invalid token/statement shape | Edit query |
| SQL_FEATURE_UNSUPPORTED / 0A000 | Disabled construct/function/type/profile | Check capabilities |
| SQL_REFERENCE_DENIED / 42501 | Unknown or unauthorized resource/field | Check current scope and grants; no existence disclosure |
| SQL_TYPE_ERROR / 42804 | Incompatible parameter/expression/result type | Fix type declarations/data mapping |
| SQL_INVALID_TEXT_VALUE / 22018 | Text cannot be parsed as the declared scalar type | Correct the value |
| SQL_DIVISION_BY_ZERO / 22012 | Evaluated division by zero | Correct the expression/value |
| SQL_AMBIGUOUS_REFERENCE / 42702 | Multiple authorized name matches | Use a unique qualifier/alias |
| SQL_INVALID_GROUPING / 42803 | Aggregate location or grouping is invalid | Correct the grouping |
| SQL_KEY_CONFLICT / 23000 | Original key is bound to another request identity | Reconcile the original request; never overwrite it |
| SQL_VALUE_OUT_OF_RANGE / 22003 | Numeric overflow or precision loss | Change input/type |
| SQL_ARTIFACT_STALE / 55000 | Version/security/incarnation incompatible | Revalidate, do not silently recompile |
| SQL_WRITE_PRECONDITION_REQUIRED / 0A000 | Mandatory exact id/revision absent | Use W1 guard shape |
| SQL_PRECONDITION_FAILED / 40001 | Required row-match assertion failed | Reread visible state and deliberately prepare a new command |
| SQL_CONSTRAINT_CONFLICT / 23000 | Sanitized integrity violation | Correct input; no protected conflict detail |
| SQL_BUDGET_EXCEEDED / 54000 | A proven resource ceiling was exceeded | Reduce scope or request a qualified larger budget |
| SQL_CURSOR_INVALID / 24000 | Cursor expired or binding changed | Explicitly restart read |
| SQL_RESULT_EXPIRED / 55000 | Original execution result no longer retained | Deliberately issue a new read |
| SQL_OUTCOME_UNKNOWN / 08007 | Commit/operation outcome not confirmed | Reconcile original operation/key only |
| SQL_DEPENDENCY_UNAVAILABLE / 08006 | Dependency unavailable; no confirmed outcome implied | Follow operation reference if already accepted |
| SQL_CANCEL_PENDING / 57014 | Stop requested, not confirmed | Observe original operation |

`retry_hint` is one of `edit`, `revalidate`, `restart_read`, `reconcile_original`, `observe_original`, `none`; it never authorizes an automatic fresh-key write. If HTTP authorization prevents viewing an existing operation, return the existing sanitized authorization error, without revealing that operation's state.

## 7. Minimum release evidence

See SQL-A01–A16 in [the review](acceptance-scenarios.md). The release manifest ties each enabled feature to its exact test corpus, native backend configuration and compiler fingerprint. Record documentation, local checks, CI, driver tests and business acceptance separately. The current manifest remains `not_qualified`; no runtime corpus was executed in this design task.
