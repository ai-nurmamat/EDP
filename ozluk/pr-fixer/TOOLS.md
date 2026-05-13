# TOOLS.md - 工具说明

## GitHub CLI 常用命令

```bash
# 查看需要修复的 PR
gh pr list --state open --repo ai-nurmamat/ozluk

# 检出 PR
gh pr checkout <number>

# 推送修复
git push origin <branch>
```

## 修复流程

1. 定位问题根因
2. 编写修复代码
3. 添加回归测试
4. 验证修复有效
