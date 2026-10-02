---
title: "用户设置菜单里的 Managed Agent API 改为「Get API keys」双行入口"
type: "体验优化"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: ""
---

# 用户设置菜单里的 Managed Agent API 改为「Get API keys」双行入口

## 核心宣传点

用户设置菜单里的 Managed Agent API 条目重新设计成双行的 API Key 链接：主文案「Get API keys」，副文案「on ZooWork Platform」，前面加钥匙图标、后面加外链图标并与文字块居中对齐，一眼就能看出这是去平台拿 API Key 的入口。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary / 变更说明

Restyle the user settings menu's Managed Agent API entry as a two-line API key link: “Get API keys” with “on ZooWork Platform”. Add a leading key icon and a trailing external-link icon, centered with the text block and aligned with neighboring menu items.

将用户设置菜单中的 Managed Agent API 入口调整为两行文案：中文显示「获取 API 密钥 / 前往 ZooWork 平台」，英文显示「Get API keys / on ZooWork Platform」。左侧钥匙与右侧外链图标居中对齐，沿用现有主题颜色、Platform 地址、新标签页打开和点击关闭菜单的行为。

## Test plan / 验证

- [x] TypeScript, targeted ESLint, and repository frontend governance checks passed.
- [x] Existing UserMenu suite passed: 75 tests.
- [x] Browser-verified Chinese and English copy and light/dark appearance. Both 16px icons share the text block's vertical center.
- [x] `git diff --check` passed.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `9f28425417d8d70664bf4e0451b638a324c011e2`
- PR: #3989
- 作者：david-srp
- 日期：2026-10-01T15:08:51Z

### Commit Message

```
style(web): refine API keys menu entry / 优化 API 密钥菜单入口 (#3989)

## Summary / 变更说明

Restyle the user settings menu's Managed Agent API entry as a two-line
API key link: “Get API keys” with “on ZooWork Platform”. Add a leading
key icon and a trailing external-link icon, centered with the text block
and aligned with neighboring menu items.

将用户设置菜单中的 Managed Agent API 入口调整为两行文案：中文显示「获取 API 密钥 / 前往 ZooWork
平台」，英文显示「Get API keys / on ZooWork
Platform」。左侧钥匙与右侧外链图标居中对齐，沿用现有主题颜色、Platform 地址、新标签页打开和点击关闭菜单的行为。

## Test plan / 验证

- [x] TypeScript, targeted ESLint, and repository frontend governance
checks passed.
- [x] Existing UserMenu suite passed: 75 tests.
- [x] Browser-verified Chinese and English copy and light/dark
appearance. Both 16px icons share the text block's vertical center.
- [x] `git diff --check` passed.
```

来源：SerendipityOneInc/ecap-workspace @ 9f284254，PR #3989，作者 david-srp。
