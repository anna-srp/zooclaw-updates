---
title: "Google 连接器暂时下线，恢复 gog 卡片与 Notion 分类修复"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# Google 连接器暂时下线，恢复 gog 卡片与 Notion 分类修复

## 核心宣传点

Google 系列 Nango 连接器暂时从设置页下线（待进一步测试），同时恢复了 gog 工具卡片显示，修复了 Notion 连接器分类错误。

## 原始内容

**Commit**: `ae6868b5fcf5c5d67093cb598a8e037fe09c8f6e`
**仓库**: ecap-workspace
**作者**: Leo-srp
**时间**: 2026-04-28T09:28:57Z

### 完整 Commit Message

```
revert(web): hide Google Nango connectors in prod + restore gog card; fix Notion category (#1441)

## Summary
Two connector-settings adjustments bundled together (both touch the same
UI surface):

### 1. Roll back Google Nango exposure (#1294 partial revert)
- Remove `google-mail`, `google-calendar`, `google-drive`,
`google-sheet`, `youtube` from `PROD_ENABLED_PROVIDERS` so the Nango
cards are hidden in prod again (still visible in non-prod for testing).
- Unwrap the `{!IS_PROD && (…)}` around the **Google Workspace** (legacy
gog CLI) card so it renders in production again.
- Instagram and Facebook (#1434) stay enabled in prod — only the
Google/YouTube portion is rolled back.

### 2. Move Notion from Communication → Productivity (was #1437)
- Notion is a docs/wiki/knowledge tool, but in `AVAILABLE_PROVIDERS` it
was tagged `category: 'communication'`, so the connectors panel rendered
it under **Communication** alongside Slack and Microsoft Teams.
- Reclassify it as `productivity` and move it next to Asana / Airtable /
Figma so the source ordering and category field stay consistent.
- Supersedes #1437 (closing as duplicate).

## Test plan
- [ ] Prod: Google Workspace card (gog CLI) is visible; Gmail / Google
Calendar / Google Drive / Google Sheets / YouTube cards are hidden under
the Connectors section.
- [ ] Non-prod: all Google Nango cards remain visible and connectable
for ongoing testing.
- [ ] In claw-settings, browse connectors by category — Notion now
appears under **Productivity**, not **Communication**.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR #1441 完整描述

## Summary
Two connector-settings adjustments bundled together (both touch the same UI surface):

### 1. Roll back Google Nango exposure (#1294 partial revert)
- Remove `google-mail`, `google-calendar`, `google-drive`, `google-sheet`, `youtube` from `PROD_ENABLED_PROVIDERS` so the Nango cards are hidden in prod again (still visible in non-prod for testing).
- Unwrap the `{!IS_PROD && (…)}` around the **Google Workspace** (legacy gog CLI) card so it renders in production again.
- Instagram and Facebook (#1434) stay enabled in prod — only the Google/YouTube portion is rolled back.

### 2. Move Notion from Communication → Productivity (was #1437)
- Notion is a docs/wiki/knowledge tool, but in `AVAILABLE_PROVIDERS` it was tagged `category: 'communication'`, so the connectors panel rendered it under **Communication** alongside Slack and Microsoft Teams.
- Reclassify it as `productivity` and move it next to Asana / Airtable / Figma so the source ordering and category field stay consistent.
- Supersedes #1437 (closing as duplicate).

## Test plan
- [ ] Prod: Google Workspace card (gog CLI) is visible; Gmail / Google Calendar / Google Drive / Google Sheets / YouTube cards are hidden under the Connectors section.
- [ ] Non-prod: all Google Nango cards remain visible and connectable for ongoing testing.
- [ ] In claw-settings, browse connectors by category — Notion now appears under **Productivity**, not **Communication**.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

