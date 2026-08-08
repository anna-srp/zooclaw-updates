---
title: "模型选择器 TTS 名称显示修复"
type: "Bug Fix"
priority: "低"
date: "2026-08-07"
status: "待审核"
channels: ""
---

## 核心宣传点

聊天与设置里的模型列表不再把 TTS 显示成 Tts，模型名称展示统一正确。

## 原始内容

### fix(models): preserve TTS acronym in chat catalog (#3298)

- SHA: `0ec6937eebe1f69d4d917227d9aa684c2ede8612`
- 仓库: 见 raw/2026-08-07

**Commit Message:**

```
fix(models): preserve TTS acronym in chat catalog (#3298)

## What changed

- treat `tts` as an acronym in the chat model catalog fallback formatter
- add a regression test for `gemini-3.1-flash-tts-preview`

## Root cause

The settings UI formatter already preserved `TTS`, but the
claw-interface catalog fallback formatter did not include `tts` in its
acronym set. The chat composer therefore displayed `Tts` when LiteLLM
did not provide a display name.

## Impact

Settings and chat model pickers now consistently display `Gemini 3.1
Flash TTS Preview`.

## Validation

- `pytest tests/unit/test_model_catalog.py -q`: 14 passed
- Ruff check and format check
- Pyright: 0 errors
- `git diff --check`
```

**PR Body:**

## What changed

- treat `tts` as an acronym in the chat model catalog fallback formatter
- add a regression test for `gemini-3.1-flash-tts-preview`

## Root cause

The settings UI formatter already preserved `TTS`, but the claw-interface catalog fallback formatter did not include `tts` in its acronym set. The chat composer therefore displayed `Tts` when LiteLLM did not provide a display name.

## Impact

Settings and chat model pickers now consistently display `Gemini 3.1 Flash TTS Preview`.

## Validation

- `pytest tests/unit/test_model_catalog.py -q`: 14 passed
- Ruff check and format check
- Pyright: 0 errors
- `git diff --check`


