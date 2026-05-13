# MEMORY.md - 长期记忆

## OpenClaw 更新规范

### 正确方式（源码构建）
```bash
cd /root/openclaw
git pull
pnpm install
pnpm run build
openclaw gateway restart
```

### 严禁方式
- ❌ npm update / npm install openclaw / npm upgrade
- ❌ 从 npm 源直接拉取预编译包

---

## 系统配置

- OpenClaw 源码：`/root/openclaw`
- 包管理器：pnpm
- Gateway MemoryMax：2.5GB
- 配置文件：`~/.config/systemd/user/openclaw-gateway.service.d/memory-limit.conf`

---

## GitHub 配置

- GitHub CLI：已安装 (gh 2.23.0)
- 认证账号：ai-nurmamat
- 监控仓库：
  - Ozluk/Ozluk（Issues 禁用）
  - ai-nurmamat/AMP
  - ai-nurmamat/debate
  - ai-nurmamat/middle-manager
  - ai-nurmamat/devmind-ai

---

## Cron 任务配置

| Agent | 频率 | 状态 |
|-------|------|------|
| ci-check | 每小时 | ok |
| issue-manager | 每2小时 | ok |
| comment-replier | 每4小时 | ok |
| pr-creator | 每小时 | ok |
| pr-reviewer | 每小时 | ok |
| pr-fixer | 每小时 | ok |

---

## 职责边界

- **pr-creator** = 只写代码，不审查、不修复
- **pr-reviewer** = 只审查，不写代码、不修复
- **pr-fixer** = 只修复，不写代码、不审查
- **issue-manager** = 只分配任务，不做开发
- **comment-replier** = 只回复评论，不做开发

---

## 重要教训

1. Cron 任务需要指定 `--agent <agent-id>` 才能让对应 agent 处理
2. GitHub Token 需要配置到环境变量或 gh auth login
3. Cron delivery.mode 需要设为 "announce" 才能发送汇报
