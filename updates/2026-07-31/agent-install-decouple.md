---
title: "安装 Agent 不再受旧版 Bot 状态阻塞"
type: "体验优化"
priority: "中"
外部: "B"
date: "2026-07-31"
status: "待审核"
channels: ""
---

## 核心宣传点

即使旧版 bot/computer 暂时不可用，市场和 Agent 详情页的「Hire 雇佣」按钮也保持可用，基于 pack 的安装可直接完成，不再被旧版就绪状态卡住。

## 原始内容

**fix(web): decouple agent install from v1 bot status (#3173)**

- SHA: `29706ff9f76ec8c2239c117ff09f4eb64fbab113`
- PR: #3173
- 日期: 2026-07-31T09:38:32Z

```
fix(web): decouple agent install from v1 bot status (#3173)

## Summary
- Keep marketplace and agent-detail Hire buttons enabled while the v1
bot/computer is unavailable.
- Let pack-based Hire requests reach the runtime-routing BFF with an
optional current computer ID, so engine installs do not require v1
readiness.
- Preserve the existing v1 gates for Publish/private-pack installs and
computer-runtime lifecycle actions such as Fire, Update, and Uninstall.

## Root cause
Marketplace Hire reused the v1 computer lifecycle gate before invoking
the BFF. That blocked engine installs even though the engine route only
needs the immutable pack ID and does not depend on a v1 bot.

## Test plan
- [x] Marketplace/detail Hire and shared action tests passed (152
tests).
- [x] Unchanged Publish/private-pack behavior passed its existing tests
(78 tests).
- [x] Changed-path Vitest selection passed (192 tests).
- [x] Changed-path ESLint passed with 0 errors.
- [x] `git diff --check` passed.
- [ ] Latest required PR CI is running.

## Local environment note
Local `verify-web.sh` reported `PluginsClient.tsx(31,38): TS18047:
searchParams is possibly null` on an unchanged file. The previous PR
revision passed the authoritative CI web typecheck and build; the latest
CI run is pending.
```

**PR Body:**

## Summary
- Keep marketplace and agent-detail Hire buttons enabled while the v1 bot/computer is unavailable.
- Let pack-based Hire requests reach the runtime-routing BFF with an optional current computer ID, so engine installs do not require v1 readiness.
- Preserve the existing v1 gates for Publish/private-pack installs and computer-runtime lifecycle actions such as Fire, Update, and Uninstall.

## Root cause
Marketplace Hire reused the v1 computer lifecycle gate before invoking the BFF. That blocked engine installs even though the engine route only needs the immutable pack ID and does not depend on a v1 bot.

## Test plan
- [x] Marketplace/detail Hire and shared action tests passed (152 tests).
- [x] Unchanged Publish/private-pack behavior passed its existing tests (78 tests).
- [x] Changed-path Vitest selection passed (192 tests).
- [x] Changed-path ESLint passed with 0 errors.
- [x] `git diff --check` passed.
- [ ] Latest required PR CI is running.

## Local environment note
Local `verify-web.sh` reported `PluginsClient.tsx(31,38): TS18047: searchParams is possibly null` on an unchanged file. The previous PR revision passed the authoritative CI web typecheck and build; the latest CI run is pending.

