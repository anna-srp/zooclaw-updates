---
title: "添加 IM 频道界面全面升级，Telegram 接入流程更流畅"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-21"
status: "待审核"
channels: "Discord, changelog"
---

# 添加 IM 频道界面全面升级，Telegram 接入流程更流畅

## 核心宣传点

添加 Telegram、微信等 IM 频道的界面焕新，支持 10 种语言，操作更直觉，新手也能轻松完成接入。

## 原始内容

```
feat(im-channel): 重做 Add IM Channel 弹窗 + Telegram wizard 嵌入到面板内 (#1818)

概要：整个 IM 频道添加流程的 UI 重做，包括 Telegram 引导 wizard。
- 10 个 locale 把 accountId 标签从 "Account identifier" → "Channel name"
- 新增 shadcn 组件（input/label/select）
- DM Policy / Group Policy 下拉选项跟随用户 locale 翻译
- Telegram wizard 嵌入到面板内，避免跳出

Linear: ECA-781
```
