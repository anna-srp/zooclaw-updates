---
title: "PPT Master 套用模板时封面图直接作为对话附件送达"
type: "体验优化"
priority: "中"
date: "2026-06-16"
status: "待审核"
channels: ""
---
# PPT Master 套用模板时封面图直接作为对话附件送达
## 核心宣传点
在 PPT Master 中「Remix 套用」模板时，模板封面图会作为真实附件直接发给智能体，生成效果更贴合所选模板。
## 原始内容
feat(landing-context): deliver PPT Master Remix cover image as a chat attachment (#2466)

## What

Completes the **PPT Master "Remix"** hand-off on the chat side: a picked
template's **cover screenshot** is now delivered to the agent as a real
Mattermost **attachment** (not just a URL in the prompt text), sent
imperceptibly through the existing landing auto-send flow.

Producer side ships in `zooclaw-tips`
(SerendipityOneInc/zooclaw-tips#54): the gallery writes
`initial_query.images = [coverUrl]` + `auto_send` into
`ecap:landingContext`. This PR makes the consumer honor both.

Two commits:

1. **Carry the contract** — `landing-context.ts` previously rebuilt the
stored context as `initial_query: { text }` only, silently dropping any
producer-supplied `images` / `auto_send`. Now both are preserved
(sanitized: string-only image entries, capped at 8; `auto_send` accepts
only literal `true`), attached only when present so text-only hand-offs
keep their minimal shape.
2. **Deliver the images** — wire `initial_query.images` through the
auto-send path so they upload + attach to the message.

## How

- `blob.ts` — `fetchExternalBlob()` pulls a third-party image
**without** bearer auth (never leak the MM token to a foreign origin;
subject to the remote's CORS).
- `useMmAttachments` — `uploadExternalImageUrls()` fetches each URL,
uploads to the channel, returns file ids; isolated from the composer's
attachment UI state (the message is programmatic, no preview chips).
- `useChatMessaging` — `handleSendMessage()` accepts explicit `fileIds`
(bypasses the render-lagged attachment-state consumption that would drop
a same-tick upload); `handleSendMessageWithImages()` uploads then sends
text + ids.
- `useLandingContextFlow` / `GenClawClient` — thread images through
`onAutoSendInitialQuery`, passing them only when present.

## Notes

- **Best-effort images**: if every upload fails (CORS, network), it
falls back to sending text alone — the cover URL is already embedded in
the prompt text, so the agent isn't left empty-handed.
- **CORS caveat**: browser must fetch the image bytes to re-upload, so
delivery depends on the image origin's CORS. `raw.githubusercontent.com`
returns `ACAO:*` (works); other origins without CORS headers degrade to
text-only. A server-side proxy would remove this dependency (out of
scope here).

## Test

- `tsc --noEmit` clean.
- 132 unit tests pass across `landing-context`, `useMmAttachments`,
`useChatMessaging`, `useLandingContextFlow` (incl. new images-carry +
images-forwarding tests).

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---

## PR Description

## What

Completes the **PPT Master "Remix"** hand-off on the chat side: a picked template's **cover screenshot** is now delivered to the agent as a real Mattermost **attachment** (not just a URL in the prompt text), sent imperceptibly through the existing landing auto-send flow.

Producer side ships in `zooclaw-tips` (SerendipityOneInc/zooclaw-tips#54): the gallery writes `initial_query.images = [coverUrl]` + `auto_send` into `ecap:landingContext`. This PR makes the consumer honor both.

Two commits:

1. **Carry the contract** — `landing-context.ts` previously rebuilt the stored context as `initial_query: { text }` only, silently dropping any producer-supplied `images` / `auto_send`. Now both are preserved (sanitized: string-only image entries, capped at 8; `auto_send` accepts only literal `true`), attached only when present so text-only hand-offs keep their minimal shape.
2. **Deliver the images** — wire `initial_query.images` through the auto-send path so they upload + attach to the message.

## How

- `blob.ts` — `fetchExternalBlob()` pulls a third-party image **without** bearer auth (never leak the MM token to a foreign origin; subject to the remote's CORS).
- `useMmAttachments` — `uploadExternalImageUrls()` fetches each URL, uploads to the channel, returns file ids; isolated from the composer's attachment UI state (the message is programmatic, no preview chips).
- `useChatMessaging` — `handleSendMessage()` accepts explicit `fileIds` (bypasses the render-lagged attachment-state consumption that would drop a same-tick upload); `handleSendMessageWithImages()` uploads then sends text + ids.
- `useLandingContextFlow` / `GenClawClient` — thread images through `onAutoSendInitialQuery`, passing them only when present.

## Notes

- **Best-effort images**: if every upload fails (CORS, network), it falls back to sending text alone — the cover URL is already embedded in the prompt text, so the agent isn't left empty-handed.
- **CORS caveat**: browser must fetch the image bytes to re-upload, so delivery depends on the image origin's CORS. `raw.githubusercontent.com` returns `ACAO:*` (works); other origins without CORS headers degrade to text-only. A server-side proxy would remove this dependency (out of scope here).

## Test

- `tsc --noEmit` clean.
- 132 unit tests pass across `landing-context`, `useMmAttachments`, `useChatMessaging`, `useLandingContextFlow` (incl. new images-carry + images-forwarding tests).

