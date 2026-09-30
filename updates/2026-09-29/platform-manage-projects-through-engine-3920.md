---
title: "开发者平台的项目改由引擎统一管理：支持命名项目的创建与归档，默认项目不可归档"
type: "Feature"
priority: "中"
date: "2026-09-29"
status: "待审核"
channels: ""
---

# 开发者平台的项目改由引擎统一管理：支持命名项目的创建与归档，默认项目不可归档

## 核心宣传点

开发者平台的项目管理从本地实现切到引擎统一管理：创建命名项目时会在引擎侧建好并持久化引擎 ID，如果本地保存中途被打断，只会恢复归属匹配的、平台自己拥有的引擎项目，不会认领别人的。命名项目的归档也走引擎，隐式的默认项目不允许归档。每个组织沿用引擎侧那个隐式默认项目，平台在管理接口里把它暴露为 default，默认项目的 API Key 按组织存取、项目 ID 为空。历史遗留的本地默认项目记录不再出现在项目列表里，它们的 API Key 也会被拒绝；这次改动不删除预发环境的历史数据。平台的项目界面和对外的接口契约文档同步更新。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary

- Create named Platform Projects through Engine, persist Engine IDs, and recover only matching Platform-owned Engine Projects after an interrupted local save.
- Archive named Projects through Engine. The implicit Default Project cannot be archived.
- Use Engine's implicit `project_id = null` Default for each Organization. Platform exposes it as `"default"` in management routes; Default API Keys are stored and queried by Organization with a null Project ID.
- Keep legacy local Default rows out of Project lists and reject their API Keys. This PR does not delete staging data.
- Update the Platform Project UI and its documented API contract.

## Test plan

- [x] Backend targeted unit tests: 93 passed.
- [x] Backend Mongo BDD tests: 7 passed.
- [x] Backend `bash scripts/verify-py.sh`: passed, including ruff, pyright, and import contracts.
- [x] Platform `pnpm lint`, `pnpm typecheck`, `pnpm test` (71 passed), and `pnpm build`: passed with Node 24.
- [x] Pre-commit and pre-push checks: passed. The outdated `check-user` hook was skipped because the active Finn GitHub login is `finn930`; commit author is `finn-srp <finn@srp.one>`.
- [ ] Backend `--full` was not run, per maintainer instruction.
- [x] Staging CSFLE: exact PR repository reads and index creation passed through the deployed encrypted client. See `docs/staging-validation/2026-09-29-platform-projects-csfle-and-cleanup.md`.

## Scope and rollout

The Platform machine-key authentication mode remains disabled for SDK/runtime requests. In staging, 7 legacy `prj_` Projects and 2 already-revoked Keys were removed after a protected backup and reference audit. Organization, Billing order, payment-event, and user records were preserved. The cleanup and validation are recorded in `docs/staging-validation/2026-09-29-platform-projects-csfle-and-cleanup.md`.

Related Engine issue: https://github.com/SerendipityOneInc/zooclaw-engine/issues/1573

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `5354ed9d6e2a1d9c411f239461db5ca8f9fce08a`
- PR: #3920
- 作者：finn-srp
- 日期：2026-09-29T06:27:35Z

### Commit Message

```
feat(platform): manage projects through Engine (#3920)

## Summary

- Create named Platform Projects through Engine, persist Engine IDs, and
recover only matching Platform-owned Engine Projects after an
interrupted local save.
- Archive named Projects through Engine. The implicit Default Project
cannot be archived.
- Use Engine's implicit `project_id = null` Default for each
Organization. Platform exposes it as `"default"` in management routes;
Default API Keys are stored and queried by Organization with a null
Project ID.
- Keep legacy local Default rows out of Project lists and reject their
API Keys. This PR does not delete staging data.
- Update the Platform Project UI and its documented API contract.

## Test plan

- [x] Backend targeted unit tests: 93 passed.
- [x] Backend Mongo BDD tests: 7 passed.
- [x] Backend `bash scripts/verify-py.sh`: passed, including ruff,
pyright, and import contracts.
- [x] Platform `pnpm lint`, `pnpm typecheck`, `pnpm test` (71 passed),
and `pnpm build`: passed with Node 24.
- [x] Pre-commit and pre-push checks: passed. The outdated `check-user`
hook was skipped because the active Finn GitHub login is `finn930`;
commit author is `finn-srp <finn@srp.one>`.
- [ ] Backend `--full` was not run, per maintainer instruction.
- [x] Staging CSFLE: exact PR repository reads and index creation passed
through the deployed encrypted client. See
`docs/staging-validation/2026-09-29-platform-projects-csfle-and-cleanup.md`.

## Scope and rollout

The Platform machine-key authentication mode remains disabled for
SDK/runtime requests. In staging, 7 legacy `prj_` Projects and 2
already-revoked Keys were removed after a protected backup and reference
audit. Organization, Billing order, payment-event, and user records were
preserved. The cleanup and validation are recorded in
`docs/staging-validation/2026-09-29-platform-projects-csfle-and-cleanup.md`.

Related Engine issue:
https://github.com/SerendipityOneInc/zooclaw-engine/issues/1573
```

来源：SerendipityOneInc/ecap-workspace @ 5354ed9d，PR #3920，作者 finn-srp。
