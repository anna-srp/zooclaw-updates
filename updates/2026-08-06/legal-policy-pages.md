---
title: "新增退款政策与 DMCA 政策页面"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-06"
status: "待审核"
channels: ""
---

## 核心宣传点

上线独立的退款政策和 DMCA 政策页面，并更新了服务条款的资格与使用规范、隐私政策的子处理方披露，合规信息更透明可查。

## 原始内容

**feat(web): add and update legal policy pages (#3282)**

- sha: `13b2fbe4cdfccea4f6bd4be8ae61786dfb6db22a`
- PR: #3282

```
feat(web): add and update legal policy pages (#3282)

## Linear

N/A

## Summary

- add standalone Refund and DMCA policy pages using the existing Terms
page visual treatment
- update Terms eligibility and acceptable-use language, and disclose
Privacy Policy subprocessors
- keep the new legal routes locale-free without adding Landing, Header,
Footer, or settings entry points

## Risk and follow-up

- Product-owner decision: the `NEED_HUMAN_REVIEW` finding about the
Airwallex disclosure is accepted as controlled risk for this PR.
- This release ships the approved legal terms only. It does not change
payment, billing, subscription, cancellation, or refund execution logic.
- Payment-provider and business-logic alignment will be handled as a
separate follow-up after the legal terms are published and does not
block this legal-page rollout.

## Test plan

- [x] `bash scripts/verify-web.sh --test-only
tests/unit/app/legal-policy-pages.unit.spec.tsx
tests/unit/middleware/middleware.unit.spec.ts`
- [x] `bash scripts/verify-web.sh --no-test <changed paths>`
- [x] `bash scripts/verify-changed.sh`
- [x] locally rendered Refund, DMCA, Terms, and Privacy routes returned
HTTP 200 and were approved in preview

Co-authored-by: eric <eric.ma@creatibi.com>
```

**PR Body:**

## Linear

N/A

## Summary

- add standalone Refund and DMCA policy pages using the existing Terms page visual treatment
- update Terms eligibility and acceptable-use language, and disclose Privacy Policy subprocessors
- keep the new legal routes locale-free without adding Landing, Header, Footer, or settings entry points

## Risk and follow-up

- Product-owner decision: the `NEED_HUMAN_REVIEW` finding about the Airwallex disclosure is accepted as controlled risk for this PR.
- This release ships the approved legal terms only. It does not change payment, billing, subscription, cancellation, or refund execution logic.
- Payment-provider and business-logic alignment will be handled as a separate follow-up after the legal terms are published and does not block this legal-page rollout.

## Test plan

- [x] `bash scripts/verify-web.sh --test-only tests/unit/app/legal-policy-pages.unit.spec.tsx tests/unit/middleware/middleware.unit.spec.ts`
- [x] `bash scripts/verify-web.sh --no-test <changed paths>`
- [x] `bash scripts/verify-changed.sh`
- [x] locally rendered Refund, DMCA, Terms, and Privacy routes returned HTTP 200 and were approved in preview

