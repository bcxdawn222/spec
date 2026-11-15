"""运行生成一致性、钩子和网页视图检查，日志统一写入 logs。"""

import argparse
import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "logs"
HOOKS = ("check-tbd", "check-gate", "check-archive", "check-verify-reminder", "loop-driver")
SUITES = ("generated", "manifests", "claude", "codex", "views", "stdin")


def run_command(name: str, command: list[str], environment: dict[str, str]) -> None:
    log_path = LOGS / f"check-{name}.log"
    logging.info("开始 %s", name)
    with log_path.open("w", encoding="utf-8") as output:
        result = subprocess.run(
            command, cwd=ROOT, env=environment, stdout=output, stderr=subprocess.STDOUT,
        )
    lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    summary = [line for line in lines if line.startswith(("FAIL", "WARN", "INFO"))]
    print("\n".join(dict.fromkeys(summary + lines[-6:])))
    logging.info("%s 退出码 %s，日志 %s", name, result.returncode, log_path)
    if result.returncode:
        raise RuntimeError(f"{name} 检查失败，完整日志 {log_path}")


def check_stdin() -> None:
    """保持 stdin 打开，验证五个钩子收到一行 JSON 后可以结束。"""
    powershell = shutil.which("powershell.exe")
    if not powershell:
        raise RuntimeError("stdin 检查需要 Windows PowerShell")
    targets = [(hook, mode) for hook in HOOKS for mode in ("direct", "launcher")]
    with tempfile.TemporaryDirectory(prefix="spec-stdin-") as directory:
        for hook, mode in targets:
            event = "Stop" if hook in ("check-verify-reminder", "loop-driver") else "UserPromptSubmit"
            payload = json.dumps({
                "cwd": directory, "prompt": "hello", "hook_event_name": event,
                "stop_hook_active": False, "last_assistant_message": "done",
            }).encode("utf-8") + b"\n"
            hook_path = str(ROOT / "codex" / "hooks" / f"{hook}.ps1")
            entry = [hook_path]
            if mode == "launcher":
                entry.insert(0, str(ROOT / "codex" / "hooks" / "hook-launcher.ps1"))
            process = subprocess.Popen(
                [powershell, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-File", *entry],
                cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            if process.stdin is None or process.stdout is None or process.stderr is None:
                raise RuntimeError("无法创建钩子检查管道")
            process.stdin.write(payload)
            process.stdin.flush()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                raise RuntimeError(f"{hook} [{mode}] 仍在等待 stdin EOF") from None
            finally:
                process.stdin.close()
            stdout = process.stdout.read()
            stderr = process.stderr.read()
            process.stdout.close()
            process.stderr.close()
            if process.returncode or stdout or stderr:
                raise RuntimeError(f"{hook} [{mode}] 普通输入检查失败 {stdout!r} {stderr!r}")
            logging.info("PASS %s [%s] 单行输入结束，stdin 仍保持打开", hook, mode)
    print("PASS 5 个钩子的直接入口与 launcher，共 10 项 stdin 保持打开检查")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", choices=(*SUITES, "all"), default="all")
    arguments = parser.parse_args()
    LOGS.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(LOGS / f"manage-{arguments.suite}.log", encoding="utf-8")],
    )
    environment = os.environ.copy()
    shell = shutil.which("sh")
    if os.name == "nt":
        git = shutil.which("git")
        if git:
            git_root = Path(git).resolve().parents[1]
            candidate = git_root / "bin" / "bash.exe"
            if candidate.is_file():
                shell = str(candidate)
                environment["PATH"] = str(git_root / "usr" / "bin") + os.pathsep + environment["PATH"]
    platform_suites = SUITES if os.name == "nt" else SUITES[:-1]
    selected = platform_suites if arguments.suite == "all" else (arguments.suite,)
    for suite in selected:
        if suite == "generated":
            run_command(suite, ["node", "tools/generate.mjs", "--check"], environment)
        elif suite == "manifests":
            count = 0
            for path in (*ROOT.rglob("*.json"), *ROOT.rglob("*.json.template")):
                if ".git" not in path.parts:
                    json.loads(path.read_text(encoding="utf-8-sig"))
                    count += 1
            print(f"PASS {count} 个 JSON 文件解析")
            logging.info("PASS %s 个 JSON 文件解析", count)
        elif suite == "stdin":
            check_stdin()
        else:
            if not shell:
                raise RuntimeError(f"{suite} 检查需要 POSIX shell 或 Git Bash")
            script = {"claude": "hooks/run-fixtures.sh", "codex": "codex/hooks/run-fixtures.sh", "views": "tools/test-views.sh"}[suite]
            run_command(suite, [shell, script], environment)


if __name__ == "__main__":
    main()
