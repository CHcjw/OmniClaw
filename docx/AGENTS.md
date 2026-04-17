# Omni Claw AI 开发指令（AGENTS.md）

## 项目概述

Omni Claw 是一个基于 **LangChain + LangGraph** 的 Agent Harness 项目，核心目标是复现并强化 OpenClaw 的工程精髓：

- 可循环编排的 Agent Loop（`agent -> tools -> agent`）
- 双阶段技能调用（`help -> run`）
- 可观测审计日志（JSONL 事件流）
- 记忆管理（长期画像 + 短期会话）
- 任务调度与心跳机制（支持常驻执行）

项目定位：

- 先做可用、可控、可追踪的 CLI Agent
- 再扩展 Web 控制台（shadcn/ui）

---

## 开发规范

### 1. 通用原则

- 优先实现 MVP 核心闭环，不做过早抽象
- 所有功能改动必须可追踪到 PRD/TECH_DESIGN 要求
- 新增模块必须可插拔，避免强耦合

### 2. 后端规范（Python）

- 使用 Python 3.11+
- 核心能力按模块分层：
  - `core/agent`（LangGraph 主循环）
  - `tools`（工具注册与执行）
  - `skills`（SKILL.md 加载与双阶段调用）
  - `tasks`（任务系统）
  - `runtime`（心跳/后台调度）
  - `obs`（日志审计）
  - `safety`（权限与沙箱）
- 禁止把业务逻辑写在 CLI 入口文件中
- 工具入参必须使用 schema 校验（Pydantic）

### 3. 前端规范（Next.js + shadcn/ui）

- 使用 Next.js App Router + TypeScript
- UI 组件优先使用 `shadcn/ui`
- 业务组件与 UI 基础组件分离：
  - `components/ui`：通用基础组件
  - `components/domain`：任务、日志、团队业务组件
- 数据请求统一通过 API 层封装，避免页面中散落请求逻辑

### 4. 安全规范（强约束）

- 文件访问必须限制在工作区内
- 高危命令默认禁止（例如破坏性删除、系统级操作）
- 涉及技能执行时必须先 `help` 再 `run`
- 任何绕过安全边界的实现都视为不合格

---

## 测试要求

### 1. 必测项

- Agent Loop：工具调用与回注流程正确
- 双阶段技能：未经过 `help` 不应直接高风险 `run`
- 任务系统：CRUD、状态流转、依赖处理正确
- 安全沙箱：路径逃逸与危险命令拦截有效
- 日志系统：关键事件按规范写入 JSONL

### 2. 测试层级

- 单元测试：核心函数/模块
- 集成测试：工具调度、任务调度、上下文压缩
- 回归测试：关键流程（需求 -> 改码 -> 测试 -> 汇报）

### 3. 交付前检查

- 后端：`pytest` 全通过
- 前端：lint/typecheck/build 通过
- 至少执行一次关键链路手动验收

---

## 代码风格

### 1. 命名规范

- Python 文件：`snake_case.py`
- 类名：`PascalCase`
- 函数/变量：`snake_case`
- 常量：`UPPER_SNAKE_CASE`
- TS 组件名：`PascalCase`
- TS 函数名：`camelCase`

### 2. 风格规范

- Python：PEP8 + 类型注解 + docstring
- TypeScript：严格类型，避免 `any`
- 日志字段统一：`ts`, `event`, `thread_id`, `payload`, `trace_id`
- 错误处理统一：用户可读信息 + 内部错误上下文

### 3. 提交规范

- 使用 Conventional Commits：`feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `chore:`
- 单次提交聚焦一个主题，避免混杂改动

---

## 注意事项

1. **先安全后能力**：任何新能力都必须先考虑权限边界与风险控制。
2. **先可观测后优化**：先把日志打全，再做性能优化。
3. **先状态外置后长对话**：任务与关键状态必须持久化，不依赖上下文“记住”。
4. **保持兼容目标**：技能机制与工程约定需兼容 `SKILL.md` / `AGENTS.md` / `CLAUDE.md`。
5. **避免过度设计**：MVP 阶段优先完成闭环，不提前引入复杂分布式架构。
6. **Web 与 CLI 一致性**：业务逻辑统一沉淀后端，前端只做展示与操作。
7. **变更需更新文档**：涉及架构、数据模型或流程变化时，必须同步更新 `docx/PRD.md` 与 `docx/TECH_DESIGN.md`。

---

## AI 执行优先级（给代理）

1. 先读需求与技术文档：`docx/OmniClaw-需求研究.md`、`docx/PRD.md`、`docx/TECH_DESIGN.md`
2. 优先完成 MVP 必做项
3. 修改代码时同时补齐测试
4. 完成后给出：变更清单、验证结果、剩余风险
