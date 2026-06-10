---
name: git-firefly-bridge
description: 本地/Mac-mini 无法直连 GitHub 时，通过 firefly SSH 中转推送 git 提交。
---

## 触发条件

本地或 mac-mini 执行 `git push` / `git pull` 超时，但 `ssh firefly` 通且 firefly 能连 GitHub。

## 前提

- `ssh firefly` 可用
- firefly 上已安装 git（`which git`）
- 本地已创建了待推送的提交

## 流程

### 1. 本地打 bundle（只包含 origin/main 之后的新提交）

```bash
cd /path/to/repo
git bundle create /tmp/repo-commits.bundle origin/main..HEAD
```

### 2. 传 bundle 到 firefly

```bash
cat /tmp/repo-commits.bundle | ssh firefly 'cat > /tmp/repo-commits.bundle'
```

### 3. 在 firefly 上 clone + 灌入 bundle + rebase + 推送

```bash
ssh firefly '
cd /tmp
rm -rf repo-push
git clone https://github.com/OWNER/REPO.git repo-push
cd repo-push
# 验证 bundle
git bundle verify /tmp/repo-commits.bundle
# 灌入
git fetch /tmp/repo-commits.bundle HEAD:incoming
# rebase 到 origin/main（如果有冲突会触发手动解决）
git checkout incoming
git rebase origin/main
# 推送
GIT_EDITOR=true git rebase --continue   # 如有冲突解决后继续
git push origin incoming:main
'
```

### 4. 本地同步

```bash
# 从 firefly 的 clone 拉取最新的 origin/main
git fetch ssh://firefly/tmp/repo-push +refs/remotes/origin/main:refs/remotes/origin/main
git reset --hard origin/main
```

### 5. 清理

```bash
git remote remove firefly 2>/dev/null   # 如果之前 add 过
rm -f /tmp/repo-commits.bundle
ssh firefly 'rm -rf /tmp/repo-push /tmp/repo-commits.bundle'
```

## 注意事项

- 如果 rebase 出现冲突（两边都改了同一文件），需要手动编辑冲突文件，`git add` 后 `GIT_EDITOR=true git rebase --continue`
- firefly 上 clone 用的是 HTTPS（不需要 SSH key），只需网络通即可
- mac-mini 同样可以用此流程：`ssh firefly` 从 mac-mini 也能通
