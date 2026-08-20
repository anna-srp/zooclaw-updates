---
title: "个人 MCP 管理上线：一段 JSON 接入任意远程 MCP 服务器"
type: "新功能上线"
priority: "高"
date: "2026-08-19"
status: "待审核"
channels: ""
---

# 个人 MCP 管理上线：一段 JSON 接入任意远程 MCP 服务器

## 核心宣传点

插件页新增「Personal MCP」标签页，填一段 JSON 就能接入远程 MCP 服务器，系统会自动发现该服务器提供的工具，支持连接启停、刷新、编辑、删除，还能逐个工具单独开关。密钥只在创建/更新时上传，永不回传浏览器。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `f63f7ba6e96e11a5ae6cdf6493c4f12424b81d00`
- PR: #3383
- 作者: sam-srp
- 日期: 2026-08-19T11:15:05Z

### Commit Message

```
feat: add personal MCP management UI (#3383)

## Summary
- add a Personal MCP tab to Plugins with one JSON configuration per
remote server
- support automatic tool discovery, connection enable/disable, refresh,
edit, delete, and per-tool enable/disable
- add Claw Interface proxy routes to the Engine MCP control plane and a
mock-backend implementation for local UI development
- keep V2 Agent settings hidden; personal MCP is user-global in phase 1
- show MCP when the V2 install capability and Main Agent both use the
Engine runtime; specialist Agents may remain on the v1 runtime during
migration
- keep a successful MCP availability decision stable for the current
browser page lifetime, re-evaluate after a full refresh, and retry
failed checks instead of caching them as unavailable

## UX details
- new connections start enabled and show a pulsing pending state until
discovery completes
- expanded rows expose refresh/edit/delete actions and the real
discovered tool list
- secrets are sent only on create/update and are never returned to the
browser
- direct `?tab=mcp` navigation falls back to Connectors when the install
capability or Main Agent is not on Engine

## Validation
- Web lint and TypeScript checks passed
- targeted MCP and Plugins Web unit tests passed, including
mixed-runtime, Main-Agent eligibility, page-lifetime stability, and
failed-check retry coverage
- Claw Interface unit tests and Ruff checks passed
- local cross-service CloudBase MCP flow verified end to end

## Design
- repository phase 1 design spec updated with the Main-Agent eligibility
and mixed-runtime rollout contract
- [Feishu design
document](https://starquest.feishu.cn/docx/Ql4Qd1lc4oSMRExvzGgcPtWDntc)

## Dependency
- requires SerendipityOneInc/zooclaw-engine#748

## Deployment
- no new environment variables
- Claw Interface reuses `ZOOCLAW_ENGINE_URL`,
`ZOOCLAW_ENGINE_SERVICE_TOKEN`, and the existing V2
`ZOOCLAW_ENGINE_ADMIN_TOKEN`
```

### PR Body

## Summary
- add a Personal MCP tab to Plugins with one JSON configuration per remote server
- support automatic tool discovery, connection enable/disable, refresh, edit, delete, and per-tool enable/disable
- add Claw Interface proxy routes to the Engine MCP control plane and a mock-backend implementation for local UI development
- keep V2 Agent settings hidden; personal MCP is user-global in phase 1
- show MCP when the V2 install capability and Main Agent both use the Engine runtime; specialist Agents may remain on the v1 runtime during migration
- keep a successful MCP availability decision stable for the current browser page lifetime, re-evaluate after a full refresh, and retry failed checks instead of caching them as unavailable

## UX details
- new connections start enabled and show a pulsing pending state until discovery completes
- expanded rows expose refresh/edit/delete actions and the real discovered tool list
- secrets are sent only on create/update and are never returned to the browser
- direct `?tab=mcp` navigation falls back to Connectors when the install capability or Main Agent is not on Engine

## Validation
- Web lint and TypeScript checks passed
- targeted MCP and Plugins Web unit tests passed, including mixed-runtime, Main-Agent eligibility, page-lifetime stability, and failed-check retry coverage
- Claw Interface unit tests and Ruff checks passed
- local cross-service CloudBase MCP flow verified end to end

## Design
- repository phase 1 design spec updated with the Main-Agent eligibility and mixed-runtime rollout contract
- [Feishu design document](https://starquest.feishu.cn/docx/Ql4Qd1lc4oSMRExvzGgcPtWDntc)

## Dependency
- requires SerendipityOneInc/zooclaw-engine#748

## Deployment
- no new environment variables
- Claw Interface reuses `ZOOCLAW_ENGINE_URL`, `ZOOCLAW_ENGINE_SERVICE_TOKEN`, and the existing V2 `ZOOCLAW_ENGINE_ADMIN_TOKEN`

