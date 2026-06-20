#!/usr/bin/env python3
"""Daily Feishu minutes index sync — segmented by day. Handles lark-cli search response format."""
import subprocess
import json
import os
import re
from datetime import date, timedelta, datetime

TODAY = date.today()
WEEK_AGO = TODAY - timedelta(days=7)

OUTPUT_DIR = os.path.expanduser("~/.hermes/hermes-agent/skills/devops/infra-ops-sop/references")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "minutes-index.md")

penv = os.environ.copy()
penv["TERM"] = "dumb"


def run_lark_search(start_date, end_date):
    """Run lark-cli minutes +search, return parsed items list."""
    cmd = (
        f'npx @larksuite/cli minutes +search'
        f' --as user'
        f' --format json'
        f' --participant-ids "me"'
        f' --start "{start_date}"'
        f' --end "{end_date}"'
        f' --page-size 30'
    )
    tmpfile = f"/tmp/minutes_{start_date}.json"
    full_cmd = f"{cmd} > {tmpfile} 2>&1"

    print(f"  Searching {start_date}..{end_date} ... ", end="", flush=True)
    subprocess.run(full_cmd, shell=True, text=True, timeout=90, env=penv)

    try:
        with open(tmpfile, 'r') as f:
            raw = f.read()
    except FileNotFoundError:
        print("NO FILE")
        return []

    if raw.strip() == "":
        print("empty")
        return []

    # Strip lark-cli prefixes before JSON
    raw = re.sub(r'^\[page \d+\] fetching\.\.\.\s*', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'^Found \d+ node\(s\)\s*\n?', '', raw, flags=re.MULTILINE)
    raw = raw.strip()

    if not raw:
        print("empty (after strip)")
        return []

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON ERR: {e}")
        return []

    items = []
    if isinstance(data, dict) and data.get("ok"):
        inner = data.get("data", {})
        search_items = inner.get("items", [])
    elif isinstance(data, list):
        search_items = data
    else:
        print(f"unexpected type: {type(data)}")
        return []

    for it in search_items:
        parsed = parse_search_item(it)
        if parsed:
            items.append(parsed)

    print(f"{len(items)} found")
    try:
        os.remove(tmpfile)
    except:
        pass

    return items


def parse_search_item(item):
    """Parse a lark-cli minutes +search result item.

    Structure:
    {
      "display_info": "TITLE\\n<b>关键词:</b> ...\\n所有者: X 开始时间: YYYY.MM.DD HH:MM:SS 时长: X 小时 Y 分 Z 秒",
      "meta_data": {
        "app_link": "https://rcnsiaef7x5y.feishu.cn/minutes/FULL_TOKEN",
        "description": "..."
      },
      "token": "truncated...suffix"   # <- TRUNCATED, don't use
    }
    """
    display = item.get("display_info", "")
    meta = item.get("meta_data", {})

    # Extract full token from app_link URL
    app_link = meta.get("app_link", "")
    token = ""
    m = re.search(r'/minutes/(\w{20,})', app_link)
    if m:
        token = m.group(1)
    else:
        # Fallback: use truncated token (not ideal)
        token = item.get("token", "")

    # Parse display_info
    lines = display.split('\n')
    topic = lines[0].strip() if lines else "未知会议"

    # Parse date/time from display_info (format: "开始时间: 2026.06.20 21:38:14")
    dt = None
    time_str = "?"
    m = re.search(r'开始时间:\s*(\d{4})\.(\d{2})\.(\d{2})\s+(\d{2}):(\d{2}):(\d{2})', display)
    if m:
        try:
            dt = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                         int(m.group(4)), int(m.group(5)), int(m.group(6)))
            time_str = dt.strftime("%H:%M")
        except:
            pass

    # Parse duration from display_info (format: "时长: X 小时 Y 分 Z 秒" or "时长: Y 分 Z 秒")
    duration_str = "未知"
    m = re.search(r'时长:\s*(.+)', display)
    if m:
        raw_dur = m.group(1).strip()
        # Normalize: "1 小时 6 分 10 秒" → "1h6m10s"
        dur = raw_dur
        # Convert spaces to compact
        dur_simple = dur.replace(' 小时 ', 'h').replace(' 小时', 'h').replace(' 分 ', 'm').replace(' 秒', 's').replace(' ', '')
        # Also handle "5 分 26 秒" → "5m26s"
        dur_simple = re.sub(r'(\d+)h', r'\1h', dur_simple)
        dur_simple = re.sub(r'(\d+)m', r'\1m', dur_simple)
        dur_simple = re.sub(r'(\d+)s', r'\1s', dur_simple)
        duration_str = dur_simple

    # Status — not available in search results; assume ✅
    status_str = "✅"

    return {
        "topic": topic,
        "token": token,
        "dt": dt,
        "time_str": time_str,
        "duration_str": duration_str,
        "status_str": status_str,
    }


def main():
    print(f"=== 妙记每日索引同步 ===")
    print(f"  日期范围: {WEEK_AGO} ~ {TODAY}")

    all_minutes = []

    current = WEEK_AGO
    while current <= TODAY:
        items = run_lark_search(current.isoformat(), current.isoformat())
        all_minutes.extend(items)
        current += timedelta(days=1)

    # Sort by datetime descending
    all_minutes.sort(key=lambda m: m["dt"] or datetime(2000, 1, 1), reverse=True)

    # Group by date
    by_date = {}
    for m in all_minutes:
        date_key = m["dt"].strftime("%Y-%m-%d") if m["dt"] else "未知日期"
        by_date.setdefault(date_key, []).append(m)

    total = len(all_minutes)
    print(f"\n  总计: {total} 场妙记")

    # Build markdown
    lines = []
    lines.append("# 飞书妙记索引")
    lines.append("")
    lines.append(f"> 最后更新: {TODAY.isoformat()} (cron: minutes-index-daily-sync)")
    lines.append(f"> 数据范围: 近7天 ({WEEK_AGO.isoformat()} ~ {TODAY.isoformat()})")
    lines.append("> 搜索身份: user (浚宇)")
    lines.append("")
    lines.append("## 统计概览")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("|------|------|")
    lines.append(f"| 近7天总数 | {total} |")
    lines.append(f"| 近24h新增 | — (from search, coarse granularity) |")
    lines.append(f"| 搜索时间 | {TODAY.isoformat()} |")
    lines.append("")
    lines.append("## 近7天妙记列表")
    lines.append("")

    all_dates = []
    d = TODAY
    while d >= WEEK_AGO:
        all_dates.append(d)
        d -= timedelta(days=1)

    weekdays_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    link_lines = []
    link_lines.append("## 链接速查")
    link_lines.append("")
    link_lines.append("| 标题 | 链接 |")
    link_lines.append("|------|------|")

    for d in all_dates:
        d_str = d.isoformat()
        wd = weekdays_cn[d.weekday()]
        day_minutes = by_date.get(d_str, [])

        lines.append(f"### {d_str} ({wd}) — {len(day_minutes)} 场")
        lines.append("")

        if not day_minutes:
            lines.append("_今日暂无妙记。_")
            lines.append("")
            continue

        display = day_minutes[:5]
        more = len(day_minutes) - 5 if len(day_minutes) > 5 else 0

        lines.append("| # | 标题 | Token | 开始时间 | 时长 | 状态 |")
        lines.append("|---|------|-------|----------|------|------|")

        for i, m in enumerate(display, 1):
            lines.append(
                f"| {i} | {m['topic']} | `{m['token']}` | {m['time_str']} | {m['duration_str']} | {m['status_str']} |"
            )
            link_lines.append(
                f"| {m['topic']} | https://rcnsiaef7x5y.feishu.cn/minutes/{m['token']} |"
            )

        if more > 0:
            lines.append(f"| ... | _+{more} more_ | | | | |")

        lines.append("")

    lines.extend(link_lines)
    lines.append("")

    output = "\n".join(lines)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        f.write(output)

    print(f"  ✓ 写入 {OUTPUT_FILE}")
    print(f"  ✓ 总计 {total} 场")

    # Summary
    print("\n===SUMMARY===")
    print(f"TOTAL={total}")
    for d in reversed(all_dates):
        d_str = d.isoformat()
        cnt = len(by_date.get(d_str, []))
        if cnt > 0:
            names = [m["topic"][:40] for m in by_date.get(d_str, [])[:5]]
            print(f"{d_str}: {cnt} - {', '.join(names)}")


if __name__ == "__main__":
    main()
