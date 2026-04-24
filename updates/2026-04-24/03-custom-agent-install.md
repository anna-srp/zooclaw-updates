---
title: "自定义 Agent 一键安装：从目录记录直接部署"
type: "新功能上线"
priority: "中"
date: "2026-04-24"
status: "待审核"
channels: ""
---
# 自定义 Agent 一键安装：从目录记录直接部署

## 核心宣传点
安装自定义 Agent 更简单了——从目录记录一键安装，支持私有 Agent，重装已保存的 Agent 不需要重新配置。

## 原始内容

feat(openclaw): install custom agents from catalog records (#1231)
- Unify archive runtime deployment for pack and custom agent installs
- Resolve private custom agent installs from catalog metadata and version hashes
- Simplify publish page installs to use saved records and updated confirmations

feat(openclaw): simplify publish page custom agent install flow (#1260)
- Simplify the custom agent install and uninstall flow on the publish page
- Generate stable, readable custom agent ids from the visible agent name or package basename
- Support reinstalling saved custom agents when the persisted record already contains the archive metadata
