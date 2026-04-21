# Omni Claw

Omni Claw 是一个基于 LangChain + LangGraph 的可控 Agent Harness 项目。
当前阶段目标：先完成可运行骨架与 MVP 闭环能力。

## 1. 环境要求

- 操作系统：Windows / macOS / Linux
- Python：`>=3.11`（推荐使用 `uv` 管理）
- 包管理与运行：`uv`

## 2. 30分钟快速启动

### Step 1：进入项目目录

```powershell
cd D:\code\program\OmniClaw
```

### Step 2：安装 uv（若已安装可跳过）

参考官方文档安装：<https://docs.astral.sh/uv/>

Windows 常见方式：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 3：创建虚拟环境并安装依赖

```powershell
uv venv
uv sync
```

### Step 4：准备环境变量

```powershell
Copy-Item .env.example .env
```

然后按需编辑 `.env`：

- `DEFAULT_PROVIDER`（如 `aliyun` / `openai` / `anthropic`）
- `DEFAULT_MODEL`（如 `glm-5`）
- `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`
- `OPENAI_API_BASE`（若使用兼容网关）

### Step 5：验证 CLI

```powershell
uv run omniclaw --help
uv run omniclaw run
uv run omniclaw config
```

### Step 6：启动后端 API

```powershell
uv run uvicorn backend.app.main:app --reload
```

看到以下日志表示启动成功：

- `Uvicorn running on http://127.0.0.1:8000`
- `Application startup complete`

## 3. 启动后如何验证

浏览器或命令行访问：

- 健康检查：<http://127.0.0.1:8000/health>
- 运行时状态：<http://127.0.0.1:8000/runtime/status>
- FastAPI 文档（Swagger）：<http://127.0.0.1:8000/docs>
- ReDoc：<http://127.0.0.1:8000/redoc>

> 注意：`http://127.0.0.1:8000/` 返回 `{"detail":"Not Found"}` 是正常的，因为当前未定义根路由。

## 4. 查看数据库与日志

### SQLite 数据库

数据库文件：`workspace/omniclaw.db`

常用命令：

```powershell
uv run python -c "import sqlite3; c=sqlite3.connect('workspace/omniclaw.db'); cur=c.cursor(); print(cur.execute('SELECT name FROM sqlite_master WHERE type=''table'' ORDER BY name').fetchall()); c.close()"
```

### JSONL 审计日志

日志文件：`.logs/audit.jsonl`

```powershell
Get-Content .\.logs\audit.jsonl -Tail 20
```

## 5. 常见问题

### Q1：`ModuleNotFoundError: pydantic_core._pydantic_core`

- 原因：虚拟环境损坏或解释器/依赖不匹配。
- 处理：重新执行 `uv venv` + `uv sync`。

### Q2：`omniclaw` 命令找不到

- 先执行：

```powershell
uv sync
```

- 兜底运行：

```powershell
uv run python -m backend.app.cli --help
```

### Q3：`{"detail":"Not Found"}`

- 检查你访问的路径是否正确。
- 可直接访问 `/docs` 查看可用接口。

## 6. 当前项目结构（简版）

```text
OmniClaw/
  backend/app/         # 后端代码（FastAPI + Agent 核心）
  frontend/src/        # 前端代码（Next.js + shadcn/ui）
  workspace/           # 本地工作区与记忆
  .logs/               # 审计日志
  .tasks/              # 任务数据
  docx/                # 需求/PRD/技术设计/计划文档
```

## 7. 下一步开发顺序

按以下文档推进：

1. `docx/OmniClaw-开发计划.md`
2. `docx/PRD.md`
3. `docx/TECH_DESIGN.md`
4. `docx/AGENTS.md`
