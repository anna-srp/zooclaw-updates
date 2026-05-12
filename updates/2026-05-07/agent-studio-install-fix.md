---
title: "修复 Agent Studio /studio install 安装失败问题"
type: "Bug Fix"
priority: "高"
date: "2026-05-07"
status: "待审核"
channels: "Discord, changelog"
---
# 修复 Agent Studio /studio install 安装失败问题

## 核心宣传点
通过 Agent Studio 安装 Agent 时不再反复失败，安装流程一次成功，体验更流畅可靠。

## 原始内容

### Commit Message
```
fix(agent-studio): /studio install — correct API contract, dry-run check, manifest expansion (#116)
```

### PR Description
## Summary

`/studio install` was failing in production: the install CLI sent the wrong payload shape, so the deployed agent had to hot-patch the script mid-conversation across 4 attempts to complete a single install.

This PR aligns the script with the actual install API contract, adds the safety nets the prior version was missing, fixes a pre-existing URL helper bug exposed along the way, and brings `agent-pack.yaml` up to the scaffold-output format.

## What was broken

1. **Wrong API payload.** Script sent `path_type="file"` (local) or `path_type="url"` (remote) with a raw filesystem path / plain URL. The install API only accepts `path_type="remote"` with a **base64-encoded HTTPS URL** as `path_value`, and rejects local filesystem paths altogether.
2. **No staging.** Local archives weren't HTTPS-served, so even if `path_type` were correct, the API server couldn't reach the file.
3. **Conflict detection lied for legacy cards.** `determine_card_action` short-circuited on `same_version` even when `path_type` had migrated, so a user upgrading from a pre-PR install would silently reuse a stale `file`-typed card.
4. **`--check-only` had real side effects.** Even a "dry-run" preview ran `publish.py` and copied the archive into the user's HTTPS-served `artifacts/shares/` before any user confirmation.
5. **`list-sources` exposed fake API fields.** Output included `path_type="file"` + raw paths that didn't match the actual install payload — misleading the LLM consumer.
