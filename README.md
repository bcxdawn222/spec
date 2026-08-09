<div align="center">

# spec-workflow

**Spec-Driven Development workflow for Claude Code, Codex CLI & Cursor**

Make large changes controllable and reversible — research, interrogation, proposal, **HARD GATE**, implementation, independent verification, archive. Every step is re-entrant, hard-constrained, and delegatable.

[![Version](https://img.shields.io/badge/version-0.5.3-blue.svg)](https://github.com/bcxdawn222/spec)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/bcxdawn222/spec)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**One workflow. Three hosts.** · [中文说明](README_cn.md)

</div>

---

## Why

AI-assisted spec-driven development has two established paradigms:

- **Fast flow**: start coding immediately, hooks as backstop — easy to drift
- **Heavy flow**: spec-first but rigid — OpenSpec's 4 commands, 9-step superpowers

**spec-workflow takes a third path**: keep the value of "think before you act", but split the flow into **12 independent commands** — every phase is re-entrant, interruptible, and redoable in isolation. Three hard-gate hooks make the flow **actually stop where it should**, and a Stop driver turns `/spec:loop` self-driving rounds into a hard mechanism.

### What makes it different

| Dimension | spec-workflow | OpenSpec | superpowers |
|---|---|---|---|
| Phase control | Explicit HARD GATE + hook interception | Fluid soft warnings | 9-step rigid flow |
| Pending decisions `[TBD]` | Allowed + hook-enforced clearing | Open Questions can linger | Forbidden |
| Command granularity | 12 independent commands | 4-command monolith | skill-based single flow |
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
claude plugin install spec@spec
# or local: claude --plugin-dir .
```

Then in a session:

```
/spec:workflow "add login + cart to the uni-app storefront"
```

### Codex CLI

```bash
codex plugin marketplace add bcxdawn222/spec
codex plugin install spec@spec
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

## The 12 Commands

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