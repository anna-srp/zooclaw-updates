---
title: "feat(billing): integrate subscription and credit top-up redesign (#3811)"
type: "新功能"
priority: "高"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# 订阅与积分充值改版：Stripe 月订阅 + $1 = 200 积分独立充值

## 核心宣传点

订阅和积分购买整体改版上线：Pro 按月 Stripe 订阅，积分可以独立购买（$1 = 200 积分，且为永久积分，不随账期清零），老订阅会迁移到新体系。Pro/Enterprise 定价页、Manage plan 面板、积分购买入口和 onboarding 展示全部换成新版；Stripe 充值发票可以直接下载。Team 用户保留 Manage 入口，但隐藏个人充值与取消操作、禁用个人订阅，Contact Sales 直接跳企业页。同时补齐了支付/积分的诊断能力，钱包变更和余额查询沿用原有链路，未完成的 Stripe Checkout 会话也能恢复。

## 分级

- 内部：P0
- 外部：S
- 发布状态：已合并待发版

## PR 说明

## Summary
- Integrate the subscription and credit top-up redesign across claw-interface and the web app: Stripe monthly subscriptions, independent credit purchases at $1 = 200 credits, legacy subscription migration, and permanent top-up credits through the existing gateway flow.
- Consolidate the Pro/Enterprise pricing, Manage plan, credit purchase, onboarding presentation, and Stripe top-up invoice download changes from the shared branch.
- Preserve Manage for Team users while hiding personal top-up/cancellation actions and disabling personal subscriptions. Contact Sales opens `/en/enterprise`.
- Add payment/credit diagnostics and retain existing wallet mutation and balance-query flows.

- Define catalog/checkout response schemas, complete pricing comparison translations, and align permanent-credit documentation and advertised Pro storage.

- Recover the original pending Stripe Checkout from the catalog, keep top-ups available when legacy subscription verification fails, and audit uncertain Checkout requests through the existing manual-review flow.

## Test plan
- [x] Onboarding recovery at e45c41a4d: 40 related frontend tests passed, including failed-response/navigation recovery through the real onboarding hook, reopening onboarding, and rejecting unrelated purchase restrictions. Type/lint/governance checks passed.
- [x] Checkout recovery fixes at cb0f75074: 209 backend tests and 25 frontend tests passed, including lost responses, popup failures, 48-hour unknown outcomes, legacy Stripe lookup failures, and concurrent paid-state protection. Type/lint/governance/import checks passed.
- [x] Review fixes at b5b5b83cc: 25 frontend tests and 6 backend response-contract tests passed; frontend type/lint/governance and backend ruff/pyright/import checks passed.
- [x] Earlier: 26 SharedPlanCard unit tests passed, including Team Manage access without top-up actions.
- [x] Pre-push frontend type/lint/governance checks and backend ruff, pyright, and import checks passed for commit 63c4ddffc.
- [x] Frontend staging release `ecap-v0.19.22-beta` succeeded; version endpoint matched 63c4ddffc and homepage returned HTTP 200 on September 18.
- [x] Backend staging release `service-v0.18.11-beta.10` succeeded on September 18.
- [ ] Review current PR CI results against the latest main. The checks above do not constitute a complete end-to-end billing acceptance run.





## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `6f12bdb4aaf461ddd44cc52540f84a78ae15808c`
- PR: #3811
- 作者：sam-srp
- 日期：2026-09-20T13:36:45Z

### Commit Message

```
feat(billing): integrate subscription and credit top-up redesign (#3811)

## Summary
- Integrate the subscription and credit top-up redesign across
claw-interface and the web app: Stripe monthly subscriptions,
independent credit purchases at $1 = 200 credits, legacy subscription
migration, and permanent top-up credits through the existing gateway
flow.
- Consolidate the Pro/Enterprise pricing, Manage plan, credit purchase,
onboarding presentation, and Stripe top-up invoice download changes from
the shared branch.
- Preserve Manage for Team users while hiding personal
top-up/cancellation actions and disabling personal subscriptions.
Contact Sales opens `/en/enterprise`.
- Add payment/credit diagnostics and retain existing wallet mutation and
balance-query flows.

- Define catalog/checkout response schemas, complete pricing comparison
translations, and align permanent-credit documentation and advertised
Pro storage.

- Recover the original pending Stripe Checkout from the catalog, keep
top-ups available when legacy subscription verification fails, and audit
uncertain Checkout requests through the existing manual-review flow.

## Test plan
- [x] Onboarding recovery at e45c41a4d: 40 related frontend tests
passed, including failed-response/navigation recovery through the real
onboarding hook, reopening onboarding, and rejecting unrelated purchase
restrictions. Type/lint/governance checks passed.
- [x] Checkout recovery fixes at cb0f75074: 209 backend tests and 25
frontend tests passed, including lost responses, popup failures, 48-hour
unknown outcomes, legacy Stripe lookup failures, and concurrent
paid-state protection. Type/lint/governance/import checks passed.
- [x] Review fixes at b5b5b83cc: 25 frontend tests and 6 backend
response-contract tests passed; frontend type/lint/governance and
backend ruff/pyright/import checks passed.
- [x] Earlier: 26 SharedPlanCard unit tests passed, including Team
Manage access without top-up actions.
- [x] Pre-push frontend type/lint/governance checks and backend ruff,
pyright, and import checks passed for commit 63c4ddffc.
- [x] Frontend staging release `ecap-v0.19.22-beta` succeeded; version
endpoint matched 63c4ddffc and homepage returned HTTP 200 on September
18.
- [x] Backend staging release `service-v0.18.11-beta.10` succeeded on
September 18.
- [ ] Review current PR CI results against the latest main. The checks
above do not constitute a complete end-to-end billing acceptance run.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
Co-authored-by: tim-srp <tim@srp.one>
Co-authored-by: shana-srp <shana@srp.one>
Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

来源：SerendipityOneInc/ecap-workspace @ 6f12bdb4，PR #3811，作者 sam-srp。