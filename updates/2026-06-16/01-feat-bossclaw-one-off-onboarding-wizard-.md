---
title: "Bossclaw 一键开通向导：注册后自动装好专属智能体"
type: "新功能上线"
priority: "中"
date: "2026-06-16"
status: "待审核"
channels: ""
---
# Bossclaw 一键开通向导：注册后自动装好专属智能体
## 核心宣传点
通过手机号登录即可一步开通 Bossclaw，注册完成后系统会自动为你装好配置好的智能体，并支持兑换订阅码、绑定微信，全程引导、开箱即用。
## 原始内容
feat(bossclaw): one-off onboarding wizard with post-signup agent auto-install (#2412)

## Linear

https://linear.app/srpone/issue/ECA-983/bossclaw-one-off-onboarding-flow-with-dedicated-warm-pool

## Summary
- **V3 design — zero backend changes**: bossclaw users are plain ECAP
users on the shared warm pool; the only channel difference is the page
auto-installing a configured agent (`NEXT_PUBLIC_BOSSCLAW_AGENT_ID`)
after signup via the existing hire pipeline (`install/async` + operation
polling).
- Standalone mobile-first wizard at `app/[locale]/bossclaw`
(self-contained for one-shot removal): Firebase phone login + Turnstile
→ optional subscription-code redemption (existing
`/api/gift-code/redeem`) → WeChat-binding QR bound to the installed
agent (personal WeChat binds exactly one agent). The install runs in the
background during the subscription-code step; the WeChat step waits for
it with a retry path.
- Spec v3
(`docs/superpowers/specs/2026-06-11-bossclaw-onboarding-design.md`)
records the design evolution and the three accepted trade-offs: no
dedicated 100-bot pool (bump `WARM_POOL_TARGET_SIZE` for the campaign
window), agent installs ~30–60s after signup, trial credits granted
normally.
- Supersedes #2405 (v2 pool-segmentation approach, closed); the
companion user-interface PR #138 is closed unmerged since `role` is no
longer touched.

**Deploy config**: frontend `NEXT_PUBLIC_BOSSCLAW_AGENT_ID`; ops bumps
`WARM_POOL_TARGET_SIZE` during the campaign. Teardown = revert the env
bump + delete the `bossclaw/` directory.

## Test plan
- [x] Frontend: 7164 unit tests passed (new: install state machine +
wizard resume), `tsc --noEmit` + eslint clean
- [ ] Staging smoke: signup → agent auto-install completes → WeChat QR
binds to the agent

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Size override justification
- This PR is intentionally self-contained for the BossClaw one-off
onboarding surface: route, wizard state, login/redeem/WeChat binding UI,
agent auto-install glue, and targeted unit coverage must ship together
for staging smoke testing.
- The largest added file is the dedicated BossClaw CSS module; keeping
the styling local avoids touching shared design-system surfaces and
keeps teardown to deleting the bossclaw directory.
- Follow-up fixes in this pass add regression tests for QR rendering,
UID-scoped wizard progress, partial-login handling, and SMS OTP request
shape.

---------

Co-authored-by: Developer <dev@srp.one>

---

## PR Description

## Linear
https://linear.app/srpone/issue/ECA-983/bossclaw-one-off-onboarding-flow-with-dedicated-warm-pool

## Summary
- **V3 design — zero backend changes**: bossclaw users are plain ECAP users on the shared warm pool; the only channel difference is the page auto-installing a configured agent (`NEXT_PUBLIC_BOSSCLAW_AGENT_ID`) after signup via the existing hire pipeline (`install/async` + operation polling).
- Standalone mobile-first wizard at `app/[locale]/bossclaw` (self-contained for one-shot removal): Firebase phone login + Turnstile → optional subscription-code redemption (existing `/api/gift-code/redeem`) → WeChat-binding QR bound to the installed agent (personal WeChat binds exactly one agent). The install runs in the background during the subscription-code step; the WeChat step waits for it with a retry path.
- Spec v3 (`docs/superpowers/specs/2026-06-11-bossclaw-onboarding-design.md`) records the design evolution and the three accepted trade-offs: no dedicated 100-bot pool (bump `WARM_POOL_TARGET_SIZE` for the campaign window), agent installs ~30–60s after signup, trial credits granted normally.
- Supersedes #2405 (v2 pool-segmentation approach, closed); the companion user-interface PR #138 is closed unmerged since `role` is no longer touched.

**Deploy config**: frontend `NEXT_PUBLIC_BOSSCLAW_AGENT_ID`; ops bumps `WARM_POOL_TARGET_SIZE` during the campaign. Teardown = revert the env bump + delete the `bossclaw/` directory.

## Test plan
- [x] Frontend: 7164 unit tests passed (new: install state machine + wizard resume), `tsc --noEmit` + eslint clean
- [ ] Staging smoke: signup → agent auto-install completes → WeChat QR binds to the agent

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Size override justification
- This PR is intentionally self-contained for the BossClaw one-off onboarding surface: route, wizard state, login/redeem/WeChat binding UI, agent auto-install glue, and targeted unit coverage must ship together for staging smoke testing.
- The largest added file is the dedicated BossClaw CSS module; keeping the styling local avoids touching shared design-system surfaces and keeps teardown to deleting the bossclaw directory.
- Follow-up fixes in this pass add regression tests for QR rendering, UID-scoped wizard progress, partial-login handling, and SMS OTP request shape.
