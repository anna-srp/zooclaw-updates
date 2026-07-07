---
title: "全站玻璃面板视觉统一"
type: "体验优化"
priority: "低"
date: "2026-07-06"
status: "待审核"
channels: ""
---

# 全站玻璃面板视觉统一

## 核心宣传点

Agent Builder、日程、专家中心、设置等页面的主面板统一为一致的玻璃质感样式，界面观感更整洁统一。

## 原始内容

[7b80a131] style(app): unify glass shell panels (#2722)

## Summary
- 统一 Agent Builder、Schedule、AI Specialists
Hub、Settings/Profile、Connector 等页面的右侧全局玻璃主面板样式，内部页面背景在 glass shell
下改为透明，避免盖住全局框架。
- 替换侧边栏收起态 logo，补上 profile 入口 hover 降低透明度效果，并移除 chat 内容区额外背景层/底纹。
- 补充本地 mock 登录态自动恢复，顺带加一个很小的 Bossclaw nullable route params guard，用来解除最新
main 上的 tsc 阻塞。

## Test plan
- [x] `bash scripts/verify-web.sh ...` targeted check: 18 files / 240
tests passed, tsc and eslint passed.
- [x] Browser preview on `http://localhost:3003`: verified Agent
Builder, Schedule, AI Specialists Hub, Settings/Profile, Connector share
the same panel computed styles.
- [x] `bash scripts/verify-changed.sh`

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>

--- PR #2722 body ---
## Summary
- 统一 Agent Builder、Schedule、AI Specialists Hub、Settings/Profile、Connector 等页面的右侧全局玻璃主面板样式，内部页面背景在 glass shell 下改为透明，避免盖住全局框架。
- 替换侧边栏收起态 logo，补上 profile 入口 hover 降低透明度效果，并移除 chat 内容区额外背景层/底纹。
- 补充本地 mock 登录态自动恢复，顺带加一个很小的 Bossclaw nullable route params guard，用来解除最新 main 上的 tsc 阻塞。

## Test plan
- [x] `bash scripts/verify-web.sh ...` targeted check: 18 files / 240 tests passed, tsc and eslint passed.
- [x] Browser preview on `http://localhost:3003`: verified Agent Builder, Schedule, AI Specialists Hub, Settings/Profile, Connector share the same panel computed styles.
- [x] `bash scripts/verify-changed.sh`

