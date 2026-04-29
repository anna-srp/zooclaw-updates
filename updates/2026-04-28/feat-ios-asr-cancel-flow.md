---
title: "iOS 语音识别支持取消正在进行中的录音"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# iOS 语音识别支持取消正在进行中的录音

## 核心宣传点

iOS 用户现在可以在语音识别进行中取消录音，避免误触导致无法终止的问题。

## 原始内容

**Commit**: `57606deb1c9102fabd4757e92d16462615a70a7f`
**仓库**: ecap-workspace
**作者**: bill-srp
**时间**: 2026-04-28T11:14:19Z

### 完整 Commit Message

```
feat(ios): add ASR cancel flow with late-frame and audio-race guards (#1443)

## Summary

Wires up the iOS side of the ASR cancel flow that pairs with the backend
cancel control message added in #1428. Cancel now reaches the ASR
WebSocket, late frames after cancel no longer leak into the input, and
the recording UI returns to wherever the user came from.

### Changes

- **UX:** `Cancel` from the recording panel now returns to the
originating panel (text input vs. voice idle) instead of always dropping
back to voice idle. Recording UI extracted from `VoiceInputPanel` into a
new `RecordingPanel` to make ownership of recording-state explicit.
- **Protocol:** When the user cancels, the client sends a `cancel` event
over the ASR WebSocket so the server stops billing/processing
immediately (consumes #1428).
- **Late-frame guard:** Final-text frames that arrive after a cancel —
or while the user has already started a new recording — are dropped
instead of being committed to the input.
- **Audio race fix:** Outgoing ASR audio is now serialized behind any
in-flight cancel so the very first audio chunk of a new recording can't
be sent on the previous (cancelling) socket and lost.
- **Tests:** New `VoiceInputCoordinatorTests` covering the cancel paths
plus updated edge-case test for the tightened transcribing-only guard.

## How to test

1. Open chat, tap voice → start recording → **Cancel** while transcript
is still streaming. Expect: returned to whichever panel started the
recording (text or voice idle), no transcript text committed.
2. Cancel mid-recording, then immediately start a new recording. Expect:
no leading audio dropped, no late text from the previous session
appearing in the new transcript.
3. Server side: confirm a `cancel` event is observed on the ASR
WebSocket when the user cancels (via #1428).

## Related

- Backend counterpart: #1428 (ASR realtime WebSocket cancel control
message)

## Checklist

- [x] Conventional commit format on title and commits
- [x] Unit tests added for new behavior (`VoiceInputCoordinatorTests`,
edge cases updated)
- [ ] Manual device verification of golden + race paths
```

### PR #1443 完整描述

## Summary

Wires up the iOS side of the ASR cancel flow that pairs with the backend cancel control message added in #1428. Cancel now reaches the ASR WebSocket, late frames after cancel no longer leak into the input, and the recording UI returns to wherever the user came from.

### Changes

- **UX:** `Cancel` from the recording panel now returns to the originating panel (text input vs. voice idle) instead of always dropping back to voice idle. Recording UI extracted from `VoiceInputPanel` into a new `RecordingPanel` to make ownership of recording-state explicit.
- **Protocol:** When the user cancels, the client sends a `cancel` event over the ASR WebSocket so the server stops billing/processing immediately (consumes #1428).
- **Late-frame guard:** Final-text frames that arrive after a cancel — or while the user has already started a new recording — are dropped instead of being committed to the input.
- **Audio race fix:** Outgoing ASR audio is now serialized behind any in-flight cancel so the very first audio chunk of a new recording can't be sent on the previous (cancelling) socket and lost.
- **Tests:** New `VoiceInputCoordinatorTests` covering the cancel paths plus updated edge-case test for the tightened transcribing-only guard.

## How to test

1. Open chat, tap voice → start recording → **Cancel** while transcript is still streaming. Expect: returned to whichever panel started the recording (text or voice idle), no transcript text committed.
2. Cancel mid-recording, then immediately start a new recording. Expect: no leading audio dropped, no late text from the previous session appearing in the new transcript.
3. Server side: confirm a `cancel` event is observed on the ASR WebSocket when the user cancels (via #1428).

## Related

- Backend counterpart: #1428 (ASR realtime WebSocket cancel control message)

## Checklist

- [x] Conventional commit format on title and commits
- [x] Unit tests added for new behavior (`VoiceInputCoordinatorTests`, edge cases updated)
- [ ] Manual device verification of golden + race paths
