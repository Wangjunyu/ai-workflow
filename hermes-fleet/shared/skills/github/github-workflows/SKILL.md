---
name: github-workflows
description: "Use when working with GitHub repositories, pull requests, reviews, auth, issues, releases, and repo administration as one connected workflow."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, git, pull-requests, code-review, repositories, releases, issues, auth]
    related_skills: [github-auth]
---

# GitHub Workflows

## Overview

This is the umbrella skill for day-to-day GitHub operational work: repository setup, remotes, forks, branch/PR lifecycle, code review, CI follow-up, releases, and related repo administration. Prefer one broad GitHub workflow skill over separate narrow PR/review/repo-management skills when the real task crosses those boundaries.

The class-level rule: GitHub work usually flows through a shared lifecycle:
1. authenticate,
2. discover repo context,
3. branch or clone,
4. implement or inspect,
5. open or review a PR,
6. monitor CI,
7. merge or release.

Load this skill whenever the user asks for GitHub work that could touch more than one of those stages.

## When to Use

- Creating, cloning, forking, or configuring repositories
- Opening, updating, reviewing, or merging pull requests
- Investigating CI failures on a PR
- Managing remotes, branches, releases, labels, or repo metadata
- Performing GitHub work where the exact subtask is not yet known

## Core Operating Pattern

### 1. Establish auth and remote context

Prefer `gh` when available; otherwise use `git` plus `curl`/API.

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
fi

REMOTE_URL=$(git remote get-url origin 2>/dev/null || true)
if [ -n "$REMOTE_URL" ]; then
  OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
  OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
  REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
fi
```

If `gh` is unavailable, load `github-auth` and confirm token-backed API access before attempting PR/review/release actions.

### 2. Pick the workflow lane

#### Lane A — Repository management
Use for create/clone/fork/remote/release/admin work.
- clone or fork repo
- inspect remotes and default branch
- configure secrets/variables/settings if needed
- prepare branch/worktree

#### Lane B — PR lifecycle
Use for branch → commit → push → PR → CI → merge.
- create branch
- make scoped changes
- push
- open PR with explicit summary and test plan
- watch CI and fix failures iteratively
- merge with the appropriate method

#### Lane C — Code review
Use for reviewing local diffs or remote PRs.
- inspect diff summary first
- read changed files with full context
- run targeted tests when possible
- produce structured findings
- post inline comments or a formal review if asked

## Subsections absorbed from narrower skills

### Pull request workflow

Use conventional branch names:
- `feat/<desc>`
- `fix/<desc>`
- `refactor/<desc>`
- `docs/<desc>`
- `ci/<desc>`

Typical flow:

```bash
git fetch origin
git checkout main && git pull origin main
git checkout -b fix/example-issue
git add <files>
git commit -m "fix: concise description"
git push -u origin HEAD
```

Create the PR with `gh pr create` when possible. Include:
- summary of changes
- test plan
- issue links (`Closes #N`) when relevant

Watch CI:

```bash
gh pr checks --watch
```

If CI fails:
1. inspect failing run/logs,
2. reproduce locally,
3. fix minimally,
4. push,
5. re-check CI.

### Code review workflow

Start broad, then drill down:

```bash
git diff main...HEAD --stat
git log main..HEAD --oneline
git diff main...HEAD --name-only
```

Review by category:
- correctness
- security
- code quality
- testing
- performance
- docs

Output structure:
- Critical
- Warnings
- Suggestions
- Looks Good

For remote PRs:
- `gh pr view <N>`
- `gh pr diff <N>`
- `gh pr checkout <N>` when local execution/context is useful

### Repository management workflow

Use for:
- clone/create/fork
- remote setup
- repo metadata and settings
- release flow
- baseline admin tasks

Keep repo work scoped and explicit: do not mix unrelated admin cleanup into a PR task unless the user asked.

## References and templates

This umbrella centralizes detailed support files from narrower GitHub skills:
- `references/review-output-template.md`
- `references/ci-troubleshooting.md`
- `references/conventional-commits.md`
- `references/github-api-cheatsheet.md`
- `templates/pr-body-bugfix.md`
- `templates/pr-body-feature.md`

Use support files for detailed one-topic artifacts rather than spawning more micro-skills.

## Common Pitfalls

1. Treating repo, PR, and review work as unrelated classes. In practice they are one GitHub workflow family.
2. Reviewing only the diff without reading surrounding file context.
3. Claiming CI is fixed without re-running checks or watching the new run complete.
4. Mixing local git state assumptions with remote GitHub state; verify both.
5. Opening or merging PRs without a clear summary/test plan.

## Verification Checklist

- [ ] Auth method confirmed (`gh` or token/API fallback)
- [ ] Correct `owner/repo` identified
- [ ] Chosen lane matches the user's GitHub task
- [ ] Any PR includes summary + test plan
- [ ] Any review is backed by actual diff/file inspection
- [ ] Any CI claim is backed by real check status
- [ ] Any merge/release action is verified after execution
