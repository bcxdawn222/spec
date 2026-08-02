---
description: 修改 proposal.md 单个段落（why/what/how/risk）。改动后清除旧 APPROVED 标记，重新输出 HARD GATE（标题改为 Proposal revised）。
---

# /spec:revise

Section: $ARGUMENTS

## 用法

- `/spec:revise why` / `/spec:revise what` / `/spec:revise how` / `/spec:revise risk`
- 不带参数 → 询问用户改哪段（自包含问题）

## 流程

1. 只改指定段落；其他段落一字不动
2. **清除旧的 `<!-- APPROVED: ... -->` 标记**（用户驳回/修改后批准自动失效）
3. 若改了 What → 检查受影响的 verify: 子句是否仍可证伪；若改了 How/Risk → 检查 design.md 是否需要同步
4. 重新输出 HARD GATE 块，标题改为 `=== Proposal revised (<段落>) ===`，并注明"旧 APPROVED 标记已清除"

## 纪律

- 不借 revise 扩写非目标段落（防文档膨胀）
- 用户评估意见逐项 adopt / refute / partial 回应后落笔
- 用户坚持的项照改并记入账本为 user-override