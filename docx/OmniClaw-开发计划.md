# Omni Claw 项目开发计划

---

## 零： 总体目标（完整项目）

### 阶段 A（基础可运行）

- 完成后端/前端工程骨架
- CLI 可启动，API 可健康检查
- 数据库与日志目录可初始化

### 阶段 B（MVP 闭环）

- LangGraph 主循环（agent -> tools -> agent）
- 双阶段技能（help -> run）
- 任务系统 + 持久化 + 安全沙箱
- 审计日志 + monitor 监控

### 阶段 C（V1 核心增强）

- 心跳调度完善（重试/重复任务）
- Web 控制台首版（任务/日志/安全）
- CLI 与 Web 统一调用 service 层

### 阶段 D（V1+ 扩展）

- 子代理协作（team mailbox）
- worktree 绑定执行
- 多 provider 路由与策略切换

### 阶段 E（交付上线）

- 测试补齐、性能优化、文档封版
- 可演示、可复盘、可继续迭代

---

## 执行计划

## 一：工程基础与可运行骨架

### 1.1：工程初始化

- 目标：项目能安装依赖并启动基础命令
- 主要文件：`pyproject.toml`、`requirements.txt`、`backend/app/cli.py`
- 当天要敲：
  1. `omniclaw run/config/monitor/tasks` 空命令
  2. CLI 参数解析与帮助信息
- 学习点：Typer 命令组织方式
- 验收：`omniclaw --help` 可用

### 1.2：FastAPI 最小服务

- 目标：API 能跑起来
- 主要文件：`backend/app/main.py`、`backend/app/api/routes/runtime.py`
- 当天要敲：
  1. `/health` 健康检查
  2. `/runtime/status` 占位接口
- 学习点：FastAPI 路由与依赖注入
- 验收：`GET /health -> {status: ok}`

### 1.3：配置系统

- 目标：统一读取 `.env` 配置
- 主要文件：`backend/app/core/config.py`（新建）
- 当天要敲：
  1. Pydantic Settings
  2. provider/model/workspace 配置项
- 学习点：环境变量与类型安全配置
- 验收：CLI 能打印当前配置摘要

### 1.4：SQLite 基础层

- 目标：数据库连接与初始化
- 主要文件：`backend/app/storage/sqlite.py`
- 当天要敲：
  1. 初始化连接
  2. 建表（sessions/messages/tasks/audit_events）
- 学习点：aiosqlite 异步事务
- 验收：首次启动自动建库

### 1.5：数据模型(DTO)

- 目标：定义 Pydantic Schema
- 主要文件：`backend/app/models/schemas.py`
- 当天要敲：Session/Message/Task/AuditEvent DTO
- 学习点：输入输出模型分离
- 验收：接口层能做 schema 校验

### 1.6：日志基础

- 目标：JSONL 日志写入
- 主要文件：`backend/app/core/logger.py`
- 当天要敲：统一 `log_event()` 与 trace_id
- 学习点：可观测性最小闭环
- 验收：生成 `.logs/*.jsonl`

### 1.7：周验收

- 目标：整理第一周可运行版本
- 当天要敲：
  1. README 启动步骤
  2. Week1 回归测试脚本
- 验收：新环境 30 分钟内可跑通

---

## 二：MVP 核心能力

### 2.1：Provider 抽象层

- 文件：`backend/app/core/provider.py`
- 实现：统一 `generate(messages)` 接口，先接 1 个 provider
- 学习点：适配器模式

### 2.2：LangGraph 主循环

- 文件：`backend/app/core/agent.py`
- 实现：state + 条件路由 + tool 回注
- 学习点：StateGraph/ToolNode

### 2.3：内置工具

- 文件：`backend/app/tools/builtins.py`、`registry.py`
- 实现：`read_file/write_file/edit_file/bash`
- 学习点：工具协议与错误统一返回

### 2.4：安全沙箱

- 文件：`backend/app/tools/sandbox_tools.py`
- 实现：路径限制、危险命令拦截、超时
- 学习点：安全边界设计

### 2.5：技能双阶段

- 文件：`backend/app/skills/loader.py`
- 实现：`help -> run` 强约束
- 学习点：高风险行为前置解释

### 2.6：任务系统 MVP

- 文件：`backend/app/tasks/manager.py`、`api/routes/tasks.py`
- 实现：CRUD + 状态流转 + 持久化
- 学习点：任务状态机设计

### 2.7：周验收（MVP）

- 场景必须通过：
  1. 自然语言请求 -> 调工具改文件
  2. 技能必须先 help 再 run
  3. 危险命令被拦截并写日志

---

## 三：上下文治理与可观测

### 3.1：上下文裁剪

- 文件：`backend/app/core/context.py`
- 实现：系统消息保留 + 最近关键轮次保留

### 3.2：摘要入口

- 文件：`backend/app/core/context.py`
- 实现：超阈值自动触发摘要

### 3.3：长期记忆接入

- 文件：`workspace/memory/user_profile.md` 读取逻辑
- 实现：会话启动加载用户画像

### 3.4：心跳调度（基础）

- 文件：`backend/app/core/heartbeat.py`
- 实现：轮询到点任务并触发

### 3.5：监控命令

- 文件：`backend/app/cli.py`（或 monitor 模块）
- 实现：`omniclaw monitor` 实时打印关键事件

### 3.6：日志检索接口

- 文件：`backend/app/api/routes/logs.py`
- 实现：按 event/thread_id/time 查询

### 3.7：周验收（稳定性）

- 长会话 30+ 轮不崩溃
- 裁剪后任务仍可继续
- monitor 可回放关键链路

---

## 四：Web 控制台首版

### 4.1：前端初始化

- 目标：Next.js + TS + Tailwind + shadcn/ui
- 文件：`frontend/src/app/*`

### 4.2：任务页

- 文件：`frontend/src/app/tasks`、`components/domain`
- 实现：任务列表 + 创建 + 状态更新

### 4.3：日志时间线页

- 文件：`frontend/src/app/timeline`
- 实现：按事件类型筛选 + 详情抽屉

### 4.4：安全页

- 文件：`frontend/src/app/security`
- 实现：危险命令拦截记录展示

### 4.5：状态管理与请求层

- 文件：`frontend/src/lib/api`、`lib/store`、`lib/schema`
- 实现：TanStack Query + Zustand + Zod

### 4.6：联调

- 目标：前端操作能驱动后端任务/日志

### 4.7：周验收（CLI + Web 一致）

- 同一任务在 CLI 与 Web 展示一致
- 同一日志可在 monitor 与 Web 查询

---

## 五：V1 增强与交付

### 5.1：任务依赖与环检测

- 文件：`backend/app/tasks/manager.py`
- 实现：blocked_by DAG 校验

### 5.2：心跳调度增强

- 文件：`backend/app/core/heartbeat.py`
- 实现：重试策略 + 幂等触发

### 5.3：team mailbox（V1）

- 文件：`backend/app/team/mailbox.py`
- 实现：基础 message/broadcast

### 5.4：worktree manager（V1）

- 文件：`backend/app/worktree/manager.py`
- 实现：绑定/状态/回收占位实现

### 5.5：多 provider 扩展位

- 文件：`backend/app/core/provider.py`
- 实现：provider registry + 路由策略

### 5.6：测试与质量

- 后端：pytest + ruff + mypy
- 前端：eslint + typecheck + build

### 5.7：交付封版

- 更新：`docx/PRD.md`、`docx/TECH_DESIGN.md`、`docx/AGENTS.md`
- 产出：Demo 脚本 + 已知问题清单 + 下一阶段计划

---

## 六. 执行原则（避免走偏）

1. 每天只做一个主目标，不并行开太多坑。
2. 每个功能都要“先能跑，再优化”。
3. 先补最小测试，再扩功能。
4. 每天结束必须留可运行状态。
5. 文档与代码同步更新，不拖欠。

---

## 七. 建议命令清单（常用）

```bash
# 后端开发
python -m pytest
python -m uvicorn backend.app.main:app --reload
python -m backend.app.cli run

# 前端开发（后续）
npm install
npm run dev
npm run build

# 质量检查（后续接入）
ruff check .
mypy backend
```
