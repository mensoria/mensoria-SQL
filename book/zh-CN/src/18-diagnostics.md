# 18. 诊断

<a id="n049"></a>

**N049.** 错误必须包含稳定的 Mensoria 错误码、五字符 SQLSTATE 风格类别、经过敏感信息清理的消息、阶段、重试提示，以及已接纳且当前可见时的原始操作引用。能够安全定位时可附带源位置范围。不得包含受保护原生文本、资源存在性细节、值、凭据或后端堆栈。

| 错误码 | 类别 | 触发条件 |
| --- | --- | --- |
| SQL_SYNTAX_ERROR | 42601 | 无效词法单元／语法或额外语句 |
| SQL_FEATURE_UNSUPPORTED | 0A000 | 已规定可选能力未启用、暂缓语法或不支持节点 |
| SQL_REFERENCE_DENIED | 42501 | 未知／未授权公共引用 |
| SQL_TYPE_ERROR | 42804 | 类型不兼容、编解码／来源映射无效或类型未解析 |
| SQL_VALUE_OUT_OF_RANGE | 22003 | 溢出、不允许的精度损失或非有限数字 |
| SQL_INVALID_TEXT_VALUE | 22018 | 文本无法解析为声明标量类型 |
| SQL_DIVISION_BY_ZERO | 22012 | 实际求值的数值除法除以零 |
| SQL_AMBIGUOUS_REFERENCE | 42702 | 允许使用的名称匹配多个已授权对象 |
| SQL_INVALID_GROUPING | 42803 | 聚合位置非法或引用未分组列 |
| SQL_ARTIFACT_STALE | 55000 | 执行依赖修订版不兼容 |
| SQL_WRITE_PRECONDITION_REQUIRED | 0A000 | 缺少 W1 强制守卫形状，或形状不安全 |
| SQL_PRECONDITION_FAILED | 40001 | 显式受影响行数断言失败 |
| SQL_CONSTRAINT_CONFLICT | 23000 | 经过敏感信息清理的完整性约束冲突 |
| SQL_KEY_CONFLICT | 23000 | 已有原始键绑定到不同请求身份 |
| SQL_BUDGET_EXCEEDED | 54000 | 超出已证明的资源界限，或计划缺少所需可强制执行预算 |
| SQL_CURSOR_INVALID | 24000 | 游标到期或绑定／版本不匹配 |
| SQL_RESULT_EXPIRED | 55000 | 原受保护结果不再保留 |
| SQL_OUTCOME_UNKNOWN | 08007 | 已接纳操作／提交尚未确认 |
| SQL_DEPENDENCY_UNAVAILABLE | 08006 | 必需依赖不可访问 |
| SQL_CANCEL_PENDING | 57014 | 已请求取消，但物理执行／提交结果尚未确认 |

这些类别不承诺 PostgreSQL 驱动行为。尤其是，40001 绝不授权盲目换新键重试，57014 绝不证明回滚。客户端必须联合使用 Mensoria 错误码、phase、retry_hint 和操作引用。

重试提示为 `edit`、`revalidate`、`restart_read`、`reconcile_original`、`observe_original`、`none`。准入之后的不确定性，优先于表面上会暗示“没有执行任何工作”的传输／前置条件错误。授权失败可以隐藏操作可见性，但不改变其持久结果。
