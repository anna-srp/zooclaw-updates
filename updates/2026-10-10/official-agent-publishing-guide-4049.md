---
title: "官网上线 Agent 发布指南页，中英双语可直接访问"
type: "其他公告"
priority: "中"
date: "2026-10-10"
status: "待审核"
channels: ""
---

# 官网上线 Agent 发布指南页，中英双语可直接访问

## 核心宣传点

ZooWork 官网新增正式的 Agent 发布指南页，英文 zoowork.ai/guides/publish-agent、中文 /zh/guides/publish-agent 均可直接访问，/en/... 会 301 跳到规范英文地址，其他语种返回 404。内容来自内部指南 v2.01，完整覆盖发布 Agent 的六个阶段，Resources 下拉新增「Publishing Guide」入口。SEO 补齐 canonical、多语言声明与 HowTo 结构化数据，两个地址已写入 sitemap。截图里的 API Key token 列已遮挡。纯前端内容。

## 分级

- 内部：P2
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 备注

与 Events 页（#4045）合并了同一处 locale 兜底逻辑，上线后建议回归两个页面的多语言 404 行为。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `194efc7720f0e4bd16fb1030f6cbdb86f8aaaf03`
- PR: #4049
- 作者：Mori-srp
- 日期：2026-10-10T12:20:19Z

### Commit Message

```
feat(marketing): add agent publishing guide at /guides/publish-agent (#4049)

## What

Adds the ZooWork Agent publishing guide as an official marketing page,
in English and Chinese.

- English: `https://zoowork.ai/guides/publish-agent` · Chinese:
`https://zoowork.ai/zh/guides/publish-agent`. `/en/guides/publish-agent`
301s to the canonical English URL; other locales return 404.
- Uses the shared `MarketingChrome` header and footer. Resources
dropdown is now Blog, Docs, Publishing Guide, Events (hrefs collected in
`resource-hrefs.ts`). Footer unchanged.
- SEO: absolute title, description, single H1, self canonical, hreflang
`en` / `zh` / `x-default`, `HowTo` JSON-LD with the six stages, both
URLs in `sitemap-main.xml` (regenerated with `pnpm
render:sitemap-main`).
- Content ported from the internal guide v2.01 (Chinese text verbatim,
English from the guide's own translation). The in-page language toggle,
personal `workers.dev` demo link and internal Feishu link are not
published.
- API key screenshot: the token column is covered with a gray box on the
original image.
- Styles in Tailwind only (no route-level CSS). README in the guide
folder for future edits.

## Reconciled with Events (#4045)

Merged latest `main`. One shared fallback: a locale a route does not
offer goes to that locale's homepage in the language switcher, and
middleware returns 404 for it. The Events-only middleware branch is
replaced by this generic rule; `/zh/events` is still 404 and
`/en/events` still 301.

## Checks

Prettier, full ESLint, `tsc --noEmit`, 332 unit tests across events,
guides, route contract, sitemap, middleware, LanguageContext, LocaleLink
and landing-content. Manual: `/events`, `/guides/publish-agent`,
`/zh/guides/publish-agent` 200; `/zh/events`, `/ja/guides/publish-agent`
404.

No UTM on internal links.

---------

Co-authored-by: Mori-srp <266966641+Mori-srp@users.noreply.github.com>
```

