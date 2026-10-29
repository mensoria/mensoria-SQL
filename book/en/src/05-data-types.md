# 5. Data types and values

<a id="n013"></a>

**N013.** A scalar value MUST have one declared logical type or be SQL NULL of a known contextual type. Backend values MUST pass the declared codec; lossy coercion or exposure as a raw native value is prohibited.

| Type spelling | Domain | Comparison / grouping |
| --- | --- | --- |
| `BOOLEAN` | TRUE, FALSE | Equality; ordering FALSE before TRUE; nullable UNKNOWN is SQL NULL |
| `BIGINT` | Signed 64-bit integer | Exact equality/order/group |
| `TEXT` | Valid Unicode scalar sequence excluding U+0000, including empty string | Exact code-point content equality; UTF-8 byte lexicographic order; no normalization or locale |
| `UUID` | 128-bit UUID; optional type feature | Equality, IN, DISTINCT, GROUP BY; ordering/MIN/MAX prohibited in v1 |
| `NUMERIC(p,s)` | Decimal, 1 <= p <= 38, 0 <= s <= p | Exact equality/order/group after safe common-type resolution |
| `DOUBLE PRECISION` | Finite IEEE binary64; optional type feature | Numeric equality/order; -0 and +0 compare/group equal; NaN/infinity prohibited |
| `TIMESTAMP WITH TIME ZONE` | UTC instant, microsecond precision, years 0001–9999 | Instant equality/order/group; no session timezone |

The type-name grammar deliberately excludes INT/INTEGER/VARCHAR/DECIMAL aliases in this draft; encountering them is unsupported syntax, not an implied alias. `NUMERIC` without precision and scale is also unsupported. These choices can be reconsidered in a later versioned revision.

NUMERIC values are exact multiples of 10^-s with magnitude less than 10^(p-s). Decimal literal type uses total written digits and fractional digits, excluding sign and leading integral zeros, with minimum precision sufficient for its scale and at least 1. A leading zero before a decimal point is required. Trailing fractional zeros contribute to the inferred scale. Parameter types explicitly declare p/s.

TEXT never trims trailing spaces and has no CHAR padding. U+0000 is prohibited in TEXT literals, typed parameters and results; reject invalid parameters as SQL_INVALID_TEXT_VALUE and invalid stored/returned values as SQL_TYPE_ERROR, never strip the character. TEXT may contain non-NUL control characters as data inside valid string/parameter encodings; logs/results remain protected. Native record IDs, geometry, duration, arrays and arbitrary objects are not members of these domains.

<a id="n014"></a>

**N014.** Authorized absent optional business fields and explicit stored nulls MUST both map to SQL NULL in the relational view. An absent required column MUST fail with `SQL_TYPE_ERROR`; an unreadable field MUST follow §20, never become an ordinary NULL.

<a id="n015"></a>

**N015.** JSON is not a core v1 type. A future registered JSON extension MUST preserve SQL NULL versus JSON value null and specify missing-path behavior separately. A transport tag reserved for JSON does not make that extension executable.
