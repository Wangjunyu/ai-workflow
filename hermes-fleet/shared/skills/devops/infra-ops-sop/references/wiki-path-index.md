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

### 首页 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 人员清单 | R2hnw298AihV7ekd05xc9mMBnfg | true |
| 我的2026-人.xlsx | AROqwQ0CMiQhh7kdlOxcZF8gnah | false |
| 客户-客户档案汇总 | QjsdwRV4viiHeekcAyacqCtenWh | false |

### 人员清单 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 人员清单更新日志说明 | GaYPwhIyKiiVPpkuqETcCLkinXf | false |

---

### 客户相关 → 子节点 (15人)

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
| 陈悦 | KkqpwlHGcihkT0kIM52cTGu1nMf | true |
| 陈妮 | FDs5wmaKIiSQbSk27oGcJBLKnPf | true |
| 李博 | URyhwU4PPiO09ak1UM1cbvuXnVh | true |
| Erin艾琳 | QtJowwdA6ipsPRkzqWwcaWefn3K | true |
| 佳佳 | YvwawNcKniSnsBkodqFch7mpnvX | true |
| 邹易 | IOEOwpB46iyzIvk2YuhcwZlfnSe | true |

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
| 关莲家庭生命周期表 | HJ6QwL6xziAJSok2qm4cprsun9R | false |
| 关莲家庭财务全景分析-Final | YFVwwThcui0Oiyk0rZ4cZtCZn1B | false |
| 关莲沟通小结-202606 | Fwk2w5oEFiUO7Fkc2gdcnX3ln4n | false |

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

### 康康 → 交付清单 → 教练服务协议-协议版 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 康康协议修改说明 | BayzwZ0qzi9l9RkrRHtcOPJnn0g | false |

### 康康 → 交付清单 → 会议记录 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 2026.6.10 康康-3个月陪跑目标沟通 | UQ0XwGZhPiXiEjkJjZccvslynje | false |
| 2026-06-03 康康 教练协议沟通 | YVSRwIG1GioxRIkJmQ4cwT6anCb | false |
| 2026-06-01 康康-教练&财务沟通 | EIg7wIEbIiFOCekLxgicCFpInZg | false |
| 2026-05-24 学了教练之后，你有哪些变化和顾虑？ | RzICwetckiIPYKkKBOLcVnkhn1c | false |
| 2026-05-23 康康-财务规划交流 | Xi0RwtXotiWviKk4zgWcAUbgn1f | false |
| 2026-05-14 康康-交流AI&教练&财务规划 | D99ywSSlfitOLNktpc8c3Yflnrb | false |
| 2026-05-09 教练对话-客户康康-教练浚宇 | EdshwfxdJiWNf5kjvFncSZbmn3b | false |

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

### 丁雅华 → 交付清单 → 教练交付-沟通记录 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 智能纪要：雅华 教练对话 2026年5月9日 | Z165wvWoWi7OQAkFOwWcPVRjnPe | false |

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

### 李博 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| Tapon: A Manifesto | Lo4OwfEVIiBBJTkkslgcRYaznYg | false |
| Tapon许愿池 From 浚宇 | GByqwZXqliY54IkpyjPc7WcHnNd | false |
| tapon-shiyong-tiyan-ji-gongzuoliu-guihua | ENGyw6nNfiQCVFkf7dwcweYfnwf | false |

### Erin艾琳 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| Erin-后来之地讨论 | Es36wv7hMi0mVBk9tt1cbBZxnJg | false |
| Erin-教练服务协议 | THfUwOfRXibZewkHaSfcS01vnGf | false |

### 佳佳 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 佳佳-教练服务协议 | GEQVwcxSnitZ35kMDU3c4rkMngf | false |

### 邹易 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 邹易 家庭保险规划 Intake 2026-06-10 | RJIVwTjlEiMsjnkM3vhcnuONngd | false |
| 邹易-保险咨询待办事项 | YAIXwoTAFiybSykUlfpcuJHGnnf | false |
| 邹易家庭保障沟通小结 | RIJtw7NLOipMEmkocgIclzLWnrb | false |

### 陈妮 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| Sammy需求沟通复盘与后续服务设计 | M3fSwuOvViyD4ekh5HdcP2Hvn2c | false |
| Sammy-需求沟通 | AEBHw9qdGiaOsxkiTMVc6f3GnRg | false |

### 陈悦 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 沈磊保单利益整理表20251225.xlsx | QJltwzh7bitRRHkbVYZcxacTnfV | false |
| 陈悦家庭财务规划-风险分析 | OGoDwKS9MiKUyzkYhAEclWx1nNb | false |
| 卡卡聊保险需求 | NXcVwWUtQithgykyF37csqIWn1g | false |
| 卡卡沟通小结-微信版-2026-06-05 | DE8dwsWvXiamS6kYbFdciJSrn51 | false |

> 6 人 has_child=true（李博、Erin艾琳、佳佳、陈妮、陈悦、邹易），已全部展开到叶子节点。

---

### 朋友们 → 子节点 (33人)

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 王秋云 | JDZbwz7jxiNbUMkrIdgcnRk3nIG | false |
| GG | FyHnwobfhiiIc0kKXHacwvURnag | false |
| 韦德华 | Z9EhwNzFfiP4jCkOYuTcuhTJnUg | false |
| 朱敏 | Ddoawuz5YiDRAykhm4Qckc6CnMd | false |
| Michael | EkfPwpdhAiO6QTkWcT0cZIYVnrb | false |
| 谢新源 | Tw0BwAeJJiHc8bkuDWLcQx31nYc | false |
| 刘凯 | P3F1wnziHinGsck84odcQjswn2g | false |
| 赵红丽 | ETdWwJQkHi658zkcqHKcaPiCnII | false |
| 黄文艺 | EdKJwMhWEibiTrkP0NZcFAkCnh0 | false |
| 宋荔斯 | E8Egw7sv7iheODklzTScwPqGnTg | false |
| 夏雪 | Oz54wP6Hoi7ipAkFmvbcOjcRnt0 | false |
| **朱训兰** | L6yAwCbzQiCJsskAyUBczAJlnvh | **false** |
| 罗惠方 | X9K0w6fx3itPhAkleGZc5qW3n6e | false |
| 蒋艺婧 | UFCAwRSYPiNrYXknTVvcJesbn4e | false |
| 谢伊璇 | HeqpwbhqGi22BBkaRFVcsXmKnVc | false |
| 阴玉双 | D9mkwW7l5iAXcUkzW1wcYdlKnub | false |
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
| **余了了** | BH4hwzxnpik3ChkmrkccIYjOnRh | **false** |
| 张敏立 | BwmywG321i64YRkV7nFcKpoxned | false |
| 何水 | BRFPwwvl5it2WEkeW65cEfWynsd | false |
| Harry 皓同学 | C26HwqnkniI44NkUHSTce8GmnJd | false |
| 邱楚 | BxQxwmfYYiO36ZkbuomcmEp5n2y | false |
| 王永澄 | MWe9weyxeib07BkKKO7cZ0hPnod | false |

> 0 人 has_child=true，全部为叶子节点。API 确认朱训兰、余了了返回 0 个子节点（2026-07-02 增量扫描验证）。每日子节点全部 has_child=false，后续无需重复枚举。

---

## C的旅程 知识库结构 (space_id: 7636692567408544990)

### 根节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 说明 | WaLQw4XKpiJzICkZAnEcJ3S4nQh | false |
| 2026年6月-7月开学典礼 | Lidkwh1pViusJJk0uY9cjDSWnSb | true |
| 北京C9见面会-2026年6月 | MHQ5w8a4rid3Yek0s7kcBkkPnlg | true |
| C9旅程-之前记录-2026年05月06日 | W17Ww2Xo6iX1fFkd6qpc7eAfnmf | false |
| 面聊招募汇总-2026年3-5月 | TPQcwsFEGiLgPfk0GX6chhuznPe | true |
| 自我介绍-浚宇 | IkOHwa5YliDRsmkOtlkcpymZnOf | false |

### 2026年6月-7月开学典礼 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 制作调研问卷文本-2026年06月09日 | VtXawiI53iD8TWkuH5yc5QYlnGh | true |
| 9.0开学典礼筹备组招募问卷 | P1BEwmXT2iB0prkxjWScfkZmnye | true |

### 开学典礼 → 制作调研问卷文本 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 9.0开学典礼筹备组招募问卷-V0.1 | ODvSwGSxCiyGwnkRPsPcT2SPnng | false |

### 开学典礼 → 9.0开学典礼筹备组招募问卷 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 宣发组 | VEdcwmJFciuVWyk043Uc19Nfnwc | false |
| 总统筹直辖 | XC8hwLs7ni8SZMkeJSpcZR34nre | false |

### 北京C9见面会-2026年6月 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 北京新生见面会（6.6）任务表 | Adf1wJd62ikQxEkieoec30p3nCc | true |
| 0606北京新生见面会_总统筹表 | Lz1wwEj1iiHtEyk6dD0cOCpqnXe | false |
| 0524新生会筹备会议纪要 | F5oVwcDgci8F7akk7r1ccN1zn6c | false |
| 20260530175649-9.0线下见面会-筹备会3-逐字稿 | XvdEwiLZEibtRykoXvvcpdo7nPf | false |
| 北京C9.0新生见面会主持稿 | UF00wrvLfioDZHk2zrOcvTninUd | false |
| C9.0 北京线下新生见面会 · 主持稿 | Mo7YwGk2TigVVOksBfIcDQ9Hnrg | false |

### 北京C9 → 任务表 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 北京新生见面会（6.6）任务表 | WTPswi2OJi242ekzpCxce8dNnPh | false |

### 面聊招募汇总-2026年3-5月 → 子节点 (21项)

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 招募-我的推荐 | YaJdwPNZ9ilzeNkVHdJcnSjHnlR | false |
| 我参与的面聊 | HPU8wya27i61cNkX8x3cvkYpn3e | true |
| 面聊PickUP | JyZ1w9ezCilug5kYn8ockpmmnge | false |
| 中台问题库 | K3Q6wqh5kijJiIkRXiHcqeJ0nCg | false |
| C9发起人见面会.pdf | BpwUwV96niOCE5kZQREcCYVUn4e | false |
| C9全国招募-发起人培训会0401-专毅.pdf | G5jGwByr7iX3ozkJn1LcOAATnfd | false |
| 招募海报-2.jpg | U5RUwPDw7irFEnkuocScixBcn0c | false |
| 招募海报.jpg | Bruuww4aIiWFfAkXh9CcCalGnDe | false |
| 组织简介.jpg | XajzwWS9Sibo3RkyY9vcEAODnhf | false |
| 9.0前台面聊话术SOP参考.xlsx | SNqKwbBRsiHAPLkHPf1cc8T4nnb | false |
| 9.0约聊记录模板_前台-候选人.docx | GSKQw2kOIiWdFfkmgOecnSSZnZg | false |
| 9.0约聊记录模板.docx | Kb6Uw9WRdizcT9krRPxcG44Knle | false |
| 面聊-AI相关 | O7qGwBEBMihx9nkGOEVcMpzUnqf | false |
| 输出: 面聊之旅对我的启发 | SXhUwj9SpihPaLkkeSOcAYSFnbe | false |
| 输出: 其他内容 | B5JIwq4hzieQmuk5SEPcpN3gnKf | false |
| 花名 | ESoTwnvg0iiYwVkzXFzcIylPnjd | false |
| 9.0约聊记录模板_前台-候选人 | LoSuww9cLikpnfkicIRcBW4Sn5f | false |
| 前台异议处理 | LwhCw3I5hiChEaku0sJcp69anIT | true |
| 立方有约 | M4GDwHCGYioWS8kbJQ6c2pMOnDd | true |
| 面聊复盘 | UvULwmDEIiiDMCkUy9GcDCXQnVg | true |
| c9加油站-0522-发言文字稿 | SiYzwRcPTiM8vnkOiMNcLdpwnrh | false |

### 面聊招募 → 我参与的面聊 → 子节点 (32人)

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 北京-赫蕊-辅聊-5.13 19:00 | SFZNw02pziNrNAkDMX1coAalnMe | true |
| 福建-陈缘圆-辅聊-5.13 10:00 | DqnJw27ZwiisKykyNehcnFrUnHg | true |
| 四川-纪拓-主聊-5.12 16:00 | B0mRwp41AimH7EkItzec8nFanMc | true |
| 四川-钟银华-辅聊-5.9 12:30 | Vci3w0iXwiI1hKkcgu9cEpBlnp2 | false |
| 深圳-崔梦梦-辅聊-5.8 20:00 | Rd6GwbL8ciek0bkSkqccyCGUnfe | true |
| 重庆-黄蓉-辅聊&记录-5.8 16:00 | MHBfwKAV2ifMGxkpWHQcfQqVnff | true |
| 北京-周泽鑫-主聊-5.8 14:30 | IPj9wAXqHioRTZka4w7cNRV1nLh | false |
| 福州-徐慧敏-主聊-5.8 13:00 | W25kwDQXZifYstkXTm3cFM9ZnUd | false |
| 北京-曹瑞芳-主聊-5.7 15:30 Done | UCLbwt27Bii2sskpU4kcvQQ0nFe | true |
| 北京-田子玄 | XJgxwy6iZiVeWSkG0GucAvdVnUd | false |
| 杭州-张翼 | CeqowsAfoimtAakFw1ZcJlGgneh | false |
| 北京-姜沣桓 | I4wQwACvgiVgZmkjSBgcP8eKndc | true |
| 北京-马群慧 | ETP8wfO8ZisdrZk3Hc6c6x7rnwf | true |
| 北京-陈岩 | UMmrwrqWFilS84kMM5bcejajnGc | false |
| 北京-王珂维 | OXyuwuIAKistD7kDt93cOejgncf | false |
| 北京-于硕鹏 | UAo7wavuXiZTIvkwKhocxymSnnb | false |
| 北京-王天宇-未参与 | Omc8w4rxgi07tXknMH7cexzxnFe | false |
| 北京-Tracy-未参与 | LKrgwKCxciUVMCkMEuTckhaynVW | false |
| 刘红颜 | EFbMwSsM8ixmdpkTQgscOCA5nvb | false |
| 北京-张雅芃 | SBQGw8sldiSWTRkg4ZZcHgV2nvc | false |
| 柳菁铧 | NlXjw3x0RiiUijked0qcLeXDnlh | false |
| 昆明-芶知晏 | VAkGwjxbRialz2kGjsRcUw3bn4D | false |
| 北京-王珂 | BuZZwfIzCiw1RNkBKZ7cDXGZnCf | false |
| 北京-王贵锋 | CVOwwefpNiQkjYkol4acUT4LnYV | false |
| 北京-杨坤 | SmuNw0YNpiZ3d8kbQS0c4pJCnqZ | false |
| 北京-李奇亮 | B9YlwWCI7iItOlk2lkWc12j5nmf | false |
| 南宁-潘颖欣-4+2 | JRfawnIAGiffBWkvY8ocR26pnrb | false |
| 山东-李玉康 | E4RzwgDYhi7GAakeSTHcOHGEnWf | false |
| 北京-田金荣 | OQ9RwnyvfixjJmkXmGfciBCungh | false |
| 北京-郭五新 | Y2EDw9kczia8BDk5TnhcD1AjnNd | false |
| 董董 | Uk4qwS9L5i5MvskV4BkcF6zEnYK | false |
| C9附件-共享资料 | HkEZwVhLximgx6k3qYmcSsk6nBd | false |

> 8 人 has_child=true，已到 2 层深度上限，未继续展开。

### 面聊招募 → 前台异议处理 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| C9.0前台异议处理小组工作要求 | K8n0w5T9TiptwokgzOCc1Dalnrg | false |
| 前台（候）异议03沈阳-彭雪-不通过 | ForEw1nxliZaDgkiHnPcKAaDnIg | true |
| 前台（候）异议10天津-张颖-通过 | W7k2wKJosi75HkkWSnOc2YuSn1e | true |
| 前台（候）异议12杭州-罗彤-通过 | JpXlwYbOiHWM1k7CNBc5jiHn6b | true |
| 前台（候）异议04新疆-宋昭霖-通过 | XBlvww553i85BwkXFPZczohanLg | true |
| 前台（候）异议15-长沙-梁羽佳-不通过 | ZiALwrxfiieGLqk9zhJcYCKTnHg | true |
| 前台异议V19_深圳-彭林-通过 | MX1FwtTWJiPnyKkFPRTchdhGnFg | true |
| 前台异议18-南昌-徐佩青-不通过 | BvaZwvtu1i6i5FknTNsczTmBnRb | true |
| 前台候选人异议22宁波-不通过 | AoY3wAuzeiM3BgkUK1Zcc5btn4d | true |
| 前台候选人异议23南京-不通过 | ZRUxw6trSiuKGtkwrK5cTOUVnqb | true |
| 前台候选人异议-最后一单-通过 | EHqywNFyki8Q1BkVEW5cC7Nlnxc | true |

> 10 个 has_child=true，已到 2 层深度上限，未继续展开。

### 面聊招募 → 立方有约 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 立方有约9.0新 v5 | Oae4wbjE4ivKSCk3DzncoVsBnNe | false |
| 立方有约9.0新 v5.pdf | RklzwY9iOis8n0kw3Zfc0YPFnOg | false |

### 面聊招募 → 面聊复盘 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 以聊为镜，见人见己-南通安杰 | XLndwQ3kWiQXjQkiLlCcnrZNnKd | false |

---

## 商业实践 知识库结构 (space_id: 7636997977323670491)

### 根节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| OPC教练 | Rk6ZwVfn7ii17KkU5jGcWPaEnkh | true |
| 我的客户 | Vi5DwspIPibFrqkidLUcl15gn0c | false |
| 后来之地 | CHoPwx6pjiOeQgkvYuVcgnSMnTb | true |
| 保险业务 | AXFxwLyHIiVtNpkX24FcjjEKnpd | true |
| 壹志团队 | X63vw5qvoiNw11kbWVNcVQisnwc | true |
| 教练之旅 | SYTZwkbZjibh4Fk5oxecOcB9nvh | true |
| 家庭财务 | KDFqwJZB8i0iiHkpZe5cZmTQnng | true |
| 归档项目 | I0hbw5rVViWY8Uk34UmcgLYunMc | true |
| 实体公司 | X3ljwuMs8iTlnOk973KcMHORnKg | true |
| 社群学习 | GrNEweMtKitobOk6tkhcopr9n8c | true |

### OPC教练 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 他山之玉 | HeZrwGtgjiyxozk3u13co1XSnMb | true |
| 画板文档 | YmVtwq1PJiLjZLkdLqrc7YignBf | false |
| Floria X 浚宇 第二场｜妙记洞察与行动建议 | JGrjwYt3Di5HOqkbMmdc6wjPnUa | false |
| 2026-05-13｜家庭财务规划与 MVA 对话记录 | VOD4wGrc1iXBtZkvaJUc2PAGn4c | false |
| 赵立心【IP创业500人峰会】参会手册 副本 | KmL3wWpghi9mmLkDG9gc8eHZnbc | false |
| 给老客户的一封信 | XXZOwQioFihC38kbMEvcAi3ZnTh | false |
| 教练课程体系深度分析与完整方案 | XGZxwdRZHioQmlksM6kcfiJ7nff | false |
| 教练课程体系三模块方案-理论整合版 | NJuQwC7miiDzpKk5GNZcKd31nNk | false |
| 2026教练培训 | EZ5Yw88jmiqnREkyIBucdkLSnlh | true |

### 后来之地 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 百万俱乐部 | U6wtwWvvSicQK4kJbZucHcc8nyh | true |
| 自我探索资料包 | Smu3wdfwviDk88k8T5DcM9y2nAf | false |

### 保险业务 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 杨立工作安排 | B0o4wuRmniHqrwkRXMNcydebnfe | true |
| 明亚主管 & 壹志团队 | TxegwjekMiEqf5ksYihctiepnKc | false |
| TWS分享准备 | JZOVwecxcias4LkAGh7c2DWln3b | true |
| TWS文稿（2025.12.15） | QV4CwPPvEi6LTjke9Vdc6Ka3nre | false |
| TWS备课-From马向文-2026年05月08日 | Vk1pwESFSiz0hqkQCWzcv96Xnah | false |
| 续期扣费追踪 | JAdSwOgauiFDfKkLb3cc0qr9nXf | false |
| 业务-按月出单情况.xlsx | TUbrwxU0giKMQnkB9Aac0J1rn9b | false |
| 他人培训 | Wq6zw8W3Hip5ZXkY3u4cJwsWnTf | false |
| 保险经纪人优势解析 | PLfxwbCbsiIFEmksEyJcSHHbn3g | false |

### 壹志团队 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 外购药专题内训 | KDOEwm5l4ihr9DkYf29clC6vn7e | false |
| 过往归档 | NHlIwtEOhiJwufksCewcE5snnDg | true |

### 教练之旅 → 子节点 (15项)

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 2026年05月06日 浚宇教练督导 教练康康 客户颜新秀 | JepIwRR7XiKHCbkuyBEc3cYHnzd | false |
| 教练对话-客户康康-教练浚宇 2026年5月9日 | SYf0wXTc0iXBK7kGvZ8cgNbjnLb | false |
| 学习小组实践2025-2026 | HlXtwdg4nifXLrkp7JJcGR7Yn8b | true |
| 学习培训记录和计划 | LolNwWXgsijj7NkHE8XcvqRAnyh | true |
| 教练AI场景 | Rp8UwvhvLiiU9Qk5khWc41gWn5e | false |
| 教练记录 | EwkYwQ4fdiMD0nkCAJUcwLJwnMc | false |
| 我被教练 | J6bPwCMMNiwgMSksoKScW9OOnLd | false |
| 教练客户说明 | MvA0w0wEiiKSUwkHlcwcHyOGnNe | true |
| 教练合约模板 – 个人教练 | TC21wMl8zijhmfkCFQzcYVOQnjf | false |
| 教练小时数记录表.xlsx | A0LIwKJeXisgCykhk60c2Ridn9f | false |
| Harry 畅聊 AI｜妙记洞察与行动建议 | MNm2w4op5iPgDCkgfZkcEEcinfA | false |
| ICF教练商业化实践指南_明哥.pdf | XJ2xwpyO2i2QtnkUOwIchblynad | false |
| MCC大师录音拆解学习 | Q7gcwTfHKi0O7kkWJRicFIEVnBe | true |
| 浚宇-介绍-v0.3-2026年05月29日.pptx | WLo7wnydEicXKXkE9ERcSoq7nxe | false |
| PCC笔试 | W3yywChp5i72n6k1K28cAUpPnMg | true |

### 家庭财务 → 子节点 (13项)

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 模板汇总 | LFNRwVCTXi95MSkMZbNcESt6nVc | true |
| 收入整理.xlsx | AmlzwBiMji9FHXkV8hFcWvIjndF | false |
| 收入支出表.xlsx | XCSxw0LroiVkVMkYD1pcvfylnwn | false |
| 搞钱研究社 | QxR3wO0TsiEbVDkt0pScyYRnnjC | false |
| 业务-展示-财务规划-风险部分说明-打印简版 | MmO0wTFuSi0vzokvREqcCLWInHb | false |
| 业务-展示-财务规划-风险部分说明 | YdFEw8P0wiVEuQkVe72cz6opn7g | false |
| 业务-展示-财务规划-一页纸版本 | PVIrwJukGi2htskGgaDcI7ysnKn | false |
| 业务开展思路 | Gdccw5xgqiDcvRkKfoWcs7pynTh | false |
| 业务-展示-财务规划-风险部分说明-PDF | XvM3w0fesidYZKkvE1hczmJQnbg | false |
| 业务-展示-财务规划-一页纸版本-PDF | Cw8MwWF3JiPSc9klTN5chOiDnhh | false |
| 业务-方案展示与反馈汇总 | Ma92wZ6c3im8ylkJlHQc2blzn1f | false |
| 客户-家庭财务规划的话题切入 | Bj5SwX4KxiIZVjkILlFckmNSnLg | false |
| 客户-沟通案例集 | T6EKwChxwitSZQkZs52cMBmAnVh | false |

### 归档项目 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 彭慧琼的会富项目归档 | OD0TwEm2eilGlYkH3BCcC5h3nIe | true |

### 实体公司 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 早日退休科技有限公司-相关材料 | CdiTw3q2li64O8kTinLcohbxnxb | false |

### 社群学习 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 开智学习 | Fw75w2oyOijSzVkppKuck1bHn7g | true |

> 商业实践 has_child=true 的深度2节点（共14个）标记待后续增量扫描展开。

---

## 家庭合伙人 知识库结构 (space_id: 7636688541917056191)

### 根节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 家庭 | X9Q8wrXrii98fNkhiU9cxm6Tn3f | true |
| 2026家庭报告 | MjfSwB0xOipw7Qkl4qnc3Kynnob | true |
| 2026相关领域 | FxUcwWHlPilY45kT8CJcGAkvn9c | true |
| 2026年5月报告 | ZY1xwFmBBi51i1kVZJIcV8UHndJ | false |

### 家庭 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 一五计划制定进展 | J8kbwoGVUi1rgck6iDQcPkPrndc | false |
| 2026复盘 | TTqBw1eTPiua20kkagrcn1ffnoe | false |
| 向爱人看齐 | EaqDwIWLliNpUXk3PDUcAXN8nFd | false |
| 王孟瑜成长记录 | JwWOwjcCMimScRk4wMYcafMUn8f | true |
| 关于父母 | XzTSw6wZgiXHJukQjoNcrQMhnde | false |
| 破冰行动 | RYG9waNZziLzSMkCsamcJ6E9nHS | true |

### 2026家庭报告 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 2025及之前的家庭报告 | W4mxwKtIriAM58kxVmWcEv0Wn8n | true |
| 2027待办想法 | Z7Pww7qe3iFy3jkI76vciyMYnYd | false |
| 浚宇2026记录 | RYzGwr1UCiV08XkR8FtcXmkLnJd | true |
| 家庭财务规划 | RoK4wPMp3iYJz7kaEijcVpFInzY | true |

### 2026相关领域 → 子节点 (13项)

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 待听内容清单 | BVtcw1VHFiafYlkC4Mpcd0eLnYe | false |
| 认知升级 | EzbhwOBOmiBIlmk3m8Rc8J53ned | false |
| 自我介绍-浚宇 | KlRqwpcV0izUgWkcpqgcWG0Rnfh | true |
| 做饭-浚宇 | S21qwkTNaiTcPKk8NsEcak88nnh | false |
| 运动健身 与 精力管理 相关 | KELwwSvjhi4j1vkhMRUcHLxnneg | false |
| 家务处理 & 滴答清单的后续处理ing | HaWzwF9rLiDGAukOEVZc9OM9nNg | false |
| 2026 端午之行的计划安排 | HemLw15DjirmXPkoBkWcf2EdnXh | false |
| 明心见性课程复盘-2026-04-13 | SYkHwV82BiwhtkkCW4vctqXTncf | false |
| 时间记录与分析 | NgNfwIB4Vi8Y4wkukywcw2bwnRc | false |
| 各项目之间的关系图.xlsx | U0hGwX8YZi4psOkzHvscMyJQnce | false |
| 我的2026.xlsx | Vs0zw8gHViDb0akr2PFcvCcJn8f | false |
| 生活经营复盘讨论脉络 | PWXCwxWYHiHKGWkKD6nc2ffUnDb | false |
| 主线校准台：3天真实反馈实验 | VIM1w4KMpiwqh3k8YqEcQQ3Mnlh | false |

> 家庭合伙人 has_child=true 的深度2节点（共6个）标记待后续增量扫描展开。

---

## AI宝典 知识库结构 (space_id: 7636675042419412190)

### 根节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| AI全景图 | EDYuwxiu6icbxMkbgpec9DgqnVc | false |
| AI工作流 | I6pcwJYkTint9PkBU0WcGFKZnwe | true |
| AI待完善工作流 以及 基础设施 以及可用资源 | U6wjw5Qaei3py2koDtwcpPkmnsh | true |
| AI日志&飞书日志 | TwsEw6GZfiEyh0kByxvcX5L3n3e | true |
| AI应用 | CdSPwCXmxilFOwkJfnuckpEynud | false |
| Harness - 2026年05月08日 From 马向文 | LN15wZ7C3iRxuHk2PqkcOnUgn6n | false |
| AI探索未完待续的部分 | BEpAwckneiauAckY2uecdCcen1g | false |
| 已归档-被入侵旧服务器资料救援与迁移方案 | NmJ2wBbZai0ahokIunZcP9EBnTg | false |

### AI工作流 → 子节点 (12项)

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| AI工作流索引 | HYzLwxSRgiGbTRkOZZgco20jneg | false |
| 服务器 tmux 与终端启动配置 2026-05-09 | GdUjwrrHHioBpak2RvwcNXBrnRd | false |
| AI工作流系统 MVA | CiFiwYYSwiAU2qkpyD7cL6KMn0g | false |
| 服务器健康检查报告 - 2026-05-09 | Ztdpwk22ni7d13k6URxcYJW5nZc | false |
| [已完成] 百万俱乐部：财务长期目标整理与写入 | SE7hwljLBiMIOhkrqMgc4mMenfe | false |
| [已完成] Hermes 每日任务总结飞书通知配置 | R7UDwr8j5iRw24kvxd3cfX9MnXf | false |
| SOP / Playbook | RPEjwcyGSiQZZSkjk2XcL4ABnyI | true |
| 每日总结复盘系统设计与原型验证 | V97swRTP7i0a9nkPorPcsYxfnJb | true |
| [已完成] Happy 手机端本地通信环境升级与清理 | MJjsw26vciUQPFkcERbcUYiSnJd | false |
| Hermes 接入飞书 | R9J1w1EBgixKZkkqjq1cLrYLnVd | false |
| Happy Coder 使用 Hermes 的可行性验证 | ShUyw5TPUirHa7kuNwAc6eDtnRh | false |
| 自媒体输出工作流 · 口述录音→公众号文章 | B4BLwuqediIfeoksBEWc2Q9Tn0d | false |

### AI待完善工作流 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 各类存储空间处理 | Z8XkwhIE3i0OeBkYfmTcsAEHn9e | false |
| AI资源的说明 | KKwiw2N98i16B6kDwVacBL0HnEf | true |

### AI日志&飞书日志 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 飞书管理和应用 | LKtpwbUxXiVTdqkDE3BcHAshndh | false |

---

## 自媒体输出 知识库结构 (space_id: 7636778878492511180)

### 根节点 (全部为叶子节点，无子节点)

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 首页 | EhQCwtr95ieCEpkqWzrcQfdcn0g | false |
| [已打印]自媒体Idea汇总-临时-2026-02-23 | JIS5wS4aKi4JHwkOAYvchiZcnVe | false |
| 凌晨3点，我想对你说 - 新手爸爸崩溃夜 | FpQGwvpbSiMTyPkyjH7cxbphnFb | false |
| 宝宝出生4个月，我被"家庭"彻底困住 | AjYlwjT2pijdV6kISr4cq3fXnhg | false |
| 断夜奶那晚，我一个人带娃，孩子自己睡着了 (1) | IKaVw0KW6iCz31k8EZkcfhFdnPe | false |
| 断夜奶那晚，我一个人带娃，孩子自己睡着了 (2) | Zo6AwnXPki32gSkg1EicCADEn7q | false |
| 自媒体输出工作流 · 口述录音→公众号文章 | UKmPw6gXjij66Xkv80kcwxnIngg | false |
| AI部分参考 | RpVzwZBBvi5dohkAptccRbq6n6f | false |
| 输出相关内容 | LHACw8m1TiYMT1kjG1hcopdAnac | false |

> 该知识库无 has_child=true 节点，9 个全部为叶子节点。

---

## 浚宇的分享-草稿 知识库结构 (space_id: 7641775683433565373)

### 根节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 浚宇的玻璃花园 | Hie9wFKu0iw4kek6kKdctvnJnCd | true |
| 让努力形成复利：个人杠杆系统 5 讲 | BqiBwKBlEilDyukvwjOceFNKnfC | true |
| 教练领域能量概念的跨学科深度研究 | Zt8BwIXtoiZE5Jkf87zcL2WdnAd | false |
| 高知人群行动瘫痪-教练解决路径 | MaAMwCzUAiR3ockXJ8ecO3aBnbg | false |
| act-深度调研-发展脉络与实证全景 | LgMww0NPti95cokLn6QcdUZRnCe | false |
| 科学主义与内在探索-深度分析-v2 | BRetwBbaDiSnxqkQSZ0coeRnnMV | false |

### 浚宇的玻璃花园 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 心智信念 | D6kLwikq4iN0E8kmNclc0DkTnyb | false |
| 人生课题 | CkClwwSvmiQMGvk7GgOcwDEHn6b | false |
| AI时代 | WkqEwkp8XiJesUkWNRUcQiRnnUd | false |
| 什么是杠杆? | LSxdwqcfYiHeGXkm2Pnc3OTonRc | false |
| 经典导读 | GWjYwXLZHiwA6kkwlBkcgwM8ndD | false |
| 三表的故事 | Jvy9wCrBPirqyfkjcAKcw0Wrnqh | false |
| 对话脉络：从最新妙记到个人杠杆系统 | Isllw1o1Fiv1ETkr1pbcBnCinfg | true |

### 让努力形成复利：个人杠杆系统 5 讲 → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 01｜你不是不会用 AI，而是还没有把 AI 放进真实工作流 | DkbKwJ4TOiDArHk9jZ5cCz3tnrg | false |
| 02｜表达不是为了流量，而是为了让正确的人找到你 | AZukwDKsdi052Vkd7szcDWGinuc | false |
| 03｜认识很多人，不等于拥有一个能托举你的场域 | XbXSwrQJQiyR99kHeAwcgm23nwT | false |
| 04｜钱真正重要的地方，是它给你选择权 | TxzpwuKEEiJbM9kXlE8c8KKunub | false |
| 05｜如果每次交付都从零开始，你的价值会被低估 | YnNDwnfyyikt9lkSQ0lcq2Bvnvg | false |

---

## 人生成长杠杆系统 知识库结构 (space_id: 7641892655059995853)

### 根节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 你不是不够努力，只是还没有让努力互相放大 | HA4TwZRnMiQti3kf18Bcn7VYn2e | true |
| 从优秀到卓越：人生成长杠杆系统 | QBEZwnYaRiJVQekgUOYco3dEnPD | false |

### 你不是不够努力... → 子节点

| 节点名 | node_token | has_child |
|--------|-----------|-----------|
| 3 分钟自测：你现在卡在哪个个人杠杆上？ | MoUTwkJjMilvUUkOm7ucI8j1nqq | false |
| 从这里开始：让努力互相放大的个人杠杆系统 | QfxRwGE5xi4OxfkXex4cB1GDnje | false |

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
| 丁雅华 | 雅华交付清单 > 丁雅华-教练交付-沟通记录 | Vwc5wRFVhiTGuxkEIFncP60qneh ✓ |

---

## 待补充

- [x] ~~康康 > 教练服务协议-协议版 (has_child=true)~~ ✓ 2026-06-11 — 1 个叶子节点（康康协议修改说明）
- [x] ~~康康 > 会议记录 (has_child=true)~~ ✓ 2026-06-11 — 7 个叶子节点
- [x] ~~丁雅华 > 教练交付-沟通记录 (has_child=true)~~ ✓ 2026-06-11 — 1 个叶子节点
- [x] ~~朋友们 下 7 个 has_child=true 的人名（李博、Erin艾琳、佳佳、朱训兰、陈妮、余了了、陈悦）~~ ✓ 2026-06-11 — 全部展开到叶子节点
- [x] ~~朋友们 下 朱训兰、余了了 子节点消失~~ ✓ 2026-06-19 — has_child → false，原 1 个子节点已被删除
- [ ] C的旅程 > 我参与的面聊 下 8 个 has_child=true 面聊记录 — 待展开
- [ ] C的旅程 > 前台异议处理 下 10 个 has_child=true — 待展开
- [ ] 商业实践 深度2节点（14个 has_child=true）— 待展开
- [ ] 家庭合伙人 深度2节点（6个 has_child=true）— 待展开
- [ ] AI宝典 深度2节点（3个 has_child=true）：SOP/Playbook、每日总结复盘系统、AI资源的说明 — 待展开
- [ ] 浚宇的分享-草稿 深度2节点：对话脉络 → 待展开
- [ ] 各人物目录下的「会议记录」路径（待发现后完善速查表）

---

## 云盘结构

> 全量扫描时间: 2026-06-11 00:41
> 统计: 199 个文件夹, 363 个文件, 最深 6 层
> 文件类型: docx:230, file:119, bitable:7, shortcut:4, sheet:3
> lark-cli API 调用: 64 次 (根 + 5 depth-1 + 27 depth-2 + 17 depth-3 + 14 depth-4/5 spot-check)
> 深度 4-6 含 ~130+ 用户级客户文件夹，已 spot-check 验证深度，未全量展开

| 📁 Client
  | 📁 2026年客户
    | 📁 关莲
      | 📄 关莲的家庭保障分析报告_20260610111144
    | 📁 魏玉洁
      | 📄 魏玉洁 保单整理表
      | 📄 魏玉洁 电子保单.pdf
      | 📄 魏玉洁 财务规划-风险部分说明 个人.docx
  | 📁 同步.坚果云.助理同步
    | 📁 00 续期提醒名单
      | 📁 ERP下载原报表
      | 📄 【已处理】浚宇 续期客户名单（20201131~20230531）.xlsx
    | 📁 2023年客户
      | 📁 任景坤
      | 📁 刘洋洋
      | 📁 吴晓雯
      | 📁 唐国清
      | 📁 夏煜&冯晨
      | 📁 孙芳屹
      | 📁 张旭艳
      | 📁 张炜明家庭保单整理
      | 📁 彭韵
      | 📁 李慧
      | 📁 杜新华
      | 📁 杨坤宁
      | 📁 杨萌
      | 📁 王丹丹
      | 📁 王柳云
      | 📁 联合展业（百C）
      | 📁 胡老师
      | 📁 詹卓璇
      | 📁 钱黎梦
      | 📁 门毅
      | 📁 陈玥
      | 📄 .DS_Store
    | 📁 2024年客户
      | 📁 Fresh天空
      | 📁 东方梅地亚
      | 📁 刘婧
      | 📁 刘竞璐
      | 📁 左惠婷
      | 📁 张宇-公司-高端医疗
      | 📁 张锐
      | 📁 曾华青
      | 📁 李祺
      | 📁 李陈磊
      | 📁 林东吴
      | 📁 林田田
      | 📁 王珂
      | 📁 田骁
      | 📁 芦华楠
      | 📁 苏亮
      | 📁 贾万泉&简婧淑
      | 📁 陈旺
      | 📁 靳傲森
      | 📁 韩东松
      | 📁 韩小燕
      | 📄 .DS_Store
    | 📁 2025年客户
      | 📁 L 李凌
      | 📁 L 李奕威
      | 📁 Y 阴玉双
      | 📁 Z 张彬，张安琪
      | 📁 Z 张海港
      | 📄 .DS_Store
    | 📁 9999 客户沟通文件
      | 📁 张玉蕾
    | 📁 企业客户资料
      | 📁 公司-文因-福利方案
      | 📁 公司-深圳-身故责任
      | 📁 北京潞晨科技有限公司
      | 📄 企业保险方案说明-v1.key
      | 📄 企业保险方案说明-v1.pdf
      | 📄 新冠相关保险方案.key
      | 📄 新冠相关保险方案.pdf
      | 📄 明亚简介-企业（21.07.21）.pdf
      | 📄 明亚简介-试用版（21.07.21）.pptx
    | 📁 其他文件
      | 📁 语雀空间续期
      | 📄 【使用】北京市住房租赁合同（2023）.doc
      | 📄 【使用（预填信息）】北京市住房租赁合同（2023）.doc
      | 📄 【可编辑范本】北京市住房租赁合同（2023）.doc
      | 📄 北京市住房租赁合同（2023）.doc
      | 📄 北京市商业办公房屋租赁合同.docx
    | 📁 孤儿单
      | 📁 刘香男
      | 📁 王海栗
      | 📁 赵海滨
      | 📁 路鹤鸣
      | 📁 韩健
    | 📁 已整理成交客户信息
      | 📁 2019-王海栗
      | 📁 2021-Yina&芸生
      | 📁 2021-冯鸽&冯振强&李芳
      | 📁 2021-刘晨星&宋雪
      | 📁 2021-唐亚杰&黄娟
      | 📁 2021-孙旭&张白驹
      | 📁 2021-张杰&欧阳柳-开智
      | 📁 2021-张梦迪
      | 📁 2021-张玉蕾&张笑语
      | 📁 2021-张诗颖&阿宁-2021-01-06
      | 📁 2021-徐正乔&沙玲玲&徐培萱
      | 📁 2021-戴悦&伟峰
      | 📁 2021-方柳勤
      | 📁 2021-李博
      | 📁 2021-李康＆刘贺军
      | 📁 2021-李影
      | 📁 2021-杨建辉&谢宏萍&杨茜
      | 📁 2021-杨琳和同事敬一
      | 📁 2021-杨萌&孟燊贤
      | 📁 2021-林东吴
      | 📁 2021-梁笑娜
      | 📁 2021-梁靖&贾可
      | 📁 2021-樊星醒
      | 📁 2021-王爽&赵希
      | 📁 2021-石勇&刘源&刘娣-2021-01-14
      | 📁 2021-肖璇
      | 📁 2021-苏尚君&苏添胜&陈秀丽
      | 📁 2021-范鹏&范随心
      | 📁 2021-詹卓璇
      | 📁 2021-赵登&吴秀彬
      | 📁 2021-赵艳
      | 📁 2021-车玲&李佳伦
      | 📁 2021-边亚瑜 & 边毓
      | 📁 2021-郝迪
      | 📁 2021-金怡&陈昀
      | 📁 2021-闫晗&高雄
      | 📁 2021-陈维
      | 📁 2021-高畅
      | 📁 2021-高闻晓
      | 📁 2022-2月-周蕾
      | 📁 2022-9月份虞春滨-伟峰
      | 📁 2022-9月杨丹
      | 📁 刘尊昌&王瑶
      | 📁 徐江&刘一文&徐子禾
      | 📁 王浚宇&王依凡&陈小菊&王万锦
      | 📄 .DS_Store
    | 📁 已整理未成交的客户信息
      | 📁 0-2021-何玉玲&刘小熙
      | 📁 0-2021-刘华亭
      | 📁 0-2021-唐柳
      | 📁 0-2021-姜岚
      | 📁 0-2021-李妙竹
      | 📁 0-2021-李虹择
      | 📁 0-2021-淡雅洁-2020-12-25-【2021年7月之后继续】
      | 📁 0-2021-贾志立
      | 📁 0-2021-金鑫
      | 📁 0-2021-马琦
      | 📁 0-个人-汤晓
      | 📁 0-个人-王卉
      | 📁 0-刘志勇
      | 📁 0-卢萍&倪嘉彬&卢敏
      | 📁 0-吴红娜
      | 📁 0-宋鑫-车险
      | 📁 0-宋顺&衣琳
      | 📁 0-小连-爱喵师妹
      | 📁 0-王明珠
      | 📁 0-蓝诗钰
      | 📁 2021-12-黄雪萍
      | 📁 2021-姜琬馨&黄子凌
      | 📁 2022-02-张梓桐
      | 📁 2022-03-09  何玲
      | 📁 2022-10月储建丹-伟峰介绍
      | 📁 2022-11月，随身保霍女士
      | 📁 2022-12月王丹丹
      | 📁 2022-1月-苏静-呆萌君
      | 📁 2022-2月-何依蔓
      | 📁 2022-3月-吴晓雯
      | 📁 2022-3月-门晓凡
      | 📁 2022-4月-周琦
      | 📁 2022-5赵开兰&侯守璐
      | 📁 2022-6张杰&钟艳蓉
      | 📁 2022-7月刘晓宇
      | 📁 2022-8月-王天阳
      | 📁 2022-8月-苏静姐姐
      | 📁 2022-9月刘亮
      | 📁 2022-9月谷恒召
      | 📁 2023-01月-陈玥
      | 📁 99-2021-其他-江佳莉
      | 📁 虚无刀
    | 📁 已整理特殊客户信息
      | 📁 99-2021-其他-张力方
      | 📁 99-2021-杨立
      | 📁 王浚宇&王依凡
      | 📁 王燕青
      | 📁 程琳
    | 📁 常用文件模板
      | 📄 00 XX家庭保单汇总表.xlsx
      | 📄 投保信息汇总.xlsx
    | 📄 .DS_Store
  | 📁 服务中客户-20205-8
    | 📁 2025-08-04-贾琛客户资料
      | 📄 MSH经典vs精选.png
      | 📄 保险方案介绍_重疾.pptx
      | 📄 保险方案介绍_高医.pptx
      | 📄 工作簿7.xlsx
      | 📄 贾琛-客户-2025-08-04.xlsx
    | 📁 梁晾
      | 📄 梁晾女儿梁昕元-9月复查血项.jpg
      | 📄 梁晾女儿梁昕元-出院小结.jpg
    | 📄 .DS_Store
    | 📄 李天心-少儿高医产品对比-2025-08-05.xlsx
    | 📄 李涵-家庭-Final-2025-07-29.xlsx
    | 📄 重疾+医疗-吴晓雯.xlsx
  | 📁 自媒体素材准备
    | 📁 航意 软件截图
      | 📄 去哪儿网截图.jpg
      | 📄 携程旅行 (0).jpg
      | 📄 携程旅行 (1).jpg
      | 📄 携程旅行 (2).jpg
      | 📄 携程旅行 (3).jpg
      | 📄 携程旅行 (4).jpg
      | 📄 携程旅行 (5).jpg
      | 📄 携程旅行 (6).jpg
      | 📄 携程旅行 (7).jpg
    | 📄 0-业务-普通门诊险并不省钱.md
    | 📄 0-业务-航空意外险.md
  | 📁 语雀空间续期-2025-7
    | 📄 教育机构、非营利公益组织、初创企业免费申请空间旗舰版.html
    | 📄 语雀01.jpg
    | 📄 语雀02.jpg
    | 📄 语雀空间（初创企业版）申请函 .docx
    | 📄 语雀空间（初创企业版）申请函 .pdf
| 📁 todo-公司讲课-保险经纪人优势解析&官宣
  | 📄 2025-08-30-一阶班-保险经纪人优势解析.m4a
  | 📄 2025-09-17-一阶班-保险经纪人优势解析.m4a
  | 📄 一阶课程-保险经纪人优势解析-2025-09-06.m4a
  | 📄 一阶课程-保险经纪人优势解析-2025-09-06.m4a_20250917_125405.docx
  | 📄 保险经纪人优势解析.m4a_20250830.md
  | 📄 步骤拆解做好经纪人的官宣（标准课件）-2026-04-09 浚宇修改.pptx
  | 📄 经纪人优势解析-自我介绍-课堂说明.pptx
  | 📄 经纪人优势解析-自我介绍-课堂说明_V2-2026-03-07.pptx
| 📁 保存到飞书-浏览器
  | 📄 AI Agent时代，比工具更稀缺的，是自主创造力
  | 📄 「ICE笔试备考」专题2：ICF笔试线上申请指南（中英文双语）
  | 📄 「ICE笔试备考」专题2：ICF笔试线上申请指南（中英文双语）
  | 📄 保存到飞书
  | 📄 利率6.5%，心动啊...
  | 📄 我是如何把AI变成“王牌教研员”，省下80%备课时间的？
  | 📄 用cherry studio打造属于你的超级助理（一）补档
  | 📄 简悦 - SimpRead 📢
  | 📄 考完PCC笔试我才发现，教练真正的商业价值藏在这些“隐秘角落”
  | 📄 考完PCC笔试我才发现，教练真正的商业价值藏在这些“隐秘角落”
  | 📄 赵学强 - 创百汇嘉宾
  | 📄 适配飞书妙记 · Kenshin/simpread · Discussion #3190
  | 📄 除了企业中高管，我还想支持这样的伙伴
| 📁 项目-C9-附件
  | 📁 10.王天宇-时间冲突-未参与
    | 📄 9.0约聊记录-王天宇.docx
    | 📄 北京_王天宇_2026-04-18-逐字稿文本.docx
    | 📄 学习型组织申请资料-王天宇.docx
  | 📁 11.芶知晏
    | 📄 学习型组织申请资料-芶知晏.docx
  | 📁 12.刘红颜
    | 📄 学习型组织申请资料0310-刘红颜.docx
  | 📁 13.柳菁铧
    | 📄 学习型组织申请资料.docx
  | 📁 14.王珂
    | 📄 .DS_Store
    | 📄 9.0约聊记录-王珂.docx
    | 📄 北京-王珂-2026年04月24日-逐字稿文本-1.docx
    | 📄 学习型组织申请资料-王珂-kelvin.pdf
  | 📁 15董董-4+2
    | 📄 董董.docx
  | 📁 16 陈岩
    | 📄 9.0约聊记录模板_前台-陈岩.docx
    | 📄 北京-陈岩-2026年04月25日-逐字稿文本-1.docx
    | 📄 学习型组织申请资料_陈岩.docx
  | 📁 18-Tracy-时间冲突,未参与
    | 📄 20260426094743-北京-Tracy-2026年04月26日-逐字稿文本-1.docx
    | 📄 Tracy，迟-1.jpeg
    | 📄 Tracy，迟-2.jpeg
    | 📄 Tracy，迟-3.jpeg
    | 📄 Tracy，迟-4.jpeg
    | 📄 Tracy，迟-5.jpeg
    | 📄 Tracy，迟-6.jpeg
    | 📄 候选人前台记录-Tracy.docx
  | 📁 19-郭五新
    | 📄 20260426194457-谭晓伟预定的会议-郭五新-转写原文版-1.docx
    | 📄 郭五新：2 - 前台面聊 - 前台约面-学习型组织申请资料-1_学习型组织申请资料-老郭(1).doc
  | 📁 20-田金荣
    | 📄 学习型组织申请资料 -田金荣.docx
  | 📁 21-王珂维
    | 📄 20260429183904-北京-王珂维-0429-逐字稿文本-1.docx
    | 📄 9.0约聊记录模板_前台-王珂维.docx
    | 📄 学习型组织申请资料-王珂维.docx
  | 📁 22-张雅芃
    | 📄 20260429215046-转写_北京-张雅芃-0429-逐字稿文本-1.docx
    | 📄 候选人前台记录-张雅芃.docx
    | 📄 学习型组织申请资料-张雅芃.docx
  | 📁 23-潘颖欣
    | 📄 .DS_Store
    | 📄 潘颖欣中台面聊主聊提问流程.docx
    | 📄 潘颖欣前台谈话记录.docx
    | 📄 潘颖欣待中台面聊.docx
  | 📁 25-曹瑞芳
    | 📄 学习型组织申请资料-曹瑞芳.docx
  | 📁 26-周泽鑫
    | 📄 前台面聊记录-周泽鑫-2026年5月8日
    | 📄 学习型组织申请资料-周泽鑫.docx
  | 📁 5.李奇亮
    | 📄 nancy_学习型组织申请资料-李奇亮.pdf
    | 📄 李奇亮-9.0约聊记录-候选人前台.docx
    | 📄 转写_北京_李奇亮_2026-04-15-逐字稿文本.pdf
  | 📁 6.杨坤
    | 📄 .DS_Store
    | 📄 20260416095349-北京_杨坤_2026-04-16-逐字稿文本-1.docx
    | 📄 学习型组织申请资料-杨坤.jpeg
    | 📄 杨坤9.0约聊记录.docx
  | 📁 7.王贵锋
    | 📄 20260416154222-北京_王贵锋_2026-04-16-逐字稿文本-1.docx
    | 📄 9.0约聊记录-王贵锋.docx
    | 📄 nancy_学习型组织申请资料-王贵锋.docx
  | 📁 8.李玉康-山东
    | 📄 学习型组织申请资料.docx
    | 📄 约聊记录模板-发起人前台李玉康docx.docx
  | 📁 9.于硕鹏
    | 📄 20260418094350-北京_于硕鹏_2026-04-18-逐字稿文本-1.docx
    | 📄 9.0约聊记录模板_前台-于硕鹏.docx
    | 📄 学习型组织申请资料_于硕鹏.pdf
  | 📄 .DS_Store
  | 📄 .~9.0前台面聊话术SOP参考.xlsx
  | 📄 9.0约聊记录模板_前台-候选人.docx
  | 📄 前台面聊最佳实践-2026-04-14.docx
  | 📄 学习型组织申请资料-周泽鑫.docx
  | 📄 徐慧敏.docx
| 📁 飞书 aily
  | 📁 202604
    | 📄 poe-chat-local.zip
  | 📁 202605
    | 📄 Harness Engineering：AI Agent时代的新工程范式
    | 📄 影视飓风AI工作流迁移建议.md
    | 📄 项目总结报告.md
| 📄 000-客户名单汇总 更新：2026年05月01日
| 📄 000-客户名单汇总 更新：2026年05月01日
| 📄 04-ICE Sample Exam Questions
| 📄 04-ICE Sample Exam Questions
| 📄 kangkang_import
| 📄 kangkang_import
| 📄 kangkang_import
| 📄 kangkang_import
| 📄 kangkang_import
| 📄 kangkang_import
| 📄 kangkang_import
| 📄 kangkang_import
| 📄 obsidian-test
| 📄 ✅任务管理
| 📄 个人任务管理
| 📄 书单分类索引-深度分析报告
| 📄 人员招募组碰头会 2026年6月9日
| 📄 北京_田子玄_2026-04-14-逐字稿文本
| 📄 同步测试-挂载知识库
| 📄 姜岚-学习型组织申请资料
| 📄 学习型组织申请资料-余紫娟（余了了） (1).pdf
| 📄 教练课程体系-To Sammy.docx
| 📄 文字记录：2025-06-19-ICE第四期共修营（第一场） 2026年5月6日
| 📄 文字记录：2025-06-22-ICE第四期共修营（第二场） 2026年5月6日
| 📄 文字记录：2025-06-26-ICE第四期共修营（第三场） 2026年5月6日
| 📄 文字记录：2025-07-03-ICE第四期共修营（第四场） 2026年5月6日
| 📄 文字记录：2026-04-29 马向文AI交流 2026年4月29日
| 📄 文字记录：20260506075204-实践营2期_康康教练对话&浚宇督导-视频-1 2026年5月6日
| 📄 文字记录：20260508091036-财务数据演练一组第一次-视频-1-共享屏幕 2026年5月8日
| 📄 文字记录：2026年4月28日-1200万储蓄险案例分享-搞钱研究社 2026年5月6日
| 📄 文字记录：AI业务接入及求职输出讨论 2026年6月7日
| 📄 文字记录：AI健康创业项目面试—周泽鑫 2026年5月8日
| 📄 文字记录：AI发展及生活话题讨论 2026年5月6日
| 📄 文字记录：AI工作流应用及合作讨论 2026年6月8日
| 📄 文字记录：AI工作流应用规划 2026年6月8日
| 📄 文字记录：AI应用交流及资源调动复盘 2026年6月7日
| 📄 文字记录：AI应用分享-1-2026年4月21日 上午10-08 2026年5月6日
| 📄 文字记录：AI应用场景及文件存储规划 2026年5月7日
| 📄 文字记录：AI航海学习问题分析 2026年5月8日
| 📄 文字记录：C9.0活动方案规划与展望 2026年6月7日
| 📄 文字记录：C9加油站·第一场-2026:04:24 19-50 2026年5月6日
| 📄 文字记录：C9加油站·第二场-2026-05-01 2026年5月6日
| 📄 文字记录：C组织活动安排与伴手礼规划 2026年6月7日
| 📄 文字记录：Floria X 浚宇 2026年5月18日
| 📄 文字记录：ICE第四期共修营（第五场）
| 📄 文字记录：ICE第四期共修营（第六场）
| 📄 文字记录：TWS课程价值及应用分享 2026年5月12日
| 📄 文字记录：soundcore Work_05-05 08:25 2026年5月5日
| 📄 文字记录：soundcore Work_05-05 09:23 2026年5月5日
| 📄 文字记录：soundcore Work_05-05 22:18_分段1 2026年5月6日
| 📄 文字记录：soundcore Work_05-05 22:18_分段2 2026年5月6日
| 📄 文字记录：soundcore Work_05-06 11:06 2026年5月6日
| 📄 文字记录：soundcore Work_05-07 20:26 2026年5月7日
| 📄 文字记录：soundcore Work_05-07 20:28 2026年5月7日
| 📄 文字记录：soundcore Work_05-08 08:35 2026年5月8日
| 📄 文字记录：soundcore Work_05-08 18:35 2026年5月8日
| 📄 文字记录：soundcore Work_05-11 08:34 2026年5月11日
| 📄 文字记录：soundcore Work_06-07 23:16 2026年6月7日
| 📄 文字记录：soundcore Work_06-07 23:26 2026年6月7日
| 📄 文字记录：soundcore Work_06-07 23:45 2026年6月7日
| 📄 文字记录：业务及家庭财务规划复盘 2026年6月7日
| 📄 文字记录：个人事业发展规划 2026年6月10日
| 📄 文字记录：中年再婚家庭情况讨论 2026年6月5日
| 📄 文字记录：人员招募组碰头会 2026年6月9日
| 📄 文字记录：任务完成情况及时间规划讨论 2026年5月9日
| 📄 文字记录：保险规划及职业发展讨论 2026年6月5日
| 📄 文字记录：信息判断及年度规划复盘思考 2026年6月7日
| 📄 文字记录：候选人面聊情况复盘 2026年5月8日
| 📄 文字记录：做饭及生活安排复盘与优化 2026年5月6日
| 📄 文字记录：劳动用工合作机会规划 2026年6月8日
| 📄 文字记录：北京新生见面会活动复盘 2026年6月7日
| 📄 文字记录：后来之地| 佳佳教练对话 2026年5月14日
| 📄 文字记录：商业学习组织候选人面试—慧敏 2026年5月8日
| 📄 文字记录：商学院面试—钟银华 2026年5月9日
| 📄 文字记录：地铁乘车信息及安全提示 2026年6月9日
| 📄 文字记录：处事原则及方法分析 2026年6月10日
| 📄 文字记录：外购药保险理赔知识专题分享 2026年5月7日
| 📄 文字记录：多设备配置及联网规划 2026年6月9日
| 📄 文字记录：子女教育方式讨论 2026年5月6日
| 📄 文字记录：学习型组织面聊—黄蓉 2026年5月8日
| 📄 文字记录：学习小组| 教练对话 Sammy 2026年5月14日
| 📄 文字记录：孩子作息及订餐事宜讨论 2026年5月11日
| 📄 文字记录：家务分工及健身计划讨论 2026年5月6日
| 📄 文字记录：家庭事务及工作研究讨论 2026年5月5日
| 📄 文字记录：家庭财务盘点方法与邀约技巧分享 2026年4月30日
| 📄 文字记录：工作与生活经历讨论 2026年6月9日
| 📄 文字记录：工作任务与生活安排讨论 2026年5月5日
| 📄 文字记录：工作挫败感复盘与自我调节 2026年6月8日
| 📄 文字记录：工作流及AI应用规划 2026年6月9日
| 📄 文字记录：工作流程及部署方案复盘 2026年6月5日
| 📄 文字记录：带饭方案讨论 2026年5月9日
| 📄 文字记录：广西发展及AI技术应用讨论 2026年6月7日
| 📄 文字记录：康康-交流AI&教练&财务规划 2026年5月14日
| 📄 文字记录：待办工具切换与带娃理念分享 2026年5月11日
| 📄 文字记录：恋爱与生活感悟讨论 2026年5月7日
| 📄 文字记录：探索之旅课程体验与成长讨论 2026年5月7日
| 📄 文字记录：教练学习小组及财务规划讨论 2026年5月9日
| 📄 文字记录：教练督导复盘与优化讨论 2026年5月6日
| 📄 文字记录：教练课程体系及商业模式规划 2026年6月7日
| 📄 文字记录：教练首秀活动复盘评估 2026年6月7日
| 📄 文字记录：新录音 2026年5月6日
| 📄 文字记录：新录音_2 2026年5月6日
| 📄 文字记录：新录音_2 2026年5月9日
| 📄 文字记录：景区闭园及健身房月卡讨论 2026年5月6日
| 📄 文字记录：每日总结复盘功能规划 2026年6月9日
| 📄 文字记录：活动复盘与后续工作规划 2026年6月7日
| 📄 文字记录：活动执行问题分析与优化建议 2026年6月7日
| 📄 文字记录：活动流程及相关细节规划 2026年6月5日
| 📄 文字记录：浚宇与用户探讨教练合作事宜 2026年5月15日
| 📄 文字记录：浚宇家庭财务规划-宇晴&文艺 2026年5月13日
| 📄 文字记录：浚宇的视频会议 2026年6月5日
| 📄 文字记录：照顾孩子过程中的互动交流 2026年5月11日
| 📄 文字记录：王依凡get笔记 2026年5月6日
| 📄 文字记录：生活段子及内容输出测试讨论 2026年5月5日
| 📄 文字记录：生活琐事及健身消费讨论 2026年5月6日
| 📄 文字记录：社交活动门槛及流程讨论 2026年6月5日
| 📄 文字记录：竞选及工作安排复盘与规划 2026年6月9日
| 📄 文字记录：笔记使用与出行住宿规划讨论 2026年5月6日
| 📄 文字记录：职业规划商业合作机会讨论 2026年5月12日
| 📄 文字记录：育儿安排与孩子活动情况讨论 2026年5月11日
| 📄 文字记录：腾讯会议_20260507_192507 2026年5月7日
| 📄 文字记录：菜市场购物及语音写作讨论 2026年5月5日
| 📄 文字记录：走向MCC之路的提升规划 2026年6月8日
| 📄 文字记录：跨境电商创业项目面试—梦梦 2026年5月8日
| 📄 文字记录：陪伴宝宝成长感悟分享 2026年6月7日
| 📄 文字记录：雅华 教练对话 2026年5月9日
| 📄 文字记录：飞书功能及会员优势分享 2026年6月7日
| 📄 文字记录：餐饮创业与组织学习交流讨论 2026年5月13日
| 📄 文字记录：马向文-家庭财务交流会0421 2026年4月21日 2026年5月6日
| 📄 断夜奶那晚，我一个人带娃，孩子自己睡着了
| 📄 时间四象限工作法
| 📄 智能纪要：2025-06-19-ICE第四期共修营（第一场） 2026年5月6日
| 📄 智能纪要：2025-06-22-ICE第四期共修营（第二场） 2026年5月6日
| 📄 智能纪要：2025-06-26-ICE第四期共修营（第三场） 2026年5月6日
| 📄 智能纪要：2025-07-03-ICE第四期共修营（第四场） 2026年5月6日
| 📄 智能纪要：2026-04-29 马向文AI交流 2026年4月29日
| 📄 智能纪要：20260506075204-实践营2期_康康教练对话&浚宇督导-视频-1 2026年5月6日
| 📄 智能纪要：20260508091036-财务数据演练一组第一次-视频-1-共享屏幕 2026年5月8日
| 📄 智能纪要：2026年4月28日-1200万储蓄险案例分享-搞钱研究社 2026年5月6日
| 📄 智能纪要：AI业务接入及求职输出讨论 2026年6月7日
| 📄 智能纪要：AI健康创业项目面试—周泽鑫 2026年5月8日
| 📄 智能纪要：AI发展及生活话题讨论 2026年5月6日
| 📄 智能纪要：AI工作流应用及合作讨论 2026年6月8日
| 📄 智能纪要：AI工作流应用规划 2026年6月8日
| 📄 智能纪要：AI应用交流及资源调动复盘 2026年6月7日
| 📄 智能纪要：AI应用分享-1-2026年4月21日 上午10-08 2026年5月6日
| 📄 智能纪要：AI应用场景及文件存储规划 2026年5月7日
| 📄 智能纪要：AI航海学习问题分析 2026年5月8日
| 📄 智能纪要：C9.0活动方案规划与展望 2026年6月6日
| 📄 智能纪要：C9加油站·第一场-2026:04:24 19-50 2026年5月6日
| 📄 智能纪要：C9加油站·第二场-2026-05-01 2026年5月6日
| 📄 智能纪要：C组织活动安排与伴手礼规划 2026年6月6日
| 📄 智能纪要：Floria X 浚宇 2026年5月18日
| 📄 智能纪要：ICE第四期共修营（第五场）
| 📄 智能纪要：ICE第四期共修营（第六场）
| 📄 智能纪要：TWS课程价值及应用分享 2026年5月12日
| 📄 智能纪要：soundcore Work_05-05 09:23 2026年5月5日
| 📄 智能纪要：soundcore Work_05-07 20:26 2026年5月7日
| 📄 智能纪要：soundcore Work_05-07 20:28 2026年5月7日
| 📄 智能纪要：soundcore Work_05-08 18:35 2026年5月8日
| 📄 智能纪要：soundcore Work_06-07 23:45 2026年6月7日
| 📄 智能纪要：业务及家庭财务规划复盘 2026年6月7日
| 📄 智能纪要：个人事业发展规划 2026年6月10日
| 📄 智能纪要：中年再婚家庭情况讨论 2026年6月5日
| 📄 智能纪要：人员招募组碰头会 2026年6月9日
| 📄 智能纪要：任务完成情况及时间规划讨论 2026年5月9日
| 📄 智能纪要：信息判断及年度规划复盘思考 2026年6月7日
| 📄 智能纪要：候选人面聊情况复盘 2026年5月8日
| 📄 智能纪要：劳动用工合作机会规划 2026年6月8日
| 📄 智能纪要：北京新生见面会活动复盘 2026年6月7日
| 📄 智能纪要：后来之地| 佳佳教练对话 2026年5月14日
| 📄 智能纪要：商业学习组织候选人面试—慧敏 2026年5月8日
| 📄 智能纪要：商学院面试—钟银华 2026年5月9日
| 📄 智能纪要：地铁乘车信息及安全提示 2026年6月9日
| 📄 智能纪要：处事原则及方法分析 2026年6月10日
| 📄 智能纪要：外购药保险理赔知识专题分享 2026年5月7日
| 📄 智能纪要：多设备配置及联网规划 2026年6月9日
| 📄 智能纪要：子女教育方式讨论 2026年5月6日
| 📄 智能纪要：学习型组织面聊—黄蓉 2026年5月8日
| 📄 智能纪要：学习小组| 教练对话 Sammy 2026年5月14日
| 📄 智能纪要：孩子作息及订餐事宜讨论 2026年5月11日
| 📄 智能纪要：家务分工及健身计划讨论 2026年5月6日
| 📄 智能纪要：家庭事务及工作研究讨论 2026年5月5日
| 📄 智能纪要：工作与生活经历讨论 2026年6月9日
| 📄 智能纪要：工作任务与生活安排讨论 2026年5月5日
| 📄 智能纪要：工作挫败感复盘与自我调节 2026年6月8日
| 📄 智能纪要：工作流及AI应用规划 2026年6月9日
| 📄 智能纪要：工作流程及部署方案复盘 2026年6月5日
| 📄 智能纪要：带饭方案讨论 2026年5月9日
| 📄 智能纪要：广西发展及AI技术应用讨论 2026年6月7日
| 📄 智能纪要：康康-交流AI&教练&财务规划 2026年5月14日
| 📄 智能纪要：待办工具切换与带娃理念分享 2026年5月11日
| 📄 智能纪要：恋爱与生活感悟讨论 2026年5月7日
| 📄 智能纪要：探索之旅课程体验与成长讨论 2026年5月7日
| 📄 智能纪要：教练学习小组及财务规划讨论 2026年5月9日
| 📄 智能纪要：教练督导复盘与优化讨论 2026年5月6日
| 📄 智能纪要：教练课程体系及商业模式规划 2026年6月7日
| 📄 智能纪要：教练首秀活动复盘评估 2026年6月6日
| 📄 智能纪要：景区闭园及健身房月卡讨论 2026年5月6日
| 📄 智能纪要：每日总结复盘功能规划 2026年6月9日
| 📄 智能纪要：活动复盘与后续工作规划 2026年6月6日
| 📄 智能纪要：活动执行问题分析与优化建议 2026年6月6日
| 📄 智能纪要：活动流程及相关细节规划 2026年6月4日
| 📄 智能纪要：浚宇家庭财务规划-宇晴&文艺 2026年5月13日
| 📄 智能纪要：浚宇的视频会议 2026年6月5日
| 📄 智能纪要：照顾孩子过程中的互动交流 2026年5月11日
| 📄 智能纪要：王依凡get笔记 2026年5月6日
| 📄 智能纪要：生活段子及内容输出测试讨论 2026年5月5日
| 📄 智能纪要：生活琐事及健身消费讨论 2026年5月6日
| 📄 智能纪要：社交活动门槛及流程讨论 2026年6月4日
| 📄 智能纪要：竞选及工作安排复盘与规划 2026年6月9日
| 📄 智能纪要：笔记使用与出行住宿规划讨论 2026年5月6日
| 📄 智能纪要：职业规划商业合作机会讨论 2026年5月12日
| 📄 智能纪要：育儿安排与孩子活动情况讨论 2026年5月11日
| 📄 智能纪要：腾讯会议_20260507_192507 2026年5月7日
| 📄 智能纪要：菜市场购物及语音写作讨论 2026年5月5日
| 📄 智能纪要：走向MCC之路的提升规划 2026年6月8日
| 📄 智能纪要：跨境电商创业项目面试—梦梦 2026年5月8日
| 📄 智能纪要：陪伴宝宝成长感悟分享 2026年6月7日
| 📄 智能纪要：飞书功能及会员优势分享 2026年6月7日
| 📄 智能纪要：餐饮创业与组织学习交流讨论 2026年5月13日
| 📄 智能纪要：马向文-家庭财务交流会0421 2026年4月21日 2026年5月6日
| 📄 测试-import导入
| 📄 玉洁沟通教练协议事宜 2026年6月5日
| 📄 简洁版-个人任务看板 Copy
| 📄 线上 / 线上活动数据分析
| 📄 财务-【会富系列课】家庭财务检测表
| 📄 邹易 家庭保险规划 Intake 2026-06-10
| 📄 雅华 教练对话 2026年5月9日

### 深度 4-6 结构说明

深度 4+ 主要是 Client/ 下的客户个人文件夹，每个客户文件夹通常包含：
- `保单明细/` — 历年保单文件
- `投前资料/` / `前期沟通/` — 投保前沟通材料
- `2022年保单/` ~ `2026年保单/` — 按年份归档
- `投保资料/` / `承保资料/` / `理赔资料/` — 业务文档
- `保全变更/` / `续保材料/` — 后续服务

**客户文件夹统计（深度 3-6）:**
| 父级目录 | 客户文件夹数 | 最深 |
|----------|:-----:|:----:|
| 2025年客户 | 5 | 5-6 |
| 2024年客户 | 21 | 5-6 |
| 2023年客户 | 21 | 5-6 |
| 已整理成交客户信息 | 45 | 5-6 |
| 已整理未成交的客户信息 | 42 | 5-6 |
| 孤儿单 | 5 | 5-6 |
| 已整理特殊客户信息 | 5 | 5-6 |
| 其他文件 | 1 | 5-6 |
| 企业客户资料 | 3 | 5-6 |
| 9999 客户沟通文件 | 1 | 5-6 |
| 00 续期提醒名单 | 1 | 5-6 |

> 深度 4-6 共 ~130+ 客户级文件夹，spot-check 确认最深可达 6 层（保单明细 → 年度保单 → 材料类型）。全量展开需额外 ~120+ API 调用。

---

*云盘结构最后更新: 2026-06-11*
---

*最后更新: 2026-06-27 — 增量扫描：新增 邹易 (has_child=true, 3 子节点) + 关莲沟通小结-202606 (1 叶子)。总计 476 节点。*
