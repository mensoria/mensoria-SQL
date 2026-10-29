# 12. Data modification

## 12.1 Common W1 rules

<a id="n031"></a>

**N031.** W1 MUST compile into existing scoped typed commands and one native transaction with the original Operation/Outbox/guard obligations. Executing user text directly under a system identity, or sequentially calling independently committing commands, is prohibited.

Targets are published `public` tables, with their exact expected Schema/mapping revision in the validated artifact. W1 supports no target aliases, joins, FROM/USING clauses, subqueries, effects, triggers supplied by the user, generated values or expression assignments. Values are literals, typed parameters or CAST of a value, with no business-column reference.

INSERT must name its columns explicitly, including exactly one `id`. UPDATE assignments must name each business column at most once. Platform revision/timestamps/owner/ACL fields cannot be assigned. Schema write authorization and NOT NULL/type/default rules apply to every assignment and to omitted fields.

## 12.2 INSERT

Base W1 accepts one `VALUES (...)` tuple, with the same arity as the explicit nonduplicate column list. Logical id is non-NULL TEXT. The row is create-if-absent; existing IDs cannot be overwritten. Omitted optional business columns become SQL NULL unless a qualified literal default exists; omitted required columns without a default fail. An explicit NULL does not invoke a default.

<a id="n032"></a>

**N032.** INSERT MUST commit a row at revision 1 and return affected_rows=1 when successful. A uniqueness/id conflict MUST return one sanitized integrity error without the existing row's data or constraint details. Conditional conflict errors do not establish that a protected row is readable; the service cannot promise perfect information-theoretic concealment of attacker-chosen unique-key occupancy.

`write.multi_values` optionally accepts multiple literal/parameter tuples. Total mutations per request remain <=16, including all statements. Duplicate target IDs within a statement/batch are rejected before mutation; no partial multi-row INSERT is permitted. INSERT SELECT, DEFAULT VALUES, RETURNING *, ON CONFLICT/UPSERT and generated identity are deferred.

## 12.3 UPDATE and DELETE

<a id="n033"></a>

**N033.** UPDATE/DELETE MUST have a WHERE predicate that is a conjunction of atomic comparisons/NULL tests with mandatory exact `id = value` and `revision = value` terms. There MUST be exactly one guard for each, with id/revision on the left, non-NULL typed scalar values on the right, id TEXT and revision positive BIGINT. OR, NOT, IN, functions or column-to-column guards are prohibited in W1 predicates.

Parentheses may group the conjunction but cannot make either guard optional. Additional conditions may read authorized business columns; extra references to id/revision other than their mandatory guards are rejected in v1. An UPDATE assignment cannot refer to old row data; users read a revision and prepare a new desired value explicitly.

An authorized UPDATE increments the current revision by 1 and updates mapped timestamps where supported, even if business values are unchanged. DELETE removes/tombstones the current row through the existing deletion command; RETURNING refers to the authorized predelete row.

<a id="n034"></a>

**N034.** An ordinary no-match UPDATE/DELETE MUST produce affected_rows=0 and an empty RETURNING row set, uniformly for absent, invisible, revision-mismatched or additional-condition-mismatched targets. Translation of an existing CAS failure to zero match MUST require proof that no mutation committed. A schema/session/guard failure is not a zero match.

## 12.4 RETURNING

RETURNING accepts an explicit nonempty list of authorized simple columns, optionally AS aliases. INSERT/UPDATE return postmutation values including the new revision; DELETE returns predelete values. All results remain protected by final publication checks. Omitted RETURNING still returns an affected-row count, with no invented business result columns.

<a id="n035"></a>

**N035.** A committed write whose RETURNING content cannot currently be published MUST retain its committed operation outcome. The service MUST withhold the content and MUST NOT report rollback or automatically resend the mutation under a new key.
