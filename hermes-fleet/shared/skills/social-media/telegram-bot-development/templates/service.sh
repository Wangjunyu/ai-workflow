#!/bin/bash
# Telegram Bot launchd 服务管理脚本
# 用法:
#   ./service.sh install   - 安装并启动
#   ./service.sh uninstall - 停止并移除
#   ./service.sh restart   - 重启
#   ./service.sh status    - 查看状态
#   ./service.sh logs      - 查看日志

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_NAME="{{PLIST_NAME}}"
PLIST_SRC="$SCRIPT_DIR/$PLIST_NAME.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"
LOGS_DIR="$SCRIPT_DIR/logs"

mkdir -p "$LOGS_DIR"

case "${1:-}" in
    install)
        echo "📦 安装 launchd 服务..."
        cp "$PLIST_SRC" "$PLIST_DEST"
        launchctl load "$PLIST_DEST"
        launchctl start "$PLIST_NAME"
        echo "✅ 服务已安装并启动"
        echo "   查看状态: $0 status"
        echo "   查看日志: $0 logs"
        ;;

    uninstall)
        echo "🗑  卸载 launchd 服务..."
        launchctl stop "$PLIST_NAME" 2>/dev/null || true
        launchctl unload "$PLIST_DEST" 2>/dev/null || true
        rm -f "$PLIST_DEST"
        echo "✅ 服务已卸载"
        ;;

    restart)
        echo "🔄 重启服务..."
        launchctl stop "$PLIST_NAME" 2>/dev/null || true
        sleep 1
        launchctl start "$PLIST_NAME" 2>/dev/null || {
            launchctl load "$PLIST_DEST"
        }
        echo "✅ 服务已重启"
        ;;

    status)
        echo "📊 服务状态:"
        launchctl list "$PLIST_NAME" 2>/dev/null || echo "  未运行"
        ;;

    logs)
        echo "📋 stdout (最近30行):"
        tail -30 "$LOGS_DIR/stdout.log" 2>/dev/null || echo "  (无日志)"
        echo ""
        echo "📋 stderr (最近30行):"
        tail -30 "$LOGS_DIR/stderr.log" 2>/dev/null || echo "  (无日志)"
        ;;

    *)
        echo "用法: $0 {install|uninstall|restart|status|logs}"
        exit 1
        ;;
esac
