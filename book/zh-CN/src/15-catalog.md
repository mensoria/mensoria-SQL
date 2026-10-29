# 15. 目录与能力发现

<a id="n042"></a>

**N042.** 目录数据必须从当前已授权、已发布的绑定生成，绝不能取自特权原生 Schema 导出。不得披露不可见资源的名称、序号、类型、基数或物理位置。

R1 最低要求的虚拟关系为：

| 关系 | 有序列 |
| --- | --- |
| `information_schema.tables` | table_schema TEXT, table_name TEXT, table_type TEXT |
| `information_schema.columns` | table_schema TEXT, table_name TEXT, column_name TEXT, ordinal_position BIGINT, data_type TEXT, is_nullable TEXT |
| `mensoria.sql_capabilities` | feature_name TEXT, enabled BOOLEAN, profile TEXT, language_version TEXT |

目录列不可空。table_type 为 `BASE TABLE`；is_nullable 为 `YES` 或 `NO`；data_type 是规范 SQL 写法，包括 NUMERIC(p,s)。ordinal_position 是冻结的绑定位置，即便过滤未授权列后留下空号也不改变。这里不承诺隐藏全部 Schema 形状推断；访问目录本身要求元数据权限。目录中不包含原生位置、秘密或系统表。

能力发现通过传输 API 暴露公共能力 ID、在当前作用域下的有效可用性及清单元数据，不得借此断言不存在的业务资源存在。实现必须公布编译器／后端／档位／Schema 适配器版本、能力／类型／函数编解码器、限制／执行模式和证据引用。不得把未知清单版本静默解释为某个更旧的兼容版本。
