---
title: 首页 SSR 与多语言 SEO 优化
type: Bug Fix
priority: B
date: 2026-07-22
status: 已合并待发版
pr: 2962
author: Mori-srp
url: https://github.com/SerendipityOneInc/ecap-workspace/pull/2962
---

首页 SSR 与多语言 SEO 优化

## Summary

- keep the redesigned anonymous homepage's H1, hero description, core navigation, and main content in the initial HTML by isolating `usePageTracking` behind a leaf-level Suspense boundary
- scope homepage title, description, canonical, Open Graph, and Twitter metadata to the homepage route, while keeping shared root fallbacks brand-safe for ZooClaw and Gensmo builds
- expose stable multilingual homepage URLs: English uses `/`; Chinese, Japanese, Korean, French, German, Italian, Spanish, Arabic, and Portuguese use `/{locale}`
- emit a self-canonical and matching Open Graph URL per h
