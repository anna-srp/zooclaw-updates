---
title: "官网首屏视觉调整：主标题与右侧文案按钮底边对齐，宽屏留白更均衡"
type: "体验优化"
priority: "中"
date: "2026-09-22"
status: "待审核"
channels: ""
---

# 官网首屏视觉调整：主标题与右侧文案按钮底边对齐，宽屏留白更均衡

## 核心宣传点

官网首屏重新排了版：大标题和右侧「副标题 + 按钮」这一组的底边对齐，页面两侧的外部留白保持一致。首屏背景画布和界面图的位置、宽度、裁切框比例也做了调整，1728–1920px 的宽屏区间留白是连续变化的，不会在某个断点突然跳一下。现有素材、文案和交互都保留，改动只限首屏这一个区块，后续首页各区域不受影响。

## 分级

- 内部：P1
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
- 调整官网首屏布局：大标题与右侧「副标题 + 按钮」组合底边对齐，两侧外部留白保持一致。
- 按 [Harvey 官网](https://www.harvey.ai/)
的参考调整首屏背景画布和界面图的位置、宽度及裁切框比例，保留现有素材、文案和交互；1728–1920px 的宽屏留白连续变化。
- 改动仅限 `ZooworkHeroSection`，后续首页区域保持不变。

## Test plan
- [x] `bash scripts/verify-web.sh
src/app/landing/components/ZooworkHomeSections.tsx
tests/unit/app/zoowork-home-body.unit.spec.tsx`
- [x] 浏览器检查 390px、600px、900px、1024px、1025px、1440px、1920px
布局，标题与文案无重叠、无横向溢出，图片框位于背景内。1440px、1920px 下左右留白相等，标题与右侧组合底边差值为 0px。
- [x] 检查 1728px、1800px、1919px、1920px 的连续布局：1919→1920px 时画布顶部仅变化约
0.8px，既定尺寸的定位不变。
- [x] 确认后续首页区域代码未变更，`git diff --check` 通过。

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `c55ee8037b6108eafa0b6931f77e9315f6c0f40a`
- PR: #3852
- 作者：shana-srp
- 日期：2026-09-22T09:06:17Z

### Commit Message

```
style(web): align homepage hero spacing and artwork (#3852)

## Summary
- 调整官网首屏布局：大标题与右侧「副标题 + 按钮」组合底边对齐，两侧外部留白保持一致。
- 按 [Harvey 官网](https://www.harvey.ai/)
的参考调整首屏背景画布和界面图的位置、宽度及裁切框比例，保留现有素材、文案和交互；1728–1920px 的宽屏留白连续变化。
- 改动仅限 `ZooworkHeroSection`，后续首页区域保持不变。

## Test plan
- [x] `bash scripts/verify-web.sh
src/app/landing/components/ZooworkHomeSections.tsx
tests/unit/app/zoowork-home-body.unit.spec.tsx`
- [x] 浏览器检查 390px、600px、900px、1024px、1025px、1440px、1920px
布局，标题与文案无重叠、无横向溢出，图片框位于背景内。1440px、1920px 下左右留白相等，标题与右侧组合底边差值为 0px。
- [x] 检查 1728px、1800px、1919px、1920px 的连续布局：1919→1920px 时画布顶部仅变化约
0.8px，既定尺寸的定位不变。
- [x] 确认后续首页区域代码未变更，`git diff --check` 通过。

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

来源：SerendipityOneInc/ecap-workspace @ c55ee803，PR #3852，作者 shana-srp。
