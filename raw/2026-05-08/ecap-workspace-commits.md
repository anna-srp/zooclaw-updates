# ecap-workspace Commits — 2026-05-08

## Commit 0a4f118f

- **SHA:** 0a4f118f
- **Author:** sam-srp
- **Date:** 2026-05-08T07:58:11Z
- **PR:** #1572

### Full Commit Message

```
fix(web): surface componentStack to Sentry from chat ErrorBoundary (#1572)

## Summary
- `ChatErrorBoundary` auto-recovers render crashes by remounting children with a fresh `key`.
  It currently only `logger.warn`s, so any error caught here — including
  the recurring `Maximum update depth exceeded` (React #185) — never
  reaches Sentry. We've been blind to which component is looping.
- Add a throttled `captureChatError('render_recovery', ...)` call that
  includes `componentStack` and a `recoveryCount`. The 2s/per-message
  throttle prevents a render loop (50+ throws/sec) from flooding the local
  breadcrumb buffer and crowding out the actual cause.
- Improve the global `ErrorBoundary`: add `tags.boundary = 'global'`
  and mirror `componentStack` into `extra` so it's visible in Sentry's
  issue list view, not just inside the React context tab.

No behavior change for users — auto-recovery flow in `ChatErrorBoundary`
is preserved.
```

### PR #1572 Body

Full PR body describes Sentry error tracking improvements for chat ErrorBoundary.
No user-facing behavior change.

---

**筛选结果：❌ 仅保留 raw（Sentry/日志/监控噪音，用户无感知）**

---

## Commit 13d0a4f0

- **SHA:** 13d0a4f0
- **Author:** kaka-srp
- **Date:** 2026-05-08T07:13:32Z
- **PR:** #1573

### Full Commit Message

```
feat(agents): agent-studio uses 1/10 sonnet, hide from picker (#1573)

## Summary

Two threads, both centered on Linear ECA-636's "Agent Studio gets a 1/10-priced Sonnet variant":

1. Wire `agent-studio-sonnet-4-6` into the `agent_studio` builtin
agent at hire time. `apply_agents_list` now reads `meta["model"]` from
the catalog row and writes `{"primary": "openai/agent-studio-sonnet-4-6"}`
into the per-agent entry.

2. Consolidate the user-facing model-id filter on the backend. New
`INTERNAL_MODEL_IDS` (exact) + `INTERNAL_MODEL_SUBSTRINGS`
(case-insensitive) constants in `plan_models.py` plus
`is_internal_model` / `filter_internal_models` helpers. Both
`resolve_models_by_type` and `resolve_models_for_plan` apply the filter,
so the `/openclaw/settings` `available_models` payload and the
`update_model` validation see the same hidden list. Two duplicate
frontend `embedding` filters deleted now that the backend is canonical.

End-to-end verified on staging: hired `agent_studio` for a test account,
confirmed the model id flowed all the way to openclaw.json on the bot pod.
```

### PR #1573 Body

Wires 1/10-priced Sonnet model (agent-studio-sonnet-4-6) into Agent Studio agent.
Backend model filtering consolidated. Agent Studio hidden from user model picker.
Cost optimization: Agent Studio now uses a dedicated model at 1/10 the standard price.

---

**筛选结果：✅ 写入 updates/（费用/性能显著改善，用户可感知的成本优化）**
