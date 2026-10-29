# 资格验证场景（英文工程参考）

以下导入场景规定未来运行时验收，不是已观察结果。工程场景保留英文，历史任务编号仅用作追踪标签。

## 2. Future semantic, isolation and fault corpus

All cases below are **not run for SQL**. Expected behavior is a requirement, not an observed result. Enable only profiles whose cases and prerequisites have actual evidence.

| ID | Scenario and fixed input | Required result / rejection |
| --- | --- | --- |
| SQL-A01 | Comments, quoted names, multistatement text, nested denied node, unknown parser variant, SELECT with effectful function | Exact allowed AST or rejection before any backend execution; no native-text fallback |
| SQL-A02 | Logical rows with optional x absent, explicit NULL and x=1; protected x in separate restricted-role fixture | `IS NULL` selects first two authorized rows; `x = NULL` selects none; protected reference is denied rather than NULL |
| SQL-A03 | TRUE/FALSE/UNKNOWN expressions; `2 NOT IN (1,NULL)`; empty IN; explicit CAST | SQL truth table; UNKNOWN not selected; empty IN rejected; unsupported cast rejected |
| SQL-A04 | int64 max, overflow, exact decimal beyond binary64 precision, timestamp offsets, repeated output labels | Exact enabled codecs/ordinals or explicit type/range error; disabled types rejected |
| SQL-A05 | R2 duplicate tuples, NULL join keys, LEFT JOIN unmatched row, COUNT of empty input, NULL grouping | Correct bag/NULL/grouping semantics; no post-aggregate authorization filtering |
| SQL-A06 | Hidden field in WHERE/ORDER/JOIN/HAVING/RETURNING; hidden table and unknown table; catalog and EXPLAIN | Uniform sanitized denial where referenced; no metadata/plan/value leakage |
| SQL-A07 | Each side of a join contains invisible rows; COUNT/MAX over mixed visible/hidden data | Only native-authorized rows enter operators; no privileged scan; result matches visible-input reference |
| SQL-A08 | Two writes with same expected revision; guard bypass through OR; bulk UPDATE; attempts to modify revision | At most one competing commit; unmatched ordinary update yields 0; unsupported shapes rejected |
| SQL-A09 | Two-item batch, second-item failure/assertion mismatch, delayed commit reply, same-key changed body | All-or-nothing transaction; no partial RETURNING; unknown reconciles original receipt; digest conflict rejected |
| SQL-A10 | Drop reply after committed write; API/DB restart; cancel before/after commit; revoke before RETURNING publication | No duplicate mutation on original-key lookup; unknown never inferred rolled back; committed content withheld on revocation |
| SQL-A11 | DDL interrupted in backfill/index build, concurrent Schema publish, native bypass, old snapshot/new incarnation | No unverified constraint advertised; no premature binding/READY; stale artifacts invalidated; original migration reconciled |
| SQL-A12 | LIMIT 120 with page_size 50; equal/null sort keys; cursor role/schema/incarnation change; concurrent sort-key edits | At most 50/50/20; correct qualified NULL ranking; invalid cursor rejected; live-list semantics disclosed |
| SQL-A13 | Read fully computed then permission withdrawn before page/cursor publication; cached plan/result access | Final fence denies content and cursor publication; no cache authority reuse |
| SQL-A14 | Huge sort/join/aggregate with LIMIT 1; missing physical-work limiter; wait deadline while native work continues | Disable unbounded plans; no false physical cancellation; ownership and budget persist until proven completion/fence |
| SQL-A15 | Prompt-generated SQL, native arrow/UDF/file/network access, unqualified vector index, result external disclosure | Generation grants no execution; disabled extensions denied; separate model-disclosure authorization |
| SQL-A16 | Capability toggled without matching evidence; driver connects and requests catalog/transaction feature | Remains disabled; driver fails explicitly or has its own versioned passing matrix; no broad compatibility claim |

Reference evaluation uses a fixed PostgreSQL version/container digest only for the supported common SQL subset, with declared differences for lexical restrictions, byte collation, safety guards, metadata, ID type and absent-field mapping. Never use PostgreSQL as the reference for SurrealDB-specific extension behavior. Compare ordered sequences for ORDER BY and multisets otherwise, preserving duplicates, NULL tags, types and full completeness. Incomplete/approximate results cannot pass exact equivalence. No PostgreSQL installation or container was started in this task.

Suggested minimum synthetic dataset: two logical tables with at least 12 rows covering repeated business values, absent/null optional fields, empty relation, int64 boundaries, tied sort keys, visible/hidden owners and row-dependent masked fields. Record seed, schema/policies, literal fixture, backend/compiler fingerprint and expected values. This proves language boundaries only; realistic load, storage faults and customer acceptance need separately scoped datasets and runs.

## 3. Design findings resolved

| Risk | Design resolution | Remaining gate |
| --- | --- | --- |
| SQL-looking native syntax mistaken for compatibility | Named language/profile and separate driver profile | No conformance claim until actual corpus |
| Parser support mistaken for safety | Exhaustive AST allowlist, typed binder and effects | Parser pin and fuzz/unsupported-node corpus |
| Hidden fields collapsed to NULL | Deny references/masks before evaluation | Native field-policy mapping qualification |
| SQL UPDATE weakens existing CAS | Exact id/revision conjunction, typed command executor | Atomic vector and zero-match translation |
| LIMIT confused with page cap | Independent logical cap/transport cursor accounting | Native continuation and result-completeness cases |
| JOIN of independently fetched live pages | Consistent authorized input view required | R2 disabled until executor selected and proven |
| Timeout interpreted as stopped work | Wait/physical deadline/cancel outcome separate | Effective work budget and owner reconciliation |
| Constraint exists only in SQL path | Every mutation interface and native bypass evaluated | M1 cannot publish unsupported enforcement |
