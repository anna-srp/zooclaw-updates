---
title: "个人 MCP 支持「托管身份」接入：不用再自己贴 Token，凭证也不落库"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-31"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---

# 个人 MCP 支持「托管身份」接入：不用再自己贴 Token，凭证也不落库

## 核心宣传点

以前接一个自建 MCP 服务，你得自己去生成一串长期有效的 Bearer Token 或者请求头，贴进配置里存着——既麻烦又不安全。现在个人 MCP 新增了「托管身份」这种接入方式：填上 MCP 服务的 HTTPS 地址就行，平台在实际调用时用你当前的登录身份现场换一张短时效的资源令牌，不保存任何交换后的令牌。

这个托管身份声明还会自动同步到你已安装的所有 Engine Agent 上，Agent Pack 自带的 MCP 配置不受影响。MCP 的服务发现、工具筛选、启用/停用、刷新、编辑、删除这些操作全部照旧。第三方 MCP 服务仍然可以继续用静态 Bearer/请求头认证，只是托管身份不能和它们混用。

另外补了一个小体验问题：新建会话发出第一条消息时，「停止」按钮现在会立刻出现，不用等一会儿才能中断。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `4e00d84711c89033f15a80cf866429d4e38db7da`
- PR: #3479
- 作者: sam-srp
- 日期: 2026-08-31T10:49:03Z

### Commit Message

```
feat(mcp): configure managed identity personal MCP (#3479)

## Summary
- support personal MCP entries using `auth: { type: "managed_identity"
}`
- use the canonical HTTPS MCP server URL itself as the RFC 8707
resource; managed identity cannot be combined with static headers or
bearer credentials
- exchange the current user token only for MCP probing and persist no
exchanged token in personal MCP records
- synchronize the managed identity declaration to all installed Engine
Agents while preserving Agent Pack MCP entries
- preserve MCP discovery, tool filters, enable/disable, refresh, edit,
and delete behavior
- return an actionable error for credentials encrypted with an
unavailable key while allowing full secret replacement to recover the
connection
- show Stop immediately for the first message in a newly created session

## Security
- MCP configuration stores only the managed identity declaration; the
server URL defines the token resource
- `user-interface` owns the trusted-resource allowlist and rejects
unregistered resources before issuing a token
- runtime authentication uses short-lived resource tokens; no resource
token is stored in Workspace
- static bearer/header authentication remains available for third-party
MCP servers

## Deployment
No new Workspace setting is required. Claw Interface uses its existing
`ACCOUNT_SERVICE_URL` (with the existing account URL fallback) for
probe-time token exchange.

## Test plan
- 30 targeted Claw Interface MCP tests, Ruff, and Pyright
- 26 targeted web MCP/new-session tests, TypeScript, and ESLint

Part of SerendipityOneInc/zooclaw-engine#892.
```

### PR Description

```
## Summary
- support personal MCP entries using `auth: { type: "managed_identity" }`
- use the canonical HTTPS MCP server URL itself as the RFC 8707 resource; managed identity cannot be combined with static headers or bearer credentials
- exchange the current user token only for MCP probing and persist no exchanged token in personal MCP records
- synchronize the managed identity declaration to all installed Engine Agents while preserving Agent Pack MCP entries
- preserve MCP discovery, tool filters, enable/disable, refresh, edit, and delete behavior
- return an actionable error for credentials encrypted with an unavailable key while allowing full secret replacement to recover the connection
- show Stop immediately for the first message in a newly created session

## Security
- MCP configuration stores only the managed identity declaration; the server URL defines the token resource
- `user-interface` owns the trusted-resource allowlist and rejects unregistered resources before issuing a token
- runtime authentication uses short-lived resource tokens; no resource token is stored in Workspace
- static bearer/header authentication remains available for third-party MCP servers

## Deployment
No new Workspace setting is required. Claw Interface uses its existing `ACCOUNT_SERVICE_URL` (with the existing account URL fallback) for probe-time token exchange.

## Test plan
- 30 targeted Claw Interface MCP tests, Ruff, and Pyright
- 26 targeted web MCP/new-session tests, TypeScript, and ESLint

Part of SerendipityOneInc/zooclaw-engine#892.
```

## 备注

安全设计：可信资源白名单由 user-interface 侧统一管理，未注册的资源会在发令牌之前被拒绝；Workspace 不存储任何资源令牌。若历史凭证是用当前不可用的密钥加密的，界面会给出可操作的错误提示，允许整体替换密钥来恢复连接。部署侧无需新增 Workspace 配置。
