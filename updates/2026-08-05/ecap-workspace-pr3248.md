---
title: "Council 报告预览浮层与运行进度提示"
type: "体验优化"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# Council 报告预览浮层与运行进度提示

## 核心宣传点

打开报告预览不再挤压正文，改为浮层展示；运行过程中还会显示实时进度动效，清楚知道 Council 正在干活。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`7ae7cc3be843d88ac60fd65065e2d8a51b8c0873`
- 作者：bill-srp
- 日期：2026-08-05T08:16:42Z
- PR：#3248

### Commit Message

```
feat(council): report preview overlay and live run progress feedback (#3248)

## Linear
<!-- 无对应 Linear issue：会话内 UX 改进需求 -->

## Summary
- **Report preview overlays the page instead of resizing it.** The
artifacts sidebar on the council page was a flex sibling of the run
content, so opening the complete report squeezed the 900px column. It is
now an absolutely-positioned overlay anchored to the workspace root
(`relative isolate`): the page keeps full width behind it, drag-resize
still caps at 2/3 viewport, and the wrapper only mounts while a preview
is open. Chat's push-aside behavior is unchanged.
- **Live progress feedback while a run is in flight**, three layers:
- Design-system `Spinner` beside the status heading and on actively
working cast rows (`aria-hidden`, `motion-reduce:animate-none`). Hidden
while explicit approval is pending — the run is waiting on the user
then, and motion would promise progress that isn't happening.
- Claude Code-style rotating status phrases (`CouncilStatusPhrase`):
each in-flight state cycles a short phrase set every 60s with a motion
crossfade (text still rotates under reduced motion; only the transition
is dropped). Phrase sets live in `council-state.ts` with index 0 as the
canonical heading, replacing `CouncilStatus`'s private headings map so
static and animated headings cannot drift.
- Elapsed + ETA line (`CouncilStatusElapsed`): "Running for 5m ·
estimated ~12m", flipping to "longer than the ~12m estimate" on overrun.
Suffix-less backend timestamps are parsed as UTC so browser-local clocks
don't skew the elapsed label (Codex-authored fix).
- **Mock backend**: council runs now seed the `mode` field the real
backend always sends (its absence silently disabled the reports fetch
locally), and the done run's report carries a stable-host file link so
the preview flow is reachable with `dev-mock.sh`.

## Test plan
- [x] `CouncilClient.unit.spec.tsx`: preview renders inside the new
`council-artifact-overlay` wrapper and unmounts with it; live-indicator
spec asserts spinner in the status card and on the working member row
only (63 page tests green)
- [x] `CouncilStatusPhrase.unit.spec.tsx` (new): rotation at 60s,
wrap-around, state-change reset, fallback — written RED-first
- [x] `CouncilStatusElapsed.unit.spec.tsx` (new): elapsed/ETA
formatting, overrun copy, sub-minute + hour granularity, ticking,
suffix-less-UTC regression, unparseable input
- [x] `bash scripts/verify-web.sh --no-test` (guards + tsc + eslint)
green
- [x] Browser-verified via Chrome on dev-mock (overlay open/resize/close
with no page reflow; GIF captured) and on a real staging run (phrases
rotating with spinner during synthesizing)
```

### PR Body

## Linear
<!-- 无对应 Linear issue：会话内 UX 改进需求 -->

## Summary
- **Report preview overlays the page instead of resizing it.** The artifacts sidebar on the council page was a flex sibling of the run content, so opening the complete report squeezed the 900px column. It is now an absolutely-positioned overlay anchored to the workspace root (`relative isolate`): the page keeps full width behind it, drag-resize still caps at 2/3 viewport, and the wrapper only mounts while a preview is open. Chat's push-aside behavior is unchanged.
- **Live progress feedback while a run is in flight**, three layers:
  - Design-system `Spinner` beside the status heading and on actively working cast rows (`aria-hidden`, `motion-reduce:animate-none`). Hidden while explicit approval is pending — the run is waiting on the user then, and motion would promise progress that isn't happening.
  - Claude Code-style rotating status phrases (`CouncilStatusPhrase`): each in-flight state cycles a short phrase set every 60s with a motion crossfade (text still rotates under reduced motion; only the transition is dropped). Phrase sets live in `council-state.ts` with index 0 as the canonical heading, replacing `CouncilStatus`'s private headings map so static and animated headings cannot drift.
  - Elapsed + ETA line (`CouncilStatusElapsed`): "Running for 5m · estimated ~12m", flipping to "longer than the ~12m estimate" on overrun. Suffix-less backend timestamps are parsed as UTC so browser-local clocks don't skew the elapsed label (Codex-authored fix).
- **Mock backend**: council runs now seed the `mode` field the real backend always sends (its absence silently disabled the reports fetch locally), and the done run's report carries a stable-host file link so the preview flow is reachable with `dev-mock.sh`.

## Test plan
- [x] `CouncilClient.unit.spec.tsx`: preview renders inside the new `council-artifact-overlay` wrapper and unmounts with it; live-indicator spec asserts spinner in the status card and on the working member row only (63 page tests green)
- [x] `CouncilStatusPhrase.unit.spec.tsx` (new): rotation at 60s, wrap-around, state-change reset, fallback — written RED-first
- [x] `CouncilStatusElapsed.unit.spec.tsx` (new): elapsed/ETA formatting, overrun copy, sub-minute + hour granularity, ticking, suffix-less-UTC regression, unparseable input
- [x] `bash scripts/verify-web.sh --no-test` (guards + tsc + eslint) green
- [x] Browser-verified via Chrome on dev-mock (overlay open/resize/close with no page reflow; GIF captured) and on a real staging run (phrases rotating with spinner during synthesizing)

