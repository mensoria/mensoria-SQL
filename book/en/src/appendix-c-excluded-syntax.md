# Appendix C. Explicitly excluded syntax

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
