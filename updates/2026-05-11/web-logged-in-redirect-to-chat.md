---
title: "已登录用户访问首页自动跳转聊天"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-11"
status: "待审核"
channels: "Discord, changelog"
---

# 已登录用户访问首页自动跳转聊天

## 核心宣传点

登录状态下打开 ZooClaw 首页，自动直接进入聊天界面，省去多余点击。

## 原始内容

Commit message:
feat(web): auto-redirect logged-in users from landing to chat (#1589)

Logged-in users visiting the root path (/ or /zh) were shown the landing
page instead of being redirected. Now:
- Authenticated + ?redirect=/xxx → redirect to that path
- Authenticated + no params → redirect to /chat
- Unauthenticated → stay on landing, redirect after login

Extracts redirect logic into useLandingRedirect hook with open-redirect
validation and URL cleanup.

PR Description:
Logged-in users visiting the root path (/ or /zh) were shown the landing page instead of being redirected. Now:
- Authenticated + ?redirect=/xxx → redirect to that path
- Authenticated + no params → redirect to /chat
- Unauthenticated → stay on landing, redirect after login

Extracts redirect logic into useLandingRedirect hook with open-redirect validation and URL cleanup.
