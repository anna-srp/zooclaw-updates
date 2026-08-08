---
title: "技能商店改版：统一官方目录 + 按 Agent 分组"
type: "体验优化"
priority: "中"
date: "2026-08-07"
status: "待审核"
channels: ""
---

## 核心宣传点

技能商店把内置与社区合并为一个官方目录，已安装技能按 Agent 工作区分组，卡片层级和中文简介都更清晰。

## 原始内容

### feat(skills): simplify official skill management (#3210)

- SHA: `3646037a900be20d346d2da49a39ef1f99b10c68`
- 仓库: 见 raw/2026-08-07

**Commit Message:**

```
feat(skills): simplify official skill management (#3210)

## Summary

- replace Built-in and Community views with a single Official catalog
- group installed skills by Agent workspace
- improve loading states, card hierarchy, publisher labeling, and
localized Chinese skill summaries
- remove the redundant Skill Store intro block

## Testing

- TypeScript (`tsc --noEmit`)
- ESLint
- 63 focused Vitest tests
- pre-push changed-surface verification

## Notes

- Skill detail lookup ambiguity for duplicate ClawHub slugs is
intentionally out of scope and will be handled separately.

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

**PR Body:**

## Summary

- replace Built-in and Community views with a single Official catalog
- group installed skills by Agent workspace
- improve loading states, card hierarchy, publisher labeling, and localized Chinese skill summaries
- remove the redundant Skill Store intro block

## Testing

- TypeScript (`tsc --noEmit`)
- ESLint
- 63 focused Vitest tests
- pre-push changed-surface verification

## Notes

- Skill detail lookup ambiguity for duplicate ClawHub slugs is intentionally out of scope and will be handled separately.


