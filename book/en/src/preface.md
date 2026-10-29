# Mensoria SQL

The SQL language specification and implementation reference for Mensoria DB.

<p class="document-meta"><span>Language version 1</span><span>Draft 0.1.0-draft.1</span><span>MSQL-SD-001</span></p>

[Read the standard](01-purpose.md) [Reading guide](reading-guide.md)

## The specification

| Chapters | Content |
| --- | --- |
| [Language foundations](01-purpose.md) | Profiles, logical model, lexical rules, types and expressions. |
| [Relational queries](08-select.md) | SELECT, ordering, joins, aggregates and optional query constructs. |
| [Mutation and schema](12-data-modification.md) | Guarded writes, atomic request transactions and migration proposals. |
| [Execution contract](15-catalog.md) | Catalogs, artifacts, results, diagnostics, budgets and authorization. |
| [Compatibility and conformance](21-extensions.md) | Extension boundaries, versioning and implementation evidence. |

## Reference indexes

[Complete grammar](appendix-a-grammar.md) · [Statements](statement-index.md) · [Error codes](18-diagnostics.md) · [Normative rules](rules-index.md)

This edition contains 24 normative chapters, four appendices and 28 worked cases. It is a proposed language standard; runtime and driver conformance have not been established. See the [profile definitions](02-profiles.md) for capability boundaries.
