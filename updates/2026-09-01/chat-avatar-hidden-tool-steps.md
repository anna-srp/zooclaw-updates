---
title: "修复：关掉「显示工具执行过程」后，助手回复的头像会消失"
type: "Bug Fix"
priority: "低"
date: "2026-09-01"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：关掉「显示工具执行过程」后，助手回复的头像会消失

## 核心宣传点

在聊天里把工具执行步骤隐藏起来之后，同一轮里第一条可见的助手回复不显示头像，位置上留一块空白。原因是被隐藏的工具组消息虽然最终渲染成空，但在此之前已经占用了这一轮的身份标识，导致后面第一条真正可见的文字回复被误判成「连续消息」，于是只渲染了一个空的头像占位。现在助手消息的分组在「显示」和「隐藏」两种模式下分别计算：隐藏工具步骤时第一条可见回复正常带头像，同一轮里后续消息仍按连续处理，不会冒出重复头像。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `31d495c6cf1380a11570f0a2320f5f4612978d25`
- PR: #3615
- 作者: sam-srp
- 日期: 2026-09-01T11:15:33Z

### Commit Message

```
fix(chat): preserve avatar when tool steps are hidden (#3615)

## Summary
- compute assistant message grouping for both visible and hidden
tool-step modes
- preserve the avatar on the first visible assistant response when tool
steps are hidden
- keep later messages in the same run consecutive to avoid duplicate
avatars

## Root cause
Hidden tool-group messages still consumed the run identity before the
renderer returned `null`, so the first visible text response was
incorrectly marked consecutive and rendered an empty avatar spacer.

## Verification
- `pnpm --filter @zooclaw/web-app exec vitest run --config
./vitest.config.mts tests/unit/chat/useOpenClawRuntime.unit.spec.ts`
- targeted ESLint checks
- `pnpm --filter @zooclaw/web-app exec tsc --noEmit`
```

### PR Body

```
## Summary
- compute assistant message grouping for both visible and hidden tool-step modes
- preserve the avatar on the first visible assistant response when tool steps are hidden
- keep later messages in the same run consecutive to avoid duplicate avatars

## Root cause
Hidden tool-group messages still consumed the run identity before the renderer returned `null`, so the first visible text response was incorrectly marked consecutive and rendered an empty avatar spacer.

## Verification
- `pnpm --filter @zooclaw/web-app exec vitest run --config ./vitest.config.mts tests/unit/chat/useOpenClawRuntime.unit.spec.ts`
- targeted ESLint checks
- `pnpm --filter @zooclaw/web-app exec tsc --noEmit`
```
