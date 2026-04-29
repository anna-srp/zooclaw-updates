---
title: "语音识别支持实时取消（后端 WebSocket 协议）"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 语音识别支持实时取消（后端 WebSocket 协议）

## 核心宣传点

语音识别 WebSocket 协议新增取消指令支持，配合 iOS 客户端实现更流畅的录音取消体验。

## 原始内容

**Commit**: `6b75dff917361f01a15ab5255b5521fcac27abcc`
**仓库**: ecap-workspace
**作者**: bill-srp
**时间**: 2026-04-28T06:54:47Z

### 完整 Commit Message

```
feat(claw-interface): Add cancel control message to ASR realtime WebSocket (#1428)

## Summary

iOS can now abandon an in-flight realtime ASR recording by sending
`{"type":"cancel"}` over the WebSocket. The server commits the upstream
buffer to keep the persistent vllm-asr session in sync (vllm-asr does
not implement `input_audio_buffer.clear`), drops the resulting
transcript, replies with `{"type":"cancelled"}`, and resets so the next
audio chunk opens a fresh buffer on the same upstream connection.

**Protocol**
- New control: `{"type":"cancel"}` from client → `{"type":"cancelled"}`
ack from server
- No `final` is sent; `enhance`/`rewrite` are not invoked
- Subsequent audio chunks reuse the open upstream WS and start a new
`input_audio_buffer.commit` (without `final`) — same lazy-buffer-start
path the first recording uses

**Implementation**
- `UpstreamASRClient.cancel()` — sends `input_audio_buffer.commit,
final: true`, drains the response stream via the existing
`_collect_transcription` helper, discards the text, swallows
`UpstreamError` (best-effort)
- `_handle_cancel` route handler — calls `upstream.cancel()`, acks
client, then `session.reset()` + `upstream.reset()`
- WS docstring updated with the new control message

**Tests**
- 6 unit tests for `UpstreamASRClient.cancel()` covering commit-frame
emission, transcript discard, buffer-state reset, error swallow, and
no-op cases
- 6 unit tests for the route's cancel branch covering ack, no-`final`
guarantee, no enhance/rewrite call, upstream `cancel`+`reset`, no-audio
cancel, and follow-up recording producing a fresh result
- 2 BDD scenarios in `tests/bdd/features/asr.feature` driven through a
real WebSocket via starlette `TestClient` with an in-memory
`_FakeUpstream`

## Test plan

- [ ] CI green: `python-code-quality / build-and-test` (ruff + pyright +
pytest)
- [ ] BDD: with MongoDB up, `TEST_MONGODB_HOST=127.0.0.1 MONGODB_USER=
MONGODB_PASSWORD= pytest tests/bdd/step_defs/test_asr_realtime.py`
- [ ] iOS smoke: start a recording, send `{"type":"cancel"}` mid-stream,
verify `{"type":"cancelled"}` is received and the next recording
produces only the new transcript
- [ ] Idempotent cancel: send `cancel` before any audio chunks, verify
single `cancelled` ack

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR #1428 完整描述

## Summary

iOS can now abandon an in-flight realtime ASR recording by sending `{"type":"cancel"}` over the WebSocket. The server commits the upstream buffer to keep the persistent vllm-asr session in sync (vllm-asr does not implement `input_audio_buffer.clear`), drops the resulting transcript, replies with `{"type":"cancelled"}`, and resets so the next audio chunk opens a fresh buffer on the same upstream connection.

**Protocol**
- New control: `{"type":"cancel"}` from client → `{"type":"cancelled"}` ack from server
- No `final` is sent; `enhance`/`rewrite` are not invoked
- Subsequent audio chunks reuse the open upstream WS and start a new `input_audio_buffer.commit` (without `final`) — same lazy-buffer-start path the first recording uses

**Implementation**
- `UpstreamASRClient.cancel()` — sends `input_audio_buffer.commit, final: true`, drains the response stream via the existing `_collect_transcription` helper, discards the text, swallows `UpstreamError` (best-effort)
- `_handle_cancel` route handler — calls `upstream.cancel()`, acks client, then `session.reset()` + `upstream.reset()`
- WS docstring updated with the new control message

**Tests**
- 6 unit tests for `UpstreamASRClient.cancel()` covering commit-frame emission, transcript discard, buffer-state reset, error swallow, and no-op cases
- 6 unit tests for the route's cancel branch covering ack, no-`final` guarantee, no enhance/rewrite call, upstream `cancel`+`reset`, no-audio cancel, and follow-up recording producing a fresh result
- 2 BDD scenarios in `tests/bdd/features/asr.feature` driven through a real WebSocket via starlette `TestClient` with an in-memory `_FakeUpstream`

## Test plan

- [ ] CI green: `python-code-quality / build-and-test` (ruff + pyright + pytest)
- [ ] BDD: with MongoDB up, `TEST_MONGODB_HOST=127.0.0.1 MONGODB_USER= MONGODB_PASSWORD= pytest tests/bdd/step_defs/test_asr_realtime.py`
- [ ] iOS smoke: start a recording, send `{"type":"cancel"}` mid-stream, verify `{"type":"cancelled"}` is received and the next recording produces only the new transcript
- [ ] Idempotent cancel: send `cancel` before any audio chunks, verify single `cancelled` ack

🤖 Generated with [Claude Code](https://claude.com/claude-code)
