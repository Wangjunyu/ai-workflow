#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_NAME="com.leon.telegram-obsidian-bot"
PLIST_SRC="$SCRIPT_DIR/$PLIST_NAME.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"
LOGS_DIR="$SCRIPT_DIR/logs"

mkdir -p "$LOGS_DIR"

case "${1:-}" in
    install)
        echo "📦 安装 launchd 服务..."
        cp "$PLIST_SRC" "$PLIST_DEST"
        launchctl unload "$PLIST_DEST" 2>/dev/null || true
        launchctl load "$PLIST_DEST"
        echo "✅ 服务已安装并加载"
        ;;
    uninstall)
        echo "🗑 卸载 launchd 服务..."
        launchctl unload "$PLIST_DEST" 2>/dev/null || true
        rm -f "$PLIST_DEST"
        echo "✅ 服务已卸载"
        ;;
    restart)
        echo "🔄 重启服务..."
        launchctl kickstart -k "gui/$(id -u)/$PLIST_NAME"
        echo "✅ 服务已重启"
        ;;
    status)
        launchctl print "gui/$(id -u)/$PLIST_NAME" 2>/dev/null || echo "未安装或未运行"
        ;;
    logs)
        echo "📋 stdout:"
        tail -30 "$LOGS_DIR/stdout.log" 2>/dev/null || echo "(无日志)"
        echo
        echo "📋 stderr:"
        tail -30 "$LOGS_DIR/stderr.log" 2>/dev/null || echo "(无日志)"
        ;;
    *)
        echo "用法: $0 {install|uninstall|restart|status|logs}"
        exit 1
        ;;
esac
