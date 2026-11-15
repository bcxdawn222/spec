<div align="center">

# spec-workflow

**Spec-Driven Development workflow for Claude Code, Codex CLI & Cursor**

Make large changes controllable and reversible — research, interrogation, proposal, **HARD GATE**, implementation, independent verification, archive. Every step is re-entrant, hard-constrained, and delegatable.

[![Version](https://img.shields.io/badge/version-0.11.1-blue.svg)](https://github.com/bcxdawn222/spec)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/bcxdawn222/spec)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**One workflow. Three hosts.** · [中文说明](README_cn.md)

</div>

---

## 当前版本与宿主范围

Claude Code 和 Codex CLI 已同步 [kamioj/spec-workflow 0.11.1](https://github.com/kamioj/spec-workflow/commit/568585ed3e8d5fa356eac51756d3aa65035d0438)，提供 18 个命令。Cursor 端采用本仓库独立维护的 12 命令适配，功能范围见其使用说明。

- 新增阶段网页视图，支持调研、问询、架构设计、方案和验收记录的标准或高级排版。
- 高级视图支持架构流程图、任务依赖图，以及可选择并复制回复的问询页和方案页。
- 新增知识库整理与无活动 spec 时的 diff 验证，并改进 Windows 钩子启动及 CRLF 文档兼容性。

升级后的 Codex 项目会话可运行 `$spec-view all advanced zh`，Claude Code 可运行 `/spec:view all advanced zh`。文档更新后重新运行视图命令刷新页面，交互页面的回复文字需要粘回会话完成确认。

开发检查通过 `python scripts/check.py` 或 `sh scripts/check.sh` 执行，检查日志写入仓库内的 `logs` 目录。

## Why

AI-assisted spec-driven development has two established paradigms:

- **Fast flow**: start coding immediately, hooks as backstop — easy to drift
- **Heavy flow**: spec-first but rigid — OpenSpec's 4 commands, 9-step superpowers

**spec-workflow takes a third path**: keep the value of "think before you act", but split the flow into **18 independent commands** for Claude Code and Codex CLI — every phase is re-entrant, interruptible, and redoable in isolation. Three hard-gate hooks make the flow **actually stop where it should**, and a Stop driver turns `/spec:loop` self-driving rounds into a hard mechanism.

### What makes it different

| Dimension | spec-workflow | OpenSpec | superpowers |
|---|---|---|---|
| Phase control | Explicit HARD GATE + hook interception | Fluid soft warnings | 9-step rigid flow |
| Pending decisions `[TBD]` | Allowed + hook-enforced clearing | Open Questions can linger | Forbidden |
| Command granularity | 18 independent commands (Claude Code / Codex CLI) | 4-command monolith | skill-based single flow |
| Mid-flow re-entry | Every phase independently callable | `/opsx:continue` | Start over |
| Anti-cheating | Commands + agent + opt-in flags | None | Implicit |

Positioning: **single developer + large changes + fool-proofing** — stricter than OpenSpec, more flexible than superpowers.

---

## Features

- **Full pipeline**: research → ask → (design) → propose → **HARD GATE** → apply → verify → archive
- **Hard gates enforced by hooks, not by prompts**: attempting to skip a step gets blocked with the reason — 0% violation rate (Claude Code / Codex CLI)
- **Independent verification**: `spec-verifier` runs in a deliberately fresh context — the conversation that wrote the code never audits itself; evidence-first, Iron Law: *no pass without fresh verification evidence*
- **Verification ledger** `verify.md`: stable finding IDs (V-N), round diffing, unfixed-items escalate to fail
- **Anti-cheating clauses**: nothing unrun is "success"; bypasses must be declared; self-reported success gets independently re-run
- **Stuck protection**: 3 consecutive failed fixes → forced stop with self-check; blind retries don't count
- **Charter audit**: hunts silent fallbacks / swallowed exceptions / old-logic fallbacks — the dirty-data class (critical on data-write paths)
- **Cross-stack delegation**: frontend + backend `spec-dev` agents run in parallel against a pinned interface contract
- **Built-in stack conventions**: Vue / React / uni-app (mini-program) / Java / Python / Flutter / TS style packs
- **One workflow, three hosts**: Claude Code plugin, Codex CLI plugin, Cursor IDE port

---

## Quick Start

### Claude Code

```bash
claude plugin marketplace add bcxdawn222/spec
claude plugin install spec@spec-workflow
# or local: claude --plugin-dir .
```

Then in a session:

```
/spec:workflow "add login + cart to the uni-app storefront"
```

### Codex CLI

```bash
codex plugin marketplace add bcxdawn222/spec
codex plugin add spec@spec-workflow
```

Then in a session:

```
$spec-workflow "add login + cart to the uni-app storefront"
```

### Cursor

```powershell
# copy the port into your project root
Copy-Item sdd-cursor\.cursor -Recurse -Force
Copy-Item sdd-cursor\AGENTS.md -Force
Copy-Item sdd-cursor\scripts -Recurse -Force
Copy-Item sdd-cursor\templates -Recurse -Force
Copy-Item sdd-cursor\references -Recurse -Force
# restart Cursor, then:
/spec:workflow "add login + cart to the uni-app storefront"
```

---

## Claude Code / Codex CLI 的 18 个命令

| Command | Responsibility |
|---|---|
| `/spec:workflow <task>` | run the whole flow end-to-end; stops at exactly two points — HARD GATE and acceptance |
| `/spec:loop <goal>` | goal-driven autonomous rounds (Plan → Act → Verify → Retrospect) with mechanical circuit breakers |
| `/spec:research <dir>` | survey practices + constraints, flag `[TBD]` |
| `/spec:ask` | resolve `[TBD]`s (interactive, or auto-triage inside workflow) |
| `/spec:design` | architecture / interface contracts / data model (mandatory for cross-stack) |
| `/spec:propose` | write the four-section proposal + critique panel → emit HARD GATE |
| `/spec:revise <section>` | revise one section, clear APPROVED marker, re-emit gate |
| `/spec:apply` | implement (auto-appends APPROVED; dispatches spec-dev, parallel for cross-stack) |
| `/spec:verify` | independent spec-verifier audit → update ledger |
| `/spec:status` | report current phase |
| `/spec:chat` | discussion mode, touches no documents |
| `/spec:archive` | gate-checked archive + retrospect + knowledge.md |
| `/spec:fix <task>` | 小改动按日期记录到修复批次 |
| `/spec:ship [date]` | 检查并完成一个修复批次 |
| `/spec:stash` | 暂停当前变更 |
| `/spec:resume [name]` | 切换或恢复指定变更 |
| `/spec:view [stage] [tier] [lang] [dir]` | 生成阶段产物的 HTML 网页视图 |
| `/spec:knowledge [focus]` | 整理项目知识库并选择需要沉淀的经验 |

---

## Repository Layout

```
/                      ← Claude Code plugin (repo root, /spec:x)
├── .claude-plugin/    ← plugin manifest
├── commands/ agents/ skills/ hooks/ rules/ tools/
├── core/              ← single source of truth (node tools/generate.mjs regenerates both hosts)
├── codex/             ← Codex CLI plugin ($spec-x skills + hooks)
└── sdd-cursor/        ← Cursor IDE port (commands + agents + Python hard-gate CLI)
```

> **For contributors**: edit `core/`, never the generated trees. `node tools/generate.mjs` propagates to both plugin trees; `--check` detects drift.

---

## Verification Ledger Example

```markdown
## Round 0 (stage: propose)
| ID | Dimension | Severity | Status | Finding | Evidence |
|---|---|---|---|---|---|
| V-1 | charter | major | fixed | silent fallback on data-write path | catch swallowed exception |

conclusion: fail → round 1 → fixed → pass
```

Severity is strictly `critical / major / minor`; conclusion is strictly `pass / fail` — no conditional passes.

---

## License

MIT. The `references/` content is self-authored distillation of official style guides (source noted in each file's frontmatter).

---

<div align="center">

Built for teams who want AI to *finish* the job, not just *start* it.

[![Star History](https://img.shields.io/github/stars/bcxdawn222/spec.svg?style=social)](https://github.com/bcxdawn222/spec)

</div>
