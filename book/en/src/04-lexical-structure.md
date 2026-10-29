# 4. Lexical structure

## 4.1 Source encoding and identifiers

<a id="n011"></a>

**N011.** SQL source MUST be valid UTF-8, without U+0000 or a byte-order mark. Whitespace outside strings/comments is ASCII space, tab, CR or LF; CRLF counts as one line break for diagnostics. All other unexpected control characters are rejected.

Unquoted identifiers use `[A-Za-z_][A-Za-z0-9_]*` and fold to lowercase. Quoted identifiers use double quotes and preserve case, but their decoded content must match the same ASCII pattern in v1. Thus `notes`, `NOTES` and `"notes"` resolve identically, while `"Notes"` is distinct. A decoded quote, whitespace or Unicode name is not a valid v1 identifier; a reviewed alias is required. Identifier length is at most 63 UTF-8 bytes, with no silent truncation.

All word terminals shown in uppercase in Appendix A are reserved, matched case-insensitively outside quoted identifiers. Quoting allows an otherwise reserved word if its decoded form obeys the identifier restriction. `PUBLIC`, `INFORMATION_SCHEMA` and `MENSORIA` remain ordinary schema identifiers rather than extra SQL keywords.

## 4.2 Literals and comments

| Token | Syntax and meaning |
| --- | --- |
| String | Single-quoted Unicode text; `''` encodes one apostrophe; backslash is an ordinary character |
| Integer | One or more ASCII digits, optional sign consumed by scalar grammar; BIGINT range checked after sign |
| Decimal | Digits, period, digits; optional sign consumed by scalar grammar; requires `type.numeric`; at most 38 precision/scale |
| Boolean | `TRUE` or `FALSE` |
| SQL NULL | `NULL`, with a type inferred from context or explicit CAST |
| Parameter | `$` followed by positive decimal position, no leading zero; e.g. `$1` |
| Comments | `--` through line end; nonnested `/* ... */`; unterminated/nested block comments rejected |

`-9223372036854775808` is a valid BIGINT literal even though its unsigned magnitude exceeds the positive BIGINT maximum. Exponents, hexadecimal/binary literals, dollar quoting, backslash-escape string prefixes, bit strings and locale-dependent numbers are deferred. UUID/timestamp/double values use typed parameters or explicit CAST from TEXT, not special literal token classes.

<a id="n012"></a>

**N012.** Normal execution MUST accept exactly one parsed statement plus at most one trailing semicolon. It MUST reject empty input, extra statements/tokens and unclosed lexical constructs. Batch input MUST be an array of independently parsed statements; semicolon splitting is prohibited. SQL text inside a comment or string is never a statement.

Source spans use one-based Unicode-code-point line/column positions, with an exclusive end position. A semantically equivalent normalized source may share a plan cache entry, but literal/parameter values remain part of execution identity.
