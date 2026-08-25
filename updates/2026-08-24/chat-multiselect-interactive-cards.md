---
title: "网页聊天支持多选交互卡片，一次可勾选多个选项再提交"
type: "新功能上线"
priority: "中"
date: "2026-08-24"
status: "待审核"
channels: ""
---

# 网页聊天支持多选交互卡片，一次可勾选多个选项再提交

## 核心宣传点

此前 Agent 发来的交互卡片只能单选、点一下就结束。现在网页端支持 multiselect 多选卡片：可以勾选多个选项后统一点「提交」，勾选状态由服务端保存，刷新或多端打开都一致；没勾任何一项时提交按钮为禁用状态。同时修掉了一个隐患——遇到未知卡片类型时不再崩溃，而是安全降级为文字提示。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `b810654f3e35ca691aaf4ec58f051b0ae78f1f1a`
- PR: #3482
- 作者: bill-srp
- 日期: 2026-08-24T02:57:02Z

### Commit Message

```
feat(chat): render multiselect interactive cards in the webapp (#3482)

## Linear
<!-- none -->

## Summary
Webapp support for the `multiselect` interactive card kind — companion
to [zooclaw-extras
#227](https://github.com/SerendipityOneInc/zooclaw-extras/pull/227),
which renders a multiselect card as N toggle buttons plus a Submit
button with selection state stored in the post itself. Design spec:
`docs/superpowers/specs/2026-08-21-chat-multiselect-cards-webapp.md`.

- **Schema** (`@zooclaw/chat-ui` `types.ts`): new `multiselect` member
of `InteractiveCardView` (`options` with server-authoritative `checked`,
`submitActionId`, `submitLabel`).
- **Parser** (`interactive-attachments.ts`): structural detection — ≥2
button actions, last id prefixed `cardmssubmit`, all preceding ids
prefixed `cardms` (Mattermost strips `integration.context` before posts
reach clients, so id shape + position is the only client-visible
signal). `checked` derives from the `✓ ` name prefix the plugin toggles
via post edits; label strips it. Non-matching shapes fall through to the
existing button-row path unchanged.
- **Renderer** (`InteractiveCards.tsx`): explicit `switch` on card kind
with a safe text-banner fallback for unknown kinds (previously a new
kind would fall into the select branch and crash). Multiselect renders
checkbox rows driven purely by props (no local selection model — state
lives in the post and updates via `post_edited`) plus a primary Submit
button disabled while nothing is checked (client-side guard for the
server's empty-submit ephemeral, which the webapp can't render).
- **Pending fix**: card `key` now includes a content signature, so the
authoritative post edit remounts the card and clears `pendingActionId`.
Previously pending never cleared on success — harmless when every click
ended the card, but it would have frozen a multiselect card after the
first toggle.
- **Float classification**: `multiselect` counts as pending, so it
floats above the composer and is suppressed inline exactly like
`buttons`/`select`.
- No transport changes: toggle and submit are plain post actions through
the existing `doPostAction`.

Out of scope (pre-existing, tracked separately): card-only posts dropped
by the replay snapshot pipeline.

## Test plan
- [x] Parser: multiselect detection with mixed checked state + `✓ `
stripping, minimum shape, plain button rows unaffected,
`cardms`-prefixed rows without a trailing submit stay a button row,
malformed shapes fall through (`interactive-attachments.unit.spec.ts`)
- [x] Renderer: checkbox/submit rendering from server state, toggle +
submit dispatch, submit disabled with zero checked, all controls
disabled while pending, pending clears on content remount, unknown-kind
fallback (`interactive-cards.test.tsx`)
- [x] Float: multiselect pending/inline/float behavior
(`interactive-card-float.unit.spec.ts`)
- [x] `bash scripts/verify-web.sh` full gate green (9,022 tests / 660
files, tsc, eslint, guards)
- [x] `@zooclaw/chat-ui` package suite 438/438 + tsc + eslint
- [ ] Live smoke against a Mattermost instance running the #227 plugin
build (blocked on #227 publish)
```

### PR Body

## Linear
<!-- none -->

## Summary
Webapp support for the `multiselect` interactive card kind — companion to [zooclaw-extras #227](https://github.com/SerendipityOneInc/zooclaw-extras/pull/227), which renders a multiselect card as N toggle buttons plus a Submit button with selection state stored in the post itself. Design spec: `docs/superpowers/specs/2026-08-21-chat-multiselect-cards-webapp.md`.

- **Schema** (`@zooclaw/chat-ui` `types.ts`): new `multiselect` member of `InteractiveCardView` (`options` with server-authoritative `checked`, `submitActionId`, `submitLabel`).
- **Parser** (`interactive-attachments.ts`): structural detection — ≥2 button actions, last id prefixed `cardmssubmit`, all preceding ids prefixed `cardms` (Mattermost strips `integration.context` before posts reach clients, so id shape + position is the only client-visible signal). `checked` derives from the `✓ ` name prefix the plugin toggles via post edits; label strips it. Non-matching shapes fall through to the existing button-row path unchanged.
- **Renderer** (`InteractiveCards.tsx`): explicit `switch` on card kind with a safe text-banner fallback for unknown kinds (previously a new kind would fall into the select branch and crash). Multiselect renders checkbox rows driven purely by props (no local selection model — state lives in the post and updates via `post_edited`) plus a primary Submit button disabled while nothing is checked (client-side guard for the server's empty-submit ephemeral, which the webapp can't render).
- **Pending fix**: card `key` now includes a content signature, so the authoritative post edit remounts the card and clears `pendingActionId`. Previously pending never cleared on success — harmless when every click ended the card, but it would have frozen a multiselect card after the first toggle.
- **Float classification**: `multiselect` counts as pending, so it floats above the composer and is suppressed inline exactly like `buttons`/`select`.
- No transport changes: toggle and submit are plain post actions through the existing `doPostAction`.

Out of scope (pre-existing, tracked separately): card-only posts dropped by the replay snapshot pipeline.

## Test plan
- [x] Parser: multiselect detection with mixed checked state + `✓ ` stripping, minimum shape, plain button rows unaffected, `cardms`-prefixed rows without a trailing submit stay a button row, malformed shapes fall through (`interactive-attachments.unit.spec.ts`)
- [x] Renderer: checkbox/submit rendering from server state, toggle + submit dispatch, submit disabled with zero checked, all controls disabled while pending, pending clears on content remount, unknown-kind fallback (`interactive-cards.test.tsx`)
- [x] Float: multiselect pending/inline/float behavior (`interactive-card-float.unit.spec.ts`)
- [x] `bash scripts/verify-web.sh` full gate green (9,022 tests / 660 files, tsc, eslint, guards)
- [x] `@zooclaw/chat-ui` package suite 438/438 + tsc + eslint
- [ ] Live smoke against a Mattermost instance running the #227 plugin build (blocked on #227 publish)

