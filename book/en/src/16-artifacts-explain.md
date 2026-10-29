# 16. Validation, artifacts and EXPLAIN

<a id="n043"></a>

**N043.** Validation MUST parse, exhaustively inspect AST nodes, resolve authorized metadata, bind types/nullability/effects, enforce feature/size/budget planning gates and record immutable dependency revisions. No execution or external side effect is authorized by a validation result.

Artifacts bind source/canonical plan digests, declared parameter types, scope/incarnation, actor authorization obligations, schema/mapping/security versions, compiler/profile fingerprint and expiry. SQL literals and source are protected artifact content. Metadata-only previews cannot borrow ordinary business-read permissions or management credentials.

<a id="n044"></a>

**N044.** Execution MUST load the exact artifact revision and recheck current authorization and compatibility before backend access and again before publication. Edits and incompatible schema/policy/compiler/incarnation changes require new validation; an existing artifact MUST NOT be silently recompiled or promoted.

EXPLAIN is an authorized nonexecuting logical-plan operation, accepted through the transport route or `EXPLAIN <select>` syntax when `plan.explain` is enabled. It returns logical resource references, typed operators, required features and effective proposed limits. It must not execute business scans, expose native text/locations/hidden cardinalities or run ANALYZE. Parameter sampling and optimizer suggestions cannot publish schema changes.
