# 语句索引

| 结构 | 档位／边界 | 参考 |
| --- | --- | --- |
| SELECT / ORDER BY / LIMIT / FETCH | R1 | [章节](08-select.md) |
| CAST / NULL / IN / CASE / COALESCE | R1；CASE/COALESCE 要求 R2 | [章节](07-expressions.md) |
| INNER JOIN / LEFT JOIN | R2 | [章节](09-joins.md) |
| GROUP BY / HAVING / COUNT / SUM / AVG / MIN / MAX | R2 | [章节](10-aggregates.md) |
| WITH / EXISTS / UNION ALL | R2 加各项独立能力开关 | [章节](11-optional-relational.md) |
| INSERT / UPDATE / DELETE / RETURNING | W1；精确 id/revision 守卫 | [章节](12-data-modification.md) |
| 原子请求批次／原始键核对 | W1；通过请求 API，不提供 BEGIN/COMMIT | [章节](13-transactions.md) |
| CREATE TABLE / ALTER TABLE ADD COLUMN / CREATE INDEX / DROP | M1；仅提案路径 | [章节](14-schema-migrations.md) |
| EXPLAIN | R1；不支持 ANALYZE | [章节](16-artifacts-explain.md) |

请先查阅[排除语法](appendix-c-excluded-syntax.md)，不要假定其他数据库的 SQL 能力自动适用。
