---
title: "iOS 客户端 Agent 市场界面全新改版"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-29"
status: "待审核"
channels: "Discord, changelog"
---

# iOS 客户端 Agent 市场界面全新改版

## 核心宣传点

iOS 上的 Agent 探索页面焕然一新，采用 Zoo Square v2 设计风格，更美观更易用；同时新增 Agent 更新提示，帮你第一时间知道有新版本可用。

## 原始内容

**Commit:** `ae86454e` — 2026-04-29T14:10:29Z
**Repo:** ecap-workspace
**Author:** bill-srp

**Commit Message:**
```
feat(ios): redesign AgentsView, add agent update flow (#1469)

## Summary

Redesigns AgentsView (the agent catalog) to match the Zoo Square v2
EXPLORE design and adds a new agent-update affordance plus a global
"agent hired" toast that survives tab switches.

### Key changes
- **EXPLORE-style row layout**: gradient background, HankenGrotesk
typography, dark navy active pill, dynamic category tabs driven by the
catalog response
- **Liquid glass menu button** (iOS 26) — fixed a latent `#if
swift(>=6.2)` gate that was preprocessing the effect out under
`SWIFT_VERSION=5.0`
- **API-driven categories**: removed the hardcoded `AgentCategory` enum;
`selectedCategory: String?` filters live against catalog `category`
values, deduped case-insensitively
- **Reusable `Toast` component** (`Views/Components/Toast.swift`) with
optional avatar/icon/emoji + action button, plus a
`.toast(item:autoDismissAfter:)` view modifier
- **Agent update flow**: when `UserAgent.has_update == true`, row shows
`plus.arrow.trianglehead.clock` + a "NEW" pill; tap calls `POST
/openclaw/agents/{id}/redeploy` (synchronous), refreshes user agents
- **Hired toast is now global** — lives on `AppShellView` (Layer 4 in
the shell ZStack) so it persists across tab switches; "Say hi" navigates
to chat
- **Hired-action simplification**: ellipsis sheet (Chat Now / Fire /
Cancel) replaced with a direct `ellipsis.message`-tap that opens chat
- **Centralized colors**: promoted `deepNavy` (#0B0F1A), `accentRed`
(#E63946), `coolTextSecondary` (#5A6478), `coolBorderLight` (#E8EBF0) to
top-level AppTheme; collapsed 5+ duplicate hex literals across
PaywallView, VoiceWaveformView, RedeemGiftCodeView, ComposeInputPanel
- **Model alignment with backend**: removed `AgentCatalogItem.isNew`
(backend never produced `is_new`); removed `UserAgent.isDefault`
(backend never produced it either; SidebarDrawerView now distinguishes
the main agent by `id == "main"`)

### Backend touchpoints (already shipped)
- `POST /openclaw/agents/{agent_id}/redeploy` — used by the new update
flow
- `GET /openclaw/agents` — `has_update` field per agent (computed in
`services/openclaw/agent_response.py`)

## Test plan
- [ ] Open AgentsView — verify EXPLORE layout, gradient background,
category tabs populated from catalog
- [ ] Liquid glass menu button visible at top-left and refracts content
beneath
- [ ] Tap `+` on an unhired agent — verify hire completes, "Hired!"
toast slides in from the top with avatar + "Say hi"
- [ ] Switch to chat tab while toast is on screen — toast persists
- [ ] Tap "Say hi" — navigates to chat with that agent
- [ ] Wait 5s without action — toast auto-dismisses
- [ ] Hire a second agent rapidly — second toast replaces the first with
a fresh 5s timer
- [ ] For an agent with `has_update == true` — NEW pill on title and
update icon on the right; tap shows spinner during redeploy and clears
`has_update` after refresh
- [ ] For a hired agent — tap `ellipsis.message` icon — opens chat
directly (no sheet)
- [ ] Filter by category — verify only matching agents show; tap "All"
pill returns full catalog
- [ ] `xcodebuild test -only-testing:ZooClawTests/AgentServiceTests
-only-testing:ZooClawTests/AgentViewModelTests` passes
- [ ] `swiftlint --strict` — 0 violations

## Notes
- 11 commits, each independently buildable. Linear history, fully
rebased on latest `main`.
- Backend has no per-agent `update` endpoint; we use the existing
`redeploy` which atomically pulls the latest catalog version.
Synchronous on the server, so iOS doesn't need polling.
- The new `Toast` component is generic — `RedeemSuccessToast` /
`ModelDegradationToast` could migrate to it in a follow-up if desired.
```

**PR #1469:** feat(ios): redesign AgentsView, add agent update flow

**PR Body:**
## Summary

Redesigns AgentsView (the agent catalog) to match the Zoo Square v2 EXPLORE design and adds a new agent-update affordance plus a global "agent hired" toast that survives tab switches.

### Key changes
- **EXPLORE-style row layout**: gradient background, HankenGrotesk typography, dark navy active pill, dynamic category tabs driven by the catalog response
- **Liquid glass menu button** (iOS 26) — fixed a latent `#if swift(>=6.2)` gate that was preprocessing the effect out under `SWIFT_VERSION=5.0`
- **API-driven categories**: removed the hardcoded `AgentCategory` enum; `selectedCategory: String?` filters live against catalog `category` values, deduped case-insensitively
- **Reusable `Toast` component** (`Views/Components/Toast.swift`) with optional avatar/icon/emoji + action button, plus a `.toast(item:autoDismissAfter:)` view modifier
- **Agent update flow**: when `UserAgent.has_update == true`, row shows `plus.arrow.trianglehead.clock` + a "NEW" pill; tap calls `POST /openclaw/agents/{id}/redeploy` (synchronous), refreshes user agents
- **Hired toast is now global** — lives on `AppShellView` (Layer 4 in the shell ZStack) so it persists across tab switches; "Say hi" navigates to chat
- **Hired-action simplification**: ellipsis sheet (Chat Now / Fire / Cancel) replaced with a direct `ellipsis.message`-tap that opens chat
- **Centralized colors**: promoted `deepNavy` (#0B0F1A), `accentRed` (#E63946), `coolTextSecondary` (#5A6478), `coolBorderLight` (#E8EBF0) to top-level AppTheme; collapsed 5+ duplicate hex literals across PaywallView, VoiceWaveformView, RedeemGiftCodeView, ComposeInputPanel
- **Model alignment with backend**: removed `AgentCatalogItem.isNew` (backend never produced `is_new`); removed `UserAgent.isDefault` (backend never produced it either; SidebarDrawerView now distinguishes the main agent by `id == "main"`)

### Backend touchpoints (already shipped)
- `POST /openclaw/agents/{agent_id}/redeploy` — used by the new update flow
- `GET /openclaw/agents` — `has_update` field per agent (computed in `services/openclaw/agent_response.py`)

## Test plan
- [ ] Open AgentsView — verify EXPLORE layout, gradient background, category tabs populated from catalog
- [ ] Liquid glass menu button visible at top-left and refracts content beneath
- [ ] Tap `+` on an unhired agent — verify hire completes, "Hired!" toast slides in from the top with avatar + "Say hi"
- [ ] Switch to chat tab while toast is on screen — toast persists
- [ ] Tap "Say hi" — navigates to chat with that agent
- [ ] Wait 5s without action — toast auto-dismisses
- [ ] Hire a second agent rapidly — second toast replaces the first with a fresh 5s timer
- [ ] For an agent with `has_update == true` — NEW pill on title and update icon on the right; tap shows spinner during redeploy and clears `has_update` after refresh
- [ ] For a hired agent — tap `ellipsis.message` icon — opens chat directly (no sheet)
- [ ] Filter by category — verify only matching agents show; tap "All" pill returns full catalog
- [ ] `xcodebuild test -only-testing:ZooClawTests/AgentServiceTests -only-testing:ZooClawTests/AgentViewModelTests` passes
- [ ] `swiftlint --strict` — 0 violations

## Notes
- 11 commits, each independently buildable. Linear history, fully rebased on latest `main`.
- Backend has no per-agent `update` endpoint; we use the existing `redeploy` which atomically pulls the latest catalog version. Synchronous on the server, so iOS doesn't need polling.
- The new `Toast` component is generic — `RedeemSuccessToast` / `ModelDegradationToast` could migrate to it in a follow-up if desired.
