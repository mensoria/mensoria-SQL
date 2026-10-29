# 1. Purpose, authority and normative terminology

## 1.1 Scope

Mensoria SQL is a standard-oriented, versioned query and mutation language for authorized logical relations in one Mensoria DB project environment. It uses familiar SQL notation and selected PostgreSQL conveniences while retaining Mensoria's current identity, schema, command and operation ownership.

This document specifies observable behavior. It does not replace the SurrealDB storage engine, create a new authorization service, or prescribe a second database. A parser, native database or client accepting similar text is not evidence of conformance.

<a id="n001"></a>

**N001.** In this document, MUST/SHALL express a requirement; MUST NOT/SHALL NOT express a prohibition; SHOULD expresses a recommendation requiring a documented reason for deviation; MAY expresses an option. An implementation claiming a profile MUST satisfy every applicable MUST requirement and publish its enabled optional features.

<a id="n002"></a>

**N002.** This draft is the language authority. [Chapter 136](companion-architecture.md) owns architecture and staged delivery; the [interface contract](companion-transport.md) owns concrete request/result encodings. A conflict MUST be corrected before enabling the affected feature; implementations MUST NOT silently choose whichever interpretation is easier.

<a id="n003"></a>

**N003.** No implementation may claim complete ISO SQL, complete PostgreSQL, JDBC/ODBC, ORM, BI-tool or PostgreSQL wire compatibility from this draft. Such claims require separately named versions, supported features and actual evidence.

## 1.2 Terms

| Term | Meaning |
| --- | --- |
| Scope | Authenticated organization/project/environment binding |
| Incarnation | Recovery generation distinguishing a current physical environment from an old one |
| Logical relation | Published SQL table or scoped query result, distinct from a physical native table |
| Binding | Versioned mapping from logical SQL names/types to published collection/schema metadata |
| Artifact | Immutable validated SQL/typed-plan revision with declared dependencies |
| Operation | Existing durable authority for accepted execution and its original-key outcome |
| Publication | Final authorized release of result bytes, metadata or a continuation capability |
| Unknown | Insufficient evidence to confirm commit, failure or physical completion |
| Complete result | All rows required by the SQL expression and its explicit logical cap have been delivered |
| Qualified feature | A feature with a frozen implementation profile and passing required evidence |

Examples are informative unless a rule or Appendix B explicitly gives an expected result. A “deferred” feature has no executable contract in v1; an “optional specified” feature has rules here but requires a separate enabled capability.
