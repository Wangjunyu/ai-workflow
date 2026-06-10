# Board (画板) Discovery Pattern

Real-world example from 康康交付清单 session.

## Scenario
User asks for "画板文档" inside a Feishu wiki document. The document's `raw_content` returns nearly empty (just a title), and `blocks` API reveals the real content is an embedded Board.

## Discovery Steps

### 1. Document blocks reveal embedded Board
```json
// GET /docx/v1/documents/{doc_token}/blocks
{
  "items": [
    {
      "block_id": "YmVtwq1PJiLjZLkdLqrc7YignBf",
      "block_type": 1,           // page
      "children": ["doxcn...Gb", "doxcn...Td"],
      "page": { "elements": [{"text_run": {"content": "画板文档"}}] }
    },
    {
      "block_id": "doxcnyJMIGJN6VQk5RoGEhNGIDb",
      "block_type": 43,          // ← BOARD! 
      "board": {
        "token": "J1GmwmBV2hbGupbFpSrcWCahnMd"  // Whiteboard token
      },
      "parent_id": "YmVtwq1PJiLjZLkdLqrc7YignBf"
    },
    {
      "block_id": "doxcnqwUBsIKIV5254UDj1KWKTd",
      "block_type": 2,           // text (empty)
      "text": { "elements": [{"text_run": {"content": ""}}] }
    }
  ]
}
```

### 2. Board API attempt
`GET /open-apis/board/v1/whiteboards/{board_token}` → 404
Board content is often not accessible via REST API. The board token + document URL are the deliverable.

### 3. Wiki node info for context
```json
// GET /wiki/v2/spaces/get_node?token=YmVtwq1PJiLjZLkdLqrc7YignBf
{
  "node": {
    "obj_type": "docx",
    "title": "画板文档",
    "parent_node_token": "Rk6ZwVfn7ii17KkU5jGcWPaEnkh"  // OPC教练 wiki
  }
}
```

## Key Takeaways
- Block type 43 = Board/whiteboard
- `raw_content` empty → always check blocks
- Board REST API likely needs special permissions (not available by default)
- The Feishu document URL itself is sufficient for the user to view the Board
