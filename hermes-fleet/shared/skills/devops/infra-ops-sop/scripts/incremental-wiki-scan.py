#!/usr/bin/env python3
"""Daily incremental wiki path index sync — detects new nodes under known has_child=true parents.

Usage:
  python3 scripts/incremental-wiki-scan.py [--space-id SPACE_ID] [--delay SECONDS]

Compares live lark-cli wiki +node-list output against the embedded `existing` dict.
Outputs new discoveries as JSON to /tmp/wiki-scan-new.json for downstream processing.
Exit code 0 = no changes, 1 = new nodes found.

Requirements: lark-cli v1.0.44+ on PATH. Uses --space-id and --parent-node-token flags.
"""
import subprocess, json, re, time, sys, os

SPACE_ID = "7636684753655319743"
DELAY = 4

# ============================================================
# Existing index data — keep in sync with wiki-path-index.md
# Format: {parent_token: {child_token: (child_name, has_child)}}
# ============================================================
existing = {}

def add_children(parent, *items):
    """Register known children for a parent token. items: (token, name, has_child)."""
    existing[parent] = {}
    for t, n, h in items:
        existing[parent][t] = (n, h)

# --- 客户相关 (root) — 14 people ---
add_children("DcMiwjhT5iY4IokSxulcWYoBnSb",
    ("AIjRwXudUizTKzkLJQncOEY5n6c", "汤望霖 Lynn", True),
    ("AzLLwrhIsiUNDwkFLZ2c3tX8nde", "关莲", True),
    ("Oj7swNMDViyat6k6v79cQrjvnIg", "魏玉洁", True),
    ("MFDKwCRzjiCBzakNXhMc1JBvn8b", "徐正乔", True),
    ("Fi5Dwjxk4iTJv2kEGANcg4cpn2e", "刘晓宇", False),
    ("XEL9wk9AOisOUXk8zywcRreInee", "康康", True),
    ("Uks3wWAF7il4ZUkXvvycS5S5noQ", "丁雅华", True),
    ("JqxFwJfYiizGXik6stjcXCWgnDb", "李慧", True),
    ("KFtbwYiV3iguHvk3dmYcP7h7nIg", "曾华青", True),
    ("KkqpwlHGcihkT0kIM52cTGu1nMf", "陈悦", True),
    ("FDs5wmaKIiSQbSk27oGcJBLKnPf", "陈妮", True),
    ("URyhwU4PPiO09ak1UM1cbvuXnVh", "李博", True),
    ("QtJowwdA6ipsPRkzqWwcaWefn3K", "Erin艾琳", True),
    ("YvwawNcKniSnsBkodqFch7mpnvX", "佳佳", True),
    ("IOEOwpB46iyzIvk2YuhcwZlfnSe", "邹易", True),
)

# --- 朋友们 (root) — 33 people ---
add_children("F58lwOvCFid1FlkUtA8cAhMsnwg",
    ("JDZbwz7jxiNbUMkrIdgcnRk3nIG", "王秋云", False),
    ("FyHnwobfhiiIc0kKXHacwvURnag", "GG", False),
    ("Z9EhwNzFfiP4jCkOYuTcuhTJnUg", "韦德华", False),
    ("Ddoawuz5YiDRAykhm4Qckc6CnMd", "朱敏", False),
    ("EkfPwpdhAiO6QTkWcT0cZIYVnrb", "Michael", False),
    ("Tw0BwAeJJiHc8bkuDWLcQx31nYc", "谢新源", False),
    ("P3F1wnziHinGsck84odcQjswn2g", "刘凯", False),
    ("ETdWwJQkHi658zkcqHKcaPiCnII", "赵红丽", False),
    ("EdKJwMhWEibiTrkP0NZcFAkCnh0", "黄文艺", False),
    ("E8Egw7sv7iheODklzTScwPqGnTg", "宋荔斯", False),
    ("Oz54wP6Hoi7ipAkFmvbcOjcRnt0", "夏雪", False),
    ("L6yAwCbzQiCJsskAyUBczAJlnvh", "朱训兰", False),
    ("X9K0w6fx3itPhAkleGZc5qW3n6e", "罗惠方", False),
    ("UFCAwRSYPiNrYXknTVvcJesbn4e", "蒋艺婧", False),
    ("HeqpwbhqGi22BBkaRFVcsXmKnVc", "谢伊璇", False),
    ("D9mkwW7l5iAXcUkzW1wcYdlKnub", "阴玉双", False),
    ("RblwwIGLNibmRQkGQn8cUaMQnxh", "杨立", False),
    ("VSH0wgo90iqr62kVvnFco43xnbf", "朱凡", False),
    ("TKndwHWcYiBkDMkSBr9cUGdsnac", "孔明", False),
    ("Ooj4wGywLiGinIksYmScLw40nVd", "杨鑫", False),
    ("XJkHw50vHiIVYekMPl6c9VrZnvh", "项士烁", False),
    ("AlYTwNfnViwNiakbz0bcgHLVnng", "罗殷宇晴", False),
    ("UnP6wXGKEiX20skHSrycO1KZn6c", "孙彦玲", False),
    ("Dv0nwyUFCigxmLk7CATcLQHJnke", "杨静", False),
    ("XUA5wAH9jik9OdkuKHhcXppdnXe", "yoyo", False),
    ("A9fywH8Qhi8p58kGBOAckYR6nhg", "晓明", False),
    ("EPsowJoHriEG8okVW0vcWhBMneh", "山雯", False),
    ("BH4hwzxnpik3ChkmrkccIYjOnRh", "余了了", False),
    ("BwmywG321i64YRkV7nFcKpoxned", "张敏立", False),
    ("BRFPwwvl5it2WEkeW65cEfWynsd", "何水", False),
    ("C26HwqnkniI44NkUHSTce8GmnJd", "Harry 皓同学", False),
    ("BxQxwmfYYiO36ZkbuomcmEp5n2y", "邱楚", False),
    ("MWe9weyxeib07BkKKO7cZ0hPnod", "王永澄", False),
)

# --- Level 1: has_child=true people's direct children ---
add_children("AIjRwXudUizTKzkLJQncOEY5n6c",  # 汤望霖
    ("CjgvwoIuIi3at2k56C2cCNcZniH", "协议沟通准备-Lynn", False),
)
add_children("AzLLwrhIsiUNDwkFLZ2c3tX8nde",  # 关莲 — 12 children
    ("JFSawr332iYSSok5jDXcqWhtnDd", "关莲-保险及资产配置方案讨论", False),
    ("Rl94wKHQfiBqRYkOF32cUrLbnad", "文字记录：保险行业现状与业务方式讨论 2026年6月5日", False),
    ("OL4zwKmEGio6qskB860cILdNnwc", "赵学强", False),
    ("JdaDwK1zjiqcGgkKJIfc10wNn17", "关莲 智能纪要：保险行业现状与业务方式讨论 2026年6月5日", False),
    ("NyLZwL4buiIfRgksthRcIMGYnJz", "关莲 智能纪要：保险规划及职业发展讨论 2026年6月5日", False),
    ("ReN6wY7TUi4LlrkZiGicCWrPnzx", "关莲-沟通小结-20260605", False),
    ("TYBvwCu6Hi5u7Mk5mVnciJ0WnFd", "关莲-横琴保单.pdf", False),
    ("Y0MDwfw9TiXImqkgyEWcMpNOnzb", "关莲家庭保障分析-生老病死-V1", False),
    ("KzFew97gWiwACwkJQdlcvCb5nWc", "关莲的家庭保障分析报告_20260610111144", False),
    ("PZZOwqGPai39kDkFfLlcDjUNnGh", "关莲家庭财务全景分析-生老病死-V2", False),
    ("HJ6QwL6xziAJSok2qm4cprsun9R", "关莲家庭生命周期表", False),
    ("YFVwwThcui0Oiyk0rZ4cZtCZn1B", "关莲家庭财务全景分析-Final", False),
    ("Fwk2w5oEFiUO7Fkc2gdcnX3ln4n", "关莲沟通小结-202606", False),
)
add_children("Oj7swNMDViyat6k6v79cQrjvnIg",  # 魏玉洁
    ("RMlnwgkCniMmkskeNl1ceAWwnqh", "玉洁交付清单", True),
)
add_children("MFDKwCRzjiCBzakNXhMc1JBvn8b",  # 徐正乔
    ("XOA7wXpeIiTL8kkjHlnc9JxKnud", "利率6.5%，心动啊...", False),
    ("NcwBwbrBFiUun7k0WNYcJ1Awnib", "正乔退休方案：世D悦享3 vs 大陆产品 · 全情景对比 - 考虑通胀的版本", False),
    ("MME3wYGX0ifa0Gko5FUcXuyKnSf", "小乔同学退休方案：世D悦享3 vs 大陆产品", False),
)
add_children("XEL9wk9AOisOUXk8zywcRreInee",  # 康康
    ("UUFIwZsYliBnj1kA5CPc71m9nyg", "康康教练对话-督导.xlsx", False),
    ("PLC2wV49MiR9Nnkoc00clIUanG5", "康康交付文档清单", True),
)
add_children("Uks3wWAF7il4ZUkXvvycS5S5noQ",  # 丁雅华
    ("PYakwBbjoiZtBQkUnLFcy1VTnmf", "雅华交付清单", True),
)
add_children("JqxFwJfYiizGXik6stjcXCWgnDb",  # 李慧
    ("PGOtwuoZ3iyAtOkjW8kcaYgVnYc", "李慧家庭财务-风险部分-2026年04月21日", False),
    ("GwHjw4sD7iE1GqksdyHcAsCLnvb", "李慧家庭财务-风险部分-2026年04月21日.pdf", False),
    ("IIQzwEuaOiJLpVkVoG3cfgs4nnc", "沟通小结-慧姐", False),
    ("H13ew1MP6ilwISkIx6ic9WtPnbc", "李慧方案准备-2026年05月25日", False),
)
add_children("KFtbwYiV3iguHvk3dmYcP7h7nIg",  # 曾华青
    ("LW40wTgzbiLuf2kj9Qacx5r1nMh", "附近森林项目反馈", False),
)

# --- Level 2: 交付清单 children ---
add_children("RMlnwgkCniMmkskeNl1ceAWwnqh",  # 玉洁交付清单
    ("DhT7wZ6ODi1xhBk3Dj3cD8gMndh", "协议沟通准备", False),
    ("DsxVweCBMighwQkz0KbcfqUFnKb", "玉洁沟通教练协议事宜", False),
    ("KTU8wU1viiigtukUM7Qc3Mu7n0c", "玉洁-教练服务协议", False),
    ("BPtXwdcDyi6M4ckVTsFcooJhnWe", "2026-04-20 玉洁沟通", False),
    ("MEqnwXwYai5Ryjk7WHGcIY9Nnve", "2026-02-10-玉洁_财务规划", False),
    ("StIkw6CaHim8QwkbIjGcY2IZn5f", "20251223085906-转写_和浚宇的教练对话-逐字稿文本-1", False),
    ("I3zIwXgh8iRapRkM4t8c0ASPnqf", "20251231163347-转写_玉洁-生命探索-逐字稿文本-1", False),
    ("PsvXwArzriEJ3ZkA27Icfc65nae", "20260107154213-转写_玉洁教练对话-逐字稿文本-1", False),
    ("Ugwdwhm0Oim6Z4k7eJvcZbFhnJe", "20260113154516-转写_玉洁-best year-逐字稿文本-1", False),
    ("OxCqwn9MKio3TfkfwGMc3RiYnWf", "20260115151714-玉洁 best year-逐字稿文本-1", False),
)
add_children("PLC2wV49MiR9Nnkoc00clIUanG5",  # 康康交付文档清单
    ("NaHvwTT4XiTUPekVFR5cpXQonZI", "康康-教练服务协议-协议版", True),
    ("WgaTw6iiFiHXnuktzaEcjkEanRh", "画板文档", False),
    ("MjpOwDi2fit35vkhUV3cMcrknqh", "财务-家庭财务检测表-2026年06月01日-V2.xlsx", False),
    ("AW2uwkHXei9Nkuk1w7Wc9CgVnZf", "康康-家庭财务检测表.xlsx", False),
    ("EcsJwMaljiMgJ5kOs7acspU6ncf", "康康-中日保险深度对比分析-From Deepseek", False),
    ("D9dLwrEP2iX8NfkcwEgcIFebnDe", "会议记录", True),
    ("X2ldwmbcMiRDkSklDgIciyUmn0b", "康康-教练服务协议-协议版.pdf", False),
    ("Ix4lwL6jri1EFdkG6xmcxE2WnLJ", "康康进展跟踪", False),
)
add_children("PYakwBbjoiZtBQkUnLFcy1VTnmf",  # 雅华交付清单
    ("F8W6wTagSi0UGtkJcbzcykitnCf", "雅华-教练服务协议-已结束", False),
    ("Vwc5wRFVhiTGuxkEIFncP60qneh", "丁雅华-教练交付-沟通记录", True),
)

# --- Level 3: deepest expanded ---
add_children("NaHvwTT4XiTUPekVFR5cpXQonZI",  # 协议版
    ("BayzwZ0qzi9l9RkrRHtcOPJnn0g", "康康协议修改说明", False),
)
add_children("D9dLwrEP2iX8NfkcwEgcIFebnDe",  # 会议记录
    ("UQ0XwGZhPiXiEjkJjZccvslynje", "2026.6.10 康康-3个月陪跑目标沟通", False),
    ("YVSRwIG1GioxRIkJmQ4cwT6anCb", "2026-06-03 康康 教练协议沟通", False),
    ("EIg7wIEbIiFOCekLxgicCFpInZg", "2026-06-01 康康-教练&财务沟通", False),
    ("RzICwetckiIPYKkKBOLcVnkhn1c", "2026-05-24 学了教练之后，你有哪些变化和顾虑？", False),
    ("Xi0RwtXotiWviKk4zgWcAUbgn1f", "2026-05-23 康康-财务规划交流", False),
    ("D99ywSSlfitOLNktpc8c3Yflnrb", "2026-05-14 康康-交流AI&教练&财务规划", False),
    ("EdshwfxdJiWNf5kjvFncSZbmn3b", "2026-05-09 教练对话-客户康康-教练浚宇", False),
)
add_children("Vwc5wRFVhiTGuxkEIFncP60qneh",  # 沟通记录
    ("Z165wvWoWi7OQAkFOwWcPVRjnPe", "智能纪要：雅华 教练对话 2026年5月9日", False),
)

# --- 朋友们 expanded (moved to 客户相关 2026-06-13, but tokens still tracked) ---
add_children("URyhwU4PPiO09ak1UM1cbvuXnVh",  # 李博
    ("Lo4OwfEVIiBBJTkkslgcRYaznYg", "Tapon: A Manifesto", False),
    ("GByqwZXqliY54IkpyjPc7WcHnNd", "Tapon许愿池 From 浚宇", False),
    ("ENGyw6nNfiQCVFkf7dwcweYfnwf", "tapon-shiyong-tiyan-ji-gongzuoliu-guihua", False),
)
add_children("QtJowwdA6ipsPRkzqWwcaWefn3K",  # Erin艾琳
    ("Es36wv7hMi0mVBk9tt1cbBZxnJg", "Erin-后来之地讨论", False),
    ("THfUwOfRXibZewkHaSfcS01vnGf", "Erin-教练服务协议", False),
)
add_children("YvwawNcKniSnsBkodqFch7mpnvX",  # 佳佳
    ("GEQVwcxSnitZ35kMDU3c4rkMngf", "佳佳-教练服务协议", False),
)
add_children("IOEOwpB46iyzIvk2YuhcwZlfnSe",  # 邹易
    ("RJIVwTjlEiMsjnkM3vhcnuONngd", "邹易 家庭保险规划 Intake 2026-06-10", False),
    ("YAIXwoTAFiybSykUlfpcuJHGnnf", "邹易-保险咨询待办事项", False),
    ("RIJtw7NLOipMEmkocgIclzLWnrb", "邹易家庭保障沟通小结", False),
)
add_children("FDs5wmaKIiSQbSk27oGcJBLKnPf",  # 陈妮
    ("M3fSwuOvViyD4ekh5HdcP2Hvn2c", "Sammy需求沟通复盘与后续服务设计", False),
    ("AEBHw9qdGiaOsxkiTMVc6f3GnRg", "Sammy-需求沟通", False),
)
add_children("KkqpwlHGcihkT0kIM52cTGu1nMf",  # 陈悦
    ("QJltwzh7bitRRHkbVYZcxacTnfV", "沈磊保单利益整理表20251225.xlsx", False),
    ("OGoDwKS9MiKUyzkYhAEclWx1nNb", "陈悦家庭财务规划-风险分析", False),
    ("NXcVwWUtQithgykyF37csqIWn1g", "卡卡聊保险需求", False),
    ("DE8dwsWvXiamS6kYbFdciJSrn51", "卡卡沟通小结-微信版-2026-06-05", False),
)
# 朱训兰 (has_child→false 2026-06-19) — empty dict, not scanned
add_children("L6yAwCbzQiCJsskAyUBczAJlnvh")
# 余了了 (has_child→false 2026-06-19) — empty dict, not scanned
add_children("BH4hwzxnpik3ChkmrkccIYjOnRh")

# --- 首页 ---
add_children("R2hnw298AihV7ekd05xc9mMBnfg",  # 人员清单
    ("GaYPwhIyKiiVPpkuqETcCLkinXf", "人员清单更新日志说明", False),
)


# ============================================================
# Scan logic
# ============================================================

def run_node_list(token, space_id=SPACE_ID):
    """Call lark-cli wiki +node-list, return {child_token: (name, has_child)} or None on error."""
    cmd = [
        "lark-cli", "wiki", "+node-list",
        "--space-id", space_id,
        "--parent-node-token", token,
        "--page-all", "--page-limit", "0",
    ]
    penv = os.environ.copy()
    penv["TERM"] = "dumb"
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=penv)
    if result.returncode != 0:
        print(f"  ERROR: lark-cli exit={result.returncode}")
        err = result.stderr.strip()[:200]
        if err:
            print(f"  stderr: {err}")
        return None

    raw = result.stdout.strip()
    if not raw:
        print("  (empty response)")
        return {}

    # Strip --page-all prefix + Found N node(s) (rule 8)
    raw = re.sub(r'^\[page \d+\] fetching\.\.\.\s*', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'^Found \d+ node\(s\)\s*\n?', '', raw, flags=re.MULTILINE)
    raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}, raw[:200]: {raw[:200]}")
        return None

    # Handle v1.0.44+ dict wrapper (rule 9b)
    nodes = data
    if isinstance(data, dict):
        if "data" in data and isinstance(data.get("data"), dict) and "nodes" in data["data"]:
            nodes = data["data"]["nodes"]
        elif "nodes" in data:
            nodes = data["nodes"]
        elif data.get("ok") is False:
            print(f"  API error: {data.get('error', 'unknown')}")
            return None

    if not isinstance(nodes, list):
        print(f"  Unexpected type: {type(nodes)}")
        return None

    children = {}
    for item in nodes:
        if not isinstance(item, dict):
            continue
        name = item.get("title", "unknown")
        ct = item.get("node_token", "")
        hc = item.get("has_child", False)
        if ct:
            children[ct] = (name, hc)
    return children


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Daily incremental wiki path index sync")
    parser.add_argument("--space-id", default=SPACE_ID)
    parser.add_argument("--delay", type=int, default=DELAY)
    args = parser.parse_args()

    # Scan list: (token, label) — only has_child=true nodes or root groups
    scans = [
        # Root groups — detect new people
        ("DcMiwjhT5iY4IokSxulcWYoBnSb", "客户相关 (root)"),
        ("F58lwOvCFid1FlkUtA8cAhMsnwg", "朋友们 (root)"),
        # Level 1 has_child=true people
        ("AIjRwXudUizTKzkLJQncOEY5n6c", "客户相关 > 汤望霖 Lynn"),
        ("AzLLwrhIsiUNDwkFLZ2c3tX8nde", "客户相关 > 关莲"),
        ("Oj7swNMDViyat6k6v79cQrjvnIg", "客户相关 > 魏玉洁"),
        ("MFDKwCRzjiCBzakNXhMc1JBvn8b", "客户相关 > 徐正乔"),
        ("XEL9wk9AOisOUXk8zywcRreInee", "客户相关 > 康康"),
        ("Uks3wWAF7il4ZUkXvvycS5S5noQ", "客户相关 > 丁雅华"),
        ("JqxFwJfYiizGXik6stjcXCWgnDb", "客户相关 > 李慧"),
        ("KFtbwYiV3iguHvk3dmYcP7h7nIg", "客户相关 > 曾华青"),
        ("KkqpwlHGcihkT0kIM52cTGu1nMf", "客户相关 > 陈悦"),
        ("FDs5wmaKIiSQbSk27oGcJBLKnPf", "客户相关 > 陈妮"),
        ("URyhwU4PPiO09ak1UM1cbvuXnVh", "客户相关 > 李博"),
        ("QtJowwdA6ipsPRkzqWwcaWefn3K", "客户相关 > Erin艾琳"),
        ("YvwawNcKniSnsBkodqFch7mpnvX", "客户相关 > 佳佳"),
        ("IOEOwpB46iyzIvk2YuhcwZlfnSe", "客户相关 > 邹易"),
        # Level 2
        ("RMlnwgkCniMmkskeNl1ceAWwnqh", "魏玉洁 > 玉洁交付清单"),
        ("PLC2wV49MiR9Nnkoc00clIUanG5", "康康 > 康康交付文档清单"),
        ("PYakwBbjoiZtBQkUnLFcy1VTnmf", "丁雅华 > 雅华交付清单"),
        # Level 3
        ("NaHvwTT4XiTUPekVFR5cpXQonZI", "康康 > 交付清单 > 协议版"),
        ("D9dLwrEP2iX8NfkcwEgcIFebnDe", "康康 > 交付清单 > 会议记录"),
        ("Vwc5wRFVhiTGuxkEIFncP60qneh", "丁雅华 > 交付清单 > 沟通记录"),
        # 首页
        ("R2hnw298AihV7ekd05xc9mMBnfg", "首页 > 人员清单"),
    ]

    all_new = {}
    total = len(scans)

    for i, (token, label) in enumerate(scans):
        print(f"\n[{i+1}/{total}] {label}")
        print(f"  token: {token}")

        children = run_node_list(token, args.space_id)
        if children is None:
            print(f"  SKIPPED (error)")
            continue

        print(f"  Found {len(children)} children")

        known = existing.get(token, {})
        new_for_parent = {}
        for ct, (cn, ch) in children.items():
            if ct not in known:
                flag = " [HAS_CHILD]" if ch else ""
                print(f"  NEW: {cn} | {ct} | has_child={ch}{flag}")
                new_for_parent[ct] = (cn, ch)
            else:
                old_hc = known[ct][1]
                if ch != old_hc:
                    print(f"  CHANGED: {cn} has_child {old_hc} -> {ch}")

        if not new_for_parent:
            current_tokens = set(children.keys())
            known_tokens = set(known.keys())
            removed = known_tokens - current_tokens
            if removed:
                print(f"  REMOVED ({len(removed)}):")
                for rt in removed:
                    print(f"    - {known[rt][0]} | {rt}")
            else:
                print(f"  (no changes, still {len(known)} children)")
        else:
            print(f"  => {len(new_for_parent)} new, {len(children)} total")
            all_new[token] = {"label": label, "children": new_for_parent, "all_children": children}

        if i < total - 1:
            time.sleep(args.delay)

    print("\n" + "=" * 60)
    print("SCAN COMPLETE — " + time.strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)

    if all_new:
        total_new = sum(len(v["children"]) for v in all_new.values())
        print(f"\nNEW DISCOVERIES: {total_new} nodes across {len(all_new)} parents")
        for token, info in all_new.items():
            print(f"\n  {info['label']}:")
            for ct, (cn, ch) in info["children"].items():
                flag = "[HAS_CHILD]" if ch else "[LEAF]"
                print(f"    {flag} {cn}")
                print(f"           token: {ct}")
        # Output JSON for downstream processing
        new_json = {}
        for token, info in all_new.items():
            new_json[token] = {
                "label": info["label"],
                "children": {ct: [cn, ch] for ct, (cn, ch) in info["children"].items()},
            }
        with open("/tmp/wiki-scan-new.json", "w") as f:
            json.dump(new_json, f, ensure_ascii=False, indent=2)
        print(f"\nSaved discovery JSON to /tmp/wiki-scan-new.json")
        return 1
    else:
        print("\nNo new paths found.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
