"""本地 Obsidian 仓库同步模块。"""

from __future__ import annotations

import fcntl
import logging
import subprocess
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


@dataclass
class GitResult:
    stdout: str
    stderr: str
    returncode: int


class ObsidianSync:
    def __init__(
        self,
        repo_path: str,
        journal_dir: str = "Journal",
        journal_format: str = "%Y-%m-%d",
        inbox_header: str = "## INBOX",
        timezone_name: str = "Asia/Shanghai",
        commit_prefix: str = "telegram-journal",
        git_branch: str = "main",
    ):
        self.repo_path = Path(repo_path).expanduser().resolve()
        self.journal_dir = journal_dir.strip("/")
        self.journal_format = journal_format
        self.inbox_header = inbox_header
        self.timezone = ZoneInfo(timezone_name)
        self.commit_prefix = commit_prefix
        self.git_branch = git_branch
        self.lock_path = self.repo_path / ".git" / "telegram-obsidian-bot.lock"

    def validate_environment(self) -> None:
        if not self.repo_path.exists():
            raise RuntimeError(f"仓库目录不存在: {self.repo_path}")
        if not (self.repo_path / ".git").exists():
            raise RuntimeError(f"不是 git 仓库: {self.repo_path}")
        journal_path = self.repo_path / self.journal_dir
        if not journal_path.exists():
            raise RuntimeError(f"Journal 目录不存在: {journal_path}")
        self._run_git(["status", "--short"], check=True)

    def tz_now(self) -> datetime:
        return datetime.now(self.timezone)

    def _journal_relpath(self, dt: Optional[date] = None) -> str:
        if dt is None:
            dt = self.tz_now().date()
        return f"{self.journal_dir}/{dt.strftime(self.journal_format)}.md"

    def _journal_abspath(self, dt: Optional[date] = None) -> Path:
        return self.repo_path / self._journal_relpath(dt)

    def read_journal(self, dt: Optional[date] = None) -> str:
        path = self._journal_abspath(dt)
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8")

    def append_to_inbox(
        self,
        text: str,
        dt: Optional[date] = None,
        extra_section_headers: Optional[list[str]] = None,
    ) -> dict:
        if dt is None:
            dt = self.tz_now().date()
        path = self._journal_abspath(dt)
        relpath = self._journal_relpath(dt)
        path.parent.mkdir(parents=True, exist_ok=True)

        self.lock_path.touch(exist_ok=True)
        with open(self.lock_path, "r+", encoding="utf-8") as lock_file:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            result = self._append_locked(path, relpath, text, dt, extra_section_headers)
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            return result

    def upsert_section(self, section_header: str, body: str, dt: Optional[date] = None) -> dict:
        if dt is None:
            dt = self.tz_now().date()
        path = self._journal_abspath(dt)
        relpath = self._journal_relpath(dt)
        path.parent.mkdir(parents=True, exist_ok=True)

        self.lock_path.touch(exist_ok=True)
        with open(self.lock_path, "r+", encoding="utf-8") as lock_file:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            result = self._upsert_section_locked(path, relpath, section_header, body, dt)
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            return result

    def get_section(self, section_header: str, dt: Optional[date] = None) -> Optional[str]:
        content = self.read_journal(dt)
        if not content:
            return None

        lines = content.splitlines()
        header_idx = self._find_section_index(lines, section_header)
        if header_idx is None:
            return None

        next_header_idx = self._find_next_section_index(lines, header_idx + 1)
        body_lines = lines[header_idx + 1 : next_header_idx if next_header_idx is not None else len(lines)]
        while body_lines and body_lines[0].strip() == "":
            body_lines.pop(0)
        while body_lines and body_lines[-1].strip() == "":
            body_lines.pop()
        return "\n".join(body_lines)

    def _append_locked(
        self,
        path: Path,
        relpath: str,
        text: str,
        dt: date,
        extra_section_headers: Optional[list[str]] = None,
    ) -> dict:
        timestamp = self.tz_now().strftime("%H:%M")
        entry_text = self._format_entry(text, timestamp)
        self._run_git(["pull", "--rebase", "origin", self.git_branch], check=True)

        if path.exists():
            original = path.read_text(encoding="utf-8")
            new_content = self._append_to_inbox_section(original, entry_text)
            action = "appended"
        else:
            weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][dt.weekday()]
            new_content = f"# {dt.strftime('%Y-%m-%d')} {weekday}\n\n{self.inbox_header}\n\n{entry_text}\n"
            action = "created"

        if extra_section_headers:
            new_content = self._ensure_sections(new_content, extra_section_headers)

        path.write_text(new_content, encoding="utf-8")

        result = {
            "success": True,
            "action": action,
            "path": relpath,
            "full_content": new_content,
            "entry_text": entry_text,
            "push_success": False,
            "commit_success": False,
            "local_write_success": True,
            "commit_message": "(未提交)",
            "date": dt.strftime("%Y-%m-%d"),
            "error": "",
        }

        self._run_git(["add", relpath], check=True)
        if not self._has_staged_changes(relpath):
            result["push_success"] = True
            result["commit_success"] = True
            result["commit_message"] = "(无变化，未提交)"
            return result

        commit_message = f"{self.commit_prefix}: append to {dt.strftime('%Y-%m-%d')}"
        self._run_git(["commit", "-m", commit_message], check=True)
        result["commit_success"] = True
        result["commit_message"] = commit_message

        try:
            self._run_git(["push", "origin", self.git_branch], check=True)
            result["push_success"] = True
        except Exception as exc:
            result["error"] = str(exc)
            logger.warning("git push 失败，已保留本地提交: %s", exc)

        return result

    def _upsert_section_locked(
        self,
        path: Path,
        relpath: str,
        section_header: str,
        body: str,
        dt: date,
    ) -> dict:
        self._run_git(["pull", "--rebase", "origin", self.git_branch], check=True)

        if path.exists():
            original = path.read_text(encoding="utf-8")
        else:
            weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][dt.weekday()]
            original = f"# {dt.strftime('%Y-%m-%d')} {weekday}\n\n{self.inbox_header}\n\n"

        new_content = self._upsert_section_content(original, section_header, body)
        path.write_text(new_content, encoding="utf-8")

        result = {
            "success": True,
            "action": "section_upserted",
            "path": relpath,
            "full_content": new_content,
            "entry_text": body,
            "push_success": False,
            "commit_success": False,
            "local_write_success": True,
            "commit_message": "(未提交)",
            "date": dt.strftime("%Y-%m-%d"),
            "error": "",
            "section_header": section_header,
        }

        self._run_git(["add", relpath], check=True)
        if not self._has_staged_changes(relpath):
            result["push_success"] = True
            result["commit_success"] = True
            result["commit_message"] = "(无变化，未提交)"
            return result

        commit_message = f"{self.commit_prefix}: update {section_header} for {dt.strftime('%Y-%m-%d')}"
        self._run_git(["commit", "-m", commit_message], check=True)
        result["commit_success"] = True
        result["commit_message"] = commit_message

        try:
            self._run_git(["push", "origin", self.git_branch], check=True)
            result["push_success"] = True
        except Exception as exc:
            result["error"] = str(exc)
            logger.warning("git push 失败，已保留本地提交: %s", exc)

        return result

    def _format_entry(self, text: str, timestamp: str) -> str:
        lines = [line.rstrip() for line in text.splitlines()]
        if len(lines) == 1:
            return f"- [{timestamp}] {lines[0]}"
        body = "\n".join(f"  {line}" if line else "  " for line in lines)
        return f"- [{timestamp}]\n{body}"

    def _append_to_inbox_section(self, content: str, entry_text: str) -> str:
        lines = content.splitlines()
        inbox_idx = self._find_section_index(lines, self.inbox_header)

        if inbox_idx is None:
            base = content.rstrip()
            if base:
                return f"{base}\n\n{self.inbox_header}\n\n{entry_text}\n"
            return f"{self.inbox_header}\n\n{entry_text}\n"

        next_header_idx = self._find_next_section_index(lines, inbox_idx + 1)

        before = lines[: inbox_idx + 1]
        inbox_body = lines[inbox_idx + 1 : next_header_idx if next_header_idx is not None else len(lines)]
        after = lines[next_header_idx:] if next_header_idx is not None else []

        while inbox_body and inbox_body[0].strip() == "":
            inbox_body.pop(0)
        while inbox_body and inbox_body[-1].strip() == "":
            inbox_body.pop()

        new_lines = before + [""]
        if inbox_body:
            new_lines += inbox_body + [""]
        new_lines += entry_text.splitlines()
        if after:
            new_lines += [""] + after

        return "\n".join(new_lines).rstrip() + "\n"

    def _upsert_section_content(self, content: str, section_header: str, body: str) -> str:
        lines = content.splitlines()
        header_idx = self._find_section_index(lines, section_header)

        body_lines = body.splitlines() if body else []

        if header_idx is None:
            base = content.rstrip()
            if base:
                new_lines = base.splitlines() + ["", section_header, ""]
            else:
                new_lines = [section_header, ""]
            new_lines.extend(body_lines)
            return "\n".join(new_lines).rstrip() + "\n"

        next_header_idx = self._find_next_section_index(lines, header_idx + 1)
        before = lines[: header_idx + 1]
        after = lines[next_header_idx:] if next_header_idx is not None else []

        new_lines = before + [""]
        new_lines.extend(body_lines)
        if after:
            new_lines += [""] + after
        return "\n".join(new_lines).rstrip() + "\n"

    def _ensure_sections(self, content: str, section_headers: list[str]) -> str:
        new_content = content
        for header in section_headers:
            lines = new_content.splitlines()
            if self._find_section_index(lines, header) is None:
                new_content = self._upsert_section_content(new_content, header, "")
        return new_content

    @staticmethod
    def _find_section_index(lines: list[str], section_header: str) -> Optional[int]:
        for i, line in enumerate(lines):
            if line.strip() == section_header:
                return i
        return None

    @staticmethod
    def _find_next_section_index(lines: list[str], start: int) -> Optional[int]:
        for i in range(start, len(lines)):
            if lines[i].startswith("## "):
                return i
        return None

    def _has_staged_changes(self, relpath: str) -> bool:
        result = self._run_git(["diff", "--cached", "--name-only", "--", relpath], check=True)
        return bool(result.stdout.strip())

    def _run_git(self, args: list[str], check: bool = False) -> GitResult:
        proc = subprocess.run(
            ["git", *args],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            timeout=60,
        )
        result = GitResult(proc.stdout, proc.stderr, proc.returncode)
        if check and proc.returncode != 0:
            msg = result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} 失败"
            raise RuntimeError(msg)
        return result
