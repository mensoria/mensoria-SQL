# 6. 类型解析与转换

## 6.1 一般解析

<a id="n016"></a>

**N016.** 同一参数重复出现时，必须解析为同一个声明类型。参数位置必须从 1 连续编号，绑定必须恰好包含这些位置。不得通过试执行后端查询来推断类型。

当存在唯一明确的公共类型时，无类型 NULL 采用另一比较／赋值／CASE／COALESCE／UNION 操作数的类型。`NULL IS NULL` 无需标量载荷类型即可合法使用，因为其结果是不可空 BOOLEAN。`NULL = NULL` 合法，得到可空 BOOLEAN 的 UNKNOWN；编译器可以对这类比较使用内部的仅 NULL 类型。直接投影裸 NULL、结果全为 NULL 的 CASE/COALESCE，或没有类型约束的参数，都要求显式类型声明／CAST。

比较、CASE、COALESCE 和 UNION 的公共类型规则如下：

1. 相同类型保留该类型。
2. BIGINT 与 NUMERIC 混用时可以扩展为 NUMERIC(19,0)；解析得到的 p/s 必须能够精确表示两个值域。
3. 两个 NUMERIC(p,s) 类型取 scale=max(s1,s2)，整数位数=max(p1-s1,p2-s2)，p=整数位数+scale。若 p>38，绑定时拒绝表达式，不得静默减少小数位数。
4. 不进行 TEXT／数值／BOOLEAN／UUID／时间戳之间的隐式转换；不进行精确数值与 DOUBLE 之间的隐式转换。

## 6.2 显式 CAST

<a id="n017"></a>

**N017.** 除明确规定的浮点转换外，CAST 必须精确生成指定类型，否则返回类型化错误。SQL NULL 可以转换为任意已启用标量类型，且结果仍为 SQL NULL。

| 来源 → 目标 | 行为 |
| --- | --- |
| 相同类型 | 恒等转换，但仍需验证目标类型修饰参数 |
| TEXT → BIGINT | 仅允许可选正负号及数字，无空白；范围为有符号 64 位 |
| TEXT → BOOLEAN | 仅允许不区分大小写的 `true` 或 `false`，无空白 |
| TEXT → NUMERIC(p,s) | 仅允许带符号的十进制／整数写法；不允许指数；允许补齐目标小数位，拒绝丢弃非零位 |
| BIGINT / NUMERIC → NUMERIC(p,s) | 必须精确表示；可移除多余的小数零，不舍入 |
| NUMERIC → BIGINT | 小数部分必须为零，且数值在范围内 |
| BIGINT / NUMERIC → DOUBLE | 仅在启用 `type.double` 时允许；明确允许按 binary64 最近值、恰好中点取偶数舍入；拒绝溢出 |
| TEXT → DOUBLE | 使用后端配置中指明的严格有限十进制／指数解析器；拒绝首尾空白、NaN 和无穷值 |
| TEXT → UUID | 标准带连字符的 8-4-4-4-12 十六进制形式；输入不区分大小写，输出规范化为小写 |
| TEXT → TIMESTAMP WITH TIME ZONE | RFC3339 日期时间，包含 `T`、秒，以及必需的 `Z` 或 ±HH:MM；小数最多 6 位，不允许闰秒 |
| BIGINT/NUMERIC/BOOLEAN/UUID/时间戳 → TEXT | 与区域设置无关的规范编解码写法；时间戳输出 UTC `Z` |

DOUBLE → TEXT 使用固定版本的、能保证有限值往返的最短字符串编解码器；DOUBLE → 精确数值暂缓。时间戳转换拒绝 `-00:00`（表示本地偏移未知）、超范围的本地组成部分／偏移，以及偏移归一化后超出年份 0001–9999 的 UTC 时刻。数字偏移的小时必须为 00–23、分钟为 00–59；转换后检查 UTC 跨日／跨年，不得钳制到边界。未列出的 UUID／数值／BOOLEAN 跨类型转换不受支持。NUMERIC → TEXT 保留声明的小数位数；BIGINT 无前导加号或前导零；BOOLEAN 使用小写 `true`／`false`。浮点 TEXT 解析和格式化必须固定在实现指纹中，原生库默认行为本身不是契约。
