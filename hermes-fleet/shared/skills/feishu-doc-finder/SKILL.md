---
name: feishu-doc-finder
description: Find documents inside a known Feishu parent document/wiki. Use when 浚宇 or 康康 asks "find X document in Y" — follow the 4-step flow and NEVER brute-force API blind spots.
category: productivity
---

# Feishu Document Finder

When the user asks to find a specific document inside a known Feishu parent document, follow this flow. Do NOT skip steps. Do NOT write exploratory code.

## Context

- 浚宇 is the coach/tech support, 康康 is the client
- Current DM is with 浚宇 (ou_af65440800aed884101066ad0ea1a212)
- Group: 康康陪跑-6.4-9.3

## User Language Mapping

康康 uses casual, non-technical language. She will NOT say "交付清单" or give you document tokens. She says things like:
- "我的画板文档" → 康康交付清单下的画板文档
- "我的财务那个表" → 康康-家庭财务检测表
- "那个教练对话的记录" → 教练相关文档

**Your job:** map her casual description to known documents. Check this table first, then fall back to the 4-step flow with the most likely parent document.

## Known Tokens

| Document | Token |
|----------|-------|
| 康康交付清单 | PLC2wV49MiR9Nnkoc00clIUanG5 |
| 康康 wiki 主页 | XEL9wk9AOisOUXk8zywcRreInee |
| 画板文档 (交付清单下) | WgaTw6iiFiHXnuktzaEcjkEanRh |
| 康康教练对话-督导 | UUFIwZsYliBnj1kA5CPc71m9nyg |
| 教练对话-客户康康-教练浚宇 | SYf0wXTc0iXBK7kGvZ8cgNbjnLb |
| 家庭财务检测表 | (康康交付清单子页面，待补充) |

Tenant base URL: `https://rcnsiaef7x5y.feishu.cn/wiki/`

## Standard 4-Step Flow

### Step 1: Read parent doc raw_content
```
GET /open-apis/docx/v1/documents/{token}/raw_content
```
Search for the target keyword in the returned text.

### Step 2: If found → return the content/link immediately

### Step 3: If NOT found → check blocks for sub_page_list
```
GET /open-apis/docx/v1/documents/{token}/blocks?page_size=100
```
Look for `block_type: 51` (sub_page_list). This confirms the doc HAS sub-pages.

### Step 4: If keyword not in raw_content → STOP. Tell the user:
"正文没有 [关键词]，可能在子页面里。把链接发我，我直接读。"

**DO NOT:**
- Call wiki children API (returns 404 for docx nodes)
- Write scripts to enumerate sub-pages (not possible via REST API)
- Try board/bitable/mindnote APIs guessing the type
- Spend more than 3 tool calls on this

## Why This Flow

Three API paths are dead ends for Feishu docx sub-pages:
1. `feishu_doc_read` — only works in document comment context, not DM
2. Wiki children API — returns 404 for docx-type nodes
3. Blocks sub_page_list — shows block_type=51 but doesn't list child tokens

The user has the link. Asking takes 5 seconds. Brute-forcing takes 15 turns.

## If User Provides a Link

Read it immediately with raw_content. If raw_content returns only title (e.g. "画板文档\n\n\n"), check blocks for embedded content (board/bitable/mindnote blocks). Report what you find — link + embedded token if any.

## Pitfalls

### DO NOT write exploratory code
The biggest failure mode: when raw_content doesn't find the keyword, writing scripts that try wiki children API, board API, bitable API, mindnote API, or block-walking — hoping one of them reveals sub-pages. **All return dead ends.** The user will see you flailing and get frustrated. Instead: Step 4, immediately.

### This skill is NOT for discovering new documents
It handles known parent → known child lookups. If the user asks "what documents does X have?" (enumeration), that's a different task — escalate to 浚宇 with a clear report of what APIs were tried.

### Recognize your user
This DM is with 浚宇 (tech support), not 康康 (client). 浚宇 expects concise reports with links, not suggestions or choices. 康康 uses casual language and does NOT provide tokens.

## Sending to Group

When 浚宇 asks to send a link to 康康:
- Target: `feishu:康康陪跑-6.4-9.3`
- Keep it brief: "康康，这是你要的 [文档名] 👇 [link]"
- After sending, confirm back to 浚宇: "已发到群 ✅"

## Post-Delivery

After resolving the request, always report back to 浚宇 with:
1. What was found (link)
2. Where it was sent (group/DM)
3. Any API dead-ends hit (so he knows the tool landscape)
