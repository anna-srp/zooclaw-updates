---
title: "AI Specialists Hub 页面布局恢复"
type: "Bug Fix"
priority: "中"
date: "2026-07-07"
status: "待审核"
channels: ""
---

# AI Specialists Hub 页面布局恢复

## 核心宣传点

AI 专家中心页面恢复正常布局和视觉样式，浏览和购买专家包体验回归正常。

## 原始内容

```
fix(web): restore specialists hub layout (#2742)

## Summary
- Restore the AI Specialists Hub to the pre-#2679 app-owned layout and
styling.
- Remove the app-side `@zooclaw/design-system` dependency/import path
introduced for this page.
- Keep the later paid-pack purchase flow intact and add a regression
test for the broken DS layout path.

## Root cause
PR #2679 migrated Specialists Hub onto the ZooClaw design-system
components/tokens, which changed the page structure and visual behavior.
This restores the original app-owned UI while preserving later business
behavior added after #2679.

## Test plan
- [x] `corepack pnpm --dir web/app exec vitest run
tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx
tests/unit/app/agents-manager/AgentCard.unit.spec.tsx
tests/unit/app/agents-manager-client.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh 'web/app/next.config.ts'
'web/app/package.json'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/AgentsManagerClient.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentCard.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentModal.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/SkillTags.tsx'
'web/app/src/app/globals.css'
'web/app/src/components/ClawConnectionStatus.tsx'
'web/app/tests/unit/app/agents-manager/AgentCard.unit.spec.tsx'
'web/app/tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] Mock preview on latest `origin/main`: `/en/agents-manager` renders
in light and dark mode with 8 cards, no `[data-agents-manager-page]`
marker, and `lg:grid-cols-3`.

## Preview
- Light: `.screenshots/specialists-hub-latest-main-light.png`
- Dark: `.screenshots/specialists-hub-latest-main-dark.png`

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>

---

## PR Description

## Summary
- Restore the AI Specialists Hub to the pre-#2679 app-owned layout and styling.
- Remove the app-side `@zooclaw/design-system` dependency/import path introduced for this page.
- Keep the later paid-pack purchase flow intact and add a regression test for the broken DS layout path.

## Root cause
PR #2679 migrated Specialists Hub onto the ZooClaw design-system components/tokens, which changed the page structure and visual behavior. This restores the original app-owned UI while preserving later business behavior added after #2679.

## Test plan
- [x] `corepack pnpm --dir web/app exec vitest run tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx tests/unit/app/agents-manager/AgentCard.unit.spec.tsx tests/unit/app/agents-manager-client.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh 'web/app/next.config.ts' 'web/app/package.json' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/AgentsManagerClient.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentCard.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentModal.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/SkillTags.tsx' 'web/app/src/app/globals.css' 'web/app/src/components/ClawConnectionStatus.tsx' 'web/app/tests/unit/app/agents-manager/AgentCard.unit.spec.tsx' 'web/app/tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] Mock preview on latest `origin/main`: `/en/agents-manager` renders in light and dark mode with 8 cards, no `[data-agents-manager-page]` marker, and `lg:grid-cols-3`.

## Preview
- Light: `.screenshots/specialists-hub-latest-main-light.png`
- Dark: `.screenshots/specialists-hub-latest-main-dark.png`

```
