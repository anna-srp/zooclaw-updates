---
title: "修复 BossClaw 手机端扫码绑定页面无法滚动"
type: "Bug Fix"
priority: "中"
date: "2026-06-30"
status: "待审核"
channels: ""
---
# 修复 BossClaw 手机端扫码绑定页面无法滚动
## 核心宣传点
在手机（尤其是较窄的 iPhone 和微信内置浏览器）上，BossClaw 扫码绑定页较长的内容现在可以正常滚动查看，不再被截断在屏幕下方。
## 原始内容
fix(bossclaw): allow mobile QR step scrolling (#2663)

## Summary
- Fix BossClaw mobile layout so tall QR binding content can scroll
instead of being clipped.
- Add CSS regression coverage for both mobile scrollability and desktop
phone-frame height capping.

## Confirmation / Evidence
- Latest `origin/main` still has `.stage { height: 100dvh; overflow:
hidden; }` and `.phone { height: 100dvh; overflow: hidden; }`. `.screen`
only has `min-height`, so it grows with content instead of becoming the
scroll container.
- User screenshot uses a 402 x 874 iPhone 17 Pro viewport and shows the
QR step continuing below the visible bottom.
- Minimal Chrome reproduction at 402 x 874, using the same BossClaw
shell rules and QR-step content height:
- Before fix: `documentScrollHeight=874`, `phoneClientHeight=874`,
`phoneScrollHeight=1010`, `phoneOverflowY=hidden`; after wheel:
`windowScrollY=0`, `screenScrollTop=0`. This confirms content exists
below the viewport but neither page nor inner screen scrolls.
- After fix: `documentScrollHeight=1010`, `phoneOverflowY=visible`;
after wheel: `windowScrollY=136`. This confirms the same tall content
becomes reachable.

## Root cause
The BossClaw shell used fixed `100dvh` height plus `overflow: hidden` on
the outer containers. The QR step content could exceed the available
viewport height, but the `.screen` element only had `min-height`, so it
grew past the parent and was clipped instead of becoming scrollable.
This is visible on smaller/taller mobile emulations and in embedded
browsers such as WeChat.

## Test plan
- [x] `pnpm --dir web/app exec eslint
tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts --quiet`
- [x] `pnpm --dir web/app test:unit
tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts
tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx
tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx`
- [x] PR CI: `web-quality / lint-and-typecheck`, `web-quality / test`,
`web-build-check`, Codex/Claude review

---

### PR Description

## Summary
- Fix BossClaw mobile layout so tall QR binding content can scroll instead of being clipped.
- Add CSS regression coverage for both mobile scrollability and desktop phone-frame height capping.

## Confirmation / Evidence
- Latest `origin/main` still has `.stage { height: 100dvh; overflow: hidden; }` and `.phone { height: 100dvh; overflow: hidden; }`. `.screen` only has `min-height`, so it grows with content instead of becoming the scroll container.
- User screenshot uses a 402 x 874 iPhone 17 Pro viewport and shows the QR step continuing below the visible bottom.
- Minimal Chrome reproduction at 402 x 874, using the same BossClaw shell rules and QR-step content height:
  - Before fix: `documentScrollHeight=874`, `phoneClientHeight=874`, `phoneScrollHeight=1010`, `phoneOverflowY=hidden`; after wheel: `windowScrollY=0`, `screenScrollTop=0`. This confirms content exists below the viewport but neither page nor inner screen scrolls.
  - After fix: `documentScrollHeight=1010`, `phoneOverflowY=visible`; after wheel: `windowScrollY=136`. This confirms the same tall content becomes reachable.

## Root cause
The BossClaw shell used fixed `100dvh` height plus `overflow: hidden` on the outer containers. The QR step content could exceed the available viewport height, but the `.screen` element only had `min-height`, so it grew past the parent and was clipped instead of becoming scrollable. This is visible on smaller/taller mobile emulations and in embedded browsers such as WeChat.

## Test plan
- [x] `pnpm --dir web/app exec eslint tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts --quiet`
- [x] `pnpm --dir web/app test:unit tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx`
- [x] PR CI: `web-quality / lint-and-typecheck`, `web-quality / test`, `web-build-check`, Codex/Claude review
