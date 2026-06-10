---
name: telegram-bot-development
description: >
  Build Telegram bots with python-telegram-bot: message handling, commands,
  deployment as macOS launchd service. Use when the user wants to create,
  modify, or deploy a Telegram bot that processes messages or automates
  workflows.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [Telegram, Bot, Automation, Deployment, macOS, launchd]
    related_skills: [github-repo-management]
---

# Telegram Bot Development

Build and deploy Telegram bots using `python-telegram-bot`. Covers project
scaffolding, message handling, command registration, and macOS background
service setup with launchd.

## When to Use

- User wants to create a Telegram bot
- User wants to automate something via Telegram messages
- Deploy a bot as a background daemon on macOS

## Prerequisites

- Python 3.9+ (system Python on macOS is fine)
- `pip3 install python-telegram-bot python-dotenv`
  - If PyPI is blocked, use mirror: `pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple python-telegram-bot python-dotenv`
- Telegram Bot Token from [@BotFather](https://t.me/BotFather) (run `/newbot`)
- Your Telegram User ID from [@userinfobot](https://t.me/userinfobot)

## Project Structure

```
my-telegram-bot/
├── bot.py              # Main entry point
├── .env                # TELEGRAM_BOT_TOKEN, ALLOWED_USERS
├── .env.example        # Template for .env
├── requirements.txt    # python-telegram-bot, python-dotenv
├── service.sh          # launchd management script
└── com.example.mybot.plist  # launchd config
```

## Bot Template

See `templates/bot.py` for a starter template with:
- Environment-based config (.env)
- Command handlers (`/start`, `/help`)
- Message handler for plain text
- User allowlist
- Graceful error handling

## Commands Pattern

```python
from telegram.ext import Application, CommandHandler, MessageHandler, filters

async def start(update, context):
    await update.message.reply_text("Hello!")

async def handle_message(update, context):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
```

## macOS Deployment (launchd)

Use launchd for background auto-start on macOS. Create a `.plist` file:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.example.mybot</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/bot.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>/path/to/bot-dir</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/path/to/logs/stdout.log</string>

    <key>StandardErrorPath</key>
    <string>/path/to/logs/stderr.log</string>
</dict>
</plist>
```

Install and manage with a `service.sh` script (see `templates/service.sh`):

```bash
./service.sh install    # Install and start
./service.sh uninstall  # Stop and remove
./service.sh restart    # Restart
./service.sh status     # Check status
./service.sh logs       # View logs
```

## Pitfalls

1. **SSL issues with PyGithub**: On macOS with LibreSSL + GFW, `PyGithub` and
   `requests` may fail to reach `api.github.com`. Use `gh api` via subprocess
   instead — it uses macOS's native TLS stack which works fine. See
   `github-repo-management` skill for the pattern.

2. **pip install fails**: Use Tsinghua mirror:
   `pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple <package>`

3. **Homebrew Python not installed**: The system `/usr/bin/python3` works fine.
   Don't assume `/opt/homebrew/bin/python3` exists — check first.

4. **Telegram message length limit**: Messages are capped at 4096 characters.
   Always truncate long replies.

5. **launchd service name**: Use a reverse-domain label like
   `com.yourname.botname` to avoid conflicts.

6. **launchd PATH**: launchd doesn't inherit user PATH. Set `EnvironmentVariables`
   explicitly in the plist, especially for `gh` and other CLI tools.
