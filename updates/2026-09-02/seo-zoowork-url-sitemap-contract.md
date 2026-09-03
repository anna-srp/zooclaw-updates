---
title: "官网 URL 体系统一：多语言地址、跳转与站点地图有了唯一事实来源"
type: "体验优化"
priority: "中"
date: "2026-09-02"
status: "待审核"
channels: "Discord+changelog"
---

# 官网 URL 体系统一：多语言地址、跳转与站点地图有了唯一事实来源

## 核心宣传点

把 ZooWork 官网的公开营销页面收敛到一套统一的 URL 契约上，路由、跳转、页面元信息、导航和站点地图 XML 全部由它生成，不再各写各的。

具体变化：首页、About、Pricing、Solutions 四个页面在 10 种语言下都有各自真实可访问的地址；显式写明语言的 URL 优先级高于 `NEXT_LOCALE` Cookie 和浏览器 `Accept-Language`，也就是你分享出去的链接是哪个语言，对方打开就是哪个语言；英文首页固定在 `/` 直接返回 200，只有 `/en` 这个别名会跳到 `/`；不带语言的 About / Pricing / Solutions 别名一律一跳到位（301）到英文正式地址。

canonical、双向 hreflang 和英文 `x-default` 只从每个页面真实声明的可用语言生成，避免指向不存在的地址。法务类页面保持无语言前缀且为 canonical，别名不收录；Contact 页面下线，直接 404 且不再产出任何元信息。站点地图 `sitemap-main.xml` 由路由契约生成，根索引只允许包含四个已审定的子站点地图。另外加了一套生产环境的 GET 巡检，覆盖状态码、跳转、可收录性、canonical、hreflang、语言标记、robots、XML 以及老域名残留。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `aadea62d2beb125d4d0ba3ebe9c69ed05e4e1e29`
- PR: #3593
- 作者: Mori-srp
- 日期: 2026-09-02T08:26:44Z

### Commit Message

```
feat(seo): establish ZooWork URL and sitemap contract (#3593)

## Summary

Establish one ZooWork URL contract as the source of truth for public
marketing routes, redirects, metadata, navigation, and XML generation.

- Make Home, About, Pricing, and Solutions available at their ten real
locale URLs.
- Keep explicit locale URLs authoritative over `NEXT_LOCALE` and
`Accept-Language`.
- Serve the English homepage at `/` as a stable direct 200; redirect
only the exact `/en` alias to `/`.
- Make bare About, Pricing, and Solutions aliases one-hop 301s to their
English final URLs.
- Generate canonical, reciprocal hreflang, and English `x-default` only
from each page's real `availableLocales` contract.
- Keep locale-free Legal pages canonical and exclude aliases; retire
Contact as a direct 404 with no metadata surface.
- Generate `sitemap-main.xml` from the route contract and constrain the
root index to its four approved leaf sitemaps.
- Add production GET auditing for status, redirects, indexability,
canonical, hreflang, language markers, robots, XML, and legacy-domain
leakage.

## Local acceptance

- [x] Merged the latest `origin/main@8d3cdb5a8` without conflict.
- [x] `bash scripts/verify-changed.sh` — governance guards, TypeScript,
and ESLint passed.
- [x] All 19 changed unit-test files passed: 338/338 tests.
- [x] Home / About / Pricing / Solutions: 40/40 final locale URLs
returned direct 200 in the local runtime audit.
- [x] `/` remained direct 200 across no preference, Cookie,
`Accept-Language`, and conflicting-preference requests.
- [x] Local main-site audit: canonical, hreflang, alias, disabled route,
language marker, and legacy-domain issue counts were all zero.
- [x] `sitemap-main.xml`: exactly 55 contract-derived URLs, with no
missing, extra, or duplicate entry.
- [x] Root sitemap index: exactly four approved leaf sitemaps.
- [x] Legacy `/features` and `/:locale/features` aliases now use
explicit one-hop 301 responses; focused config tests passed 3/3.

The production build completed code compilation, but local static
prerender cannot be marked fully passed because this environment does
not contain a valid Firebase API key for the untouched `/en/features`
and `/en/contact` collection paths. CI `web-build-check` remains the
authoritative build gate.

## PR size exception

The repository size gate reports 3,549 changed lines against a
3,000-line threshold (`+2,790 / -759`), so this PR intentionally uses
the repository-supported `size-override` label. The 549-line excess is
dominated by the contract-coupled production GET auditor
(`audit-public-seo.ts`, 1,151 lines), its regression tests, and the
40-route content-readiness fixture. Keeping these gates with the URL
behavior ensures the release SHA cannot publish the XML/metadata change
without its production acceptance contract. This exception does not
waive TypeScript, ESLint, build, unit-test, CodeQL, review, or
production GET gates.

## Release boundary

This PR may merge to `main` and deploy to staging after current CI and
review pass, but it must not be released to production until all of the
following are true:

1. Tips, Industry D1, and Docs changes are deployed to production and
have fresh GET receipts.
2. The Blog leaf sitemap has a fresh release-window 200/readback
receipt.
3. The stacked brand-scope PR B is rebased onto main, reviewed, merged,
and included in the same locked production SHA.
4. The production release uses an immutable `ecap-vX.Y.Z-release`
tag/ref whose SHA exactly equals the approved locked main SHA.

The local all-surface audit intentionally still rejects 14
external-owner routes until their production deployments exist: three
external leaf sitemaps and eleven Industry detail pages. Do not treat
local XML generation or this PR's CI as production acceptance.

After production deployment, run:

```bash
cd web/app
pnpm exec tsx scripts/audit-public-seo.ts --phase main-production --root https://zoowork.ai/sitemap.xml
```

## Out of scope

- Industry hall redirect D2.
- Google Search Console submission.
- Unapproved repository-wide replacement of legal/history/tracking
identifiers.
- The four temporary legacy social-account URLs, which remain a
separately documented B exception until official ZooWork accounts exist.
```

### PR Body

```
## Summary

Establish one ZooWork URL contract as the source of truth for public marketing routes, redirects, metadata, navigation, and XML generation.

- Make Home, About, Pricing, and Solutions available at their ten real locale URLs.
- Keep explicit locale URLs authoritative over `NEXT_LOCALE` and `Accept-Language`.
- Serve the English homepage at `/` as a stable direct 200; redirect only the exact `/en` alias to `/`.
- Make bare About, Pricing, and Solutions aliases one-hop 301s to their English final URLs.
- Generate canonical, reciprocal hreflang, and English `x-default` only from each page's real `availableLocales` contract.
- Keep locale-free Legal pages canonical and exclude aliases; retire Contact as a direct 404 with no metadata surface.
- Generate `sitemap-main.xml` from the route contract and constrain the root index to its four approved leaf sitemaps.
- Add production GET auditing for status, redirects, indexability, canonical, hreflang, language markers, robots, XML, and legacy-domain leakage.

## Local acceptance

- [x] Merged the latest `origin/main@8d3cdb5a8` without conflict.
- [x] `bash scripts/verify-changed.sh` — governance guards, TypeScript, and ESLint passed.
- [x] All 19 changed unit-test files passed: 338/338 tests.
- [x] Home / About / Pricing / Solutions: 40/40 final locale URLs returned direct 200 in the local runtime audit.
- [x] `/` remained direct 200 across no preference, Cookie, `Accept-Language`, and conflicting-preference requests.
- [x] Local main-site audit: canonical, hreflang, alias, disabled route, language marker, and legacy-domain issue counts were all zero.
- [x] `sitemap-main.xml`: exactly 55 contract-derived URLs, with no missing, extra, or duplicate entry.
- [x] Root sitemap index: exactly four approved leaf sitemaps.
- [x] Legacy `/features` and `/:locale/features` aliases now use explicit one-hop 301 responses; focused config tests passed 3/3.

The production build completed code compilation, but local static prerender cannot be marked fully passed because this environment does not contain a valid Firebase API key for the untouched `/en/features` and `/en/contact` collection paths. CI `web-build-check` remains the authoritative build gate.

## PR size exception

The repository size gate reports 3,549 changed lines against a 3,000-line threshold (`+2,790 / -759`), so this PR intentionally uses the repository-supported `size-override` label. The 549-line excess is dominated by the contract-coupled production GET auditor (`audit-public-seo.ts`, 1,151 lines), its regression tests, and the 40-route content-readiness fixture. Keeping these gates with the URL behavior ensures the release SHA cannot publish the XML/metadata change without its production acceptance contract. This exception does not waive TypeScript, ESLint, build, unit-test, CodeQL, review, or production GET gates.

## Release boundary

This PR may merge to `main` and deploy to staging after current CI and review pass, but it must not be released to production until all of the following are true:

1. Tips, Industry D1, and Docs changes are deployed to production and have fresh GET receipts.
2. The Blog leaf sitemap has a fresh release-window 200/readback receipt.
3. The stacked brand-scope PR B is rebased onto main, reviewed, merged, and included in the same locked production SHA.
4. The production release uses an immutable `ecap-vX.Y.Z-release` tag/ref whose SHA exactly equals the approved locked main SHA.

The local all-surface audit intentionally still rejects 14 external-owner routes until their production deployments exist: three external leaf sitemaps and eleven Industry detail pages. Do not treat local XML generation or this PR's CI as production acceptance.

After production deployment, run:

```bash
cd web/app
pnpm exec tsx scripts/audit-public-seo.ts --phase main-production --root https://zoowork.ai/sitemap.xml
```

## Out of scope

- Industry hall redirect D2.
- Google Search Console submission.
- Unapproved repository-wide replacement of legal/history/tracking identifiers.
- The four temporary legacy social-account URLs, which remain a separately documented B exception until official ZooWork accounts exist.

```

