# AI Workflow

这个仓库用于承载我的 AI 工作流项目。

当前第一部分：telegram-obsidian

功能概述：
- 通过 Telegram Bot 接收我的文本输入
- 自动写入 Obsidian 仓库的当日日记 INBOX
- 自动执行 git add / commit / push
- 将同步结果回传到 Telegram

项目结构：
- telegram-obsidian/：Telegram → Obsidian → GitHub 同步模块

设计原则：
- 程序仓库与内容仓库分离
- 本仓库只保存代码、配置模板、部署说明
- Obsidian 内容仓库独立维护，并使用其自己的 GitHub 远程仓库

部署思路：
1. 克隆本仓库
2. 配置 telegram-obsidian/.env
3. 在目标机器上准备 Obsidian 内容仓库
4. 安装 Python 依赖并启动 Bot

后续可扩展模块示例：
- ocean/
- agents/
- sync/
- deploy/
- docs/
