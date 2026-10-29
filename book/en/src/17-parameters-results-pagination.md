# 17. Parameters, results and pagination

## 17.1 Value and result shape

<a id="n045"></a>

**N045.** Parameters MUST bind scalar values, never identifiers, keywords, directions, expressions, scope or executable fragments. A string containing SQL syntax remains a TEXT value. Array/JSON/native tagged parameter escape hatches are prohibited until separately specified.

Result metadata has ordered columns with one-based ordinals, labels, declared logical types/typemods and nullability. Rows are arrays in that order, allowing duplicate labels without data loss. Schema types do not change when current values happen to be NULL.

The transport uses tagged values. BIGINT/NUMERIC are exact decimal strings; UUID/timestamp use canonical strings; BOOLEAN uses a boolean; DOUBLE uses a finite number; SQL NULL is `{"type":"null"}`. A nullable non-NULL value retains its ordinary type tag. The interface contract governs complete JSON shapes. `affected_rows` is an exact BIGINT decimal string for DML, and null for SELECT.

## 17.2 Continuation and completeness

<a id="n046"></a>

**N046.** Transport page_size MUST NOT change SQL LIMIT. A result with LIMIT 120/page_size 50 has at most 50/50/20 rows. Continuation MUST track remaining logical cap and consumed rows, not rerun LIMIT 120 afresh for each page.

A resumable R1 live keyset requires explicit total ordering including an authorized unique logical id. Nullable sort requires a correct NULL-rank/value/id continuation predicate and its feature. Without a proven total order, the executor must deliver one bounded complete result or reject continuation. R2 joins, aggregates, DISTINCT and UNION require a qualified retained complete result or a separately proven resumable plan; a naive id cursor is insufficient.

<a id="n047"></a>

**N047.** Cursors MUST bind actor/authorization, query/artifact/typed-bindings digest, versions, scope/incarnation/security sequence, sort state, remaining cap and original expiry. Every page, including empty/cursor-only responses, MUST pass current publication authorization. Changing a role/schema/incarnation, expiry or a digest makes the cursor invalid.

A live keyset is a mutable multi-page list: sort-key changes/inserts/deletes may cause omissions or repeats. It is not a transaction snapshot. A materialized result must derive from a qualified input view and retain protected provenance; expiry/revocation terminates access. Snapshot export is the separately qualified existing SnapshotTicket workflow.

<a id="n048"></a>

**N048.** A response MUST distinguish a complete logical result, a normal partial page with continuation, and an incomplete result caused by budget/deadline/error. An incomplete aggregate cannot be labeled complete. No total count is inferred from page length. The transport field is `page.result_complete`, not an unrelated success flag.
