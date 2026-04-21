"""审计日志（JSON）基础实现"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

LOG_FILE = Path(".logs/audit.jsonl")

def _now_iso() -> str:
    """返回 UTC ISO 时间字符串"""
    return datetime.now(timezone.utc).isoformat()

def _ensure_log_dir() -> None:
    """确保日志目录存在"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def log_event(
    event: str,
    thread_id: str,
    payload: dict,
    trace_id: str | None = None,
) -> dict:
    """写入一条审计事件到 JSONL"""
    _ensure_log_dir()

    record = {
        "id": str(uuid4()),
        "ts": _now_iso(),
        "event": event,
        "thread_id": thread_id,
        "trace_id": trace_id or str(uuid4()),
        "payload": payload,
    }

    # ensure_ascii=False 保证中文可读；一行一条便于流式读取。
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return record

def read_recent_events(limit: int = 20) -> list[dict]:
    """读取最近 N 条审计日志"""
    if not LOG_FILE.exists():
        return []
    
    lines = LOG_FILE.read_text(encoding="utf-8").splitlines()
    rows = lines[-limit:]
    return [json.loads(line) for line in rows if line.strip()]