---
title: "修复：用 Project Key 创建的 Agent 恢复 Pro 默认规格（4 vCPU / 4 GiB），不再误配成 Starter"
type: "Bug Fix"
priority: "中"
date: "2026-10-02"
status: "待审核"
channels: ""
---

# 修复：用 Project Key 创建的 Agent 恢复 Pro 默认规格（4 vCPU / 4 GiB），不再误配成 Starter

## 核心宣传点

通过开发者平台 Project Key 创建 Agent 时，默认运行规格从误用的 Starter 恢复为 Pro（4 vCPU、4 GiB），与原来 API Platform 的产品规则一致。原因是接入 zwp_live_ 这类 Project Key 时新增的分支固定写了 starter，没有沿用旧 API Platform 的 Pro 默认规则；内部计量套餐和沙箱计算规格本来是两套独立配置。新旧 API Platform 路径现在共用同一个默认规格常量，调用方传进来的规格仍然由服务端覆盖。本次只影响之后新创建的 Agent，不开放用户自选规格，也不改存量 Agent。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary

Platform Project Key 创建 Agent 时，默认规格从误用的 Starter 恢复为 Pro（4 vCPU、4
GiB），与原 API Platform 产品规则一致。新旧 API Platform 路径共用默认规格常量，调用方传入的规格仍由服务端覆盖。

Fixes #3998

## Root cause

接入 `zwp_live_` Project Key 时新增分支固定使用 `starter`，没有沿用旧 API Platform 的 Pro
默认规则。内部 `starter_20_month` 计量套餐与 sandbox 计算规格是独立配置；API Platform 没有 Work
业务订阅，也应按既定规则默认 Pro。

同步补充 runtime 契约。本次只影响后续创建的 Agent，不开放用户自选规格，不修改存量 Agent。

## Test plan

- [x] 回归测试先复现原代码转发 `starter`、预期 `pro` 的失败，再验证修复通过。
- [x] 93 项定向测试通过：Default/具名 Project；省略规格或提交 `starter` /
`ultra`；凭据初始化、ownership 和 usage attribution；旧 API Platform 不查询 Work
订阅；Work 规格策略及内部规格接口隔离。
- [x] 提交前 Python lint、类型和 import 检查通过。
- [x] 同步最新 main 后，在最终 commit `7ab5bac5203201cae10d8710c819928bf01a7445`
运行 `ecap-verify-py-ci`：**13,661 passed、5 skipped、4 warnings；coverage
89.96%**（4 workers、sysmon、89.5% threshold）。Linux 依赖解析、静态/all CI lint 和两个
jscpd 检查全部通过。

Engine/Gateway 使用 mock，MongoDB
测试使用本地实例。本次没有更改数据库查询形式，未执行线上数据修改、部署或真实付费调用。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `d6a300f73642a7b9496812cdba0406e05d2b0ca7`
- PR: #3999
- 作者：finn-srp
- 日期：2026-10-02T07:02:19Z

### Commit Message

```
fix(platform): 恢复 Project Key 创建 Agent 的 Pro 默认规格 (#3999)

## Summary

Platform Project Key 创建 Agent 时，默认规格从误用的 Starter 恢复为 Pro（4 vCPU、4
GiB），与原 API Platform 产品规则一致。新旧 API Platform 路径共用默认规格常量，调用方传入的规格仍由服务端覆盖。

Fixes #3998

## Root cause

接入 `zwp_live_` Project Key 时新增分支固定使用 `starter`，没有沿用旧 API Platform 的 Pro
默认规则。内部 `starter_20_month` 计量套餐与 sandbox 计算规格是独立配置；API Platform 没有 Work
业务订阅，也应按既定规则默认 Pro。

同步补充 runtime 契约。本次只影响后续创建的 Agent，不开放用户自选规格，不修改存量 Agent。

## Test plan

- [x] 回归测试先复现原代码转发 `starter`、预期 `pro` 的失败，再验证修复通过。
- [x] 93 项定向测试通过：Default/具名 Project；省略规格或提交 `starter` /
`ultra`；凭据初始化、ownership 和 usage attribution；旧 API Platform 不查询 Work
订阅；Work 规格策略及内部规格接口隔离。
- [x] 提交前 Python lint、类型和 import 检查通过。
- [x] 同步最新 main 后，在最终 commit `7ab5bac5203201cae10d8710c819928bf01a7445`
运行 `ecap-verify-py-ci`：**13,661 passed、5 skipped、4 warnings；coverage
89.96%**（4 workers、sysmon、89.5% threshold）。Linux 依赖解析、静态/all CI lint 和两个
jscpd 检查全部通过。

Engine/Gateway 使用 mock，MongoDB
测试使用本地实例。本次没有更改数据库查询形式，未执行线上数据修改、部署或真实付费调用。
```

来源：SerendipityOneInc/ecap-workspace @ d6a300f7，PR #3999，作者 finn-srp。
