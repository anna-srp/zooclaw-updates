---
title: "修复：安装失败的 Agent 残留占位符污染列表，现在可以删掉了"
type: "Bug Fix"
priority: "中"
date: "2026-09-11"
status: "待审核"
channels: "changelog"
---

# 修复：安装失败的 Agent 残留占位符污染列表，现在可以删掉了

## 核心宣传点

装 Agent 失败之后留下的那些"僵尸"占位符，之前会一直挂在列表和统计里，删不掉也用不了。这次做了清理和区分。

**列表干净了**。未绑定的失败或不完整的遗留安装占位符，从统一 Agent 列表、快捷入口和统计里排除掉。注意区分：已绑定的 `install_failed` Agent 仍然可见、可管理，和 active / disabled / error / uninstall-failed 状态的 Agent 一样；草稿恢复流程不变。

**失败占位符可以删了**，但有前提。所有者可以软删除一个没有绑定 Computer、且带原始 Pack ID 的失败 Pack 安装占位符——不过要先通过 owner/org/workspace-label 查询确认 Engine 侧确实没有对应的运行时才行。

**几个失败闭环处理得比较谨慎**。如果 Engine 创建其实成功了，只是响应或者 Mongo ID 写入丢了，那么安装重试锚点会保留下来，不会误删。查询出错或者响应格式不对时一律 fail closed，不执行任何删除。真实运行时身份的生命周期保持原样。

**还有一处**：最近会话列表做了折叠。

## 原始内容

### fix(agents): handle failed installs and fold recent conversations (#3695)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `8ed456b6`
- PR: #3695
- 作者: kaka-srp
- 日期: 2026-09-11

改动要点（PR 原文）：将未绑定的失败或不完整遗留安装占位符从统一 Agent 列表、快捷入口与统计中排除，已绑定的 `install_failed` Agent 仍与 active/disabled/error/uninstall-failed 状态一同可见可管理，草稿恢复不变；允许所有者软删除没有绑定 Computer 且带原始 Pack ID 的失败 Pack 安装占位符，仅在 owner/org/workspace-label 查询确认 Engine 无对应运行时之后；若 Engine 创建成功但其响应或 Mongo ID 写入丢失，保留安装重试锚点，查询错误或格式错误的响应 fail closed 且不执行删除；保持真实运行时身份的既有生命周期；匹配失败状态、身份、owner/org、revision 缺失与观测到的更新行为。

## 备注

发布状态：已上线（已包含在 `ecap-v0.19.5-release` 中）。

对外发布注意：属于清理类修复，用户感知为"列表变干净了、失败的能删了"。进 changelog 即可。
