---
title: "修复 Agent Builder 历史项目崩溃，重建机器人后可恢复项目"
type: "Bug Fix"
priority: "中"
date: "2026-06-29"
status: "待审核"
channels: ""
---

# 修复 Agent Builder 历史项目崩溃，重建机器人后可恢复项目

## 核心宣传点

修复了 Agent Builder 打开含图片的历史消息时的崩溃问题；重新创建机器人后，原有的 Agent Builder 项目也能自动恢复，不再丢失搭建进度。

## 原始内容

### Commit Message

```
fix(agent-builder): recover recreated builder projects (#2635)

## Summary
- Fix Agent Builder image attachment crashes by mounting
`ImagePreviewProvider` on the Agent Builder page.
- Recover historical Agent Builder projects after bot recreation when a
submitted/share/published pack artifact exists.
- Mark unrecoverable recreated-bot historical projects with a clear
archive instruction when no artifact exists.

## Root cause
Two separate staging failure modes were involved:

1. Historical Agent Builder messages with image attachments triggered
`useImagePreview()`, but the Agent Builder route did not provide
`ImagePreviewProvider`. Sentry showed `useImagePreview must be used
within ImagePreviewProvider` on the Agent Builder route.
2. After a user recreated the bot, old Agent Builder project records
could still point at the deleted old bot runtime. Workspace
materialization then called the stale bot runtime `/runtime/exec` and
got 404.

Linear:
https://linear.app/srpone/issue/ECA-1126/fix-agent-builder-recovery-crashes

## Test plan
- [x] `pnpm test:unit tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] `pnpm exec eslint
src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx
tests/unit/app/agent-builder-client.unit.spec.tsx --quiet`
- [x] `.venv/bin/pytest tests/unit/test_agent_builder_service.py`
- [x] `.venv/bin/pytest tests/unit/test_agent_builder_service.py -k
'recreated_runtime or
import_project_source_uses_recovered_builder_after_recreated_runtime or
import_submitted_pack_source_regenerates_presigned_url'`
- [x] `.venv/bin/ruff check app/services/agent_builder_service.py
tests/unit/test_agent_builder_service.py`
- [x] `.venv/bin/ruff format --check
app/services/agent_builder_service.py
tests/unit/test_agent_builder_service.py`
- [x] `/opt/homebrew/bin/pyright --pythonpath .venv/bin/python
app/services/agent_builder_service.py
tests/unit/test_agent_builder_service.py`
- [x] `git diff --check`

## Notes
- A previous full frontend `tsc` attempt failed before dependency
refresh because local `web/app/node_modules` was missing existing
workspace/dependency links (`@zooclaw/auth-client`, `ldrs/react`). That
was an environment/install issue, not introduced by this PR.
```

### PR Description

## Summary
- Fix Agent Builder image attachment crashes by mounting `ImagePreviewProvider` on the Agent Builder page.
- Recover historical Agent Builder projects after bot recreation when a submitted/share/published pack artifact exists.
- Mark unrecoverable recreated-bot historical projects with a clear archive instruction when no artifact exists.

## Root cause
Two separate staging failure modes were involved:

1. Historical Agent Builder messages with image attachments triggered `useImagePreview()`, but the Agent Builder route did not provide `ImagePreviewProvider`. Sentry showed `useImagePreview must be used within ImagePreviewProvider` on the Agent Builder route.
2. After a user recreated the bot, old Agent Builder project records could still point at the deleted old bot runtime. Workspace materialization then called the stale bot runtime `/runtime/exec` and got 404.

Linear: https://linear.app/srpone/issue/ECA-1126/fix-agent-builder-recovery-crashes

## Test plan
- [x] `pnpm test:unit tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] `pnpm exec eslint src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx tests/unit/app/agent-builder-client.unit.spec.tsx --quiet`
- [x] `.venv/bin/pytest tests/unit/test_agent_builder_service.py`
- [x] `.venv/bin/pytest tests/unit/test_agent_builder_service.py -k 'recreated_runtime or import_project_source_uses_recovered_builder_after_recreated_runtime or import_submitted_pack_source_regenerates_presigned_url'`
- [x] `.venv/bin/ruff check app/services/agent_builder_service.py tests/unit/test_agent_builder_service.py`
- [x] `.venv/bin/ruff format --check app/services/agent_builder_service.py tests/unit/test_agent_builder_service.py`
- [x] `/opt/homebrew/bin/pyright --pythonpath .venv/bin/python app/services/agent_builder_service.py tests/unit/test_agent_builder_service.py`
- [x] `git diff --check`

## Notes
- A previous full frontend `tsc` attempt failed before dependency refresh because local `web/app/node_modules` was missing existing workspace/dependency links (`@zooclaw/auth-client`, `ldrs/react`). That was an environment/install issue, not introduced by this PR.

