---
title: "修复：在 Agent Build 对话里输入 /new 不再把当前会话切走"
type: "Bug Fix"
priority: "中"
date: "2026-09-23"
status: "待审核"
channels: ""
---

# 修复：在 Agent Build 对话里输入 /new 不再把当前会话切走

## 核心宣传点

Agent Build 是一个连续的构建对话，中途被 /new 切换会话会让之前的构建上下文断掉。现在 Build 里的独立 /new 指令会被拦下，给出本地化的说明提示，而不是一个「发送失败」的红色横幅；草稿和附件都保留，普通任务会话里的 /new 行为不受影响。拦截同时作用于输入框和共享的会话发送通道，运行时或程序化发送也会在乐观消息和网络请求之前被校验住。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary

- Block standalone `/new` commands in Agent Build, with localized informational guidance instead of a send-failure banner. Preserve drafts and attachments; normal task chats remain unchanged.
- Validate both the composer and the shared conversation send path, covering runtime/programmatic sends before optimistic messages or network requests.
- Also reject `/new` as the first Build prompt, before provisioning an Agent/session or preparing attachments. The Home launcher and creation dialog show creation-specific guidance and allow a corrected retry.

Related to https://github.com/SerendipityOneInc/agent-channel-service/issues/144.

## Root cause

Build retains a canonical development session, but ACS interprets `/new` as session rotation. Forwarding it from Build can leave the stored development session and Mattermost thread binding inconsistent. This change implements the agreed ECAP-side guard without changing ACS or Engine.

The pre-submission review identified that the first Build prompt bypassed the conversation hook. The shared creation service now guards that path before any resource creation or attachment preparation, using the same command matcher as ongoing Build chats.

## Scope

- Exact standalone matching, including case and surrounding whitespace; mentions, quoted/code content, and command arguments are not treated as `/new`.
- Explicit blank creation, normal prompts, and non-Build conversation behavior remain available.
- No context-reset feature, historical session repair, ACS/Engine changes, or deployment.
- This is a Web client guard, not a server-side restriction for direct Mattermost/other clients.

## Test plan

- [x] 380 targeted Vitest tests across 15 files: conversation guard/runtime sends, composer submission and draft preservation, Agent creation and retries, Home launcher, and normal session chat regressions.
- [x] TypeScript check: `bash scripts/verify-web.sh --tsc-only`.
- [x] ESLint on all changed TypeScript files.
- [x] Frontend governance guards: `bash scripts/verify-web.sh --guards-only`.
- [x] `git diff --check`.
- [ ] Real browser / staging end-to-end smoke (not performed).

Full build and repository-wide checks are delegated to CI.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `b5b781ee13f0f5b19222a86ebdea5f750af936f4`
- PR: #3875
- 作者：kaka-srp
- 日期：2026-09-23T04:01:39Z

### Commit Message

```
fix(agents): prevent session rotation in Build conversations (#3875)

## Summary

- Block standalone `/new` commands in Agent Build, with localized
informational guidance instead of a send-failure banner. Preserve drafts
and attachments; normal task chats remain unchanged.
- Validate both the composer and the shared conversation send path,
covering runtime/programmatic sends before optimistic messages or
network requests.
- Also reject `/new` as the first Build prompt, before provisioning an
Agent/session or preparing attachments. The Home launcher and creation
dialog show creation-specific guidance and allow a corrected retry.

Related to
https://github.com/SerendipityOneInc/agent-channel-service/issues/144.

## Root cause

Build retains a canonical development session, but ACS interprets `/new`
as session rotation. Forwarding it from Build can leave the stored
development session and Mattermost thread binding inconsistent. This
change implements the agreed ECAP-side guard without changing ACS or
Engine.

The pre-submission review identified that the first Build prompt
bypassed the conversation hook. The shared creation service now guards
that path before any resource creation or attachment preparation, using
the same command matcher as ongoing Build chats.

## Scope

- Exact standalone matching, including case and surrounding whitespace;
mentions, quoted/code content, and command arguments are not treated as
`/new`.
- Explicit blank creation, normal prompts, and non-Build conversation
behavior remain available.
- No context-reset feature, historical session repair, ACS/Engine
changes, or deployment.
- This is a Web client guard, not a server-side restriction for direct
Mattermost/other clients.

## Test plan

- [x] 380 targeted Vitest tests across 15 files: conversation
guard/runtime sends, composer submission and draft preservation, Agent
creation and retries, Home launcher, and normal session chat
regressions.
- [x] TypeScript check: `bash scripts/verify-web.sh --tsc-only`.
- [x] ESLint on all changed TypeScript files.
- [x] Frontend governance guards: `bash scripts/verify-web.sh
--guards-only`.
- [x] `git diff --check`.
- [ ] Real browser / staging end-to-end smoke (not performed).

Full build and repository-wide checks are delegated to CI.
```

来源：SerendipityOneInc/ecap-workspace @ b5b781ee，PR #3875，作者 kaka-srp。