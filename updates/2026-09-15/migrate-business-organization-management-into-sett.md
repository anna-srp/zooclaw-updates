---
title: "feat(settings): migrate Business organization management into Settings (#3715)"
type: "新功能"
priority: "低"
date: "2026-09-15"
status: "待审核"
channels: ""
---

# feat(settings): migrate Business organization management into Settings (#3715)

## 核心宣传点

## Linear

N/A — migration spec: `docs/superpowers/specs/2026-09-14-settings-business-migration.md`

## Summary

- Moves the existing Business organization experience into the main Settings shell: General, Members, Packs, and Usage.
- Preserves the existing setup, invite acceptance, organization join, and checkout flows under the main web app.
- Migrates only the file routes required by existing Business behavior: organization logos in `R2_PUBLIC_BUCKET` and Pack archives/assets in `R2_AGENT_PACKS_BUCKET`.
- Adds an isolated `team-admin` local mock and four loopback-only Playwright scenarios.
- Does not add or change any `services/claw-interface` API, move R2 objects, deploy, or cut over a domain.

The `business.zoowork.ai` invite/domain cutover is tracked separately in #3727. Removal of the old Business frontend remains tracked by #3713 and must happen only after deployment and observation.

## Review order

The PR is intentionally one migration unit, but the history is split into seven reviewable commits:

1. `docs(settings): define Business migration boundary`
2. `feat(settings): migrate Business file storage routes`
3. `feat(settings): add organization management pages`
4. `feat(settings): migrate organization Pack management`
5. `feat(settings): migrate setup invite and checkout flows`
6. `test(settings): add team admin mock coverage`
7. `fix(settings): reject oversized R2 uploads before parsing`

The diff exceeds the normal 3,000-line budget because the old Business surface is being moved as one deployable flow. Splitting General, Members, Packs, setup/invite, and checkout into separate PRs would leave intermediate states where navigation or entry flows point to missing pages. The `size-override` label is therefore retained; reviewers can follow the commit order above.

## Test plan

- [x] Governance guards, TypeScript, ESLint, and `git diff --check` passed on Node 24 after rebasing onto current `origin/main`.
- [x] Full frontend unit suite passed: 798 files; 10,112 tests passed, 70 skipped, 1 todo.
- [x] R2 upload route tests passed 7/7, including pre-parse `Content-Length` rejection and invalid-header fallback.
- [x] Stateful local Playwright suite passed 4/4 against the loopback-only `team-admin` mock: General/logo persistence, member lifecycle, quota persistence, and mobile navigation.
- [x] Next production webpack compilation completed successfully locally.
- [ ] CI `web-build-check` currently fails while fetching existing Google Fonts (`Inter`, `DM Sans`, and `Cormorant Garamond`) with `ETIMEDOUT`; no migration module fails compilation.

No production deployment, domain change, payment, real invitation, or production data write was performed.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `0eafabb67bb74c64a865c9aaf824bce62c11592b`
- PR: #3715
- 作者：finn-srp
- 日期：2026-09-15T07:03:50Z

### Commit Message

```
feat(settings): migrate Business organization management into Settings (#3715)

## Linear

N/A — migration spec:
`docs/superpowers/specs/2026-09-14-settings-business-migration.md`

## Summary

- Moves the existing Business organization experience into the main
Settings shell: General, Members, Packs, and Usage.
- Preserves the existing setup, invite acceptance, organization join,
and checkout flows under the main web app.
- Migrates only the file routes required by existing Business behavior:
or
```
