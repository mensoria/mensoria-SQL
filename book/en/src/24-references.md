# 24. References

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
