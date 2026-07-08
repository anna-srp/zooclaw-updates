---
title: "iOS 端修复聊天消息列表解析失败问题"
type: "Bug Fix"
priority: "中"
date: "2026-07-07"
status: "待审核"
channels: ""
---

# iOS 端修复聊天消息列表解析失败问题

## 核心宣传点

iOS 端聊天消息列表在遇到复杂消息数据时不再解析失败，消息展示更稳定。

## 原始内容

```
fix(ios): decode mixed Mattermost post props (#2760)

## Summary

- Change iOS Mattermost post props decoding from string-only to
heterogeneous JSON values.
- Add a regression test covering numeric, boolean, nested, array, and
null props in Mattermost post lists.

## Verification

- `swiftlint lint ZooClaw/Models/Mattermost/MattermostModels.swift
ZooClawTests/MattermostModelsTests.swift`
- `xcodebuild build-for-testing -project ZooClaw.xcodeproj -scheme
ZooClaw -destination 'generic/platform=iOS Simulator'
-parallel-testing-enabled NO
-maximum-concurrent-test-simulator-destinations 1
-only-testing:ZooClawTests/MattermostModelsTests/postListDecodesMixedProps`

Note: I could not run the XCTest itself locally because this machine has
no matching concrete iOS Simulator device; generic simulator
build-for-testing succeeded.

---

## PR Description

## Summary

- Change iOS Mattermost post props decoding from string-only to heterogeneous JSON values.
- Add a regression test covering numeric, boolean, nested, array, and null props in Mattermost post lists.

## Verification

- `swiftlint lint ZooClaw/Models/Mattermost/MattermostModels.swift ZooClawTests/MattermostModelsTests.swift`
- `xcodebuild build-for-testing -project ZooClaw.xcodeproj -scheme ZooClaw -destination 'generic/platform=iOS Simulator' -parallel-testing-enabled NO -maximum-concurrent-test-simulator-destinations 1 -only-testing:ZooClawTests/MattermostModelsTests/postListDecodesMixedProps`

Note: I could not run the XCTest itself locally because this machine has no matching concrete iOS Simulator device; generic simulator build-for-testing succeeded.

```
