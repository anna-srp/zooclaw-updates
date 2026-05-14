# ecap-workspace Commits — 2026-05-13

仓库: SerendipityOneInc/ecap-workspace  
日期: 2026-05-13 (UTC)  
Commits 数量: 20

---

## Commit 1 — bd058e20

**SHA**: bd058e20  
**PR**: #1616  
**Title**: fix(billing): per-invoice download + Stripe customer reuse + credit-sync wallet sum (ECA-669)

### 完整 Commit Message

```
fix(billing): per-invoice download + Stripe customer reuse + credit-sync wallet sum (ECA-669) (#1616)

## Summary

Closes both halves of ECA-669:

### Half 1 — invoice download "点 24$ 显示 100$"

Two compounding defects:

1. **Stripe customer not reused across checkouts.**
create-checkout-session/route.ts never passed customer= to stripe.checkout.sessions.create,
so Stripe spawned a fresh customer object on every paid checkout. The
checkout.session.completed webhook then overwrote user.stripe_customer_id with the newest one,
orphaning the previous customer (and all its invoices).
2. **Download button had no per-invoice scope.** Each row in InvoiceHistory.tsx called
the same no-arg openCustomerPortal(), which mounts Stripe Billing Portal against
account.stripe_customer_id. Historical orphan invoices were unreachable regardless of
which row was clicked.

Prod audit: 71 paid Stripe orders missing stripe_invoice_id (63 sub + 8 topup, all ORD-*);
17 of those are orphan across 9 users (~$749).

### Half 2 — credit-sync "订阅后左右积分不一致"

Reported on uid 7339182334568046592 (Antom Starter): left sidebar shows 积分 48,346 while
right /claw-settings 用量 panel shows 积分 33,120 / 33,120 at the same time.
Root cause: this user has two active subscription wallets in BG (legacy duplicate from BG init).
check_user_credits iterated wallets and assigned balances per match, so the duplicate
overwrote the previous result.

Fix: sum across non-terminated wallets of each kind.
```

---

## Commit 2 — 96b01c12

**SHA**: 96b01c12  
**PR**: #1617  
**Title**: refactor(arch-review): extract inline prompt to .claude/commands/arch-review.md

### 完整 Commit Message

```
refactor(arch-review): extract inline prompt to .claude/commands/arch-review.md (#1617)

Extracts the 300-line system prompt from arch_review.py into a standalone Markdown
file at .claude/commands/arch-review.md. arch_review.py loads it at runtime instead.
No behavior change. Prompt text is identical.
```

---

## Commit 3 — 24156f91

**SHA**: 24156f91  
**PR**: #1537  
**Title**: refactor(web): RQ v2 PR-b3 — useBillingCredits switches to useQuery

### 完整 Commit Message

```
refactor(web): RQ v2 PR-b3 — useBillingCredits switches to useQuery (#1537)

Migrates useBillingCredits from a manual SWR-style hook to React Query useQuery.
Part of the React Query v2 migration series.
```

---

## Commit 4 — 44cc763a

**SHA**: 44cc763a  
**PR**: #1613  
**Title**: feat(claw-interface): wire vulture dead-function detection (informational) — #1503 PR1

### 完整 Commit Message

```
feat(claw-interface): wire vulture dead-function detection (informational) — #1503 PR1 (#1613)

Adds vulture dead-function detection to claw-interface CI. Runs in informational mode
(non-blocking) to surface dead code without failing the build.
```

---

## Commit 5 — 2d789d73

**SHA**: 2d789d73  
**PR**: #1615  
**Title**: ci: delegate pr-size-check to srp-actions reusable

### 完整 Commit Message

```
ci: delegate pr-size-check to srp-actions reusable (#1615)

Replaces local pr-size-check workflow with the shared srp-actions/pr-size-check-v1
reusable action. No behavior change.
```

---

## Commit 6 — 502b138a

**SHA**: 502b138a  
**PR**: #1614  
**Title**: fix(arch-review): line-anchor RESOLVED_END marker in manual_suffix extract

### 完整 Commit Message

```
fix(arch-review): line-anchor RESOLVED_END marker in manual_suffix extract (#1614)

Fixes a regex in arch_review.py that failed to extract manual_suffix content when
the RESOLVED_END marker appeared mid-line rather than at line start.
```

---

## Commit 7 — d86a20b5

**SHA**: d86a20b5  
**PR**: #1611  
**Title**: ci(web): delegate web-quality to srp-actions/web-code-quality-v1

### 完整 Commit Message

```
ci(web): delegate web-quality to srp-actions/web-code-quality-v1 (#1611)

Replaces local web-quality CI workflow with the srp-actions reusable.
No behavior change.
```

---

## Commit 8 — d276c0f1

**SHA**: d276c0f1  
**PR**: #1612  
**Title**: ci: delegate codex-review to srp-actions/codex-review

### 完整 Commit Message

```
ci: delegate codex-review to srp-actions/codex-review (#1612)

Replaces local codex-review workflow with srp-actions reusable.
No behavior change.
```

---

## Commit 9 — 0c3c0102

**SHA**: 0c3c0102  
**PR**: #1610  
**Title**: chore: enable github plugin

### 完整 Commit Message

```
chore: enable github plugin (#1610)

Enable github@claude-plugins-core plugin in the agent config.
```

---

## Commit 10 — 592ae7e7

**SHA**: 592ae7e7  
**PR**: #1608  
**Title**: feat(arch-review): parametrize output language, default to Simplified Chinese

### 完整 Commit Message

```
feat(arch-review): parametrize output language, default to Simplified Chinese (#1608)

Adds --language flag to arch_review.py (default: "Simplified Chinese").
Prompt now instructs the model to respond in the specified language.
```

---

## Commit 11 — f72f8834

**SHA**: f72f8834  
**PR**: #1607  
**Title**: fix: 清 31 条 Dependabot + 3 条 CodeQL 安全告警

### 完整 Commit Message

```
fix: 清 31 条 Dependabot + 3 条 CodeQL 安全告警(收编 #1576) (#1607)

合并 dependabot PR #1576 的 8 个 minor/patch bump，叠加 GitHub Security 上 31 条
open Dependabot alerts + 3 条 CodeQL alerts 的全量修复。

主要升级：
- next: ^15.5.15 → ^15.5.18 (security: middleware bypass / SSRF / DoS / XSS)
- mermaid: ^11.14.0 → ^11.15.0 (security: 4 alerts)
- wrangler: ^4.85.0 → ^4.86.0
- @opennextjs/cloudflare: ^1.19.4 → ^1.19.5
- dompurify: ^3.4.1 → ^3.4.2
- marked: ^18.0.0 → ^18.0.3
```

---

## Commit 12 — 9b02c07a

**SHA**: 9b02c07a  
**PR**: #1588  
**Title**: feat(claw-interface): introduce Profile schema and dedicated profile_repo

### 完整 Commit Message

```
feat(claw-interface): introduce Profile schema and dedicated profile_repo for gem_account (#1588)

Adds Profile schema and a dedicated profile_repo for gem_account management.
Internal architecture change to support agent profile management in claw-interface.
```

---

## Commit 13 — 43a47c68

**SHA**: 43a47c68  
**PR**: #1606  
**Title**: chore(web): final dir-naming cleanup — baseline 6 → 0

### 完整 Commit Message

```
chore(web): final dir-naming cleanup — baseline 6 → 0 (#1606)

Final batch of directory naming cleanup. Baseline violation count: 6 → 0.
All camelCase directories renamed to kebab-case.
```

---

## Commit 14 — 20f9d08f

**SHA**: 20f9d08f  
**PR**: #1605  
**Title**: chore(web): rename lib/ 顶层 9 个 camelCase 散文件 → kebab-case

### 完整 Commit Message

```
chore(web): rename lib/ 顶层 9 个 camelCase 散文件 → kebab-case (#1605)

清理 lib/ 目录顶层 9 个 camelCase 文件名为 kebab-case。代码规范整理，无行为变化。
```

---

## Commit 15 — ce06aaca

**SHA**: ce06aaca  
**PR**: #1604  
**Title**: chore(web): rename lib/ 子目录剩余 13 个 camelCase 文件 → kebab-case

### 完整 Commit Message

```
chore(web): rename lib/ 子目录剩余 13 个 camelCase 文件 → kebab-case (#1604)

清理 lib/ 子目录剩余 13 个 camelCase 文件名为 kebab-case。代码规范整理，无行为变化。
```

---

## Commit 16 — c4c5d46a

**SHA**: c4c5d46a  
**PR**: #1603  
**Title**: chore(web): rename lib/skills/ 6 个 camelCase 文件 → kebab-case

### 完整 Commit Message

```
chore(web): rename lib/skills/ 6 个 camelCase 文件 → kebab-case (#1603)

清理 lib/skills/ 目录 6 个 camelCase 文件名为 kebab-case。代码规范整理，无行为变化。
```

---

## Commit 17 — 7ec66da8

**SHA**: 7ec66da8  
**PR**: #1592  
**Title**: feat: harden Antom Alipay payment integration

### 完整 Commit Message

```
feat: harden Antom Alipay payment integration (#1592)

- Integrate Antom/Alipay as a provider-aware payment path alongside Stripe.
- Harden Antom Cashier one-time payment creation with DB-authoritative amount/currency,
  redirect URL allowlisting, and signed API response verification.
- Add official Subscription Payment create/cancel plumbing.
- Make webhook/recovery fulfillment idempotent across success/failure/cancel paths.
- Add refund compensation that refunds through Antom and voids previously granted
  Billing Gateway credits with deterministic revoke transaction IDs.
- Treat refunded/compensating order states as non-success on the frontend payment success page.
- Sandbox tested end-to-end: Cashier top-up path, inquiry/webhook recovery, order paid,
  and credits grant all verified.
```

---

## Commit 18 — 0ed68020

**SHA**: 0ed68020  
**PR**: #1602  
**Title**: refactor(web): prefill composer instead of auto-sending landing query

### 完整 Commit Message

```
refactor(web): prefill composer instead of auto-sending landing query (#1602)

The landing-context flow (?sp=<specialist_id> + localStorage['ecap:landingContext'])
used to auto-send the initial query into chat once the agent switch settled.
This refactor replaces the auto-send with a prefill into the composer, so the user
reviews the prompt and submits manually.

Why: The user wanted the landing-page initial query to land in the chat input rather
than fire automatically — gives them a chance to edit before sending and avoids
surprise sends on the very first interaction.
```

---

## Commit 19 — 6d16f096

**SHA**: 6d16f096  
**PR**: #1590  
**Title**: docs: point CLAUDE.md to zooclaw-tips sister repo

### 完整 Commit Message

```
docs: point CLAUDE.md to zooclaw-tips sister repo (#1590)

Add Related Repos section to CLAUDE.md linking the zooclaw-tips sister repository
for agent tips and tricks.
```

---

## Commit 20 — c39f59e5

**SHA**: c39f59e5  
**PR**: #1601  
**Title**: fix(web): prevent login modal reopen race

### 完整 Commit Message

```
fix(web): prevent login modal reopen race (#1601)

Fixes a race where rapidly reopening the login modal (close → open within 300ms)
caused a stale exit timer to unmount the freshly-opened modal.

- Track the in-flight transition timer in a useRef so each isOpen flip cancels
  the prior handle before scheduling the next.
- Use a single setTimeout-based primitive for both the enter (0ms) and exit
  (300ms, gates shouldRender).

New regression test: "does not let a stale close timer unmount the modal after
it reopens" — covers the race; 4522 unit tests passed.
```
