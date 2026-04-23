# ecap-workspace Commits - Last 7 Days


## 2026-04-23


## fa75cf8

**作者**: tim-srp
**日期**: 2026-04-22T15:21:02Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/fa75cf85645badee84fea3f63ffd3a3329a6809c](https://github.com/SerendipityOneInc/ecap-workspace/commit/fa75cf85645badee84fea3f63ffd3a3329a6809c)

### Commit Message
```
docs: add E2E test suite documentation (#1241)

## Summary
- Add `docs/e2e/README.md` documenting the full E2E test suite
- Covers architecture (auth setup, overlay suppression, shared session),
complete test inventory (35 specs), utilities, and CI config

## Test plan
- [ ] Documentation only, no code changes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR #1241: docs: add E2E test suite documentation

## Summary
- Add `docs/e2e/README.md` documenting the full E2E test suite
- Covers architecture (auth setup, overlay suppression, shared session), complete test inventory (35 specs), utilities, and CI config

## Test plan
- [ ] Documentation only, no code changes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 03a01e3

**作者**: tim-srp
**日期**: 2026-04-22T15:06:11Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/03a01e3f6e0ec48671cf373e281943bd3b3bd6a6](https://github.com/SerendipityOneInc/ecap-workspace/commit/03a01e3f6e0ec48671cf373e281943bd3b3bd6a6)

### Commit Message
```
feat: auto-upgrade bot image on subscription recovery (#1221)

## Summary
- When a user resubscribes, `start_user_bots` now auto-upgrades the
bot's deployment image to the latest published release before starting,
so stopped bots always come back on the newest version
- Add `release_repo.get_latest_published_release()` — queries only the
`published` flag (not `is_latest`) to handle edge case where a newer
draft release steals the `is_latest` marker
- Add `scripts/upgrade_srpone_bot_image.py` with `--scope` flag
(internal/external/all) for batch upgrades
- Add `scripts/bot_version_stats.py` for version distribution reporting
- Add `scripts/README.md` documenting all scripts

## Test plan
- [ ] Verify `get_latest_published_release()` returns the correct
release when `is_latest` is on a different (draft) release
- [ ] Verify `_upgrade_bot_image_if_needed()` upgrades outdated bots and
skips up-to-date ones
- [ ] Verify `start_user_bots()` still works when no published release
exists (graceful fallback)
- [ ] Verify image upgrade failure does not block bot startup
(best-effort behavior)
- [ ] Test `upgrade_srpone_bot_image.py --scope internal/external/all`
with `DRY_RUN=1`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR #1221: feat: auto-upgrade bot image on subscription recovery

## Summary
- When a user resubscribes, `start_user_bots` now auto-upgrades the bot's deployment image to the latest published release before starting, so stopped bots always come back on the newest version
- Add `release_repo.get_latest_published_release()` — queries only the `published` flag (not `is_latest`) to handle edge case where a newer draft release steals the `is_latest` marker
- Add `scripts/upgrade_srpone_bot_image.py` with `--scope` flag (internal/external/all) for batch upgrades
- Add `scripts/bot_version_stats.py` for version distribution reporting
- Add `scripts/README.md` documenting all scripts

## Test plan
- [ ] Verify `get_latest_published_release()` returns the correct release when `is_latest` is on a different (draft) release
- [ ] Verify `_upgrade_bot_image_if_needed()` upgrades outdated bots and skips up-to-date ones
- [ ] Verify `start_user_bots()` still works when no published release exists (graceful fallback)
- [ ] Verify image upgrade failure does not block bot startup (best-effort behavior)
- [ ] Test `upgrade_srpone_bot_image.py --scope internal/external/all` with `DRY_RUN=1`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 8f04abf

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T12:53:52Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/8f04abf4ff8da4bc11ae84374c8f4adaf0c103df](https://github.com/SerendipityOneInc/ecap-workspace/commit/8f04abf4ff8da4bc11ae84374c8f4adaf0c103df)

### Commit Message
```
fix(security): clear 7 CodeQL alerts (permissions / stack trace / ReDoS) (#1235)

## Summary

**PR 1/6** of a security-alert cleanup series. Clears **7 CodeQL
alerts** with source-only changes. Dependabot work follows in PR 2 (Next
patch), PR 3 (transitive overrides), PR 4 (Electron major), PR 5/6
(logging triage).

See plan: `/home/node/.claude/plans/security-and-alerts-vast-sprout.md`

## Changes

| File | Alert(s) | Fix |
|---|---|---|
| `.github/workflows/pr-size-check-reusable.yml` |
[#469](https://github.com/SerendipityOneInc/ecap-workspace/security/code-scanning/469)
`actions/missing-workflow-permissions` | Add top-level `permissions:`
(contents: read, issues: write, pull-requests: write — required for
sticky comment). |
| `services/claw-interface/app/routes/litellm.py:1544-1546` |
[#118](https://github.com/SerendipityOneInc/ecap-workspace/security/code-scanning/118)
`py/stack-trace-exposure` | SSE response body fixed to `{"error":
"Streaming error"}`; full detail stays in `logger.exception`. |
|
`services/claw-interface/app/routes/session/utils.py::_sanitize_content_for_title`
|
[#68-72](https://github.com/SerendipityOneInc/ecap-workspace/security/code-scanning/72)
(5x) `py/polynomial-redos` | Cap input at 8192 chars + pre-compile the 7
patterns. Input cap is the structural fix CodeQL recognises; **rule
order preserved bit-for-bit** so existing sanitizer behaviour (including
the dead-code video rule) is unchanged. Adds
`test_caps_oversized_input_to_bound_regex_work` to lock the cap in. |

## Out of scope (tracked separately)

- **[#452 /
#453](https://github.com/SerendipityOneInc/ecap-workspace/security/code-scanning/452)
`py/weak-sensitive-data-hashing` in `agent_catalog.py`** — two attempts
landed then reverted in this branch:
1. `hashlib.md5(..., usedforsecurity=False)` — not honored by this
specific CodeQL query (it tracks "sensitive data → weak hash", not "is
this securely hashed").
2. Wrap in `_stable_catalog_fingerprint` helper — CodeQL's
inter-procedural taint analysis still reaches the md5 sink, reduced
alerts 2→1 but CI "new alerts" gate still red.

The md5 digest here is a content-addressable cache key persisted in
mongo (`user.agent_pack_versions`); switching to sha256 would flip every
installed agent to "update available" for every existing user on deploy.
**Post-merge plan**: dismiss #452 / #453 via the `code-scanning/alerts`
API with `dismissed_reason=false positive` and a note about the
cache-key role.

## Test plan
- [x] `pyright app/ tests/` — clean
- [x] `ruff check app/ tests/` — clean
- [x] `ruff format --check app/ tests/` — clean
- [x] `pytest tests/unit/test_agent_catalog.py
tests/unit/test_session_utils.py tests/unit/test_litellm_endpoints.py` —
**76 passed** (including new
`test_caps_oversized_input_to_bound_regex_work`)
- [ ] CodeQL re-scan after merge: open count 36 → **~29** (36 − 7
cleared here; #452/#453 dismissed separately)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1235: fix(security): clear 7 CodeQL alerts (permissions / stack trace / ReDoS)

## Summary

**PR 1/6** of a security-alert cleanup series. Clears **7 CodeQL alerts** with source-only changes. Dependabot work follows in PR 2 (Next patch), PR 3 (transitive overrides), PR 4 (Electron major), PR 5/6 (logging triage).

See plan: `/home/node/.claude/plans/security-and-alerts-vast-sprout.md`

## Changes

| File | Alert(s) | Fix |
|---|---|---|
| `.github/workflows/pr-size-check-reusable.yml` | [#469](https://github.com/SerendipityOneInc/ecap-workspace/security/code-scanning/469) `actions/missing-workflow-permissions` | Add top-level `permissions:` (contents: read, issues: write, pull-requests: write — required for sticky comment). |
| `services/claw-interface/app/routes/litellm.py:1544-1546` | [#118](https://github.com/SerendipityOneInc/ecap-workspace/security/code-scanning/118) `py/stack-trace-exposure` | SSE response body fixed to `{"error": "Streaming error"}`; full detail stays in `logger.exception`. |
| `services/claw-interface/app/routes/session/utils.py::_sanitize_content_for_title` | [#68-72](https://github.com/SerendipityOneInc/ecap-workspace/security/code-scanning/72) (5x) `py/polynomial-redos` | Cap input at 8192 chars + pre-compile the 7 patterns. Input cap is the structural fix CodeQL recognises; **rule order preserved bit-for-bit** so existing sanitizer behaviour (including the dead-code video rule) is unchanged. Adds `test_caps_oversized_input_to_bound_regex_work` to lock the cap in. |

## Out of scope (tracked separately)

- **[#452 / #453](https://github.com/SerendipityOneInc/ecap-workspace/security/code-scanning/452) `py/weak-sensitive-data-hashing` in `agent_catalog.py`** — two attempts landed then reverted in this branch:
  1. `hashlib.md5(..., usedforsecurity=False)` — not honored by this specific CodeQL query (it tracks "sensitive data → weak hash", not "is this securely hashed").
  2. Wrap in `_stable_catalog_fingerprint` helper — CodeQL's inter-procedural taint analysis still reaches the md5 sink, reduced alerts 2→1 but CI "new alerts" gate still red.

  The md5 digest here is a content-addressable cache key persisted in mongo (`user.agent_pack_versions`); switching to sha256 would flip every installed agent to "update available" for every existing user on deploy. **Post-merge plan**: dismiss #452 / #453 via the `code-scanning/alerts` API with `dismissed_reason=false positive` and a note about the cache-key role.

## Test plan
- [x] `pyright app/ tests/` — clean
- [x] `ruff check app/ tests/` — clean
- [x] `ruff format --check app/ tests/` — clean
- [x] `pytest tests/unit/test_agent_catalog.py tests/unit/test_session_utils.py tests/unit/test_litellm_endpoints.py` — **76 passed** (including new `test_caps_oversized_input_to_bound_regex_work`)
- [ ] CodeQL re-scan after merge: open count 36 → **~29** (36 − 7 cleared here; #452/#453 dismissed separately)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 6c19daf

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T12:20:59Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/6c19daf620de1738c430f45d3230068c6185d5be](https://github.com/SerendipityOneInc/ecap-workspace/commit/6c19daf620de1738c430f45d3230068c6185d5be)

### Commit Message
```
chore(web): clean barrel re-exports + dead factories — first pass B6 (#1234)

## Summary
- First batch of unused-exports cleanup toward the B-track `exports`
hard-gate.
- Scope here: **barrels + entire-dead files + obvious local-only
helpers**.
- Remaining ~21 scattered exports (in `src/lib/**`, `src/app/_seo.ts`,
hooks, contexts, e2e) ship in follow-up PR(s).
- **exports category stays informational** in `02-dead-code.sh`;
promotion to hard-gate happens once the remaining list hits zero.

## Why split
knip reported **39** unused exports on main. Cleaning all at once would
be a 1500+ line diff; splitting by "category of fix" makes each PR
reviewable in isolation. This first PR covers the risk-free structural
stuff:

| Category | Why safe first |
|---|---|
| Barrel re-exports | Just delete lines; live imports work unchanged |
| Entire-dead component files | No caller at all (verified by grep +
knip) |
| Single-file local helpers | Convert `export function` → `function`
when only internal caller |
| Legacy consumer ignore | `config/examples/**` pairs with
already-ignored `ExampleShowcase` |

## Changes

| File | Change |
|---|---|
| `src/components/ui/index.ts` | Drop `Input`/`ToastProvider`/`useToast`
re-exports (4→2 lines) |
| `src/components/ui/Input.tsx` | **Deleted** — zero callers |
| `src/components/mattermost/index.ts` | Drop `useMMAuth` re-export |
| `src/lib/api/index.ts` | Reduce to single live re-export `api` |
| `src/lib/featureVisibility.ts` | `isSrpOneWhitelistedEmail` → local
(only caller is `canViewInternalOnlyFeatures` same file) |
| `tests/unit/helpers/index.ts` | 17 re-exports → 5 live ones |
| `tests/unit/helpers/factories.ts` | Drop 8 dead factory functions +
orphan `SessionItem` import |
| `web/knip.config.ts` | Add `src/config/examples/**` to legacy ignore
list |

`src/config/examples/**` explanation: all consumers are inside
`ExampleShowcase/*` and `AgentChatClient/index.tsx` — both already in
the legacy ignore list from B5. knip can't see those callers, so it
flags the config exports as unused. Adding the pair here freezes them
together.

8 files, +9 / -237.

## Local verification
- `pnpm lint:imports` — exit 0, 9 known violations ignored
- `pnpm test:unit` — **4014 tests pass**
- `npx tsc --noEmit` — clean
- `pnpm lint` — clean
- `pnpm exec knip --include exports` — 21 remaining (was 39)

## Follow-up scope (not in this PR)
21 scattered exports across:
- `src/app/_seo.ts` (9) — most likely become local helpers
- `src/app/[locale]/chat/hooks/*` (3)
- `src/lib/api/{openclaw,user,auth-middleware}.ts` (11)
- `src/lib/{skills/*, use-cases, tracking, agentCatalogCache,
auth/subscriptionStorage}.ts` (17)
- `src/hooks/useCustomAgentPublishes.ts` (4)
- `src/contexts/AppEnvironmentContext.tsx` (1) /
`src/components/{LocaleLink, billing/SubscriptionPanel}.tsx` (2)
- `tests/e2e/{fixtures, utils}.ts` (6)

Once all reach zero, B6-final PR will add `exports` to `02-dead-code.sh`
`--include`.

## Test plan
- [x] 4014 unit tests pass
- [x] tsc + eslint clean
- [x] No dep-cruiser regression
- [ ] CI confirms
- [ ] Reviewer sanity-checks the `config/examples/**` legacy-ignore
addition

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1234: chore(web): clean barrel re-exports + dead factories — first pass B6

## Summary
- First batch of unused-exports cleanup toward the B-track `exports` hard-gate.
- Scope here: **barrels + entire-dead files + obvious local-only helpers**.
- Remaining ~21 scattered exports (in `src/lib/**`, `src/app/_seo.ts`, hooks, contexts, e2e) ship in follow-up PR(s).
- **exports category stays informational** in `02-dead-code.sh`; promotion to hard-gate happens once the remaining list hits zero.

## Why split
knip reported **39** unused exports on main. Cleaning all at once would be a 1500+ line diff; splitting by "category of fix" makes each PR reviewable in isolation. This first PR covers the risk-free structural stuff:

| Category | Why safe first |
|---|---|
| Barrel re-exports | Just delete lines; live imports work unchanged |
| Entire-dead component files | No caller at all (verified by grep + knip) |
| Single-file local helpers | Convert `export function` → `function` when only internal caller |
| Legacy consumer ignore | `config/examples/**` pairs with already-ignored `ExampleShowcase` |

## Changes

| File | Change |
|---|---|
| `src/components/ui/index.ts` | Drop `Input`/`ToastProvider`/`useToast` re-exports (4→2 lines) |
| `src/components/ui/Input.tsx` | **Deleted** — zero callers |
| `src/components/mattermost/index.ts` | Drop `useMMAuth` re-export |
| `src/lib/api/index.ts` | Reduce to single live re-export `api` |
| `src/lib/featureVisibility.ts` | `isSrpOneWhitelistedEmail` → local (only caller is `canViewInternalOnlyFeatures` same file) |
| `tests/unit/helpers/index.ts` | 17 re-exports → 5 live ones |
| `tests/unit/helpers/factories.ts` | Drop 8 dead factory functions + orphan `SessionItem` import |
| `web/knip.config.ts` | Add `src/config/examples/**` to legacy ignore list |

`src/config/examples/**` explanation: all consumers are inside `ExampleShowcase/*` and `AgentChatClient/index.tsx` — both already in the legacy ignore list from B5. knip can't see those callers, so it flags the config exports as unused. Adding the pair here freezes them together.

8 files, +9 / -237.

## Local verification
- `pnpm lint:imports` — exit 0, 9 known violations ignored
- `pnpm test:unit` — **4014 tests pass**
- `npx tsc --noEmit` — clean
- `pnpm lint` — clean
- `pnpm exec knip --include exports` — 21 remaining (was 39)

## Follow-up scope (not in this PR)
21 scattered exports across:
- `src/app/_seo.ts` (9) — most likely become local helpers
- `src/app/[locale]/chat/hooks/*` (3)
- `src/lib/api/{openclaw,user,auth-middleware}.ts` (11)
- `src/lib/{skills/*, use-cases, tracking, agentCatalogCache, auth/subscriptionStorage}.ts` (17)
- `src/hooks/useCustomAgentPublishes.ts` (4)
- `src/contexts/AppEnvironmentContext.tsx` (1) / `src/components/{LocaleLink, billing/SubscriptionPanel}.tsx` (2)
- `tests/e2e/{fixtures, utils}.ts` (6)

Once all reach zero, B6-final PR will add `exports` to `02-dead-code.sh` `--include`.

## Test plan
- [x] 4014 unit tests pass
- [x] tsc + eslint clean
- [x] No dep-cruiser regression
- [ ] CI confirms
- [ ] Reviewer sanity-checks the `config/examples/**` legacy-ignore addition

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T12:20:46Z): /lgtm

---

## ebe8465

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T12:11:13Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/ebe8465cb2260fcbdc13736c0b0c360f4aae771d](https://github.com/SerendipityOneInc/ecap-workspace/commit/ebe8465cb2260fcbdc13736c0b0c360f4aae771d)

### Commit Message
```
ci: bump pnpm/action-setup v4→v5 + checkout v4→v6 stragglers (#1233)

## Summary
- Clear the Node.js 20 deprecation warning from `pnpm/action-setup@v4`
(seen on e2e run
[24775282279](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24775282279)).
- Bump 5× `pnpm/action-setup@v4 → v5` (v5.0.0 is the same action
re-released on Node 24).
- Sweep 3× remaining `actions/checkout@v4 → v6` in
`claude-arch-review.yaml`, `pr-size-check-reusable.yml`,
`service-deploy.yml` so the whole repo is on Node 24 action runtimes,
consistent with the pattern from b672e4f7.

## Out of scope
- The cosmetic `Post Run actions/checkout@v6: git failed with exit 128`
annotation in the same e2e run is a known runner cleanup issue
(`actions/checkout#1541`); no action-version bump fixes it.
- Similar Node 20 / stale-action stragglers in
`SerendipityOneInc/srp-actions` (checkout@v3, setup-python@v4,
google-github-actions/*@v1) — will be addressed in a separate PR against
that repo.

## Test plan
- [ ] CI green on this PR (code-quality, pr-size-check, any e2e
retrigger)
- [ ] Manually re-run `e2e` workflow after merge and confirm the
`pnpm/action-setup@v4` Node 20 annotation is gone

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1233: ci: bump pnpm/action-setup v4→v5 + checkout v4→v6 stragglers

## Summary
- Clear the Node.js 20 deprecation warning from `pnpm/action-setup@v4` (seen on e2e run [24775282279](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24775282279)).
- Bump 5× `pnpm/action-setup@v4 → v5` (v5.0.0 is the same action re-released on Node 24).
- Sweep 3× remaining `actions/checkout@v4 → v6` in `claude-arch-review.yaml`, `pr-size-check-reusable.yml`, `service-deploy.yml` so the whole repo is on Node 24 action runtimes, consistent with the pattern from b672e4f7.

## Out of scope
- The cosmetic `Post Run actions/checkout@v6: git failed with exit 128` annotation in the same e2e run is a known runner cleanup issue (`actions/checkout#1541`); no action-version bump fixes it.
- Similar Node 20 / stale-action stragglers in `SerendipityOneInc/srp-actions` (checkout@v3, setup-python@v4, google-github-actions/*@v1) — will be addressed in a separate PR against that repo.

## Test plan
- [ ] CI green on this PR (code-quality, pr-size-check, any e2e retrigger)
- [ ] Manually re-run `e2e` workflow after merge and confirm the `pnpm/action-setup@v4` Node 20 annotation is gone

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T12:11:02Z): /lgtm

---

## bc28a16

**作者**: tim-srp
**日期**: 2026-04-22T11:57:31Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/bc28a16f46bf774f3f8f93eb37f002bc4ebc8293](https://github.com/SerendipityOneInc/ecap-workspace/commit/bc28a16f46bf774f3f8f93eb37f002bc4ebc8293)

### Commit Message
```
fix(e2e): suppress blocking overlays + improve response detection (#1229)

## Summary
- Suppress all known overlay modals (GuideTourModal, CompensationPopup,
SeedanceLaunchModal) in E2E auth setup via `E2E_OVERLAY_SUPPRESSION` map
with `{uid}` placeholder support
- Add stop button to `waitForResponseStart()` race for earlier response
detection
- Rename workflow from PandaClaw to ZooClaw

## Test plan
- [ ] E2E tests pass on production without overlay interception errors
- [ ] New overlay modals can be added by updating
`E2E_OVERLAY_SUPPRESSION` in `test-data.ts`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR #1229: fix(e2e): suppress blocking overlays + improve response detection

## Summary
- Suppress all known overlay modals (GuideTourModal, CompensationPopup, SeedanceLaunchModal) in E2E auth setup via `E2E_OVERLAY_SUPPRESSION` map with `{uid}` placeholder support
- Add stop button to `waitForResponseStart()` race for earlier response detection
- Rename workflow from PandaClaw to ZooClaw

## Test plan
- [ ] E2E tests pass on production without overlay interception errors
- [ ] New overlay modals can be added by updating `E2E_OVERLAY_SUPPRESSION` in `test-data.ts`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 7b4c261

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T11:27:43Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/7b4c2615ff39e4b916ba81c791ae6286cbc3a496](https://github.com/SerendipityOneInc/ecap-workspace/commit/7b4c2615ff39e4b916ba81c791ae6286cbc3a496)

### Commit Message
```
test(web): SkillDetailClient 全面覆盖 (#894 Step 9 2/2) (#1227)

## Summary

Epic #894 Step 9 (#903) 最后一个文件 — \`SkillDetailClient.tsx\` (548 LOC) 从
0% → 43 tests 覆盖核心分支,**零源码改动**。

Step 9 两个 1200 LOC client 组件全部覆盖完成(PR #1220 SkillsSearchClient + 本 PR)。

## 覆盖

| 组 | # | 覆盖 |
|---|---|---|
| Loading / not-found | 6 | pending / notFound / 参数缺失 / 网络失败 / back 导航 /
失败但有 cache 保留 |
| Official / builtin | 5 | 匹配 runtime / source 不匹配 / builtin 分支 / 无
match / 无 uid skip |
| Community runtime 集成 | 2 | runtime match + 非 managed / cached 立即渲染 |
| Back 导航 | 1 | back → /skills/search |
| Action 按钮 | 5 | open modal / 隐藏 / 禁用态 / 未登录 / install vs manage label
|
| Modal 动作 | 6 | install / uninstall / error+toast / uninstall no toast
/ no workspace / close |
| Installed 状态 UI | 3 | community Summary / 非 community badge / 未安装 |
| 内容 section | 7 | installCommands / runtimeRequirements / files /
changelog / externalUrl |
| 指标格式化 | 4 | formatNumber / undefined / formatDate null / valid date |
| Refresh + unmount | 3 | refreshing spinner / community unmount /
runtime unmount |

## 关键观察

### Source quirk(非 bug,是设计)

\`buildCommunityDetailState\` L164-170 在**无 runtime match 时硬编码
\`installed: false\`** 覆盖 payload:

\`\`\`tsx
const baseDetail = runtimeSkill
  ? buildRuntimeSkillDetail(runtimeSkill, payload)
  : {
      ...payload,
      installState: 'not_installed' as const,
      installed: false,  // ← 硬编码
    }
\`\`\`

这是**本地优先**设计:runtime skills 是 source of truth,server 的
\`installed=true\` 会被覆盖(server 可能 stale)。测试走 runtime match path 来获得
installed=true 状态。

### Asymmetric UX

Uninstall 错误**不触发 showToast**(只 install 会):

\`\`\`tsx
} catch (error) {
  setActionError(message)
  if (action === 'install') {
    showToast(message, 'error')  // ← 只 install
  }
}
\`\`\`

测试记录了这个 contract,但 reviewer 可以讨论是否该修。

## Bug-hunt

#903 flagged "重复点击 install 防重":源码用 \`pendingAgentId\` 做 guard (L412
\`disabled={isActionDisabled || pendingAgentId !== null}\`) ✓ 没有新发现的
bug。

## Test plan

- [x] \`pnpm test:unit --
tests/unit/app/skills/detail/SkillDetailClient.unit.spec.tsx\` 43/43
passed
- [x] lint / prettier clean
- [ ] CI green

## 关联

- Epic #894 Step 9 (#903)
- 第 1 部分:PR #1220 SkillsSearchClient coverage
- **Step 9 覆盖工作到此完成**(共 74 tests = 31+43)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1227: test(web): SkillDetailClient 全面覆盖 (#894 Step 9 2/2)

## Summary

Epic #894 Step 9 (#903) 最后一个文件 — \`SkillDetailClient.tsx\` (548 LOC) 从 0% → 43 tests 覆盖核心分支,**零源码改动**。

Step 9 两个 1200 LOC client 组件全部覆盖完成(PR #1220 SkillsSearchClient + 本 PR)。

## 覆盖

| 组 | # | 覆盖 |
|---|---|---|
| Loading / not-found | 6 | pending / notFound / 参数缺失 / 网络失败 / back 导航 / 失败但有 cache 保留 |
| Official / builtin | 5 | 匹配 runtime / source 不匹配 / builtin 分支 / 无 match / 无 uid skip |
| Community runtime 集成 | 2 | runtime match + 非 managed / cached 立即渲染 |
| Back 导航 | 1 | back → /skills/search |
| Action 按钮 | 5 | open modal / 隐藏 / 禁用态 / 未登录 / install vs manage label |
| Modal 动作 | 6 | install / uninstall / error+toast / uninstall no toast / no workspace / close |
| Installed 状态 UI | 3 | community Summary / 非 community badge / 未安装 |
| 内容 section | 7 | installCommands / runtimeRequirements / files / changelog / externalUrl |
| 指标格式化 | 4 | formatNumber / undefined / formatDate null / valid date |
| Refresh + unmount | 3 | refreshing spinner / community unmount / runtime unmount |

## 关键观察

### Source quirk(非 bug,是设计)

\`buildCommunityDetailState\` L164-170 在**无 runtime match 时硬编码 \`installed: false\`** 覆盖 payload:

\`\`\`tsx
const baseDetail = runtimeSkill
  ? buildRuntimeSkillDetail(runtimeSkill, payload)
  : {
      ...payload,
      installState: 'not_installed' as const,
      installed: false,  // ← 硬编码
    }
\`\`\`

这是**本地优先**设计:runtime skills 是 source of truth,server 的 \`installed=true\` 会被覆盖(server 可能 stale)。测试走 runtime match path 来获得 installed=true 状态。

### Asymmetric UX

Uninstall 错误**不触发 showToast**(只 install 会):

\`\`\`tsx
} catch (error) {
  setActionError(message)
  if (action === 'install') {
    showToast(message, 'error')  // ← 只 install
  }
}
\`\`\`

测试记录了这个 contract,但 reviewer 可以讨论是否该修。

## Bug-hunt

#903 flagged "重复点击 install 防重":源码用 \`pendingAgentId\` 做 guard (L412 \`disabled={isActionDisabled || pendingAgentId !== null}\`) ✓ 没有新发现的 bug。

## Test plan

- [x] \`pnpm test:unit -- tests/unit/app/skills/detail/SkillDetailClient.unit.spec.tsx\` 43/43 passed
- [x] lint / prettier clean
- [ ] CI green

## 关联

- Epic #894 Step 9 (#903)
- 第 1 部分:PR #1220 SkillsSearchClient coverage
- **Step 9 覆盖工作到此完成**(共 74 tests = 31+43)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T11:27:32Z): /lgtm

---

## b672e4f

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T11:27:09Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/b672e4f760e7cb875684ceee0252773abaf84fc7](https://github.com/SerendipityOneInc/ecap-workspace/commit/b672e4f760e7cb875684ceee0252773abaf84fc7)

### Commit Message
```
ci(codex-review): bump checkout@v6 + github-script@v8 to clear Node 20 / git-128 warnings (#1228)

## Summary
- Bump `actions/checkout@v4 → v6` and `actions/github-script@v7 → v8` in
`codex-review.yaml`
- Clears two warnings on every codex-review run: Node.js 20 deprecation
(for these two actions) and `Post Checkout repository: git exit code
128` (known post-cleanup bug in checkout v4, fixed in v6+)
- Residual Node-20 warning from `setup-node` pinned inside
`openai/codex-action@v1` will remain until OpenAI releases a new version
— out of our control

## Test plan
- [ ] Next codex-review run on a PR shows no `git exit code 128` warning
- [ ] Node-20 deprecation warning only lists `actions/setup-node@<sha>`
(the one inside `openai/codex-action@v1`), not checkout or github-script

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1228: ci(codex-review): bump checkout@v6 + github-script@v8 to clear Node 20 / git-128 warnings

## Summary
- Bump `actions/checkout@v4 → v6` and `actions/github-script@v7 → v8` in `codex-review.yaml`
- Clears two warnings on every codex-review run: Node.js 20 deprecation (for these two actions) and `Post Checkout repository: git exit code 128` (known post-cleanup bug in checkout v4, fixed in v6+)
- Residual Node-20 warning from `setup-node` pinned inside `openai/codex-action@v1` will remain until OpenAI releases a new version — out of our control

## Test plan
- [ ] Next codex-review run on a PR shows no `git exit code 128` warning
- [ ] Node-20 deprecation warning only lists `actions/setup-node@<sha>` (the one inside `openai/codex-action@v1`), not checkout or github-script

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T11:26:59Z): /lgtm

---

## 49033cd

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T11:26:27Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/49033cdd2b2bf874ef84d9aa39fb1006bce6bd50](https://github.com/SerendipityOneInc/ecap-workspace/commit/49033cdd2b2bf874ef84d9aa39fb1006bce6bd50)

### Commit Message
```
fix(ci): split pr-size-check label refresh into a separate workflow (#1230)

## Summary
- `self-approve` label events (applied by the /lgtm workflow) re-fired
`pr-size-check.yml` with a `labeled` action. The `size` job's if-filter
skipped, producing a completed/skipped check-suite under the `PR Size
Check` workflow. GitHub's merge-queue ruleset evaluator then marked the
required `size / size-check` context as **"Expected — Waiting for status
to be reported"** even though the earlier code-event run reported
SUCCESS. Auto-merge enqueue deadlocked on #1225.
- Split the label-refresh path into a new `pr-size-label-refresh.yml`.
`pr-size-check.yml` now subscribes only to code events + `merge_group`,
so the required `size / size-check` context always comes from a real
run, never a skipped sibling.
- `size-override` toggle behavior is preserved: the new workflow calls
the same reusable with `post_comment: true`, so the sticky comment still
refreshes on label apply/remove.

## Test plan
- [ ] After merge: open a no-op PR that doesn't touch `web/**` /
`ios/**` / `services/claw-interface/**` and verify `size / size-check`
reports SUCCESS and stays clean after self-approve (no "Expected" state,
auto-merge enqueues without manual click).
- [ ] Apply `size-override` to a large PR and confirm
`pr-size-label-refresh.yml` re-runs the reusable and updates the sticky
comment.
- [ ] Apply any other label (e.g. `self-approve`) to a PR and confirm it
produces a skipped check-run under `PR Size Check (label refresh)` — NOT
under `PR Size Check` — and doesn't affect merge eligibility.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1230: fix(ci): split pr-size-check label refresh into a separate workflow

## Summary
- `self-approve` label events (applied by the /lgtm workflow) re-fired `pr-size-check.yml` with a `labeled` action. The `size` job's if-filter skipped, producing a completed/skipped check-suite under the `PR Size Check` workflow. GitHub's merge-queue ruleset evaluator then marked the required `size / size-check` context as **"Expected — Waiting for status to be reported"** even though the earlier code-event run reported SUCCESS. Auto-merge enqueue deadlocked on #1225.
- Split the label-refresh path into a new `pr-size-label-refresh.yml`. `pr-size-check.yml` now subscribes only to code events + `merge_group`, so the required `size / size-check` context always comes from a real run, never a skipped sibling.
- `size-override` toggle behavior is preserved: the new workflow calls the same reusable with `post_comment: true`, so the sticky comment still refreshes on label apply/remove.

## Test plan
- [ ] After merge: open a no-op PR that doesn't touch `web/**` / `ios/**` / `services/claw-interface/**` and verify `size / size-check` reports SUCCESS and stays clean after self-approve (no "Expected" state, auto-merge enqueues without manual click).
- [ ] Apply `size-override` to a large PR and confirm `pr-size-label-refresh.yml` re-runs the reusable and updates the sticky comment.
- [ ] Apply any other label (e.g. `self-approve`) to a PR and confirm it produces a skipped check-run under `PR Size Check (label refresh)` — NOT under `PR Size Check` — and doesn't affect merge eligibility.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T11:26:18Z): /lgtm

---

## 8c4d682

**作者**: bryce-srp
**日期**: 2026-04-22T11:21:30Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/8c4d682fbb41be185a144bcd2879a2da1bd20fb5](https://github.com/SerendipityOneInc/ecap-workspace/commit/8c4d682fbb41be185a144bcd2879a2da1bd20fb5)

### Commit Message
```
refactor(billing): remove ending_at from subscribe, add terminate_subscription (#1141)

## Summary
- Stop passing `ending_at` to Billing Gateway `subscribe()` —
subscription expiry now fully managed by cron + Stripe webhook calling
`terminate_subscription()` explicitly
- Add `BillingGatewayClient.terminate_subscription()` method (calls
`POST /billing/customers/{id}/subscriptions/{ext_id}/terminate`)
- Add terminate calls to `_handle_expired_subscription` (cron),
`_check_apple_subscription` (cron), and `handle_subscription_deleted`
(Stripe webhook)
- All terminate calls are best-effort (try/except + exc_info traceback)
— failure does not block expiry flow
- Full tracing logs at every terminate entry/exit point for debugging

## Why
Previously `ending_at` was passed to Lago via Billing Gateway, creating
a dual-expiry mechanism (Lago auto-expiry + cron). Since claw-interface
already owns all time/expiry logic via cron jobs, the Lago-side
`ending_at` was redundant. Removing it simplifies the model to a single
cron-driven approach and gives us explicit control over when
subscriptions terminate.

## Test plan
- [ ] `pytest tests/unit/test_billing_client.py -v` — new terminate
tests + subscribe without ending_at
- [ ] `pytest
tests/unit/test_stripe_coverage.py::TestHandleSubscriptionDeletedPartial
-v` — terminate in webhook
- [ ] `pytest tests/unit/test_subscription_manager.py -v` — ending_at no
longer in subscribe calls
- [ ] `pyright app/ tests/` clean
- [ ] Manual: verify cron expiry calls terminate before clear_wallet in
logs

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
Co-authored-by: Copilot Autofix powered by AI <62310815+github-advanced-security[bot]@users.noreply.github.com>
```

### PR #1141: refactor(billing): remove ending_at from subscribe, add terminate_subscription

## Summary
- Stop passing `ending_at` to Billing Gateway `subscribe()` — subscription expiry now fully managed by cron + Stripe webhook calling `terminate_subscription()` explicitly
- Add `BillingGatewayClient.terminate_subscription()` method (calls `POST /billing/customers/{id}/subscriptions/{ext_id}/terminate`)
- Add terminate calls to `_handle_expired_subscription` (cron), `_check_apple_subscription` (cron), and `handle_subscription_deleted` (Stripe webhook)
- All terminate calls are best-effort (try/except + exc_info traceback) — failure does not block expiry flow
- Full tracing logs at every terminate entry/exit point for debugging

## Why
Previously `ending_at` was passed to Lago via Billing Gateway, creating a dual-expiry mechanism (Lago auto-expiry + cron). Since claw-interface already owns all time/expiry logic via cron jobs, the Lago-side `ending_at` was redundant. Removing it simplifies the model to a single cron-driven approach and gives us explicit control over when subscriptions terminate.

## Test plan
- [ ] `pytest tests/unit/test_billing_client.py -v` — new terminate tests + subscribe without ending_at
- [ ] `pytest tests/unit/test_stripe_coverage.py::TestHandleSubscriptionDeletedPartial -v` — terminate in webhook
- [ ] `pytest tests/unit/test_subscription_manager.py -v` — ending_at no longer in subscribe calls
- [ ] `pyright app/ tests/` clean
- [ ] Manual: verify cron expiry calls terminate before clear_wallet in logs

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 4950e3a

**作者**: Fangmiao-srp
**日期**: 2026-04-22T11:16:41Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/4950e3ac7cdf35d2706e76a770a10f62c973eec7](https://github.com/SerendipityOneInc/ecap-workspace/commit/4950e3ac7cdf35d2706e76a770a10f62c973eec7)

### Commit Message
```
feat: track sign_up/login events (GA4 + Google Ads + Reddit Pixel) (#1219)

## Summary
- Backend `/users/create` now returns `created: bool` based on MongoDB
upsert result (new user → true, existing → false)
- Frontend bubbles `created` from `_createAndSyncUser` →
`syncBusinessData` → `_completeLogin`, where it fires `trackSignUp` or
`trackLogin`
- `loginUser` now requires a `method` string (`google`, `email_link`,
`phone`, `email_otp`) — compile-time enforcement prevents missing
tracking
- Added Google Ads conversion label for `sign_up` event

## Test plan
- [ ] Existing unit tests updated for new `loginUser(token, phone,
method)` signature
- [ ] CI: `code-quality / lint-and-test` passes (web)
- [ ] CI: `python-code-quality / build-and-test` passes (backend)
- [ ] Manual: Google login as new user → GA4 shows `sign_up` event with
`method: google`, Google Ads conversion fires
- [ ] Manual: Google login as existing user → GA4 shows `login` event
with `method: google`, no Ads conversion

Part of #1032 tracking pipeline split.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Muyao Wang <muyao@MuyaodeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### PR #1219: feat: track sign_up/login events (GA4 + Google Ads + Reddit Pixel)

## Summary
- Backend `/users/create` now returns `created: bool` based on MongoDB upsert result (new user → true, existing → false)
- Frontend bubbles `created` from `_createAndSyncUser` → `syncBusinessData` → `_completeLogin`, where it fires `trackSignUp` or `trackLogin`
- `loginUser` now requires a `method` string (`google`, `email_link`, `phone`, `email_otp`) — compile-time enforcement prevents missing tracking
- Added Google Ads conversion label for `sign_up` event

## Test plan
- [ ] Existing unit tests updated for new `loginUser(token, phone, method)` signature
- [ ] CI: `code-quality / lint-and-test` passes (web)
- [ ] CI: `python-code-quality / build-and-test` passes (backend)
- [ ] Manual: Google login as new user → GA4 shows `sign_up` event with `method: google`, Google Ads conversion fires
- [ ] Manual: Google login as existing user → GA4 shows `login` event with `method: google`, no Ads conversion

Part of #1032 tracking pipeline split.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## d303b53

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T11:14:09Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/d303b535cf5f3cd7ef31bfdb4abd927a9723c90c](https://github.com/SerendipityOneInc/ecap-workspace/commit/d303b535cf5f3cd7ef31bfdb4abd927a9723c90c)

### Commit Message
```
fix(ci): repair claude-develop workflow expression parse error (#1225)

## Summary
- Fix broken `\!=` → `!=` in `.github/workflows/claude-develop.yaml`
`if:` expression — GitHub Actions couldn't parse it, so every push
generated a failed zero-job run and emailed the committer. All 30 recent
runs of this workflow are `push` / `failure` / 0 jobs.
- Add `github.event_name == 'issues'` guard so any future trigger
mismatch short-circuits to skip rather than failure.

Example failed run:
https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24771345811
Root cause landed in #391.

## Test plan
- [x] Grep confirmed no sibling `claude-*.yaml` / `codex-*.yaml`
workflow has the same backslash-bang pattern
- [ ] After merge, confirm pushes to `main` no longer produce
`.github/workflows/claude-develop.yaml` failure runs
- [ ] Verify intended flow still works by labeling an issue with
`claude-develop`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1225: fix(ci): repair claude-develop workflow expression parse error

## Summary
- Fix broken `\!=` → `!=` in `.github/workflows/claude-develop.yaml` `if:` expression — GitHub Actions couldn't parse it, so every push generated a failed zero-job run and emailed the committer. All 30 recent runs of this workflow are `push` / `failure` / 0 jobs.
- Add `github.event_name == 'issues'` guard so any future trigger mismatch short-circuits to skip rather than failure.

Example failed run: https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24771345811
Root cause landed in #391.

## Test plan
- [x] Grep confirmed no sibling `claude-*.yaml` / `codex-*.yaml` workflow has the same backslash-bang pattern
- [ ] After merge, confirm pushes to `main` no longer produce `.github/workflows/claude-develop.yaml` failure runs
- [ ] Verify intended flow still works by labeling an issue with `claude-develop`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T10:10:08Z): /lgtm

---

## 8bc914a

**作者**: nolan-srp
**日期**: 2026-04-22T11:03:05Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/8bc914a7b7ae63a9f72679c49d98358a2702ac7d](https://github.com/SerendipityOneInc/ecap-workspace/commit/8bc914a7b7ae63a9f72679c49d98358a2702ac7d)

### Commit Message
```
feat(openclaw): add private custom agent catalog flow (#1147)

## Summary
- add owner-scoped private custom agent catalog reads and CRUD endpoints
in OpenClaw
- support local and remote custom agent archive sources through install,
deploy, and runtime flows
- update the publish UI and web API layer for private agent cards,
including install payload validation coverage
```

### PR #1147: feat(openclaw): add private custom agent catalog flow

## Summary
- add owner-scoped private custom agent catalog reads and CRUD endpoints in OpenClaw
- support local and remote custom agent archive sources through install, deploy, and runtime flows
- update the publish UI and web API layer for private agent cards, including install payload validation coverage

---

## ecc75ea

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T10:26:15Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/ecc75ea866b583b679f4b3f0b4eea83d6147c08f](https://github.com/SerendipityOneInc/ecap-workspace/commit/ecc75ea866b583b679f4b3f0b4eea83d6147c08f)

### Commit Message
```
test(web): SkillsSearchClient 全面覆盖 (#894 Step 9 1/2) (#1220)

## Summary

Epic #894 Step 9 (#903) — \`SkillsSearchClient.tsx\` (607 LOC) 从 0% → 31
tests 覆盖核心分支,**零源码改动**。

## 覆盖

| 组 | # | 覆盖 |
|---|---|---|
| Initial render / auth | 4 | 空态/tab 渲染/无 uid skip 拉取/authLoading 态 |
| 运行时 skills fetch | 3 | cached hit/fetch 错误 fallback/unmount cancel |
| Tab 切换 | 3 | community 触发拉取/cache replace+refetch/official 过滤 source |
| 搜索过滤 | 3 | matchesSkillQuery / 大小写 trim / 按 downloads 排序 |
| Community pagination | 4 | IntersectionObserver
触发拉下一页/dedup/replace=true 失败 fallback/hasMore=false 无新拉取 |
| Skill card 渲染 | 4 | 基本信息/installed check/community
InstalledAgentsSummary/action 隐藏 |
| 详情导航 | 2 | detailAvailable=true → router.push / false 不可点 |
| Action + 管理 modal | 8 | 开 modal / install / uninstall / error → toast
+ 错误/未登录 / 无 workspace / close / 禁用态早返 |

## 技术要点

- 13 hook/API/util 依赖全部 hoisted mock
- \`FakeIntersectionObserver\` 捕获构造 instance,\`.trigger()\` 驱动无限滚动分支
- 双 mount observer 现象(hasMore=true 默认 state → 首次 load →
hasMore=false)已记在测试注释里,并验证 \`disconnect\` 被调用

## Test plan

- [x] \`pnpm test:unit --
tests/unit/app/skills/search/SkillsSearchClient.unit.spec.tsx\` 31/31
passed
- [x] lint/prettier clean
- [ ] CI green

## 关联

- Epic #894 Step 9 (#903)
- 剩余:SkillDetailClient (548 LOC) 另起 PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1220: test(web): SkillsSearchClient 全面覆盖 (#894 Step 9 1/2)

## Summary

Epic #894 Step 9 (#903) — \`SkillsSearchClient.tsx\` (607 LOC) 从 0% → 31 tests 覆盖核心分支,**零源码改动**。

## 覆盖

| 组 | # | 覆盖 |
|---|---|---|
| Initial render / auth | 4 | 空态/tab 渲染/无 uid skip 拉取/authLoading 态 |
| 运行时 skills fetch | 3 | cached hit/fetch 错误 fallback/unmount cancel |
| Tab 切换 | 3 | community 触发拉取/cache replace+refetch/official 过滤 source |
| 搜索过滤 | 3 | matchesSkillQuery / 大小写 trim / 按 downloads 排序 |
| Community pagination | 4 | IntersectionObserver 触发拉下一页/dedup/replace=true 失败 fallback/hasMore=false 无新拉取 |
| Skill card 渲染 | 4 | 基本信息/installed check/community InstalledAgentsSummary/action 隐藏 |
| 详情导航 | 2 | detailAvailable=true → router.push / false 不可点 |
| Action + 管理 modal | 8 | 开 modal / install / uninstall / error → toast + 错误/未登录 / 无 workspace / close / 禁用态早返 |

## 技术要点

- 13 hook/API/util 依赖全部 hoisted mock
- \`FakeIntersectionObserver\` 捕获构造 instance,\`.trigger()\` 驱动无限滚动分支
- 双 mount observer 现象(hasMore=true 默认 state → 首次 load → hasMore=false)已记在测试注释里,并验证 \`disconnect\` 被调用

## Test plan

- [x] \`pnpm test:unit -- tests/unit/app/skills/search/SkillsSearchClient.unit.spec.tsx\` 31/31 passed
- [x] lint/prettier clean
- [ ] CI green

## 关联

- Epic #894 Step 9 (#903)
- 剩余:SkillDetailClient (548 LOC) 另起 PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T10:26:04Z): /lgtm

---

## 4a30829

**作者**: dependabot[bot]
**日期**: 2026-04-22T10:19:52Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/4a308294d0ebd7f4867c4633fa7b1f5b318e4215](https://github.com/SerendipityOneInc/ecap-workspace/commit/4a308294d0ebd7f4867c4633fa7b1f5b318e4215)

### Commit Message
```
chore(deps): update pyjwt requirement from >=2.8.0 to >=2.12.1 in /services/claw-interface (#1200)

Updates the requirements on [pyjwt](https://github.com/jpadilla/pyjwt)
to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/jpadilla/pyjwt/releases">pyjwt's
releases</a>.</em></p>
<blockquote>
<h2>2.12.1</h2>
<h2>What's Changed</h2>
<ul>
<li>Add typing_extensions dependency for Python &lt; 3.11 by <a
href="https://github.com/jpadilla"><code>@​jpadilla</code></a> in <a
href="https://redirect.github.com/jpadilla/pyjwt/pull/1151">jpadilla/pyjwt#1151</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a
href="https://github.com/jpadilla/pyjwt/compare/2.12.0...2.12.1">https://github.com/jpadilla/pyjwt/compare/2.12.0...2.12.1</a></p>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/jpadilla/pyjwt/blob/master/CHANGELOG.rst">pyjwt's
changelog</a>.</em></p>
<blockquote>
<h2><code>v2.12.1
&lt;https://github.com/jpadilla/pyjwt/compare/2.12.0...2.12.1&gt;</code>__</h2>
<p>Fixed</p>
<pre><code>
- Add missing ``typing_extensions`` dependency for Python &lt; 3.11 in
`[#1150](https://github.com/jpadilla/pyjwt/issues/1150)
&lt;https://github.com/jpadilla/pyjwt/issues/1150&gt;`__
<h2><code>v2.12.0
&amp;lt;https://github.com/jpadilla/pyjwt/compare/2.11.0...2.12.0&amp;gt;</code>__</h2>
<p>Fixed
</code></pre></p>
<ul>
<li>Annotate PyJWKSet.keys for pyright by <a
href="https://github.com/tamird"><code>@​tamird</code></a> in
<code>[#1134](https://github.com/jpadilla/pyjwt/issues/1134)
&lt;https://github.com/jpadilla/pyjwt/pull/1134&gt;</code>__</li>
<li>Close <code>HTTPError</code> response to prevent
<code>ResourceWarning</code> on Python 3.14 by <a
href="https://github.com/veeceey"><code>@​veeceey</code></a> in
<code>[#1133](https://github.com/jpadilla/pyjwt/issues/1133)
&lt;https://github.com/jpadilla/pyjwt/pull/1133&gt;</code>__</li>
<li>Do not keep <code>algorithms</code> dict in PyJWK instances by <a
href="https://github.com/akx"><code>@​akx</code></a> in
<code>[#1143](https://github.com/jpadilla/pyjwt/issues/1143)
&lt;https://github.com/jpadilla/pyjwt/pull/1143&gt;</code>__</li>
<li>Validate the crit (Critical) Header Parameter defined in RFC 7515
§4.1.11. by <a
href="https://github.com/dmbs335"><code>@​dmbs335</code></a> in
<code>GHSA-752w-5fwx-jx9f
&lt;https://github.com/jpadilla/pyjwt/security/advisories/GHSA-752w-5fwx-jx9f&gt;</code>__</li>
<li>Use PyJWK algorithm when encoding without explicit algorithm in
<code>[#1148](https://github.com/jpadilla/pyjwt/issues/1148)
&lt;https://github.com/jpadilla/pyjwt/pull/1148&gt;</code>__</li>
</ul>
<p>Added</p>
<pre><code>
- Docs: Add ``PyJWKClient`` API reference and document the two-tier
caching system (JWK Set cache and signing key LRU cache).
<h2><code>v2.11.0
&amp;lt;https://github.com/jpadilla/pyjwt/compare/2.10.1...2.11.0&amp;gt;</code>__</h2>
<p>Fixed
</code></pre></p>
<ul>
<li>Enforce ECDSA curve validation per RFC 7518 Section 3.4.</li>
<li>Fix build system warnings by <a
href="https://github.com/kurtmckee"><code>@​kurtmckee</code></a> in
<code>[#1105](https://github.com/jpadilla/pyjwt/issues/1105)
&lt;https://github.com/jpadilla/pyjwt/pull/1105&gt;</code>__</li>
<li>Validate key against allowed types for Algorithm family in
<code>[#964](https://github.com/jpadilla/pyjwt/issues/964)
&lt;https://github.com/jpadilla/pyjwt/pull/964&gt;</code>__</li>
<li>Add iterator for JWKSet in
<code>[#1041](https://github.com/jpadilla/pyjwt/issues/1041)
&lt;https://github.com/jpadilla/pyjwt/pull/1041&gt;</code>__</li>
<li>Validate <code>iss</code> claim is a string during encoding and
decoding by <a
href="https://github.com/pachewise"><code>@​pachewise</code></a> in
<code>[#1040](https://github.com/jpadilla/pyjwt/issues/1040)
&lt;https://github.com/jpadilla/pyjwt/pull/1040&gt;</code>__</li>
<li>Improve typing/logic for <code>options</code> in decode,
decode_complete by <a
href="https://github.com/pachewise"><code>@​pachewise</code></a> in
<code>[#1045](https://github.com/jpadilla/pyjwt/issues/1045)
&lt;https://github.com/jpadilla/pyjwt/pull/1045&gt;</code>__</li>
<li>Declare float supported type for lifespan and timeout by <a
href="https://github.com/nikitagashkov"><code>@​nikitagashkov</code></a>
in <code>[#1068](https://github.com/jpadilla/pyjwt/issues/1068)
&lt;https://github.com/jpadilla/pyjwt/pull/1068&gt;</code>__</li>
<li>Fix <code>SyntaxWarning</code>\s/<code>DeprecationWarning</code>\s
caused by invalid escape sequences by <a
href="https://github.com/kurtmckee"><code>@​kurtmckee</code></a> in
<code>[#1103](https://github.com/jpadilla/pyjwt/issues/1103)
&lt;https://github.com/jpadilla/pyjwt/pull/1103&gt;</code>__</li>
<li>Development: Build a shared wheel once to speed up test suite setup
times by <a
href="https://github.com/kurtmckee"><code>@​kurtmckee</code></a> in
<code>[#1114](https://github.com/jpadilla/pyjwt/issues/1114)
&lt;https://github.com/jpadilla/pyjwt/pull/1114&gt;</code>__</li>
<li>Development: Test type annotations across all supported Python
versions,
increase the strictness of the type checking, and remove the mypy
pre-commit hook
by <a href="https://github.com/kurtmckee"><code>@​kurtmckee</code></a>
in <code>[#1112](https://github.com/jpadilla/pyjwt/issues/1112)
&lt;https://github.com/jpadilla/pyjwt/pull/1112&gt;</code>__</li>
</ul>
<p>Added</p>
<pre><code>
- Support Python 3.14, and test against PyPy 3.10 and 3.11 by @kurtmckee
in `[#1104](https://github.com/jpadilla/pyjwt/issues/1104)
&lt;https://github.com/jpadilla/pyjwt/pull/1104&gt;`__
- Development: Migrate to ``build`` to test package building in CI by
@kurtmckee in `[#1108](https://github.com/jpadilla/pyjwt/issues/1108)
&lt;https://github.com/jpadilla/pyjwt/pull/1108&gt;`__
- Development: Improve coverage config and eliminate unused test suite
code by @kurtmckee in
`[#1115](https://github.com/jpadilla/pyjwt/issues/1115)
&lt;https://github.com/jpadilla/pyjwt/pull/1115&gt;`__
&lt;/tr&gt;&lt;/table&gt; 
</code></pre>
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/a4e1a3d1218b01c5806420b8f16d9308ac4adc30"><code>a4e1a3d</code></a>
Add typing_extensions dependency for Python &lt; 3.11 (<a
href="https://redirect.github.com/jpadilla/pyjwt/issues/1151">#1151</a>)</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/bd9700cca7f9258fadcc429c1034e508025931f2"><code>bd9700c</code></a>
Use PyJWK algorithm when encoding without explicit algorithm (<a
href="https://redirect.github.com/jpadilla/pyjwt/issues/1148">#1148</a>)</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/051ea341b5573fe3edcd53042f347929b92c2b92"><code>051ea34</code></a>
Merge commit from fork</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/1451d70eca2059bc472703692f0bb0777bc0fe93"><code>1451d70</code></a>
fix: do not store reference to algorithms dict on PyJWK (<a
href="https://redirect.github.com/jpadilla/pyjwt/issues/1143">#1143</a>)</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/f3ba74c106df9ce10e272dfaad96acb4ab3ef5a5"><code>f3ba74c</code></a>
[pre-commit.ci] pre-commit autoupdate (<a
href="https://redirect.github.com/jpadilla/pyjwt/issues/1145">#1145</a>)</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/0318ffa7b156b01600376e38952bf961382e0724"><code>0318ffa</code></a>
[pre-commit.ci] pre-commit autoupdate (<a
href="https://redirect.github.com/jpadilla/pyjwt/issues/1141">#1141</a>)</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/a52753db3c1075ac01337fa8b7cc92b13a19ac09"><code>a52753d</code></a>
Bump actions/download-artifact from 7 to 8 (<a
href="https://redirect.github.com/jpadilla/pyjwt/issues/1142">#1142</a>)</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/b85050f1d444c6828bb4618ee764443b0a3f5d18"><code>b85050f</code></a>
chore(tests): enable mypy (<a
href="https://redirect.github.com/jpadilla/pyjwt/issues/1138">#1138</a>)</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/1272b264779717cc481c8341f321a7fc8b3aaba6"><code>1272b26</code></a>
[pre-commit.ci] pre-commit autoupdate (<a
href="https://redirect.github.com/jpadilla/pyjwt/issues/1135">#1135</a>)</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/99a87287c26cb97c94399084ee4186ee52207a7f"><code>99a8728</code></a>
chore: remove superfluous constants (<a
href="https://redirect.github.com/jpadilla/pyjwt/issues/1136">#1136</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/jpadilla/pyjwt/compare/2.8.0...2.12.1">compare
view</a></li>
</ul>
</details>
<br />

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR #1200: chore(deps): update pyjwt requirement from >=2.8.0 to >=2.12.1 in /services/claw-interface

Updates the requirements on [pyjwt](https://github.com/jpadilla/pyjwt) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/jpadilla/pyjwt/releases">pyjwt's releases</a>.</em></p>
<blockquote>
<h2>2.12.1</h2>
<h2>What's Changed</h2>
<ul>
<li>Add typing_extensions dependency for Python &lt; 3.11 by <a href="https://github.com/jpadilla"><code>@​jpadilla</code></a> in <a href="https://redirect.github.com/jpadilla/pyjwt/pull/1151">jpadilla/pyjwt#1151</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/jpadilla/pyjwt/compare/2.12.0...2.12.1">https://github.com/jpadilla/pyjwt/compare/2.12.0...2.12.1</a></p>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/jpadilla/pyjwt/blob/master/CHANGELOG.rst">pyjwt's changelog</a>.</em></p>
<blockquote>
<h2><code>v2.12.1 &lt;https://github.com/jpadilla/pyjwt/compare/2.12.0...2.12.1&gt;</code>__</h2>
<p>Fixed</p>
<pre><code>
- Add missing ``typing_extensions`` dependency for Python &lt; 3.11 in `[#1150](https://github.com/jpadilla/pyjwt/issues/1150) &lt;https://github.com/jpadilla/pyjwt/issues/1150&gt;`__
<h2><code>v2.12.0 &amp;lt;https://github.com/jpadilla/pyjwt/compare/2.11.0...2.12.0&amp;gt;</code>__</h2>
<p>Fixed
</code></pre></p>
<ul>
<li>Annotate PyJWKSet.keys for pyright by <a href="https://github.com/tamird"><code>@​tamird</code></a> in <code>[#1134](https://github.com/jpadilla/pyjwt/issues/1134) &lt;https://github.com/jpadilla/pyjwt/pull/1134&gt;</code>__</li>
<li>Close <code>HTTPError</code> response to prevent <code>ResourceWarning</code> on Python 3.14 by <a href="https://github.com/veeceey"><code>@​veeceey</code></a> in <code>[#1133](https://github.com/jpadilla/pyjwt/issues/1133) &lt;https://github.com/jpadilla/pyjwt/pull/1133&gt;</code>__</li>
<li>Do not keep <code>algorithms</code> dict in PyJWK instances by <a href="https://github.com/akx"><code>@​akx</code></a> in <code>[#1143](https://github.com/jpadilla/pyjwt/issues/1143) &lt;https://github.com/jpadilla/pyjwt/pull/1143&gt;</code>__</li>
<li>Validate the crit (Critical) Header Parameter defined in RFC 7515 §4.1.11. by <a href="https://github.com/dmbs335"><code>@​dmbs335</code></a> in <code>GHSA-752w-5fwx-jx9f &lt;https://github.com/jpadilla/pyjwt/security/advisories/GHSA-752w-5fwx-jx9f&gt;</code>__</li>
<li>Use PyJWK algorithm when encoding without explicit algorithm in <code>[#1148](https://github.com/jpadilla/pyjwt/issues/1148) &lt;https://github.com/jpadilla/pyjwt/pull/1148&gt;</code>__</li>
</ul>
<p>Added</p>
<pre><code>
- Docs: Add ``PyJWKClient`` API reference and document the two-tier caching system (JWK Set cache and signing key LRU cache).
<h2><code>v2.11.0 &amp;lt;https://github.com/jpadilla/pyjwt/compare/2.10.1...2.11.0&amp;gt;</code>__</h2>
<p>Fixed
</code></pre></p>
<ul>
<li>Enforce ECDSA curve validation per RFC 7518 Section 3.4.</li>
<li>Fix build system warnings by <a href="https://github.com/kurtmckee"><code>@​kurtmckee</code></a> in <code>[#1105](https://github.com/jpadilla/pyjwt/issues/1105) &lt;https://github.com/jpadilla/pyjwt/pull/1105&gt;</code>__</li>
<li>Validate key against allowed types for Algorithm family in <code>[#964](https://github.com/jpadilla/pyjwt/issues/964) &lt;https://github.com/jpadilla/pyjwt/pull/964&gt;</code>__</li>
<li>Add iterator for JWKSet in <code>[#1041](https://github.com/jpadilla/pyjwt/issues/1041) &lt;https://github.com/jpadilla/pyjwt/pull/1041&gt;</code>__</li>
<li>Validate <code>iss</code> claim is a string during encoding and decoding by <a href="https://github.com/pachewise"><code>@​pachewise</code></a> in <code>[#1040](https://github.com/jpadilla/pyjwt/issues/1040) &lt;https://github.com/jpadilla/pyjwt/pull/1040&gt;</code>__</li>
<li>Improve typing/logic for <code>options</code> in decode, decode_complete by <a href="https://github.com/pachewise"><code>@​pachewise</code></a> in <code>[#1045](https://github.com/jpadilla/pyjwt/issues/1045) &lt;https://github.com/jpadilla/pyjwt/pull/1045&gt;</code>__</li>
<li>Declare float supported type for lifespan and timeout by <a href="https://github.com/nikitagashkov"><code>@​nikitagashkov</code></a> in <code>[#1068](https://github.com/jpadilla/pyjwt/issues/1068) &lt;https://github.com/jpadilla/pyjwt/pull/1068&gt;</code>__</li>
<li>Fix <code>SyntaxWarning</code>\s/<code>DeprecationWarning</code>\s caused by invalid escape sequences by <a href="https://github.com/kurtmckee"><code>@​kurtmckee</code></a> in <code>[#1103](https://github.com/jpadilla/pyjwt/issues/1103) &lt;https://github.com/jpadilla/pyjwt/pull/1103&gt;</code>__</li>
<li>Development: Build a shared wheel once to speed up test suite setup times by <a href="https://github.com/kurtmckee"><code>@​kurtmckee</code></a> in <code>[#1114](https://github.com/jpadilla/pyjwt/issues/1114) &lt;https://github.com/jpadilla/pyjwt/pull/1114&gt;</code>__</li>
<li>Development: Test type annotations across all supported Python versions,
increase the strictness of the type checking, and remove the mypy pre-commit hook
by <a href="https://github.com/kurtmckee"><code>@​kurtmckee</code></a> in <code>[#1112](https://github.com/jpadilla/pyjwt/issues/1112) &lt;https://github.com/jpadilla/pyjwt/pull/1112&gt;</code>__</li>
</ul>
<p>Added</p>
<pre><code>
- Support Python 3.14, and test against PyPy 3.10 and 3.11 by @kurtmckee in `[#1104](https://github.com/jpadilla/pyjwt/issues/1104) &lt;https://github.com/jpadilla/pyjwt/pull/1104&gt;`__
- Development: Migrate to ``build`` to test package building in CI by @kurtmckee in `[#1108](https://github.com/jpadilla/pyjwt/issues/1108) &lt;https://github.com/jpadilla/pyjwt/pull/1108&gt;`__
- Development: Improve coverage config and eliminate unused test suite code by @kurtmckee in `[#1115](https://github.com/jpadilla/pyjwt/issues/1115) &lt;https://github.com/jpadilla/pyjwt/pull/1115&gt;`__
&lt;/tr&gt;&lt;/table&gt; 
</code></pre>
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/jpadilla/pyjwt/commit/a4e1a3d1218b01c5806420b8f16d9308ac4adc30"><code>a4e1a3d</code></a> Add typing_extensions dependency for Python &lt; 3.11 (<a href="https://redirect.github.com/jpadilla/pyjwt/issues/1151">#1151</a>)</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/bd9700cca7f9258fadcc429c1034e508025931f2"><code>bd9700c</code></a> Use PyJWK algorithm when encoding without explicit algorithm (<a href="https://redirect.github.com/jpadilla/pyjwt/issues/1148">#1148</a>)</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/051ea341b5573fe3edcd53042f347929b92c2b92"><code>051ea34</code></a> Merge commit from fork</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/1451d70eca2059bc472703692f0bb0777bc0fe93"><code>1451d70</code></a> fix: do not store reference to algorithms dict on PyJWK (<a href="https://redirect.github.com/jpadilla/pyjwt/issues/1143">#1143</a>)</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/f3ba74c106df9ce10e272dfaad96acb4ab3ef5a5"><code>f3ba74c</code></a> [pre-commit.ci] pre-commit autoupdate (<a href="https://redirect.github.com/jpadilla/pyjwt/issues/1145">#1145</a>)</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/0318ffa7b156b01600376e38952bf961382e0724"><code>0318ffa</code></a> [pre-commit.ci] pre-commit autoupdate (<a href="https://redirect.github.com/jpadilla/pyjwt/issues/1141">#1141</a>)</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/a52753db3c1075ac01337fa8b7cc92b13a19ac09"><code>a52753d</code></a> Bump actions/download-artifact from 7 to 8 (<a href="https://redirect.github.com/jpadilla/pyjwt/issues/1142">#1142</a>)</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/b85050f1d444c6828bb4618ee764443b0a3f5d18"><code>b85050f</code></a> chore(tests): enable mypy (<a href="https://redirect.github.com/jpadilla/pyjwt/issues/1138">#1138</a>)</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/1272b264779717cc481c8341f321a7fc8b3aaba6"><code>1272b26</code></a> [pre-commit.ci] pre-commit autoupdate (<a href="https://redirect.github.com/jpadilla/pyjwt/issues/1135">#1135</a>)</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/99a87287c26cb97c94399084ee4186ee52207a7f"><code>99a8728</code></a> chore: remove superfluous constants (<a href="https://redirect.github.com/jpadilla/pyjwt/issues/1136">#1136</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/jpadilla/pyjwt/compare/2.8.0...2.12.1">compare view</a></li>
</ul>
</details>
<br />


### Human Comments
- **chris-srp** (2026-04-22T10:18:23Z): @dependabot rebase

---

## cd87bea

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T10:13:21Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/cd87beaddc74cda105efb294ad679eec26c36497](https://github.com/SerendipityOneInc/ecap-workspace/commit/cd87beaddc74cda105efb294ad679eec26c36497)

### Commit Message
```
ci(claude-review): emit success status for dependabot PRs to unblock auto-merge (#1226)

## Summary
Follow-up to #1218 — the `auto-review` job in
`.github/workflows/claude-review.yaml` skips `dependabot[bot]` by
design, but the org ruleset still requires the `auto-review /
auto-review` status check. A SKIPPED check doesn't satisfy that rule, so
**auto-merge hangs indefinitely on dependabot PRs** (symptom: #1200 had
auto-merge enabled + approved but stayed in `mergeStateStatus:
BLOCKED`).

This PR adds a tiny mirror of the existing `auto-review-merge-group`
workaround: a job that fires on `pull_request` + dependabot actor and
POSTs a success commit status with the same context. Uses
`secrets.GITHUB_TOKEN` so the status carries `integration_id: 15368`
(GitHub Actions app) — matches the ruleset's integration filter.

## Why this only bit now
Admin merge button **does** bypass the ruleset (via `bypass_actors:
[{actor_id: 5, RepositoryRole, always}]`), so manually clicking Merge on
#1188/#1193/etc worked. But auto-merge doesn't traverse that path — it
waits for all required checks to legitimately pass. Without this job,
every dependabot PR needs manual intervention to land.

## Test plan
- [x] YAML validates (`python3 -c 'import yaml; yaml.safe_load(...)'`).
- [ ] After merge: dependabot PRs (#1200, #1207, #1208, #1209, #1213,
#1214) should show `auto-review / auto-review` as success once they
rebase onto the new main (or re-run the workflow). Auto-merge will then
proceed.
- [ ] Future dependabot PRs will auto-merge cleanly once approved + CI
green.

## Notes
- Existing broken PRs may need `@dependabot rebase` comments (or a
manual synchronize) to pick up the workflow change in their
`pull_request` event context.
- The real reviewer gate still runs at PR stage for non-dependabot
actors — no change in review coverage.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1226: ci(claude-review): emit success status for dependabot PRs to unblock auto-merge

## Summary
Follow-up to #1218 — the `auto-review` job in `.github/workflows/claude-review.yaml` skips `dependabot[bot]` by design, but the org ruleset still requires the `auto-review / auto-review` status check. A SKIPPED check doesn't satisfy that rule, so **auto-merge hangs indefinitely on dependabot PRs** (symptom: #1200 had auto-merge enabled + approved but stayed in `mergeStateStatus: BLOCKED`).

This PR adds a tiny mirror of the existing `auto-review-merge-group` workaround: a job that fires on `pull_request` + dependabot actor and POSTs a success commit status with the same context. Uses `secrets.GITHUB_TOKEN` so the status carries `integration_id: 15368` (GitHub Actions app) — matches the ruleset's integration filter.

## Why this only bit now
Admin merge button **does** bypass the ruleset (via `bypass_actors: [{actor_id: 5, RepositoryRole, always}]`), so manually clicking Merge on #1188/#1193/etc worked. But auto-merge doesn't traverse that path — it waits for all required checks to legitimately pass. Without this job, every dependabot PR needs manual intervention to land.

## Test plan
- [x] YAML validates (`python3 -c 'import yaml; yaml.safe_load(...)'`).
- [ ] After merge: dependabot PRs (#1200, #1207, #1208, #1209, #1213, #1214) should show `auto-review / auto-review` as success once they rebase onto the new main (or re-run the workflow). Auto-merge will then proceed.
- [ ] Future dependabot PRs will auto-merge cleanly once approved + CI green.

## Notes
- Existing broken PRs may need `@dependabot rebase` comments (or a manual synchronize) to pick up the workflow change in their `pull_request` event context.
- The real reviewer gate still runs at PR stage for non-dependabot actors — no change in review coverage.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T10:13:10Z): /lgtm

---

## 0c9a051

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T10:12:09Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/0c9a0514dc0fda8b0b5064883589dfe72e9bdd9d](https://github.com/SerendipityOneInc/ecap-workspace/commit/0c9a0514dc0fda8b0b5064883589dfe72e9bdd9d)

### Commit Message
```
chore(web): delete 27 unused files + promote knip files gate (B5) (#1126)

## Summary
- Deletes **27 orphaned files** (4014 deletions, 4 insertions).
- Adds `tests/e2e/**/*.setup.ts` to knip `entry` (Playwright `testMatch`
regex FP).
- Promotes knip's `files` category to the hard gate — any new unused
file now fails CI.

> ⚠️ **PR exceeds the 2000-line size gate** (4014 deletions). Please
apply the `size-override` label; the total is 100% mechanical file
removal with zero added logic, and splitting would create cross-PR
ordering with no review benefit. This matches prior per-category cleanup
precedent (`feedback_pr_size_rename_doubles`).

## What was deleted

| Directory / file | Files | Notes |
|---|---|---|
| `src/components/ExampleShowcase/*` | 8 | Entire orphaned landing-page
preview system |
|
`src/app/[locale]/claw-settings/components/{Bot,General,Identity,Skills}*`
| 4 | Legacy settings sections removed upstream |
| `src/app/[locale]/chat/components/{ChatWelcome,ToolProgressFloat}.tsx`
| 2 | Replaced components |
| `src/app/[locale]/canvas/{components,hooks}/index.ts` | 2 | Empty
barrel files |
| `src/components/AgentChatClient/{hooks/index.ts,index.tsx}` | 2 |
Barrel + stale entry |
|
`src/components/{AgentTag,BotStatusWidget,LanguageSelector,PageHeader,RatioSelector}.tsx`
| 5 | Orphaned singletons |
| `src/components/onboarding/SpriteIntro.tsx` | 1 | Replaced component |
| `src/lib/sentry/index.ts` | 1 | Empty barrel |
| `src/utils/{getResultLink.js,testEnvironment.js}` | 2 | Stale `.js`
utils |

All 27 were verified zero-importer via `grep -rn` (runtime + test).

## Why `tests/e2e/auth/auth.setup.ts` was NOT deleted

`playwright.config.ts:38`:
```ts
{ name: 'setup', testDir: './tests/e2e/auth', testMatch: /auth\.setup\.ts/ }
```

Playwright loads this file via a **regex** testMatch — knip's static
analysis can't follow regex string refs, so it reports the file as
unused. Real usage is verified by Playwright runtime. Added it to knip
`entry` so the gate recognizes it natively.

## Gate change

`web/scripts/ci-lint/02-dead-code.sh` `--include` list:
- Before:
`dependencies,devDependencies,unlisted,binaries,optionalPeerDependencies,unresolved,duplicates`
- After: `...,files` ← new

Any future `src/` file that no longer has an importer will fail the
`web-quality` CI step. The B-track roadmap promotes `exports` / `types`
/ `enumMembers` in later PRs.

## Verification
- `pnpm exec knip --include files` — exit 0, 0 unused files
- `npx tsc --noEmit` — clean
- `pnpm test:unit` — **3476 tests pass**
- `pnpm lint` — clean

## Test plan
- [x] Type check, unit tests, ESLint all pass
- [x] knip files gate is 0 violations
- [ ] CI confirms above (web-quality + asset-size-guard + jscpd)
- [ ] Reviewer applies `size-override` label after reading deletion
manifest
- [ ] Reviewer validates the `auth.setup.ts` FP reasoning + entry
addition
- [ ] (Post-merge) bundle shrinks: `ExampleShowcase/*` and orphan
components should reduce `.next` output

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1126: chore(web): delete 27 unused files + promote knip files gate (B5)

## Summary
- Deletes **27 orphaned files** (4014 deletions, 4 insertions).
- Adds `tests/e2e/**/*.setup.ts` to knip `entry` (Playwright `testMatch` regex FP).
- Promotes knip's `files` category to the hard gate — any new unused file now fails CI.

> ⚠️ **PR exceeds the 2000-line size gate** (4014 deletions). Please apply the `size-override` label; the total is 100% mechanical file removal with zero added logic, and splitting would create cross-PR ordering with no review benefit. This matches prior per-category cleanup precedent (`feedback_pr_size_rename_doubles`).

## What was deleted

| Directory / file | Files | Notes |
|---|---|---|
| `src/components/ExampleShowcase/*` | 8 | Entire orphaned landing-page preview system |
| `src/app/[locale]/claw-settings/components/{Bot,General,Identity,Skills}*` | 4 | Legacy settings sections removed upstream |
| `src/app/[locale]/chat/components/{ChatWelcome,ToolProgressFloat}.tsx` | 2 | Replaced components |
| `src/app/[locale]/canvas/{components,hooks}/index.ts` | 2 | Empty barrel files |
| `src/components/AgentChatClient/{hooks/index.ts,index.tsx}` | 2 | Barrel + stale entry |
| `src/components/{AgentTag,BotStatusWidget,LanguageSelector,PageHeader,RatioSelector}.tsx` | 5 | Orphaned singletons |
| `src/components/onboarding/SpriteIntro.tsx` | 1 | Replaced component |
| `src/lib/sentry/index.ts` | 1 | Empty barrel |
| `src/utils/{getResultLink.js,testEnvironment.js}` | 2 | Stale `.js` utils |

All 27 were verified zero-importer via `grep -rn` (runtime + test).

## Why `tests/e2e/auth/auth.setup.ts` was NOT deleted

`playwright.config.ts:38`:
```ts
{ name: 'setup', testDir: './tests/e2e/auth', testMatch: /auth\.setup\.ts/ }
```

Playwright loads this file via a **regex** testMatch — knip's static analysis can't follow regex string refs, so it reports the file as unused. Real usage is verified by Playwright runtime. Added it to knip `entry` so the gate recognizes it natively.

## Gate change

`web/scripts/ci-lint/02-dead-code.sh` `--include` list:
- Before: `dependencies,devDependencies,unlisted,binaries,optionalPeerDependencies,unresolved,duplicates`
- After: `...,files` ← new

Any future `src/` file that no longer has an importer will fail the `web-quality` CI step. The B-track roadmap promotes `exports` / `types` / `enumMembers` in later PRs.

## Verification
- `pnpm exec knip --include files` — exit 0, 0 unused files
- `npx tsc --noEmit` — clean
- `pnpm test:unit` — **3476 tests pass**
- `pnpm lint` — clean

## Test plan
- [x] Type check, unit tests, ESLint all pass
- [x] knip files gate is 0 violations
- [ ] CI confirms above (web-quality + asset-size-guard + jscpd)
- [ ] Reviewer applies `size-override` label after reading deletion manifest
- [ ] Reviewer validates the `auth.setup.ts` FP reasoning + entry addition
- [ ] (Post-merge) bundle shrinks: `ExampleShowcase/*` and orphan components should reduce `.next` output

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T07:30:27Z): /lgtm

---

## d74450d

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T10:08:46Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/d74450dbc55c944603eafe180b227f0c77822cf0](https://github.com/SerendipityOneInc/ecap-workspace/commit/d74450dbc55c944603eafe180b227f0c77822cf0)

### Commit Message
```
refactor(web): lift ConnectionStatus type to lib/chat — fix W2 (A1-PR7) (#1176)

## Summary
- Fixes one W2 violation: `src/hooks/useStableConnectionStatus.ts` was
reaching into `@/app/[locale]/chat/hooks` for the `ConnectionStatus`
type (W2 forbids `hooks → app`).
- `ConnectionStatus` is a pure string-union type (zero runtime) —
trivially hoistable to `src/lib/chat/websocket-types.ts` as a Layer-2
primitive.
- Baseline shrinks by 1 (currently 15 → 14; after A1-PR6 also merges: 13
→ 12).

## The move

\`\`\`ts
// src/lib/chat/websocket-types.ts  (new)
export type ConnectionStatus = 'disconnected' | 'connecting' |
'connected' | 'reconnecting' | 'error'
\`\`\`

`src/app/[locale]/chat/hooks/useOpenClawWebSocket.ts` now imports the
type from lib and **re-exports** it, so intra-feature callers that use
`import type { ConnectionStatus } from './useOpenClawWebSocket'`
(`useOpenClawChat`, `useProfileGreeting`, `useSubagentChat`,
`GenClawInput`, `SubagentChatPanel`) don't need to change.

Only the W2 violator (`useStableConnectionStatus.ts`) rewrites its
import to `@/lib/chat/websocket-types`.

## What this PR intentionally does NOT touch

- **W3 violations from `OpenClawContext`**: It too imports from
`@/app/[locale]/chat/hooks` (for `useOpenClawInit`,
`useOpenClawWebSocket` — functions, not just types). Those are W3
violations and need a different approach (likely extracting the hook
bodies or inverting control). Separate PR.
- **Other W2 violations** (`useBrandVocabulary` → BrandThemeProvider,
`useRequireChat` → OnboardingProvider): both need hook extraction from
Provider files — more involved, separate PR.

## Changes

| File | Change |
|---|---|
| `src/lib/chat/websocket-types.ts` | **new** — single export |
| `src/app/[locale]/chat/hooks/useOpenClawWebSocket.ts` | drop local
type def; import + re-export from lib |
| `src/hooks/useStableConnectionStatus.ts` | rewrite type import |
| `.dependency-cruiser-known-violations.json` | remove the W2
useStableConnectionStatus entry |

4 files, +10 / −11.

## Local verification
- \`pnpm lint:imports\` — exit 0, 14 known violations ignored
- \`npx tsc --noEmit\` — clean
- Intra-feature type imports verified: `useOpenClawChat` /
`useProfileGreeting` / `useSubagentChat` / `GenClawInput` /
`SubagentChatPanel` still use `./useOpenClawWebSocket` and tsc doesn't
break

## Interaction with open PRs

- **#1145 (A1-PR6)** is in merge queue; this PR touches
`.dependency-cruiser-known-violations.json` differently (different entry
removed), git 3-way merge auto-resolves. No file overlap otherwise.

## Test plan
- [x] `lint:imports` reports one fewer known violation after strip
- [x] tsc clean
- [ ] CI confirms web-quality
- [ ] Reviewer validates the re-export pattern in
`useOpenClawWebSocket.ts` doesn't create any stale alias path

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1176: refactor(web): lift ConnectionStatus type to lib/chat — fix W2 (A1-PR7)

## Summary
- Fixes one W2 violation: `src/hooks/useStableConnectionStatus.ts` was reaching into `@/app/[locale]/chat/hooks` for the `ConnectionStatus` type (W2 forbids `hooks → app`).
- `ConnectionStatus` is a pure string-union type (zero runtime) — trivially hoistable to `src/lib/chat/websocket-types.ts` as a Layer-2 primitive.
- Baseline shrinks by 1 (currently 15 → 14; after A1-PR6 also merges: 13 → 12).

## The move

\`\`\`ts
// src/lib/chat/websocket-types.ts  (new)
export type ConnectionStatus = 'disconnected' | 'connecting' | 'connected' | 'reconnecting' | 'error'
\`\`\`

`src/app/[locale]/chat/hooks/useOpenClawWebSocket.ts` now imports the type from lib and **re-exports** it, so intra-feature callers that use `import type { ConnectionStatus } from './useOpenClawWebSocket'` (`useOpenClawChat`, `useProfileGreeting`, `useSubagentChat`, `GenClawInput`, `SubagentChatPanel`) don't need to change.

Only the W2 violator (`useStableConnectionStatus.ts`) rewrites its import to `@/lib/chat/websocket-types`.

## What this PR intentionally does NOT touch

- **W3 violations from `OpenClawContext`**: It too imports from `@/app/[locale]/chat/hooks` (for `useOpenClawInit`, `useOpenClawWebSocket` — functions, not just types). Those are W3 violations and need a different approach (likely extracting the hook bodies or inverting control). Separate PR.
- **Other W2 violations** (`useBrandVocabulary` → BrandThemeProvider, `useRequireChat` → OnboardingProvider): both need hook extraction from Provider files — more involved, separate PR.

## Changes

| File | Change |
|---|---|
| `src/lib/chat/websocket-types.ts` | **new** — single export |
| `src/app/[locale]/chat/hooks/useOpenClawWebSocket.ts` | drop local type def; import + re-export from lib |
| `src/hooks/useStableConnectionStatus.ts` | rewrite type import |
| `.dependency-cruiser-known-violations.json` | remove the W2 useStableConnectionStatus entry |

4 files, +10 / −11.

## Local verification
- \`pnpm lint:imports\` — exit 0, 14 known violations ignored
- \`npx tsc --noEmit\` — clean
- Intra-feature type imports verified: `useOpenClawChat` / `useProfileGreeting` / `useSubagentChat` / `GenClawInput` / `SubagentChatPanel` still use `./useOpenClawWebSocket` and tsc doesn't break

## Interaction with open PRs

- **#1145 (A1-PR6)** is in merge queue; this PR touches `.dependency-cruiser-known-violations.json` differently (different entry removed), git 3-way merge auto-resolves. No file overlap otherwise.

## Test plan
- [x] `lint:imports` reports one fewer known violation after strip
- [x] tsc clean
- [ ] CI confirms web-quality
- [ ] Reviewer validates the re-export pattern in `useOpenClawWebSocket.ts` doesn't create any stale alias path

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T10:08:34Z): /lgtm

---

## e855338

**作者**: dependabot[bot]
**日期**: 2026-04-22T10:03:11Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/e85533800c60af7fb9573b1bbe57260fdd098735](https://github.com/SerendipityOneInc/ecap-workspace/commit/e85533800c60af7fb9573b1bbe57260fdd098735)

### Commit Message
```
chore(deps): update websockets requirement from >=12.0 to >=16.0 in /services/claw-interface (#1214)

Updates the requirements on
[websockets](https://github.com/python-websockets/websockets) to permit
the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/python-websockets/websockets/releases">websockets's
releases</a>.</em></p>
<blockquote>
<h2>16.0</h2>
<p>See <a
href="https://websockets.readthedocs.io/en/stable/project/changelog.html">https://websockets.readthedocs.io/en/stable/project/changelog.html</a>
for details.</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/python-websockets/websockets/commit/d4303a5d3e373fc8c34177c3dec1a9c75c8865fa"><code>d4303a5</code></a>
Release version 16.0.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/851bcd756bf114e41438f04d928aa85838724fe1"><code>851bcd7</code></a>
Bump pypa/cibuildwheel from 3.3.0 to 3.3.1</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/740c8d373e10ced940fb33c3e0457991841c10c4"><code>740c8d3</code></a>
Temporarily remove the trio implementation.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/92ea0553587ba07a4668c30dfd9e6210d9f26bc9"><code>92ea055</code></a>
Add missing changelog entry.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/ba74244154df5a74f044d0f8cd971acac636bb74"><code>ba74244</code></a>
Document bug fix.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/9410483c016463a6cd08b2a5321337b85e094f10"><code>9410483</code></a>
Pin sphinx to avoid error in sphinxcontrib-trio.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/8e4d408e17b0bfa1a91aa62e054b8786a8132231"><code>8e4d408</code></a>
Document asyncio's TLS read buffer.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/cb3500b0b030715dc3caa1e3ce95affe4a79b8bd"><code>cb3500b</code></a>
Stop referring to the asyncio implementation as new.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/6563a9c884d92df4c889bb174dc84a56a7377686"><code>6563a9c</code></a>
The threading implementation supports max_queue.</li>
<li><a
href="https://github.com/python-websockets/websockets/commit/9f17e92dbee2b9a14e02b2792cfbb127efbd4098"><code>9f17e92</code></a>
Clarify that protocol_mutex protects pending_pings.</li>
<li>Additional commits viewable in <a
href="https://github.com/python-websockets/websockets/compare/12.0...16.0">compare
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

### PR #1214: chore(deps): update websockets requirement from >=12.0 to >=16.0 in /services/claw-interface

Updates the requirements on [websockets](https://github.com/python-websockets/websockets) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/python-websockets/websockets/releases">websockets's releases</a>.</em></p>
<blockquote>
<h2>16.0</h2>
<p>See <a href="https://websockets.readthedocs.io/en/stable/project/changelog.html">https://websockets.readthedocs.io/en/stable/project/changelog.html</a> for details.</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/python-websockets/websockets/commit/d4303a5d3e373fc8c34177c3dec1a9c75c8865fa"><code>d4303a5</code></a> Release version 16.0.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/851bcd756bf114e41438f04d928aa85838724fe1"><code>851bcd7</code></a> Bump pypa/cibuildwheel from 3.3.0 to 3.3.1</li>
<li><a href="https://github.com/python-websockets/websockets/commit/740c8d373e10ced940fb33c3e0457991841c10c4"><code>740c8d3</code></a> Temporarily remove the trio implementation.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/92ea0553587ba07a4668c30dfd9e6210d9f26bc9"><code>92ea055</code></a> Add missing changelog entry.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/ba74244154df5a74f044d0f8cd971acac636bb74"><code>ba74244</code></a> Document bug fix.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/9410483c016463a6cd08b2a5321337b85e094f10"><code>9410483</code></a> Pin sphinx to avoid error in sphinxcontrib-trio.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/8e4d408e17b0bfa1a91aa62e054b8786a8132231"><code>8e4d408</code></a> Document asyncio's TLS read buffer.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/cb3500b0b030715dc3caa1e3ce95affe4a79b8bd"><code>cb3500b</code></a> Stop referring to the asyncio implementation as new.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/6563a9c884d92df4c889bb174dc84a56a7377686"><code>6563a9c</code></a> The threading implementation supports max_queue.</li>
<li><a href="https://github.com/python-websockets/websockets/commit/9f17e92dbee2b9a14e02b2792cfbb127efbd4098"><code>9f17e92</code></a> Clarify that protocol_mutex protects pending_pings.</li>
<li>Additional commits viewable in <a href="https://github.com/python-websockets/websockets/compare/12.0...16.0">compare view</a></li>
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

---

## ec468b4

**作者**: dependabot[bot]
**日期**: 2026-04-22T10:02:59Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/ec468b4c7c227d2d3205af82ce22569a1079b458](https://github.com/SerendipityOneInc/ecap-workspace/commit/ec468b4c7c227d2d3205af82ce22569a1079b458)

### Commit Message
```
chore(deps-dev): update pytest-xdist requirement from >=3.6 to >=3.8.0 in /services/claw-interface (#1213)

Updates the requirements on
[pytest-xdist](https://github.com/pytest-dev/pytest-xdist) to permit the
latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/pytest-dev/pytest-xdist/blob/master/CHANGELOG.rst">pytest-xdist's
changelog</a>.</em></p>
<blockquote>
<h1>pytest-xdist 3.8.0 (2025-06-30)</h1>
<h2>Features</h2>
<ul>
<li>

<p><code>[#1083](https://github.com/pytest-dev/pytest-xdist/issues/1083)
&lt;https://github.com/pytest-dev/pytest-xdist/issues/1083&gt;</code>_:
Add <code>--no-loadscope-reorder</code> and
<code>--loadscope-reorder</code> option to control whether to
automatically reorder tests in loadscope for tests where relative
ordering matters. This only applies when using
<code>loadscope</code>.</p>
<p>For example, [test_file_1, test_file_2, ..., test_file_n] are given
as input test files, if <code>--no-loadscope-reorder</code> is used, for
either worker, the <code>test_file_a</code> will be executed before
<code>test_file_b</code> only if <code>a &lt; b</code>.</p>
<p>The default behavior is to reorder the tests to maximize the number
of tests that can be executed in parallel.</p>
</li>
</ul>
<h1>pytest-xdist 3.7.0 (2025-05-26)</h1>
<h2>Features</h2>
<ul>
<li>

<p><code>[#1142](https://github.com/pytest-dev/pytest-xdist/issues/1142)
&lt;https://github.com/pytest-dev/pytest-xdist/issues/1142&gt;</code>_:
Added support for Python 3.13.</p>
</li>
<li>

<p><code>[#1144](https://github.com/pytest-dev/pytest-xdist/issues/1144)
&lt;https://github.com/pytest-dev/pytest-xdist/issues/1144&gt;</code>_:
The internal <code>steal</code> command is now atomic - it unschedules
either all requested tests or none.</p>
<p>This is a prerequisite for group/scope support in the
<code>worksteal</code> scheduler, so test groups won't be broken up
incorrectly.</p>
</li>
<li>

<p><code>[#1170](https://github.com/pytest-dev/pytest-xdist/issues/1170)
&lt;https://github.com/pytest-dev/pytest-xdist/issues/1170&gt;</code>_:
Add the <code>--px</code> arg to create proxy gateways.</p>
<p>Proxy gateways are passed to additional gateways using the
<code>via</code> keyword.
They can serve as a way to run multiple workers on remote machines.</p>
</li>
<li>

<p><code>[#1200](https://github.com/pytest-dev/pytest-xdist/issues/1200)
&lt;https://github.com/pytest-dev/pytest-xdist/issues/1200&gt;</code>_:
Now multiple <code>xdist_group</code> markers are considered when
assigning tests to groups (order does not matter).</p>
<p>Previously, only the last marker would assign a test to a group, but
now if a test has multiple <code>xdist_group</code> marks applied (for
example via parametrization or via fixtures), they are merged to make a
new group.</p>
</li>
</ul>
<h2>Removals</h2>
<ul>

<li><code>[#1162](https://github.com/pytest-dev/pytest-xdist/issues/1162)
&lt;https://github.com/pytest-dev/pytest-xdist/issues/1162&gt;</code>_:
Dropped support for EOL Python 3.8.</li>
</ul>
<h2>Trivial Changes</h2>
<ul>
<li>

<p><code>[#1092](https://github.com/pytest-dev/pytest-xdist/issues/1092)
&lt;https://github.com/pytest-dev/pytest-xdist/issues/1092&gt;</code>_:
Update an error message to better indicate where users should go for
more information.</p>
</li>
<li>

<p><code>[#1190](https://github.com/pytest-dev/pytest-xdist/issues/1190)
&lt;https://github.com/pytest-dev/pytest-xdist/issues/1190&gt;</code>_:
Switched to using a SPDX license identifier introduced in PEP 639.</p>
</li>
</ul>
<h1>pytest-xdist 3.6.1 (2024-04-28)</h1>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/pytest-dev/pytest-xdist/commit/1e3e4dc16523c8a8f6c67d95a950166420718c99"><code>1e3e4dc</code></a>
Release 3.8.0</li>
<li><a
href="https://github.com/pytest-dev/pytest-xdist/commit/600aad575a4e4382855145b0c464d51b8f0b7242"><code>600aad5</code></a>
Ensure all xdist group names are strings (<a
href="https://redirect.github.com/pytest-dev/pytest-xdist/issues/1216">#1216</a>)</li>
<li><a
href="https://github.com/pytest-dev/pytest-xdist/commit/9d7ba5b5fbbbe26793fbfb7cb1903eb69425cf09"><code>9d7ba5b</code></a>
Add <code>--no-loadscope-reorder</code> and
<code>--loadscope-reorder</code> options (<a
href="https://redirect.github.com/pytest-dev/pytest-xdist/issues/1217">#1217</a>)</li>
<li><a
href="https://github.com/pytest-dev/pytest-xdist/commit/532f07fb181bb1546eda79bbe6b46bdb56c699e1"><code>532f07f</code></a>
Merge pull request <a
href="https://redirect.github.com/pytest-dev/pytest-xdist/issues/1210">#1210</a>
from pytest-dev/pre-commit-ci-update-config</li>
<li><a
href="https://github.com/pytest-dev/pytest-xdist/commit/0883ad085e0cf039c8ae13eb2789c1076544d225"><code>0883ad0</code></a>
Fix Path usage in <code>test_rsync_roots_no_roots</code></li>
<li><a
href="https://github.com/pytest-dev/pytest-xdist/commit/58a51bc14015d211761e44c2bdacab09c3893668"><code>58a51bc</code></a>
[pre-commit.ci] pre-commit autoupdate</li>
<li><a
href="https://github.com/pytest-dev/pytest-xdist/commit/59a2ad0150697b9ff837f3ae8dcf6e074d5a114b"><code>59a2ad0</code></a>
Merge pull request <a
href="https://redirect.github.com/pytest-dev/pytest-xdist/issues/1220">#1220</a>
from pytest-dev/dependabot/github_actions/github-act...</li>
<li><a
href="https://github.com/pytest-dev/pytest-xdist/commit/d42b9c72044855236c68286ca3bdb34486a05872"><code>d42b9c7</code></a>
build(deps): bump hynek/build-and-inspect-python-package</li>
<li><a
href="https://github.com/pytest-dev/pytest-xdist/commit/ebfcb99072aed3503fda5175245f28895a0204bb"><code>ebfcb99</code></a>
Merge pull request <a
href="https://redirect.github.com/pytest-dev/pytest-xdist/issues/1206">#1206</a>
from pytest-dev/release-3.7.0</li>
<li><a
href="https://github.com/pytest-dev/pytest-xdist/commit/23b7fd6054298a530b02b33d07007b3082a36277"><code>23b7fd6</code></a>
[pre-commit.ci] pre-commit autoupdate (<a
href="https://redirect.github.com/pytest-dev/pytest-xdist/issues/1207">#1207</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/pytest-dev/pytest-xdist/compare/v3.6.0...v3.8.0">compare
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

### PR #1213: chore(deps-dev): update pytest-xdist requirement from >=3.6 to >=3.8.0 in /services/claw-interface

Updates the requirements on [pytest-xdist](https://github.com/pytest-dev/pytest-xdist) to permit the latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/pytest-dev/pytest-xdist/blob/master/CHANGELOG.rst">pytest-xdist's changelog</a>.</em></p>
<blockquote>
<h1>pytest-xdist 3.8.0 (2025-06-30)</h1>
<h2>Features</h2>
<ul>
<li>
<p><code>[#1083](https://github.com/pytest-dev/pytest-xdist/issues/1083) &lt;https://github.com/pytest-dev/pytest-xdist/issues/1083&gt;</code>_: Add <code>--no-loadscope-reorder</code> and <code>--loadscope-reorder</code> option to control whether to automatically reorder tests in loadscope for tests where relative ordering matters. This only applies when using <code>loadscope</code>.</p>
<p>For example, [test_file_1, test_file_2, ..., test_file_n] are given as input test files, if <code>--no-loadscope-reorder</code> is used, for either worker, the <code>test_file_a</code> will be executed before <code>test_file_b</code> only if <code>a &lt; b</code>.</p>
<p>The default behavior is to reorder the tests to maximize the number of tests that can be executed in parallel.</p>
</li>
</ul>
<h1>pytest-xdist 3.7.0 (2025-05-26)</h1>
<h2>Features</h2>
<ul>
<li>
<p><code>[#1142](https://github.com/pytest-dev/pytest-xdist/issues/1142) &lt;https://github.com/pytest-dev/pytest-xdist/issues/1142&gt;</code>_: Added support for Python 3.13.</p>
</li>
<li>
<p><code>[#1144](https://github.com/pytest-dev/pytest-xdist/issues/1144) &lt;https://github.com/pytest-dev/pytest-xdist/issues/1144&gt;</code>_: The internal <code>steal</code> command is now atomic - it unschedules either all requested tests or none.</p>
<p>This is a prerequisite for group/scope support in the <code>worksteal</code> scheduler, so test groups won't be broken up incorrectly.</p>
</li>
<li>
<p><code>[#1170](https://github.com/pytest-dev/pytest-xdist/issues/1170) &lt;https://github.com/pytest-dev/pytest-xdist/issues/1170&gt;</code>_: Add the <code>--px</code> arg to create proxy gateways.</p>
<p>Proxy gateways are passed to additional gateways using the <code>via</code> keyword.
They can serve as a way to run multiple workers on remote machines.</p>
</li>
<li>
<p><code>[#1200](https://github.com/pytest-dev/pytest-xdist/issues/1200) &lt;https://github.com/pytest-dev/pytest-xdist/issues/1200&gt;</code>_: Now multiple <code>xdist_group</code> markers are considered when assigning tests to groups (order does not matter).</p>
<p>Previously, only the last marker would assign a test to a group, but now if a test has multiple <code>xdist_group</code> marks applied (for example via parametrization or via fixtures), they are merged to make a new group.</p>
</li>
</ul>
<h2>Removals</h2>
<ul>
<li><code>[#1162](https://github.com/pytest-dev/pytest-xdist/issues/1162) &lt;https://github.com/pytest-dev/pytest-xdist/issues/1162&gt;</code>_: Dropped support for EOL Python 3.8.</li>
</ul>
<h2>Trivial Changes</h2>
<ul>
<li>
<p><code>[#1092](https://github.com/pytest-dev/pytest-xdist/issues/1092) &lt;https://github.com/pytest-dev/pytest-xdist/issues/1092&gt;</code>_: Update an error message to better indicate where users should go for more information.</p>
</li>
<li>
<p><code>[#1190](https://github.com/pytest-dev/pytest-xdist/issues/1190) &lt;https://github.com/pytest-dev/pytest-xdist/issues/1190&gt;</code>_: Switched to using a SPDX license identifier introduced in PEP 639.</p>
</li>
</ul>
<h1>pytest-xdist 3.6.1 (2024-04-28)</h1>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/pytest-dev/pytest-xdist/commit/1e3e4dc16523c8a8f6c67d95a950166420718c99"><code>1e3e4dc</code></a> Release 3.8.0</li>
<li><a href="https://github.com/pytest-dev/pytest-xdist/commit/600aad575a4e4382855145b0c464d51b8f0b7242"><code>600aad5</code></a> Ensure all xdist group names are strings (<a href="https://redirect.github.com/pytest-dev/pytest-xdist/issues/1216">#1216</a>)</li>
<li><a href="https://github.com/pytest-dev/pytest-xdist/commit/9d7ba5b5fbbbe26793fbfb7cb1903eb69425cf09"><code>9d7ba5b</code></a> Add <code>--no-loadscope-reorder</code> and <code>--loadscope-reorder</code> options (<a href="https://redirect.github.com/pytest-dev/pytest-xdist/issues/1217">#1217</a>)</li>
<li><a href="https://github.com/pytest-dev/pytest-xdist/commit/532f07fb181bb1546eda79bbe6b46bdb56c699e1"><code>532f07f</code></a> Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest-xdist/issues/1210">#1210</a> from pytest-dev/pre-commit-ci-update-config</li>
<li><a href="https://github.com/pytest-dev/pytest-xdist/commit/0883ad085e0cf039c8ae13eb2789c1076544d225"><code>0883ad0</code></a> Fix Path usage in <code>test_rsync_roots_no_roots</code></li>
<li><a href="https://github.com/pytest-dev/pytest-xdist/commit/58a51bc14015d211761e44c2bdacab09c3893668"><code>58a51bc</code></a> [pre-commit.ci] pre-commit autoupdate</li>
<li><a href="https://github.com/pytest-dev/pytest-xdist/commit/59a2ad0150697b9ff837f3ae8dcf6e074d5a114b"><code>59a2ad0</code></a> Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest-xdist/issues/1220">#1220</a> from pytest-dev/dependabot/github_actions/github-act...</li>
<li><a href="https://github.com/pytest-dev/pytest-xdist/commit/d42b9c72044855236c68286ca3bdb34486a05872"><code>d42b9c7</code></a> build(deps): bump hynek/build-and-inspect-python-package</li>
<li><a href="https://github.com/pytest-dev/pytest-xdist/commit/ebfcb99072aed3503fda5175245f28895a0204bb"><code>ebfcb99</code></a> Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest-xdist/issues/1206">#1206</a> from pytest-dev/release-3.7.0</li>
<li><a href="https://github.com/pytest-dev/pytest-xdist/commit/23b7fd6054298a530b02b33d07007b3082a36277"><code>23b7fd6</code></a> [pre-commit.ci] pre-commit autoupdate (<a href="https://redirect.github.com/pytest-dev/pytest-xdist/issues/1207">#1207</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/pytest-dev/pytest-xdist/compare/v3.6.0...v3.8.0">compare view</a></li>
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

---

## c194e88

**作者**: dependabot[bot]
**日期**: 2026-04-22T10:02:45Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/c194e88957b00a77c29d9c5b7c3d7824b76cbb9f](https://github.com/SerendipityOneInc/ecap-workspace/commit/c194e88957b00a77c29d9c5b7c3d7824b76cbb9f)

### Commit Message
```
chore(deps): update openai requirement from >=1.0.0 to >=2.32.0 in /services/claw-interface (#1209)

Updates the requirements on
[openai](https://github.com/openai/openai-python) to permit the latest
version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/releases">openai's
releases</a>.</em></p>
<blockquote>
<h2>v2.32.0</h2>
<h2>2.32.0 (2026-04-15)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.31.0...v2.32.0">v2.31.0...v2.32.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add detail to InputFileContent (<a
href="https://github.com/openai/openai-python/commit/60de21d1fcfbcadea0d9b8d884c73c9dc49d14ff">60de21d</a>)</li>
<li><strong>api:</strong> add OAuthErrorCode type (<a
href="https://github.com/openai/openai-python/commit/0c8d2c3b44242c9139dc554896ea489b56e236b8">0c8d2c3</a>)</li>
<li><strong>client:</strong> add event handler implementation for
websockets (<a
href="https://github.com/openai/openai-python/commit/0280d0568f706684ecbf0aabf3575cdcb7fd22d5">0280d05</a>)</li>
<li><strong>client:</strong> allow enqueuing to websockets even when not
connected (<a
href="https://github.com/openai/openai-python/commit/67aa20e69bc0e4a3b7694327c808606bfa24a966">67aa20e</a>)</li>
<li><strong>client:</strong> support reconnection in websockets (<a
href="https://github.com/openai/openai-python/commit/eb72a953ea9dc5beec3eef537be6eb32292c3f65">eb72a95</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li>ensure file data are only sent as 1 parameter (<a
href="https://github.com/openai/openai-python/commit/c0c2ecd0f6b64fa5fafda6134bb06995b143a2cf">c0c2ecd</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>improve examples (<a
href="https://github.com/openai/openai-python/commit/84712fa0f094b53151a0fe6ac85aa98018b2a7e2">84712fa</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's
changelog</a>.</em></p>
<blockquote>
<h2>2.32.0 (2026-04-15)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.31.0...v2.32.0">v2.31.0...v2.32.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add detail to InputFileContent (<a
href="https://github.com/openai/openai-python/commit/60de21d1fcfbcadea0d9b8d884c73c9dc49d14ff">60de21d</a>)</li>
<li><strong>api:</strong> add OAuthErrorCode type (<a
href="https://github.com/openai/openai-python/commit/0c8d2c3b44242c9139dc554896ea489b56e236b8">0c8d2c3</a>)</li>
<li><strong>client:</strong> add event handler implementation for
websockets (<a
href="https://github.com/openai/openai-python/commit/0280d0568f706684ecbf0aabf3575cdcb7fd22d5">0280d05</a>)</li>
<li><strong>client:</strong> allow enqueuing to websockets even when not
connected (<a
href="https://github.com/openai/openai-python/commit/67aa20e69bc0e4a3b7694327c808606bfa24a966">67aa20e</a>)</li>
<li><strong>client:</strong> support reconnection in websockets (<a
href="https://github.com/openai/openai-python/commit/eb72a953ea9dc5beec3eef537be6eb32292c3f65">eb72a95</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li>ensure file data are only sent as 1 parameter (<a
href="https://github.com/openai/openai-python/commit/c0c2ecd0f6b64fa5fafda6134bb06995b143a2cf">c0c2ecd</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>improve examples (<a
href="https://github.com/openai/openai-python/commit/84712fa0f094b53151a0fe6ac85aa98018b2a7e2">84712fa</a>)</li>
</ul>
<h2>2.31.0 (2026-04-08)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.30.0...v2.31.0">v2.30.0...v2.31.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> add phase field to conversations message (<a
href="https://github.com/openai/openai-python/commit/3e5834efb39b24e019a29dc54d890c67d18cbb54">3e5834e</a>)</li>
<li><strong>api:</strong> add web_search_call.results to
ResponseIncludable type (<a
href="https://github.com/openai/openai-python/commit/ffd8741dd38609a5af0159ceb800d8ddba7925f8">ffd8741</a>)</li>
<li><strong>client:</strong> add support for short-lived tokens (<a
href="https://redirect.github.com/openai/openai-python/issues/1608">#1608</a>)
(<a
href="https://github.com/openai/openai-python/commit/22fe7228d4990c197cd721b3ad7931ad05cca5dd">22fe722</a>)</li>
<li><strong>client:</strong> support sending raw data over websockets
(<a
href="https://github.com/openai/openai-python/commit/f1bc52ef641dfca6fdf2a5b00ce3b09bff2552f5">f1bc52e</a>)</li>
<li><strong>internal:</strong> implement indices array format for query
and form serialization (<a
href="https://github.com/openai/openai-python/commit/49194cfa711328216ff131d6f65c9298822a7c51">49194cf</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>client:</strong> preserve hardcoded query params when
merging with user params (<a
href="https://github.com/openai/openai-python/commit/92e109c3d9569a942e1919e75977dc13fa015f9a">92e109c</a>)</li>
<li><strong>types:</strong> remove web_search_call.results from
ResponseIncludable (<a
href="https://github.com/openai/openai-python/commit/d3cc40165cd86015833d15167cc7712b4102f932">d3cc401</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>tests:</strong> bump steady to v0.20.1 (<a
href="https://github.com/openai/openai-python/commit/d60e2eea7f6916540cd4ba901dceb07051119da4">d60e2ee</a>)</li>
<li><strong>tests:</strong> bump steady to v0.20.2 (<a
href="https://github.com/openai/openai-python/commit/6508d474332d4e82d9615c0a9a77379f9b5e4412">6508d47</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li><strong>api:</strong> update file parameter descriptions in
vector_stores files and file_batches (<a
href="https://github.com/openai/openai-python/commit/a9e7ebd505b9ae90514339aa63c6f1984a08cf6b">a9e7ebd</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/openai/openai-python/commit/e507a4ebeea4c3f93cd48986014a3e2ca79230c2"><code>e507a4e</code></a>
release: 2.32.0 (<a
href="https://redirect.github.com/openai/openai-python/issues/3074">#3074</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/750354ed65565b31d0547bf00f4f3180ac1bfeef"><code>750354e</code></a>
release: 2.31.0</li>
<li><a
href="https://github.com/openai/openai-python/commit/5be95364a5a82746cb7b1c77df10dfaf138496bb"><code>5be9536</code></a>
feat(client): add support for short-lived tokens (<a
href="https://redirect.github.com/openai/openai-python/issues/1608">#1608</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/f1fd4fae0329ee3df2f1bb25d93f51311782ad1a"><code>f1fd4fa</code></a>
feat(client): support sending raw data over websockets</li>
<li><a
href="https://github.com/openai/openai-python/commit/73ea2f75ba57a1db964518b33b790b1e1251b8d5"><code>73ea2f7</code></a>
fix(client): preserve hardcoded query params when merging with user
params</li>
<li><a
href="https://github.com/openai/openai-python/commit/454b2575d59a086f279d99dc791058acee2f14c0"><code>454b257</code></a>
feat(api): add web_search_call.results to ResponseIncludable type</li>
<li><a
href="https://github.com/openai/openai-python/commit/de2c7b1d087f41f33ada85a7460f32e55331778a"><code>de2c7b1</code></a>
chore(tests): bump steady to v0.20.2</li>
<li><a
href="https://github.com/openai/openai-python/commit/6efca95a76f6ca9cb91fdf536c6c9ebcef075541"><code>6efca95</code></a>
chore(tests): bump steady to v0.20.1</li>
<li><a
href="https://github.com/openai/openai-python/commit/2076d85f9226113e4ba360a7f456091988092dbf"><code>2076d85</code></a>
feat(api): add phase field to conversations message</li>
<li><a
href="https://github.com/openai/openai-python/commit/c0c59afa39a82f73063a52f624a9a4a2a6bf3313"><code>c0c59af</code></a>
fix(types): remove web_search_call.results from ResponseIncludable</li>
<li>Additional commits viewable in <a
href="https://github.com/openai/openai-python/compare/v1.0.0...v2.32.0">compare
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

### PR #1209: chore(deps): update openai requirement from >=1.0.0 to >=2.32.0 in /services/claw-interface

Updates the requirements on [openai](https://github.com/openai/openai-python) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/releases">openai's releases</a>.</em></p>
<blockquote>
<h2>v2.32.0</h2>
<h2>2.32.0 (2026-04-15)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.31.0...v2.32.0">v2.31.0...v2.32.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add detail to InputFileContent (<a href="https://github.com/openai/openai-python/commit/60de21d1fcfbcadea0d9b8d884c73c9dc49d14ff">60de21d</a>)</li>
<li><strong>api:</strong> add OAuthErrorCode type (<a href="https://github.com/openai/openai-python/commit/0c8d2c3b44242c9139dc554896ea489b56e236b8">0c8d2c3</a>)</li>
<li><strong>client:</strong> add event handler implementation for websockets (<a href="https://github.com/openai/openai-python/commit/0280d0568f706684ecbf0aabf3575cdcb7fd22d5">0280d05</a>)</li>
<li><strong>client:</strong> allow enqueuing to websockets even when not connected (<a href="https://github.com/openai/openai-python/commit/67aa20e69bc0e4a3b7694327c808606bfa24a966">67aa20e</a>)</li>
<li><strong>client:</strong> support reconnection in websockets (<a href="https://github.com/openai/openai-python/commit/eb72a953ea9dc5beec3eef537be6eb32292c3f65">eb72a95</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li>ensure file data are only sent as 1 parameter (<a href="https://github.com/openai/openai-python/commit/c0c2ecd0f6b64fa5fafda6134bb06995b143a2cf">c0c2ecd</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>improve examples (<a href="https://github.com/openai/openai-python/commit/84712fa0f094b53151a0fe6ac85aa98018b2a7e2">84712fa</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's changelog</a>.</em></p>
<blockquote>
<h2>2.32.0 (2026-04-15)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.31.0...v2.32.0">v2.31.0...v2.32.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add detail to InputFileContent (<a href="https://github.com/openai/openai-python/commit/60de21d1fcfbcadea0d9b8d884c73c9dc49d14ff">60de21d</a>)</li>
<li><strong>api:</strong> add OAuthErrorCode type (<a href="https://github.com/openai/openai-python/commit/0c8d2c3b44242c9139dc554896ea489b56e236b8">0c8d2c3</a>)</li>
<li><strong>client:</strong> add event handler implementation for websockets (<a href="https://github.com/openai/openai-python/commit/0280d0568f706684ecbf0aabf3575cdcb7fd22d5">0280d05</a>)</li>
<li><strong>client:</strong> allow enqueuing to websockets even when not connected (<a href="https://github.com/openai/openai-python/commit/67aa20e69bc0e4a3b7694327c808606bfa24a966">67aa20e</a>)</li>
<li><strong>client:</strong> support reconnection in websockets (<a href="https://github.com/openai/openai-python/commit/eb72a953ea9dc5beec3eef537be6eb32292c3f65">eb72a95</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li>ensure file data are only sent as 1 parameter (<a href="https://github.com/openai/openai-python/commit/c0c2ecd0f6b64fa5fafda6134bb06995b143a2cf">c0c2ecd</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>improve examples (<a href="https://github.com/openai/openai-python/commit/84712fa0f094b53151a0fe6ac85aa98018b2a7e2">84712fa</a>)</li>
</ul>
<h2>2.31.0 (2026-04-08)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.30.0...v2.31.0">v2.30.0...v2.31.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> add phase field to conversations message (<a href="https://github.com/openai/openai-python/commit/3e5834efb39b24e019a29dc54d890c67d18cbb54">3e5834e</a>)</li>
<li><strong>api:</strong> add web_search_call.results to ResponseIncludable type (<a href="https://github.com/openai/openai-python/commit/ffd8741dd38609a5af0159ceb800d8ddba7925f8">ffd8741</a>)</li>
<li><strong>client:</strong> add support for short-lived tokens (<a href="https://redirect.github.com/openai/openai-python/issues/1608">#1608</a>) (<a href="https://github.com/openai/openai-python/commit/22fe7228d4990c197cd721b3ad7931ad05cca5dd">22fe722</a>)</li>
<li><strong>client:</strong> support sending raw data over websockets (<a href="https://github.com/openai/openai-python/commit/f1bc52ef641dfca6fdf2a5b00ce3b09bff2552f5">f1bc52e</a>)</li>
<li><strong>internal:</strong> implement indices array format for query and form serialization (<a href="https://github.com/openai/openai-python/commit/49194cfa711328216ff131d6f65c9298822a7c51">49194cf</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>client:</strong> preserve hardcoded query params when merging with user params (<a href="https://github.com/openai/openai-python/commit/92e109c3d9569a942e1919e75977dc13fa015f9a">92e109c</a>)</li>
<li><strong>types:</strong> remove web_search_call.results from ResponseIncludable (<a href="https://github.com/openai/openai-python/commit/d3cc40165cd86015833d15167cc7712b4102f932">d3cc401</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>tests:</strong> bump steady to v0.20.1 (<a href="https://github.com/openai/openai-python/commit/d60e2eea7f6916540cd4ba901dceb07051119da4">d60e2ee</a>)</li>
<li><strong>tests:</strong> bump steady to v0.20.2 (<a href="https://github.com/openai/openai-python/commit/6508d474332d4e82d9615c0a9a77379f9b5e4412">6508d47</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li><strong>api:</strong> update file parameter descriptions in vector_stores files and file_batches (<a href="https://github.com/openai/openai-python/commit/a9e7ebd505b9ae90514339aa63c6f1984a08cf6b">a9e7ebd</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/openai/openai-python/commit/e507a4ebeea4c3f93cd48986014a3e2ca79230c2"><code>e507a4e</code></a> release: 2.32.0 (<a href="https://redirect.github.com/openai/openai-python/issues/3074">#3074</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/750354ed65565b31d0547bf00f4f3180ac1bfeef"><code>750354e</code></a> release: 2.31.0</li>
<li><a href="https://github.com/openai/openai-python/commit/5be95364a5a82746cb7b1c77df10dfaf138496bb"><code>5be9536</code></a> feat(client): add support for short-lived tokens (<a href="https://redirect.github.com/openai/openai-python/issues/1608">#1608</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/f1fd4fae0329ee3df2f1bb25d93f51311782ad1a"><code>f1fd4fa</code></a> feat(client): support sending raw data over websockets</li>
<li><a href="https://github.com/openai/openai-python/commit/73ea2f75ba57a1db964518b33b790b1e1251b8d5"><code>73ea2f7</code></a> fix(client): preserve hardcoded query params when merging with user params</li>
<li><a href="https://github.com/openai/openai-python/commit/454b2575d59a086f279d99dc791058acee2f14c0"><code>454b257</code></a> feat(api): add web_search_call.results to ResponseIncludable type</li>
<li><a href="https://github.com/openai/openai-python/commit/de2c7b1d087f41f33ada85a7460f32e55331778a"><code>de2c7b1</code></a> chore(tests): bump steady to v0.20.2</li>
<li><a href="https://github.com/openai/openai-python/commit/6efca95a76f6ca9cb91fdf536c6c9ebcef075541"><code>6efca95</code></a> chore(tests): bump steady to v0.20.1</li>
<li><a href="https://github.com/openai/openai-python/commit/2076d85f9226113e4ba360a7f456091988092dbf"><code>2076d85</code></a> feat(api): add phase field to conversations message</li>
<li><a href="https://github.com/openai/openai-python/commit/c0c59afa39a82f73063a52f624a9a4a2a6bf3313"><code>c0c59af</code></a> fix(types): remove web_search_call.results from ResponseIncludable</li>
<li>Additional commits viewable in <a href="https://github.com/openai/openai-python/compare/v1.0.0...v2.32.0">compare view</a></li>
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

---

## 7b580f5

**作者**: dependabot[bot]
**日期**: 2026-04-22T10:02:26Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/7b580f5b92b0a91c1494d4a7bbff55ac919a5b21](https://github.com/SerendipityOneInc/ecap-workspace/commit/7b580f5b92b0a91c1494d4a7bbff55ac919a5b21)

### Commit Message
```
chore(deps): bump the minor-and-patch group in /web with 2 updates (#1208)

[//]: # (dependabot-start)
⚠️  **Dependabot is rebasing this PR** ⚠️ 

Rebasing might not happen immediately, so don't worry if this takes some
time.

Note: if you make any changes to this PR yourself, they will take
precedence over the rebase.

---

[//]: # (dependabot-end)

Bumps the minor-and-patch group in /web with 2 updates:
[lucide-react](https://github.com/lucide-icons/lucide/tree/HEAD/packages/lucide-react)
and
[@eslint/js](https://github.com/eslint/eslint/tree/HEAD/packages/js).

Updates `lucide-react` from 0.546.0 to 0.577.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/lucide-icons/lucide/releases">lucide-react's
releases</a>.</em></p>
<blockquote>
<h2>Version 0.577.0</h2>
<h2>What's Changed</h2>
<ul>
<li>chore(deps): bump rollup from 4.53.3 to 4.59.0 by <a
href="https://github.com/dependabot"><code>@​dependabot</code></a>[bot]
in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/4106">lucide-icons/lucide#4106</a></li>
<li>fix(repo): correctly ignore docs/releaseMetadata via .gitignore by
<a href="https://github.com/bhavberi"><code>@​bhavberi</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/4100">lucide-icons/lucide#4100</a></li>
<li>feat(icons): added <code>ellipse</code> icon by <a
href="https://github.com/KISHORE-KUMAR-S"><code>@​KISHORE-KUMAR-S</code></a>
in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/3749">lucide-icons/lucide#3749</a></li>
</ul>
<h2>New Contributors</h2>
<ul>
<li><a href="https://github.com/bhavberi"><code>@​bhavberi</code></a>
made their first contribution in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/4100">lucide-icons/lucide#4100</a></li>
<li><a
href="https://github.com/KISHORE-KUMAR-S"><code>@​KISHORE-KUMAR-S</code></a>
made their first contribution in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/3749">lucide-icons/lucide#3749</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a
href="https://github.com/lucide-icons/lucide/compare/0.576.0...0.577.0">https://github.com/lucide-icons/lucide/compare/0.576.0...0.577.0</a></p>
<h2>Version 0.576.0</h2>
<h2>What's Changed</h2>
<ul>
<li>Added zodiac signs by <a
href="https://github.com/karsa-mistmere"><code>@​karsa-mistmere</code></a>
in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/712">lucide-icons/lucide#712</a></li>
<li>fix(icons): fixes guideline violations in <code>package-*</code>
icons. by <a
href="https://github.com/karsa-mistmere"><code>@​karsa-mistmere</code></a>
in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/4074">lucide-icons/lucide#4074</a></li>
<li>fix(icons): changed <code>receipt</code> icon by <a
href="https://github.com/karsa-mistmere"><code>@​karsa-mistmere</code></a>
in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/4075">lucide-icons/lucide#4075</a></li>
<li>fix(icons): updated <code>cuboid</code> icon tags and categories by
<a
href="https://github.com/karsa-mistmere"><code>@​karsa-mistmere</code></a>
in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/4095">lucide-icons/lucide#4095</a></li>
<li>fix(icons): changed <code>cuboid</code> icon by <a
href="https://github.com/jamiemlaw"><code>@​jamiemlaw</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/4098">lucide-icons/lucide#4098</a></li>
<li>fix(lucide-font, lucide-static): Fixing stable code points by <a
href="https://github.com/ericfennis"><code>@​ericfennis</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/3894">lucide-icons/lucide#3894</a></li>
<li>feat(icons): added <code>fishing-rod</code> icon by <a
href="https://github.com/7ender"><code>@​7ender</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/3839">lucide-icons/lucide#3839</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a
href="https://github.com/lucide-icons/lucide/compare/0.575.0...0.576.0">https://github.com/lucide-icons/lucide/compare/0.575.0...0.576.0</a></p>
<h2>Version 0.575.0</h2>
<h2>What's Changed</h2>
<ul>
<li>feat(icons): added <code>message-square-check</code> icon by <a
href="https://github.com/karsa-mistmere"><code>@​karsa-mistmere</code></a>
in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/4076">lucide-icons/lucide#4076</a></li>
<li>fix(lucide): Fix ESM Module output path in build by <a
href="https://github.com/ericfennis"><code>@​ericfennis</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/4084">lucide-icons/lucide#4084</a></li>
<li>feat(icons): added <code>metronome</code> icon by <a
href="https://github.com/edwloef"><code>@​edwloef</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/4063">lucide-icons/lucide#4063</a></li>
<li>fix(icons): remove execution permission of SVG files by <a
href="https://github.com/duckafire"><code>@​duckafire</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/4053">lucide-icons/lucide#4053</a></li>
<li>fix(icons): changed <code>file-pen-line</code> icon by <a
href="https://github.com/jguddas"><code>@​jguddas</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/3970">lucide-icons/lucide#3970</a></li>
<li>feat(icons): added <code>square-arrow-right-exit</code> and
<code>square-arrow-right-enter</code> icons by <a
href="https://github.com/EthanHazel"><code>@​EthanHazel</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/3958">lucide-icons/lucide#3958</a></li>
<li>fix(icons): renamed <code>flip-*</code> to
<code>square-centerline-dashed-*</code> by <a
href="https://github.com/jguddas"><code>@​jguddas</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/3945">lucide-icons/lucide#3945</a></li>
</ul>
<h2>New Contributors</h2>
<ul>
<li><a href="https://github.com/edwloef"><code>@​edwloef</code></a> made
their first contribution in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/4063">lucide-icons/lucide#4063</a></li>
<li><a href="https://github.com/duckafire"><code>@​duckafire</code></a>
made their first contribution in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/4053">lucide-icons/lucide#4053</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a
href="https://github.com/lucide-icons/lucide/compare/0.573.0...0.575.0">https://github.com/lucide-icons/lucide/compare/0.573.0...0.575.0</a></p>
<h2>Version 0.574.0</h2>
<h2>What's Changed</h2>
<ul>
<li>fix(icons): changed <code>rocking-chair</code> icon by <a
href="https://github.com/jamiemlaw"><code>@​jamiemlaw</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/3445">lucide-icons/lucide#3445</a></li>
<li>fix(icons): flipped <code>coins</code> icon by <a
href="https://github.com/jguddas"><code>@​jguddas</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/3158">lucide-icons/lucide#3158</a></li>
<li>feat(icons): added <code>x-line-top</code> icon by <a
href="https://github.com/jguddas"><code>@​jguddas</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/2838">lucide-icons/lucide#2838</a></li>
<li>feat(icons): added <code>mouse-left</code> icon by <a
href="https://github.com/marvfash"><code>@​marvfash</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/2788">lucide-icons/lucide#2788</a></li>
<li>feat(icons): added <code>mouse-right</code> icon by <a
href="https://github.com/marvfash"><code>@​marvfash</code></a> in <a
href="https://redirect.github.com/lucide-icons/lucide/pull/2787">lucide-icons/lucide#2787</a></li>
</ul>
<h2>New Contributors</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/lucide-icons/lucide/commit/f6c0d0603ae2bc92f54d0397d70233274e53da97"><code>f6c0d06</code></a>
chore(deps): bump rollup from 4.53.3 to 4.59.0 (<a
href="https://github.com/lucide-icons/lucide/tree/HEAD/packages/lucide-react/issues/4106">#4106</a>)</li>
<li><a
href="https://github.com/lucide-icons/lucide/commit/67c04854576e5afce536e332d1f44ce5cccec4fe"><code>67c0485</code></a>
feat(scripts): added helper script to automatically update
OpenCollective bac...</li>
<li><a
href="https://github.com/lucide-icons/lucide/commit/b6ed43d48cfed254e9c3cdf68fb4bbbf8e634580"><code>b6ed43d</code></a>
feat(packages): Added aria-hidden fallback for decorative icons to all
packag...</li>
<li><a
href="https://github.com/lucide-icons/lucide/commit/076e0bbcd91e4720c7bc2180e474c855e06c927c"><code>076e0bb</code></a>
chore(dependencies): Update dependencies (<a
href="https://github.com/lucide-icons/lucide/tree/HEAD/packages/lucide-react/issues/3809">#3809</a>)</li>
<li><a
href="https://github.com/lucide-icons/lucide/commit/80d6f737e0a02c3c11af8d87cb986e33a4ef08d8"><code>80d6f73</code></a>
fix(icons): Rename fingerprint icon to fingerprint-pattern (<a
href="https://github.com/lucide-icons/lucide/tree/HEAD/packages/lucide-react/issues/3767">#3767</a>)</li>
<li>See full diff in <a
href="https://github.com/lucide-icons/lucide/commits/0.577.0/packages/lucide-react">compare
view</a></li>
</ul>
</details>
<details>
<summary>Maintainer changes</summary>
<p>This version was pushed to npm by <a
href="https://www.npmjs.com/~GitHub%20Actions">GitHub Actions</a>, a new
releaser for lucide-react since your current version.</p>
</details>
<br />

Updates `@eslint/js` from 9.39.3 to 9.39.4
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/eslint/eslint/releases"><code>@​eslint/js</code>'s
releases</a>.</em></p>
<blockquote>
<h2>v9.39.4</h2>
<h2>Bug Fixes</h2>
<ul>
<li><a
href="https://github.com/eslint/eslint/commit/f18f6c8ae92a1bcfc558f48c0bd863ea94067459"><code>f18f6c8</code></a>
fix: update dependency minimatch to ^3.1.5 (<a
href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20564">#20564</a>)
(Milos Djermanovic)</li>
<li><a
href="https://github.com/eslint/eslint/commit/a3c868f6ef103c1caff9d15f744f9ebd995e872f"><code>a3c868f</code></a>
fix: update dependency <code>@​eslint/eslintrc</code> to ^3.3.4 (<a
href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20554">#20554</a>)
(Milos Djermanovic)</li>
<li><a
href="https://github.com/eslint/eslint/commit/234d005da6cd3c924f359e3783fbf565a3c047c3"><code>234d005</code></a>
fix: minimatch security vulnerability patch for v9.x (<a
href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20549">#20549</a>)
(Andrej Beles)</li>
<li><a
href="https://github.com/eslint/eslint/commit/b1b37eecaa033d2e390e1d8f1d6e68d0f5ff3a6a"><code>b1b37ee</code></a>
fix: update <code>ajv</code> to <code>6.14.0</code> to address security
vulnerabilities (<a
href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20538">#20538</a>)
(루밀LuMir)</li>
</ul>
<h2>Documentation</h2>
<ul>
<li><a
href="https://github.com/eslint/eslint/commit/46751526037682f8b42abcfb3e06d19213719347"><code>4675152</code></a>
docs: add deprecation notice partial (<a
href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20520">#20520</a>)
(Milos Djermanovic)</li>
</ul>
<h2>Chores</h2>
<ul>
<li><a
href="https://github.com/eslint/eslint/commit/b8b4eb15901c1bd6ef40d2589da4ae75795c0f6e"><code>b8b4eb1</code></a>
chore: update dependencies for ESLint v9.39.4 (<a
href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20596">#20596</a>)
(Francesco Trotta)</li>
<li><a
href="https://github.com/eslint/eslint/commit/71b2f6b628b76157b4a2a296cb969dc56abb296c"><code>71b2f6b</code></a>
chore: package.json update for <code>@​eslint/js</code> release
(Jenkins)</li>
<li><a
href="https://github.com/eslint/eslint/commit/1d16c2fa3998440ae7b0f6e2612935bd6b0ded1d"><code>1d16c2f</code></a>
ci: pin Node.js 25.6.1 (<a
href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20563">#20563</a>)
(Milos Djermanovic)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/eslint/eslint/commit/71b2f6b628b76157b4a2a296cb969dc56abb296c"><code>71b2f6b</code></a>
chore: package.json update for <code>@​eslint/js</code> release</li>
<li>See full diff in <a
href="https://github.com/eslint/eslint/commits/v9.39.4/packages/js">compare
view</a></li>
</ul>
</details>
<br />

<details>
<summary>Most Recent Ignore Conditions Applied to This Pull
Request</summary>

| Dependency Name | Ignore Conditions |
| --- | --- |
| @eslint/js | [>= 10.a, < 11] |
| lucide-react | [>= 1.a, < 2] |
</details>


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
- `@dependabot ignore <dependency name> major version` will close this
group update PR and stop Dependabot creating any more for the specific
dependency's major version (unless you unignore this specific
dependency's major version or upgrade to it yourself)
- `@dependabot ignore <dependency name> minor version` will close this
group update PR and stop Dependabot creating any more for the specific
dependency's minor version (unless you unignore this specific
dependency's minor version or upgrade to it yourself)
- `@dependabot ignore <dependency name>` will close this group update PR
and stop Dependabot creating any more for the specific dependency
(unless you unignore this specific dependency or upgrade to it yourself)
- `@dependabot unignore <dependency name>` will remove all of the ignore
conditions of the specified dependency
- `@dependabot unignore <dependency name> <ignore condition>` will
remove the ignore condition of the specified dependency and ignore
conditions


</details>

---------

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
Co-authored-by: chris-srp <chris@srp.one>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1208: chore(deps): bump the minor-and-patch group in /web with 2 updates

Bumps the minor-and-patch group in /web with 2 updates: [lucide-react](https://github.com/lucide-icons/lucide/tree/HEAD/packages/lucide-react) and [@eslint/js](https://github.com/eslint/eslint/tree/HEAD/packages/js).

Updates `lucide-react` from 0.546.0 to 0.577.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/lucide-icons/lucide/releases">lucide-react's releases</a>.</em></p>
<blockquote>
<h2>Version 0.577.0</h2>
<h2>What's Changed</h2>
<ul>
<li>chore(deps): bump rollup from 4.53.3 to 4.59.0 by <a href="https://github.com/dependabot"><code>@​dependabot</code></a>[bot] in <a href="https://redirect.github.com/lucide-icons/lucide/pull/4106">lucide-icons/lucide#4106</a></li>
<li>fix(repo): correctly ignore docs/releaseMetadata via .gitignore by <a href="https://github.com/bhavberi"><code>@​bhavberi</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/4100">lucide-icons/lucide#4100</a></li>
<li>feat(icons): added <code>ellipse</code> icon by <a href="https://github.com/KISHORE-KUMAR-S"><code>@​KISHORE-KUMAR-S</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/3749">lucide-icons/lucide#3749</a></li>
</ul>
<h2>New Contributors</h2>
<ul>
<li><a href="https://github.com/bhavberi"><code>@​bhavberi</code></a> made their first contribution in <a href="https://redirect.github.com/lucide-icons/lucide/pull/4100">lucide-icons/lucide#4100</a></li>
<li><a href="https://github.com/KISHORE-KUMAR-S"><code>@​KISHORE-KUMAR-S</code></a> made their first contribution in <a href="https://redirect.github.com/lucide-icons/lucide/pull/3749">lucide-icons/lucide#3749</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/lucide-icons/lucide/compare/0.576.0...0.577.0">https://github.com/lucide-icons/lucide/compare/0.576.0...0.577.0</a></p>
<h2>Version 0.576.0</h2>
<h2>What's Changed</h2>
<ul>
<li>Added zodiac signs by <a href="https://github.com/karsa-mistmere"><code>@​karsa-mistmere</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/712">lucide-icons/lucide#712</a></li>
<li>fix(icons): fixes guideline violations in <code>package-*</code> icons. by <a href="https://github.com/karsa-mistmere"><code>@​karsa-mistmere</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/4074">lucide-icons/lucide#4074</a></li>
<li>fix(icons): changed <code>receipt</code> icon by <a href="https://github.com/karsa-mistmere"><code>@​karsa-mistmere</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/4075">lucide-icons/lucide#4075</a></li>
<li>fix(icons): updated <code>cuboid</code> icon tags and categories by <a href="https://github.com/karsa-mistmere"><code>@​karsa-mistmere</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/4095">lucide-icons/lucide#4095</a></li>
<li>fix(icons): changed <code>cuboid</code> icon by <a href="https://github.com/jamiemlaw"><code>@​jamiemlaw</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/4098">lucide-icons/lucide#4098</a></li>
<li>fix(lucide-font, lucide-static): Fixing stable code points by <a href="https://github.com/ericfennis"><code>@​ericfennis</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/3894">lucide-icons/lucide#3894</a></li>
<li>feat(icons): added <code>fishing-rod</code> icon by <a href="https://github.com/7ender"><code>@​7ender</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/3839">lucide-icons/lucide#3839</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/lucide-icons/lucide/compare/0.575.0...0.576.0">https://github.com/lucide-icons/lucide/compare/0.575.0...0.576.0</a></p>
<h2>Version 0.575.0</h2>
<h2>What's Changed</h2>
<ul>
<li>feat(icons): added <code>message-square-check</code> icon by <a href="https://github.com/karsa-mistmere"><code>@​karsa-mistmere</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/4076">lucide-icons/lucide#4076</a></li>
<li>fix(lucide): Fix ESM Module output path in build by <a href="https://github.com/ericfennis"><code>@​ericfennis</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/4084">lucide-icons/lucide#4084</a></li>
<li>feat(icons): added <code>metronome</code> icon by <a href="https://github.com/edwloef"><code>@​edwloef</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/4063">lucide-icons/lucide#4063</a></li>
<li>fix(icons): remove execution permission of SVG files by <a href="https://github.com/duckafire"><code>@​duckafire</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/4053">lucide-icons/lucide#4053</a></li>
<li>fix(icons): changed <code>file-pen-line</code> icon by <a href="https://github.com/jguddas"><code>@​jguddas</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/3970">lucide-icons/lucide#3970</a></li>
<li>feat(icons): added <code>square-arrow-right-exit</code> and <code>square-arrow-right-enter</code> icons by <a href="https://github.com/EthanHazel"><code>@​EthanHazel</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/3958">lucide-icons/lucide#3958</a></li>
<li>fix(icons): renamed <code>flip-*</code> to <code>square-centerline-dashed-*</code> by <a href="https://github.com/jguddas"><code>@​jguddas</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/3945">lucide-icons/lucide#3945</a></li>
</ul>
<h2>New Contributors</h2>
<ul>
<li><a href="https://github.com/edwloef"><code>@​edwloef</code></a> made their first contribution in <a href="https://redirect.github.com/lucide-icons/lucide/pull/4063">lucide-icons/lucide#4063</a></li>
<li><a href="https://github.com/duckafire"><code>@​duckafire</code></a> made their first contribution in <a href="https://redirect.github.com/lucide-icons/lucide/pull/4053">lucide-icons/lucide#4053</a></li>
</ul>
<p><strong>Full Changelog</strong>: <a href="https://github.com/lucide-icons/lucide/compare/0.573.0...0.575.0">https://github.com/lucide-icons/lucide/compare/0.573.0...0.575.0</a></p>
<h2>Version 0.574.0</h2>
<h2>What's Changed</h2>
<ul>
<li>fix(icons): changed <code>rocking-chair</code> icon by <a href="https://github.com/jamiemlaw"><code>@​jamiemlaw</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/3445">lucide-icons/lucide#3445</a></li>
<li>fix(icons): flipped <code>coins</code> icon by <a href="https://github.com/jguddas"><code>@​jguddas</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/3158">lucide-icons/lucide#3158</a></li>
<li>feat(icons): added <code>x-line-top</code> icon by <a href="https://github.com/jguddas"><code>@​jguddas</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/2838">lucide-icons/lucide#2838</a></li>
<li>feat(icons): added <code>mouse-left</code> icon by <a href="https://github.com/marvfash"><code>@​marvfash</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/2788">lucide-icons/lucide#2788</a></li>
<li>feat(icons): added <code>mouse-right</code> icon by <a href="https://github.com/marvfash"><code>@​marvfash</code></a> in <a href="https://redirect.github.com/lucide-icons/lucide/pull/2787">lucide-icons/lucide#2787</a></li>
</ul>
<h2>New Contributors</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/lucide-icons/lucide/commit/f6c0d0603ae2bc92f54d0397d70233274e53da97"><code>f6c0d06</code></a> chore(deps): bump rollup from 4.53.3 to 4.59.0 (<a href="https://github.com/lucide-icons/lucide/tree/HEAD/packages/lucide-react/issues/4106">#4106</a>)</li>
<li><a href="https://github.com/lucide-icons/lucide/commit/67c04854576e5afce536e332d1f44ce5cccec4fe"><code>67c0485</code></a> feat(scripts): added helper script to automatically update OpenCollective bac...</li>
<li><a href="https://github.com/lucide-icons/lucide/commit/b6ed43d48cfed254e9c3cdf68fb4bbbf8e634580"><code>b6ed43d</code></a> feat(packages): Added aria-hidden fallback for decorative icons to all packag...</li>
<li><a href="https://github.com/lucide-icons/lucide/commit/076e0bbcd91e4720c7bc2180e474c855e06c927c"><code>076e0bb</code></a> chore(dependencies): Update dependencies (<a href="https://github.com/lucide-icons/lucide/tree/HEAD/packages/lucide-react/issues/3809">#3809</a>)</li>
<li><a href="https://github.com/lucide-icons/lucide/commit/80d6f737e0a02c3c11af8d87cb986e33a4ef08d8"><code>80d6f73</code></a> fix(icons): Rename fingerprint icon to fingerprint-pattern (<a href="https://github.com/lucide-icons/lucide/tree/HEAD/packages/lucide-react/issues/3767">#3767</a>)</li>
<li>See full diff in <a href="https://github.com/lucide-icons/lucide/commits/0.577.0/packages/lucide-react">compare view</a></li>
</ul>
</details>
<details>
<summary>Maintainer changes</summary>
<p>This version was pushed to npm by <a href="https://www.npmjs.com/~GitHub%20Actions">GitHub Actions</a>, a new releaser for lucide-react since your current version.</p>
</details>
<br />

Updates `@eslint/js` from 9.39.3 to 9.39.4
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/eslint/eslint/releases"><code>@​eslint/js</code>'s releases</a>.</em></p>
<blockquote>
<h2>v9.39.4</h2>
<h2>Bug Fixes</h2>
<ul>
<li><a href="https://github.com/eslint/eslint/commit/f18f6c8ae92a1bcfc558f48c0bd863ea94067459"><code>f18f6c8</code></a> fix: update dependency minimatch to ^3.1.5 (<a href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20564">#20564</a>) (Milos Djermanovic)</li>
<li><a href="https://github.com/eslint/eslint/commit/a3c868f6ef103c1caff9d15f744f9ebd995e872f"><code>a3c868f</code></a> fix: update dependency <code>@​eslint/eslintrc</code> to ^3.3.4 (<a href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20554">#20554</a>) (Milos Djermanovic)</li>
<li><a href="https://github.com/eslint/eslint/commit/234d005da6cd3c924f359e3783fbf565a3c047c3"><code>234d005</code></a> fix: minimatch security vulnerability patch for v9.x (<a href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20549">#20549</a>) (Andrej Beles)</li>
<li><a href="https://github.com/eslint/eslint/commit/b1b37eecaa033d2e390e1d8f1d6e68d0f5ff3a6a"><code>b1b37ee</code></a> fix: update <code>ajv</code> to <code>6.14.0</code> to address security vulnerabilities (<a href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20538">#20538</a>) (루밀LuMir)</li>
</ul>
<h2>Documentation</h2>
<ul>
<li><a href="https://github.com/eslint/eslint/commit/46751526037682f8b42abcfb3e06d19213719347"><code>4675152</code></a> docs: add deprecation notice partial (<a href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20520">#20520</a>) (Milos Djermanovic)</li>
</ul>
<h2>Chores</h2>
<ul>
<li><a href="https://github.com/eslint/eslint/commit/b8b4eb15901c1bd6ef40d2589da4ae75795c0f6e"><code>b8b4eb1</code></a> chore: update dependencies for ESLint v9.39.4 (<a href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20596">#20596</a>) (Francesco Trotta)</li>
<li><a href="https://github.com/eslint/eslint/commit/71b2f6b628b76157b4a2a296cb969dc56abb296c"><code>71b2f6b</code></a> chore: package.json update for <code>@​eslint/js</code> release (Jenkins)</li>
<li><a href="https://github.com/eslint/eslint/commit/1d16c2fa3998440ae7b0f6e2612935bd6b0ded1d"><code>1d16c2f</code></a> ci: pin Node.js 25.6.1 (<a href="https://github.com/eslint/eslint/tree/HEAD/packages/js/issues/20563">#20563</a>) (Milos Djermanovic)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/eslint/eslint/commit/71b2f6b628b76157b4a2a296cb969dc56abb296c"><code>71b2f6b</code></a> chore: package.json update for <code>@​eslint/js</code> release</li>
<li>See full diff in <a href="https://github.com/eslint/eslint/commits/v9.39.4/packages/js">compare view</a></li>
</ul>
</details>
<br />

<details>
<summary>Most Recent Ignore Conditions Applied to This Pull Request</summary>

| Dependency Name | Ignore Conditions |
| --- | --- |
| @eslint/js | [>= 10.a, < 11] |
| lucide-react | [>= 1.a, < 2] |
</details>


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
- `@dependabot ignore <dependency name> major version` will close this group update PR and stop Dependabot creating any more for the specific dependency's major version (unless you unignore this specific dependency's major version or upgrade to it yourself)
- `@dependabot ignore <dependency name> minor version` will close this group update PR and stop Dependabot creating any more for the specific dependency's minor version (unless you unignore this specific dependency's minor version or upgrade to it yourself)
- `@dependabot ignore <dependency name>` will close this group update PR and stop Dependabot creating any more for the specific dependency (unless you unignore this specific dependency or upgrade to it yourself)
- `@dependabot unignore <dependency name>` will remove all of the ignore conditions of the specified dependency
- `@dependabot unignore <dependency name> <ignore condition>` will remove the ignore condition of the specified dependency and ignore conditions


</details>

---

## 77cb606

**作者**: dependabot[bot]
**日期**: 2026-04-22T10:01:55Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/77cb60676ab309d2821b5cdd73495016c1331fac](https://github.com/SerendipityOneInc/ecap-workspace/commit/77cb60676ab309d2821b5cdd73495016c1331fac)

### Commit Message
```
chore(deps): update cachetools requirement from >=5.0.0 to >=7.0.6 in /services/claw-interface (#1207)

Updates the requirements on
[cachetools](https://github.com/tkem/cachetools) to permit the latest
version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/tkem/cachetools/blob/master/CHANGELOG.rst">cachetools's
changelog</a>.</em></p>
<blockquote>
<h1>v7.0.6 (2026-04-20)</h1>
<ul>
<li>
<p>Minor code improvements.</p>
</li>
<li>
<p>Update project URLs.</p>
</li>
<li>
<p>Update CI environment.</p>
</li>
</ul>
<h1>v7.0.5 (2026-03-09)</h1>
<ul>
<li>Minor <code>@cachedmethod</code> performance improvements.</li>
</ul>
<h1>v7.0.4 (2026-03-08)</h1>
<ul>
<li>
<p>Fix and properly document <code>@cachedmethod.cache_key</code>
behavior.</p>
</li>
<li>
<p>Minor documentation improvements.</p>
</li>
</ul>
<h1>v7.0.3 (2026-03-05)</h1>
<ul>
<li>Fix <code>DeprecationWarning</code> when creating an autospec mock
with
<code>@cachedmethod</code> decorations.</li>
</ul>
<h1>v7.0.2 (2026-03-02)</h1>
<ul>
<li>Provide more efficient <code>clear()</code> implementation for all
support
Cache classes (courtesy Josep Pon Farreny).</li>
</ul>
<h1>v7.0.1 (2026-02-10)</h1>
<ul>
<li>
<p>Various test improvements.</p>
</li>
<li>
<p>Update Copilot Instructions.</p>
</li>
</ul>
<h1>v7.0.0 (2026-02-01)</h1>
<ul>
<li>Require Python 3.10 or later (breaking change).</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/tkem/cachetools/commit/28d4506f2a49d781ffbcecb095fa7aba5bb80aff"><code>28d4506</code></a>
Release v7.0.6.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/51921a4812b3304be9625ed004f024935a8036af"><code>51921a4</code></a>
Remove _TimedCache default timer to simplify type stubs.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/a4249f6aa3b4cb2fe287b08631c308bb88b9396c"><code>a4249f6</code></a>
Bump codecov/codecov-action from 5.5.2 to 6.0.0 (<a
href="https://redirect.github.com/tkem/cachetools/issues/392">#392</a>)</li>
<li><a
href="https://github.com/tkem/cachetools/commit/aa87283858f09b6820103373b7623d4ef51d233f"><code>aa87283</code></a>
feat: update project URLs in pyproject.toml to show on pypi.org (<a
href="https://redirect.github.com/tkem/cachetools/issues/390">#390</a>)</li>
<li><a
href="https://github.com/tkem/cachetools/commit/5dce86fc5c9c565c6e9c912e2be5d6abb9586a1d"><code>5dce86f</code></a>
Release v7.0.5.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/af5e68812b6fc5e432b5098711b5f4dcb5d20ccd"><code>af5e688</code></a>
Minor <a
href="https://github.com/cachedmethod"><code>@​cachedmethod</code></a>
performance improvements.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/0ca75e6049b63faa75c05b9929c83e3507be84a0"><code>0ca75e6</code></a>
Relase v7.0.4.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/5b1fa392d07a74774f9eb6796205777c81110f1c"><code>5b1fa39</code></a>
Prepare v7.0.4.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/18e5930ced2cf107c273b81d949dbab8ce3f48e1"><code>18e5930</code></a>
Fix <a
href="https://redirect.github.com/tkem/cachetools/issues/218">#218</a>:
Fix and properly document <a
href="https://github.com/cachedmethod"><code>@​cachedmethod</code></a>.cache_key
handling.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/98ec79ff8be24ce1346d6a96602f11ccbda4f76f"><code>98ec79f</code></a>
Drop &quot;class method&quot; from <a
href="https://github.com/cachedmethod"><code>@​cachedmethod</code></a>
docstring.</li>
<li>Additional commits viewable in <a
href="https://github.com/tkem/cachetools/compare/v5.0.0...v7.0.6">compare
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

### PR #1207: chore(deps): update cachetools requirement from >=5.0.0 to >=7.0.6 in /services/claw-interface

Updates the requirements on [cachetools](https://github.com/tkem/cachetools) to permit the latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/tkem/cachetools/blob/master/CHANGELOG.rst">cachetools's changelog</a>.</em></p>
<blockquote>
<h1>v7.0.6 (2026-04-20)</h1>
<ul>
<li>
<p>Minor code improvements.</p>
</li>
<li>
<p>Update project URLs.</p>
</li>
<li>
<p>Update CI environment.</p>
</li>
</ul>
<h1>v7.0.5 (2026-03-09)</h1>
<ul>
<li>Minor <code>@cachedmethod</code> performance improvements.</li>
</ul>
<h1>v7.0.4 (2026-03-08)</h1>
<ul>
<li>
<p>Fix and properly document <code>@cachedmethod.cache_key</code> behavior.</p>
</li>
<li>
<p>Minor documentation improvements.</p>
</li>
</ul>
<h1>v7.0.3 (2026-03-05)</h1>
<ul>
<li>Fix <code>DeprecationWarning</code> when creating an autospec mock with
<code>@cachedmethod</code> decorations.</li>
</ul>
<h1>v7.0.2 (2026-03-02)</h1>
<ul>
<li>Provide more efficient <code>clear()</code> implementation for all support
Cache classes (courtesy Josep Pon Farreny).</li>
</ul>
<h1>v7.0.1 (2026-02-10)</h1>
<ul>
<li>
<p>Various test improvements.</p>
</li>
<li>
<p>Update Copilot Instructions.</p>
</li>
</ul>
<h1>v7.0.0 (2026-02-01)</h1>
<ul>
<li>Require Python 3.10 or later (breaking change).</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/tkem/cachetools/commit/28d4506f2a49d781ffbcecb095fa7aba5bb80aff"><code>28d4506</code></a> Release v7.0.6.</li>
<li><a href="https://github.com/tkem/cachetools/commit/51921a4812b3304be9625ed004f024935a8036af"><code>51921a4</code></a> Remove _TimedCache default timer to simplify type stubs.</li>
<li><a href="https://github.com/tkem/cachetools/commit/a4249f6aa3b4cb2fe287b08631c308bb88b9396c"><code>a4249f6</code></a> Bump codecov/codecov-action from 5.5.2 to 6.0.0 (<a href="https://redirect.github.com/tkem/cachetools/issues/392">#392</a>)</li>
<li><a href="https://github.com/tkem/cachetools/commit/aa87283858f09b6820103373b7623d4ef51d233f"><code>aa87283</code></a> feat: update project URLs in pyproject.toml to show on pypi.org (<a href="https://redirect.github.com/tkem/cachetools/issues/390">#390</a>)</li>
<li><a href="https://github.com/tkem/cachetools/commit/5dce86fc5c9c565c6e9c912e2be5d6abb9586a1d"><code>5dce86f</code></a> Release v7.0.5.</li>
<li><a href="https://github.com/tkem/cachetools/commit/af5e68812b6fc5e432b5098711b5f4dcb5d20ccd"><code>af5e688</code></a> Minor <a href="https://github.com/cachedmethod"><code>@​cachedmethod</code></a> performance improvements.</li>
<li><a href="https://github.com/tkem/cachetools/commit/0ca75e6049b63faa75c05b9929c83e3507be84a0"><code>0ca75e6</code></a> Relase v7.0.4.</li>
<li><a href="https://github.com/tkem/cachetools/commit/5b1fa392d07a74774f9eb6796205777c81110f1c"><code>5b1fa39</code></a> Prepare v7.0.4.</li>
<li><a href="https://github.com/tkem/cachetools/commit/18e5930ced2cf107c273b81d949dbab8ce3f48e1"><code>18e5930</code></a> Fix <a href="https://redirect.github.com/tkem/cachetools/issues/218">#218</a>: Fix and properly document <a href="https://github.com/cachedmethod"><code>@​cachedmethod</code></a>.cache_key handling.</li>
<li><a href="https://github.com/tkem/cachetools/commit/98ec79ff8be24ce1346d6a96602f11ccbda4f76f"><code>98ec79f</code></a> Drop &quot;class method&quot; from <a href="https://github.com/cachedmethod"><code>@​cachedmethod</code></a> docstring.</li>
<li>Additional commits viewable in <a href="https://github.com/tkem/cachetools/compare/v5.0.0...v7.0.6">compare view</a></li>
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

---

## b03beca

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T09:59:22Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/b03beca2a6102b83e7c906ad8e348aa85f900f93](https://github.com/SerendipityOneInc/ecap-workspace/commit/b03beca2a6102b83e7c906ad8e348aa85f900f93)

### Commit Message
```
ci(dependabot): add cooldown to defer PRs until versions are mature (#1218)

## Summary
- Adds `cooldown` block to both `/web` (npm) and
`/services/claw-interface` (pip) ecosystems in `.github/dependabot.yml`:
- `default-days: 7` — aligns with pnpm's `minimumReleaseAge: 10080`
(7d), preventing dependabot from filing PRs that cannot generate a
lockfile under our install-time supply-chain gate.
  - `semver-major-days: 14` — extra soak for breaking bumps.
- Also ignores `@vitejs/plugin-react >=6.0.0` (ecosystem incompat —
requires vite@^8 which our vitest 4.x transitive pins to ^7; verified
locally).
- Root-cause fix for the current batch of broken dependabot PRs (now all
closed or fixed): #1208 fixed (lockfile regenerated), #1210 / #1211 /
#1212 / #1215 closed.

## Context
Recent offenders (as of 2026-04-22):
| PR | Package | Age / issue |
| --- | --- | --- |
| #1215 | marked 18.0.2 | 4 days — closed, cooldown will re-open |
| #1211 | wrangler 4.84.1 | 1 day + stale base — closed |
| #1210 | stripe 22.0.2 | 6 days — closed |
| #1212 | @vitejs/plugin-react 6.0.1 | peer incompat vs vite 7 — closed
+ ignored |
| #1208 | lucide-react + @eslint/js | transitive <7d — lockfile
regenerated manually |

`cooldown` lives at the PR-generation layer; `minimumReleaseAge` lives
at the install layer. Both now enforce the same 7-day floor, so
dependabot will stop producing DOA PRs in the common case. Transitive
<7d corner cases remain possible but shrink as the mature version wins
at PR time.

## Test plan
- [x] `python3 -c "import yaml;
yaml.safe_load(open('.github/dependabot.yml'))"` — YAML validates.
- [x] Local verification on #1212 branch confirmed the
`@vitejs/plugin-react@6` + `vite@7` `ERR_PACKAGE_PATH_NOT_EXPORTED`
incompatibility.
- [ ] GitHub validates the manifest on merge (surfaces as a check in PR
view).
- [ ] Observe next weekly dependabot cycle (Mondays) — only mature
versions open PRs; no @vitejs/plugin-react >=6 re-open.

Refs: feedback memory `dependabot_minimum_release_age` for the companion
manual fix template.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1218: ci(dependabot): add cooldown to defer PRs until versions are mature

## Summary
- Adds `cooldown` block to both `/web` (npm) and `/services/claw-interface` (pip) ecosystems in `.github/dependabot.yml`:
  - `default-days: 7` — aligns with pnpm's `minimumReleaseAge: 10080` (7d), preventing dependabot from filing PRs that cannot generate a lockfile under our install-time supply-chain gate.
  - `semver-major-days: 14` — extra soak for breaking bumps.
- Also ignores `@vitejs/plugin-react >=6.0.0` (ecosystem incompat — requires vite@^8 which our vitest 4.x transitive pins to ^7; verified locally).
- Root-cause fix for the current batch of broken dependabot PRs (now all closed or fixed): #1208 fixed (lockfile regenerated), #1210 / #1211 / #1212 / #1215 closed.

## Context
Recent offenders (as of 2026-04-22):
| PR | Package | Age / issue |
| --- | --- | --- |
| #1215 | marked 18.0.2 | 4 days — closed, cooldown will re-open |
| #1211 | wrangler 4.84.1 | 1 day + stale base — closed |
| #1210 | stripe 22.0.2 | 6 days — closed |
| #1212 | @vitejs/plugin-react 6.0.1 | peer incompat vs vite 7 — closed + ignored |
| #1208 | lucide-react + @eslint/js | transitive <7d — lockfile regenerated manually |

`cooldown` lives at the PR-generation layer; `minimumReleaseAge` lives at the install layer. Both now enforce the same 7-day floor, so dependabot will stop producing DOA PRs in the common case. Transitive <7d corner cases remain possible but shrink as the mature version wins at PR time.

## Test plan
- [x] `python3 -c "import yaml; yaml.safe_load(open('.github/dependabot.yml'))"` — YAML validates.
- [x] Local verification on #1212 branch confirmed the `@vitejs/plugin-react@6` + `vite@7` `ERR_PACKAGE_PATH_NOT_EXPORTED` incompatibility.
- [ ] GitHub validates the manifest on merge (surfaces as a check in PR view).
- [ ] Observe next weekly dependabot cycle (Mondays) — only mature versions open PRs; no @vitejs/plugin-react >=6 re-open.

Refs: feedback memory `dependabot_minimum_release_age` for the companion manual fix template.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T09:59:11Z): /lgtm

---

## 0cb9857

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T09:38:46Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/0cb98572abbcfa518a763f4e3c69f702ddef6b20](https://github.com/SerendipityOneInc/ecap-workspace/commit/0cb98572abbcfa518a763f4e3c69f702ddef6b20)

### Commit Message
```
docs: CLAUDE.md 加 3 条高价值规则(review judgment / CI ref / defineProperty leak) (#1217)

## Summary

按 memory \`feedback_claude_md_bar\` 的"不可由 1-2 文件 derive + 会复发"高门槛,从 59 条
memory 里筛出 3 条团队共享价值高的补充。

## 3 条改动

### 1. \`web/CLAUDE.md\` — 扩展 Global mutation 规则

原规则只点名 \`Object.assign(navigator/URL)\`,但
\`Object.defineProperty(window, 'location', ...)\` 走不同机制**一样会跨 worker
泄漏**(\`vi.unstubAllGlobals\` / \`restoreAllMocks\` 都不管)。本 session PR
#1202 review 里 \`NEED_HUMAN_REVIEW\` 正是撞这条——显式点出 \`defineProperty\`
避免下一个人同样踩坑。

### 2. \`CLAUDE.md\`(root) / CI Checks — \`refs/pull/N/merge\` 说明

"本地绿 CI 红"的高频根因:Actions 默认 checkout auto-merge preview,不是 PR HEAD,所以后入
main 的 PR 会跟你的 PR 语义冲突。这条是 GitHub 行为,不在仓库任何文件里写明。1 句话让人直接避开。

### 3. \`CLAUDE.md\`(root) / PR Workflow — Code review judgment 规则

本 session 被用户 2 次纠正(PR #1144 unmount race + PR #1150
\`vi.restoreAllMocks\`),高频判断型痛点。核心:\`non-blocking\` / \`nit\` 标签 ≠
skip,需要看实际代码判断;直接列出 worth-fixing / skip 信号。

## 筛选过程(跳过但考虑过的候选)

| 候选 | 判定 | 原因 |
|---|---|---|
| Merge queue 3 坑 | 跳过 | 太长 3 段;频率低保留 memory |
| Coverage ratchet \`floor(obs-1.5)\` | 跳过 | 已在 \`vitest.config.mts\`
注释,1 grep 可找 |
| jsdom Image/fake timer spec 模式 | 跳过 | 单 spec file 可见 |
| Profile orphan tabs 工程决策 | 跳过 | 历史清单不进 CLAUDE.md |

## Test plan

- [x] diff 可读性 review
- [ ] CI green(docs-only 不触发代码 pipeline)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1217: docs: CLAUDE.md 加 3 条高价值规则(review judgment / CI ref / defineProperty leak)

## Summary

按 memory \`feedback_claude_md_bar\` 的"不可由 1-2 文件 derive + 会复发"高门槛,从 59 条 memory 里筛出 3 条团队共享价值高的补充。

## 3 条改动

### 1. \`web/CLAUDE.md\` — 扩展 Global mutation 规则

原规则只点名 \`Object.assign(navigator/URL)\`,但 \`Object.defineProperty(window, 'location', ...)\` 走不同机制**一样会跨 worker 泄漏**(\`vi.unstubAllGlobals\` / \`restoreAllMocks\` 都不管)。本 session PR #1202 review 里 \`NEED_HUMAN_REVIEW\` 正是撞这条——显式点出 \`defineProperty\` 避免下一个人同样踩坑。

### 2. \`CLAUDE.md\`(root) / CI Checks — \`refs/pull/N/merge\` 说明

"本地绿 CI 红"的高频根因:Actions 默认 checkout auto-merge preview,不是 PR HEAD,所以后入 main 的 PR 会跟你的 PR 语义冲突。这条是 GitHub 行为,不在仓库任何文件里写明。1 句话让人直接避开。

### 3. \`CLAUDE.md\`(root) / PR Workflow — Code review judgment 规则

本 session 被用户 2 次纠正(PR #1144 unmount race + PR #1150 \`vi.restoreAllMocks\`),高频判断型痛点。核心:\`non-blocking\` / \`nit\` 标签 ≠ skip,需要看实际代码判断;直接列出 worth-fixing / skip 信号。

## 筛选过程(跳过但考虑过的候选)

| 候选 | 判定 | 原因 |
|---|---|---|
| Merge queue 3 坑 | 跳过 | 太长 3 段;频率低保留 memory |
| Coverage ratchet \`floor(obs-1.5)\` | 跳过 | 已在 \`vitest.config.mts\` 注释,1 grep 可找 |
| jsdom Image/fake timer spec 模式 | 跳过 | 单 spec file 可见 |
| Profile orphan tabs 工程决策 | 跳过 | 历史清单不进 CLAUDE.md |

## Test plan

- [x] diff 可读性 review
- [ ] CI green(docs-only 不触发代码 pipeline)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## cb275f7

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T09:21:49Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/cb275f73437e85fa5dfe9efc849894347a1c2186](https://github.com/SerendipityOneInc/ecap-workspace/commit/cb275f73437e85fa5dfe9efc849894347a1c2186)

### Commit Message
```
chore(web): ratchet coverage threshold 55 → 69 + 4 维度 (#894 Step 11 收尾) (#1216)

## Summary

Epic #894 Step 11 (#905) 最后一步:4 个 coverage PR(#1173 ModelSelector /
#1179 FeedbackDialog / #1198 ArchivedSessionPanel / #1202
GuideTourModal)合并后,以实测 \`observed - 1.5%\` 为各维度 threshold,从单维度 \`lines\`
扩到 4 维度。

## 实测数据(2026-04-22 origin/main)

| 维度 | observed | threshold | buffer |
|---|---|---|---|
| statements | 69.61% | 68 | 1.61% |
| branches | 63.10% | 61 | 2.10% |
| functions | 67.38% | 65 | 2.38% |
| lines | 71.45% | 69 | 2.45% |

## Ratchet 规则

**coverage(越高越好,阈值=下限): \`floor(observed - 1.5%)\`**

跟 duplication 规则 \`ceil(obs) + 1.5%\` 方向相反、意图相同——留微小波动 buffer。1.5%
足够吃住正常 flake,又不至于让静默 regression 溜过去。

## #905 原目标未达成

#905 建议 lines/statements 80, functions 75, branches 70。Step 11 四个
coverage PR 把 lines 从 ~56.5% 推到 71.45%(gain +15%),**离 80 目标还差 ~8-10
个百分点**。

本 PR **不激进追 80**,忠实 ratchet 到当前实测水位。继续往 80 推进的任务建议拆成后续 PR(挑选剩余
0%-coverage 的大文件补)——避免为了拿数字硬写测试反而影响代码质量。

## Test plan

- [x] \`pnpm test:unit:coverage\` 本地跑,thresholds 全通过(唯一 failing file 是
pre-existing AdminClient flake,跟 threshold 无关)
- [x] 新增 3 个维度 threshold 都贴近实测 (buffer 1.6-2.5%)
- [ ] CI green

## 关联

- Epic #894 / Step 11 (#905)
- 最近 merge 的 4 个 coverage PR: #1173 / #1179 / #1198 / #1202

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1216: chore(web): ratchet coverage threshold 55 → 69 + 4 维度 (#894 Step 11 收尾)

## Summary

Epic #894 Step 11 (#905) 最后一步:4 个 coverage PR(#1173 ModelSelector / #1179 FeedbackDialog / #1198 ArchivedSessionPanel / #1202 GuideTourModal)合并后,以实测 \`observed - 1.5%\` 为各维度 threshold,从单维度 \`lines\` 扩到 4 维度。

## 实测数据(2026-04-22 origin/main)

| 维度 | observed | threshold | buffer |
|---|---|---|---|
| statements | 69.61% | 68 | 1.61% |
| branches | 63.10% | 61 | 2.10% |
| functions | 67.38% | 65 | 2.38% |
| lines | 71.45% | 69 | 2.45% |

## Ratchet 规则

**coverage(越高越好,阈值=下限): \`floor(observed - 1.5%)\`**

跟 duplication 规则 \`ceil(obs) + 1.5%\` 方向相反、意图相同——留微小波动 buffer。1.5% 足够吃住正常 flake,又不至于让静默 regression 溜过去。

## #905 原目标未达成

#905 建议 lines/statements 80, functions 75, branches 70。Step 11 四个 coverage PR 把 lines 从 ~56.5% 推到 71.45%(gain +15%),**离 80 目标还差 ~8-10 个百分点**。

本 PR **不激进追 80**,忠实 ratchet 到当前实测水位。继续往 80 推进的任务建议拆成后续 PR(挑选剩余 0%-coverage 的大文件补)——避免为了拿数字硬写测试反而影响代码质量。

## Test plan

- [x] \`pnpm test:unit:coverage\` 本地跑,thresholds 全通过(唯一 failing file 是 pre-existing AdminClient flake,跟 threshold 无关)
- [x] 新增 3 个维度 threshold 都贴近实测 (buffer 1.6-2.5%)
- [ ] CI green

## 关联

- Epic #894 / Step 11 (#905)
- 最近 merge 的 4 个 coverage PR: #1173 / #1179 / #1198 / #1202

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T09:21:40Z): /lgtm

---

## f6c6241

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T09:09:05Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/f6c624164c2518a618bb58820668c8141a8ab35b](https://github.com/SerendipityOneInc/ecap-workspace/commit/f6c624164c2518a618bb58820668c8141a8ab35b)

### Commit Message
```
test(web): GuideTourModal 全面覆盖 (#894 Step 11 补) (#1202)

## Summary

Epic #894 Step 11 (#905) — \`GuideTourModal.tsx\` (418 LOC) 从 0% →
全分支,33 tests,**零源码改动**。

## 覆盖

| 组 | # | 覆盖 |
|---|---|---|
| useGuideTour hook | 7 | enabled=false/true × storage 组合 / 事件监听 /
unmount / dismiss 幂等 |
| GUIDE_TOUR_DISMISSED_EVENT | 1 | 稳定字符串契约 |
| Initial render | 4 | slide 文本 (双 layout) / 预加载 / opacity 转换 |
| Nav 箭头 + dots | 4 | next/prev/dot jump / 末 slide 隐藏 next |
| 手势 swipe (mobile) | 5 | 左/右 >50 / <50 阈值 / 首尾 clamp |
| Close 行为 | 4 | 桌面 X / 移动 X / backdrop / dispatched 事件 |
| CTA → window.open | 6 | hire/chat/schedule/create + locale 解析
(en/zh/fallback) |
| handleNext 末 slide | 1 | CTA 触发 onClose + markSeen |
| markSeen 幂等 | 1 | 双击 backdrop 只派发一次 |

## 技术要点

- **Stub global `Image` 构造器** 以按需触发 onload — jsdom 不真加载 img 资源,直接渲染会让
\`loadedImages\` 永远空集
- **window.location 重写** 测试 locale 路径解析(\`/en/...\` vs \`/zh/...\` vs
\`/\`)
- 双 layout(md:flex / md:hidden)同时渲染在 DOM 中,assertion 用
\`getAllByText().length === 2\`
- \`vi.spyOn(window, 'open')\` 遵循 web/CLAUDE.md 偏好

## Bug-hunt 发现

**图片加载失败 slide 永久卡死** → issue #1199

\`img\` 只挂 \`onload\` 无 \`onerror\`,一旦图片 404 对应 slide 永远 opacity
0,skeleton 持续 pulsing。典型 happy-path 完备但 error-path 裸奔的模式。

## Test plan

- [x] \`pnpm --filter web test:unit --
tests/unit/components/GuideTourModal.unit.spec.tsx\` (33/33 passed)
- [x] lint/prettier clean
- [ ] CI green

## 关联

- Epic #894 / Step 11 (#905)
- Follow-up bug: #1199
- **下一步:抬 vitest coverage threshold 35 → 80**(Step 11 最后一步)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1202: test(web): GuideTourModal 全面覆盖 (#894 Step 11 补)

## Summary

Epic #894 Step 11 (#905) — \`GuideTourModal.tsx\` (418 LOC) 从 0% → 全分支,33 tests,**零源码改动**。

## 覆盖

| 组 | # | 覆盖 |
|---|---|---|
| useGuideTour hook | 7 | enabled=false/true × storage 组合 / 事件监听 / unmount / dismiss 幂等 |
| GUIDE_TOUR_DISMISSED_EVENT | 1 | 稳定字符串契约 |
| Initial render | 4 | slide 文本 (双 layout) / 预加载 / opacity 转换 |
| Nav 箭头 + dots | 4 | next/prev/dot jump / 末 slide 隐藏 next |
| 手势 swipe (mobile) | 5 | 左/右 >50 / <50 阈值 / 首尾 clamp |
| Close 行为 | 4 | 桌面 X / 移动 X / backdrop / dispatched 事件 |
| CTA → window.open | 6 | hire/chat/schedule/create + locale 解析 (en/zh/fallback) |
| handleNext 末 slide | 1 | CTA 触发 onClose + markSeen |
| markSeen 幂等 | 1 | 双击 backdrop 只派发一次 |

## 技术要点

- **Stub global `Image` 构造器** 以按需触发 onload — jsdom 不真加载 img 资源,直接渲染会让 \`loadedImages\` 永远空集
- **window.location 重写** 测试 locale 路径解析(\`/en/...\` vs \`/zh/...\` vs \`/\`)
- 双 layout(md:flex / md:hidden)同时渲染在 DOM 中,assertion 用 \`getAllByText().length === 2\`
- \`vi.spyOn(window, 'open')\` 遵循 web/CLAUDE.md 偏好

## Bug-hunt 发现

**图片加载失败 slide 永久卡死** → issue #1199

\`img\` 只挂 \`onload\` 无 \`onerror\`,一旦图片 404 对应 slide 永远 opacity 0,skeleton 持续 pulsing。典型 happy-path 完备但 error-path 裸奔的模式。

## Test plan

- [x] \`pnpm --filter web test:unit -- tests/unit/components/GuideTourModal.unit.spec.tsx\` (33/33 passed)
- [x] lint/prettier clean
- [ ] CI green

## 关联

- Epic #894 / Step 11 (#905)
- Follow-up bug: #1199
- **下一步:抬 vitest coverage threshold 35 → 80**(Step 11 最后一步)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T09:08:53Z): /lgtm

---

## d1d160f

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T09:04:53Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/d1d160f7092ad3a908c3967d1f8be025e662040c](https://github.com/SerendipityOneInc/ecap-workspace/commit/d1d160f7092ad3a908c3967d1f8be025e662040c)

### Commit Message
```
ci(dependabot): also ignore redis until favie-common relaxes its 5.0.6 pin (#1206)

## Summary

Same pattern as #1196 (motor / pymongo / Pillow):

- \`favie-common\` v0.3.58 pins \`redis==5.0.6\`
- Dependabot #1201 (bump \`redis >=7.4.0\`) therefore fails with \`No
solution found\` in UV
- Add \`redis\` to the existing pip \`ignore:\` block until favie-common
relaxes the pin upstream

## Test plan

- [x] YAML syntax visual check
- [ ] After merge: close #1201 and confirm no new redis bump PR re-opens
next Dependabot run

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR #1206: ci(dependabot): also ignore redis until favie-common relaxes its 5.0.6 pin

## Summary

Same pattern as #1196 (motor / pymongo / Pillow):

- \`favie-common\` v0.3.58 pins \`redis==5.0.6\`
- Dependabot #1201 (bump \`redis >=7.4.0\`) therefore fails with \`No solution found\` in UV
- Add \`redis\` to the existing pip \`ignore:\` block until favie-common relaxes the pin upstream

## Test plan

- [x] YAML syntax visual check
- [ ] After merge: close #1201 and confirm no new redis bump PR re-opens next Dependabot run

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T09:04:39Z): /lgtm

---

## 9d4c81b

**作者**: dependabot[bot]
**日期**: 2026-04-22T09:01:29Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/9d4c81bf2bdc89deec2415c3abac74906c8947db](https://github.com/SerendipityOneInc/ecap-workspace/commit/9d4c81bf2bdc89deec2415c3abac74906c8947db)

### Commit Message
```
chore(deps-dev): bump eslint-plugin-simple-import-sort from 12.1.1 to 13.0.0 in /web (#1193)

Bumps
[eslint-plugin-simple-import-sort](https://github.com/lydell/eslint-plugin-simple-import-sort)
from 12.1.1 to 13.0.0.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/lydell/eslint-plugin-simple-import-sort/blob/main/CHANGELOG.md">eslint-plugin-simple-import-sort's
changelog</a>.</em></p>
<blockquote>
<h3>Version 13.0.0 (2026-04-06)</h3>
<p>This release puts imports from the same source, but with different
import styles, in a deterministic order.</p>
<pre lang="js"><code>// First namespace imports:
import * as Circle from &quot;circle;
// Then default imports:
import createCircle from &quot;circle&quot;;
// Then named imports:
import { radius } from &quot;circle&quot;;
</code></pre>
<p>That is especially useful if you need to have both a namespace import
<em>and</em> want to import a few things separately (since that cannot
be combined into a single import statement). With the above rule, the
imports end up in a deterministic order.</p>
<p>It’s only a breaking change if you import from the same source
multiple times in the same file (using different styles), and only in
the form that you need to autofix your files.</p>
<p>Thanks to Kannan Goundan (<a
href="https://github.com/cakoose"><code>@​cakoose</code></a>)!</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/90078e7fce900b6860ab7cd1800c6ff055601d88"><code>90078e7</code></a>
eslint-plugin-simple-import-sort v13.0.0</li>
<li><a
href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/7794d14a1871cda51f8379c5f3f65b902adf4cd4"><code>7794d14</code></a>
Determinstic ordering between different import styles (<a
href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/203">#203</a>)</li>
<li><a
href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/5ce648ae0be2d0c79062648e2f36c06a5c46bceb"><code>5ce648a</code></a>
Fix deprecation warning when running tests</li>
<li><a
href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/27c4d1af2abe47a0603c02164df0bc5d90dc835e"><code>27c4d1a</code></a>
Fix code coverage</li>
<li><a
href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/d994f4771f0f1b63a58059ee0c9376e286e64e1a"><code>d994f47</code></a>
Bump picomatch (<a
href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/208">#208</a>)</li>
<li><a
href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/b8f246db3d813437b1f66aaba73e7a08d6cdac58"><code>b8f246d</code></a>
Bump flatted from 3.2.9 to 3.4.2 (<a
href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/207">#207</a>)</li>
<li><a
href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/1c2d0e3add06f932a8d6a4e61759ccf2566613b8"><code>1c2d0e3</code></a>
Bump rollup from 4.50.1 to 4.59.0 (<a
href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/206">#206</a>)</li>
<li><a
href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/23dd72fe4118496372fb0ed6d8013af70e186bb2"><code>23dd72f</code></a>
Bump lodash from 4.17.21 to 4.17.23 (<a
href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/204">#204</a>)</li>
<li><a
href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/0f8dc7a7b96b44e4b9d10f89ea788a9ed22f02aa"><code>0f8dc7a</code></a>
Bump js-yaml from 4.1.0 to 4.1.1 (<a
href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/202">#202</a>)</li>
<li><a
href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/4584b9e860dd8f50bbb10d9423c2ecafbb4357f8"><code>4584b9e</code></a>
Bump vite from 7.1.5 to 7.1.11 (<a
href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/201">#201</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/lydell/eslint-plugin-simple-import-sort/compare/v12.1.1...v13.0.0">compare
view</a></li>
</ul>
</details>
<br />


[![Dependabot compatibility
score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=eslint-plugin-simple-import-sort&package-manager=npm_and_yarn&previous-version=12.1.1&new-version=13.0.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

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

---------

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
Co-authored-by: chris-srp <chrispenguin+dependabot@gmail.com>
```

### PR #1193: chore(deps-dev): bump eslint-plugin-simple-import-sort from 12.1.1 to 13.0.0 in /web

Bumps [eslint-plugin-simple-import-sort](https://github.com/lydell/eslint-plugin-simple-import-sort) from 12.1.1 to 13.0.0.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/lydell/eslint-plugin-simple-import-sort/blob/main/CHANGELOG.md">eslint-plugin-simple-import-sort's changelog</a>.</em></p>
<blockquote>
<h3>Version 13.0.0 (2026-04-06)</h3>
<p>This release puts imports from the same source, but with different import styles, in a deterministic order.</p>
<pre lang="js"><code>// First namespace imports:
import * as Circle from &quot;circle;
// Then default imports:
import createCircle from &quot;circle&quot;;
// Then named imports:
import { radius } from &quot;circle&quot;;
</code></pre>
<p>That is especially useful if you need to have both a namespace import <em>and</em> want to import a few things separately (since that cannot be combined into a single import statement). With the above rule, the imports end up in a deterministic order.</p>
<p>It’s only a breaking change if you import from the same source multiple times in the same file (using different styles), and only in the form that you need to autofix your files.</p>
<p>Thanks to Kannan Goundan (<a href="https://github.com/cakoose"><code>@​cakoose</code></a>)!</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/90078e7fce900b6860ab7cd1800c6ff055601d88"><code>90078e7</code></a> eslint-plugin-simple-import-sort v13.0.0</li>
<li><a href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/7794d14a1871cda51f8379c5f3f65b902adf4cd4"><code>7794d14</code></a> Determinstic ordering between different import styles (<a href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/203">#203</a>)</li>
<li><a href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/5ce648ae0be2d0c79062648e2f36c06a5c46bceb"><code>5ce648a</code></a> Fix deprecation warning when running tests</li>
<li><a href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/27c4d1af2abe47a0603c02164df0bc5d90dc835e"><code>27c4d1a</code></a> Fix code coverage</li>
<li><a href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/d994f4771f0f1b63a58059ee0c9376e286e64e1a"><code>d994f47</code></a> Bump picomatch (<a href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/208">#208</a>)</li>
<li><a href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/b8f246db3d813437b1f66aaba73e7a08d6cdac58"><code>b8f246d</code></a> Bump flatted from 3.2.9 to 3.4.2 (<a href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/207">#207</a>)</li>
<li><a href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/1c2d0e3add06f932a8d6a4e61759ccf2566613b8"><code>1c2d0e3</code></a> Bump rollup from 4.50.1 to 4.59.0 (<a href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/206">#206</a>)</li>
<li><a href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/23dd72fe4118496372fb0ed6d8013af70e186bb2"><code>23dd72f</code></a> Bump lodash from 4.17.21 to 4.17.23 (<a href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/204">#204</a>)</li>
<li><a href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/0f8dc7a7b96b44e4b9d10f89ea788a9ed22f02aa"><code>0f8dc7a</code></a> Bump js-yaml from 4.1.0 to 4.1.1 (<a href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/202">#202</a>)</li>
<li><a href="https://github.com/lydell/eslint-plugin-simple-import-sort/commit/4584b9e860dd8f50bbb10d9423c2ecafbb4357f8"><code>4584b9e</code></a> Bump vite from 7.1.5 to 7.1.11 (<a href="https://redirect.github.com/lydell/eslint-plugin-simple-import-sort/issues/201">#201</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/lydell/eslint-plugin-simple-import-sort/compare/v12.1.1...v13.0.0">compare view</a></li>
</ul>
</details>
<br />


[![Dependabot compatibility score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=eslint-plugin-simple-import-sort&package-manager=npm_and_yarn&previous-version=12.1.1&new-version=13.0.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

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

### Human Comments
- **chris-srp** (2026-04-22T08:29:51Z): @dependabot rebase

---

## c4ebd7c

**作者**: dependabot[bot]
**日期**: 2026-04-22T09:00:40Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/c4ebd7c0d3831f36e8f0f5e8abd4b2ec541308ae](https://github.com/SerendipityOneInc/ecap-workspace/commit/c4ebd7c0d3831f36e8f0f5e8abd4b2ec541308ae)

### Commit Message
```
chore(deps): bump the minor-and-patch group across 1 directory with 12 updates (#1189)

Bumps the minor-and-patch group with 12 updates in the /web directory:

| Package | From | To |
| --- | --- | --- |
|
[@opennextjs/cloudflare](https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare)
| `1.17.1` | `1.19.3` |
| [@sentry/cloudflare](https://github.com/getsentry/sentry-javascript) |
`10.41.0` | `10.49.0` |
| [@sentry/nextjs](https://github.com/getsentry/sentry-javascript) |
`10.41.0` | `10.49.0` |
|
[@tanstack/react-query](https://github.com/TanStack/query/tree/HEAD/packages/react-query)
| `5.96.2` | `5.99.2` |
| [dompurify](https://github.com/cure53/DOMPurify) | `3.3.1` | `3.4.1` |
|
[@tailwindcss/postcss](https://github.com/tailwindlabs/tailwindcss/tree/HEAD/packages/@tailwindcss-postcss)
| `4.2.1` | `4.2.4` |
|
[@vitest/coverage-v8](https://github.com/vitest-dev/vitest/tree/HEAD/packages/coverage-v8)
| `4.0.18` | `4.1.5` |
|
[@vitest/expect](https://github.com/vitest-dev/vitest/tree/HEAD/packages/expect)
| `4.0.18` | `4.1.5` |
| [firebase](https://github.com/firebase/firebase-js-sdk) | `12.8.0` |
`12.12.1` |
| [knip](https://github.com/webpro-nl/knip/tree/HEAD/packages/knip) |
`6.5.0` | `6.6.1` |
|
[tailwindcss](https://github.com/tailwindlabs/tailwindcss/tree/HEAD/packages/tailwindcss)
| `4.2.1` | `4.2.4` |
|
[vitest](https://github.com/vitest-dev/vitest/tree/HEAD/packages/vitest)
| `4.0.18` | `4.1.5` |


Updates `@opennextjs/cloudflare` from 1.17.1 to 1.19.3
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/opennextjs/opennextjs-cloudflare/releases"><code>@​opennextjs/cloudflare</code>'s
releases</a>.</em></p>
<blockquote>
<h2><code>@​opennextjs/cloudflare</code><a
href="https://github.com/1"><code>@​1</code></a>.19.3</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1215">#1215</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/608893e63e1ee16d07c7ec42da979657cf2a62bd"><code>608893e</code></a>
Thanks <a href="https://github.com/vicb"><code>@​vicb</code></a>! -
Factor large repeated values in manifests</p>
<p>This reduce the size of the generated code.</p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1218">#1218</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/f0d022685b24881a142bb01005ff78089be8c8d3"><code>f0d0226</code></a>
Thanks <a
href="https://github.com/314systems"><code>@​314systems</code></a>! -
remove <code>process.version</code> override</p>
<p>Remove process.version / process.versions.node overrides now that <a
href="https://redirect.github.com/unjs/unenv/pull/493">unjs/unenv#493</a>
is merged and shipped in <a
href="https://github.com/unjs/unenv/releases/tag/v2.0.0-rc.16">unenv@2.0.0-rc.16</a>
(project uses 2.0.0-rc.24)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1199">#1199</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/32594d6a921c5ebdbe25f38635bb2c9dabdcbff1"><code>32594d6</code></a>
Thanks <a href="https://github.com/SdSadat"><code>@​SdSadat</code></a>!
- fix(cli): fail fast in non-TTY environments instead of hanging on
config-creation prompts</p>
<p>When <code>open-next.config.ts</code> (or
<code>wrangler.(toml|json|jsonc)</code>) is missing, the CLI
prompts the user to auto-create it. In non-TTY environments (Cloudflare
Workers
Builds, Docker, CI) the Enquirer prompt can't read stdin, so the build
hangs or
fails with a truncated prompt and a cryptic exit code — the user sees
<code>? Missing required open-next.config.ts file, do you want to create
one? (Y/n)</code>
and then <code> ELIFECYCLE Command failed with exit code 13</code>, with
no hint at what
to do next.</p>
<p>Now, in non-interactive environments, both prompts throw an
actionable error
with the exact template to paste (for <code>open-next.config.ts</code>)
or point at the
existing <code>--skipWranglerConfigCheck</code> /
<code>SKIP_WRANGLER_CONFIG_CHECK</code> escape
hatch (for the wrangler config). Interactive behavior is unchanged.</p>
</li>
</ul>
<h2><code>@​opennextjs/cloudflare</code><a
href="https://github.com/1"><code>@​1</code></a>.19.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1207">#1207</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/0958726939d59e4a5c5a3062190278ffdfde38f5"><code>0958726</code></a>
Thanks <a
href="https://github.com/edmundhung"><code>@​edmundhung</code></a>! -
bump <code>@opennextjs/aws</code> to 3.10.2</p>
<p>See details at <a
href="https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2">https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2</a></p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1139">#1139</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/79b01b84fd92191517b7a11516c04208f9d474a6"><code>79b01b8</code></a>
Thanks <a
href="https://github.com/james-elicx"><code>@​james-elicx</code></a>! -
Fix Turbopack external module resolution by dynamically discovering
external imports at build time.</p>
<p>When packages are listed in <code>serverExternalPackages</code>,
Turbopack externalizes them via <code>externalImport()</code> which uses
dynamic <code>await import(id)</code>. The bundler (ESBuild) can't
statically analyze <code>import(id)</code> with a variable, so these
modules aren't included in the worker bundle.</p>
<p>This patch:</p>
<ul>
<li>Discovers hashed Turbopack external module mappings from
<code>.next/node_modules/</code> symlinks (e.g.
<code>shiki-43d062b67f27bbdc</code> → <code>shiki</code>)</li>
<li>Scans traced chunk files for bare external imports (e.g.
<code>externalImport(&quot;shiki&quot;)</code>) and subpath imports
(e.g. <code>shiki/engine/javascript</code>)</li>
<li>Generates explicit <code>switch/case</code> entries so the bundler
can statically resolve and include these modules</li>
</ul>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1203">#1203</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/6f02d12a75a78410711cc0d9db13ab0d41ed903a"><code>6f02d12</code></a>
Thanks <a
href="https://github.com/314systems"><code>@​314systems</code></a>! -
fix: exclude unsupported Next.js 16 releases from peer dependencies.</p>
<p>The previous range allowed Next.js 16.0.0 through 16.2.2 without a
peer dependency warning because <code>&gt;=16.2.3</code> was already
covered by <code>&gt;=15.5.15</code>.</p>
<p>The range now explicitly supports Next.js 15.5.15 and above in the
15.x line, and Next.js 16.2.3 and above in the 16.x line.</p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1200">#1200</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/7820ad0a0e5f57aba0580f3cabfdd0caa75cc9bb"><code>7820ad0</code></a>
Thanks <a
href="https://github.com/NathanDrake2406"><code>@​NathanDrake2406</code></a>!
- fix: reuse sharded tag data when filling the regional cache.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/opennextjs/opennextjs-cloudflare/blob/main/packages/cloudflare/CHANGELOG.md"><code>@​opennextjs/cloudflare</code>'s
changelog</a>.</em></p>
<blockquote>
<h2>1.19.3</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1215">#1215</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/608893e63e1ee16d07c7ec42da979657cf2a62bd"><code>608893e</code></a>
Thanks <a href="https://github.com/vicb"><code>@​vicb</code></a>! -
Factor large repeated values in manifests</p>
<p>This reduce the size of the generated code.</p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1218">#1218</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/f0d022685b24881a142bb01005ff78089be8c8d3"><code>f0d0226</code></a>
Thanks <a
href="https://github.com/314systems"><code>@​314systems</code></a>! -
remove <code>process.version</code> override</p>
<p>Remove process.version / process.versions.node overrides now that <a
href="https://redirect.github.com/unjs/unenv/pull/493">unjs/unenv#493</a>
is merged and shipped in <a
href="https://github.com/unjs/unenv/releases/tag/v2.0.0-rc.16">unenv@2.0.0-rc.16</a>
(project uses 2.0.0-rc.24)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1199">#1199</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/32594d6a921c5ebdbe25f38635bb2c9dabdcbff1"><code>32594d6</code></a>
Thanks <a href="https://github.com/SdSadat"><code>@​SdSadat</code></a>!
- fix(cli): fail fast in non-TTY environments instead of hanging on
config-creation prompts</p>
<p>When <code>open-next.config.ts</code> (or
<code>wrangler.(toml|json|jsonc)</code>) is missing, the CLI
prompts the user to auto-create it. In non-TTY environments (Cloudflare
Workers
Builds, Docker, CI) the Enquirer prompt can't read stdin, so the build
hangs or
fails with a truncated prompt and a cryptic exit code — the user sees
<code>? Missing required open-next.config.ts file, do you want to create
one? (Y/n)</code>
and then <code> ELIFECYCLE Command failed with exit code 13</code>, with
no hint at what
to do next.</p>
<p>Now, in non-interactive environments, both prompts throw an
actionable error
with the exact template to paste (for <code>open-next.config.ts</code>)
or point at the
existing <code>--skipWranglerConfigCheck</code> /
<code>SKIP_WRANGLER_CONFIG_CHECK</code> escape
hatch (for the wrangler config). Interactive behavior is unchanged.</p>
</li>
</ul>
<h2>1.19.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1207">#1207</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/0958726939d59e4a5c5a3062190278ffdfde38f5"><code>0958726</code></a>
Thanks <a
href="https://github.com/edmundhung"><code>@​edmundhung</code></a>! -
bump <code>@opennextjs/aws</code> to 3.10.2</p>
<p>See details at <a
href="https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2">https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2</a></p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1139">#1139</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/79b01b84fd92191517b7a11516c04208f9d474a6"><code>79b01b8</code></a>
Thanks <a
href="https://github.com/james-elicx"><code>@​james-elicx</code></a>! -
Fix Turbopack external module resolution by dynamically discovering
external imports at build time.</p>
<p>When packages are listed in <code>serverExternalPackages</code>,
Turbopack externalizes them via <code>externalImport()</code> which uses
dynamic <code>await import(id)</code>. The bundler (ESBuild) can't
statically analyze <code>import(id)</code> with a variable, so these
modules aren't included in the worker bundle.</p>
<p>This patch:</p>
<ul>
<li>Discovers hashed Turbopack external module mappings from
<code>.next/node_modules/</code> symlinks (e.g.
<code>shiki-43d062b67f27bbdc</code> → <code>shiki</code>)</li>
<li>Scans traced chunk files for bare external imports (e.g.
<code>externalImport(&quot;shiki&quot;)</code>) and subpath imports
(e.g. <code>shiki/engine/javascript</code>)</li>
<li>Generates explicit <code>switch/case</code> entries so the bundler
can statically resolve and include these modules</li>
</ul>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1203">#1203</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/6f02d12a75a78410711cc0d9db13ab0d41ed903a"><code>6f02d12</code></a>
Thanks <a
href="https://github.com/314systems"><code>@​314systems</code></a>! -
fix: exclude unsupported Next.js 16 releases from peer dependencies.</p>
<p>The previous range allowed Next.js 16.0.0 through 16.2.2 without a
peer dependency warning because <code>&gt;=16.2.3</code> was already
covered by <code>&gt;=15.5.15</code>.</p>
<p>The range now explicitly supports Next.js 15.5.15 and above in the
15.x line, and Next.js 16.2.3 and above in the 16.x line.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/d577521081365c6f9235d32959216f6db5e9268a"><code>d577521</code></a>
Version Packages (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1219">#1219</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/608893e63e1ee16d07c7ec42da979657cf2a62bd"><code>608893e</code></a>
Factor manifest code to reduce the bundle size (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1215">#1215</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/32594d6a921c5ebdbe25f38635bb2c9dabdcbff1"><code>32594d6</code></a>
fix(cli): fail fast in non-TTY environments instead of hanging on
config-crea...</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/f0d022685b24881a142bb01005ff78089be8c8d3"><code>f0d0226</code></a>
remove <code>process.version</code> override now that unenv#493 is
merged (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1218">#1218</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/ac28b08693dacd6c1e38d68863a91dc236cc9677"><code>ac28b08</code></a>
fix: typo (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1217">#1217</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/264d0a0c9cf80d3d8982e0a0a82f823ec2eb3ab5"><code>264d0a0</code></a>
Version Packages (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1201">#1201</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/0958726939d59e4a5c5a3062190278ffdfde38f5"><code>0958726</code></a>
chore: bump <code>@​opennextjs/aws</code> version (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1207">#1207</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/7820ad0a0e5f57aba0580f3cabfdd0caa75cc9bb"><code>7820ad0</code></a>
Reuse sharded tag data on regional cache fill (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1200">#1200</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/585795dbe20fe20d8662addbf9b7be64d82e3184"><code>585795d</code></a>
fix: regression where getEnvFromPlatformProxy received wrong options
type (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1">#1</a>...</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/6f02d12a75a78410711cc0d9db13ab0d41ed903a"><code>6f02d12</code></a>
fix: narrow peerDependencies next range to exclude 16.0.0–16.2.2 (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1203">#1203</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/opennextjs/opennextjs-cloudflare/commits/@opennextjs/cloudflare@1.19.3/packages/cloudflare">compare
view</a></li>
</ul>
</details>
<br />

Updates `@sentry/cloudflare` from 10.41.0 to 10.49.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/getsentry/sentry-javascript/releases"><code>@​sentry/cloudflare</code>'s
releases</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM
structure when an error occurs, providing a snapshot of the page state
for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link
them (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm
invocation, with proper linking between related alarms for better
observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with
<code>enableRpcTracePropagation</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic
trace propagation for Cloudflare RPC calls via <code>.fetch()</code>,
ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI
integrations (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain,
LangGraph) now support an <code>enableTruncation</code> option to
control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor
<code>AsyncLocalStorageContextManager</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally,
reducing external dependencies and ensuring consistent behavior across
environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for
<code>eventLoopBlockIntegration</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on
<code>gen_ai</code> spans (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6
operation name mapping (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from
<code>releaseLock()</code> in streaming (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents
(<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to
prevent memory leak (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/getsentry/sentry-javascript/blob/develop/CHANGELOG.md"><code>@​sentry/cloudflare</code>'s
changelog</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM
structure when an error occurs, providing a snapshot of the page state
for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link
them (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm
invocation, with proper linking between related alarms for better
observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with
<code>enableRpcTracePropagation</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic
trace propagation for Cloudflare RPC calls via <code>.fetch()</code>,
ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI
integrations (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain,
LangGraph) now support an <code>enableTruncation</code> option to
control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor
<code>AsyncLocalStorageContextManager</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally,
reducing external dependencies and ensuring consistent behavior across
environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for
<code>eventLoopBlockIntegration</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on
<code>gen_ai</code> spans (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6
operation name mapping (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from
<code>releaseLock()</code> in streaming (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents
(<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to
prevent memory leak (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/745af797c9e0d10d8b35725694862b1de6f064ae"><code>745af79</code></a>
release: 10.49.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/46dcef1590e8e3a677c74aceed9fa7641cc6e7c3"><code>46dcef1</code></a>
Merge pull request <a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20348">#20348</a>
from getsentry/prepare-release/10.49.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/bf4e188d1dde124677e933922949f0a626661d0a"><code>bf4e188</code></a>
meta(changelog): Update changelog for 10.49.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/5f72df55e5337fc1ba1a8bd70894b55b6a862bab"><code>5f72df5</code></a>
feat(cloudflare): Enable RPC trace propagation with
enableRpcTracePropagation...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/50438f9863e5cb5630459a6b1f967bbc15b0d188"><code>50438f9</code></a>
feat(browser): Emit web vitals as streamed spans (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/19827">#19827</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/3332fecd7aa53f6aca2ed42639f5a3ccc0e8fae5"><code>3332fec</code></a>
fix(opentelemetry): Use WeakRef for context stored on scope to prevent
memory...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/684a41fa4c7d5591be6a2fa7bff2db0ab5a62dbb"><code>684a41f</code></a>
ref(opentelemetry): Replace <code>@opentelemetry/resources</code> with
inline `getSentry...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/8b2a9dce02ee45f5ade7a23fd3ee0f4ae9d39d67"><code>8b2a9dc</code></a>
ci: Remove Docker container for Verdaccio package publishing (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20329">#20329</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/0007c7b81321b659d74641c5587e78f10755f714"><code>0007c7b</code></a>
ci: Extract test names for flaky test issues (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20298">#20298</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/9b9d65c8a4b7018dfc6bcdf0cfd43cb4d3ab2c75"><code>9b9d65c</code></a>
chore(ci): Bump actions/cache to v5 and actions/download-artifact to v7
(<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20249">#20249</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/getsentry/sentry-javascript/compare/10.41.0...10.49.0">compare
view</a></li>
</ul>
</details>
<br />

Updates `@sentry/nextjs` from 10.41.0 to 10.49.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/getsentry/sentry-javascript/releases"><code>@​sentry/nextjs</code>'s
releases</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM
structure when an error occurs, providing a snapshot of the page state
for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link
them (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm
invocation, with proper linking between related alarms for better
observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with
<code>enableRpcTracePropagation</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic
trace propagation for Cloudflare RPC calls via <code>.fetch()</code>,
ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI
integrations (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain,
LangGraph) now support an <code>enableTruncation</code> option to
control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor
<code>AsyncLocalStorageContextManager</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally,
reducing external dependencies and ensuring consistent behavior across
environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for
<code>eventLoopBlockIntegration</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on
<code>gen_ai</code> spans (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6
operation name mapping (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from
<code>releaseLock()</code> in streaming (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents
(<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to
prevent memory leak (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/getsentry/sentry-javascript/blob/develop/CHANGELOG.md"><code>@​sentry/nextjs</code>'s
changelog</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM
structure when an error occurs, providing a snapshot of the page state
for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link
them (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm
invocation, with proper linking between related alarms for better
observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with
<code>enableRpcTracePropagation</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic
trace propagation for Cloudflare RPC calls via <code>.fetch()</code>,
ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI
integrations (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain,
LangGraph) now support an <code>enableTruncation</code> option to
control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor
<code>AsyncLocalStorageContextManager</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally,
reducing external dependencies and ensuring consistent behavior across
environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for
<code>eventLoopBlockIntegration</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on
<code>gen_ai</code> spans (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6
operation name mapping (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from
<code>releaseLock()</code> in streaming (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents
(<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to
prevent memory leak (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/745af797c9e0d10d8b35725694862b1de6f064ae"><code>745af79</code></a>
release: 10.49.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/46dcef1590e8e3a677c74aceed9fa7641cc6e7c3"><code>46dcef1</code></a>
Merge pull request <a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20348">#20348</a>
from getsentry/prepare-release/10.49.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/bf4e188d1dde124677e933922949f0a626661d0a"><code>bf4e188</code></a>
meta(changelog): Update changelog for 10.49.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/5f72df55e5337fc1ba1a8bd70894b55b6a862bab"><code>5f72df5</code></a>
feat(cloudflare): Enable RPC trace propagation with
enableRpcTracePropagation...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/50438f9863e5cb5630459a6b1f967bbc15b0d188"><code>50438f9</code></a>
feat(browser): Emit web vitals as streamed spans (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/19827">#19827</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/3332fecd7aa53f6aca2ed42639f5a3ccc0e8fae5"><code>3332fec</code></a>
fix(opentelemetry): Use WeakRef for context stored on scope to prevent
memory...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/684a41fa4c7d5591be6a2fa7bff2db0ab5a62dbb"><code>684a41f</code></a>
ref(opentelemetry): Replace <code>@opentelemetry/resources</code> with
inline `getSentry...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/8b2a9dce02ee45f5ade7a23fd3ee0f4ae9d39d67"><code>8b2a9dc</code></a>
ci: Remove Docker container for Verdaccio package publishing (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20329">#20329</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/0007c7b81321b659d74641c5587e78f10755f714"><code>0007c7b</code></a>
ci: Extract test names for flaky test issues (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20298">#20298</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/9b9d65c8a4b7018dfc6bcdf0cfd43cb4d3ab2c75"><code>9b9d65c</code></a>
chore(ci): Bump actions/cache to v5 and actions/download-artifact to v7
(<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20249">#20249</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/getsentry/sentry-javascript/compare/10.41.0...10.49.0">compare
view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query` from 5.96.2 to 5.99.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/releases"><code>@​tanstack/react-query</code>'s
releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/blob/main/packages/react-query/CHANGELOG.md"><code>@​tanstack/react-query</code>'s
changelog</a>.</em></p>
<blockquote>
<h2>5.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2>5.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2>5.99.0</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.99.0</li>
</ul>
</li>
</ul>
<h2>5.98.0</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.98.0</li>
</ul>
</li>
</ul>
<h2>5.97.0</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a
href="https://github.com/TanStack/query/commit/2bfb12cc44f1d8495106136e4ddacb817135f8f9"><code>2bfb12c</code></a>]:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.97.0</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/TanStack/query/commit/a3ec7b30cc4c18b2c5aefe608638ecadce732b81"><code>a3ec7b3</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10520">#10520</a>)</li>
<li><a
href="https://github.com/TanStack/query/commit/69d2757c982f7bd5a483398492fe753f6f574ab8"><code>69d2757</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10514">#10514</a>)</li>
<li><a
href="https://github.com/TanStack/query/commit/7ffa1ed0b01d8c397c379dbb3d85da80b278b21c"><code>7ffa1ed</code></a>
test({react,preact,solid}-query/useQueries): fix test description from
'useQu...</li>
<li><a
href="https://github.com/TanStack/query/commit/bc83d370e8922f1c3126aea4e7757ce8761a06f2"><code>bc83d37</code></a>
test({react,preact}-query/useMutation): unify destructuring pattern in
comple...</li>
<li><a
href="https://github.com/TanStack/query/commit/aad1bd59d8e1ecebf14f556e0d9ca2605b4e4b80"><code>aad1bd5</code></a>
test({react,preact}-query/useMutation): add parallel 'mutateAsync' tests
with...</li>
<li><a
href="https://github.com/TanStack/query/commit/d7643b54fda462492d474695cd35e2549cefa5d7"><code>d7643b5</code></a>
test({react,preact}-query/useMutation): add optimistic update tests with
succ...</li>
<li><a
href="https://github.com/TanStack/query/commit/cd89d6f706bd143382db5ae3807ed8644ec52afe"><code>cd89d6f</code></a>
test({react,preact}-query/useMutation): add conditional handling and
retry te...</li>
<li><a
href="https://github.com/TanStack/query/commit/6e15fe62d2551b5269b21a1522f3c7bd653808ba"><code>6e15fe6</code></a>
test({react,preact}-query/useMutation): add chained 'mutateAsync' tests
for s...</li>
<li><a
href="https://github.com/TanStack/query/commit/792d3a5b32ee90b13f44456bb50518d24e9550d5"><code>792d3a5</code></a>
test({react,preact}-query/useMutation): add callback tests when
'useMutation'...</li>
<li><a
href="https://github.com/TanStack/query/commit/1b661b34ec5d1df00b4b0a2c084efbd486e73899"><code>1b661b3</code></a>
test({react,preact}-query/useMutation): add single callback tests for
'mutate...</li>
<li>Additional commits viewable in <a
href="https://github.com/TanStack/query/commits/@tanstack/react-query@5.99.2/packages/react-query">compare
view</a></li>
</ul>
</details>
<br />

Updates `dompurify` from 3.3.1 to 3.4.1
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/cure53/DOMPurify/releases">dompurify's
releases</a>.</em></p>
<blockquote>
<h2>DOMPurify 3.4.1</h2>
<ul>
<li>Fixed an issue with on-handler stripping for HTML-spec-reserved
custom element names (<code>font-face</code>,
<code>color-profile</code>, <code>missing-glyph</code>,
<code>font-face-src</code>, <code>font-face-uri</code>,
<code>font-face-format</code>, <code>font-face-name</code>) under
permissive <code>CUSTOM_ELEMENT_HANDLING</code></li>
<li>Fixed a case-sensitivity gap in the <code>annotation-xml</code>
check that allowed mixed-case variants to bypass the
basic-custom-element exclusion in XHTML mode</li>
<li>Fixed <code>SANITIZE_NAMED_PROPS</code> repeatedly prefixing
already-prefixed <code>id</code> and <code>name</code> values on
subsequent sanitization</li>
<li>Fixed the <code>IN_PLACE</code> root-node check to explicitly guard
against non-string <code>nodeName</code> (DOM-clobbering
robustness)</li>
<li>Removed a duplicate <code>slot</code> entry from the default HTML
attribute allow-list</li>
<li>Strengthened the fast-check fuzz harness with explicit XSS
invariants, an expanded seed-payload corpus, an additional idempotence
property for <code>SANITIZE_NAMED_PROPS</code>, and a negative-control
assertion ensuring the invariants actually fire</li>
<li>Added regression and pinning tests covering the above fixes and two
accepted-behavior contracts (<code>SAFE_FOR_TEMPLATES</code> greedy
scrub, hook-added attribute handling)</li>
<li>Extended CodeQL analysis to run on <code>3.x</code> and
<code>2.x</code> maintenance branches</li>
</ul>
<h2>DOMPurify 3.4.0</h2>
<p><strong>Most relevant changes:</strong></p>
<ul>
<li>Fixed a problem with <code>FORBID_TAGS</code> not winning over
<code>ADD_TAGS</code>, thanks <a
href="https://github.com/kodareef5"><code>@​kodareef5</code></a></li>
<li>Fixed several minor problems and typos regarding MathML attributes,
thanks <a
href="https://github.com/DavidOliver"><code>@​DavidOliver</code></a></li>
<li>Fixed <code>ADD_ATTR</code>/<code>ADD_TAGS</code> function leaking
into subsequent array-based calls, thanks <a
href="https://github.com/1Jesper1"><code>@​1Jesper1</code></a></li>
<li>Fixed a missing <code>SAFE_FOR_TEMPLATES</code> scrub in
<code>RETURN_DOM</code> path, thanks <a
href="https://github.com/bencalif"><code>@​bencalif</code></a></li>
<li>Fixed a prototype pollution via
<code>CUSTOM_ELEMENT_HANDLING</code>, thanks <a
href="https://github.com/trace37labs"><code>@​trace37labs</code></a></li>
<li>Fixed an issue with <code>ADD_TAGS</code> function form bypassing
<code>FORBID_TAGS</code>, thanks <a
href="https://github.com/eddieran"><code>@​eddieran</code></a></li>
<li>Fixed an issue with <code>ADD_ATTR</code> predicates skipping URI
validation, thanks <a
href="https://github.com/christos-eth"><code>@​christos-eth</code></a></li>
<li>Fixed an issue with <code>USE_PROFILES</code> prototype pollution,
thanks <a
href="https://github.com/christos-eth"><code>@​christos-eth</code></a></li>
<li>Fixed an issue leading to possible mXSS via Re-Contextualization,
thanks <a
href="https://github.com/researchatfluidattacks"><code>@​researchatfluidattacks</code></a>
and others</li>
<li>Fixed an issue with closing tags leading to possible mXSS, thanks <a
href="https://github.com/frevadiscor"><code>@​frevadiscor</code></a></li>
<li>Fixed a problem with the type dentition patcher after Node version
bump</li>
<li>Fixed freezing BS runs by reducing the tested browsers array</li>
<li>Bumped several dependencies where possible</li>
<li>Added needed files for OpenSSF scorecard checks</li>
</ul>
<p><strong>Published Advisories are here:</strong>
<a
href="https://github.com/cure53/DOMPurify/security/advisories?state=published">https://github.com/cure53/DOMPurify/security/advisories?state=published</a></p>
<h2>DOMPurify 3.3.3</h2>
<ul>
<li>Fixed an engine requirement for Node 20 which caused hiccups, thanks
<a href="https://github.com/Rotzbua"><code>@​Rotzbua</code></a></li>
</ul>
<h2>DOMPurify 3.3.2</h2>
<ul>
<li>Fixed a possible bypass caused by jsdom's faulty raw-text tag
parsing, thanks multiple reporters</li>
<li>Fixed a prototype pollution issue when working with custom elements,
thanks <a
href="https://github.com/christos-eth"><code>@​christos-eth</code></a></li>
<li>Fixed a lenient config parsing in <code>_isValidAttribute</code>,
thanks <a
href="https://github.com/christos-eth"><code>@​christos-eth</code></a></li>
<li>Bumped and removed several dependencies, thanks <a
href="https://github.com/Rotzbua"><code>@​Rotzbua</code></a></li>
<li>Fixed the test suite after bumping dependencies, thanks <a
href="https://github.com/Rotzbua"><code>@​Rotzbua</code></a></li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/cure53/DOMPurify/commit/5b0cdbbf52331e854c0a2de875b1a3790ecec2b8"><code>5b0cdbb</code></a>
chore: merge main into 3.x for 3.4.1 release (<a
href="https://redirect.github.com/cure53/DOMPurify/issues/1301">#1301</a>)</li>
<li><a
href="https://github.com/cure53/DOMPurify/commit/09f59115a311469de5b625225760593e551f080a"><code>09f5911</code></a>
test: added three more browsers to test setup (OSX, mobile)</li>
<li><a
href="https://github.com/cure53/DOMPurify/commit/5b16e0b892e82b1779d62b9928b43c4c4ff290b9"><code>5b16e0b</code></a>
Getting 3.x branch ready for 3.4.0 release (<a
href="https://redirect.github.com/cure53/DOMPurify/issues/1250">#1250</a>)</li>
<li><a
href="https://github.com/cure53/DOMPurify/commit/8bcbf73ae7eb56e7b4f1300b66cf543342c7ee27"><code>8bcbf73</code></a>
chore: Preparing 3.3.3 release</li>
<li><a
href="https://github.com/cure53/DOMPurify/commit/5faddd60af7b4d612f32a0c6b44432b77c8c490c"><code>5faddd6</code></a>
fix: engine requirement (<a
href="https://redirect.github.com/cure53/DOMPurify/issues/1210">#1210</a>)</li>
<li><a
href="https://github.com/cure53/DOMPurify/commit/0f91e3add5c028bc4110c513b0c2571b284c35af"><code>0f91e3a</code></a>
Update README.md</li>
<li><a
href="https://github.com/cure53/DOMPurify/commit/d5ff1a8c605df1df998c2e7df2c4c8ac762b0dea"><code>d5ff1a8</code></a>
Merge branch 'main' of github.com:cure53/DOMPurify</li>
<li><a
href="https://github.com/cure53/DOMPurify/commit/c3efd489010366e755de9d65fd741888fd8b7462"><code>c3efd48</code></a>
fix: moved back from jsdom 28 to jsdom 20</li>
<li><a
href="https://github.com/cure53/DOMPurify/commit/988b888108c8df911ef37e68d0e26c85ad90e885"><code>988b888</code></a>
fix: moved back from jsdom 28 to jsdom 20</li>
<li><a
href="https://github.com/cure53/DOMPurify/commit/2726c74e9c6a0645127d1630e5ca49f64bc9fe67"><code>2726c74</code></a>
chore: Preparing 3.3.2 release</li>
<li>Additional commits viewable in <a
href="https://github.com/cure53/DOMPurify/compare/3.3.1...3.4.1">compare
view</a></li>
</ul>
</details>
<details>
<summary>Install script changes</summary>
<p>This version adds <code>prepare</code> script that runs during
installation. Review the package contents before updating.</p>
</details>
<br />

Updates `@tailwindcss/postcss` from 4.2.1 to 4.2.4
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/tailwindlabs/tailwindcss/releases"><code>@​tailwindcss/postcss</code>'s
releases</a>.</em></p>
<blockquote>
<h2>v4.2.4</h2>
<h3>Fixed</h3>
<ul>
<li>Ensure imports in <code>@import</code> and <code>@plugin</code>
still resolve correctly when using Vite aliases in
<code>@tailwindcss/vite</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19947">#19947</a>)</li>
</ul>
<h2>v4.2.3</h2>
<h3>Fixed</h3>
<ul>
<li>Canonicalization: improve canonicalizations for
<code>tracking-*</code> utilities by preferring non-negative utilities
(e.g. <code>-tracking-tighter</code> → <code>tracking-wider</code>) (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19827">#19827</a>)</li>
<li>Fix crash due to invalid characters in candidate (exceeding valid
unicode code point range) (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19829">#19829</a>)</li>
<li>Ensure query params in imports are considered unique resources when
using <code>@tailwindcss/webpack</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19723">#19723</a>)</li>
<li>Canonicalization: collapse arbitrary values into shorthand utilities
(e.g. <code>px-[1.2rem] py-[1.2rem]</code> → <code>p-[1.2rem]</code>)
(<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19837">#19837</a>)</li>
<li>Canonicalization: collapse <code>border-{t,b}-*</code> into
<code>border-y-*</code>, <code>border-{l,r}-*</code> into
<code>border-x-*</code>, and <code>border-{t,r,b,l}-*</code> into
<code>border-*</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>scroll-m{t,b}-*</code> into
<code>scroll-my-*</code>, <code>scroll-m{l,r}-*</code> into
<code>scroll-mx-*</code>, and <code>scroll-m{t,r,b,l}-*</code> into
<code>scroll-m-*</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>scroll-p{t,b}-*</code> into
<code>scroll-py-*</code>, <code>scroll-p{l,r}-*</code> into
<code>scroll-px-*</code>, and <code>scroll-p{t,r,b,l}-*</code> into
<code>scroll-p-*</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>overflow-{x,y}-*</code> into
<code>overflow-*</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>overscroll-{x,y}-*</code> into
<code>overscroll-*</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Read from <code>--placeholder-color</code> instead of
<code>--background-color</code> for <code>placeholder-*</code> utilities
(<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19843">#19843</a>)</li>
<li>Upgrade: ensure files are not emptied out when killing the upgrade
process while it's running (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19846">#19846</a>)</li>
<li>Upgrade: use <code>config.content</code> when migrating from
Tailwind CSS v3 to Tailwind CSS v4 (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19846">#19846</a>)</li>
<li>Upgrade: never migrate files that are ignored by git (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19846">#19846</a>)</li>
<li>Add <code>.env</code> and <code>.env.*</code> to default ignored
content files (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19846">#19846</a>)</li>
<li>Canonicalization: migrate <code>overflow-ellipsis</code> into
<code>text-ellipsis</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19849">#19849</a>)</li>
<li>Canonicalization: migrate <code>start-full</code> →
<code>inset-s-full</code>, <code>start-auto</code> →
<code>inset-s-auto</code>, <code>start-px</code> →
<code>inset-s-px</code>, and <code>start-&lt;number&gt;</code> →
<code>inset-s-&lt;number&gt;</code> as well as negative versions (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19849">#19849</a>)</li>
<li>Canonicalization: migrate <code>end-full</code> →
<code>inset-e-full</code>, <code>end-auto</code> →
<code>inset-e-auto</code>, <code>end-px</code> →
<code>inset-e-px</code>, and <code>end-&lt;number&gt;</code> →
<code>inset-e-&lt;number&gt;</code> as well as negative versions (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19849">#19849</a>)</li>
<li>Canonicalization: move the <code>-</code> sign inside the arbitrary
value <code>-left-[9rem]</code> → <code>left-[-9rem]</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19858">#19858</a>)</li>
<li>Canonicalization: move the <code>-</code> sign outside the arbitrary
value <code>ml-[calc(-1*var(--width))]</code> →
<code>-ml-(--width)</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19858">#19858</a>)</li>
<li>Improve performance when scanning JSONL / NDJSON files (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19862">#19862</a>)</li>
<li>Support <code>NODE_PATH</code> environment variable in standalone
CLI (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19617">#19617</a>)</li>
</ul>
<h2>v4.2.2</h2>
<h3>Added</h3>
<ul>
<li>Support Vite 8 in <code>@tailwindcss/vite</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19790">#19790</a>)</li>
</ul>
<h3>Fixed</h3>
<ul>
<li>Don't crash when candidates contain prototype properties like
<code>row-constructor</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19725">#19725</a>)</li>
<li>Canonicalize <code>calc(var(--spacing)*…)</code> expressions into
<code>--spacing(…)</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19769">#19769</a>)</li>
<li>Fix crash in canonicalization step when handling utilities
containing <code>@property</code> at-rules (e.g. <code>shadow-sm
border</code>) (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19727">#19727</a>)</li>
<li>Skip full reload for server only modules scanned by client CSS when
using <code>@tailwindcss/vite</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19745">#19745</a>)</li>
<li>Improve canonicalization for bare values exceeding default spacing
scale suggestions (e.g. <code>w-1234 h-1234</code> →
<code>size-1234</code>) (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19809">#19809</a>)</li>
<li>Fix canonicalization resulting in empty list (e.g. <code>w-5 h-5
size-5</code> → <code>''</code> instead of <code>size-5</code>) (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19812">#19812</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/tailwindlabs/tailwindcss/blob/main/CHANGELOG.md"><code>@​tailwindcss/postcss</code>'s
changelog</a>.</em></p>
<blockquote>
<h2>[4.2.4] - 2026-04-21</h2>
<h3>Fixed</h3>
<ul>
<li>Ensure imports in <code>@import</code> and <code>@plugin</code>
still resolve correctly when using Vite aliases in
<code>@tailwindcss/vite</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19947">#19947</a>)</li>
</ul>
<h2>[4.2.3] - 2026-04-20</h2>
<h3>Fixed</h3>
<ul>
<li>Canonicalization: improve canonicalizations for
<code>tracking-*</code> utilities by preferring non-negative utilities
(e.g. <code>-tracking-tighter</code> → <code>tracking-wider</code>) (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19827">#19827</a>)</li>
<li>Fix crash due to invalid characters in candidate (exceeding valid
unicode code point range) (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19829">#19829</a>)</li>
<li>Ensure query params in imports are considered unique resources when
using <code>@tailwindcss/webpack</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19723">#19723</a>)</li>
<li>Canonicalization: collapse arbitrary values into shorthand utilities
(e.g. <code>px-[1.2rem] py-[1.2rem]</code> → <code>p-[1.2rem]</code>)
(<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19837">#19837</a>)</li>
<li>Canonicalization: collapse <code>border-{t,b}-*</code> into
<code>border-y-*</code>, <code>border-{l,r}-*</code> into
<code>border-x-*</code>, and <code>border-{t,r,b,l}-*</code> into
<code>border-*</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>scroll-m{t,b}-*</code> into
<code>scroll-my-*</code>, <code>scroll-m{l,r}-*</code> into
<code>scroll-mx-*</code>, and <code>scroll-m{t,r,b,l}-*</code> into
<code>scroll-m-*</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>scroll-p{t,b}-*</code> into
<code>scroll-py-*</code>, <code>scroll-p{l,r}-*</code> into
<code>scroll-px-*</code>, and <code>scroll-p{t,r,b,l}-*</code> into
<code>scroll-p-*</code> (<a
href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>overflow-{x,y}-*</code> into
<code>overflow-*</code> (<a
href="https://redirect.gi…
```

### PR #1189: chore(deps): bump the minor-and-patch group across 1 directory with 12 updates

Bumps the minor-and-patch group with 12 updates in the /web directory:

| Package | From | To |
| --- | --- | --- |
| [@opennextjs/cloudflare](https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare) | `1.17.1` | `1.19.3` |
| [@sentry/cloudflare](https://github.com/getsentry/sentry-javascript) | `10.41.0` | `10.49.0` |
| [@sentry/nextjs](https://github.com/getsentry/sentry-javascript) | `10.41.0` | `10.49.0` |
| [@tanstack/react-query](https://github.com/TanStack/query/tree/HEAD/packages/react-query) | `5.96.2` | `5.99.2` |
| [dompurify](https://github.com/cure53/DOMPurify) | `3.3.1` | `3.4.1` |
| [@tailwindcss/postcss](https://github.com/tailwindlabs/tailwindcss/tree/HEAD/packages/@tailwindcss-postcss) | `4.2.1` | `4.2.4` |
| [@vitest/coverage-v8](https://github.com/vitest-dev/vitest/tree/HEAD/packages/coverage-v8) | `4.0.18` | `4.1.5` |
| [@vitest/expect](https://github.com/vitest-dev/vitest/tree/HEAD/packages/expect) | `4.0.18` | `4.1.5` |
| [firebase](https://github.com/firebase/firebase-js-sdk) | `12.8.0` | `12.12.1` |
| [knip](https://github.com/webpro-nl/knip/tree/HEAD/packages/knip) | `6.5.0` | `6.6.1` |
| [tailwindcss](https://github.com/tailwindlabs/tailwindcss/tree/HEAD/packages/tailwindcss) | `4.2.1` | `4.2.4` |
| [vitest](https://github.com/vitest-dev/vitest/tree/HEAD/packages/vitest) | `4.0.18` | `4.1.5` |


Updates `@opennextjs/cloudflare` from 1.17.1 to 1.19.3
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/opennextjs/opennextjs-cloudflare/releases"><code>@​opennextjs/cloudflare</code>'s releases</a>.</em></p>
<blockquote>
<h2><code>@​opennextjs/cloudflare</code><a href="https://github.com/1"><code>@​1</code></a>.19.3</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1215">#1215</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/608893e63e1ee16d07c7ec42da979657cf2a62bd"><code>608893e</code></a> Thanks <a href="https://github.com/vicb"><code>@​vicb</code></a>! - Factor large repeated values in manifests</p>
<p>This reduce the size of the generated code.</p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1218">#1218</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/f0d022685b24881a142bb01005ff78089be8c8d3"><code>f0d0226</code></a> Thanks <a href="https://github.com/314systems"><code>@​314systems</code></a>! - remove <code>process.version</code> override</p>
<p>Remove process.version / process.versions.node overrides now that <a href="https://redirect.github.com/unjs/unenv/pull/493">unjs/unenv#493</a> is merged and shipped in <a href="https://github.com/unjs/unenv/releases/tag/v2.0.0-rc.16">unenv@2.0.0-rc.16</a> (project uses 2.0.0-rc.24)</p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1199">#1199</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/32594d6a921c5ebdbe25f38635bb2c9dabdcbff1"><code>32594d6</code></a> Thanks <a href="https://github.com/SdSadat"><code>@​SdSadat</code></a>! - fix(cli): fail fast in non-TTY environments instead of hanging on config-creation prompts</p>
<p>When <code>open-next.config.ts</code> (or <code>wrangler.(toml|json|jsonc)</code>) is missing, the CLI
prompts the user to auto-create it. In non-TTY environments (Cloudflare Workers
Builds, Docker, CI) the Enquirer prompt can't read stdin, so the build hangs or
fails with a truncated prompt and a cryptic exit code — the user sees
<code>? Missing required open-next.config.ts file, do you want to create one? (Y/n)</code>
and then <code> ELIFECYCLE  Command failed with exit code 13</code>, with no hint at what
to do next.</p>
<p>Now, in non-interactive environments, both prompts throw an actionable error
with the exact template to paste (for <code>open-next.config.ts</code>) or point at the
existing <code>--skipWranglerConfigCheck</code> / <code>SKIP_WRANGLER_CONFIG_CHECK</code> escape
hatch (for the wrangler config). Interactive behavior is unchanged.</p>
</li>
</ul>
<h2><code>@​opennextjs/cloudflare</code><a href="https://github.com/1"><code>@​1</code></a>.19.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1207">#1207</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/0958726939d59e4a5c5a3062190278ffdfde38f5"><code>0958726</code></a> Thanks <a href="https://github.com/edmundhung"><code>@​edmundhung</code></a>! - bump <code>@opennextjs/aws</code> to 3.10.2</p>
<p>See details at <a href="https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2">https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2</a></p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1139">#1139</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/79b01b84fd92191517b7a11516c04208f9d474a6"><code>79b01b8</code></a> Thanks <a href="https://github.com/james-elicx"><code>@​james-elicx</code></a>! - Fix Turbopack external module resolution by dynamically discovering external imports at build time.</p>
<p>When packages are listed in <code>serverExternalPackages</code>, Turbopack externalizes them via <code>externalImport()</code> which uses dynamic <code>await import(id)</code>. The bundler (ESBuild) can't statically analyze <code>import(id)</code> with a variable, so these modules aren't included in the worker bundle.</p>
<p>This patch:</p>
<ul>
<li>Discovers hashed Turbopack external module mappings from <code>.next/node_modules/</code> symlinks (e.g. <code>shiki-43d062b67f27bbdc</code> → <code>shiki</code>)</li>
<li>Scans traced chunk files for bare external imports (e.g. <code>externalImport(&quot;shiki&quot;)</code>) and subpath imports (e.g. <code>shiki/engine/javascript</code>)</li>
<li>Generates explicit <code>switch/case</code> entries so the bundler can statically resolve and include these modules</li>
</ul>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1203">#1203</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/6f02d12a75a78410711cc0d9db13ab0d41ed903a"><code>6f02d12</code></a> Thanks <a href="https://github.com/314systems"><code>@​314systems</code></a>! - fix: exclude unsupported Next.js 16 releases from peer dependencies.</p>
<p>The previous range allowed Next.js 16.0.0 through 16.2.2 without a peer dependency warning because <code>&gt;=16.2.3</code> was already covered by <code>&gt;=15.5.15</code>.</p>
<p>The range now explicitly supports Next.js 15.5.15 and above in the 15.x line, and Next.js 16.2.3 and above in the 16.x line.</p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1200">#1200</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/7820ad0a0e5f57aba0580f3cabfdd0caa75cc9bb"><code>7820ad0</code></a> Thanks <a href="https://github.com/NathanDrake2406"><code>@​NathanDrake2406</code></a>! - fix: reuse sharded tag data when filling the regional cache.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/opennextjs/opennextjs-cloudflare/blob/main/packages/cloudflare/CHANGELOG.md"><code>@​opennextjs/cloudflare</code>'s changelog</a>.</em></p>
<blockquote>
<h2>1.19.3</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1215">#1215</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/608893e63e1ee16d07c7ec42da979657cf2a62bd"><code>608893e</code></a> Thanks <a href="https://github.com/vicb"><code>@​vicb</code></a>! - Factor large repeated values in manifests</p>
<p>This reduce the size of the generated code.</p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1218">#1218</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/f0d022685b24881a142bb01005ff78089be8c8d3"><code>f0d0226</code></a> Thanks <a href="https://github.com/314systems"><code>@​314systems</code></a>! - remove <code>process.version</code> override</p>
<p>Remove process.version / process.versions.node overrides now that <a href="https://redirect.github.com/unjs/unenv/pull/493">unjs/unenv#493</a> is merged and shipped in <a href="https://github.com/unjs/unenv/releases/tag/v2.0.0-rc.16">unenv@2.0.0-rc.16</a> (project uses 2.0.0-rc.24)</p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1199">#1199</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/32594d6a921c5ebdbe25f38635bb2c9dabdcbff1"><code>32594d6</code></a> Thanks <a href="https://github.com/SdSadat"><code>@​SdSadat</code></a>! - fix(cli): fail fast in non-TTY environments instead of hanging on config-creation prompts</p>
<p>When <code>open-next.config.ts</code> (or <code>wrangler.(toml|json|jsonc)</code>) is missing, the CLI
prompts the user to auto-create it. In non-TTY environments (Cloudflare Workers
Builds, Docker, CI) the Enquirer prompt can't read stdin, so the build hangs or
fails with a truncated prompt and a cryptic exit code — the user sees
<code>? Missing required open-next.config.ts file, do you want to create one? (Y/n)</code>
and then <code> ELIFECYCLE  Command failed with exit code 13</code>, with no hint at what
to do next.</p>
<p>Now, in non-interactive environments, both prompts throw an actionable error
with the exact template to paste (for <code>open-next.config.ts</code>) or point at the
existing <code>--skipWranglerConfigCheck</code> / <code>SKIP_WRANGLER_CONFIG_CHECK</code> escape
hatch (for the wrangler config). Interactive behavior is unchanged.</p>
</li>
</ul>
<h2>1.19.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1207">#1207</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/0958726939d59e4a5c5a3062190278ffdfde38f5"><code>0958726</code></a> Thanks <a href="https://github.com/edmundhung"><code>@​edmundhung</code></a>! - bump <code>@opennextjs/aws</code> to 3.10.2</p>
<p>See details at <a href="https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2">https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2</a></p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1139">#1139</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/79b01b84fd92191517b7a11516c04208f9d474a6"><code>79b01b8</code></a> Thanks <a href="https://github.com/james-elicx"><code>@​james-elicx</code></a>! - Fix Turbopack external module resolution by dynamically discovering external imports at build time.</p>
<p>When packages are listed in <code>serverExternalPackages</code>, Turbopack externalizes them via <code>externalImport()</code> which uses dynamic <code>await import(id)</code>. The bundler (ESBuild) can't statically analyze <code>import(id)</code> with a variable, so these modules aren't included in the worker bundle.</p>
<p>This patch:</p>
<ul>
<li>Discovers hashed Turbopack external module mappings from <code>.next/node_modules/</code> symlinks (e.g. <code>shiki-43d062b67f27bbdc</code> → <code>shiki</code>)</li>
<li>Scans traced chunk files for bare external imports (e.g. <code>externalImport(&quot;shiki&quot;)</code>) and subpath imports (e.g. <code>shiki/engine/javascript</code>)</li>
<li>Generates explicit <code>switch/case</code> entries so the bundler can statically resolve and include these modules</li>
</ul>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1203">#1203</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/6f02d12a75a78410711cc0d9db13ab0d41ed903a"><code>6f02d12</code></a> Thanks <a href="https://github.com/314systems"><code>@​314systems</code></a>! - fix: exclude unsupported Next.js 16 releases from peer dependencies.</p>
<p>The previous range allowed Next.js 16.0.0 through 16.2.2 without a peer dependency warning because <code>&gt;=16.2.3</code> was already covered by <code>&gt;=15.5.15</code>.</p>
<p>The range now explicitly supports Next.js 15.5.15 and above in the 15.x line, and Next.js 16.2.3 and above in the 16.x line.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/d577521081365c6f9235d32959216f6db5e9268a"><code>d577521</code></a> Version Packages (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1219">#1219</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/608893e63e1ee16d07c7ec42da979657cf2a62bd"><code>608893e</code></a> Factor manifest code to reduce the bundle size (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1215">#1215</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/32594d6a921c5ebdbe25f38635bb2c9dabdcbff1"><code>32594d6</code></a> fix(cli): fail fast in non-TTY environments instead of hanging on config-crea...</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/f0d022685b24881a142bb01005ff78089be8c8d3"><code>f0d0226</code></a> remove <code>process.version</code> override now that unenv#493 is merged (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1218">#1218</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/ac28b08693dacd6c1e38d68863a91dc236cc9677"><code>ac28b08</code></a> fix: typo (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1217">#1217</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/264d0a0c9cf80d3d8982e0a0a82f823ec2eb3ab5"><code>264d0a0</code></a> Version Packages (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1201">#1201</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/0958726939d59e4a5c5a3062190278ffdfde38f5"><code>0958726</code></a> chore: bump <code>@​opennextjs/aws</code> version (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1207">#1207</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/7820ad0a0e5f57aba0580f3cabfdd0caa75cc9bb"><code>7820ad0</code></a> Reuse sharded tag data on regional cache fill (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1200">#1200</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/585795dbe20fe20d8662addbf9b7be64d82e3184"><code>585795d</code></a> fix: regression where getEnvFromPlatformProxy received wrong options type (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1">#1</a>...</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/6f02d12a75a78410711cc0d9db13ab0d41ed903a"><code>6f02d12</code></a> fix: narrow peerDependencies next range to exclude 16.0.0–16.2.2 (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1203">#1203</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/opennextjs/opennextjs-cloudflare/commits/@opennextjs/cloudflare@1.19.3/packages/cloudflare">compare view</a></li>
</ul>
</details>
<br />

Updates `@sentry/cloudflare` from 10.41.0 to 10.49.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/getsentry/sentry-javascript/releases"><code>@​sentry/cloudflare</code>'s releases</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM structure when an error occurs, providing a snapshot of the page state for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link them (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm invocation, with proper linking between related alarms for better observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with <code>enableRpcTracePropagation</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic trace propagation for Cloudflare RPC calls via <code>.fetch()</code>, ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI integrations (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain, LangGraph) now support an <code>enableTruncation</code> option to control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor <code>AsyncLocalStorageContextManager</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally, reducing external dependencies and ensuring consistent behavior across environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for <code>eventLoopBlockIntegration</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on <code>gen_ai</code> spans (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6 operation name mapping (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from <code>releaseLock()</code> in streaming (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to prevent memory leak (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/getsentry/sentry-javascript/blob/develop/CHANGELOG.md"><code>@​sentry/cloudflare</code>'s changelog</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM structure when an error occurs, providing a snapshot of the page state for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link them (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm invocation, with proper linking between related alarms for better observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with <code>enableRpcTracePropagation</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic trace propagation for Cloudflare RPC calls via <code>.fetch()</code>, ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI integrations (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain, LangGraph) now support an <code>enableTruncation</code> option to control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor <code>AsyncLocalStorageContextManager</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally, reducing external dependencies and ensuring consistent behavior across environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for <code>eventLoopBlockIntegration</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on <code>gen_ai</code> spans (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6 operation name mapping (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from <code>releaseLock()</code> in streaming (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to prevent memory leak (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/745af797c9e0d10d8b35725694862b1de6f064ae"><code>745af79</code></a> release: 10.49.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/46dcef1590e8e3a677c74aceed9fa7641cc6e7c3"><code>46dcef1</code></a> Merge pull request <a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20348">#20348</a> from getsentry/prepare-release/10.49.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/bf4e188d1dde124677e933922949f0a626661d0a"><code>bf4e188</code></a> meta(changelog): Update changelog for 10.49.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/5f72df55e5337fc1ba1a8bd70894b55b6a862bab"><code>5f72df5</code></a> feat(cloudflare): Enable RPC trace propagation with enableRpcTracePropagation...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/50438f9863e5cb5630459a6b1f967bbc15b0d188"><code>50438f9</code></a> feat(browser): Emit web vitals as streamed spans (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/19827">#19827</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/3332fecd7aa53f6aca2ed42639f5a3ccc0e8fae5"><code>3332fec</code></a> fix(opentelemetry): Use WeakRef for context stored on scope to prevent memory...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/684a41fa4c7d5591be6a2fa7bff2db0ab5a62dbb"><code>684a41f</code></a> ref(opentelemetry): Replace <code>@opentelemetry/resources</code> with inline `getSentry...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/8b2a9dce02ee45f5ade7a23fd3ee0f4ae9d39d67"><code>8b2a9dc</code></a> ci: Remove Docker container for Verdaccio package publishing (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20329">#20329</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/0007c7b81321b659d74641c5587e78f10755f714"><code>0007c7b</code></a> ci: Extract test names for flaky test issues (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20298">#20298</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/9b9d65c8a4b7018dfc6bcdf0cfd43cb4d3ab2c75"><code>9b9d65c</code></a> chore(ci): Bump actions/cache to v5 and actions/download-artifact to v7 (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20249">#20249</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/getsentry/sentry-javascript/compare/10.41.0...10.49.0">compare view</a></li>
</ul>
</details>
<br />

Updates `@sentry/nextjs` from 10.41.0 to 10.49.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/getsentry/sentry-javascript/releases"><code>@​sentry/nextjs</code>'s releases</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM structure when an error occurs, providing a snapshot of the page state for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link them (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm invocation, with proper linking between related alarms for better observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with <code>enableRpcTracePropagation</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic trace propagation for Cloudflare RPC calls via <code>.fetch()</code>, ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI integrations (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain, LangGraph) now support an <code>enableTruncation</code> option to control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor <code>AsyncLocalStorageContextManager</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally, reducing external dependencies and ensuring consistent behavior across environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for <code>eventLoopBlockIntegration</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on <code>gen_ai</code> spans (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6 operation name mapping (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from <code>releaseLock()</code> in streaming (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to prevent memory leak (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/getsentry/sentry-javascript/blob/develop/CHANGELOG.md"><code>@​sentry/nextjs</code>'s changelog</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM structure when an error occurs, providing a snapshot of the page state for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link them (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm invocation, with proper linking between related alarms for better observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with <code>enableRpcTracePropagation</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic trace propagation for Cloudflare RPC calls via <code>.fetch()</code>, ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI integrations (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain, LangGraph) now support an <code>enableTruncation</code> option to control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor <code>AsyncLocalStorageContextManager</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally, reducing external dependencies and ensuring consistent behavior across environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for <code>eventLoopBlockIntegration</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on <code>gen_ai</code> spans (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6 operation name mapping (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from <code>releaseLock()</code> in streaming (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to prevent memory leak (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/745af797c9e0d10d8b35725694862b1de6f064ae"><code>745af79</code></a> release: 10.49.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/46dcef1590e8e3a677c74aceed9fa7641cc6e7c3"><code>46dcef1</code></a> Merge pull request <a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20348">#20348</a> from getsentry/prepare-release/10.49.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/bf4e188d1dde124677e933922949f0a626661d0a"><code>bf4e188</code></a> meta(changelog): Update changelog for 10.49.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/5f72df55e5337fc1ba1a8bd70894b55b6a862bab"><code>5f72df5</code></a> feat(cloudflare): Enable RPC trace propagation with enableRpcTracePropagation...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/50438f9863e5cb5630459a6b1f967bbc15b0d188"><code>50438f9</code></a> feat(browser): Emit web vitals as streamed spans (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/19827">#19827</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/3332fecd7aa53f6aca2ed42639f5a3ccc0e8fae5"><code>3332fec</code></a> fix(opentelemetry): Use WeakRef for context stored on scope to prevent memory...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/684a41fa4c7d5591be6a2fa7bff2db0ab5a62dbb"><code>684a41f</code></a> ref(opentelemetry): Replace <code>@opentelemetry/resources</code> with inline `getSentry...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/8b2a9dce02ee45f5ade7a23fd3ee0f4ae9d39d67"><code>8b2a9dc</code></a> ci: Remove Docker container for Verdaccio package publishing (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20329">#20329</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/0007c7b81321b659d74641c5587e78f10755f714"><code>0007c7b</code></a> ci: Extract test names for flaky test issues (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20298">#20298</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/9b9d65c8a4b7018dfc6bcdf0cfd43cb4d3ab2c75"><code>9b9d65c</code></a> chore(ci): Bump actions/cache to v5 and actions/download-artifact to v7 (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20249">#20249</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/getsentry/sentry-javascript/compare/10.41.0...10.49.0">compare view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query` from 5.96.2 to 5.99.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/releases"><code>@​tanstack/react-query</code>'s releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/blob/main/packages/react-query/CHANGELOG.md"><code>@​tanstack/react-query</code>'s changelog</a>.</em></p>
<blockquote>
<h2>5.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2>5.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2>5.99.0</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.99.0</li>
</ul>
</li>
</ul>
<h2>5.98.0</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.98.0</li>
</ul>
</li>
</ul>
<h2>5.97.0</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a href="https://github.com/TanStack/query/commit/2bfb12cc44f1d8495106136e4ddacb817135f8f9"><code>2bfb12c</code></a>]:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.97.0</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/TanStack/query/commit/a3ec7b30cc4c18b2c5aefe608638ecadce732b81"><code>a3ec7b3</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10520">#10520</a>)</li>
<li><a href="https://github.com/TanStack/query/commit/69d2757c982f7bd5a483398492fe753f6f574ab8"><code>69d2757</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10514">#10514</a>)</li>
<li><a href="https://github.com/TanStack/query/commit/7ffa1ed0b01d8c397c379dbb3d85da80b278b21c"><code>7ffa1ed</code></a> test({react,preact,solid}-query/useQueries): fix test description from 'useQu...</li>
<li><a href="https://github.com/TanStack/query/commit/bc83d370e8922f1c3126aea4e7757ce8761a06f2"><code>bc83d37</code></a> test({react,preact}-query/useMutation): unify destructuring pattern in comple...</li>
<li><a href="https://github.com/TanStack/query/commit/aad1bd59d8e1ecebf14f556e0d9ca2605b4e4b80"><code>aad1bd5</code></a> test({react,preact}-query/useMutation): add parallel 'mutateAsync' tests with...</li>
<li><a href="https://github.com/TanStack/query/commit/d7643b54fda462492d474695cd35e2549cefa5d7"><code>d7643b5</code></a> test({react,preact}-query/useMutation): add optimistic update tests with succ...</li>
<li><a href="https://github.com/TanStack/query/commit/cd89d6f706bd143382db5ae3807ed8644ec52afe"><code>cd89d6f</code></a> test({react,preact}-query/useMutation): add conditional handling and retry te...</li>
<li><a href="https://github.com/TanStack/query/commit/6e15fe62d2551b5269b21a1522f3c7bd653808ba"><code>6e15fe6</code></a> test({react,preact}-query/useMutation): add chained 'mutateAsync' tests for s...</li>
<li><a href="https://github.com/TanStack/query/commit/792d3a5b32ee90b13f44456bb50518d24e9550d5"><code>792d3a5</code></a> test({react,preact}-query/useMutation): add callback tests when 'useMutation'...</li>
<li><a href="https://github.com/TanStack/query/commit/1b661b34ec5d1df00b4b0a2c084efbd486e73899"><code>1b661b3</code></a> test({react,preact}-query/useMutation): add single callback tests for 'mutate...</li>
<li>Additional commits viewable in <a href="https://github.com/TanStack/query/commits/@tanstack/react-query@5.99.2/packages/react-query">compare view</a></li>
</ul>
</details>
<br />

Updates `dompurify` from 3.3.1 to 3.4.1
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/cure53/DOMPurify/releases">dompurify's releases</a>.</em></p>
<blockquote>
<h2>DOMPurify 3.4.1</h2>
<ul>
<li>Fixed an issue with on-handler stripping for HTML-spec-reserved custom element names (<code>font-face</code>, <code>color-profile</code>, <code>missing-glyph</code>, <code>font-face-src</code>, <code>font-face-uri</code>, <code>font-face-format</code>, <code>font-face-name</code>) under permissive <code>CUSTOM_ELEMENT_HANDLING</code></li>
<li>Fixed a case-sensitivity gap in the <code>annotation-xml</code> check that allowed mixed-case variants to bypass the basic-custom-element exclusion in XHTML mode</li>
<li>Fixed <code>SANITIZE_NAMED_PROPS</code> repeatedly prefixing already-prefixed <code>id</code> and <code>name</code> values on subsequent sanitization</li>
<li>Fixed the <code>IN_PLACE</code> root-node check to explicitly guard against non-string <code>nodeName</code> (DOM-clobbering robustness)</li>
<li>Removed a duplicate <code>slot</code> entry from the default HTML attribute allow-list</li>
<li>Strengthened the fast-check fuzz harness with explicit XSS invariants, an expanded seed-payload corpus, an additional idempotence property for <code>SANITIZE_NAMED_PROPS</code>, and a negative-control assertion ensuring the invariants actually fire</li>
<li>Added regression and pinning tests covering the above fixes and two accepted-behavior contracts (<code>SAFE_FOR_TEMPLATES</code> greedy scrub, hook-added attribute handling)</li>
<li>Extended CodeQL analysis to run on <code>3.x</code> and <code>2.x</code> maintenance branches</li>
</ul>
<h2>DOMPurify 3.4.0</h2>
<p><strong>Most relevant changes:</strong></p>
<ul>
<li>Fixed a problem with <code>FORBID_TAGS</code> not winning over <code>ADD_TAGS</code>, thanks <a href="https://github.com/kodareef5"><code>@​kodareef5</code></a></li>
<li>Fixed several minor problems and typos regarding MathML attributes, thanks <a href="https://github.com/DavidOliver"><code>@​DavidOliver</code></a></li>
<li>Fixed <code>ADD_ATTR</code>/<code>ADD_TAGS</code> function leaking into subsequent array-based calls, thanks <a href="https://github.com/1Jesper1"><code>@​1Jesper1</code></a></li>
<li>Fixed a missing <code>SAFE_FOR_TEMPLATES</code> scrub in <code>RETURN_DOM</code> path, thanks <a href="https://github.com/bencalif"><code>@​bencalif</code></a></li>
<li>Fixed a prototype pollution via <code>CUSTOM_ELEMENT_HANDLING</code>, thanks <a href="https://github.com/trace37labs"><code>@​trace37labs</code></a></li>
<li>Fixed an issue with <code>ADD_TAGS</code> function form bypassing <code>FORBID_TAGS</code>, thanks <a href="https://github.com/eddieran"><code>@​eddieran</code></a></li>
<li>Fixed an issue with <code>ADD_ATTR</code> predicates skipping URI validation, thanks <a href="https://github.com/christos-eth"><code>@​christos-eth</code></a></li>
<li>Fixed an issue with <code>USE_PROFILES</code> prototype pollution, thanks <a href="https://github.com/christos-eth"><code>@​christos-eth</code></a></li>
<li>Fixed an issue leading to possible mXSS via Re-Contextualization, thanks <a href="https://github.com/researchatfluidattacks"><code>@​researchatfluidattacks</code></a> and others</li>
<li>Fixed an issue with closing tags leading to possible mXSS, thanks <a href="https://github.com/frevadiscor"><code>@​frevadiscor</code></a></li>
<li>Fixed a problem with the type dentition patcher after Node version bump</li>
<li>Fixed freezing BS runs by reducing the tested browsers array</li>
<li>Bumped several dependencies where possible</li>
<li>Added needed files for OpenSSF scorecard checks</li>
</ul>
<p><strong>Published Advisories are here:</strong>
<a href="https://github.com/cure53/DOMPurify/security/advisories?state=published">https://github.com/cure53/DOMPurify/security/advisories?state=published</a></p>
<h2>DOMPurify 3.3.3</h2>
<ul>
<li>Fixed an engine requirement for Node 20 which caused hiccups, thanks <a href="https://github.com/Rotzbua"><code>@​Rotzbua</code></a></li>
</ul>
<h2>DOMPurify 3.3.2</h2>
<ul>
<li>Fixed a possible bypass caused by jsdom's faulty raw-text tag parsing, thanks multiple reporters</li>
<li>Fixed a prototype pollution issue when working with custom elements, thanks <a href="https://github.com/christos-eth"><code>@​christos-eth</code></a></li>
<li>Fixed a lenient config parsing in <code>_isValidAttribute</code>, thanks <a href="https://github.com/christos-eth"><code>@​christos-eth</code></a></li>
<li>Bumped and removed several dependencies, thanks <a href="https://github.com/Rotzbua"><code>@​Rotzbua</code></a></li>
<li>Fixed the test suite after bumping dependencies, thanks <a href="https://github.com/Rotzbua"><code>@​Rotzbua</code></a></li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/cure53/DOMPurify/commit/5b0cdbbf52331e854c0a2de875b1a3790ecec2b8"><code>5b0cdbb</code></a> chore: merge main into 3.x for 3.4.1 release (<a href="https://redirect.github.com/cure53/DOMPurify/issues/1301">#1301</a>)</li>
<li><a href="https://github.com/cure53/DOMPurify/commit/09f59115a311469de5b625225760593e551f080a"><code>09f5911</code></a> test: added three more browsers to test setup (OSX, mobile)</li>
<li><a href="https://github.com/cure53/DOMPurify/commit/5b16e0b892e82b1779d62b9928b43c4c4ff290b9"><code>5b16e0b</code></a> Getting 3.x branch ready for 3.4.0 release (<a href="https://redirect.github.com/cure53/DOMPurify/issues/1250">#1250</a>)</li>
<li><a href="https://github.com/cure53/DOMPurify/commit/8bcbf73ae7eb56e7b4f1300b66cf543342c7ee27"><code>8bcbf73</code></a> chore: Preparing 3.3.3 release</li>
<li><a href="https://github.com/cure53/DOMPurify/commit/5faddd60af7b4d612f32a0c6b44432b77c8c490c"><code>5faddd6</code></a> fix: engine requirement (<a href="https://redirect.github.com/cure53/DOMPurify/issues/1210">#1210</a>)</li>
<li><a href="https://github.com/cure53/DOMPurify/commit/0f91e3add5c028bc4110c513b0c2571b284c35af"><code>0f91e3a</code></a> Update README.md</li>
<li><a href="https://github.com/cure53/DOMPurify/commit/d5ff1a8c605df1df998c2e7df2c4c8ac762b0dea"><code>d5ff1a8</code></a> Merge branch 'main' of github.com:cure53/DOMPurify</li>
<li><a href="https://github.com/cure53/DOMPurify/commit/c3efd489010366e755de9d65fd741888fd8b7462"><code>c3efd48</code></a> fix: moved back from jsdom 28 to jsdom 20</li>
<li><a href="https://github.com/cure53/DOMPurify/commit/988b888108c8df911ef37e68d0e26c85ad90e885"><code>988b888</code></a> fix: moved back from jsdom 28 to jsdom 20</li>
<li><a href="https://github.com/cure53/DOMPurify/commit/2726c74e9c6a0645127d1630e5ca49f64bc9fe67"><code>2726c74</code></a> chore: Preparing 3.3.2 release</li>
<li>Additional commits viewable in <a href="https://github.com/cure53/DOMPurify/compare/3.3.1...3.4.1">compare view</a></li>
</ul>
</details>
<details>
<summary>Install script changes</summary>
<p>This version adds <code>prepare</code> script that runs during installation. Review the package contents before updating.</p>
</details>
<br />

Updates `@tailwindcss/postcss` from 4.2.1 to 4.2.4
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/tailwindlabs/tailwindcss/releases"><code>@​tailwindcss/postcss</code>'s releases</a>.</em></p>
<blockquote>
<h2>v4.2.4</h2>
<h3>Fixed</h3>
<ul>
<li>Ensure imports in <code>@import</code> and <code>@plugin</code> still resolve correctly when using Vite aliases in <code>@tailwindcss/vite</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19947">#19947</a>)</li>
</ul>
<h2>v4.2.3</h2>
<h3>Fixed</h3>
<ul>
<li>Canonicalization: improve canonicalizations for <code>tracking-*</code> utilities by preferring non-negative utilities (e.g. <code>-tracking-tighter</code> → <code>tracking-wider</code>) (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19827">#19827</a>)</li>
<li>Fix crash due to invalid characters in candidate (exceeding valid unicode code point range) (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19829">#19829</a>)</li>
<li>Ensure query params in imports are considered unique resources when using <code>@tailwindcss/webpack</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19723">#19723</a>)</li>
<li>Canonicalization: collapse arbitrary values into shorthand utilities (e.g. <code>px-[1.2rem] py-[1.2rem]</code> → <code>p-[1.2rem]</code>) (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19837">#19837</a>)</li>
<li>Canonicalization: collapse <code>border-{t,b}-*</code> into <code>border-y-*</code>, <code>border-{l,r}-*</code> into <code>border-x-*</code>, and <code>border-{t,r,b,l}-*</code> into <code>border-*</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>scroll-m{t,b}-*</code> into <code>scroll-my-*</code>, <code>scroll-m{l,r}-*</code> into <code>scroll-mx-*</code>, and <code>scroll-m{t,r,b,l}-*</code> into <code>scroll-m-*</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>scroll-p{t,b}-*</code> into <code>scroll-py-*</code>, <code>scroll-p{l,r}-*</code> into <code>scroll-px-*</code>, and <code>scroll-p{t,r,b,l}-*</code> into <code>scroll-p-*</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>overflow-{x,y}-*</code> into <code>overflow-*</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>overscroll-{x,y}-*</code> into <code>overscroll-*</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Read from <code>--placeholder-color</code> instead of <code>--background-color</code> for <code>placeholder-*</code> utilities (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19843">#19843</a>)</li>
<li>Upgrade: ensure files are not emptied out when killing the upgrade process while it's running (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19846">#19846</a>)</li>
<li>Upgrade: use <code>config.content</code> when migrating from Tailwind CSS v3 to Tailwind CSS v4 (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19846">#19846</a>)</li>
<li>Upgrade: never migrate files that are ignored by git (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19846">#19846</a>)</li>
<li>Add <code>.env</code> and <code>.env.*</code> to default ignored content files (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19846">#19846</a>)</li>
<li>Canonicalization: migrate <code>overflow-ellipsis</code> into <code>text-ellipsis</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19849">#19849</a>)</li>
<li>Canonicalization: migrate <code>start-full</code> → <code>inset-s-full</code>, <code>start-auto</code> → <code>inset-s-auto</code>, <code>start-px</code> → <code>inset-s-px</code>, and <code>start-&lt;number&gt;</code> → <code>inset-s-&lt;number&gt;</code> as well as negative versions (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19849">#19849</a>)</li>
<li>Canonicalization: migrate <code>end-full</code> → <code>inset-e-full</code>, <code>end-auto</code> → <code>inset-e-auto</code>, <code>end-px</code> → <code>inset-e-px</code>, and <code>end-&lt;number&gt;</code> → <code>inset-e-&lt;number&gt;</code> as well as negative versions (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19849">#19849</a>)</li>
<li>Canonicalization: move the <code>-</code> sign inside the arbitrary value <code>-left-[9rem]</code> → <code>left-[-9rem]</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19858">#19858</a>)</li>
<li>Canonicalization: move the <code>-</code> sign outside the arbitrary value <code>ml-[calc(-1*var(--width))]</code> → <code>-ml-(--width)</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19858">#19858</a>)</li>
<li>Improve performance when scanning JSONL / NDJSON files (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19862">#19862</a>)</li>
<li>Support <code>NODE_PATH</code> environment variable in standalone CLI (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19617">#19617</a>)</li>
</ul>
<h2>v4.2.2</h2>
<h3>Added</h3>
<ul>
<li>Support Vite 8 in <code>@tailwindcss/vite</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19790">#19790</a>)</li>
</ul>
<h3>Fixed</h3>
<ul>
<li>Don't crash when candidates contain prototype properties like <code>row-constructor</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19725">#19725</a>)</li>
<li>Canonicalize <code>calc(var(--spacing)*…)</code> expressions into <code>--spacing(…)</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19769">#19769</a>)</li>
<li>Fix crash in canonicalization step when handling utilities containing <code>@property</code> at-rules (e.g. <code>shadow-sm border</code>) (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19727">#19727</a>)</li>
<li>Skip full reload for server only modules scanned by client CSS when using <code>@tailwindcss/vite</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19745">#19745</a>)</li>
<li>Improve canonicalization for bare values exceeding default spacing scale suggestions (e.g. <code>w-1234 h-1234</code> → <code>size-1234</code>) (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19809">#19809</a>)</li>
<li>Fix canonicalization resulting in empty list (e.g. <code>w-5 h-5 size-5</code> → <code>''</code> instead of <code>size-5</code>) (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19812">#19812</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/tailwindlabs/tailwindcss/blob/main/CHANGELOG.md"><code>@​tailwindcss/postcss</code>'s changelog</a>.</em></p>
<blockquote>
<h2>[4.2.4] - 2026-04-21</h2>
<h3>Fixed</h3>
<ul>
<li>Ensure imports in <code>@import</code> and <code>@plugin</code> still resolve correctly when using Vite aliases in <code>@tailwindcss/vite</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19947">#19947</a>)</li>
</ul>
<h2>[4.2.3] - 2026-04-20</h2>
<h3>Fixed</h3>
<ul>
<li>Canonicalization: improve canonicalizations for <code>tracking-*</code> utilities by preferring non-negative utilities (e.g. <code>-tracking-tighter</code> → <code>tracking-wider</code>) (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19827">#19827</a>)</li>
<li>Fix crash due to invalid characters in candidate (exceeding valid unicode code point range) (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19829">#19829</a>)</li>
<li>Ensure query params in imports are considered unique resources when using <code>@tailwindcss/webpack</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19723">#19723</a>)</li>
<li>Canonicalization: collapse arbitrary values into shorthand utilities (e.g. <code>px-[1.2rem] py-[1.2rem]</code> → <code>p-[1.2rem]</code>) (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19837">#19837</a>)</li>
<li>Canonicalization: collapse <code>border-{t,b}-*</code> into <code>border-y-*</code>, <code>border-{l,r}-*</code> into <code>border-x-*</code>, and <code>border-{t,r,b,l}-*</code> into <code>border-*</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>scroll-m{t,b}-*</code> into <code>scroll-my-*</code>, <code>scroll-m{l,r}-*</code> into <code>scroll-mx-*</code>, and <code>scroll-m{t,r,b,l}-*</code> into <code>scroll-m-*</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>scroll-p{t,b}-*</code> into <code>scroll-py-*</code>, <code>scroll-p{l,r}-*</code> into <code>scroll-px-*</code>, and <code>scroll-p{t,r,b,l}-*</code> into <code>scroll-p-*</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>overflow-{x,y}-*</code> into <code>overflow-*</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Canonicalization: collapse <code>overscroll-{x,y}-*</code> into <code>overscroll-*</code> (<a href="https://redirect.github.com/tailwindlabs/tailwindcss/pull/19842">#19842</a>)</li>
<li>Read from <code>--placeho...

_Description has been truncated_

### Human Comments
- **chris-srp** (2026-04-22T08:35:42Z): /lgtm
- **chris-srp** (2026-04-22T08:36:16Z): /lgtm
- **chris-srp** (2026-04-22T09:00:19Z): /lgtm

---

## 57b9ed9

**作者**: dependabot[bot]
**日期**: 2026-04-22T08:59:41Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/57b9ed904063f69df935234c8e1bb19c73668a67](https://github.com/SerendipityOneInc/ecap-workspace/commit/57b9ed904063f69df935234c8e1bb19c73668a67)

### Commit Message
```
chore(deps): update stripe requirement from <15.0,>=14.0 to >=14.4.1,<15.0 in /services/claw-interface (#1188)

Updates the requirements on
[stripe](https://github.com/stripe/stripe-python) to permit the latest
version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/stripe/stripe-python/releases">stripe's
releases</a>.</em></p>
<blockquote>
<h2>v14.4.1</h2>
<ul>
<li><a
href="https://redirect.github.com/stripe/stripe-python/pull/1748">#1748</a>
Add Stripe-Request-Trigger header</li>
<li><a
href="https://redirect.github.com/stripe/stripe-python/pull/1743">#1743</a>
Add agent information to UserAgent</li>
</ul>
<p>See <a
href="https://github.com/stripe/stripe-python/blob/v14.4.1/CHANGELOG.md">the
changelog for more details</a>.</p>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/stripe/stripe-python/blob/master/CHANGELOG.md">stripe's
changelog</a>.</em></p>
<blockquote>
<h2>14.4.1 - 2026-03-06</h2>
<ul>
<li><a
href="https://redirect.github.com/stripe/stripe-python/pull/1748">#1748</a>
Add Stripe-Request-Trigger header</li>
<li><a
href="https://redirect.github.com/stripe/stripe-python/pull/1743">#1743</a>
Add agent information to UserAgent</li>
</ul>
<h2>14.4.0 - 2026-02-25</h2>
<p>This release changes the pinned API version to
<code>2026-02-25.clover</code>.</p>
<ul>
<li><a
href="https://redirect.github.com/stripe/stripe-python/pull/1737">#1737</a>
Allow AIOHTTPClient to accept user-provided session or connector. Fixes
<a
href="https://redirect.github.com/stripe/stripe-python/pull/1736">#1736</a></li>
<li><a
href="https://redirect.github.com/stripe/stripe-python/pull/1732">#1732</a>
Update generated code
<ul>
<li>Add support for new resources <code>reserve.Hold</code>,
<code>reserve.Plan</code>, and <code>reserve.Release</code></li>
<li>Add support for <code>location</code> and <code>reader</code> on
<code>Charge.PaymentMethodDetail.CardPresent</code>,
<code>Charge.PaymentMethodDetail.InteracPresent</code>,
<code>ConfirmationToken.PaymentMethodPreview.Card.GeneratedFrom.PaymentMethodDetail.CardPresent</code>,
<code>PaymentAttemptRecord.PaymentMethodDetail.CardPresent</code>,
<code>PaymentAttemptRecord.PaymentMethodDetail.InteracPresent</code>,
<code>PaymentMethod.Card.GeneratedFrom.PaymentMethodDetail.CardPresent</code>,
<code>PaymentRecord.PaymentMethodDetail.CardPresent</code>, and
<code>PaymentRecord.PaymentMethodDetail.InteracPresent</code></li>
<li>Add support for new value <code>lk_vat</code> on enums
<code>Checkout.Session.CustomerDetail.TaxId.type</code>,
<code>Invoice.CustomerTaxId.type</code>,
<code>Tax.Calculation.CustomerDetail.TaxId.type</code>,
<code>Tax.Transaction.CustomerDetail.TaxId.type</code>, and
<code>TaxId.type</code></li>
<li>Add support for new value <code>lk_vat</code> on enums
<code>CustomerCreateParamsTaxIdDatum.type</code>,
<code>CustomerCreateTaxIdParams.type</code>,
<code>InvoiceCreatePreviewParamsCustomerDetailTaxId.type</code>,
<code>TaxIdCreateParams.type</code>, and
<code>tax.CalculationCreateParamsCustomerDetailTaxId.type</code></li>
<li>Add support for new values <code>reserve.hold.created</code>,
<code>reserve.hold.updated</code>, <code>reserve.plan.created</code>,
<code>reserve.plan.disabled</code>, <code>reserve.plan.expired</code>,
<code>reserve.plan.updated</code>, and
<code>reserve.release.created</code> on enum
<code>Event.type</code></li>
<li>Add support for new values <code>terminal_wifi_certificate</code>
and <code>terminal_wifi_private_key</code> on enums
<code>File.purpose</code> and <code>FileListParams.purpose</code></li>
<li>Add support for new values <code>terminal_wifi_certificate</code>
and <code>terminal_wifi_private_key</code> on enum
<code>FileCreateParams.purpose</code></li>
<li>Add support for new value <code>pay_by_bank</code> on enums
<code>Invoice.PaymentSetting.payment_method_types</code>,
<code>InvoiceCreateParamsPaymentSetting.payment_method_types</code>,
<code>InvoiceModifyParamsPaymentSetting.payment_method_types</code>,
<code>Subscription.PaymentSetting.payment_method_types</code>,
<code>SubscriptionCreateParamsPaymentSetting.payment_method_types</code>,
and
<code>SubscriptionModifyParamsPaymentSetting.payment_method_types</code></li>
<li>Add support for <code>display_name</code> and
<code>service_user_number</code> on
<code>Mandate.PaymentMethodDetail.BacsDebit</code></li>
<li>Change type of
<code>PaymentAttemptRecord.PaymentMethodDetail.Boleto.tax_id</code> and
<code>PaymentRecord.PaymentMethodDetail.Boleto.tax_id</code> from
<code>string</code> to <code>nullable(string)</code></li>
<li>Change type of
<code>PaymentAttemptRecord.PaymentMethodDetail.UsBankAccount.expected_debit_date</code>
and
<code>PaymentRecord.PaymentMethodDetail.UsBankAccount.expected_debit_date</code>
from <code>nullable(string)</code> to <code>string</code></li>
<li>Add support for <code>transaction_purpose</code> on
<code>PaymentIntent.PaymentMethodOption.UsBankAccount</code>,
<code>PaymentIntentConfirmParamsPaymentMethodOptionUsBankAccount</code>,
<code>PaymentIntentCreateParamsPaymentMethodOptionUsBankAccount</code>,
and
<code>PaymentIntentModifyParamsPaymentMethodOptionUsBankAccount</code></li>
<li>Add support for <code>optional_items</code> on
<code>PaymentLinkModifyParams</code></li>
<li>Remove support for unused <code>card_issuer_decline</code> on
<code>Radar.PaymentEvaluation.Insight</code></li>
<li>Add support for <code>payment_behavior</code> on
<code>SubscriptionItemDeleteParams</code></li>
<li>Add support for <code>lk</code> on
<code>Tax.Registration.CountryOption</code> and
<code>tax.RegistrationCreateParamsCountryOption</code></li>
<li>Add support for <code>cellular</code> and <code>stripe_s710</code>
on <code>Terminal.Configuration</code>,
<code>terminal.ConfigurationCreateParams</code>, and
<code>terminal.ConfigurationModifyParams</code></li>
<li>Add support for new values <code>simulated_stripe_s710</code> and
<code>stripe_s710</code> on enums
<code>Terminal.Reader.device_type</code> and
<code>terminal.ReaderListParams.device_type</code></li>
<li>Add support for new values <code>reserve.hold.created</code>,
<code>reserve.hold.updated</code>, <code>reserve.plan.created</code>,
<code>reserve.plan.disabled</code>, <code>reserve.plan.expired</code>,
<code>reserve.plan.updated</code>, and
<code>reserve.release.created</code> on enums
<code>WebhookEndpointCreateParams.enabled_events</code> and
<code>WebhookEndpointModifyParams.enabled_events</code></li>
<li>Add support for new value <code>2026-02-25.clover</code> on enum
<code>WebhookEndpointCreateParams.api_version</code></li>
<li>Add support for snapshot events <code>reserve.hold.created</code>
and <code>reserve.hold.updated</code> with resource
<code>reserve.Hold</code></li>
<li>Add support for snapshot events <code>reserve.plan.created</code>,
<code>reserve.plan.disabled</code>, <code>reserve.plan.expired</code>,
and <code>reserve.plan.updated</code> with resource
<code>reserve.Plan</code></li>
<li>Add support for snapshot event <code>reserve.release.created</code>
with resource <code>reserve.Release</code></li>
<li>Add support for error codes <code>storer_capability_missing</code>
and <code>storer_capability_not_active</code> on
<code>Invoice.LastFinalizationError</code>,
<code>PaymentIntent.LastPaymentError</code>,
<code>SetupAttempt.SetupError</code>,
<code>SetupIntent.LastSetupError</code>, and
<code>StripeError</code></li>
</ul>
</li>
<li><a
href="https://redirect.github.com/stripe/stripe-python/pull/1731">#1731</a>
Added instruction to update CA certificates in README.</li>
</ul>
<h2>14.3.0 - 2026-01-28</h2>
<p>This release changes the pinned API version to
<code>2026-01-28.clover</code>.</p>
<ul>
<li><a
href="https://redirect.github.com/stripe/stripe-python/pull/1725">#1725</a>
Update generated code
<ul>
<li>Add support for new resource
<code>radar.PaymentEvaluation</code></li>
<li>Add support for <code>create</code> method on resource
<code>radar.PaymentEvaluation</code></li>
<li>Add support for <code>adjustable_quantity</code> on
<code>LineItem</code></li>
<li>Add support for new value <code>risk_reserved</code> on enum
<code>BalanceTransaction.balance_type</code></li>
<li>Add support for new values <code>reserve_hold</code> and
<code>reserve_release</code> on enum
<code>BalanceTransaction.type</code></li>
<li>Add support for new values <code>2.3.0</code> and <code>2.3.1</code>
on enums
<code>Charge.PaymentMethodDetail.Card.ThreeDSecure.version</code>,
<code>PaymentIntentConfirmParamsPaymentMethodOptionCardThreeDSecure.version</code>,
<code>PaymentIntentCreateParamsPaymentMethodOptionCardThreeDSecure.version</code>,
<code>PaymentIntentModifyParamsPaymentMethodOptionCardThreeDSecure.version</code>,
<code>SetupAttempt.PaymentMethodDetail.Card.ThreeDSecure.version</code>,
<code>SetupIntentConfirmParamsPaymentMethodOptionCardThreeDSecure.version</code>,
<code>SetupIntentCreateParamsPaymentMethodOptionCardThreeDSecure.version</code>,
and
<code>SetupIntentModifyParamsPaymentMethodOptionCardThreeDSecure.version</code></li>
<li>Add support for new value <code>adyen</code> on enums
<code>Charge.PaymentMethodDetail.Ideal.bank</code>,
<code>ConfirmationToken.PaymentMethodPreview.Ideal.bank</code>,
<code>ConfirmationTokenCreateParamsPaymentMethodDatumIdeal.bank</code>,
<code>PaymentAttemptRecord.PaymentMethodDetail.Ideal.bank</code>,
<code>PaymentIntentConfirmParamsPaymentMethodDatumIdeal.bank</code>,
<code>PaymentIntentCreateParamsPaymentMethodDatumIdeal.bank</code>,
<code>PaymentIntentModifyParamsPaymentMethodDatumIdeal.bank</code>,
<code>PaymentMethod.Ideal.bank</code>,
<code>PaymentMethodCreateParamsIdeal.bank</code>,
<code>PaymentRecord.PaymentMethodDetail.Ideal.bank</code>,
<code>SetupAttempt.PaymentMethodDetail.Ideal.bank</code>,
<code>SetupIntentConfirmParamsPaymentMethodDatumIdeal.bank</code>,
<code>SetupIntentCreateParamsPaymentMethodDatumIdeal.bank</code>, and
<code>SetupIntentModifyParamsPaymentMethodDatumIdeal.bank</code></li>
<li>Add support for new value <code>ADYBNL2A</code> on enums
<code>Charge.PaymentMethodDetail.Ideal.bic</code>,
<code>ConfirmationToken.PaymentMethodPreview.Ideal.bic</code>,
<code>PaymentAttemptRecord.PaymentMethodDetail.Ideal.bic</code>,
<code>PaymentMethod.Ideal.bic</code>,
<code>PaymentRecord.PaymentMethodDetail.Ideal.bic</code>, and
<code>SetupAttempt.PaymentMethodDetail.Ideal.bic</code></li>
<li>Add support for new value <code>pl_nip</code> on enums
<code>Checkout.Session.CustomerDetail.TaxId.type</code>,
<code>Invoice.CustomerTaxId.type</code>,
<code>Tax.Calculation.CustomerDetail.TaxId.type</code>,
<code>Tax.Transaction.CustomerDetail.TaxId.type</code>, and
<code>TaxId.type</code></li>
<li>Add support for new value <code>pl_nip</code> on enums
<code>CustomerCreateParamsTaxIdDatum.type</code>,
<code>CustomerCreateTaxIdParams.type</code>,
<code>InvoiceCreatePreviewParamsCustomerDetailTaxId.type</code>,
<code>TaxIdCreateParams.type</code>, and
<code>tax.CalculationCreateParamsCustomerDetailTaxId.type</code></li>
<li>Change <code>Invoice.PaymentSetting.PaymentMethodOption.payto</code>
and <code>Subscription.PaymentSetting.PaymentMethodOption.payto</code>
to be required</li>
</ul>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/stripe/stripe-python/commit/2855dc80a44a3b2795d5ebd52397137488203ec9"><code>2855dc8</code></a>
Bump version to 14.4.1</li>
<li><a
href="https://github.com/stripe/stripe-python/commit/f3393d1e93d12bb03bbc1b2c371cf1fce39c7d9d"><code>f3393d1</code></a>
add new agent keys (<a
href="https://redirect.github.com/stripe/stripe-python/issues/1751">#1751</a>)</li>
<li><a
href="https://github.com/stripe/stripe-python/commit/1b1a293bde79d804c239af05b8d18811a85a3d8a"><code>1b1a293</code></a>
Add Stripe-Request-Trigger header (<a
href="https://redirect.github.com/stripe/stripe-python/issues/1748">#1748</a>)</li>
<li><a
href="https://github.com/stripe/stripe-python/commit/596c603e77b1eb9a1f8dd18d1c612c8131c0903a"><code>596c603</code></a>
Add agent information to UserAgent (<a
href="https://redirect.github.com/stripe/stripe-python/issues/1743">#1743</a>)</li>
<li><a
href="https://github.com/stripe/stripe-python/commit/e4b87f0068bf36f53dbcb1711bc8b12a39c7c32f"><code>e4b87f0</code></a>
add .claude directory (<a
href="https://redirect.github.com/stripe/stripe-python/issues/1740">#1740</a>)</li>
<li><a
href="https://github.com/stripe/stripe-python/commit/984950e50aee37efb9df61b86a0294581f868ec1"><code>984950e</code></a>
Bump version to 14.4.0</li>
<li><a
href="https://github.com/stripe/stripe-python/commit/a643eac6562ca7addbb37c3aa95fa3bafa5809f0"><code>a643eac</code></a>
Allow AIOHTTPClient to accept user-provided session or connector (<a
href="https://redirect.github.com/stripe/stripe-python/issues/1736">#1736</a>)
(<a
href="https://redirect.github.com/stripe/stripe-python/issues/1737">#1737</a>)</li>
<li><a
href="https://github.com/stripe/stripe-python/commit/aa759bd1f9465e85a9c6fae05569d20fa2c703da"><code>aa759bd</code></a>
Update generated code (<a
href="https://redirect.github.com/stripe/stripe-python/issues/1732">#1732</a>)</li>
<li><a
href="https://github.com/stripe/stripe-python/commit/5202e51e114cc71182a71b980b8e2ac51eb175df"><code>5202e51</code></a>
Added instruction to update CA certificates in README. (<a
href="https://redirect.github.com/stripe/stripe-python/issues/1731">#1731</a>)</li>
<li><a
href="https://github.com/stripe/stripe-python/commit/8dddb63f703d776ae9a06fb9d49bfc88e3e28e2c"><code>8dddb63</code></a>
Bump version to 14.3.0</li>
<li>Additional commits viewable in <a
href="https://github.com/stripe/stripe-python/compare/v14.0.0...v14.4.1">compare
view</a></li>
</ul>
</details>
<br />

<details>
<summary>Most Recent Ignore Conditions Applied to This Pull
Request</summary>

| Dependency Name | Ignore Conditions |
| --- | --- |
| stripe | [>= 15.dev0, < 16] |
</details>


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

### PR #1188: chore(deps): update stripe requirement from <15.0,>=14.0 to >=14.4.1,<15.0 in /services/claw-interface

Updates the requirements on [stripe](https://github.com/stripe/stripe-python) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/stripe/stripe-python/releases">stripe's releases</a>.</em></p>
<blockquote>
<h2>v14.4.1</h2>
<ul>
<li><a href="https://redirect.github.com/stripe/stripe-python/pull/1748">#1748</a> Add Stripe-Request-Trigger header</li>
<li><a href="https://redirect.github.com/stripe/stripe-python/pull/1743">#1743</a> Add agent information to UserAgent</li>
</ul>
<p>See <a href="https://github.com/stripe/stripe-python/blob/v14.4.1/CHANGELOG.md">the changelog for more details</a>.</p>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/stripe/stripe-python/blob/master/CHANGELOG.md">stripe's changelog</a>.</em></p>
<blockquote>
<h2>14.4.1 - 2026-03-06</h2>
<ul>
<li><a href="https://redirect.github.com/stripe/stripe-python/pull/1748">#1748</a> Add Stripe-Request-Trigger header</li>
<li><a href="https://redirect.github.com/stripe/stripe-python/pull/1743">#1743</a> Add agent information to UserAgent</li>
</ul>
<h2>14.4.0 - 2026-02-25</h2>
<p>This release changes the pinned API version to <code>2026-02-25.clover</code>.</p>
<ul>
<li><a href="https://redirect.github.com/stripe/stripe-python/pull/1737">#1737</a> Allow AIOHTTPClient to accept user-provided session or connector. Fixes <a href="https://redirect.github.com/stripe/stripe-python/pull/1736">#1736</a></li>
<li><a href="https://redirect.github.com/stripe/stripe-python/pull/1732">#1732</a> Update generated code
<ul>
<li>Add support for new resources <code>reserve.Hold</code>, <code>reserve.Plan</code>, and <code>reserve.Release</code></li>
<li>Add support for <code>location</code> and <code>reader</code> on <code>Charge.PaymentMethodDetail.CardPresent</code>, <code>Charge.PaymentMethodDetail.InteracPresent</code>, <code>ConfirmationToken.PaymentMethodPreview.Card.GeneratedFrom.PaymentMethodDetail.CardPresent</code>, <code>PaymentAttemptRecord.PaymentMethodDetail.CardPresent</code>, <code>PaymentAttemptRecord.PaymentMethodDetail.InteracPresent</code>, <code>PaymentMethod.Card.GeneratedFrom.PaymentMethodDetail.CardPresent</code>, <code>PaymentRecord.PaymentMethodDetail.CardPresent</code>, and <code>PaymentRecord.PaymentMethodDetail.InteracPresent</code></li>
<li>Add support for new value <code>lk_vat</code> on enums <code>Checkout.Session.CustomerDetail.TaxId.type</code>, <code>Invoice.CustomerTaxId.type</code>, <code>Tax.Calculation.CustomerDetail.TaxId.type</code>, <code>Tax.Transaction.CustomerDetail.TaxId.type</code>, and <code>TaxId.type</code></li>
<li>Add support for new value <code>lk_vat</code> on enums <code>CustomerCreateParamsTaxIdDatum.type</code>, <code>CustomerCreateTaxIdParams.type</code>, <code>InvoiceCreatePreviewParamsCustomerDetailTaxId.type</code>, <code>TaxIdCreateParams.type</code>, and <code>tax.CalculationCreateParamsCustomerDetailTaxId.type</code></li>
<li>Add support for new values <code>reserve.hold.created</code>, <code>reserve.hold.updated</code>, <code>reserve.plan.created</code>, <code>reserve.plan.disabled</code>, <code>reserve.plan.expired</code>, <code>reserve.plan.updated</code>, and <code>reserve.release.created</code> on enum <code>Event.type</code></li>
<li>Add support for new values <code>terminal_wifi_certificate</code> and <code>terminal_wifi_private_key</code> on enums <code>File.purpose</code> and <code>FileListParams.purpose</code></li>
<li>Add support for new values <code>terminal_wifi_certificate</code> and <code>terminal_wifi_private_key</code> on enum <code>FileCreateParams.purpose</code></li>
<li>Add support for new value <code>pay_by_bank</code> on enums <code>Invoice.PaymentSetting.payment_method_types</code>, <code>InvoiceCreateParamsPaymentSetting.payment_method_types</code>, <code>InvoiceModifyParamsPaymentSetting.payment_method_types</code>, <code>Subscription.PaymentSetting.payment_method_types</code>, <code>SubscriptionCreateParamsPaymentSetting.payment_method_types</code>, and <code>SubscriptionModifyParamsPaymentSetting.payment_method_types</code></li>
<li>Add support for <code>display_name</code> and <code>service_user_number</code> on <code>Mandate.PaymentMethodDetail.BacsDebit</code></li>
<li>Change type of <code>PaymentAttemptRecord.PaymentMethodDetail.Boleto.tax_id</code> and <code>PaymentRecord.PaymentMethodDetail.Boleto.tax_id</code> from <code>string</code> to <code>nullable(string)</code></li>
<li>Change type of <code>PaymentAttemptRecord.PaymentMethodDetail.UsBankAccount.expected_debit_date</code> and <code>PaymentRecord.PaymentMethodDetail.UsBankAccount.expected_debit_date</code> from <code>nullable(string)</code> to <code>string</code></li>
<li>Add support for <code>transaction_purpose</code> on <code>PaymentIntent.PaymentMethodOption.UsBankAccount</code>, <code>PaymentIntentConfirmParamsPaymentMethodOptionUsBankAccount</code>, <code>PaymentIntentCreateParamsPaymentMethodOptionUsBankAccount</code>, and <code>PaymentIntentModifyParamsPaymentMethodOptionUsBankAccount</code></li>
<li>Add support for <code>optional_items</code> on <code>PaymentLinkModifyParams</code></li>
<li>Remove support for unused <code>card_issuer_decline</code> on <code>Radar.PaymentEvaluation.Insight</code></li>
<li>Add support for <code>payment_behavior</code> on <code>SubscriptionItemDeleteParams</code></li>
<li>Add support for <code>lk</code> on <code>Tax.Registration.CountryOption</code> and <code>tax.RegistrationCreateParamsCountryOption</code></li>
<li>Add support for <code>cellular</code> and <code>stripe_s710</code> on <code>Terminal.Configuration</code>, <code>terminal.ConfigurationCreateParams</code>, and <code>terminal.ConfigurationModifyParams</code></li>
<li>Add support for new values <code>simulated_stripe_s710</code> and <code>stripe_s710</code> on enums <code>Terminal.Reader.device_type</code> and <code>terminal.ReaderListParams.device_type</code></li>
<li>Add support for new values <code>reserve.hold.created</code>, <code>reserve.hold.updated</code>, <code>reserve.plan.created</code>, <code>reserve.plan.disabled</code>, <code>reserve.plan.expired</code>, <code>reserve.plan.updated</code>, and <code>reserve.release.created</code> on enums <code>WebhookEndpointCreateParams.enabled_events</code> and <code>WebhookEndpointModifyParams.enabled_events</code></li>
<li>Add support for new value <code>2026-02-25.clover</code> on enum <code>WebhookEndpointCreateParams.api_version</code></li>
<li>Add support for snapshot events <code>reserve.hold.created</code> and <code>reserve.hold.updated</code> with resource <code>reserve.Hold</code></li>
<li>Add support for snapshot events <code>reserve.plan.created</code>, <code>reserve.plan.disabled</code>, <code>reserve.plan.expired</code>, and <code>reserve.plan.updated</code> with resource <code>reserve.Plan</code></li>
<li>Add support for snapshot event <code>reserve.release.created</code> with resource <code>reserve.Release</code></li>
<li>Add support for error codes <code>storer_capability_missing</code> and <code>storer_capability_not_active</code> on <code>Invoice.LastFinalizationError</code>, <code>PaymentIntent.LastPaymentError</code>, <code>SetupAttempt.SetupError</code>, <code>SetupIntent.LastSetupError</code>, and <code>StripeError</code></li>
</ul>
</li>
<li><a href="https://redirect.github.com/stripe/stripe-python/pull/1731">#1731</a> Added instruction to update CA certificates in README.</li>
</ul>
<h2>14.3.0 - 2026-01-28</h2>
<p>This release changes the pinned API version to <code>2026-01-28.clover</code>.</p>
<ul>
<li><a href="https://redirect.github.com/stripe/stripe-python/pull/1725">#1725</a> Update generated code
<ul>
<li>Add support for new resource <code>radar.PaymentEvaluation</code></li>
<li>Add support for <code>create</code> method on resource <code>radar.PaymentEvaluation</code></li>
<li>Add support for <code>adjustable_quantity</code> on <code>LineItem</code></li>
<li>Add support for new value <code>risk_reserved</code> on enum <code>BalanceTransaction.balance_type</code></li>
<li>Add support for new values <code>reserve_hold</code> and <code>reserve_release</code> on enum <code>BalanceTransaction.type</code></li>
<li>Add support for new values <code>2.3.0</code> and <code>2.3.1</code> on enums <code>Charge.PaymentMethodDetail.Card.ThreeDSecure.version</code>, <code>PaymentIntentConfirmParamsPaymentMethodOptionCardThreeDSecure.version</code>, <code>PaymentIntentCreateParamsPaymentMethodOptionCardThreeDSecure.version</code>, <code>PaymentIntentModifyParamsPaymentMethodOptionCardThreeDSecure.version</code>, <code>SetupAttempt.PaymentMethodDetail.Card.ThreeDSecure.version</code>, <code>SetupIntentConfirmParamsPaymentMethodOptionCardThreeDSecure.version</code>, <code>SetupIntentCreateParamsPaymentMethodOptionCardThreeDSecure.version</code>, and <code>SetupIntentModifyParamsPaymentMethodOptionCardThreeDSecure.version</code></li>
<li>Add support for new value <code>adyen</code> on enums <code>Charge.PaymentMethodDetail.Ideal.bank</code>, <code>ConfirmationToken.PaymentMethodPreview.Ideal.bank</code>, <code>ConfirmationTokenCreateParamsPaymentMethodDatumIdeal.bank</code>, <code>PaymentAttemptRecord.PaymentMethodDetail.Ideal.bank</code>, <code>PaymentIntentConfirmParamsPaymentMethodDatumIdeal.bank</code>, <code>PaymentIntentCreateParamsPaymentMethodDatumIdeal.bank</code>, <code>PaymentIntentModifyParamsPaymentMethodDatumIdeal.bank</code>, <code>PaymentMethod.Ideal.bank</code>, <code>PaymentMethodCreateParamsIdeal.bank</code>, <code>PaymentRecord.PaymentMethodDetail.Ideal.bank</code>, <code>SetupAttempt.PaymentMethodDetail.Ideal.bank</code>, <code>SetupIntentConfirmParamsPaymentMethodDatumIdeal.bank</code>, <code>SetupIntentCreateParamsPaymentMethodDatumIdeal.bank</code>, and <code>SetupIntentModifyParamsPaymentMethodDatumIdeal.bank</code></li>
<li>Add support for new value <code>ADYBNL2A</code> on enums <code>Charge.PaymentMethodDetail.Ideal.bic</code>, <code>ConfirmationToken.PaymentMethodPreview.Ideal.bic</code>, <code>PaymentAttemptRecord.PaymentMethodDetail.Ideal.bic</code>, <code>PaymentMethod.Ideal.bic</code>, <code>PaymentRecord.PaymentMethodDetail.Ideal.bic</code>, and <code>SetupAttempt.PaymentMethodDetail.Ideal.bic</code></li>
<li>Add support for new value <code>pl_nip</code> on enums <code>Checkout.Session.CustomerDetail.TaxId.type</code>, <code>Invoice.CustomerTaxId.type</code>, <code>Tax.Calculation.CustomerDetail.TaxId.type</code>, <code>Tax.Transaction.CustomerDetail.TaxId.type</code>, and <code>TaxId.type</code></li>
<li>Add support for new value <code>pl_nip</code> on enums <code>CustomerCreateParamsTaxIdDatum.type</code>, <code>CustomerCreateTaxIdParams.type</code>, <code>InvoiceCreatePreviewParamsCustomerDetailTaxId.type</code>, <code>TaxIdCreateParams.type</code>, and <code>tax.CalculationCreateParamsCustomerDetailTaxId.type</code></li>
<li>Change <code>Invoice.PaymentSetting.PaymentMethodOption.payto</code> and <code>Subscription.PaymentSetting.PaymentMethodOption.payto</code> to be required</li>
</ul>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/stripe/stripe-python/commit/2855dc80a44a3b2795d5ebd52397137488203ec9"><code>2855dc8</code></a> Bump version to 14.4.1</li>
<li><a href="https://github.com/stripe/stripe-python/commit/f3393d1e93d12bb03bbc1b2c371cf1fce39c7d9d"><code>f3393d1</code></a> add new agent keys (<a href="https://redirect.github.com/stripe/stripe-python/issues/1751">#1751</a>)</li>
<li><a href="https://github.com/stripe/stripe-python/commit/1b1a293bde79d804c239af05b8d18811a85a3d8a"><code>1b1a293</code></a> Add Stripe-Request-Trigger header (<a href="https://redirect.github.com/stripe/stripe-python/issues/1748">#1748</a>)</li>
<li><a href="https://github.com/stripe/stripe-python/commit/596c603e77b1eb9a1f8dd18d1c612c8131c0903a"><code>596c603</code></a> Add agent information to UserAgent (<a href="https://redirect.github.com/stripe/stripe-python/issues/1743">#1743</a>)</li>
<li><a href="https://github.com/stripe/stripe-python/commit/e4b87f0068bf36f53dbcb1711bc8b12a39c7c32f"><code>e4b87f0</code></a> add .claude directory (<a href="https://redirect.github.com/stripe/stripe-python/issues/1740">#1740</a>)</li>
<li><a href="https://github.com/stripe/stripe-python/commit/984950e50aee37efb9df61b86a0294581f868ec1"><code>984950e</code></a> Bump version to 14.4.0</li>
<li><a href="https://github.com/stripe/stripe-python/commit/a643eac6562ca7addbb37c3aa95fa3bafa5809f0"><code>a643eac</code></a> Allow AIOHTTPClient to accept user-provided session or connector (<a href="https://redirect.github.com/stripe/stripe-python/issues/1736">#1736</a>) (<a href="https://redirect.github.com/stripe/stripe-python/issues/1737">#1737</a>)</li>
<li><a href="https://github.com/stripe/stripe-python/commit/aa759bd1f9465e85a9c6fae05569d20fa2c703da"><code>aa759bd</code></a> Update generated code (<a href="https://redirect.github.com/stripe/stripe-python/issues/1732">#1732</a>)</li>
<li><a href="https://github.com/stripe/stripe-python/commit/5202e51e114cc71182a71b980b8e2ac51eb175df"><code>5202e51</code></a> Added instruction to update CA certificates in README. (<a href="https://redirect.github.com/stripe/stripe-python/issues/1731">#1731</a>)</li>
<li><a href="https://github.com/stripe/stripe-python/commit/8dddb63f703d776ae9a06fb9d49bfc88e3e28e2c"><code>8dddb63</code></a> Bump version to 14.3.0</li>
<li>Additional commits viewable in <a href="https://github.com/stripe/stripe-python/compare/v14.0.0...v14.4.1">compare view</a></li>
</ul>
</details>
<br />

<details>
<summary>Most Recent Ignore Conditions Applied to This Pull Request</summary>

| Dependency Name | Ignore Conditions |
| --- | --- |
| stripe | [>= 15.dev0, < 16] |
</details>


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

---

## 24bbc33

**作者**: dependabot[bot]
**日期**: 2026-04-22T08:58:43Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/24bbc334b334799c40eaf3883ad958524dd5ad5c](https://github.com/SerendipityOneInc/ecap-workspace/commit/24bbc334b334799c40eaf3883ad958524dd5ad5c)

### Commit Message
```
chore(deps): update cryptography requirement from >=42.0.0 to >=46.0.7 in /services/claw-interface (#1187)

Updates the requirements on
[cryptography](https://github.com/pyca/cryptography) to permit the
latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst">cryptography's
changelog</a>.</em></p>
<blockquote>
<p>46.0.7 - 2026-04-07</p>
<pre><code>
* **SECURITY ISSUE**: Fixed an issue where non-contiguous buffers could
be
  passed to APIs that accept Python buffers, which could lead to buffer
  overflow. **CVE-2026-39892**
* Updated Windows, macOS, and Linux wheels to be compiled with OpenSSL
3.5.6.
<p>.. _v46-0-6:</p>
<p>46.0.6 - 2026-03-25<br />
</code></pre></p>
<ul>
<li><strong>SECURITY ISSUE</strong>: Fixed a bug where name constraints
were not applied
to peer names during verification when the leaf certificate contains a
wildcard DNS SAN. Ordinary X.509 topologies are not affected by this
bug,
including those used by the Web PKI. Credit to <strong>Oleh Konko
(1seal)</strong> for
reporting the issue. <strong>CVE-2026-34073</strong></li>
</ul>
<p>.. _v46-0-5:</p>
<p>46.0.5 - 2026-02-10</p>
<pre><code>
* An attacker could create a malicious public key that reveals portions
of your
private key when using certain uncommon elliptic curves (binary curves).
This version now includes additional security checks to prevent this
attack.
This issue only affects binary elliptic curves, which are rarely used in
real-world applications. Credit to **XlabAI Team of Tencent Xuanwu Lab
and
Atuin Automated Vulnerability Discovery Engine** for reporting the
issue.
  **CVE-2026-26007**
* Support for ``SECT*`` binary elliptic curves is deprecated and will be
  removed in the next release.
<p>.. v46-0-4:</p>
<p>46.0.4 - 2026-01-27<br />
</code></pre></p>
<ul>
<li><code>Dropped support for win_arm64 wheels</code>_.</li>
<li>Updated Windows, macOS, and Linux wheels to be compiled with OpenSSL
3.5.5.</li>
</ul>
<p>.. _v46-0-3:</p>
<p>46.0.3 - 2025-10-15</p>
<pre><code>
* Fixed compilation when using LibreSSL 4.2.0.
<p>.. _v46-0-2:<br />
&lt;/tr&gt;&lt;/table&gt;<br />
</code></pre></p>
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/pyca/cryptography/commit/622d672e429a7cff836a23c5903683dbec1901f5"><code>622d672</code></a>
46.0.7 release (<a
href="https://redirect.github.com/pyca/cryptography/issues/14602">#14602</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/91d728897bdad30cd5c79a2b23e207f1f050d587"><code>91d7288</code></a>
Cherry-pick <a
href="https://redirect.github.com/pyca/cryptography/issues/14542">#14542</a>
(<a
href="https://redirect.github.com/pyca/cryptography/issues/14543">#14543</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/06e120e682cb200e3f7050c02f0bcdac90c4c6ad"><code>06e120e</code></a>
bump version for 46.0.5 release (<a
href="https://redirect.github.com/pyca/cryptography/issues/14289">#14289</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/0eebb9dbb6343d9bc1d91e5a2482ed4e054a6d8c"><code>0eebb9d</code></a>
EC check key on cofactor &gt; 1 (<a
href="https://redirect.github.com/pyca/cryptography/issues/14287">#14287</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/bedf6e186b814f69a3f54f51252c23a71d44ed2e"><code>bedf6e1</code></a>
fix openssl version on 46 branch (<a
href="https://redirect.github.com/pyca/cryptography/issues/14220">#14220</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/e6f44fc8e6391f05d719fb9d369692325b87a471"><code>e6f44fc</code></a>
bump for 46.0.4 and drop win arm64 due to CI issues (<a
href="https://redirect.github.com/pyca/cryptography/issues/14217">#14217</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/c0af4dd7b75921bbe9f1d41a03dbd4b64a9e3403"><code>c0af4dd</code></a>
release 46.0.3 (<a
href="https://redirect.github.com/pyca/cryptography/issues/13681">#13681</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/99efe5ad150a56efadafacaffd0e3ee319373904"><code>99efe5a</code></a>
bump version for 46.0.2 (<a
href="https://redirect.github.com/pyca/cryptography/issues/13531">#13531</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/e735cfc27502320101c130335c556394a125ba52"><code>e735cfc</code></a>
release 46.0.1 (<a
href="https://redirect.github.com/pyca/cryptography/issues/13450">#13450</a>)</li>
<li><a
href="https://github.com/pyca/cryptography/commit/4e457ffba43a6d87efc63c33041e2081438dd8a4"><code>4e457ff</code></a>
Explicitly specify python in mac uv build invocation (<a
href="https://redirect.github.com/pyca/cryptography/issues/13447">#13447</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/pyca/cryptography/compare/42.0.0...46.0.7">compare
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

### PR #1187: chore(deps): update cryptography requirement from >=42.0.0 to >=46.0.7 in /services/claw-interface

Updates the requirements on [cryptography](https://github.com/pyca/cryptography) to permit the latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst">cryptography's changelog</a>.</em></p>
<blockquote>
<p>46.0.7 - 2026-04-07</p>
<pre><code>
* **SECURITY ISSUE**: Fixed an issue where non-contiguous buffers could be
  passed to APIs that accept Python buffers, which could lead to buffer
  overflow. **CVE-2026-39892**
* Updated Windows, macOS, and Linux wheels to be compiled with OpenSSL 3.5.6.
<p>.. _v46-0-6:</p>
<p>46.0.6 - 2026-03-25<br />
</code></pre></p>
<ul>
<li><strong>SECURITY ISSUE</strong>: Fixed a bug where name constraints were not applied
to peer names during verification when the leaf certificate contains a
wildcard DNS SAN. Ordinary X.509 topologies are not affected by this bug,
including those used by the Web PKI. Credit to <strong>Oleh Konko (1seal)</strong> for
reporting the issue. <strong>CVE-2026-34073</strong></li>
</ul>
<p>.. _v46-0-5:</p>
<p>46.0.5 - 2026-02-10</p>
<pre><code>
* An attacker could create a malicious public key that reveals portions of your
  private key when using certain uncommon elliptic curves (binary curves).
  This version now includes additional security checks to prevent this attack.
  This issue only affects binary elliptic curves, which are rarely used in
  real-world applications. Credit to **XlabAI Team of Tencent Xuanwu Lab and
  Atuin Automated Vulnerability Discovery Engine** for reporting the issue.
  **CVE-2026-26007**
* Support for ``SECT*`` binary elliptic curves is deprecated and will be
  removed in the next release.
<p>.. v46-0-4:</p>
<p>46.0.4 - 2026-01-27<br />
</code></pre></p>
<ul>
<li><code>Dropped support for win_arm64 wheels</code>_.</li>
<li>Updated Windows, macOS, and Linux wheels to be compiled with OpenSSL 3.5.5.</li>
</ul>
<p>.. _v46-0-3:</p>
<p>46.0.3 - 2025-10-15</p>
<pre><code>
* Fixed compilation when using LibreSSL 4.2.0.
<p>.. _v46-0-2:<br />
&lt;/tr&gt;&lt;/table&gt;<br />
</code></pre></p>
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/pyca/cryptography/commit/622d672e429a7cff836a23c5903683dbec1901f5"><code>622d672</code></a> 46.0.7 release (<a href="https://redirect.github.com/pyca/cryptography/issues/14602">#14602</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/91d728897bdad30cd5c79a2b23e207f1f050d587"><code>91d7288</code></a> Cherry-pick <a href="https://redirect.github.com/pyca/cryptography/issues/14542">#14542</a> (<a href="https://redirect.github.com/pyca/cryptography/issues/14543">#14543</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/06e120e682cb200e3f7050c02f0bcdac90c4c6ad"><code>06e120e</code></a> bump version for 46.0.5 release (<a href="https://redirect.github.com/pyca/cryptography/issues/14289">#14289</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/0eebb9dbb6343d9bc1d91e5a2482ed4e054a6d8c"><code>0eebb9d</code></a> EC check key on cofactor &gt; 1 (<a href="https://redirect.github.com/pyca/cryptography/issues/14287">#14287</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/bedf6e186b814f69a3f54f51252c23a71d44ed2e"><code>bedf6e1</code></a> fix openssl version on 46 branch (<a href="https://redirect.github.com/pyca/cryptography/issues/14220">#14220</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/e6f44fc8e6391f05d719fb9d369692325b87a471"><code>e6f44fc</code></a> bump for 46.0.4 and drop win arm64 due to CI issues (<a href="https://redirect.github.com/pyca/cryptography/issues/14217">#14217</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/c0af4dd7b75921bbe9f1d41a03dbd4b64a9e3403"><code>c0af4dd</code></a> release 46.0.3 (<a href="https://redirect.github.com/pyca/cryptography/issues/13681">#13681</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/99efe5ad150a56efadafacaffd0e3ee319373904"><code>99efe5a</code></a> bump version for 46.0.2 (<a href="https://redirect.github.com/pyca/cryptography/issues/13531">#13531</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/e735cfc27502320101c130335c556394a125ba52"><code>e735cfc</code></a> release 46.0.1 (<a href="https://redirect.github.com/pyca/cryptography/issues/13450">#13450</a>)</li>
<li><a href="https://github.com/pyca/cryptography/commit/4e457ffba43a6d87efc63c33041e2081438dd8a4"><code>4e457ff</code></a> Explicitly specify python in mac uv build invocation (<a href="https://redirect.github.com/pyca/cryptography/issues/13447">#13447</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/pyca/cryptography/compare/42.0.0...46.0.7">compare view</a></li>
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

---

## e59ac0f

**作者**: dependabot[bot]
**日期**: 2026-04-22T08:58:26Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/e59ac0ffc21b59f85396881bbd88ccafc82508e7](https://github.com/SerendipityOneInc/ecap-workspace/commit/e59ac0ffc21b59f85396881bbd88ccafc82508e7)

### Commit Message
```
chore(deps-dev): update pytest-bdd requirement from >=8.0.0 to >=8.1.0 in /services/claw-interface (#1185)

Updates the requirements on
[pytest-bdd](https://github.com/pytest-dev/pytest-bdd) to permit the
latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/pytest-dev/pytest-bdd/blob/master/CHANGES.rst">pytest-bdd's
changelog</a>.</em></p>
<blockquote>
<h2>[8.1.0] - 2024-12-05</h2>
<p>Added
+++++</p>
<p>Changed
+++++++</p>
<ul>
<li>Step arguments <code>&quot;datatable&quot;</code> and
<code>&quot;docstring&quot;</code> are now reserved, and they can't be
used as step argument names. An error is raised if a step parser uses
these names.</li>
<li>Scenario <code>description</code> field is now set for Cucumber JSON
output.</li>
</ul>
<p>Deprecated
++++++++++</p>
<p>Removed
+++++++</p>
<p>Fixed
+++++</p>
<ul>
<li>Fixed an issue with the upcoming pytest release related to the use
of <code>@pytest.mark.usefixtures</code> with an empty list.</li>
<li>Render template variables in docstrings and datatable cells with
example table entries, as we already do for steps definitions.</li>
</ul>
<p>Security
++++++++</p>
<h2>[8.0.0] - 2024-11-14</h2>
<p>Added
+++++</p>
<ul>
<li>Gherkin keyword aliases can now be used and correctly reported in
json and terminal output (see <code>Keywords
&lt;https://cucumber.io/docs/gherkin/reference/#keywords&gt;</code>_ for
permitted list).</li>
<li>Added localization support. The language of the feature file can be
specified using the <code># language: &lt;language&gt;</code> directive
at the beginning of the file.</li>
<li>Rule keyword can be used in feature files (see <code>Rule
&lt;https://cucumber.io/docs/gherkin/reference/#rule&gt;</code>_)</li>
<li>Added support for multiple example tables</li>
<li>Added filtering by tags against example tables</li>
<li>Since the 7.x series:
<ul>
<li>Tags can now be on multiple lines (stacked)</li>
<li>Continuation of steps using asterisks (<code>*</code>) instead of
<code>And</code>/<code>But</code> supported.</li>
<li>Added <code>datatable</code> argument for steps that contain a
datatable (see <code>Data Tables
&lt;https://cucumber.io/docs/gherkin/reference/#data-tables&gt;</code>_).</li>
<li>Added <code>docstring</code> argument for steps that contain a
docstring (see <code>Doc Strings
&lt;https://cucumber.io/docs/gherkin/reference/#doc-strings&gt;</code>_).</li>
</ul>
</li>
</ul>
<p>Changed
+++++++</p>
<ul>
<li>
<p>Changelog format updated to follow <code>Keep a Changelog
&lt;https://keepachangelog.com/en/1.1.0/&gt;</code>_.</p>
</li>
<li>
<p>Text after the <code>#</code> character is no longer stripped from
the Scenario and Feature name.</p>
</li>
<li>
<p>Since the 7.x series:</p>
<ul>
<li>Use the <code>gherkin-official
&lt;https://pypi.org/project/gherkin-official/&gt;</code>_ parser,
replacing the custom parsing logic. This will make pytest-bdd more
compatible with the Gherkin specification.</li>
<li>Multiline steps must now always use triple-quotes for the additional
lines.</li>
</ul>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/pytest-dev/pytest-bdd/commit/6cdd340504decb0bbe660639cc78788d244b498c"><code>6cdd340</code></a>
Bump version to 8.1.0</li>
<li><a
href="https://github.com/pytest-dev/pytest-bdd/commit/68b9625ae7251a0b62f56677b2a6b5eee67f731b"><code>68b9625</code></a>
Fix Changelog</li>
<li><a
href="https://github.com/pytest-dev/pytest-bdd/commit/86a956e12b25abd986d1c06382afa5f95c03df21"><code>86a956e</code></a>
Merge pull request <a
href="https://redirect.github.com/pytest-dev/pytest-bdd/issues/745">#745</a>
from pytest-dev/test-177</li>
<li><a
href="https://github.com/pytest-dev/pytest-bdd/commit/633ee28fd7323203702e234fdd277d6bd005371b"><code>633ee28</code></a>
Merge branch 'master' into test-177</li>
<li><a
href="https://github.com/pytest-dev/pytest-bdd/commit/6e1f54d2915e3e232a350ac0d319dd22d29b0619"><code>6e1f54d</code></a>
Update test steps</li>
<li><a
href="https://github.com/pytest-dev/pytest-bdd/commit/6a2b2fbfbc8e6376183bb769704c68d2208a63ff"><code>6a2b2fb</code></a>
Merge pull request <a
href="https://redirect.github.com/pytest-dev/pytest-bdd/issues/749">#749</a>
from pytest-dev/test-feature-description-in-json</li>
<li><a
href="https://github.com/pytest-dev/pytest-bdd/commit/02d7c3f48bcaae1fe8719e66680f176e14ce9d3a"><code>02d7c3f</code></a>
Add changelog entry</li>
<li><a
href="https://github.com/pytest-dev/pytest-bdd/commit/4df8963d2b1aa80dac327765b57046f1b6027172"><code>4df8963</code></a>
Add new description field that is now expected</li>
<li><a
href="https://github.com/pytest-dev/pytest-bdd/commit/e19288ac07da40730838275da4b091c1eaef31a7"><code>e19288a</code></a>
Add missing scenario description in json</li>
<li><a
href="https://github.com/pytest-dev/pytest-bdd/commit/0efda3f87d8ef59a6a8461f73f32e1db5a82db5a"><code>0efda3f</code></a>
Add test for json correctly populating the description from a
feature</li>
<li>Additional commits viewable in <a
href="https://github.com/pytest-dev/pytest-bdd/compare/8.0.0...8.1.0">compare
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

### PR #1185: chore(deps-dev): update pytest-bdd requirement from >=8.0.0 to >=8.1.0 in /services/claw-interface

Updates the requirements on [pytest-bdd](https://github.com/pytest-dev/pytest-bdd) to permit the latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/pytest-dev/pytest-bdd/blob/master/CHANGES.rst">pytest-bdd's changelog</a>.</em></p>
<blockquote>
<h2>[8.1.0] - 2024-12-05</h2>
<p>Added
+++++</p>
<p>Changed
+++++++</p>
<ul>
<li>Step arguments <code>&quot;datatable&quot;</code> and <code>&quot;docstring&quot;</code> are now reserved, and they can't be used as step argument names. An error is raised if a step parser uses these names.</li>
<li>Scenario <code>description</code> field is now set for Cucumber JSON output.</li>
</ul>
<p>Deprecated
++++++++++</p>
<p>Removed
+++++++</p>
<p>Fixed
+++++</p>
<ul>
<li>Fixed an issue with the upcoming pytest release related to the use of <code>@pytest.mark.usefixtures</code> with an empty list.</li>
<li>Render template variables in docstrings and datatable cells with example table entries, as we already do for steps definitions.</li>
</ul>
<p>Security
++++++++</p>
<h2>[8.0.0] - 2024-11-14</h2>
<p>Added
+++++</p>
<ul>
<li>Gherkin keyword aliases can now be used and correctly reported in json and terminal output (see <code>Keywords &lt;https://cucumber.io/docs/gherkin/reference/#keywords&gt;</code>_ for permitted list).</li>
<li>Added localization support. The language of the feature file can be specified using the <code># language: &lt;language&gt;</code> directive at the beginning of the file.</li>
<li>Rule keyword can be used in feature files (see <code>Rule &lt;https://cucumber.io/docs/gherkin/reference/#rule&gt;</code>_)</li>
<li>Added support for multiple example tables</li>
<li>Added filtering by tags against example tables</li>
<li>Since the 7.x series:
<ul>
<li>Tags can now be on multiple lines (stacked)</li>
<li>Continuation of steps using asterisks (<code>*</code>) instead of <code>And</code>/<code>But</code> supported.</li>
<li>Added <code>datatable</code> argument for steps that contain a datatable (see <code>Data Tables &lt;https://cucumber.io/docs/gherkin/reference/#data-tables&gt;</code>_).</li>
<li>Added <code>docstring</code> argument for steps that contain a docstring (see <code>Doc Strings &lt;https://cucumber.io/docs/gherkin/reference/#doc-strings&gt;</code>_).</li>
</ul>
</li>
</ul>
<p>Changed
+++++++</p>
<ul>
<li>
<p>Changelog format updated to follow <code>Keep a Changelog &lt;https://keepachangelog.com/en/1.1.0/&gt;</code>_.</p>
</li>
<li>
<p>Text after the <code>#</code> character is no longer stripped from the Scenario and Feature name.</p>
</li>
<li>
<p>Since the 7.x series:</p>
<ul>
<li>Use the <code>gherkin-official &lt;https://pypi.org/project/gherkin-official/&gt;</code>_ parser, replacing the custom parsing logic. This will make pytest-bdd more compatible with the Gherkin specification.</li>
<li>Multiline steps must now always use triple-quotes for the additional lines.</li>
</ul>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/pytest-dev/pytest-bdd/commit/6cdd340504decb0bbe660639cc78788d244b498c"><code>6cdd340</code></a> Bump version to 8.1.0</li>
<li><a href="https://github.com/pytest-dev/pytest-bdd/commit/68b9625ae7251a0b62f56677b2a6b5eee67f731b"><code>68b9625</code></a> Fix Changelog</li>
<li><a href="https://github.com/pytest-dev/pytest-bdd/commit/86a956e12b25abd986d1c06382afa5f95c03df21"><code>86a956e</code></a> Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest-bdd/issues/745">#745</a> from pytest-dev/test-177</li>
<li><a href="https://github.com/pytest-dev/pytest-bdd/commit/633ee28fd7323203702e234fdd277d6bd005371b"><code>633ee28</code></a> Merge branch 'master' into test-177</li>
<li><a href="https://github.com/pytest-dev/pytest-bdd/commit/6e1f54d2915e3e232a350ac0d319dd22d29b0619"><code>6e1f54d</code></a> Update test steps</li>
<li><a href="https://github.com/pytest-dev/pytest-bdd/commit/6a2b2fbfbc8e6376183bb769704c68d2208a63ff"><code>6a2b2fb</code></a> Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest-bdd/issues/749">#749</a> from pytest-dev/test-feature-description-in-json</li>
<li><a href="https://github.com/pytest-dev/pytest-bdd/commit/02d7c3f48bcaae1fe8719e66680f176e14ce9d3a"><code>02d7c3f</code></a> Add changelog entry</li>
<li><a href="https://github.com/pytest-dev/pytest-bdd/commit/4df8963d2b1aa80dac327765b57046f1b6027172"><code>4df8963</code></a> Add new description field that is now expected</li>
<li><a href="https://github.com/pytest-dev/pytest-bdd/commit/e19288ac07da40730838275da4b091c1eaef31a7"><code>e19288a</code></a> Add missing scenario description in json</li>
<li><a href="https://github.com/pytest-dev/pytest-bdd/commit/0efda3f87d8ef59a6a8461f73f32e1db5a82db5a"><code>0efda3f</code></a> Add test for json correctly populating the description from a feature</li>
<li>Additional commits viewable in <a href="https://github.com/pytest-dev/pytest-bdd/compare/8.0.0...8.1.0">compare view</a></li>
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

---

## 89d98e4

**作者**: sam-srp
**日期**: 2026-04-22T08:30:47Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/89d98e43a294fae5c5ff63ba19e7f9017c096d73](https://github.com/SerendipityOneInc/ecap-workspace/commit/89d98e43a294fae5c5ff63ba19e7f9017c096d73)

### Commit Message
```
fix(web): render OOXML run-level spc (letter-spacing) in PPTX preview (#1204)

## Summary
- `PptxRenderer` parsed paragraph-level `spcBef`/`spcAft` but ignored
run-level `<a:rPr spc="…">`, so tracked-out labels (e.g. `SS26 FASHION
REPORT` with `spc="600"` = 6pt letter-spacing) rendered with no tracking
and looked visually smaller than in PowerPoint.
- Parse `spc` as 1/100 pt on the `TextRun` and emit CSS
`letter-spacing`, scaled through the same `100cqw /
var(--slide-design-cx-px)` factor as `fontSize` so tracking
shrinks/grows proportionally with the slide container across preview
sizes.
- No pptx file was changed; the fix lives entirely in the renderer.
Negative `spc` values (character compression) work out of the box via
CSS negative `letter-spacing`.

## Test plan
- [ ] Open a PPTX whose title uses `<a:rPr spc="600">` (e.g. any
SS26-style cover slide) in the artifact preview and confirm letters are
tracked out and match the PowerPoint render.
- [ ] Resize the preview panel and confirm letter-spacing scales with
the slide (no fixed pt drift).
- [ ] Spot-check a deck without `spc` attributes to confirm no
regression (letter-spacing unset → browser default).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1204: fix(web): render OOXML run-level spc (letter-spacing) in PPTX preview

## Summary
- `PptxRenderer` parsed paragraph-level `spcBef`/`spcAft` but ignored run-level `<a:rPr spc="…">`, so tracked-out labels (e.g. `SS26 FASHION REPORT` with `spc="600"` = 6pt letter-spacing) rendered with no tracking and looked visually smaller than in PowerPoint.
- Parse `spc` as 1/100 pt on the `TextRun` and emit CSS `letter-spacing`, scaled through the same `100cqw / var(--slide-design-cx-px)` factor as `fontSize` so tracking shrinks/grows proportionally with the slide container across preview sizes.
- No pptx file was changed; the fix lives entirely in the renderer. Negative `spc` values (character compression) work out of the box via CSS negative `letter-spacing`.

## Test plan
- [ ] Open a PPTX whose title uses `<a:rPr spc="600">` (e.g. any SS26-style cover slide) in the artifact preview and confirm letters are tracked out and match the PowerPoint render.
- [ ] Resize the preview panel and confirm letter-spacing scales with the slide (no fixed pt drift).
- [ ] Spot-check a deck without `spc` attributes to confirm no regression (letter-spacing unset → browser default).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 158e1ec

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T08:33:18Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/158e1ec894aea8dc33a1db7576f60332a2058d62](https://github.com/SerendipityOneInc/ecap-workspace/commit/158e1ec894aea8dc33a1db7576f60332a2058d62)

### Commit Message
```
docs(ci): add 2026-04-22 CI acceleration retrospective (#1205)

## Summary

把今天刚完成的 CI 加速系列（7 PRs + srp-actions 1 PR）记一份 spec，放在现有 spec
约定目录下。可以作为团队分享链接使用——无需每次复制粘贴长对话。

## 为什么单独开 PR 而不是合到 PR #1175/#1181

- 这两个 PR 已经 merge 了
- 新增文档改动纯追加、零执行风险，可以快速 review 合并
- 文档放错地方或措辞调整不影响生产 CI

## 主要内容

- 改动清单（按 web / python / iOS 分类，每项机制 + PR 链接）
- 实测收益表（merge queue 关键路径、单步骤 cold vs warm、本地测试）
- 主动跳过方案 + 理由（xlarge runner、self-hosted、UT/BDD 拆分等）
- 6 条可复用 insights（cache 持久化模式、rotation bucket 设计、xdist pitfalls 等）
- 遗留 follow-ups（#1166 #1178）

## 位置选择

放 \`docs/superpowers/specs/2026-04-22-ci-acceleration.md\`：
- 匹配现有 spec 命名约定（\`YYYY-MM-DD-<name>.md\`）
- 和 2026-04-20 的 web-dead-code / web-import-boundaries 等 "rollout spec"
对称
- 和 \`docs/ci-review-and-merge-queue.md\`（描述 CI
架构现状）互补：本文讲"我们怎么加速到现在的状态"，那篇讲"现在的架构如何工作"

## Test plan

- [ ] 本 PR CI 绿（只新增 markdown 文件）
- [ ] 合并后 URL 稳定 → 可复制给同事

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1205: docs(ci): add 2026-04-22 CI acceleration retrospective

## Summary

把今天刚完成的 CI 加速系列（7 PRs + srp-actions 1 PR）记一份 spec，放在现有 spec 约定目录下。可以作为团队分享链接使用——无需每次复制粘贴长对话。

## 为什么单独开 PR 而不是合到 PR #1175/#1181

- 这两个 PR 已经 merge 了
- 新增文档改动纯追加、零执行风险，可以快速 review 合并
- 文档放错地方或措辞调整不影响生产 CI

## 主要内容

- 改动清单（按 web / python / iOS 分类，每项机制 + PR 链接）
- 实测收益表（merge queue 关键路径、单步骤 cold vs warm、本地测试）
- 主动跳过方案 + 理由（xlarge runner、self-hosted、UT/BDD 拆分等）
- 6 条可复用 insights（cache 持久化模式、rotation bucket 设计、xdist pitfalls 等）
- 遗留 follow-ups（#1166 #1178）

## 位置选择

放 \`docs/superpowers/specs/2026-04-22-ci-acceleration.md\`：
- 匹配现有 spec 命名约定（\`YYYY-MM-DD-<name>.md\`）
- 和 2026-04-20 的 web-dead-code / web-import-boundaries 等 "rollout spec" 对称
- 和 \`docs/ci-review-and-merge-queue.md\`（描述 CI 架构现状）互补：本文讲"我们怎么加速到现在的状态"，那篇讲"现在的架构如何工作"

## Test plan

- [ ] 本 PR CI 绿（只新增 markdown 文件）
- [ ] 合并后 URL 稳定 → 可复制给同事

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T08:28:43Z): /lgtm
- **chris-srp** (2026-04-22T08:30:09Z): /lgtm

---

## f8dea23

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T08:14:21Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/f8dea23b176f0b080e2e46e1813309113cacaa7e](https://github.com/SerendipityOneInc/ecap-workspace/commit/f8dea23b176f0b080e2e46e1813309113cacaa7e)

### Commit Message
```
test(web): ArchivedSessionPanel 全面覆盖 (#894 Step 11 补) (#1198)

## Summary

Epic #894 Step 11 (#905) — \`ArchivedSessionPanel.tsx\` (301 LOC) 从 0% →
全分支,43 tests。源码仅 \`export\` 4 个 pure helper(同 SizeSelector 先例),无功能变动。

## 覆盖

| 组 | # | 覆盖 |
|---|---|---|
| extractTexts | 5 | string / 空白 / 混合 block / 非 text block / null/非对象 |
| cleanUserText | 5 | envelope+ts / 仅 ts / 无 / 大小写 / trim |
| isSystemUserMessage | 5 | 3 种注入模式 + 空 + 普通消息 |
| parseMessage | 10 | JSON string / 非法 / 非对象 / type=message 包装 / 非
user/assistant / user 清洗 / startup 过滤 / assistant 不清洗 / 空 content / 数组
block |
| 认证/就绪闸门 | 3 | authLoading / !chatReady / !isLoggedIn |
| 列表 loading | 4 | in-flight / success=false / 空列表 / unmount cancel |
| 列表渲染 | 6 | 排序 / badge / startup fallback / 空 fallback / 未选中 / {count}
替换 |
| 点击加载历史 | 5 | fetch+spinner / 成功渲染 bubble / 全 system 过滤 / success=false
/ 选中态高亮 |

## 源码改动

4 处 \`function X\` → \`export function X\`(\`extractTexts\` /
\`cleanUserText\` / \`isSystemUserMessage\` / \`parseMessage\`),让 pure
helper 可直接单测。参照 SizeSelector 的 \`getSizeDimensions\` /
\`groupSizesByRatio\` 先例。

## Bug-hunt 发现

**loadHistory 竞态** → issue #1197

快速切换两个 session 时,如果第二个 fetch 先返回,后到的第一个会覆盖 UI 显示错消息。对比 list-fetch 的
\`cancelled\` flag 模式,loadHistory 缺同样的保护。

## Test plan

- [x] \`pnpm --filter web test:unit --
tests/unit/app/session-history/ArchivedSessionPanel.unit.spec.tsx\`
(43/43 passed)
- [x] lint/prettier clean
- [ ] CI green

## 关联

- Epic #894 / Step 11 (#905)
- Follow-up bug: #1197
- 剩余:GuideTourModal (418)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1198: test(web): ArchivedSessionPanel 全面覆盖 (#894 Step 11 补)

## Summary

Epic #894 Step 11 (#905) — \`ArchivedSessionPanel.tsx\` (301 LOC) 从 0% → 全分支,43 tests。源码仅 \`export\` 4 个 pure helper(同 SizeSelector 先例),无功能变动。

## 覆盖

| 组 | # | 覆盖 |
|---|---|---|
| extractTexts | 5 | string / 空白 / 混合 block / 非 text block / null/非对象 |
| cleanUserText | 5 | envelope+ts / 仅 ts / 无 / 大小写 / trim |
| isSystemUserMessage | 5 | 3 种注入模式 + 空 + 普通消息 |
| parseMessage | 10 | JSON string / 非法 / 非对象 / type=message 包装 / 非 user/assistant / user 清洗 / startup 过滤 / assistant 不清洗 / 空 content / 数组 block |
| 认证/就绪闸门 | 3 | authLoading / !chatReady / !isLoggedIn |
| 列表 loading | 4 | in-flight / success=false / 空列表 / unmount cancel |
| 列表渲染 | 6 | 排序 / badge / startup fallback / 空 fallback / 未选中 / {count} 替换 |
| 点击加载历史 | 5 | fetch+spinner / 成功渲染 bubble / 全 system 过滤 / success=false / 选中态高亮 |

## 源码改动

4 处 \`function X\` → \`export function X\`(\`extractTexts\` / \`cleanUserText\` / \`isSystemUserMessage\` / \`parseMessage\`),让 pure helper 可直接单测。参照 SizeSelector 的 \`getSizeDimensions\` / \`groupSizesByRatio\` 先例。

## Bug-hunt 发现

**loadHistory 竞态** → issue #1197

快速切换两个 session 时,如果第二个 fetch 先返回,后到的第一个会覆盖 UI 显示错消息。对比 list-fetch 的 \`cancelled\` flag 模式,loadHistory 缺同样的保护。

## Test plan

- [x] \`pnpm --filter web test:unit -- tests/unit/app/session-history/ArchivedSessionPanel.unit.spec.tsx\` (43/43 passed)
- [x] lint/prettier clean
- [ ] CI green

## 关联

- Epic #894 / Step 11 (#905)
- Follow-up bug: #1197
- 剩余:GuideTourModal (418)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T08:14:10Z): /lgtm

---

## dc026dd

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T08:10:54Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/dc026dd751a54a424293e03d73d22bbaa66cb76b](https://github.com/SerendipityOneInc/ecap-workspace/commit/dc026dd751a54a424293e03d73d22bbaa66cb76b)

### Commit Message
```
fix(ios): unhang 4 service tests + close push:main observability gap (#1178) (#1195)

Closes #1178.

## Root cause

The 4 "failing" tests aren't assertion failures — they **hang for ~72s**
then time out. Evidence from CI run `24765663093`:

- `verifyUserThrowsOnHTTPError()` **passes** (its path has no
`AppError.capture`)
- The 4 failing tests all hit `AppError.capture` / `captureMessage` in
error paths:
- `AccountService.swift:129` (networkError), `:149` (invalidResponse
decode), `:155` (userNotActive)
- `NetworkService.swift:111` (decoding failure, propagated by
AgentService)

`ZooClawApp.init` correctly skips `SentrySDK.start()` in test mode
(`ZooClawApp.swift:43-53`), but `AppError.reporter` still defaulted to
`SentryErrorReporter()`. Calling `SentrySDK.capture(...)` against a
non-started SDK hangs the simulator.

## Code fix

- `AppError.swift`: add `NoOpErrorReporter`; make `AppError.reporter`
default to it when `XCTestBundlePath` is set (mirrors the existing
`ZooClawApp.isTesting` pattern).
- `AccountServiceTests` / `AgentServiceTests`: install a
`MockErrorReporter` in `init()` as defense-in-depth — so test ordering
across suites can't leak a live reporter.

Existing `AppErrorTests.init { AppError.reporter = mock }` pattern
unchanged.

## CI fix (observability gap)

The reason this sat broken on main for 2 days:

1. `ios-quality > Run unit tests` was gated to `push ||
workflow_dispatch`, so **merge_group skipped tests entirely** → broken
PR slipped past the queue. → Now `!= 'pull_request'`. Same change
applied to the 3 dependent steps (Test results summary / Coverage
Summary / Upload).
2. `Notify Feishu on failure` fired only on `pull_request`, so
**push:main failures were silent**. → Now also fires on `push` to
`refs/heads/main`. `CONTENT` template reworked with a conditional
`format()` so the push case renders commit + run links (the push context
has `github.event.pull_request.*` = null).

**Intentionally not touching**: the `needs.changes.outputs.ios ==
'true'` paths-filter — legitimate acceleration for non-iOS PRs. The new
merge_group gate plus push:main notification together cover the blind
spot without paying the full iOS-job cost on every PR.

**Scope**: iOS only. `web-quality` has the same Feishu gate — treating
that as a follow-up to keep the PR focused.

## Test plan

- [ ] CI passes on this PR (pull_request event → unit tests skipped,
SwiftLint + dup gating preserved)
- [ ] After merge-to-queue, merge_group CI runs unit tests and 4
previously-hanging tests pass in <1s each
- [ ] After merge to main, next push:main failure (if any) fires a
Feishu notification with commit + run links

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## 5aface6

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T08:15:41Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/5aface6139dd6d329fd232e85ef32754bcfab7d9](https://github.com/SerendipityOneInc/ecap-workspace/commit/5aface6139dd6d329fd232e85ef32754bcfab7d9)

### Commit Message
```
ci(dependabot): ignore motor/pymongo/Pillow until favie-common relaxes pins (#1196)

## Summary

- favie-common (pinned via git URL at v0.3.58 in
`services/claw-interface/requirements.txt`) still pins `pymongo==4.8.0`
and `pillow==11.2.1`
- UV resolver rejects any direct bump → Dependabot PRs #1184 (motor +
pymongo) and #1186 (Pillow) fail with `No solution found when resolving
dependencies`
- Same persistent-follow-up pattern as stripe #1180

Extends the pip `ignore:` section so Dependabot stops auto-reopening
these bumps. Lift each entry (or add a `versions:` constraint) once
favie-common relaxes the corresponding upstream pin.

## Test plan

- [x] `.github/dependabot.yml` is valid YAML (visual review)
- [ ] After merge: verify next Dependabot run does not re-open
motor/pymongo/Pillow PRs
- [ ] Close #1184 and #1186 once this merges (will be done as follow-up)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1196: ci(dependabot): ignore motor/pymongo/Pillow until favie-common relaxes pins

## Summary

- favie-common (pinned via git URL at v0.3.58 in `services/claw-interface/requirements.txt`) still pins `pymongo==4.8.0` and `pillow==11.2.1`
- UV resolver rejects any direct bump → Dependabot PRs #1184 (motor + pymongo) and #1186 (Pillow) fail with `No solution found when resolving dependencies`
- Same persistent-follow-up pattern as stripe #1180

Extends the pip `ignore:` section so Dependabot stops auto-reopening these bumps. Lift each entry (or add a `versions:` constraint) once favie-common relaxes the corresponding upstream pin.

## Test plan

- [x] `.github/dependabot.yml` is valid YAML (visual review)
- [ ] After merge: verify next Dependabot run does not re-open motor/pymongo/Pillow PRs
- [ ] Close #1184 and #1186 once this merges (will be done as follow-up)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## ae1ced3

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T08:07:09Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/ae1ced3cfa7fcf358772941fc49249fb49e7530e](https://github.com/SerendipityOneInc/ecap-workspace/commit/ae1ced3cfa7fcf358772941fc49249fb49e7530e)

### Commit Message
```
refactor(web): inline auth uid subscription in UserBusinessDataContext — fix W3 (A1-PR9) (#1194)

## Summary
- Fixes one W3 violation: `src/contexts/UserBusinessDataContext.tsx` was
importing `useAuth` from `@/hooks/useAuth` — violates "contexts/ must
not import hooks/".
- Provider inlines a window-event subscription + direct `getUserInfo()`
read instead of going through the `useAuth` hook.
- Baseline shrinks by 1 (13 → 12 after A1-PR8 merges; currently 14 → 13
on this branch).

## Why inline instead of routing through a new Context

`useAuth` lives in `hooks/`. W3 says `contexts/` can't import `hooks/`.
But `contexts/` **can** import from `lib/`. Since `useAuth`'s only job
here was reading `userInfo?.uid` + subscribing to `auth-state-changed`,
the Provider just does the same thing directly:

```ts
const [uid, setUid] = useState<string | undefined>(() => getUserInfo().uid)
useEffect(() => {
  const sync = () => setUid(getUserInfo().uid)
  window.addEventListener('auth-state-changed', sync)
  return () => window.removeEventListener('auth-state-changed', sync)
}, [])
```

Same data source as `useAuth`, no intermediate hook layer.

## Why `lib/auth/storage` instead of `lib/auth/manager`

`manager.getCurrentUser` is a trivial `return getUserInfo()` wrapper,
BUT `manager.ts` imports `firebase/auth` at module-load time. Any module
that imports from `manager` transitively triggers Firebase init, which
requires `NEXT_PUBLIC_FIREBASE_*` env vars and breaks tests that don't
mock it.

`storage.getUserInfo` is a pure localStorage read with zero side effects
or firebase chain. That's the right target for a Context module.

Verified by running `tests/unit/contexts/OpenClawContext.unit.spec.tsx`
— it transitively resolves `UserBusinessDataContext.tsx`; with `manager`
import it broke with `FirebaseError: Error (auth/invalid-api-key)`, with
`storage` it passes.

## Changes

| File | Change |
|---|---|
| `src/contexts/UserBusinessDataContext.tsx` | drop `useAuth` import;
add `getUserInfo` from `@/lib/auth/storage`; inline subscription |
| `.dependency-cruiser-known-violations.json` | remove W3 entry
`UserBusinessDataContext → useAuth` |

2 files, +13 / -12.

## Local verification
- `pnpm lint:imports` — exit 0, `12 known violations ignored`
- `pnpm test:unit tests/unit/contexts` — 29 tests pass (3 specs:
LanguageContext / MattermostContext / OpenClawContext)
- `npx tsc --noEmit` — clean
- `pnpm lint` — clean

## Remaining W3 (5 after this)

Same pattern applies to:
- `MattermostContext → useAuth` + `MattermostContext → useMattermost`
- `OpenClawContext → useAuth` + `→ useUserAgents` + `→ chat/hooks`

They'll either inline subscriptions like this PR, or — for the
`chat/hooks` path — extract hook bodies to `lib/` like A1-PR7 did for
`ConnectionStatus`. Each will land in its own small PR.

## Test plan
- [x] 29 context tests pass
- [x] tsc + eslint clean
- [x] Baseline JSON shrinks by 1
- [ ] CI confirms web-quality
- [ ] Reviewer validates the `storage` vs `manager` choice (avoiding
firebase init)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1194: refactor(web): inline auth uid subscription in UserBusinessDataContext — fix W3 (A1-PR9)

## Summary
- Fixes one W3 violation: `src/contexts/UserBusinessDataContext.tsx` was importing `useAuth` from `@/hooks/useAuth` — violates "contexts/ must not import hooks/".
- Provider inlines a window-event subscription + direct `getUserInfo()` read instead of going through the `useAuth` hook.
- Baseline shrinks by 1 (13 → 12 after A1-PR8 merges; currently 14 → 13 on this branch).

## Why inline instead of routing through a new Context

`useAuth` lives in `hooks/`. W3 says `contexts/` can't import `hooks/`. But `contexts/` **can** import from `lib/`. Since `useAuth`'s only job here was reading `userInfo?.uid` + subscribing to `auth-state-changed`, the Provider just does the same thing directly:

```ts
const [uid, setUid] = useState<string | undefined>(() => getUserInfo().uid)
useEffect(() => {
  const sync = () => setUid(getUserInfo().uid)
  window.addEventListener('auth-state-changed', sync)
  return () => window.removeEventListener('auth-state-changed', sync)
}, [])
```

Same data source as `useAuth`, no intermediate hook layer.

## Why `lib/auth/storage` instead of `lib/auth/manager`

`manager.getCurrentUser` is a trivial `return getUserInfo()` wrapper, BUT `manager.ts` imports `firebase/auth` at module-load time. Any module that imports from `manager` transitively triggers Firebase init, which requires `NEXT_PUBLIC_FIREBASE_*` env vars and breaks tests that don't mock it.

`storage.getUserInfo` is a pure localStorage read with zero side effects or firebase chain. That's the right target for a Context module.

Verified by running `tests/unit/contexts/OpenClawContext.unit.spec.tsx` — it transitively resolves `UserBusinessDataContext.tsx`; with `manager` import it broke with `FirebaseError: Error (auth/invalid-api-key)`, with `storage` it passes.

## Changes

| File | Change |
|---|---|
| `src/contexts/UserBusinessDataContext.tsx` | drop `useAuth` import; add `getUserInfo` from `@/lib/auth/storage`; inline subscription |
| `.dependency-cruiser-known-violations.json` | remove W3 entry `UserBusinessDataContext → useAuth` |

2 files, +13 / -12.

## Local verification
- `pnpm lint:imports` — exit 0, `12 known violations ignored`
- `pnpm test:unit tests/unit/contexts` — 29 tests pass (3 specs: LanguageContext / MattermostContext / OpenClawContext)
- `npx tsc --noEmit` — clean
- `pnpm lint` — clean

## Remaining W3 (5 after this)

Same pattern applies to:
- `MattermostContext → useAuth` + `MattermostContext → useMattermost`
- `OpenClawContext → useAuth` + `→ useUserAgents` + `→ chat/hooks`

They'll either inline subscriptions like this PR, or — for the `chat/hooks` path — extract hook bodies to `lib/` like A1-PR7 did for `ConnectionStatus`. Each will land in its own small PR.

## Test plan
- [x] 29 context tests pass
- [x] tsc + eslint clean
- [x] Baseline JSON shrinks by 1
- [ ] CI confirms web-quality
- [ ] Reviewer validates the `storage` vs `manager` choice (avoiding firebase init)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T08:06:59Z): /lgtm

---

## 4c63e13

**作者**: Leo-srp
**日期**: 2026-04-22T08:00:46Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/4c63e13c5a0f940f39d2ea30a4c79b76df810192](https://github.com/SerendipityOneInc/ecap-workspace/commit/4c63e13c5a0f940f39d2ea30a4c79b76df810192)

### Commit Message
```
fix: add identity encoding for twitter-v2 Nango proxy hang (#1174)

## Summary
- Add `Nango-Proxy-Accept-Encoding: identity` header for twitter-v2
proxy requests
- Fixes X (Twitter) connector completely non-functional — all API calls
hang indefinitely

## Root cause
X API returns gzip-compressed responses. Nango's proxy sends response
headers (including `content-length: 99`) but hangs while piping the gzip
body back to the client. Requesting `identity` encoding bypasses gzip
compression.

Verified:
- Without fix: HTTP 200 but hangs 30s+ with no body (all 3 twitter-v2
connections, both prod and staging)
- With fix: returns in <1s with correct data
- Other providers (GitHub, Slack, Notion, Linear) unaffected
- Direct X API call with same OAuth token works fine (2s)

## Test plan
- [ ] CI passes
- [ ] Deploy to staging, enable twitter-v2 connector, verify `x_get_me`
returns data
- [ ] Verify other connectors (GitHub, Linear, etc.) still work

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR #1174: fix: add identity encoding for twitter-v2 Nango proxy hang

## Summary
- Add `Nango-Proxy-Accept-Encoding: identity` header for twitter-v2 proxy requests
- Fixes X (Twitter) connector completely non-functional — all API calls hang indefinitely

## Root cause
X API returns gzip-compressed responses. Nango's proxy sends response headers (including `content-length: 99`) but hangs while piping the gzip body back to the client. Requesting `identity` encoding bypasses gzip compression.

Verified:
- Without fix: HTTP 200 but hangs 30s+ with no body (all 3 twitter-v2 connections, both prod and staging)
- With fix: returns in <1s with correct data
- Other providers (GitHub, Slack, Notion, Linear) unaffected
- Direct X API call with same OAuth token works fine (2s)

## Test plan
- [ ] CI passes
- [ ] Deploy to staging, enable twitter-v2 connector, verify `x_get_me` returns data
- [ ] Verify other connectors (GitHub, Linear, etc.) still work

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fe53360

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T08:00:34Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/fe533604db1e4ac1e6d72ba55c87d3dadbb63a02](https://github.com/SerendipityOneInc/ecap-workspace/commit/fe533604db1e4ac1e6d72ba55c87d3dadbb63a02)

### Commit Message
```
test(web): FeedbackDialog 全面覆盖 (#894 Step 11 补) (#1179)

## Summary

Epic #894 Step 11 (#905) — \`FeedbackDialog.tsx\` (337 LOC) 从 0% →
全分支,29 tests,**零源码改动**。

## 覆盖

| 组 | # | 覆盖 |
|---|---|---|
| Initial render (greeting) | 3 | 4 category 按钮 / 标题 / input+disabled
submit |
| Initial render (crash) | 2 | 4 crash option / crash 标题 |
| 非 crash category 选择 | 3 | add user+system / quick reply 只在最新 / unknown
安全 |
| Crash option 选择 | 1 | add user + followUp.other |
| 输入栏 | 5 | Enter/Shift+Enter/whitespace-only/空输入 guard |
| Submit success | 5 | payload / fallback / crash eventId / openClaw
session / null |
| Submit error | 2 | 转 error 态 / retry 回 followUp |
| Done + auto-close | 3 | 3s timer / continue 重置 / unmount 清 timer |
| Close button | 1 | onClose |
| Reset on new crash | 2 | prop 变 → 重置 / 同对象不重置 |
| ChatBubble | 2 | user 右对齐 / system wrench emoji |

## Bug-hunt 发现

**submit 失败时用户输入丢失** → issue #1177

L132 \`setInputValue('')\` 在 submit 前清空,catch 分支不恢复,用户点 retry 回 followUp
时 textarea 空了必须重输。符合 #905 "Feedback 提交失败的 fallback" bug-hunt 清单。

## 技术要点

- 存根 \`HTMLElement.prototype.scrollTo\`:jsdom 不实现,fake timer 下 rAF
同步触发会炸
- 只在 auto-close / continue / unmount 三个测试用 fake timer,遵循 web/CLAUDE.md
"fake-timers + waitFor 不混"

## Test plan

- [x] \`pnpm --filter web test:unit --
tests/unit/components/Feedback/FeedbackDialog.unit.spec.tsx\` (29/29
passed)
- [x] lint/prettier clean
- [ ] CI green

## 关联

- Epic #894 / Step 11 (#905)
- Follow-up bug: #1177
- 剩余:GuideTourModal (418) / ArchivedSessionPanel (301)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1179: test(web): FeedbackDialog 全面覆盖 (#894 Step 11 补)

## Summary

Epic #894 Step 11 (#905) — \`FeedbackDialog.tsx\` (337 LOC) 从 0% → 全分支,29 tests,**零源码改动**。

## 覆盖

| 组 | # | 覆盖 |
|---|---|---|
| Initial render (greeting) | 3 | 4 category 按钮 / 标题 / input+disabled submit |
| Initial render (crash) | 2 | 4 crash option / crash 标题 |
| 非 crash category 选择 | 3 | add user+system / quick reply 只在最新 / unknown 安全 |
| Crash option 选择 | 1 | add user + followUp.other |
| 输入栏 | 5 | Enter/Shift+Enter/whitespace-only/空输入 guard |
| Submit success | 5 | payload / fallback / crash eventId / openClaw session / null |
| Submit error | 2 | 转 error 态 / retry 回 followUp |
| Done + auto-close | 3 | 3s timer / continue 重置 / unmount 清 timer |
| Close button | 1 | onClose |
| Reset on new crash | 2 | prop 变 → 重置 / 同对象不重置 |
| ChatBubble | 2 | user 右对齐 / system wrench emoji |

## Bug-hunt 发现

**submit 失败时用户输入丢失** → issue #1177

L132 \`setInputValue('')\` 在 submit 前清空,catch 分支不恢复,用户点 retry 回 followUp 时 textarea 空了必须重输。符合 #905 "Feedback 提交失败的 fallback" bug-hunt 清单。

## 技术要点

- 存根 \`HTMLElement.prototype.scrollTo\`:jsdom 不实现,fake timer 下 rAF 同步触发会炸
- 只在 auto-close / continue / unmount 三个测试用 fake timer,遵循 web/CLAUDE.md "fake-timers + waitFor 不混"

## Test plan

- [x] \`pnpm --filter web test:unit -- tests/unit/components/Feedback/FeedbackDialog.unit.spec.tsx\` (29/29 passed)
- [x] lint/prettier clean
- [ ] CI green

## 关联

- Epic #894 / Step 11 (#905)
- Follow-up bug: #1177
- 剩余:GuideTourModal (418) / ArchivedSessionPanel (301)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T08:00:24Z): /lgtm

---

## efe0b0c

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T07:50:18Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/efe0b0c8247ff6a845624449e41ee51cff63c023](https://github.com/SerendipityOneInc/ecap-workspace/commit/efe0b0c8247ff6a845624449e41ee51cff63c023)

### Commit Message
```
refactor(web): extract useBrandTheme + useOnboarding to contexts/ — fix W2 last 2 (A1-PR8) (#1182)

## Summary
- Fixes the **remaining 2 W2 violations** via the standard
Context-extraction pattern.
- `useBrandTheme` + `useOnboarding` hooks moved from their Provider
files (in `components/`) to standalone `src/contexts/` modules.
- Side benefit: `resolveOnboardingStatus.ts` (pure logic, no React deps)
moved from `components/onboarding/` to
`src/lib/onboarding/resolveStatus.ts` — where pure helpers belong.
- Baseline shrinks by 2 (13 after A1-PR7 → 11 after this).

## Structural issue being fixed

Both `BrandThemeProvider.tsx` and `OnboardingProvider.tsx` co-located
their context-consumer hook with the Provider component:

\`\`\`tsx
// src/components/SomeProvider.tsx
const SomeContext = createContext<SomeContextValue>(...)
export function useSomeContext() { return useContext(SomeContext) }
export function SomeProvider({ children }) { ... }
\`\`\`

That puts the hook inside `components/`, so any consumer in
`src/hooks/**` (like `useBrandVocabulary` / `useRequireChat`) becomes a
W2 violation (\`hooks → components\`).

## The pattern applied

\`\`\`
contexts/XxxContext.tsx     ← Context + hook + types + fallback
components/XxxProvider.tsx ← imports Context; wraps children; sets value
\`\`\`

Every layer gets the right home:
- \`contexts → hooks/components/app\` is forbidden by W3 (already
respected)
- \`components → contexts\` is allowed (W4)
- \`hooks → contexts\` is allowed (W2 only forbids \`hooks →
components/app\`)
- \`app → contexts\` is trivially allowed

## Changes

| Path | Change |
|---|---|
| \`src/contexts/BrandThemeContext.tsx\` | **new** — Context +
\`useBrandTheme\` + \`BrandThemeContextValue\` + fallback |
| \`src/contexts/OnboardingContext.tsx\` | **new** — Context +
\`useOnboarding\` + \`OnboardingContextType\` + \`OnboardingStep\` +
\`OnboardingPhase\` types |
| \`src/lib/onboarding/resolveStatus.ts\` | \`git mv\` from
\`src/components/onboarding/resolveOnboardingStatus.ts\` |
| \`src/components/BrandThemeProvider.tsx\` | shrunk to the Provider
component only |
| \`src/components/onboarding/OnboardingProvider.tsx\` | shrunk to the
Provider component only; re-exports types from Context for caller compat
|
| 4 \`useBrandTheme\` call sites | retargeted to
\`@/contexts/BrandThemeContext\` |
| 15 \`useOnboarding\` call sites | retargeted to
\`@/contexts/OnboardingContext\` |
| Test mocks (4 specs) | repoint to new Context paths |
| \`.dependency-cruiser-known-violations.json\` | remove 2 W2 entries |

No re-export shim left behind.

## Local verification
- \`pnpm lint:imports\` — exit 0, \`13 known violations ignored\`
- \`pnpm test:unit tests/unit/components/onboarding tests/unit/hooks
tests/unit/components/BrandThemeProvider.unit.spec.tsx\` — 602 tests
pass
- \`npx tsc --noEmit\` — clean
- \`pnpm lint\` — clean

## Aftermath

With this + A1-PR7 (in flight):
- **W1** (lib pure): 0 ✅
- **W2** (hooks pure): 0 ✅ (first time!)
- **W4** (components below pages): 0 ✅
- **W6** (theme leaf): 0 ✅

Remaining baseline: W3 × 6 + W5 × 4 = 10 (the UI-state-feature coupling
cluster).

## Test plan
- [x] 602 affected tests pass
- [x] tsc + eslint clean
- [x] Baseline JSON shrinks (−2)
- [ ] CI confirms web-quality
- [ ] Reviewer validates the Context-extraction pattern, no missed
caller

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1182: refactor(web): extract useBrandTheme + useOnboarding to contexts/ — fix W2 last 2 (A1-PR8)

## Summary
- Fixes the **remaining 2 W2 violations** via the standard Context-extraction pattern.
- `useBrandTheme` + `useOnboarding` hooks moved from their Provider files (in `components/`) to standalone `src/contexts/` modules.
- Side benefit: `resolveOnboardingStatus.ts` (pure logic, no React deps) moved from `components/onboarding/` to `src/lib/onboarding/resolveStatus.ts` — where pure helpers belong.
- Baseline shrinks by 2 (13 after A1-PR7 → 11 after this).

## Structural issue being fixed

Both `BrandThemeProvider.tsx` and `OnboardingProvider.tsx` co-located their context-consumer hook with the Provider component:

\`\`\`tsx
// src/components/SomeProvider.tsx
const SomeContext = createContext<SomeContextValue>(...)
export function useSomeContext() { return useContext(SomeContext) }
export function SomeProvider({ children }) { ... }
\`\`\`

That puts the hook inside `components/`, so any consumer in `src/hooks/**` (like `useBrandVocabulary` / `useRequireChat`) becomes a W2 violation (\`hooks → components\`).

## The pattern applied

\`\`\`
contexts/XxxContext.tsx     ← Context + hook + types + fallback
components/XxxProvider.tsx  ← imports Context; wraps children; sets value
\`\`\`

Every layer gets the right home:
- \`contexts → hooks/components/app\` is forbidden by W3 (already respected)
- \`components → contexts\` is allowed (W4)
- \`hooks → contexts\` is allowed (W2 only forbids \`hooks → components/app\`)
- \`app → contexts\` is trivially allowed

## Changes

| Path | Change |
|---|---|
| \`src/contexts/BrandThemeContext.tsx\` | **new** — Context + \`useBrandTheme\` + \`BrandThemeContextValue\` + fallback |
| \`src/contexts/OnboardingContext.tsx\` | **new** — Context + \`useOnboarding\` + \`OnboardingContextType\` + \`OnboardingStep\` + \`OnboardingPhase\` types |
| \`src/lib/onboarding/resolveStatus.ts\` | \`git mv\` from \`src/components/onboarding/resolveOnboardingStatus.ts\` |
| \`src/components/BrandThemeProvider.tsx\` | shrunk to the Provider component only |
| \`src/components/onboarding/OnboardingProvider.tsx\` | shrunk to the Provider component only; re-exports types from Context for caller compat |
| 4 \`useBrandTheme\` call sites | retargeted to \`@/contexts/BrandThemeContext\` |
| 15 \`useOnboarding\` call sites | retargeted to \`@/contexts/OnboardingContext\` |
| Test mocks (4 specs) | repoint to new Context paths |
| \`.dependency-cruiser-known-violations.json\` | remove 2 W2 entries |

No re-export shim left behind.

## Local verification
- \`pnpm lint:imports\` — exit 0, \`13 known violations ignored\`
- \`pnpm test:unit tests/unit/components/onboarding tests/unit/hooks tests/unit/components/BrandThemeProvider.unit.spec.tsx\` — 602 tests pass
- \`npx tsc --noEmit\` — clean
- \`pnpm lint\` — clean

## Aftermath

With this + A1-PR7 (in flight):
- **W1** (lib pure): 0 ✅
- **W2** (hooks pure): 0 ✅ (first time!)
- **W4** (components below pages): 0 ✅
- **W6** (theme leaf): 0 ✅

Remaining baseline: W3 × 6 + W5 × 4 = 10 (the UI-state-feature coupling cluster).

## Test plan
- [x] 602 affected tests pass
- [x] tsc + eslint clean
- [x] Baseline JSON shrinks (−2)
- [ ] CI confirms web-quality
- [ ] Reviewer validates the Context-extraction pattern, no missed caller

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T07:50:07Z): /lgtm

---

## 37a2e67

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T07:46:18Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/37a2e67be45e2e2c7a01ab5e80425cc65121003d](https://github.com/SerendipityOneInc/ecap-workspace/commit/37a2e67be45e2e2c7a01ab5e80425cc65121003d)

### Commit Message
```
ci(ios): split actions/cache into restore + explicit save-on-success (#1181)

## Problem

PR #1175 加了 iOS DerivedData + Homebrew cache，但在验证时意外发现：**任何 job 失败都会让
\`actions/cache@v4\` 的 post-step save 被 skip**，从而 cache 永远不 warm 起来。

触发点：issue #1178（4 个 Swift 单测在 main 上静默失败）的 job failure 导致
workflow_dispatch 验证时：
- \`Post Restore Xcode DerivedData caches\`: **skipped**（没 save）
- \`Post Cache Homebrew downloads\`: **skipped**（没 save）

结论：只要 iOS unit test 挂一次（merge queue 下虽然不跑，但 push:main 和
workflow_dispatch 会触发），cache 就白存。PR #1175 的加速基础设施对"后续步骤脆弱性"零容错。

## Fix

把 \`actions/cache@v4\` 拆成 \`actions/cache/restore@v4\` + 显式
\`actions/cache/save@v4\`，save 步骤用 \`if: always() && <id>.outcome ==
'success'\` 保证：

1. **Homebrew downloads**: save 放在 \`Install tools\` 之后。brew 装好了就保存，哪怕后续
Swift build 或 test 挂了都不影响。
2. **Xcode DerivedData**: save 放在 \`Build for testing\` 之后、\`Run unit
tests\` **之前**。\`build-for-testing\` 包含了所有贵的编译产物；测试步骤只是消费这些产物，测试挂了不会污染
cache。

每个 save 步骤再加 \`cache-hit != 'true'\` 过滤：同一 week bucket + 同
Package.resolved 的后续 run 会 exact-key 命中，不做冗余 upload。

## Structural improvement

这次是"修 #1175 发现的 fragility"，但也是个普适的 CI 稳健模式：**"贵的中间产物要紧随着计算步骤保存，不要寄希望于
post-step 运行"**。任何依赖 post-step 机制的 cache 都有这个隐患。

## 关联

- #1175 (merged): 引入 DerivedData + brew cache
- #1178: 4 个 Swift 单测 main 上静默失败（independent fix，iOS 方处理）
- 本 PR 无需等待 #1178 修好——解耦 cache 持久化和测试通过状态

## Test plan

- [ ] 本 PR CI 绿（paths-filter 不会触发 ios-quality，但 YAML 语法检查会抓明显问题）
- [ ] 合并后 \`gh workflow run code-quality.yml --ref main\` 触发 dispatch
- [ ] 即便 #1178 未修复（unit test 仍挂），验证：
  - \`Save Homebrew downloads\` step 执行成功 + cache entry 产生
  - \`Save Xcode DerivedData caches\` step 执行成功 + cache entry 产生
- [ ] 第二次 dispatch 观察 restore 命中：
  - brew install 从 8s → 2-3s（已缓存 bottles）
- Build for testing 从 ~186s → 更低（Xcode incremental + cached ModuleCache）

## 后续

- 合并后由 workflow_dispatch 验证 cache 真实命中效果
- 若 #1178 之后修好，push:main 也会 exercise cache save（更多验证数据）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1181: ci(ios): split actions/cache into restore + explicit save-on-success

## Problem

PR #1175 加了 iOS DerivedData + Homebrew cache，但在验证时意外发现：**任何 job 失败都会让 \`actions/cache@v4\` 的 post-step save 被 skip**，从而 cache 永远不 warm 起来。

触发点：issue #1178（4 个 Swift 单测在 main 上静默失败）的 job failure 导致 workflow_dispatch 验证时：
- \`Post Restore Xcode DerivedData caches\`: **skipped**（没 save）
- \`Post Cache Homebrew downloads\`: **skipped**（没 save）

结论：只要 iOS unit test 挂一次（merge queue 下虽然不跑，但 push:main 和 workflow_dispatch 会触发），cache 就白存。PR #1175 的加速基础设施对"后续步骤脆弱性"零容错。

## Fix

把 \`actions/cache@v4\` 拆成 \`actions/cache/restore@v4\` + 显式 \`actions/cache/save@v4\`，save 步骤用 \`if: always() && <id>.outcome == 'success'\` 保证：

1. **Homebrew downloads**: save 放在 \`Install tools\` 之后。brew 装好了就保存，哪怕后续 Swift build 或 test 挂了都不影响。
2. **Xcode DerivedData**: save 放在 \`Build for testing\` 之后、\`Run unit tests\` **之前**。\`build-for-testing\` 包含了所有贵的编译产物；测试步骤只是消费这些产物，测试挂了不会污染 cache。

每个 save 步骤再加 \`cache-hit != 'true'\` 过滤：同一 week bucket + 同 Package.resolved 的后续 run 会 exact-key 命中，不做冗余 upload。

## Structural improvement

这次是"修 #1175 发现的 fragility"，但也是个普适的 CI 稳健模式：**"贵的中间产物要紧随着计算步骤保存，不要寄希望于 post-step 运行"**。任何依赖 post-step 机制的 cache 都有这个隐患。

## 关联

- #1175 (merged): 引入 DerivedData + brew cache
- #1178: 4 个 Swift 单测 main 上静默失败（independent fix，iOS 方处理）
- 本 PR 无需等待 #1178 修好——解耦 cache 持久化和测试通过状态

## Test plan

- [ ] 本 PR CI 绿（paths-filter 不会触发 ios-quality，但 YAML 语法检查会抓明显问题）
- [ ] 合并后 \`gh workflow run code-quality.yml --ref main\` 触发 dispatch
- [ ] 即便 #1178 未修复（unit test 仍挂），验证：
  - \`Save Homebrew downloads\` step 执行成功 + cache entry 产生
  - \`Save Xcode DerivedData caches\` step 执行成功 + cache entry 产生
- [ ] 第二次 dispatch 观察 restore 命中：
  - brew install 从 8s → 2-3s（已缓存 bottles）
  - Build for testing 从 ~186s → 更低（Xcode incremental + cached ModuleCache）

## 后续

- 合并后由 workflow_dispatch 验证 cache 真实命中效果
- 若 #1178 之后修好，push:main 也会 exercise cache save（更多验证数据）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T07:46:06Z): /lgtm

---

## ca1b030

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T07:45:05Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/ca1b0300eaaef1be55707340c4ca7eca0d1d5453](https://github.com/SerendipityOneInc/ecap-workspace/commit/ca1b0300eaaef1be55707340c4ca7eca0d1d5453)

### Commit Message
```
ci(dependabot): ignore stripe>=15 until attribute-access migration (#1180)

## Summary
- 关掉 dependabot 每周重提 `stripe>=15` bump 的 noise（跟进 PR #1043 的关闭）
- 把"社交约束"（靠人读 requirements.txt 行尾注释）升级成"机械约束"（dependabot.yml ignore）

## Why
`services/claw-interface/requirements.txt` 上的 `stripe>=14.0,<15.0`
带有内联注释说明 stripe 15 会破坏 dict-access，但 dependabot 看不到注释。PR #1043 就是第 N
次收到同样的 bump 提案、CI 假绿（mock 遮蔽了 StripeObject 行为变更）、人工关闭的循环。

加 `ignore` 之后只有显式升级 `<15` 到更高版本时 dependabot 才会重新提这个包的 major bump。

## Unblock path (另开 issue 跟踪)
1. `app/routes/subscription.py:71` 和
`app/services/stripe/order_confirm.py:59,106,133` 把 `cast(dict[str,
Any], ...)` + `.get()`/`[]` 改成 attribute-access
2. 补一个用真 StripeObject fixture 的契约测试，堵住未来 major bump 的假阴性
3. 去掉 `<15.0` pin + 本 PR 的 ignore

## Test plan
- [ ] Dependabot CI schema 校验（ci gate）绿
- [ ] 下周期 dependabot 周跑不再对 `stripe` 提 `>=15` 的 PR（事后观察）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1180: ci(dependabot): ignore stripe>=15 until attribute-access migration

## Summary
- 关掉 dependabot 每周重提 `stripe>=15` bump 的 noise（跟进 PR #1043 的关闭）
- 把"社交约束"（靠人读 requirements.txt 行尾注释）升级成"机械约束"（dependabot.yml ignore）

## Why
`services/claw-interface/requirements.txt` 上的 `stripe>=14.0,<15.0` 带有内联注释说明 stripe 15 会破坏 dict-access，但 dependabot 看不到注释。PR #1043 就是第 N 次收到同样的 bump 提案、CI 假绿（mock 遮蔽了 StripeObject 行为变更）、人工关闭的循环。

加 `ignore` 之后只有显式升级 `<15` 到更高版本时 dependabot 才会重新提这个包的 major bump。

## Unblock path (另开 issue 跟踪)
1. `app/routes/subscription.py:71` 和 `app/services/stripe/order_confirm.py:59,106,133` 把 `cast(dict[str, Any], ...)` + `.get()`/`[]` 改成 attribute-access
2. 补一个用真 StripeObject fixture 的契约测试，堵住未来 major bump 的假阴性
3. 去掉 `<15.0` pin + 本 PR 的 ignore

## Test plan
- [ ] Dependabot CI schema 校验（ci gate）绿
- [ ] 下周期 dependabot 周跑不再对 `stripe` 提 `>=15` 的 PR（事后观察）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T07:44:53Z): /lgtm

---

## 7f7b8d1

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T07:34:20Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/7f7b8d1cc5c493932eb374d2d269e76e250b177e](https://github.com/SerendipityOneInc/ecap-workspace/commit/7f7b8d1cc5c493932eb374d2d269e76e250b177e)

### Commit Message
```
test(web): ModelSelector 全面覆盖 (#894 Step 11 补) (#1173)

## Summary

Epic #894 Step 11 (#905) — \`ModelSelector.tsx\` (381 LOC) 从 0% → 全分支,56
tests,**零源码改动**。

## 覆盖

| 组 | # | 覆盖 |
|---|---|---|
| Trigger button | 3 | 正常 displayName / placeholder / disabled |
| Open/close | 8 | click/mousedown-outside/Escape/非-Escape/disabled-noop
|
| Tab auto-sync | 5 | selectedModel 三类型自动切 tab + 手动切 tab + underline |
| Model selection | 4 | click select / aria-selected / checkmark /
comingSoon-disabled |
| Empty tab | 2 | noModels i18n + hardcode fallback |
| Tab labels | 1 | i18n 空串回退到 "Text"/"Image"/"Video" |
| Tags | 3 | slice(0,3) / i18n 或 raw / 无 tags 不渲染 |
| 类型推断 | 15 | id 子串 → image/video 分类 + mode 覆盖 id |
| 图标分支 | 14 | owned_by / id / displayName 四种线索 + flux/SVG fallback |
| Trigger icon | 2 | 有/无 selectedModel 分支 |

## Bug-hunt

#905 flagged ModelSelector 键盘导航 a11y——源码只 ESC 关闭,缺
ArrowUp/Down/Enter。已开独立 issue #1172 跟踪,不在本 coverage PR 范围内(遵循
test-as-bug-hunt 规则:不在测试 PR 捎带修源 bug)。

## Test plan

- [x] \`pnpm --filter web test:unit --
tests/unit/components/ModelSelector.unit.spec.tsx\` (56/56 passed)
- [x] \`pnpm exec tsc --noEmit\` (ModelSelector 相关 0 error)
- [ ] CI green

## 关联

- Epic #894 / Step 11 (#905)
- Follow-up bug issue: #1172
- 剩余:FeedbackDialog (337) / GuideTourModal (418) / ArchivedSessionPanel
(301)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1173: test(web): ModelSelector 全面覆盖 (#894 Step 11 补)

## Summary

Epic #894 Step 11 (#905) — \`ModelSelector.tsx\` (381 LOC) 从 0% → 全分支,56 tests,**零源码改动**。

## 覆盖

| 组 | # | 覆盖 |
|---|---|---|
| Trigger button | 3 | 正常 displayName / placeholder / disabled |
| Open/close | 8 | click/mousedown-outside/Escape/非-Escape/disabled-noop |
| Tab auto-sync | 5 | selectedModel 三类型自动切 tab + 手动切 tab + underline |
| Model selection | 4 | click select / aria-selected / checkmark / comingSoon-disabled |
| Empty tab | 2 | noModels i18n + hardcode fallback |
| Tab labels | 1 | i18n 空串回退到 "Text"/"Image"/"Video" |
| Tags | 3 | slice(0,3) / i18n 或 raw / 无 tags 不渲染 |
| 类型推断 | 15 | id 子串 → image/video 分类 + mode 覆盖 id |
| 图标分支 | 14 | owned_by / id / displayName 四种线索 + flux/SVG fallback |
| Trigger icon | 2 | 有/无 selectedModel 分支 |

## Bug-hunt

#905 flagged ModelSelector 键盘导航 a11y——源码只 ESC 关闭,缺 ArrowUp/Down/Enter。已开独立 issue #1172 跟踪,不在本 coverage PR 范围内(遵循 test-as-bug-hunt 规则:不在测试 PR 捎带修源 bug)。

## Test plan

- [x] \`pnpm --filter web test:unit -- tests/unit/components/ModelSelector.unit.spec.tsx\` (56/56 passed)
- [x] \`pnpm exec tsc --noEmit\` (ModelSelector 相关 0 error)
- [ ] CI green

## 关联

- Epic #894 / Step 11 (#905)
- Follow-up bug issue: #1172
- 剩余:FeedbackDialog (337) / GuideTourModal (418) / ArchivedSessionPanel (301)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T07:34:08Z): /lgtm

---

## 9b4e94d

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T07:25:22Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/9b4e94dbe30dcad5bc805114eeb342c552e3f338](https://github.com/SerendipityOneInc/ecap-workspace/commit/9b4e94dbe30dcad5bc805114eeb342c552e3f338)

### Commit Message
```
refactor(web): lift showSaveToast + chatIdentity out of app/ — fix W4 (A1-PR6) (#1145)

## Summary
- Fixes **both W4 violations** in the baseline: `components/` reaching
into `app/[locale]/...` for shared helpers.
- Lifts `showSaveToast` to `src/lib/save-toast.ts` and moves
`chatIdentity.ts` to `src/lib/chat/`.
- Baseline shrinks **16 → 14**. W4 contract fully clean.

## The two violations

| Violator | Reached into | Fix |
|---|---|---|
| `components/agent-settings/AgentIdentitySection.tsx` |
`app/[locale]/claw-settings/components/SaveButton.tsx` (for
`showSaveToast`) | Extract wrapper to `src/lib/save-toast.ts`; rewrite 6
callers |
| `components/SideNav.tsx` | `app/[locale]/chat/lib/chatIdentity.ts`
(for `resolveChatIdentity`) | Move file to
`src/lib/chat/chatIdentity.ts`; rewrite 3 callers |

## Case 2 sub-issue: `lib → theme` would flip the violation

`chatIdentity.ts` had a module-level `DEFAULT_BOT_AVATAR =
getDefaultAssistantAvatarSrc()`. Simply moving to `lib/` would create a
new **W1** violation (`lib → theme`).

Resolution: make `resolveAssistantAvatarPresentation`'s `defaultAvatar`
parameter **required** and push avatar resolution to the callers (`app/`
and `components/` layers, both allowed to import theme). `SideNav` only
calls `resolveChatIdentity` so is unaffected by the signature change.

## Changes

| File | Change |
|---|---|
| `src/lib/save-toast.ts` | **new** — owns `showSaveToast` |
| `src/app/[locale]/claw-settings/components/SaveButton.tsx` | drop
`showSaveToast` export + `@/lib/download-toast` import |
| 5 claw-settings Section components + `AgentIdentitySection` + 2 specs
| retarget `showSaveToast` imports to `@/lib/save-toast` |
| `src/lib/chat/chatIdentity.ts` | renamed from
`src/app/[locale]/chat/lib/chatIdentity.ts`; drop `@/theme/brand-assets`
import + `DEFAULT_BOT_AVATAR` module const; `defaultAvatar` now required
|
| `src/app/[locale]/chat/GenClawClient.tsx` | declare its own
`DEFAULT_BOT_AVATAR` (app→theme OK) and pass it |
| 2 chat component callers + 4 test fixtures | pass `defaultAvatar`
explicitly |
| `.dependency-cruiser-known-violations.json` | remove 2 W4 entries (16
→ 14) |

18 files, +49 / -45. All `simple-import-sort` autofixes applied.

## Local verification
- \`pnpm lint:imports\` — exit 0, \`14 known violations ignored\`
- \`pnpm test:unit\` full suite — **3653 tests pass**
- \`npx tsc --noEmit\` — clean
- \`pnpm lint\` — clean

## Aftermath

With this + A1-PR5 (in flight):
- **W1** (lib pure): 0 ✅
- **W4** (components below pages): 0 ✅
- **W6** (theme leaf): 0 after A1-PR5 merges

Remaining baseline (post-merge of both): **13 = W2(3) + W3(5 or 6) +
W5(4)**. Last cleanup cluster is hooks/contexts/features.

## Interaction with open PRs

- **#1131 (A1-PR5)**: both PRs modify
`.dependency-cruiser-known-violations.json` but remove different entries
(W6 vs 2× W4). git 3-way merge will auto-resolve (non-overlapping array
elements). No file overlap otherwise.
- **#1126 (B5)**: no overlap — B5 deletes files + tweaks knip.config.ts,
this PR touches W4 import architecture.

## Test plan
- [x] All unit tests pass
- [x] tsc + eslint clean
- [x] `lint:imports` reports 14 known violations ignored (was 16)
- [ ] CI confirms web-quality + asset-size + jscpd
- [ ] Reviewer validates the `defaultAvatar` required-param approach vs
alternatives (module-level theme read, or inject a theme-provider
function)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1145: refactor(web): lift showSaveToast + chatIdentity out of app/ — fix W4 (A1-PR6)

## Summary
- Fixes **both W4 violations** in the baseline: `components/` reaching into `app/[locale]/...` for shared helpers.
- Lifts `showSaveToast` to `src/lib/save-toast.ts` and moves `chatIdentity.ts` to `src/lib/chat/`.
- Baseline shrinks **16 → 14**. W4 contract fully clean.

## The two violations

| Violator | Reached into | Fix |
|---|---|---|
| `components/agent-settings/AgentIdentitySection.tsx` | `app/[locale]/claw-settings/components/SaveButton.tsx` (for `showSaveToast`) | Extract wrapper to `src/lib/save-toast.ts`; rewrite 6 callers |
| `components/SideNav.tsx` | `app/[locale]/chat/lib/chatIdentity.ts` (for `resolveChatIdentity`) | Move file to `src/lib/chat/chatIdentity.ts`; rewrite 3 callers |

## Case 2 sub-issue: `lib → theme` would flip the violation

`chatIdentity.ts` had a module-level `DEFAULT_BOT_AVATAR = getDefaultAssistantAvatarSrc()`. Simply moving to `lib/` would create a new **W1** violation (`lib → theme`).

Resolution: make `resolveAssistantAvatarPresentation`'s `defaultAvatar` parameter **required** and push avatar resolution to the callers (`app/` and `components/` layers, both allowed to import theme). `SideNav` only calls `resolveChatIdentity` so is unaffected by the signature change.

## Changes

| File | Change |
|---|---|
| `src/lib/save-toast.ts` | **new** — owns `showSaveToast` |
| `src/app/[locale]/claw-settings/components/SaveButton.tsx` | drop `showSaveToast` export + `@/lib/download-toast` import |
| 5 claw-settings Section components + `AgentIdentitySection` + 2 specs | retarget `showSaveToast` imports to `@/lib/save-toast` |
| `src/lib/chat/chatIdentity.ts` | renamed from `src/app/[locale]/chat/lib/chatIdentity.ts`; drop `@/theme/brand-assets` import + `DEFAULT_BOT_AVATAR` module const; `defaultAvatar` now required |
| `src/app/[locale]/chat/GenClawClient.tsx` | declare its own `DEFAULT_BOT_AVATAR` (app→theme OK) and pass it |
| 2 chat component callers + 4 test fixtures | pass `defaultAvatar` explicitly |
| `.dependency-cruiser-known-violations.json` | remove 2 W4 entries (16 → 14) |

18 files, +49 / -45. All `simple-import-sort` autofixes applied.

## Local verification
- \`pnpm lint:imports\` — exit 0, \`14 known violations ignored\`
- \`pnpm test:unit\` full suite — **3653 tests pass**
- \`npx tsc --noEmit\` — clean
- \`pnpm lint\` — clean

## Aftermath

With this + A1-PR5 (in flight):
- **W1** (lib pure): 0 ✅
- **W4** (components below pages): 0 ✅
- **W6** (theme leaf): 0 after A1-PR5 merges

Remaining baseline (post-merge of both): **13 = W2(3) + W3(5 or 6) + W5(4)**. Last cleanup cluster is hooks/contexts/features.

## Interaction with open PRs

- **#1131 (A1-PR5)**: both PRs modify `.dependency-cruiser-known-violations.json` but remove different entries (W6 vs 2× W4). git 3-way merge will auto-resolve (non-overlapping array elements). No file overlap otherwise.
- **#1126 (B5)**: no overlap — B5 deletes files + tweaks knip.config.ts, this PR touches W4 import architecture.

## Test plan
- [x] All unit tests pass
- [x] tsc + eslint clean
- [x] `lint:imports` reports 14 known violations ignored (was 16)
- [ ] CI confirms web-quality + asset-size + jscpd
- [ ] Reviewer validates the `defaultAvatar` required-param approach vs alternatives (module-level theme read, or inject a theme-provider function)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T07:25:11Z): /lgtm

---

## 342b91d

**作者**: bill-srp
**日期**: 2026-04-22T07:24:11Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/342b91dddee53a049d33c499e55932f7b555c94a](https://github.com/SerendipityOneInc/ecap-workspace/commit/342b91dddee53a049d33c499e55932f7b555c94a)

### Commit Message
```
feat(ios): Voice input polish, waveform, toolbar and transcription improvements (#1157)

## Summary

- **Recording panel** — new inline waveform UI with cancel/confirm
buttons (replaces full-screen recording)
- **Voice waveform** — Canvas-based scrolling waveform matching Figma
spec with per-bar opacity
- **Voice toolbar** — extracted `ComposeVoiceToolbar` with space,
long-press repeat-delete, undo/redo, edit (wand)
- **Transcription** — insert at cursor position, voice edit rewrites
selected text or selects all
- **Move `onTranscription`** — from `ZooClawApp` to `ChatInputView`
where both coordinator and view model are in scope
- **Persist input mode** — voice/keyboard preference saved to
UserDefaults
- **Fix message ordering** — reverse messages at ChatListView boundary
for correct newest-at-bottom
- **Styling** — simplify message bubble (remove shadows/strokes), update
theme colors, ComposeInputPanel Figma match
- **CI/CD** — RC and App Store deploy stages, build number auto-bump

**Stack:** 2/3 — depends on #1156, merge after it.

## Test plan

- [ ] Voice recording: waveform animates, cancel discards, confirm
transcribes
- [ ] Transcription inserts at cursor position (not always appending)
- [ ] Long-press delete repeats, timer cleans up on view removal
- [ ] Undo/redo buttons appear after edits
- [ ] Voice edit (wand) selects all text and starts rewrite
- [ ] Input mode persists across app restarts
- [ ] Message order correct after fix (newest at bottom)
- [ ] Message bubbles render without shadows/strokes (simplified
styling)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR #1157: feat(ios): Voice input polish, waveform, toolbar and transcription improvements

## Summary

- **Recording panel** — new inline waveform UI with cancel/confirm buttons (replaces full-screen recording)
- **Voice waveform** — Canvas-based scrolling waveform matching Figma spec with per-bar opacity
- **Voice toolbar** — extracted `ComposeVoiceToolbar` with space, long-press repeat-delete, undo/redo, edit (wand)
- **Transcription** — insert at cursor position, voice edit rewrites selected text or selects all
- **Move `onTranscription`** — from `ZooClawApp` to `ChatInputView` where both coordinator and view model are in scope
- **Persist input mode** — voice/keyboard preference saved to UserDefaults
- **Fix message ordering** — reverse messages at ChatListView boundary for correct newest-at-bottom
- **Styling** — simplify message bubble (remove shadows/strokes), update theme colors, ComposeInputPanel Figma match
- **CI/CD** — RC and App Store deploy stages, build number auto-bump

**Stack:** 2/3 — depends on #1156, merge after it.

## Test plan

- [ ] Voice recording: waveform animates, cancel discards, confirm transcribes
- [ ] Transcription inserts at cursor position (not always appending)
- [ ] Long-press delete repeats, timer cleans up on view removal
- [ ] Undo/redo buttons appear after edits
- [ ] Voice edit (wand) selects all text and starts rewrite
- [ ] Input mode persists across app restarts
- [ ] Message order correct after fix (newest at bottom)
- [ ] Message bubbles render without shadows/strokes (simplified styling)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **bill-srp** (2026-04-22T07:23:44Z): /lgtm

---

## cc8f7eb

**作者**: dependabot[bot]
**日期**: 2026-04-22T07:27:07Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/cc8f7ebb6ea9634d5b24261559e301a86874fac0](https://github.com/SerendipityOneInc/ecap-workspace/commit/cc8f7ebb6ea9634d5b24261559e301a86874fac0)

### Commit Message
```
chore(deps): bump the minor-and-patch group across 1 directory with 21 updates (#1163)

Bumps the minor-and-patch group with 21 updates in the /web directory:

| Package | From | To |
| --- | --- | --- |
|
[@assistant-ui/react](https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react)
| `0.12.19` | `0.12.25` |
|
[@opennextjs/cloudflare](https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare)
| `1.17.1` | `1.19.3` |
| [@sentry/cloudflare](https://github.com/getsentry/sentry-javascript) |
`10.41.0` | `10.49.0` |
| [@sentry/nextjs](https://github.com/getsentry/sentry-javascript) |
`10.41.0` | `10.49.0` |
|
[@tanstack/react-query](https://github.com/TanStack/query/tree/HEAD/packages/react-query)
| `5.96.2` | `5.99.2` |
|
[@xyflow/react](https://github.com/xyflow/xyflow/tree/HEAD/packages/react)
| `12.10.1` | `12.10.2` |
| [dompurify](https://github.com/cure53/DOMPurify) | `3.3.1` | `3.4.1` |
| [mermaid](https://github.com/mermaid-js/mermaid) | `11.13.0` |
`11.14.0` |
| [react](https://github.com/facebook/react/tree/HEAD/packages/react) |
`19.2.4` | `19.2.5` |
|
[react-dom](https://github.com/facebook/react/tree/HEAD/packages/react-dom)
| `19.2.4` | `19.2.5` |
| [@eslint/eslintrc](https://github.com/eslint/eslintrc) | `3.3.4` |
`3.3.5` |
| [@playwright/test](https://github.com/microsoft/playwright) | `1.58.2`
| `1.59.1` |
|
[@tailwindcss/postcss](https://github.com/tailwindlabs/tailwindcss/tree/HEAD/packages/@tailwindcss-postcss)
| `4.2.1` | `4.2.4` |
|
[@vitest/coverage-v8](https://github.com/vitest-dev/vitest/tree/HEAD/packages/coverage-v8)
| `4.0.18` | `4.1.5` |
|
[@vitest/expect](https://github.com/vitest-dev/vitest/tree/HEAD/packages/expect)
| `4.0.18` | `4.1.5` |
| [dotenv](https://github.com/motdotla/dotenv) | `17.3.1` | `17.4.2` |
| [firebase](https://github.com/firebase/firebase-js-sdk) | `12.8.0` |
`12.12.1` |
| [knip](https://github.com/webpro-nl/knip/tree/HEAD/packages/knip) |
`6.5.0` | `6.6.0` |
| [prettier](https://github.com/prettier/prettier) | `3.8.1` | `3.8.3` |
|
[tailwindcss](https://github.com/tailwindlabs/tailwindcss/tree/HEAD/packages/tailwindcss)
| `4.2.1` | `4.2.4` |
|
[vitest](https://github.com/vitest-dev/vitest/tree/HEAD/packages/vitest)
| `4.0.18` | `4.1.5` |


Updates `@assistant-ui/react` from 0.12.19 to 0.12.25
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/assistant-ui/assistant-ui/releases"><code>@​assistant-ui/react</code>'s
releases</a>.</em></p>
<blockquote>
<h2><code>@​assistant-ui/react</code><a
href="https://github.com/0"><code>@​0</code></a>.12.25</h2>
<h3>Patch Changes</h3>
<ul>
<li>c988db8: chore: update dependencies</li>
<li>Updated dependencies [f20b9ca]</li>
<li>Updated dependencies [c988db8]
<ul>
<li><code>@​assistant-ui/core</code><a
href="https://github.com/0"><code>@​0</code></a>.1.14</li>
<li>assistant-stream@0.3.11</li>
<li>assistant-cloud@0.1.26</li>
<li><code>@​assistant-ui/store</code><a
href="https://github.com/0"><code>@​0</code></a>.2.7</li>
<li><code>@​assistant-ui/tap</code><a
href="https://github.com/0"><code>@​0</code></a>.5.8</li>
</ul>
</li>
</ul>
<h2><code>@​assistant-ui/react</code><a
href="https://github.com/0"><code>@​0</code></a>.12.24</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p>42bc640: feat: support edit lineage and startRun in EditComposer send
flow</p>
<ul>
<li>Add <code>SendOptions</code> with <code>startRun</code> flag to
<code>composer.send()</code></li>
<li>Expose <code>parentId</code> and <code>sourceId</code> on
<code>EditComposerState</code></li>
<li>Add <code>EditComposerRuntimeCore</code> interface extending
<code>ComposerRuntimeCore</code></li>
<li>Bypass text-unchanged guard when <code>startRun</code> is explicitly
set</li>
<li><code>ComposerSendOptions</code> extends <code>SendOptions</code>
for consistent layering</li>
</ul>
</li>
<li>
<p>e82726c: fix(react): forward viewport slack props from
MessagePrimitive.Root</p>
</li>
<li>
<p>376bb00: chore: update dependencies</p>
</li>
<li>
<p>87e7761: feat: generalize mention system into trigger popover
architecture with slash command support</p>
<ul>
<li>Introduce <code>ComposerInputPlugin</code> protocol to decouple
ComposerInput from mention-specific code</li>
<li>Extract generic <code>TriggerPopoverResource</code> from
<code>MentionResource</code> supporting multiple trigger characters</li>
<li>Add <code>Unstable_TriggerItem</code>,
<code>Unstable_TriggerCategory</code>,
<code>Unstable_TriggerAdapter</code> generic types</li>
<li>Add <code>Unstable_SlashCommandAdapter</code>,
<code>Unstable_SlashCommandItem</code> types</li>
<li>Add <code>ComposerPrimitive.Unstable_TriggerPopoverRoot</code> and
related primitives</li>
<li>Add <code>ComposerPrimitive.Unstable_SlashCommandRoot</code> and
related primitives</li>
<li>Add <code>unstable_useSlashCommandAdapter</code> hook for building
slash command adapters</li>
<li>Refactor <code>MentionResource</code> as thin wrapper around
<code>TriggerPopoverResource</code></li>
<li>Alias
<code>Unstable_MentionItem</code>/<code>Unstable_MentionAdapter</code>
to generic trigger types</li>
<li>Update <code>react-lexical</code> <code>KeyboardPlugin</code> to use
plugin protocol</li>
<li>All existing <code>Unstable_Mention*</code> APIs remain
unchanged</li>
</ul>
</li>
<li>
<p>Updated dependencies [42bc640]</p>
</li>
<li>
<p>Updated dependencies [376bb00]</p>
</li>
<li>
<p>Updated dependencies [87e7761]</p>
<ul>
<li><code>@​assistant-ui/core</code><a
href="https://github.com/0"><code>@​0</code></a>.1.13</li>
<li>assistant-cloud@0.1.25</li>
<li><code>@​assistant-ui/tap</code><a
href="https://github.com/0"><code>@​0</code></a>.5.7</li>
</ul>
</li>
</ul>
<h2><code>@​assistant-ui/react</code><a
href="https://github.com/0"><code>@​0</code></a>.12.23</h2>
<h3>Patch Changes</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/assistant-ui/assistant-ui/blob/main/packages/react/CHANGELOG.md"><code>@​assistant-ui/react</code>'s
changelog</a>.</em></p>
<blockquote>
<h2>0.12.25</h2>
<h3>Patch Changes</h3>
<ul>
<li>c988db8: chore: update dependencies</li>
<li>Updated dependencies [f20b9ca]</li>
<li>Updated dependencies [c988db8]
<ul>
<li><code>@​assistant-ui/core</code><a
href="https://github.com/0"><code>@​0</code></a>.1.14</li>
<li>assistant-stream@0.3.11</li>
<li>assistant-cloud@0.1.26</li>
<li><code>@​assistant-ui/store</code><a
href="https://github.com/0"><code>@​0</code></a>.2.7</li>
<li><code>@​assistant-ui/tap</code><a
href="https://github.com/0"><code>@​0</code></a>.5.8</li>
</ul>
</li>
</ul>
<h2>0.12.24</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p>42bc640: feat: support edit lineage and startRun in EditComposer send
flow</p>
<ul>
<li>Add <code>SendOptions</code> with <code>startRun</code> flag to
<code>composer.send()</code></li>
<li>Expose <code>parentId</code> and <code>sourceId</code> on
<code>EditComposerState</code></li>
<li>Add <code>EditComposerRuntimeCore</code> interface extending
<code>ComposerRuntimeCore</code></li>
<li>Bypass text-unchanged guard when <code>startRun</code> is explicitly
set</li>
<li><code>ComposerSendOptions</code> extends <code>SendOptions</code>
for consistent layering</li>
</ul>
</li>
<li>
<p>e82726c: fix(react): forward viewport slack props from
MessagePrimitive.Root</p>
</li>
<li>
<p>376bb00: chore: update dependencies</p>
</li>
<li>
<p>87e7761: feat: generalize mention system into trigger popover
architecture with slash command support</p>
<ul>
<li>Introduce <code>ComposerInputPlugin</code> protocol to decouple
ComposerInput from mention-specific code</li>
<li>Extract generic <code>TriggerPopoverResource</code> from
<code>MentionResource</code> supporting multiple trigger characters</li>
<li>Add <code>Unstable_TriggerItem</code>,
<code>Unstable_TriggerCategory</code>,
<code>Unstable_TriggerAdapter</code> generic types</li>
<li>Add <code>Unstable_SlashCommandAdapter</code>,
<code>Unstable_SlashCommandItem</code> types</li>
<li>Add <code>ComposerPrimitive.Unstable_TriggerPopoverRoot</code> and
related primitives</li>
<li>Add <code>ComposerPrimitive.Unstable_SlashCommandRoot</code> and
related primitives</li>
<li>Add <code>unstable_useSlashCommandAdapter</code> hook for building
slash command adapters</li>
<li>Refactor <code>MentionResource</code> as thin wrapper around
<code>TriggerPopoverResource</code></li>
<li>Alias
<code>Unstable_MentionItem</code>/<code>Unstable_MentionAdapter</code>
to generic trigger types</li>
<li>Update <code>react-lexical</code> <code>KeyboardPlugin</code> to use
plugin protocol</li>
<li>All existing <code>Unstable_Mention*</code> APIs remain
unchanged</li>
</ul>
</li>
<li>
<p>Updated dependencies [42bc640]</p>
</li>
<li>
<p>Updated dependencies [376bb00]</p>
</li>
<li>
<p>Updated dependencies [87e7761]</p>
<ul>
<li><code>@​assistant-ui/core</code><a
href="https://github.com/0"><code>@​0</code></a>.1.13</li>
<li>assistant-cloud@0.1.25</li>
<li><code>@​assistant-ui/tap</code><a
href="https://github.com/0"><code>@​0</code></a>.5.7</li>
</ul>
</li>
</ul>
<h2>0.12.23</h2>
<h3>Patch Changes</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/0950c800b72a0ddae37819c336bed3a409415bbf"><code>0950c80</code></a>
chore: update versions (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3778">#3778</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/c988db84494aede9eb07548fe1b5266456c53f08"><code>c988db8</code></a>
chore: update dependencies (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3809">#3809</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/61833123b3b6cf5ea92caa83e3519e857e44b181"><code>6183312</code></a>
chore: update versions (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3772">#3772</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/376bb00f21d90f3866fa7d57f2c3de11015787a9"><code>376bb00</code></a>
chore: update dependencies (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3777">#3777</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/e82726cd9ee2ada08487248ca31b54bcd1d4b025"><code>e82726c</code></a>
fix(react): forward viewport slack props from MessagePrimitive.Root (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3773">#3773</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/42bc64039d5a020044875bcad3ca2df21ad10009"><code>42bc640</code></a>
feat(core): support edit lineage and startRun in EditComposer (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3775">#3775</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/87e7761a81e2aff995829caf904abd3d0a700c54"><code>87e7761</code></a>
feat(react): generalize mention into trigger popover with slash command
suppo...</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/526890641e899f8b8c328e2895fd825800c5dbc5"><code>5268906</code></a>
chore: update versions (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3750">#3750</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/a8bf84bdc07a03a475564fd78eb9152e1ad7c52d"><code>a8bf84b</code></a>
feat(core): expose getLoadThreadsPromise on ThreadListRuntime (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3762">#3762</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/ec50e8a67564c4529d75e9707885a4b27751dda6"><code>ec50e8a</code></a>
fix(core): prevent resolved history tool calls from re-executing (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3717">#3717</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/assistant-ui/assistant-ui/commits/@assistant-ui/react@0.12.25/packages/react">compare
view</a></li>
</ul>
</details>
<br />

Updates `@opennextjs/cloudflare` from 1.17.1 to 1.19.3
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/opennextjs/opennextjs-cloudflare/releases"><code>@​opennextjs/cloudflare</code>'s
releases</a>.</em></p>
<blockquote>
<h2><code>@​opennextjs/cloudflare</code><a
href="https://github.com/1"><code>@​1</code></a>.19.3</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1215">#1215</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/608893e63e1ee16d07c7ec42da979657cf2a62bd"><code>608893e</code></a>
Thanks <a href="https://github.com/vicb"><code>@​vicb</code></a>! -
Factor large repeated values in manifests</p>
<p>This reduce the size of the generated code.</p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1218">#1218</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/f0d022685b24881a142bb01005ff78089be8c8d3"><code>f0d0226</code></a>
Thanks <a
href="https://github.com/314systems"><code>@​314systems</code></a>! -
remove <code>process.version</code> override</p>
<p>Remove process.version / process.versions.node overrides now that <a
href="https://redirect.github.com/unjs/unenv/pull/493">unjs/unenv#493</a>
is merged and shipped in <a
href="https://github.com/unjs/unenv/releases/tag/v2.0.0-rc.16">unenv@2.0.0-rc.16</a>
(project uses 2.0.0-rc.24)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1199">#1199</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/32594d6a921c5ebdbe25f38635bb2c9dabdcbff1"><code>32594d6</code></a>
Thanks <a href="https://github.com/SdSadat"><code>@​SdSadat</code></a>!
- fix(cli): fail fast in non-TTY environments instead of hanging on
config-creation prompts</p>
<p>When <code>open-next.config.ts</code> (or
<code>wrangler.(toml|json|jsonc)</code>) is missing, the CLI
prompts the user to auto-create it. In non-TTY environments (Cloudflare
Workers
Builds, Docker, CI) the Enquirer prompt can't read stdin, so the build
hangs or
fails with a truncated prompt and a cryptic exit code — the user sees
<code>? Missing required open-next.config.ts file, do you want to create
one? (Y/n)</code>
and then <code> ELIFECYCLE Command failed with exit code 13</code>, with
no hint at what
to do next.</p>
<p>Now, in non-interactive environments, both prompts throw an
actionable error
with the exact template to paste (for <code>open-next.config.ts</code>)
or point at the
existing <code>--skipWranglerConfigCheck</code> /
<code>SKIP_WRANGLER_CONFIG_CHECK</code> escape
hatch (for the wrangler config). Interactive behavior is unchanged.</p>
</li>
</ul>
<h2><code>@​opennextjs/cloudflare</code><a
href="https://github.com/1"><code>@​1</code></a>.19.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1207">#1207</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/0958726939d59e4a5c5a3062190278ffdfde38f5"><code>0958726</code></a>
Thanks <a
href="https://github.com/edmundhung"><code>@​edmundhung</code></a>! -
bump <code>@opennextjs/aws</code> to 3.10.2</p>
<p>See details at <a
href="https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2">https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2</a></p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1139">#1139</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/79b01b84fd92191517b7a11516c04208f9d474a6"><code>79b01b8</code></a>
Thanks <a
href="https://github.com/james-elicx"><code>@​james-elicx</code></a>! -
Fix Turbopack external module resolution by dynamically discovering
external imports at build time.</p>
<p>When packages are listed in <code>serverExternalPackages</code>,
Turbopack externalizes them via <code>externalImport()</code> which uses
dynamic <code>await import(id)</code>. The bundler (ESBuild) can't
statically analyze <code>import(id)</code> with a variable, so these
modules aren't included in the worker bundle.</p>
<p>This patch:</p>
<ul>
<li>Discovers hashed Turbopack external module mappings from
<code>.next/node_modules/</code> symlinks (e.g.
<code>shiki-43d062b67f27bbdc</code> → <code>shiki</code>)</li>
<li>Scans traced chunk files for bare external imports (e.g.
<code>externalImport(&quot;shiki&quot;)</code>) and subpath imports
(e.g. <code>shiki/engine/javascript</code>)</li>
<li>Generates explicit <code>switch/case</code> entries so the bundler
can statically resolve and include these modules</li>
</ul>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1203">#1203</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/6f02d12a75a78410711cc0d9db13ab0d41ed903a"><code>6f02d12</code></a>
Thanks <a
href="https://github.com/314systems"><code>@​314systems</code></a>! -
fix: exclude unsupported Next.js 16 releases from peer dependencies.</p>
<p>The previous range allowed Next.js 16.0.0 through 16.2.2 without a
peer dependency warning because <code>&gt;=16.2.3</code> was already
covered by <code>&gt;=15.5.15</code>.</p>
<p>The range now explicitly supports Next.js 15.5.15 and above in the
15.x line, and Next.js 16.2.3 and above in the 16.x line.</p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1200">#1200</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/7820ad0a0e5f57aba0580f3cabfdd0caa75cc9bb"><code>7820ad0</code></a>
Thanks <a
href="https://github.com/NathanDrake2406"><code>@​NathanDrake2406</code></a>!
- fix: reuse sharded tag data when filling the regional cache.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/opennextjs/opennextjs-cloudflare/blob/main/packages/cloudflare/CHANGELOG.md"><code>@​opennextjs/cloudflare</code>'s
changelog</a>.</em></p>
<blockquote>
<h2>1.19.3</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1215">#1215</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/608893e63e1ee16d07c7ec42da979657cf2a62bd"><code>608893e</code></a>
Thanks <a href="https://github.com/vicb"><code>@​vicb</code></a>! -
Factor large repeated values in manifests</p>
<p>This reduce the size of the generated code.</p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1218">#1218</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/f0d022685b24881a142bb01005ff78089be8c8d3"><code>f0d0226</code></a>
Thanks <a
href="https://github.com/314systems"><code>@​314systems</code></a>! -
remove <code>process.version</code> override</p>
<p>Remove process.version / process.versions.node overrides now that <a
href="https://redirect.github.com/unjs/unenv/pull/493">unjs/unenv#493</a>
is merged and shipped in <a
href="https://github.com/unjs/unenv/releases/tag/v2.0.0-rc.16">unenv@2.0.0-rc.16</a>
(project uses 2.0.0-rc.24)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1199">#1199</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/32594d6a921c5ebdbe25f38635bb2c9dabdcbff1"><code>32594d6</code></a>
Thanks <a href="https://github.com/SdSadat"><code>@​SdSadat</code></a>!
- fix(cli): fail fast in non-TTY environments instead of hanging on
config-creation prompts</p>
<p>When <code>open-next.config.ts</code> (or
<code>wrangler.(toml|json|jsonc)</code>) is missing, the CLI
prompts the user to auto-create it. In non-TTY environments (Cloudflare
Workers
Builds, Docker, CI) the Enquirer prompt can't read stdin, so the build
hangs or
fails with a truncated prompt and a cryptic exit code — the user sees
<code>? Missing required open-next.config.ts file, do you want to create
one? (Y/n)</code>
and then <code> ELIFECYCLE Command failed with exit code 13</code>, with
no hint at what
to do next.</p>
<p>Now, in non-interactive environments, both prompts throw an
actionable error
with the exact template to paste (for <code>open-next.config.ts</code>)
or point at the
existing <code>--skipWranglerConfigCheck</code> /
<code>SKIP_WRANGLER_CONFIG_CHECK</code> escape
hatch (for the wrangler config). Interactive behavior is unchanged.</p>
</li>
</ul>
<h2>1.19.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1207">#1207</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/0958726939d59e4a5c5a3062190278ffdfde38f5"><code>0958726</code></a>
Thanks <a
href="https://github.com/edmundhung"><code>@​edmundhung</code></a>! -
bump <code>@opennextjs/aws</code> to 3.10.2</p>
<p>See details at <a
href="https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2">https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2</a></p>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1139">#1139</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/79b01b84fd92191517b7a11516c04208f9d474a6"><code>79b01b8</code></a>
Thanks <a
href="https://github.com/james-elicx"><code>@​james-elicx</code></a>! -
Fix Turbopack external module resolution by dynamically discovering
external imports at build time.</p>
<p>When packages are listed in <code>serverExternalPackages</code>,
Turbopack externalizes them via <code>externalImport()</code> which uses
dynamic <code>await import(id)</code>. The bundler (ESBuild) can't
statically analyze <code>import(id)</code> with a variable, so these
modules aren't included in the worker bundle.</p>
<p>This patch:</p>
<ul>
<li>Discovers hashed Turbopack external module mappings from
<code>.next/node_modules/</code> symlinks (e.g.
<code>shiki-43d062b67f27bbdc</code> → <code>shiki</code>)</li>
<li>Scans traced chunk files for bare external imports (e.g.
<code>externalImport(&quot;shiki&quot;)</code>) and subpath imports
(e.g. <code>shiki/engine/javascript</code>)</li>
<li>Generates explicit <code>switch/case</code> entries so the bundler
can statically resolve and include these modules</li>
</ul>
</li>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1203">#1203</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/6f02d12a75a78410711cc0d9db13ab0d41ed903a"><code>6f02d12</code></a>
Thanks <a
href="https://github.com/314systems"><code>@​314systems</code></a>! -
fix: exclude unsupported Next.js 16 releases from peer dependencies.</p>
<p>The previous range allowed Next.js 16.0.0 through 16.2.2 without a
peer dependency warning because <code>&gt;=16.2.3</code> was already
covered by <code>&gt;=15.5.15</code>.</p>
<p>The range now explicitly supports Next.js 15.5.15 and above in the
15.x line, and Next.js 16.2.3 and above in the 16.x line.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/d577521081365c6f9235d32959216f6db5e9268a"><code>d577521</code></a>
Version Packages (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1219">#1219</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/608893e63e1ee16d07c7ec42da979657cf2a62bd"><code>608893e</code></a>
Factor manifest code to reduce the bundle size (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1215">#1215</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/32594d6a921c5ebdbe25f38635bb2c9dabdcbff1"><code>32594d6</code></a>
fix(cli): fail fast in non-TTY environments instead of hanging on
config-crea...</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/f0d022685b24881a142bb01005ff78089be8c8d3"><code>f0d0226</code></a>
remove <code>process.version</code> override now that unenv#493 is
merged (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1218">#1218</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/ac28b08693dacd6c1e38d68863a91dc236cc9677"><code>ac28b08</code></a>
fix: typo (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1217">#1217</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/264d0a0c9cf80d3d8982e0a0a82f823ec2eb3ab5"><code>264d0a0</code></a>
Version Packages (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1201">#1201</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/0958726939d59e4a5c5a3062190278ffdfde38f5"><code>0958726</code></a>
chore: bump <code>@​opennextjs/aws</code> version (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1207">#1207</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/7820ad0a0e5f57aba0580f3cabfdd0caa75cc9bb"><code>7820ad0</code></a>
Reuse sharded tag data on regional cache fill (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1200">#1200</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/585795dbe20fe20d8662addbf9b7be64d82e3184"><code>585795d</code></a>
fix: regression where getEnvFromPlatformProxy received wrong options
type (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1">#1</a>...</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/6f02d12a75a78410711cc0d9db13ab0d41ed903a"><code>6f02d12</code></a>
fix: narrow peerDependencies next range to exclude 16.0.0–16.2.2 (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1203">#1203</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/opennextjs/opennextjs-cloudflare/commits/@opennextjs/cloudflare@1.19.3/packages/cloudflare">compare
view</a></li>
</ul>
</details>
<br />

Updates `@sentry/cloudflare` from 10.41.0 to 10.49.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/getsentry/sentry-javascript/releases"><code>@​sentry/cloudflare</code>'s
releases</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM
structure when an error occurs, providing a snapshot of the page state
for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link
them (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm
invocation, with proper linking between related alarms for better
observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with
<code>enableRpcTracePropagation</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic
trace propagation for Cloudflare RPC calls via <code>.fetch()</code>,
ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI
integrations (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain,
LangGraph) now support an <code>enableTruncation</code> option to
control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor
<code>AsyncLocalStorageContextManager</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally,
reducing external dependencies and ensuring consistent behavior across
environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for
<code>eventLoopBlockIntegration</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on
<code>gen_ai</code> spans (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6
operation name mapping (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from
<code>releaseLock()</code> in streaming (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents
(<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to
prevent memory leak (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/getsentry/sentry-javascript/blob/develop/CHANGELOG.md"><code>@​sentry/cloudflare</code>'s
changelog</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM
structure when an error occurs, providing a snapshot of the page state
for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link
them (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm
invocation, with proper linking between related alarms for better
observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with
<code>enableRpcTracePropagation</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic
trace propagation for Cloudflare RPC calls via <code>.fetch()</code>,
ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI
integrations (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain,
LangGraph) now support an <code>enableTruncation</code> option to
control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor
<code>AsyncLocalStorageContextManager</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally,
reducing external dependencies and ensuring consistent behavior across
environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for
<code>eventLoopBlockIntegration</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on
<code>gen_ai</code> spans (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6
operation name mapping (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from
<code>releaseLock()</code> in streaming (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents
(<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to
prevent memory leak (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/745af797c9e0d10d8b35725694862b1de6f064ae"><code>745af79</code></a>
release: 10.49.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/46dcef1590e8e3a677c74aceed9fa7641cc6e7c3"><code>46dcef1</code></a>
Merge pull request <a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20348">#20348</a>
from getsentry/prepare-release/10.49.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/bf4e188d1dde124677e933922949f0a626661d0a"><code>bf4e188</code></a>
meta(changelog): Update changelog for 10.49.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/5f72df55e5337fc1ba1a8bd70894b55b6a862bab"><code>5f72df5</code></a>
feat(cloudflare): Enable RPC trace propagation with
enableRpcTracePropagation...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/50438f9863e5cb5630459a6b1f967bbc15b0d188"><code>50438f9</code></a>
feat(browser): Emit web vitals as streamed spans (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/19827">#19827</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/3332fecd7aa53f6aca2ed42639f5a3ccc0e8fae5"><code>3332fec</code></a>
fix(opentelemetry): Use WeakRef for context stored on scope to prevent
memory...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/684a41fa4c7d5591be6a2fa7bff2db0ab5a62dbb"><code>684a41f</code></a>
ref(opentelemetry): Replace <code>@opentelemetry/resources</code> with
inline `getSentry...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/8b2a9dce02ee45f5ade7a23fd3ee0f4ae9d39d67"><code>8b2a9dc</code></a>
ci: Remove Docker container for Verdaccio package publishing (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20329">#20329</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/0007c7b81321b659d74641c5587e78f10755f714"><code>0007c7b</code></a>
ci: Extract test names for flaky test issues (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20298">#20298</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/9b9d65c8a4b7018dfc6bcdf0cfd43cb4d3ab2c75"><code>9b9d65c</code></a>
chore(ci): Bump actions/cache to v5 and actions/download-artifact to v7
(<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20249">#20249</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/getsentry/sentry-javascript/compare/10.41.0...10.49.0">compare
view</a></li>
</ul>
</details>
<br />

Updates `@sentry/nextjs` from 10.41.0 to 10.49.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/getsentry/sentry-javascript/releases"><code>@​sentry/nextjs</code>'s
releases</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM
structure when an error occurs, providing a snapshot of the page state
for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link
them (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm
invocation, with proper linking between related alarms for better
observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with
<code>enableRpcTracePropagation</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic
trace propagation for Cloudflare RPC calls via <code>.fetch()</code>,
ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI
integrations (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain,
LangGraph) now support an <code>enableTruncation</code> option to
control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor
<code>AsyncLocalStorageContextManager</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally,
reducing external dependencies and ensuring consistent behavior across
environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for
<code>eventLoopBlockIntegration</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on
<code>gen_ai</code> spans (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6
operation name mapping (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from
<code>releaseLock()</code> in streaming (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents
(<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to
prevent memory leak (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/getsentry/sentry-javascript/blob/develop/CHANGELOG.md"><code>@​sentry/nextjs</code>'s
changelog</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM
structure when an error occurs, providing a snapshot of the page state
for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link
them (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm
invocation, with proper linking between related alarms for better
observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with
<code>enableRpcTracePropagation</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic
trace propagation for Cloudflare RPC calls via <code>.fetch()</code>,
ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI
integrations (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>,
<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain,
LangGraph) now support an <code>enableTruncation</code> option to
control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor
<code>AsyncLocalStorageContextManager</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally,
reducing external dependencies and ensuring consistent behavior across
environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for
<code>eventLoopBlockIntegration</code> (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on
<code>gen_ai</code> spans (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6
operation name mapping (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from
<code>releaseLock()</code> in streaming (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents
(<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to
prevent memory leak (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a
href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/745af797c9e0d10d8b35725694862b1de6f064ae"><code>745af79</code></a>
release: 10.49.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/46dcef1590e8e3a677c74aceed9fa7641cc6e7c3"><code>46dcef1</code></a>
Merge pull request <a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20348">#20348</a>
from getsentry/prepare-release/10.49.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/bf4e188d1dde124677e933922949f0a626661d0a"><code>bf4e188</code></a>
meta(changelog): Update changelog for 10.49.0</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/5f72df55e5337fc1ba1a8bd70894b55b6a862bab"><code>5f72df5</code></a>
feat(cloudflare): Enable RPC trace propagation with
enableRpcTracePropagation...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/50438f9863e5cb5630459a6b1f967bbc15b0d188"><code>50438f9</code></a>
feat(browser): Emit web vitals as streamed spans (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/19827">#19827</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/3332fecd7aa53f6aca2ed42639f5a3ccc0e8fae5"><code>3332fec</code></a>
fix(opentelemetry): Use WeakRef for context stored on scope to prevent
memory...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/684a41fa4c7d5591be6a2fa7bff2db0ab5a62dbb"><code>684a41f</code></a>
ref(opentelemetry): Replace <code>@opentelemetry/resources</code> with
inline `getSentry...</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/8b2a9dce02ee45f5ade7a23fd3ee0f4ae9d39d67"><code>8b2a9dc</code></a>
ci: Remove Docker container for Verdaccio package publishing (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20329">#20329</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/0007c7b81321b659d74641c5587e78f10755f714"><code>0007c7b</code></a>
ci: Extract test names for flaky test issues (<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20298">#20298</a>)</li>
<li><a
href="https://github.com/getsentry/sentry-javascript/commit/9b9d65c8a4b7018dfc6bcdf0cfd43cb4d3ab2c75"><code>9b9d65c</code></a>
chore(ci): Bump actions/cache to v5 and actions/download-artifact to v7
(<a
href="https://redirect.github.com/getsentry/sentry-javascript/issues/20249">#20249</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/getsentry/sentry-javascript/compare/10.41.0...10.49.0">compare
view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query` from 5.96.2 to 5.99.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/releases"><code>@​tanstack/react-query</code>'s
releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/blob/main/packages/react-query/CHANGELOG.md"><code>@​tanstack/react-query</code>'s
changelog</a>.</em></p>
<blockquote>
<h2>5.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2>5.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2>5.99.0</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.99.0</li>
</ul>
</li>
</ul>
<h2>5.98.0</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.98.0</li>
</ul>
</li>
</ul>
<h2>5.97.0</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a
href="https://github.com/TanStack/query/commit/2bfb12cc44f1d8495106136e4ddacb817135f8f9"><code>2bfb12c</code></a>]:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.97.0</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/TanStack/query/commit/a3ec7b30cc4c18b2c5aefe608638ecadce732b81"><code>a3ec7b3</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10520">#10520</a>)</li>
<li><a
href="https://github.com/TanStack/query/commit/69d2757c982f7bd5a483398492fe753f6f574ab8"><code>69d2757</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10514">#10514</a>)</li>
<li><a
href="https://github.com/TanStack/query/commit/7ffa1ed0b01d8c397c379dbb3d85da80b278b21c"><code>7ffa1ed</code></a>
test({react,preact,solid}-query/useQueries): fix test description from
'useQu...</li>
<li><a
href="https://github.com/TanStack/query/commit/bc83d370e8922f1c3126aea4e7757ce8761a06f2"><code>bc83d37</code></a>
test({react,preact}-query/useMutation): unify destructuring pattern in
comple...</li>
<li><a
href="https://github.com/TanStack/query/commit/aad1bd59d8e1ecebf14f556e0d9ca2605b4e4b80"><code>aad1bd5</code></a>
test({react,preact}-query/useMutation): add parallel 'mutateAsync' tests
with...</li>
<li><a
href="https://github.com/TanStack/query/commit/d7643b54fda462492d474695cd35e2549cefa5d7"><code>d7643b5</code></a>
test({react,preact}-query/useMutation): add optimistic update tests with
succ...</li>
<li><a
href="https://github.com/TanStack/query/commit/cd89d6f706bd143382db5ae3807ed8644ec52afe"><code>cd89d6f</code></a>
test({react,preact}-query/useMutation): add conditional handling and
retry te...</li>
<li><a
href="https://github.com/TanStack/query/commit/6e15fe62d2551b5269b21a1522f3c7bd653808ba"><code>6e15fe6</code></a>
test({react,preact}-query/useMutation): add chained 'mutateAsync' tests
for s...</li>
<li><a
href="https://github.com/TanStack/query/commit/792d3a5b32ee90b13f44456bb50518d24e9550d5"><code>792d3a5</code></a>
test({react,preact}-query/useMutation): add callback tests when
'useMutation'...</li>
<li><a
href="https://github.com/TanStack/query/commit/1b661b34ec5d1df00b4b0a2c084efbd486e73899"><code>1b661b3</code></a>
test({react,preact}-query/useMutation): add single callback tests for
'mutate...</li>
<li>Additional commits viewable in <a
href="https://github.com/TanStack/query/commits/@tanstack/react-query@5.99.2/packages/react-query">compare
view</a></li>
</ul>
</details>
<br />

Updates `@xyflow/react` from 12.10.1 to 12.10.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/xyflow/xyflow/releases"><code>@​xyflow/react</code>'s
releases</a>.</em></p>
<blockquote>
<h2><code>@​xyflow/react</code><a
href="https://github.com/12"><code>@​12</code></a>.10.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/xyflow/xyflow/pull/5735">#5735</a> <a
href="https://github.com/xyflow/xyflow/commit/a6c938fb2e5ed030512ef75d665ac80dc3a66bc6"><code>a6c938fb2</code></a>
Thanks <a href="https://github.com/nvie"><code>@​nvie</code></a>! -
Allow <code>type</code> field to be missing in <code>BuiltInNode</code>
(no <code>type</code> field is the same as <code>type:
&quot;default&quot;</code>)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/xyflow/xyflow/pull/5722">#5722</a> <a
href="https://github.com/xyflow/xyflow/commit/8c9b7e726e0bb79871c85017dace0f1ccf1b478c"><code>8c9b7e726</code></a>
Thanks <a href="https://github.com/dfblhmm"><code>@​dfblhmm</code></a>!
- Add <code>snapGrid</code> to <code>screenToFlowPosition</code>
options</p>
</li>
<li>
<p><a
href="https://redirect.github.com/xyflow/xyflow/pull/5723">#5723</a> <a
href="https://github.com/xyflow/xyflow/commit/82249517a3338d7bd0d6d499abecfaa6bca8c339"><code>82249517a</code></a>
Thanks <a href="https://github.com/moklick"><code>@​moklick</code></a>!
- Pass options to useReactFlow/useSvelteFlow viewport helper functions
correctly</p>
</li>
<li>
<p><a
href="https://redirect.github.com/xyflow/xyflow/pull/5733">#5733</a> <a
href="https://github.com/xyflow/xyflow/commit/64115cd086d2c04235f1cae80acb45455fd0de49"><code>64115cd08</code></a>
Thanks <a
href="https://github.com/AlaricBaraou"><code>@​AlaricBaraou</code></a>!
- Fix empty store during ReactFlow remount by reordering StoreUpdater
before GraphView and using layout effects</p>
</li>
<li>
<p><a
href="https://redirect.github.com/xyflow/xyflow/pull/5727">#5727</a> <a
href="https://github.com/xyflow/xyflow/commit/dd54e86b91da29c1f58f646ad9a99f96f0c4a2e5"><code>dd54e86b9</code></a>
Thanks <a
href="https://github.com/solastley"><code>@​solastley</code></a>! -
Ensure visual nodes selection state is cleared when zero selected nodes
remain in the flow</p>
</li>
<li>
<p>Updated dependencies [<a
href="https://github.com/xyflow/xyflow/commit/4a278dbbf942b2bc964e4159347b70ae6617f3dc"><code>4a278dbbf</code></a>]:</p>
<ul>
<li><code>@​xyflow/system</code><a
href="https://github.com/0"><code>@​0</code></a>.0.76</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/xyflow/xyflow/blob/main/packages/react/CHANGELOG.md"><code>@​xyflow/react</code>'s
changelog</a>.</em></p>
<blockquote>
<h2>12.10.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/xyflow/xyflow/pull/5735">#5735</a> <a
href="https://github.com/xyflow/xyflow/commit/a6c938fb2e5ed030512ef75d665ac80dc3a66bc6"><code>a6c938fb2</code></a>
Thanks <a href="https://github.com/nvie"><code>@​nvie</code></a>! -
Allow <code>type</code> field to be missing in <code>BuiltInNode</code>
(no <code>type</code> field is the same as <code>type:
&quot;default&quot;</code>)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/xyflow/xyflow/pull/5722">#5722</a> <a
href="https://github.com/xyflow/xyflow/commit/8c9b7e726e0bb79871c85017dace0f1ccf1b478c"><code>8c9b7e726</code></a>
Thanks <a href="https://github.com/dfblhmm"><code>@​dfblhmm</code></a>!
- Add <code>snapGrid</code> to <code>screenToFlowPosition</code>
options</p>
</li>
<li>
<p><a
href="https://redirect.github.com/xyflow/xyflow/pull/5723">#5723</a> <a
href="https://github.com/xyflow/xyflow/commit/82249517a3338d7bd0d6d499abecfaa6bca8c339"><code>82249517a</code></a>
Thanks <a href="https://github.com/moklick"><code>@​moklick</code></a>!
- Pass options to useReactFlow/useSvelteFlow viewport helper functions
correctly</p>
</li>
<li>
<p><a
href="https://redirect.github.com/xyflow/xyflow/pull/5733">#5733</a> <a
href="https://github.com/xyflow/xyflow/commit/64115cd086d2c04235f1cae80acb45455fd0de49"><code>64115cd08</code></a>
Thanks <a
href="https://github.com/AlaricBaraou"><code>@​AlaricBaraou</code></a>!
- Fix empty store during ReactFlow remount by reordering StoreUpdater
before GraphView and using layout effects</p>
</li>
<li>
<p><a
href="https://redirect.github.com/xyflow/xyflow/pull/5727">#5727</a> <a
href="https://github.com/xyflow/xyflow/commit/dd54e86b91da29c1f58f646ad9a99f96f0c4a2e5"><code>dd54e86b9</code></a>
Thanks <a
href="https://github.com/solastley"><code>@​solastley</code></a>! -
Ensure visual nodes selection state is cleared when zero selected nodes
remain in the flow</p>
</li>
<li>
<p>Updated dependencies [<a
href="https://github.com/xyflow/xyflow/commit/4a278dbbf942b2bc964e4159347b70ae6617f3dc"><code>4a278dbbf</code></a>]:</p>
<ul>
<li><code>@​xyflow/system</code><a
href="https://github.com/0"><code>@​0</code></a>.0.76</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/xyflow/xyflow/commit/ba0a3612fdec69bd3e63046cb25c2b94d30ea672"><code>ba0a361</code></a>
chore(packages): bump</li>
<li><a
href="https://github.com/xyflow/xyflow/commit/613ad309998563c1009397d5312e23f302670554"><code>613ad30</code></a>
Merge pull request <a
href="https://github.com/xyflow/xyflow/tree/HEAD/packages/react/issues/5733">#5733</a>
from AlaricBaraou/fix/store-reset-timing-on-remount</li>
<li><a
href="https://github.com/xyflow/xyflow/commit/a6c938fb2e5ed030512ef75d665ac80dc3a66bc6"><code>a6c938f</code></a>
Explicitly allow missing <code>type</code> field in BuiltInNode type
definition</li>
<li><a
href="https://github.com/xyflow/xyflow/commit…
```

### PR #1163: chore(deps): bump the minor-and-patch group across 1 directory with 21 updates

Bumps the minor-and-patch group with 21 updates in the /web directory:

| Package | From | To |
| --- | --- | --- |
| [@assistant-ui/react](https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react) | `0.12.19` | `0.12.25` |
| [@opennextjs/cloudflare](https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare) | `1.17.1` | `1.19.3` |
| [@sentry/cloudflare](https://github.com/getsentry/sentry-javascript) | `10.41.0` | `10.49.0` |
| [@sentry/nextjs](https://github.com/getsentry/sentry-javascript) | `10.41.0` | `10.49.0` |
| [@tanstack/react-query](https://github.com/TanStack/query/tree/HEAD/packages/react-query) | `5.96.2` | `5.99.2` |
| [@xyflow/react](https://github.com/xyflow/xyflow/tree/HEAD/packages/react) | `12.10.1` | `12.10.2` |
| [dompurify](https://github.com/cure53/DOMPurify) | `3.3.1` | `3.4.1` |
| [mermaid](https://github.com/mermaid-js/mermaid) | `11.13.0` | `11.14.0` |
| [react](https://github.com/facebook/react/tree/HEAD/packages/react) | `19.2.4` | `19.2.5` |
| [react-dom](https://github.com/facebook/react/tree/HEAD/packages/react-dom) | `19.2.4` | `19.2.5` |
| [@eslint/eslintrc](https://github.com/eslint/eslintrc) | `3.3.4` | `3.3.5` |
| [@playwright/test](https://github.com/microsoft/playwright) | `1.58.2` | `1.59.1` |
| [@tailwindcss/postcss](https://github.com/tailwindlabs/tailwindcss/tree/HEAD/packages/@tailwindcss-postcss) | `4.2.1` | `4.2.4` |
| [@vitest/coverage-v8](https://github.com/vitest-dev/vitest/tree/HEAD/packages/coverage-v8) | `4.0.18` | `4.1.5` |
| [@vitest/expect](https://github.com/vitest-dev/vitest/tree/HEAD/packages/expect) | `4.0.18` | `4.1.5` |
| [dotenv](https://github.com/motdotla/dotenv) | `17.3.1` | `17.4.2` |
| [firebase](https://github.com/firebase/firebase-js-sdk) | `12.8.0` | `12.12.1` |
| [knip](https://github.com/webpro-nl/knip/tree/HEAD/packages/knip) | `6.5.0` | `6.6.0` |
| [prettier](https://github.com/prettier/prettier) | `3.8.1` | `3.8.3` |
| [tailwindcss](https://github.com/tailwindlabs/tailwindcss/tree/HEAD/packages/tailwindcss) | `4.2.1` | `4.2.4` |
| [vitest](https://github.com/vitest-dev/vitest/tree/HEAD/packages/vitest) | `4.0.18` | `4.1.5` |


Updates `@assistant-ui/react` from 0.12.19 to 0.12.25
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/assistant-ui/assistant-ui/releases"><code>@​assistant-ui/react</code>'s releases</a>.</em></p>
<blockquote>
<h2><code>@​assistant-ui/react</code><a href="https://github.com/0"><code>@​0</code></a>.12.25</h2>
<h3>Patch Changes</h3>
<ul>
<li>c988db8: chore: update dependencies</li>
<li>Updated dependencies [f20b9ca]</li>
<li>Updated dependencies [c988db8]
<ul>
<li><code>@​assistant-ui/core</code><a href="https://github.com/0"><code>@​0</code></a>.1.14</li>
<li>assistant-stream@0.3.11</li>
<li>assistant-cloud@0.1.26</li>
<li><code>@​assistant-ui/store</code><a href="https://github.com/0"><code>@​0</code></a>.2.7</li>
<li><code>@​assistant-ui/tap</code><a href="https://github.com/0"><code>@​0</code></a>.5.8</li>
</ul>
</li>
</ul>
<h2><code>@​assistant-ui/react</code><a href="https://github.com/0"><code>@​0</code></a>.12.24</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p>42bc640: feat: support edit lineage and startRun in EditComposer send flow</p>
<ul>
<li>Add <code>SendOptions</code> with <code>startRun</code> flag to <code>composer.send()</code></li>
<li>Expose <code>parentId</code> and <code>sourceId</code> on <code>EditComposerState</code></li>
<li>Add <code>EditComposerRuntimeCore</code> interface extending <code>ComposerRuntimeCore</code></li>
<li>Bypass text-unchanged guard when <code>startRun</code> is explicitly set</li>
<li><code>ComposerSendOptions</code> extends <code>SendOptions</code> for consistent layering</li>
</ul>
</li>
<li>
<p>e82726c: fix(react): forward viewport slack props from MessagePrimitive.Root</p>
</li>
<li>
<p>376bb00: chore: update dependencies</p>
</li>
<li>
<p>87e7761: feat: generalize mention system into trigger popover architecture with slash command support</p>
<ul>
<li>Introduce <code>ComposerInputPlugin</code> protocol to decouple ComposerInput from mention-specific code</li>
<li>Extract generic <code>TriggerPopoverResource</code> from <code>MentionResource</code> supporting multiple trigger characters</li>
<li>Add <code>Unstable_TriggerItem</code>, <code>Unstable_TriggerCategory</code>, <code>Unstable_TriggerAdapter</code> generic types</li>
<li>Add <code>Unstable_SlashCommandAdapter</code>, <code>Unstable_SlashCommandItem</code> types</li>
<li>Add <code>ComposerPrimitive.Unstable_TriggerPopoverRoot</code> and related primitives</li>
<li>Add <code>ComposerPrimitive.Unstable_SlashCommandRoot</code> and related primitives</li>
<li>Add <code>unstable_useSlashCommandAdapter</code> hook for building slash command adapters</li>
<li>Refactor <code>MentionResource</code> as thin wrapper around <code>TriggerPopoverResource</code></li>
<li>Alias <code>Unstable_MentionItem</code>/<code>Unstable_MentionAdapter</code> to generic trigger types</li>
<li>Update <code>react-lexical</code> <code>KeyboardPlugin</code> to use plugin protocol</li>
<li>All existing <code>Unstable_Mention*</code> APIs remain unchanged</li>
</ul>
</li>
<li>
<p>Updated dependencies [42bc640]</p>
</li>
<li>
<p>Updated dependencies [376bb00]</p>
</li>
<li>
<p>Updated dependencies [87e7761]</p>
<ul>
<li><code>@​assistant-ui/core</code><a href="https://github.com/0"><code>@​0</code></a>.1.13</li>
<li>assistant-cloud@0.1.25</li>
<li><code>@​assistant-ui/tap</code><a href="https://github.com/0"><code>@​0</code></a>.5.7</li>
</ul>
</li>
</ul>
<h2><code>@​assistant-ui/react</code><a href="https://github.com/0"><code>@​0</code></a>.12.23</h2>
<h3>Patch Changes</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/assistant-ui/assistant-ui/blob/main/packages/react/CHANGELOG.md"><code>@​assistant-ui/react</code>'s changelog</a>.</em></p>
<blockquote>
<h2>0.12.25</h2>
<h3>Patch Changes</h3>
<ul>
<li>c988db8: chore: update dependencies</li>
<li>Updated dependencies [f20b9ca]</li>
<li>Updated dependencies [c988db8]
<ul>
<li><code>@​assistant-ui/core</code><a href="https://github.com/0"><code>@​0</code></a>.1.14</li>
<li>assistant-stream@0.3.11</li>
<li>assistant-cloud@0.1.26</li>
<li><code>@​assistant-ui/store</code><a href="https://github.com/0"><code>@​0</code></a>.2.7</li>
<li><code>@​assistant-ui/tap</code><a href="https://github.com/0"><code>@​0</code></a>.5.8</li>
</ul>
</li>
</ul>
<h2>0.12.24</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p>42bc640: feat: support edit lineage and startRun in EditComposer send flow</p>
<ul>
<li>Add <code>SendOptions</code> with <code>startRun</code> flag to <code>composer.send()</code></li>
<li>Expose <code>parentId</code> and <code>sourceId</code> on <code>EditComposerState</code></li>
<li>Add <code>EditComposerRuntimeCore</code> interface extending <code>ComposerRuntimeCore</code></li>
<li>Bypass text-unchanged guard when <code>startRun</code> is explicitly set</li>
<li><code>ComposerSendOptions</code> extends <code>SendOptions</code> for consistent layering</li>
</ul>
</li>
<li>
<p>e82726c: fix(react): forward viewport slack props from MessagePrimitive.Root</p>
</li>
<li>
<p>376bb00: chore: update dependencies</p>
</li>
<li>
<p>87e7761: feat: generalize mention system into trigger popover architecture with slash command support</p>
<ul>
<li>Introduce <code>ComposerInputPlugin</code> protocol to decouple ComposerInput from mention-specific code</li>
<li>Extract generic <code>TriggerPopoverResource</code> from <code>MentionResource</code> supporting multiple trigger characters</li>
<li>Add <code>Unstable_TriggerItem</code>, <code>Unstable_TriggerCategory</code>, <code>Unstable_TriggerAdapter</code> generic types</li>
<li>Add <code>Unstable_SlashCommandAdapter</code>, <code>Unstable_SlashCommandItem</code> types</li>
<li>Add <code>ComposerPrimitive.Unstable_TriggerPopoverRoot</code> and related primitives</li>
<li>Add <code>ComposerPrimitive.Unstable_SlashCommandRoot</code> and related primitives</li>
<li>Add <code>unstable_useSlashCommandAdapter</code> hook for building slash command adapters</li>
<li>Refactor <code>MentionResource</code> as thin wrapper around <code>TriggerPopoverResource</code></li>
<li>Alias <code>Unstable_MentionItem</code>/<code>Unstable_MentionAdapter</code> to generic trigger types</li>
<li>Update <code>react-lexical</code> <code>KeyboardPlugin</code> to use plugin protocol</li>
<li>All existing <code>Unstable_Mention*</code> APIs remain unchanged</li>
</ul>
</li>
<li>
<p>Updated dependencies [42bc640]</p>
</li>
<li>
<p>Updated dependencies [376bb00]</p>
</li>
<li>
<p>Updated dependencies [87e7761]</p>
<ul>
<li><code>@​assistant-ui/core</code><a href="https://github.com/0"><code>@​0</code></a>.1.13</li>
<li>assistant-cloud@0.1.25</li>
<li><code>@​assistant-ui/tap</code><a href="https://github.com/0"><code>@​0</code></a>.5.7</li>
</ul>
</li>
</ul>
<h2>0.12.23</h2>
<h3>Patch Changes</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/0950c800b72a0ddae37819c336bed3a409415bbf"><code>0950c80</code></a> chore: update versions (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3778">#3778</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/c988db84494aede9eb07548fe1b5266456c53f08"><code>c988db8</code></a> chore: update dependencies (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3809">#3809</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/61833123b3b6cf5ea92caa83e3519e857e44b181"><code>6183312</code></a> chore: update versions (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3772">#3772</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/376bb00f21d90f3866fa7d57f2c3de11015787a9"><code>376bb00</code></a> chore: update dependencies (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3777">#3777</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/e82726cd9ee2ada08487248ca31b54bcd1d4b025"><code>e82726c</code></a> fix(react): forward viewport slack props from MessagePrimitive.Root (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3773">#3773</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/42bc64039d5a020044875bcad3ca2df21ad10009"><code>42bc640</code></a> feat(core): support edit lineage and startRun in EditComposer (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3775">#3775</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/87e7761a81e2aff995829caf904abd3d0a700c54"><code>87e7761</code></a> feat(react): generalize mention into trigger popover with slash command suppo...</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/526890641e899f8b8c328e2895fd825800c5dbc5"><code>5268906</code></a> chore: update versions (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3750">#3750</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/a8bf84bdc07a03a475564fd78eb9152e1ad7c52d"><code>a8bf84b</code></a> feat(core): expose getLoadThreadsPromise on ThreadListRuntime (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3762">#3762</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/ec50e8a67564c4529d75e9707885a4b27751dda6"><code>ec50e8a</code></a> fix(core): prevent resolved history tool calls from re-executing (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3717">#3717</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/assistant-ui/assistant-ui/commits/@assistant-ui/react@0.12.25/packages/react">compare view</a></li>
</ul>
</details>
<br />

Updates `@opennextjs/cloudflare` from 1.17.1 to 1.19.3
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/opennextjs/opennextjs-cloudflare/releases"><code>@​opennextjs/cloudflare</code>'s releases</a>.</em></p>
<blockquote>
<h2><code>@​opennextjs/cloudflare</code><a href="https://github.com/1"><code>@​1</code></a>.19.3</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1215">#1215</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/608893e63e1ee16d07c7ec42da979657cf2a62bd"><code>608893e</code></a> Thanks <a href="https://github.com/vicb"><code>@​vicb</code></a>! - Factor large repeated values in manifests</p>
<p>This reduce the size of the generated code.</p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1218">#1218</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/f0d022685b24881a142bb01005ff78089be8c8d3"><code>f0d0226</code></a> Thanks <a href="https://github.com/314systems"><code>@​314systems</code></a>! - remove <code>process.version</code> override</p>
<p>Remove process.version / process.versions.node overrides now that <a href="https://redirect.github.com/unjs/unenv/pull/493">unjs/unenv#493</a> is merged and shipped in <a href="https://github.com/unjs/unenv/releases/tag/v2.0.0-rc.16">unenv@2.0.0-rc.16</a> (project uses 2.0.0-rc.24)</p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1199">#1199</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/32594d6a921c5ebdbe25f38635bb2c9dabdcbff1"><code>32594d6</code></a> Thanks <a href="https://github.com/SdSadat"><code>@​SdSadat</code></a>! - fix(cli): fail fast in non-TTY environments instead of hanging on config-creation prompts</p>
<p>When <code>open-next.config.ts</code> (or <code>wrangler.(toml|json|jsonc)</code>) is missing, the CLI
prompts the user to auto-create it. In non-TTY environments (Cloudflare Workers
Builds, Docker, CI) the Enquirer prompt can't read stdin, so the build hangs or
fails with a truncated prompt and a cryptic exit code — the user sees
<code>? Missing required open-next.config.ts file, do you want to create one? (Y/n)</code>
and then <code> ELIFECYCLE  Command failed with exit code 13</code>, with no hint at what
to do next.</p>
<p>Now, in non-interactive environments, both prompts throw an actionable error
with the exact template to paste (for <code>open-next.config.ts</code>) or point at the
existing <code>--skipWranglerConfigCheck</code> / <code>SKIP_WRANGLER_CONFIG_CHECK</code> escape
hatch (for the wrangler config). Interactive behavior is unchanged.</p>
</li>
</ul>
<h2><code>@​opennextjs/cloudflare</code><a href="https://github.com/1"><code>@​1</code></a>.19.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1207">#1207</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/0958726939d59e4a5c5a3062190278ffdfde38f5"><code>0958726</code></a> Thanks <a href="https://github.com/edmundhung"><code>@​edmundhung</code></a>! - bump <code>@opennextjs/aws</code> to 3.10.2</p>
<p>See details at <a href="https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2">https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2</a></p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1139">#1139</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/79b01b84fd92191517b7a11516c04208f9d474a6"><code>79b01b8</code></a> Thanks <a href="https://github.com/james-elicx"><code>@​james-elicx</code></a>! - Fix Turbopack external module resolution by dynamically discovering external imports at build time.</p>
<p>When packages are listed in <code>serverExternalPackages</code>, Turbopack externalizes them via <code>externalImport()</code> which uses dynamic <code>await import(id)</code>. The bundler (ESBuild) can't statically analyze <code>import(id)</code> with a variable, so these modules aren't included in the worker bundle.</p>
<p>This patch:</p>
<ul>
<li>Discovers hashed Turbopack external module mappings from <code>.next/node_modules/</code> symlinks (e.g. <code>shiki-43d062b67f27bbdc</code> → <code>shiki</code>)</li>
<li>Scans traced chunk files for bare external imports (e.g. <code>externalImport(&quot;shiki&quot;)</code>) and subpath imports (e.g. <code>shiki/engine/javascript</code>)</li>
<li>Generates explicit <code>switch/case</code> entries so the bundler can statically resolve and include these modules</li>
</ul>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1203">#1203</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/6f02d12a75a78410711cc0d9db13ab0d41ed903a"><code>6f02d12</code></a> Thanks <a href="https://github.com/314systems"><code>@​314systems</code></a>! - fix: exclude unsupported Next.js 16 releases from peer dependencies.</p>
<p>The previous range allowed Next.js 16.0.0 through 16.2.2 without a peer dependency warning because <code>&gt;=16.2.3</code> was already covered by <code>&gt;=15.5.15</code>.</p>
<p>The range now explicitly supports Next.js 15.5.15 and above in the 15.x line, and Next.js 16.2.3 and above in the 16.x line.</p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1200">#1200</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/7820ad0a0e5f57aba0580f3cabfdd0caa75cc9bb"><code>7820ad0</code></a> Thanks <a href="https://github.com/NathanDrake2406"><code>@​NathanDrake2406</code></a>! - fix: reuse sharded tag data when filling the regional cache.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/opennextjs/opennextjs-cloudflare/blob/main/packages/cloudflare/CHANGELOG.md"><code>@​opennextjs/cloudflare</code>'s changelog</a>.</em></p>
<blockquote>
<h2>1.19.3</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1215">#1215</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/608893e63e1ee16d07c7ec42da979657cf2a62bd"><code>608893e</code></a> Thanks <a href="https://github.com/vicb"><code>@​vicb</code></a>! - Factor large repeated values in manifests</p>
<p>This reduce the size of the generated code.</p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1218">#1218</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/f0d022685b24881a142bb01005ff78089be8c8d3"><code>f0d0226</code></a> Thanks <a href="https://github.com/314systems"><code>@​314systems</code></a>! - remove <code>process.version</code> override</p>
<p>Remove process.version / process.versions.node overrides now that <a href="https://redirect.github.com/unjs/unenv/pull/493">unjs/unenv#493</a> is merged and shipped in <a href="https://github.com/unjs/unenv/releases/tag/v2.0.0-rc.16">unenv@2.0.0-rc.16</a> (project uses 2.0.0-rc.24)</p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1199">#1199</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/32594d6a921c5ebdbe25f38635bb2c9dabdcbff1"><code>32594d6</code></a> Thanks <a href="https://github.com/SdSadat"><code>@​SdSadat</code></a>! - fix(cli): fail fast in non-TTY environments instead of hanging on config-creation prompts</p>
<p>When <code>open-next.config.ts</code> (or <code>wrangler.(toml|json|jsonc)</code>) is missing, the CLI
prompts the user to auto-create it. In non-TTY environments (Cloudflare Workers
Builds, Docker, CI) the Enquirer prompt can't read stdin, so the build hangs or
fails with a truncated prompt and a cryptic exit code — the user sees
<code>? Missing required open-next.config.ts file, do you want to create one? (Y/n)</code>
and then <code> ELIFECYCLE  Command failed with exit code 13</code>, with no hint at what
to do next.</p>
<p>Now, in non-interactive environments, both prompts throw an actionable error
with the exact template to paste (for <code>open-next.config.ts</code>) or point at the
existing <code>--skipWranglerConfigCheck</code> / <code>SKIP_WRANGLER_CONFIG_CHECK</code> escape
hatch (for the wrangler config). Interactive behavior is unchanged.</p>
</li>
</ul>
<h2>1.19.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1207">#1207</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/0958726939d59e4a5c5a3062190278ffdfde38f5"><code>0958726</code></a> Thanks <a href="https://github.com/edmundhung"><code>@​edmundhung</code></a>! - bump <code>@opennextjs/aws</code> to 3.10.2</p>
<p>See details at <a href="https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2">https://github.com/opennextjs/opennextjs-aws/releases/tag/v3.10.2</a></p>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1139">#1139</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/79b01b84fd92191517b7a11516c04208f9d474a6"><code>79b01b8</code></a> Thanks <a href="https://github.com/james-elicx"><code>@​james-elicx</code></a>! - Fix Turbopack external module resolution by dynamically discovering external imports at build time.</p>
<p>When packages are listed in <code>serverExternalPackages</code>, Turbopack externalizes them via <code>externalImport()</code> which uses dynamic <code>await import(id)</code>. The bundler (ESBuild) can't statically analyze <code>import(id)</code> with a variable, so these modules aren't included in the worker bundle.</p>
<p>This patch:</p>
<ul>
<li>Discovers hashed Turbopack external module mappings from <code>.next/node_modules/</code> symlinks (e.g. <code>shiki-43d062b67f27bbdc</code> → <code>shiki</code>)</li>
<li>Scans traced chunk files for bare external imports (e.g. <code>externalImport(&quot;shiki&quot;)</code>) and subpath imports (e.g. <code>shiki/engine/javascript</code>)</li>
<li>Generates explicit <code>switch/case</code> entries so the bundler can statically resolve and include these modules</li>
</ul>
</li>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1203">#1203</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/6f02d12a75a78410711cc0d9db13ab0d41ed903a"><code>6f02d12</code></a> Thanks <a href="https://github.com/314systems"><code>@​314systems</code></a>! - fix: exclude unsupported Next.js 16 releases from peer dependencies.</p>
<p>The previous range allowed Next.js 16.0.0 through 16.2.2 without a peer dependency warning because <code>&gt;=16.2.3</code> was already covered by <code>&gt;=15.5.15</code>.</p>
<p>The range now explicitly supports Next.js 15.5.15 and above in the 15.x line, and Next.js 16.2.3 and above in the 16.x line.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/d577521081365c6f9235d32959216f6db5e9268a"><code>d577521</code></a> Version Packages (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1219">#1219</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/608893e63e1ee16d07c7ec42da979657cf2a62bd"><code>608893e</code></a> Factor manifest code to reduce the bundle size (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1215">#1215</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/32594d6a921c5ebdbe25f38635bb2c9dabdcbff1"><code>32594d6</code></a> fix(cli): fail fast in non-TTY environments instead of hanging on config-crea...</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/f0d022685b24881a142bb01005ff78089be8c8d3"><code>f0d0226</code></a> remove <code>process.version</code> override now that unenv#493 is merged (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1218">#1218</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/ac28b08693dacd6c1e38d68863a91dc236cc9677"><code>ac28b08</code></a> fix: typo (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1217">#1217</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/264d0a0c9cf80d3d8982e0a0a82f823ec2eb3ab5"><code>264d0a0</code></a> Version Packages (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1201">#1201</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/0958726939d59e4a5c5a3062190278ffdfde38f5"><code>0958726</code></a> chore: bump <code>@​opennextjs/aws</code> version (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1207">#1207</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/7820ad0a0e5f57aba0580f3cabfdd0caa75cc9bb"><code>7820ad0</code></a> Reuse sharded tag data on regional cache fill (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1200">#1200</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/585795dbe20fe20d8662addbf9b7be64d82e3184"><code>585795d</code></a> fix: regression where getEnvFromPlatformProxy received wrong options type (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1">#1</a>...</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/6f02d12a75a78410711cc0d9db13ab0d41ed903a"><code>6f02d12</code></a> fix: narrow peerDependencies next range to exclude 16.0.0–16.2.2 (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1203">#1203</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/opennextjs/opennextjs-cloudflare/commits/@opennextjs/cloudflare@1.19.3/packages/cloudflare">compare view</a></li>
</ul>
</details>
<br />

Updates `@sentry/cloudflare` from 10.41.0 to 10.49.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/getsentry/sentry-javascript/releases"><code>@​sentry/cloudflare</code>'s releases</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM structure when an error occurs, providing a snapshot of the page state for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link them (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm invocation, with proper linking between related alarms for better observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with <code>enableRpcTracePropagation</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic trace propagation for Cloudflare RPC calls via <code>.fetch()</code>, ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI integrations (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain, LangGraph) now support an <code>enableTruncation</code> option to control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor <code>AsyncLocalStorageContextManager</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally, reducing external dependencies and ensuring consistent behavior across environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for <code>eventLoopBlockIntegration</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on <code>gen_ai</code> spans (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6 operation name mapping (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from <code>releaseLock()</code> in streaming (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to prevent memory leak (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/getsentry/sentry-javascript/blob/develop/CHANGELOG.md"><code>@​sentry/cloudflare</code>'s changelog</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM structure when an error occurs, providing a snapshot of the page state for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link them (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm invocation, with proper linking between related alarms for better observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with <code>enableRpcTracePropagation</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic trace propagation for Cloudflare RPC calls via <code>.fetch()</code>, ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI integrations (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain, LangGraph) now support an <code>enableTruncation</code> option to control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor <code>AsyncLocalStorageContextManager</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally, reducing external dependencies and ensuring consistent behavior across environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for <code>eventLoopBlockIntegration</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on <code>gen_ai</code> spans (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6 operation name mapping (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from <code>releaseLock()</code> in streaming (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to prevent memory leak (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/745af797c9e0d10d8b35725694862b1de6f064ae"><code>745af79</code></a> release: 10.49.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/46dcef1590e8e3a677c74aceed9fa7641cc6e7c3"><code>46dcef1</code></a> Merge pull request <a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20348">#20348</a> from getsentry/prepare-release/10.49.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/bf4e188d1dde124677e933922949f0a626661d0a"><code>bf4e188</code></a> meta(changelog): Update changelog for 10.49.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/5f72df55e5337fc1ba1a8bd70894b55b6a862bab"><code>5f72df5</code></a> feat(cloudflare): Enable RPC trace propagation with enableRpcTracePropagation...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/50438f9863e5cb5630459a6b1f967bbc15b0d188"><code>50438f9</code></a> feat(browser): Emit web vitals as streamed spans (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/19827">#19827</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/3332fecd7aa53f6aca2ed42639f5a3ccc0e8fae5"><code>3332fec</code></a> fix(opentelemetry): Use WeakRef for context stored on scope to prevent memory...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/684a41fa4c7d5591be6a2fa7bff2db0ab5a62dbb"><code>684a41f</code></a> ref(opentelemetry): Replace <code>@opentelemetry/resources</code> with inline `getSentry...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/8b2a9dce02ee45f5ade7a23fd3ee0f4ae9d39d67"><code>8b2a9dc</code></a> ci: Remove Docker container for Verdaccio package publishing (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20329">#20329</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/0007c7b81321b659d74641c5587e78f10755f714"><code>0007c7b</code></a> ci: Extract test names for flaky test issues (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20298">#20298</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/9b9d65c8a4b7018dfc6bcdf0cfd43cb4d3ab2c75"><code>9b9d65c</code></a> chore(ci): Bump actions/cache to v5 and actions/download-artifact to v7 (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20249">#20249</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/getsentry/sentry-javascript/compare/10.41.0...10.49.0">compare view</a></li>
</ul>
</details>
<br />

Updates `@sentry/nextjs` from 10.41.0 to 10.49.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/getsentry/sentry-javascript/releases"><code>@​sentry/nextjs</code>'s releases</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM structure when an error occurs, providing a snapshot of the page state for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link them (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm invocation, with proper linking between related alarms for better observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with <code>enableRpcTracePropagation</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic trace propagation for Cloudflare RPC calls via <code>.fetch()</code>, ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI integrations (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain, LangGraph) now support an <code>enableTruncation</code> option to control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor <code>AsyncLocalStorageContextManager</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally, reducing external dependencies and ensuring consistent behavior across environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for <code>eventLoopBlockIntegration</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on <code>gen_ai</code> spans (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6 operation name mapping (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from <code>releaseLock()</code> in streaming (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to prevent memory leak (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/getsentry/sentry-javascript/blob/develop/CHANGELOG.md"><code>@​sentry/nextjs</code>'s changelog</a>.</em></p>
<blockquote>
<h2>10.49.0</h2>
<h3>Important Changes</h3>
<ul>
<li>
<p><strong>feat(browser): Add View Hierarchy integration (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/14981">#14981</a>)</strong></p>
<p>A new <code>viewHierarchyIntegration</code> captures the DOM structure when an error occurs, providing a snapshot of the page state for debugging. Enable it in your Sentry configuration:</p>
<pre lang="javascript"><code>import * as Sentry from '@sentry/browser';
<p>Sentry.init({
dsn: '<strong>DSN</strong>',
integrations: [Sentry.viewHierarchyIntegration()],
});
</code></pre></p>
</li>
<li>
<p><strong>feat(cloudflare): Split alarms into multiple traces and link them (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19373">#19373</a>)</strong></p>
<p>Durable Object alarms now create separate traces for each alarm invocation, with proper linking between related alarms for better observability.</p>
</li>
<li>
<p><strong>feat(cloudflare): Enable RPC trace propagation with <code>enableRpcTracePropagation</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/19991">#19991</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20345">#20345</a>)</strong></p>
<p>A new <code>enableRpcTracePropagation</code> option enables automatic trace propagation for Cloudflare RPC calls via <code>.fetch()</code>, ensuring distributed traces flow correctly across service bindings.</p>
</li>
<li>
<p><strong>feat(core): Add <code>enableTruncation</code> option to AI integrations (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20167">#20167</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20181">#20181</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20182">#20182</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20183">#20183</a>, <a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20184">#20184</a>)</strong></p>
<p>All AI integrations (OpenAI, Anthropic, Google GenAI, LangChain, LangGraph) now support an <code>enableTruncation</code> option to control whether large AI inputs/outputs are truncated.</p>
</li>
<li>
<p><strong>feat(opentelemetry): Vendor <code>AsyncLocalStorageContextManager</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20243">#20243</a>)</strong></p>
<p>The OpenTelemetry context manager is now vendored internally, reducing external dependencies and ensuring consistent behavior across environments.</p>
</li>
</ul>
<h3>Other Changes</h3>
<ul>
<li>feat(core): Export a reusable function to add tracing headers (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20076">#20076</a>)</li>
<li>feat(core): Expose <code>rewriteSources</code> top level option (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20142">#20142</a>)</li>
<li>feat(deps): bump defu from 6.1.4 to 6.1.6 (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20104">#20104</a>)</li>
<li>feat(node-native): Add support for V8 v14 (Node v25+) (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20125">#20125</a>)</li>
<li>feat(node): Include global scope for <code>eventLoopBlockIntegration</code> (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20108">#20108</a>)</li>
<li>fix(core, node): Support loading Express options lazily (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20211">#20211</a>)</li>
<li>fix(core): Set <code>conversation_id</code> only on <code>gen_ai</code> spans (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20274">#20274</a>)</li>
<li>fix(core): Use <code>ai.operationId</code> for Vercel AI V6 operation name mapping (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20285">#20285</a>)</li>
<li>fix(deno): Avoid inferring invalid span op from Deno tracer (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20128">#20128</a>)</li>
<li>fix(deno): Handle <code>reader.closed</code> rejection from <code>releaseLock()</code> in streaming (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20187">#20187</a>)</li>
<li>fix(nextjs): Preserve directive prologues in turbopack loaders (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20103">#20103</a>)</li>
<li>fix(nextjs): Skip custom browser tracing setup for bot user agents (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20263">#20263</a>)</li>
<li>fix(opentelemetry): Use WeakRef for context stored on scope to prevent memory leak (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20328">#20328</a>)</li>
<li>fix(replay): Use live click attributes in breadcrumbs (<a href="https://redirect.github.com/getsentry/sentry-javascript/pull/20262">#20262</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/745af797c9e0d10d8b35725694862b1de6f064ae"><code>745af79</code></a> release: 10.49.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/46dcef1590e8e3a677c74aceed9fa7641cc6e7c3"><code>46dcef1</code></a> Merge pull request <a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20348">#20348</a> from getsentry/prepare-release/10.49.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/bf4e188d1dde124677e933922949f0a626661d0a"><code>bf4e188</code></a> meta(changelog): Update changelog for 10.49.0</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/5f72df55e5337fc1ba1a8bd70894b55b6a862bab"><code>5f72df5</code></a> feat(cloudflare): Enable RPC trace propagation with enableRpcTracePropagation...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/50438f9863e5cb5630459a6b1f967bbc15b0d188"><code>50438f9</code></a> feat(browser): Emit web vitals as streamed spans (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/19827">#19827</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/3332fecd7aa53f6aca2ed42639f5a3ccc0e8fae5"><code>3332fec</code></a> fix(opentelemetry): Use WeakRef for context stored on scope to prevent memory...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/684a41fa4c7d5591be6a2fa7bff2db0ab5a62dbb"><code>684a41f</code></a> ref(opentelemetry): Replace <code>@opentelemetry/resources</code> with inline `getSentry...</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/8b2a9dce02ee45f5ade7a23fd3ee0f4ae9d39d67"><code>8b2a9dc</code></a> ci: Remove Docker container for Verdaccio package publishing (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20329">#20329</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/0007c7b81321b659d74641c5587e78f10755f714"><code>0007c7b</code></a> ci: Extract test names for flaky test issues (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20298">#20298</a>)</li>
<li><a href="https://github.com/getsentry/sentry-javascript/commit/9b9d65c8a4b7018dfc6bcdf0cfd43cb4d3ab2c75"><code>9b9d65c</code></a> chore(ci): Bump actions/cache to v5 and actions/download-artifact to v7 (<a href="https://redirect.github.com/getsentry/sentry-javascript/issues/20249">#20249</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/getsentry/sentry-javascript/compare/10.41.0...10.49.0">compare view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query` from 5.96.2 to 5.99.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/releases"><code>@​tanstack/react-query</code>'s releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/blob/main/packages/react-query/CHANGELOG.md"><code>@​tanstack/react-query</code>'s changelog</a>.</em></p>
<blockquote>
<h2>5.99.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.99.2</li>
</ul>
</li>
</ul>
<h2>5.99.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.99.1</li>
</ul>
</li>
</ul>
<h2>5.99.0</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.99.0</li>
</ul>
</li>
</ul>
<h2>5.98.0</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.98.0</li>
</ul>
</li>
</ul>
<h2>5.97.0</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a href="https://github.com/TanStack/query/commit/2bfb12cc44f1d8495106136e4ddacb817135f8f9"><code>2bfb12c</code></a>]:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.97.0</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/TanStack/query/commit/a3ec7b30cc4c18b2c5aefe608638ecadce732b81"><code>a3ec7b3</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10520">#10520</a>)</li>
<li><a href="https://github.com/TanStack/query/commit/69d2757c982f7bd5a483398492fe753f6f574ab8"><code>69d2757</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10514">#10514</a>)</li>
<li><a href="https://github.com/TanStack/query/commit/7ffa1ed0b01d8c397c379dbb3d85da80b278b21c"><code>7ffa1ed</code></a> test({react,preact,solid}-query/useQueries): fix test description from 'useQu...</li>
<li><a href="https://github.com/TanStack/query/commit/bc83d370e8922f1c3126aea4e7757ce8761a06f2"><code>bc83d37</code></a> test({react,preact}-query/useMutation): unify destructuring pattern in comple...</li>
<li><a href="https://github.com/TanStack/query/commit/aad1bd59d8e1ecebf14f556e0d9ca2605b4e4b80"><code>aad1bd5</code></a> test({react,preact}-query/useMutation): add parallel 'mutateAsync' tests with...</li>
<li><a href="https://github.com/TanStack/query/commit/d7643b54fda462492d474695cd35e2549cefa5d7"><code>d7643b5</code></a> test({react,preact}-query/useMutation): add optimistic update tests with succ...</li>
<li><a href="https://github.com/TanStack/query/commit/cd89d6f706bd143382db5ae3807ed8644ec52afe"><code>cd89d6f</code></a> test({react,preact}-query/useMutation): add conditional handling and retry te...</li>
<li><a href="https://github.com/TanStack/query/commit/6e15fe62d2551b5269b21a1522f3c7bd653808ba"><code>6e15fe6</code></a> test({react,preact}-query/useMutation): add chained 'mutateAsync' tests for s...</li>
<li><a href="https://github.com/TanStack/query/commit/792d3a5b32ee90b13f44456bb50518d24e9550d5"><code>792d3a5</code></a> test({react,preact}-query/useMutation): add callback tests when 'useMutation'...</li>
<li><a href="https://github.com/TanStack/query/commit/1b661b34ec5d1df00b4b0a2c084efbd486e73899"><code>1b661b3</code></a> test({react,preact}-query/useMutation): add single callback tests for 'mutate...</li>
<li>Additional commits viewable in <a href="https://github.com/TanStack/query/commits/@tanstack/react-query@5.99.2/packages/react-query">compare view</a></li>
</ul>
</details>
<br />

Updates `@xyflow/react` from 12.10.1 to 12.10.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/xyflow/xyflow/releases"><code>@​xyflow/react</code>'s releases</a>.</em></p>
<blockquote>
<h2><code>@​xyflow/react</code><a href="https://github.com/12"><code>@​12</code></a>.10.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/xyflow/xyflow/pull/5735">#5735</a> <a href="https://github.com/xyflow/xyflow/commit/a6c938fb2e5ed030512ef75d665ac80dc3a66bc6"><code>a6c938fb2</code></a> Thanks <a href="https://github.com/nvie"><code>@​nvie</code></a>! - Allow <code>type</code> field to be missing in <code>BuiltInNode</code> (no <code>type</code> field is the same as <code>type: &quot;default&quot;</code>)</p>
</li>
<li>
<p><a href="https://redirect.github.com/xyflow/xyflow/pull/5722">#5722</a> <a href="https://github.com/xyflow/xyflow/commit/8c9b7e726e0bb79871c85017dace0f1ccf1b478c"><code>8c9b7e726</code></a> Thanks <a href="https://github.com/dfblhmm"><code>@​dfblhmm</code></a>! - Add <code>snapGrid</code> to <code>screenToFlowPosition</code> options</p>
</li>
<li>
<p><a href="https://redirect.github.com/xyflow/xyflow/pull/5723">#5723</a> <a href="https://github.com/xyflow/xyflow/commit/82249517a3338d7bd0d6d499abecfaa6bca8c339"><code>82249517a</code></a> Thanks <a href="https://github.com/moklick"><code>@​moklick</code></a>! - Pass options to useReactFlow/useSvelteFlow viewport helper functions correctly</p>
</li>
<li>
<p><a href="https://redirect.github.com/xyflow/xyflow/pull/5733">#5733</a> <a href="https://github.com/xyflow/xyflow/commit/64115cd086d2c04235f1cae80acb45455fd0de49"><code>64115cd08</code></a> Thanks <a href="https://github.com/AlaricBaraou"><code>@​AlaricBaraou</code></a>! - Fix empty store during ReactFlow remount by reordering StoreUpdater before GraphView and using layout effects</p>
</li>
<li>
<p><a href="https://redirect.github.com/xyflow/xyflow/pull/5727">#5727</a> <a href="https://github.com/xyflow/xyflow/commit/dd54e86b91da29c1f58f646ad9a99f96f0c4a2e5"><code>dd54e86b9</code></a> Thanks <a href="https://github.com/solastley"><code>@​solastley</code></a>! - Ensure visual nodes selection state is cleared when zero selected nodes remain in the flow</p>
</li>
<li>
<p>Updated dependencies [<a href="https://github.com/xyflow/xyflow/commit/4a278dbbf942b2bc964e4159347b70ae6617f3dc"><code>4a278dbbf</code></a>]:</p>
<ul>
<li><code>@​xyflow/system</code><a href="https://github.com/0"><code>@​0</code></a>.0.76</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/xyflow/xyflow/blob/main/packages/react/CHANGELOG.md"><code>@​xyflow/react</code>'s changelog</a>.</em></p>
<blockquote>
<h2>12.10.2</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/xyflow/xyflow/pull/5735">#5735</a> <a href="https://github.com/xyflow/xyflow/commit/a6c938fb2e5ed030512ef75d665ac80dc3a66bc6"><code>a6c938fb2</code></a> Thanks <a href="https://github.com/nvie"><code>@​nvie</code></a>! - Allow <code>type</code> field to be missing in <code>BuiltInNode</code> (no <code>type</code> field is the same as <code>type: &quot;default&quot;</code>)</p>
</li>
<li>
<p><a href="https://redirect.github.com/xyflow/xyflow/pull/5722">#5722</a> <a href="https://github.com/xyflow/xyflow/commit/8c9b7e726e0bb79871c85017dace0f1ccf1b478c"><code>8c9b7e726</code></a> Thanks <a href="https://github.com/dfblhmm"><code>@​dfblhmm</code></a>! - Add <code>snapGrid</code> to <code>screenToFlowPosition</code> options</p>
</li>
<li>
<p><a href="https://redirect.github.com/xyflow/xyflow/pull/5723">#5723</a> <a href="https://github.com/xyflow/xyflow/commit/82249517a3338d7bd0d6d499abecfaa6bca8c339"><code>82249517a</code></a> Thanks <a href="https://github.com/moklick"><code>@​moklick</code></a>! - Pass options to useReactFlow/useSvelteFlow viewport helper functions correctly</p>
</li>
<li>
<p><a href="https://redirect.github.com/xyflow/xyflow/pull/5733">#5733</a> <a href="https://github.com/xyflow/xyflow/commit/64115cd086d2c04235f1cae80acb45455fd0de49"><code>64115cd08</code></a> Thanks <a href="https://github.com/AlaricBaraou"><code>@​AlaricBaraou</code></a>! - Fix empty store during ReactFlow remount by reordering StoreUpdater before GraphView and using layout effects</p>
</li>
<li>
<p><a href="https://redirect.github.com/xyflow/xyflow/pull/5727">#5727</a> <a href="https://github.com/xyflow/xyflow/commit/dd54e86b91da29c1f58f646ad9a99f96f0c4a2e5"><code>dd54e86b9</code></a> Thanks <a href="https://github.com/solastley"><code>@​solastley</code></a>! - Ensure visual nodes selection state is cleared when zero selected nodes remain in the flow</p>
</li>
<li>
<p>Updated dependencies [<a href="https://github.com/xyflow/xyflow/commit/4a278dbbf942b2bc964e4159347b70ae6617f3dc"><code>4a278dbbf</code></a>]:</p>
<ul>
<li><code>@​xyflow/system</code><a href="https://github.com/0"><code>@​0</code></a>.0.76</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/xyflow/xyflow/commit/ba0a3612fdec69bd3e63046cb25c2b94d30ea672"><code>ba0a361</code></a> chore(packages): bump</li>
<li><a href="https://github.com/xyflow/xyflow/commit/613ad309998563c1009397d5312e23f302670554"><code>613ad30</code></a> Merge pull request <a href="https://github.com/xyflow/xyflow/tree/HEAD/packages/react/issues/5733">#5733</a> from AlaricBaraou/fix/store-reset-timing-on-remount</li>
<li><a href="https://github.com/xyflow/xyflow/commit/a6c938fb2e5ed030512ef75d665ac80dc3a66bc6"><code>a6c938f</code></a> Explicitly allow missing <code>type</code> field in BuiltInNode type definition</li>
<li><a href="https://github.com/xyflow/xyflow/commit/f2831bdf31ae4cd1c19eaa2bda6617f3d651f88a"><code>f2831bd</code></a> Merge pull request <a href="https://github.com/xyflow/xyflow/tree/HEAD/packages/react/issues/5727">#5727</a> from unifygtm/clear-nodes-selection-active</li>
<li><a href="https://github.com/xyflow/xyflow/commit/0e48d846fa6e10ac7eed4...

_Description has been truncated_

### Human Comments
- **chris-srp** (2026-04-22T07:22:48Z): Pushed [9f4c4c6](https://github.com/SerendipityOneInc/ecap-workspace/commit/9f4c4c63f) to regenerate `pnpm-lock.yaml` and partially revert the grouped bump.

**Root cause**: dependabot bumped 21 packages in `web/package.json` but didn't regenerate `pnpm-lock.yaml`, so `pnpm install --frozen-lockfile` in web-quality CI failed with `ERR_PNPM_OUTDATED_LOCKFILE` (19 mismatched specifiers). Regenerating triggered pnpm's `minimumReleaseAge: 10080` (7-day) supply-chain guard from #1158 — 12 of the 21 target versions were published in the last 7 days and got rejected.

**Fix**: keep 9 mature bumps (published >=2026-04-15), revert 12 too-new ones to their original versions. Dependabot will retry the deferred bumps on next weekly cycle once the packages age past the 7-day threshold.

| Status | Packages |
|---|---|
| Kept (mature) | `@assistant-ui/react` `^0.12.25` · `@xyflow/react` `^12.10.2` · `mermaid` `^11.14.0` · `react` / `react-dom` `^19.2.5` · `@eslint/eslintrc` `^3.3.5` · `@playwright/test` `^1.59.1` · `dotenv` `^17.4.2` · `prettier` `^3.8.3` |
| Reverted (too new, <7d old) | `@opennextjs/cloudflare` · `@sentry/cloudflare` · `@sentry/nextjs` · `@tanstack/react-query` · `dompurify` · `@tailwindcss/postcss` · `@vitest/coverage-v8` · `@vitest/expect` · `firebase` · `knip` · `tailwindcss` · `vitest` |

Locally verified: `pnpm install --frozen-lockfile` now succeeds against the regenerated `pnpm-lock.yaml`.

---

## c0271de

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T07:18:16Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/c0271de19d546f4b8e0de932d195270e22e618dc](https://github.com/SerendipityOneInc/ecap-workspace/commit/c0271de19d546f4b8e0de932d195270e22e618dc)

### Commit Message
```
ci: iOS DerivedData cache + weekly rotation + asset-size-guard narrowing (#1175)

## Summary

Phase 2 Merge-queue 加速 PR 合订本，3 个 commit：

### 1. iOS DerivedData + Homebrew cache (commit 1)
- 新增 `~/Library/Caches/Homebrew/downloads` cache：swiftlint + xcbeautify
不再每次重下载（~6-8s/run）
- 把原 SourcePackages-only cache 扩到整个 `$DERIVED_DATA`，覆盖
Build/Intermediates.noindex（增量编译对象文件）+ ModuleCache.noindex（Swift 模块预编译头）

### 2. DerivedData cache rotation 改为 ISO 周 bucket (commit 2)
- 原本 key 里带 `github.run_id` 每次 run 生成新 cache entry。DerivedData 1-3GB × 每
run × 多 PR 并发 → 挤占 10GB repo cache 配额，会把 web/python 的小 cache 都 LRU 掉
- 改成 `$(date -u +%G-W%V)` 周 bucket：同一周内 exact-key hit 不 save；周滚动时 save
一次新 cache；restore-keys 仍然从旧周 + 旧 Package.resolved hash 降级 seed
- Cache write 频率从 ~N/run 压到 ~1/week/(OS × Package.resolved) 组合

### 3. asset-size-guard paths-filter 窄化 (commit 3)
- 数据：最近 5 次 merge_group 的 asset-size-guard 都是 44-49s，其中 38s 是 pnpm
install + Node setup，**actual check step 0s**（大部分 PR 压根没动 asset 文件，node
脚本瞬间返回）
- 给 `changes` job 加独立的 `assets` 过滤器（匹配 `scripts/check-asset-size.mjs` 里的
ASSET_PREFIXES：`web/public/**`,
`ios/ZooClaw/ZooClaw/Assets.xcassets/**`）
- 把 asset-size-guard 触发条件从 `web || ios` 窄化成 `assets`
- 预计 ~80%+ 非 asset 的 web/iOS PR 直接 skip 这个 job，每次省 44s

## 预期收益

| 场景 | Phase 1 后 baseline | 本 PR 后 |
|---|---|---|
| ios-quality (cache miss) | 411s | ~411s（首次没 cache hit） |
| ios-quality (cache hit) | N/A | ~310-340s（估 -20-25%） |
| asset-size-guard (80%+ PRs) | 44s | **0s (skipped)** |
| asset-size-guard (asset PRs) | 44s | 44s（不变） |

对非 iOS 非 asset 的常规 PR（占绝大多数），merge queue 关键路径直接砍掉 44s asset-size-guard。

## 验证策略

- `ios-quality` 默认 paths-filter 只在 `ios/**` 改动时触发——本 PR 只改 workflow 所以
CI 里 ios-quality 会 skip
- 合并后我会 `gh workflow run code-quality.yml --ref main` 触发
workflow_dispatch（所有 job 强制跑），拿冷启动 baseline
- 再触发一次拿 warm cache 数据，对比 Build for testing step 耗时
- asset-size-guard 的 skip 行为：本 PR CI 里应该是 skipped，因为只改 workflow 不改 asset

## 下一步（视实测数据）

- 若 ios-quality warm cache 稳定 < 350s：Phase 2 基本收工
- 若仍 > 400s：提新 PR 升级 `macos-15` → `macos-15-xlarge`（+100% 成本，-100-150s）
- UT + BDD 拆分 + lint-and-typecheck 拆 pyright 的方案（涉及 srp-actions 改造），单独评估

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1175: ci: iOS DerivedData cache + weekly rotation + asset-size-guard narrowing

## Summary

Phase 2 Merge-queue 加速 PR 合订本，3 个 commit：

### 1. iOS DerivedData + Homebrew cache (commit 1)
- 新增 `~/Library/Caches/Homebrew/downloads` cache：swiftlint + xcbeautify 不再每次重下载（~6-8s/run）
- 把原 SourcePackages-only cache 扩到整个 `$DERIVED_DATA`，覆盖 Build/Intermediates.noindex（增量编译对象文件）+ ModuleCache.noindex（Swift 模块预编译头）

### 2. DerivedData cache rotation 改为 ISO 周 bucket (commit 2)
- 原本 key 里带 `github.run_id` 每次 run 生成新 cache entry。DerivedData 1-3GB × 每 run × 多 PR 并发 → 挤占 10GB repo cache 配额，会把 web/python 的小 cache 都 LRU 掉
- 改成 `$(date -u +%G-W%V)` 周 bucket：同一周内 exact-key hit 不 save；周滚动时 save 一次新 cache；restore-keys 仍然从旧周 + 旧 Package.resolved hash 降级 seed
- Cache write 频率从 ~N/run 压到 ~1/week/(OS × Package.resolved) 组合

### 3. asset-size-guard paths-filter 窄化 (commit 3)
- 数据：最近 5 次 merge_group 的 asset-size-guard 都是 44-49s，其中 38s 是 pnpm install + Node setup，**actual check step 0s**（大部分 PR 压根没动 asset 文件，node 脚本瞬间返回）
- 给 `changes` job 加独立的 `assets` 过滤器（匹配 `scripts/check-asset-size.mjs` 里的 ASSET_PREFIXES：`web/public/**`, `ios/ZooClaw/ZooClaw/Assets.xcassets/**`）
- 把 asset-size-guard 触发条件从 `web || ios` 窄化成 `assets`
- 预计 ~80%+ 非 asset 的 web/iOS PR 直接 skip 这个 job，每次省 44s

## 预期收益

| 场景 | Phase 1 后 baseline | 本 PR 后 |
|---|---|---|
| ios-quality (cache miss) | 411s | ~411s（首次没 cache hit） |
| ios-quality (cache hit) | N/A | ~310-340s（估 -20-25%） |
| asset-size-guard (80%+ PRs) | 44s | **0s (skipped)** |
| asset-size-guard (asset PRs) | 44s | 44s（不变） |

对非 iOS 非 asset 的常规 PR（占绝大多数），merge queue 关键路径直接砍掉 44s asset-size-guard。

## 验证策略

- `ios-quality` 默认 paths-filter 只在 `ios/**` 改动时触发——本 PR 只改 workflow 所以 CI 里 ios-quality 会 skip
- 合并后我会 `gh workflow run code-quality.yml --ref main` 触发 workflow_dispatch（所有 job 强制跑），拿冷启动 baseline
- 再触发一次拿 warm cache 数据，对比 Build for testing step 耗时
- asset-size-guard 的 skip 行为：本 PR CI 里应该是 skipped，因为只改 workflow 不改 asset

## 下一步（视实测数据）

- 若 ios-quality warm cache 稳定 < 350s：Phase 2 基本收工
- 若仍 > 400s：提新 PR 升级 `macos-15` → `macos-15-xlarge`（+100% 成本，-100-150s）
- UT + BDD 拆分 + lint-and-typecheck 拆 pyright 的方案（涉及 srp-actions 改造），单独评估

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T07:18:06Z): /lgtm

---

## 57e0b44

**作者**: dependabot[bot]
**日期**: 2026-04-22T06:53:43Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/57e0b443203b4583ba214c8b1d62973e57577a0b](https://github.com/SerendipityOneInc/ecap-workspace/commit/57e0b443203b4583ba214c8b1d62973e57577a0b)

### Commit Message
```
chore(deps-dev): update import-linter requirement from >=2.0 to >=2.11 in /services/claw-interface (#1171)

[//]: # (dependabot-start)
⚠️  **Dependabot is rebasing this PR** ⚠️ 

Rebasing might not happen immediately, so don't worry if this takes some
time.

Note: if you make any changes to this PR yourself, they will take
precedence over the rebase.

---

[//]: # (dependabot-end)

Updates the requirements on
[import-linter](https://github.com/seddonym/import-linter) to permit the
latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/seddonym/import-linter/blob/main/docs/release_notes.md">import-linter's
changelog</a>.</em></p>
<blockquote>
<h2>2.11 (2026-03-06)</h2>
<ul>
<li>Add <code>--version</code> flag to <code>lint-imports</code> and
<code>import-linter</code> commands.</li>
<li>Make <code>fastapi</code> and <code>uvicorn</code> optional via the
<code>ui</code> extra (<code>pip install import-linter[ui]</code>).</li>
<li>Bugfix: fix back button navigation in explore command.</li>
<li>Provide lower limits for <code>fastapi</code> and
<code>uvicorn</code> in <code>pyproject.toml</code>.</li>
<li>Switch to nox for testing.</li>
</ul>
<h2>2.10 (2026-02-06)</h2>
<ul>
<li>Add <code>import-linter</code> group command, with
<code>import-linter lint</code> alias.</li>
<li>Add <code>import-linter explore</code> command.</li>
<li>Add <code>import-linter drawgraph</code> command.</li>
</ul>
<h2>2.9 (2025-12-11)</h2>
<ul>
<li>Support passing namespaces as root packages, not just portions.</li>
<li>Bugfix: support Python 3.14 syntax.</li>
</ul>
<h2>2.8 (2025-12-08)</h2>
<ul>
<li>Fix logo display bug on Windows (fall back to simpler heading)
<a
href="https://redirect.github.com/seddonym/import-linter/issues/309">seddonym/import-linter#309</a></li>
<li>Rewrite docs (and switch from Sphinx to mkdocs).</li>
</ul>
<h2>2.7 (2025-11-19)</h2>
<ul>
<li>Print using rich instead of click.</li>
<li>Remove pluggable Printer class.</li>
<li>Add ascii art logo.</li>
<li>Add progress animations when building graph and checking
contracts.</li>
</ul>
<h2>2.6 (2025-11-10)</h2>
<ul>
<li>Add <code>acyclic_siblings</code> contract type.</li>
<li>Add contract field <code>IntegerField</code>.</li>
<li>Drop support for Python 3.9.</li>
</ul>
<h2>2.5.2 (2025-10-09)</h2>
<ul>
<li>Fix build issue with PyPI description.</li>
</ul>
<h2>2.5.1 (2025-10-09)</h2>
<ul>
<li>Correct documentation that incorrectly stated that protected modules
are allowed to import each other.</li>
<li>Officially support Python 3.14.</li>
</ul>
<h2>2.5 (2025-09-15)</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/seddonym/import-linter/commit/fabeab72e88f5055721c785003a2fde80f79bc64"><code>fabeab7</code></a>
Release v2.11</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/af956e1416aee2ea2cecc9fb94cd892affe6d6d2"><code>af956e1</code></a>
Use nox for CI</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/e0005c47e2147affc7cf0d19fdf0ac37f981afcf"><code>e0005c4</code></a>
Delegate to nox to run the tests from the justfile</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/61df307700bd89e1616bb355e43e8a124e58130a"><code>61df307</code></a>
Add test_earliest_dependencies to noxfile</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/736e4d3d9eea0bb37e2edaad6aceff3dbb7f8a4f"><code>736e4d3</code></a>
Add noxfile for testing under each Python version</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/5cea377fb0efe90b912f16ff9bb49c20aa6cdf1d"><code>5cea377</code></a>
Add ability to run nox</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/521b90be68f8840e4ca08277c8f9837392bc75a7"><code>521b90b</code></a>
Tweak lowest dependencies of ui</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/903a61d06153bb8e8273a0cdcde8c5b27a650b1c"><code>903a61d</code></a>
Don't run tests for Python 3.9</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/b447e69eb564b28757fc3beb06ee5c4066054067"><code>b447e69</code></a>
Move httpx to dev dependency</li>
<li><a
href="https://github.com/seddonym/import-linter/commit/230b22cbd05b485c0355e7a8ced634a7ab3fb782"><code>230b22c</code></a>
Rename dev-no-ui to dev-minimal</li>
<li>Additional commits viewable in <a
href="https://github.com/seddonym/import-linter/compare/v2.0...v2.11">compare
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
Co-authored-by: Chris@ZooClaw <chris@srp.one>
```

### PR #1171: chore(deps-dev): update import-linter requirement from >=2.0 to >=2.11 in /services/claw-interface

Updates the requirements on [import-linter](https://github.com/seddonym/import-linter) to permit the latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/seddonym/import-linter/blob/main/docs/release_notes.md">import-linter's changelog</a>.</em></p>
<blockquote>
<h2>2.11 (2026-03-06)</h2>
<ul>
<li>Add <code>--version</code> flag to <code>lint-imports</code> and <code>import-linter</code> commands.</li>
<li>Make <code>fastapi</code> and <code>uvicorn</code> optional via the <code>ui</code> extra (<code>pip install import-linter[ui]</code>).</li>
<li>Bugfix: fix back button navigation in explore command.</li>
<li>Provide lower limits for <code>fastapi</code> and <code>uvicorn</code> in <code>pyproject.toml</code>.</li>
<li>Switch to nox for testing.</li>
</ul>
<h2>2.10 (2026-02-06)</h2>
<ul>
<li>Add <code>import-linter</code> group command, with <code>import-linter lint</code> alias.</li>
<li>Add <code>import-linter explore</code> command.</li>
<li>Add <code>import-linter drawgraph</code> command.</li>
</ul>
<h2>2.9 (2025-12-11)</h2>
<ul>
<li>Support passing namespaces as root packages, not just portions.</li>
<li>Bugfix: support Python 3.14 syntax.</li>
</ul>
<h2>2.8 (2025-12-08)</h2>
<ul>
<li>Fix logo display bug on Windows (fall back to simpler heading)
<a href="https://redirect.github.com/seddonym/import-linter/issues/309">seddonym/import-linter#309</a></li>
<li>Rewrite docs (and switch from Sphinx to mkdocs).</li>
</ul>
<h2>2.7 (2025-11-19)</h2>
<ul>
<li>Print using rich instead of click.</li>
<li>Remove pluggable Printer class.</li>
<li>Add ascii art logo.</li>
<li>Add progress animations when building graph and checking contracts.</li>
</ul>
<h2>2.6 (2025-11-10)</h2>
<ul>
<li>Add <code>acyclic_siblings</code> contract type.</li>
<li>Add contract field <code>IntegerField</code>.</li>
<li>Drop support for Python 3.9.</li>
</ul>
<h2>2.5.2 (2025-10-09)</h2>
<ul>
<li>Fix build issue with PyPI description.</li>
</ul>
<h2>2.5.1 (2025-10-09)</h2>
<ul>
<li>Correct documentation that incorrectly stated that protected modules
are allowed to import each other.</li>
<li>Officially support Python 3.14.</li>
</ul>
<h2>2.5 (2025-09-15)</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/seddonym/import-linter/commit/fabeab72e88f5055721c785003a2fde80f79bc64"><code>fabeab7</code></a> Release v2.11</li>
<li><a href="https://github.com/seddonym/import-linter/commit/af956e1416aee2ea2cecc9fb94cd892affe6d6d2"><code>af956e1</code></a> Use nox for CI</li>
<li><a href="https://github.com/seddonym/import-linter/commit/e0005c47e2147affc7cf0d19fdf0ac37f981afcf"><code>e0005c4</code></a> Delegate to nox to run the tests from the justfile</li>
<li><a href="https://github.com/seddonym/import-linter/commit/61df307700bd89e1616bb355e43e8a124e58130a"><code>61df307</code></a> Add test_earliest_dependencies to noxfile</li>
<li><a href="https://github.com/seddonym/import-linter/commit/736e4d3d9eea0bb37e2edaad6aceff3dbb7f8a4f"><code>736e4d3</code></a> Add noxfile for testing under each Python version</li>
<li><a href="https://github.com/seddonym/import-linter/commit/5cea377fb0efe90b912f16ff9bb49c20aa6cdf1d"><code>5cea377</code></a> Add ability to run nox</li>
<li><a href="https://github.com/seddonym/import-linter/commit/521b90be68f8840e4ca08277c8f9837392bc75a7"><code>521b90b</code></a> Tweak lowest dependencies of ui</li>
<li><a href="https://github.com/seddonym/import-linter/commit/903a61d06153bb8e8273a0cdcde8c5b27a650b1c"><code>903a61d</code></a> Don't run tests for Python 3.9</li>
<li><a href="https://github.com/seddonym/import-linter/commit/b447e69eb564b28757fc3beb06ee5c4066054067"><code>b447e69</code></a> Move httpx to dev dependency</li>
<li><a href="https://github.com/seddonym/import-linter/commit/230b22cbd05b485c0355e7a8ced634a7ab3fb782"><code>230b22c</code></a> Rename dev-no-ui to dev-minimal</li>
<li>Additional commits viewable in <a href="https://github.com/seddonym/import-linter/compare/v2.0...v2.11">compare view</a></li>
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

---

## f2641e8

**作者**: dependabot[bot]
**日期**: 2026-04-22T06:52:36Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/f2641e887f7a81c6b181a478c3a90db8ff6fd0f2](https://github.com/SerendipityOneInc/ecap-workspace/commit/f2641e887f7a81c6b181a478c3a90db8ff6fd0f2)

### Commit Message
```
chore(deps-dev): update ruff requirement from >=0.8.0 to >=0.15.11 in /services/claw-interface (#1170)

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to
permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/releases">ruff's
releases</a>.</em></p>
<blockquote>
<h2>0.15.11</h2>
<h2>Release Notes</h2>
<p>Released on 2026-04-16.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>ruff</code>] Ignore <code>RUF029</code> when function is
decorated with <code>asynccontextmanager</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24642">#24642</a>)</li>
<li>[<code>airflow</code>] Implement
<code>airflow-xcom-pull-in-template-string</code> (<code>AIR201</code>)
(<a
href="https://redirect.github.com/astral-sh/ruff/pull/23583">#23583</a>)</li>
<li>[<code>flake8-bandit</code>] Fix <code>S103</code> false positives
and negatives in mask analysis (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24424">#24424</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-async</code>] Omit overridden methods for
<code>ASYNC109</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24648">#24648</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>[<code>flake8-async</code>] Add override mention to
<code>ASYNC109</code> docs (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24666">#24666</a>)</li>
<li>Update Neovim config examples to use <code>vim.lsp.config</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24577">#24577</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/augustelalande"><code>@​augustelalande</code></a></li>
<li><a
href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a
href="https://github.com/benberryallwood"><code>@​benberryallwood</code></a></li>
<li><a
href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a href="https://github.com/Dev-iL"><code>@​Dev-iL</code></a></li>
</ul>
<h2>Install ruff 0.15.11</h2>
<h3>Install prebuilt binaries via shell script</h3>
<pre lang="sh"><code>curl --proto '=https' --tlsv1.2 -LsSf
https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-installer.sh
| sh
</code></pre>
<h3>Install prebuilt binaries via powershell script</h3>
<pre lang="sh"><code>powershell -ExecutionPolicy Bypass -c &quot;irm
https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-installer.ps1
| iex&quot;
</code></pre>
<h2>Download ruff 0.15.11</h2>
<table>
<thead>
<tr>
<th>File</th>
<th>Platform</th>
<th>Checksum</th>
</tr>
</thead>
<tbody>
<tr>
<td><a
href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-aarch64-apple-darwin.tar.gz">ruff-aarch64-apple-darwin.tar.gz</a></td>
<td>Apple Silicon macOS</td>
<td><a
href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-aarch64-apple-darwin.tar.gz.sha256">checksum</a></td>
</tr>
<tr>
<td><a
href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-x86_64-apple-darwin.tar.gz">ruff-x86_64-apple-darwin.tar.gz</a></td>
<td>Intel macOS</td>
<td><a
href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-x86_64-apple-darwin.tar.gz.sha256">checksum</a></td>
</tr>
<tr>
<td><a
href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-aarch64-pc-windows-msvc.zip">ruff-aarch64-pc-windows-msvc.zip</a></td>
<td>ARM64 Windows</td>
<td><a
href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-aarch64-pc-windows-msvc.zip.sha256">checksum</a></td>
</tr>
<tr>
<td><a
href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-i686-pc-windows-msvc.zip">ruff-i686-pc-windows-msvc.zip</a></td>
<td>x86 Windows</td>
<td><a
href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-i686-pc-windows-msvc.zip.sha256">checksum</a></td>
</tr>
</tbody>
</table>
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
<h2>0.15.11</h2>
<p>Released on 2026-04-16.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>ruff</code>] Ignore <code>RUF029</code> when function is
decorated with <code>asynccontextmanager</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24642">#24642</a>)</li>
<li>[<code>airflow</code>] Implement
<code>airflow-xcom-pull-in-template-string</code> (<code>AIR201</code>)
(<a
href="https://redirect.github.com/astral-sh/ruff/pull/23583">#23583</a>)</li>
<li>[<code>flake8-bandit</code>] Fix <code>S103</code> false positives
and negatives in mask analysis (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24424">#24424</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-async</code>] Omit overridden methods for
<code>ASYNC109</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24648">#24648</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>[<code>flake8-async</code>] Add override mention to
<code>ASYNC109</code> docs (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24666">#24666</a>)</li>
<li>Update Neovim config examples to use <code>vim.lsp.config</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24577">#24577</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/augustelalande"><code>@​augustelalande</code></a></li>
<li><a
href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a
href="https://github.com/benberryallwood"><code>@​benberryallwood</code></a></li>
<li><a
href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a href="https://github.com/Dev-iL"><code>@​Dev-iL</code></a></li>
</ul>
<h2>0.15.10</h2>
<p>Released on 2026-04-09.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>flake8-logging</code>] Allow closures in except handlers
(<code>LOG004</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24464">#24464</a>)</li>
<li>[<code>flake8-self</code>] Make <code>SLF</code> diagnostics robust
to non-self-named variables (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24281">#24281</a>)</li>
<li>[<code>flake8-simplify</code>] Make the fix for
<code>collapsible-if</code> safe in <code>preview</code>
(<code>SIM102</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24371">#24371</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Avoid emitting multi-line f-string elements before Python 3.12 (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24377">#24377</a>)</li>
<li>Avoid syntax error from <code>E502</code> fixes in f-strings and
t-strings (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24410">#24410</a>)</li>
<li>Strip form feeds from indent passed to <code>dedent_to</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24381">#24381</a>)</li>
<li>[<code>pyupgrade</code>] Fix panic caused by handling of octals
(<code>UP012</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24390">#24390</a>)</li>
<li>Reject multi-line f-string elements before Python 3.12 (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24355">#24355</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>ruff</code>] Treat f-string interpolation as potential side
effect (<code>RUF019</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24426">#24426</a>)</li>
</ul>
<h3>Server</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/astral-sh/ruff/commit/53554b1cfe837f2eb992a81794480699478f1116"><code>53554b1</code></a>
Bump 0.15.11 (<a
href="https://redirect.github.com/astral-sh/ruff/issues/24678">#24678</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/08c56c83cffbb1025cbf5bdede6c6d8be591cf47"><code>08c56c8</code></a>
Factor out the <code>mdtest</code> crate (<a
href="https://redirect.github.com/astral-sh/ruff/issues/24616">#24616</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/725fbb736d2a999971449b61190b914abd26102a"><code>725fbb7</code></a>
[ty] Use partially qualified names when reporting diagnostics regarding
bad c...</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/ddd6a30ff5fa27694dc1c50d0749885a1519d0a7"><code>ddd6a30</code></a>
[ty] Do not suggest argument completion when at value of keyword
argument (<a
href="https://redirect.github.com/astral-sh/ruff/issues/2">#2</a>...</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/9282e61d482a36da08d66bb8271afeef50b3bc45"><code>9282e61</code></a>
Disallow <a
href="https://github.com/disjoint"><code>@​disjoint</code></a>_base on
TypedDicts and Protocols (<a
href="https://redirect.github.com/astral-sh/ruff/issues/24671">#24671</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/e9986d8e3008eefe2e387312c4dc8b9c60f6f362"><code>e9986d8</code></a>
[ty] Reject using properties with <code>Never</code> setters or deleters
(<a
href="https://redirect.github.com/astral-sh/ruff/issues/24510">#24510</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/9cf212ff82f7b66b4a275ad6a9b1564aee1fa4a8"><code>9cf212f</code></a>
[ty] Normalize property setter and deleter wrappers (<a
href="https://redirect.github.com/astral-sh/ruff/issues/24509">#24509</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/12a1589de4d7120cf99441ee4c14871bdc20968d"><code>12a1589</code></a>
Add override mention to ASYNC109 docs (<a
href="https://redirect.github.com/astral-sh/ruff/issues/24666">#24666</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/dccb03d010f4442ed60624f8d2ba932706abaabb"><code>dccb03d</code></a>
[ty] Avoid panicking on overloaded <code>Callable</code> type context
(<a
href="https://redirect.github.com/astral-sh/ruff/issues/24661">#24661</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/61f9a0a5763fb068cd2f26c0ee9d63a277fb26c2"><code>61f9a0a</code></a>
[ty] Sync vendored typeshed stubs (<a
href="https://redirect.github.com/astral-sh/ruff/issues/24646">#24646</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/astral-sh/ruff/compare/0.8.0...0.15.11">compare
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

### PR #1170: chore(deps-dev): update ruff requirement from >=0.8.0 to >=0.15.11 in /services/claw-interface

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's releases</a>.</em></p>
<blockquote>
<h2>0.15.11</h2>
<h2>Release Notes</h2>
<p>Released on 2026-04-16.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>ruff</code>] Ignore <code>RUF029</code> when function is decorated with <code>asynccontextmanager</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/24642">#24642</a>)</li>
<li>[<code>airflow</code>] Implement <code>airflow-xcom-pull-in-template-string</code> (<code>AIR201</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/23583">#23583</a>)</li>
<li>[<code>flake8-bandit</code>] Fix <code>S103</code> false positives and negatives in mask analysis (<a href="https://redirect.github.com/astral-sh/ruff/pull/24424">#24424</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-async</code>] Omit overridden methods for <code>ASYNC109</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/24648">#24648</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>[<code>flake8-async</code>] Add override mention to <code>ASYNC109</code> docs (<a href="https://redirect.github.com/astral-sh/ruff/pull/24666">#24666</a>)</li>
<li>Update Neovim config examples to use <code>vim.lsp.config</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/24577">#24577</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/augustelalande"><code>@​augustelalande</code></a></li>
<li><a href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a href="https://github.com/benberryallwood"><code>@​benberryallwood</code></a></li>
<li><a href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a href="https://github.com/Dev-iL"><code>@​Dev-iL</code></a></li>
</ul>
<h2>Install ruff 0.15.11</h2>
<h3>Install prebuilt binaries via shell script</h3>
<pre lang="sh"><code>curl --proto '=https' --tlsv1.2 -LsSf https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-installer.sh | sh
</code></pre>
<h3>Install prebuilt binaries via powershell script</h3>
<pre lang="sh"><code>powershell -ExecutionPolicy Bypass -c &quot;irm https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-installer.ps1 | iex&quot;
</code></pre>
<h2>Download ruff 0.15.11</h2>
<table>
<thead>
<tr>
<th>File</th>
<th>Platform</th>
<th>Checksum</th>
</tr>
</thead>
<tbody>
<tr>
<td><a href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-aarch64-apple-darwin.tar.gz">ruff-aarch64-apple-darwin.tar.gz</a></td>
<td>Apple Silicon macOS</td>
<td><a href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-aarch64-apple-darwin.tar.gz.sha256">checksum</a></td>
</tr>
<tr>
<td><a href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-x86_64-apple-darwin.tar.gz">ruff-x86_64-apple-darwin.tar.gz</a></td>
<td>Intel macOS</td>
<td><a href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-x86_64-apple-darwin.tar.gz.sha256">checksum</a></td>
</tr>
<tr>
<td><a href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-aarch64-pc-windows-msvc.zip">ruff-aarch64-pc-windows-msvc.zip</a></td>
<td>ARM64 Windows</td>
<td><a href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-aarch64-pc-windows-msvc.zip.sha256">checksum</a></td>
</tr>
<tr>
<td><a href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-i686-pc-windows-msvc.zip">ruff-i686-pc-windows-msvc.zip</a></td>
<td>x86 Windows</td>
<td><a href="https://releases.astral.sh/github/ruff/releases/download/0.15.11/ruff-i686-pc-windows-msvc.zip.sha256">checksum</a></td>
</tr>
</tbody>
</table>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
<blockquote>
<h2>0.15.11</h2>
<p>Released on 2026-04-16.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>ruff</code>] Ignore <code>RUF029</code> when function is decorated with <code>asynccontextmanager</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/24642">#24642</a>)</li>
<li>[<code>airflow</code>] Implement <code>airflow-xcom-pull-in-template-string</code> (<code>AIR201</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/23583">#23583</a>)</li>
<li>[<code>flake8-bandit</code>] Fix <code>S103</code> false positives and negatives in mask analysis (<a href="https://redirect.github.com/astral-sh/ruff/pull/24424">#24424</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-async</code>] Omit overridden methods for <code>ASYNC109</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/24648">#24648</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>[<code>flake8-async</code>] Add override mention to <code>ASYNC109</code> docs (<a href="https://redirect.github.com/astral-sh/ruff/pull/24666">#24666</a>)</li>
<li>Update Neovim config examples to use <code>vim.lsp.config</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/24577">#24577</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/augustelalande"><code>@​augustelalande</code></a></li>
<li><a href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a href="https://github.com/benberryallwood"><code>@​benberryallwood</code></a></li>
<li><a href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a href="https://github.com/Dev-iL"><code>@​Dev-iL</code></a></li>
</ul>
<h2>0.15.10</h2>
<p>Released on 2026-04-09.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>flake8-logging</code>] Allow closures in except handlers (<code>LOG004</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/24464">#24464</a>)</li>
<li>[<code>flake8-self</code>] Make <code>SLF</code> diagnostics robust to non-self-named variables (<a href="https://redirect.github.com/astral-sh/ruff/pull/24281">#24281</a>)</li>
<li>[<code>flake8-simplify</code>] Make the fix for <code>collapsible-if</code> safe in <code>preview</code> (<code>SIM102</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/24371">#24371</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Avoid emitting multi-line f-string elements before Python 3.12 (<a href="https://redirect.github.com/astral-sh/ruff/pull/24377">#24377</a>)</li>
<li>Avoid syntax error from <code>E502</code> fixes in f-strings and t-strings (<a href="https://redirect.github.com/astral-sh/ruff/pull/24410">#24410</a>)</li>
<li>Strip form feeds from indent passed to <code>dedent_to</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/24381">#24381</a>)</li>
<li>[<code>pyupgrade</code>] Fix panic caused by handling of octals (<code>UP012</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/24390">#24390</a>)</li>
<li>Reject multi-line f-string elements before Python 3.12 (<a href="https://redirect.github.com/astral-sh/ruff/pull/24355">#24355</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>ruff</code>] Treat f-string interpolation as potential side effect (<code>RUF019</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/24426">#24426</a>)</li>
</ul>
<h3>Server</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/astral-sh/ruff/commit/53554b1cfe837f2eb992a81794480699478f1116"><code>53554b1</code></a> Bump 0.15.11 (<a href="https://redirect.github.com/astral-sh/ruff/issues/24678">#24678</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/08c56c83cffbb1025cbf5bdede6c6d8be591cf47"><code>08c56c8</code></a> Factor out the <code>mdtest</code> crate (<a href="https://redirect.github.com/astral-sh/ruff/issues/24616">#24616</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/725fbb736d2a999971449b61190b914abd26102a"><code>725fbb7</code></a> [ty] Use partially qualified names when reporting diagnostics regarding bad c...</li>
<li><a href="https://github.com/astral-sh/ruff/commit/ddd6a30ff5fa27694dc1c50d0749885a1519d0a7"><code>ddd6a30</code></a> [ty] Do not suggest argument completion when at value of keyword argument (<a href="https://redirect.github.com/astral-sh/ruff/issues/2">#2</a>...</li>
<li><a href="https://github.com/astral-sh/ruff/commit/9282e61d482a36da08d66bb8271afeef50b3bc45"><code>9282e61</code></a> Disallow <a href="https://github.com/disjoint"><code>@​disjoint</code></a>_base on TypedDicts and Protocols (<a href="https://redirect.github.com/astral-sh/ruff/issues/24671">#24671</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/e9986d8e3008eefe2e387312c4dc8b9c60f6f362"><code>e9986d8</code></a> [ty] Reject using properties with <code>Never</code> setters or deleters (<a href="https://redirect.github.com/astral-sh/ruff/issues/24510">#24510</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/9cf212ff82f7b66b4a275ad6a9b1564aee1fa4a8"><code>9cf212f</code></a> [ty] Normalize property setter and deleter wrappers (<a href="https://redirect.github.com/astral-sh/ruff/issues/24509">#24509</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/12a1589de4d7120cf99441ee4c14871bdc20968d"><code>12a1589</code></a> Add override mention to ASYNC109 docs (<a href="https://redirect.github.com/astral-sh/ruff/issues/24666">#24666</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/dccb03d010f4442ed60624f8d2ba932706abaabb"><code>dccb03d</code></a> [ty] Avoid panicking on overloaded <code>Callable</code> type context (<a href="https://redirect.github.com/astral-sh/ruff/issues/24661">#24661</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/61f9a0a5763fb068cd2f26c0ee9d63a277fb26c2"><code>61f9a0a</code></a> [ty] Sync vendored typeshed stubs (<a href="https://redirect.github.com/astral-sh/ruff/issues/24646">#24646</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.8.0...0.15.11">compare view</a></li>
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

---

## daeed53

**作者**: dependabot[bot]
**日期**: 2026-04-22T06:52:18Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/daeed5370717a6e3f430e97ac7393853657e65a9](https://github.com/SerendipityOneInc/ecap-workspace/commit/daeed5370717a6e3f430e97ac7393853657e65a9)

### Commit Message
```
chore(deps-dev): update deptry requirement from >=0.20 to >=0.25.1 in /services/claw-interface (#1169)

Updates the requirements on
[deptry](https://github.com/osprey-oss/deptry) to permit the latest
version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/osprey-oss/deptry/releases">deptry's
releases</a>.</em></p>
<blockquote>
<h2>0.25.1</h2>
<h2>What's Changed</h2>
<p>Release <a
href="https://github.com/osprey-oss/deptry/releases/tag/0.25.0">0.25.0</a>
was yanked in PyPI because of a failure during the release. 0.25.1 is
identical, but includes a fix in the release process.</p>
<p><strong>Full Changelog</strong>: <a
href="https://github.com/osprey-oss/deptry/compare/0.25.0...0.25.1">https://github.com/osprey-oss/deptry/compare/0.25.0...0.25.1</a></p>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/osprey-oss/deptry/blob/main/CHANGELOG.md">deptry's
changelog</a>.</em></p>
<blockquote>
<h2>0.25.1 - 2025-03-18</h2>
<p>Release 0.25.0 was yanked in PyPI because of a failure during the
release. 0.25.1 is identical, but includes a fix in the release
process.</p>
<h2>0.25.0 - 2025-03-18</h2>
<h3>Repository moved to Osprey OSS</h3>
<p>deptry has moved from <a
href="https://github.com/fpgmaas/deptry">fpgmaas/deptry</a> to <a
href="https://github.com/osprey-oss/deptry">osprey-oss/deptry</a> under
the new Osprey OSS organisation. This ensures the project is not tied to
a single account and makes it easier to manage contributors and access
as the project grows.</p>
<h3>Features</h3>
<ul>
<li>Support inline <code># deptry: ignore</code> comments to suppress
violations (<a
href="https://redirect.github.com/fpgmaas/deptry/pull/1473">#1473</a>)</li>
<li>Support non-dev dependency groups with
<code>--non-dev-dependency-groups</code> (<a
href="https://redirect.github.com/fpgmaas/deptry/pull/1440">#1440</a>)</li>
<li>Use <code>tomli</code> on Python &lt; 3.15 for TOML 1.1 support (<a
href="https://redirect.github.com/fpgmaas/deptry/pull/1446">#1446</a>)</li>
<li>Add <code>--optional-dependencies-dev-groups</code> and deprecate
<code>--pep621-dev-dependency-groups</code> (<a
href="https://redirect.github.com/fpgmaas/deptry/pull/1391">#1391</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li>Ensure that <code>--config</code> does not suppress output (<a
href="https://redirect.github.com/fpgmaas/deptry/pull/1390">#1390</a>)</li>
</ul>
<h3>Full Changelog</h3>
<p><a
href="https://github.com/fpgmaas/deptry/compare/0.24.0...0.25.0">https://github.com/fpgmaas/deptry/compare/0.24.0...0.25.0</a></p>
<h2>0.24.0 - 2025-11-09</h2>
<h3>Breaking changes</h3>
<h4>Python 3.9 support dropped</h4>
<p>Support for Python 3.9 has been dropped, as it has reached its end of
life.</p>
<h4>PyPy 3.10 support dropped, 3.11 added</h4>
<p>Support for PyPy 3.10 has been dropped, since it is unsupported. We
now only test against PyPy 3.11, and only publish wheels for this
version.</p>
<h3>Features</h3>
<ul>
<li>Add GitHub Actions annotations reporter (<a
href="https://redirect.github.com/osprey-oss/deptry/pull/1059">#1059</a>)</li>
<li>Add support for Python 3.14 (<a
href="https://redirect.github.com/osprey-oss/deptry/pull/1224">#1224</a>)</li>
<li>Drop support for Python 3.9 (<a
href="https://redirect.github.com/osprey-oss/deptry/pull/1328">#1328</a>)</li>
<li>Publish wheels for PyPy 3.11 and drop 3.10 (<a
href="https://redirect.github.com/osprey-oss/deptry/pull/1227">#1227</a>)</li>
</ul>
<h3>Full Changelog</h3>
<p><a
href="https://github.com/osprey-oss/deptry/compare/0.23.1...0.24.0">https://github.com/osprey-oss/deptry/compare/0.23.1...0.24.0</a></p>
<h2>0.23.1 - 2025-07-30</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/osprey-oss/deptry/commit/0c39226d761685125c5ff71ca81282d6751c9540"><code>0c39226</code></a>
Remove pinned maturin version for building windows wheels in release (<a
href="https://redirect.github.com/osprey-oss/deptry/issues/1516">#1516</a>)</li>
<li><a
href="https://github.com/osprey-oss/deptry/commit/501a929da2e323fb3b49322380169ade0fd4709f"><code>501a929</code></a>
chore(packaging): use PEP 639 license format (<a
href="https://redirect.github.com/osprey-oss/deptry/issues/1514">#1514</a>)</li>
<li><a
href="https://github.com/osprey-oss/deptry/commit/2d89cf487520b0284a4f6f6a6077ce3bb7299bbd"><code>2d89cf4</code></a>
Releasenotes for release 0.25.0 (<a
href="https://redirect.github.com/osprey-oss/deptry/issues/1510">#1510</a>)</li>
<li><a
href="https://github.com/osprey-oss/deptry/commit/ef64f9367f58aab61e752f8a48c07dd9fd137f7f"><code>ef64f93</code></a>
Replace all references of fpgmaas/deptry with osprey-oss/deptry (<a
href="https://redirect.github.com/osprey-oss/deptry/issues/1513">#1513</a>)</li>
<li><a
href="https://github.com/osprey-oss/deptry/commit/fdec8c532f2172ec64bec4b779fcb56508e276ef"><code>fdec8c5</code></a>
Add trusted publishing (<a
href="https://redirect.github.com/osprey-oss/deptry/issues/1512">#1512</a>)</li>
<li><a
href="https://github.com/osprey-oss/deptry/commit/2e27ae2242567f2958aa9a451f54d4b3ec31740b"><code>2e27ae2</code></a>
chore(deps): update uv-version to v0.10.10 (<a
href="https://redirect.github.com/osprey-oss/deptry/issues/1503">#1503</a>)</li>
<li><a
href="https://github.com/osprey-oss/deptry/commit/9d1f7d1e6ed1d27c163dd1abc28eeda5beba50ca"><code>9d1f7d1</code></a>
chore(deps): update pre-commit hook astral-sh/ruff-pre-commit to v0.15.6
(<a
href="https://redirect.github.com/osprey-oss/deptry/issues/1502">#1502</a>)</li>
<li><a
href="https://github.com/osprey-oss/deptry/commit/2a5a0a6b631f0ee1e4475b1e9212d0bafe3af68c"><code>2a5a0a6</code></a>
chore(deps): update dependency mkdocs-material to v9.7.5 (<a
href="https://redirect.github.com/osprey-oss/deptry/issues/1501">#1501</a>)</li>
<li><a
href="https://github.com/osprey-oss/deptry/commit/487f682138d7ac9370cb1b9edd0be26a1e8940d0"><code>487f682</code></a>
chore(deps): update dependency pnpm to v10.32.1 (<a
href="https://redirect.github.com/osprey-oss/deptry/issues/1506">#1506</a>)</li>
<li><a
href="https://github.com/osprey-oss/deptry/commit/608ba46360298c30db7402179fe85349f78391f4"><code>608ba46</code></a>
fix(deps): update ruff rust to v0.15.6 (<a
href="https://redirect.github.com/osprey-oss/deptry/issues/1504">#1504</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/osprey-oss/deptry/compare/0.20.0...0.25.1">compare
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

### PR #1169: chore(deps-dev): update deptry requirement from >=0.20 to >=0.25.1 in /services/claw-interface

Updates the requirements on [deptry](https://github.com/osprey-oss/deptry) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/osprey-oss/deptry/releases">deptry's releases</a>.</em></p>
<blockquote>
<h2>0.25.1</h2>
<h2>What's Changed</h2>
<p>Release <a href="https://github.com/osprey-oss/deptry/releases/tag/0.25.0">0.25.0</a> was yanked in PyPI because of a failure during the release. 0.25.1 is identical, but includes a fix in the release process.</p>
<p><strong>Full Changelog</strong>: <a href="https://github.com/osprey-oss/deptry/compare/0.25.0...0.25.1">https://github.com/osprey-oss/deptry/compare/0.25.0...0.25.1</a></p>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/osprey-oss/deptry/blob/main/CHANGELOG.md">deptry's changelog</a>.</em></p>
<blockquote>
<h2>0.25.1 - 2025-03-18</h2>
<p>Release 0.25.0 was yanked in PyPI because of a failure during the release. 0.25.1 is identical, but includes a fix in the release process.</p>
<h2>0.25.0 - 2025-03-18</h2>
<h3>Repository moved to Osprey OSS</h3>
<p>deptry has moved from <a href="https://github.com/fpgmaas/deptry">fpgmaas/deptry</a> to <a href="https://github.com/osprey-oss/deptry">osprey-oss/deptry</a> under the new Osprey OSS organisation. This ensures the project is not tied to a single account and makes it easier to manage contributors and access as the project grows.</p>
<h3>Features</h3>
<ul>
<li>Support inline <code># deptry: ignore</code> comments to suppress violations (<a href="https://redirect.github.com/fpgmaas/deptry/pull/1473">#1473</a>)</li>
<li>Support non-dev dependency groups with <code>--non-dev-dependency-groups</code> (<a href="https://redirect.github.com/fpgmaas/deptry/pull/1440">#1440</a>)</li>
<li>Use <code>tomli</code> on Python &lt; 3.15 for TOML 1.1 support (<a href="https://redirect.github.com/fpgmaas/deptry/pull/1446">#1446</a>)</li>
<li>Add <code>--optional-dependencies-dev-groups</code> and deprecate <code>--pep621-dev-dependency-groups</code> (<a href="https://redirect.github.com/fpgmaas/deptry/pull/1391">#1391</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li>Ensure that <code>--config</code> does not suppress output (<a href="https://redirect.github.com/fpgmaas/deptry/pull/1390">#1390</a>)</li>
</ul>
<h3>Full Changelog</h3>
<p><a href="https://github.com/fpgmaas/deptry/compare/0.24.0...0.25.0">https://github.com/fpgmaas/deptry/compare/0.24.0...0.25.0</a></p>
<h2>0.24.0 - 2025-11-09</h2>
<h3>Breaking changes</h3>
<h4>Python 3.9 support dropped</h4>
<p>Support for Python 3.9 has been dropped, as it has reached its end of life.</p>
<h4>PyPy 3.10 support dropped, 3.11 added</h4>
<p>Support for PyPy 3.10 has been dropped, since it is unsupported. We now only test against PyPy 3.11, and only publish wheels for this version.</p>
<h3>Features</h3>
<ul>
<li>Add GitHub Actions annotations reporter (<a href="https://redirect.github.com/osprey-oss/deptry/pull/1059">#1059</a>)</li>
<li>Add support for Python 3.14 (<a href="https://redirect.github.com/osprey-oss/deptry/pull/1224">#1224</a>)</li>
<li>Drop support for Python 3.9 (<a href="https://redirect.github.com/osprey-oss/deptry/pull/1328">#1328</a>)</li>
<li>Publish wheels for PyPy 3.11 and drop 3.10 (<a href="https://redirect.github.com/osprey-oss/deptry/pull/1227">#1227</a>)</li>
</ul>
<h3>Full Changelog</h3>
<p><a href="https://github.com/osprey-oss/deptry/compare/0.23.1...0.24.0">https://github.com/osprey-oss/deptry/compare/0.23.1...0.24.0</a></p>
<h2>0.23.1 - 2025-07-30</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/osprey-oss/deptry/commit/0c39226d761685125c5ff71ca81282d6751c9540"><code>0c39226</code></a> Remove pinned maturin version for building windows wheels in release (<a href="https://redirect.github.com/osprey-oss/deptry/issues/1516">#1516</a>)</li>
<li><a href="https://github.com/osprey-oss/deptry/commit/501a929da2e323fb3b49322380169ade0fd4709f"><code>501a929</code></a> chore(packaging): use PEP 639 license format (<a href="https://redirect.github.com/osprey-oss/deptry/issues/1514">#1514</a>)</li>
<li><a href="https://github.com/osprey-oss/deptry/commit/2d89cf487520b0284a4f6f6a6077ce3bb7299bbd"><code>2d89cf4</code></a> Releasenotes for release 0.25.0 (<a href="https://redirect.github.com/osprey-oss/deptry/issues/1510">#1510</a>)</li>
<li><a href="https://github.com/osprey-oss/deptry/commit/ef64f9367f58aab61e752f8a48c07dd9fd137f7f"><code>ef64f93</code></a> Replace all references of fpgmaas/deptry with osprey-oss/deptry (<a href="https://redirect.github.com/osprey-oss/deptry/issues/1513">#1513</a>)</li>
<li><a href="https://github.com/osprey-oss/deptry/commit/fdec8c532f2172ec64bec4b779fcb56508e276ef"><code>fdec8c5</code></a> Add trusted publishing (<a href="https://redirect.github.com/osprey-oss/deptry/issues/1512">#1512</a>)</li>
<li><a href="https://github.com/osprey-oss/deptry/commit/2e27ae2242567f2958aa9a451f54d4b3ec31740b"><code>2e27ae2</code></a> chore(deps): update uv-version to v0.10.10 (<a href="https://redirect.github.com/osprey-oss/deptry/issues/1503">#1503</a>)</li>
<li><a href="https://github.com/osprey-oss/deptry/commit/9d1f7d1e6ed1d27c163dd1abc28eeda5beba50ca"><code>9d1f7d1</code></a> chore(deps): update pre-commit hook astral-sh/ruff-pre-commit to v0.15.6 (<a href="https://redirect.github.com/osprey-oss/deptry/issues/1502">#1502</a>)</li>
<li><a href="https://github.com/osprey-oss/deptry/commit/2a5a0a6b631f0ee1e4475b1e9212d0bafe3af68c"><code>2a5a0a6</code></a> chore(deps): update dependency mkdocs-material to v9.7.5 (<a href="https://redirect.github.com/osprey-oss/deptry/issues/1501">#1501</a>)</li>
<li><a href="https://github.com/osprey-oss/deptry/commit/487f682138d7ac9370cb1b9edd0be26a1e8940d0"><code>487f682</code></a> chore(deps): update dependency pnpm to v10.32.1 (<a href="https://redirect.github.com/osprey-oss/deptry/issues/1506">#1506</a>)</li>
<li><a href="https://github.com/osprey-oss/deptry/commit/608ba46360298c30db7402179fe85349f78391f4"><code>608ba46</code></a> fix(deps): update ruff rust to v0.15.6 (<a href="https://redirect.github.com/osprey-oss/deptry/issues/1504">#1504</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/osprey-oss/deptry/compare/0.20.0...0.25.1">compare view</a></li>
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

---

## d1df204

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T06:47:42Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/d1df2048df0516004bc3100def934d21d147fe4d](https://github.com/SerendipityOneInc/ecap-workspace/commit/d1df2048df0516004bc3100def934d21d147fe4d)

### Commit Message
```
test(web): ImagePreview 全面覆盖 (#894 Step 11 补) (#1162)

## Summary

Epic #894 Step 11 (#905) — \`ImagePreview.tsx\` (257 LOC) 从 0% → 全分支。31
tests,零源码改动。

## 新增 31 个测试

| 分组 | # | 覆盖 |
|---|---|---|
| 单图模式 | 6 | preview URL / blur 占位 / spinner fallback / onLoad/onError /
blur onError 立刻标 loaded |
| 视频模式 | 2 | \`<video>\` controls+autoPlay / 不渲染 \`<img>\` |
| 画廊模式 | 9 | N/M 指示符 / 双箭头可见性 / prev/next click + stopPropagation / 视频项
/ 本地 index fallback / 单图不是画廊 |
| 关闭交互 | 4 | backdrop / X / Escape / 内容区点击不关 |
| 键盘导航 | 4 | ArrowLeft/Right / 边界 no-op / 其他键 no-op |
| 下载 | 3 | 参数透传 / 画廊用 active item / stopPropagation |
| body scroll lock | 2 | mount set hidden / unmount 还原 |
| currentIndex sync | 1 | prop 变 → 指示符更新 |

## Harness 要点

- **thumbnail mock 用 URL 后缀区分**：`getBlurUrl` → `?blur=1`,
`getPreviewUrl` → `?preview=1`，测试通过 suffix 过滤找对 `<img>`
- **X button 点击 2 次 onClose**：click bubbles button → overlay，两处都触发
onClose。幂等不是 bug，assertion 用 `toHaveBeenCalled()` 不 pin 次数

## Bug-hunting

无新发现。X button 的双 dispatch 是 click-bubbling 正常行为，onClose 幂等处理得当。

## Test plan

- [x] 31/31 通过
- [x] tsc clean (只剩 knip.config pre-existing)
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 11 (#905)
- 剩余: ModelSelector (381) / FeedbackDialog (337) / GuideTourModal (418)
/ ArchivedSessionPanel (301)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1162: test(web): ImagePreview 全面覆盖 (#894 Step 11 补)

## Summary

Epic #894 Step 11 (#905) — \`ImagePreview.tsx\` (257 LOC) 从 0% → 全分支。31 tests,零源码改动。

## 新增 31 个测试

| 分组 | # | 覆盖 |
|---|---|---|
| 单图模式 | 6 | preview URL / blur 占位 / spinner fallback / onLoad/onError / blur onError 立刻标 loaded |
| 视频模式 | 2 | \`<video>\` controls+autoPlay / 不渲染 \`<img>\` |
| 画廊模式 | 9 | N/M 指示符 / 双箭头可见性 / prev/next click + stopPropagation / 视频项 / 本地 index fallback / 单图不是画廊 |
| 关闭交互 | 4 | backdrop / X / Escape / 内容区点击不关 |
| 键盘导航 | 4 | ArrowLeft/Right / 边界 no-op / 其他键 no-op |
| 下载 | 3 | 参数透传 / 画廊用 active item / stopPropagation |
| body scroll lock | 2 | mount set hidden / unmount 还原 |
| currentIndex sync | 1 | prop 变 → 指示符更新 |

## Harness 要点

- **thumbnail mock 用 URL 后缀区分**：`getBlurUrl` → `?blur=1`, `getPreviewUrl` → `?preview=1`，测试通过 suffix 过滤找对 `<img>`
- **X button 点击 2 次 onClose**：click bubbles button → overlay，两处都触发 onClose。幂等不是 bug，assertion 用 `toHaveBeenCalled()` 不 pin 次数

## Bug-hunting

无新发现。X button 的双 dispatch 是 click-bubbling 正常行为，onClose 幂等处理得当。

## Test plan

- [x] 31/31 通过
- [x] tsc clean (只剩 knip.config pre-existing)
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 11 (#905)
- 剩余: ModelSelector (381) / FeedbackDialog (337) / GuideTourModal (418) / ArchivedSessionPanel (301)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T06:47:31Z): /lgtm

---

## 19f5a5d

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T06:41:19Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/19f5a5dcb85e0163707c42a23387fa811bdc4933](https://github.com/SerendipityOneInc/ecap-workspace/commit/19f5a5dcb85e0163707c42a23387fa811bdc4933)

### Commit Message
```
ci(dependabot): group pip minor/patch updates to cut CI trigger count (#1167)

## Summary

3 行改动：pip ecosystem 加 \`groups.minor-and-patch\`，和 npm 已有配置对称。

## 动机（merge queue 加速收尾 PR）

之前每周 \`requirements.txt\` 的 N 个 minor/patch 更新 → N 个独立 dependabot PR → N
次完整 \`claw-interface-quality\` CI run（每次 ~130-160s）。加 groups 后一周累积的非
breaking pip 更新合成 1 个 PR，N 次 CI 压到 1 次。

按一周 3-5 个 pip 更新的历史频率估算，单纯 dependabot 噪音减少 **每周 ~5-10 分钟 CI 时长 + 4-5 个
review 干扰**。

breaking（major）更新不被 group，仍然独立 PR——因为它们需要真人判断是否升级。

## 系列进度（CI acceleration 全景）

- [x] PR #1159: \`web-quality\` 升 \`ubuntu-latest-m\`（已合）
- [x] PR #1160: ESLint cache + tsc incremental + Vitest threads（已合）
- [x] srp-actions #59: \`pytest_args\` input + ruff cache（已合）
- [ ] PR #1165: pytest-xdist + per-worker mongo DB + logging test
fix（APPROVED + CLEAN，等手动 merge）
- [ ] PR #1167（本 PR）: dependabot pip groups（收尾）

## Out of scope（follow-ups）

- **iOS（Phase 2）**：merge queue 关键路径 95%+ 瓶颈，单独讨论；方案候选
\`macos-15-xlarge\` 或 self-hosted M-class
- **Issue #1166**: \`TestConfigureLogging\` 行为式重写（根治 PR #1165 里的生产代码让步）
- **code-quality.yml install dedup**: \`asset-size-guard\` 和
\`web-quality\` 共用 pnpm install（改 check 名字，需 branch protection 协调，未做）

## Test plan

- [ ] 本 PR CI 绿（只改配置文件，影响最小）
- [ ] 下周第一次 dependabot 触发时观察 pip PR：应该是 1 个合并 PR 而非 N 个单独 PR
- [ ] 若任何 pip 更新在 group 里 break，fallback 方案：改 \`groups\` 粒度（如按
\`dependency-type: "production"\` vs "development" 拆两 group）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1167: ci(dependabot): group pip minor/patch updates to cut CI trigger count

## Summary

3 行改动：pip ecosystem 加 \`groups.minor-and-patch\`，和 npm 已有配置对称。

## 动机（merge queue 加速收尾 PR）

之前每周 \`requirements.txt\` 的 N 个 minor/patch 更新 → N 个独立 dependabot PR → N 次完整 \`claw-interface-quality\` CI run（每次 ~130-160s）。加 groups 后一周累积的非 breaking pip 更新合成 1 个 PR，N 次 CI 压到 1 次。

按一周 3-5 个 pip 更新的历史频率估算，单纯 dependabot 噪音减少 **每周 ~5-10 分钟 CI 时长 + 4-5 个 review 干扰**。

breaking（major）更新不被 group，仍然独立 PR——因为它们需要真人判断是否升级。

## 系列进度（CI acceleration 全景）

- [x] PR #1159: \`web-quality\` 升 \`ubuntu-latest-m\`（已合）
- [x] PR #1160: ESLint cache + tsc incremental + Vitest threads（已合）
- [x] srp-actions #59: \`pytest_args\` input + ruff cache（已合）
- [ ] PR #1165: pytest-xdist + per-worker mongo DB + logging test fix（APPROVED + CLEAN，等手动 merge）
- [ ] PR #1167（本 PR）: dependabot pip groups（收尾）

## Out of scope（follow-ups）

- **iOS（Phase 2）**：merge queue 关键路径 95%+ 瓶颈，单独讨论；方案候选 \`macos-15-xlarge\` 或 self-hosted M-class
- **Issue #1166**: \`TestConfigureLogging\` 行为式重写（根治 PR #1165 里的生产代码让步）
- **code-quality.yml install dedup**: \`asset-size-guard\` 和 \`web-quality\` 共用 pnpm install（改 check 名字，需 branch protection 协调，未做）

## Test plan

- [ ] 本 PR CI 绿（只改配置文件，影响最小）
- [ ] 下周第一次 dependabot 触发时观察 pip PR：应该是 1 个合并 PR 而非 N 个单独 PR
- [ ] 若任何 pip 更新在 group 里 break，fallback 方案：改 \`groups\` 粒度（如按 \`dependency-type: "production"\` vs "development" 拆两 group）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T06:41:09Z): /lgtm

---

## 3a56acc

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T06:34:18Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/3a56acc950b6ff008781c4916300cce8dd30cbdc](https://github.com/SerendipityOneInc/ecap-workspace/commit/3a56acc950b6ff008781c4916300cce8dd30cbdc)

### Commit Message
```
ci(python): parallel pytest with xdist + upgrade claw-interface runner (#1165)

## Summary

Merge-queue acceleration 系列第 3 个 PR。本地实测定型为 **\`-n 4 --dist
loadfile\`**：

| 模式 | pytest 内时长 | 加速 |
|---|---|---|
| Sequential baseline | 26.47s | — |
| \`-n auto\` (29 workers) | 31.66s | **-20% ❌** 过多 worker 启动开销 |
| \`-n 8\` | 17.88s | +32% |
| **\`-n 4\`** | **17.80s** | **+32%** |

## Changes

1. **workflow caller** 传 \`runner_name: ubuntu-latest-m\` +
\`pytest_args: '-n 4 --dist loadfile'\`
2. **requirements-dev.txt** 加 \`pytest-xdist>=3.6\`
3. **pyproject.toml [tool.deptry.per_rule_ignores]** 把 pytest-xdist
加入"pytest plugins"白名单（通过 CLI 激活，不 import）
4. **tests/unit/test_app_logging.py** fix 一个被并行暴露的预存 isolation bug：

\`TestConfigureLogging\` 多个测试
\`patch("app.app_logging.logging.StreamHandler")\` 把 stdlib
StreamHandler 替换成 MagicMock。但 \`configure_logging\` 内部调用的
\`_suppress_noisy_loggers\` 会做 \`isinstance(h,
logging.StreamHandler)\`——MagicMock 不能当 isinstance 参数就 TypeError。
    
顺序跑时，运行到 \`TestConfigureLogging\` 之前还没测试触发那些 noisy loggers 挂
handlers，list comprehension 空跑避开了 isinstance。xdist 下**同一 worker
先跑其他测试**，noisy logger handlers 被填满就炸。
    
修法：类级 autouse fixture stub 掉 \`_suppress_noisy_loggers\`，让
\`TestConfigureLogging\` 只关心自己的职责；\`TestSuppressNoisyLoggers\` 继续验证真实实现。

## 依赖

- **srp-actions #59** ✅ 已合并（添加 \`pytest_args\` input + ruff cache）
- 现有 caller 继续保持默认（pytest_args=''），不受影响

## Mongo 并发担心

用户合理的质疑——\`-n\` 下多个 worker 共享同一 mongo container 是否会 race。结论：\`--dist
loadfile\` 策略保证**同一个 test file 内的测试串行**（BDD feature 文件内部安全），实测 2557
tests 全过，没有 mongo 相关新失败。未来如果出现跨文件 mongo race，迁移方案是在 repo 测试 infra 里加
worker-scoped database name。本 PR 不涉及。

## 预期 CI 影响

claw-interface-quality 从 ~160s 降到 ~125-135s：
- Runner 升级 (\`ubuntu-latest-m\`): ~10-15s
- Ruff cache（从 srp-actions #59 自动生效）: 冷 run 不受益，第二次起 ~5-10s
- pytest-xdist \`-n 4\`: ~8-10s

## 系列进度

- [x] PR #1 (#1159): runner 升级 (merged)
- [ ] PR #2 (#1160): Web 缓存 + Vitest 并行（APPROVED + CLEAN，等你手动 merge）
- [x] srp-actions #59: pytest_args input + ruff cache (merged)
- [ ] PR #3 (本 PR): Python 并行 + runner 升级
- [ ] PR #4: 共用 pnpm cache + Dependabot groups（收尾）

## Test plan

- [x] 本地 \`pytest tests -n 4 --dist loadfile\`: 2557 passed, 368
skipped, 18.29s
- [x] 本地 \`ruff check\` / \`ruff format --check\`: 通过
- [x] 本地 \`pyright app tests\`: 0 errors
- [x] 本地 \`bash scripts/ci-lint/*.sh\`: 6 个脚本全过
- [ ] CI: claw-interface-quality 第一次 run 数据（无 ruff cache 命中）对比 baseline
160s
- [ ] CI: 下一次触及 \`services/claw-interface/**\` 的 PR 时应看到 ruff cache 生效

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## Follow-up

- #1166: refactor TestConfigureLogging to behavior-based assertions（根治
commit 3 的生产代码让步，D 方案）

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1165: ci(python): parallel pytest with xdist + upgrade claw-interface runner

## Summary

Merge-queue acceleration 系列第 3 个 PR。本地实测定型为 **\`-n 4 --dist loadfile\`**：

| 模式 | pytest 内时长 | 加速 |
|---|---|---|
| Sequential baseline | 26.47s | — |
| \`-n auto\` (29 workers) | 31.66s | **-20% ❌** 过多 worker 启动开销 |
| \`-n 8\` | 17.88s | +32% |
| **\`-n 4\`** | **17.80s** | **+32%** |

## Changes

1. **workflow caller** 传 \`runner_name: ubuntu-latest-m\` + \`pytest_args: '-n 4 --dist loadfile'\`
2. **requirements-dev.txt** 加 \`pytest-xdist>=3.6\`
3. **pyproject.toml [tool.deptry.per_rule_ignores]** 把 pytest-xdist 加入"pytest plugins"白名单（通过 CLI 激活，不 import）
4. **tests/unit/test_app_logging.py** fix 一个被并行暴露的预存 isolation bug：

    \`TestConfigureLogging\` 多个测试 \`patch("app.app_logging.logging.StreamHandler")\` 把 stdlib StreamHandler 替换成 MagicMock。但 \`configure_logging\` 内部调用的 \`_suppress_noisy_loggers\` 会做 \`isinstance(h, logging.StreamHandler)\`——MagicMock 不能当 isinstance 参数就 TypeError。
    
    顺序跑时，运行到 \`TestConfigureLogging\` 之前还没测试触发那些 noisy loggers 挂 handlers，list comprehension 空跑避开了 isinstance。xdist 下**同一 worker 先跑其他测试**，noisy logger handlers 被填满就炸。
    
    修法：类级 autouse fixture stub 掉 \`_suppress_noisy_loggers\`，让 \`TestConfigureLogging\` 只关心自己的职责；\`TestSuppressNoisyLoggers\` 继续验证真实实现。

## 依赖

- **srp-actions #59** ✅ 已合并（添加 \`pytest_args\` input + ruff cache）
- 现有 caller 继续保持默认（pytest_args=''），不受影响

## Mongo 并发担心

用户合理的质疑——\`-n\` 下多个 worker 共享同一 mongo container 是否会 race。结论：\`--dist loadfile\` 策略保证**同一个 test file 内的测试串行**（BDD feature 文件内部安全），实测 2557 tests 全过，没有 mongo 相关新失败。未来如果出现跨文件 mongo race，迁移方案是在 repo 测试 infra 里加 worker-scoped database name。本 PR 不涉及。

## 预期 CI 影响

claw-interface-quality 从 ~160s 降到 ~125-135s：
- Runner 升级 (\`ubuntu-latest-m\`): ~10-15s
- Ruff cache（从 srp-actions #59 自动生效）: 冷 run 不受益，第二次起 ~5-10s
- pytest-xdist \`-n 4\`: ~8-10s

## 系列进度

- [x] PR #1 (#1159): runner 升级 (merged)
- [ ] PR #2 (#1160): Web 缓存 + Vitest 并行（APPROVED + CLEAN，等你手动 merge）
- [x] srp-actions #59: pytest_args input + ruff cache (merged)
- [ ] PR #3 (本 PR): Python 并行 + runner 升级
- [ ] PR #4: 共用 pnpm cache + Dependabot groups（收尾）

## Test plan

- [x] 本地 \`pytest tests -n 4 --dist loadfile\`: 2557 passed, 368 skipped, 18.29s
- [x] 本地 \`ruff check\` / \`ruff format --check\`: 通过
- [x] 本地 \`pyright app tests\`: 0 errors
- [x] 本地 \`bash scripts/ci-lint/*.sh\`: 6 个脚本全过
- [ ] CI: claw-interface-quality 第一次 run 数据（无 ruff cache 命中）对比 baseline 160s
- [ ] CI: 下一次触及 \`services/claw-interface/**\` 的 PR 时应看到 ruff cache 生效

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## Follow-up

- #1166: refactor TestConfigureLogging to behavior-based assertions（根治 commit 3 的生产代码让步，D 方案）

### Human Comments
- **chris-srp** (2026-04-22T06:34:08Z): /lgtm

---

## 5d7f6ae

**作者**: peter-srp
**日期**: 2026-04-22T06:03:17Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/5d7f6aef3a6a2e1f3277aeb45d2f45eecf9d90c1](https://github.com/SerendipityOneInc/ecap-workspace/commit/5d7f6aef3a6a2e1f3277aeb45d2f45eecf9d90c1)

### Commit Message
```
fix(chat): validate message length & file count, retry MM backfill (#1161)

## Summary
Three product-logic fixes discovered via Sentry deep-dive analysis:

- **Message length validation** — `sendPost()` now pre-validates against
Mattermost's 4000-char limit before hitting the server. Previously,
oversized messages silently failed with a cryptic server error. Error
now surfaces as a toast through the existing `mm.error` chain.
- **File count limit** — `GenClawInput` now enforces a
10-file-per-message limit (Mattermost server constraint) at the UI layer
before upload starts. Added `CHAT_MAX_FILE_COUNT` constant and i18n
keys. `sendPost()` has a belt-and-suspenders guard.
- **Backfill retry** — `fetchMissedMessages()` now retries up to 2 times
with exponential backoff (1s → 2s) before reporting `backfill_failed` to
Sentry. Previously, a single network hiccup left permanent message gaps
for the session.

### Sentry issues addressed
| Issue | Events (7d) | Users | Fix |
|-------|-------------|-------|-----|
| `MattermostError: Post Message too long` | 5 | 1 | Pre-validate length
|
| `MattermostError: 上传只允许最多10个文件` | 1 | 1 | UI + API guard |
| `backfill_failed — Failed to fetch` | 47 | 16 | Retry with backoff |

## Test plan
- [ ] `tsc --noEmit` passes (confirmed locally)
- [ ] ESLint passes (confirmed via pre-commit hook)
- [ ] Full test suite passes: 238 files, 3712 tests
- [ ] Verify message > 4000 chars shows toast error (not silent failure)
- [ ] Verify > 10 file uploads are blocked with alert before upload
starts
- [ ] Monitor `backfill_failed` events in Sentry — expect significant
reduction

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR #1161: fix(chat): validate message length & file count, retry MM backfill

## Summary
Three product-logic fixes discovered via Sentry deep-dive analysis:

- **Message length validation** — `sendPost()` now pre-validates against Mattermost's 4000-char limit before hitting the server. Previously, oversized messages silently failed with a cryptic server error. Error now surfaces as a toast through the existing `mm.error` chain.
- **File count limit** — `GenClawInput` now enforces a 10-file-per-message limit (Mattermost server constraint) at the UI layer before upload starts. Added `CHAT_MAX_FILE_COUNT` constant and i18n keys. `sendPost()` has a belt-and-suspenders guard.
- **Backfill retry** — `fetchMissedMessages()` now retries up to 2 times with exponential backoff (1s → 2s) before reporting `backfill_failed` to Sentry. Previously, a single network hiccup left permanent message gaps for the session.

### Sentry issues addressed
| Issue | Events (7d) | Users | Fix |
|-------|-------------|-------|-----|
| `MattermostError: Post Message too long` | 5 | 1 | Pre-validate length |
| `MattermostError: 上传只允许最多10个文件` | 1 | 1 | UI + API guard |
| `backfill_failed — Failed to fetch` | 47 | 16 | Retry with backoff |

## Test plan
- [ ] `tsc --noEmit` passes (confirmed locally)
- [ ] ESLint passes (confirmed via pre-commit hook)
- [ ] Full test suite passes: 238 files, 3712 tests
- [ ] Verify message > 4000 chars shows toast error (not silent failure)
- [ ] Verify > 10 file uploads are blocked with alert before upload starts
- [ ] Monitor `backfill_failed` events in Sentry — expect significant reduction

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **peter-srp** (2026-04-22T06:02:59Z): /lgtm

---

## 49f1b5c

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T05:54:24Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/49f1b5cff3aae3c503f5eb1f7536e768c53f05f4](https://github.com/SerendipityOneInc/ecap-workspace/commit/49f1b5cff3aae3c503f5eb1f7536e768c53f05f4)

### Commit Message
```
ci(web): cache ESLint + tsc incremental + Vitest threads pool (#1160)

## Summary

三项互相叠加的提速，全部本地测过：

| 改动 | 首次 | 缓存后 | 加速 |
|---|---|---|---|
| ESLint `--cache --cache-strategy content` | 39.4s | 7.0s | **5.6×
(-32s)** |
| tsc `--noEmit`（tsconfig 已有 `incremental: true`，只需跨 run 持久化
`tsconfig.tsbuildinfo`） | 27.4s | 10.6s | **2.6× (-17s)** |
| Vitest `pool: 'threads'`（默认 `forks`） | — | 17.2s wall-clock, 238 files
/ 3712 tests | 启动 overhead -1~3s，threads 并行效率高 |

## GitHub Actions 缓存策略

Evolving key：
- `key:
web-lint-tsc-{OS}-{hash(pnpm-lock+eslint-config+tsconfig)}-{run_id}` —
每次 run 独立，始终保存
- `restore-keys`: 两层 fallback，优先同 hash 前缀命中；降级到 OS 前缀

失效条件：`pnpm-lock.yaml` / `eslint.config.mjs` / `tsconfig.json` 任一改动。

## 配套关系

- PR #1 (#1159) 把 runner 升级到 `ubuntu-latest-m`，解锁更多 CPU
- 本 PR 的 Vitest threads pool 本地测到 **CPU 使用 2031%**（即 ~20 核并行）——只有升级后的
runner 能真正吃满
- 两者**相辅相成**：PR #1 给硬件，PR #2 给软件利用率

## Caveats

- 首次 CI run 没 cache 命中，时长和基线持平；**第二次 run 开始见收益**
- Cache 总量：ESLint 510KB + tsconfig.tsbuildinfo 4.9MB ≈ 5.5MB，远低于 GHA 单缓存
5GB 上限
- 若 ESLint cache 误报失效导致 lint 变慢，可以 bump `eslint.config.mjs` 的一行注释作为
cache 清理手段

## 系列进度

- [x] PR #1 (#1159): runner 升级（auto-merge 启用中）
- [x] PR #2 (本 PR): Web 缓存 + Vitest 并行
- [ ] PR #3: Python 侧 pytest-xdist + uv cache + ruff cache（需联动
srp-actions）
- [ ] PR #4: 共用 pnpm cache + Dependabot groups

## Test plan

- [ ] 本 PR 第一次 CI run：web-quality 时长应不显著变差（cache miss 是期待的）
- [ ] 合并后第二次触及 `web/**` 的 PR：web-quality 时长应下降 ~40-50s
- [ ] 对比 \`gh api
repos/SerendipityOneInc/ecap-workspace/actions/runs/<id>/jobs | jq
'.jobs[] | select(.name==\"web-quality\") | .steps[] | {name,
conclusion, started_at, completed_at}'\` 检查单步耗时
- [x] 本地 \`pnpm lint\` / \`npx tsc --noEmit\` / \`pnpm test:unit\` 均通过

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1160: ci(web): cache ESLint + tsc incremental + Vitest threads pool

## Summary

三项互相叠加的提速，全部本地测过：

| 改动 | 首次 | 缓存后 | 加速 |
|---|---|---|---|
| ESLint `--cache --cache-strategy content` | 39.4s | 7.0s | **5.6× (-32s)** |
| tsc `--noEmit`（tsconfig 已有 `incremental: true`，只需跨 run 持久化 `tsconfig.tsbuildinfo`） | 27.4s | 10.6s | **2.6× (-17s)** |
| Vitest `pool: 'threads'`（默认 `forks`） | — | 17.2s wall-clock, 238 files / 3712 tests | 启动 overhead -1~3s，threads 并行效率高 |

## GitHub Actions 缓存策略

Evolving key：
- `key: web-lint-tsc-{OS}-{hash(pnpm-lock+eslint-config+tsconfig)}-{run_id}` — 每次 run 独立，始终保存
- `restore-keys`: 两层 fallback，优先同 hash 前缀命中；降级到 OS 前缀

失效条件：`pnpm-lock.yaml` / `eslint.config.mjs` / `tsconfig.json` 任一改动。

## 配套关系

- PR #1 (#1159) 把 runner 升级到 `ubuntu-latest-m`，解锁更多 CPU
- 本 PR 的 Vitest threads pool 本地测到 **CPU 使用 2031%**（即 ~20 核并行）——只有升级后的 runner 能真正吃满
- 两者**相辅相成**：PR #1 给硬件，PR #2 给软件利用率

## Caveats

- 首次 CI run 没 cache 命中，时长和基线持平；**第二次 run 开始见收益**
- Cache 总量：ESLint 510KB + tsconfig.tsbuildinfo 4.9MB ≈ 5.5MB，远低于 GHA 单缓存 5GB 上限
- 若 ESLint cache 误报失效导致 lint 变慢，可以 bump `eslint.config.mjs` 的一行注释作为 cache 清理手段

## 系列进度

- [x] PR #1 (#1159): runner 升级（auto-merge 启用中）
- [x] PR #2 (本 PR): Web 缓存 + Vitest 并行
- [ ] PR #3: Python 侧 pytest-xdist + uv cache + ruff cache（需联动 srp-actions）
- [ ] PR #4: 共用 pnpm cache + Dependabot groups

## Test plan

- [ ] 本 PR 第一次 CI run：web-quality 时长应不显著变差（cache miss 是期待的）
- [ ] 合并后第二次触及 `web/**` 的 PR：web-quality 时长应下降 ~40-50s
- [ ] 对比 \`gh api repos/SerendipityOneInc/ecap-workspace/actions/runs/<id>/jobs | jq '.jobs[] | select(.name==\"web-quality\") | .steps[] | {name, conclusion, started_at, completed_at}'\` 检查单步耗时
- [x] 本地 \`pnpm lint\` / \`npx tsc --noEmit\` / \`pnpm test:unit\` 均通过

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T05:36:53Z): /lgtm

---

## 6a5b801

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T05:35:46Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/6a5b8014edff8d4e0695ce115d872289c0bc7833](https://github.com/SerendipityOneInc/ecap-workspace/commit/6a5b8014edff8d4e0695ce115d872289c0bc7833)

### Commit Message
```
test(web): FeedbackProvider 全面覆盖 (#894 Step 11 补) (#1150)

## Summary

Epic #894 Step 11 (#905) — \`FeedbackProvider.tsx\` (176 LOC) 从 0% →
全分支，21 tests，零源码改动。

## 新增 21 个测试

| 组 | # | 覆盖 |
|---|---|---|
| Context hooks | 3 | useFeedback 外 provider 抛 / 内返上下文 / useHealthStatus
subscribe 重渲染 |
| HealthMonitor 生命周期 | 2 | mount new + subscribe / unmount destroy +
unsubscribe |
| Sentry user identity | 3 | uid + phone_number 优先 / fallback phone / 无
uid → clearSentryUser |
| Dialog open/close | 5 | 初始关 / openDialog hook / closeDialog →
acknowledge / FAB toggle open/close |
| reportCrash flow | 2 | monitor.reportCrash + crashInfo 传 dialog /
close 后 crashInfo 清 |
| ErrorBoundary bridge | 2 | mount 后直通 / mount 前 queued + replay |
| Window error listeners | 3 | error / unhandledrejection / unmount 清理 |

## Harness 要点

- **HealthMonitor mock 必须是真 class**：arrow-function `vi.fn()` 不支持
`new`，源码 `new HealthMonitor()` 会抛 `is not a constructor`
- **ErrorBoundary bridge + `act()`**：`reportCrashFromErrorBoundary` 在
React 外调用，setState 不自动 batch，assertion 前须 `act()` 包起来
- **Module-level pending queue**：`pendingCrashes` 在文件级定义，测试顺序敏感。BEFORE
mount 测试先 push 再 mount

## Bug-hunting

无新发现。`longtask` observer 的 try/catch（浏览器不支持 longtask 类型时 gracefully
退出）没测 — 属于环境分支，生产 jsdom 里 PerformanceObserver 没 longtask 支持，当前测试通过观察
observer 不 crash 间接覆盖。

## Test plan

- [x] 21/21 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 11 (#905)
- 剩余：ModelSelector (381) / FeedbackDialog (337) / GuideTourModal (418) /
ImagePreview (257) / ArchivedSessionPanel (301)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1150: test(web): FeedbackProvider 全面覆盖 (#894 Step 11 补)

## Summary

Epic #894 Step 11 (#905) — \`FeedbackProvider.tsx\` (176 LOC) 从 0% → 全分支，21 tests，零源码改动。

## 新增 21 个测试

| 组 | # | 覆盖 |
|---|---|---|
| Context hooks | 3 | useFeedback 外 provider 抛 / 内返上下文 / useHealthStatus subscribe 重渲染 |
| HealthMonitor 生命周期 | 2 | mount new + subscribe / unmount destroy + unsubscribe |
| Sentry user identity | 3 | uid + phone_number 优先 / fallback phone / 无 uid → clearSentryUser |
| Dialog open/close | 5 | 初始关 / openDialog hook / closeDialog → acknowledge / FAB toggle open/close |
| reportCrash flow | 2 | monitor.reportCrash + crashInfo 传 dialog / close 后 crashInfo 清 |
| ErrorBoundary bridge | 2 | mount 后直通 / mount 前 queued + replay |
| Window error listeners | 3 | error / unhandledrejection / unmount 清理 |

## Harness 要点

- **HealthMonitor mock 必须是真 class**：arrow-function `vi.fn()` 不支持 `new`，源码 `new HealthMonitor()` 会抛 `is not a constructor`
- **ErrorBoundary bridge + `act()`**：`reportCrashFromErrorBoundary` 在 React 外调用，setState 不自动 batch，assertion 前须 `act()` 包起来
- **Module-level pending queue**：`pendingCrashes` 在文件级定义，测试顺序敏感。BEFORE mount 测试先 push 再 mount

## Bug-hunting

无新发现。`longtask` observer 的 try/catch（浏览器不支持 longtask 类型时 gracefully 退出）没测 — 属于环境分支，生产 jsdom 里 PerformanceObserver 没 longtask 支持，当前测试通过观察 observer 不 crash 间接覆盖。

## Test plan

- [x] 21/21 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 11 (#905)
- 剩余：ModelSelector (381) / FeedbackDialog (337) / GuideTourModal (418) / ImagePreview (257) / ArchivedSessionPanel (301)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T05:35:35Z): /lgtm

---

## 599e328

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T05:05:34Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/599e3288a9f935dab4e80a26d4fc453910b10d64](https://github.com/SerendipityOneInc/ecap-workspace/commit/599e3288a9f935dab4e80a26d4fc453910b10d64)

### Commit Message
```
ci(web): upgrade web-quality runner to ubuntu-latest-m (#1159)

## Summary

- web-quality job 从 `ubuntu-latest` 升级到 `ubuntu-latest-m`（org 已有的 larger
runner，`service-deploy.yml` 已在用）
- 该 job 内部 install + lint + tsc + vitest + jscpd 全部串行执行且 CPU-bound，单个
runner 升级直接换时长
- 预期：merge queue 下 web-quality 从 ~180s 降到 ~90-120s

## 背景（merge queue 加速系列）

merge queue 高吞吐场景下，`code-quality` workflow 的关键路径时长直接决定合并队列吞吐。分析见本地 plan
文件。本 PR 是 4 个小 PR 系列的第 1 个（最小风险、最快收益）：

- PR #1（本 PR）：runner 升级
- PR #2：Web 侧 ESLint cache + Vitest pool + tsc incremental +
`.eslintcache` / `.tsbuildinfo` actions/cache
- PR #3：Python 侧 pytest-xdist + uv cache + ruff cache + runner 升级（需联动
srp-actions）
- PR #4：共用 pnpm cache 粒度 + Dependabot groups

iOS 侧（merge queue 关键路径 95%+ 的瓶颈）作为二阶段单独评估，不在本系列内。

## Test plan

- [ ] PR 自身 CI 绿（本 PR 只改 web-quality 的 runner label，其他 job 不受影响）
- [ ] 对比最近 3 次 main 分支 run 的 web-quality 时长 vs 本 PR 合并后接下来 3 次
merge_group run 的 web-quality 时长
- [ ] 取 timing: \`gh api
repos/SerendipityOneInc/ecap-workspace/actions/runs/<id>/jobs | jq
'.jobs[] | select(.name==\"web-quality\") | {started_at,
completed_at}'\`
- [ ] 若 `ubuntu-latest-m` 不可用（job 卡在 "Waiting for a runner"），回退到
`ubuntu-latest`

## Caveats

- 未升级 `claw-interface-quality` 的 runner——它是 srp-actions 的 reusable
workflow，需要对端加 `runner` input，放在 PR #3
- 未升级 `asset-size-guard` 和 `ios-quality`——前者 44s 不值得，后者 macOS 计费另当别论

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1159: ci(web): upgrade web-quality runner to ubuntu-latest-m

## Summary

- web-quality job 从 `ubuntu-latest` 升级到 `ubuntu-latest-m`（org 已有的 larger runner，`service-deploy.yml` 已在用）
- 该 job 内部 install + lint + tsc + vitest + jscpd 全部串行执行且 CPU-bound，单个 runner 升级直接换时长
- 预期：merge queue 下 web-quality 从 ~180s 降到 ~90-120s

## 背景（merge queue 加速系列）

merge queue 高吞吐场景下，`code-quality` workflow 的关键路径时长直接决定合并队列吞吐。分析见本地 plan 文件。本 PR 是 4 个小 PR 系列的第 1 个（最小风险、最快收益）：

- PR #1（本 PR）：runner 升级
- PR #2：Web 侧 ESLint cache + Vitest pool + tsc incremental + `.eslintcache` / `.tsbuildinfo` actions/cache
- PR #3：Python 侧 pytest-xdist + uv cache + ruff cache + runner 升级（需联动 srp-actions）
- PR #4：共用 pnpm cache 粒度 + Dependabot groups

iOS 侧（merge queue 关键路径 95%+ 的瓶颈）作为二阶段单独评估，不在本系列内。

## Test plan

- [ ] PR 自身 CI 绿（本 PR 只改 web-quality 的 runner label，其他 job 不受影响）
- [ ] 对比最近 3 次 main 分支 run 的 web-quality 时长 vs 本 PR 合并后接下来 3 次 merge_group run 的 web-quality 时长
- [ ] 取 timing: \`gh api repos/SerendipityOneInc/ecap-workspace/actions/runs/<id>/jobs | jq '.jobs[] | select(.name==\"web-quality\") | {started_at, completed_at}'\`
- [ ] 若 `ubuntu-latest-m` 不可用（job 卡在 "Waiting for a runner"），回退到 `ubuntu-latest`

## Caveats

- 未升级 `claw-interface-quality` 的 runner——它是 srp-actions 的 reusable workflow，需要对端加 `runner` input，放在 PR #3
- 未升级 `asset-size-guard` 和 `ios-quality`——前者 44s 不值得，后者 macOS 计费另当别论

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **chris-srp** (2026-04-22T05:05:23Z): /lgtm

---

## 11507a6

**作者**: Chris@ZooClaw
**日期**: 2026-04-22T04:30:50Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/11507a6b35385a9237edd2d7c1f657025c8b8bd3](https://github.com/SerendipityOneInc/ecap-workspace/commit/11507a6b35385a9237edd2d7c1f657025c8b8bd3)

### Commit Message
```
chore(pnpm): add minimumReleaseAge for supply-chain hardening (#1158)

## Summary
- Add `minimumReleaseAge: 10080` (7 days, pnpm's unit is minutes) to
`pnpm-workspace.yaml`
- Delays installing freshly-published versions so compromised releases
have time to be detected and yanked before entering our dependency tree
- Supported by pnpm 10.16+ (repo is on 10.26.2 via `packageManager` in
`web/package.json`)

## Test plan
- [ ] `pnpm install` still resolves against the existing lockfile
(cooldown only affects *new* resolves)
- [ ] `pnpm add lodash@latest --dry-run` is rejected if latest was
published <7 days ago
- [ ] CI `code-quality / lint-and-test` stays green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1158: chore(pnpm): add minimumReleaseAge for supply-chain hardening

## Summary
- Add `minimumReleaseAge: 10080` (7 days, pnpm's unit is minutes) to `pnpm-workspace.yaml`
- Delays installing freshly-published versions so compromised releases have time to be detected and yanked before entering our dependency tree
- Supported by pnpm 10.16+ (repo is on 10.26.2 via `packageManager` in `web/package.json`)

## Test plan
- [ ] `pnpm install` still resolves against the existing lockfile (cooldown only affects *new* resolves)
- [ ] `pnpm add lodash@latest --dry-run` is rejected if latest was published <7 days ago
- [ ] CI `code-quality / lint-and-test` stays green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## d9b8e4b

**作者**: bill-srp
**日期**: 2026-04-22T04:16:31Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/d9b8e4b66c7a41e15ab667097eb14c5e7e83bce1](https://github.com/SerendipityOneInc/ecap-workspace/commit/d9b8e4b66c7a41e15ab667097eb14c5e7e83bce1)

### Commit Message
```
feat(ios): Replace ExyteChat with custom ChatListView and overlay input (#1156)

## Summary

- **Replace ExyteChat** (9,500-line library) with a custom
`ChatListView` (~220 lines) using an inverted `UITableView` with
`UIHostingConfiguration` cells
- **New `ComposeInputPanel`** — reusable 3-row input component
(attachments, text, toolbar) used by both text and voice modes
- **Overlay input architecture** — `ChatInputView` is overlaid on the
chat list (not in a VStack), enabling gradient backgrounds to fade over
chat content
- **Simplify `TextInputPanel`** — now a thin wrapper around
`ComposeInputPanel`
- **Simplify `VoiceInputPanel`** — stripped to match Figma design,
replaced programmatic `VoiceInputButton` with `recording_button` PNG
asset
- **Delete dead code** — `ExyteChatAdapter.swift`, most of
`VoiceInputButton.swift`
- Design spec:
`docs/superpowers/specs/2026-04-21-custom-chat-list-view.md`

**Stack:** 1/3 — independent, merge first. PR3 builds on this.

## Test plan

- [ ] Messages display in correct order (newest at bottom)
- [ ] Scroll-to-bottom button appears when scrolled up
- [ ] Keyboard dismisses on scroll
- [ ] Pagination loads older messages when scrolling to top
- [ ] Text input: type, attach, send all work
- [ ] Voice panel: record, transcribe, send work
- [ ] Empty state shows when no messages

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR #1156: feat(ios): Replace ExyteChat with custom ChatListView and overlay input

## Summary

- **Replace ExyteChat** (9,500-line library) with a custom `ChatListView` (~220 lines) using an inverted `UITableView` with `UIHostingConfiguration` cells
- **New `ComposeInputPanel`** — reusable 3-row input component (attachments, text, toolbar) used by both text and voice modes
- **Overlay input architecture** — `ChatInputView` is overlaid on the chat list (not in a VStack), enabling gradient backgrounds to fade over chat content
- **Simplify `TextInputPanel`** — now a thin wrapper around `ComposeInputPanel`
- **Simplify `VoiceInputPanel`** — stripped to match Figma design, replaced programmatic `VoiceInputButton` with `recording_button` PNG asset
- **Delete dead code** — `ExyteChatAdapter.swift`, most of `VoiceInputButton.swift`
- Design spec: `docs/superpowers/specs/2026-04-21-custom-chat-list-view.md`

**Stack:** 1/3 — independent, merge first. PR3 builds on this.

## Test plan

- [ ] Messages display in correct order (newest at bottom)
- [ ] Scroll-to-bottom button appears when scrolled up
- [ ] Keyboard dismisses on scroll
- [ ] Pagination loads older messages when scrolling to top
- [ ] Text input: type, attach, send all work
- [ ] Voice panel: record, transcribe, send work
- [ ] Empty state shows when no messages

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 37eb93c

**作者**: bill-srp
**日期**: 2026-04-22T04:16:27Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/37eb93c6f1dce7af13aff7e1f2cffb7cdaed7816](https://github.com/SerendipityOneInc/ecap-workspace/commit/37eb93c6f1dce7af13aff7e1f2cffb7cdaed7816)

### Commit Message
```
feat(ci): Add RC and App Store stages to iOS deploy pipeline (#1155)

## Summary

- Add RC (Release Candidate) and App Store upload stages to the iOS
deploy workflow
- Auto-bump build number in Xcode project after App Store upload
- Fix duplicate `ZooClaw.storekit` entry in pbxproj
- Add clean build step to avoid stale DerivedData on self-hosted runner

## Test plan

- [ ] TestFlight deploy succeeds from `rc/*` tag
- [ ] App Store upload succeeds from `release/*` tag
- [ ] Build number increments after upload
- [ ] Self-hosted runner builds cleanly from fresh state

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR #1155: feat(ci): Add RC and App Store stages to iOS deploy pipeline

## Summary

- Add RC (Release Candidate) and App Store upload stages to the iOS deploy workflow
- Auto-bump build number in Xcode project after App Store upload
- Fix duplicate `ZooClaw.storekit` entry in pbxproj
- Add clean build step to avoid stale DerivedData on self-hosted runner

## Test plan

- [ ] TestFlight deploy succeeds from `rc/*` tag
- [ ] App Store upload succeeds from `release/*` tag
- [ ] Build number increments after upload
- [ ] Self-hosted runner builds cleanly from fresh state

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 369faa3

**作者**: peter-srp
**日期**: 2026-04-22T03:25:05Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/369faa3eeac5ea2fcd834e13a92d1d7cd19e8cc1](https://github.com/SerendipityOneInc/ecap-workspace/commit/369faa3eeac5ea2fcd834e13a92d1d7cd19e8cc1)

### Commit Message
```
fix(sentry): prevent OpenClaw connection storm — breadcrumb-only for transient errors (#1154)

## Summary
- **OpenClaw connection monitor** (`openclawMonitor.ts`): transient
reasons (`abnormal_close`, `heartbeat_timeout`, `challenge_timeout`,
`handshake_timeout`) downgraded from `captureMessage` to breadcrumb-only
— same pattern that fixed the MM connection storm. Actionable reasons
(`reconnect_exhausted`, `ws_creation_failed`, `auth_missing`,
`handshake_rejected`) unchanged.
- **Network monitor** (`networkMonitor.ts`): added 5-minute dedup window
to `captureSocketError` — previously had zero dedup, producing ~500
duplicate `Socket mattermost disconnect` events/day.
- **MM channel misalignment** (`useMattermostIntegration.ts`):
downgraded from `captureMessage` to `addBreadcrumb` — this warning
auto-corrects and was generating ~2,400 events/day with no actionable
signal.

**Expected reduction: ~8,600 events/day (~60% of current Sentry
volume).**

### Context
Sentry health scan showed OpenClaw connection errors at 5,940 events/24h
from 184 users — the same trajectory as the MM `reconnect_exhausted`
storm (493K events) that burned through Sentry quota two weeks ago. The
root pattern is identical: transient WebSocket failures that self-heal
via reconnect, but each failure fires a `captureMessage` with only a
5-minute per-reason dedup window. With 184 concurrent users, this allows
up to 4,400 events/hour under network instability.

## Test plan
- [ ] Verify `tsc --noEmit` passes (confirmed locally)
- [ ] Verify ESLint passes (confirmed via pre-commit hook)
- [ ] `networkMonitor.unit.spec.ts` dedup test passes in CI
- [ ] Monitor Sentry event volume 24h post-deploy — expect drop from
~5,800 to ~2,000 events/day

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR #1154: fix(sentry): prevent OpenClaw connection storm — breadcrumb-only for transient errors

## Summary
- **OpenClaw connection monitor** (`openclawMonitor.ts`): transient reasons (`abnormal_close`, `heartbeat_timeout`, `challenge_timeout`, `handshake_timeout`) downgraded from `captureMessage` to breadcrumb-only — same pattern that fixed the MM connection storm. Actionable reasons (`reconnect_exhausted`, `ws_creation_failed`, `auth_missing`, `handshake_rejected`) unchanged.
- **Network monitor** (`networkMonitor.ts`): added 5-minute dedup window to `captureSocketError` — previously had zero dedup, producing ~500 duplicate `Socket mattermost disconnect` events/day.
- **MM channel misalignment** (`useMattermostIntegration.ts`): downgraded from `captureMessage` to `addBreadcrumb` — this warning auto-corrects and was generating ~2,400 events/day with no actionable signal.

**Expected reduction: ~8,600 events/day (~60% of current Sentry volume).**

### Context
Sentry health scan showed OpenClaw connection errors at 5,940 events/24h from 184 users — the same trajectory as the MM `reconnect_exhausted` storm (493K events) that burned through Sentry quota two weeks ago. The root pattern is identical: transient WebSocket failures that self-heal via reconnect, but each failure fires a `captureMessage` with only a 5-minute per-reason dedup window. With 184 concurrent users, this allows up to 4,400 events/hour under network instability.

## Test plan
- [ ] Verify `tsc --noEmit` passes (confirmed locally)
- [ ] Verify ESLint passes (confirmed via pre-commit hook)
- [ ] `networkMonitor.unit.spec.ts` dedup test passes in CI
- [ ] Monitor Sentry event volume 24h post-deploy — expect drop from ~5,800 to ~2,000 events/day

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### Human Comments
- **peter-srp** (2026-04-22T03:03:51Z): /lgtm

---

## d10ff0e

**作者**: nolan-srp
**日期**: 2026-04-22T03:05:09Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/d10ff0ef96e4277a10ab51f2ce5fc957a869a6fe](https://github.com/SerendipityOneInc/ecap-workspace/commit/d10ff0ef96e4277a10ab51f2ce5fc957a869a6fe)

### Commit Message
```
fix(claw-interface): harden openclaw agent settings config parsing (#1151)

## Summary
- add a shared FastClaw bot config parser that handles both flat and
nested payloads
- harden per-agent settings reads so malformed config entries degrade to
defaults instead of returning 500
- align cleanup and agent deploy reads with the same parser and add
focused unit coverage for nested and malformed config cases
```

### PR #1151: fix(claw-interface): harden openclaw agent settings config parsing

## Summary
- add a shared FastClaw bot config parser that handles both flat and nested payloads
- harden per-agent settings reads so malformed config entries degrade to defaults instead of returning 500
- align cleanup and agent deploy reads with the same parser and add focused unit coverage for nested and malformed config cases

---

## 2c5def7

**作者**: Fangmiao-srp
**日期**: 2026-04-22T02:27:26Z
**链接**: [https://github.com/SerendipityOneInc/ecap-workspace/commit/2c5def745e983a3f6a89c70c1b1fe515b56e4e94](https://github.com/SerendipityOneInc/ecap-workspace/commit/2c5def745e983a3f6a89c70c1b1fe515b56e4e94)

### Commit Message
```
refactor(web): normalize platform strings to web-desktop/web-mobile (#1152)

## Summary
- Simplify `platform` detection from 5 legacy values (`gensmo-ios-app`,
`gensmo-android-app`, `savyo-pc-web`, `savyo-mobile-web`,
`webview-android`) to 2 product-agnostic values (`web-desktop`,
`web-mobile`)
- Add `platform: getMetaPlatform()` to `getBaseEventParams()` in
`tracking.ts` so all GA4 events carry the normalized value
- Remove dead `setGensmoAppEnv()` function and its tests
- Clean up redundant platform assertions in test files

Sub-PR #4 of #1032.

## Test plan
- [x] All 24 user-agent unit tests pass (node + jsdom environments)
- [ ] Verify GA4 events in dev tools contain `platform: 'web-desktop'`
on desktop
- [ ] Verify GA4 events contain `platform: 'web-mobile'` on mobile UA

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Muyao Wang <muyao@MuyaodeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### PR #1152: refactor(web): normalize platform strings to web-desktop/web-mobile

## Summary
- Simplify `platform` detection from 5 legacy values (`gensmo-ios-app`, `gensmo-android-app`, `savyo-pc-web`, `savyo-mobile-web`, `webview-android`) to 2 product-agnostic values (`web-desktop`, `web-mobile`)
- Add `platform: getMetaPlatform()` to `getBaseEventParams()` in `tracking.ts` so all GA4 events carry the normalized value
- Remove dead `setGensmoAppEnv()` function and its tests
- Clean up redundant platform assertions in test files

Sub-PR #4 of #1032.

## Test plan
- [x] All 24 user-agent unit tests pass (node + jsdom environments)
- [ ] Verify GA4 events in dev tools contain `platform: 'web-desktop'` on desktop
- [ ] Verify GA4 events contain `platform: 'web-mobile'` on mobile UA

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---


## 2026-04-22


共 22 个 commits

## feat(web): render pptx OOXML tables (graphicFrame > a:tbl) (#1149)

- **SHA**: [3b09da9a](https://github.com/SerendipityOneInc/ecap-workspace/commit/3b09da9ac2f9c935d94a533754af840243e53156)
- **作者**: sam-srp
- **时间**: 2026-04-21T12:43:53Z
- **PR**: [#1149](https://github.com/SerendipityOneInc/ecap-workspace/pull/1149)

### Commit Message

feat(web): render pptx OOXML tables (graphicFrame > a:tbl) (#1149)

## Summary

Slides with real OOXML tables (`<p:graphicFrame>` containing `<a:tbl>`)
previously rendered a blank region where the table should be — our
renderer's dispatcher only handled `sp`/`pic`/`cxnSp`/`grpSp`. This PR
adds a fourth branch that flattens each `<a:tc>` cell into a synthetic
`SlideShape` (text + styled rect), positioned at its computed column/row
offset within the frame's bounding box.

Most common pptx cases now render with the right data: data tables,
feature matrices, schedules, etc.

## What's parsed

| XML | Produces |
|---|---|
| `<p:xfrm>/<a:off>/<a:ext>` | frame's slide-level position/size |
| `<a:tblGrid>/<a:gridCol w=…>` | column widths (scaled to fit
`frame.cx`) |
| `<a:tr h=…>` | row heights |
| `<a:tc>` | one cell per iteration |
| `<a:tcPr>/<a:solidFill>` | cell background color + alpha |
| `<a:tcPr>/<a:lnL/lnR/lnT/lnB>` | border (first side with a color wins;
uniform on all 4 sides) |
| `<a:tc>/<a:txBody>` | cell text via existing `extractParagraphs` |
| `<a:tc>/<a:bodyPr anchor=…>` | vertical alignment (defaults to middle)
|

## Known limits (not load-bearing, deferred)

- `gridSpan` / `rowSpan` (merged cells) — merged cells render as
separate cells
- Charts and SmartArt inside `graphicFrame` still render empty
- Per-side border differences collapse to uniform (cells in practice use
the same color on all four sides; 1px width makes the visual delta at
internal joins imperceptible)

## Test plan

- [ ] Open a deck with a data table → cells appear with text, fill,
borders
- [ ] Regression: decks without tables are unchanged
- [ ] Regression: existing pptx decks (no `graphicFrame`) render
identically

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Slides with real OOXML tables (`<p:graphicFrame>` containing `<a:tbl>`) previously rendered a blank region where the table should be — our renderer's dispatcher only handled `sp`/`pic`/`cxnSp`/`grpSp`. This PR adds a fourth branch that flattens each `<a:tc>` cell into a synthetic `SlideShape` (text + styled rect), positioned at its computed column/row offset within the frame's bounding box.

Most common pptx cases now render with the right data: data tables, feature matrices, schedules, etc.

## What's parsed

| XML | Produces |
|---|---|
| `<p:xfrm>/<a:off>/<a:ext>` | frame's slide-level position/size |
| `<a:tblGrid>/<a:gridCol w=…>` | column widths (scaled to fit `frame.cx`) |
| `<a:tr h=…>` | row heights |
| `<a:tc>` | one cell per iteration |
| `<a:tcPr>/<a:solidFill>` | cell background color + alpha |
| `<a:tcPr>/<a:lnL/lnR/lnT/lnB>` | border (first side with a color wins; uniform on all 4 sides) |
| `<a:tc>/<a:txBody>` | cell text via existing `extractParagraphs` |
| `<a:tc>/<a:bodyPr anchor=…>` | vertical alignment (defaults to middle) |

## Known limits (not load-bearing, deferred)

- `gridSpan` / `rowSpan` (merged cells) — merged cells render as separate cells
- Charts and SmartArt inside `graphicFrame` still render empty
- Per-side border differences collapse to uniform (cells in practice use the same color on all four sides; 1px width makes the visual delta at internal joins imperceptible)

## Test plan

- [ ] Open a deck with a data table → cells appear with text, fill, borders
- [ ] Regression: decks without tables are unchanged
- [ ] Regression: existing pptx decks (no `graphicFrame`) render identically

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## test(web): SizeSelector 全面覆盖 (#894 Step 11 补) (#1148)

- **SHA**: [a08dcaa9](https://github.com/SerendipityOneInc/ecap-workspace/commit/a08dcaa94ab98ecf5112d74392b4fe3df306c6d5)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-21T12:31:20Z
- **PR**: [#1148](https://github.com/SerendipityOneInc/ecap-workspace/pull/1148)

### Commit Message

test(web): SizeSelector 全面覆盖 (#894 Step 11 补) (#1148)

## Summary

Epic #894 Step 11 (#905) — 先补 SizeSelector.tsx (189 LOC) 从 0% → 全分支。26
tests，+2 行源码 export。

## 新增 26 个测试

| 分组 | # | 覆盖 |
|---|---|---|
| getSizeDimensions | 8 | auto / 5 种 ratio / malformed / 单段 / 零维度（gcd
无限递归守卫） |
| groupSizesByRatio | 2 | 按 ratio 分组 / 空输入 |
| 单选 pill | 2 | options.length===1 无 button / label 兜底 value |
| 多选下拉 | 9 | 默认关闭 / 点开 / 再点关 / 选项 click → onChange+关闭 / selected 样式 /
'auto' → "Auto" / 点外关 / 点内不关 / Escape 关 / 非 Escape 不关 |
| disabled | 1 | disabled=true 不响应 |
| Trigger label | 3 | 有 label / 无 label / value 找不到 → options[0] |

## Harness 要点

- 零维度守卫：`getSizeDimensions('0x512')` 触发 `parts[0]=0` 的 truthy check 失败 →
fall back Auto，避免 `gcd(0, 512)` 可能无限递归
- 下拉打开后有多个 button（trigger + 每个尺寸），cache trigger 引用避免
`getByRole('button')` 多匹配歧义

## Bug-hunting

无新发现。`getSizeDimensions` 的零值 guard 借助 `parts[0] && parts[1]` truthy
判断，行为合理。

## Test plan

- [x] 26/26 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 11 (#905)
- 剩余：ModelSelector (381) / FeedbackDialog (337) / FeedbackProvider (176)
/ GuideTourModal (418) / ImagePreview (257) / ArchivedSessionPanel
(301)，之后抬阈值 35 → 80

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Epic #894 Step 11 (#905) — 先补 SizeSelector.tsx (189 LOC) 从 0% → 全分支。26 tests，+2 行源码 export。

## 新增 26 个测试

| 分组 | # | 覆盖 |
|---|---|---|
| getSizeDimensions | 8 | auto / 5 种 ratio / malformed / 单段 / 零维度（gcd 无限递归守卫） |
| groupSizesByRatio | 2 | 按 ratio 分组 / 空输入 |
| 单选 pill | 2 | options.length===1 无 button / label 兜底 value |
| 多选下拉 | 9 | 默认关闭 / 点开 / 再点关 / 选项 click → onChange+关闭 / selected 样式 / 'auto' → "Auto" / 点外关 / 点内不关 / Escape 关 / 非 Escape 不关 |
| disabled | 1 | disabled=true 不响应 |
| Trigger label | 3 | 有 label / 无 label / value 找不到 → options[0] |

## Harness 要点

- 零维度守卫：`getSizeDimensions('0x512')` 触发 `parts[0]=0` 的 truthy check 失败 → fall back Auto，避免 `gcd(0, 512)` 可能无限递归
- 下拉打开后有多个 button（trigger + 每个尺寸），cache trigger 引用避免 `getByRole('button')` 多匹配歧义

## Bug-hunting

无新发现。`getSizeDimensions` 的零值 guard 借助 `parts[0] && parts[1]` truthy 判断，行为合理。

## Test plan

- [x] 26/26 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 11 (#905)
- 剩余：ModelSelector (381) / FeedbackDialog (337) / FeedbackProvider (176) / GuideTourModal (418) / ImagePreview (257) / ArchivedSessionPanel (301)，之后抬阈值 35 → 80

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@chris-srp: /lgtm

---

## test(web): AgentDetailClient 全面覆盖 (#894 Step 9 收尾) (#1144)

- **SHA**: [6f776be2](https://github.com/SerendipityOneInc/ecap-workspace/commit/6f776be2c6e2ac4380c5e851e9147a1819c70d65)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-21T11:36:08Z
- **PR**: [#1144](https://github.com/SerendipityOneInc/ecap-workspace/pull/1144)

### Commit Message

test(web): AgentDetailClient 全面覆盖 (#894 Step 9 收尾) (#1144)

## Summary

Epic #894 Step 9 (#903) — 最后一个未覆盖的文件：\`AgentDetailClient.tsx\` (608 LOC)
从 0% → 全分支。issue 明说覆盖关键 ~200 行（7 个 modal state + escape handler + lock
states）。31 tests, 零源码改动。

## 新增 31 个测试

| 组 | # | 覆盖 |
|---|---|---|
| 初始渲染 | 6 | loading / catalog 成功 / 无匹配 / reject / unmount race / bio 空时
description fallback |
| CTA 按钮 | 5 | 未 hired 只显示 Hire / hired 显示 Chat+Fire / has_update →
Update / !has_update 隐藏 / Chat router.push |
| Hire 流 | 5 | confirm modal / isLocked 禁用 / confirm → hireAgent+success
/ reject 无 success / "Go to chat" |
| Fire 流 | 4 | confirm modal + FIRE 输入门 / 错文字 disabled / "FIRE" enabled
+ fireAgent / reject |
| Update 流 | 6 | confirm / updateAgent+removeItem
CLAW_IDENTITY_CACHE+updated / reject / skip / Send /new → resetAgent /
isResetting 禁用+label |
| Escape | 2 | confirm → Escape 关 / success 优先级 > confirm |
| syncing | 1 | modal + button disabled |
| error banner | 1 | |

## Harness 要点

- **heavy imports stub** (ClawPageHeader / LocaleLink / AnimalAvatar) 成
testid div，专注 AgentDetailClient 状态机
- **"Panda Agent" 双重出现**：breadcrumb + h1，用 unique bio `'I am a panda.'`
做 waitFor anchor
- **`zooSquare.confirmFire` 严格匹配**：4 处元素同
prefix（Title/Desc/Prompt/button），必须用精确 string 避免 regex 误中

## Bug-hunting

无新发现。组件的 cancelled 标志防 setState-on-unmounted，7 modal 的 escape
优先级合理（success > confirm > fireConfirm > fired > updateConfirm >
updated，isResetting 守卫 updated）。

## Test plan

- [x] 31/31 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 9 (#903) 清单里其他文件（PublishAgentsClient /
SkillsSearchClient / SkillDetailClient / useAgentActions /
useCustomAgentPublishes / useUserAgents）已有测试；合入后 #903 可 close

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Epic #894 Step 9 (#903) — 最后一个未覆盖的文件：\`AgentDetailClient.tsx\` (608 LOC) 从 0% → 全分支。issue 明说覆盖关键 ~200 行（7 个 modal state + escape handler + lock states）。31 tests, 零源码改动。

## 新增 31 个测试

| 组 | # | 覆盖 |
|---|---|---|
| 初始渲染 | 6 | loading / catalog 成功 / 无匹配 / reject / unmount race / bio 空时 description fallback |
| CTA 按钮 | 5 | 未 hired 只显示 Hire / hired 显示 Chat+Fire / has_update → Update / !has_update 隐藏 / Chat router.push |
| Hire 流 | 5 | confirm modal / isLocked 禁用 / confirm → hireAgent+success / reject 无 success / "Go to chat" |
| Fire 流 | 4 | confirm modal + FIRE 输入门 / 错文字 disabled / "FIRE" enabled + fireAgent / reject |
| Update 流 | 6 | confirm / updateAgent+removeItem CLAW_IDENTITY_CACHE+updated / reject / skip / Send /new → resetAgent / isResetting 禁用+label |
| Escape | 2 | confirm → Escape 关 / success 优先级 > confirm |
| syncing | 1 | modal + button disabled |
| error banner | 1 | |

## Harness 要点

- **heavy imports stub** (ClawPageHeader / LocaleLink / AnimalAvatar) 成 testid div，专注 AgentDetailClient 状态机
- **"Panda Agent" 双重出现**：breadcrumb + h1，用 unique bio `'I am a panda.'` 做 waitFor anchor
- **`zooSquare.confirmFire` 严格匹配**：4 处元素同 prefix（Title/Desc/Prompt/button），必须用精确 string 避免 regex 误中

## Bug-hunting

无新发现。组件的 cancelled 标志防 setState-on-unmounted，7 modal 的 escape 优先级合理（success > confirm > fireConfirm > fired > updateConfirm > updated，isResetting 守卫 updated）。

## Test plan

- [x] 31/31 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 9 (#903) 清单里其他文件（PublishAgentsClient / SkillsSearchClient / SkillDetailClient / useAgentActions / useCustomAgentPublishes / useUserAgents）已有测试；合入后 #903 可 close

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@chris-srp: /lgtm

---

## refactor(web): extract brand-theme bootstrap to src/app/ — fix W6 (A1-PR5) (#1131)

- **SHA**: [ea59b3ef](https://github.com/SerendipityOneInc/ecap-workspace/commit/ea59b3efe1778004084a8ab41176b84706d61146)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-21T10:27:06Z
- **PR**: [#1131](https://github.com/SerendipityOneInc/ecap-workspace/pull/1131)

### Commit Message

refactor(web): extract brand-theme bootstrap to src/app/ — fix W6 (A1-PR5) (#1131)

## Summary
- Fixes the single W6 violation `src/theme/brand-themes.ts →
src/lib/auth/types` by extracting `getBrandThemeBootstrapScript()` out
of `theme/` into `src/app/_brand-bootstrap.ts`.
- Leaves `STORAGE_KEYS.BRAND_THEME` as **single source of truth** in
`lib/auth/types` — all three callers (bootstrap / provider /
logout-preserve) consume it by that path.
- Baseline shrinks **17 → 16**.

## Why extract instead of inline duplicate

Initial draft inlined `'ecap-brand-theme'` twice (once in `theme/`, once
in `lib/auth/types`) with cross-ref comments. Reviewer flagged the
underlying oddity: why does `brand-themes.ts` know about localStorage at
all?

Answer: it contains `getBrandThemeBootstrapScript()` which generates an
IIFE string for SSR first-paint. That function needs the storage key to
embed in the script. But this function is **App-Router-specific** — it's
only called from `src/app/[locale]/layout.tsx` to emit an inline
`<script>` for first-paint anti-flicker.

So the real fix is to move the App-Router concern out of `theme/`:

| Concern | Home before | Home after |
|---|---|---|
| Brand registry + types + guards | `theme/brand-themes.ts` |
`theme/brand-themes.ts` (unchanged) |
| `BRAND_THEME_ATTRIBUTE` (DOM contract string) |
`theme/brand-themes.ts` | `theme/brand-themes.ts` (unchanged — no
cross-layer dep) |
| `getBrandThemeBootstrapScript` (SSR first-paint logic) |
`theme/brand-themes.ts` | **`src/app/_brand-bootstrap.ts`** (new) |
| `BRAND_THEME_STORAGE_KEY` | `theme/brand-themes.ts` (derived from
STORAGE_KEYS) | **removed** — callers use `STORAGE_KEYS.BRAND_THEME`
directly |

After the move, `theme/brand-themes.ts` has **zero cross-layer imports**
— a true Layer-1 leaf per W6.

## Layer check

- `src/app/_brand-bootstrap.ts` → `src/lib/auth/types` — `app → lib` ✅
- `src/app/_brand-bootstrap.ts` → `src/theme/brand-themes` — `app →
theme` ✅
- `src/components/BrandThemeProvider.tsx` → `src/lib/auth/types` —
`components → lib` ✅
- `src/components/BrandThemeProvider.tsx` → `src/theme/brand-themes` —
`components → theme` ✅
- `src/app/[locale]/layout.tsx` → `src/app/_brand-bootstrap` — `app →
app` ✅

## Changes

| File | Change |
|---|---|
| `src/app/_brand-bootstrap.ts` | **new** — owns
`getBrandThemeBootstrapScript` + imports `STORAGE_KEYS` from lib and
brand data from theme |
| `src/theme/brand-themes.ts` | drop storage-key export + bootstrap fn +
`@/lib/auth/types` import; pure data/types/guards only |
| `src/components/BrandThemeProvider.tsx` | import `STORAGE_KEYS` from
`@/lib/auth/types` instead of `BRAND_THEME_STORAGE_KEY` |
| `src/app/[locale]/layout.tsx` | import `getBrandThemeBootstrapScript`
from new home |
| `tests/unit/theme/brand-themes.unit.spec.ts` | keep only
`isBrandThemeName` coverage |
| `tests/unit/app/_brand-bootstrap.unit.spec.ts` | **new** — covers
bootstrap script shape via static string assertions |
| `tests/unit/components/BrandThemeProvider.unit.spec.tsx` +
`tests/unit/hooks/useBrandVocabulary.unit.spec.tsx` | update imports to
`STORAGE_KEYS.BRAND_THEME` |
| `.dependency-cruiser-known-violations.json` | remove W6 entry (17 →
16) |

9 files changed, +119 / −187 (test file cleanup is the big delta — moved
to two smaller files).

## Note on bootstrap runtime tests

The prior test used `new Function()` to execute the generated script
string against mocked globals. The moved test drops that path and keeps
only static-shape assertions (contains IIFE / contains storage key /
contains all allowed names / etc). Runtime correctness of the script is
covered transitively by e2e (the script actually runs during SSR). If a
targeted runtime test becomes needed, it belongs in a jsdom-with-eval
harness, not unit tests.

## Local verification
- \`pnpm lint:imports\` — exit 0, \`16 known violations ignored\`
- \`pnpm test:unit\` affected files — 31 tests pass
- \`npx tsc --noEmit\` — clean
- \`pnpm lint\` — clean

## Aftermath

With this + A1-PR4 already merged, **W1 and W6 contracts are fully
clean**. Remaining baseline 15 is entirely W2/W3/W4/W5 cluster (the \"UI
layer still touching pages/features\" knot). Each subsequent A1-PR6+
takes a handful.

## Test plan
- [x] tsc + eslint + unit tests pass
- [x] Baseline JSON shrinks correctly (17 → 16)
- [ ] CI confirms web-quality + asset-size + jscpd
- [ ] Reviewer validates \`src/app/_brand-bootstrap.ts\` as the right
home for SSR first-paint logic (vs staying in theme with inline
duplicate)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- Fixes the single W6 violation `src/theme/brand-themes.ts → src/lib/auth/types` by extracting `getBrandThemeBootstrapScript()` out of `theme/` into `src/app/_brand-bootstrap.ts`.
- Leaves `STORAGE_KEYS.BRAND_THEME` as **single source of truth** in `lib/auth/types` — all three callers (bootstrap / provider / logout-preserve) consume it by that path.
- Baseline shrinks **17 → 16**.

## Why extract instead of inline duplicate

Initial draft inlined `'ecap-brand-theme'` twice (once in `theme/`, once in `lib/auth/types`) with cross-ref comments. Reviewer flagged the underlying oddity: why does `brand-themes.ts` know about localStorage at all?

Answer: it contains `getBrandThemeBootstrapScript()` which generates an IIFE string for SSR first-paint. That function needs the storage key to embed in the script. But this function is **App-Router-specific** — it's only called from `src/app/[locale]/layout.tsx` to emit an inline `<script>` for first-paint anti-flicker.

So the real fix is to move the App-Router concern out of `theme/`:

| Concern | Home before | Home after |
|---|---|---|
| Brand registry + types + guards | `theme/brand-themes.ts` | `theme/brand-themes.ts` (unchanged) |
| `BRAND_THEME_ATTRIBUTE` (DOM contract string) | `theme/brand-themes.ts` | `theme/brand-themes.ts` (unchanged — no cross-layer dep) |
| `getBrandThemeBootstrapScript` (SSR first-paint logic) | `theme/brand-themes.ts` | **`src/app/_brand-bootstrap.ts`** (new) |
| `BRAND_THEME_STORAGE_KEY` | `theme/brand-themes.ts` (derived from STORAGE_KEYS) | **removed** — callers use `STORAGE_KEYS.BRAND_THEME` directly |

After the move, `theme/brand-themes.ts` has **zero cross-layer imports** — a true Layer-1 leaf per W6.

## Layer check

- `src/app/_brand-bootstrap.ts` → `src/lib/auth/types` — `app → lib` ✅
- `src/app/_brand-bootstrap.ts` → `src/theme/brand-themes` — `app → theme` ✅
- `src/components/BrandThemeProvider.tsx` → `src/lib/auth/types` — `components → lib` ✅
- `src/components/BrandThemeProvider.tsx` → `src/theme/brand-themes` — `components → theme` ✅
- `src/app/[locale]/layout.tsx` → `src/app/_brand-bootstrap` — `app → app` ✅

## Changes

| File | Change |
|---|---|
| `src/app/_brand-bootstrap.ts` | **new** — owns `getBrandThemeBootstrapScript` + imports `STORAGE_KEYS` from lib and brand data from theme |
| `src/theme/brand-themes.ts` | drop storage-key export + bootstrap fn + `@/lib/auth/types` import; pure data/types/guards only |
| `src/components/BrandThemeProvider.tsx` | import `STORAGE_KEYS` from `@/lib/auth/types` instead of `BRAND_THEME_STORAGE_KEY` |
| `src/app/[locale]/layout.tsx` | import `getBrandThemeBootstrapScript` from new home |
| `tests/unit/theme/brand-themes.unit.spec.ts` | keep only `isBrandThemeName` coverage |
| `tests/unit/app/_brand-bootstrap.unit.spec.ts` | **new** — covers bootstrap script shape via static string assertions |
| `tests/unit/components/BrandThemeProvider.unit.spec.tsx` + `tests/unit/hooks/useBrandVocabulary.unit.spec.tsx` | update imports to `STORAGE_KEYS.BRAND_THEME` |
| `.dependency-cruiser-known-violations.json` | remove W6 entry (17 → 16) |

9 files changed, +119 / −187 (test file cleanup is the big delta — moved to two smaller files).

## Note on bootstrap runtime tests

The prior test used `new Function()` to execute the generated script string against mocked globals. The moved test drops that path and keeps only static-shape assertions (contains IIFE / contains storage key / contains all allowed names / etc). Runtime correctness of the script is covered transitively by e2e (the script actually runs during SSR). If a targeted runtime test becomes needed, it belongs in a jsdom-with-eval harness, not unit tests.

## Local verification
- \`pnpm lint:imports\` — exit 0, \`16 known violations ignored\`
- \`pnpm test:unit\` affected files — 31 tests pass
- \`npx tsc --noEmit\` — clean
- \`pnpm lint\` — clean

## Aftermath

With this + A1-PR4 already merged, **W1 and W6 contracts are fully clean**. Remaining baseline 15 is entirely W2/W3/W4/W5 cluster (the \"UI layer still touching pages/features\" knot). Each subsequent A1-PR6+ takes a handful.

## Test plan
- [x] tsc + eslint + unit tests pass
- [x] Baseline JSON shrinks correctly (17 → 16)
- [ ] CI confirms web-quality + asset-size + jscpd
- [ ] Reviewer validates \`src/app/_brand-bootstrap.ts\` as the right home for SSR first-paint logic (vs staying in theme with inline duplicate)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@chris-srp: /lgtm

---

## fix: agent id of popup (#1143)

- **SHA**: [212f5703](https://github.com/SerendipityOneInc/ecap-workspace/commit/212f5703aad8761fcd8ead4e1a0dcf9703b9c0e3)
- **作者**: nolan-srp
- **时间**: 2026-04-21T10:24:34Z
- **PR**: [#1143](https://github.com/SerendipityOneInc/ecap-workspace/pull/1143)

### Commit Message

fix: agent id of popup (#1143)

---

## test(web): ClawSettingsClient 关键分支覆盖 (#894 Step 5 收尾) (#1142)

- **SHA**: [06325039](https://github.com/SerendipityOneInc/ecap-workspace/commit/06325039918012d44d97f542ab23ab7558661030)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-21T10:13:10Z
- **PR**: [#1142](https://github.com/SerendipityOneInc/ecap-workspace/pull/1142)

### Commit Message

test(web): ClawSettingsClient 关键分支覆盖 (#894 Step 5 收尾) (#1142)

## Summary

Epic #894 Step 5 (#899) 的最后一个文件：\`ClawSettingsClient.tsx\` (438 LOC)。按
issue 描述只覆盖关键 ~120 行（auth gates + tab routing + noBot 分支 + status tab
internal-only visibility），27 个测试。

## 源码变动（1 行）

- \`BotStatusBanner\` 加 \`export\`

## 新增 27 个测试

| 组 | # | 覆盖 |
|---|---|---|
| BotStatusBanner | 5 | ready/no_bot 返 null / creating/starting 各自 label
/ i18n 兜底到英文 default |
| Auth 状态机 | 6 | authLoading → dot-spin / !chatReady → null /
!isLoggedIn → login prompt / 无 uid → login prompt / login 按钮 →
showLoginModal / 全过 → SettingsLayout |
| Tab routing | 9 | 默认 account / 非法 paramTab fallback /
channels/account-usage/account-billing/connectors/sessions/statistics
对应组件 / 点击 tab → router.replace('?tab=X') |
| noBot 分支 | 3 | 非 account tab + 无 settings / bot_status='no_bot' /
account tab bypass |
| Status tab internal-only | 2 | canViewInternalOnlyFeatures false/true
→ ImageVersionSection 可见性 |
| error + loading | 2 | error banner / 内层 dot-spin |

## Harness 要点

所有 heavy 子组件（GeneralTab / UsageTabContent / BillingTabContent /
ChannelsSection / ConnectorsSection / DiagnosticsSection /
ImageVersionSection / SessionResetSection / UsageCard /
WorkspaceFilesSection）stub 成 testid 占位，让测试只盯 ClawSettingsClient 自己的
routing / auth 逻辑。SettingsLayout stub 暴露 `tab-{id}` testid 让点击 tab 可驱动
onTabChange。

## 不覆盖范围

- `StatusTab` 内部组件（logs modal 弹框逻辑）— 复杂但非 issue 重点，未来如需再补
- Resources 30s 自动 poll — 需要 fake timer + waitFor 混合，收益低
- versionCheck.needsUpgrade → UpgradeNotificationBanner — 纯透传 props

## Test plan

- [x] 27/27 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899) — 所有清单文件已覆盖，#899 可 close

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Epic #894 Step 5 (#899) 的最后一个文件：\`ClawSettingsClient.tsx\` (438 LOC)。按 issue 描述只覆盖关键 ~120 行（auth gates + tab routing + noBot 分支 + status tab internal-only visibility），27 个测试。

## 源码变动（1 行）

- \`BotStatusBanner\` 加 \`export\`

## 新增 27 个测试

| 组 | # | 覆盖 |
|---|---|---|
| BotStatusBanner | 5 | ready/no_bot 返 null / creating/starting 各自 label / i18n 兜底到英文 default |
| Auth 状态机 | 6 | authLoading → dot-spin / !chatReady → null / !isLoggedIn → login prompt / 无 uid → login prompt / login 按钮 → showLoginModal / 全过 → SettingsLayout |
| Tab routing | 9 | 默认 account / 非法 paramTab fallback / channels/account-usage/account-billing/connectors/sessions/statistics 对应组件 / 点击 tab → router.replace('?tab=X') |
| noBot 分支 | 3 | 非 account tab + 无 settings / bot_status='no_bot' / account tab bypass |
| Status tab internal-only | 2 | canViewInternalOnlyFeatures false/true → ImageVersionSection 可见性 |
| error + loading | 2 | error banner / 内层 dot-spin |

## Harness 要点

所有 heavy 子组件（GeneralTab / UsageTabContent / BillingTabContent / ChannelsSection / ConnectorsSection / DiagnosticsSection / ImageVersionSection / SessionResetSection / UsageCard / WorkspaceFilesSection）stub 成 testid 占位，让测试只盯 ClawSettingsClient 自己的 routing / auth 逻辑。SettingsLayout stub 暴露 `tab-{id}` testid 让点击 tab 可驱动 onTabChange。

## 不覆盖范围

- `StatusTab` 内部组件（logs modal 弹框逻辑）— 复杂但非 issue 重点，未来如需再补
- Resources 30s 自动 poll — 需要 fake timer + waitFor 混合，收益低
- versionCheck.needsUpgrade → UpgradeNotificationBanner — 纯透传 props

## Test plan

- [x] 27/27 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899) — 所有清单文件已覆盖，#899 可 close

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@chris-srp: /lgtm

---

## test(web): ConnectorsSection 全面覆盖 (#894 Step 5 补) (#1130)

- **SHA**: [b7b78b08](https://github.com/SerendipityOneInc/ecap-workspace/commit/b7b78b0893baa8b7bf9f90ff4ee4af7284a6d554)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-21T09:52:40Z
- **PR**: [#1130](https://github.com/SerendipityOneInc/ecap-workspace/pull/1130)

### Commit Message

test(web): ConnectorsSection 全面覆盖 (#894 Step 5 补) (#1130)

## Summary

Epic #894 Step 5 (#899) — 再补一个：\`ConnectorsSection.tsx\` (493 LOC) 从 0%
→ 全分支，28 tests。源码零改动（Google Workspace connector + Nango integrations +
ModeDropdown 的所有导出都已经是 named exports），test-only PR。

## 新增 28 个测试

| 分组 | # | 覆盖 |
|---|---|---|
| loading state | 2 | 初始 / resolve 后消失 |
| Google 卡状态机 | 3 | 无 token / token+!alive (Reconnect) / token+alive
(Disconnect) |
| API error | 2 | Error 实例 / 非-Error fallback "Failed to load status" |
| handleConnect | 3 | 成功 → window.location.href 赋值 / 失败 → error + 按钮恢复 /
readonly→false 传给 getConnectorAuthUrl |
| handleDisconnect | 2 | 成功 → refetch / 失败 → error |
| handleReconnect | 2 | 成功 → injectConnector + refetch / 失败 |
| ModeDropdown | 3 | 展开 / 点外关 / 选项切换 |
| Nango cards | 7 | connected/pending/error/unknown 4 种 status /
disconnect 回调 / toggle enable vs disable / saving → disabled |
| Available integrations | 3 | 有未连接则渲染 section / Connect click → connect
+ window.open + pollUntilConnected / null URL 不 open / 全连接则隐藏 section |

## Harness 要点

- **window.location 代理**：jsdom 的 location 是只读的，source 里
\`window.location.href = url\` 会抛。用 Proxy 装 href setter 记录赋值，测试直接检查
hrefWrites 数组
- **integrations factory**：返回可 mock 的
connect/disconnect/enable/disable/pollUntilConnected，不同测试换不同 connections
数组
- **\`settings.connect\` 多处出现**：Google card + 每个 Available card 都有同名按钮，用
\`findAllByText + [0]\` 定位 Google（DOM 顺序稳定）

## Bug-hunting

无新发现。Google connector state machine 干净，error recovery 路径到位。

## Test plan

- [x] 28/28 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899)
- Step 5 剩下：ClawSettingsClient (438 LOC, 关键 ~120)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Epic #894 Step 5 (#899) — 再补一个：\`ConnectorsSection.tsx\` (493 LOC) 从 0% → 全分支，28 tests。源码零改动（Google Workspace connector + Nango integrations + ModeDropdown 的所有导出都已经是 named exports），test-only PR。

## 新增 28 个测试

| 分组 | # | 覆盖 |
|---|---|---|
| loading state | 2 | 初始 / resolve 后消失 |
| Google 卡状态机 | 3 | 无 token / token+!alive (Reconnect) / token+alive (Disconnect) |
| API error | 2 | Error 实例 / 非-Error fallback "Failed to load status" |
| handleConnect | 3 | 成功 → window.location.href 赋值 / 失败 → error + 按钮恢复 / readonly→false 传给 getConnectorAuthUrl |
| handleDisconnect | 2 | 成功 → refetch / 失败 → error |
| handleReconnect | 2 | 成功 → injectConnector + refetch / 失败 |
| ModeDropdown | 3 | 展开 / 点外关 / 选项切换 |
| Nango cards | 7 | connected/pending/error/unknown 4 种 status / disconnect 回调 / toggle enable vs disable / saving → disabled |
| Available integrations | 3 | 有未连接则渲染 section / Connect click → connect + window.open + pollUntilConnected / null URL 不 open / 全连接则隐藏 section |

## Harness 要点

- **window.location 代理**：jsdom 的 location 是只读的，source 里 \`window.location.href = url\` 会抛。用 Proxy 装 href setter 记录赋值，测试直接检查 hrefWrites 数组
- **integrations factory**：返回可 mock 的 connect/disconnect/enable/disable/pollUntilConnected，不同测试换不同 connections 数组
- **\`settings.connect\` 多处出现**：Google card + 每个 Available card 都有同名按钮，用 \`findAllByText + [0]\` 定位 Google（DOM 顺序稳定）

## Bug-hunting

无新发现。Google connector state machine 干净，error recovery 路径到位。

## Test plan

- [x] 28/28 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899)
- Step 5 剩下：ClawSettingsClient (438 LOC, 关键 ~120)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@chris-srp: /lgtm

---

## fix: clean up stale domain refs and remove dead env vars (#1140)

- **SHA**: [28ef8cd1](https://github.com/SerendipityOneInc/ecap-workspace/commit/28ef8cd1d299f6a09e9042b0d598ee3105283bca)
- **作者**: peter-srp
- **时间**: 2026-04-21T08:28:09Z
- **PR**: [#1140](https://github.com/SerendipityOneInc/ecap-workspace/pull/1140)

### Commit Message

fix: clean up stale domain refs and remove dead env vars (#1140)

## Summary
- **`www.zooclaw.ai` → `zooclaw.ai`**: E2E/CI 配置中错误使用了不支持的 www
子域名（playwright.config、e2e.yml、auth setup 等 6 处）
- **`pandaclaw.ai` → `zooclaw.ai`**: 设计稿 mockup 中的旧域名邮箱替换（4 处
docs/design HTML）
- **移除 `NEXT_PUBLIC_APP_URL`**: 前端代码已不引用，但 deploy.yml 的 validation
仍在检查导致部署失败（`Missing required variables/secrets: NEXT_PUBLIC_APP_URL`）
- **移除 `NEXT_PUBLIC_GEM_WORKFLOW_URL`、`NEXT_PUBLIC_BACKEND_URL`**:
web/src/ 中 0 引用的死变量，从 deploy pipeline 和 .env.example 中清除

## Test plan
- [ ] Deploy pipeline 不再因 `NEXT_PUBLIC_APP_URL` 缺失而报错
- [ ] E2E tests 正确指向 `https://zooclaw.ai`（非 www）
- [ ] Staging / production deploy 正常完成

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- **`www.zooclaw.ai` → `zooclaw.ai`**: E2E/CI 配置中错误使用了不支持的 www 子域名（playwright.config、e2e.yml、auth setup 等 6 处）
- **`pandaclaw.ai` → `zooclaw.ai`**: 设计稿 mockup 中的旧域名邮箱替换（4 处 docs/design HTML）
- **移除 `NEXT_PUBLIC_APP_URL`**: 前端代码已不引用，但 deploy.yml 的 validation 仍在检查导致部署失败（`Missing required variables/secrets: NEXT_PUBLIC_APP_URL`）
- **移除 `NEXT_PUBLIC_GEM_WORKFLOW_URL`、`NEXT_PUBLIC_BACKEND_URL`**: web/src/ 中 0 引用的死变量，从 deploy pipeline 和 .env.example 中清除

## Test plan
- [ ] Deploy pipeline 不再因 `NEXT_PUBLIC_APP_URL` 缺失而报错
- [ ] E2E tests 正确指向 `https://zooclaw.ai`（非 www）
- [ ] Staging / production deploy 正常完成

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@peter-srp: /lgtm

---

## fix(claw-interface): backfill agent workspaces in /openclaw/agents (#1138)

- **SHA**: [11cb1f46](https://github.com/SerendipityOneInc/ecap-workspace/commit/11cb1f46868a3c8cce2d054c0ef0096acace925d)
- **作者**: nolan-srp
- **时间**: 2026-04-21T07:46:53Z
- **PR**: [#1138](https://github.com/SerendipityOneInc/ecap-workspace/pull/1138)

### Commit Message

fix(claw-interface): backfill agent workspaces in /openclaw/agents (#1138)

## Summary
- backfill agent workspace paths in \/openclaw\/agents from the live bot
config when available
- keep the endpoint resilient by falling back to null workspaces if live
config lookup fails
- add unit coverage for workspace mapping extraction, response
hydration, and route fallback behavior

### PR Description

## Summary
- backfill agent workspace paths in \/openclaw\/agents from the live bot config when available
- keep the endpoint resilient by falling back to null workspaces if live config lookup fails
- add unit coverage for workspace mapping extraction, response hydration, and route fallback behavior

---

## fix(claw-interface): suppress LiteLLM INFO logs polluting GCP ERROR stream (#1139)

- **SHA**: [89402eb1](https://github.com/SerendipityOneInc/ecap-workspace/commit/89402eb14a7fce68fe00ef8ec92cf5e792606631)
- **作者**: peter-srp
- **时间**: 2026-04-21T07:45:48Z
- **PR**: [#1139](https://github.com/SerendipityOneInc/ecap-workspace/pull/1139)

### Commit Message

fix(claw-interface): suppress LiteLLM INFO logs polluting GCP ERROR stream (#1139)

## Summary
- LiteLLM v1.82.3 attaches its own `StreamHandler(stderr)` at import
time. In GCP containers, stderr is captured as ERROR severity — so
~100+/day INFO-level `completion()` messages were inflating error counts
and adding noise to monitoring.
- Added `_suppress_noisy_loggers()` in `app_logging.py` that raises
LiteLLM (and related `httpx`/`openai`) loggers to WARNING level and
strips their stderr handlers.
- 3 new unit tests covering level suppression, handler stripping, and
integration with `configure_logging()`.

## Test plan
- [ ] CI passes (`python-code-quality / build-and-test`)
- [ ] Deploy to staging and verify GCP Logs no longer show
`LiteLLM:INFO` entries in ERROR stream
- [ ] Confirm real LiteLLM warnings/errors (e.g. model failures, rate
limits) still appear

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- LiteLLM v1.82.3 attaches its own `StreamHandler(stderr)` at import time. In GCP containers, stderr is captured as ERROR severity — so ~100+/day INFO-level `completion()` messages were inflating error counts and adding noise to monitoring.
- Added `_suppress_noisy_loggers()` in `app_logging.py` that raises LiteLLM (and related `httpx`/`openai`) loggers to WARNING level and strips their stderr handlers.
- 3 new unit tests covering level suppression, handler stripping, and integration with `configure_logging()`.

## Test plan
- [ ] CI passes (`python-code-quality / build-and-test`)
- [ ] Deploy to staging and verify GCP Logs no longer show `LiteLLM:INFO` entries in ERROR stream
- [ ] Confirm real LiteLLM warnings/errors (e.g. model failures, rate limits) still appear

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@peter-srp: /lgtm
@peter-srp: <img width="2020" height="512" alt="image" src="https://github.com/user-attachments/assets/803ea430-4698-49bb-833b-80cacfcfb69e" />


---

## fix: replace hardcoded domain URLs with relative paths and env vars (#1137)

- **SHA**: [50c709aa](https://github.com/SerendipityOneInc/ecap-workspace/commit/50c709aa29333370386ec264c71450fa54fe9374)
- **作者**: peter-srp
- **时间**: 2026-04-21T06:56:43Z
- **PR**: [#1137](https://github.com/SerendipityOneInc/ecap-workspace/pull/1137)

### Commit Message

fix: replace hardcoded domain URLs with relative paths and env vars (#1137)

## Summary

- **Backend `_admin.py`**: stale `ecap.gensmo.com` fallback →
`zooclaw.ai`
- **Frontend links** (public-nav-data, LoginForm, UserMenu,
PublicFooter, userguide-html, user-guide.html): absolute
`https://zooclaw.ai/*` → relative paths (`/tips`, `/about/terms`, etc.)
- **`sms-terms` page**: hardcoded display URL → `seoConfig.siteUrl` from
`_seo.ts`
- **`middleware.ts`**: `CANONICAL_ORIGIN` reads `NEXT_PUBLIC_SITE_URL`
env var with legacy-domain guard
- **`_seo.ts`**: `getCanonicalSiteUrl` now recognizes legacy host
markers (`gensmo.com`, `gsmo.ai`, `ecap.`) and normalizes to
`zooclaw.ai` — prevents misconfigured
`NEXT_PUBLIC_SITE_URL=https://ecap.gsmo.ai` from polluting canonical
URLs, hreflang, and OG meta

### Action required after merge
Update GitHub repo variable: `NEXT_PUBLIC_SITE_URL` →
`https://zooclaw.ai` (currently set to stale `https://ecap.gsmo.ai`)

### Not changed (with rationale)
| File | Reason |
|------|--------|
| `_seo.ts` `PRODUCTION_SITE_URL` | Single source of truth for
canonical/hreflang/OG — all other code references this |
| `sitemap*.xml` | XML sitemap spec requires absolute `<loc>` URLs;
static files can't import constants |
| `wrangler.toml` `FRONTEND_URL` | Deployment config; CI overrides
per-environment via `--var` |
| iOS `AppEnvironment.swift` | Native app, separate build — already uses
correct domain |
| `robots.ts` / `middleware.ts` `LEGACY_HOSTS` | Intentional old-domain
list for 301 redirects and crawler blocking |
| `docs/plans/*.md` | Historical design documents |

## Test plan

- [ ] CI lint + type check pass
- [ ] Manual: verify footer/nav links work (relative paths resolve
correctly)
- [ ] Manual: LoginForm terms/privacy links open in new tab
- [ ] Manual: user guide CTA button works
- [ ] SEO: canonical URLs, hreflang, and sitemaps unchanged — verify
with `curl -s https://zooclaw.ai/en/pricing | grep canonical`
- [ ] After deploy: update `NEXT_PUBLIC_SITE_URL` repo var to
`https://zooclaw.ai`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

- **Backend `_admin.py`**: stale `ecap.gensmo.com` fallback → `zooclaw.ai`
- **Frontend links** (public-nav-data, LoginForm, UserMenu, PublicFooter, userguide-html, user-guide.html): absolute `https://zooclaw.ai/*` → relative paths (`/tips`, `/about/terms`, etc.)
- **`sms-terms` page**: hardcoded display URL → `seoConfig.siteUrl` from `_seo.ts`
- **`middleware.ts`**: `CANONICAL_ORIGIN` reads `NEXT_PUBLIC_SITE_URL` env var with legacy-domain guard
- **`_seo.ts`**: `getCanonicalSiteUrl` now recognizes legacy host markers (`gensmo.com`, `gsmo.ai`, `ecap.`) and normalizes to `zooclaw.ai` — prevents misconfigured `NEXT_PUBLIC_SITE_URL=https://ecap.gsmo.ai` from polluting canonical URLs, hreflang, and OG meta

### Action required after merge
Update GitHub repo variable: `NEXT_PUBLIC_SITE_URL` → `https://zooclaw.ai` (currently set to stale `https://ecap.gsmo.ai`)

### Not changed (with rationale)
| File | Reason |
|------|--------|
| `_seo.ts` `PRODUCTION_SITE_URL` | Single source of truth for canonical/hreflang/OG — all other code references this |
| `sitemap*.xml` | XML sitemap spec requires absolute `<loc>` URLs; static files can't import constants |
| `wrangler.toml` `FRONTEND_URL` | Deployment config; CI overrides per-environment via `--var` |
| iOS `AppEnvironment.swift` | Native app, separate build — already uses correct domain |
| `robots.ts` / `middleware.ts` `LEGACY_HOSTS` | Intentional old-domain list for 301 redirects and crawler blocking |
| `docs/plans/*.md` | Historical design documents |

## Test plan

- [ ] CI lint + type check pass
- [ ] Manual: verify footer/nav links work (relative paths resolve correctly)
- [ ] Manual: LoginForm terms/privacy links open in new tab
- [ ] Manual: user guide CTA button works
- [ ] SEO: canonical URLs, hreflang, and sitemaps unchanged — verify with `curl -s https://zooclaw.ai/en/pricing | grep canonical`
- [ ] After deploy: update `NEXT_PUBLIC_SITE_URL` repo var to `https://zooclaw.ai`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@peter-srp: /lgtm

---

## feat(chat): 深链未雇佣/未知 agent 跳转 Agent Studio hire 面板 (#1020)

- **SHA**: [4b1ac4a4](https://github.com/SerendipityOneInc/ecap-workspace/commit/4b1ac4a4900f60a383d74a7817222098e5b1f0b2)
- **作者**: vincent-srp
- **时间**: 2026-04-21T06:53:43Z
- **PR**: [#1020](https://github.com/SerendipityOneInc/ecap-workspace/pull/1020)

### Commit Message

feat(chat): 深链未雇佣/未知 agent 跳转 Agent Studio hire 面板 (#1020)

## Summary

`/chat?agent_id=<slug>` 深链兜底改造，把原本「静默回退到 main agent」的断头路改成两条有意义的引导路径。

- 目标 slug **在 official catalog 但未雇佣** → toast「You need to hire {name}
first」+ `router.replace('/agents-manager/{slug}')`
- 目标 slug **不在 catalog（无效 / 拼错 / 已下线）** → toast「Try Agent Studio to
build a custom one」+ `router.replace('/agents-manager/agent_studio')`
- 已雇佣 → 沿用现有直进逻辑
- 排队在 Onboarding + 「Reaching your Claw…」init 完成之后才触发（`canUseChat &&
isChatReady` 各自 latch + 1.5s buffer）。**不** gate 在 GuideTour 上 — 从未关过
tour 的回访用户否则会被卡死

## 设计约定

- **永不替用户自动雇佣**：hook 不导入 `installOpenClawAgent`（结构性约束），雇佣是目的页职责
- **Toast 用全局 ToastProvider**（z-9999，跨页面持久），跳转后还能在目的页继续展示 ~2.4s
- **空 catalog 不误判为 slug 缺失**：catalog fetch 失败时 hold 在 `loading_meta`，不跳
Agent Studio；catalog populate 后自动恢复；8s 超时后 toast「catalog unavailable」并清掉
`agent_id`
- **`hiredIds` + `userAgentsLoading` 双重防御**：避免冷缓存 + 慢网下，已雇佣 agent 因
hydration 没赶上 1.5s buffer 被误判为未雇佣
- **`canUseChat` / `isChatReady` 用 latched ever-true**：post-login
时这俩信号会震荡（onboarding resolver / bot init 多阶段），latch 后取「曾经为 true」满足
buffer，避开「同时为 true」永不到达的窗口

## 顺带修复（同样影响 unauth /chat 体验）

- **OnboardingModal 在 `!authLoading && !isLoggedIn` 时直接 return null**：避开
AnimatePresence 600ms 淡出窗口，不再吞掉 LandingScreen 按钮的点击
- **LoginCheckProvider pathname effect 改成 two-real-values 状态机**：Next.js
15 `usePathname()` 类型签名 `string | null`，hydration 期可能短暂返回 null；旧逻辑把
`null → 实值`误判为导航，关掉刚被 LandingScreen 打开的登录面板

## Changes

- 新增 `useDeepLinkHireFlow` hook + 24 单测
- 新增 `AGENT_STUDIO_SLUG` 常量（`web/src/lib/agentSlugs.ts`）
- `GuideTourModal`：抽 `GUIDE_TOUR_DISMISSED_EVENT` 常量 +
`markGuideTourSeen()` helper（idempotent）
- `LandingScreen` mount 时自动 open LoginModal（带 StrictMode guard）
- 4 个 i18n keys（en + zh）：`chatDeepLink.notHired.toast` /
`chatDeepLink.notFound.toStudio` / `chatDeepLink.catalogUnavailable`
- `OnboardingModal` + `LoginCheckProvider` 两处 unauth /chat 修复（见上）
- 同步更新 `useSessionLogs` 单测断言（删了 chat 页不消费的 `&session_id=` 参数）

## Test plan

- [x] `useDeepLinkHireFlow.unit.spec.ts` 24 tests 全过
- [x] `LoginCheckProvider.unit.spec.tsx` 12 tests 全过（含
null→real-pathname 回归）
- [x] `pnpm lint` + `pnpm tsc --noEmit` 干净
- [x] 全量 `pnpm vitest run` 2848 tests 全过
- [ ] 手测：已雇佣 agent 深链直进
- [ ] 手测：未雇佣官方 agent 深链 → toast + 跳 `/agents-manager/{id}`
- [ ] 手测：不存在 slug → toast + 跳 `/agents-manager/agent_studio`
- [ ] 手测：未登录深链 → 自动唤起登录面板（不闪、按钮可点击）+ 登录后 query 保留 + 触发深链
- [ ] 手测：catalog 离线 → 8s 后 toast + 清 `agent_id` 落到主 chat

## Known follow-ups (out of scope for this PR)

- `canUseChatEver` / `isChatReadyEver` 在 `agentId` 切换时不重置 — 同会话内换
deep-link 且 bot 恰好在 reconnect 的窄场景，redirect 可能在浮层未消失时 fire。修法是 3
行（`agentId` 变化时 snapshot 当前值），但 scope 蔓延，留作后续

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>

### PR Description

## Summary

`/chat?agent_id=<slug>` 深链兜底改造，把原本「静默回退到 main agent」的断头路改成两条有意义的引导路径。

- 目标 slug **在 official catalog 但未雇佣** → toast「You need to hire {name} first」+ `router.replace('/agents-manager/{slug}')`
- 目标 slug **不在 catalog（无效 / 拼错 / 已下线）** → toast「Try Agent Studio to build a custom one」+ `router.replace('/agents-manager/agent_studio')`
- 已雇佣 → 沿用现有直进逻辑
- 排队在 Onboarding + 「Reaching your Claw…」init 完成之后才触发（`canUseChat && isChatReady` 各自 latch + 1.5s buffer）。**不** gate 在 GuideTour 上 — 从未关过 tour 的回访用户否则会被卡死

## 设计约定

- **永不替用户自动雇佣**：hook 不导入 `installOpenClawAgent`（结构性约束），雇佣是目的页职责
- **Toast 用全局 ToastProvider**（z-9999，跨页面持久），跳转后还能在目的页继续展示 ~2.4s
- **空 catalog 不误判为 slug 缺失**：catalog fetch 失败时 hold 在 `loading_meta`，不跳 Agent Studio；catalog populate 后自动恢复；8s 超时后 toast「catalog unavailable」并清掉 `agent_id`
- **`hiredIds` + `userAgentsLoading` 双重防御**：避免冷缓存 + 慢网下，已雇佣 agent 因 hydration 没赶上 1.5s buffer 被误判为未雇佣
- **`canUseChat` / `isChatReady` 用 latched ever-true**：post-login 时这俩信号会震荡（onboarding resolver / bot init 多阶段），latch 后取「曾经为 true」满足 buffer，避开「同时为 true」永不到达的窗口

## 顺带修复（同样影响 unauth /chat 体验）

- **OnboardingModal 在 `!authLoading && !isLoggedIn` 时直接 return null**：避开 AnimatePresence 600ms 淡出窗口，不再吞掉 LandingScreen 按钮的点击
- **LoginCheckProvider pathname effect 改成 two-real-values 状态机**：Next.js 15 `usePathname()` 类型签名 `string | null`，hydration 期可能短暂返回 null；旧逻辑把 `null → 实值`误判为导航，关掉刚被 LandingScreen 打开的登录面板

## Changes

- 新增 `useDeepLinkHireFlow` hook + 24 单测
- 新增 `AGENT_STUDIO_SLUG` 常量（`web/src/lib/agentSlugs.ts`）
- `GuideTourModal`：抽 `GUIDE_TOUR_DISMISSED_EVENT` 常量 + `markGuideTourSeen()` helper（idempotent）
- `LandingScreen` mount 时自动 open LoginModal（带 StrictMode guard）
- 4 个 i18n keys（en + zh）：`chatDeepLink.notHired.toast` / `chatDeepLink.notFound.toStudio` / `chatDeepLink.catalogUnavailable`
- `OnboardingModal` + `LoginCheckProvider` 两处 unauth /chat 修复（见上）
- 同步更新 `useSessionLogs` 单测断言（删了 chat 页不消费的 `&session_id=` 参数）

## Test plan

- [x] `useDeepLinkHireFlow.unit.spec.ts` 24 tests 全过
- [x] `LoginCheckProvider.unit.spec.tsx` 12 tests 全过（含 null→real-pathname 回归）
- [x] `pnpm lint` + `pnpm tsc --noEmit` 干净
- [x] 全量 `pnpm vitest run` 2848 tests 全过
- [ ] 手测：已雇佣 agent 深链直进
- [ ] 手测：未雇佣官方 agent 深链 → toast + 跳 `/agents-manager/{id}`
- [ ] 手测：不存在 slug → toast + 跳 `/agents-manager/agent_studio`
- [ ] 手测：未登录深链 → 自动唤起登录面板（不闪、按钮可点击）+ 登录后 query 保留 + 触发深链
- [ ] 手测：catalog 离线 → 8s 后 toast + 清 `agent_id` 落到主 chat

## Known follow-ups (out of scope for this PR)

- `canUseChatEver` / `isChatReadyEver` 在 `agentId` 切换时不重置 — 同会话内换 deep-link 且 bot 恰好在 reconnect 的窄场景，redirect 可能在浮层未消失时 fire。修法是 3 行（`agentId` 变化时 snapshot 当前值），但 scope 蔓延，留作后续

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(web): Seedance 2.0 上新弹窗 — 点击 Try now 跳转 agent 详情页走 hire 确认流程 (#981)

- **SHA**: [a2566491](https://github.com/SerendipityOneInc/ecap-workspace/commit/a2566491b5252eb429232d480283b0b35ea93e59)
- **作者**: lynn Zhuang
- **时间**: 2026-04-21T06:21:37Z
- **PR**: [#981](https://github.com/SerendipityOneInc/ecap-workspace/pull/981)

### Commit Message

feat(web): Seedance 2.0 上新弹窗 — 点击 Try now 跳转 agent 详情页走 hire 确认流程 (#981)

## 概要
  重新引入 Seedance 2.0 上新弹窗（此前 #866 被 revert #918）。

  **关键变更**：点击「立即体验」不再直接调用 hire API，而是跳转到 Vibe Drama
  的 agent 详情页（`/agents-manager/vibe_drama`），用户需手动点击 Confirm
  完成雇佣。

  ## 功能说明
  - 16:9 宣传视频自动播放循环（静音）
  - 每用户仅展示一次（localStorage 标记）
  - 与 Guide Tour 弹窗互斥：Guide Tour 未看过时不弹出，等下次登录
  - 弹窗延迟 5 秒出现，等 chat 页面渲染完成后再展示

  ## 改动文件
  | 文件 | 说明 |
  |------|------|
  | `web/src/components/SeedanceLaunchModal.tsx` | 新增弹窗组件 |
  | `web/src/app/[locale]/chat/GenClawClient.tsx` | 在 chat 页面挂载弹窗 |
  | `web/src/lib/auth/types.ts` | 新增 `SEEDANCE_LAUNCH_SEEN` 存储键 |
  | `web/src/locales/en.ts` | 英文文案 |
  | `web/src/locales/zh.ts` | 中文文案 |

  ## 与 #866 的区别
  | | #866（已 revert） | 本 PR |
  |---|---|---|
  | Try now 行为 | 直接调用 `installOpenClawAgent` API | 跳转到 agent 详情页 |
  | 雇佣确认 | 无需确认，自动雇佣 | 用户手动点击 Confirm 确认 |
  | 跳转方式 | `router.push` → chat 页面 | `window.location.href` → agent
  详情页 |

  ## 测试计划
  - [ ] 登录 → 进入 chat → 5 秒后弹窗出现（前提：Guide Tour 已看过）
  - [ ] 关闭弹窗 → 刷新 → 不再出现
  - [ ] 点击「立即体验」→ 跳转到 Vibe Drama 详情页
  - [ ] 在详情页点击 Hire → Confirm → 雇佣成功
  - [ ] 新用户未看过 Guide Tour → 弹窗不出现
  - [ ] 官网首页不弹出
<img width="2544" height="1504" alt="20260417
<img width="2564" height="1690" alt="20260417-123733"
src="https://github.com/user-attachments/assets/3841348a-e307-41e9-9f44-5a3dbe3a4265"
/>
-123731"
src="https://github.com/user-attachments/assets/71cf6cb8-d28d-485c-bb7a-a8c709cf6dfa"
/>

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@LynndeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>

### PR Description

## 概要
  重新引入 Seedance 2.0 上新弹窗（此前 #866 被 revert #918）。

  **关键变更**：点击「立即体验」不再直接调用 hire API，而是跳转到 Vibe Drama
  的 agent 详情页（`/agents-manager/vibe_drama`），用户需手动点击 Confirm
  完成雇佣。

  ## 功能说明
  - 16:9 宣传视频自动播放循环（静音）
  - 每用户仅展示一次（localStorage 标记）
  - 与 Guide Tour 弹窗互斥：Guide Tour 未看过时不弹出，等下次登录
  - 弹窗延迟 5 秒出现，等 chat 页面渲染完成后再展示

  ## 改动文件
  | 文件 | 说明 |
  |------|------|
  | `web/src/components/SeedanceLaunchModal.tsx` | 新增弹窗组件 |
  | `web/src/app/[locale]/chat/GenClawClient.tsx` | 在 chat 页面挂载弹窗 |
  | `web/src/lib/auth/types.ts` | 新增 `SEEDANCE_LAUNCH_SEEN` 存储键 |
  | `web/src/locales/en.ts` | 英文文案 |
  | `web/src/locales/zh.ts` | 中文文案 |

  ## 与 #866 的区别
  | | #866（已 revert） | 本 PR |
  |---|---|---|
  | Try now 行为 | 直接调用 `installOpenClawAgent` API | 跳转到 agent 详情页 |
  | 雇佣确认 | 无需确认，自动雇佣 | 用户手动点击 Confirm 确认 |
  | 跳转方式 | `router.push` → chat 页面 | `window.location.href` → agent
  详情页 |

  ## 测试计划
  - [ ] 登录 → 进入 chat → 5 秒后弹窗出现（前提：Guide Tour 已看过）
  - [ ] 关闭弹窗 → 刷新 → 不再出现
  - [ ] 点击「立即体验」→ 跳转到 Vibe Drama 详情页
  - [ ] 在详情页点击 Hire → Confirm → 雇佣成功
  - [ ] 新用户未看过 Guide Tour → 弹窗不出现
  - [ ] 官网首页不弹出
<img width="2544" height="1504" alt="20260417
<img width="2564" height="1690" alt="20260417-123733" src="https://github.com/user-attachments/assets/3841348a-e307-41e9-9f44-5a3dbe3a4265" />
-123731" src="https://github.com/user-attachments/assets/71cf6cb8-d28d-485c-bb7a-a8c709cf6dfa" />


---

## fix: migrate E2E base URL to www.zooclaw.ai (#1028)

- **SHA**: [e248f7ff](https://github.com/SerendipityOneInc/ecap-workspace/commit/e248f7ffbf373867e9b254661de3acff1169c9ff)
- **作者**: tim-srp
- **时间**: 2026-04-21T05:26:00Z
- **PR**: [#1028](https://github.com/SerendipityOneInc/ecap-workspace/pull/1028)

### Commit Message

fix: migrate E2E base URL to www.zooclaw.ai (#1028)

## Summary
- Update default E2E base URL from `ecap.gensmo.com` to `www.zooclaw.ai`
across all test configs and CI
- Update backend `openclaw_client.py` fallback URL
- Legacy redirect logic in `middleware.ts` and `robots.ts` intentionally
preserved

## Changed files
- `web/playwright.config.ts` — default baseURL
- `web/tests/e2e/auth/auth.setup.ts` — fallback URL + comment
- `web/tests/e2e/auth/capture-tokens.ts` — production URL
- `web/tests/e2e/specs/api-auth-uid-validation.spec.ts` — fallback URL
- `.github/workflows/e2e.yml` — workflow dispatch options + schedule
default
- `services/claw-interface/app/services/openclaw_client.py` — app
creation fallback URL

## Test plan
- [ ] Verify E2E tests can reach `https://www.zooclaw.ai` via auth setup
- [ ] Verify CI workflow dispatch shows new URL options

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- Update default E2E base URL from `ecap.gensmo.com` to `www.zooclaw.ai` across all test configs and CI
- Update backend `openclaw_client.py` fallback URL
- Legacy redirect logic in `middleware.ts` and `robots.ts` intentionally preserved

## Changed files
- `web/playwright.config.ts` — default baseURL
- `web/tests/e2e/auth/auth.setup.ts` — fallback URL + comment
- `web/tests/e2e/auth/capture-tokens.ts` — production URL
- `web/tests/e2e/specs/api-auth-uid-validation.spec.ts` — fallback URL
- `.github/workflows/e2e.yml` — workflow dispatch options + schedule default
- `services/claw-interface/app/services/openclaw_client.py` — app creation fallback URL

## Test plan
- [ ] Verify E2E tests can reach `https://www.zooclaw.ai` via auth setup
- [ ] Verify CI workflow dispatch shows new URL options

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(web): sticky sidebar bottom nav with scrollable agent list (ECA-520) (#1132)

- **SHA**: [a7c3d696](https://github.com/SerendipityOneInc/ecap-workspace/commit/a7c3d6962bccd97caf2cf0bb4ac9d11630bf5ca7)
- **作者**: Nemo Feng
- **时间**: 2026-04-21T04:54:28Z
- **PR**: [#1132](https://github.com/SerendipityOneInc/ecap-workspace/pull/1132)

### Commit Message

fix(web): sticky sidebar bottom nav with scrollable agent list (ECA-520) (#1132)

## Summary

Addresses [ECA-520](https://linear.app/) — when the agent list grows
long, it pushes the fixed sidebar entries (**AI Specialists Hub**,
**Schedule**, **User Guide**, and **Admin**) plus the user card off the
bottom of the sidebar.

## Root cause

`<nav>` in `SideNav.tsx` was `flex min-h-0 flex-1 flex-col` with a `<div
className="flex-1" />` spacer between the agent list and the bottom
items. No descendant had `overflow-y` set, so as the agent list grew it
stole the spacer's slack and then pushed everything below out of view.

## Approach

Make the agent list the **only flex-absorber** — wrap it in `flex-1
min-h-0 overflow-y-auto` so it takes all remaining vertical space and
scrolls internally. The spacer is removed; the bottom nav and admin
sections now stay naturally pinned at the bottom.

## UI details

- **Hidden scrollbar** — uses the existing `.scrollbar-hide` utility
from `globals.css` (cross-browser: Firefox `scrollbar-width: none` +
WebKit `::-webkit-scrollbar { display: none }`).
- **Shadow overlay on the sticky section** — a `::before` pseudo-element
on the bottom nav container, positioned at `bottom: 100%` with a
`bg-gradient-to-t from-sidebar-background to-transparent` of height
`h-12`. It visually emanates from the sticky nav and covers the bottom
~48px of the agent list, signaling "more content above." Theme-aware
because the gradient uses `var(--sidebar-background)`.
- **Conditional overlay via `data-scroll-state`** — a small effect
tracks three states on the scroll container: `none` (list fits, no
overflow), `overflow` (more above the fold), `end` (scrolled to bottom).
CSS `data-[scroll-state=overflow]:before:opacity-100` shows the shadow
only when there's genuinely more to reveal; a 150ms opacity transition
makes the reveal/hide feel polished.
- **48px scroll-end buffer** — a sentinel `<div aria-hidden
className="h-12 flex-shrink-0" />` at the end of the list. When the user
scrolls all the way down, the last real agent sits above the 48px empty
region and the overlay fades out — so the last agent is fully visible,
not half-clipped, exactly at scroll-end.

## Design preview

Before/after HTML mockup (with slider for agent count, admin toggle, and
theme toggle) added at `docs/design/sidebar-scroll-fix-preview.html` for
future reference.

## Test plan

- [ ] Open `/chat` with many custom agents (≥10 on a laptop display, ≥20
on a tall monitor). Verify all four bottom entries + user card remain
visible.
- [ ] Scroll the agent list to the middle → last visible agent is
half-clipped by a soft shadow.
- [ ] Scroll to the very bottom → shadow fades out, last agent fully
visible.
- [ ] Remove all custom agents (only the default Assistant remains) → no
shadow, no scroll, list looks unchanged from before.
- [ ] Toggle light/dark theme → shadow fade color follows
`--sidebar-background` correctly.
- [ ] Collapse the sidebar (icon-only) → scrolling still works on long
lists.
- [ ] Mobile drawer mode → sticky behavior works the same way.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>

### PR Description

## Summary

Addresses [ECA-520](https://linear.app/) — when the agent list grows long, it pushes the fixed sidebar entries (**AI Specialists Hub**, **Schedule**, **User Guide**, and **Admin**) plus the user card off the bottom of the sidebar.

## Root cause

`<nav>` in `SideNav.tsx` was `flex min-h-0 flex-1 flex-col` with a `<div className="flex-1" />` spacer between the agent list and the bottom items. No descendant had `overflow-y` set, so as the agent list grew it stole the spacer's slack and then pushed everything below out of view.

## Approach

Make the agent list the **only flex-absorber** — wrap it in `flex-1 min-h-0 overflow-y-auto` so it takes all remaining vertical space and scrolls internally. The spacer is removed; the bottom nav and admin sections now stay naturally pinned at the bottom.

## UI details

- **Hidden scrollbar** — uses the existing `.scrollbar-hide` utility from `globals.css` (cross-browser: Firefox `scrollbar-width: none` + WebKit `::-webkit-scrollbar { display: none }`).
- **Shadow overlay on the sticky section** — a `::before` pseudo-element on the bottom nav container, positioned at `bottom: 100%` with a `bg-gradient-to-t from-sidebar-background to-transparent` of height `h-12`. It visually emanates from the sticky nav and covers the bottom ~48px of the agent list, signaling "more content above." Theme-aware because the gradient uses `var(--sidebar-background)`.
- **Conditional overlay via `data-scroll-state`** — a small effect tracks three states on the scroll container: `none` (list fits, no overflow), `overflow` (more above the fold), `end` (scrolled to bottom). CSS `data-[scroll-state=overflow]:before:opacity-100` shows the shadow only when there's genuinely more to reveal; a 150ms opacity transition makes the reveal/hide feel polished.
- **48px scroll-end buffer** — a sentinel `<div aria-hidden className="h-12 flex-shrink-0" />` at the end of the list. When the user scrolls all the way down, the last real agent sits above the 48px empty region and the overlay fades out — so the last agent is fully visible, not half-clipped, exactly at scroll-end.

## Design preview

Before/after HTML mockup (with slider for agent count, admin toggle, and theme toggle) added at `docs/design/sidebar-scroll-fix-preview.html` for future reference.

## Test plan

- [ ] Open `/chat` with many custom agents (≥10 on a laptop display, ≥20 on a tall monitor). Verify all four bottom entries + user card remain visible.
- [ ] Scroll the agent list to the middle → last visible agent is half-clipped by a soft shadow.
- [ ] Scroll to the very bottom → shadow fades out, last agent fully visible.
- [ ] Remove all custom agents (only the default Assistant remains) → no shadow, no scroll, list looks unchanged from before.
- [ ] Toggle light/dark theme → shadow fade color follows `--sidebar-background` correctly.
- [ ] Collapse the sidebar (icon-only) → scrolling still works on long lists.
- [ ] Mobile drawer mode → sticky behavior works the same way.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(web): resolve N+1 /credits/check requests via dedup + cache (#1136)

- **SHA**: [898d4801](https://github.com/SerendipityOneInc/ecap-workspace/commit/898d48014788dbf7eb58c6786295e34ef0079e7a)
- **作者**: peter-srp
- **时间**: 2026-04-21T04:00:14Z
- **PR**: [#1136](https://github.com/SerendipityOneInc/ecap-workspace/pull/1136)

### Commit Message

fix(web): resolve N+1 /credits/check requests via dedup + cache (#1136)

## Summary

Fixes Sentry
[#7353162497](https://serendipity-one-inc.sentry.io/issues/7353162497/)
— N+1 API Call detection on `/api/users/credits/check` (92 events / 10
users since 2025-03-21).

**Root cause**: When a `credits-refresh` event fires, every
`useBillingCredits` hook instance (~7-10 on `/chat`) runs its own
listener which clears `globalFetchingPromise` and fires a separate fetch
— the dedup mechanism is destroyed by the event handler itself.

**Fixes (by priority):**

- **P0 — Microtask-batched refresh**: Added a module-level
`creditsRefreshPending` flag. The first listener in a synchronous event
dispatch schedules a single `queueMicrotask` that clears cache/promise
and calls `refresh(true)` once. Subsequent listeners only bump
`renderTick` (for mock state re-reads) and return early.
- **P1 — Cache-aware pre-flight**: `useSendMessage` now checks
`getCachedCreditsCheck(uid)` before making a raw `/credits/check` API
call; `checkCreditsEnough` returns early when the global cache is fresh
and shows sufficient credits. Backend still rejects if truly
insufficient.
- **P2 — Double-trigger now safe**: `OnboardingProvider` retains its
original immediate + 3s retry pattern for `triggerCreditsRefresh()`.
With P0 in place, each trigger produces at most 1 API call (previously
N), so the double-trigger is benign (2 calls max vs. 2N before).

**Expected result**: A `credits-refresh` event now produces **1** API
call instead of **7+**. Pre-flight checks in chat reuse the 1-minute
cache instead of firing a new request per message send.

## Test plan

- [x] `tsc --noEmit` — zero errors
- [x] ESLint — zero new errors (only pre-existing
`@typescript-eslint/no-explicit-any` warnings)
- [x] Vitest — 76/76 pass (useBillingCredits + useSendMessage suites)
- [x] Regression tests: concurrent refresh dedup, multi-instance mount
dedup, `getCachedCreditsCheck` uid filtering, `checkCreditsEnough`
cache-first
- [ ] Manual: open `/chat`, verify only 1 `/credits/check` call in
Network tab on page load
- [ ] Manual: send a message — no additional `/credits/check` if cache
is fresh
- [ ] Sentry: monitor N+1 issue for resolution after deploy

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary

Fixes Sentry [#7353162497](https://serendipity-one-inc.sentry.io/issues/7353162497/) — N+1 API Call detection on `/api/users/credits/check` (92 events / 10 users since 2025-03-21).

**Root cause**: When a `credits-refresh` event fires, every `useBillingCredits` hook instance (~7-10 on `/chat`) runs its own listener which clears `globalFetchingPromise` and fires a separate fetch — the dedup mechanism is destroyed by the event handler itself.

**Fixes (by priority):**

- **P0 — Microtask-batched refresh**: Added a module-level `creditsRefreshPending` flag. The first listener in a synchronous event dispatch schedules a single `queueMicrotask` that clears cache/promise and calls `refresh(true)` once. Subsequent listeners only bump `renderTick` (for mock state re-reads) and return early.
- **P1 — Cache-aware pre-flight**: `useSendMessage` now checks `getCachedCreditsCheck(uid)` before making a raw `/credits/check` API call; `checkCreditsEnough` returns early when the global cache is fresh and shows sufficient credits. Backend still rejects if truly insufficient.
- **P2 — Double-trigger now safe**: `OnboardingProvider` retains its original immediate + 3s retry pattern for `triggerCreditsRefresh()`. With P0 in place, each trigger produces at most 1 API call (previously N), so the double-trigger is benign (2 calls max vs. 2N before).

**Expected result**: A `credits-refresh` event now produces **1** API call instead of **7+**. Pre-flight checks in chat reuse the 1-minute cache instead of firing a new request per message send.

## Test plan

- [x] `tsc --noEmit` — zero errors
- [x] ESLint — zero new errors (only pre-existing `@typescript-eslint/no-explicit-any` warnings)
- [x] Vitest — 76/76 pass (useBillingCredits + useSendMessage suites)
- [x] Regression tests: concurrent refresh dedup, multi-instance mount dedup, `getCachedCreditsCheck` uid filtering, `checkCreditsEnough` cache-first
- [ ] Manual: open `/chat`, verify only 1 `/credits/check` call in Network tab on page load
- [ ] Manual: send a message — no additional `/credits/check` if cache is fresh
- [ ] Sentry: monitor N+1 issue for resolution after deploy

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@peter-srp: /lgtm

---

## fix(web): subagent session auto-dismiss with server-side status (#1118)

- **SHA**: [9f81426d](https://github.com/SerendipityOneInc/ecap-workspace/commit/9f81426dd7acdf9fc5e6b3de423a7984bf7faf83)
- **作者**: tim-srp
- **时间**: 2026-04-21T03:33:57Z
- **PR**: [#1118](https://github.com/SerendipityOneInc/ecap-workspace/pull/1118)

### Commit Message

fix(web): subagent session auto-dismiss with server-side status (#1118)

## Summary
- Replace client-side time-based `inferStatus` with authoritative
server-side `status` field from OpenClaw's `sessions.list` API (resolves
stale subagent sessions that never disappear)
- Add phase-based auto-dismiss: `running` sessions stay visible,
terminal sessions (`done`/`failed`/`timeout`/`killed`) fade out after
15-20s with CSS transition
- Collapsed sessions show as "N completed" summary button, expandable to
review history and open subagent panels

## Context
OpenClaw subagent sessions use `cleanup: "keep"` by default, so
completed session entries persist in `sessions.json` for 30 days. The
previous frontend used `updatedAt` age to infer status, which was
inaccurate — the server already returns a precise `status` field derived
from the in-memory subagent run lifecycle (`running` | `done` | `killed`
| `failed` | `timeout`).

## Test plan
- [x] Unit tests pass (22 tests across 2 spec files)
- [ ] Verify subagent pills appear with green pulse when running
- [ ] Verify done sessions show checkmark, then fade out after ~15s
- [ ] Verify failed/timeout sessions show red dot, fade out after ~20s
- [ ] Verify collapsed "N completed" button appears after all fade out
- [ ] Verify clicking collapsed button expands to show completed
sessions
- [ ] Verify clicking a collapsed session still opens SubagentChatPanel

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- Replace client-side time-based `inferStatus` with authoritative server-side `status` field from OpenClaw's `sessions.list` API (resolves stale subagent sessions that never disappear)
- Add phase-based auto-dismiss: `running` sessions stay visible, terminal sessions (`done`/`failed`/`timeout`/`killed`) fade out after 15-20s with CSS transition
- Collapsed sessions show as "N completed" summary button, expandable to review history and open subagent panels

## Context
OpenClaw subagent sessions use `cleanup: "keep"` by default, so completed session entries persist in `sessions.json` for 30 days. The previous frontend used `updatedAt` age to infer status, which was inaccurate — the server already returns a precise `status` field derived from the in-memory subagent run lifecycle (`running` | `done` | `killed` | `failed` | `timeout`).

## Test plan
- [x] Unit tests pass (22 tests across 2 spec files)
- [ ] Verify subagent pills appear with green pulse when running
- [ ] Verify done sessions show checkmark, then fade out after ~15s
- [ ] Verify failed/timeout sessions show red dot, fade out after ~20s
- [ ] Verify collapsed "N completed" button appears after all fade out
- [ ] Verify clicking collapsed button expands to show completed sessions
- [ ] Verify clicking a collapsed session still opens SubagentChatPanel

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@tim-srp: ## Response to Codex Review

### 1. 500ms terminal-session refetch loop — Addressed

The dismiss timer was **never** calling `fetchSessions()` — it recalculates phases purely locally via `setSessions()` (see comment at L143-144). However, the 500ms interval was unnecessarily frequent for a local-only recalculation.

**Change:** Increased dismiss timer interval from `500ms` → `3_000ms` (3s), and `FADE_DURATION_MS` from `500ms` → `3_000ms` to match. This ensures:
- The `fading` phase is reliably captured by the 3s tick (previously 500ms fading window could be missed with a slower tick)
- 6x reduction in `setSessions` calls during terminal phase
- Total dismiss timeline: ~18s for `done` sessions (was ~15.5s), ~23s for `failed` (was ~20.5s) — imperceptible difference

### 2. Missing primary-use-case tests — Already covered

The test file has **27 tests** covering:
- Phase timer transitions: `visible → fading → collapsed` full lifecycle
- Multiple sessions with different dismiss delays (`done` 15s vs `failed` 20s)
- Dismiss timer runs locally without extra server fetch (verified `sendRequest` call count)
- Timer auto-stops after all sessions are collapsed
- Server status trust over time-based fallback

The collapsed summary button in `GenClawClient.tsx` is UI rendering logic — appropriate for E2E coverage, not unit-level hook tests.

---

## feat(web): enrich chat tool display — richer text, emoji, collapse, timer (#1100)

- **SHA**: [e0cd8bb8](https://github.com/SerendipityOneInc/ecap-workspace/commit/e0cd8bb881830e62cdd95b526075934f2d3f9887)
- **作者**: peter-srp
- **时间**: 2026-04-21T03:23:58Z
- **PR**: [#1100](https://github.com/SerendipityOneInc/ecap-workspace/pull/1100)

### Commit Message

feat(web): enrich chat tool display — richer text, emoji, collapse, timer (#1100)

## Summary
- Expand action text variants from 4→8 per tool type with longer
narrative phrasing; add `withQuery` for exec/process/write so all tools
can reference user query
- Add emoji pool per tool type (hash-picked per `tool_call_id` for
visual variety, approach B)
- Collapse earlier tools when >3 in expanded state — "N earlier steps"
toggle to avoid 19-row walls
- Show real-time elapsed timer on the running tool + 3-dot bounce
animation replacing thin pulse dot
- Replace streaming indicator with rotating `|` cursor for main output
- Move copy/reply action buttons to right side; only show after
generation completes
- Update en.ts and zh.ts with all new i18n keys

## Test plan
- [ ] Verify tool group renders emoji + richer text for each tool type
- [ ] Trigger >3 tools and confirm only last tool visible with "N
earlier steps" button
- [ ] Click "N earlier steps" to expand full list
- [ ] Confirm running tool shows bounce animation + live elapsed timer
- [ ] Verify rotating | cursor appears at end of streaming text
- [ ] Verify copy/reply buttons appear on right side only after message
completes
- [ ] Switch language to zh and verify all new i18n keys render
correctly

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- Expand action text variants from 4→8 per tool type with longer narrative phrasing; add `withQuery` for exec/process/write so all tools can reference user query
- Add emoji pool per tool type (hash-picked per `tool_call_id` for visual variety, approach B)
- Collapse earlier tools when >3 in expanded state — "N earlier steps" toggle to avoid 19-row walls
- Show real-time elapsed timer on the running tool + 3-dot bounce animation replacing thin pulse dot
- Replace streaming indicator with rotating `|` cursor for main output
- Move copy/reply action buttons to right side; only show after generation completes
- Update en.ts and zh.ts with all new i18n keys

## Test plan
- [ ] Verify tool group renders emoji + richer text for each tool type
- [ ] Trigger >3 tools and confirm only last tool visible with "N earlier steps" button
- [ ] Click "N earlier steps" to expand full list
- [ ] Confirm running tool shows bounce animation + live elapsed timer
- [ ] Verify rotating | cursor appears at end of streaming text
- [ ] Verify copy/reply buttons appear on right side only after message completes
- [ ] Switch language to zh and verify all new i18n keys render correctly

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@peter-srp: /lgtm

---

## fix(web): replace 880KB JPEG bg-pattern with 31KB WebP to fix LCP (#1135)

- **SHA**: [6c516a5d](https://github.com/SerendipityOneInc/ecap-workspace/commit/6c516a5de658b7f5f533a798e79194764fca9796)
- **作者**: peter-srp
- **时间**: 2026-04-21T03:16:06Z
- **PR**: [#1135](https://github.com/SerendipityOneInc/ecap-workspace/pull/1135)

### Commit Message

fix(web): replace 880KB JPEG bg-pattern with 31KB WebP to fix LCP (#1135)

## Summary
- **LCP fix**: panda-claw chat background pattern was a 1638×914
external JPEG (417KB light / 467KB dark) loaded on every `/chat` page
visit — replaced with locally-served WebP (13KB / 18KB, **96.5%
reduction**)
- **DRY**: `OnboardingLayout` hardcoded the same image URL separately;
now shares `--ecap-chat-bg-pattern` CSS token with `GenClawClient`
- **Same-origin**: images move from `assets.yesy.site` CDN to
`public/images/`, eliminating cross-origin DNS/TLS overhead

## Changes
| File | What |
|------|------|
| `web/public/images/chat-bg-pattern-{light,dark}.webp` | Optimized WebP
versions (cwebp q75) |
| `web/src/theme/brand-theme-tokens.css` | Point
`--ecap-chat-bg-pattern` to local WebP |
| `web/src/components/onboarding/OnboardingProvider.tsx` | Update
preload URL |
| `web/src/components/onboarding/OnboardingLayout.tsx` | Replace
hardcoded `style={{}}` with CSS token |

## Test plan
- [ ] Open `/chat` in panda-claw light theme — verify background pattern
renders correctly
- [ ] Toggle to dark mode — verify dark pattern renders
- [ ] Open onboarding flow — verify background pattern matches chat page
- [ ] DevTools Network tab: confirm images load from
`/images/chat-bg-pattern-*.webp` (~13-18KB)
- [ ] Lighthouse: verify LCP improvement on `/chat`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- **LCP fix**: panda-claw chat background pattern was a 1638×914 external JPEG (417KB light / 467KB dark) loaded on every `/chat` page visit — replaced with locally-served WebP (13KB / 18KB, **96.5% reduction**)
- **DRY**: `OnboardingLayout` hardcoded the same image URL separately; now shares `--ecap-chat-bg-pattern` CSS token with `GenClawClient`
- **Same-origin**: images move from `assets.yesy.site` CDN to `public/images/`, eliminating cross-origin DNS/TLS overhead

## Changes
| File | What |
|------|------|
| `web/public/images/chat-bg-pattern-{light,dark}.webp` | Optimized WebP versions (cwebp q75) |
| `web/src/theme/brand-theme-tokens.css` | Point `--ecap-chat-bg-pattern` to local WebP |
| `web/src/components/onboarding/OnboardingProvider.tsx` | Update preload URL |
| `web/src/components/onboarding/OnboardingLayout.tsx` | Replace hardcoded `style={{}}` with CSS token |

## Test plan
- [ ] Open `/chat` in panda-claw light theme — verify background pattern renders correctly
- [ ] Toggle to dark mode — verify dark pattern renders
- [ ] Open onboarding flow — verify background pattern matches chat page
- [ ] DevTools Network tab: confirm images load from `/images/chat-bg-pattern-*.webp` (~13-18KB)
- [ ] Lighthouse: verify LCP improvement on `/chat`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### 人类评论

@peter-srp: /lgtm

---

## fix(ios): Remove bundle_identifier from update_code_signing_settings (#1093)

- **SHA**: [f26b920c](https://github.com/SerendipityOneInc/ecap-workspace/commit/f26b920c0835f96ba8adc0e7dd51b92b7fe92cc5)
- **作者**: bill-srp
- **时间**: 2026-04-21T02:30:09Z
- **PR**: [#1093](https://github.com/SerendipityOneInc/ecap-workspace/pull/1093)

### Commit Message

fix(ios): Remove bundle_identifier from update_code_signing_settings (#1093)

## Summary

Fixes the staging iOS deploy failure ([failed
run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24659916823/job/72102910515))
caused by provisioning profile mismatch on the
`ZooClawNotificationService` target.

The `bundle_identifier` parameter in `update_code_signing_settings` can
leak across targets despite `targets:` scoping, overwriting the
extension's bundle ID
(`one.srp.zooclaw-staging.ZooClawNotificationService`) with the main
app's ID (`one.srp.zooclaw-staging`). This causes the provisioning
profile check to fail.

**Fix:** Remove `bundle_identifier` from all
`update_code_signing_settings` calls in both staging and release lanes.
The pbxproj already has the correct per-target, per-configuration bundle
IDs — only signing settings (profile, identity, team) need overriding at
CI time.

## Test plan

- [ ] Tag `ios-v1.4.0-beta.5` on this branch to trigger staging deploy
- [ ] Verify build completes without provisioning profile errors
- [ ] Verify IPA is produced and uploaded to TestFlight

### PR Description

## Summary

Fixes the staging iOS deploy failure ([failed run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24659916823/job/72102910515)) caused by provisioning profile mismatch on the `ZooClawNotificationService` target.

The `bundle_identifier` parameter in `update_code_signing_settings` can leak across targets despite `targets:` scoping, overwriting the extension's bundle ID (`one.srp.zooclaw-staging.ZooClawNotificationService`) with the main app's ID (`one.srp.zooclaw-staging`). This causes the provisioning profile check to fail.

**Fix:** Remove `bundle_identifier` from all `update_code_signing_settings` calls in both staging and release lanes. The pbxproj already has the correct per-target, per-configuration bundle IDs — only signing settings (profile, identity, team) need overriding at CI time.

## Test plan

- [ ] Tag `ios-v1.4.0-beta.5` on this branch to trigger staging deploy
- [ ] Verify build completes without provisioning profile errors
- [ ] Verify IPA is produced and uploaded to TestFlight

---

## chore(web): drop 6 unused deps + add postcss/tsx + shrink knip allowlist (B4) (#1122)

- **SHA**: [1a357890](https://github.com/SerendipityOneInc/ecap-workspace/commit/1a35789075ef12b5e60677e9447248d7c25fd313)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-21T02:25:06Z
- **PR**: [#1122](https://github.com/SerendipityOneInc/ecap-workspace/pull/1122)

### Commit Message

chore(web): drop 6 unused deps + add postcss/tsx + shrink knip allowlist (B4) (#1122)

## Summary
- Removes 6 deps that no `src/` import references: `@mdx-js/loader`,
`@mdx-js/react`, `@next/mdx`, `@types/mdx`, `@stripe/stripe-js`,
`@types/dompurify`.
- Adds 2 deps that were resolving via pnpm's transitive hoist (fragile):
`postcss`, `tsx`.
- Adds `functions/**` to knip `entry` / `project` so knip sees the
`@sentry/cloudflare` usage in `web/functions/_middleware.ts` natively,
instead of relying on an ignore-list entry.
- Shrinks `knip.config.ts` allowlist from 10 baseline-legacy entries to
**0** — remaining `ignoreDependencies` (3 entries) are all genuine
permanent FPs.

## Verification
- `grep -rn '@mdx-js|@next/mdx|@stripe/stripe-js' web/src` — **zero
hits** (deps fully orphaned)
- `grep -rn 'dompurify' web/src` — only runtime `dompurify` imports;
`@types/dompurify` truly unused (runtime package ships own TS types)
- `grep -rn '@sentry/cloudflare' web/` — **used in
`web/functions/_middleware.ts`** (Cloudflare Pages Functions); kept +
knip entry expanded
- `pnpm test:unit` — **224 test files / 3457 tests pass**
- `WARN_ONLY=1 pnpm lint:ci` — exit 0; knip dep-health gate clean

## knip.config.ts delta

Before (10 allowlist entries): `eslint-config-next`, `@vitest/expect`,
`dependency-cruiser` (3 FPs) + `@mdx-js/loader`, `@mdx-js/react`,
`@next/mdx`, `@types/mdx`, `@stripe/stripe-js`, `@sentry/cloudflare`,
`@types/dompurify`, `postcss` (8 baseline-legacy) + `tsx` (1
ignoreBinaries).

After (3 entries, all permanent FPs):
```ts
ignoreDependencies: [
  'eslint-config-next',   // FlatCompat.extends('next/...') string ref
  '@vitest/expect',       // declare module in web/jest-dom.d.ts
  'dependency-cruiser',   // invoked from shell script (pnpm exec)
],
```

`ignoreBinaries` removed entirely (tsx is now a devDep).

## Why @sentry/cloudflare stays
`web/functions/_middleware.ts`:
```ts
import * as Sentry from '@sentry/cloudflare'
export const onRequest = Sentry.sentryPagesPlugin({...})
```
This is the Cloudflare Pages Function entry — outside Next.js App
Router. Previously knip didn't scan `functions/` so reported it as
unused. The right fix is to expand knip's `entry` / `project` to cover
it, not to ignore the dep.

## Interaction with open PRs
- **#1120 (B3)** is in merge queue. B3 modifies `02-dead-code.sh`
(`--include` list) and `backend.ts` (drops alias exports). B4 modifies
`package.json`, `knip.config.ts`, and `pnpm-lock.yaml`. No file overlap
— both will rebase cleanly regardless of order.

## Test plan
- [x] Unit tests pass (224 files / 3457 tests)
- [x] knip dep-health gate clean with new entry/project globs
- [ ] CI confirms above + jscpd + asset-size-guard
- [ ] Reviewer validates `@sentry/cloudflare` via `functions/` is the
correct resolution (vs permanent ignore-list)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

### PR Description

## Summary
- Removes 6 deps that no `src/` import references: `@mdx-js/loader`, `@mdx-js/react`, `@next/mdx`, `@types/mdx`, `@stripe/stripe-js`, `@types/dompurify`.
- Adds 2 deps that were resolving via pnpm's transitive hoist (fragile): `postcss`, `tsx`.
- Adds `functions/**` to knip `entry` / `project` so knip sees the `@sentry/cloudflare` usage in `web/functions/_middleware.ts` natively, instead of relying on an ignore-list entry.
- Shrinks `knip.config.ts` allowlist from 10 baseline-legacy entries to **0** — remaining `ignoreDependencies` (3 entries) are all genuine permanent FPs.

## Verification
- `grep -rn '@mdx-js|@next/mdx|@stripe/stripe-js' web/src` — **zero hits** (deps fully orphaned)
- `grep -rn 'dompurify' web/src` — only runtime `dompurify` imports; `@types/dompurify` truly unused (runtime package ships own TS types)
- `grep -rn '@sentry/cloudflare' web/` — **used in `web/functions/_middleware.ts`** (Cloudflare Pages Functions); kept + knip entry expanded
- `pnpm test:unit` — **224 test files / 3457 tests pass**
- `WARN_ONLY=1 pnpm lint:ci` — exit 0; knip dep-health gate clean

## knip.config.ts delta

Before (10 allowlist entries): `eslint-config-next`, `@vitest/expect`, `dependency-cruiser` (3 FPs) + `@mdx-js/loader`, `@mdx-js/react`, `@next/mdx`, `@types/mdx`, `@stripe/stripe-js`, `@sentry/cloudflare`, `@types/dompurify`, `postcss` (8 baseline-legacy) + `tsx` (1 ignoreBinaries).

After (3 entries, all permanent FPs):
```ts
ignoreDependencies: [
  'eslint-config-next',   // FlatCompat.extends('next/...') string ref
  '@vitest/expect',       // declare module in web/jest-dom.d.ts
  'dependency-cruiser',   // invoked from shell script (pnpm exec)
],
```

`ignoreBinaries` removed entirely (tsx is now a devDep).

## Why @sentry/cloudflare stays
`web/functions/_middleware.ts`:
```ts
import * as Sentry from '@sentry/cloudflare'
export const onRequest = Sentry.sentryPagesPlugin({...})
```
This is the Cloudflare Pages Function entry — outside Next.js App Router. Previously knip didn't scan `functions/` so reported it as unused. The right fix is to expand knip's `entry` / `project` to cover it, not to ignore the dep.

## Interaction with open PRs
- **#1120 (B3)** is in merge queue. B3 modifies `02-dead-code.sh` (`--include` list) and `backend.ts` (drops alias exports). B4 modifies `package.json`, `knip.config.ts`, and `pnpm-lock.yaml`. No file overlap — both will rebase cleanly regardless of order.

## Test plan
- [x] Unit tests pass (224 files / 3457 tests)
- [x] knip dep-health gate clean with new entry/project globs
- [ ] CI confirms above + jscpd + asset-size-guard
- [ ] Reviewer validates `@sentry/cloudflare` via `functions/` is the correct resolution (vs permanent ignore-list)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(tracking): move gtag init to TSX as verbatim Google snippet (#1133)

- **SHA**: [e4a567a6](https://github.com/SerendipityOneInc/ecap-workspace/commit/e4a567a6e0942749bb4c73c88f5932d60ccb365b)
- **作者**: Fangmiao-srp
- **时间**: 2026-04-21T02:12:20Z
- **PR**: [#1133](https://github.com/SerendipityOneInc/ecap-workspace/pull/1133)

### Commit Message

fix(tracking): move gtag init to TSX as verbatim Google snippet (#1133)

## Summary
- gtag.js internally uses `Array.isArray()` to route dataLayer entries —
Arrays go to a dot-notation path (ignored), only Arguments objects are
recognized as gtag commands
- Our `tracking.ts` used an arrow function with rest params (`(...args)
=> dataLayer.push(args)`), which pushed Arrays instead of Arguments
objects — **all config/event commands were silently ignored, no collect
requests were ever sent**
- Fix: move initialization to `TrackingScripts.tsx` using Google's
original snippet verbatim (`function gtag(){dataLayer.push(arguments)}`)
- Also fixes incorrect Google Ads conversion label
(`LNs9CJnnJp8cEPLbzKxD` → `LNz9CJnnjp8cEPLbzKxD`)

## Changes
| File | Change |
|------|--------|
| `TrackingScripts.tsx` | Added verbatim Google tag init snippet (only
modification: `send_page_view: false` for SPA) |
| `tracking.ts` | Removed module-level init block, fixed conversion
label, removed unused `dataLayer` from type |
| `tracking.unit.spec.ts` | Removed init tests, switched assertions from
dataLayer checks to mock-based |

## Test plan
- [ ] Deploy to staging
- [ ] Open Chrome DevTools Network tab → search for `/g/collect` or
`/j/collect` → confirm requests appear
- [ ] Check Tag Assistant: no more "Deferred hits" warning
- [ ] Verify `window.google_tag_data.tidr.destination` is not empty
- [ ] GA4 DebugView shows real-time events

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Muyao Wang <muyao@MuyaodeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>

### PR Description

## Summary
- gtag.js internally uses `Array.isArray()` to route dataLayer entries — Arrays go to a dot-notation path (ignored), only Arguments objects are recognized as gtag commands
- Our `tracking.ts` used an arrow function with rest params (`(...args) => dataLayer.push(args)`), which pushed Arrays instead of Arguments objects — **all config/event commands were silently ignored, no collect requests were ever sent**
- Fix: move initialization to `TrackingScripts.tsx` using Google's original snippet verbatim (`function gtag(){dataLayer.push(arguments)}`)
- Also fixes incorrect Google Ads conversion label (`LNs9CJnnJp8cEPLbzKxD` → `LNz9CJnnjp8cEPLbzKxD`)

## Changes
| File | Change |
|------|--------|
| `TrackingScripts.tsx` | Added verbatim Google tag init snippet (only modification: `send_page_view: false` for SPA) |
| `tracking.ts` | Removed module-level init block, fixed conversion label, removed unused `dataLayer` from type |
| `tracking.unit.spec.ts` | Removed init tests, switched assertions from dataLayer checks to mock-based |

## Test plan
- [ ] Deploy to staging
- [ ] Open Chrome DevTools Network tab → search for `/g/collect` or `/j/collect` → confirm requests appear
- [ ] Check Tag Assistant: no more "Deferred hits" warning
- [ ] Verify `window.google_tag_data.tidr.destination` is not empty
- [ ] GA4 DebugView shows real-time events

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 2026-04-21


共 41 条 commits

---

## [5fc68303](https://github.com/SerendipityOneInc/ecap-workspace/commit/5fc683030b31de7be479be7141aa4abf894ae1e8)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T15:30:49Z

**Message:**
```
refactor(web): relocate seo.ts from lib/ to app/_seo.ts — fix W1 (A1-PR4) (#1128)

## Summary
- Fixes the remaining W1 violation `lib/seo.ts → @/theme/brand-assets`
by relocating `seo.ts` up one layer (lib → app).
- `seo.ts` is page-metadata logic exclusive to the App Router — all 4
callers already live under `src/app/`. Moving the module is simpler than
restructuring `theme/`.
- Baseline shrinks **17 → 16**. W6 (`theme/brand-themes →
lib/auth/types`) stays in baseline for a separate small PR.

## Why relocate instead of restructuring theme/

Reviewer-suggested approach.

| Scope | This PR (relocate `seo.ts`) | Alternative (split
`theme/brand-*` → `config/brand/*`) |
|---|---|---|
| Files touched | **7** | ~23 |
| Diff | **+5 / −14** | +31 / −49 |
| Violations fixed | W1 | W1 + W6 |
| theme/ structure | unchanged | rewritten |

The alternative required relocating 2 files from `theme/` plus 16 caller
import rewrites. This PR only moves `seo.ts` + its test and updates 4
callers. W6 is a 1-line fix (move `STORAGE_KEYS.BRAND_THEME` out of
`lib/auth/types`) deferred to its own PR.

## Why `@/app/_seo`

`src/app/` forbids top consumer imports from nothing (app is Layer 4),
so `app → theme` is allowed by W1-W6. Leading underscore matches the
existing `src/app/[locale]/_presignedFactory.ts` convention — Next.js
ignores underscore-prefixed non-route files.

Alternative homes considered + rejected:
- `src/app/seo.ts` — no underscore convention in this codebase
- `src/lib/app-metadata/seo.ts` — still `lib/`, W1 still fails
- `src/app/[locale]/_seo.ts` — locks it under [locale]; `app/robots.ts`
and `app/layout.tsx` are root-level

## Changes

| File | Change |
|---|---|
| `web/src/lib/seo.ts` | `git mv` → `web/src/app/_seo.ts` |
| `web/tests/unit/lib/seo.unit.spec.ts` | `git mv` →
`web/tests/unit/app/_seo.unit.spec.ts` |
| `web/src/app/[locale]/about/page.tsx` | import `@/lib/seo` →
`@/app/_seo` |
| `web/src/app/[locale]/layout.tsx` | same + import sort reshuffled |
| `web/src/app/layout.tsx` | same |
| `web/src/app/robots.ts` | same |
| `web/.dependency-cruiser-known-violations.json` | remove W1 seo entry
(17 → 16) |

## Local verification
- `pnpm lint:imports` — exit 0, \`16 known violations ignored\`
- `pnpm test:unit tests/unit/app/_seo.unit.spec.ts` — 6 tests pass
- `npx tsc --noEmit` — clean
- `pnpm lint` — clean

## Remaining baseline 16

After this PR lands: W2(3) / W3(5) / W4(2) / W5(4) / W6(2) — fully
UI-and-feature-isolation cluster + 2 theme-leaf entries (brand-themes →
lib/auth/types + brand-assets → theme internal). Each subsequent cleanup
PR removes a handful.

## Test plan
- [x] Unit tests pass (6 tests)
- [x] dep-cruiser hard gate still green (17 → 16 known violations)
- [x] tsc + eslint clean
- [ ] CI confirms web-quality + asset-size-guard + jscpd
- [ ] Reviewer validates `_seo` underscore naming + relocation approach

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [329248c5](https://github.com/SerendipityOneInc/ecap-workspace/commit/329248c52269a61a9b8fd52c0c4db1347ba4657d)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T15:26:20Z

**Message:**
```
test(web): DiagnosticsSection 全面覆盖 (#894 Step 5 补) (#1129)

## Summary

Epic #894 Step 5 (#899) — 再补一个：\`DiagnosticsSection.tsx\` (338 LOC) 从 0%
→ 全分支。49 tests.

## 源码变动（极小）

- 6 个 pure helper (parseCpu/Memory/Disk + formatCpu/Memory/Disk) 加
export
- 零语义变化、零 runtime 行为变化

## 新增 49 个测试

| 分组 | # | 覆盖 |
|---|---|---|
| parseCpuMillicores | 4 | 空串 / nanocores / millicores / 整核 |
| parseMemoryMiB | 7 | 空串 / Gi/Mi/Ki (binary) / G/M (decimal) / 裸 bytes
|
| parseDiskGiB | 5 | 空串 / Gi / Mi/Ki 降级 / 裸 bytes |
| formatCpu | 4 | 空串 / >= 1000ms / 中段 / sub-milli |
| formatMemory | 4 | 空串 / >= 1024 / 中段 / sub-MiB |
| formatDisk | 4 | 空串 / Gi / Mi / Ki |
| DiagnosticsSection gate | 2 | !botRunning → 提示 / true → Card 渲染 |
| ResourcesCard | 10 | loading/error/empty/data 状态机 / bot_id & pod_name
可选 / disk gauge 有无 / usage=undefined 提示 / refresh 回调 / SemiCircleGauge
>=80% destructive / <80% success / 0% → "—" |
| LogsViewer | 6 | loading/empty/logs / Tail select default=100 + change
传给 refresh / Timestamps checkbox / loading 按钮 disabled |

## Bug-hunting

无新发现。状态机清晰；gauge 阈值切换（80%）逻辑对；parse/format 单位处理完整。

## Test plan

- [x] 49/49 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899)
- 剩余：ConnectorsSection (493) / ClawSettingsClient (438 关键 ~120)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [420c5898](https://github.com/SerendipityOneInc/ecap-workspace/commit/420c589893122447d887fb939d69ea02638b555c)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T15:07:53Z

**Message:**
```
test(web): DiaryCards 全面覆盖 (#894 Step 5 补) (#1121)

## Summary

Epic #894 Step 5 (#899) — 再补一个：\`DiaryCards.tsx\` (150 LOC) 从 0% →
全分支，19 tests。

## 新增 19 个测试

| 组 | # | 覆盖 |
|---|---|---|
| 加载状态 | 1 | 3 个 animate-pulse skeleton |
| 空状态 | 3 | success=true+空文件 / success=false / API reject（finally 清
loading） |
| 列表渲染 | 4 | sort desc + slice(0,10) / first_user_message 兜底 session_id
/ archive_reason 兜底 "Archived session" / 卡片点击 →
router.push('/session-history') |
| formatDate | 6 | ISO 当天 "Today" / 其他日 weekday / Unix seconds / Unix ms
/ invalid → 原样 / 空串 → "Unknown" |
| 滚动控件 | 4 | files ≤ 3 隐藏箭头 / > 3 显示 / 点左 scrollBy(-280) / 点右
scrollBy(+280) |
| Unmount 竞态 | 1 | cancelled flag 防卸载后 setState |

## Harness 要点

- `vi.useFakeTimers()` 先于 `vi.setSystemTime()` — 吃过 #1119 round 2
的教训，`formatDate` 的 "Today" 判断依赖确定"今天"
- i18n mock 对 `t(key) || 'English'` 模式的 key 返回 `''` 触发英文兜底
- jsdom 不实现 `HTMLElement.scrollBy`，用 `Object.defineProperty` 手搭（同
ScrollToBottomButton）

## Bug-hunting

无新发现。组件 unmount race 有正确的 cancelled flag；三个 fallback 链都有。

## Test plan

- [x] 19/19 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899)
- Step 5 已覆盖：ChannelsSection / Slack/Telegram/Discord/FeishuSetup
wizards / Integrations / ModelSection / TimezoneSection / SaveButton /
useClawSettings / useIntegrations / UsageCard (#1119) / 本 PR
- 剩余：ConnectorsSection (493 LOC) / DiagnosticsSection (338 LOC) /
ClawSettingsClient (438 LOC key ~120)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [36d1152b](https://github.com/SerendipityOneInc/ecap-workspace/commit/36d1152b198548cf9d9b5d61d63de5fb9a40e23e)

**Author:** tim-srp  
**Date:** 2026-04-20T15:06:53Z

**Message:**
```
feat(web): replace degraded banner with IQ bar (#1123)

## Summary
- Replace the text-only "积分已用完，正在使用基础模型运行中" degraded banner with a
visual **intelligence bar** (gradient red→green, indicator at 25/100)
- New messaging: "AI 变笨了" / "AI is underpowered" — users immediately
understand quality trade-off instead of being confused by "basic model"
wording
- Theme-aware: IQ bar gradient colors defined as CSS vars
(`ecap-iq-bar-*`) with dark mode support
- 3 new i18n keys (`degradedTitle`, `degradedScore`, `boostAI`) across
all 7 languages

## Motivation
Users on free models attributed poor AI output quality to product bugs
rather than model capability. This redesign makes the quality difference
unmistakably clear.

## Test plan
- [ ] Verify degraded banner renders IQ bar in light mode
- [ ] Verify degraded banner renders correctly in dark mode
- [ ] Verify `expired` and `expiryWarning` variants are unchanged
- [ ] Check all 7 languages display correctly (zh, en, ja, ko, es, pt,
ar)
- [ ] Click "充值提升" / "Boost AI" navigates to `/subscription`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [9ab17392](https://github.com/SerendipityOneInc/ecap-workspace/commit/9ab17392e774753118be0685696f635b9c3a725e)

**Author:** sam-srp  
**Date:** 2026-04-20T14:50:35Z

**Message:**
```
feat(web): preview Mattermost attachments + pptx rendering fixes (#1125)

## Summary

- **Preview MM attachments inline**: clicking a previewable file
attachment (pdf / xlsx / docx / pptx / html / md / code / ...) on a
Mattermost message now opens the artifact preview side panel, and
bot-sent attachments auto-open like today's in-text artifact URLs.
- **Infrastructure**: adds an optional `PreviewSource` on `PreviewFile`
carrying the MM Bearer token. A new `useResolvedUrl` hook fetches MM
URLs with auth once per preview, caches them as blob URLs, and cleans up
on unmount — renderers stay auth-unaware.
- **pptx renderer overhaul**: the existing hand-rolled OOXML renderer
had a long tail of bugs exposed by real-world decks. This PR fixes each
one with a principled spec-based solution.

## What changed in pptx rendering

Text:
- Strip BiDi control chars (stray `U+202E` was reversing titles)
- Drop `display: flex` on paragraphs → flex items were trimming
leading/trailing whitespace, dropping spaces between
differently-formatted runs
- `overflow: visible` on text shapes — PowerPoint lets text overflow
shape bounds; we were clipping tight table cells
- Honor `<a:ea>` / `<a:latin>` typeface with CJK-aware fallback stack
(YaHei → PingFang → Noto CJK)
- Font size in `cqw` units against a per-slide CSS variable → text
scales with the slide container (same behavior as PowerPoint canvas
resize)
- Parse `<a:spcBef>`, `<a:spcAft>`, `<a:lnSpc>` with sensible default
(0.4em) when master defaults would have applied
- Render `<a:buChar>` bullets with hanging indent from `marL` + `indent`

Shapes:
- Parse `<a:custGeom>` paths (moveTo / lnTo / cubicBezTo / quadBezTo /
arcTo / close) to SVG
- Multi-subpath support (was only reading first `<a:path>` of
`<a:pathLst>`)
- `prstGeom` presets as SVG paths: ellipse, line, triangle, diamond,
parallelogram, hexagon, arrows, star5, arc, blockArc
- `prst="arc"` sweep angles from `<a:avLst>` adj1/adj2 with correct
normalization (`?: sw1 sw1 sw2`)
- `xfrm` `rot` / `flipH` / `flipV` applied as CSS transforms
- `roundRect` corner radius uses spec formula `adj / 100000 × min(w, h)
/ 2`
- Border `<a:alpha>` now applied (was ignored — borders rendered at 100%
opacity)

Layout:
- Drop the `max-w-3xl` cap on the preview container so slides fill the
preview pane

Misc:
- Force correct MIME on MM blob URLs (MM serves
`application/octet-stream`, which made `<iframe>` show HTML source text)
- Hide "copy link" on MM-sourced previews (blob URLs aren't shareable)

## Files

- New: `web/src/components/artifacts/useResolvedUrl.ts`,
`docs/superpowers/specs/2026-04-20-mm-attachment-preview.md`
- Modified: `ArtifactPreview.tsx`, `types.ts`, `MMAttachments.tsx`,
`useArtifactsSidebar.ts`, `MarkdownContent.tsx`, `GenClawClient.tsx`,
`PptxRenderer.tsx`

## Test plan

- [ ] Send pdf / xlsx / docx / pptx / html / md / code / csv as MM
attachments → each opens in preview on click; bot-sent attachments
auto-open
- [ ] Download button downloads original file (not blob) with correct
extension
- [ ] Copy-link hidden for MM previews, visible for artifact URLs
- [ ] Existing artifact URL previews unchanged (regression check on
public URLs)
- [ ] pptx: text renders correctly (no reversed titles, no missing
spaces, Chinese fonts OK)
- [ ] pptx: curves / arcs / non-rect shapes render (not collapsed to
rectangles)
- [ ] pptx: preview fills full preview pane width; fonts scale
proportionally

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [00d19e47](https://github.com/SerendipityOneInc/ecap-workspace/commit/00d19e47f27bc9ee1d211d5b73f23954f60c88f1)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T14:56:14Z

**Message:**
```
refactor(web): extract triggerCreditsRefresh to src/lib (A1-PR3) (#1124)

## Summary
- First A1 cleanup PR — fixes 1 of the 2 W1 violations in the baseline.
- Moves the plain-function `triggerCreditsRefresh` out of
`src/hooks/useBillingCredits.ts` into a new
`src/lib/billing-credits.ts`.
- Rewrites **all 3** call sites (no re-export shim) and shrinks the
baseline 18 → 17.

## Why `triggerCreditsRefresh` doesn't belong in `hooks/`
```ts
export function triggerCreditsRefresh(): void {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent('credits-refresh'))
  }
}
```
No React state, no `use*` dependency — it's a plain event dispatcher
that happened to live alongside the `useBillingCredits` hook. Any `lib/`
module needing to signal "refresh credits" had to import from
`@/hooks/*`, which is exactly the W1 contract violation (`lib → hooks` —
upward dependency).

## Changes

| File | Action |
|---|---|
| `web/src/lib/billing-credits.ts` | **new** — 14 lines, single function
|
| `web/src/hooks/useBillingCredits.ts` | drop the function + its
comment; `getCachedCredits` / `clearCreditsCache` / hook stay |
| `src/components/billing/SubscriptionPanel.tsx` | `@/hooks` →
`@/lib/billing-credits` for this symbol |
| `src/components/onboarding/OnboardingProvider.tsx` | same |
| `src/lib/payment/handlePaymentSuccess.ts` | same (the W1 violator) |
| `tests/unit/lib/billing-credits.unit.spec.ts` | **new** — 2 tests
moved from hooks spec |
| `tests/unit/hooks/useBillingCredits.unit.spec.ts` | describe block
removed + import trimmed |
| `tests/unit/lib/payment/handlePaymentSuccess.unit.spec.ts` | mock path
+ dynamic-import path |
| `tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx` |
split single `vi.mock(@/hooks/useBillingCredits)` into 2 mocks |
| `web/.dependency-cruiser-known-violations.json` | removed the fixed
`handlePaymentSuccess.ts → useBillingCredits.ts` entry |

No re-export shim is left behind, per the project convention
(`feedback_no_reexport_shim` in the author's memory).

## Baseline shrinks 18 → 17
The `depcruise-baseline` pattern designed in A1-PR2 works as expected:
each cleanup PR removes one entry from the baseline JSON and fixes the
corresponding import. When the JSON is `[]` the baseline file itself can
be deleted.

Remaining W1: `src/lib/seo.ts → @/theme/brand-assets` (11-caller
refactor, deferred to its own PR).

## Local verification
- `pnpm lint:imports` — exit 0, prints `17 known violations ignored`
- `pnpm test:unit` on the 4 affected files — **68 tests pass**
- `pnpm lint` — clean (simple-import-sort auto-fixed during commit)
- `npx tsc --noEmit` — clean

## Test plan
- [x] Unit tests pass (all 4 affected files)
- [x] dep-cruiser hard gate still green (baseline shrinks 18 → 17)
- [ ] CI confirms above
- [ ] Reviewer validates split mock approach in
`SubscriptionPanel.unit.spec.tsx` (one `vi.mock` per module)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [36587abd](https://github.com/SerendipityOneInc/ecap-workspace/commit/36587abd8cc613e6d841b13fe3237f0a2e602273)

**Author:** tim-srp  
**Date:** 2026-04-20T14:34:53Z

**Message:**
```
test(e2e): add model switching, onboarding & subscription E2E tests (#1019)

## Summary
- **Model Switching**: selector button, dropdown tabs, tab filtering,
model selection, ESC close
- **Onboarding Flow**: full 4-step UI via `?onboarding=preview` mode
(invite code → name → companion → loading)
- **Subscription & Pricing**: public pricing page, subscription panel,
billing toggle, plan CTAs; staging-only Stripe sandbox tests (upgrade
redirect, downgrade/cancel modals)

## Files
- `web/tests/e2e/specs/model-switching.spec.ts` — 5 scenarios
- `web/tests/e2e/specs/onboarding-flow.spec.ts` — 5 scenarios
- `web/tests/e2e/specs/subscription-pricing.spec.ts` — 10 scenarios (3
staging-only)
- `web/playwright.config.ts` — register 3 new projects

## Test plan
- [ ] `pnpm exec playwright test --project=model-switching`
- [ ] `pnpm exec playwright test --project=onboarding-flow`
- [ ] `pnpm exec playwright test --project=subscription-pricing`
- [ ] Staging: `E2E_ENV=staging pnpm exec playwright test
--project=subscription-pricing`

## Follow-up fixes

### `onboarding-flow` — preview-mode starts on step 1 again
Local run against staging surfaced one real bug:

**Symptom**: Scenario 1 "Step 1 — Invite Code entry" timed out with
Continue button `[disabled]`; 3 downstream scenarios skipped via serial
mode.

**Root cause**: two conflicts with the shared auth state / page chrome:
1. `auth.setup.ts` seeds `ecap:onboarding:progress` marking every step
completed (so other specs bypass the modal). This spec inherited that
storage state and was landing on Companion Select instead of step 1.
2. `GuideTourModal` (`fixed inset-0 z-[100]`) overlays the viewport on
fresh sessions and intercepts pointer events on the invite code form —
Playwright log: `<img alt="One brain. Full crew." ... from <div
data-sentry-component="GuideTourModal" ...> subtree intercepts pointer
events`.

**Fix** (`onboarding-flow.spec.ts` `beforeAll`, no business-code
changes):
- Strip `ecap:onboarding:progress*` keys via `addInitScript` so React
reads `DEFAULT_PROGRESS` and renders step 1.
- Apply `E2E_OVERLAY_SUPPRESSION` (same set used by `model-switching` /
`agent-hire-fire`) to dismiss `GuideTourModal` + compensation popup.
- Scenario 1: wait for `"Got an invite code?"` prompt before
interacting, switch to `input[placeholder="Enter code"]` +
`pressSequentially('TESTCODE', { delay: 30 })` so the controlled input's
`onChange` (with `.toUpperCase()` transform) reliably fires, and `await
expect(continueBtn).toBeEnabled()` before click so a future state-sync
regression surfaces in 5s rather than a 180s disabled-click timeout.

**Local verification**: `E2E_ENV=staging pnpm test:e2e
--project=onboarding-flow` → **6/6 passed in 21.5s**.

### Auto-review follow-ups
- **Stripe popup race** (subscription-pricing Upgrade scenario):
`popup.url()` was read the instant the event fired, but Stripe opens
`about:blank` first and then redirects — capture could be `about:blank`
and silently fail. Also, `page.on('popup', ...)` leaks a long-lived
handler across tests. Switched to a scoped `page.waitForEvent('popup')`
raced against the click, then
`popup.waitForURL(/checkout\.stripe\.com/)` before reading the URL.
- **Tailwind-class locator** (model-switching selection scenario):
`option.locator('.text-sm.font-medium')` violated `web/CLAUDE.md`'s
"Tailwind class strings are styling, not contract" rule. Added
`data-testid="model-option-name"` on the model display-name div and
updated the test to use `getByTestId`.
- **Dead redirect fallback in upgrade assertion**: `SubscriptionPanel`
always uses `window.open(..., '_blank', 'noopener,noreferrer')` — there
is no in-tab redirect path. The previous `else {
expect(page.url()).toContain(...) }` was dead code that produced a
confusing `/en/subscription does not contain checkout.stripe.com`
message when the popup event was missed. Replaced with two explicit
assertions: popup must be captured (self-explanatory failure message) +
captured URL must contain `checkout.stripe.com`.

### Known non-blockers (not addressed in this PR)
- `waitForTimeout(300)` after tab clicks in a few places — pragmatic
transition-animation padding; would only be worth revisiting if slow CI
produces flake.
- Hardcoded `100`/`200` price assertions — already scoped to
`plan-card-pro` / `plan-card-ultra` so no broad matching; easier to
update when prices actually change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [7660252d](https://github.com/SerendipityOneInc/ecap-workspace/commit/7660252dcc693d25b259cc801db9a8c012d58cb7)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T14:14:29Z

**Message:**
```
refactor(web): drop backend.ts BackendAPI aliases + promote duplicates gate (B3) (#1120)

## Summary
- Cleans the 6 legacy `*BackendAPI` alias exports in
`web/src/lib/api/backend.ts` — the sole content of knip's "duplicate
exports" baseline.
- Promotes the `duplicates` category to knip's hard gate in
`02-dead-code.sh` so new aliases fail CI.
- First content-cleanup PR of the B track.

## Scope
- `web/src/lib/api/backend.ts`: remove the 6 alias exports
(`callBackendAPI` = `callAPI`, etc). Only reference in src/ is
`backend.ts` itself.
- `web/tests/unit/lib/api/backend.unit.spec.ts`: remove the "backward
compatible exports" `describe` block (sole consumer of the aliases). 19
functional tests remain.
- `web/scripts/ci-lint/02-dead-code.sh`: add `duplicates` to knip
`--include`; header comment updated to match the new incremental-gate
roadmap.

## Why this was safe to drop
`grep -r '(call|get|post|put|delete|patch)BackendAPI' web/` returned
only:
1. `web/src/lib/api/backend.ts` — the 6 `export const` lines themselves
2. `web/tests/unit/lib/api/backend.unit.spec.ts` — the one test block
that asserted they === the canonical functions

No production code (src/ or tests/e2e/) imports the alias form. The
"向后兼容" comment suggests they were kept during a rename from `BackendAPI`
→ `API`; the rename is now fully absorbed.

## Local verification
- `pnpm test:unit tests/unit/lib/api/backend.unit.spec.ts` — **19 tests
pass**
- `WARN_ONLY=1 pnpm lint:ci` — **exit 0**; knip dep-health gate (now
including `duplicates`) reports 0 violations
- `pnpm lint` — clean (prettier fixed one trailing-newline issue
post-edit)

## Interaction with open PRs
- **#1115 (A1-PR2)** is in merge queue. B3 doesn't touch
`01-import-boundaries.sh`, the baseline JSON, or the workflow step, so
order-of-merge doesn't matter. Whichever lands first, the other rebases
cleanly.

## Test plan
- [x] 19 existing backend.ts unit tests pass
- [x] Orchestrator runs knip with `duplicates` included, 0 violations
- [ ] CI confirms above
- [ ] Reviewer validates that `backward compatible exports` describe was
the only test coupling to the aliases

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [4248accc](https://github.com/SerendipityOneInc/ecap-workspace/commit/4248acccde09e22c372b02bac94d64a44cd534b5)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T14:12:45Z

**Message:**
```
test(web): UsageCard 全面覆盖 (#894 Step 5 补) (#1119)

## Summary

Epic #894 Step 5 (#899) — 再补一个：\`UsageCard.tsx\` (249 LOC) 从 0% → 全分支，20
tests。

## 新增测试

| 组 | # | 覆盖 |
|---|---|---|
| 内容状态机 | 4 | error / no-data / loading / usage 呈现 |
| Stat tile 值 | 6 | messages user/asst 分解 / latency.count=0 → "—" /
ms→秒格式 (1.2s, p95 2.5s) / sessions / errors + "of N messages" /
toolCalls + uniqueTools |
| 日期预设 | 5 | default=today / yesterday / 7days / preset sticky / loading
→ refresh disabled |
| DailyStrip | 3 | empty / length=1 (阈值>1 隐藏) / length>=2 渲染 bar+tooltip
|
| TopTools | 2 | 空数组隐藏 / slice(0,5) 截断 |

## Harness 要点

- \`vi.setSystemTime(new Date('2026-04-20T12:00:00Z'))\` 固定让
\`dateRange()\` preset 派生日期确定
- i18n mock 返回 key，文案断言全走 key

## Bug-hunting

无新发现。状态机切换合理，preset sticky 逻辑对。

## Test plan

- [x] 20/20 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899) 
- 续 DiscordSetupWizard #1112 / ChannelsSection / Slack / Telegram /
Feishu / ModelSection / TimezoneSection / SaveButton (这些已有测试)
- 剩余 Step 5 未覆盖：ConnectorsSection (493 LOC) / DiagnosticsSection (338
LOC) / DiaryCards (150 LOC) / ClawSettingsClient (438 LOC, key parts
~120)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [83a5cade](https://github.com/SerendipityOneInc/ecap-workspace/commit/83a5cade46d88463393461e8d375b8a47bc2d7ef)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T14:01:19Z

**Message:**
```
feat(web): freeze import-boundaries baseline + flip hard gate (A1-PR2) (#1115)

## Summary
- Merges original A1-PR2 (baseline) + A1-PR3 (hard gate) into one
rollout step — same 2-phase pattern as deptry / B2.
- Generates `.dependency-cruiser-known-violations.json` containing the
18 legacy violations frozen via `depcruise-baseline`.
- `01-import-boundaries.sh` drops `WARN_ONLY`, uses `--ignore-known` —
baseline passes, new violations fail CI.
- CI step no longer sets `WARN_ONLY=1`.

## Baseline contents

18 known violations (14 errors + 4 warnings) — same numbers reported in
#1098 warn-mode run:

| Contract | Count |
|----------|-------|
| W1 (lib pure) | 2 |
| W2 (hooks pure) | 3 |
| W3 (contexts pure) | 5 |
| W4 (components below pages) | 2 |
| W5 (feature isolation) | 4 |
| W6 (theme leaf) | 1 |

## Maintenance

Each A1-PR3+ cleanup PR removes a batch of entries from
`web/.dependency-cruiser-known-violations.json` and fixes the matching
imports. The file shrinks monotonically until empty.

Regenerate with:
```bash
pnpm exec depcruise-baseline --config .dependency-cruiser.cjs 'src/**/*.{ts,tsx}'
```

## Local verification
- `pnpm lint:imports` — exit 0, prints `18 known violations ignored`.
- A novel violation (e.g. `src/lib/foo.ts` importing `@/components/Bar`)
would fail the gate since it's not in the baseline.

## Spec changes
The PR matrix in
`docs/superpowers/specs/2026-04-20-web-import-boundaries.md` is updated
from 5 phases to 3 (PR0 spec / PR1 warn / PR2 baseline + hard gate /
PR3+ cleanup). Rationale: after PR1 landed, the `@/*` alias resolver
risk was confirmed resolved, so the extra "soft baseline freeze" step
between warn and hard gate added no safety margin. Mirrors the B track's
2-phase approach.

## Interaction with open PRs
- **#1106 (B2)**: currently sets `WARN_ONLY=1` on its `Web CI-lint
orchestrator` step because A1 was still in warn mode. Once this PR
lands, B2 rebase will drop that env block — the `WARN_ONLY` path is gone
from `01-import-boundaries.sh` and no longer needed.

## Test plan
- [ ] CI `web-quality` job runs new step, `01-import-boundaries.sh`
passes on baseline, exit 0
- [ ] Existing ESLint / TS / unit-test / jscpd / asset-size steps
unchanged
- [ ] PR-size gate passes
- [ ] Reviewer validates the baseline file format (each entry has
`type`, `from`, `to`, `rule.name`, `rule.severity`) and that W1-W6 all
represented

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [ef416402](https://github.com/SerendipityOneInc/ecap-workspace/commit/ef4164027d04434ec615b6b486a51fcf1b00c26c)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:57:30Z

**Message:**
```
ci: skip redundant gating on push:main in code-quality.yml (#1038) (#1111)

## Context

Closes #1038. After merge queue was enabled, every PR merge produces
**two** `code-quality` runs against the same commit SHA:

1. **merge_group** (gating, before fast-forward) — must pass to allow
merge
2. **push:main** (after fast-forward) — duplicates all gating, and
occasionally red-crosses main from unrelated flakes

Example: PR #994's merge produced runs
[24558845557](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24558845557)
(merge_group ✅) and
[24559126136](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24559126136)
(push ❌, Simulator CoreData teardown flake).

## Approach (issue option A — minimal)

Guard pure gating steps with `if: github.event_name != 'push'` so they
skip on main-branch pushes. Test + coverage + badge publishing steps are
untouched so the iOS/web coverage badges keep updating on every merge.

### Affected steps

| Job | Gating steps now skipped on `push:main` |
|---|---|
| `web-quality` | Lint, ignores SHRINK-ONLY check, Import boundaries
(warn-mode), Type check, jscpd src + tests |
| `ios-quality` | SwiftLint, jscpd src + tests |
| `python-duplication-check` | entire job (guarded at job level) |
| `claw-interface-quality` | entire reusable-workflow job (guarded at
job level) |

The aggregator `code-quality` step is updated to treat `skipped` status
on python jobs as non-failure (previously required `success`).

## Intentionally not addressed

- **iOS unit tests still run on push:main**, because they produce the
coverage artifact the iOS badge step consumes. A Simulator flake during
that step can still red-cross main (which is **issue #1038 acceptance
item 3**). Fixing that requires moving iOS test + badge publishing into
the `merge_group` event instead of `push:main`, which is a larger
architectural change. Tracked in #1116.
- **`on: push: branches: [main]` trigger kept intentionally** so a
manual/bypass push still triggers a run (not a silent no-op). The
improvement comes from step-level skipping, not trigger removal.

## Verification

`act` isn't available in this worktree, so the real verification is the
first post-merge `push:main` run: look for Lint / tsc / jscpd /
SwiftLint rows marked `skipped` in the `ios-quality` + `web-quality`
jobs under the main-branch run.

Meanwhile this PR's own CI (which runs under `pull_request` event)
executes the **full** gating path — confirming the added `if` conditions
don't break the PR-time gate.

## Test plan

- [x] YAML structure reviewed for unintended step ordering / missing-if
errors
- [x] `code-quality` aggregator updated so `python*` jobs in `skipped`
state don't falsely fail
- [ ] Post-merge verification: first `push:main` run after merge should
show Lint/tsc/jscpd/SwiftLint as `skipped`, with `Unit Tests with
Coverage` + badge steps still running

Closes #1038

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [11143a30](https://github.com/SerendipityOneInc/ecap-workspace/commit/11143a3096ff4636f461ff364fcdb2c4ec56eef8)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:43:45Z

**Message:**
```
test(web): DiscordSetupWizard 全面覆盖 (#894 Step 5 补) (#1112)

## Summary

Epic #894 Step 5 (#899) 的 setup wizard 三件套对齐 — Slack / Telegram 已有测试，本
PR 补 Discord。
20 tests / +320 source LOC from 0% → 全分支。

## 新增 20 个测试

| 分组 | # | 覆盖点 |
|---|---|---|
| welcome step | 3 | 渲染 / Cancel → onClose / getStarted 推进 |
| create-app step | 3 | 6 步说明 + developer portal link target/rel / back
→ welcome / next → input-token |
| input-token validation | 4 | 空 token / <50 字符 invalid hint / >=50
enabled / back 清 error |
| advanced config toggle | 3 | 折叠默认 / 展开后 dm/group select + account
input / 透传到 addClawChannel payload |
| handleConnect | 5 | 成功路径 + addClawChannel 默认参数 / Error 实例 message 显示 /
非 Error fallback / account 空白→"default" / token trim |
| invite step | 2 | 5 步 invite 说明 / Done → onSuccess+onClose |

## Bug-hunting

`complete` step 是源码 dead branch — 没有 handler 会触发它，纯 UI 无障碍路径。提 issue
或清理看后续收尾 PR。

## Test plan

- [x] 20/20 通过
- [x] tsc clean
- [x] lint clean
- [ ] CI 绿

## 关联

- Epic #894 Step 5 (#899)
- 续 Slack / Telegram wizard specs

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [05353087](https://github.com/SerendipityOneInc/ecap-workspace/commit/0535308785099c80be50f745cfadd7b708cc06f0)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:42:23Z

**Message:**
```
test(web): GenClawClient 内部组件覆盖 (#894 Step 4) (#1110)

## Summary

Epic #894 Step 4 (#898)。\`GenClawClient.tsx\` 默认导出 1100+ LOC 是整合组件（hooks
+ 布局 + provider 链），走 E2E 更合适。本 PR 聚焦 issue #898
明确点名的两块（**ChatErrorBoundary** + **连接错误 modal**），加上几个纯 UI helper，从
GenClawClient.tsx 导出内部组件让它们可独立受测。

## 源码变动（极小）

- 8 处 \`function\` → \`export function\` / \`class\` → \`export class\`
- 零语义变化、零 runtime 行为变化

## 新增 48 个测试

| 组件 | # | 覆盖点 |
|---|---|---|
| \`formatChannelTime\` | 8 | pure function — 空值 / NaN / 秒 vs 毫秒 自动缩放 /
分钟/小时/天分段 |
| \`ChannelIcon\` | 7 | 6 种平台 emoji 渲染 / 未知平台 SVG fallback /
case-insensitive |
| \`RemoteStatusBadge\` | 8 | 5 种 status → dot 颜色 / unknown fallback /
waiting pulse / message vs status 降级 |
| \`Toast\` | 4 | 渲染 + 4000ms 自动 dismiss / X 按钮立即关闭 / unmount 清 timer |
| \`ConfirmModal\` | 6 | open=false 不渲染 / 默认/自定义 labels /
onConfirm/onCancel / typeToConfirm gate / destructive variant / close 重置
typed |
| \`AdvancedRecreate\` | 5 | 展开/收起 / RECREATE 输入门 / onRecreate 触发 /
Cancel 路径 |
| \`ConnectionErrorModal\` | 5 | headline + status badge / wsError 段 /
reconnect 按钮 / redeploy→ConfirmModal→Confirm / redeploy Cancel |
| \`ChatErrorBoundary\` | 3 | 无错误透传子组件 / getDerivedStateFromError 返回空
partial / componentDidCatch 打 logger.warn + setState updater 增 errorKey
|

## 测试策略

### ChatErrorBoundary — 直接调类方法
React 19 concurrent replay 会同步重放 render 跳过正常 commit 路径，用 \`throw\`
驱动错误边界会 flaky。改为：直接 \`new ChatErrorBoundary()\`，spy setState，调
componentDidCatch 和 getDerivedStateFromError — 100% 确定。

### 其他内部组件 — render + testid + 行为断言
ConfirmModal 里的 "Confirm"/"Cancel" 按钮实际 label 是 t(key) ||
'fallback'。i18n mock 返回 key，所以 DOM 上显示 \`common.cancel\` /
\`genClaw.recreateClaw\`。getAllByText 处理同 label 多元素（modal h3 + button
同文本）。

## 不在本 PR 范围

- **auth 检查分支**：位于默认导出内部（async useEffect 里校 uid + router.push）。要测就得 mock
60+ 依赖或直接渲染默认导出 — 性价比太低，issue 里"auth 检查"留给 E2E 或后续独立 PR。
- **useEffect 里抛错是否被 ErrorBoundary 捕获**：issue bug-hunting 里提到；已在
ChatErrorBoundary 说明 componentDidCatch 只捕 render/children 抛错，effect 抛错是
React 已知 gotcha，不在本 PR 范围。

## Test plan

- [x] 48/48 GenClawClient.internals 测试通过
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [ ] CI 绿

## 关联

- Epic #894 Step 4 (#898)
- #898 还剩 \`GenClawClient.tsx\` 默认导出的 auth 检查分支（超出本 PR），建议等 E2E 补

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [630953e5](https://github.com/SerendipityOneInc/ecap-workspace/commit/630953e573fcf8f3ec9e2929f2b5f9d25ff07366)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:38:44Z

**Message:**
```
feat(web): wire knip for dead code / dep health gate (B2) (#1106)

## Summary
- Wires **knip** as a hard gate for dep-health categories in `web/` CI.
- Content-level categories (files / exports / types / duplicates) are
reported informationally; hard-gated in later B-track PRs.
- Implements all three rounds of #1095 review feedback directly.
- B2 scope: **install + baseline freeze + hard gate for dep-health
only**.

## Baseline (absorbed in `knip.config.ts`)

| Category | Count | Handling |
|----------|-------|----------|
| Unused dependencies | 7 | `ignoreDependencies` baseline legacy — B4
cleans |
| Unlisted dependencies | 1 (`postcss`) | `ignoreDependencies` — B4 adds
explicitly |
| Unlisted binaries | 1 (`tsx`) | `ignoreBinaries` — B4 `pnpm add -D
tsx` |
| Permanent FPs | 2 | `eslint-config-next` + `@vitest/expect` — kept
separate |
| Unused files | 28 | Informational (B5) |
| Unused exports | 39 | Informational (B6+) |
| Unused types | 58 | Informational (B6+) |
| Duplicate exports | 6 | Informational (B3 first target) |

`pnpm lint:deadcode` exit 0 locally. Dep-health hard gate clean: 0
violations outside the allowlist.

## #1095 review feedback addressed in this PR

From round 2:
- ✅ `eslint-config-next` as permanent FP (FlatCompat string ref)
- ✅ `@vitest/expect` as permanent FP (`declare module` augmentation in
`web/jest-dom.d.ts:20`)
- ✅ App Router metadata entries (`robots.ts` + preventive `sitemap` /
`manifest` / OG images / icons)
- ✅ knip version pinned to exact `6.5.0` (no caret)

From round 3:
- ✅ `project` glob includes `.mts`
- ✅ `tsx` correctly scoped to `ignoreBinaries` (rather than
`ignoreDependencies`)
- ✅ Independent `02-dead-code.sh` script, decoupled from A1's
`00-run-all.sh` to avoid merge-order coupling between A track and B
track

## Rollout contract
B2 gate covers: `dependencies / devDependencies / unlisted / binaries /
unresolved / optionalPeerDependencies`. Content categories ship in:
- **B3** → promote `duplicates` to hard gate + clean 6 in
`src/lib/api/backend.ts`
- **B5** → promote `files` + delete 28 unused files
- **B6+** → promote `exports / types / enumMembers / ...`
module-by-module

Each category-promotion PR adds its type to the `--include` list in
`02-dead-code.sh` and removes the corresponding allowlist entries.

## Test plan
- [x] `pnpm lint:deadcode` exit 0 locally
- [x] Full report prints 131 informational items then dep-health gate
prints 0 violations
- [ ] CI `code-quality / web-quality` runs new step, gate passes
- [ ] Existing ESLint / TS / unit-test / jscpd steps unchanged
- [ ] Reviewer validates `ignoreDependencies` permanent vs legacy split
is correctly commented

## Notes
- Runs independently of A1-PR1 (#1098). Both PRs add files under
`web/scripts/ci-lint/` but non-overlapping (`02-*` here, `00-*` / `01-*`
there); git auto-merge should resolve cleanly.
- `@sentry/cloudflare` in the legacy list with a comment — may resolve
via `src/instrumentation.ts`; B4 to verify before removing.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [20e8e062](https://github.com/SerendipityOneInc/ecap-workspace/commit/20e8e0623c0bfa80b73e5d8d1dedc170d9917490)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:33:15Z

**Message:**
```
chore(web): promote tests/ no-unused-vars from warn to error (#1073) (#1114)

Follow-up to #1109, which cleared the 23-warning backlog.

With the backlog at zero, flipping severity to `error` is the missing
piece — the lint script runs `eslint src/ tests/ --quiet`, which
silently filters warnings out of CI output, so warn-level here was
effectively a no-op. Error-level means future regressions actually break
the build.

## Summary

- `web/eslint.config.mjs` `tests/` override:
`@typescript-eslint/no-unused-vars` from `'warn'` → `'error'`
- Kept the existing `^_`-prefix ignore patterns untouched (so
deliberately-unused destructures like `_setMessages` still pass)

## Test plan

- [x] `pnpm --filter web lint` — clean (exit 0)
- [x] Quick sanity: manually introduced a bogus unused var locally,
confirmed lint now fails
- [x] Depends on #1109 being merged to main (confirmed at the time of
branching this PR off `origin/main`)

Closes #1073

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [7fdf7f08](https://github.com/SerendipityOneInc/ecap-workspace/commit/7fdf7f08be76b0b096cc76ab65fcc0eff5c15844)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:16:52Z

**Message:**
```
chore(web): clean up 23 no-unused-vars warnings in tests/ (#1109)

Preparatory cleanup so the follow-up PR can promote
`@typescript-eslint/no-unused-vars` from `warn` to `error` in the
`tests/` override without CI going red. Currently silenced by `eslint
src/ tests/ --quiet` in the `lint` script, so warnings have been
accumulating invisibly.

## Summary

- 3 unused imports: `beforeEach`, `waitFor`, `AuthSubscribe` type
- 1 motion stub destructure in PaywallContent: rename
`initial`/`animate`/`exit`/`transition` to underscore-prefixed so they
still get stripped out of DOM props but satisfy the `/^_/u` pattern
- 12 unused `setMessages` destructures in
`useCanvasSession.unit.spec.ts`: rename to `_setMessages` (helper
returns both the mock and `result`; tests only assert on `result`)
- 3 unused `handlers` destructures in `useOpenClawChat.unit.spec.ts`:
dropped from destructuring
- 1 unused `callbacks` destructure in `useSSEStream.unit.spec.ts`:
dropped
- 4 stale `// eslint-disable-next-line
@typescript-eslint/no-explicit-any` directives that had no matching
warning (auto-fixed by `eslint --fix`)

Zero behavior change, zero test coverage change — purely removing dead
bindings.

## Follow-up

Next PR will:
1. Promote `@typescript-eslint/no-unused-vars` from `warn` to `error` in
the tests/ override (`web/eslint.config.mjs:458-466`)
2. Keep `--quiet` in the lint script (other warning-level rules would
otherwise flood CI logs)

Tracking #1073.

## Test plan

- [x] `npx eslint tests/ --rule '{"@typescript-eslint/no-explicit-any":
"off"}'` — 0 warnings, 0 errors (was 23+4)
- [x] `pnpm --filter web test:unit useCanvasSession useOpenClawChat
useSSEStream useArtifactsSidebar useMattermostIntegration GeneralTab
PaywallContent` — 160/160 pass
- [x] `pnpm --filter web lint` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [01f9c695](https://github.com/SerendipityOneInc/ecap-workspace/commit/01f9c69550b6b738aa89fcdc5095517debecf6cf)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:09:21Z

**Message:**
```
test(web): OpenClawThread 全面覆盖 (#894 Step 3 补) (#1107)

## Summary

Epic #894 Step 3 (#897) 剩下的最后一个文件。其余 5 个 Step 3
文件（OpenClawAssistantMessage / OpenClawUserMessage / useArtifactsSidebar
/ useMattermostIntegration / useOpenClawRuntime）都已经有测试 — 本 PR 把
\`OpenClawThread.tsx\` (380 LOC) 从 0% 补到全分支。

## 新增 30 个测试

| 分组 | 数量 | 覆盖点 |
|---|---|---|
| historyLoaded / awaitingGreeting 门控 | 5 | Empty 分支 / "Setting things
up" 横幅 / compact 变体 bypass |
| Load older messages | 4 | hasMore / loadingMore disabled / 点击回调 |
| QuickActionCards 可见性 | 8 | 8 条显示门控全覆盖（messageCount / historyLoaded /
awaitingGreeting / thread.isRunning / compact / onSendMessage /
showQuickActions / agentId 透传）|
| UserMessageFactory | 4 | \`__SESSION_DIVIDER__\` → SessionDivider 分流 /
isLastMessage / compact 透传 |
| AssistantMessageFactory | 5 | isConsecutive 4 种组合（首条 / 前条 user / 前条
assistant / 前条 tool-group）+ props 透传 |
| auto-scroll 副作用 | 2 | 新 user 消息 → scrollTo instant / 新 assistant 不触发 |
| ScrollToBottomButton | 2 | 阈值下隐藏 / 阈值上显示+点击滚动 |

## Harness 要点

**\`@assistant-ui/react\` mock**：\`useMessage()\` 需要 per-message 上下文，用
\`React.createContext\` 模拟 — 模块级变量会被 lazy JSX eval 覆盖成最后一次迭代值（classic
closure pitfall，已踩过一次）。

**jsdom \`scrollTo\` 缺失**：\`HTMLElement.scrollTo\` 在 jsdom 里没实现；用
\`Object.defineProperty(el, 'scrollTo', { configurable: true, value:
vi.fn() })\` 手搭，不能用 \`vi.spyOn\`（spyOn 要求属性存在）。

**子组件 stub**：OpenClawUserMessage / OpenClawAssistantMessage /
QuickActionCards 都 stub 成 testid + 数据属性，让 factory 透传逻辑能够直接 snapshot。

## Bug-hunting

无新发现。ackActive / isConsecutive / isLastMessage 计算逻辑都合理；auto-scroll 只在新
user 消息上触发（正确）；ScrollToBottomButton 的 200px 阈值 + scrollHeight
判可滚动的条件都合理。

## Test plan

- [x] 30/30 OpenClawThread 测试通过
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [ ] CI 绿

## 关联

- Epic #894 Step 3 (#897)
- Step 3 所有文件覆盖后 #897 可 close（5 个已测 + OpenClawThread 本 PR）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [3715f6c2](https://github.com/SerendipityOneInc/ecap-workspace/commit/3715f6c2a66cf3b0219f9d698adcbcaa20079584)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T13:04:12Z

**Message:**
```
test(web): SlackSetupWizard try/finally + ChannelsSection effect deps (#1066 + #1074 part 1) (#1105)

Two non-bug hygiene items from the review follow-up queue. Small PR
intentionally — each item alone is < 10 lines, but they share the
"review follow-up polish" model, so bundling avoids churn.

## 1. SlackSetupWizard spec robustness (#1066)

- Wrap the `process.on('unhandledRejection', ...)` listener in
`try/finally` so the handler is removed even if an `expect()` above
throws. This matches the `try/finally` pattern already in place for the
fake-timer test earlier in the same file.
- Fix the `onUnhandled` signature from `(e: PromiseRejectionEvent |
Error)` to `(reason: unknown)`. Runtime behavior was fine — Node calls
the handler with `(reason, promise)` and the existing `caught.push(e)`
happened to receive `reason` — but the type was misleading to future
readers.

## 2. ChannelsSection `ChannelCard` effect deps (#1074 part 1)

- Add `onPairingExpanded` to the `useEffect` deps array; remove the
`eslint-disable-line react-hooks/exhaustive-deps`.
- Parent re-renders pass a fresh closure each render, but
`autoExpandPairing` only flips true when the channel list changes, so in
the worst case this fires one extra idempotent `setPairing(true)` +
`onPairingExpanded?.()`. Both are no-ops on repeat.
- Benefit: removes a stale-closure risk for any future caller whose
callback identity is less stable than today's `onClearLastAdded`.

### Skipped: #1074 part 2 (spec file split)

Not included. Low-priority maintainability; splitting ~600-line spec
into 3–4 files would risk jscpd duplication drift (mocks/factories
replicated across files). Can revisit if the spec ever becomes painful
to debug.

## Test plan

- [x] `pnpm --filter web test:unit SlackSetupWizard ChannelsSection` —
79/79 pass (30 + 49)
- [x] `pnpm --filter web lint` — clean
- [x] `npx tsc --noEmit` — clean

Closes #1066
Closes #1074

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [54b6a7b8](https://github.com/SerendipityOneInc/ecap-workspace/commit/54b6a7b847321cb1a3ce7497829b45890cabc2f6)

**Author:** peter-srp  
**Date:** 2026-04-20T12:51:03Z

**Message:**
```
fix(web): stop reporting MM connection errors to Sentry (#1103)

## Summary
- Removes `Sentry.logger.error/warn` calls from
`captureMMConnectionFailure` — these bypass `beforeSend` and were still
consuming 10K+ events/user/hour, overwhelming Sentry quota
- Retains breadcrumb-only reporting (free, provides context for
subsequent real errors)
- `beforeSend` filter in `sentry.client.config.ts` kept as safety net
for old cached releases
- Removes now-unused `sanitizeURL` helper and `sanitizeUrl` import

## Context
Sentry issue: https://serendipity-one-inc.sentry.io/issues/7401127622/

Previous attempts (dedup windows → Sentry Logs migration) failed because
`Sentry.logger.*` with `enableLogs: true` still creates issues and
consumes event quota, unlike `beforeSend` which only intercepts
`captureException`/`captureMessage`.

## Test plan
- [x] Unit tests updated and passing (`connectionDedup.unit.spec.ts` — 6
tests)
- [x] Lint passes
- [ ] Verify on staging that the Sentry issue stops receiving new events

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [6202a27b](https://github.com/SerendipityOneInc/ecap-workspace/commit/6202a27b3c2956ca4ac68a208d6d6738c392e044)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T12:49:24Z

**Message:**
```
feat(web): wire dependency-cruiser for import boundaries (A1-PR1, warn mode) (#1098)

## Summary
- Wires **dependency-cruiser** as the engine for W1–W6 import
architecture contracts.
- CI runs in **warning mode** (`WARN_ONLY=1`) — violations print but
don't fail the build.
- A1-PR2 freezes the baseline into an allowlist; A1-PR3 flips the hard
gate.
- Also applies review feedback on the A1 spec merged in #1094.

## Baseline (from this config)
**14 errors + 4 warnings** across the 609 modules / 1645 dependencies
cruised. Hot spots:

| Contract | Count |
|----------|-------|
| W1 (lib pure) | 2 |
| W2 (hooks pure) | 3 |
| W3 (contexts pure) | 5 |
| W4 (components below pages) | 2 |
| W5 (feature isolation, warn-level) | 4 |
| W6 (theme leaf) | 1 |

More than the ~6 grep-based estimate in the spec because
dependency-cruiser also follows relative-path imports and re-exports,
which grep missed.

## Changes

### New files
- `web/.dependency-cruiser.cjs` — W1–W6 rules, proper `\[locale\]` regex
escaping, tsconfig resolver
- `web/scripts/ci-lint/00-run-all.sh` — CI-lint orchestrator (mirrors
`services/claw-interface/scripts/ci-lint/` layout)
- `web/scripts/ci-lint/01-import-boundaries.sh` — dep-cruiser runner
with `WARN_ONLY` switch

### Modified
- `web/package.json` — `lint:imports` / `lint:ci` scripts,
`dependency-cruiser` devDep
- `.github/workflows/code-quality.yml` — new "Import boundaries check
(warn mode, A1-PR1)" step in `web-quality` job
- `docs/superpowers/specs/2026-04-20-web-import-boundaries.md` — applies
review feedback from #1094 (see below)

## #1094 review feedback addressed
1. **W1 extended to forbid `lib → theme`** (Option A per decision).
`seo.ts → brand-assets` becomes a real W1 violation, fixable in A1-PR4+
by moving brand-assets to `src/config/brand/` or `src/lib/brand/`.
2. **`[locale]` regex pitfall** documented in spec's 风险与缓解 section and
applied to W5 patterns in the config (`\\[locale\\]`).
3. **Layer diagram** clarified with explicit `hooks → contexts`
direction annotation.

Non-blocking Codex suggestions (W5 shared-directory definition, grep
reproducibility) deferred to A1-PR2.

## Local verification
- `pnpm lint` (ESLint) — pass
- `pnpm lint:imports` (WARN_ONLY=0) — exit 14, prints all 14 errors + 4
warns
- `WARN_ONLY=1 pnpm lint:ci` — exit 0, prints warnings but doesn't fail
- Config uses escaped `\\[locale\\]` and `tsConfig +
enhancedResolveOptions` — verified dep-cruiser resolves `@/*` aliases
(609 modules cruised vs earlier 2-module dry-run without resolver)

## Test plan
- [ ] CI `code-quality / web-quality` job runs new step, logs baseline
violations, does not fail build
- [ ] Existing ESLint / TS / unit-test / jscpd steps still pass
- [ ] PR-size gate passes (~180 new lines excluding lockfile)
- [ ] Reviewer to validate the W5 regex capture-group approach (`$1`
reference) works as expected vs an explicit feature-name whitelist

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [57aad0ba](https://github.com/SerendipityOneInc/ecap-workspace/commit/57aad0baa3c275600285a5224efeda027163e181)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T12:46:51Z

**Message:**
```
chore(web): remove dead verify step from TelegramSetupWizard (#1096)

## Summary

- Removes the unreachable `verify` step from `TelegramSetupWizard`
(`setStep('verify')` was never called)
- Drops the dead `pairCode`/`pairSaving` state, `handleApprovePairing`
handler, verify UI block, `approveChannelPairing` import
- Drops `verifyTitle` / `verifyDesc` i18n keys across 10 locale files
(unused after the UI block removal)
- Strips the corresponding mock + comment from the wizard's unit spec

The API-level `approveChannelPairing` is retained — it is still used by
the generic pairing flow in `useClawSettings.ts` (surfaced through
`ChannelsSection`'s inline pairing panel). `pairingCodePlaceholder` also
stays for that reason.

Fixes #1064 (part 1 of 2). Part 2 (hardcoded `allow_from: ['*']` while
the `allowlist` policy is still offered) is left open pending a product
decision on whether `allowlist` mode should expose a real whitelist UI
control.

## Test plan

- [x] `pnpm --filter web test:unit TelegramSetupWizard` — 24/24 tests
pass
- [x] `pnpm --filter web lint` — clean
- [x] `npx tsc --noEmit` — clean
- [x] Verified `grep -r "verifyTitle\|verifyDesc"` returns no matches
- [x] Verified wizard happy path tests still cover welcome → create-bot
→ input-token → configuring → complete

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [c70ae11c](https://github.com/SerendipityOneInc/ecap-workspace/commit/c70ae11cbedf41563024e2ccb05730e7fee8404d)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T12:44:35Z

**Message:**
```
docs(web): add dead code / dep health spec (B1) (#1095)

## Summary
- Design spec for dead code + dependency health CI gate in `web/` using
**knip**.
- First PR of the **B track** (parallel to the A track / import
boundaries via dependency-cruiser, spec merged in #1094).
- Pure doc — no code changes, no CI gates added.

## Context
Mirrors the claw-interface CI quality bar (ruff / pyright / 6
import-linter contracts / jscpd / **deptry** / coverage 90%). `web/` has
`@typescript-eslint/no-unused-vars` (single-file) but **no cross-file
dead code / dep health tooling**. This spec fills that gap with a single
tool (knip) covering unused exports / files / deps / devDeps / unlisted
/ duplicates / binaries.

See `docs/superpowers/specs/2026-04-20-web-dead-code.md` for:
- Tool selection rationale (knip over ts-prune + depcheck +
eslint-plugin-unused-imports)
- Baseline from `npx knip` dry-run: ~120 violations (6 files, 6 unused
deps, 3 unused devDeps, 1 unlisted dep, 1 unlisted binary, 39 unused
exports, 58 unused exported types, 6 duplicate exports)
- 2-stage rollout (spec → wire-up + baseline freeze + hard gate in one
PR)
- Category-based cleanup order (duplicates → unused deps → unused files
→ exports by module)
- FP risk areas (Playwright setup files, dynamic imports, pnpm-hoisted
transitives)

## Non-goals
- Does **not** tighten existing thresholds (complexity 25 / max-lines
500 / coverage 55% stay).
- Does **not** tighten `tsconfig` (already strict).
- Does **not** introduce ts-prune / depcheck /
eslint-plugin-unused-imports (knip covers all).

## Test plan
- [x] Markdown renders correctly
- [ ] Reviewer validates knip over three-tool composite rationale
- [ ] Reviewer reviews baseline categorization (duplicate exports in
`src/lib/api/backend.ts` are 1st target — low-risk, high signal)
- [ ] No CI gates triggered (pure doc PR)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [5ef59521](https://github.com/SerendipityOneInc/ecap-workspace/commit/5ef5952169254093fa33a5d9108f8d87d8a880b5)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T12:42:47Z

**Message:**
```
test(web): SubscriptionPanel 全面覆盖 (#896 Step 2 Part B) (#1097)

## Summary

Epic #894 Step 2 Part B — 覆盖 701 LOC 的 SubscriptionPanel.tsx 从 0% → 全分支。
续 #1076（Part A：SuccessClient + OnboardingSuccessClient）。

### 新增 35 个测试

| 分组 | 数量 | 覆盖点 |
|---|---|---|
| Provider + context | 3 | openPanel / closePanel / outside-provider
no-op |
| Close behaviors | 1 | Escape key 关面板 |
| Billing cycle toggle | 1 | yearly 默认 + Monthly 切换传递到 PlanCard |
| handleAction (subscribe/upgrade/switch-cycle) | 6 | !isLoggedIn /
downgrade 分流 / happy path / createOrder fail / postAPI 无 url / 无 uid 静默
|
| handleTopupPurchase (Buy) | 4 | active 付费 / 非 active toast /
!isLoggedIn / createOrder fail |
| openCustomerPortal (Edit billing) | 5 | 无 uid / 成功 /
no-Stripe-customer / 通用错误 / 异常 finally 清 portalLoading |
| handleDowngradeConfirm | 4 | 成功 refresh+toast / 失败保留模态 / 异常 / close
按钮清 target |
| Cancel subscription onConfirm | 4 | 成功关 panel / 失败保留 / 网络异常 / 无 uid 静默
|
| Conditional UI | 6 | pendingDowngrade 横幅 / cancelAtPeriodEnd+Renew /
错误 banner / isActiveSub 切换 / Keep Current Plan toast |
| Contact Support | 1 | openSupportTicket('billing') |

### Harness 要点（踩坑记录）

**Modal stub 必须 stopPropagation**：DowngradeConfirmModal /
CancelConfirmModal 在源码里是 backdrop div (onClick=onClose) 的子节点，真实 modal 用
React portal 绕开；stub 直接内联在同一棵 DOM 里，测试里 fireEvent.click 会冒泡到 backdrop →
关掉整个 panel 让后续断言挂掉。两个 stub 的外层 div 加 `onClick={e =>
e.stopPropagation()}`。

**PlanCard stub**：PlanCard 有独立 spec 覆盖渲染；这里只 stub 成
subscribe/upgrade/downgrade 三个 testid 按钮，专注测 panel 自己的 handleAction
分流逻辑。

## Bug-hunting

无发现需 follow-up 的 bug。Panel 的错误处理合理，三个主要异步 handler (handleAction /
handleTopupPurchase / openCustomerPortal) 都有 try/catch，Sentry capture
正确绑 \`confirm_api_error\`。

## Test plan

- [x] 35/35 SubscriptionPanel 测试
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [ ] CI 绿

## 关联

- Epic #894 Step 2 (#896) — Part A #1076 + Part B 本 PR → #896 可 close
- 续 #1076（Part A post-purchase UX）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [bb826bdb](https://github.com/SerendipityOneInc/ecap-workspace/commit/bb826bdb2a6bdcac5f97d8dc1a49687f225aa4e9)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T11:26:03Z

**Message:**
```
test(web): payment success clients 覆盖 (#896 Step 2 Part A) (#1076)

## Summary

Epic #894 Step 2 的第一部分。覆盖两个 payment-success UI entry point，从 0% → 全分支。
SubscriptionPanel.tsx (701 LOC) 作为 Part B 单独 PR（体量不宜合并）。

### 新增 24 个测试

**SuccessClient** (14 tests, subscription/success/SuccessClient.tsx 298
LOC)
- 参数校验：missing session_id / missing order_id → error UI
- 4 个主状态分支：loading → redirecting、loading → pending refresh、loading →
error、loading → success-render
- 3 条 redirect
触发条件：`order_status='completed'`、`payment_status='paid'`、`payment_status='no_payment_required'`（free
tier）
- subscription vs credits 分支渲染
- 未知 plan tier → 回退 "Pro" + 20,000 credits
- subscription_info 缺失 → 不渲染 details 块
- localStorage ONBOARDING_PROGRESS paymentCompleted 标记
- JSON.parse 坏数据 → 静默 catch，redirect 仍进行

**OnboardingSuccessClient** (10 tests,
onboarding/success/OnboardingSuccessClient.tsx 92 LOC)
- userInfo.uid gate：无 uid → 停在 loading
- missing session_id / missing order_id → error 状态
- success 流：localStorage 标记 + router.push('/chat') 1500ms 后
- processedRef 防重复执行（re-render 不再触发 handlePaymentSuccess）
- `Error` 实例 vs bare object 错误兜底（'Unexpected error'）
- error 状态 "Go to chat" 按钮

### 不在本 PR 范围

- SubscriptionPanel.tsx (701 LOC, 0%) — Part B 单独 PR
- BillingTab.tsx — 已被移除（current: GeneralTab + UsageTab）
- 其他 Step 2 清单文件已有测试（DowngradeConfirmModal / InvoiceHistory /
SharedPlanCard / PaywallContent / CreditsDisplay / stripe API routes）

### Bug-hunting

未发现需要 follow-up issue 的 bug。两份 UI 的状态机合理，localStorage 使用有合理 catch；Stripe
params 在 \`handlePaymentSuccess\` 里处理（已有测试）。

## Test plan

- [x] 14/14 SuccessClient + 10/10 OnboardingSuccessClient 通过
- [x] 3273/3273 全量 unit 测试
- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [ ] CI 绿

## 关联
- Epic #894 Step 2 (#896)
- 续：Part B 即将覆盖 SubscriptionPanel.tsx

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [5d45acf3](https://github.com/SerendipityOneInc/ecap-workspace/commit/5d45acf3e55844f293aa5d5774e06a88ec8110f8)

**Author:** Chris@ZooClaw  
**Date:** 2026-04-20T11:30:52Z

**Message:**
```
docs(web): add import boundaries spec (A1-PR0) (#1094)

## Summary
- Design spec for web/ import architecture constraints (W1–W6).
- First PR of the **A1 track** (import boundaries via
dependency-cruiser).
- Paired B1 track (dead code via knip) will ship in parallel.
- Pure doc — no code changes, no CI gates added.

## Context
Mirrors the claw-interface CI quality bar (ruff / pyright / 6
import-linter contracts / jscpd / deptry / coverage 90%). `web/` already
covers per-file rules (complexity 25 / max-lines 500 / jscpd 5.5% /
Tailwind semantics / asset-size-guard / PR-size gate) but has **zero
tooling for cross-file architectural constraints**. This spec fills that
gap.

See `docs/superpowers/specs/2026-04-20-web-import-boundaries.md` for:
- Layer model (theme/config → lib → hooks/contexts → components → app)
- W1–W6 contracts
- Tool selection rationale (dependency-cruiser over
eslint-plugin-boundaries)
- Initial grep-based baseline (~6 direct violations — W3 already clean)
- 5-PR rollout sequence (spec → wire-up in warn mode → baseline freeze →
hard gate → violation cleanup)

## Non-goals
- Does **not** tighten existing thresholds (complexity 25 / max-lines
500 / coverage 55% stay).
- Does **not** add pre-commit hook (worktree + husky conflict per
existing convention).
- Does **not** introduce sonarjs / type-coverage.

## Test plan
- [x] Markdown renders correctly (GitHub preview)
- [ ] Reviewer validates W1–W6 contract semantics against web/ domain
intent
- [ ] Reviewer confirms dependency-cruiser > eslint-plugin-boundaries
trade-off
- [ ] No CI gates triggered (pure doc PR)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## [16f7f368](https://github.com/SerendipityOneInc/ecap-workspace/commit/16f7f3680bd84e0310f0701160623ada0b1efbf7)

**Author:** bill-srp  
**Date:** 2026-04-20T09:26:34Z

**Message:**
```
fix(ios): Scope code signing settings to correct targets (#1091)

## Summary

Fixes the **Deploy iOS (Staging)** build failure caused by provisioning
profile mismatch ([failed
run](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/24656532866/job/72091350956)).

`update_code_signing_settings` without a `targets` parameter applies to
**all** native targets. The second call (NotificationService extension)
was overwriting the first (main app), leaving the `ZooClaw` target with
the extension's provisioning profile — which lacks Push Notifications
and Sign In with Apple capabilities.

**Fix:** Add `targets:` parameter to scope each call to its intended
target:
- `ZooClaw` → main app profile
- `ZooClawNotificationService` → extension profile

Applied to both `staging` and `release` lanes.

## Test plan

- [ ] Re-run Deploy iOS (Staging) workflow on this branch
- [ ] Verify build completes without provisioning profile errors
- [ ] Verify IPA is produced and uploaded to TestFlight
```

---

## [21f5edeb](https://github.com/SerendipityOneInc/ecap-workspace/commit/21f5edeb8ad8b10117e8edccf2dbba14203cdb8d)

**Author:** peter-srp  
**Date:** 2026-04-20T09:23:49Z

**Message:**
```
feat(web): replace admin session logs with order history (#1092)

## Summary
- Replace the deprecated "日志" (session logs) button with "充值历史" (order
history) in the admin users table
- New `OrderHistoryModal` displays date, type, credits, amount, and
status columns — reuses existing `getOrdersList` API
- Remove deprecated `SessionLogsModal`, `useSessionLogs` hook, and
associated tests

## Test plan
- [ ] Open admin dashboard → Users tab → click "充值历史" button on a user
row
- [ ] Verify modal shows order history table with correct data
- [ ] Verify modal shows empty state for users with no orders
- [ ] Verify loading spinner appears while fetching
- [ ] Verify Escape key closes the modal
- [ ] Verify error toast on API failure
- [ ] `pnpm vitest run tests/unit/app/admin/` — all 43 tests pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [7643e984](https://github.com/SerendipityOneInc/ecap-workspace/commit/7643e9844bf8aa5ad61d7121fd3ec8063f4f936b)

**Author:** Fangmiao-srp  
**Date:** 2026-04-20T08:50:16Z

**Message:**
```
feat(web): add page_view conversion label for Google Ads (#1089)

## What
在 `tracking.ts` 的 `CONVERSION_LABELS` 中填入 page_view 的 Google Ads
conversion label。

## Why
Google Ads 需要 conversion label 才能追踪 page_view 转化。之前 label 为
null，`sendConversion` 直接跳过。

## Changes
- `tracking.ts`: `page_view: null` → `page_view:
'AW-18078707186/LNs9CJnnJp8cEPLbzKxD'`

## Impact
用户触发 `trackPageView` 时，除了发 GA4 事件和 Reddit Pixel，现在会额外发一条 Google Ads
conversion 事件。

---------

Co-authored-by: Muyao Wang <muyao@MuyaodeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

---

## [2748e8c6](https://github.com/SerendipityOneInc/ecap-workspace/commit/2748e8c6bd25c601578864f7261d9ea7ea433bc7)

**Author:** peter-srp  
**Date:** 2026-04-20T08:44:24Z

**Message:**
```
fix(web): require both WS+MM for connection status + anti-jitter debounce (#1090)

## Summary
- **双通道状态判定**：连接状态现在要求 WebSocket（bot 健康探针）和
Mattermost（消息通道）同时连接才显示"已连接"。修复了 MM 连接但 bot 实际不可达时仍显示绿色的问题。
- **非对称防抖**：connected → 断开方向延迟 3 秒（抑制网络抖动闪烁），恢复连接立即生效，error/initializing
等紧急状态立即穿透。
- **统一状态源**：Header badge 和 Input 框现在共享同一个 `useStableConnectionStatus`
hook，不再各自计算。

## Changes
- New: `web/src/hooks/useStableConnectionStatus.ts` — 统一状态计算 + 非对称防抖
hook
- Modified: `web/src/components/ClawPageHeader.tsx` — 使用新 hook 替代内联状态计算
- Modified: `web/src/app/[locale]/chat/GenClawClient.tsx` — Input 状态改用
stableStatus
- Updated: `web/tests/unit/components/ClawPageHeader.unit.spec.ts` —
测试覆盖新语义

## Test plan
- [ ] tsc --noEmit 通过
- [ ] 单元测试通过（8 cases）
- [ ] 验证正常连接时显示绿色"已连接"
- [ ] 断开网络 < 3 秒，右上角状态不变
- [ ] 断开网络 > 3 秒，显示"重新连接"
- [ ] 恢复网络后立即变回绿色
- [ ] Bot 重启时显示"重启中"（橙色）
- [ ] WS 连接但 MM 未连接时显示"重新连接"

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [e7a8a69b](https://github.com/SerendipityOneInc/ecap-workspace/commit/e7a8a69bc9fd01aba25fb734ce7361eddd33882c)

**Author:** nolan-srp  
**Date:** 2026-04-20T08:06:33Z

**Message:**
```
fix(web): filter HEARTBEAT status summaries from chat (#1087)

## Summary
- filter assistant/system chat output that contains HEARTBEAT.md status
summaries
- keep ordinary HEARTBEAT.md mentions and generic status messages
visible
- cover history and streaming message paths for the new filtering
behavior
```

---

## [99018c24](https://github.com/SerendipityOneInc/ecap-workspace/commit/99018c2402f1fb9797b7aa04e1d528bb409932b5)

**Author:** bill-srp  
**Date:** 2026-04-20T07:54:23Z

**Message:**
```
fix(ios): add NotificationService extension provisioning to Fastfile (#1088)

## Summary
- Add provisioning profile setup for `ZooClawNotificationService`
extension in both staging and release Fastlane lanes
- `match` now fetches profiles for both the main app and the
notification extension
- `update_code_signing_settings` and
`export_options.provisioningProfiles` updated to include extension
bundle IDs
- Fixes TestFlight upload failure: `CFBundleIdentifier Collision` caused
by missing extension provisioning

## Test plan
- [ ] Re-run staging build workflow and verify TestFlight upload
succeeds
- [ ] Verify production release lane also works with extension
provisioning
```

---

## [ebfb1676](https://github.com/SerendipityOneInc/ecap-workspace/commit/ebfb1676cc17f72fb101e1f6c45253468dfeaa8c)

**Author:** Leo-srp  
**Date:** 2026-04-20T07:26:08Z

**Message:**
```
feat: proxy_client_id_header + fix Claw Tools toggle (#987)

## Summary

**Backend:**
- `proxy_client_id_header` in SKILL.md metadata for providers needing
OAuth client_id as a header
- Fetch client_id from Nango via `GET
/integrations/{provider}?include=credentials`
- Inject as `Nango-Proxy-{header}` at tool execution time

**Frontend:**
- Fix invisible toggle switch: `bg-input` track + `ring-1 ring-black/5`
knob

Replaces #926 (closed due to merge conflicts from executor extraction)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## [eb1c7333](https://github.com/SerendipityOneInc/ecap-workspace/commit/eb1c733310e9a5f7c3cee153f9dc43111e5228b3)

**Author:** kaka-srp  
**Date:** 2026-04-20T07:16:54Z

**Message:**
```
fix(eca-501): skip new-user wallet probe + retry bootstrap on 502/504 (#1086)

## Context

Linear: [ECA-501](https://linear.app/srpone/issue/ECA-501) —
billing-gateway + claw-interface emit ~1,265 / 24h billing 404 errors in
prod.

Prod log analysis broke this down into three classes:

| Class | 24h count | Source |
|---|---:|---|
| `[BILLING_CLIENT] HTTP 404` on `get_credits` after new-user bootstrap
| **126** | `_resolve_existing_wallets` probe; self-healing; not
user-facing |
| `[BILLING_INIT] Failed to initialize` (409 → `get_user` 404) | ~11 |
409/404 race when bg has partial state from a prior failed bootstrap |
| `[BILLING_INIT] Failed to initialize` (500 from bg bootstrap) | ~27 |
bg's upstream LiteLLM call times out |

This PR targets the first two classes. The 500 class is on the bg side
and will be tracked separately.

## Changes

### 1. Skip `_resolve_existing_wallets` probe for newly-created users

`bootstrap_user` now returns `_newly_created: bool` in the response
dict:
- `True` when bg returns 2xx (customer created this call)
- `False` when bg returns 409 (user existed) — via either the 409 body
or the `get_user` fallback

`_do_billing_init` skips the `get_credits` probe when
`_newly_created=True`. For new users, the probe was guaranteed to 404
because Lago's wallets index hadn't caught up with the just-created
customer (~300ms lag) and was then swallowed — pure log noise. The probe
is still useful for 409 / partial-init recovery, so it stays on that
path.

Expected effect: **~126/24h `BILLING_CLIENT HTTP 404` → ~0**.

### 2. Retry bootstrap POST on 502/504

Bg's distributed lock now makes bootstrap idempotent, so retries are
safe. On gateway-level transients (502/504, typically LiteLLM upstream
hiccup), we retry 2 more times with 0.5s + 1.5s backoff (3 attempts
total).

Explicitly does not retry:
- **500**: application-level bug — amplifying would mask, not help
- **Timeout**: separate concern, deferred

Expected effect: most 502/504-driven `BILLING_INIT Failed` events
self-recover within one request instead of requiring the user to retry.

## Test plan

- [x] 9 new/updated `bootstrap_user` unit tests (200 / 409 /
409-fallback / 502 retry / 504 retry / retry-exhaust / 500 no-retry /
json-parse-error fallback)
- [x] 2 updated `_do_billing_init` unit tests: verifies `get_credits` is
NOT called for new users, IS called for 409 recovery
- [x] `ruff check` + `ruff format` + `pyright` clean
- [x] `python-code-quality / file-length` check (file at exactly 500 /
500)
- [ ] Post-merge: monitor `[BILLING_CLIENT] HTTP 404` count over 48h;
expect drop from ~130/24h to <10/24h

## Notes

- RC-1 (cross-pod concurrent bootstrap creating duplicate teams) is
already mitigated by bg's distributed lock — no claw-interface change
needed.
- RC-3 (bg bootstrap returning 500 when LiteLLM upstream times out) is a
bg-side issue; 502/504 retry here handles the gateway-level variant of
the same root cause.
```

---

## [63bd907c](https://github.com/SerendipityOneInc/ecap-workspace/commit/63bd907c6ee471269dd551243ec787bd2febced9)

**Author:** peter-srp  
**Date:** 2026-04-20T06:35:41Z

**Message:**
```
Feature/fix ws status (#1085)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [ed3339ca](https://github.com/SerendipityOneInc/ecap-workspace/commit/ed3339cac1e71d3a29cf77790ee91b737896d023)

**Author:** bill-srp  
**Date:** 2026-04-20T06:35:00Z

**Message:**
```
ci(ios): Switch staging to TestFlight and add AppsFlyer config (#1084)

## Summary

Switch iOS staging distribution from Pgyer to TestFlight and configure
AppsFlyer keys for production builds.

### Changes
- **Fastlane staging lane**: Ad Hoc signing → App Store signing, Pgyer
upload → TestFlight upload
- **Bundle ID override**: staging builds use `one.srp.zooclaw-staging`
via `xcargs` (project default remains `one.srp.zooclaw`)
- **Build number**: extracted from tag sequence (`ios-v1.2.3-beta.7` →
build `7`), falls back to Xcode project value
- **Secrets.xcconfig**: production gets `APPSFLYER_DEV_KEY` +
`APPSFLYER_APP_ID`, staging gets empty file. Removed unused `SENTRY_DSN`
(hardcoded in app)
- **Cleanup**: removed `fastlane-plugin-pgyer` from Pluginfile, updated
PR comment and Feishu notification text

### Prerequisites (manual)
- [x] Register `one.srp.zooclaw-staging` in App Store Connect
- [x] App Store provisioning profile exists in Match repo
- [x] Firebase staging plist matches staging bundle ID
- [ ] Add `APPSFLYER_DEV_KEY` and `APPSFLYER_APP_ID` to GitHub Secrets
- [ ] Optionally remove `IOS_SENTRY_DSN` secret (no longer used)

## Test plan

- [ ] Trigger staging build via `gh workflow run "Deploy iOS" --ref
feat/ios-workflow -f environment=staging`
- [ ] Verify IPA is uploaded to TestFlight under the staging app
- [ ] Verify build number matches tag sequence
- [ ] Trigger production build and verify AppsFlyer keys are in the IPA

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## [9ac2bc28](https://github.com/SerendipityOneInc/ecap-workspace/commit/9ac2bc2810908d0cfb0f4ac3e1bdf1ecfbd5cf1c)

**Author:** peter-srp  
**Date:** 2026-04-20T06:26:35Z

**Message:**
```
chore(web): remove 29MB of unreferenced static assets (#1082)

Full-repo grep + manifest/CI/config scan confirmed zero references for
all deleted files:

- themes/panda-claw/w.gif (12.7MB) — w.webp is the version in use
- images/nano-banana-2-hero.png (6.1MB) — leftover from initial extract
- themes/panda-claw/logo-panda-claw-full.png (4.1MB) — unused since
theme refactor
- themes/panda-claw/loading.gif (2.9MB) — replaced, never cleaned up
- themes/panda-claw/panda-takeoff.gif (663KB) — unused onboarding
animation
- images/upgrade-mascot.png (647KB) — widget switched to CDN image
- images/assets-demo/ (1.75MB, 5 files) — demo placeholders never wired
up
- images/onboarding-panel.png (259KB) — superseded by redesign
- images/gradient_BG.png (88KB) — unused background

Also removes the now-stale w.gif example from docs/asset-size-guide.md.

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [3e22ace0](https://github.com/SerendipityOneInc/ecap-workspace/commit/3e22ace0049f5694f70e0183c241ed19961d1963)

**Author:** Nemo Feng  
**Date:** 2026-04-20T05:50:33Z

**Message:**
```
fix(agents-manager): force fresh agent list after hire/fire/update (#1044)

## Summary
- Hiring multiple specialists in quick succession (<3 s apart) and
clicking **Start Chat** on the latest success modal appeared to open the
*previous* agent's chat. Route was correct (`/chat?agent_id=<new>`), but
header/avatar/MM channel rendered the prior agent.
- Root cause: `refreshUserAgentsCache` has a 3 s read-throttle that
returned the pre-mutation `_lastResult` and skipped the
`ecap:agents:updated` dispatch. The chat page's identity lookup
(`userAgents.find(a => a.id === agentId)`) then fell through to the
previously-active agent until the next real fetch.
- Fix: add an opt-in `force` flag to `refreshUserAgentsCache` and pass
`force: true` from the mutation path in `useAgentActions.refreshAgents`.
Read-only callers (mount, tab visibility, WS events) still benefit from
the throttle.

## Trade-off
One extra `GET /agents` + catalog warm-up per hire/fire/update (~100–300
ms). Acceptable for correctness; the throttle was designed for burst
*reads*, not post-mutation refreshes.

## Test plan
- [ ] AI Specialists Hub → hire agent A → dismiss success modal → hire
agent B → click **Start Chat** on B's modal → chat opens with B's
avatar/name/MM channel (not A's).
- [ ] Repeat the above 3+ hires in a row; every "Start Chat" opens the
correct agent.
- [ ] Fire a hired agent → list updates immediately (no 3 s staleness).
- [ ] Update an agent with a new version → post-update refresh still
reflects the latest state.
- [ ] Normal mount/tab-switch flow: `userAgents` still debounces bursty
reads (no regression in request volume from passive callers).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Nemo Feng <nemofq@gmail.com>
Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

---

## [bb75eb79](https://github.com/SerendipityOneInc/ecap-workspace/commit/bb75eb79c6911352735f25f1165c5895334e3a7d)

**Author:** sam-srp  
**Date:** 2026-04-20T05:21:04Z

**Message:**
```
fix(claw-interface): correct FastClaw cron.runs endpoint (#1083)

## Summary

- Reports from the schedule page threw a hard `404 Not Found` on every
call to `GET /cron/jobs/{job_id}/runs`, even on freshly created bots.
- Root cause: the client used a nested path
`/runtime/cron/jobs/{job_id}/runs` that **does not exist** on FastClaw.
Verified against `fastclaw/handler/api/v1/bot_cron.go:251` (`CronRuns`)
and the route registration at `fastclaw/cmd/server.go:191`, which
register a **flat** endpoint: `GET
/bots/:id/runtime/cron/runs?id={job_id}&limit={n}`.
- Fix: switch to the flat path with `id` as a query param. Drop
unsupported `offset` / `sortDir` from the outbound request (FastClaw
ignores them anyway); keep them on the Python signature so callers
(route layer, frontend) don't break.

## Test plan

- [x] `pytest tests/unit/test_openclaw_client.py::TestGetCronRuns` — 4/4
pass (2 new assertions: flat URL + `id` query, unsupported params
ignored)
- [x] `ruff check` / `ruff format --check` / `pyright` clean
- [x] `lint-imports` — 8/8 contracts kept
- [x] `deptry` — no dependency issues
- [ ] Manual: open `/schedule` on staging after deploy, verify cron run
history loads without 500 errors

## Notes

- `offset` / `sortDir` are kept on the Python signature only for
compatibility — FastClaw has no pagination/sorting on this endpoint yet.
Frontend's "load more" will return the same first-page until FastClaw
adds it upstream.
- Also already merged into `staging` (via a main-sync merge) and pushed,
so staging deploy picks this up without waiting for main.
```

---

## [46de46b1](https://github.com/SerendipityOneInc/ecap-workspace/commit/46de46b13d6bfc4cdc14d1c42d156a2a81c1447d)

**Author:** peter-srp  
**Date:** 2026-04-20T02:32:33Z

**Message:**
```
fix(web): resolve Sentry errors — JSON-LD, hydration, 401 noise (#1080)

## Summary

Fixes 3 categories of Sentry errors (4 issues total) identified from the
24h health overview:

- **JSON-LD `@context` TypeError** (Sentry
[#7347020751](https://serendipity-one-inc.sentry.io/issues/7347020751/)
/
[#7344333754](https://serendipity-one-inc.sentry.io/issues/7344333754/)):
`getStructuredDataSchemas()` returned a bare JSON array, causing Safari
parsers to access `@context` on the array root (undefined). Now uses the
standard `{ @context, @graph: [...] }` wrapper.

- **Hydration mismatch** (Sentry
[#7238337700](https://serendipity-one-inc.sentry.io/issues/7238337700/)):
`GenClawClient` and `SideNav` read `sessionStorage`/`localStorage` in
`useState` initializers — server rendered with `{}` while client
hydrated with cached data. Moved browser storage reads to `useEffect` so
initial render is identical on both sides.

- **HTTP 401 noise** (Sentry
[#7416524759](https://serendipity-one-inc.sentry.io/issues/7416524759/)):
`httpClientIntegration` captured all 400-599 status codes including 401,
which is expected when tokens expire. Excluded 401 from capture range
(`[400, [402, 599]]`).

## Changes

| File | Change |
|------|--------|
| `web/src/lib/seo.ts` | `@graph` wrapper for JSON-LD structured data |
| `web/src/app/[locale]/chat/GenClawClient.tsx` | `useState` →
`useEffect` for sessionStorage/localStorage |
| `web/src/components/SideNav.tsx` | Same hydration fix for identity
cache + hire CTA state |
| `web/sentry.client.config.ts` | Exclude 401 from
`httpClientIntegration` |

## Test plan

- [ ] Visit homepage (`/en`, `/zh`) in Safari — no console errors,
JSON-LD validates in [Schema.org
validator](https://validator.schema.org/)
- [ ] Visit `/chat` page — no hydration warnings in console;
identity/settings load correctly after mount
- [ ] Trigger a 401 (expired token) — verify it does NOT appear in
Sentry
- [ ] Trigger a 403/500 — verify it DOES appear in Sentry
- [ ] `tsc --noEmit` passes (verified locally)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [6d98c1c3](https://github.com/SerendipityOneInc/ecap-workspace/commit/6d98c1c360e0a658b5b48d689354ad35e272a1dd)

**Author:** peter-srp  
**Date:** 2026-04-20T01:50:26Z

**Message:**
```
fix(web): resolve hydration mismatch from browser storage reads in us… (#1078)

…eState initializers

SideNav and GenClawClient read localStorage/sessionStorage in useState
initializers, producing different values on server ({}) vs client
(cached data). Move storage reads to useEffect so first render matches
SSR output.

Fixes Sentry ECAP-WEBSITE-2 (Hydration Error — 2,876 events / 114
users).

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

---

## [35ebc0da](https://github.com/SerendipityOneInc/ecap-workspace/commit/35ebc0dafc695924ecd0c00ccb04b8b36779cf35)

**Author:** peter-srp  
**Date:** 2026-04-20T01:50:15Z

**Message:**
```
fix(web): use theme-aware text color on CompensationPopup button (#1079)

Replace hardcoded `text-white` with `text-ecap-primary-text` so the "Got
it" button has correct contrast in panda-claw dark mode where the
primary color inverts to a light shade (#e8e8e4).

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

## 2026-04-20


今日无更新

## 2026-04-19

共 25 条 commits

## [0429559b](https://github.com/SerendipityOneInc/ecap-workspace/commit/0429559b22a1ee5c676670898d40e7132cc59449)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T10:28:08Z
- **消息**: test(web): useMattermost reconnect / bot poll / connect 错误分支覆盖 (#1075)

```
## Summary

延续 #1071 merged 的进展，覆盖之前 deferred 的三块源码分支 — **reconnect
scheduling**、**pollBotStatus**、**connect() 错误路径**，不改动产线代码。

### 新增 11 个测试

**reconnect scheduling (5)**
- ws onDisconnect → `scheduleReconnect` → state=`reconnecting`
- intentionalDisconnect 守卫：`disconnect()` 后 ws onDisconnect 不重启
- duplicate timer 守卫：重复 onDisconnect 不重复 scheduleReconnect
- 成功 reconnect → 回到 `connected`、`isReconnectExhausted=false`
- MAX_RECONNECT_ATTEMPTS (5) 耗尽 → `isReconnectExhausted=true` + 错误消息

**pollBotSt
```

## [1695dcdd](https://github.com/SerendipityOneInc/ecap-workspace/commit/1695dcdd9d0aeab9b6b942a3e66da49877646d08)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T09:49:31Z
- **消息**: test(web): useMattermost 补覆盖 reaction/typing/sendMessage/杂项 (#901 Step 7b) (#1071)

```
## Summary

Plan Step 7b——useMattermost hook (839 行) 原 48% 覆盖，~400 行未覆盖。本 PR 针对
reaction events / typing events / sendMessage / loadMoreHistory /
disconnect / autoConnect / clearWaitingForBotReply 这些高 ROI 分支补齐 **23
tests**，推到 **65.6% lines / 68.1% statements**（+20 pp）。

## 23 新 tests / 365 行

| 分组 | tests | 覆盖点 |
|---|---|---|
| reaction events | 8 | reaction_added 追加 / 幂等 / 累积 / reaction_removed
匹配移除 / 单条时删 key / 非匹配 no-op / malformed JSON 吞 / 字段缺失吞 |
| typing events | 4 | bot typing → waiting=
```

## [79ac2db4](https://github.com/SerendipityOneInc/ecap-workspace/commit/79ac2db475084e22e0789b8633df1df6d58ba2ee)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T09:11:53Z
- **消息**: test(web): ChannelsSection 全面覆盖 (#899 Step 5e — 收尾) (#1070)

```
## Summary

Step 5 收尾——Claw Settings 的 \`ChannelsSection\` (869 行) 原先 0 测试。Step 5
最后一块。

子 wizards (Feishu/Telegram/Slack/Discord) 各自独立 spec 已合入；本 PR 将它们 mock 为
stub，聚焦 Section + ChannelCard + StatusBadge + AddChannelModal 的编排 / 渲染 /
状态机。

## 47 tests / 576 行

| 分组 | tests | 覆盖点 |
|---|---|---|
| render gates | 6 | botRunning × redeploying 矩阵 / empty state /
restarting banner / button disabled |
| channel card 渲染 | 4 | platform / account / status / group policy /
emoji fallback |
| StatusBadge |
```

## [2dba8928](https://github.com/SerendipityOneInc/ecap-workspace/commit/2dba8928d8048c9d49d5ae269ad2a45f8f4816d5)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T07:21:43Z
- **消息**: test(web): IntegrationsSection 全面覆盖 (#899 Step 5d) (#1068)

```
## Summary

Step 5 追加——claw-settings \`IntegrationsSection\` (194 行) 原先 0
测试。Third-party OAuth 连接管理 UI：Connected Services 区 + Available
Integrations 区 + toggle / disconnect / connect 交互 + 异步 \`handleConnect\`
流程（window.open popup）。

## 22 tests / 235 行

| 分组 | tests | 覆盖点 |
|---|---|---|
| section 可见性 | 3 | 空状态 / 部分连 / 全连时的 heading 显隐 |
| status badge | 4 | \`connected\`/\`pending\`/\`error\` 各 badge + 未知不渲染
(it.each) |
| 可选字段 | 3 | account_name / error_message / 都空 |
| ConnectedCard 交互 | 6 | di
```

## [da1a18ff](https://github.com/SerendipityOneInc/ecap-workspace/commit/da1a18ff2e050e8d3993964a73479283313e1b96)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T07:01:43Z
- **消息**: chore(web): 收紧 jscpd 阈值 + spec 收尾(web dedup 系列完成) (#1067)

```
## Summary

web 代码重复率系列 13 PR 执行完毕(#1017 基建起,至 #1063 跨 6% 目标)。**最后一步** —— 收紧 jscpd
阈值 + 更新 spec 状态为 done。

## 阈值变更

按 `ceil(obs) + 1.5%` 规则(memory `project_test_dedup_done`,Python dedup
经验沉淀):

| 配置 | 旧阈值 | obs | 新阈值 | buffer |
|------|--------|-----|--------|--------|
| `.jscpd.src.json` | 6% | 3.90% | **5.5%** | 1.6% |
| `.jscpd.tests.json` | 10% | 5.87% | **7.5%** | 1.63% |

阈值下调 **0.5%** 对 src、**2.5%** 对 tests,同时保留 1.6% 缓冲让新代码有生长空间,突破前触发 CI gate
预警。

## 系列最终成果

| 范围 | Before | After | 变化 |
|
```

## [c7b0f59e](https://github.com/SerendipityOneInc/ecap-workspace/commit/c7b0f59e6b8928c175f83b73cb9f433df73c558c)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:54:55Z
- **消息**: test(web): SlackSetupWizard 全面覆盖 (#899 Step 5c) (#1065)

```
## Summary

Step 5 三件套收尾——Claw Settings Slack setup wizard (428 行) 原先 0 测试。接 #1047
Feishu / #1056 Telegram 之后第三个 wizard。

吸收前两个 PR 的 review 教训，spec 一次到位：
- **jest-dom matchers** (`toBeInTheDocument` / `toBeDisabled` /
`not.toBeInTheDocument`)
- **强断言**（验 API payload 精确）
- **无 `.not.toThrow()` 噪音 / 无冗余 waitFor**
- **前瞻处理 unhandled rejection**（源 `handleCopyManifest` 无 `.catch()`）

## 30 tests / 454 行

| 分组 | tests | 覆盖点 |
|---|---|---|
| welcome | 3 | 渲染 / cancel / getStarted |
| create-app | 6 | 
```

## [891d7007](https://github.com/SerendipityOneInc/ecap-workspace/commit/891d70075bf27c286a87ef21f706331ddc955702)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:51:11Z
- **消息**: refactor(web): T2-g useCanvasSession spec 抽 renderSessionAndInit helper(跨 6% 目标) (#1063)

```
## Summary

useCanvasSession spec 17 个 test 重复 6 行 pattern:

```ts
const setMessages = vi.fn()
const { result } = renderHook(() => useCanvasSession({ setMessages }))

await act(async () => {
  await result.current.initializeSession()
})
```

**抽 `renderSessionAndInit()` helper** 返回 `{ setMessages, result
}`;`replace_all` 一次吃 16+ 处 identical block。

**刻意保留** 1 处 `'should return expected shape'` test — 它不走
`initializeSession`,pattern 不匹配,inline 最清晰。

## 重复率变化 🎯

- **tests: 6.13% → 5.87%**(253 → 24
```

## [4f52af7b](https://github.com/SerendipityOneInc/ecap-workspace/commit/4f52af7b22525cb9607fd5949ea0324c7b886ca6)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:42:14Z
- **消息**: test(web): TelegramSetupWizard 全面覆盖 (#899 Step 5b) (#1056)

```
## Summary

Coverage 推进 plan Step 5b——Claw Settings Telegram setup wizard (336 行) 原先
0 测试。接 #1047 FeishuSetupModal 之后的同 wizard 主题。

吸收 PR #1047 多轮 review 教训，spec 一次到位：
- **jest-dom matchers** (`toBeInTheDocument` / `not.toBeInTheDocument`) 
- **强断言**（验 API 被调用 + payload）
- **无 `.not.toThrow()` 噪音** / **无多余 `waitFor`**
- 本组件无 polling / countdown → `waitFor` 仅在 `addClawChannel` Promise
成功/失败后的 DOM 更新用（真 async，合理）

## 24 tests / 328 行

| 分组 | tests | 覆盖点 |
|---|---|---|
| welcome | 3 | 渲染 / cancel 
```

## [dd641f16](https://github.com/SerendipityOneInc/ecap-workspace/commit/dd641f16bfd744dd1c15ef492366ece9628135a6)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:31:27Z
- **消息**: chore: add .nvmrc pinning Node to 24 (#1062)

```
## Summary
Add a one-line `.nvmrc` file at the repo root with `24`. Complements
#1061 (tightening `engines.node` to `>=24 <25`) — the `engines` field
*fails* CI/install when the wrong Node is used; `.nvmrc` lets nvm/fnm
*auto-switch* to the right one before that check runs.

## What changes for contributors
- `nvm use` (no arguments, from the repo root) — auto-switches to Node
24.
- `fnm use` — same; fnm reads `.nvmrc`.
- `direnv` users can add `use node` to a `.envrc` and it follows this
file.

```

## [1c0abf0d](https://github.com/SerendipityOneInc/ecap-workspace/commit/1c0abf0d3bd07040e903ce40e9c2467eeb525b32)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:31:10Z
- **消息**: chore: tighten engines.node to >=24 <25 (#1061)

```
## Summary
Restrict `engines.node` from `>=24` to `>=24 <25`. Node 25 produces
silently-broken local dev state:
- vitest v4 + jsdom 26 + Node 25 combo leaves `localStorage` without a
`.clear` method at test runtime — 114 tests fail locally with
`TypeError: localStorage.clear is not a function` while CI (Node 24)
runs the same tests all green.
- In some vitest invocations on Node 25, the test discovery loop never
completes — 60+ seconds of environment boot followed by "0 tests loaded"
and non-zer
```

## [fdfcbfac](https://github.com/SerendipityOneInc/ecap-workspace/commit/fdfcbfac19611e976530e1c5d36f913b041c7ecc)
- **作者**: tim-srp
- **时间**: 2026-04-18T06:29:49Z
- **消息**: fix(openclaw): correct redeploy allowlist to preserve user data (#1060)

```
## Summary
Fix the pack redeploy allowlist — it was protecting pack templates
(TOOLS.md, AGENTS.md) while exposing user data (SOUL.md, IDENTITY.md,
memory/, media/).

## Changes

**File allowlist (never overwrite):**

| Before | After |
|--------|-------|
| MEMORY.md, USER.md, TOOLS.md, AGENTS.md | MEMORY.md, USER.md, SOUL.md,
IDENTITY.md |

**Copy-if-missing (new mechanism):**
- BOOTSTRAP.md — skip when local file exists (preserve in-progress
onboarding), copy when absent. Agents use its presen
```
- **description**:
  ## Summary
  Fix the pack redeploy allowlist — it was protecting pack templates (TOOLS.md, AGENTS.md) while exposing user data (SOUL.md, IDENTITY.md, memory/, media/).
  
  ## Changes
  
  **File allowlist (never overwrite):**
  
  | Before | After |
  |--------|-------|
  | MEMORY.md, USER.md, TOOLS.md, AGENTS.md | MEMORY.md, USER.md, SOUL.md, IDENTITY.md |
  
  **Copy-if-missing (new mechanism):**
  - BOOTSTRAP.md — skip when local file exists (preserve in-progress onboarding), copy when absent. Agents use its presence to decide whether onboarding is needed.
  
  **Dir allowlist (never overwrite):**
  
  | Before | After |
  |--------|-------|
  | data/, artifacts/, zip/ | data/, artifacts/, zip/, memory/, media/ |
  
  ## Test plan
  - [x] Updated 3 allowlist assertions + added BOOTSTRAP.md copy-if-missing assertions
  - [x] All 79 unit tests pass
  
  🤖 Generated with [Claude Code](https://claude.com/claude-code)

## [4beb5a91](https://github.com/SerendipityOneInc/ecap-workspace/commit/4beb5a91a9bcab6f7df8b425f968cb7ebe1965d6)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:13:29Z
- **消息**: refactor(web): T2-f useCanvasChat spec 抽 renderAgentAndSend helper (#1059)

```
## Summary

useCanvasChat spec 12 个 streaming test 重复 7 行 pattern:

```ts
const params = makeDefaultParams()
params.chatMode = 'agent' as const
const { result } = renderHook(() => useCanvasChat(params))

await act(async () => {
  await result.current.sendMessage('Agent task')
})

const callbacks = mockStartStream.mock.calls[0][1]
```

这是 jscpd 识别的**最大 block**:L291-334 master,被 10+ 处 clone(14 行块 × 2 + 12 行块
× 多),贡献 tests dup 的 ~0.4%。

**抽 `renderAgentAndSend(message)` helper**:
- 内嵌 `makeDefaultP
```

## [0785e4e8](https://github.com/SerendipityOneInc/ecap-workspace/commit/0785e4e855cb7c2f20c380a5f779abb037043577)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:07:36Z
- **消息**: test(web): finish jest-dom migration for components/ (variable-ref form) (#1058)

```
## Summary
- Finish the components/ jest-dom migration started in #1029: 12
variable-reference presence assertions across 6 files, swapped from
`.toBeDefined()` / `.not.toBeNull()` / `.toBeNull()` to the jest-dom
semantic equivalents.
- Pure 1:1 matcher swap — net line change is 0 (12 insertions / 12
deletions).

## Context
#1029 migrated 148 inline-query sites
(`expect(screen.getByX(...)).toBeDefined()`) but intentionally left the
variable-reference form (`const el = getByX(...);
expect(el).toB
```

## [4b194c48](https://github.com/SerendipityOneInc/ecap-workspace/commit/4b194c48a7ca874b14d36d46f01aca9ab7dee46a)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:03:37Z
- **消息**: refactor(web): T2-e useOpenClawChat spec 抽 renderClawChat/renderStreamingChat helper (#1054)

```
## Summary

useOpenClawChat spec 30 个 test 有 2 大重复簇:

1. **send-message flow 样板**(15 处):`mockWsStatus = 'connected'` + `const
{ result } = renderHook(() => useOpenClawChat(getMockWs()))`
2. **streaming test 样板**(8 处):`const { handlers } =
setupWithEventCapture()` + `renderHook(...)` + `const sessionKey =
result.current.sessionKey` + `const chatHandler = handlers[0]`

**抽 2 个 helper 到顶层**:
- `renderClawChat(wsStatus?)` — 设 status + renderHook,default
`'connected'`
- `renderStreamingChat()` — 捕获 o
```

## [77493608](https://github.com/SerendipityOneInc/ecap-workspace/commit/774936080f34250030631b69eebccf3d65bed89f)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T06:02:33Z
- **消息**: refactor(claw-interface): openclaw_client.py → mixin package (1333→max 346) (#1055)

```
## Summary
- Convert 1333-line `openclaw_client.py` into a package with 8 mixin
files (max 346 lines each)
- `OpenClawPlatformClient` class assembled via multiple inheritance in
`__init__.py`
- **Zero caller changes** — all 30+ callers keep using `from
app.services.openclaw_client import get_openclaw_client`
- Only 4 test patch paths updated (logger/SETTINGS/asyncio moved to
mixin modules)

### Mixin files
| File | Lines | Domain |
|------|------:|--------|
| `_base.py` | 97 | HTTP pool, connect
```

## [aa03774c](https://github.com/SerendipityOneInc/ecap-workspace/commit/aa03774cfa5da2a4f0db3e26ee64ff580c51822e)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T05:55:17Z
- **消息**: refactor(web): T2-d upload spec 抽 setupUploadBrowserMocks helper (#1052)

```
## Summary

upload spec 3 个 describe 重复 29 行 identical beforeEach + afterEach 样板:
- `uploadToR2 — behavior tests`(L39-67)
- `onProgress callbacks`(L431-459)
- `uploadToR2 error paths`(L613-641)

`useUploadState` 里还有个 inline test(`'upload function calls
uploadToR2...'`)也用同 17 行 setup。

**抽 `setupUploadBrowserMocks(opts?)` helper 到模块顶层**:
- 构造 fetchSpy + 覆盖 `global.fetch`
- stub `URL.createObjectURL` / `revokeObjectURL`
- `vi.stubGlobal('Image', class {...})` 默认 width=800 height=600,可
overrides
- 
```

## [38117d18](https://github.com/SerendipityOneInc/ecap-workspace/commit/38117d1892769bf98f732ecb7fe33d9169f8ab3b)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T05:54:05Z
- **消息**: test(web): FeishuSetupModal 全面覆盖 (#899 Step 5) (#1047)

```
## Summary

Coverage 推进 plan Step 5——Claw Settings 的 Feishu setup modal (246 行) 原先 0
测试。Step 5 三个 wizards 里最小 / 自包含度最高，先拿下作为热身。

## 24 tests / 365 行 / 覆盖清单

**4 phase 迁移 × 2 种 timer**：

| 分组 | tests | 覆盖点 |
|---|---|---|
| initial render | 2 | loading phase + startFeishuSetup 参数映射 |
| QR phase | 3 | QR SVG value / 5:00 格式 / 0:09 leading-zero |
| startSetup 失败 | 2 | Error 消息 + 非 Error "Failed to start setup"
fallback |
| polling 正常结果 | 6 | success / expired / denied / error+message /
error+fallba
```

## [e6b7c81a](https://github.com/SerendipityOneInc/ecap-workspace/commit/e6b7c81a08ff849c1a0aa980bb917b61ed296a6f)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T05:44:40Z
- **消息**: chore(web): remove dead pnpm block from web/package.json (#1051)

```
## Summary
Delete `web/package.json`'s `pnpm.overrides` +
`pnpm.onlyBuiltDependencies`. pnpm ≥ 8 ignores `pnpm.*` in workspace
child packages — only the root `package.json` block is honored. CI has
been printing two warnings on every install for this reason, and the
block has been dead code since the switch.

## Why this is a behavioral no-op
- **`overrides`** — `{flatted, fast-xml-parser, undici}` is
character-for-character identical to the root's block. Only the root
copy was ever honored.
- *
```

## [48266f6b](https://github.com/SerendipityOneInc/ecap-workspace/commit/48266f6bcee0e75ce78ecaac775e49cf2e85ac60)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T05:42:47Z
- **消息**: refactor(claw-interface): agent_deploy 拆 3 modules — 全 ≤500 (#1015)

```
## Summary

agent_deploy.py(961 行)拆为 3 sibling + 主文件,全部 ≤500:

| 文件 | 行数 |
|---|---:|
| agent_deploy.py | 305 |
| agent_deploy_pack.py | 350 |
| agent_deploy_phases.py | 188 |
| agent_deploy_workspace.py | 177 |

主文件 re-export 全部 moved symbols(noqa:F401),caller 零改动。
测试用 monkeypatch proxy fixture 同步 sub-module bindings,不需要每个 test 加
dual-patch。

pyright 0 errors / 2521 passed / agent_deploy 从 file-length WARNING 消失。
需 size-override。

🤖 Generated with [Claude Code](https://claude.com/claude-code)


```

## [52060f9f](https://github.com/SerendipityOneInc/ecap-workspace/commit/52060f9f6079ba701e097cc776ff3d58aef6803c)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T05:39:53Z
- **消息**: refactor(web): T2-c useLiteLLMApi spec 引入 renderLiteLLMApi helper (#1050)

```
## Summary

useLiteLLMApi spec 21 处 test 重复同样的 9 行 `renderHook(() => useLiteLLMApi({
... 4 fields ... }))` 样板,只有 `sessionId` 有 3 种变化(`null` / `'s1'` /
`'session-1'`),其他字段全默认。

**抽 `renderLiteLLMApi(overrides?: Partial<LiteLLMHookOptions>)`
helper**:
- 默认 `sessionId: null, selectedModel: 'gpt-4', agentName: 'test',
setShowInsufficientCreditsModal: vi.fn()`
- `overrides` 浅覆盖,spread 模式

**3 次 `replace_all` 按 sessionId 值分组吃完 21 处**:
- 17 处 `sessionId: null` → `renderLiteLLMApi()`
- 2 处 `sessionId: '
```

## [77d8365a](https://github.com/SerendipityOneInc/ecap-workspace/commit/77d8365ab86ee2681532ee8d86eecd26dce0014c)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T05:29:35Z
- **消息**: chore(web): pin vitest via pnpm.overrides, drop #1029 runtime workaround (#1049)

```
## Summary
- Root `pnpm.overrides` pins the vitest family (`vitest`,
`@vitest/expect`, `@vitest/runner`, `@vitest/spy`, `@vitest/utils`,
`@vitest/snapshot`) to `^4`. Prior state had `vitest@4.0.18` (web's
direct dep) and `vitest@1.6.1` (transitive) coexisting, which caused the
class of bugs #1029 had to work around.
- Drop the manual `expect.extend(matchers)` from `web/vitest.setup.ts`.
With one-and-only-one vitest in the graph, jest-dom's `/vitest` entry
binds to the right `expect` on its own.

```

## [2065b660](https://github.com/SerendipityOneInc/ecap-workspace/commit/2065b66021b972639bd68f31a4ed9bbcd9105b67)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T04:56:22Z
- **消息**: docs: add asset size guide for designers and engineers (#1048)

```
## 背景

PR #1039 刚合入了 pre-commit 自动压缩 + CI 硬上限拦截的素材大小控制机制。本 PR
补一份面向使用者的指南文档，方便设计师和工程师了解如何启用、日常怎么使用、遇到问题怎么处理。

## 文档位置

`docs/asset-size-guide.md`（顶层，和 `docs/local-dev-guide.md` /
`docs/ci-review-and-merge-queue.md` 同级，kebab-case 沿袭现有命名）。

## 覆盖内容

- 两层防线的职责边界（pre-commit warn-only + CI 硬上限 fail）
- 硬上限阈值表
- 设计师一次性启用：`pnpm install` 在仓库根即可
- 日常 commit 会看到的两种输出（自动压缩成功 / 压不下去 warning）
- **工具坏掉时 commit 会被阻断**（刻意行为，避免 sharp 缺失时静默放过素材）
- 如何从 `.git/asset-backup/` 按时间戳恢复被误优化的原件
- 超阈值时的常规处理建议（squoosh / WebP
```

## [1f5718d8](https://github.com/SerendipityOneInc/ecap-workspace/commit/1f5718d8486f84a5e1d75d44eb6e1b410753ad1a)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T04:45:27Z
- **消息**: feat(ci): block oversized assets with pre-commit hook and CI gate (#1039)

```
## 背景

设计师偶尔把未优化的大图/GIF 直接 commit 进仓库（存量如 `web/public/themes/panda-claw/w.gif`
13M、`nano-banana-2-hero.png` 6M），增加前端 bundle 体积和首屏负担。现有
`scripts/check-pr-size.sh` 主动排除所有二进制文件（职责是行数预算），素材字节数完全不设防。

本 PR 建立两层防线：

1. **本地 pre-commit**：自动用 sharp 无损压缩新增/修改的 PNG/JPG/WebP 并
re-stage，超阈值只警告不阻断 —— 保证设计师工作流顺畅。
2. **CI `asset-size-guard`**：硬上限，压缩后仍超阈值直接 fail PR。

## 设计要点

- **范围**：`web/public/**` + `ios/ZooClaw/ZooClaw/Assets.xcassets/**`（iOS
CLAUDE.md 不动）
- **阈值**：PNG/JPG 500KB · WebP 300KB · GIF 1MB · MP4
```
- **description**:
  ## 背景
  
  设计师偶尔把未优化的大图/GIF 直接 commit 进仓库（存量如 `web/public/themes/panda-claw/w.gif` 13M、`nano-banana-2-hero.png` 6M），增加前端 bundle 体积和首屏负担。现有 `scripts/check-pr-size.sh` 主动排除所有二进制文件（职责是行数预算），素材字节数完全不设防。
  
  本 PR 建立两层防线：
  
  1. **本地 pre-commit**：自动用 sharp 无损压缩新增/修改的 PNG/JPG/WebP 并 re-stage，超阈值只警告不阻断 —— 保证设计师工作流顺畅。
  2. **CI `asset-size-guard`**：硬上限，压缩后仍超阈值直接 fail PR。
  
  ## 设计要点
  
  - **范围**：`web/public/**` + `ios/ZooClaw/ZooClaw/Assets.xcassets/**`（iOS CLAUDE.md 不动）
  - **阈值**：PNG/JPG 500KB · WebP 300KB · GIF 1MB · MP4/MOV 2MB · SVG 100KB
  - **存量豁免**：CI 只检查 `git diff --diff-filter=ACMR origin/main..HEAD` 选出的新增/修改文件，历史超标老素材放过；一旦 modify 就回归新规则
  - **自动 re-stage**：pre-commit 优化工作树文件后会 `git add` 重新入 index（lint-staged 模式），避免 "优化了但 commit 的还是原文件" 的坑
  - **Worktree 兼容**：`git rev-parse --git-dir` 取真实 gitdir，备份写 `<git-dir>/asset-backup/`
  - **Summary job 联动**：`asset-size-guard` 已加入 `code-quality` summary 的 needs + 判定脚本，branch protection 生效
  
  ## 本地验证
  
  | Case | 结果 |
  |---|---|
  | 662KB 可压缩 PNG staged | sharp 压到 206KB 并自动 re-stage，index blob 变更 ✓ |
  | 614KB 随机字节 PNG | sharp 读不通 → warning 不阻断，commit 退出 0 ✓ |
  | 无 staged asset | 脚本静默退出 0 ✓ |
  | YAML 语法 | `yaml.safe_load` 通过 ✓ |
  
  CI 端 fail path 尚未本地验证 —— 本 PR 合并前会在此分支追加一个超大测试文件推一轮，观察 `asset-size-guard` 红叉，确认后 revert。
  
  ## 风险
  
  1. **Sharp 原地优化是破坏性的** — 已 mitigate：先 copy 到 `<git-dir>/asset-backup/<basename>.<sha16>.bak`，optimize 后仅在"更小"时 rename 覆盖
  2. **Rename 噪声**：`--diff-filter=ACMR` 包含 rename；视为 feature（大文件 rename 值得重新审视大小）
  
  ## Test plan
  
  - [x] 本地 `node scripts/check-asset-size.mjs --mode=precommit` 三个 case
  - [x] YAML 语法
  - [ ] CI `asset-size-guard` 在违规文件的 PR 上 fail（见本 PR 后续 commit）
  - [ ] CI `asset-size-guard` 在合规文件的 PR 上 pass
  - [ ] `code-quality` summary 把 asset-size-guard 的结果正确汇总
  
  🤖 Generated with [Claude Code](https://claude.com/claude-code)
- **pr_comments**:
  ---
  **chris-srp** (2026-04-18):
  ## Review 反馈处理（commit 53529a5dc）
  
  感谢两个 auto-reviewer。三个 actionable finding 已解决：
  
  | Finding | 来源 | 处理 |
  |---|---|---|
  | Animated WebP 数据损坏（`w.webp` 147 帧 → sharp 塌成 1 帧） | Codex | `optimize()` 加 `metadata.pages > 1` 检测，命中直接 return null 跳过 |
  | CI 两点 diff → PR 陈旧时 base-only 变更误报 | Claude + Codex | `collectFiles` 改三点 `$base...$head`，对齐 GitHub Files Changed 语义 |
  | 过时 TODO scaffold 注释（第 18–39 行） | Claude | 已删 22 行注释块 |
  
  ### 关于测试覆盖
  
  两个 bot 都 flag "no automated tests for primary behavior" 为 `NEED_HUMAN_REVIEW`，本 PR 不再补测试，理由：
  
  1. **CI 已实证两条路径**：commit 2ca1660 (548B compliant) → `asset-size-guard pass 54s`；commit 4ee76aa (700KB random) → `asset-size-guard fail 41s` + summary 正确 fail。fixtures 已在 eaf7c831 清理。
  2. **核心逻辑简单**：`getThreshold` 是扁平表查找；`isAssetPath` 是前缀+扩展名 && 阈值查找；`parseArgs` 是三参数 switch。可读即正确。
  3. **非关键路径**：脚本失败只影响警告信号，不会损坏代码；sharp 优化被 try/catch 包围，异常写 warn 不抛。
  
  如果后续发现实际业务需要补回归测试（例如三点 diff 在 stale PR 上的行为、animated 检测对边缘格式），单独开 issue 补，不卡本 PR。
  ---
  **chris-srp** (2026-04-18):
  /lgtm

## [091bd65e](https://github.com/SerendipityOneInc/ecap-workspace/commit/091bd65e5916b4e7446f22083dd963276f0991d3)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T04:40:23Z
- **消息**: refactor(web): T2-b useSSEStream spec 引入 runStartStream helper (#1041)

```
## Summary

useSSEStream spec 947 行,18 处重复 ~15 行 startStream 样板(renderHook +
3-callback bag + DEFAULT_PAYLOAD + `await act(() => startStream(...))`)。

**抽 2 个 helper**:
- `makeCallbacks(withCredits?)` — 构造 3-cb 或 4-cb
bag(onInsufficientCredits 可选)
- `runStartStream(opts?)` — `renderHook` + `startStream` 一体,return `{
result, callbacks }`。payload 默认 `{ agentName: 'test-agent', uid:
'user-1', sessionId: 'sess-1', message: 'Hello' }`,hookOptions 默认 `{
sessionId: 'sess-1' }`,都可通过 `opts` 覆盖

**替换方式**(
```

## [1fa0e19d](https://github.com/SerendipityOneInc/ecap-workspace/commit/1fa0e19d910d52f1fcffa3fda8a4ad1aa6c9b0d2)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-18T04:38:54Z
- **消息**: chore(web): eslint 规则拦截 expect(getBy*/findBy*).toBeDefined() (#1037)

```
## Summary

Follow-up to #1035——加规则防复发。

#1035 清除了仓库里 29 处冗余 `expect(getBy*/findBy*).toBeDefined()`。但"冗余 +
易复制"的模板一旦存在就会持续传染（本仓库同模式跨 3 PR、3 个文件、半年时间）。加 ESLint 规则在 CI
层硬阻断，让下一个开发者复制粘贴时秒报错。

## 规则

`tests/**/*.{ts,tsx,js,jsx}` override block 下 `no-restricted-syntax` 新增
2 条 selector：

| Selector | 匹配 |
|---|---|
| sync | `expect(getByX(...)).toBeDefined()` |
| async | `expect(await findByX(...)).toBeDefined()` |

前缀 `getBy / findBy / getAllBy / findAllBy` 精确命中 RTL 查询 API，不误伤：
- `querySelector(...)`
```


## 2026-04-18


共 60 条 commits

- **[65c9934](https://github.com/SerendipityOneInc/ecap-workspace/commit/65c99342e5c02eea2b65c5cb72491152e344401b)** `2026-04-17` — test(web): adopt jest-dom + migrate components/ presence assertions (#1029)  
  作者: Chris@ZooClaw

- **[fd58a68](https://github.com/SerendipityOneInc/ecap-workspace/commit/fd58a687881adb3aadaf83548eb5776e04831346)** `2026-04-17` — refactor(web): T2-a-2 globalBridge helper 再 7 处 + 回应 #1036 review (#1040)  
  作者: Chris@ZooClaw

- **[eb0259b](https://github.com/SerendipityOneInc/ecap-workspace/commit/eb0259bb39857af67fbc972acdbc3806efca7386)** `2026-04-17` — feat(web): migrate tracking to gtag and add page_view event (#1033)  
  作者: Fangmiao-srp

- **[9e6b9b2](https://github.com/SerendipityOneInc/ecap-workspace/commit/9e6b9b2b3bccd256c8b97542e5cad091b8f77989)** `2026-04-17` — refactor(web): T2-a-1 globalBridge spec 引入 setupBridge helper (15/25 处) (#1036)  
  作者: Chris@ZooClaw

- **[dfb3a52](https://github.com/SerendipityOneInc/ecap-workspace/commit/dfb3a52b3214339eaa2c13c4d284de8688eb725c)** `2026-04-17` — test(web): 清除 29 处冗余 expect(getBy*/findBy*).toBeDefined() (#1035)  
  作者: Chris@ZooClaw

- **[2d63ca0](https://github.com/SerendipityOneInc/ecap-workspace/commit/2d63ca087f8d8ce43a6109a6117747d908607db5)** `2026-04-17` — test(web): T1 follow-up 回应 PR #1030 review 3 条 (#1034)  
  作者: Chris@ZooClaw

- **[3f97ffc](https://github.com/SerendipityOneInc/ecap-workspace/commit/3f97ffcc2fbd29194711eb5975a7aebf70995460)** `2026-04-17` — test(web): UserCard + UserMenu 全面覆盖 + 9 处 testid 契约 (#1031)  
  作者: Chris@ZooClaw

- **[89ffd2a](https://github.com/SerendipityOneInc/ecap-workspace/commit/89ffd2a212e848b9a9ed65f3a4e48b7971df8199)** `2026-04-17` — refactor(web): T1 合并 auth manager 两个 spec 去 89 行 clone (#1030)  
  作者: Chris@ZooClaw

- **[1135458](https://github.com/SerendipityOneInc/ecap-workspace/commit/1135458af1cb6d4ae349a45d83b0954e1f2e5402)** `2026-04-17` — refactor(web): S4 presigned factory + models size 常量(测试先行) (#1027)  
  作者: Chris@ZooClaw

- **[20dd1cc](https://github.com/SerendipityOneInc/ecap-workspace/commit/20dd1cc9cb252b9dceb69efeec5557470ad7ff87)** `2026-04-17` — test(e2e): add agent hire/fire lifecycle E2E tests (#998)  
  作者: tim-srp

- **[57d2cb1](https://github.com/SerendipityOneInc/ecap-workspace/commit/57d2cb1f4bdf90a22423bc8e9aa713f5d68c3cce)** `2026-04-17` — fix(web): 价格展示统一向上取整（ceil 替代 round） (#1026)  
  作者: vincent-srp

- **[a313cba](https://github.com/SerendipityOneInc/ecap-workspace/commit/a313cba994a0ea3fea95f0eb9f1b42d63663907a)** `2026-04-17` — test(web): UserAvatar 全面覆盖 + 5 处 testid 契约 (#1025)  
  作者: Chris@ZooClaw

- **[4b83633](https://github.com/SerendipityOneInc/ecap-workspace/commit/4b836332cc4d7832823811ac2056cdb2257c6bd8)** `2026-04-17` — refactor(web): 抽 authHeaders + agents install/uninstall factory (#894 Step S2+S3) (#1024)  
  作者: Chris@ZooClaw

- **[b3bc602](https://github.com/SerendipityOneInc/ecap-workspace/commit/b3bc602b85dab1f55bdc56952f0fbcdf29b1e813)** `2026-04-17` — chore(web): 删除 Profile 页 5 个 orphan tabs + 死代码测试 (#1021)  
  作者: Chris@ZooClaw

- **[f20e411](https://github.com/SerendipityOneInc/ecap-workspace/commit/f20e411471d10b365b07c683279469ce38a558a3)** `2026-04-17` — fix(web): restore base64 markdown image rendering (#1023)  
  作者: nolan-srp

- **[ffbb0fb](https://github.com/SerendipityOneInc/ecap-workspace/commit/ffbb0fb649ebc5f8c5a4fd9a7300e0fc28c5e1fc)** `2026-04-17` — fix: default groupPolicy to 'open' in platform setup wizards (#1022)  
  作者: kaka-srp

- **[528e12e](https://github.com/SerendipityOneInc/ecap-workspace/commit/528e12e9c187252f40e75b00cc65c2866c94b8b5)** `2026-04-17` — refactor(web): release action factory + jscpd 本地脚本 (#1017)  
  作者: Chris@ZooClaw

- **[0d9d327](https://github.com/SerendipityOneInc/ecap-workspace/commit/0d9d3270041de00149214fc2524d592a09184f9b)** `2026-04-17` — fix(web): 版本升级弹窗暗色模式适配 (#1016)  
  作者: lynn Zhuang

- **[5bf60d4](https://github.com/SerendipityOneInc/ecap-workspace/commit/5bf60d4b8588b3bc054820ed87be0ce1f0070251)** `2026-04-17` — fix(web): 侧边栏 Hire AI Specialists 改名为 AI Specialists Hub (#1018)  
  作者: lynn Zhuang

- **[795f67a](https://github.com/SerendipityOneInc/ecap-workspace/commit/795f67af64e3df60a20c0d852b13e6629e144cd5)** `2026-04-17` — test(web): Profile GeneralTab 全面覆盖 (#902 Step 8b) (#1013)  
  作者: Chris@ZooClaw

- **[a3163ce](https://github.com/SerendipityOneInc/ecap-workspace/commit/a3163cecd3ba0038f8cc7b987f07566145fa8004)** `2026-04-17` — fix(claw-interface): use manifest versions for pack updates (#1014)  
  作者: nolan-srp

- **[fb4afdd](https://github.com/SerendipityOneInc/ecap-workspace/commit/fb4afdd3fdbbc6ad49664e6c4f38d6a50ef3274b)** `2026-04-17` — fix(web): restore DiaryCards to Settings General tab (#1000)  
  作者: tim-srp

- **[3143f02](https://github.com/SerendipityOneInc/ecap-workspace/commit/3143f023d6af65e0e76c8e3cdf35d825bc0b9436)** `2026-04-17` — feat(ios): Integrate Pulse for in-app network debugging (#994)  
  作者: bill-srp

- **[cdd223c](https://github.com/SerendipityOneInc/ecap-workspace/commit/cdd223c9783b6a0e197e2b7921ba33c5afc78bb1)** `2026-04-17` — test(claw-interface): 合并 current_user dict 到 make_current_user helper (#1010)  
  作者: Chris@ZooClaw

- **[b55c2d9](https://github.com/SerendipityOneInc/ecap-workspace/commit/b55c2d9fe7068d616b95a7575c179f9703521b06)** `2026-04-17` — refactor(claw-interface): openclaw_settings → package 结构 (#1005)  
  作者: Chris@ZooClaw

- **[a8ab422](https://github.com/SerendipityOneInc/ecap-workspace/commit/a8ab4223fda195d15d0cbd9a90b4a28a552e9f1c)** `2026-04-17` — test(web): GenClawInput 全面覆盖 (#898 Step 4a) (#1012)  
  作者: Chris@ZooClaw

- **[169ee5f](https://github.com/SerendipityOneInc/ecap-workspace/commit/169ee5f123dee90c0f1deab8963b59c4d2458faf)** `2026-04-17` — docs(web): CLAUDE.md fake-timers + waitFor mix 规则 (#1011)  
  作者: Chris@ZooClaw

- **[3691944](https://github.com/SerendipityOneInc/ecap-workspace/commit/36919443a05a00a034b9634281d0068eba7ff681)** `2026-04-17` — chore(web): bump coverage floor 35% → 55% lines (#1009)  
  作者: Chris@ZooClaw

- **[112bd87](https://github.com/SerendipityOneInc/ecap-workspace/commit/112bd8760fc95aae111ab90665758396633c098d)** `2026-04-17` — fix(web): artifact preview not switching when clicking different file (#1006)  
  作者: peter-srp

- **[7fa1e88](https://github.com/SerendipityOneInc/ecap-workspace/commit/7fa1e8838ae1dd38e10fcc14188a3338d9505e36)** `2026-04-17` — test(web): Profile UserSettings + Claw Settings 小组件覆盖 (#899/#902 Step 8a/5a) (#1008)  
  作者: Chris@ZooClaw

- **[02953e8](https://github.com/SerendipityOneInc/ecap-workspace/commit/02953e84d05402395953683f44dac7fbeeaf0ae6)** `2026-04-17` — refactor(auth): remove guest account registration for unregistered visitors (#1004)  
  作者: peter-srp

- **[fd3a794](https://github.com/SerendipityOneInc/ecap-workspace/commit/fd3a7949062852985df98a5c96d6aa625b33b3fb)** `2026-04-17` — test(claw-interface): 合并 _mock_response 到 _http_helpers.py (#1007)  
  作者: Chris@ZooClaw

- **[995ef31](https://github.com/SerendipityOneInc/ecap-workspace/commit/995ef319340c3f635a2fb53c68aff1a366720975)** `2026-04-17` — test(claw-interface): orders_repo + integration_repo 原子操作迁移到 BDD + fal_video rename (#1002)  
  作者: Chris@ZooClaw

- **[20f58e5](https://github.com/SerendipityOneInc/ecap-workspace/commit/20f58e5c98e6b31a221b39a361d88c44629160da)** `2026-04-17` — test(web): Mattermost websocket service + Provider 覆盖 (#901 Step 7a) (#1003)  
  作者: Chris@ZooClaw

- **[224d997](https://github.com/SerendipityOneInc/ecap-workspace/commit/224d9971bd554ff56ed067c1714e72ba6f439dd4)** `2026-04-17` — test(web): ArtifactPreview 组件覆盖 (#904 Step 10c 收尾) (#996)  
  作者: Chris@ZooClaw

- **[86bfb3a](https://github.com/SerendipityOneInc/ecap-workspace/commit/86bfb3ac9089ab32fa80a2e6d74eb7c104f20757)** `2026-04-17` — test(claw-interface): user_repo 原子操作测试迁移到 BDD (真 mongo) (#999)  
  作者: Chris@ZooClaw

- **[c585f79](https://github.com/SerendipityOneInc/ecap-workspace/commit/c585f79851d52da480e07bff8ec2724a34752a8b)** `2026-04-17` — refactor(claw-interface): agents 拆透 — 6 sub-modules + 删 ALLOWLIST (5/10) (#993)  
  作者: Chris@ZooClaw

- **[013de5e](https://github.com/SerendipityOneInc/ecap-workspace/commit/013de5ec9f9b3c24e70e01543c8a50d5c4ace2ce)** `2026-04-17` — test(claw-interface): 合并 OpenClaw 域 builder 到 _openclaw_helpers.py (#997)  
  作者: Chris@ZooClaw

- **[0938cd1](https://github.com/SerendipityOneInc/ecap-workspace/commit/0938cd129fe1c77c698f0dcb92910b78a30c3499)** `2026-04-17` — test(web): MarkdownContent DOMPurify/交互 + useResizable 覆盖 (#904 Step 10b) (#992)  
  作者: Chris@ZooClaw

- **[80a1524](https://github.com/SerendipityOneInc/ecap-workspace/commit/80a152462ddd6e07f99e2f5fda4564fcf0846a64)** `2026-04-17` — test(claw-interface): 清理测试孤儿件 + 顶层 unit 测试移位 (#995)  
  作者: Chris@ZooClaw

- **[5b9aa45](https://github.com/SerendipityOneInc/ecap-workspace/commit/5b9aa45644ad6b5a6f80b3e1bd3c69d1f04fe204)** `2026-04-17` — fix(chat): deduplicate attachments already rendered as artifact cards (#991)  
  作者: peter-srp

- **[f8a90a7](https://github.com/SerendipityOneInc/ecap-workspace/commit/f8a90a71410a199de811c4d65e9402057202b938)** `2026-04-17` — refactor(claw-interface): 收紧 ruff 全局 ignore (B008/PLR0911/PLW0603/PLC0415) (#990)  
  作者: Chris@ZooClaw

- **[66f4305](https://github.com/SerendipityOneInc/ecap-workspace/commit/66f4305871a68a6610bf753b3f1825415e70ad3e)** `2026-04-17` — test(web): renderMarkdownToHtml + artifacts/types 纯函数覆盖 (#904 Step 10a) (#989)  
  作者: Chris@ZooClaw

- **[f462b95](https://github.com/SerendipityOneInc/ecap-workspace/commit/f462b954bf3d65519ca894bb379979acd82c22f8)** `2026-04-17` — refactor(claw-interface): openclaw_integrations → package 结构 (#986)  
  作者: Chris@ZooClaw

- **[d547949](https://github.com/SerendipityOneInc/ecap-workspace/commit/d547949d74629754357c355e174e75da3b4dc584)** `2026-04-17` — fix(claw-interface): clean up legacy skills on agent redeploy (#985)  
  作者: nolan-srp

- **[983051b](https://github.com/SerendipityOneInc/ecap-workspace/commit/983051b15d0841cda85c03ba96fdd3fb891311f7)** `2026-04-17` — refactor(claw-interface): app/ 启用 PLR2004 — HTTPStatus + 业务常量 (#984)  
  作者: Chris@ZooClaw

- **[5f9cad9](https://github.com/SerendipityOneInc/ecap-workspace/commit/5f9cad9241716d7dafffed63dbe20fb63a76faa7)** `2026-04-17` — test(web): LoginForm 单元覆盖 (#900 Step 6b, security-heavy) (#974)  
  作者: Chris@ZooClaw

- **[168bcca](https://github.com/SerendipityOneInc/ecap-workspace/commit/168bccaa213a5dbbd1d96e20e606a69f4f7535bf)** `2026-04-17` — refactor(claw-interface): 拆出 openclaw_agents 的 catalog 与 operation tracking (4/10) (#980)  
  作者: Chris@ZooClaw

- **[2a3cf4f](https://github.com/SerendipityOneInc/ecap-workspace/commit/2a3cf4f780111370b6cefe172d8d6d280e65f444)** `2026-04-17` — feat: batch credits grant + compensation popup (#875)  
  作者: peter-srp

- **[fb89697](https://github.com/SerendipityOneInc/ecap-workspace/commit/fb8969754d3390df05f9c2dcd9ad41b0e1b70561)** `2026-04-17` — chore(claw-interface): 收敛 ruff ignore — 摘 SIM102/108/B905，SIM117 per-file (#982)  
  作者: Chris@ZooClaw

- **[f2d9136](https://github.com/SerendipityOneInc/ecap-workspace/commit/f2d913637a118d238e6d79904b24d2027883eabd)** `2026-04-17` — test(web): lib/auth/manager 补 9 条分支覆盖 (#900 Step 6c) (#975)  
  作者: Chris@ZooClaw

- **[e40e618](https://github.com/SerendipityOneInc/ecap-workspace/commit/e40e61872ca7f8c908ff6afe6f0f0b82cce78153)** `2026-04-17` — test(web): AuthProvider/LoginModal/LoginCheckProvider 覆盖 (#900 Step 6a) (#972)  
  作者: Chris@ZooClaw

- **[73fa5c3](https://github.com/SerendipityOneInc/ecap-workspace/commit/73fa5c3e11497489907751d6298b2261cb93bea0)** `2026-04-17` — refactor(claw-interface): 抽 openclaw_integrations 的 executor 到 routes sibling (3/10) (#971)  
  作者: Chris@ZooClaw

- **[34aabe6](https://github.com/SerendipityOneInc/ecap-workspace/commit/34aabe69a38d9a362d4042e5f0e955f0372e7e04)** `2026-04-17` — refactor(claw-interface): openclaw_settings 拆透 — 删原文件,达 ≤500 (2/10) (#973)  
  作者: Chris@ZooClaw

- **[5a7b1a4](https://github.com/SerendipityOneInc/ecap-workspace/commit/5a7b1a4e4f515f530950ff54bd940844d83a53f7)** `2026-04-17` — test(web): #894 hook PR review follow-ups (#962 + #968) (#979)  
  作者: Chris@ZooClaw

- **[a75df1f](https://github.com/SerendipityOneInc/ecap-workspace/commit/a75df1f4fa220fb19252bb9dfcf753d0c04fb8a4)** `2026-04-17` — fix(sentry): drop MM connection lost events + fix rate-limit fingerprint (#978)  
  作者: peter-srp

- **[d745987](https://github.com/SerendipityOneInc/ecap-workspace/commit/d745987684cd6db922a6498935036cbf70a7d56c)** `2026-04-17` — fix(eca-464): only show upgrade banner when current version is older (#977)  
  作者: kaka-srp

- **[b44157c](https://github.com/SerendipityOneInc/ecap-workspace/commit/b44157ce876733c6708383ace4f7a8533f6779da)** `2026-04-17` — chore(ci): remove dormant nango-deploy.yml workflow (#976)  
  作者: Leo-srp

- **[626e03c](https://github.com/SerendipityOneInc/ecap-workspace/commit/626e03ca54de58101e9b3c5cfb8f12dcc9ecda2e)** `2026-04-17` — feat(ios): Stream bot replies via post_edited, handle reactions, improve connection resilience (#922)  
  作者: bill-srp

- **[95e6e9c](https://github.com/SerendipityOneInc/ecap-workspace/commit/95e6e9c0b9781cba7b89bc53aa4f29f5cd5e6157)** `2026-04-17` — fix(sentry): eliminate MM connection 93K event storm — infinite loop + Logs migration (#944)  
  作者: peter-srp

## 2026-04-17

共 93 条 commits

## `125444c6` refactor(claw-interface): 拆分 openclaw_settings — Feishu / multi-agent / image-version (1/10) (#969)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:45:28Z
- **链接**: [125444c6](https://github.com/SerendipityOneInc/ecap-workspace/commit/125444c6acef198d5496d1426caec92944e365a4)

## `88b24c35` test(web): useSubagentChat hook 覆盖 (#894 final chat hook) (#970)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:44:04Z
- **链接**: [88b24c35](https://github.com/SerendipityOneInc/ecap-workspace/commit/88b24c35bf29b54d9956fd17651adfa6dcd18cb7)

## `72827d98` test(web): useSubagentSessions hook 覆盖 (#894 additional) (#968)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:43:33Z
- **链接**: [72827d98](https://github.com/SerendipityOneInc/ecap-workspace/commit/72827d98868ad90c2125d52022eb3ab6eb172147)

## `565ac323` test(web): useProfileGreeting hook 覆盖 (#894 additional) (#966)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:39:43Z
- **链接**: [565ac323](https://github.com/SerendipityOneInc/ecap-workspace/commit/565ac323562f94eb57936525d385c7cccb5439f1)

## `ec079fbf` test(web): useUserAgents hook + refreshUserAgentsCache 覆盖 (#894 additional) (#962)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:37:55Z
- **链接**: [ec079fbf](https://github.com/SerendipityOneInc/ecap-workspace/commit/ec079fbfe50649a8774ce1f3996efd819905c810)

## `a721d6f1` test(web): useIntegrations hook 覆盖 (#894 additional) (#959)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:35:44Z
- **链接**: [a721d6f1](https://github.com/SerendipityOneInc/ecap-workspace/commit/a721d6f1c7bf38b6466901f57ecf91258c420302)

## `ccb2452c` refactor(orders): 下沉 resolve+validate 到 OrderCreateRequest (Pydantic model_validator) (#957)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:35:26Z
- **链接**: [ccb2452c](https://github.com/SerendipityOneInc/ecap-workspace/commit/ccb2452c694ed0318a8699903e819eba4dcc4a08)

## `23fcc0c6` test(web): useClawSettings hook 覆盖 (#894 largest remaining hook, 372 LoC) (#964)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:38:55Z
- **链接**: [23fcc0c6](https://github.com/SerendipityOneInc/ecap-workspace/commit/23fcc0c622e79dc45cde13a7300d7eac0ee4029a)

## `d0d78bc0` refactor(ci): merge_group 下启用 paths-filter,按 diff 跳过无关 pipeline (#967)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:32:27Z
- **链接**: [d0d78bc0](https://github.com/SerendipityOneInc/ecap-workspace/commit/d0d78bc026de0ffd94fba939845c10efe82b5160)

## `e4cd3910` docs(claw-interface): Python 超长文件拆分方案 spec (0/10) (#965)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:06:03Z
- **链接**: [e4cd3910](https://github.com/SerendipityOneInc/ecap-workspace/commit/e4cd391045f633915afc8323b92724cbcc04d01e)

## `93930886` test(web): address PR #949 + #955 review follow-ups (#958)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T15:45:48Z
- **链接**: [93930886](https://github.com/SerendipityOneInc/ecap-workspace/commit/93930886ba05ecb10482b14efd683d2c9ebce6f2)

## `2c3edac8` fix(ci): claude-review 在 merge_group 下 emit status 解锁 queue (#963)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T15:45:13Z
- **链接**: [2c3edac8](https://github.com/SerendipityOneInc/ecap-workspace/commit/2c3edac893c87b4eba86037b0fb34ca090ed541c)

## `be82a7b7` fix(ci): pr-size-check 跳过无关 label 事件 (#961)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T15:42:41Z
- **链接**: [be82a7b7](https://github.com/SerendipityOneInc/ecap-workspace/commit/be82a7b7c3434b3b91ff4e9a762c5d2122c81f07)

## `12d177d1` feat(ci): /lgtm 评论触发 author self-approve (AI-first workflow) (#956)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T15:02:01Z
- **链接**: [12d177d1](https://github.com/SerendipityOneInc/ecap-workspace/commit/12d177d1b15dfcc4b90f1dcc1bc4f630a471579b)

## `2b0b5910` test(web): 4 small hooks 覆盖 (useIsAdmin / useRequireChat / useVersionCheck / useOfficialAgentCatalog) (#949)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T14:46:02Z
- **链接**: [2b0b5910](https://github.com/SerendipityOneInc/ecap-workspace/commit/2b0b5910e86d8af2b5a08cb283585a723148a230)

## `5d426b41` test(web): useAgentActions hook 覆盖 (#894 additional) (#955)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T14:45:35Z
- **链接**: [5d426b41](https://github.com/SerendipityOneInc/ecap-workspace/commit/5d426b4158dfde14ca9a291c2ecf8baf0c9d96be)

## `134d69a7` test(web): useAgentSettings hook 覆盖 (#894 additional) (#954)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T14:44:50Z
- **链接**: [134d69a7](https://github.com/SerendipityOneInc/ecap-workspace/commit/134d69a758e3a80cf8c428825bd586d55e5a590d)

## `408f3bf5` refactor(orders): 拆分 create_order 降复杂度 (allowlist 7→6) (#953)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T14:31:28Z
- **链接**: [408f3bf5](https://github.com/SerendipityOneInc/ecap-workspace/commit/408f3bf50db3feb8e3bfce323c95752824024b26)

## `d46a106b` ci: 给 required workflow 加 merge_group trigger (merge queue PR 1/2) (#952)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T14:22:34Z
- **链接**: [d46a106b](https://github.com/SerendipityOneInc/ecap-workspace/commit/d46a106ba4af50a32cf6f34125fe082e03a0eae1)

## `dc361489` refactor(billing): 拆分 _do_billing_init 降复杂度 (allowlist 8→7) (#948)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T14:19:02Z
- **链接**: [dc361489](https://github.com/SerendipityOneInc/ecap-workspace/commit/dc361489962bcd02160222527c2de01d66596fcd)

## `d8f78d08` test(web): remove vacuous assertion in compact-mode test (follow-up to #946) (#947)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:58:31Z
- **链接**: [d8f78d08](https://github.com/SerendipityOneInc/ecap-workspace/commit/d8f78d08c138108ec624f1e62891b59307bb6dbc)

## `d894978d` test(web): OpenClawAssistantMessage 覆盖 (#897 Part 5) (#946)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:52:28Z
- **链接**: [d894978d](https://github.com/SerendipityOneInc/ecap-workspace/commit/d894978d658cabca505e70f2a56b50b5c86b3fed)

## `dcd724bf` test(web): useMattermostIntegration hook 覆盖 (#897 Part 4) (#945)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:43:26Z
- **链接**: [dcd724bf](https://github.com/SerendipityOneInc/ecap-workspace/commit/dcd724bff082a6184e48954dfd2cb594cde0e16b)

## `5d9ceb65` test(web): add Date.now() fallback test for missing timestamp (follow-up to #941) (#942)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:25:49Z
- **链接**: [5d9ceb65](https://github.com/SerendipityOneInc/ecap-workspace/commit/5d9ceb65544a6a2bccc1d620fd6782a577522ac2)

## `3e81b956` feat(errors): Phases 4+5 — stripe services migration + C3 contract tighten (closes #873) (#943)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:25:09Z
- **链接**: [3e81b956](https://github.com/SerendipityOneInc/ecap-workspace/commit/3e81b9560038f77e4a0dc8114b53a488efc499f6)

## `7621631b` test(web): useOpenClawRuntime hook 覆盖 (#897 Part 3) (#941)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:13:12Z
- **链接**: [7621631b](https://github.com/SerendipityOneInc/ecap-workspace/commit/7621631b41dcfcf843d2ed3f05e4fe52e4e3cd02)

## `24681461` refactor(scheduler): cleanup_stale_jobs 改走 session_job_repo + 收尾 scheduler C1 (PR 3/6) (#939)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:12:09Z
- **链接**: [24681461](https://github.com/SerendipityOneInc/ecap-workspace/commit/24681461635bf2fd3653acc9822b85dc1fb2f9b1)

## `adc311ca` fix(worktree): enable pre-commit hooks inside worktrees (#940)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:08:49Z
- **链接**: [adc311ca](https://github.com/SerendipityOneInc/ecap-workspace/commit/adc311cacbd446385df110d673cf30b3aa7fafa0)

## `75bd370b` test(web): drop redundant second rerender in useArtifactsSidebar streaming test (follow-up to #933) (#938)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:03:16Z
- **链接**: [75bd370b](https://github.com/SerendipityOneInc/ecap-workspace/commit/75bd370bb3536e8da4edabd684c26d2de6934bf9)

## `0291d6df` feat(importlinter): 新增 C5 (HTTP 工具) + C6 (skills/tasks 叶) 合约 (PR 6/6) (#937)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:02:09Z
- **链接**: [0291d6df](https://github.com/SerendipityOneInc/ecap-workspace/commit/0291d6df5c165b3ebe69caa66684d02411831e9b)

## `ad716290` test(web): useArtifactsSidebar hook 覆盖 (#897 Part 2) (#933)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:57:55Z
- **链接**: [ad716290](https://github.com/SerendipityOneInc/ecap-workspace/commit/ad716290dfd1eb4e91bdbe2b851aaa4e259560e2)

## `b7e3ca38` test(web): assert isCopied state transition after copy click (follow-up to #928) (#931)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:57:23Z
- **链接**: [b7e3ca38](https://github.com/SerendipityOneInc/ecap-workspace/commit/b7e3ca38f8ea6475db086c59932629bac6a95ccd)

## `36f917a5` feat(database): session_job_repo for scheduler cleanup (PR 1/6) (#932)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:56:33Z
- **链接**: [36f917a5](https://github.com/SerendipityOneInc/ecap-workspace/commit/36f917a5f8ef7121dc1e4c538c5e0f671838ef30)

## `48c5cc48` chore: remove empty app/service/ ghost directory (PR 5/6) (#936)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:55:47Z
- **链接**: [48c5cc48](https://github.com/SerendipityOneInc/ecap-workspace/commit/48c5cc48d67865cd0979e6c527f2a422cce39c0e)

## `1d92c229` refactor(cron): subscription_cron 改走 user_repo + 抽 3 helper (PR 2/6) (#934)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:55:27Z
- **链接**: [1d92c229](https://github.com/SerendipityOneInc/ecap-workspace/commit/1d92c2298b72957b2b55e3e5b6c3080181847242)

## `ea5bf176` fix(agent-updates): require session reset and preserve redeploy files (#930)
- **作者**: nolan-srp
- **时间**: 2026-04-16T12:42:31Z
- **链接**: [ea5bf176](https://github.com/SerendipityOneInc/ecap-workspace/commit/ea5bf176443b7e854b17daf8801c85b0486cf106)

## `07565b1b` feat(errors): Phase 3 — migrate invite_code service to domain exceptions (#873) (#929)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:29:19Z
- **链接**: [07565b1b](https://github.com/SerendipityOneInc/ecap-workspace/commit/07565b1b17dacb0383a9746e91f2cb3fec045b68)

## `a9a35ca4` test(web): OpenClawUserMessage 覆盖 (#897 Part 1) (#928)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:26:08Z
- **链接**: [a9a35ca4](https://github.com/SerendipityOneInc/ecap-workspace/commit/a9a35ca48ad3baefcb96fa46259623bbca0011b4)

## `74d7c69c` feat(web): 版本升级浮动弹窗 + Changelog 独立页面 (#920)
- **作者**: lynn Zhuang
- **时间**: 2026-04-16T12:24:19Z
- **链接**: [74d7c69c](https://github.com/SerendipityOneInc/ecap-workspace/commit/74d7c69c51b66b574d069861f08b61e3e35ce111)

## `df60173c` feat(billing): align Starter trial UX across subscription panel (#914)
- **作者**: vincent-srp
- **时间**: 2026-04-16T12:14:36Z
- **链接**: [df60173c](https://github.com/SerendipityOneInc/ecap-workspace/commit/df60173cc76673204653154b1a1a00bbe36a22c0)

## `7df228e3` fix(sentry): throttle MM connection reports + global rate limit (#910)
- **作者**: peter-srp
- **时间**: 2026-04-16T12:08:11Z
- **链接**: [7df228e3](https://github.com/SerendipityOneInc/ecap-workspace/commit/7df228e3ba8c888d2ae49cc415c212cf458f6997)

## `e89aee0a` fix: Apple subscription check, DM policy allowFrom, and release published flag (#915)
- **作者**: kaka-srp
- **时间**: 2026-04-16T12:04:46Z
- **链接**: [e89aee0a](https://github.com/SerendipityOneInc/ecap-workspace/commit/e89aee0ac2d7b1bd2ed160868019591518843a6c)

## `fcaf8ebf` test(web): verify billing_cycle=monthly downstream payload (follow-up to #919) (#925)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:01:43Z
- **链接**: [fcaf8ebf](https://github.com/SerendipityOneInc/ecap-workspace/commit/fcaf8ebf21fd6c61e86d522ab37930c752d0570e)

## `7ebf3bbb` feat(errors): Phase 2 — migrate gift_code service to domain exceptions (#873) (#924)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T11:57:55Z
- **链接**: [7ebf3bbb](https://github.com/SerendipityOneInc/ecap-workspace/commit/7ebf3bbbf12628f16646f9f829ff66982dfed0d5)

## `68d1d8f9` test(web): InvoiceHistory + SharedPlanCard 覆盖 (#896 Part 2b) (#921)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T11:52:39Z
- **链接**: [68d1d8f9](https://github.com/SerendipityOneInc/ecap-workspace/commit/68d1d8f919a2725236349b1cc64c33c6274164ca)

## `fed6ab16` test(web): PaywallContent + vitest postcss bypass (#896 Part 2a) (#919)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T11:51:15Z
- **链接**: [fed6ab16](https://github.com/SerendipityOneInc/ecap-workspace/commit/fed6ab16e2fc218f8f1a356cdd38f6a5f501a05d)

## `87db3f0f` fix(web): typewriter cleanup flushes stale useMemo cache (#923)
- **作者**: sam-srp
- **时间**: 2026-04-16T11:37:30Z
- **链接**: [87db3f0f](https://github.com/SerendipityOneInc/ecap-workspace/commit/87db3f0f1dc4011f729f2d61e032e8b9ad392837)

## `104c88cd` feat(errors): Phase 1 — migrate openclaw + leaf utility services to domain exceptions (#873) (#907)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T11:30:52Z
- **链接**: [104c88cd](https://github.com/SerendipityOneInc/ecap-workspace/commit/104c88cdf515e0482a3d0649f01767014b96f7bd)

## `3c99c7a7` test(web): reset mocks per test in DowngradeConfirmModal (follow-up to #916) (#917)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T11:24:15Z
- **链接**: [3c99c7a7](https://github.com/SerendipityOneInc/ecap-workspace/commit/3c99c7a7a9e35eb81ffad4da61cdf82adbc21354)

## `ef2ce17d` Revert "feat(web): Seedance 2.0 上新弹窗 — 自动雇佣 Vibe Drama 并进入聊天" (#918)
- **作者**: bryce-srp
- **时间**: 2026-04-16T10:53:43Z
- **链接**: [ef2ce17d](https://github.com/SerendipityOneInc/ecap-workspace/commit/ef2ce17d6ed05e2fecd261643fbe55bf05c3f8e2)

## `2caf084c` test(web): billing + credits 核心单测 (#896 Part 1) (#916)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T10:47:42Z
- **链接**: [2caf084c](https://github.com/SerendipityOneInc/ecap-workspace/commit/2caf084c9ea1ea12714213c08eebea7a61e02fc1)

## `c04888ba` chore(web): drop redundant LandingClient.tsx entry (follow-up to #911) (#913)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T10:31:02Z
- **链接**: [c04888ba](https://github.com/SerendipityOneInc/ecap-workspace/commit/c04888ba5e2b571243845027ef166268a5afe98b)

## `deb2c236` chore(web): 修正 vitest coverage scope — Client.tsx 分母纠正 (#895) (#911)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T10:14:30Z
- **链接**: [deb2c236](https://github.com/SerendipityOneInc/ecap-workspace/commit/deb2c2360d12f4b55f291594cfd6323572c30108)

## `cd3e58cc` chore(lint): widen pnpm lint to src/ + tests/ (4/4) (#909)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T10:02:44Z
- **链接**: [cd3e58cc](https://github.com/SerendipityOneInc/ecap-workspace/commit/cd3e58ccf5c1bca09ed61941449eaa4bd0a3a5c1)

## `6fa23b55` fix(claw-interface): pin stripe<15 to restore .get() on Session/Subsc… (#908)
- **作者**: tim-srp
- **时间**: 2026-04-16T10:01:59Z
- **链接**: [6fa23b55](https://github.com/SerendipityOneInc/ecap-workspace/commit/6fa23b5525817624d35bf01cd0f2c88b336be0a4)

## `97a8d2a7` chore(lint): fix 2 errors + 46 warnings in tests/ (3/4) (#906)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T09:49:30Z
- **链接**: [97a8d2a7](https://github.com/SerendipityOneInc/ecap-workspace/commit/97a8d2a708caa8133870042b88df2f77f9cb327e)

## `574e61c9` refactor(chat): replace ToolStepsBar with ToolGroup, simplify tool status pipeline (#876)
- **作者**: peter-srp
- **时间**: 2026-04-16T09:41:57Z
- **链接**: [574e61c9](https://github.com/SerendipityOneInc/ecap-workspace/commit/574e61c947cde6803c6479a082e44e022da92f96)

## `233d91b0` feat: require active subscription before granting credits (#884)
- **作者**: bryce-srp
- **时间**: 2026-04-16T09:30:40Z
- **链接**: [233d91b0](https://github.com/SerendipityOneInc/ecap-workspace/commit/233d91b039e13a65df830c6b2f7dc450327d2344)

## `866bb535` feat(claw-interface): Add Apple subscription status query method (#893)
- **作者**: bill-srp
- **时间**: 2026-04-16T09:17:18Z
- **链接**: [866bb535](https://github.com/SerendipityOneInc/ecap-workspace/commit/866bb5358602f45e6488900b13b3abae8a066ecd)

## `9735f196` chore(lint): prettier + import-sort autofix for tests/ (2/4) (#892)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T09:00:15Z
- **链接**: [9735f196](https://github.com/SerendipityOneInc/ecap-workspace/commit/9735f196d5b2bfedac762aca981f1b002f2652cf)

## `1898b4c9` feat(errors): Phase 0 — domain-exception layer + C3 contract (#873) (#889)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T08:59:06Z
- **链接**: [1898b4c9](https://github.com/SerendipityOneInc/ecap-workspace/commit/1898b4c9f33aa523de0a02a95583f8ca42c0050b)

## `4bee6471` feat(web): Seedance 2.0 上新弹窗 — 自动雇佣 Vibe Drama 并进入聊天 (#866)
- **作者**: lynn Zhuang
- **时间**: 2026-04-16T08:55:12Z
- **链接**: [4bee6471](https://github.com/SerendipityOneInc/ecap-workspace/commit/4bee64710a11e4f3d220c751bf4c43c3e4a923f6)

## `62338cda` chore(lint): add tests/ override + lint:tests script (1/4) (#890)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T08:46:42Z
- **链接**: [62338cda](https://github.com/SerendipityOneInc/ecap-workspace/commit/62338cda895d1d4e0a254b05e093edaf34f0a854)

## `5b0ecd26` feat(seo): 301 redirect ecap.gensmo.com → zooclaw.ai + migration banner (#887)
- **作者**: peter-srp
- **时间**: 2026-04-16T08:34:10Z
- **链接**: [5b0ecd26](https://github.com/SerendipityOneInc/ecap-workspace/commit/5b0ecd260a733ceb750330567fe8b0707e38e410)

## `a4b3c4de` chore(ci-lint): guard that three import-linter repo lists stay in sync (#888)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T08:20:29Z
- **链接**: [a4b3c4de](https://github.com/SerendipityOneInc/ecap-workspace/commit/a4b3c4def76bbe08d39e205e7ab986c13a71d2bb)

## `97687fd0` docs(superpowers): service-layer exception decoupling spec (#873 Item 1) (#882)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T08:17:54Z
- **链接**: [97687fd0](https://github.com/SerendipityOneInc/ecap-workspace/commit/97687fd081695c2bcdb7a3c36d315f1b918eec02)

## `07409bf0` fix(devcontainer): activate claw-interface venv in all shells (#886)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T08:06:53Z
- **链接**: [07409bf0](https://github.com/SerendipityOneInc/ecap-workspace/commit/07409bf09e9d1fe19e13b59a048fa169e57bce99)

## `0b12920e` chore(ci-lint): retire 02-repo-pattern-guard.sh (superseded by import-linter C1) (#885)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:55:05Z
- **链接**: [0b12920e](https://github.com/SerendipityOneInc/ecap-workspace/commit/0b12920ecd178e9347b767605fe4647363723e41)

## `a098ef9d` feat(sentry): comprehensive monitoring coverage (#860)
- **作者**: peter-srp
- **时间**: 2026-04-16T07:40:17Z
- **链接**: [a098ef9d](https://github.com/SerendipityOneInc/ecap-workspace/commit/a098ef9df2424aa329b4f7960adfc757cc3a8fd6)

## `c85e2e01` chore(lint): add layered-architecture contracts (C2, C2b, C4, C4b) (#872)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:33:02Z
- **链接**: [c85e2e01](https://github.com/SerendipityOneInc/ecap-workspace/commit/c85e2e01c17a7ec347ddf8ae44d97e06e9c7c1f3)

## `83dfaab7` fix(agents-manager): require explicit session reset after updates (#879)
- **作者**: nolan-srp
- **时间**: 2026-04-16T07:30:25Z
- **链接**: [83dfaab7](https://github.com/SerendipityOneInc/ecap-workspace/commit/83dfaab7c9c3745109230c8a18d300e2569c5da0)

## `ae8b90e6` chore(claw-interface): enforce deptry gate — Step 2 of #870 (#883)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:23:42Z
- **链接**: [ae8b90e6](https://github.com/SerendipityOneInc/ecap-workspace/commit/ae8b90e6af491b9e4a15e35e11499986cb102c92)

## `0ad945f7` chore(lint): adopt import-linter with C1 mongo-isolation contract (#871)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:21:53Z
- **链接**: [0ad945f7](https://github.com/SerendipityOneInc/ecap-workspace/commit/0ad945f795ccef2c5bcef6f4bc034f77d955188e)

## `37b0a736` test(claw-interface): harden 04-deptry.sh test from silent no-op (#880)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:14:34Z
- **链接**: [37b0a736](https://github.com/SerendipityOneInc/ecap-workspace/commit/37b0a7365acfd73dac1bbde02288e1638b8b18a7)

## `bf68cfd8` docs(openclaw-runtime): fix _resolve docstring to match 3-tuple return (#881)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:12:03Z
- **链接**: [bf68cfd8](https://github.com/SerendipityOneInc/ecap-workspace/commit/bf68cfd87a1218b7b02263853870dc0d04d8043c)

## `2dafe33c` chore(claw-interface): add deptry dependency-consistency gate (warning mode) — Step 1 of #870 (#877)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:02:16Z
- **链接**: [2dafe33c](https://github.com/SerendipityOneInc/ecap-workspace/commit/2dafe33c6cb57f8484112343e7bd8b5a98dd41c7)

## `e0b661a0` fix: change connector skill injection path to ~/.agents/skills (#878)
- **作者**: Leo-srp
- **时间**: 2026-04-16T06:45:35Z
- **链接**: [e0b661a0](https://github.com/SerendipityOneInc/ecap-workspace/commit/e0b661a00c8928cf94f4999198cd2c96661a6bc4)

## `031a481d` fix(web): 修复 agent 详情页和弹窗里头像浮动动画的问题 (#863)
- **作者**: lynn Zhuang
- **时间**: 2026-04-16T06:06:18Z
- **链接**: [031a481d](https://github.com/SerendipityOneInc/ecap-workspace/commit/031a481d8a583bb22eecab27d987206a0f367aeb)

## `00e43349` docs(lazy-imports): annotate the non-obvious function-body imports (#874)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T05:44:45Z
- **链接**: [00e43349](https://github.com/SerendipityOneInc/ecap-workspace/commit/00e43349e1576e9a2c09ee1c288e41ad5cc38a89)

## `055867ba` refactor(openclaw): move get_user_bot_and_token to services layer (#869)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T05:16:01Z
- **链接**: [055867ba](https://github.com/SerendipityOneInc/ecap-workspace/commit/055867ba4a78682c67d825024fcf37d2923e5592)

## `0343d092` refactor(orders): import ensure_billing_initialized from services directly (#868)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T05:14:36Z
- **链接**: [0343d092](https://github.com/SerendipityOneInc/ecap-workspace/commit/0343d0928046a3e649b1bddc1b6c5b07769fcdfb)

## `caa19e66` chore(ci-lint): broaden repo-pattern scan to entire app/ except database/ (#867)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T05:14:01Z
- **链接**: [caa19e66](https://github.com/SerendipityOneInc/ecap-workspace/commit/caa19e665ed9c93405e9a994b1fd916f59cf0fc3)

## `d4834a34` test(claw-interface): extract shared user-doc builder (#864) (#865)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T04:26:39Z
- **链接**: [d4834a34](https://github.com/SerendipityOneInc/ecap-workspace/commit/d4834a34474d41f9baff4b97fcbfb20ea44f8ad9)

## `ea63724b` chore(ci-lint): extend repo-pattern guard to scan app/lifetime.py (#859)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T04:18:52Z
- **链接**: [ea63724b](https://github.com/SerendipityOneInc/ecap-workspace/commit/ea63724b8672414f41e640fd25a2ace9d66cde96)

## `a145411b` refactor(claw-interface): extract resolve_or_generate_code (#853)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T04:10:02Z
- **链接**: [a145411b](https://github.com/SerendipityOneInc/ecap-workspace/commit/a145411be12afef692a0e81365ec76ed7c8c1ad5)

## `f6403881` feat(chat): Mattermost reactions, tool-steps toggle, smoother streaming (#742)
- **作者**: sam-srp
- **时间**: 2026-04-16T04:07:10Z
- **链接**: [f6403881](https://github.com/SerendipityOneInc/ecap-workspace/commit/f6403881f57af2391379eaabaddecc0b563d2c2b)

## `7507366c` refactor(claw-interface): PagedResponse model + duplicate-key helper (#851)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T04:01:50Z
- **链接**: [7507366c](https://github.com/SerendipityOneInc/ecap-workspace/commit/7507366cc549370226c8d78623c25af1ab193eb9)

## `ffb124a8` chore(ci-lint): tighten jscpd tests threshold 10.5% → 7.5% (#852)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T03:49:08Z
- **链接**: [ffb124a8](https://github.com/SerendipityOneInc/ecap-workspace/commit/ffb124a8ef958464b0cc3c45aae72cd5ccff42a4)

## `5b61ec43` test(claw-interface): round 4 dedup — connector_status + admin_boost (-60 LOC) (#856)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T03:40:44Z
- **链接**: [5b61ec43](https://github.com/SerendipityOneInc/ecap-workspace/commit/5b61ec43452498e077049d9ca9103fe84e2cf727)

## `22f0b03e` test(claw-interface): round 5 dedup — chat_validation (-65 LOC) (#857)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T03:34:55Z
- **链接**: [22f0b03e](https://github.com/SerendipityOneInc/ecap-workspace/commit/22f0b03e1eea4c48a1ac5e6df8575c53ca232fee)

## `afa99590` test(claw-interface): round 6 dedup — litellm_sse_edit (-36 LOC) (#858)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T03:34:27Z
- **链接**: [afa99590](https://github.com/SerendipityOneInc/ecap-workspace/commit/afa99590dd8981471c0119713081a608fbc0eb70)

## `cab8e9d4` refactor(claw-interface): unify admin guard into shared dependency (#847)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T03:32:08Z
- **链接**: [cab8e9d4](https://github.com/SerendipityOneInc/ecap-workspace/commit/cab8e9d439492eebe133a8307fb27f7e6bf8a932)

## `748d119b` fix(claw-interface): scope skill loader hidden-file filter to skill dir (#839)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T02:55:50Z
- **链接**: [748d119b](https://github.com/SerendipityOneInc/ecap-workspace/commit/748d119b1d13e4c77ae71e853ac03e5b1fb4c121)

