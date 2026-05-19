---
title: "修复：Bot 头像每周失效问题"
type: "Bug Fix"
priority: "中"
date: "2026-05-18"
status: "待审核"
channels: ""
---
# 修复：Bot 头像每周失效问题

## 核心宣传点
修复了用户上传的 Bot 头像 7 天后自动失效（显示为空白/破损）的问题，现在头像将永久有效。

## 原始内容

**Commit**: `12dc9ba6` | ecap-workspace | 2026-05-18T10:22:56Z  
**PR**: #1725 | fix(web): persist permanent CDN URL for bot avatar uploads

---

### 根因

Bot avatar 上传走 `purpose: 'user_upload'`，该路径自 #245 起返回的是 **7 天预签名 GET URL**。该 URL 被存入 bot 的 `identity.avatar` 字段，7 天后链接过期 —— 每周一次所有用户自定义 Bot 头像失效（R2 返回 `<Code>ExpiredRequest</Code>`）。

### 修复方案

引入专用 `bot_avatar` purpose，路由到同一个 user-image bucket，但**绕过**预签名分支，改为返回永久 CDN URL（`https://uimg2.iminsp.com/bot_avatar/YYYYMMDD/{uuid}.{ext}`）。

聊天中的消息附件上传（`user_upload` / `dupe_user_upload`）保持原有 7 天签名访问行为不变。
