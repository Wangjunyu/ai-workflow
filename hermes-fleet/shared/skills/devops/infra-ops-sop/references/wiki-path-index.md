# Wiki 路径索引

**用途**: 飞书知识库的节点路径缓存。需要定位某个人/某个目录时，先查此表。只在找不到时做实时 API 发现，发现后更新此表。

**更新规则**: 每次通过 API 发现新路径后，立即追加到对应 section。

---

## 知识库 Space 列表

| 知识库名称 | space_id |
|-----------|----------|
| C的旅程 | 7636692567408544990 |
| 人 | 7636684753655319743 |
| 商业实践 | 7636997977323670491 |
| 家庭合伙人 | 7636688541917056191 |
| AI宝典 | 7636675042419412190 |
| 自媒体输出 | 7636778878492511180 |
| 浚宇的分享-草稿 | 7641775683433565373 |
| 人生成长杠杆系统 | 7641892655059995853 |

---

## 人 知识库结构 (space_id: 7636684753655319743)

### 根节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 首页 | Xi3nwKUm6itSJCkxUgUcWMlunic | true |
| 朋友们 | F58lwOvCFid1FlkUtA8cAhMsnwg | true |
| 客户相关 | DcMiwjhT5iY4IokSxulcWYoBnSb | true |

### 客户相关 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 汤望霖 Lynn | AIjRwXudUizTKzkLJQncOEY5n6c | true |
| 关莲 | AzLLwrhIsiUNDwkFLZ2c3tX8nde | true |
| 魏玉洁 | Oj7swNMDViyat6k6v79cQrjvnIg | true |
| 徐正乔 | MFDKwCRzjiCBzakNXhMc1JBvn8b | true |
| 刘晓宇 | Fi5Dwjxk4iTJv2kEGANcg4cpn2e | false |
| **康康** | **XEL9wk9AOisOUXk8zywcRreInee** | **true** |
| 丁雅华 | Uks3wWAF7il4ZUkXvvycS5S5noQ | true |
| 李慧 | JqxFwJfYiizGXik6stjcXCWgnDb | true |
| 曾华青 | KFtbwYiV3iguHvk3dmYcP7h7nIg | true |

### 康康 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 康康教练对话-督导.xlsx | UUFIwZsYliBnj1kA5CPc71m9nyg | false |
| 康康交付文档清单 | PLC2wV49MiR9Nnkoc00clIUanG5 | true |

### 康康交付文档清单 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 康康-教练服务协议-协议版 | NaHvwTT4XiTUPekVFR5cpXQonZI | true |
| 画板文档 | WgaTw6iiFiHXnuktzaEcjkEanRh | false |
| 财务-家庭财务检测表-2026年06月01日-V2.xlsx | MjpOwDi2fit35vkhUV3cMcrknqh | false |
| 康康-家庭财务检测表.xlsx | AW2uwkHXei9Nkuk1w7Wc9CgVnZf | false |
| 康康-中日保险深度对比分析-From Deepseek | EcsJwMaljiMgJ5kOs7acspU6ncf | false |
| **会议记录** | **D9dLwrEP2iX8NfkcwEgcIFebnDe** | **true** |
| 康康-教练服务协议-协议版.pdf | X2ldwmbcMiRDkSklDgIciyUmn0b | false |
| 康康进展跟踪 | Ix4lwL6jri1EFdkG6xmcxE2WnLJ | false |

---

## 常用目标路径速查

### 妙记 → 知识库同步

| 人名 | 妙记存放节点 | node_token | 命名规范 |
|------|------------|-----------|---------|
| 康康 | 人 > 客户相关 > 康康 > 康康交付文档清单 > 会议记录 | D9dLwrEP2iX8NfkcwEgcIFebnDe | `YYYY-MM-DD 人名-标题` |

---

## 待补充

- [ ] 朋友们 下的 38 个人名节点（按需补充，不预先枚举）
- [ ] 其他知识库的结构（按需补充）
