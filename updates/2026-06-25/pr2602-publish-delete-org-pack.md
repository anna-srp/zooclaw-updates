---
title: "发布页支持删除（下架）已发布的 Agent 包"
type: "体验优化"
priority: "中"
date: "2026-06-25"
status: "待审核"
channels: ""
---

# 发布页支持删除（下架）已发布的 Agent 包

## 核心宣传点

在 Agent 发布页可以直接删除自己发布的 Agent 包，并带二次确认，发布与下架管理更顺手。

## 原始内容

### Commit Message

```
fix(agents): wire publish delete to deprecate org packs (#2602)

## Summary
- Wire the publish-page Delete action to org pack deprecation.
- Add a confirmation modal and preserve backend pack_id for the
deprecate call.
- Keep Delete disabled for installed agents and non-deprecatable publish
records.

## Tests
- pnpm --dir web/app exec vitest run
tests/unit/app/agents-manager-publish.unit.spec.tsx
- bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/PublishAgentsClient.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/components/PublishDeleteConfirmModal.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/components/types.ts'
web/app/src/models/org-agent-pack.ts
web/app/src/services/org-agent-packs.ts
web/app/tests/unit/app/agents-manager-publish.unit.spec.tsx
- bash scripts/verify-changed.sh
```

### PR Description

## Summary
- Wire the publish-page Delete action to org pack deprecation.
- Add a confirmation modal and preserve backend pack_id for the deprecate call.
- Keep Delete disabled for installed agents and non-deprecatable publish records.

## Tests
- pnpm --dir web/app exec vitest run tests/unit/app/agents-manager-publish.unit.spec.tsx
- bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/PublishAgentsClient.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/components/PublishDeleteConfirmModal.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/components/types.ts' web/app/src/models/org-agent-pack.ts web/app/src/services/org-agent-packs.ts web/app/tests/unit/app/agents-manager-publish.unit.spec.tsx
- bash scripts/verify-changed.sh

