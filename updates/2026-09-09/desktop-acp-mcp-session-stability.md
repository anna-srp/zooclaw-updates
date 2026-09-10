---
title: "修复：Desktop 恢复旧会话时报「Invalid MCP bridge credential」、一个大文件把整条连接搞断"
type: "Bug Fix"
priority: "高"
date: "2026-09-09"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：Desktop 恢复旧会话时报「Invalid MCP bridge credential」、一个大文件把整条连接搞断

## 核心宣传点

昨天刚上线的 Desktop 接远程 V2 Agent，这两天暴露了三个挺影响使用的问题，现在一并修掉了。

**问题一：接着聊旧会话就报凭据失效。** Engine 按 Agent 配置版本持久化 MCP 工具目录，而 Claw Interface 此前**每次 prompt 都用一个随机 bridge ID** 生成 Engine 侧的服务名和凭据。于是你恢复一个旧的 Engine 会话时，它照着记忆里的老工具名去调，而那条临时路由早就没了——直接 `Invalid MCP bridge credential`。现在工具名、公开路由和凭据在 DSH 轮换临时 ACP `serverId` 时保持**稳定不变**；每个稳定的 Engine MCP server 会被路由到当前连着的那台 Desktop，重复声明会被拒绝，你自己配的、与之冲突的个人 MCP 配置会被保留下来。

**问题二：一个超大的本地工具返回值能把整条 ACP 连接干掉。** Desktop 中继此前把任何超过 1 MiB 传输上限的响应都当致命错误处理，所以一次读了个大文件，整个连接就断了。现在超限响应会被转换成**有界的 JSON-RPC 错误**返回，ACP 连接不断——混在同一批里的响应与通知也都能正常保留。另外桥接拆除后 MCP SSE 流会干净收尾，不再留残连接。

**问题三：后台一直在偷偷重试配对。** 旧的 FastClaw Desktop node 自动连接是无条件启动的，可现在可用的 Desktop Agent 目标走的是 Mattermost 或 DSH，于是它就在那儿持续重试 `/openclaw/settings/desktop-pair`，还把 MCP-over-ACP 已经提供的本地工具路径重复了一遍。这次把它和对应的渲染进程 IPC 面一起停用，Desktop 的工作目录控制保留不变。

安全上没引入新东西：**不需要任何新环境变量**，稳定路由的凭据是从既有 `SECRET_KEY` 派生的按域分隔 HMAC。

## 原始内容

### fix(acp): stabilize Desktop MCP-over-ACP sessions (#3669)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `f8d4e4ab`
- PR: #3669
- 作者: zayne-srp
- 日期: 2026-09-09T03:21:56Z

### Summary

- keep Desktop MCP-over-ACP tool names, public routes, and credentials stable when DSH rotates its temporary ACP `serverId`
- route each stable Engine MCP server to the currently connected Desktop peer while rejecting duplicate declarations and preserving conflicting personal MCP configuration
- convert oversized local MCP responses into bounded JSON-RPC errors without disconnecting ACP, including mixed response/notification batches
- end MCP SSE streams cleanly after bridge teardown
- disable the legacy FastClaw Desktop node auto-connect and renderer IPC surface while retaining Desktop working-directory controls

### Root cause

The Engine persisted MCP catalogs by Agent configuration version, but Claw Interface previously generated the Engine server name and credential from a random bridge ID on every prompt. A resumed Engine session could therefore call an old tool name after its temporary route had been removed, producing `Invalid MCP bridge credential`. Separately, the Desktop relay treated every response above the 1 MiB transport limit as fatal, so one large local tool result terminated the whole ACP connection.

The legacy FastClaw Desktop node connector was also started unconditionally even though the available Desktop Agent targets now use Mattermost or DSH. This caused continuous `/openclaw/settings/desktop-pair` retries and duplicated the local tool path already provided by MCP-over-ACP.

### Test plan

- Desktop TypeScript typecheck；Desktop tests 46 passed（1 个 opt-in Codex 集成测试跳过）
- Claw Interface ACP/MCP tests 58 passed
- Ruff、格式化、Pyright、import-linter、changed-surface gate 与 diff 检查通过
- Telepresence staging smoke：跨 Claw Interface 与 Desktop 重启复用同一个 V2 Engine 会话，`mcp__acp-dsh-tools__read` 工具名与路由保持一致，无 401 或凭据错误
- 超限 MCP 重放：返回有界错误、混合批次中的通知被保留、同一 ACP 连接上的后续请求成功
- 已安装版 Desktop smoke：远程 V2 DSH 连接成功并完成一次本地 MCP 文件读取；过了原重试间隔后未再出现 `desktop-pair` 请求

No new environment variable is required. Stable route credentials are domain-separated HMAC values derived from the existing `SECRET_KEY`.

## 备注

发布状态：已上线（已包含在最新 `ecap-*-release` 正式发布中）。

这是 2026-09-08「Desktop 接远程 V2 Agent / 本地 Codex·Claude Code」功能的紧随修复。对外传播时建议与该功能合并叙述，或作为「Desktop 稳定性改进」单独发；单独发时需要说明它修的是 Desktop 侧远程 Agent 会话，避免与主站聊天混淆。
