---
title: "修复：更新从旧版迁移来的 Agent 前，会先问你一句「这会暂停同机的其他 Agent」"
type: "Bug Fix"
priority: "中"
date: "2026-09-04"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：更新从旧版迁移来的 Agent 前，会先问你一句「这会暂停同机的其他 Agent」

## 核心宣传点

从 V1 迁移过来的 Agent 工作区有个共享运行环境的特性：更新其中一个，可能会连带把同一台机器上的其他 Agent 一起暂停掉。以前这件事是静默发生的——你点个更新，别的 Agent 就莫名其妙停了，事后也不知道是谁干的。

现在这类工作区会被显式标记出来，它们的后台 Pack 批量更新会被推迟，并且必须由你**明确确认一次**之后才会真的执行。确认弹窗在所有会遇到这个动作的地方都补齐了：侧边栏、Agents 管理页、我的 Agent、聊天会话、Agent Builder 的发布与更新流程，以及 iOS 端。

底层的运行时选择逻辑也一并修正：原来是靠一份写死的 Pack ID 白名单来决定走哪个运行时，现在改为按提交内容的能力检测——具备有效 Engine 资产的走 V2，已批准的旧版提交继续走 V1 归档路径，并且已经是 V2 的 Agent 不会被悄悄降级回 V1。Agent Builder V2 现在会正常产出 Engine 运行时资产，环境就绪的异步等待窗口也加了有界重试。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `e9f91acc76aa5dfd31951ad15053b196da840c2a`
- PR: #3649
- 作者: kaka-srp
- 日期: 2026-09-04T09:07:02Z

### Commit Message

```
fix(agents): confirm migrated shared computer updates (#3649)

## Summary

- Replace the Pack-ID runtime allowlist with submission capability
detection: valid Engine assets use V2, approved legacy submissions keep
the V1 archive path, and existing V2 provenance cannot silently
downgrade.
- Mark V1-migrated Agent workspaces that may pause sibling Agents, defer
their background Pack fan-out update, and require an explicit user
confirmation before forwarding `allow_shared_computer_pause=true`.
- Add the confirmation flow to SideNav, Agents Manager, My Agents, chat
sessions, Agent Builder publish/update, and iOS.
- Publish Engine runtime assets from Agent Builder V2 and retry the
bounded async Environment-readiness window.
- Preserve `AGENTS_V1_ONLY_UIDS`; keep the deprecated Pack allowlist
values in deployment overlays only for one older-image rollback window.
New code ignores that setting.

## Root cause

The migrated Agent still shares a legacy Computer, so a Pack update that
changes its Environment can pause sibling Agents. The previous update
path neither had an explicit user-consent contract for that disruption
nor a capability-based way to distinguish legacy Pack submissions from
V2 Engine assets. A Pack-ID allowlist was therefore both too narrow and
unable to express the actual runtime compatibility.

## Behavior

- Normal Agents update without an extra prompt.
- A migrated shared-Computer Agent shows a conservative warning that
sibling Agents may be temporarily unavailable and active tasks may be
interrupted; data and memories are preserved.
- Only the confirmed retry sends `allow_shared_computer_pause=true`.
- Legacy Packs without an Engine asset continue through V1
compatibility; malformed or missing metadata for a previously V2 Agent
fails closed.

## Test plan

- [x] Backend unit suite: 647 tests passed in focused review validation.
- [x] Post-refactor backend selection/lifecycle/routes suite: 202 tests
passed.
- [x] `bash scripts/verify-py.sh` passed (Ruff, format, Pyright, import
contracts).
- [x] Web unit suite: 298 focused tests passed; the complete Web CI
suite also passed after fixing an incomplete legacy test mock.
- [x] `bash scripts/verify-web.sh --no-test` and push-gate Web checks
passed.
- [x] iOS SwiftLint, simulator build, and tests passed on macOS CI.
- [x] Three focused agent reviews and both repository auto-review gates
completed with no remaining findings.

## Rollout

Deploy the Engine companion first, then the ECAP backend, Web, and iOS
clients. This PR does not deploy or migrate user data.

## Companion PR

- Engine contract and Computer-level fence:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1229
```

### PR Body

```
## Summary

- Replace the Pack-ID runtime allowlist with submission capability detection: valid Engine assets use V2, approved legacy submissions keep the V1 archive path, and existing V2 provenance cannot silently downgrade.
- Mark V1-migrated Agent workspaces that may pause sibling Agents, defer their background Pack fan-out update, and require an explicit user confirmation before forwarding `allow_shared_computer_pause=true`.
- Add the confirmation flow to SideNav, Agents Manager, My Agents, chat sessions, Agent Builder publish/update, and iOS.
- Publish Engine runtime assets from Agent Builder V2 and retry the bounded async Environment-readiness window.
- Preserve `AGENTS_V1_ONLY_UIDS`; keep the deprecated Pack allowlist values in deployment overlays only for one older-image rollback window. New code ignores that setting.

## Root cause

The migrated Agent still shares a legacy Computer, so a Pack update that changes its Environment can pause sibling Agents. The previous update path neither had an explicit user-consent contract for that disruption nor a capability-based way to distinguish legacy Pack submissions from V2 Engine assets. A Pack-ID allowlist was therefore both too narrow and unable to express the actual runtime compatibility.

## Behavior

- Normal Agents update without an extra prompt.
- A migrated shared-Computer Agent shows a conservative warning that sibling Agents may be temporarily unavailable and active tasks may be interrupted; data and memories are preserved.
- Only the confirmed retry sends `allow_shared_computer_pause=true`.
- Legacy Packs without an Engine asset continue through V1 compatibility; malformed or missing metadata for a previously V2 Agent fails closed.

## Test plan

- [x] Backend unit suite: 647 tests passed in focused review validation.
- [x] Post-refactor backend selection/lifecycle/routes suite: 202 tests passed.
- [x] `bash scripts/verify-py.sh` passed (Ruff, format, Pyright, import contracts).
- [x] Web unit suite: 298 focused tests passed; the complete Web CI suite also passed after fixing an incomplete legacy test mock.
- [x] `bash scripts/verify-web.sh --no-test` and push-gate Web checks passed.
- [x] iOS SwiftLint, simulator build, and tests passed on macOS CI.
- [x] Three focused agent reviews and both repository auto-review gates completed with no remaining findings.

## Rollout

Deploy the Engine companion first, then the ECAP backend, Web, and iOS clients. This PR does not deploy or migrate user data.

## Companion PR

- Engine contract and Computer-level fence: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1229

```
