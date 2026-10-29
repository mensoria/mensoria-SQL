# 7. Expressions, predicates and NULL

## 7.1 Boolean and comparison semantics

<a id="n018"></a>

**N018.** WHERE, ON, HAVING and searched CASE conditions MUST be BOOLEAN. They MUST NOT use numeric/string/native truthiness. Only TRUE passes a filter or ON match; FALSE and UNKNOWN do not.

| A | B | A AND B | A OR B |
| --- | --- | --- | --- |
| TRUE | TRUE | TRUE | TRUE |
| TRUE | FALSE | FALSE | TRUE |
| TRUE | UNKNOWN | UNKNOWN | TRUE |
| FALSE | FALSE | FALSE | FALSE |
| FALSE | UNKNOWN | FALSE | UNKNOWN |
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

AND/OR are commutative. NOT TRUE=FALSE; NOT FALSE=TRUE; NOT UNKNOWN=UNKNOWN. UNKNOWN is the truth interpretation of a NULL BOOLEAN; it is not a separate stored scalar tag.

`=`, `<>`, `<`, `<=`, `>`, `>=` operate on comparable common types. `!=` is accepted as an alias for `<>`. An ordinary comparison involving SQL NULL yields UNKNOWN, including NULL against NULL. UUID permits only equality/inequality until a separately specified ordering feature exists. `IS NULL` and `IS NOT NULL` return nonnullable BOOLEAN.

`x IN (a,b,...)` is TRUE if any typed comparison is TRUE, otherwise UNKNOWN if any comparison is UNKNOWN, otherwise FALSE. NOT IN applies logical NOT. Lists must be nonempty and scalar; IN subqueries, row constructors and array membership are deferred. A NULL left operand therefore yields UNKNOWN against a nonempty list.

<a id="n019"></a>

**N019.** Boolean evaluation order is not a user-visible short-circuit guarantee. Validation MUST inspect all branches, including unreachable branches, for resource/type/effect permission. CASE/COALESCE value evaluation follows §7.2, but it MUST NOT suppress binding errors in a branch.

## 7.2 CASE and COALESCE, R2

Searched `CASE WHEN condition THEN value ... [ELSE value] END` returns the first branch whose condition is TRUE; omitted ELSE returns typed SQL NULL. All result branches resolve to one common type. Conditions may be FALSE or UNKNOWN and continue to later branches. Simple CASE is deferred.

`COALESCE(a,b,...)` requires at least two arguments with one common result type; returns the first non-NULL argument, or typed NULL if all are NULL. An all-untyped-NULL argument set is rejected unless an explicit cast supplies the common type.

<a id="n020"></a>

**N020.** For scalar expressions, an unchosen CASE result and COALESCE arguments after the chosen value MUST NOT raise a runtime value error. The compiler MUST still bind/authorize their contents. Group aggregates are computed before SELECT scalar CASE and cannot be guarded from aggregate errors by CASE.

## 7.3 Optional arithmetic and text expressions

`expr.numeric_arithmetic` enables unary +/- and binary +,-,*,/ for same-resolved-domain numeric operands. Unary sign propagates SQL NULL. A binary operator whose evaluated operand is SQL NULL returns typed SQL NULL, including typed NULL divided by zero; the division operator checks zero only when both operands are non-NULL. Each operand expression must still be evaluated for its own errors (in either order), so NULL plus an independently failing CAST is an error. CASE/COALESCE retain their explicit lazy value-branch semantics. BIGINT +,-,* return BIGINT with checked overflow; BIGINT / BIGINT returns NUMERIC(38,6) with round-half-even. Division by zero errors. Mixed BIGINT/NUMERIC first resolves exactly under §6; all NUMERIC operations use the rules below. DOUBLE combines only with DOUBLE, returns finite binary64 and rejects nonfinite results/division by zero.

NUMERIC +,- return NUMERIC(38,max(s1,s2)); multiplication returns NUMERIC(38,min(38,s1+s2)) but MUST reject rather than discard any nonzero fractional digits beyond scale 38. NUMERIC division returns NUMERIC(38,max(s1,s2,6)), rounding half-even once to the result scale. All operations reject a result whose integral part cannot fit. Arithmetic precision/scale are derived before execution and do not change by row value.

`expr.text_basic` enables TEXT concatenation `||`, `CHAR_LENGTH(TEXT) -> BIGINT`, and `OCTET_LENGTH(TEXT) -> BIGINT`. Concatenation and both functions are NULL-propagating. Character length counts Unicode scalar values, not grapheme clusters; octet length counts UTF-8 bytes. No implicit scalar-to-TEXT conversion. LIKE, regex, LOWER/UPPER, locale collation and user functions are deferred.

Operator precedence, highest to lowest: parentheses/CAST/function/CASE; unary sign; */; binary +/-; ||; comparison/IN/IS NULL; NOT; AND; OR. Binary arithmetic and concatenation associate left. Comparisons cannot chain: `1 < 2 < 3` is invalid.
