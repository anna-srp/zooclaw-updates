---
title: "修复：Agent 详情弹窗里的长分享链接会撑破弹窗边界"
type: "Bug Fix"
priority: "低"
date: "2026-08-31"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：Agent 详情弹窗里的长分享链接会撑破弹窗边界

## 核心宣传点

共享 Agent 的详情弹窗里，分享链接如果比较长会把弹窗整个撑宽，右边溢出到边界外面。根因是链接那一行是 CSS Grid 的直接子项，它默认的 min-width: auto 会保留长 URL 的最小内容宽度——就算内层 Flex 子项已经允许收缩，也没法跨层去覆盖 Grid item 的这个约束。现在修好了，URL 的省略号显示和复制按钮的行为都保持原样。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `cd6abe078cebfb8ff4e82b60c8527b15ac65a5d4`
- PR: #3595
- 作者: lynn Zhuang
- 日期: 2026-08-31T07:04:07Z

### Commit Message

```
fix(agent-builder): 修复 Agent 详情弹窗分享链接溢出 (#3595)

## 摘要
- 修复共享 Agent 详情弹窗中长分享链接撑出弹窗边界的问题。
- 保留现有的 URL 省略显示与复制按钮行为。

## 根因
分享链接行是 CSS Grid 的直接子项。其默认的 `min-width: auto` 会保留长 URL
的最小内容宽度，导致该行超过固定宽度的弹窗；即使内部 Flex 子项已允许收缩，也无法跨层覆盖 Grid item 的最小宽度约束。

## 测试计划
- [x] `bash scripts/verify-web.sh
'src/app/[locale]/(app)/(chat)/agent-builder/my-agents/owned/components/PublishDetailModal.tsx'
'tests/unit/app/agent-builder/my-agents/OwnedAgentsClient.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] 在 1440px 视口下使用 Playwright 测量：弹窗的 `scrollWidth` 与 `clientWidth` 均为
512px，分享链接行右边界保持在弹窗内部。
```

### PR Description

```
## 摘要
- 修复共享 Agent 详情弹窗中长分享链接撑出弹窗边界的问题。
- 保留现有的 URL 省略显示与复制按钮行为。

## 根因
分享链接行是 CSS Grid 的直接子项。其默认的 `min-width: auto` 会保留长 URL 的最小内容宽度，导致该行超过固定宽度的弹窗；即使内部 Flex 子项已允许收缩，也无法跨层覆盖 Grid item 的最小宽度约束。

## 测试计划
- [x] `bash scripts/verify-web.sh 'src/app/[locale]/(app)/(chat)/agent-builder/my-agents/owned/components/PublishDetailModal.tsx' 'tests/unit/app/agent-builder/my-agents/OwnedAgentsClient.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] 在 1440px 视口下使用 Playwright 测量：弹窗的 `scrollWidth` 与 `clientWidth` 均为 512px，分享链接行右边界保持在弹窗内部。
```

## 备注

已用 Playwright 在 1440px 视口实测：弹窗 scrollWidth 与 clientWidth 均为 512px，链接行右边界留在弹窗内部。
