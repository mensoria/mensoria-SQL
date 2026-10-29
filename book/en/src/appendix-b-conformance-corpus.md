# Appendix B. Worked conformance corpus

The fixtures and expected results below are normative language examples, not executed SQL acceptance. SQL types are part of every expected result; lexical numbers in the tables denote exact logical values, not JSON binary64 conversions. Every SELECT uses an explicit FROM, including constant expression examples.

## B.1 Fixture S: visible logical data

For actor A, all listed columns/rows are readable except the explicitly hidden row. Actual test setup must create these tables through controlled fixture authority; these tables do not exist merely because they appear here.

`public.notes`: id TEXT NOT NULL, revision BIGINT NOT NULL, title TEXT NOT NULL, category TEXT nullable, score BIGINT nullable.

| id | revision | title | category | score |
| --- | --- | --- | --- | --- |
| n1 | 1 | Alpha | a | 10 |
| n2 | 1 | Beta | a | native absence → SQL NULL |
| n3 | 1 | Gamma | SQL NULL | 20 |
| n4 | 1 | Delta | a | 10 |
| n5 | 1 | Epsilon | SQL NULL | SQL NULL |
| n_hidden | 1 | Hidden | secret | 999; row invisible to A |

`public.labels`: id TEXT NOT NULL, revision BIGINT NOT NULL, code TEXT NOT NULL, label TEXT NOT NULL.

| id | revision | code | label |
| --- | --- | --- | --- |
| l1 | 1 | a | Primary |
| l2 | 1 | a | Duplicate |
| l_hidden | 1 | secret | Hidden; row invisible to A |

`public.empty_notes` has the same columns as notes and no rows. Each mutation example starts with a fresh fixture unless it explicitly defines a sequential/concurrent case. Fixture H has the same data but denies actor A access to score; it is used only for denial cases. The duplicate code values in labels are intentional and require no unique constraint.

## B.2 R1 values, NULL and ordering

<a id="c01"></a>

**C01 — R1, absent/null equivalence.**

```sql
SELECT id FROM public.notes WHERE score IS NULL ORDER BY id;
```

Expected TEXT rows: `[n2]`, `[n5]` in that order. The hidden row never enters evaluation.

<a id="c02"></a>

**C02 — R1, ordinary NULL equality.**

```sql
SELECT id FROM public.notes WHERE score = NULL ORDER BY id;
```

Expected typed empty result. `NULL = NULL` would also be UNKNOWN, not TRUE.

<a id="c03"></a>

**C03 — R1, NOT IN with NULL.**

```sql
SELECT id FROM public.notes WHERE score NOT IN (10, NULL) ORDER BY id;
```

Expected empty result: score=10 produces FALSE after NOT; score=20 and NULL produce UNKNOWN.

<a id="c04"></a>

**C04 — R1, bound text stays data.**

```sql
SELECT id FROM public.notes WHERE title = $1 ORDER BY id;
```

With TEXT `$1 = "x'; DELETE FROM public.notes; --"`, expected empty rows and no mutation. The parameter is never reparsed as SQL.

<a id="c05"></a>

**C05 — R1 + read.nullable_order, explicit NULL rank.**

```sql
SELECT id, score FROM public.notes
ORDER BY score DESC NULLS LAST, id ASC LIMIT 4;
```

Expected `(TEXT, nullable BIGINT)` rows: `[n3,20]`, `[n1,10]`, `[n4,10]`, `[n2,NULL]`. Without the nullable-order feature, expect SQL_FEATURE_UNSUPPORTED before execution.

<a id="c06"></a>

**C06 — R1, duplicate labels remain separate.**

```sql
SELECT id AS x, title AS x FROM public.notes WHERE id = 'n1';
```

Expected columns `x TEXT`, `x TEXT`; one ordered row `[n1,Alpha]`. `ORDER BY x` added to this query must produce SQL_AMBIGUOUS_REFERENCE.

## B.3 R2 duplicates, JOIN and aggregates

<a id="c07"></a>

**C07 — R2, DISTINCT includes one NULL group.**

```sql
SELECT DISTINCT category FROM public.notes ORDER BY category NULLS LAST;
```

Requires read.nullable_order. Expected nullable TEXT rows `[a]`, `[NULL]`.

<a id="c08"></a>

**C08 — R2, LEFT JOIN preserves multiplicity and unmatched rows.**

```sql
SELECT n.id, l.label FROM public.notes AS n
LEFT JOIN public.labels AS l ON n.category = l.code
ORDER BY n.id, l.label NULLS LAST;
```

Requires read.nullable_order because l.label becomes nullable. Expected `(TEXT, nullable TEXT)` rows: `[n1,Duplicate]`, `[n1,Primary]`, `[n2,Duplicate]`, `[n2,Primary]`, `[n3,NULL]`, `[n4,Duplicate]`, `[n4,Primary]`, `[n5,NULL]`. Hidden rows do not contribute.

<a id="c09"></a>

**C09 — R2, exact aggregate types and NULL inputs.**

```sql
SELECT COUNT(*) AS rows_n, COUNT(score) AS values_n,
       SUM(score) AS total, AVG(score) AS mean
FROM public.notes;
```

Expected one row: BIGINT 5, BIGINT 3, NUMERIC(38,0) `40`, NUMERIC(38,6) `13.333333`.

<a id="c10"></a>

**C10 — R2, grouped NULL categories.**

```sql
SELECT category, COUNT(*) AS n, SUM(score) AS total
FROM public.notes GROUP BY category ORDER BY category NULLS LAST;
```

Requires read.nullable_order. Expected rows: `[a,3,20]`, `[NULL,2,20]`; n is BIGINT, total NUMERIC(38,0), category nullable TEXT.

<a id="c11"></a>

**C11 — R2, empty aggregate vs empty groups.**

```sql
SELECT COUNT(*) AS n, SUM(score) AS total FROM public.empty_notes;
```

Expected one row `[BIGINT 0, NUMERIC(38,0) NULL]`. Adding `GROUP BY category` without projecting category yields zero rows; it does not yield one zero-count group.

<a id="c12"></a>

**C12 — R2 + expr.numeric_arithmetic, conditional value evaluation.**

```sql
SELECT CASE WHEN score = 0 THEN CAST(0 AS NUMERIC(38,6))
            ELSE 10 / score END AS ratio
FROM public.notes WHERE id = 'n1';
```

Expected NUMERIC(38,6) `1.000000`. In a dedicated fixture where n1.score=0, expected `0.000000`, with no evaluated division-by-zero error. A score=0 row in an aggregate argument would still obey aggregate-before-projection rules.

<a id="c13"></a>

**C13 — R2, COALESCE common type.**

```sql
SELECT id, COALESCE(score, 0) AS score_value
FROM public.notes WHERE id = 'n2';
```

Expected `[TEXT n2, BIGINT 0]`. `COALESCE(NULL,NULL)` without contextual type is SQL_TYPE_ERROR.

## B.4 Specified optional relational features

<a id="c14"></a>

**C14 — R2 + read.cte, nonrecursive derived relation.**

```sql
WITH published AS (
    SELECT id, score FROM public.notes WHERE score >= 10
)
SELECT id FROM published ORDER BY id;
```

Expected `[n1]`, `[n3]`, `[n4]`. A recursive/self-reference is SQL_FEATURE_UNSUPPORTED or a sanitized reference error, with no backend execution.

<a id="c15"></a>

**C15 — R2 + read.exists, authorized uncorrelated existence.**

```sql
SELECT id FROM public.notes
WHERE EXISTS (SELECT 1 FROM public.labels WHERE code = 'secret')
ORDER BY id;
```

Expected empty rows for A: the only matching label is invisible. Changing `'secret'` to `'a'` yields n1–n5.

<a id="c16"></a>

**C16 — R2 + read.union_all, bag concatenation.**

```sql
SELECT id FROM public.notes WHERE id = 'n1'
UNION ALL
SELECT id FROM public.notes WHERE id = 'n1'
ORDER BY id;
```

Expected two identical TEXT rows `[n1]`, `[n1]`; DISTINCT must not be inferred.

## B.5 W1, M1, types and rejection

<a id="c17"></a>

**C17 — W1, CAS success.**

```sql
UPDATE public.notes SET title = $1
WHERE id = $2 AND revision = $3
RETURNING id, title, revision;
```

With TEXT `$1=Reviewed`, TEXT `$2=n1`, BIGINT `$3=1`, expected affected_rows `1` and row `[n1,Reviewed,2]`. A separately submitted command with expected revision 1 after this confirmed update returns affected_rows `0`. A same-original-key replay attaches to the first operation and does not increment again.

<a id="c18"></a>

**C18 — W1, unsafe guards denied.**

```sql
UPDATE public.notes SET title = 'Bad'
WHERE id = 'n1' OR revision = 1;
```

Expected SQL_WRITE_PRECONDITION_REQUIRED before backend mutation. Removing WHERE entirely also cannot execute; it fails grammar validation. `revision=revision` and updates to revision are prohibited.

<a id="c19"></a>

**C19 — W1, atomic two-item assertion failure.**

Submit two separate C17-shaped artifacts as one request: item 1 targets n1 revision 1, item 2 targets n3 revision 99; both require_affected_rows=1. Expected confirmed SQL_PRECONDITION_FAILED with n1/n3 unchanged. A dropped commit reply instead requires original-key reconciliation and cannot be called a confirmed rollback.

<a id="c20"></a>

**C20 — M1, Schema proposal only.**

```sql
CREATE TABLE public.review_notes (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT
);
```

Expected a migration proposal in preview; the table is not queryable until actual maintenance/verification/publication completes. Submitting this to ordinary SQL execution must reject it as an unsupported execution class.

<a id="c21"></a>

**C21 — R1, BIGINT range and explicit type.**

```sql
SELECT CAST($1 AS BIGINT) AS v FROM public.notes WHERE id = 'n1';
```

TEXT `$1=-9223372036854775808` yields exact BIGINT minimum. TEXT `$1=9223372036854775808` yields SQL_VALUE_OUT_OF_RANGE. TEXT `$1=12x` yields SQL_INVALID_TEXT_VALUE.

<a id="c22"></a>

**C22 — R2, NUMERIC conversion cannot round silently.**

```sql
SELECT CAST($1 AS NUMERIC(5,2)) AS v
FROM public.notes WHERE id = 'n1';
```

TEXT `$1=12.340` yields NUMERIC(5,2) `12.34`; `$1=12.345` yields SQL_VALUE_OUT_OF_RANGE. `$1=1000` also overflows the three integral digits.

<a id="c23"></a>

**C23 — R1, permission-masked column is not NULL.**

```sql
SELECT id FROM public.notes WHERE score IS NULL ORDER BY id;
```

Under fixture H, expected SQL_REFERENCE_DENIED. It must not return all five visible rows by interpreting masked score as absent/null.

<a id="c24"></a>

**C24 — R1, paging and invalidation.**

Use a separate 120-row fixture with unique ordered TEXT ids, execute `SELECT id FROM public.page_notes ORDER BY id LIMIT 120` with page_size 50. Expected 50/50/20 rows, result_complete=false/false/true. Revoke the session or change Schema/incarnation before page 2: old cursor must fail and publish no new rows/cursor. This is an expected scenario, not a claim that pagination was executed here.

<a id="c25"></a>

**C25 — W1, original key and lost reply.**

Inject loss after C17 actually commits, restart the owned API/database as specified by its runtime qualification, then inspect the original operation. Expected one committed update at revision 2 or an explicitly unresolved outcome until authoritative reconciliation; no second mutation or automatically generated key. The runtime qualification must distinguish loss before vs after commit and retain both receipts.

<a id="c26"></a>

**C26 — R1, catalog and nonexecuting plan.**

```sql
EXPLAIN SELECT id FROM public.notes WHERE id = $1;
```

Declare TEXT parameter type. Expected sanitized logical Scan/Filter/Project information and required features; no business scan, row values, native physical name, hidden cardinality or permission grant.

<a id="c27"></a>

**C27 — R2 + type.numeric, aggregate result scale.**

A separate table `public.decimals` has id TEXT, value NUMERIC(6,2), rows `[d1,1.00]`, `[d2,2.00]`, `[d3,NULL]` with qualified mappings. `SELECT SUM(value) AS s, AVG(value) AS a FROM public.decimals` yields NUMERIC(38,2) `3.00`, NUMERIC(38,6) `1.500000`.

<a id="c28"></a>

**C28 — Disabled/deferred syntax.**

```sql
SELECT http::get('https://example.invalid') FROM public.notes;
```

Expected syntax or feature rejection before execution, no external request. A parser recognizing a native call does not permit native fallback. The same rule applies to unsupported graph arrows, UDFs, interactive transactions and unregistered extension functions.
