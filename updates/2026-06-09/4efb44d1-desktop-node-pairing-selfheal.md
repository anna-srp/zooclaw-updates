---
title: "桌面节点配对自动恢复，远程操作更稳定"
type: "产品基础功能更新"
priority: "中"
date: "2026-06-09"
status: "待审核"
channels: ""
---

# 桌面节点配对自动恢复，远程操作更稳定

## 核心宣传点

桌面节点在机器人重启后会自动恢复授权配对，避免出现「之前能用、突然失效」的远程操作中断。

## 原始内容

完整 commit message：

```
feat(desktop-node): node.* command namespace + agent operator pairing self-heal (#2296)

Linear: https://linear.app/srpone/issue/ECA-879

Combines two desktop-node changes (previously split as #2287 + #2296)
into one PR per request.

## 1. Namespace desktop node commands under `node.*`
The desktop node's commands used to collide with OpenClaw's built-in
**file-transfer** commands (`dir.list` / `file.*`), which routed them
through the file-transfer plugin's `allowReadPaths` policy. Rename all
desktop node commands to a dedicated `node.*` namespace:

`node.fs.list` / `node.fs.read` / `node.fs.write` / `node.fs.edit` /
`node.fs.glob` / `node.fs.grep` / `node.shell.exec` /
`node.capabilities` (drop `dir.list`).

Now pure custom node commands: gated only by
`gateway.nodes.allowCommands`, never the file-transfer plugin, invoked
by the bot via the generic `node.invoke`. Command names are validated as
`NonEmptyString` (no dot-count limit; OpenClaw itself uses two-dot
commands like `system.run.prepare`). No backward-compat aliases — this
protocol isn't live in production and lands coordinated with the
gateway-side `allowCommands` switch (already updated in gcp-foundation).

## 2. Self-heal the bot agent operator pairing
For the bot to `node.invoke`, its **own agent operator connection** must
carry `operator.write`. That pairing can be lost across a bot pod
restart and sit pending re-approval — and until re-approved every invoke
fails with `missing scope: operator.write`, even though the node is
paired and online (the exact cause of a "worked, then broke" staging
regression).

Extend the desktop-node approve flow to best-effort re-approve the
agent's own operator pairing in-process (same Control-UI `runtime_exec`
path), **strictly scoped** — only a device that is `isRepair` (re-pair
of a previously-trusted device) + operator-only roles +
`operator.*`-only scopes + cli client shape; refuses to act if more than
one candidate matches (never mass-approves); failures surface as
`ok:false`. Node approval is unaffected if the heal step errors.

> Durable fix for #2 still belongs in fastclaw (persist the bot pod's
device-pairing state across restarts). This is the claw-interface safety
net.

## Test plan
- [x] `ruff` + `ruff format` clean, `lint-imports` (8/8 incl. C3) pass.
- [x] Desktop `tsc --noEmit` passes.
- [x] claw-interface unit tests (node approve, agent-operator-repair
parse, best-effort parse) pass.
- [ ] Staging: fresh pairing registers the `node.*` commands; bot
invokes them; confirm whether the operator-pairing heal fires at the
right time (operator pending may only appear once the agent attempts an
invoke — to validate on staging).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

PR 描述：

Linear: https://linear.app/srpone/issue/ECA-879

Combines two desktop-node changes (previously split as #2287 + #2296) into one PR per request.

## 1. Namespace desktop node commands under `node.*`
The desktop node's commands used to collide with OpenClaw's built-in **file-transfer** commands (`dir.list` / `file.*`), which routed them through the file-transfer plugin's `allowReadPaths` policy. Rename all desktop node commands to a dedicated `node.*` namespace:

`node.fs.list` / `node.fs.read` / `node.fs.write` / `node.fs.edit` / `node.fs.glob` / `node.fs.grep` / `node.shell.exec` / `node.capabilities` (drop `dir.list`).

Now pure custom node commands: gated only by `gateway.nodes.allowCommands`, never the file-transfer plugin, invoked by the bot via the generic `node.invoke`. Command names are validated as `NonEmptyString` (no dot-count limit; OpenClaw itself uses two-dot commands like `system.run.prepare`). No backward-compat aliases — this protocol isn't live in production and lands coordinated with the gateway-side `allowCommands` switch (already updated in gcp-foundation).

## 2. Self-heal the bot agent operator pairing
For the bot to `node.invoke`, its **own agent operator connection** must carry `operator.write`. That pairing can be lost across a bot pod restart and sit pending re-approval — and until re-approved every invoke fails with `missing scope: operator.write`, even though the node is paired and online (the exact cause of a "worked, then broke" staging regression).

Extend the desktop-node approve flow to best-effort re-approve the agent's own operator pairing in-process (same Control-UI `runtime_exec` path), **strictly scoped** — only a device that is `isRepair` (re-pair of a previously-trusted device) + operator-only roles + `operator.*`-only scopes + cli client shape; refuses to act if more than one candidate matches (never mass-approves); failures surface as `ok:false`. Node approval is unaffected if the heal step errors.

> Durable fix for #2 still belongs in fastclaw (persist the bot pod's device-pairing state across restarts). This is the claw-interface safety net.

## Test plan
- [x] `ruff` + `ruff format` clean, `lint-imports` (8/8 incl. C3) pass.
- [x] Desktop `tsc --noEmit` passes.
- [x] claw-interface unit tests (node approve, agent-operator-repair parse, best-effort parse) pass.
- [ ] Staging: fresh pairing registers the `node.*` commands; bot invokes them; confirm whether the operator-pairing heal fires at the right time (operator pending may only appear once the agent attempts an invoke — to validate on staging).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

