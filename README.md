# spec（二开仓库）

基于 [kamioj/spec-workflow](https://github.com/kamioj/spec-workflow)（MIT）的 Spec-Driven Development 工作流，二开基线仓库。

## 仓库结构

```
/                         ← 上游 kamioj/spec-workflow 原版内容（v0.5.x，未改动基线）
├── .claude-plugin/       ← Claude Code 插件（/spec:x 命令）
├── codex/                ← OpenAI Codex CLI 插件（$spec-x skills + hooks）
├── core/                 ← 单一事实源（generate.mjs 生成双端产物，改这里）
├── commands/ agents/ skills/ hooks/ rules/ tools/
└── README_cn.md          ← 原版中文说明（v0.5.x 快照）

sdd-cursor/               ← 二开产物 #1：Cursor 移植版（本仓库新增）
├── .cursor/commands/     ← 12 个 /spec:x 命令（Cursor slash commands）
├── .cursor/agents/       ← spec-dev / spec-verifier 子代理（独立验收）
├── .cursor/rules/        ← HARD GATE + 反作弊 + Stuck 规则
├── scripts/sdd.py        ← 硬门 CLI（gate / apply-check / archive-check，退出码 2 拦截）
├── templates/            ← research / proposal / tasks / verify 模板
└── references/           ← 编码宪章 + 栈规范（含 uni-app 小程序规范）
```

## 两套基线的定位

| 基线 | 宿主 | 特点 |
|---|---|---|
| 上游原版（根目录） | Claude Code / Codex CLI | 完整插件形态，shell hook 硬门，双端生成器 |
| sdd-cursor/ | Cursor IDE | 命令 + 子代理 + Python 硬门，无 hook 事件用脚本兜底 |

## 二开指南

- **改上游逻辑**：只改 `core/`，跑 `node tools/generate.mjs` 重新生成两端
- **改 Cursor 版**：直接改 `sdd-cursor/`，硬门逻辑在 `sdd-cursor/scripts/sdd.py`
- **新增能力**（如小程序/SaaS 专属规范）：`sdd-cursor/references/` 按栈添加，agent 派单时按栈加载

## 快速开始

```powershell
# Claude Code
claude plugin marketplace add kamioj/spec-workflow
# 或本地: claude plugin install ./

# Codex CLI
codex plugin marketplace add kamioj/spec-workflow

# Cursor（本仓库二开版）
cd 你的项目
.\sdd-cursor\install.ps1
# 重启 Cursor，/spec:workflow "需求描述"
```

License: MIT（上游）· 二开产物同样 MIT 延续。