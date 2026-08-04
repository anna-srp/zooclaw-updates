---
title: "知识库工作区改版"
type: "体验优化"
priority: "中"
date: "2026-08-03"
status: "待审核"
channels: ""
---

## 核心宣传点

知识库改用清晰的库卡片布局，支持我拥有的/共享的/未归档状态，文档管理、协作者邀请与分页体验全面升级。

## 原始内容

**Commit**: `644a5a36f98ea458c185f02a6a6a08eb8af6db5d` — shana-srp — 2026-08-03T05:58:21Z

### Commit Message

```
feat(web): redesign knowledge base workspace (#3176)

## Linear

N/A

## Summary

- Redesign the knowledge-base overview around library cards, including
owned, shared, and unfiled states.
- Add fixed-size library dialogs for documents and access management,
collaborator invitation, stable pagination, and responsive upload/file
states.
- Add localized copy, custom knowledge-base icons, mock scenarios,
focused unit coverage, and a design specification.
- Preserve the existing backend data contracts and mutation flow.

## Merge queue repair

- Merged current `main` after merge-group run 30781003384 exposed
contract drift from #3181.
- Updated artifact selection tests for the new `messageUrl` contract and
removed the unused `getAgentArtifact` export that failed the knip hard
gate.
- Applied `size-override` because the PR event still uses base SHA
`a7ab6615`, so the size job counts later `main` changes (11,513 lines)
as PR changes even though they are already on `main`.

## Test plan

- [x] Knowledge-base focused Vitest suite: 59 tests passed.
- [x] Artifact merge-failure Vitest suite: 8 tests passed.
- [x] `lint:ci` passed, including the knip hard gate.
- [x] Repository `verify-web.sh` passed (governance guards, TypeScript,
focused Vitest, ESLint).

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

```
## Linear

N/A

## Summary

- Redesign the knowledge-base overview around library cards, including owned, shared, and unfiled states.
- Add fixed-size library dialogs for documents and access management, collaborator invitation, stable pagination, and responsive upload/file states.
- Add localized copy, custom knowledge-base icons, mock scenarios, focused unit coverage, and a design specification.
- Preserve the existing backend data contracts and mutation flow.

## Merge queue repair

- Merged current `main` after merge-group run 30781003384 exposed contract drift from #3181.
- Updated artifact selection tests for the new `messageUrl` contract and removed the unused `getAgentArtifact` export that failed the knip hard gate.
- Applied `size-override` because the PR event still uses base SHA `a7ab6615`, so the size job counts later `main` changes (11,513 lines) as PR changes even though they are already on `main`.

## Test plan

- [x] Knowledge-base focused Vitest suite: 59 tests passed.
- [x] Artifact merge-failure Vitest suite: 8 tests passed.
- [x] `lint:ci` passed, including the knip hard gate.
- [x] Repository `verify-web.sh` passed (governance guards, TypeScript, focused Vitest, ESLint).

```
