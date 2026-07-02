---
title: "BossClaw 引导页视觉与动效全面升级"
type: "体验优化"
priority: "中"
date: "2026-07-01"
status: "待审核"
channels: ""
---
# BossClaw 引导页视觉与动效全面升级
## 核心宣传点
BossClaw 的新手引导页面按最新设计参考做了像素级的视觉与动效升级（新配色、专属字体、首屏加载动画等），界面更精致统一，功能流程保持不变。
## 原始内容
feat(bossclaw): align onboarding UI & motion to zooclaw-boss reference (#2691)

## What

Pixel-level **visual + motion** alignment of the BossClaw onboarding
wizard (`web/app/src/app/[locale]/bossclaw`) to the `zooclaw-boss`
reference. **UX flow, step structure, and all backend/functional
behavior are frozen** — this is a re-skin + motion port, not a flow
change.

Spec: `docs/superpowers/specs/2026-07-01-bossclaw-ui-align.md`.

## Highlights

**Design system**
- `--boss-*` scoped token layer on `.bossclawRoot` (was fully hardcoded
hex); satisfies the no-hardcoded-color lint.
- Self-hosted **subset** Noto Serif SC / Noto Sans SC (variable wght,
~120–150KB each) + regen script `bossclaw-subset-fonts.sh` (rerun on
copy changes).
- Type scale corrected to the reference (weights/sizes were
systematically heavier/larger).

**New signature elements**
- First-load **Preloader** (gold mark pulse + progress bar + reveal,
gated on font/asset ready).
- Unified single animated **gold-dot progress** across all 6 steps
(replaced the dual brand-header + segmented-bar system).
- Screen-enter transitions, hero glow/sheen/CTA breathing + shine,
done-page draw-check + halo + live dot.
- Official **SVG wordmark** + gold app-icon claw marks (preloader / done
/ QR) + campaign **favicon** scoped to the route.

**Per-screen**
- Hero, Capabilities (reworked to the 6 canonical capabilities, grouped,
with a pinned + glowing CTA), Login/Redeem (reference single-form +
fields), WeChat bind (pod-steps checklist + QR frame + guide), Done.
- Layout fixes: hero fill-height, headline→form spacing, 28px gutter,
back-button centering, done title/subtitle.

**Preserved (frozen)**
- Real OTP login / `boss-info/bind` / `subscription-code/redeem` / agent
install / multi-channel switcher.
- `#2663` mobile scroll, `#2665` weixin-only bind guide,
`?fresh=1`/`subscription_code` URL prefill.

## Testing
- `bash scripts/verify-web.sh <bossclaw>` — **guards + tsc + 60 unit
tests + eslint all green**.
- Rendered every step at 390px and diffed against the reference
(typography, layout, motion).
- WeChat bind (pod-loader + QR) validated against **staging** backend
(mock can't drive the real install).

## Notes
- Mobile-first; the pinned bottom CTA uses `position: fixed` on mobile
(phone container body-scrolls) and an in-flow footer on desktop
(fixed-height card).
- No Linear issue (frontend re-skin of an existing campaign page).

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>

---

### PR Description

## What

Pixel-level **visual + motion** alignment of the BossClaw onboarding wizard (`web/app/src/app/[locale]/bossclaw`) to the `zooclaw-boss` reference. **UX flow, step structure, and all backend/functional behavior are frozen** — this is a re-skin + motion port, not a flow change.

Spec: `docs/superpowers/specs/2026-07-01-bossclaw-ui-align.md`.

## Highlights

**Design system**
- `--boss-*` scoped token layer on `.bossclawRoot` (was fully hardcoded hex); satisfies the no-hardcoded-color lint.
- Self-hosted **subset** Noto Serif SC / Noto Sans SC (variable wght, ~120–150KB each) + regen script `bossclaw-subset-fonts.sh` (rerun on copy changes).
- Type scale corrected to the reference (weights/sizes were systematically heavier/larger).

**New signature elements**
- First-load **Preloader** (gold mark pulse + progress bar + reveal, gated on font/asset ready).
- Unified single animated **gold-dot progress** across all 6 steps (replaced the dual brand-header + segmented-bar system).
- Screen-enter transitions, hero glow/sheen/CTA breathing + shine, done-page draw-check + halo + live dot.
- Official **SVG wordmark** + gold app-icon claw marks (preloader / done / QR) + campaign **favicon** scoped to the route.

**Per-screen**
- Hero, Capabilities (reworked to the 6 canonical capabilities, grouped, with a pinned + glowing CTA), Login/Redeem (reference single-form + fields), WeChat bind (pod-steps checklist + QR frame + guide), Done.
- Layout fixes: hero fill-height, headline→form spacing, 28px gutter, back-button centering, done title/subtitle.

**Preserved (frozen)**
- Real OTP login / `boss-info/bind` / `subscription-code/redeem` / agent install / multi-channel switcher.
- `#2663` mobile scroll, `#2665` weixin-only bind guide, `?fresh=1`/`subscription_code` URL prefill.

## Testing
- `bash scripts/verify-web.sh <bossclaw>` — **guards + tsc + 60 unit tests + eslint all green**.
- Rendered every step at 390px and diffed against the reference (typography, layout, motion).
- WeChat bind (pod-loader + QR) validated against **staging** backend (mock can't drive the real install).

## Notes
- Mobile-first; the pinned bottom CTA uses `position: fixed` on mobile (phone container body-scrolls) and an in-flow footer on desktop (fixed-height card).
- No Linear issue (frontend re-skin of an existing campaign page).

