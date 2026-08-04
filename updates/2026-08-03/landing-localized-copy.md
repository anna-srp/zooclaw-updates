---
title: "官网多语言文案补全"
type: "体验优化"
priority: "低"
date: "2026-08-03"
status: "待审核"
channels: ""
---

## 核心宣传点

首页文案、示例提示词和模板信息现已完整支持多种语言（含日、韩、法、德、意、西、阿、葡），非英文用户不再看到英文兜底。

## 原始内容

**Commit**: `a813d96f8024d73ab484ad62dd1e55b7db3579bd` — shana-srp — 2026-08-03T08:18:59Z

### Commit Message

```
fix(landing): complete localized starter copy (#3201)

## Summary

- align the landing-page hero, category labels, and footer copy with the
latest English source across all supported locales
- localize all starter prompt titles and prompt bodies instead of
forcing non-English locales to fall back to English
- localize slide-template names, metadata, descriptions, tags, and
best-use copy for every supported language
- restore the wide landing template-preview layout and add regression
coverage

## Root cause

The landing dictionaries only overrode a subset of the latest English
copy, while `getStarterPromptTranslation` explicitly forced every locale
except English and Chinese back to English. Template metadata supported
only English and Chinese. Separately, the shared dialog's responsive
`sm:max-w-lg` default overrode the landing preview's intended wide
layout.

## Test plan

- [x] ESLint for all changed locale, catalog, copy, and test files
- [x] locale/catalog unit tests: 10 passed
- [x] chat-ui starter component tests: 14 passed
- [x] prompt-key completeness audit: 0 missing keys for zh, ja, ko, fr,
de, it, es, ar, and pt
- [x] local preview routes returned HTTP 200

## Notes

- Full `tsc` remains blocked by a pre-existing `AgentPickerProps.open`
error on current `main`, unrelated to this PR.
- Template preview images contain baked-in source-language text and are
intentionally not dynamically translated.

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

```
## Summary

- align the landing-page hero, category labels, and footer copy with the latest English source across all supported locales
- localize all starter prompt titles and prompt bodies instead of forcing non-English locales to fall back to English
- localize slide-template names, metadata, descriptions, tags, and best-use copy for every supported language
- restore the wide landing template-preview layout and add regression coverage

## Root cause

The landing dictionaries only overrode a subset of the latest English copy, while `getStarterPromptTranslation` explicitly forced every locale except English and Chinese back to English. Template metadata supported only English and Chinese. Separately, the shared dialog's responsive `sm:max-w-lg` default overrode the landing preview's intended wide layout.

## Test plan

- [x] ESLint for all changed locale, catalog, copy, and test files
- [x] locale/catalog unit tests: 10 passed
- [x] chat-ui starter component tests: 14 passed
- [x] prompt-key completeness audit: 0 missing keys for zh, ja, ko, fr, de, it, es, ar, and pt
- [x] local preview routes returned HTTP 200

## Notes

- Full `tsc` remains blocked by a pre-existing `AgentPickerProps.open` error on current `main`, unrelated to this PR.
- Template preview images contain baked-in source-language text and are intentionally not dynamically translated.

```
