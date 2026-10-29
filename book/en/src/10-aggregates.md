# 10. Grouping and aggregates

GROUP BY accepts explicit input column references only; output aliases, ordinals, expression grouping, rollup/cube/grouping sets and functional-dependency relaxation are deferred. Grouping without an aggregate is permitted and yields one row per group. SQL NULL values form one group; composite group equality follows tuple semantics.

<a id="n027"></a>

**N027.** In a grouped query, every nonaggregate column reference in SELECT/HAVING/ORDER BY MUST be a GROUP BY key. In an aggregate query without GROUP BY, no nonaggregate input columns may be projected or referenced in HAVING/ORDER BY. Aggregate calls are allowed only in SELECT/HAVING and cannot nest.

HAVING requires a grouped or aggregate query and keeps only TRUE. WHERE/ON/GROUP BY cannot contain aggregate calls. ORDER BY may use a unique projected aggregate alias, but not a new aggregate expression. Aggregate DISTINCT, FILTER, ordered aggregates and window clauses are deferred.

| Signature | Result type | Empty/all-NULL behavior |
| --- | --- | --- |
| COUNT(*) | BIGINT NOT NULL | 0 |
| COUNT(x), x any enabled scalar | BIGINT NOT NULL | 0 |
| SUM(BIGINT) | NUMERIC(38,0) | NULL |
| SUM(NUMERIC(p,s)) | NUMERIC(38,s) | NULL |
| AVG(BIGINT) | NUMERIC(38,6) | NULL |
| AVG(NUMERIC(p,s)) | NUMERIC(38,max(s,6)) | NULL |
| MIN/MAX(x), x BOOLEAN/BIGINT/TEXT/NUMERIC/timestamp | Same type as x | NULL |
| SUM/AVG(DOUBLE) | DOUBLE PRECISION | NULL |
| MIN/MAX(DOUBLE) | DOUBLE PRECISION | NULL |

Optional type signatures require the corresponding feature. UUID is allowed in COUNT/DISTINCT/GROUP BY but not MIN/MAX. NUMERIC is mandatory in R2 so BIGINT aggregates always have a defined exact result representation.

<a id="n028"></a>

**N028.** Aggregates except COUNT(*) MUST ignore SQL NULL inputs. SUM of exact values MUST use a mathematically exact accumulator and check the final declared result; AVG MUST divide the exact sum by the count and round half-even once to its declared scale. A result that cannot fit MUST error. COUNT overflow also errors.

Floating aggregate accumulation order can vary; its codec/algorithm, allowed comparison tolerance and repeatability limits must be published. A floating result cannot pass exact numeric equivalence merely because a finite value was returned. SUM/AVG cannot silently truncate a dataset to satisfy a work budget.

On zero input rows, an aggregate query without GROUP BY produces exactly one aggregate row before HAVING; a query with GROUP BY produces zero groups. MIN/MAX text use byte ordering. Nullable aggregate metadata is retained even when the current input is nonempty.
