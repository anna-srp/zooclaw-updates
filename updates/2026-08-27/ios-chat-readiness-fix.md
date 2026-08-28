---
title: "修复：iOS App 聊天界面一直转圈连不上，实际账号里有可用 Agent"
type: "Bug Fix"
priority: "高"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 修复：iOS App 聊天界面一直转圈连不上，实际账号里有可用 Agent

## 核心宣传点

部分账号在 iOS App 里打开聊天会永远停在连接中：App 只肯等那个「主 Agent」变成活跃状态，主 Agent 不满足条件时就一直轮询到会话结束，发消息直接失败。现在 App 判断逻辑和网页端对齐——只要账号里存在任意一个可连接的 Agent 就能开始聊天；确实一个都没有时，会明确提示「该账号还没有配置聊天 Agent」并给出「重新检查」按钮，而不是让你对着转圈干等。雇佣新 Agent 后也会自动重连。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `587e43710617a74f00c3376c9794b89976c65d57`
- PR: #3544
- 作者: bill-srp
- 日期: 2026-08-27T10:59:52Z

### Commit Message

```
fix(ios): gate chat on runtime capability and any connectable engine agent (#3544)

## Linear
<!-- follow-up to #3526; no Linear issue -->

## Summary
- **Bug (TestFlight 1.9.0 build 3, prod):** an account whose main engine
agent isn't `active` with a Mattermost DM never got chat:
`AgentRuntimeViewModel.waitForMainAgent` polled `GET
/agents?runtime=engine` for the whole session, Mattermost was never
contacted, and sends failed with `noActiveChannel`. Web works on the
same account because it gates only on `install-capability == engine` and
connects to **any** active engine agent with a DM channel
(`selectChatEligibleAgents`, main preferred).
- **Fix:** readiness = capability only (main-agent poll and its
`/agents` request burst removed); `MattermostViewModel.ChatAvailability`
(`unknown | noAgent | available`) drives a "No chat agent is set up for
this account yet" banner with **Check again**; the composer is disabled
with "Connecting…" until chat is available *and* connected; one
automatic reconnect after a successful agent install or when the agent
list gains a connectable row.
- Spec: `docs/superpowers/specs/2026-08-27-ios-v2-chat-readiness.md`.
Follow-up to #3526.

## Test plan
- [x] `swiftlint --strict` 0 violations; simulator build + whole
`ZooClawTests` bundle green locally (counts in PR checks)
- [x] Unit: capability `engine` ⇒ `.ready` with no `/agents` poll;
`computer` ⇒ `.notEligible`; cancellation ⇒ `.idle`; generation guard
across reset; `.noAgent` when no DM-capable agent (no `/users/me`, no
WS); connects on a non-main DM-capable agent;
`ChatComposerState.resolve` matrix; reconnect after hire
- [ ] TestFlight re-test on the `7279764241869537280` account (org
`4ee1b7db…`): chat connects or shows the no-agent banner instead of
spinning; hire an agent → chat connects
```

### PR Description

```
## Linear
<!-- follow-up to #3526; no Linear issue -->

## Summary
- **Bug (TestFlight 1.9.0 build 3, prod):** an account whose main engine agent isn't `active` with a Mattermost DM never got chat: `AgentRuntimeViewModel.waitForMainAgent` polled `GET /agents?runtime=engine` for the whole session, Mattermost was never contacted, and sends failed with `noActiveChannel`. Web works on the same account because it gates only on `install-capability == engine` and connects to **any** active engine agent with a DM channel (`selectChatEligibleAgents`, main preferred).
- **Fix:** readiness = capability only (main-agent poll and its `/agents` request burst removed); `MattermostViewModel.ChatAvailability` (`unknown | noAgent | available`) drives a "No chat agent is set up for this account yet" banner with **Check again**; the composer is disabled with "Connecting…" until chat is available *and* connected; one automatic reconnect after a successful agent install or when the agent list gains a connectable row.
- Spec: `docs/superpowers/specs/2026-08-27-ios-v2-chat-readiness.md`. Follow-up to #3526.

## Test plan
- [x] `swiftlint --strict` 0 violations; simulator build + whole `ZooClawTests` bundle green locally (counts in PR checks)
- [x] Unit: capability `engine` ⇒ `.ready` with no `/agents` poll; `computer` ⇒ `.notEligible`; cancellation ⇒ `.idle`; generation guard across reset; `.noAgent` when no DM-capable agent (no `/users/me`, no WS); connects on a non-main DM-capable agent; `ChatComposerState.resolve` matrix; reconnect after hire
- [ ] TestFlight re-test on the `7279764241869537280` account (org `4ee1b7db…`): chat connects or shows the no-agent banner instead of spinning; hire an agent → chat connects

```

---
