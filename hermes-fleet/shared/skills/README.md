# Shared Skills

此目录存放跨机器共享的 skill 文件，由 fleet sync 部署到每台机器的 `~/.hermes/skills/` 全局目录。

## 工作原理

1. 把需要共享的 skill 目录放入此处（保持 `category/skill-name/SKILL.md` 结构）
2. 运行 `bash deploy/sync.sh <host>` 自动部署到目标机器
3. 所有 profile 都能使用这些 skill（因为是全局部署）

## 当前已收录的 skill

| Skill | 来源 | 用途 |
|-------|------|------|
| devops/git-firefly-bridge | MBP | 跨机器 Git 操作桥接 |
| note-taking/obsidian-cli | MBP | Obsidian CLI 操作 |
| note-taking/obsidian-workflows | mac-mini | Obsidian 工作流 |
| productivity/daily-review | MBP | 每日复盘 |
| productivity/file-organization | MBP | 文件整理 |
| productivity/poe-platform | MBP | Poe 平台操作 |
| productivity/feishu-document-api | mac-mini | 飞书文档 API |
| research/technical-research | MBP | 技术调研 |
| github/github-workflows | mac-mini | GitHub Actions 工作流 |
| media/music-generation-workflows | mac-mini | 音乐生成工作流 |
| social-media/telegram-bot-development | mac-mini | Telegram Bot 开发 |
| software-development/agent-memory-stack-debugging | mac-mini | Agent 记忆调试 |
| software-development/debugging-workflows | mac-mini | 调试工作流 |
| software-development/local-knowledge-capture | mac-mini | 本地知识捕获 |
| feishu-doc-finder | mac-mini | 飞书文档查找 |

## 添加新 skill

将 skill 目录复制到此，保持 `category/skill-name/` 结构：
```
shared/skills/
  category/
    skill-name/
      SKILL.md
      references/   (可选)
      templates/    (可选)
      scripts/      (可选)
```

然后提交并运行 sync。
