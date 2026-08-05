---
title: "Agent 公开分享页上线：无需登录即可查看并一键雇佣"
type: "新功能上线"
priority: "高"
date: "2026-08-04"
status: "待审核"
channels: ""
commit: "3b7fa205420052b5930a1c30463c650d19438aca"
repo: "SerendipityOneInc/ecap-workspace"
---

## 核心宣传点

Agent 现在拥有 Agent Store 风格的公开分享页：任何人无需登录即可浏览 Agent 介绍，点击雇佣时自动引导登录并回到原页面，付费 Pack 也有对应购买入口，分享传播更顺畅。

## 原始内容

```
feat(agent-share): add frontend-only public share page (#3216)

## Linear

N/A

## Summary

- Add a frontend-only Agent Store-style public pack page using the
anonymous fields already available on `main`.
- Preserve the dedicated share-page header, all-method login return
path, hire routing, paid-pack CTA behavior, avatar-derived hero,
conditional field rendering, and natural hero-tail sticky treatment.
- Keep the share page inside the common marketing chrome so it renders
the same `LandingFooter` and `getFooterColumns` source as the ZooClaw
homepage; homepage footer changes therefore flow through automatically.
- Add a local mock fixture for visual QA and regression tests for the
stable-field boundary, shared footer, header auth flow, and hire links.

## Scope

- Frontend only: all changed files are under `web/`.
- No `services/` code, database schema, backend response model, or
production API change.
- This is the fast-release frontend-only alternative to #3166; the
existing frontend + backend PR remains separate.

## Known limitations

- Trigger words, version, author, license, languages, archive size,
published time, and release notes are intentionally omitted because the
current anonymous response does not reliably expose them.
- Missing optional values are omitted instead of rendering empty
information rows.

## Test plan

- [x] Targeted share-page and authentication tests — 99 tests across 6
files passed, including `LoginForm`, email OTP verification, and phone
verification return paths.
- [x] `bash scripts/verify-web.sh --no-test` — governance guards,
TypeScript, and ESLint passed.
- [x] `bash scripts/verify-changed.sh` — all changed surfaces passed.
- [x] Browser QA at `/zh/packs/mock-agent-share-frontend-only`: hero,
sticky state, stable fields, CTA routing, and zero console errors.
- [x] Compared the local and production homepage footer: identical text
and all 26 links.

---------

Co-authored-by: eric <eric.ma@creatibi.com>

---

### PR Body

## Linear

N/A

## Summary

- Add a frontend-only Agent Store-style public pack page using the anonymous fields already available on `main`.
- Preserve the dedicated share-page header, all-method login return path, hire routing, paid-pack CTA behavior, avatar-derived hero, conditional field rendering, and natural hero-tail sticky treatment.
- Keep the share page inside the common marketing chrome so it renders the same `LandingFooter` and `getFooterColumns` source as the ZooClaw homepage; homepage footer changes therefore flow through automatically.
- Add a local mock fixture for visual QA and regression tests for the stable-field boundary, shared footer, header auth flow, and hire links.

## Scope

- Frontend only: all changed files are under `web/`.
- No `services/` code, database schema, backend response model, or production API change.
- This is the fast-release frontend-only alternative to #3166; the existing frontend + backend PR remains separate.

## Known limitations

- Trigger words, version, author, license, languages, archive size, published time, and release notes are intentionally omitted because the current anonymous response does not reliably expose them.
- Missing optional values are omitted instead of rendering empty information rows.

## Test plan

- [x] Targeted share-page and authentication tests — 99 tests across 6 files passed, including `LoginForm`, email OTP verification, and phone verification return paths.
- [x] `bash scripts/verify-web.sh --no-test` — governance guards, TypeScript, and ESLint passed.
- [x] `bash scripts/verify-changed.sh` — all changed surfaces passed.
- [x] Browser QA at `/zh/packs/mock-agent-share-frontend-only`: hero, sticky state, stable fields, CTA routing, and zero console errors.
- [x] Compared the local and production homepage footer: identical text and all 26 links.

```
