# Feature index

[Profile definitions and normative registry](02-profiles.md#feature-registry). This is a reference copy of the registry; it does not enable features.

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
