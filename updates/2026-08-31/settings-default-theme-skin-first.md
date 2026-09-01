---
title: "设置里的主题皮肤：默认皮肤 Paper Focus 排到第一位，也可以主动选回来"
type: "体验优化"
priority: "低"
date: "2026-08-31"
status: "待审核"
channels: "Discord+changelog"
---

# 设置里的主题皮肤：默认皮肤 Paper Focus 排到第一位，也可以主动选回来

## 核心宣传点

设置页的主题皮肤列表里，默认皮肤 Paper Focus 以前是隐式的、不在可选项里，现在把它显式放出来并排在第一位，其余皮肤的相对顺序保持不变。换过别的皮肤之后想换回默认，直接点第一个就行。Paper Focus 的中英文描述文案也一并更新了。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `505fc095a687cbb1d8bcdb766d9361a1082bbb4c`
- PR: #3598
- 作者: shana-srp
- 日期: 2026-08-31T10:50:49Z

### Commit Message

```
feat(settings): show the default theme skin first (#3598)

## Summary

- expose Paper Focus as the selectable default Theme skin
- place the default skin first while preserving the order of the
remaining skins
- update the Paper Focus description in English and Chinese
- cover the default selection and tile order with a unit test

## Testing

- `pnpm exec vitest run
tests/unit/components/settings/GeneralTab.unit.spec.tsx
tests/unit/theme/brand-themes.unit.spec.ts` (48 passed)
- `bash scripts/verify-changed.sh` (pre-push: TypeScript and ESLint
passed)

## Preview

- `http://localhost:3000/claw-settings`

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Description

```
## Summary

- expose Paper Focus as the selectable default Theme skin
- place the default skin first while preserving the order of the remaining skins
- update the Paper Focus description in English and Chinese
- cover the default selection and tile order with a unit test

## Testing

- `pnpm exec vitest run tests/unit/components/settings/GeneralTab.unit.spec.tsx tests/unit/theme/brand-themes.unit.spec.ts` (48 passed)
- `bash scripts/verify-changed.sh` (pre-push: TypeScript and ESLint passed)

## Preview

- `http://localhost:3000/claw-settings`

```
