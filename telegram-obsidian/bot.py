#!/usr/bin/env python3
"""Telegram → Obsidian Journal 同步机器人。

将发给 bot 的文本消息追加到本地 Obsidian 仓库 Journal/YYYY-MM-DD.md 的 ## INBOX 段落，
随后执行 git add / commit / push，并把结果回给 Telegram。
"""

from __future__ import annotations

import logging
import os
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from obsidian_sync import ObsidianSync

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)
logger = logging.getLogger("tg-obsidian-bot")

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TIMEZONE_NAME = os.getenv("TIMEZONE", "Asia/Shanghai").strip() or "Asia/Shanghai"
OBSIDIAN_REPO_PATH = os.getenv("OBSIDIAN_REPO_PATH", "/Users/leon-home/leon-obsidian").strip()
JOURNAL_DIR = os.getenv("JOURNAL_DIR", "Journal").strip() or "Journal"
JOURNAL_FORMAT = os.getenv("JOURNAL_FORMAT", "%Y-%m-%d").strip() or "%Y-%m-%d"
INBOX_HEADER = os.getenv("INBOX_HEADER", "## INBOX").strip() or "## INBOX"
COMMIT_PREFIX = os.getenv("COMMIT_PREFIX", "telegram-journal").strip() or "telegram-journal"
GIT_BRANCH = os.getenv("GIT_BRANCH", "main").strip() or "main"

ALLOWED_USERS_RAW = os.getenv("ALLOWED_USERS", "").strip()
ALLOWED_USERS = {
    int(uid.strip())
    for uid in ALLOWED_USERS_RAW.split(",")
    if uid.strip()
}

_sync = None


def tz_now() -> datetime:
    return datetime.now(ZoneInfo(TIMEZONE_NAME))


def current_date_str() -> str:
    return tz_now().strftime("%Y-%m-%d")


def get_sync() -> ObsidianSync:
    global _sync
    if _sync is None:
        _sync = ObsidianSync(
            repo_path=OBSIDIAN_REPO_PATH,
            journal_dir=JOURNAL_DIR,
            journal_format=JOURNAL_FORMAT,
            inbox_header=INBOX_HEADER,
            timezone_name=TIMEZONE_NAME,
            commit_prefix=COMMIT_PREFIX,
            git_branch=GIT_BRANCH,
        )
    return _sync


def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USERS


def ensure_config() -> None:
    missing = []
    if not BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not ALLOWED_USERS:
        missing.append("ALLOWED_USERS")
    if missing:
        raise RuntimeError(f"缺少必要配置: {', '.join(missing)}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 你好 {user.first_name}！\n\n"
        "我是 Obsidian 日记同步机器人。\n"
        "发给我的文本会自动写入今日日记的 ## INBOX，并推送到 GitHub。\n\n"
        "命令:\n"
        "/today - 查看今天日记\n"
        "/yesterday - 查看昨天日记\n"
        "/help - 显示帮助"
    )


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        await update.message.reply_text("⛔ 你没有权限使用此机器人。")
        return

    sync = get_sync()
    content = sync.read_journal()
    today_str = current_date_str()
    if not content:
        await update.message.reply_text(f"📭 {today_str} 日记还没有内容")
        return

    preview = content[:3500]
    if len(content) > 3500:
        preview += f"\n\n... (还有 {len(content) - 3500} 字符)"
    await update.message.reply_text(f"📅 {today_str}\n\n{preview}")


async def yesterday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        await update.message.reply_text("⛔ 你没有权限使用此机器人。")
        return

    sync = get_sync()
    target_date = (tz_now() - timedelta(days=1)).date()
    content = sync.read_journal(target_date)
    target_str = target_date.strftime("%Y-%m-%d")
    if not content:
        await update.message.reply_text(f"📭 {target_str} 日记还没有内容")
        return

    preview = content[:3500]
    if len(content) > 3500:
        preview += f"\n\n... (还有 {len(content) - 3500} 字符)"
    await update.message.reply_text(f"📅 {target_str}\n\n{preview}")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 命令列表\n\n"
        "/today - 查看今天日记\n"
        "/yesterday - 查看昨天日记\n"
        "/help - 显示帮助\n\n"
        "💬 直接发文本给我，会自动写入今日日记的 ## INBOX。"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id if user else 0
    message = update.message

    if not message or not message.text:
        return

    if not is_allowed(user_id):
        logger.warning("未授权用户 %s (%s) 尝试使用 bot", user_id, user.first_name if user else "unknown")
        await message.reply_text("⛔ 你没有权限使用此机器人。")
        return

    text = message.text.strip()
    if not text:
        return

    logger.info("收到来自 %s (ID: %s): %s", user.first_name if user else "unknown", user_id, text[:100])
    status_msg = await message.reply_text("⏳ 正在写入 Obsidian 并推送 GitHub...")

    try:
        result = get_sync().append_to_inbox(text)
    except Exception as e:
        logger.error("同步失败: %s", e, exc_info=True)
        await status_msg.edit_text(f"❌ 同步失败: {e}")
        return

    reply = format_result_message(result)
    await status_msg.edit_text(reply)


def format_result_message(result: dict) -> str:
    date_str = result["date"]
    status_text = "已创建" if result["action"] == "created" else "已追加"
    push_text = "成功" if result["push_success"] else "失败"
    commit_text = "成功" if result.get("commit_success") else "失败"
    local_text = "成功" if result.get("local_write_success") else "失败"
    content = result["full_content"]
    if len(content) > 2800:
        content = content[:2800] + "\n... (截断)"

    lines = [
        f"✅ {status_text} {date_str} 日记",
        f"文件: {result['path']}",
        f"本地写入: {local_text}",
        f"Git commit: {commit_text}",
        f"GitHub push: {push_text}",
        f"Commit: {result.get('commit_message', '(无 commit)')}",
    ]
    if result.get("error"):
        lines.append(f"错误: {result['error']}")

    lines.extend([
        "",
        f"新增内容:\n{result['entry_text']}",
        "",
        f"当天日记内容:\n{content}",
    ])
    return "\n".join(lines)[:4000]


def main():
    try:
        ensure_config()
    except Exception as e:
        logger.error("❌ 配置错误: %s", e)
        sys.exit(1)

    sync = get_sync()
    try:
        sync.validate_environment()
    except Exception as e:
        logger.error("❌ 环境检查失败: %s", e)
        sys.exit(1)

    logger.info("仓库: %s | 日记目录: %s | 时区: %s | 分支: %s", OBSIDIAN_REPO_PATH, JOURNAL_DIR, TIMEZONE_NAME, GIT_BRANCH)
    logger.info("允许用户: %s", sorted(ALLOWED_USERS))

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("yesterday", yesterday))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🤖 Bot 启动中...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
