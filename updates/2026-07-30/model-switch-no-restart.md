---
title: "切换模型即时生效，无需重启提示"
type: "体验优化"
priority: "中"
date: "2026-07-30"
status: "待审核"
channels: ""
---

## 核心宣传点

ZooClaw Engine 智能体切换模型时即时生效，不再弹出多余的重启提示，模型切换更顺滑。

## 原始内容

**Commit**: 5a844d9c (PR #3144)
**外部评级**: B | **内部**: P2 | **信息类型**: 体验优化

### Commit Message

```
fix(chat): skip restart prompt for v2 model changes (#3144)

## Summary

- pass the selected agent workspace runtime through every chat composer
surface
- apply ZooClaw Engine model changes without showing the OpenClaw
restart prompt
- preserve the existing restart flow for computer-backed agents
- add regression coverage for runtime propagation and the engine
no-restart behavior

## Root cause

The shared composer treated every successful model update as an OpenClaw
configuration change. ZooClaw Engine applies v2 model updates
immediately, so engine-backed agents were incorrectly asked to restart
after a successful update.

## Test plan

- [x] Web governance guards
- [x] Targeted Vitest run: 12 files, 315 tests passed
- [x] ESLint for all changed files
- [x] Full web ESLint through `scripts/verify-changed.sh`

## Known unrelated check failure

The project-wide TypeScript check currently fails at
`src/app/[locale]/(app)/plugins/PluginsClient.tsx:31` because
`searchParams` may be null. This file is unchanged by this PR.
```

### PR Body

## Summary

- pass the selected agent workspace runtime through every chat composer surface
- apply ZooClaw Engine model changes without showing the OpenClaw restart prompt
- preserve the existing restart flow for computer-backed agents
- add regression coverage for runtime propagation and the engine no-restart behavior

## Root cause

The shared composer treated every successful model update as an OpenClaw configuration change. ZooClaw Engine applies v2 model updates immediately, so engine-backed agents were incorrectly asked to restart after a successful update.

## Test plan

- [x] Web governance guards
- [x] Targeted Vitest run: 12 files, 315 tests passed
- [x] ESLint for all changed files
- [x] Full web ESLint through `scripts/verify-changed.sh`

## Known unrelated check failure

The project-wide TypeScript check currently fails at `src/app/[locale]/(app)/plugins/PluginsClient.tsx:31` because `searchParams` may be null. This file is unchanged by this PR.

