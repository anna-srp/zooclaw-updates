---
title: "优化 IM 频道连接的快捷引导提示"
type: "体验优化"
priority: "低"
date: "2026-07-10"
status: "待审核"
channels: ""
---

## 核心宣传点

更新了“连接 IM 频道”快捷指令的引导文案，现在会更清楚地指引你从左下角头像菜单进入 设置 > IM 频道 完成连接。

## 原始内容

**fix(web): update IM channel quick start prompt (#2761)**

SHA: `a7d26c12828e36f6858aa4b7ad042ef027494cee` | 作者: rayrain-srp | PR #2761

```
fix(web): update IM channel quick start prompt (#2761)

## Summary
- Update the built-in main-agent `connect-im` Quick Start prompt to send
users to ZooClaw `Settings > IM Channels` from the bottom-left avatar
menu.
- Keep the existing quick-command click behavior and localized label
behavior unchanged.
- Add regression coverage for the prompt contents and New Chat card
subtitle.

## Linear
- https://linear.app/srpone/issue/ECA-1179/

## Test Plan
- `bash -lc 'source ~/.nvm/nvm.sh && nvm use 24.16.0 >/dev/null && bash
scripts/verify-web.sh
web/app/src/app/'"'"'[locale]'"'"'/'"'"'(app)'"'"'/'"'"'(chat)'"'"'/chat/components/quick-commands.ts
web/app/tests/unit/app/chat/quick-commands.unit.spec.ts
web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx'`
- pre-push changed-surface gate: PR size budget, `verify-web.sh
--no-test` (`tsc`, full frontend lint, guards)

This is the ECA-1179 short-term prompt stopgap only. It does not add
quick-command navigation; a future fix can make this command open
`/claw-settings?tab=channels` directly.

---------

Co-authored-by: Developer <dev@srp.one>
```

### PR body

## Summary
- Update the built-in main-agent `connect-im` Quick Start prompt to send users to ZooClaw `Settings > IM Channels` from the bottom-left avatar menu.
- Keep the existing quick-command click behavior and localized label behavior unchanged.
- Add regression coverage for the prompt contents and New Chat card subtitle.

## Linear
- https://linear.app/srpone/issue/ECA-1179/

## Test Plan
- `bash -lc 'source ~/.nvm/nvm.sh && nvm use 24.16.0 >/dev/null && bash scripts/verify-web.sh web/app/src/app/'"'"'[locale]'"'"'/'"'"'(app)'"'"'/'"'"'(chat)'"'"'/chat/components/quick-commands.ts web/app/tests/unit/app/chat/quick-commands.unit.spec.ts web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx'`
- pre-push changed-surface gate: PR size budget, `verify-web.sh --no-test` (`tsc`, full frontend lint, guards)

This is the ECA-1179 short-term prompt stopgap only. It does not add quick-command navigation; a future fix can make this command open `/claw-settings?tab=channels` directly.

