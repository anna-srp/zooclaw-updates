# ecap-workspace commits for 2026-06-05

## de639257 - Chris@ZooClaw - 2026-06-05T11:57:02Z
```
docs(web): set zustand/motion/react-query/usehooks-ts as default frontend libs (#2230)

## What

Two edits to `web/app/CLAUDE.md` (the real file is `web/app/AGENTS.md`;
CLAUDE.md symlinks to it).

### 1. Add `## 默认技术选型 (first-choice libraries)`
A single decision rule mapping each cross-cutting frontend concern to
its default library, so new code doesn't reinvent these and old code has
a clear migration target:

| 问题域 | 默认 | 替代掉 |
|---|---|---|
| 服务端数据 / session cache | `@tanstack/react-query@^5` | 手写 fetch + 缓存 |
| 跨组件状态 / event 派发 | `zustand@^5` (vanilla split) | `dispatchEvent` +
listener |
| 动效 / 过渡 | `motion@^12` (`motion/react`) |
`mount→RAF→setState`、`framer-motion` 旧包名 |
| DOM / 浏览器 hook | `usehooks-ts@3.x` | 手写 `useEffect` +
add/removeEventListener |

react-query and zustand already had deep sections (cross-linked);
**motion and usehooks-ts were undocumented** as defaults — that's the
new signal. All four verified against `package.json` + live imports.

### 2. Strip issue-execution-progress
Removed per-PR / epic-progress narratives (epic #1363–#1369
enumerations, "#1865/#1867/#1990 review-fix loops", "PR 2/3 of that
epic", etc.) while **keeping** the design rationale (root causes,
rephrased) and forward trackers (open issues like `#1997`). Execution
progress ages into noise; rules and rationale don't.

Net: **+13 / −6 lines**, docs only.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
**PR Body:**
## What

Two edits to `web/app/CLAUDE.md` (the real file is `web/app/AGENTS.md`; CLAUDE.md symlinks to it).

### 1. Add `## 默认技术选型 (first-choice libraries)`
A single decision rule mapping each cross-cutting frontend concern to its default library, so new code doesn't reinvent these and old code has a clear migration target:

| 问题域 | 默认 | 替代掉 |
|---|---|---|
| 服务端数据 / session cache | `@tanstack/react-query@^5` | 手写 fetch + 缓存 |
| 跨组件状态 / event 派发 | `zustand@^5` (vanilla split) | `dispatchEvent` + listener |
| 动效 / 过渡 | `motion@^12` (`motion/react`) | `mount→RAF→setState`、`framer-motion` 旧包名 |
| DOM / 浏览器 hook | `usehooks-ts@3.x` | 手写 `useEffect` + add/removeEventListener |

react-query and zustand already had deep sections (cross-linked); **motion and usehooks-ts were undocumented** as defaults — that's the new signal. All four verified against `package.json` + live imports.

### 2. Strip issue-execution-progress
Removed per-PR / epic-progress narratives (epic #1363–#1369 enumerations, "#1865/#1867/#1990 review-fix loops", "PR 2/3 of that epic", etc.) while **keeping** the design rationale (root causes, rephrased) and forward trackers (open issues like `#1997`). Execution progress ages into noise; rules and rationale don't.

Net: **+13 / −6 lines**, docs only.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## a77b89b5 - rayhuang198212 - 2026-06-05T11:05:29Z
```
test(web): stabilize e2e chat and agents flows (#2212)

## Summary
- Stabilize web E2E coverage for the current PandaClaw / Agent Studio
runtime by moving chat lifecycle, streaming, actions, subagent, and
error-handling specs onto the unified chat flow.
- Add shared E2E helpers for hiring/firing agents, opening agent chat,
suppressing known overlays, and cleaning up hired-agent state after
tests.
- Add a Claw Settings page object and refactor settings specs to use
locale-free navigation with English locale cookies.
- Update agents-manager and publish-flow specs to use fresh pages,
stronger assertions, deterministic cleanup, and current UI selectors.
- Remove deprecated example-card chat coverage that no longer matches
the current runtime.

## Test plan
- [ ] `cd web/app && pnpm test:e2e`
- [ ] `cd web && pnpm lint:ci`

## Why this PR exceeds the usual size limitation
Because it is a coordinated E2E refactor. The PandaClaw page object
changed at the foundation layer, so the dependent chat/runtime specs had
to move with it. Splitting the page-object change from the spec updates
would leave the suite in a partially migrated state and make the
refactor incomplete.
```
**PR Body:**
## Summary
- Stabilize web E2E coverage for the current PandaClaw / Agent Studio runtime by moving chat lifecycle, streaming, actions, subagent, and error-handling specs onto the unified chat flow.
- Add shared E2E helpers for hiring/firing agents, opening agent chat, suppressing known overlays, and cleaning up hired-agent state after tests.
- Add a Claw Settings page object and refactor settings specs to use locale-free navigation with English locale cookies.
- Update agents-manager and publish-flow specs to use fresh pages, stronger assertions, deterministic cleanup, and current UI selectors.
- Remove deprecated example-card chat coverage that no longer matches the current runtime.

## Test plan
- [ ] `cd web/app && pnpm test:e2e`
- [ ] `cd web && pnpm lint:ci`

## Why this PR exceeds the usual size limitation
Because it is a coordinated E2E refactor. The PandaClaw page object changed at the foundation layer, so the dependent chat/runtime specs had to move with it. Splitting the page-object change from the spec updates would leave the suite in a partially migrated state and make the refactor incomplete.

## e7da55f3 - Chris@ZooClaw - 2026-06-05T11:01:53Z
```
ci(auto-review): give Codex reviewer the srp-codex App identity (#2228)

## What

Wire the `srp-codex` GitHub App into Codex review. Passes `CODEX_APP_ID`
/
`CODEX_APP_PRIVATE_KEY` to the `codex-review.yaml` reusable so Codex
posts its
PR reviews and verdict labels as **`srp-codex[bot]`** via an App token,
instead
of the generic `github-actions[bot]` under the default `GITHUB_TOKEN`.

This removes the Claude/Codex identity asymmetry — `claude-review`
already runs
under a dedicated App (`srp-claude-assistant`).

## Depends on

- srp-actions#93 (merged) — declares the two optional secrets and routes
every
Codex GitHub write through the App token, falling back to `GITHUB_TOKEN`
when
  unset.

## This PR is its own live test

The auto-review run on this PR exercises the new path end-to-end.
Expected:
- Codex's review comment is authored by `srp-codex[bot]`.
- On a re-push, the prior Codex review folds to OUTDATED (validates the
  de-hardcoded author filter from srp-actions#93).
- No startup_failure (secret declarations align across caller and
reusable).

## Spec

`docs/superpowers/specs/2026-06-05-codex-reviewer-app-identity.md` —
full
cross-repo rollout, the App permission set, and the deferred follow-up
(tightening the repo default `GITHUB_TOKEN` to read-only).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- codesmith:footer -->
---
<a
href="https://app.blacksmith.sh/SerendipityOneInc/codesmith/ecap-workspace/pr/2228"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img
alt="View with Codesmith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a>
<a
href="https://backend.blacksmith.sh/track/enable-autofix?expires=1783247699&installation_id=138111599&pr_number=2228&repository=SerendipityOneInc%2Fecap-workspace&return_to=https%3A%2F%2Fgithub.com%2FSerendipityOneInc%2Fecap-workspace%2Fpull%2F2228&signature=3a77fa1a32f913b82199761a67d84e9175fb8aa0e91ad8e8f1211705d61f9769"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img
alt="Autofix with Codesmith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith</code> with what you
need. Autofix is disabled.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```
**PR Body:**
## What

Wire the `srp-codex` GitHub App into Codex review. Passes `CODEX_APP_ID` /
`CODEX_APP_PRIVATE_KEY` to the `codex-review.yaml` reusable so Codex posts its
PR reviews and verdict labels as **`srp-codex[bot]`** via an App token, instead
of the generic `github-actions[bot]` under the default `GITHUB_TOKEN`.

This removes the Claude/Codex identity asymmetry — `claude-review` already runs
under a dedicated App (`srp-claude-assistant`).

## Depends on

- srp-actions#93 (merged) — declares the two optional secrets and routes every
  Codex GitHub write through the App token, falling back to `GITHUB_TOKEN` when
  unset.

## This PR is its own live test

The auto-review run on this PR exercises the new path end-to-end. Expected:
- Codex's review comment is authored by `srp-codex[bot]`.
- On a re-push, the prior Codex review folds to OUTDATED (validates the
  de-hardcoded author filter from srp-actions#93).
- No startup_failure (secret declarations align across caller and reusable).

## Spec

`docs/superpowers/specs/2026-06-05-codex-reviewer-app-identity.md` — full
cross-repo rollout, the App permission set, and the deferred follow-up
(tightening the repo default `GITHUB_TOKEN` to read-only).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- codesmith:footer -->
---
<a href="https://app.blacksmith.sh/SerendipityOneInc/codesmith/ecap-workspace/pr/2228"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source media="(prefers-color-scheme: light)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img alt="View with Codesmith" src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a> <a href="https://backend.blacksmith.sh/track/enable-autofix?expires=1783247699&installation_id=138111599&pr_number=2228&repository=SerendipityOneInc%2Fecap-workspace&return_to=https%3A%2F%2Fgithub.com%2FSerendipityOneInc%2Fecap-workspace%2Fpull%2F2228&signature=3a77fa1a32f913b82199761a67d84e9175fb8aa0e91ad8e8f1211705d61f9769"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source media="(prefers-color-scheme: light)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img alt="Autofix with Codesmith" src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith</code> with what you need. Autofix is disabled.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->

## b896f759 - kaka-srp - 2026-06-05T10:05:27Z
```
fix(billing): sync model access from v2 profiles (#2226)

## Summary
- Sync LiteLLM key/team model access from Billing v2 profiles only;
legacy ecap-account key/team fields are no longer authoritative.
- Pass/load Billing v2 profiles through fulfillment, subscription-code,
Stripe/cron/Apple sync paths so model access uses the correct
billing_key and team_id; subscription-code upgrades now return a typed
503 when the v2 profile is not ready.
- Return /users/credits/check no_subscription for v2
free/expired/canceled users without a ready profile, while preserving
503 for active/non-terminal not-ready profiles.

## Root cause
Model access sync still read deprecated ecap-account billing fields, so
plan upgrades could leave LiteLLM key/team model groups stale after the
v2 migration. Separately, credits/check classified terminal
no-subscription v2 users with unready profiles as billing_not_ready
before reaching Billing Gateway.

## Test plan
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check .
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pyright app tests
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_litellm_model_access.py
tests/unit/test_stripe_billing_gateway.py
tests/unit/test_subscription_code.py
tests/unit/test_subscription_expiry.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_user_credits.py
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_litellm_model_access.py
tests/unit/test_stripe_billing_gateway.py
tests/unit/test_subscription_code.py
tests/unit/test_subscription_expiry.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_user_credits.py
tests/unit/test_apple_subscription_manager.py
tests/unit/test_apple_routes.py
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check
app/services/subscription_code.py app/services/stripe/billing_gateway.py
app/services/subscription_expiry.py app/cron/subscription_cron.py
app/routes/apple.py app/services/apple_subscription_manager.py
tests/unit/test_subscription_code.py
tests/unit/test_litellm_model_access.py
tests/unit/test_stripe_billing_gateway.py
tests/unit/test_subscription_expiry.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_user_credits.py
tests/unit/test_apple_subscription_manager.py
tests/unit/test_apple_routes.py
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pyright
app/services/subscription_code.py app/services/stripe/billing_gateway.py
app/services/subscription_expiry.py app/cron/subscription_cron.py
app/routes/apple.py app/services/apple_subscription_manager.py
tests/unit/test_subscription_code.py
tests/unit/test_litellm_model_access.py
tests/unit/test_stripe_billing_gateway.py
tests/unit/test_subscription_expiry.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_user_credits.py
tests/unit/test_apple_subscription_manager.py
tests/unit/test_apple_routes.py
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pyright
app/errors/__init__.py app/services/subscription_code.py
tests/unit/test_subscription_code.py
- [x] cd services/claw-interface && scripts/ci-lint/03-complexity.sh
- [ ] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest --cov=app
--cov-report=term-missing --cov-fail-under=90 -q (local full suite
failed in unrelated OpenClaw/Mattermost-isolation tests: 3 failed, 2
errors; coverage reported 88.20% < 90%)

## Linear
-
https://linear.app/srpone/issue/ECA-903/fix-billing-v2-model-access-sync
```
**PR Body:**
## Summary
- Sync LiteLLM key/team model access from Billing v2 profiles only; legacy ecap-account key/team fields are no longer authoritative.
- Pass/load Billing v2 profiles through fulfillment, subscription-code, Stripe/cron/Apple sync paths so model access uses the correct billing_key and team_id; subscription-code upgrades now return a typed 503 when the v2 profile is not ready.
- Return /users/credits/check no_subscription for v2 free/expired/canceled users without a ready profile, while preserving 503 for active/non-terminal not-ready profiles.

## Root cause
Model access sync still read deprecated ecap-account billing fields, so plan upgrades could leave LiteLLM key/team model groups stale after the v2 migration. Separately, credits/check classified terminal no-subscription v2 users with unready profiles as billing_not_ready before reaching Billing Gateway.

## Test plan
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check .
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pyright app tests
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_litellm_model_access.py tests/unit/test_stripe_billing_gateway.py tests/unit/test_subscription_code.py tests/unit/test_subscription_expiry.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_user_credits.py
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_litellm_model_access.py tests/unit/test_stripe_billing_gateway.py tests/unit/test_subscription_code.py tests/unit/test_subscription_expiry.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_user_credits.py tests/unit/test_apple_subscription_manager.py tests/unit/test_apple_routes.py
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check app/services/subscription_code.py app/services/stripe/billing_gateway.py app/services/subscription_expiry.py app/cron/subscription_cron.py app/routes/apple.py app/services/apple_subscription_manager.py tests/unit/test_subscription_code.py tests/unit/test_litellm_model_access.py tests/unit/test_stripe_billing_gateway.py tests/unit/test_subscription_expiry.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_user_credits.py tests/unit/test_apple_subscription_manager.py tests/unit/test_apple_routes.py
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pyright app/services/subscription_code.py app/services/stripe/billing_gateway.py app/services/subscription_expiry.py app/cron/subscription_cron.py app/routes/apple.py app/services/apple_subscription_manager.py tests/unit/test_subscription_code.py tests/unit/test_litellm_model_access.py tests/unit/test_stripe_billing_gateway.py tests/unit/test_subscription_expiry.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_user_credits.py tests/unit/test_apple_subscription_manager.py tests/unit/test_apple_routes.py
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pyright app/errors/__init__.py app/services/subscription_code.py tests/unit/test_subscription_code.py
- [x] cd services/claw-interface && scripts/ci-lint/03-complexity.sh
- [ ] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q (local full suite failed in unrelated OpenClaw/Mattermost-isolation tests: 3 failed, 2 errors; coverage reported 88.20% < 90%)

## Linear
- https://linear.app/srpone/issue/ECA-903/fix-billing-v2-model-access-sync

## 225f75d7 - Chris@ZooClaw - 2026-06-05T10:03:38Z
```
ci: migrate workflows to Blacksmith runners (#2227)

Re-open of #2221 under a human author so the auto-review actor-trust
gate runs.
The original PR was authored by `blacksmith-sh[bot]`, which is not in
the
reviewers' `allowed_bots` list — both `claude-review` and `codex-review`
hard-fail
before invoking the model ("Workflow initiated by non-human actor").
Same commits,
human author.

---

This PR has been automatically generated using Blacksmith's Migration
Wizard:

1. Selected workflows now run on Blacksmith's faster hardware (e.g.
`runs-on: blacksmith-4vcpu-ubuntu-2204`).
2. Jobs on Blacksmith use Blacksmith's colocated actions cache.
3. Improved GitHub Actions observability / logging.
4. Docker builds share Docker layer cache.

<!-- codesmith:footer -->
---
<a
href="https://app.blacksmith.sh/SerendipityOneInc/codesmith/ecap-workspace/pr/2227"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img
alt="View with Codesmith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a>
<a
href="https://backend.blacksmith.sh/track/enable-autofix?expires=1783245413&installation_id=138111599&pr_number=2227&repository=SerendipityOneInc%2Fecap-workspace&return_to=https%3A%2F%2Fgithub.com%2FSerendipityOneInc%2Fecap-workspace%2Fpull%2F2227&signature=331d52a53d220e5146b0fda6afa01f2e057d526ccd728d8089535da53c8deb16"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img
alt="Autofix with Codesmith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith</code> with what you
need. Autofix is disabled.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->

Co-authored-by: blacksmith-sh[bot] <157653362+blacksmith-sh[bot]@users.noreply.github.com>
```
**PR Body:**
Re-open of #2221 under a human author so the auto-review actor-trust gate runs.
The original PR was authored by `blacksmith-sh[bot]`, which is not in the
reviewers' `allowed_bots` list — both `claude-review` and `codex-review` hard-fail
before invoking the model ("Workflow initiated by non-human actor"). Same commits,
human author.

---

This PR has been automatically generated using Blacksmith's Migration Wizard:

1. Selected workflows now run on Blacksmith's faster hardware (e.g. `runs-on: blacksmith-4vcpu-ubuntu-2204`).
2. Jobs on Blacksmith use Blacksmith's colocated actions cache.
3. Improved GitHub Actions observability / logging.
4. Docker builds share Docker layer cache.

<!-- codesmith:footer -->
---
<a href="https://app.blacksmith.sh/SerendipityOneInc/codesmith/ecap-workspace/pr/2227"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source media="(prefers-color-scheme: light)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img alt="View with Codesmith" src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a> <a href="https://backend.blacksmith.sh/track/enable-autofix?expires=1783245413&installation_id=138111599&pr_number=2227&repository=SerendipityOneInc%2Fecap-workspace&return_to=https%3A%2F%2Fgithub.com%2FSerendipityOneInc%2Fecap-workspace%2Fpull%2F2227&signature=331d52a53d220e5146b0fda6afa01f2e057d526ccd728d8089535da53c8deb16"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source media="(prefers-color-scheme: light)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img alt="Autofix with Codesmith" src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith</code> with what you need. Autofix is disabled.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->

## cc9d6324 - bill-srp - 2026-06-05T09:30:02Z
```
refactor(claw-interface): stop legacy OpenClaw bot reads (#2224)

## Summary
- Route remaining business Mattermost bot reads through the V2 runtime
projection backed by agent workspaces.
- Stop using legacy `account.openclaw_bots` to locate Mattermost bot
state during provision, reconcile, and cleanup paths.
- Keep legacy account array writes/materialization only as
compatibility/backfill support while reads use ZooClaw computers and
agent workspaces.

## Test plan
- [x] `docker exec ecap-workspace-claw-interface-bill bash -lc 'cd
/workspaces/ecap-workspace-claw-interface/services/claw-interface &&
source /home/node/.venvs/claw-interface/bin/activate && ruff check . &&
pyright app tests && pytest tests/unit/test_agent_mm_state_service.py
tests/unit/test_mattermost_reconcile.py
tests/unit/test_agent_mm_wiring.py
tests/unit/test_mattermost_provisioner.py
tests/unit/test_openclaw_routes.py
tests/unit/test_openclaw_settings_routes.py
tests/unit/test_openclaw_agents.py -q'`
- [x] `docker exec ecap-workspace-claw-interface-bill bash -lc 'cd
/workspaces/ecap-workspace-claw-interface/services/claw-interface &&
source /home/node/.venvs/claw-interface/bin/activate && ruff check . &&
pyright app tests'`
- [ ] `docker exec ecap-workspace-claw-interface-bill bash -lc 'cd
/workspaces/ecap-workspace-claw-interface/services/claw-interface &&
source /home/node/.venvs/claw-interface/bin/activate && pytest --cov=app
--cov-report=term-missing --cov-fail-under=90 -q'` failed locally: 4660
passed, 2 deptry test failures because the devcontainer cannot resolve
the host git worktree path
(`/Users/bill/Github/StarQuestAI/ecap-workspace/.git/worktrees/ecap-workspace-claw-interface`),
then coverage reported 88.33% below the 90% gate.

<!-- codesmith:footer -->
---
<a
href="https://app.blacksmith.sh/SerendipityOneInc/codesmith/ecap-workspace/pr/2224"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img
alt="View with Codesmith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a>
<a
href="https://backend.blacksmith.sh/track/enable-autofix?expires=1783234506&installation_id=138111599&pr_number=2224&repository=SerendipityOneInc%2Fecap-workspace&return_to=https%3A%2F%2Fgithub.com%2FSerendipityOneInc%2Fecap-workspace%2Fpull%2F2224&signature=391c0a1dee7c504306124efe78b013f24c480bc4a8918b35d5fbbea39e4c5cb7"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img
alt="Autofix with Codesmith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith</code> with what you
need. Autofix is disabled.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->
```
**PR Body:**
## Summary
- Route remaining business Mattermost bot reads through the V2 runtime projection backed by agent workspaces.
- Stop using legacy `account.openclaw_bots` to locate Mattermost bot state during provision, reconcile, and cleanup paths.
- Keep legacy account array writes/materialization only as compatibility/backfill support while reads use ZooClaw computers and agent workspaces.

## Test plan
- [x] `docker exec ecap-workspace-claw-interface-bill bash -lc 'cd /workspaces/ecap-workspace-claw-interface/services/claw-interface && source /home/node/.venvs/claw-interface/bin/activate && ruff check . && pyright app tests && pytest tests/unit/test_agent_mm_state_service.py tests/unit/test_mattermost_reconcile.py tests/unit/test_agent_mm_wiring.py tests/unit/test_mattermost_provisioner.py tests/unit/test_openclaw_routes.py tests/unit/test_openclaw_settings_routes.py tests/unit/test_openclaw_agents.py -q'`
- [x] `docker exec ecap-workspace-claw-interface-bill bash -lc 'cd /workspaces/ecap-workspace-claw-interface/services/claw-interface && source /home/node/.venvs/claw-interface/bin/activate && ruff check . && pyright app tests'`
- [ ] `docker exec ecap-workspace-claw-interface-bill bash -lc 'cd /workspaces/ecap-workspace-claw-interface/services/claw-interface && source /home/node/.venvs/claw-interface/bin/activate && pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q'` failed locally: 4660 passed, 2 deptry test failures because the devcontainer cannot resolve the host git worktree path (`/Users/bill/Github/StarQuestAI/ecap-workspace/.git/worktrees/ecap-workspace-claw-interface`), then coverage reported 88.33% below the 90% gate.

<!-- codesmith:footer -->
---
<a href="https://app.blacksmith.sh/SerendipityOneInc/codesmith/ecap-workspace/pr/2224"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source media="(prefers-color-scheme: light)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img alt="View with Codesmith" src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a> <a href="https://backend.blacksmith.sh/track/enable-autofix?expires=1783234506&installation_id=138111599&pr_number=2224&repository=SerendipityOneInc%2Fecap-workspace&return_to=https%3A%2F%2Fgithub.com%2FSerendipityOneInc%2Fecap-workspace%2Fpull%2F2224&signature=391c0a1dee7c504306124efe78b013f24c480bc4a8918b35d5fbbea39e4c5cb7"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source media="(prefers-color-scheme: light)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img alt="Autofix with Codesmith" src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith</code> with what you need. Autofix is disabled.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->

## a9b03b9d - bill-srp - 2026-06-05T09:00:49Z
```
feat(dashboard-console): add vertical pack plans management UI (#2225)

## Linear

https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary
Adds the **vertical pack plans** management surface to the
`dashboard-console` app — a global catalog of product bundles that group
included agent packs with optional paid add-on agents. Frontend-only;
the internal CRUD API already shipped in #2219.

- **Page + data layer:** new `/vertical-pack-plans` route and sidebar
entry, card-framed table, empty/loading states, and create/edit/delete
dialogs. MVVM split (pure helpers + TanStack Query read model +
view-model hook). Client calls `/internal/vertical-pack-plans` with the
same live/seed fallback as agent-packs — admin auth/CORS is still gated
by ECA-886, so it serves seed data until that lands.
- **Agent picker drawer:** right-slide `Sheet` with checkbox
multi-select + search, applied on a "Done" confirm. Included agents
render as removable chips; add-ons as drawer-picked rows with a per-row
price input. Catalog-pick-only (no free-typed ids); unknown ids are
preserved as raw chips/rows (no silent data loss).
- **Mutual exclusion:** a pack can be either included or an add-on, not
both — cross-selected packs are disabled (greyed, unclickable) in the
other field's drawer.
- **Readable list:** the table resolves agent pack ids to friendly pack
names (raw id fallback), matching the modal chips.

## Test plan
- [x] `pnpm test` (117 unit/component tests), `pnpm tsc`, `pnpm lint` —
all green locally
- [ ] CI `code-quality / lint-and-test` passes
- [ ] Create a plan; add included + add-on agents via the drawer;
confirm a pack chosen in one field is disabled in the other
- [ ] Edit then delete a plan; verify chips/rows show friendly names and
an unknown id falls back to the raw id
- [ ] Backend unreachable → page shows the seed-data banner and stays
interactive (local-only mutations)

<!-- codesmith:footer -->
---
<a
href="https://app.blacksmith.sh/SerendipityOneInc/codesmith/ecap-workspace/pr/2225"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img
alt="View with Codesmith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a>
<a
href="https://backend.blacksmith.sh/track/enable-autofix?expires=1783237160&installation_id=138111599&pr_number=2225&repository=SerendipityOneInc%2Fecap-workspace&return_to=https%3A%2F%2Fgithub.com%2FSerendipityOneInc%2Fecap-workspace%2Fpull%2F2225&signature=c4c27b5147cbd9769c224855c492e97433c3d06f2c1ca3fe50b657e70f2b4460"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img
alt="Autofix with Codesmith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith</code> with what you
need. Autofix is disabled.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->
```
**PR Body:**
## Linear
https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary
Adds the **vertical pack plans** management surface to the `dashboard-console` app — a global catalog of product bundles that group included agent packs with optional paid add-on agents. Frontend-only; the internal CRUD API already shipped in #2219.

- **Page + data layer:** new `/vertical-pack-plans` route and sidebar entry, card-framed table, empty/loading states, and create/edit/delete dialogs. MVVM split (pure helpers + TanStack Query read model + view-model hook). Client calls `/internal/vertical-pack-plans` with the same live/seed fallback as agent-packs — admin auth/CORS is still gated by ECA-886, so it serves seed data until that lands.
- **Agent picker drawer:** right-slide `Sheet` with checkbox multi-select + search, applied on a "Done" confirm. Included agents render as removable chips; add-ons as drawer-picked rows with a per-row price input. Catalog-pick-only (no free-typed ids); unknown ids are preserved as raw chips/rows (no silent data loss).
- **Mutual exclusion:** a pack can be either included or an add-on, not both — cross-selected packs are disabled (greyed, unclickable) in the other field's drawer.
- **Readable list:** the table resolves agent pack ids to friendly pack names (raw id fallback), matching the modal chips.

## Test plan
- [x] `pnpm test` (117 unit/component tests), `pnpm tsc`, `pnpm lint` — all green locally
- [ ] CI `code-quality / lint-and-test` passes
- [ ] Create a plan; add included + add-on agents via the drawer; confirm a pack chosen in one field is disabled in the other
- [ ] Edit then delete a plan; verify chips/rows show friendly names and an unknown id falls back to the raw id
- [ ] Backend unreachable → page shows the seed-data banner and stays interactive (local-only mutations)

<!-- codesmith:footer -->
---
<a href="https://app.blacksmith.sh/SerendipityOneInc/codesmith/ecap-workspace/pr/2225"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source media="(prefers-color-scheme: light)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img alt="View with Codesmith" src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a> <a href="https://backend.blacksmith.sh/track/enable-autofix?expires=1783237160&installation_id=138111599&pr_number=2225&repository=SerendipityOneInc%2Fecap-workspace&return_to=https%3A%2F%2Fgithub.com%2FSerendipityOneInc%2Fecap-workspace%2Fpull%2F2225&signature=c4c27b5147cbd9769c224855c492e97433c3d06f2c1ca3fe50b657e70f2b4460"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source media="(prefers-color-scheme: light)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img alt="Autofix with Codesmith" src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith</code> with what you need. Autofix is disabled.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->

## 7a8216ae - bill-srp - 2026-06-05T03:44:22Z
```
fix(openclaw): read bot state from v2 computers (#2220)

## Summary
- Reserve primary bot creation in ZooClawComputer state before calling
FastClaw, preventing duplicate bot creates during concurrent init.
- Switch OpenClaw bot/Mattermost runtime reads away from legacy account
openclaw_bots and onto V2 computer/runtime state.
- Keep compatibility writes to legacy openclaw_bots while updating tests
for the V2 read contract.

## Root cause
Legacy account openclaw_bots could be stale or empty while V2
computer/runtime state was authoritative, so read paths could select the
wrong bot or re-enrich sparse V2 payloads from stale account data.
Concurrent init also needed a V2 reservation before platform bot
creation to avoid duplicate FastClaw creates.

## Test plan
- [x] Devcontainer: ruff check on touched backend/test files
- [x] Devcontainer: pytest tests/unit/test_bot_state_service.py
tests/unit/test_openclaw_admin_routes.py
tests/unit/test_openclaw_routes.py -q
```
**PR Body:**
## Summary
- Reserve primary bot creation in ZooClawComputer state before calling FastClaw, preventing duplicate bot creates during concurrent init.
- Switch OpenClaw bot/Mattermost runtime reads away from legacy account openclaw_bots and onto V2 computer/runtime state.
- Keep compatibility writes to legacy openclaw_bots while updating tests for the V2 read contract.

## Root cause
Legacy account openclaw_bots could be stale or empty while V2 computer/runtime state was authoritative, so read paths could select the wrong bot or re-enrich sparse V2 payloads from stale account data. Concurrent init also needed a V2 reservation before platform bot creation to avoid duplicate FastClaw creates.

## Test plan
- [x] Devcontainer: ruff check on touched backend/test files
- [x] Devcontainer: pytest tests/unit/test_bot_state_service.py tests/unit/test_openclaw_admin_routes.py tests/unit/test_openclaw_routes.py -q


## 57632aa0 - sam-srp - 2026-06-05T03:39:02Z
```
fix(claw-interface): close Redis client on shutdown (#2222)

## Summary
- add an explicit `close_redis()` teardown for the shared async Redis
singleton
- call Redis teardown during FastAPI shutdown before the event loop
exits
- cover Redis close/reset behavior and shutdown wiring in unit tests

## Verification
- `conda run -n base pytest tests/unit/test_redis_client.py -q`
- `conda run -n base python -m py_compile app/services/redis_client.py
app/lifetime.py tests/unit/test_redis_client.py
tests/unit/test_lifetime.py`
- `git diff --check`

Note: full `tests/unit/test_lifetime.py` is blocked locally by missing
`stripe` in the base conda environment during `app.scheduler` import,
before this change is exercised.

Closes ECA-891

<!-- codesmith:footer -->
---
<a
href="https://app.blacksmith.sh/SerendipityOneInc/codesmith/ecap-workspace/pr/2222"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img
alt="View with Codesmith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a>
<a
href="https://backend.blacksmith.sh/track/enable-autofix?expires=1783221164&installation_id=138111599&pr_number=2222&repository=SerendipityOneInc%2Fecap-workspace&return_to=https%3A%2F%2Fgithub.com%2FSerendipityOneInc%2Fecap-workspace%2Fpull%2F2222&signature=1e4467eb585b78eb9f0052e01d91737c84e478a5180220c14edb29c492518389"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img
alt="Autofix with Codesmith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith</code> with what you
need. Autofix is disabled.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->
```
**PR Body:**
## Summary
- add an explicit `close_redis()` teardown for the shared async Redis singleton
- call Redis teardown during FastAPI shutdown before the event loop exits
- cover Redis close/reset behavior and shutdown wiring in unit tests

## Verification
- `conda run -n base pytest tests/unit/test_redis_client.py -q`
- `conda run -n base python -m py_compile app/services/redis_client.py app/lifetime.py tests/unit/test_redis_client.py tests/unit/test_lifetime.py`
- `git diff --check`

Note: full `tests/unit/test_lifetime.py` is blocked locally by missing `stripe` in the base conda environment during `app.scheduler` import, before this change is exercised.

Closes ECA-891

<!-- codesmith:footer -->
---
<a href="https://app.blacksmith.sh/SerendipityOneInc/codesmith/ecap-workspace/pr/2222"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source media="(prefers-color-scheme: light)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img alt="View with Codesmith" src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a> <a href="https://backend.blacksmith.sh/track/enable-autofix?expires=1783221164&installation_id=138111599&pr_number=2222&repository=SerendipityOneInc%2Fecap-workspace&return_to=https%3A%2F%2Fgithub.com%2FSerendipityOneInc%2Fecap-workspace%2Fpull%2F2222&signature=1e4467eb585b78eb9f0052e01d91737c84e478a5180220c14edb29c492518389"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source media="(prefers-color-scheme: light)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img alt="Autofix with Codesmith" src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith</code> with what you need. Autofix is disabled.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->

## 06fc4cc3 - kaka-srp - 2026-06-05T03:32:39Z
```
fix(stripe): ignore stale terminal subscription webhooks (#2223)

## Summary
- Ignore stale Stripe invoice.payment_failed events when the local
subscription agreement is already terminal.
- Ignore customer.subscription.updated snapshots after a terminal local
agreement, while keeping deleted/canceled idempotency intact.
- Add record-level and adapter-level regression tests for the ECA-901
webhook retry case.

## Root cause
Stripe can deliver or retry invoice/subscription facts after a
subscription has already been canceled locally. The Billing v2 state
machine correctly rejects terminal-to-live transitions such as canceled
-> past_due, but the Stripe webhook adapter treated that stale provider
fact as an exception, returning 500 and causing retries.

## Test plan
- [x] source /home/node/.venvs/claw-interface/bin/activate && pytest
services/claw-interface/tests/unit/test_billing_v2_provider_records.py
services/claw-interface/tests/unit/test_stripe_billing_v2.py -q
- [x] source /home/node/.venvs/claw-interface/bin/activate && ruff check
.
- [x] source /home/node/.venvs/claw-interface/bin/activate && pyright
app tests
- [ ] source /home/node/.venvs/claw-interface/bin/activate && pytest
--cov=app --cov-report=term-missing --cov-fail-under=90 -q (stopped at
63% passing per request)

Linear:
https://linear.app/srpone/issue/ECA-901/stripe-webhook-rejects-canceled-past-due-subscription-state-transition

<!-- codesmith:footer -->
---
<a
href="https://app.blacksmith.sh/SerendipityOneInc/codesmith/ecap-workspace/pr/2223"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img
alt="View with Codesmith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a>
<a
href="https://backend.blacksmith.sh/track/enable-autofix?expires=1783221708&installation_id=138111599&pr_number=2223&repository=SerendipityOneInc%2Fecap-workspace&return_to=https%3A%2F%2Fgithub.com%2FSerendipityOneInc%2Fecap-workspace%2Fpull%2F2223&signature=9f2368aa6fbcdf8fff9130427ea6492726b9331294630fa442aa42ac1680dc3d"><picture><source
media="(prefers-color-scheme: dark)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source
media="(prefers-color-scheme: light)"
srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img
alt="Autofix with Codesmith"
src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith</code> with what you
need. Autofix is disabled.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->
```
**PR Body:**
## Summary
- Ignore stale Stripe invoice.payment_failed events when the local subscription agreement is already terminal.
- Ignore customer.subscription.updated snapshots after a terminal local agreement, while keeping deleted/canceled idempotency intact.
- Add record-level and adapter-level regression tests for the ECA-901 webhook retry case.

## Root cause
Stripe can deliver or retry invoice/subscription facts after a subscription has already been canceled locally. The Billing v2 state machine correctly rejects terminal-to-live transitions such as canceled -> past_due, but the Stripe webhook adapter treated that stale provider fact as an exception, returning 500 and causing retries.

## Test plan
- [x] source /home/node/.venvs/claw-interface/bin/activate && pytest services/claw-interface/tests/unit/test_billing_v2_provider_records.py services/claw-interface/tests/unit/test_stripe_billing_v2.py -q
- [x] source /home/node/.venvs/claw-interface/bin/activate && ruff check .
- [x] source /home/node/.venvs/claw-interface/bin/activate && pyright app tests
- [ ] source /home/node/.venvs/claw-interface/bin/activate && pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q (stopped at 63% passing per request)

Linear: https://linear.app/srpone/issue/ECA-901/stripe-webhook-rejects-canceled-past-due-subscription-state-transition

<!-- codesmith:footer -->
---
<a href="https://app.blacksmith.sh/SerendipityOneInc/codesmith/ecap-workspace/pr/2223"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"><source media="(prefers-color-scheme: light)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-light-v2.svg"><img alt="View with Codesmith" src="https://pr-comments-assets.blacksmith.sh/codesmith/view-with-codesmith-dark-v2.svg"></picture></a> <a href="https://backend.blacksmith.sh/track/enable-autofix?expires=1783221708&installation_id=138111599&pr_number=2223&repository=SerendipityOneInc%2Fecap-workspace&return_to=https%3A%2F%2Fgithub.com%2FSerendipityOneInc%2Fecap-workspace%2Fpull%2F2223&signature=9f2368aa6fbcdf8fff9130427ea6492726b9331294630fa442aa42ac1680dc3d"><picture><source media="(prefers-color-scheme: dark)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"><source media="(prefers-color-scheme: light)" srcset="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-light.svg"><img alt="Autofix with Codesmith" src="https://pr-comments-assets.blacksmith.sh/codesmith/autofix-with-codesmith-dark.svg"></picture></a>
<sup>Need help on this PR? Tag <code>@codesmith</code> with what you need. Autofix is disabled.</sup>

<!-- codesmith:autofix:disabled -->
<!-- /codesmith:footer -->
