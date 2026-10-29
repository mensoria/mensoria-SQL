# 6. Type resolution and casts

## 6.1 General resolution

<a id="n016"></a>

**N016.** Repeated occurrences of a parameter MUST resolve to a single declared type. Positions MUST be contiguous from 1 and bindings MUST contain exactly those positions. Types cannot be inferred from a backend execution trial.

An untyped NULL adopts the other comparison/assignment/CASE/COALESCE/UNION operand type when one unambiguous common type exists. `NULL IS NULL` is valid without a scalar payload type because the result is nonnullable BOOLEAN. `NULL = NULL` is valid and yields nullable BOOLEAN UNKNOWN; the compiler may use an internal null-only type for these comparisons. A bare projected NULL, an all-NULL CASE/COALESCE result, or an unconstrained parameter requires explicit type declaration/CAST.

Comparison, CASE, COALESCE and UNION common types are:

1. Identical types retain that type.
2. BIGINT may widen to NUMERIC(19,0) when combined with NUMERIC; the resolved p/s must exactly represent both domains.
3. Two NUMERIC(p,s) types resolve to scale=max(s1,s2) and integral digits=max(p1-s1,p2-s2); p=integral+scale. If p>38, reject the expression at binding; never silently reduce scale.
4. No implicit TEXT/numeric/BOOLEAN/UUID/timestamp conversion; no implicit exact-number/DOUBLE conversion.

## 6.2 Explicit CAST

<a id="n017"></a>

**N017.** CAST MUST either produce the specified type exactly, except explicitly defined floating conversion, or report a typed error. SQL NULL casts to any enabled scalar type and remains SQL NULL.

| Source → target | Behavior |
| --- | --- |
| Same type | Identity, subject to target typemod validation |
| TEXT → BIGINT | Optional sign plus digits only, no whitespace; signed 64-bit range |
| TEXT → BOOLEAN | Case-insensitive `true` or `false` only, no whitespace |
| TEXT → NUMERIC(p,s) | Signed decimal/integer notation only; no exponent; target scale padding allowed, nonzero discarded digits rejected |
| BIGINT / NUMERIC → NUMERIC(p,s) | Exact representation required; excess fractional zeros may be removed, no rounding |
| NUMERIC → BIGINT | Fractional part must be zero and value in range |
| BIGINT / NUMERIC → DOUBLE | Only with `type.double`; explicitly permitted binary64 round-to-nearest-ties-even; overflow rejected |
| TEXT → DOUBLE | Strict finite decimal/exponent parser named in the backend profile; surrounding whitespace, NaN and infinity rejected |
| TEXT → UUID | Standard hyphenated 8-4-4-4-12 hexadecimal form, case-insensitive input; canonical lowercase output |
| TEXT → TIMESTAMP WITH TIME ZONE | RFC3339 date/time with `T`, seconds and mandatory `Z` or ±HH:MM; <= 6 fractional digits, no leap seconds |
| BIGINT/NUMERIC/BOOLEAN/UUID/timestamp → TEXT | Locale-independent canonical codec spelling; timestamp UTC `Z` |

DOUBLE → TEXT uses a pinned shortest-round-trip finite codec; DOUBLE → exact number is deferred. Timestamp conversion rejects `-00:00` (unknown local offset), out-of-range local components/offsets and UTC instants outside years 0001–9999 after offset normalization. Numeric offsets must have hours 00–23 and minutes 00–59; UTC rollover is checked after conversion, without clamping. Cross-type UUID/numeric/BOOLEAN casts not listed above are unsupported. NUMERIC-to-TEXT preserves its declared scale; BIGINT has no leading plus/zeros; BOOLEAN uses lowercase `true`/`false`. Floating TEXT parsing/formatting must be fixed in the implementation fingerprint; native library defaults alone are not a contract.
