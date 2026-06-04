---
title: "搭建 React Router v7 管理员仪表盘框架"
type: "新功能上线"
priority: "高"
date: "2026-06-03"
status: "待审核"
channels: "站内弹窗, Use Case, Discord, changelog"
---
# 搭建 React Router v7 管理员仪表盘框架

## 核心宣传点

内部管理后台功能增强，提升 Agent 上架和审核效率。

## 原始内容

**Repo:** SerendipityOneInc/ecap-workspace  
**SHA:** `9aebf1fe44163b6fda530c877c31bd61a7dfa5e7`  
**作者:** bill-srp  
**日期:** 2026-06-03T10:37:46Z  
**URL:** https://github.com/SerendipityOneInc/ecap-workspace/commit/9aebf1fe44163b6fda530c877c31bd61a7dfa5e7

### Commit Message

```
feat(dashboard): scaffold React Router v7 admin dashboard shell on Workers (#2174)

## Linear

https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary

**PR 1 of 2** — splits the closed #2158 (agent-pack admin dashboard)
into two smaller, independently reviewable PRs. This one lands the
**dashboard shell only**, with no agent-packs feature logic.

- New `@zooclaw/dashboard-app`: a **React Router v7** app on Cloudflare
Workers (`web/dashboard`), distinct from the Next.js enterprise-admin
console
- shadcn/ui primitives scoped to what the shell actually consumes
(`button`, `input`, `separator`, `sheet`, `sidebar`, `skeleton`,
`tooltip`)
- Collapsible sidebar layout (`dashboard-shell`) with an Overview-only
nav and a blank masthead home page
- Registered as a pnpm workspace member and wired into the
`dependabot-lockfile-refresh` + `auto-review` workflows

The agent-packs catalogue (list/CRUD, submit-version flow, submissions
history, claw-interface API) lands in **PR 2** once this merges.

## Test plan
- [x] `pnpm typecheck` (cf-typegen + react-router typegen + `tsc -b`)
passes
- [x] `pnpm test` passes (0 tests — the suite ships with the feature in
PR 2)
- [x] `pnpm install --frozen-lockfile` is consistent (CI-equivalent)
- [ ] CI green on this PR
## PR size
`size-override` applied (~2045 lines, just over the 2000 gate). The bulk
is **generated/vendored**, not hand-written logic: the pnpm-lock delta
for a new workspace app plus shadcn/ui primitives copied verbatim from
the registry. Mirrors the original #2158, which also carried
`size-override`. Splitting the scaffold further would fragment a single
coherent app skeleton.
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary

**PR 1 of 2** — splits the closed #2158 (agent-pack admin dashboard) into two smaller, independently reviewable PRs. This one lands the **dashboard shell only**, with no agent-packs feature logic.

- New `@zooclaw/dashboard-app`: a **React Router v7** app on Cloudflare Workers (`web/dashboard`), distinct from the Next.js enterprise-admin console
- shadcn/ui primitives scoped to what the shell actually consumes (`button`, `input`, `separator`, `sheet`, `sidebar`, `skeleton`, `tooltip`)
- Collapsible sidebar layout (`dashboard-shell`) with an Overview-only nav and a blank masthead home page
- Registered as a pnpm workspace member and wired into the `dependabot-lockfile-refresh` + `auto-review` workflows

The agent-packs catalogue (list/CRUD, submit-version flow, submissions history, claw-interface API) lands in **PR 2** once this merges.

## Test plan
- [x] `pnpm typecheck` (cf-typegen + react-router typegen + `tsc -b`) passes
- [x] `pnpm test` passes (0 tests — the suite ships with the feature in PR 2)
- [x] `pnpm install --frozen-lockfile` is consistent (CI-equivalent)
- [ ] CI green on this PR
## PR size
`size-override` applied (~2045 lines, just over the 2000 gate). The bulk is **generated/vendored**, not hand-written logic: the pnpm-lock delta for a new workspace app plus shadcn/ui primitives copied verbatim from the registry. Mirrors the original #2158, which also carried `size-override`. Splitting the scaffold further would fragment a single coherent app skeleton.
