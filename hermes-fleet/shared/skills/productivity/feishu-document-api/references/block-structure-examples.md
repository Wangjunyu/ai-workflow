# Feishu Block Structure Examples

## Example: 康康交付清单 (PLC2wV49MiR9Nnkoc00clIUanG5)

Root document (`block_type: 1` = page):
- children: array of child block IDs
- page.elements[0].text_run.content: "康康交付文档清单"

Child blocks:
```
[51] block_type=51 (sub_page_list)  → wiki_token: PLC2wV49MiR9Nnkoc00clIUanG5
[4]  block_type=4  (heading2)       → "交付清单包含文件类型"
[12] block_type=12 (bullet)         → "沟通记录-文字版"
[12] block_type=12 (bullet)         → "财务检测表"
[12] block_type=12 (bullet)         → "其他文档"
[4]  block_type=4  (heading2)       → "进展说明"
[12] block_type=12 (bullet)         → "2026年06月03日" (has children: 2 sub-bullets)
  [12] block_type=12 (bullet)       → "沟通确认协议"
  [12] block_type=12 (bullet)       → "康康决定目前放下教练学习的需要"
```

## Block type reference
- `1` = page
- `4` = heading2
- `12` = bullet
- `51` = sub_page_list (contains wiki_token for child page listing)

## Example: 画板文档 (YmVtwq1PJiLjZLkdLqrc7YignBf)

raw_content returned: `"画板文档\n\n\n"` — effectively empty.
Likely a Bitable/Board type, not a text document. Use wiki node API to confirm.
