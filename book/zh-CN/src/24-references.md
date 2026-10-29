# 24. 参考资料

参考资料是说明性技术输入；以上带编号的规范性规则定义 Mensoria 的选择。核对日期为 2026-10-29。未复制受专有版权保护的 ISO 标准正文，也未声称已审阅该正文。

- [PostgreSQL 18 词法结构](https://www.postgresql.org/docs/18/sql-syntax-lexical.html)：实际词法参考；Mensoria 有意收窄标识符和字面值语法。
- [PostgreSQL 18 值表达式](https://www.postgresql.org/docs/18/sql-expressions.html)：表达式存在超出语法解析的上下文规则；Mensoria 自行定义闭合子集。
- [PostgreSQL 18 比较](https://www.postgresql.org/docs/18/functions-comparison.html)：涉及 NULL 的比较背景。
- [PostgreSQL 18 SELECT](https://www.postgresql.org/docs/18/sql-select.html)：关系子句参考，不声明支持其完整语法。
- [PostgreSQL 18 聚合函数](https://www.postgresql.org/docs/18/functions-aggregate.html)：聚合类型和空输入参考；Mensoria 的十进制结果小数位数和舍入规则是明确的自身选择。
- [PostgreSQL 18 WITH 查询](https://www.postgresql.org/docs/18/queries-with.html)：CTE 背景；Mensoria 排除递归和数据修改。
- [PostgreSQL 18 错误码](https://www.postgresql.org/docs/18/errcodes-appendix.html)：五字符类别参考；Mensoria 错误码及重试行为仍是独立契约。
- [PostgreSQL 18 协议概览](https://www.postgresql.org/docs/18/protocol-overview.html)：驱动／会话协议需要单独契约。
- [SurrealDB NONE 与 NULL](https://surrealdb.com/docs/reference/query-language/language-primitives/data-types/none-and-null)：原生缺失与 null 的区别；不自动等同于 SQL。
- [SurrealDB 事务](https://surrealdb.com/docs/learn/querying/concepts-and-guides/transactions)：原生执行是实现输入，需要在固定版本上完成资格验证。
- [sqlparser-rs 文档](https://docs.rs/crate/sqlparser/latest)：候选语法解析器；语义检查仍由 Mensoria 负责。
