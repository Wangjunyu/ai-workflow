# Node Inspector Recipes

This reference preserves Node-specific debugger detail under the debugging umbrella.

## Choose among
- `node inspect`
- `--inspect` / `--inspect-brk`
- CDP scripting for automation-heavy debugging

## Use when
- debugging Node.js scripts, tsx apps, or Ink/TUI code
- inspecting running processes through the V8 inspector

## Core rule
Prefer `node inspect` first; escalate to CDP automation only when repeated scripted inspection is worth it.

## Common pitfalls
- wrong source/line due to transpiled JS
- attaching too late without `--inspect-brk`
- child processes not inheriting the intended debugging mode
- leaving a paused target running after detaching
