---
title: "已安装的组织包 Agent 支持一键更新"
type: "体验优化"
priority: "中"
date: "2026-07-07"
status: "待审核"
channels: ""
---

# 已安装的组织包 Agent 支持一键更新

## 核心宣传点

在发布页面即可看到已安装 Agent 的更新提示并一键升级到最新版本，无需重新安装。

## 原始内容

```
feat(web): add custom publish agent updates (#2763)

## Summary

- add a custom publish-page Update action for installed org-pack agents
- show Update only when the installed workspace submission differs from
the pack latest submission, matching the official agents page behavior
- reuse the computer-scoped agent update route and refresh
current-computer agents after completion

## Tests

- `./node_modules/.bin/vitest run --config ./vitest.config.mts
tests/unit/app/agents-manager-publish.unit.spec.tsx`
- `./node_modules/.bin/tsc --noEmit` with stale `.next/types`
temporarily moved out and restored
- `git diff --check`

## Notes

- `pnpm --dir web/app exec ...` is still blocked locally by the existing
`ERR_PNPM_MISSING_TARBALL_INTEGRITY` issue for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.
- Direct `eslint` invocation is currently blocked locally by dependency
resolution for `tw-animate-css`.

---

## PR Description

## Summary

- add a custom publish-page Update action for installed org-pack agents
- show Update only when the installed workspace submission differs from the pack latest submission, matching the official agents page behavior
- reuse the computer-scoped agent update route and refresh current-computer agents after completion

## Tests

- `./node_modules/.bin/vitest run --config ./vitest.config.mts tests/unit/app/agents-manager-publish.unit.spec.tsx`
- `./node_modules/.bin/tsc --noEmit` with stale `.next/types` temporarily moved out and restored
- `git diff --check`

## Notes

- `pnpm --dir web/app exec ...` is still blocked locally by the existing `ERR_PNPM_MISSING_TARBALL_INTEGRITY` issue for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.
- Direct `eslint` invocation is currently blocked locally by dependency resolution for `tw-animate-css`.

```
