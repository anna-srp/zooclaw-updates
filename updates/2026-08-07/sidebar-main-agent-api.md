---
title: "侧边栏主助手改由接口驱动"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-07"
status: "待审核"
channels: ""
---

## 核心宣传点

侧边栏不再显示点不动的空壳助手条目，加载时有骨架占位，助手信息与后台保持一致。

## 原始内容

### feat(web): drive sidebar main agent row from agents API (#3295)

- SHA: `e4cf39a5d76e1ebd9a6bfa2807e167bac4fb2a22`
- 仓库: 见 raw/2026-08-07

**Commit Message:**

```
feat(web): drive sidebar main agent row from agents API (#3295)

# Description

The sidebar's main "Assistant" row was synthetic: `SideNavAgentList`
rendered it unconditionally with a hardcoded `agentId: 'main'` and a
hardcoded "Assistant" fallback identity — even for users whose agents
API returned no main agent, where it was a hollow shell (no
`workspace_id`, routing to bare `/chat` with no runtime behind it). Now
that #3287 provisions a real default main agent for AGENTS_V2 users
(`is_main: true` in the agents API, lazily ensured on every `GET
/agents`), the sidebar renders the main row from the API response like
every other agent row.

Design spec:
`docs/superpowers/specs/2026-08-07-sidebar-api-main-agent-design.md`
(included in this PR with the implementation plan).

## Behavior matrix

| State | Main-agent slot |
|---|---|
| Logged out / not mounted | Nothing (row is now auth-scoped) |
| Logged in, agents query initial-loading | Skeleton row
(`nav-item-chat-skeleton`, pulse, footprint-matched — no layout shift) |
| Loaded, API has a main agent | Real row, unchanged contents (same
`nav-item-chat` testid, accordion key, identity resolution) |
| Loaded, no main agent | Nothing |

## What changed

- `SideNavAgentList`: two new required props `hasMainAgent` /
`isAgentsLoading`; `mainRow` included only when present-and-loaded;
skeleton rendered during initial load only (`isLoading`, never
`isFetching` — background refetches don't flash it).
- `SideNav`: wires `hasMainAgent={mainAgent != null}` (existing
`selectMainAgentWorkspace` result) and `isAgentsLoading={isMounted &&
userLoggedIn && agentsLoading}` from `useChatEligibleAgents`.
- `lib/agent-list.ts`: deleted the dead data-level fallback
(`MAIN_FALLBACK_AGENT` + `withMainFallback` — zero production callers);
`isMainAgent`'s `agent_id === 'main'` literal stays for computer-runtime
rows and rolling deploys.

## Sequencing

#3287 (backend) is merged; this should ship in a web release **after**
the backend release reaches the environment, so the lazy-ensure closes
any "no main agent" window to a single query cycle for v2 users.

# Test Plan

- [x] New unit tests: hidden when API has no main agent (extras
unaffected), skeleton while loading, real row once loaded
(`SideNavAgentList.unit.spec.tsx`)
- [x] Pre-existing sidebar suite passes through the new required props
(`renderList` defaults)
- [x] `withMainFallback` test cases removed with the API; remaining
`agent-list` cases unchanged
- [x] Independent `bash scripts/verify-web.sh src/components/sidenav
src/lib/agent-list.ts`: guards + tsc + vitest (201 tests) + eslint all
green
- [x] Live mock-backend check (`dev-mock.sh`, ready-user scenario):
sidebar shows API-driven "Assistant" row (`is_main: true` from mock),
sessions expand, extras render, no skeleton after load — screenshot
captured locally in `.screenshots/`
- [ ] CI full unit suite + coverage (`web-quality`) — full local suite
skipped per repo policy (CI is the source of truth)
- [ ] Staging visual check after web + backend releases: fresh v2 user
sees Assistant appear from the API (no synthetic row)
```

**PR Body:**

# Description

The sidebar's main "Assistant" row was synthetic: `SideNavAgentList` rendered it unconditionally with a hardcoded `agentId: 'main'` and a hardcoded "Assistant" fallback identity — even for users whose agents API returned no main agent, where it was a hollow shell (no `workspace_id`, routing to bare `/chat` with no runtime behind it). Now that #3287 provisions a real default main agent for AGENTS_V2 users (`is_main: true` in the agents API, lazily ensured on every `GET /agents`), the sidebar renders the main row from the API response like every other agent row.

Design spec: `docs/superpowers/specs/2026-08-07-sidebar-api-main-agent-design.md` (included in this PR with the implementation plan).

## Behavior matrix

| State | Main-agent slot |
|---|---|
| Logged out / not mounted | Nothing (row is now auth-scoped) |
| Logged in, agents query initial-loading | Skeleton row (`nav-item-chat-skeleton`, pulse, footprint-matched — no layout shift) |
| Loaded, API has a main agent | Real row, unchanged contents (same `nav-item-chat` testid, accordion key, identity resolution) |
| Loaded, no main agent | Nothing |

## What changed

- `SideNavAgentList`: two new required props `hasMainAgent` / `isAgentsLoading`; `mainRow` included only when present-and-loaded; skeleton rendered during initial load only (`isLoading`, never `isFetching` — background refetches don't flash it).
- `SideNav`: wires `hasMainAgent={mainAgent != null}` (existing `selectMainAgentWorkspace` result) and `isAgentsLoading={isMounted && userLoggedIn && agentsLoading}` from `useChatEligibleAgents`.
- `lib/agent-list.ts`: deleted the dead data-level fallback (`MAIN_FALLBACK_AGENT` + `withMainFallback` — zero production callers); `isMainAgent`'s `agent_id === 'main'` literal stays for computer-runtime rows and rolling deploys.

## Sequencing

#3287 (backend) is merged; this should ship in a web release **after** the backend release reaches the environment, so the lazy-ensure closes any "no main agent" window to a single query cycle for v2 users.

# Test Plan

- [x] New unit tests: hidden when API has no main agent (extras unaffected), skeleton while loading, real row once loaded (`SideNavAgentList.unit.spec.tsx`)
- [x] Pre-existing sidebar suite passes through the new required props (`renderList` defaults)
- [x] `withMainFallback` test cases removed with the API; remaining `agent-list` cases unchanged
- [x] Independent `bash scripts/verify-web.sh src/components/sidenav src/lib/agent-list.ts`: guards + tsc + vitest (201 tests) + eslint all green
- [x] Live mock-backend check (`dev-mock.sh`, ready-user scenario): sidebar shows API-driven "Assistant" row (`is_main: true` from mock), sessions expand, extras render, no skeleton after load — screenshot captured locally in `.screenshots/`
- [ ] CI full unit suite + coverage (`web-quality`) — full local suite skipped per repo policy (CI is the source of truth)
- [ ] Staging visual check after web + backend releases: fresh v2 user sees Assistant appear from the API (no synthetic row)


