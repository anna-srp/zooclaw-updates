---
title: "feat(web): rename business marketing routes to enterprise (#3726)"
type: "新功能"
priority: "中"
date: "2026-09-15"
status: "待审核"
channels: ""
---

# feat(web): rename business marketing routes to enterprise (#3726)

## 核心宣传点

## Summary

- Rename the enterprise marketing page from `/{locale}/business` to `/{locale}/enterprise` for all 10 supported locales.
- Update shared navigation/footer links, English labels to **Enterprise**, and canonical/Open Graph/hreflang URLs.
- Hide the hero eyebrow “Built for AI agents in production” only in English; preserve Chinese and all other locales.
- Preserve the enterprise page's existing rounded-corner treatment on the new route (verified automated-review finding).
- Permanently redirect legacy business page URLs to the corresponding enterprise page, retaining query parameters and browser fragments. Keep diagram assets and contact APIs unchanged.

## Test plan

- [x] Targeted Vitest suite: **209 tests passed across 12 files**, covering localization/metadata, navigation/footer, marketing chrome, redirects, SEO contracts and hero eyebrow visibility across all 10 locales.
- [x] TypeScript check passed during implementation.
- [x] Live local HTTP checks: all 10 enterprise locale pages return 200 with correct canonical URLs; all legacy locale URLs redirect with 301 and preserve query parameters.
- [x] Browser verification: English header/footer display Enterprise; a legacy URL preserves its query and `#training` anchor after redirect.
- [x] Browser verification: English hero eyebrow removed; Chinese hero eyebrow unchanged.
- [x] Browser computed-style check: enterprise contact form Submit button retains the intended 6px corner radius after the route migration.
- [x] `git diff --check`.
- Full test suite and production build are left to CI. Local preview uses preview-only environment configuration; no environment files or dependency changes are included.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `cf91f444ea83d5e8e1b331671a77acbd99c029e5`
- PR: #3726
- 作者：ericma-srp
- 日期：2026-09-15T03:19:04Z

### Commit Message

```
feat(web): rename business marketing routes to enterprise (#3726)

## Summary

- Rename the enterprise marketing page from `/{locale}/business` to
`/{locale}/enterprise` for all 10 supported locales.
- Update shared navigation/footer links, English labels to
**Enterprise**, and canonical/Open Graph/hreflang URLs.
- Hide the hero eyebrow “Built for AI agents in production” only in
English; preserve Chinese and all other locales.
- Preserve the enterprise page's existing rounded-corner treatment o
```
