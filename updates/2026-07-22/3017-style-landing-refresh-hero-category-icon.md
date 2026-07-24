---
title: 首页 Hero 分类图标焕新
type: 体验优化
priority: B
date: 2026-07-22
status: 已合并待发版
pr: 3017
author: shana-maker
url: https://github.com/SerendipityOneInc/ecap-workspace/pull/3017
---

首页 Hero 分类图标焕新

## Summary

- replace the four landing-page Hero category icons with the supplied SVG assets
- serve the icons from local static assets instead of remote URLs
- preserve the existing 24x24 rendered size and pill layout

## Testing

- `bash scripts/verify-web.sh src/app/landing/landingContent.ts` with Node.js 24
- pre-push changed-surface verification (`tsc` and ESLint)
- verified all four SVG assets return HTTP 200 in the local preview
- verified the landing page renders all four icons at 24x24 with no browser console errors

