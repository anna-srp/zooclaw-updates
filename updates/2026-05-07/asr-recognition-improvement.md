---
title: "语音识别准确率提升：产品名词识别更准"
type: "体验优化"
priority: "中"
date: "2026-05-07"
status: "待审核"
channels: ""
---
# 语音识别准确率提升：产品名词识别更准

## 核心宣传点
语音识别现在能更准确地识别"ZooClaw"、"OpenClaw"等专有名词，减少谐音误识别，语音输入体验更流畅。

## 原始内容

### Commit Message
```
feat(asr): add default prompt to bias upstream recognition (#1559)
```

### PR Description
## Summary
- Forward a configurable default prompt (`ZooClaw, OpenClaw, Claude`) to upstream Qwen3-ASR on **both** transports:
  - HTTP `POST /v1/audio/transcriptions` — multipart `prompt` form field
  - Realtime WebSocket — `session.update` payload
- Biases recognition toward product-specific proper nouns prone to homophone misrecognition.
- Override via env var `ASR_DEFAULT_PROMPT`.
- Drive-by: bump default `ASR_BASE_URL` domain from `g.yesy.dev` → `g.yesy.online` (separate commit).

## Test plan
- [x] `pytest tests/unit/test_asr_upstream_client.py tests/unit/test_asr_service.py tests/unit/test_settings.py` — 74 passed locally
- [ ] Manual smoke: realtime ASR session resolves `ZooClaw` / `OpenClaw` / `Claude` correctly on near-homophone audio
