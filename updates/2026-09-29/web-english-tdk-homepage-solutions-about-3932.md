---
title: "官网英文版首页、Solutions 和 About 页更新 SEO 标题与描述"
type: "Improvement"
priority: "低"
date: "2026-09-29"
status: "待审核"
channels: ""
---

# 官网英文版首页、Solutions 和 About 页更新 SEO 标题与描述

## 核心宣传点

按 SEO 服务商的关键词建议，只更新了营销站英文版的标题、描述和关键词：首页标题改为「AI Agent Platform to Build, Deploy & Run AI Agents | ZooWork」并配新描述，/solutions 改为「AI Agents for Business | ZooWork Solutions」并新增独立的 SEO 配置，/about 改为「About Serendipity One, the Company Behind ZooWork | ZooWork」并用绝对标题，让 HTML、OG 和 Twitter 三处标题一致、不再重复拼接站名后缀。SEO 配置新增了一个可选的绝对标题字段。中文、日文及其他所有语种均未改动。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

English-only TDK update for the marketing site, based on the SEO vendor's keyword recommendations (approved by 徐老师).

- `/`: title `AI Agent Platform to Build, Deploy & Run AI Agents | ZooWork`, new description
- `/solutions`: title `AI Agents for Business | ZooWork Solutions`, new description (new `solutions-seo.ts`)
- `/about`: title `About Serendipity One, the Company Behind ZooWork | ZooWork` (absolute title, so HTML/OG/Twitter titles match with no doubled suffix)
- `_seo.ts`: new optional `absoluteTitle`

zh/ja and all other locales unchanged. Tests: unit (app / lib/seo / theme) pass, lint, tsc, knip pass. New test covers the /about metadata titles.

Needs a human review before merge.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `15a8f3488511af85766d59e0999ff1a32b8d8e98`
- PR: #3932
- 作者：Mori-srp
- 日期：2026-09-29T15:08:21Z

### Commit Message

```
feat(web): update English TDK for homepage, /solutions and /about (#3932)

English-only TDK update for the marketing site, based on the SEO
vendor's keyword recommendations (approved by 徐老师).

- `/`: title `AI Agent Platform to Build, Deploy & Run AI Agents |
ZooWork`, new description
- `/solutions`: title `AI Agents for Business | ZooWork Solutions`, new
description (new `solutions-seo.ts`)
- `/about`: title `About Serendipity One, the Company Behind ZooWork |
ZooWork` (absolute title, so HTML/OG/Twitter titles match with no
doubled suffix)
- `_seo.ts`: new optional `absoluteTitle`

zh/ja and all other locales unchanged. Tests: unit (app / lib/seo /
theme) pass, lint, tsc, knip pass. New test covers the /about metadata
titles.

Needs a human review before merge.
```

来源：SerendipityOneInc/ecap-workspace @ 15a8f348，PR #3932，作者 Mori-srp。
