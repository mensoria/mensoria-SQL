# Glossary

This lookup aid is informative; normative definitions remain in [Chapter 1](01-purpose.md).

| Term | Meaning in this book | Primary reference |
| --- | --- | --- |
| Artifact | Immutable validated source/typed-plan revision; validation grants no execution permission | [16](16-artifacts-explain.md) |
| Binding | Published logical-to-native schema mapping | [3](03-database-model.md) |
| CAS | Compare-and-set using an expected revision | [12](12-data-modification.md) |
| Complete result | Entire requested logical result including its explicit cap | [17](17-parameters-results-pagination.md) |
| Guard | Existing native authorization/admission conflict boundary touched by execution | [13](13-transactions.md) |
| Incarnation | Recovery generation; old targets/artifacts cannot silently become current | [3](03-database-model.md) |
| IR | Closed typed intermediate representation, independent of the upstream AST | [22](22-compatibility.md) |
| Keyset | Continuation using an ordered last-key state; ordinary pages are live, not snapshots | [17](17-parameters-results-pagination.md) |
| Operation | Existing durable execution/outcome authority bound to the original key | [13](13-transactions.md) |
| Outbox | Transactionally committed event intent alongside the business change and receipt | [13](13-transactions.md) |
| Profile | Minimum conformance feature set, such as R1 or W1 | [2](02-profiles.md) |
| Publication | Final authorized release of result content or continuation | [20](20-authorization-audit.md) |
| Qualified | Frozen implementation configuration with required passing evidence | [23](23-conformance.md) |
| UNKNOWN | NULL truth interpretation in expressions; distinct from an unknown execution outcome | [7](07-expressions.md), [13](13-transactions.md) |
