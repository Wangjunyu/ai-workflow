# Python Network / Package Repair

This reference preserves the dependency-and-network bring-up workflow under the debugging umbrella.

## Use when
- pip/index/TLS issues block package installation
- Python HTTP clients fail while curl works
- tool runtime and current shell Python differ

## Core loop
1. identify the exact interpreter,
2. verify imports there,
3. repair dependencies incrementally,
4. separate import success from live network success,
5. test proxy/TLS assumptions explicitly.

## Rule
Do not call the feature fixed just because imports work; verify live connectivity separately when that is part of the user's task.
