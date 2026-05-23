---
title: "修复聊天中视频预览崩溃问题"
type: "Bug Fix"
priority: "中"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# 修复聊天中视频预览崩溃问题

## 核心宣传点

修复了在聊天中分享某些类型视频链接时预览区域显示异常的问题，现在会优雅处理不支持的视频格式。

## 原始内容

**Commit**: 1c5ba698a454ecd51c3d66931a2e193c544a15a5
**Author**: bill-srp
**Date**: 2026-05-22T09:37:08Z
**PR**: #1848

### Commit Message
```
fix(chat): handle unsupported video preview sources (#1848)

## Summary
- Handle unsupported or expired video sources in the chat image/video
preview modal.
- Replace native video autoplay with explicit playback handling so
NotSupportedError is caught.
- Add a video fallback state and regression test.

## Root cause
Chat video thumbnails open ImagePreview with type=video. The preview
used native video autoplay directly, so unsupported or missing media
sources could surface a browser NotSupportedError as an unhandled
production error instead of degrading to UI fallback.

Linear:
https://linear.app/srpone/issue/ECA-638/frontend-notsupportederror-media-element-has-no-supported-sources
Sentry: https://serendipity-one-inc.sentry.io/issues/7465603235/

## Test plan
- [x] pnpm test:unit tests/unit/components/ImagePreview.unit.spec.tsx
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [ ] pnpm --dir web run lint (blocked locally: ESLint fails while
loading next/core-web-vitals before file analysis: Unexpected top-level
property "name")
```

### PR Description
## Summary
- Handle unsupported or expired video sources in the chat image/video preview modal.
- Replace native video autoplay with explicit playback handling so NotSupportedError is caught.
- Add a video fallback state and regression test.

## Root cause
Chat video thumbnails open ImagePreview with type=video. The preview used native video autoplay directly, so unsupported or missing media sources could surface a browser NotSupportedError as an unhandled production error instead of degrading to UI fallback.

Linear: https://linear.app/srpone/issue/ECA-638/frontend-notsupportederror-media-element-has-no-supported-sources
Sentry: https://serendipity-one-inc.sentry.io/issues/7465603235/

## Test plan
- [x] pnpm test:unit tests/unit/components/ImagePreview.unit.spec.tsx
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [ ] pnpm --dir web run lint (blocked locally: ESLint fails while loading next/core-web-vitals before file analysis: Unexpected top-level property "name")

