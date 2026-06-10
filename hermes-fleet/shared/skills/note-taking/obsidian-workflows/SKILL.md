---
name: obsidian-workflows
description: "Use when working with Obsidian vaults through either direct filesystem edits or the Obsidian CLI on a running remote host."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [obsidian, notes, vault, cli, filesystem]
    related_skills: [obsidian-markdown]
---

# Obsidian Workflows

## Overview

This is the umbrella skill for Obsidian note operations. Prefer one class-level skill covering both local filesystem-first workflows and remote CLI-driven workflows rather than splitting them into separate narrow skills by transport.

The two main lanes are:
1. direct filesystem access to a vault, and
2. remote `obsidian` CLI access on a machine where Obsidian is running.

Choose the lane that matches the environment, but keep the mental model unified: identify the vault, inspect note state, make targeted edits, and verify the final note path/content.

## When to Use

- Reading, searching, creating, or editing Obsidian notes
- Deciding whether to use filesystem tools or the Obsidian CLI
- Working with a local vault path or a remote Mac-hosted Obsidian instance
- Managing note content, tasks, properties, backlinks, or daily notes

## Lane A — Filesystem-first vault work

Use this when the vault is directly accessible from the current machine.

Core rules:
- Resolve the vault path first.
- Prefer file tools over shell commands for note contents.
- Use absolute paths, not unresolved environment variables.

Typical operations:
- `read_file` for note contents
- `search_files(target="files")` to list notes
- `search_files(target="content")` to search markdown
- `write_file` to create notes
- `patch` for focused edits

If the vault path is unknown, resolve `OBSIDIAN_VAULT_PATH` or use the known fallback before using file tools.

## Lane B — Obsidian CLI on remote host

Use this when the user's workflow depends on the Obsidian app and CLI running on a remote machine.

Core rule:
- run the CLI on the host where Obsidian is running, typically through SSH.

Pattern:
```bash
ssh mac-mini "obsidian <command>"
```

This lane is useful for:
- note creation/opening inside the app context
- task/property/backlink commands
- daily note workflows
- vault operations exposed by the Obsidian CLI

## Choosing the lane

Use filesystem-first when:
- the vault is locally mounted or directly accessible
- the task is content-centric and file tools are enough
- you want precise line-based edits and search

Use CLI lane when:
- the vault lives on a remote machine with Obsidian running
- the user specifically wants `obsidian` CLI features
- the operation depends on Obsidian app semantics rather than plain files

## Shared pitfalls absorbed from narrower skills

1. Do not assume the vault path; resolve it first.
2. Do not pass `$OBSIDIAN_VAULT_PATH` literally into file tools.
3. Do not run the Obsidian CLI locally if it only works on the remote machine.
4. When a git-backed vault may be behind the remote state, sync before inventing parallel local folder structure.
5. Prefer one note-operations umbrella with transport-specific subsections over separate micro-skills by access method.

## Verification Checklist

- [ ] Correct vault identified
- [ ] Correct lane chosen (filesystem or remote CLI)
- [ ] Final path/note target verified
- [ ] Edits/searches executed with the appropriate tool family
- [ ] No duplicate or misplaced note created through path confusion
