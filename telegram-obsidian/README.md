# telegram-obsidian

这是 AI Workflow 的第一部分。

它负责把 Telegram 中发来的文本，自动写入 Obsidian 仓库的 Journal 文件，并同步到该仓库对应的 GitHub 远程仓库。

## 当前能力

- 接收 Telegram 文本消息
- 仅允许指定用户使用
- 写入当日日记的 `## INBOX`
- 支持 `/today` 和 `/yesterday` 查询
- 自动 git add / commit / push
- 将处理结果返回到 Telegram

## 目录文件

- `bot.py`：Telegram Bot 主程序
- `obsidian_sync.py`：写入 Journal 与 Git 同步逻辑
- `.env.example`：环境变量模板
- `requirements.txt`：Python 依赖
- `service.sh`：macOS launchd 服务管理脚本
- `com.leon.telegram-obsidian-bot.plist`：macOS launchd 配置

## 依赖

- Python 3.10+
- git
- 一个可写的 Obsidian 内容仓库
- Telegram Bot Token

## 配置

复制配置模板：

```bash
cp .env.example .env
```

需要重点填写：
- `TELEGRAM_BOT_TOKEN`
- `ALLOWED_USERS`
- `OBSIDIAN_REPO_PATH`
- `TIMEZONE`

说明：
- `OBSIDIAN_REPO_PATH` 应指向你的 Obsidian 内容仓库本地路径
- 该内容仓库需要已经配置好 GitHub 远程仓库和 push 权限

## 本地运行

```bash
cd telegram-obsidian
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 bot.py
```

## macOS 后台运行

```bash
cd telegram-obsidian
./service.sh install
./service.sh status
./service.sh logs
```

## Linux 服务器部署建议

当前仓库内置的是 macOS 的 launchd 配置。
如果你要部署到 Linux 服务器，建议：

1. 克隆本仓库
2. 创建 Python 虚拟环境并安装依赖
3. 配置 `.env`
4. 另外使用 `systemd` 托管 `python3 bot.py`

建议的 systemd 启动命令为：

```bash
/usr/bin/env python3 /path/to/ai-workflow/telegram-obsidian/bot.py
```

工作目录建议设置为：

```bash
/path/to/ai-workflow/telegram-obsidian
```

## 迁移到新服务器时需要准备的内容

1. 本仓库代码
2. Obsidian 内容仓库代码
3. Telegram Bot Token
4. 允许访问的 Telegram 用户 ID
5. 目标机器的 Git push 权限

## 安全注意

- 不要把真实 `.env` 提交到 GitHub
- 不要把任何 Token、私钥、凭证写入仓库
- 建议先在新机器验证可运行，再删除旧机器本地目录
