---
title: "官网 About 页面改版：三平台并列换成一条完整的 ZooWork 故事线"
type: "体验优化"
priority: "低"
date: "2026-08-28"
status: "待审核"
channels: ""
---

# 官网 About 页面改版：三平台并列换成一条完整的 ZooWork 故事线

## 核心宣传点

About 页面的文案和排版在所有支持的语言里都重写了一遍。原来把三个平台并列展示的结构，换成了一个响应式的 ZooWork 故事版块加统一的品牌呈现，读下来是一条线而不是三个割裂的块。页面上的 CTA 行为也和营销站顶部导航的按钮对齐，桌面端和移动端、中英文都确认过没有横向溢出。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `a987d20f2f98904c7821a4cbe0d526f3b614c6a4`
- PR: #3556
- 作者: shana-srp
- 日期: 2026-08-28T02:38:49Z

### Commit Message

```
feat(marketing): refresh About page content and layout (#3556)

## Linear

N/A

## Summary
- refresh the localized About page content and typography across all
supported languages
- replace the three-platform presentation with a single responsive
ZooWork story section and brand treatment
- align the About page CTA behavior with the shared marketing header
actions
- add focused unit coverage for localized content, CTA behavior, and the
ZooWork story section

## Test plan
- [x] `bash scripts/verify-web.sh`
- [x] `bash scripts/verify-local.sh`
- [x] desktop and mobile About page visual checks in English and Chinese
- [x] verified no horizontal overflow across supported locales

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Description

```
## Linear

N/A

## Summary
- refresh the localized About page content and typography across all supported languages
- replace the three-platform presentation with a single responsive ZooWork story section and brand treatment
- align the About page CTA behavior with the shared marketing header actions
- add focused unit coverage for localized content, CTA behavior, and the ZooWork story section

## Test plan
- [x] `bash scripts/verify-web.sh`
- [x] `bash scripts/verify-local.sh`
- [x] desktop and mobile About page visual checks in English and Chinese
- [x] verified no horizontal overflow across supported locales

```
