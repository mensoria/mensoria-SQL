# 21. Multimodel extension framework

<a id="n055"></a>

**N055.** A language extension MUST register a stable `mensoria` namespace, exact syntax/signatures, parameter/result codecs, NULL behavior, determinism/effects, scope/lineage, limits, index readiness, evidence and versioning before its parser/executor can accept it. Core expressions MUST NOT silently pass through native SurrealQL fragments.

This draft specifies no executable JSON/graph/fulltext/vector function. Their names in discovery are capability reservations only. A future extension specification must define at least:

| Extension | Required additional contract |
| --- | --- |
| JSON | SQL NULL vs JSON null, missing path, extraction/casts, object/array equality, duplicate keys and nesting limits |
| Graph | Edge relation binding, allowed direction/labels, per-hop policies, cycles, depth/edge/vertex limits, result lineage |
| Full-text | Analyzer/language/index revision, match/scoring semantics, authorization prefilter, readiness and deterministic limits |
| Vector | Dimension/metric/value codec, exact vs ANN mode, candidate/output budgets, filter semantics, index generation and recall evaluation |

Existing approved edge collections may be queried as ordinary R2 relations when their bindings qualify; that does not enable graph traversal syntax. Arrow paths, native function calls, live subscriptions and provider-specific vector operators remain rejected.

<a id="n056"></a>

**N056.** External model calls, embeddings, HTTP/file access, object uploads and job scheduling MUST NOT occur as hidden SQL transaction effects. They remain separate authorized platform commands, with their own external-unknown reconciliation. ANN results must never be advertised as exact relational equivalence.
