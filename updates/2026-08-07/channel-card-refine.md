---
title: "渠道卡片界面优化"
type: "体验优化"
priority: "中"
date: "2026-08-07"
status: "待审核"
channels: ""
---

## 核心宣传点

渠道页更清爽：卡片直接显示绑定的 Agent 和头像，连接状态图标、飞书配置流程与二维码提示都更易读。

## 原始内容

### feat(channels): refine channel card interactions (#3252)

- SHA: `09fdb77a5a18a6d4308b7d26324a0b04a02fd705`
- 仓库: 见 raw/2026-08-07

**Commit Message:**

```
feat(channels): refine channel card interactions (#3252)

## Summary

- simplify channel cards by removing policy fields and showing the bound
Agent with its avatar
- refine connected/disconnected platform icon states, including the
updated Feishu asset and consistent Weixin gray treatment
- improve Feishu/Lark setup layout, dynamic QR action copy, platform
card ordering, and channels header alignment

## Testing

- `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/claw-settings/ChannelsSection.unit.spec.tsx
tests/unit/app/claw-settings/ChannelsSection-engine.unit.spec.tsx` (43
passed, 69 skipped)
- merged latest `origin/main`, then `scripts/verify-web.sh` selected 10
channel-related test files: 110 passed, 69 skipped
- targeted ESLint passed
- `git diff --check` passed

## Known baseline issue

- full TypeScript verification is currently blocked by unrelated
mainline errors in `UnifiedChatComposer.tsx` (`AgentPickerProps.open`)
and `packages/chat-ui/src/types.ts` (React type resolution)

## Screenshots

- validated locally on `/channels` for connected Feishu, Agent avatar
placement, add-platform dialog, Feishu/Lark setup, card ordering, and
header layout

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

**PR Body:**

## Summary

- simplify channel cards by removing policy fields and showing the bound Agent with its avatar
- refine connected/disconnected platform icon states, including the updated Feishu asset and consistent Weixin gray treatment
- improve Feishu/Lark setup layout, dynamic QR action copy, platform card ordering, and channels header alignment

## Testing

- `pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/claw-settings/ChannelsSection.unit.spec.tsx tests/unit/app/claw-settings/ChannelsSection-engine.unit.spec.tsx` (43 passed, 69 skipped)
- merged latest `origin/main`, then `scripts/verify-web.sh` selected 10 channel-related test files: 110 passed, 69 skipped
- targeted ESLint passed
- `git diff --check` passed

## Known baseline issue

- full TypeScript verification is currently blocked by unrelated mainline errors in `UnifiedChatComposer.tsx` (`AgentPickerProps.open`) and `packages/chat-ui/src/types.ts` (React type resolution)

## Screenshots

- validated locally on `/channels` for connected Feishu, Agent avatar placement, add-platform dialog, Feishu/Lark setup, card ordering, and header layout


