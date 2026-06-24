---
title: "新建对话页 Agent 选择器默认折叠为两行"
type: "体验优化"
priority: "中"
date: "2026-06-23"
status: "待审核"
channels: ""
---
# 新建对话页 Agent 选择器默认折叠为两行

## 核心宣传点
新建对话时的 Agent 选择列表默认收起为两行，点开三角即可展开全部，界面更清爽。

## 原始内容
```
feat(new-chat): collapse agent selector to two rows with expand toggle (#2563)

## What

The new-chat "Choose an agent" selector previously rendered every agent
as wrapping pills, which could grow to many rows. It now **clamps to two
rows by default** and shows an inline chevron toggle at the end of row 2
to expand/collapse when there are more agents than fit.

- Collapsed (default): first two rows of agent pills + a `▾` chevron at
the end of row 2.
- Expanded: all agents + a `▴` chevron to collapse.
- No chevron when agents already fit within two rows (no behavior change
for small teams).

## How

- **`agent-selector-rows.ts`** (new, pure):
`computeCollapsedVisibleCount(rects, containerWidth, chevronWidth, gap)`
groups measured pill rects into rows and returns how many pills survive
the collapse, reserving space for the chevron at the end of row 2
(always keeps all of row 1 and ≥1 pill in row 2).
- **`AgentSelector.tsx`**: an invisible measuring layer renders every
pill at the real width; a `useIsomorphicLayoutEffect` reads each pill's
box and a `ResizeObserver` recomputes on container resize. The visible
row renders `agents.slice(0, visibleCount)` when collapsed, plus the
chevron toggle.
- Accessibility: chevron is a button with `aria-expanded`,
`aria-controls`, and "Show all agents" / "Show fewer agents" labels.

## Decisions

- A selected agent that falls in a hidden row stays hidden until expand
(the composer header still names the active agent) — chosen for
predictable ordering.
- Chevron is icon-only (no count), matching the existing pill styling.

## Testing

- `bash scripts/verify-web.sh` — tsc, vitest (31/31 incl. 6 new cases
for the row-fit math), eslint all pass.
- Verified live in-app: collapsed shows 2 rows + chevron; expanding
reveals all agents; toggling collapses again. Responsive (re-measures on
resize).
- jsdom has no real layout, so the DOM wiring is exercised by the live
app; the pure helper is unit-tested with synthetic rects (noted in the
test).
![Uploading screenshot-20260623-155624.png…]()

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR description
## What

The new-chat "Choose an agent" selector previously rendered every agent as wrapping pills, which could grow to many rows. It now **clamps to two rows by default** and shows an inline chevron toggle at the end of row 2 to expand/collapse when there are more agents than fit.

- Collapsed (default): first two rows of agent pills + a `▾` chevron at the end of row 2.
- Expanded: all agents + a `▴` chevron to collapse.
- No chevron when agents already fit within two rows (no behavior change for small teams).

## How

- **`agent-selector-rows.ts`** (new, pure): `computeCollapsedVisibleCount(rects, containerWidth, chevronWidth, gap)` groups measured pill rects into rows and returns how many pills survive the collapse, reserving space for the chevron at the end of row 2 (always keeps all of row 1 and ≥1 pill in row 2).
- **`AgentSelector.tsx`**: an invisible measuring layer renders every pill at the real width; a `useIsomorphicLayoutEffect` reads each pill's box and a `ResizeObserver` recomputes on container resize. The visible row renders `agents.slice(0, visibleCount)` when collapsed, plus the chevron toggle.
- Accessibility: chevron is a button with `aria-expanded`, `aria-controls`, and "Show all agents" / "Show fewer agents" labels.

## Decisions

- A selected agent that falls in a hidden row stays hidden until expand (the composer header still names the active agent) — chosen for predictable ordering.
- Chevron is icon-only (no count), matching the existing pill styling.

## Testing

- `bash scripts/verify-web.sh` — tsc, vitest (31/31 incl. 6 new cases for the row-fit math), eslint all pass.
- Verified live in-app: collapsed shows 2 rows + chevron; expanding reveals all agents; toggling collapses again. Responsive (re-measures on resize).
- jsdom has no real layout, so the DOM wiring is exercised by the live app; the pure helper is unit-tested with synthetic rects (noted in the test).
![Uploading screenshot-20260623-155624.png…]()

