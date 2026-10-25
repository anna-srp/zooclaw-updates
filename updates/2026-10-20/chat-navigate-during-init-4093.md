---
title: "发起对话/创建 Agent 后立即进入页面，不用再等首条消息发完"
type: "体验优化"
priority: "高"
date: "2026-10-20"
status: "待审核"
channels: ""
---

# 发起对话/创建 Agent 后立即进入页面，不用再等首条消息发完

## 核心宣传点

以前从首页、新任务或创建 Agent 发送内容时，页面要等整条首消息链路（会话绑定、上传、投递）跑完才跳转，等待感明显。现在接口一返回任务/会话或 Agent 工作区就立刻打开目标页，已提交的文字和附件名在后台完成初始化期间保持可见。失败时会保留原有的创建身份和已上传文件，投递前或被明确拒绝后可以在目标页直接改文案、删附件、重试或丢弃草稿；状态不确定的发送则锁定原始内容等待对账。Agent 列表在创建成功后后台刷新，即使首条消息投递失败也能找到新建的 Agent，且刷新不阻塞跳转。

## 分级

- 内部：P1
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `ea2682be24e4f359bc03f70bfe8e2b470f9a8a96`
- PR: #4093
- 作者：Nemo Feng
- 日期：2026-10-20T00:06:55Z

### Commit Message

```
fix(chat): navigate while agent conversations initialize (#4093)

## Summary
Sending from Home/New Task or Create Agent now opens the destination as
soon as the existing API returns its task/session or Agent workspace.
The submitted text and attachment names remain visible while
conversation setup, uploads, and delivery finish. Failures retain the
existing creation identity and uploaded files. Before delivery or after
a definitive rejection, the destination lets users edit text, remove
attachments, retry, or discard the draft. Uncertain sends keep the
original payload locked for reconciliation.

Agent lists refresh in the background as soon as creation succeeds, so
the new Agent remains discoverable if first-message delivery fails and
the draft is discarded. List refresh does not delay navigation.

## Root cause
Navigation previously awaited the full first-message pipeline, and the
destination could repeat conversation binding. Agent creation also
awaited list refreshes. This frontend change keeps the operation alive
across navigation, shares successful setup through React Query, and
pauses competing destination initialization until delivery completes.
Retrying an uncertain task message checks thread history and reuses a
stable pending-post ID.

Launches are isolated by destination. An explicit new submission from
Home remains a new task/Agent; the change does not globally serialize
users’ work. Retry on the existing destination retains that launch’s
identity. A delivered launch is released on a history-load error so the
normal error surface replaces progress without resending.

Backend endpoints, provisioning, authorization, the awaited billing
gate, and model/upload/send ordering are unchanged. Agent creation still
waits for the existing synchronous provisioning API before it has a
workspace to open. In-flight drafts are memory-only; a full browser
reload does not automatically resend.

Known Mattermost limits are validated before task creation/handoff.
Editing a first Build message resumes in the existing workspace without
changing its original creation input. Discard releases only the local
draft and restores normal chat; it does not resend or delete the
destination.

## Test plan
- [x] Frontend governance guards, TypeScript, and ESLint
(`scripts/verify-web.sh --no-test` on changed files).
- [x] 794 relevant tests across New Chat, Agent workspaces, Agent query
hooks, launch lifecycle, and auth cleanup; additional attachment-only,
rendered pending/retry, delivered-history-failure, and retired-runtime
handoff regression checks passed. Handoff tests use the supported Engine
runtime.
- [x] Local Playwright with ready-user mock: held conversation setup
pending and saw the task page in ~1.1 seconds, with its submitted
message visible. Injected a 503, retried on the same task URL, and
observed one message send and no duplicate destination binding.
- [x] Local Playwright: held build-session setup pending and saw the
newly created Agent workspace in ~1.0 second; releasing it completed
delivery and rendered normal chat.

- [x] Permanent-error recovery: 234 focused tests passed, including
over-limit Home drafts retaining files, edited retries after source
unmount, retained upload IDs, Build creation identity, uncertain-send
editing guards, and discarded callback safety. Frontend governance,
TypeScript, and ESLint passed.
- [x] Local Playwright recovery checks: a 4,001-character task stayed on
Home with zero task-create requests; removing a rejected attachment and
editing the draft sent once on the same task URL without re-uploading
the retained file; a rejected Build message was edited in the same
workspace with one creation request; mobile Discard restored the
composer without another POST. Console errors were the intentionally
injected 400/413 responses.

- [x] Creation/list-refresh follow-up: 64 focused tests passed,
including an active sidebar observer with delayed refresh, upload/post
failure followed by discard, scoped list invalidation, and no resend or
duplicate creation. TypeScript, governance guards, and ESLint passed.

Mock timings demonstrate navigation no longer waits for downstream
setup; they are not production latency estimates. Local tests use UTC,
matching CI, because an unrelated existing date-display test assumes
UTC.
```

