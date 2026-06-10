---
name: local-knowledge-capture
description: |
  Capture completed work into the user’s local knowledge base correctly:
  verify the real vault/path, prefer updating the right existing document
  over creating detached notes, and clean up mistaken writes.
summary: |
  Capture completed work into the user’s local knowledge base correctly:
  verify the real vault/path, prefer updating the right existing document
  over creating detached notes, and clean up mistaken writes.
when_to_use:
  - User asks to save a summary, workflow note, or project record into Obsidian or another local markdown knowledge base.
  - You generated a note and need to place it in the correct local vault/folder.
  - The user corrects the destination path or says the content belongs inside an existing document instead of a new index/note.
not_for:
  - Generic file writing outside a knowledge base.
  - Cloud docs or SaaS note systems handled by dedicated skills.
version: 1.0.0
---

# Local knowledge capture

## Core rule

When saving knowledge artifacts for this user, the deliverable is not just “a markdown file exists.” The content must land in the correct knowledge base, in the correct location, with the correct level of integration into the existing structure.

## Workflow

1. Resolve the actual vault/root path from the live filesystem before writing or searching.
   - Do not rely on defaults, guesses, iCloud conventions, Desktop assumptions, or remembered paths.
   - If multiple plausible vaults exist, verify which one is active from the user’s wording and live paths.
   - When search tools return empty results for an expected vault, verify the path with a direct filesystem check before concluding the note is missing.

2. Prefer the user’s stated structure over creating new structure.
   - If the user says the content belongs in an existing document, update that document.
   - Do not create a separate index page, summary page, or new folder unless the user asked for it.

3. When the task is retrieval rather than writing, search the most likely active vault thoroughly before broadening scope.
   - Start from the verified vault root.
   - Inspect high-signal folders already suggested by the repo structure, such as workflow, infrastructure, AI-info, or server-related areas.
   - Use conversation/session recall alongside vault search when the user says they "already explored this before" or implies prior notes exist.

4. When writing a new note, place it under the requested folder with a durable title.
   - Use Obsidian-friendly markdown.
   - Keep summaries concise enough to be maintainable but complete enough to be reusable.

5. If you wrote to the wrong place, fix it immediately.
   - Move or recreate the content in the correct location.
   - Remove or neutralize the mistaken write so the vault does not accumulate duplicate/confusing artifacts.

6. Report exact paths in the final response.
   - State where the correct content now lives.
   - If a mistaken copy existed, state how it was cleaned up.
   - If the key artifact is an existing note, name the exact file(s) that should drive the next step.

## Pitfalls

### Do not assume the default Obsidian vault

A common failure mode is writing to an iCloud or fallback Obsidian path because it looks plausible. Always verify the actual vault path first.

### Do not create unnecessary index pages

If the user says “just add this into the infrastructure document,” then update that document directly. Do not create a parallel index or a detached note just because it seems tidy.

### Wrong-location cleanup matters

A wrong file left behind creates future confusion. If you misplace a note, clean it up in the same session.

## User-specific preference captured from session

For this user’s knowledge capture workflow:
- Obsidian location assumptions must be verified against the live filesystem.
- Content that belongs in an existing AI infrastructure document should be merged there instead of creating standalone index pages.
- If a note was written to the wrong vault/path, clean it up immediately.
