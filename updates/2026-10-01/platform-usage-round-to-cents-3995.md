---
title: "修复：Usage 汇总金额按美分四舍五入，小额明细不再显示为 $0.00"
type: "Bug Fix"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: ""
---

# 修复：Usage 汇总金额按美分四舍五入，小额明细不再显示为 $0.00

## 核心宣传点

开发者平台 Usage 的汇总金额现在按美分四舍五入，例如 $0.405717 会显示成 $0.41；单条用量记录则保留最多六位小数，避免很小的费用被显示成 $0.00。原因是汇总和明细之前共用同一套最多六位小数的格式化逻辑。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary / 变更概述
- Usage 汇总金额按美分四舍五入，例如 `$0.405717` 显示为 `$0.41`。
- 单条 Usage 记录保留最多六位小数，避免小额费用显示为 `$0.00`。
- Round the Usage summary to cents while preserving up to six decimals for individual records.

## Root cause / 原因
汇总和明细共用最多六位小数的金额格式化函数，导致汇总展示过多小数位。The summary and individual records shared the same six-decimal formatter.

## Test plan / 验证
- [x] `pnpm typecheck` in `web/platform`
- [x] `pnpm exec vitest run src/routes/usage.test.tsx` (11 tests)
- [x] ESLint for the three changed files
- [x] `git diff --check`

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `43849158dd1f3a30b2598ac57c9be8e0b12cfff6`
- PR: #3995
- 作者：david-srp
- 日期：2026-10-01T18:55:13Z

### Commit Message

```
fix(platform): Usage 汇总金额按美分四舍五入 / round total spend to cents (#3995)

## Summary / 变更概述
- Usage 汇总金额按美分四舍五入，例如 `$0.405717` 显示为 `$0.41`。
- 单条 Usage 记录保留最多六位小数，避免小额费用显示为 `$0.00`。
- Round the Usage summary to cents while preserving up to six decimals
for individual records.

## Root cause / 原因
汇总和明细共用最多六位小数的金额格式化函数，导致汇总展示过多小数位。The summary and individual records
shared the same six-decimal formatter.

## Test plan / 验证
- [x] `pnpm typecheck` in `web/platform`
- [x] `pnpm exec vitest run src/routes/usage.test.tsx` (11 tests)
- [x] ESLint for the three changed files
- [x] `git diff --check`
```

来源：SerendipityOneInc/ecap-workspace @ 43849158，PR #3995，作者 david-srp。
