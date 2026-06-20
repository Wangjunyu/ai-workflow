#!/usr/bin/env python3
"""
Daily incremental wiki path index sync script.
Used by cron jobs to detect new wiki nodes under known has_child=true parents.

Usage:
  python3 scripts/incremental-wiki-scan.py [--space-id SPACE_ID] [--delay SECONDS]

Reads existing index data from embedded dict (mirrors wiki-path-index.md).
Outputs new discoveries as JSON for downstream index updater.

Requirements: lark-cli v1.0.44+ (uses --space-id and --parent-node-token flags).
"""
import subprocess
import json
import re
import time
import sys

SPACE_ID = "7636684753655319743"
DELAY = 4  # seconds between API calls

# Existing index data (extracted from wiki-path-index.md)
# Format: {node_token: {children: {child_token: (child_name, has_child)}}}
# NOTE: Update this dict when wiki-path-index.md changes substantially.
existing = {
    # 客户相关 people (level 1)
    "AIjRwXudUizTKzkLJQncOEY5n6c": {"children": {"CjgvwoIuIi3at2k56C2cCNcZniH": ("协议沟通准备-Lynn", False)}},
    "AzLLwrhIsiUNDwkFLZ2c3tX8nde": {"children": {
        "JFSawr332iYSSok5jDXcqWhtnDd": ("关莲-保险及资产配置方案讨论", False),
        "Rl94wKHQfiBqRYkOF32cUrLbnad": ("文字记录：保险行业现状与业务方式讨论 2026年6月5日", False),
        "OL4zwKmEGio6qskB860cILdNnwc": ("赵学强", False),
        "JdaDwK1zjiqcGgkKJIfc10wNn17": ("关莲 智能纪要：保险行业现状与业务方式讨论 2026年6月5日", False),
        "NyLZwL4buiIfRgksthRcIMGYnJz": ("关莲 智能纪要：保险规划及职业发展讨论 2026年6月5日", False),
        "ReN6wY7TUi4LlrkZiGicCWrPnzx": ("关莲-沟通小结-20260605", False),
        "TYBvwCu6Hi5u7Mk5mVnciJ0WnFd": ("关莲-横琴保单.pdf", False),
        "Y0MDwfw9TiXImqkgyEWcMpNOnzb": ("关莲家庭保障分析-生老病死-V1", False),
        "KzFew97gWiwACwkJQdlcvCb5nWc": ("关莲的家庭保障分析报告_20260610111144", False),
        "PZZOwqGPai39kDkFfLlcDjUNnGh": ("关莲家庭财务全景分析-生老病死-V2", False),
        "HJ6QwL6xziAJSok2qm4cprsun9R": ("关莲家庭生命周期表", False),
        "YFVwwThcui0Oiyk0rZ4cZtCZn1B": ("关莲家庭财务全景分析-Final", False),
    }},
    "Oj7swNMDViyat6k6v79cQrjvnIg": {"children": {"RMlnwgkCniMmkskeNl1ceAWwnqh": ("玉洁交付清单", True)}},
    "MFDKwCRzjiCBzakNXhMc1JBvn8b": {"children": {
        "XOA7wXpeIiTL8kkjHlnc9JxKnud": ("利率6.5%，心动啊...", False),
        "NcwBwbrBFiUun7k0WNYcJ1Awnib": ("正乔退休方案...", False),
        "MME3wYGX0ifa0Gko5FUcXuyKnSf": ("小乔同学退休方案...", False),
    }},
    "XEL9wk9AOisOUXk8zywcRreInee": {"children": {
        "UUFIwZsYliBnj1kA5CPc71m9nyg": ("康康教练对话-督导.xlsx", False),
        "PLC2wV49MiR9Nnkoc00clIUanG5": ("康康交付文档清单", True),
    }},
    "Uks3wWAF7il4ZUkXvvycS5S5noQ": {"children": {"PYakwBbjoiZtBQkUnLFcy1VTnmf": ("雅华交付清单", True)}},
    "JqxFwJfYiizGXik6stjcXCWgnDb": {"children": {
        "PGOtwuoZ3iyAtOkjW8kcaYgVnYc": ("李慧家庭财务-风险部分-2026年04月21日", False),
        "GwHjw4sD7iE1GqksdyHcAsCLnvb": ("李慧家庭财务-风险部分-2026年04月21日.pdf", False),
        "IIQzwEuaOiJLpVkVoG3cfgs4nnc": ("沟通小结-慧姐", False),
        "H13ew1MP6ilwISkIx6ic9WtPnbc": ("李慧方案准备-2026年05月25日", False),
    }},
    "KFtbwYiV3iguHvk3dmYcP7h7nIg": {"children": {"LW40wTgzbiLuf2kj9Qacx5r1nMh": ("附近森林项目反馈", False)}},
    "RMlnwgkCniMmkskeNl1ceAWwnqh": {"children": {
        "DhT7wZ6ODi1xhBk3Dj3cD8gMndh": ("协议沟通准备", False),
        "DsxVweCBMighwQkz0KbcfqUFnKb": ("玉洁沟通教练协议事宜", False),
        "KTU8wU1viiigtukUM7Qc3Mu7n0c": ("玉洁-教练服务协议", False),
        "BPtXwdcDyi6M4ckVTsFcooJhnWe": ("2026-04-20 玉洁沟通", False),
        "MEqnwXwYai5Ryjk7WHGcIY9Nnve": ("2026-02-10-玉洁_财务规划", False),
        "StIkw6CaHim8QwkbIjGcY2IZn5f": ("20251223085906-转写...", False),
        "I3zIwXgh8iRapRkM4t8c0ASPnqf": ("20251231163347-转写...", False),
        "PsvXwArzriEJ3ZkA27Icfc65nae": ("20260107154213-转写...", False),
        "Ugwdwhm0Oim6Z4k7eJvcZbFhnJe": ("20260113154516-转写...", False),
        "OxCqwn9MKio3TfkfwGMc3RiYnWf": ("20260115151714-玉洁 best year...", False),
    }},
    "PLC2wV49MiR9Nnkoc00clIUanG5": {"children": {
        "NaHvwTT4XiTUPekVFR5cpXQonZI": ("康康-教练服务协议-协议版", True),
        "WgaTw6iiFiHXnuktzaEcjkEanRh": ("画板文档", False),
        "MjpOwDi2fit35vkhUV3cMcrknqh": ("财务-家庭财务检测表-V2.xlsx", False),
        "AW2uwkHXei9Nkuk1w7Wc9CgVnZf": ("康康-家庭财务检测表.xlsx", False),
        "EcsJwMaljiMgJ5kOs7acspU6ncf": ("康康-中日保险深度对比分析", False),
        "D9dLwrEP2iX8NfkcwEgcIFebnDe": ("会议记录", True),
        "X2ldwmbcMiRDkSklDgIciyUmn0b": ("康康-教练服务协议-协议版.pdf", False),
        "Ix4lwL6jri1EFdkG6xmcxE2WnLJ": ("康康进展跟踪", False),
    }},
    "PYakwBbjoiZtBQkUnLFcy1VTnmf": {"children": {
        "F8W6wTagSi0UGtkJcbzcykitnCf": ("雅华-教练服务协议-已结束", False),
        "Vwc5wRFVhiTGuxkEIFncP60qneh": ("丁雅华-教练交付-沟通记录", True),
    }},
    # Level 3 (deepest expanded)
    "NaHvwTT4XiTUPekVFR5cpXQonZI": {"children": {"BayzwZ0qzi9l9RkrRHtcOPJnn0g": ("康康协议修改说明", False)}},
    "D9dLwrEP2iX8NfkcwEgcIFebnDe": {"children": {
        "YVSRwIG1GioxRIkJmQ4cwT6anCb": ("2026-06-03 康康 教练协议沟通", False),
        "EIg7wIEbIiFOCekLxgicCFpInZg": ("2026-06-01 康康-教练&财务沟通", False),
        "RzICwetckiIPYKkKBOLcVnkhn1c": ("2026-05-24 学了教练之后...", False),
        "Xi0RwtXotiWviKk4zgWcAUbgn1f": ("2026-05-23 康康-财务规划交流", False),
        "D99ywSSlfitOLNktpc8c3Yflnrb": ("2026-05-14 康康-交流AI&教练&财务规划", False),
        "EdshwfxdJiWNf5kjvFncSZbmn3b": ("2026-05-09 教练对话-客户康康-教练浚宇", False),
        "UQ0XwGZhPiXiEjkJjZccvslynje": ("2026.6.10 康康-3个月陪跑目标沟通", False),
    }},
    "Vwc5wRFVhiTGuxkEIFncP60qneh": {"children": {"Z165wvWoWi7OQAkFOwWcPVRjnPe": ("智能纪要：雅华 教练对话 2026年5月9日", False)}},
    # 朋友们 (expanded 2026-06-11, all leaf)
    "URyhwU4PPiO09ak1UM1cbvuXnVh": {"children": {
        "Lo4OwfEVIiBBJTkkslgcRYaznYg": ("Tapon: A Manifesto", False),
        "GByqwZXqliY54IkpyjPc7WcHnNd": ("Tapon许愿池 From 浚宇", False),
        "ENGyw6nNfiQCVFkf7dwcweYfnwf": ("tapon-...", False),
    }},
    "QtJowwdA6ipsPRkzqWwcaWefn3K": {"children": {
        "Es36wv7hMi0mVBk9tt1cbBZxnJg": ("Erin-后来之地讨论", False),
        "THfUwOfRXibZewkHaSfcS01vnGf": ("Erin-教练服务协议", False),
    }},
    "YvwawNcKniSnsBkodqFch7mpnvX": {"children": {"GEQVwcxSnitZ35kMDU3c4rkMngf": ("佳佳-教练服务协议", False)}},
    # 朱训兰 (朋友们) — has_child → false 2026-06-19
    "L6yAwCbzQiCJsskAyUBczAJlnvh": {},
    "FDs5wmaKIiSQbSk27oGcJBLKnPf": {"children": {
        "M3fSwuOvViyD4ekh5HdcP2Hvn2c": ("Sammy需求沟通复盘与后续服务设计", False),
        "AEBHw9qdGiaOsxkiTMVc6f3GnRg": ("Sammy-需求沟通", False),
    }},
    # 余了了 (朋友们) — has_child → false 2026-06-19
    "BH4hwzxnpik3ChkmrkccIYjOnRh": {},
    "KkqpwlHGcihkT0kIM52cTGu1nMf": {"children": {
        "QJltwzh7bitRRHkbVYZcxacTnfV": ("沈磊保单利益整理表20251225.xlsx", False),
        "OGoDwKS9MiKUyzkYhAEclWx1nNb": ("陈悦家庭财务规划-风险分析", False),
        "NXcVwWUtQithgykyF37csqIWn1g": ("卡卡聊保险需求", False),
        "DE8dwsWvXiamS6kYbFdciJSrn51": ("卡卡沟通小结-微信版-2026-06-05", False),
    }},
    # 首页 > 人员清单 (2026-06-21)
    "R2hnw298AihV7ekd05xc9mMBnfg": {"children": {"GaYPwhIyKiiVPpkuqETcCLkinXf": ("人员清单更新日志说明", False)}},
}


def run_lark_node_list(token, space_id=SPACE_ID):
    """Call lark-cli wiki +node-list and return parsed children dict.
    
    Uses v1.0.44+ flag-based syntax and handles dict response wrapper.
    """
    cmd = [
        "lark-cli", "wiki", "+node-list",
        "--space-id", space_id,
        "--parent-node-token", token,
        "--page-all", "--page-limit", "0",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        print(f"  ERROR: lark-cli failed (exit={result.returncode})")
        err = result.stderr.strip()[:200]
        if err:
            print(f"  stderr: {err}")
        return None

    raw = result.stdout.strip()
    if not raw:
        print("  (empty response)")
        return {}

    # Strip --page-all prefix pollution (rule 8)
    raw = re.sub(r'^\[page \d+\] fetching\.\.\.\s*', '', raw, flags=re.MULTILINE)
    raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}")
        print(f"  Raw (first 300): {raw[:300]}")
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
        print(f"  Unexpected nodes type: {type(nodes)}")
        return None

    children = {}
    for item in nodes:
        if not isinstance(item, dict):
            continue
        name = item.get("title", "unknown")
        child_token = item.get("node_token", "")
        has_child = item.get("has_child", False)
        if child_token:
            children[child_token] = (name, has_child)

    return children


def compare_and_report(token, section_label, current_children):
    """Compare current children with known existing and report new ones."""
    if token not in existing:
        if current_children:
            print(f"  NEW NODE ({len(current_children)} children)")
            for ct, (cn, ch) in current_children.items():
                flag = " [HAS_CHILD]" if ch else ""
                print(f"    | {cn} | {ct} | {ch}{flag}")
            return current_children
        return {}

    known = existing[token]["children"]
    new_children = {}

    for ct, (cn, ch) in current_children.items():
        if ct not in known:
            flag = " [HAS_CHILD]" if ch else ""
            print(f"  NEW: {cn} | {ct} | {ch}{flag}")
            new_children[ct] = (cn, ch)

    if not new_children:
        print(f"  (no new, still {len(known)} children)")
    else:
        print(f"  => {len(new_children)} new, {len(current_children)} total")

    return new_children


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--space-id", default=SPACE_ID)
    parser.add_argument("--delay", type=int, default=DELAY)
    args = parser.parse_args()

    scans = [
        # 客户相关 level 1
        ("AIjRwXudUizTKzkLJQncOEY5n6c", "客户相关 > 汤望霖 Lynn", 1),
        ("AzLLwrhIsiUNDwkFLZ2c3tX8nde", "客户相关 > 关莲", 1),
        ("Oj7swNMDViyat6k6v79cQrjvnIg", "客户相关 > 魏玉洁", 1),
        ("MFDKwCRzjiCBzakNXhMc1JBvn8b", "客户相关 > 徐正乔", 1),
        ("XEL9wk9AOisOUXk8zywcRreInee", "客户相关 > 康康", 1),
        ("Uks3wWAF7il4ZUkXvvycS5S5noQ", "客户相关 > 丁雅华", 1),
        ("JqxFwJfYiizGXik6stjcXCWgnDb", "客户相关 > 李慧", 1),
        ("KFtbwYiV3iguHvk3dmYcP7h7nIg", "客户相关 > 曾华青", 1),
        # 从朋友们移入的 5 人 (2026-06-13)
        ("KkqpwlHGcihkT0kIM52cTGu1nMf", "客户相关 > 陈悦", 1),
        ("FDs5wmaKIiSQbSk27oGcJBLKnPf", "客户相关 > 陈妮", 1),
        ("URyhwU4PPiO09ak1UM1cbvuXnVh", "客户相关 > 李博", 1),
        ("QtJowwdA6ipsPRkzqWwcaWefn3K", "客户相关 > Erin艾琳", 1),
        ("YvwawNcKniSnsBkodqFch7mpnvX", "客户相关 > 佳佳", 1),
        # level 2
        ("RMlnwgkCniMmkskeNl1ceAWwnqh", "客户相关 > 魏玉洁 > 玉洁交付清单", 2),
        ("PLC2wV49MiR9Nnkoc00clIUanG5", "客户相关 > 康康 > 康康交付文档清单", 2),
        ("PYakwBbjoiZtBQkUnLFcy1VTnmf", "客户相关 > 丁雅华 > 雅华交付清单", 2),
        # level 3 (deepest)
        ("NaHvwTT4XiTUPekVFR5cpXQonZI", "客户相关 > 康康 > 交付清单 > 协议版", 3),
        ("D9dLwrEP2iX8NfkcwEgcIFebnDe", "客户相关 > 康康 > 交付清单 > 会议记录", 3),
        ("Vwc5wRFVhiTGuxkEIFncP60qneh", "客户相关 > 丁雅华 > 交付清单 > 沟通记录", 3),
        # 首页 (NEW 2026-06-13)
        ("R2hnw298AihV7ekd05xc9mMBnfg", "首页 > 人员清单", 1),
        # 朋友们 — 朱训兰、余了了 has_child→false 2026-06-19，已移除
    ],

    all_new_discoveries = {}
    total = len(scans)

    for i, (token, label, depth) in enumerate(scans):
        print(f"\n[{i+1}/{total}] Scanning: {label}")
        print(f"  token: {token}")

        children = run_lark_node_list(token, args.space_id)
        if children is None:
            print(f"  SKIPPED (API error)")
            continue

        print(f"  Found {len(children)} children")
        new = compare_and_report(token, label, children)
        if new:
            all_new_discoveries[token] = {
                "label": label,
                "depth": depth,
                "children": new,
                "all_children": children,
            }

        if i < total - 1:
            time.sleep(args.delay)

    print("\n" + "="*60)
    print("SCAN COMPLETE")
    print("="*60)

    if all_new_discoveries:
        total_new = sum(len(v["children"]) for v in all_new_discoveries.values())
        print(f"\nNEW DISCOVERIES: {total_new} nodes across {len(all_new_discoveries)} parents")
        for token, info in all_new_discoveries.items():
            print(f"\n  {info['label']}:")
            for ct, (cn, ch) in info["children"].items():
                flag = "[HAS_CHILD]" if ch else "[LEAF]"
                print(f"    {flag} {cn} | {ct}")
    else:
        print("\nNo new paths found.")

    return 0 if not all_new_discoveries else 1


if __name__ == "__main__":
    sys.exit(main())
