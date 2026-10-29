# Reading guide

This reference has five parts. Read it linearly for the full contract, or follow one of these routes.

| Reader | Suggested route | Question answered |
| --- | --- | --- |
| Application developer | [Profiles](02-profiles.md) → [SELECT](08-select.md) → [Parameters/results](17-parameters-results-pagination.md) → [DML](12-data-modification.md) | What can my application submit and rely on? |
| Language implementer | [Lexical rules](04-lexical-structure.md) → [Types](05-data-types.md) → [Expressions](07-expressions.md) → [Grammar](appendix-a-grammar.md) | What exactly is accepted, typed and evaluated? |
| Data/authorization reviewer | [Binding](03-database-model.md) → [JOIN](09-joins.md) → [Transactions](13-transactions.md) → [Authorization](20-authorization-audit.md) | Which identity owns work and when may data be published? |
| Schema operator | [Schema proposals](14-schema-migrations.md) → [Budgets](19-budgets-cancellation.md) → [Conformance](23-conformance.md) | What must be verified before publication or reopening? |
| Conformance engineer | [Worked corpus](appendix-b-conformance-corpus.md) → [Qualification scenarios](acceptance-scenarios.md) → [Excluded syntax](appendix-c-excluded-syntax.md) | Which positive, negative and fault boundaries need evidence? |

## How to read a requirement

`N001`–`N060` are stable normative rule IDs. `C01`–`C28` are worked language cases. `SQL-A01`–`SQL-A16` are future semantic/security/fault qualification scenarios. A passing documentation check is not a passing runtime case.

MUST/SHALL and MUST NOT/SHALL NOT are requirements/prohibitions. SHOULD is a recommendation requiring a documented reason for deviation; MAY is optional. A grammar production does not authorize an optional feature, and an example is not a runtime receipt.

## Five parts

1. **Language foundations** — scope, profiles, logical names, tokens, types and expressions.
2. **Relational queries** — projection, ordering, joins, aggregates and optional constructs.
3. **Mutation and schema** — guarded commands, atomic request batches, unknown outcomes and migrations.
4. **Execution contract** — metadata, artifacts, transport values, diagnostics, budgets and authorization.
5. **Evolution and evidence** — extensions, compatibility, qualification and sources.

The grammar and exact examples follow the normative chapters. Rule, feature, statement and glossary indexes support lookup; the informative companions explain implementation ownership and transport without creating another language authority.
