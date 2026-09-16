---
title: "fix(landing): stabilize Safari scrolling and pause hidden demos (#3744)"
type: "Bug 修复"
priority: "中"
date: "2026-09-15"
status: "待审核"
channels: ""
---

# fix(landing): stabilize Safari scrolling and pause hidden demos (#3744)

## 核心宣传点

## Summary
- Fix homepage jumps in desktop and mobile Safari by keeping all workplace carousel panels in one stable, intrinsically sized grid row. Inactive panels are invisible, inert, and excluded from accessibility APIs.
- Pause carousel timers and repeating platform/runtime animations outside the viewport, in background tabs, and when reduced motion is enabled. Preserve manual selection, replay cadence, and keyboard controls.
- Keep the header's glass effect constant while transitioning its background and border, avoiding scroll-triggered blur interpolation.

## Root cause
The workplace carousel rendered entering and exiting panels in normal block flow. Every 2.4 seconds, their heights briefly added together and then collapsed, moving the content below them. Different final panel heights also shifted the document. Other homepage demos continued rendering off-screen, and the fixed header animated its 22px backdrop blur when scrolling started.

The shared visibility hook now requires 10% intersection, so a thin strip of section padding at the bottom of a phone viewport does not start an otherwise hidden demo.

## Test plan
- [x] Frontend governance guards, TypeScript, ESLint, and 77 focused unit tests (including off-screen/background pause, live reduced motion, viewport-edge visibility, manual cadence reset, and timer cleanup).
- [x] Playwright WebKit 26.4: desktop English, mobile English, and mobile Chinese. Automatic cycling visits all three workplace panels with **0px panel-height variation and no viewport movement**.
- [x] The same Chromium desktop/mobile and Chinese checks passed; reduced-motion checks wait for the emulated media change to propagate.
- [x] Both engines: keyboard/manual selection, hidden-panel focus exclusion, no horizontal page overflow, visible-demo updates, and zero off-screen demo DOM mutations during sampled windows.

| WebKit viewport | Before: panel height during a cycle | After |
| --- | --- | --- |
| 1440 × 900 | 637–1377px | 723px, stable |
| 390 × 844 | 750–2154px | 1259px, stable |

Browser validation used automated WebKit and Chromium on the local mock stack; physical iPhone/Safari testing has not been performed. These measurements establish layout stability and stopped off-screen work, not device FPS.

Design and validation notes: `docs/superpowers/specs/2026-09-15-safari-landing-render.md`.

The existing homepage dictionary test now supplies the browser `matchMedia` API required by the visibility hook; its copy assertions remain unchanged.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `3fa71042a69d542540cba4c479d8cf2c8598b1cc`
- PR: #3744
- 作者：shana-srp
- 日期：2026-09-15T13:00:04Z

### Commit Message

```
fix(landing): stabilize Safari scrolling and pause hidden demos (#3744)

## Summary
- Fix homepage jumps in desktop and mobile Safari by keeping all
workplace carousel panels in one stable, intrinsically sized grid row.
Inactive panels are invisible, inert, and excluded from accessibility
APIs.
- Pause carousel timers and repeating platform/runtime animations
outside the viewport, in background tabs, and when reduced motion is
enabled. Preserve manual selection, replay cadence, and keyboard
cont
```
