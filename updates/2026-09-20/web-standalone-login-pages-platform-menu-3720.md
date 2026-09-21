---
title: "feat(web): add standalone login pages and disabled Platform menu (#3720)"
type: "新功能"
priority: "中"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# 独立登录页上线，官网首页不再被登录状态自动带走

## 核心宣传点

公开首页现在不管你有没有登录、也不管其他标签页里登录状态怎么变，都会保持在首页，不会自动把你弹进应用里。点菜单里的 ZooWork 仍然在新标签打开 /login，已登录跳转和 Agent/Specialist 参数交接照旧。营销页的 Get Started 菜单新增独立的 ZooWork 登录入口，以及一个置灰的 API Platform 入口（暫不可点，对应的 /platform/login 页面目前只是预览）。

## 分级

- 内部：P1
- 外部：B
- 发布状态：已上线

## PR 说明

## Summary

The public homepage stays visible regardless of existing login sessions or authentication changes in another tab. Authentication no longer automatically navigates the homepage into the app. Clicking the ZooWork menu entry still opens `/login` in a new tab, where existing-session redirects and Agent/Specialist handoffs continue to work.

Marketing Get Started menus offer a standalone ZooWork login entry and a disabled API Platform entry. ZooWork opens the current-origin `/login` in a new tab and retains its existing authentication and application destination. API Platform stays greyed out without navigation; its locale-specific `/platform/login` page remains available as a presentation-only preview using the existing main-web login flow.

- Keep the standalone ZooWork login page, language handling, supported Agent/Specialist handoff parameters, and original header/hero analytics context.
- Keep the branded Platform login page, Google/email controls, shared footer, animated background, pause control and reduced-motion support.
- Keep the latest disabled-menu behavior in both marketing menus, including keyboard/mouse semantics and regression coverage.
- Keep the homepage Restaurant Operations Agent demo copy and localized accessible descriptions.
- The Platform page uses the existing `LoginForm` presentation variant, Firebase/email OTP/CAPTCHA handling, `business=ecap` identity, and current-page completion behavior. This PR does not introduce independent Platform authentication or a redirect to `platform.zoowork.ai`.

## Authentication scope

The independent Platform authentication implementation has been withdrawn through an additive, targeted rollback. Its dedicated BFF routes, named Firebase instance, session/challenge cookies, isolated client cache/layout, result tracker and deployment configuration were removed, together with the three dependent deployment-validation follow-ups. The original page/form behavior and tests were restored. The later disabled-menu change and unrelated main-branch changes remain intact; commit history was not rewritten.

No user-interface backend, deployed settings, existing production sessions or deployments were changed by this rollback. No Platform-specific runtime secret or destination configuration is required by this PR.

## Validation

- Conflict refresh (2026-09-18): merged main at `ee377fc6a5` in `26f4bb15a5`. Resolved `globals.css` by retaining standalone login tokens and the latest Agent settings styling. Kept the updated Agent Gallery URL in the automatically merged header test. All 377 relevant tests across 21 files, TypeScript, scoped ESLint, repository governance, CSS parsing and PR-diff whitespace/conflict checks passed.
- Synced main at `721a2d037a` and resolved both test conflicts, preserving grouped Solutions navigation, the canonical `/home` application destination, passive homepage behavior and explicit new-tab login. The merged result passed 437 focused tests across 18 files, TypeScript, scoped ESLint, repository governance and whitespace/conflict-marker checks.
- Homepage session behavior: 110 focused tests passed across 6 files, covering authenticated homepage visits, post-hydration/session changes, marketing chrome, new-tab menus and existing login-page redirects. Five new homepage regression cases failed against the previous automatic-redirect implementation and pass with this change.
- Homepage follow-up: TypeScript, scoped ESLint, repository governance and `git diff --check` passed.
- 414 relevant tests passed across 29 files, covering restored login/OTP behavior, Platform page wiring, ordinary auth routes, layouts, header/homepage menu behavior and analytics.
- TypeScript, scoped ESLint, repository governance and `git diff --check` passed in the isolated rollback worktree.
- Compared the restored tree with the pre-integration PR snapshot: the remaining differences are the intentionally retained disabled-menu change/documentation and unrelated main-branch feedback changes.
- Checked that removed Platform authentication/configuration identifiers and deleted-document references no longer remain in the source, tests, deployment workflow or docs.
- No real Google/email sign-in or deployed browser end-to-end login was exercised for this rollback. Cloud checks should be evaluated against the latest PR head.



## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `c0dd5d8577194ee345b7dd537b21ef8301146e14`
- PR: #3720
- 作者：shana-srp
- 日期：2026-09-20T02:45:30Z

### Commit Message

```
feat(web): add standalone login pages and disabled Platform menu (#3720)

## Summary

The public homepage stays visible regardless of existing login sessions
or authentication changes in another tab. Authentication no longer
automatically navigates the homepage into the app. Clicking the ZooWork
menu entry still opens `/login` in a new tab, where existing-session
redirects and Agent/Specialist handoffs continue to work.

Marketing Get Started menus offer a standalone ZooWork login entry and a
disabled API Platform entry. ZooWork opens the current-origin `/login`
in a new tab and retains its existing authentication and application
destination. API Platform stays greyed out without navigation; its
locale-specific `/platform/login` page remains available as a
presentation-only preview using the existing main-web login flow.

- Keep the standalone ZooWork login page, language handling, supported
Agent/Specialist handoff parameters, and original header/hero analytics
context.
- Keep the branded Platform login page, Google/email controls, shared
footer, animated background, pause control and reduced-motion support.
- Keep the latest disabled-menu behavior in both marketing menus,
including keyboard/mouse semantics and regression coverage.
- Keep the homepage Restaurant Operations Agent demo copy and localized
accessible descriptions.
- The Platform page uses the existing `LoginForm` presentation variant,
Firebase/email OTP/CAPTCHA handling, `business=ecap` identity, and
current-page completion behavior. This PR does not introduce independent
Platform authentication or a redirect to `platform.zoowork.ai`.

## Authentication scope

The independent Platform authentication implementation has been
withdrawn through an additive, targeted rollback. Its dedicated BFF
routes, named Firebase instance, session/challenge cookies, isolated
client cache/layout, result tracker and deployment configuration were
removed, together with the three dependent deployment-validation
follow-ups. The original page/form behavior and tests were restored. The
later disabled-menu change and unrelated main-branch changes remain
intact; commit history was not rewritten.

No user-interface backend, deployed settings, existing production
sessions or deployments were changed by this rollback. No
Platform-specific runtime secret or destination configuration is
required by this PR.

## Validation

- Conflict refresh (2026-09-18): merged main at `ee377fc6a5` in
`26f4bb15a5`. Resolved `globals.css` by retaining standalone login
tokens and the latest Agent settings styling. Kept the updated Agent
Gallery URL in the automatically merged header test. All 377 relevant
tests across 21 files, TypeScript, scoped ESLint, repository governance,
CSS parsing and PR-diff whitespace/conflict checks passed.
- Synced main at `721a2d037a` and resolved both test conflicts,
preserving grouped Solutions navigation, the canonical `/home`
application destination, passive homepage behavior and explicit new-tab
login. The merged result passed 437 focused tests across 18 files,
TypeScript, scoped ESLint, repository governance and
whitespace/conflict-marker checks.
- Homepage session behavior: 110 focused tests passed across 6 files,
covering authenticated homepage visits, post-hydration/session changes,
marketing chrome, new-tab menus and existing login-page redirects. Five
new homepage regression cases failed against the previous
automatic-redirect implementation and pass with this change.
- Homepage follow-up: TypeScript, scoped ESLint, repository governance
and `git diff --check` passed.
- 414 relevant tests passed across 29 files, covering restored login/OTP
behavior, Platform page wiring, ordinary auth routes, layouts,
header/homepage menu behavior and analytics.
- TypeScript, scoped ESLint, repository governance and `git diff
--check` passed in the isolated rollback worktree.
- Compared the restored tree with the pre-integration PR snapshot: the
remaining differences are the intentionally retained disabled-menu
change/documentation and unrelated main-branch feedback changes.
- Checked that removed Platform authentication/configuration identifiers
and deleted-document references no longer remain in the source, tests,
deployment workflow or docs.
- No real Google/email sign-in or deployed browser end-to-end login was
exercised for this rollback. Cloud checks should be evaluated against
the latest PR head.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
Co-authored-by: tim-srp <tim@srp.one>
```

来源：SerendipityOneInc/ecap-workspace @ c0dd5d85，PR #3720，作者 shana-srp。