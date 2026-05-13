# TOOLS.md - 工具说明

## GitHub CLI 常用命令

```bash
# 查看分配给我的 Issue
gh issue list --assignee @me --repo ai-nurmamat/ozluk

# 创建分支
git checkout -b feature/<issue-number>

# 创建 PR
gh pr create --title "feat: <description>" --body "Closes #<issue-number>"
```

## 开发流程

1. 接收任务 → 确认需求
2. 创建分支 → 编写代码
3. 编写测试 → 提交 PR
4. 等待审查 → 不自己合并
