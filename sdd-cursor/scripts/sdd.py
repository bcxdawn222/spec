#!/usr/bin/env python3
"""SDD 硬门 CLI（Cursor 版 spec-workflow 移植）。

用法:
  python sdd.py new <name>          # 初始化一个 change 工作区
  python sdd.py gate                # propose 前置检查（research 存在 + [TBD] 清空）
  python sdd.py apply-check         # apply 前置检查（proposal 四段齐全 + 单一 active change）
  python sdd.py archive-check       # 归档前置检查（APPROVED 标记 + verify 账本 + tasks 勾选）
  python sdd.py status              # 报告当前阶段
  python sdd.py ledger              # 展示当前 change 的验证账本

退出码: 0 = 通过, 2 = 拦截。命令文件必须在其流程入口先调用对应检查，
失败即停，不强制绕过。设计沿自 spec-workflow 的 check-gate/check-archive 硬门思路。
"""

import re
import sys
from datetime import datetime
from pathlib import Path

SECTIONS = ["## Why", "## What", "## How", "## Risk"]
SECTION_RE = re.compile(r"^## (Why|What|How|Risk)(?!\w)", re.M)  # 行首匹配，标题后不紧跟字母，防止 RiskX 蒙混
APPROVED_RE = re.compile(r"<!--\s*APPROVED:.*-->")
TBD_RE = re.compile(r"\[TBD\]")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPEC_DIR = PROJECT_ROOT / "spec"
CHANGES_DIR = SPEC_DIR / "changes"
ARCHIVE_DIR = SPEC_DIR / "archive"


def err(msg: str) -> None:
    print(f"[SDD-BLOCK] {msg}")


def active_changes() -> list[Path]:
    if not CHANGES_DIR.is_dir():
        return []
    return [d for d in sorted(CHANGES_DIR.iterdir()) if d.is_dir()]


def single_change() -> Path | None:
    changes = active_changes()
    if len(changes) == 0:
        err("没有 active change。先运行: python scripts/sdd.py new <name>（或按流程 /spec:research -> /spec:propose）")
        return None
    if len(changes) > 1:
        names = ", ".join(c.name for c in changes)
        err(f"检测到多个 active change（{names}）。流程假设单一 active change，先 /spec:archive 归档其余的。")
        return None
    return changes[0]


def has_open_tbd(text: str) -> bool:
    """只检查 ## Open 段落内的待决列表项（标题与注释里的 [TBD] 字样不算）。"""
    m = re.search(r"^## Open.*?(?=^## |\Z)", text, re.M | re.S)
    if not m:
        return False
    for line in m.group(0).splitlines():
        if line.startswith("## "):
            continue
        if TBD_RE.search(line):
            return True
    return False


def check_research(change: Path) -> bool:
    research = change / "research.md"
    if not research.exists():
        err("缺少 research.md，先运行 /spec:research")
        return False
    text = research.read_text(encoding="utf-8", errors="replace")
    if has_open_tbd(text):
        err("research.md 的 ## Open 段仍有 [TBD] 待决点。先运行 /spec:ask 消解，禁止带着未决点写方案。")
        return False
    return True


def check_proposal(change: Path) -> bool:
    proposal = change / "proposal.md"
    if not proposal.exists():
        err(f"{change.name} 缺少 proposal.md。先运行 /spec:propose")
        return False
    text = proposal.read_text(encoding="utf-8", errors="replace")
    found = {m.group(1) for m in SECTION_RE.finditer(text)}
    missing = [s.split()[1] for s in SECTIONS if s.split()[1] not in found]
    if missing:
        err(f"proposal.md 缺少段落: {', '.join('## ' + m for m in missing)}。先运行 /spec:revise 补全。")
        return False
    return True


def cmd_new(name: str) -> int:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
        err("change 名称只允许字母/数字/下划线/连字符。")
        return 2
    change = CHANGES_DIR / name
    if change.exists():
        err(f"{name} 已存在。")
        return 2
    change.mkdir(parents=True)
    tmpl = PROJECT_ROOT / "templates"
    for fname in ("research.md", "proposal.md", "tasks.md", "verify.md"):
        src = tmpl / fname
        if src.exists() and not (change / fname).exists():
            (change / fname).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"[SDD-OK] 已创建 change: spec/changes/{name}/")
    return 0


def cmd_gate() -> int:
    change = single_change()
    if change is None:
        return 2
    ok = check_research(change)
    if ok:
        print(f"[SDD-OK] gate 前置通过: research.md 完整且 [TBD] 已清空 ({change.name})")
    return 0 if ok else 2


def cmd_apply_check() -> int:
    change = single_change()
    if change is None:
        return 2
    ok = check_research(change) and check_proposal(change)
    if ok:
        print(f"[SDD-OK] apply 前置通过: research + proposal 四段齐全 ({change.name})")
        print("        （注意: APPROVED 标记由 /spec:apply 自动追加，此处不校验）")
    return 0 if ok else 2


def cmd_archive_check() -> int:
    change = single_change()
    if change is None:
        return 2
    ok = True
    if not check_proposal(change):
        ok = False
    text = (change / "proposal.md").read_text(encoding="utf-8", errors="replace")
    if not APPROVED_RE.search(text):
        err("proposal.md 无 APPROVED 标记：流程被绕过，归档被拒。确需归档请输入 force/abandoned（在 retrospect.md 记录原因）。")
        ok = False
    verify = change / "verify.md"
    if not verify.exists() or verify.stat().st_size == 0:
        err("缺少验证账本 verify.md：未验收就归档被拒。先运行 /spec:verify。")
        ok = False
    tasks = change / "tasks.md"
    if tasks.exists():
        ttext = tasks.read_text(encoding="utf-8", errors="replace")
        open_tasks = re.findall(r"- \[ \]", ttext)
        if open_tasks:
            err(f"tasks.md 仍有 {len(open_tasks)} 个未勾选任务。")
            ok = False
    if ok:
        print(f"[SDD-OK] 归档前置通过: proposal 已批准 + 验证账本存在 + 任务全部完成 ({change.name})")
    return 0 if ok else 2


def cmd_status() -> int:
    changes = active_changes()
    if not changes:
        print("[SDD] 无 active change。开始新任务: python scripts/sdd.py new <name>")
        return 0
    for change in changes:
        name = change.name
        stage = "research"
        if (change / "proposal.md").exists():
            stage = "propose（待 HARD GATE 审批）"
            ptext = (change / "proposal.md").read_text(encoding="utf-8", errors="replace")
            if APPROVED_RE.search(ptext):
                stage = "apply（已批准，实施中/待验证）"
                if (change / "verify.md").exists() and (change / "verify.md").stat().st_size:
                    stage = "verify/验收（账本已存在）"
        print(f"[SDD] {name}: {stage}   (spec/changes/{name}/)")
        for f in ("research.md", "design.md", "proposal.md", "tasks.md", "verify.md", "retrospect.md"):
            if (change / f).exists():
                print(f"      - {f}")
    return 0


def cmd_ledger() -> int:
    change = single_change()
    if change is None:
        return 2
    ledger = change / "verify.md"
    if not ledger.exists() or ledger.stat().st_size == 0:
        print(f"[SDD] {change.name} 尚无验证账本（首次写入发生在 propose 的 critique 轮或 apply 收尾）。")
        return 0
    print(ledger.read_text(encoding="utf-8", errors="replace"))
    return 0


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 0
    cmd = args[0]
    if cmd == "new":
        if len(args) < 2:
            err("用法: python sdd.py new <name>")
            return 2
        return cmd_new(args[1])
    if cmd == "gate":
        return cmd_gate()
    if cmd == "apply-check":
        return cmd_apply_check()
    if cmd == "archive-check":
        return cmd_archive_check()
    if cmd == "status":
        return cmd_status()
    if cmd == "ledger":
        return cmd_ledger()
    err(f"未知命令: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main())