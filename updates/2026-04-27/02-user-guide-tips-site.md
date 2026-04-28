---
title: "User Guide 升级：跳转独立 Tips 站点"
type: "体验优化"
priority: "低"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# User Guide 升级：跳转独立 Tips 站点

## 核心宣传点
点击 ZooClaw 侧栏和官网 header 中的「User Guide」，现在会在新标签页打开独立的使用技巧站点，支持中/日/英三语版本，内容更丰富。

## 原始内容
**Commit**: feat(web): User Guide 跳转到独立 tips 站点（新标签页）— 官网 header + 侧栏 sidebar (#1311)  
**PR Body**:  
User Guide 点击改为新标签页打开独立 tips 站点（zooclaw.ai/tips/），支持多语言（zh/ja/en）。官网 header 和侧栏 sidebar 均已更新。Cloudflare zone 路由 /tips/* → tips worker，前端不再耦合具体域名，由 Cloudflare 边缘根据请求 Host 决定部署环境。external: true 保留，新标签页打开符合用户预期。
