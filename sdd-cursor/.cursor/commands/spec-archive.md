---
description: 归档阶段。前置硬门：proposal 已批准（APPROVED 标记）+ 验证账本存在 + tasks 全部勾选。写 retrospect.md 复盘后移入 spec/archive/YYYY-MM-DD-<name>/。显式 force/abandoned 可放行（需记录原因）。
---

# /spec:archive

## 前置（先跑硬门，拦截即停）

```bash
python scripts/sdd.py archive-check
```

被拦截 → 按报错处理：无 APPROVED → 说明流程被绕过；无 verify.md → 先 /spec:verify；tasks 未勾完 → 完成或说明。

**显式放行**：确需归档但检查不过，用户明确说 `force`（按现状归档）或 `abandoned`（放弃此方向）→ 在 retrospect.md 记录原因后放行。

## 流程

1. 写 `spec/changes/<name>/retrospect.md`（≤40 行）：
   - 偏差审查："文档说 A，代码做 B"清单
   - verify 证据行
   - 未完成/延期项
   - force/abandoned 原因（若有）
2. 将整个 change 目录移入 `spec/archive/YYYY-MM-DD-<name>/`
3. 更新 `spec/knowledge.md`：沉淀跨 change 持久事实（`<事实> | 证据 | 日期 (change)`）；被证伪的旧事实**替换**而非并存；change 特有内容留在归档目录不搬
4. loop 运行的教训并入 knowledge.md

## 纪律

- 只归档，不删改代码
- 复盘要诚实：偏差、未完成项必须列出，不粉饰