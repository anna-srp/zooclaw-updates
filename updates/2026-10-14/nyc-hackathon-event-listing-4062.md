---
title: "官网活动页上线纽约 Fashion and Finance 黑客松，可直接跳转报名"
type: "其他公告"
priority: "中"
date: "2026-10-14"
status: "待审核"
channels: ""
---

# 官网活动页上线纽约 Fashion and Finance 黑客松，可直接跳转报名

## 核心宣传点

官网活动页里纽约那场「即将举行」的活动从占位状态更新为正式信息：Fashion and Finance Hackathon with ZooWork。卡片新增官方 AI Tinkerers 活动链接和可见的「View event details」入口，用户可以直接点进去看详情与报名；活动主视觉以响应式卡片展示，完整保留原图构图，并以体积约 196 KB 的 WebP 优化资源提供。活动链接与主视觉也一并写入页面生成的 Event 结构化数据，便于搜索引擎识别。活动维护指南和单元测试覆盖同步更新。纯前端内容更新，无需后端配套发版。

## 分级

- 内部：P2
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `ebc85775144ebae3a3772f332289edd074823b34`
- PR: #4062
- 作者：anna-srp
- 日期：2026-10-14T02:50:43Z

### Commit Message

```
feat(marketing): feature the NYC hackathon event (#4062)

## What

Updates the upcoming New York event from its placeholder state to the
official **Fashion and Finance Hackathon with ZooWork** listing.

- Adds the official AI Tinkerers event URL and a visible **View event
details** link.
- Features the supplied event artwork in a responsive upcoming-event
card.
- Serves the artwork as an optimized WebP asset (about 196 KB) while
preserving its full composition.
- Includes the event URL and artwork in the generated Event JSON-LD.
- Updates the event maintenance guide and unit coverage.

Event page:
https://nyc.aitinkerers.org/p/fashion-and-finance-hackathon-with-zoowork

## Validation

- Event URL returns HTTP 200 and its title matches the page copy.
- Local desktop and narrow-screen previews render the full artwork
without cropping its title, date, or partner logos.
- `events-schema.unit.spec.ts`: 12 tests passed.
- Prettier, ESLint, and `tsc --noEmit` passed for the changed files.

---------

Co-authored-by: Yueru Wang <yueruwang@Yuerus-MacBook-Air.local>
```

