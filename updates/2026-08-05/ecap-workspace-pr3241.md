---
title: "新版运行时用户也能自动安装行业套装"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# 新版运行时用户也能自动安装行业套装

## 核心宣传点

使用新版引擎、没有独立电脑的用户，现在也能在引导流程中自动装好行业套装里的 Agent，开箱即用。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`aa0294a8bf722265e57c99ad2bba2b8b64c6a61d`
- 作者：bill-srp
- 日期：2026-08-05T03:09:24Z
- PR：#3241

### Commit Message

```
feat(web): run the vertical-pack installer for engine-mode users (#3241)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- spec-driven:
docs/superpowers/specs/2026-08-04-v2-onboarding-engine-install.md, Phase
4 (frontend leg) -->

## Summary
Frontend leg of Phase 4 (backend = #3235, merged): the vertical-pack
package auto-installer works for engine-mode users with no computer.

- `VerticalPackPackageInstaller`: enables on v1 init readiness **or**
engine mode (uid-scoped `botStatus === 'engine'` from the onboarding
store — the Phase 2 signal).
- `useVerticalPackPackageInstaller` engine branch: computer
lookup/status queries fully disabled; package query enables without a
computer; once-per-session install key scoped to `'engine'`; pre-install
dedup reads the unified agent list across **all runtimes** (mirroring
the backend's cross-runtime dedup); and because #3235 installs + starts
engine agents inline, the engine path skips the 5-minute
`waitForAgentWorkspaceStatus` polling entirely — it just invalidates the
agent cache when the install call returns.
- v1 computer path byte-for-byte unchanged (resolution refactored into a
pure helper, same semantics, existing tests still pass).

## Test plan
- [x] TDD (RED first): engine-mode user with no computer → package
fetched, missing packs installed, no computer queries, cache
invalidated, no polling; cross-runtime dedup skips engine-held packs;
uid-scoped component enablement; v1 path unchanged (15 targeted tests
green)
- [x] Full local gate `bash scripts/verify-web.sh`: guards + tsc +
vitest + eslint — green
- [x] `pnpm lint:imports`: 0 errors
- [ ] CI (`web-quality` + `web-build-check`)
```

### PR Body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- spec-driven: docs/superpowers/specs/2026-08-04-v2-onboarding-engine-install.md, Phase 4 (frontend leg) -->

## Summary
Frontend leg of Phase 4 (backend = #3235, merged): the vertical-pack package auto-installer works for engine-mode users with no computer.

- `VerticalPackPackageInstaller`: enables on v1 init readiness **or** engine mode (uid-scoped `botStatus === 'engine'` from the onboarding store — the Phase 2 signal).
- `useVerticalPackPackageInstaller` engine branch: computer lookup/status queries fully disabled; package query enables without a computer; once-per-session install key scoped to `'engine'`; pre-install dedup reads the unified agent list across **all runtimes** (mirroring the backend's cross-runtime dedup); and because #3235 installs + starts engine agents inline, the engine path skips the 5-minute `waitForAgentWorkspaceStatus` polling entirely — it just invalidates the agent cache when the install call returns.
- v1 computer path byte-for-byte unchanged (resolution refactored into a pure helper, same semantics, existing tests still pass).

## Test plan
- [x] TDD (RED first): engine-mode user with no computer → package fetched, missing packs installed, no computer queries, cache invalidated, no polling; cross-runtime dedup skips engine-held packs; uid-scoped component enablement; v1 path unchanged (15 targeted tests green)
- [x] Full local gate `bash scripts/verify-web.sh`: guards + tsc + vitest + eslint — green
- [x] `pnpm lint:imports`: 0 errors
- [ ] CI (`web-quality` + `web-build-check`)

