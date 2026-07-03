---
title: "知识库支持删除文档，并在设置中新增入口"
type: "体验优化"
priority: "中"
date: "2026-07-02"
status: "待审核"
channels: ""
---
# 知识库支持删除文档，并在设置中新增入口
## 核心宣传点
知识库页面现在可以直接删除自己上传的文档（仅文档所有者可删），并且在设置导航里新增了「Knowledge Base」入口，管理内部资料更方便。
## 原始内容
### [ecap-workspace PR #2688]

feat(knowledge-base): owner-only document delete + settings nav entry (#2688)

## Summary

Adds knowledge-base document **management** to the web app +
claw-interface BFF, and surfaces the page in Settings.

Pairs with
**[ecap-proxy-service#141](https://github.com/SerendipityOneInc/ecap-proxy-service/issues/141)**
(owner-only delete enforcement + `is_owner` in the documents listing),
already implemented and deployed to staging (`v0.6.31-beta.6`). This PR
is the `ecap-workspace` side.

Closes #2687

## What's included

- **Delete a document** from the knowledge-base page
- `deleteDocument()` service + React Query mutation (invalidates the
documents list on success)
  - Per-row delete control with a confirm dialog + success/error toast
- claw-interface BFF `DELETE /knowledge-base/documents/{id}` —
transparent passthrough forwarding the caller's bearer token; upstream
status codes (incl. `403`/`404`) pass through verbatim (no BFF change
needed to error handling)
- **Owner-only gating (UX):** the delete control is hidden when
`is_owner === false`. The field is optional for backward-compat (missing
→ shown); the **real** authorization gate is the upstream `403` on a
non-owner delete.
- **Status label copy:** `indexed → Uploaded / 已上传`, `pending → Parsing…
/ 解析中`; the date column header `Indexed → Upload time / 上传时间`. Status
*values* stay backend-owned — only the localized display text changes.
- **Settings navigation:** a **Knowledge Base** entry under **IM
Channels** in `claw-settings`, linking out to the standalone
`/knowledge-base` page (org-scoped, so it is not placed behind the
bot-gated settings tabs).

## Testing

- **Unit:** `verify-web.sh` green — `tsc` + `vitest` (added service /
hook / `DocumentList` cases incl. the `is_owner` three-state gate) +
`eslint`; claw-settings suite 555/555. Backend `verify-py.sh` green —
`ruff` + `pyright` + import-linter; added BFF delete-route unit tests
(owner passthrough + 403/404 propagation).
- **End-to-end (local → staging):** validated the full delete flow
against staging `ecap-proxy-service` through a local claw-interface +
Telepresence tunnel: delete of an owned document succeeds (toast + list
refresh); the deployed schema returns `is_owner`; non-owner delete
returns the upstream `403`.

## Notes

- Delete authorization + `is_owner` computation live in
`ecap-proxy-service` (#141), not here.
- No auto-merge requested.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---

## PR Description

## Summary

Adds knowledge-base document **management** to the web app + claw-interface BFF, and surfaces the page in Settings.

Pairs with **[ecap-proxy-service#141](https://github.com/SerendipityOneInc/ecap-proxy-service/issues/141)** (owner-only delete enforcement + `is_owner` in the documents listing), already implemented and deployed to staging (`v0.6.31-beta.6`). This PR is the `ecap-workspace` side.

Closes #2687

## What's included

- **Delete a document** from the knowledge-base page
  - `deleteDocument()` service + React Query mutation (invalidates the documents list on success)
  - Per-row delete control with a confirm dialog + success/error toast
  - claw-interface BFF `DELETE /knowledge-base/documents/{id}` — transparent passthrough forwarding the caller's bearer token; upstream status codes (incl. `403`/`404`) pass through verbatim (no BFF change needed to error handling)
- **Owner-only gating (UX):** the delete control is hidden when `is_owner === false`. The field is optional for backward-compat (missing → shown); the **real** authorization gate is the upstream `403` on a non-owner delete.
- **Status label copy:** `indexed → Uploaded / 已上传`, `pending → Parsing… / 解析中`; the date column header `Indexed → Upload time / 上传时间`. Status *values* stay backend-owned — only the localized display text changes.
- **Settings navigation:** a **Knowledge Base** entry under **IM Channels** in `claw-settings`, linking out to the standalone `/knowledge-base` page (org-scoped, so it is not placed behind the bot-gated settings tabs).

## Testing

- **Unit:** `verify-web.sh` green — `tsc` + `vitest` (added service / hook / `DocumentList` cases incl. the `is_owner` three-state gate) + `eslint`; claw-settings suite 555/555. Backend `verify-py.sh` green — `ruff` + `pyright` + import-linter; added BFF delete-route unit tests (owner passthrough + 403/404 propagation).
- **End-to-end (local → staging):** validated the full delete flow against staging `ecap-proxy-service` through a local claw-interface + Telepresence tunnel: delete of an owned document succeeds (toast + list refresh); the deployed schema returns `is_owner`; non-owner delete returns the upstream `403`.

## Notes

- Delete authorization + `is_owner` computation live in `ecap-proxy-service` (#141), not here.
- No auto-merge requested.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

