# Mensoria SQL design review and acceptance map

**Date:** 2026-10-29. **Scope:** MSQL-001–007, documentation only. [Language design](../../docs/surrealql-source-analysis/136-mensoria-db-sql-design.md) and [interface contract](contracts/mensoria-sql.md) are the authorities. Existing structured query code and historical receipts are reference evidence only.

## 1. Requirements and task coverage

| Requirement | Design coverage | Design task | Future implementation | Acceptance |
| --- | --- | --- | --- | --- |
| MSQL-001 compatibility | Design §§1–2, 12 | SQLD001–002 | SQLI001, SQLI008 | A01, A16 |
| MSQL-002 language/types | Design §§3–5; contract §§2–4 | SQLD002–003 | SQLI001–003 | A02–A05, A12 |
| MSQL-003 authorization | Design §§3, 5–6; contract §§1–3 | SQLD003 | SQLI002–003, SQLI006 | A06–A07, A13 |
| MSQL-004 writes/unknown | Design §7; contract §§5–6 | SQLD003 | SQLI004 | A08–A10 |
| MSQL-005 migrations | Design §8 | SQLD003 | SQLI005 | A11 |
| MSQL-006 interfaces/budgets | Design §§6, 9–10; contract §§1–6 | SQLD003 | SQLI002–003, SQLI007 | A04, A12–A15 |
| MSQL-007 delivery/evidence | Design §§11–12; this review | SQLD004 | SQLI001–008 | A01–A16 |

MSQL-SC01 maps to A01/A16; SC02 to A02–A05/A12; SC03 to A06–A11/A13–A15; SC04 to A16 and the evidence table below. Static coverage is complete; runtime success criteria remain unverified.

## 2. Future semantic, isolation and fault corpus

All cases below are **not run for SQL**. Expected behavior is a requirement, not an observed result. Enable only profiles whose cases and prerequisites have actual evidence.

| ID | Scenario and fixed input | Required result / rejection |
| --- | --- | --- |
| SQL-A01 | Comments, quoted names, multistatement text, nested denied node, unknown parser variant, SELECT with effectful function | Exact allowed AST or rejection before any backend execution; no native-text fallback |
| SQL-A02 | Logical rows with optional x absent, explicit NULL and x=1; protected x in separate restricted-role fixture | `IS NULL` selects first two authorized rows; `x = NULL` selects none; protected reference is denied rather than NULL |
| SQL-A03 | TRUE/FALSE/UNKNOWN expressions; `2 NOT IN (1,NULL)`; empty IN; explicit CAST | SQL truth table; UNKNOWN not selected; empty IN rejected; unsupported cast rejected |
| SQL-A04 | int64 max, overflow, exact decimal beyond binary64 precision, timestamp offsets, repeated output labels | Exact enabled codecs/ordinals or explicit type/range error; disabled types rejected |
| SQL-A05 | R2 duplicate tuples, NULL join keys, LEFT JOIN unmatched row, COUNT of empty input, NULL grouping | Correct bag/NULL/grouping semantics; no post-aggregate authorization filtering |
| SQL-A06 | Hidden field in WHERE/ORDER/JOIN/HAVING/RETURNING; hidden table and unknown table; catalog and EXPLAIN | Uniform sanitized denial where referenced; no metadata/plan/value leakage |
| SQL-A07 | Each side of a join contains invisible rows; COUNT/MAX over mixed visible/hidden data | Only native-authorized rows enter operators; no privileged scan; result matches visible-input reference |
| SQL-A08 | Two writes with same expected revision; guard bypass through OR; bulk UPDATE; attempts to modify revision | At most one competing commit; unmatched ordinary update yields 0; unsupported shapes rejected |
| SQL-A09 | Two-item batch, second-item failure/assertion mismatch, delayed commit reply, same-key changed body | All-or-nothing transaction; no partial RETURNING; unknown reconciles original receipt; digest conflict rejected |
| SQL-A10 | Drop reply after committed write; API/DB restart; cancel before/after commit; revoke before RETURNING publication | No duplicate mutation on original-key lookup; unknown never inferred rolled back; committed content withheld on revocation |
| SQL-A11 | DDL interrupted in backfill/index build, concurrent Schema publish, native bypass, old snapshot/new incarnation | No unverified constraint advertised; no premature binding/READY; stale artifacts invalidated; original migration reconciled |
| SQL-A12 | LIMIT 120 with page_size 50; equal/null sort keys; cursor role/schema/incarnation change; concurrent sort-key edits | At most 50/50/20; correct qualified NULL ranking; invalid cursor rejected; live-list semantics disclosed |
| SQL-A13 | Read fully computed then permission withdrawn before page/cursor publication; cached plan/result access | Final fence denies content and cursor publication; no cache authority reuse |
| SQL-A14 | Huge sort/join/aggregate with LIMIT 1; missing physical-work limiter; wait deadline while native work continues | Disable unbounded plans; no false physical cancellation; ownership and budget persist until proven completion/fence |
| SQL-A15 | Prompt-generated SQL, native arrow/UDF/file/network access, unqualified vector index, result external disclosure | Generation grants no execution; disabled extensions denied; separate model-disclosure authorization |
| SQL-A16 | Capability toggled without matching evidence; driver connects and requests catalog/transaction feature | Remains disabled; driver fails explicitly or has its own versioned passing matrix; no broad compatibility claim |

Reference evaluation uses a fixed PostgreSQL version/container digest only for the supported common SQL subset, with declared differences for lexical restrictions, byte collation, safety guards, metadata, ID type and absent-field mapping. Never use PostgreSQL as the reference for SurrealDB-specific extension behavior. Compare ordered sequences for ORDER BY and multisets otherwise, preserving duplicates, NULL tags, types and full completeness. Incomplete/approximate results cannot pass exact equivalence. No PostgreSQL installation or container was started in this task.

Suggested minimum synthetic dataset: two logical tables with at least 12 rows covering repeated business values, absent/null optional fields, empty relation, int64 boundaries, tied sort keys, visible/hidden owners and row-dependent masked fields. Record seed, schema/policies, literal fixture, backend/compiler fingerprint and expected values. This proves language boundaries only; realistic load, storage faults and customer acceptance need separately scoped datasets and runs.

## 3. Design findings resolved

| Risk | Design resolution | Remaining gate |
| --- | --- | --- |
| SQL-looking native syntax mistaken for compatibility | Named language/profile and separate driver profile | No conformance claim until actual corpus |
| Parser support mistaken for safety | Exhaustive AST allowlist, typed binder and effects | Parser pin and fuzz/unsupported-node corpus |
| Hidden fields collapsed to NULL | Deny references/masks before evaluation | Native field-policy mapping qualification |
| SQL UPDATE weakens existing CAS | Exact id/revision conjunction, typed command executor | Atomic vector and zero-match translation |
| LIMIT confused with page cap | Independent logical cap/transport cursor accounting | Native continuation and result-completeness cases |
| JOIN of independently fetched live pages | Consistent authorized input view required | R2 disabled until executor selected and proven |
| Timeout interpreted as stopped work | Wait/physical deadline/cancel outcome separate | Effective work budget and owner reconciliation |
| Constraint exists only in SQL path | Every mutation interface and native bypass evaluated | M1 cannot publish unsupported enforcement |

## 4. Evidence status

| Layer | Current result |
| --- | --- |
| Upstream research | Public PostgreSQL/SurrealDB/sqlparser documentation read; fixed links in design §12; not runtime evidence |
| Repository inspection | Active feature 004 confirmed; current native backend/SDK pin 3.3.0; current query subset lacks SQL; actual branch main |
| Independent read-only design research | Existing query.rs/data.rs and chapters 27/38 reviewed for NULL/policy/CAS/receipt/publication/pagination boundaries |
| Documentation verification | See final static verification record below |
| Local SQL parser/runtime/semantic/fault checks | NOT RUN; no SQL implementation delivered |
| CI / PostgreSQL wire or driver matrix | NOT RUN |
| Business acceptance / production / deployment | NOT RUN |

No old frozen acceptance JSON or runtime receipt is rewritten. Concurrent application and documentation changes already present in the shared checkout are preserved. No commit or push is part of this task.

## 5. Static verification record

The final record is appended after checking local Markdown references, code fences, MSQL/task/acceptance coverage, JSON examples, whitespace and scoped changes. These checks do not execute SQL or qualify any profile.


Static verification completed on 2026-10-29:

- Scoped content: 3 new authority/review files and SQL-only appended sections in 8 existing files (11 files total).
- Local Markdown references: 31 targets checked, including 3 explicit heading anchors; no missing target or anchor.
- Fenced JSON examples: 5 parsed with Python `json.loads`; code fences balanced; no unresolved placeholders or trailing whitespace in scoped content.
- Coverage: MSQL-001–007, SQLD001–004, SQLI001–008 and SQL-A01–A16 present exactly where required; all 4 documentation tasks complete, all 8 implementation tasks remain unchecked.
- `git diff --check --` over the 8 existing files changed for this increment: exit 0. New files were checked directly for whitespace because they are untracked.
- Final scoped review: only the new SQL authority/contract/review and linked append-only documentation sections were authored for this increment; no application source, dependency, migration, OpenAPI or frozen runtime receipt edited by this task.

The static verifier was an inline Python documentation check, not a SQL test harness. The mutable `sqlparser/latest` research link was observed as 0.63.0; the implementation dependency is not selected or installed. SQL runtime, CI, drivers, business acceptance and production remain NOT RUN.


## Full normative edition review (2026-10-29)

[137 full standard draft](../../docs/surrealql-source-analysis/137-mensoria-sql-standard-draft.md)
is now the authority for syntax and observable language semantics. Chapter 136
retains architecture/delivery, and the transport contract retains JSON/API
shapes. The earlier verification record above remains scoped to its original
three-file authority set; it is not relabeled as evidence for this increment.

MSQL-008/SC05 map to SQLS001–004, normative N001–N060, the 32-feature registry,
71 EBNF productions and worked cases C01–C28. Runtime implementation remains
SQLI001–008, all unchecked; SQLI001 additionally depends on SQLS004.

Independent read-only review found six concrete omissions in the initial full
draft: arithmetic NULL propagation, timestamp normalization range/-00:00,
logical index names/lookup, nullable ADD COLUMN default backfill, TEXT U+0000
policy and the transport's language-authority link. All six were corrected in
the same normative draft and linked authorities. A second read-only pass found
no additional concrete contradiction between the grammar, semantic sections
and worked cases. This is a scoped static review, not a claim of complete
language/parser correctness.

Static checks for the full edition:

- 24 main clauses and 4 appendices present; 60 unique sequential normative rule IDs, 32 unique feature IDs and 28 sequential worked-case IDs.
- 71 unique EBNF productions; all referenced nonterminals resolve. This checks symbol closure, not parser generation, ambiguity or runtime grammar acceptance.
- 17 independent fixture/value authoring checks using Python exact integers/Decimal/list operations verified the documented sorting, join multiplicity, counts, grouping, NULL examples, scale/rounding, numeric precision and 50/50/20 paging arithmetic. These do not execute SQL or qualify its semantics.
- Scoped Markdown target/anchor, code-fence, JSON-example, placeholder and whitespace checks pass; the final counts are recorded below after the final pass.
- `git diff --check --` over the 7 existing tracked files changed for this increment passed (exit 0); the three pre-existing untracked SQL files and the new standard are checked directly.

No parser/backend SQL runtime, CI, client/driver, customer, production or
performance acceptance ran. No source/dependency/migration/OpenAPI/old runtime
receipt was edited by this increment, and no commit or push was performed.

Final full-edition static pass: 11 scoped files, 30 local Markdown targets including 2 heading anchors, 5 JSON examples and 33 fenced blocks checked; no missing reference, undefined grammar symbol, duplicate identifier, placeholder or whitespace issue. SQLS001–004 complete; SQLI001–008 remain unchecked.


## Chinese edition translation verification (2026-10-29)

[The full Simplified Chinese edition](../../docs/surrealql-source-analysis/137-mensoria-sql-standard-draft.zh-CN.md)
translates draft 0.1.0-draft.1 without changing its language requirements. English
remains the source for translation reconciliation. This proportional documentation
increment adds no new feature, implementation task, dependency or runtime capability.

Verification: all 24 main clauses and 4 appendices have the same paragraph-block,
table-row, list-item and subheading counts as their English counterparts. All
60 normative IDs, 32 feature IDs and 28 case IDs match in order. All 25 fenced
SQL/EBNF blocks are byte-for-byte equivalent as decoded UTF-8 text; the 71 EBNF
productions are retained. Inline code matches in every corresponding section
after normalizing only the translated human-readable nullable type annotations.
The 11 external reference URLs match in order; all 9 local translation links
resolve. Code fences balance; no placeholder or trailing whitespace was found.
These are static translation/completeness checks, not a semantic proof or SQL run.

English source SHA-256: `19d9971bc495ae602fc909ecda25599b2fb17f222a168dac293aa7375ab35558`.
Chinese edition SHA-256: `566b1f7870b2f1da2079a08fcd6817d63aed72615464097107d773173e20d28c`.

Only the Chinese edition, English-language navigation, documentation index and
this review record are changed for this translation increment. No SQL parser,
backend, CI, driver, business or production acceptance ran; no commit/push.
