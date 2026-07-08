---
title: "修复侧边栏用户指南跳转错误"
type: "Bug Fix"
priority: "中"
date: "2026-07-07"
status: "待审核"
channels: ""
---

# 修复侧边栏用户指南跳转错误

## 核心宣传点

点击侧边栏「用户指南」现在能正确跳转到帮助文档，不再出现页面报错。

## 原始内容

```
fix(app): 修复侧边栏用户指南跳转 (#2736)

## 变更内容

- 修复侧边栏「User Guide」在本地预览时误进入应用内 `/tips/...` 路径，导致 Next.js 报 `Missing
<html> and <body> tags in the root layout` 的问题。
- 增加旧 Tips 路径兼容跳转，覆盖 `/tips/en`、`/en/tips/en` 等入口。
- 保留 `lang` 和 `theme` 参数，并支持通过 `NEXT_PUBLIC_TIPS_ORIGIN` 覆盖 Tips 站点域名。

## 验证

- 本地预览：`/tips/en` 会跳转到 `https://zooclaw.ai/tips/?lang=en`
- 本地预览：`/en/tips/en` 会跳转到 `https://zooclaw.ai/tips/?lang=en`
- 本地预览：`/tips/agentstudioguide?lang=zh&theme=dark` 会跳转到
`https://zooclaw.ai/tips/agentstudioguide?lang=zh&theme=dark`
- `bash scripts/verify-web.sh ...`
- `bash scripts/verify-changed.sh`
- GitHub PR checks: 44/44 passed

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>

---

## PR Description

## 变更内容

- 修复侧边栏「User Guide」在本地预览时误进入应用内 `/tips/...` 路径，导致 Next.js 报 `Missing <html> and <body> tags in the root layout` 的问题。
- 增加旧 Tips 路径兼容跳转，覆盖 `/tips/en`、`/en/tips/en` 等入口。
- 保留 `lang` 和 `theme` 参数，并支持通过 `NEXT_PUBLIC_TIPS_ORIGIN` 覆盖 Tips 站点域名。

## 验证

- 本地预览：`/tips/en` 会跳转到 `https://zooclaw.ai/tips/?lang=en`
- 本地预览：`/en/tips/en` 会跳转到 `https://zooclaw.ai/tips/?lang=en`
- 本地预览：`/tips/agentstudioguide?lang=zh&theme=dark` 会跳转到 `https://zooclaw.ai/tips/agentstudioguide?lang=zh&theme=dark`
- `bash scripts/verify-web.sh ...`
- `bash scripts/verify-changed.sh`
- GitHub PR checks: 44/44 passed

```
