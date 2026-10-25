# SerendipityOneInc/ecap-workspace — commits 2026-10-09

## feat(platform): add project webhook management (#4034)

- **SHA**: `1175b107954c359d7dc73a4cac7c7b46da2241f4`
- **作者**: finn-srp
- **日期**: 2026-10-09T12:25:32Z
- **PR**: #4034

### Commit Message

```
feat(platform): add project webhook management (#4034)

Platform users can now manage signed Webhook delivery for the selected
Project through the authenticated claw-interface API.

## Summary
- Add Webhooks navigation and list/detail pages: create paused, edit
event/session scope, test delivery, enable/pause, rotate one-time
secrets, delete, inspect filtered/paged delivery history and redeliver
terminal events.
- Add a browser facade with verified Project tenancy, admin-only writes,
bounded typed input (including server-enforced paused creation), closed
route/method vocabulary, scoped idempotency and no-store responses.
Reuse the route resolver in the existing SDK facade.
- Poll tests by their exact receipt and refresh endpoint/history after
asynchronous test or redelivery completion. Switching Project from
detail returns to the new Project's list before querying the old
endpoint in the new scope.
- Keep signing secrets in transient component state only; clear them on
scope changes and discard late responses. Include preview fixtures,
product/design documentation and behavior regressions.

Related to #3787. [Engine
#1898](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1898),
which provides exact `receipt_id` filtering, is merged and released. The
specific receipt isolation scenario has passed against the deployed
staging Engine; production deployment and production-full-smoke
succeeded for the merge commit. See the review validation below for the
scope of each check. The feature requires both claw-interface and
Platform deployment.

## Validation
- After rebasing to latest main (542b009578), Node 24 Platform lint,
typecheck, all 283 tests and production build passed in the existing
Linux devcontainer with one worker.
- `ecap-verify-py-ci`: all dependency, static, ci-lint, duplication and
full pytest/coverage gates passed against the final rebased
implementation: 12,086 passed, 5 skipped, coverage 89.59% (4 workers,
sysmon, 89.5% threshold).
- Linux backend targeted suites passed 31 Platform tests plus 139
existing SDK Webhook proxy tests.
- User's existing authenticated Chrome → normal BFF → real Account
verification → full local claw-interface → real Engine/PostgreSQL →
public HTTPS receiver: paused creation/test, signed receipt, actual 503
retry, enable/pause, normal/immediate secret rotation, single/batch
redelivery and automatic 302 disablement/recovery passed. Switching from
real detail to the user's newly created Project showed its empty list.
- Regression negative controls reproduced receipt-matching, asynchronous
refresh and Project-switch bugs before their fixes. The create API
regression reproduces the review finding (enabled creation returned
201); the fixed schema rejects it with 400 before contacting Engine,
while a separate update still enables delivery.

## Limits
No production deployment, paid model test or staging CSFLE validation.
Local Billing is unconfigured. Delete/pagination/cross-Project
authorization are automated coverage, not claimed as manual live UI
coverage. The local review endpoint remains paused. Full evidence and
scope are recorded in
`docs/superpowers/specs/2026-10-08-platform-webhooks.md`.


## Receipt review validation — 2026-10-09
- Added two UI regressions for an older successful test remaining in
history while a new receipt is unprojected, then pending or dead. Both
fail when the receipt query is removed and pass with it restored.
- Real staging SDK facade -> deployed Engine -> public HTTPS
signature-verifying receiver: the first test succeeded; a different
receipt received 503 and remained pending; a third received 302 and
became dead/http_3xx. Each filtered page excluded the older success. The
first receipt still returned its original success; a nonexistent receipt
returned an empty page.
- Used a dedicated stopped test Agent and paused Webhook. No sessions,
inference or Sandbox runs. All per-probe resources were deleted;
subsequent listing confirmed no test Agent remained.
- Engine production deployment:
https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/37884096329
. Production-full-smoke:
https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/37885299313
. Both passed for c1318164c0935a656d57784d2bae6956db998c8a; these are
release evidence, not a production run of this receipt regression.
- The real staging probe used the machine-key Agent webhook facade. UI
regressions use MSW. The unmerged Platform browser facade has not been
tested as a deployed browser-to-Engine flow; previous authenticated
browser coverage used the full local stack.

## Enabled endpoint edit review fix — 2026-10-09
- Addressed Tim's P2: edit submissions omit `url` whenever the trimmed
address is unchanged. Creation still requires a URL; paused endpoints
still submit changed URLs. The form callback types distinguish full
creation fields from partial update fields.
- Added seven serialized UI request regressions: description, event
types and session scope edits on enabled and paused endpoints, plus URL
changes while paused. The test API returns Engine's 409 whenever an
enabled endpoint receives `url`, even unchanged. Six cases failed before
the fix; all seven pass after it. The existing creation test now asserts
that the URL is included.
- Preview updates enforce the same enabled-URL rejection, with a
regression for rejection, non-URL edits, pause and URL change. The two
relevant suites passed all 43 tests.
- URL fix originally validated at
f4ee15a709acbb8efca2a8087b45521c6db138a7. All Platform and Python gates
above were rerun after the rebase. This follow-up uses
contract-enforcing local UI tests, not a new live browser/Engine test.


## Empty-204 deletion review fix — 2026-10-09
- Addressed [Tim's deletion
P2](https://github.com/SerendipityOneInc/ecap-workspace/pull/4034#discussion_r4227805104):
browser facade preserves an absent upstream Content-Type instead of
labeling the bodyless Engine 204 as JSON. Existing upstream Content-Type
and no-store behavior remain preserved.
- The Platform API client skips response-body parsing on 204, including
when a proxy retains a JSON header. Successful deletion can therefore
close the dialog, invalidate the endpoint list and navigate back. Other
statuses retain their original parsing/error behavior.
- Negative controls: before the fix, the actual FastAPI route's
headerless-upstream regression failed because it added application/json;
the UI deletion regression with JSON-labelled empty 204 failed to
navigate. Both now pass.
- Targeted validation: 172 backend webhook facade tests and 48
UI/API-client/Worker tests passed. API-client tests assert that no
JSON/text parser is called for either form of empty 204.
- Cross-layer local probe: captured the actual FastAPI TestClient
response to a mocked Engine httpx.Response(204), verified empty body and
absent Content-Type, then consumed those exact response headers/status
through the production Worker handler and webhook API client. Probe
passed. This validates response transport with test
authentication/upstream stubs, not deployed browser-to-Engine deletion.
- Rebased onto main 542b009578. At 197a7f351, all Node 24 Platform gates
and full ecap-verify-py-ci passed with the counts above. No live or
production deletion was performed.
```

### PR Body

Platform users can now manage signed Webhook delivery for the selected Project through the authenticated claw-interface API.

## Summary
- Add Webhooks navigation and list/detail pages: create paused, edit event/session scope, test delivery, enable/pause, rotate one-time secrets, delete, inspect filtered/paged delivery history and redeliver terminal events.
- Add a browser facade with verified Project tenancy, admin-only writes, bounded typed input (including server-enforced paused creation), closed route/method vocabulary, scoped idempotency and no-store responses. Reuse the route resolver in the existing SDK facade.
- Poll tests by their exact receipt and refresh endpoint/history after asynchronous test or redelivery completion. Switching Project from detail returns to the new Project's list before querying the old endpoint in the new scope.
- Keep signing secrets in transient component state only; clear them on scope changes and discard late responses. Include preview fixtures, product/design documentation and behavior regressions.

Related to #3787. [Engine #1898](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1898), which provides exact `receipt_id` filtering, is merged and released. The specific receipt isolation scenario has passed against the deployed staging Engine; production deployment and production-full-smoke succeeded for the merge commit. See the review validation below for the scope of each check. The feature requires both claw-interface and Platform deployment.

## Validation
- After rebasing to latest main (542b009578), Node 24 Platform lint, typecheck, all 283 tests and production build passed in the existing Linux devcontainer with one worker.
- `ecap-verify-py-ci`: all dependency, static, ci-lint, duplication and full pytest/coverage gates passed against the final rebased implementation: 12,086 passed, 5 skipped, coverage 89.59% (4 workers, sysmon, 89.5% threshold).
- Linux backend targeted suites passed 31 Platform tests plus 139 existing SDK Webhook proxy tests.
- User's existing authenticated Chrome → normal BFF → real Account verification → full local claw-interface → real Engine/PostgreSQL → public HTTPS receiver: paused creation/test, signed receipt, actual 503 retry, enable/pause, normal/immediate secret rotation, single/batch redelivery and automatic 302 disablement/recovery passed. Switching from real detail to the user's newly created Project showed its empty list.
- Regression negative controls reproduced receipt-matching, asynchronous refresh and Project-switch bugs before their fixes. The create API regression reproduces the review finding (enabled creation returned 201); the fixed schema rejects it with 400 before contacting Engine, while a separate update still enables delivery.

## Limits
No production deployment, paid model test or staging CSFLE validation. Local Billing is unconfigured. Delete/pagination/cross-Project authorization are automated coverage, not claimed as manual live UI coverage. The local review endpoint remains paused. Full evidence and scope are recorded in `docs/superpowers/specs/2026-10-08-platform-webhooks.md`.


## Receipt review validation — 2026-10-09
- Added two UI regressions for an older successful test remaining in history while a new receipt is unprojected, then pending or dead. Both fail when the receipt query is removed and pass with it restored.
- Real staging SDK facade -> deployed Engine -> public HTTPS signature-verifying receiver: the first test succeeded; a different receipt received 503 and remained pending; a third received 302 and became dead/http_3xx. Each filtered page excluded the older success. The first receipt still returned its original success; a nonexistent receipt returned an empty page.
- Used a dedicated stopped test Agent and paused Webhook. No sessions, inference or Sandbox runs. All per-probe resources were deleted; subsequent listing confirmed no test Agent remained.
- Engine production deployment: https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/37884096329 . Production-full-smoke: https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/37885299313 . Both passed for c1318164c0935a656d57784d2bae6956db998c8a; these are release evidence, not a production run of this receipt regression.
- The real staging probe used the machine-key Agent webhook facade. UI regressions use MSW. The unmerged Platform browser facade has not been tested as a deployed browser-to-Engine flow; previous authenticated browser coverage used the full local stack.

## Enabled endpoint edit review fix — 2026-10-09
- Addressed Tim's P2: edit submissions omit `url` whenever the trimmed address is unchanged. Creation still requires a URL; paused endpoints still submit changed URLs. The form callback types distinguish full creation fields from partial update fields.
- Added seven serialized UI request regressions: description, event types and session scope edits on enabled and paused endpoints, plus URL changes while paused. The test API returns Engine's 409 whenever an enabled endpoint receives `url`, even unchanged. Six cases failed before the fix; all seven pass after it. The existing creation test now asserts that the URL is included.
- Preview updates enforce the same enabled-URL rejection, with a regression for rejection, non-URL edits, pause and URL change. The two relevant suites passed all 43 tests.
- URL fix originally validated at f4ee15a709acbb8efca2a8087b45521c6db138a7. All Platform and Python gates above were rerun after the rebase. This follow-up uses contract-enforcing local UI tests, not a new live browser/Engine test.


## Empty-204 deletion review fix — 2026-10-09
- Addressed [Tim's deletion P2](https://github.com/SerendipityOneInc/ecap-workspace/pull/4034#discussion_r4227805104): browser facade preserves an absent upstream Content-Type instead of labeling the bodyless Engine 204 as JSON. Existing upstream Content-Type and no-store behavior remain preserved.
- The Platform API client skips response-body parsing on 204, including when a proxy retains a JSON header. Successful deletion can therefore close the dialog, invalidate the endpoint list and navigate back. Other statuses retain their original parsing/error behavior.
- Negative controls: before the fix, the actual FastAPI route's headerless-upstream regression failed because it added application/json; the UI deletion regression with JSON-labelled empty 204 failed to navigate. Both now pass.
- Targeted validation: 172 backend webhook facade tests and 48 UI/API-client/Worker tests passed. API-client tests assert that no JSON/text parser is called for either form of empty 204.
- Cross-layer local probe: captured the actual FastAPI TestClient response to a mocked Engine httpx.Response(204), verified empty body and absent Content-Type, then consumed those exact response headers/status through the production Worker handler and webhook API client. Probe passed. This validates response transport with test authentication/upstream stubs, not deployed browser-to-Engine deletion.
- Rebased onto main 542b009578. At 197a7f351, all Node 24 Platform gates and full ecap-verify-py-ci passed with the counts above. No live or production deletion was performed.


---

## feat(agents): allow task-scoped platform model selection (#4039)

- **SHA**: `542b009578d5a95cb4466111b37263250e84ae42`
- **作者**: kaka-srp
- **日期**: 2026-10-09T09:42:47Z
- **PR**: #4039

### Commit Message

```
feat(agents): allow task-scoped platform model selection (#4039)

## Summary

Allow users to choose a platform model for the current Web Task's
subsequent turns while Edit continues to save the Agent default through
a Revision. Task selection is persisted on the canonical Engine Session,
survives refresh, and does not change another Task or the Agent
definition. Choosing the currently checked default explicitly pins that
model for the Task; there is no new reset/default menu item.

Authorize Task access and model entitlement in claw-interface, then
forward Engine's selection/config CAS. Wire existing Task and new-chat
composers to the Task controller. On first send, create the Session,
save the choice, bind the conversation, and only then send; failures
retain the same Session/idempotency key for retry.

Preserve the latest main's model retirement/missing-model sending gates
and read-only inherited Agent Auto, without adding Task Auto or personal
subscription functionality. No iOS change.

## Review and CI follow-up

The first CI Web test run found three older test files still asserting
Revision writes or missing the Task hook seam. Updated those contracts
and verified 114 focused Web tests, including the real composer
selecting a Task draft and passing it on first send without any
Revision/default write. Scoped the launcher Task controller to Engine
Agents and omitted an absent model draft from creation parameters.
Corrected the design error table to the existing public `400
agent.model_unavailable` and `409 agent_session.task_model_changed`; 18
backend Task model tests include actual FastAPI/shared-handler HTTP
assertions for missing, withdrawn, and ambiguous catalog models. Both
review agents completed a targeted re-review with no new actionable
findings.

## Dependencies and rollout

Depends on [zooclaw-engine
#1921](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1921).
Deploy its controld and all relevant workers first, then deploy this
backend and Web together. No new migration or Vault setting is needed.
Do not roll the workers back while stored Task selections still require
the new runtime behavior.

## Test plan

- [x] Web Task hook, first-send orchestration, Revision/composer
regression suites: 95 tests passed.
- [x] Backend Task/default-model/retirement metadata suites: 102 tests
passed.
- [x] Web CI guards, tsc, ESLint and import boundaries passed; Python
ruff/format, pyright and import-linter passed.
- [x] Real local Next.js/FastAPI against staging CSFLE plus shared
zooclaw-dev ACS/Engine and real LiteLLM: existing Task switch/refresh;
selected model on first send; checked-default pinning after Edit changes
the default; unaffected Task follows the new default; an in-progress
reply stays on its original model and the next turn changes; first-save
failure sends nothing and retry reuses the Session without duplicate
chat messages; 403/409 leave selection unchanged. Actual Engine records
verified Anthropic/Responses model execution and visible replies.
- [x] Two review agents completed review and targeted re-review.
Confirmed dependency-boundary and retirement integration findings were
fixed. Removing Task model guards makes the retirement/withdrawal tests
fail; restoring them returns the suite to green.
- [x] Test resources were independent and cleaned through the existing
flows. Engine adds real PostgreSQL contention tests and `/new`
regression coverage in its companion PR.
- [ ] CI and deployed staging acceptance remain separate from these
local results. Personal subscription operations, every catalog model,
and image/very-long-context execution were not claimed as live coverage.

Design and validation details:
`docs/superpowers/specs/2026-10-09-agent-task-platform-model-override.md`.

Lifecycle clarification: Engine follows its existing model-lifecycle
contract. Expiry blocks new selections; existing Task choices/default
references continue during drain until formal retirement. This does not
introduce automatic substitution. The companion Engine PR adds
execution/projection/admission regression coverage for that distinction.

Draining same-choice retry now passes the public entitlement/catalog
layer only when Engine reports that exact explicit choice as available
and writable. New references, retired/unavailable/read-only choices and
ambiguous aliases remain rejected; expected versions are still passed
unchanged for authoritative Engine CAS. Six additional tests cover
retention/rejection and stale-CAS behavior; Task model plus
route-boundary suites pass 63 tests.
```

### PR Body

## Summary

Allow users to choose a platform model for the current Web Task's subsequent turns while Edit continues to save the Agent default through a Revision. Task selection is persisted on the canonical Engine Session, survives refresh, and does not change another Task or the Agent definition. Choosing the currently checked default explicitly pins that model for the Task; there is no new reset/default menu item.

Authorize Task access and model entitlement in claw-interface, then forward Engine's selection/config CAS. Wire existing Task and new-chat composers to the Task controller. On first send, create the Session, save the choice, bind the conversation, and only then send; failures retain the same Session/idempotency key for retry.

Preserve the latest main's model retirement/missing-model sending gates and read-only inherited Agent Auto, without adding Task Auto or personal subscription functionality. No iOS change.

## Review and CI follow-up

The first CI Web test run found three older test files still asserting Revision writes or missing the Task hook seam. Updated those contracts and verified 114 focused Web tests, including the real composer selecting a Task draft and passing it on first send without any Revision/default write. Scoped the launcher Task controller to Engine Agents and omitted an absent model draft from creation parameters. Corrected the design error table to the existing public `400 agent.model_unavailable` and `409 agent_session.task_model_changed`; 18 backend Task model tests include actual FastAPI/shared-handler HTTP assertions for missing, withdrawn, and ambiguous catalog models. Both review agents completed a targeted re-review with no new actionable findings.

## Dependencies and rollout

Depends on [zooclaw-engine #1921](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1921). Deploy its controld and all relevant workers first, then deploy this backend and Web together. No new migration or Vault setting is needed. Do not roll the workers back while stored Task selections still require the new runtime behavior.

## Test plan

- [x] Web Task hook, first-send orchestration, Revision/composer regression suites: 95 tests passed.
- [x] Backend Task/default-model/retirement metadata suites: 102 tests passed.
- [x] Web CI guards, tsc, ESLint and import boundaries passed; Python ruff/format, pyright and import-linter passed.
- [x] Real local Next.js/FastAPI against staging CSFLE plus shared zooclaw-dev ACS/Engine and real LiteLLM: existing Task switch/refresh; selected model on first send; checked-default pinning after Edit changes the default; unaffected Task follows the new default; an in-progress reply stays on its original model and the next turn changes; first-save failure sends nothing and retry reuses the Session without duplicate chat messages; 403/409 leave selection unchanged. Actual Engine records verified Anthropic/Responses model execution and visible replies.
- [x] Two review agents completed review and targeted re-review. Confirmed dependency-boundary and retirement integration findings were fixed. Removing Task model guards makes the retirement/withdrawal tests fail; restoring them returns the suite to green.
- [x] Test resources were independent and cleaned through the existing flows. Engine adds real PostgreSQL contention tests and `/new` regression coverage in its companion PR.
- [ ] CI and deployed staging acceptance remain separate from these local results. Personal subscription operations, every catalog model, and image/very-long-context execution were not claimed as live coverage.

Design and validation details: `docs/superpowers/specs/2026-10-09-agent-task-platform-model-override.md`.

Lifecycle clarification: Engine follows its existing model-lifecycle contract. Expiry blocks new selections; existing Task choices/default references continue during drain until formal retirement. This does not introduce automatic substitution. The companion Engine PR adds execution/projection/admission regression coverage for that distinction.

Draining same-choice retry now passes the public entitlement/catalog layer only when Engine reports that exact explicit choice as available and writable. New references, retired/unavailable/read-only choices and ambiguous aliases remain rejected; expected versions are still passed unchanged for authoritative Engine CAS. Six additional tests cover retention/rejection and stale-CAS behavior; Task model plus route-boundary suites pass 63 tests.


---

## feat(landing): add ZooWork Product Hunt award badge (#4031)

- **SHA**: `da4c7efdd9e0b81ea62bed11b1b6f453d5ef90f6`
- **作者**: shana-srp
- **日期**: 2026-10-09T08:21:27Z
- **PR**: #4031

### Commit Message

```
feat(landing): add ZooWork Product Hunt award badge (#4031)

## Summary
- Show ZooWork's official #1 Product of the Day badge above the homepage
headline, left-aligned with 24px spacing, and beneath the footer brand
description.
- Link both badges and the footer Product Hunt icon to
https://www.producthunt.com/products/zoowork/awards. Use the verified
ZooWork launch ID (1259794) and the official SVG, with accessible image
text and visible keyboard focus.
- Use existing hero whitespace and responsive sizing to preserve the
headline position and avoid overflow.

## Test plan
- [x] Homepage unit tests: 64 passed.
- [x] Footer / marketing chrome tests: 34 passed.
- [x] Final `verify-web.sh --no-test` passed: governance guards,
TypeScript, and targeted ESLint. Formatting and pre-commit full ESLint
also passed.
- [x] CI-equivalent Next.js compile build passed.
- [x] Browser verification at 1440px and 390px: official SVG loads,
badge aligns with the headline, and there is no horizontal overflow.
- Full production build compiles, but prerendering fails because local
Firebase configuration is missing.

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

## Summary
- Show ZooWork's official #1 Product of the Day badge above the homepage headline, left-aligned with 24px spacing, and beneath the footer brand description.
- Link both badges and the footer Product Hunt icon to https://www.producthunt.com/products/zoowork/awards. Use the verified ZooWork launch ID (1259794) and the official SVG, with accessible image text and visible keyboard focus.
- Use existing hero whitespace and responsive sizing to preserve the headline position and avoid overflow.

## Test plan
- [x] Homepage unit tests: 64 passed.
- [x] Footer / marketing chrome tests: 34 passed.
- [x] Final `verify-web.sh --no-test` passed: governance guards, TypeScript, and targeted ESLint. Formatting and pre-commit full ESLint also passed.
- [x] CI-equivalent Next.js compile build passed.
- [x] Browser verification at 1440px and 390px: official SVG loads, badge aligns with the headline, and there is no horizontal overflow.
- Full production build compiles, but prerendering fails because local Firebase configuration is missing.


---

## feat(models): add picker display tiers and web model retirement replacement (#4037)

- **SHA**: `1638b8a7df0b56282e1662a0b9455f39ab59f7f8`
- **作者**: tim-srp
- **日期**: 2026-10-09T07:34:41Z
- **PR**: #4037

### Commit Message

```
feat(models): add picker display tiers and web model retirement replacement (#4037)

## Linear
None linked.

## Summary
This PR ships two features. Design spec:
`docs/superpowers/specs/2026-10-08-model-display-tiers-and-retirement.md`.

### 1. Model picker display tiers
- **Backend (`claw-interface`).** The backend reads LiteLLM
`model_info.display_tier` and returns it on `/models`.
- Only the integers `1` and `2` are accepted. `bool`, numeric strings
and floats are logged and ignored.
  - The default is `1`, including when metadata is unavailable.
- Across deployments, an unspecified tier is ignored. Conflicting
explicit tiers log a warning and fall back to `1`.
  - Regional display-name overrides keep the tier.
  - The existing 300-second metadata cache is reused.
- **Shared `ModelPicker` (`@zooclaw/chat-ui`).**
- Eight primary rows, including the selected model. The selected model
stays primary even when it is tier 2, unavailable or retired, and it is
never made selectable again.
- Tier-2 and overflow models sit under a collapsed **More models** row.
  - Search covers the full catalog.
  - Copy is localized in en and zh.
- Entitlements, order, pricing, the default model and the saved Agent
model are unchanged.
- **Rollout note:** every catalog with more than eight models gets the
**More models** row and search as soon as this ships, even before any
tier is assigned.

### 2. Model retirement: web app experience only
- **Contract.** `/models` and `GET /agents/{workspace_id}/model` gain an
optional `retirement_at` field (UTC Unix seconds). The Agent model read
carries the deadline even after the model has left the selectable
catalog; the model label still comes from the catalog `display_name` or
the model-ID label.
- **Deadline mapping.** `retirement_at` is copied only from Engine
`expired_at`.
- In Engine, `expired_at` is the **admission cutoff** for new
selections. It does not stop execution.
  - Engine `retired_at` is never in the future, so it is not used.
- An unselectable model, a model absent from Engine, or a failed catalog
request never produces a deadline.
- The Agent model read is Engine-only (FastClaw V1 was removed on main
in #4028). `/models` without `runtime=engine` never reads Engine
lifecycle and has no `retirement_at`.
- **Before the deadline.** A dismissible notice appears directly above
the composer. It shows the deadline in the user's timezone with a
timezone label, and offers **Change model** (nothing preselected) and
**Dismiss**.
- It is shown at most once per rolling 24 hours, measured from when it
is displayed.
- The 24-hour limit is shared per user, model and deadline, so it holds
across refreshes, revisits and other Agents.
- A rescheduled deadline is a new notice. A cancelled deadline removes
it.
  - An open conversation never gets the notice re-inserted.
- **From the deadline.** The existing unavailable-model dialog is reused
as a required replacement.
- It opens on entry, when the deadline passes while the chat is open,
and on any send attempt. Notice suppression does not delay it.
- It has no Later or close button, and Escape and backdrop clicks are
ignored. **Back to chats** leads to `/tasks`.
- It offers only selectable, concrete, eligible models that are not the
current one, in API order, with nothing preselected or recommended.
  - The draft and history are kept.
- A failed save keeps the selected replacement, shows an inline error
and reloads the options. A chosen model that disappears from the options
is rejected.
- The dialog closes only once the Agent's model really is the
replacement. Revision controllers stay blocked until the new Revision is
active, and the computer restart flow is unchanged.
- Users who cannot change the model see a short explanation and no
confirm button.
  - A catalog load failure shows a retryable error.
- **Recommendation and preselection removed.**
- The existing missing-model dialog no longer preselects the catalog
default.
- The picker lifecycle text no longer names `expired_fallback_to` as a
"planned replacement".

### Post-PR review fixes (commit `95738ffdd`)
- **Optional change never reopens by itself.** The **Change model**
request is tied to the Agent, model and deadline it was made for. It is
cleared as soon as the dialog leaves `change` mode, for example when the
deadline passes, the missing-model prompt or billing takes over, or the
model or Agent changes.
- **A failed background refetch does not lift a known retired gate.**
TanStack keeps the last data when a refetch fails, so a deadline already
read for this Agent model stays in force.
  - A first read that fails still invents nothing.
- A later successful read with no deadline lifts the gate, so a
cancelled schedule is honoured.
- While the read is failing, a user who cannot change the model sees a
retryable load error instead of "ask an administrator".
- **App locale.** Picker lifecycle dates use the app locale in the
composer and Agent Settings, matching the notice.
- **Launcher Revision activation recovery.**
- Before this fix, a failed apply left the definition `pending`
indefinitely, with only **Back to chats**.
- The `activating` dialog now shows an inline error and **Retry**. Retry
replays the original idempotent save, or, after a reload, re-applies the
working Revision through the existing settings commit without
operations.
- Retry is not treated as activation: sending stays blocked until the
definition reports the Revision active.
  - Engine is unchanged.
- **Notice buttons.** These now have `type="button"`, so they cannot
submit the surrounding composer form. A regression spec covers this.

### Final review follow-ups
- Long retirement deadlines now schedule bounded timer wake-ups and
re-arm until the exact deadline; fake-clock tests cover a 30-day
deadline, cancellation, rescheduling and unmount cleanup. No early
retirement and send-time guard unchanged.
- Removed the unused helper export flagged by knip.
- (Superseded) An earlier session-reset test typing fix is no longer in
this PR: main #4028 deleted that V1 test file and the merge accepted the
deletion.

### Merge of origin/main (`c27748263`)
- Merged `7cb5df1dd` (#4028, FastClaw V1 removal). Conflicts:
`agent_model_service.py` kept main's Engine-only read and re-applied
only `retirement_at`; `test_openclaw_settings_routes.py` deletion
accepted. No V1 code, no `model_display_name`, no Engine edits.

### Scope reduction
- Removed the newly added `model_display_name` from the Agent model read
(schema, backend population, frontend type/query/composer, mock, tests,
spec). The retirement label uses the existing catalog `display_name`,
then the existing model-ID label. `retirement_at` is unchanged. No
replacement field.

### What this PR does not do
- **The required replacement is enforced only in the web composer.**
Engine, ACS/IM channels, the public API, schedules, ACP and WhatsApp are
**not** blocked; Engine keeps running an Agent whose model passed
`expired_at`.
- **No Engine changes** and no cross-repository changes. Engine
lifecycle semantics, the operator migration to `expired_fallback_to` and
the Auto/inherited fallbacks are unchanged.
- No deployment, no production tier assignment and no data analysis.

## Test plan
- [x] Final CI-like full web coverage on Node 24: **885 files, 11,195
passed, 0 failed**. Timer regression asserts only hook-owned
wakeups/cleanup rather than framework-global fake-timer counts; the
pre-fix hook still fails both new cases.
- [x] Backend `bash scripts/verify-py.sh`: ruff, ruff format, pyright
and import-linter all pass. The `scripts/ci-lint` guards (01–07) also
pass.
- [x] Backend pytest, model-related files
(`test_model_retirement_deadline`, `test_model_catalog_display_tier`,
`test_model_catalog`, `test_agent_model_service`,
`test_agent_model_routes`, `test_agent_builder_test_model_service`,
`test_model_retirement`, `test_model_retirement_recovery`,
`test_agent_model_environment_isolation`): 128 passed. The full backend
suite was not run locally; it runs in CI.
- [x] Web `vitest run`, full suite at `95738ffdd`: 884 files, 11191
passed, 70 skipped, 1 todo. (It was 11183 at `a34d970ec`.)
- [x] Post-review mutation checks. Each fix, when reverted on its own,
makes its new tests fail:
  - the change-flag scope: 2 tests;
  - the stale-known gate: 1 test;
  - the locale: 1 test;
  - the activation Retry: 1 test.
- [x] `@zooclaw/chat-ui` vitest: 523 passed.
- [x] Web `tsc`, eslint, governance guards, `pnpm lint:ci`
(dependency-cruiser, knip) and `pnpm dup`: all pass.
- [x] Mutation check: making the retirement send gate always allow
causes 5 of the new tests to fail.
- [x] Long-deadline hook tests: 11 passed, including 2 new regressions
that fail on old code; lint and TypeScript passed.
- [x] ~~Pydantic typing compatibility~~: superseded; those session-reset
tests were deleted on main (#4028). Post-merge pyright is covered below.
- [x] Mock backend: `MOCK_MODEL_RETIREMENT=upcoming|retired`. `/models`
and the Agent model read return `retirement_at` (checked with curl).
- [x] **Local browser walkthrough (mock only): 66/66 assertions passed,
zero page errors.** Picker/upcoming/deadline-crossing 33; retired 16;
notice-button/draft/stability supplement 17. Change/Dismiss generate no
message or conversation POST and preserve the draft; no replacement
preselection; Escape/backdrop cannot bypass the retired dialog. Reminder
stayed visible in all 40 samples over 20 seconds without a rebuild, and
refresh suppression passed. The Firebase blocker was resolved with
temporary worktree-only placeholder env; the original symlink was
restored and owned servers stopped. Shared root env was untouched. This
does not verify real Engine activation. Main runs used `95738ffdd`;
later runs included only the unused-export removal subsequently
committed as `d1dc95480`.
- [x] After removing `model_display_name` (`febff8f02`): `verify-py`
passes; backend model/agent-model pytest 52 + 403 passed; `verify-web`
(guards, tsc, eslint) and vitest on composer/agent/revision-model
suites, 116 files, 1271 tests passed. Earlier full-suite and browser
results above predate this commit.
- [x] After merging origin/main (`c27748263`): `verify-py` (ruff, ruff
format, pyright `app/ tests/`, import-linter 8/8) passed; pytest on
`test_agent_model_service`, `test_model_retirement_deadline`,
`test_model_catalog`, `test_model_catalog_display_tier`,
`test_agent_model_routes`: 84 passed; `verify-web` on
composer/agent/revision-model suites: 116 files, 1271 tests passed; CI
on `c27748263`: 41/41 non-skipped checks passed. Full backend pytest,
full web suite and browser checks were not re-run after the merge. The
follow-up spec commit `b81193599` is documentation-only.
- [ ] **Not verified: staging.** Not exercised against a real Engine
catalog with a scheduled `expired_at`.
- [ ] E2E helper (`composer-picker-controls.ts`): earlier typecheck,
lint and `--list` checks passed. The specs were not run here, against
production or staging.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

## Linear
None linked.

## Summary
This PR ships two features. Design spec: `docs/superpowers/specs/2026-10-08-model-display-tiers-and-retirement.md`.

### 1. Model picker display tiers
- **Backend (`claw-interface`).** The backend reads LiteLLM `model_info.display_tier` and returns it on `/models`.
  - Only the integers `1` and `2` are accepted. `bool`, numeric strings and floats are logged and ignored.
  - The default is `1`, including when metadata is unavailable.
  - Across deployments, an unspecified tier is ignored. Conflicting explicit tiers log a warning and fall back to `1`.
  - Regional display-name overrides keep the tier.
  - The existing 300-second metadata cache is reused.
- **Shared `ModelPicker` (`@zooclaw/chat-ui`).**
  - Eight primary rows, including the selected model. The selected model stays primary even when it is tier 2, unavailable or retired, and it is never made selectable again.
  - Tier-2 and overflow models sit under a collapsed **More models** row.
  - Search covers the full catalog.
  - Copy is localized in en and zh.
- Entitlements, order, pricing, the default model and the saved Agent model are unchanged.
- **Rollout note:** every catalog with more than eight models gets the **More models** row and search as soon as this ships, even before any tier is assigned.

### 2. Model retirement: web app experience only
- **Contract.** `/models` and `GET /agents/{workspace_id}/model` gain an optional `retirement_at` field (UTC Unix seconds). The Agent model read carries the deadline even after the model has left the selectable catalog; the model label still comes from the catalog `display_name` or the model-ID label.
- **Deadline mapping.** `retirement_at` is copied only from Engine `expired_at`.
  - In Engine, `expired_at` is the **admission cutoff** for new selections. It does not stop execution.
  - Engine `retired_at` is never in the future, so it is not used.
  - An unselectable model, a model absent from Engine, or a failed catalog request never produces a deadline.
  - The Agent model read is Engine-only (FastClaw V1 was removed on main in #4028). `/models` without `runtime=engine` never reads Engine lifecycle and has no `retirement_at`.
- **Before the deadline.** A dismissible notice appears directly above the composer. It shows the deadline in the user's timezone with a timezone label, and offers **Change model** (nothing preselected) and **Dismiss**.
  - It is shown at most once per rolling 24 hours, measured from when it is displayed.
  - The 24-hour limit is shared per user, model and deadline, so it holds across refreshes, revisits and other Agents.
  - A rescheduled deadline is a new notice. A cancelled deadline removes it.
  - An open conversation never gets the notice re-inserted.
- **From the deadline.** The existing unavailable-model dialog is reused as a required replacement.
  - It opens on entry, when the deadline passes while the chat is open, and on any send attempt. Notice suppression does not delay it.
  - It has no Later or close button, and Escape and backdrop clicks are ignored. **Back to chats** leads to `/tasks`.
  - It offers only selectable, concrete, eligible models that are not the current one, in API order, with nothing preselected or recommended.
  - The draft and history are kept.
  - A failed save keeps the selected replacement, shows an inline error and reloads the options. A chosen model that disappears from the options is rejected.
  - The dialog closes only once the Agent's model really is the replacement. Revision controllers stay blocked until the new Revision is active, and the computer restart flow is unchanged.
  - Users who cannot change the model see a short explanation and no confirm button.
  - A catalog load failure shows a retryable error.
- **Recommendation and preselection removed.**
  - The existing missing-model dialog no longer preselects the catalog default.
  - The picker lifecycle text no longer names `expired_fallback_to` as a "planned replacement".

### Post-PR review fixes (commit `95738ffdd`)
- **Optional change never reopens by itself.** The **Change model** request is tied to the Agent, model and deadline it was made for. It is cleared as soon as the dialog leaves `change` mode, for example when the deadline passes, the missing-model prompt or billing takes over, or the model or Agent changes.
- **A failed background refetch does not lift a known retired gate.** TanStack keeps the last data when a refetch fails, so a deadline already read for this Agent model stays in force.
  - A first read that fails still invents nothing.
  - A later successful read with no deadline lifts the gate, so a cancelled schedule is honoured.
  - While the read is failing, a user who cannot change the model sees a retryable load error instead of "ask an administrator".
- **App locale.** Picker lifecycle dates use the app locale in the composer and Agent Settings, matching the notice.
- **Launcher Revision activation recovery.**
  - Before this fix, a failed apply left the definition `pending` indefinitely, with only **Back to chats**.
  - The `activating` dialog now shows an inline error and **Retry**. Retry replays the original idempotent save, or, after a reload, re-applies the working Revision through the existing settings commit without operations.
  - Retry is not treated as activation: sending stays blocked until the definition reports the Revision active.
  - Engine is unchanged.
- **Notice buttons.** These now have `type="button"`, so they cannot submit the surrounding composer form. A regression spec covers this.

### Final review follow-ups
- Long retirement deadlines now schedule bounded timer wake-ups and re-arm until the exact deadline; fake-clock tests cover a 30-day deadline, cancellation, rescheduling and unmount cleanup. No early retirement and send-time guard unchanged.
- Removed the unused helper export flagged by knip.
- (Superseded) An earlier session-reset test typing fix is no longer in this PR: main #4028 deleted that V1 test file and the merge accepted the deletion.

### Merge of origin/main (`c27748263`)
- Merged `7cb5df1dd` (#4028, FastClaw V1 removal). Conflicts: `agent_model_service.py` kept main's Engine-only read and re-applied only `retirement_at`; `test_openclaw_settings_routes.py` deletion accepted. No V1 code, no `model_display_name`, no Engine edits.

### Scope reduction
- Removed the newly added `model_display_name` from the Agent model read (schema, backend population, frontend type/query/composer, mock, tests, spec). The retirement label uses the existing catalog `display_name`, then the existing model-ID label. `retirement_at` is unchanged. No replacement field.

### What this PR does not do
- **The required replacement is enforced only in the web composer.** Engine, ACS/IM channels, the public API, schedules, ACP and WhatsApp are **not** blocked; Engine keeps running an Agent whose model passed `expired_at`.
- **No Engine changes** and no cross-repository changes. Engine lifecycle semantics, the operator migration to `expired_fallback_to` and the Auto/inherited fallbacks are unchanged.
- No deployment, no production tier assignment and no data analysis.

## Test plan
- [x] Final CI-like full web coverage on Node 24: **885 files, 11,195 passed, 0 failed**. Timer regression asserts only hook-owned wakeups/cleanup rather than framework-global fake-timer counts; the pre-fix hook still fails both new cases.
- [x] Backend `bash scripts/verify-py.sh`: ruff, ruff format, pyright and import-linter all pass. The `scripts/ci-lint` guards (01–07) also pass.
- [x] Backend pytest, model-related files (`test_model_retirement_deadline`, `test_model_catalog_display_tier`, `test_model_catalog`, `test_agent_model_service`, `test_agent_model_routes`, `test_agent_builder_test_model_service`, `test_model_retirement`, `test_model_retirement_recovery`, `test_agent_model_environment_isolation`): 128 passed. The full backend suite was not run locally; it runs in CI.
- [x] Web `vitest run`, full suite at `95738ffdd`: 884 files, 11191 passed, 70 skipped, 1 todo. (It was 11183 at `a34d970ec`.)
- [x] Post-review mutation checks. Each fix, when reverted on its own, makes its new tests fail:
  - the change-flag scope: 2 tests;
  - the stale-known gate: 1 test;
  - the locale: 1 test;
  - the activation Retry: 1 test.
- [x] `@zooclaw/chat-ui` vitest: 523 passed.
- [x] Web `tsc`, eslint, governance guards, `pnpm lint:ci` (dependency-cruiser, knip) and `pnpm dup`: all pass.
- [x] Mutation check: making the retirement send gate always allow causes 5 of the new tests to fail.
- [x] Long-deadline hook tests: 11 passed, including 2 new regressions that fail on old code; lint and TypeScript passed.
- [x] ~~Pydantic typing compatibility~~: superseded; those session-reset tests were deleted on main (#4028). Post-merge pyright is covered below.
- [x] Mock backend: `MOCK_MODEL_RETIREMENT=upcoming|retired`. `/models` and the Agent model read return `retirement_at` (checked with curl).
- [x] **Local browser walkthrough (mock only): 66/66 assertions passed, zero page errors.** Picker/upcoming/deadline-crossing 33; retired 16; notice-button/draft/stability supplement 17. Change/Dismiss generate no message or conversation POST and preserve the draft; no replacement preselection; Escape/backdrop cannot bypass the retired dialog. Reminder stayed visible in all 40 samples over 20 seconds without a rebuild, and refresh suppression passed. The Firebase blocker was resolved with temporary worktree-only placeholder env; the original symlink was restored and owned servers stopped. Shared root env was untouched. This does not verify real Engine activation. Main runs used `95738ffdd`; later runs included only the unused-export removal subsequently committed as `d1dc95480`.
- [x] After removing `model_display_name` (`febff8f02`): `verify-py` passes; backend model/agent-model pytest 52 + 403 passed; `verify-web` (guards, tsc, eslint) and vitest on composer/agent/revision-model suites, 116 files, 1271 tests passed. Earlier full-suite and browser results above predate this commit.
- [x] After merging origin/main (`c27748263`): `verify-py` (ruff, ruff format, pyright `app/ tests/`, import-linter 8/8) passed; pytest on `test_agent_model_service`, `test_model_retirement_deadline`, `test_model_catalog`, `test_model_catalog_display_tier`, `test_agent_model_routes`: 84 passed; `verify-web` on composer/agent/revision-model suites: 116 files, 1271 tests passed; CI on `c27748263`: 41/41 non-skipped checks passed. Full backend pytest, full web suite and browser checks were not re-run after the merge. The follow-up spec commit `b81193599` is documentation-only.
- [ ] **Not verified: staging.** Not exercised against a real Engine catalog with a scheduled `expired_at`.
- [ ] E2E helper (`composer-picker-controls.ts`): earlier typecheck, lint and `--list` checks passed. The specs were not run here, against production or staging.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## refactor(integrations): remove retired Nango integration code (#4035)

- **SHA**: `9d6e56de2b282f8c14babf0018ac3da8a5fd0e5b`
- **作者**: tim-srp
- **日期**: 2026-10-09T06:56:35Z
- **PR**: #4035

### Commit Message

```
refactor(integrations): remove retired Nango integration code (#4035)

## Summary
- Removes the legacy Nango integration code from `web/app` and
`claw-interface`. The plugin page and chat Connector dialogs already use
Composio. A repository reference search found no remaining caller of the
removed frontend modules.
- Frontend (6 files + 4 dedicated specs): `services/integrations.ts`,
`models/integration.ts`, `hooks/useIntegrations.ts`,
`hooks/queries/integrations/{useIntegrationsQuery,keys}.ts`, and
`claw-settings/components/IntegrationsSection.tsx`.
- Backend (4 files + 6 dedicated unit/BDD tests): the
`/openclaw/integrations/*` router (connect, list, disconnect, enable,
disable, and `POST webhooks/nango`), `services/integration_provider.py`
(the Nango client), `database/integration_repo.py`, and
`schema/integration.py`.
- Also removes the router registration, the
`INTEGRATION_CONNECTION_COLLECTION` code constant, and three
import-linter entries. The live collection and its data are untouched.
- Removes the `AppSettings` fields `NANGO_GATEWAY_URL`,
`NANGO_SERVER_URL`, `NANGO_PUBLIC_URL`, `NANGO_SECRET_KEY`,
`NANGO_WEBHOOK_SECRET` and `INTEGRATION_CREDITS_PER_CALL`, plus the
`NANGO_SERVER_URL` validator.
- `AppSettings` uses `extra="ignore"`. A new test checks that leftover
`NANGO_*` env vars, including a value the old validator rejected, do not
break settings construction.
- This removes code-side settings only. It does not change Vault or any
deployed Secret (see "Configuration follow-through").
- Removes the `NANGO_GATEWAY_URL` bot-env injection in
`services/openclaw/bot_config.py::build_deployment_env` and
`services/openclaw_client/_bot_lifecycle.py::create_bot`.
- Both sites are already unreachable in production code. Every caller
first calls `get_openclaw_client()`, which has unconditionally raised
`NotFoundError(code="agent.runtime_retired")` since #3874 retired
FastClaw V1
(`services/claw-interface/app/services/openclaw_client/__init__.py:47-49`).
- This affects only retired V1 code. No V1 or FastClaw path is
re-enabled.
- **Unchanged:**
- Composio routes and settings (`ECAP_PROXY_SERVICE_URL`) and the shared
`ProviderLogo`;
  - `USER_INTERNAL_TOKEN` / `CLAW_INTERFACE_URL`;
  - V2 Engine installation and credential services;
  - auth, billing, and Python/npm dependencies;
  - historical Nango credentials and data, and runtime configuration.
- **Docs:**
- `architecture.md` and `architecture.zh-CN.md` now describe the
Composio connector path and mark the proxy's Nango `/integrations/*`
routes as retiring separately in that repository.
- The README and AGENTS dependency lists and the `web/app/AGENTS.md`
React Query reference are updated.
- The 2026-05-25 Composio spec gets a dated note. Archives are
unchanged.

## Owner decision and scope (reported, not newly measured)
- The owner decision is **reported** in tim-srp's [independent review
comment](https://github.com/SerendipityOneInc/ecap-workspace/pull/4035#issuecomment-6059076512):
this cleanup may assume legacy Nango has no remaining users or calls,
and historical connection owners should move to the Composio Connector.
This PR relies on that reported decision. It was not personally verified
as an owner instruction.
- This changes the accepted risk premise, not the evidence. **No new
zero-traffic observation was made, and the Nango callback configuration
was not inspected.** Earlier audit records (for example the 2026-10-08
snapshot of 0 claw-interface legacy requests over 30 days) remain
historical snapshots.
- Removing `POST /openclaw/integrations/webhooks/nango` and the legacy
management APIs is intended. After deployment those paths return 404,
and no compatibility endpoint or Nango restoration is planned. Any
remaining callback configuration is to be disabled during the separate
Nango shutdown; not performed here.

## Related work (context only)
- SerendipityOneInc/ecap-skills#292 (removes the `zooclaw-connectors`
skill source) was merged on 2026-10-08T09:47:38Z at head
`4e369eea4c139803b8ae0f2c0ffc8de99109dfaf`. This shows the source is
gone, not that previously installed copies are gone.
- This PR does not change `ecap-proxy-service`, `gcp-foundation`,
`openclaw-docker` or `ecap-agent-pack`. Proxy route removal is handled
in its own repository. The same comment reports the proxy G1 caller gate
as closed by that decision; it was not closed by new traffic evidence.

## Before merge (merging to `main` auto-deploys staging)
- [x] Required CI checks pass on the current head
`28ec64614e5088e87e867077da5fe8cfabed840e`. All required contexts
(`code-quality`, `size / size-check`, `auto-review / auto-review`) are
SUCCESS, and the commit's raw `statusCheckRollup` is SUCCESS (29
succeeded, 21 skipped, 0 failed). The superseded FAILURE runs from the
label-less `opened` event belong to the previous head `8e43283d2` and
remain there as history. Re-confirm if the head changes again.
- [ ] The PR is currently a draft with no approval. Before merge, a
human reviewer marks it ready for review and approves it (the ruleset
requires 1 approval and resolved review threads). This update does not
change the draft status or record an approval.
- [ ] Rollout preparation: whoever runs the staging deploy has the
acceptance checklist below.

## Post-merge staging acceptance (current business; required before any
production release)
- [ ] Composio: provider list, connect, real OAuth callback, enable,
disable, disconnect, and a real tool execution.
- [ ] V2 agent installation and start, including Engine credentials, and
config update.
- [ ] Shared authentication, billing, and proxy features (for example
YouTube and search) still work.
- [ ] claw-interface error rates and logs show no new errors on
supported paths. `/openclaw/integrations/*` returning 404 is expected,
and legacy requests alone do not trigger rollback; regressions in
supported current functionality do.
- [ ] Production is a separate, explicit release step (manual release
tag).

**Retired-V1 gates removed.** Earlier drafts listed two items that would
require V1:
- verifying `NANGO_GATEWAY_URL` on newly created or recreated FastClaw
computers;
- FastClaw env merge semantics.

Both are obsolete because V1 is retired in code (see Summary). Do not
re-enable V1 or create/recreate a FastClaw computer to test this.
`openclaw-docker` and `ecap-agent-pack` remain out of scope.

## Configuration follow-through (separate change, per environment after
code rollout)
- Deleting settings does not remove live Vault keys.
`services/claw-interface/kustomize/base/static-secret.yaml` declares a
`VaultStaticSecret` with:
  - mount `srp`
  - KV-v2 path `ecap/claw-interface/env`
  - destination `vault-claw-interface-env-secret`
- The overlays do not patch this declaration. The deployment consumes
the Secret via `envFrom`, and no `secretKeyRef` names a `NANGO_*` key.
- In each environment, do this only after this code is rolled out there:
staging first (after staging acceptance), then production after its
release. Staging cleanup does not wait for production. In each
environment, remove only the obsolete claw-interface-specific `NANGO_*`
keys (the 2026-10-08 audit snapshot recorded five per environment),
then:
  - preserve shared keys and previous versions;
  - verify the synchronized Secret and new Pods.
- Check whether an `INTEGRATION_CREDITS_PER_CALL` key actually exists in
Vault before recording it as removed. The audit snapshot did not list
it.
- Do not revoke the shared Nango server key as part of this service's
cleanup.
- Historical collections and credentials remain retained.

## Rollback
Revert this PR and redeploy `claw-interface` and web. No data or
configuration was changed, and the deployed Secret keys still exist, so
the restored code picks them up again.

## Review comment disposition
| Feedback | Disposition |
|---|---|
| Codex P1: retire the configured Nango webhook before removing its
receiver | **Superseded by the owner decision reported in [this
comment](https://github.com/SerendipityOneInc/ecap-workspace/pull/4035#issuecomment-6059076512).**
The 404 is intended; no compatibility endpoint. Any remaining callback
configuration is to be disabled during the separate Nango shutdown; not
performed here. Not newly verified. |
| Codex P1: verify bot-runtime compatibility before omitting
`NANGO_GATEWAY_URL` | **Resolved by code evidence.** Both injection
sites are reachable only after `get_openclaw_client()`, which
unconditionally raises `agent.runtime_retired` (test
`TestGetOpenclawClient::test_retired_runtime_cannot_be_accessed`
passes). At base `3c32605e4`, nothing in `app/` outside the deleted
files and `settings.py` referenced the removed settings or modules
except the router registration, one docstring and these two dead
injection sites. No V2 Engine module was among them. The "new/recreated
FastClaw bot" check was removed instead of re-enabling V1. |
| Claude review (approve; later need-human-review on the same two items)
| Same dispositions as the two Codex items. The non-blocking note about
the proxy row in `architecture.md` is deferred until the proxy routes
are removed. |
| Codex re-review of the docs-only commit (APPROVE, no findings) | No
action needed. Codex notes the two earlier P1 items are no longer
reportable defects given the reported owner decision. |
| Claude re-review (NEED_HUMAN_REVIEW, no P0–P2 findings) | No code
change. It reviewed the previous body, which had not yet marked the two
items resolved; this body does. Its "FastClaw env contract for new bots"
concern is resolved by the `agent.runtime_retired` evidence above. Human
review remains required by the ruleset. |
| PR size check comment (FAILURE at 3,869 > 3,000) | Historical. The
`size-override` label is applied, and the latest `size / size-check`
runs are SUCCESS. The diff is about 98% deletion of Nango-only files. |
| [Independent review update
(tim-srp)](https://github.com/SerendipityOneInc/ecap-workspace/pull/4035#issuecomment-6059076512)
| Adopted: owner-decision framing, removal of the retired-V1 gate,
current-business acceptance, Vault declaration, and the
`INTEGRATION_CREDITS_PER_CALL` Vault caveat. The stale "removal is gated
on confirming no current caller" wording in `architecture.md` /
`architecture.zh-CN.md` was corrected to "removed separately in that
repository; do not add callers". |

## Test plan
Historical results on head `8e43283d2`, plus the follow-up re-check:
- [x] `bash scripts/verify-py.sh`: ruff check, ruff format, pyright
`app/ tests/` (0 errors), import-linter (8 contracts kept).
- [x] `services/claw-interface/scripts/ci-lint/01–08` guards all exit 0,
including deptry, import-linter repo sync and vulture.
- [x] Targeted pytest, first pass: 420 passed, 21 skipped. The skipped
tests are the BDD lifecycle scenarios, which need MongoDB; no local
MongoDB was started for that run. They are covered by the CI run below.
- [x] Follow-up re-check: `tests/unit/test_settings.py`,
`test_composio_connectors.py`, `test_openclaw_bot_config.py` and
`test_openclaw_client.py` → **241 passed**, matching the independent
review's count.
`TestGetOpenclawClient::test_retired_runtime_cannot_be_accessed` → 1
passed.
- [x] Regression tests:
- the real `create_app()` router has no `/openclaw/integrations*` path
and still registers all six Composio connector routes;
  - the four removed modules can no longer be imported;
  - stale `NANGO_*` env vars are ignored;
- deployment env built by the (retired) bot helpers omits
`NANGO_GATEWAY_URL` and keeps `USER_INTERNAL_TOKEN` /
`CLAW_INTERFACE_URL`.
- [x] `bash scripts/verify-web.sh <keys/ProviderLogo/composio specs>
src/locales/en.ts src/locales/zh.ts`:
- guards and `tsc` passed; eslint had 0 errors (2 existing warnings in
an unchanged spec);
- vitest matches by basename stem, so the `en`/`zh` targets widened the
run to 508 files / 6,560 tests, all passing.
- [x] `bash scripts/verify-changed.sh` on the committed diff and in the
pre-push hook: all changed surfaces passed, for both `8e43283d2` and the
docs-only follow-up `28ec64614`. Pre-commit had no applicable checks for
the two root-level Markdown files. Both pushes skipped only the pre-push
size check (`SKIP_PR_SIZE_CHECK=1`, covered by `size-override`); no
other check was skipped.
- [x] CI on the current head `28ec64614`: Code Quality Check run
37774452540, PR Size Check 37774451900, CI Gate 37774450881, CodeQL
37774450872, PR title check and auto-review all succeeded. The quality
jobs below all passed. On the previous head `8e43283d2`, Code Quality
Check run 37764990538 had passed the same jobs:
  - web-quality (lint/typecheck and test) and web-build-check;
  - claw-interface-quality (lint/typecheck and pytest);
  - python-duplication-check;
  - enterprise-admin, dashboard and platform quality.
  CodeQL, CI Gate, PR title and PR Size Check also succeeded.
- [ ] Not performed: live Vault or Nango callback inspection, live
traffic observation, real OAuth or tool-call tests. These belong to
staging acceptance or a separate operation.

## Size
The diff is +84 / −3,785 countable lines (3,869 total), above the
3,000-line budget, and about 98% of it deletes files used only by the
retired Nango integration. Following the repository's documented option
for size exceptions, the PR carries the `size-override` label. The only
bypass used was the pre-push size check (`SKIP_PR_SIZE_CHECK=1`);
changed-surface verification still ran. If reviewers prefer, it can be
split into a web PR (~1.7k lines) and a backend PR (~2.2k lines).



## Main synchronization (2026-10-09)

Merged current main `7cb5df1dd0d9a0b38be984d2f46fcaf8565ac00d` into this
PR in `481ee0005c65297e6c1e7d0ef3d49be9cb062c51`, preserving main as the
authority for the FastClaw V1 retirement in #4028.

- Resolved all six modify/delete conflicts by retaining main deletions:
`bot_config.py`, `openclaw_client/_bot_lifecycle.py`, and the four
corresponding retired V1 test files. No deleted V1 code was restored.
- The original injection/test edits in those six files are now redundant
and no longer part of this PR delta. Remaining scope against updated
main is 38 files, +80/-3775.
- Reviewed automatic merges in settings, collection constants,
import-linter configuration and settings tests. Current Composio paths,
shared proxy URL and authentication configuration remain intact.
- Local validation on merged tree: backend static checks (ruff, format,
pyright, 8 import contracts), frontend guards/tsc/eslint, 94 targeted
backend tests (Composio, settings, account organization, app startup and
lifetime), and 25 frontend query-key tests all passed. Full suites/build
remain CI checks.
- Normal push retained all validation hooks; used the
repository-supported size-only exception corresponding to this PR
existing `size-override` label, since the cleanup deletes more than 3000
lines. No force-push, deployment, resource/data mutation, or PR merge
performed.
```

### PR Body

## Summary
- Removes the legacy Nango integration code from `web/app` and `claw-interface`. The plugin page and chat Connector dialogs already use Composio. A repository reference search found no remaining caller of the removed frontend modules.
  - Frontend (6 files + 4 dedicated specs): `services/integrations.ts`, `models/integration.ts`, `hooks/useIntegrations.ts`, `hooks/queries/integrations/{useIntegrationsQuery,keys}.ts`, and `claw-settings/components/IntegrationsSection.tsx`.
  - Backend (4 files + 6 dedicated unit/BDD tests): the `/openclaw/integrations/*` router (connect, list, disconnect, enable, disable, and `POST webhooks/nango`), `services/integration_provider.py` (the Nango client), `database/integration_repo.py`, and `schema/integration.py`.
  - Also removes the router registration, the `INTEGRATION_CONNECTION_COLLECTION` code constant, and three import-linter entries. The live collection and its data are untouched.
- Removes the `AppSettings` fields `NANGO_GATEWAY_URL`, `NANGO_SERVER_URL`, `NANGO_PUBLIC_URL`, `NANGO_SECRET_KEY`, `NANGO_WEBHOOK_SECRET` and `INTEGRATION_CREDITS_PER_CALL`, plus the `NANGO_SERVER_URL` validator.
  - `AppSettings` uses `extra="ignore"`. A new test checks that leftover `NANGO_*` env vars, including a value the old validator rejected, do not break settings construction.
  - This removes code-side settings only. It does not change Vault or any deployed Secret (see "Configuration follow-through").
- Removes the `NANGO_GATEWAY_URL` bot-env injection in `services/openclaw/bot_config.py::build_deployment_env` and `services/openclaw_client/_bot_lifecycle.py::create_bot`.
  - Both sites are already unreachable in production code. Every caller first calls `get_openclaw_client()`, which has unconditionally raised `NotFoundError(code="agent.runtime_retired")` since #3874 retired FastClaw V1 (`services/claw-interface/app/services/openclaw_client/__init__.py:47-49`).
  - This affects only retired V1 code. No V1 or FastClaw path is re-enabled.
- **Unchanged:**
  - Composio routes and settings (`ECAP_PROXY_SERVICE_URL`) and the shared `ProviderLogo`;
  - `USER_INTERNAL_TOKEN` / `CLAW_INTERFACE_URL`;
  - V2 Engine installation and credential services;
  - auth, billing, and Python/npm dependencies;
  - historical Nango credentials and data, and runtime configuration.
- **Docs:**
  - `architecture.md` and `architecture.zh-CN.md` now describe the Composio connector path and mark the proxy's Nango `/integrations/*` routes as retiring separately in that repository.
  - The README and AGENTS dependency lists and the `web/app/AGENTS.md` React Query reference are updated.
  - The 2026-05-25 Composio spec gets a dated note. Archives are unchanged.

## Owner decision and scope (reported, not newly measured)
- The owner decision is **reported** in tim-srp's [independent review comment](https://github.com/SerendipityOneInc/ecap-workspace/pull/4035#issuecomment-6059076512): this cleanup may assume legacy Nango has no remaining users or calls, and historical connection owners should move to the Composio Connector. This PR relies on that reported decision. It was not personally verified as an owner instruction.
- This changes the accepted risk premise, not the evidence. **No new zero-traffic observation was made, and the Nango callback configuration was not inspected.** Earlier audit records (for example the 2026-10-08 snapshot of 0 claw-interface legacy requests over 30 days) remain historical snapshots.
- Removing `POST /openclaw/integrations/webhooks/nango` and the legacy management APIs is intended. After deployment those paths return 404, and no compatibility endpoint or Nango restoration is planned. Any remaining callback configuration is to be disabled during the separate Nango shutdown; not performed here.

## Related work (context only)
- SerendipityOneInc/ecap-skills#292 (removes the `zooclaw-connectors` skill source) was merged on 2026-10-08T09:47:38Z at head `4e369eea4c139803b8ae0f2c0ffc8de99109dfaf`. This shows the source is gone, not that previously installed copies are gone.
- This PR does not change `ecap-proxy-service`, `gcp-foundation`, `openclaw-docker` or `ecap-agent-pack`. Proxy route removal is handled in its own repository. The same comment reports the proxy G1 caller gate as closed by that decision; it was not closed by new traffic evidence.

## Before merge (merging to `main` auto-deploys staging)
- [x] Required CI checks pass on the current head `28ec64614e5088e87e867077da5fe8cfabed840e`. All required contexts (`code-quality`, `size / size-check`, `auto-review / auto-review`) are SUCCESS, and the commit's raw `statusCheckRollup` is SUCCESS (29 succeeded, 21 skipped, 0 failed). The superseded FAILURE runs from the label-less `opened` event belong to the previous head `8e43283d2` and remain there as history. Re-confirm if the head changes again.
- [ ] The PR is currently a draft with no approval. Before merge, a human reviewer marks it ready for review and approves it (the ruleset requires 1 approval and resolved review threads). This update does not change the draft status or record an approval.
- [ ] Rollout preparation: whoever runs the staging deploy has the acceptance checklist below.

## Post-merge staging acceptance (current business; required before any production release)
- [ ] Composio: provider list, connect, real OAuth callback, enable, disable, disconnect, and a real tool execution.
- [ ] V2 agent installation and start, including Engine credentials, and config update.
- [ ] Shared authentication, billing, and proxy features (for example YouTube and search) still work.
- [ ] claw-interface error rates and logs show no new errors on supported paths. `/openclaw/integrations/*` returning 404 is expected, and legacy requests alone do not trigger rollback; regressions in supported current functionality do.
- [ ] Production is a separate, explicit release step (manual release tag).

**Retired-V1 gates removed.** Earlier drafts listed two items that would require V1:
- verifying `NANGO_GATEWAY_URL` on newly created or recreated FastClaw computers;
- FastClaw env merge semantics.

Both are obsolete because V1 is retired in code (see Summary). Do not re-enable V1 or create/recreate a FastClaw computer to test this. `openclaw-docker` and `ecap-agent-pack` remain out of scope.

## Configuration follow-through (separate change, per environment after code rollout)
- Deleting settings does not remove live Vault keys. `services/claw-interface/kustomize/base/static-secret.yaml` declares a `VaultStaticSecret` with:
  - mount `srp`
  - KV-v2 path `ecap/claw-interface/env`
  - destination `vault-claw-interface-env-secret`
- The overlays do not patch this declaration. The deployment consumes the Secret via `envFrom`, and no `secretKeyRef` names a `NANGO_*` key.
- In each environment, do this only after this code is rolled out there: staging first (after staging acceptance), then production after its release. Staging cleanup does not wait for production. In each environment, remove only the obsolete claw-interface-specific `NANGO_*` keys (the 2026-10-08 audit snapshot recorded five per environment), then:
  - preserve shared keys and previous versions;
  - verify the synchronized Secret and new Pods.
- Check whether an `INTEGRATION_CREDITS_PER_CALL` key actually exists in Vault before recording it as removed. The audit snapshot did not list it.
- Do not revoke the shared Nango server key as part of this service's cleanup.
- Historical collections and credentials remain retained.

## Rollback
Revert this PR and redeploy `claw-interface` and web. No data or configuration was changed, and the deployed Secret keys still exist, so the restored code picks them up again.

## Review comment disposition
| Feedback | Disposition |
|---|---|
| Codex P1: retire the configured Nango webhook before removing its receiver | **Superseded by the owner decision reported in [this comment](https://github.com/SerendipityOneInc/ecap-workspace/pull/4035#issuecomment-6059076512).** The 404 is intended; no compatibility endpoint. Any remaining callback configuration is to be disabled during the separate Nango shutdown; not performed here. Not newly verified. |
| Codex P1: verify bot-runtime compatibility before omitting `NANGO_GATEWAY_URL` | **Resolved by code evidence.** Both injection sites are reachable only after `get_openclaw_client()`, which unconditionally raises `agent.runtime_retired` (test `TestGetOpenclawClient::test_retired_runtime_cannot_be_accessed` passes). At base `3c32605e4`, nothing in `app/` outside the deleted files and `settings.py` referenced the removed settings or modules except the router registration, one docstring and these two dead injection sites. No V2 Engine module was among them. The "new/recreated FastClaw bot" check was removed instead of re-enabling V1. |
| Claude review (approve; later need-human-review on the same two items) | Same dispositions as the two Codex items. The non-blocking note about the proxy row in `architecture.md` is deferred until the proxy routes are removed. |
| Codex re-review of the docs-only commit (APPROVE, no findings) | No action needed. Codex notes the two earlier P1 items are no longer reportable defects given the reported owner decision. |
| Claude re-review (NEED_HUMAN_REVIEW, no P0–P2 findings) | No code change. It reviewed the previous body, which had not yet marked the two items resolved; this body does. Its "FastClaw env contract for new bots" concern is resolved by the `agent.runtime_retired` evidence above. Human review remains required by the ruleset. |
| PR size check comment (FAILURE at 3,869 > 3,000) | Historical. The `size-override` label is applied, and the latest `size / size-check` runs are SUCCESS. The diff is about 98% deletion of Nango-only files. |
| [Independent review update (tim-srp)](https://github.com/SerendipityOneInc/ecap-workspace/pull/4035#issuecomment-6059076512) | Adopted: owner-decision framing, removal of the retired-V1 gate, current-business acceptance, Vault declaration, and the `INTEGRATION_CREDITS_PER_CALL` Vault caveat. The stale "removal is gated on confirming no current caller" wording in `architecture.md` / `architecture.zh-CN.md` was corrected to "removed separately in that repository; do not add callers". |

## Test plan
Historical results on head `8e43283d2`, plus the follow-up re-check:
- [x] `bash scripts/verify-py.sh`: ruff check, ruff format, pyright `app/ tests/` (0 errors), import-linter (8 contracts kept).
- [x] `services/claw-interface/scripts/ci-lint/01–08` guards all exit 0, including deptry, import-linter repo sync and vulture.
- [x] Targeted pytest, first pass: 420 passed, 21 skipped. The skipped tests are the BDD lifecycle scenarios, which need MongoDB; no local MongoDB was started for that run. They are covered by the CI run below.
- [x] Follow-up re-check: `tests/unit/test_settings.py`, `test_composio_connectors.py`, `test_openclaw_bot_config.py` and `test_openclaw_client.py` → **241 passed**, matching the independent review's count. `TestGetOpenclawClient::test_retired_runtime_cannot_be_accessed` → 1 passed.
- [x] Regression tests:
  - the real `create_app()` router has no `/openclaw/integrations*` path and still registers all six Composio connector routes;
  - the four removed modules can no longer be imported;
  - stale `NANGO_*` env vars are ignored;
  - deployment env built by the (retired) bot helpers omits `NANGO_GATEWAY_URL` and keeps `USER_INTERNAL_TOKEN` / `CLAW_INTERFACE_URL`.
- [x] `bash scripts/verify-web.sh <keys/ProviderLogo/composio specs> src/locales/en.ts src/locales/zh.ts`:
  - guards and `tsc` passed; eslint had 0 errors (2 existing warnings in an unchanged spec);
  - vitest matches by basename stem, so the `en`/`zh` targets widened the run to 508 files / 6,560 tests, all passing.
- [x] `bash scripts/verify-changed.sh` on the committed diff and in the pre-push hook: all changed surfaces passed, for both `8e43283d2` and the docs-only follow-up `28ec64614`. Pre-commit had no applicable checks for the two root-level Markdown files. Both pushes skipped only the pre-push size check (`SKIP_PR_SIZE_CHECK=1`, covered by `size-override`); no other check was skipped.
- [x] CI on the current head `28ec64614`: Code Quality Check run 37774452540, PR Size Check 37774451900, CI Gate 37774450881, CodeQL 37774450872, PR title check and auto-review all succeeded. The quality jobs below all passed. On the previous head `8e43283d2`, Code Quality Check run 37764990538 had passed the same jobs:
  - web-quality (lint/typecheck and test) and web-build-check;
  - claw-interface-quality (lint/typecheck and pytest);
  - python-duplication-check;
  - enterprise-admin, dashboard and platform quality.
  CodeQL, CI Gate, PR title and PR Size Check also succeeded.
- [ ] Not performed: live Vault or Nango callback inspection, live traffic observation, real OAuth or tool-call tests. These belong to staging acceptance or a separate operation.

## Size
The diff is +84 / −3,785 countable lines (3,869 total), above the 3,000-line budget, and about 98% of it deletes files used only by the retired Nango integration. Following the repository's documented option for size exceptions, the PR carries the `size-override` label. The only bypass used was the pre-push size check (`SKIP_PR_SIZE_CHECK=1`); changed-surface verification still ran. If reviewers prefer, it can be split into a web PR (~1.7k lines) and a backend PR (~2.2k lines).



## Main synchronization (2026-10-09)

Merged current main `7cb5df1dd0d9a0b38be984d2f46fcaf8565ac00d` into this PR in `481ee0005c65297e6c1e7d0ef3d49be9cb062c51`, preserving main as the authority for the FastClaw V1 retirement in #4028.

- Resolved all six modify/delete conflicts by retaining main deletions: `bot_config.py`, `openclaw_client/_bot_lifecycle.py`, and the four corresponding retired V1 test files. No deleted V1 code was restored.
- The original injection/test edits in those six files are now redundant and no longer part of this PR delta. Remaining scope against updated main is 38 files, +80/-3775.
- Reviewed automatic merges in settings, collection constants, import-linter configuration and settings tests. Current Composio paths, shared proxy URL and authentication configuration remain intact.
- Local validation on merged tree: backend static checks (ruff, format, pyright, 8 import contracts), frontend guards/tsc/eslint, 94 targeted backend tests (Composio, settings, account organization, app startup and lifetime), and 25 frontend query-key tests all passed. Full suites/build remain CI checks.
- Normal push retained all validation hooks; used the repository-supported size-only exception corresponding to this PR existing `size-override` label, since the cleanup deletes more than 3000 lines. No force-push, deployment, resource/data mutation, or PR merge performed.


---

## refactor(agents): remove retired FastClaw V1 code (#4028)

- **SHA**: `7cb5df1dd0d9a0b38be984d2f46fcaf8565ac00d`
- **作者**: kaka-srp
- **日期**: 2026-10-09T03:03:39Z
- **PR**: #4028

### Commit Message

```
refactor(agents): remove retired FastClaw V1 code (#4028)

Retired FastClaw V1 routes and runtime implementations remained after
admission and routing were removed in #3874. This PR deletes those
implementations, Council, exclusive dependencies and obsolete tests, and
removes unreachable V1 branches from retained Engine services.

Current Agent development/editing, Engine/ACS, desktop native OpenClaw,
iOS, persisted history and archive-based recovery remain supported.
**Agents → Legacy agent projects** and its Engine Builder/Pack
Test/submit workflow are retained for a separate next phase. Historical
FastClaw references retain the existing fail-closed
`agent.runtime_retired` boundary. This PR does not delete database
history, Vault configuration or infrastructure.

Validation:
- Started the changed local frontend/backend using `.vscode/tasks.json`
against real staging dependencies, without mocking HTTP responses.
Verified Agents, Builder list/new/fork, Engine source import,
archive-based recovery, test iteration, actual Engine/ACS preview
message/reply, accept/submit, model read/write, locale/timezone
propagation, official batch install/start/dedup/uninstall, artifact
publish/list/detail/download/delete, and logout/cache/session cleanup.
Batch install exercised the real changed service/runtime helpers; no
active vertical package was assigned to the account.
- Isolated test projects, runtimes, preview,
artifact/source/conversation were cleaned; the submitted test pack was
deprecated and the original account locale restored.
- Latest-head backend CI: **12,005 passed, 5 skipped; coverage 89.58%,
above the unchanged 89.5% requirement**. Local recovery suite: 45
passed. After merging latest main, scheduler/recovery checks: 21 passed.
Four earlier local BDD scenarios required unavailable local MongoDB; the
full backend suite ran in CI.
- Frontend focused Builder/client/owned-agent/model-control checks: 187
passed. Knip, frontend governance/TypeScript/ESLint, Python
Ruff/format/Pyright/import-linter, and skill-sync checks passed locally.
Latest-head frontend tests/build, CodeQL, duplication checks,
admin/dashboard/platform checks passed in CI.
- Coverage correction `4293794997` adds two tests that exercise real
recovery/renewal orchestration and require cancellation cleanup to
finish before returning. Independent mutation verification confirmed
both tests fail if awaited task cleanup is removed. No production
behavior or coverage threshold was changed to satisfy the gate.
- Latest main `3c32605e4a` is merged in `dcbaf53525`. Both branches
independently removed a scheduler job and changed the expected count
from 10 to 9; the combined result correctly has 8. Both removed-job
absence assertions and retained-job contracts remain enforced.
Independent AST review confirmed no other job or function binding was
lost.
- Independent local review used the latest main code-review skill,
covered the complete deletion inventory and retained callers, and found
no actionable introduced defects. Targeted reviews of both CI
corrections also passed. Automated Claude review found no code defects;
automated Codex review skipped because GitHub could not generate the
oversized diff.

CI status: **all required checks passed on
`dcbaf5352527f95c2e921e5e69b36617408f2c01`**. The backend lint job
initially hit a transient `setup-uv` manifest-download timeout; a
failed-job rerun passed Ruff, Pyright and all custom lint guards. Code
Quality Check completed successfully. No CI configuration was changed.

Existing validation issues remain separate per owner direction:
- Workspace Files list/content: staging Engine has no files root (local
and deployed staging both return 503).
- Global artifact-library rendering: stale runtime records cause 409;
Assistant-scoped access succeeds. The independent fix is PR #4029,
verified through staging requests and browser rendering.
- Localhost embedded artifact preview: resolver-origin CORS restriction.
Actual downloaded bytes and SHA-256 were verified; embedded preview was
not represented as passing.
- Historical non-Engine Pack Test cleanup can encounter
`agent.runtime_retired`, but its cleanup service is unchanged and main
already raises the identical error unconditionally. This is a
pre-existing operational issue, not introduced or worsened here. No
historical-data emptiness or cleanup success is claimed.

Evidence: [validation
report](docs/validation/2026-10-08-remove-fastclaw-v1-validation.md),
[design
spec](docs/superpowers/specs/2026-10-08-remove-fastclaw-v1-dead-code.md).
The latest CI results above supersede the earlier pending coverage
results in the report.

`size-override` covers the coherent retirement deletion exceeding the
line budget; ordinary quality gates remain enabled. This PR remains a
draft. Do not merge or release automatically.
```

### PR Body

Retired FastClaw V1 routes and runtime implementations remained after admission and routing were removed in #3874. This PR deletes those implementations, Council, exclusive dependencies and obsolete tests, and removes unreachable V1 branches from retained Engine services.

Current Agent development/editing, Engine/ACS, desktop native OpenClaw, iOS, persisted history and archive-based recovery remain supported. **Agents → Legacy agent projects** and its Engine Builder/Pack Test/submit workflow are retained for a separate next phase. Historical FastClaw references retain the existing fail-closed `agent.runtime_retired` boundary. This PR does not delete database history, Vault configuration or infrastructure.

Validation:
- Started the changed local frontend/backend using `.vscode/tasks.json` against real staging dependencies, without mocking HTTP responses. Verified Agents, Builder list/new/fork, Engine source import, archive-based recovery, test iteration, actual Engine/ACS preview message/reply, accept/submit, model read/write, locale/timezone propagation, official batch install/start/dedup/uninstall, artifact publish/list/detail/download/delete, and logout/cache/session cleanup. Batch install exercised the real changed service/runtime helpers; no active vertical package was assigned to the account.
- Isolated test projects, runtimes, preview, artifact/source/conversation were cleaned; the submitted test pack was deprecated and the original account locale restored.
- Merge-queue backend CI against latest main: **12,058 passed, 5 skipped; coverage 89.58%, above the unchanged 89.5% requirement**. Local recovery suite: 45 passed. After merging latest main, scheduler/recovery checks: 21 passed. Four earlier local BDD scenarios required unavailable local MongoDB; the full backend suite ran in CI.
- Frontend focused Builder/client/owned-agent/model-control checks: 187 passed. Knip, frontend governance/TypeScript/ESLint, Python Ruff/format/Pyright/import-linter, and skill-sync checks passed locally. Latest-head frontend tests/build, CodeQL, duplication checks, admin/dashboard/platform checks passed in CI.
- Coverage correction `4293794997` adds two tests that exercise real recovery/renewal orchestration and require cancellation cleanup to finish before returning. Independent mutation verification confirmed both tests fail if awaited task cleanup is removed. No production behavior or coverage threshold was changed to satisfy the gate.
- Latest main `3c32605e4a` is merged in `dcbaf53525`. Both branches independently removed a scheduler job and changed the expected count from 10 to 9; the combined result correctly has 8. Both removed-job absence assertions and retained-job contracts remain enforced. Independent AST review confirmed no other job or function binding was lost.
- Independent local review used the latest main code-review skill, covered the complete deletion inventory and retained callers, and found no actionable introduced defects. Targeted reviews of both CI corrections also passed. Automated Claude review found no code defects; automated Codex review skipped because GitHub could not generate the oversized diff.

CI status: **all required checks passed on PR head `dcbaf5352527f95c2e921e5e69b36617408f2c01` and merge-queue integration `7cb5df1dd0d9a0b38be984d2f46fcaf8565ac00d` against latest main**. The backend lint job initially hit a transient `setup-uv` manifest-download timeout; a failed-job rerun passed Ruff, Pyright and all custom lint guards. Code Quality Check completed successfully. No CI configuration was changed.

Existing validation issues remain separate per owner direction:
- Workspace Files list/content: staging Engine has no files root (local and deployed staging both return 503).
- Global artifact-library rendering: stale runtime records cause 409; Assistant-scoped access succeeds. The independent fix is PR #4029, verified through staging requests and browser rendering.
- Localhost embedded artifact preview: resolver-origin CORS restriction. Actual downloaded bytes and SHA-256 were verified; embedded preview was not represented as passing.
- Historical non-Engine Pack Test cleanup can encounter `agent.runtime_retired`, but its cleanup service is unchanged and main already raises the identical error unconditionally. This is a pre-existing operational issue, not introduced or worsened here. No historical-data emptiness or cleanup success is claimed.

Evidence: [validation report](docs/validation/2026-10-08-remove-fastclaw-v1-validation.md), [design spec](docs/superpowers/specs/2026-10-08-remove-fastclaw-v1-dead-code.md). The latest CI results above supersede the earlier pending coverage results in the report.

`size-override` covers the coherent retirement deletion exceeding the line budget; ordinary quality gates remain enabled. The owner authorized merging after validation and review. The protected merge queue passed all required checks and squash-merged this PR as `7cb5df1dd0d9a0b38be984d2f46fcaf8565ac00d`. Publishing a release is a separate action.


---
