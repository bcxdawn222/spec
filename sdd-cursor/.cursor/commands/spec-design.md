---
description: 技术设计（按需）。架构图（结构不画字段）/ 接口契约（精确 schema）/ 数据模型 / 争议决策深度论证。跨栈改动强制先做设计钉死契约。
---

# /spec:design

## 何时必做

- 前后端跨栈（含接口契约变更）← **强制**
- 接口 >3 个
- 需要架构图/数据流图/时序图
- 深度决策论证 >300 字

## 产出（spec/changes/<name>/design.md）

- `## Architecture` — 架构图（结构级，不画字段）
- `## Interfaces` — 接口契约：endpoint/method/path + 输入 schema + 输出 schema + 错误码/错误结构（**精确到可直接实现**，不算叙述预算）
- `## Data Model` — 数据模型
- `## Migration` — 迁移方案（若有）
- `## Key Decisions` — 只展开 1-2 个**真正有争议**的决策（各 ≤12 行）

## 纪律

- 叙述/论证 ≤150 行（契约除外）；>20 节点图拆分成多个
- 业务动机 → proposal.md Why（不写）；风险/回滚 → proposal.md Risk（不写）
- research.md 的 DEC-N 结论**引用不转抄**
- 契约不精确是真正的失败——宁可长，不可含糊