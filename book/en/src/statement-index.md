# Statement index

| Construct | Profile / boundary | Reference |
| --- | --- | --- |
| SELECT / ORDER BY / LIMIT / FETCH | R1 | [Chapter](08-select.md) |
| CAST / NULL / IN / CASE / COALESCE | R1; CASE/COALESCE R2 | [Chapter](07-expressions.md) |
| INNER JOIN / LEFT JOIN | R2 | [Chapter](09-joins.md) |
| GROUP BY / HAVING / COUNT / SUM / AVG / MIN / MAX | R2 | [Chapter](10-aggregates.md) |
| WITH / EXISTS / UNION ALL | R2 + individual flags | [Chapter](11-optional-relational.md) |
| INSERT / UPDATE / DELETE / RETURNING | W1; exact id/revision guards | [Chapter](12-data-modification.md) |
| Atomic request batch / original-key reconciliation | W1; request API, not BEGIN/COMMIT | [Chapter](13-transactions.md) |
| CREATE TABLE / ALTER TABLE ADD COLUMN / CREATE INDEX / DROP | M1; proposal path only | [Chapter](14-schema-migrations.md) |
| EXPLAIN | R1; no ANALYZE | [Chapter](16-artifacts-explain.md) |

See [excluded syntax](appendix-c-excluded-syntax.md) before assuming another SQL feature is accepted.
