# 2. Conformance profiles and feature registry

## 2.1 Profiles

<a id="n004"></a>

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

<a id="feature-registry"></a>

## 2.2 Feature identifiers

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

<a id="n005"></a>

**N005.** A statement requiring multiple features MUST satisfy their union, including type and operator dependencies. Disabled or deferred syntax MUST fail before execution with `SQL_FEATURE_UNSUPPORTED`, even when the parser recognizes it.

<a id="n006"></a>

**N006.** An implementation MAY expose separately named preview features before a complete profile qualifies, but MUST NOT advertise that profile as enabled. A preview still obeys every applicable normative semantic/security requirement. Effective limits and missing profile requirements MUST be discoverable.
