---
title: "桌面端账号切换重连修复"
type: "Bug Fix"
priority: "中"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# 桌面端账号切换重连修复

## 核心宣传点
修复了桌面端切换账号后仍连接到上一个账号机器人、导致设备配对不显示的问题，账号切换后设备能正确配对。

## 原始内容
```
fix(desktop): account-keyed reconnect, node-only bootstrap, dev process cleanup (#2335)

## Summary
Three desktop fixes found during PandaClaw acceptance testing:

- **Account-keyed reconnect** — the desktop reconnect fast-path reused
the persisted gateway target/token without checking it belonged to the
currently logged-in account. After switching accounts the node kept
reconnecting to the *previous* account's bot, so the current account's
dashboard never showed a paired device. The cached `remote-target` is
now tagged with the `uid` that created it; the fast-path only fires when
it matches the current uid, otherwise it falls through to a fresh
pairing. Pre-existing caches (no uid) are treated as stale and re-pair.
- **Node-only bootstrap (least privilege)** — the desktop client
connects as a `node` with no scopes, but the bootstrap token profile
over-granted `roles: [node, operator]` + `operator.*` scopes. The
gateway auto-approves the node role but holds the operator-scope grant
for explicit approval, leaving a "role upgrade requires approval"
pending on every (re)connect. The bootstrap now requests the `node` role
only, so pairing is fully automatic.
- **Dev process-group cleanup** — `pnpm dev` spawned web (next) +
electron via `shell: true` and only killed the `sh` wrapper, so closing
the app window orphaned the real `next dev` server. It kept holding port
3000, shifting later launches to 3001/3002/3003 and breaking the
desktop→BFF connection. Each child is now spawned `detached` and the
whole process group is killed on every exit path
(SIGINT/SIGTERM/SIGHUP/exit/uncaughtException/window-close); added a
`pnpm dev:kill` manual nuke for stuck orphans.

## Linear
https://linear.app/srpone/issue/ECA-879

## Test plan
- [x] Switch accounts in PandaClaw → desktop node re-pairs against the
new account's bot instead of silently reconnecting to the old one.
- [x] Fresh pairing no longer leaves an operator-scope "role upgrade
requires approval" pending; node pairs + serves commands automatically.
- [x] Close the app window → no orphaned `next dev` / port left
occupied; next launch binds 3000 cleanly.
- [x] `tsc --noEmit` clean (desktop).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>

---

### PR Description

## Summary
Three desktop fixes found during PandaClaw acceptance testing:

- **Account-keyed reconnect** — the desktop reconnect fast-path reused the persisted gateway target/token without checking it belonged to the currently logged-in account. After switching accounts the node kept reconnecting to the *previous* account's bot, so the current account's dashboard never showed a paired device. The cached `remote-target` is now tagged with the `uid` that created it; the fast-path only fires when it matches the current uid, otherwise it falls through to a fresh pairing. Pre-existing caches (no uid) are treated as stale and re-pair.
- **Node-only bootstrap (least privilege)** — the desktop client connects as a `node` with no scopes, but the bootstrap token profile over-granted `roles: [node, operator]` + `operator.*` scopes. The gateway auto-approves the node role but holds the operator-scope grant for explicit approval, leaving a "role upgrade requires approval" pending on every (re)connect. The bootstrap now requests the `node` role only, so pairing is fully automatic.
- **Dev process-group cleanup** — `pnpm dev` spawned web (next) + electron via `shell: true` and only killed the `sh` wrapper, so closing the app window orphaned the real `next dev` server. It kept holding port 3000, shifting later launches to 3001/3002/3003 and breaking the desktop→BFF connection. Each child is now spawned `detached` and the whole process group is killed on every exit path (SIGINT/SIGTERM/SIGHUP/exit/uncaughtException/window-close); added a `pnpm dev:kill` manual nuke for stuck orphans.

## Linear
https://linear.app/srpone/issue/ECA-879

## Test plan
- [x] Switch accounts in PandaClaw → desktop node re-pairs against the new account's bot instead of silently reconnecting to the old one.
- [x] Fresh pairing no longer leaves an operator-scope "role upgrade requires approval" pending; node pairs + serves commands automatically.
- [x] Close the app window → no orphaned `next dev` / port left occupied; next launch binds 3000 cleanly.
- [x] `tsc --noEmit` clean (desktop).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

```
