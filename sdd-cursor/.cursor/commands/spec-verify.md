---
description: 验收阶段。派发独立全新上下文的 spec-verifier 子代理（实施对话永不自审），三维度 + charter 审计，证据先行。每次运行更新验证账本 spec/changes/<name>/verify.md（稳定发现编号 + 轮次对比 + 未修升级）。
---

# /spec:verify

## 为什么派独立子代理

刚写完代码的对话不能审计自己的输出——同一上下文、同一盲点，"要求它客观"实测几乎无效。**独立性就是机制**。

## 流程

1. 确认当前 active change；读 proposal.md 的 `verify:` 子句（验收清单）+ `Not in this change`（排除区）
2. 派发 spec-verifier 子代理（fresh context，只读项目源码）：
   - **Completeness**：每个 What 项对照 verify: 子句；无子句的项标记（禁止自创通过）
   - **Correctness**：编译/测试/边界，每条结论必须铁律证据（无证据不算通过）
   - **Coherence**：匹配 How 决策；无范围蔓延；`Not in this change` 内零修改
   - **Charter audit**：猎静默 fallback / 吞异常返默认值 / 新逻辑回退旧分支 / `|| defaultValue` 链掩盖失败——可用 ast-grep 机器扫描（references/rules 有配置），否则手动 Grep 上述模式；命中项按"是否可溯源到 proposal How/Risk 决策"判定（可溯源且响亮降级 → 非发现；不可溯源 → major；数据写路径 → critical）
3. 结果写入 `verify.md` 账本：稳定 V-N 编号、严重级（critical/major/minor 三档）、状态、每轮证据
4. 报告 conclusion: **pass / fail 二值**（有 critical/major 存活或任一 verify: 子句未满足 = fail）

## 发现格式（证据先于结论，硬格式）

```
[DIMENSION: completeness|correctness|coherence|charter]
[SEVERITY: critical|major|minor]
[FILE:LINE]
[EVIDENCE: ≤5 行真实代码引用]
→ FINDING: <一句问题描述>
```

- 没有可引用证据 = 不是发现（机械过滤幻觉发现）
- 每维度 ≤3 条，按严重级排序

## 反驳协议（返回前必跑）

- 阶段1 审计：列出全部可疑发现 + 证据，无视作者意图
- 阶段2 辩护：每条一行——proposal/design 哪个可引用决策授权了它？"看起来是有意的"不算辩护
- 阶段3 裁决：只返回活下来的发现；被辩护掉的记录引用后丢弃

## 豁免规则（硬编码，零裁量）

- fallback/守卫本身不是发现——只有 charter 溯源规则裁决
- 已有测试覆盖的路径不报"未测试"
- `Not in this change` 内不要求任何工作

## 修复轮（apply 收尾账本轮消费）

- open critical/major → 修复 → 重验（只限 open 发现 + 修复 diff，**不是全新全量跑**）
- 最多 2 轮自动修复；仍未清 → 带进验收报告，不无限磨
- 用户验收反馈的采纳项记为 user-sourced findings（稳定 V-N）→ 修复 → 重验，无轮次上限直到用户说 archive

## 铁律

**没有新鲜验证证据就没有通过。** 不算数的：上次运行的结果 / 部分检查冒充全量 / "应该能行"的信心 / 开发 agent 的自报（其 Evidence 字段是声明不是证明——关键命令自己重跑）。

## 反作弊

- 眼睛看代码通过 ≠ Correctness 通过——测试必须真跑
- partial 必须说明哪里 partial，"基本通过"永不接受
- 账本里 open 2+ 轮的项自动升级为 fail 处理