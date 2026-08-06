---
title: "修复 Agent 卡片误跳转与聊天入口空白"
type: "Bug Fix"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# 修复 Agent 卡片误跳转与聊天入口空白

## 核心宣传点

解雇 Agent 时不会再误跳详情页；装好 Agent 后点 Start Chat 直接进入新任务页，不再落到空白会话。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`60aee159390d8031d9c0273412e4d0221a81c92b`
- 作者：bill-srp
- 日期：2026-08-05T05:59:26Z
- PR：#3244

### Commit Message

```
fix(web): agents-manager fire click propagation and start-chat routing (#3244)

## Summary
Two agents-manager fixes:
1. **Fire menu click no longer triggers the card click.** Firing an
agent opened the confirm-fire modal *and* navigated to
`/agents-manager/{packId}` at the same time. Fixed with
`onClick={(event) => event.stopPropagation()}` on the card dropdown's
`DropdownMenuContent`.
2. **Start Chat CTAs now route to the New Task launcher.** After
installing an agent, Start Chat (hire-success modal, card Chat button,
detail page, publish flow, post-update session reset) landed on
`/chat?workspace_id=` — the workspace's "Session History" DM, which is
empty for a fresh install and is exactly the surface the sidenav hides
as a "navigation dead end" for session-less agents
(`SideNavAgentSessions.tsx`). All of these now go through
`buildWorkspaceNewChatHref` (`/new-chat?workspace_id=`), landing on the
New Task launcher pre-selected with the agent.

## Root cause
**Fix 1:** The whole agent card is a `LocaleLink` (Next.js `<Link>`),
and the Fire action is a Radix `DropdownMenuItem` nested inside it. The
existing `event.preventDefault()` in `onSelect` only cancels Radix's
menu auto-close — it does nothing to the underlying click. Although
`DropdownMenuContent` renders in a portal (native DOM bubbling never
reaches the anchor), **React synthetic events bubble through the JSX
tree, not the DOM tree**: the item click propagated up to the Link's
navigation `onClick` and Next.js client-navigated. The fix deliberately
uses `stopPropagation()` only, **without** `preventDefault()`: Radix
dispatches the item's select event from a composed click handler that
bails when `defaultPrevented` is set, so preventing default at the
content level would suppress `onSelect` and make Fire a no-op.

**Fix 2:** `openChat`/`pushWorkspaceChat` used `buildWorkspaceChatHref`,
which targets the engine agent's Mattermost DM surface ("Session
History"). For a freshly installed agent that surface has zero sessions;
the sidenav model already treats it as a dead end and offers "New Task"
instead. Per owner decision (New Task everywhere), all agents-manager
start-chat entry points now route to the launcher regardless of runtime.

## Test plan
- [x] Fix 1 regression test: `fire menu click requests fire without
bubbling to the card link` — mocked `LocaleLink` carries a click spy
standing in for Next Link's navigation handler; failed before the fix
(spy called), passes after, and asserts `onRequestFire` still fires
- [x] Fix 2: flipped all 15 destination assertions across the 4
agents-manager specs from `/chat?workspace_id=` to
`/new-chat?workspace_id=` first (RED: exactly those 15 failed), then
switched the 4 call sites (GREEN: 176/176)
- [x] `bash scripts/verify-web.sh` on changed files: guards + `tsc` +
`vitest` + `eslint` all green
- [x] Browser-validated against the mock stack (`scripts/dev-mock.sh`,
install handlers mutate real state): install → hire-success "Start Chat"
lands on `/new-chat?workspace_id=workspace_mock_4`; hired card "Chat"
lands on `/new-chat?workspace_id=workspace_mock_1` with the New Task
composer pre-selected to the agent; no stray card navigation
```

### PR Body

## Summary
Two agents-manager fixes:
1. **Fire menu click no longer triggers the card click.** Firing an agent opened the confirm-fire modal *and* navigated to `/agents-manager/{packId}` at the same time. Fixed with `onClick={(event) => event.stopPropagation()}` on the card dropdown's `DropdownMenuContent`.
2. **Start Chat CTAs now route to the New Task launcher.** After installing an agent, Start Chat (hire-success modal, card Chat button, detail page, publish flow, post-update session reset) landed on `/chat?workspace_id=` — the workspace's "Session History" DM, which is empty for a fresh install and is exactly the surface the sidenav hides as a "navigation dead end" for session-less agents (`SideNavAgentSessions.tsx`). All of these now go through `buildWorkspaceNewChatHref` (`/new-chat?workspace_id=`), landing on the New Task launcher pre-selected with the agent.

## Root cause
**Fix 1:** The whole agent card is a `LocaleLink` (Next.js `<Link>`), and the Fire action is a Radix `DropdownMenuItem` nested inside it. The existing `event.preventDefault()` in `onSelect` only cancels Radix's menu auto-close — it does nothing to the underlying click. Although `DropdownMenuContent` renders in a portal (native DOM bubbling never reaches the anchor), **React synthetic events bubble through the JSX tree, not the DOM tree**: the item click propagated up to the Link's navigation `onClick` and Next.js client-navigated. The fix deliberately uses `stopPropagation()` only, **without** `preventDefault()`: Radix dispatches the item's select event from a composed click handler that bails when `defaultPrevented` is set, so preventing default at the content level would suppress `onSelect` and make Fire a no-op.

**Fix 2:** `openChat`/`pushWorkspaceChat` used `buildWorkspaceChatHref`, which targets the engine agent's Mattermost DM surface ("Session History"). For a freshly installed agent that surface has zero sessions; the sidenav model already treats it as a dead end and offers "New Task" instead. Per owner decision (New Task everywhere), all agents-manager start-chat entry points now route to the launcher regardless of runtime.

## Test plan
- [x] Fix 1 regression test: `fire menu click requests fire without bubbling to the card link` — mocked `LocaleLink` carries a click spy standing in for Next Link's navigation handler; failed before the fix (spy called), passes after, and asserts `onRequestFire` still fires
- [x] Fix 2: flipped all 15 destination assertions across the 4 agents-manager specs from `/chat?workspace_id=` to `/new-chat?workspace_id=` first (RED: exactly those 15 failed), then switched the 4 call sites (GREEN: 176/176)
- [x] `bash scripts/verify-web.sh` on changed files: guards + `tsc` + `vitest` + `eslint` all green
- [x] Browser-validated against the mock stack (`scripts/dev-mock.sh`, install handlers mutate real state): install → hire-success "Start Chat" lands on `/new-chat?workspace_id=workspace_mock_4`; hired card "Chat" lands on `/new-chat?workspace_id=workspace_mock_1` with the New Task composer pre-selected to the agent; no stray card navigation

