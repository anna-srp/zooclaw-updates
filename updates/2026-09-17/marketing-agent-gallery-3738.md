---
title: "feat(marketing): add Agent Gallery to Solutions and navigation (#3738)"
type: "新功能"
priority: "中"
date: "2026-09-17"
status: "待审核"
channels: ""
---

# feat(marketing): add Agent Gallery to Solutions and navigation (#3738)

## 核心宣传点

官网 Solutions 上新 Agent Gallery：导航拆成 Agent Gallery 和 Industry 两组，页脚也加了 Gallery 入口，中英文站点都能直接逛现成 Agent。

## PR 说明

Solutions currently lists only industries. This change adds Agent Gallery above Industries, groups the Solutions navigation into Agent Gallery and Industry, and adds a Gallery footer link. English and Chinese chrome point to the initial English Gallery at `https://zoowork.ai/en/agent-gallery`; no links point to chatgpt.site. The grouped navigation uses named sections and native link lists with focus and Escape handling.

Gallery pages and reports live in [zoowork-agent-gallery](https://github.com/SerendipityOneInc/zoowork-agent-gallery). Its independent Worker owns `/en/agent-gallery`, its descendants, and `/agent-gallery-assets/*`. This PR adds `/en/agent-gallery/sitemap.xml` to the main site's root sitemap. It includes the industry-card presentation from #3734 so reviewers can assess the complete Solutions page.

**Release gate:** keep this PR in draft until [Gallery PR #1](https://github.com/SerendipityOneInc/zoowork-agent-gallery/pull/1) is approved and merged, Guangbin completes Workers Builds setup, and the official directory, all 10 details, assets, reports and sitemap pass production checks. Publish the main-site entry and sitemap only afterward. Analytics is not yet connected in the independent Worker.

Validation: main-app TypeScript and ESLint passed; all seven header regressions and eight affected link/sitemap tests pass. All final-commit CI checks passed, including web-quality, web-build-check and CodeQL. Automated review confirmed the prior navigation accessibility finding is resolved. English/Chinese Solutions and the two-column menu were inspected locally. The independent Gallery passed its production build and local Worker checks for 11 pages, 64 referenced assets/reports, five negative routes, preview noindex and 11 sitemap URLs; all ten detail pages were checked at 390px without horizontal overflow. The formal route remained 404 at the last live check, so the complete production click path is still pending.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `1d3913df3fc08db883a025119907bd35bc934f9b`
- PR: #3738
- 作者：Mori-srp
- 日期：2026-09-17T06:39:17Z

### Commit Message

```
feat(marketing): add Agent Gallery to Solutions and navigation (#3738)

Solutions currently lists only industries. This change adds Agent
Gallery above Industries, groups the Solutions navigation into Agent
Gallery and Industry, and adds a Gallery footer link. English and
Chinese chrome point to the initial English Gallery at
`https://zoowork.ai/en/agent-gallery`; no links point to chatgpt.site.
The grouped navigation uses named sections and native link lists with
focus and Escape handling.

Gallery pages and reports live in
[zoowork-agent-gallery](https://github.com/SerendipityOneInc/zoowork-agent-gallery).
Its independent Worker owns `/en/agent-gallery`, its descendants, and
`/agent-gallery-assets/*`. This PR adds `/en/agent-gallery/sitemap.xml`
to the main site's root sitemap. It includes the industry-card
presentation from #3734 so reviewers can assess the complete Solutions
page.

**Release gate:** keep this PR in draft until [Gallery PR
#1](https://github.com/SerendipityOneInc/zoowork-agent-gallery/pull/1)
is approved and merged, Guangbin completes Workers Builds setup, and the
official directory, all 10 details, assets, reports and sitemap pass
production checks. Publish the
```
