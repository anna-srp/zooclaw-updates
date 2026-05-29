---
title: "修复分享回放中显示错误用户头像的问题"
type: "Bug Fix"
priority: "低"
date: "2026-05-28"
status: "待审核"
channels: ""
---

# 修复分享回放中显示错误用户头像的问题

## 核心宣传点

查看他人分享的对话记录时，用户头像现在显示中性占位图标，不再错误地显示当前登录用户自己的头像。

## 原始内容

fix(web): neutral avatar placeholder for user messages in share replay (#1995)

Share replay 复用了 live chat 的 OpenClawUserMessage，其中 UserAvatar() 直接读 auth.currentUser?.photoURL + localStorage 用户信息——live chat 下 viewer == sender 刚好成立，share replay 下穿帮：登录态 viewer 看到的是自己的头像，未登录 viewer 看到的是 'U' 字母。通过 useIsReplayReadOnly() 检测 replay 模式，replay 下渲染 Heroicons UserIcon 中性占位，不再读 viewer 身份。
