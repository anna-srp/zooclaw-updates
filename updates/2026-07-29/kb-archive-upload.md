---
title: "知识库支持压缩包上传：拖入 .zip/.tar 一次性导入整包文件，界面按树状展开"
type: "新功能上线"
priority: "高"
date: "2026-07-29"
status: "待审核"
channels: ""
---

## 核心宣传点

现在可以直接把 .zip / .tar / .tar.gz 压缩包拖进知识库，系统会自动解包并把其中每个受支持的文件作为独立文档入库，界面上整个压缩包显示为一个可展开的节点，批量导入资料更省事。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- commit：1a4a89f592381ccaa9647d7a8e1d2b88214f5ddf
- PR：#3096
- 日期：2026-07-29T04:25:46Z

### Commit message

```
feat(kb-archive): archive (.zip/.tar/.tar.gz) upload — BFF passthrough + web two-level tree (#3096)

## What

Client + BFF for **knowledge-base archive upload** — the workspace half
of the archive feature. Users drop a `.zip` / `.tar` / `.tar.gz`; the
proxy extracts it and ingests each supported file as its own KB document
(all-or-nothing), and the UI shows the bundle as one expandable node
over its files.

Backend counterpart: **ecap-proxy-service PR #168** (`POST
/knowledge-base/upload/archive`, `DELETE /knowledge-base/archives/{id}`,
provenance + resource guards). This PR is safe to merge alongside it.

## BFF (`claw-interface`) — E段

- `POST /knowledge-base/upload/archive`: transparent passthrough with
the larger **100MB** archive body cap (vs 50MB single-file); mirrors the
existing `upload_document` shape.
- `DELETE /knowledge-base/archives/{id}`: idempotent passthrough,
mirroring the existing `delete_document` / `delete_kb` `@router.delete`
routes in this module.
- `_error_detail` now forwards a structured **dict/list** `detail`
intact, so the web can localize the proxy's `{code, params}` rejection
instead of it being flattened to a generic string.

## Web — F段

- **Endpoint routing by extension** (F1): archives → `/upload/archive`,
everything else → `/upload`. Both target the same library.
- **Client precheck** (F2): archives get the 100MB soft cap; >100MB
rejected with a local toast.
- **Two-level tree** (F3): `DocumentList` groups files sharing an
`archive_id` under one collapsible node (`archive_filename` + count;
children show `display_path` + index status); single files stay leaves.
`onDelete` remains optional so read-only shared-library views are
unaffected.
- **Per-archive delete** (F4): node delete → confirm → `DELETE
/archives/{id}`.
- **Localized errors** (F5): each structured rejection code
(`archiveUnsupported` / `archiveCorrupt` / … / `archiveBusy`) maps to an
en + zh message; 429 → "try again shortly".
- **Success count** (F6): imported-document count in the success toast.

## Rebased onto current main

The original archive work sat on a 183-commits-stale branch where the KB
UI lived at `(app)/knowledge-base/`. main relocated it to
`(app)/plugins/knowledge-base/` and shipped JSON/MD support +
collaborator/grants. This PR re-applies the archive feature onto the
**current** structure; the stale JSON/MD commits were dropped (already
on main). Kept lean: `isAcceptedUpload` (used only by its own test) and
an unused `KnowledgeBaseArchiveItem` export were dropped to satisfy the
dead-code gate.

## Tests

- BFF: `TestKnowledgeBaseArchiveProxy` — 4 tests incl.
`test_dict_detail_preserved` (whole file **35 passed**; route
pyright-clean).
- Web: 5 new specs (constants F1/F2, service E/F1, `UploadDropzone` F2,
`DocumentList` tree F3/F4, `KnowledgeBaseClient` routing/errors
F1/F5/F6) — **16 tests**. Full KB dir **106 passed** (no regression);
`tsc` clean; `dup:src` + knip clean for touched files.

> Note: eslint couldn't run in the authoring checkout (workspace
`@zooclaw/design-system` not linked locally); CI `web-quality` is the
authoritative eslint gate. Code mirrors the surrounding files' style.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What

Client + BFF for **knowledge-base archive upload** — the workspace half of the archive feature. Users drop a `.zip` / `.tar` / `.tar.gz`; the proxy extracts it and ingests each supported file as its own KB document (all-or-nothing), and the UI shows the bundle as one expandable node over its files.

Backend counterpart: **ecap-proxy-service PR #168** (`POST /knowledge-base/upload/archive`, `DELETE /knowledge-base/archives/{id}`, provenance + resource guards). This PR is safe to merge alongside it.

## BFF (`claw-interface`) — E段

- `POST /knowledge-base/upload/archive`: transparent passthrough with the larger **100MB** archive body cap (vs 50MB single-file); mirrors the existing `upload_document` shape.
- `DELETE /knowledge-base/archives/{id}`: idempotent passthrough, mirroring the existing `delete_document` / `delete_kb` `@router.delete` routes in this module.
- `_error_detail` now forwards a structured **dict/list** `detail` intact, so the web can localize the proxy's `{code, params}` rejection instead of it being flattened to a generic string.

## Web — F段

- **Endpoint routing by extension** (F1): archives → `/upload/archive`, everything else → `/upload`. Both target the same library.
- **Client precheck** (F2): archives get the 100MB soft cap; >100MB rejected with a local toast.
- **Two-level tree** (F3): `DocumentList` groups files sharing an `archive_id` under one collapsible node (`archive_filename` + count; children show `display_path` + index status); single files stay leaves. `onDelete` remains optional so read-only shared-library views are unaffected.
- **Per-archive delete** (F4): node delete → confirm → `DELETE /archives/{id}`.
- **Localized errors** (F5): each structured rejection code (`archiveUnsupported` / `archiveCorrupt` / … / `archiveBusy`) maps to an en + zh message; 429 → "try again shortly".
- **Success count** (F6): imported-document count in the success toast.

## Rebased onto current main

The original archive work sat on a 183-commits-stale branch where the KB UI lived at `(app)/knowledge-base/`. main relocated it to `(app)/plugins/knowledge-base/` and shipped JSON/MD support + collaborator/grants. This PR re-applies the archive feature onto the **current** structure; the stale JSON/MD commits were dropped (already on main). Kept lean: `isAcceptedUpload` (used only by its own test) and an unused `KnowledgeBaseArchiveItem` export were dropped to satisfy the dead-code gate.

## Tests

- BFF: `TestKnowledgeBaseArchiveProxy` — 4 tests incl. `test_dict_detail_preserved` (whole file **35 passed**; route pyright-clean).
- Web: 5 new specs (constants F1/F2, service E/F1, `UploadDropzone` F2, `DocumentList` tree F3/F4, `KnowledgeBaseClient` routing/errors F1/F5/F6) — **16 tests**. Full KB dir **106 passed** (no regression); `tsc` clean; `dup:src` + knip clean for touched files.

> Note: eslint couldn't run in the authoring checkout (workspace `@zooclaw/design-system` not linked locally); CI `web-quality` is the authoritative eslint gate. Code mirrors the surrounding files' style.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

