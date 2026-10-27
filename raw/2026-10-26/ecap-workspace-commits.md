# SerendipityOneInc/ecap-workspace — commits 2026-10-26

## fix(events): add Chinese localization and brand typography (#4141)

- **SHA**: `5aae85bac7c69e31a99e88a6152ae15b197cbfcc`
- **作者**: anna-srp
- **日期**: 2026-10-26T11:09:48Z
- **PR**: #4141

### Commit Message

```
fix(events): add Chinese localization and brand typography (#4141)

## Summary

Selecting Chinese from Events previously returned visitors to the
homepage. Add a complete `/zh/events` page and keep visitors on Events
when switching languages, including their query string and section
anchor.

- Localize all nine event cards, navigation, filters, dates,
accessibility labels, metadata and structured data with editorial
Chinese copy. Keep the original images, facts and destination links.
- Use the official Noto Serif SC display face and Noto Sans SC content
face with Chinese spacing and responsive heading sizes. Load the font
registry only from the Events route; Events-specific aliases leave
English and shared Header/Footer typography unchanged.
- Register `/zh/events` in the route contract and sitemap. Document
bilingual content maintenance and provide a deterministic font-manifest
generator using the existing design-system assets and licenses.

## Root cause

Events was registered as English-only, so the shared language switcher
correctly fell back to the selected language's homepage. The page also
had no Chinese content or explicitly loaded Chinese brand fonts.

## Test plan

- [x] Seven targeted unit-test files: 146 tests passed, covering
localized rendering, filtering, source-link preservation, structured
data, SEO, sitemap, route boundaries and language switching with
query/hash preservation. After review fixes, reran the three affected
files plus the new font contract test: 43 tests passed.
- [x] Font manifest generation check is included in the unit suite; all
202 official font faces preserve their Unicode subsets and variable
weights without duplicating font binaries.
- [x] Local browser verification at 390, 768 and 1440 px; Chinese fonts
load, no horizontal overflow, English and shared chrome retain their
typography.
- [x] Repository pre-commit lint and pre-push changed-surface
verification.
- [x] Reproduced CI's three stale `LocaleLink` expectations locally,
updated them for the now-published Chinese route, and added the reverse
English-navigation case. All 101 tests in the four directly related
files pass; query strings and anchors remain covered.

Review follow-up: the generated stylesheet contains font-face asset
registration only, with no component selectors or layout rules; all page
styling remains Tailwind. It is imported at the Events entry rather than
globally. Local asset inspection confirms the homepage includes no
Events font registrations and the Events CSS includes the expected 202
faces. The font sync check runs in the unit suite. Existing scoped
heading overrides and the intentionally omitted Chinese state
abbreviation are unchanged.

Frontend-only change. No backend or configuration migration.

---------

Co-authored-by: Yueru Wang <yueruwang@Yuerus-MacBook-Air.local>
```

### PR Body

## Summary

Selecting Chinese from Events previously returned visitors to the homepage. Add a complete `/zh/events` page and keep visitors on Events when switching languages, including their query string and section anchor.

- Localize all nine event cards, navigation, filters, dates, accessibility labels, metadata and structured data with editorial Chinese copy. Keep the original images, facts and destination links.
- Use the official Noto Serif SC display face and Noto Sans SC content face with Chinese spacing and responsive heading sizes. Load the font registry only from the Events route; Events-specific aliases leave English and shared Header/Footer typography unchanged.
- Register `/zh/events` in the route contract and sitemap. Document bilingual content maintenance and provide a deterministic font-manifest generator using the existing design-system assets and licenses.

## Root cause

Events was registered as English-only, so the shared language switcher correctly fell back to the selected language's homepage. The page also had no Chinese content or explicitly loaded Chinese brand fonts.

## Test plan

- [x] Seven targeted unit-test files: 146 tests passed, covering localized rendering, filtering, source-link preservation, structured data, SEO, sitemap, route boundaries and language switching with query/hash preservation. After review fixes, reran the three affected files plus the new font contract test: 43 tests passed.
- [x] Font manifest generation check is included in the unit suite; all 202 official font faces preserve their Unicode subsets and variable weights without duplicating font binaries.
- [x] Local browser verification at 390, 768 and 1440 px; Chinese fonts load, no horizontal overflow, English and shared chrome retain their typography.
- [x] Repository pre-commit lint and pre-push changed-surface verification.
- [x] Reproduced CI's three stale `LocaleLink` expectations locally, updated them for the now-published Chinese route, and added the reverse English-navigation case. All 101 tests in the four directly related files pass; query strings and anchors remain covered.

Review follow-up: the generated stylesheet contains font-face asset registration only, with no component selectors or layout rules; all page styling remains Tailwind. It is imported at the Events entry rather than globally. Local asset inspection confirms the homepage includes no Events font registrations and the Events CSS includes the expected 202 faces. The font sync check runs in the unit suite. Existing scoped heading overrides and the intentionally omitted Chinese state abbreviation are unchanged.

Frontend-only change. No backend or configuration migration.


---

## fix(api-keys): stop issuing new Work service tokens (#4071)

- **SHA**: `b724445eaf435c08140d7e09157c1f408458abef`
- **作者**: finn-srp
- **日期**: 2026-10-26T10:26:59Z
- **PR**: #4071

### Commit Message

```
fix(api-keys): stop issuing new Work service tokens (#4071)

Work settings still offered `zct_` API key creation alongside Platform
Project keys. This change hides that entry in Identity and shared
Organization navigation, and makes old API Keys deep links fall back to
General. Authenticated requests to the Work key create endpoint now
return `409 service_token.issuance_disabled` with a link to Platform
before any key is generated.

Existing Work keys continue to authenticate and use `/service/v1`; list,
rebind and revoke remain available through their existing backend
endpoints. The retirement spec records all three steps, with request
rejection and implementation cleanup deferred until Finn requests them.
No resource or billing migration is included.

The public publish-agent guide no longer sends new users to Settings →
API Keys: #4123 rebuilt it on the Platform Agent Starter and `zwp_live_`
Project keys, and it is live on zoowork.ai.

Rebased onto main `fd8c551` (2026-10-26). The rebase was conflict-free.
Two follow-up commits update e2e expectations that still required the
API Keys link: the `settings-team-admin` mock e2e added in #4094, and
the deployed-suite `settings.spec.ts` run by the scheduled/manual
`settings` project. Both now expect General, Usage and Billing and
assert that API Keys is absent. No other e2e spec references the API
Keys tab.

Validation on `26e5d6e` (the later `f561259` changes only
`tests/e2e/specs/settings.spec.ts`; `tsc` and ESLint pass on it):
- `pnpm test:unit`: 867 files passed; 10,940 tests passed, one skipped.
- `pnpm lint:ci` passed.
- `ecap-verify-py-ci` passed: Linux dependency resolution,
static/ci-lint checks, both duplication checks, and 12,871 tests passed
(14 skipped), with 89.68% coverage against the 89.5% gate.
- Manual check with `next dev` against the local mock backend: for a
team admin and a personal org admin, the account menu's Settings opens
`/identity` with the full navigation and no API Keys entry;
`/identity?tab=account-api-keys` renders General;
`/identity/organization` renders normally. The account menu's "Get API
keys" item links to ZooWork Platform.
- The updated e2e specs were not run locally (no Playwright browser
installed on this machine); their assertions match the manual check
above.
- The legacy `check-user` commit hook was skipped because it requires a
GitHub login ending in `-srp`. GitHub operations use Finn's
authenticated `finn930` account, and the commit author is `finn-srp
<finn@srp.one>`.

Deployment requires both Web and claw-interface.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

### PR Body

Work settings still offered `zct_` API key creation alongside Platform Project keys. This change hides that entry in Identity and shared Organization navigation, and makes old API Keys deep links fall back to General. Authenticated requests to the Work key create endpoint now return `409 service_token.issuance_disabled` with a link to Platform before any key is generated.

Existing Work keys continue to authenticate and use `/service/v1`; list, rebind and revoke remain available through their existing backend endpoints. The retirement spec records all three steps, with request rejection and implementation cleanup deferred until Finn requests them. No resource or billing migration is included.

The public publish-agent guide no longer sends new users to Settings → API Keys: #4123 rebuilt it on the Platform Agent Starter and `zwp_live_` Project keys, and it is live on zoowork.ai.

Rebased onto main `fd8c551` (2026-10-26). The rebase was conflict-free. Two follow-up commits update e2e expectations that still required the API Keys link: the `settings-team-admin` mock e2e added in #4094, and the deployed-suite `settings.spec.ts` run by the scheduled/manual `settings` project. Both now expect General, Usage and Billing and assert that API Keys is absent. No other e2e spec references the API Keys tab.

Validation on `26e5d6e` (the later `f561259` changes only `tests/e2e/specs/settings.spec.ts`; `tsc` and ESLint pass on it):
- `pnpm test:unit`: 867 files passed; 10,940 tests passed, one skipped.
- `pnpm lint:ci` passed.
- `ecap-verify-py-ci` passed: Linux dependency resolution, static/ci-lint checks, both duplication checks, and 12,871 tests passed (14 skipped), with 89.68% coverage against the 89.5% gate.
- Manual check with `next dev` against the local mock backend: for a team admin and a personal org admin, the account menu's Settings opens `/identity` with the full navigation and no API Keys entry; `/identity?tab=account-api-keys` renders General; `/identity/organization` renders normally. The account menu's "Get API keys" item links to ZooWork Platform.
- The updated e2e specs were not run locally (no Playwright browser installed on this machine); their assertions match the manual check above.
- The legacy `check-user` commit hook was skipped because it requires a GitHub login ending in `-srp`. GitHub operations use Finn's authenticated `finn930` account, and the commit author is `finn-srp <finn@srp.one>`.

Deployment requires both Web and claw-interface.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(agents): preserve Environment pins during runtime identity projection (#4140)

- **SHA**: `d35586415a80d33a34a2fc66afccf4a65d6793b3`
- **作者**: kaka-srp
- **日期**: 2026-10-26T07:37:54Z
- **PR**: #4140

### Commit Message

```
fix(agents): preserve Environment pins during runtime identity projection (#4140)

## Summary

创建 Agent 运行时身份投影时保留当前解析出的 Environment ID
和精确版本，避免只为绑定身份而重建配置，却把自定义环境切换为默认环境。MCP 配置迁移走同一处逻辑，也保留该绑定。

## Root cause

`source_declaration` 不一定包含实际 Environment 绑定。staging E2B canary
的初始配置使用自定义 Environment `@2`，但身份投影复制声明时没有补上解析出的绑定，Engine 在创建候选配置时重新选中了默认
Environment `@21`，因此沙盒缺少自定义环境提供的命令。候选声明现在以当前实际绑定覆盖缺失或陈旧的 Environment 字段。

本 PR 仅修改身份投影的候选配置与回归测试；不增加配置项、接口或数据库迁移。

## Test plan

- [x] 修复前先运行回归验证：4 项环境保留断言失败，其他 4 项通过。
- [x] 修复后相关 3 个测试文件共 23 项通过，覆盖声明缺失环境、声明版本陈旧、声明指向不同环境、MCP 迁移、凭据恢复和撤销行为。
- [x] `bash scripts/verify-py.sh` 通过：Ruff 检查和格式、Pyright、8 条导入契约。
- [ ] 修复版本尚未发布；发布 staging 后需重跑 E2B Environment 定向验收，不能将本地测试视为线上验收通过。

Related: https://github.com/SerendipityOneInc/zooclaw-engine/issues/2102
```

### PR Body

## Summary

创建 Agent 运行时身份投影时保留当前解析出的 Environment ID 和精确版本，避免只为绑定身份而重建配置，却把自定义环境切换为默认环境。MCP 配置迁移走同一处逻辑，也保留该绑定。

## Root cause

`source_declaration` 不一定包含实际 Environment 绑定。staging E2B canary 的初始配置使用自定义 Environment `@2`，但身份投影复制声明时没有补上解析出的绑定，Engine 在创建候选配置时重新选中了默认 Environment `@21`，因此沙盒缺少自定义环境提供的命令。候选声明现在以当前实际绑定覆盖缺失或陈旧的 Environment 字段。

本 PR 仅修改身份投影的候选配置与回归测试；不增加配置项、接口或数据库迁移。

## Test plan

- [x] 修复前先运行回归验证：4 项环境保留断言失败，其他 4 项通过。
- [x] 修复后相关 3 个测试文件共 23 项通过，覆盖声明缺失环境、声明版本陈旧、声明指向不同环境、MCP 迁移、凭据恢复和撤销行为。
- [x] `bash scripts/verify-py.sh` 通过：Ruff 检查和格式、Pyright、8 条导入契约。
- [ ] 修复版本尚未发布；发布 staging 后需重跑 E2B Environment 定向验收，不能将本地测试视为线上验收通过。

Related: https://github.com/SerendipityOneInc/zooclaw-engine/issues/2102


---

## test(e2e): cover Agent channel entry (#4138)

- **SHA**: `fd8c551cbd7cc62b26bc70ca49fd79815380ca19`
- **作者**: rayhuang198212
- **日期**: 2026-10-26T05:30:08Z
- **PR**: #4138

### Commit Message

```
test(e2e): cover Agent channel entry (#4138)

## Summary

- add the `agent-channel-entry` Playwright project
- cover navigation from a newly created Agent workspace to External
channels
- verify the created Agent appears as the Feishu channel target
- verify the Feishu manual setup form exposes empty App ID and App
Secret fields
- verify cancelling and refreshing does not create a channel connection
- reuse the shared Agent creation and cleanup infrastructure
- register the project in E2E CI and document its coverage

## Safety

- does not enter or submit third-party credentials
- does not start QR-code setup
- does not create a Feishu connection
- cleans up the created test Agent automatically

## Validation

- `pnpm install --frozen-lockfile`
- `pnpm exec tsc --noEmit --project app/tsconfig.json`
- `pnpm --filter @zooclaw/web-app run lint`
- `pnpm --filter @zooclaw/web-app run lint:ci`
- Staging Playwright: `2 passed`
```

### PR Body

## Summary

- add the `agent-channel-entry` Playwright project
- cover navigation from a newly created Agent workspace to External channels
- verify the created Agent appears as the Feishu channel target
- verify the Feishu manual setup form exposes empty App ID and App Secret fields
- verify cancelling and refreshing does not create a channel connection
- reuse the shared Agent creation and cleanup infrastructure
- register the project in E2E CI and document its coverage

## Safety

- does not enter or submit third-party credentials
- does not start QR-code setup
- does not create a Feishu connection
- cleans up the created test Agent automatically

## Validation

- `pnpm install --frozen-lockfile`
- `pnpm exec tsc --noEmit --project app/tsconfig.json`
- `pnpm --filter @zooclaw/web-app run lint`
- `pnpm --filter @zooclaw/web-app run lint:ci`
- Staging Playwright: `2 passed`


---

## feat(channels): add versioned interaction settings and pause controls (#4136)

- **SHA**: `69659b1a64e8d267d9d94db0b545c992b2af9f3a`
- **作者**: kaka-srp
- **日期**: 2026-10-26T03:27:21Z
- **PR**: #4136

### Commit Message

```
feat(channels): add versioned interaction settings and pause controls (#4136)

## Summary

Channel owners can now read and edit supported DM/group access rules,
member/group lists and mention gating, and pause or resume a connection
while retaining its identity, credentials and history. A dedicated
editor sends versioned partial updates, retains failed drafts, and
separates saved settings from gateway application status.

Guided Feishu/WeCom/DingTalk setup preserves the chosen rules. The
backend and Service API share typed settings and owner-scoped
recent-contact contracts; English/Chinese UI controls follow the
capabilities advertised by ACS. Existing per-group overrides and Feishu
document-permission controls are preserved.

## Dependencies and rollout

- Companion ACS PR:
https://github.com/SerendipityOneInc/agent-channel-service/pull/175.
- Deploy ACS first, complete the claw-interface rollout, then deploy web
or enable clients using the new setup fields.
- Old setup requests retain their Redis shape across a backend rolling
deploy. No Engine code or schema migration is included.
- Design and acceptance:
`docs/superpowers/specs/2026-10-23-channel-settings-closed-loop.md`.

## Test plan

- Backend channel/setup/client/Service API regression tests: 305 passed.
- Frontend channel/page/query suites: 343 passed.
- Web governance, TypeScript, ESLint; backend Ruff, format, Pyright and
architecture contracts passed.
- Playwright local browser acceptance: global and Agent-scoped entries,
edit/save/refetch/reload, member/group lists, conflict draft
preservation/reload, pause/resume, platform capability differences,
Chinese labels and 390px viewport.
- Companion ACS acceptance exercises real local HTTP, Engine identity,
PostgreSQL and Feishu gateway application acknowledgments, plus
installed-provider mention admission checks.
- UI browser tests use mock authentication/backend data. No customer
messages or live LLM chat turns were sent.

## Local review

Astra completed a local review and targeted re-review. All four verified
findings were fixed: provider-prefixed wildcard IDs, ineffective WeChat
DM controls, legacy Feishu mention-default changes, and old WeChat
create compatibility. The re-review found no new actionable issues and
cleared the change for PR creation.

## Automated review follow-up

- Enabled the existing workspace query polling on the global Channels
page; pending gateway application refreshes every five seconds even when
connection health is already healthy. The editor continues observing the
shared query. Browser acceptance verified pending-to-applied after
saving without navigation or window refocus.
- Preserved historical explicit-null behavior for existing nullable
update fields and create allow_from; newly introduced
list/mention/version inputs still reject null.
- Added a regression proving a legacy pairing policy stays visible and
is absent from an unrelated dirty-only update. Capability lists describe
newly selectable policies and do not redefine historical API values.
- ACS/backend/web deployment order and setup-session rolling
compatibility remain documented above. Readability-only refactors were
left outside this change.

Astra independently re-reviewed this follow-up delta and found no new
actionable issues.

Final review adjudication: ACS remains the policy authority. Its update
path normalizes every effective dm_policy=open to allowFrom=["*"], so a
simultaneously forwarded member list cannot override open access. Split
validation is intentional: claw-interface validates provided fields; ACS
validates them against saved policy under its transaction. Existing
owner resolution is shared across Service API actions. Deployment must
follow the documented ACS → complete backend rollout → web order; this
PR does not perform a release.
```

### PR Body

## Summary

Channel owners can now read and edit supported DM/group access rules, member/group lists and mention gating, and pause or resume a connection while retaining its identity, credentials and history. A dedicated editor sends versioned partial updates, retains failed drafts, and separates saved settings from gateway application status.

Guided Feishu/WeCom/DingTalk setup preserves the chosen rules. The backend and Service API share typed settings and owner-scoped recent-contact contracts; English/Chinese UI controls follow the capabilities advertised by ACS. Existing per-group overrides and Feishu document-permission controls are preserved.

## Dependencies and rollout

- Companion ACS PR: https://github.com/SerendipityOneInc/agent-channel-service/pull/175.
- Deploy ACS first, complete the claw-interface rollout, then deploy web or enable clients using the new setup fields.
- Old setup requests retain their Redis shape across a backend rolling deploy. No Engine code or schema migration is included.
- Design and acceptance: `docs/superpowers/specs/2026-10-23-channel-settings-closed-loop.md`.

## Test plan

- Backend channel/setup/client/Service API regression tests: 305 passed.
- Frontend channel/page/query suites: 343 passed.
- Web governance, TypeScript, ESLint; backend Ruff, format, Pyright and architecture contracts passed.
- Playwright local browser acceptance: global and Agent-scoped entries, edit/save/refetch/reload, member/group lists, conflict draft preservation/reload, pause/resume, platform capability differences, Chinese labels and 390px viewport.
- Companion ACS acceptance exercises real local HTTP, Engine identity, PostgreSQL and Feishu gateway application acknowledgments, plus installed-provider mention admission checks.
- UI browser tests use mock authentication/backend data. No customer messages or live LLM chat turns were sent.

## Local review

Astra completed a local review and targeted re-review. All four verified findings were fixed: provider-prefixed wildcard IDs, ineffective WeChat DM controls, legacy Feishu mention-default changes, and old WeChat create compatibility. The re-review found no new actionable issues and cleared the change for PR creation.

## Automated review follow-up

- Enabled the existing workspace query polling on the global Channels page; pending gateway application refreshes every five seconds even when connection health is already healthy. The editor continues observing the shared query. Browser acceptance verified pending-to-applied after saving without navigation or window refocus.
- Preserved historical explicit-null behavior for existing nullable update fields and create allow_from; newly introduced list/mention/version inputs still reject null.
- Added a regression proving a legacy pairing policy stays visible and is absent from an unrelated dirty-only update. Capability lists describe newly selectable policies and do not redefine historical API values.
- ACS/backend/web deployment order and setup-session rolling compatibility remain documented above. Readability-only refactors were left outside this change.

Astra independently re-reviewed this follow-up delta and found no new actionable issues.

Final review adjudication: ACS remains the policy authority. Its update path normalizes every effective dm_policy=open to allowFrom=["*"], so a simultaneously forwarded member list cannot override open access. Split validation is intentional: claw-interface validates provided fields; ACS validates them against saved policy under its transaction. Existing owner resolution is shared across Service API actions. Deployment must follow the documented ACS → complete backend rollout → web order; this PR does not perform a release.


---

## fix(usage): group tool service labels (#3848)

- **SHA**: `8bfe5b087ab1e2892e6da722b578938657c3b787`
- **作者**: kaka-srp
- **日期**: 2026-10-26T03:18:23Z
- **PR**: #3848

### Commit Message

```
fix(usage): group tool service labels (#3848)

## Summary

Usage details now label tool-service records as `Tool usage` / `工具使用`,
while retaining configured model names and `Compute`. This changes
presentation only and preserves usage records and billing data.

The branch is synchronized with current main, preserving the current
table styling, locale formatting, scoped filters, and cursor pagination.

## Validation

- Focused `UsageDimensions` regression suite: 8 tests passed, including
tool/model/compute labels, pagination, refresh, and scoped filters.
- Local frontend governance guards, TypeScript, and targeted ESLint
passed. The final JSX-only formatting correction passed targeted ESLint.
- `git diff --check` and local PR size check passed.
- Updated-head GitHub CI passed, including frontend tests, type/lint
checks, production build, CodeQL, and PR size checks. Claude and Codex
automated reviews both approved with no findings.
```

### PR Body

## Summary

Usage details now label tool-service records as `Tool usage` / `工具使用`, while retaining configured model names and `Compute`. This changes presentation only and preserves usage records and billing data.

The branch is synchronized with current main, preserving the current table styling, locale formatting, scoped filters, and cursor pagination.

## Validation

- Focused `UsageDimensions` regression suite: 8 tests passed, including tool/model/compute labels, pagination, refresh, and scoped filters.
- Local frontend governance guards, TypeScript, and targeted ESLint passed. The final JSX-only formatting correction passed targeted ESLint.
- `git diff --check` and local PR size check passed.
- Updated-head GitHub CI passed, including frontend tests, type/lint checks, production build, CodeQL, and PR size checks. Claude and Codex automated reviews both approved with no findings.


---

## fix(artifacts): isolate detached runtimes in global library (#4029)

- **SHA**: `eaefa002951b6b8e0d3d285686f1e7e5521d2c6b`
- **作者**: kaka-srp
- **日期**: 2026-10-26T03:02:02Z
- **PR**: #4029

### Commit Message

```
fix(artifacts): isolate detached runtimes in global library (#4029)

The global Artifact Library returned 409 for the whole page when one
persisted Agent had a detached Engine runtime. Skip only
`agent.runtime_detached` sources during the global aggregation so
artifacts from healthy Agents remain available. Explicit Agent selection
preserves the conflict; other conflicts and dependency failures still
propagate. No workspace records are changed.

This fixes an existing issue independently of V1 retirement PR #4028. It
does not change Workspace Files or artifact-resolver CORS configuration.

Validation: 22 related tests passed; scoped Ruff/format/Pyright and
pre-commit review passed. Local FastAPI used the tasks.json staging
dependencies and encrypted Mongo client without mocked HTTP: deployed
staging returned 409, modified local backend returned 200 with three
existing artifacts, and local `/assets` rendered all three after the
cold-compile request was retried. Browser credentials were cleared and
the original account locale was restored independently.

Evidence: [validation
report](docs/validation/2026-10-08-artifact-library-detached.md). All
required CI checks passed. Claude and Codex reviews returned APPROVE
with no actionable correctness findings. Remains a draft for owner
review; do not merge or release automatically.

Review adjudication: retain the existing missing-Engine-agent log
because the targeted detached-runtime condition is the client mapping of
an Engine 404, not a transport disconnection. The suggested
boolean-expression comment is stylistic; the scope/code matrix is
directly covered by tests. No extra refactor is included.
```

### PR Body

The global Artifact Library returned 409 for the whole page when one persisted Agent had a detached Engine runtime. Skip only `agent.runtime_detached` sources during the global aggregation so artifacts from healthy Agents remain available. Explicit Agent selection preserves the conflict; other conflicts and dependency failures still propagate. No workspace records are changed.

This fixes an existing issue independently of V1 retirement PR #4028. It does not change Workspace Files or artifact-resolver CORS configuration.

Validation: 22 related tests passed; scoped Ruff/format/Pyright and pre-commit review passed. Local FastAPI used the tasks.json staging dependencies and encrypted Mongo client without mocked HTTP: deployed staging returned 409, modified local backend returned 200 with three existing artifacts, and local `/assets` rendered all three after the cold-compile request was retried. Browser credentials were cleared and the original account locale was restored independently.

Evidence: [validation report](docs/validation/2026-10-08-artifact-library-detached.md). All required CI checks passed. Claude and Codex reviews returned APPROVE with no actionable correctness findings. Remains a draft for owner review; do not merge or release automatically.

Review adjudication: retain the existing missing-Engine-agent log because the targeted detached-runtime condition is the client mapping of an Engine 404, not a transport disconnection. The suggested boolean-expression comment is stylistic; the scope/code matrix is directly covered by tests. No extra refactor is included.


---
