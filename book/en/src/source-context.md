# Historical source context

This book is standalone. The following source-collection references explain provenance and ownership; they are not missing dependencies that a reader must fetch to understand the normative language. Their original repository paths are retained as identifiers, not as broken local links.

<a id="feature-requirements"></a>

## Feature requirements

The original feature was `specs/004-surrealdb-rust-ai-baas`. MSQL-001–008 describe language profiles, types, authorization, guarded writes, migrations, interfaces, evidence and the full standard. SQLD/SQLS were documentation tasks; SQLI001–008 remained future implementation. This publication does not reclassify their state. The normative requirements reproduced here are N001–N060.

<a id="data-model-and-write-ownership"></a>

## Data model and write ownership

Source chapter 27 defined logical collections/Schema revisions, record CAS, current identity checks, guarded native transactions and business/Operation/Outbox ownership. This book's [DML](12-data-modification.md) and [transactions](13-transactions.md) make the SQL obligations explicit; SQL cannot introduce a privileged bypass.

<a id="structured-query-baseline"></a>

## Structured-query baseline

Source chapter 38 described an earlier JSON query subset and live keyset cursors. Those historical checks do not qualify SQL NULL/OR/joins/aggregates, physical-work budgets or SQL conformance. The [SQL pagination contract](17-parameters-results-pagination.md) is the language requirement.

<a id="assistant-query-boundary"></a>

## Assistant/query boundary

Source chapter 19 separated generation, validation, execution and optimization under a trusted query executor. Model-generated source does not grant execution/disclosure authority; this book retains that boundary in [artifacts](16-artifacts-explain.md) and [authorization](20-authorization-audit.md).

<a id="studio-boundary"></a>

## Studio boundary

Source chapter 133 described the browser/API bridge and its identity/session/ticket obligations. A platform Member role does not imply business-data privileges. SQL uses the same current native authorization and final publication fence.

## Engineering references

The [architecture companion](companion-architecture.md), [transport contract](companion-transport.md) and [qualification scenarios](acceptance-scenarios.md) are retained as informative implementation references. The historical full review snapshot is in the repository's source archive; its old local receipts are not runtime evidence for this book.
