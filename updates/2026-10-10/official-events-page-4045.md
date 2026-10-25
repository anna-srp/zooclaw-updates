---
title: "官网上线活动页 /events，可查看 ZooWork 线下与社区活动"
type: "其他公告"
priority: "中"
date: "2026-10-10"
status: "待审核"
channels: ""
---

# 官网上线活动页 /events，可查看 ZooWork 线下与社区活动

## 核心宣传点

zoowork.ai/events 正式上线，用户可在官网直接浏览 ZooWork 活动列表。页面建在主站内、复用统一头尾，目前仅英文版；/en/events 会 301 跳到 /events，非英文路径（如 /zh/events）由中间件返回真实 404（此前父级 loading.tsx 会先流式返回 200）。导航 Resources 下新增 Events 入口，sitemap 重新生成共 66 个地址，SEO 补齐标题描述、canonical、分享图与 7 条 Event 结构化数据。活动内容集中在 events-data.ts，市场改一个文件即可更新。

## 分级

- 内部：P2
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 备注

取代 #4042 与独立仓库方案 zoowork-events#1，独立仓库路线已放弃。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `d38db0883ba0d3284949da07624af70ee9c2bf05`
- PR: #4045
- 作者：Mori-srp
- 日期：2026-10-10T08:52:35Z

### Commit Message

```
feat(marketing): add official Events page at /events (#4045)

## What

Adds an official Events page at `https://zoowork.ai/events`, built
inside the main site so it uses the shared `LandingHeader` /
`LandingFooter`.

- Page under `web/app/src/app/[locale]/(marketing)/events/`; English
only (`availableLocales: ['en']`).
- `/en/events` 301s to `/events`; non-English `/events` (e.g.
`/zh/events`) return a real 404 from middleware (the page-level
`notFound()` streamed a 200 because of the parent `loading.tsx`).
- Resources nav gets `Events` (internal link, same tab). Footer
unchanged.
- `sitemap-main.xml` regenerated with `https://zoowork.ai/events` (66
URLs). Root `sitemap.xml` unchanged.
- SEO: title, description, canonical, OG/Twitter share image (1200×630),
and 7 `Event` JSON-LD items generated from the same data as the visible
cards.
- All event content lives in `events-data.ts` so marketing can update
events by editing one file.

Supersedes #4042 and SerendipityOneInc/zoowork-events#1 (separate-repo
approach dropped).

## Checks run locally

Prettier, ESLint, `tsc --noEmit`, 272 unit tests in the affected suites
plus a new `events-schema` spec, middleware suites (159). Manual:
`/events` 200, `/en/events` 301, `/zh/events` 404.

No UTM on internal links. No new analytics or consent code.

---------

Co-authored-by: Mori-srp <266966641+Mori-srp@users.noreply.github.com>
```

