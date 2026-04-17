# Omni Claw 技术设计（TECH_DESIGN）

## 技术栈选择
### 后端
- 语言：Python 3.11+
- Agent 框架：LangChain + LangGraph
- 模型接入：OpenAI / Anthropic / OpenAI Compatible（Provider 抽象层）
- API 框架：FastAPI（用于 Web 控制台数据接口）
- 配置管理：python-dotenv + pydantic-settings
- 异步与任务：asyncio（心跳、调度、后台执行）

### 终端层
- CLI：Typer
- 交互终端：prompt_toolkit
- 终端可视化：Rich（监控、状态、日志输出）

### 前端
- 框架：Next.js（App Router）+ TypeScript
- UI 体系：shadcn/ui（基于 Radix UI）+ Tailwind CSS
- 数据请求：TanStack Query
- 客户端状态：Zustand
- 表单与校验：React Hook Form + Zod
- 图表：Recharts（优先）/ ECharts（复杂图可选）
- 实时通道：SSE（MVP）/ WebSocket（V1+）

### 数据存储
- SQLite：会话 checkpoint、任务索引、事件索引
- JSONL：审计日志（事件流）
- Markdown：长期用户画像、技能说明（SKILL.md）
- 文件系统目录：`.tasks`、`.logs`、`.team`、`.worktrees`、`workspace/memory`

### 工程与部署
- 测试：pytest
- 代码质量：ruff + mypy（后端），ESLint + Prettier（前端）
- CI：GitHub Actions（lint/typecheck/test/build）
- 部署建议：
  - 本地单机（MVP）
  - Docker Compose（V1）

## 项目结构
```text
OmniClaw/
  docx/
    OmniClaw-需求研究.md
    PRD.md
    TECH_DESIGN.md

  backend/
    app/
      main.py                 # FastAPI 入口
      api/
        routes/
          tasks.py
          logs.py
          runtime.py
      core/
        agent.py              # LangGraph 装配与主循环
        provider.py           # 模型提供商抽象
        context.py            # 上下文裁剪与摘要
        heartbeat.py          # 心跳与调度
        logger.py             # JSONL 审计日志
      tools/
        builtins.py           # 内置工具
        sandbox_tools.py      # 文件/Shell 安全沙箱
        registry.py           # 工具注册与分发
      skills/
        loader.py             # SKILL.md 动态加载与 help/run 调用
      tasks/
        manager.py            # 任务 CRUD / 依赖图
      team/
        mailbox.py            # 协作消息机制（V1）
      worktree/
        manager.py            # worktree 绑定/执行/回收（V1）
      models/
        schemas.py            # Pydantic DTO
      storage/
        sqlite.py
        repositories/

  frontend/
    src/
      app/
        (dashboard)/
        tasks/
        timeline/
        security/
      components/
        ui/                   # shadcn/ui 组件
        domain/               # 业务组件（任务/日志/团队）
      lib/
        api/
        store/
        schema/
        utils/
      hooks/
      types/

  workspace/
    office/
    memory/
      user_profile.md

  .tasks/
  .logs/
  .team/
  .worktrees/
```

## 数据模型
### 1. Session（会话）
- id: string
- thread_id: string
- provider: string
- model: string
- summary: string
- created_at: datetime
- updated_at: datetime

### 2. Message（消息）
- id: string
- session_id: string
- role: 'system' | 'user' | 'assistant' | 'tool'
- content: text/json
- tool_name: string | null
- created_at: datetime

### 3. AuditEvent（审计事件）
- id: string
- ts: datetime
- thread_id: string
- event: 'llm_input' | 'tool_call' | 'tool_result' | 'ai_message' | 'system_action'
- payload: json
- trace_id: string

### 4. Task（任务）
- id: int
- subject: string
- description: string
- status: 'pending' | 'in_progress' | 'completed' | 'deleted'
- owner: string | null
- blocked_by: int[]
- worktree: string | null
- repeat: 'hourly' | 'daily' | 'weekly' | 'monthly' | null
- repeat_count: int | null
- target_time: datetime | null
- created_at: datetime
- updated_at: datetime

### 5. BackgroundJob（后台任务）
- id: string
- command: string
- status: 'running' | 'completed' | 'error'
- result: text
- started_at: datetime
- finished_at: datetime | null

### 6. SkillMetadata（技能元数据）
- name: string
- description: string
- path: string
- version: string | null
- loaded_at: datetime

### 7. UserProfile（长期画像）
- user_id: string（默认本地单用户）
- profile_markdown: text
- updated_at: datetime

### 8. TeamMessage（团队消息，V1）
- id: string
- from_agent: string
- to_agent: string
- type: 'message' | 'broadcast' | 'shutdown_request' | 'shutdown_response' | 'plan_approval_response'
- content: text
- request_id: string | null
- created_at: datetime

### 9. WorktreeBinding（工作区绑定，V1）
- name: string
- path: string
- branch: string
- task_id: int
- status: 'active' | 'kept' | 'removed'
- created_at: datetime
- updated_at: datetime

## 关键技术点
1. **LangGraph 主循环稳定性**
- 关键点：`agent -> tools -> agent` 的状态一致性
- 注意：工具异常不能导致整个会话崩溃，必须以 `tool_result(error)` 回注

2. **双阶段技能调用安全机制（help -> run）**
- 关键点：强制先读取 SKILL.md，再决定执行
- 注意：`run` 阶段命令必须经过沙箱验证与危险命令检查

3. **上下文治理与压缩策略**
- 关键点：长会话下防 token 膨胀
- 注意：保留系统消息、最近关键轮次、任务状态；旧对话摘要化并可追溯

4. **审计日志可追踪性**
- 关键点：统一事件模型与 trace_id
- 注意：日志字段稳定，便于后续检索、回放和问题定位

5. **任务依赖图一致性**
- 关键点：blocked_by 的有向无环约束（DAG）
- 注意：更新依赖时做环检测；任务完成时自动解除下游阻塞

6. **沙箱与路径安全**
- 关键点：所有路径必须限制在 workspace 内
- 注意：拒绝 `..`、绝对路径逃逸；限制危险 shell 指令；设置超时

7. **后台任务与心跳并发控制**
- 关键点：后台线程/协程与主循环并发访问状态
- 注意：使用锁或事务避免竞争条件；心跳触发需幂等

8. **CLI 与 Web 一致性**
- 关键点：同一业务逻辑服务于两种入口
- 注意：将逻辑收敛到后端 service 层，CLI/Web 仅作为适配层

9. **实时日志推送性能**
- 关键点：Web 端日志滚动展示
- 注意：优先 SSE，后续根据并发切 WebSocket；分页与窗口裁剪避免前端卡顿

10. **可扩展性（MCP/多模型/多代理）**
- 关键点：Provider、Tool、Skill、Runtime 采用可插拔设计
- 注意：接口先定义后实现，避免后期重构成本
