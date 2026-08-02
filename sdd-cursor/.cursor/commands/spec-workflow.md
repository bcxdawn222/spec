---
description: 完整 SDD 流程，端到端，需求全权委托。开放决策内部自动分诊（不中途提问）；只在两个点停下——HARD GATE 和验收/归档。用户作为评估者参与，评估轮次不限。触发词: spec first / proposal / design first / draft a plan / 先写方案。
---

# /spec:workflow

Task: $ARGUMENTS

## 适用边界

大改动（>150 行 / 涉及 3+ 文件 / 引入新依赖 / 架构决策）。小/中改动直接做，**绝不**激活本流程。

## 执行顺序（逐阶段调用，任一阶段被拒或 gate 失败 → 停下报告，不硬推）

1. **/spec:research "<方向>"** — 调研业界实践 + 关键约束 + 标出 [TBD] 待决点
2. **/spec:ask（auto-triage 模式）** — 不盘问用户；把每个 [TBD] 分诊进 `## Decided`：
   - 事实类 → 查证据定；可逆偏好 → 自决 + `auto` 标记；不可逆/产品语义 → 自决 + `escalated` 标记（gate 置顶展示，除非被推翻）
   - 每个自决过四问过滤器；"不做/最小实现"永远是候选
   - 流程后期冒出的新 [TBD] 同样内部消解，绝不中途提问
3. **判断是否要 /spec:design** — 满足任一即必做：
   - 前后端跨栈（含接口契约）← **强制**
   - 接口 >3 个
   - 需要架构图/数据流图/时序图
   - 深度决策论证 >300 字
4. **/spec:propose** — 写四段式 proposal.md，然后跑 critique 面板（默认镜头：necessity 主审 + regression-compat；一轮反驳；存活发现写入账本 round 0）
   - 写之前先跑 `python scripts/sdd.py gate`
5. **HARD GATE（触点 1/2）** — 按 rules 输出固定块，置顶 escalated 决策，等待
   - 用户回复是评估：逐项 adopt / refute / partial，一轮回完，用户终审
   - **写零行代码直到用户回复**
6. **/spec:apply** — 实施（先跑 `python scripts/sdd.py apply-check`；apply 自动追加 APPROVED 标记；首行回显 escalated 决策）
7. **验收 = apply 收尾账本轮** — apply 已派发唯一一次独立 spec-verifier 并写入账本；本步消费该轮：开 critical/major 发现 → 修复 → 限定重验（≤2 轮自动修复）；仍有未清项 → 带进验收报告，不无限磨
8. **验收（触点 2/2）** — 先报未清账本项 + escalated 决策，等待
   - 用户验收反馈同样是评估：逐项 adopt / refute / partial，采纳项记为 user-sourced findings（稳定 V-N）→ 修复轮 → 重验
   - **无轮次上限**——直到用户说 archive → /spec:archive

## 流程中途可插队命令

- /spec:chat — 讨论模式，不动文档
- /spec:ask — 追加一轮消解（新冒出的 TBD）
- /spec:research "<新方向>" — 重新调研（旧产物快照保留，不删）
- /spec:status — 查看当前阶段

## 反作弊（全程）

- 没跑过的命令/输出不得报成功；绕过必须明说"bypass，根因未解决"
- 硬编码必须注释 + tasks.md 注明
- 别处自报成功不算验证，独立重跑
- 任务前提错误（矛盾需求/超范围/工具不兼容）→ 停下报告 "task is not feasible"