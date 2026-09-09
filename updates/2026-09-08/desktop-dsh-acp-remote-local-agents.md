---
title: "ZooClaw Desktop 能接远程 V2 Agent 了，也能挂本地 Codex / Claude Code"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-08"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---

# ZooClaw Desktop 能接远程 V2 Agent 了，也能挂本地 Codex / Claude Code

## 核心宣传点

桌面端这次补上了最关键的一环：DSH 会话现在可以直接连到**你自己的远程 V2 Engine Agent**，也可以连**本地跑的编码 Agent**。

ZooClaw Desktop 会自动发现你已登录账号下的 Engine 工作区，选一个就能把 DSH 接到那个远程 V2 Agent 上，走的是通过 Claw Interface 暴露的**已认证 ACP 会话**——不需要你手工配端口、贴 token。

新增的 Agent 选择器给了三个明确目标：**远程 V2 Agent**、**本地 Codex**、**本地 Claude Code**。官方的 Codex ACP 与 Claude Agent ACP 适配器直接打包进来，本地 Agent 各自跑在**隔离的 DSH home** 里互不污染；本地 Agent 想用 DSH 的工具，走标准 ACP `mcpServers`、底层是带认证的 loopback Streamable HTTP。

安全边界划得挺清楚：目标命令、适配器路径、环境变量和端口**全部由 Electron 主进程掌管**，渲染进程只能从允许名单里挑一个目标 ID，选不出名单外的东西。另外实现了符合标准的 MCP-over-ACP 桥接，含**限定在单次 prompt 作用域内的 MCP 租约**（prompt-scoped MCP leases），出问题时显式失败而不是静默降级。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `f9713045`
- PR: #3659
- 日期: 2026-09-08

### Commit Message

```
feat(desktop): connect DSH to remote and local ACP agents (#3659)

## Summary

- consolidate the managed Desktop DSH conversation foundation from #3511
into this PR; #3511 remains closed and is fully contained in this branch
- expose authenticated ACP sessions for owned V2 Engine agents through
Claw Interface
- implement the ACP lifecycle and standards-conformant MCP-over-ACP
bridge, including prompt-scoped MCP leases
- let ZooClaw Desktop discover the signed-in user's Engine workspaces
and connect DSH to the selected remote V2 Agent automatically
- add a runtime-managed Agent selector with three explicit targets:
Remote V2 Agent, local Codex, and local Claude Code
- bundle the official Codex ACP and Claude Agent ACP adapters, isolate
local Agent state in separate DSH homes, and expose local DSH tools
through standard ACP `mcpServers` backed by authenticated loopback
Streamable HTTP
- keep target commands, adapter paths, environment variables, and ports
owned by Electron Main; the renderer can only select an allow-listed
target ID
- fail explicitly when the selected target is unavailable or when remote
V2 is selected without a Desktop login; do not silently fall back to
another Agent

## Dependency

- uses the DSH implementation from SerendipityOneInc/deepseek-harness#12

## Bundled runtime

- DSH: `0.1.1-rc.2`
- DSH source commit: `bca37f82333c8fdb6ab32eac894cc5a40d583709`
- Codex ACP adapter: `1.10.0`
- Claude Agent ACP adapter: `0.74.0`
- darwin-arm64 artifact SHA-256:
`b245b790d15bd60113106b1c734d4497ba56916e0fe2df740bd137d73b6e1479`

## Protocol compatibility

- validates the ACP handshake and MCP server declarations against pinned
official ACP fixtures
- exposes MCP Streamable HTTP to V2 Engine while forwarding tool traffic
over the owning ACP connection
- uses standard ACP `mcpServers` for the official local adapters; local
DSH publishes its authenticated MCP catalog on a dynamically allocated
loopback port
- authenticates Desktop ACP WebSockets and isolates remote tool routing
by bridge lease

## Validation

- `bash scripts/verify-changed.sh`: Web governance, TypeScript, ESLint,
Claw Interface ruff, formatting, pyright, and import contracts passed
- Desktop TypeScript passed; 41 tests passed and the opt-in external
Codex test was skipped in the normal suite
- Web target-selector and General settings tests: 34 passed
- DSH artifact checksum/path validation passed and staging is idempotent
- real local Codex ACP smoke passed end to end, including the DSH MCP
catalog and assistant response
- real local Claude adapter reached ACP session binding and the DSH MCP
catalog; the model request correctly returned the local Claude CLI's
revoked-OAuth 401, so a complete Claude response requires valid user
Claude credentials
- local Claw Interface + Telepresence staging smoke previously completed
a remote V2 response and remote invocation of a Desktop DSH tool

## Review notes

- this is the only open ecap-workspace PR for the feature and supersedes
#3511
- the large diff is dominated by the pinned ACP schema fixture and
bundled DSH artifact stored through Git LFS
- no credentials or temporary tunnel URLs are committed; runtime
endpoints and tokens remain environment-provided
```

## 备注

发布状态：已合并待发版（尚未包含在最新的 `ecap-*-release` 前端正式发布中）。本 PR 合并了先前 #3511 的托管 Desktop DSH 会话基础，#3511 保持关闭状态、其内容已完整包含在本分支。
