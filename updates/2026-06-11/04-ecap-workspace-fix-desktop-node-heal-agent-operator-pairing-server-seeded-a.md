---
title: "桌面端设备配对自愈，配对更稳定"
type: "Bug Fix"
priority: "中"
date: "2026-06-11"
status: "待审核"
channels: ""
---

# 桌面端设备配对自愈，配对更稳定

## 核心宣传点
桌面端改为服务端下发配对信息并在授权时自动修复 Agent 配对关系，设备连接更稳定；节点命令失败时也能显示真实错误原因，不再只显示笼统的「node invoke failed」。

## 原始内容
```
fix(desktop-node): heal agent-operator pairing (server-seeded) and surface real node command errors (#2369)

## Summary
本 PR 包含 `heal-agent-operator-pairing` 分支的全部工作(此前一直未开 PR),共三块:

**1. Server-seeded desktop pairing(核心)**
- claw-interface: `desktop-pair` 路由 + schema + `desktop_node_pairing` 服务
—— 一次调用在 bot gateway 上 seed device + node pairing,返回连接目标和 device
token;并在 desktop-node approve 时自愈 bot 的 agent operator pairing
- desktop: `loadLocalIdentity()` / `applyServerPairing()` —— app 上报
deviceId + Ed25519 公钥,持久化 server 返回的 pairing,auto-connect 走 seeded
pairing 而非 bootstrap
- web: `/api/openclaw/settings/desktop-pair` 代理路由(含
`DESKTOP_PAIR_BACKEND_URL` devcontainer 调试逃生口)

**2. node.* 命令命名空间**
- desktop 节点命令统一 `node.*` 前缀,避免与 gateway 内置 file-transfer
命令(`dir.list`/`file.fetch`)冲突;按 uid 区分缓存 pairing,换账号自动重新配对

**3. node.invoke.result 错误格式修复**
- 失败回包改为协议要求的**顶层** `error: { code, message }`(此前嵌在 `payload.error`
里,gateway 读不到,所有命令失败都显示成不透明的 `node invoke failed`)

## Root cause(第 3 块)
`connection.ts` 的 invoke-dispatch 是 vendor 后补写的,未对照 gateway
协议(`NodeInvokeResultParamsSchema`):错误字符串被塞进 `payload.error`,而 gateway 的
`respondUnavailableOnNodeInvokeError` 只读顶层 `error.message`,读不到就兜底 `"node
invoke failed"`,真实失败原因(如 `old_string not found in file`)被吞掉。

## Test plan
- [x] desktop `tsc --noEmit` 通过(含 pairing 改动)
- [x] invoke 回包新格式用 openclaw gateway 真实 ajv
schema(`validateNodeInvokeResultParams`)校验通过,失败帧 `error.message` 可透传
- [x] `fsEdit` handler 冒烟:替换成功 / old_string 不存在 / 不唯一 / replace_all /
缺参数,行为全部正确
- [x] claw-interface 单测已随分支 commit
更新(`test_openclaw_settings_routes.py`),CI `python-code-quality` 验证
- [ ] 重启 desktop dev 后端到端验证:server-seeded pairing 自动连接 + `node.fs.edit`
失败时 bot 显示具体错误

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>

--- PR Description ---

## Summary
本 PR 包含 `heal-agent-operator-pairing` 分支的全部工作(此前一直未开 PR),共三块:

**1. Server-seeded desktop pairing(核心)**
- claw-interface: `desktop-pair` 路由 + schema + `desktop_node_pairing` 服务 —— 一次调用在 bot gateway 上 seed device + node pairing,返回连接目标和 device token;并在 desktop-node approve 时自愈 bot 的 agent operator pairing
- desktop: `loadLocalIdentity()` / `applyServerPairing()` —— app 上报 deviceId + Ed25519 公钥,持久化 server 返回的 pairing,auto-connect 走 seeded pairing 而非 bootstrap
- web: `/api/openclaw/settings/desktop-pair` 代理路由(含 `DESKTOP_PAIR_BACKEND_URL` devcontainer 调试逃生口)

**2. node.* 命令命名空间**
- desktop 节点命令统一 `node.*` 前缀,避免与 gateway 内置 file-transfer 命令(`dir.list`/`file.fetch`)冲突;按 uid 区分缓存 pairing,换账号自动重新配对

**3. node.invoke.result 错误格式修复**
- 失败回包改为协议要求的**顶层** `error: { code, message }`(此前嵌在 `payload.error` 里,gateway 读不到,所有命令失败都显示成不透明的 `node invoke failed`)

## Root cause(第 3 块)
`connection.ts` 的 invoke-dispatch 是 vendor 后补写的,未对照 gateway 协议(`NodeInvokeResultParamsSchema`):错误字符串被塞进 `payload.error`,而 gateway 的 `respondUnavailableOnNodeInvokeError` 只读顶层 `error.message`,读不到就兜底 `"node invoke failed"`,真实失败原因(如 `old_string not found in file`)被吞掉。

## Test plan
- [x] desktop `tsc --noEmit` 通过(含 pairing 改动)
- [x] invoke 回包新格式用 openclaw gateway 真实 ajv schema(`validateNodeInvokeResultParams`)校验通过,失败帧 `error.message` 可透传
- [x] `fsEdit` handler 冒烟:替换成功 / old_string 不存在 / 不唯一 / replace_all / 缺参数,行为全部正确
- [x] claw-interface 单测已随分支 commit 更新(`test_openclaw_settings_routes.py`),CI `python-code-quality` 验证
- [ ] 重启 desktop dev 后端到端验证:server-seeded pairing 自动连接 + `node.fs.edit` 失败时 bot 显示具体错误

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```
