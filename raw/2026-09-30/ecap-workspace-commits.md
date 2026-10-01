# SerendipityOneInc/ecap-workspace — commits 2026-09-30

## fix(chat): keep Stop available for running tasks after navigation (#3961)

- **SHA**: `5509dcd98dc2d377cb109d901748cd73db1121b2`
- **作者**: tim-srp
- **日期**: 2026-09-30T17:38:12Z
- **PR**: #3961

### Commit Message

```
fix(chat): keep Stop available for running tasks after navigation (#3961)
```

### PR Body

```
## Summary
- Restore the Stop control for an in-flight Engine v2 turn after refreshing or navigating away and back.
- Reconstruct running state from thread history while preserving v1 `turn_status` heartbeat behavior.
- Avoid false-positive Stop controls after a hidden `/stop` post or when opening an old, expired run from a long-lived view.
- Clear the stopped session's provider waiting state and synchronize its stop post, so switching threads does not resurrect Stop or hide it for a subsequent new turn.
- In Agent Builder, hide Stop after a successful stop and refetch the thread history so a remount does not reuse pre-stop history when the WebSocket echo is missed.

## Root cause
The in-memory waiting flag is lost when the chat provider remounts. The fallback status reconstruction only recognized v1 `turn_status` posts, while v2 uses `assistant_segment` and `tool_status` posts. Follow-up review also found stale provider state and delayed stop-post delivery could falsely show Stop after cancellation.

## Verification
- Initial regression tests failed against `main` (3 expected failures) and pass with this fix.
- Cancellation and stale-view tests failed against the initial PR head and pass after the review fixes.
- New session-switch and Agent Builder tests fail without their respective follow-up fixes and pass with them.
- Agent Builder remount test fails without the history refetch and passes with it.
- Latest focused verification: 76/76 tests, typecheck, lint, and guards passed.
- Related suites: 49 files, 630/630 tests passed.
- `bash scripts/verify-changed.sh` and commit/push hooks passed.

## Remaining caveat
If an Engine v2 run fails without writing a final/error segment, an inactive run may be shown as running for up to 30 minutes. After a successful Builder stop, a brief Stop flash remains possible if the user remounts before the refetch completes; a failed refetch leaves stale history until the next successful fetch. The separate Engine v2 channel bridge is not available in this repository, so these paths were not verified in staging.
```

---

## fix(pricing): continue Pro entry to plan management (#3962)

- **SHA**: `41ecb2799ceaffa3c3db6a29fcdc2c3c539c3b47`
- **作者**: ericma-srp
- **日期**: 2026-09-30T17:30:48Z
- **PR**: #3962

### Commit Message

```
fix(pricing): continue Pro entry to plan management (#3962)

## Summary

Pricing's Pro buttons currently force a login prompt and leave users on
the pricing page after authentication. Both entry points now reuse a
verified session, or continue to Manage plan after login, including
OAuth redirects.

- Signed-out users log in, then continue to the existing plan dialog.
Signed-in non-Pro and expired users skip login and use the existing Get
started / Resubscribe flow.
- Existing Pro subscribers see Manage Subscription and enter the
existing subscription and payment-management flow.
- Keep the dialog on `/subscription` until it closes, preventing
workspace onboarding from opening underneath it for first-time
subscribers. Preserve the existing landing destination on close.
- Restore the pricing-to-plan analytics handoff and clear it when login
is canceled.

This is a frontend-only behavior change, plus tests and tracking
documentation. It does not change backend APIs, prices, entitlements,
catalog restrictions, Stripe handling, or billing state rules. Opening
the entry does not create an order; checkout still requires confirmation
in the existing dialog. The local scenario hub and mock billing pages
are excluded from this PR.

## Validation

Latest commit: `4aadf7f6d`. All applicable CI checks passed; CodeQL and
both automated reviews report no blocking findings. The full web suite
passed: 877 files, 11,013 tests passed, 70 skipped, 1 todo.

- 126 targeted unit tests passed across pricing, authentication
continuation, subscription entry, existing plan actions, translations,
and tracking.
- The existing specialist-return regression tests now assert that
navigation happens on dialog close, preserving both `?sp=` and the plain
`/chat` fallback.
- TypeScript, ESLint, and frontend governance guards passed.
- Seven browser scenarios passed with the real frontend and mocked
authentication/billing responses: signed out, free, active Pro, expired,
sign-in to an existing Pro account, payment failure, and Chinese active
Pro.
- All seven scenarios produced zero order/checkout requests before
confirmation. Get started / Resubscribe used the existing order and
checkout endpoints; Update payment method used the existing
customer-portal endpoint.
- Real Google/phone authentication and real Stripe payment were not
exercised; browser evidence is local simulation, not production payment
verification.
```

### PR Body

```
## Summary

Pricing's Pro buttons currently force a login prompt and leave users on the pricing page after authentication. Both entry points now reuse a verified session, or continue to Manage plan after login, including OAuth redirects.

- Signed-out users log in, then continue to the existing plan dialog. Signed-in non-Pro and expired users skip login and use the existing Get started / Resubscribe flow.
- Existing Pro subscribers see Manage Subscription and enter the existing subscription and payment-management flow.
- Keep the dialog on `/subscription` until it closes, preventing workspace onboarding from opening underneath it for first-time subscribers. Preserve the existing landing destination on close.
- Restore the pricing-to-plan analytics handoff and clear it when login is canceled.

This is a frontend-only behavior change, plus tests and tracking documentation. It does not change backend APIs, prices, entitlements, catalog restrictions, Stripe handling, or billing state rules. Opening the entry does not create an order; checkout still requires confirmation in the existing dialog. The local scenario hub and mock billing pages are excluded from this PR.

## Validation

Latest commit: `4aadf7f6d`. All applicable CI checks passed; CodeQL and both automated reviews report no blocking findings. The full web suite passed: 877 files, 11,013 tests passed, 70 skipped, 1 todo.

- 126 targeted unit tests passed across pricing, authentication continuation, subscription entry, existing plan actions, translations, and tracking.
- The existing specialist-return regression tests now assert that navigation happens on dialog close, preserving both `?sp=` and the plain `/chat` fallback.
- TypeScript, ESLint, and frontend governance guards passed.
- Seven browser scenarios passed with the real frontend and mocked authentication/billing responses: signed out, free, active Pro, expired, sign-in to an existing Pro account, payment failure, and Chinese active Pro.
- All seven scenarios produced zero order/checkout requests before confirmation. Get started / Resubscribe used the existing order and checkout endpoints; Update payment method used the existing customer-portal endpoint.
- Real Google/phone authentication and real Stripe payment were not exercised; browser evidence is local simulation, not production payment verification.
```

---

## feat(landing): align marketing footer with nav (Product / Use Cases / Resources), fix DMCA label (#3957)

- **SHA**: `71940e63b846e8402a9a9a875fef24cc9ac61a77`
- **作者**: Mori-srp
- **日期**: 2026-09-30T14:47:40Z
- **PR**: #3957

### Commit Message

```
feat(landing): align marketing footer with nav (Product / Use Cases / Resources), fix DMCA label (#3957)

## Linear
N/A

## Summary
Reorganizes the marketing footer (spec approved by David):
- **Product**: Agent Builder → /home · Managed Agent API (non-clickable,
"Coming soon" badge; data keeps https://platform.zoowork.ai +
`comingSoon` flag so it becomes a link by flipping one flag once DNS is
live) · Enterprise → /enterprise · iOS App (existing QR popup,
unchanged) · ZooData → https://zoodata.ai (new tab)
- **Use Cases** (new column title, replaces Industry): Solutions →
/solutions · Agent Gallery · the 9 existing industry pages (unchanged)
- **Resources**: Pricing → /pricing · Blog · Docs
- **Company**: unchanged, label typo DCMA → DMCA in all 10 locales
- Removed from footer: Web App, Learn, What's New. Removed the
now-unused `onWebApp` / footer `tips` plumbing (top nav still uses
`tips`). Locale keys `footerWebApp`, `resLearn`, `resWhatsNew`,
`footerIndustry` kept.
- New locale keys: `footerUseCases`, `footerAgentBuilder`,
`footerManagedAgentApi`, `footerComingSoon` (all 10 locales).

## Test plan
- [x] Updated landing-content, landing-footer, marketing-chrome and
legal-footer-links unit tests (new columns/order, /home link,
coming-soon renders as non-link text, DMCA, new labels)
- [x] Full unit suite, `tsc --noEmit`, `lint`, `lint:ci` pass locally
- [x] Rendered `/` and `/zh` locally at 1440px and checked the EN / ZH
footer (screenshots available on request)

## Follow-ups (not in this PR)
- Tips pages (/tips/) lose their main-site footer link. Add
`/tips/sitemap.xml` (and `/blog/sitemap-index.xml`) to the root sitemap
index so they stay discoverable.
- Decide whether to noindex `/home` (empty initial HTML, currently
index,follow).
- Top-nav alignment (e.g. a Product dropdown, ZooData placement) is
pending.
- Switch Managed Agent API to a real link once platform.zoowork.ai
resolves.
- Sync the blog (zooclaw-blog) and agent-gallery footer copies (also fix
DCMA in gallery-chrome.tsx).

---

## 概要
按 David 批准的方案调整官网页脚：
- **产品**：Agent Builder → /home · Managed Agent API（不可点击，带「即将推出」标记；数据里保留
https://platform.zoowork.ai 和 `comingSoon` 标志，域名解析上线后改一个标志即可变成链接）· 企业版 →
/enterprise · iOS 应用（沿用二维码弹窗）· ZooData → https://zoodata.ai（新标签页）
- **应用场景**（新列名，取代「行业」列）：解决方案 → /solutions · Agent Gallery · 原有 9
个行业页（不变）
- **资源**：定价 → /pricing · 博客 · 文档
- **公司**：不变，10 个语言的 DCMA 拼写错误改为 DMCA
- 页脚去掉 Web App、学习、更新日志，并删除不再使用的 `onWebApp` 和页脚 `tips` 相关代码（顶部导航仍使用
`tips`）。保留 `footerWebApp`、`resLearn`、`resWhatsNew`、`footerIndustry` 文案
key。
- 新增文案
key：`footerUseCases`、`footerAgentBuilder`、`footerManagedAgentApi`、`footerComingSoon`（10
种语言）。

## 测试
- 更新 landing-content、landing-footer、marketing-chrome、legal-footer-links
单测（新列和顺序、/home 链接、「即将推出」渲染为不可点击文字、DMCA、新文案）。
- 本地全量单测、`tsc --noEmit`、`lint`、`lint:ci` 均通过。
- 本地以 1440px 渲染 `/` 和 `/zh` 检查中英文页脚（截图可按需提供）。

## 后续（不在本 PR）
- Tips 页面（/tips/）失去主站页脚入口，建议把 `/tips/sitemap.xml`（及
`/blog/sitemap-index.xml`）加入根 sitemap 索引，保证可被搜索引擎发现。
- `/home` 是否加 noindex（初始 HTML 为空，目前 index,follow）待定。
- 顶部导航对齐（如「产品」下拉菜单、ZooData 位置）待定。
- platform.zoowork.ai 解析上线后，把 Managed Agent API 改为真实链接。
- 同步博客站（zooclaw-blog）和 agent-gallery 的页脚副本（gallery-chrome.tsx 里也有 DCMA）。
```

### PR Body

```
## Linear
N/A

## Summary
Reorganizes the marketing footer (spec approved by David):
- **Product**: Agent Builder → /home · Managed Agent API (non-clickable, "Coming soon" badge; data keeps https://platform.zoowork.ai + `comingSoon` flag so it becomes a link by flipping one flag once DNS is live) · Enterprise → /enterprise · iOS App (existing QR popup, unchanged) · ZooData → https://zoodata.ai (new tab)
- **Use Cases** (new column title, replaces Industry): Solutions → /solutions · Agent Gallery · the 9 existing industry pages (unchanged)
- **Resources**: Pricing → /pricing · Blog · Docs
- **Company**: unchanged, label typo DCMA → DMCA in all 10 locales
- Removed from footer: Web App, Learn, What's New. Removed the now-unused `onWebApp` / footer `tips` plumbing (top nav still uses `tips`). Locale keys `footerWebApp`, `resLearn`, `resWhatsNew`, `footerIndustry` kept.
- New locale keys: `footerUseCases`, `footerAgentBuilder`, `footerManagedAgentApi`, `footerComingSoon` (all 10 locales).

## Test plan
- [x] Updated landing-content, landing-footer, marketing-chrome and legal-footer-links unit tests (new columns/order, /home link, coming-soon renders as non-link text, DMCA, new labels)
- [x] Full unit suite, `tsc --noEmit`, `lint`, `lint:ci` pass locally
- [x] Rendered `/` and `/zh` locally at 1440px and checked the EN / ZH footer (screenshots available on request)

## Follow-ups (not in this PR)
- Tips pages (/tips/) lose their main-site footer link. Add `/tips/sitemap.xml` (and `/blog/sitemap-index.xml`) to the root sitemap index so they stay discoverable.
- Decide whether to noindex `/home` (empty initial HTML, currently index,follow).
- Top-nav alignment (e.g. a Product dropdown, ZooData placement) is pending.
- Switch Managed Agent API to a real link once platform.zoowork.ai resolves.
- Sync the blog (zooclaw-blog) and agent-gallery footer copies (also fix DCMA in gallery-chrome.tsx).

---

## 概要
按 David 批准的方案调整官网页脚：
- **产品**：Agent Builder → /home · Managed Agent API（不可点击，带「即将推出」标记；数据里保留 https://platform.zoowork.ai 和 `comingSoon` 标志，域名解析上线后改一个标志即可变成链接）· 企业版 → /enterprise · iOS 应用（沿用二维码弹窗）· ZooData → https://zoodata.ai（新标签页）
- **应用场景**（新列名，取代「行业」列）：解决方案 → /solutions · Agent Gallery · 原有 9 个行业页（不变）
- **资源**：定价 → /pricing · 博客 · 文档
- **公司**：不变，10 个语言的 DCMA 拼写错误改为 DMCA
- 页脚去掉 Web App、学习、更新日志，并删除不再使用的 `onWebApp` 和页脚 `tips` 相关代码（顶部导航仍使用 `tips`）。保留 `footerWebApp`、`resLearn`、`resWhatsNew`、`footerIndustry` 文案 key。
- 新增文案 key：`footerUseCases`、`footerAgentBuilder`、`footerManagedAgentApi`、`footerComingSoon`（10 种语言）。

## 测试
- 更新 landing-content、landing-footer、marketing-chrome、legal-footer-links 单测（新列和顺序、/home 链接、「即将推出」渲染为不可点击文字、DMCA、新文案）。
- 本地全量单测、`tsc --noEmit`、`lint`、`lint:ci` 均通过。
- 本地以 1440px 渲染 `/` 和 `/zh` 检查中英文页脚（截图可按需提供）。

## 后续（不在本 PR）
- Tips 页面（/tips/）失去主站页脚入口，建议把 `/tips/sitemap.xml`（及 `/blog/sitemap-index.xml`）加入根 sitemap 索引，保证可被搜索引擎发现。
- `/home` 是否加 noindex（初始 HTML 为空，目前 index,follow）待定。
- 顶部导航对齐（如「产品」下拉菜单、ZooData 位置）待定。
- platform.zoowork.ai 解析上线后，把 Managed Agent API 改为真实链接。
- 同步博客站（zooclaw-blog）和 agent-gallery 的页脚副本（gallery-chrome.tsx 里也有 DCMA）。
```

---

## fix(platform): enable billing and runtime without activation flags (#3955)

- **SHA**: `6de207c9d52992028b913254520bf04728da2059`
- **作者**: finn-srp
- **日期**: 2026-09-30T13:19:57Z
- **PR**: #3955

### Commit Message

```
fix(platform): enable billing and runtime without activation flags (#3955)

## Summary

Platform billing and Project-key runtime are implemented, but default
activation settings still hide them. Remove `PLATFORM_BILLING_ENABLED`
and `SERVICE_API_AUTH_MODE`; `/service/v1` now accepts both Work `zct_`
tokens and Platform `zwp_live_` keys through separate namespace-selected
authenticators. Fix the Platform account business to `ecap-platform` and
remove the redundant `API_PLATFORM_BUSINESS` setting.

Keep existing Work token creation, storage, hashing, JWT encryption,
membership checks, billing credentials, compute policy and Engine
attribution unchanged. Preserve the original Work error code for
missing/non-service credentials. Keep Platform storage readiness,
ownership, credits and payment checks. Existing frontend URL,
encryption, billing and Engine configuration remains required.

Remove UI notices claiming API keys cannot run Agents, and update the
current operations documentation. Usage APIs are available; the frontend
Usage page remains a placeholder.

## Root cause

The old rollout settings defaulted billing off and service
authentication to Work-only, even after Platform Org billing and runtime
integration landed. They were also configurable across both products, so
replacing them must preserve the existing Work authentication path.

Rollout follows the requested sequence: remove the flags, deploy
staging, then complete staging end-to-end validation before considering
production. The current Service and Platform workflows deploy main
pushes to staging; production requires a separate release tag or
explicit production workflow dispatch. This PR does not initiate
production promotion. The automatic review's rollout-sequencing note
does not require restoring a flag or changing Work key configuration.

## Test plan

- [x] Work compatibility checks through HTTP and the real
dispatch/authentication functions, with real token hashing and JWT
encryption: existing-key Agent creation and credential seeding, Work
usage attribution, revoked/unknown keys, suspended membership and
tampered ciphertext. Database and Engine calls are mocked.
- [x] 65 targeted Work/Platform authentication and proxy tests.
- [x] Node 24 Platform `pnpm lint`, `pnpm typecheck`, `pnpm test` (27
tests), and `pnpm build` on the final rebased commit.
- [x] Final rebased commit: local `ecap-verify-py-ci` (Linux
dependencies, static checks, all ci-lint guards, both duplication
checks, full pytest and coverage): 13,347 passed, 5 skipped; 89.89%
coverage against the 89.5% CI threshold.
- [ ] Staging end-to-end login, top-up and billable Agent execution
after deployment; this PR does not run live billing tests or modify
deployed secrets.
```

### PR Body

```
## Summary

Platform billing and Project-key runtime are implemented, but default activation settings still hide them. Remove `PLATFORM_BILLING_ENABLED` and `SERVICE_API_AUTH_MODE`; `/service/v1` now accepts both Work `zct_` tokens and Platform `zwp_live_` keys through separate namespace-selected authenticators. Fix the Platform account business to `ecap-platform` and remove the redundant `API_PLATFORM_BUSINESS` setting.

Keep existing Work token creation, storage, hashing, JWT encryption, membership checks, billing credentials, compute policy and Engine attribution unchanged. Preserve the original Work error code for missing/non-service credentials. Keep Platform storage readiness, ownership, credits and payment checks. Existing frontend URL, encryption, billing and Engine configuration remains required.

Remove UI notices claiming API keys cannot run Agents, and update the current operations documentation. Usage APIs are available; the frontend Usage page remains a placeholder.

## Root cause

The old rollout settings defaulted billing off and service authentication to Work-only, even after Platform Org billing and runtime integration landed. They were also configurable across both products, so replacing them must preserve the existing Work authentication path.

Rollout follows the requested sequence: remove the flags, deploy staging, then complete staging end-to-end validation before considering production. The current Service and Platform workflows deploy main pushes to staging; production requires a separate release tag or explicit production workflow dispatch. This PR does not initiate production promotion. The automatic review's rollout-sequencing note does not require restoring a flag or changing Work key configuration.

## Test plan

- [x] Work compatibility checks through HTTP and the real dispatch/authentication functions, with real token hashing and JWT encryption: existing-key Agent creation and credential seeding, Work usage attribution, revoked/unknown keys, suspended membership and tampered ciphertext. Database and Engine calls are mocked.
- [x] 65 targeted Work/Platform authentication and proxy tests.
- [x] Node 24 Platform `pnpm lint`, `pnpm typecheck`, `pnpm test` (27 tests), and `pnpm build` on the final rebased commit.
- [x] Final rebased commit: local `ecap-verify-py-ci` (Linux dependencies, static checks, all ci-lint guards, both duplication checks, full pytest and coverage): 13,347 passed, 5 skipped; 89.89% coverage against the 89.5% CI threshold.
- [ ] Staging end-to-end login, top-up and billable Agent execution after deployment; this PR does not run live billing tests or modify deployed secrets.
```

---

## fix(builder): treat Mattermost's not-a-member 400 as a clean team removal (#3956)

- **SHA**: `e271cd7d51effb66dbef6eed54c9829dae3eec9e`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-30T12:57:24Z
- **PR**: #3956

### Commit Message

```
fix(builder): treat Mattermost's not-a-member 400 as a clean team removal (#3956)

## Summary
`MattermostClient.remove_user_from_team` treated only 404 as "membership
already gone". When the user isn't on the team, Mattermost responds with
**400** and error id `api.team.remove_user_from_team.missing.app_error`
("The user does not appear to be part of this team";
`server/channels/app/team.go` `leaveTeam`, `mattermost/mattermost`). A
Builder bot joins the org team lazily: only when its first session
channel is ensured (`session_channel_service` →
`ensure_builder_team_membership`) or when ingress is restored. A Project
whose setup failed before anyone opened its chat therefore has a bot
that never joined the team. Idle-ingress release and archived-runtime
cleanup still try to remove that membership, hit the 400, release their
lease, and retry every hour indefinitely.

Change:
- Accept that specific 400 as already clean, just like 404.
- Keep raising every other 400, and log its Mattermost error id
(`[MATTERMOST] remove_user_from_team rejected …`) so the next unexpected
rejection is diagnosable. Today the log only shows `400 Bad Request`.
- Move the error-id parsing that `add_user_to_team` already did
(team-full detection) into a shared `_error_id` helper.

## Evidence (staging, after #3833 deployed as `staging-bf83aab`)
A manual `cleanup_agent_builder_runtime` run (`cron-run-8e705746e42d`)
returned `processed 0 / failed 3`, the same as the scheduled 12:23 UTC
run on the previous image. All three failures raised from
`remove_builder_team_membership` → `remove_user_from_team` with `400 Bad
Request`:
- idle release: `abp_896946f3…`
- archived cleanup: `abp_5287ee46…`, `abp_135bb52c…`

Root cause, verified with read-only lookups on staging:
- Mattermost (11.5.1): both teams exist (`delete_at=0`, not
group-constrained), and all three bots exist and are active
(`is_bot=true`, `delete_at=0`). `GET /teams/{team}/members/{bot}`
returns **404 `app.team.get_member.missing.app_error`**, and `GET
/users/{bot}/teams` returns `[]`. Mattermost only soft-deletes a
membership when a user leaves (`TeamService.RemoveTeamMember` sets
`DeleteAt` via `UpdateMember`), and `GetMember` doesn't filter
`DeleteAt`. So a 404 here means these bots **never joined** the team;
they didn't leave it earlier. `leaveTeam` turns exactly that lookup miss
into the 400 `api.team.remove_user_from_team.missing.app_error`. The
handler's only other 400 (`group_constrained`) doesn't apply to bots.
- ECAP: all three Projects' setup failed
(`builder_workspace_status=failed`; the two archived ones on 2026-09-02,
about 15 min after creation, i.e. the setup timeout). Their Builder
workspaces have `mattermost.session_channel_id == ""`: no chat was ever
opened, so `ensure_builder_team_membership` never ran.

The same run also confirmed that #3833's new
`builder_setup_pending_claim_ids.0: {$exists: false}` read and the
`claim_archived` write go through staging's encrypted client without
error: all three rows were selected and claimed before failing at the
Mattermost step.

## Test plan
- New `test_remove_user_from_team_accepts_mattermost_not_member_400` and
`test_remove_user_from_team_still_raises_other_400s`. As a negative
control, removing the new branch fails exactly the first test.
- 647 unit tests pass (Mattermost client, Pack test cleanup, all Agent
Builder suites). `verify-py` passes (ruff, format, pyright,
import-linter), and so do `ci-lint` 01–08.
- After deploy: the next hourly `cleanup_agent_builder_runtime` run on
staging should clean those three Projects (`processed_count` > 0), and
archived ones should then report `builder_runtime_cleanup_complete:
true`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

```
## Summary
`MattermostClient.remove_user_from_team` treated only 404 as "membership already gone". When the user isn't on the team, Mattermost responds with **400** and error id `api.team.remove_user_from_team.missing.app_error` ("The user does not appear to be part of this team"; `server/channels/app/team.go` `leaveTeam`, `mattermost/mattermost`). A Builder bot joins the org team lazily: only when its first session channel is ensured (`session_channel_service` → `ensure_builder_team_membership`) or when ingress is restored. A Project whose setup failed before anyone opened its chat therefore has a bot that never joined the team. Idle-ingress release and archived-runtime cleanup still try to remove that membership, hit the 400, release their lease, and retry every hour indefinitely.

Change:
- Accept that specific 400 as already clean, just like 404.
- Keep raising every other 400, and log its Mattermost error id (`[MATTERMOST] remove_user_from_team rejected …`) so the next unexpected rejection is diagnosable. Today the log only shows `400 Bad Request`.
- Move the error-id parsing that `add_user_to_team` already did (team-full detection) into a shared `_error_id` helper.

## Evidence (staging, after #3833 deployed as `staging-bf83aab`)
A manual `cleanup_agent_builder_runtime` run (`cron-run-8e705746e42d`) returned `processed 0 / failed 3`, the same as the scheduled 12:23 UTC run on the previous image. All three failures raised from `remove_builder_team_membership` → `remove_user_from_team` with `400 Bad Request`:
- idle release: `abp_896946f3…`
- archived cleanup: `abp_5287ee46…`, `abp_135bb52c…`

Root cause, verified with read-only lookups on staging:
- Mattermost (11.5.1): both teams exist (`delete_at=0`, not group-constrained), and all three bots exist and are active (`is_bot=true`, `delete_at=0`). `GET /teams/{team}/members/{bot}` returns **404 `app.team.get_member.missing.app_error`**, and `GET /users/{bot}/teams` returns `[]`. Mattermost only soft-deletes a membership when a user leaves (`TeamService.RemoveTeamMember` sets `DeleteAt` via `UpdateMember`), and `GetMember` doesn't filter `DeleteAt`. So a 404 here means these bots **never joined** the team; they didn't leave it earlier. `leaveTeam` turns exactly that lookup miss into the 400 `api.team.remove_user_from_team.missing.app_error`. The handler's only other 400 (`group_constrained`) doesn't apply to bots.
- ECAP: all three Projects' setup failed (`builder_workspace_status=failed`; the two archived ones on 2026-09-02, about 15 min after creation, i.e. the setup timeout). Their Builder workspaces have `mattermost.session_channel_id == ""`: no chat was ever opened, so `ensure_builder_team_membership` never ran.

The same run also confirmed that #3833's new `builder_setup_pending_claim_ids.0: {$exists: false}` read and the `claim_archived` write go through staging's encrypted client without error: all three rows were selected and claimed before failing at the Mattermost step.

## Test plan
- New `test_remove_user_from_team_accepts_mattermost_not_member_400` and `test_remove_user_from_team_still_raises_other_400s`. As a negative control, removing the new branch fails exactly the first test.
- 647 unit tests pass (Mattermost client, Pack test cleanup, all Agent Builder suites). `verify-py` passes (ruff, format, pyright, import-linter), and so do `ci-lint` 01–08.
- After deploy: the next hourly `cleanup_agent_builder_runtime` run on staging should clean those three Projects (`processed_count` > 0), and archived ones should then report `builder_runtime_cleanup_complete: true`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## fix(builder): confirm archived runtime cleanup after setup settles (#3833)

- **SHA**: `bf83aab7757fc7946a54b9c3b22dd6c77ab5ba36`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-30T12:28:07Z
- **PR**: #3833

### Commit Message

```
fix(builder): confirm archived runtime cleanup after setup settles (#3833)

## Summary

When a Builder Project is archived while its dedicated Engine agent is
still being allocated, retain the late runtime identity and confirm
cleanup only after all acquired setup operations settle. Preserve the
existing expired-lease retry behavior; each setup adds a durable pending
token and removes only its own token in `finally`. Archive cleanup
claims and the final completion write require no pending setup tokens.
An unresolved install placeholder is retained rather than marked
deleted.

Reuse `POST /agent-builder/v2/projects/{id}/archive`, returning freshly
read Project state with additive `builder_runtime_cleanup_complete`.
Only confirmed runtime cleanup persists `true`; busy/failed cleanup
stays false. New projects optionally accept and expose
`client_request_id` (lowercase UUID, requires `force_new=true`) so
owned-project listing can recover a persisted creation whose response
was lost. Recovery intentionally uses client-side exact-key filtering of
the paginated existing owned-projects list (`include_archived=true`,
`limit`/`offset`); this PR does not add a server-side UUID lookup. The
Engine consumer must check its expected project count and require
explicit cleanup completion. Existing import paths remain compatible
after extracting the create-request schema to stay below the file-length
gate.

Addresses #3688 alongside Engine smoke recovery in
SerendipityOneInc/zooclaw-engine#1340. Deploy the backend contract
before requiring it in Engine smoke; no frontend changes or
existing-project migration. The cleanup retry scan does not adopt
historical cleaned rows merely because the new completion field is
absent.

## Test plan

- 315 related Builder/runtime/repository tests and Mongo query-contract
guard passed after the schema extraction; the final narrowed retry
filter then passed all 17 repository tests, including its new
historical-row guard.
- Targeted Pyright passed; full-backend Ruff check/format passed before
the mechanical schema extraction, and changed-file/pre-commit checks
passed afterward. Isolated import-linter (8 contracts), deptry, and
vulture passed.
- Local environment limitation: shared venv has broken shebangs and
lacks Pyright. Tests used isolated Python 3.13 with existing read-only
dependencies plus a temporary Sentry dependency. Standard
`verify-py`/`verify-changed` could not complete their backend
entrypoints; the three broken pre-commit entrypoints were skipped after
equivalent isolated checks passed. Shared venv untouched. CI must
validate its Python 3.12 environment and full suite.
- No staging mutation, model call, deployment, or manual data repair.
New classic single-document Mongo updates passed the static CSFLE syntax
guard, but have not been exercised through staging's encrypted client;
that remains a release validation requirement.

## Boundaries

A backend process dying before releasing a setup token, or an ambiguous
remote create with no concrete Engine IDs, remains pending rather than
falsely reporting success. This does not implement general
distributed-install recovery. The correlation key is not an idempotency
promise or a run-close tombstone; a create request not yet persisted is
not discoverable by listing. Engine recovery must bound its wait and
fail when expected projects or completion confirmation are missing.

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

```
## Summary

When a Builder Project is archived while its dedicated Engine agent is still being allocated, retain the late runtime identity and confirm cleanup only after all acquired setup operations settle. Preserve the existing expired-lease retry behavior; each setup adds a durable pending token and removes only its own token in `finally`. Archive cleanup claims and the final completion write require no pending setup tokens. An unresolved install placeholder is retained rather than marked deleted.

Reuse `POST /agent-builder/v2/projects/{id}/archive`, returning freshly read Project state with additive `builder_runtime_cleanup_complete`. Only confirmed runtime cleanup persists `true`; busy/failed cleanup stays false. New projects optionally accept and expose `client_request_id` (lowercase UUID, requires `force_new=true`) so owned-project listing can recover a persisted creation whose response was lost. Recovery intentionally uses client-side exact-key filtering of the paginated existing owned-projects list (`include_archived=true`, `limit`/`offset`); this PR does not add a server-side UUID lookup. The Engine consumer must check its expected project count and require explicit cleanup completion. Existing import paths remain compatible after extracting the create-request schema to stay below the file-length gate.

Addresses #3688 alongside Engine smoke recovery in SerendipityOneInc/zooclaw-engine#1340. Deploy the backend contract before requiring it in Engine smoke; no frontend changes or existing-project migration. The cleanup retry scan does not adopt historical cleaned rows merely because the new completion field is absent.

## Test plan

- 315 related Builder/runtime/repository tests and Mongo query-contract guard passed after the schema extraction; the final narrowed retry filter then passed all 17 repository tests, including its new historical-row guard.
- Targeted Pyright passed; full-backend Ruff check/format passed before the mechanical schema extraction, and changed-file/pre-commit checks passed afterward. Isolated import-linter (8 contracts), deptry, and vulture passed.
- Local environment limitation: shared venv has broken shebangs and lacks Pyright. Tests used isolated Python 3.13 with existing read-only dependencies plus a temporary Sentry dependency. Standard `verify-py`/`verify-changed` could not complete their backend entrypoints; the three broken pre-commit entrypoints were skipped after equivalent isolated checks passed. Shared venv untouched. CI must validate its Python 3.12 environment and full suite.
- No staging mutation, model call, deployment, or manual data repair. New classic single-document Mongo updates passed the static CSFLE syntax guard, but have not been exercised through staging's encrypted client; that remains a release validation requirement.

## Boundaries

A backend process dying before releasing a setup token, or an ambiguous remote create with no concrete Engine IDs, remains pending rather than falsely reporting success. This does not implement general distributed-install recovery. The correlation key is not an idempotency promise or a run-close tombstone; a create request not yet persisted is not discoverable by listing. Engine recovery must bound its wait and fail when expected projects or completion confirmation are missing.
```

---

## fix(models): recover retirement revisions and recognize adopted baselines (#3769)

- **SHA**: `9e4e42ce1effb185436a348c32f0562afc2073d3`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-30T12:27:22Z
- **PR**: #3769

### Commit Message

```
fix(models): recover retirement revisions and recognize adopted baselines (#3769)

## Summary
Fix model retirement preflight for adopted editing baselines and recover
a model-only Revision that was committed to Mongo but failed to activate
in Engine.

#3766 has merged (8156c3048); this PR is now rebased directly onto main
as a single commit (ac65222df).

## Root cause
Preflight compared only projection keys, although adopted Agents use the
existing baseline fingerprint contract. It also treated a migration’s
own saved-but-unapplied Revision as an unrelated draft, so generating a
fresh plan could not resume the operation.

Reuse `matches_revision` and add an explicit `resume_operation_id` to
read-only planning. For example, plan unfinished Agents with
`"resume_operation_id": "github:123456789"`, the operation prefix in the
failed run’s request artifact. Review the new digest and use normal
canary/apply. Recovery verifies the committed ChangeSet’s owner,
original operation, base, current Working Revision, active base, and
exact model-only source transformation before retrying the existing
apply path. It does not create a second product Revision or publish
unrelated drafts. Engine migration uses the new workflow operation ID.

## Test plan
- 37 focused retirement and Revision-application tests passed.
- Regression tests exercise failed activation followed by a read-only
recovery plan and successful application, baseline fingerprint matching,
unrelated edits, wrong operation/owner/base, changed replacement, and
state changes after plan review.
- `bash scripts/verify-py.sh`: Ruff, formatting, Pyright and all 8
import contracts passed.
- The changed-surface verifier passed the backend gate; inherited
frontend changes from #3766 were skipped locally because this backend
worktree has no frontend dependencies. Branch quality CI was explicitly
dispatched because stacked PRs do not automatically trigger the
main-targeted quality workflow.
- No new Mongo query forms; recovery uses existing bounded repository
reads and existing commit/apply behavior. No staging or production data
was changed.

Companion Engine fix and canonical runbook update:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1495

## CI
Branch Code Quality Check passed on `80afc10dd`
(https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/35190058005).
Automated review reported no findings. Now that it targets main,
main-targeted merge validation runs on ac65222df. Locally: 216 focused
backend tests and `verify-py` pass.
```

### PR Body

```
## Summary
Fix model retirement preflight for adopted editing baselines and recover a model-only Revision that was committed to Mongo but failed to activate in Engine.

#3766 has merged (8156c3048); this PR is now rebased directly onto main as a single commit (ac65222df).

## Root cause
Preflight compared only projection keys, although adopted Agents use the existing baseline fingerprint contract. It also treated a migration’s own saved-but-unapplied Revision as an unrelated draft, so generating a fresh plan could not resume the operation.

Reuse `matches_revision` and add an explicit `resume_operation_id` to read-only planning. For example, plan unfinished Agents with `"resume_operation_id": "github:123456789"`, the operation prefix in the failed run’s request artifact. Review the new digest and use normal canary/apply. Recovery verifies the committed ChangeSet’s owner, original operation, base, current Working Revision, active base, and exact model-only source transformation before retrying the existing apply path. It does not create a second product Revision or publish unrelated drafts. Engine migration uses the new workflow operation ID.

## Test plan
- 37 focused retirement and Revision-application tests passed.
- Regression tests exercise failed activation followed by a read-only recovery plan and successful application, baseline fingerprint matching, unrelated edits, wrong operation/owner/base, changed replacement, and state changes after plan review.
- `bash scripts/verify-py.sh`: Ruff, formatting, Pyright and all 8 import contracts passed.
- The changed-surface verifier passed the backend gate; inherited frontend changes from #3766 were skipped locally because this backend worktree has no frontend dependencies. Branch quality CI was explicitly dispatched because stacked PRs do not automatically trigger the main-targeted quality workflow.
- No new Mongo query forms; recovery uses existing bounded repository reads and existing commit/apply behavior. No staging or production data was changed.

Companion Engine fix and canonical runbook update: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1495

## CI
Branch Code Quality Check passed on `80afc10dd` (https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/35190058005). Automated review reported no findings. Now that it targets main, main-targeted merge validation runs on ac65222df. Locally: 216 focused backend tests and `verify-py` pass.
```

---

## feat(models): add retirement notices and revision-aware migration (#3766)

- **SHA**: `8156c3048083fe5bb6b321dc7f5209bb2f5e6c2b`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-30T12:19:29Z
- **PR**: #3766

### Commit Message

```
feat(models): add retirement notices and revision-aware migration (#3766)

Agents can retain models scheduled for removal in their product source,
Auto targets or inherited defaults. This connects V2 model selection to
Engine lifecycle metadata and adds explicit operator migration through
immutable product Revisions. It never changes models during a chat
request.

- Show retirement dates/replacements, disable expired choices, and
refresh V2 catalog/current-model state without changing V1 behavior or
expanding entitlement.
- Materialize expired inherited defaults for new Agents with owner
permissions, including image-generation permissions. Migration preserves
Auto and materializes affected helper defaults into a new Revision.
- Provide the in-pod operator module used by Engine’s
plan/canary/serial-batch workflow. Check owner entitlement, unapplied
drafts, plan digest, CAS, auxiliary state and the exact canary
retirement fingerprint; stop on drift. Canary artifact provenance is
enforced by the companion Engine workflow.

Companion:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1482. Deploy
Engine’s additive schema, controld and all workers first, then this PR;
enable retirement operations only after both are deployed. The canonical
runbook is in the Engine PR. No production/staging user data was
changed.

Validation: 139 targeted Python tests passed; after extracting
install-default handling, all 95 directly related tests passed again.
`verify-py.sh` (ruff, pyright, 8 import contracts), frontend
typecheck/governance/lint, model hook/presentation tests and 20
model-picker tests passed. Commit and changed-surface push hooks also
run repository checks. CI follow-up regressions also passed: 52 backend
tests and 106 frontend tests. Full remote CI remains authoritative.

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

```
Agents can retain models scheduled for removal in their product source, Auto targets or inherited defaults. This connects V2 model selection to Engine lifecycle metadata and adds explicit operator migration through immutable product Revisions. It never changes models during a chat request.

- Show retirement dates/replacements, disable expired choices, and refresh V2 catalog/current-model state without changing V1 behavior or expanding entitlement.
- Materialize expired inherited defaults for new Agents with owner permissions, including image-generation permissions. Migration preserves Auto and materializes affected helper defaults into a new Revision.
- Provide the in-pod operator module used by Engine’s plan/canary/serial-batch workflow. Check owner entitlement, unapplied drafts, plan digest, CAS, auxiliary state and the exact canary retirement fingerprint; stop on drift. Canary artifact provenance is enforced by the companion Engine workflow.

Companion: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1482. Deploy Engine’s additive schema, controld and all workers first, then this PR; enable retirement operations only after both are deployed. The canonical runbook is in the Engine PR. No production/staging user data was changed.

Validation: 139 targeted Python tests passed; after extracting install-default handling, all 95 directly related tests passed again. `verify-py.sh` (ruff, pyright, 8 import contracts), frontend typecheck/governance/lint, model hook/presentation tests and 20 model-picker tests passed. Commit and changed-surface push hooks also run repository checks. CI follow-up regressions also passed: 52 backend tests and 106 frontend tests. Full remote CI remains authoritative.
```

---

## feat(platform): connect Project Key runtime to Org billing and usage (#3954)

- **SHA**: `55e3f7572f5cb02e0fb2a2eb2bb9aa4fc3fbd564`
- **作者**: finn-srp
- **日期**: 2026-09-30T11:47:30Z
- **PR**: #3954

### Commit Message

```
feat(platform): connect Project Key runtime to Org billing and usage (#3954)

## Summary

SDK 的 `zwp_live_` Project Key 接入现有 Agent/Session API，使用 ZooWork owner
UID 认证，并将所有 Project/Key 的消费归到同一 Org business customer。

- ECAP 将公开 `pak_` ID 映射为 Engine 已支持的 32 位 ID，强制 owner、Org 和
Project，校验资源归属；Default Project 保持 `project_id=null`。
- Key 创建/rebind 加密绑定 owner JWT，复用 Work 的保存和手动 rebind 生命周期；未增加自动续期。
- Org 初始化时加密保存首次生成的 callable LiteLLM secret。Agent 读取保存的 secret，并在读取前后核对
Org payer。拒绝将 Gateway reuse 响应的管理 hash 用作 runtime
secret；初始化重试复用已保存的值，不调用个人 Billing Profile 初始化。
- secret 使用现有 `CONNECTOR_ENCRYPTION_KEY`、AES-GCM、随机 nonce 和 Org/owner
绑定的 AAD。新增私有 Org 字段及首次写入 CAS；公开 DTO 不变。加密配置在首次生成前校验。
- 保留 Key/Actor/Org attribution，按 Org/Project 隔离 idempotency scope；Org
Usage 包含 shared Sandbox 费用，不修改共享 Key 的全局 metadata。
- 修复 Usage Key 分组 ID 转换、个人 Skill null Org 可见性，并补回归测试。

仅修改 ECAP，Engine 和 Billing Gateway 沿用现有接口。前置 ECAP #3945、user-interface
#164 均已合并，base 为 main。

## Validation

- [x] 最终定向回归：**322 passed**，覆盖 Platform 服务、Agent/Skill proxy 和本地普通 Mongo
repositories。Engine/Gateway 使用 mock；普通 Mongo 与真实 CSFLE 的证据分开记录。
- [x] ruff、format、pyright 和 8 个 import contracts 通过；commit hooks 通过。Finn
author/committer 为 `finn-srp <finn@srp.one>`，GitHub 为
`finn930`。仅跳过要求登录名以 `-srp` 结尾并改写全局身份的旧 check-user hook。
- [x] 运行时源码 commit
`31edce2226a2ee5f507198ca666eb6f6d83273ce`（后续仅补验收文档）运行
`ecap-verify-py-ci`：依赖解析、静态/all CI lint、两个 jscpd 检查及 pytest
全部通过。**13,315 passed, 5 skipped, 4 warnings；coverage 89.91%**（4
workers、sysmon、89.5% threshold）。

- [x] 真实 staging CSFLE：当前运行时源码通过 **58 项检查**，涵盖 Default/named/legacy Key
rebind 与 revoke、并发 CAS、撤销优先，以及 Org secret 的 null/缺失字段、并发首次写入、防覆盖和租户绑定。3
Key + 4 Org fixture 全部删除；独立加密进程确认零残留与持久化成功审计。使用已配置的加密客户端和存储加密
key，未部署或调用计费服务。详见
[验证记录](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/platform-runtime-org-usage/docs/staging-validation/2026-09-30-platform-runtime-credentials-csfle.md)。

## Acceptance limits

真实本地 TS SDK → staging 的前一轮已通过 Key 鉴权、创建/启动 Agent、Session 和 Project
get/list 隔离。模型调用曾失败 401：ECAP 丢弃首次 secret 后误用 reuse-path hash；本次代码修复及
mock 回归不代表已完成新的真实模型调用。

前一轮 Usage 503 定位为独立的环境版本问题：当时 staging Gateway beta 尚无已合并的 Usage #76。无需新增
Gateway 代码；验收环境需要提供 #76 的接口，部署需单独授权。

用户已允许重新测试时清理对应坏 Key 数据，不做旧 Key 恢复。历史订单、充值事件、钱包和外部 ledger 保留。本次仅清理了 CSFLE
验证所创建的 7 条独立 fixture。现有应用数据、3 条历史充值订单和 11 条支付事件保留；没有部署或执行新的真实付费调用。

当前 rebind/secret CAS 的真实 CSFLE gate 已通过，staging 存储加密配置也已确认存在。后续仍需部署后的
HTTP/SDK 验收：手动凭据恢复、跨 Org/Project 隔离、实际
LLM/Sandbox/工具消费及重复事件，以及充值、消费、可用余额、Usage 和 ledger 对账。CSFLE fixture
验证不代替真实运行和计费闭环。

## Review disposition

原先的 Usage/Skill 两项代码缺陷已修复。CodeQL #665 仍为已确认并 dismiss 的公开 Key ID
归因映射误报。运行时源码 head `31edce2226` 的 GitHub 检查 18 passed、17 skipped、0
failed。

Codex/Claude 先前要求的真实 CSFLE 验证现已完成，准确源码、环境、58 项结果、清理和独立审计证据已补入仓库。后续
commit 仅更新这三份验证/规格文档，没有 Python、测试或依赖变更，因此保留已通过的全量本地结果，不重复运行同一全量检查。最新文档
head `4a58b46612` 的 Codex review 已确认原 P1 resolved，九个源码 hash 与 checkout
一致，结论 APPROVE。Claude 未提出新代码问题，但仍引用旧上下文称 CSFLE 未完成；该说法与本次 58
项真实检查、独立复核和验证记录不符，不新增代码修复或重复 staging 测试。真实部署/付费闭环仍是单独验收项。
```

### PR Body

```
## Summary

SDK 的 `zwp_live_` Project Key 接入现有 Agent/Session API，使用 ZooWork owner UID 认证，并将所有 Project/Key 的消费归到同一 Org business customer。

- ECAP 将公开 `pak_` ID 映射为 Engine 已支持的 32 位 ID，强制 owner、Org 和 Project，校验资源归属；Default Project 保持 `project_id=null`。
- Key 创建/rebind 加密绑定 owner JWT，复用 Work 的保存和手动 rebind 生命周期；未增加自动续期。
- Org 初始化时加密保存首次生成的 callable LiteLLM secret。Agent 读取保存的 secret，并在读取前后核对 Org payer。拒绝将 Gateway reuse 响应的管理 hash 用作 runtime secret；初始化重试复用已保存的值，不调用个人 Billing Profile 初始化。
- secret 使用现有 `CONNECTOR_ENCRYPTION_KEY`、AES-GCM、随机 nonce 和 Org/owner 绑定的 AAD。新增私有 Org 字段及首次写入 CAS；公开 DTO 不变。加密配置在首次生成前校验。
- 保留 Key/Actor/Org attribution，按 Org/Project 隔离 idempotency scope；Org Usage 包含 shared Sandbox 费用，不修改共享 Key 的全局 metadata。
- 修复 Usage Key 分组 ID 转换、个人 Skill null Org 可见性，并补回归测试。

仅修改 ECAP，Engine 和 Billing Gateway 沿用现有接口。前置 ECAP #3945、user-interface #164 均已合并，base 为 main。

## Validation

- [x] 最终定向回归：**322 passed**，覆盖 Platform 服务、Agent/Skill proxy 和本地普通 Mongo repositories。Engine/Gateway 使用 mock；普通 Mongo 与真实 CSFLE 的证据分开记录。
- [x] ruff、format、pyright 和 8 个 import contracts 通过；commit hooks 通过。Finn author/committer 为 `finn-srp <finn@srp.one>`，GitHub 为 `finn930`。仅跳过要求登录名以 `-srp` 结尾并改写全局身份的旧 check-user hook。
- [x] 运行时源码 commit `31edce2226a2ee5f507198ca666eb6f6d83273ce`（后续仅补验收文档）运行 `ecap-verify-py-ci`：依赖解析、静态/all CI lint、两个 jscpd 检查及 pytest 全部通过。**13,315 passed, 5 skipped, 4 warnings；coverage 89.91%**（4 workers、sysmon、89.5% threshold）。

- [x] 真实 staging CSFLE：当前运行时源码通过 **58 项检查**，涵盖 Default/named/legacy Key rebind 与 revoke、并发 CAS、撤销优先，以及 Org secret 的 null/缺失字段、并发首次写入、防覆盖和租户绑定。3 Key + 4 Org fixture 全部删除；独立加密进程确认零残留与持久化成功审计。使用已配置的加密客户端和存储加密 key，未部署或调用计费服务。详见 [验证记录](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/platform-runtime-org-usage/docs/staging-validation/2026-09-30-platform-runtime-credentials-csfle.md)。

## Acceptance limits

真实本地 TS SDK → staging 的前一轮已通过 Key 鉴权、创建/启动 Agent、Session 和 Project get/list 隔离。模型调用曾失败 401：ECAP 丢弃首次 secret 后误用 reuse-path hash；本次代码修复及 mock 回归不代表已完成新的真实模型调用。

前一轮 Usage 503 定位为独立的环境版本问题：当时 staging Gateway beta 尚无已合并的 Usage #76。无需新增 Gateway 代码；验收环境需要提供 #76 的接口，部署需单独授权。

用户已允许重新测试时清理对应坏 Key 数据，不做旧 Key 恢复。历史订单、充值事件、钱包和外部 ledger 保留。本次仅清理了 CSFLE 验证所创建的 7 条独立 fixture。现有应用数据、3 条历史充值订单和 11 条支付事件保留；没有部署或执行新的真实付费调用。

当前 rebind/secret CAS 的真实 CSFLE gate 已通过，staging 存储加密配置也已确认存在。后续仍需部署后的 HTTP/SDK 验收：手动凭据恢复、跨 Org/Project 隔离、实际 LLM/Sandbox/工具消费及重复事件，以及充值、消费、可用余额、Usage 和 ledger 对账。CSFLE fixture 验证不代替真实运行和计费闭环。

## Review disposition

原先的 Usage/Skill 两项代码缺陷已修复。CodeQL #665 仍为已确认并 dismiss 的公开 Key ID 归因映射误报。运行时源码 head `31edce2226` 的 GitHub 检查 18 passed、17 skipped、0 failed。

Codex/Claude 先前要求的真实 CSFLE 验证现已完成，准确源码、环境、58 项结果、清理和独立审计证据已补入仓库。后续 commit 仅更新这三份验证/规格文档，没有 Python、测试或依赖变更，因此保留已通过的全量本地结果，不重复运行同一全量检查。最新文档 head `4a58b46612` 的 Codex review 已确认原 P1 resolved，九个源码 hash 与 checkout 一致，结论 APPROVE。Claude 未提出新代码问题，但仍引用旧上下文称 CSFLE 未完成；该说法与本次 58 项真实检查、独立复核和验证记录不符，不新增代码修复或重复 staging 测试。真实部署/付费闭环仍是单独验收项。
```

---

## fix(auth): 优化邮箱和手机登录的原页面验证码交互 (#3953)

- **SHA**: `41477cb6356653d1f56f996dbf04f1c3744cd49e`
- **作者**: lynn Zhuang
- **日期**: 2026-09-30T11:24:05Z
- **PR**: #3953

### Commit Message

```
fix(auth): 优化邮箱和手机登录的原页面验证码交互 (#3953)

## 改动说明


邮箱和手机验证码原先会跳转到独立验证页面，打断登录卡片内的操作；较高的登录卡片还会把标题和右侧素材挤出视口。本次让验证码输入、错误提示和验证成功反馈在发起登录的原卡片内完成，并调整布局以适应卡片高度变化。

- 共用六位验证码输入：支持完整粘贴、编辑、退格、回车提交和系统验证码自动填充；返回时保留邮箱、手机号及地区。
- 点击验证后，按钮显示旋转圆环与“验证中 /
Verifying...”文案，并锁定输入及重复提交；认证状态更新时暂缓页面自动跳转，让成功反馈按原有 3 秒回调时机完整展示。
- 调整页面留白、卡片高度和右侧素材尺寸；国家选择菜单使用登录色板，完整短信授权说明在“继续”按钮上方直接展示，无需点击或展开。
- 统一中英文文案，增加紫绿渐变成功图标、进入提示的动态走光，以及更柔和的卡片阴影；减少动态效果设置下使用静态提示。
- 提供仅开发环境可用的
`/login/preview`，从登录方式选择开始测试邮箱和手机完整流程，支持直接查看验证码、验证中与成功状态；Mock 使用
`alex@example.com`、`+1 4155550100` 和验证码 `123456`，验证等待约 1.6
秒，不发送验证码或建立登录会话。`?state=verifying` 可停留检查 loading 效果，重新演示会取消待完成的 Mock 验证。

## 问题原因与兼容性

原来的验证码入口依赖 `/user/verify`
跳转；登录页左栏的独立视口高度和底部留白叠加后，较高卡片会导致页面内容向下溢出。现在由共享验证控制器切换卡片内容，登录页与本地预览共用布局。

继续使用现有邮箱 API、Firebase 手机认证、CAPTCHA、账号与会话创建流程、认证请求快照和登录后目标地址。保留邮箱首次发送的 60
秒等待、手机首次重发可用的节奏、重发后的 60 秒等待，以及原有成功回调时机。真实验证的 loading
直接跟随接口状态，不增加人为延迟。Google 登录和旧验证链接保持兼容，短信完整声明与原有七个地区选项保留。

首轮 Codex 审查指出 `current_page`
目标被兜底路径覆盖：已复现并修复。验证前显式保存“留在当前页面”语义，平台登录不再误跳到聊天页；认证完成清理上下文后，指定聊天页和订阅页仍保持原有跳转目标。

已处理
[短信说明展示位置的审查评论](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#discussion_r4143427271)：完整短信说明恢复到手机号提交按钮之前直接可见，包含短信频率、STOP/HELP、资费及条款/隐私链接；移除信息弹层与重复的授权摘要，保留原有授权文案与登录行为。

已修复 [Sam 关于当前页验证完成后持续 loading
的评论](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#discussion_r4143834835)：`current_page`
且未提供完成回调时，在原有三秒成功反馈后清理验证码和验证状态、解除 busy，并刷新当前页面。Next.js
刷新会保留客户端状态，因此显式清理避免一直显示“Continuing to
ZooWork...”；既有成功回调及指定地址跳转不变，卸载时取消完成计时器。

## 验证

- [x] 同步最新 `main` 后，TypeScript、变更文件 ESLint、格式检查与前端治理检查通过。
- [x] 登录、旧邮箱/手机验证及 CAPTCHA：4 个测试文件、109 项测试通过。
- [x] 登录弹窗和认证请求快照：3 个测试文件、46 项测试通过。
- [x] 本地 Mock 的重发节奏、错误验证码、验证中状态、成功和取消重置：1 个测试文件、4 项测试通过。
- [x] 自动跳转延后与登录页 busy 状态接线：2 个测试文件、26 项测试通过。
- [x] 最后一次 loading 调整后，相关测试筛选共 22 个测试文件、267 项测试通过，TypeScript 与 ESLint
通过（包含上述部分测试）。
- [x] 登录后目标兼容性修复：新增平台 `current_page`、指定聊天页和订阅页回归测试；登录组件共 84
项测试通过，TypeScript、ESLint 与治理检查通过。
- [x] 导入边界和依赖健康检查通过。
- [x] 本地浏览器预览邮箱、手机、验证码、验证中及成功状态；用户已确认原有视觉效果，并查看英文登录方式选择面板。新增 loading
已在英文 Mock 页面展示并截图。
- [x] 上一提交 `9069c02f9` 的 CI 构建、完整测试、类型检查、ESLint 与 CodeQL 全部通过。
- [x] 上一提交已获得 [Codex
Review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#pullrequestreview-5364553949)，首轮
P1 已修复；Claude 审查同样为 APPROVE。
- [x] 短信说明展示修复：默认登录与新版登录入口的完整说明无需交互即可看见，并位于提交按钮之前；登录组件共 86
项测试、TypeScript、ESLint、格式与治理检查通过。本地英文预览已检查并截图。
- [x] 短信说明修复提交 `4b9c81584` 的 CI 构建、完整测试、类型检查、ESLint 与 CodeQL
全部通过，未发现新增代码扫描告警；[该提交 Codex
Review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#pullrequestreview-5365025055)，Claude
同样为 APPROVE。短信说明审查评论已解决。
- [x] 当前页完成行为回归：覆盖 Platform 邮箱登录、手机号成功后 busy
释放及控件恢复、三秒完成时机和卸载取消计时器；登录组件共 88 项测试、TypeScript、ESLint、格式与治理检查通过。
- [x] 当前页完成行为修复提交 `86b3cef5d` 的 CI 构建、完整测试、类型检查、ESLint 与 CodeQL
全部通过，未发现新增代码扫描告警；[最新 Codex
Review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#pullrequestreview-5365431364)，[Claude
同样为
APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#issuecomment-5910056560)。Sam
的成功态退出审查评论已解决。

本地使用针对性测试；完整构建与完整测试套件由 CI 执行。未发送真实验证码验证外部提供方。本次仅涉及 Web
前端，无后端部署改动。截图保留在本地 `.screenshots/`，不随代码提交。



<img width="3420" height="1350" alt="20260930-175730"
src="https://github.com/user-attachments/assets/c290bb2f-4a48-414e-9842-48bf5bea84c4"
/>
```

### PR Body

```
## 改动说明

邮箱和手机验证码原先会跳转到独立验证页面，打断登录卡片内的操作；较高的登录卡片还会把标题和右侧素材挤出视口。本次让验证码输入、错误提示和验证成功反馈在发起登录的原卡片内完成，并调整布局以适应卡片高度变化。

- 共用六位验证码输入：支持完整粘贴、编辑、退格、回车提交和系统验证码自动填充；返回时保留邮箱、手机号及地区。
- 点击验证后，按钮显示旋转圆环与“验证中 / Verifying...”文案，并锁定输入及重复提交；认证状态更新时暂缓页面自动跳转，让成功反馈按原有 3 秒回调时机完整展示。
- 调整页面留白、卡片高度和右侧素材尺寸；国家选择菜单使用登录色板，完整短信授权说明在“继续”按钮上方直接展示，无需点击或展开。
- 统一中英文文案，增加紫绿渐变成功图标、进入提示的动态走光，以及更柔和的卡片阴影；减少动态效果设置下使用静态提示。
- 提供仅开发环境可用的 `/login/preview`，从登录方式选择开始测试邮箱和手机完整流程，支持直接查看验证码、验证中与成功状态；Mock 使用 `alex@example.com`、`+1 4155550100` 和验证码 `123456`，验证等待约 1.6 秒，不发送验证码或建立登录会话。`?state=verifying` 可停留检查 loading 效果，重新演示会取消待完成的 Mock 验证。

## 问题原因与兼容性

原来的验证码入口依赖 `/user/verify` 跳转；登录页左栏的独立视口高度和底部留白叠加后，较高卡片会导致页面内容向下溢出。现在由共享验证控制器切换卡片内容，登录页与本地预览共用布局。

继续使用现有邮箱 API、Firebase 手机认证、CAPTCHA、账号与会话创建流程、认证请求快照和登录后目标地址。保留邮箱首次发送的 60 秒等待、手机首次重发可用的节奏、重发后的 60 秒等待，以及原有成功回调时机。真实验证的 loading 直接跟随接口状态，不增加人为延迟。Google 登录和旧验证链接保持兼容，短信完整声明与原有七个地区选项保留。

首轮 Codex 审查指出 `current_page` 目标被兜底路径覆盖：已复现并修复。验证前显式保存“留在当前页面”语义，平台登录不再误跳到聊天页；认证完成清理上下文后，指定聊天页和订阅页仍保持原有跳转目标。

已处理 [短信说明展示位置的审查评论](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#discussion_r4143427271)：完整短信说明恢复到手机号提交按钮之前直接可见，包含短信频率、STOP/HELP、资费及条款/隐私链接；移除信息弹层与重复的授权摘要，保留原有授权文案与登录行为。

已修复 [Sam 关于当前页验证完成后持续 loading 的评论](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#discussion_r4143834835)：`current_page` 且未提供完成回调时，在原有三秒成功反馈后清理验证码和验证状态、解除 busy，并刷新当前页面。Next.js 刷新会保留客户端状态，因此显式清理避免一直显示“Continuing to ZooWork...”；既有成功回调及指定地址跳转不变，卸载时取消完成计时器。

## 验证

- [x] 同步最新 `main` 后，TypeScript、变更文件 ESLint、格式检查与前端治理检查通过。
- [x] 登录、旧邮箱/手机验证及 CAPTCHA：4 个测试文件、109 项测试通过。
- [x] 登录弹窗和认证请求快照：3 个测试文件、46 项测试通过。
- [x] 本地 Mock 的重发节奏、错误验证码、验证中状态、成功和取消重置：1 个测试文件、4 项测试通过。
- [x] 自动跳转延后与登录页 busy 状态接线：2 个测试文件、26 项测试通过。
- [x] 最后一次 loading 调整后，相关测试筛选共 22 个测试文件、267 项测试通过，TypeScript 与 ESLint 通过（包含上述部分测试）。
- [x] 登录后目标兼容性修复：新增平台 `current_page`、指定聊天页和订阅页回归测试；登录组件共 84 项测试通过，TypeScript、ESLint 与治理检查通过。
- [x] 导入边界和依赖健康检查通过。
- [x] 本地浏览器预览邮箱、手机、验证码、验证中及成功状态；用户已确认原有视觉效果，并查看英文登录方式选择面板。新增 loading 已在英文 Mock 页面展示并截图。
- [x] 上一提交 `9069c02f9` 的 CI 构建、完整测试、类型检查、ESLint 与 CodeQL 全部通过。
- [x] 上一提交已获得 [Codex Review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#pullrequestreview-5364553949)，首轮 P1 已修复；Claude 审查同样为 APPROVE。
- [x] 短信说明展示修复：默认登录与新版登录入口的完整说明无需交互即可看见，并位于提交按钮之前；登录组件共 86 项测试、TypeScript、ESLint、格式与治理检查通过。本地英文预览已检查并截图。
- [x] 短信说明修复提交 `4b9c81584` 的 CI 构建、完整测试、类型检查、ESLint 与 CodeQL 全部通过，未发现新增代码扫描告警；[该提交 Codex Review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#pullrequestreview-5365025055)，Claude 同样为 APPROVE。短信说明审查评论已解决。
- [x] 当前页完成行为回归：覆盖 Platform 邮箱登录、手机号成功后 busy 释放及控件恢复、三秒完成时机和卸载取消计时器；登录组件共 88 项测试、TypeScript、ESLint、格式与治理检查通过。
- [x] 当前页完成行为修复提交 `86b3cef5d` 的 CI 构建、完整测试、类型检查、ESLint 与 CodeQL 全部通过，未发现新增代码扫描告警；[最新 Codex Review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#pullrequestreview-5365431364)，[Claude 同样为 APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#issuecomment-5910056560)。Sam 的成功态退出审查评论已解决。

本地使用针对性测试；完整构建与完整测试套件由 CI 执行。未发送真实验证码验证外部提供方。本次仅涉及 Web 前端，无后端部署改动。截图保留在本地 `.screenshots/`，不随代码提交。



<img width="3420" height="1350" alt="20260930-175730" src="https://github.com/user-attachments/assets/c290bb2f-4a48-414e-9842-48bf5bea84c4" />
```

---

## fix(agents): 更新介绍视频并按旧项目显示 Legacy 入口 (#3949)

- **SHA**: `581cd0d2854703a9979048d5969c296ce514f15b`
- **作者**: lynn Zhuang
- **日期**: 2026-09-30T08:55:40Z
- **PR**: #3949

### Commit Message

```
fix(agents): 更新介绍视频并按旧项目显示 Legacy 入口 (#3949)

## 改动摘要

修复 Agents 空状态的视频封面，以及无旧项目用户仍能看到 Legacy 入口的问题。

- 将介绍视频更新为 YouTube `lVzTUU0cE9g`，初始显示本地封面，点击后加载嵌入播放器。
- 裁去封面左右各 1px 的边缘，消除两侧黑线，并保持播放器的 16:9 比例。
- 仅在用户拥有旧项目时显示「Legacy agent projects」入口及分隔线；未取得查询结果或首次查询失败时隐藏入口。
- 补充中英文播放按钮文案，以及视频、Legacy 查询和入口显示的前端测试。

## 问题原因

原有 MP4 未设置封面，初始帧接近空白；Legacy 入口为无条件渲染，没有判断用户是否存在旧项目。

## 改动范围

**本 PR 仅包含 `web/app` 的前端代码、静态图片和前端测试，没有修改任何后端代码、接口或后端功能。**

Legacy 判断复用已有只读接口 `GET
/agent-builder/entry/projects?limit=1&offset=0`，按用户隔离查询缓存，不影响新版 Agent
列表的加载。

## 验证

- [x] 4 个相关测试文件，共 23
项测试通过：视频点击加载、无旧项目隐藏入口、有旧项目保留入口、查询失败与登录范围，以及既有创建/导航行为。
- [x] TypeScript 类型检查、修改文件的 ESLint 和仓库治理检查通过。
- [x] 本地 mock 环境验证桌面和手机封面、无横向溢出、播放器切换时尺寸不变，以及新用户/旧项目用户的入口显示。
- [x] `git diff --check` 通过。

YouTube 在当前测试浏览器中要求登录以验证非机器人，已确认新视频嵌入地址和封面切换，**尚未确认该浏览器中的实际播放**。本 PR 不绕过
YouTube 验证。
```

### PR Body

```
## 改动摘要

修复 Agents 空状态的视频封面，以及无旧项目用户仍能看到 Legacy 入口的问题。

- 将介绍视频更新为 YouTube `lVzTUU0cE9g`，初始显示本地封面，点击后加载嵌入播放器。
- 裁去封面左右各 1px 的边缘，消除两侧黑线，并保持播放器的 16:9 比例。
- 仅在用户拥有旧项目时显示「Legacy agent projects」入口及分隔线；未取得查询结果或首次查询失败时隐藏入口。
- 补充中英文播放按钮文案，以及视频、Legacy 查询和入口显示的前端测试。

## 问题原因

原有 MP4 未设置封面，初始帧接近空白；Legacy 入口为无条件渲染，没有判断用户是否存在旧项目。

## 改动范围

**本 PR 仅包含 `web/app` 的前端代码、静态图片和前端测试，没有修改任何后端代码、接口或后端功能。**

Legacy 判断复用已有只读接口 `GET /agent-builder/entry/projects?limit=1&offset=0`，按用户隔离查询缓存，不影响新版 Agent 列表的加载。

## 验证

- [x] 4 个相关测试文件，共 23 项测试通过：视频点击加载、无旧项目隐藏入口、有旧项目保留入口、查询失败与登录范围，以及既有创建/导航行为。
- [x] TypeScript 类型检查、修改文件的 ESLint 和仓库治理检查通过。
- [x] 本地 mock 环境验证桌面和手机封面、无横向溢出、播放器切换时尺寸不变，以及新用户/旧项目用户的入口显示。
- [x] `git diff --check` 通过。

YouTube 在当前测试浏览器中要求登录以验证非机器人，已确认新视频嵌入地址和封面切换，**尚未确认该浏览器中的实际播放**。本 PR 不绕过 YouTube 验证。
```

---

## feat(platform): connect organization prepaid billing and top-ups (#3945)

- **SHA**: `8e70546a594751d0aedcf973ad804a4069250128`
- **作者**: finn-srp
- **日期**: 2026-09-30T08:53:10Z
- **PR**: #3945

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

### PR Body

```
## Summary

本 PR 接通 Platform **Org 充值、可用余额和付款记录**。付款方复用 ZooWork Work business 的 team/customer 映射，`billing_team_id == Lago customer_id`；Owner UID 用于认证和审计。Org 下所有 Project/Key 共用钱包，充值和 Usage 查询使用同一个 customer。

- 首次 Add funds 幂等初始化 Org billing，再创建 Stripe one-time Checkout。订单保存 customer/wallet 快照，沿用既有支付校验、幂等履约和恢复流程；页面 GET 只读取状态。
- 复用现有 Gateway 的 bootstrap、business team/key binding、wallet、ledger、credits/check 和 Usage API。校验 canonical Key 的 business customer/team；已有 Work Billing Profile 时拒绝改写 Key。**Gateway 和 Lago 没有代码改动。**
- Billing 页和 sidebar 展示真实余额、Add funds、付款记录和可重试错误；余额包含未结算用量。Platform Key Usage 限制为同一 Org customer 下的当前 Key，保留 Work `zct_` 路径。

## Existing plan reuse

直接复用 Work business 已使用的 `BG_PLAN_STARTER_20_MONTH`（`starter_20_month`），无需传入或新增 plan 配置变量。已只读确认 production 存在此 plan，**固定费为 0 USD**。它仅提供 Lago 内部计量周期，名字中的 20 不代表 Platform 收取 $20 月费。

Platform 只有充值后按量消费，没有商业订阅、月度赠送或免费额度。钱包永久有效，USD 1 = 200 credits；初始化前校验 plan 固定费为零且币种为 USD。

## Validation

- 本地用户完成一笔 Stripe **test mode** $5 付款后，只读核对：订单 succeeded/fulfilled，同一 Org customer/wallet 仅入账一次 1,000 credits，可用余额 $5；两个付款 webhook 没有重复入账。
- `ecap-verify-py-ci`：13,196 passed、5 skipped，coverage 89.90%；依赖解析、静态检查、全部 CI lint、两个 jscpd 均通过。Platform Node 24 lint/typecheck/test（27 passed）/build 通过。
- **P1 要求的真实 staging CSFLE 验证已完成**：team/account CAS 的 null/缺失字段、owner/status 拒绝、重复 team/customer 的实际唯一索引冲突、UID Org 共存均通过。没有 bypass 加密；测试 fixture 已删除，持久审计保留。[验证记录](docs/staging-validation/2026-09-30-platform-billing-csfle-and-clerk-cleanup.md)。
- 验证发现旧 Clerk 唯一索引会使第二个 UID Org 插入失败。用户随后明确授权清理；已备份并审计删除 staging 的 5 user、5 Org、2 关联 Project 和两个 Clerk 唯一索引，建立 UID 约束。3 个历史充值订单、7 个支付事件及外部账户/流水保留，历史履约继续使用订单快照。

## Boundaries

- #3939 已合并，base 为 main；同步使用 merge，没有 rebase/reset/force push。
- `PLATFORM_BILLING_ENABLED` 默认 false。未部署，未修改 production；CSFLE 验证覆盖 repository 操作，不等于部署后 HTTP 或消费闭环验收。
- Agent 可更新内部凭据、Engine 的 Platform 身份接入和 LLM/Sandbox/tool 事件的 Project/Key 归因仍需后续 PR。Engine runtime 继续返回 `platform.engine_access_not_ready`，申请 Key 不代表 SDK 已可运行。
- 当前代码/依赖已无 Clerk 实现，测试 fixture 已改为 UID。staging Vault 的 3 个废弃 `PLATFORM_CLERK_*` 字段已通过 CAS 删除，其余 126 个字段读回完全一致，VSO 已自动同步。没有手工 patch Secret；既有 Pod 的进程环境刷新留待授权 rollout。

## Review follow-up

- 已修复付款记录依赖余额成功的问题（`f23a51846`）：独立查询与渲染 Org 付款记录；余额失败时仍可查看支付/到账状态，Add funds 保持禁用。管理员权限和后端 Billing 开关继续生效。回归测试先在旧实现失败，再在修复后通过；Node 24 lint/typecheck/test（27 passed）/build 通过。
- 按维护者明确决定，本 PR 暂不修复 plan 列表分页问题，Gateway 不改。当前仍通过 `/lago/plans` 返回的第一页查找 `starter_20_month`；若目标 plan 不在第一页，可能误判不可用并影响初始化、余额与充值。此项保留为已知限制，未声明当前 production 已触发。
```

---

## fix(agents): preserve runtime resource class in builder environments (#3951)

- **SHA**: `1f7ad2d957c7000628bdcd606d23930434c972de`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-30T08:48:07Z
- **PR**: #3951

### Commit Message

```
fix(agents): preserve runtime resource class in builder environments (#3951)

## Summary
- Fixes #3950. Builder test and commit now prepare dependency
environments using the Agent's actual Engine runtime resource class:
Starter stays Starter, Pro uses Pro, and Ultra uses Ultra. Missing
legacy values retain the existing Starter fallback.
- Preserve readiness checks: an environment that is still building
cannot produce a candidate configuration or committed revision.

## Root cause
Both authoring entrypoints omitted `resource_class` when calling
`materialize_environment`, so it defaulted to Starter. After #3925 made
Agent creation select the account's resource class, editing a Pro Agent
could prepare a Starter variant and then fail Engine's actual-runtime
validation with `409 environment_not_ready` (`environment pro variant is
not ready`), surfaced as `agent.runtime_error`.

Use the already-loaded Agent detail, matching the existing update path,
rather than recomputing the current account plan. No Engine validation,
billing, model selection, data migration, or frontend change is needed.

## Scope
The fix covers newly materialized environments. Reusing an unchanged
environment after a runtime class/plan change is an independent
pre-existing path tracked in #3952; this PR does not rebuild or replace
retained/imported environment pins.

## Test plan
- [x] Regression demonstrated before fix: 8 Pro/Ultra cases failed while
8 Starter/legacy cases passed.
- [x] 75 targeted authoring/environment tests passed, including 16 new
cases across both entrypoints, all supported classes plus legacy
fallback, and ready/building states. Tests exercise real environment
materialization and assert Engine build/read parameters and the
no-commit readiness gate.
- [x] Backend static checks (ruff, format, pyright, import-linter).
- [x] CI backend full tests, lint/typecheck, and CodeQL passed for
`805b3be55`; no open code-scanning alerts on the PR merge ref.
- [x] CI aggregate summary passed; all reported checks settled without
failures.

Backend-only deployment. The fix has not been deployed or retested
against live staging; no production/staging data was modified by this
PR.
```

### PR Body

```
## Summary
- Fixes #3950. Builder test and commit now prepare dependency environments using the Agent's actual Engine runtime resource class: Starter stays Starter, Pro uses Pro, and Ultra uses Ultra. Missing legacy values retain the existing Starter fallback.
- Preserve readiness checks: an environment that is still building cannot produce a candidate configuration or committed revision.

## Root cause
Both authoring entrypoints omitted `resource_class` when calling `materialize_environment`, so it defaulted to Starter. After #3925 made Agent creation select the account's resource class, editing a Pro Agent could prepare a Starter variant and then fail Engine's actual-runtime validation with `409 environment_not_ready` (`environment pro variant is not ready`), surfaced as `agent.runtime_error`.

Use the already-loaded Agent detail, matching the existing update path, rather than recomputing the current account plan. No Engine validation, billing, model selection, data migration, or frontend change is needed.

## Scope
The fix covers newly materialized environments. Reusing an unchanged environment after a runtime class/plan change is an independent pre-existing path tracked in #3952; this PR does not rebuild or replace retained/imported environment pins.

## Test plan
- [x] Regression demonstrated before fix: 8 Pro/Ultra cases failed while 8 Starter/legacy cases passed.
- [x] 75 targeted authoring/environment tests passed, including 16 new cases across both entrypoints, all supported classes plus legacy fallback, and ready/building states. Tests exercise real environment materialization and assert Engine build/read parameters and the no-commit readiness gate.
- [x] Backend static checks (ruff, format, pyright, import-linter).
- [x] CI backend full tests, lint/typecheck, and CodeQL passed for `805b3be55`; no open code-scanning alerts on the PR merge ref.
- [x] CI aggregate summary passed; all reported checks settled without failures.

Backend-only deployment. The fix has not been deployed or retested against live staging; no production/staging data was modified by this PR.
```

---

## fix(agents): apply personal Codex rules on every model surface (#3946)

- **SHA**: `799281b3d9712a87c5a9bf241cbe9a9e1a9689a3`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-30T07:38:55Z
- **PR**: #3946

### Commit Message

```
fix(agents): apply personal Codex rules on every model surface (#3946)

## Summary

#3930 fixed personal Codex selection in the Edit Agent composer. This PR
applies the same rules to every other surface that shows or changes an
Agent model. Spec:
`docs/superpowers/specs/2026-09-30-codex-model-surfaces.md`.

**Backend (claw-interface)**
- **Pack updates keep personal models.** `model_primary_for_update` no
longer treats a current `openai-codex/` model as withdrawn. Owner
updates and the publisher fan-out (`pack_skill_edits` →
`pack_skill_agent_update_service`) no longer replace it with the Pack
default, which used to make Engine drop the binding.
- **Leaving a subscription restores the Revision default.** On a bound
self-evolving Agent, a platform `PUT /agents/{id}/model` must match the
working Revision's `model_primary`. Any other model returns 409
`agent_revision.settings_required`, which directs the user to change the
default in Edit Agent. If the Revision cannot be read, the exit stays
open. The response now reports `model_managed` the same way the next
read does.
- **Binding a Codex model needs preview admission.** `PUT
/agents/{id}/model` with an `openai-codex/` model now requires the
verified-email admission, not only the master switch. Leaving a
subscription stays ungated.

**Web**
- **One shared flow.** `useAgentModelFlow` (moved from #3930's
`useWorkspaceModelFlow`) now drives the Agent workspace (Edit Agent and
task view) and the New Chat launcher:
  - editable Revisions keep the #3930 behaviour;
- task view and shared copies can only restore the Revision default
while bound;
- ordinary Engine Agents list, bind and label personal models in the
launcher.
- **Agent Settings.** The Default model section shows the active
personal model. Saving a different default clears the binding after the
commit. Saving an unchanged default keeps it. A failed clear stays
visible and can be retried.
- **Broken bindings.** A binding whose connection is missing or not
connected is labelled in the composer. The Codex dialog shows it with
its status, Reconnect (the user then picks the model again from the new
connection) and Disconnect. Disconnect and model refresh also reread the
Agent models.
- **Bound but no longer admitted.** A binding that outlived preview
admission gets a restricted dialog with Disconnect and the exit hint.
While discovery is loading or has failed, the state is treated as
unknown, not as restricted.

**iOS** is a separate PR, #3947. This branch briefly contained those
commits; the last commit reverts them, so this PR's diff has no iOS
changes.

## Root cause

Personal subscriptions are runtime bindings layered on the Agent's
platform model (#3923). Only the workspace hook added in #3930 handled
that; every other writer still assumed platform models only:

- Pack in-place update keeps the owner's model only if the platform
catalog still offers it (#3851). A Codex model is never in that catalog,
so it looked withdrawn and was replaced.
- The runtime PUT accepted any platform model when leaving a
subscription. Revision-managed Agents therefore diverged from their
Revision, and the next Revision render silently reset them.
- New Chat, Agent Settings and iOS had no subscription awareness. They
showed a stale model, could not bind, or cleared the binding without
telling the user.
- The Codex dialog hid bindings that were not connected or no longer
admitted, so there was no way to repair or leave them.

## Test plan

- [x] Backend, `bash scripts/verify-py.sh` (ruff, format, pyright,
import-linter): passed.
- [x] Backend, targeted pytest over 12 files: 278 passed. Each new test
fails against the unfixed code:
  - Pack update fix: 3 fail;
  - Revision-default exit: 6 fail;
  - admission gate: 3 fail;
  - response `model_managed`: 1 fails.
- [x] Web, `bash scripts/verify-web.sh <changed tests>`: 213 passed.
- [x] Web, wider vitest over every spec that imports a changed module
plus `tests/unit/app/agents`: 89 files, 1249 tests passed.
- [x] Web, `tsc --noEmit --incremental false` and `eslint --no-cache` on
the changed files: passed.
- [x] Combined branch, `bash scripts/verify-changed.sh` (web guards,
tsc, eslint; ruff, format, pyright, import-linter): all changed surfaces
passed.
- [ ] Staging check with an admitted account:
  - bind and leave in task view, Edit Agent, Settings and New Chat;
  - Pack update of a bound Agent;
  - disconnect and reconnect.

## Deployment

- Deploy claw-interface and web together. Web restricts task-view exits
to the Revision default and rereads the model after a clear, so it also
behaves correctly against the current backend.
- No Engine change and no data migration.

## Related

- iOS Agent Settings: #3947 (independent of this PR; it also works
against the current backend)
- Agent Builder's own model contract: #3941
- Unified model selector for every surface: #3942

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

```
## Summary

#3930 fixed personal Codex selection in the Edit Agent composer. This PR applies the same rules to every other surface that shows or changes an Agent model. Spec: `docs/superpowers/specs/2026-09-30-codex-model-surfaces.md`.

**Backend (claw-interface)**
- **Pack updates keep personal models.** `model_primary_for_update` no longer treats a current `openai-codex/` model as withdrawn. Owner updates and the publisher fan-out (`pack_skill_edits` → `pack_skill_agent_update_service`) no longer replace it with the Pack default, which used to make Engine drop the binding.
- **Leaving a subscription restores the Revision default.** On a bound self-evolving Agent, a platform `PUT /agents/{id}/model` must match the working Revision's `model_primary`. Any other model returns 409 `agent_revision.settings_required`, which directs the user to change the default in Edit Agent. If the Revision cannot be read, the exit stays open. The response now reports `model_managed` the same way the next read does.
- **Binding a Codex model needs preview admission.** `PUT /agents/{id}/model` with an `openai-codex/` model now requires the verified-email admission, not only the master switch. Leaving a subscription stays ungated.

**Web**
- **One shared flow.** `useAgentModelFlow` (moved from #3930's `useWorkspaceModelFlow`) now drives the Agent workspace (Edit Agent and task view) and the New Chat launcher:
  - editable Revisions keep the #3930 behaviour;
  - task view and shared copies can only restore the Revision default while bound;
  - ordinary Engine Agents list, bind and label personal models in the launcher.
- **Agent Settings.** The Default model section shows the active personal model. Saving a different default clears the binding after the commit. Saving an unchanged default keeps it. A failed clear stays visible and can be retried.
- **Broken bindings.** A binding whose connection is missing or not connected is labelled in the composer. The Codex dialog shows it with its status, Reconnect (the user then picks the model again from the new connection) and Disconnect. Disconnect and model refresh also reread the Agent models.
- **Bound but no longer admitted.** A binding that outlived preview admission gets a restricted dialog with Disconnect and the exit hint. While discovery is loading or has failed, the state is treated as unknown, not as restricted.

**iOS** is a separate PR, #3947. This branch briefly contained those commits; the last commit reverts them, so this PR's diff has no iOS changes.

## Root cause

Personal subscriptions are runtime bindings layered on the Agent's platform model (#3923). Only the workspace hook added in #3930 handled that; every other writer still assumed platform models only:

- Pack in-place update keeps the owner's model only if the platform catalog still offers it (#3851). A Codex model is never in that catalog, so it looked withdrawn and was replaced.
- The runtime PUT accepted any platform model when leaving a subscription. Revision-managed Agents therefore diverged from their Revision, and the next Revision render silently reset them.
- New Chat, Agent Settings and iOS had no subscription awareness. They showed a stale model, could not bind, or cleared the binding without telling the user.
- The Codex dialog hid bindings that were not connected or no longer admitted, so there was no way to repair or leave them.

## Test plan

- [x] Backend, `bash scripts/verify-py.sh` (ruff, format, pyright, import-linter): passed.
- [x] Backend, targeted pytest over 12 files: 278 passed. Each new test fails against the unfixed code:
  - Pack update fix: 3 fail;
  - Revision-default exit: 6 fail;
  - admission gate: 3 fail;
  - response `model_managed`: 1 fails.
- [x] Web, `bash scripts/verify-web.sh <changed tests>`: 213 passed.
- [x] Web, wider vitest over every spec that imports a changed module plus `tests/unit/app/agents`: 89 files, 1249 tests passed.
- [x] Web, `tsc --noEmit --incremental false` and `eslint --no-cache` on the changed files: passed.
- [x] Combined branch, `bash scripts/verify-changed.sh` (web guards, tsc, eslint; ruff, format, pyright, import-linter): all changed surfaces passed.
- [ ] Staging check with an admitted account:
  - bind and leave in task view, Edit Agent, Settings and New Chat;
  - Pack update of a bound Agent;
  - disconnect and reconnect.

## Deployment

- Deploy claw-interface and web together. Web restricts task-view exits to the Revision default and rereads the model after a clear, so it also behaves correctly against the current backend.
- No Engine change and no data migration.

## Related

- iOS Agent Settings: #3947 (independent of this PR; it also works against the current backend)
- Agent Builder's own model contract: #3941
- Unified model selector for every surface: #3942

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## fix(chat): 以整轮结束事件为准保留 Thinking 和运行状态 (#3948)

- **SHA**: `e09e62829c1e77382ea276000ca5d1f6f48d06ab`
- **作者**: lynn Zhuang
- **日期**: 2026-09-30T07:29:34Z
- **PR**: #3948

### Commit Message

```
fix(chat): 以整轮结束事件为准保留 Thinking 和运行状态 (#3948)

## 改动说明
修复 Agent Build / Chat 在中途收到图片或普通消息后，Thinking
与运行状态提前消失的问题。当前轮次出现运行协议事件后，以明确的整轮结束事件作为完成依据；图片、进度文本和单个工具结果不会结束整轮等待。无运行协议的普通回复和命令确认保留原有兼容行为。

## 问题原因

原逻辑把未携带运行状态标记的机器人附件消息视为完整回复，WebSocket、历史消息补载及状态标签三条路径会提前结束等待。本次统一这三条路径的判断，并按当前用户轮次和线程隔离，避免影响其他会话。

## 审查修正
接受 Codex 对可选 `run_id` 的反馈：工具状态即使不带运行
ID，也按运行协议事件处理。新增/加强三个路径的回归用例，确认附件不会提前结束等待。

## 修改范围
- 仅修改前端状态判断与回归测试。
- 增加本地 mock 附件预览 fixture，方便复现和检查。
- 没有修改 services/、生产后端、数据库、接口或部署配置；仅需前端发布。

## 验证
- [x] TypeScript、ESLint、仓库前端治理检查通过。
- [x] 9 个相关测试文件、254 项测试通过，覆盖中途附件、明确结束事件、普通回复和线程隔离。
- [x] 本地 mock 页面确认工具完成后仍显示 Thinking 和停止按钮，预览已确认。
- [x] mock 脚本语法和 ESLint 检查通过。
- [ ] GitHub CI（创建 PR 后自动运行）。
```

### PR Body

```
## 改动说明
修复 Agent Build / Chat 在中途收到图片或普通消息后，Thinking 与运行状态提前消失的问题。当前轮次出现运行协议事件后，以明确的整轮结束事件作为完成依据；图片、进度文本和单个工具结果不会结束整轮等待。无运行协议的普通回复和命令确认保留原有兼容行为。

## 问题原因
原逻辑把未携带运行状态标记的机器人附件消息视为完整回复，WebSocket、历史消息补载及状态标签三条路径会提前结束等待。本次统一这三条路径的判断，并按当前用户轮次和线程隔离，避免影响其他会话。

## 审查修正
接受 Codex 对可选 `run_id` 的反馈：工具状态即使不带运行 ID，也按运行协议事件处理。新增/加强三个路径的回归用例，确认附件不会提前结束等待。

## 修改范围
- 仅修改前端状态判断与回归测试。
- 增加本地 mock 附件预览 fixture，方便复现和检查。
- 没有修改 services/、生产后端、数据库、接口或部署配置；仅需前端发布。

## 验证
- [x] TypeScript、ESLint、仓库前端治理检查通过。
- [x] 9 个相关测试文件、254 项测试通过，覆盖中途附件、明确结束事件、普通回复和线程隔离。
- [x] 本地 mock 页面确认工具完成后仍显示 Thinking 和停止按钮，预览已确认。
- [x] mock 脚本语法和 ESLint 检查通过。
- [ ] GitHub CI（创建 PR 后自动运行）。
```

---

## fix(billing): reuse Stripe customers across checkout purchases (#3940)

- **SHA**: `c6cb0bec51108a936e856196146a11de888f5117`
- **作者**: sam-srp
- **日期**: 2026-09-30T05:46:12Z
- **PR**: #3940

### Commit Message

```
fix(billing): reuse Stripe customers across checkout purchases (#3940)

## Summary
Subscription and top-up Checkout previously supplied only
`customer_email`, allowing repeat purchases by one ZooWork user to
create separate Stripe Customers and be treated as first-time purchases
again. New Checkout requests now share a durable Customer binding scoped
to UID and Stripe account. Staging and production already use separate
databases; no test/live binding field or API-key-prefix parsing is
added.

## Root cause and fix
- Recover an existing Customer from UID-owned successful payment history
(including zero-dollar/refunded orders), agreements or legacy records;
never associate accounts by email alone.
- Reserve one binding atomically and create with a stable Stripe
idempotency key. Freeze creation parameters for retries, persist the
selected Customer on the payment order, and fail closed on unresolved
creation beyond the safe retry window or invalid canonical identity.
- Both subscription and top-up Checkout pass `customer`. API-key
rotation within a Stripe account preserves the binding. Coupon/product
settings and environment variables are unchanged.

## Test plan
- [x] Billing-policy and Stripe unit suite: 644 passed, 5 skipped; CSFLE
query guard passed; all 18 new customer/repository tests passed.
- [x] Full `scripts/verify-py.sh`: Ruff, format, Pyright, import
contracts; commit hooks also passed.
- [x] New read operations exercised through staging's actual encrypted
Mongo client (`encryption_enabled=True`).
- [ ] Staging encrypted write/CAS exercise with an isolated fixture and
Stripe sandbox end-to-end redemption validation before release.

## Rollout boundaries
Existing Checkout URLs and pre-deployment uncertain requests retain
their original parameters for payment/idempotency safety; already issued
URLs are not retroactively expired and can remain usable until normal
expiry. Existing Stripe Customers/balances/subscriptions are not merged
or modified. This PR has not been deployed and does not change
production data.
```

### PR Body

```
## Summary
Subscription and top-up Checkout previously supplied only `customer_email`, allowing repeat purchases by one ZooWork user to create separate Stripe Customers and be treated as first-time purchases again. New Checkout requests now share a durable Customer binding scoped to UID and Stripe account. Staging and production already use separate databases; no test/live binding field or API-key-prefix parsing is added.

## Root cause and fix
- Recover an existing Customer from UID-owned successful payment history (including zero-dollar/refunded orders), agreements or legacy records; never associate accounts by email alone.
- Reserve one binding atomically and create with a stable Stripe idempotency key. Freeze creation parameters for retries, persist the selected Customer on the payment order, and fail closed on unresolved creation beyond the safe retry window or invalid canonical identity.
- Both subscription and top-up Checkout pass `customer`. API-key rotation within a Stripe account preserves the binding. Coupon/product settings and environment variables are unchanged.

## Test plan
- [x] Billing-policy and Stripe unit suite: 644 passed, 5 skipped; CSFLE query guard passed; all 18 new customer/repository tests passed.
- [x] Full `scripts/verify-py.sh`: Ruff, format, Pyright, import contracts; commit hooks also passed.
- [x] New read operations exercised through staging's actual encrypted Mongo client (`encryption_enabled=True`).
- [ ] Staging encrypted write/CAS exercise with an isolated fixture and Stripe sandbox end-to-end redemption validation before release.

## Rollout boundaries
Existing Checkout URLs and pre-deployment uncertain requests retain their original parameters for payment/idempotency safety; already issued URLs are not retroactively expired and can remain usable until normal expiry. Existing Stripe Customers/balances/subscriptions are not merged or modified. This PR has not been deployed and does not change production data.
```

---

## docs(agents): give each worktree its own backend venv (#3944)

- **SHA**: `82a7e29a08daebc77ec51bbf397c7674a5d1473b`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-30T05:04:24Z
- **PR**: #3944

### Commit Message

```
docs(agents): give each worktree its own backend venv (#3944)

## Summary
`AGENTS.md` (Worktrees section) told agents that when pre-push
`verify-py` can't find `.venv` in a new worktree, they should symlink
`services/claw-interface/.venv` to the main checkout's. This replaces
that with creating a per-worktree venv:

```bash
cd services/claw-interface && uv venv --python 3.12 .venv && uv pip install -r requirements.txt -r requirements-dev.txt
```

## Why
With the symlink, every worktree installs its own branch's requirements
into the same env, so whichever install ran last wins. Seen on one dev
machine where five worktrees shared the main checkout's venv:

- An older branch's `uv pip install` downgraded `openai` 3.13.0 → 3.3.1
under every other worktree.
- After the shared venv was rebuilt, the last branch installed had no
`sentry-sdk`, so `verify-py` (pyright missing imports) and pytest
collection failed on branches that need it.

A worktree with its own venv passed `verify-py` and all 574 builder unit
tests.

The `--python 3.12` flag matches the release image (`python:3.12.3`) and
CI. #3943 adds a `.python-version` so uv picks 3.12 by default; the
explicit flag works either way.

## Test plan
- Docs-only change (one line in `AGENTS.md`; `CLAUDE.md` is a symlink to
it).
- Nothing else in the repo recommends or creates the symlink (`git grep`
over AGENTS/README/docs/scripts).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

```
## Summary
`AGENTS.md` (Worktrees section) told agents that when pre-push `verify-py` can't find `.venv` in a new worktree, they should symlink `services/claw-interface/.venv` to the main checkout's. This replaces that with creating a per-worktree venv:

```bash
cd services/claw-interface && uv venv --python 3.12 .venv && uv pip install -r requirements.txt -r requirements-dev.txt
```

## Why
With the symlink, every worktree installs its own branch's requirements into the same env, so whichever install ran last wins. Seen on one dev machine where five worktrees shared the main checkout's venv:

- An older branch's `uv pip install` downgraded `openai` 3.13.0 → 3.3.1 under every other worktree.
- After the shared venv was rebuilt, the last branch installed had no `sentry-sdk`, so `verify-py` (pyright missing imports) and pytest collection failed on branches that need it.

A worktree with its own venv passed `verify-py` and all 574 builder unit tests.

The `--python 3.12` flag matches the release image (`python:3.12.3`) and CI. #3943 adds a `.python-version` so uv picks 3.12 by default; the explicit flag works either way.

## Test plan
- Docs-only change (one line in `AGENTS.md`; `CLAUDE.md` is a symlink to it).
- Nothing else in the repo recommends or creates the symlink (`git grep` over AGENTS/README/docs/scripts).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## chore(claw-interface): pin local Python to 3.12 (#3943)

- **SHA**: `dda5153f792f126e824f6e74d504c5e2579da3c9`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-30T05:04:07Z
- **PR**: #3943

### Commit Message

```
chore(claw-interface): pin local Python to 3.12 (#3943)

## Summary
Add `services/claw-interface/.python-version` (`3.12`) so `uv venv` /
`uv pip` pick the same interpreter as the release image and CI without
needing `--python` every time.

- Release image: `services/claw-interface/Dockerfile` is `FROM
python:3.12.3` (unchanged since the monorepo conversion; also what
`service-v0.18.22-release` built).
- CI: `code-quality.yml` passes `python_version: '3.12'` to the shared
Python quality workflow.
- README and `.devcontainer/postCreateCommand.sh` already say `uv venv
--python 3.12`; this makes the default match when someone forgets the
flag.

## Why
Without a pin, `uv venv` takes the first `python` on PATH. On a dev
machine where that is a 3.13 conda install, the venv ends up with
packages under `lib/python3.13` while `pyproject.toml` pins pyright to
`.venv` with `pythonVersion = "3.12"`. `bash scripts/verify-py.sh` then
reports ~2000 missing-import errors that CI never sees. After rebuilding
the venv on 3.12, the same tree reports 0 pyright errors.

## Test plan
- `uv python find` in `services/claw-interface/`:
`/home/.../miniconda3/bin/python3` before, `/usr/bin/python3.12` after;
sibling directories are unaffected.
- No runtime or CI change: the Dockerfile and CI set their interpreter
explicitly and don't read `.python-version`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

```
## Summary
Add `services/claw-interface/.python-version` (`3.12`) so `uv venv` / `uv pip` pick the same interpreter as the release image and CI without needing `--python` every time.

- Release image: `services/claw-interface/Dockerfile` is `FROM python:3.12.3` (unchanged since the monorepo conversion; also what `service-v0.18.22-release` built).
- CI: `code-quality.yml` passes `python_version: '3.12'` to the shared Python quality workflow.
- README and `.devcontainer/postCreateCommand.sh` already say `uv venv --python 3.12`; this makes the default match when someone forgets the flag.

## Why
Without a pin, `uv venv` takes the first `python` on PATH. On a dev machine where that is a 3.13 conda install, the venv ends up with packages under `lib/python3.13` while `pyproject.toml` pins pyright to `.venv` with `pythonVersion = "3.12"`. `bash scripts/verify-py.sh` then reports ~2000 missing-import errors that CI never sees. After rebuilding the venv on 3.12, the same tree reports 0 pyright errors.

## Test plan
- `uv python find` in `services/claw-interface/`: `/home/.../miniconda3/bin/python3` before, `/usr/bin/python3.12` after; sibling directories are unaffected.
- No runtime or CI change: the Dockerfile and CI set their interpreter explicitly and don't read `.python-version`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## fix(claw): isolate model changes and agent lifecycle from compute upgrades (#3928)

- **SHA**: `543ad5c901e927353a3889d3b91f4bcbe00be9f4`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-30T04:26:53Z
- **PR**: #3928

### Commit Message

```
fix(claw): isolate model changes and agent lifecycle from compute upgrades (#3928)

## Problem and behavior

Saving an API model after disconnecting a personal subscription also
tried to change the Agent's Sandbox class. A missing target-class
Environment variant could reject the entire model save with
`environment_not_ready`.

Model saves, start/prepare, existing default-Agent reads/retries,
Service API config writes, and Pack content/environment updates now
preserve compute. API model selection clears the subscription binding.
Agent creation still selects its initial class from trusted server
entitlements; actual runtime/Environment validation remains in place.

V1-migrated Agents retain their existing compute configuration. Both
migrated main and secondary workspaces are excluded from
entitlement-change synchronization and the hourly class-reconciliation
cron using the canonical `is_migrated_v1` identity. Skipped rows do not
block pagination or count as failures; cron `processed_count` continues
to count scanned rows. This policy covers upgrades and downgrades.
Native Agents in the same account still synchronize normally.

Native reconciliation reads the current class and skips matching values.
Older Engines that omit the projection retain the existing PUT fallback;
differing classes are updated normally and target-Environment failures
remain visible. No automatic Environment build or retry is added.

Service API Agents intentionally have no ECAP workspace row. Entitlement
synchronization now also pages Engine's tenant-scoped Agent inventory;
the hourly sweep independently enumerates active memberships using an
indexed `(uid, org_id)` cursor, so owners with no workspace and Agents
whose creation token was revoked are covered. The additional pass
excludes any Computer represented by a workspace record, including
retired or migrated siblings, preserving the existing lifecycle policy.
It validates inventory ownership and pagination, isolates individual
Agent failures, and shares the cron's batch budget. No synthetic
workspaces or foreground class updates are introduced.

The resource-class cron now has a separate 100-request Engine inventory
budget, charging empty, workspace-only, and failed pages before I/O. A
durable singleton checkpoint carries both the workspace and membership
cursors, current Engine page, and unfinished page IDs across
invocations. A 900-second atomic lease covers both phases; a shorter
600-second timeout bounds a live run, overlapping triggers skip work,
and owner/expiry checks fence stale checkpoint writers. Positive Agent
budgets also resume from their saved position. Each bounded inventory
slice yields back to workspace repair on the next invocation, retaining
independent inventory progress. A full sweep can span multiple hourly
invocations; foreground entitlement hooks still provide the fast path.

## Scope and compatibility

SerendipityOneInc/zooclaw-engine#1772's shared-Computer atomic upgrade
proposal is withdrawn. This PR does not require it or impose a new hard
deployment prerequisite on SerendipityOneInc/zooclaw-engine#1771. The
earlier automatic-build proposal SerendipityOneInc/zooclaw-engine#1767
remains withdrawn.

This change does not repair historical Computer/config drift or mutate
deployed data. Migrated Agents may retain a lower or higher class than
their current plan intentionally. It does not pin existing Sandbox
instances forever or introduce an upgrade-on-recreation mechanism.
Native synchronization remains best effort plus the hourly cron and
requires a ready target Environment; native downgrades may therefore
retain higher resources until synchronization succeeds.

Product ops owns Environment builds/retries. Issue #3933 retains
health/impact visibility, with intentional migrated-class retention
distinguished from actual runtime failures.

## Validation

- Latest bounded-scan fix: 62 targeted tests passed, covering
empty/workspace-only/failed inventory budgets, default-unlimited Agent
budgets, tail and large-owner page continuation, mid-page Agent limits,
failure isolation, native-workspace continuation, overlapping runs,
timeout checkpoints, expired-lease recovery, stale-owner fencing,
repository atomic-operation contracts, existing cron routes and CSFLE
syntax guards.
- `scripts/verify-changed.sh` passed: Ruff, formatting, Pyright, and all
8 import contracts.
- Final CI on `1464cc836`: **13,098 passed, 5 skipped**, coverage
**89.86%**. All quality, CodeQL and auto-review gates passed:
https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/36663154292.
Latest Codex and Claude reviews approve with no blocking findings.
- Prior review findings fixed: Service API inventory coverage and
membership cursor/index. Re-enabled native main Agents continue to use
the accepted background-convergence policy. The new scan-cost finding is
addressed by independent request/time budgets, durable continuation and
a singleton lease.
- No merge, deployment, or live user-data mutation. The new
`ecap-engine-class-scan` singleton uses Mongo's built-in unique `_id`;
atomic updates are classic single-collection operations, without
aggregation or pipeline updates. Live encrypted-client validation of
claim/checkpoint/release remains required before release; unit mocks and
syntax guards do not prove CSFLE compatibility.
```

### PR Body

```
## Problem and behavior

Saving an API model after disconnecting a personal subscription also tried to change the Agent's Sandbox class. A missing target-class Environment variant could reject the entire model save with `environment_not_ready`.

Model saves, start/prepare, existing default-Agent reads/retries, Service API config writes, and Pack content/environment updates now preserve compute. API model selection clears the subscription binding. Agent creation still selects its initial class from trusted server entitlements; actual runtime/Environment validation remains in place.

V1-migrated Agents retain their existing compute configuration. Both migrated main and secondary workspaces are excluded from entitlement-change synchronization and the hourly class-reconciliation cron using the canonical `is_migrated_v1` identity. Skipped rows do not block pagination or count as failures; cron `processed_count` continues to count scanned rows. This policy covers upgrades and downgrades. Native Agents in the same account still synchronize normally.

Native reconciliation reads the current class and skips matching values. Older Engines that omit the projection retain the existing PUT fallback; differing classes are updated normally and target-Environment failures remain visible. No automatic Environment build or retry is added.

Service API Agents intentionally have no ECAP workspace row. Entitlement synchronization now also pages Engine's tenant-scoped Agent inventory; the hourly sweep independently enumerates active memberships using an indexed `(uid, org_id)` cursor, so owners with no workspace and Agents whose creation token was revoked are covered. The additional pass excludes any Computer represented by a workspace record, including retired or migrated siblings, preserving the existing lifecycle policy. It validates inventory ownership and pagination, isolates individual Agent failures, and shares the cron's batch budget. No synthetic workspaces or foreground class updates are introduced.

The resource-class cron now has a separate 100-request Engine inventory budget, charging empty, workspace-only, and failed pages before I/O. A durable singleton checkpoint carries both the workspace and membership cursors, current Engine page, and unfinished page IDs across invocations. A 900-second atomic lease covers both phases; a shorter 600-second timeout bounds a live run, overlapping triggers skip work, and owner/expiry checks fence stale checkpoint writers. Positive Agent budgets also resume from their saved position. Each bounded inventory slice yields back to workspace repair on the next invocation, retaining independent inventory progress. A full sweep can span multiple hourly invocations; foreground entitlement hooks still provide the fast path.

## Scope and compatibility

SerendipityOneInc/zooclaw-engine#1772's shared-Computer atomic upgrade proposal is withdrawn. This PR does not require it or impose a new hard deployment prerequisite on SerendipityOneInc/zooclaw-engine#1771. The earlier automatic-build proposal SerendipityOneInc/zooclaw-engine#1767 remains withdrawn.

This change does not repair historical Computer/config drift or mutate deployed data. Migrated Agents may retain a lower or higher class than their current plan intentionally. It does not pin existing Sandbox instances forever or introduce an upgrade-on-recreation mechanism. Native synchronization remains best effort plus the hourly cron and requires a ready target Environment; native downgrades may therefore retain higher resources until synchronization succeeds.

Product ops owns Environment builds/retries. Issue #3933 retains health/impact visibility, with intentional migrated-class retention distinguished from actual runtime failures.

## Validation

- Latest bounded-scan fix: 62 targeted tests passed, covering empty/workspace-only/failed inventory budgets, default-unlimited Agent budgets, tail and large-owner page continuation, mid-page Agent limits, failure isolation, native-workspace continuation, overlapping runs, timeout checkpoints, expired-lease recovery, stale-owner fencing, repository atomic-operation contracts, existing cron routes and CSFLE syntax guards.
- `scripts/verify-changed.sh` passed: Ruff, formatting, Pyright, and all 8 import contracts.
- Final CI on `1464cc836`: **13,098 passed, 5 skipped**, coverage **89.86%**. All quality, CodeQL and auto-review gates passed: https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/36663154292. Latest Codex and Claude reviews approve with no blocking findings.
- Prior review findings fixed: Service API inventory coverage and membership cursor/index. Re-enabled native main Agents continue to use the accepted background-convergence policy. The new scan-cost finding is addressed by independent request/time budgets, durable continuation and a singleton lease.
- No merge, deployment, or live user-data mutation. The new `ecap-engine-class-scan` singleton uses Mongo's built-in unique `_id`; atomic updates are classic single-collection operations, without aggregation or pipeline updates. Live encrypted-client validation of claim/checkpoint/release remains required before release; unit mocks and syntax guards do not prove CSFLE compatibility.
```

---

## fix(agents): allow personal Codex selection while editing (#3930)

- **SHA**: `afd87ea99b6e8ca4f044ab2bd47be17725b0842b`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-30T03:21:39Z
- **PR**: #3930

### Commit Message

```
fix(agents): allow personal Codex selection while editing (#3930)

## Summary

Edit Agent now offers the same admitted Personal Codex models as New
Task. The picker displays an active personal runtime model, while
ordinary API model edits continue to save through the Revision flow.

## Root cause

The workspace passed subscription choices only in use mode, and the
shared composer additionally suppressed them whenever a Revision model
controller was present. The backend runtime grants in #3927 and
zooclaw-engine#1761 were already available, but Edit Agent never exposed
the selection.

Personal connections remain runtime bindings rather than source content.
Selecting a different API model first saves the Revision choice and then
explicitly clears an active personal binding. Restoring the same
normalized source model skips the Revision write and only clears the
runtime subscription, including when source/picker IDs use different
provider prefixes. A failed clear remains visible and retryable. When
the source model changes, Revision saves await backend Apply before
clearing the runtime binding. Dirty/read-only revisions and busy/loading
states keep subscription selection disabled. Both sources now wait for a
successful runtime model lookup: before that read, an absent connection
means unknown, so an API-only source save could silently leave an
unobserved subscription active. This includes provisioning/lookup
failures and is covered by a regression test.

Save failures no longer hide the model list: Edit Agent retains its
Settings error, while the launcher reports failure through the existing
toast. Only query/load errors enter the picker error state, so a failed
save can be retried by selecting the model again. New Chat Retry also
refetches the Agent definition and its working/active Revision queries;
missing Revision IDs are skipped and identical IDs share one refetch.

## Test plan

- [x] 93 targeted tests passed after the same-model restoration fix. The
new real Settings/controller regression fails on the old implementation
for `litellm/` and bare source IDs; it now passes without any Revision
commit. Also covers unchanged-source gates, changed-model save ordering,
and clear-failure retry.

- [x] 110 targeted tests passed after the review fix: workspace model
flow, shared composer, Revision warnings, Settings flow, and launcher
Revision query/save behavior.
- [x] Regression checks retain selection after a failed Settings save
and retry a failed launcher model save with the same idempotency key.
Genuine runtime lookup errors still expose Retry.
- [x] 97 targeted tests passed after the launcher Retry fix, including
definition/working/active lookup failure recovery through the picker
controller and no requests for missing Revision IDs.
- [x] Frontend TypeScript, changed-file ESLint, and governance guards.
- [x] Covered Edit Agent/New Task selection, active model display,
reconnection, API return, failed saves/retries, backend admission, and
runtime lookup errors with an actionable Retry button.
- Full frontend suites/build/security checks run in CI. Local pnpm
global virtual-store resolution initially prevented test startup;
reinstalled this worktree with the local virtual store, with no
dependency/lockfile changes.

Frontend-only follow-up; the existing staging Engine beta and backend
authorization endpoints are sufficient. This PR requires the ECAP web
deployment after merge, with no additional Engine release.
```

### PR Body

```
## Summary

Edit Agent now offers the same admitted Personal Codex models as New Task. The picker displays an active personal runtime model, while ordinary API model edits continue to save through the Revision flow.

## Root cause

The workspace passed subscription choices only in use mode, and the shared composer additionally suppressed them whenever a Revision model controller was present. The backend runtime grants in #3927 and zooclaw-engine#1761 were already available, but Edit Agent never exposed the selection.

Personal connections remain runtime bindings rather than source content. Selecting a different API model first saves the Revision choice and then explicitly clears an active personal binding. Restoring the same normalized source model skips the Revision write and only clears the runtime subscription, including when source/picker IDs use different provider prefixes. A failed clear remains visible and retryable. When the source model changes, Revision saves await backend Apply before clearing the runtime binding. Dirty/read-only revisions and busy/loading states keep subscription selection disabled. Both sources now wait for a successful runtime model lookup: before that read, an absent connection means unknown, so an API-only source save could silently leave an unobserved subscription active. This includes provisioning/lookup failures and is covered by a regression test.

Save failures no longer hide the model list: Edit Agent retains its Settings error, while the launcher reports failure through the existing toast. Only query/load errors enter the picker error state, so a failed save can be retried by selecting the model again. New Chat Retry also refetches the Agent definition and its working/active Revision queries; missing Revision IDs are skipped and identical IDs share one refetch.

## Test plan

- [x] 93 targeted tests passed after the same-model restoration fix. The new real Settings/controller regression fails on the old implementation for `litellm/` and bare source IDs; it now passes without any Revision commit. Also covers unchanged-source gates, changed-model save ordering, and clear-failure retry.

- [x] 110 targeted tests passed after the review fix: workspace model flow, shared composer, Revision warnings, Settings flow, and launcher Revision query/save behavior.
- [x] Regression checks retain selection after a failed Settings save and retry a failed launcher model save with the same idempotency key. Genuine runtime lookup errors still expose Retry.
- [x] 97 targeted tests passed after the launcher Retry fix, including definition/working/active lookup failure recovery through the picker controller and no requests for missing Revision IDs.
- [x] Frontend TypeScript, changed-file ESLint, and governance guards.
- [x] Covered Edit Agent/New Task selection, active model display, reconnection, API return, failed saves/retries, backend admission, and runtime lookup errors with an actionable Retry button.
- Full frontend suites/build/security checks run in CI. Local pnpm global virtual-store resolution initially prevented test startup; reinstalled this worktree with the local virtual store, with no dependency/lockfile changes.

Frontend-only follow-up; the existing staging Engine beta and backend authorization endpoints are sufficient. This PR requires the ECAP web deployment after merge, with no additional Engine release.
```

---

## feat(platform): establish Project key identity alongside Work tokens (#3939)

- **SHA**: `84cd82b18cdb93a9a749285ad5303f49b6ddd42f`
- **作者**: finn-srp
- **日期**: 2026-09-30T03:10:47Z
- **PR**: #3939

### Commit Message

```
feat(platform): establish Project key identity alongside Work tokens (#3939)

## Summary

- Tighten Project API key queries to exclude rows assigned to another
Organization while keeping legacy named-key rows without an Organization
ID readable through their Project.
- Add `owner_uid` to the validated Platform machine principal, resolved
from the active personal Platform Organization and active Platform user.
The key's `created_by` remains audit metadata.
- Add an opt-in `mixed` `/service/v1` auth mode. It routes `zct_` Work
tokens and `zwp_live_` Platform keys to their separate verifiers without
fallback. The deployed default stays `legacy`.
- Cover Key creation, listing, repeated revocation, UID/Project
isolation, mixed routing and the existing Engine gate. Document the
identity boundary and remaining runtime contract.

## Validation

- Focused service and repository tests: 158 passed; the final
no-fallback test is included in the full suite.
- Full local Python CI-equivalent gate: 13,053 passed, 5 skipped,
coverage 89.83%. Dependency resolution, static checks, CI lint and both
duplication checks passed.

## Scope and rollout

- Builds on merged login PR #3937 and supersedes closed PR #3938.
- A Platform Key can authenticate in opt-in mode but still receives
`platform.engine_access_not_ready` for Engine resources and Usage. This
PR does not issue durable Agent credentials, enable SDK runtime,
implement UID Billing or Usage, deploy, clean existing staging data, or
run a billable live test.
- The named-key filter first passed a [read-only staging CSFLE
check](docs/staging-validation/2026-09-30-platform-key-query-csfle-readonly.md).
With approved isolated staging fixtures, the current PR repository code
then passed [actual encrypted-client list, lookup, and revoke
operations](docs/staging-validation/2026-09-30-platform-key-csfle-fixture.md)
for Organization-bound and legacy missing-Organization rows. Each revoke
changed one row, repeats changed none, and both fixture rows were
deleted and verified absent. No deploy or billable request was
performed.
```

### PR Body

```
## Summary

- Tighten Project API key queries to exclude rows assigned to another Organization while keeping legacy named-key rows without an Organization ID readable through their Project.
- Add `owner_uid` to the validated Platform machine principal, resolved from the active personal Platform Organization and active Platform user. The key's `created_by` remains audit metadata.
- Add an opt-in `mixed` `/service/v1` auth mode. It routes `zct_` Work tokens and `zwp_live_` Platform keys to their separate verifiers without fallback. The deployed default stays `legacy`.
- Cover Key creation, listing, repeated revocation, UID/Project isolation, mixed routing and the existing Engine gate. Document the identity boundary and remaining runtime contract.

## Validation

- Focused service and repository tests: 158 passed; the final no-fallback test is included in the full suite.
- Full local Python CI-equivalent gate: 13,053 passed, 5 skipped, coverage 89.83%. Dependency resolution, static checks, CI lint and both duplication checks passed.

## Scope and rollout

- Builds on merged login PR #3937 and supersedes closed PR #3938.
- A Platform Key can authenticate in opt-in mode but still receives `platform.engine_access_not_ready` for Engine resources and Usage. This PR does not issue durable Agent credentials, enable SDK runtime, implement UID Billing or Usage, deploy, clean existing staging data, or run a billable live test.
- The named-key filter first passed a [read-only staging CSFLE check](docs/staging-validation/2026-09-30-platform-key-query-csfle-readonly.md). With approved isolated staging fixtures, the current PR repository code then passed [actual encrypted-client list, lookup, and revoke operations](docs/staging-validation/2026-09-30-platform-key-csfle-fixture.md) for Organization-bound and legacy missing-Organization rows. Each revoke changed one row, repeats changed none, and both fixture rows were deleted and verified absent. No deploy or billable request was performed.
```

---
