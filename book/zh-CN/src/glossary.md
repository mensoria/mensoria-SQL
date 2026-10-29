# 术语表

本表用于说明性查阅；规范定义仍以[第 1 章](01-purpose.md)为准。

| 术语 | 本书含义 | 主要参考 |
| --- | --- | --- |
| 制品 Artifact | 不可变且经校验的源文本／带类型计划修订版；校验不授予执行权限 | [16](16-artifacts-explain.md) |
| 绑定 Binding | 已发布的逻辑到原生 Schema 映射 | [3](03-database-model.md) |
| CAS | 依据预期修订号比较并更新 | [12](12-data-modification.md) |
| 完整结果 | 包含显式上限在内的全部请求逻辑结果 | [17](17-parameters-results-pagination.md) |
| 守卫 Guard | 执行时触碰的现有原生授权／准入冲突边界 | [13](13-transactions.md) |
| 环境代次 Incarnation | 恢复代次；旧目标／制品不能静默成为当前对象 | [3](03-database-model.md) |
| IR | 独立于上游 AST 的闭合带类型中间表示 | [22](22-compatibility.md) |
| Keyset | 基于有序末键状态继续读取；普通页面是实时列表，不是快照 | [17](17-parameters-results-pagination.md) |
| 操作 Operation | 绑定原始键的现有持久执行／结果权威 | [13](13-transactions.md) |
| Outbox | 与业务变更和收据在同一事务提交的事件意图 | [13](13-transactions.md) |
| 档位 Profile | 最低符合性能力集合，例如 R1 或 W1 | [2](02-profiles.md) |
| 结果发布 Publication | 经最终授权释放内容或后续读取能力 | [20](20-authorization-audit.md) |
| 已验证资格 Qualified | 已冻结实现配置并具有所需通过证据 | [23](23-conformance.md) |
| UNKNOWN | 表达式中 NULL 的真值解释；不同于执行结果未知 | [7](07-expressions.md)、[13](13-transactions.md) |
