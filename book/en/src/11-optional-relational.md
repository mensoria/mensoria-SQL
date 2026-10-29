# 11. Optional relational constructs

## 11.1 Nonrecursive CTE

`read.cte` enables `WITH name AS (select), ... select`. Bodies and the main statement must be SELECT queries. CTEs may reference earlier CTEs, never themselves/later entries; duplicate names and cycles are errors. Each CTE projects explicit unique output names; column-name lists, recursive/data-modifying CTEs and materialization hints are deferred. CTE names hide same-named unqualified public tables within the statement; explicit `public.name` still identifies the table.

<a id="n029"></a>

**N029.** A CTE MUST preserve bag, NULL, type, lineage and authorized consistent-view semantics. Materialization/inlining MUST NOT change query results or bypass budgets. Each query block retains the two-relation join limit; the complete statement is also subject to published total relation/node limits.

## 11.2 EXISTS

`read.exists` enables [NOT] EXISTS with an uncorrelated SELECT body, only as a predicate. It returns TRUE when its authorized body result has at least one row, FALSE otherwise; never UNKNOWN. The body must project exactly one literal `1`; bind and authorize all its relation/filter references. Correlation, scalar subqueries, IN subqueries and arbitrary projected EXISTS are deferred.

EXISTS observes the body after its logical WHERE/grouping/cap; thus LIMIT 0 is FALSE, and `SELECT 1` over an aggregate-producing FROM does not become a special shortcut. No EXISTS body may weaken the consistent input-view requirement for its parent query.

## 11.3 UNION ALL

`read.union_all` enables a bounded chain of SELECT branches, with no UNION DISTINCT/INTERSECT/EXCEPT. Branches must have equal arity; each column position resolves to one common type. Labels come from the first branch; output nullability is the union of branch nullabilities. All duplicate rows are preserved.

<a id="n030"></a>

**N030.** UNION ALL branches MUST share the statement's qualified consistent view and authorization lineage. Without a final ORDER BY, branch output order is unspecified. In v1 branches cannot have their own ORDER BY/cap; final ORDER BY refers only to unique output labels, and final cap applies to the entire union.

CTE/EXISTS/UNION can combine only when every required feature is enabled and the full AST obeys the grammar, depth and budget rules. Optional syntax does not loosen parent query restrictions.
