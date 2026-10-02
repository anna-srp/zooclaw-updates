# SerendipityOneInc/ecap-workspace — commits 2026-10-01

## feat(pricing): add Managed Agent API pricing entry (#3994)

- **SHA**: `82dd578cd98730fb24ee141643e7082e515363b4`
- **作者**: ericma-srp
- **日期**: 2026-10-01T20:07:33Z

### Commit Message

```
feat(pricing): add Managed Agent API pricing entry (#3994)

## Summary

- Add a separate “Building with APIs?” callout above the Pro and
Enterprise comparison. “Explore Managed Agent API” uses the shared
Platform host constant and opens billing with `addFunds=1`.
- Signed-out visitors see Platform login first, then email or Google
sign-in continues to billing and opens the existing Add funds dialog.
Preserve the requested path, query and hash in router history state,
including session restoration after a refresh. One shared resolver
restricts return destinations to internal `/settings` routes; ordinary
homepage sign-in still opens API keys. Once explicit sign-out deletes
the session cookie, the auth provider marks the logout and the route
guard clears the previous destination, including a later Firebase
cleanup rejection. A failed cookie deletion stays on the current page;
the login route also clears any existing target before rendering
sign-in, so a refresh cannot resurrect it. The existing cross-tab
revision notification now distinguishes sign-in/sign-out using only an
event type and random revision. Receiving tabs clear old protected URLs
before session recovery; the logout marker resets only when a new
session is verified or published, including rapid account replacement.
Legacy revision consumers remain compatible. Billing permissions and
readiness continue to gate the dialog, and navigation creates no top-up
order.
- Center the pricing hero, use the final audience copy (“Flexible plans
for domain experts and enterprises, with API pricing for FDEs.”),
enlarge the subtitle and API callout text, and keep equal spacing above
and below the callout. Preserve the original subscription cards and
Custom Pricing label; update the comparison heading and Enterprise
tagline.
- Update all 10 supported locales, preserving the supplied FDE
terminology. The marketing web and Platform frontends both need
deployment; no backend or payment-processing changes.

## Product contract

The product owner explicitly requested the final CTA wording **Explore
Managed Agent API** on 2026-10-02 and required translation into all
supported languages. This is the accepted product decision, including
the existing Platform billing/Add funds destination described below. The
product owner also directed follow-up review fixes to address technical
implementation issues while preserving the confirmed product design.

Product-owner instruction: “按钮你从view api pricing，改为 Explore Managed
Agent API 注意翻译成各国语言。”

“Explore Managed Agent API” opens Platform billing with the existing Add
funds amount chooser. Signed-out visitors log in first and continue to
the same destination. Opening the page or chooser does not create a
top-up or Stripe Checkout; only explicit “Buy Credits” confirmation
creates the order. Billing permissions and wallet readiness remain
mandatory.

## Test plan

- [x] Web governance guards, TypeScript and ESLint; Platform TypeScript,
changed-file ESLint and production build.
- [x] Latest CTA copy: all 10 supported locales translated, with 54
marketing entry/locale-completeness tests passing. The full 185-test
Platform suite passed for the authentication changes. Router regressions
reproduce the review findings, then cover email sign-in, Google sign-in,
refreshed-session continuation, ordinary homepage sign-in, explicit
sign-out followed by a different account signing in through either
method, cookie-deletion failure, Firebase cleanup failure after local
logout, reset of the explicit-logout marker on a new login, login-page
target clearing before refresh/re-login, and zero top-up POSTs.
Integrated regressions use the real auth provider and router with mocked
account/session boundaries to cover cross-tab logout, email re-login,
incoming replacement sessions, and replacement before or during
restoration. Notification tests cover event types and unique revisions
without credentials. Destination tests reject external and malformed
return targets. Existing router cases exercise the exact `?addFunds=1`
URL without billing permission and while initialization is pending, and
assert that the chooser remains closed; billing failure also preserves
history without creating Checkout.
- [x] Local browser preview with mock auth/data: email sign-in, Google
sign-in and restored-session continuation all open Add funds on billing
and clear the return state. Account-menu sign-out followed by mock
Google sign-in reaches API keys with no saved target or Add funds
dialog. Production authentication and payment were not exercised.
- [x] Pricing layout checked at 1440×900, 375×667 and 320×568; equal
callout spacing, visible API entry and no horizontal overflow. Sampled
English, Chinese and French layouts. After the CTA rename, all 10
locales were browser-checked at 375×667 with a fully visible API button
and no horizontal/text overflow; English desktop at 1440×900 and
English/German at 320×568 were also checked. Fresh Arabic RTL browser
checks at 1440×900 and 375×667 confirm `lang=ar`, `dir=rtl`, correct CTA
direction, first-screen visibility, and no horizontal/text overflow.

The full marketing web suite and build run in CI.
```

### PR Body

```
## Summary

- Add a separate “Building with APIs?” callout above the Pro and Enterprise comparison. “Explore Managed Agent API” uses the shared Platform host constant and opens billing with `addFunds=1`.
- Signed-out visitors see Platform login first, then email or Google sign-in continues to billing and opens the existing Add funds dialog. Preserve the requested path, query and hash in router history state, including session restoration after a refresh. One shared resolver restricts return destinations to internal `/settings` routes; ordinary homepage sign-in still opens API keys. Once explicit sign-out deletes the session cookie, the auth provider marks the logout and the route guard clears the previous destination, including a later Firebase cleanup rejection. A failed cookie deletion stays on the current page; the login route also clears any existing target before rendering sign-in, so a refresh cannot resurrect it. The existing cross-tab revision notification now distinguishes sign-in/sign-out using only an event type and random revision. Receiving tabs clear old protected URLs before session recovery; the logout marker resets only when a new session is verified or published, including rapid account replacement. Legacy revision consumers remain compatible. Billing permissions and readiness continue to gate the dialog, and navigation creates no top-up order.
- Center the pricing hero, use the final audience copy (“Flexible plans for domain experts and enterprises, with API pricing for FDEs.”), enlarge the subtitle and API callout text, and keep equal spacing above and below the callout. Preserve the original subscription cards and Custom Pricing label; update the comparison heading and Enterprise tagline.
- Update all 10 supported locales, preserving the supplied FDE terminology. The marketing web and Platform frontends both need deployment; no backend or payment-processing changes.

## Product contract

The product owner explicitly requested the final CTA wording **Explore Managed Agent API** on 2026-10-02 and required translation into all supported languages. This is the accepted product decision, including the existing Platform billing/Add funds destination described below. The product owner also directed follow-up review fixes to address technical implementation issues while preserving the confirmed product design.

Product-owner instruction: “按钮你从view api pricing，改为 Explore Managed Agent API 注意翻译成各国语言。”

“Explore Managed Agent API” opens Platform billing with the existing Add funds amount chooser. Signed-out visitors log in first and continue to the same destination. Opening the page or chooser does not create a top-up or Stripe Checkout; only explicit “Buy Credits” confirmation creates the order. Billing permissions and wallet readiness remain mandatory.

## Test plan

- [x] Web governance guards, TypeScript and ESLint; Platform TypeScript, changed-file ESLint and production build.
- [x] Latest CTA copy: all 10 supported locales translated, with 54 marketing entry/locale-completeness tests passing. The full 185-test Platform suite passed for the authentication changes. Router regressions reproduce the review findings, then cover email sign-in, Google sign-in, refreshed-session continuation, ordinary homepage sign-in, explicit sign-out followed by a different account signing in through either method, cookie-deletion failure, Firebase cleanup failure after local logout, reset of the explicit-logout marker on a new login, login-page target clearing before refresh/re-login, and zero top-up POSTs. Integrated regressions use the real auth provider and router with mocked account/session boundaries to cover cross-tab logout, email re-login, incoming replacement sessions, and replacement before or during restoration. Notification tests cover event types and unique revisions without credentials. Destination tests reject external and malformed return targets. Existing router cases exercise the exact `?addFunds=1` URL without billing permission and while initialization is pending, and assert that the chooser remains closed; billing failure also preserves history without creating Checkout.
- [x] Local browser preview with mock auth/data: email sign-in, Google sign-in and restored-session continuation all open Add funds on billing and clear the return state. Account-menu sign-out followed by mock Google sign-in reaches API keys with no saved target or Add funds dialog. Production authentication and payment were not exercised.
- [x] Pricing layout checked at 1440×900, 375×667 and 320×568; equal callout spacing, visible API entry and no horizontal overflow. Sampled English, Chinese and French layouts. After the CTA rename, all 10 locales were browser-checked at 375×667 with a fully visible API button and no horizontal/text overflow; English desktop at 1440×900 and English/German at 320×568 were also checked. Fresh Arabic RTL browser checks at 1440×900 and 375×667 confirm `lang=ar`, `dir=rtl`, correct CTA direction, first-screen visibility, and no horizontal/text overflow.

The full marketing web suite and build run in CI.
```

---

## fix(platform): raise Add funds limit to $1,000 / 提高充值上限 (#3996)

- **SHA**: `f7004fd6f1c211422aec924c02f96803e10960e8`
- **作者**: david-srp
- **日期**: 2026-10-01T19:55:44Z

### Commit Message

```
fix(platform): raise Add funds limit to $1,000 / 提高充值上限 (#3996)

## Summary / 变更
- Raise the Platform Add funds maximum from $500 to $1,000 ($100,000
cents). / 将 Platform 单次充值上限从 500 美元提高到 1,000 美元。
- Align the API request limit, backend policy, frontend response schema,
preview fixture, and test fixture. / 同步请求校验、后端策略、前端响应校验及预览与测试数据。
- Preserve old frontend bundles: Billing GET defaults to the $500
advertised maximum and returns $1,000 only when the new client sends its
capability header. / 旧版前端仍收到 500 美元上限；新版前端声明能力后才收到 1,000 美元上限。
- Forward that capability header through the Platform Worker proxy. /
Platform Worker 代理转发该能力标识。

## Root cause / 原因
The $500 limit was enforced independently by the Platform backend and
frontend response schema. Updating only one side would leave a displayed
amount that could not be submitted, or an API response that the frontend
rejected. / 原上限分别写在后端和前端校验中，只修改单侧会导致展示与提交不一致。

An older open or cached frontend bundle also rejects a $1,000 Billing
GET response. The new capability header keeps that response at $500 for
old clients regardless of backend deployment order. / 旧版或已缓存的前端也会拒绝返回
1,000 美元上限的 Billing 响应；能力标识让旧客户端在任意部署顺序下继续收到 500 美元上限。

## Test plan / 验证
- [x] Backend capability tests: 62 passed; billing route tests: 3
passed, including $1,000 accepted, $1,000.01 rejected, and old/new
client negotiation.
- [x] Platform router and preview tests: 52 passed, including an old
server response with the new client header.
- [x] Worker proxy and Platform router tests: 56 passed, including
upstream forwarding of the capability header.
- [x] Platform TypeScript typecheck and changed-file ESLint passed.
- [x] Python Ruff and commit hooks passed.
- [ ] Full backend pre-push verification: the isolated worktree
dependency download stalled; CI will run the authoritative backend gate.
```

### PR Body

```
## Summary / 变更
- Raise the Platform Add funds maximum from $500 to $1,000 ($100,000 cents). / 将 Platform 单次充值上限从 500 美元提高到 1,000 美元。
- Align the API request limit, backend policy, frontend response schema, preview fixture, and test fixture. / 同步请求校验、后端策略、前端响应校验及预览与测试数据。
- Preserve old frontend bundles: Billing GET defaults to the $500 advertised maximum and returns $1,000 only when the new client sends its capability header. / 旧版前端仍收到 500 美元上限；新版前端声明能力后才收到 1,000 美元上限。
- Forward that capability header through the Platform Worker proxy. / Platform Worker 代理转发该能力标识。

## Root cause / 原因
The $500 limit was enforced independently by the Platform backend and frontend response schema. Updating only one side would leave a displayed amount that could not be submitted, or an API response that the frontend rejected. / 原上限分别写在后端和前端校验中，只修改单侧会导致展示与提交不一致。

An older open or cached frontend bundle also rejects a $1,000 Billing GET response. The new capability header keeps that response at $500 for old clients regardless of backend deployment order. / 旧版或已缓存的前端也会拒绝返回 1,000 美元上限的 Billing 响应；能力标识让旧客户端在任意部署顺序下继续收到 500 美元上限。

## Test plan / 验证
- [x] Backend capability tests: 62 passed; billing route tests: 3 passed, including $1,000 accepted, $1,000.01 rejected, and old/new client negotiation.
- [x] Platform router and preview tests: 52 passed, including an old server response with the new client header.
- [x] Worker proxy and Platform router tests: 56 passed, including upstream forwarding of the capability header.
- [x] Platform TypeScript typecheck and changed-file ESLint passed.
- [x] Python Ruff and commit hooks passed.
- [ ] Full backend pre-push verification: the isolated worktree dependency download stalled; CI will run the authoritative backend gate.
```

---

## fix(platform): Usage 汇总金额按美分四舍五入 / round total spend to cents (#3995)

- **SHA**: `43849158dd1f3a30b2598ac57c9be8e0b12cfff6`
- **作者**: david-srp
- **日期**: 2026-10-01T18:55:13Z

### Commit Message

```
fix(platform): Usage 汇总金额按美分四舍五入 / round total spend to cents (#3995)

## Summary / 变更概述
- Usage 汇总金额按美分四舍五入，例如 `$0.405717` 显示为 `$0.41`。
- 单条 Usage 记录保留最多六位小数，避免小额费用显示为 `$0.00`。
- Round the Usage summary to cents while preserving up to six decimals
for individual records.

## Root cause / 原因
汇总和明细共用最多六位小数的金额格式化函数，导致汇总展示过多小数位。The summary and individual records
shared the same six-decimal formatter.

## Test plan / 验证
- [x] `pnpm typecheck` in `web/platform`
- [x] `pnpm exec vitest run src/routes/usage.test.tsx` (11 tests)
- [x] ESLint for the three changed files
- [x] `git diff --check`
```

### PR Body

```
## Summary / 变更概述
- Usage 汇总金额按美分四舍五入，例如 `$0.405717` 显示为 `$0.41`。
- 单条 Usage 记录保留最多六位小数，避免小额费用显示为 `$0.00`。
- Round the Usage summary to cents while preserving up to six decimals for individual records.

## Root cause / 原因
汇总和明细共用最多六位小数的金额格式化函数，导致汇总展示过多小数位。The summary and individual records shared the same six-decimal formatter.

## Test plan / 验证
- [x] `pnpm typecheck` in `web/platform`
- [x] `pnpm exec vitest run src/routes/usage.test.tsx` (11 tests)
- [x] ESLint for the three changed files
- [x] `git diff --check`
```

---

## feat(platform): 优化 API key 创建 UI / Improve API key creation UI (#3993)

- **SHA**: `d805fb0ef6b21b76122ec8a2a6c5c64f377236e3`
- **作者**: david-srp
- **日期**: 2026-10-01T18:34:45Z

### Commit Message

```
feat(platform): 优化 API key 创建 UI / Improve API key creation UI (#3993)

## Summary / 变更概述

- 优化 API key 创建弹窗：移除 Cancel，展示所属 Project、名称提示与长度计数，并在输入旁显示创建错误。
- 按参考图调整密钥保存弹窗：强调密钥只展示一次，提供带图标的 Copy key / Copied 按钮和 Done
按钮；关闭后清除页面中的密钥。
- 将预览 API key 列表的分页大小调整为 50，避免仅有两条记录就出现 Load more keys；将导航品牌文字改为 ZooWork
Platform。

- Refine the API key creation dialog with project context, name
guidance, inline errors, and no Cancel button.
- Align the one-time secret dialog with the reference, including Copy
key / Copied and Done actions.
- Match preview key pagination to the 50-item API default and rename the
navigation brand to ZooWork Platform.

## Test plan / 验证

- [x] `pnpm lint` (web/platform)
- [x] `pnpm typecheck` (web/platform)
- [x] `pnpm test -- src/app/router.test.tsx
src/preview/api-middleware.test.ts` (154 tests passed)
- [x] Local preview checked at `/__preview/settings/api-keys`

Expiry display is deferred because the current API does not expose an
expiry value. / 当前 API 尚无过期时间字段，暂不显示。
```

### PR Body

```
## Summary / 变更概述

- 优化 API key 创建弹窗：移除 Cancel，展示所属 Project、名称提示与长度计数，并在输入旁显示创建错误。
- 按参考图调整密钥保存弹窗：强调密钥只展示一次，提供带图标的 Copy key / Copied 按钮和 Done 按钮；关闭后清除页面中的密钥。
- 将预览 API key 列表的分页大小调整为 50，避免仅有两条记录就出现 Load more keys；将导航品牌文字改为 ZooWork Platform。

- Refine the API key creation dialog with project context, name guidance, inline errors, and no Cancel button.
- Align the one-time secret dialog with the reference, including Copy key / Copied and Done actions.
- Match preview key pagination to the 50-item API default and rename the navigation brand to ZooWork Platform.

## Test plan / 验证

- [x] `pnpm lint` (web/platform)
- [x] `pnpm typecheck` (web/platform)
- [x] `pnpm test -- src/app/router.test.tsx src/preview/api-middleware.test.ts` (154 tests passed)
- [x] Local preview checked at `/__preview/settings/api-keys`

Expiry display is deferred because the current API does not expose an expiry value. / 当前 API 尚无过期时间字段，暂不显示。
```

---

## fix(platform): use rounded icons across platform routes (#3992)

- **SHA**: `3fab7255c1c63bad3abd078840e24ccdfd8129cc`
- **作者**: ericma-srp
- **日期**: 2026-10-01T16:53:01Z

### Commit Message

```
fix(platform): use rounded icons across platform routes (#3992)

Platform browser tabs currently show square deep-blue icons. Replace the
16px/32px favicons and 180px touch icon with rounded transparent
corners, preserving the existing color and white mark. Update the shared
production and local-preview HTML entries to the new asset filenames, so
every Platform route uses the rounded icons and browsers fetch fresh
assets.

All changes are limited to `web/platform`. The black ZooWork icon used
by `zoowork.ai` and its brand assets remain unchanged.

Validation:
- `corepack pnpm --filter @zooclaw/platform-app build` passed, including
TypeScript checks; built icon files match the final source assets.
- Pixel checks confirmed transparent corners and unchanged fully opaque
interior pixels at 16px, 32px, and 180px.
- In-browser local-preview checks confirmed the shared rounded icon
links on login, API keys, and Terms routes; source inspection confirmed
the production SPA shares one global entry without route-specific
favicon overrides.
- `git diff --check` passed.
```

### PR Body

```
Platform browser tabs currently show square deep-blue icons. Replace the 16px/32px favicons and 180px touch icon with rounded transparent corners, preserving the existing color and white mark. Update the shared production and local-preview HTML entries to the new asset filenames, so every Platform route uses the rounded icons and browsers fetch fresh assets.

All changes are limited to `web/platform`. The black ZooWork icon used by `zoowork.ai` and its brand assets remain unchanged.

Validation:
- `corepack pnpm --filter @zooclaw/platform-app build` passed, including TypeScript checks; built icon files match the final source assets.
- Pixel checks confirmed transparent corners and unchanged fully opaque interior pixels at 16px, 32px, and 180px.
- In-browser local-preview checks confirmed the shared rounded icon links on login, API keys, and Terms routes; source inspection confirmed the production SPA shares one global entry without route-specific favicon overrides.
- `git diff --check` passed.
```

---

## feat(platform): add Terms page and entry points (#3988)

- **SHA**: `85a33e6829ab704993e172d53d636ccbeba79e28`
- **作者**: ericma-srp
- **日期**: 2026-10-01T15:54:09Z

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

### PR Body

```
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
```

---

## feat(marketing): 优化官网导航与优惠角标 / refine navigation and offer badge (#3991)

- **SHA**: `a5c182616b5ce2761d6f821d7bbb4f9596bbfedb`
- **作者**: david-srp
- **日期**: 2026-10-01T15:50:05Z

### Commit Message

```
feat(marketing): 优化官网导航与优惠角标 / refine navigation and offer badge (#3991)

## Summary
官网共享导航新增 Developer 入口，放在 Enterprise 与 Resources 之间，在新标签页打开
https://zoowork.ai/docs/。移除重复的 Home 导航项，保留 Logo 返回首页；Pricing 右上角增加紧凑的红色
`70% OFF` 角标，复用定价页的优惠颜色。

Add a Developer link between Enterprise and Resources, opening the docs
in a new tab. Remove the redundant Home item while preserving logo
navigation, and show a compact red `70% OFF` badge above Pricing using
the existing pricing offer color. Shared marketing pages and the mobile
menu inherit these changes.

## Test plan
- [x] Rebased onto latest main; preserved the recently added navigation
and mobile download behavior.
- [x] Targeted landing content, header and marketing chrome suites: 54
tests passed.
- [x] TypeScript, ESLint and repository governance checks through the
pre-push gate.
- [x] Browser-checked 1440px desktop, 1103px narrow desktop and 390px
mobile; verified Developer destination/new-tab attributes, logo home
link and no badge overlap.
- [x] Confirmed the navigation and Pricing page offer badges render the
same red color.

仅涉及官网展示，未修改价格、结算或权益逻辑。Presentation only; no pricing, checkout or
entitlement logic changes.
```

### PR Body

```
## Summary
官网共享导航新增 Developer 入口，放在 Enterprise 与 Resources 之间，在新标签页打开 https://zoowork.ai/docs/。移除重复的 Home 导航项，保留 Logo 返回首页；Pricing 右上角增加紧凑的红色 `70% OFF` 角标，复用定价页的优惠颜色。

Add a Developer link between Enterprise and Resources, opening the docs in a new tab. Remove the redundant Home item while preserving logo navigation, and show a compact red `70% OFF` badge above Pricing using the existing pricing offer color. Shared marketing pages and the mobile menu inherit these changes.

## Test plan
- [x] Rebased onto latest main; preserved the recently added navigation and mobile download behavior.
- [x] Targeted landing content, header and marketing chrome suites: 54 tests passed.
- [x] TypeScript, ESLint and repository governance checks through the pre-push gate.
- [x] Browser-checked 1440px desktop, 1103px narrow desktop and 390px mobile; verified Developer destination/new-tab attributes, logo home link and no badge overlap.
- [x] Confirmed the navigation and Pricing page offer badges render the same red color.

仅涉及官网展示，未修改价格、结算或权益逻辑。Presentation only; no pricing, checkout or entitlement logic changes.
```

---

## fix(marketing): 补齐移动下载入口 / preserve non-iOS download fallback (#3987)

- **SHA**: `b35465d0820488602de73ebf7e1a943453fbbb49`
- **作者**: david-srp
- **日期**: 2026-10-01T15:17:34Z

### Commit Message

```
fix(marketing): 补齐移动下载入口 / preserve non-iOS download fallback (#3987)

## Summary

- Follow-up to #3986: route the mobile-menu download CTA through the
existing shared device-aware download action.
- iOS continues directly to the App Store. Android and narrow desktop
visitors keep the marketing page and see the shared QR dialog.
- Close the navigation sheet when starting the download flow; keep
labels, locale behavior, sales CTAs and other navigation unchanged.

补齐 #3986 未包含的移动下载入口修复：iOS 直达 App Store，Android
和窄屏桌面保留官网页面并显示二维码。仅复用已有处理，不改动其它导航。

## Root cause

The mobile-menu download CTA used a direct same-tab App Store link,
bypassing the shared device detection. A narrow viewport is not proof of
iOS, so Android and narrow desktop visitors were also navigated away.
The fix was prepared during #3986 review, but the merge queue locked
that branch and merged before the follow-up could be pushed.

移动菜单由屏幕宽度决定显示，原按钮却对所有设备直接跳 App Store。先前补丁因合并队列锁定未能推送，此 PR 从最新 main 单独补上。

## Test plan

- [x] Prior browser verification of the identical affected source:
Android and narrow desktop retain the current page, show QR, dismiss the
dialog, and reopen the menu successfully.
- [x] Prior iPhone browser emulation of the identical affected source:
same-tab App Store handoff without QR or an extra tab. Apple requests
intercepted for URL verification; physical-device native App Store
launch remains untested.
- [x] Fresh-worktree TypeScript, governance guards, changed-file ESLint
and 50 targeted unit tests.
- [ ] CI and automated review on this PR.
```

### PR Body

```
## Summary

- Follow-up to #3986: route the mobile-menu download CTA through the existing shared device-aware download action.
- iOS continues directly to the App Store. Android and narrow desktop visitors keep the marketing page and see the shared QR dialog.
- Close the navigation sheet when starting the download flow; keep labels, locale behavior, sales CTAs and other navigation unchanged.

补齐 #3986 未包含的移动下载入口修复：iOS 直达 App Store，Android 和窄屏桌面保留官网页面并显示二维码。仅复用已有处理，不改动其它导航。

## Root cause

The mobile-menu download CTA used a direct same-tab App Store link, bypassing the shared device detection. A narrow viewport is not proof of iOS, so Android and narrow desktop visitors were also navigated away. The fix was prepared during #3986 review, but the merge queue locked that branch and merged before the follow-up could be pushed.

移动菜单由屏幕宽度决定显示，原按钮却对所有设备直接跳 App Store。先前补丁因合并队列锁定未能推送，此 PR 从最新 main 单独补上。

## Test plan

- [x] Prior browser verification of the identical affected source: Android and narrow desktop retain the current page, show QR, dismiss the dialog, and reopen the menu successfully.
- [x] Prior iPhone browser emulation of the identical affected source: same-tab App Store handoff without QR or an extra tab. Apple requests intercepted for URL verification; physical-device native App Store launch remains untested.
- [x] Fresh-worktree TypeScript, governance guards, changed-file ESLint and 50 targeted unit tests.
- [ ] CI and automated review on this PR.
```

---

## style(landing): 优化首页产品入口 / refine homepage product navigation (#3990)

- **SHA**: `2cb678187cdab2b87cebd1aa17ce361cc9a74bce`
- **作者**: david-srp
- **日期**: 2026-10-01T15:14:53Z

### Commit Message

```
style(landing): 优化首页产品入口 / refine homepage product navigation (#3990)

## Summary / 改动说明

The homepage product cards looked like static descriptions despite being
clickable. Add always-visible, product-specific CTAs and clearer
hover/focus feedback so visitors can recognize the four entry points and
their next actions.

首页四个产品入口原本容易被误认为静态介绍。本次增加常显 CTA 和清晰的悬停、键盘焦点反馈，让用户直观看出入口可点击。

- Redraw all four product diagrams as consistent SVG illustrations using
the homepage palette; preserve static/reduced-motion variants and
visibility-based animation.
- Replace the section headline, subtitle, and product descriptions with
the approved copy, and synchronize all ten homepage language
dictionaries.
- Keep existing link destinations, new-tab behavior, and login locale
handling. Align desktop CTAs and adapt icon/text spacing for narrow
screens.

统一四组 SVG 的轮廓和品牌配色，更新中英文及其他语言文案，并优化桌面 CTA 对齐与手机布局。链接目标、新标签页行为及登录语言传递保持原样。

## Test plan / 验证

- [x] TypeScript type-check and repository frontend governance checks.
- [x] ESLint and formatting checks; pre-commit and pre-push gates.
- [x] Homepage rendering and localization tests: 95 tests across two
suites.
- [x] Browser validation at 320, 390, 768, 1024, and 1440px: loaded
SVGs, complete text, no horizontal overflow, aligned desktop CTAs.
- [x] English and Chinese screenshots reviewed locally; keyboard focus
and reduced-motion behavior verified.

Frontend-only change. No production deployment is included.
```

### PR Body

```
## Summary / 改动说明

The homepage product cards looked like static descriptions despite being clickable. Add always-visible, product-specific CTAs and clearer hover/focus feedback so visitors can recognize the four entry points and their next actions.

首页四个产品入口原本容易被误认为静态介绍。本次增加常显 CTA 和清晰的悬停、键盘焦点反馈，让用户直观看出入口可点击。

- Redraw all four product diagrams as consistent SVG illustrations using the homepage palette; preserve static/reduced-motion variants and visibility-based animation.
- Replace the section headline, subtitle, and product descriptions with the approved copy, and synchronize all ten homepage language dictionaries.
- Keep existing link destinations, new-tab behavior, and login locale handling. Align desktop CTAs and adapt icon/text spacing for narrow screens.

统一四组 SVG 的轮廓和品牌配色，更新中英文及其他语言文案，并优化桌面 CTA 对齐与手机布局。链接目标、新标签页行为及登录语言传递保持原样。

## Test plan / 验证

- [x] TypeScript type-check and repository frontend governance checks.
- [x] ESLint and formatting checks; pre-commit and pre-push gates.
- [x] Homepage rendering and localization tests: 95 tests across two suites.
- [x] Browser validation at 320, 390, 768, 1024, and 1440px: loaded SVGs, complete text, no horizontal overflow, aligned desktop CTAs.
- [x] English and Chinese screenshots reviewed locally; keyboard focus and reduced-motion behavior verified.

Frontend-only change. No production deployment is included.
```

---

## style(web): refine API keys menu entry / 优化 API 密钥菜单入口 (#3989)

- **SHA**: `9f28425417d8d70664bf4e0451b638a324c011e2`
- **作者**: david-srp
- **日期**: 2026-10-01T15:08:51Z

### Commit Message

```
style(web): refine API keys menu entry / 优化 API 密钥菜单入口 (#3989)

## Summary / 变更说明

Restyle the user settings menu's Managed Agent API entry as a two-line
API key link: “Get API keys” with “on ZooWork Platform”. Add a leading
key icon and a trailing external-link icon, centered with the text block
and aligned with neighboring menu items.

将用户设置菜单中的 Managed Agent API 入口调整为两行文案：中文显示「获取 API 密钥 / 前往 ZooWork
平台」，英文显示「Get API keys / on ZooWork
Platform」。左侧钥匙与右侧外链图标居中对齐，沿用现有主题颜色、Platform 地址、新标签页打开和点击关闭菜单的行为。

## Test plan / 验证

- [x] TypeScript, targeted ESLint, and repository frontend governance
checks passed.
- [x] Existing UserMenu suite passed: 75 tests.
- [x] Browser-verified Chinese and English copy and light/dark
appearance. Both 16px icons share the text block's vertical center.
- [x] `git diff --check` passed.
```

### PR Body

```
## Summary / 变更说明

Restyle the user settings menu's Managed Agent API entry as a two-line API key link: “Get API keys” with “on ZooWork Platform”. Add a leading key icon and a trailing external-link icon, centered with the text block and aligned with neighboring menu items.

将用户设置菜单中的 Managed Agent API 入口调整为两行文案：中文显示「获取 API 密钥 / 前往 ZooWork 平台」，英文显示「Get API keys / on ZooWork Platform」。左侧钥匙与右侧外链图标居中对齐，沿用现有主题颜色、Platform 地址、新标签页打开和点击关闭菜单的行为。

## Test plan / 验证

- [x] TypeScript, targeted ESLint, and repository frontend governance checks passed.
- [x] Existing UserMenu suite passed: 75 tests.
- [x] Browser-verified Chinese and English copy and light/dark appearance. Both 16px icons share the text block's vertical center.
- [x] `git diff --check` passed.
```

---

## feat(platform): support discounted first-purchase top-ups (#3967)

- **SHA**: `d52f9212106f9257162fb52ffcca9c14455d4cc0`
- **作者**: ericma-srp
- **日期**: 2026-10-01T13:02:19Z

### Commit Message

```
feat(platform): support discounted first-purchase top-ups (#3967)

Platform 充值支持在 Stripe Checkout 输入优惠码，并按用户填写的充值金额到账。折扣与实付款分别记录，完全抵扣的订单也能在
Stripe 确认完成后正常发放额度。

### 产品规则

- 保持现有 $5–$500、最多两位小数的输入范围。配置固定 $200 的券时，抵扣为充值金额与 $200 中的较小值：充值 $50，付
$0、到账 $50；充值 $200，付 $0、到账 $200；充值 $300，付 $100、到账 $300。不得自动改价、凑整或扩大折扣。
- 每个 Platform
用户首次成功充值后，不再开放新客优惠入口；全额抵扣和后续退款均不恢复资格。并发结账只允许一个新客资格占用；正常替换结账前必须确认旧 Stripe
Session 已过期；结果不明确且已转人工处理的旧单，仅可保守关闭新客资格占用，让新订单按原价继续。已有 Checkout
历史的账号按保守规则处理。
- Stripe 管理 Coupon 金额、产品和各码核销上限。现有 TOPUP 产品在 Work / Platform
之间共享，不按域名隔离。本 PR 不创建优惠码；另行配置好的活动码不代表支付流程已经验收。
- 新订单固定 Customer、Product 和结账策略。旧订单保留原结账和结算路径；不合并历史身份或余额。

### 结算与安全

通过 Stripe 实际 Session 重新校验身份、产品、币种、充值金额、折扣、实付款和完成状态，再记录结算事实并发放 Lago
额度。失败、未完成或金额不一致的订单不能入账。退款以实付款为上限，继续保留人工补偿审查。订单、资格更新和测试操作沿用持久审计；充值历史分别展示面值、优惠和实付。

并发 Customer reservation 的重复键处理已修复：识别原生及 Mongo wrapper 包装的重复键，读取
canonical binding；无关数据库异常继续抛出。Claude 和 Codex 最近一轮均确认此修复有效。

### 需求负责人接手的验收事项

**2026-10-01，Eric（ericma-srp）明确接受下面两项已披露的风险与待验收状态，负责在 staging 和线上验收；不要求
Claude / Codex 自动代码评审代为完成真实环境验收。两项缺少验收证据不再作为本 PR 等待 AI 处理的
NEED_HUMAN_REVIEW 理由，也不要求 PR 因此保持 Draft。**

| 验收事项 | 当前状态与产品影响 | 责任和验收边界 |
| --- | --- | --- |
| staging CSFLE 数据库读取与资格更新 | 尚未在真实 staging
加密客户端运行。若不兼容，可能导致新用户无法创建充值结账；本地测试不是环境兼容性证据。 | Eric 负责 staging
隔离、带审计的检查，再在线上验收实际充值流程。已有执行脚本和清理/审计方案保留；fixture 脚本不能用于生产。 |
| Stripe 低于最低扣款金额 | 充值 $200.01–$200.49，减去 $200 后应付 $0.01–$0.49，可能被
Stripe 拒绝；尚未完成真实支付验证。 | Eric 在 staging / Stripe
测试环境及线上验收实际行为、失败提示和返回修改金额的体验，并决定活动启用。保持现有金额与折扣规则，不新增自动改价或回退功能来假定问题已经解决。
|

这次交接**不等于验收通过**。Eric 后续记录环境、时间、版本、结果、订单/审计关联
ID及已知边界的最终产品结论。真实环境验收应覆盖全额抵扣、补差额、$200.01 / $200.49 / $200.50
边界、资格不可重复使用、并发/替换结账、失败不入账与成功到账；退款、Webhook 重放与恢复也保留在原有联调范围内。

代码评审仍检查正确性、资金安全、权限、幂等及新引入的实际缺陷。本次不修改 CI、分支保护、仓库级自动评审规则，不撤销历史
review，不豁免其他发现。

-
[需求及验收责任](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/platform-topup-promotions/docs/superpowers/specs/2026-10-01-platform-topup-promotions.md)
- [staging
执行及证据记录](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/platform-topup-promotions/docs/staging-validation/2026-10-01-platform-promotions-csfle.md)
- [Stripe
最低扣款规则](https://docs.stripe.com/currencies#minimum-and-maximum-charge-amounts)

### 最新审查修复与验证

已修复 tim-srp 的三项代码问题，以及后续自动评审确认的一项错误提示问题（与上面的人工环境验收事项分开）：

- **P1：首次结账卡住后，后续充值也被阻塞。** 当保留首购资格的旧单已进入
`manual_review`，新请求先验证同一用户、环境和客户归属，再通过带审计的 CAS 关闭旧
reservation，以旧单为保守的新客资格标记。新订单复用原
Customer，但不开放优惠码，允许用户按原价继续充值。不会把结果不明确的旧单当成未付款、取消旧付款或重新发放新客优惠；旧单的迟到支付仍可在
Stripe 核验后幂等结算。正常可替换的 Checkout 仍须先确认 Stripe 已过期。
- **P2：身份准备失败无限重试并累积审计。** 客户身份准备移到结账租约内，重试次数在调用前持久化，最多 5 次；失败达到上限或超过 20
小时安全窗口后转人工处理，由现有恢复扫描排除。终态重复请求不再写入失败历史。活动租约、并发和过期快照通过 CAS 保护；未开始 Stripe
Checkout 的身份准备不能被误认成历史购买。

- **P1：后台恢复旧失败订单会关闭用户正在使用的结账页面。**
只有用户主动创建或重试充值，才允许替换另一订单的结账。后台恢复默认无替换权限；竞争失败的订单转入有明确原因的人工处理状态，不再自动扫描。用户主动重试仍可在次数和时间上限内继续原请求。回归复现了
A 正在准备、B 被拒绝、A 成功打开、后台恢复 B 的完整顺序，确认 A 不会被关闭；主动重试 B 时才执行经核验的替换。
- **P1：客户准备失败返回未处理的异常。** Stripe /
账单客户准备失败保留重试状态和审计，向前端返回既有的“账单服务暂时不可用”错误约定，不泄露底层错误；身份竞争仍返回正常冲突提示。

已同步最新 `main`。回归覆盖无 Session/异常旧单、归属错误、CAS 竞争、原价 Checkout
参数、旧单迟到支付与重复事件、正常新客资格、持续/临时身份失败、最后一次尝试并发、崩溃与超时、旧数据无计数字段。

本次本地验证：

- 235 项相关后端测试通过；后端完整 ruff、format、pyright（app/tests）及 8 项 import
contracts 通过。
- Platform 前端 129 项测试、ESLint 及 TypeScript/Vite build 通过，覆盖与最新 main
合并后的新版充值历史页面。
- pre-commit 的 pyright 包装脚本仍有目录空格问题，因此该包装项使用已完成的独立完整 `verify-py.sh`
结果替代；未修改仓库检查规则，其他提交/推送检查照常执行。
- 上述是本地/mock 验证，真实 staging CSFLE 和 Stripe/Lago 验收仍由 Eric 按上文负责，未标记为通过。

### 上一轮冲突解决与 Tim 意见（0443426d6）

最新提交 `0443426d6` 合入 `main@4184093a8`。冲突仅在充值历史表格：保留 main 的共享 Table
组件、新版布局、状态展示及溢出处理，同时保留本 PR 的 Discount / Paid 信息；不退回旧版界面，不修改充值金额和优惠计算。

Tim 在 `d89307c0d`
上指出的重试计数问题已复现并修复：结账/优惠资格冲突不再消耗身份准备重试次数。仍先持久化尝试以覆盖进程崩溃，但已确认的冲突在同一带租约校验和审计的状态更新里退回本次计数，保留此前真实服务故障次数。后台仍不能恢复冲突订单或替换正在使用的
Checkout；真实失败仍受 5 次/20 小时上限限制。

回归：同一充值请求连续冲突 7 次，分别从 0 次和 4 次历史服务失败开始，之后用户主动重试均可替换已确认过期的旧 Session；另验证 4
次历史服务失败经过冲突后仍保留，第 5 次真实失败会终止自动恢复。新增断言在修复前失败、修复后通过。

216 项后端测试和 129 项前端测试通过，完整后端静态/类型/依赖检查与 Platform lint/build 通过。最新提交的
GitHub 检查已结束：27 项通过，14 项按条件跳过，无失败或待完成项；本 PR merge ref 无未解决 CodeQL 告警。Tim
提到的真实 Mongo/CSFLE 查询验证仍属于 Eric 已接手的环境验收，单元测试不冒充真实环境证据，Stripe
最低扣款验收边界也保持不变。

上一提交 `d89307c0d` 的 Claude / Codex 均为 APPROVE。Claude 的未来共享 helper
建议未实施：目前没有必要增加抽象。最新提交 `0443426d6` 的 Claude / Codex 也均为 APPROVE，无
P0/P1/P2，Claude 明确确认 Tim 最新问题已修复。GitHub 已确认 MERGEABLE（无合并冲突）；已重新请求 Tim
正式审查，当前 BLOCKED 仍等待审批条件，并非合并冲突。


### 最新修复：长时间未完成的 Stripe Customer 关联与 Pricing 分隔线（90ad46023）

Tim 在 `0443426d6` 上提出的 P2 已修复。原逻辑在未绑定 Customer 的预留超过 23
小时后永久拒绝充值；现在转入有审计的核对流程：分页列举预留创建以来的 Stripe Customers（含 5 分钟时钟裕量），按原始
binding 元数据、UID 与环境核对。唯一匹配时恢复原
Customer；完整确认没有匹配后才重试原创建参数及幂等键，保留已有优惠资格状态。成功通过现有 CAS 关联并记录
`customer.reconciled`，失败、重放意图也记录到原 binding 审计。

不把超时、分页中断、畸形响应、多重匹配或身份不一致视为“没有客户”。每次最多读取 100 页；还有后续页时，将游标和候选 Customer
带审计地保存，下次从断点继续，不能据此创建客户。完整扫描后、重放创建前清空断点，避免漏掉随后成功创建的客户。原有订单重试/时间上限、绑定归属校验及新客资格规则均保留。本次没有操作真实
Stripe 客户或修改优惠码。

Stripe 没有按幂等键直接查 Customer 的接口；使用原请求写入的确定性 binding 元数据查证创建结果。遵循 [Customer
列表分页](https://docs.stripe.com/api/customers/list) 与
[幂等请求](https://docs.stripe.com/api/idempotent_requests) 约定，不使用可能延迟的
[Search](https://docs.stripe.com/api/customers/search) 结果作为客户不存在的证明。

同 PR 包含用户点名的小 UI 调整：Pricing 的 Pro / Enterprise 中间竖线从 `pricing-ink/18`
调淡到 `pricing-ink/8`，5 处组成同一条竖线的单元格保持一致；布局、文案、横线及其他边框不变。

验证：235 项相关后端测试通过，覆盖 23 小时前/边界/多日后的恢复、分页、歧义/失败不创建、原键重放、并发收敛、资格保留和恢复后的原价
Checkout；Pricing 原有 5 项测试、TypeScript、ESLint 与前端治理检查通过。真实 staging CSFLE 与
Stripe 验收仍按前文由 Eric 负责。

当前最新提交为 `9b27a8df0`。GitHub 检查已结束，无失败或待完成项，merge ref 无未解决 CodeQL
告警，GitHub 确认为 MERGEABLE。Codex 最新评审 APPROVE；Claude 确认没有新增代码缺陷，仅为 Eric
已接手的两项环境验收给出 NEED_HUMAN_REVIEW。按既定用户要求移除了该标签并保留原始评审与待验收状态，仍等待 Tim 正式审查。

Claude 在 `90ad46023` 上提出的大账户扫描上限问题已进一步修复：100
页是单次批量上限，不是永久上限；游标及候选客户跨请求保存，CAS 同时校验旧时间戳与断点，防止过期 worker
覆盖进度。没有按“创建后几小时”缩短查询时间范围，因为更晚成功的创建也必须核对。新增测试覆盖跨批次匹配、跨批次重复匹配、创建丢失响应后重新从头核对，以及并发过期
worker。后端回归总数更新为 235。Pricing 调淡是用户明确要求的同 PR 范围，并非 rebase 意外带入。

环境验收范围补充：`customer_repair_cursor` / `customer_repair_match_id` 与
`updated_at` 参与的断点 CAS，需要实际验证旧文档字段缺失、断点保存/续读、竞争更新失败与完成后的清空；本地测试及现有 probe
不代表这些字段已通过 staging CSFLE 实跑。
```

### PR Body

```
Platform 充值支持在 Stripe Checkout 输入优惠码，并按用户填写的充值金额到账。折扣与实付款分别记录，完全抵扣的订单也能在 Stripe 确认完成后正常发放额度。

### 产品规则

- 保持现有 $5–$500、最多两位小数的输入范围。配置固定 $200 的券时，抵扣为充值金额与 $200 中的较小值：充值 $50，付 $0、到账 $50；充值 $200，付 $0、到账 $200；充值 $300，付 $100、到账 $300。不得自动改价、凑整或扩大折扣。
- 每个 Platform 用户首次成功充值后，不再开放新客优惠入口；全额抵扣和后续退款均不恢复资格。并发结账只允许一个新客资格占用；正常替换结账前必须确认旧 Stripe Session 已过期；结果不明确且已转人工处理的旧单，仅可保守关闭新客资格占用，让新订单按原价继续。已有 Checkout 历史的账号按保守规则处理。
- Stripe 管理 Coupon 金额、产品和各码核销上限。现有 TOPUP 产品在 Work / Platform 之间共享，不按域名隔离。本 PR 不创建优惠码；另行配置好的活动码不代表支付流程已经验收。
- 新订单固定 Customer、Product 和结账策略。旧订单保留原结账和结算路径；不合并历史身份或余额。

### 结算与安全

通过 Stripe 实际 Session 重新校验身份、产品、币种、充值金额、折扣、实付款和完成状态，再记录结算事实并发放 Lago 额度。失败、未完成或金额不一致的订单不能入账。退款以实付款为上限，继续保留人工补偿审查。订单、资格更新和测试操作沿用持久审计；充值历史分别展示面值、优惠和实付。

并发 Customer reservation 的重复键处理已修复：识别原生及 Mongo wrapper 包装的重复键，读取 canonical binding；无关数据库异常继续抛出。Claude 和 Codex 最近一轮均确认此修复有效。

### 需求负责人接手的验收事项

**2026-10-01，Eric（ericma-srp）明确接受下面两项已披露的风险与待验收状态，负责在 staging 和线上验收；不要求 Claude / Codex 自动代码评审代为完成真实环境验收。两项缺少验收证据不再作为本 PR 等待 AI 处理的 NEED_HUMAN_REVIEW 理由，也不要求 PR 因此保持 Draft。**

| 验收事项 | 当前状态与产品影响 | 责任和验收边界 |
| --- | --- | --- |
| staging CSFLE 数据库读取与资格更新 | 尚未在真实 staging 加密客户端运行。若不兼容，可能导致新用户无法创建充值结账；本地测试不是环境兼容性证据。 | Eric 负责 staging 隔离、带审计的检查，再在线上验收实际充值流程。已有执行脚本和清理/审计方案保留；fixture 脚本不能用于生产。 |
| Stripe 低于最低扣款金额 | 充值 $200.01–$200.49，减去 $200 后应付 $0.01–$0.49，可能被 Stripe 拒绝；尚未完成真实支付验证。 | Eric 在 staging / Stripe 测试环境及线上验收实际行为、失败提示和返回修改金额的体验，并决定活动启用。保持现有金额与折扣规则，不新增自动改价或回退功能来假定问题已经解决。 |

这次交接**不等于验收通过**。Eric 后续记录环境、时间、版本、结果、订单/审计关联 ID及已知边界的最终产品结论。真实环境验收应覆盖全额抵扣、补差额、$200.01 / $200.49 / $200.50 边界、资格不可重复使用、并发/替换结账、失败不入账与成功到账；退款、Webhook 重放与恢复也保留在原有联调范围内。

代码评审仍检查正确性、资金安全、权限、幂等及新引入的实际缺陷。本次不修改 CI、分支保护、仓库级自动评审规则，不撤销历史 review，不豁免其他发现。

- [需求及验收责任](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/platform-topup-promotions/docs/superpowers/specs/2026-10-01-platform-topup-promotions.md)
- [staging 执行及证据记录](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/platform-topup-promotions/docs/staging-validation/2026-10-01-platform-promotions-csfle.md)
- [Stripe 最低扣款规则](https://docs.stripe.com/currencies#minimum-and-maximum-charge-amounts)

### 最新审查修复与验证

已修复 tim-srp 的三项代码问题，以及后续自动评审确认的一项错误提示问题（与上面的人工环境验收事项分开）：

- **P1：首次结账卡住后，后续充值也被阻塞。** 当保留首购资格的旧单已进入 `manual_review`，新请求先验证同一用户、环境和客户归属，再通过带审计的 CAS 关闭旧 reservation，以旧单为保守的新客资格标记。新订单复用原 Customer，但不开放优惠码，允许用户按原价继续充值。不会把结果不明确的旧单当成未付款、取消旧付款或重新发放新客优惠；旧单的迟到支付仍可在 Stripe 核验后幂等结算。正常可替换的 Checkout 仍须先确认 Stripe 已过期。
- **P2：身份准备失败无限重试并累积审计。** 客户身份准备移到结账租约内，重试次数在调用前持久化，最多 5 次；失败达到上限或超过 20 小时安全窗口后转人工处理，由现有恢复扫描排除。终态重复请求不再写入失败历史。活动租约、并发和过期快照通过 CAS 保护；未开始 Stripe Checkout 的身份准备不能被误认成历史购买。

- **P1：后台恢复旧失败订单会关闭用户正在使用的结账页面。** 只有用户主动创建或重试充值，才允许替换另一订单的结账。后台恢复默认无替换权限；竞争失败的订单转入有明确原因的人工处理状态，不再自动扫描。用户主动重试仍可在次数和时间上限内继续原请求。回归复现了 A 正在准备、B 被拒绝、A 成功打开、后台恢复 B 的完整顺序，确认 A 不会被关闭；主动重试 B 时才执行经核验的替换。
- **P1：客户准备失败返回未处理的异常。** Stripe / 账单客户准备失败保留重试状态和审计，向前端返回既有的“账单服务暂时不可用”错误约定，不泄露底层错误；身份竞争仍返回正常冲突提示。

已同步最新 `main`。回归覆盖无 Session/异常旧单、归属错误、CAS 竞争、原价 Checkout 参数、旧单迟到支付与重复事件、正常新客资格、持续/临时身份失败、最后一次尝试并发、崩溃与超时、旧数据无计数字段。

本次本地验证：

- 235 项相关后端测试通过；后端完整 ruff、format、pyright（app/tests）及 8 项 import contracts 通过。
- Platform 前端 129 项测试、ESLint 及 TypeScript/Vite build 通过，覆盖与最新 main 合并后的新版充值历史页面。
- pre-commit 的 pyright 包装脚本仍有目录空格问题，因此该包装项使用已完成的独立完整 `verify-py.sh` 结果替代；未修改仓库检查规则，其他提交/推送检查照常执行。
- 上述是本地/mock 验证，真实 staging CSFLE 和 Stripe/Lago 验收仍由 Eric 按上文负责，未标记为通过。

### 上一轮冲突解决与 Tim 意见（0443426d6）

最新提交 `0443426d6` 合入 `main@4184093a8`。冲突仅在充值历史表格：保留 main 的共享 Table 组件、新版布局、状态展示及溢出处理，同时保留本 PR 的 Discount / Paid 信息；不退回旧版界面，不修改充值金额和优惠计算。

Tim 在 `d89307c0d` 上指出的重试计数问题已复现并修复：结账/优惠资格冲突不再消耗身份准备重试次数。仍先持久化尝试以覆盖进程崩溃，但已确认的冲突在同一带租约校验和审计的状态更新里退回本次计数，保留此前真实服务故障次数。后台仍不能恢复冲突订单或替换正在使用的 Checkout；真实失败仍受 5 次/20 小时上限限制。

回归：同一充值请求连续冲突 7 次，分别从 0 次和 4 次历史服务失败开始，之后用户主动重试均可替换已确认过期的旧 Session；另验证 4 次历史服务失败经过冲突后仍保留，第 5 次真实失败会终止自动恢复。新增断言在修复前失败、修复后通过。

216 项后端测试和 129 项前端测试通过，完整后端静态/类型/依赖检查与 Platform lint/build 通过。最新提交的 GitHub 检查已结束：27 项通过，14 项按条件跳过，无失败或待完成项；本 PR merge ref 无未解决 CodeQL 告警。Tim 提到的真实 Mongo/CSFLE 查询验证仍属于 Eric 已接手的环境验收，单元测试不冒充真实环境证据，Stripe 最低扣款验收边界也保持不变。

上一提交 `d89307c0d` 的 Claude / Codex 均为 APPROVE。Claude 的未来共享 helper 建议未实施：目前没有必要增加抽象。最新提交 `0443426d6` 的 Claude / Codex 也均为 APPROVE，无 P0/P1/P2，Claude 明确确认 Tim 最新问题已修复。GitHub 已确认 MERGEABLE（无合并冲突）；已重新请求 Tim 正式审查，当前 BLOCKED 仍等待审批条件，并非合并冲突。


### 最新修复：长时间未完成的 Stripe Customer 关联与 Pricing 分隔线（90ad46023）

Tim 在 `0443426d6` 上提出的 P2 已修复。原逻辑在未绑定 Customer 的预留超过 23 小时后永久拒绝充值；现在转入有审计的核对流程：分页列举预留创建以来的 Stripe Customers（含 5 分钟时钟裕量），按原始 binding 元数据、UID 与环境核对。唯一匹配时恢复原 Customer；完整确认没有匹配后才重试原创建参数及幂等键，保留已有优惠资格状态。成功通过现有 CAS 关联并记录 `customer.reconciled`，失败、重放意图也记录到原 binding 审计。

不把超时、分页中断、畸形响应、多重匹配或身份不一致视为“没有客户”。每次最多读取 100 页；还有后续页时，将游标和候选 Customer 带审计地保存，下次从断点继续，不能据此创建客户。完整扫描后、重放创建前清空断点，避免漏掉随后成功创建的客户。原有订单重试/时间上限、绑定归属校验及新客资格规则均保留。本次没有操作真实 Stripe 客户或修改优惠码。

Stripe 没有按幂等键直接查 Customer 的接口；使用原请求写入的确定性 binding 元数据查证创建结果。遵循 [Customer 列表分页](https://docs.stripe.com/api/customers/list) 与 [幂等请求](https://docs.stripe.com/api/idempotent_requests) 约定，不使用可能延迟的 [Search](https://docs.stripe.com/api/customers/search) 结果作为客户不存在的证明。

同 PR 包含用户点名的小 UI 调整：Pricing 的 Pro / Enterprise 中间竖线从 `pricing-ink/18` 调淡到 `pricing-ink/8`，5 处组成同一条竖线的单元格保持一致；布局、文案、横线及其他边框不变。

验证：235 项相关后端测试通过，覆盖 23 小时前/边界/多日后的恢复、分页、歧义/失败不创建、原键重放、并发收敛、资格保留和恢复后的原价 Checkout；Pricing 原有 5 项测试、TypeScript、ESLint 与前端治理检查通过。真实 staging CSFLE 与 Stripe 验收仍按前文由 Eric 负责。

当前最新提交为 `9b27a8df0`。GitHub 检查已结束，无失败或待完成项，merge ref 无未解决 CodeQL 告警，GitHub 确认为 MERGEABLE。Codex 最新评审 APPROVE；Claude 确认没有新增代码缺陷，仅为 Eric 已接手的两项环境验收给出 NEED_HUMAN_REVIEW。按既定用户要求移除了该标签并保留原始评审与待验收状态，仍等待 Tim 正式审查。

Claude 在 `90ad46023` 上提出的大账户扫描上限问题已进一步修复：100 页是单次批量上限，不是永久上限；游标及候选客户跨请求保存，CAS 同时校验旧时间戳与断点，防止过期 worker 覆盖进度。没有按“创建后几小时”缩短查询时间范围，因为更晚成功的创建也必须核对。新增测试覆盖跨批次匹配、跨批次重复匹配、创建丢失响应后重新从头核对，以及并发过期 worker。后端回归总数更新为 235。Pricing 调淡是用户明确要求的同 PR 范围，并非 rebase 意外带入。

环境验收范围补充：`customer_repair_cursor` / `customer_repair_match_id` 与 `updated_at` 参与的断点 CAS，需要实际验证旧文档字段缺失、断点保存/续读、竞争更新失败与完成后的清空；本地测试及现有 probe 不代表这些字段已通过 staging CSFLE 实跑。
```

---

## fix(marketing): 修复官网入口 / fix website CTA navigation (#3986)

- **SHA**: `7196eb86507a5ff714439511ed8cc8f6dbad73c4`
- **作者**: david-srp
- **日期**: 2026-10-01T13:00:41Z

### Commit Message

```
fix(marketing): 修复官网入口 / fix website CTA navigation (#3986)

## Summary

- Get Started 菜单将 `ZooWork.ai` 更名为 `Agent Builder`；官网共用的 Talk to Sales
按钮在新标签页打开当前语言的 Enterprise 表单页。
- 产品菜单、卡片及页脚的产品入口统一新开标签页，站内内容导航保留同页。保留 Agent Builder 的语言与登录交接参数。
- 官网 iPhone/iPad 下载入口直接前往 App Store，桌面保留二维码；首页复用共享下载处理，移除重复弹窗包装。

Rename the menu entry to Agent Builder, route sales CTAs to localized
Enterprise forms, align product links to new tabs, and send iOS visitors
directly to the App Store while retaining desktop QR downloads.

## Root cause

销售按钮仍使用邮件链接；各产品入口独立决定打开方式；首页和页脚直接弹二维码，移动菜单则直链 App Store，造成同一设备操作不一致。

Sales CTAs used mail links, and separate navigation/download
implementations produced inconsistent behavior across entry points.

## Test plan

- [x] 136 related unit tests across 8 files, including iPhone
Safari/Chrome, iPad desktop mode, non-iOS fallbacks, localized sales
links, login handoffs, and product navigation.
- [x] TypeScript, changed-file ESLint, repository governance guards, and
`git diff --check`.
- [x] Desktop Chrome: menu copy; all 3 homepage sales CTAs; all 4
product cards; same-tab Pricing; actual Enterprise popup and
first-screen form; desktop QR dialog.
- [x] iPhone browser emulation: footer, homepage App section, mobile
Products menu, and mobile download button navigate directly to the App
Store in the current tab without a QR dialog. App Store requests were
intercepted for URL verification; native iOS app launch was not tested
on a physical device.
```

### PR Body

```
## Summary

- Get Started 菜单将 `ZooWork.ai` 更名为 `Agent Builder`；官网共用的 Talk to Sales 按钮在新标签页打开当前语言的 Enterprise 表单页。
- 产品菜单、卡片及页脚的产品入口统一新开标签页，站内内容导航保留同页。保留 Agent Builder 的语言与登录交接参数。
- 官网 iPhone/iPad 下载入口直接前往 App Store，桌面保留二维码；首页复用共享下载处理，移除重复弹窗包装。

Rename the menu entry to Agent Builder, route sales CTAs to localized Enterprise forms, align product links to new tabs, and send iOS visitors directly to the App Store while retaining desktop QR downloads.

## Root cause

销售按钮仍使用邮件链接；各产品入口独立决定打开方式；首页和页脚直接弹二维码，移动菜单则直链 App Store，造成同一设备操作不一致。

Sales CTAs used mail links, and separate navigation/download implementations produced inconsistent behavior across entry points.

## Test plan

- [x] Initial implementation: 136 related unit tests across 8 files, including iPhone Safari/Chrome, iPad desktop mode, non-iOS fallbacks, localized sales links, login handoffs, and product navigation.
- [x] TypeScript, changed-file ESLint, repository governance guards, and `git diff --check`.
- [x] Desktop Chrome: menu copy; all 3 homepage sales CTAs; all 4 product cards; same-tab Pricing; actual Enterprise popup and first-screen form; desktop QR dialog.
- [x] iPhone browser emulation: footer, homepage App section, mobile Products menu, and mobile download button navigate directly to the App Store in the current tab without a QR dialog. App Store requests were intercepted for URL verification; native iOS app launch was not tested on a physical device.

## Unmerged follow-up / 未包含的后续补丁

The non-iOS mobile-menu download fallback fix is committed locally as `5b1cf6237`, but is **not included in this merged PR**: GitHub rejected the push while the PR was in the merge queue, and the queue merged the original head at 2026-10-01 13:09:02 UTC as `7196eb86507a5ff714439511ed8cc8f6dbad73c4`. The local follow-up passed 50 related unit tests, TypeScript, ESLint, governance guards, and browser checks for Android/narrow-desktop QR flow and iPhone App Store handoff. A separate follow-up PR is needed. This task did not change the queue or perform the merge.

非 iOS 移动菜单下载入口修复已在本地完成验证，但未赶上队列合并；需另开后续 PR。合入的是 `05d97f3b2`，不包含本地补丁 `5b1cf6237`。
```

---

## fix(platform): persist login across tabs / 跨标签页保持登录 (#3984)

- **SHA**: `253ce6ab4f605ce91ef683d4c528b462e7305f90`
- **作者**: david-srp
- **日期**: 2026-10-01T13:00:01Z

### Commit Message

```
fix(platform): persist login across tabs / 跨标签页保持登录 (#3984)

## Summary / 改动
Platform previously stored its account JWT only in sessionStorage.
Opening an independent tab or returning after closing the page required
another login even while the token remained valid.

- Persist a verified, Platform-only JWT in a host-only
HttpOnly/Secure/SameSite=Lax cookie, bounded by its signed expiry;
migrate existing tab credentials without discarding them on transient
failures.
- Add a same-origin Cloudflare Worker session BFF and `/platform/v1`
proxy. Preserve `ecap-platform` identity isolation and existing upstream
authorization/idempotency contracts; enforce same-origin mutations and
no-store responses.
- Synchronize login/logout across tabs, revalidate confirmed business
authentication errors without replaying writes, and preserve OTP/Google
login across focus changes.
- Always route development, preview and production API calls through the
page origin, ignoring legacy VITE_API_BASE_URL overrides. Wire Worker
upstream URLs from existing deployment variables and document local
development.

新标签页、关页重开可恢复登录；退出和切换账号同步其他标签页。业务 API 401
会重新验证账号，网络/权限故障不会误清会话，写操作不会自动重放。

## Root cause / 原因与边界
Session persistence was scoped to a browser tab, while business 401
responses had no identity recovery path. The existing
interrupted-restoration fix (#3979) is retained.

Account service main currently signs registered-user JWTs for 300 days
by default and has no general refresh-token endpoint. This PR respects
the actual signed expiry; it does not invent renewal, extend tokens,
share Work's cookie, change backend billing, or claim production
validation. Actual expiry still requires sign-in.

## Validation / 验证
- [x] Platform lint and TypeScript checks
- [x] Platform unit/component suite: 148 tests passed
- [x] Production Vite build
- [x] Local Chromium + real Wrangler Worker against synthetic
Account/API fixtures: persistent HttpOnly cookie, new-tab
authentication, close-all-pages/reopen authentication, no JWT in Web
Storage, cross-tab logout
- [x] Real Vite → Wrangler → synthetic Account/API smoke with an
existing-style `.env.local` pointing `VITE_API_BASE_URL` at the old
backend: cookie issuance, same-origin business calls with upstream
Bearer, new-tab login, cross-tab logout, and no JWT in Web Storage
- [x] Worker regressions: business/expiry validation, CSRF, transient
preservation, proxy header/idempotency contract, upstream cookie
stripping
- [x] Independent code review; fixed and regression-tested the
focus/OTP/Google-login race it found
- [x] `git diff --check`

No live business writes, deployment or release were performed. Staging
integration with real Account/Firebase remains a deployment verification
step.
```

### PR Body

```
## Summary / 改动
Platform previously stored its account JWT only in sessionStorage. Opening an independent tab or returning after closing the page required another login even while the token remained valid.

- Persist a verified, Platform-only JWT in a host-only HttpOnly/Secure/SameSite=Lax cookie, bounded by its signed expiry; migrate existing tab credentials without discarding them on transient failures.
- Add a same-origin Cloudflare Worker session BFF and `/platform/v1` proxy. Preserve `ecap-platform` identity isolation and existing upstream authorization/idempotency contracts; enforce same-origin mutations and no-store responses.
- Synchronize login/logout across tabs, revalidate confirmed business authentication errors without replaying writes, and preserve OTP/Google login across focus changes.
- Always route development, preview and production API calls through the page origin, ignoring legacy VITE_API_BASE_URL overrides. Wire Worker upstream URLs from existing deployment variables and document local development.

新标签页、关页重开可恢复登录；退出和切换账号同步其他标签页。业务 API 401 会重新验证账号，网络/权限故障不会误清会话，写操作不会自动重放。

## Root cause / 原因与边界
Session persistence was scoped to a browser tab, while business 401 responses had no identity recovery path. The existing interrupted-restoration fix (#3979) is retained.

Account service main currently signs registered-user JWTs for 300 days by default and has no general refresh-token endpoint. This PR respects the actual signed expiry; it does not invent renewal, extend tokens, share Work's cookie, change backend billing, or claim production validation. Actual expiry still requires sign-in.

## Validation / 验证
- [x] Platform lint and TypeScript checks
- [x] Platform unit/component suite: 148 tests passed
- [x] Production Vite build
- [x] Local Chromium + real Wrangler Worker against synthetic Account/API fixtures: persistent HttpOnly cookie, new-tab authentication, close-all-pages/reopen authentication, no JWT in Web Storage, cross-tab logout
- [x] Real Vite → Wrangler → synthetic Account/API smoke with an existing-style `.env.local` pointing `VITE_API_BASE_URL` at the old backend: cookie issuance, same-origin business calls with upstream Bearer, new-tab login, cross-tab logout, and no JWT in Web Storage
- [x] Worker regressions: business/expiry validation, CSRF, transient preservation, proxy header/idempotency contract, upstream cookie stripping
- [x] Independent code review; fixed and regression-tested the focus/OTP/Google-login race it found
- [x] `git diff --check`

No live business writes, deployment or release were performed. Staging integration with real Account/Firebase remains a deployment verification step.
```

---

## fix(auth): 修复移动端登录页滚动 / stabilize mobile login scrolling (#3985)

- **SHA**: `5450405d1a895cd1618c0c7872129c0136d4e269`
- **作者**: david-srp
- **日期**: 2026-10-01T12:42:04Z

### Commit Message

```
fix(auth): 修复移动端登录页滚动 / stabilize mobile login scrolling (#3985)

## Summary / 改动
- 修复 Web App 与 Platform
登录页在手机浏览器中随视口变化上下跳动、顶部不易返回及露出黑色背景的问题。移动端采用顶部自然排列和稳定的 `svh`
最小高度，保留整页原生滚动；桌面保留双栏居中。
- Stabilize both mobile login layouts and scope the white document
canvas to the standalone login route. Authentication behavior is
unchanged; the selected theme returns when leaving login.

## Root cause / 原因
动态视口高度配合垂直居中会在地址栏伸缩时移动内容；Platform 外层仍使用
`100vh`，与登录容器高度不一致；两端登录页外层还会继承深色背景。The fix removes mobile recentering
and aligns the login document canvas without introducing scroll locks or
viewport JavaScript.

## Test plan / 验证
- [x] Web App governance guards, TypeScript, login-related tests,
targeted ESLint, and pre-commit full ESLint.
- [x] Platform TypeScript, 22 login/theme tests, and targeted ESLint.
- [x] Chromium mobile widths 320 / 393 / 430 and landscape 844; viewport
heights 850 → 680 → 320 → 850; heading stays at 104px for width 393.
- [x] Focus input in a short viewport, touch-scroll back to the header,
reach bottom terms, and check horizontal overflow.
- [x] Light/dark login canvas, theme restoration after login unmount,
and desktop 1440 × 900 screenshots.
- [ ] iPhone Chrome device verification. Chromium emulation does not
reproduce native iOS browser chrome or keyboard; supplemental WebKit
download was stopped due to slow transfer.

Review focus: mobile scroll recovery and scoped document styles in both
login surfaces. No backend deployment is required; Web App and Platform
are separate frontend deployments.
```

### PR Body

```
## Summary / 改动
- 修复 Web App 与 Platform 登录页在手机浏览器中随视口变化上下跳动、顶部不易返回及露出黑色背景的问题。移动端采用顶部自然排列和稳定的 `svh` 最小高度，保留整页原生滚动；桌面保留双栏居中。
- Stabilize both mobile login layouts and scope the white document canvas to the standalone login route. Authentication behavior is unchanged; the selected theme returns when leaving login.

## Root cause / 原因
动态视口高度配合垂直居中会在地址栏伸缩时移动内容；Platform 外层仍使用 `100vh`，与登录容器高度不一致；两端登录页外层还会继承深色背景。The fix removes mobile recentering and aligns the login document canvas without introducing scroll locks or viewport JavaScript.

## Test plan / 验证
- [x] Web App governance guards, TypeScript, login-related tests, targeted ESLint, and pre-commit full ESLint.
- [x] Platform TypeScript, 22 login/theme tests, and targeted ESLint.
- [x] Chromium mobile widths 320 / 393 / 430 and landscape 844; viewport heights 850 → 680 → 320 → 850; heading stays at 104px for width 393.
- [x] Focus input in a short viewport, touch-scroll back to the header, reach bottom terms, and check horizontal overflow.
- [x] Light/dark login canvas, theme restoration after login unmount, and desktop 1440 × 900 screenshots.
- [ ] iPhone Chrome device verification. Chromium emulation does not reproduce native iOS browser chrome or keyboard; supplemental WebKit download was stopped due to slow transfer.

Review focus: mobile scroll recovery and scoped document styles in both login surfaces. No backend deployment is required; Web App and Platform are separate frontend deployments.
```

---

## fix(web): 修复 iOS Google 登录 / prepare Google sign-in on iOS (#3983)

- **SHA**: `ef3b0f9ccd69446d5290e18d0d2fc0c59764743e`
- **作者**: david-srp
- **日期**: 2026-10-01T12:17:24Z

### Commit Message

```
fix(web): 修复 iOS Google 登录 / prepare Google sign-in on iOS (#3983)

## Summary

修复 webapp 在 iOS 上的 Google 登录路径：登录表单挂载时等待 Firebase
`authStateReady()`，准备完成后才启用 Google 按钮；iPhone/iPad 改用直接由点击触发的
popup。准备失败时显示提示，邮箱与手机登录继续可用。

Prepare Firebase before enabling Google sign-in and use the existing
popup/token-exchange flow on iOS. Apply the readiness state to the
default, landing, and legacy Platform login forms. Preserve Android
redirect behavior and existing session-reset/profile-persistence
safeguards.

## Root cause

当前 webapp 将 iOS 导向 `signInWithRedirect`，该流程可能受 Safari 的跨域存储限制影响。直接切换
popup 仍需处理首次初始化耗时：Firebase 在 Safari 上会提前初始化 popup
resolver，等待这一步完成后再允许点击，可以避免初始化消耗点击的 transient user activation。点击 handler
内不再等待准备过程。

The existing mobile branch sends iOS through Firebase redirect sign-in,
which is sensitive to third-party storage restrictions. This adopts the
preparation approach from Finn's #3974: finish Firebase startup before
the click, then invoke `signInWithPopup` directly from the click
handler. Firebase token exchange and profile persistence still use the
existing desktop path.

References: #3974 (Platform popup initialization), #3972 (separate
first-party auth-domain approach for redirects).

## Test plan

- [x] 231 targeted tests passed across 7 suites: login form, redirect
completion, login modal, app-shell auth, standalone login page, landing
login modal, and auth manager.
- [x] New preparation and iPhone/iPad popup regression cases failed
against the original implementation, then passed with the fix.
- [x] `bash scripts/verify-web.sh --no-test src/components/LoginForm.tsx
src/components/login/PlatformLoginFields.tsx src/locales/en.ts
src/locales/zh.ts tests/unit/components/LoginForm.unit.spec.tsx` —
TypeScript, ESLint, and governance checks passed.
- [x] `git diff --check`.
- [ ] Real-device iOS Google authorization and callback/session
acceptance test. Unit tests stub Firebase; this PR does not claim a
completed live OAuth round trip.

仅需 web 部署。No backend changes or auth-domain configuration changes.
```

### PR Body

```
## Summary

修复 webapp 在 iOS 上的 Google 登录路径：登录表单挂载时等待 Firebase `authStateReady()`，准备完成后才启用 Google 按钮；iPhone/iPad 改用直接由点击触发的 popup。准备失败时显示提示，邮箱与手机登录继续可用。

Prepare Firebase before enabling Google sign-in and use the existing popup/token-exchange flow on iOS. Apply the readiness state to the default, landing, and legacy Platform login forms. Preserve Android redirect behavior and existing session-reset/profile-persistence safeguards.

## Root cause

当前 webapp 将 iOS 导向 `signInWithRedirect`，该流程可能受 Safari 的跨域存储限制影响。直接切换 popup 仍需处理首次初始化耗时：Firebase 在 Safari 上会提前初始化 popup resolver，等待这一步完成后再允许点击，可以避免初始化消耗点击的 transient user activation。点击 handler 内不再等待准备过程。

The existing mobile branch sends iOS through Firebase redirect sign-in, which is sensitive to third-party storage restrictions. This adopts the preparation approach from Finn's #3974: finish Firebase startup before the click, then invoke `signInWithPopup` directly from the click handler. Firebase token exchange and profile persistence still use the existing desktop path.

References: #3974 (Platform popup initialization), #3972 (separate first-party auth-domain approach for redirects).

## Test plan

- [x] 231 targeted tests passed across 7 suites: login form, redirect completion, login modal, app-shell auth, standalone login page, landing login modal, and auth manager.
- [x] New preparation and iPhone/iPad popup regression cases failed against the original implementation, then passed with the fix.
- [x] `bash scripts/verify-web.sh --no-test src/components/LoginForm.tsx src/components/login/PlatformLoginFields.tsx src/locales/en.ts src/locales/zh.ts tests/unit/components/LoginForm.unit.spec.tsx` — TypeScript, ESLint, and governance checks passed.
- [x] `git diff --check`.
- [ ] Real-device iOS Google authorization and callback/session acceptance test. Unit tests stub Firebase; this PR does not claim a completed live OAuth round trip.

仅需 web 部署。No backend changes or auth-domain configuration changes.
```

---

## fix(platform): 更新登录视频与首帧，锁定素材交互 (#3982)

- **SHA**: `4184093a8214cd2244f752616aac64ce23e6923f`
- **作者**: david-srp
- **日期**: 2026-10-01T11:13:54Z

### Commit Message

```
fix(platform): 更新登录视频与首帧，锁定素材交互 (#3982)

## 改动概述

替换 Platform 登录页右侧默认视频及兜底首帧，锁定素材交互。仅涉及 `web/platform` 的 4 个文件；不包含此前已合并的
Platform UI 重构。

## 涉及入口与交互

| 页面 / 状态入口 | 本次变化 |
| --- | --- |
| Platform 未登录首页 `/`：Google / 邮箱登录入口旁的右侧展示区 | 替换为用户提供的 Codex App
开发场景视频，改为随前端部署的同源静态资源；静音、循环、内联播放，不显示播放控件。登录按钮和认证流程不变。 |
| 同一登录页的邮箱验证码步骤 | 共用 `LoginVisual`，同步展示新视频及首帧；验证码输入、发送、校验和重发逻辑不变。 |
| 视频尚未加载 / 自动播放被浏览器阻止 | 使用新视频实际首帧作为原生 poster，避免从不同图片切换至视频；首帧压缩为 WebP，约
76 KB。 |
| 视频加载失败 | 回退至同一首帧图片，并更新图片替代文本。 |
| 右侧视频和兜底图的鼠标交互 | 禁止拖拽、文本选择、点击素材和素材区右键菜单；禁用视频画中画及远程播放入口，不影响左侧表单。 |
| 移动端 / 减少动画 / 后台页面 | 保留原有策略：移动端隐藏的展示区不下载视频；减少动画设置下保留首帧；切到后台或移出可视区暂停。 |
| 本地隔离预览 `/__preview/?auth=login` | 复用同一组件，可查看上述变化；无新增生产路由或预览配置改动。 |

## 文件范围

- `web/platform/src/components/login-visual.tsx`：素材引用、兜底图片和交互锁定。
- `web/platform/public/videos/login/platform-codex-login.mp4`：新增约 5
秒、834 × 1112 的 H.264 视频（约 1.43 MB）；移除音轨，保留原视频画质并启用渐进加载。
-
`web/platform/public/images/login/platform-codex-login-poster.webp`：新增视频首帧兜底图。
- `web/platform/src/components/login-visual.test.tsx`：更新素材断言，补充视频 /
兜底图的拖拽及右键拦截验证。

## 验证结果

- [x] 登录素材组件测试：4 项通过。
- [x] Platform lint、生产构建通过。
- [x] 桌面浏览器：视频正常静音播放并推进；点击、拖拽、右键操作不打断播放，未触发素材拖拽。
- [x] 模拟视频错误：正确显示首帧兜底图。
- [x] 移动端：无视频请求，无横向溢出。
- [x] 媒体检查：输出视频仅有视频轨，无音轨。
- [x] `git diff --check` 通过。
- [x] CI 已全部结束，无失败项；Platform、Web、CodeQL 等适用检查通过。两轮自动审查均为低风险通过，无 P0/P1/P2
发现。

## 影响边界

仅修改前端登录展示，不改后端、接口契约、权限、登录认证、支付或余额逻辑；无需后端部署。CI 和审核状态以本 PR 最新结果为准。

请 @tim-srp 审核。
```

### PR Body

```
## 改动概述

替换 Platform 登录页右侧默认视频及兜底首帧，锁定素材交互。仅涉及 `web/platform` 的 4 个文件；不包含此前已合并的 Platform UI 重构。

## 涉及入口与交互

| 页面 / 状态入口 | 本次变化 |
| --- | --- |
| Platform 未登录首页 `/`：Google / 邮箱登录入口旁的右侧展示区 | 替换为用户提供的 Codex App 开发场景视频，改为随前端部署的同源静态资源；静音、循环、内联播放，不显示播放控件。登录按钮和认证流程不变。 |
| 同一登录页的邮箱验证码步骤 | 共用 `LoginVisual`，同步展示新视频及首帧；验证码输入、发送、校验和重发逻辑不变。 |
| 视频尚未加载 / 自动播放被浏览器阻止 | 使用新视频实际首帧作为原生 poster，避免从不同图片切换至视频；首帧压缩为 WebP，约 76 KB。 |
| 视频加载失败 | 回退至同一首帧图片，并更新图片替代文本。 |
| 右侧视频和兜底图的鼠标交互 | 禁止拖拽、文本选择、点击素材和素材区右键菜单；禁用视频画中画及远程播放入口，不影响左侧表单。 |
| 移动端 / 减少动画 / 后台页面 | 保留原有策略：移动端隐藏的展示区不下载视频；减少动画设置下保留首帧；切到后台或移出可视区暂停。 |
| 本地隔离预览 `/__preview/?auth=login` | 复用同一组件，可查看上述变化；无新增生产路由或预览配置改动。 |

## 文件范围

- `web/platform/src/components/login-visual.tsx`：素材引用、兜底图片和交互锁定。
- `web/platform/public/videos/login/platform-codex-login.mp4`：新增约 5 秒、834 × 1112 的 H.264 视频（约 1.43 MB）；移除音轨，保留原视频画质并启用渐进加载。
- `web/platform/public/images/login/platform-codex-login-poster.webp`：新增视频首帧兜底图。
- `web/platform/src/components/login-visual.test.tsx`：更新素材断言，补充视频 / 兜底图的拖拽及右键拦截验证。

## 验证结果

- [x] 登录素材组件测试：4 项通过。
- [x] Platform lint、生产构建通过。
- [x] 桌面浏览器：视频正常静音播放并推进；点击、拖拽、右键操作不打断播放，未触发素材拖拽。
- [x] 模拟视频错误：正确显示首帧兜底图。
- [x] 移动端：无视频请求，无横向溢出。
- [x] 媒体检查：输出视频仅有视频轨，无音轨。
- [x] `git diff --check` 通过。
- [x] CI 已全部结束，无失败项；Platform、Web、CodeQL 等适用检查通过。两轮自动审查均为低风险通过，无 P0/P1/P2 发现。

## 影响边界

仅修改前端登录展示，不改后端、接口契约、权限、登录认证、支付或余额逻辑；无需后端部署。CI 和审核状态以本 PR 最新结果为准。

请 @tim-srp 审核。
```

---

## fix(marketing): 启用官网与 WebApp 的 Managed Agent API 平台入口 (#3981)

- **SHA**: `9ec8efab48eeb573366040b288cf99649a826e9e`
- **作者**: david-srp
- **日期**: 2026-10-01T11:11:42Z

### Commit Message

```
fix(marketing): 启用官网与 WebApp 的 Managed Agent API 平台入口 (#3981)

## 改动说明

Managed Agent API 已在 https://platform.zoowork.ai 上线，但官网仍有入口显示 Coming
soon、无法点击，登录选择菜单也仍禁用该产品。本次启用这些导流入口，并让官网与 WebApp 共用同一个平台地址常量。

基于最新 main（147177be3），包含 Lynn 的 #3968 以及随后首页产品文案调整
#3969；**已覆盖官网前部新增的四产品入口中的 Managed Agent API 卡片**。

## 涉及的全部入口

| 页面位置 | 本次改动 | 跳转方式 |
| --- | --- | --- |
| 官网桌面页头 → Products / 产品 → Managed Agent API | 解除禁用并移除 Coming soon，指向新平台
| 当前标签页 |
| 官网手机导航抽屉 → Products / 产品 → Managed Agent API | 与桌面共用产品配置，同步解除禁用并移除
Coming soon | 当前标签页 |
| 官网首页首屏下方四产品卡片 → Managed Agent API | 启用 Lynn 在 #3968 新增的卡片入口，移除 Coming
soon 和不可点击状态 | 当前标签页 |
| 官网桌面页头 → 开始使用下拉菜单 → Managed Agent API | 将禁用菜单项改为平台外链 | 新标签页 |
| 官网手机导航抽屉 → 开始使用下拉菜单 → Managed Agent API | 通过共享菜单同步启用，点击后执行关闭导航回调 |
新标签页 |
| 官网首页首屏 Hero → Get Started / 开始使用下拉菜单 → Managed Agent API |
通过共享登录菜单启用平台外链 | 新标签页 |
| 官网首页底部 CTA → Get Started / 开始使用下拉菜单 → Managed Agent API |
通过共享登录菜单启用平台外链 | 新标签页 |
| 官网公共页脚 → Product / 产品 → Managed Agent API | 解除禁用并移除 Coming
soon；覆盖首页及复用 MarketingChrome 的营销页面 | 新标签页 |
| 现有 /[locale]/platform/login 页面独立页脚 → Managed Agent API |
StandaloneMarketingFooter 共用页脚配置，同步启用平台外链 | 新标签页 |
| WebApp 用户菜单 → Managed Agent API | 原先已可用且地址正确，本次改为引用统一地址常量，保持现有行为 |
新标签页 |

## 实现与边界

- 新增 `web/app/src/lib/platform-href.ts`，集中维护
`https://platform.zoowork.ai`，由产品配置、页脚配置、登录下拉菜单和 WebApp 用户菜单共用。
- 解除产品配置和页脚中的 `comingSoon` 状态；登录下拉菜单使用真实链接，保留键盘操作、菜单关闭和外链安全属性。
- 外链不拼接 `/zh`、`/en` 等语言前缀，也不携带 WebApp 的登录或 Agent handoff
参数；保留各入口原有的当前页/新标签页策略。
- 官网公共页头、页脚也覆盖 About 等营销页面；**About 页内底部的独立“开始使用”按钮未启用平台下拉菜单，不属于本次改动入口**。
- 现有 `/[locale]/platform/login` 路由及其登录逻辑保持不变，本次只影响其复用的页脚入口。
- 部署范围仅 `web/app`，无需修改或重新部署 `web/platform` 和后端。

## 验证

- [x] 5 个现有相关测试文件、176 项测试通过，覆盖桌面/手机导航、首页产品卡片、首页 CTA、中英文页脚及 WebApp
用户菜单回归。
- [x] 追加核验平台菜单点击关闭行为后，19 项页头测试再次通过。
- [x] TypeScript 类型检查和修改文件 ESLint 通过。
- [x] `verify-web.sh --guards-only` 仓库治理检查通过；`git diff --check` 通过。
- [x] `https://platform.zoowork.ai` 公网 HTTP 检查返回 200。
- [x] 合并预览构建、WebApp 全量测试、静态检查及 CodeQL 已通过；其余适用 CI 均通过。
- [x] Codex、Claude 自动评审均通过；人工评审已请求 @tim-srp。

请求 @tim-srp review。
```

### PR Body

```
## 改动说明

Managed Agent API 已在 https://platform.zoowork.ai 上线，但官网仍有入口显示 Coming soon、无法点击，登录选择菜单也仍禁用该产品。本次启用这些导流入口，并让官网与 WebApp 共用同一个平台地址常量。

基于最新 main（147177be3），包含 Lynn 的 #3968 以及随后首页产品文案调整 #3969；**已覆盖官网前部新增的四产品入口中的 Managed Agent API 卡片**。

## 涉及的全部入口

| 页面位置 | 本次改动 | 跳转方式 |
| --- | --- | --- |
| 官网桌面页头 → Products / 产品 → Managed Agent API | 解除禁用并移除 Coming soon，指向新平台 | 当前标签页 |
| 官网手机导航抽屉 → Products / 产品 → Managed Agent API | 与桌面共用产品配置，同步解除禁用并移除 Coming soon | 当前标签页 |
| 官网首页首屏下方四产品卡片 → Managed Agent API | 启用 Lynn 在 #3968 新增的卡片入口，移除 Coming soon 和不可点击状态 | 当前标签页 |
| 官网桌面页头 → 开始使用下拉菜单 → Managed Agent API | 将禁用菜单项改为平台外链 | 新标签页 |
| 官网手机导航抽屉 → 开始使用下拉菜单 → Managed Agent API | 通过共享菜单同步启用，点击后执行关闭导航回调 | 新标签页 |
| 官网首页首屏 Hero → Get Started / 开始使用下拉菜单 → Managed Agent API | 通过共享登录菜单启用平台外链 | 新标签页 |
| 官网首页底部 CTA → Get Started / 开始使用下拉菜单 → Managed Agent API | 通过共享登录菜单启用平台外链 | 新标签页 |
| 官网公共页脚 → Product / 产品 → Managed Agent API | 解除禁用并移除 Coming soon；覆盖首页及复用 MarketingChrome 的营销页面 | 新标签页 |
| 现有 /[locale]/platform/login 页面独立页脚 → Managed Agent API | StandaloneMarketingFooter 共用页脚配置，同步启用平台外链 | 新标签页 |
| WebApp 用户菜单 → Managed Agent API | 原先已可用且地址正确，本次改为引用统一地址常量，保持现有行为 | 新标签页 |

## 实现与边界

- 新增 `web/app/src/lib/platform-href.ts`，集中维护 `https://platform.zoowork.ai`，由产品配置、页脚配置、登录下拉菜单和 WebApp 用户菜单共用。
- 解除产品配置和页脚中的 `comingSoon` 状态；登录下拉菜单使用真实链接，保留键盘操作、菜单关闭和外链安全属性。
- 外链不拼接 `/zh`、`/en` 等语言前缀，也不携带 WebApp 的登录或 Agent handoff 参数；保留各入口原有的当前页/新标签页策略。
- 官网公共页头、页脚也覆盖 About 等营销页面；**About 页内底部的独立“开始使用”按钮未启用平台下拉菜单，不属于本次改动入口**。
- 现有 `/[locale]/platform/login` 路由及其登录逻辑保持不变，本次只影响其复用的页脚入口。
- 部署范围仅 `web/app`，无需修改或重新部署 `web/platform` 和后端。

## 验证

- [x] 5 个现有相关测试文件、176 项测试通过，覆盖桌面/手机导航、首页产品卡片、首页 CTA、中英文页脚及 WebApp 用户菜单回归。
- [x] 追加核验平台菜单点击关闭行为后，19 项页头测试再次通过。
- [x] TypeScript 类型检查和修改文件 ESLint 通过。
- [x] `verify-web.sh --guards-only` 仓库治理检查通过；`git diff --check` 通过。
- [x] `https://platform.zoowork.ai` 公网 HTTP 检查返回 200。
- [x] 合并预览构建、WebApp 全量测试、静态检查及 CodeQL 已通过；其余适用 CI 均通过。
- [x] Codex、Claude 自动评审均通过；人工评审已请求 @tim-srp。

请求 @tim-srp review。
```

---

## fix(platform): preserve sessions during interrupted restoration (#3979)

- **SHA**: `73cffba7f42e83be29c269cfa8e03d88ca11ef86`
- **作者**: finn-srp
- **日期**: 2026-10-01T10:38:33Z

### Commit Message

```
fix(platform): preserve sessions during interrupted restoration (#3979)

## Summary

Platform currently clears its saved session whenever the account
restoration request rejects. Interrupted refreshes, network failures,
timeouts, and invalid response bodies can therefore send a signed-in
user back to the login page.

Preserve credentials on recoverable failures and show a shared recovery
screen at the original route. Only explicit logout, expiry, or confirmed
Account authentication errors clear the session and private cache.

## Root cause and changes

- Replace the catch-all logout handler with explicit signed-out,
restoring, authenticated, and recovery-error states. Business bootstrap
remains gated until `/user/me` verifies the identity.
- Manage restoration with TanStack Query, forward cancellation to fetch,
time out requests after 8 seconds, and retry network/timeout/5xx
failures once. Manual retries honor browser-readable `Retry-After`
headers.
- Recognize Account's existing authentication `403` detail responses
while preserving unknown `403` errors. Business API permission errors do
not trigger logout.
- Give each in-memory session a non-secret query ID and guard pending
login attempts against logout/unmount. Seed the verified login result to
avoid a duplicate `/user/me` request.
- Extend the shared Account client with optional cancellation and error
metadata while retaining existing call signatures.

Preserve the Console UI and sign-in changes from #3978. The merged login
page keeps the recovery gate; PreviewAuthProvider now implements the
expanded auth contract, and recovery route tests include the new
InterfaceProvider and Account Settings path.

No backend or storage migration is required.

## Test plan

- [x] Node 24: Platform `pnpm lint`, `pnpm typecheck`, `pnpm test` (127
tests), `pnpm build` against the resolved merge with current main.
- [x] Auth client `pnpm test` (48 tests) and `pnpm lint`.
- [x] Main web app `pnpm test:unit` (11,124 passed; 70 skipped; 1 todo).
- [x] Regression coverage for network, cancellation, timeout,
server/response errors, unknown and recognized 403s, expiry, offline
reconnect, rate limiting, StrictMode remounts, and stale
restoration/login results.
- [x] Local Chromium with mocked Account/business endpoints: 25 rapid
reloads while account requests were pending retained credentials and did
not start business bootstrap. Network, timeout, unknown 403, and
Retry-After recovered at the original URL; recognized authentication 403
cleared the session. No live business requests or writes were made.

Deployment and verification against the hosted staging site remain
pending.
```

### PR Body

```
## Summary

Platform currently clears its saved session whenever the account restoration request rejects. Interrupted refreshes, network failures, timeouts, and invalid response bodies can therefore send a signed-in user back to the login page.

Preserve credentials on recoverable failures and show a shared recovery screen at the original route. Only explicit logout, expiry, or confirmed Account authentication errors clear the session and private cache.

## Root cause and changes

- Replace the catch-all logout handler with explicit signed-out, restoring, authenticated, and recovery-error states. Business bootstrap remains gated until `/user/me` verifies the identity.
- Manage restoration with TanStack Query, forward cancellation to fetch, time out requests after 8 seconds, and retry network/timeout/5xx failures once. Manual retries honor browser-readable `Retry-After` headers.
- Recognize Account's existing authentication `403` detail responses while preserving unknown `403` errors. Business API permission errors do not trigger logout.
- Give each in-memory session a non-secret query ID and guard pending login attempts against logout/unmount. Seed the verified login result to avoid a duplicate `/user/me` request.
- Extend the shared Account client with optional cancellation and error metadata while retaining existing call signatures.

Preserve the Console UI and sign-in changes from #3978. The merged login page keeps the recovery gate; PreviewAuthProvider now implements the expanded auth contract, and recovery route tests include the new InterfaceProvider and Account Settings path.

No backend or storage migration is required.

## Test plan

- [x] Node 24: Platform `pnpm lint`, `pnpm typecheck`, `pnpm test` (127 tests), `pnpm build` against the resolved merge with current main.
- [x] Auth client `pnpm test` (48 tests) and `pnpm lint`.
- [x] Main web app `pnpm test:unit` (11,124 passed; 70 skipped; 1 todo).
- [x] Regression coverage for network, cancellation, timeout, server/response errors, unknown and recognized 403s, expiry, offline reconnect, rate limiting, StrictMode remounts, and stale restoration/login results.
- [x] Local Chromium with mocked Account/business endpoints: 25 rapid reloads while account requests were pending retained credentials and did not start business bootstrap. Network, timeout, unknown 403, and Retry-After recovered at the original URL; recognized authentication 403 cleared the session. No live business requests or writes were made.

Deployment and verification against the hosted staging site remain pending.
```

---

## refactor(platform): 统一 Console UI 与登录体验 / align console UI and sign-in (#3978)

- **SHA**: `147177be311c27eb44533d13f50cadab9d3befa8`
- **作者**: david-srp
- **日期**: 2026-10-01T10:14:11Z

### Commit Message

```
refactor(platform): 统一 Console UI 与登录体验 / align console UI and sign-in (#3978)

## 迭代内容
- 对齐 ZooWork System 2.0：统一字体、表格、弹窗、空状态、hover、暗色和移动端样式。
- 精简侧栏：保留 API keys、Usage、Documentation；其余收进 Settings / Organization
settings，个人设置改名 Account，项目切换下拉列表自动加载下一页。
- 优化充值：统一 Add funds 文案，支持预设/自定义金额和即时校验，补齐零余额展示与充值引导。
- 更新登录：Ship your agents 文案、六位验证码交互、静音循环视频及约 59 KB 的真实首帧兜底图。
- 更新品牌：ZooWork Console 标识、深蓝 favicon、ZooWork｜Managed Agents API
标签页标题和外观设置。
- 增加隔离的本地 UI 预览与回归测试，预览入口不进入生产构建；预览主题与 Settings 同步并跨页面保留。
- 修复 tim-srp 提出的 3 处交互问题：账单就绪后才提示零余额充值、首屏尊重保存主题、返回登录上一步保留同邮箱验证码冷却时间。

## 范围与风险
- **未修改任何后端。** 相对 main，仅改动 `web/platform`、前端依赖锁文件及设计文档；API
客户端、数据结构、认证/账单核心逻辑和共享组件实现均未改动。
- 已合入 main 的 #3973，保留登录后账单初始化及失败重试规则；切换 Console / Settings
不重新挂载初始化逻辑，避免重复请求。
- 保留现有权限控制、充值幂等和支付状态轮询；仅需部署 Platform 前端，无数据迁移或新增环境变量。
- `size-override`：本次完整 UI 重构覆盖多个页面，同时包含测试、预览和设计文档，超过 3,000
行常规预算；使用已有行数例外，其他 CI 和代码审查照常执行。

## 验证
- [x] 最新 Platform CI 全量测试：15 个文件、101 项全部通过；本地对应回归测试通过。
- [x] Platform lint、TypeScript 检查、生产构建通过。
- [x] 桌面/移动端登录、验证码、视频兜底、设置导航、零余额和项目切换已在本地预览核验。
- [x] 确认无后端及接口契约变更。
- [x] 最新修复提交 `27a6ebed1` 全部适用 GitHub CI 通过，两套自动复审通过，无未解决 P0/P1/P2。
- [x] CodeQL #666 已核实并记录为误报：固定本地预览路径跳转，不执行 HTML，且不进入生产构建。
- [ ] tim-srp 人工复审（3 条意见已修复，持续跟进）。

未执行真实支付扣款。构建有非阻断性体积提示：主包约 506 KB（gzip 约 152 KB）。
```

### PR Body

```
## 迭代内容
- 对齐 ZooWork System 2.0：统一字体、表格、弹窗、空状态、hover、暗色和移动端样式。
- 精简侧栏：保留 API keys、Usage、Documentation；其余收进 Settings / Organization settings，个人设置改名 Account，项目切换下拉列表自动加载下一页。
- 优化充值：统一 Add funds 文案，支持预设/自定义金额和即时校验，补齐零余额展示与充值引导。
- 更新登录：Ship your agents 文案、六位验证码交互、静音循环视频及约 59 KB 的真实首帧兜底图。
- 更新品牌：ZooWork Console 标识、深蓝 favicon、ZooWork｜Managed Agents API 标签页标题和外观设置。
- 增加隔离的本地 UI 预览与回归测试，预览入口不进入生产构建；预览主题与 Settings 同步并跨页面保留。
- 修复 tim-srp 提出的 3 处交互问题：账单就绪后才提示零余额充值、首屏尊重保存主题、返回登录上一步保留同邮箱验证码冷却时间。

## 范围与风险
- **未修改任何后端。** 相对 main，仅改动 `web/platform`、前端依赖锁文件及设计文档；API 客户端、数据结构、认证/账单核心逻辑和共享组件实现均未改动。
- 已合入 main 的 #3973，保留登录后账单初始化及失败重试规则；切换 Console / Settings 不重新挂载初始化逻辑，避免重复请求。
- 保留现有权限控制、充值幂等和支付状态轮询；仅需部署 Platform 前端，无数据迁移或新增环境变量。
- `size-override`：本次完整 UI 重构覆盖多个页面，同时包含测试、预览和设计文档，超过 3,000 行常规预算；使用已有行数例外，其他 CI 和代码审查照常执行。

## 验证
- [x] 最新 Platform CI 全量测试：15 个文件、101 项全部通过；本地对应回归测试通过。
- [x] Platform lint、TypeScript 检查、生产构建通过。
- [x] 桌面/移动端登录、验证码、视频兜底、设置导航、零余额和项目切换已在本地预览核验。
- [x] 确认无后端及接口契约变更。
- [x] 最新修复提交 `27a6ebed1` 全部适用 GitHub CI 通过，两套自动复审通过，无未解决 P0/P1/P2。
- [x] CodeQL #666 已核实并记录为误报：固定本地预览路径跳转，不执行 HTML，且不进入生产构建。
- [x] tim-srp 已批准 `27a6ebed1`，确认 3 条意见已修复，未发现新的实质回归（人工复审未独立运行测试）。

未执行真实支付扣款。构建有非阻断性体积提示：主包约 506 KB（gzip 约 152 KB）。
```

---

## feat(platform): enable agent-scoped webhooks for Project keys (#3976)

- **SHA**: `e8a0e5f596baedd6f33ab84d6b4a86a10ce7f103`
- **作者**: finn-srp
- **日期**: 2026-10-01T09:24:53Z

### Commit Message

```
feat(platform): enable agent-scoped webhooks for Project keys (#3976)

Platform Project keys currently return 404 for every Agent webhook
route, even when they can manage the same Agent through the runtime API.
Allow the existing Agent-scoped webhook routes after the existing
organization, explicit project (including default), and owner checks.
Work owner/Agent routes stay available; Platform owner/project-wide
registration remains unavailable.

Also strip caller `project_id` alongside `org_id`/`owner_uid`. Engine
selects owner versus project creation from the query, so forwarding a
caller project selector could change the Work owner route's scope.
Engine continues to validate body scope and endpoint/event/delivery
scope.

Keep Work idempotency hashes byte-compatible. Platform hashes add a
credential-family/project namespace and remain stable across key
rotation. Existing POST update/delete aliases and `Cache-Control:
no-store` are retained. Update the service spec and API documentation.
The receiver guidance explicitly requires durable enqueue before ACK, as
already required by #3975; this is an intentional documentation
correction.

Validation:
- 195 targeted webhook, Platform Agent runtime, and service proxy tests
passed.
- Ruff, Pyright, import-linter and applicable pre-commit checks passed.
The legacy GitHub-login suffix hook was skipped because this workspace
explicitly requires Finn's verified `finn930` account; commit author is
`finn-srp <finn@srp.one>`.
- `ecap-verify-py-ci` on final commit `7517de0f0`: Linux dependency
resolution, static checks, all ci-lint guards and both duplication
checks passed; 13,438 tests passed, 5 skipped, coverage 89.92% (CI
threshold 89.5%).

All applicable GitHub checks passed, including backend tests/static
checks, duplication checks and CodeQL. Codex and Claude reviews both
approved with no actionable findings.

Refs #3975 and #3786. This PR delivers the backend portion only. SDK
management helpers remain tracked in TypeScript #34/Python #5; public
bilingual docs/Coding Skill and an authorized staging receiver smoke
remain follow-ups. No Engine flags, deployments or live webhook tests
were performed.
```

### PR Body

```
Platform Project keys currently return 404 for every Agent webhook route, even when they can manage the same Agent through the runtime API. Allow the existing Agent-scoped webhook routes after the existing organization, explicit project (including default), and owner checks. Work owner/Agent routes stay available; Platform owner/project-wide registration remains unavailable.

Also strip caller `project_id` alongside `org_id`/`owner_uid`. Engine selects owner versus project creation from the query, so forwarding a caller project selector could change the Work owner route's scope. Engine continues to validate body scope and endpoint/event/delivery scope.

Keep Work idempotency hashes byte-compatible. Platform hashes add a credential-family/project namespace and remain stable across key rotation. Existing POST update/delete aliases and `Cache-Control: no-store` are retained. Update the service spec and API documentation. The receiver guidance explicitly requires durable enqueue before ACK, as already required by #3975; this is an intentional documentation correction.

Validation:
- 195 targeted webhook, Platform Agent runtime, and service proxy tests passed.
- Ruff, Pyright, import-linter and applicable pre-commit checks passed. The legacy GitHub-login suffix hook was skipped because this workspace explicitly requires Finn's verified `finn930` account; commit author is `finn-srp <finn@srp.one>`.
- `ecap-verify-py-ci` on final commit `7517de0f0`: Linux dependency resolution, static checks, all ci-lint guards and both duplication checks passed; 13,438 tests passed, 5 skipped, coverage 89.92% (CI threshold 89.5%).

All applicable GitHub checks passed, including backend tests/static checks, duplication checks and CodeQL. Codex and Claude reviews both approved with no actionable findings.

Refs #3975 and #3786. This PR delivers the backend portion only. SDK management helpers remain tracked in TypeScript #34/Python #5; public bilingual docs/Coding Skill and an authorized staging receiver smoke remain follow-ups. No Engine flags, deployments or live webhook tests were performed.
```

---

## fix(platform): initialize organization billing after login (#3973)

- **SHA**: `27184baa732470236e4a86931e9360100cac31da`
- **作者**: finn-srp
- **日期**: 2026-10-01T06:07:30Z

### Commit Message

```
fix(platform): initialize organization billing after login (#3973)

## Summary

Platform now initializes an uninitialized Organization wallet after
authenticated bootstrap, using the existing `POST
/platform/v1/billing/initialize`. Users can create API keys without
first starting a top-up. Initialization runs alongside the shell:
navigation, existing API keys, Projects, Account and payment history
remain accessible during setup or a billing outage. Failures retain the
login session, show the returned error inside the page, and offer
explicit Retry. API key creation uses its existing permissions and does
not depend on billing reads or initialization. Only top-ups wait for
initialized billing; existing keys can still be revoked. Existing
wallets are reused and their actual balance is displayed.

The change is entirely in `web/platform`. Only the Platform frontend
needs deployment; there are no new environment variables. Agent
creation, Engine forwarding, server authentication and consumption-time
balance enforcement are unchanged from main. Setup creates no credits,
payment order, Stripe Checkout or promotional reservation.

## Root cause

Wallet initialization currently happens when starting a top-up. A user
who has only signed in can therefore receive `409
platform.billing_not_ready` from SDK Agent creation because the
Organization has no billing association.

The frontend reads billing status and initializes only when it is
explicitly `uninitialized` and the user has billing-management
permission. It makes one automatic initialization POST per page session,
including React StrictMode. A failed initialization POST requires
explicit Retry: query refetches and network reconnects cannot retry it
automatically.

Billing GET recovery is separate from retrying a failed initialization
POST. While GET is failing, the frontend does not infer a missing wallet
or initialize. GET may recover through manual Retry or automatic
network-reconnect refetch. If it then explicitly returns `uninitialized`
and no initialization POST has been attempted, the first automatic
initialization is allowed. This recovery is intentional. Window-focus
refetch is already disabled globally in `AppProviders`; `retryOnMount:
false` only prevents route mounts from restarting a failed GET.

Members without billing permission neither read nor initialize billing.
`failed` and `manual_review` states show explicit setup messages;
neither is automatically retried, and manual review directs the user to
support. The current backend actually returns only `uninitialized` or
`ready` from GET, and success or HTTP errors from initialization; the
extra state handling preserves the existing public schema.

## Test plan

- [x] Node 24: `pnpm lint`, `pnpm typecheck`, `pnpm test` (48 tests),
and `pnpm build`.
- [x] StrictMode coverage for one automatic initialization, zero-balance
display, explicit Retry after failure, existing-wallet reuse, and
unchanged Checkout behavior.
- [x] Degraded-mode coverage for pending billing reads/setup, API key
creation during billing failures (including failed reads before and
after a ready wallet and navigation), existing key visibility/revocation
availability, payment history and navigation after setup failure,
billing-read recovery, members without billing permission, and
failed/manual-review statuses.
- [x] Real focus/reconnect events through TanStack Query: focus does not
refetch billing; reconnect permits the first initialization after GET
recovery but never automatically retries a failed initialization POST.
- [x] Merged latest main, preserving the Organization Usage page and
branding changes. Final diff contains only eight files under
`web/platform`; no backend or dependency changes.
- [ ] Staging login and SDK consumption verification after frontend
deployment.

Supersedes #3971 with a frontend-only change.
```

### PR Body

```
## Summary

Platform now initializes an uninitialized Organization wallet after authenticated bootstrap, using the existing `POST /platform/v1/billing/initialize`. Users can create API keys without first starting a top-up. Initialization runs alongside the shell: navigation, existing API keys, Projects, Account and payment history remain accessible during setup or a billing outage. Failures retain the login session, show the returned error inside the page, and offer explicit Retry. API key creation uses its existing permissions and does not depend on billing reads or initialization. Only top-ups wait for initialized billing; existing keys can still be revoked. Existing wallets are reused and their actual balance is displayed.

The change is entirely in `web/platform`. Only the Platform frontend needs deployment; there are no new environment variables. Agent creation, Engine forwarding, server authentication and consumption-time balance enforcement are unchanged from main. Setup creates no credits, payment order, Stripe Checkout or promotional reservation.

## Root cause

Wallet initialization currently happens when starting a top-up. A user who has only signed in can therefore receive `409 platform.billing_not_ready` from SDK Agent creation because the Organization has no billing association.

The frontend reads billing status and initializes only when it is explicitly `uninitialized` and the user has billing-management permission. It makes one automatic initialization POST per page session, including React StrictMode. A failed initialization POST requires explicit Retry: query refetches and network reconnects cannot retry it automatically.

Billing GET recovery is separate from retrying a failed initialization POST. While GET is failing, the frontend does not infer a missing wallet or initialize. GET may recover through manual Retry or automatic network-reconnect refetch. If it then explicitly returns `uninitialized` and no initialization POST has been attempted, the first automatic initialization is allowed. This recovery is intentional. Window-focus refetch is already disabled globally in `AppProviders`; `retryOnMount: false` only prevents route mounts from restarting a failed GET.

Members without billing permission neither read nor initialize billing. `failed` and `manual_review` states show explicit setup messages; neither is automatically retried, and manual review directs the user to support. The current backend actually returns only `uninitialized` or `ready` from GET, and success or HTTP errors from initialization; the extra state handling preserves the existing public schema.

## Test plan

- [x] Node 24: `pnpm lint`, `pnpm typecheck`, `pnpm test` (48 tests), and `pnpm build`.
- [x] StrictMode coverage for one automatic initialization, zero-balance display, explicit Retry after failure, existing-wallet reuse, and unchanged Checkout behavior.
- [x] Degraded-mode coverage for pending billing reads/setup, API key creation during billing failures (including failed reads before and after a ready wallet and navigation), existing key visibility/revocation availability, payment history and navigation after setup failure, billing-read recovery, members without billing permission, and failed/manual-review statuses.
- [x] Real focus/reconnect events through TanStack Query: focus does not refetch billing; reconnect permits the first initialization after GET recovery but never automatically retries a failed initialization POST.
- [x] Merged latest main, preserving the Organization Usage page and branding changes. Final diff contains only eight files under `web/platform`; no backend or dependency changes.
- [ ] Staging login and SDK consumption verification after frontend deployment.

Supersedes #3971 with a frontend-only change.
```

---

## feat(platform): expose organization usage and update branding (#3970)

- **SHA**: `7f1deae1e938df1541c3fe4154f6794f5693e5c5`
- **作者**: finn-srp
- **日期**: 2026-10-01T03:48:13Z

### Commit Message

```
feat(platform): expose organization usage and update branding (#3970)

## Summary

Platform Usage was deferred and tied to the selected Project even though
the available Usage API reports the entire Organization. Expose one
top-level Organization Usage page using the existing read-only API;
switching the active Project leaves Usage unchanged.

- Show complete snapshot spend in USD, model/tool calls, and
cursor-paged activity for rolling 24h/7d/30d ranges. Preserve snapshot
and as_of across pages; refresh starts a new snapshot.
- Keep All projects fixed and show a concise “Filter unavailable”
notice. Preserve shared/unattributed costs and distinguish errors,
permissions, billing readiness, and verified zero usage without
initializing billing.
- Replace the sidebar and sign-in branding with the supplied ZooWork
logo, including narrow-screen and dark-mode styling.

Frontend only; no service, API contract, or deployment changes. Future
Project attribution/filtering remains tracked in
https://github.com/SerendipityOneInc/ecap-workspace/issues/3958 (this PR
does not close it). Activity loads 50 rows at a time; loaded rows remain
in the DOM.

## Test plan

- [x] Rebased onto current main, then ran Node 24 `pnpm lint`, `pnpm
typecheck`, `pnpm test` (37 passed), and `pnpm build` in `web/platform`.
- [x] MSW coverage for Organization scope independent of Project
selection, snapshot pagination/refresh/expiry, time ranges, shared
costs, incomplete totals, errors, permission denial, billing readiness,
and zero usage.
- [x] Desktop and mobile visual checks; synthetic 2,000-record preview
and long model/session strings render without outer horizontal overflow.
- [x] Local dev connects to the existing staging API. Fixture stress
preview is gitignored and excluded from the shipped entry point.
```

### PR Body

```
## Summary

Platform Usage was deferred and tied to the selected Project even though the available Usage API reports the entire Organization. Expose one top-level Organization Usage page using the existing read-only API; switching the active Project leaves Usage unchanged.

- Show complete snapshot spend in USD, model/tool calls, and cursor-paged activity for rolling 24h/7d/30d ranges. Preserve snapshot and as_of across pages; refresh starts a new snapshot.
- Keep All projects fixed and show a concise “Filter unavailable” notice. Preserve shared/unattributed costs and distinguish errors, permissions, billing readiness, and verified zero usage without initializing billing.
- Replace the sidebar and sign-in branding with the supplied ZooWork logo, including narrow-screen and dark-mode styling.

Frontend only; no service, API contract, or deployment changes. Future Project attribution/filtering remains tracked in https://github.com/SerendipityOneInc/ecap-workspace/issues/3958 (this PR does not close it). Activity loads 50 rows at a time; loaded rows remain in the DOM.

## Test plan

- [x] Rebased onto current main, then ran Node 24 `pnpm lint`, `pnpm typecheck`, `pnpm test` (37 passed), and `pnpm build` in `web/platform`.
- [x] MSW coverage for Organization scope independent of Project selection, snapshot pagination/refresh/expiry, time ranges, shared costs, incomplete totals, errors, permission denial, billing readiness, and zero usage.
- [x] Desktop and mobile visual checks; synthetic 2,000-record preview and long model/session strings render without outer horizontal overflow.
- [x] Local dev connects to the existing staging API. Fixture stress preview is gitignored and excluded from the shipped entry point.
```

---

## fix(marketing): update homepage product copy (#3969)

- **SHA**: `8d707fd3625c00575a00d7a32ffb0b1fbc550681`
- **作者**: ericma-srp
- **日期**: 2026-10-01T02:37:47Z

### Commit Message

```
fix(marketing): update homepage product copy (#3969)

## Summary
- Rename the shared Get Started dropdown entry from `Agent Builder` to
`ZooWork.ai`.
- Update the third homepage product card to `Enterprise AI Stack` and
`Deploy, govern, and scale AI across your organization.` Keep the
existing Enterprise navigation label and all destinations unchanged.
- Synchronize the description across all 10 locale dictionaries and
update existing homepage expectations. Frontend only; no backend
changes.

## Test plan
- [x] Synced local main and based the branch on `1ba301d89`.
- [x] Existing header, homepage and locale dictionary suites: 114 tests
passed (including desktop login, handoff parameters and mobile drawer
behavior).
- [x] Changed-surface pre-push verification: governance guards,
TypeScript, full frontend ESLint passed.
- [x] Local Edge browser verified desktop and mobile dropdown/product
card copy; no mobile horizontal overflow or page errors.
- [x] `git diff --check`.
- Local preview: `http://localhost:3020/` (preview-only Firebase
configuration; authentication is outside this copy-change validation).
```

### PR Body

```
## Summary
- Rename the shared Get Started dropdown entry from `Agent Builder` to `ZooWork.ai`.
- Update the third homepage product card to `Enterprise AI Stack` and `Deploy, govern, and scale AI across your organization.` Keep the existing Enterprise navigation label and all destinations unchanged.
- Synchronize the description across all 10 locale dictionaries and update existing homepage expectations. Frontend only; no backend changes.

## Test plan
- [x] Synced local main and based the branch on `1ba301d89`.
- [x] Existing header, homepage and locale dictionary suites: 114 tests passed (including desktop login, handoff parameters and mobile drawer behavior).
- [x] Changed-surface pre-push verification: governance guards, TypeScript, full frontend ESLint passed.
- [x] Local Edge browser verified desktop and mobile dropdown/product card copy; no mobile horizontal overflow or page errors.
- [x] `git diff --check`.
- Local preview: `http://localhost:3020/` (preview-only Firebase configuration; authentication is outside this copy-change validation).
```

---

## ci(platform): deploy production from release tags (#3959)

- **SHA**: `1ba301d89cdce12231ffbf2c938a1bbb1c2f84ee`
- **作者**: finn-srp
- **日期**: 2026-10-01T01:33:49Z

### Commit Message

```
ci(platform): deploy production from release tags (#3959)

## Summary

Platform currently has staging beta tags but no production tag trigger.
Add `platform-v<major>.<minor>.<patch>-release` so pushing a reviewed
release tag builds with the production GitHub Environment and deploys
the `zoowork-platform` Worker.

Main and beta tags continue deploying staging. Explicit manual
environment selection takes precedence over tag names. An
environment-free setup job validates the trigger and outputs the
deployment environment before the deploy job requests any GitHub
Environment. Deployment names and concurrency match that selection.
Document the independent frontend release and prerequisite backend
releases.

## Test plan

- Node 24, on the final commit after rebasing onto `origin/main`: `pnpm
lint`, `pnpm typecheck`, `pnpm test` (27 passed), `pnpm build`.
- Parsed workflow YAML and executed the setup job Bash without a
checkout for main, beta, release, default/manual production, and manual
staging on a release tag; checked that run names and concurrency match
the resolved environment.
- Rejected malformed, wrong-prefix and shell-content tags and invalid
manual environments without producing a deployment output. Verified that
setup has no Environment or checkout-dependent working directory,
deployment depends on setup, and checkout precedes deployment shell
steps.
- `git diff --check` passed.

Production readiness: user-interface `v0.6.17-release` already includes
Platform login. Its MCP token scope change #164 is being reverted
separately and is not a dependency of this Platform/SDK release.
claw-interface `service-v0.18.24-release` includes the current Platform
runtime/billing changes. This PR does not itself trigger production
deployment; merging it triggers staging.

The repository's existing production Environment requires approval by a
configured reviewer. Release tags trigger the workflow; deployment
proceeds after that existing approval. No Environment protection
settings are changed.
```

### PR Body

```
## Summary

Platform currently has staging beta tags but no production tag trigger. Add `platform-v<major>.<minor>.<patch>-release` so pushing a reviewed release tag builds with the production GitHub Environment and deploys the `zoowork-platform` Worker.

Main and beta tags continue deploying staging. Explicit manual environment selection takes precedence over tag names. An environment-free setup job validates the trigger and outputs the deployment environment before the deploy job requests any GitHub Environment. Deployment names and concurrency match that selection. Document the independent frontend release and prerequisite backend releases.

## Test plan

- Node 24, on the final commit after rebasing onto `origin/main`: `pnpm lint`, `pnpm typecheck`, `pnpm test` (27 passed), `pnpm build`.
- Parsed workflow YAML and executed the setup job Bash without a checkout for main, beta, release, default/manual production, and manual staging on a release tag; checked that run names and concurrency match the resolved environment.
- Rejected malformed, wrong-prefix and shell-content tags and invalid manual environments without producing a deployment output. Verified that setup has no Environment or checkout-dependent working directory, deployment depends on setup, and checkout precedes deployment shell steps.
- `git diff --check` passed.

Production readiness: user-interface `v0.6.17-release` already includes Platform login. Its MCP token scope change #164 is being reverted separately and is not a dependency of this Platform/SDK release. claw-interface `service-v0.18.24-release` includes the current Platform runtime/billing changes. This PR does not itself trigger production deployment; merging it triggers staging.

The repository's existing production Environment requires approval by a configured reviewer. Release tags trigger the workflow; deployment proceeds after that existing approval. No Environment protection settings are changed.
```

---

## fix(agents): 接通个人技能上传并优化弹窗交互 (#3966)

- **SHA**: `a1bdaf226399ecd69fa6fc02c52a9ba5f649687b`
- **作者**: lynn Zhuang
- **日期**: 2026-10-01T00:31:26Z

### Commit Message

```
fix(agents): 接通个人技能上传并优化弹窗交互 (#3966)

## 概要

Agent 编辑页原来的个人 Skill 上传弹窗只提供文件选择，Upload 按钮始终禁用。现在选择有效 ZIP
后可上传到个人技能库，并将文本文件加入当前 Agent 草稿；点击 Save 后提交为新版本。

- 接入已有 `POST /skills` 接口，上传后刷新技能库缓存；保留当前 Agent 的其他未保存修改。
- 个人库已存在同名技能时复用其条目，通过 `POST /skills/{id}/versions` 上传新版本；支持相同技能包用于多个
Agent，本地 mock 同步拒绝重复创建同名条目。
- 补充 ZIP、`SKILL.md`、文件路径、UTF-8、解压大小及保存操作数校验；禁止覆盖同名技能，失败时保留文件并支持重试。
- 源码大小预检覆盖完整文件集，包括依赖、运行配置、连接、评估及只读引用；上传已成功但 Agent 暂存失败时，重试复用上传结果，避免重复注册。
- 上传前通过新增的只读 `GET /agents/{workspace_id}/skills/binding-names` 检查当前
Agent 的可绑定名称，直接复用后端基线继承筛选规则：保留因缺少配置而暂不可用的
Skill，排除禁用、被替代等条目；重名或查询失败时停止注册。聊天菜单继续使用原来的可用技能列表。
- 改为紧凑的单文件弹窗，使用技能库同款闪电 thumbnail、浅灰文件卡片及独立浅色图标背景；更换文件有下划线，更换/移除使用一致的
hover 背景。
- 文件卡片和 Upload 按钮展示上传中 loading，期间禁用文件操作与重复提交；设置冲突期间禁用 Skill
编辑/上传，上传途中出现冲突时保留成功结果，恢复后重试不重复写入技能库；移除 Agent 设置顶部撤销按钮。
- 编辑页现有更多菜单提供“丢弃未保存修改”，恢复普通草稿的名称、模型、Instructions 和 Skills，同时保留顶部 Undo
按钮移除的设计；待应用资源变更单独提供“丢弃未生效的修改”恢复入口，调用原有服务端撤销流程。上传提示明确文本包的文件数和完整源码大小限制。
- 修正本地 mock：技能名称取自 ZIP 内 `SKILL.md`，不再取 ZIP 文件名；保存技能文件时保留旧版本快照。

## 根因

上传弹窗原先是预览 UI，没有绑定提交回调且按钮写死为禁用。接通后，本地 mock 又将 ZIP 文件名误当作技能名，导致文件名与
frontmatter 名称不同的有效技能包被误报失败。

## 验证

- [x] 本轮 5 个前端测试文件、73 项测试及 2 个后端测试文件、33
项测试通过，覆盖暂不可用基线的重名拦截、禁用/被替代条目排除、首次源码技能继承、所有者权限、检查失败、独立缓存及 mock
契约。追加冲突修复复跑 5 个前端测试文件、68 项测试，覆盖冲突前的写入阻止、异步途中发生冲突、恢复后的缓存重试和 UI
禁用。普通草稿丢弃入口另有 4 个相关文件、55 项回归通过，验证真实草稿恢复、dirty 状态清除及保存/冲突保护。完整 CI
暴露的两份历史面板测试已补齐 ViewModel 的草稿、头像上传和删除状态，整个 Agent 单测目录 64 个文件、517
项测试通过；未改动生产逻辑或原有测试断言。前序上传、失败重试、文件操作、loading、草稿保存、ZIP 校验和容量预检回归已通过。
- [x] 前端治理 guards、TypeScript、ESLint 通过；后端 Ruff、格式、Pyright 和 8
项架构导入契约通过；提交及推送执行仓库 hooks。
- [x] 本地 mock 浏览器验证：`beauty htmlskill.zip` 识别为 `ppt-beautify`，8
个文件完整上传并保存，刷新后保留。
- [x] 浏览器验证 loading 图标、上传期间操作禁用、两个按钮的 hover、thumbnail 背景，以及顶部撤销按钮移除。

- [x] 最新提交 `89ba1b065` 的完整 CI 已通过：前端 881 个测试文件、11090 项测试通过（70 项跳过、1 项
todo），前端构建、后端完整测试、类型/质量检查及 CodeQL 均通过，无 pending/失败项、无未关闭的 PR CodeQL 告警。
- [x] 最新提交的 [Codex
review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3966#pullrequestreview-5371612790)
和 [Claude
review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3966#issuecomment-5919104500)
结论均为 APPROVE，零 P0/P1/P2。

## 范围与限制

涉及 web/app、本地 mock 及 claw-interface
的只读检查接口；个人技能上传仍使用已有接口。发布时需要同时发布前后端，先发布后端以提供新增检查接口。未改变数据库查询形式或写入流程。Agent
设置当前以文本源码保存技能，本入口一次上传一个包含 `SKILL.md` 的 UTF-8 文本技能包；二进制附件、与当前 Agent
绑定技能重名及超过源码/提交限制的包会明确提示。线上效果需前端发布后生效，尚未对 staging/production 进行实际上传验证。
```

### PR Body

```
## 概要

Agent 编辑页原来的个人 Skill 上传弹窗只提供文件选择，Upload 按钮始终禁用。现在选择有效 ZIP 后可上传到个人技能库，并将文本文件加入当前 Agent 草稿；点击 Save 后提交为新版本。

- 接入已有 `POST /skills` 接口，上传后刷新技能库缓存；保留当前 Agent 的其他未保存修改。
- 个人库已存在同名技能时复用其条目，通过 `POST /skills/{id}/versions` 上传新版本；支持相同技能包用于多个 Agent，本地 mock 同步拒绝重复创建同名条目。
- 补充 ZIP、`SKILL.md`、文件路径、UTF-8、解压大小及保存操作数校验；禁止覆盖同名技能，失败时保留文件并支持重试。
- 源码大小预检覆盖完整文件集，包括依赖、运行配置、连接、评估及只读引用；上传已成功但 Agent 暂存失败时，重试复用上传结果，避免重复注册。
- 上传前通过新增的只读 `GET /agents/{workspace_id}/skills/binding-names` 检查当前 Agent 的可绑定名称，直接复用后端基线继承筛选规则：保留因缺少配置而暂不可用的 Skill，排除禁用、被替代等条目；重名或查询失败时停止注册。聊天菜单继续使用原来的可用技能列表。
- 改为紧凑的单文件弹窗，使用技能库同款闪电 thumbnail、浅灰文件卡片及独立浅色图标背景；更换文件有下划线，更换/移除使用一致的 hover 背景。
- 文件卡片和 Upload 按钮展示上传中 loading，期间禁用文件操作与重复提交；设置冲突期间禁用 Skill 编辑/上传，上传途中出现冲突时保留成功结果，恢复后重试不重复写入技能库；移除 Agent 设置顶部撤销按钮。
- 编辑页现有更多菜单提供“丢弃未保存修改”，恢复普通草稿的名称、模型、Instructions 和 Skills，同时保留顶部 Undo 按钮移除的设计；待应用资源变更单独提供“丢弃未生效的修改”恢复入口，调用原有服务端撤销流程。上传提示明确文本包的文件数和完整源码大小限制。
- 修正本地 mock：技能名称取自 ZIP 内 `SKILL.md`，不再取 ZIP 文件名；保存技能文件时保留旧版本快照。

## 根因

上传弹窗原先是预览 UI，没有绑定提交回调且按钮写死为禁用。接通后，本地 mock 又将 ZIP 文件名误当作技能名，导致文件名与 frontmatter 名称不同的有效技能包被误报失败。

## 验证

- [x] 本轮 5 个前端测试文件、73 项测试及 2 个后端测试文件、33 项测试通过，覆盖暂不可用基线的重名拦截、禁用/被替代条目排除、首次源码技能继承、所有者权限、检查失败、独立缓存及 mock 契约。追加冲突修复复跑 5 个前端测试文件、68 项测试，覆盖冲突前的写入阻止、异步途中发生冲突、恢复后的缓存重试和 UI 禁用。普通草稿丢弃入口另有 4 个相关文件、55 项回归通过，验证真实草稿恢复、dirty 状态清除及保存/冲突保护。完整 CI 暴露的两份历史面板测试已补齐 ViewModel 的草稿、头像上传和删除状态，整个 Agent 单测目录 64 个文件、517 项测试通过；未改动生产逻辑或原有测试断言。前序上传、失败重试、文件操作、loading、草稿保存、ZIP 校验和容量预检回归已通过。
- [x] 前端治理 guards、TypeScript、ESLint 通过；后端 Ruff、格式、Pyright 和 8 项架构导入契约通过；提交及推送执行仓库 hooks。
- [x] 本地 mock 浏览器验证：`beauty htmlskill.zip` 识别为 `ppt-beautify`，8 个文件完整上传并保存，刷新后保留。
- [x] 浏览器验证 loading 图标、上传期间操作禁用、两个按钮的 hover、thumbnail 背景，以及顶部撤销按钮移除。

- [x] 最新提交 `89ba1b065` 的完整 CI 已通过：前端 881 个测试文件、11090 项测试通过（70 项跳过、1 项 todo），前端构建、后端完整测试、类型/质量检查及 CodeQL 均通过，无 pending/失败项、无未关闭的 PR CodeQL 告警。
- [x] 最新提交的 [Codex review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3966#pullrequestreview-5371612790) 和 [Claude review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3966#issuecomment-5919104500) 结论均为 APPROVE，零 P0/P1/P2。

## 范围与限制

涉及 web/app、本地 mock 及 claw-interface 的只读检查接口；个人技能上传仍使用已有接口。发布时需要同时发布前后端，先发布后端以提供新增检查接口。未改变数据库查询形式或写入流程。Agent 设置当前以文本源码保存技能，本入口一次上传一个包含 `SKILL.md` 的 UTF-8 文本技能包；二进制附件、与当前 Agent 绑定技能重名及超过源码/提交限制的包会明确提示。线上效果需前端发布后生效，尚未对 staging/production 进行实际上传验证。
```

---

## feat(landing): 更新官网产品导航、页芯对齐和移动端适配 (#3968)

- **SHA**: `69054215659574912a0d9e2ac985eeab11133f31`
- **作者**: lynn Zhuang
- **日期**: 2026-10-01T00:28:46Z

### Commit Message

```
feat(landing): 更新官网产品导航、页芯对齐和移动端适配 (#3968)

## 变更说明

官网原先缺少集中的产品入口，移动端导航不可发现，各区块左右边界也不一致。本次按设计稿统一页芯，并补齐产品导航和手机访问体验。

- 首屏下方增加 Agent Builder、Managed Agent API（Coming soon）、Enterprise、ZooData
四个产品卡片，包含标题、描述和对应产品的线条动效插画。卡片采用浅灰背景，移除跳转箭头。
- 新增 Products 下拉，复用 iOS App 弹窗入口；Resources 移除重复的 ZooData，并统一 hover
展开。桌面下拉面板平滑切换，保留原来的箭头方向表现。
- Header、首屏界面图、产品区和后续正文、页脚统一为 1176px 最大内容宽度；首屏背景全宽，增加背景视差，界面图仍保持对齐。
- 手机 Header 使用无边框图标菜单，导航支持触控展开；Get Started 放入菜单，保留首屏 CTA。菜单支持滚动、关闭后焦点恢复及
RTL；七天试点流程适配窄屏。
- 按 Figma 更新共用的移动 App 弹窗，官网与登录后的 Profile 面板共用。桌面以扫码为主，手机保留直接前往 App Store
的下载按钮。
- 两处 Get Started 下拉的产品名称统一为 Agent Builder；未登录访问 `/home` 跳转至
`/login`，等待服务端 `/account/me` 校验后再判断会话，支持仅有 HttpOnly
Cookie、尚未恢复本地缓存的登录用户；临时失败保留重试入口。
- 产品菜单与卡片的站内链接保留当前域名和语言，App 路由通过现有语言 Cookie 传递选择；Resources 在 hover
后点击仍保持展开，键盘与触控可切换。
- Products 导航、产品卡片以及 Home 匿名/失效会话拦截使用独立的认证归因，更新 GA4 调用点登记；由现有登录表单发送 Flow
事件，避免计入首屏 CTA 转化。
- 动效尊重减少动态效果设置，手机关闭背景视差。

## 设计参考

-
[页芯与内容对齐](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=1198-3992)
- [iOS App
下载弹窗](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=1185-3310)

## 验证

- Web TypeScript、ESLint、治理检查通过；本地单元测试 11026 项通过（70 项跳过，1 项待办），动效补充后的相关
90 项测试通过；同步最新 main 后，认证、弹窗和导航等 70 项相关测试通过。
- 设计系统 Sheet 的类型检查、Lint 和 6 项单元测试通过。
- Chrome 浏览器检查 320–2560px 共 36 组边界（全部 10 种语言，包含 RTL）：内容对齐、无横向溢出、Header
无重叠。
- 已验证桌面 Products → Solutions → Resources hover 切换、手机导航 → 共用 iOS
弹窗、下载入口、背景视差及减少动态效果模式。
- 已复核首页 46 张图片均正常加载，访客态 `/home` 登录跳转通过。
- Tim review 后补充的相关 120 项测试通过，TypeScript、ESLint 和治理检查通过。浏览器复现 Cookie
登录初始化返回 503、但 `/account/me` 成功的场景：Home 可进入；真实访客仍跳转登录。另验证 Resources hover
后点击、键盘关闭及日文桌面/卡片/手机产品路由。
- 认证归因修复后，相关 280 项测试、TypeScript、ESLint 和治理检查通过；浏览器验证四类登录入口保留各自的
intent/trigger，继续复核 Cookie 登录与匿名拦截行为。
- 本地验证使用 Chrome 设备模拟，未进行实体 iPhone/Safari 验证；完整生产构建由 CI 验证。
- 最终提交 `0b382660c` 的 CI 已完成：24 项通过、14 项按路径规则跳过，无失败；包括完整 Web 单元测试、生产构建和
CodeQL。

## Review

已请求 `tim-srp` 复核；最终提交 `0b382660c` 的 [Codex
review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3968#pullrequestreview-5372289557)
结论为 **APPROVE**，未发现问题，CI 已通过。等待人工审批，尚未合并。
```

### PR Body

```
## 变更说明

官网原先缺少集中的产品入口，移动端导航不可发现，各区块左右边界也不一致。本次按设计稿统一页芯，并补齐产品导航和手机访问体验。

- 首屏下方增加 Agent Builder、Managed Agent API（Coming soon）、Enterprise、ZooData 四个产品卡片，包含标题、描述和对应产品的线条动效插画。卡片采用浅灰背景，移除跳转箭头。
- 新增 Products 下拉，复用 iOS App 弹窗入口；Resources 移除重复的 ZooData，并统一 hover 展开。桌面下拉面板平滑切换，保留原来的箭头方向表现。
- Header、首屏界面图、产品区和后续正文、页脚统一为 1176px 最大内容宽度；首屏背景全宽，增加背景视差，界面图仍保持对齐。
- 手机 Header 使用无边框图标菜单，导航支持触控展开；Get Started 放入菜单，保留首屏 CTA。菜单支持滚动、关闭后焦点恢复及 RTL；七天试点流程适配窄屏。
- 按 Figma 更新共用的移动 App 弹窗，官网与登录后的 Profile 面板共用。桌面以扫码为主，手机保留直接前往 App Store 的下载按钮。
- 两处 Get Started 下拉的产品名称统一为 Agent Builder；未登录访问 `/home` 跳转至 `/login`，等待服务端 `/account/me` 校验后再判断会话，支持仅有 HttpOnly Cookie、尚未恢复本地缓存的登录用户；临时失败保留重试入口。
- 产品菜单与卡片的站内链接保留当前域名和语言，App 路由通过现有语言 Cookie 传递选择；Resources 在 hover 后点击仍保持展开，键盘与触控可切换。
- Products 导航、产品卡片以及 Home 匿名/失效会话拦截使用独立的认证归因，更新 GA4 调用点登记；由现有登录表单发送 Flow 事件，避免计入首屏 CTA 转化。
- 动效尊重减少动态效果设置，手机关闭背景视差。

## 设计参考

- [页芯与内容对齐](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=1198-3992)
- [iOS App 下载弹窗](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=1185-3310)

## 验证

- Web TypeScript、ESLint、治理检查通过；本地单元测试 11026 项通过（70 项跳过，1 项待办），动效补充后的相关 90 项测试通过；同步最新 main 后，认证、弹窗和导航等 70 项相关测试通过。
- 设计系统 Sheet 的类型检查、Lint 和 6 项单元测试通过。
- Chrome 浏览器检查 320–2560px 共 36 组边界（全部 10 种语言，包含 RTL）：内容对齐、无横向溢出、Header 无重叠。
- 已验证桌面 Products → Solutions → Resources hover 切换、手机导航 → 共用 iOS 弹窗、下载入口、背景视差及减少动态效果模式。
- 已复核首页 46 张图片均正常加载，访客态 `/home` 登录跳转通过。
- Tim review 后补充的相关 120 项测试通过，TypeScript、ESLint 和治理检查通过。浏览器复现 Cookie 登录初始化返回 503、但 `/account/me` 成功的场景：Home 可进入；真实访客仍跳转登录。另验证 Resources hover 后点击、键盘关闭及日文桌面/卡片/手机产品路由。
- 认证归因修复后，相关 280 项测试、TypeScript、ESLint 和治理检查通过；浏览器验证四类登录入口保留各自的 intent/trigger，继续复核 Cookie 登录与匿名拦截行为。
- 本地验证使用 Chrome 设备模拟，未进行实体 iPhone/Safari 验证；完整生产构建由 CI 验证。
- 最终提交 `0b382660c` 的 CI 已完成：24 项通过、14 项按路径规则跳过，无失败；包括完整 Web 单元测试、生产构建和 CodeQL。

## Review

已请求 `tim-srp` 复核；最终提交 `0b382660c` 的 [Codex review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3968#pullrequestreview-5372289557) 结论为 **APPROVE**，未发现问题，CI 已通过。等待人工审批，尚未合并。
```

---

