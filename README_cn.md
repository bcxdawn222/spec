<div align="center">

# spec-workflow

**三端统一的 Spec-Driven 开发工作流：Claude Code · Codex CLI · Cursor**

让大改动可控可回滚——调研、拷问、提案、**HARD GATE 硬门**、实施、独立验收、归档。每步可重入、可硬约束、可派单。

[![Version](https://img.shields.io/badge/version-0.5.3-blue.svg)](https://github.com/bcxdawn222/spec)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**一套工作流，三个宿主。** · [English](README.md)

</div>

---

## 为什么

AI 辅助 spec-driven development 的两种既有范式：

- **快流**：直接动手、hook 兜底——容易跑偏
- **重流**：先 spec 后做但僵化——OpenSpec 4 命令、superpowers 9 步

**spec-workflow 走第三路**：保留"先想清楚再动手"的价值，把流程拆成 **12 个独立命令**——每阶段可重入、可中断、可单点重做。3 个硬门 hook 让"该停的地方真停下来"，外加 Stop 驱动器让 `/spec:loop` 自主轮次成为硬机制。

### 差异化对比

| 维度 | spec-workflow | OpenSpec | superpowers |
|---|---|---|---|
| 阶段控制 | 显式 HARD GATE + hook 拦截 | fluid 软警告 | 9 步硬流程 |
| 待决点 [TBD] | 允许 + hook 强制清空 | 可滞留 | 严禁 |
| 命令粒度 | 12 个独立命令 | 4 命令一把梭 | skill 单流程 |
| 中途重入 | 每阶段独立调用 | continue 推进 | 重头来 |
| 反作弊 | 命令 + agent 双层 + opt-in | 无 | 隐含 |

定位：**单人 + 大改动 + 防呆机制**——比 OpenSpec 严，比 superpowers 灵活。

---

## 特性

- **全流程**：research → ask → (design) → propose → **HARD GATE** → apply → verify → archive
- **硬门是 hook 拦截不是提示词**：跳过流程直接被拦下并给出原因——0% 违规率（Claude Code / Codex CLI）
- **独立验收**：`spec-verifier` 在刻意全新的上下文中运行——写代码的对话永不自审；证据先行，铁律：*无新鲜验证证据就没有通过*
- **验证账本** `verify.md`：稳定发现编号（V-N）、跨轮对比、未修复项自动升级为 fail
- **反作弊条款**：没跑过的不算成功；绕过必须声明；自报成功独立重跑
- **Stuck 保护**：同一方向 3 次连续失败 → 强制停止自检；盲重试不算
- **Charter 审计**：猎捕静默 fallback / 吞异常 / 回退旧逻辑——脏数据类缺陷（数据写路径 = critical）
- **跨栈并行派单**：前后端 spec-dev 按钉死的接口契约并行实施
- **内置技术栈规范**：Vue / React / uni-app（小程序）/ Java / Python / Flutter / TS 风格包
- **一套流程三个宿主**：Claude Code 插件 · Codex CLI 插件 · Cursor 移植版

---

## 快速开始

### Claude Code

```bash
claude plugin marketplace add bcxdawn222/spec
claude plugin install spec@spec
```

会话里输入：

```
/spec:workflow "做一个带登录的 uni-app 小程序商城"
```

### Codex CLI

```bash
codex plugin marketplace add bcxdawn222/spec
codex plugin install spec@spec
```

会话里输入：

```
$spec-workflow "做一个带登录的 uni-app 小程序商城"
```

### Cursor

```powershell
# 把 sdd-cursor 移植版复制到项目根
Copy-Item sdd-cursor\.cursor -Recurse -Force
Copy-Item sdd-cursor\AGENTS.md -Force
Copy-Item sdd-cursor\scripts -Recurse -Force
Copy-Item sdd-cursor\templates -Recurse -Force
Copy-Item sdd-cursor\references -Recurse -Force
# 重启 Cursor 后：
/spec:workflow "做一个带登录的 uni-app 小程序商城"
```

---

## 12 个命令

| 命令 | 职责 |
|---|---|
| `/spec:workflow <任务>` | 全流程托管，只停两个点——HARD GATE 与验收 |
| `/spec:loop <目标>` | 目标驱动自主循环（Plan→Act→Verify→Retrospect），机械熔断 |
| `/spec:research <方向>` | 调研实践 + 约束，标 [TBD] |
| `/spec:ask` | 消解 [TBD]（交互式 / workflow 内自动分诊） |
| `/spec:design` | 架构 / 接口契约 / 数据模型（跨栈必做） |
| `/spec:propose` | 写四段式方案 + critique 自审 → 输出 HARD GATE |
| `/spec:revise <段落>` | 改一段、清 APPROVED、重新出 gate |
| `/spec:apply` | 实施（自动追加 APPROVED；派 spec-dev，跨栈并行） |
| `/spec:verify` | 独立 spec-verifier 审计 → 更新账本 |
| `/spec:status` | 查看当前阶段 |
| `/spec:chat` | 讨论模式，不动文档 |
| `/spec:archive` | 硬门归档 + 复盘 + knowledge.md |

---

## 仓库结构

```
/                      ← Claude Code 插件（根目录 /spec:x）
├── .claude-plugin/    ← 插件清单
├── commands/ agents/ skills/ hooks/ rules/ tools/
├── core/              ← 单一事实源（node tools/generate.mjs 重新生成双端）
├── codex/             ← Codex CLI 插件（$spec-x skills + hooks）
└── sdd-cursor/        ← Cursor 移植版（命令 + 子代理 + Python 硬门 CLI）
```

> **给贡献者**：只改 `core/`，不要改生成的树。`node tools/generate.mjs` 自动同步双端；`--check` 检测漂移。

---

## 验证账本示例

```markdown
## Round 0（stage: propose）
| ID | 维度 | 严重级 | 状态 | 发现 | 证据 |
|---|---|---|---|---|---|
| V-1 | charter | major | fixed | 数据写路径静默 fallback | catch 吞异常 |

conclusion: fail → round 1 → fixed → pass
```

严重级严格三档 `critical / major / minor`；结论严格二值 `pass / fail`——没有"有条件通过"。

---

## License

MIT。`references/` 内容为对应官方规范要点的自有提炼（各文件 frontmatter 注明 source）。

---

<div align="center">

让 AI 不只是*开始*干活，而是*完成*交付。

[![Star History](https://img.shields.io/github/stars/bcxdawn222/spec.svg?style=social)](https://github.com/bcxdawn222/spec)

</div>