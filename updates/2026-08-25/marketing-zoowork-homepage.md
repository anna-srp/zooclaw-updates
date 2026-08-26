---
title: "全新 ZooWork 官网首页上线，支持 10 种语言（含阿拉伯语从右至左排版）"
type: "新功能上线"
priority: "中"
date: "2026-08-25"
status: "待审核"
channels: ""
---

# 全新 ZooWork 官网首页上线，支持 10 种语言（含阿拉伯语从右至左排版）

## 核心宣传点

官网首页整体换新为 ZooWork 品牌形象，八个板块完整呈现产品能力，其中包含重新设计的「Agent 运行时六大能力」和「安全边界六原则」两块内容。首页、顶部导航、页脚、品牌素材和 App 下载弹窗全部完成 10 种语言本地化，阿拉伯语按从右至左正确排版。Get Started 仍然直连原有登录流程，Talk to Sales 会直接打开写好收件人的邮件。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `f392cde8dee9f30e454374464a144c1b86b9ab3b`
- PR: #3401
- 作者: shana-srp
- 日期: 2026-08-25T02:57:33Z

### Commit Message

```
feat(marketing): launch localized ZooWork homepage (#3401)

## Linear

N/A

## Summary

- Replace the public homepage body with the new ZooWork marketing
experience.
- Render the supplied eight-section experience in isolated, same-origin
auto-height frames so its CSS and JavaScript cannot leak into the shared
Next.js marketing chrome.
- Merge the approved Runtime and Security redesign from
`zoowork-official-demo#1`: a six-capability Agent Runtime grid and a
six-principle security-boundary model.
- Refresh the shared header, footer, brand assets, and App Store dialog
while preserving the existing authentication behavior.
- Localize the homepage, shared chrome, App Store dialog, metadata, and
refreshed Runtime/Security content across all 10 supported locales,
including RTL document direction for Arabic.
- Keep Get Started connected to the existing login flow and route Talk
to Sales to a pre-addressed system email.
- Add focused unit coverage for the embedded homepage, translations,
metadata, shared marketing chrome, brand assets, and App Store
interactions.
- Features, Contact, and Pricing page changes were extracted to #3429,
#3430, and #3431 respectively.

## Test plan

- [x] `bash scripts/verify-web.sh`
- [x] TypeScript passed.
- [x] 656 test files passed (8,872 tests passed; 70 skipped; 1 todo).
- [x] ESLint passed.
- [x] Verified all 10 supported locales and complete runtime homepage
translations: 368/368 keys per translated bundle.
- [x] Browser-smoke-tested the homepage and English-to-Chinese locale
switch, including shared chrome and embedded section content.
- [x] Verified Arabic RTL handling, localized iframe metadata, dynamic
demo copy, and App Store dialog copy.

## Notes

- This PR intentionally exceeds the normal line budget because it
vendors the approved static homepage experience and complete homepage
translation bundles; the PR already carries the required size override
handling.
- The separately scoped Features, Contact, and Pricing work is tracked
in #3429, #3430, and #3431.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
Co-authored-by: bill-srp <bill@srp.one>
```

### PR Description

```
## Linear

N/A

## Summary

- Replace the public homepage body with the new ZooWork marketing experience.
- Render the supplied eight-section experience in isolated, same-origin auto-height frames so its CSS and JavaScript cannot leak into the shared Next.js marketing chrome.
- Merge the approved Runtime and Security redesign from `zoowork-official-demo#1`: a six-capability Agent Runtime grid and a six-principle security-boundary model.
- Refresh the shared header, footer, brand assets, and App Store dialog while preserving the existing authentication behavior.
- Localize the homepage, shared chrome, App Store dialog, metadata, and refreshed Runtime/Security content across all 10 supported locales, including RTL document direction for Arabic.
- Keep Get Started connected to the existing login flow and route Talk to Sales to a pre-addressed system email.
- Add focused unit coverage for the embedded homepage, translations, metadata, shared marketing chrome, brand assets, and App Store interactions.
- Features, Contact, and Pricing page changes were extracted to #3429, #3430, and #3431 respectively.

## Test plan

- [x] `bash scripts/verify-web.sh`
- [x] TypeScript passed.
- [x] 656 test files passed (8,872 tests passed; 70 skipped; 1 todo).
- [x] ESLint passed.
- [x] Verified all 10 supported locales and complete runtime homepage translations: 368/368 keys per translated bundle.
- [x] Browser-smoke-tested the homepage and English-to-Chinese locale switch, including shared chrome and embedded section content.
- [x] Verified Arabic RTL handling, localized iframe metadata, dynamic demo copy, and App Store dialog copy.

## Notes

- This PR intentionally exceeds the normal line budget because it vendors the approved static homepage experience and complete homepage translation bundles; the PR already carries the required size override handling.
- The separately scoped Features, Contact, and Pricing work is tracked in #3429, #3430, and #3431.

```
