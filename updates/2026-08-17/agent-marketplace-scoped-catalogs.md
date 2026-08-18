---
title: "Agent 市场分成「公开 / 共享给我 / 我的 Agent」三个目录"
type: 产品基础功能更新
priority: 中
date: 2026-08-17
status: "待审核"
channels: ""
---

## 核心宣传点

Agent 市场重新整理成三个独立目录：公开市场、共享给我的、我的 Agent。别人分享给你的 Agent 只有在你真正「雇佣」后才会出现在「共享给我」，不会再被一堆链接刷屏；「我的 Agent」里直接能看到自己在 Agent Builder 建的 Agent 及其状态标签，找 Agent、装 Agent、管 Agent 都在一个地方完成。

## 原始内容

**Commit**: `c5b88ecbfd` — feat(agent-marketplace): add scoped agent catalogs (#3368)
**作者**: lynn Zhuang ｜ **日期**: 2026-08-17T05:55:32Z

```
feat(agent-marketplace): add scoped agent catalogs (#3368)

## Linear

N/A

## Summary

- Refactor Agent Marketplace into independent Public, Shared with me,
and My Agents catalogs.
- Keep share-link agents out of Shared with me until they are hired,
while preserving installed snapshots if sharing later ends.
- Surface Agent Builder records directly in My Agents with lifecycle
badges and ZooClaw Design System card actions.
- Preserve existing public card styling, detail dialogs,
install/update/fire flows, and add mock scenarios for all visibility
states.
- Add regression coverage for lifecycle rendering, exact
shared-workspace updates, install-state loading, bio fallback, dialog
embedding, and card keyboard semantics.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Targeted `verify-web.sh`: TypeScript, 32 Vitest files / 401 tests,
and ESLint
- [x] `agents-manager.spec.ts`: 9 Playwright scenarios against the local
mock stack
- [x] Manual review at `http://localhost:3006/agents-manager`

## Size override

This is one cohesive Marketplace information-architecture refactor
spanning the catalog model, three scoped views, shared lookup state,
embedded My Agents cards, mocks, and regression tests. Splitting those
contracts would leave intermediate branches with mismatched UI/data
behavior. The branch exceeds the normal size budget, so this PR requires
the `size-override` label.
```
