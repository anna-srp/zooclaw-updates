---
title: 知识库协作者可浏览共享库文件，“编辑者”更名为“协作者”
type: 产品基础功能更新
priority: 中
date: 2026-07-28
status: 待审核
channels: ""
---

## 核心宣传点

知识库共享更进一步：被授权的协作者现在可以直接浏览共享库里的文件（只读），一目了然地看到对方分享了什么。同时把原来的“编辑者”角色更名为更贴切的“协作者”，并在授权时清楚提示这次分享的可再分享范围，让共享权限更透明、更好懂。

## 原始内容

**Commit:** 19f5d63ece2... (PR #3086) by kyle-srp @ 2026-07-28T07:00:12Z

```
feat(knowledge-base): collaborator read-only library browsing + editor→collaborator rename (#3086)
```

### PR body

## What

Front-to-back so a knowledge-base library's **owner** or an active **editor** grantee ("collaborator") can browse a shared library's files, plus renames the user-facing "editor" role to "collaborator" and discloses the re-share reach at grant time. Plan clauses **C11–C21**; workspace spec: `docs/superpowers/specs/2026-07-28-kb-collaborator.md`.

## Pieces

- **BFF** (`services/claw-interface`): `GET /knowledge-base/kbs/{kb_id}/documents` — transparent passthrough to ecap-proxy-service (owner/editor authz lives upstream). GET-only, mirrors `list_grants`.
- **web client**: `listKbDocuments(kbId, signal?)` via `callClawInterfaceAPI` (generic claw proxy — no dedicated web BFF route, per the passthrough-first convention).
- **web view**: new `SharedLibraryDocuments` — React Query fetch → read-only `DocumentList` (loading / empty / error). Wired into `KnowledgeBaseClient`: selecting a shared library swaps in this view (the library's files live in its owning org and never appear in the caller's org-scoped `/documents` list).
- **read-only affordance**: `DocumentList.onDelete` is now optional; a read-only view passes no handler, so no delete control renders (even if a doc arrives without `is_owner`).
- **i18n**: "editor/编辑者" → "collaborator/协作者" (values only; wire `grant_type`/`role` stay `editor`, zero migration) + `reshareNotice` disclosure in `GrantsPanel`.

Pack/installer edge rendering + stop-sharing (C19–C21) already existed in `GrantsPanel` and were left untouched.

## Tests

Clause-keyed unit tests: BFF passthrough + registration; client URL/signal; `SharedLibraryDocuments` C13–C15 (incl. read-only with `is_owner` missing, library naming); `KnowledgeBaseClient` shared-selection wiring (renders the collaborator view, drops the org filter, threads `library`). kb frontend suite green (90), BFF green (2), tsc + eslint clean.

## Depends on / deploy order (REQUIRED)

The shared-library browse chain is web → claw-interface `/kbs/{kb_id}/documents` → ecap-proxy-service `/kbs/{kb_id}/documents`. These three surfaces deploy independently, and the route only exists once claw-interface + proxy ship, so:

**Required deploy order: ecap-proxy-service (#166) → claw-interface → web.**

If web ships first, selecting a shared library shows a non-fatal error state until claw-interface/proxy catch up. A 404 is intentionally **not** degraded to an "empty" state on the client — the proxy legitimately 404s a revoked/deleted/unknown library, which status alone can't distinguish from a not-yet-deployed route (codex P1). The i18n rename has no backend dependency. Other locales fall back to English for new keys. No data migration.
