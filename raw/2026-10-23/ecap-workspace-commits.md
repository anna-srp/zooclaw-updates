# SerendipityOneInc/ecap-workspace — commits 2026-10-23

## fix(platform): show usage in the preferred display time zone (#4127)

- **SHA**: `07a445147eb1259301470d138d897d7d95650a09`
- **作者**: david-srp
- **日期**: 2026-10-23T16:44:22Z
- **PR**: #4127

### Commit Message

```
fix(platform): show usage in the preferred display time zone (#4127)

## Summary

Usage currently forces UTC while the rest of Platform commonly displays
device-local times. A user in UTC+08:00 sees an event at `Oct 22, 17:58`
instead of their local `Oct 23, 01:58`.

- Default Usage display to the device time zone, with UTC offsets in the
table header, range boundaries and As of timestamp. Show a historical
record's own offset when it differs across DST; retain the source
datetime and UTC tooltip.
- Add a basic Time zone selector to Account settings: Follow system, UTC
and browser-supported IANA zones. Remember manual choices per verified
user in this browser; Follow system clears the override. Handle
blocked/invalid storage and refresh device detection on
focus/visibility.
- Keep supported time-zone options in stable order and reuse
timestamp/offset formatters per zone, preserving event-date DST offsets.
- Keep API queries in UTC and preserve totals, cache keys, snapshots and
loaded pages. No backend, billing calculation, Billing-page or Webhooks
changes. Preferences do not sync across devices.

## Root cause

The Usage formatter and labels hard-code UTC, with no display
preference. This change only converts timestamps for presentation; it
does not shift event instants or alter the reporting window.

## Test plan

- [x] Node 24 / pinned pnpm 10.26.2: Platform lint, typecheck and
production build.
- [x] 29 targeted tests passed across formatting, preference provider,
Usage and Account navigation (125 unrelated router tests intentionally
skipped locally).
- [x] Verify Shanghai midnight rollover, India/Nepal fractional offsets,
New York DST repeated hours, persistence/reset, per-user isolation and
blocked/invalid storage.
- [x] Verify changing display zone leaves requests in UTC, totals
unchanged and loaded pagination intact.
- [x] Existing local fixture preview: desktop Usage, mobile Account
settings, UTC selection survives reload, Follow system restores
UTC+08:00, no browser console errors.

Local UI checks use sample data; production/staging business services
were not exercised. CI runs the full Platform suite. Screenshots are
retained locally under `.screenshots/` and are not committed.

---------

Co-authored-by: david-srp <264104338+david-srp@users.noreply.github.com>
```

### PR Body

## Summary

Usage currently forces UTC while the rest of Platform commonly displays device-local times. A user in UTC+08:00 sees an event at `Oct 22, 17:58` instead of their local `Oct 23, 01:58`.

- Default Usage display to the device time zone, with UTC offsets in the table header, range boundaries and As of timestamp. Show a historical record's own offset when it differs across DST; retain the source datetime and UTC tooltip.
- Add a basic Time zone selector to Account settings: Follow system, UTC and browser-supported IANA zones. Remember manual choices per verified user in this browser; Follow system clears the override. Handle blocked/invalid storage and refresh device detection on focus/visibility.
- Keep supported time-zone options in stable order and reuse timestamp/offset formatters per zone, preserving event-date DST offsets.
- Keep API queries in UTC and preserve totals, cache keys, snapshots and loaded pages. No backend, billing calculation, Billing-page or Webhooks changes. Preferences do not sync across devices.

## Root cause

The Usage formatter and labels hard-code UTC, with no display preference. This change only converts timestamps for presentation; it does not shift event instants or alter the reporting window.

## Test plan

- [x] Node 24 / pinned pnpm 10.26.2: Platform lint, typecheck and production build.
- [x] 29 targeted tests passed across formatting, preference provider, Usage and Account navigation (125 unrelated router tests intentionally skipped locally).
- [x] Verify Shanghai midnight rollover, India/Nepal fractional offsets, New York DST repeated hours, persistence/reset, per-user isolation and blocked/invalid storage.
- [x] Verify changing display zone leaves requests in UTC, totals unchanged and loaded pagination intact.
- [x] Existing local fixture preview: desktop Usage, mobile Account settings, UTC selection survives reload, Follow system restores UTC+08:00, no browser console errors.

Local UI checks use sample data; production/staging business services were not exercised. CI runs the full Platform suite. Screenshots are retained locally under `.screenshots/` and are not committed.



---

## refactor(agents): provision only native runtime identities (#4134)

- **SHA**: `bb8b4ca6402657cfb2b748347074dc1fc1d97d00`
- **作者**: kaka-srp
- **日期**: 2026-10-23T12:01:51Z
- **PR**: #4134

### Commit Message

```
refactor(agents): provision only native runtime identities (#4134)

Managed Work and Platform Agents now always provision and resume their
native runtime identity. Remove the Engine login-JWT credential writer
and per-Agent mode selection; creation, reinstall, billing-key
provisioning and resource policy initialization use the existing native
handoff and revocation paths.

Login/Cookie/OAuth, Work service-token authentication, Platform API keys
and billing JWT ciphertext are unchanged. `USER_INTERNAL_TOKEN` remains
a sandbox alias for the runtime credential. Coordinated Engine cleanup
and schema contraction:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/2096. No
deployment is performed here.

Validation: `scripts/verify-py.sh` passed (Ruff/format, Pyright
app+tests and import contracts); 421 related unit tests and 90
authentication regression tests passed. The suites overlap; these are
separate runs, not a combined unique-test count.

Updated baseline/template/service-proxy, BDD and local Build-harness
fixtures to use the native credential contract; local Engine-only
fixtures carry no CI business authority. An additional 166 affected
fixture tests passed. Local BDD needs MongoDB and was skipped; GitHub CI
runs the database-backed suite.

Ordinary start only resumes a credential already registered in CI; a
missing registry entry returns `agent.credentials_not_ready` without
issuing identity or implicitly migrating resources/MCP configuration.
New creation and explicit reinstall retain the full
policy/projection-first provisioning path. A real Work-token HTTP
regression covers an unmigrated Agent with no projection and a legacy
managed-identity MCP; existing prepared handoff recovery remains
covered. The new guard also passes a one-line negative control (one
intended failure when removed, restored green).


Local Astra review of the complete coordinated branches found no CI
production defect. It also covered the final BDD fixture correction,
which mocks identity refresh at the lifecycle boundary rather than
globally mocking the credential registry. Four focused CI
credential/handoff/projection/Work-auth files passed 40 tests during the
review. Full CI passed on the preceding revision; the final fixture-only
commit will rerun CI. No merge or deployment is included.
```

### PR Body

Managed Work and Platform Agents now always provision and resume their native runtime identity. Remove the Engine login-JWT credential writer and per-Agent mode selection; creation, reinstall, billing-key provisioning and resource policy initialization use the existing native handoff and revocation paths.

Login/Cookie/OAuth, Work service-token authentication, Platform API keys and billing JWT ciphertext are unchanged. `USER_INTERNAL_TOKEN` remains a sandbox alias for the runtime credential. Coordinated Engine cleanup and schema contraction: https://github.com/SerendipityOneInc/zooclaw-engine/pull/2096. No deployment is performed here.

Validation: `scripts/verify-py.sh` passed (Ruff/format, Pyright app+tests and import contracts); 421 related unit tests and 90 authentication regression tests passed. The suites overlap; these are separate runs, not a combined unique-test count.

Updated baseline/template/service-proxy, BDD and local Build-harness fixtures to use the native credential contract; local Engine-only fixtures carry no CI business authority. An additional 166 affected fixture tests passed. Local BDD needs MongoDB and was skipped; GitHub CI runs the database-backed suite.

Ordinary start only resumes a credential already registered in CI; a missing registry entry returns `agent.credentials_not_ready` without issuing identity or implicitly migrating resources/MCP configuration. New creation and explicit reinstall retain the full policy/projection-first provisioning path. A real Work-token HTTP regression covers an unmigrated Agent with no projection and a legacy managed-identity MCP; existing prepared handoff recovery remains covered. The new guard also passes a one-line negative control (one intended failure when removed, restored green).


Local Astra review of the complete coordinated branches found no CI production defect. It also covered the final BDD fixture correction, which mocks identity refresh at the lifecycle boundary rather than globally mocking the credential registry. Four focused CI credential/handoff/projection/Work-auth files passed 40 tests during the review. Full CI passed on the preceding revision; the final fixture-only commit will rerun CI. No merge or deployment is included.


---

## fix(chat): attach composer uploads as Mattermost files in session threads (#4132)

- **SHA**: `9a8b2b7e7b03fbfee0009408e6e49f1827ef296a`
- **作者**: engineering-agent-srp
- **日期**: 2026-10-23T10:36:12Z
- **PR**: #4132

### Commit Message

```
fix(chat): attach composer uploads as Mattermost files in session threads (#4132)

## Problem

A customer's agent (ULTRA_1 / `agt_01m27r804mg5k7jnjrjyfhbzdw`) could
not see screenshots sent from the web session thread. The engine
received the posts with **0 attachments**, and the agent's `image` fetch
of the pasted link got R2 `401 Unauthorized`.

## Root cause

`GenClawInput` only uploads composer files as Mattermost files when
`uploadOverride` is passed. Otherwise it falls back to uploading into
the R2 user-image bucket and inserting `![image.png](<7-day presigned
GET URL>)` (~460 chars) into the message text.

- `ChatBody` (main `/chat`) passes `uploadOverride` while MM is
connected.
- `SessionThreadClient` (`/chat/{workspaceId}/sessions/{sessionId}`) and
`AgentWorkspaceClient` (`/agents/{workspaceId}` task/build) never wired
`useMmAttachments`, so **every** image from these surfaces goes down the
link fallback.

The agent then has to hand-copy the presigned URL into a tool call. The
engine already documents that models garble these (`media-inputs.ts`,
`r2://` short reference, #292). A corrupted `X-Amz-Credential` access
key gives R2 401, which matches the agent's report. (The exact URL the
agent used was not captured; this part is inferred.)

## Fix

- `useSessionThreadChat` now owns a `useMmAttachments` instance bound to
the thread channel and the user's MM token. It exposes
`composerAttachments` (`uploadOverride`, `attachExistingFile`,
`mmAttachments`, remove/retry, `isMmUploading`).
- `sendThreadMessage` sends only finished uploads still shown in the
composer as `file_ids` (same filtering as
`useChatMessaging.sendMMMessage`). It clears the composer on success and
keeps the ids for retry on failure or a no-op send.
- `useSendThreadReply.send` / `postThreadReply` accept image-only
replies when file ids are present. The composer already enables Send for
attachments with no text.
- Wired into `SessionThreadClient` and `AgentWorkspaceClient`. Read-only
Legacy and External surfaces are unchanged.
- `hasRevision` / `canEditDefinition` moved to
`lib/revision-presentation.ts` with no behavior change, to keep
`useViewModel.ts` under the 600-line limit.

## Verification

- New tests fail on `main` (4) and pass with this change:
- `useSessionThreadChat`: exposes `uploadOverride`; sends file ids,
including image-only; clears on success; keeps ids on failure.
  - `useSendThreadReply`: forwards file ids, image-only.
  - `postThreadReply`: image-only reply with file ids.
- `scripts/verify-web.sh <changed files>`: guards ✓, vitest 191 ✓,
eslint ✓. Also `tests/unit/app/agents`: 542 ✓.
- ⚠️ `tsc --noEmit` could not finish locally (OOM in a small sandbox).
Relying on CI `web-quality`.
- Not yet validated in a browser or on staging. After deploy: send a
screenshot from a session thread, then confirm the post has `file_ids`
and the engine inbound message has 1 attachment.

## Notes

- Mattermost retirement is in progress but not on `main`. This is a
small fix on the current transport.
- Follow-up options not in this PR: `SubagentChatPanel` still always
uses the link fallback. A server-side "own-bucket presigned link →
attachment" path in ACS or the engine would remove the copy-the-URL
dependency regardless of transport.

---------

Co-authored-by: zoowork-engineering-agent <326424865+zoowork-engineering-agent@users.noreply.github.com>
Co-authored-by: finn-srp <finn@srp.one>
Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

## Problem

A customer's agent (ULTRA_1 / `agt_01m27r804mg5k7jnjrjyfhbzdw`) could not see screenshots sent from the web session thread. The engine received the posts with **0 attachments**, and the agent's `image` fetch of the pasted link got R2 `401 Unauthorized`.

## Root cause

`GenClawInput` only uploads composer files as Mattermost files when `uploadOverride` is passed. Otherwise it falls back to uploading into the R2 user-image bucket and inserting `![image.png](<7-day presigned GET URL>)` (~460 chars) into the message text.

- `ChatBody` (main `/chat`) passes `uploadOverride` while MM is connected.
- `SessionThreadClient` (`/chat/{workspaceId}/sessions/{sessionId}`) and `AgentWorkspaceClient` (`/agents/{workspaceId}` task/build) never wired `useMmAttachments`, so **every** image from these surfaces goes down the link fallback.

The agent then has to hand-copy the presigned URL into a tool call. The engine already documents that models garble these (`media-inputs.ts`, `r2://` short reference, #292). A corrupted `X-Amz-Credential` access key gives R2 401, which matches the agent's report. (The exact URL the agent used was not captured; this part is inferred.)

## Fix

- `useSessionThreadChat` now owns a `useMmAttachments` instance bound to the thread channel and the user's MM token. It exposes `composerAttachments` (`uploadOverride`, `attachExistingFile`, `mmAttachments`, remove/retry, `isMmUploading`).
- `sendThreadMessage` sends only finished uploads still shown in the composer as `file_ids` (same filtering as `useChatMessaging.sendMMMessage`). It clears the composer on success and keeps the ids for retry on failure or a no-op send.
- `useSendThreadReply.send` / `postThreadReply` accept image-only replies when file ids are present. The composer already enables Send for attachments with no text.
- Wired into `SessionThreadClient` and `AgentWorkspaceClient`. Read-only Legacy and External surfaces are unchanged.
- `hasRevision` / `canEditDefinition` moved to `lib/revision-presentation.ts` with no behavior change, to keep `useViewModel.ts` under the 600-line limit.

## Verification

- New tests fail on `main` (4) and pass with this change:
  - `useSessionThreadChat`: exposes `uploadOverride`; sends file ids, including image-only; clears on success; keeps ids on failure.
  - `useSendThreadReply`: forwards file ids, image-only.
  - `postThreadReply`: image-only reply with file ids.
- `scripts/verify-web.sh <changed files>`: guards ✓, vitest 191 ✓, eslint ✓. Also `tests/unit/app/agents`: 542 ✓.
- ⚠️ `tsc --noEmit` could not finish locally (OOM in a small sandbox). Relying on CI `web-quality`.
- Not yet validated in a browser or on staging. After deploy: send a screenshot from a session thread, then confirm the post has `file_ids` and the engine inbound message has 1 attachment.

## Notes

- Mattermost retirement is in progress but not on `main`. This is a small fix on the current transport.
- Follow-up options not in this PR: `SubagentChatPanel` still always uses the link fallback. A server-side "own-bucket presigned link → attachment" path in ACS or the engine would remove the copy-the-URL dependency regardless of transport.


---

## feat: qualify business contact submissions (#4130)

- **SHA**: `19dd49fe757d63088222889297ec163c8a118b2e`
- **作者**: Shirley151515
- **日期**: 2026-10-23T08:41:51Z
- **PR**: #4130

### Commit Message

```
feat: qualify business contact submissions (#4130)

## Summary

Enterprise contact submissions now accept optional business details up
to 5,000 characters, with revised copy across all 10 locales. Chinese
and English prompts invite workflows, challenges, goals and systems to
connect.

The API rejects public/personal and disposable email providers using the
MIT-licensed Kikobeats/free-email-domains snapshot (31,097 domains;
commit 18d04cbaa077cca754e129a417fbdf780dea332a). Validation normalizes
case and IDNA, matches bulk entries exactly and only inherits blocking
for explicit provider-owned namespaces and runs before lead logging or
Feishu notification. The browser displays a localized email error and
retains the other fields for correction. The domain dataset stays on the
backend, with no runtime external lookup or browser bundle overhead.

## Validation

- 67 backend contact tests passed, including direct API rejection,
uppercase/subdomain/Unicode bypass cases, allowed custom domains,
notification behavior and the 5,000/5,001-character boundary.
- 89 frontend tests passed: all six business-page suites and both
API/error-handling suites.
- Full web/app TypeScript check passed; targeted ESLint, Ruff and
formatting checks passed.
- Web governance guards passed (cache guard reports its existing
bootstrap condition).
- Actual Next.js local page + isolated real FastAPI route: Gmail and
Mailinator rejected; corrected company-domain submission succeeded. Test
webhook disabled.

Previous head `8d13ec16bd161c0687b74d261be9d728501fcc53`: GitHub CI
completed with 28 passing checks, 14 conditional skips, no failures or
pending checks. This includes web build, frontend/backend test and
lint/typecheck jobs, CodeQL and automated reviews.

## Dataset size and deployment

The third-party domain snapshot contributes 31,098 lines to this PR; its
original formatting, MIT license, pinned revision and update
instructions are retained for auditability. The size exception is solely
for this vendored dataset.

Deploy and verify the compatible backend FIRST, then deploy the
frontend. Do not deploy the new frontend against the old backend; on
rollback, revert the frontend first. The existing backend image copies
the app directory, including the dataset. New unknown disposable domains
may evade any static list; this snapshot must be periodically reviewed
and updated. A domain absent from the list is not proof of mailbox
ownership or company affiliation.



## Review follow-up

`f9f8053` fixes shared-registration-domain false positives and bounds
the serialized Feishu notification to 20,000 UTF-8 bytes. Full Chinese
descriptions at 5,000 characters fit; oversized notification text is
explicitly truncated without changing the original submission. New
regression coverage includes Chinese, emoji and JSON escaping. CI for
`f9f8053827332ba4c9fd0d57b1ee1d501bcaf307` completed: 28 passing checks,
14 conditional skips, zero failures or pending checks. Frontend/backend
complete test suites, typechecks and build passed. The Codex review job
may skip content review because of dataset size; human re-review by
tim-srp remains requested.

---------

Co-authored-by: 15 <s15@15deMacBook-Pro.local>
```

### PR Body

## Summary

Enterprise contact submissions now accept optional business details up to 5,000 characters, with revised copy across all 10 locales. Chinese and English prompts invite workflows, challenges, goals and systems to connect.

The API rejects public/personal and disposable email providers using the MIT-licensed Kikobeats/free-email-domains snapshot (31,097 domains; commit 18d04cbaa077cca754e129a417fbdf780dea332a). Validation normalizes case and IDNA, matches bulk entries exactly and only inherits blocking for explicit provider-owned namespaces and runs before lead logging or Feishu notification. The browser displays a localized email error and retains the other fields for correction. The domain dataset stays on the backend, with no runtime external lookup or browser bundle overhead.

## Validation

- 67 backend contact tests passed, including direct API rejection, uppercase/subdomain/Unicode bypass cases, allowed custom domains, notification behavior and the 5,000/5,001-character boundary.
- 89 frontend tests passed: all six business-page suites and both API/error-handling suites.
- Full web/app TypeScript check passed; targeted ESLint, Ruff and formatting checks passed.
- Web governance guards passed (cache guard reports its existing bootstrap condition).
- Actual Next.js local page + isolated real FastAPI route: Gmail and Mailinator rejected; corrected company-domain submission succeeded. Test webhook disabled.

Previous head `8d13ec16bd161c0687b74d261be9d728501fcc53`: GitHub CI completed with 28 passing checks, 14 conditional skips, no failures or pending checks. This includes web build, frontend/backend test and lint/typecheck jobs, CodeQL and automated reviews.

## Dataset size and deployment

The third-party domain snapshot contributes 31,098 lines to this PR; its original formatting, MIT license, pinned revision and update instructions are retained for auditability. The size exception is solely for this vendored dataset.

Deploy and verify the compatible backend FIRST, then deploy the frontend. Do not deploy the new frontend against the old backend; on rollback, revert the frontend first. The existing backend image copies the app directory, including the dataset. New unknown disposable domains may evade any static list; this snapshot must be periodically reviewed and updated. A domain absent from the list is not proof of mailbox ownership or company affiliation.



## Review follow-up

`f9f8053` fixes shared-registration-domain false positives and bounds the serialized Feishu notification to 20,000 UTF-8 bytes. Full Chinese descriptions at 5,000 characters fit; oversized notification text is explicitly truncated without changing the original submission. New regression coverage includes Chinese, emoji and JSON escaping. CI for `f9f8053827332ba4c9fd0d57b1ee1d501bcaf307` completed: 28 passing checks, 14 conditional skips, zero failures or pending checks. Frontend/backend complete test suites, typechecks and build passed. The Codex review job may skip content review because of dataset size; human re-review by tim-srp remains requested.


---

## feat(claw-interface): serve Work service tokens on the service-API LLM gateway (#4129)

- **SHA**: `bc775898554a72788a7af478a8657d97d023368c`
- **作者**: tim-srp
- **日期**: 2026-10-23T07:28:07Z
- **PR**: #4129

### Commit Message

```
feat(claw-interface): serve Work service tokens on the service-API LLM gateway (#4129)

## Summary

Follow-up to #4128. `/service/v1/llm/models` and
`/service/v1/llm/chat/completions` returned `404 service_api.not_found`
for `zct_` Work service tokens, so a managed-agent key created in
ZooWork Work could not call models directly (for example from the
ZooWork desktop).

- A `zct_` token now gets its bound member's own Billing Profile key
(`llm_gateway.resolve_billing_key`). That is the same key and payer as
the member's web usage and `/llm/v1`.
- The call is refused with `409 llm.billing_owner_mismatch` unless the
member's current organization is the token's organization, so a token
can never bill a different org.
- `zwp_live_` Platform keys are unchanged and keep the organization
payer key.

## Test plan

- [x] `tests/unit/test_service_api_llm.py`: a zct token uses the member
key; a member with no current org or a different org gets 409 before
LiteLLM is called
- [x] Full claw-interface unit suite: 12519 passed, 14 skipped
- [x] `scripts/ci-lint/*.sh`, ruff, pyright clean
- [ ] Staging: `GET /service/v1/llm/models` and a streamed completion
with a staging `zct_` token

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

## Summary

Follow-up to #4128. `/service/v1/llm/models` and `/service/v1/llm/chat/completions` returned `404 service_api.not_found` for `zct_` Work service tokens, so a managed-agent key created in ZooWork Work could not call models directly (for example from the ZooWork desktop).

- A `zct_` token now gets its bound member's own Billing Profile key (`llm_gateway.resolve_billing_key`). That is the same key and payer as the member's web usage and `/llm/v1`.
- The call is refused with `409 llm.billing_owner_mismatch` unless the member's current organization is the token's organization, so a token can never bill a different org.
- `zwp_live_` Platform keys are unchanged and keep the organization payer key.

## Test plan

- [x] `tests/unit/test_service_api_llm.py`: a zct token uses the member key; a member with no current org or a different org gets 409 before LiteLLM is called
- [x] Full claw-interface unit suite: 12519 passed, 14 skipped
- [x] `scripts/ci-lint/*.sh`, ruff, pyright clean
- [ ] Staging: `GET /service/v1/llm/models` and a streamed completion with a staging `zct_` token

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(platform): stop project list auto-retry before the observer disconnects (#4125)

- **SHA**: `d80f8e6e59ed627337c770b331120bdd9f08b3a3`
- **作者**: finn-srp
- **日期**: 2026-10-23T06:51:26Z
- **PR**: #4125

### Commit Message

```
fix(platform): stop project list auto-retry before the observer disconnects (#4125)

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

## Summary

- 修复 #4124：`ProjectSwitcher` 分页的 “stops automatic retries on failure…”
用例在 CI 偶发失败（`loadMoreProjects` 预期调用 1 次，实际 2 次）。只改 `web/app` 的 PR（例如
#4123）也会因为它挂掉 `platform-quality`。
- 这不只是测试问题。组件在加载失败后，存在一个很短的窗口仍然会自动重试，违背了“失败后停止自动重试、等用户点 Retry”的设计。本 PR
修的是组件本身。

## Root cause

`ProjectOptions` 在加载失败后，通过 `useEffect` 的 cleanup 执行
`IntersectionObserver.disconnect()`，以此停止自动加载。但 effect cleanup 在 commit
之后才执行。如果在这之前 observer 回调又触发了，就会调用 `loadNextPage()`。`loadNextPage`
本身不检查“刚刚失败过”，于是又自动请求了一次。

测试里的 `findByRole('Retry loading projects')` 在 DOM 更新后就返回。机器负载高时，旧
observer 的 cleanup 这时还没执行，第二次 `showListEnd()` 正好落在这个窗口里。

修复：用一个同步更新的 ref 记录加载状态（`'idle' | 'pending' | 'failed'`），替代原来的
`requestPending`。状态为 `'failed'` 时，自动加载直接返回；只有用户点 Retry（`loadNextPage({
retry: true })`）才会重新请求。这样不再依赖 effect cleanup 的执行时机。

已知但不在本 PR 范围：成功路径上，`loadMoreProjects` 返回后、provider 的新 cursor 状态 commit
之前，如果再次触发加载，会用旧 cursor 重复请求同一页。provider 的 `appendUnique`
会去重，不会产生错误数据，只是多一次请求。根因在 provider 的 cursor 更新时机，需要单独处理。

## Test plan

- [x] 新增用例：失败前先拿到 observer 回调，失败后再直接调用它，模拟 cleanup 前触发。修复前稳定失败（预期 1 次，实际
2 次），修复后通过。
- [x] 复现与验证：后台并发跑完整测试制造负载，同时把该测试文件反复跑 30 次。修复前失败 1 次，断言与 CI
一致（`project-switcher.test.tsx:92`）；修复后 30 次全部通过。
- [x] 变异检查：去掉 `'failed'` 判断后，新用例失败；恢复后通过。
- [x] rebase 到最新 main 后，在 `web/platform` 依次运行 `pnpm lint`、`pnpm
typecheck`、`pnpm test`（31 个文件、378 个用例）和 `pnpm build`，全部通过。

Fixes #4124

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

## Summary

- 修复 #4124：`ProjectSwitcher` 分页的 “stops automatic retries on failure…” 用例在 CI 偶发失败（`loadMoreProjects` 预期调用 1 次，实际 2 次）。只改 `web/app` 的 PR（例如 #4123）也会因为它挂掉 `platform-quality`。
- 这不只是测试问题。组件在加载失败后，存在一个很短的窗口仍然会自动重试，违背了“失败后停止自动重试、等用户点 Retry”的设计。本 PR 修的是组件本身。

## Root cause

`ProjectOptions` 在加载失败后，通过 `useEffect` 的 cleanup 执行 `IntersectionObserver.disconnect()`，以此停止自动加载。但 effect cleanup 在 commit 之后才执行。如果在这之前 observer 回调又触发了，就会调用 `loadNextPage()`。`loadNextPage` 本身不检查“刚刚失败过”，于是又自动请求了一次。

测试里的 `findByRole('Retry loading projects')` 在 DOM 更新后就返回。机器负载高时，旧 observer 的 cleanup 这时还没执行，第二次 `showListEnd()` 正好落在这个窗口里。

修复：用一个同步更新的 ref 记录加载状态（`'idle' | 'pending' | 'failed'`），替代原来的 `requestPending`。状态为 `'failed'` 时，自动加载直接返回；只有用户点 Retry（`loadNextPage({ retry: true })`）才会重新请求。这样不再依赖 effect cleanup 的执行时机。

已知但不在本 PR 范围：成功路径上，`loadMoreProjects` 返回后、provider 的新 cursor 状态 commit 之前，如果再次触发加载，会用旧 cursor 重复请求同一页。provider 的 `appendUnique` 会去重，不会产生错误数据，只是多一次请求。根因在 provider 的 cursor 更新时机，需要单独处理。

## Test plan

- [x] 新增用例：失败前先拿到 observer 回调，失败后再直接调用它，模拟 cleanup 前触发。修复前稳定失败（预期 1 次，实际 2 次），修复后通过。
- [x] 复现与验证：后台并发跑完整测试制造负载，同时把该测试文件反复跑 30 次。修复前失败 1 次，断言与 CI 一致（`project-switcher.test.tsx:92`）；修复后 30 次全部通过。
- [x] 变异检查：去掉 `'failed'` 判断后，新用例失败；恢复后通过。
- [x] rebase 到最新 main 后，在 `web/platform` 依次运行 `pnpm lint`、`pnpm typecheck`、`pnpm test`（31 个文件、378 个用例）和 `pnpm build`，全部通过。

Fixes #4124

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(agents): preserve runtime owner inventory metadata (#4118)

- **SHA**: `21d1f7a24b83c26cc5a76636d06883705d321aa0`
- **作者**: kaka-srp
- **日期**: 2026-10-23T06:55:49Z
- **PR**: #4118

### Commit Message

```
fix(agents): preserve runtime owner inventory metadata (#4118)

Opaque runtime credentials cannot support the existing product inventory
Skill's owner selector and account inventory while retaining explicit
resource selections. Add a single `metadata=true` view to the existing
Agent list/detail, channel, schedule and conversation GETs. It verifies
the live Work subject, applied projection, current active binding and
active owner/org membership, then returns only the fields the Skill
actually uses. The metadata list supplies authoritative string owner_uid
and account email.

Ordinary four GETs retain their legacy-only gate; JWT responses retain
their original DTO even with the metadata query. Runtime metadata omits
schedule message/spec/delivery/outcome, channel secrets/capabilities,
and conversation title/body/preview. Conversations preserve the existing
chat-only query; build and preview sessions remain excluded. Existing
owner/org target checks remain, and runtime GET list cannot provision an
Agent. No new endpoint, policy model, login capability or mutation is
added.

Validation: 169 related tests pass; full backend Ruff, formatting,
Pyright app/tests and eight import contracts pass. Feature staging at
service-v0.18.45-beta.runtimeinventory.1 verified real public TLS
requests: explicit/legacy own+sibling metadata, foreign-owner/org 404,
ordinary explicit 403, context spoof rejection, nonempty
schedule/conversation redaction, original JWT field retention,
current-head mismatch rejection and revoked-credential 401. The official
Skill code also called this public staging API. No production release or
customer Skill/pin changes.

Related official consumer fix:
https://github.com/SerendipityOneInc/claw-steward/pull/175

## Local review and follow-up validation

Reviewed the complete PR against its main merge base, including
ownership/current-binding authorization, explicit versus legacy resource
selection, DTO redaction, ordinary JWT compatibility, and the real
service/repository call chains.

Resolved the prior conversation-contract finding: the original mock
returned build sessions even though the production query excludes them.
The runtime schema, defensive route filter, test expectations, and spec
now consistently describe the existing chat-only inventory. A new
HTTP-to-repository regression test checks the actual owner/Agent/purpose
query and limit for both runtime and JWT callers, including JWT field
retention with `metadata=true`. The database query and JWT
implementation are unchanged.

- Local regression: 229 tests passed across runtime inventory/reader,
Agent/channel/schedule/conversation routes, and conversation
repository/service tests. The tightened route regression failed before
the fix and passed afterward.
- Full backend static verification passed: Ruff check/format, Pyright
app/tests, and all eight import contracts.
- Targeted re-review of the fix found no remaining actionable findings.
- This follow-up was validated locally; the earlier staging evidence
above predates this follow-up. No new staging deployment, provider
calls, production data changes, or release was performed.
```

### PR Body

Opaque runtime credentials cannot support the existing product inventory Skill's owner selector and account inventory while retaining explicit resource selections. Add a single `metadata=true` view to the existing Agent list/detail, channel, schedule and conversation GETs. It verifies the live Work subject, applied projection, current active binding and active owner/org membership, then returns only the fields the Skill actually uses. The metadata list supplies authoritative string owner_uid and account email.

Ordinary four GETs retain their legacy-only gate; JWT responses retain their original DTO even with the metadata query. Runtime metadata omits schedule message/spec/delivery/outcome, channel secrets/capabilities, and conversation title/body/preview. Conversations preserve the existing chat-only query; build and preview sessions remain excluded. Existing owner/org target checks remain, and runtime GET list cannot provision an Agent. No new endpoint, policy model, login capability or mutation is added.

Validation: 169 related tests pass; full backend Ruff, formatting, Pyright app/tests and eight import contracts pass. Feature staging at service-v0.18.45-beta.runtimeinventory.1 verified real public TLS requests: explicit/legacy own+sibling metadata, foreign-owner/org 404, ordinary explicit 403, context spoof rejection, nonempty schedule/conversation redaction, original JWT field retention, current-head mismatch rejection and revoked-credential 401. The official Skill code also called this public staging API. No production release or customer Skill/pin changes.

Related official consumer fix: https://github.com/SerendipityOneInc/claw-steward/pull/175

## Local review and follow-up validation

Reviewed the complete PR against its main merge base, including ownership/current-binding authorization, explicit versus legacy resource selection, DTO redaction, ordinary JWT compatibility, and the real service/repository call chains.

Resolved the prior conversation-contract finding: the original mock returned build sessions even though the production query excludes them. The runtime schema, defensive route filter, test expectations, and spec now consistently describe the existing chat-only inventory. A new HTTP-to-repository regression test checks the actual owner/Agent/purpose query and limit for both runtime and JWT callers, including JWT field retention with `metadata=true`. The database query and JWT implementation are unchanged.

- Local regression: 229 tests passed across runtime inventory/reader, Agent/channel/schedule/conversation routes, and conversation repository/service tests. The tightened route regression failed before the fix and passed afterward.
- Full backend static verification passed: Ruff check/format, Pyright app/tests, and all eight import contracts.
- Targeted re-review of the fix found no remaining actionable findings.
- This follow-up was validated locally; the earlier staging evidence above predates this follow-up. No new staging deployment, provider calls, production data changes, or release was performed.


---

## fix(marketing): 恢复官网 pricing 分类栏的品牌样式 (#4126)

- **SHA**: `53e5d93ce5b7c184f8fa4b5c831c6d44972904bd`
- **作者**: lynn Zhuang
- **日期**: 2026-10-23T06:36:23Z
- **PR**: #4126

### Commit Message

```
fix(marketing): 恢复官网 pricing 分类栏的品牌样式 (#4126)

## Summary

- 修复官网 pricing 工具与媒体分类栏被设计系统 2.1.0
样式覆盖的问题，恢复与价格卡片同宽的分类栏、紫色选中背景和白色文字；手机端保留三列两行布局。
- 同时恢复页面顶部产品切换栏的全宽布局和品牌下划线。
- pricing 的品牌外观由官网页面管理，使用 Radix Tabs 保留键盘导航、焦点及 ARIA 关联。修改位于 ECAP
官网，独立设计系统仓库与 npm 包无需发布。

## Root cause

共享 Tabs 引入了未放入 CSS layer 的 `.zc-selection-group` / `.zc-selection-item`
规则，优先于官网原有的 Tailwind 工具类。`width: fit-content` 和灰色背景覆盖了官网的全宽白色分类栏；白色
moving indicator 又接管了选中背景，导致紫色选中态失效。

本次让官网两组 Tabs 直接使用现有 Radix 底层组件，在页面内设置品牌样式，不再依赖设计系统的中性 selection
样式。价格、文案和业务导航逻辑保持不变，未回退产品内 Tabs / Segmented。

## Test plan

- [x] 先运行浏览器回归检查复现失败：1440px 下分类栏比内容卡片窄约 494px。
- [x] 修复后 Playwright 6/6 通过：中英文 × 375 / 768 /
1440px；检查实际计算颜色、全宽对齐、各分类内容关联、键盘循环与 End 导航、产品切换及横向溢出。
- [x] pricing 相关单元测试 70/70 通过，包含价格目录、导航、方案展示、翻译完整性与 typography 检查。
- [x] `verify-web.sh --no-test`：治理检查、TypeScript 和改动文件 ESLint
通过；新增独立测试配置后再次运行 TypeScript / ESLint 通过。
- [x] `pnpm install --frozen-lockfile --offline --ignore-scripts`
通过；仅声明工作区已有的 `radix-ui@1.5.0` 为官网直接依赖，没有升级依赖。
- [x] 新视觉测试配置已登记到 Knip 的 Playwright 入口，`knip` 硬门禁与完整 `pnpm lint:ci`
通过。初轮 CI 暴露的两个测试文件未登记问题已修复，未增加任何忽略项。
- [x] 最新提交 `672f3ee2c` 的远程 CI 已通过，包括官网生产构建、全量单测、质量门禁与
CodeQL；两项自动审查均通过，无阻塞发现。仍需仓库要求的人工 review 后合并。

本地重跑视觉检查（先启动官网并读取实际端口）：

```sh
PRICING_BASE_URL=http://localhost:<实际端口> pnpm exec playwright test --config tests/visual/pricing-tabs.config.ts
```

另：排查期间误跑到已有的页脚视觉测试 `landing-footer-consent-row.spec.ts`，其 fixture 读取现有
Button re-export 时报 `Unexpected fixture dependency:
@zooclaw/design-system`。该 fixture 与 Button 文件均未在本 PR 改动；本次为 pricing
提供独立配置，不扩大到页脚测试修复。

## 审查备注的处理

- 视觉回归检查目前需本地启动服务后运行，未接入 CI；CI 已通过的是既有构建、单元测试和质量门禁。自动启动服务的视觉 CI 可独立完善。
- RGB 固定值用于保护用户指定的品牌外观；有意更改 pricing 的设计 token 时应同步更新预期。
- 面板的 `outline-none` 沿用原共享 Tabs 的表现，本 PR 没有新增或扩大该行为。焦点规则的整体改进留作独立调整。
```

### PR Body

## Summary

- 修复官网 pricing 工具与媒体分类栏被设计系统 2.1.0 样式覆盖的问题，恢复与价格卡片同宽的分类栏、紫色选中背景和白色文字；手机端保留三列两行布局。
- 同时恢复页面顶部产品切换栏的全宽布局和品牌下划线。
- pricing 的品牌外观由官网页面管理，使用 Radix Tabs 保留键盘导航、焦点及 ARIA 关联。修改位于 ECAP 官网，独立设计系统仓库与 npm 包无需发布。

## Root cause

共享 Tabs 引入了未放入 CSS layer 的 `.zc-selection-group` / `.zc-selection-item` 规则，优先于官网原有的 Tailwind 工具类。`width: fit-content` 和灰色背景覆盖了官网的全宽白色分类栏；白色 moving indicator 又接管了选中背景，导致紫色选中态失效。

本次让官网两组 Tabs 直接使用现有 Radix 底层组件，在页面内设置品牌样式，不再依赖设计系统的中性 selection 样式。价格、文案和业务导航逻辑保持不变，未回退产品内 Tabs / Segmented。

## Test plan

- [x] 先运行浏览器回归检查复现失败：1440px 下分类栏比内容卡片窄约 494px。
- [x] 修复后 Playwright 6/6 通过：中英文 × 375 / 768 / 1440px；检查实际计算颜色、全宽对齐、各分类内容关联、键盘循环与 End 导航、产品切换及横向溢出。
- [x] pricing 相关单元测试 70/70 通过，包含价格目录、导航、方案展示、翻译完整性与 typography 检查。
- [x] `verify-web.sh --no-test`：治理检查、TypeScript 和改动文件 ESLint 通过；新增独立测试配置后再次运行 TypeScript / ESLint 通过。
- [x] `pnpm install --frozen-lockfile --offline --ignore-scripts` 通过；仅声明工作区已有的 `radix-ui@1.5.0` 为官网直接依赖，没有升级依赖。
- [x] 新视觉测试配置已登记到 Knip 的 Playwright 入口，`knip` 硬门禁与完整 `pnpm lint:ci` 通过。初轮 CI 暴露的两个测试文件未登记问题已修复，未增加任何忽略项。
- [x] 最新提交 `672f3ee2c` 的远程 CI 已通过，包括官网生产构建、全量单测、质量门禁与 CodeQL；两项自动审查均通过，无阻塞发现。仍需仓库要求的人工 review 后合并。

本地重跑视觉检查（先启动官网并读取实际端口）：

```sh
PRICING_BASE_URL=http://localhost:<实际端口> pnpm exec playwright test --config tests/visual/pricing-tabs.config.ts
```

另：排查期间误跑到已有的页脚视觉测试 `landing-footer-consent-row.spec.ts`，其 fixture 读取现有 Button re-export 时报 `Unexpected fixture dependency: @zooclaw/design-system`。该 fixture 与 Button 文件均未在本 PR 改动；本次为 pricing 提供独立配置，不扩大到页脚测试修复。

## 审查备注的处理

- 视觉回归检查目前需本地启动服务后运行，未接入 CI；CI 已通过的是既有构建、单元测试和质量门禁。自动启动服务的视觉 CI 可独立完善。
- RGB 固定值用于保护用户指定的品牌外观；有意更改 pricing 的设计 token 时应同步更新预期。
- 面板的 `outline-none` 沿用原共享 Tabs 的表现，本 PR 没有新增或扩大该行为。焦点规则的整体改进留作独立调整。


---

## feat(claw-interface): OpenAI-compatible LLM gateway for user JWTs and Platform API keys (#4128)

- **SHA**: `518b4e81be6305baa9ae9d2e711024bbc46eb87d`
- **作者**: tim-srp
- **日期**: 2026-10-23T05:49:18Z
- **PR**: #4128

### Commit Message

```
feat(claw-interface): OpenAI-compatible LLM gateway for user JWTs and Platform API keys (#4128)

## Summary

An OpenAI-compatible pass-through to LiteLLM, so clients can call models
without holding a LiteLLM key. The key is attached server-side and is
never returned.

- `GET /llm/v1/models` and `POST /llm/v1/chat/completions` authenticate
with a **user JWT** and attach the caller's Billing Profile key. If the
profile has no key yet, billing initialization runs once. An optional
`X-ECAP-Org-Id` header rejects the call when the caller is not billed to
that org.
- `GET /service/v1/llm/models` and `POST
/service/v1/llm/chat/completions` authenticate with a **Platform API
key** (`zwp_live_`) and attach the organization's payer key through
`require_billing_key`, the same key Agents run with. Work service tokens
(`zct_`) get 404.
- Request bodies are restricted to public Chat Completions fields;
`api_key`, `api_base` and other routing overrides are rejected. Requests
are never retried. Upstream headers and error bodies are masked into
stable `llm.*` codes.
- LiteLLM handles provider adaptation; this service streams bytes
through unchanged.

The first consumer is the ZooWork desktop (`ecap-workforce`), which can
then take a Platform key instead of a LiteLLM key.

Docs: `services/claw-interface/docs/llm-gateway.md`.

## Test plan

- [x] `tests/unit/test_llm_gateway.py` and
`tests/unit/test_service_api_llm.py`
- [x] Full claw-interface unit suite: 12514 passed, 14 skipped
- [x] ruff format / ruff check / pyright clean on changed files
- [ ] Staging: call `/service/v1/llm/chat/completions` with a bound
`zwp_live_` key and stream a reply

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

## Summary

An OpenAI-compatible pass-through to LiteLLM, so clients can call models without holding a LiteLLM key. The key is attached server-side and is never returned.

- `GET /llm/v1/models` and `POST /llm/v1/chat/completions` authenticate with a **user JWT** and attach the caller's Billing Profile key. If the profile has no key yet, billing initialization runs once. An optional `X-ECAP-Org-Id` header rejects the call when the caller is not billed to that org.
- `GET /service/v1/llm/models` and `POST /service/v1/llm/chat/completions` authenticate with a **Platform API key** (`zwp_live_`) and attach the organization's payer key through `require_billing_key`, the same key Agents run with. Work service tokens (`zct_`) get 404.
- Request bodies are restricted to public Chat Completions fields; `api_key`, `api_base` and other routing overrides are rejected. Requests are never retried. Upstream headers and error bodies are masked into stable `llm.*` codes.
- LiteLLM handles provider adaptation; this service streams bytes through unchanged.

The first consumer is the ZooWork desktop (`ecap-workforce`), which can then take a Platform key instead of a LiteLLM key.

Docs: `services/claw-interface/docs/llm-gateway.md`.

## Test plan

- [x] `tests/unit/test_llm_gateway.py` and `tests/unit/test_service_api_llm.py`
- [x] Full claw-interface unit suite: 12514 passed, 14 skipped
- [x] ruff format / ruff check / pyright clean on changed files
- [ ] Staging: call `/service/v1/llm/chat/completions` with a bound `zwp_live_` key and stream a reply

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## docs(web): rebuild the Agent guide around the Platform starter (#4123)

- **SHA**: `af1af5e34df3d6557b67af7f40226b59d12a8463`
- **作者**: finn-srp
- **日期**: 2026-10-23T02:51:29Z
- **PR**: #4123

### Commit Message

```
docs(web): rebuild the Agent guide around the Platform starter (#4123)

<!-- PR 标题：type(scope): description -->

## Summary

`/guides/publish-agent` 原来建立在 ZooWork App Kit 和 Work API key 上。App Kit
已在 2026-10-01 从 quickstarts 删除（zoowork-platform-quickstarts #18），读者照第 4
到第 6 步做不下去，第 2 步还在让读者用 `zct_` key。这次把指南改成基于 Platform Agent Starter 的
Demo 指南。

- **定位**：标题改为 “Build a ZooWork Agent Demo” / “用 ZooWork 快速做一个 Agent
Demo”，版本 3.0。路由不变。
- **六个阶段**：设计 Agent → 拿 Project key 并充值 → coding agent 写
`agent/agent.md` 和 `app.config.ts`，运行 `npm run setup` → `npm run dev` 试用
→ 迭代 → 公开之前。指南不负责部署，第 6 步指向 starter README 的 “Before you go public”。
- **key**：读者自己把 `zwp_live_` key 填进 `.env`，不交给 coding
agent，也不粘贴到聊天里。`.env.example` 已带 production 地址，指南只让读者填 key。第 2 阶段加了直达
platform.zoowork.ai 的按钮。
- **狗狗案例**：给出给 coding agent 的
Prompt，以及两个结果文件的完整内容，中英文各一套。为了渲染这两个文件，`guide-sections.tsx` 加了 3 行。
- **截图**：Platform API keys 截图来自 `web/platform` 的 `dev:preview` 假数据，只显示
key 前缀。狗狗案例的 4 张截图来自 staging 上 starter 的真实运行（最新 starter
`f56d4be`，加上页面展示的同一版 `agent.md`）。跑完已 cleanup，没有残留资源。旧的 App Kit 截图已删除。
- **概念、清单、总结**：App Kit、`AGENT_PICKER`、`ZOOWORK_AGENT_ID`、share link
全部移除；区分 coding skill 和 Platform Skill。
- **测试**：单测锁定 `zwp_live_xxx`、`agent/agent.md`、`npm run setup` 和 Platform
链接；全页禁止出现 `zct_`、`App
Kit`、`AGENT_PICKER`、`ZOOWORK_AGENT_ID`、`ZOOWORK_BASE_URL` 和真实 key。SEO
测试同步更新标题。

相关 PR：
- zoowork-sdk-skills #38：skill 只在“空目录 + 想要可运行的聊天 demo”时提一次 starter。
- zoowork-agents-docs #69：quickstart 的下一步加上 Agent Starter 链接。

待定（本 PR 不改）：导航入口仍叫 “Publishing Guide / 发布指南”。内部原稿 v2.01 的作者需要知道这次改版。

## Test plan

- [x] rebase 到最新 main 后运行 `pnpm test:unit`：866 个文件、10909 个用例通过，1 个跳过
- [x] `pnpm lint:ci`、`verify-web.sh --no-test`（guards、tsc、eslint）通过
- [x] `prettier --check`、图片大小检查通过
- [x] 本地 `next dev` 打开中英文页面：所有图片加载成功，手机宽度 390 下没有横向滚动；可复制块、案例的两个结果文件和
Platform 按钮显示正常

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

<!-- PR 标题：type(scope): description -->

## Summary

`/guides/publish-agent` 原来建立在 ZooWork App Kit 和 Work API key 上。App Kit 已在 2026-10-01 从 quickstarts 删除（zoowork-platform-quickstarts #18），读者照第 4 到第 6 步做不下去，第 2 步还在让读者用 `zct_` key。这次把指南改成基于 Platform Agent Starter 的 Demo 指南。

- **定位**：标题改为 “Build a ZooWork Agent Demo” / “用 ZooWork 快速做一个 Agent Demo”，版本 3.0。路由不变。
- **六个阶段**：设计 Agent → 拿 Project key 并充值 → coding agent 写 `agent/agent.md` 和 `app.config.ts`，运行 `npm run setup` → `npm run dev` 试用 → 迭代 → 公开之前。指南不负责部署，第 6 步指向 starter README 的 “Before you go public”。
- **key**：读者自己把 `zwp_live_` key 填进 `.env`，不交给 coding agent，也不粘贴到聊天里。`.env.example` 已带 production 地址，指南只让读者填 key。第 2 阶段加了直达 platform.zoowork.ai 的按钮。
- **狗狗案例**：给出给 coding agent 的 Prompt，以及两个结果文件的完整内容，中英文各一套。为了渲染这两个文件，`guide-sections.tsx` 加了 3 行。
- **截图**：Platform API keys 截图来自 `web/platform` 的 `dev:preview` 假数据，只显示 key 前缀。狗狗案例的 4 张截图来自 staging 上 starter 的真实运行（最新 starter `f56d4be`，加上页面展示的同一版 `agent.md`）。跑完已 cleanup，没有残留资源。旧的 App Kit 截图已删除。
- **概念、清单、总结**：App Kit、`AGENT_PICKER`、`ZOOWORK_AGENT_ID`、share link 全部移除；区分 coding skill 和 Platform Skill。
- **测试**：单测锁定 `zwp_live_xxx`、`agent/agent.md`、`npm run setup` 和 Platform 链接；全页禁止出现 `zct_`、`App Kit`、`AGENT_PICKER`、`ZOOWORK_AGENT_ID`、`ZOOWORK_BASE_URL` 和真实 key。SEO 测试同步更新标题。

相关 PR：
- zoowork-sdk-skills #38：skill 只在“空目录 + 想要可运行的聊天 demo”时提一次 starter。
- zoowork-agents-docs #69：quickstart 的下一步加上 Agent Starter 链接。

待定（本 PR 不改）：导航入口仍叫 “Publishing Guide / 发布指南”。内部原稿 v2.01 的作者需要知道这次改版。

## Test plan

- [x] rebase 到最新 main 后运行 `pnpm test:unit`：866 个文件、10909 个用例通过，1 个跳过
- [x] `pnpm lint:ci`、`verify-web.sh --no-test`（guards、tsc、eslint）通过
- [x] `prettier --check`、图片大小检查通过
- [x] 本地 `next dev` 打开中英文页面：所有图片加载成功，手机宽度 390 下没有横向滚动；可复制块、案例的两个结果文件和 Platform 按钮显示正常

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
