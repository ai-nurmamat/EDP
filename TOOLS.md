# TOOLS.md - Local Notes

## 智能路由引擎

### 任务类型识别规则

| 关键词 | 任务类型 | 派发给 |
|--------|---------|--------|
| 创建、开发、编写、新增 | 开发 | pr-creator |
| 审查、检查、评估、review | 审查 | pr-reviewer |
| 修复、解决、bug、错误 | 修复 | pr-fixer |
| 前端、ui、界面、web | 前端 | frontend-dev |
| 后端、api、服务、server | 后端 | backend-dev |
| 测试、coverage、test | 测试 | tester |
| 文档、readme、guide | 文档 | doc-writer |
| ci、pipeline、workflow | CI/CD | ci-engineer |
| 安全、漏洞、security | 安全 | security-auditor |
| issue、工单、反馈 | Issue | issue-manager |
| 评论、回复、comment | 评论 | comment-replier |

---

## 任务派发模板

```markdown
📋 任务派发单

🎯 任务描述：[清晰描述要做什么]
📝 任务类型：[开发/审查/修复/文档/测试]
🔧 派发给：[执行者名称]
📌 优先级：[P0-紧急/P1-重要/P2-一般]
⏰ 截止时间：[具体时间]

✅ 验收标准：
1. [具体可衡量的标准1]
2. [具体可衡量的标准2]
```

---

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
- ❌ npm update
- ❌ npm install openclaw
- ❌ npm upgrade

---

## 系统配置

- OpenClaw 源码：`/root/openclaw`
- 包管理器：pnpm（不是 npm）
- Gateway MemoryMax：2.5GB
