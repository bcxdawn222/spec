# SDD for Cursor（spec-workflow 移植版）

把 [kamioj/spec-workflow](https://github.com/kamioj/spec-workflow)（MIT）的 Spec-Driven Development 核心机制移植到 Cursor：
**发需求 → 自动调研出方案 → HARD GATE 审批 → 自动实施 → 独立验收 → 归档**，全程可重入、可硬约束、可派单。

## 核心机制（与原版对齐）

| 机制 | 实现 |
|---|---|
| 12 个阶段命令 | `.cursor/commands/spec-*.md`（workflow/loop/research/ask/design/propose/revise/apply/verify/status/chat/archive） |
| HARD GATE 硬门 | `scripts/sdd.py gate|apply-check|archive-check` 退出码 2 拦截，命令文档强制先跑 |
| 独立验收 | `.cursor/agents/spec-verifier.md` 子代理，fresh context，证据先行，写入验证账本 |
| 实施派单 | `.cursor/agents/spec-dev.md`，跨栈并发双派（frontend + backend） |
| 验证账本 | `spec/changes/<name>/verify.md`，稳定 V-N 编号 + 轮次对比 + 未修升级 |
| 反作弊 / Stuck / 编码宪章 | `AGENTS.md` + `.cursor/rules/sdd-core.mdc` + `references/code-charter.md` |
| 小程序/SaaS 栈规范 | `references/uniapp-miniprogram.md` 等（按需复制） |

## 安装（两步）

### 1. 复制到目标项目

```powershell
# 方案 A：一键安装到当前目录的项目（已 cd 到项目根）
.\sdd-cursor\install.ps1

# 方案 B：指定目标项目路径
.\sdd-cursor\install.ps1 -Target D:\projects\my-saas

# 方案 C：手动复制
# 把 .cursor/、AGENTS.md、scripts/、templates/、references/ 拷到项目根
```

### 2. 重启 Cursor（让命令/规则/子代理生效）

在项目里输入 `/spec` 即可看到命令列表。

## 使用

```text
/spec:workflow "做一个带登录的 uni-app 小程序商城"   ← 全流程托管（只停两个点：审批 + 验收）
/spec:loop "把支付模块的测试跑绿"                    ← 目标驱动自主循环
/spec:propose /spec:apply /spec:verify               ← 单步推进
python scripts/sdd.py status                         ← 看当前阶段
```

**激活边界**：流程只在你说"先写方案"或调用 `/spec:x` 时启动；小改动直接干，不走仪式。

## 硬门速查

```bash
python scripts/sdd.py new <name>       # 初始化 change（自动复制模板）
python scripts/sdd.py gate             # propose 前：research 存在 + [TBD] 清空
python scripts/sdd.py apply-check      # apply 前：proposal 四段齐全 + 单一 change
python scripts/sdd.py archive-check    # 归档前：APPROVED + verify 账本 + tasks 勾选
python scripts/sdd.py status | ledger  # 查看阶段 / 账本
```

退出码 2 = 拦截。归档可用 `force` / `abandoned` 显式放行（retrospect.md 记录原因）。

## 与原版的差异（Cursor 环境适配）

1. **无 UserPromptSubmit hook**：原版用 shell hook 硬拦截，Cursor 只能靠命令文档强制 + AGENTS.md 规则双保险。违规率低于纯提示词但非 0——收到拦截必须停下处理，不强制绕过
2. **无 --codex 异构双审**：Cursor 里可用任意子代理作为异构评审者替代（派一个非 spec-verifier 的 general-purpose 代理做第二层 review）
3. **命令行入口**：原版全部 slash 命令；这里硬门是 Python（跨平台），命令入口是 Cursor 命令

## 目录

```
sdd-cursor/
├── AGENTS.md                  # 核心规则（复制到项目根生效）
├── .cursor/
│   ├── rules/sdd-core.mdc     # HARD GATE 固定块 + 反作弊 + Stuck + 职责矩阵
│   ├── commands/spec-*.md     # 12 个阶段命令
│   └── agents/spec-dev.md, spec-verifier.md
├── scripts/sdd.py             # 硬门 CLI
├── templates/                 # research/proposal/tasks/verify 模板（new 时自动复制）
└── references/                # 编码宪章 / 栈规范 / 产物格式（自 spec-workflow 提炼，MIT）
```

License: MIT（机制移植自 kamioj/spec-workflow；references 内容为原仓库自有提炼，见各文件 frontmatter 的 source 声明）。