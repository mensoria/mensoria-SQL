# Edition, authority and provenance

| Field | Value |
| --- | --- |
| Book edition | First bilingual book edition, 2026-10-29 |
| Language document | MSQL-SD-001 |
| Document revision | 0.1.0-draft.1 |
| Language version | 1 |
| Status | Draft; runtime conformance not established |
| Maintained manuscript | `book/en/src` and `book/zh-CN/src` |

## Editorial boundary

The source's 24 clauses are now individual chapters; four appendices remain separate. Stable rule/feature/case identifiers, inline technical values and fenced SQL/EBNF are retained. Heading levels and local navigation are adapted to a book. Front matter, indexes, language switching and provenance notes are editorial additions and grant no new language capability.

Historical chapter numbers such as “136” identify the source collection's architecture material. In this edition they resolve to informative companions or the [source context](source-context.md), rather than a nonexistent book chapter.

## Imported inputs

The five original documents are frozen under `sources/archstudio/` and identified by per-file SHA-256 in `sources/manifest.json`. They came from an ArchStudio working tree; its base Git commit alone does not identify the then-uncommitted drafts. The manifest records that distinction. Historical source links inside those snapshots remain unchanged for provenance; only the maintained book pages form the standalone navigation graph.

English is the language source for translation reconciliation. The normative draft, architecture companion and transport contract have separate ownership. Changes affecting meaning must update the paired chapters, revision history and conformance evidence; publishing the book itself does not change runtime readiness.
