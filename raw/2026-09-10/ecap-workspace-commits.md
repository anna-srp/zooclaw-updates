# SerendipityOneInc/ecap-workspace — commits 2026-09-10

## feat(business): notify Feishu after contact submissions (#3697)

- **SHA**: `673ee3d8ad388ed18018300c6dba62a85997d24d`
- **作者**: tim-srp
- **日期**: 2026-09-10T14:08:58Z
- **PR**: #3697

### Commit Message

```
feat(business): notify Feishu after contact submissions (#3697)

## Summary
After logging a business contact submission, optionally send a readable
Feishu bot message containing source `zoowork-business`, email, and
service. The existing frontend and API payload stay unchanged.

- Add `BUSINESS_CONTACT_FEISHU_WEBHOOK_URL`, defaulting to empty; skip
notification when unset.
- Send plain text with `aiohttp` in a background task with a 5-second
timeout. Notification failures do not fail the submission or expose the
webhook in logs.
- Keep the change in the existing route, settings, and test files only.

## Test plan
- [x] 34 targeted backend tests passed, including disabled notification,
message content, invalid input, timeout, transport failure, and bot
rejection.
- [x] Ruff, formatting, pyright, import-linter, and `git diff --check`
passed.

## Configuration
Set `BUSINESS_CONTACT_FEISHU_WEBHOOK_URL` in the production Vault KV
secret `srp/ecap/claw-interface/env` and roll out the backend to load
it. The webhook is not stored in this PR. No frontend deployment is
needed.
```

### PR Body

```
## Summary
After logging a business contact submission, optionally send a readable Feishu bot message containing source `zoowork-business`, email, and service. The existing frontend and API payload stay unchanged.

- Add `BUSINESS_CONTACT_FEISHU_WEBHOOK_URL`, defaulting to empty; skip notification when unset.
- Send plain text with `aiohttp` in a background task with a 5-second timeout. Notification failures do not fail the submission or expose the webhook in logs.
- Keep the change in the existing route, settings, and test files only.

## Test plan
- [x] 34 targeted backend tests passed, including disabled notification, message content, invalid input, timeout, transport failure, and bot rejection.
- [x] Ruff, formatting, pyright, import-linter, and `git diff --check` passed.

## Configuration
Set `BUSINESS_CONTACT_FEISHU_WEBHOOK_URL` in the production Vault KV secret `srp/ecap/claw-interface/env` and roll out the backend to load it. The webhook is not stored in this PR. No frontend deployment is needed.
```

---

## feat(business): record public sales contact submissions (#3696)

- **SHA**: `029923ffbeeceee674f69e27ccfa4ecdc494be99`
- **作者**: tim-srp
- **日期**: 2026-09-10T13:45:02Z
- **PR**: #3696

### Commit Message

```
feat(business): record public sales contact submissions (#3696)

## Summary
The Business contact form previously showed success without delivering
the lead. It now submits to an unauthenticated `POST /business/contact`
endpoint and shows success only after the backend acknowledges the
request.

- Validate email and accept a free-form service string using explicit
Pydantic request/response schemas; log accepted submissions as
single-line JSON under `business_contact_submitted`.
- Allow only the matching POST through the frontend auth middleware and
reuse the existing claw proxy.
- Keep submission and pending/error state in the existing form
component, calling the existing API helper directly. Submit the existing
dropdown text without a service enum or mapping.
- Log directly in the backend route; only the route and request/response
schema are new production files. No additional ViewModel, query hook,
service layer, or model files.

Contact details are recorded in application logs only. Deploy the
backend before the frontend.

## Test plan
- [x] Backend endpoint tests: 24 passed (anonymous access, free-form
service strings, invalid input rejection, single-line JSON logging,
OpenAPI schemas).
- [x] Frontend tests: 140 passed (submission lifecycle, localization,
navigation, middleware scope, proxy).
- [x] Backend ruff, formatting, pyright, and import-linter checks
passed.
- [x] Frontend TypeScript, changed-file ESLint, and governance guards
passed.
- [x] `git diff --check` passed.

## Review follow-up
Automated review flagged possible automated submissions/log flooding.
The route intentionally accepts anonymous requests and has no
route-specific server-side rate limit; frontend duplicate-submit
protection is not bot protection. The application already logs incoming
HTTP requests globally. Production edge/WAF protection has not been
verified, so the review's deployment-level impact remains unconfirmed.
This PR keeps the requested log-only scope; verify edge protection and
decide the rate-limit policy before rollout rather than introducing an
arbitrary limit or an unreliable per-process limiter here.
```

### PR Body

```
## Summary
The Business contact form previously showed success without delivering the lead. It now submits to an unauthenticated `POST /business/contact` endpoint and shows success only after the backend acknowledges the request.

- Validate email and accept a free-form service string using explicit Pydantic request/response schemas; log accepted submissions as single-line JSON under `business_contact_submitted`.
- Allow only the matching POST through the frontend auth middleware and reuse the existing claw proxy.
- Keep submission and pending/error state in the existing form component, calling the existing API helper directly. Submit the existing dropdown text without a service enum or mapping.
- Log directly in the backend route; only the route and request/response schema are new production files. No additional ViewModel, query hook, service layer, or model files.

Contact details are recorded in application logs only. Deploy the backend before the frontend.

## Test plan
- [x] Backend endpoint tests: 24 passed (anonymous access, free-form service strings, invalid input rejection, single-line JSON logging, OpenAPI schemas).
- [x] Frontend tests: 140 passed (submission lifecycle, localization, navigation, middleware scope, proxy).
- [x] Backend ruff, formatting, pyright, and import-linter checks passed.
- [x] Frontend TypeScript, changed-file ESLint, and governance guards passed.
- [x] `git diff --check` passed.

## Review follow-up
Automated review flagged possible automated submissions/log flooding. The route intentionally accepts anonymous requests and has no route-specific server-side rate limit; frontend duplicate-submit protection is not bot protection. The application already logs incoming HTTP requests globally. Production edge/WAF protection has not been verified, so the review's deployment-level impact remains unconfirmed. This PR keeps the requested log-only scope; verify edge protection and decide the rate-limit policy before rollout rather than introducing an arbitrary limit or an unreliable per-process limiter here.
```

---

## fix(agents): respect runtime permissions for shared agent actions (#3685)

- **SHA**: `a0967b393f160e73373feb80852ecbf780810153`
- **作者**: tim-srp
- **日期**: 2026-09-10T13:33:13Z
- **PR**: #3685

### Commit Message

```
fix(agents): respect runtime permissions for shared agent actions (#3685)

## Summary
- Allow shared Engine agents to be fired while the OpenClaw WebSocket is
disconnected.
- Derive shared card Fire and Update permissions from the existing
workspace eligibility function, preserving Computer connection
requirements and update/sync locks.

## Root cause
Shared cards used the global connection lock even though Engine
uninstall does not require that connection. The confirmation flow
already used runtime-aware eligibility, so the entry point and
confirmation disagreed.

## Test plan
- [x] 31 targeted tests passed across MyAgentsClient, its view model,
and agent eligibility.
- [x] Changed-file ESLint, frontend governance guards, and git diff
--check passed.
- [x] Regression coverage for disconnected Engine/Computer agents,
syncing, current/other workspace updates, and the actual Fire menu
action.
- [ ] Full local TypeScript check: blocked by chat-ui dependency/type
resolution (missing senderLabel in UserMessageView and React types). No
errors reported in changed files; CI remains authoritative.

Frontend-only change; no backend deployment or data migration required.
```

### PR Body

```
## Summary
- Allow shared Engine agents to be fired while the OpenClaw WebSocket is disconnected.
- Derive shared card Fire and Update permissions from the existing workspace eligibility function, preserving Computer connection requirements and update/sync locks.

## Root cause
Shared cards used the global connection lock even though Engine uninstall does not require that connection. The confirmation flow already used runtime-aware eligibility, so the entry point and confirmation disagreed.

## Test plan
- [x] 31 targeted tests passed across MyAgentsClient, its view model, and agent eligibility.
- [x] Changed-file ESLint, frontend governance guards, and git diff --check passed.
- [x] Regression coverage for disconnected Engine/Computer agents, syncing, current/other workspace updates, and the actual Fire menu action.
- [ ] Full local TypeScript check: blocked by chat-ui dependency/type resolution (missing senderLabel in UserMessageView and React types). No errors reported in changed files; CI remains authoritative.

Frontend-only change; no backend deployment or data migration required.
```

---

## fix(agents): retain exact environments for shared packs (#3694)

- **SHA**: `b8ff6694d84874be5c4cbf664cd3ad109b25241c`
- **作者**: kaka-srp
- **日期**: 2026-09-10T12:08:21Z
- **PR**: #3694

### Commit Message

```
fix(agents): retain exact environments for shared packs (#3694)

## Summary

Shared Engine Packs now keep the exact Environment build that matches
their approved runtime archive. After the existing Pack access checks,
installation and update authorize that build for the receiving
organization before creating or updating the Agent.

Updates also compare the actual Environment pin when the archive SHA is
unchanged, allowing previously installed instances that fell back to the
base Environment to recover through the normal update/retry path. An
already-correct binding remains a no-op.

## Root cause

The installer discarded Environment pins for nonofficial Packs shared
across organizations. Skills arrived without their dependency
environment, while author preview continued to use the dedicated build.
The same-SHA early return also skipped repair of existing incorrect
bindings.

## Test plan

- [x] 213 targeted runtime selection, install, lifecycle and Engine
client tests passed, including same-submission runtime revisions and
failure propagation.
- [x] Python static checks and pre-commit checks passed. CI backend
suite: 10,868 passed, 5 skipped; all ECAP CI and automated review checks
passed.
- [x] Actual local Python client → companion Controld → shared
PostgreSQL verified exact grants, retry, SHA/version upgrades, Agent
updates and uninstall/reinstall. Test resources were cleaned and the
original local service branches restored.
- [x] Independent agent review completed; the Engine same-submission
grant conflict was fixed and re-reviewed.
- [ ] After deployment, repeat the original report-generation task
across two organizations and verify the resulting files. Local tests did
not start a Sandbox or execute that user task.

## Rollout

Depends on [zooclaw-engine
#1350](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1350).
Deploy its grant endpoint and migrations first, then claw-interface.
This PR requires only the backend deployment. Existing affected
instances recover through normal Pack update/retry; no production
backfill or automatic scan is included.

Scope is limited to Engine Pack runtime authorization and binding. V1,
Builder prompts, ACS and frontend behavior are unchanged.
```

### PR Body

```
## Summary

Shared Engine Packs now keep the exact Environment build that matches their approved runtime archive. After the existing Pack access checks, installation and update authorize that build for the receiving organization before creating or updating the Agent.

Updates also compare the actual Environment pin when the archive SHA is unchanged, allowing previously installed instances that fell back to the base Environment to recover through the normal update/retry path. An already-correct binding remains a no-op.

## Root cause

The installer discarded Environment pins for nonofficial Packs shared across organizations. Skills arrived without their dependency environment, while author preview continued to use the dedicated build. The same-SHA early return also skipped repair of existing incorrect bindings.

## Test plan

- [x] 213 targeted runtime selection, install, lifecycle and Engine client tests passed, including same-submission runtime revisions and failure propagation.
- [x] Python static checks and pre-commit checks passed. CI backend suite: 10,868 passed, 5 skipped; all ECAP CI and automated review checks passed.
- [x] Actual local Python client → companion Controld → shared PostgreSQL verified exact grants, retry, SHA/version upgrades, Agent updates and uninstall/reinstall. Test resources were cleaned and the original local service branches restored.
- [x] Independent agent review completed; the Engine same-submission grant conflict was fixed and re-reviewed.
- [ ] After deployment, repeat the original report-generation task across two organizations and verify the resulting files. Local tests did not start a Sandbox or execute that user task.

## Rollout

Depends on [zooclaw-engine #1350](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1350). Deploy its grant endpoint and migrations first, then claw-interface. This PR requires only the backend deployment. Existing affected instances recover through normal Pack update/retry; no production backfill or automatic scan is included.

Scope is limited to Engine Pack runtime authorization and binding. V1, Builder prompts, ACS and frontend behavior are unchanged.
```

---

## feat(agents): unify agent navigation and legacy workspace access (#3693)

- **SHA**: `edfde328c6090f011c3f6e942a40d4deb5360938`
- **作者**: kaka-srp
- **日期**: 2026-09-10T11:36:18Z
- **PR**: #3693

### Commit Message

```
feat(agents): unify agent navigation and legacy workspace access (#3693)

## Summary

- Unify the global Agents navigation with the existing V2 workspaces:
five paginated shortcuts, fixed Main access, and direct
Connector/MCP/Skills/Knowledge Base links. Keep Main out of the
buildable list and preserve existing runtime IDs, tasks, channels and
schedules.
- Prepare editable baselines in place from exact installed sources,
preserving persona files, private/global skill ownership, runtime
configuration and environment pins. No Engine/ACS changes or database
migration in this PR.
- Keep ordinary task/history/artifact/schedule/channel use available for
legacy Agents without a baseline. Build, Agent Settings, Share and
Rename require a baseline; Delete retains the existing
confirmation/lifecycle and Main protection.
- Global New Task can select available created/shared/legacy Agents and
send through the existing session/conversation transport. Remove the
Hire more Agents footer.

## Review corrections

Independent reviewers covered frontend, business APIs, and
baseline/runtime-source behavior. Verified issues fixed before
submission:

- Restore the missing fixed Main destination without making Main
editable.
- Use Revision commits for the selected definition's model picker,
instead of the legacy endpoint that rejects definition edits. Explicit
model changes disable inherited Auto routing; unrelated edits preserve
it. If persistence succeeds but runtime application fails, show the
actual active model and retry the original request/key even after the
working Revision advances.
- Recognize an adopted baseline's source fingerprint for Share
readiness, and preserve portable runtime configuration on copy creation.
- Reject sharing an imported environment without complete portable build
source, including old install links, rather than silently dropping
files/build steps. Existing installed copies remain usable.
- Disable baseline-less Rename instead of adding cross-store locking for
a race-prone runtime/Mongo dual write. Prepared Agents retain
Revision-backed rename.

## CI follow-up

- Confirmed the automated review's empty-skills finding against Engine
main. Preserve the explicit skill-selection marker through adoption,
source-file round trips, frontend settings/model saves and subsequent
runtime projections. Explicit `skills: []` remains empty; absent
declarations keep default behavior, and unmarked sources keep their
prior digest.
- Updated the Mattermost context's exact ordinary-list assertion to
`listAgents(false)`; the HTTP behavior is unchanged. The context, query
and service regression suites pass (47 tests).
- Made the Auto-routing test's starting model explicit instead of
inheriting deployment defaults, and added an unchanged-model case. All
39 authoring tests pass with both local defaults and the CI model
default.

## Validation

- Backend: 375 targeted regression tests passed after the CI/review
follow-up, including six explicit-skill-policy tests. Auto-routing
fixture recheck: 39 passed under local and CI model defaults. Ruff,
formatting, Pyright and all eight import contracts passed.
- Shared chat package: TypeScript, 11 Agent picker tests and scoped
ESLint passed.
- Frontend: 304 changed-surface regression tests passed after the
follow-up; governance guards, TypeScript and full ESLint passed. Shared
Composer model state suite: 40 passed.
- Latest main merged locally, including the independent API
documentation link fix.
- Earlier authorized local/staging baseline trials and encrypted-client
read/write evidence are documented in the design spec. This review did
not repeat live adoption or a real browser-to-model turn;
mocks/plain-Mongo checks are not claimed as CSFLE or end-to-end proof.

## Scope / rollout

Frontend + claw-interface changes only. No dependency bump, new feature
flag, credential, schema migration, production deployment or bulk
adoption on reads. Existing legacy agents stay usable before offline
baseline preparation. Imported-environment sharing remains explicitly
unavailable until full portable environment source is supported.

The user authorized `size-override` for this cross-surface feature. The
PR keeps the offline-baseline contract, legacy read access, navigation
and launcher consumers together with their regression coverage; it does
not change Engine/ACS or release workflows.

Design and validation history:
`docs/superpowers/specs/2026-09-10-unified-agents-navigation.md`.
```

### PR Body

```
## Summary

- Unify the global Agents navigation with the existing V2 workspaces: five paginated shortcuts, fixed Main access, and direct Connector/MCP/Skills/Knowledge Base links. Keep Main out of the buildable list and preserve existing runtime IDs, tasks, channels and schedules.
- Prepare editable baselines in place from exact installed sources, preserving persona files, private/global skill ownership, runtime configuration and environment pins. No Engine/ACS changes or database migration in this PR.
- Keep ordinary task/history/artifact/schedule/channel use available for legacy Agents without a baseline. Build, Agent Settings, Share and Rename require a baseline; Delete retains the existing confirmation/lifecycle and Main protection.
- Global New Task can select available created/shared/legacy Agents and send through the existing session/conversation transport. Remove the Hire more Agents footer.

## Review corrections

Independent reviewers covered frontend, business APIs, and baseline/runtime-source behavior. Verified issues fixed before submission:

- Restore the missing fixed Main destination without making Main editable.
- Use Revision commits for the selected definition's model picker, instead of the legacy endpoint that rejects definition edits. Explicit model changes disable inherited Auto routing; unrelated edits preserve it. If persistence succeeds but runtime application fails, show the actual active model and retry the original request/key even after the working Revision advances.
- Recognize an adopted baseline's source fingerprint for Share readiness, and preserve portable runtime configuration on copy creation.
- Reject sharing an imported environment without complete portable build source, including old install links, rather than silently dropping files/build steps. Existing installed copies remain usable.
- Disable baseline-less Rename instead of adding cross-store locking for a race-prone runtime/Mongo dual write. Prepared Agents retain Revision-backed rename.

## CI follow-up

- Confirmed the automated review's empty-skills finding against Engine main. Preserve the explicit skill-selection marker through adoption, source-file round trips, frontend settings/model saves and subsequent runtime projections. Explicit `skills: []` remains empty; absent declarations keep default behavior, and unmarked sources keep their prior digest.
- Updated the Mattermost context's exact ordinary-list assertion to `listAgents(false)`; the HTTP behavior is unchanged. The context, query and service regression suites pass (47 tests).
- Made the Auto-routing test's starting model explicit instead of inheriting deployment defaults, and added an unchanged-model case. All 39 authoring tests pass with both local defaults and the CI model default.

## Validation

- Backend: 375 targeted regression tests passed after the CI/review follow-up, including six explicit-skill-policy tests. Auto-routing fixture recheck: 39 passed under local and CI model defaults. Ruff, formatting, Pyright and all eight import contracts passed.
- Shared chat package: TypeScript, 11 Agent picker tests and scoped ESLint passed.
- Frontend: 304 changed-surface regression tests passed after the follow-up; governance guards, TypeScript and full ESLint passed. Shared Composer model state suite: 40 passed.
- Latest main merged locally, including the independent API documentation link fix.
- Earlier authorized local/staging baseline trials and encrypted-client read/write evidence are documented in the design spec. This review did not repeat live adoption or a real browser-to-model turn; mocks/plain-Mongo checks are not claimed as CSFLE or end-to-end proof.

## Scope / rollout

Frontend + claw-interface changes only. No dependency bump, new feature flag, credential, schema migration, production deployment or bulk adoption on reads. Existing legacy agents stay usable before offline baseline preparation. Imported-environment sharing remains explicitly unavailable until full portable environment source is supported.

The user authorized `size-override` for this cross-surface feature. The PR keeps the offline-baseline contract, legacy read access, navigation and launcher consumers together with their regression coverage; it does not change Engine/ACS or release workflows.

Design and validation history: `docs/superpowers/specs/2026-09-10-unified-agents-navigation.md`.
```

---

## fix(settings): API 快速入门直接使用 ZooWork 域名 (#3691)

- **SHA**: `de1d2bde3e39443b9c963d1ea9d97d65948e2ebd`
- **作者**: lynn Zhuang
- **日期**: 2026-09-10T09:31:25Z
- **PR**: #3691

### Commit Message

```
fix(settings): API 快速入门直接使用 ZooWork 域名 (#3691)

## 修复内容

将 API Keys 页及创建密钥后引导中的 API Quickstart 链接直接指向
`https://zoowork.ai/docs/en/get-started/quickstart`，避免打开文档时地址栏先出现
`zooclaw.ai` 再切换为 `zoowork.ai`。

## 问题原因

共享的 Quickstart 地址仍使用旧域名。旧地址返回 301 跳转至
ZooWork，造成额外请求和地址栏闪现。同步删除了「文档迁移前保留旧域名」的过期注释。文档路径及英文语言设置保持不变。

## 验证

- [x] 确认旧地址返回 301，新地址直接返回 200。
- [x] 更新现有链接断言：修复前 2 个用例失败，修复后 API Keys 的 57 项测试全部通过。
- [x] 通过 `verify-web.sh`：TypeScript、目标测试、ESLint 及适用的治理检查。

仅修改前端文档链接，无需调整后端 API 域名或部署配置。
```

### PR Body

```
## 修复内容

将 API Keys 页及创建密钥后引导中的 API Quickstart 链接直接指向 `https://zoowork.ai/docs/en/get-started/quickstart`，避免打开文档时地址栏先出现 `zooclaw.ai` 再切换为 `zoowork.ai`。

## 问题原因

共享的 Quickstart 地址仍使用旧域名。旧地址返回 301 跳转至 ZooWork，造成额外请求和地址栏闪现。同步删除了「文档迁移前保留旧域名」的过期注释。文档路径及英文语言设置保持不变。

## 验证

- [x] 确认旧地址返回 301，新地址直接返回 200。
- [x] 更新现有链接断言：修复前 2 个用例失败，修复后 API Keys 的 57 项测试全部通过。
- [x] 通过 `verify-web.sh`：TypeScript、目标测试、ESLint 及适用的治理检查。

仅修改前端文档链接，无需调整后端 API 域名或部署配置。
```

---

## feat(builder): prepare project roots without starting a model turn (#3687)

- **SHA**: `8d97743423ca0e6afb1c8ffcf89c76917177fd02`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-10T08:16:37Z
- **PR**: #3687

### Commit Message

```
feat(builder): prepare project roots without starting a model turn (#3687)

## Summary

Add authenticated `POST /agent-builder/v2/projects/{project_id}/prepare`
so a dedicated Builder Project can initialize and validate its canonical
workspace before its first model turn. Reuse the existing
owned-project/runtime readiness guards, renewable ingress claim, and
`ensure_project_root` / `assert_project_root` operations. The endpoint
does not post a message or call an LLM.

This supports Engine Builder smoke provisioning through real Project
creation instead of an ordinary Agent Studio hire with missing
`BUILDER_PROJECT_CONTEXT.json`. Deploy this backend endpoint before
enabling the corresponding Engine smoke path; no frontend change or
existing-project migration is required.

## Test plan

- 51 targeted runtime-service/lifecycle tests passed, including project
ownership, route auth, claim conflict, initialization/assert ordering,
and failure without turn dispatch.
- Full backend Ruff check and format passed; targeted Pyright passed
with repository checking levels; isolated import-linter (8 contracts),
deptry, and vulture passed.
- Local tooling limitation: the shared venv has a broken Python shebang
and lacks Pyright. Tests used an isolated Python 3.13 interpreter with
existing read-only dependencies; targeted Pyright used an explicit
temporary dependency path. `verify-py.sh` could not complete its
standard entrypoints; `verify-changed.sh` explicitly skipped backend
verification for incomplete tooling. Three broken hook entrypoints were
skipped only after their equivalent isolated commands passed. Shared
venv unchanged.
- No full pytest/coverage suite, Python 3.12 CI-equivalent local
environment, live model calls, deployment, or staging mutations
performed. CI remains required.
```

### PR Body

```
## Summary

Add authenticated `POST /agent-builder/v2/projects/{project_id}/prepare` so a dedicated Builder Project can initialize and validate its canonical workspace before its first model turn. Reuse the existing owned-project/runtime readiness guards, renewable ingress claim, and `ensure_project_root` / `assert_project_root` operations. The endpoint does not post a message or call an LLM.

This supports Engine Builder smoke provisioning through real Project creation instead of an ordinary Agent Studio hire with missing `BUILDER_PROJECT_CONTEXT.json`. Deploy this backend endpoint before enabling the corresponding Engine smoke path; no frontend change or existing-project migration is required.

## Test plan

- 51 targeted runtime-service/lifecycle tests passed, including project ownership, route auth, claim conflict, initialization/assert ordering, and failure without turn dispatch.
- Full backend Ruff check and format passed; targeted Pyright passed with repository checking levels; isolated import-linter (8 contracts), deptry, and vulture passed.
- Local tooling limitation: the shared venv has a broken Python shebang and lacks Pyright. Tests used an isolated Python 3.13 interpreter with existing read-only dependencies; targeted Pyright used an explicit temporary dependency path. `verify-py.sh` could not complete its standard entrypoints; `verify-changed.sh` explicitly skipped backend verification for incomplete tooling. Three broken hook entrypoints were skipped only after their equivalent isolated commands passed. Shared venv unchanged.
- No full pytest/coverage suite, Python 3.12 CI-equivalent local environment, live model calls, deployment, or staging mutations performed. CI remains required.
```

---

## fix(chat): isolate active subagents from activity summaries (#3689)

- **SHA**: `b0739251895b29f8e882f447790004e2fab2502c`
- **作者**: kaka-srp
- **日期**: 2026-09-10T08:02:39Z
- **PR**: #3689

### Commit Message

```
fix(chat): isolate active subagents from activity summaries (#3689)

## Summary

When subagent creation fails and later retries succeed, the activity
summary now returns to the normal completed state instead of remaining
at `Delegated work · needs attention`. Failed attempts stay available in
the expandable detail rows.

Active or approval-waiting subagents appear in a separate delegated-work
group, with their own status and elapsed time, so they cannot override
the ordinary activity summary. This change is limited to the shared
`ToolGroup` component and its rendering tests.

## Root cause

The delegated-work summary bypassed the ordinary activity rules whenever
any `sessions_spawn` step was present. Historical spawn errors therefore
kept the whole group failed and expanded, while a completed child could
also hide ordinary tools that were still running. Separating active
children from historical steps lets terminal attempts use the existing
activity-summary rules.

## Test plan

- [x] Targeted ToolGroup and AssistantMessage rendering suites: 82 tests
passed, covering rejected calls and successful retries, recovery timing,
independent running/approval states, and child completion/failure moving
into history.
- [x] `pnpm tsc` in `web/packages/chat-ui`.
- [x] `pnpm lint` in `web/packages/chat-ui`.
- [x] `git diff --check`.
```

### PR Body

```
## Summary

When subagent creation fails and later retries succeed, the activity summary now returns to the normal completed state instead of remaining at `Delegated work · needs attention`. Failed attempts stay available in the expandable detail rows.

Active or approval-waiting subagents appear in a separate delegated-work group, with their own status and elapsed time, so they cannot override the ordinary activity summary. This change is limited to the shared `ToolGroup` component and its rendering tests.

## Root cause

The delegated-work summary bypassed the ordinary activity rules whenever any `sessions_spawn` step was present. Historical spawn errors therefore kept the whole group failed and expanded, while a completed child could also hide ordinary tools that were still running. Separating active children from historical steps lets terminal attempts use the existing activity-summary rules.

## Test plan

- [x] Targeted ToolGroup and AssistantMessage rendering suites: 82 tests passed, covering rejected calls and successful retries, recovery timing, independent running/approval states, and child completion/failure moving into history.
- [x] `pnpm tsc` in `web/packages/chat-ui`.
- [x] `pnpm lint` in `web/packages/chat-ui`.
- [x] `git diff --check`.
```

---

## fix(agents): raise paid plan install limits to 20/40/100 (#3684)

- **SHA**: `3e232907e40493505cc9b7dca62e1c8f55c8a17f`
- **作者**: tim-srp
- **日期**: 2026-09-10T06:43:53Z
- **PR**: #3684

### Commit Message

```
fix(agents): raise paid plan install limits to 20/40/100 (#3684)

## Summary
- Raise Starter / Pro / Ultra installed-agent caps from 5 / 10 / 20 to
20 / 40 / 100.
- The shared backend policy covers agent-definition creation, engine
installs, computer installs, and batch installs. Free and expired
subscriptions remain capped at 5; existing vertical-pack exemptions
remain intact.
- Preserve the existing unknown-plan fallback to Starter, now 20.

## Root cause
Paid subscriptions still used the original low install caps, so
agent-definition creation could fail with `agent.limit_exceeded` after
only 5 agents on Starter.

## Test plan
- [x] 224 targeted quota/install tests, including 24 boundary cases
covering every tier and all three quota entry points.
- [x] 13 agent-development creation-claim tests.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8
import contracts passed.

Backend deployment only; no database migration or frontend deployment
required.
```

### PR Body

```
## Summary
- Raise Starter / Pro / Ultra installed-agent caps from 5 / 10 / 20 to 20 / 40 / 100.
- The shared backend policy covers agent-definition creation, engine installs, computer installs, and batch installs. Free and expired subscriptions remain capped at 5; existing vertical-pack exemptions remain intact.
- Preserve the existing unknown-plan fallback to Starter, now 20.

## Root cause
Paid subscriptions still used the original low install caps, so agent-definition creation could fail with `agent.limit_exceeded` after only 5 agents on Starter.

## Test plan
- [x] 224 targeted quota/install tests, including 24 boundary cases covering every tier and all three quota entry points.
- [x] 13 agent-development creation-claim tests.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8 import contracts passed.

Backend deployment only; no database migration or frontend deployment required.
```

---

## fix(e2e): switch LLM judge default to gpt-5.6-luna (#3682)

- **SHA**: `9a1192418138f67932bf1cbc360ef41989c6d546`
- **作者**: tim-srp
- **日期**: 2026-09-10T06:04:04Z
- **PR**: #3682

### Commit Message

```
fix(e2e): switch LLM judge default to gpt-5.6-luna (#3682)

## Summary
- Change the E2E LLM judge default model from `gpt-4o-mini` to
`gpt-5.6-luna`.
- Preserve explicit model overrides and the existing LiteLLM endpoint
and authentication.

## Root cause
The production E2E judge's existing default model is reported
unavailable on the configured LiteLLM proxy. The CI workflow does not
set `LLM_JUDGE_MODEL`, so it uses this default.

## Test plan
- [x] `git diff --check`
- [x] Trace CI configuration to confirm it uses the judge default.
- [x] Run `bash scripts/verify-changed.sh` (no locally verifiable
surfaces selected for this E2E-only change).
- Local lint/type checks and live E2E were not run: the isolated
worktree has no frontend dependencies; live model availability remains
to be verified by an authenticated E2E run.
```

### PR Body

```
## Summary
- Change the E2E LLM judge default model from `gpt-4o-mini` to `gpt-5.6-luna`.
- Preserve explicit model overrides and the existing LiteLLM endpoint and authentication.

## Root cause
The production E2E judge's existing default model is reported unavailable on the configured LiteLLM proxy. The CI workflow does not set `LLM_JUDGE_MODEL`, so it uses this default.

## Test plan
- [x] `git diff --check`
- [x] Trace CI configuration to confirm it uses the judge default.
- [x] Run `bash scripts/verify-changed.sh` (no locally verifiable surfaces selected for this E2E-only change).
- Local lint/type checks and live E2E were not run: the isolated worktree has no frontend dependencies; live model availability remains to be verified by an authenticated E2E run.
```

---

## fix(claw-interface): keep Engine-owned MCP options through the read/write-back (#3680)

- **SHA**: `b27a26465181c5a542c65d36686a406cbf5bbf21`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-10T03:30:31Z
- **PR**: #3680

### Commit Message

```
fix(claw-interface): keep Engine-owned MCP options through the read/write-back (#3680)

Fixes #3679。

## 问题

engine #1216（`v0.1.28-release` 起在生产）给 managed agents API 的
`resource.mcp[]` 加了可选的 `exposure: "deferred" | "direct"`。claw-interface
的 `EngineMcpServer` 是 `extra="forbid"` 且没有这个字段，于是带该字段的 Agent：

- `engine_client/_agents.py::_parse_mcp_servers` 逐条 `model_validate` 直接
ValidationError，`get_agent` / `get_agent_status` 的 20+ 个调用点（agent
builder、activation / apply / change_set / revision、`service_api`）对这个
Agent 全部失败；
- 即使读侧不炸，`mcp_sync_service` 与 `acp_engine_mcp` 都是「读回整个数组 → 保留不归自己管的条目 →
整体 PUT 回去」，回写的 `model_dump(exclude_none=True)` 会把 schema
不认识的键丢掉，一次无关的同步就把用户配的 `direct` 悄悄改回 `deferred`。

## 改动

- `EngineMcpServer` 显式声明 `exposure: Literal["deferred", "direct"] | None
= None`，缺省 `None` 表示「未声明」，不会替调用方发一个它没要的值。
- `extra` 从 `forbid` 改为 `allow`：这个 schema 是 engine
所拥有契约的投影，本服务只是读回、保留、原样写回，engine 之后再加字段（计划里还有 `permission` / `tools` /
`context`）不该让读整体失败，也不该在回写时被静默丢弃。构造侧的拼写保护仍由 pyright 的字段签名提供。
- 两个回归测试：engine client 层钉住带 `exposure`
和一个未知键的条目能读进来、并逐字段回写；`mcp_sync_service` 层钉住 personal MCP 同步不会重置它不管的
server 的 `exposure`。

## 验证

- `pytest tests/unit/test_engine_client.py
tests/unit/test_mcp_sync_service.py tests/unit/test_acp_engine_mcp.py
tests/unit/test_engine_client_mcp.py` — 100 passed
- `ruff check` / `ruff format --check` 改动文件通过；pyright 对改动文件除本地 venv
解析不到的 import 假阴性外无报错

## 不在本 PR 范围

在 MCP 配置界面把 `direct` / `deferred` 暴露给用户，另开。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_017dPVyymv7nqvkX7KnpL9VE
```

### PR Body

```
Fixes #3679。

## 问题

engine #1216（`v0.1.28-release` 起在生产）给 managed agents API 的 `resource.mcp[]` 加了可选的 `exposure: "deferred" | "direct"`。claw-interface 的 `EngineMcpServer` 是 `extra="forbid"` 且没有这个字段，于是带该字段的 Agent：

- `engine_client/_agents.py::_parse_mcp_servers` 逐条 `model_validate` 直接 ValidationError，`get_agent` / `get_agent_status` 的 20+ 个调用点（agent builder、activation / apply / change_set / revision、`service_api`）对这个 Agent 全部失败；
- 即使读侧不炸，`mcp_sync_service` 与 `acp_engine_mcp` 都是「读回整个数组 → 保留不归自己管的条目 → 整体 PUT 回去」，回写的 `model_dump(exclude_none=True)` 会把 schema 不认识的键丢掉，一次无关的同步就把用户配的 `direct` 悄悄改回 `deferred`。

## 改动

- `EngineMcpServer` 显式声明 `exposure: Literal["deferred", "direct"] | None = None`，缺省 `None` 表示「未声明」，不会替调用方发一个它没要的值。
- `extra` 从 `forbid` 改为 `allow`：这个 schema 是 engine 所拥有契约的投影，本服务只是读回、保留、原样写回，engine 之后再加字段（计划里还有 `permission` / `tools` / `context`）不该让读整体失败，也不该在回写时被静默丢弃。构造侧的拼写保护仍由 pyright 的字段签名提供。
- 两个回归测试：engine client 层钉住带 `exposure` 和一个未知键的条目能读进来、并逐字段回写；`mcp_sync_service` 层钉住 personal MCP 同步不会重置它不管的 server 的 `exposure`。

## 验证

- `pytest tests/unit/test_engine_client.py tests/unit/test_mcp_sync_service.py tests/unit/test_acp_engine_mcp.py tests/unit/test_engine_client_mcp.py` — 100 passed
- `ruff check` / `ruff format --check` 改动文件通过；pyright 对改动文件除本地 venv 解析不到的 import 假阴性外无报错

## 不在本 PR 范围

在 MCP 配置界面把 `direct` / `deferred` 暴露给用户，另开。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_017dPVyymv7nqvkX7KnpL9VE
```

---

## build(deps): update websockets requirement from >=17.0.1 to >=17.1 in /services/claw-interface (#3654)

- **SHA**: `7ea6807e460b2358c300b714cb81fefe191b21ec`
- **作者**: dependabot[bot]
- **日期**: 2026-09-10T03:31:19Z
- **PR**: #3654

### Commit Message

```
build(deps): update websockets requirement from >=17.0.1 to >=17.1 in /services/claw-interface (#3654)

Updates the requirements on
[websockets](https://github.com/python-websockets/websockets) to permit
the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/python-websockets/websockets/releases">websockets's
releases</a>.</em></p>
<blockquote>
<h2>17.1</h2>
<p>See <a
href="https://websockets.readthedocs.io/en/stable/project/changelog.html">https://websockets.readthedocs.io/en/stable/project/changelog.html</a>
for details.</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/python-websockets/websockets/commit/e87ea9be0373edd5065b5e94dfa714cfde23023b"><code>e87ea9b</code></a>
Release version 17.1.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/caf68ab866350ab43305bc0a2ce28e4c845b90ab"><code>caf68ab</code></a>
Minor whitespace normalization.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/f4c73b76c74044c53f700360792448ee0328983b"><code>f4c73b7</code></a>
Accept pathlib.Path objects in path arguments.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/b1e4a144d1824ec4dbd2416489691bbe212a1be8"><code>b1e4a14</code></a>
Clarify when the new asyncio implementation became the default.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/c7cc7ed3508c3ce082801994e7587ac694758102"><code>c7cc7ed</code></a>
Move process_exception to the Sans-I/O layer.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/2543503f5e6633e79afb20992511b12ef2b7d663"><code>2543503</code></a>
Support reconnecting in the threading implementation.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/1c8fb090d966c358dcb4069b8c71c13969d1cec0"><code>1c8fb09</code></a>
Follow redirects in the sync implementation.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/1f7f0e537233ac82e4ca51921678963c696c8c08"><code>1f7f0e5</code></a>
Deprecate calling connect() directly.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/c06d5c566b04113405272230856de669e8534e74"><code>c06d5c5</code></a>
Support overriding host/post in the sync client.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/885e69bc1a218566bb0ad653c2c326e80245ab6a"><code>885e69b</code></a>
Add tests for connecting without a context manager.</li>
<li>Additional commits viewable in <a
href="https://github.com/python-websockets/websockets/compare/17.0.1...17.1">compare
view</a></li>
</ul>
</details>
<br />

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

```
Updates the requirements on [websockets](https://github.com/python-websockets/websockets) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/python-websockets/websockets/releases">websockets's releases</a>.</em></p>
<blockquote>
<h2>17.1</h2>
<p>See <a href="https://websockets.readthedocs.io/en/stable/project/changelog.html">https://websockets.readthedocs.io/en/stable/project/changelog.html</a> for details.</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/python-websockets/websockets/commit/e87ea9be0373edd5065b5e94dfa714cfde23023b"><code>e87ea9b</code></a> Release version 17.1.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/caf68ab866350ab43305bc0a2ce28e4c845b90ab"><code>caf68ab</code></a> Minor whitespace normalization.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/f4c73b76c74044c53f700360792448ee0328983b"><code>f4c73b7</code></a> Accept pathlib.Path objects in path arguments.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/b1e4a144d1824ec4dbd2416489691bbe212a1be8"><code>b1e4a14</code></a> Clarify when the new asyncio implementation became the default.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/c7cc7ed3508c3ce082801994e7587ac694758102"><code>c7cc7ed</code></a> Move process_exception to the Sans-I/O layer.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/2543503f5e6633e79afb20992511b12ef2b7d663"><code>2543503</code></a> Support reconnecting in the threading implementation.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/1c8fb090d966c358dcb4069b8c71c13969d1cec0"><code>1c8fb09</code></a> Follow redirects in the sync implementation.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/1f7f0e537233ac82e4ca51921678963c696c8c08"><code>1f7f0e5</code></a> Deprecate calling connect() directly.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/c06d5c566b04113405272230856de669e8534e74"><code>c06d5c5</code></a> Support overriding host/post in the sync client.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/885e69bc1a218566bb0ad653c2c326e80245ab6a"><code>885e69b</code></a> Add tests for connecting without a context manager.</li>
<li>Additional commits viewable in <a href="https://github.com/python-websockets/websockets/compare/17.0.1...17.1">compare view</a></li>
</ul>
</details>
<br />
```

---

## build(deps-dev): update ruff requirement from >=0.16.4 to >=0.16.5 in /services/claw-interface (#3655)

- **SHA**: `e838508b068d61de65e17cb8c37bb14721bb616c`
- **作者**: dependabot[bot]
- **日期**: 2026-09-10T03:31:07Z
- **PR**: #3655

### Commit Message

```
build(deps-dev): update ruff requirement from >=0.16.4 to >=0.16.5 in /services/claw-interface (#3655)

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to
permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/releases">ruff's
releases</a>.</em></p>
<blockquote>
<h2>0.16.5</h2>
<h2>Release Notes</h2>
<p>Released on 2026-08-27.</p>
<h3>Preview features</h3>
<ul>
<li>Allow rules without codes (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28049">#28049</a>)</li>
<li>Introduce category selectors (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27666">#27666</a>)</li>
<li>Update preview default rules and categories (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27877">#27877</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-async</code>] Detect blocking generic HTTP requests
(<code>ASYNC210</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28024">#28024</a>)</li>
<li>[<code>flake8-datetimez</code>] Allow timezone-safe
<code>strptime</code> chains (<code>DTZ007</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28023">#28023</a>)</li>
<li>[<code>flake8-simplify</code>] Respect side effects in
<code>lambda</code> defaults (<code>SIM401</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28000">#28000</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Fix duplicated &quot;of&quot; in <code>ClientOptions</code> doc
comment (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27978">#27978</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Document rule acceptance guidelines (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27910">#27910</a>)</li>
<li>Document the new category selectors (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27906">#27906</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li>
<li><a href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li>
<li><a
href="https://github.com/jelle-openai"><code>@​jelle-openai</code></a></li>
<li><a
href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a
href="https://github.com/aarushkandukoori"><code>@​aarushkandukoori</code></a></li>
</ul>
<h2>Install ruff 0.16.5</h2>
<h3>Install prebuilt binaries via shell script</h3>
<pre lang="sh"><code>curl --proto '=https' --tlsv1.2 -LsSf
https://releases.astral.sh/github/ruff/releases/download/0.16.5/ruff-installer.sh
| sh
</code></pre>
<h3>Install prebuilt binaries via powershell script</h3>
<pre lang="sh"><code>powershell -ExecutionPolicy Bypass -c &quot;irm
https://releases.astral.sh/github/ruff/releases/download/0.16.5/ruff-installer.ps1
| iex&quot;
</code></pre>
<h2>Download ruff 0.16.5</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
changelog</a>.</em></p>
<blockquote>
<h2>0.16.5</h2>
<p>Released on 2026-08-27.</p>
<h3>Preview features</h3>
<ul>
<li>Allow rules without codes (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28049">#28049</a>)</li>
<li>Introduce category selectors (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27666">#27666</a>)</li>
<li>Update preview default rules and categories (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27877">#27877</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-async</code>] Detect blocking generic HTTP requests
(<code>ASYNC210</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28024">#28024</a>)</li>
<li>[<code>flake8-datetimez</code>] Allow timezone-safe
<code>strptime</code> chains (<code>DTZ007</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28023">#28023</a>)</li>
<li>[<code>flake8-simplify</code>] Respect side effects in
<code>lambda</code> defaults (<code>SIM401</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/28000">#28000</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Fix duplicated &quot;of&quot; in <code>ClientOptions</code> doc
comment (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27978">#27978</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Document rule acceptance guidelines (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27910">#27910</a>)</li>
<li>Document the new category selectors (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27906">#27906</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li>
<li><a href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li>
<li><a
href="https://github.com/jelle-openai"><code>@​jelle-openai</code></a></li>
<li><a
href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a
href="https://github.com/aarushkandukoori"><code>@​aarushkandukoori</code></a></li>
</ul>
<h2>0.16.4</h2>
<p>Released on 2026-08-20.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>flake8-use-pathlib</code>] Add autofix for
<code>PTH116</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26460">#26460</a>)</li>
<li>[<code>refurb</code>] Restrict <code>delete-full-slice</code> to
lists (<code>FURB131</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27711">#27711</a>)</li>
<li>[<code>refurb</code>] Skip <code>FURB101</code> and
<code>FURB103</code> when the <code>open</code> argument is a file
descriptor (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27643">#27643</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Fix <code>InvalidInstruction</code> on Windows CPUs that do not
support <code>POPCNT</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27803">#27803</a>)</li>
<li>[<code>pyflakes</code>] Emit semantic syntax errors in string type
definitions as <code>F722</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27835">#27835</a>)</li>
<li>[<code>pylint</code>] Allow <code>os._exit</code> imports in
<code>import-private-name</code> (<code>PLC2701</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27738">#27738</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/astral-sh/ruff/commit/9e4938c4a60bed3e87a11ee1e1db1bd23f4d964a"><code>9e4938c</code></a>
Bump 0.16.5 (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28110">#28110</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/aad0e909ef1390f4b2a3ba8aa0a67fb8ea5cbacd"><code>aad0e90</code></a>
Allow rules without codes (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28049">#28049</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/5fdab73c5052350400c36b08c5d7710210343bc4"><code>5fdab73</code></a>
Update preview default rules and categories (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27877">#27877</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/29c8e5b2d0a46eb7dc4ff11c1b0a0dc5ccea52e4"><code>29c8e5b</code></a>
Document rule acceptance guidelines (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27910">#27910</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/50a4d7fd106603a5616b01ac3bef3306252b248f"><code>50a4d7f</code></a>
Document the new category selectors (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27906">#27906</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/ada87950ea188f882f69b7bd6e2213a9696e3ee2"><code>ada8795</code></a>
Introduce category selectors (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27666">#27666</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/d8947238863b61922bfc83f07edcc697c1cc07c0"><code>d894723</code></a>
[ty] Infer lambda parameters through callable type aliases (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28109">#28109</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/2685fdebbcf9938736fed8c45886a629f9c99a06"><code>2685fde</code></a>
[ty] Narrow functional enum members in <code>==</code> and
<code>match</code> (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28103">#28103</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/efcffd2178ce62e9951a53d4c50cadc225a0cfec"><code>efcffd2</code></a>
[ty] Intersection simplifications with subtype-related generic
specialization...</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/eb780488037504e11f145ed778654fd8a825028b"><code>eb78048</code></a>
[ty] Bump ecosystem-analyzer for HTML escaping (<a
href="https://redirect.github.com/astral-sh/ruff/issues/28104">#28104</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/astral-sh/ruff/compare/0.16.4...0.16.5">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

```
Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's releases</a>.</em></p>
<blockquote>
<h2>0.16.5</h2>
<h2>Release Notes</h2>
<p>Released on 2026-08-27.</p>
<h3>Preview features</h3>
<ul>
<li>Allow rules without codes (<a href="https://redirect.github.com/astral-sh/ruff/pull/28049">#28049</a>)</li>
<li>Introduce category selectors (<a href="https://redirect.github.com/astral-sh/ruff/pull/27666">#27666</a>)</li>
<li>Update preview default rules and categories (<a href="https://redirect.github.com/astral-sh/ruff/pull/27877">#27877</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-async</code>] Detect blocking generic HTTP requests (<code>ASYNC210</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/28024">#28024</a>)</li>
<li>[<code>flake8-datetimez</code>] Allow timezone-safe <code>strptime</code> chains (<code>DTZ007</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/28023">#28023</a>)</li>
<li>[<code>flake8-simplify</code>] Respect side effects in <code>lambda</code> defaults (<code>SIM401</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/28000">#28000</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Fix duplicated &quot;of&quot; in <code>ClientOptions</code> doc comment (<a href="https://redirect.github.com/astral-sh/ruff/pull/27978">#27978</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Document rule acceptance guidelines (<a href="https://redirect.github.com/astral-sh/ruff/pull/27910">#27910</a>)</li>
<li>Document the new category selectors (<a href="https://redirect.github.com/astral-sh/ruff/pull/27906">#27906</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li>
<li><a href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li>
<li><a href="https://github.com/jelle-openai"><code>@​jelle-openai</code></a></li>
<li><a href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a href="https://github.com/aarushkandukoori"><code>@​aarushkandukoori</code></a></li>
</ul>
<h2>Install ruff 0.16.5</h2>
<h3>Install prebuilt binaries via shell script</h3>
<pre lang="sh"><code>curl --proto '=https' --tlsv1.2 -LsSf https://releases.astral.sh/github/ruff/releases/download/0.16.5/ruff-installer.sh | sh
</code></pre>
<h3>Install prebuilt binaries via powershell script</h3>
<pre lang="sh"><code>powershell -ExecutionPolicy Bypass -c &quot;irm https://releases.astral.sh/github/ruff/releases/download/0.16.5/ruff-installer.ps1 | iex&quot;
</code></pre>
<h2>Download ruff 0.16.5</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
<blockquote>
<h2>0.16.5</h2>
<p>Released on 2026-08-27.</p>
<h3>Preview features</h3>
<ul>
<li>Allow rules without codes (<a href="https://redirect.github.com/astral-sh/ruff/pull/28049">#28049</a>)</li>
<li>Introduce category selectors (<a href="https://redirect.github.com/astral-sh/ruff/pull/27666">#27666</a>)</li>
<li>Update preview default rules and categories (<a href="https://redirect.github.com/astral-sh/ruff/pull/27877">#27877</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-async</code>] Detect blocking generic HTTP requests (<code>ASYNC210</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/28024">#28024</a>)</li>
<li>[<code>flake8-datetimez</code>] Allow timezone-safe <code>strptime</code> chains (<code>DTZ007</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/28023">#28023</a>)</li>
<li>[<code>flake8-simplify</code>] Respect side effects in <code>lambda</code> defaults (<code>SIM401</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/28000">#28000</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Fix duplicated &quot;of&quot; in <code>ClientOptions</code> doc comment (<a href="https://redirect.github.com/astral-sh/ruff/pull/27978">#27978</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Document rule acceptance guidelines (<a href="https://redirect.github.com/astral-sh/ruff/pull/27910">#27910</a>)</li>
<li>Document the new category selectors (<a href="https://redirect.github.com/astral-sh/ruff/pull/27906">#27906</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li>
<li><a href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li>
<li><a href="https://github.com/jelle-openai"><code>@​jelle-openai</code></a></li>
<li><a href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a href="https://github.com/aarushkandukoori"><code>@​aarushkandukoori</code></a></li>
</ul>
<h2>0.16.4</h2>
<p>Released on 2026-08-20.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>flake8-use-pathlib</code>] Add autofix for <code>PTH116</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/26460">#26460</a>)</li>
<li>[<code>refurb</code>] Restrict <code>delete-full-slice</code> to lists (<code>FURB131</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27711">#27711</a>)</li>
<li>[<code>refurb</code>] Skip <code>FURB101</code> and <code>FURB103</code> when the <code>open</code> argument is a file descriptor (<a href="https://redirect.github.com/astral-sh/ruff/pull/27643">#27643</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Fix <code>InvalidInstruction</code> on Windows CPUs that do not support <code>POPCNT</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/27803">#27803</a>)</li>
<li>[<code>pyflakes</code>] Emit semantic syntax errors in string type definitions as <code>F722</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/27835">#27835</a>)</li>
<li>[<code>pylint</code>] Allow <code>os._exit</code> imports in <code>import-private-name</code> (<code>PLC2701</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27738">#27738</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/astral-sh/ruff/commit/9e4938c4a60bed3e87a11ee1e1db1bd23f4d964a"><code>9e4938c</code></a> Bump 0.16.5 (<a href="https://redirect.github.com/astral-sh/ruff/issues/28110">#28110</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/aad0e909ef1390f4b2a3ba8aa0a67fb8ea5cbacd"><code>aad0e90</code></a> Allow rules without codes (<a href="https://redirect.github.com/astral-sh/ruff/issues/28049">#28049</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/5fdab73c5052350400c36b08c5d7710210343bc4"><code>5fdab73</code></a> Update preview default rules and categories (<a href="https://redirect.github.com/astral-sh/ruff/issues/27877">#27877</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/29c8e5b2d0a46eb7dc4ff11c1b0a0dc5ccea52e4"><code>29c8e5b</code></a> Document rule acceptance guidelines (<a href="https://redirect.github.com/astral-sh/ruff/issues/27910">#27910</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/50a4d7fd106603a5616b01ac3bef3306252b248f"><code>50a4d7f</code></a> Document the new category selectors (<a href="https://redirect.github.com/astral-sh/ruff/issues/27906">#27906</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/ada87950ea188f882f69b7bd6e2213a9696e3ee2"><code>ada8795</code></a> Introduce category selectors (<a href="https://redirect.github.com/astral-sh/ruff/issues/27666">#27666</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/d8947238863b61922bfc83f07edcc697c1cc07c0"><code>d894723</code></a> [ty] Infer lambda parameters through callable type aliases (<a href="https://redirect.github.com/astral-sh/ruff/issues/28109">#28109</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/2685fdebbcf9938736fed8c45886a629f9c99a06"><code>2685fde</code></a> [ty] Narrow functional enum members in <code>==</code> and <code>match</code> (<a href="https://redirect.github.com/astral-sh/ruff/issues/28103">#28103</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/efcffd2178ce62e9951a53d4c50cadc225a0cfec"><code>efcffd2</code></a> [ty] Intersection simplifications with subtype-related generic specialization...</li>
<li><a href="https://github.com/astral-sh/ruff/commit/eb780488037504e11f145ed778654fd8a825028b"><code>eb78048</code></a> [ty] Bump ecosystem-analyzer for HTML escaping (<a href="https://redirect.github.com/astral-sh/ruff/issues/28104">#28104</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.16.4...0.16.5">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>
```

---

## build(deps): update cryptography requirement from >=50.0.0 to >=50.0.1 in /services/claw-interface (#3656)

- **SHA**: `973f0fb8fd6a8de573cd9efdab3b082c20c6a47a`
- **作者**: dependabot[bot]
- **日期**: 2026-09-10T03:30:57Z
- **PR**: #3656

### Commit Message

```
build(deps): update cryptography requirement from >=50.0.0 to >=50.0.1 in /services/claw-interface (#3656)

Updates the requirements on
[cryptography](https://github.com/pyca/cryptography) to permit the
latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst">cryptography's
changelog</a>.</em></p>
<blockquote>
<p>50.0.1 - 2026-08-25</p>
<pre><code>
* Updated Windows, macOS, and Linux wheels to be compiled with OpenSSL
4.0.2.
<p>.. _v50-0-0:</p>
<p>50.0.0 - 2026-07-31<br />
</code></pre></p>
<ul>
<li><strong>SECURITY ISSUE</strong>:

:func:<code>~cryptography.hazmat.primitives.serialization.pkcs7.pkcs7_decrypt_der</code>
and its PEM and S/MIME variants no longer expose distinguishable errors
or
timing when unwrapping a <code>RecipientInfo</code>'s
<code>encryptedKey</code>, which could
act as a Bleichenbacher oracle for callers that decrypt untrusted
messages.
A random key is now substituted on failure, as described in
:rfc:<code>3218</code>.
Credit to <strong><a
href="https://github.com/X1AOxiang"><code>@​X1AOxiang</code></a></strong>
for reporting the issue. <strong>CVE-2026-69247</strong></li>
<li>Deprecated Diffie-Hellman key exchange over finite fields (FFDH).
Everything FFDH is deprecated, including the types in
<code>cryptography.hazmat.primitives.asymmetric.dh</code> and loading
FFDH keys or
parameters with the key loading APIs. Users should migrate to a more
modern key exchange algorithm.</li>
<li>Added <code>xof()</code> class methods to
:class:<code>~cryptography.hazmat.primitives.hashes.SHAKE128</code> and
:class:<code>~cryptography.hazmat.primitives.hashes.SHAKE256</code> for
constructing
algorithm instances configured for use with
:class:<code>~cryptography.hazmat.primitives.hashes.XOFHash</code>.</li>
<li>The :mod:<code>X.509 verification
&lt;cryptography.x509.verification&gt;</code> APIs are now
considered stable and are subject to our API stability policy.</li>
<li>Added the :doc:<code>/cobblestone</code> recipe, an implementation
of the
Cobblestone-128 and Cobblestone-256 instantiations of the <code>C2SP
chunked-encryption specification
&lt;https://c2sp.org/chunked-encryption&gt;</code>_ for streaming
authenticated
encryption of large messages.</li>
<li>Parsing a Signed Certificate Timestamp list now rejects encodings
that
carry trailing bytes after the list or after an individual SCT, instead
of
silently ignoring them.</li>
<li>Added support for using :class:<code>~cryptography.x509.Name</code>
as a field type in
the :doc:<code>/hazmat/asn1/index</code> module.</li>
<li>Loading a public key or an EC private key now rejects DER where the
<code>subjectPublicKey</code> (or EC <code>publicKey</code>) <code>BIT
STRING</code> declares a non-zero
number of unused bits, instead of silently ignoring it.</li>
<li>Parsing a CRL entry's <code>InvalidityDate</code> extension now
rejects a
<code>GeneralizedTime</code> that carries fractional seconds or another
non-DER form,
matching the strict encoding already required for every other X.509 time
field.</li>
<li>:func:<code>~cryptography.x509.ocsp.load_der_ocsp_request</code> and
:func:<code>~cryptography.x509.ocsp.load_der_ocsp_response</code> now
reject a request
or response whose <code>version</code> field is not <code>v1</code>, the
only version defined
by RFC 6960, matching the version validation already performed when
loading</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/pyca/cryptography/commit/ffde75a2b594822c740a2e4748b56c00548302bf"><code>ffde75a</code></a>
bump for 50.0.1 + changelog (<a
href="https://redirect.github.com/pyca/cryptography/issues/15520">#15520</a>)</li>
<li>See full diff in <a
href="https://github.com/pyca/cryptography/compare/50.0.0...50.0.1">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

```
Updates the requirements on [cryptography](https://github.com/pyca/cryptography) to permit the latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst">cryptography's changelog</a>.</em></p>
<blockquote>
<p>50.0.1 - 2026-08-25</p>
<pre><code>
* Updated Windows, macOS, and Linux wheels to be compiled with OpenSSL 4.0.2.
<p>.. _v50-0-0:</p>
<p>50.0.0 - 2026-07-31<br />
</code></pre></p>
<ul>
<li><strong>SECURITY ISSUE</strong>:
:func:<code>~cryptography.hazmat.primitives.serialization.pkcs7.pkcs7_decrypt_der</code>
and its PEM and S/MIME variants no longer expose distinguishable errors or
timing when unwrapping a <code>RecipientInfo</code>'s <code>encryptedKey</code>, which could
act as a Bleichenbacher oracle for callers that decrypt untrusted messages.
A random key is now substituted on failure, as described in :rfc:<code>3218</code>.
Credit to <strong><a href="https://github.com/X1AOxiang"><code>@​X1AOxiang</code></a></strong> for reporting the issue. <strong>CVE-2026-69247</strong></li>
<li>Deprecated Diffie-Hellman key exchange over finite fields (FFDH).
Everything FFDH is deprecated, including the types in
<code>cryptography.hazmat.primitives.asymmetric.dh</code> and loading FFDH keys or
parameters with the key loading APIs. Users should migrate to a more
modern key exchange algorithm.</li>
<li>Added <code>xof()</code> class methods to
:class:<code>~cryptography.hazmat.primitives.hashes.SHAKE128</code> and
:class:<code>~cryptography.hazmat.primitives.hashes.SHAKE256</code> for constructing
algorithm instances configured for use with
:class:<code>~cryptography.hazmat.primitives.hashes.XOFHash</code>.</li>
<li>The :mod:<code>X.509 verification &lt;cryptography.x509.verification&gt;</code> APIs are now
considered stable and are subject to our API stability policy.</li>
<li>Added the :doc:<code>/cobblestone</code> recipe, an implementation of the
Cobblestone-128 and Cobblestone-256 instantiations of the <code>C2SP chunked-encryption specification &lt;https://c2sp.org/chunked-encryption&gt;</code>_ for streaming authenticated
encryption of large messages.</li>
<li>Parsing a Signed Certificate Timestamp list now rejects encodings that
carry trailing bytes after the list or after an individual SCT, instead of
silently ignoring them.</li>
<li>Added support for using :class:<code>~cryptography.x509.Name</code> as a field type in
the :doc:<code>/hazmat/asn1/index</code> module.</li>
<li>Loading a public key or an EC private key now rejects DER where the
<code>subjectPublicKey</code> (or EC <code>publicKey</code>) <code>BIT STRING</code> declares a non-zero
number of unused bits, instead of silently ignoring it.</li>
<li>Parsing a CRL entry's <code>InvalidityDate</code> extension now rejects a
<code>GeneralizedTime</code> that carries fractional seconds or another non-DER form,
matching the strict encoding already required for every other X.509 time
field.</li>
<li>:func:<code>~cryptography.x509.ocsp.load_der_ocsp_request</code> and
:func:<code>~cryptography.x509.ocsp.load_der_ocsp_response</code> now reject a request
or response whose <code>version</code> field is not <code>v1</code>, the only version defined
by RFC 6960, matching the version validation already performed when loading</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/pyca/cryptography/commit/ffde75a2b594822c740a2e4748b56c00548302bf"><code>ffde75a</code></a> bump for 50.0.1 + changelog (<a href="https://redirect.github.com/pyca/cryptography/issues/15520">#15520</a>)</li>
<li>See full diff in <a href="https://github.com/pyca/cryptography/compare/50.0.0...50.0.1">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>
```

---

