# Python Debugger Recipes

This reference preserves Python-specific debugger detail under the debugging umbrella.

## Choose among
- `breakpoint()` / pdb
- `python -m pdb`
- `debugpy` for remote or attach workflows

## Use when
- traceback is insufficient
- state must be inspected live
- the process is long-running or headless

## Core rule
Start with the cheapest thing that works, usually `breakpoint()`.

## Common pitfalls
- xdist and pdb do not mix well
- non-TTY contexts can hang on breakpoints
- attach workflows need port/process verification
- remove debug hooks before finishing
