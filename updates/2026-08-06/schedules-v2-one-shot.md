---
title: "一次性定时任务全流程打通：能建、能留存、能看结果"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-06"
status: "待审核"
channels: ""
---

## 核心宣传点

定时任务页的一次性任务修好了：填的时间按你浏览器所在时区正确换算成执行时刻，执行完的任务会作为只读历史保留，并且可以点开查看这次任务的运行结果。

## 原始内容

**fix(schedules): complete v2 one-shot workflow (#3285)**

- sha: `f857f5a4796012242bccc6e8a6e4a7383c796df6`
- PR: #3285

```
fix(schedules): complete v2 one-shot workflow (#3285)

## Summary

- interpret the Schedule page's `datetime-local` input in browser local
time and send the corresponding UTC instant, with explicit UI guidance
- make product-created Engine one-shots request `deleteAfterRun`, keep
completed runs visible as read-only history, and map Temporal month
names back to ISO instants
- expose schedule-scoped isolated-session results through claw-interface
and a dedicated read-only Web result page
- keep Engine delivery fixed to `none`; this PR does not add
owner-default onboarding or an outbound destination selector

Engine dependency:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/624

## Root cause

The V2 product flow crossed several incomplete contracts: the Engine
emitted Temporal calendar month names that claw-interface did not map
back, product `at` requests did not opt into one-shot cleanup, run
projections did not expose their isolated result session, and the UI did
not explain that `datetime-local` is browser-local before conversion to
UTC. As a result, users could not reliably create, retain, or inspect
one-shot jobs even after the Engine-side create bug was fixed.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Web schedule tests: 8 files, 233 tests passed (1 todo)
- [x] claw-interface schedule tests: 92 passed
- [x] Web governance guards, TypeScript, and ESLint passed
- [x] Python ruff, format, pyright, and import-linter passed
- [ ] After Engine PR deployment, create a future `at` job in staging
and verify it fires once at the matching UTC instant
- [ ] Verify the completed job remains in history and its result link
renders only assistant-visible text
```

**PR Body:**

## Summary

- interpret the Schedule page's `datetime-local` input in browser local time and send the corresponding UTC instant, with explicit UI guidance
- make product-created Engine one-shots request `deleteAfterRun`, keep completed runs visible as read-only history, and map Temporal month names back to ISO instants
- expose schedule-scoped isolated-session results through claw-interface and a dedicated read-only Web result page
- keep Engine delivery fixed to `none`; this PR does not add owner-default onboarding or an outbound destination selector

Engine dependency: https://github.com/SerendipityOneInc/zooclaw-engine/pull/624

## Root cause

The V2 product flow crossed several incomplete contracts: the Engine emitted Temporal calendar month names that claw-interface did not map back, product `at` requests did not opt into one-shot cleanup, run projections did not expose their isolated result session, and the UI did not explain that `datetime-local` is browser-local before conversion to UTC. As a result, users could not reliably create, retain, or inspect one-shot jobs even after the Engine-side create bug was fixed.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Web schedule tests: 8 files, 233 tests passed (1 todo)
- [x] claw-interface schedule tests: 92 passed
- [x] Web governance guards, TypeScript, and ESLint passed
- [x] Python ruff, format, pyright, and import-linter passed
- [ ] After Engine PR deployment, create a future `at` job in staging and verify it fires once at the matching UTC instant
- [ ] Verify the completed job remains in history and its result link renders only assistant-visible text

