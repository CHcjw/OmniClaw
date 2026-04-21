# D:\code\program\OmniClaw\scripts\1_check.py
"""一 回归检查脚本。"""

from pathlib import Path
import sqlite3
import json


def check_db() -> None:
    db = Path("workspace/omniclaw.db")
    assert db.exists(), "数据库文件不存在: workspace/omniclaw.db"

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    tables = {
        row[0]
        for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }
    conn.close()

    required = {"sessions", "messages", "tasks", "audit_events"}
    missing = required - tables
    assert not missing, f"缺少数据表: {missing}"


def check_log() -> None:
    log_file = Path(".logs/audit.jsonl")
    assert log_file.exists(), "日志文件不存在: .logs/audit.jsonl"
    lines = [line for line in log_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert lines, "日志文件为空"
    json.loads(lines[-1])  # 至少最后一行是合法 JSON


def check_core_files() -> None:
    required_files = [
        "backend/app/main.py",
        "backend/app/core/config.py",
        "backend/app/core/logger.py",
        "backend/app/storage/sqlite.py",
        "backend/app/models/schemas.py",
    ]
    for f in required_files:
        assert Path(f).exists(), f"缺少文件: {f}"


if __name__ == "__main__":
    check_core_files()
    check_db()
    check_log()
    print("一：回归通过：核心文件、数据库、日志均正常。")
