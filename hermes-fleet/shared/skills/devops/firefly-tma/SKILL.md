---
name: firefly-tma
description: Manage firefly's tmux session picker (tma) — the SSH entry point that auto-launches Hermes profile sessions. Use when modifying tma behavior, adding new profiles to the menu, debugging auto-launch issues, or understanding the tma + .bashrc integration.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [firefly, tmux, tma, ssh, session, profile, devops]
    related_skills: [hermes-agent, hermes-profile-setup]
---

# Firefly TMA — Tmux Session Picker

## Overview

`tma` (`~/.local/bin/tma`) is firefly's SSH entry point. On interactive login, `.bashrc` automatically executes `tma`, presenting a menu of active tmux sessions and the option to create new ones.

New sessions are created by piping Hermes profiles directly into the menu — no two-step submenu.

## When to Use

- User says "修一下 tma" / "改 tma"
- New Hermes profile created — tma auto-discovers from `~/.hermes/profiles/`
- SSH login loops (plain shell → tma → exit → tma → ...)
- User wants to bypass tma on login

## How It Works

### Auto-Launch (`.bashrc` line 122-124)

```bash
if [[ $- == *i* ]] && [ -z "${TMUX:-}" ] && [ -z "${NO_TMUX:-}" ] && command -v tma >/dev/null 2>&1; then
  exec tma
fi
```

Conditions: interactive shell + not in tmux + `NO_TMUX` not set + tma exists.

### Bypass

```bash
NO_TMUX=1 ssh firefly    # Skip tma on login
```

Or press `s` in the tma menu for a plain shell.

### New Session Menu

When pressing `n`, tma scans `~/.hermes/profiles/` and presents:

```
New session:
  1) default (Hermes)
  2) biz-intake (Hermes)
  3) biz-planner (Hermes)
  4) f-baby_love (Hermes)
  5) Others (plain shell)
Choice:
```

- Options 1-N: creates `hermes` / `hermes-<profile>` session, auto-executes `hermes` or `hermes --profile <profile>`
- Last option: prompts for name, creates plain shell session

### Profile Auto-Discovery

tma scans `${HERMES_HOME:-$HOME/.hermes}/profiles/` at menu time — new profiles appear automatically without editing tma.

## File Locations

| File | Purpose |
|------|---------|
| `~/.local/bin/tma` | Main script |
| `~/.bashrc` | Auto-launch trigger (line 122-124) |

## Common Pitfalls

1. **Plain shell loop**: Without `NO_TMUX=1 exec bash` in the `s` option, exiting a plain shell re-enters tma infinitely. Already fixed.
2. **`local` keyword in case block**: `local` only works inside functions, not in `case` blocks in the main script body. Use plain assignment.
3. **Profile not showing**: Profiles are scanned at menu time. If `hermes profile create` just ran, the new profile will appear next time `n` is pressed — no restart needed.
4. **tma changes not taking effect**: SSH re-login needed (new bash session). Or run `exec tma` to restart.

## Verification Checklist

- [ ] `bash -n ~/.local/bin/tma` passes syntax check
- [ ] SSH login lands on tma menu
- [ ] `n` shows all profiles + Others
- [ ] Selecting a Hermes profile launches `hermes --profile <name>` correctly
- [ ] `NO_TMUX=1 ssh firefly` bypasses tma
- [ ] `s` in menu gives plain shell
