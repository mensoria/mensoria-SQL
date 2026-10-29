# 8. SELECT, ordering and logical limits

## 8.1 Logical evaluation

<a id="n021"></a>

**N021.** SELECT MUST behave as: bind and authorize relations/columns → obtain qualified input view → apply per-relation row policy → FROM/JOIN → WHERE → GROUP/aggregate when present → HAVING → projection → DISTINCT → ORDER BY → logical LIMIT/FETCH → authorized publication. Physical execution may differ only when proven semantically equivalent.

R1 requires FROM with exactly one relation. SELECT without FROM is deferred. Projection accepts scalar expressions allowed by enabled features, optionally `AS output_name`; output alias AS is required in v1. Unaliased simple columns use their column name; other unaliased expressions receive deterministic labels `expr_1`, `expr_2`, etc., numbered by their projection ordinal. Duplicate output labels are allowed for top-level reads because wire rows use ordinals, but cannot be referenced ambiguously.

`*` or `alias.*` expands authorized bound columns in catalog order. Star cannot be mixed with other items in the same SELECT list in v1. An unauthorized/row-dependent-masked field is not silently included and nullified. Expansion is frozen in the artifact; incompatible binding/policy changes invalidate it.

<a id="n022"></a>

**N022.** Default SELECT ALL MUST preserve duplicate projected rows. DISTINCT requires R2 and groups SQL NULL values together for tuple equality. It MUST compare full typed tuples rather than hash values alone. For DISTINCT, ORDER BY expressions must be projected expressions or unique output labels; hidden sort columns cannot change duplicate elimination semantics.

## 8.2 ORDER BY

Each key is a permitted input/projected column reference or a unique output alias; numeric ordinal ordering and arbitrary sort expressions are deferred. ASC is default. NULL placement is ASC NULLS LAST, DESC NULLS FIRST; explicit NULLS FIRST/LAST overrides it.

<a id="n023"></a>

**N023.** Every nullable order key, including one made nullable by LEFT JOIN, MUST require `read.nullable_order`. Without the feature, validation rejects that sort. All keys use declared logical comparison, not backend locale or record-order behavior.

R1 supports at most four order keys. R2 retains the same default ceiling unless an installation publishes a larger qualified limit. Ties have unspecified order unless explicit keys form a total order. An executor may choose a repeatable order internally, but cannot promise it as SQL semantics.

## 8.3 LIMIT and FETCH

LIMIT n and FETCH FIRST n ROWS ONLY are alternative nonnegative integer literal caps, within BIGINT and the published maximum logical-result bound. LIMIT 0 returns typed empty rows but still performs binding/authorization checks. Both forms together, OFFSET, LIMIT ALL, FETCH NEXT and WITH TIES are deferred.

<a id="n024"></a>

**N024.** Missing LIMIT MUST mean the entire logical result subject to explicit resource enforcement, not an undocumented default LIMIT. SQL limits MUST remain distinct from transport page sizes, deadlines and scan budgets. A partial result MUST NOT be reported as complete.

Without ORDER BY, which rows satisfy a LIMIT is unspecified. Exact cross-page continuation requires the stronger conditions in §17; the transport MUST NOT silently append an id sort key and claim it was requested SQL ordering.
