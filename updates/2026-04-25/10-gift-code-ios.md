---
title: "iOS 新增礼品码兑换入口"
type: "新功能上线"
priority: "中"
date: "2026-04-25"
status: "待审核"
channels: "Discord + changelog"
---

# iOS 新增礼品码兑换入口

## 核心宣传点

iOS 用户现在可以直接在 App 内兑换礼品码，享受赠送的会员或积分。

## 原始内容

Commit: 36849b60610b53b3a515bd81ea8c30512a9b1d20

Message:
feat(ios): Add gift code redemption flow (#1283)

## Summary

Add a complete gift code redemption feature to the iOS app, allowing
users to enter and redeem gift codes for bonus credits or subscription
activations.

- **GiftCodeService** — new actor-based service calling `POST
/api/gift-code/redeem` with proper error mapping for all backend error
codes (`invalid_code`, `already_participated`, `code_exhausted`,
`no_subscription`, `plan_downgrade_not_allowed`)
- **RedeemResult** — enum supporting both `.credits(Int)` and
`.subscription(planTier:durationDays:)` responses, forward-compatible
with the unified redeem endpoint from #1270
- **RedeemGiftCodeView** — modal UI with centered text input,
slide-from-bottom animation, loading state, error display, and success
auto-dismiss
- **RedeemSuccessToast** — toast notification with category-aware
messaging (credits vs subscription)
- **Sidebar integration** — redeem button added to sidebar drawer with
gift icon asset
- **NetworkError enhancement** — `httpError` case now carries response
body `Data` so callers can parse structured error responses
- **28 unit tests** — GiftCodeServiceTests (11), RedeemStateTests (3),
RedeemDisabledTests (7), AppShellRedeemWiringTests (3),
RedeemOverlayContractTests (6)

### Version bump: 1.4.0 → 1.5.0 (build 1)

Build number reset from 7 to 1 is intentional. App Store Connect tracks
`CURRENT_PROJECT_VERSION` per `MARKETING_VERSION` — build 1 of 1.5.0
does not conflict with build 7 of 1.4.0. Ref: [Apple
TN3104](https://developer.apple.com/documentation/technotes/tn3104-xcode-build-numbers)

## Test plan

- [ ] Open sidebar, tap "Redeem Gift Code" button
- [ ] Verify modal slides up from bottom with spring animation
- [ ] Enter a valid credit gift code → verify success toast and credits
refresh
- [ ] Enter a valid subscription code → verify subscription activation
toast
- [ ] Enter an invalid code → verify "invalid code" error message
- [ ] Enter an already-used code → verify "already participated" error
- [ ] Enter an exhausted/expired code → verify "redemption limit" error
- [ ] Redeem with a plan higher than the code → verify "plan downgrade"
error
- [ ] Tap backdrop to dismiss modal
- [ ] Verify text input is centered in the code field

🤖 Generated with [Claude Code](https://claude.com/claude-code)

PR Description:
## Summary

Add a complete gift code redemption feature to the iOS app, allowing users to enter and redeem gift codes for bonus credits or subscription activations.

- **GiftCodeService** — new actor-based service calling `POST /api/gift-code/redeem` with proper error mapping for all backend error codes (`invalid_code`, `already_participated`, `code_exhausted`, `no_subscription`, `plan_downgrade_not_allowed`)
- **RedeemResult** — enum supporting both `.credits(Int)` and `.subscription(planTier:durationDays:)` responses, forward-compatible with the unified redeem endpoint from #1270
- **RedeemGiftCodeView** — modal UI with centered text input, slide-from-bottom animation, loading state, error display, and success auto-dismiss
- **RedeemSuccessToast** — toast notification with category-aware messaging (credits vs subscription)
- **Sidebar integration** — redeem button added to sidebar drawer with gift icon asset
- **NetworkError enhancement** — `httpError` case now carries response body `Data` so callers can parse structured error responses
- **28 unit tests** — GiftCodeServiceTests (11), RedeemStateTests (3), RedeemDisabledTests (7), AppShellRedeemWiringTests (3), RedeemOverlayContractTests (6)

### Version bump: 1.4.0 → 1.5.0 (build 1)

Build number reset from 7 to 1 is intentional. App Store Connect tracks `CURRENT_PROJECT_VERSION` per `MARKETING_VERSION` — build 1 of 1.5.0 does not conflict with build 7 of 1.4.0. Ref: [Apple TN3104](https://developer.apple.com/documentation/technotes/tn3104-xcode-build-numbers)

## Test plan

- [ ] Open sidebar, tap "Redeem Gift Code" button
- [ ] Verify modal slides up from bottom with spring animation
- [ ] Enter a valid credit gift code → verify success toast and credits refresh
- [ ] Enter a valid subscription code → verify subscription activation toast
- [ ] Enter an invalid code → verify "invalid code" error message
- [ ] Enter an already-used code → verify "already participated" error
- [ ] Enter an exhausted/expired code → verify "redemption limit" error
- [ ] Redeem with a plan higher than the code → verify "plan downgrade" error
- [ ] Tap backdrop to dismiss modal
- [ ] Verify text input is centered in the code field

🤖 Generated with [Claude Code](https://claude.com/claude-code)
