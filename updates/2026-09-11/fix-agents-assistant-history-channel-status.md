---
title: "修复：Assistant 历史对话打不开、改完渠道配置状态不刷新"
type: "Bug Fix"
priority: "高"
date: "2026-09-11"
status: "待审核"
channels: "changelog"
---

# 修复：Assistant 历史对话打不开、改完渠道配置状态不刷新

## 核心宣传点

Assistant（Main）这条链路上的几个问题一起修掉了。

**新建的 Assistant 对话走对流程了**。Engine 支撑的 Assistant 新会话现在和其他 Engine Agent 一样，走同一套任务创建和 ACS 绑定流程。computer-runtime 那条路径保持不变。

**历史对话能正常打开了**。已有的 Web 对话现在会用 Engine 记录的原始 thread 重新打开——哪怕之前某次访问失败、在规范 Engine session ID 下留了个空映射，也能正确恢复。原始存储记录保留不动，ACS 绑定校验照旧执行。

**头像显示正常**。工作区已有的 Main 身份信息暴露给详情页，没配自定义头像时复用标准 Assistant 头像。

**渠道状态会刷新了**。改完渠道配置之后，当前 Agent 的渠道状态保持最新，不用手动刷页面才能看到变化。

## 原始内容

### fix(agents): restore Assistant history and refresh channel status (#3698)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `4294b890`
- PR: #3698
- 作者: kaka-srp
- 日期: 2026-09-11

改动要点（PR 原文）：将新的 Engine 支撑 Assistant 会话路由到与其他 Engine Agent 相同的任务创建与 ACS 绑定流程，computer-runtime 路径保持不变；使用 Engine 记录的原始 thread 重新打开已有 Web 对话，即使此前失败的访问在规范 Engine session ID 下创建了空映射，同时保留原始存储记录并继续强制 ACS 绑定校验；将工作区已有的 Main 身份暴露给详情页，未配置自定义头像时复用标准 Assistant 头像；覆盖无 Build 基线的 Main 历史列表、原始 thread 复用、scope 与归档防护、创建/路由及头像呈现的测试；配置后保持当前 Agent 渠道状态最新。

## 备注

发布状态：已上线（已包含在 `ecap-v0.19.5-release` 中）。

对外发布注意：Assistant 是默认入口，历史对话打不开属于高感知问题。进 changelog。
