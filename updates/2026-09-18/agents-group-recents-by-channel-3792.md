---
title: "feat(agents): group recent conversations by channel (#3792)"
type: "新功能上线"
priority: "中"
date: "2026-09-18"
status: "待审核"
channels: ""
---

# Recents 会话列表按渠道分组了

## 核心宣传点

最近会话现在会把外部渠道的对话按渠道图标和名称归组，只显示已经加载到会话的渠道，每个分组默认折叠、可以各自展开。Web 和 Mattermost 的会话仍然不分组、排在渠道分组上面，保留原来的八行 Show more。weixin 和 openclaw-weixin 合并成一个微信分组，未知渠道有兜底图标。点开某个会话时分组的展开状态不会丢，切换 Agent 会重置。

## 分级

- 内部：P2
- 外部：B
- 发布状态：已合并待发版

## PR 说明

## Summary

Recents now groups external-channel conversations under channel icons and names. Only channels with loaded conversations appear, and each group starts collapsed and expands independently. Web/Mattermost conversations remain ungrouped above the channel groups, with the existing eight-row Show more control.

- Merge `weixin` and `openclaw-weixin` into one Weixin group; reuse existing channel labels/icons and a fallback for unknown channels.
- Preserve disclosure state when selecting a conversation by keeping navigation outside session-scoped preview providers. Switching Agents resets navigation state.
- Keep shared Load more pagination and long-title truncation. Channels found on older pages appear when those pages are loaded; this does not fetch all history up front.

Frontend-only deployment; no backend/API changes.

## Test plan

- [x] Local changed-file verification: governance guards, TypeScript and ESLint passed; 10 related test files / 105 tests passed.
- [x] Read-only code review completed without findings; focused recheck: 4 files / 22 tests passed.
- [x] Import-boundary check completed with zero errors (repository-wide warning-level findings remain).
- [x] Chromium fixture using the actual navigation and design-system components: default collapse, keyboard activation, independent channel groups, selected conversation, pagination, desktop/mobile interaction and long-title truncation. Scrolling content and rows stay within the 224px desktop viewport.
- [ ] Authenticated staging end-to-end acceptance after deployment. Browser validation above uses fixture session data.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `704d4cda6303482c5c39f1d59fc30f83aa316753`
- PR: #3792
- 作者：kaka-srp
- 日期：2026-09-18T03:55:36Z

### Commit Message

```
feat(agents): group recent conversations by channel (#3792)

## Summary

Recents now groups external-channel conversations under channel icons
and names. Only channels with loaded conversations appear, and each
group starts collapsed and expands independently. Web/Mattermost
conversations remain ungrouped above the channel groups, with the
existing eight-row Show more control.

- Merge `weixin` and `openclaw-weixin` into one Weixin group; reuse
existing channel labels/icons and a fallback for unknown channels.
- Preserve disclosure state when selecting a conversation by keeping
navigation outside session-scoped preview providers. Switching Agents
resets navigation state.
- Keep shared Load more pagination and long-title truncation. Channels
found on older pages appear when those pages are loaded; this does not
fetch all history up front.

Frontend-only deployment; no backend/API changes.

## Test plan

- [x] Local changed-file verification: governance guards, TypeScript and
ESLint passed; 10 related test files / 105 tests passed.
- [x] Read-only code review completed without findings; focused recheck:
4 files / 22 tests passed.
- [x] Import-boundary check completed with zero errors (repository-wide
warning-level findings remain).
- [x] Chromium fixture using the actual navigation and design-system
components: default collapse, keyboard activation, independent channel
groups, selected conversation, pagination, desktop/mobile interaction
and long-title truncation. Scrolling content and rows stay within the
224px desktop viewport.
- [ ] Authenticated staging end-to-end acceptance after deployment.
Browser validation above uses fixture session data.
```

## 备注

发布状态：已合并待发版（尚未包含在任何 ecap-*-release tag 中，最新正式 release 为 ecap-v0.19.16-release）。

来源：SerendipityOneInc/ecap-workspace @ 704d4cda，PR #3792，作者 kaka-srp。
