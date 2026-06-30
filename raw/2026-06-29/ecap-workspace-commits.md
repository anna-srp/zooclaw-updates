# ecap-workspace commits — 2026-06-29


共 11 个 commit


---

## chore: bump favie-common to v0.3.68 (#2657)

- **SHA**: `f3ec92150865a448ba9fb2adf54c6efb437dc145`
- **作者**: tim-srp
- **日期**: 2026-06-29T14:29:04Z
- **PR**: #2657

### 完整 Commit Message

```
chore: bump favie-common to v0.3.68 (#2657)

## Summary
- Bump `services/claw-interface/requirements.txt` from `favie-common`
`v0.3.66` to `v0.3.68`.
- This pulls in the merged `find_one_and_update` sensitive-collection
dual-write fix from `SerendipityOneInc/favie-common#101`.

## Verification
- `rg "favie-common\.git@|SerendipityOneInc/favie-common" -n .`
- `git diff --check`
- `git ls-remote --tags
https://github.com/SerendipityOneInc/favie-common.git
"refs/tags/v0.3.68*"`
- `python -m pip install --no-deps --target "$tmpdir"
"git+https://github.com/SerendipityOneInc/favie-common.git@v0.3.68"`

Note: the direct Git source build still reports the package metadata
version from `favie-common` source (`0.3.66`), but the code is resolved
from tag `v0.3.68`; the GitHub Release artifact itself is `0.3.68`.
```

### PR Body

## Summary
- Bump `services/claw-interface/requirements.txt` from `favie-common` `v0.3.66` to `v0.3.68`.
- This pulls in the merged `find_one_and_update` sensitive-collection dual-write fix from `SerendipityOneInc/favie-common#101`.

## Verification
- `rg "favie-common\.git@|SerendipityOneInc/favie-common" -n .`
- `git diff --check`
- `git ls-remote --tags https://github.com/SerendipityOneInc/favie-common.git "refs/tags/v0.3.68*"`
- `python -m pip install --no-deps --target "$tmpdir" "git+https://github.com/SerendipityOneInc/favie-common.git@v0.3.68"`

Note: the direct Git source build still reports the package metadata version from `favie-common` source (`0.3.66`), but the code is resolved from tag `v0.3.68`; the GitHub Release artifact itself is `0.3.68`.


---

## fix(billing): require Billing Profile keys for runtime flows (#2649)

- **SHA**: `f2283c9195c669f91449bf283e7d3ceb79dfcb58`
- **作者**: kaka-srp
- **日期**: 2026-06-29T12:33:45Z
- **PR**: #2649

### 完整 Commit Message

```
fix(billing): require Billing Profile keys for runtime flows (#2649)

## Summary
- Route runtime LiteLLM key resolution through ready Billing Profile
only; account `billing_key` remains schema-compatible but is no longer a
runtime credential source.
- Clean non-Billing-v2 call sites across session/chat, OpenClaw bot env
sync, normalized computers, pack tests, warm-pool, subscription
code/trial/expiry, Stripe/Antom entitlement paths.
- Add compatibility repair for legacy-ready expiry cleanup and warm-pool
partial rows by materializing legacy billing state into Billing Profile
before continuing.
- Keep admin billing events queryable by uid/customer id for ops
debugging without falling back to legacy `team_id` or account key.

## Root cause
Runtime and lifecycle paths still had mixed Billing v1/v2 assumptions:
some paths read account-level billing fields directly, while others
required Billing Profile readiness. That could either inject stale
account keys or skip cleanup for legacy data that had not yet
materialized a Billing Profile.

## Production data check
- Active/paid marker accounts without ready profile: 0
- Recent 30d session/openclaw/pack-test runtime users without ready
profile: 0
- Remaining gaps were expired/free/stopped or warm-pool hygiene rows;
this PR adds self-healing for the warm-pool partial and expiry cleanup
cases.

## Test plan
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_account_billing_key.py tests/unit/test_admin_events.py
tests/unit/test_antom_subscription_trials.py
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_billing_profiles_v2.py
tests/unit/test_billing_summary_v2.py
tests/unit/test_billing_warm_pool.py
tests/unit/test_chat_create_session.py tests/unit/test_chat_endpoint.py
tests/unit/test_chat_validation.py tests/unit/test_computer_service.py
tests/unit/test_openclaw_bot_config.py
tests/unit/test_openclaw_routes.py
tests/unit/test_pack_test_runtime_service.py
tests/unit/test_stripe_entitlement_service.py
tests/unit/test_subscription_code.py
tests/unit/test_subscription_expiry.py
tests/unit/test_billing_v2_cleanup_coverage.py
tests/unit/test_user_trial_credits_service.py
tests/unit/test_warm_pool.py
tests/unit/test_warm_pool_openclaw_assets.py
tests/unit/test_warm_pool_provisioning_assets.py -q --tb=short` (`437
passed`)

Linear: https://linear.app/srpone/issue/ECA-1099
```

### PR Body

## Summary
- Route runtime LiteLLM key resolution through ready Billing Profile only; account `billing_key` remains schema-compatible but is no longer a runtime credential source.
- Clean non-Billing-v2 call sites across session/chat, OpenClaw bot env sync, normalized computers, pack tests, warm-pool, subscription code/trial/expiry, Stripe/Antom entitlement paths.
- Add compatibility repair for legacy-ready expiry cleanup and warm-pool partial rows by materializing legacy billing state into Billing Profile before continuing.
- Keep admin billing events queryable by uid/customer id for ops debugging without falling back to legacy `team_id` or account key.

## Root cause
Runtime and lifecycle paths still had mixed Billing v1/v2 assumptions: some paths read account-level billing fields directly, while others required Billing Profile readiness. That could either inject stale account keys or skip cleanup for legacy data that had not yet materialized a Billing Profile.

## Production data check
- Active/paid marker accounts without ready profile: 0
- Recent 30d session/openclaw/pack-test runtime users without ready profile: 0
- Remaining gaps were expired/free/stopped or warm-pool hygiene rows; this PR adds self-healing for the warm-pool partial and expiry cleanup cases.

## Test plan
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_account_billing_key.py tests/unit/test_admin_events.py tests/unit/test_antom_subscription_trials.py tests/unit/test_billing_profiles_initialization.py tests/unit/test_billing_profiles_v2.py tests/unit/test_billing_summary_v2.py tests/unit/test_billing_warm_pool.py tests/unit/test_chat_create_session.py tests/unit/test_chat_endpoint.py tests/unit/test_chat_validation.py tests/unit/test_computer_service.py tests/unit/test_openclaw_bot_config.py tests/unit/test_openclaw_routes.py tests/unit/test_pack_test_runtime_service.py tests/unit/test_stripe_entitlement_service.py tests/unit/test_subscription_code.py tests/unit/test_subscription_expiry.py tests/unit/test_billing_v2_cleanup_coverage.py tests/unit/test_user_trial_credits_service.py tests/unit/test_warm_pool.py tests/unit/test_warm_pool_openclaw_assets.py tests/unit/test_warm_pool_provisioning_assets.py -q --tb=short` (`437 passed`)

Linear: https://linear.app/srpone/issue/ECA-1099



---

## feat(claw-interface): add paid agent pack listing (#2655)

- **SHA**: `14de3e83bbf3773c9a4f6a1a7bf4c5a558049a44`
- **作者**: bill-srp
- **日期**: 2026-06-29T12:24:29Z
- **PR**: #2655

### 完整 Commit Message

```
feat(claw-interface): add paid agent pack listing (#2655)

## Summary

- Add paid agent-pack listing metadata, price rows, origin lookup, and
indexes.
- Add user-triggered paid listing submission that copies the source pack
submission asset into the ZooClaw org.
- Keep paid listing creation retryable by writing the paid pack as draft
first, then submission, then price, and finally moving the pack to
listing review.
- Extend review approval to bind the approved price to the paid pack.

## Validation

- `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_paid_listing_service.py -q`
- `/opt/homebrew/bin/ruff check
services/claw-interface/app/services/pack_store/paid_listing_service.py
services/claw-interface/tests/unit/test_paid_listing_service.py`
- `/opt/homebrew/bin/ruff format --check
services/claw-interface/app/services/pack_store/paid_listing_service.py
services/claw-interface/tests/unit/test_paid_listing_service.py`
- `/Users/bill/.venvs/claw-interface/bin/lint-imports`
- `git diff --check`

## Notes

- `bash scripts/verify-changed.sh` returned 3 locally because the script
could not find the backend pyright/import-linter toolchain on PATH and
skipped the py gate.
- Direct import-linter passed via the existing venv. Direct pyright was
not usable in this local shell because it could not resolve broad
project dependencies such as fastapi, pytest, and favie_common.
```

### PR Body

## Summary

- Add paid agent-pack listing metadata, price rows, origin lookup, and indexes.
- Add user-triggered paid listing submission that copies the source pack submission asset into the ZooClaw org.
- Keep paid listing creation retryable by writing the paid pack as draft first, then submission, then price, and finally moving the pack to listing review.
- Extend review approval to bind the approved price to the paid pack.

## Validation

- `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_paid_listing_service.py -q`
- `/opt/homebrew/bin/ruff check services/claw-interface/app/services/pack_store/paid_listing_service.py services/claw-interface/tests/unit/test_paid_listing_service.py`
- `/opt/homebrew/bin/ruff format --check services/claw-interface/app/services/pack_store/paid_listing_service.py services/claw-interface/tests/unit/test_paid_listing_service.py`
- `/Users/bill/.venvs/claw-interface/bin/lint-imports`
- `git diff --check`

## Notes

- `bash scripts/verify-changed.sh` returned 3 locally because the script could not find the backend pyright/import-linter toolchain on PATH and skipped the py gate.
- Direct import-linter passed via the existing venv. Direct pyright was not usable in this local shell because it could not resolve broad project dependencies such as fastapi, pytest, and favie_common.



---

## fix(pack-test): cap temporary bot slug length (#2650)

- **SHA**: `dd1de9ad2b79161a2aa8cf793e3c8560c3a5726b`
- **作者**: kaka-srp
- **日期**: 2026-06-29T11:59:35Z
- **PR**: #2650

### 完整 Commit Message

```
fix(pack-test): cap temporary bot slug length (#2650)

## Summary
- Cap Pack Test temporary FastClaw bot slugs at 50 characters.
- Preserve the pack display id while truncating only the temporary
runtime bot name.
- Add regression coverage for the shanghai-weather-outfit failure shape
and longer display ids.

## Testing
- bash scripts/verify-py.sh
- bash scripts/verify-changed.sh
- cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_pack_test_runtime_service.py -q

## Linear
https://linear.app/srpone/issue/ECA-1128/fix-pack-test-bot-slug-length
```

### PR Body

## Summary
- Cap Pack Test temporary FastClaw bot slugs at 50 characters.
- Preserve the pack display id while truncating only the temporary runtime bot name.
- Add regression coverage for the shanghai-weather-outfit failure shape and longer display ids.

## Testing
- bash scripts/verify-py.sh
- bash scripts/verify-changed.sh
- cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_pack_test_runtime_service.py -q

## Linear
https://linear.app/srpone/issue/ECA-1128/fix-pack-test-bot-slug-length



---

## docs(agents): add computer settings migration plan (#2644)

- **SHA**: `0a4121f388f6ee56d223e452d80b2cd2dafd2f5e`
- **作者**: bill-srp
- **日期**: 2026-06-29T10:39:04Z
- **PR**: #2644

### 完整 Commit Message

```
docs(agents): add computer settings migration plan (#2644)

## Linear
N/A

## Summary
- Add the computer-scoped agent settings migration design spec.
- Add the implementation plan used to split backend and frontend work.

## Split
This is the docs-only slice split out from the original agent settings
migration PR.

Related PRs:
- Backend slice: #2637
- Frontend slice: stacked on #2637

## Test plan
- [x] Documentation-only change; no runtime tests required.
```

### PR Body

## Linear
N/A

## Summary
- Add the computer-scoped agent settings migration design spec.
- Add the implementation plan used to split backend and frontend work.

## Split
This is the docs-only slice split out from the original agent settings migration PR.

Related PRs:
- Backend slice: #2637
- Frontend slice: stacked on #2637

## Test plan
- [x] Documentation-only change; no runtime tests required.



---

## docs: sync-docs weekly sweep (2026-06-29) (#2642)

- **SHA**: `91a33b5f95134892ea95cc1bf3e9748972ccc1a7`
- **作者**: srp-claude-assistant[bot]
- **日期**: 2026-06-29T08:47:15Z
- **PR**: #2642

### 完整 Commit Message

```
docs: sync-docs weekly sweep (2026-06-29) (#2642)

## Tier 1 — Deterministic fixes

_(probe clean — no path/version/structure/env hits)_

## Tier 2 — Semantic fixes (with evidence)

- **`web/app/AGENTS.md` — shadcn installed list stale**: `input`,
`label`, `select` still listed under "常用还没装的" but all three are present
at `web/app/src/components/ds/input.tsx`, `label.tsx`, `select.tsx`
(added in PR #1818). Moved to "已安装"; removed from the not-yet list.

- **`AGENTS.md` — devcontainer state-backup capability undocumented**:
`.agents/skills/devcontainer-state-backup/SKILL.md` and
`scripts/dev-state-backup.sh` were added in this window (commit
`9b6b7c9fd` area). The DevContainer section had no pointer to this
capability; someone rebuilding their container would not know agent
state can be preserved. Added a one-line note pointing to the skill and
`docs/devcontainer-state-backup.md`.

## Tier 3 — Suggestions (not applied)

- `README.md` `initializeCommand.sh` description: the script now also
ensures `/dev/net/tun` exists (for Telepresence) and creates
`~/.cache/pnpm` — not mentioned in README. Low impact; the existing
description ("resolves GitHub token, merges .env") is still accurate for
onboarding purposes.
- `web/app/AGENTS.md` shadcn "加新组件" examples still reference `npx
shadcn@latest add input` and `npx shadcn@latest add card label` — the
`input` example is now redundant since `input` is installed. Could be
updated to a different not-yet-installed component as the example, but
this is cosmetic.

---

**Docs changed**: `AGENTS.md`, `web/app/AGENTS.md`

**Review window**: `ee0066df3..HEAD` (~90 days)

Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### PR Body

## Tier 1 — Deterministic fixes

_(probe clean — no path/version/structure/env hits)_

## Tier 2 — Semantic fixes (with evidence)

- **`web/app/AGENTS.md` — shadcn installed list stale**: `input`, `label`, `select` still listed under "常用还没装的" but all three are present at `web/app/src/components/ds/input.tsx`, `label.tsx`, `select.tsx` (added in PR #1818). Moved to "已安装"; removed from the not-yet list.

- **`AGENTS.md` — devcontainer state-backup capability undocumented**: `.agents/skills/devcontainer-state-backup/SKILL.md` and `scripts/dev-state-backup.sh` were added in this window (commit `9b6b7c9fd` area). The DevContainer section had no pointer to this capability; someone rebuilding their container would not know agent state can be preserved. Added a one-line note pointing to the skill and `docs/devcontainer-state-backup.md`.

## Tier 3 — Suggestions (not applied)

- `README.md` `initializeCommand.sh` description: the script now also ensures `/dev/net/tun` exists (for Telepresence) and creates `~/.cache/pnpm` — not mentioned in README. Low impact; the existing description ("resolves GitHub token, merges .env") is still accurate for onboarding purposes.
- `web/app/AGENTS.md` shadcn "加新组件" examples still reference `npx shadcn@latest add input` and `npx shadcn@latest add card label` — the `input` example is now redundant since `input` is installed. Could be updated to a different not-yet-installed component as the example, but this is cosmetic.

---

**Docs changed**: `AGENTS.md`, `web/app/AGENTS.md`

**Review window**: `ee0066df3..HEAD` (~90 days)



---

## docs: sync-docs weekly sweep (2026-06-29) (#2642)

- **SHA**: `1d448f9c5e80496626703476e5f15258ee874350`
- **作者**: srp-claude-assistant[bot]
- **日期**: 2026-06-29T08:47:15Z
- **PR**: #2642

### 完整 Commit Message

```
docs: sync-docs weekly sweep (2026-06-29) (#2642)

## Tier 1 — Deterministic fixes

_(probe clean — no path/version/structure/env hits)_

## Tier 2 — Semantic fixes (with evidence)

- **`web/app/AGENTS.md` — shadcn installed list stale**: `input`,
`label`, `select` still listed under "常用还没装的" but all three are present
at `web/app/src/components/ds/input.tsx`, `label.tsx`, `select.tsx`
(added in PR #1818). Moved to "已安装"; removed from the not-yet list.

- **`AGENTS.md` — devcontainer state-backup capability undocumented**:
`.agents/skills/devcontainer-state-backup/SKILL.md` and
`scripts/dev-state-backup.sh` were added in this window (commit
`9b6b7c9fd` area). The DevContainer section had no pointer to this
capability; someone rebuilding their container would not know agent
state can be preserved. Added a one-line note pointing to the skill and
`docs/devcontainer-state-backup.md`.

## Tier 3 — Suggestions (not applied)

- `README.md` `initializeCommand.sh` description: the script now also
ensures `/dev/net/tun` exists (for Telepresence) and creates
`~/.cache/pnpm` — not mentioned in README. Low impact; the existing
description ("resolves GitHub token, merges .env") is still accurate for
onboarding purposes.
- `web/app/AGENTS.md` shadcn "加新组件" examples still reference `npx
shadcn@latest add input` and `npx shadcn@latest add card label` — the
`input` example is now redundant since `input` is installed. Could be
updated to a different not-yet-installed component as the example, but
this is cosmetic.

---

**Docs changed**: `AGENTS.md`, `web/app/AGENTS.md`

**Review window**: `ee0066df3..HEAD` (~90 days)

Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### PR Body

## Tier 1 — Deterministic fixes

_(probe clean — no path/version/structure/env hits)_

## Tier 2 — Semantic fixes (with evidence)

- **`web/app/AGENTS.md` — shadcn installed list stale**: `input`, `label`, `select` still listed under "常用还没装的" but all three are present at `web/app/src/components/ds/input.tsx`, `label.tsx`, `select.tsx` (added in PR #1818). Moved to "已安装"; removed from the not-yet list.

- **`AGENTS.md` — devcontainer state-backup capability undocumented**: `.agents/skills/devcontainer-state-backup/SKILL.md` and `scripts/dev-state-backup.sh` were added in this window (commit `9b6b7c9fd` area). The DevContainer section had no pointer to this capability; someone rebuilding their container would not know agent state can be preserved. Added a one-line note pointing to the skill and `docs/devcontainer-state-backup.md`.

## Tier 3 — Suggestions (not applied)

- `README.md` `initializeCommand.sh` description: the script now also ensures `/dev/net/tun` exists (for Telepresence) and creates `~/.cache/pnpm` — not mentioned in README. Low impact; the existing description ("resolves GitHub token, merges .env") is still accurate for onboarding purposes.
- `web/app/AGENTS.md` shadcn "加新组件" examples still reference `npx shadcn@latest add input` and `npx shadcn@latest add card label` — the `input` example is now redundant since `input` is installed. Could be updated to a different not-yet-installed component as the example, but this is cosmetic.

---

**Docs changed**: `AGENTS.md`, `web/app/AGENTS.md`

**Review window**: `ee0066df3..HEAD` (~90 days)



---

## fix(chat): gate pack test preview session fetch (#2640)

- **SHA**: `9b6b7c9fd5da35ea79f94e431e627f754217c358`
- **作者**: kaka-srp
- **日期**: 2026-06-29T08:05:44Z
- **PR**: #2640

### 完整 Commit Message

```
fix(chat): gate pack test preview session fetch (#2640)

## Summary
- Gate the Mattermost pack-test preview-session fetch behind a confirmed
pack-test computer.
- Add coverage for normal route computers and pack-test records missing
a run id.

## Root cause
The Mattermost provider treated any URL computer_id as a pack-test
preview computer and called the preview-session endpoint. The backend
intentionally returns 404 for non-pack-test computers, which created
Sentry noise for normal chat routes.

Linear:
https://linear.app/srpone/issue/ECA-1093/前端-pack-test-preview-session-接口-404-apiclawcomputersuuidpack-test

## Test plan
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/contexts/MattermostContext.unit.spec.tsx
- [x] bash scripts/verify-web.sh
web/app/src/components/providers/MattermostProvider.tsx
web/app/tests/unit/contexts/MattermostContext.unit.spec.tsx
- [x] bash scripts/verify-changed.sh
```

### PR Body

## Summary
- Gate the Mattermost pack-test preview-session fetch behind a confirmed pack-test computer.
- Add coverage for normal route computers and pack-test records missing a run id.

## Root cause
The Mattermost provider treated any URL computer_id as a pack-test preview computer and called the preview-session endpoint. The backend intentionally returns 404 for non-pack-test computers, which created Sentry noise for normal chat routes.

Linear: https://linear.app/srpone/issue/ECA-1093/前端-pack-test-preview-session-接口-404-apiclawcomputersuuidpack-test

## Test plan
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/contexts/MattermostContext.unit.spec.tsx
- [x] bash scripts/verify-web.sh web/app/src/components/providers/MattermostProvider.tsx web/app/tests/unit/contexts/MattermostContext.unit.spec.tsx
- [x] bash scripts/verify-changed.sh



---

## feat(chat): support conversation titles (#2636)

- **SHA**: `7a4916cf8b37b74435d6cfbdd36d553916d86dc1`
- **作者**: bill-srp
- **日期**: 2026-06-29T07:09:30Z
- **PR**: #2636

### 完整 Commit Message

```
feat(chat): support conversation titles (#2636)

## Summary

- Add conversation title metadata to OpenClaw session-channel records
and keep create/update/list responses on the same record shape.
- Generate a concise title during conversation creation from the
submitted title via LiteLLM proxy, with fallback behavior when
generation is unavailable.
- Add manual rename through `POST
/computers/{computer_id}/agents/{agent_id}/conversations/{session_id}`
with `title` in the request body.
- Wire the frontend conversation list/thread UI to display and rename
titles.

Linear:
https://linear.app/srpone/issue/ECA-1034/chat-session-%E6%94%AF%E6%8C%81%E6%A0%87%E9%A2%98-rename-%E5%92%8C%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90%E6%A0%87%E9%A2%98

## Local Checks

- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh` passed.
- `cd services/claw-interface &&
/Users/bill/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_chat_session_title_service.py
tests/unit/test_openclaw_session_channel_schema.py
tests/unit/test_openclaw_session_channel_repo.py
tests/unit/test_conversations.py
tests/unit/test_openclaw_session_channel_service.py
tests/unit/test_agent_builder_service.py -q` passed: 127 passed.
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-changed.sh` ran backend verification successfully and
exited 3 because `web/node_modules` is missing, so the web surface was
skipped.
- `bash scripts/verify-web.sh ...` ran frontend governance guards, then
could not reach tsc/vitest/eslint because pnpm attempted install and
repeatedly failed to resolve `registry.npmjs.org` in this environment. I
interrupted the retrying install after the repeated DNS failures.
```

### PR Body

## Summary

- Add conversation title metadata to OpenClaw session-channel records and keep create/update/list responses on the same record shape.
- Generate a concise title during conversation creation from the submitted title via LiteLLM proxy, with fallback behavior when generation is unavailable.
- Add manual rename through `POST /computers/{computer_id}/agents/{agent_id}/conversations/{session_id}` with `title` in the request body.
- Wire the frontend conversation list/thread UI to display and rename titles.

Linear: https://linear.app/srpone/issue/ECA-1034/chat-session-%E6%94%AF%E6%8C%81%E6%A0%87%E9%A2%98-rename-%E5%92%8C%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90%E6%A0%87%E9%A2%98

## Local Checks

- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh` passed.
- `cd services/claw-interface && /Users/bill/.venvs/claw-interface/bin/python -m pytest tests/unit/test_chat_session_title_service.py tests/unit/test_openclaw_session_channel_schema.py tests/unit/test_openclaw_session_channel_repo.py tests/unit/test_conversations.py tests/unit/test_openclaw_session_channel_service.py tests/unit/test_agent_builder_service.py -q` passed: 127 passed.
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-changed.sh` ran backend verification successfully and exited 3 because `web/node_modules` is missing, so the web surface was skipped.
- `bash scripts/verify-web.sh ...` ran frontend governance guards, then could not reach tsc/vitest/eslint because pnpm attempted install and repeatedly failed to resolve `registry.npmjs.org` in this environment. I interrupted the retrying install after the repeated DNS failures.



---

## feat(zooclaw-ds): radix-nova component baseline (tokens + ~53 components + preview) (#2615)

- **SHA**: `1316ece38acc1fe7c13ded50b334216b9c86aeb0`
- **作者**: lynn Zhuang
- **日期**: 2026-06-29T06:28:18Z
- **PR**: #2615

### 完整 Commit Message

```
feat(zooclaw-ds): radix-nova component baseline (tokens + ~53 components + preview) (#2615)

## What

Builds the **full shadcn radix-nova component baseline** for
`@zooclaw/design-system`, rendered through `@zooclaw/tokens`. Re-ports
the existing components from the canonical radix-nova source and adds
the missing primitives, so the package is a complete,
internally-consistent component set with ZooClaw's brand (ink-first,
brand red as a sparing accent, Liquid-Glass surfaces).

Spec/plan:
`docs/superpowers/specs/2026-06-25-zooclaw-ds-radix-nova-baseline-design.md`
+ `docs/superpowers/plans/2026-06-25-zooclaw-ds-radix-nova-baseline.md`.

**Scope:** only the two DS packages + the spec/plan docs (+ the lockfile
for Phase-2 deps). No `web/app`, no services.

## Components (~53)

- **Phase 0 — re-port (16):** button, input, textarea, label, field,
checkbox, switch, tooltip, dropdown-menu, dialog, select, badge, card,
tabs, accordion, alert (+ the original toast, now superseded).
- **Phase 1 — new primitives (28):** popover, hover-card, alert-dialog,
sheet, collapsible, context-menu, menubar, navigation-menu, scroll-area,
aspect-ratio, radio-group, slider, toggle, toggle-group, native-select,
avatar, skeleton, progress, spinner, kbd, separator, button-group,
input-group, pagination, breadcrumb, table, item, empty.
- **Phase 2 — light-dep (4):** command (`cmdk`), drawer (`vaul`),
input-otp (`input-otp`), sonner (`sonner`). `sonner` is now the
canonical `Toaster`/`toast`; the hand-rolled toast is `@deprecated` +
dropped from the barrel.

New deps: `cmdk ^1.1.1`, `vaul ^1.1.2`, `input-otp ^1.4.2`, `sonner
^2.0.7`.

## Tokens & brand rules

- **3-tier tokens** unchanged in shape; refinements this PR:
- `--zc-wash` neutral so `hover:bg-muted/accent` reads as a visible
change (was collapsed onto `--background`).
- `--ring` = **mid-gray ink** (`--zc-ink-3`), not brand red — a red
focus ring read as an error. Red now only on `destructive` /
`aria-invalid`.
- **Brand reconciliation** applied per component: `default` button stays
dark CTA (not red); selected/checked/range fills use ink; overlays use
ZooClaw glass; destructive is the radix-nova soft tint; outline button
is transparent (shows its surface).
- **Icons:** lucide/tabler → **Heroicons** throughout (no lucide dep).

## Preview (docs catalog)

Full English preview with a section per component, a complete
**Typography** scale (h1–h4 serif,
lead/p/blockquote/list/code/large/small/muted/table), and a
comprehensive Button showcase (variants, sizes, icon, with-icon,
rounded, loading/spinner, nested Button Group, as-child).

## ⚠️ Consumer contract

The components use shadcn radix-nova's shorthand variants
(`data-checked:`, `data-horizontal:`, `data-open:`…). Any consumer must
declare these **`@custom-variant`s** at its CSS entry (same place as
`dark`) — see `preview/preview.css`. Without them, state/orientation
styles don't apply (invisible slider track, radio/checkbox fills, etc.).
To document for `web/app` adoption.

## Verification

- `pnpm exec tsc --noEmit` — clean
- `pnpm exec vitest run` — **218 tests / 49 files**
- `pnpm run lint` — clean
- `pnpm run build:preview` — builds
- Preview validated section-by-section.

## Out of scope / follow-ups

- **Phase 3** (heavy-dep): calendar (`react-day-picker`), carousel
(`embla`), chart (`recharts`), resizable, sidebar — separate PR(s),
pending a deps decision.
- Consuming the package in `web/app` (the `@custom-variant` contract
above + `@source` + token import).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01H6MfqYq5KJmFo7ydEj5fnn


---

## Size & review notes

**Why one large PR (`size-override` applied):** this is the whole
radix-nova baseline kept as a single reviewable unit — ~53 components +
the 3-tier tokens + the docs catalog — rather than ~50 micro-PRs that
each only make sense together. The bulk is additive component source +
the preview catalog; there's no risky cross-cutting app/runtime logic,
and the heavy-dependency components are split to a follow-up.
Justification per the `size-override` label policy.

**Codex fixes (this PR):**
- **No breaking barrel removal.** `BadgeProps`/`FieldProps`/`AlertProps`
restored as deprecated `ComponentProps` aliases; the full hand-rolled
toast surface (`Toast*`, `Toaster`, `toast`, `useToast`, `dismiss`,
`clearToasts`, `ToastItem`, `ToastOptions`) is retained and
`@deprecated`. **Sonner is additive** — exported as `Sonner` /
`sonnerToast`, so no existing import or `toast({ title })` call site
breaks.
- **`sonner.tsx`** now imports `type CSSProperties` instead of relying
on an ambient `React` namespace.

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

Builds the **full shadcn radix-nova component baseline** for `@zooclaw/design-system`, rendered through `@zooclaw/tokens`. Re-ports the existing components from the canonical radix-nova source and adds the missing primitives, so the package is a complete, internally-consistent component set with ZooClaw's brand (ink-first, brand red as a sparing accent, Liquid-Glass surfaces).

Spec/plan: `docs/superpowers/specs/2026-06-25-zooclaw-ds-radix-nova-baseline-design.md` + `docs/superpowers/plans/2026-06-25-zooclaw-ds-radix-nova-baseline.md`.

**Scope:** only the two DS packages + the spec/plan docs (+ the lockfile for Phase-2 deps). No `web/app`, no services.

## Components (~53)

- **Phase 0 — re-port (16):** button, input, textarea, label, field, checkbox, switch, tooltip, dropdown-menu, dialog, select, badge, card, tabs, accordion, alert (+ the original toast, now superseded).
- **Phase 1 — new primitives (28):** popover, hover-card, alert-dialog, sheet, collapsible, context-menu, menubar, navigation-menu, scroll-area, aspect-ratio, radio-group, slider, toggle, toggle-group, native-select, avatar, skeleton, progress, spinner, kbd, separator, button-group, input-group, pagination, breadcrumb, table, item, empty.
- **Phase 2 — light-dep (4):** command (`cmdk`), drawer (`vaul`), input-otp (`input-otp`), sonner (`sonner`). `sonner` is now the canonical `Toaster`/`toast`; the hand-rolled toast is `@deprecated` + dropped from the barrel.

New deps: `cmdk ^1.1.1`, `vaul ^1.1.2`, `input-otp ^1.4.2`, `sonner ^2.0.7`.

## Tokens & brand rules

- **3-tier tokens** unchanged in shape; refinements this PR:
  - `--zc-wash` neutral so `hover:bg-muted/accent` reads as a visible change (was collapsed onto `--background`).
  - `--ring` = **mid-gray ink** (`--zc-ink-3`), not brand red — a red focus ring read as an error. Red now only on `destructive` / `aria-invalid`.
- **Brand reconciliation** applied per component: `default` button stays dark CTA (not red); selected/checked/range fills use ink; overlays use ZooClaw glass; destructive is the radix-nova soft tint; outline button is transparent (shows its surface).
- **Icons:** lucide/tabler → **Heroicons** throughout (no lucide dep).

## Preview (docs catalog)

Full English preview with a section per component, a complete **Typography** scale (h1–h4 serif, lead/p/blockquote/list/code/large/small/muted/table), and a comprehensive Button showcase (variants, sizes, icon, with-icon, rounded, loading/spinner, nested Button Group, as-child).

## ⚠️ Consumer contract

The components use shadcn radix-nova's shorthand variants (`data-checked:`, `data-horizontal:`, `data-open:`…). Any consumer must declare these **`@custom-variant`s** at its CSS entry (same place as `dark`) — see `preview/preview.css`. Without them, state/orientation styles don't apply (invisible slider track, radio/checkbox fills, etc.). To document for `web/app` adoption.

## Verification

- `pnpm exec tsc --noEmit` — clean
- `pnpm exec vitest run` — **218 tests / 49 files**
- `pnpm run lint` — clean
- `pnpm run build:preview` — builds
- Preview validated section-by-section.

## Out of scope / follow-ups

- **Phase 3** (heavy-dep): calendar (`react-day-picker`), carousel (`embla`), chart (`recharts`), resizable, sidebar — separate PR(s), pending a deps decision.
- Consuming the package in `web/app` (the `@custom-variant` contract above + `@source` + token import).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01H6MfqYq5KJmFo7ydEj5fnn


---

## Size & review notes

**Why one large PR (`size-override` applied):** this is the whole radix-nova baseline kept as a single reviewable unit — ~53 components + the 3-tier tokens + the docs catalog — rather than ~50 micro-PRs that each only make sense together. The bulk is additive component source + the preview catalog; there's no risky cross-cutting app/runtime logic, and the heavy-dependency components are split to a follow-up. Justification per the `size-override` label policy.

**Codex fixes (this PR):**
- **No breaking barrel removal.** `BadgeProps`/`FieldProps`/`AlertProps` restored as deprecated `ComponentProps` aliases; the full hand-rolled toast surface (`Toast*`, `Toaster`, `toast`, `useToast`, `dismiss`, `clearToasts`, `ToastItem`, `ToastOptions`) is retained and `@deprecated`. **Sonner is additive** — exported as `Sonner` / `sonnerToast`, so no existing import or `toast({ title })` call site breaks.
- **`sonner.tsx`** now imports `type CSSProperties` instead of relying on an ambient `React` namespace.



---

## fix(agent-builder): recover recreated builder projects (#2635)

- **SHA**: `6605bb983c290a59b8a1a36672e0ee4b6c5dd9df`
- **作者**: kaka-srp
- **日期**: 2026-06-29T02:54:03Z
- **PR**: #2635

### 完整 Commit Message

```
fix(agent-builder): recover recreated builder projects (#2635)

## Summary
- Fix Agent Builder image attachment crashes by mounting
`ImagePreviewProvider` on the Agent Builder page.
- Recover historical Agent Builder projects after bot recreation when a
submitted/share/published pack artifact exists.
- Mark unrecoverable recreated-bot historical projects with a clear
archive instruction when no artifact exists.

## Root cause
Two separate staging failure modes were involved:

1. Historical Agent Builder messages with image attachments triggered
`useImagePreview()`, but the Agent Builder route did not provide
`ImagePreviewProvider`. Sentry showed `useImagePreview must be used
within ImagePreviewProvider` on the Agent Builder route.
2. After a user recreated the bot, old Agent Builder project records
could still point at the deleted old bot runtime. Workspace
materialization then called the stale bot runtime `/runtime/exec` and
got 404.

Linear:
https://linear.app/srpone/issue/ECA-1126/fix-agent-builder-recovery-crashes

## Test plan
- [x] `pnpm test:unit tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] `pnpm exec eslint
src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx
tests/unit/app/agent-builder-client.unit.spec.tsx --quiet`
- [x] `.venv/bin/pytest tests/unit/test_agent_builder_service.py`
- [x] `.venv/bin/pytest tests/unit/test_agent_builder_service.py -k
'recreated_runtime or
import_project_source_uses_recovered_builder_after_recreated_runtime or
import_submitted_pack_source_regenerates_presigned_url'`
- [x] `.venv/bin/ruff check app/services/agent_builder_service.py
tests/unit/test_agent_builder_service.py`
- [x] `.venv/bin/ruff format --check
app/services/agent_builder_service.py
tests/unit/test_agent_builder_service.py`
- [x] `/opt/homebrew/bin/pyright --pythonpath .venv/bin/python
app/services/agent_builder_service.py
tests/unit/test_agent_builder_service.py`
- [x] `git diff --check`

## Notes
- A previous full frontend `tsc` attempt failed before dependency
refresh because local `web/app/node_modules` was missing existing
workspace/dependency links (`@zooclaw/auth-client`, `ldrs/react`). That
was an environment/install issue, not introduced by this PR.
```

### PR Body

## Summary
- Fix Agent Builder image attachment crashes by mounting `ImagePreviewProvider` on the Agent Builder page.
- Recover historical Agent Builder projects after bot recreation when a submitted/share/published pack artifact exists.
- Mark unrecoverable recreated-bot historical projects with a clear archive instruction when no artifact exists.

## Root cause
Two separate staging failure modes were involved:

1. Historical Agent Builder messages with image attachments triggered `useImagePreview()`, but the Agent Builder route did not provide `ImagePreviewProvider`. Sentry showed `useImagePreview must be used within ImagePreviewProvider` on the Agent Builder route.
2. After a user recreated the bot, old Agent Builder project records could still point at the deleted old bot runtime. Workspace materialization then called the stale bot runtime `/runtime/exec` and got 404.

Linear: https://linear.app/srpone/issue/ECA-1126/fix-agent-builder-recovery-crashes

## Test plan
- [x] `pnpm test:unit tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] `pnpm exec eslint src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx tests/unit/app/agent-builder-client.unit.spec.tsx --quiet`
- [x] `.venv/bin/pytest tests/unit/test_agent_builder_service.py`
- [x] `.venv/bin/pytest tests/unit/test_agent_builder_service.py -k 'recreated_runtime or import_project_source_uses_recovered_builder_after_recreated_runtime or import_submitted_pack_source_regenerates_presigned_url'`
- [x] `.venv/bin/ruff check app/services/agent_builder_service.py tests/unit/test_agent_builder_service.py`
- [x] `.venv/bin/ruff format --check app/services/agent_builder_service.py tests/unit/test_agent_builder_service.py`
- [x] `/opt/homebrew/bin/pyright --pythonpath .venv/bin/python app/services/agent_builder_service.py tests/unit/test_agent_builder_service.py`
- [x] `git diff --check`

## Notes
- A previous full frontend `tsc` attempt failed before dependency refresh because local `web/app/node_modules` was missing existing workspace/dependency links (`@zooclaw/auth-client`, `ldrs/react`). That was an environment/install issue, not introduced by this PR.

