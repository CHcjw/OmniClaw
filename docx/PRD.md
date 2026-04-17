# Omni Claw 产品需求文档（PRD）

## 1. 产品概述

Omni Claw 是一个 **基于 LangChain + LangGraph** 的透明、可控、可扩展 Agent Harness 产品。

产品目标不是做“简单聊天机器人”，而是复用并升级 OpenClaw 的核心精髓：

- 用 **LangGraph StateGraph** 构建可循环、可编排的 Agent 主引擎
- 用 **双阶段技能调用（help -> run）** 降低高风险工具误用
- 用 **全链路审计日志 + 监控终端** 提升可观测与可追责能力
- 用 **记忆系统 + 心跳任务系统** 支持持续运行与长期协作

一句话定义：
**Omni Claw = LangGraph Agent Loop + Two-Phase Skill Safety + Observable Runtime + Persistent Task/Memory**

## 2. 目标用户

1. AI 应用开发者（核心用户）

- 需要一个可落地的 LangChain Agent 工程框架，而不只是 demo
- 希望快速迭代工具、技能、记忆、任务编排能力

2. 小型研发团队（2-10 人）

- 需要把复杂需求拆解给多个 Agent/任务并行处理
- 需要可审计、可回放、可定位问题的执行过程

3. Agent 工程学习者

- 想系统理解“从 Agent Loop 到生产级 Harness”的全过程
- 想学习 CyberClaw 的安全边界与可观测设计

## 3. 功能列表

### 3.1 LangChain 主引擎

1. LangGraph Agent Loop

- 基于 `StateGraph` 构建 `agent -> tools -> agent` 循环
- 使用条件路由（tool_use 时走 tools，否则结束）
- 统一消息状态管理（messages + summary）

2. 工具体系

- 内置工具：时间、计算、任务管理、文件操作、Shell 执行
- 动态技能工具：从 `SKILL.md` 自动加载
- 工具调用统一分发与标准化返回

### 3.2 CyberClaw 核心亮点（重点）

1. 双阶段技能调用（必备）

- `mode='help'`：先读技能说明书（SKILL.md）
- `mode='run'`：确认后执行命令
- 明确支持“反悔换工具”流程，降低误执行风险

2. 透明审计与监控

- 事件级日志：`llm_input/tool_call/tool_result/ai_message/system_action`
- JSONL 持久化日志（按 thread_id 归档）
- 监控终端实时展示工具调用与结果摘要

3. 记忆与上下文治理

- 长期记忆：用户画像（Markdown）
- 短期记忆：会话状态（SQLite checkpoint）
- 上下文裁剪 + 自动摘要，防止 token 膨胀

4. 心跳任务系统

- 后台轮询任务队列（定时触发）
- 支持 daily/weekly/monthly 循环任务
- 任务持久化，重启后可恢复

5. 安全沙箱

- 文件与命令仅允许在工作区内执行
- 路径越权拦截（`..`、绝对路径、主目录逃逸）
- 高危命令拦截 + 超时熔断 + 非交互执行规范

### 3.3 扩展能力

1. 子代理与团队协作（V1）

- 子任务隔离上下文执行
- 消息收发、计划审批、关停协议

2. worktree 隔离执行（V1）

- 任务绑定独立工作目录/分支
- 并行改动互不污染

3. Web 可视化控制台（V1 起步）

- 任务看板、执行轨迹、日志检索、团队状态
- CLI + Web 双入口，Web 用于管理与可视化

## 4. 功能优先级

### 4.1 必做（MVP）

1. LangGraph 主循环 + ToolNode 分发
2. 双阶段技能调用（help -> run）
3. 审计日志（5类事件）+ CLI 监控器
4. 上下文裁剪与摘要记忆
5. 任务系统（创建/查询/修改/删除 + 持久化）
6. 安全沙箱（路径拦截 + 危险命令拦截）

### 4.2 应做（V1）

1. 心跳后台调度完善（含循环任务与重试策略）
2. 子代理与团队协作协议
3. worktree 隔离执行与任务绑定
4. 审批机制（敏感工具执行前确认）
5. Web 控制台（基于 shadcn/ui 的首版）

### 4.3 后续添加（V2+）

1. 多模型路由（OpenAI/Anthropic/兼容 API/Ollama）
2. MCP 深度集成与插件市场能力
3. 企业级权限分层与多租户隔离
4. 工作流模板与行业场景预设

## 5. 界面设计

### 5.1 CLI 主界面（MVP）

1. 聊天交互区

- 用户输入
- Agent 输出（自然语言 + 工具执行回显）

2. 状态提示区

- 当前模式（normal/tool_calling/compacting）
- 当前模型与 provider
- 任务与后台状态

3. 命令入口

- `omniclaw run`：主交互
- `omniclaw config`：配置向导
- `omniclaw monitor`：实时监控日志

### 5.2 Web 界面（V1）

1. 设计基调

- 组件体系：`shadcn/ui` 为主
- 布局风格：左侧导航 + 顶部状态栏 + 主内容区
- 视觉方向：简洁工程化，强调信息密度与可读性

2. 页面结构

- 仪表盘：运行健康度、任务概览、异常告警
- 任务页：任务列表、依赖关系、状态流转
- 执行轨迹页：LLM 输入、工具调用、结果时间线
- 团队页：Agent 状态、消息记录、审批面板
- 安全页：命令拦截记录、审批记录、风险统计

3. 关键交互

- 任务状态拖拽/快捷更新
- 日志筛选（按事件类型、任务ID、时间范围）
- 工具调用详情抽屉（参数/结果/耗时）

## 6. 技术栈建议

### 6.1 后端（强约束）

- Python 3.11+
- LangChain / langchain-core
- LangGraph（StateGraph + ToolNode）
- pydantic（输入 schema 与数据校验）
- aiosqlite（会话与 checkpoint）
- python-dotenv（环境配置）

### 6.2 终端体验

- typer（CLI 命令）
- prompt_toolkit（交互输入）
- rich（监控与日志可视化）

### 6.3 前端（推荐组合：shadcn/ui + 其他）

1. 基础框架

- Next.js（App Router）
- TypeScript
- Tailwind CSS
- shadcn/ui（基于 Radix UI 的组件体系）

2. 状态与请求

- TanStack Query（服务端数据缓存与请求状态）
- Zustand（轻量客户端状态管理）

3. 表单与校验

- React Hook Form
- Zod

4. 可视化

- Recharts 或 ECharts（日志/任务统计图表）
- React Flow（可选，用于任务依赖图）

5. 数据通信

- REST API（MVP）
- WebSocket/SSE（V1，用于实时日志流）

### 6.4 工程质量

- pytest（单测/集成）
- ruff + mypy（风格/类型）
- ESLint + Prettier（前端规范）
- GitHub Actions（lint + test + build）

## 7. 代码风格和架构模式

### 7.1 代码风格

1. 全量类型注解 + docstring
2. 工具入参必须 schema 化（Pydantic）
3. 错误返回统一结构（用户可读 + 内部错误码）
4. 日志统一 JSONL，字段稳定：`ts/event/thread_id/payload`

### 7.2 架构模式（推荐）

1. 后端分层模块

- `core/agent.py`：LangGraph 引擎装配
- `core/tools/`：内置工具与沙箱工具
- `core/skill_loader.py`：动态技能加载
- `core/context.py`：上下文裁剪与摘要
- `core/heartbeat.py`：任务调度
- `core/logger.py`：审计日志
- `entry/cli.py`：命令入口与配置向导
- `entry/monitor.py`：日志监控终端

2. 前端分层模块（Web）

- `app/`：路由与页面骨架
- `components/ui/`：shadcn/ui 基础组件
- `components/domain/`：任务、日志、团队业务组件
- `lib/api/`：请求封装
- `lib/store/`：zustand store
- `lib/schema/`：zod schema

3. 设计原则

- Loop 稳定，机制插拔（tool/skill/task/monitor）
- 状态外置（任务、日志、记忆独立持久化）
- 安全优先（执行前理解，理解后执行）
- 前后端契约优先（统一 DTO/事件类型）

## 8. 限制条件和边界场景

### 8.1 限制条件

1. MVP 仅支持单机本地工作区
2. 默认工作区隔离，不支持任意系统目录访问
3. 高危命令默认禁用
4. 运行稳定性优先于执行速度

### 8.2 边界场景

1. 技能说明不完整或冲突

- 强制先 help；若无法确认安全则拒绝 run

2. 上下文过长

- 自动摘要并裁剪旧消息，只保留最近关键轮次

3. 工具卡死或超时

- 统一超时熔断并写入 system_action 日志

4. 任务循环依赖

- 创建/修改依赖时进行环检测，拒绝非法图

5. 并发改动冲突

- 推荐进入 worktree 模式执行并行任务

6. 日志爆量

- JSONL 分片归档 + 最近窗口监控

## 验收标准（建议）

1. 功能验收

- 能完成“需求 -> 改码 -> 测试 -> 汇报”完整闭环
- 双阶段技能调用在高风险场景可稳定触发

2. 安全验收

- 路径逃逸与危险命令拦截有效
- 审计日志可追溯到每一次工具调用

3. 稳定性验收

- 连续多轮对话不崩溃
- 上下文压缩后任务可继续推进

4. 性能/质量指标

- 在安全场景集上，双阶段调用较单阶段误执行率显著下降（目标：>50%下降）
- 关键路径单次响应可控（交互场景 <= 5-10s，视模型与工具而定）
