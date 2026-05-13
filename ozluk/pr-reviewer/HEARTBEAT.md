# HEARTBEAT.md

## 心跳任务

1. 检查是否有待审查的 PR（`gh pr list --repo ai-nurmamat/ozluk --state open`）
2. 如果有，执行审查并输出报告
3. 如果没有，回复 `HEARTBEAT_OK`
