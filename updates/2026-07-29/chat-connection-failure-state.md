---
title: "聊天连接失败时不再暴露技术报错：改为友好的重连提示（中英文）"
type: "体验优化"
priority: "中"
date: "2026-07-29"
status: "待审核"
channels: ""
---

## 核心宣传点

当聊天与 Agent 的连接中断时，之前会把底层传输错误和内部主机名直接甩给你；现在换成了带插图、中英文文案的「连接恢复中」友好状态，并保留一键重试，界面更专业、不再泄露技术细节。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- commit：f11273537a311b3a5d3eb9210e25c51cf229535e
- PR：#3117
- 日期：2026-07-29T09:11:47Z

### Commit message

```
fix(chat): improve agent connection failure state (#3117)

## Summary

- Replace the raw Mattermost fetch error with a product-safe agent
connection recovery state.
- Use the supplied no-connection illustration, visually offset 10px
left, with localized English and Chinese copy.
- Preserve the retry behavior while hiding duplicated technical errors
and internal hostnames.

## Root cause

The full-screen Mattermost failure path reused a low-level error view
that exposed transport details directly to users. This produced
Claw-specific terminology, duplicated failure messaging, and internal
service URLs instead of an actionable Agent recovery state.

## Test plan

- [x] `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/chat/ChatGateStates-recorder.unit.spec.tsx
tests/unit/app/chat/GenClawClient.internals.unit.spec.tsx` — 53 tests
passed
- [x] `bash scripts/verify-web.sh --no-test ...` — governance guards,
TypeScript, and ESLint passed
- [x] `bash scripts/verify-changed.sh` — changed frontend surface passed
- [x] Browser visual validation — illustration returned HTTP 200,
decoded at 200x200, and measured 10px left of the button center

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
```

### PR body

## Summary

- Replace the raw Mattermost fetch error with a product-safe agent connection recovery state.
- Use the supplied no-connection illustration, visually offset 10px left, with localized English and Chinese copy.
- Preserve the retry behavior while hiding duplicated technical errors and internal hostnames.

## Root cause

The full-screen Mattermost failure path reused a low-level error view that exposed transport details directly to users. This produced Claw-specific terminology, duplicated failure messaging, and internal service URLs instead of an actionable Agent recovery state.

## Test plan

- [x] `pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/chat/ChatGateStates-recorder.unit.spec.tsx tests/unit/app/chat/GenClawClient.internals.unit.spec.tsx` — 53 tests passed
- [x] `bash scripts/verify-web.sh --no-test ...` — governance guards, TypeScript, and ESLint passed
- [x] `bash scripts/verify-changed.sh` — changed frontend surface passed
- [x] Browser visual validation — illustration returned HTTP 200, decoded at 200x200, and measured 10px left of the button center

