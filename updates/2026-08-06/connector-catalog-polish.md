---
title: "连接器目录卡片视觉优化"
type: "体验优化"
priority: "中"
date: "2026-08-06"
status: "待审核"
channels: ""
---

## 核心宣传点

插件页的连接器改用统一的服务商 Logo 和更易读的中文说明，去掉多余的加载/空状态方框，标签页改为分段控件，浏览更清爽。

## 原始内容

**fix(plugins): polish connector catalog cards (#3266)**

- sha: `82fbe074f03866fcb7f8abc56953ce9d9a32b3b2`
- PR: #3266

```
fix(plugins): polish connector catalog cards (#3266)

## Summary
- Remove the connector loading/empty status box from the plugins page.
- Add consistent 36px provider logos with frontend-owned local assets
and fallbacks for the first coming-soon providers.
- Replace raw provider notes with concise localized descriptions for
common providers.
- Polish provider cards and switch the top-level plugin tabs to a
segmented control.

## Root cause
Unknown providers fell back to inconsistent initials, loading and empty
provider states rendered as an unnecessary bordered box, and the
tab/card treatments were visually inconsistent.

Provider logos are intentionally frontend-owned. This PR does not add or
depend on a backend `logo_url` field.

## Test plan
- [x] TypeScript `tsc --noEmit`
- [x] 53 targeted Vitest tests for PluginsClient, ProviderLogo, and
ComposioConnectorsClient
- [x] ESLint and frontend pre-push verification
- [x] Python ruff, ruff-format, and pyright pre-commit hooks
- [ ] Full CI checks after the latest push

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

**PR Body:**

## Summary
- Remove the connector loading/empty status box from the plugins page.
- Add consistent 36px provider logos with frontend-owned local assets and fallbacks for the first coming-soon providers.
- Replace raw provider notes with concise localized descriptions for common providers.
- Polish provider cards and switch the top-level plugin tabs to a segmented control.

## Root cause
Unknown providers fell back to inconsistent initials, loading and empty provider states rendered as an unnecessary bordered box, and the tab/card treatments were visually inconsistent.

Provider logos are intentionally frontend-owned. This PR does not add or depend on a backend `logo_url` field.

## Test plan
- [x] TypeScript `tsc --noEmit`
- [x] 53 targeted Vitest tests for PluginsClient, ProviderLogo, and ComposioConnectorsClient
- [x] ESLint and frontend pre-push verification
- [x] Python ruff, ruff-format, and pyright pre-commit hooks
- [ ] Full CI checks after the latest push

