---
title: "官网首页头图改版：新文案、新视觉素材，页脚 tagline 一并更新"
type: "体验优化"
priority: "中"
date: "2026-08-31"
status: "待审核"
channels: "Discord+changelog"
---

# 官网首页头图改版：新文案、新视觉素材，页脚 tagline 一并更新

## 核心宣传点

官网首页顶部的标题、副标题、按钮排布和字体做了一轮刷新，页脚的 tagline 也一起换了，所有支持的语言版本同步生效。头图背景和产品界面截图换成了新的高清素材，界面图保留 16px 圆角。文案、素材来源、布局类名和各语言词条都补了回归测试覆盖。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `40a5897c1a0e8f55692292fdc2f259e67afd4ea4`
- PR: #3578
- 作者: shana-srp
- 日期: 2026-08-31T06:14:34Z

### Commit Message

```
feat(landing): refresh homepage hero content (#3578)

## Linear

N/A

## Summary

- Refresh the homepage hero title, subtitle, CTA alignment, typography,
and footer tagline across all supported locales.
- Replace the hero background and product interface with the supplied
high-resolution assets; preserve the interface at a 16 px radius.
- Add regression coverage for hero copy, media sources, layout classes,
and localized dictionaries.

## Test plan

- [x] `pnpm exec vitest run
tests/unit/app/zoowork-home-body.unit.spec.tsx
tests/unit/locales/zoowork-home-dictionary.unit.spec.ts
tests/unit/app/marketing-chrome.unit.spec.tsx
tests/unit/app/landing-footer.unit.spec.tsx` (58 tests)
- [x] `bash scripts/verify-changed.sh`
- [x] `node web/scripts/check-asset-size.mjs --mode=ci
--base=origin/main --head=HEAD`

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Description

```
## Linear

N/A

## Summary

- Refresh the homepage hero title, subtitle, CTA alignment, typography, and footer tagline across all supported locales.
- Replace the hero background and product interface with the supplied high-resolution assets; preserve the interface at a 16 px radius.
- Add regression coverage for hero copy, media sources, layout classes, and localized dictionaries.

## Test plan

- [x] `pnpm exec vitest run tests/unit/app/zoowork-home-body.unit.spec.tsx tests/unit/locales/zoowork-home-dictionary.unit.spec.ts tests/unit/app/marketing-chrome.unit.spec.tsx tests/unit/app/landing-footer.unit.spec.tsx` (58 tests)
- [x] `bash scripts/verify-changed.sh`
- [x] `node web/scripts/check-asset-size.mjs --mode=ci --base=origin/main --head=HEAD`

```

## 备注

纯前端 marketing 页面改动，无后端依赖。已通过资源体积检查（check-asset-size）。
