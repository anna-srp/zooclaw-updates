---
title: "修复：用量明细里工具服务记录统一标注为「工具使用」"
type: "Bug Fix"
priority: "低"
date: "2026-10-26"
status: "待审核"
channels: ""
---

# 修复：用量明细里工具服务记录统一标注为「工具使用」

## 核心宣传点

用量明细中属于工具服务的记录此前标签混乱不易辨认，现在统一显示为「工具使用」（英文 `Tool usage`），已配置的模型名称和「Compute」标签保持原样。本次只改展示，用量记录和计费数据都不变，表格样式、本地化格式、范围筛选和游标分页也保持现状。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `8bfe5b087ab1e2892e6da722b578938657c3b787`
- PR: #3848
- 作者：kaka-srp
- 日期：2026-10-26T03:18:23Z

### Commit Message

```
fix(usage): group tool service labels (#3848)

## Summary

Usage details now label tool-service records as `Tool usage` / `工具使用`,
while retaining configured model names and `Compute`. This changes
presentation only and preserves usage records and billing data.

The branch is synchronized with current main, preserving the current
table styling, locale formatting, scoped filters, and cursor pagination.

## Validation

- Focused `UsageDimensions` regression suite: 8 tests passed, including
tool/model/compute labels, pagination, refresh, and scoped filters.
- Local frontend governance guards, TypeScript, and targeted ESLint
passed. The final JSX-only formatting correction passed targeted ESLint.
- `git diff --check` and local PR size check passed.
- Updated-head GitHub CI passed, including frontend tests, type/lint
checks, production build, CodeQL, and PR size checks. Claude and Codex
automated reviews both approved with no findings.
```
