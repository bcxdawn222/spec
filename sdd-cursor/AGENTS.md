# SDD Workflow（Spec-Driven Development，Cursor 版）

本项目启用 spec-workflow 移植流程：**research → ask → propose → HARD GATE → apply → verify → archive**。
完整机制与命令索引见 `.cursor/rules/sdd-core.mdc`，各阶段细节见 `.cursor/commands/spec-*.md`。

## 激活边界（最重要）

- **流程仅由用户显式激活**：用户输入 `/spec:x` 命令，或明确说"先写方案 / 出个 proposal / 先设计"。
- 模型**绝不自行激活** spec 流程。大任务（>150 行 / 3+ 文件 / 新依赖 / 架构决策）最多给一行建议：
  "这个改动较大，要走 spec 流程吗？"——用户不回答就正常干活。
- 小改动（<30 行单文件、typo、日志、样式）永远不触发 spec。

## 全局通用原则（任何任务都生效）

### 反作弊
1. 没实际跑过的命令/测试**不得**报告为成功——成功声明必须带证据（命令 + 退出码/关键输出行）
2. mock 响应 / 改断言 / 把检查函数改成 return true 这类绕过，**必须**明说"bypass，根因未解决"
3. 硬编码（偏移量/固定哈希/一次性参数）必须加代码注释 + tasks.md 里注明"仅适用于本案例"
4. 别处 agent 或上一轮的自报成功不算验证——关键命令必须独立重跑

### Stuck 保护
同一方向连续 3 次修复失败 → 立即停下报告。一次尝试 = 新假设 + 代码改动 + 验证；
重跑同一代码/改 typo/调日志不算。第 2 次起必须说明上次为什么失败。

```
=== Stuck Self-Check ===
Symptom: <一行>
Three hypotheses tried:
  1. <假设> → <结果>
  2. <假设> → <结果>
  3. <假设> → <结果>
Inferred root cause: <能推断就写，否则 unknown>
Suggested new direction: <有就写，否则 awaiting user guidance>
```

### 任务不可行立即停
前提本身错了（需求自相矛盾 / 超出范围 / 工具不兼容）→ 停止并报告，不要硬做。

## 产物地图（spec/ 目录）

```
spec/
├── knowledge.md                  # 跨 change 的持久事实（archive 维护，research 先读）
├── changes/<change-name>/
│   ├── research.md               # 调研（Practices/Constraints/Open[TBD]/Decided）
│   ├── design.md                 # 可选：架构/接口契约/数据模型
│   ├── proposal.md               # 方案（Why/What/How/Risk + verify: 子句 + APPROVED 标记）
│   ├── tasks.md                  # 可选：任务清单（跨栈/>5子任务/多执行者）
│   ├── verify.md                 # 验证账本（稳定 V-N 编号 + 轮次 + 证据）
│   └── retrospect.md             # 归档复盘（archive 时写）
└── archive/YYYY-MM-DD-<name>/    # 归档目录
```

**职责边界**：每份内容只在唯一权威处写全，别处只引用不重述。
research 写外部信息；design 写内部技术结构；proposal 写决策记录；verify 写验证记录。
发明这四类之外的第五类文件需要用户明确同意。

## 硬门（sdd.py 强制检查）

| 检查 | 触发点 | 命令 |
|---|---|---|
| gate | /spec:propose 前 | `python scripts/sdd.py gate`（research 存在 + [TBD] 清空） |
| apply-check | /spec:apply 前 | `python scripts/sdd.py apply-check`（proposal 四段齐全 + 单一 change） |
| archive-check | /spec:archive 前 | `python scripts/sdd.py archive-check`（APPROVED + verify 账本 + tasks 勾选） |

退出码 2 = 拦截，**不得**强制绕过（归档的 force/abandoned 显式放行除外，需在 retrospect.md 记录原因）。
注意：Cursor 无 UserPromptSubmit hook，硬门由命令文档强制先跑脚本 + 本规则双保险，违规率低于纯提示词但非 0，agent 收到拦截必须停下处理。

## 语言规范

- 正文按用户工作语言；段落标题永远用英文原形（`## Why / ## What / ## How / ## Risk`），不许翻译（revise 按英文名定位段落）。