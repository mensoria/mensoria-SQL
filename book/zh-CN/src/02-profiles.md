# 2. 符合性档位与能力登记表

## 2.1 档位

<a id="n004"></a>

**N004.** 档位启用必须限定作用域、实施版本管理并具有证据支持。解析器能够构造 AST，不得成为启用能力的依据。

| 档位 | 最低必需行为 | 依赖 |
| --- | --- | --- |
| R1 | 单关系 SELECT；BOOLEAN/BIGINT/TEXT；比较、AND/OR/NOT、NULL 检查、IN；别名、标量 CAST、排序、LIMIT/FETCH；已授权元数据和 EXPLAIN | 当前原生身份、策略／结果发布屏障，以及经资格验证的有效预算 |
| W1 | 单行 INSERT；带精确 id/revision 的 UPDATE/DELETE；显式列 RETURNING；原子请求批次 | R1，以及经资格验证的同事务命令向量／收据能力 |
| R2 | DISTINCT；两个关系的 INNER/LEFT 等值连接；GROUP BY/HAVING；五种指定聚合；CASE/COALESCE；NUMERIC(p,s) | R1，以及在有界关系执行下的一致、已授权输入视图 |
| M1 | CREATE TABLE、ADD COLUMN、CREATE/DROP INDEX、DROP TABLE 提案 | R1，以及现有 SchemaAdmin／维护发布流程 |
| X1 | 逐项命名的多模型扩展框架 | R1 及每个扩展各自的前置条件；不整体启用 |
| P1 | 预留的驱动／线协议兼容档位 | 另行规定协议和客户端版本；不属于本语言草案的规定范围 |

R2 不隐含 W1 或 M1；W1 不隐含 R2。M1 不得接受对应类型能力尚未启用的类型。X1 和 P1 单独均不能构成完整的 SQL 支持声明。

<a id="feature-registry"></a>

## 2.2 能力标识符

下列稳定标识符表示语言能力，不是可执行函数名称。必需能力仅随所属档位启用。已规定的可选能力在明确通过资格验证之前保持关闭。

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

<a id="n005"></a>

**N005.** 需要多项能力的语句必须满足这些能力的并集，包括类型和运算符依赖。对于已关闭或暂缓的语法，即便解析器能够识别，也必须在执行前以 `SQL_FEATURE_UNSUPPORTED` 拒绝。

<a id="n006"></a>

**N006.** 在完整档位通过资格验证之前，实现可以开放单独命名的预览能力，但不得宣称该档位已启用。预览仍须遵守所有适用的规范性语义及安全要求。有效限制和档位尚未满足的要求必须能够被查询。
