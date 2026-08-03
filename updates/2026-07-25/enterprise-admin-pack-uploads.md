---
title: "企业管理后台恢复 Agent Pack 上传能力"
type: "产品基础功能更新"
priority: "中"
外部: "B"
date: "2026-07-25"
status: "待审核"
channels: ""
---

## 核心宣传点

组织管理员可以直接在企业管理后台「添加 Pack」和「提交新版本」，支持 ZIP / TAR.GZ 压缩包解析、自动填充元数据、头像上传，无需再走额外通道即可上架和更新自家 Agent Pack。

## 原始内容

- **仓库**: SerendipityOneInc/ecap-workspace
- **SHA**: `463ae7cc3224c0bcec949114331976da183965a7`
- **PR**: #3067
- **作者**: bill-srp | **日期**: 2026-07-25T02:39:20Z

### Commit Message
```
feat(enterprise-admin): restore parsed pack archive uploads (#3067)

## Linear

N/A

## Summary

- restore the Enterprise Admin “Add pack” and “Submit new version” entry
points for organization admins
- share Dashboard Console’s Agent Pack archive parser through a
workspace package, support ZIP/TAR.GZ, and autofill archive metadata in
both Enterprise forms
- upload archives and optional avatars through the Worker R2 bindings,
including expanded metadata fields and parsed quick commands
- add an explicit admin-only direct-upload API contract while preserving
the Pack Test gate for non-admin submissions
- positively verify the target org admin and Pack before R2 writes;
clean up uploads after explicit rejection while preserving them when a
committed submission is possible
- redirect partial create failures to the persisted draft instead of
reusing stale form state against a cached Pack ID
- require claw-interface to HEAD the submitted private R2 key and verify
its stored org/Pack metadata before any direct upload can be
auto-approved

## Test plan

- [x] Enterprise Admin: 47 test files / 306 tests, TypeScript, ESLint,
and production build
- [x] Dashboard Console: 68 test files / 567 tests, TypeScript, ESLint,
and production build
- [x] Shared archive package: TypeScript and ESLint
- [x] claw-interface: targeted Pack Store/schema/service tests (78
passed), Ruff check, and Ruff format
- [x] Post-rebase focused checks: Enterprise 30 tests, Dashboard parser
19 tests, backend route 21 tests
- [x] Review fixes: R2 authorization/cleanup route tests plus
create/version compensation regressions
- [x] Provenance fix: 56 backend route, R2 storage, and direct-upload
validation tests plus Ruff check/format
- [x] Cleanup race fix: preserve assets after ambiguous transport/5xx
results; delete them after pre-submit failures or explicit 4xx rejection
- [ ] `scripts/verify-changed.sh` backend static tier was skipped
locally because `pyright` and `lint-imports` are not installed; CI
remains authoritative

## Size override

The size check counts 1,058 changed lines for moving the existing
526-line Dashboard archive parser into the shared workspace package (526
additions plus 532 deletions/re-export lines). The remaining overage is
the post-review org-admin authorization, R2 compensation path, and their
regression coverage. These changes form one cross-surface contract and
are kept together so neither app nor backend lands with a partial upload
flow.
```

### PR Body
```
## Linear

N/A

## Summary

- restore the Enterprise Admin “Add pack” and “Submit new version” entry points for organization admins
- share Dashboard Console’s Agent Pack archive parser through a workspace package, support ZIP/TAR.GZ, and autofill archive metadata in both Enterprise forms
- upload archives and optional avatars through the Worker R2 bindings, including expanded metadata fields and parsed quick commands
- add an explicit admin-only direct-upload API contract while preserving the Pack Test gate for non-admin submissions
- positively verify the target org admin and Pack before R2 writes; clean up uploads after explicit rejection while preserving them when a committed submission is possible
- redirect partial create failures to the persisted draft instead of reusing stale form state against a cached Pack ID
- require claw-interface to HEAD the submitted private R2 key and verify its stored org/Pack metadata before any direct upload can be auto-approved

## Test plan

- [x] Enterprise Admin: 47 test files / 306 tests, TypeScript, ESLint, and production build
- [x] Dashboard Console: 68 test files / 567 tests, TypeScript, ESLint, and production build
- [x] Shared archive package: TypeScript and ESLint
- [x] claw-interface: targeted Pack Store/schema/service tests (78 passed), Ruff check, and Ruff format
- [x] Post-rebase focused checks: Enterprise 30 tests, Dashboard parser 19 tests, backend route 21 tests
- [x] Review fixes: R2 authorization/cleanup route tests plus create/version compensation regressions
- [x] Provenance fix: 56 backend route, R2 storage, and direct-upload validation tests plus Ruff check/format
- [x] Cleanup race fix: preserve assets after ambiguous transport/5xx results; delete them after pre-submit failures or explicit 4xx rejection
- [ ] `scripts/verify-changed.sh` backend static tier was skipped locally because `pyright` and `lint-imports` are not installed; CI remains authoritative

## Size override

The size check counts 1,058 changed lines for moving the existing 526-line Dashboard archive parser into the shared workspace package (526 additions plus 532 deletions/re-export lines). The remaining overage is the post-review org-admin authorization, R2 compensation path, and their regression coverage. These changes form one cross-surface contract and are kept together so neither app nor backend lands with a partial upload flow.

```
