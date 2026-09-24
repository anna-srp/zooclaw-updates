---
title: "注册页文案、视频与排版更新：主标题改为 Deploy your expertise"
type: "体验优化"
priority: "低"
date: "2026-09-23"
status: "待审核"
channels: ""
---

# 注册页文案、视频与排版更新：主标题改为 Deploy your expertise

## 核心宣传点

注册页主标题改成「Deploy your expertise」，副标题改成「Agent delivery platform for domain experts」，并使用独立的注册文案键，登录和结账页共用的提示语不受影响（副标题按要求不带句号，是最终确认稿）。英文邮箱输入框的占位文案缩短，页面视频和字体排版一并更新。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
- Update the signup page heading to “Deploy your expertise” and subtitle to “Agent delivery platform for domain experts” using dedicated signup copy keys, preserving the shared login/checkout prompts. The subtitle intentionally has no trailing period, as explicitly requested by the user; this is the final approved copy.
- Shorten the English email placeholder to “Enter your email”.
- Replace the right-side visual with the supplied 5.63-second video and matching poster. The silent H.264 MP4 is 571 KB; the poster is 88 KB. Existing layout dimensions and playback behavior are unchanged.

- Refine heading word spacing: -0.192em for the main heading and -2.8px for the subtitle; request subtitle weight 500 (the current GFS Didot font supplies only its regular face).

## Test plan
- [x] Verify the new copy and video in the local browser; video playback reached readyState 4 with the expected 1080×1348 dimensions and 5.63-second duration.
- [x] Confirm both assets are below repository size limits.
- [x] Governance guards, TypeScript, and scoped ESLint pass on updated main.
- [x] Five relevant test files pass (96 tests): SignupVisual, LoginForm, zoowork-login-page, landing-content, and login-branding.

- [x] Browser measurements confirm heading spaces at 8.97px (56px font) and subtitle spaces at 3.55px (18px font), matching the reference spacing closely.




## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `50fb2c50c08a166ae97ec78f58077a53de75725c`
- PR: #3877
- 作者：shana-srp
- 日期：2026-09-23T08:08:08Z

### Commit Message

```
style(auth): refresh signup copy, video and typography (#3877)

## Summary
- Update the signup page heading to “Deploy your expertise” and subtitle
to “Agent delivery platform for domain experts” using dedicated signup
copy keys, preserving the shared login/checkout prompts. The subtitle
intentionally has no trailing period, as explicitly requested by the
user; this is the final approved copy.
- Shorten the English email placeholder to “Enter your email”.
- Replace the right-side visual with the supplied 5.63-second video and
matching poster. The silent H.264 MP4 is 571 KB; the poster is 88 KB.
Existing layout dimensions and playback behavior are unchanged.

- Refine heading word spacing: -0.192em for the main heading and -2.8px
for the subtitle; request subtitle weight 500 (the current GFS Didot
font supplies only its regular face).

## Test plan
- [x] Verify the new copy and video in the local browser; video playback
reached readyState 4 with the expected 1080×1348 dimensions and
5.63-second duration.
- [x] Confirm both assets are below repository size limits.
- [x] Governance guards, TypeScript, and scoped ESLint pass on updated
main.
- [x] Five relevant test files pass (96 tests): SignupVisual, LoginForm,
zoowork-login-page, landing-content, and login-branding.

- [x] Browser measurements confirm heading spaces at 8.97px (56px font)
and subtitle spaces at 3.55px (18px font), matching the reference
spacing closely.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

来源：SerendipityOneInc/ecap-workspace @ 50fb2c50，PR #3877，作者 shana-srp。