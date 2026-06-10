# CI Troubleshooting

Use this reference when a PR check fails and the task becomes diagnose → reproduce → fix → re-run.

## Loop
1. Inspect failed checks.
2. Open the failing workflow logs.
3. Reproduce locally when possible.
4. Make the smallest fix.
5. Push and watch the next run to completion.

## Handy commands
```bash
gh pr checks
gh pr checks --watch
gh run list --branch $(git branch --show-current) --limit 5
gh run view <RUN_ID> --log-failed
```

## Rule
Do not say CI is fixed until the replacement run is green.
