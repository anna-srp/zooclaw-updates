---
title: "新 Skill 上架：zooclaw-connectors 第三方服务连接器"
type: "Skill 上架/更新"
priority: "高"
date: "2026-05-13"
status: "待审核"
channels: "站内弹窗 + Use Case + Discord + changelog"
---

# 新 Skill 上架：zooclaw-connectors 第三方服务连接器

## 核心宣传点

ZooClaw Agent 现在可以直接访问你已连接的第三方服务（GitHub、Linear、Slack、Notion、Google Drive/Calendar/Gmail、Jira 等），无需为每个服务单独安装 Skill，一个连接器搞定所有集成。

## 原始内容

**来源**: ecap-skills PR #194 | SHA: 27552e67

**Commit Message**:
```
feat(zooclaw-connectors): add skill for third-party connector access via ecap-proxy-service (#194)

Thin CLI wrapper around the ecap-proxy-service /integrations/* API so an agent
can discover what the user has connected (GitHub, Linear, Slack, Notion, Google
services, etc.) and invoke tools without per-service skills.

- Single integrations.py with subcommands: list-connectors, list-connections,
  list-tools <provider>, execute <provider> <action>.
- Auth mode picked from env: USER_INTERNAL_TOKEN (User-JWT) takes priority over
  ECAP_PROXY_API_KEY + ECAP_END_USER_ID (Service-key).
- One HTTP call per invocation. Two-phase write confirmation is owned by the
  agent: first call returns summary, agent shows it, second call re-invokes with
  --confirmed. Script stays stateless.
```

**PR #194 Description**:
```
New `zooclaw-connectors/` skill that lets an agent reach the user's connected
third-party services (GitHub, Linear, Slack, Notion, Google Drive/Calendar/Gmail,
Jira, etc.) via the ecap-proxy-service `/integrations/*` API.

What's in the box:
- zooclaw-connectors/SKILL.md — frontmatter, path rule, decision flow, auth modes,
  two-phase write-confirmation, full error-code taxonomy, caching guidance, examples.
- zooclaw-connectors/scripts/zooclaw-connectors.py — single CLI with four subcommands:
  - list-connectors  → GET /integrations/connectors
  - list-connections → GET /integrations/connections
  - list-tools <provider> → GET /integrations/<provider>/tools
  - execute <provider> <action> --params-json '<json>' [--confirmed] → POST /integrations/execute
```
