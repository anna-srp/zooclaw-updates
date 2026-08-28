---
title: "官网首页恢复到已验收的版本，动效和交互细节全部回归"
type: "体验优化"
priority: "中"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 官网首页恢复到已验收的版本，动效和交互细节全部回归

## 核心宣传点

官网首页此前合并进主干的版本和产品最终确认的版本对不上，还是用内嵌 HTML 页面的临时方案做的。现在八个板块全部改回原生组件实现并接入统一的样式体系，五屏运行阶段演示、三屏工作台、集成状态提示、Agent Builder 发布循环、ZooData 抽取动效和成果轮播这些已验收的交互细节全部回归；顶部 Logo 的比例也修正了，不再糊。当前的路由、多语言 SEO、登录埋点和后续的安全修复都原样保留。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `e1977c82b7ed84ed7d82b150c4f7385e8d44f891`
- PR: #3522
- 作者: shana-srp
- 日期: 2026-08-27T03:15:46Z

### Commit Message

```
fix(marketing): restore approved ZooWork homepage (#3522)

## Linear

N/A

## Summary

- Restore the user-approved ZooWork homepage visual baseline from
[`f4c986e`](https://github.com/SerendipityOneInc/ecap-workspace/commit/f4c986e9dbe4ae9a216c8593f89db9ec47484d30)
while keeping the current WebApp architecture.
- Render all eight homepage sections as native React components styled
through the shared Tailwind token system.
- Restore the approved interaction details: five distinct run-stage
screens, three distinct Workplace screens, integration pings, the Agent
Builder publish loop, ZooData extraction motion, and the outcomes
carousel.
- Restore the full Zenith Operations API workplace instead of the
simplified replacement, and fix the header logo's intrinsic aspect ratio
so its 1446×390 source stays sharp.
- Remove the CRM header icon, Marcelo avatar, and the two decorative
animals from the App Store QR dialog.
- Retain current `main` routing, locale/SEO handling, auth tracking,
shared marketing chrome, dependency state, and later security fixes.

## Why

PR
[#3401](https://github.com/SerendipityOneInc/ecap-workspace/pull/3401)
was merged with a final tree that does not match the user-confirmed
homepage version. The acceptance baseline is the historical commit above
and this confirmed preview:

- [Approved
preview](https://pr3401-f4c986e.zoowork-preview.pages.dev/new-chat)

This repair does not reset the repository or reuse the merged feature
branch. It forward-ports only the approved homepage visuals and behavior
onto current `main`.

## Implementation

- Remove the temporary `srcDoc`/iframe implementation, embedded HTML
document, standalone CSS, and standalone JavaScript.
- Use native React sections for Hero, role carousel, run demo, platform,
Agent Runtime, workplace, outcomes, security, and final CTA.
- Keep homepage colors in shared semantic Tailwind tokens and motion in
`motion/react`; no injected `<style>` blocks or imperative DOM animation
scripts remain.
- Preserve the approved PNG canvas background while retaining the
current WebP asset used elsewhere.
- Keep native route dictionaries and current CTA/login behavior.
- Document the migration and rollback strategy in
`docs/superpowers/specs/2026-08-26-restore-approved-zoowork-homepage.md`.

## Validation

- `bash scripts/verify-web.sh` in a non-sandbox environment:
  - governance guards passed;
  - TypeScript passed;
  - 670 test files passed;
  - 9,209 tests passed, 70 skipped, 1 todo;
  - ESLint passed.
- Focused homepage verification: 48 tests passed.
- Pre-push changed-surface verification passed.
- GitHub web quality, build, CodeQL, title, and size checks passed.
- Real route checks against the local Next.js server:
  - `/` → HTTP 200;
  - `/en` → canonical HTTP 301 redirect to `/`;
  - `/zh` → HTTP 200;
- `/new-chat` → HTTP 200 as a real application route, not a homepage
fallback.

## Visual QA

- Compared Hero, role carousel, run demo, platform/Runtime, workplace,
outcomes, security, and CTA against the approved preview section by
section.
- Confirmed every run-stage tab and Workplace tab renders its own
screen, rather than only restyling a shared frame.
- Confirmed integration, Agent Builder, ZooData, and autoplay motion
runs through native React/Motion code with reduced-motion support.
- Confirmed the preview returns the original PNG/WebP/SVG bytes for Next
image URLs; the header logo renders from its 1446×390 source at the
correct aspect ratio.
- Store Analyst / Deal Desk and other autoplay areas can show a
different dynamic frame at capture time; layout and visual treatment
remain aligned.
- Verified the CRM header icon and Marcelo avatar are absent.
- Verified the QR dialog contains only the QR code and no decorative
animals.
- Screenshots are stored locally under `.screenshots/` and are
intentionally not committed.

## Rollback

The pre-migration static version remains available at commit
`51745959543727093e018607015be252588f0a22` and remote backup branch
`codex/backup-zoowork-home-static-51745959`.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Description

```
## Linear

N/A

## Summary

- Restore the user-approved ZooWork homepage visual baseline from [`f4c986e`](https://github.com/SerendipityOneInc/ecap-workspace/commit/f4c986e9dbe4ae9a216c8593f89db9ec47484d30) while keeping the current WebApp architecture.
- Render all eight homepage sections as native React components styled through the shared Tailwind token system.
- Restore the approved interaction details: five distinct run-stage screens, three distinct Workplace screens, integration pings, the Agent Builder publish loop, ZooData extraction motion, and the outcomes carousel.
- Restore the full Zenith Operations API workplace instead of the simplified replacement, and fix the header logo's intrinsic aspect ratio so its 1446×390 source stays sharp.
- Remove the CRM header icon, Marcelo avatar, and the two decorative animals from the App Store QR dialog.
- Retain current `main` routing, locale/SEO handling, auth tracking, shared marketing chrome, dependency state, and later security fixes.

## Why

PR [#3401](https://github.com/SerendipityOneInc/ecap-workspace/pull/3401) was merged with a final tree that does not match the user-confirmed homepage version. The acceptance baseline is the historical commit above and this confirmed preview:

- [Approved preview](https://pr3401-f4c986e.zoowork-preview.pages.dev/new-chat)

This repair does not reset the repository or reuse the merged feature branch. It forward-ports only the approved homepage visuals and behavior onto current `main`.

## Implementation

- Remove the temporary `srcDoc`/iframe implementation, embedded HTML document, standalone CSS, and standalone JavaScript.
- Use native React sections for Hero, role carousel, run demo, platform, Agent Runtime, workplace, outcomes, security, and final CTA.
- Keep homepage colors in shared semantic Tailwind tokens and motion in `motion/react`; no injected `<style>` blocks or imperative DOM animation scripts remain.
- Preserve the approved PNG canvas background while retaining the current WebP asset used elsewhere.
- Keep native route dictionaries and current CTA/login behavior.
- Document the migration and rollback strategy in `docs/superpowers/specs/2026-08-26-restore-approved-zoowork-homepage.md`.

## Validation

- `bash scripts/verify-web.sh` in a non-sandbox environment:
  - governance guards passed;
  - TypeScript passed;
  - 670 test files passed;
  - 9,209 tests passed, 70 skipped, 1 todo;
  - ESLint passed.
- Focused homepage verification: 48 tests passed.
- Pre-push changed-surface verification passed.
- GitHub web quality, build, CodeQL, title, and size checks passed.
- Real route checks against the local Next.js server:
  - `/` → HTTP 200;
  - `/en` → canonical HTTP 301 redirect to `/`;
  - `/zh` → HTTP 200;
  - `/new-chat` → HTTP 200 as a real application route, not a homepage fallback.

## Visual QA

- Compared Hero, role carousel, run demo, platform/Runtime, workplace, outcomes, security, and CTA against the approved preview section by section.
- Confirmed every run-stage tab and Workplace tab renders its own screen, rather than only restyling a shared frame.
- Confirmed integration, Agent Builder, ZooData, and autoplay motion runs through native React/Motion code with reduced-motion support.
- Confirmed the preview returns the original PNG/WebP/SVG bytes for Next image URLs; the header logo renders from its 1446×390 source at the correct aspect ratio.
- Store Analyst / Deal Desk and other autoplay areas can show a different dynamic frame at capture time; layout and visual treatment remain aligned.
- Verified the CRM header icon and Marcelo avatar are absent.
- Verified the QR dialog contains only the QR code and no decorative animals.
- Screenshots are stored locally under `.screenshots/` and are intentionally not committed.

## Rollback

The pre-migration static version remains available at commit `51745959543727093e018607015be252588f0a22` and remote backup branch `codex/backup-zoowork-home-static-51745959`.

```

---
