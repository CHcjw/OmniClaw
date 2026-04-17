# Omni Claw 需求研究

## 目标
打造一个结合 **Claude Code 风格开发体验** 与 **OpenClaw 风格常驻助手能力** 的通用 Agent Harness 项目：
- 既能在终端中完成从需求到代码提交的开发任务
- 也能通过任务系统与心跳机制实现持续运行和主动执行
- 在多任务场景下具备团队协作与隔离执行能力（任务与工作区解耦）

## 调研发现
- **Claude Code** 强在终端内的高效开发闭环：读代码、改文件、跑测试、提交修复，强调“从描述到交付”。
- **Learn-Claude-Code** 提供了完整的 Harness 教学路径：从单循环到工具分发、任务系统、多代理协作、worktree 隔离，适合作为工程骨架参考。
- **OpenClaw** 强在“常驻型个人助理”能力：多通道接入、长期运行、主动触发（heartbeat/cron），适合作为产品化能力参考。
- **Kode 类产品** 强调多模型、多代理与工程化兼容（如 AGENTS.md/CLAUDE.md），说明生态兼容与可扩展是落地关键。

## 核心需求
1. **统一 Agent Loop 与工具调度**：支持 bash/read/write/edit 等基础能力，保证最小可用闭环。
2. **任务驱动执行系统**：支持任务创建、依赖关系、状态流转与持久化，任务可跨会话恢复。
3. **上下文治理**：支持上下文压缩与关键状态外置存储，避免长会话失控。
4. **子代理与团队协作**：支持子任务委派、消息收发、计划审批等协作机制。
5. **隔离执行通道**：支持任务与工作目录（worktree/独立工作区）绑定，避免并行改动冲突。
6. **常驻运行能力**：支持 heartbeat/定时任务，能主动检查与执行待办。
7. **安全与权限边界**：危险命令拦截、路径越权防护、可选审批机制。
8. **可观测性**：记录关键事件日志（输入、工具调用、结果、系统动作），便于排障与审计。
9. **生态兼容能力**：支持技能/规范兼容（如 SKILL.md、AGENTS.md/CLAUDE.md）以降低迁移成本。

## 参考产品
- Claude Code: https://www.anthropic.com/product/claude-code
- Claude Code Docs: https://docs.anthropic.com/en/docs/claude-code/overview
- OpenClaw: https://github.com/openclaw/openclaw
- Learn-Claude-Code: https://github.com/shareAI-lab/learn-claude-code
- Kode: https://github.com/shareAI-lab/Kode
