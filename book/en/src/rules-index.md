# Normative rule index

This index is a lookup aid; linked chapter text is authoritative.

| Rule | Requirement opening |
| --- | --- |
| [N001](01-purpose.md#n001) | In this document, MUST/SHALL express a requirement; MUST NOT/SHALL NOT express a prohibition; SHOULD expresses a recommendation requiring a documented reason for deviation; MAY expresses an option. |
| [N002](01-purpose.md#n002) | This draft is the language authority. |
| [N003](01-purpose.md#n003) | No implementation may claim complete ISO SQL, complete PostgreSQL, JDBC/ODBC, ORM, BI-tool or PostgreSQL wire compatibility from this draft. |
| [N004](02-profiles.md#n004) | Profile enablement MUST be scoped, versioned and backed by evidence. |
| [N005](02-profiles.md#n005) | A statement requiring multiple features MUST satisfy their union, including type and operator dependencies. |
| [N006](02-profiles.md#n006) | An implementation MAY expose separately named preview features before a complete profile qualifies, but MUST NOT advertise that profile as enabled. |
| [N007](03-database-model.md#n007) | One execution MUST bind to one server-derived scope and incarnation. |
| [N008](03-database-model.md#n008) | A logical table MUST map to a published collection binding containing its logical identity, SchemaRevision, mapping revision, ordered columns, types, nullability, source mappings and policy obligations. |
| [N009](03-database-model.md#n009) | New SQL bindings MUST reserve `id`, `revision`, `created_at` and `updated_at` against business-column collisions. |
| [N010](03-database-model.md#n010) | Name resolution MUST use authorized catalog metadata. |
| [N011](04-lexical-structure.md#n011) | SQL source MUST be valid UTF-8, without U+0000 or a byte-order mark. |
| [N012](04-lexical-structure.md#n012) | Normal execution MUST accept exactly one parsed statement plus at most one trailing semicolon. |
| [N013](05-data-types.md#n013) | A scalar value MUST have one declared logical type or be SQL NULL of a known contextual type. |
| [N014](05-data-types.md#n014) | Authorized absent optional business fields and explicit stored nulls MUST both map to SQL NULL in the relational view. |
| [N015](05-data-types.md#n015) | JSON is not a core v1 type. |
| [N016](06-type-resolution.md#n016) | Repeated occurrences of a parameter MUST resolve to a single declared type. |
| [N017](06-type-resolution.md#n017) | CAST MUST either produce the specified type exactly, except explicitly defined floating conversion, or report a typed error. |
| [N018](07-expressions.md#n018) | WHERE, ON, HAVING and searched CASE conditions MUST be BOOLEAN. |
| [N019](07-expressions.md#n019) | Boolean evaluation order is not a user-visible short-circuit guarantee. |
| [N020](07-expressions.md#n020) | For scalar expressions, an unchosen CASE result and COALESCE arguments after the chosen value MUST NOT raise a runtime value error. |
| [N021](08-select.md#n021) | SELECT MUST behave as: bind and authorize relations/columns → obtain qualified input view → apply per-relation row policy → FROM/JOIN → WHERE → GROUP/aggregate when present → HAVING → projection → DISTINCT → ORDER BY → logical LIMIT/FETCH → authorized publication. |
| [N022](08-select.md#n022) | Default SELECT ALL MUST preserve duplicate projected rows. |
| [N023](08-select.md#n023) | Every nullable order key, including one made nullable by LEFT JOIN, MUST require `read.nullable_order`. |
| [N024](08-select.md#n024) | Missing LIMIT MUST mean the entire logical result subject to explicit resource enforcement, not an undocumented default LIMIT. |
| [N025](09-joins.md#n025) | ON MUST be a nonempty conjunction of typed equalities, each comparing a column from the left relation with a column from the right relation. |
| [N026](09-joins.md#n026) | Both input relations MUST be read from one qualified consistent view; joining independent live paginated API results is prohibited. |
| [N027](10-aggregates.md#n027) | In a grouped query, every nonaggregate column reference in SELECT/HAVING/ORDER BY MUST be a GROUP BY key. |
| [N028](10-aggregates.md#n028) | Aggregates except COUNT(*) MUST ignore SQL NULL inputs. |
| [N029](11-optional-relational.md#n029) | A CTE MUST preserve bag, NULL, type, lineage and authorized consistent-view semantics. |
| [N030](11-optional-relational.md#n030) | UNION ALL branches MUST share the statement's qualified consistent view and authorization lineage. |
| [N031](12-data-modification.md#n031) | W1 MUST compile into existing scoped typed commands and one native transaction with the original Operation/Outbox/guard obligations. |
| [N032](12-data-modification.md#n032) | INSERT MUST commit a row at revision 1 and return affected_rows=1 when successful. |
| [N033](12-data-modification.md#n033) | UPDATE/DELETE MUST have a WHERE predicate that is a conjunction of atomic comparisons/NULL tests with mandatory exact `id = value` and `revision = value` terms. |
| [N034](12-data-modification.md#n034) | An ordinary no-match UPDATE/DELETE MUST produce affected_rows=0 and an empty RETURNING row set, uniformly for absent, invisible, revision-mismatched or additional-condition-mismatched targets. |
| [N035](12-data-modification.md#n035) | A committed write whose RETURNING content cannot currently be published MUST retain its committed operation outcome. |
| [N036](13-transactions.md#n036) | The transaction MUST atomically validate current native actor/session/family, schema/mapping, record guards and admission obligations, then commit business changes, ordered per-item outcomes, the original Operation receipt and Outbox records together. |
| [N037](13-transactions.md#n037) | Every accepted execution MUST have one original idempotency key bound to its actor, scope/incarnation, language/compiler/profile fingerprint, canonical typed IR, typed values, expected revisions and ordered batch assertions. |
| [N038](13-transactions.md#n038) | A lost reply, deadline, disconnected client, missing observation or cancel request MUST NOT be interpreted as rollback, failure, physical completion or permission to issue a fresh-key mutation. |
| [N039](14-schema-migrations.md#n039) | Only the existing Schema service, under current SchemaAdmin and fenced maintenance authority, may apply a DDL proposal. |
| [N040](14-schema-migrations.md#n040) | An ADD COLUMN marked NOT NULL on a nonempty relation MUST have an explicit qualified default/backfill source and actual verification before publication. |
| [N041](14-schema-migrations.md#n041) | The migration MUST use preview → expected-version check → admission close/drain → expand/backfill → actual schema/data/index verification → CAS binding publish → current-watermark reopen. |
| [N042](15-catalog.md#n042) | Catalog data MUST be generated from currently authorized published bindings, never from a privileged native schema dump. |
| [N043](16-artifacts-explain.md#n043) | Validation MUST parse, exhaustively inspect AST nodes, resolve authorized metadata, bind types/nullability/effects, enforce feature/size/budget planning gates and record immutable dependency revisions. |
| [N044](16-artifacts-explain.md#n044) | Execution MUST load the exact artifact revision and recheck current authorization and compatibility before backend access and again before publication. |
| [N045](17-parameters-results-pagination.md#n045) | Parameters MUST bind scalar values, never identifiers, keywords, directions, expressions, scope or executable fragments. |
| [N046](17-parameters-results-pagination.md#n046) | Transport page_size MUST NOT change SQL LIMIT. |
| [N047](17-parameters-results-pagination.md#n047) | Cursors MUST bind actor/authorization, query/artifact/typed-bindings digest, versions, scope/incarnation/security sequence, sort state, remaining cap and original expiry. |
| [N048](17-parameters-results-pagination.md#n048) | A response MUST distinguish a complete logical result, a normal partial page with continuation, and an incomplete result caused by budget/deadline/error. |
| [N049](18-diagnostics.md#n049) | Errors MUST contain a stable Mensoria code, five-character SQLSTATE-style category, sanitized message, phase, retry hint and original operation reference when already accepted and currently observable. |
| [N050](19-budgets-cancellation.md#n050) | An enabled implementation MUST enforce and advertise bounds for source/body size, AST nodes/depth, result columns/page bytes, row mutations, execution ownership, concurrency and every physical-work/intermediate resource used by its plans. |
| [N051](19-budgets-cancellation.md#n051) | The service MUST distinguish client wait timeout, execution deadline, cancel intent, confirmed worker completion and confirmed commit outcome. |
| [N052](20-authorization-audit.md#n052) | SQL MUST reuse native row/field authorization, scoped Control admission and current session/family checks. |
| [N053](20-authorization-audit.md#n053) | All reads of plans, history, metadata, cached results, artifacts, cursors and original-operation results MUST reauthorize currently protected content. |
| [N054](20-authorization-audit.md#n054) | Audit MUST correlate actor/scope, artifact/compiler/profile/schema versions, redacted query shape and typed-value digests, original operation, security/incarnation watermarks, consumed budgets, outcome and publication state. |
| [N055](21-extensions.md#n055) | A language extension MUST register a stable `mensoria` namespace, exact syntax/signatures, parameter/result codecs, NULL behavior, determinism/effects, scope/lineage, limits, index readiness, evidence and versioning before its parser/executor can accept it. |
| [N056](21-extensions.md#n056) | External model calls, embeddings, HTTP/file access, object uploads and job scheduling MUST NOT occur as hidden SQL transaction effects. |
| [N057](22-compatibility.md#n057) | Every accepted artifact MUST bind language version, draft/semantic revision, compiler fingerprint, enabled feature set and schema adapter/backend profile. |
| [N058](22-compatibility.md#n058) | SQL compatibility, native SurrealQL compatibility, PostgreSQL wire compatibility and named client compatibility MUST be reported separately. |
| [N059](23-conformance.md#n059) | Feature qualification MUST freeze source/build/compiler/parser/backend/storage settings, fixture schema/policies/data, capability limits and complete expected/actual typed results. |
| [N060](23-conformance.md#n060) | Documentation checks, local parser/runtime tests, CI, driver qualification, real customer acceptance and production qualification MUST be recorded independently. |
