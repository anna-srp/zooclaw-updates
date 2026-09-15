# SerendipityOneInc/ecap-workspace — commits 2026-09-14

## fix(agents): keep recent conversation controls within sidebar (#3725)

- **SHA**: `f756f8c8fff47c1a8b0632e9c57be37da936a547`
- **作者**: kaka-srp
- **日期**: 2026-09-14T12:34:03Z
- **PR**: #3725

### Commit Message

```
fix(agents): keep recent conversation controls within sidebar (#3725)

## Summary

Long conversation titles could stretch the recent-history sidebar,
clipping titles and selected-row backgrounds and moving Show more / Show
less text outside the visible area. Keep all scrolling navigation
content within the sidebar so titles truncate and the controls remain
visible. On the compact sidebar, Load more uses an accessible icon
consistent with the existing fold control.

## Root cause

Radix ScrollArea wraps its content in a `display: table` element. The
intrinsic width of long, non-wrapping titles expanded that element: a
224px viewport had 744px-wide rows and buttons. A single grid column
with a zero minimum width constrains the content locally in
`AgentWorkspaceNav`.

Only the frontend needs deployment.

## Test plan

- [x] Existing navigation unit suite: 9 tests passed.
- [x] `bash scripts/verify-web.sh --no-test`: governance guards,
TypeScript and ESLint passed.
- [x] Chromium fixture renders the actual navigation component,
design-system ScrollArea/Button and compiled application CSS;
translations and view-model data are fixtures. Before/after geometry
confirms 744px → 224px content width and working title truncation.
- [x] Actual browser clicks verify 8 → 13 → 8 recents, scrolling to
footer controls in a short window, and Load more callbacks at desktop
and mobile widths, including a long channel name and status badge.
- [x] Independent Agent review: no findings.

Authenticated staging browser acceptance remains to be performed after
deployment.
```

### PR Body

## Summary

Long conversation titles could stretch the recent-history sidebar, clipping titles and selected-row backgrounds and moving Show more / Show less text outside the visible area. Keep all scrolling navigation content within the sidebar so titles truncate and the controls remain visible. On the compact sidebar, Load more uses an accessible icon consistent with the existing fold control.

## Root cause

Radix ScrollArea wraps its content in a `display: table` element. The intrinsic width of long, non-wrapping titles expanded that element: a 224px viewport had 744px-wide rows and buttons. A single grid column with a zero minimum width constrains the content locally in `AgentWorkspaceNav`.

Only the frontend needs deployment.

## Test plan

- [x] Existing navigation unit suite: 9 tests passed.
- [x] `bash scripts/verify-web.sh --no-test`: governance guards, TypeScript and ESLint passed.
- [x] Chromium fixture renders the actual navigation component, design-system ScrollArea/Button and compiled application CSS; translations and view-model data are fixtures. Before/after geometry confirms 744px → 224px content width and working title truncation.
- [x] Actual browser clicks verify 8 → 13 → 8 recents, scrolling to footer controls in a short window, and Load more callbacks at desktop and mobile widths, including a long channel name and status badge.
- [x] Independent Agent review: no findings.

Authenticated staging browser acceptance remains to be performed after deployment.


---

## fix(agents): restore unindexed web conversation history (#3722)

- **SHA**: `281719bd3762af2a65578328feb3df4734a1e03b`
- **作者**: kaka-srp
- **日期**: 2026-09-14T11:51:26Z
- **PR**: #3722

### Commit Message

```
fix(agents): restore unindexed web conversation history (#3722)

## Summary

Restore saved Web histories that have an original thread but no Engine
session index. The reported staging Agent has twelve nonempty Web
threads and one Feishu conversation; the previous Engine-only list
showed just three Web conversations and Feishu.

Merge owned original thread indexes before product pagination, preserve
saved titles, and deduplicate original roots and canonical Engine IDs.
Unindexed threads open with their original rich history in a read-only
view; existing Web and external-channel transports keep their behavior.
Reading or selecting these histories does not create sessions/threads,
bind ACS, replay inbound messages, or start an Agent.

Engine dependency:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1435 (deploy
first).

## Root cause

The previous compatibility fix only enriched sessions returned by
Engine. Nine original Web threads never entered that candidate set. One
canonical Engine ID also has a separate empty alias thread, so IDs alone
cannot deduplicate history.

Deletion metadata from the companion Engine change prevents deleted
sessions from reappearing through the Mongo fallback. ECAP requires an
explicit acknowledgement; an older Engine keeps the existing list
without unsafe fallback. Direct legacy reads enforce ownership, archive
and purpose boundaries. Older clients retain the text-history endpoint:
HTTP validation accepts its bounded original-thread continuation cursors
while preserving the existing Engine event cursor format and limit. A
failed access refresh stops exposing cached original-thread references.

## Test plan

- [x] Backend static/type/import checks and 92 targeted task, history,
and HTTP route tests. The legacy history regression follows actual
server-issued cursors through three HTTP requests and checks original
text, attachments, and rejection of cross-session, malformed, and
oversized cursors.
- [x] 16 targeted frontend tests and frontend static/type/lint guards.
The broad frontend run passed 5,820 tests with one unrelated Markdown
hydration timing failure; that file passed all 51 tests on isolated
rerun.
- [x] Candidate code through real staging encrypted Mongo and original
Mattermost threads: twelve Web plus one Feishu, all nine missing
titles/bodies readable, thirteen unique items across two-item pages.
- [x] Candidate Engine SQL against real staging/production PostgreSQL in
READ ONLY transactions; production encrypted Mongo query also passed.
These validate candidate code against dependencies, not deployed browser
behavior.
- [x] Independent review; stale-cache access and deleted-session
resurrection findings fixed.
- [ ] Deploy companion Engine change first, then claw-interface and web,
and verify the reported Agent in the browser. No live application/data
changes were made by this PR work.

Metadata reconciliation scans the scoped Engine inventory in bounded
pages. Measured production SQL (1,184 rows) took 98 ms and the encrypted
Mongo page 149 ms; deployed endpoint latency still needs rollout
acceptance.

Design and validation details:
`docs/superpowers/specs/2026-09-14-unindexed-web-history-design.md`.
```

### PR Body

## Summary

Restore saved Web histories that have an original thread but no Engine session index. The reported staging Agent has twelve nonempty Web threads and one Feishu conversation; the previous Engine-only list showed just three Web conversations and Feishu.

Merge owned original thread indexes before product pagination, preserve saved titles, and deduplicate original roots and canonical Engine IDs. Unindexed threads open with their original rich history in a read-only view; existing Web and external-channel transports keep their behavior. Reading or selecting these histories does not create sessions/threads, bind ACS, replay inbound messages, or start an Agent.

Engine dependency: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1435 (deploy first).

## Root cause

The previous compatibility fix only enriched sessions returned by Engine. Nine original Web threads never entered that candidate set. One canonical Engine ID also has a separate empty alias thread, so IDs alone cannot deduplicate history.

Deletion metadata from the companion Engine change prevents deleted sessions from reappearing through the Mongo fallback. ECAP requires an explicit acknowledgement; an older Engine keeps the existing list without unsafe fallback. Direct legacy reads enforce ownership, archive and purpose boundaries. Older clients retain the text-history endpoint: HTTP validation accepts its bounded original-thread continuation cursors while preserving the existing Engine event cursor format and limit. A failed access refresh stops exposing cached original-thread references.

## Test plan

- [x] Backend static/type/import checks and 92 targeted task, history, and HTTP route tests. The legacy history regression follows actual server-issued cursors through three HTTP requests and checks original text, attachments, and rejection of cross-session, malformed, and oversized cursors.
- [x] 16 targeted frontend tests and frontend static/type/lint guards. The broad frontend run passed 5,820 tests with one unrelated Markdown hydration timing failure; that file passed all 51 tests on isolated rerun.
- [x] Candidate code through real staging encrypted Mongo and original Mattermost threads: twelve Web plus one Feishu, all nine missing titles/bodies readable, thirteen unique items across two-item pages.
- [x] Candidate Engine SQL against real staging/production PostgreSQL in READ ONLY transactions; production encrypted Mongo query also passed. These validate candidate code against dependencies, not deployed browser behavior.
- [x] Independent review; stale-cache access and deleted-session resurrection findings fixed.
- [ ] Deploy companion Engine change first, then claw-interface and web, and verify the reported Agent in the browser. No live application/data changes were made by this PR work.

Metadata reconciliation scans the scoped Engine inventory in bounded pages. Measured production SQL (1,184 rows) took 98 ms and the encrypted Mongo page 149 ms; deployed endpoint latency still needs rollout acceptance.

Design and validation details: `docs/superpowers/specs/2026-09-14-unindexed-web-history-design.md`.


---

## fix(chat): allow a.zoowork.ai artifact host for previews (#3721)

- **SHA**: `16b9836447ddbb34db260bd83b72576916b4af65`
- **作者**: bill-srp
- **日期**: 2026-09-14T10:38:00Z
- **PR**: #3721

### Commit Message

```
fix(chat): allow a.zoowork.ai artifact host for previews (#3721)

## Summary
- Add `a.zoowork.ai` to `STABLE_ARTIFACT_HOSTS` in
`web/app/src/lib/artifacts/stable-hosts.ts`, keeping the four existing
hosts.
- Cover the new host in `types.unit.spec.ts` (`isArtifactUrl`) and
`published-artifact.unit.spec.ts` (`parsePublishedArtifactRefs`).
- Web app only. No changes to `services/`, `desktop/`, or `ios/`.

## Root cause
`STABLE_ARTIFACT_HOSTS` is the single allowlist behind
`isStableArtifactHost` / `isArtifactUrl`, which gate artifact preview,
file-card extraction, and published-artifact ref parsing. After the
ZooWork rebrand the production V2 artifact origin moved to
`a.zoowork.ai`, but the allowlist still listed only `a.zooclaw.ai`, so
URLs on the new host were rejected and no preview rendered.

Not in scope here (noted for follow-up): the legacy V1 host picker in
`WorkspaceShared.tsx` and `services/claw-interface/.../artifact_url.py`
still branch on the hostname containing `zooclaw`, so on `zoowork.ai`
they fall through to the staging host.

## Test plan
- [x] TDD: added the `a.zoowork.ai` assertion first and confirmed it
failed, then added the host and confirmed green.
- [x] `pnpm vitest run --config ./vitest.config.mts
tests/unit/components/artifacts
tests/unit/models/published-artifact.unit.spec.ts` from `web/app`: 10
files, 126 tests passing.
- [ ] Staging/prod smoke: open a chat message with an
`https://a.zoowork.ai/...` artifact link and confirm the preview sidebar
and file card render.
```

### PR Body

## Summary
- Add `a.zoowork.ai` to `STABLE_ARTIFACT_HOSTS` in `web/app/src/lib/artifacts/stable-hosts.ts`, keeping the four existing hosts.
- Cover the new host in `types.unit.spec.ts` (`isArtifactUrl`) and `published-artifact.unit.spec.ts` (`parsePublishedArtifactRefs`).
- Web app only. No changes to `services/`, `desktop/`, or `ios/`.

## Root cause
`STABLE_ARTIFACT_HOSTS` is the single allowlist behind `isStableArtifactHost` / `isArtifactUrl`, which gate artifact preview, file-card extraction, and published-artifact ref parsing. After the ZooWork rebrand the production V2 artifact origin moved to `a.zoowork.ai`, but the allowlist still listed only `a.zooclaw.ai`, so URLs on the new host were rejected and no preview rendered.

Not in scope here (noted for follow-up): the legacy V1 host picker in `WorkspaceShared.tsx` and `services/claw-interface/.../artifact_url.py` still branch on the hostname containing `zooclaw`, so on `zoowork.ai` they fall through to the staging host.

## Test plan
- [x] TDD: added the `a.zoowork.ai` assertion first and confirmed it failed, then added the host and confirmed green.
- [x] `pnpm vitest run --config ./vitest.config.mts tests/unit/components/artifacts tests/unit/models/published-artifact.unit.spec.ts` from `web/app`: 10 files, 126 tests passing.
- [ ] Staging/prod smoke: open a chat message with an `https://a.zoowork.ai/...` artifact link and confirm the preview sidebar and file card render.


---

## fix(desktop): sync cloud conversation titles and rename (#3717)

- **SHA**: `8bf6ad5ad81ae0ce6f32f2db85c3b6b0c68abfa0`
- **作者**: zayne-srp
- **日期**: 2026-09-14T10:06:21Z
- **PR**: #3717

### Commit Message

```
fix(desktop): sync cloud conversation titles and rename (#3717)

## Summary
- Seed Remote V2 cloud conversation titles from the first message via
the existing Web creation API; refresh the affected workspace when the
title is ready.
- Route Remote V2 rename to the existing cloud API with
workspace/target-scoped cache updates. Preserve local Codex/Claude
behavior.
- Complete ZooWork branding for the window, tray, helper process, agent
descriptions, errors and installer product name.
- Reuse Web brand assets instead of overlaying obsolete Desktop images.
Preserve app ID, user-data directory, URL schemes and
environment-variable names for compatibility.

## Scope
- No Claw Interface, ACS, Engine or DSH runtime API changes.
- The pre-existing automatic-title/manual-rename race remains explicitly
out of scope.
- Existing untitled conversations are not bulk-backfilled.
- macOS upgrades use ZooWork.app; the old ZooClaw.app bundle should be
removed separately, without deleting application data.

## Validation
- Desktop: 52 tests passed, 1 optional Codex integration test skipped;
TypeScript passed.
- Latest combined branding/title build: 23 targeted frontend tests
passed; production build succeeded.
- Push-time TypeScript, ESLint and changed-surface checks passed.
- Built and locally ad-hoc signed ZooWork.app; installed and launched on
staging. UI, retained login/session list, Desktop bridge and signature
verification passed.
- Earlier Developer ID signed/notarized DMG contains title fixes but NOT
this subsequent branding update. It has not been rebuilt; this local
ZooWork.app is not a newly notarized distribution DMG.
```

### PR Body

## Summary
- Seed Remote V2 cloud conversation titles from the first message via the existing Web creation API; refresh the affected workspace when the title is ready.
- Route Remote V2 rename to the existing cloud API with workspace/target-scoped cache updates. Preserve local Codex/Claude behavior.
- Complete ZooWork branding for the window, tray, helper process, agent descriptions, errors and installer product name.
- Reuse Web brand assets instead of overlaying obsolete Desktop images. Preserve app ID, user-data directory, URL schemes and environment-variable names for compatibility.

## Scope
- No Claw Interface, ACS, Engine or DSH runtime API changes.
- The pre-existing automatic-title/manual-rename race remains explicitly out of scope.
- Existing untitled conversations are not bulk-backfilled.
- macOS upgrades use ZooWork.app; the old ZooClaw.app bundle should be removed separately, without deleting application data.

## Validation
- Desktop: 52 tests passed, 1 optional Codex integration test skipped; TypeScript passed.
- Latest combined branding/title build: 23 targeted frontend tests passed; production build succeeded.
- Push-time TypeScript, ESLint and changed-surface checks passed.
- Built and locally ad-hoc signed ZooWork.app; installed and launched on staging. UI, retained login/session list, Desktop bridge and signature verification passed.
- Earlier Developer ID signed/notarized DMG contains title fixes but NOT this subsequent branding update. It has not been rebuilt; this local ZooWork.app is not a newly notarized distribution DMG.


---

## fix(agents): restore migrated conversations in recent tasks (#3719)

- **SHA**: `20d80bd39c5d2b728c8bc75d9e6647c0e459b738`
- **作者**: kaka-srp
- **日期**: 2026-09-14T08:56:22Z
- **PR**: #3719

### Commit Message

```
fix(agents): restore migrated conversations in recent tasks (#3719)

## Summary

Restore migrated Web conversations in Recent conversations by reusing
their original saved titles and filling pages with visible sessions.
Manual and generated titles are preserved, Mongo archive state is
respected during list/read/select/open, and the original Mattermost
thread continues to supply the conversation body.

Use Engine's filtered activity cursor, retaining numeric-page
compatibility for older browsers. The frontend consumes opaque cursors
and deduplicates overlapping sessions. It also preserves the current
empty conversation on direct links and across tabs by using the
successful, authorized task read; it does not fabricate a task from a
URL or revive cached data after a failed read.

## Root cause

Engine paged before product visibility filtering, and import-time
updates pushed old Web sessions behind internal history. ECAP derived
titles only from public user events, which migrated Web sessions lack,
despite saved Mongo titles and readable Mattermost threads. The UI then
hid the titleless sessions.

Independent review also identified that the persisted selected-session
pointer can differ from the browser URL. That P2 is fixed and
independently re-reviewed with no findings.

## Test plan

- [x] Backend: 112 relevant tests passed, including original titles,
archive enforcement, thread aliases, visible-page refill, cursor
continuation, numeric compatibility, client/route contracts and
encrypted-Mongo query guards.
- [x] Frontend: original 32 related tests passed (two cold-import
timeouts passed on an unchanged-file rerun). Final direct-link fix: 18
relevant tests passed, with both new regressions first demonstrated
failing.
- [x] Backend static checks: ruff, format, full pyright and 8 import
contracts passed.
- [x] Frontend changed-surface type/lint/governance checks passed;
commit/push checks run normally.
- [x] Independent cross-repository review and follow-up review of the P2
correction completed.
- [x] Production read-only evidence confirmed saved titles and readable
original threads; the bounded Mongo query form was accepted by the
deployed encrypted client.
- [ ] After deployment, verify the 15 active migrated Web conversations
are discoverable with their original titles and readable bodies, the
already-archived conversation remains archived, and ordinary Web/WeCom
behavior is unchanged.

## Dependency and rollout

Requires [Engine
#1425](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1425).
Deploy **Engine → claw-interface → Web**. The backend rejects an older
Engine response that lacks the new cursor contract rather than silently
displaying partial history.

No account remigration, transcript/public-event backfill, V1 restart,
Agent Studio change, channel reassignment, automatic unarchive or
synthetic inbound message is included. This PR does not deploy or modify
production data.
```

### PR Body

## Summary

Restore migrated Web conversations in Recent conversations by reusing their original saved titles and filling pages with visible sessions. Manual and generated titles are preserved, Mongo archive state is respected during list/read/select/open, and the original Mattermost thread continues to supply the conversation body.

Use Engine's filtered activity cursor, retaining numeric-page compatibility for older browsers. The frontend consumes opaque cursors and deduplicates overlapping sessions. It also preserves the current empty conversation on direct links and across tabs by using the successful, authorized task read; it does not fabricate a task from a URL or revive cached data after a failed read.

## Root cause

Engine paged before product visibility filtering, and import-time updates pushed old Web sessions behind internal history. ECAP derived titles only from public user events, which migrated Web sessions lack, despite saved Mongo titles and readable Mattermost threads. The UI then hid the titleless sessions.

Independent review also identified that the persisted selected-session pointer can differ from the browser URL. That P2 is fixed and independently re-reviewed with no findings.

## Test plan

- [x] Backend: 112 relevant tests passed, including original titles, archive enforcement, thread aliases, visible-page refill, cursor continuation, numeric compatibility, client/route contracts and encrypted-Mongo query guards.
- [x] Frontend: original 32 related tests passed (two cold-import timeouts passed on an unchanged-file rerun). Final direct-link fix: 18 relevant tests passed, with both new regressions first demonstrated failing.
- [x] Backend static checks: ruff, format, full pyright and 8 import contracts passed.
- [x] Frontend changed-surface type/lint/governance checks passed; commit/push checks run normally.
- [x] Independent cross-repository review and follow-up review of the P2 correction completed.
- [x] Production read-only evidence confirmed saved titles and readable original threads; the bounded Mongo query form was accepted by the deployed encrypted client.
- [ ] After deployment, verify the 15 active migrated Web conversations are discoverable with their original titles and readable bodies, the already-archived conversation remains archived, and ordinary Web/WeCom behavior is unchanged.

## Dependency and rollout

Requires [Engine #1425](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1425). Deploy **Engine → claw-interface → Web**. The backend rejects an older Engine response that lacks the new cursor contract rather than silently displaying partial history.

No account remigration, transcript/public-event backfill, V1 restart, Agent Studio change, channel reassignment, automatic unarchive or synthetic inbound message is included. This PR does not deploy or modify production data.


---

## fix(e2e): mark GA4 test traffic for filtering (#3718)

- **SHA**: `3244305610b1921ca1540f7fccb6366f45948c0a`
- **作者**: winston-srp
- **日期**: 2026-09-14T08:20:45Z
- **PR**: #3718

### Commit Message

```
fix(e2e): mark GA4 test traffic for filtering (#3718)

## Summary
Production browser E2E currently reaches GA4 without a stable test
marker, so ETL cannot reliably exclude anonymous test events. Set
`traffic_type=e2e` before the application's first Google Tag command in
every E2E browser context, including auth setup, shared sessions,
explicit `browser.newContext()` calls and token capture.

The change stays in the test harness. Normal application browsers are
unchanged; after merge, E2E jobs using this revision carry the marker
without a Web/backend release. The tracking specification documents the
field contract. ETL changes belong to a separate repository and are
outside this PR. No production ETL view or GA4 data filter is changed.

## Root cause
A test account UID does not identify anonymous E2E events, and browser
versions are not reliable test identities. The shared browser fixture
installs an init script before returning new contexts, so the marker
also covers contexts that bypass the usual page fixture. It queues an
actual IArguments `set` command without pre-creating `window.gtag`,
configuring GA or changing page/identity fields.

## Test plan
- Passed: `pnpm exec playwright test --project=analytics-marker
--reporter=list` (3 tests: first-page bootstrap ordering and command
format; reload/storage clearing/popup; explicit browser contexts).
- Passed: targeted TypeScript check, ESLint for changed TypeScript
files, formatting and repository governance guards.
- Passed: isolated Chromium experiment using the real Google Tag script;
marked `page_view` (with first-visit/session-start flags) and
`send_message` requests contain `tt=e2e`, while an unmarked context does
not. Every collection request was intercepted locally; no synthetic
events were sent to production.
- Full application type-check was stopped after blocking on local
dependency filesystem reads. Targeted TypeScript and full pre-commit
ESLint passed; CI remains the full-project type-check gate.
- The existing `popup-helper` suite has an unrelated launcher
expectation mismatch in “opens agent chat”; reproduced with its original
upstream fixture import. This PR leaves that test/helper unchanged.

Production BigQuery export will need verification after the first merged
E2E run; historical events cannot acquire this marker retroactively.
```

### PR Body

## Summary
Production browser E2E currently reaches GA4 without a stable test marker, so ETL cannot reliably exclude anonymous test events. Set `traffic_type=e2e` before the application's first Google Tag command in every E2E browser context, including auth setup, shared sessions, explicit `browser.newContext()` calls and token capture.

The change stays in the test harness. Normal application browsers are unchanged; after merge, E2E jobs using this revision carry the marker without a Web/backend release. The tracking specification documents the field contract. ETL changes belong to a separate repository and are outside this PR. No production ETL view or GA4 data filter is changed.

## Root cause
A test account UID does not identify anonymous E2E events, and browser versions are not reliable test identities. The shared browser fixture installs an init script before returning new contexts, so the marker also covers contexts that bypass the usual page fixture. It queues an actual IArguments `set` command without pre-creating `window.gtag`, configuring GA or changing page/identity fields.

## Test plan
- Passed: `pnpm exec playwright test --project=analytics-marker --reporter=list` (3 tests: first-page bootstrap ordering and command format; reload/storage clearing/popup; explicit browser contexts).
- Passed: targeted TypeScript check, ESLint for changed TypeScript files, formatting and repository governance guards.
- Passed: isolated Chromium experiment using the real Google Tag script; marked `page_view` (with first-visit/session-start flags) and `send_message` requests contain `tt=e2e`, while an unmarked context does not. Every collection request was intercepted locally; no synthetic events were sent to production.
- Full application type-check was stopped after blocking on local dependency filesystem reads. Targeted TypeScript and full pre-commit ESLint passed; CI remains the full-project type-check gate.
- The existing `popup-helper` suite has an unrelated launcher expectation mismatch in “opens agent chat”; reproduced with its original upstream fixture import. This PR leaves that test/helper unchanged.

Production BigQuery export will need verification after the first merged E2E run; historical events cannot acquire this marker retroactively.


---

## docs(agents): require audits for payment and subscription operations (#3716)

- **SHA**: `3ccf961e9211e71350584a0797d55cfd29894041`
- **作者**: kaka-srp
- **日期**: 2026-09-14T07:21:25Z
- **PR**: #3716

### Commit Message

```
docs(agents): require audits for payment and subscription operations (#3716)

## Summary

Add a core rule to `AGENTS.md` requiring durable, queryable audit
records for payment and subscription operations, including
offline/manual work through scripts, CLI, direct database changes, and
payment-provider consoles.

The rule defines the required operator, target, reason, before/after
state, outcome, and correlation fields, and preserves linked history for
failures, reversals, and compensating actions. Temporary files, chat
messages, and console output alone do not meet the requirement.

## Test plan

- [x] Reviewed the diff: only the new core audit rule in `AGENTS.md` is
included.
- [x] `git diff --check origin/main...HEAD`
- [x] `bash scripts/verify-changed.sh` — no application surfaces
selected for this documentation-only change.
- [x] Confirmed `CLAUDE.md` continues to use the shared `AGENTS.md`
symlink.
```

### PR Body

## Summary

Add a core rule to `AGENTS.md` requiring durable, queryable audit records for payment and subscription operations, including offline/manual work through scripts, CLI, direct database changes, and payment-provider consoles.

The rule defines the required operator, target, reason, before/after state, outcome, and correlation fields, and preserves linked history for failures, reversals, and compensating actions. Temporary files, chat messages, and console output alone do not meet the requirement.

## Test plan

- [x] Reviewed the diff: only the new core audit rule in `AGENTS.md` is included.
- [x] `git diff --check origin/main...HEAD`
- [x] `bash scripts/verify-changed.sh` — no application surfaces selected for this documentation-only change.
- [x] Confirmed `CLAUDE.md` continues to use the shared `AGENTS.md` symlink.


---

## test(e2e): align chat flows with ZooWork 2.0 session routes (#3712)

- **SHA**: `ecfc8561b9cf299b13561dba0ed35bbe8cbffd41`
- **作者**: rayhuang198212
- **日期**: 2026-09-14T04:05:16Z
- **PR**: #3712

### Commit Message

```
test(e2e): align chat flows with ZooWork 2.0 session routes (#3712)

## Summary

- Support both legacy workspace chat routes and ZooWork 2.0 Agent task
routes when the new-chat launcher submits a prompt.
- Add a shared session-route matcher with coverage for localized routes
and incomplete or invalid URLs.
- Read session titles from the active Agent workspace navigation item
when the editable chat header is unavailable.
- Update the unauthenticated-access assertion to target the current
login form contract.

  ## Motivation

The E2E chat flows still assumed the legacy
`/chat/:workspaceId/sessions/:sessionId` route and header layout.
ZooWork 2.0 can instead navigate to `/agents/:workspaceId?
view=task&session=:sessionId`, causing otherwise valid flows to time out
or return an empty session title.

This change updates the test infrastructure to recognize both supported
UI paths without changing application behavior.
```

### PR Body

## Summary

  - Support both legacy workspace chat routes and ZooWork 2.0 Agent task routes when the new-chat launcher submits a prompt.
  - Add a shared session-route matcher with coverage for localized routes and incomplete or invalid URLs.
  - Read session titles from the active Agent workspace navigation item when the editable chat header is unavailable.
  - Update the unauthenticated-access assertion to target the current login form contract.

  ## Motivation

  The E2E chat flows still assumed the legacy `/chat/:workspaceId/sessions/:sessionId` route and header layout. ZooWork 2.0 can instead navigate to `/agents/:workspaceId?
  view=task&session=:sessionId`, causing otherwise valid flows to time out or return an empty session title.

  This change updates the test infrastructure to recognize both supported UI paths without changing application behavior.

---

## fix(agents): raise all plan install limits to 1000000 (#3714)

- **SHA**: `1452edfb5a796b6ae0282baba0baf1f694d7e71b`
- **作者**: tim-srp
- **日期**: 2026-09-14T04:05:25Z
- **PR**: #3714

### Commit Message

```
fix(agents): raise all plan install limits to 1000000 (#3714)

## Summary

将 Free / Starter / Pro / Ultra 的 Agent 安装数量上限从 10000 统一提高至
1000000，未知套餐仍沿用 Starter 默认值。生产代码仅修改四个映射值，保留全部安装、锁、重试和购买校验逻辑。

同步更新单装、Engine、批量及套餐边界测试。数量检查使用 Python 整数加法与比较，无浮点转换，也不会根据上限预分配资源。

## Validation

- 237 个相关单元测试通过，覆盖 1000000 边界及超限拒绝。
- 提交及推送钩子执行静态、类型与导入检查。
- git diff --check 通过。

仅需后端部署，无数据库迁移。
```

### PR Body

## Summary

将 Free / Starter / Pro / Ultra 的 Agent 安装数量上限从 10000 统一提高至 1000000，未知套餐仍沿用 Starter 默认值。生产代码仅修改四个映射值，保留全部安装、锁、重试和购买校验逻辑。

同步更新单装、Engine、批量及套餐边界测试。数量检查使用 Python 整数加法与比较，无浮点转换，也不会根据上限预分配资源。

## Validation

- 237 个相关单元测试通过，覆盖 1000000 边界及超限拒绝。
- 提交及推送钩子执行静态、类型与导入检查。
- git diff --check 通过。

仅需后端部署，无数据库迁移。


---

## fix(agents): raise all plan install limits to 10000 (#3710)

- **SHA**: `eb501ed1e6df32147b38728c0bf7a135653c827a`
- **作者**: tim-srp
- **日期**: 2026-09-14T03:17:53Z
- **PR**: #3710

### Commit Message

```
fix(agents): raise all plan install limits to 10000 (#3710)

## Summary

将 Free / Starter / Pro / Ultra 的 Agent 安装数量上限统一提高到 10000；未知套餐沿用 Starter
默认值。生产代码仅调整映射表中的四个数值，保留现有安装锁、配额检查、重试和购买校验。

同步更新四个测试文件中的套餐与边界断言，覆盖单装、Engine 安装、批量安装及到期套餐回退。

## Validation

- 237 个相关单元测试通过。
- `bash scripts/verify-py.sh` 通过：Ruff、格式、Pyright、8 个导入契约。
- `git diff --check` 通过。

仅需后端部署，无数据库迁移。
```

### PR Body

## Summary

将 Free / Starter / Pro / Ultra 的 Agent 安装数量上限统一提高到 10000；未知套餐沿用 Starter 默认值。生产代码仅调整映射表中的四个数值，保留现有安装锁、配额检查、重试和购买校验。

同步更新四个测试文件中的套餐与边界断言，覆盖单装、Engine 安装、批量安装及到期套餐回退。

## Validation

- 237 个相关单元测试通过。
- `bash scripts/verify-py.sh` 通过：Ruff、格式、Pyright、8 个导入契约。
- `git diff --check` 通过。

仅需后端部署，无数据库迁移。


---
