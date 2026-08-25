---
title: "素材库新增「已发布产物」区，可直接查看并引用 Agent 产出的文件"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-24"
status: "待审核"
channels: ""
---

# 素材库新增「已发布产物」区，可直接查看并引用 Agent 产出的文件

## 核心宣传点

选中 v2 引擎 Agent 时，素材库不再只有一个工作区文件浏览器，上方会多出「已发布产物」区块，直接列出这个 Agent 已发布的成果文件，支持翻页浏览。已就绪的产物点一下就能在预览面板打开，图片直接预览，也能作为附件带进对话；还在生成中、失败或已删除的条目会置灰并标明状态。Computer（v1）Agent 的使用方式保持不变。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `76377d0105dd77ef5ace895620315b6b615dffe1`
- PR: #3380
- 作者: bill-srp
- 日期: 2026-08-24T10:41:04Z

### Commit Message

```
feat(assets): show published artifacts for engine agents (#3380)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Assets library now surfaces v2 engine artifacts: when the selected
agent in the workspace browser is an **engine-runtime** agent, the panel
splits into a "Published Artifacts" section (from the v2 artifact
registry via the existing per-workspace `GET
/agents/{workspace_id}/artifacts` API) above the existing "Workspace
Files" browser. Computer (v1) agents are unchanged — they keep the plain
file browser.
- New `web/app/src/components/assets/PublishedArtifactsList.tsx`: pages
through `useAgentArtifacts` (limit 20) with a frozen `createdBefore`
snapshot cursor (same pattern as the chat Resources panel's
PublishedArtifactsTab) so pagination stays stable while new artifacts
land; snapshot + page reset on workspace switch and on error-retry.
- Ready artifacts with a stable `url` are clickable and open in the
existing preview pane as an attachable target (`messageUrl` = the
artifact's stable engine URL, image extensions previewed as images);
pending/failed/deleted artifacts render disabled with their status.
- `WorkspaceBrowser.tsx` keeps a single agent selector; the engine
branch wraps both sections in labeled `<section>`s with i18n headings
(`assets.publishedArtifacts` / `assets.workspaceFiles`, en + zh).
- Frontend half of the Artifact Library feature; backend cross-agent
library API is PR #3372.

## Test plan
- [x] 7 new unit tests for `PublishedArtifactsList` (attachable preview
target with stable URL, non-ready/URL-less not selectable, image
detection, shared loading/empty states, error retry re-snapshots, page
next/prev drives the query, workspace switch resets page + snapshot)
- [x] 1 new `WorkspaceBrowser` test: engine workspaces split into
Published Artifacts + Workspace Files sections (computer agents keep the
legacy browser — existing tests unchanged)
- [x] Full local gate green: `bash scripts/verify-web.sh` — CI guards,
tsc, eslint, and the full vitest suite (364 files / 5166 tests)
- [ ] `web-build-check` (`next build`) runs in CI

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Assets library now surfaces v2 engine artifacts: when the selected agent in the workspace browser is an **engine-runtime** agent, the panel splits into a "Published Artifacts" section (from the v2 artifact registry via the existing per-workspace `GET /agents/{workspace_id}/artifacts` API) above the existing "Workspace Files" browser. Computer (v1) agents are unchanged — they keep the plain file browser.
- New `web/app/src/components/assets/PublishedArtifactsList.tsx`: pages through `useAgentArtifacts` (limit 20) with a frozen `createdBefore` snapshot cursor (same pattern as the chat Resources panel's PublishedArtifactsTab) so pagination stays stable while new artifacts land; snapshot + page reset on workspace switch and on error-retry.
- Ready artifacts with a stable `url` are clickable and open in the existing preview pane as an attachable target (`messageUrl` = the artifact's stable engine URL, image extensions previewed as images); pending/failed/deleted artifacts render disabled with their status.
- `WorkspaceBrowser.tsx` keeps a single agent selector; the engine branch wraps both sections in labeled `<section>`s with i18n headings (`assets.publishedArtifacts` / `assets.workspaceFiles`, en + zh).
- Frontend half of the Artifact Library feature; backend cross-agent library API is PR #3372.

## Test plan
- [x] 7 new unit tests for `PublishedArtifactsList` (attachable preview target with stable URL, non-ready/URL-less not selectable, image detection, shared loading/empty states, error retry re-snapshots, page next/prev drives the query, workspace switch resets page + snapshot)
- [x] 1 new `WorkspaceBrowser` test: engine workspaces split into Published Artifacts + Workspace Files sections (computer agents keep the legacy browser — existing tests unchanged)
- [x] Full local gate green: `bash scripts/verify-web.sh` — CI guards, tsc, eslint, and the full vitest suite (364 files / 5166 tests)
- [ ] `web-build-check` (`next build`) runs in CI

