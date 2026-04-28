---
title: "iOS 聊天界面点击和流式卡顿问题修复"
type: "Bug Fix"
priority: "高"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# iOS 聊天界面点击和流式卡顿问题修复

## 核心宣传点
修复了 iOS 用户在聊天中无法点击链接、图片、视频和文件卡片的 Bug，以及流式回复时 App 偶尔卡死的问题，聊天体验更流畅。

## 原始内容
**Commit**: fix(ios): Fix chat tap gestures and streaming app hang (#1370)  
**PR Body**:  
三个 iOS 聊天视图修复：  
1. 解除点击手势拦截（ScrollView 上的 .onTapGesture 独占手势拦截了链接/图片/视频/文件卡片的点击，改为 .simultaneousGesture(TapGesture())）  
2. 修复 bubble overlay 吸收所有点击的问题（Color.clear.contentShape(Rectangle()) 是点击测试赢家，吸收了整个 bubble 区域的点击，改用 GeometryReader + PreferenceKey + .simultaneousGesture）  
3. 修复 streaming 期间 app 卡死（可能由主线程操作引起）
