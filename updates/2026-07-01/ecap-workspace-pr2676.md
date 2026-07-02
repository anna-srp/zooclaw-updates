---
title: "Agent Builder 新增引导式首页"
type: "体验优化"
priority: "中"
date: "2026-07-01"
status: "待审核"
channels: ""
---
# Agent Builder 新增引导式首页
## 核心宣传点
打开 Agent Builder 时不再直接跳进上次的项目，而是先进入引导式首页：新用户看到醒目的「创建 / 打开」入口，老用户能一键「继续上次的项目」并看到最近项目列表，找项目更方便。
## 原始内容
feat(agent-builder): add onboarding home page (#2676)

## What

`/agent-builder` now opens an onboarding-focused **home page** instead
of auto-redirecting to the last-opened project.

- **New user (empty):** prominent Create / Open buttons.
- **Returning user:** a "Continue where you left off" hero plus a
recent-projects list (status chip + updated time) with an inline "Show
all".
- **Deep link (`?prompt=`):** a card to create an agent from the pending
prompt.
- **Breadcrumb:** "Agent Builder" is now a link back to the home.

## Scope

Frontend-only — no backend / API / schema changes. Reuses the existing
`/agent-builder/projects` endpoints and the existing header action
cluster. Adds new presentational components under the `agent-builder/`
route; the only behavior changes to existing code are removing the entry
redirect and making the breadcrumb a link. Existing patterns are reused
(date formatter, button/chip/avatar styles).

## Testing

- Changes were built test-first; full `verify-web` passes locally
(project-wide `tsc` + vitest 3824 + eslint).
- `next build` is left to CI.

## Notes

- Visuals were validated against a local static demo that compiles the
real `globals.css` (this environment can't run a dev server); a preview
deploy is the final visual check.
- In the project view the breadcrumb is now a link, so that component no
longer renders an `<h1>` there.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---

### PR Description

## What

`/agent-builder` now opens an onboarding-focused **home page** instead of auto-redirecting to the last-opened project.

- **New user (empty):** prominent Create / Open buttons.
- **Returning user:** a "Continue where you left off" hero plus a recent-projects list (status chip + updated time) with an inline "Show all".
- **Deep link (`?prompt=`):** a card to create an agent from the pending prompt.
- **Breadcrumb:** "Agent Builder" is now a link back to the home.

## Scope

Frontend-only — no backend / API / schema changes. Reuses the existing `/agent-builder/projects` endpoints and the existing header action cluster. Adds new presentational components under the `agent-builder/` route; the only behavior changes to existing code are removing the entry redirect and making the breadcrumb a link. Existing patterns are reused (date formatter, button/chip/avatar styles).

## Testing

- Changes were built test-first; full `verify-web` passes locally (project-wide `tsc` + vitest 3824 + eslint).
- `next build` is left to CI.

## Notes

- Visuals were validated against a local static demo that compiles the real `globals.css` (this environment can't run a dev server); a preview deploy is the final visual check.
- In the project view the breadcrumb is now a link, so that component no longer renders an `<h1>` there.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

