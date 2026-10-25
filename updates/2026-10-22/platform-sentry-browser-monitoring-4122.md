---
title: "Platform 接入前端错误监控，页面崩溃能被及时发现"
type: "后端功能"
priority: "中"
date: "2026-10-22"
status: "待审核"
channels: ""
---

# Platform 接入前端错误监控，页面崩溃能被及时发现

## 核心宣传点

开发者平台此前没有浏览器端错误监控，页面渲染失败只能在用户自己的控制台里看到，团队无从感知。本次在应用启动前初始化前端监控，上报到独立项目并区分预发与生产环境、按提交号划分版本，捕获渲染错误和根错误并带上组件调用栈，同时保留原有控制台输出。已知的取消类与布局观察器噪声会被过滤，分包加载失败会被归组但不丢弃；控制台与 DOM 行为轨迹关闭，请求凭据和 URL 参数会被脱敏。用户界面没有变化，收益是线上问题的发现和定位速度。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## 备注

源码映射上传复用仓库既有的鉴权令牌，需显式开启才会上传。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `e4a9ccc67c94bc8996186e582d285655e0043baa`
- PR: #4122
- 作者：finn-srp
- 日期：2026-10-22T12:12:23Z

### Commit Message

```
feat(platform): add Sentry browser error monitoring (#4122)

## Summary

Platform currently has no browser error monitoring, so render failures
only appear in the browser console. Initialize `@sentry/react` before
the application and report to the dedicated `zoowork-platform` project,
with separate staging/production environments and commit-scoped
releases.

- Capture render and root errors with React component stacks while
preserving console output. Fallback/recoverable errors are handled;
uncaught root errors remain unhandled.
- Filter known cancellation/ResizeObserver noise and group chunk-loading
failures without dropping them. Disable console/DOM breadcrumbs and
scrub request credentials and URL parameters.
- Reuse the repository `SENTRY_AUTH_TOKEN` for source maps. Uploads
require an explicit flag and a scoped release; plugin failures stop the
build. Delete hidden source maps before Cloudflare deployment.

## Test plan

- [x] Rebased on current `main` (`f4aee46783`); Node 24: `pnpm lint`,
`pnpm typecheck`, `pnpm test` (31 files / 377 tests), and `pnpm build`
passed.
- [x] Real Vite 8/Sentry plugin offline success path: all 32 runtime
debug IDs matched prepared upload comments/maps; all 32 generated `.map`
files were removed from `dist`. The Sentry CLI was replaced with a local
success stub; the actual plugin performed ID injection, artifact
preparation and cleanup.
- [x] Real Vite builds failed on simulated release-creation and
source-map-upload failures; no live Sentry requests were sent.
- [x] Validated workflow YAML/shell configuration and missing-token
failures for both environments.

Live Sentry upload permissions and event ingestion remain to be verified
in staging. This PR covers browser exceptions; Worker monitoring and
handled API/network-error reporting are separate work.
```

