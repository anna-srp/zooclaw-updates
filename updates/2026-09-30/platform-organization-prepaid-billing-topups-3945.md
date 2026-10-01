---
title: "开发者平台组织充值上线：Billing 页显示真实余额、Add funds 与付款记录，USD 1 = 200 credits"
type: "Feature"
priority: "高"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 开发者平台组织充值上线：Billing 页显示真实余额、Add funds 与付款记录，USD 1 = 200 credits

## 核心宣传点

开发者平台的组织充值、可用余额和付款记录这次全部接通。Billing 页和侧边栏展示真实余额（含未结算用量）、Add funds 入口、付款记录，以及可重试的错误提示。首次点 Add funds 会幂等地初始化组织账单，再创建 Stripe 一次性结账；订单保存客户与钱包快照，沿用既有的支付校验、幂等履约和恢复流程。组织下所有 Project 和 Key 共用同一个钱包，充值和用量查询走同一个计费客户。平台这边只有充值后按量消费，没有商业订阅、没有月度赠送、没有免费额度，钱包永久有效，USD 1 = 200 credits。内部复用 Work 已有的计量周期配置，固定费为 0 美元，初始化前会校验固定费为零且币种为美元。实测用 Stripe 测试模式付了一笔 5 美元，订单成功履约、同一组织钱包只入账一次 1000 credits、可用余额 5 美元，两个支付回调没有重复入账。

## 分级

- 内部：P0
- 外部：A
- toB 相关：是
- 发布状态：已随正式 release 上线

## PR 说明

## Summary

本 PR 接通 Platform **Org 充值、可用余额和付款记录**。付款方复用 ZooWork Work business 的
team/customer 映射，`billing_team_id == Lago customer_id`；Owner UID
用于认证和审计。Org 下所有 Project/Key 共用钱包，充值和 Usage 查询使用同一个 customer。

- 首次 Add funds 幂等初始化 Org billing，再创建 Stripe one-time Checkout。订单保存
customer/wallet 快照，沿用既有支付校验、幂等履约和恢复流程；页面 GET 只读取状态。
- 复用现有 Gateway 的 bootstrap、business team/key
binding、wallet、ledger、credits/check 和 Usage API。校验 canonical Key 的
business customer/team；已有 Work Billing Profile 时拒绝改写 Key。**Gateway 和
Lago 没有代码改动。**
- Billing 页和 sidebar 展示真实余额、Add funds、付款记录和可重试错误；余额包含未结算用量。Platform Key
Usage 限制为同一 Org customer 下的当前 Key，保留 Work `zct_` 路径。

## Existing plan reuse

直接复用 Work business 已使用的
`BG_PLAN_STARTER_20_MONTH`（`starter_20_month`），无需传入或新增 plan 配置变量。已只读确认
production 存在此 plan，**固定费为 0 USD**。它仅提供 Lago 内部计量周期，名字中的 20 不代表 Platform
收取 $20 月费。

Platform 只有充值后按量消费，没有商业订阅、月度赠送或免费额度。钱包永久有效，USD 1 = 200 credits；初始化前校验
plan 固定费为零且币种为 USD。

## Validation

- 本地用户完成一笔 Stripe **test mode** $5 付款后，只读核对：订单 succeeded/fulfilled，同一
Org customer/wallet 仅入账一次 1,000 credits，可用余额 $5；两个付款 webhook 没有重复入账。
- `ecap-verify-py-ci`：13,196 passed、5 skipped，coverage
89.90%；依赖解析、静态检查、全部 CI lint、两个 jscpd 均通过。Platform Node 24
lint/typecheck/test（27 passed）/build 通过。
- **P1 要求的真实 staging CSFLE 验证已完成**：team/account CAS 的
null/缺失字段、owner/status 拒绝、重复 team/customer 的实际唯一索引冲突、UID Org 共存均通过。没有
bypass 加密；测试 fixture
已删除，持久审计保留。[验证记录](docs/staging-validation/2026-09-30-platform-billing-csfle-and-clerk-cleanup.md)。
- 验证发现旧 Clerk 唯一索引会使第二个 UID Org 插入失败。用户随后明确授权清理；已备份并审计删除 staging 的 5
user、5 Org、2 关联 Project 和两个 Clerk 唯一索引，建立 UID 约束。3 个历史充值订单、7
个支付事件及外部账户/流水保留，历史履约继续使用订单快照。

## Boundaries

- #3939 已合并，base 为 main；同步使用 merge，没有 rebase/reset/force push。
- `PLATFORM_BILLING_ENABLED` 默认 false。未部署，未修改 production；CSFLE 验证覆盖
repository 操作，不等于部署后 HTTP 或消费闭环验收。
- Agent 可更新内部凭据、Engine 的 Platform 身份接入和 LLM/Sandbox/tool 事件的 Project/Key
归因仍需后续 PR。Engine runtime 继续返回 `platform.engine_access_not_ready`，申请 Key
不代表 SDK 已可运行。
- 当前代码/依赖已无 Clerk 实现，测试 fixture 已改为 UID。staging Vault 的 3 个废弃
`PLATFORM_CLERK_*` 字段已通过 CAS 删除，其余 126 个字段读回完全一致，VSO 已自动同步。没有手工 patch
Secret；既有 Pod 的进程环境刷新留待授权 rollout。

## Review follow-up

- 已修复付款记录依赖余额成功的问题（`f23a51846`）：独立查询与渲染 Org 付款记录；余额失败时仍可查看支付/到账状态，Add
funds 保持禁用。管理员权限和后端 Billing 开关继续生效。回归测试先在旧实现失败，再在修复后通过；Node 24
lint/typecheck/test（27 passed）/build 通过。
- 按维护者明确决定，本 PR 暂不修复 plan 列表分页问题，Gateway 不改。当前仍通过 `/lago/plans` 返回的第一页查找
`starter_20_month`；若目标 plan 不在第一页，可能误判不可用并影响初始化、余额与充值。此项保留为已知限制，未声明当前
production 已触发。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `8e70546a594751d0aedcf973ad804a4069250128`
- PR: #3945
- 作者：finn-srp
- 日期：2026-09-30T08:53:10Z

### Commit Message

```
feat(platform): connect organization prepaid billing and top-ups (#3945)

## Summary

本 PR 接通 Platform **Org 充值、可用余额和付款记录**。付款方复用 ZooWork Work business 的
team/customer 映射，`billing_team_id == Lago customer_id`；Owner UID
用于认证和审计。Org 下所有 Project/Key 共用钱包，充值和 Usage 查询使用同一个 customer。

- 首次 Add funds 幂等初始化 Org billing，再创建 Stripe one-time Checkout。订单保存
customer/wallet 快照，沿用既有支付校验、幂等履约和恢复流程；页面 GET 只读取状态。
- 复用现有 Gateway 的 bootstrap、business team/key
binding、wallet、ledger、credits/check 和 Usage API。校验 canonical Key 的
business customer/team；已有 Work Billing Profile 时拒绝改写 Key。**Gateway 和
Lago 没有代码改动。**
- Billing 页和 sidebar 展示真实余额、Add funds、付款记录和可重试错误；余额包含未结算用量。Platform Key
Usage 限制为同一 Org customer 下的当前 Key，保留 Work `zct_` 路径。

## Existing plan reuse

直接复用 Work business 已使用的
`BG_PLAN_STARTER_20_MONTH`（`starter_20_month`），无需传入或新增 plan 配置变量。已只读确认
production 存在此 plan，**固定费为 0 USD**。它仅提供 Lago 内部计量周期，名字中的 20 不代表 Platform
收取 $20 月费。

Platform 只有充值后按量消费，没有商业订阅、月度赠送或免费额度。钱包永久有效，USD 1 = 200 credits；初始化前校验
plan 固定费为零且币种为 USD。

## Validation

- 本地用户完成一笔 Stripe **test mode** $5 付款后，只读核对：订单 succeeded/fulfilled，同一
Org customer/wallet 仅入账一次 1,000 credits，可用余额 $5；两个付款 webhook 没有重复入账。
- `ecap-verify-py-ci`：13,196 passed、5 skipped，coverage
89.90%；依赖解析、静态检查、全部 CI lint、两个 jscpd 均通过。Platform Node 24
lint/typecheck/test（27 passed）/build 通过。
- **P1 要求的真实 staging CSFLE 验证已完成**：team/account CAS 的
null/缺失字段、owner/status 拒绝、重复 team/customer 的实际唯一索引冲突、UID Org 共存均通过。没有
bypass 加密；测试 fixture
已删除，持久审计保留。[验证记录](docs/staging-validation/2026-09-30-platform-billing-csfle-and-clerk-cleanup.md)。
- 验证发现旧 Clerk 唯一索引会使第二个 UID Org 插入失败。用户随后明确授权清理；已备份并审计删除 staging 的 5
user、5 Org、2 关联 Project 和两个 Clerk 唯一索引，建立 UID 约束。3 个历史充值订单、7
个支付事件及外部账户/流水保留，历史履约继续使用订单快照。

## Boundaries

- #3939 已合并，base 为 main；同步使用 merge，没有 rebase/reset/force push。
- `PLATFORM_BILLING_ENABLED` 默认 false。未部署，未修改 production；CSFLE 验证覆盖
repository 操作，不等于部署后 HTTP 或消费闭环验收。
- Agent 可更新内部凭据、Engine 的 Platform 身份接入和 LLM/Sandbox/tool 事件的 Project/Key
归因仍需后续 PR。Engine runtime 继续返回 `platform.engine_access_not_ready`，申请 Key
不代表 SDK 已可运行。
- 当前代码/依赖已无 Clerk 实现，测试 fixture 已改为 UID。staging Vault 的 3 个废弃
`PLATFORM_CLERK_*` 字段已通过 CAS 删除，其余 126 个字段读回完全一致，VSO 已自动同步。没有手工 patch
Secret；既有 Pod 的进程环境刷新留待授权 rollout。

## Review follow-up

- 已修复付款记录依赖余额成功的问题（`f23a51846`）：独立查询与渲染 Org 付款记录；余额失败时仍可查看支付/到账状态，Add
funds 保持禁用。管理员权限和后端 Billing 开关继续生效。回归测试先在旧实现失败，再在修复后通过；Node 24
lint/typecheck/test（27 passed）/build 通过。
- 按维护者明确决定，本 PR 暂不修复 plan 列表分页问题，Gateway 不改。当前仍通过 `/lago/plans` 返回的第一页查找
`starter_20_month`；若目标 plan 不在第一页，可能误判不可用并影响初始化、余额与充值。此项保留为已知限制，未声明当前
production 已触发。
```

来源：SerendipityOneInc/ecap-workspace @ 8e70546a，PR #3945，作者 finn-srp。
