---
title: "首页展示视频：用自动播放演示替代静态截图"
type: "产品基础功能更新"
priority: "低"
date: "2026-04-25"
status: "待审核"
channels: "Discord + changelog"
---

# 首页展示视频：用自动播放演示替代静态截图

## 核心宣传点

首页英雄区域已换成自动播放的产品演示视频，更直观地展示 ZooClaw 能做什么。

## 原始内容

Commit: 29fcffd7a883d3038d56e752804b552726a81767

Message:
feat(web): replace landing hero screenshot with autoplay demo video (#1276)

## Summary
- Replace the static hero product screenshot (`<img>`) with a
muted-autoplay `<video>` (720p, 13.7 MB, hosted on Cloudflare R2),
paired with a circular click-to-unmute button overlay in the
bottom-right corner of the video
- Inline SVG icons (speaker-mute / speaker-on) toggled via `useState`,
consistent with the existing inline-SVG convention in `LandingSecurity`
/ `LandingSpecialists`
- Header now collapses to its pill form on any scroll (threshold 10 px)
instead of only after the user has scrolled past the entire hero section
— matches the scroll-sticky behavior common on Apple / Stripe / Linear
landing pages

## Why
The previous hero image was a static screenshot; a demo video conveys
the product's "proactive AI team" pitch far more effectively. The header
collapse delay was unintuitive — users scrolling even a small amount
expected the sticky pill immediately.

## Test plan
- [x] Verified in Playwright: `autoPlay + muted` triggers autoplay;
click toggles `muted` state and swaps SVG icon
- [x] Verified header transitions: `scrollY <= 10` → full-width bar;
`scrollY > 10` → 920 px pill with `border-radius: 999px`; returns on
scroll back to 0
- [x] Mobile responsive tweaks: mute button shrinks to 40 px at `<768px`
viewport
- [x] A11y: `aria-label` on video + button, `aria-pressed` reflects mute
state, keyboard-focusable via `:focus-visible` outline
- [ ] Sanity-check on real iOS Safari (inline playback + click gesture
unlock)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
2. 官网视频替换，
- 强压缩；3:18 全长，720p，CRF 28 + 保留音轨；~20-30MB；
默认静音自动播放，用户点一下才开声音（行业惯例，Apple/Stripe 都这么做）
- 并修复顶bar显示bug，只要鼠标滚动就缩起
<img width="1280" height="383" alt="image"
src="https://github.com/user-attachments/assets/7c4a4777-d8b7-4c1b-b4a1-a714213cf7de"
/>

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

PR Description:
## Summary
- Replace the static hero product screenshot (`<img>`) with a muted-autoplay `<video>` (720p, 13.7 MB, hosted on Cloudflare R2), paired with a circular click-to-unmute button overlay in the bottom-right corner of the video
- Inline SVG icons (speaker-mute / speaker-on) toggled via `useState`, consistent with the existing inline-SVG convention in `LandingSecurity` / `LandingSpecialists`
- Header now collapses to its pill form on any scroll (threshold 10 px) instead of only after the user has scrolled past the entire hero section — matches the scroll-sticky behavior common on Apple / Stripe / Linear landing pages

## Why
The previous hero image was a static screenshot; a demo video conveys the product's "proactive AI team" pitch far more effectively. The header collapse delay was unintuitive — users scrolling even a small amount expected the sticky pill immediately.

## Test plan
- [x] Verified in Playwright: `autoPlay + muted` triggers autoplay; click toggles `muted` state and swaps SVG icon
- [x] Verified header transitions: `scrollY <= 10` → full-width bar; `scrollY > 10` → 920 px pill with `border-radius: 999px`; returns on scroll back to 0
- [x] Mobile responsive tweaks: mute button shrinks to 40 px at `<768px` viewport
- [x] A11y: `aria-label` on video + button, `aria-pressed` reflects mute state, keyboard-focusable via `:focus-visible` outline
- [ ] Sanity-check on real iOS Safari (inline playback + click gesture unlock)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
2. 官网视频替换，
- 强压缩；3:18 全长，720p，CRF 28 + 保留音轨；~20-30MB； 默认静音自动播放，用户点一下才开声音（行业惯例，Apple/Stripe 都这么做）
- 并修复顶bar显示bug，只要鼠标滚动就缩起
<img width="1280" height="383" alt="image" src="https://github.com/user-attachments/assets/7c4a4777-d8b7-4c1b-b4a1-a714213cf7de" />

