---
title: "修复：非 iOS 设备点手机菜单里的下载入口不再无反应"
type: "Bug Fix"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: ""
---

# 修复：非 iOS 设备点手机菜单里的下载入口不再无反应

## 核心宣传点

作为官网入口修复的后续，手机菜单里的下载 CTA 改为统一走已有的、能识别设备的下载动作。iOS 继续直接进 App Store，Android 和窄屏桌面访客则保留原来的营销页兜底，不会再出现点了没反应的情况。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary

- Follow-up to #3986: route the mobile-menu download CTA through the existing shared device-aware download action.
- iOS continues directly to the App Store. Android and narrow desktop visitors keep the marketing page and see the shared QR dialog.
- Close the navigation sheet when starting the download flow; keep labels, locale behavior, sales CTAs and other navigation unchanged.

补齐 #3986 未包含的移动下载入口修复：iOS 直达 App Store，Android 和窄屏桌面保留官网页面并显示二维码。仅复用已有处理，不改动其它导航。

## Root cause

The mobile-menu download CTA used a direct same-tab App Store link, bypassing the shared device detection. A narrow viewport is not proof of iOS, so Android and narrow desktop visitors were also navigated away. The fix was prepared during #3986 review, but the merge queue locked that branch and merged before the follow-up could be pushed.

移动菜单由屏幕宽度决定显示，原按钮却对所有设备直接跳 App Store。先前补丁因合并队列锁定未能推送，此 PR 从最新 main 单独补上。

## Test plan

- [x] Prior browser verification of the identical affected source: Android and narrow desktop retain the current page, show QR, dismiss the dialog, and reopen the menu successfully.
- [x] Prior iPhone browser emulation of the identical affected source: same-tab App Store handoff without QR or an extra tab. Apple requests intercepted for URL verification; physical-device native App Store launch remains untested.
- [x] Fresh-worktree TypeScript, governance guards, changed-file ESLint and 50 targeted unit tests.
- [ ] CI and automated review on this PR.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `b35465d0820488602de73ebf7e1a943453fbbb49`
- PR: #3987
- 作者：david-srp
- 日期：2026-10-01T15:17:34Z

### Commit Message

```
fix(marketing): 补齐移动下载入口 / preserve non-iOS download fallback (#3987)

## Summary

- Follow-up to #3986: route the mobile-menu download CTA through the
existing shared device-aware download action.
- iOS continues directly to the App Store. Android and narrow desktop
visitors keep the marketing page and see the shared QR dialog.
- Close the navigation sheet when starting the download flow; keep
labels, locale behavior, sales CTAs and other navigation unchanged.

补齐 #3986 未包含的移动下载入口修复：iOS 直达 App Store，Android
和窄屏桌面保留官网页面并显示二维码。仅复用已有处理，不改动其它导航。

## Root cause

The mobile-menu download CTA used a direct same-tab App Store link,
bypassing the shared device detection. A narrow viewport is not proof of
iOS, so Android and narrow desktop visitors were also navigated away.
The fix was prepared during #3986 review, but the merge queue locked
that branch and merged before the follow-up could be pushed.

移动菜单由屏幕宽度决定显示，原按钮却对所有设备直接跳 App Store。先前补丁因合并队列锁定未能推送，此 PR 从最新 main 单独补上。

## Test plan

- [x] Prior browser verification of the identical affected source:
Android and narrow desktop retain the current page, show QR, dismiss the
dialog, and reopen the menu successfully.
- [x] Prior iPhone browser emulation of the identical affected source:
same-tab App Store handoff without QR or an extra tab. Apple requests
intercepted for URL verification; physical-device native App Store
launch remains untested.
- [x] Fresh-worktree TypeScript, governance guards, changed-file ESLint
and 50 targeted unit tests.
- [ ] CI and automated review on this PR.
```

来源：SerendipityOneInc/ecap-workspace @ b35465d0，PR #3987，作者 david-srp。
