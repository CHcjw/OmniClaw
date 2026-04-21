"""sqlite 数据库存储层"""

from __future__ import annotations
from pathlib import Path
import aiosqlite

def _ensure_parent_dir(db_path: Path) -> None:
    """确保数据库父目录存在"""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

async def init_db(db_path: str) -> None:
    """初始化数据库与基础表结构"""
    _ensure_parent_dir(db_path)

    async with aiosqlite.connect(db_path) as conn:
        # 开启外键约束
        await conn.execute("PRAGMA foreign_keys = ON")

        # 创建表
        await conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                thread_id TEXT NOT NULL,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                summary TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                tool_name TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                description TEXT DEFAULT '',
                status TEXT NOT NULL DEFAULT 'pending',
                owner TEXT,
                blocked_by TEXT DEFAULT '[]',
                target_time TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS audit_events (
                id TEXT PRIMARY KEY,
                ts TEXT NOT NULL,
                thread_id TEXT NOT NULL,
                event TEXT NOT NULL,
                payload TEXT NOT NULL,
                trace_id TEXT
            );
            """
        )

        await conn.commit()