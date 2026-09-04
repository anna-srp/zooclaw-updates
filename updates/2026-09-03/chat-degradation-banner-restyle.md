---
title: "模型降级提示条恢复中性配色，不再像报错"
type: "体验优化"
priority: "中"
date: "2026-09-03"
status: "待审核"
channels: "Discord+changelog"
---

# 模型降级提示条恢复中性配色，不再像报错

## 核心宣传点

当额度或其他原因导致对话临时降级到备用模型时，聊天里会出现一条提示横幅。这条横幅此前一直是老的警告色版本，视觉上像是出了故障，容易让人误以为对话坏了。设计上已批准的中性版改稿此前只存在于一个已关闭、未合并的 PR 里，所以 main 分支和线上版本都还在构建旧样式。

这次把它落回去了：横幅改为透明中性底 + 白色描边的操作按钮，观感上是「告知」而不是「报错」。同时把遗留的四段式 IQ 进度条色值换成已审定的共享渐变色 token，覆盖所有主题作用域。本次只做降级横幅这一件事，原 PR 里的引导巡览（guide tour）行为改动被有意排除在外。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `3101fe99d46aba80400b887ebd73efa9e8295c28`
- PR: #3632
- 作者: shana-srp
- 日期: 2026-09-03T05:49:29Z

### Commit Message

```
fix(chat): restore neutral degradation banner (#3632)

## Summary
- restyle the degraded-model banner with a transparent neutral surface
and white bordered action button
- replace the legacy four-stop IQ bar tokens with the approved shared
gradient token across all theme scopes
- add focused regression assertions for the restored banner classes and
gradient

This is the degradation-banner-only replacement for #3339; it
intentionally excludes the guide-tour behavior changes from that PR.

## Root cause
The approved banner restyle previously lived only in closed, unmerged PR
#3339, so both `main` and the production release continued to build the
legacy warning-colored banner.

## Test plan
- [x] `pnpm exec vitest run
src/__tests__/model-degradation-banner.test.tsx` (5 tests)
- [x] `pnpm tsc` and `pnpm lint` in `web/packages/chat-ui`
- [x] `bash scripts/verify-web.sh --no-test --no-lint
web/app/src/app/globals.css`
- [x] pre-commit and pre-push changed-surface verification

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

```
## Summary
- restyle the degraded-model banner with a transparent neutral surface and white bordered action button
- replace the legacy four-stop IQ bar tokens with the approved shared gradient token across all theme scopes
- add focused regression assertions for the restored banner classes and gradient

This is the degradation-banner-only replacement for #3339; it intentionally excludes the guide-tour behavior changes from that PR.

## Root cause
The approved banner restyle previously lived only in closed, unmerged PR #3339, so both `main` and the production release continued to build the legacy warning-colored banner.

## Test plan
- [x] `pnpm exec vitest run src/__tests__/model-degradation-banner.test.tsx` (5 tests)
- [x] `pnpm tsc` and `pnpm lint` in `web/packages/chat-ui`
- [x] `bash scripts/verify-web.sh --no-test --no-lint web/app/src/app/globals.css`
- [x] pre-commit and pre-push changed-surface verification
```
