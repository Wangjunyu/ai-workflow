---
name: poe-platform
description: "Poe.com platform: API capabilities, SDKs, chat history retrieval, Canvas Apps API, limitations and workarounds."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [poe, ai-platform, api, research, chat-history]
    related_skills: []
---

# Poe Platform

Working with Poe.com (Quora's AI aggregator) — API capabilities, chat history access, SDK options, and platform limitations.

## When to Use

- User asks about Poe's API, SDK, or programmatic access
- User wants to export or retrieve Poe chat history/conversations
- User is building an integration with Poe
- Researching what Poe can and cannot do via API

## Quick Summary

Poe has two API surfaces:

1. **REST API** (`api.poe.com`) — forward-only. Send messages, get responses. No chat history retrieval.
2. **Canvas Apps API** (`window.Poe`) — browser JS only. Can read recent messages from current chat.

## REST API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/chat/completions` | POST | OpenAI-compatible, all bots |
| `/v1/messages` | POST | Anthropic-compatible, Claude only |
| `/v1/responses` | POST | OpenAI Responses API format (reasoning, tools, web search) |
| `/v1/models` | GET | List available models |
| `/v1/balance` | GET | Check point balance |
| `/usage/points_history` | GET | Usage metadata (bot_name, query_id, cost, timestamp — NO message content) |

Key limitation: **no endpoint retrieves actual message content/history.** The REST API is a forward-only pipeline.

API key management: `poe.com/api/keys`

## Chat History: What's Possible

See `references/chat-history-research.md` for detailed findings.

**Bottom line**: Poe's REST API cannot retrieve past conversation content. Options:

- **Canvas App** (`window.Poe.getDefaultChat(limit)`) — browser JS only, current chat only, gets text content
- **Usage History API** — metadata only, up to 30 days
- **Browser automation** — scrape Poe web, login required, high maintenance
- **Poe data export** — check Poe settings for "Export Data" option

## SDKs

- **Official Python SDK**: `fastapi-poe` (PyPI) — for building bots on Poe
- **Official client**: `poe-client` (PyPI)
- **Third-party `poe-api`** (ading2210) — reverse-engineered, ARCHIVED 2023, does not work

## References

- `references/chat-history-research.md` — Full research notes on retrieving Poe conversation history
