---
title: "素材库改版：「我的上传」和「AI 生成」分开成两个标签页，支持搜索和多维筛选"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-25"
status: "待审核"
channels: ""
---

# 素材库改版：「我的上传」和「AI 生成」分开成两个标签页，支持搜索和多维筛选

## 核心宣传点

素材库重新做了一版：我自己传的文件和 Agent 生成的文件拆成两个独立标签页，各自都能按文件类型、按 Agent 筛选，也能直接搜索；支持网格和列表两种布局、按日期自动分组、图片可直接预览，选好的素材还能一键带回聊天输入框。PDF、DOCX、PPTX、XLSX 这类文档在网格里显示封面时不会去解析整个文件，所以列表再长也不会拖慢页面。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `07feaace1e8d8d931de7b447a7b48a85e2eb862a`
- PR: #3225
- 作者: shana-srp
- 日期: 2026-08-25T02:41:10Z

### Commit Message

```
feat(assets): redesign unified asset library (#3225)

## Summary

- restore the original #3225 Library frontend with separate My uploads
and AI generated tabs
- keep the shared file-type and Agent filters, search, grid/list
layouts, date grouping, image preview, and Composer selection flow
- connect AI generated files to the account-scoped cursor endpoint from
#3372: `GET /agents/artifacts/library`
- keep structured-file grid previews fixed-cost; PDF, DOCX, PPTX, and
XLSX covers do not parse the full document
- discard authenticated preview completions if the account or Mattermost
token changes while a Blob request is in flight

## Conflict resolution

- merged the latest `origin/main` into the existing #3225 branch with
the PR branch as first parent
- restored the last known-good Library frontend from `dd34a2ae` on top
of current main instead of resolving conflicts by taking main's empty
tree
- GitHub reports the PR as `MERGEABLE`; the PR now contains the Library
implementation rather than a zero-file diff

## Validation

- `bash scripts/verify-web.sh` passed TypeScript, focused Vitest,
ESLint, and all frontend governance guards
- restored Library suite: 84 relevant tests passed
- authenticated-preview regression suite: 39 UploadsFeed tests passed
- dependency-boundary and dead-code gates passed
- first GitHub run passed web build, web lint/typecheck, web tests,
CodeQL, title, and size checks; the follow-up review fix is running the
same gates again

## Size override

The restored page crosses the 3,000-line budget because it reintroduces
the complete Library feed and its comprehensive regression suite while
deleting the superseded workspace-browser implementation. The
`size-override` label keeps the production behavior and tests together
in the original #3225 PR instead of dropping coverage to trim 63 lines.

## Dependency

The backend Library route is already on `main` via #3372. This PR
restores and adapts the frontend only.

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Description

```
## Summary

- restore the original #3225 Library frontend with separate My uploads and AI generated tabs
- keep the shared file-type and Agent filters, search, grid/list layouts, date grouping, image preview, and Composer selection flow
- connect AI generated files to the account-scoped cursor endpoint from #3372: `GET /agents/artifacts/library`
- keep structured-file grid previews fixed-cost; PDF, DOCX, PPTX, and XLSX covers do not parse the full document
- discard authenticated preview completions if the account or Mattermost token changes while a Blob request is in flight

## Conflict resolution

- merged the latest `origin/main` into the existing #3225 branch with the PR branch as first parent
- restored the last known-good Library frontend from `dd34a2ae` on top of current main instead of resolving conflicts by taking main's empty tree
- GitHub reports the PR as `MERGEABLE`; the PR now contains the Library implementation rather than a zero-file diff

## Validation

- `bash scripts/verify-web.sh` passed TypeScript, focused Vitest, ESLint, and all frontend governance guards
- restored Library suite: 84 relevant tests passed
- authenticated-preview regression suite: 39 UploadsFeed tests passed
- dependency-boundary and dead-code gates passed
- first GitHub run passed web build, web lint/typecheck, web tests, CodeQL, title, and size checks; the follow-up review fix is running the same gates again

## Size override

The restored page crosses the 3,000-line budget because it reintroduces the complete Library feed and its comprehensive regression suite while deleting the superseded workspace-browser implementation. The `size-override` label keeps the production behavior and tests together in the original #3225 PR instead of dropping coverage to trim 63 lines.

## Dependency

The backend Library route is already on `main` via #3372. This PR restores and adapts the frontend only.


```
