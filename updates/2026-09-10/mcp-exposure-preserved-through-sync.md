---
title: "修复：Agent 配了 MCP 的「直连」模式，被一次无关的同步悄悄改回「延迟」；部分 Agent 整体读取失败"
type: "Bug Fix"
priority: "高"
date: "2026-09-10"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：Agent 配了 MCP 的「直连」模式，被一次无关的同步悄悄改回「延迟」；部分 Agent 整体读取失败

## 核心宣传点

这是一个典型的「上游加字段、下游 schema 太严」引发的连锁故障，影响面不小，值得说清。

Engine 侧（engine #1216，自 `v0.1.28-release` 起在生产）给 managed agents API 的 `resource.mcp[]` 加了一个可选字段 `exposure: "deferred" | "direct"`。而 claw-interface 里对应的 `EngineMcpServer` 模型是 `extra="forbid"` 且没有这个字段，于是带该字段的 Agent 遭遇两类问题：

- **读不出来**：逐条 `model_validate` 直接抛 ValidationError，导致 `get_agent` / `get_agent_status` 的 **20 多个调用点**（agent builder、activation / apply / change_set / revision、`service_api`）对这个 Agent 全部失败。
- **配置被静默回退**：即使读侧不炸，MCP 同步与 ACP 那两条路径都是「读回整个数组 → 保留不归自己管的条目 → 整体 PUT 回去」，而回写用的 `model_dump(exclude_none=True)` 会把 schema 不认识的键丢掉——于是**一次完全无关的同步，就把你配好的 `direct` 悄悄改回 `deferred`**。

修复做了两件事：`EngineMcpServer` 显式声明 `exposure: Literal["deferred", "direct"] | None = None`，缺省 `None` 表示「未声明」，不会替调用方发一个它没要求的值；同时把 `extra` 从 `forbid` 改成 `allow`——这个 schema 本质是 Engine 所拥有契约的一个投影，本服务只是读回、保留、原样写回，Engine 之后再加字段（计划中还有 `permission` / `tools` / `context`）不该让整体读取失败，也不该在回写时被静默丢弃。构造侧的拼写保护仍由 pyright 的字段签名提供。

## 原始内容

### fix(claw-interface): keep Engine-owned MCP options through the read/write-back (#3680)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `b27a2646`
- PR: #3680
- 作者: Chris@ZooClaw
- 日期: 2026-09-10T03:30:31Z
- 关联 Issue: #3679

改动（PR 原文要点）：

- `EngineMcpServer` 显式声明 `exposure: Literal["deferred", "direct"] | None = None`。
- `extra` 由 `forbid` 改为 `allow`，使 Engine 后续新增字段不致读取整体失败或回写丢弃。
- 两个回归测试：engine client 层钉住带 `exposure` 和一个未知键的条目能读进来并逐字段回写；`mcp_sync_service` 层钉住 personal MCP 同步不会重置它不管的 server 的 `exposure`。

验证：`pytest tests/unit/test_engine_client.py tests/unit/test_mcp_sync_service.py tests/unit/test_acp_engine_mcp.py tests/unit/test_engine_client_mcp.py` — 100 passed；改动文件 `ruff check` / `ruff format --check` 通过；pyright 对改动文件除本地 venv 解析不到的 import 假阴性外通过。

## 备注

发布状态：已上线（已包含在 `ecap-v0.19.3-release` 正式发布中）。

对外发布注意：这条对普通用户偏底层，建议只进 Discord + changelog，措辞落在「MCP 直连设置不会再被同步重置」这个可感知结果上，不必展开 schema 细节。
