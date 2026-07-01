---
title: "修复引导浮层按钮在部分页面点击后 404"
type: "Bug Fix"
priority: "中"
date: "2026-06-30"
status: "待审核"
channels: ""
---
# 修复引导浮层按钮在部分页面点击后 404
## 核心宣传点
修复了在 /new-chat 等页面点击新手引导浮层的跳转按钮时会打开错误链接、导致 404 的问题，现在会正确跳转到对应语言的目标页面。
## 原始内容
fix(web): validate guide tour locale before CTA navigation (#2659)

## Summary
- Fix guide tour CTA links when the current route first segment is not a
supported locale.
- Reuse existing i18n locale parsing and fall back to the current
LanguageContext locale for locale-free app routes.
- Add regression coverage for `/new-chat` opening the CTA destination in
the active language.

## Root cause
The guide tour CTA used `window.location.pathname.split("/")[1]` as the
locale. On app routes like `/new-chat`, that first segment is not a
locale, so the CTA opened `/new-chat/agents-manager`, which 404s.

## Test plan
- [x] `pnpm --dir web/app test:unit
tests/unit/components/GuideTourModal.unit.spec.tsx`
- [x] `pnpm --dir web/app exec tsc --noEmit --pretty false`
- [x] `pnpm --dir web/app exec eslint src/components/GuideTourModal.tsx
tests/unit/components/GuideTourModal.unit.spec.tsx --quiet`

---

### PR Description

## Summary
- Fix guide tour CTA links when the current route first segment is not a supported locale.
- Reuse existing i18n locale parsing and fall back to the current LanguageContext locale for locale-free app routes.
- Add regression coverage for `/new-chat` opening the CTA destination in the active language.

## Root cause
The guide tour CTA used `window.location.pathname.split("/")[1]` as the locale. On app routes like `/new-chat`, that first segment is not a locale, so the CTA opened `/new-chat/agents-manager`, which 404s.

## Test plan
- [x] `pnpm --dir web/app test:unit tests/unit/components/GuideTourModal.unit.spec.tsx`
- [x] `pnpm --dir web/app exec tsc --noEmit --pretty false`
- [x] `pnpm --dir web/app exec eslint src/components/GuideTourModal.tsx tests/unit/components/GuideTourModal.unit.spec.tsx --quiet`
