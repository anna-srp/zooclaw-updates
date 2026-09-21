---
title: "fix(seo): unify public marketing English URLs (#3806)"
type: "Bug Fix"
priority: "中"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# 修复：英文营销页 URL 统一，去掉 /en 前缀

## 核心宣传点

英文版 About、Pricing、Solutions、Enterprise 四个公开页移到 /about、/pricing、/solutions、/enterprise，老的 /en/... 链接返回 301 跳转并保留原有查询参数，非英文公开页保持各自的一级语言前缀。导航、语言切换、middleware 和内部 rewrite 都改用精确的营销页白名单，通用 locale 工具、后端 URL 生成、登录、订阅、结算、API 和附件链接行为不变。canonical、语言 alternates、Enterprise 元数据和 65 条主 sitemap 已对齐，另外补齐了八个语言包里缺失的 Solutions 文案，这些语言的公开页不会再回落成英文。

## 分级

- 内部：P2
- 外部：B
- 发布状态：已上线

## PR 说明

## Summary

Move the English About, Pricing, Solutions, and Enterprise public pages to `/about`, `/pricing`, `/solutions`, and `/enterprise`. Legacy `/en/...` links return a 301 while retaining the original query string. Non-English public URLs keep their existing first-level locale.

Use an exact marketing-page allowlist for navigation, language switching, middleware, and internal rewrites. Generic locale helpers, backend URL generators, login, subscription, checkout, APIs, and attachment URLs retain their existing behavior. Align canonical, real-language alternates, Enterprise metadata, and the 65-entry main sitemap. Complete missing Solutions copy in eight existing locale dictionaries so those public locale pages do not fall back to English.

## Root cause

The public marketing URL contract previously prefixed English inner pages, while Enterprise maintained separate SEO metadata. Shared navigation therefore needed a marketing-specific resolver with the existing product resolver as its fallback.

## Test plan

- [x] Rebased onto `edd8bb8bef71e7835ab207a9e6caf000ade1d24e`; range-diff confirms the migration patch is unchanged.
- [x] Reran 352 relevant tests on the rebased branch: route allowlist, query preservation, SEO, navigation/language switching, middleware, and excluded product/API/asset paths.
- [x] Earlier local verification of the same migration patch: optimized Next build, 82/82 development HTTP checks, 82/82 built-server HTTP checks, and four page-family browser language round-trips with query/hash preservation.
- [x] Local desktop/mobile login entry and a mocked authenticated Pricing-to-subscription flow; stopped before payment. This does not claim an end-to-end payment test.
- [x] GitHub CI: 819 frontend test files, 10,336 tests passed, 70 skipped, 1 todo; lint/type checks and the compile-mode Next build passed. All 23 active checks passed; 15 conditional checks were skipped.
- [x] Both automated reviews found no issues in this migration; inspected their full comments and inline review threads (none).
- [ ] Human engineering review and production routing/cache/rollback confirmation; this PR remains a draft with auto-merge disabled.

### Known baseline verification limitation

The local build-generated type check exposes an existing `/api/download/route.ts` export error (`isAllowedUrl` is not an allowed Next route export). That source is byte-identical on this branch, its original base, and latest main. The first pre-push check failed on this error. Generated build types and the incremental cache were archived, then the normal unmodified pre-push source checks were rerun in the clean-source state used by CI. No hook was bypassed and no API source or type-check configuration was changed. A post-build generated-type check still needs that separate baseline issue resolved; a clean-source CI pass does not close it.

## Release dependencies

Keep this draft unmerged. Confirm the four public paths' actual production routing, absence of reverse redirect rules, cache handling, and a compatible rollback before release. Current production still uses prefixed English inner pages; local verification is not production acceptance.

Publish cross-site link follow-ups only after these new production URLs return the expected content and old aliases redirect correctly:

- Gallery: https://github.com/SerendipityOneInc/zoowork-agent-gallery/pull/6
- Blog: https://github.com/SerendipityOneInc/zooclaw-blog/pull/11

Gallery's own migrated paths remain unchanged; Blog's own locale migration and Tips are separate work. This task does not merge PRs, deploy production, change Worker routing, or operate GSC.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `25750ee083ba44ca26932edb0cdcce2e14f16f46`
- PR: #3806
- 作者：Mori-srp
- 日期：2026-09-20T03:38:20Z

### Commit Message

```
fix(seo): unify public marketing English URLs (#3806)

## Summary

Move the English About, Pricing, Solutions, and Enterprise public pages
to `/about`, `/pricing`, `/solutions`, and `/enterprise`. Legacy
`/en/...` links return a 301 while retaining the original query string.
Non-English public URLs keep their existing first-level locale.

Use an exact marketing-page allowlist for navigation, language
switching, middleware, and internal rewrites. Generic locale helpers,
backend URL generators, login, subscription, checkout, APIs, and
attachment URLs retain their existing behavior. Align canonical,
real-language alternates, Enterprise metadata, and the 65-entry main
sitemap. Complete missing Solutions copy in eight existing locale
dictionaries so those public locale pages do not fall back to English.

## Root cause

The public marketing URL contract previously prefixed English inner
pages, while Enterprise maintained separate SEO metadata. Shared
navigation therefore needed a marketing-specific resolver with the
existing product resolver as its fallback.

## Test plan

- [x] Rebased onto `edd8bb8bef71e7835ab207a9e6caf000ade1d24e`;
range-diff confirms the migration patch is unchanged.
- [x] Reran 352 relevant tests on the rebased branch: route allowlist,
query preservation, SEO, navigation/language switching, middleware, and
excluded product/API/asset paths.
- [x] Earlier local verification of the same migration patch: optimized
Next build, 82/82 development HTTP checks, 82/82 built-server HTTP
checks, and four page-family browser language round-trips with
query/hash preservation.
- [x] Local desktop/mobile login entry and a mocked authenticated
Pricing-to-subscription flow; stopped before payment. This does not
claim an end-to-end payment test.
- [x] GitHub CI: 819 frontend test files, 10,336 tests passed, 70
skipped, 1 todo; lint/type checks and the compile-mode Next build
passed. All 23 active checks passed; 15 conditional checks were skipped.
- [x] Both automated reviews found no issues in this migration;
inspected their full comments and inline review threads (none).
- [ ] Human engineering review and production routing/cache/rollback
confirmation; this PR remains a draft with auto-merge disabled.

### Known baseline verification limitation

The local build-generated type check exposes an existing
`/api/download/route.ts` export error (`isAllowedUrl` is not an allowed
Next route export). That source is byte-identical on this branch, its
original base, and latest main. The first pre-push check failed on this
error. Generated build types and the incremental cache were archived,
then the normal unmodified pre-push source checks were rerun in the
clean-source state used by CI. No hook was bypassed and no API source or
type-check configuration was changed. A post-build generated-type check
still needs that separate baseline issue resolved; a clean-source CI
pass does not close it.

## Release dependencies

Keep this draft unmerged. Confirm the four public paths' actual
production routing, absence of reverse redirect rules, cache handling,
and a compatible rollback before release. Current production still uses
prefixed English inner pages; local verification is not production
acceptance.

Publish cross-site link follow-ups only after these new production URLs
return the expected content and old aliases redirect correctly:

- Gallery:
https://github.com/SerendipityOneInc/zoowork-agent-gallery/pull/6
- Blog: https://github.com/SerendipityOneInc/zooclaw-blog/pull/11

Gallery's own migrated paths remain unchanged; Blog's own locale
migration and Tips are separate work. This task does not merge PRs,
deploy production, change Worker routing, or operate GSC.
```

来源：SerendipityOneInc/ecap-workspace @ 25750ee0，PR #3806，作者 Mori-srp。