#!/usr/bin/env python3
"""Telegram → Obsidian Journal 同步机器人。

将发给 bot 的文本消息追加到本地 Obsidian 仓库 Journal/YYYY-MM-DD.md 的 ## INBOX 段落，
随后执行 git add / commit / push，并把结果回给 Telegram。
"""

from __future__ import annotations

import logging
import os
import sys
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import BotCommand, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from daily_ops import DailyOps
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
GOALS_OBSIDIAN_PATHS = [item.strip() for item in os.getenv("GOALS_OBSIDIAN_PATHS", "").split(",") if item.strip()]
AI_SESSION_ROOTS = [item.strip() for item in os.getenv("AI_SESSION_ROOTS", "").split(",") if item.strip()]
EVENING_PRE_REVIEW_TIME = os.getenv("EVENING_PRE_REVIEW_TIME", "18:00").strip() or "18:00"
EVENING_REVIEW_TIME = os.getenv("EVENING_REVIEW_TIME", "21:00").strip() or "21:00"
MORNING_BRIEF_TIME = os.getenv("MORNING_BRIEF_TIME", "05:00").strip() or "05:00"

ALLOWED_USERS_RAW = os.getenv("ALLOWED_USERS", "").strip()
ALLOWED_USERS = {
    int(uid.strip())
    for uid in ALLOWED_USERS_RAW.split(",")
    if uid.strip()
}

_sync = None
_daily_ops = None
_pending_pre_reviews: dict[int, str] = {}


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


def get_daily_ops() -> DailyOps:
    global _daily_ops
    if _daily_ops is None:
        _daily_ops = DailyOps(
            sync=get_sync(),
            goal_paths=GOALS_OBSIDIAN_PATHS,
            ai_session_roots=AI_SESSION_ROOTS,
        )
    return _daily_ops


def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USERS


async def configure_menu(application: Application) -> None:
    commands = [
        BotCommand("pre_review", "预复盘"),
        BotCommand("evening_review", "正式复盘"),
        BotCommand("morning_brief", "次晨简报"),
        BotCommand("organize_today", "整理今天"),
        BotCommand("today", "查看今天"),
        BotCommand("yesterday", "查看昨天"),
        BotCommand("help", "帮助"),
    ]
    await application.bot.set_my_commands(commands)


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
        "/pre_review - 立即生成 18:00 预复盘\n"
        "/evening_review - 立即生成 21:00 正式复盘\n"
        "/morning_brief - 立即生成次晨简报\n"
        "/organize_today - 整理今天页面\n"
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
        "/pre_review - 立即生成 18:00 预复盘\n"
        "/evening_review - 立即生成 21:00 正式复盘\n"
        "/morning_brief - 立即生成次晨简报\n"
        "/organize_today - 整理今天页面\n"
        "/help - 显示帮助\n\n"
        "💬 直接发文本给我，会自动写入今日日记的 ## INBOX，并保留当天固定 section。"
    )


async def pre_review_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        await update.message.reply_text("⛔ 你没有权限使用此机器人。")
        return

    daily_ops = get_daily_ops()
    result = daily_ops.build_pre_review()
    daily_ops.write_pre_review()
    if result.needs_input:
        _pending_pre_reviews[update.effective_user.id] = result.journal_path
    else:
        _pending_pre_reviews.pop(update.effective_user.id, None)
    await update.message.reply_text(result.message)


async def evening_review_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        await update.message.reply_text("⛔ 你没有权限使用此机器人。")
        return

    daily_ops = get_daily_ops()
    daily_ops.write_evening_review()
    result = daily_ops.build_evening_review()
    await update.message.reply_text(result.message)


async def morning_brief_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        await update.message.reply_text("⛔ 你没有权限使用此机器人。")
        return

    daily_ops = get_daily_ops()
    daily_ops.write_morning_brief()
    result = daily_ops.build_morning_brief()
    await update.message.reply_text(result.message)


async def organize_today_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update.effective_user.id):
        await update.message.reply_text("⛔ 你没有权限使用此机器人。")
        return

    await update.message.reply_text(
        "🧹 整理今天功能我会接着做成 AI 整理版。\n\n"
        "当前版本已经保留了固定 section，你可以先用预复盘 / 正式复盘把今天内容收起来。"
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
        result = get_sync().append_to_inbox(
            text,
            extra_section_headers=get_daily_ops().inbox_sections_for_capture(),
        )
    except Exception as e:
        logger.error("同步失败: %s", e, exc_info=True)
        await status_msg.edit_text(f"❌ 同步失败: {e}")
        return

    if user_id in _pending_pre_reviews:
        daily_ops = get_daily_ops()
        pre_review = daily_ops.build_pre_review()
        daily_ops.write_pre_review()
        if pre_review.needs_input:
            reply = "✅ 已收到这条补充，并继续整理时间记录。\n\n" + pre_review.message
        else:
            _pending_pre_reviews.pop(user_id, None)
            reply = "✅ 已收到你的补充，我已经继续完成预复盘整理。\n\n" + pre_review.message
    else:
        reply = format_result_message(result)
    await status_msg.edit_text(reply)


def format_result_message(result: dict) -> str:
    date_str = result["date"]
    status_text = "已创建" if result["action"] == "created" else "已追加"
    push_text = "成功" if result["push_success"] else "失败"
    commit_text = "成功" if result.get("commit_success") else "失败"
    local_text = "成功" if result.get("local_write_success") else "失败"

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
        "当天页面固定 section 已保留，可供晚间复盘和次晨简报继续整理。",
    ])
    return "\n".join(lines)[:4000]


def parse_schedule_time(value: str) -> time:
    hour_str, minute_str = value.split(":", 1)
    return time(
        hour=int(hour_str),
        minute=int(minute_str),
        tzinfo=ZoneInfo(TIMEZONE_NAME),
    )


async def scheduled_pre_review(context: ContextTypes.DEFAULT_TYPE):
    daily_ops = get_daily_ops()
    daily_ops.write_pre_review()
    result = daily_ops.build_pre_review()
    for user_id in sorted(ALLOWED_USERS):
        await context.bot.send_message(chat_id=user_id, text=result.message)


async def scheduled_evening_review(context: ContextTypes.DEFAULT_TYPE):
    daily_ops = get_daily_ops()
    daily_ops.write_evening_review()
    result = daily_ops.build_evening_review()
    for user_id in sorted(ALLOWED_USERS):
        await context.bot.send_message(chat_id=user_id, text=result.message)


async def scheduled_morning_brief(context: ContextTypes.DEFAULT_TYPE):
    daily_ops = get_daily_ops()
    daily_ops.write_morning_brief()
    result = daily_ops.build_morning_brief()
    for user_id in sorted(ALLOWED_USERS):
        await context.bot.send_message(chat_id=user_id, text=result.message)


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
    app.add_handler(CommandHandler("pre_review", pre_review_cmd))
    app.add_handler(CommandHandler("evening_review", evening_review_cmd))
    app.add_handler(CommandHandler("morning_brief", morning_brief_cmd))
    app.add_handler(CommandHandler("organize_today", organize_today_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    if app.job_queue is not None:
        app.job_queue.run_daily(scheduled_pre_review, time=parse_schedule_time(EVENING_PRE_REVIEW_TIME))
        app.job_queue.run_daily(scheduled_evening_review, time=parse_schedule_time(EVENING_REVIEW_TIME))
        app.job_queue.run_daily(scheduled_morning_brief, time=parse_schedule_time(MORNING_BRIEF_TIME))

    logger.info("🤖 Bot 启动中...")
    app.post_init = configure_menu
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
