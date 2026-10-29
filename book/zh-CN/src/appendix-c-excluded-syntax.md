# 附录 C. 明确排除的语法

此列表是规范性拒绝范围，不构成未来实现这些能力的承诺。

| 类别 | 本草案排除项 |
| --- | --- |
| 词法便利语法 | Unicode／含空格标识符、美元引用字符串、转义字符串前缀、指数 SQL 字面值、类型名称别名 |
| 查询形状 | 无 FROM 的 SELECT、OFFSET、标量／关联／IN 子查询、派生表语法、SELECT INTO、TABLE 简写 |
| 连接 | CROSS/NATURAL/RIGHT/FULL/LATERAL、USING、逗号连接、非等值连接、单个查询块超过两个关系引用 |
| 分组／窗口 | GROUP BY 表达式／序号、grouping sets/rollup/cube、聚合 DISTINCT/FILTER/ORDER BY、窗口函数 |
| 集合表达式 | UNION DISTINCT、INTERSECT、EXCEPT、分支各自的上限／排序 |
| 谓词／函数 | BETWEEN、LIKE、正则、IS DISTINCT FROM、IS TRUE/FALSE/UNKNOWN、一般 UDF 调用、易变函数 |
| DML | 一般集合 UPDATE/DELETE、盲覆盖／upsert、INSERT SELECT、MERGE、生成键、表达式赋值、RETURNING * |
| 事务 | SQL BEGIN/COMMIT/ROLLBACK、保存点、客户端保持的开放事务、SET TRANSACTION、分布式事务 |
| DDL／安全 | 创建 Schema／角色／用户／数据库、GRANT/REVOKE、过程／触发器、ALTER TYPE/RENAME/DROP COLUMN、TRUNCATE、任意原生 Schema |
| 约束 | 一般 UNIQUE/FOREIGN KEY/CHECK、级联或延迟约束、未经资格验证的原生索引强制约束 |
| 原生／外部 | USE、命名空间切换、原生记录 ID／箭头遍历、原生函数命名空间、文件／网络访问、COPY／导入／导出、实时查询语法 |
| 扩展 | 在独立扩展规范完成登记并具有证据前，所有可执行 JSON／图／全文／向量语法 |
| 驱动声明 | 完整 pg_catalog/INFORMATION_SCHEMA、PostgreSQL 会话／portal／OID、通用 ORM／BI 兼容性 |

对于已识别但被排除的 AST，可以返回 SQL_FEATURE_UNSUPPORTED；对于语法范围外的文本，可以返回 SQL_SYNTAX_ERROR。两者都必须在后端执行之前拒绝。错误分类不得暴露受保护资源是否存在。
