---
title: "体验优化：官网活动页改用 ZooWork 品牌视觉，无活动时自动隐藏「即将举行」"
type: "体验优化"
priority: "低"
date: "2026-10-13"
status: "待审核"
channels: ""
---

# 体验优化：官网活动页改用 ZooWork 品牌视觉，无活动时自动隐藏「即将举行」

## 核心宣传点

把 /events 活动页对齐到 ZooWork 官网的设计语言和已确认的桌面/移动端版式。即将举行的活动改为文字在左、日期在右，与下方往期列表保持相同外边界；复用共享营销容器与设计系统按钮，控件圆角 6px、卡片 12px 统一，鼠标指针为手型，键盘焦点可见。英雄区改为居中，往期导航简化成文字筛选。没有即将举行的活动时，英雄区链接和整个区块会自动隐藏，往期列表仍可正常使用。纯前端改动。

## 分级

- 内部：P3
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `bdb8801b9a30bd24e64f16960343852905b82464`
- PR: #4063
- 作者：shana-srp
- 日期：2026-10-13T06:49:55Z

### Commit Message

```
style(events): align page with ZooWork branding (#4063)

## Summary

Align `/events` with ZooWork's marketing design language and the
approved desktop/mobile layout. The upcoming event now groups its text
on the left and date on the right while keeping the same outer edges as
the archive.

- Reuse shared marketing containers, ZooWork tokens and design-system
buttons, with consistent 6px control / 12px card radii, hand cursors and
visible keyboard focus.
- Center the hero, simplify archive navigation into text filters, and
align the community section and its primary/secondary actions.
- Consolidate duplicate event copy, retain the original Didot event
typography and `#7D7895` announcement color, and remove unused upcoming
fields from the data, tests and maintenance guide.
- Hide both the Upcoming hero link and section when no upcoming events
exist, while keeping the archive and its filters available. Remove an
unused page marker and clarify the documented heading structure.

## Test plan

- [x] Updated to latest `main` (`b971edece7`) before committing.
- [x] `scripts/verify-web.sh` on affected Events source/tests:
TypeScript, targeted ESLint, governance guards and all 14 Events tests
passed, including empty-upcoming navigation and archive filtering.
- [x] Commit hook's full frontend lint, Prettier and `git diff --check`
passed.
- [x] Browser verification at 1280px and 393px: container alignment,
responsive card order, no horizontal overflow, filters/counts, section
anchors, links, keyboard focus and cursor styling.

## Screenshots

Desktop:

![Events
desktop](https://github.com/SerendipityOneInc/ecap-workspace/blob/fcc67e8135e327730134976454f7900c9ac6d5a8/docs/superpowers/specs/assets/events-visual-unification-desktop.png?raw=true)

Mobile upcoming card:

![Events
mobile](https://github.com/SerendipityOneInc/ecap-workspace/blob/fcc67e8135e327730134976454f7900c9ac6d5a8/docs/superpowers/specs/assets/events-visual-unification-mobile.png?raw=true)

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

