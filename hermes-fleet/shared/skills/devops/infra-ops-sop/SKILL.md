---
name: infra-ops-sop
description: 【强制入口】所有飞书/Obsidian/Getnote/跨服务器操作的第一站。不加载此 skill 就不能执行任何 infra 操作。包含完整的路由表、坑位文档、API 注意事项。禁止 agent 自己探索 API——一切走 SOP。
category: devops
---

# Infra-Ops SOP — Master Router

**🛑 STOP — READ THIS FIRST.**

If you are reading this skill because you've already started trying to call `lark-cli`, write Feishu API calls, SSH to another machine, or manipulate Obsidian files **without loading this skill first** — STOP immediately. Delete or abort any half-written code. Start over from this skill's routing table.

You do NOT have the ability to figure out Feishu/Obsidian/SSH operations on your own. The sub-skills referenced below contain the ONLY correct way to do these operations — they encode months of battle-testing, API version changes, authentication pitfalls, and Hermes-specific quirks that you cannot discover by trial and error.

---

**MANDATORY ENTRY POINT.** When ANY agent needs to do Feishu, Obsidian, or Getnote operations, load this skill FIRST. It routes to the correct sub-skill. Do NOT write exploratory code from scratch — the sub-skills contain battle-tested, error-documented procedures.

## Auto-Detection: When You MUST Load This Skill

Load this skill the moment you see ANY of these keywords in the user's request or in your planned actions:

**飞书/Lark/Feishu** — doc, wiki, 知识库, 云盘, drive, 妙记, meeting minutes, 文档
**Obsidian** — vault, note, 笔记, markdown
**Getnote/得到大脑** — 笔记保存, 搜索
**Infrastructure** — SSH, Tailscale, 服务器, mac-mini, firefly, profile 创建
**Tools** — lark-cli, obsidian-cli, getnote

**If you catch yourself about to call `lark-cli` without having loaded this skill: STOP. Load this skill first.**

## When to Load

Load this skill when the agent needs to:
- Read/find any Feishu document
- Download a 妙记 (meeting minutes) transcript
- Sync content to Obsidian vault
- Sync content to 得到大脑 (Getnote)
- Create a new infra-ops profile
- Scan/index Feishu wiki knowledge base paths
- Scan/index Feishu cloud drive folder structure
- Run long-running overnight scans (silent cron + morning report)
- SSH to mac-mini or any other machine for infrastructure tasks
- Manage cron jobs for infrastructure monitoring

## Routing Table

| Operation | Sub-Skill to Load |
|-----------|-------------------|
| Read/find Feishu doc | `infra-feishu-doc-read` |
| Download 妙记 transcript | `infra-feishu-minute-download` |
| Obsidian vault sync (read/write/git) | `infra-obsidian-sync` |
| Getnote save/search/list | `infra-getnote-sync` |
| 飞书群组免 @ 配置 | `references/feishu-group-config.md` |
| Create new infra-ops profile | See `references/profile-create-conventions.md` |
| 检查 firefly 上的非 Hermes 服务 | `references/firefly-services.md` |
| Scan wiki knowledge base paths | `references/wiki-scan-workflow.md` |
| Scan cloud drive folder tree | `references/drive-scan-sop.md` |
| Run overnight silent scan | `references/wiki-scan-workflow.md` (Phase 5) |
| Daily incremental wiki sync | `scripts/incremental-wiki-scan.py` — detects new child nodes |
| Daily minutes index sync | `scripts/minutes-daily-search.py` — search + update minutes-index.md |

## Core Rules (apply to ALL sub-skills)

### 0. Check Wiki Path Index FIRST (NEW)

Before doing ANY live API discovery for wiki paths, check `references/wiki-path-index.md`. This index caches known wiki space IDs, person directories, and meeting record nodes. Live discovery is expensive (5+ API calls for a single path) — the index makes it instant.

**If the path is in the index:** use it directly. Zero API calls.
**If the path is NOT in the index:** do live discovery, then UPDATE the index with the new path.
**If doing a full/wide scan (multiple knowledge bases, many nodes):** follow `references/wiki-scan-workflow.md` — probe first, estimate cost, confirm with user, then use subagent batches with sleep delays.

### 1. Never Guess Auth
If an API returns `401`, `403`, `99991679` (missing_scope), or `131006` (permission denied) — STOP. Report exactly what permission/scope is needed. Do NOT try adjacent endpoints.

### 2. The `{variable}` Template-Substitution Bug
The Hermes preprocessor silently replaces `{identifier}` patterns in ALL code strings — even single-quoted heredocs. Always use `%s` formatting and `dict()` constructor in Python. Never put `{...}` in terminal/write_file code strings.

String concatenation (`"prefix " + var`) is safe. Prefer `%s` for all interpolation.

### 3. Sub-Page Dead End
Feishu REST API CANNOT enumerate sub-pages of docx documents. `raw_content` + `blocks` (block_type=51) confirm sub-pages exist, but do NOT list them. Wiki children API returns 404. One round-trip to the user is faster than 15 rounds of failed brute-force.

### 4. Identity Ownership
A document created by bot (tenant token) CANNOT be moved by user auth. And vice versa. The entity that creates owns it. Plan identity usage upfront.

### 5. Auth Is Layered
Page-readable ≠ space-enumerable. Test each layer: page body → node metadata → wiki space → enumeration. Report which layer fails, not just "it doesn't work."

### 6. Overnight Silent Scan Pattern (NEW)
For long-running full scans (50+ API calls, 10+ minutes), do NOT run inline — use cron jobs with `deliver='local'` (no user notification) + a separate morning report cron at 06:05 with `deliver='origin'`. This keeps the user's chat clean overnight. See `references/wiki-scan-workflow.md` Phase 5 for the step-by-step recipe.

Key parameters for silent scan cron jobs:
- `deliver='local'` — output saved to file, no message to user
- `enabled_toolsets=["terminal","file","skills"]` — minimal toolset
- `profile='default'` — inherit the right skills/env
- `schedule='1m'` or `'2m'` — stagger jobs by 1-2 minutes so they don't all hit the API simultaneously at startup

### 7. Script Execution in Hermes (NEW)
Hermes security filters block `command | python3 -c '...'` (pipe-to-interpreter) and `python3 << 'EOF'` (heredoc-to-interpreter). Both are treated as code injection risks.

**Workaround:** Always write scripts to a file with `write_file`, then run with `terminal("python3 /path/to/script.py")`.

This applies to all infra-ops tools (lark-cli, getnote, obsidian-cli) — any pipeline that pipes CLI output into Python for parsing.

### 8. `--page-all` + `Found N node(s)` JSON Output Pollution (lark-cli)
When using `lark-cli ... --page-all`, two prefixes pollute stdout BEFORE the JSON:
- `[page N] fetching...` (--page-all pagination prefix)
- `Found N node(s)` (lark-cli summary line, appears even without --page-all when output goes to file via `>`)

Parsing raw output with either prefix will fail with `JSONDecodeError`.

**Fix:** Always strip BOTH prefixes before parsing:
```python
raw = re.sub(r'^\[page \d+\] fetching\.\.\.\s*', '', raw, flags=re.MULTILINE)
raw = re.sub(r'^Found \d+ node\(s\)\s*\n?', '', raw, flags=re.MULTILINE)
```
This affects all `lark-cli drive files list` and `lark-cli wiki` commands that use `--page-all` OR redirect to file.

### 9. lark-cli v1.0.44+ Breaking Changes (NEW)

**lark-cli v1.0.44** introduced two breaking changes from earlier versions:

#### 9a. Flag-only arguments — positional args rejected
Positional arguments are no longer supported. Any command passing a token or space_id as a positional arg will fail with:
```
Error: positional arguments are not supported (got ["<value>"]); pass values via flags
```

**Fix:** Always use flags:
```bash
# ❌ BROKEN in v1.0.44+
lark-cli wiki +node-list <token>

# ✅ CORRECT
lark-cli wiki +node-list --space-id <space_id> --parent-node-token <token>
```

#### 9b. Dict response wrapper instead of raw array
Responses are wrapped in `{"ok":true, "data":{"nodes":[...]}}` instead of a bare JSON array.

**Fix:** Navigate into `data["nodes"]` before iterating:
```python
data = json.loads(raw)
if isinstance(data, dict) and "data" in data:
    nodes = data["data"]["nodes"]  # v1.0.44+ dict wrapper
elif isinstance(data, list):
    nodes = data                    # legacy bare array
else:
    # error handling
```

#### 9c. Wiki node-list syntax reference (v1.0.44)
```
lark-cli wiki +node-list --space-id <SPACE_ID> --parent-node-token <TOKEN> --page-all --page-limit 0
```
- `--space-id`: wiki space ID (use `+space-list` to discover)
- `--parent-node-token`: parent node to enumerate children of
- `--page-all`: auto-paginate through all pages
- `--page-limit 0`: unlimited pages (default 10)

### 10. 妙记匿名说话人无法通过 API 改名 (NEW)

**问题**：当妙记中某说话人未匹配到飞书用户（显示为「说话人 1」「说话人 2」），`minutes minutes get` 和 transcript API 均**不返回**该说话人的 `open_id`。`+speaker-replace` 需要 `--from-user-id`（`ou_` 开头），无法获取。

**根因**：匿名说话人在飞书系统中没有用户身份绑定，API 不暴露其内部 speaker_id。

**结论**：此类改名只能在飞书网页端手动操作。API 路线不通。不要反复尝试不同 endpoint 或暴力搜索——已验证 `minutes minutes get`、`transcript`、`+search` 均不返回匿名说话人 ID。

**权限要求**：`+speaker-replace` 需 `minutes:minutes:update` scope（需额外授权，不在默认 scope 中）。

### 11. lark-cli auth token 获取 (NEW)

`lark-cli` 没有 `auth token` 子命令。需通过 `lark-cli api <method> <path>` 直接调用 Lark Open API（自动附带 token），无需手动提取 Bearer token。

```bash
# ✅ 正确：直接调用 api 子命令
npx @larksuite/cli api GET "/open-apis/minutes/v1/minutes/{token}" 

# ❌ 错误：尝试 lark-cli auth token（不存在）
```

### 10. `hermes config set` 存嵌套值为 JSON 字符串（BUG）

`hermes config set feishu.group_rules '{"chat_id": {...}}'` 会把值存成 **JSON 字符串**，不是 YAML dict。

Feishu adapter 用 `isinstance(raw_group_rules, dict)` 判断，字符串会被跳过 → 配置不生效。

**Fix:** 直接编辑 config.yaml（用 Python yaml.dump + write_file 或手动编辑）。不要通过 `hermes config set` 设置嵌套 dict 值。

### 12. 飞书免 @ 配置：oc_（群 ID）≠ omt_（话题 ID）

**问题**：group_rules 中配置了 `omt_` 前缀的话题 ID，但免 @ 不生效。

**根因**：`_admit` 函数（feishu.py:4009）用 `chat_id` 查找 `group_rules`，而飞书事件中 `chat_id` 始终是 `oc_` 前缀的群 ID。`omt_` 前缀的话题 ID 存在 `thread_id` 字段，不会被 `_admit` 的字典查找匹配到。

**结论**：`group_rules` 中 `omt_` 开头的条目是**死代码**——永远不生效。只保留 `oc_` 群 ID 条目即可。话题路由由 `_send_raw_message` 自动处理，无需额外配置。

**验证方法**：`grep -c 'Inbound group.*chat_id=oc_<ID>' gateway.log` vs `grep -c 'Sending response.*to oc_<ID>' gateway.log`。回复数 ≥ 入站数 = 免 @ 生效。

详见 `references/feishu-group-config.md`。

### 14. 妙记索引 Cron 需要用户授权 (NEW)

**问题**：`cron/minutes-index-daily-sync` 在 firefly cron 中执行 `lark-cli minutes +search` 失败。

**根因**：`minutes +search` 仅支持 `--as user`。Bot 身份无法使用此命令（报错：`--as bot is not supported`），Bot 直调 REST API 也失败（`/minutes` → 404，`/minutes/search` → field validation 失败）。Firefly 是无头服务器，无 GNOME keyring 守护进程，lark-cli 用户 OAuth token 无法持久化存储。

**现状**：每次 `lark-cli auth login` 需要通过浏览器扫码授权。在 cron 环境中无法交互。

**解决方案**：
- **短期**：用户在 firefly 上手动 `lark-cli auth login --domain minutes`，扫码授权一次。token 会暂存，但可能随时间过期。
- **长期**：将 cron job 迁移到 mac-mini（有用户会话 + Keychain Access），或使用飞书服务端 OAuth 流程（refresh token 持久化到文件而非 keychain）。

**相关日志证据**：`auth status` → `user: missing`；`minutes +search` → `need_user_authorization`。

### 15. `read_file` + `write_file` 大文件数据丢失 (NEW — 2026-06-13)

**问题**：`read_file` 对大文件（>~100K chars）返回截断内容，用 `write_file` 写回截断内容会导致数据永久丢失。本次会话中 `wiki-path-index.md`（65KB, 1371 行）被读到 1371 行看似完整，但 `write_file` 写回时只剩 235 行——云盘结构和多个知识库 section 全部丢失。

**根因**：`read_file` 底层有字符数上限，超过后静默截断（不报错，返回的 `content` 看似完整但缺少后半部分）。`write_file` 整文件覆写，没有任何 diff 保护。

**恢复方法**：
```bash
# 从 git 历史恢复原始文件
cd ~/ai-workflow
git show <last-good-commit>:path/to/file.md > /tmp/restored.md
cp /tmp/restored.md <target-path>
```

**正确做法**：对大于 ~60KB 的文件（`wiki-path-index.md`、云盘索引等），**永远不要 read_file + write_file 整文件处理**。改用：
1. **小修改**：直接用 `patch` tool 做 surgical 替换（不改动文件其余部分）
2. **大修改**：用 `execute_code` Python 脚本 `open(path).read()` + `.write()`（绕过 read_file/write_file 工具限制）
3. **恢复**：`git show` 从历史恢复

**识别大文件**：执行任何 infra 操作前，如果目标文件是 `references/wiki-path-index.md` 或其他已知的大型索引文件，默认它就是大文件，直接走 patch 或 execute_code 路线。

### 16. 增量扫描脚本 `existing` dict 需与索引同步 (NEW — 2026-06-13)

**问题**：`scripts/incremental-wiki-scan.py` 内嵌 `existing` dict 缓存了已知节点。当 `wiki-path-index.md` 发生结构性变化（新增叶子节点、人员移动等），脚本 dict 若不同步更新，下次 cron 运行会报 false positive。

**触发条件**：以下索引变更需同步更新脚本 dict：
- 任何 has_child=true 父节点下新增叶子节点
- 人员跨目录移动（token 不变但 organizational 位置变化 — 仅需更新 scan list 标签）
- 新增 has_child=true 的父节点（需加入 scan list + existing dict）

**同步步骤**：
1. 更新 `wiki-path-index.md` 后，立即检查对应的 `incremental-wiki-scan.py`
2. 新增叶子 token → 加入 `existing` dict 对应父节点的 `children` 中
3. 新增父节点 → 加入 `scans` list 和 `existing` dict
4. 人员移动 → 更新 `scans` list 中的 label 字符串
5. **has_child→false** → 将 `existing` dict 对应条目改为 `{}`，**并从 `scans` list 中移除**（避免每日浪费 API 调用枚举空子节点）

### 17. lark-cli TTY 输出截断 — minutes +search token 不完整 (NEW — 2026-06-16)

**问题**：`lark-cli minutes +search --format json` 在 stdout 是 TTY 时，token 字段被截断显示（如 `obcn9d...41bj`），导致后续 API 调用无法使用。

**根因**：lark-cli 检测到 TTY 时会对长字段做省略显示，即使 `--format json` 也不例外。`subprocess.run(capture_output=True)` (stdout=PIPE) 理论上不受影响，但通过 `print()` 输出到 Hermes terminal tool 时可能再次触发截断。

**Workaround**：始终将 lark-cli 输出重定向到文件，再从文件读取：
```bash
# ✅ 正确：输出到文件
npx @larksuite/cli minutes +search --as user --format json ... > /tmp/result.json 2>&1

# ❌ 错误：直接捕获 stdout（token 可能截断）
result = subprocess.run(cmd, capture_output=True, text=True)
data = json.loads(result.stdout)  # token 字段可能不完整
```

**验证**：读取文件后检查 `len(item["token"])` — 完整 token 应为 24 字符（`obcn` + 20 位）。

**波及范围**：可能影响所有 lark-cli 输出中包含长 ID/token 字段的命令（`drive files list`、`wiki +node-list` 等）。遇到截断字段时优先尝试文件重定向。

**参考脚本**：`scripts/minutes-daily-search.py` — 完整的逐日分段搜索实现，输出到文件后解析。

### 18. Python subprocess 调用 npx/lark-cli 必须显式传递 TERM (NEW — 2026-06-18)

**问题**：`subprocess.run(cmd, shell=True, ...)` 启动 npx 子进程时，若父 Python 进程缺少 `TERM` 环境变量，npx 会报 `TERM environment variable not set.` 并退出码 1。

**根因**：Hermes cron / background terminal 环境不设置 `TERM`。`subprocess.run()` 默认继承父进程环境，npx 读到空 TERM 后拒绝运行。

**Fix**：
```python
penv = os.environ.copy()
penv.setdefault("TERM", "dumb")  # or penv["TERM"] = "dumb"
subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=90, env=penv)
```

**NOT `penv.setdefault`** alone — 如果 `TERM` 已存在但值为空字符串，`setdefault` 不会覆盖。如需保险，直接 `penv["TERM"] = "dumb"`。

### 19. lark-cli 脚本：前台运行 vs 后台运行 (NEW — 2026-06-18)

**问题**：调用 lark-cli 的 Python 脚本用 `terminal(background=true)` 启动时，`TERM` 变量丢失导致 npx 报错，即使已在 subprocess 内设置了 env。

**Workaround**：对于需要多步 lark-cli 调用（3+ 次 API 调用）的扫描脚本，使用 `terminal(background=false)` 前台运行并设置足够的 timeout（如 `timeout=300`）。脚本内部 sleep 间隔不会触发超时——timeout 只在命令完全卡死时生效。

**适用场景**：wiki 增量扫描（~20 API calls × 4s sleep = ~80s）、drive 目录枚举、minutes 批量搜索等。

**注意**：此规则仅在脚本内已正确设置 `env=penv` 但仍失败时使用。优先尝试 foreground 而非反复调 background env。

### 20. minutes +search 响应字段结构与 token 截断 (NEW — 2026-06-21)

**问题**：`lark-cli minutes +search` 返回的 item 结构不同于 `minutes minutes get`。关键字段：
- `display_info`: 格式化字符串（标题 + 关键词 + 所有者 + 开始时间 + 时长）
- `meta_data.app_link`: 完整妙记 URL（`https://rcnsiaef7x5y.feishu.cn/minutes/FULL_TOKEN`）— **唯一可靠的完整 token 来源**
- `token`: **永远被截断**（如 `obcnct...qu2t`）— 即使输出重定向到文件后 JSON 中也如此。这是 lark-cli 对搜索结果的故意截断，与 TTY 无关

**没有的字段**：`create_time`（Unix 时间戳）、`duration`（秒数）、`status`、`topic`（独立字段）。所有信息需从 `display_info` 字符串中正则解析。

**Fix**：
```python
# ✅ 从 app_link URL 提取完整 token
m = re.search(r'/minutes/(\w{20,})', item["meta_data"]["app_link"])
token = m.group(1)  # 24-char full token

# ❌ 使用 item["token"] — 被截断，无法用于 API 调用
```

**display_info 解析**：
```python
# 格式: "TITLE\n<b>关键词:</b> ...\n所有者: X 开始时间: YYYY.MM.DD HH:MM:SS 时长: X 小时 Y 分 Z 秒"
lines = display.split('\n')
topic = lines[0].strip()
m = re.search(r'开始时间:\s*(\d{4})\.(\d{2})\.(\d{2})\s+(\d{2}):(\d{2}):(\d{2})', display)
m = re.search(r'时长:\s*(.+)', display)  # "X 小时 Y 分 Z 秒" or "Y 分 Z 秒"
```

**参考实现**：`scripts/minutes-daily-search.py` — 完整的 `parse_search_item()` 函数。

### 13. 免 @ 问题排查：走源码+日志，不兜圈子

用户报告免 @ 不生效时，**不要**基于"之前配置过应该没问题"做断言。必须走：
1. 读源码 → 确认匹配逻辑（`_admit` 用哪个字段、字典 key 是什么）
2. 查日志 → 统计入站/出站数、有无拒绝记录
3. 核对 config → 确认 group_rules 是 YAML dict 不是 JSON 字符串
4. 用数据回复，不做"我觉得应该没问题"的循环论证

## Verification Checklist

Before concluding any infra-ops task:
- [ ] Correct sub-skill loaded and followed
- [ ] Auth checked before API calls
- [ ] No `{variable}` bug in any code string
- [ ] Error codes reported precisely (not generic "it failed")
- [ ] No brute-forcing dead-end API paths
- [ ] `--page-all` output stripped of `[page N] fetching...` prefix before JSON parsing
- [ ] lark-cli commands use flags (`--space-id`, `--parent-node-token`) not positional args (v1.0.44+)
- [ ] API responses parsed via `data["data"]["nodes"]` dict wrapper (v1.0.44+), not bare array
- [ ] Scripts written to file (not piped to interpreter or heredoc) to avoid Hermes security blocks
- [ ] Large files (>60KB) edited via `patch` or `execute_code`, not `read_file` + `write_file` (rule 15)
- [ ] `incremental-wiki-scan.py` existing dict synced after index changes (rule 16)
- [ ] `incremental-wiki-scan.py` scans list cleaned up if has_child→false (rule 16 step 5)
- [ ] lark-cli output for ID/token fields checked for TTY truncation; use file redirect if truncated (rule 17)
- [ ] `Found N node(s)` prefix stripped before JSON parsing, not just `[page N]` prefix (rule 8 updated)
- [ ] Python subprocess calling npx passes `env=penv` with `TERM=dumb` (rule 18)
- [ ] Multi-step lark-cli scripts run in foreground (not background) to avoid TERM loss (rule 19)

## Cross-Profile Coverage: Ensuring Every Profile Routes Here

This skill is useless if other profiles don't know to load it. The mechanism is AGENTS.md routing instructions.

### Fleet Template

A reusable routing section lives at `hermes-fleet/shared/templates/infra-routing.md`. When creating new profiles or auditing existing ones, insert this into their AGENTS.md.

### Routing Section (insert into every non-infra profile's AGENTS.md)

```markdown
## 基础设施路由

**你不会自己摸索飞书 API、SSH 连接、Obsidian 路径、得到大脑 API。所有 infra 操作必须走 SOP。**

当用户让你做以下操作时，先加载 `infra-ops-sop`，然后按其路由表加载对应子 skill：

| 操作类型 | 加载 Skill |
|---------|-----------|
| 飞书文档/知识库/妙记/云盘 | `infra-ops-sop` |
| Obsidian vault 读写/同步/Git | `infra-ops-sop` |
| 得到大脑（Get笔记） | `infra-ops-sop` |
| 跨服务器 SSH/文件 | `infra-ops-sop`、`git-firefly-bridge` |
| 创建新 Hermes profile | `infra-ops-sop`、`infra-profile-create` |
| 网络/Tailscale | `infra-ops-sop`、`tailscale` |

**原则：不猜 API、不试错端点、不走捷径。走 SOP。**
```

### Verification Commands

```bash
# Check which profiles have infra-ops-sop available
for p in $(hermes profile list --names); do
  hermes -p $p skills list 2>/dev/null | grep -q infra-ops-sop && echo "$p ✅" || echo "$p ❌ MISSING"
done

# Check which profiles have the routing section in AGENTS.md
for p in default bengbeng tws-coach peopleman planner intake; do
  path="$HOME/.hermes/profiles/$p/AGENTS.md"
  [ "$p" = "default" ] && path="$HOME/.hermes/AGENTS.md"
  grep -q '基础设施路由' "$path" 2>/dev/null && echo "$p ✅" || echo "$p ❌ MISSING"
done

# Deploy missing skills to profile with own skills dir
cp -r ~/.hermes/skills/devops/infra-* ~/.hermes/profiles/<name>/skills/devops/
```

### Common Gaps Found

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Profile lists infra-ops-sop but directory missing | Sync command failed silently | `cp -r` directly from global skills |
| Profile has skills but doesn't load them | AGENTS.md missing routing section | Insert routing section into AGENTS.md |
| New profile created after fleet sync | infra-profile-create step 2c doesn't auto-add routing | Manually insert; update infra-profile-create skill |
