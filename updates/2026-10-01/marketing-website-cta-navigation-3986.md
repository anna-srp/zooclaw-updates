---
title: "修复：官网 Talk to Sales 与产品入口跳转错乱"
type: "Bug Fix"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: ""
---

# 修复：官网 Talk to Sales 与产品入口跳转错乱

## 核心宣传点

官网 Get Started 菜单把 ZooWork.ai 改名为 Agent Builder；共用的 Talk to Sales 按钮改为在新标签页打开当前语言的 Enterprise 表单页。产品菜单、产品卡片和页脚的产品入口统一改为新开标签页，站内内容导航仍留在同页，Agent Builder 的语言与登录交接参数保持不变。官网的 iPhone / iPad 下载入口直接前往 App Store，桌面仍保留二维码。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary

- Get Started 菜单将 `ZooWork.ai` 更名为 `Agent Builder`；官网共用的 Talk to Sales 按钮在新标签页打开当前语言的 Enterprise 表单页。
- 产品菜单、卡片及页脚的产品入口统一新开标签页，站内内容导航保留同页。保留 Agent Builder 的语言与登录交接参数。
- 官网 iPhone/iPad 下载入口直接前往 App Store，桌面保留二维码；首页复用共享下载处理，移除重复弹窗包装。

Rename the menu entry to Agent Builder, route sales CTAs to localized Enterprise forms, align product links to new tabs, and send iOS visitors directly to the App Store while retaining desktop QR downloads.

## Root cause

销售按钮仍使用邮件链接；各产品入口独立决定打开方式；首页和页脚直接弹二维码，移动菜单则直链 App Store，造成同一设备操作不一致。

Sales CTAs used mail links, and separate navigation/download implementations produced inconsistent behavior across entry points.

## Test plan

- [x] Initial implementation: 136 related unit tests across 8 files, including iPhone Safari/Chrome, iPad desktop mode, non-iOS fallbacks, localized sales links, login handoffs, and product navigation.
- [x] TypeScript, changed-file ESLint, repository governance guards, and `git diff --check`.
- [x] Desktop Chrome: menu copy; all 3 homepage sales CTAs; all 4 product cards; same-tab Pricing; actual Enterprise popup and first-screen form; desktop QR dialog.
- [x] iPhone browser emulation: footer, homepage App section, mobile Products menu, and mobile download button navigate directly to the App Store in the current tab without a QR dialog. App Store requests were intercepted for URL verification; native iOS app launch was not tested on a physical device.

## Unmerged follow-up / 未包含的后续补丁

The non-iOS mobile-menu download fallback fix is committed locally as `5b1cf6237`, but is **not included in this merged PR**: GitHub rejected the push while the PR was in the merge queue, and the queue merged the original head at 2026-10-01 13:09:02 UTC as `7196eb86507a5ff714439511ed8cc8f6dbad73c4`. The local follow-up passed 50 related unit tests, TypeScript, ESLint, governance guards, and browser checks for Android/narrow-desktop QR flow and iPhone App Store handoff. A separate follow-up PR is needed. This task did not change the queue or perform the merge.

非 iOS 移动菜单下载入口修复已在本地完成验证，但未赶上队列合并；需另开后续 PR。合入的是 `05d97f3b2`，不包含本地补丁 `5b1cf6237`。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `7196eb86507a5ff714439511ed8cc8f6dbad73c4`
- PR: #3986
- 作者：david-srp
- 日期：2026-10-01T13:00:41Z

### Commit Message

```
fix(marketing): 修复官网入口 / fix website CTA navigation (#3986)

## Summary

- Get Started 菜单将 `ZooWork.ai` 更名为 `Agent Builder`；官网共用的 Talk to Sales
按钮在新标签页打开当前语言的 Enterprise 表单页。
- 产品菜单、卡片及页脚的产品入口统一新开标签页，站内内容导航保留同页。保留 Agent Builder 的语言与登录交接参数。
- 官网 iPhone/iPad 下载入口直接前往 App Store，桌面保留二维码；首页复用共享下载处理，移除重复弹窗包装。

Rename the menu entry to Agent Builder, route sales CTAs to localized
Enterprise forms, align product links to new tabs, and send iOS visitors
directly to the App Store while retaining desktop QR downloads.

## Root cause

销售按钮仍使用邮件链接；各产品入口独立决定打开方式；首页和页脚直接弹二维码，移动菜单则直链 App Store，造成同一设备操作不一致。

Sales CTAs used mail links, and separate navigation/download
implementations produced inconsistent behavior across entry points.

## Test plan

- [x] 136 related unit tests across 8 files, including iPhone
Safari/Chrome, iPad desktop mode, non-iOS fallbacks, localized sales
links, login handoffs, and product navigation.
- [x] TypeScript, changed-file ESLint, repository governance guards, and
`git diff --check`.
- [x] Desktop Chrome: menu copy; all 3 homepage sales CTAs; all 4
product cards; same-tab Pricing; actual Enterprise popup and
first-screen form; desktop QR dialog.
- [x] iPhone browser emulation: footer, homepage App section, mobile
Products menu, and mobile download button navigate directly to the App
Store in the current tab without a QR dialog. App Store requests were
intercepted for URL verification; native iOS app launch was not tested
on a physical device.
```

来源：SerendipityOneInc/ecap-workspace @ 7196eb86，PR #3986，作者 david-srp。
