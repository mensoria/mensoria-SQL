# 15. Catalog and capability discovery

<a id="n042"></a>

**N042.** Catalog data MUST be generated from currently authorized published bindings, never from a privileged native schema dump. An invisible resource's name, ordinal, type, cardinality or physical location MUST NOT be disclosed.

The R1 minimum virtual relations are:

| Relation | Ordered columns |
| --- | --- |
| `information_schema.tables` | table_schema TEXT, table_name TEXT, table_type TEXT |
| `information_schema.columns` | table_schema TEXT, table_name TEXT, column_name TEXT, ordinal_position BIGINT, data_type TEXT, is_nullable TEXT |
| `mensoria.sql_capabilities` | feature_name TEXT, enabled BOOLEAN, profile TEXT, language_version TEXT |

Catalog columns are nonnullable. table_type is `BASE TABLE`; is_nullable is `YES` or `NO`; data_type is the canonical SQL spelling, including NUMERIC(p,s). ordinal_position is the frozen binding position, even when filtering unauthorized columns leaves gaps. Concealing all schema-shape inference is not promised; catalog access itself requires metadata permission. Native locations, secrets and system tables are absent.

Capabilities expose public feature IDs and current scope-effective availability, plus manifest metadata through the transport API. They never assert a missing business resource exists. An implementation must publish compiler/backend/profile/schema-adapter versions, feature/type/function codecs, limits/enforcement modes and evidence references. Unknown manifest versions are not silently interpreted as an older compatible one.
