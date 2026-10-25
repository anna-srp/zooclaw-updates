---
title: "用量页改按本地时区展示，并支持手动选择时区"
type: "体验优化"
priority: "高"
date: "2026-10-23"
status: "待审核"
channels: ""
---

# 用量页改按本地时区展示，并支持手动选择时区

## 核心宣传点

用量页此前强制按 UTC 展示，而平台其他位置普遍用设备本地时间，东八区用户会把凌晨 1:58 的事件看成前一天 17:58，极易误判。本次用量展示默认跟随设备时区，表头、时间范围边界和数据截止时间都带上 UTC 偏移；历史记录如果因夏令时导致偏移不同，会显示该记录自身的偏移，并保留原始时间与 UTC 悬浮提示。账户设置新增时区选择：跟随系统、UTC 以及浏览器支持的时区，手动选择会按已验证用户在本浏览器内记住，切回「跟随系统」即清除覆盖；本地存储被禁用或数据非法时有兜底，页面重新获得焦点时会刷新设备时区检测。

## 分级

- 内部：P1
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `07a445147eb1259301470d138d897d7d95650a09`
- PR: #4127
- 作者：david-srp
- 日期：2026-10-23T16:44:22Z

### Commit Message

```
fix(platform): show usage in the preferred display time zone (#4127)

## Summary

Usage currently forces UTC while the rest of Platform commonly displays
device-local times. A user in UTC+08:00 sees an event at `Oct 22, 17:58`
instead of their local `Oct 23, 01:58`.

- Default Usage display to the device time zone, with UTC offsets in the
table header, range boundaries and As of timestamp. Show a historical
record's own offset when it differs across DST; retain the source
datetime and UTC tooltip.
- Add a basic Time zone selector to Account settings: Follow system, UTC
and browser-supported IANA zones. Remember manual choices per verified
user in this browser; Follow system clears the override. Handle
blocked/invalid storage and refresh device detection on
focus/visibility.
- Keep supported time-zone options in stable order and reuse
timestamp/offset formatters per zone, preserving event-date DST offsets.
- Keep API queries in UTC and preserve totals, cache keys, snapshots and
loaded pages. No backend, billing calculation, Billing-page or Webhooks
changes. Preferences do not sync across devices.

## Root cause

The Usage formatter and labels hard-code UTC, with no display
preference. This change only converts timestamps for presentation; it
does not shift event instants or alter the reporting window.

## Test plan

- [x] Node 24 / pinned pnpm 10.26.2: Platform lint, typecheck and
production build.
- [x] 29 targeted tests passed across formatting, preference provider,
Usage and Account navigation (125 unrelated router tests intentionally
skipped locally).
- [x] Verify Shanghai midnight rollover, India/Nepal fractional offsets,
New York DST repeated hours, persistence/reset, per-user isolation and
blocked/invalid storage.
- [x] Verify changing display zone leaves requests in UTC, totals
unchanged and loaded pagination intact.
- [x] Existing local fixture preview: desktop Usage, mobile Account
settings, UTC selection survives reload, Follow system restores
UTC+08:00, no browser console errors.

Local UI checks use sample data; production/staging business services
were not exercised. CI runs the full Platform suite. Screenshots are
retained locally under `.screenshots/` and are not committed.

---------

Co-authored-by: david-srp <264104338+david-srp@users.noreply.github.com>
```

