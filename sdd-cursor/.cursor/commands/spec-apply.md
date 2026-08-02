---
description: 实施阶段。按 proposal/tasks 推进实现。前置硬门：proposal 四段齐全 + 单一 active change。验证模型：实施中自跑秒级工作检查；收尾派发一次独立 spec-verifier 写入账本。
---

# /spec:apply

## 前置 + 自动批准

1. 先跑硬门（拦截即停，不绕过）：
```bash
python scripts/sdd.py apply-check
```
2. proposal.md 无 APPROVED 标记 → **立即追加** `<!-- APPROVED: YYYY-MM-DD HH:mm -->`（把用户本次调用视为批准动作；已有标记不重复追加）
3. research.md `## Decided` 有 `escalated` 项 → **输出首行必须回显**："Implementing with <N> escalated decisions: <一行一个>"（第二次知情同意点）

## 范围

- 无 tasks.md → 按 proposal `## What` 顺序推进
- 有 tasks.md 单执行者 → 按任务顺序；多执行者 → 只做本 owner 任务

## 派发 spec-dev 子代理（按 What 类型）

| What 涉及 | 派发 |
|---|---|
| UI/路由/组件/样式/前端交互 | spec-dev（scope: frontend） |
| 服务端/API/数据模型/DB 迁移/中间件 | spec-dev（scope: backend） |
| **跨栈（含契约变更）** | **先钉死契约 → 并发派两个 spec-dev（frontend + backend）** |
| 配置/脚本/CI/文档 | 主对话自己做 |

- 派发 prompt 必须写明 `scope: frontend/backend/fullstack` + **原样携带 What 的 `Not in this change` 清单**（触碰排除范围 = 停下报告，扩范围是用户决定）
- 跨栈串行是被禁止的：契约先落地 design.md `## Interfaces`（缺契约拒绝派发，先 /spec:design），然后并行实施，联调阶段再接真数据

## 可选强化旗标

`/spec:apply design`（前端 agent 读 references/frontend-aesthetics.md 防 AI 味）
`/spec:apply solid`（读 agent-principles.md §1 防偷懒）
`/spec:apply verify`（读 agent-principles.md §2 防幻觉）
可组合：`/spec:apply design solid verify`。默认不开。

## 实施 + 验证模型

- **独立验证是终局事件，不是节奏**：实施中只跑自己的工作检查（秒级自跑，不写账本，不派子代理）；最后一个 What 项落地后派发**唯一一次**独立 spec-verifier（新上下文，实施对话不能自审），结果写入 `verify.md` 账本轮，**然后才算实施完成**——没有独立账本轮覆盖最终状态的 "done" 不是 done
- 按 deps 推进，只碰依赖完成的任务；每完成一个节点就近跑该节点的检查（编译/测试），别攒到结尾
- 完成的任务在 tasks.md 勾选 `[x]`（谁完成谁勾）

## 失败分诊

| 症状 | 类别 | 处理 |
|---|---|---|
| 没按 proposal 实现 | 实施不完整 | 继续实施 |
| 语法/类型/边界错误 | 单点 bug | 直接修 |
| 做了 proposal 没要求的事 | 漂移 | 回到 proposal 对齐 |
| 完全按 proposal 做还是错 | **方案错了** | 停，走 /spec:revise（不要静默改 proposal 迁就代码） |

**永远不要静默改 proposal 去适配已写代码**——proposal 是"该做什么"的真相。

## Stuck 保护

同一错误/场景 3 次连续修复失败 → 停止报告（格式见 AGENTS.md），等用户裁决。

## 反作弊

- 没跑过的不报成功（成功带证据：命令 + 退出码/关键输出）
- 让它"看起来通过"的绕过（mock 假响应/改断言/检查函数 return true）必须明说 "bypass，根因未解决"
- 硬编码加注释 + tasks.md 注明"仅适用于本案例"

## 编码宪章（本阶段对所有写码者生效）

写任何代码前先读 `references/code-charter.md`。核心：失败必须响亮（该抛就抛，**绝不静默改道**）；改逻辑是替换不是叠加（**绝不保留旧逻辑当 fallback**——脏数据第一大来源）；核心逻辑 fail-fast；降级只发生在信任边界且必须响亮。fallback/降级/compat 是 **gate 级决策**：proposal How/Risk 未授权就不许写——verify 的 charter 审计把未授权 fallback 记为发现（数据写路径 = critical）。

## 不做的事

- 不 commit/push（除非用户要求）
- 不归档（用户说 archive 才做）
- 不改 proposal 迁就代码