---
title: "修复 v2 Agent 模型选择显示不正确"
type: "Bug Fix"
priority: "中"
date: "2026-07-31"
status: "待审核"
channels: ""
---

## 核心宣传点

修复了 v2 Agent 模型选择在保存后回读显示为空的问题，现在所选模型能正确展示。

## 原始内容

**fix(chat): restore v2 model selection display (#3167)**

- SHA: `cbf32b25235c09cdd8c14be86d110a7e55866287`
- PR: #3167
- 日期: 2026-07-31T06:18:08Z

```
fix(chat): restore v2 model selection display (#3167)

## Summary

- Read the selected v2 Agent model from the Engine's current
`declared.model.primary` response shape.
- Keep `resource.model.primary` as a compatibility fallback for older
Engine responses.
- Return provider-free public model ids so `litellm/gpt-5.5` matches the
composer catalog entry `gpt-5.5`.
- Add the staging investigation report covering the readback defect and
the separate GPT streaming failure.

## Root cause

The Engine agent-detail contract moved the declared configuration from
`resource` to `declared`, while `claw-interface` continued reading only
`resource.model.primary`. Model updates therefore reached the Engine,
but subsequent GET requests returned `model_id: null` and the composer
lost its selected value after a refetch.

Once the response parser reads the current field, Engine model ids may
still carry a provider prefix such as `litellm/`. The public catalog
uses provider-free aliases, so the read path now removes the first
provider segment consistently for both `openai/` and `litellm/`.

The GPT `/v1/messages` streaming failure documented in the report is
separate and is not changed by this PR. It is tracked in
`SerendipityOneInc/zooclaw-engine#531`.

## Test plan

- [x] `pytest -q tests/unit/test_engine_client.py
tests/unit/test_agent_model_service.py` — 56 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] pre-commit and pre-push hooks
```

**PR Body:**

## Summary

- Read the selected v2 Agent model from the Engine's current `declared.model.primary` response shape.
- Keep `resource.model.primary` as a compatibility fallback for older Engine responses.
- Return provider-free public model ids so `litellm/gpt-5.5` matches the composer catalog entry `gpt-5.5`.
- Add the staging investigation report covering the readback defect and the separate GPT streaming failure.

## Root cause

The Engine agent-detail contract moved the declared configuration from `resource` to `declared`, while `claw-interface` continued reading only `resource.model.primary`. Model updates therefore reached the Engine, but subsequent GET requests returned `model_id: null` and the composer lost its selected value after a refetch.

Once the response parser reads the current field, Engine model ids may still carry a provider prefix such as `litellm/`. The public catalog uses provider-free aliases, so the read path now removes the first provider segment consistently for both `openai/` and `litellm/`.

The GPT `/v1/messages` streaming failure documented in the report is separate and is not changed by this PR. It is tracked in `SerendipityOneInc/zooclaw-engine#531`.

## Test plan

- [x] `pytest -q tests/unit/test_engine_client.py tests/unit/test_agent_model_service.py` — 56 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] pre-commit and pre-push hooks

