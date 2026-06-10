# 康康交付清单 — Document Structure

Token: `PLC2wV49MiR9Nnkoc00clIUanG5`
URL: `https://rcnsiaef7x5y.feishu.cn/wiki/PLC2wV49MiR9Nnkoc00clIUanG5`
Parent: 康康 wiki 主页 (`XEL9wk9AOisOUXk8zywcRreInee`)

## Document Content (raw_content)

```
康康交付文档清单

交付清单包含文件类型
沟通记录-文字版
财务检测表
其他文档
进展说明
2026年06月03日
沟通确认协议
康康决定目前放下教练学习的需要
```

## Block Structure

| Block ID | Type | Content |
|----------|------|---------|
| PLC2wV49... | 1 (page) | "康康交付文档清单" |
| Sv9Ld6BR... | 51 (sub_page_list) | wiki_token=self |
| DJkBdbJO... | 4 (heading2) | "交付清单包含文件类型" |
| HoSodxxR... | 12 (bullet) | "沟通记录-文字版" |
| PUFcdvfb... | 12 (bullet) | "财务检测表" |
| HyhedNK9... | 12 (bullet) | "其他文档" |
| OsWfdi03... | 4 (heading2) | "进展说明" |
| S2Tjdba7... | 12 (bullet) | "2026年06月03日" (has children) |
| TmSbdsDo... | 12 (bullet) | "沟通确认协议" |
| IcCndaOL... | 12 (bullet) | "康康决定目前放下教练学习的需要" |

## Confirmed Sub-Pages

| Name | Token | Type | Notes |
|------|-------|------|-------|
| 画板文档 | WgaTw6iiFiHXnuktzaEcjkEanRh | docx (embeds Board) | Board token: OVIywsH5vh2clEbFMKXcKnfZnXA |

## API Dead Ends

- Wiki children API (`/wiki/v2/spaces/{space}/nodes/{token}/children`) → 404 for this docx node
- Space-level node listing → returns empty
- Sub-page enumeration via blocks → block_type=51 exists but child tokens not exposed

## Discovery Method

Sub-pages can only be found by:
1. User providing the direct link
2. Obsidian wiki sync (feishu_wiki_sync.py via lark-cli)

Last updated: 2026-06-03 (after 画板文档 lookup session)
