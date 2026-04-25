---
title: "对话分享链接修复：正确使用前端域名"
type: "Bug Fix"
priority: "中"
date: "2026-04-25"
status: "待审核"
channels: "Discord + changelog"
---

# 对话分享链接修复：正确使用前端域名

## 核心宣传点

修复了对话分享功能生成链接时使用了错误域名的问题，分享链接现在可以正常打开。

## 原始内容

Commit: e7dbc1491aa6d9ea815742074250207df3e4fee7

Message:
fix(chat-replay): use APP_FRONTEND_URL for share links (#1319)

## Summary

- Share URLs are user-facing frontend links (`/share/*` route lives in
the Next.js app), so `_build_share_url()` now resolves against
`APP_FRONTEND_URL` instead of `APP_PUBLIC_URL`.
- Falls back to relative path `/share/{id}` when `APP_FRONTEND_URL` is
unset; the frontend's `absoluteUrl()` helper resolves that against
`window.location.origin`.

## Why

In staging the two settings point at different hosts:

| Key | Staging value | Purpose |
|---|---|---|
| `APP_PUBLIC_URL` | `https://claw-interface.ecap.yesy.live` |
**Backend** host — OAuth/webhook callbacks (Google, Stripe return, bot
env) |
| `APP_FRONTEND_URL` | `https://ecap.gensmo.nosay.live` | **Frontend**
host — what users open in the browser |

The previous code used `APP_PUBLIC_URL`, so shared replay links pointed
at the backend domain where `/share/*` doesn't exist → 404. This PR
fixes only the share-link call site; other callers of `APP_PUBLIC_URL`
(OAuth callbacks, Stripe portal, bot env injection) are correct as-is
and unchanged.

DB stores only `share_id`, not full URLs — no data migration needed.
After deploy, all newly created links will use the frontend host.

## Test plan

- [x] Three new unit tests cover `APP_FRONTEND_URL` precedence,
trailing-slash stripping, and relative-path fallback
- [x] `pytest tests/unit/test_chat_replay_create.py` — 17/17 passing
locally
- [x] ruff, pyright, import-linter, deptry, file-length, complexity,
collection-constants, repo-sync — all clean
- [ ] After merge: smoke-test on staging by creating a new share and
opening the URL in incognito

PR Description:
## Summary

- Share URLs are user-facing frontend links (`/share/*` route lives in the Next.js app), so `_build_share_url()` now resolves against `APP_FRONTEND_URL` instead of `APP_PUBLIC_URL`.
- Falls back to relative path `/share/{id}` when `APP_FRONTEND_URL` is unset; the frontend's `absoluteUrl()` helper resolves that against `window.location.origin`.

## Why

In staging the two settings point at different hosts:

| Key | Staging value | Purpose |
|---|---|---|
| `APP_PUBLIC_URL` | `https://claw-interface.ecap.yesy.live` | **Backend** host — OAuth/webhook callbacks (Google, Stripe return, bot env) |
| `APP_FRONTEND_URL` | `https://ecap.gensmo.nosay.live` | **Frontend** host — what users open in the browser |

The previous code used `APP_PUBLIC_URL`, so shared replay links pointed at the backend domain where `/share/*` doesn't exist → 404. This PR fixes only the share-link call site; other callers of `APP_PUBLIC_URL` (OAuth callbacks, Stripe portal, bot env injection) are correct as-is and unchanged.

DB stores only `share_id`, not full URLs — no data migration needed. After deploy, all newly created links will use the frontend host.

## Test plan

- [x] Three new unit tests cover `APP_FRONTEND_URL` precedence, trailing-slash stripping, and relative-path fallback
- [x] `pytest tests/unit/test_chat_replay_create.py` — 17/17 passing locally
- [x] ruff, pyright, import-linter, deptry, file-length, complexity, collection-constants, repo-sync — all clean
- [ ] After merge: smoke-test on staging by creating a new share and opening the URL in incognito
