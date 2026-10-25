---
title: "修复：页面切换加载时深色模式不再闪回浅色"
type: "Bug Fix"
priority: "中"
date: "2026-10-08"
status: "待审核"
channels: ""
---

# 修复：页面切换加载时深色模式不再闪回浅色

## 核心宣传点

修复了页面进入和退出加载状态时主题被重置的问题。此前从「身份」页跳转到首页，加载骨架出现的一瞬间，浏览器会把文档上的深色类名和 color-scheme 清掉，恢复时只还原了字体类，结果保存的深色/跟随系统偏好虽然没丢，页面却渲染成浅色，看起来像闪白。根因是根级 loading 边界包住了带主题 Provider 的语言布局；本次把共享的加载组件下移到语言目录内、主题 Provider 之下，公开回放页的动态兜底仍留在它自己的文档布局里。已补充回归用例，在真实布局上对「深色」和「跟随系统深色」两种偏好分别挂起再恢复验证。

## 分级

- 内部：P2
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `706c9df8a81a754db23d8a207032b4a9386b4eba`
- PR: #4033
- 作者：sharplee-srp
- 日期：2026-10-08T08:56:29Z

### Commit Message

```
fix(web): preserve appearance across loading boundaries (#4033)

## Summary
Keep the selected appearance when page content enters and leaves a
loading state. Move the shared `loading.tsx` into `[locale]`, below the
layout that owns the document and theme providers. Keep the dynamic
public replay fallback under `share/loading.tsx`, inside its own
document layout.

## Root cause
The root loading boundary wrapped the locale layout's `<html>`. In the
production browser, suspending that boundary caused React to remove the
document's theme class and `color-scheme`; reappearance restored only
the layout's font classes. The saved `dark` / `system` preference
remained intact, but the page rendered light.

The confirmed production trigger was navigating from Identity to Home. A
hard reload of Identity alone did not reproduce the reported symptom in
the diagnostic runs.

## Test plan
- Regression renders the actual locale layout with loading boundaries
derived from the route files, then suspends and resumes page content for
explicit dark and system-dark preferences.
- Confirmed both dark/system regression cases fail with the old root
loading placement and pass with the new placement.
- Passed 103 relevant tests across 14 files, TypeScript, ESLint, and web
governance checks. The pre-push changed-surface gate passed.

- Local browser E2E passed on `8baf36571`: local Next.js with real
staging APIs/account, Chromium on the browser host. Tested explicit dark
with OS light and system mode with OS dark.
- Explicit dark and system-dark modes survived Identity refresh,
Identity → Home navigation with the Home chunk delayed by 3 seconds, and
Home refresh. The actual loading fallback appeared in both runs; a DOM
observer recorded zero losses of the dark class or color-scheme. Stored
preferences and dark body colors remained correct.
- System mode also followed light → dark OS changes after refresh. No
page errors or failed API responses were observed. Identity/Home
screenshots were visually checked.

- Supplemental light-mode browser E2E passed on the same commit with OS
dark: select Light in settings, refresh Identity, navigate to Home with
its chunk delayed by 3 seconds, and refresh Home. The actual loading
fallback appeared; `html.light`, `color-scheme: light`, the stored light
preference and light body background persisted, with no dark class or
missing-theme mutations. No page errors or failed API responses were
observed. The Home screenshot was visually checked.

This validates local Web against staging APIs. Deployed production
validation still requires release; this PR does not deploy the change.
```

