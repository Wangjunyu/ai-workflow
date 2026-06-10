# Feishu Minutes End-to-End Workflow

When 浚宇 says "推送妙记" or "刚才和康康的交流有妙记记录":

## Step 1: Auth check
```bash
lark-cli config bind --source hermes --identity user-default  # if not bound
```
User auth should already have: `minutes:minutes.basic:read`, `minutes:minutes.transcript:export`, `wiki:*` (for archive step).
If expired, re-auth with QR flow: `lark-cli auth login --domain minutes --no-wait --json` → QR → `--device-code`.

## Step 2: Download transcript
```bash
# Get minutes info
lark-cli minutes minutes get --params '{"minute_token":"<token>"}' --as user

# Download transcript (saves to /private/tmp/download.txt)
lark-cli api GET "/open-apis/minutes/v1/minutes/<token>/transcript" --as user
```

## Step 3: Upload transcript to Drive (fallback when file push blocked)
```python
# POST /open-apis/drive/v1/files/upload_all (tenant token)
# Returns file URL like https://rcnsiaef7x5y.feishu.cn/file/A6Wf...
```
Use `%s` formatting and `dict()` — never `{variable}` patterns (Hermes template-injection bug).

## Step 4: Write meeting summary as docx
**Option A: Create via tenant token (bot) then share URL** — bot can create+write docx independently.
**Option B: Create directly in wiki node (user)** — `lark-cli wiki +node-create --as user --parent-node-token <...>` then write with user token (needs `docx:document` scope).

```python
# Create docx:
# POST /open-apis/docx/v1/documents → document_id
# Write blocks (2=text, 5=heading3):
# POST .../blocks/{doc_id}/children → append content blocks
```

## Step 5: Push to 康康陪跑群 (3 messages)
1. **妙记链接**: `send_message(target="feishu:康康陪跑-6.4-9.3", message="🔗 <minutes_url>")`
2. **原文文件**: `send_message` with Drive URL from Step 3
3. **会议总结**: `send_message` with docx URL from Step 4 + inline summary

## Step 6: Archive to wiki (under 会议记录 node)
**Cross-ownership trap:** Docx created by bot can't be moved by user, and vice versa. If docx was created by bot, don't try to `wiki +move` it — share the URL or add a comment on 康康交付清单 instead.

**Recommended approach:** Create docx via `wiki +node-create --as user` directly in the wiki tree, then write content. This keeps ownership unified.

If wiki move fails (131006), fall back:
```bash
lark-cli drive +add-comment --as bot --doc "NyPZdDNryoyzWhxjxPzcYhaSnec" --type docx --full-comment \
  --content '[{"type":"text","text":"📝 <title>: <drive_or_docx_url>"}]'
```

## Key Tokens (persistent)

| Resource | Token |
|----------|-------|
| 康康交付清单 wiki node | PLC2wV49MiR9Nnkoc00clIUanG5 |
| 康康交付清单 docx obj | NyPZdDNryoyzWhxjxPzcYhaSnec |
| 会议记录 wiki node | D9dLwrEP2iX8NfkcwEgcIFebnDe |
| 康康陪跑群 chat_id | oc_227dda7fd76cf0004921a079e09d1823 |
| 康康陪跑群 target | feishu:康康陪跑-6.4-9.3 |
| Wiki space ID | 7636684753655319743 |

## Pitfalls

### CRITICAL: NEVER mention technical details in the group
The 康康陪跑群 is client-facing. Messages must only contain results — no API errors, permission issues, auth workflows, or file upload problems. Technical issues stay in DM with 浚宇.

### CRITICAL: Don't summarize before reading the transcript
康康 wants summary based on actual transcript content, not fabricated. Read the full transcript before summarizing.

### CRITICAL: Use heredoc for Python with curly braces
`write_file` and terminal `-c` both mangle f-strings containing curly braces due to Hermes template-injection. Always use heredoc with single-quoted delimiter:
```bash
python3 << 'PYEOF'
# code with {curly_braces} here - safe
PYEOF
```

### Transcript API path
The transcript endpoint is `/open-apis/minutes/v1/minutes/{token}/transcript` (NOT `/open-apis/vc/v1/...`). Tenant token returns 404; user token works.

### Drive upload needs multipart form
`curl -F` for multipart. parent_type=explorer, parent_node= (empty = root).

### Message file attach blocked
Bot lacks `im:resource:upload` scope (rejected by Feishu). User auth also rejected this scope. Workaround: Drive upload → share link in text message.

### Wiki node children not enumerable via API
When searching for sub-pages under a wiki node, all three API paths (raw_content, blocks/sub_page_list, wiki children) are dead ends. Just ask the user for the direct link.

## Group Communication Rules
- **Never mention technical details** in the group (permissions, APIs, file upload failures, etc.)
- Group messages: results only, concise, professional
- Technical issues → DM 浚宇 privately
- When sending meeting summary, only the summary content — no process notes
- If a tool/API path is blocked, solve it in DM with 浚宇; group sees only the final result
