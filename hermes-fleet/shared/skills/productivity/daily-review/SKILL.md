---
name: daily-review
description: Review past Hermes sessions and write structured AI usage summaries to the Obsidian daily Journal note. Use when the user asks "what did I do yesterday/last week with AI" or "整理记录".
---

# Daily AI Usage Review

Review what the user did with Hermes across sessions and write a structured summary to the Obsidian daily Journal note.

## Trigger phrases
- "昨天/今天/这周用AI做了哪些事情"
- "整理记录" / "汇总一下"
- "帮我看一下之前的交流记录"

## Workflow

### 1. Find sessions

```bash
session_search("broad keyword")          # broad first
session_search("specific keyword")       # narrow down
```

Check both local AND Mac mini (`ssh mac-mini`), though most sessions are local.

Use multiple keyword queries to catch sessions that session_search might miss. Common keyword groups for this user: 妙记/下载/脚本/康康/布尔玛/tmux/SSH/NAS/Obsidian/笔记/同步/skill/飞书/Poe/Cursor.

### 2. Compile and check for gaps

Cross-reference: if a session summary from a broad query mentions topics not captured, do targeted queries for those topics.

### 2b. Check Feishu minutes for new recordings

When the user asks about a specific day's activity, also check if new 飞书妙记 (recordings) were created that day:

```bash
lark-cli --as user minutes +search --owner-ids me --start YYYY-MM-DD --page-size 20 --format json
```

Extract full tokens from `meta_data.app_link` (display tokens are truncated). Get details per token via:
```bash
lark-cli --as user api GET /open-apis/minutes/v1/minutes/{full_token}
```

⚠️ API response nests under `data.minute`, not `data` directly. Use `data.minute.title`, `data.minute.create_time`, `data.minute.duration`.

Present the recordings as a table with: title, time, duration. Ask the user if they want this added to the Journal.

### 3. Confirm location before writing

- Check if the Journal note for that date already exists (`Journal/YYYY-MM-DD.md`)
- Read existing content to find the right insertion point
- Propose the location and format, get user confirmation before writing

### 4. Write the summary

Format: concise bullet points — enough detail to understand what was done, not a full transcript. Each entry should include:

- **Title with status emoji** (✅ done, ⏳ in progress, ⚠️ blocked)
- **Bullet points**: key actions and outcomes, 3-5 bullets per item
- **Session ID**: `> 会话: \`session_id\`` for traceability
- **Recovery section**: at the bottom, show how to recover with `session_search`

### 5. Include recovery instructions

At the end of the summary, add:

```markdown
### 如何恢复这些对话
在 Hermes 中用 `session_search` 搜索关键词或直接查会话 ID：
\`\`\`
session_search("关键词")
\`\`\`
```

## Format: good vs bad

**Good** (concise but complete):
```
### 2. 手机 SSH 配置 + 录音文件盘点 ✅
- vivo V2436A（Android 16 + Termux）配好 SSH，密钥走 Bitwarden，别名 `vivo`
- Mac mini 上也配通了手机 SSH（通过 Bitwarden SSH Agent）
- 盘点了手机录音：17GB / 1099 个文件（通话 437、微信 163、腾讯会议 200 等）
- 尝试远程整理桌面 App 排序但被 Android 权限限制阻拦
> 会话: `20260603_045513_1777fc`
```

**Too verbose** (avoid): full narrative paragraphs, step-by-step replay, every command and output. The journal is for recall, not replay.

**Too terse** (avoid): one-liner with no detail. "Fixed Cursor file associations." — not actionable enough.

## Pitfalls

- Don't skip the "confirm location/format" step — the user wants to approve before you write
- Don't include every session — only those where real work was done; skip trivial 2-message sessions
- Don't guess the Journal path — always use the actual vault path from memory (`/Users/leon/Desktop/Leon-Obsidian/Leon/`)
- session_search may return sessions from adjacent days (e.g., late-night June 2 feels like June 3); include those if the user would consider them "yesterday's work"
- Voice input errors: "UC点" → "Obsidian", "欧币" → "Obsidian", "知书库" → "知识库" — apply phonetic correction
