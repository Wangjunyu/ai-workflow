#!/usr/bin/env python3
"""
Daily Feishu minutes search — segmented by date, output to file.

USAGE:
    python3 scripts/minutes-daily-search.py [--days N] [--output FILE]

    Searches the past N days (default 8) one day at a time via:
      lark-cli minutes +search --as user --format json --participant-ids me
                              --start $DATE --end $DATE --page-size 30

    Saves raw per-day JSON to /tmp/minutes_search/<date>.json,
    then writes deduplicated results to --output (default /tmp/minutes_result.json).

PITFALL: lark-cli truncates token fields when stdout is a TTY.
         This script redirects to file (> outfile) to preserve full tokens.
         Do NOT capture stdout via subprocess.PIPE — use shell redirect.
"""
import subprocess
import json
import re
import sys
import os
import argparse
from datetime import date, timedelta


def parse_args():
    p = argparse.ArgumentParser(description="Search Feishu minutes by date segments")
    p.add_argument("--days", type=int, default=8,
                   help="Number of past days to search (default: 8, covers today + 7 days)")
    p.add_argument("--output", default="/tmp/minutes_result.json",
                   help="Output JSON file (default: /tmp/minutes_result.json)")
    p.add_argument("--tmpdir", default="/tmp/minutes_search",
                   help="Temp directory for per-day raw JSON (default: /tmp/minutes_search)")
    p.add_argument("--today", help="Override today's date (YYYY-MM-DD, default: system date)")
    return p.parse_args()


def main():
    args = parse_args()

    if args.today:
        today = date.fromisoformat(args.today)
    else:
        today = date.today()

    start = today - timedelta(days=args.days - 1)
    os.makedirs(args.tmpdir, exist_ok=True)

    all_minutes = []
    errors = []

    for i in range(args.days):
        d = start + timedelta(days=i)
        date_str = d.strftime("%Y-%m-%d")
        outfile = os.path.join(args.tmpdir, f"{date_str}.json")

        # MUST use shell redirect (> file) to avoid TTY truncation (rule 17)
        cmd = (
            f"cd /home/leon && "
            f"npx @larksuite/cli minutes +search "
            f"--as user --format json --participant-ids me "
            f"--start {date_str} --end {date_str} --page-size 30 "
            f"> {outfile} 2>&1"
        )

        try:
            # Rule 18: npx needs TERM set
            penv = os.environ.copy()
            penv["TERM"] = "dumb"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=45, env=penv)

            if not os.path.exists(outfile) or os.path.getsize(outfile) == 0:
                errors.append(f"{date_str}: no output file")
                print(f"  {date_str}: NO OUTPUT", file=sys.stderr)
                continue

            with open(outfile, 'r') as f:
                raw = f.read().strip()

            # Strip npm notices / non-JSON prefix before opening brace
            idx = raw.find('{')
            if idx > 0:
                raw = raw[idx:]

            # Strip npm notices / trailing cruft after JSON object close
            # (npm prints notices to stderr which get merged via 2>&1)
            # Find the last '}' at outermost nesting level
            depth = 0
            last_close = -1
            for i, ch in enumerate(raw):
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        last_close = i
            if last_close > 0:
                raw = raw[:last_close + 1]

            data = json.loads(raw)
            items = data.get("data", {}).get("items", [])

            for item in items:
                minute = {
                    "token": item.get("token", ""),
                    "date": date_str
                }

                display = item.get("display_info", "")
                lines = display.split("\n")
                title = lines[0].strip() if lines else "无标题"
                title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
                minute["title"] = title

                desc = item.get("meta_data", {}).get("description", "")
                combined = display + desc

                dm = re.search(r"时长:\s*(.+?)(?:所有者:|$)", combined)
                minute["duration"] = dm.group(1).strip() if dm else "未知"

                sm = re.search(r"开始时间:\s*(\d{4}\.\d{2}\.\d{2}\s*\d{2}:\d{2}:\d{2})", combined)
                minute["start_time"] = sm.group(1) if sm else date_str

                all_minutes.append(minute)

            print(f"  {date_str}: {len(items)} results", file=sys.stderr)

        except subprocess.TimeoutExpired:
            errors.append(f"{date_str}: timeout")
            print(f"  {date_str}: TIMEOUT", file=sys.stderr)
        except json.JSONDecodeError as e:
            errors.append(f"{date_str}: JSON parse error: {e}")
            print(f"  {date_str}: JSON ERROR", file=sys.stderr)
        except Exception as e:
            errors.append(f"{date_str}: {e}")
            print(f"  {date_str}: ERROR - {e}", file=sys.stderr)

    # Deduplicate by token
    seen = set()
    unique = []
    for m in all_minutes:
        if m["token"] not in seen:
            seen.add(m["token"])
            unique.append(m)

    output = {
        "minutes": unique,
        "errors": errors,
        "total": len(unique),
        "search_range": f"{start} to {today}"
    }

    with open(args.output, 'w') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Print compact summary to stdout
    print(f"Total: {len(unique)} minutes ({start} to {today})")
    if errors:
        print(f"Errors: {len(errors)}")
    for m in unique:
        print(f"  {m['date']} | {m['token']} | {m['title']} | {m['duration']}")


if __name__ == "__main__":
    main()
