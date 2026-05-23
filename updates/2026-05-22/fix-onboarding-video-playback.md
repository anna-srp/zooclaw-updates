---
title: "修复新功能介绍视频播放失败问题"
type: "Bug Fix"
priority: "低"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# 修复新功能介绍视频播放失败问题

## 核心宣传点

修复了 App 内功能介绍视频无法正常播放的问题，现在新功能上线时的引导视频能正常显示。

## 原始内容

**Commit**: 5acb93feaa6d65a296116bcc007cd4a0f67a0e92
**Author**: bill-srp
**Date**: 2026-05-22T10:07:27Z
**PR**: #1850

### Commit Message
```
fix(onboarding): handle feature launch video playback errors (#1850)

## Summary
- Catch rejected feature-launch video playback attempts.
- Keep the modal play state accurate when the browser cannot play the
video.
- Add unit coverage for rejected media playback.

## Root cause
FeatureLaunchModal set its local playing state to true immediately after
calling video.play(). If the browser rejected playback, for example with
NotSupportedError, the promise rejection was not handled and the UI
could remain in the wrong state.

## Test plan
- [x] pnpm --dir web/app run test:unit
tests/unit/components/FeatureLaunchModal.unit.spec.tsx
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [ ] pnpm --dir web run lint (blocked locally: ESLint fails while
loading next/core-web-vitals before file analysis: Unexpected top-level
property "name")
```

### PR Description
## Summary
- Catch rejected feature-launch video playback attempts.
- Keep the modal play state accurate when the browser cannot play the video.
- Add unit coverage for rejected media playback.

## Root cause
FeatureLaunchModal set its local playing state to true immediately after calling video.play(). If the browser rejected playback, for example with NotSupportedError, the promise rejection was not handled and the UI could remain in the wrong state.

## Test plan
- [x] pnpm --dir web/app run test:unit tests/unit/components/FeatureLaunchModal.unit.spec.tsx
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [ ] pnpm --dir web run lint (blocked locally: ESLint fails while loading next/core-web-vitals before file analysis: Unexpected top-level property "name")

