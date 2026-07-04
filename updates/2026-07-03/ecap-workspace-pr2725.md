---
title: "Agent Builder 构建会话恢复「回放分享」功能"
type: "Bug Fix"
priority: "中"
date: "2026-07-03"
status: "待审核"
channels: ""
---

# Agent Builder 构建会话恢复「回放分享」功能

## 核心宣传点

在 Agent Builder 里构建 Agent 的对话过程又可以一键生成回放分享链接了，方便把搭建过程分享给他人。

## 原始内容

fix(agent-builder): restore build replay sharing (#2725)

## Summary
- Restore replay sharing on the Agent Builder build conversation.
- Reuse the existing chat replay share flow in the builder pane and hide
the composer during selection.
- Gate the Share action to ready, rendered builder conversations and
cover the replay create payload.

## Root cause
Agent Builder's build page renders its own conversation surface. After
that surface diverged from the main chat layout, it no longer wired the
header Share action or replay selection frame into the builder
conversation, so replay sharing disappeared from the build flow.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderReplayShare.tsx'
web/app/tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] `git push` pre-push changed-surface gate

---

**PR Description:**

## Summary
- Restore replay sharing on the Agent Builder build conversation.
- Reuse the existing chat replay share flow in the builder pane and hide the composer during selection.
- Gate the Share action to ready, rendered builder conversations and cover the replay create payload.

## Root cause
Agent Builder's build page renders its own conversation surface. After that surface diverged from the main chat layout, it no longer wired the header Share action or replay selection frame into the builder conversation, so replay sharing disappeared from the build flow.

## Test plan
- [x] `pnpm exec vitest run tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderReplayShare.tsx' web/app/tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] `git push` pre-push changed-surface gate

