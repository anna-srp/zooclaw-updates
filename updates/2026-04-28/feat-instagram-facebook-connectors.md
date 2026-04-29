---
title: "上线 Instagram 和 Facebook 数据连接器"
type: "新功能上线"
priority: "高"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 上线 Instagram 和 Facebook 数据连接器

## 核心宣传点

ZooClaw 现在支持连接你的 Instagram 和 Facebook 账号，Agent 可以直接访问你的社交媒体数据来完成任务。

## 原始内容

**Commit**: `3b23fa862a742b435b877f2a2215bd3f763c21d0`
**仓库**: ecap-workspace
**作者**: Leo-srp
**时间**: 2026-04-28T08:51:04Z

### 完整 Commit Message

```
feat(web): enable Instagram + Facebook connectors in production (#1434)

## Summary
- Add `instagram` and `facebook` to `PROD_ENABLED_PROVIDERS` in
`ConnectorsSection.tsx` so the Nango cards render in claw-settings on
prod.
- Mirrors the Google connector rollout pattern from #1294.

## Pre-deploy check
- Confirm Instagram + Facebook providers are configured in the
**production** Nango instance (OAuth app, scopes, callback URL). Without
that, users clicking *Connect* will hit an OAuth error.

## Test plan
- [ ] Smoke check on staging: Instagram + Facebook cards render in
claw-settings and OAuth flow succeeds end-to-end
- [ ] After deploy, verify the same on production with a test account

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR #1434 完整描述

## Summary
- Add `instagram` and `facebook` to `PROD_ENABLED_PROVIDERS` in `ConnectorsSection.tsx` so the Nango cards render in claw-settings on prod.
- Mirrors the Google connector rollout pattern from #1294.

## Pre-deploy check
- Confirm Instagram + Facebook providers are configured in the **production** Nango instance (OAuth app, scopes, callback URL). Without that, users clicking *Connect* will hit an OAuth error.

## Test plan
- [ ] Smoke check on staging: Instagram + Facebook cards render in claw-settings and OAuth flow succeeds end-to-end
- [ ] After deploy, verify the same on production with a test account

🤖 Generated with [Claude Code](https://claude.com/claude-code)
