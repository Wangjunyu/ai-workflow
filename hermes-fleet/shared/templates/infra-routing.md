# 基础设施路由（共享模板）

> 插入到每个非 infra-ops profile 的 AGENTS.md 末尾。由 fleet sync 统一管理。

## 基础设施路由

**你不会自己摸索飞书 API、SSH 连接、Obsidian 路径、得到大脑 API。所有 infra 操作必须走 SOP。**

当浚宇让你做以下操作时，先加载 `infra-ops-sop`，然后按其路由表加载对应子 skill：

| 操作类型 | 加载 Skill |
|---------|-----------|
| 飞书文档/知识库/妙记/云盘 | `infra-ops-sop` |
| Obsidian vault 读写/同步/Git | `infra-ops-sop` |
| 得到大脑（Get笔记） | `infra-ops-sop` |
| 跨服务器 SSH/文件 | `infra-ops-sop`、`git-firefly-bridge` |
| 创建新 Hermes profile | `infra-ops-sop`、`infra-profile-create` |
| 网络/Tailscale | `infra-ops-sop`、`tailscale` |

**原则：不猜 API、不试错端点、不走捷径。走 SOP。**
