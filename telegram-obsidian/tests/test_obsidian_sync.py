import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from obsidian_sync import ObsidianSync


class ObsidianSyncTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmpdir.name)
        (self.repo / ".git").mkdir()
        (self.repo / "Journal").mkdir()
        self.sync = ObsidianSync(repo_path=str(self.repo))

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_append_keeps_lock_file_unmodified(self):
        with patch.object(self.sync, "_run_git"):
            with patch.object(self.sync, "_has_staged_changes", return_value=False):
                self.sync.append_to_inbox("lock test")

        self.assertTrue(self.sync.lock_path.exists())
        self.assertEqual(self.sync.lock_path.read_text(encoding="utf-8"), "")

    def test_append_runs_git_pull_rebase_before_writing(self):
        commands = []

        def fake_run_git(args, check=False):
            commands.append(args)
            class Result:
                stdout = ""
                stderr = ""
                returncode = 0
            return Result()

        with patch.object(self.sync, "_run_git", side_effect=fake_run_git):
            with patch.object(self.sync, "_has_staged_changes", return_value=True):
                self.sync.append_to_inbox("hello")

        self.assertGreaterEqual(len(commands), 4)
        self.assertEqual(commands[0], ["pull", "--rebase", "origin", self.sync.git_branch])
        self.assertEqual(commands[1], ["add", "Journal/" + self.sync.tz_now().strftime("%Y-%m-%d") + ".md"])

    def test_push_failure_preserves_local_write_and_reports_status(self):
        def fake_run_git(args, check=False):
            cmd = tuple(args)
            if cmd[:2] == ("push", "origin"):
                raise RuntimeError("push failed")
            class Result:
                stdout = ""
                stderr = ""
                returncode = 0
            return Result()

        with patch.object(self.sync, "_run_git", side_effect=fake_run_git):
            with patch.object(self.sync, "_has_staged_changes", return_value=True):
                result = self.sync.append_to_inbox("hello push fail")

        self.assertTrue(result["local_write_success"])
        self.assertTrue(result["commit_success"])
        self.assertFalse(result["push_success"])
        self.assertIn("push failed", result["error"])
        content = (self.repo / result["path"]).read_text(encoding="utf-8")
        self.assertIn("hello push fail", content)

    def test_append_inserts_before_next_header(self):
        path = self.repo / "Journal/2026-06-05.md"
        path.write_text(
            "# 2026-06-05 周五\n\n## INBOX\n\n- [09:00] old\n\n## NEXT\n\nbody\n",
            encoding="utf-8",
        )

        with patch.object(self.sync, "_run_git") as run_git:
            with patch.object(self.sync, "_has_staged_changes", return_value=False):
                result = self.sync._append_locked(path, "Journal/2026-06-05.md", "new item", self.sync.tz_now().date())

        run_git.assert_called()
        content = result["full_content"]
        self.assertIn("## INBOX\n\n- [09:00] old\n\n- [", content)
        self.assertIn("## NEXT", content)
        self.assertLess(content.index("new item"), content.index("## NEXT"))

    def test_append_adds_inbox_if_missing(self):
        path = self.repo / "Journal/2026-06-05.md"
        path.write_text("# 2026-06-05 周五\n\n## Summary\n\nbody\n", encoding="utf-8")

        with patch.object(self.sync, "_run_git") as run_git:
            with patch.object(self.sync, "_has_staged_changes", return_value=False):
                result = self.sync._append_locked(path, "Journal/2026-06-05.md", "new item", self.sync.tz_now().date())

        run_git.assert_called()
        content = result["full_content"]
        self.assertIn("## INBOX", content)
        self.assertIn("new item", content)


if __name__ == "__main__":
    unittest.main()
