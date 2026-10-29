# 20. Authorization, lineage and auditing

<a id="n052"></a>

**N052.** SQL MUST reuse native row/field authorization, scoped Control admission and current session/family checks. It MUST NOT replace them with a privileged scan and later filter, cached grants, a caller-selected role or an issuer identity with business-data access.

A reference to a protected field is denied in projection, predicate, ordering, join, grouping, aggregate input, CASE branch and RETURNING. Row-dependent field masks that cannot be proven readable for the entire bound input make that SQL column unusable for that artifact. Star expands only provably readable columns. An unexpected masked value invalidates the pending result rather than being treated as absent data.

<a id="n053"></a>

**N053.** All reads of plans, history, metadata, cached results, artifacts, cursors and original-operation results MUST reauthorize currently protected content. A plan cache key is not a permission grant. Revocation before final publication MUST suppress the pending content and continuation even when backend computation finished.

Aggregates may intentionally reveal statistics about authorized rows; this language provides access control, not differential privacy. Threats from unique-key conflicts, authorized counts and catalog shape must be documented without falsely claiming universal non-inference. Native error sanitization remains mandatory.

<a id="n054"></a>

**N054.** Audit MUST correlate actor/scope, artifact/compiler/profile/schema versions, redacted query shape and typed-value digests, original operation, security/incarnation watermarks, consumed budgets, outcome and publication state. Ordinary logs MUST omit raw SQL literals, parameters, result rows and credentials; query/actor labels must not create unbounded metric cardinality.

Audit retention and support access follow existing platform controls. Model-generated SQL is untrusted source. Disclosing SQL text, schema samples or result data to an external model requires separate current disclosure authorization and must not happen implicitly during execution.
