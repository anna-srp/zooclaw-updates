---
title: "修复：Amazon Analyst 在细分类目下搜索不到结果的问题"
type: "Bug Fix"
priority: "中"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 修复：Amazon Analyst 在细分类目下搜索不到结果的问题

## 核心宣传点

修复了 Amazon Analyst Agent 在使用细分品类（如「耳机 > 头戴式耳机」）搜索时返回 0 结果的问题，现在会自动降级为关键词搜索确保结果正常返回。

## 原始内容

**Commit**: `a3b24a27e215f1b7481b25f5c468dd05151b00f6`
**仓库**: ecap-agent-pack
**作者**: christine-srp
**时间**: 2026-04-28T09:42:32Z

### 完整 Commit Message

```
fix(amazon-analyst): downgrade to keyword-only when categoryPath returns empty (#111)

Mirrors APIClaw-Skills #60: when --keyword and a deep-leaf --category are
both supplied (e.g. "Electronics > … > Over-Ear Headphones"), the
backend has no aggregation data for that exact leaf and markets/search
returns total=0. Without the fallback, the dead categoryPath propagates
to every downstream step in cmd_market_entry, so the entire 11-endpoint
report comes back empty.

After Step 1a, if markets/search came back failed/empty AND we have a
keyword to fall back to, drop categoryPath and rerun keyword-only. The
downgrade is recorded in results.meta.category_downgrade.

All 10 bundled apiclaw.py copies under amazon-analyst/.agents/skills/
get the same patch (sync-managed copies of the canonical script).

Reproduced via Kimi 2.5 driving amazon-analyst against "Over-Ear
Headphones" — the user-facing report ended up all-empty.

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #111 完整描述

## Summary

Mirrors the canonical fix in SerendipityOneInc/APIClaw-Skills#61.

When `--keyword` and a deep-leaf `--category` are both supplied (e.g. `Electronics > … > Over-Ear Headphones`), the backend has no aggregation data for that exact leaf and `markets/search` returns `total=0`. Without the fallback, the dead `categoryPath` propagates to every downstream step in `cmd_market_entry`, so the entire 11-endpoint report comes back empty.

After Step 1a, if `markets/search` came back failed/empty AND we have a keyword to fall back to, drop `categoryPath` and rerun keyword-only. The downgrade is recorded in `results.meta.category_downgrade`.

All 10 bundled `apiclaw.py` copies under `amazon-analyst/.agents/skills/` get the same patch (sync-managed copies of the canonical script).

## Why

Reproduced via Kimi 2.5 driving `amazon-analyst` against "Over-Ear Headphones" — the user-facing report ended up all-empty. Symptoms:

- `markets/search` → `total: 0`
- `products/*` → `HTTP 500`
- `reviews/analysis` → `INSUFFICIENT_REVIEWS (0 reviews)`

## Diff shape

- 10 files, +200 lines, -0 (pure additive 20-line fallback block in each copy's `cmd_market_entry`)
- No other changes

## Related

- Canonical fix: SerendipityOneInc/APIClaw-Skills#61
- Backend bug tracker (separate, server-side fix needed for full resolution): SerendipityOneInc/hermes-workspace#223
  — `/products/*` HTTP 500 on `keyword` containing `-` / `'` / `&` / `/` (Lucene reserved chars). Skill cannot strip these without changing search semantics.

## History note

This PR replaces #110 (closed). #110 was opened against a stale local ref before noticing that the amazon-analyst pack had already merged into `main` via #100 on 2026-04-23 — that PR ended up trying to re-introduce the entire pack on top of an outdated base, producing 44-file conflicts. This PR is a clean fix-only diff against the latest `main`.

## Test plan

- [x] Cherry-picked from the original fix commit (213cd70) — diff identical to what was reviewed in #110
- [x] APIClaw-Skills test suite for the canonical fix: 45/45 ✅
- [ ] Smoke run amazon-analyst end-to-end on the deep-leaf prompt that triggered the bug

🤖 Generated with [Claude Code](https://claude.com/claude-code)
