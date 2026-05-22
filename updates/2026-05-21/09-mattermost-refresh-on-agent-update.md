---
title: "更新 Agent 后 Mattermost Bot 自动刷新"
type: "Bug Fix"
priority: "低"
date: "2026-05-21"
status: "待审核"
channels: "Discord, changelog"
---

# 更新 Agent 后 Mattermost Bot 自动刷新

## 核心宣传点

修改 Agent 设置后，关联的 Mattermost Bot 现在会自动同步更新，不再需要手动刷新。

## 原始内容

```
fix(web): refresh Mattermost bots after agent updates (#1719)

After an agent is updated, automatically refresh Mattermost bot associations so the changes are reflected immediately without manual intervention.
```
