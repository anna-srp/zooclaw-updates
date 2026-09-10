---
title: "用量账单里的「Unknown」终于说清楚了：运行环境计算独立成一类"
type: "体验优化"
priority: "中"
date: "2026-09-09"
status: "待审核"
channels: "Discord+changelog"
---

# 用量账单里的「Unknown」终于说清楚了：运行环境计算独立成一类

## 核心宣传点

看用量明细时，有一块积分一直被归到 **Unknown** 里，谁也说不清那是什么钱。原因很实在：沙箱运行环境的计费事件带 `usage_type` 但**没有模型字段**，而用量看板是按模型分组的，没模型的就全掉进「未知」。

现在读取 Lago 事件时会识别 `usage_type=sandbox_compute`，在主站和企业后台都显示为 **Compute / 运行环境计算**，图表悬浮提示里也一样。**存量事件直接受益**——不需要重写或重新上报任何计费数据。

顺带把这一块的文案理顺了：

- 标题、空状态、汇总说明从只说「模型」改成「模型与服务」。
- 事件数改称 **usage records / 计费记录数**——一条 compute 事件代表一段已完成的执行，叫「记录数」比叫「调用次数」准确。
- 修了主站汇总的一处 fallback bug：金额带小数时会把中文翻译丢掉，退回英文。

**没变的部分**：API 字段、积分计算方式、事件计数、时间分桶、模型显示名 fallback，以及那些**真正**未知的用量——后者仍然照实显示为未知，不会被硬塞进 Compute。

## 原始内容

### fix(billing): classify compute usage across billing dashboards (#3672)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `bfb00080`
- PR: #3672
- 作者: sam-srp
- 日期: 2026-09-09T06:33:26Z

### Summary

Sandbox compute events have a `usage_type` but no model, so the usage dashboards group their credits under `Unknown`. Classify `usage_type=sandbox_compute` when reading Lago events and display **Compute / 运行环境计算** in the main app and enterprise admin, including chart tooltips. Existing events benefit without rewriting or republishing billing data.

Update headings, empty states, and summaries to include models and services. Show event counts as **usage records / 计费记录数**, since a compute event represents a completed execution segment. Preserve the existing API fields, credit calculation, event counts, time buckets, model display-name fallback, and genuinely unknown usage. Fix the main app's summary fallback so decimal amounts no longer discard Chinese translations.

### Validation

- 后端用量聚合 7 tests passed（含跨两个时间桶的 compute/tool/unknown/零成本模型混合事件，金额与计数精确校验）
- 主站用量组件 8 tests passed（用真实中英文案目录，compute 与 unknown 并存）
- 企业后台用量组件与视图模型 40 tests passed（含本地化 tooltip、服务端下发名称、旧标识 fallback）
- 后端 Ruff、Pyright、8 项 import-layer 合约通过；两个前端 TypeScript 与定向 ESLint 通过；主站治理守卫通过
- 未执行：真实账户账单对账、浏览器 smoke

### Rollout

需部署 `claw-interface`、`web/app`、`web/enterprise-admin` 三者才能拿到完整显示效果。无需 Engine 或 billing-gateway 部署，无计费迁移或重放。

## 备注

发布状态：已上线（已包含在最新 `ecap-*-release` 正式发布中）。

主站与企业后台都受影响，toB 侧同样可感知。注意 PR 声明未做真实账户对账与浏览器 smoke，对外只讲「分类与文案更清楚」，不要延伸成「修正了计费金额」——积分计算方式本身未改动。
