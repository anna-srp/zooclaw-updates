# ecap-workspace — 2026-07-07 commits

## feat(web): add custom publish agent updates (#2763)

- **SHA**: 2dc120175481b1dc3a7dec8c5a14829308e3213e
- **作者**: bill-srp
- **日期**: 2026-07-07T13:42:43Z
- **PR**: #2763

### Commit Message

```
feat(web): add custom publish agent updates (#2763)

## Summary

- add a custom publish-page Update action for installed org-pack agents
- show Update only when the installed workspace submission differs from
the pack latest submission, matching the official agents page behavior
- reuse the computer-scoped agent update route and refresh
current-computer agents after completion

## Tests

- `./node_modules/.bin/vitest run --config ./vitest.config.mts
tests/unit/app/agents-manager-publish.unit.spec.tsx`
- `./node_modules/.bin/tsc --noEmit` with stale `.next/types`
temporarily moved out and restored
- `git diff --check`

## Notes

- `pnpm --dir web/app exec ...` is still blocked locally by the existing
`ERR_PNPM_MISSING_TARBALL_INTEGRITY` issue for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.
- Direct `eslint` invocation is currently blocked locally by dependency
resolution for `tw-animate-css`.
```

### PR Body

## Summary

- add a custom publish-page Update action for installed org-pack agents
- show Update only when the installed workspace submission differs from the pack latest submission, matching the official agents page behavior
- reuse the computer-scoped agent update route and refresh current-computer agents after completion

## Tests

- `./node_modules/.bin/vitest run --config ./vitest.config.mts tests/unit/app/agents-manager-publish.unit.spec.tsx`
- `./node_modules/.bin/tsc --noEmit` with stale `.next/types` temporarily moved out and restored
- `git diff --check`

## Notes

- `pnpm --dir web/app exec ...` is still blocked locally by the existing `ERR_PNPM_MISSING_TARBALL_INTEGRITY` issue for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.
- Direct `eslint` invocation is currently blocked locally by dependency resolution for `tw-animate-css`.


## fix(ios): decode mixed Mattermost post props (#2760)

- **SHA**: 5212cacf4a28822118f2bdeec1b34905c145c600
- **作者**: bill-srp
- **日期**: 2026-07-07T10:35:02Z
- **PR**: #2760

### Commit Message

```
fix(ios): decode mixed Mattermost post props (#2760)

## Summary

- Change iOS Mattermost post props decoding from string-only to
heterogeneous JSON values.
- Add a regression test covering numeric, boolean, nested, array, and
null props in Mattermost post lists.

## Verification

- `swiftlint lint ZooClaw/Models/Mattermost/MattermostModels.swift
ZooClawTests/MattermostModelsTests.swift`
- `xcodebuild build-for-testing -project ZooClaw.xcodeproj -scheme
ZooClaw -destination 'generic/platform=iOS Simulator'
-parallel-testing-enabled NO
-maximum-concurrent-test-simulator-destinations 1
-only-testing:ZooClawTests/MattermostModelsTests/postListDecodesMixedProps`

Note: I could not run the XCTest itself locally because this machine has
no matching concrete iOS Simulator device; generic simulator
build-for-testing succeeded.
```

### PR Body

## Summary

- Change iOS Mattermost post props decoding from string-only to heterogeneous JSON values.
- Add a regression test covering numeric, boolean, nested, array, and null props in Mattermost post lists.

## Verification

- `swiftlint lint ZooClaw/Models/Mattermost/MattermostModels.swift ZooClawTests/MattermostModelsTests.swift`
- `xcodebuild build-for-testing -project ZooClaw.xcodeproj -scheme ZooClaw -destination 'generic/platform=iOS Simulator' -parallel-testing-enabled NO -maximum-concurrent-test-simulator-destinations 1 -only-testing:ZooClawTests/MattermostModelsTests/postListDecodesMixedProps`

Note: I could not run the XCTest itself locally because this machine has no matching concrete iOS Simulator device; generic simulator build-for-testing succeeded.


## style(agent-builder): 优化测试模式布局 (#2755)

- **SHA**: bf1a1a6830fb11be08c7d8bea67f3493c679e5df
- **作者**: lynn Zhuang
- **日期**: 2026-07-07T10:15:42Z
- **PR**: #2755

### Commit Message

```
style(agent-builder): 优化测试模式布局 (#2755)

## 变更内容

- 优化 Agent Builder 的 test mode 布局：右侧测试面板独立展示，标题与左侧 header 对齐，并支持关闭/重新打开。
- 点击 `Package & Test` 后立即进入 test mode 展示测试面板，同时保留失败回滚。
- 将顶部状态标签调整为更小的状态 tag 样式，避免看起来像按钮。
- 统一右上角图标 tooltip 样式，并补充 `Test panel` 文案。
- 完善本地 mock 预览数据，方便在本地直接查看 Agent Builder 测试模式页面。

## 验证

- `node --check web/app/scripts/mock-backend.mjs`
- `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/agent-builder-client.unit.spec.tsx`
- `bash scripts/verify-web.sh ...`
- push 前的 `verify-changed` 检查已通过

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
```

### PR Body

## 变更内容

- 优化 Agent Builder 的 test mode 布局：右侧测试面板独立展示，标题与左侧 header 对齐，并支持关闭/重新打开。
- 点击 `Package & Test` 后立即进入 test mode 展示测试面板，同时保留失败回滚。
- 将顶部状态标签调整为更小的状态 tag 样式，避免看起来像按钮。
- 统一右上角图标 tooltip 样式，并补充 `Test panel` 文案。
- 完善本地 mock 预览数据，方便在本地直接查看 Agent Builder 测试模式页面。

## 验证

- `node --check web/app/scripts/mock-backend.mjs`
- `pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/agent-builder-client.unit.spec.tsx`
- `bash scripts/verify-web.sh ...`
- push 前的 `verify-changed` 检查已通过


## docs(review): tighten crash and failure-mode flip-flop guidance (#2718)

- **SHA**: e2e95301e9d6de21bcfcdde4842748b4c07856a5
- **作者**: bill-srp
- **日期**: 2026-07-07T09:27:14Z
- **PR**: #2718

### Commit Message

```
docs(review): tighten crash and failure-mode flip-flop guidance (#2718)

## Summary

Two calibration fixes to `code-review.md`, following up on #2714 and
motivated by the PR #2706 review loop (30 review rounds / 32 commits
over ~2 days):

1. **Restore deterministic crashes to the REQUEST_CHANGES impact list.**
#2714 dropped the old "won't compile/crash" class. Dropping "won't
compile" was right (CI owns that), but a deterministic crash / unhandled
error on a production request path is not reliably CI-caught (e.g. a
webhook handler that throws on a real provider payload) and is as severe
as "wrong result". A strict reader of the current list would demote a
guaranteed-crash finding to NEED_HUMAN_REVIEW.

2. **Stop failure-mode flip-flops.** In #2706 the reviewer blocked at
11:40 for *swallowing* pack-lookup failures (fail-open), then at 13:25
for *failing closed* after the fix, then again demanded fail-closed in a
later round — one direction per round, unbounded. The guide already
routes "fail-open vs fail-closed tradeoffs" to NEED_HUMAN_REVIEW; this
adds the explicit rule for the observed pattern: if a previous round
demanded the opposite failure mode for the same operation, don't block
in either direction — surface the decision to a human.

## Testing

- Documentation-only change; drift probe and no code paths affected.
- Reviewers read this file from the base branch, so the change takes
effect on PRs reviewed after merge.


## Second commit — failure-mode defaults

3. **Codify failure-mode defaults for `services/claw-interface`** (area
notes): user-facing lifecycle operations (install/uninstall) degrade
gracefully — proceed with persisted state, clean what is resolvable,
record residue for the repair loop, never strand a `*_failed` row before
any work runs; background reconcile/repair passes fail closed and retry
next cycle rather than act on incomplete identity data. This settles the
exact tradeoff PR #2706 oscillated on (uninstall fail-open at 13:25 vs
reconcile fail-closed at 08:24) as standing policy, so reviewers judge
against a default instead of re-litigating it per round.
```

### PR Body

## Summary

Two calibration fixes to `code-review.md`, following up on #2714 and motivated by the PR #2706 review loop (30 review rounds / 32 commits over ~2 days):

1. **Restore deterministic crashes to the REQUEST_CHANGES impact list.** #2714 dropped the old "won't compile/crash" class. Dropping "won't compile" was right (CI owns that), but a deterministic crash / unhandled error on a production request path is not reliably CI-caught (e.g. a webhook handler that throws on a real provider payload) and is as severe as "wrong result". A strict reader of the current list would demote a guaranteed-crash finding to NEED_HUMAN_REVIEW.

2. **Stop failure-mode flip-flops.** In #2706 the reviewer blocked at 11:40 for *swallowing* pack-lookup failures (fail-open), then at 13:25 for *failing closed* after the fix, then again demanded fail-closed in a later round — one direction per round, unbounded. The guide already routes "fail-open vs fail-closed tradeoffs" to NEED_HUMAN_REVIEW; this adds the explicit rule for the observed pattern: if a previous round demanded the opposite failure mode for the same operation, don't block in either direction — surface the decision to a human.

## Testing

- Documentation-only change; drift probe and no code paths affected.
- Reviewers read this file from the base branch, so the change takes effect on PRs reviewed after merge.


## Second commit — failure-mode defaults

3. **Codify failure-mode defaults for `services/claw-interface`** (area notes): user-facing lifecycle operations (install/uninstall) degrade gracefully — proceed with persisted state, clean what is resolvable, record residue for the repair loop, never strand a `*_failed` row before any work runs; background reconcile/repair passes fail closed and retry next cycle rather than act on incomplete identity data. This settles the exact tradeoff PR #2706 oscillated on (uninstall fail-open at 13:25 vs reconcile fail-closed at 08:24) as standing policy, so reviewers judge against a default instead of re-litigating it per round.


## fix(pack-store): reuse backend archive copy flow (#2758)

- **SHA**: 1a86d098bac4cf42e7535d6a12d4d96360de3b84
- **作者**: bill-srp
- **日期**: 2026-07-07T08:17:00Z
- **PR**: #2758

### Commit Message

```
fix(pack-store): reuse backend archive copy flow (#2758)

## Summary

- route dashboard-console private-pack submission through the backend
`from-private` endpoint instead of the dashboard `/api/r2/copy` proxy
- centralize server-side pack archive copying in
`pack_store.archive_copy`
- reuse the same R2 copy helper for marketplace listing copies and
official private submission copies
- remove the dashboard-console R2 copy route/helper and related tests

## Tests

- `PYTHONPATH=services/claw-interface
/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_submission_service.py
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py
services/claw-interface/tests/unit/test_paid_listing_service.py
services/claw-interface/tests/unit/test_public_listing_service.py -q`
- `/Users/bill/.venvs/claw-interface/bin/ruff check
services/claw-interface/app/routes/internal/agent_packs.py
services/claw-interface/app/schema/internal/agent_packs.py
services/claw-interface/app/services/pack_store/archive_copy.py
services/claw-interface/app/services/pack_store/paid_listing_service.py
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py
services/claw-interface/tests/unit/test_paid_listing_service.py
services/claw-interface/tests/unit/test_public_listing_service.py
services/claw-interface/tests/unit/test_submission_service.py`
- `./node_modules/.bin/vitest run app/lib/claw-api.test.ts
app/routes/agent-packs/submit-from-private-dialog.test.tsx`
- `./node_modules/.bin/tsc -b`
- `./node_modules/.bin/eslint app/lib/claw-api.ts
app/routes/agent-packs/submit-from-private-dialog.tsx
app/lib/claw-api.test.ts
app/routes/agent-packs/submit-from-private-dialog.test.tsx`
- `git diff --check`
```

### PR Body

## Summary

- route dashboard-console private-pack submission through the backend `from-private` endpoint instead of the dashboard `/api/r2/copy` proxy
- centralize server-side pack archive copying in `pack_store.archive_copy`
- reuse the same R2 copy helper for marketplace listing copies and official private submission copies
- remove the dashboard-console R2 copy route/helper and related tests

## Tests

- `PYTHONPATH=services/claw-interface /Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_submission_service.py services/claw-interface/tests/unit/test_internal_agent_packs_routes.py services/claw-interface/tests/unit/test_paid_listing_service.py services/claw-interface/tests/unit/test_public_listing_service.py -q`
- `/Users/bill/.venvs/claw-interface/bin/ruff check services/claw-interface/app/routes/internal/agent_packs.py services/claw-interface/app/schema/internal/agent_packs.py services/claw-interface/app/services/pack_store/archive_copy.py services/claw-interface/app/services/pack_store/paid_listing_service.py services/claw-interface/tests/unit/test_internal_agent_packs_routes.py services/claw-interface/tests/unit/test_paid_listing_service.py services/claw-interface/tests/unit/test_public_listing_service.py services/claw-interface/tests/unit/test_submission_service.py`
- `./node_modules/.bin/vitest run app/lib/claw-api.test.ts app/routes/agent-packs/submit-from-private-dialog.test.tsx`
- `./node_modules/.bin/tsc -b`
- `./node_modules/.bin/eslint app/lib/claw-api.ts app/routes/agent-packs/submit-from-private-dialog.tsx app/lib/claw-api.test.ts app/routes/agent-packs/submit-from-private-dialog.test.tsx`
- `git diff --check`


## refactor(web): remove unused api routes (#2757)

- **SHA**: ae15b28adf8b55739a9eb9e7a0e48890b119ea03
- **作者**: bill-srp
- **日期**: 2026-07-07T07:47:08Z
- **PR**: #2757

### Commit Message

```
refactor(web): remove unused api routes (#2757)

## Summary

- Remove unused web-only BFF routes and stale client helpers with no
current webapp callers.
- Keep active paths intact: OpenClaw redeploy/recreate, task DELETE
cleanup, chat replay create/revoke/public share reads, and desktop-pair.
- Update unit tests and shared test mocks to match the reduced API
surface.

## Scope

- Frontend only: this PR changes files under `web/app`.

## Verification

- `git diff --check origin/main...HEAD` passed.
- Static `rg` scans found no remaining references to removed
helpers/routes.
- `bash scripts/verify-web.sh ...` ran governance guards successfully,
but `tsc`, `vitest`, and `eslint` did not start because pnpm install
fails before tool execution with `ERR_PNPM_MISSING_TARBALL_INTEGRITY`
for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.
- Re-ran the same verify command outside the sandbox; it failed on the
same pnpm lockfile integrity issue.
```

### PR Body

## Summary

- Remove unused web-only BFF routes and stale client helpers with no current webapp callers.
- Keep active paths intact: OpenClaw redeploy/recreate, task DELETE cleanup, chat replay create/revoke/public share reads, and desktop-pair.
- Update unit tests and shared test mocks to match the reduced API surface.

## Scope

- Frontend only: this PR changes files under `web/app`.

## Verification

- `git diff --check origin/main...HEAD` passed.
- Static `rg` scans found no remaining references to removed helpers/routes.
- `bash scripts/verify-web.sh ...` ran governance guards successfully, but `tsc`, `vitest`, and `eslint` did not start because pnpm install fails before tool execution with `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`.
- Re-ran the same verify command outside the sandbox; it failed on the same pnpm lockfile integrity issue.


## feat(design-system): expand zooclaw preview foundations (#2702)

- **SHA**: 9d021a4878ba55268192adc08bcadd80823fa512
- **作者**: lynn Zhuang
- **日期**: 2026-07-07T06:39:46Z
- **PR**: #2702

### Commit Message

```
feat(design-system): expand zooclaw preview foundations (#2702)

## Summary

- Expand the ZooClaw design-system foundations preview with extracted
Liquid Glass colors, typography, spacing, shadows, glass tiers, and an
app shell sample.
- Add and refine DS component styling for Tag, Card, Button, Switch,
Table, Accordion, and Alert.
- Add regression tests for preview structure/CSS contracts and
token/component behavior.

## Validation

- `pnpm --filter @zooclaw/design-system test`
- `pnpm --filter @zooclaw/design-system tsc`
- `pnpm --filter @zooclaw/design-system lint`
- `pnpm --filter @zooclaw/design-system build:preview`

## Notes

- `scripts/verify-changed.sh` reported no locally verifiable surfaces
because the touched `web/` files are outside `web/app`; CI remains the
authoritative gate.

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR Body

## Summary

- Expand the ZooClaw design-system foundations preview with extracted Liquid Glass colors, typography, spacing, shadows, glass tiers, and an app shell sample.
- Add and refine DS component styling for Tag, Card, Button, Switch, Table, Accordion, and Alert.
- Add regression tests for preview structure/CSS contracts and token/component behavior.

## Validation

- `pnpm --filter @zooclaw/design-system test`
- `pnpm --filter @zooclaw/design-system tsc`
- `pnpm --filter @zooclaw/design-system lint`
- `pnpm --filter @zooclaw/design-system build:preview`

## Notes

- `scripts/verify-changed.sh` reported no locally verifiable surfaces because the touched `web/` files are outside `web/app`; CI remains the authoritative gate.


## fix(pack-store): copy pack archives via r2-access-worker (#2754)

- **SHA**: 9c2755d14139a05cf99d0bca92b905b5ddb9d4fe
- **作者**: bill-srp
- **日期**: 2026-07-07T05:50:02Z
- **PR**: #2754

### Commit Message

```
fix(pack-store): copy pack archives via r2-access-worker (#2754)

## Summary
- Move pack-archive copies off the backend boto3/S3 path into
`services/r2-access-worker`: new `POST /copy` endpoint (service-token
auth via `COPY_SERVICE_TOKEN` secret, key/extension validation, 100 MB
cap) that performs the copy through the Worker's R2 binding and
**restamps** destination `customMetadata` (`org_id`/`pack_id` from the
destination key + `source_key`)
- Add backend client `app/services/agent_packs_worker.py`
(`copy_pack_archive`); worker URL derived from
`R2_AGENT_PACKS_UPLOAD_URL`, authenticated with new
`R2_AGENT_PACKS_COPY_TOKEN` setting; failures surface as
`pack.archive_copy_failed` (502) without forwarding worker statuses to
API clients
- Migrate both backend copy call sites:
`paid_listing_service._copy_submission_asset` (webapp private→public
share) and `pack_test_submission_service.promote_test_run_asset`
(pack-test promotion); delete the now-unused
`R2StorageClient.copy_object`
- Fix `_asset_ext` mapping `.tar.gz` sources to `.gz` destination keys
- Design spec:
`docs/superpowers/specs/2026-07-07-pack-archive-copy-via-worker.md`

## Root cause
The webapp share flow (PR #2735) copied the pack archive with boto3
`CopyObject` using the backend's R2 S3 credentials. Pack archives are
written exclusively through Cloudflare Worker R2 **bindings**
(r2-access-worker `/upload`, console upload routes) into
`zooclaw-agent-packs`, while the backend's
`require_agent_packs_bucket()` silently falls back to the public bucket
(`gem-image`) when `R2_AGENT_PACKS_BUCKET_NAME` is unset — so the share
copy failed with `NoSuchKey` (reproduced with the backend's own
credentials: the promoted archive HEADs 200 in `zooclaw-agent-packs`,
404 in `gem-image`). `promote_test_run_asset` shared the same failure
mode. Delegating the copy to the worker that owns the bucket binding
removes the backend S3 dependency entirely, and restamping metadata on
copy stops the stale `pack_id=<display_id>` metadata that boto3's
default `MetadataDirective=COPY` propagated.

## Deployment prerequisites
- `COPY_SERVICE_TOKEN` is a GitHub environment secret (`staging` +
`production`, already provisioned); `deploy-r2-access-worker.yml` now
applies it to the worker on every deploy via wrangler-action `secrets:`
- Set `R2_AGENT_PACKS_COPY_TOKEN` (same value per env) in claw-interface
env via gcp-foundation
- Rollout order (addresses the Codex review note): merging auto-deploys
the staging worker; cut the `r2-access-worker-v1.1.0-release` tag (prod
worker) **before** the backend release that carries this change, so
`/copy` exists before anything calls it

## Test plan
- [x] r2-access-worker: `vitest run` — 33 passed (14 new `/copy` tests:
auth, key validation, missing source, oversize, metadata restamp); `tsc
--noEmit` clean
- [x] claw-interface: `pytest tests/unit/test_agent_packs_worker.py
tests/unit/test_paid_listing_service.py
tests/unit/test_public_listing_service.py
tests/unit/test_pack_test_service.py -q` — 54 passed (new client tests +
call-site swaps + `.tar.gz` extension regression test)
- [x] `bash scripts/verify-py.sh` — all checks passed
- [ ] Staging: share a private pack end-to-end after
`COPY_SERVICE_TOKEN` / `R2_AGENT_PACKS_COPY_TOKEN` are provisioned
```

### PR Body

## Summary
- Move pack-archive copies off the backend boto3/S3 path into `services/r2-access-worker`: new `POST /copy` endpoint (service-token auth via `COPY_SERVICE_TOKEN` secret, key/extension validation, 100 MB cap) that performs the copy through the Worker's R2 binding and **restamps** destination `customMetadata` (`org_id`/`pack_id` from the destination key + `source_key`)
- Add backend client `app/services/agent_packs_worker.py` (`copy_pack_archive`); worker URL derived from `R2_AGENT_PACKS_UPLOAD_URL`, authenticated with new `R2_AGENT_PACKS_COPY_TOKEN` setting; failures surface as `pack.archive_copy_failed` (502) without forwarding worker statuses to API clients
- Migrate both backend copy call sites: `paid_listing_service._copy_submission_asset` (webapp private→public share) and `pack_test_submission_service.promote_test_run_asset` (pack-test promotion); delete the now-unused `R2StorageClient.copy_object`
- Fix `_asset_ext` mapping `.tar.gz` sources to `.gz` destination keys
- Design spec: `docs/superpowers/specs/2026-07-07-pack-archive-copy-via-worker.md`

## Root cause
The webapp share flow (PR #2735) copied the pack archive with boto3 `CopyObject` using the backend's R2 S3 credentials. Pack archives are written exclusively through Cloudflare Worker R2 **bindings** (r2-access-worker `/upload`, console upload routes) into `zooclaw-agent-packs`, while the backend's `require_agent_packs_bucket()` silently falls back to the public bucket (`gem-image`) when `R2_AGENT_PACKS_BUCKET_NAME` is unset — so the share copy failed with `NoSuchKey` (reproduced with the backend's own credentials: the promoted archive HEADs 200 in `zooclaw-agent-packs`, 404 in `gem-image`). `promote_test_run_asset` shared the same failure mode. Delegating the copy to the worker that owns the bucket binding removes the backend S3 dependency entirely, and restamping metadata on copy stops the stale `pack_id=<display_id>` metadata that boto3's default `MetadataDirective=COPY` propagated.

## Deployment prerequisites
- `COPY_SERVICE_TOKEN` is a GitHub environment secret (`staging` + `production`, already provisioned); `deploy-r2-access-worker.yml` now applies it to the worker on every deploy via wrangler-action `secrets:`
- Set `R2_AGENT_PACKS_COPY_TOKEN` (same value per env) in claw-interface env via gcp-foundation
- Rollout order (addresses the Codex review note): merging auto-deploys the staging worker; cut the `r2-access-worker-v1.1.0-release` tag (prod worker) **before** the backend release that carries this change, so `/copy` exists before anything calls it

## Test plan
- [x] r2-access-worker: `vitest run` — 33 passed (14 new `/copy` tests: auth, key validation, missing source, oversize, metadata restamp); `tsc --noEmit` clean
- [x] claw-interface: `pytest tests/unit/test_agent_packs_worker.py tests/unit/test_paid_listing_service.py tests/unit/test_public_listing_service.py tests/unit/test_pack_test_service.py -q` — 54 passed (new client tests + call-site swaps + `.tar.gz` extension regression test)
- [x] `bash scripts/verify-py.sh` — all checks passed
- [ ] Staging: share a private pack end-to-end after `COPY_SERVICE_TOKEN` / `R2_AGENT_PACKS_COPY_TOKEN` are provisioned


## feat(ios): update login and onboarding UI (#2747)

- **SHA**: eafeed4f7f1f80e12777cb0a1d351ba1254e6d22
- **作者**: shana-srp
- **日期**: 2026-07-07T03:27:37Z
- **PR**: #2747

### Commit Message

```
feat(ios): update login and onboarding UI (#2747)

## Summary
- add the new onboarding login modal and preserve email, Google, and
Apple auth flows
- update iOS login/onboarding/settings assets and primary button color
tokens
- restore Google sign-in lookup for local staging builds and add
onboarding coverage

## Verification
- env DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
xcodebuild build -project ios/ZooClaw/ZooClaw.xcodeproj -scheme ZooClaw
-configuration Debug -destination
id=EDFB6195-BD59-4FD5-B86D-BA1A57B8C351 -derivedDataPath
build/DerivedData MARKETING_VERSION=1.8.0 build

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

## Summary
- add the new onboarding login modal and preserve email, Google, and Apple auth flows
- update iOS login/onboarding/settings assets and primary button color tokens
- restore Google sign-in lookup for local staging builds and add onboarding coverage

## Verification
- env DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer xcodebuild build -project ios/ZooClaw/ZooClaw.xcodeproj -scheme ZooClaw -configuration Debug -destination id=EDFB6195-BD59-4FD5-B86D-BA1A57B8C351 -derivedDataPath build/DerivedData MARKETING_VERSION=1.8.0 build

## fix(app): 修复侧边栏用户指南跳转 (#2736)

- **SHA**: b8525c160cac2bfe62ce3b996636e0f903cfaa58
- **作者**: lynn Zhuang
- **日期**: 2026-07-07T03:25:09Z
- **PR**: #2736

### Commit Message

```
fix(app): 修复侧边栏用户指南跳转 (#2736)

## 变更内容

- 修复侧边栏「User Guide」在本地预览时误进入应用内 `/tips/...` 路径，导致 Next.js 报 `Missing
<html> and <body> tags in the root layout` 的问题。
- 增加旧 Tips 路径兼容跳转，覆盖 `/tips/en`、`/en/tips/en` 等入口。
- 保留 `lang` 和 `theme` 参数，并支持通过 `NEXT_PUBLIC_TIPS_ORIGIN` 覆盖 Tips 站点域名。

## 验证

- 本地预览：`/tips/en` 会跳转到 `https://zooclaw.ai/tips/?lang=en`
- 本地预览：`/en/tips/en` 会跳转到 `https://zooclaw.ai/tips/?lang=en`
- 本地预览：`/tips/agentstudioguide?lang=zh&theme=dark` 会跳转到
`https://zooclaw.ai/tips/agentstudioguide?lang=zh&theme=dark`
- `bash scripts/verify-web.sh ...`
- `bash scripts/verify-changed.sh`
- GitHub PR checks: 44/44 passed

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
```

### PR Body

## 变更内容

- 修复侧边栏「User Guide」在本地预览时误进入应用内 `/tips/...` 路径，导致 Next.js 报 `Missing <html> and <body> tags in the root layout` 的问题。
- 增加旧 Tips 路径兼容跳转，覆盖 `/tips/en`、`/en/tips/en` 等入口。
- 保留 `lang` 和 `theme` 参数，并支持通过 `NEXT_PUBLIC_TIPS_ORIGIN` 覆盖 Tips 站点域名。

## 验证

- 本地预览：`/tips/en` 会跳转到 `https://zooclaw.ai/tips/?lang=en`
- 本地预览：`/en/tips/en` 会跳转到 `https://zooclaw.ai/tips/?lang=en`
- 本地预览：`/tips/agentstudioguide?lang=zh&theme=dark` 会跳转到 `https://zooclaw.ai/tips/agentstudioguide?lang=zh&theme=dark`
- `bash scripts/verify-web.sh ...`
- `bash scripts/verify-changed.sh`
- GitHub PR checks: 44/44 passed


## fix(web): restore specialists hub layout (#2742)

- **SHA**: 938723a48a08a306996efa0732f6128306687aa5
- **作者**: lynn Zhuang
- **日期**: 2026-07-07T03:05:54Z
- **PR**: #2742

### Commit Message

```
fix(web): restore specialists hub layout (#2742)

## Summary
- Restore the AI Specialists Hub to the pre-#2679 app-owned layout and
styling.
- Remove the app-side `@zooclaw/design-system` dependency/import path
introduced for this page.
- Keep the later paid-pack purchase flow intact and add a regression
test for the broken DS layout path.

## Root cause
PR #2679 migrated Specialists Hub onto the ZooClaw design-system
components/tokens, which changed the page structure and visual behavior.
This restores the original app-owned UI while preserving later business
behavior added after #2679.

## Test plan
- [x] `corepack pnpm --dir web/app exec vitest run
tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx
tests/unit/app/agents-manager/AgentCard.unit.spec.tsx
tests/unit/app/agents-manager-client.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh 'web/app/next.config.ts'
'web/app/package.json'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/AgentsManagerClient.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentCard.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentModal.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/SkillTags.tsx'
'web/app/src/app/globals.css'
'web/app/src/components/ClawConnectionStatus.tsx'
'web/app/tests/unit/app/agents-manager/AgentCard.unit.spec.tsx'
'web/app/tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] Mock preview on latest `origin/main`: `/en/agents-manager` renders
in light and dark mode with 8 cards, no `[data-agents-manager-page]`
marker, and `lg:grid-cols-3`.

## Preview
- Light: `.screenshots/specialists-hub-latest-main-light.png`
- Dark: `.screenshots/specialists-hub-latest-main-dark.png`

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
```

### PR Body

## Summary
- Restore the AI Specialists Hub to the pre-#2679 app-owned layout and styling.
- Remove the app-side `@zooclaw/design-system` dependency/import path introduced for this page.
- Keep the later paid-pack purchase flow intact and add a regression test for the broken DS layout path.

## Root cause
PR #2679 migrated Specialists Hub onto the ZooClaw design-system components/tokens, which changed the page structure and visual behavior. This restores the original app-owned UI while preserving later business behavior added after #2679.

## Test plan
- [x] `corepack pnpm --dir web/app exec vitest run tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx tests/unit/app/agents-manager/AgentCard.unit.spec.tsx tests/unit/app/agents-manager-client.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh 'web/app/next.config.ts' 'web/app/package.json' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/AgentsManagerClient.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentCard.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentModal.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/SkillTags.tsx' 'web/app/src/app/globals.css' 'web/app/src/components/ClawConnectionStatus.tsx' 'web/app/tests/unit/app/agents-manager/AgentCard.unit.spec.tsx' 'web/app/tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] Mock preview on latest `origin/main`: `/en/agents-manager` renders in light and dark mode with 8 cards, no `[data-agents-manager-page]` marker, and `lg:grid-cols-3`.

## Preview
- Light: `.screenshots/specialists-hub-latest-main-light.png`
- Dark: `.screenshots/specialists-hub-latest-main-dark.png`


## fix(chat-replay): authorize session thread shares (#2751)

- **SHA**: 49a739095972edba333d153a0be2121446e47f8a
- **作者**: kaka-srp
- **日期**: 2026-07-07T02:49:10Z
- **PR**: #2751

### Commit Message

```
fix(chat-replay): authorize session thread shares (#2751)

## Summary
- authorize chat replay creation from canonical OpenClaw session-channel
records
- keep current-org workspace ownership as the join point, even when the
cached workspace `session_channel_id` is empty
- scope session-thread replay posts to the recorded Mattermost thread
root

## Validation
- `/home/node/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_chat_replay_create.py -q`
- `/home/node/.venvs/claw-interface/bin/python -m ruff check
services/claw-interface/app/services/chat_replay/create.py
services/claw-interface/tests/unit/test_chat_replay_create.py`
- `/home/node/.venvs/claw-interface/bin/python -m ruff format --check
services/claw-interface/app/services/chat_replay/create.py
services/claw-interface/tests/unit/test_chat_replay_create.py`
- `bash scripts/verify-changed.sh`
```

### PR Body

## Summary
- authorize chat replay creation from canonical OpenClaw session-channel records
- keep current-org workspace ownership as the join point, even when the cached workspace `session_channel_id` is empty
- scope session-thread replay posts to the recorded Mattermost thread root

## Validation
- `/home/node/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_chat_replay_create.py -q`
- `/home/node/.venvs/claw-interface/bin/python -m ruff check services/claw-interface/app/services/chat_replay/create.py services/claw-interface/tests/unit/test_chat_replay_create.py`
- `/home/node/.venvs/claw-interface/bin/python -m ruff format --check services/claw-interface/app/services/chat_replay/create.py services/claw-interface/tests/unit/test_chat_replay_create.py`
- `bash scripts/verify-changed.sh`

