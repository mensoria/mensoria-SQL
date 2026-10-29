# Mensoria SQL Standard Draft — Full Edition

| Field | Value |
| --- | --- |
| Document identifier | MSQL-SD-001 |
| Draft revision | 0.1.0-draft.1 |
| Language version | 1 |
| Status | Proposed normative draft; no runtime conformance established |
| Date | 2026-10-29, Asia/Shanghai |
| Product | Mensoria DB |

**Chinese edition:** [简体中文完整版](137-mensoria-sql-standard-draft.zh-CN.md)

[Documentation index](README.md) · [Architecture and delivery](136-mensoria-db-sql-design.md) · [Transport contract](../../specs/004-surrealdb-rust-ai-baas/contracts/mensoria-sql.md) · [Feature requirements](../../specs/004-surrealdb-rust-ai-baas/spec.md) · [Review and evidence](../../specs/004-surrealdb-rust-ai-baas/mensoria-sql-design-review.md)

## Contents

1. Purpose, authority and normative terminology
2. Conformance profiles and feature registry
3. Database model, names and binding
4. Lexical structure
5. Data types and values
6. Type resolution and casts
7. Expressions, predicates and NULL
8. SELECT, ordering and logical limits
9. JOIN
10. Grouping and aggregates
11. Optional relational constructs
12. Data modification
13. Request transactions, idempotency and unknown outcomes
14. Schema definition and migration
15. Catalog and capability discovery
16. Validation, artifacts and EXPLAIN
17. Parameters, results and pagination
18. Diagnostics
19. Budgets, deadlines and cancellation
20. Authorization, lineage and auditing
21. Multimodel extension framework
22. Compatibility, versioning and implementation requirements
23. Conformance evidence and release requirements
24. References

Appendices: A. Closed grammar; B. Worked conformance corpus; C. Excluded syntax; D. Review checklist and revision history.

## 1. Purpose, authority and normative terminology

### 1.1 Scope

Mensoria SQL is a standard-oriented, versioned query and mutation language for authorized logical relations in one Mensoria DB project environment. It uses familiar SQL notation and selected PostgreSQL conveniences while retaining Mensoria's current identity, schema, command and operation ownership.

This document specifies observable behavior. It does not replace the SurrealDB storage engine, create a new authorization service, or prescribe a second database. A parser, native database or client accepting similar text is not evidence of conformance.

**N001.** In this document, MUST/SHALL express a requirement; MUST NOT/SHALL NOT express a prohibition; SHOULD expresses a recommendation requiring a documented reason for deviation; MAY expresses an option. An implementation claiming a profile MUST satisfy every applicable MUST requirement and publish its enabled optional features.

**N002.** This draft is the language authority. [Chapter 136](136-mensoria-db-sql-design.md) owns architecture and staged delivery; the [interface contract](../../specs/004-surrealdb-rust-ai-baas/contracts/mensoria-sql.md) owns concrete request/result encodings. A conflict MUST be corrected before enabling the affected feature; implementations MUST NOT silently choose whichever interpretation is easier.

**N003.** No implementation may claim complete ISO SQL, complete PostgreSQL, JDBC/ODBC, ORM, BI-tool or PostgreSQL wire compatibility from this draft. Such claims require separately named versions, supported features and actual evidence.

### 1.2 Terms

| Term | Meaning |
| --- | --- |
| Scope | Authenticated organization/project/environment binding |
| Incarnation | Recovery generation distinguishing a current physical environment from an old one |
| Logical relation | Published SQL table or scoped query result, distinct from a physical native table |
| Binding | Versioned mapping from logical SQL names/types to published collection/schema metadata |
| Artifact | Immutable validated SQL/typed-plan revision with declared dependencies |
| Operation | Existing durable authority for accepted execution and its original-key outcome |
| Publication | Final authorized release of result bytes, metadata or a continuation capability |
| Unknown | Insufficient evidence to confirm commit, failure or physical completion |
| Complete result | All rows required by the SQL expression and its explicit logical cap have been delivered |
| Qualified feature | A feature with a frozen implementation profile and passing required evidence |

Examples are informative unless a rule or Appendix B explicitly gives an expected result. A “deferred” feature has no executable contract in v1; an “optional specified” feature has rules here but requires a separate enabled capability.

## 2. Conformance profiles and feature registry

### 2.1 Profiles

**N004.** Profile enablement MUST be scoped, versioned and backed by evidence. A parser's ability to construct an AST MUST NOT enable a feature.

| Profile | Minimum required behavior | Dependencies |
| --- | --- | --- |
| R1 | Single-relation SELECT; BOOLEAN/BIGINT/TEXT; comparisons, AND/OR/NOT, NULL tests, IN; aliases, scalar CAST, ordering, LIMIT/FETCH; authorized metadata and EXPLAIN | Current native identity, policy/publication fences, qualified effective budgets |
| W1 | One-row INSERT; exact-id/revision UPDATE/DELETE; explicit-column RETURNING; atomic request batches | R1 and qualified same-transaction command-vector/receipt support |
| R2 | DISTINCT; two-relation INNER/LEFT equijoin; GROUP BY/HAVING; five named aggregates; CASE/COALESCE; NUMERIC(p,s) | R1 and a consistent authorized input view with bounded relational execution |
| M1 | CREATE TABLE, ADD COLUMN, CREATE/DROP INDEX, DROP TABLE proposals | R1 and existing SchemaAdmin/maintenance publication workflow |
| X1 | Framework for individually named multimodel extensions | R1 plus each extension's own prerequisites; no blanket enablement |
| P1 | Reserved driver/wire compatibility profile | Separately specified protocol/client versions; outside this language draft |

R2 does not imply W1 or M1. W1 does not imply R2. M1 cannot accept types whose corresponding type feature is disabled. X1 and P1 are not independently complete claims of SQL support.

### 2.2 Feature identifiers

These stable identifiers are language features, not executable function names. Required features are enabled only with their owning profile. Specified optional features are disabled unless explicitly qualified.

| Feature ID | Status / owner | Rule |
| --- | --- | --- |
| `read.single_relation` | Required R1 | §§3, 8 |
| `expr.boolean_predicates` | Required R1 | §7 |
| `expr.in_list` | Required R1 | §7 |
| `type.boolean_bigint_text` | Required R1 | §§5–6 |
| `read.order_limit` | Required R1 | §8 |
| `catalog.scoped` | Required R1 | §15 |
| `plan.explain` | Required R1 | §16 |
| `read.nullable_order` | Specified optional R1 | §§8, 17 |
| `type.uuid` | Specified optional R1 | §§5–6 |
| `write.cas` | Required W1 | §12 |
| `write.returning` | Required W1 | §12 |
| `write.atomic_batch` | Required W1 | §13 |
| `write.multi_values` | Specified optional W1 | §§12–13 |
| `read.distinct` | Required R2 | §8 |
| `read.equijoin` | Required R2 | §9 |
| `read.group_aggregate` | Required R2 | §10 |
| `expr.case_coalesce` | Required R2 | §7 |
| `type.numeric` | Required R2 | §§5–6, 10 |
| `expr.numeric_arithmetic` | Specified optional R2 | §7 |
| `expr.text_basic` | Specified optional R2 | §7 |
| `read.cte` | Specified optional R2 | §11 |
| `read.exists` | Specified optional R2 | §11 |
| `read.union_all` | Specified optional R2 | §11 |
| `type.double` | Specified optional R2 | §§5–6, 10 |
| `type.timestamptz` | Specified optional R2 | §§5–6 |
| `schema.proposal` | Required M1 | §14 |
| `schema.literal_default` | Specified optional M1 | §14 |
| `extension.json` | Deferred X1 | §21 defines registration requirements only |
| `extension.graph` | Deferred X1 | §21 defines registration requirements only |
| `extension.fulltext` | Deferred X1 | §21 defines registration requirements only |
| `extension.vector` | Deferred X1 | §21 defines registration requirements only |
| `driver.postgresql` | Reserved P1 | Requires separate driver specification |

**N005.** A statement requiring multiple features MUST satisfy their union, including type and operator dependencies. Disabled or deferred syntax MUST fail before execution with `SQL_FEATURE_UNSUPPORTED`, even when the parser recognizes it.

**N006.** An implementation MAY expose separately named preview features before a complete profile qualifies, but MUST NOT advertise that profile as enabled. A preview still obeys every applicable normative semantic/security requirement. Effective limits and missing profile requirements MUST be discoverable.

## 3. Database model, names and binding

**N007.** One execution MUST bind to one server-derived scope and incarnation. SQL MUST NOT override the physical target, switch namespaces/databases, or join across project environments.

The default schema is `public`. A user table reference is either `table_name` or `public.table_name`. Only the three virtual catalog relations in §15 use other schemas. Three-part names, `search_path`, temporary schemas and native record-target notation are prohibited.

**N008.** A logical table MUST map to a published collection binding containing its logical identity, SchemaRevision, mapping revision, ordered columns, types, nullability, source mappings and policy obligations. An arbitrary native/schemaless table MUST NOT automatically appear as a SQL table.

Platform SQL columns are `id TEXT NOT NULL`, `revision BIGINT NOT NULL`, and qualified `created_at`/`updated_at` timestamp columns when actually mapped and enabled. Timestamp columns are not implied for historical collections without suitable data. `id` is immutable. `revision` is server-owned, initially 1 for a new SQL-created row, and increments by 1 for each committed UPDATE, including a value-preserving update. Revision overflow fails the transaction.

**N009.** New SQL bindings MUST reserve `id`, `revision`, `created_at` and `updated_at` against business-column collisions. Existing conflicting fields MUST use an explicit reviewed SQL alias; binding MUST NOT rename stored data implicitly.

**N010.** Name resolution MUST use authorized catalog metadata. Missing and unauthorized public resource references MUST yield the same sanitized `SQL_REFERENCE_DENIED`; no hidden physical table, name, row count or native error may be returned.

A table alias hides its original qualifier inside that query block. A column reference is unqualified or qualified by the active table/CTE alias. Ambiguous references are rejected. Output aliases are visible only to ORDER BY, never WHERE/ON/GROUP BY/HAVING or another item in the same SELECT list. An alias matching both an output label and input column in ORDER BY resolves to the unique output label; duplicate matching output labels are ambiguous.

## 4. Lexical structure

### 4.1 Source encoding and identifiers

**N011.** SQL source MUST be valid UTF-8, without U+0000 or a byte-order mark. Whitespace outside strings/comments is ASCII space, tab, CR or LF; CRLF counts as one line break for diagnostics. All other unexpected control characters are rejected.

Unquoted identifiers use `[A-Za-z_][A-Za-z0-9_]*` and fold to lowercase. Quoted identifiers use double quotes and preserve case, but their decoded content must match the same ASCII pattern in v1. Thus `notes`, `NOTES` and `"notes"` resolve identically, while `"Notes"` is distinct. A decoded quote, whitespace or Unicode name is not a valid v1 identifier; a reviewed alias is required. Identifier length is at most 63 UTF-8 bytes, with no silent truncation.

All word terminals shown in uppercase in Appendix A are reserved, matched case-insensitively outside quoted identifiers. Quoting allows an otherwise reserved word if its decoded form obeys the identifier restriction. `PUBLIC`, `INFORMATION_SCHEMA` and `MENSORIA` remain ordinary schema identifiers rather than extra SQL keywords.

### 4.2 Literals and comments

| Token | Syntax and meaning |
| --- | --- |
| String | Single-quoted Unicode text; `''` encodes one apostrophe; backslash is an ordinary character |
| Integer | One or more ASCII digits, optional sign consumed by scalar grammar; BIGINT range checked after sign |
| Decimal | Digits, period, digits; optional sign consumed by scalar grammar; requires `type.numeric`; at most 38 precision/scale |
| Boolean | `TRUE` or `FALSE` |
| SQL NULL | `NULL`, with a type inferred from context or explicit CAST |
| Parameter | `$` followed by positive decimal position, no leading zero; e.g. `$1` |
| Comments | `--` through line end; nonnested `/* ... */`; unterminated/nested block comments rejected |

`-9223372036854775808` is a valid BIGINT literal even though its unsigned magnitude exceeds the positive BIGINT maximum. Exponents, hexadecimal/binary literals, dollar quoting, backslash-escape string prefixes, bit strings and locale-dependent numbers are deferred. UUID/timestamp/double values use typed parameters or explicit CAST from TEXT, not special literal token classes.

**N012.** Normal execution MUST accept exactly one parsed statement plus at most one trailing semicolon. It MUST reject empty input, extra statements/tokens and unclosed lexical constructs. Batch input MUST be an array of independently parsed statements; semicolon splitting is prohibited. SQL text inside a comment or string is never a statement.

Source spans use one-based Unicode-code-point line/column positions, with an exclusive end position. A semantically equivalent normalized source may share a plan cache entry, but literal/parameter values remain part of execution identity.

## 5. Data types and values

**N013.** A scalar value MUST have one declared logical type or be SQL NULL of a known contextual type. Backend values MUST pass the declared codec; lossy coercion or exposure as a raw native value is prohibited.

| Type spelling | Domain | Comparison / grouping |
| --- | --- | --- |
| `BOOLEAN` | TRUE, FALSE | Equality; ordering FALSE before TRUE; nullable UNKNOWN is SQL NULL |
| `BIGINT` | Signed 64-bit integer | Exact equality/order/group |
| `TEXT` | Valid Unicode scalar sequence excluding U+0000, including empty string | Exact code-point content equality; UTF-8 byte lexicographic order; no normalization or locale |
| `UUID` | 128-bit UUID; optional type feature | Equality, IN, DISTINCT, GROUP BY; ordering/MIN/MAX prohibited in v1 |
| `NUMERIC(p,s)` | Decimal, 1 <= p <= 38, 0 <= s <= p | Exact equality/order/group after safe common-type resolution |
| `DOUBLE PRECISION` | Finite IEEE binary64; optional type feature | Numeric equality/order; -0 and +0 compare/group equal; NaN/infinity prohibited |
| `TIMESTAMP WITH TIME ZONE` | UTC instant, microsecond precision, years 0001–9999 | Instant equality/order/group; no session timezone |

The type-name grammar deliberately excludes INT/INTEGER/VARCHAR/DECIMAL aliases in this draft; encountering them is unsupported syntax, not an implied alias. `NUMERIC` without precision and scale is also unsupported. These choices can be reconsidered in a later versioned revision.

NUMERIC values are exact multiples of 10^-s with magnitude less than 10^(p-s). Decimal literal type uses total written digits and fractional digits, excluding sign and leading integral zeros, with minimum precision sufficient for its scale and at least 1. A leading zero before a decimal point is required. Trailing fractional zeros contribute to the inferred scale. Parameter types explicitly declare p/s.

TEXT never trims trailing spaces and has no CHAR padding. U+0000 is prohibited in TEXT literals, typed parameters and results; reject invalid parameters as SQL_INVALID_TEXT_VALUE and invalid stored/returned values as SQL_TYPE_ERROR, never strip the character. TEXT may contain non-NUL control characters as data inside valid string/parameter encodings; logs/results remain protected. Native record IDs, geometry, duration, arrays and arbitrary objects are not members of these domains.

**N014.** Authorized absent optional business fields and explicit stored nulls MUST both map to SQL NULL in the relational view. An absent required column MUST fail with `SQL_TYPE_ERROR`; an unreadable field MUST follow §20, never become an ordinary NULL.

**N015.** JSON is not a core v1 type. A future registered JSON extension MUST preserve SQL NULL versus JSON value null and specify missing-path behavior separately. A transport tag reserved for JSON does not make that extension executable.

## 6. Type resolution and casts

### 6.1 General resolution

**N016.** Repeated occurrences of a parameter MUST resolve to a single declared type. Positions MUST be contiguous from 1 and bindings MUST contain exactly those positions. Types cannot be inferred from a backend execution trial.

An untyped NULL adopts the other comparison/assignment/CASE/COALESCE/UNION operand type when one unambiguous common type exists. `NULL IS NULL` is valid without a scalar payload type because the result is nonnullable BOOLEAN. `NULL = NULL` is valid and yields nullable BOOLEAN UNKNOWN; the compiler may use an internal null-only type for these comparisons. A bare projected NULL, an all-NULL CASE/COALESCE result, or an unconstrained parameter requires explicit type declaration/CAST.

Comparison, CASE, COALESCE and UNION common types are:

1. Identical types retain that type.
2. BIGINT may widen to NUMERIC(19,0) when combined with NUMERIC; the resolved p/s must exactly represent both domains.
3. Two NUMERIC(p,s) types resolve to scale=max(s1,s2) and integral digits=max(p1-s1,p2-s2); p=integral+scale. If p>38, reject the expression at binding; never silently reduce scale.
4. No implicit TEXT/numeric/BOOLEAN/UUID/timestamp conversion; no implicit exact-number/DOUBLE conversion.

### 6.2 Explicit CAST

**N017.** CAST MUST either produce the specified type exactly, except explicitly defined floating conversion, or report a typed error. SQL NULL casts to any enabled scalar type and remains SQL NULL.

| Source → target | Behavior |
| --- | --- |
| Same type | Identity, subject to target typemod validation |
| TEXT → BIGINT | Optional sign plus digits only, no whitespace; signed 64-bit range |
| TEXT → BOOLEAN | Case-insensitive `true` or `false` only, no whitespace |
| TEXT → NUMERIC(p,s) | Signed decimal/integer notation only; no exponent; target scale padding allowed, nonzero discarded digits rejected |
| BIGINT / NUMERIC → NUMERIC(p,s) | Exact representation required; excess fractional zeros may be removed, no rounding |
| NUMERIC → BIGINT | Fractional part must be zero and value in range |
| BIGINT / NUMERIC → DOUBLE | Only with `type.double`; explicitly permitted binary64 round-to-nearest-ties-even; overflow rejected |
| TEXT → DOUBLE | Strict finite decimal/exponent parser named in the backend profile; surrounding whitespace, NaN and infinity rejected |
| TEXT → UUID | Standard hyphenated 8-4-4-4-12 hexadecimal form, case-insensitive input; canonical lowercase output |
| TEXT → TIMESTAMP WITH TIME ZONE | RFC3339 date/time with `T`, seconds and mandatory `Z` or ±HH:MM; <= 6 fractional digits, no leap seconds |
| BIGINT/NUMERIC/BOOLEAN/UUID/timestamp → TEXT | Locale-independent canonical codec spelling; timestamp UTC `Z` |

DOUBLE → TEXT uses a pinned shortest-round-trip finite codec; DOUBLE → exact number is deferred. Timestamp conversion rejects `-00:00` (unknown local offset), out-of-range local components/offsets and UTC instants outside years 0001–9999 after offset normalization. Numeric offsets must have hours 00–23 and minutes 00–59; UTC rollover is checked after conversion, without clamping. Cross-type UUID/numeric/BOOLEAN casts not listed above are unsupported. NUMERIC-to-TEXT preserves its declared scale; BIGINT has no leading plus/zeros; BOOLEAN uses lowercase `true`/`false`. Floating TEXT parsing/formatting must be fixed in the implementation fingerprint; native library defaults alone are not a contract.

## 7. Expressions, predicates and NULL

### 7.1 Boolean and comparison semantics

**N018.** WHERE, ON, HAVING and searched CASE conditions MUST be BOOLEAN. They MUST NOT use numeric/string/native truthiness. Only TRUE passes a filter or ON match; FALSE and UNKNOWN do not.

| A | B | A AND B | A OR B |
| --- | --- | --- | --- |
| TRUE | TRUE | TRUE | TRUE |
| TRUE | FALSE | FALSE | TRUE |
| TRUE | UNKNOWN | UNKNOWN | TRUE |
| FALSE | FALSE | FALSE | FALSE |
| FALSE | UNKNOWN | FALSE | UNKNOWN |
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

AND/OR are commutative. NOT TRUE=FALSE; NOT FALSE=TRUE; NOT UNKNOWN=UNKNOWN. UNKNOWN is the truth interpretation of a NULL BOOLEAN; it is not a separate stored scalar tag.

`=`, `<>`, `<`, `<=`, `>`, `>=` operate on comparable common types. `!=` is accepted as an alias for `<>`. An ordinary comparison involving SQL NULL yields UNKNOWN, including NULL against NULL. UUID permits only equality/inequality until a separately specified ordering feature exists. `IS NULL` and `IS NOT NULL` return nonnullable BOOLEAN.

`x IN (a,b,...)` is TRUE if any typed comparison is TRUE, otherwise UNKNOWN if any comparison is UNKNOWN, otherwise FALSE. NOT IN applies logical NOT. Lists must be nonempty and scalar; IN subqueries, row constructors and array membership are deferred. A NULL left operand therefore yields UNKNOWN against a nonempty list.

**N019.** Boolean evaluation order is not a user-visible short-circuit guarantee. Validation MUST inspect all branches, including unreachable branches, for resource/type/effect permission. CASE/COALESCE value evaluation follows §7.2, but it MUST NOT suppress binding errors in a branch.

### 7.2 CASE and COALESCE, R2

Searched `CASE WHEN condition THEN value ... [ELSE value] END` returns the first branch whose condition is TRUE; omitted ELSE returns typed SQL NULL. All result branches resolve to one common type. Conditions may be FALSE or UNKNOWN and continue to later branches. Simple CASE is deferred.

`COALESCE(a,b,...)` requires at least two arguments with one common result type; returns the first non-NULL argument, or typed NULL if all are NULL. An all-untyped-NULL argument set is rejected unless an explicit cast supplies the common type.

**N020.** For scalar expressions, an unchosen CASE result and COALESCE arguments after the chosen value MUST NOT raise a runtime value error. The compiler MUST still bind/authorize their contents. Group aggregates are computed before SELECT scalar CASE and cannot be guarded from aggregate errors by CASE.

### 7.3 Optional arithmetic and text expressions

`expr.numeric_arithmetic` enables unary +/- and binary +,-,*,/ for same-resolved-domain numeric operands. Unary sign propagates SQL NULL. A binary operator whose evaluated operand is SQL NULL returns typed SQL NULL, including typed NULL divided by zero; the division operator checks zero only when both operands are non-NULL. Each operand expression must still be evaluated for its own errors (in either order), so NULL plus an independently failing CAST is an error. CASE/COALESCE retain their explicit lazy value-branch semantics. BIGINT +,-,* return BIGINT with checked overflow; BIGINT / BIGINT returns NUMERIC(38,6) with round-half-even. Division by zero errors. Mixed BIGINT/NUMERIC first resolves exactly under §6; all NUMERIC operations use the rules below. DOUBLE combines only with DOUBLE, returns finite binary64 and rejects nonfinite results/division by zero.

NUMERIC +,- return NUMERIC(38,max(s1,s2)); multiplication returns NUMERIC(38,min(38,s1+s2)) but MUST reject rather than discard any nonzero fractional digits beyond scale 38. NUMERIC division returns NUMERIC(38,max(s1,s2,6)), rounding half-even once to the result scale. All operations reject a result whose integral part cannot fit. Arithmetic precision/scale are derived before execution and do not change by row value.

`expr.text_basic` enables TEXT concatenation `||`, `CHAR_LENGTH(TEXT) -> BIGINT`, and `OCTET_LENGTH(TEXT) -> BIGINT`. Concatenation and both functions are NULL-propagating. Character length counts Unicode scalar values, not grapheme clusters; octet length counts UTF-8 bytes. No implicit scalar-to-TEXT conversion. LIKE, regex, LOWER/UPPER, locale collation and user functions are deferred.

Operator precedence, highest to lowest: parentheses/CAST/function/CASE; unary sign; */; binary +/-; ||; comparison/IN/IS NULL; NOT; AND; OR. Binary arithmetic and concatenation associate left. Comparisons cannot chain: `1 < 2 < 3` is invalid.

## 8. SELECT, ordering and logical limits

### 8.1 Logical evaluation

**N021.** SELECT MUST behave as: bind and authorize relations/columns → obtain qualified input view → apply per-relation row policy → FROM/JOIN → WHERE → GROUP/aggregate when present → HAVING → projection → DISTINCT → ORDER BY → logical LIMIT/FETCH → authorized publication. Physical execution may differ only when proven semantically equivalent.

R1 requires FROM with exactly one relation. SELECT without FROM is deferred. Projection accepts scalar expressions allowed by enabled features, optionally `AS output_name`; output alias AS is required in v1. Unaliased simple columns use their column name; other unaliased expressions receive deterministic labels `expr_1`, `expr_2`, etc., numbered by their projection ordinal. Duplicate output labels are allowed for top-level reads because wire rows use ordinals, but cannot be referenced ambiguously.

`*` or `alias.*` expands authorized bound columns in catalog order. Star cannot be mixed with other items in the same SELECT list in v1. An unauthorized/row-dependent-masked field is not silently included and nullified. Expansion is frozen in the artifact; incompatible binding/policy changes invalidate it.

**N022.** Default SELECT ALL MUST preserve duplicate projected rows. DISTINCT requires R2 and groups SQL NULL values together for tuple equality. It MUST compare full typed tuples rather than hash values alone. For DISTINCT, ORDER BY expressions must be projected expressions or unique output labels; hidden sort columns cannot change duplicate elimination semantics.

### 8.2 ORDER BY

Each key is a permitted input/projected column reference or a unique output alias; numeric ordinal ordering and arbitrary sort expressions are deferred. ASC is default. NULL placement is ASC NULLS LAST, DESC NULLS FIRST; explicit NULLS FIRST/LAST overrides it.

**N023.** Every nullable order key, including one made nullable by LEFT JOIN, MUST require `read.nullable_order`. Without the feature, validation rejects that sort. All keys use declared logical comparison, not backend locale or record-order behavior.

R1 supports at most four order keys. R2 retains the same default ceiling unless an installation publishes a larger qualified limit. Ties have unspecified order unless explicit keys form a total order. An executor may choose a repeatable order internally, but cannot promise it as SQL semantics.

### 8.3 LIMIT and FETCH

LIMIT n and FETCH FIRST n ROWS ONLY are alternative nonnegative integer literal caps, within BIGINT and the published maximum logical-result bound. LIMIT 0 returns typed empty rows but still performs binding/authorization checks. Both forms together, OFFSET, LIMIT ALL, FETCH NEXT and WITH TIES are deferred.

**N024.** Missing LIMIT MUST mean the entire logical result subject to explicit resource enforcement, not an undocumented default LIMIT. SQL limits MUST remain distinct from transport page sizes, deadlines and scan budgets. A partial result MUST NOT be reported as complete.

Without ORDER BY, which rows satisfy a LIMIT is unspecified. Exact cross-page continuation requires the stronger conditions in §17; the transport MUST NOT silently append an id sort key and claim it was requested SQL ordering.

## 9. JOIN

R2 supports one INNER JOIN or LEFT [OUTER] JOIN between two relation references. Plain JOIN is INNER JOIN. Each side must have an unambiguous alias when a qualifier would otherwise be ambiguous. RIGHT/FULL/CROSS/NATURAL JOIN, USING, comma joins and lateral joins are deferred.

**N025.** ON MUST be a nonempty conjunction of typed equalities, each comparing a column from the left relation with a column from the right relation. No OR, constants, residual inequalities or effects are allowed in v1 join conditions. Each input MUST already satisfy its own current native row policy.

INNER JOIN emits every matching pair, preserving multiplicity. LEFT JOIN emits every matching pair, or one null-extended right tuple when no authorized right tuple matches. Native absence and SQL NULL do not match on ordinary equality. WHERE runs after JOIN; filtering a null-extended right column can remove the output row.

**N026.** Both input relations MUST be read from one qualified consistent view; joining independent live paginated API results is prohibited. A planner MUST NOT replace a LEFT JOIN with INNER JOIN or move a WHERE predicate into ON unless equivalent under SQL NULL, duplicates and policy rules.

A qualified input view is an internal execution guarantee, not permission to advertise a named PostgreSQL isolation level. An ordinary R1 cursor may still be a mutable live list across separately executed pages.

## 10. Grouping and aggregates

GROUP BY accepts explicit input column references only; output aliases, ordinals, expression grouping, rollup/cube/grouping sets and functional-dependency relaxation are deferred. Grouping without an aggregate is permitted and yields one row per group. SQL NULL values form one group; composite group equality follows tuple semantics.

**N027.** In a grouped query, every nonaggregate column reference in SELECT/HAVING/ORDER BY MUST be a GROUP BY key. In an aggregate query without GROUP BY, no nonaggregate input columns may be projected or referenced in HAVING/ORDER BY. Aggregate calls are allowed only in SELECT/HAVING and cannot nest.

HAVING requires a grouped or aggregate query and keeps only TRUE. WHERE/ON/GROUP BY cannot contain aggregate calls. ORDER BY may use a unique projected aggregate alias, but not a new aggregate expression. Aggregate DISTINCT, FILTER, ordered aggregates and window clauses are deferred.

| Signature | Result type | Empty/all-NULL behavior |
| --- | --- | --- |
| COUNT(*) | BIGINT NOT NULL | 0 |
| COUNT(x), x any enabled scalar | BIGINT NOT NULL | 0 |
| SUM(BIGINT) | NUMERIC(38,0) | NULL |
| SUM(NUMERIC(p,s)) | NUMERIC(38,s) | NULL |
| AVG(BIGINT) | NUMERIC(38,6) | NULL |
| AVG(NUMERIC(p,s)) | NUMERIC(38,max(s,6)) | NULL |
| MIN/MAX(x), x BOOLEAN/BIGINT/TEXT/NUMERIC/timestamp | Same type as x | NULL |
| SUM/AVG(DOUBLE) | DOUBLE PRECISION | NULL |
| MIN/MAX(DOUBLE) | DOUBLE PRECISION | NULL |

Optional type signatures require the corresponding feature. UUID is allowed in COUNT/DISTINCT/GROUP BY but not MIN/MAX. NUMERIC is mandatory in R2 so BIGINT aggregates always have a defined exact result representation.

**N028.** Aggregates except COUNT(*) MUST ignore SQL NULL inputs. SUM of exact values MUST use a mathematically exact accumulator and check the final declared result; AVG MUST divide the exact sum by the count and round half-even once to its declared scale. A result that cannot fit MUST error. COUNT overflow also errors.

Floating aggregate accumulation order can vary; its codec/algorithm, allowed comparison tolerance and repeatability limits must be published. A floating result cannot pass exact numeric equivalence merely because a finite value was returned. SUM/AVG cannot silently truncate a dataset to satisfy a work budget.

On zero input rows, an aggregate query without GROUP BY produces exactly one aggregate row before HAVING; a query with GROUP BY produces zero groups. MIN/MAX text use byte ordering. Nullable aggregate metadata is retained even when the current input is nonempty.

## 11. Optional relational constructs

### 11.1 Nonrecursive CTE

`read.cte` enables `WITH name AS (select), ... select`. Bodies and the main statement must be SELECT queries. CTEs may reference earlier CTEs, never themselves/later entries; duplicate names and cycles are errors. Each CTE projects explicit unique output names; column-name lists, recursive/data-modifying CTEs and materialization hints are deferred. CTE names hide same-named unqualified public tables within the statement; explicit `public.name` still identifies the table.

**N029.** A CTE MUST preserve bag, NULL, type, lineage and authorized consistent-view semantics. Materialization/inlining MUST NOT change query results or bypass budgets. Each query block retains the two-relation join limit; the complete statement is also subject to published total relation/node limits.

### 11.2 EXISTS

`read.exists` enables [NOT] EXISTS with an uncorrelated SELECT body, only as a predicate. It returns TRUE when its authorized body result has at least one row, FALSE otherwise; never UNKNOWN. The body must project exactly one literal `1`; bind and authorize all its relation/filter references. Correlation, scalar subqueries, IN subqueries and arbitrary projected EXISTS are deferred.

EXISTS observes the body after its logical WHERE/grouping/cap; thus LIMIT 0 is FALSE, and `SELECT 1` over an aggregate-producing FROM does not become a special shortcut. No EXISTS body may weaken the consistent input-view requirement for its parent query.

### 11.3 UNION ALL

`read.union_all` enables a bounded chain of SELECT branches, with no UNION DISTINCT/INTERSECT/EXCEPT. Branches must have equal arity; each column position resolves to one common type. Labels come from the first branch; output nullability is the union of branch nullabilities. All duplicate rows are preserved.

**N030.** UNION ALL branches MUST share the statement's qualified consistent view and authorization lineage. Without a final ORDER BY, branch output order is unspecified. In v1 branches cannot have their own ORDER BY/cap; final ORDER BY refers only to unique output labels, and final cap applies to the entire union.

CTE/EXISTS/UNION can combine only when every required feature is enabled and the full AST obeys the grammar, depth and budget rules. Optional syntax does not loosen parent query restrictions.

## 12. Data modification

### 12.1 Common W1 rules

**N031.** W1 MUST compile into existing scoped typed commands and one native transaction with the original Operation/Outbox/guard obligations. Executing user text directly under a system identity, or sequentially calling independently committing commands, is prohibited.

Targets are published `public` tables, with their exact expected Schema/mapping revision in the validated artifact. W1 supports no target aliases, joins, FROM/USING clauses, subqueries, effects, triggers supplied by the user, generated values or expression assignments. Values are literals, typed parameters or CAST of a value, with no business-column reference.

INSERT must name its columns explicitly, including exactly one `id`. UPDATE assignments must name each business column at most once. Platform revision/timestamps/owner/ACL fields cannot be assigned. Schema write authorization and NOT NULL/type/default rules apply to every assignment and to omitted fields.

### 12.2 INSERT

Base W1 accepts one `VALUES (...)` tuple, with the same arity as the explicit nonduplicate column list. Logical id is non-NULL TEXT. The row is create-if-absent; existing IDs cannot be overwritten. Omitted optional business columns become SQL NULL unless a qualified literal default exists; omitted required columns without a default fail. An explicit NULL does not invoke a default.

**N032.** INSERT MUST commit a row at revision 1 and return affected_rows=1 when successful. A uniqueness/id conflict MUST return one sanitized integrity error without the existing row's data or constraint details. Conditional conflict errors do not establish that a protected row is readable; the service cannot promise perfect information-theoretic concealment of attacker-chosen unique-key occupancy.

`write.multi_values` optionally accepts multiple literal/parameter tuples. Total mutations per request remain <=16, including all statements. Duplicate target IDs within a statement/batch are rejected before mutation; no partial multi-row INSERT is permitted. INSERT SELECT, DEFAULT VALUES, RETURNING *, ON CONFLICT/UPSERT and generated identity are deferred.

### 12.3 UPDATE and DELETE

**N033.** UPDATE/DELETE MUST have a WHERE predicate that is a conjunction of atomic comparisons/NULL tests with mandatory exact `id = value` and `revision = value` terms. There MUST be exactly one guard for each, with id/revision on the left, non-NULL typed scalar values on the right, id TEXT and revision positive BIGINT. OR, NOT, IN, functions or column-to-column guards are prohibited in W1 predicates.

Parentheses may group the conjunction but cannot make either guard optional. Additional conditions may read authorized business columns; extra references to id/revision other than their mandatory guards are rejected in v1. An UPDATE assignment cannot refer to old row data; users read a revision and prepare a new desired value explicitly.

An authorized UPDATE increments the current revision by 1 and updates mapped timestamps where supported, even if business values are unchanged. DELETE removes/tombstones the current row through the existing deletion command; RETURNING refers to the authorized predelete row.

**N034.** An ordinary no-match UPDATE/DELETE MUST produce affected_rows=0 and an empty RETURNING row set, uniformly for absent, invisible, revision-mismatched or additional-condition-mismatched targets. Translation of an existing CAS failure to zero match MUST require proof that no mutation committed. A schema/session/guard failure is not a zero match.

### 12.4 RETURNING

RETURNING accepts an explicit nonempty list of authorized simple columns, optionally AS aliases. INSERT/UPDATE return postmutation values including the new revision; DELETE returns predelete values. All results remain protected by final publication checks. Omitted RETURNING still returns an affected-row count, with no invented business result columns.

**N035.** A committed write whose RETURNING content cannot currently be published MUST retain its committed operation outcome. The service MUST withhold the content and MUST NOT report rollback or automatically resend the mutation under a new key.

## 13. Request transactions, idempotency and unknown outcomes

### 13.1 Atomic request contract

A transaction is one submitted array of W1 statements, not an interactive SQL session. Base limits are <=16 items and <=16 total row mutations, same scope/incarnation, one mutation per target logical row. SELECT and DDL items, savepoints, value dependencies between items and cross-request BEGIN/COMMIT are prohibited. RETURNING supplies the write's read result.

**N036.** The transaction MUST atomically validate current native actor/session/family, schema/mapping, record guards and admission obligations, then commit business changes, ordered per-item outcomes, the original Operation receipt and Outbox records together. A confirmed precommit failure MUST leave no partial business changes or partial RETURNING publication.

An optional request-level `require_affected_rows: 1` assertion on an UPDATE/DELETE item aborts the entire transaction when it would match zero rows. Ordinary standalone SQL retains zero-match success. Item outcomes follow request order; no intermediate result is published before the batch commit.

No named SQL isolation level is implied by this atomic request guarantee. `SET TRANSACTION`, SERIALIZABLE labels and phantom/write-skew claims require a separate qualified contract; unsupported requests are rejected rather than ignored.

### 13.2 Original-key identity

**N037.** Every accepted execution MUST have one original idempotency key bound to its actor, scope/incarnation, language/compiler/profile fingerprint, canonical typed IR, typed values, expected revisions and ordered batch assertions. Same key/different identity MUST conflict; same key/same identity MUST attach to the original operation under current authorization.

The canonical IR must preserve all semantic distinctions, including literal values, decimal scale where meaningful, NULL types, duplicate-sensitive operators and item order. No particular JSON serializer or cryptographic digest is mandated by the language; the implementation contract must pin its canonicalization and keyed-identity protocol.

Repeated reads attach to their original execution; they are not fresh reads. If protected results expire, the original read returns `SQL_RESULT_EXPIRED`; a deliberate new read may use a new key. A lookup MUST NOT create or replay the old operation body.

### 13.3 Outcome and cancellation

**N038.** A lost reply, deadline, disconnected client, missing observation or cancel request MUST NOT be interpreted as rollback, failure, physical completion or permission to issue a fresh-key mutation. Reconciliation MUST refer to the original operation/key/incarnation.

The existing operation authority distinguishes accepted/running, confirmed committed, confirmed failed and unknown/reconciliation-required outcomes. SQL must reuse that authority rather than maintain an independently writable commit state. A backend-confirmed conflict may permit bounded full-transaction retry only after the original attempt is proven uncommitted; a generic transport error does not.

Revocation may prevent a user from observing an existing operation. Authorization failure does not change the durable operation's outcome. After recovery, old-incarnation identities and artifacts cannot access a new target merely by reusing the key.

## 14. Schema definition and migration

M1 parses DDL into proposals. Accepted forms are CREATE TABLE, ALTER TABLE ADD COLUMN, CREATE INDEX, DROP INDEX and DROP TABLE under §14's restricted grammar. Each item targets the current public schema, with expected schema/mapping metadata outside SQL. A successful preview creates a proposal, not a live database change.

**N039.** Only the existing Schema service, under current SchemaAdmin and fenced maintenance authority, may apply a DDL proposal. Query execution MUST NOT install native schema or grant itself management credentials.

### 14.1 Columns and constraints

CREATE TABLE must contain exactly one `id TEXT PRIMARY KEY` column. PRIMARY KEY is allowed only on id, implies NOT NULL and cannot appear as a table-level constraint. Platform revision/timestamps are binding-managed; users cannot declare them as business columns. Other declared columns are nullable unless NOT NULL is specified. For newly created bindings, column order is id, revision, then created_at/updated_at when qualified, then business columns in declaration order excluding id. Existing bindings retain their explicitly published order; ADD COLUMN appends the new business column.

`schema.literal_default` permits `DEFAULT <literal>` or a CAST of a literal, checked once against the target type. Parameters, functions, SQL expressions, sequences, DEFAULT keywords in INSERT, generated columns and volatile defaults are deferred. Defaults apply on omitted INSERT columns; a SET assignment of NULL remains NULL.

**N040.** An ADD COLUMN marked NOT NULL on a nonempty relation MUST have an explicit qualified default/backfill source and actual verification before publication. If the proposal language cannot express an adequate safe backfill, it MUST reject the proposal and require a separate reviewed Schema migration.

ADD COLUMN without a default exposes SQL NULL for every existing row and is allowed only for nullable columns (or a proven empty relation). ADD COLUMN with a qualified literal default must materialize that default for every existing row, nullable or not, before the new binding is published. A default does not dynamically replace absent/null values during later reads. All mutation paths must then obey the published omitted-value/default contract.

Logical indexes live in the current `public` schema, with index-name uniqueness across that environment's logical SQL tables. Each index binds exactly one table identity and its immutable column list/type mapping. CREATE uses create-if-absent name reservation; any current conflicting name gives sanitized SQL_CONSTRAINT_CONFLICT, without its owner/table details. A same-original-operation proposal retry reconciles its original name reservation. DROP resolves `public.index_name` (or its unqualified equivalent), requires management permission on its owning table and expected index/binding revision, and uses the same SQL_REFERENCE_DENIED for a missing or unauthorized name. Logical names never identify caller-chosen physical indexes.

CREATE INDEX creates a nonunique index proposal on explicitly named qualified scalar columns. Index method, physical name and readiness are adapter-owned; lack of a qualified mapping rejects the proposal. DROP INDEX/TABLE uses explicit current resource versions and destructive review; no CASCADE/IF EXISTS/IF NOT EXISTS fast path is defined.

UNIQUE, FOREIGN KEY, CHECK, deferrable constraints, constraint validation hints and cascading actions are deferred. No accepted native declaration may be advertised as SQL-enforced unless every write interface and direct native-writer boundary respects it. SQL-only validation does not prove a database-wide invariant.

### 14.2 Publication and failure

**N041.** The migration MUST use preview → expected-version check → admission close/drain → expand/backfill → actual schema/data/index verification → CAS binding publish → current-watermark reopen. Partial, incompatible or unknown state MUST remain unreleased/BLOCKED pending original-operation reconciliation.

Index preparation/readiness and binding publication are distinct. Removal/contract must respect retained artifacts, versions and active owners. A destructive change cannot be rolled back merely by running an old binary. Recovery must requalify mappings and invalidate old-incarnation artifacts/cursors.

## 15. Catalog and capability discovery

**N042.** Catalog data MUST be generated from currently authorized published bindings, never from a privileged native schema dump. An invisible resource's name, ordinal, type, cardinality or physical location MUST NOT be disclosed.

The R1 minimum virtual relations are:

| Relation | Ordered columns |
| --- | --- |
| `information_schema.tables` | table_schema TEXT, table_name TEXT, table_type TEXT |
| `information_schema.columns` | table_schema TEXT, table_name TEXT, column_name TEXT, ordinal_position BIGINT, data_type TEXT, is_nullable TEXT |
| `mensoria.sql_capabilities` | feature_name TEXT, enabled BOOLEAN, profile TEXT, language_version TEXT |

Catalog columns are nonnullable. table_type is `BASE TABLE`; is_nullable is `YES` or `NO`; data_type is the canonical SQL spelling, including NUMERIC(p,s). ordinal_position is the frozen binding position, even when filtering unauthorized columns leaves gaps. Concealing all schema-shape inference is not promised; catalog access itself requires metadata permission. Native locations, secrets and system tables are absent.

Capabilities expose public feature IDs and current scope-effective availability, plus manifest metadata through the transport API. They never assert a missing business resource exists. An implementation must publish compiler/backend/profile/schema-adapter versions, feature/type/function codecs, limits/enforcement modes and evidence references. Unknown manifest versions are not silently interpreted as an older compatible one.

## 16. Validation, artifacts and EXPLAIN

**N043.** Validation MUST parse, exhaustively inspect AST nodes, resolve authorized metadata, bind types/nullability/effects, enforce feature/size/budget planning gates and record immutable dependency revisions. No execution or external side effect is authorized by a validation result.

Artifacts bind source/canonical plan digests, declared parameter types, scope/incarnation, actor authorization obligations, schema/mapping/security versions, compiler/profile fingerprint and expiry. SQL literals and source are protected artifact content. Metadata-only previews cannot borrow ordinary business-read permissions or management credentials.

**N044.** Execution MUST load the exact artifact revision and recheck current authorization and compatibility before backend access and again before publication. Edits and incompatible schema/policy/compiler/incarnation changes require new validation; an existing artifact MUST NOT be silently recompiled or promoted.

EXPLAIN is an authorized nonexecuting logical-plan operation, accepted through the transport route or `EXPLAIN <select>` syntax when `plan.explain` is enabled. It returns logical resource references, typed operators, required features and effective proposed limits. It must not execute business scans, expose native text/locations/hidden cardinalities or run ANALYZE. Parameter sampling and optimizer suggestions cannot publish schema changes.

## 17. Parameters, results and pagination

### 17.1 Value and result shape

**N045.** Parameters MUST bind scalar values, never identifiers, keywords, directions, expressions, scope or executable fragments. A string containing SQL syntax remains a TEXT value. Array/JSON/native tagged parameter escape hatches are prohibited until separately specified.

Result metadata has ordered columns with one-based ordinals, labels, declared logical types/typemods and nullability. Rows are arrays in that order, allowing duplicate labels without data loss. Schema types do not change when current values happen to be NULL.

The transport uses tagged values. BIGINT/NUMERIC are exact decimal strings; UUID/timestamp use canonical strings; BOOLEAN uses a boolean; DOUBLE uses a finite number; SQL NULL is `{"type":"null"}`. A nullable non-NULL value retains its ordinary type tag. The interface contract governs complete JSON shapes. `affected_rows` is an exact BIGINT decimal string for DML, and null for SELECT.

### 17.2 Continuation and completeness

**N046.** Transport page_size MUST NOT change SQL LIMIT. A result with LIMIT 120/page_size 50 has at most 50/50/20 rows. Continuation MUST track remaining logical cap and consumed rows, not rerun LIMIT 120 afresh for each page.

A resumable R1 live keyset requires explicit total ordering including an authorized unique logical id. Nullable sort requires a correct NULL-rank/value/id continuation predicate and its feature. Without a proven total order, the executor must deliver one bounded complete result or reject continuation. R2 joins, aggregates, DISTINCT and UNION require a qualified retained complete result or a separately proven resumable plan; a naive id cursor is insufficient.

**N047.** Cursors MUST bind actor/authorization, query/artifact/typed-bindings digest, versions, scope/incarnation/security sequence, sort state, remaining cap and original expiry. Every page, including empty/cursor-only responses, MUST pass current publication authorization. Changing a role/schema/incarnation, expiry or a digest makes the cursor invalid.

A live keyset is a mutable multi-page list: sort-key changes/inserts/deletes may cause omissions or repeats. It is not a transaction snapshot. A materialized result must derive from a qualified input view and retain protected provenance; expiry/revocation terminates access. Snapshot export is the separately qualified existing SnapshotTicket workflow.

**N048.** A response MUST distinguish a complete logical result, a normal partial page with continuation, and an incomplete result caused by budget/deadline/error. An incomplete aggregate cannot be labeled complete. No total count is inferred from page length. The transport field is `page.result_complete`, not an unrelated success flag.

## 18. Diagnostics

**N049.** Errors MUST contain a stable Mensoria code, five-character SQLSTATE-style category, sanitized message, phase, retry hint and original operation reference when already accepted and currently observable. Source span is optional when safely attributable. They MUST NOT include protected native text, resource existence details, values, credentials or backend stack traces.

| Code | Category | Trigger |
| --- | --- | --- |
| SQL_SYNTAX_ERROR | 42601 | Invalid token/grammar or extra statement |
| SQL_FEATURE_UNSUPPORTED | 0A000 | Specified optional feature disabled, deferred syntax or unsupported node |
| SQL_REFERENCE_DENIED | 42501 | Unknown/unauthorized public reference |
| SQL_TYPE_ERROR | 42804 | Incompatible types, invalid codec/source mapping or unresolved type |
| SQL_VALUE_OUT_OF_RANGE | 22003 | Overflow, unsupported precision loss or nonfinite number |
| SQL_INVALID_TEXT_VALUE | 22018 | Text cannot be parsed as the declared scalar type |
| SQL_DIVISION_BY_ZERO | 22012 | Evaluated numeric division by zero |
| SQL_AMBIGUOUS_REFERENCE | 42702 | Multiple authorized matches for a permitted name |
| SQL_INVALID_GROUPING | 42803 | Illegal aggregate location or ungrouped column |
| SQL_ARTIFACT_STALE | 55000 | Incompatible execution dependency revision |
| SQL_WRITE_PRECONDITION_REQUIRED | 0A000 | W1 mandatory guard shape absent or unsafe |
| SQL_PRECONDITION_FAILED | 40001 | Explicit affected-row assertion fails |
| SQL_CONSTRAINT_CONFLICT | 23000 | Sanitized integrity violation |
| SQL_KEY_CONFLICT | 23000 | Existing original key bound to different request identity |
| SQL_BUDGET_EXCEEDED | 54000 | Proven resource bound exceeded or plan lacks required enforceable budget |
| SQL_CURSOR_INVALID | 24000 | Cursor expiry/binding/version mismatch |
| SQL_RESULT_EXPIRED | 55000 | Original protected result no longer retained |
| SQL_OUTCOME_UNKNOWN | 08007 | Accepted operation/commit not confirmed |
| SQL_DEPENDENCY_UNAVAILABLE | 08006 | Required dependency inaccessible |
| SQL_CANCEL_PENDING | 57014 | Cancellation requested, physical/commit outcome unconfirmed |

These categories do not promise PostgreSQL driver behavior. In particular 40001 never authorizes blind fresh-key retry, and 57014 never proves rollback. Clients must use the Mensoria code, phase, retry_hint and operation reference together.

Retry hints are `edit`, `revalidate`, `restart_read`, `reconcile_original`, `observe_original`, `none`. Uncertainty after admission takes precedence over a superficial transport/precondition error that would imply no work occurred. Authorization failures may suppress operation visibility without changing its durable outcome.

## 19. Budgets, deadlines and cancellation

**N050.** An enabled implementation MUST enforce and advertise bounds for source/body size, AST nodes/depth, result columns/page bytes, row mutations, execution ownership, concurrency and every physical-work/intermediate resource used by its plans. If a required budget cannot be enforced, the plan MUST be refused.

Initial design ceilings are <=64 KiB request body, <=1,024 AST nodes, depth<=32, <=32 selected columns, <=4 sort keys, page_size default 50/max 100, page bytes<=256 KiB, batch items<=16 and total mutation rows<=16. These are proposed admission bounds, not capacity/SLO measurements. A qualified installation may publish lower bounds; raising a bound requires corresponding qualification.

Scan rows/bytes, input snapshot size, join fanout, aggregate groups, sort memory, result materialization, execution duration and tenant concurrency need explicit effective numeric ceilings and enforcement modes in the manifest. LIMIT 1 does not bound an aggregate/join/sort's work. A time spent waiting for an RPC is not a bound on physical work.

**N051.** The service MUST distinguish client wait timeout, execution deadline, cancel intent, confirmed worker completion and confirmed commit outcome. Ownership/permits must remain accounted for until actual completion or established fencing/reconciliation permits release. The service MUST withhold unauthorized or expired late results.

Partial read bytes already published cannot be recalled. Publication fencing must define the point after which withdrawal blocks future bytes; no claim of network-byte retraction is allowed. Streaming and resumability need evidence beyond buffered page tests.

## 20. Authorization, lineage and auditing

**N052.** SQL MUST reuse native row/field authorization, scoped Control admission and current session/family checks. It MUST NOT replace them with a privileged scan and later filter, cached grants, a caller-selected role or an issuer identity with business-data access.

A reference to a protected field is denied in projection, predicate, ordering, join, grouping, aggregate input, CASE branch and RETURNING. Row-dependent field masks that cannot be proven readable for the entire bound input make that SQL column unusable for that artifact. Star expands only provably readable columns. An unexpected masked value invalidates the pending result rather than being treated as absent data.

**N053.** All reads of plans, history, metadata, cached results, artifacts, cursors and original-operation results MUST reauthorize currently protected content. A plan cache key is not a permission grant. Revocation before final publication MUST suppress the pending content and continuation even when backend computation finished.

Aggregates may intentionally reveal statistics about authorized rows; this language provides access control, not differential privacy. Threats from unique-key conflicts, authorized counts and catalog shape must be documented without falsely claiming universal non-inference. Native error sanitization remains mandatory.

**N054.** Audit MUST correlate actor/scope, artifact/compiler/profile/schema versions, redacted query shape and typed-value digests, original operation, security/incarnation watermarks, consumed budgets, outcome and publication state. Ordinary logs MUST omit raw SQL literals, parameters, result rows and credentials; query/actor labels must not create unbounded metric cardinality.

Audit retention and support access follow existing platform controls. Model-generated SQL is untrusted source. Disclosing SQL text, schema samples or result data to an external model requires separate current disclosure authorization and must not happen implicitly during execution.

## 21. Multimodel extension framework

**N055.** A language extension MUST register a stable `mensoria` namespace, exact syntax/signatures, parameter/result codecs, NULL behavior, determinism/effects, scope/lineage, limits, index readiness, evidence and versioning before its parser/executor can accept it. Core expressions MUST NOT silently pass through native SurrealQL fragments.

This draft specifies no executable JSON/graph/fulltext/vector function. Their names in discovery are capability reservations only. A future extension specification must define at least:

| Extension | Required additional contract |
| --- | --- |
| JSON | SQL NULL vs JSON null, missing path, extraction/casts, object/array equality, duplicate keys and nesting limits |
| Graph | Edge relation binding, allowed direction/labels, per-hop policies, cycles, depth/edge/vertex limits, result lineage |
| Full-text | Analyzer/language/index revision, match/scoring semantics, authorization prefilter, readiness and deterministic limits |
| Vector | Dimension/metric/value codec, exact vs ANN mode, candidate/output budgets, filter semantics, index generation and recall evaluation |

Existing approved edge collections may be queried as ordinary R2 relations when their bindings qualify; that does not enable graph traversal syntax. Arrow paths, native function calls, live subscriptions and provider-specific vector operators remain rejected.

**N056.** External model calls, embeddings, HTTP/file access, object uploads and job scheduling MUST NOT occur as hidden SQL transaction effects. They remain separate authorized platform commands, with their own external-unknown reconciliation. ANN results must never be advertised as exact relational equivalence.

## 22. Compatibility, versioning and implementation requirements

**N057.** Every accepted artifact MUST bind language version, draft/semantic revision, compiler fingerprint, enabled feature set and schema adapter/backend profile. A semantic change to NULL, numeric conversion, ordering, guard or privilege behavior requires a new compatible version decision and revalidation of affected artifacts.

Adding optional features must not reinterpret previously accepted syntax. Security withdrawal may disable a capability immediately, invalidating cached plans/artifacts/cursors as necessary. There is no guarantee that stale artifacts survive an upgrade. A server must not reinterpret an unknown language or manifest version as version 1.

Parser versions and upstream backend behavior are implementation inputs, not language authorities. A mature parser may be used, but its AST must be exhaustively classified into a closed typed IR; unknown nodes default to denied. SurrealDB SDK/server 3.3.0 is the current repository's pinned reference runtime, not a statement that it already implements this SQL draft.

**N058.** SQL compatibility, native SurrealQL compatibility, PostgreSQL wire compatibility and named client compatibility MUST be reported separately. A P1 document must specify protocol version, authentication/TLS, sessions, Parse/Bind/Execute/Sync/portal behavior, type codecs/OIDs, metadata views, errors, cancel and transaction semantics. This draft grants none of those capabilities.

R1/W1/M1 restrictions such as mandatory CAS, no interactive transactions and a limited catalog are observable compatibility differences. An ORM requiring missing functionality must fail clearly or use an explicitly tested adapter; the service must not pretend a discarded statement succeeded.

## 23. Conformance evidence and release requirements

**N059.** Feature qualification MUST freeze source/build/compiler/parser/backend/storage settings, fixture schema/policies/data, capability limits and complete expected/actual typed results. Negative tests must verify rejection before execution; fault cases must retain uncertain/failed evidence.

Required evidence includes Appendix B's semantic cases and SQL-A01–A16 in [the acceptance map](../../specs/004-surrealdb-rust-ai-baas/mensoria-sql-design-review.md). Differential checks use a fixed reference database only for the shared SQL subset, after documenting deliberate differences. Compare complete ordered sequences with ORDER BY and typed multisets otherwise. Preserve duplicates, NULL tags and precision. Floating/ANN modes require declared tolerances/quality metrics and cannot silently satisfy exact cases.

**N060.** Documentation checks, local parser/runtime tests, CI, driver qualification, real customer acceptance and production qualification MUST be recorded independently. No SQL profile is enabled by the existence of this document, its grammar, synthetic corpus or passing static link checks.

## 24. References

References are informative technical inputs; the numbered normative rules above define Mensoria choices. Checked 2026-10-29. No proprietary ISO standard text has been reproduced or claimed to have been reviewed.

- [PostgreSQL 18 lexical structure](https://www.postgresql.org/docs/18/sql-syntax-lexical.html): practical lexical reference; Mensoria deliberately narrows identifier/literal syntax.
- [PostgreSQL 18 value expressions](https://www.postgresql.org/docs/18/sql-expressions.html): expressions have contextual rules beyond parsing; Mensoria owns its closed subset.
- [PostgreSQL 18 comparisons](https://www.postgresql.org/docs/18/functions-comparison.html): NULL-aware comparison background.
- [PostgreSQL 18 SELECT](https://www.postgresql.org/docs/18/sql-select.html): relational clause reference; no claim to its full grammar.
- [PostgreSQL 18 aggregate functions](https://www.postgresql.org/docs/18/functions-aggregate.html): aggregate type/empty-input reference; Mensoria's decimal result scales and rounding are explicit local choices.
- [PostgreSQL 18 WITH queries](https://www.postgresql.org/docs/18/queries-with.html): CTE background; Mensoria excludes recursion/data modification.
- [PostgreSQL 18 error codes](https://www.postgresql.org/docs/18/errcodes-appendix.html): five-character category reference; Mensoria codes and retry behavior remain distinct.
- [PostgreSQL 18 protocol overview](https://www.postgresql.org/docs/18/protocol-overview.html): driver/session protocol requires a separate contract.
- [SurrealDB NONE and NULL](https://surrealdb.com/docs/reference/query-language/language-primitives/data-types/none-and-null): native absence/null distinction; no automatic SQL equivalence.
- [SurrealDB transactions](https://surrealdb.com/docs/learn/querying/concepts-and-guides/transactions): native execution is an implementation input requiring fixed-version qualification.
- [sqlparser-rs documentation](https://docs.rs/crate/sqlparser/latest): candidate syntactic parser; semantic checks remain Mensoria-owned.

## Appendix A. Closed EBNF grammar

This appendix is normative syntax, qualified by the profile/type/authorization constraints in §§2–23. It is not a claim that a parser has been implemented. `::=` defines a production; `|` is alternation; `[ ... ]` is optional; `{ ... }` repeats zero or more times; quoted strings are terminals; `? ... ?` denotes a lexical scanner rule defined in §4. Whitespace/comments may occur between tokens. Keyword terminals are matched case-insensitively. Longest lexical token applies; <=/>=/<>/!= are single operators.

The grammar includes specified optional features; their presence does not enable them. A context restriction in the normative text takes precedence over a grammatically constructible expression. Unknown AST forms cannot be accepted through grammar recovery.

```ebnf
statement ::= (select_query | insert_statement | update_statement | delete_statement | ddl_statement | explain_statement) [";"] ;

select_query ::= [with_clause] select_chain [order_by_clause] [row_cap] ;
with_clause ::= "WITH" cte_definition {"," cte_definition} ;
cte_definition ::= identifier "AS" "(" select_query ")" ;
select_chain ::= select_core {"UNION" "ALL" select_core} ;
select_core ::= "SELECT" [set_quantifier] projection "FROM" from_clause [where_clause] [group_by_clause] [having_clause] ;
set_quantifier ::= "ALL" | "DISTINCT" ;
projection ::= "*" | identifier "." "*" | select_item {"," select_item} ;
select_item ::= expression ["AS" identifier] ;
from_clause ::= relation_reference [join_clause] ;
relation_reference ::= relation_name [["AS"] identifier] ;
relation_name ::= identifier ["." identifier] ;
join_clause ::= ["INNER" | "LEFT" ["OUTER"]] "JOIN" relation_reference "ON" expression ;
where_clause ::= "WHERE" expression ;
group_by_clause ::= "GROUP" "BY" column_reference {"," column_reference} ;
having_clause ::= "HAVING" expression ;
order_by_clause ::= "ORDER" "BY" order_key {"," order_key} ;
order_key ::= column_reference ["ASC" | "DESC"] ["NULLS" ("FIRST" | "LAST")] ;
row_cap ::= "LIMIT" integer_literal | "FETCH" "FIRST" integer_literal "ROWS" "ONLY" ;

expression ::= or_expression ;
or_expression ::= and_expression {"OR" and_expression} ;
and_expression ::= not_expression {"AND" not_expression} ;
not_expression ::= ["NOT"] predicate ;
predicate ::= "EXISTS" "(" select_query ")" | scalar_expression [predicate_suffix] ;
predicate_suffix ::= comparison_operator scalar_expression | "IS" ["NOT"] "NULL" | ["NOT"] "IN" "(" write_value {"," write_value} ")" ;
comparison_operator ::= "=" | "<>" | "!=" | "<" | "<=" | ">" | ">=" ;
scalar_expression ::= additive_expression {"||" additive_expression} ;
additive_expression ::= multiplicative_expression {("+" | "-") multiplicative_expression} ;
multiplicative_expression ::= unary_expression {("*" | "/") unary_expression} ;
unary_expression ::= [sign] primary ;
primary ::= unsigned_literal | parameter | column_reference | "(" expression ")" | cast_expression | case_expression | coalesce_expression | text_function | aggregate_expression ;
cast_expression ::= "CAST" "(" expression "AS" data_type ")" ;
case_expression ::= "CASE" when_clause {when_clause} ["ELSE" expression] "END" ;
when_clause ::= "WHEN" expression "THEN" expression ;
coalesce_expression ::= "COALESCE" "(" expression "," expression {"," expression} ")" ;
text_function ::= ("CHAR_LENGTH" | "OCTET_LENGTH") "(" expression ")" ;
aggregate_expression ::= "COUNT" "(" ("*" | expression) ")" | ("SUM" | "AVG" | "MIN" | "MAX") "(" expression ")" ;
column_reference ::= identifier ["." identifier] ;

insert_statement ::= "INSERT" "INTO" relation_name "(" column_list ")" "VALUES" value_tuple {"," value_tuple} [returning_clause] ;
column_list ::= identifier {"," identifier} ;
value_tuple ::= "(" write_value {"," write_value} ")" ;
write_value ::= literal | parameter | "CAST" "(" write_value "AS" data_type ")" ;
update_statement ::= "UPDATE" relation_name "SET" assignment {"," assignment} where_clause [returning_clause] ;
assignment ::= identifier "=" write_value ;
delete_statement ::= "DELETE" "FROM" relation_name where_clause [returning_clause] ;
returning_clause ::= "RETURNING" returning_item {"," returning_item} ;
returning_item ::= identifier ["AS" identifier] ;

explain_statement ::= "EXPLAIN" select_query ;
ddl_statement ::= create_table | add_column | create_index | drop_index | drop_table ;
create_table ::= "CREATE" "TABLE" relation_name "(" column_definition {"," column_definition} ")" ;
column_definition ::= identifier data_type [primary_key_clause | not_null_clause] [default_clause] ;
primary_key_clause ::= "PRIMARY" "KEY" ;
not_null_clause ::= "NOT" "NULL" ;
default_clause ::= "DEFAULT" default_value ;
default_value ::= literal | "CAST" "(" default_value "AS" data_type ")" ;
add_column ::= "ALTER" "TABLE" relation_name "ADD" "COLUMN" column_definition ;
create_index ::= "CREATE" "INDEX" identifier "ON" relation_name "(" column_list ")" ;
drop_index ::= "DROP" "INDEX" relation_name ;
drop_table ::= "DROP" "TABLE" relation_name ;

data_type ::= "BOOLEAN" | "BIGINT" | "TEXT" | "UUID" | "NUMERIC" "(" integer_literal "," integer_literal ")" | "DOUBLE" "PRECISION" | "TIMESTAMP" "WITH" "TIME" "ZONE" ;
literal ::= [sign] numeric_literal | string_literal | "TRUE" | "FALSE" | "NULL" ;
unsigned_literal ::= numeric_literal | string_literal | "TRUE" | "FALSE" | "NULL" ;
numeric_literal ::= integer_literal | decimal_literal ;
sign ::= "+" | "-" ;
identifier ::= bare_identifier | quoted_identifier ;
bare_identifier ::= ? ASCII identifier scanner, section 4.1; excludes reserved keywords ? ;
quoted_identifier ::= ? Double-quoted identifier scanner, section 4.1 ? ;
integer_literal ::= ? One or more ASCII digits, section 4.2 ? ;
decimal_literal ::= ? ASCII digits then period then ASCII digits, section 4.2 ? ;
string_literal ::= ? Single-quoted UTF-8 string with doubled apostrophes, section 4.2 ? ;
parameter ::= ? Dollar sign and positive decimal index without leading zero, section 4.2 ? ;
```

Additional contextual grammar restrictions:

- DDL is admitted only by migration preview, EXPLAIN only by the plan path, and DML only with W1; normal SQL execution never admits DDL simply because `statement` can parse it.
- A relation name's optional first component is a schema; a column reference's first component is its active relation qualifier. Semantic binding rejects unsupported schemas.
- R1 permits signed numeric literals but unary signs on columns/parameters/CAST require `expr.numeric_arithmetic`; binary arithmetic/concatenation require their feature. Nested unary signs are not part of this grammar.
- IN list entries are literals/parameters/CAST thereof. They cannot be column expressions or queries.
- W1 where_clause is further limited to the proven conjunctive guard shape in §12.3. M1 ADD COLUMN cannot declare a second primary key or platform column.
- There is no grammar for a client-supplied function name: the enabled named constructs above form a closed set. Future extension syntax requires a new registered grammar revision.

## Appendix B. Worked conformance corpus

The fixtures and expected results below are normative language examples, not executed SQL acceptance. SQL types are part of every expected result; lexical numbers in the tables denote exact logical values, not JSON binary64 conversions. Every SELECT uses an explicit FROM, including constant expression examples.

### B.1 Fixture S: visible logical data

For actor A, all listed columns/rows are readable except the explicitly hidden row. Actual test setup must create these tables through controlled fixture authority; these tables do not exist merely because they appear here.

`public.notes`: id TEXT NOT NULL, revision BIGINT NOT NULL, title TEXT NOT NULL, category TEXT nullable, score BIGINT nullable.

| id | revision | title | category | score |
| --- | --- | --- | --- | --- |
| n1 | 1 | Alpha | a | 10 |
| n2 | 1 | Beta | a | native absence → SQL NULL |
| n3 | 1 | Gamma | SQL NULL | 20 |
| n4 | 1 | Delta | a | 10 |
| n5 | 1 | Epsilon | SQL NULL | SQL NULL |
| n_hidden | 1 | Hidden | secret | 999; row invisible to A |

`public.labels`: id TEXT NOT NULL, revision BIGINT NOT NULL, code TEXT NOT NULL, label TEXT NOT NULL.

| id | revision | code | label |
| --- | --- | --- | --- |
| l1 | 1 | a | Primary |
| l2 | 1 | a | Duplicate |
| l_hidden | 1 | secret | Hidden; row invisible to A |

`public.empty_notes` has the same columns as notes and no rows. Each mutation example starts with a fresh fixture unless it explicitly defines a sequential/concurrent case. Fixture H has the same data but denies actor A access to score; it is used only for denial cases. The duplicate code values in labels are intentional and require no unique constraint.

### B.2 R1 values, NULL and ordering

**C01 — R1, absent/null equivalence.**

```sql
SELECT id FROM public.notes WHERE score IS NULL ORDER BY id;
```

Expected TEXT rows: `[n2]`, `[n5]` in that order. The hidden row never enters evaluation.

**C02 — R1, ordinary NULL equality.**

```sql
SELECT id FROM public.notes WHERE score = NULL ORDER BY id;
```

Expected typed empty result. `NULL = NULL` would also be UNKNOWN, not TRUE.

**C03 — R1, NOT IN with NULL.**

```sql
SELECT id FROM public.notes WHERE score NOT IN (10, NULL) ORDER BY id;
```

Expected empty result: score=10 produces FALSE after NOT; score=20 and NULL produce UNKNOWN.

**C04 — R1, bound text stays data.**

```sql
SELECT id FROM public.notes WHERE title = $1 ORDER BY id;
```

With TEXT `$1 = "x'; DELETE FROM public.notes; --"`, expected empty rows and no mutation. The parameter is never reparsed as SQL.

**C05 — R1 + read.nullable_order, explicit NULL rank.**

```sql
SELECT id, score FROM public.notes
ORDER BY score DESC NULLS LAST, id ASC LIMIT 4;
```

Expected `(TEXT, nullable BIGINT)` rows: `[n3,20]`, `[n1,10]`, `[n4,10]`, `[n2,NULL]`. Without the nullable-order feature, expect SQL_FEATURE_UNSUPPORTED before execution.

**C06 — R1, duplicate labels remain separate.**

```sql
SELECT id AS x, title AS x FROM public.notes WHERE id = 'n1';
```

Expected columns `x TEXT`, `x TEXT`; one ordered row `[n1,Alpha]`. `ORDER BY x` added to this query must produce SQL_AMBIGUOUS_REFERENCE.

### B.3 R2 duplicates, JOIN and aggregates

**C07 — R2, DISTINCT includes one NULL group.**

```sql
SELECT DISTINCT category FROM public.notes ORDER BY category NULLS LAST;
```

Requires read.nullable_order. Expected nullable TEXT rows `[a]`, `[NULL]`.

**C08 — R2, LEFT JOIN preserves multiplicity and unmatched rows.**

```sql
SELECT n.id, l.label FROM public.notes AS n
LEFT JOIN public.labels AS l ON n.category = l.code
ORDER BY n.id, l.label NULLS LAST;
```

Requires read.nullable_order because l.label becomes nullable. Expected `(TEXT, nullable TEXT)` rows: `[n1,Duplicate]`, `[n1,Primary]`, `[n2,Duplicate]`, `[n2,Primary]`, `[n3,NULL]`, `[n4,Duplicate]`, `[n4,Primary]`, `[n5,NULL]`. Hidden rows do not contribute.

**C09 — R2, exact aggregate types and NULL inputs.**

```sql
SELECT COUNT(*) AS rows_n, COUNT(score) AS values_n,
       SUM(score) AS total, AVG(score) AS mean
FROM public.notes;
```

Expected one row: BIGINT 5, BIGINT 3, NUMERIC(38,0) `40`, NUMERIC(38,6) `13.333333`.

**C10 — R2, grouped NULL categories.**

```sql
SELECT category, COUNT(*) AS n, SUM(score) AS total
FROM public.notes GROUP BY category ORDER BY category NULLS LAST;
```

Requires read.nullable_order. Expected rows: `[a,3,20]`, `[NULL,2,20]`; n is BIGINT, total NUMERIC(38,0), category nullable TEXT.

**C11 — R2, empty aggregate vs empty groups.**

```sql
SELECT COUNT(*) AS n, SUM(score) AS total FROM public.empty_notes;
```

Expected one row `[BIGINT 0, NUMERIC(38,0) NULL]`. Adding `GROUP BY category` without projecting category yields zero rows; it does not yield one zero-count group.

**C12 — R2 + expr.numeric_arithmetic, conditional value evaluation.**

```sql
SELECT CASE WHEN score = 0 THEN CAST(0 AS NUMERIC(38,6))
            ELSE 10 / score END AS ratio
FROM public.notes WHERE id = 'n1';
```

Expected NUMERIC(38,6) `1.000000`. In a dedicated fixture where n1.score=0, expected `0.000000`, with no evaluated division-by-zero error. A score=0 row in an aggregate argument would still obey aggregate-before-projection rules.

**C13 — R2, COALESCE common type.**

```sql
SELECT id, COALESCE(score, 0) AS score_value
FROM public.notes WHERE id = 'n2';
```

Expected `[TEXT n2, BIGINT 0]`. `COALESCE(NULL,NULL)` without contextual type is SQL_TYPE_ERROR.

### B.4 Specified optional relational features

**C14 — R2 + read.cte, nonrecursive derived relation.**

```sql
WITH published AS (
    SELECT id, score FROM public.notes WHERE score >= 10
)
SELECT id FROM published ORDER BY id;
```

Expected `[n1]`, `[n3]`, `[n4]`. A recursive/self-reference is SQL_FEATURE_UNSUPPORTED or a sanitized reference error, with no backend execution.

**C15 — R2 + read.exists, authorized uncorrelated existence.**

```sql
SELECT id FROM public.notes
WHERE EXISTS (SELECT 1 FROM public.labels WHERE code = 'secret')
ORDER BY id;
```

Expected empty rows for A: the only matching label is invisible. Changing `'secret'` to `'a'` yields n1–n5.

**C16 — R2 + read.union_all, bag concatenation.**

```sql
SELECT id FROM public.notes WHERE id = 'n1'
UNION ALL
SELECT id FROM public.notes WHERE id = 'n1'
ORDER BY id;
```

Expected two identical TEXT rows `[n1]`, `[n1]`; DISTINCT must not be inferred.

### B.5 W1, M1, types and rejection

**C17 — W1, CAS success.**

```sql
UPDATE public.notes SET title = $1
WHERE id = $2 AND revision = $3
RETURNING id, title, revision;
```

With TEXT `$1=Reviewed`, TEXT `$2=n1`, BIGINT `$3=1`, expected affected_rows `1` and row `[n1,Reviewed,2]`. A separately submitted command with expected revision 1 after this confirmed update returns affected_rows `0`. A same-original-key replay attaches to the first operation and does not increment again.

**C18 — W1, unsafe guards denied.**

```sql
UPDATE public.notes SET title = 'Bad'
WHERE id = 'n1' OR revision = 1;
```

Expected SQL_WRITE_PRECONDITION_REQUIRED before backend mutation. Removing WHERE entirely also cannot execute; it fails grammar validation. `revision=revision` and updates to revision are prohibited.

**C19 — W1, atomic two-item assertion failure.**

Submit two separate C17-shaped artifacts as one request: item 1 targets n1 revision 1, item 2 targets n3 revision 99; both require_affected_rows=1. Expected confirmed SQL_PRECONDITION_FAILED with n1/n3 unchanged. A dropped commit reply instead requires original-key reconciliation and cannot be called a confirmed rollback.

**C20 — M1, Schema proposal only.**

```sql
CREATE TABLE public.review_notes (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT
);
```

Expected a migration proposal in preview; the table is not queryable until actual maintenance/verification/publication completes. Submitting this to ordinary SQL execution must reject it as an unsupported execution class.

**C21 — R1, BIGINT range and explicit type.**

```sql
SELECT CAST($1 AS BIGINT) AS v FROM public.notes WHERE id = 'n1';
```

TEXT `$1=-9223372036854775808` yields exact BIGINT minimum. TEXT `$1=9223372036854775808` yields SQL_VALUE_OUT_OF_RANGE. TEXT `$1=12x` yields SQL_INVALID_TEXT_VALUE.

**C22 — R2, NUMERIC conversion cannot round silently.**

```sql
SELECT CAST($1 AS NUMERIC(5,2)) AS v
FROM public.notes WHERE id = 'n1';
```

TEXT `$1=12.340` yields NUMERIC(5,2) `12.34`; `$1=12.345` yields SQL_VALUE_OUT_OF_RANGE. `$1=1000` also overflows the three integral digits.

**C23 — R1, permission-masked column is not NULL.**

```sql
SELECT id FROM public.notes WHERE score IS NULL ORDER BY id;
```

Under fixture H, expected SQL_REFERENCE_DENIED. It must not return all five visible rows by interpreting masked score as absent/null.

**C24 — R1, paging and invalidation.**

Use a separate 120-row fixture with unique ordered TEXT ids, execute `SELECT id FROM public.page_notes ORDER BY id LIMIT 120` with page_size 50. Expected 50/50/20 rows, result_complete=false/false/true. Revoke the session or change Schema/incarnation before page 2: old cursor must fail and publish no new rows/cursor. This is an expected scenario, not a claim that pagination was executed here.

**C25 — W1, original key and lost reply.**

Inject loss after C17 actually commits, restart the owned API/database as specified by its runtime qualification, then inspect the original operation. Expected one committed update at revision 2 or an explicitly unresolved outcome until authoritative reconciliation; no second mutation or automatically generated key. The runtime qualification must distinguish loss before vs after commit and retain both receipts.

**C26 — R1, catalog and nonexecuting plan.**

```sql
EXPLAIN SELECT id FROM public.notes WHERE id = $1;
```

Declare TEXT parameter type. Expected sanitized logical Scan/Filter/Project information and required features; no business scan, row values, native physical name, hidden cardinality or permission grant.

**C27 — R2 + type.numeric, aggregate result scale.**

A separate table `public.decimals` has id TEXT, value NUMERIC(6,2), rows `[d1,1.00]`, `[d2,2.00]`, `[d3,NULL]` with qualified mappings. `SELECT SUM(value) AS s, AVG(value) AS a FROM public.decimals` yields NUMERIC(38,2) `3.00`, NUMERIC(38,6) `1.500000`.

**C28 — Disabled/deferred syntax.**

```sql
SELECT http::get('https://example.invalid') FROM public.notes;
```

Expected syntax or feature rejection before execution, no external request. A parser recognizing a native call does not permit native fallback. The same rule applies to unsupported graph arrows, UDFs, interactive transactions and unregistered extension functions.

## Appendix C. Explicitly excluded syntax

This list is normative rejection scope, not a promise to implement the listed features later.

| Category | Excluded in this draft |
| --- | --- |
| Lexical convenience | Unicode/space-containing identifiers, dollar strings, escape string prefixes, exponent SQL literals, type-name aliases |
| Query shape | SELECT without FROM, OFFSET, scalar/correlated/IN subqueries, derived-table syntax, SELECT INTO, TABLE shorthand |
| Join | CROSS/NATURAL/RIGHT/FULL/LATERAL, USING, comma joins, nonequijoin, more than two relation references in a query block |
| Group/window | GROUP BY expressions/ordinals, grouping sets/rollup/cube, aggregate DISTINCT/FILTER/ORDER BY, window functions |
| Set expressions | UNION DISTINCT, INTERSECT, EXCEPT, per-branch caps/order |
| Predicates/functions | BETWEEN, LIKE, regex, IS DISTINCT FROM, IS TRUE/FALSE/UNKNOWN, general UDF calls, volatile functions |
| DML | General set UPDATE/DELETE, blind overwrite/upsert, INSERT SELECT, MERGE, generated keys, expression assignments, RETURNING * |
| Transactions | SQL BEGIN/COMMIT/ROLLBACK, savepoints, client-held/open transactions, SET TRANSACTION, distributed transactions |
| DDL/security | Schema/role/user/database creation, GRANT/REVOKE, procedures/triggers, ALTER TYPE/RENAME/DROP COLUMN, TRUNCATE, arbitrary native schema |
| Constraints | General UNIQUE/FOREIGN KEY/CHECK, cascading or deferred constraints, unqualified native index enforcement |
| Native/external | USE, namespace switching, raw record IDs/arrow traversal, native function namespaces, file/network access, COPY/import/export, live query syntax |
| Extensions | Executable JSON/graph/fulltext/vector syntax until a separate registered specification and evidence exists |
| Driver claims | Full pg_catalog/INFORMATION_SCHEMA, PostgreSQL sessions/portals/OIDs, generic ORM/BI compatibility |

A recognized excluded AST may use SQL_FEATURE_UNSUPPORTED; text outside the grammar may use SQL_SYNTAX_ERROR. Both must reject before backend execution. Error classification must not expose protected resource existence.

## Appendix D. Review checklist and revision history

### D.1 Draft completeness criteria

- Every grammar nonterminal resolves; every terminal/lexical category has a rule.
- Every enabled profile has a minimum feature set, semantic rules, applicable corpus and implementation gates.
- Every specified optional feature has dependencies, supported syntax, types/NULL behavior and rejection when disabled.
- Every top-level example names its required profile/features or rejection expectation.
- Type resolution, NULL, bags, joins, aggregates, guards, original-key outcome and publication rules agree across the authorities.
- Documentation, local runtime, CI, client and business/production evidence remain separate.

### D.2 Revision 0.1.0-draft.1

Initial full normative edition. Expands the earlier architecture proposal into a language standard draft; preserves existing architecture/transport/operation ownership. Resolves R2 NUMERIC as mandatory, defines exact aggregate result scales/half-even AVG, specifies a closed grammar and a 28-case worked corpus. No existing SQL implementation or released standard is superseded because none has been qualified here.
