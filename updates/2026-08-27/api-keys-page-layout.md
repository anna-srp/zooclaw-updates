---
title: "API Keys 页面重新排版：内容不再溢出，密钥弹窗和空状态更清爽"
type: "体验优化"
priority: "低"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# API Keys 页面重新排版：内容不再溢出，密钥弹窗和空状态更清爽

## 核心宣传点

API Keys 页面把重复的说明文字和操作按钮混在一起，表格内容也没有宽度约束，密钥多了以后会横向溢出；打开某一行的操作菜单时，整行还会莫名其妙地变灰。现在页面操作区、空状态和一次性密钥弹窗统一按新的设置页排版，说明文案精简为跟随当前状态的快速上手链接，表格用紧凑日期和截断把内容收在卡片内，展开行菜单也不会再让整行变色。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `6d2b0f0b655b12d255632f011a77b45a127a5ae2`
- PR: #3552
- 作者: lynn Zhuang
- 日期: 2026-08-27T09:35:02Z

### Commit Message

```
fix(settings): refine API keys page layout (#3552)

## Summary
- align API key page actions, empty state, and one-time secret dialog
with the approved settings layout
- simplify API guidance copy and keep quickstart links contextual to
each state
- fit populated key rows within the card using compact dates,
truncation, and a stable minimum content width
- keep table rows transparent while their action menus are open

## Root cause
The API key page mixed duplicated guidance and actions with
unconstrained table content. The shared table row also applies a muted
background whenever a descendant menu trigger is expanded, which caused
an unintended row highlight.

## Test plan
- [x] `bash scripts/verify-web.sh
'src/app/[locale]/(app)/claw-settings/components/ApiKeysTab.tsx'
'tests/unit/app/claw-settings/ApiKeysTab.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/claw-settings/ApiKeysTab.unit.spec.tsx` (57 tests)
- [x] Verify the populated table has no horizontal overflow
(`clientWidth === scrollWidth`)
- [x] Verify an expanded row action menu leaves the row background
transparent
```

### PR Description

```
## Summary
- align API key page actions, empty state, and one-time secret dialog with the approved settings layout
- simplify API guidance copy and keep quickstart links contextual to each state
- fit populated key rows within the card using compact dates, truncation, and a stable minimum content width
- keep table rows transparent while their action menus are open

## Root cause
The API key page mixed duplicated guidance and actions with unconstrained table content. The shared table row also applies a muted background whenever a descendant menu trigger is expanded, which caused an unintended row highlight.

## Test plan
- [x] `bash scripts/verify-web.sh 'src/app/[locale]/(app)/claw-settings/components/ApiKeysTab.tsx' 'tests/unit/app/claw-settings/ApiKeysTab.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/claw-settings/ApiKeysTab.unit.spec.tsx` (57 tests)
- [x] Verify the populated table has no horizontal overflow (`clientWidth === scrollWidth`)
- [x] Verify an expanded row action menu leaves the row background transparent

```

---
