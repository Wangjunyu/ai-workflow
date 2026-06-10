---
name: file-organization
description: >
  Organize cluttered directories (Desktop, Downloads, home, etc.) by grouping
  files into projects. Scan first, investigate purpose, present as annotated
  markdown, then execute. User drives decisions; agent does the legwork.
  Use when user says "桌面很乱" "帮我整理文件" "扫描一下" "看看有没有没用的".
---

# File Organization

## Workflow (mandatory order)

1. **SCAN** — List top-level items only. Use `ls -la` not recursive search.
   Also run `du -sh` on directories to identify space hogs.

2. **INVESTIGATE** — For each suspicious or large item, dig into what it IS:
   - Check config files (package.json, Cargo.toml, config.yaml, .git/config)
   - Check logs to see last active date
   - Check running processes (`ps aux | grep`) to see if still alive
   - Check README or identity files
   - Do NOT just list file sizes — the user wants to know PURPOSE, not just volume

3. **GROUP BY PROJECT** — Present findings clustered by project/use-case, NOT by
   file size or alphabet. A "项目" is a coherent activity: "PCC考试", "保险经纪",
   "C9.0学习组织", "AI工具链", "Babytree逆向", etc. If unsure of project boundaries,
   ask the user to correct your grouping.

4. **PRESENT AS MARKDOWN** — Write a structured markdown file to the Desktop (e.g.,
   `~/Desktop/文件整理-待标注.md`) with:
   - Each project as a section
   - Each file/folder as a table row with size
   - A `> ` block for the user to annotate decisions
   - Clear separation between "确定可删", "需要你决定", and "保留" categories
   - For each ambiguous item, include: what it is, evidence, judgment, and options

5. **WAIT** — Do NOT execute anything until the user has annotated the file and
   explicitly tells you to proceed.

6. **EXECUTE** — After user marks up the file, run all moves/deletes in batch.
   Use Python `shutil` via `execute_code` (not shell) when filenames contain `&`,
   `()`, Chinese characters, or other special characters that break shell parsing.

## Pitfalls

- The user uses voice input — names and terms may be misrecognized. Apply
  phonetic correction: "PC区"→"PCC", "ID文档"→"MD文档", "C九"→"C9.0",
  "一个千的"→"一起的". Echo corrections back to confirm.
- The user explicitly dislikes file-by-file analysis — always group by project.
- Never delete or move without the user's explicit annotation approval.
- When creating markdown files for annotation, put them on Desktop (user's
  preferred workspace for this workflow).
- The user may have both dirs and zips of the same project (duplicate storage).
  Flag these explicitly.
- Hidden dot-directories in `~` often contain active config — investigate before
  recommending deletion. Use `ps aux`, log timestamps, and config file analysis
  to determine if something is still in use.
- `brew list <pkg>` can time out (60s+). Don't block on it — check binary
  existence as a fallback.

## Example annotation block format

```markdown
## 3. C9.0 学习型组织

| 文件/文件夹 | 大小 | 备注 |
|---|---|---|
| 视频1：C公约讲解.mp4 | 678 MB | |
| C9.0 北京线下新生见面会 · 主持稿.docx | 31 KB | 下载目录 |

你的标注：
> 
```
