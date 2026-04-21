"""数据模型定义"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

# =========================
# Session
# =========================
class SessionBase(BaseModel):
    """会话基础字段"""

    thread_id: str = Field(..., description="线程ID")
    provider: str = Field(..., description="模型提供商")
    model: str = Field(..., description="模型名称")
    summary: str = Field(default="", description="会话摘要")


class SessionCreate(SessionBase):
    """创建会话时的输入模型"""

class SessionRead(SessionBase):
    """会话读取模型"""

    id: str
    created_at: datetime
    updated_at: datetime

# =========================
# Message
# =========================
MessageRole = Literal["system", "user", "assistant", "tool"]

class MessageBase(BaseModel):
    """消息基础字段"""

    session_id: str
    role: MessageRole
    content: str
    tool_name: str | None = None


class MessageCreate(MessageBase):
    """创建消息时的输入模型"""


class MessageRead(MessageBase):
    """消息读取模型"""

    id: str
    created_at: datetime

# =========================
# Task
# =========================
TaskStatus = Literal["pending", "in_progress", "completed", "deleted"]

class TaskBase(BaseModel):
    """任务基础字段"""

    subject: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    status: TaskStatus = "pending"
    owner: str | None = None
    blocked_by: list[int] = Field(default_factory=list)
    target_time: datetime | None = None


class TaskCreate(BaseModel):
    """创建任务输入模型"""

    subject: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    owner: str | None = None
    blocked_by: list[int] = Field(default_factory=list)
    target_time: datetime | None = None


class TaskUpdate(BaseModel):
    """更新任务输入模型（全字段可选）"""

    subject: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus | None = None
    owner: str | None = None
    blocked_by: list[int] | None = None
    target_time: datetime | None = None


class TaskRead(TaskBase):
    """任务读取模型"""

    id: int
    created_at: datetime
    updated_at: datetime

# =========================
# AuditEvent
# =========================
AuditEventType = Literal[
    "llm_input",
    "tool_call",
    "tool_result",
    "ai_message",
    "system_action",
]


class AuditEventBase(BaseModel):
    """审计事件基础字段"""

    thread_id: str
    event: AuditEventType
    payload: dict = Field(default_factory=dict)
    trace_id: str | None = None


class AuditEventCreate(AuditEventBase):
    """创建审计事件输入模型"""


class AuditEventRead(AuditEventBase):
    """审计事件读取模型"""

    id: str
    ts: datetime