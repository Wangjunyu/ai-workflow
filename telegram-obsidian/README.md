# telegram-obsidian

这是 AI Workflow 的第一部分。

它负责把 Telegram 中发来的文本，自动写入 Obsidian 仓库的 Journal 文件，并同步到该仓库对应的 GitHub 远程仓库。

## 当前能力

- 接收 Telegram 文本消息
- 仅允许指定用户使用
- 写入当日日记的 `## INBOX`
- 支持 `/today` 和 `/yesterday` 查询
- 自动 git pull --rebase / add / commit / push
- 将处理结果返回到 Telegram
- 支持 macOS launchd 与 Linux systemd 两种常驻方式

## 目录文件

- `bot.py`：Telegram Bot 主程序
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

说明：
- `ALLOWED_USERS` 必填；未配置时 bot 不会启动
- `OBSIDIAN_REPO_PATH` 应指向你的 Obsidian 内容仓库本地路径
- 该内容仓库需要已经配置好 Git 远程仓库和 push 权限
- 如果多台机器同步同一个 Obsidian 仓库，`GIT_BRANCH` 应保持一致

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

## 部署方案 A / B

A 和 B 是两种常驻方案，只选一种运行。
不要同时启动两份 bot，否则同一个 Telegram token 会争抢 updates。

### 方案 A：macOS 用 launchd

适合：mac mini、MacBook、常开 macOS 机器。

这套仓库里已经带了 launchd 管理脚本：

```bash
cd /path/to/ai-workflow/telegram-obsidian
./service.sh install
./service.sh status
./service.sh logs
```

常用命令：

```bash
./service.sh restart
./service.sh uninstall
```

注意：
- `com.leon.telegram-obsidian-bot.plist` 里的路径现在仍是示例路径，部署前要改成你机器上的真实路径
- `service.sh` 会把 plist 安装到 `~/Library/LaunchAgents/`
- 日志默认在项目目录下 `logs/stdout.log` 和 `logs/stderr.log`

### 方案 B：Linux 用 systemd

适合：Linux 服务器、云主机、长期后台运行。

仓库里提供了两个层级：
1. 用户级 systemd：不需要 root，但要求当前环境有可用的 `systemctl --user`
2. 系统级 systemd：需要 root，适合服务器正式托管

#### B1. 用户级 systemd

先尝试：

```bash
cd /path/to/ai-workflow/telegram-obsidian
./install-systemd-user.sh install
```

查看状态和日志：

```bash
./install-systemd-user.sh status
./install-systemd-user.sh logs
```

卸载：

```bash
./install-systemd-user.sh remove
```

如果报错：

```text
Failed to connect to bus: No medium found
```

说明当前环境没有可用的 user systemd bus。这不是代码问题，直接改用下面的系统级方案 B2。

#### B2. 系统级 systemd

先检查并按需修改仓库里的服务文件：

- `WorkingDirectory=/path/to/ai-workflow/telegram-obsidian`
- `ExecStart=/path/to/ai-workflow/telegram-obsidian/.venv/bin/python /path/to/ai-workflow/telegram-obsidian/bot.py`
- `User=你的运行用户`

如果你的实际路径就是：
- 项目：`/home/leon/ai-workflow/telegram-obsidian`
- 用户：`leon`

那么仓库里的 `telegram-obsidian.service` 可以直接作为参考。

安装步骤：

```bash
sudo cp /path/to/ai-workflow/telegram-obsidian/telegram-obsidian.service /etc/systemd/system/telegram-obsidian.service
sudo systemctl daemon-reload
sudo systemctl enable telegram-obsidian.service
sudo systemctl restart telegram-obsidian.service
sudo systemctl status telegram-obsidian.service --no-pager
```

查看日志：

```bash
sudo journalctl -u telegram-obsidian.service -n 100 --no-pager
```

重启 / 停止：

```bash
sudo systemctl restart telegram-obsidian.service
sudo systemctl stop telegram-obsidian.service
```

如果服务启动失败，优先检查：
- `.env` 是否存在且配置完整
- `OBSIDIAN_REPO_PATH` 是否是当前机器的真实本地路径
- Obsidian 仓库是否已配置好 Git 远程和 push 权限
- `.venv` 是否已安装依赖

## git 同步行为

每次收到新消息后，bot 会按这个顺序执行：

1. `git pull --rebase origin <branch>`
2. 写入 `Journal/YYYY-MM-DD.md` 的 `## INBOX`
3. `git add`
4. `git commit`
5. `git push origin <branch>`

这样做的目的是尽量减少多机同时写同一个仓库时的推送冲突。

## push 失败时会发生什么

如果 push 失败：
- 本地写入仍然保留
- 本地 commit 仍然保留
- Telegram 回执会显示 `GitHub push: 失败`
- 错误信息会回给用户

这意味着内容通常没有丢，只是还没同步到远端。

你可以先在 Obsidian 仓库里检查：

```bash
cd /path/to/your/obsidian-repo
git status
git log --oneline -5
git push origin main
```

如果你使用的不是 `main`，把最后一行里的分支名改成你的 `GIT_BRANCH`。

## 迁移到新服务器时需要准备的内容

1. 本仓库代码
2. Obsidian 内容仓库代码
3. Telegram Bot Token
4. 允许访问的 Telegram 用户 ID
5. 目标机器的 Git push 权限
6. 新机器上的 `.env`
7. 选择 launchd 或 systemd 其中一种常驻方案

## 安全注意

- 不要把真实 `.env` 提交到 GitHub
- 不要把任何 Token、私钥、凭证写入仓库
- 不要同时运行两份使用同一 bot token 的实例
- 建议先在新机器验证可运行，再停掉旧机器实例
