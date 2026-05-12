---
title: "Agent Studio 成本大幅优化，运行费用降至原来 1/10"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-08"
status: "待审核"
channels: "Discord, changelog"
---

# Agent Studio 成本大幅优化，运行费用降至原来 1/10

## 核心宣传点

Agent Studio 现已使用专属低价模型，运行成本降至原来的 1/10，让你用更低的费用构建和调试 Agent。

## 原始内容

**Commit:** 13d0a4f0  
**PR:** #1573  
**作者:** kaka-srp  
**日期:** 2026-05-08

```
feat(agents): agent-studio uses 1/10 sonnet, hide from picker (#1573)

## Summary

Two threads, both centered on Linear ECA-636's "Agent Studio gets a 1/10-priced Sonnet variant":

1. Wire `agent-studio-sonnet-4-6` into the `agent_studio` builtin
agent at hire time. `apply_agents_list` now reads `meta["model"]` from
the catalog row and writes `{"primary": "openai/agent-studio-sonnet-4-6"}`
into the per-agent entry. Catalog row in code (`LEGACY_OFFICIAL_AGENT_MAP`)
gains the field; the staging Mongo row was already patched manually before
this PR (prod still owes the same PATCH /openclaw/internal/agent-catalog/agent_studio).

2. Consolidate the user-facing model-id filter on the backend. New
`INTERNAL_MODEL_IDS` (exact) + `INTERNAL_MODEL_SUBSTRINGS`
(case-insensitive) constants in `plan_models.py` plus
`is_internal_model` / `filter_internal_models` helpers. Both
`resolve_models_by_type` and `resolve_models_for_plan` apply the filter,
so the `/openclaw/settings` `available_models` payload and the
`update_model` validation see the same hidden list. Two duplicate
frontend `embedding` filters (`ModelSection.tsx`, `AgentModelSection.tsx`)
deleted now that the backend is canonical.

End-to-end verified on staging: hired `agent_studio` for a test account,
confirmed the model id flowed all the way to /home/node/.openclaw/openclaw.json
on the bot pod, observed the OpenClaw runtime fallback chain via
[model-fallback/decision] logs, then confirmed the discount price after
LiteLLM team-group access was added by the platform team.
```

**PR #1573 Description:**

Wires 1/10-priced Sonnet model (`agent-studio-sonnet-4-6`) into Agent Studio agent. Backend model filtering consolidated so internal models are hidden from the user model picker. Agent Studio now uses a dedicated model at 1/10 the standard Claude Sonnet price. Cost optimization: significant reduction in Agent Studio operational costs for ZooClaw and users.
