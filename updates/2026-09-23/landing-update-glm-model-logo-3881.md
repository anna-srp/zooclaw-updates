---
title: "官网首页模型区的 GLM 图标更新为黑色 Z 标识"
type: "体验优化"
priority: "低"
date: "2026-09-23"
status: "待审核"
channels: ""
---

# 官网首页模型区的 GLM 图标更新为黑色 Z 标识

## 核心宣传点

首页模型滚动区里原来的蓝色 GLM 图标换成了新的黑色 Z logo，附上了原始 PNG 素材，外面的圆形容器、尺寸和动画效果都保持原样。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
Replace the homepage model row's blue GLM icon with the supplied black Z logo. Add the original PNG and update the GLM image reference while preserving the existing circle, sizing, and animation.

## Validation
- `bash scripts/verify-web.sh --no-test src/app/landing/components/ZooworkHomeSections.tsx` passed (governance guards, TypeScript, ESLint).
- Prettier and `git diff --check` passed.
- Verified the rendered homepage and replacement logo in the local browser at `/#platform`.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `30fce6f9d7a8dc95c86a04afeee918cbb1aa202c`
- PR: #3881
- 作者：shana-srp
- 日期：2026-09-23T08:08:21Z

### Commit Message

```
fix(landing): update GLM model logo (#3881)

## Summary
Replace the homepage model row's blue GLM icon with the supplied black Z
logo. Add the original PNG and update the GLM image reference while
preserving the existing circle, sizing, and animation.

## Validation
- `bash scripts/verify-web.sh --no-test
src/app/landing/components/ZooworkHomeSections.tsx` passed (governance
guards, TypeScript, ESLint).
- Prettier and `git diff --check` passed.
- Verified the rendered homepage and replacement logo in the local
browser at `/#platform`.

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

来源：SerendipityOneInc/ecap-workspace @ 30fce6f9，PR #3881，作者 shana-srp。