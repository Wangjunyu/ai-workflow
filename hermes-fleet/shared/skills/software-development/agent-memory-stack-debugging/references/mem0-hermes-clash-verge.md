# Hermes + mem0 + Clash Verge reference

This reference captures a reusable troubleshooting pattern for memory-stack failures where the apparent root cause changes as each layer is repaired.

## Situation shape

Observed pattern:
- Hermes memory provider configured as mem0
- `hermes memory status` reported provider/plugin available
- Active agent memory tool still failed
- The CLI/runtime interpreter and current agent interpreter were different
- After dependency repair, provider import worked but client initialization failed on TLS
- After proxy route changes in Clash Verge, the TLS error disappeared and the endpoint returned HTTP 401

## Durable lessons

### 1. Status vs runtime are different checks

A healthy `hermes memory status` does not prove the active agent process can import and use the same provider. It may only prove the Hermes CLI environment is healthy.

### 2. Interpreter split is a first-class root cause

In this case, Hermes CLI used its own venv while the active tool session used a different Python. That difference explained why mem0 looked installed from one path but unavailable from another.

### 3. Transport repair can be proven by an auth-layer failure

For mem0, a useful progression is:
- transport/TLS error => network path still broken
- HTTP 401 / invalid API key => network path is fixed; remaining issue is authentication

This is an important diagnostic transition. Do not treat 401 as failure to connect.

### 4. Clash Verge route switching can be the decisive fix

If the host uses Clash Verge/mihomo and the relevant traffic is still routed to DIRECT or to a weak node, memory-provider API calls may fail during TLS even though local proxy infrastructure is running.

Practical sequence:
- inspect local controller/socket
- inspect selectors such as GLOBAL and manual-choice groups
- switch relevant selectors away from DIRECT
- choose a node suitable for the target AI/API traffic
- re-test the exact provider endpoint immediately

### 5. End state may be "runtime repaired, session restart still needed"

If packages were repaired in the Hermes runtime venv and network transport was fixed, the remaining problem can be that the already-running agent session has not inherited the repaired environment yet.

That is not the same as the stack still being broken.

## Suggested phrasing for future handoffs

Use language like:
- "The Hermes runtime is repaired and mem0 network access is working."
- "The remaining issue is whether the current agent process must restart/reload to pick up the repaired environment."
- "A 401/invalid-key response now indicates transport success, not network failure."
