---
name: technical-research
description: Research technical topics, frameworks, and landscapes from the terminal. Covers GitHub API, package registries, and fallback strategies when web search is blocked or unreliable.
category: research
---

# Technical Research

Use when the user asks you to research a technical topic, survey a landscape, compare frameworks, or compile a structured report from terminal-accessible data sources.

**Default deliverable**: structured markdown summary saved to the working directory (or user-specified path).

## Workflow

### 1. Web search first

Try DuckDuckGo Lite or Google as the primary discovery channel. Accept that these often fail — timeouts, empty results, or captcha walls are normal in shared-IP environments. Set a tight timeout (10–15s) and move on if it blocks.

### 2. GitHub API as primary fallback

When web search is blocked, GitHub API is the most reliable structured data source for technical topics.

Load the reference: `skill_view(name='technical-research', file_path='references/github-api-patterns.md')` for curl recipes, endpoint catalog, and parsing patterns. Key capabilities below.

Key capabilities:
- **Repo discovery**: `search/repositories` by topic, sorted by stars — reveals popularity and ecosystem
- **Metadata**: individual repo endpoints for stars, description, topics, last-updated
- **Deep content**: raw README fetch via `Accept: application/vnd.github.raw` header — frontline documentation
- **Code search**: `search/code` scoped to orgs — find features, patterns, implementations

### 3. Package registries for ecosystem data

Use PyPI and npm registries to get version info, descriptions, and dependency graphs:
- PyPI: `https://pypi.org/pypi/{package}/json`
- npm: `https://registry.npmjs.org/{package}/latest`

### 4. Compile the report

Structure findings into a markdown document with:
- A clear title and date
- Table of contents if the report spans multiple sections
- Tables for comparison data (stars, features, tradeoffs)
- Architecture diagrams in ASCII or described in prose
- A recommendations/summary section at the end
- Source attribution in a footer

### Pitfalls

- **DuckDuckGo Lite often returns empty HTML** — don't retry more than twice. Switch to GitHub API immediately.
- **Google returns captcha pages** on shared/datacenter IPs. Again, don't retry — pivot.
- **GitHub API rate limits**: 60 req/hr unauthenticated, 5000/hr with token. Use `--connect-timeout 5 --max-time 12` on every curl call to avoid hanging.
- **Wikipedia API may also be blocked** — don't rely on it being available.
- **Repo names change**: MemGPT → Letta is a real example. Use `search/repositories` to find the current canonical name, not guesses.
