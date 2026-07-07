---
title: "ZooClaw iOS 1.8.0 版本准备就绪"
type: "新功能上线"
priority: "中"
date: "2026-07-06"
status: "待审核"
channels: ""
---

# ZooClaw iOS 1.8.0 版本准备就绪

## 核心宣传点

iOS 新版本 1.8.0 完成开发：新增会话/子话题界面、可直接在手机上跟进话题讨论，并更新了启动引导、全新 App 图标和订阅状态展示。

## 原始内容

[3af1a6c7] feat(ios): prepare ZooClaw 1.8.0 (#2734)

## Summary

- Prepare the ZooClaw iOS 1.8.0 branch for review.
- Move iOS bot/account flows onto the current computer-scoped APIs and
remove stale wrappers.
- Add conversation session/thread UI and Mattermost thread routing.
- Refresh launch/onboarding assets, app icon, and subscription/status
handling.

## Validation

- `swiftlint`
- `xcodebuild -project ZooClaw.xcodeproj -scheme ZooClaw -destination
'platform=iOS Simulator,name=iPhone 17 Pro' build`
- `bash scripts/verify-changed.sh` returned no locally verifiable
surfaces for this iOS-only diff.
- `git merge-tree --write-tree HEAD origin/main` completed without
conflicts.

## Notes

- `xcodebuild -project ZooClaw.xcodeproj -scheme ZooClaw -destination
'platform=macOS' build` could not run locally because the current
`ZooClaw` scheme exposes no macOS destination in this checkout.

---------

Co-authored-by: shana-srp <shana@srp.one>
Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>

--- PR #2734 body ---
## Summary

- Prepare the ZooClaw iOS 1.8.0 branch for review.
- Move iOS bot/account flows onto the current computer-scoped APIs and remove stale wrappers.
- Add conversation session/thread UI and Mattermost thread routing.
- Refresh launch/onboarding assets, app icon, and subscription/status handling.

## Validation

- `swiftlint`
- `xcodebuild -project ZooClaw.xcodeproj -scheme ZooClaw -destination 'platform=iOS Simulator,name=iPhone 17 Pro' build`
- `bash scripts/verify-changed.sh` returned no locally verifiable surfaces for this iOS-only diff.
- `git merge-tree --write-tree HEAD origin/main` completed without conflicts.

## Notes

- `xcodebuild -project ZooClaw.xcodeproj -scheme ZooClaw -destination 'platform=macOS' build` could not run locally because the current `ZooClaw` scheme exposes no macOS destination in this checkout.

