---
title: "着陆页跳转后不再自动发送，改为预填输入框"
type: "产品基础功能更新"
priority: "低"
date: "2026-05-13"
status: "待审核"
channels: "Discord + changelog"
---

# 着陆页跳转后不再自动发送，改为预填输入框

## 核心宣传点

当你从落地页点击进入某个 Agent 对话时，查询内容现在会自动填入输入框而非直接发送——你可以先确认或修改后再提交，避免意外的"突然发话"。

## 原始内容

**来源**: ecap-workspace PR #1602 | SHA: 0ed68020

**Commit Message**:
```
refactor(web): prefill composer instead of auto-sending landing query (#1602)

The landing-context flow (?sp=<specialist_id> + localStorage['ecap:landingContext'])
used to auto-send the initial query into chat once the agent switch settled.
This refactor replaces the auto-send with a prefill into the composer, so the user
reviews the prompt and submits manually.

Why: The user wanted the landing-page initial query to land in the chat input rather
than fire automatically — gives them a chance to edit before sending and avoids
surprise sends on the very first interaction.

What changed:
- useLandingContextFlow.ts — onSwitchAgent(agentId, prefillText?). Dropped
  onSendMessage and currentAgentId from the hook's interface. Phase 5 (delivering)
  collapses to cleanup: mark delivered + clear localStorage.
- GenClawClient.tsx — pass prefillText to the chat input component.
```

**PR #1602 Description**:
```
Summary: The landing-context flow used to auto-send the initial query.
This refactor replaces the auto-send with a prefill into the composer,
so the user reviews the prompt and submits manually.

Why: Gives users a chance to edit before sending and avoids surprise sends
on the very first interaction.
```
