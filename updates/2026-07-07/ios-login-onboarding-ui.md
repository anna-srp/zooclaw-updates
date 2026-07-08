---
title: "iOS 登录与新手引导界面焕新"
type: "体验优化"
priority: "中"
date: "2026-07-07"
status: "待审核"
channels: ""
---

# iOS 登录与新手引导界面焕新

## 核心宣传点

iOS 端全新登录弹窗与引导界面，支持邮箱、Google、Apple 三种登录方式，上手更轻松。

## 原始内容

```
feat(ios): update login and onboarding UI (#2747)

## Summary
- add the new onboarding login modal and preserve email, Google, and
Apple auth flows
- update iOS login/onboarding/settings assets and primary button color
tokens
- restore Google sign-in lookup for local staging builds and add
onboarding coverage

## Verification
- env DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
xcodebuild build -project ios/ZooClaw/ZooClaw.xcodeproj -scheme ZooClaw
-configuration Debug -destination
id=EDFB6195-BD59-4FD5-B86D-BA1A57B8C351 -derivedDataPath
build/DerivedData MARKETING_VERSION=1.8.0 build

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>

---

## PR Description

## Summary
- add the new onboarding login modal and preserve email, Google, and Apple auth flows
- update iOS login/onboarding/settings assets and primary button color tokens
- restore Google sign-in lookup for local staging builds and add onboarding coverage

## Verification
- env DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcodebuild build -project ios/ZooClaw/ZooClaw.xcodeproj -scheme ZooClaw -configuration Debug -destination id=EDFB6195-BD59-4FD5-B86D-BA1A57B8C351 -derivedDataPath build/DerivedData MARKETING_VERSION=1.8.0 build
```
