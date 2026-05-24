# SerendipityOneInc/ecap-workspace — 2026-05-23

## d0f171e — fix(openclaw): wait for agent activation readiness (#1883)

- **Author:** tim-srp
- **Date:** 2026-05-23T09:17:22Z
- **SHA:** d0f171e3db84b74fcc130f0295acd7c5de844c39

### Commit Message

```
fix(openclaw): wait for agent activation readiness (#1883)

## Summary
- wait for the target Mattermost account to be running and connected
before sending post-install activation
- keep legacy runtime compatibility when channelAccounts is absent
- apply the same per-agent readiness wait to hired agent activation and
skip activation when readiness times out

## Tests
- ruff check app/routes/openclaw_agents/core.py
app/routes/openclaw_agents/shared.py tests/unit/test_openclaw_agents.py
- ruff check .
- pytest -W 'ignore::PendingDeprecationWarning'
tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_activation_waits_for_specific_mattermost_account
tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_activation_skips_post_when_specific_mattermost_account_times_out
tests/unit/test_openclaw_agents.py::TestUpdateUserAgentsMMProvisioning::test_rehire_uses_hi_activation_message
tests/unit/test_openclaw_agents.py::TestHireAgent::test_hire_agent_rehire_uses_hi_activation

## Notes
- pyright app tests was attempted locally, but this shell cannot resolve
backend dependencies such as fastapi, pytest, and favie_common outside
the devcontainer/CI environment.
```

### PR #1883 Body

## Summary
- wait for the target Mattermost account to be running and connected before sending post-install activation
- keep legacy runtime compatibility when channelAccounts is absent
- apply the same per-agent readiness wait to hired agent activation and skip activation when readiness times out

## Tests
- ruff check app/routes/openclaw_agents/core.py app/routes/openclaw_agents/shared.py tests/unit/test_openclaw_agents.py
- ruff check .
- pytest -W 'ignore::PendingDeprecationWarning' tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_activation_waits_for_specific_mattermost_account tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_activation_skips_post_when_specific_mattermost_account_times_out tests/unit/test_openclaw_agents.py::TestUpdateUserAgentsMMProvisioning::test_rehire_uses_hi_activation_message tests/unit/test_openclaw_agents.py::TestHireAgent::test_hire_agent_rehire_uses_hi_activation

## Notes
- pyright app tests was attempted locally, but this shell cannot resolve backend dependencies such as fastapi, pytest, and favie_common outside the devcontainer/CI environment.

---

## 51840ef — feat(enterprise-admin): polish account entry and users UI (#1863)

- **Author:** bill-srp
- **Date:** 2026-05-23T07:59:24Z
- **SHA:** 51840ef7c24def537464e5ba0e87e02034be72aa

### Commit Message

```
feat(enterprise-admin): polish account entry and users UI (#1863)

## Linear

https://linear.app/srpone/issue/ECA-749/admin-console-web-phase-1-users-module

## Summary
- polish the enterprise-admin login and verify screens with the Business
console visual treatment
- refine the users page, invite dialog, user actions, and table layout,
including the UID column
- keep R2 upload handling scoped to organization logos after the worker
upload integration landed separately

## Split PR status
The account proxy, onboarding flow, org API alignment, R2 worker upload
integration, and join invite flow were split out and merged separately.
This PR now carries only the remaining frontend polish and org-logo
scoping changes.

## Tests
- Not rerun for this metadata update after rebasing the original branch
onto current main.
```

### PR #1863 Body

## Linear
https://linear.app/srpone/issue/ECA-749/admin-console-web-phase-1-users-module

## Summary
- polish the enterprise-admin login and verify screens with the Business console visual treatment
- refine the users page, invite dialog, user actions, and table layout, including the UID column
- keep R2 upload handling scoped to organization logos after the worker upload integration landed separately

## Split PR status
The account proxy, onboarding flow, org API alignment, R2 worker upload integration, and join invite flow were split out and merged separately. This PR now carries only the remaining frontend polish and org-logo scoping changes.

## Tests
- Not rerun for this metadata update after rebasing the original branch onto current main.

---

## 3279974 — feat(web): split artifact Download into HTML + PDF-via-prompt menu (#1880)

- **Author:** Nemo Feng
- **Date:** 2026-05-23T07:34:02Z
- **SHA:** 32799746bd75f617cb597a101b6866d5b15220e3

### Commit Message

```
feat(web): split artifact Download into HTML + PDF-via-prompt menu (#1880)

## Linear
https://linear.app/srpone/issue/ECA-809/

## Summary
- When previewing an **HTML** artifact, the top-right Download button
now opens a 2-item dropdown:
  1. **Download as HTML** — original behavior (raw blob download)
2. **Download as PDF (send a prompt)** — sends a localized prompt into
the current chat asking the assistant to use headless Chromium to
convert the HTML to PDF
- All other artifact types (PDF, CSV, code, etc.) keep the existing
single Download button
- The share/replay viewer (`/share/<shareId>`) also keeps the single
button — `onSendMessage` is an optional prop, so the dropdown branch is
only enabled where a chat composer exists
- New `artifacts` i18n namespace with 4 keys (`download`,
`downloadAsHtml`, `downloadAsPdfViaPrompt`, `downloadPdfPrompt`)
translated across all 10 locales (en/zh/ja/ko/fr/de/it/es/ar/pt). The
prompt body matches the active UI language at click time
- Implementation uses the existing shadcn `DropdownMenu` primitive
(`@/components/ds/dropdown-menu`) — no new deps, no hand-rolled UI, no
backend changes

## Test plan
- [ ] Open chat, trigger an HTML artifact → toolbar shows Download
button with a chevron; clicking opens a 2-item dropdown styled like
surrounding popovers
- [ ] Click **Download as HTML** → file saves (existing behavior
unchanged)
- [ ] Click **Download as PDF (send a prompt)** → localized prompt
appears as a sent message in the chat; assistant begins responding
- [ ] Switch UI language (e.g. EN → ZH) → both menu labels and the sent
prompt body switch to that locale
- [ ] Open a non-HTML artifact (PDF, CSV, code) → toolbar shows the
original single Download button (no dropdown)
- [ ] Open `/share/<shareId>` on an HTML artifact → toolbar shows the
original single Download button (no PDF option, since there's no chat to
send into)

---------

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

### PR #1880 Body

## Linear
https://linear.app/srpone/issue/ECA-809/

## Summary
- When previewing an **HTML** artifact, the top-right Download button now opens a 2-item dropdown:
  1. **Download as HTML** — original behavior (raw blob download)
  2. **Download as PDF (send a prompt)** — sends a localized prompt into the current chat asking the assistant to use headless Chromium to convert the HTML to PDF
- All other artifact types (PDF, CSV, code, etc.) keep the existing single Download button
- The share/replay viewer (`/share/<shareId>`) also keeps the single button — `onSendMessage` is an optional prop, so the dropdown branch is only enabled where a chat composer exists
- New `artifacts` i18n namespace with 4 keys (`download`, `downloadAsHtml`, `downloadAsPdfViaPrompt`, `downloadPdfPrompt`) translated across all 10 locales (en/zh/ja/ko/fr/de/it/es/ar/pt). The prompt body matches the active UI language at click time
- Implementation uses the existing shadcn `DropdownMenu` primitive (`@/components/ds/dropdown-menu`) — no new deps, no hand-rolled UI, no backend changes

## Test plan
- [ ] Open chat, trigger an HTML artifact → toolbar shows Download button with a chevron; clicking opens a 2-item dropdown styled like surrounding popovers
- [ ] Click **Download as HTML** → file saves (existing behavior unchanged)
- [ ] Click **Download as PDF (send a prompt)** → localized prompt appears as a sent message in the chat; assistant begins responding
- [ ] Switch UI language (e.g. EN → ZH) → both menu labels and the sent prompt body switch to that locale
- [ ] Open a non-HTML artifact (PDF, CSV, code) → toolbar shows the original single Download button (no dropdown)
- [ ] Open `/share/<shareId>` on an HTML artifact → toolbar shows the original single Download button (no PDF option, since there's no chat to send into)

---

## d20f87b — fix(enterprise-admin): add invite join flow (#1881)

- **Author:** bill-srp
- **Date:** 2026-05-23T06:33:45Z
- **SHA:** d20f87be25a8e80202750c0087053bf4fe185215

### Commit Message

```
fix(enterprise-admin): add invite join flow (#1881)

## Summary
- replace the old invite landing with /join and a compatibility
/orgs/[orgId]/join route
- add invited-user email OTP signup/login and join redemption flow
- gate join redemption for accounts that already belong to a workspace

## Scope
- frontend-only; backend invite email link changes will land separately

## Test plan
- pnpm --filter @zooclaw/enterprise-admin exec vitest run --config
./vitest.config.mts app/join/__tests__/join-page.test.tsx
app/__tests__/useEntryViewModel.test.tsx
hooks/__tests__/useInvite.test.tsx lib/__tests__/auth.test.ts
- pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --filter @zooclaw/enterprise-admin lint
```

### PR #1881 Body

## Summary
- replace the old invite landing with /join and a compatibility /orgs/[orgId]/join route
- add invited-user email OTP signup/login and join redemption flow
- gate join redemption for accounts that already belong to a workspace

## Scope
- frontend-only; backend invite email link changes will land separately

## Test plan
- pnpm --filter @zooclaw/enterprise-admin exec vitest run --config ./vitest.config.mts app/join/__tests__/join-page.test.tsx app/__tests__/useEntryViewModel.test.tsx hooks/__tests__/useInvite.test.tsx lib/__tests__/auth.test.ts
- pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --filter @zooclaw/enterprise-admin lint

---

## 49d1ffa — refactor(web): migrate pricing CSS to scoped .css file (#368 F8, hygiene) (#1878)

- **Author:** Chris@ZooClaw
- **Date:** 2026-05-23T06:29:58Z
- **SHA:** 49d1ffacbd99ca00362143c062907689b8df2475

### Commit Message

```
refactor(web): migrate pricing CSS to scoped .css file (#368 F8, hygiene) (#1878)

## Summary

Closes **F8** in arch-review issue #368 as a **hygiene + consistency
cleanup**, not a visual-regression fix.

> **Re-framing note (learned from PR #1875 / F9)**: F8 was originally
framed by the arch-review tool as "730-line inline CSS includes unscoped
global resets leaking to siblings." Closer audit found Tailwind v4
preflight (`@import 'tailwindcss'` in `globals.css`) already applies the
same `*` margin/padding 0 and `a` color/text-decoration resets to the
entire site, so the two unscoped rules at the top of `PAGE_CSS` were
**redundant duplicates of framework defaults**, not a silent leak. The
PR remains net-positive for hygiene reasons listed below, but the threat
model in F8 (mirroring F9) was overstated.

## What changed

Mirror the established `landing.css` (PRs #741 / #756) + `userguide.css`
(#1875 / F9) migration:

- **New `web/app/src/app/[locale]/pricing/pricing.css`** — 741 lines
extracted from the inline `PAGE_CSS` template literal in
`PublicPricingClient.tsx`.
- Scope the previously-unscoped top-of-file resets under `.pricing-root
*, ...` and `.pricing-root a`. Tailwind preflight already covers this
globally, but scoping is the local-convention contract — future
maintainers shouldn't encounter a stray bare `*` selector in a
`pricing-root`-prefixed CSS file.
- `PublicPricingClient.tsx`:
- Top-level `import './pricing.css'` replaces the 743-line `const
PAGE_CSS = \`...\`` block.
  - Drop the `<style>{PAGE_CSS}</style>` runtime injection.

Outer wrapper already uses `className="pricing-root min-h-screen"`, so
no DOM change needed. Every other selector in the original CSS already
used `.pricing-root` as a prefix.

## Why it's net-positive (even with no real visual regression)

| Reason | Detail |
|---|---|
| Consistency with `landing.css` + `userguide.css` pattern | Three
branded modules now share the same `.{module}-root` + dedicated `.css`
file idiom |
| Drift defense | If Tailwind preflight is ever disabled or a component
restructures, scoped rules remain bounded; redundant unscoped rules
would silently start mattering |
| Build-time CSS extraction | Next.js extracts imported `.css` at build,
avoiding the runtime `<style>` injection's hydration flash |
| Drop 743 lines of inline template-literal CSS in `.tsx` | `.tsx`
shrinks 1187 → 443 lines; CSS lives in a real `.css` file IDE / lint
tooling can work with |

## Net diff

| File | Change |
|---|---|
| `pricing.css` | new, 741 lines |
| `PublicPricingClient.tsx` | -743 lines `PAGE_CSS` block, -1 `<style>`
injection, +1 `import './pricing.css'` |
| **Total** | +744 / -746 |

## Test plan

- [x] `pnpm tsc` clean
- [x] `pnpm lint` clean (after auto-fix import sort)
- [x] `pnpm test:unit` — 5659 tests pass
- [ ] Manual smoke on staging: `/{locale}/pricing` renders identical
(font, dark background, plan cards, toast). Expectation is **no visible
change** since Tailwind preflight already provided the equivalent resets
globally.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1878 Body

## Summary

Closes **F8** in arch-review issue #368 as a **hygiene + consistency cleanup**, not a visual-regression fix.

> **Re-framing note (learned from PR #1875 / F9)**: F8 was originally framed by the arch-review tool as "730-line inline CSS includes unscoped global resets leaking to siblings." Closer audit found Tailwind v4 preflight (`@import 'tailwindcss'` in `globals.css`) already applies the same `*` margin/padding 0 and `a` color/text-decoration resets to the entire site, so the two unscoped rules at the top of `PAGE_CSS` were **redundant duplicates of framework defaults**, not a silent leak. The PR remains net-positive for hygiene reasons listed below, but the threat model in F8 (mirroring F9) was overstated.

## What changed

Mirror the established `landing.css` (PRs #741 / #756) + `userguide.css` (#1875 / F9) migration:

- **New `web/app/src/app/[locale]/pricing/pricing.css`** — 741 lines extracted from the inline `PAGE_CSS` template literal in `PublicPricingClient.tsx`.
- Scope the previously-unscoped top-of-file resets under `.pricing-root *, ...` and `.pricing-root a`. Tailwind preflight already covers this globally, but scoping is the local-convention contract — future maintainers shouldn't encounter a stray bare `*` selector in a `pricing-root`-prefixed CSS file.
- `PublicPricingClient.tsx`:
  - Top-level `import './pricing.css'` replaces the 743-line `const PAGE_CSS = \`...\`` block.
  - Drop the `<style>{PAGE_CSS}</style>` runtime injection.

Outer wrapper already uses `className="pricing-root min-h-screen"`, so no DOM change needed. Every other selector in the original CSS already used `.pricing-root` as a prefix.

## Why it's net-positive (even with no real visual regression)

| Reason | Detail |
|---|---|
| Consistency with `landing.css` + `userguide.css` pattern | Three branded modules now share the same `.{module}-root` + dedicated `.css` file idiom |
| Drift defense | If Tailwind preflight is ever disabled or a component restructures, scoped rules remain bounded; redundant unscoped rules would silently start mattering |
| Build-time CSS extraction | Next.js extracts imported `.css` at build, avoiding the runtime `<style>` injection's hydration flash |
| Drop 743 lines of inline template-literal CSS in `.tsx` | `.tsx` shrinks 1187 → 443 lines; CSS lives in a real `.css` file IDE / lint tooling can work with |

## Net diff

| File | Change |
|---|---|
| `pricing.css` | new, 741 lines |
| `PublicPricingClient.tsx` | -743 lines `PAGE_CSS` block, -1 `<style>` injection, +1 `import './pricing.css'` |
| **Total** | +744 / -746 |

## Test plan

- [x] `pnpm tsc` clean
- [x] `pnpm lint` clean (after auto-fix import sort)
- [x] `pnpm test:unit` — 5659 tests pass
- [ ] Manual smoke on staging: `/{locale}/pricing` renders identical (font, dark background, plan cards, toast). Expectation is **no visible change** since Tailwind preflight already provided the equivalent resets globally.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 1943aaa — fix(openclaw): log deprecated init agent selection (#1879)

- **Author:** Chris@ZooClaw
- **Date:** 2026-05-23T06:08:01Z
- **SHA:** 1943aaa0287b143f2c8d430644139e77504c1460

### Commit Message

```
fix(openclaw): log deprecated init agent selection (#1879)

## Summary
- Add error-level telemetry when `/openclaw/init` receives deprecated
`selected_agent_ids`.
- Include issue #403 in the log line so alerts point directly to the
investigation context.
- Cover the telemetry with a focused init endpoint unit test.

## Root cause
`/openclaw/init` still accepts `selected_agent_ids` for backward
compatibility, but init-time agent selection is deprecated and should
eventually move fully to `/openclaw/agents` / hire / fire / install /
uninstall routes. Before changing behavior, we need to know whether any
real clients still send the deprecated field.

Tracked in
https://github.com/SerendipityOneInc/ecap-workspace/issues/403.

## Test plan
- [x] `uv run --no-project --with-requirements requirements.txt
--with-requirements requirements-dev.txt pytest
tests/unit/test_openclaw_endpoints_extra.py -q`
- [x] `uv run --no-project --with-requirements requirements.txt
--with-requirements requirements-dev.txt ruff format --check
app/routes/openclaw.py app/services/openclaw/init_telemetry.py
tests/unit/test_openclaw_endpoints_extra.py`
- [x] `uv run --no-project --with-requirements requirements.txt
--with-requirements requirements-dev.txt ruff check
app/routes/openclaw.py app/services/openclaw/init_telemetry.py
tests/unit/test_openclaw_endpoints_extra.py`
- [x] `bash scripts/ci-lint/01-file-length.sh`
```

### PR #1879 Body

## Summary
- Add error-level telemetry when `/openclaw/init` receives deprecated `selected_agent_ids`.
- Include issue #403 in the log line so alerts point directly to the investigation context.
- Cover the telemetry with a focused init endpoint unit test.

## Root cause
`/openclaw/init` still accepts `selected_agent_ids` for backward compatibility, but init-time agent selection is deprecated and should eventually move fully to `/openclaw/agents` / hire / fire / install / uninstall routes. Before changing behavior, we need to know whether any real clients still send the deprecated field.

Tracked in https://github.com/SerendipityOneInc/ecap-workspace/issues/403.

## Test plan
- [x] `uv run --no-project --with-requirements requirements.txt --with-requirements requirements-dev.txt pytest tests/unit/test_openclaw_endpoints_extra.py -q`
- [x] `uv run --no-project --with-requirements requirements.txt --with-requirements requirements-dev.txt ruff format --check app/routes/openclaw.py app/services/openclaw/init_telemetry.py tests/unit/test_openclaw_endpoints_extra.py`
- [x] `uv run --no-project --with-requirements requirements.txt --with-requirements requirements-dev.txt ruff check app/routes/openclaw.py app/services/openclaw/init_telemetry.py tests/unit/test_openclaw_endpoints_extra.py`
- [x] `bash scripts/ci-lint/01-file-length.sh`


---

## 006c082 — fix(enterprise-admin): add R2 logo upload (#1877)

- **Author:** bill-srp
- **Date:** 2026-05-23T05:54:11Z
- **SHA:** 006c082e9db48a9c1b89655544bb7ecf2986436c

### Commit Message

```
fix(enterprise-admin): add R2 logo upload (#1877)

## Summary
- add Cloudflare R2 bindings and upload helpers for enterprise-admin
- add authenticated /api/r2/upload for org logos with file type/size
validation
- add optional workspace logo upload during onboarding

## Test plan
- pnpm --filter @zooclaw/enterprise-admin exec vitest run --config
./vitest.config.mts lib/__tests__/r2.test.ts
app/api/r2/upload/__tests__/route.test.ts
components/onboarding/__tests__/OrgLogoField.test.tsx
components/onboarding/__tests__/OrgSetupForm.test.tsx
app/onboarding/__tests__/onboarding-page.test.tsx
- pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --filter @zooclaw/enterprise-admin lint
```

### PR #1877 Body

## Summary
- add Cloudflare R2 bindings and upload helpers for enterprise-admin
- add authenticated /api/r2/upload for org logos with file type/size validation
- add optional workspace logo upload during onboarding

## Test plan
- pnpm --filter @zooclaw/enterprise-admin exec vitest run --config ./vitest.config.mts lib/__tests__/r2.test.ts app/api/r2/upload/__tests__/route.test.ts components/onboarding/__tests__/OrgLogoField.test.tsx components/onboarding/__tests__/OrgSetupForm.test.tsx app/onboarding/__tests__/onboarding-page.test.tsx
- pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --filter @zooclaw/enterprise-admin lint

---

## a923dbc — test(web): dedup top-3 specs + restore jscpd threshold to 7.0 (#1869) (#1876)

- **Author:** Chris@ZooClaw
- **Date:** 2026-05-23T05:41:29Z
- **SHA:** a923dbc0b38057d9230df9c7fc74fe9cf169e108

### Commit Message

```
test(web): dedup top-3 specs + restore jscpd threshold to 7.0 (#1869) (#1876)

## Summary

Closes #1869. Extract file-local helpers in 3 unit specs to collapse
repeated test scaffolding, then restore the `web/app/.jscpd.tests.json`
tests-duplication threshold from `8.0` (#1867 hygiene workaround) back
to `7.0`.

| Spec | Helper(s) | Dup lines removed (jscpd) |
|---|---|---|
| `tests/unit/app/admin/useBatchGrant.unit.spec.ts` | `openBatchGrant` /
`runBatchGrant` | 91L (10 clones) → off top-N |
| `tests/unit/hooks/useLandingContextFlow.unit.spec.ts` |
`seedLandingContext` | 119L (13 clones) → off top-N |
| `tests/unit/hooks/useClawSettings.unit.spec.ts` | `bootClawSettings` /
`bootAndCall` | 81L (10 clones) → off top-N |

**Diff: -227 / +130 lines (net -97) across 3 spec files**.

**Results:**
- jscpd tests `percentage` (lines): **6.48% → 6.12%**
- jscpd tests `percentageTokens`: 7.78% → 7.28%
- `.jscpd.tests.json` `threshold`: **8.0 → 7.0**, `_comment` removed

## Why the threshold change is bigger than it looks

While investigating the issue I found the stated premise (jscpd failing
at 7.98% threshold-breach in #1867) is a metric-confusion: jscpd's
`threshold` config gates `statistics.total.percentage` (lines%), **not**
`percentageTokens`. The 7.98% number was the token% (jscpd's adjacent
table column).

Verified locally on PR #1867's parent commit:

```
$ git checkout 83b56930~1 -- web/app/tests web/app/.jscpd.tests.json
$ cd web/app && npx jscpd --threshold 7.0 --silent -c .jscpd.tests.json
exit=0
# percentage: 6.71, percentageTokens: 7.99
```

So even at the pre-#1867 state, line% (6.71%) was under threshold 7.0 →
the gate would have **passed**. The #1867 CI red on attempt 676e34f6 was
a `tsc --noEmit` TS2322 error in `useNavIdentity.unit.spec.ts(239,16)`,
not jscpd; the jscpd step exited 0.

This PR fixes both:
1. **Threshold:** restores 7.0 and removes the explanatory `_comment`
workaround
2. **Dedup:** brings line% from 6.48 → 6.12, giving the gate ~0.88pp
real buffer (first time since the threshold metric was selected)

## Out of scope

- Token% gate (jscpd doesn't natively support a token% threshold; issue
Option C was explicitly rejected)
- `openclaw-agents-install-uninstall` / `useSSEStream` / `useLiteLLMApi`
— already deduped in #1867; remaining clones are test-case variance, not
setup repetition
- `upload.unit.spec.ts` + `upload-extras.unit.spec.ts` — known dup
hotspot per memory `feedback_test_extras_jscpd_dup`; base+extras
shared-fixture refactor is its own scope
- `useSubagentSessions` (78L, 9 clones) — clones are event-shape
variations across distinct test cases, not setup repetition; remaining
0.88pp buffer is comfortable enough to defer

## Test plan
- [x] `cd web/app && pnpm dup:tests` — exit 0 at threshold 7.0
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm test:unit` — 5658 passed (no regressions)
- [x] `npx eslint` on the 3 changed files — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## 8366b94 — fix(enterprise-admin): enable onboarding wizard (#1872)

- **Author:** bill-srp
- **Date:** 2026-05-23T05:31:45Z
- **SHA:** 8366b9473cbc6d42ab5c5c17780ef19349fbd32b

### Commit Message

```
fix(enterprise-admin): enable onboarding wizard (#1872)

## Summary
- remove the onboarding coming-soon gate now that the account/org/users
API slices are merged
- simplify first-run onboarding invites to email-only input
- send default member role and computer quota for onboarding invites
- update bulk invite parsing and onboarding tests

## Root cause
The onboarding wizard was still hidden behind
NEXT_PUBLIC_ONBOARDING_ENABLED and its bulk invite parser still required
role/quota fields, even though the intended first-run flow only asks for
invitee email and uses defaults.

## Test plan
- [x] pnpm --filter @zooclaw/enterprise-admin exec vitest run --config
./vitest.config.mts app/onboarding/__tests__/onboarding-page.test.tsx
components/onboarding/__tests__/BulkInviteForm.test.tsx
lib/__tests__/parse-bulk-invite.test.ts
components/onboarding/__tests__/OrgSetupForm.test.tsx
components/onboarding/__tests__/WarmPoolForm.test.tsx
components/onboarding/__tests__/StepIndicator.test.tsx
- [x] pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- [x] pnpm --filter @zooclaw/enterprise-admin lint
```

### PR #1872 Body

## Summary
- remove the onboarding coming-soon gate now that the account/org/users API slices are merged
- simplify first-run onboarding invites to email-only input
- send default member role and computer quota for onboarding invites
- update bulk invite parsing and onboarding tests

## Root cause
The onboarding wizard was still hidden behind NEXT_PUBLIC_ONBOARDING_ENABLED and its bulk invite parser still required role/quota fields, even though the intended first-run flow only asks for invitee email and uses defaults.

## Test plan
- [x] pnpm --filter @zooclaw/enterprise-admin exec vitest run --config ./vitest.config.mts app/onboarding/__tests__/onboarding-page.test.tsx components/onboarding/__tests__/BulkInviteForm.test.tsx lib/__tests__/parse-bulk-invite.test.ts components/onboarding/__tests__/OrgSetupForm.test.tsx components/onboarding/__tests__/WarmPoolForm.test.tsx components/onboarding/__tests__/StepIndicator.test.tsx
- [x] pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- [x] pnpm --filter @zooclaw/enterprise-admin lint

---

## 5d20b2e — fix(web): migrate userguide CSS to scoped .css file + close unscoped global reset (#1875)

- **Author:** Chris@ZooClaw
- **Date:** 2026-05-23T05:30:39Z
- **SHA:** 5d20b2e693a4db87a7cf2c9a8ec935d275e73b76

### Commit Message

```
fix(web): migrate userguide CSS to scoped .css file + close unscoped global reset (#1875)

## Summary

Closes **F9** in arch-review issue #368: `UserGuideClient.tsx` was
injecting ~584 lines of CSS via a runtime `<style>` element, and the
first two rules were **unscoped global resets** that leaked to the
shared `PublicHeader` / `PublicFooter` components rendered alongside the
guide content.

The leaky rules:
```css
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
a { text-decoration: none; color: inherit; cursor: pointer; }
```

Because Next.js injects `<style>` blocks into the document `<head>`,
these applied across the whole page — silent visual-regression vector.

## Changes

Migration follows the existing `landing.css` pattern (PRs #741 / #756):

- **New `web/app/src/app/[locale]/userguide/userguide.css`** — merged
content of the two old `*-css.ts` modules. The two unscoped rules are
now `.userguide-root *, ...` and `.userguide-root a` (matches
`landing.css` line 1 + line 36).
- **`UserGuideClient.tsx`** — replace `<style>{GUIDE_CSS +
GUIDE_TIPS_CSS}</style>` with a top-level `import './userguide.css'`.
Drop the two `import { GUIDE_CSS / GUIDE_TIPS_CSS }` imports.
- **Delete** `userguide-css.ts` (483 lines) and `userguide-tips-css.ts`
(101 lines).

All other rules in the original CSS already used `.userguide-root` as a
selector prefix, so this migration only had to fix the two unscoped
resets — every other selector is already correctly scoped. The outer
wrapper already uses `className="userguide-root min-h-screen"`, so no
DOM change needed.

## Net diff

| File | Change |
|---|---|
| `userguide.css` | new, 581 lines |
| `userguide-css.ts` | deleted (was 483 lines) |
| `userguide-tips-css.ts` | deleted (was 101 lines) |
| `UserGuideClient.tsx` | -3 imports + 1 `import './userguide.css'`,
removed `<style>` injection |
| **Total** | +104 / -109 |

## Test plan

- [x] `pnpm tsc` clean
- [x] `pnpm lint` clean (after auto-fix import sort)
- [x] `pnpm test:unit` — 5659 tests pass
- [ ] Manual smoke on staging: `/{locale}/userguide` page renders
identical to before (font, dark background, sidebar, FAQ, tip-card
flips, anchor scroll). Verify `PublicHeader` + `PublicFooter` on
`/userguide` and on a separate page (e.g. `/`) show no margin / padding
/ link-color regressions from the reset leak.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1875 Body

## Summary

Closes **F9** in arch-review issue #368 as a **code hygiene + consistency** cleanup. Migrates `web/app/src/app/[locale]/userguide/` from runtime `<style>{cssString}</style>` injection to a static `.css` import, and scopes the two top-level CSS reset rules under `.userguide-root *` to match the established `landing.css` pattern.

> **Re-framing note (added post-review)**: F9 was originally framed as "fix silent visual regression risk from unscoped global reset leaking to PublicHeader/PublicFooter." Closer audit found Tailwind v4 preflight (`@import 'tailwindcss'` in `globals.css`) already applies the same `*` margin/padding 0 and `a` color/text-decoration resets to the entire site, so the two unscoped rules in `userguide-css.ts` were **redundant with framework defaults, not a real leak**. The PR remains net-positive for hygiene reasons listed below, but the threat model in arch-review F9 was overstated.

## What changed

Migration follows the existing `landing.css` pattern (PRs #741 / #756):

- **New `web/app/src/app/[locale]/userguide/userguide.css`** — merged content of the two old `*-css.ts` modules (583 lines).
- **Scoped the two reset rules** under `.userguide-root *, ...` and `.userguide-root a` (matches `landing.css` line 1 + line 36) — even though Tailwind preflight already does the equivalent globally, scoping protects against future drift if preflight ever gets disabled or a component changes layout.
- **`UserGuideClient.tsx`** — replace `<style>{GUIDE_CSS + GUIDE_TIPS_CSS}</style>` with a top-level `import './userguide.css'`. Drop the two `import { GUIDE_CSS / GUIDE_TIPS_CSS }` imports.
- **Delete** `userguide-css.ts` (483 lines) and `userguide-tips-css.ts` (101 lines).

The outer wrapper already uses `className="userguide-root min-h-screen"`, so no DOM change needed. All other selectors in the original CSS already used `.userguide-root` as a prefix.

## Why it's net-positive (even if no real visual regression existed)

| Reason | Detail |
|---|---|
| Consistency with `landing.css` pattern | Future maintainers won't be confused why `/landing` is scoped and `/userguide` isn't — both follow the same idiom now |
| Drift defense | If Tailwind preflight is ever disabled or a component restructures, scoped rules remain bounded; unscoped reset would silently start mattering |
| Build-time CSS extraction | Next.js extracts imported `.css` during build, avoiding the runtime `<style>` injection's hydration flash. Marginally better UX on first paint |
| Drop ~584 lines of `.ts` template-literal CSS | Source tree cleanup + IDE CSS tooling (autocomplete / lint) now works on `.css` file directly |

## Net diff

| File | Change |
|---|---|
| `userguide.css` | new, 581 lines |
| `userguide-css.ts` | deleted (was 483 lines) |
| `userguide-tips-css.ts` | deleted (was 101 lines) |
| `UserGuideClient.tsx` | -3 imports + 1 `import './userguide.css'`, removed `<style>` injection |
| **Total** | +104 / -109 |

## Test plan

- [x] `pnpm tsc` clean
- [x] `pnpm lint` clean (after auto-fix import sort)
- [x] `pnpm test:unit` — 5659 tests pass
- [ ] Manual smoke on staging: `/{locale}/userguide` page renders identical to before (font, dark background, sidebar, FAQ, tip-card flips, anchor scroll). Verify `PublicHeader` + `PublicFooter` show no margin / padding / link-color regressions — but expectation is **no visible change** because Tailwind preflight already provided equivalent reset globally.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## df94abb — fix(org): provision billing team server side (#1874)

- **Author:** bill-srp
- **Date:** 2026-05-23T05:20:05Z
- **SHA:** df94abbb28f548db170d846a905d1623062a4db3

### Commit Message

```
fix(org): provision billing team server side (#1874)

## Summary
- remove billing team fields from the public org create request
- provision the org billing team server-side through Billing Gateway
- keep POST /orgs behind platform admin auth while creating the caller
as org admin

## Tests
- docker exec service-enterprise-bill bash -lc 'cd
/workspaces/service-enterprise/services/claw-interface && pytest
tests/unit/test_org_service.py tests/unit/test_routes_org.py
tests/unit/test_schema_org.py'
- docker exec service-enterprise-bill bash -lc 'cd
/workspaces/service-enterprise/services/claw-interface && ruff check
app/routes/enterprise/org.py app/schema/org.py
app/services/org/org_service.py tests/unit/test_org_service.py
tests/unit/test_routes_org.py tests/unit/test_schema_org.py'
- docker exec service-enterprise-bill bash -lc 'cd
/workspaces/service-enterprise/services/claw-interface && pyright
app/routes/enterprise/org.py app/schema/org.py
app/services/org/org_service.py tests/unit/test_org_service.py
tests/unit/test_routes_org.py tests/unit/test_schema_org.py'
```

### PR #1874 Body

## Summary
- remove billing team fields from the public org create request
- provision the org billing team server-side through Billing Gateway
- keep POST /orgs behind platform admin auth while creating the caller as org admin

## Tests
- docker exec service-enterprise-bill bash -lc 'cd /workspaces/service-enterprise/services/claw-interface && pytest tests/unit/test_org_service.py tests/unit/test_routes_org.py tests/unit/test_schema_org.py'
- docker exec service-enterprise-bill bash -lc 'cd /workspaces/service-enterprise/services/claw-interface && ruff check app/routes/enterprise/org.py app/schema/org.py app/services/org/org_service.py tests/unit/test_org_service.py tests/unit/test_routes_org.py tests/unit/test_schema_org.py'
- docker exec service-enterprise-bill bash -lc 'cd /workspaces/service-enterprise/services/claw-interface && pyright app/routes/enterprise/org.py app/schema/org.py app/services/org/org_service.py tests/unit/test_org_service.py tests/unit/test_routes_org.py tests/unit/test_schema_org.py'

---

## d923c07 — fix(web): redirect /terms → /about/terms and delete stale stub + .bak files (#1873)

- **Author:** Chris@ZooClaw
- **Date:** 2026-05-23T05:14:05Z
- **SHA:** d923c07bd19cbcb105ca6df1d9c319a36b7bdff2

### Commit Message

```
fix(web): redirect /terms → /about/terms and delete stale stub + .bak files (#1873)

## Summary

Closes **F5** in arch-review issue #368: redundant `/terms` route +
stale `.bak` files.

The `/terms` route was rendering an unfinished `TermsClient` stub that
only showed a `common.loading` placeholder. The real Terms of Service
has always lived at `/about/terms` (164-line implementation under
`web/app/src/app/[locale]/about/terms/`). Two `page.tsx.bak` files were
also lingering in source control.

## Changes

- **`[locale]/terms/page.tsx`** → server-side redirect to `/about/terms`
via `next/navigation`'s `redirect()`. Preserves any external links /
bookmarks / search results that still point at the legacy `/terms` URL.
- **Delete `[locale]/terms/TermsClient.tsx`** — the loading-placeholder
stub is no longer needed once the route just redirects.
- **Delete `[locale]/terms/page.tsx.bak`** and
**`[locale]/about/page.tsx.bak`** — stale .bak files.
- **Keep `[locale]/abount/terms/`** — already a proper
`redirect('/about/terms')` page; preserves links to the historical typo
URL.

Net diff: `-4 files (3 deleted + 1 modified), +8 / -47 lines`.

## Test plan

- [x] `pnpm tsc` clean
- [x] `pnpm lint` clean (changed dir only)
- [x] `pnpm test:unit` — 5658 tests pass (no regressions)
- [ ] Smoke on staging: `/{locale}/terms` 301/302 redirects to
`/{locale}/about/terms`; the real page still renders correctly;
`/{locale}/abount/terms` still redirects (typo path unchanged)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1873 Body

## Summary

Closes **F5** in arch-review issue #368: redundant `/terms` route + stale `.bak` files.

The `/terms` route was rendering an unfinished `TermsClient` stub that only showed a `common.loading` placeholder. The real Terms of Service has always lived at `/about/terms` (164-line implementation under `web/app/src/app/[locale]/about/terms/`). Two `page.tsx.bak` files were also lingering in source control.

## Changes

- **`[locale]/terms/page.tsx`** → server-side redirect to `/about/terms` via `next/navigation`'s `redirect()`. Preserves any external links / bookmarks / search results that still point at the legacy `/terms` URL.
- **Delete `[locale]/terms/TermsClient.tsx`** — the loading-placeholder stub is no longer needed once the route just redirects.
- **Delete `[locale]/terms/page.tsx.bak`** and **`[locale]/about/page.tsx.bak`** — stale .bak files.
- **Keep `[locale]/abount/terms/`** — already a proper `redirect('/about/terms')` page; preserves links to the historical typo URL.

Net diff: `-4 files (3 deleted + 1 modified), +8 / -47 lines`.

## Test plan

- [x] `pnpm tsc` clean
- [x] `pnpm lint` clean (changed dir only)
- [x] `pnpm test:unit` — 5658 tests pass (no regressions)
- [ ] Smoke on staging: `/{locale}/terms` 301/302 redirects to `/{locale}/about/terms`; the real page still renders correctly; `/{locale}/abount/terms` still redirects (typo path unchanged)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 83b5693 — refactor(web): extract useClawIdentityQuery + useAgentIdentityMapOverlay sub-hooks (#1867)

- **Author:** Chris@ZooClaw
- **Date:** 2026-05-23T04:53:56Z
- **SHA:** 83b56930b01bc92caae18fadccb0c52a14e87b71

### Commit Message

```
refactor(web): extract useClawIdentityQuery + useAgentIdentityMapOverlay sub-hooks (#1867)

## Summary

Follow-up to PR #1865 (issue #368 F2 / F11). `useChatIdentity` and
`useNavIdentity` shared **four blocks** of duplicated identity-loading
plumbing:

1. `openclawKeys.clawIdentity` useQuery + queryFn (same shape)
2. Error log effect for the same query
3. `setCachedGlobalIdentity` / sessionStorage persistence
4. `OPENCLAW_AGENT_IDENTITY_UPDATED_EVENT` overlay state + listener

Both hooks subscribed to the same RQ cache bucket but ran independent
effect chains. PR #1865's review trail already showed this invariant
drifting between the two: r1 fixed the uid-gated sessionStorage write in
`useNavIdentity`; `useChatIdentity` carried the same un-gated write but
escaped notice because that file was not in the diff.

## What changed

Two new sub-hooks both consumers import:

- **`useClawIdentityQuery(uid, enabled)`**
(`web/app/src/hooks/queries/openclaw/useClawIdentityQuery.ts`) — owns
the useQuery + `refetchOnMount: 'always'` + uid-gated
`setCachedGlobalIdentity`. Returns the standard `UseQueryResult` so each
caller composes its own error log (chat-tagged `captureChatWarning` vs.
generic `Sentry.captureMessage`). Slots next to the existing
domain-query primitives in `hooks/queries/openclaw/`
(`useAgentSettingsQuery`, `useClawResources`).
- **`useAgentIdentityMapOverlay(uid)`**
(`web/app/src/hooks/useAgentIdentityMapOverlay.ts`) — owns the agent
identity overlay state, sessionStorage bootstrap, the
`OPENCLAW_AGENT_IDENTITY_UPDATED_EVENT` listener, and the
`lastKnownUidRef` reset on uid change. Returns a `Record<string,
CachedAgentIdentity>` map. Not a generic primitive — it's an app-level
shared block between two long-stable core hooks (chat + nav).

`useChatIdentity` keeps its chat-specific composition (active-agent
useAgentSettingsQuery, `resolvedChatIdentity` / `chatAvatarPresentation`
memos, `handleAgentIdentitySaved`). The inline query + sessionStorage
write + event listener are gone.

**Note on the uid-gated persistence behavior the sub-hook enforces**: it
is redundant for `useChatIdentity` in current prod flow — the `/chat`
route unmounts on logout, and the existing `clearUserStorage`
(`web/app/src/lib/auth/storage.ts:179`) + `manager.ts:240-242` explicit
`removeItem` already clear `sessionStorage` before `useChatIdentity`
remounts under a new uid. The redundancy is intentional: symmetric
implementation removes one drift surface between the two consumers, and
stays correct if the chat route lifecycle ever changes (e.g. a
modal-style chat overlay that stays mounted across auth changes).

`useNavIdentity` keeps batch-endpoint-specific behavior
(`agentSettingsBatch` useQuery, batch-cache patching on identity events,
its own `cachedGlobal` bootstrap for first-paint). The duplicated
`clawIdentity` + agent-overlay effects are delegated to the sub-hooks.

## Net diff

| File | Lines |
|---|---|
| `useChatIdentity.ts` | -59 |
| `useNavIdentity.ts` | -125 / +similar (recomposition) |
| **+ `useClawIdentityQuery.ts`** | +58 |
| **+ `useAgentIdentityMapOverlay.ts`** | +60 |
| **Net** | +173 / -129 = **+44 lines** |

Source-of-truth count for the duplicated patterns: 2 → 1.

## Why this is worth +44 lines

- Both consumers are core, long-stable hooks (chat / nav), not
throw-away callers — sub-hook abstractions stay relevant.
- `OPENCLAW_AGENT_IDENTITY_UPDATED_EVENT` schema, `CachedAgentIdentity`
shape, and the sessionStorage key are invariants both hooks must agree
on. PR #1865 review trail already exhibited drift on this surface;
collapsing implementation reduces the drift surface to 1.
- `useClawIdentityQuery` is a real domain-query primitive matching the
existing `hooks/queries/openclaw/` convention.

## Test plan

- [x] `pnpm tsc` clean
- [x] `pnpm lint` clean
- [x] `pnpm test:unit` — 5647 tests pass (no regressions;
`useNavIdentity.unit.spec.ts` integration coverage still pins the
SideNav contract end-to-end)
- [ ] Manual smoke on staging: chat page + SideNav identity render
unchanged; settings page identity edit propagates to both consumers
(chat header + SideNav avatar)
- [ ] DevTools Network: confirm only one `getClawSettings` round-trip
fires when both SideNav and chat page are mounted (already the case
after PR #1865, this PR doesn't change that)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1867 Body

## Summary

Follow-up to PR #1865 (issue #368 F2 / F11). `useChatIdentity` and `useNavIdentity` shared **four blocks** of duplicated identity-loading plumbing:

1. `openclawKeys.clawIdentity` useQuery + queryFn (same shape)
2. Error log effect for the same query
3. `setCachedGlobalIdentity` / sessionStorage persistence
4. `OPENCLAW_AGENT_IDENTITY_UPDATED_EVENT` overlay state + listener

Both hooks subscribed to the same RQ cache bucket but ran independent effect chains. PR #1865's review trail already showed this invariant drifting between the two: r1 fixed the uid-gated sessionStorage write in `useNavIdentity`; `useChatIdentity` carried the same un-gated write but escaped notice because that file was not in the diff.

## What changed

Two new sub-hooks both consumers import:

- **`useClawIdentityQuery(uid, enabled)`** (`web/app/src/hooks/queries/openclaw/useClawIdentityQuery.ts`) — owns the useQuery + `refetchOnMount: 'always'` + uid-gated `setCachedGlobalIdentity`. Returns the standard `UseQueryResult` so each caller composes its own error log (chat-tagged `captureChatWarning` vs. generic `Sentry.captureMessage`). Slots next to the existing domain-query primitives in `hooks/queries/openclaw/` (`useAgentSettingsQuery`, `useClawResources`).
- **`useAgentIdentityMapOverlay(uid)`** (`web/app/src/hooks/useAgentIdentityMapOverlay.ts`) — owns the agent identity overlay state, sessionStorage bootstrap, the `OPENCLAW_AGENT_IDENTITY_UPDATED_EVENT` listener, and the `lastKnownUidRef` reset on uid change. Returns a `Record<string, CachedAgentIdentity>` map. Not a generic primitive — it's an app-level shared block between two long-stable core hooks (chat + nav).

`useChatIdentity` keeps its chat-specific composition (active-agent useAgentSettingsQuery, `resolvedChatIdentity` / `chatAvatarPresentation` memos, `handleAgentIdentitySaved`). The inline query + sessionStorage write + event listener are gone.

**Note on the uid-gated persistence behavior the sub-hook enforces**: it is redundant for `useChatIdentity` in current prod flow — the `/chat` route unmounts on logout, and the existing `clearUserStorage` (`web/app/src/lib/auth/storage.ts:179`) + `manager.ts:240-242` explicit `removeItem` already clear `sessionStorage` before `useChatIdentity` remounts under a new uid. The redundancy is intentional: symmetric implementation removes one drift surface between the two consumers, and stays correct if the chat route lifecycle ever changes (e.g. a modal-style chat overlay that stays mounted across auth changes).

`useNavIdentity` keeps batch-endpoint-specific behavior (`agentSettingsBatch` useQuery, batch-cache patching on identity events, its own `cachedGlobal` bootstrap for first-paint). The duplicated `clawIdentity` + agent-overlay effects are delegated to the sub-hooks.

## Net diff

| File | Lines |
|---|---|
| `useChatIdentity.ts` | -59 |
| `useNavIdentity.ts` | -125 / +similar (recomposition) |
| **+ `useClawIdentityQuery.ts`** | +58 |
| **+ `useAgentIdentityMapOverlay.ts`** | +60 |
| **Net** | +173 / -129 = **+44 lines** |

Source-of-truth count for the duplicated patterns: 2 → 1.

## Why this is worth +44 lines

- Both consumers are core, long-stable hooks (chat / nav), not throw-away callers — sub-hook abstractions stay relevant.
- `OPENCLAW_AGENT_IDENTITY_UPDATED_EVENT` schema, `CachedAgentIdentity` shape, and the sessionStorage key are invariants both hooks must agree on. PR #1865 review trail already exhibited drift on this surface; collapsing implementation reduces the drift surface to 1.
- `useClawIdentityQuery` is a real domain-query primitive matching the existing `hooks/queries/openclaw/` convention.

## Test plan

- [x] `pnpm tsc` clean
- [x] `pnpm lint` clean
- [x] `pnpm test:unit` — 5647 tests pass (no regressions; `useNavIdentity.unit.spec.ts` integration coverage still pins the SideNav contract end-to-end)
- [ ] Manual smoke on staging: chat page + SideNav identity render unchanged; settings page identity edit propagates to both consumers (chat header + SideNav avatar)
- [ ] DevTools Network: confirm only one `getClawSettings` round-trip fires when both SideNav and chat page are mounted (already the case after PR #1865, this PR doesn't change that)

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## 02bb585 — fix(enterprise-admin): match org users api (#1871)

- **Author:** bill-srp
- **Date:** 2026-05-23T04:41:24Z
- **SHA:** 02bb585061a81b84dd198eb7763fd745d16863c0

### Commit Message

```
fix(enterprise-admin): match org users api (#1871)

## Summary
- match the users page to the deployed org users API shape
- consume raw user arrays and filter/page client-side
- update invite typing to the batch invite response
- remove the unsupported user removal action
- align org typing with backend-owned billing fields

## Root cause
The frontend still expected earlier users/org API contracts: paginated
user responses, single invite metadata, removable users, and
frontend-visible billing_team fields. The backend account/org APIs now
expose different shapes.

## Test plan
- [x] pnpm --filter @zooclaw/enterprise-admin exec vitest run --config
./vitest.config.mts hooks/__tests__/useUsers.test.tsx
hooks/__tests__/useOrg.test.tsx
app/\(dashboard\)/users/__tests__/useUsersViewModel.test.tsx
app/\(dashboard\)/users/__tests__/users-page.test.tsx
components/users/__tests__/InviteDialog.test.tsx
components/users/__tests__/UserActions.test.tsx
components/users/__tests__/UserTable.test.tsx
app/\(dashboard\)/org/__tests__/org-page.test.tsx
app/onboarding/__tests__/onboarding-page.test.tsx
- [x] pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- [x] pnpm --filter @zooclaw/enterprise-admin lint
```

### PR #1871 Body

## Summary
- match the users page to the deployed org users API shape
- consume raw user arrays and filter/page client-side
- update invite typing to the batch invite response
- remove the unsupported user removal action
- align org typing with backend-owned billing fields

## Root cause
The frontend still expected earlier users/org API contracts: paginated user responses, single invite metadata, removable users, and frontend-visible billing_team fields. The backend account/org APIs now expose different shapes.

## Test plan
- [x] pnpm --filter @zooclaw/enterprise-admin exec vitest run --config ./vitest.config.mts hooks/__tests__/useUsers.test.tsx hooks/__tests__/useOrg.test.tsx app/\(dashboard\)/users/__tests__/useUsersViewModel.test.tsx app/\(dashboard\)/users/__tests__/users-page.test.tsx components/users/__tests__/InviteDialog.test.tsx components/users/__tests__/UserActions.test.tsx components/users/__tests__/UserTable.test.tsx app/\(dashboard\)/org/__tests__/org-page.test.tsx app/onboarding/__tests__/onboarding-page.test.tsx
- [x] pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- [x] pnpm --filter @zooclaw/enterprise-admin lint

---

## 319ad04 — fix(enterprise-admin): proxy account api requests (#1870)

- **Author:** bill-srp
- **Date:** 2026-05-23T04:21:11Z
- **SHA:** 319ad04885cf1a169a363ad497c5e60f34a36893

### Commit Message

```
fix(enterprise-admin): proxy account api requests (#1870)

## Summary
- add a Next.js BFF proxy for claw-interface requests
- route enterprise-admin API calls through /api/claw so browser requests
do not depend on direct backend CORS/env exposure
- update login/auth hydration to use claw /account and /account/me
response models
- validate deploy-time env for NEXT_PUBLIC_ACCOUNT_URL and
CLAW_INTERFACE_URL

## Tests
- pnpm --filter @zooclaw/enterprise-admin exec vitest run --config
./vitest.config.mts lib/__tests__/api.test.ts
lib/__tests__/claw-proxy.test.ts lib/__tests__/auth.test.ts
- pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --filter @zooclaw/enterprise-admin lint
```

### PR #1870 Body

## Summary
- add a Next.js BFF proxy for claw-interface requests
- route enterprise-admin API calls through /api/claw so browser requests do not depend on direct backend CORS/env exposure
- update login/auth hydration to use claw /account and /account/me response models
- validate deploy-time env for NEXT_PUBLIC_ACCOUNT_URL and CLAW_INTERFACE_URL

## Tests
- pnpm --filter @zooclaw/enterprise-admin exec vitest run --config ./vitest.config.mts lib/__tests__/api.test.ts lib/__tests__/claw-proxy.test.ts lib/__tests__/auth.test.ts
- pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit
- pnpm --filter @zooclaw/enterprise-admin lint

---

## 661b513 — refactor(claw-interface): cut warm-pool provisioning to assets (#1856)

- **Author:** tim-srp
- **Date:** 2026-05-23T02:52:47Z
- **SHA:** 661b513b2c4c4c7188a181fc5688789083083900

### Commit Message

```
refactor(claw-interface): cut warm-pool provisioning to assets (#1856)

## Summary
- cut warm-pool provisioning and cleanup over to `ecap-warm-pool-assets`
- add warm-pool-specific OpenClaw helpers for app creation, bot
creation, and readiness updates without touching `ecap-account`
- update warm-pool unit coverage to assert the new assets path and
remove old account-path expectations

## Phase
- Phase 2 of warm-pool assets migration
- behavior-changing phase
- intended to pair with clear-pool release before rollout

## What changed
- `warm_pool_provisioner` now initializes/updates pre-claim state in
`ecap-warm-pool-assets`
- expired/failed cleanup now reads assets and marks assets as
`discarded`
- warm-pool provisioning no longer pre-creates or mutates `ecap-account`
- new helper coverage added for:
  - `ensure_app_for_warm_pool`
  - `create_and_start_bot_for_warm_pool`
  - `check_and_update_bot_ready_for_warm_pool`

## Local verification
Passed:
- `pytest
services/claw-interface/tests/unit/test_warm_pool_additional_coverage.py
services/claw-interface/tests/unit/test_warm_pool_assets_repo.py
services/claw-interface/tests/unit/test_billing_warm_pool.py
services/claw-interface/tests/unit/test_warm_pool_provisioning_assets.py
services/claw-interface/tests/unit/test_warm_pool_openclaw_assets.py -q`
- `ruff check
services/claw-interface/app/services/warm_pool_provisioner.py
services/claw-interface/app/services/openclaw/bot_lifecycle.py
services/claw-interface/app/services/openclaw/bot_init.py
services/claw-interface/tests/unit/test_warm_pool_additional_coverage.py
services/claw-interface/tests/unit/test_warm_pool_provisioning_assets.py
services/claw-interface/tests/unit/test_warm_pool_openclaw_assets.py`

Known repo-local blockers in this worktree (not introduced by this PR):
- `pyright app tests` fails on broad missing third-party imports in the
current local env
- `pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` is
interrupted by existing BDD dependency/deprecation collection errors
(`pytest_bdd`, `python_multipart` warning handling)
```

### PR #1856 Body

## Summary
- cut warm-pool provisioning and cleanup over to `ecap-warm-pool-assets`
- add warm-pool-specific OpenClaw helpers for app creation, bot creation, and readiness updates without touching `ecap-account`
- update warm-pool unit coverage to assert the new assets path and remove old account-path expectations

## Phase
- Phase 2 of warm-pool assets migration
- behavior-changing phase
- intended to pair with clear-pool release before rollout

## What changed
- `warm_pool_provisioner` now initializes/updates pre-claim state in `ecap-warm-pool-assets`
- expired/failed cleanup now reads assets and marks assets as `discarded`
- warm-pool provisioning no longer pre-creates or mutates `ecap-account`
- new helper coverage added for:
  - `ensure_app_for_warm_pool`
  - `create_and_start_bot_for_warm_pool`
  - `check_and_update_bot_ready_for_warm_pool`

## Local verification
Passed:
- `pytest services/claw-interface/tests/unit/test_warm_pool_additional_coverage.py services/claw-interface/tests/unit/test_warm_pool_assets_repo.py services/claw-interface/tests/unit/test_billing_warm_pool.py services/claw-interface/tests/unit/test_warm_pool_provisioning_assets.py services/claw-interface/tests/unit/test_warm_pool_openclaw_assets.py -q`
- `ruff check services/claw-interface/app/services/warm_pool_provisioner.py services/claw-interface/app/services/openclaw/bot_lifecycle.py services/claw-interface/app/services/openclaw/bot_init.py services/claw-interface/tests/unit/test_warm_pool_additional_coverage.py services/claw-interface/tests/unit/test_warm_pool_provisioning_assets.py services/claw-interface/tests/unit/test_warm_pool_openclaw_assets.py`

Known repo-local blockers in this worktree (not introduced by this PR):
- `pyright app tests` fails on broad missing third-party imports in the current local env
- `pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` is interrupted by existing BDD dependency/deprecation collection errors (`pytest_bdd`, `python_multipart` warning handling)


---

## 3016089 — refactor(web): extract SideNav identity loading into useNavIdentity hook (#1865)

- **Author:** Chris@ZooClaw
- **Date:** 2026-05-23T02:27:03Z
- **SHA:** 3016089cbb8b9f8f3e03259b2c15f9773227b2d5

### Commit Message

```
refactor(web): extract SideNav identity loading into useNavIdentity hook (#1865)

## Summary

Closes the SideNav-side half of finding **F2** (duplicate identity
loading between SideNav and GenClawClient) and the identity-loading
slice of **F11** (1056-line god component) from arch-review issue #368.

- New hook `web/app/src/hooks/useNavIdentity.ts` shares the
`openclawKeys.clawIdentity` + `openclawKeys.agentSettings` react-query
buckets with `useChatIdentity` + `useAgentSettingsQuery`, so when both
SideNav and the chat page are mounted only one network round-trip fires
per identity (was two timers running side-by-side).
- `useQueries` replaces the hand-written sequential loop with 500ms
rate-limit-avoiding delays. The active-agent query already cached by the
chat page becomes a cache hit (zero re-fetch).
- Same-tab `OPENCLAW_*_IDENTITY_UPDATED_EVENT` listeners now patch the
react-query cache directly via `setQueryData`, eliminating the
per-component state-sync ladder.
- `SideNav.tsx` 1056 → 935 lines: removes two `useState`, two
`useEffect` blocks (event listener + raw fetch loop), and 5 imports from
`openclaw-identity-cache` / `openclaw-settings`.

`SideNav.tsx` remains in the legacy-complexity override list because the
remaining 5 responsibilities (subscription/credits, locale switcher,
agent list scroll, user menu, avatar hydration) still push the file over
the 600-line `max-lines` threshold. That cleanup is tracked as a
follow-up sequence under issue #368.

## Test plan

- [x] `pnpm tsc` clean
- [x] `pnpm lint` clean (including pre-commit hook)
- [x] `pnpm test:unit` — 361 files / 5620 tests pass (no regressions in
`useAgentSettings`, `openclaw-identity-cache`, `AgentIdentitySection`
specs)
- [ ] Manual smoke on staging: chat page + SideNav identity render
unchanged; settings page identity edit propagates to SideNav avatar in
same tab; cross-tab `storage` event still updates auth state
- [ ] DevTools Network: confirm `getClawSettings` and `getAgentSettings`
for the active agent fire only once when both SideNav and `/chat` are
mounted (was two requests pre-PR)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Production latency (real measurement — 2026-05-22)

DevTools console fetch directly to the BFF batch endpoint on prod, my
account (8 agents):

| Run | Time |
|---|---|
| 1 | 1064 ms |
| 2 | 593 ms |
| 3 | 771 ms |
| 4 | 990 ms |
| 5 | 557 ms |
| **avg** | **795 ms** |

For comparison, prod legacy SideNav with 8 agents (sequential GET +
500ms throttle per `openclaw-agent-settings.ts:86-92`):

| Scenario | Total | Source |
|---|---|---|
| **Batch (this PR)** | **~800ms** | measured |
| Sequential + 500ms (current prod) | ~12-15s | `8 × ~1.5s + 7 × 500ms`
|
| Sequential + 429 retry overhead | ~15-17s | observed: single per-agent
samples ranged 1.1-1.9s; the 1.9s outlier likely included a +1s
429-retry from the rate-limit edge |

~15× total-time improvement. Also eliminates the client-side 429-retry
overhead because batch is one endpoint hit (cannot trip 10 calls / 5s on
its own).

## Reviewer feedback addressed

| Round | Finding | Resolution |
|---|---|---|
| Codex r1 — cross-session leak | `setCached*` in queryFn could persist
a prior user's identity after logout | Hoisted into `useEffect` gated on
`[query.data, uid]` (commit `55316023`) |
| Codex r1 — rate-limit risk | Per-agent `useQueries` would burst past
10 calls / 5s | Replaced with single batch `POST
/openclaw/settings/agents` (commit `55316023`) |
| Claude r1 — channels shape mismatch | `useNavIdentity` clawIdentity
queryFn omitted `channels`, could strip the field from `useChatIdentity`
subscribers | Shape aligned: `{name, emoji, avatar, channels}` (commit
`55316023`) |
| Codex r2 — staleTime drift from useChatIdentity | New queries used
default 30s staleTime while `useChatIdentity` is `refetchOnMount:
'always'` | Added `refetchOnMount: 'always'` to both queries (commit
`e0aae30c`) |
| Codex r2 — no regression test | Behavior-preserving refactor; per
Claude's review feedback | Deferred to issue #368 cleanup sequence |

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1865 Body

## Summary

Closes the SideNav-side half of finding **F2** (duplicate identity loading between SideNav and GenClawClient) and the identity-loading slice of **F11** (1056-line god component) from arch-review issue #368.

- New hook `web/app/src/hooks/useNavIdentity.ts` shares the `openclawKeys.clawIdentity` + `openclawKeys.agentSettings` react-query buckets with `useChatIdentity` + `useAgentSettingsQuery`, so when both SideNav and the chat page are mounted only one network round-trip fires per identity (was two timers running side-by-side).
- `useQueries` replaces the hand-written sequential loop with 500ms rate-limit-avoiding delays. The active-agent query already cached by the chat page becomes a cache hit (zero re-fetch).
- Same-tab `OPENCLAW_*_IDENTITY_UPDATED_EVENT` listeners now patch the react-query cache directly via `setQueryData`, eliminating the per-component state-sync ladder.
- `SideNav.tsx` 1056 → 935 lines: removes two `useState`, two `useEffect` blocks (event listener + raw fetch loop), and 5 imports from `openclaw-identity-cache` / `openclaw-settings`.

`SideNav.tsx` remains in the legacy-complexity override list because the remaining 5 responsibilities (subscription/credits, locale switcher, agent list scroll, user menu, avatar hydration) still push the file over the 600-line `max-lines` threshold. That cleanup is tracked as a follow-up sequence under issue #368.

## Test plan

- [x] `pnpm tsc` clean
- [x] `pnpm lint` clean (including pre-commit hook)
- [x] `pnpm test:unit` — 361 files / 5620 tests pass (no regressions in `useAgentSettings`, `openclaw-identity-cache`, `AgentIdentitySection` specs)
- [ ] Manual smoke on staging: chat page + SideNav identity render unchanged; settings page identity edit propagates to SideNav avatar in same tab; cross-tab `storage` event still updates auth state
- [ ] DevTools Network: confirm `getClawSettings` and `getAgentSettings` for the active agent fire only once when both SideNav and `/chat` are mounted (was two requests pre-PR)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Production latency (real measurement — 2026-05-22)

DevTools console fetch directly to the BFF batch endpoint on prod, my account (8 agents):

| Run | Time |
|---|---|
| 1 | 1064 ms |
| 2 | 593 ms |
| 3 | 771 ms |
| 4 | 990 ms |
| 5 | 557 ms |
| **avg** | **795 ms** |

For comparison, prod legacy SideNav with 8 agents (sequential GET + 500ms throttle per `openclaw-agent-settings.ts:86-92`):

| Scenario | Total | Source |
|---|---|---|
| **Batch (this PR)** | **~800ms** | measured |
| Sequential + 500ms (current prod) | ~12-15s | `8 × ~1.5s + 7 × 500ms` |
| Sequential + 429 retry overhead | ~15-17s | observed: single per-agent samples ranged 1.1-1.9s; the 1.9s outlier likely included a +1s 429-retry from the rate-limit edge |

~15× total-time improvement. Also eliminates the client-side 429-retry overhead because batch is one endpoint hit (cannot trip 10 calls / 5s on its own).

## Reviewer feedback addressed

| Round | Finding | Resolution |
|---|---|---|
| Codex r1 — cross-session leak | `setCached*` in queryFn could persist a prior user's identity after logout | Hoisted into `useEffect` gated on `[query.data, uid]` (commit `55316023`) |
| Codex r1 — rate-limit risk | Per-agent `useQueries` would burst past 10 calls / 5s | Replaced with single batch `POST /openclaw/settings/agents` (commit `55316023`) |
| Claude r1 — channels shape mismatch | `useNavIdentity` clawIdentity queryFn omitted `channels`, could strip the field from `useChatIdentity` subscribers | Shape aligned: `{name, emoji, avatar, channels}` (commit `55316023`) |
| Codex r2 — staleTime drift from useChatIdentity | New queries used default 30s staleTime while `useChatIdentity` is `refetchOnMount: 'always'` | Added `refetchOnMount: 'always'` to both queries (commit `e0aae30c`) |
| Codex r2 — no regression test | Behavior-preserving refactor; per Claude's review feedback | Deferred to issue #368 cleanup sequence |


---

