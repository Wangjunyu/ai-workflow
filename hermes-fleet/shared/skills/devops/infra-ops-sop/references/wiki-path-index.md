# Wiki 路径索引

**用途**: 飞书知识库的节点路径缓存。需要定位某个人/某个目录时，先查此表。只在找不到时做实时 API 发现，发现后更新此表。

**更新规则**: 每次通过 API 发现新路径后，立即追加到对应 section。每天早上 6 点 cron 增量扫描「客户相关」和「朋友们」。

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

---

### 客户相关 → 子节点 (9人)

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 汤望霖 Lynn | AIjRwXudUizTKzkLJQncOEY5n6c | true |
| 关莲 | AzLLwrhIsiUNDwkFLZ2c3tX8nde | true |
| 魏玉洁 | Oj7swNMDViyat6k6v79cQrjvnIg | true |
| 徐正乔 | MFDKwCRzjiCBzakNXhMc1JBvn8b | true |
| 刘晓宇 | Fi5Dwjxk4iTJv2kEGANcg4cpn2e | false |
| 康康 | XEL9wk9AOisOUXk8zywcRreInee | true |
| 丁雅华 | Uks3wWAF7il4ZUkXvvycS5S5noQ | true |
| 李慧 | JqxFwJfYiizGXik6stjcXCWgnDb | true |
| 曾华青 | KFtbwYiV3iguHvk3dmYcP7h7nIg | true |

---

### 汤望霖 Lynn → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 协议沟通准备-Lynn | CjgvwoIuIi3at2k56C2cCNcZniH | false |

---

### 关莲 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 关莲-保险及资产配置方案讨论 | JFSawr332iYSSok5jDXcqWhtnDd | false |
| 文字记录：保险行业现状与业务方式讨论 2026年6月5日 | Rl94wKHQfiBqRYkOF32cUrLbnad | false |
| 赵学强 | OL4zwKmEGio6qskB860cILdNnwc | false |
| 关莲 智能纪要：保险行业现状与业务方式讨论 2026年6月5日 | JdaDwK1zjiqcGgkKJIfc10wNn17 | false |
| 关莲 智能纪要：保险规划及职业发展讨论 2026年6月5日 | NyLZwL4buiIfRgksthRcIMGYnJz | false |
| 关莲-沟通小结-20260605 | ReN6wY7TUi4LlrkZiGicCWrPnzx | false |
| 关莲-横琴保单.pdf | TYBvwCu6Hi5u7Mk5mVnciJ0WnFd | false |
| 关莲家庭保障分析-生老病死-V1 | Y0MDwfw9TiXImqkgyEWcMpNOnzb | false |
| 关莲的家庭保障分析报告_20260610111144 | KzFew97gWiwACwkJQdlcvCb5nWc | false |
| 关莲家庭财务全景分析-生老病死-V2 | PZZOwqGPai39kDkFfLlcDjUNnGh | false |

---

### 魏玉洁 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 玉洁交付清单 | RMlnwgkCniMmkskeNl1ceAWwnqh | true |

### 魏玉洁 → 玉洁交付清单 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 协议沟通准备 | DhT7wZ6ODi1xhBk3Dj3cD8gMndh | false |
| 玉洁沟通教练协议事宜 | DsxVweCBMighwQkz0KbcfqUFnKb | false |
| 玉洁-教练服务协议 | KTU8wU1viiigtukUM7Qc3Mu7n0c | false |
| 2026-04-20 玉洁沟通 | BPtXwdcDyi6M4ckVTsFcooJhnWe | false |
| 2026-02-10-玉洁_财务规划 | MEqnwXwYai5Ryjk7WHGcIY9Nnve | false |
| 20251223085906-转写_和浚宇的教练对话-逐字稿文本-1 | StIkw6CaHim8QwkbIjGcY2IZn5f | false |
| 20251231163347-转写_玉洁-生命探索-逐字稿文本-1 | I3zIwXgh8iRapRkM4t8c0ASPnqf | false |
| 20260107154213-转写_玉洁教练对话-逐字稿文本-1 | PsvXwArzriEJ3ZkA27Icfc65nae | false |
| 20260113154516-转写_玉洁-best year-逐字稿文本-1 | Ugwdwhm0Oim6Z4k7eJvcZbFhnJe | false |
| 20260115151714-玉洁 best year-逐字稿文本-1 | OxCqwn9MKio3TfkfwGMc3RiYnWf | false |

---

### 徐正乔 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 利率6.5%，心动啊... | XOA7wXpeIiTL8kkjHlnc9JxKnud | false |
| 正乔退休方案：世D悦享3 vs 大陆产品 · 全情景对比 - 考虑通胀的版本 | NcwBwbrBFiUun7k0WNYcJ1Awnib | false |
| 小乔同学退休方案：世D悦享3 vs 大陆产品 | MME3wYGX0ifa0Gko5FUcXuyKnSf | false |

---

### 刘晓宇 → 子节点

*(无子节点)*

---

### 康康 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 康康教练对话-督导.xlsx | UUFIwZsYliBnj1kA5CPc71m9nyg | false |
| 康康交付文档清单 | PLC2wV49MiR9Nnkoc00clIUanG5 | true |

### 康康 → 康康交付文档清单 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| **康康-教练服务协议-协议版** | NaHvwTT4XiTUPekVFR5cpXQonZI | **true** |
| 画板文档 | WgaTw6iiFiHXnuktzaEcjkEanRh | false |
| 财务-家庭财务检测表-2026年06月01日-V2.xlsx | MjpOwDi2fit35vkhUV3cMcrknqh | false |
| 康康-家庭财务检测表.xlsx | AW2uwkHXei9Nkuk1w7Wc9CgVnZf | false |
| 康康-中日保险深度对比分析-From Deepseek | EcsJwMaljiMgJ5kOs7acspU6ncf | false |
| **会议记录** | D9dLwrEP2iX8NfkcwEgcIFebnDe | **true** |
| 康康-教练服务协议-协议版.pdf | X2ldwmbcMiRDkSklDgIciyUmn0b | false |
| 康康进展跟踪 | Ix4lwL6jri1EFdkG6xmcxE2WnLJ | false |

---

### 丁雅华 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 雅华交付清单 | PYakwBbjoiZtBQkUnLFcy1VTnmf | true |

### 丁雅华 → 雅华交付清单 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 雅华-教练服务协议-已结束 | F8W6wTagSi0UGtkJcbzcykitnCf | false |
| **丁雅华-教练交付-沟通记录** | Vwc5wRFVhiTGuxkEIFncP60qneh | **true** |

---

### 李慧 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 李慧家庭财务-风险部分-2026年04月21日 | PGOtwuoZ3iyAtOkjW8kcaYgVnYc | false |
| 李慧家庭财务-风险部分-2026年04月21日.pdf | GwHjw4sD7iE1GqksdyHcAsCLnvb | false |
| 沟通小结-慧姐 | IIQzwEuaOiJLpVkVoG3cfgs4nnc | false |
| 李慧方案准备-2026年05月25日 | H13ew1MP6ilwISkIx6ic9WtPnbc | false |

---

### 曾华青 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 附近森林项目反馈 | LW40wTgzbiLuf2kj9Qacx5r1nMh | false |

---

### 朋友们 → 子节点 (38人，仅1层)

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| **李博** | URyhwU4PPiO09ak1UM1cbvuXnVh | **true** |
| 王秋云 | JDZbwz7jxiNbUMkrIdgcnRk3nIG | false |
| GG | FyHnwobfhiiIc0kKXHacwvURnag | false |
| 韦德华 | Z9EhwNzFfiP4jCkOYuTcuhTJnUg | false |
| 朱敏 | Ddoawuz5YiDRAykhm4Qckc6CnMd | false |
| Michael | EkfPwpdhAiO6QTkWcT0cZIYVnrb | false |
| 谢新源 | Tw0BwAeJJiHc8bkuDWLcQx31nYc | false |
| 刘凯 | P3F1wnziHinGsck84odcQjswn2g | false |
| 赵红丽 | ETdWwJQkHi658zkcqHKcaPiCnII | false |
| 黄文艺 | EdKJwMhWEibiTrkP0NZcFAkCnh0 | false |
| **Erin艾琳** | QtJowwdA6ipsPRkzqWwcaWefn3K | **true** |
| **佳佳** | YvwawNcKniSnsBkodqFch7mpnvX | **true** |
| 宋荔斯 | E8Egw7sv7iheODklzTScwPqGnTg | false |
| 夏雪 | Oz54wP6Hoi7ipAkFmvbcOjcRnt0 | false |
| **朱训兰** | L6yAwCbzQiCJsskAyUBczAJlnvh | **true** |
| 罗惠方 | X9K0w6fx3itPhAkleGZc5qW3n6e | false |
| 蒋艺婧 | UFCAwRSYPiNrYXknTVvcJesbn4e | false |
| 谢伊璇 | HeqpwbhqGi22BBkaRFVcsXmKnVc | false |
| 阴玉双 | D9mkwW7l5iAXcUkzW1wcYdlKnub | false |
| **陈妮** | FDs5wmaKIiSQbSk27oGcJBLKnPf | **true** |
| 杨立 | RblwwIGLNibmRQkGQn8cUaMQnxh | false |
| 朱凡 | VSH0wgo90iqr62kVvnFco43xnbf | false |
| 孔明 | TKndwHWcYiBkDMkSBr9cUGdsnac | false |
| 杨鑫 | Ooj4wGywLiGinIksYmScLw40nVd | false |
| 项士烁 | XJkHw50vHiIVYekMPl6c9VrZnvh | false |
| 罗殷宇晴 | AlYTwNfnViwNiakbz0bcgHLVnng | false |
| 孙彦玲 | UnP6wXGKEiX20skHSrycO1KZn6c | false |
| 杨静 | Dv0nwyUFCigxmLk7CATcLQHJnke | false |
| yoyo | XUA5wAH9jik9OdkuKHhcXppdnXe | false |
| 晓明 | A9fywH8Qhi8p58kGBOAckYR6nhg | false |
| 山雯 | EPsowJoHriEG8okVW0vcWhBMneh | false |
| **余了了** | BH4hwzxnpik3ChkmrkccIYjOnRh | **true** |
| 张敏立 | BwmywG321i64YRkV7nFcKpoxned | false |
| 何水 | BRFPwwvl5it2WEkeW65cEfWynsd | false |
| Harry 皓同学 | C26HwqnkniI44NkUHSTce8GmnJd | false |
| 邱楚 | BxQxwmfYYiO36ZkbuomcmEp5n2y | false |
| 王永澄 | MWe9weyxeib07BkKKO7cZ0hPnod | false |
| **陈悦** | KkqpwlHGcihkT0kIM52cTGu1nMf | **true** |

> 7 人 has_child=true（加粗标记），未递归深入。后续增量扫描会逐步展开。

---

## 常用目标路径速查

### 妙记 → 知识库同步

| 人名 | 妙记存放节点 | node_token | 命名规范 |
|------|------------|-----------|---------|
| 康康 | 人 > 客户相关 > 康康 > 康康交付文档清单 > 会议记录 | D9dLwrEP2iX8NfkcwEgcIFebnDe | `YYYY-MM-DD 人名-标题` |

### 其他已知的「会议记录」类节点

| 人名 | 路径 | node_token（待确认子节点） |
|------|------|--------------------------|
| 康康 | 康康交付文档清单 > 会议记录 | D9dLwrEP2iX8NfkcwEgcIFebnDe ✓ |
| 丁雅华 | 雅华交付清单 > 丁雅华-教练交付-沟通记录 | Vwc5wRFVhiTGuxkEIFncP60qneh（has_child=true，待展开） |

---

## 待补充

- [ ] 康康 > 教练服务协议-协议版 (has_child=true)
- [ ] 康康 > 会议记录 (has_child=true，已知深层节点)
- [ ] 丁雅华 > 教练交付-沟通记录 (has_child=true)
- [ ] 朋友们 下 7 个 has_child=true 的人名（李博、Erin艾琳、佳佳、朱训兰、陈妮、余了了、陈悦）— 待 cron 增量扫描逐步展开
- [ ] 其他知识库的结构（按需补充）
- [ ] 各人物目录下的「会议记录」路径（待发现后完善速查表）

---

*最后更新: 2026-06-11 — 全量扫描完成：客户相关 9 人（2层深度）+ 朋友们 38 人（1层）*
