---
title: "组织知识库页面上线：可上传并管理文档"
type: "新功能上线"
priority: "中"
date: "2026-06-27"
status: "待审核"
channels: ""
---
# 组织知识库页面上线：可上传并管理文档

## 核心宣传点
现在你的组织有了专属「知识库」页面：可以查看组织内已上传的文档及其索引状态，并直接上传新文档（支持点击或拖拽上传），让团队资料集中沉淀、随用随取。

## 原始内容
```
feat(knowledge-base): org knowledge-base upload page (#2617)

## What

Admartels a standalone **org knowledge-base** page to `web-app` at
`/<locale>/knowledge-base`. It lists the organization's documents with
their index status and lets a member upload new documents — backed by
the existing `ecap-proxy-service` `/knowledge-base/*` endpoints.

The page lives under the `(app)` route group (so it inherits login +
`AccountSessionGate`) but is **not** registered in any nav menu — it's
reachable only at its own URL, as requested.

## How

- **Service** `src/services/knowledge-base.ts` — typed wrappers over the
existing `callClawInterfaceAPI` (routes through the `/api/claw` BFF →
proxy service, auto-attaches the JWT). Upload is `multipart/form-data`
(field `file`) with a 120s timeout.
- **Hook** `hooks/useKnowledgeBase.ts` — React Query: uid-scoped
documents query + upload mutation that **invalidates the list on
success** (no polling; new docs appear as `pending`).
- **Components** — `UploadDropzone` (click + drag-drop with client-side
type/size validation), `DocumentList` (rows + empty state),
`StatusBadge` (indexed/pending/failed via semantic `ecap-*` tokens).
- **Page** — `KnowledgeBaseClient` composes them with
success/warning/error toasts; `page.tsx` is a server component wrapping
it in `<Suspense>`.
- **i18n** — new `knowledgeBase` namespace in `en.ts` + `zh.ts` (other
locales fall back to English).

## Tenancy / security

Org is resolved **server-side from the JWT**; the client never sends
uid/org in the request body (upload sends only the file; list is a bare
GET). The uid only scopes the React Query cache key, so switching
accounts can't leak another org's cached list.

## Scope

List + basic single-file upload. Intentionally **no** polling, batch
upload, or delete/rename (none were requested; the backend exposes no
delete).

## Tests

14 unit tests across service, hook, and the three components (Vitest).
`pnpm tsc --noEmit` and `pnpm eslint` over the feature both pass clean.
```
