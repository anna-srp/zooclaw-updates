---
title: "修复：结账页的优惠码输入框不再被本地首充判断关掉，使用资格统一交给 Stripe 判定"
type: "Bug Fix"
priority: "高"
date: "2026-10-02"
status: "待审核"
channels: ""
---

# 修复：结账页的优惠码输入框不再被本地首充判断关掉，使用资格统一交给 Stripe 判定

## 核心宣传点

ZooWork 和开发者平台的充值结账现在始终提供优惠码输入入口，不再由本地逻辑判断你是不是首次充值、以前有没有充值过或用过券。优惠码的首单限制、适用产品、核销次数和有效期全部由 Stripe 决定，订阅结账也是同一套规则。原因是之前的实现把入口绑在本地「首次充值资格」上，历史 Checkout（包括没付成功的尝试）和待完成的资格占用都会把入口关掉，甚至挡住再次充值。Stripe 已确认的优惠支付现在也不再依赖本地首单标记才能到账，订单归属、产品与金额校验、退款处理和防重复到账机制保持不变。充值金额范围、到账额度算法和 Stripe 后台券配置都没有变化；上线后需要从 Add funds 新发起一笔充值来验收，旧的付款链接不会自动补上输入入口。

## 分级

- 内部：P0
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary

ZooWork 和 Platform
的充值结账始终提供优惠码输入入口，不再由本地判断用户是否首次充值、是否充值过或是否使用过优惠券。优惠码的首单限制、适用产品、核销次数和有效期全部由
Stripe 决定。ZooWork 订阅结账也保持这一规则。

- Platform 删除历史充值查询、首次优惠资格占用/消耗/释放，以及为了复用资格而关闭旧 Checkout 的逻辑。新 Checkout
复用稳定的 Stripe Customer，并始终启用优惠码输入。
- Stripe 已确认的优惠支付不再依赖本地首次订单标记才能到账。保留订单/Customer
归属、产品和金额验证、退款处理、审计及防重复到账机制。
- ZooWork 订阅与 Top up 原本已无条件开放输入入口，本次增加新老客户与两种 Checkout 模式的回归覆盖。

## Root cause

PR #3967 的 Platform 实现把优惠码入口绑定到本地“首次充值资格”：历史
Checkout（包括未付款的尝试）、已记录的首次订单和待完成的优惠资格占用，都会关闭入口或阻止再次充值。这与产品要求不符。

本次明确取消这一层业务判断；数据库中的旧资格字段仅保留用于兼容读取和审计，不参与优惠资格判断。删除不再使用的历史查询，并同步维护隔离的
staging CSFLE 检查脚本。

## Compatibility and release

- 已经发给 Stripe 的请求参数、幂等键和已生成的付款链接保持不变，避免重试时参数冲突。**上线后从 Add funds
发起一笔新的充值来验收；旧链接不会自动增加输入入口。**
- 充值金额范围、订单面额、抵扣金额与到账额度算法、Stripe 后台的券配置均不变；不新增生产数据库查询形式或数据迁移。
- 仅后端需要部署；此 PR 不执行部署或真实支付。
- 按产品负责人 Eric 已确认的验收分工，staging/线上真实优惠券资格和到账验收、加密数据库 fixture 读取/CAS 验收由
Eric 执行。代码评审工具负责代码正确性，不以代替上述环境验收为要求。此次本地测试不宣称完成真实 Stripe 或 staging CSFLE
验收。
- 需求及验收细则：`docs/superpowers/specs/2026-10-02-stripe-promotion-entry.md`。

## Test plan

- [x] 247 项定向回归：Platform 充值/Customer/重试/结算、CSFLE probe 安全逻辑、ZooWork
Checkout 与 Stripe SDK 重试（最终同一次运行：247 passed）。
- [x] `bash scripts/verify-py.sh`：ruff、格式、pyright（app/tests）、8 项 import
contracts 全通过。
- [x] 函数复杂度及其余 pre-commit 检查通过；dead-code 检查未发现本次改动遗留的死函数。原有 pyright hook
未给含空格的路径加引号，已用上述完整 app/tests 检查替代该 hook。
- [x] PR CI 全部通过（后端测试/静态检查/重复代码/CodeQL）；Codex、Claude 自动评审均
APPROVE，无需要修复的问题。Claude 对既有身份冲突重试和注释的非缺陷观察已复核：保留身份恢复机制，不恢复任何优惠资格判断。
- [ ] Eric 在部署后分别用新账号、有充值/用券历史的账号发起全新 Checkout，确认入口始终显示；核对 Stripe
接受可用券、拒绝受限券，以及全额/部分抵扣到账。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `b226e79e077ee05eb547e43f11a53b62488022c7`
- PR: #4001
- 作者：ericma-srp
- 日期：2026-10-02T08:50:31Z

### Commit Message

```
fix(billing): 由 Stripe 统一判断优惠码使用资格 (#4001)

## Summary

ZooWork 和 Platform
的充值结账始终提供优惠码输入入口，不再由本地判断用户是否首次充值、是否充值过或是否使用过优惠券。优惠码的首单限制、适用产品、核销次数和有效期全部由
Stripe 决定。ZooWork 订阅结账也保持这一规则。

- Platform 删除历史充值查询、首次优惠资格占用/消耗/释放，以及为了复用资格而关闭旧 Checkout 的逻辑。新 Checkout
复用稳定的 Stripe Customer，并始终启用优惠码输入。
- Stripe 已确认的优惠支付不再依赖本地首次订单标记才能到账。保留订单/Customer
归属、产品和金额验证、退款处理、审计及防重复到账机制。
- ZooWork 订阅与 Top up 原本已无条件开放输入入口，本次增加新老客户与两种 Checkout 模式的回归覆盖。

## Root cause

PR #3967 的 Platform 实现把优惠码入口绑定到本地“首次充值资格”：历史
Checkout（包括未付款的尝试）、已记录的首次订单和待完成的优惠资格占用，都会关闭入口或阻止再次充值。这与产品要求不符。

本次明确取消这一层业务判断；数据库中的旧资格字段仅保留用于兼容读取和审计，不参与优惠资格判断。删除不再使用的历史查询，并同步维护隔离的
staging CSFLE 检查脚本。

## Compatibility and release

- 已经发给 Stripe 的请求参数、幂等键和已生成的付款链接保持不变，避免重试时参数冲突。**上线后从 Add funds
发起一笔新的充值来验收；旧链接不会自动增加输入入口。**
- 充值金额范围、订单面额、抵扣金额与到账额度算法、Stripe 后台的券配置均不变；不新增生产数据库查询形式或数据迁移。
- 仅后端需要部署；此 PR 不执行部署或真实支付。
- 按产品负责人 Eric 已确认的验收分工，staging/线上真实优惠券资格和到账验收、加密数据库 fixture 读取/CAS 验收由
Eric 执行。代码评审工具负责代码正确性，不以代替上述环境验收为要求。此次本地测试不宣称完成真实 Stripe 或 staging CSFLE
验收。
- 需求及验收细则：`docs/superpowers/specs/2026-10-02-stripe-promotion-entry.md`。

## Test plan

- [x] 247 项定向回归：Platform 充值/Customer/重试/结算、CSFLE probe 安全逻辑、ZooWork
Checkout 与 Stripe SDK 重试（最终同一次运行：247 passed）。
- [x] `bash scripts/verify-py.sh`：ruff、格式、pyright（app/tests）、8 项 import
contracts 全通过。
- [x] 函数复杂度及其余 pre-commit 检查通过；dead-code 检查未发现本次改动遗留的死函数。原有 pyright hook
未给含空格的路径加引号，已用上述完整 app/tests 检查替代该 hook。
- [x] PR CI 全部通过（后端测试/静态检查/重复代码/CodeQL）；Codex、Claude 自动评审均
APPROVE，无需要修复的问题。Claude 对既有身份冲突重试和注释的非缺陷观察已复核：保留身份恢复机制，不恢复任何优惠资格判断。
- [ ] Eric 在部署后分别用新账号、有充值/用券历史的账号发起全新 Checkout，确认入口始终显示；核对 Stripe
接受可用券、拒绝受限券，以及全额/部分抵扣到账。
```

来源：SerendipityOneInc/ecap-workspace @ b226e79e，PR #4001，作者 ericma-srp。
