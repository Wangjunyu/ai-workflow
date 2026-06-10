---
name: debugging-workflows
description: "Use when diagnosing software bugs through root-cause analysis, language-specific debuggers, and verification-driven fix loops."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [debugging, troubleshooting, root-cause, pdb, debugpy, node-inspect, diagnostics]
    related_skills: [test-driven-development]
---

# Debugging Workflows

## Overview

This umbrella skill covers the broad debugging class: root-cause investigation, debugger selection, environment isolation, and verification of fixes. Separate language-specific debugger recipes belong as subsections or references under this umbrella, not as standalone siblings unless they define a genuinely separate maintenance class.

The default order is:
1. understand the failure,
2. reproduce it,
3. isolate the cause,
4. use the right debugger or instrumentation,
5. verify the fix.

## When to Use

- Investigating failing tests or runtime bugs
- Choosing between logging, pdb/debugpy, or Node inspector
- Diagnosing environment mismatches and package/runtime issues
- Running a structured root-cause analysis before changing code

## Phase 1 — Root-cause investigation

Before fixing anything:
- read the full error
- reproduce consistently
- inspect recent changes
- trace data flow
- isolate the failing component

Do not propose fixes before understanding why the failure happens.

## Phase 2 — Debugger lane selection

### Python lane
Use when the failing component is Python.
Common options:
- `breakpoint()` / pdb for cheapest local inspection
- `python -m pdb` for script-first debugging
- `debugpy` for attach/remote/headless cases

### Node lane
Use when the failing component is Node.js / tsx / Ink / browser-adjacent CLI JS.
Common options:
- `node inspect` for fast local REPL debugging
- inspector/CDP tooling for scripted or remote inspection

### Network/package/environment lane
Use when the failure is not application logic first, but runtime bring-up:
- wrong interpreter or venv
- package import drift
- TLS/proxy mismatch
- pip/httpx failure with curl still working

Treat this as a debugging subsection, not a separate top-level class.

## Verification-driven fix loop

After identifying root cause:
- create or identify a failing test/repro
- make the smallest fix
- rerun the narrow repro
- rerun broader verification
- stop if repeated fixes suggest an architectural issue

## Support materials

Use references for backend-specific and language-specific detail rather than new sibling skills.

## Common Pitfalls

1. Jumping to fixes before root-cause analysis.
2. Treating Python, Node, and environment debugging as unrelated classes when they are one debugging family.
3. Confusing dependency repair with real network/API success.
4. Declaring success before re-running the actual repro or tests.
5. Spawning a new skill for one debugger/backend instead of adding a labeled subsection or reference.
6. On macOS system-inspection tasks, misusing the terminal tool's `workdir` by accidentally stuffing shell syntax or command fragments into it. `workdir` must be a plain filesystem path only.
7. When checking load or memory on macOS, over-interpreting `unused` memory from `top` as danger by itself. Prefer explaining memory pressure, compression, and swap together before concluding the machine is unhealthy.

## macOS system-load inspection note

For "why is memory high?" or "how loaded is the machine?" style questions on macOS:
- gather `uptime`, `top`, `vm_stat`, and `memory_pressure`
- inspect both single heavy processes and grouped app families (for example WeChat/Electron/Chromium multi-process trees)
- call out that compressed memory can make `PhysMem used` look alarming even when swap is still zero
- when possible, aggregate related helper/renderer/GPU processes so the user sees the real app-level culprit rather than a confusing list of child processes

## Verification Checklist

- [ ] Failure reproduced or evidence gathered
- [ ] Root cause hypothesis formed before fix
- [ ] Correct debugger lane chosen
- [ ] Environment/runtime mismatch ruled in or out explicitly
- [ ] Fix verified with the real repro or test suite
