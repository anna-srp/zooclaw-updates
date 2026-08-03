---
title: "Council 多模型调研功能上线（Beta）：支持调研深度与档位选择"
type: "新功能上线"
priority: "高"
外部: "A"
date: "2026-07-30"
status: "待审核"
channels: ""
---

## 核心宣传点

全新「Council」多模型调研功能进入 Beta：一次提问，多个顶尖模型协同调研。可自选调研深度（快速/标准/深度）和成本档位（经济/标准/premium），系统自动分派并汇总结论。

## 原始内容

**Commit**: 61cc126c (PR #3157)
**外部评级**: A | **内部**: P1 | **信息类型**: 新功能上线

### Commit Message

```
feat(council): automate approval with depth and tier intent (#3157)

## Linear

https://linear.app/srpone/issue/ECA-1211/council-多模型调研功能上线-beta-版

## Summary

First slice of #3139.

- Add Auto / Quick / Standard / Deep depth selection without consuming
the topic's 2,000-character budget.
- Add Economy / Standard / Premium tier intent.
- Automatically post `go` only for the exact run dispatched in the
current browser session.
- Wait for requested depth and tier to be observed before automatic
approval.
- Fall back to an explicit approval control after reload, dispatch
failure, tier timeout, or an observed depth mismatch.
- Replace the mutable confirmation gate with read-only run details and
explicit retry controls.

The Mattermost event refresh, dedicated hidden Council thread, and
synthesis summary are intentionally excluded and land in the follow-up
slices below.

## Stack

1. This PR — approval, depth, and tier intent
2. #3158 — dedicated run thread identity
3. #3160 — event-driven status refresh
4. #3161 — terminal thread synthesis

Review and merge in that order.

## Test plan

- [x] `bash scripts/verify-web.sh web/app/src/components/council
web/app/src/hooks/council web/app/tests/unit/app/council
web/app/tests/unit/hooks/council`
- [x] 64 selected Council tests
- [x] TypeScript and ESLint checks
```

### PR Body

## Linear

https://linear.app/srpone/issue/ECA-1211/council-多模型调研功能上线-beta-版

## Summary

First slice of #3139.

- Add Auto / Quick / Standard / Deep depth selection without consuming the topic's 2,000-character budget.
- Add Economy / Standard / Premium tier intent.
- Automatically post `go` only for the exact run dispatched in the current browser session.
- Wait for requested depth and tier to be observed before automatic approval.
- Fall back to an explicit approval control after reload, dispatch failure, tier timeout, or an observed depth mismatch.
- Replace the mutable confirmation gate with read-only run details and explicit retry controls.

The Mattermost event refresh, dedicated hidden Council thread, and synthesis summary are intentionally excluded and land in the follow-up slices below.

## Stack

1. This PR — approval, depth, and tier intent
2. #3158 — dedicated run thread identity
3. #3160 — event-driven status refresh
4. #3161 — terminal thread synthesis

Review and merge in that order.

## Test plan

- [x] `bash scripts/verify-web.sh web/app/src/components/council web/app/src/hooks/council web/app/tests/unit/app/council web/app/tests/unit/hooks/council`
- [x] 64 selected Council tests
- [x] TypeScript and ESLint checks

