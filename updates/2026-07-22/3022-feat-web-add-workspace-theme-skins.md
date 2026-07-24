---
title: 工作区支持主题皮肤（赤陶暖笺 / 靛蓝专注 浅色皮肤）
type: 新功能
priority: A
date: 2026-07-22
status: 已合并待发版
pr: 3022
author: shana-maker
url: https://github.com/SerendipityOneInc/ecap-workspace/pull/3022
---

工作区支持主题皮肤（赤陶暖笺 / 靛蓝专注 浅色皮肤）

## Summary

- add the light-mode `Terracotta Note / 赤陶暖笺` and `Indigo Focus / 靛蓝专注` workspace skins, with persistence and toggle-back to the original UI
- extend semantic skin styling across navigation, settings, new chat, active chat/composer, AI Specialists Hub, and Schedule
- keep dark/system appearance independent by disabling skin selection outside light mode
- improve local mock preview support, agent avatars, WebSocket handshake, and hire-button behavior

## Validation

- `bash scripts/verify-changed.sh`
- focused web validation: 37 test files / 692 tests passed, TypeScript and ESLint p
