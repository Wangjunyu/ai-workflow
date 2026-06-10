# Poe Chat History Retrieval — Research Notes

Date: 2026-06-03

## Question

Can Poe's API be used to programmatically retrieve past AI conversation records?

## Findings

### REST API: No

Poe's REST API (`api.poe.com`) has no endpoint that returns historical message content. Every endpoint is forward-only — you send messages, you get responses.

The closest endpoint is `GET /usage/points_history`, which returns:

```json
{
  "has_more": true,
  "length": 5,
  "data": [
    {
      "creation_time": 1761523099056852,
      "bot_name": "Claude-Sonnet-4.5",
      "query_id": "ltol8bhnkya9ak3twt",
      "usage_type": "API",
      "cost_points": 6554
    }
  ]
}
```

- **Contains**: bot_name, query_id, cost_points, timestamp, usage_type (API/Chat/Canvas App)
- **Does NOT contain**: message text, user prompts, AI responses
- **Retention**: 30 days
- **Pagination**: cursor-based via `starting_after` parameter (use last `query_id`)
- **Max per request**: 100 entries, default 20

### Canvas Apps API: Partial

The `window.Poe` browser JS API (available only inside Poe Canvas Apps) has:

```javascript
const chat = await window.Poe.getDefaultChat(50);
// Returns:
// chat.messages[]  — {text, role, contentType, attachments}
// chat.userMembers[] — participants
```

- Gets actual message text
- Default limit: 50 messages
- **Limitations**: browser-only, current chat only, requires Canvas App context

### Third-Party Libraries

| Library | Status | Notes |
|---------|--------|-------|
| `poe-api` (ading2210) | ARCHIVED Sep 2023 | Reverse-engineered, 2.5k stars, does not work |
| `fastapi-poe` | Active (v0.0.83) | Official, for building bots, not for retrieving history |
| `poe-client` | Active (v0.5.1) | Official Python client |

### Poe Web Data Export

Poe may offer a GDPR/data export option in settings (similar to ChatGPT's "Export Data"). Not confirmed — check `poe.com/settings`.

## Potential Workarounds

### Option 1: Canvas App Exporter
Build a Poe Canvas App that calls `getDefaultChat()`, formats messages, and provides a download button. Limited to current chat only.

### Option 2: Browser Automation
Use Selenium/Puppeteer to log into Poe Web, navigate conversations, and scrape content.
- Pros: Full access to all conversations
- Cons: Login handling, anti-bot detection, high maintenance

### Option 3: Poe WebSocket/Mobile API Reverse Engineering
Poe's web and mobile apps use internal APIs to load conversation history. These are not documented and may change. Could be reverse-engineered but fragile.

## Sources

- https://creator.poe.com/docs — Poe Creator Platform documentation
- https://creator.poe.com/api-reference/overview — API Reference overview
- https://creator.poe.com/api-reference/createMessage — Messages API (Anthropic-compatible)
- https://creator.poe.com/api-reference/getPointsHistory — Usage History API
- https://creator.poe.com/api-reference/createChatCompletion — Chat Completions API
- https://github.com/ading2210/poe-api — Archived third-party library
