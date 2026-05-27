---
title: "Agent Pack 提交历史页面优化"
type: "产品基础功能更新"
priority: "低"
date: "2026-05-26"
status: "待审核"
channels: "Discord + changelog"
---
# Agent Pack 提交历史页面优化

## 核心宣传点

Agent Pack 详情页的版本历史展示更清晰，支持直接下载每次提交的资源文件。

## 原始内容

**Commit:** bd6b24f8
**Repo:** ecap-workspace
**Author:** bill-srp

**Commit Message:**
```
fix(enterprise): clean up pack submission history (#1940)

## Summary
- Remove the duplicated Version history section from the pack detail
page
- Add per-submission asset links pointing at
https://agentpack.zooclaw.ai
- Define the pack archive public domain in the R2 upload contract/config
- Cover the visible history behavior, generated asset URLs, and pack
archive public URLs with tests

## Root cause
The pack detail page rendered both Submission history and Version
history from the same versions API payload, so admins saw duplicated
rows. The remaining history table also did not expose the uploaded asset
URL, and the storage contract previously treated pack archives as having
no public URL.

## Test plan
- [x] pnpm --dir web/enterprise-admin exec eslint . --max-warnings=0
--cache --cache-location .eslintcache --cache-strategy content
--ignore-pattern coverage
- [x] pnpm --dir web/enterprise-admin run test
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit

Note: `pnpm --dir web/enterprise-admin run lint` hits an ignored local
coverage artifact in this worktree
(`web/enterprise-admin/coverage/block-navigation.js`). The equivalent
eslint check above ignores coverage and passed.
```

**PR #1940: fix(enterprise): clean up pack submission history**

## Summary
- Remove the duplicated Version history section from the pack detail page
- Add per-submission asset download actions for https://agentpack.zooclaw.ai assets
- Fetch pack assets with the stored account token in the Authorization header before saving the blob
- Define the pack archive public domain in the R2 upload contract/config
- Cover the visible history behavior, authenticated asset fetch, and pack archive public URLs with tests

## Root cause
The pack detail page rendered both Submission history and Version history from the same versions API payload, so admins saw duplicated rows. The remaining history table also did not expose the uploaded asset URL. Pack asset downloads require authenticated requests, so a direct anchor link could not attach the required Authorization header.

## Test plan
- [x] pnpm --dir web/enterprise-admin exec eslint . --max-warnings=0 --cache --cache-location .eslintcache --cache-strategy content --ignore-pattern coverage
- [x] pnpm --dir web/enterprise-admin test components/packs/__tests__/SubmissionList.test.tsx app/(dashboard)/packs/[packId]/__tests__/pack-detail-page.test.tsx
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit

Note: `pnpm --dir web/enterprise-admin run lint` hits an ignored local coverage artifact in this worktree (`web/enterprise-admin/coverage/block-navigation.js`). The equivalent eslint check above ignores coverage and passed.
