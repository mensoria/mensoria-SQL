# 22. Compatibility, versioning and implementation requirements

<a id="n057"></a>

**N057.** Every accepted artifact MUST bind language version, draft/semantic revision, compiler fingerprint, enabled feature set and schema adapter/backend profile. A semantic change to NULL, numeric conversion, ordering, guard or privilege behavior requires a new compatible version decision and revalidation of affected artifacts.

Adding optional features must not reinterpret previously accepted syntax. Security withdrawal may disable a capability immediately, invalidating cached plans/artifacts/cursors as necessary. There is no guarantee that stale artifacts survive an upgrade. A server must not reinterpret an unknown language or manifest version as version 1.

Parser versions and upstream backend behavior are implementation inputs, not language authorities. A mature parser may be used, but its AST must be exhaustively classified into a closed typed IR; unknown nodes default to denied. SurrealDB SDK/server 3.3.0 is the current repository's pinned reference runtime, not a statement that it already implements this SQL draft.

<a id="n058"></a>

**N058.** SQL compatibility, native SurrealQL compatibility, PostgreSQL wire compatibility and named client compatibility MUST be reported separately. A P1 document must specify protocol version, authentication/TLS, sessions, Parse/Bind/Execute/Sync/portal behavior, type codecs/OIDs, metadata views, errors, cancel and transaction semantics. This draft grants none of those capabilities.

R1/W1/M1 restrictions such as mandatory CAS, no interactive transactions and a limited catalog are observable compatibility differences. An ORM requiring missing functionality must fail clearly or use an explicitly tested adapter; the service must not pretend a discarded statement succeeded.
