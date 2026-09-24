---
title: "修复：从模板创建 Agent 的选择弹窗，交互和视觉更统一了"
type: "体验优化"
priority: "中"
date: "2026-09-23"
status: "待审核"
channels: ""
---

# 修复：从模板创建 Agent 的选择弹窗，交互和视觉更统一了

## 核心宣传点

走「从模板创建 Agent」这条路径时，入口卡片、模板列表和弹窗的视觉不太一致，弹窗高度也会随内容跳动。这次把入口卡片改成中性样式、头像改为叠放展示、模板卡片固定尺寸，弹窗高度随内容自适应且导航前后一致，边距更均衡，头尾固定、只有内容区滚动，滚动条是贴边的浅色细条。另附一个可选开启的九模板本地 mock 预览，方便按截图核对效果；头像素材单独交付。

## 分级

- 内部：P1
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Changes

Improve the Create Agent and template-selection flow: neutral entry cards, overlapping avatars, fixed-size template cards, content-adaptive dialog height and consistent navigation, balanced margins, fixed header/footer, and a pale edge scrollbar. Include an opt-in nine-template local mock preview based on user screenshots. Avatar images are delivered separately; this PR contains no generated avatar assets or hardcoded template-to-image mapping. Cards and details use the API-provided avatar_url.

## Explicit design requirement

The user explicitly requires ALL chat inputs on ALL pages to have NO additional focus-state border, outline, or ring of any color. Remove the ring added during earlier review from the shared ChatComposer itself. Preserve the normal resting border and text caret. Buttons and other controls retain their focus styling. This applies through UnifiedChatComposer to new chat, sessions, Create Agent and Agent Builder, and directly to the subagent panel. Do not reintroduce a ring to obtain review approval; this is an explicit product decision.

The previous Codex APPROVE applied to commit 6a39119e0, before this updated user requirement, and must not be reported as approval of the current head.

## Validation

- ChatComposer: 51 tests passed; focused package ESLint passed.
- Template/create dialog: 9 tests passed in the preceding UI change.
- After merging current main: 30 focused app tests, full app TypeScript, ESLint and push governance checks passed.
- Latest focus-ring removal verified in shared component source and consumer overrides; final browser visual validation remains pending.
- No staging deployment or live template data mutation.

## Base

The PR currently targets main after an external base change. It initially targeted feature/retire-v1-runtime to backport a focus override fix already present on main. Current main is now merged; the stale test conflict was resolved against current Engine behavior and tested.

## Latest layout refinement

Dialog height follows content, capped at min(640px, 80dvh). Long content scrolls internally; short forms no longer reserve empty space before the footer. Entry title is centered at 24px with increased top spacing. Template and copy steps retain their back navigation and alignment. Nine relevant app tests pass. Browser capture is currently unavailable due to native pipe startup failure.

Template cards use the existing brand composer shadow token, with the shared card-elevation fallback, for a subtle resting shadow.

## Avatar handoff

Removed the three generated WebP files and local name-based avatar resolver from the PR diff. The user received a ZIP with PNG originals, 256px WebP versions, and a template-to-filename README for engineering to upload and configure via avatar_url.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `ca6fc23c0cd4af8afcbb27a1d5abf038c5877bdd`
- PR: #3879
- 作者：lynn Zhuang
- 日期：2026-09-23T09:51:14Z

### Commit Message

```
fix(agents): 修复从模板创建Agent路径的交互和视觉 (#3879)

## Changes

Improve the Create Agent and template-selection flow: neutral entry
cards, overlapping avatars, fixed-size template cards, content-adaptive
dialog height and consistent navigation, balanced margins, fixed
header/footer, and a pale edge scrollbar. Include an opt-in
nine-template local mock preview based on user screenshots. Avatar
images are delivered separately; this PR contains no generated avatar
assets or hardcoded template-to-image mapping. Cards and details use the
API-provided avatar_url.

## Explicit design requirement

The user explicitly requires ALL chat inputs on ALL pages to have NO
additional focus-state border, outline, or ring of any color. Remove the
ring added during earlier review from the shared ChatComposer itself.
Preserve the normal resting border and text caret. Buttons and other
controls retain their focus styling. This applies through
UnifiedChatComposer to new chat, sessions, Create Agent and Agent
Builder, and directly to the subagent panel. Do not reintroduce a ring
to obtain review approval; this is an explicit product decision.

The previous Codex APPROVE applied to commit 6a39119e0, before this
updated user requirement, and must not be reported as approval of the
current head.

## Validation

- ChatComposer: 51 tests passed; focused package ESLint passed.
- Template/create dialog: 9 tests passed in the preceding UI change.
- After merging current main: 30 focused app tests, full app TypeScript,
ESLint and push governance checks passed.
- Latest focus-ring removal verified in shared component source and
consumer overrides; final browser visual validation remains pending.
- No staging deployment or live template data mutation.

## Base

The PR currently targets main after an external base change. It
initially targeted feature/retire-v1-runtime to backport a focus
override fix already present on main. Current main is now merged; the
stale test conflict was resolved against current Engine behavior and
tested.

## Latest layout refinement

Dialog height follows content, capped at min(640px, 80dvh). Long content
scrolls internally; short forms no longer reserve empty space before the
footer. Entry title is centered at 24px with increased top spacing.
Template and copy steps retain their back navigation and alignment. Nine
relevant app tests pass. Browser capture is currently unavailable due to
native pipe startup failure.

Template cards use the existing brand composer shadow token, with the
shared card-elevation fallback, for a subtle resting shadow.

## Avatar handoff

Removed the three generated WebP files and local name-based avatar
resolver from the PR diff. The user received a ZIP with PNG originals,
256px WebP versions, and a template-to-filename README for engineering
to upload and configure via avatar_url.

---------

Co-authored-by: kaka-srp <kaka@srp.one>
```

来源：SerendipityOneInc/ecap-workspace @ ca6fc23c，PR #3879，作者 lynn Zhuang。