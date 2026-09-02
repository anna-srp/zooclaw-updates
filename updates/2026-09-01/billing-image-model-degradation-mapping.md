---
title: "修复：额度用尽后新版图片模型没有降级路线，生图直接失败"
type: "Bug Fix"
priority: "低"
date: "2026-09-01"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：额度用尽后新版图片模型没有降级路线，生图直接失败

## 核心宣传点

托管图片生成的默认模型换到了 `gemini-3.1-flash-image` 这个稳定别名，但计费侧的模型降级映射表里只登记了它的 `-preview` 预览别名。结果是额度耗尽的用户如果落到稳定版模型上，就找不到可降级的目标模型。现在把稳定别名也加进降级映射（降级到 `hunyuan-image-3`），与既有的预览版条目并存。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `90d9bbb6609eac5b843dc35362cde9a6fb8f5a3f`
- PR: #3601
- 作者: sharplee-srp
- 日期: 2026-09-01T09:25:11Z

### Commit Message

```
fix(billing): add stable gemini-3.1-flash-image to image degradation mapping (#3601)

## Summary
- Add the stable `gemini-3.1-flash-image` alias to
`MODEL_DEGRADATION_MAPPINGS` (→ `hunyuan-image-3`), alongside the
existing `-preview` entry.
- Pin it in `test_tier_writer.py`'s image-model degradation check.

## Root cause
zooclaw-engine PR
[#999](https://github.com/SerendipityOneInc/zooclaw-engine/pull/999)
changes the v2 managed image-generation default to `gpt-image-2` →
`gemini-3.1-flash-image` (stable Vertex alias; already registered on
staging LiteLLM with `starter/pro/ultra-image_generation` access
groups). The degradation table only knew the preview alias, so a
credits-depleted user whose image call fell through to the stable model
would have no degradation route.

## Test plan
- [x] `ruff check` / `ruff format --check` on the two files
- [x] `pytest tests/unit/test_tier_writer.py
tests/unit/test_plan_models.py` — 50 passed

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01KK2cYPdkCp1Uxnzb2konn8

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

```
## Summary
- Add the stable `gemini-3.1-flash-image` alias to `MODEL_DEGRADATION_MAPPINGS` (→ `hunyuan-image-3`), alongside the existing `-preview` entry.
- Pin it in `test_tier_writer.py`'s image-model degradation check.

## Root cause
zooclaw-engine PR [#999](https://github.com/SerendipityOneInc/zooclaw-engine/pull/999) changes the v2 managed image-generation default to `gpt-image-2` → `gemini-3.1-flash-image` (stable Vertex alias; already registered on staging LiteLLM with `starter/pro/ultra-image_generation` access groups). The degradation table only knew the preview alias, so a credits-depleted user whose image call fell through to the stable model would have no degradation route.

## Test plan
- [x] `ruff check` / `ruff format --check` on the two files
- [x] `pytest tests/unit/test_tier_writer.py tests/unit/test_plan_models.py` — 50 passed

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01KK2cYPdkCp1Uxnzb2konn8

```
