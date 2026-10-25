---
title: "官网 robots.txt 开放博客站点地图，并允许 Gemini 抓取公开页面"
type: "其他公告"
priority: "低"
date: "2026-10-10"
status: "待审核"
channels: ""
---

# 官网 robots.txt 开放博客站点地图，并允许 Gemini 抓取公开页面

## 核心宣传点

调整 zoowork.ai 的 robots.txt 两处：一是在根 sitemap 旁新增 Blog 站点地图声明（blog/sitemap-index.xml），让搜索引擎能发现全部博客文章；Blog 本身就是 sitemap index，所以直接在 robots.txt 声明而非嵌进根索引，Tips 栏目内容质量仍在整改、有意不加。二是移除对 Google-Extended 的 Disallow，允许 Gemini 使用我们的公开页面；GPTBot、ClaudeBot、CCBot 等其他 AI 爬虫封禁规则不变。用户侧无可见变化，主要影响搜索与 AI 产品对公开内容的收录。

## 分级

- 内部：P3
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 备注

audit-public-seo.ts 在 main 上本来就失败（期望 2 个根 sitemap 子项，实际 3 个，agent-gallery 新增所致），属于既有问题，不在本次范围内。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `85f50312c0011b0bd66cc00a023e620dfe8e6f10`
- PR: #4041
- 作者：Mori-srp
- 日期：2026-10-10T08:52:23Z

### Commit Message

```
feat(seo): advertise blog sitemap in robots.txt and allow Google-Extended (#4041)

## What

Two small changes to `robots.txt` on zoowork.ai:

1. **Advertise the Blog sitemap.** Add `Sitemap:
https://zoowork.ai/blog/sitemap-index.xml` next to the existing root
sitemap, so search engines can discover all Blog posts. The Blog index
is itself a sitemap index, so it is declared in `robots.txt` instead of
being nested inside the root index. Tips is intentionally **not** added
(content quality still being fixed).
2. **Allow `Google-Extended`.** Remove the `Disallow: /` rule for
`Google-Extended`, so Gemini can use our public pages. All other AI
crawler blocks (GPTBot, ClaudeBot, CCBot, Applebot-Extended, Amazonbot,
meta-externalagent) are unchanged.

## Also updated

- `web/app/scripts/audit-public-seo.ts`: expected sitemap directives now
include the Blog index.
- `tests/unit/app/_seo.unit.spec.ts`: asserts exactly these two sitemap
lines.
- `docs/seo/zoowork_marketing_url_contract.md`: records the 2026-10-09
decision.

## Checks

- `_seo.unit.spec.ts`: 18 passed.
- Reviewed separately; no blocking issues.

Note: `audit-public-seo.ts` already fails on `main` because it expects 2
root sitemap children while `public/sitemap.xml` has 3 (agent-gallery
was added). That is pre-existing and not touched here.

---------

Co-authored-by: Mori-srp <266966641+Mori-srp@users.noreply.github.com>
```

