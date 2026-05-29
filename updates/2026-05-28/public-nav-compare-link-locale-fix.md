---
title: "官网「对比 ZooClaw」链接修复，语言/主题跨页面保持一致"
type: "Bug Fix"
priority: "低"
date: "2026-05-28"
status: "待审核"
channels: ""
---

# 官网「对比 ZooClaw」链接修复，语言/主题跨页面保持一致

## 核心宣传点

官网导航中「对比 ZooClaw」现在可以正常点击，同时访问 /tips/* 页面时会自动继承当前语言和主题设置，不再出现页面闪烁或语言错乱。

## 原始内容

fix(public-nav): 官网增加入口跳转到wire Compare ZooClaw link + carry locale/theme to /tips/* (#1996)

- learnCompare entry had no href; render it as external link to /tips/compare/
- All 6 /tips/* Learn dropdown items now pass ?lang=&theme= via buildTipsHref so the sibling zooclaw-tips worker can SSR with the matching language and color scheme instead of flashing dark-default before localStorage reconciles
- Add [locale]/not-found.tsx so locale-route 404s inherit the [locale] layout html/body
