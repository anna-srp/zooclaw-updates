---
title: "修复：官网跳转行业解决方案页时保留当前语言，不再跳到语言不定的页面"
type: "Bug Fix"
priority: "低"
date: "2026-09-24"
status: "待审核"
channels: ""
---

# 修复：官网跳转行业解决方案页时保留当前语言，不再跳到语言不定的页面

## 核心宣传点

行业解决方案页在一个独立站点上，官网过去用的是固定链接、不带那个站点支持的语言参数，所以把官网链接文案翻译了也没用，落地页语言仍然是不确定的。现在跳转会带上语言：中文（zh）打开 ?lang=zh，英文和其他所有支持的语言打开 ?lang=en。这套共享的 URL 构造被应用到 Solutions 导航菜单、Solutions 卡片、共享与独立页脚，以及首页和企业页的行业案例——比如英文 Pricing 页现在链到 /industry/cn-cbec/?lang=en，而不是语言不指定的页面。10 个语言各 27 条行业链接都验证过，行业站内容、SEO canonical 和部署配置都没改。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary
- Preserve the main site's language when opening an industry solution: Chinese (`zh`) opens `?lang=zh`; English and every other supported locale open `?lang=en`.
- Apply the shared URL builder to the Solutions navigation menu, Solutions cards, shared and standalone footers, and homepage/enterprise industry cases. For example, English Pricing now links to `/industry/cn-cbec/?lang=en` instead of the language-unspecified page.

## Root cause
Industry links used fixed URLs without the language parameter supported by the separate industry site. Translating the main site's link labels did not select the destination page's language.

## Test plan
- [x] Scoped `scripts/verify-web.sh`: governance guards, TypeScript, 89 existing tests across 7 files, and ESLint passed.
- [x] Runtime check of all 10 supported locales: 27 industry links per locale across the navigation, Solutions catalog, and footer use the expected language.
- [x] Browser verification of English, Chinese, and German Pricing links, the English Solutions dropdown, and Chinese Solutions cards.
- [x] Local rendered-page checks for Chinese/German Solutions and Chinese homepage/enterprise industry links.
- [x] Production industry page with `?lang=en` renders English and `?lang=zh` renders Chinese; the legacy enterprise-case domain redirect preserves the query parameter.
- [x] `git diff --check`.

No industry-site content, SEO canonical URLs, or deployment configuration is changed.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `05e0720402c2b668cdb90d702c9786958c406d59`
- PR: #3899
- 作者：ericma-srp
- 日期：2026-09-24T08:49:40Z

### Commit Message

```
fix(marketing): preserve language in industry links (#3899)

## Summary
- Preserve the main site's language when opening an industry solution:
Chinese (`zh`) opens `?lang=zh`; English and every other supported
locale open `?lang=en`.
- Apply the shared URL builder to the Solutions navigation menu,
Solutions cards, shared and standalone footers, and homepage/enterprise
industry cases. For example, English Pricing now links to
`/industry/cn-cbec/?lang=en` instead of the language-unspecified page.

## Root cause
Industry links used fixed URLs without the language parameter supported
by the separate industry site. Translating the main site's link labels
did not select the destination page's language.

## Test plan
- [x] Scoped `scripts/verify-web.sh`: governance guards, TypeScript, 89
existing tests across 7 files, and ESLint passed.
- [x] Runtime check of all 10 supported locales: 27 industry links per
locale across the navigation, Solutions catalog, and footer use the
expected language.
- [x] Browser verification of English, Chinese, and German Pricing
links, the English Solutions dropdown, and Chinese Solutions cards.
- [x] Local rendered-page checks for Chinese/German Solutions and
Chinese homepage/enterprise industry links.
- [x] Production industry page with `?lang=en` renders English and
`?lang=zh` renders Chinese; the legacy enterprise-case domain redirect
preserves the query parameter.
- [x] `git diff --check`.

No industry-site content, SEO canonical URLs, or deployment
configuration is changed.
```

来源：SerendipityOneInc/ecap-workspace @ 05e07204，PR #3899，作者 ericma-srp。