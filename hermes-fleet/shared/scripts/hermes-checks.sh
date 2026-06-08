#!/usr/bin/env bash
# Hermes 健康检查脚本 — 适用于所有机器
# 用法: bash hermes-checks.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

pass() { echo -e "${GREEN}[OK]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; }

echo "=== Hermes Fleet Health Check ==="
echo ""

# 1. Hermes CLI
if command -v hermes &>/dev/null; then
  pass "hermes CLI: $(hermes --version 2>&1 | head -1)"
else
  fail "hermes CLI not found"
fi

# 2. Config
if hermes config check &>/dev/null; then
  pass "hermes config: valid"
else
  fail "hermes config has issues"
fi

# 3. Profiles
echo ""
echo "Profiles:"
hermes profile list 2>/dev/null || fail "cannot list profiles"

# 4. Gateway status
echo ""
echo "Gateway:"
hermes gateway status 2>/dev/null || echo "  (gateway not running)"

# 5. Git (for fleet repo)
echo ""
echo "Fleet repo:"
if git -C "$HOME/ai-workflow" status --short --branch 2>/dev/null; then
  pass "fleet repo: $HOME/ai-workflow"
else
  fail "fleet repo not found at $HOME/ai-workflow"
fi

echo ""
echo "=== Done ==="
