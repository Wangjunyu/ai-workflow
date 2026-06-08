# Hermes Fleet — Profile 配置分发系统

> 云端定义，按机部署。Git 管配置，Secrets 管密钥，本地管运行。

## 设计原则

1. **云端母版，本地实例**
   - Git 仓库保存所有 profile 的定义和模板
   - 每台机器 render 成本地可运行的 ~/.hermes/profiles/
   - 运行态（sessions/logs/auth）不同步

2. **分层组合**
   - `layers/` — 按机器角色叠加的配置层
   - `profiles/` — 每个 profile 的完整定义
   - `hosts/` — 每台机器要哪些 profile
   - `shared/` — 跨 profile 共享资源

3. **密钥外置**
   - Git 不存真实 .env
   - 通过 Bitwarden / 手动注入
   - profile 只定义需要哪些密钥

4. **程序与配置分离**
   - 本仓库 = 配置 + 模板 + 部署说明
   - 不混入 Obsidian 内容、session 历史、日志

## 目录结构

```
hermes-fleet/
├── README.md               ← 本文
├── .gitignore
├── layers/                  ← 配置层（按机器角色叠加）
│   ├── base.yaml            ← 所有机器通用
│   ├── cli.yaml             ← 交互 CLI 型机器
│   └── bot.yaml             ← 跑 Gateway 的机器
├── profiles/                ← Profile 完整定义
│   ├── default/
│   │   ├── profile.yaml     ← 元信息
│   │   ├── config.yaml      ← 主配置
│   │   └── personality.md   ← 人格
│   └── bulma/
│       ├── profile.yaml
│       ├── config.yaml
│       └── personality.md
├── hosts/                   ← 机器定义
│   ├── local.yaml           ← 本地 MacBook
│   ├── mac-mini.yaml        ← Mac mini
│   └── firefly.yaml         ← Linux 服务器
├── shared/                  ← 跨 profile 共享资源
│   ├── scripts/
│   ├── skills/
│   └── personality/
└── deploy/                  ← 部署工具
    ├── render.py            ← 合并 layers + profiles
    └── sync.sh              ← 渲染 + 远程同步
```

## 配置合并规则

每个 profile 的最终 config 按以下优先级合并（后者覆盖前者）：

```
base.yaml          ← 最低优先
  ↓
role layer         ← cli.yaml / bot.yaml
  ↓
profile config     ← profiles/<name>/config.yaml
  ↓
host override      ← hosts/<host>.yaml 中的覆盖字段
  ↓
.env secrets       ← 本地注入的密钥
```

## 快速开始

### 1. 拉取仓库

```bash
git clone https://github.com/Wangjunyu/ai-workflow.git
cd ai-workflow/hermes-fleet
```

### 2. 查看当前舰队

```bash
# 有哪些机器
ls hosts/

# 有哪些 profile
ls profiles/

# 有哪些配置层
ls layers/
```

### 3. 部署到本机

```bash
bash deploy/sync.sh local
```

### 4. 部署到远程

```bash
bash deploy/sync.sh mac-mini
bash deploy/sync.sh firefly
```

### 5. 部署后检查

```bash
# 本地
hermes profile list
hermes -p bulma config

# 远程
ssh mac-mini 'bash ~/.hermes/scripts/hermes-checks.sh'
```

## 日常工作流

### 修改配置

```
1. 编辑 layers/ 或 profiles/ 中的文件
2. 重新部署到目标机：bash deploy/sync.sh <host>
3. 新 session 生效（gateway 需 restart）
```

### 新增 profile

```
1. 创建 profiles/<name>/ 目录，写入 profile.yaml + config.yaml + personality.md
2. 在目标 hosts/<host>.yaml 的 profiles 列表加入 <name>
3. deploy + sync
```

### 新增机器

```
1. 创建 hosts/<host>.yaml
2. 指定 profiles 列表和 layers 列表
3. deploy + sync
```

## 跨 profile 调用

跨 profile 不做内建树状继承。使用显式调用：

```bash
# 手工切换
hermes -p bulma chat -q "..."

# 子进程调用（在 default 里调 bulma）
hermes -p bulma chat -q "..." > /tmp/result.txt

# 运维控制
hermes -p bulma gateway restart
hermes -p bulma cron list
```

详见 Obsidian 笔记：[[Hermes-Fleet-Profile配置体系]]

## 机器与 Profile 矩阵

| 机器 | Profiles | Layers | Gateway |
|------|----------|--------|---------|
| local | default | base + cli | - |
| mac-mini | default, bulma | base + cli + bot | bulma running |
| firefly | default | base + cli | - |

## 依赖

- Python 3 + PyYAML: `pip install pyyaml`
- rsync
- ssh 免密登录（远程部署用）
- hermes CLI（目标机）

## 安全注意事项

- `.env` 和真实密钥不提交 Git
- 部署不同步 sessions / logs / auth.json
- 远程同步排除运行时敏感文件
- Bot profile 不同时在 2 台机器运行（webhook 冲突）
