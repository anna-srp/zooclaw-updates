---
title: "官网活动页补上 10 月两场活动回顾，卡片封面统一"
type: "其他公告"
priority: "低"
date: "2026-10-21"
status: "待审核"
channels: ""
---

# 官网活动页补上 10 月两场活动回顾，卡片封面统一

## 核心宣传点

官网 Events 页此前缺少 10 月 14 日 BytePlus 展会和 10 月 17 日复旦论坛两场活动，且过往活动卡片默认每场都有外部来源链接。本次补上这两场活动的已审图片与按角色区分的文案，BytePlus 卡片因无公开来源链接保持静态展示；所有过往活动统一为一张不被遮挡的封面图、标签放在图片下方，同时有回顾又有原活动页的活动仍优先展示回顾入口。页面正文字体改为显式的 Inter / Noto Sans 组合，与市场物料排版一致并提供可预期的中日韩字体回退。

## 分级

- 内部：P3
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `61819da69b0545201be75e651f29cb634de02b4d`
- PR: #4088
- 作者：anna-srp
- 日期：2026-10-21T02:59:46Z

### Commit Message

```
feat(web): add October event recaps (#4088)

The Events page was missing ZooWork’s October 14 BytePlus showcase and
October 17 Fudan forum, and past-event cards assumed every event had an
external source link.

This change adds both events with approved photography and role-aware
copy, keeps the BytePlus card static because no public source link is
available, and standardizes every past event on one unobstructed cover
image with labels below the image. It also preserves recap-first actions
for events that have both a recap and an original event page.

The explicit Inter/Noto Sans body stack aligns the page with ZooWork’s
marketing typography and provides a predictable CJK fallback. Follow-up
review fixes preserve bottom spacing on source-less cards and document
the optional `url`/`cta` pair for future event updates.

Validation:
- ESLint on the Events page files and unit test
- 15 Events unit tests
- TypeScript typecheck
- Visual review at mobile and desktop widths

---------

Co-authored-by: Yueru Wang <yueruwang@Yuerus-MacBook-Air.local>
```

