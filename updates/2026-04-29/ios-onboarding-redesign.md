---
title: "iOS 注册引导流程全面视觉升级"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-29"
status: "待审核"
channels: "Discord, changelog"
---

# iOS 注册引导流程全面视觉升级

## 核心宣传点

iOS 端从注册到入门的完整引导流程完成视觉大改版，包含英雄页、角色选择、场景选择、注册验证等全流程新设计，新用户首次体验更流畅。

## 原始内容

**Commit:** `8001a63d` — 2026-04-29T08:33:54Z
**Repo:** ecap-workspace
**Author:** bill-srp

**Commit Message:**
```
feat(ios): Pre-auth onboarding redesign with role + use-case screens (#1458)

## Summary

**PR-A of 2** in the onboarding redesign split. Builds on the
infrastructure landed in #1452 and ships the redesigned **pre-auth**
flow: hero → name → role → use case → register.

This PR was extracted from #1450 to fit the 2000-line PR size budget.
PR-B (forthcoming) will ship the post-auth view redesigns:
EmailOTPLoginView, AgentSelectView, SetupLoadingView, and the full
OnboardingFlowView refactor.

### Pre-auth view redesigns

- **HeroView** — video background loop, Montserrat + Instrument Serif
tagline.
- **NameInputView** — editorial italic-serif underline input, panda
avatar, Continue pinned bottom.
- **RoleSelectionView** *(new)* — six-card grid; default-first with VM
rehydration on back-nav.
- **UseCaseSelectionView** *(new)* — four-card grid; same rehydration
pattern.
- **RegisterView** — simplified email-only entry with Google / Apple
SSO, inline terms/privacy.

### VM scaffolding

- New `roleSelection` / `useCaseSelection` enum cases.
- `selectedRole` / `selectedUseCase` storage (drives the rehydration on
back-nav).
- `selectedAgentIds: Set<String>` with `maxSelectedAgents = 3`.
- `goBack` table aligned with `canGoBack` (no dead branches).

### NotificationsView fix

PR #1452 deleted three onboarding notification imagesets but main's
NotificationsView still references them. This PR ships the redesigned
view (logo_black + animated cards) to restore main's visual integrity
rather than leaving it broken until PR-B.

### Compatibility shims

`AgentSelectView` and `SetupLoadingView` keep their main-version designs
but are minimally updated to consume `selectedAgentIds: Set<String>`
(replacing the dropped `selectedAgentId: String?`). Their full redesigns
ship in PR-B.

## Tests

- 28/28 OnboardingViewModelTests pass.
- New coverage: rehydration, set mutations, `maxSelectedAgents`, new
screen navigation.

## Test plan

- [ ] Onboarding pre-auth flow end-to-end: hero → name → role → use case
→ register
- [ ] Back-navigation from role/use-case restores prior selection
(rehydration)
- [ ] Notifications screen renders correctly (logo + animated cards, no
missing images)
- [ ] Agent select still works end-to-end (compat shim consuming
`selectedAgentIds.first`)
- [ ] Existing chat / agents / settings flows unchanged

## Notes

- Size: **1133 / 2000 lines** — comfortable budget, no `size-override`
needed.
- Mid-flow visual mismatch is expected on TestFlight builds between this
PR and PR-B (new pre-auth + old EmailOTP / AgentSelect / SetupLoading).
- Supersedes the corresponding portions of #1450; #1450 will be closed
or rebased once both halves land.
```

**PR #1458:** feat(ios): Pre-auth onboarding redesign with role + use-case screens

**PR Body:**
## Summary

**PR-A of 2** in the onboarding redesign split. Builds on the infrastructure landed in #1452 and ships the redesigned **pre-auth** flow: hero → name → role → use case → register.

This PR was extracted from #1450 to fit the 2000-line PR size budget. PR-B (forthcoming) will ship the post-auth view redesigns: EmailOTPLoginView, AgentSelectView, SetupLoadingView, and the full OnboardingFlowView refactor.

### Pre-auth view redesigns

- **HeroView** — video background loop, Montserrat + Instrument Serif tagline.
- **NameInputView** — editorial italic-serif underline input, panda avatar, Continue pinned bottom.
- **RoleSelectionView** *(new)* — six-card grid; default-first with VM rehydration on back-nav.
- **UseCaseSelectionView** *(new)* — four-card grid; same rehydration pattern.
- **RegisterView** — simplified email-only entry with Google / Apple SSO, inline terms/privacy.

### VM scaffolding

- New `roleSelection` / `useCaseSelection` enum cases.
- `selectedRole` / `selectedUseCase` storage (drives the rehydration on back-nav).
- `selectedAgentIds: Set<String>` with `maxSelectedAgents = 3`.
- `goBack` table aligned with `canGoBack` (no dead branches).

### NotificationsView fix

PR #1452 deleted three onboarding notification imagesets but main's NotificationsView still references them. This PR ships the redesigned view (logo_black + animated cards) to restore main's visual integrity rather than leaving it broken until PR-B.

### Compatibility shims

`AgentSelectView` and `SetupLoadingView` keep their main-version designs but are minimally updated to consume `selectedAgentIds: Set<String>` (replacing the dropped `selectedAgentId: String?`). Their full redesigns ship in PR-B.

## Tests

- 28/28 OnboardingViewModelTests pass.
- New coverage: rehydration, set mutations, `maxSelectedAgents`, new screen navigation.

## Test plan

- [ ] Onboarding pre-auth flow end-to-end: hero → name → role → use case → register
- [ ] Back-navigation from role/use-case restores prior selection (rehydration)
- [ ] Notifications screen renders correctly (logo + animated cards, no missing images)
- [ ] Agent select still works end-to-end (compat shim consuming `selectedAgentIds.first`)
- [ ] Existing chat / agents / settings flows unchanged

## Notes

- Size: **1133 / 2000 lines** — comfortable budget, no `size-override` needed.
- Mid-flow visual mismatch is expected on TestFlight builds between this PR and PR-B (new pre-auth + old EmailOTP / AgentSelect / SetupLoading).
- Supersedes the corresponding portions of #1450; #1450 will be closed or rebased once both halves land.
