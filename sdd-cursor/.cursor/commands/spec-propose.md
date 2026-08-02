---
description: 写或整体重写 proposal.md（## Why / ## What / ## How / ## Risk）。前置硬门：research.md 的 [TBD] 必须为空。完成后输出 HARD GATE 等用户审批。
---

# /spec:propose

## 前置（先跑硬门，拦截即停）

```bash
python scripts/sdd.py gate
```

被拦截 → 按报错处理：缺 research → /spec:research；有 [TBD] → /spec:ask

## 流程

1. 读 research.md（`## Decided` + Practices/Constraints）+ design.md（若有）
2. 写 `spec/changes/<name>/proposal.md`：
   - `## Why` 动机（用户可感知）
   - `## What` 每条带 `| verify: <可观察行为/可执行检查>` 子句，段末 `### Not in this change` 排除清单
   - `## How` 结论 + 指向 design 的指针
   - `## Risk` 风险 + 回滚
   - 格式细节见 `references/proposal-spec.md`
3. **判断是否同时生成 tasks.md**（在 gate 上显式声明触发条件 + 拆分，不静默附带）：
   - 跨栈项目（apply 时前后端两个 spec-dev 并行） / >5 个独立子任务 / 多执行者
   - 格式见 `references/tasks-spec.md`；单线程简单实现不生成
4. **跑 critique 面板**（结构性对抗，不靠更聪明的单一作者）：
   - 并行派发独立上下文批评者（只读 proposal + design + research Decided），各锁定一个立场：
     - necessity（主审）：「默认反对每个措施」，四问反驳每个 What 项和 How 里的 fallback；静默 fallback（吞失败回退旧逻辑）无真实触发场景证据 → 建议删除；响亮守卫（边界校验/幂等/CAS/失败即抛）按"保护什么不变量 + 破坏半径"评判
     - regression-compat：破坏了什么现有行为/消费者/已装用户
     - testability / performance：仅用户点名时开
   - workflow 自动模式默认 necessity + regression-compat 两个；独立调用让用户多选
   - 纪律：证据-或-丢弃（必须引具体行 + 具体场景）；每镜头 ≤3 条；**仅一轮反驳**；面板永不否决
   - 存活发现写入 `verify.md` 作为 **round 0（stage: propose）**，稳定 V-N 编号
5. **输出 HARD GATE 固定块**（见 `.cursor/rules/sdd-core.mdc`），然后**等用户回复，不写任何代码**

## 反模式

- ❌ gate 批准前写代码
- ❌ research 还有 [TBD] 就写方案
- ❌ ## How 照抄 research Decided（蒸馏不搬运）
- ❌ What 项没有 verify: 子句（验收无从下手）
- ❌ 翻译段落标题（## Why 永远英文原形）
- ❌ 跳过 critique 面板或隐瞒未解决发现（gate 是剧场还是决策，取决于信息完整）
- ❌ 等 gate 期间自己加 APPROVED 标记（那是替用户批准）
- ❌ 用户驳回后还保留旧 APPROVED（/spec:revise 必须清除）