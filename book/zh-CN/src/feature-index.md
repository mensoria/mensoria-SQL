# 能力索引

[档位定义与规范登记表](02-profiles.md#feature-registry)。本页为查阅副本，不启用能力。

| 能力 ID | 状态／所属档位 | 规则 |
| --- | --- | --- |
| `read.single_relation` | R1 必需 | 第 3、8 节 |
| `expr.boolean_predicates` | R1 必需 | 第 7 节 |
| `expr.in_list` | R1 必需 | 第 7 节 |
| `type.boolean_bigint_text` | R1 必需 | 第 5–6 节 |
| `read.order_limit` | R1 必需 | 第 8 节 |
| `catalog.scoped` | R1 必需 | 第 15 节 |
| `plan.explain` | R1 必需 | 第 16 节 |
| `read.nullable_order` | R1 已规定的可选能力 | 第 8、17 节 |
| `type.uuid` | R1 已规定的可选能力 | 第 5–6 节 |
| `write.cas` | W1 必需 | 第 12 节 |
| `write.returning` | W1 必需 | 第 12 节 |
| `write.atomic_batch` | W1 必需 | 第 13 节 |
| `write.multi_values` | W1 已规定的可选能力 | 第 12–13 节 |
| `read.distinct` | R2 必需 | 第 8 节 |
| `read.equijoin` | R2 必需 | 第 9 节 |
| `read.group_aggregate` | R2 必需 | 第 10 节 |
| `expr.case_coalesce` | R2 必需 | 第 7 节 |
| `type.numeric` | R2 必需 | 第 5–6、10 节 |
| `expr.numeric_arithmetic` | R2 已规定的可选能力 | 第 7 节 |
| `expr.text_basic` | R2 已规定的可选能力 | 第 7 节 |
| `read.cte` | R2 已规定的可选能力 | 第 11 节 |
| `read.exists` | R2 已规定的可选能力 | 第 11 节 |
| `read.union_all` | R2 已规定的可选能力 | 第 11 节 |
| `type.double` | R2 已规定的可选能力 | 第 5–6、10 节 |
| `type.timestamptz` | R2 已规定的可选能力 | 第 5–6 节 |
| `schema.proposal` | M1 必需 | 第 14 节 |
| `schema.literal_default` | M1 已规定的可选能力 | 第 14 节 |
| `extension.json` | X1 暂缓 | 第 21 节仅规定登记要求 |
| `extension.graph` | X1 暂缓 | 第 21 节仅规定登记要求 |
| `extension.fulltext` | X1 暂缓 | 第 21 节仅规定登记要求 |
| `extension.vector` | X1 暂缓 | 第 21 节仅规定登记要求 |
| `driver.postgresql` | P1 预留 | 需要单独的驱动规范 |
