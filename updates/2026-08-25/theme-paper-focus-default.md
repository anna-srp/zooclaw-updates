---
title: "网页端换新默认外观 Paper Focus，原来的玻璃拟态改为可选皮肤"
type: "体验优化"
priority: "中"
date: "2026-08-25"
status: "待审核"
channels: ""
---

# 网页端换新默认外观 Paper Focus，原来的玻璃拟态改为可选皮肤

## 核心宣传点

浅色模式的默认外观换成了更干净、更适合长时间阅读的 Paper Focus 皮肤，桌面端侧边栏宽度也一并调整到 260px；原来那套半透明玻璃质感被保留下来，改名为「Pure Glass」放进皮肤列表，喜欢的话随时可以在外观设置里切回去。点击「恢复默认」时也会回到 Paper Focus。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `978d1a6fa8fe076857fc996c4dd36c070dca03a5`
- PR: #3507
- 作者: shana-srp
- 日期: 2026-08-25T07:59:19Z

### Commit Message

```
feat(theme): make Paper Focus the primary skin (#3507)

## Linear

N/A — no linked Linear issue was provided.

## Summary

- make Paper Focus the default primary skin and reset target for
Appearance Light
- expose the former `panda-claw` treatment as the optional Pure Glass
skin, with clean white neutral styling and no duplicate Paper Focus card
- align the Paper Focus desktop sidebar to 260px and cover bootstrap,
persistence, provider, asset, and selector behavior with focused tests

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/verify-web.sh --no-test <changed TypeScript files>`
- [x] focused Vitest suite: 5 files, 87 tests passed
- [x] `git diff --check origin/main...HEAD`

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Description

```
## Linear

N/A — no linked Linear issue was provided.

## Summary

- make Paper Focus the default primary skin and reset target for Appearance Light
- expose the former `panda-claw` treatment as the optional Pure Glass skin, with clean white neutral styling and no duplicate Paper Focus card
- align the Paper Focus desktop sidebar to 260px and cover bootstrap, persistence, provider, asset, and selector behavior with focused tests

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/verify-web.sh --no-test <changed TypeScript files>`
- [x] focused Vitest suite: 5 files, 87 tests passed
- [x] `git diff --check origin/main...HEAD`

```
