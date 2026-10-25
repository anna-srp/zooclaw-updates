---
title: "官网首页与页脚新增 Product Hunt「每日第一」徽章"
type: "其他公告"
priority: "低"
date: "2026-10-09"
status: "待审核"
channels: ""
---

# 官网首页与页脚新增 Product Hunt「每日第一」徽章

## 核心宣传点

官网首页主标题上方新增了 ZooWork 的 Product Hunt 官方「#1 Product of the Day」徽章，左对齐、与标题留 24px 间距；页脚品牌介绍下方也放了一枚。两处徽章以及页脚的 Product Hunt 图标都会跳转到官方获奖页面，使用的是经核对的 ZooWork 发布 ID 与官方 SVG 素材，带无障碍替代文本和清晰的键盘聚焦样式。布局上复用了原有的 Hero 留白和响应式尺寸，标题位置不变，1440px 与 390px 两种宽度下都不会出现横向溢出。

## 分级

- 内部：P3
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `da4c7efdd9e0b81ea62bed11b1b6f453d5ef90f6`
- PR: #4031
- 作者：shana-srp
- 日期：2026-10-09T08:21:27Z

### Commit Message

```
feat(landing): add ZooWork Product Hunt award badge (#4031)

## Summary
- Show ZooWork's official #1 Product of the Day badge above the homepage
headline, left-aligned with 24px spacing, and beneath the footer brand
description.
- Link both badges and the footer Product Hunt icon to
https://www.producthunt.com/products/zoowork/awards. Use the verified
ZooWork launch ID (1259794) and the official SVG, with accessible image
text and visible keyboard focus.
- Use existing hero whitespace and responsive sizing to preserve the
headline position and avoid overflow.

## Test plan
- [x] Homepage unit tests: 64 passed.
- [x] Footer / marketing chrome tests: 34 passed.
- [x] Final `verify-web.sh --no-test` passed: governance guards,
TypeScript, and targeted ESLint. Formatting and pre-commit full ESLint
also passed.
- [x] CI-equivalent Next.js compile build passed.
- [x] Browser verification at 1440px and 390px: official SVG loads,
badge aligns with the headline, and there is no horizontal overflow.
- Full production build compiles, but prerendering fails because local
Firebase configuration is missing.

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

