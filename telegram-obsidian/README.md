# telegram-obsidian

这是 AI Workflow 的第一部分。

它负责把 Telegram 中发来的文本，自动写入 Obsidian 仓库的 Journal 文件，并同步到该仓库对应的 GitHub 远程仓库。

## 当前能力

- 接收 Telegram 文本消息
- 仅允许指定用户使用
- 写入当日日记的 `## INBOX`
- 自动补齐当天页面固定 section
- 支持 `/today` 和 `/yesterday` 查询
- 支持 `/pre_review`、`/evening_review`、`/morning_brief` 手动触发
- 支持 `18:00 / 21:00 / 05:00` 三次固定节奏推送
- 自动 git pull --rebase / add / commit / push
- 将处理结果返回到 Telegram
- 支持 macOS launchd 与 Linux systemd 两种常驻方式

## 目录文件

- `bot.py`：Telegram Bot 主程序
- `daily_ops.py`：日运营 MVA 逻辑
- `obsidian_sync.py`：写入 Journal 与 Git 同步逻辑
- `.env.example`：环境变量模板
- `requirements.txt`：Python 依赖
- `service.sh`：macOS launchd 服务管理脚本
- `com.leon.telegram-obsidian-bot.plist`：macOS launchd 配置模板
- `telegram-obsidian.service`：Linux systemd 服务文件模板
- `install-systemd-user.sh`：Linux 用户级 systemd 安装脚本

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
- `GIT_BRANCH`
- `GOALS_OBSIDIAN_PATHS`
- `AI_SESSION_ROOTS`

说明：
- `ALLOWED_USERS` 必填；未配置时 bot 不会启动
- `OBSIDIAN_REPO_PATH` 应指向你的 Obsidian 内容仓库本地路径
- 该内容仓库需要已经配置好 Git 远程仓库和 push 权限
- 如果多台机器同步同一个 Obsidian 仓库，`GIT_BRANCH` 应保持一致
- `GOALS_OBSIDIAN_PATHS` 用逗号分隔多个本地目标页路径
- `AI_SESSION_ROOTS` 用逗号分隔多个 AI session 根目录

## 本地运行

推荐用 `uv` 创建虚拟环境：

```bash
cd /path/to/ai-workflow/telegram-obsidian
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env
python bot.py
```

如果你更习惯标准 venv，也可以：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 bot.py
```

## 启动前自检

```bash
cd /path/to/ai-workflow/telegram-obsidian
source .venv/bin/activate
python - <<'PY'
from bot import ensure_config, get_sync
ensure_config()
get_sync().validate_environment()
print('SELF_CHECK_OK')
PY
```

如果输出 `SELF_CHECK_OK`，说明最基本的配置、仓库路径、Journal 目录、git 可用性都正常。

## 日运营 MVA

当前 MVA 的设计是：

1. 白天你发自然语言，先写进当天页面的 `## INBOX`
2. 系统自动保留当天固定 section
3. `18:00` 发送预复盘
4. `21:00` 发送正式复盘
5. `05:00` 发送次晨简报

第一版固定 section 包括：

- `## 今日概览`
- `## 业务推动`
- `## 目标对齐`
- `## 破冰行动进展`
- `## AI 活动摘要`
- `## 18:00 预复盘`
- `## 21:00 正式复盘`
- `## 明日动作草案`
- `## 05:00 次晨简报`
