# 18. Diagnostics

<a id="n049"></a>

**N049.** Errors MUST contain a stable Mensoria code, five-character SQLSTATE-style category, sanitized message, phase, retry hint and original operation reference when already accepted and currently observable. Source span is optional when safely attributable. They MUST NOT include protected native text, resource existence details, values, credentials or backend stack traces.

| Code | Category | Trigger |
| --- | --- | --- |
| SQL_SYNTAX_ERROR | 42601 | Invalid token/grammar or extra statement |
| SQL_FEATURE_UNSUPPORTED | 0A000 | Specified optional feature disabled, deferred syntax or unsupported node |
| SQL_REFERENCE_DENIED | 42501 | Unknown/unauthorized public reference |
| SQL_TYPE_ERROR | 42804 | Incompatible types, invalid codec/source mapping or unresolved type |
| SQL_VALUE_OUT_OF_RANGE | 22003 | Overflow, unsupported precision loss or nonfinite number |
| SQL_INVALID_TEXT_VALUE | 22018 | Text cannot be parsed as the declared scalar type |
| SQL_DIVISION_BY_ZERO | 22012 | Evaluated numeric division by zero |
| SQL_AMBIGUOUS_REFERENCE | 42702 | Multiple authorized matches for a permitted name |
| SQL_INVALID_GROUPING | 42803 | Illegal aggregate location or ungrouped column |
| SQL_ARTIFACT_STALE | 55000 | Incompatible execution dependency revision |
| SQL_WRITE_PRECONDITION_REQUIRED | 0A000 | W1 mandatory guard shape absent or unsafe |
| SQL_PRECONDITION_FAILED | 40001 | Explicit affected-row assertion fails |
| SQL_CONSTRAINT_CONFLICT | 23000 | Sanitized integrity violation |
| SQL_KEY_CONFLICT | 23000 | Existing original key bound to different request identity |
| SQL_BUDGET_EXCEEDED | 54000 | Proven resource bound exceeded or plan lacks required enforceable budget |
| SQL_CURSOR_INVALID | 24000 | Cursor expiry/binding/version mismatch |
| SQL_RESULT_EXPIRED | 55000 | Original protected result no longer retained |
| SQL_OUTCOME_UNKNOWN | 08007 | Accepted operation/commit not confirmed |
| SQL_DEPENDENCY_UNAVAILABLE | 08006 | Required dependency inaccessible |
| SQL_CANCEL_PENDING | 57014 | Cancellation requested, physical/commit outcome unconfirmed |

These categories do not promise PostgreSQL driver behavior. In particular 40001 never authorizes blind fresh-key retry, and 57014 never proves rollback. Clients must use the Mensoria code, phase, retry_hint and operation reference together.

Retry hints are `edit`, `revalidate`, `restart_read`, `reconcile_original`, `observe_original`, `none`. Uncertainty after admission takes precedence over a superficial transport/precondition error that would imply no work occurred. Authorization failures may suppress operation visibility without changing its durable outcome.
