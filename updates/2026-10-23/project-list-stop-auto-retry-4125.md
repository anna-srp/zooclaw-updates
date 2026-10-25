---
title: "修复：项目列表加载失败后仍会自动重试一次"
type: "Bug Fix"
priority: "中"
date: "2026-10-23"
status: "待审核"
channels: ""
---

# 修复：项目列表加载失败后仍会自动重试一次

## 核心宣传点

项目切换器的分页在加载失败后，设计上应停止自动重试、等用户点击 Retry，但实现里是靠副作用清理阶段断开可视区观察器来停止自动加载，而清理要等到渲染提交之后才执行。如果在这个很短的窗口里观察器回调又触发，加载下一页的方法本身并不检查「刚刚失败过」，于是会再自动发一次请求。本次改为用同步更新的状态引用记录空闲/进行中/已失败，从组件层面真正阻断失败后的自动重试，而不是只改测试。顺带修掉了因此在持续集成中偶发失败、并会连带阻塞其他前端 PR 的质量门禁。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `d80f8e6e59ed627337c770b331120bdd9f08b3a3`
- PR: #4125
- 作者：finn-srp
- 日期：2026-10-23T06:51:26Z

### Commit Message

```
fix(platform): stop project list auto-retry before the observer disconnects (#4125)

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

## Summary

- 修复 #4124：`ProjectSwitcher` 分页的 “stops automatic retries on failure…”
用例在 CI 偶发失败（`loadMoreProjects` 预期调用 1 次，实际 2 次）。只改 `web/app` 的 PR（例如
#4123）也会因为它挂掉 `platform-quality`。
- 这不只是测试问题。组件在加载失败后，存在一个很短的窗口仍然会自动重试，违背了“失败后停止自动重试、等用户点 Retry”的设计。本 PR
修的是组件本身。

## Root cause

`ProjectOptions` 在加载失败后，通过 `useEffect` 的 cleanup 执行
`IntersectionObserver.disconnect()`，以此停止自动加载。但 effect cleanup 在 commit
之后才执行。如果在这之前 observer 回调又触发了，就会调用 `loadNextPage()`。`loadNextPage`
本身不检查“刚刚失败过”，于是又自动请求了一次。

测试里的 `findByRole('Retry loading projects')` 在 DOM 更新后就返回。机器负载高时，旧
observer 的 cleanup 这时还没执行，第二次 `showListEnd()` 正好落在这个窗口里。

修复：用一个同步更新的 ref 记录加载状态（`'idle' | 'pending' | 'failed'`），替代原来的
`requestPending`。状态为 `'failed'` 时，自动加载直接返回；只有用户点 Retry（`loadNextPage({
retry: true })`）才会重新请求。这样不再依赖 effect cleanup 的执行时机。

已知但不在本 PR 范围：成功路径上，`loadMoreProjects` 返回后、provider 的新 cursor 状态 commit
之前，如果再次触发加载，会用旧 cursor 重复请求同一页。provider 的 `appendUnique`
会去重，不会产生错误数据，只是多一次请求。根因在 provider 的 cursor 更新时机，需要单独处理。

## Test plan

- [x] 新增用例：失败前先拿到 observer 回调，失败后再直接调用它，模拟 cleanup 前触发。修复前稳定失败（预期 1 次，实际
2 次），修复后通过。
- [x] 复现与验证：后台并发跑完整测试制造负载，同时把该测试文件反复跑 30 次。修复前失败 1 次，断言与 CI
一致（`project-switcher.test.tsx:92`）；修复后 30 次全部通过。
- [x] 变异检查：去掉 `'failed'` 判断后，新用例失败；恢复后通过。
- [x] rebase 到最新 main 后，在 `web/platform` 依次运行 `pnpm lint`、`pnpm
typecheck`、`pnpm test`（31 个文件、378 个用例）和 `pnpm build`，全部通过。

Fixes #4124

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

