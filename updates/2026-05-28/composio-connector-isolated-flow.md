---
title: "新增 Composio 连接器独立接入流程（功能灰度中）"
type: "新功能上线"
priority: "中"
date: "2026-05-28"
status: "待审核"
channels: ""
---

# 新增 Composio 连接器独立接入流程（功能灰度中）

## 核心宣传点

ZooClaw 现在支持通过 Composio 连接更多第三方服务，该功能正在灰度开放中，连接更多工具生态的能力进一步扩展。

## 原始内容

feat(composio): add isolated connector flow (#1933)

Add a feature-flagged Settings entry and isolated Composio connector page. Route Composio connector UI/BFF calls through ecap-proxy-service. Keep claw-interface stateless for Composio connection data and credentials. Composio page is gated by NEXT_PUBLIC_COMPOSIO_CONNECTORS_PAGE_ENABLED / COMPOSIO_CONNECTORS_PAGE_ENABLED. Does not modify existing connector, channel, or integration execution routes.
