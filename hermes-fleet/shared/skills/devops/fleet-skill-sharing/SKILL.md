---
name: fleet-skill-sharing
description: Share Hermes skills across machines via the ai-workflow/hermes-fleet repo. Use when adding a shared skill, deploying skills to remote machines, troubleshooting missing skills on a profile, or understanding the skill deployment pipeline.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [fleet, skills, deployment, cross-machine, devops]
    related_skills: [hermes-agent, hermes-profile-setup]
---

# Fleet Skill Sharing — Cross-Machine Skill Deployment

## Overview

Skills in `ai-workflow/hermes-fleet/shared/skills/` are the canonical skill pool. They get deployed to `~/.hermes/skills/` on every machine, ensuring consistent tooling regardless of which machine the agent runs on.

## When to Use

- User asks "how do I share skills across machines?"
- A skill exists on one machine but not others — time to add it to the pool
- New shared skill created — need to deploy
- Profile shows missing local skills — deployment issue
- User says "为什么这个 skill 在 X 机器上没有?"

## Architecture

```
hermes-fleet/
  shared/skills/                ← Canonical skill pool (Git)
    <category>/
      <skill-name>/
        SKILL.md
        references/             (optional)
        templates/              (optional)
        scripts/                (optional)
```

Skills are deployed to TWO locations on each machine:

1. **`~/.hermes/skills/`** — Global, used by profiles WITHOUT their own skills dir
2. **`~/.hermes/profiles/<name>/skills/`** — Per-profile, for profiles WITH their own skills dir (like bulma)

Both locations must be kept in sync. `render.py` handles this automatically.

## Workflow

### Adding a New Shared Skill

```bash
# 1. Place skill in fleet repo
mkdir -p ~/ai-workflow/hermes-fleet/shared/skills/<category>/<skill-name>/
cp -r ~/.hermes/skills/<category>/<skill-name>/* \
      ~/ai-workflow/hermes-fleet/shared/skills/<category>/<skill-name>/

# 2. Commit
cd ~/ai-workflow
git add hermes-fleet/shared/skills/
git commit -m "fleet: add shared skill <skill-name>"
git push
```

### Deploying to Machines

```bash
# Deploy to a remote machine (mac-mini, MBP)
tar czf - -C ~/ai-workflow/hermes-fleet/shared/skills . | \
  ssh <user>@<host> 'mkdir -p ~/.hermes/skills && tar xzf - -C ~/.hermes/skills/'

# Also deploy to profile-specific skills (for profiles like bulma)
ssh <user>@<host> 'mkdir -p ~/.hermes/profiles/<name>/skills/<category> && \
  cp -r ~/.hermes/skills/<category>/<skill-name> ~/.hermes/profiles/<name>/skills/<category>/'

# Restart gateway if profile is a bot
ssh <user>@<host> 'hermes -p <name> gateway restart'
```

### For firefly (local machine)

```bash
cp -r ~/ai-workflow/hermes-fleet/shared/skills/* ~/.hermes/skills/
```

## Deployment Mechanism

`render.py` (lines 106-120) handles staging:
1. Copies `shared/skills/` → `staging/shared/skills/` (global)
2. Copies each skill dir → `staging/profiles/<name>/skills/` (per-profile)

`sync.sh` handles delivery:
1. `staging/shared/skills/` → `~/.hermes/skills/` (rsync or tar+ssh)
2. `staging/profiles/<name>/` → `~/.hermes/profiles/<name>/` (includes skills/)

## Verification

After deployment, verify skills are visible:

```bash
# Check default profile (uses global skills)
hermes -p default skills list | grep local

# Check bot profiles (use per-profile skills)
hermes -p bulma skills list | grep local

# Count local skills
hermes -p <name> skills list | grep -c "local"
```

## What NOT to Share

Machine-specific skills that depend on OS-specific tools:

- `apple/*` — macOS only (Apple Notes, Reminders, iMessage, etc.)
- `iterm2-config` — macOS terminal only
- `macos-computer-use` — macOS accessibility APIs

These stay local to the machine that needs them.

## Current Shared Skills (15)

| Skill | Category | Source | Purpose |
|-------|----------|--------|---------|
| git-firefly-bridge | devops | MBP | Git push/pull via firefly when direct GitHub blocked |
| obsidian-cli | note-taking | MBP | Obsidian CLI operations |
| obsidian-workflows | note-taking | mac-mini | Obsidian workflow patterns |
| daily-review | productivity | MBP | Daily AI usage review → Journal |
| file-organization | productivity | MBP | Organize cluttered directories |
| poe-platform | productivity | MBP | Poe.com platform capabilities |
| feishu-document-api | productivity | mac-mini | Feishu REST API for doc/minutes access |
| technical-research | research | MBP | Technical topic research from terminal |
| github-workflows | github | mac-mini | GitHub PR/review/issue workflows |
| music-generation-workflows | media | mac-mini | AI music generation |
| telegram-bot-development | social-media | mac-mini | Telegram bot with python-telegram-bot |
| agent-memory-stack-debugging | software-dev | mac-mini | Diagnose memory stack failures |
| debugging-workflows | software-dev | mac-mini | Root-cause debugging workflows |
| local-knowledge-capture | software-dev | mac-mini | Capture work into knowledge base |
| feishu-doc-finder | (root) | mac-mini | Find docs inside Feishu wiki |

## Common Pitfalls

1. **Profile has own skills dir but shared skills not copied there**: Profiles like `bulma` with their own `skills/` directory only look at their own copy, NOT `~/.hermes/skills/`. Must deploy to both locations.

2. **rsync not available on target**: Some Linux VMs (like firefly) don't have rsync. Use `tar czf - ... | ssh ... tar xzf -` as fallback.

3. **Gateway cache**: After deploying new skills to a bot profile, restart the gateway: `hermes -p <name> gateway restart`.

4. **.bundled_manifest**: This file tracks built-in skills only. New shared skills appear as "local" — no manifest update needed.

5. **Skill not showing after deploy**: Run `hermes -p <name> skills list` to verify. If missing, check both locations (`~/.hermes/skills/` and `~/.hermes/profiles/<name>/skills/`).

## Verification Checklist

- [ ] Skill file in `shared/skills/<category>/<name>/SKILL.md` with valid frontmatter
- [ ] `git add` + `git commit` + `git push` completed
- [ ] Deployed to all target machines (tar+ssh)
- [ ] Deployed to per-profile skills dirs for bot profiles
- [ ] Bot profile gateway restarted
- [ ] `hermes -p <name> skills list | grep local` confirms visibility
