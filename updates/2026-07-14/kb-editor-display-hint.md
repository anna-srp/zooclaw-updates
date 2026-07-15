---
title: "知识库共享面板显示被添加编辑者的脱敏标识"
type: "体验优化"
priority: "中"
date: "2026-07-14"
status: "待审核"
channels: ""
---

# 知识库共享面板显示被添加编辑者的脱敏标识

## 核心宣传点
共享面板里编辑者一行显示所有者填写的脱敏邮箱/手机号（如 ky***@srp.one），便于确认加对了人。

## 原始内容
### PR #2857 — feat(kb-sharing): show masked display_hint on editor grant rows (#2857)
作者: kyle-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2857

## What

Editor rows in the Sharing panel show the masked identifier the owner typed (`ky***@srp.one`) instead of `Editor · 74369469…`. Legacy edges (no hint) and installer rows keep the pseudonymous truncated uid — installers' contact info is intentionally never shown to the library owner.

## Wire

`KnowledgeBaseGrant.display_hint?: string` — optional, so older proxies render exactly as today. Pairs with:
- SerendipityOneInc/ecap-proxy-service#149 — field accepted/stored/echoed, **masked server-side** (privacy boundary at the proxy)
- #2856 — BFF sends the masked hint on add_editor

Any deploy order is safe.

## Not in this PR

Pack-share rows still show the truncated pack_id. Resolving the pack *name* needs an agent-catalog data source this page doesn't load; pulling the whole catalog for one label isn't worth it — follow-up if the label proves confusing in practice.

## Tests (TDD, red first)

- editor row renders the hint when present (and not the uid)
- hint-less legacy edge + installer row keep the truncated uid

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### PR #2856 — feat(kb-sharing): send masked display_hint with editor grants (#2856)
作者: kyle-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2856

## What

`add_editor` now masks the owner-typed identifier (`ky***@srp.one` / `***5678`, capped at the proxy's 64-char limit) and sends it as `display_hint` alongside the resolved uid, so the proxy's grant audit list can show *who* was added.

Pairs with SerendipityOneInc/ecap-proxy-service#149 (proxy accepts/stores/echoes the field). Either side deploying first is safe: the field is optional upstream, and without it the audit list just keeps showing truncated uids.

## Why

The Sharing panel shows editor edges as `Editor · 74369469…` — unreadable. Design choice (write-time masking in the BFF, no reverse lookup, installer edges stay uid-only) keeps raw contact data inside the CSFLE profile store; the masked form is the only copy that leaves it.

## Tests (TDD, red first)

- `_mask_identifier`: email keeps 2 local chars + full domain; phone keeps last 4; output capped ≤64
- `add_editor` body carries the masked hint, never the raw identifier
- existing exact-body assertion updated for the evolved contract

🤖 Generated with [Claude Code](https://claude.com/claude-code)
