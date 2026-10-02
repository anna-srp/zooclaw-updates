---
title: "开发者平台上线 API Credit Terms 条款页，充值、登录与个人设置都能打开"
type: "新功能"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: "Discord+changelog"
---

# 开发者平台上线 API Credit Terms 条款页，充值、登录与个人设置都能打开

## 核心宣传点

开发者平台用户现在可以从 Add funds 弹窗、登录页和 Profile 设置三个位置打开 API Credit Terms。新增的公开 /terms 页面完整呈现了条款文档里全部 13 个非空段落，充值前想确认条款不用再去别处找。

## 分级

- 内部：P2
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary
Platform users can now open the supplied API Credit Terms from the Add funds dialog, the sign-in page, and Profile settings. The new public `/terms` page renders all 13 non-empty paragraphs of `Zoowork Credit Terms.docx` verbatim, including its original title and update date.

- Add `API Credit Terms` and the explicit purchase-assent sentence to the payment dialog's bottom explanatory text; use `Buy Credits — $X` for the purchase action to match the supplied wording. Billing, the sidebar Add funds link, and the zero-balance reminder share this dialog.
- Replace the sign-in page's general ZooWork Terms link with the supplied Platform agreement, labeled `Zoowork API Credit Terms` to match the document's original title, and add a small `Terms` link beneath Profile appearance settings.
- Open terms in a separate tab so users retain the original form and selected payment amount. All three entries lead to the same supplied document.

## Test plan
- [x] Platform lint, TypeScript checks, and production build.
- [x] Existing Platform test suite: 127 tests across 17 files passed.
- [x] Exact paragraph comparison between Word, stored content, and rendered page: all 13 paragraphs match.
- [x] Browser verification of login and Profile links, Billing button, sidebar Add funds, and zero-balance reminder; terms readable while signed out.
- [x] Local UI preview reviewed by the requester. Preview uses sample accounts; no real checkout or payment was performed.

## Product-owner clarification for review
`zoowork.ai` and `platform.zoowork.ai` are distinct products with different user agreements. The requester explicitly confirms that this PR replaces the user agreement for **platform.zoowork.ai** with the supplied new Word document. It is not intended to retain the old `zoowork.ai/about/terms` agreement as Platform's sign-in terms. All three Platform entry points must use the supplied document, whose text and title must remain verbatim.

The product owner additionally confirms that the current non-expiring credit behavior is allowed for this release. The supplied one-year expiration clause stays verbatim; implementing per-purchase expiry is deferred to a later feature and is outside this PR. This is an explicitly accepted rollout limitation, not a claim that expiration is implemented, tested, or legally validated. Both decisions are recorded in `web/platform/PRODUCT.md`.

Auto Merge is disabled while the reviewers reassess and remaining findings are resolved. Do not merge solely because CI is green.

## Review disposition (in progress)
- Platform agreement replacement: confirmed by the product owner and recorded in `web/platform/PRODUCT.md`. Codex explicitly withdrew its earlier P1 on restoring the other product's agreement.
- Purchase action / assent mismatch: fixed in `3e2e2cb0a`; the button now says `Buy Credits — $X`, and the bottom notice repeats the supplied assent wording next to the Terms link. The Word content remains byte-for-byte unchanged.
- Sign-in label / document-title mismatch: the sign-in link now uses the exact original title, `Zoowork API Credit Terms`, while continuing to point to the owner-designated Platform agreement at `/terms`.
- Latest Claude and Codex reviews confirm the sign-in label fix; Claude also confirms the public-route and entry-point coverage gap is closed. The optional dialog-title naming observation is left unchanged: `Add funds` describes the wallet operation while `Buy Credits` is the purchase action explicitly named by the supplied agreement.
- Validation: the production build and browser verification passed on the UI revision. The latest 42 focused router/login tests pass, including a signed-out agreement route check and assertions on the sign-in, Profile, and purchase-consent links. The initial implementation's full 127-test suite also passed. No real payment was submitted.
- One-year credit expiration: accepted by the product owner for this release, with backend enforcement explicitly deferred. Preserve the supplied text and current fulfillment behavior. The earlier comments that called the scope decision pending are superseded by [the recorded owner decision](https://github.com/SerendipityOneInc/ecap-workspace/pull/3988#issuecomment-5933034441). Review any other independently supported defects normally.
- The comment-triggered Claude assistant failed during AWS OIDC role assumption. The normal Claude/Codex automatic review workflow is being used for the new revision instead.

- Incorporated-policy destinations: also unresolved after the latest Codex review. The supplied DOCX has no hyperlinks, and Platform has no separate Terms and Conditions / Refund and Cancellation Policy routes. The owner has been asked whether the referenced main-site policies also apply or to provide Platform-specific content/URLs. Do not infer policy applicability from a shared brand.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `85a33e6829ab704993e172d53d636ccbeba79e28`
- PR: #3988
- 作者：ericma-srp
- 日期：2026-10-01T15:54:09Z

### Commit Message

```
feat(platform): add Terms page and entry points (#3988)

## Summary
Platform users can now open the supplied API Credit Terms from the Add
funds dialog, the sign-in page, and Profile settings. The new public
`/terms` page renders all 13 non-empty paragraphs of `Zoowork Credit
Terms.docx` verbatim, including its original title and update date.

- Add `API Credit Terms` and the explicit purchase-assent sentence to
the payment dialog's bottom explanatory text; use `Buy Credits — $X` for
the purchase action to match the supplied wording. Billing, the sidebar
Add funds link, and the zero-balance reminder share this dialog.
- Replace the sign-in page's general ZooWork Terms link with the
supplied Platform agreement, labeled `Zoowork API Credit Terms` to match
the document's original title, and add a small `Terms` link beneath
Profile appearance settings.
- Open terms in a separate tab so users retain the original form and
selected payment amount. All three entries lead to the same supplied
document.

## Test plan
- [x] Platform lint, TypeScript checks, and production build.
- [x] Existing Platform test suite: 127 tests across 17 files passed.
- [x] Exact paragraph comparison between Word, stored content, and
rendered page: all 13 paragraphs match.
- [x] Browser verification of login and Profile links, Billing button,
sidebar Add funds, and zero-balance reminder; terms readable while
signed out.
- [x] Local UI preview reviewed by the requester. Preview uses sample
accounts; no real checkout or payment was performed.

## Product-owner clarification for review
`zoowork.ai` and `platform.zoowork.ai` are distinct products with
different user agreements. The requester explicitly confirms that this
PR replaces the user agreement for **platform.zoowork.ai** with the
supplied new Word document. It is not intended to retain the old
`zoowork.ai/about/terms` agreement as Platform's sign-in terms. All
three Platform entry points must use the supplied document, whose text
and title must remain verbatim.

The product owner additionally confirms that the current non-expiring
credit behavior is allowed for this release. The supplied one-year
expiration clause stays verbatim; implementing per-purchase expiry is
deferred to a later feature and is outside this PR. This is an
explicitly accepted rollout limitation, not a claim that expiration is
implemented, tested, or legally validated. Both decisions are recorded
in `web/platform/PRODUCT.md`.

Auto Merge is disabled while the reviewers reassess and remaining
findings are resolved. Do not merge solely because CI is green.

## Review disposition (in progress)
- Platform agreement replacement: confirmed by the product owner and
recorded in `web/platform/PRODUCT.md`. Codex explicitly withdrew its
earlier P1 on restoring the other product's agreement.
- Purchase action / assent mismatch: fixed in `3e2e2cb0a`; the button
now says `Buy Credits — $X`, and the bottom notice repeats the supplied
assent wording next to the Terms link. The Word content remains
byte-for-byte unchanged.
- Sign-in label / document-title mismatch: the sign-in link now uses the
exact original title, `Zoowork API Credit Terms`, while continuing to
point to the owner-designated Platform agreement at `/terms`.
- Latest Claude and Codex reviews confirm the sign-in label fix; Claude
also confirms the public-route and entry-point coverage gap is closed.
The optional dialog-title naming observation is left unchanged: `Add
funds` describes the wallet operation while `Buy Credits` is the
purchase action explicitly named by the supplied agreement.
- Validation: the production build and browser verification passed on
the UI revision. The latest 42 focused router/login tests pass,
including a signed-out agreement route check and assertions on the
sign-in, Profile, and purchase-consent links. The initial
implementation's full 127-test suite also passed. No real payment was
submitted.
- One-year credit expiration: accepted by the product owner for this
release, with backend enforcement explicitly deferred. Preserve the
supplied text and current fulfillment behavior. The earlier comments
that called the scope decision pending are superseded by [the recorded
owner
decision](https://github.com/SerendipityOneInc/ecap-workspace/pull/3988#issuecomment-5933034441).
Review any other independently supported defects normally.
- The comment-triggered Claude assistant failed during AWS OIDC role
assumption. The normal Claude/Codex automatic review workflow is being
used for the new revision instead.

- Incorporated-policy destinations: also unresolved after the latest
Codex review. The supplied DOCX has no hyperlinks, and Platform has no
separate Terms and Conditions / Refund and Cancellation Policy routes.
The owner has been asked whether the referenced main-site policies also
apply or to provide Platform-specific content/URLs. Do not infer policy
applicability from a shared brand.
```

来源：SerendipityOneInc/ecap-workspace @ 85a33e68，PR #3988，作者 ericma-srp。
