"""项目回归检查脚本"""

from __future__ import annotations

import asyncio
import json
import sqlite3
import traceback
from pathlib import Path
from uuid import uuid4

from backend.app.core.logger import LOG_FILE, log_event, read_recent_events
from backend.app.storage.sqlite import init_db

DB_PATH = "workspace/omniclaw.db"


def check_core_files() -> None:
    """检查核心文件是否存在。"""
    required_files = [
        "backend/app/main.py",
        "backend/app/core/config.py",
        "backend/app/core/logger.py",
        "backend/app/storage/sqlite.py",
        "backend/app/models/schemas.py",
    ]
    for file_path in required_files:
        assert Path(file_path).exists(), f"缺少文件: {file_path}"


def check_db_exists_and_tables() -> None:
    """检查数据库文件与关键表是否存在，并打印查表结果。"""
    db = Path(DB_PATH)
    assert db.exists(), f"数据库文件不存在: {DB_PATH}"

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    tables = [
        row[0]
        for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    ]
    conn.close()

    print(f"  - 查表结果: {tables}")

    required = {"sessions", "messages", "tasks", "audit_events"}
    missing = required - set(tables)
    assert not missing, f"缺少数据表: {missing}"


def check_db_idempotent_init() -> None:
    """检查数据库初始化幂等性（重复执行不报错）。"""
    asyncio.run(init_db(DB_PATH))


def check_task_insert_and_query() -> None:
    """检查任务插入与查询行为是否正常。"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    task_subject = f"project-check-{uuid4().hex[:8]}"
    now = "2026-04-22T00:00:00+00:00"

    cur.execute(
        """
        INSERT INTO tasks (subject, description, status, owner, blocked_by, target_time, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (task_subject, "behavior test", "pending", "tester", "[]", None, now, now),
    )
    conn.commit()

    row = cur.execute(
        "SELECT subject, status, owner FROM tasks WHERE subject = ?",
        (task_subject,),
    ).fetchone()

    conn.close()

    assert row is not None, "任务插入后未查询到"
    assert row[0] == task_subject and row[1] == "pending", "任务字段不符合预期"


def check_log_write_and_read() -> None:
    """检查日志写入与读取行为是否正常。"""
    before = 0
    if LOG_FILE.exists():
        before = len([x for x in LOG_FILE.read_text(encoding="utf-8").splitlines() if x.strip()])

    event = log_event(
        event="system_action",
        thread_id="project-check-thread",
        payload={"step": "log_write_test"},
    )

    after = len([x for x in LOG_FILE.read_text(encoding="utf-8").splitlines() if x.strip()])
    assert after == before + 1, "日志写入后行数未增加"

    # 检查最后一条日志是否是合法 JSON 且字段完整。
    last_line = LOG_FILE.read_text(encoding="utf-8").splitlines()[-1]
    record = json.loads(last_line)
    for key in ("id", "ts", "event", "thread_id", "trace_id", "payload"):
        assert key in record, f"日志字段缺失: {key}"

    # 验证读取函数是否能读到刚写入的数据。
    recent = read_recent_events(1)
    assert recent and recent[-1]["id"] == event["id"], "read_recent_events 读取结果不符合预期"


def run_check(name: str, fn) -> tuple[bool, str]:
    """执行单项检查并返回结果。"""
    try:
        fn()
        print(f"[PASS] {name}")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] {name}: {exc}")
        return False, traceback.format_exc()


def main() -> None:
    """按顺序执行所有检查并输出可读报告。"""
    checks = [
        ("核心文件存在", check_core_files),
        ("数据库初始化幂等", check_db_idempotent_init),
        ("数据库与表结构", check_db_exists_and_tables),
        ("任务插入与查询", check_task_insert_and_query),
        ("日志写入与读取", check_log_write_and_read),
    ]

    print("=== 项目回归检查开始 ===")
    passed = 0
    failed_details: list[tuple[str, str]] = []

    for name, fn in checks:
        ok, detail = run_check(name, fn)
        if ok:
            passed += 1
        else:
            failed_details.append((name, detail))

    total = len(checks)
    print(f"\n=== 检查完成：{passed}/{total} 通过 ===")

    if failed_details:
        print("\n--- 失败详情 ---")
        for name, detail in failed_details:
            print(f"\n[{name}]\n{detail}")
        raise SystemExit(1)

    print("项目回归通过：存在性 + 行为性检查全部通过。")


if __name__ == "__main__":
    main()
