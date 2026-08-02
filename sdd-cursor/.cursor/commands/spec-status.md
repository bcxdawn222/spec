---
description: 查看当前阶段与产物状态。不写任何文件。
---

# /spec:status

运行：

```bash
python scripts/sdd.py status
```

## 汇报格式

- 当前 active change（若多个 → 提示先归档其余的）
- 所处阶段：research / propose（待审批）/ apply（已批准）/ verify（账本已存在）
- 已生成产物清单
- 下一步建议（自包含：做什么 + 为什么 + 结果）：
  - research.md 有 [TBD] → `/spec:ask` 消解后 `/spec:propose`
  - proposal 缺段 → `/spec:revise <section>`
  - 已批准未验证 → `/spec:verify`
  - 账本 open 项 → 修复后重验

只报告，不推进流程、不改文件。