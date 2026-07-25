---
title: "性能优化：多语言字典按需加载，页面加载更快"
type: "体验优化"
priority: "中"
date: "2026-07-24"
status: "待审核"
channels: ""
---

## 核心宣传点

优化了多语言加载方式：不再让每位访客一次性下载全部 10 种语言的翻译字典（约 200KB），改为服务端按当前语言按需加载，落地页 JS 体积显著下降，页面首屏加载更快。

## 原始内容

**Commit**: `e1750e2a19` — bill-srp — 2026-07-24T13:34:51Z

### Commit Message

```
perf(i18n): lazy-load locale dictionaries server-side (#3064)

## Summary

Stop shipping all 10 locale dictionaries (~200KB gzipped, ~693KB source)
inside the client JS bundle. Previously
`src/contexts/LanguageContext.tsx` (`'use client'`) statically imported
every dictionary via the `src/locales/index.ts` barrel, so every visitor
downloaded and parsed all 10 languages — exceeding the 150KB
landing-page JS budget on translation data alone.

Following the Next.js App Router i18n pattern, dictionaries now stay
server-side:

- **`src/locales/get-dictionary.ts`** (new, `server-only`): per-locale
dynamic `import()`. English returns directly; other locales load `en` +
target concurrently and immutably deep-merge (English fills any missing
keys) so the client receives one complete dictionary.
- **`[locale]/layout.tsx`** (server component) calls
`getDictionary(locale)` and passes the result through `ClientLayout` →
`LanguageProvider` as a `dictionary` prop.
- `LanguageProvider` no longer imports `@/locales`; the now-redundant
dual-lookup fallback in `getNestedValue` is removed (the dictionary
arrives pre-merged).
- The skills metadata pages and the `share/[shareId]` replay server
boundary were converted to `getDictionary` so **no client component
imports a dictionary**.
- Deleted the `src/locales/index.ts` barrel (no remaining consumers; the
`TranslationKeys`/`TranslationKey` types had zero external users). Added
`server-only` dep + a Vitest alias to a no-op stub.

`t()`'s signature, `{param}` interpolation, and missing-key fallback
behavior are all unchanged — zero call-site churn. Locale switching
still works via `setLocale`'s existing `router.refresh()` /
`router.push`, which re-renders the server layout with the new
dictionary.

**Result:** ~200KB gzipped removed from the shared client bundle; each
user now receives only their active locale (~25–30KB gzipped) in the RSC
payload. Desktop build confirmed shared first-load JS at 108KB with no
dictionary markers in client static chunks (present in server chunks).

Design spec:
`docs/superpowers/specs/2026-07-24-locale-dictionary-lazy-loading.md`
(included in this branch).

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + `tsc --noEmit` + vitest
(7,229 passing, 1 skip, 1 todo) + eslint, all green
- [x] `pnpm lint:imports` — exit 0 (309 warn-only W5 baseline, 0 errors)
- [x] `pnpm lint:deadcode` (knip hard gate) — exit 0 after barrel
deletion
- [x] `pnpm test:unit:coverage` — 88.65% stmt / 81.93% br / 87.40% fn /
90.89% ln, all above ratcheted thresholds
- [x] New `get-dictionary` unit tests: en passthrough, deep-merge
fallback, non-object leaf handling
- [ ] Post-merge: staging smoke — verify language switch on homepage
(`/` + `/zh`), an app page (`/chat`), and an SEO page (`/pricing`)
renders translated copy with no hydration errors
- [ ] Post-merge: confirm `next build` (`web-build-check`) bundle
reduction in CI
```

### PR Body

## Summary

Stop shipping all 10 locale dictionaries (~200KB gzipped, ~693KB source) inside the client JS bundle. Previously `src/contexts/LanguageContext.tsx` (`'use client'`) statically imported every dictionary via the `src/locales/index.ts` barrel, so every visitor downloaded and parsed all 10 languages — exceeding the 150KB landing-page JS budget on translation data alone.

Following the Next.js App Router i18n pattern, dictionaries now stay server-side:

- **`src/locales/get-dictionary.ts`** (new, `server-only`): per-locale dynamic `import()`. English returns directly; other locales load `en` + target concurrently and immutably deep-merge (English fills any missing keys) so the client receives one complete dictionary.
- **`[locale]/layout.tsx`** (server component) calls `getDictionary(locale)` and passes the result through `ClientLayout` → `LanguageProvider` as a `dictionary` prop.
- `LanguageProvider` no longer imports `@/locales`; the now-redundant dual-lookup fallback in `getNestedValue` is removed (the dictionary arrives pre-merged).
- The skills metadata pages and the `share/[shareId]` replay server boundary were converted to `getDictionary` so **no client component imports a dictionary**.
- Deleted the `src/locales/index.ts` barrel (no remaining consumers; the `TranslationKeys`/`TranslationKey` types had zero external users). Added `server-only` dep + a Vitest alias to a no-op stub.

`t()`'s signature, `{param}` interpolation, and missing-key fallback behavior are all unchanged — zero call-site churn. Locale switching still works via `setLocale`'s existing `router.refresh()` / `router.push`, which re-renders the server layout with the new dictionary.

**Result:** ~200KB gzipped removed from the shared client bundle; each user now receives only their active locale (~25–30KB gzipped) in the RSC payload. Desktop build confirmed shared first-load JS at 108KB with no dictionary markers in client static chunks (present in server chunks).

Design spec: `docs/superpowers/specs/2026-07-24-locale-dictionary-lazy-loading.md` (included in this branch).

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + `tsc --noEmit` + vitest (7,229 passing, 1 skip, 1 todo) + eslint, all green
- [x] `pnpm lint:imports` — exit 0 (309 warn-only W5 baseline, 0 errors)
- [x] `pnpm lint:deadcode` (knip hard gate) — exit 0 after barrel deletion
- [x] `pnpm test:unit:coverage` — 88.65% stmt / 81.93% br / 87.40% fn / 90.89% ln, all above ratcheted thresholds
- [x] New `get-dictionary` unit tests: en passthrough, deep-merge fallback, non-object leaf handling
- [ ] Post-merge: staging smoke — verify language switch on homepage (`/` + `/zh`), an app page (`/chat`), and an SEO page (`/pricing`) renders translated copy with no hydration errors
- [ ] Post-merge: confirm `next build` (`web-build-check`) bundle reduction in CI

