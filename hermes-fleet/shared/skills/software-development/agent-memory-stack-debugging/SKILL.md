---
name: agent-memory-stack-debugging
description: Diagnose and repair AI agent memory-stack failures across config, runtime environment, dependencies, network, and verification layers.
version: 1.0.0
author: Hermes Agent
---

# Agent Memory Stack Debugging

Use this skill when an AI agent's memory system appears enabled but does not actually work at runtime. This includes cases involving Hermes memory providers such as mem0, or similar systems where status commands, plugins, Python environments, API keys, and proxy/network paths can disagree.

This is a class-level debugging skill for memory-stack bring-up and repair. It is not specific to one provider, though mem0/Hermes is a primary example.

## When to use

Trigger this skill when any of the following are true:
- The user says memory is configured but reads/writes fail.
- A CLI status command says memory is available, but the active agent/tool call still errors.
- A provider package imports in one shell or venv but not from the agent runtime.
- Memory initialization succeeds only partway and then fails on API/network/TLS checks.
- The user wants the agent to fix the memory stack directly rather than repeatedly asking for manual steps.

## Core principle

Treat memory as a stack with multiple independent failure layers:
1. Configuration layer
2. Runtime/interpreter layer
3. Dependency layer
4. Network/proxy/API reachability layer
5. End-to-end verification layer

Do not stop at the first layer that looks healthy.

## Preferred workflow

### 1. Establish the exact failure surface

Determine which operation fails:
- Status/health command
- Import
- Client initialization
- Real read/write operation

Capture the exact failing boundary. Do not generalize too early.

### 2. Check for environment split before chasing packages

This is the highest-value early check.

Compare:
- The CLI/tooling interpreter path
- The active agent runtime interpreter path
- Any project-specific venv involved

Pitfall:
A status command may run in one Python environment while agent tool invocations run in another. This can create a false impression that the provider is installed and working when only the CLI environment is healthy.

Always explicitly identify which interpreter owns the working code path.

### 3. Validate config independently of runtime

Check that:
- The intended provider is selected
- Required API key/config exists
- The plugin/provider is enabled

But do not confuse config correctness with runtime readiness.

Pitfall:
`status available` is not proof of functionality. It may only mean the configured provider name and plugin wiring look valid.

### 4. Repair dependencies in the runtime that matters

Install or repair packages in the interpreter actually used by the production memory path.

If package installation is unreliable:
- Prefer a deterministic fallback such as downloading wheels and installing locally.
- Validate incrementally by importing the provider package and then the client object that matters.
- If deeper imports fail, enumerate and repair transitive dependencies methodically.

Pitfall:
Do not declare success after the top-level package imports. Many memory providers only fail during client initialization when optional/transitive dependencies or network calls activate.

### 5. Escalate to network testing as soon as imports pass

Once the provider imports and client construction begins, move immediately to testing the actual API endpoint path.

Verify in order:
- Can the endpoint be reached at all?
- Is TLS handshake successful?
- Does the response change from transport failure to an auth/business-level response?

Interpretation:
- TLS/connect/EOF errors mean transport is still broken.
- HTTP 401/403 after transport succeeds usually means the network path is fixed and the remaining issue is credentials or authorization.

This distinction is critical.

### 6. For proxy-managed systems, treat proxy control as part of the repair

If the environment uses Clash Verge, mihomo, or similar local proxy management, do not treat proxy settings as an afterthought.

When authorized by the user, directly inspect and modify the relevant proxy/rule selectors instead of only suggesting manual GUI changes.

Preferred sequence:
- Confirm the local controller/socket exists.
- Inspect active selectors and current route choices.
- Switch global or relevant rule groups away from DIRECT when the target service needs proxying.
- Re-test the exact API endpoint immediately after each switch.

Pitfall:
A proxy can be "running" while the relevant selector is still routed to DIRECT or to an unstable node for the target service.

### 7. Verify with a real provider lifecycle, not just status

After repair, perform layered proof:
- Provider package import works
- Client object import works
- Client initialization reaches the remote service successfully
- Real memory read/write path succeeds if credentials are available

If credentials are not available for a safe write test, an auth-layer response such as `invalid API key` after successful TLS can still prove that the transport layer is repaired.

### 8. Distinguish runtime repaired vs current session repaired

If the CLI/runtime environment is fixed but the current agent session still uses an older interpreter/process state, say so explicitly.

Pitfall:
The user may believe the whole system is still broken when only the already-running agent process needs restart/reload to pick up repaired dependencies.

State the difference clearly:
- "Hermes CLI/runtime is repaired"
- "Current agent process may need restart to inherit the repaired environment"

## User workflow preference to embed

When the user expresses frustration about being repeatedly asked to do manual repair steps, prefer direct action whenever permissions and tool access allow it.

For this class of task:
- Act first on diagnosable and reversible changes.
- Ask only for scope-changing or side-effectful authorization, such as modifying proxy routing.
- Once authorized, continue through diagnosis, repair, and verification without bouncing work back to the user.

## Verification checklist

Before closing the task, confirm all applicable items:
- Correct provider configured
- Correct runtime interpreter identified
- Dependencies repaired in the right environment
- API endpoint reachable over the intended network path
- TLS succeeds
- Auth/business-level response understood
- Real memory operations verified, or precise reason why only runtime/session split remains

## Support files

See `references/mem0-hermes-clash-verge.md` for a concrete example covering Hermes + mem0 + Clash Verge route switching and the signal that a 401 after TLS means transport is fixed.
