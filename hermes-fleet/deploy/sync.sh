#!/usr/bin/env bash
# Hermes Fleet — Sync
#
# 渲染并同步 profile 配置到目标机器。
#
# 用法:
#   bash deploy/sync.sh <host-name>
#
# 依赖:
#   - Python 3 + PyYAML (pip install pyyaml)
#   - ssh 免密登录目标机
#   - 目标机上已安装 hermes
#
# 不同步的内容:
#   - .env（密钥由 bitwarden / 手动管理）
#   - sessions/
#   - logs/
#   - auth.json / auth 缓存

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

FLEET_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAGING="/tmp/hermes-staging-${1:-unknown}"

sync_host() {
    local host="$1"
    local staging="$2"

    echo -e "${GREEN}=== Syncing profiles to: $host ===${NC}"

    # Step 1: Render
    echo "→ Rendering..."
    python3 "$FLEET_ROOT/deploy/render.py" "$host" --staging-dir "$staging"

    # Step 2: Check staging
    if [ ! -d "$staging" ]; then
        echo -e "${RED}ERROR: staging dir not found: $staging${NC}"
        exit 1
    fi

    # Step 3: Local or remote?
    # localhost = 直接复制到 ~/.hermes/profiles/
    if [ "$host" = "local" ] || [ "$host" = "localhost" ]; then
        echo "→ Deploying locally..."
        for profile_dir in "$staging/profiles/"*/; do
            profile_name="$(basename "$profile_dir")"
            target="$HOME/.hermes/profiles/$profile_name"
            echo "  → $profile_dir → $target"
            mkdir -p "$target"
            rsync -av --delete \
                --exclude='.env' \
                --exclude='sessions/' \
                --exclude='logs/' \
                --exclude='auth.json' \
                "$profile_dir" "$target/"
        done

        # scripts
        if [ -d "$staging/shared/scripts" ]; then
            mkdir -p "$HOME/.hermes/scripts"
            rsync -av "$staging/shared/scripts/" "$HOME/.hermes/scripts/"
        fi
    else
        # Remote deploy via rsync over SSH (aliases from ~/.ssh/config)
        echo "→ Deploying to remote: $host..."
        ssh "$host" "mkdir -p ~/.hermes/profiles"
        for profile_dir in "$staging/profiles/"*/; do
            profile_name="$(basename "$profile_dir")"
            target="$host:~/.hermes/profiles/$profile_name"
            echo "  → $profile_dir → $target"
            rsync -avz --delete \
                --exclude='.env' \
                --exclude='sessions/' \
                --exclude='logs/' \
                --exclude='auth.json' \
                "$profile_dir" "$target"
        done

        if [ -d "$staging/shared/scripts" ]; then
            rsync -avz "$staging/shared/scripts/" "$host:~/.hermes/scripts/"
        fi
    fi

    echo ""
    echo -e "${GREEN}=== Sync complete: $host ===${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Review config on target: hermes -p <name> config"
    echo "  2. Verify .env is set up (manual step)"
    echo "  3. Check: hermes -p <name> chat -q 'test'"
    if [ "$host" != "local" ] && [ "$host" != "localhost" ]; then
        echo ""
        echo "  Or run health check remotely:"
        echo "  ssh $host 'bash ~/.hermes/scripts/hermes-checks.sh'"
    fi
}

# --- main ---
if [ $# -lt 1 ]; then
    echo "Usage: bash deploy/sync.sh <host-name>"
    echo ""
    echo "Available hosts:"
    for f in "$FLEET_ROOT/hosts/"*.yaml; do
        echo "  - $(basename "$f" .yaml)"
    done
    exit 1
fi

sync_host "$1" "$STAGING"
