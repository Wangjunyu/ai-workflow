#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE_NAME="telegram-obsidian.service"
SERVICE_FILE="$SCRIPT_DIR/$SERVICE_NAME"
USER_SYSTEMD_DIR="${HOME}/.config/systemd/user"
USER_TARGET_FILE="${USER_SYSTEMD_DIR}/${SERVICE_NAME}"

usage() {
    cat <<'EOF'
用法:
  ./install-systemd-user.sh install   安装并启动用户级 systemd 服务
  ./install-systemd-user.sh status    查看用户级服务状态
  ./install-systemd-user.sh logs      查看用户级服务日志
  ./install-systemd-user.sh remove    卸载用户级服务

前提:
  1. 当前机器支持 systemctl --user
  2. 当前登录会话可访问 user bus

如果出现 “Failed to connect to bus: No medium found”，说明当前环境没有可用的 user systemd bus。
此时请改用 README 里的方案 B：系统级 systemd 服务。
EOF
}

require_user_bus() {
    if ! systemctl --user show-environment >/dev/null 2>&1; then
        echo "❌ 当前环境没有可用的 user systemd bus。"
        echo "请改用系统级 systemd 方案，见 README 的方案 B。"
        exit 1
    fi
}

install_service() {
    require_user_bus
    mkdir -p "$USER_SYSTEMD_DIR"
    cp "$SERVICE_FILE" "$USER_TARGET_FILE"
    systemctl --user daemon-reload
    systemctl --user enable "$SERVICE_NAME"
    systemctl --user restart "$SERVICE_NAME"
    systemctl --user status "$SERVICE_NAME" --no-pager
}

show_status() {
    require_user_bus
    systemctl --user status "$SERVICE_NAME" --no-pager
}

show_logs() {
    require_user_bus
    journalctl --user -u "$SERVICE_NAME" -n 50 --no-pager
}

remove_service() {
    require_user_bus
    systemctl --user disable --now "$SERVICE_NAME" || true
    rm -f "$USER_TARGET_FILE"
    systemctl --user daemon-reload
    echo "✅ 已卸载用户级 systemd 服务"
}

case "${1:-}" in
    install)
        install_service
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    remove|uninstall)
        remove_service
        ;;
    *)
        usage
        exit 1
        ;;
esac
