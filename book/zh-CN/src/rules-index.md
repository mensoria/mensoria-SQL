# 规范规则索引

本索引用于查阅，所链接章节的规则全文为准。

| 规则 | 要求开头 |
| --- | --- |
| [N001](01-purpose.md#n001) | 本文件中的 MUST/SHALL 译为“必须”，表示强制要求；MUST NOT/SHALL NOT 译为“不得”，表示禁止；SHOULD 译为“应当”，表示偏离时需要记录理由的建议；MAY 译为“可以”，表示可选。 |
| [N002](01-purpose.md#n002) | 本草案是语言规范的权威。 |
| [N003](01-purpose.md#n003) | 任何实现均不得仅依据本草案声明完整 ISO SQL、完整 PostgreSQL、JDBC/ODBC、ORM、BI 工具或 PostgreSQL 线协议兼容。 |
| [N004](02-profiles.md#n004) | 档位启用必须限定作用域、实施版本管理并具有证据支持。 |
| [N005](02-profiles.md#n005) | 需要多项能力的语句必须满足这些能力的并集，包括类型和运算符依赖。 |
| [N006](02-profiles.md#n006) | 在完整档位通过资格验证之前，实现可以开放单独命名的预览能力，但不得宣称该档位已启用。 |
| [N007](03-database-model.md#n007) | 一次执行必须绑定到一个由服务端确定的作用域和环境代次。 |
| [N008](03-database-model.md#n008) | 逻辑表必须映射到已发布的集合绑定，其中包含逻辑身份、SchemaRevision、映射修订号、有序列、类型、可空性、来源映射及策略约束。 |
| [N009](03-database-model.md#n009) | 新 SQL 绑定必须保留 `id`、`revision`、`created_at` 和 `updated_at`，防止与业务列重名。 |
| [N010](03-database-model.md#n010) | 名称解析必须使用已授权的目录元数据。 |
| [N011](04-lexical-structure.md#n011) | SQL 源文本必须是有效 UTF-8，且不得包含 U+0000 或字节顺序标记。 |
| [N012](04-lexical-structure.md#n012) | 普通执行必须接受恰好一条经解析的语句，并允许末尾最多一个分号。 |
| [N013](05-data-types.md#n013) | 标量值必须具有一个声明的逻辑类型，或为上下文类型已知的 SQL NULL。 |
| [N014](05-data-types.md#n014) | 对已授权但缺失的可选业务字段，以及显式存储的 null，必须统一映射为关系视图中的 SQL NULL。 |
| [N015](05-data-types.md#n015) | JSON 不是 v1 核心类型。 |
| [N016](06-type-resolution.md#n016) | 同一参数重复出现时，必须解析为同一个声明类型。 |
| [N017](06-type-resolution.md#n017) | 除明确规定的浮点转换外，CAST 必须精确生成指定类型，否则返回类型化错误。 |
| [N018](07-expressions.md#n018) | WHERE、ON、HAVING 及搜索式 CASE 的条件必须为 BOOLEAN。 |
| [N019](07-expressions.md#n019) | 布尔求值顺序不构成对用户可见的短路保证。 |
| [N020](07-expressions.md#n020) | 对标量表达式，未选中的 CASE 结果以及 COALESCE 已选中值之后的参数，不得引发运行时值错误。 |
| [N021](08-select.md#n021) | SELECT 的行为必须等价于以下顺序：绑定并授权关系／列 → 获取经资格验证的输入视图 → 对每个关系应用行策略 → FROM/JOIN → WHERE → 存在时执行 GROUP／聚合 → HAVING → 投影 → DISTINCT → ORDER BY → 逻辑 LIMIT/FETCH → 经授权发布结果。 |
| [N022](08-select.md#n022) | 默认 SELECT ALL 必须保留重复的投影行。 |
| [N023](08-select.md#n023) | 所有可空排序键，包括因 LEFT JOIN 而变得可空的键，都必须要求 `read.nullable_order`。 |
| [N024](08-select.md#n024) | 不写 LIMIT 必须表示在显式资源约束下返回完整逻辑结果，而不是使用未记录的默认 LIMIT。 |
| [N025](09-joins.md#n025) | ON 必须是非空的带类型相等条件合取，每项比较左侧关系的一列与右侧关系的一列。 |
| [N026](09-joins.md#n026) | 两个输入关系必须从同一个经资格验证的一致视图读取；禁止连接独立实时分页 API 的结果。 |
| [N027](10-aggregates.md#n027) | 在分组查询中，SELECT/HAVING/ORDER BY 内所有非聚合列引用都必须是 GROUP BY 键。 |
| [N028](10-aggregates.md#n028) | 除 COUNT(*) 外的聚合必须忽略 SQL NULL 输入。 |
| [N029](11-optional-relational.md#n029) | CTE 必须保留多重集合、NULL、类型、血缘及已授权一致视图语义。 |
| [N030](11-optional-relational.md#n030) | UNION ALL 各分支必须共享语句的经资格验证的一致视图及授权血缘。 |
| [N031](12-data-modification.md#n031) | W1 必须编译为现有作用域内的带类型命令，并在一个原生事务中满足原有 Operation/Outbox/guard 约束。 |
| [N032](12-data-modification.md#n032) | INSERT 成功时必须提交修订号为 1 的行，并返回 affected_rows=1。 |
| [N033](12-data-modification.md#n033) | UPDATE/DELETE 必须带 WHERE 谓词，该谓词是原子比较／NULL 检查的合取，并强制包含精确的 `id = value` 和 `revision = value` 两项。 |
| [N034](12-data-modification.md#n034) | 普通未匹配 UPDATE/DELETE 必须返回 affected_rows=0 和空 RETURNING 行集，对目标不存在、不可见、修订号不匹配或附加条件不匹配保持一致。 |
| [N035](12-data-modification.md#n035) | 已提交写入的 RETURNING 内容若当前无法发布，必须保留其已提交操作结果。 |
| [N036](13-transactions.md#n036) | 事务必须原子验证当前原生主体／会话／会话族、Schema／映射、记录守卫及准入约束，然后一起提交业务变更、有序逐项结果、原始 Operation 收据及 Outbox 记录。 |
| [N037](13-transactions.md#n037) | 每次已接纳执行必须具有一个原始幂等键，绑定主体、作用域／环境代次、语言／编译器／档位指纹、规范化带类型 IR、带类型值、预期修订号及有序批次断言。 |
| [N038](13-transactions.md#n038) | 回复丢失、到达截止时间、客户端断开、缺少观察结果或收到取消请求，均不得被解释为回滚、失败、底层物理执行完成或允许换新键修改。 |
| [N039](14-schema-migrations.md#n039) | 只有现有 Schema 服务，使用当前 SchemaAdmin 权限及具有安全围栏的维护权威，才能应用 DDL 提案。 |
| [N040](14-schema-migrations.md#n040) | 对非空关系执行带 NOT NULL 的 ADD COLUMN，必须有明确且经资格验证的默认值／回填来源，并在发布前实际验证。 |
| [N041](14-schema-migrations.md#n041) | 迁移必须采用：预览 → 预期版本检查 → 关闭准入／排空 → 扩展／回填 → 实际 Schema／数据／索引验证 → CAS 发布绑定 → 按当前安全水位重新开放。 |
| [N042](15-catalog.md#n042) | 目录数据必须从当前已授权、已发布的绑定生成，绝不能取自特权原生 Schema 导出。 |
| [N043](16-artifacts-explain.md#n043) | 校验必须完成解析、穷尽检查 AST 节点、解析已授权元数据、绑定类型／可空性／副作用、执行能力／大小／预算规划门槛检查，并记录不可变依赖修订号。 |
| [N044](16-artifacts-explain.md#n044) | 执行必须加载准确的制品修订版，并在访问后端前以及发布结果前再次检查当前授权和兼容性。 |
| [N045](17-parameters-results-pagination.md#n045) | 参数必须绑定标量值，绝不能绑定标识符、关键字、方向、表达式、作用域或可执行片段。 |
| [N046](17-parameters-results-pagination.md#n046) | 传输 page_size 不得改变 SQL LIMIT。 |
| [N047](17-parameters-results-pagination.md#n047) | 游标必须绑定主体／授权、查询／制品／带类型绑定摘要、版本、作用域／环境代次／安全序列、排序状态、剩余上限及原始到期时间。 |
| [N048](17-parameters-results-pagination.md#n048) | 响应必须区分完整逻辑结果、可继续读取的普通部分页面，以及因预算／截止时间／错误而不完整的结果。 |
| [N049](18-diagnostics.md#n049) | 错误必须包含稳定的 Mensoria 错误码、五字符 SQLSTATE 风格类别、经过敏感信息清理的消息、阶段、重试提示，以及已接纳且当前可见时的原始操作引用。 |
| [N050](19-budgets-cancellation.md#n050) | 已启用实现必须强制执行并公布源文本／请求体大小、AST 节点数／深度、结果列／页面字节数、修改行数、执行所有权、并发，以及计划使用的每种底层物理工作／中间资源界限。 |
| [N051](19-budgets-cancellation.md#n051) | 服务必须区分客户端等待超时、执行截止时间、取消意图、确认 worker 完成和确认提交结果。 |
| [N052](20-authorization-audit.md#n052) | SQL 必须复用原生行／字段授权、限定作用域的 Control 准入及当前会话／会话族检查。 |
| [N053](20-authorization-audit.md#n053) | 读取计划、历史、元数据、缓存结果、制品、游标及原始操作结果时，都必须按当前权限重新授权受保护内容。 |
| [N054](20-authorization-audit.md#n054) | 审计必须关联主体／作用域、制品／编译器／档位／Schema 版本、脱敏查询形状和带类型值摘要、原始操作、安全／环境代次水位、已消耗预算、执行结果及发布状态。 |
| [N055](21-extensions.md#n055) | 语言扩展在其解析器／执行器接受输入之前，必须登记稳定的 `mensoria` 命名空间、精确语法／签名、参数／结果编解码器、NULL 行为、确定性／副作用、作用域／血缘、限制、索引就绪条件、证据及版本规则。 |
| [N056](21-extensions.md#n056) | 外部模型调用、嵌入生成、HTTP／文件访问、对象上传及任务调度，不得作为隐藏 SQL 事务副作用发生。 |
| [N057](22-compatibility.md#n057) | 每个已接受制品必须绑定语言版本、草案／语义修订号、编译器指纹、已启用能力集，以及 Schema 适配器／后端配置。 |
| [N058](22-compatibility.md#n058) | SQL 兼容性、原生 SurrealQL 兼容性、PostgreSQL 线协议兼容性和具名客户端兼容性必须分别报告。 |
| [N059](23-conformance.md#n059) | 能力资格验证必须冻结源码／构建／编译器／解析器／后端／存储配置、夹具 Schema／策略／数据、能力限制，以及完整的带类型预期／实际结果。 |
| [N060](23-conformance.md#n060) | 文档检查、本地解析器／运行时测试、CI、驱动资格验证、真实客户验收及生产资格验证，必须独立记录。 |
