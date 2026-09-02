---
title: "iOS App 引导流程换新：ZooWork 品牌视觉与欢迎页改版"
type: "体验优化"
priority: "中"
date: "2026-09-01"
status: "待审核"
channels: "Discord+changelog"
---

# iOS App 引导流程换新：ZooWork 品牌视觉与欢迎页改版

## 核心宣传点

iOS App 的侧边栏、启动页和引导页 Logo 全部换成新版 ZooWork 素材，欢迎页的头图背景、文案、字体、间距和按钮圆角按定稿设计重新做了一版，引导流程里出现的通知示例也从 ZooClaw 改成 ZooWork。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `2aced668de6254de8c22647f124db1aef6227dfe`
- PR: #3614
- 作者: shana-srp
- 日期: 2026-09-01T11:06:57Z

### Commit Message

```
feat(ios): refresh ZooWork onboarding branding (#3614)

## Summary

- replace the sidebar, launch, and onboarding logos with the supplied
ZooWork artwork
- refresh the welcome hero background, copy, typography, spacing, and
button radius to match the approved preview
- update onboarding notification examples from ZooClaw to ZooWork

## Testing

- `env DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
xcodebuild -project ios/ZooClaw/ZooClaw.xcodeproj -scheme ZooClaw
-configuration Debug -destination 'platform=iOS
Simulator,id=C0CBC067-D5B6-43EC-A85A-8F6542210C2E' -derivedDataPath
.build/ios-logo-update build`
- manually previewed the signed build in the iOS 26.5 simulator while
preserving the existing authenticated session

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

```
## Summary

- replace the sidebar, launch, and onboarding logos with the supplied ZooWork artwork
- refresh the welcome hero background, copy, typography, spacing, and button radius to match the approved preview
- update onboarding notification examples from ZooClaw to ZooWork

## Testing

- `env DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcodebuild -project ios/ZooClaw/ZooClaw.xcodeproj -scheme ZooClaw -configuration Debug -destination 'platform=iOS Simulator,id=C0CBC067-D5B6-43EC-A85A-8F6542210C2E' -derivedDataPath .build/ios-logo-update build`
- manually previewed the signed build in the iOS 26.5 simulator while preserving the existing authenticated session

```
