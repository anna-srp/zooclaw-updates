# SerendipityOneInc/ecap-workspace — commits 2026-09-02

## feat(claw-interface): track Business member LLM usage from join time (#3516)

- **SHA**: `4d9eedb4fa608252bc222490c3d4e488101f774c`
- **作者**: sharplee-srp
- **日期**: 2026-09-02T13:50:26Z
- **PR**: #3516

### Commit Message

```
feat(claw-interface): track Business member LLM usage from join time (#3516)

## Linear

_None — this came out of a production billing investigation, not a
tracked issue._

## Problem

Business members on an **Unlimited** LLM quota show `0` usage on the
Usage page no matter how much they actually spend.

Root cause is in LiteLLM, not in our aggregation: LiteLLM only creates a
`LiteLLM_TeamMembership` row when a member is *added to a team with
budget fields*. A member bound to a Business team without a quota never
gets that row. LiteLLM then increments member spend with an
`update_many` against the missing row, which matches zero documents and
**silently drops every increment** — no error, no log, just a permanent
`0`.

So the members most likely to spend the most (Unlimited) are exactly the
ones that are never metered.

## What this PR does

**1. Ensure the tracking row at every Business bind point.**

New `app/services/org/member_usage_tracking.py` wraps billing-gateway's
`ensure_tracking` mode: create an unlimited, window-only row when
missing; otherwise repin the period boundary while preserving the
member's quota and accumulated spend. It is called right after the key
bind in all seven paths:

- accept invite / join org
- personal to business upgrade
- suspended member resume
- existing-account enterprise handoff
- first billing-key bootstrap
- plan / model-access rebind
- team org creation

The call is **best-effort and time-boxed (10s)**: the bind has already
succeeded by the time it runs, so a failure or a `reset_pending` result
logs and continues rather than rolling anything back. `suspended`
members are included on purpose — suspend only moves the key to a
personal fallback team, so the Business membership row and its
accumulated spend survive and must stay pinned.

**2. Omitted-vs-null quota semantics on `POST
/orgs/{org_id}/users/{uid}/llm-quota`.**

An omitted `quota_credits` now means *repin only* (preserve the quota,
re-align the window); an explicit `null` means *clear the quota to
Unlimited*. `ge=1` is unchanged, so a `0` quota still cannot reach
billing-gateway.

**3. Unknown usage is explicit end to end.**

`tracking_status` is passed through from billing-gateway; when the
gateway omits it, `not_initialized` is derived from a missing
`budget_reset_at`, otherwise `tracked`. `used_credits` stays a non-null
number on the wire for backward compatibility, but enterprise-admin now
treats `tracking_status == "not_initialized"` as authoritative: it
displays `Unknown`, excludes the row from member totals/share and
usage-based filters, exports an unknown value in CSV, and offers an
Untracked filter. The Users table no longer renders `0 / quota` for an
untracked member.

The row Retry action sends `{}` to the existing quota endpoint, so an
admin can initialize/repin tracking without changing the member's quota.
`_to_public` also no longer requires a quota to report `reset_pending`,
so an Unlimited member's drifted window remains visible and retryable.

**4. Rollover hook now repins Unlimited members.**

After a credit reset LiteLLM recomputes the member budget from its own
clock and normalizes it to a *calendar-month* boundary. The rollover
hook previously skipped every member without a positive quota, so
Unlimited members drifted onto LiteLLM's month boundary and got reset
mid credit period — undercounting again. They are now aligned through
the same quota-preserving ensure call. Expired boundaries are still left
alone (LiteLLM's reset job has to zero the row before its boundary can
move). Concurrency stays 5; the deadline scales with member count
(`min(300, max(30, 2n))` s) and truncation is logged with a count.
Members who left the org are excluded. The ensure client falls back to
the legacy repin body on a 422 from an older gateway, so this hook keeps
working for limited members regardless of deploy order. The first
enterprise-package grant also runs the sweep so founding members get a
row as soon as a credit period exists.

Eligibility repository failures fail closed: if the org or membership
list cannot be read, no member is aligned. A confirmed absence of a
local org mapping retains the previous align-all fallback. Failed ensure
calls are not counted as settled, so any later timeout reports the true
number of unresolved members.

**5. Controlled backfill and production completion gate.**

`services/claw-interface/scripts/backfill_member_usage_tracking.py`
walks every `org_type=team` org and ensures a row for its `active` and
`suspended` members. `--dry-run` is the default, `--write` applies, and
`--verify` performs a fresh read-only completion check. The JSON reports
failed org/member counts plus remaining `members_not_initialized` and
`members_repin_needed`; verify exits non-zero while failures or fixable
rows remain.

The script reads first and only writes where the row is missing or
drifted, so it never clears a quota, never resets a spend counter, and
re-running a converged org is a no-op. Orgs with no current credit
period are counted as skipped rather than failing the walk.

The production procedure and gate are committed in
`docs/production-validation/2026-09-01-member-usage-tracking-rollout.md`.

## Rollout order

**The billing-gateway PR must deploy FIRST.**

- SerendipityOneInc/billing-gateway#69
(`feat/member-usage-tracking-ensure`).
- Then deploy claw-interface and enterprise-admin from this PR.
- Run the reviewed dry-run, one write, and final `--verify` from the
production runbook.
- Production completion requires `converged=true`, zero org/member
failures, `members_not_initialized=0`, and `members_repin_needed=0`.

The contract changes are backward compatible: an older billing-gateway
returns **422** on the unknown `ensure_tracking` field, and the
best-effort wrapper tolerates that (logs and continues, bind is
unaffected). So merging this first is safe but inert — no tracking rows
get created until billing-gateway ships.

## Test plan

- [x] Backend PR-related unit tests: **256 passed**; backfill targeted
suite: **16 passed**.
- [x] Changed backend files: Ruff check + format passed; Pyright has 0
errors; import-linter keeps all 8 contracts.
- [x] enterprise-admin targeted tests: **69 passed**; full suite under
CI's UTC timezone: **426 passed**; ESLint and `tsc --noEmit` pass.
- [x] Fresh isolated A102 E2E against the production LiteLLM image
(`ghcr.io/berriai/litellm-database@sha256:8075b0…`) with real
Postgres/Mongo/Redis, billing-gateway#69, and this branch: **7 scenarios
/ 84 assertions passed**.
- [x] E2E completion gate: `--verify` exits 0 with `converged=true`,
zero failures, `members_not_initialized=0`, and
`members_repin_needed=0`.
- [x] Real-browser enterprise-admin check: before backfill, the legacy
row shows `Unknown`, share `—`, and `Tracking not initialized`; after
backfill and one metered request it shows `6 credits / 16.7%` and no
tracking warning.

`verify-local --changed` still surfaces an unrelated repository-wide
Ruff baseline (72 lint findings and 20 format drifts outside this PR).
The changed files and all scoped checks above pass; unrelated files were
intentionally left untouched.

## Size override justification

The PR is **3287 changed lines** against the repository's 3000-line
budget. The 287-line overage comes from the reviewer-requested
unknown-state and rollover-failure coverage, backfill verification
tests, and the production rollout runbook. Splitting those from the
implementation would separate the safety gate and tests from the code
they validate, so `size-override` is applied for this review round.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01DN37xKgDJNupV4VSFYdjWY

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Linear

_None — this came out of a production billing investigation, not a tracked issue._

## Problem

Business members on an **Unlimited** LLM quota show `0` usage on the Usage page no matter how much they actually spend.

Root cause is in LiteLLM, not in our aggregation: LiteLLM only creates a `LiteLLM_TeamMembership` row when a member is *added to a team with budget fields*. A member bound to a Business team without a quota never gets that row. LiteLLM then increments member spend with an `update_many` against the missing row, which matches zero documents and **silently drops every increment** — no error, no log, just a permanent `0`.

So the members most likely to spend the most (Unlimited) are exactly the ones that are never metered.

## What this PR does

**1. Ensure the tracking row at every Business bind point.**

New `app/services/org/member_usage_tracking.py` wraps billing-gateway's `ensure_tracking` mode: create an unlimited, window-only row when missing; otherwise repin the period boundary while preserving the member's quota and accumulated spend. It is called right after the key bind in all seven paths:

- accept invite / join org
- personal to business upgrade
- suspended member resume
- existing-account enterprise handoff
- first billing-key bootstrap
- plan / model-access rebind
- team org creation

The call is **best-effort and time-boxed (10s)**: the bind has already succeeded by the time it runs, so a failure or a `reset_pending` result logs and continues rather than rolling anything back. `suspended` members are included on purpose — suspend only moves the key to a personal fallback team, so the Business membership row and its accumulated spend survive and must stay pinned.

**2. Omitted-vs-null quota semantics on `POST /orgs/{org_id}/users/{uid}/llm-quota`.**

An omitted `quota_credits` now means *repin only* (preserve the quota, re-align the window); an explicit `null` means *clear the quota to Unlimited*. `ge=1` is unchanged, so a `0` quota still cannot reach billing-gateway.

**3. Unknown usage is explicit end to end.**

`tracking_status` is passed through from billing-gateway; when the gateway omits it, `not_initialized` is derived from a missing `budget_reset_at`, otherwise `tracked`. `used_credits` stays a non-null number on the wire for backward compatibility, but enterprise-admin now treats `tracking_status == "not_initialized"` as authoritative: it displays `Unknown`, excludes the row from member totals/share and usage-based filters, exports an unknown value in CSV, and offers an Untracked filter. The Users table no longer renders `0 / quota` for an untracked member.

The row Retry action sends `{}` to the existing quota endpoint, so an admin can initialize/repin tracking without changing the member's quota. `_to_public` also no longer requires a quota to report `reset_pending`, so an Unlimited member's drifted window remains visible and retryable.

**4. Rollover hook now repins Unlimited members.**

After a credit reset LiteLLM recomputes the member budget from its own clock and normalizes it to a *calendar-month* boundary. The rollover hook previously skipped every member without a positive quota, so Unlimited members drifted onto LiteLLM's month boundary and got reset mid credit period — undercounting again. They are now aligned through the same quota-preserving ensure call. Expired boundaries are still left alone (LiteLLM's reset job has to zero the row before its boundary can move). Concurrency stays 5; the deadline scales with member count (`min(300, max(30, 2n))` s) and truncation is logged with a count. Members who left the org are excluded. The ensure client falls back to the legacy repin body on a 422 from an older gateway, so this hook keeps working for limited members regardless of deploy order. The first enterprise-package grant also runs the sweep so founding members get a row as soon as a credit period exists.

Eligibility repository failures fail closed: if the org or membership list cannot be read, no member is aligned. A confirmed absence of a local org mapping retains the previous align-all fallback. Failed ensure calls are not counted as settled, so any later timeout reports the true number of unresolved members.

**5. Controlled backfill and production completion gate.**

`services/claw-interface/scripts/backfill_member_usage_tracking.py` walks every `org_type=team` org and ensures a row for its `active` and `suspended` members. `--dry-run` is the default, `--write` applies, and `--verify` performs a fresh read-only completion check. The JSON reports failed org/member counts plus remaining `members_not_initialized` and `members_repin_needed`; verify exits non-zero while failures or fixable rows remain.

The script reads first and only writes where the row is missing or drifted, so it never clears a quota, never resets a spend counter, and re-running a converged org is a no-op. Orgs with no current credit period are counted as skipped rather than failing the walk.

The production procedure and gate are committed in `docs/production-validation/2026-09-01-member-usage-tracking-rollout.md`.

## Rollout order

**The billing-gateway PR must deploy FIRST.**

- SerendipityOneInc/billing-gateway#69 (`feat/member-usage-tracking-ensure`).
- Then deploy claw-interface and enterprise-admin from this PR.
- Run the reviewed dry-run, one write, and final `--verify` from the production runbook.
- Production completion requires `converged=true`, zero org/member failures, `members_not_initialized=0`, and `members_repin_needed=0`.

The contract changes are backward compatible: an older billing-gateway returns **422** on the unknown `ensure_tracking` field, and the best-effort wrapper tolerates that (logs and continues, bind is unaffected). So merging this first is safe but inert — no tracking rows get created until billing-gateway ships.

## Test plan

- [x] Backend PR-related unit tests: **256 passed**; backfill targeted suite: **16 passed**.
- [x] Changed backend files: Ruff check + format passed; Pyright has 0 errors; import-linter keeps all 8 contracts.
- [x] enterprise-admin targeted tests: **69 passed**; full suite under CI's UTC timezone: **426 passed**; ESLint and `tsc --noEmit` pass.
- [x] Fresh isolated A102 E2E against the production LiteLLM image (`ghcr.io/berriai/litellm-database@sha256:8075b0…`) with real Postgres/Mongo/Redis, billing-gateway#69, and this branch: **7 scenarios / 84 assertions passed**.
- [x] E2E completion gate: `--verify` exits 0 with `converged=true`, zero failures, `members_not_initialized=0`, and `members_repin_needed=0`.
- [x] Real-browser enterprise-admin check: before backfill, the legacy row shows `Unknown`, share `—`, and `Tracking not initialized`; after backfill and one metered request it shows `6 credits / 16.7%` and no tracking warning.

`verify-local --changed` still surfaces an unrelated repository-wide Ruff baseline (72 lint findings and 20 format drifts outside this PR). The changed files and all scoped checks above pass; unrelated files were intentionally left untouched.

## Size override justification

The PR is **3287 changed lines** against the repository's 3000-line budget. The 287-line overage comes from the reviewer-requested unknown-state and rollover-failure coverage, backfill verification tests, and the production rollout runbook. Splitting those from the implementation would separate the safety gate and tests from the code they validate, so `size-override` is applied for this review round.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01DN37xKgDJNupV4VSFYdjWY


---

## fix(agents): 展示垂直行业包 Agent 更新提示 (#3627)

- **SHA**: `7506b2f777833f17ab17ed17a57b9ac62f6d3fda`
- **作者**: lynn Zhuang
- **日期**: 2026-09-02T13:45:11Z
- **PR**: #3627

### Commit Message

```
fix(agents): 展示垂直行业包 Agent 更新提示 (#3627)

## 变更摘要
- 在判断已安装 Agent 是否有更新时，纳入当前登录用户的垂直行业套餐 Agent Pack
- 在侧边栏过期 Agent 的 New Task 旁展示紧凑的品牌紫色更新按钮，覆盖主 Agent 和附加 Agent
- 更新开始后，即使鼠标移出 Agent 行也持续显示 Updating；快速请求至少展示 500ms 的加载反馈
- 增加垂直行业包、computer runtime、侧边栏按钮顺序与常驻状态、快速更新反馈的回归测试

## 根因
原有更新判断仅对比 Marketplace、组织私有包或分享包目录，并且排除了非 engine runtime。垂直行业套餐中的 Agent
Pack 来自当前垂直套餐接口，因此已安装 Agent 找不到对应的最新版本，界面无法显示更新状态。侧边栏此前也只渲染头像
badge，没有提供实际更新入口。

## 测试计划
- [x] 针对更新 hook、版本判断、侧边栏组件及相关测试运行 `bash scripts/verify-web.sh`
- [x] 通过 46 项 Vitest 定向测试，覆盖侧边栏及共享更新反馈
- [x] 通过 `bash scripts/verify-changed.sh`
- [x] 使用本地 mock 手动验证 Update、鼠标移出后的 Updating 常驻，以及成功后的按钮消失
```

### PR Body

## 变更摘要
- 在判断已安装 Agent 是否有更新时，纳入当前登录用户的垂直行业套餐 Agent Pack
- 在侧边栏过期 Agent 的 New Task 旁展示紧凑的品牌紫色更新按钮，覆盖主 Agent 和附加 Agent
- 更新开始后，即使鼠标移出 Agent 行也持续显示 Updating；快速请求至少展示 500ms 的加载反馈
- 增加垂直行业包、computer runtime、侧边栏按钮顺序与常驻状态、快速更新反馈的回归测试

## 根因
原有更新判断仅对比 Marketplace、组织私有包或分享包目录，并且排除了非 engine runtime。垂直行业套餐中的 Agent Pack 来自当前垂直套餐接口，因此已安装 Agent 找不到对应的最新版本，界面无法显示更新状态。侧边栏此前也只渲染头像 badge，没有提供实际更新入口。

## 测试计划
- [x] 针对更新 hook、版本判断、侧边栏组件及相关测试运行 `bash scripts/verify-web.sh`
- [x] 通过 46 项 Vitest 定向测试，覆盖侧边栏及共享更新反馈
- [x] 通过 `bash scripts/verify-changed.sh`
- [x] 使用本地 mock 手动验证 Update、鼠标移出后的 Updating 常驻，以及成功后的按钮消失


---

## feat(channels): add DingTalk to engine agents (#3624)

- **SHA**: `7de5eface078225d02b0304a579246086d0f2aca`
- **作者**: kaka-srp
- **日期**: 2026-09-02T11:34:51Z
- **PR**: #3624

### Commit Message

```
feat(channels): add DingTalk to engine agents (#3624)

## Linear

N/A — no issue was provided for this change.

## Summary

- expose DingTalk as a supported Engine channel in ECAP, with QR setup
as the default and manual `clientId`/`clientSecret` entry as fallback
- reuse the existing v1 DingTalk registration protocol while storing
Engine setup sessions separately and writing successful channels only to
ACS as platform `dingtalk`
- map the product platform `dingtalk-connector` across
list/create/update/remove, and protect QR polling with workspace-scoped
ownership, atomic terminal claims, and cross-pod interval gating
- preserve the legacy v1 flow unchanged; final agent review found no
scope expansion or redundant implementation

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh <changed paths>` — 118 passed, 69
skipped
- [x] focused backend channel/route/v1 suite — 181 passed
- [x] expanded Engine setup/session regression suite — 103 passed
- [x] focused frontend DingTalk/channel suite — 60 passed
- [x] frontend and Python source/test duplication checks
- [x] Python file-length, complexity, dead-code, Ruff, Pyright, ESLint,
TypeScript, and import-contract gates
- [ ] live DingTalk/Redis/ACS smoke (requires deployed credentials and
infrastructure)
```

### PR Body

## Linear

N/A — no issue was provided for this change.

## Summary

- expose DingTalk as a supported Engine channel in ECAP, with QR setup as the default and manual `clientId`/`clientSecret` entry as fallback
- reuse the existing v1 DingTalk registration protocol while storing Engine setup sessions separately and writing successful channels only to ACS as platform `dingtalk`
- map the product platform `dingtalk-connector` across list/create/update/remove, and protect QR polling with workspace-scoped ownership, atomic terminal claims, and cross-pod interval gating
- preserve the legacy v1 flow unchanged; final agent review found no scope expansion or redundant implementation

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh <changed paths>` — 118 passed, 69 skipped
- [x] focused backend channel/route/v1 suite — 181 passed
- [x] expanded Engine setup/session regression suite — 103 passed
- [x] focused frontend DingTalk/channel suite — 60 passed
- [x] frontend and Python source/test duplication checks
- [x] Python file-length, complexity, dead-code, Ruff, Pyright, ESLint, TypeScript, and import-contract gates
- [ ] live DingTalk/Redis/ACS smoke (requires deployed credentials and infrastructure)


---

## fix(ios): prevent sidebar session row overlap (#3619)

- **SHA**: `3ad90ee2f57bafc18614af141835b7612ad191ce`
- **作者**: shana-srp
- **日期**: 2026-09-02T10:27:28Z
- **PR**: #3619

### Commit Message

```
fix(ios): prevent sidebar session row overlap (#3619)

## Summary
- Prevent expanded sidebar session rows from overlapping the following
agent row.
- Let the conversation section use its intrinsic height while keeping
each conversation and history row at a consistent 36pt height.

## Root cause
The expanded conversation stack used 35pt inter-item spacing while being
forced into a fixed 237pt frame. With multiple conversations, its
children rendered beyond that frame, but the surrounding agent list only
reserved the fixed height, so later agent rows appeared underneath the
overflowing content.

## Test plan
- [x] `swiftlint lint --strict --no-cache
ZooClaw/Views/SidebarDrawerView.swift`
- [x] `xcrun swiftc -frontend -parse
ZooClaw/Views/SidebarDrawerView.swift`
- [x] Generic iOS Simulator Debug build with `xcodebuild`
- [x] Multi-conversation sidebar interaction preview confirms expanded
sessions no longer overlap subsequent agent rows

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

## Summary
- Prevent expanded sidebar session rows from overlapping the following agent row.
- Let the conversation section use its intrinsic height while keeping each conversation and history row at a consistent 36pt height.

## Root cause
The expanded conversation stack used 35pt inter-item spacing while being forced into a fixed 237pt frame. With multiple conversations, its children rendered beyond that frame, but the surrounding agent list only reserved the fixed height, so later agent rows appeared underneath the overflowing content.

## Test plan
- [x] `swiftlint lint --strict --no-cache ZooClaw/Views/SidebarDrawerView.swift`
- [x] `xcrun swiftc -frontend -parse ZooClaw/Views/SidebarDrawerView.swift`
- [x] Generic iOS Simulator Debug build with `xcodebuild`
- [x] Multi-conversation sidebar interaction preview confirms expanded sessions no longer overlap subsequent agent rows


---

## fix(ios): stop APNs pushes leaking across signed-in accounts (#3621)

- **SHA**: `e2688c2af518ca076b1ce5a51e3adb4632415659`
- **作者**: bill-srp
- **日期**: 2026-09-02T10:24:23Z
- **PR**: #3621

### Commit Message

```
fix(ios): stop APNs pushes leaking across signed-in accounts (#3621)

## Summary
- Cache the APNs push registration as an identity tuple (`tokenHex` +
ECAP uid + Mattermost user id) in a new Keychain record
(`mm_push_registration.v2`), deleting the legacy token-only cache so it
can never satisfy the skip check; switching accounts on the same device
now re-registers the token under the new Mattermost user.
- Register the device token immediately after Mattermost token
validation succeeds (using the server-authoritative user id) instead of
waiting for the WebSocket to reach connected; accounts with valid
credentials but no connectable bot now still validate and register.
Registration retries up to 3 times with short backoff, and only persists
the record on success.
- On sign-out, while the old credentials are still valid, make a
best-effort `PUT /api/v4/users/sessions/device` with
`device_notification_disabled: "true"` (2s timeout; 4xx treated as
server-unsupported) before disconnecting and clearing the local
registration record. Failures never block sign-out.

## Root cause
One iPhone/app install shares a single APNs token across every signed-in
ECAP account, but Mattermost delivers pushes per logical user: it reads
that user's sessions and sends to each saved DeviceId. ZooClaw cached
only the bare token hex, so after an account switch the "token
unchanged, skipping registration" guard left the token bound to the
previous account's session — and sign-out only cleared local state,
never the server-side DeviceId. Registration was also gated behind
WebSocket connect (and skipped entirely for no-bot accounts), so some
accounts never claimed the token at all while a stale account kept
receiving that phone's notifications.

Client-side fix covers normal sign-in/sign-out flows. Repairing
already-leaked tokens (kill/uninstall/legacy cases) needs a backend
token-owner registry — tracked as a follow-up phase.

## Test plan
- [x] New/updated Swift Testing coverage: identity-tuple skip vs.
re-register on ECAP-uid or MM-user change, no persistence on failure +
bounded retry, legacy key migration/cleanup, disable-device API payload
and 4xx compatibility, no-bot validation ordering, sign-out disables
device notifications before dropping credentials and survives a failing
disable call
- [x] Full simulator suite: 892/892 passed (`xcodebuild test`, iPhone 17
Pro)
- [x] `swiftlint --strict`: 0 violations
```

### PR Body

## Summary
- Cache the APNs push registration as an identity tuple (`tokenHex` + ECAP uid + Mattermost user id) in a new Keychain record (`mm_push_registration.v2`), deleting the legacy token-only cache so it can never satisfy the skip check; switching accounts on the same device now re-registers the token under the new Mattermost user.
- Register the device token immediately after Mattermost token validation succeeds (using the server-authoritative user id) instead of waiting for the WebSocket to reach connected; accounts with valid credentials but no connectable bot now still validate and register. Registration retries up to 3 times with short backoff, and only persists the record on success.
- On sign-out, while the old credentials are still valid, make a best-effort `PUT /api/v4/users/sessions/device` with `device_notification_disabled: "true"` (2s timeout; 4xx treated as server-unsupported) before disconnecting and clearing the local registration record. Failures never block sign-out.

## Root cause
One iPhone/app install shares a single APNs token across every signed-in ECAP account, but Mattermost delivers pushes per logical user: it reads that user's sessions and sends to each saved DeviceId. ZooClaw cached only the bare token hex, so after an account switch the "token unchanged, skipping registration" guard left the token bound to the previous account's session — and sign-out only cleared local state, never the server-side DeviceId. Registration was also gated behind WebSocket connect (and skipped entirely for no-bot accounts), so some accounts never claimed the token at all while a stale account kept receiving that phone's notifications.

Client-side fix covers normal sign-in/sign-out flows. Repairing already-leaked tokens (kill/uninstall/legacy cases) needs a backend token-owner registry — tracked as a follow-up phase.

## Test plan
- [x] New/updated Swift Testing coverage: identity-tuple skip vs. re-register on ECAP-uid or MM-user change, no persistence on failure + bounded retry, legacy key migration/cleanup, disable-device API payload and 4xx compatibility, no-bot validation ordering, sign-out disables device notifications before dropping credentials and survives a failing disable call
- [x] Full simulator suite: 892/892 passed (`xcodebuild test`, iPhone 17 Pro)
- [x] `swiftlint --strict`: 0 violations


---

## fix(chat): improve pasted links and upload cards (#3620)

- **SHA**: `7d15a631cd8eef34d8cc9c366c073edf181ee302`
- **作者**: shana-srp
- **日期**: 2026-09-02T08:44:17Z
- **PR**: #3620

### Commit Message

```
fix(chat): improve pasted links and upload cards (#3620)

## Summary
- show pasted URLs in full and keep them directly clickable in the
composer and transcript
- render non-image uploads as compact attachment cards with localized
progress state
- reuse the existing app-owned file-type icons and make resolved file
cards open their target URL

## Root cause
The rich-text editor truncated URL labels and disabled link interaction.
Non-image R2 uploads were represented as Markdown links, so they fell
through to the generic inline link badge instead of the existing
attachment-card visual system.

## Test plan
- [x] `pnpm exec vitest run src/__tests__/rich-text-input.test.tsx
src/__tests__/rich-text-input-utils.test.ts
src/__tests__/rich-text-input-url.test.ts` (103 tests)
- [x] `pnpm exec vitest run
tests/unit/components/markdown/render-markdown-to-html.unit.spec.ts` (68
tests)
- [x] `pnpm exec vitest run
tests/unit/components/chat/unified-chat-composer/UnifiedChatComposer.unit.spec.tsx
tests/unit/components/chat/unified-chat-composer/composer-file-type-icons.unit.spec.ts`
(56 tests)
- [x] `bash scripts/verify-changed.sh`
- [x] manually verified uploading and resolved file-card states in the
local mock Chat preview

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary
- show pasted URLs in full and keep them directly clickable in the composer and transcript
- render non-image uploads as compact attachment cards with localized progress state
- reuse the existing app-owned file-type icons and make resolved file cards open their target URL

## Root cause
The rich-text editor truncated URL labels and disabled link interaction. Non-image R2 uploads were represented as Markdown links, so they fell through to the generic inline link badge instead of the existing attachment-card visual system.

## Test plan
- [x] `pnpm exec vitest run src/__tests__/rich-text-input.test.tsx src/__tests__/rich-text-input-utils.test.ts src/__tests__/rich-text-input-url.test.ts` (103 tests)
- [x] `pnpm exec vitest run tests/unit/components/markdown/render-markdown-to-html.unit.spec.ts` (68 tests)
- [x] `pnpm exec vitest run tests/unit/components/chat/unified-chat-composer/UnifiedChatComposer.unit.spec.tsx tests/unit/components/chat/unified-chat-composer/composer-file-type-icons.unit.spec.ts` (56 tests)
- [x] `bash scripts/verify-changed.sh`
- [x] manually verified uploading and resolved file-card states in the local mock Chat preview


---

## feat(seo): establish ZooWork URL and sitemap contract (#3593)

- **SHA**: `aadea62d2beb125d4d0ba3ebe9c69ed05e4e1e29`
- **作者**: Mori-srp
- **日期**: 2026-09-02T08:26:44Z
- **PR**: #3593

### Commit Message

```
feat(seo): establish ZooWork URL and sitemap contract (#3593)

## Summary

Establish one ZooWork URL contract as the source of truth for public
marketing routes, redirects, metadata, navigation, and XML generation.

- Make Home, About, Pricing, and Solutions available at their ten real
locale URLs.
- Keep explicit locale URLs authoritative over `NEXT_LOCALE` and
`Accept-Language`.
- Serve the English homepage at `/` as a stable direct 200; redirect
only the exact `/en` alias to `/`.
- Make bare About, Pricing, and Solutions aliases one-hop 301s to their
English final URLs.
- Generate canonical, reciprocal hreflang, and English `x-default` only
from each page's real `availableLocales` contract.
- Keep locale-free Legal pages canonical and exclude aliases; retire
Contact as a direct 404 with no metadata surface.
- Generate `sitemap-main.xml` from the route contract and constrain the
root index to its four approved leaf sitemaps.
- Add production GET auditing for status, redirects, indexability,
canonical, hreflang, language markers, robots, XML, and legacy-domain
leakage.

## Local acceptance

- [x] Merged the latest `origin/main@8d3cdb5a8` without conflict.
- [x] `bash scripts/verify-changed.sh` — governance guards, TypeScript,
and ESLint passed.
- [x] All 19 changed unit-test files passed: 338/338 tests.
- [x] Home / About / Pricing / Solutions: 40/40 final locale URLs
returned direct 200 in the local runtime audit.
- [x] `/` remained direct 200 across no preference, Cookie,
`Accept-Language`, and conflicting-preference requests.
- [x] Local main-site audit: canonical, hreflang, alias, disabled route,
language marker, and legacy-domain issue counts were all zero.
- [x] `sitemap-main.xml`: exactly 55 contract-derived URLs, with no
missing, extra, or duplicate entry.
- [x] Root sitemap index: exactly four approved leaf sitemaps.
- [x] Legacy `/features` and `/:locale/features` aliases now use
explicit one-hop 301 responses; focused config tests passed 3/3.

The production build completed code compilation, but local static
prerender cannot be marked fully passed because this environment does
not contain a valid Firebase API key for the untouched `/en/features`
and `/en/contact` collection paths. CI `web-build-check` remains the
authoritative build gate.

## PR size exception

The repository size gate reports 3,549 changed lines against a
3,000-line threshold (`+2,790 / -759`), so this PR intentionally uses
the repository-supported `size-override` label. The 549-line excess is
dominated by the contract-coupled production GET auditor
(`audit-public-seo.ts`, 1,151 lines), its regression tests, and the
40-route content-readiness fixture. Keeping these gates with the URL
behavior ensures the release SHA cannot publish the XML/metadata change
without its production acceptance contract. This exception does not
waive TypeScript, ESLint, build, unit-test, CodeQL, review, or
production GET gates.

## Release boundary

This PR may merge to `main` and deploy to staging after current CI and
review pass, but it must not be released to production until all of the
following are true:

1. Tips, Industry D1, and Docs changes are deployed to production and
have fresh GET receipts.
2. The Blog leaf sitemap has a fresh release-window 200/readback
receipt.
3. The stacked brand-scope PR B is rebased onto main, reviewed, merged,
and included in the same locked production SHA.
4. The production release uses an immutable `ecap-vX.Y.Z-release`
tag/ref whose SHA exactly equals the approved locked main SHA.

The local all-surface audit intentionally still rejects 14
external-owner routes until their production deployments exist: three
external leaf sitemaps and eleven Industry detail pages. Do not treat
local XML generation or this PR's CI as production acceptance.

After production deployment, run:

```bash
cd web/app
pnpm exec tsx scripts/audit-public-seo.ts --phase main-production --root https://zoowork.ai/sitemap.xml
```

## Out of scope

- Industry hall redirect D2.
- Google Search Console submission.
- Unapproved repository-wide replacement of legal/history/tracking
identifiers.
- The four temporary legacy social-account URLs, which remain a
separately documented B exception until official ZooWork accounts exist.
```

### PR Body

## Summary

Establish one ZooWork URL contract as the source of truth for public marketing routes, redirects, metadata, navigation, and XML generation.

- Make Home, About, Pricing, and Solutions available at their ten real locale URLs.
- Keep explicit locale URLs authoritative over `NEXT_LOCALE` and `Accept-Language`.
- Serve the English homepage at `/` as a stable direct 200; redirect only the exact `/en` alias to `/`.
- Make bare About, Pricing, and Solutions aliases one-hop 301s to their English final URLs.
- Generate canonical, reciprocal hreflang, and English `x-default` only from each page's real `availableLocales` contract.
- Keep locale-free Legal pages canonical and exclude aliases; retire Contact as a direct 404 with no metadata surface.
- Generate `sitemap-main.xml` from the route contract and constrain the root index to its four approved leaf sitemaps.
- Add production GET auditing for status, redirects, indexability, canonical, hreflang, language markers, robots, XML, and legacy-domain leakage.

## Local acceptance

- [x] Merged the latest `origin/main@8d3cdb5a8` without conflict.
- [x] `bash scripts/verify-changed.sh` — governance guards, TypeScript, and ESLint passed.
- [x] All 19 changed unit-test files passed: 338/338 tests.
- [x] Home / About / Pricing / Solutions: 40/40 final locale URLs returned direct 200 in the local runtime audit.
- [x] `/` remained direct 200 across no preference, Cookie, `Accept-Language`, and conflicting-preference requests.
- [x] Local main-site audit: canonical, hreflang, alias, disabled route, language marker, and legacy-domain issue counts were all zero.
- [x] `sitemap-main.xml`: exactly 55 contract-derived URLs, with no missing, extra, or duplicate entry.
- [x] Root sitemap index: exactly four approved leaf sitemaps.
- [x] Legacy `/features` and `/:locale/features` aliases now use explicit one-hop 301 responses; focused config tests passed 3/3.

The production build completed code compilation, but local static prerender cannot be marked fully passed because this environment does not contain a valid Firebase API key for the untouched `/en/features` and `/en/contact` collection paths. CI `web-build-check` remains the authoritative build gate.

## PR size exception

The repository size gate reports 3,549 changed lines against a 3,000-line threshold (`+2,790 / -759`), so this PR intentionally uses the repository-supported `size-override` label. The 549-line excess is dominated by the contract-coupled production GET auditor (`audit-public-seo.ts`, 1,151 lines), its regression tests, and the 40-route content-readiness fixture. Keeping these gates with the URL behavior ensures the release SHA cannot publish the XML/metadata change without its production acceptance contract. This exception does not waive TypeScript, ESLint, build, unit-test, CodeQL, review, or production GET gates.

## Release boundary

This PR may merge to `main` and deploy to staging after current CI and review pass, but it must not be released to production until all of the following are true:

1. Tips, Industry D1, and Docs changes are deployed to production and have fresh GET receipts.
2. The Blog leaf sitemap has a fresh release-window 200/readback receipt.
3. The stacked brand-scope PR B is rebased onto main, reviewed, merged, and included in the same locked production SHA.
4. The production release uses an immutable `ecap-vX.Y.Z-release` tag/ref whose SHA exactly equals the approved locked main SHA.

The local all-surface audit intentionally still rejects 14 external-owner routes until their production deployments exist: three external leaf sitemaps and eleven Industry detail pages. Do not treat local XML generation or this PR's CI as production acceptance.

After production deployment, run:

```bash
cd web/app
pnpm exec tsx scripts/audit-public-seo.ts --phase main-production --root https://zoowork.ai/sitemap.xml
```

## Out of scope

- Industry hall redirect D2.
- Google Search Console submission.
- Unapproved repository-wide replacement of legal/history/tracking identifiers.
- The four temporary legacy social-account URLs, which remain a separately documented B exception until official ZooWork accounts exist.


---

## docs(feishu): simplify channel tool deployment (#3618)

- **SHA**: `8d3cdb5a8ed0ee14542bbabde43b3380b0e91c76`
- **作者**: kaka-srp
- **日期**: 2026-09-02T04:19:47Z
- **PR**: #3618

### Commit Message

```
docs(feishu): simplify channel tool deployment (#3618)

## Summary

- align the Feishu document-tools design with the final shared-token
architecture
- remove obsolete rollout-switch and dedicated-token requirements
- document the Engine-first, skills-second, ACS-last staging rollout
order
- record the worker-only sync topology, trust-boundary impact, migration
prerequisite, and validation evidence

## Verification

- `bash scripts/verify-changed.sh`
- `git diff --check`

## Tracking

No Linear issue was requested for this change.
```

### PR Body

## Summary

- align the Feishu document-tools design with the final shared-token architecture
- remove obsolete rollout-switch and dedicated-token requirements
- document the Engine-first, skills-second, ACS-last staging rollout order
- record the worker-only sync topology, trust-boundary impact, migration prerequisite, and validation evidence

## Verification

- `bash scripts/verify-changed.sh`
- `git diff --check`

## Tracking

No Linear issue was requested for this change.


---

## feat(ios): align sidebar and draft conversation flow (#3612)

- **SHA**: `5471efc7fd3b142b0db5d74ccf80ead1363dfa3d`
- **作者**: shana-srp
- **日期**: 2026-09-02T03:58:28Z
- **PR**: #3612

### Commit Message

```
feat(ios): align sidebar and draft conversation flow (#3612)

## Linear

N/A — split from #3043.

## Summary

- Restyle the iOS sidebar and align agent/history interactions with the
updated design.
- Persist empty conversation drafts per signed-in user, reuse them
safely, and reveal them only after real thread content exists.
- Create a missing conversation on first send and freeze the Mattermost
send target across asynchronous attachment uploads or sidebar changes.
- Port the chronological first 15 non-merge commits from #3043 onto the
current `main` workspace-based conversation APIs.

This is split 1 of 3 for #3043. Follow-up commits resolve Swift
compatibility, async target binding, attachment channel ownership, and
CI lint issues found during validation and review.

## Review handling

- `REQUEST_CHANGES`: fix before merge.
- `NEED_HUMAN_REVIEW`: Codex assesses whether the finding is worth
fixing; fix justified findings, otherwise leave a PR comment with the
technical rationale.

## Test plan

- [x] Build the ZooClaw app and test targets on the iOS 26.5 simulator.
- [x] Run `AgentConversationViewModelTests`, `AppCoordinatorTests`,
`MattermostViewModelThreadTests`, `SidebarAgentExpansionStateTests`,
`ChatInputSendTests`, and `MattermostViewModelAttachmentsTests` (45
tests passed).
- [x] Run Swift parser checks and `git diff --check` on
conflict-resolved files.

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

## Linear

N/A — split from #3043.

## Summary

- Restyle the iOS sidebar and align agent/history interactions with the updated design.
- Persist empty conversation drafts per signed-in user, reuse them safely, and reveal them only after real thread content exists.
- Create a missing conversation on first send and freeze the Mattermost send target across asynchronous attachment uploads or sidebar changes.
- Port the chronological first 15 non-merge commits from #3043 onto the current `main` workspace-based conversation APIs.

This is split 1 of 3 for #3043. Follow-up commits resolve Swift compatibility, async target binding, attachment channel ownership, and CI lint issues found during validation and review.

## Review handling

- `REQUEST_CHANGES`: fix before merge.
- `NEED_HUMAN_REVIEW`: Codex assesses whether the finding is worth fixing; fix justified findings, otherwise leave a PR comment with the technical rationale.

## Test plan

- [x] Build the ZooClaw app and test targets on the iOS 26.5 simulator.
- [x] Run `AgentConversationViewModelTests`, `AppCoordinatorTests`, `MattermostViewModelThreadTests`, `SidebarAgentExpansionStateTests`, `ChatInputSendTests`, and `MattermostViewModelAttachmentsTests` (45 tests passed).
- [x] Run Swift parser checks and `git diff --check` on conflict-resolved files.


---

## feat(admin): search orgs by user identity (#3617)

- **SHA**: `7dbce01066e2927fc46435b9969d31430ee55aef`
- **作者**: sam-srp
- **日期**: 2026-09-02T03:50:46Z
- **PR**: #3617

### Commit Message

```
feat(admin): search orgs by user identity (#3617)

## Summary

- add UID and email filters to the Dashboard Console Orgs page
- persist the new filters in URL search parameters
- extend `GET /internal/orgs` with exact creator UID and exact email
filtering
- resolve email matches through the authoritative `gem_account` profile
collection, then filter personal or team orgs by `created_by`
- treat combined UID and email filters as an intersection and avoid
querying orgs when the identity does not match

## Validation

- 72 targeted claw-interface tests
- Ruff format and lint
- Pyright
- all claw-interface custom lint scripts
- 45 targeted dashboard-console tests
- dashboard-console TypeScript typecheck and ESLint
- `git diff --check`

No new settings, database fields, or migrations.
```

### PR Body

## Summary

- add UID and email filters to the Dashboard Console Orgs page
- persist the new filters in URL search parameters
- extend `GET /internal/orgs` with exact creator UID and exact email filtering
- resolve email matches through the authoritative `gem_account` profile collection, then filter personal or team orgs by `created_by`
- treat combined UID and email filters as an intersection and avoid querying orgs when the identity does not match

## Validation

- 72 targeted claw-interface tests
- Ruff format and lint
- Pyright
- all claw-interface custom lint scripts
- 45 targeted dashboard-console tests
- dashboard-console TypeScript typecheck and ESLint
- `git diff --check`

No new settings, database fields, or migrations.

---

## fix(pack-tests): wait for sandbox readiness before preview (#3574)

- **SHA**: `e43138cd3fd477d72a28bea604260ced3aa9caf4`
- **作者**: sharplee-srp
- **日期**: 2026-09-02T03:37:23Z
- **PR**: #3574

### Commit Message

```
fix(pack-tests): wait for sandbox readiness before preview (#3574)

## Summary

- run the existing strict Agent Sandbox preparation barrier after the
preview Agent starts and before creating its Session
- reuse the bounded config-version retry path so config races are
resolved against the latest active version
- keep the preview unavailable when Sandbox or Skill preparation fails

## Root cause

The Pack test preview path started the Engine Agent and immediately
created a preview Session without waiting for strict Sandbox/Skill
readiness. A config update could therefore make the first workflow stale
before its initial sync, leaving the shared Skill view empty when the
first preview turn attempted to read `SKILL.md`.

## Dependency and rollout

Depends on SerendipityOneInc/zooclaw-engine#991. Deploy the Engine PR
first, then this ECAP change.

## Test plan

- [x] `pytest tests/unit/test_pack_test_engine_runtime_service.py
tests/unit/test_engine_agent_resource_class.py -q` — 22 passed
- [x] Ruff check and format check on both changed Python files
- [x] Pyright on both changed Python files — 0 errors
- [x] pre-commit changed-file checks, import contracts, and PR size gate
- [ ] Repository-wide `bash scripts/verify-py.sh` is blocked by existing
unrelated main-branch baseline issues: 72 Ruff findings, 20 files
requiring formatting, and 4 route-helper Pyright errors; all 8
import-linter contracts pass
```

### PR Body

## Summary

- run the existing strict Agent Sandbox preparation barrier after the preview Agent starts and before creating its Session
- reuse the bounded config-version retry path so config races are resolved against the latest active version
- keep the preview unavailable when Sandbox or Skill preparation fails

## Root cause

The Pack test preview path started the Engine Agent and immediately created a preview Session without waiting for strict Sandbox/Skill readiness. A config update could therefore make the first workflow stale before its initial sync, leaving the shared Skill view empty when the first preview turn attempted to read `SKILL.md`.

## Dependency and rollout

Depends on SerendipityOneInc/zooclaw-engine#991. Deploy the Engine PR first, then this ECAP change.

## Test plan

- [x] `pytest tests/unit/test_pack_test_engine_runtime_service.py tests/unit/test_engine_agent_resource_class.py -q` — 22 passed
- [x] Ruff check and format check on both changed Python files
- [x] Pyright on both changed Python files — 0 errors
- [x] pre-commit changed-file checks, import contracts, and PR size gate
- [ ] Repository-wide `bash scripts/verify-py.sh` is blocked by existing unrelated main-branch baseline issues: 72 Ruff findings, 20 files requiring formatting, and 4 route-helper Pyright errors; all 8 import-linter contracts pass


---

## feat(channels): expose Feishu document capabilities (#3605)

- **SHA**: `cb3e690218ff0a553970cdbebb2b3a41c0e2f72d`
- **作者**: kaka-srp
- **日期**: 2026-09-02T02:46:08Z
- **PR**: #3605

### Commit Message

```
feat(channels): expose Feishu document capabilities (#3605)

## Linear

None — this cross-repository implementation was approved without a
Linear issue.

## Summary

- Add the reviewed design for channel-backed native Feishu/Lark document
tools on managed Engine v2 Agents.
- Add claw-interface request/projection support for account-level
`permission_admin_enabled`, Agent-level capability sync, and
account-level Provider status.
- Add Web controls and separate sync/provider status presentation for
Engine Feishu channels.
- Make the dedicated permission field the only public mutation surface;
raw `config.tools` is rejected and ACS owns the stored `tools.perm`
block.

## Review decisions implemented

- Model source fact, desired capability, and applied Engine state as
separate layers.
- Keep v1 explicitly channel-backed; tool-only mode is a follow-up that
requires a separate Provider account/binding model.
- Aggregate `permission_admin_available` at Agent scope without using it
to authorize a selected account.
- Identify Engine-owned Skills with `managed_by='capability'` plus
`installed_by='agent-channel-service'`.
- Split capability sync state from per-account Provider scope/approval
state.

## Related PRs

- Engine contract, capability endpoint, and runner:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1078
- ACS execution and reconciliation:
https://github.com/SerendipityOneInc/agent-channel-service/pull/103
- Managed Skills:
https://github.com/SerendipityOneInc/ecap-skills/pull/272

## Validation

- `bash scripts/verify-py.sh` passed.
- Ownership/projection targeted backend suite: 126 passed.
- Web TypeScript and targeted ESLint passed.
- Web targeted suites: 203 passed, 69 skipped.
- Push-time changed-surface verification passed.
- Engine `verify:quick`: light tier 2785 passed, 2 skipped; heavy tier
1814 passed.
- ACS TypeScript, oxlint, build, and targeted unit/contract suites
passed.
- Skills repository linter passed with only 12 unrelated pre-existing
warnings.
- ACS PostgreSQL integration suite is present but was skipped locally
because `TEST_DATABASE_URL` is not configured.
- Staging Feishu/Lark end-to-end validation remains a rollout gate.

## Rollout dependencies

1. Merge Engine and publish `@zooclaw/channel-tools-contract@0.1.0`.
2. Refresh the ACS lockfile from the registry, then merge/deploy ACS
feature-off.
3. Merge and publish the managed Skills.
4. Enable Staging reconciliation, run dry-run backfill, and complete
Feishu/Lark E2E acceptance before Production.
```

### PR Body

## Linear

None — this cross-repository implementation was approved without a Linear issue.

## Summary

- Add the reviewed design for channel-backed native Feishu/Lark document tools on managed Engine v2 Agents.
- Add claw-interface request/projection support for account-level `permission_admin_enabled`, Agent-level capability sync, and account-level Provider status.
- Add Web controls and separate sync/provider status presentation for Engine Feishu channels.
- Make the dedicated permission field the only public mutation surface; raw `config.tools` is rejected and ACS owns the stored `tools.perm` block.

## Review decisions implemented

- Model source fact, desired capability, and applied Engine state as separate layers.
- Keep v1 explicitly channel-backed; tool-only mode is a follow-up that requires a separate Provider account/binding model.
- Aggregate `permission_admin_available` at Agent scope without using it to authorize a selected account.
- Identify Engine-owned Skills with `managed_by='capability'` plus `installed_by='agent-channel-service'`.
- Split capability sync state from per-account Provider scope/approval state.

## Related PRs

- Engine contract, capability endpoint, and runner: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1078
- ACS execution and reconciliation: https://github.com/SerendipityOneInc/agent-channel-service/pull/103
- Managed Skills: https://github.com/SerendipityOneInc/ecap-skills/pull/272

## Validation

- `bash scripts/verify-py.sh` passed.
- Ownership/projection targeted backend suite: 126 passed.
- Web TypeScript and targeted ESLint passed.
- Web targeted suites: 203 passed, 69 skipped.
- Push-time changed-surface verification passed.
- Engine `verify:quick`: light tier 2785 passed, 2 skipped; heavy tier 1814 passed.
- ACS TypeScript, oxlint, build, and targeted unit/contract suites passed.
- Skills repository linter passed with only 12 unrelated pre-existing warnings.
- ACS PostgreSQL integration suite is present but was skipped locally because `TEST_DATABASE_URL` is not configured.
- Staging Feishu/Lark end-to-end validation remains a rollout gate.

## Rollout dependencies

1. Merge Engine and publish `@zooclaw/channel-tools-contract@0.1.0`.
2. Refresh the ACS lockfile from the registry, then merge/deploy ACS feature-off.
3. Merge and publish the managed Skills.
4. Enable Staging reconciliation, run dry-run backfill, and complete Feishu/Lark E2E acceptance before Production.


---
