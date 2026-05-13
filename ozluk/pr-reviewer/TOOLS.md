# TOOLS.md - 工具说明

## GitHub CLI 常用命令

```bash
# 查看待审查 PR
gh pr list --state open --repo ai-nurmamat/ozluk

# 查看 PR 详情
gh pr view <number>

# 审查 PR
gh pr review <number> --approve/--request-changes
```

## 审查重点

1. 代码质量和可读性
2. 安全漏洞
3. 性能问题
4. 测试覆盖
5. 文档完整性
