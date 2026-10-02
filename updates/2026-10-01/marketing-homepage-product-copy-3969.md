---
title: "官网首页第三张产品卡改为 Enterprise AI Stack，Get Started 菜单文案同步调整"
type: "体验优化"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: ""
---

# 官网首页第三张产品卡改为 Enterprise AI Stack，Get Started 菜单文案同步调整

## 核心宣传点

官网首页第三张产品卡的标题和描述改为 Enterprise AI Stack / Deploy, govern, and scale AI across your organization，共享的 Get Started 下拉里的条目则从 Agent Builder 改回 ZooWork.ai，其余入口和跳转保持不变。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
- Rename the shared Get Started dropdown entry from `Agent Builder` to `ZooWork.ai`.
- Update the third homepage product card to `Enterprise AI Stack` and `Deploy, govern, and scale AI across your organization.` Keep the existing Enterprise navigation label and all destinations unchanged.
- Synchronize the description across all 10 locale dictionaries and update existing homepage expectations. Frontend only; no backend changes.

## Test plan
- [x] Synced local main and based the branch on `1ba301d89`.
- [x] Existing header, homepage and locale dictionary suites: 114 tests passed (including desktop login, handoff parameters and mobile drawer behavior).
- [x] Changed-surface pre-push verification: governance guards, TypeScript, full frontend ESLint passed.
- [x] Local Edge browser verified desktop and mobile dropdown/product card copy; no mobile horizontal overflow or page errors.
- [x] `git diff --check`.
- Local preview: `http://localhost:3020/` (preview-only Firebase configuration; authentication is outside this copy-change validation).

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `8d707fd3625c00575a00d7a32ffb0b1fbc550681`
- PR: #3969
- 作者：ericma-srp
- 日期：2026-10-01T02:37:47Z

### Commit Message

```
fix(marketing): update homepage product copy (#3969)

## Summary
- Rename the shared Get Started dropdown entry from `Agent Builder` to
`ZooWork.ai`.
- Update the third homepage product card to `Enterprise AI Stack` and
`Deploy, govern, and scale AI across your organization.` Keep the
existing Enterprise navigation label and all destinations unchanged.
- Synchronize the description across all 10 locale dictionaries and
update existing homepage expectations. Frontend only; no backend
changes.

## Test plan
- [x] Synced local main and based the branch on `1ba301d89`.
- [x] Existing header, homepage and locale dictionary suites: 114 tests
passed (including desktop login, handoff parameters and mobile drawer
behavior).
- [x] Changed-surface pre-push verification: governance guards,
TypeScript, full frontend ESLint passed.
- [x] Local Edge browser verified desktop and mobile dropdown/product
card copy; no mobile horizontal overflow or page errors.
- [x] `git diff --check`.
- Local preview: `http://localhost:3020/` (preview-only Firebase
configuration; authentication is outside this copy-change validation).
```

来源：SerendipityOneInc/ecap-workspace @ 8d707fd3，PR #3969，作者 ericma-srp。
