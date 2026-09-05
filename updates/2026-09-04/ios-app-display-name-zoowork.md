---
title: "iOS App 名字正式改成 ZooWork"
type: "体验优化"
priority: "低"
date: "2026-09-04"
status: "待审核"
channels: "Discord+changelog"
---

# iOS App 名字正式改成 ZooWork

## 核心宣传点

品牌更名的收尾动作：iOS 应用在桌面上显示的名称在 Debug 和 Release 两套配置里都改成了 **ZooWork**，相机、麦克风、保存照片这三处系统权限申请的说明文案也同步换成了新名字——就是你第一次授权时弹窗里那句话，以前还写着旧品牌名，现在对得上了。

Bundle ID、URL scheme、entitlements 以及 Xcode 的 target / product 名称全部保持不动，所以已安装的 App 不会被当成新应用，深度链接、推送和各类集成也不受影响。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `93c3b4384470584f814ef33ed19916a8d7e31ae1`
- PR: #3652
- 作者: shana-srp
- 日期: 2026-09-04T12:02:46Z

### Commit Message

```
chore(ios): rename app display name to ZooWork (#3652)

## Summary
- Set the iOS app display name to **ZooWork** in both Debug and Release
configurations, and update the camera, microphone, and photo-saving
permission descriptions to match.
- Preserve bundle identifiers, URL schemes, entitlements, and the Xcode
target/product names so existing app identity and integrations stay
intact.

## Test plan
- [x] Validate the Xcode project and app Info.plist with `plutil -lint`.
- [x] Parse the app target's build configurations and verify both
display names are `ZooWork`, with the existing staging and production
bundle identifiers preserved.
- [x] Run `git diff --check`.
- [x] Run `bash scripts/check-pr-size.sh --base origin/main` (14 / 3000
lines).
- [x] Run `bash scripts/verify-changed.sh` (no locally verifiable
surfaces apply to this project-metadata-only change).
- [x] CI `ios-quality` passed. No local build or packaging was
performed.
- [x] Claude and Codex automatic reviews reported no findings; code
scanning reported no open alerts for this PR's merge ref.

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

```
## Summary
- Set the iOS app display name to **ZooWork** in both Debug and Release configurations, and update the camera, microphone, and photo-saving permission descriptions to match.
- Preserve bundle identifiers, URL schemes, entitlements, and the Xcode target/product names so existing app identity and integrations stay intact.

## Test plan
- [x] Validate the Xcode project and app Info.plist with `plutil -lint`.
- [x] Parse the app target's build configurations and verify both display names are `ZooWork`, with the existing staging and production bundle identifiers preserved.
- [x] Run `git diff --check`.
- [x] Run `bash scripts/check-pr-size.sh --base origin/main` (14 / 3000 lines).
- [x] Run `bash scripts/verify-changed.sh` (no locally verifiable surfaces apply to this project-metadata-only change).
- [x] CI `ios-quality` passed. No local build or packaging was performed.
- [x] Claude and Codex automatic reviews reported no findings; code scanning reported no open alerts for this PR's merge ref.

```
