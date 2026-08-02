---
description: 调研阶段。调研业界实践 + 关键约束 + 标出 [TBD] 待决点，写 research.md。结果快照进 research/ 弃稿堆，不删除。
---

# /spec:research

Direction: $ARGUMENTS

## 流程

1. 先读 `spec/knowledge.md`（若有）：项目级持久事实优先复用，不重复调研
2. 若已有旧方向 research.md → 快照到 `spec/changes/<name>/research/`（弃稿堆，可复活），再写新的
3. 调研并写入 `spec/changes/<name>/research.md`：
   - `## Practices`：业界做法，一句话一个结论，带来源
   - `## Constraints`：技术/业务/兼容性约束
   - `## Open [TBD]`：待决点（**别急着替用户决定**）
   - `## Decided`：已决项 DEC-N（结论 + 一行理由 + auto/escalated 标记）
4. 新出现的 [TBD] 必须落进 `## Open [TBD]`

## 纪律

- 只写外部信息；架构/接口/数据模型 → 留给 design.md
- 深挖搜索交给 researcher 子代理；跨文件检索交给 code-explorer
- 独立调研可并发派发
- 产出 ≤ 每条一行；深度论证不写在这里（→ design.md 争议决策节）