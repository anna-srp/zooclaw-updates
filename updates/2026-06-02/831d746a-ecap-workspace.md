---
title: "[平台] add Microsoft Teams channel option"
type: "新功能上线"
priority: "高"
date: "2026-06-02"
status: "待审核"
channels: ""
---
# [平台] add Microsoft Teams channel option

## 核心宣传点
来自 ecap-workspace 仓库的更新：feat(settings): add Microsoft Teams channel option

## 原始内容
**Commit**: 831d746a36efdbff231c933241acd9ad52ac3db4
**Title**: feat(settings): add Microsoft Teams channel option (#1992)
**Author**: kaka-srp
**Date**: 2026-06-02T13:15:28Z

**PR**: #1992

### Commit Message
```
feat(settings): add Microsoft Teams channel option (#1992)

## Linear

https://linear.app/srpone/issue/ECA-845/add-microsoft-teams-channel-integration

## Summary
- Add Microsoft Teams to the channel picker and display existing
`msteams` channels as Microsoft Teams.
- Reuse the existing manual channel credential flow with App ID, App
Password, and optional Tenant ID.
- Add unit coverage for the platform picker, card label, and optional
Tenant ID payload.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit`
- [ ] Real Microsoft Teams end-to-end messaging test, blocked locally by
no Microsoft 365 Teams tenant/account.
```

### PR Description
## Linear
https://linear.app/srpone/issue/ECA-845/add-microsoft-teams-channel-integration

## Summary
- Add Microsoft Teams to the channel picker and display existing `msteams` channels as Microsoft Teams.
- Reuse the existing manual channel credential flow with App ID, App Password, and optional Tenant ID.
- Add unit coverage for the platform picker, card label, and optional Tenant ID payload.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit`
- [ ] Real Microsoft Teams end-to-end messaging test, blocked locally by no Microsoft 365 Teams tenant/account.

