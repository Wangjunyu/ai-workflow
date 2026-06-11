# 飞书妙记索引

> 自动生成于 cron: `minutes-index-daily-sync`
> 数据来源: `lark-cli minutes +search --participant-ids "me"`

## 统计概览

> 最后更新: 2026-06-12 03:52 UTC+8 — ⚠️ **同步失败**（用户授权缺失）

| 维度 | 数量 |
|------|:----:|
| 近7天妙记总数 | ❌ 无法获取 |
| 近24h新增 | ❌ 无法获取 |

## 故障说明

**根本原因：** `lark-cli` 用户身份缺失。`minutes +search` 仅支持 `--as user`，而当前环境（firefly cron）中无已登录用户。

**日志证据：**
- `lark-cli auth status` → `user: missing (no user logged in)`
- `lark-cli minutes +search` → `need_user_authorization (user: )`
- Bot 身份可用但 `minutes +search` 不支持 bot（报错：`--as bot is not supported, this command only supports: user`）
- Bot 直调 REST API `/open-apis/minutes/v1/minutes` → 404；`/minutes/search` → field validation 失败

**需要的操作（用户侧）：**
1. 在 firefly 上执行：`lark-cli auth login --domain minutes`
2. 用飞书扫描 QR 码完成授权
3. 授权后用户 token 会持续有效（含 refresh token 自动续期）

**备选方案（长期）：** 将 cron job 改为在 mac-mini（有用户会话/Keychain Access）执行，或迁移到支持 user access token 的服务端 OAuth 流程。

## 近7天妙记列表

| 日期 | 标题 | minute_token | 时长 |
|------|------|-------------|:--:|
| (待用户修复授权后重新同步) | | | |
