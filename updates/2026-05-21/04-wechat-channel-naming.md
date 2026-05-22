---
title: "微信频道支持自定义名称"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-21"
status: "待审核"
channels: "Discord, changelog"
---

# 微信频道支持自定义名称

## 核心宣传点

添加微信频道时现在可以给它取个名字，方便区分多个微信账号。

## 原始内容

```
fix: allow naming WeChat channels (#1830)

- Show the account/name input for WeChat QR setup
- Pass optional WeChat account names through frontend and backend setup sessions
- Preserve the old fallback to the detected WeChat ilink account when the user leaves the default value untouched

Linear: ECA-780
```
