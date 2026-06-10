#!/usr/bin/env python3
"""Telegram Bot 模板。

使用:
1. 复制此文件到你的项目目录
2. 在 .env 中设置 TELEGRAM_BOT_TOKEN 和 ALLOWED_USERS
3. 运行: python3 bot.py
"""

import logging
import os
import sys

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ── 日志 ──────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)
logger = logging.getLogger("my-tg-bot")

# ── 配置 ──────────────────────────────────────────────────────
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_USERS = {
    int(uid.strip())
    for uid in os.getenv("ALLOWED_USERS", "").split(",")
    if uid.strip()
}


def is_allowed(user_id: int) -> bool:
    """检查用户是否在白名单中。未设置白名单则允许所有人。"""
    if not ALLOWED_USERS:
        return True
    return user_id in ALLOWED_USERS


# ── Handlers ──────────────────────────────────────────────────


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 你好 {user.first_name}！\n\n"
        "我是你的机器人。\n"
        "命令:\n"
        "/help - 显示帮助"
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 命令列表\n\n"
        "/help - 显示帮助\n\n"
        "💬 直接发消息给我即可。",
        parse_mode=ParseMode.MARKDOWN,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理收到的文本消息。"""
    user = update.effective_user
    message = update.message

    if not message or not message.text:
        return

    if not is_allowed(user.id if user else 0):
        logger.warning(f"未授权用户 {user.id if user else '?'} 尝试使用 bot")
        await message.reply_text("⛔ 你没有权限使用此机器人。")
        return

    text = message.text.strip()
    logger.info(f"收到消息: {text[:100]}")

    # TODO: 在这里添加你的业务逻辑
    await message.reply_text(f"收到: {text}")


# ── Main ──────────────────────────────────────────────────────


def main():
    if not BOT_TOKEN:
        logger.error("❌ 未设置 TELEGRAM_BOT_TOKEN，请检查 .env 文件")
        sys.exit(1)

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("🤖 Bot 启动中...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
