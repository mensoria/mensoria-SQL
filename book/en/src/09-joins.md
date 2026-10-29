# 9. JOIN

R2 supports one INNER JOIN or LEFT [OUTER] JOIN between two relation references. Plain JOIN is INNER JOIN. Each side must have an unambiguous alias when a qualifier would otherwise be ambiguous. RIGHT/FULL/CROSS/NATURAL JOIN, USING, comma joins and lateral joins are deferred.

<a id="n025"></a>

**N025.** ON MUST be a nonempty conjunction of typed equalities, each comparing a column from the left relation with a column from the right relation. No OR, constants, residual inequalities or effects are allowed in v1 join conditions. Each input MUST already satisfy its own current native row policy.

INNER JOIN emits every matching pair, preserving multiplicity. LEFT JOIN emits every matching pair, or one null-extended right tuple when no authorized right tuple matches. Native absence and SQL NULL do not match on ordinary equality. WHERE runs after JOIN; filtering a null-extended right column can remove the output row.

<a id="n026"></a>

**N026.** Both input relations MUST be read from one qualified consistent view; joining independent live paginated API results is prohibited. A planner MUST NOT replace a LEFT JOIN with INNER JOIN or move a WHERE predicate into ON unless equivalent under SQL NULL, duplicates and policy rules.

A qualified input view is an internal execution guarantee, not permission to advertise a named PostgreSQL isolation level. An ordinary R1 cursor may still be a mutable live list across separately executed pages.
