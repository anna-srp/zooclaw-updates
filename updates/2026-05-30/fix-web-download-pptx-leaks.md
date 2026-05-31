---
title: "文件下载与 PPTX 解析稳定性修复"
type: "Bug Fix"
priority: "中"
date: "2026-05-30"
status: "待审核"
channels: ""
---

# 文件下载与 PPTX 解析稳定性修复

## 核心宣传点

下载附件和解析 PPTX 文件时偶发的卡顿/失败问题已修复，体验更流畅稳定。

## 原始内容

fix(web): createObjectURL leaks in MMAttachments download + pptx-parser partial failure (#2076)

## Summary

#2072 follow-up(createObjectURL 14 文件 → useObjectUrl,**不在 #2072 自身
scope**)的 PR 2 / 3。修两个真实 lifecycle bug,跟 PR #2075 独立可平行。

**Bug 1 —
`MMAttachments.tsx::FileAttachment.handleDownload`**(`setTimeout(revoke,
1000)` race)
- unmount race / double-click race / timing fragility 三连
- 改用 `lib/download.ts::triggerDownload`(已 battle-tested 同步 click + 同步
revoke)
- `triggerDownload` 由 module-local 改 export

**Bug 2 — `pptx-parser.ts::fileToBlobUrl`**(部分失败 leak)
- parse 中途 throw 时,已 mint 的 ObjectURL 永不进 `slides` state → 永不 revoke
- 累计 `createdUrls: string[]` + `try/catch` 包裹 slide 循环,throw 路径统一 revoke
- 抽 `parseOneSlide` helper 保持 nesting ≤ max-depth=5

## 测试

- **MMAttachments**: 锁两条 invariant —— 单点击后 revoke 在同 tick 触发(无 timer);1s
内连点两次,两个 URL 都被 revoke(不再因 ref 被覆盖而 leak URL #1)
- **pptx-parser**: 成功路径 0 revoke(所有权交 slides[]);partial-failure 时 throw
前每个 mint 都被 revoke(用 `vi.spyOn(DOMParser.prototype, 'parseFromString')`
在第 4 次调用触发 throw,精准 land 在 slide 1 minted URL 之后)

## Test plan

- [x] `pnpm lint` 全绿
- [x] `npx tsc --noEmit` 全绿
- [x] `pnpm test:unit` 全 6234 测试通过(含新增 2 case for MMAttachments + 2 case
for pptx-parser)
- [ ] CI: code-quality / lint-and-test 绿

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

#2072 follow-up(createObjectURL 14 文件 → useObjectUrl,**不在 #2072 自身 scope**)的 PR 2 / 3。修两个真实 lifecycle bug,跟 PR #2075 独立可平行。

**Bug 1 — `MMAttachments.tsx::FileAttachment.handleDownload`**(`setTimeout(revoke, 1000)` race)
- unmount race / double-click race / timing fragility 三连
- 改用 `lib/download.ts::triggerDownload`(已 battle-tested 同步 click + 同步 revoke)
- `triggerDownload` 由 module-local 改 export

**Bug 2 — `pptx-parser.ts::fileToBlobUrl`**(部分失败 leak)
- parse 中途 throw 时,已 mint 的 ObjectURL 永不进 `slides` state → 永不 revoke
- 累计 `createdUrls: string[]` + `try/catch` 包裹 slide 循环,throw 路径统一 revoke
- 抽 `parseOneSlide` helper 保持 nesting ≤ max-depth=5

## 测试

- **MMAttachments**: 锁两条 invariant —— 单点击后 revoke 在同 tick 触发(无 timer);1s 内连点两次,两个 URL 都被 revoke(不再因 ref 被覆盖而 leak URL #1)
- **pptx-parser**: 成功路径 0 revoke(所有权交 slides[]);partial-failure 时 throw 前每个 mint 都被 revoke(用 `vi.spyOn(DOMParser.prototype, 'parseFromString')` 在第 4 次调用触发 throw,精准 land 在 slide 1 minted URL 之后)

## Test plan

- [x] `pnpm lint` 全绿
- [x] `npx tsc --noEmit` 全绿
- [x] `pnpm test:unit` 全 6234 测试通过(含新增 2 case for MMAttachments + 2 case for pptx-parser)
- [ ] CI: code-quality / lint-and-test 绿

🤖 Generated with [Claude Code](https://claude.com/claude-code)
