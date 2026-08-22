---
title: "聊天输入框「添加」菜单完成中文本地化"
type: "体验优化"
priority: "中"
date: "2026-08-21"
status: "待审核"
channels: ""
---

# 聊天输入框「添加」菜单完成中文本地化

## 核心宣传点

聊天输入框里的「+ 添加」入口以及它下面的最近文件、Skills、Skill 商店、素材库几个面板，此前不管切换到哪种语言都只显示英文，加载中、出错、空列表这些状态也一样。现在中文用户看到的是完整的中文界面，其他语言仍会回退到英文，不影响已有翻译。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `2a2a970a96a89c639ee2dbe4415a0938f33b0d30`
- PR: #3473
- 作者: rayrain-srp
- 日期: 2026-08-21T12:29:06Z

### Commit Message

```
fix(chat): localize composer add menu (#3473)

## Summary

- Localize the Composer Add trigger and its Recent, Skills, Skill Store,
and Asset Library flows in English and Simplified Chinese.
- Keep shared `@zooclaw/chat-ui` components presentational by passing
localized labels from the app.
- Preserve English fallback for every other locale through the existing
deep-merge dictionary behavior; no other locale files are changed.
- Linear:
https://linear.app/srpone/issue/ECA-1389/chat-i18n-localize-add-menu-tooltip-and-attachment-menu-copy

## Root cause

The unified Composer Add menu and its nested attachment surfaces
contained hard-coded English strings, including the trigger tooltip/ARIA
label and loading, error, empty, and action copy. Shared chat UI
components also owned user-facing defaults, so the app locale could not
translate those states consistently in either v1 or v2.

## Test plan

- [x] App unit tests: 11 files / 94 tests covering English, Chinese,
menu states, localized prompt insertion, and non-English fallback.
- [x] Agent Builder integration regressions: 2 files / 73 tests covering
Composer usage from the creation flow.
- [x] Shared chat-ui unit tests: 2 files / 20 tests covering the
localized label contracts and loading/error/empty states.
- [x] `pnpm tsc` and targeted ESLint for `@zooclaw/chat-ui`.
- [x] `bash scripts/verify-web.sh --no-test` for the changed app surface
(governance guards, full app TypeScript, ESLint).
- [x] Pre-push changed-surface verification.
```

### PR Body

## Summary

- Localize the Composer Add trigger and its Recent, Skills, Skill Store, and Asset Library flows in English and Simplified Chinese.
- Keep shared `@zooclaw/chat-ui` components presentational by passing localized labels from the app.
- Preserve English fallback for every other locale through the existing deep-merge dictionary behavior; no other locale files are changed.
- Linear: https://linear.app/srpone/issue/ECA-1389/chat-i18n-localize-add-menu-tooltip-and-attachment-menu-copy

## Root cause

The unified Composer Add menu and its nested attachment surfaces contained hard-coded English strings, including the trigger tooltip/ARIA label and loading, error, empty, and action copy. Shared chat UI components also owned user-facing defaults, so the app locale could not translate those states consistently in either v1 or v2.

## Test plan

- [x] App unit tests: 11 files / 94 tests covering English, Chinese, menu states, localized prompt insertion, and non-English fallback.
- [x] Agent Builder integration regressions: 2 files / 73 tests covering Composer usage from the creation flow.
- [x] Shared chat-ui unit tests: 2 files / 20 tests covering the localized label contracts and loading/error/empty states.
- [x] `pnpm tsc` and targeted ESLint for `@zooclaw/chat-ui`.
- [x] `bash scripts/verify-web.sh --no-test` for the changed app surface (governance guards, full app TypeScript, ESLint).
- [x] Pre-push changed-surface verification.

