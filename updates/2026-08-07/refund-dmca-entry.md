---
title: "新增退款政策与 DMCA 入口"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-07"
status: "待审核"
channels: ""
---

## 核心宣传点

官网页脚和订阅面板新增退款政策、DMCA 入口，相关条款查阅更方便，并已完成多语言适配。

## 原始内容

### feat(web): add refund and DMCA policy entry links (#3296)

- SHA: `09d723950398fb053061fc4db5f72e682f010b90`
- 仓库: 见 raw/2026-08-07

**Commit Message:**

```
feat(web): add refund and DMCA policy entry links (#3296)

## Linear

No Linear issue — requested directly for the legal-policy entry rollout.

## Summary

- add Refund Policy and `DCMA` links to the ZooClaw global footer,
between Terms and Gensmo
- localize Refund Policy for all supported footer locales; keep the
visible `DCMA` label identical in every locale per product requirement
- add `Refund Policy` beside Contact Support in the subscription panel
footer, with English and Chinese copy
- point the new entries to the existing `/about/refund` and
`/about/dmca` pages
- add regression coverage for footer order, links, and localized copy

## Risk / review

- Low risk: this PR only exposes existing static legal pages through
navigation links.
- It does not change refund, payment, subscription, or DMCA business
logic, and it does not alter the legal-page contents.
- `NEED_HUMAN_REVIEW` is not required for this scoped navigation update.

## Test plan

- [x] `PATH="/tmp/legal-entry-pnpm10:$PATH" bash scripts/verify-web.sh
--no-test`
- [x] 101 focused Vitest tests across landing content,
SubscriptionPanel, and locale coverage
- [x] local visual verification for Chinese footer and
subscription-panel footer
- [x] `git diff --check`
```

**PR Body:**

## Linear

No Linear issue — requested directly for the legal-policy entry rollout.

## Summary

- add Refund Policy and `DCMA` links to the ZooClaw global footer, between Terms and Gensmo
- localize Refund Policy for all supported footer locales; keep the visible `DCMA` label identical in every locale per product requirement
- add `Refund Policy` beside Contact Support in the subscription panel footer, with English and Chinese copy
- point the new entries to the existing `/about/refund` and `/about/dmca` pages
- add regression coverage for footer order, links, and localized copy

## Risk / review

- Low risk: this PR only exposes existing static legal pages through navigation links.
- It does not change refund, payment, subscription, or DMCA business logic, and it does not alter the legal-page contents.
- `NEED_HUMAN_REVIEW` is not required for this scoped navigation update.

## Test plan

- [x] `PATH="/tmp/legal-entry-pnpm10:$PATH" bash scripts/verify-web.sh --no-test`
- [x] 101 focused Vitest tests across landing content, SubscriptionPanel, and locale coverage
- [x] local visual verification for Chinese footer and subscription-panel footer
- [x] `git diff --check`


