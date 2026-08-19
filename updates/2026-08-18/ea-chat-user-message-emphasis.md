---
title: "聊天里你自己发的消息更醒目，能力受限提示文案更清晰"
type: "体验优化"
priority: "中"
date: "2026-08-18"
status: "待审核"
channels: ""
---

# 聊天里你自己发的消息更醒目，能力受限提示文案更清晰

## 核心宣传点

在主聊天、紧凑视图、分享会话、深度研究等所有聊天界面，用户自己发的消息统一加粗到 500 字重，和 AI 回复一眼分得清；能力降级提示也改成更好懂的「AI 能力受限 · 理解力 {score}/100」，操作按钮改为「提升能力」。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `bd2d807414ed4cb8923f7e0f228f5a8944194d68`
- PR: #3366
- 作者: shana-srp
- 日期: 2026-08-18T09:14:23Z

### Commit Message

```
fix(chat): improve user message emphasis (#3366)

## Summary

- set user-authored chat message text to a consistent 500 font weight
across main, compact, shared-thread, deep-research, card-action, and
feedback chat surfaces
- keep assistant response body text at its existing default weight
- replace the Chinese degradation copy with “AI 能力受限 · 理解力 {score}/100”
and rename the action to “提升能力”
- add regression coverage for user-versus-assistant message emphasis

## Testing

- `pnpm --dir web/packages/chat-ui test` — 354 tests passed
- `pnpm --dir web/packages/chat-ui tsc`
- `pnpm --dir web/packages/chat-ui lint`
- targeted web app tests — 51 tests passed
- targeted ESLint for changed app files

## Notes

- Tailwind `font-medium` is used because it maps to font weight 500;
`font-semibold` maps to 600.

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

```
## Summary

- set user-authored chat message text to a consistent 500 font weight across main, compact, shared-thread, deep-research, card-action, and feedback chat surfaces
- keep assistant response body text at its existing default weight
- replace the Chinese degradation copy with “AI 能力受限 · 理解力 {score}/100” and rename the action to “提升能力”
- add regression coverage for user-versus-assistant message emphasis

## Testing

- `pnpm --dir web/packages/chat-ui test` — 354 tests passed
- `pnpm --dir web/packages/chat-ui tsc`
- `pnpm --dir web/packages/chat-ui lint`
- targeted web app tests — 51 tests passed
- targeted ESLint for changed app files

## Notes

- Tailwind `font-medium` is used because it maps to font weight 500; `font-semibold` maps to 600.

```
