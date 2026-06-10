---
name: obsidian-cli
description: Interact with Obsidian vaults using the Obsidian CLI — read, create, search, and manage notes, tasks, properties, and more. Requires Obsidian running on the remote Mac mini. Use when the user asks to interact with their Obsidian vault, manage notes, search vault content, or perform vault operations.
version: 1.0.0
author: kepano / adapted for Hermes
license: MIT
metadata:
  hermes:
    tags: [obsidian, cli, notes, vault]
    related_skills: [obsidian-markdown, obsidian]
---

# Obsidian CLI (via Remote Mac mini)

Use the `obsidian` CLI on the remote Mac mini (connected via Tailscale SSH). Requires Obsidian to be running on the Mac mini.

## Critical: Remote Execution

All `obsidian` commands MUST be executed on the Mac mini via SSH:

```bash
ssh mac-mini "obsidian <command>"
```

NOT locally. The `obsidian` CLI only works where Obsidian is running.

## Prerequisites

- Obsidian 1.12.7+ installed on Mac mini at `/Applications/Obsidian.app`
- CLI enabled: Settings → General → Enable "Command Line Interface"
- Obsidian MUST be running (otherwise first command will auto-launch it)
- SSH access via `ssh mac-mini` (Tailscale, key auth configured)

## Vault Info

- Path: `/Users/leon-home/leon-obsidian`
- Vault name: `leon-obsidian`

## Command Reference

Run `ssh mac-mini "obsidian help"` to see all available commands.

## Syntax

**Parameters** take a value with `=`:

```bash
ssh mac-mini "obsidian create name=\"My Note\" content=\"Hello world\""
```

**Flags** are boolean switches:

```bash
ssh mac-mini "obsidian create name=\"My Note\" silent overwrite"
```

For multiline content use `\n` for newline and `\t` for tab.

## File Targeting

- `file=<name>` — resolves like a wikilink
- `path=<path>` — exact path from vault root, e.g. `folder/note.md`

## Vault Targeting

Commands target the most recently focused vault by default. Use `vault=<name>` to target a specific vault:

```bash
ssh mac-mini "obsidian vault=\"leon-obsidian\" search query=\"test\""
```

## Common Patterns

```bash
ssh mac-mini "obsidian read file=\"My Note\""
ssh mac-mini "obsidian create name=\"New Note\" content=\"# Hello\" silent"
ssh mac-mini "obsidian append file=\"My Note\" content=\"New line\""
ssh mac-mini "obsidian search query=\"search term\" limit=10"
ssh mac-mini "obsidian daily:read"
ssh mac-mini "obsidian daily:append content=\"- [ ] New task\""
ssh mac-mini "obsidian property:set name=\"status\" value=\"done\" file=\"My Note\""
ssh mac-mini "obsidian tasks daily todo"
ssh mac-mini "obsidian tags sort=count counts"
ssh mac-mini "obsidian backlinks file=\"My Note\""
```

Use `silent` to prevent files from opening. Use `total` on list commands to get a count.

## Common Pitfalls

1. **Obsidian not running.** CLI needs the Obsidian app running. First command will auto-launch it, but it takes a moment.
2. **Wrong vault.** If you have multiple vaults, the CLI targets the most recently focused one. Use `vault=<name>` to be explicit.
3. **SSH quoting.** Double-nested quotes need escaping: outer for SSH, inner for obsidian params. Use escaped double quotes: `ssh mac-mini "obsidian create name=\"Note\" content=\"text\""`
4. **CLI not enabled.** Must be manually enabled in Obsidian Settings → General → "Command Line Interface" first.
