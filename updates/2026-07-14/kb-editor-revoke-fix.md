---
title: "修复移除知识库编辑者时的授权校验"
type: "Bug Fix"
priority: "中"
date: "2026-07-14"
status: "待审核"
channels: ""
---

# 修复移除知识库编辑者时的授权校验

## 核心宣传点
修复移除知识库编辑者时未正确携带用户标识的问题（含越权防护）。

## 原始内容
### PR #2868 — fix(kb-sharing): send grantee_uid on editor revoke (root-cause, no edge exemption) (#2868)
作者: kyle-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2868

## ⚠️ RELEASE GATE — deploy proxy first

**SerendipityOneInc/ecap-proxy-service#152 MUST be deployed to the target environment BEFORE this PR is merged/deployed there.** (codex P1, accepted.)

There is no code shim that makes web-first safe: the edge IDOR guard only skips when the body has **no** `uid`, while an old proxy (`extra="forbid"`, `uid` only) rejects any body **without** `uid` — the same field can't be both present and absent. So the ordering is a hard, one-directional gate:
- proxy #152 first → accepts `grantee_uid` (and `uid` alias) → web-then works ✓
- web first, old proxy → `grantee_uid` is an unknown field → 422 ✗

(Not a regression of a working feature: revoke is currently broken at the edge with a 403; web-first would merely change that failure to a 422. Still — deploy proxy first.)

Staging order: merge proxy #152 → beta tag → rollout → then merge this.

## What

Editor-revoke body now sends `grantee_uid` (was `uid`).

## Why (root-cause fix)

The revoke body's `uid` was the **grantee being revoked**, not the caller — but the edge IDOR guard reads a body `uid` as caller self-identification and 403'd every editor revoke before it reached the backend. A body with no `uid` field is skipped by the guard, so renaming to `grantee_uid` fixes revoke with **zero middleware special-casing**. Supersedes #2867 (pattern-exemption), now closed. Pack-share revoke (`source`) unaffected.

## Pairs with

ecap-proxy-service#152 — accepts `grantee_uid`, keeps `uid` as a deprecated alias.

## Tests

GrantsPanel editor-revoke asserts the `grantee_uid` body. verify-web green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
