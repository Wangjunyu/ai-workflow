# GitHub API Cheat Sheet

Use when `gh` is unavailable and the workflow falls back to `git` + `curl`.

## Detect owner/repo
```bash
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

## Common endpoints
- `GET /repos/$OWNER/$REPO/pulls/<n>`
- `GET /repos/$OWNER/$REPO/pulls/<n>/files`
- `POST /repos/$OWNER/$REPO/pulls`
- `POST /repos/$OWNER/$REPO/issues/<n>/comments`
- `PUT /repos/$OWNER/$REPO/pulls/<n>/merge`
