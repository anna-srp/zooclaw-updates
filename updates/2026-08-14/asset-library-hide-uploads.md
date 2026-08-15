---
title: "资产库精简：直接进入作品视图"
type: "体验优化"
priority: "中"
date: "2026-08-14"
status: "待审核"
channels: ""
---

## 核心宣传点

资产库去掉了多余的 Uploads / Artifacts 标签切换，打开就是文件浏览和预览，少点一次。

## 原始内容

feat(assets): hide uploads panel in asset library (#3381)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Hide the Uploads panel in the asset library: `AssetLibraryContent` no
longer renders the Uploads/Artifacts tab bar — the artifacts view
(workspace browser sidebar + preview area) renders directly.
Selection-mode wiring (attach-from-library) is unchanged and now flows
only through artifact previews.
- Delete the now-unreferenced `UploadsFeed.tsx` and its unit spec (the
knip dead-code gate fails CI on unused files; git history keeps it
recoverable). The chat Resources panel's separate `MyUploadsTab` is
untouched.
- Remove the now-unused `assets.uploads` / `assets.artifacts` locale
keys (en + zh), stale UploadsFeed mocks/comments in related specs, and
the stale eslint-config doc reference.
- Net −1,344 lines. Independent of #3380 (based on main); both touch the
assets surface but different files.

## Test plan
- [x] TDD: `AssetLibraryContent` spec rewritten first (no tablist
renders; workspace browser + preview render directly; selection-mode
wiring still works) — 4 expected failures against the old
implementation, then green
- [x] All touched specs pass (8 files, 147 tests)
- [x] `bash scripts/verify-web.sh` green: CI guards, tsc, eslint, full
vitest (645 files / 8,676 tests)
- [x] Coverage gate locally: 88.7 / 82.2 / 87.8 / 91.3 vs ratchet 83 /
75 / 81 / 85 (deleting well-covered UploadsFeed does not breach the
ratchet)

---
### PR Body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Hide the Uploads panel in the asset library: `AssetLibraryContent` no longer renders the Uploads/Artifacts tab bar — the artifacts view (workspace browser sidebar + preview area) renders directly. Selection-mode wiring (attach-from-library) is unchanged and now flows only through artifact previews.
- Delete the now-unreferenced `UploadsFeed.tsx` and its unit spec (the knip dead-code gate fails CI on unused files; git history keeps it recoverable). The chat Resources panel's separate `MyUploadsTab` is untouched.
- Remove the now-unused `assets.uploads` / `assets.artifacts` locale keys (en + zh), stale UploadsFeed mocks/comments in related specs, and the stale eslint-config doc reference.
- Net −1,344 lines. Independent of #3380 (based on main); both touch the assets surface but different files.

## Test plan
- [x] TDD: `AssetLibraryContent` spec rewritten first (no tablist renders; workspace browser + preview render directly; selection-mode wiring still works) — 4 expected failures against the old implementation, then green
- [x] All touched specs pass (8 files, 147 tests)
- [x] `bash scripts/verify-web.sh` green: CI guards, tsc, eslint, full vitest (645 files / 8,676 tests)
- [x] Coverage gate locally: 88.7 / 82.2 / 87.8 / 91.3 vs ratchet 83 / 75 / 81 / 85 (deleting well-covered UploadsFeed does not breach the ratchet)

