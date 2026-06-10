# 康康交付文档清单 — Known Structure

**Wiki Token**: `PLC2wV...anG5` (stored in navigate_wiki.py)
**Space ID**: `7636684753655319743`
**Node Type**: `docx`
**has_child**: `True`

## Document Blocks (as of 2026-06-03)

```
[1]  PAGE: "康康交付文档清单"
  ├── [51] SUB_PAGE_LIST (children=[])  ← 子页面在这里，但 children 为空
  ├── [4]  HEADING: "交付清单包含文件类型"
  │    ├── [12] BULLET: "沟通记录-文字版"
  │    ├── [12] BULLET: "财务检测表"
  │    └── [12] BULLET: "其他文档"
  └── [4]  HEADING: "进展说明"
       └── [12] BULLET: "2026年06月03日"
            ├── [12] BULLET: "沟通确认协议"
            └── [12] BULLET: "康康决定目前放下教练学习的需要"
```

## Key Finding: No Board Found

The document blocks do NOT contain any `block_type=43` (Board/画板) blocks.
The wiki children API for this docx node returns non-JSON (HTML error).
This means the 画板 may be:
- In a separate wiki node under the same space (not embedded in this doc)
- Accessible only via the Feishu UI's sub-page navigation
- A different content type than expected

## Access Pattern

When 康康 asks for the 画板:
1. First try document blocks → if board found, great
2. If not, ask her for the direct link — the API path is unreliable for this structure
