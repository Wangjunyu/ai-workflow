"""Daily ops helpers for the Telegram -> Obsidian workflow."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Iterable

from obsidian_sync import ObsidianSync


SECTION_OVERVIEW = "## 今日概览"
SECTION_BUSINESS = "## 业务推动"
SECTION_GOALS = "## 目标对齐"
SECTION_BREAKTHROUGH = "## 破冰行动进展"
SECTION_AI_ACTIVITY = "## AI 活动摘要"
SECTION_TIME_RECORDS = "## 时间记录草稿"
SECTION_PRE_REVIEW = "## 18:00 预复盘"
SECTION_EVENING_REVIEW = "## 21:00 正式复盘"
SECTION_NEXT_ACTIONS = "## 明日动作草案"
SECTION_MORNING_BRIEF = "## 05:00 次晨简报"

DEFAULT_DAILY_SECTIONS = [
    SECTION_OVERVIEW,
    SECTION_BUSINESS,
    SECTION_GOALS,
    SECTION_BREAKTHROUGH,
    SECTION_AI_ACTIVITY,
    SECTION_TIME_RECORDS,
    SECTION_PRE_REVIEW,
    SECTION_EVENING_REVIEW,
    SECTION_NEXT_ACTIONS,
    SECTION_MORNING_BRIEF,
]

TIME_RANGE_PATTERN = re.compile(r"(?P<start>\d{1,2}:\d{2})\s*[-~～到]\s*(?P<end>\d{1,2}:\d{2})")


@dataclass
class DailyOpsResult:
    message: str
    section_body: str
    journal_path: str
    missing_time_entries: tuple[str, ...] = ()

    @property
    def needs_input(self) -> bool:
        return bool(self.missing_time_entries)


class DailyOps:
    def __init__(
        self,
        sync: ObsidianSync,
        goal_paths: Iterable[str] | None = None,
        ai_session_roots: Iterable[str] | None = None,
    ):
        self.sync = sync
        self.goal_paths = [Path(p).expanduser() for p in (goal_paths or []) if p.strip()]
        self.ai_session_roots = [Path(p).expanduser() for p in (ai_session_roots or []) if p.strip()]

    def inbox_sections_for_capture(self) -> list[str]:
        return DEFAULT_DAILY_SECTIONS.copy()

    def build_pre_review(self, dt: date | None = None) -> DailyOpsResult:
        target_date = dt or self.sync.tz_now().date()
        inbox_entries = self._recent_inbox_entries(target_date, limit=None)
        inbox_preview = inbox_entries[-5:]
        goal_summary = self._goal_summary()
        ai_summary = self._ai_activity_summary(target_date)
        time_records, missing_entries = self._extract_time_records(inbox_entries)

        section_lines = [
            f"- 生成时间：{self.sync.tz_now().strftime('%H:%M')}",
            f"- 当前已记录输入：{len(inbox_entries)} 条",
            f"- 已提取时间记录：{len(time_records)} 条",
            f"- 待补时间记录：{len(missing_entries)} 条",
            "",
            "- 截至目前的时间记录：",
        ]
        if time_records:
            section_lines.extend(f"  - {entry}" for entry in time_records)
        else:
            section_lines.append("  - 暂未提取到明确时间段，请补充时间记录")
        section_lines.extend(["", "- 待补时间记录："])
        if missing_entries:
            section_lines.extend(f"  - {entry}" for entry in missing_entries)
        else:
            section_lines.append("  - 暂无待补项")
        section_lines.extend(["", "- 最近输入："])
        if inbox_preview:
            section_lines.extend(f"  - {entry}" for entry in inbox_preview)
        else:
            section_lines.append("  - 暂无白天输入")
        section_lines.extend(["", "- 当前目标背景："])
        if goal_summary:
            section_lines.extend(f"  - {line}" for line in goal_summary)
        else:
            section_lines.append("  - 暂未读取到目标页摘要")
        section_lines.extend(["", "- 当前 AI 活动："])
        if ai_summary:
            section_lines.extend(f"  - {line}" for line in ai_summary)
        else:
            section_lines.append("  - 暂未检测到当日 AI session 活动")
        section_lines.extend([
            "",
            "- 待你确认：",
            "  - 今天最重要的推进是什么？",
            "  - 破冰行动今天有没有真实推进？",
            "  - 21:00 前最需要收口的内容是什么？",
        ])
        section_body = "\n".join(section_lines)

        message_lines = [f"🕕 18:00 预复盘 | {target_date.strftime('%Y-%m-%d')}", ""]
        if missing_entries:
            message_lines.extend([
                "我已经先提取了截至目前的时间记录，但还有一些内容没法归进时间线。",
                "你把这些按 `09:30-10:10 做了什么` 这种格式补给我，我收到后会继续整理，不用你再点一次。",
                "",
                "待补的内容：",
            ])
            message_lines.extend(f"- {entry}" for entry in missing_entries[:5])
            if len(missing_entries) > 5:
                message_lines.append(f"- ... 还有 {len(missing_entries) - 5} 条")
            message_lines.extend(["", "目前已识别的时间记录："])
            if time_records:
                message_lines.extend(f"- {entry}" for entry in time_records[:6])
            else:
                message_lines.append("- 暂无明确时间段")
        else:
            message_lines.append("我先把今天截至目前的时间记录和素材收了一下。")
            if time_records:
                message_lines.extend(f"- {entry}" for entry in time_records[:6])
            elif inbox_preview:
                message_lines.extend(f"- {entry}" for entry in inbox_preview)
            else:
                message_lines.append("- 目前还没有白天输入")

        message_lines.extend([
            "",
            "我现在最想确认 3 件事：",
            "1. 今天最重要的推进是什么？",
            "2. 破冰行动今天有没有真实推进？",
            "3. 今晚 21:00 前最该收口的内容是什么？",
        ])
        message = "\n".join(message_lines)
        journal_path = self.sync._journal_relpath(target_date)
        return DailyOpsResult(
            message=message,
            section_body=section_body,
            journal_path=journal_path,
            missing_time_entries=tuple(missing_entries),
        )

    def build_evening_review(self, dt: date | None = None) -> DailyOpsResult:
        target_date = dt or self.sync.tz_now().date()
        inbox_preview = self._recent_inbox_entries(target_date, limit=8)

        section_lines = [
            f"- 生成时间：{self.sync.tz_now().strftime('%H:%M')}",
            "- 今日事实底稿：",
        ]
        if inbox_preview:
            section_lines.extend(f"  - {entry}" for entry in inbox_preview)
        else:
            section_lines.append("  - 暂无可复盘输入")
        section_lines.extend([
            "",
            "- 正式复盘问题：",
            "  - 今天真正推进了什么？",
            "  - 哪些事情只是忙，没有形成推进？",
            "  - 长期目标、短期目标和破冰行动分别推进到了哪里？",
            "  - 明天最重要的 1-3 个动作是什么？",
        ])
        section_body = "\n".join(section_lines)

        message = "\n".join([
            f"🌙 21:00 正式复盘 | {target_date.strftime('%Y-%m-%d')}",
            "",
            "我已经把今天的素材汇总好了。",
            "你可以直接回我自然语言，我来帮你整理进今天页面。",
            "",
            "我重点想和你收 4 件事：",
            "1. 今天真正推进了什么？",
            "2. 哪些事情只是忙？",
            "3. 破冰行动今天有没有实质动作？",
            "4. 明天最重要的 1-3 个动作是什么？",
        ])
        journal_path = self.sync._journal_relpath(target_date)
        return DailyOpsResult(message=message, section_body=section_body, journal_path=journal_path)

    def build_morning_brief(self, dt: date | None = None) -> DailyOpsResult:
        target_date = dt or self.sync.tz_now().date()
        yesterday = target_date - timedelta(days=1)
        carry_over = self.sync.get_section(SECTION_NEXT_ACTIONS, yesterday) or ""
        carry_lines = [line.strip("- ").strip() for line in carry_over.splitlines() if line.strip()]
        carry_lines = [line for line in carry_lines if not line.startswith("## ")]
        carry_lines = carry_lines[:5]

        section_lines = [
            f"- 生成时间：{self.sync.tz_now().strftime('%H:%M')}",
            f"- 基于昨天页面：{self.sync._journal_relpath(yesterday)}",
            "- 昨日延续动作：",
        ]
        if carry_lines:
            section_lines.extend(f"  - {line}" for line in carry_lines)
        else:
            section_lines.append("  - 昨晚还没有明确写出明日动作草案")
        section_lines.extend([
            "",
            "- 今日建议：",
            "  - 先做最贴近业务结果的一步",
            "  - 破冰行动优先安排在最清醒的时间段",
            "  - 中午前检查一次是否偏离重点",
        ])
        section_body = "\n".join(section_lines)

        message_lines = [
            f"🌅 05:00 次晨简报 | {target_date.strftime('%Y-%m-%d')}",
            "",
            f"我先基于昨天 {yesterday.strftime('%Y-%m-%d')} 的内容给你一个开场。",
        ]
        if carry_lines:
            message_lines.extend(f"- {line}" for line in carry_lines)
        else:
            message_lines.append("- 昨晚还没有明确写出今天动作草案")
        message_lines.extend([
            "",
            "今天建议你先抓 1 件最贴近业务结果的事，再看其他。",
        ])
        message = "\n".join(message_lines)
        journal_path = self.sync._journal_relpath(target_date)
        return DailyOpsResult(message=message, section_body=section_body, journal_path=journal_path)

    def write_pre_review(self, dt: date | None = None) -> dict:
        result = self.build_pre_review(dt)
        return self.sync.upsert_section(SECTION_PRE_REVIEW, result.section_body, dt)

    def write_evening_review(self, dt: date | None = None) -> dict:
        result = self.build_evening_review(dt)
        return self.sync.upsert_section(SECTION_EVENING_REVIEW, result.section_body, dt)

    def write_morning_brief(self, dt: date | None = None) -> dict:
        result = self.build_morning_brief(dt)
        return self.sync.upsert_section(SECTION_MORNING_BRIEF, result.section_body, dt)

    def _recent_inbox_entries(self, dt: date, limit: int | None = 5) -> list[str]:
        section = self.sync.get_section(self.sync.inbox_header, dt) or ""
        entries = []
        for line in section.splitlines():
            stripped = line.strip()
            if stripped.startswith("- "):
                entries.append(stripped[2:])
        if limit is None:
            return entries
        return entries[-limit:]

    def _extract_time_records(self, inbox_entries: list[str]) -> tuple[list[str], list[str]]:
        time_records: list[str] = []
        missing_entries: list[str] = []
        for entry in inbox_entries:
            text = entry.strip()
            if not text:
                continue
            range_match = TIME_RANGE_PATTERN.search(text)
            if range_match:
                start = range_match.group("start")
                end = range_match.group("end")
                cleaned = text.replace(range_match.group(0), "").strip(" -:：")
                if cleaned.startswith("]"):
                    cleaned = cleaned[1:].strip()
                time_records.append(f"{start}-{end} {cleaned}".strip())
                continue

            if text.startswith("[") and "]" in text:
                timestamp, rest = text.split("]", 1)
                timestamp = timestamp.lstrip("[")
                rest = rest.strip()
                time_records.append(f"{timestamp} 记录：{rest}（待补时长/分类）")
                missing_entries.append(f"[{timestamp}] {rest}")
                continue

            missing_entries.append(text)
        return time_records, missing_entries

    def _goal_summary(self, max_lines: int = 6) -> list[str]:
        lines: list[str] = []
        for path in self.goal_paths:
            if not path.exists():
                continue
            title = path.stem
            lines.append(f"{title}")
            try:
                content = path.read_text(encoding="utf-8")
            except Exception:
                continue
            for raw in content.splitlines():
                text = raw.strip().lstrip("- ").strip()
                if not text or text.startswith("---") or text.startswith("feishu_url:"):
                    continue
                if text.startswith("#"):
                    continue
                lines.append(text[:120])
                if len(lines) >= max_lines:
                    return lines[:max_lines]
        return lines[:max_lines]

    def _ai_activity_summary(self, dt: date) -> list[str]:
        start = datetime.combine(dt, time.min, tzinfo=self.sync.timezone)
        lines: list[str] = []
        for root in self.ai_session_roots:
            if not root.exists():
                continue
            recent: list[Path] = []
            try:
                for path in root.rglob("*"):
                    if not path.is_file():
                        continue
                    modified = datetime.fromtimestamp(path.stat().st_mtime, tz=self.sync.timezone)
                    if modified >= start:
                        recent.append(path)
            except Exception:
                continue

            if not recent:
                continue
            recent.sort(key=lambda item: item.stat().st_mtime, reverse=True)
            sample = ", ".join(item.name for item in recent[:3])
            lines.append(f"{root}: {len(recent)} 个更新，最近有 {sample}")
        return lines
