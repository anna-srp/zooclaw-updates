---
title: "修复：会话串里发出的截图 Agent 看不到，现已作为真实附件上传"
type: "Bug Fix"
priority: "高"
date: "2026-10-23"
status: "待审核"
channels: ""
---

# 修复：会话串里发出的截图 Agent 看不到，现已作为真实附件上传

## 核心宣传点

有客户的 Agent 收不到用户在网页会话串里发送的截图：引擎侧收到的消息附件数为 0，Agent 按消息里粘贴的链接去取图还会被存储服务拒绝授权。根因是输入框组件只有在显式传入上传覆盖参数时才会把文件作为聊天附件上传，否则会退化成把图片塞进用户图片桶、再往消息正文里插入一条长达数百字符的带签名临时链接；主聊天页传了该参数，而会话串页面和 Agent 工作区的任务/构建页从来没传。修复后这些入口的输入框上传也统一作为真实附件进入会话线程，Agent 能直接读到图片而不依赖会过期的链接。

## 分级

- 内部：P1
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `9a8b2b7e7b03fbfee0009408e6e49f1827ef296a`
- PR: #4132
- 作者：engineering-agent-srp
- 日期：2026-10-23T10:36:12Z

### Commit Message

```
fix(chat): attach composer uploads as Mattermost files in session threads (#4132)

## Problem

A customer's agent (ULTRA_1 / `agt_01m27r804mg5k7jnjrjyfhbzdw`) could
not see screenshots sent from the web session thread. The engine
received the posts with **0 attachments**, and the agent's `image` fetch
of the pasted link got R2 `401 Unauthorized`.

## Root cause

`GenClawInput` only uploads composer files as Mattermost files when
`uploadOverride` is passed. Otherwise it falls back to uploading into
the R2 user-image bucket and inserting `![image.png](<7-day presigned
GET URL>)` (~460 chars) into the message text.

- `ChatBody` (main `/chat`) passes `uploadOverride` while MM is
connected.
- `SessionThreadClient` (`/chat/{workspaceId}/sessions/{sessionId}`) and
`AgentWorkspaceClient` (`/agents/{workspaceId}` task/build) never wired
`useMmAttachments`, so **every** image from these surfaces goes down the
link fallback.

The agent then has to hand-copy the presigned URL into a tool call. The
engine already documents that models garble these (`media-inputs.ts`,
`r2://` short reference, #292). A corrupted `X-Amz-Credential` access
key gives R2 401, which matches the agent's report. (The exact URL the
agent used was not captured; this part is inferred.)

## Fix

- `useSessionThreadChat` now owns a `useMmAttachments` instance bound to
the thread channel and the user's MM token. It exposes
`composerAttachments` (`uploadOverride`, `attachExistingFile`,
`mmAttachments`, remove/retry, `isMmUploading`).
- `sendThreadMessage` sends only finished uploads still shown in the
composer as `file_ids` (same filtering as
`useChatMessaging.sendMMMessage`). It clears the composer on success and
keeps the ids for retry on failure or a no-op send.
- `useSendThreadReply.send` / `postThreadReply` accept image-only
replies when file ids are present. The composer already enables Send for
attachments with no text.
- Wired into `SessionThreadClient` and `AgentWorkspaceClient`. Read-only
Legacy and External surfaces are unchanged.
- `hasRevision` / `canEditDefinition` moved to
`lib/revision-presentation.ts` with no behavior change, to keep
`useViewModel.ts` under the 600-line limit.

## Verification

- New tests fail on `main` (4) and pass with this change:
- `useSessionThreadChat`: exposes `uploadOverride`; sends file ids,
including image-only; clears on success; keeps ids on failure.
  - `useSendThreadReply`: forwards file ids, image-only.
  - `postThreadReply`: image-only reply with file ids.
- `scripts/verify-web.sh <changed files>`: guards ✓, vitest 191 ✓,
eslint ✓. Also `tests/unit/app/agents`: 542 ✓.
- ⚠️ `tsc --noEmit` could not finish locally (OOM in a small sandbox).
Relying on CI `web-quality`.
- Not yet validated in a browser or on staging. After deploy: send a
screenshot from a session thread, then confirm the post has `file_ids`
and the engine inbound message has 1 attachment.

## Notes

- Mattermost retirement is in progress but not on `main`. This is a
small fix on the current transport.
- Follow-up options not in this PR: `SubagentChatPanel` still always
uses the link fallback. A server-side "own-bucket presigned link →
attachment" path in ACS or the engine would remove the copy-the-URL
dependency regardless of transport.

---------

Co-authored-by: zoowork-engineering-agent <326424865+zoowork-engineering-agent@users.noreply.github.com>
Co-authored-by: finn-srp <finn@srp.one>
Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

