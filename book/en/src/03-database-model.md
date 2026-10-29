# 3. Database model, names and binding

<a id="n007"></a>

**N007.** One execution MUST bind to one server-derived scope and incarnation. SQL MUST NOT override the physical target, switch namespaces/databases, or join across project environments.

The default schema is `public`. A user table reference is either `table_name` or `public.table_name`. Only the three virtual catalog relations in §15 use other schemas. Three-part names, `search_path`, temporary schemas and native record-target notation are prohibited.

<a id="n008"></a>

**N008.** A logical table MUST map to a published collection binding containing its logical identity, SchemaRevision, mapping revision, ordered columns, types, nullability, source mappings and policy obligations. An arbitrary native/schemaless table MUST NOT automatically appear as a SQL table.

Platform SQL columns are `id TEXT NOT NULL`, `revision BIGINT NOT NULL`, and qualified `created_at`/`updated_at` timestamp columns when actually mapped and enabled. Timestamp columns are not implied for historical collections without suitable data. `id` is immutable. `revision` is server-owned, initially 1 for a new SQL-created row, and increments by 1 for each committed UPDATE, including a value-preserving update. Revision overflow fails the transaction.

<a id="n009"></a>

**N009.** New SQL bindings MUST reserve `id`, `revision`, `created_at` and `updated_at` against business-column collisions. Existing conflicting fields MUST use an explicit reviewed SQL alias; binding MUST NOT rename stored data implicitly.

<a id="n010"></a>

**N010.** Name resolution MUST use authorized catalog metadata. Missing and unauthorized public resource references MUST yield the same sanitized `SQL_REFERENCE_DENIED`; no hidden physical table, name, row count or native error may be returned.

A table alias hides its original qualifier inside that query block. A column reference is unqualified or qualified by the active table/CTE alias. Ambiguous references are rejected. Output aliases are visible only to ORDER BY, never WHERE/ON/GROUP BY/HAVING or another item in the same SELECT list. An alias matching both an output label and input column in ORDER BY resolves to the unique output label; duplicate matching output labels are ambiguous.
