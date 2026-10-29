# 10. 分组与聚合

GROUP BY 仅接受显式输入列引用；输出别名、序号、表达式分组、rollup/cube/grouping sets 及基于函数依赖放宽分组约束均暂缓。允许无聚合的分组，每组输出一行。SQL NULL 值形成同一组；复合分组相等性遵循元组语义。

<a id="n027"></a>

**N027.** 在分组查询中，SELECT/HAVING/ORDER BY 内所有非聚合列引用都必须是 GROUP BY 键。在没有 GROUP BY 的聚合查询中，不得投影非聚合输入列，也不得在 HAVING/ORDER BY 中引用这些列。聚合调用仅允许出现在 SELECT/HAVING，且不得嵌套。

HAVING 要求查询存在分组或聚合，仅保留 TRUE。WHERE/ON/GROUP BY 不得包含聚合调用。ORDER BY 可以使用唯一的已投影聚合别名，但不能引入新的聚合表达式。聚合 DISTINCT、FILTER、有序聚合及窗口子句暂缓。

| 签名 | 结果类型 | 空输入／全部为 NULL 时的行为 |
| --- | --- | --- |
| COUNT(*) | BIGINT NOT NULL | 0 |
| COUNT(x)，x 为任意已启用标量 | BIGINT NOT NULL | 0 |
| SUM(BIGINT) | NUMERIC(38,0) | NULL |
| SUM(NUMERIC(p,s)) | NUMERIC(38,s) | NULL |
| AVG(BIGINT) | NUMERIC(38,6) | NULL |
| AVG(NUMERIC(p,s)) | NUMERIC(38,max(s,6)) | NULL |
| MIN/MAX(x)，x 为 BOOLEAN/BIGINT/TEXT/NUMERIC/时间戳 | 与 x 相同的类型 | NULL |
| SUM/AVG(DOUBLE) | DOUBLE PRECISION | NULL |
| MIN/MAX(DOUBLE) | DOUBLE PRECISION | NULL |

可选类型签名要求相应能力。UUID 允许用于 COUNT/DISTINCT/GROUP BY，但不允许用于 MIN/MAX。NUMERIC 是 R2 必需能力，确保 BIGINT 聚合始终具有明确的精确结果表示。

<a id="n028"></a>

**N028.** 除 COUNT(*) 外的聚合必须忽略 SQL NULL 输入。精确数值的 SUM 必须使用数学上精确的累加器，并检查最终声明结果；AVG 必须用精确总和除以计数，并仅在生成其声明的小数位数时按恰好中点取偶数舍入一次。结果无法容纳时必须报错。COUNT 溢出也报错。

浮点聚合的累加顺序可以变化，必须公布其编解码器／算法、允许的比较误差及可重复性限制。不能仅因返回了有限浮点值，就认为满足精确数值等价性。SUM/AVG 不得为了满足工作预算而静默截断数据集。

输入为零行时，无 GROUP BY 的聚合查询在 HAVING 前恰好产生一行聚合结果；有 GROUP BY 的查询产生零个组。TEXT 的 MIN/MAX 使用字节序。即使当前输入非空，也保留聚合结果的可空元数据。
