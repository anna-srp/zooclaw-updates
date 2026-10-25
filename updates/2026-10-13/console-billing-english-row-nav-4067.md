---
title: "体验优化：员工 Console 计费页统一英文文案，整行可点进详情并新增 ID 复制按钮"
type: "体验优化"
priority: "中"
date: "2026-10-13"
status: "待审核"
channels: ""
---

# 体验优化：员工 Console 计费页统一英文文案，整行可点进详情并新增 ID 复制按钮

## 核心宣传点

员工 Console 的 Platform Billing 页此前混进了中文文案，与整体英文后台不一致。本次把导航、组织搜索、余额、充值确认、历史记录、校验与本地错误提示全部统一为英文。交互上，点击组织行的非交互区域即可进入详情，组织名原生链接保留，进出详情时搜索条件与分页状态都会保留。由于整行可点导致双击选中 ID 变得不可靠，这次在 Org ID 和 Owner UID 旁新增了独立的复制按钮，点击不会触发跳转，成功后显示对勾并向屏幕阅读器播报结果，剪贴板失败后可以重试。仅员工后台可见，不影响客户侧界面，纯前端改动无需后端配套发版。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `716772edf30cb732ab3c553a4e498f1b0f0276ac`
- PR: #4067
- 作者：finn-srp
- 日期：2026-10-13T07:58:06Z

### Commit Message

```
fix(console): unify billing language and row navigation (#4067)

## Summary
- Use English throughout Console Platform Billing: navigation,
organization search, balance, top-up confirmation, history, validation
and local error messages.
- Open details from non-interactive areas of an organization row. Retain
the native organization-name link and preserve search/pagination when
entering and leaving details.
- Add copy buttons beside Org ID and Owner UID that do not navigate.
Show a success checkmark, announce the result to screen readers, and
allow retry after clipboard failure.

## Root cause
The billing UI introduced Chinese copy into the English staff Console
and a separate detail action. Whole-row navigation subsequently made
double-click ID selection unreliable. Dedicated copy controls preserve
reliable ID copying alongside immediate row navigation.

## Test plan
- [x] Node 24, on the new branch based on current main: Console lint,
typecheck and build.
- [x] Focused billing route and dashboard shell tests: 22 passed,
including both ID copy actions, keyboard activation, failure/retry, row
navigation and search/pagination preservation.
- [x] Previous browser validation of this identical Console
implementation: actual clipboard values, copy without navigation,
desktop/mobile layout, keyboard copy, failure/retry, native link
behavior and row navigation.
- [x] No recharge was submitted by automated checks.

## Related review
Replaces https://github.com/SerendipityOneInc/ecap-workspace/pull/4065
at the author's request with a fresh PR and review request. Includes the
fix for Tim's ID-copy finding from the first submission.

## Review disposition
- CI passed on the new PR; CodeQL reports no open alerts on its merge
ref. Claude and Codex both returned APPROVE verdicts with no blocking
findings.
- Keep the persistent success checkmark: feedback is intentional and
copying remains available. Claude's concern about a selection elsewhere
suppressing row navigation was not reproduced in prior browser checks;
retain the drag-selection guard.
- A fresh review request was sent to `tim-srp` when this PR was created.
Formal reviewer approval is still pending.
```

