---
title: "iOS 侧边栏改版：交互重做、草稿会话不再乱窜，展开会话也不再压住下一行"
type: "体验优化"
priority: "中"
date: "2026-09-02"
status: "待审核"
channels: "Discord+changelog"
---

# iOS 侧边栏改版：交互重做、草稿会话不再乱窜，展开会话也不再压住下一行

## 核心宣传点

iOS App 的侧边栏按新设计重做了视觉与交互，Agent 行和历史会话行的操作方式统一对齐。

草稿会话的行为也理顺了：空白草稿会按当前登录用户分别保存并安全复用，只有当会话里真的产生了内容之后才会在列表里露出来，不会再出现一堆空会话；第一次发送消息时才真正创建会话，并且在发送过程中把 Mattermost 的目标会话冻结住——即使这期间有附件在异步上传、或者你在侧边栏切来切去，消息也不会被投到别的会话里去。

同时修复了一个布局问题：展开某个 Agent 的会话列表后，展开内容会压住下一个 Agent 行。原因是展开的会话栈用了 35pt 的行间距却被塞进固定 237pt 的高度里，会话一多子视图就画到了框外，而外层 Agent 列表只按固定高度预留空间。现在会话区改用自身实际高度，每个会话行和历史行统一 36pt。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `5471efc7fd3b142b0db5d74ccf80ead1363dfa3d`
- PR: #3612
- 作者: shana-srp
- 日期: 2026-09-02T03:58:28Z

### Commit Message

```
feat(ios): align sidebar and draft conversation flow (#3612)

## Linear

N/A — split from #3043.

## Summary

- Restyle the iOS sidebar and align agent/history interactions with the
updated design.
- Persist empty conversation drafts per signed-in user, reuse them
safely, and reveal them only after real thread content exists.
- Create a missing conversation on first send and freeze the Mattermost
send target across asynchronous attachment uploads or sidebar changes.
- Port the chronological first 15 non-merge commits from #3043 onto the
current `main` workspace-based conversation APIs.

This is split 1 of 3 for #3043. Follow-up commits resolve Swift
compatibility, async target binding, attachment channel ownership, and
CI lint issues found during validation and review.

## Review handling

- `REQUEST_CHANGES`: fix before merge.
- `NEED_HUMAN_REVIEW`: Codex assesses whether the finding is worth
fixing; fix justified findings, otherwise leave a PR comment with the
technical rationale.

## Test plan

- [x] Build the ZooClaw app and test targets on the iOS 26.5 simulator.
- [x] Run `AgentConversationViewModelTests`, `AppCoordinatorTests`,
`MattermostViewModelThreadTests`, `SidebarAgentExpansionStateTests`,
`ChatInputSendTests`, and `MattermostViewModelAttachmentsTests` (45
tests passed).
- [x] Run Swift parser checks and `git diff --check` on
conflict-resolved files.

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

```
## Linear

N/A — split from #3043.

## Summary

- Restyle the iOS sidebar and align agent/history interactions with the updated design.
- Persist empty conversation drafts per signed-in user, reuse them safely, and reveal them only after real thread content exists.
- Create a missing conversation on first send and freeze the Mattermost send target across asynchronous attachment uploads or sidebar changes.
- Port the chronological first 15 non-merge commits from #3043 onto the current `main` workspace-based conversation APIs.

This is split 1 of 3 for #3043. Follow-up commits resolve Swift compatibility, async target binding, attachment channel ownership, and CI lint issues found during validation and review.

## Review handling

- `REQUEST_CHANGES`: fix before merge.
- `NEED_HUMAN_REVIEW`: Codex assesses whether the finding is worth fixing; fix justified findings, otherwise leave a PR comment with the technical rationale.

## Test plan

- [x] Build the ZooClaw app and test targets on the iOS 26.5 simulator.
- [x] Run `AgentConversationViewModelTests`, `AppCoordinatorTests`, `MattermostViewModelThreadTests`, `SidebarAgentExpansionStateTests`, `ChatInputSendTests`, and `MattermostViewModelAttachmentsTests` (45 tests passed).
- [x] Run Swift parser checks and `git diff --check` on conflict-resolved files.

```

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `3ad90ee2f57bafc18614af141835b7612ad191ce`
- PR: #3619
- 作者: shana-srp
- 日期: 2026-09-02T10:27:28Z

### Commit Message

```
fix(ios): prevent sidebar session row overlap (#3619)

## Summary
- Prevent expanded sidebar session rows from overlapping the following
agent row.
- Let the conversation section use its intrinsic height while keeping
each conversation and history row at a consistent 36pt height.

## Root cause
The expanded conversation stack used 35pt inter-item spacing while being
forced into a fixed 237pt frame. With multiple conversations, its
children rendered beyond that frame, but the surrounding agent list only
reserved the fixed height, so later agent rows appeared underneath the
overflowing content.

## Test plan
- [x] `swiftlint lint --strict --no-cache
ZooClaw/Views/SidebarDrawerView.swift`
- [x] `xcrun swiftc -frontend -parse
ZooClaw/Views/SidebarDrawerView.swift`
- [x] Generic iOS Simulator Debug build with `xcodebuild`
- [x] Multi-conversation sidebar interaction preview confirms expanded
sessions no longer overlap subsequent agent rows

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

```
## Summary
- Prevent expanded sidebar session rows from overlapping the following agent row.
- Let the conversation section use its intrinsic height while keeping each conversation and history row at a consistent 36pt height.

## Root cause
The expanded conversation stack used 35pt inter-item spacing while being forced into a fixed 237pt frame. With multiple conversations, its children rendered beyond that frame, but the surrounding agent list only reserved the fixed height, so later agent rows appeared underneath the overflowing content.

## Test plan
- [x] `swiftlint lint --strict --no-cache ZooClaw/Views/SidebarDrawerView.swift`
- [x] `xcrun swiftc -frontend -parse ZooClaw/Views/SidebarDrawerView.swift`
- [x] Generic iOS Simulator Debug build with `xcodebuild`
- [x] Multi-conversation sidebar interaction preview confirms expanded sessions no longer overlap subsequent agent rows

```

