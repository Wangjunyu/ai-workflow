---
name: feishu-document-api
description: Read and interact with Feishu/Lark documents and minutes (妙记) via REST API + lark-cli when feishu_doc_read is unavailable (e.g., in DM context). Covers token auth, raw_content, blocks, wiki nodes, minutes transcript access, lark-cli domain auth, and shell-escaping pitfalls.
---

# Feishu Document API

When `feishu_doc_read` fails with "Feishu client not available (not in a Feishu comment context)", use the Feishu REST API directly via `terminal`. This happens in DM/私聊 — the built-in tool only works when the user @mentions you inside a Feishu document comment.

## Prerequisites

Environment variables must be set:
- `FEISHU_APP_ID` — e.g. `cli_aa952e66a6799ceb`
- `FEISHU_APP_SECRET`

## Step 1: Get tenant_access_token

```bash
python3 << 'PYEOF'
import subprocess, json, os

r = subprocess.run(['curl', '-s', '-X', 'POST',
    'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps({'app_id': os.environ['FEISHU_APP_ID'], 'app_secret': os.environ['FEISHU_APP_SECRET']})],
    capture_output=True, text=True)
token = json.loads(r.stdout)['tenant_access_token']
print(token)
PYEOF
```

Token expires in ~2 hours. Cache it in `/tmp/feishu_token.json` for the session.

## Step 2: Read document content

Document tokens look like `PLC2wV49MiR9Nnkoc00clIUanG5` or `YmVtwq1PJiLjZLkdLqrc7YignBf`.

### raw_content (plain text)

```bash
curl -s "https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/raw_content" \
  -H "Authorization: Bearer ${TOKE...```

Best for: searching text, extracting summaries.

### blocks (structured)

```bash
curl -s "https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks?page_size=100" \
  -H "Authorization: Bearer ${TOKE...```

Returns block tree with types: `page`, `heading2`, `bullet`, `sub_page_list`, etc. Useful for discovering child pages and document structure.

### wiki node info (type detection)

```bash
curl -s "https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token={NODE_TOKEN}" \
  -H "Authorization: Bearer ${TOKE...```

Returns `obj_type` (e.g., `doc`, `bitable`, `mindnote`, `board`), title, parent, children. Crucial when `raw_content` returns empty — the document may be a non-text type (Bitable, Board, etc.).

## Pitfalls

### Shell escaping with tokens

Tokens may contain characters (like `***`, `$`, backticks) that break shell strings. Two safe patterns:

**Pattern A: Python subprocess (preferred)**
```python
python3 << 'PYEOF'
import subprocess, json, os
# ... get token with subprocess.run(['curl', ...])
# Token never touches shell interpolation
PYEOF
```

**WARNING: The `{variable}` template-substitution bug — applies EVERYWHERE, not just f-strings.** The Hermes preprocessor silently replaces `{identifier}` patterns in ALL code that passes through `terminal`, `write_file`, `execute_code`, AND heredocs — even single-quoted `<< 'PYEOF'` blocks. Any line like `"Bearer {token}"` or `f"url/{id}"` gets corrupted. This cost 10+ rounds of debugging.

**THE FIX: Use `%s` formatting and `dict()` constructor exclusively.** Never put `{...}` in any code string.
```python
# BROKEN — {tk} gets replaced, string breaks:
auth = "Bearer " + tk  # actually fine, but
auth = f"Bearer {tk}"  # BROKEN

# WORKS:
auth = "Bearer %s" % tk
body = json.dumps(dict(children=[dict(block_type=2, text=...)]))
```

String concatenation (`"prefix " + var`) is safe. `.format()` with doubled braces (`{{}}`) may work but is fragile. **Prefer `%s` for all string interpolation in terminal/write_file/execute_code contexts.**

**Pattern B: Write token to file first**
```bash
echo "$TOKE..." > /tmp/fstoken.txt
TOK=$(cat /tmp/fstoken.txt)
curl ... -H "Authorization: Bearer ***" ...
```

### raw_content returns empty → check blocks for embedded objects

The document may be a Bitable, Board, or Mindnote — not a text document. Use `wiki/v2/spaces/get_node` to check `obj_type`, then use the appropriate API for that type.

**Board (whiteboard) detection via blocks API is the most common case.** When `raw_content` returns only a title, the real content is often an embedded Board:

```bash
# Get blocks — look for block_type=43 (Board)
curl -s "https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks?page_size=50" \
  -H "Authorization: Bearer ${TOKE...```

Block type 43 = Board/whiteboard. The `board.token` field holds the whiteboard token for deeper access. Board API: `GET /open-apis/board/v1/whiteboards/{board_token}` (may require additional permissions).

### Board content not available via REST API

Board/whiteboard content is often not accessible through the standard REST API (returns 404). In these cases, the board token combined with the document URL is the deliverable — the user can view it directly in Feishu.

### sub_page_list interpretation

Documents with `sub_page_list` blocks (block_type=51, containing `wiki_token`) have child pages. These are Feishu document-internal sub-pages, NOT wiki node children. The wiki children API may return 404 for docx nodes. Use the `sub_page_list` block's wiki_token to identify the parent wiki structure, then check block children for the actual sub-page tokens.

### lark-cli as an alternative tool

`lark-cli` (`/opt/homebrew/bin/lark-cli`) is the Feishu CLI tool. It provides `wiki +node-list` for listing wiki nodes and `drive +export` for exporting documents. Requires `lark-cli config bind --source hermes --identity user-default` to bind to the Hermes environment. Once bound, it's often faster than raw REST calls for navigation tasks.

## Minutes (妙记) Access

**App-level REST API is a dead end.** The `/open-apis/vc/v1/minutes/` endpoints return 404 unless the app has been granted VC (视频会议) permissions in the Feishu developer console. Most apps don't have this. Don't waste time trying.

**The correct path: lark-cli user authorization with `--domain minutes`.** This grants user-level access to minutes, which the user can already view in Feishu.

See `references/feishu-minutes-errors.md` for a catalog of specific error codes and their resolutions.

### Full auth flow

```bash
# Step 1: Bind lark-cli (one-time)
lark-cli config bind --source hermes --identity user-default

# Step 2: Initiate device auth (non-blocking)
lark-cli auth login --domain minutes --no-wait --json
# Returns: {"device_code": "...", "verification_url": "https://..."}

# Step 3: Generate QR code for user to scan
cd /tmp && lark-cli auth qrcode "<verification_url>" -o feishu_auth_qr.png
# Display the QR image to the user + the verification_url as fallback

# Step 4: AFTER user confirms authorization complete, poll with device_code
lark-cli auth login --device-code "<device_code_from_step2>"
```

### Domain flag and scope combination

Use `--domain` for bulk domain-scoped auth. Available domains: `approval, apps, attendance, base, calendar, contact, docs, drive, event, im, mail, markdown, minutes, okr, sheets, slides, task, vc, wiki, all`.

`--recommend` only requests auto-approve scopes — may miss domain-specific permissions.

**Adding specific scopes:** When `--domain` grants most permissions but a specific one is missing (e.g., `wiki:node:move`), combine `--domain` + `--scope`:
```bash
lark-cli auth login --domain wiki --scope "wiki:node:move" --no-wait --json
```

**Avoid bare `--scope` without `--domain` for large permission sets.** `--scope "wiki:node:move wiki:node:update wiki:node:delete"` may fail with "invalid or malformed scopes" — the `--domain` prefix normalizes the scope namespace. Prefer `--domain wiki --scope "wiki:node:move"` and add scopes incrementally.

### After auth: accessing minutes

Once authorized, lark-cli can call minutes APIs directly with `lark-cli api`. The minutes token comes from the URL: `https://...feishu.cn/minutes/<token>`. Tokens look like `obcn5l9n17t3hsj882976g59`.

**Get minutes basic info (works with `--domain minutes` auth):**
```bash
lark-cli minutes minutes get --params '{"minute_token":"<token>"}' --as user
# Returns: title, duration, owner_id, create_time, url, cover
```

**Get transcript (REQUIRES extra scopes!):**
```bash
lark-cli api GET "/open-apis/minutes/v1/minutes/<token>/transcript" --as user
```

⚠️ **CRITICAL: Transcript needs a SECOND auth round.** The initial `--domain minutes` auth grants `minutes:minutes.basic:read` (enough for basic info), but transcript access requires:
- `minutes:minute:download`
- `minutes:minutes.transcript:export`

If you get `99991679` / `missing_scope`, re-auth with:
```bash
lark-cli auth login --scope "minutes:minute:download minutes:minutes.transcript:export" --no-wait --json
# Then QR → user scans → device-code poll as before
```

The scope-based auth ADDITIVELY grants new scopes — existing scopes are preserved.

**API path gotcha:** Basic info and transcript are on DIFFERENT base paths:
- Basic info: `/open-apis/vc/v1/minutes/<token>` ✅
- Transcript: `/open-apis/vc/v1/minutes/<token>/transcript` ❌ (404 even with user auth!)
- Transcript (correct): `/open-apis/minutes/v1/minutes/<token>/transcript` ✅

Don't waste time guessing paths — use `lark-cli api` which handles the routing.

### One-shot automation idea

For recurring use (e.g., "after every coaching call, download minutes and push to group"), auth once with all needed scopes, then script the download+push steps. The user auth flow is the blocker — once authorized, the rest is automatable.

Full end-to-end workflow (download → Drive upload → group message → wiki comment): see `references/feishu-minutes-workflow.md`.

### QR code generation gotcha

`lark-cli auth qrcode` requires `--output` to be a **relative path** within the current directory. Absolute paths like `/tmp/qr.png` are rejected with "unsafe output path". Always `cd` to the target directory first:

```bash
cd /tmp && lark-cli auth qrcode "<verification_url>" -o qr.png
```

## Sending files to Feishu groups

### Finding group chat_id

Group chat_ids are in `~/.hermes/profiles/bulma/channel_directory.json`. Look for entries with `"type": "group"`:

```json
{
  "id": "oc_227dda7fd76cf0004921a079e09d1823",
  "name": "康康陪跑-6.4-9.3",
  "type": "group"
}
```

### Sending text-only (works via gateway)

```python
send_message(target="feishu:康康陪跑-6.4-9.3", message="text here")
```

### Wiki comments (alternative to node creation)

When you lack `wiki:node:create` scope but need to attach information to a wiki doc, add a full-document comment with `lark-cli drive +add-comment`:

```bash
lark-cli drive +add-comment \
  --as bot \
  --doc "<doc_token_or_obj_token>" \
  --type docx \
  --full-comment \
  --content '[{"type":"text","text":"📝 Title: https://link.to/file"}]'
```

The `--content` flag takes a JSON array of reply_elements. For plain text, use `[{"type":"text","text":"your message"}]`.

Bot identity works for this even without user auth — as long as the bot has `docx:comment` permission (standard for docx app).

### Sending files (requires app permission)

**Gateway `send_message` with MEDIA: does NOT work for files on Feishu** — returns "Feishu file upload missing file_key". Images may work, but text files don't.

**lark-cli `im +messages-send` with `--file`** needs app-level permission `im:resource:upload` (bot identity). Without it, even the bot can't upload files to group chats.

**lark-cli as user** needs extra scopes (`im:message.send_as_user`, `im:message`) which requires yet another auth round.

**Cannot combine `--file` + `--text`** in one `lark-cli im +messages-send` call — send them as separate messages.

### Current blocker for file push

App `cli_aa952e66a6799ceb` lacks `im:resource:upload` permission. Admin must enable it in Feishu developer console. Once granted, bot can `lark-cli im +messages-send --as bot --chat-id <oc_xxx> --file <path>` to push transcript files to groups.

### Fallback: Drive upload + share link

When file push is blocked, upload to Feishu Drive via REST API (`POST /open-apis/drive/v1/files/upload_all`) and share the returned `url` to the group:

```python
# Safe from the {variable} bug — uses %s formatting
import subprocess, json, os
filepath = "/tmp/transcript.txt"
filename = "transcript.txt"
# Get token first (see Step 1)
cmd = [
    'curl', '-s', '-X', 'POST',
    'https://open.feishu.cn/open-apis/drive/v1/files/upload_all',
    '-H', 'Authorization: Bearer %s' % tk,
    '-F', 'file_name=' + filename,
    '-F', 'parent_type=explorer',
    '-F', 'parent_node=',
    '-F', 'size=' + str(os.path.getsize(filepath)),
    '-F', 'file=@' + filepath
]
r = subprocess.run(cmd, capture_output=True, text=True)
# Returns: {"code":0,"data":{"file_token":"A6Wf...","url":"https://..."}}
```

This uses tenant (app) token and works without extra scopes. Files go to the app's Drive space — group members may need access permission depending on tenant settings.

## Creating and writing docx documents via REST API

### Create a new docx

```python
r = subprocess.run(['curl','-s','-X','POST',
    'https://open.feishu.cn/open-apis/docx/v1/documents',
    '-H','Authorization: Bearer %s' % tk,
    '-H','Content-Type: application/json',
    '-d', json.dumps(dict(title='Document Title'))],
    capture_output=True,text=True)
doc_id = json.loads(r.stdout)['data']['document']['document_id']
```

### Write blocks (append children to the page block)

The document's root block has the same ID as the document. Append children to it:

```python
# Block types: 2=text, 5=heading3
blocks = [
    (5, 'heading3', 'Section Title'),
    (2, 'text', 'Paragraph content here.'),
    (2, 'text', ''),
]

for bt, btype, txt in blocks:
    if btype == 'heading3':
        body = json.dumps(dict(children=[dict(
            block_type=bt,
            heading3=dict(elements=[dict(text_run=dict(content=txt, text_element_style=dict()))], style=dict())
        )]), ensure_ascii=False)
    else:
        body = json.dumps(dict(children=[dict(
            block_type=bt,
            text=dict(elements=[dict(text_run=dict(content=txt, text_element_style=dict()))], style=dict())
        )]), ensure_ascii=False)
    
    subprocess.run(['curl','-s','-X','POST',
        'https://open.feishu.cn/open-apis/docx/v1/documents/%s/blocks/%s/children' % (doc_id, doc_id),
        '-H','Authorization: Bearer %s' % tk,
        '-H','Content-Type: application/json',
        '-d', body], capture_output=True,text=True)
```

**App (tenant) token works for docx creation and writing** — no user auth needed.

### Moving a Drive docx into a Wiki node

After creating+writing a docx, move it into a wiki tree with `lark-cli wiki +move`:

```bash
lark-cli wiki +move \
  --as bot \
  --obj-type docx \
  --obj-token "<document_id>" \
  --target-space-id "<space_id>" \
  --target-parent-token "<wiki_node_token>"
```

⚠️ **Permissions trap:** This often fails with 131006 (`permission denied`) for both bot and user identities. Bot needs `wiki:node:create` app permission; user needs `wiki:node:create wiki:node:read wiki:space:read` scopes.

**Cross-ownership trap:** A docx created by the bot (tenant token) CANNOT be moved by the user (even with full wiki scopes) — returns 131006 "no move permission for document". And vice versa: a user-created docx is not writable by the bot. **The entity that creates the document owns it.** Solution: use the same identity for both creation and move, or create the docx directly inside the wiki via `lark-cli wiki +node-create --as user --parent-node-token <...>` then write content with that same identity.

When blocked, fall back to sharing the docx URL directly or adding a wiki comment with the link.

### User context

When user says "搜飞书文档" and provides a token, use the token directly — don't search Obsidian for the document name. Example: 康康交付清单 `PLC2wV49MiR9Nnkoc00clIUanG5`.

See `references/kangkang-delivery-list.md` for the full document structure and known sub-pages.

### CRITICAL: Finding a document inside another document's sub-pages

**The sub-page dead end is real.** When a user asks "找 X 文档里的 Y 文档" and searching the parent's `raw_content` doesn't find it:

| Method | Result |
|--------|--------|
| `raw_content` | Only document body, no sub-pages |
| `blocks` (sub_page_list) | Shows that sub-pages exist, but **cannot enumerate them** |
| Wiki children API | Returns 404 for docx-type nodes |

**DO NOT keep writing code to brute-force this.** All three API paths are dead for sub-page discovery. The correct workflow:

1. Read parent's `raw_content`, search for keyword
2. **If not found → IMMEDIATELY tell user**: "正文没有，可能在子页面里。飞书 API 拿不到子页面列表，链接发我。"
3. Do NOT loop through blocks, try wiki children, switch API endpoints, or write more scripts

This is a hard API limitation, not a skill issue. One round-trip to the user is faster than 15 rounds of failed code.

### Workflow pitfall: survey before coding

When a user asks to find or read a Feishu document, load this skill FIRST. Do not start writing Python scripts from scratch — the patterns documented here (token auth, blocks API, subprocess escaping, lark-cli) cover 90% of cases. If `feishu_doc_read` fails, check: (1) are we in DM? → use REST API patterns below, (2) is lark-cli bound? → prefer lark-cli for navigation, (3) did raw_content return empty? → check blocks for embedded objects.

**When a tool or API path fails, STOP and report the dead end to the user.** Do not enter a loop of writing new scripts trying adjacent API endpoints. One clear report beats ten blind attempts.
