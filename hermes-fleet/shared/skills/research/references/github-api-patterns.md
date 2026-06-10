# GitHub API Research Patterns

Tested and working from datacenter/shared IPs where DuckDuckGo and Google are blocked.

## curl boilerplate

```bash
curl -s --connect-timeout 5 --max-time 12 \
  "https://api.github.com/..." \
  -H "User-Agent: curl/8.0"
```

Always use `--connect-timeout` and `--max-time` — GitHub API can hang indefinitely on some networks.

## Endpoint recipes

### Repo metadata

```bash
curl ... "https://api.github.com/repos/{owner}/{repo}" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); \
  print(f'stars={d[\"stargazers_count\"]}, desc={d[\"description\"]}')"
```

### Search repos (discover projects in a space)

```bash
curl ... "https://api.github.com/search/repositories?q={query}&sort=stars&per_page=5"
```

Parse with:
```python
for r in d.get('items',[]):
    print(f'{r["full_name"]}: stars={r["stargazers_count"]}, desc={r.get("description","")[:120]}')
```

### Raw README (best source of documentation)

```bash
curl ... "https://api.github.com/repos/{owner}/{repo}/readme" \
  -H "Accept: application/vnd.github.raw"
```

The `Accept` header is critical — without it you get JSON metadata, with it you get raw markdown.

### Code search (find features in an org)

```bash
curl ... "https://api.github.com/search/code?q={query}+org:{org_name}&per_page=5"
```

### Multiple repos in a loop

```bash
for repo in owner1/repo1 owner2/repo2 owner3/repo3; do
  data=$(curl -s --connect-timeout 5 --max-time 10 \
    "https://api.github.com/repos/$repo" -H "User-Agent: curl/8.0")
  echo "$repo: $(echo "$data" | python3 -c "...")"
done
```

## Parsing patterns

Use `python3 -c` inline (not `jq`, which may not be installed):

```python
# Safe access — repos can return null for any field
d.get("stargazers_count", "?")
d.get("description", "")[:120]

# Items list from search
for r in d.get('items',[]): ...
```

## When GitHub also fails

Try package registries:
- PyPI: `https://pypi.org/pypi/{package}/json`
- npm: `https://registry.npmjs.org/{package}/latest`

Or fall back to model training knowledge with explicit caveats.

## Real example from 2026-06 session

Researched AI agent memory frameworks. Web search (DuckDuckGo, Google) both returned empty — likely IP-based blocking. Pivoted to GitHub API:

1. `search/repositories?q=MemGPT+agent+memory` → discovered renaming to Letta
2. Fetched 10+ repo metadata endpoints for star counts and descriptions
3. Pulled raw READMEs for Mem0, Letta, Zep, Graphiti → architecture details
4. Compiled 388-line structured markdown report
