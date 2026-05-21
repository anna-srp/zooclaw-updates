---
title: "图片生成失败时自动切换到混元图片3作为备用模型"
type: "产品基础功能更新"
priority: "高"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "5d5d8acddc2ce011240e27c795f9d1cbc3e65231"
pr: 1758
---
# 图片生成失败时自动切换到混元图片3作为备用模型

## 核心宣传点

图片生成遇到错误时，系统现在会自动降级使用混元图片3（Hunyuan Image 3）模型，减少生成失败情况，提升成功率。

## 原始内容

### Commit Message

```
fix(eca-736): route image-gen fallback to hunyuan-image-3 (#1758)

## Summary

Flip `_IMAGE_FALLBACK` in
`services/claw-interface/app/services/plan_models.py` from
`zooclaw-img-model` to `hunyuan-image-3`. Degraded users' image-gen
calls now go to a chat-capable model that returns the shape designer's
CLI expects.

**Depends on:**
[hunyuan3img-online#4](https://github.com/SerendipityOneInc/hunyuan3img-online/pull/4)
— that PR adds the `/v1/chat/completions` endpoint on `hunyuan-image-3`
and is **already deployed to production** (image `doks-v0.0.6-release`,
gem-production rollout verified). Designer-style end-to-end via prod
LiteLLM (`https://litellm.vllm.yesy.online`) passes for both
text-to-image and image-to-image. Safe to merge this PR at any time.

## Why

When a user's team is degraded, the LiteLLM `TierDegradationHandler`
rewrites `data["model"]` in-place from e.g. `gemini-2.5-flash-image` to
whatever `_IMAGE_FALLBACK` resolves to. Today that's `zooclaw-img-model`
(`Tongyi-MAI/Z-Image-Turbo` on vllm-omni). vllm-omni's
`/v1/chat/completions` returns `message.content` as a list of multimodal
parts (`[{"type":"image_url",...}]`) — but LiteLLM's `Message.content:
Optional[str]` Pydantic field rejects lists, so the whole response fails
to parse and bubbles up as `APIConnectionError: Invalid response
object`. The designer CLI exits non-zero and Stylist tells the user it
can't generate.

Switching the fallback to `hunyuan-image-3`
(HunyuanImage-3.0-Instruct-Distil, now with a `/v1/chat/completions`
endpoint that returns `content: str` + `images: [{"type": "image_url",
"image_url": {"url": "data:..."}}]`) fixes the validator crash AND
preserves designer's existing response-reading code (`getattr(message,
"images", None)` at `image_generation_cli.py:419`).

## Changes

- `services/claw-interface/app/services/plan_models.py:180` — one-line
constant flip (`_IMAGE_FALLBACK = "hunyuan-image-3"`)
- `services/claw-interface/tests/unit/test_tier_writer.py` — new
regression test
`test_mappings_have_expected_image_entries_routed_to_hunyuan` asserting
all seven image models (gemini-*-image-*, gpt-image-*, grok-imagine-*)
route to `hunyuan-image-3`

## Test plan

- [x] `pytest
tests/unit/test_tier_writer.py::TestSyncDegradationMappings -v` — new
test fails before fix (assertion: `routes to 'zooclaw-img-model';
expected hunyuan-image-3`), passes after
- [x] `ruff check + ruff format --check` on touched files — clean
- [ ] Post-merge: trigger a degraded chat-completion against a Gemini
image model via the staging LiteLLM proxy and confirm an image is
returned (already proven against prod hunyuan endpoint directly; this
would confirm the Redis-sync + degradation-hook path)

Closes ECA-736.
```

### PR Description

## Summary

Flip `_IMAGE_FALLBACK` in `services/claw-interface/app/services/plan_models.py` from `zooclaw-img-model` to `hunyuan-image-3`. Degraded users' image-gen calls now go to a chat-capable model that returns the shape designer's CLI expects.

**Depends on:** [hunyuan3img-online#4](https://github.com/SerendipityOneInc/hunyuan3img-online/pull/4) — that PR adds the `/v1/chat/completions` endpoint on `hunyuan-image-3` and is **already deployed to production** (image `doks-v0.0.6-release`, gem-production rollout verified). Designer-style end-to-end via prod LiteLLM (`https://litellm.vllm.yesy.online`) passes for both text-to-image and image-to-image. Safe to merge this PR at any time.

## Why

When a user's team is degraded, the LiteLLM `TierDegradationHandler` rewrites `data["model"]` in-place from e.g. `gemini-2.5-flash-image` to whatever `_IMAGE_FALLBACK` resolves to. Today that's `zooclaw-img-model` (`Tongyi-MAI/Z-Image-Turbo` on vllm-omni). vllm-omni's `/v1/chat/completions` returns `message.content` as a list of multimodal parts (`[{"type":"image_url",...}]`) — but LiteLLM's `Message.content: Optional[str]` Pydantic field rejects lists, so the whole response fails to parse and bubbles up as `APIConnectionError: Invalid response object`. The designer CLI exits non-zero and Stylist tells the user it can't generate.

Switching the fallback to `hunyuan-image-3` (HunyuanImage-3.0-Instruct-Distil, now with a `/v1/chat/completions` endpoint that returns `content: str` + `images: [{"type": "image_url", "image_url": {"url": "data:..."}}]`) fixes the validator crash AND preserves designer's existing response-reading code (`getattr(message, "images", None)` at `image_generation_cli.py:419`).

## Changes

- `services/claw-interface/app/services/plan_models.py:180` — one-line constant flip (`_IMAGE_FALLBACK = "hunyuan-image-3"`)
- `services/claw-interface/tests/unit/test_tier_writer.py` — new regression test `test_mappings_have_expected_image_entries_routed_to_hunyuan` asserting all seven image models (gemini-*-image-*, gpt-image-*, grok-imagine-*) route to `hunyuan-image-3`

## Test plan

- [x] `pytest tests/unit/test_tier_writer.py::TestSyncDegradationMappings -v` — new test fails before fix (assertion: `routes to 'zooclaw-img-model'; expected hunyuan-image-3`), passes after
- [x] `ruff check + ruff format --check` on touched files — clean
- [ ] Post-merge: trigger a degraded chat-completion against a Gemini image model via the staging LiteLLM proxy and confirm an image is returned (already proven against prod hunyuan endpoint directly; this would confirm the Redis-sync + degradation-hook path)

Closes ECA-736.
