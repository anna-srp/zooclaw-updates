---
title: "Agent 目录新增快速命令（quick_commands）支持"
type: "新功能上线"
priority: "中"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "c916c5720e29255f4f899a201a790c85a9d3ce80"
pr: 1773
---
# Agent 目录新增快速命令（quick_commands）支持

## 核心宣传点

Agent 现在可以在目录中配置快捷指令，用户可以一键触发常用操作，提升使用效率。

## 原始内容

### Commit Message

```
feat(claw-interface): add quick_commands to agent catalog schema (#1773)

## Summary
- Add `QuickCommand` model and `quick_commands` field to agent catalog
schema
- Each agent can now declare per-agent quick command shortcuts via the
internal catalog API
- Frontend reads from the existing catalog API cache — no new endpoints
needed

## Linear Issue

https://linear.app/srpone/issue/ECA-711/zooclaw-web-agent-new-chat-体验完善可配置快捷指令区-specialist-开场选项

## Changes
- `app/schema/openclaw.py`: Add `QuickCommand` model (`id`, `label`,
`label_cn`, `prompt`), add `quick_commands` field to `AgentCatalogItem`,
`UpsertAgentCatalogRequest`, `PatchAgentCatalogRequest`

## Frontend Contract

After this lands, the catalog API response includes:

```typescript
interface QuickCommand {
  id: string
  label: string
  label_cn: string
  prompt: string
}

// Added to existing AgentCatalogItem
quick_commands?: QuickCommand[]
```

- Data available from existing `agent-catalog-cache.ts` localStorage
cache
- Agents without quick commands return `[]`
- Frontend should use `label_cn` when locale is `zh`, otherwise `label`

## Test plan
- [ ] `GET /openclaw/agent-catalog` returns `quick_commands` when
configured
- [ ] `PATCH /internal/agent-catalog/{agent_id}` with `quick_commands`
persists correctly
- [ ] Agents without `quick_commands` return empty array (backward
compat)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
- Add `QuickCommand` model and `quick_commands` field to agent catalog schema
- Each agent can now declare per-agent quick command shortcuts via the internal catalog API
- Frontend reads from the existing catalog API cache — no new endpoints needed

## Linear Issue
https://linear.app/srpone/issue/ECA-711/zooclaw-web-agent-new-chat-体验完善可配置快捷指令区-specialist-开场选项

## Changes
- `app/schema/openclaw.py`: Add `QuickCommand` model (`id`, `label`, `label_cn`, `prompt`), add `quick_commands` field to `AgentCatalogItem`, `UpsertAgentCatalogRequest`, `PatchAgentCatalogRequest`

## Frontend Contract

After this lands, the catalog API response includes:

```typescript
interface QuickCommand {
  id: string
  label: string
  label_cn: string
  prompt: string
}

// Added to existing AgentCatalogItem
quick_commands?: QuickCommand[]
```

- Data available from existing `agent-catalog-cache.ts` localStorage cache
- Agents without quick commands return `[]`
- Frontend should use `label_cn` when locale is `zh`, otherwise `label`

## Test plan
- [ ] `GET /openclaw/agent-catalog` returns `quick_commands` when configured
- [ ] `PATCH /internal/agent-catalog/{agent_id}` with `quick_commands` persists correctly
- [ ] Agents without `quick_commands` return empty array (backward compat)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
