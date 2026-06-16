# SerendipityOneInc/ecap-workspace — commits 2026-06-15

共 24 条 commits

---

## perf(ci): speed up claw-interface python tests (runner + log silencing) (#2472)
- **sha**: `9329cfe5a5c03bc05f4a87b7832ad13b7530f777`
- **作者**: Chris@ZooClaw (chris-srp)
- **日期**: 2026-06-15T13:54:03Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/9329cfe5a5c03bc05f4a87b7832ad13b7530f777
- **PR**: #2472

### 完整 commit message

```
perf(ci): speed up claw-interface python tests (runner + log silencing) (#2472)

## 背景

同事反馈 `claw-interface-quality`（python-code-quality / build-and-test）测试环节是
CI 瓶颈，通常 4–5 分钟。

实测两次近期 run 的逐 step 时长证明：**`Run tests` 一步占 226–248s ≈
85%**，是唯一可优化面。其余都已很快：依赖安装命中 uv 缓存 5–7s，`lint-and-typecheck` 是独立并行
job（~1min，不在关键路径），mongo 容器初始化 ~24s 固定开销。

测试质量分布：单测 **4228 个函数 / 283 文件**（mock mongo，CPU-bound，主导成本）；BDD **266
scenario / 34 文件**（真连 mongo，IO-bound）。

## 本 PR 的两档改动（成本中性，不改任何测试/fixture 代码）

1. **runner provider 切换**：`ubuntu-latest-m` →
`blacksmith-4vcpu-ubuntu-2404`。**同 4-vCPU 量级（成本中性）**，但 Blacksmith CPU 更快
+ 带 docker layer cache（可压缩 ~24s 的 mongo `Initialize containers`），并统一全仓
runner provider（其余 55 个 job 已在用）。
2. **CI-only 日志静音**：`pytest_args` 追加 `-o log_cli=false -o
log_file_level=WARNING`。xdist 下 live log 本就基本失效，per-test INFO 文件日志对 4.7k
测试是纯开销。**不改 `pyproject.toml`，本地开发日志不受影响。**

## 不在本 PR

- **sys.monitoring 覆盖率后端**（最大一档）：需要 srp-actions 先暴露 `coverage_core`
input —— 见 **SerendipityOneInc/srp-actions#104**。该 PR 合并后，单独再开一个 1 行
follow-up 给本 caller 加 `coverage_core: 'sysmon'`，避免在 input 落地前引用 `@main`
导致 CI 报未知 input。
- **不**提升 vCPU 量级（严格成本中性）；**不**改 `--cov-fail-under=90`；**不**动
conftest/fixture。

## 验证

- 测试数量不变：单测 4228、BDD 266（改前/改后一致）。
- 覆盖率门禁 `--cov-fail-under=90` 仍绿。
- 无新增 skip（CI 有 mongo service，BDD 应 0 skip）。
- 提速以本 PR 的 CI run `Run tests` step 时长对比基线（226–248s）为准。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: chris-srp <xuwenhao@msn.com>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## 背景

同事反馈 `claw-interface-quality`（python-code-quality / build-and-test）测试环节是 CI 瓶颈，通常 4–5 分钟。

实测两次近期 run 的逐 step 时长证明：**`Run tests` 一步占 226–248s ≈ 85%**，是唯一可优化面。其余都已很快：依赖安装命中 uv 缓存 5–7s，`lint-and-typecheck` 是独立并行 job（~1min，不在关键路径），mongo 容器初始化 ~24s 固定开销。

测试质量分布：单测 **4228 个函数 / 283 文件**（mock mongo，CPU-bound，主导成本）；BDD **266 scenario / 34 文件**（真连 mongo，IO-bound）。

## 本 PR 的两档改动（成本中性，不改任何测试/fixture 代码）

1. **runner provider 切换**：`ubuntu-latest-m` → `blacksmith-4vcpu-ubuntu-2404`。**同 4-vCPU 量级（成本中性）**，但 Blacksmith CPU 更快 + 带 docker layer cache（可压缩 ~24s 的 mongo `Initialize containers`），并统一全仓 runner provider（其余 55 个 job 已在用）。
2. **CI-only 日志静音**：`pytest_args` 追加 `-o log_cli=false -o log_file_level=WARNING`。xdist 下 live log 本就基本失效，per-test INFO 文件日志对 4.7k 测试是纯开销。**不改 `pyproject.toml`，本地开发日志不受影响。**

## 不在本 PR

- **sys.monitoring 覆盖率后端**（最大一档）：需要 srp-actions 先暴露 `coverage_core` input —— 见 **SerendipityOneInc/srp-actions#104**。该 PR 合并后，单独再开一个 1 行 follow-up 给本 caller 加 `coverage_core: 'sysmon'`，避免在 input 落地前引用 `@main` 导致 CI 报未知 input。
- **不**提升 vCPU 量级（严格成本中性）；**不**改 `--cov-fail-under=90`；**不**动 conftest/fixture。

## 验证

- 测试数量不变：单测 4228、BDD 266（改前/改后一致）。
- 覆盖率门禁 `--cov-fail-under=90` 仍绿。
- 无新增 skip（CI 有 mongo service，BDD 应 0 skip）。
- 提速以本 PR 的 CI run `Run tests` step 时长对比基线（226–248s）为准。

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(agents): support private pack install source (#2458)
- **sha**: `c796590472b2ebe8a03615d65b85f63537b0b925`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-15T12:54:08Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/c796590472b2ebe8a03615d65b85f63537b0b925
- **PR**: #2458

### 完整 commit message

```
feat(agents): support private pack install source (#2458)

## Linear
N/A

## Summary
- Add `source` to the computer-scoped agent install request body,
defaulting to `official`.
- Resolve pack lookup org server-side: `official` uses the Zooclaw pack
org, `private` uses the authenticated user's current org.
- Keep private installs strict: no org id is accepted from the client
and no fallback to official packs is attempted.
- Allow the web agent install client to pass `source: 'private'` when
installing an organization pack.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/pytest
tests/unit/test_agent_install_service.py tests/unit/test_agent_routes.py
-q`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff check
app/schema/agent_workspace.py app/routes/computer/agents.py
app/services/computer/agent_install_service.py
tests/unit/test_agent_install_service.py
tests/unit/test_agent_routes.py`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff format --check
app/schema/agent_workspace.py app/routes/computer/agents.py
app/services/computer/agent_install_service.py
tests/unit/test_agent_install_service.py
tests/unit/test_agent_routes.py`
- [x] `/Users/bill/.venvs/claw-interface/bin/pyright --pythonpath
/Users/bill/.venvs/claw-interface/bin/python
app/schema/agent_workspace.py app/routes/computer/agents.py
app/services/computer/agent_install_service.py
tests/unit/test_agent_install_service.py
tests/unit/test_agent_routes.py`
- [x] `pnpm --dir web/app exec vitest run
tests/unit/services/agent-workspaces.unit.spec.ts`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `git diff --check HEAD`

## Notes
- `bash scripts/verify-changed.sh` could not complete on this macOS host
because `web/scripts/check-no-react-in-stores.sh` uses `mapfile`, which
is unavailable in the system `/bin/bash` 3.2. The directly relevant web
checks passed separately.
```

### PR body

## Linear
N/A

## Summary
- Add `source` to the computer-scoped agent install request body, defaulting to `official`.
- Resolve pack lookup org server-side: `official` uses the Zooclaw pack org, `private` uses the authenticated user's current org.
- Keep private installs strict: no org id is accepted from the client and no fallback to official packs is attempted.
- Allow the web agent install client to pass `source: 'private'` when installing an organization pack.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/pytest tests/unit/test_agent_install_service.py tests/unit/test_agent_routes.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff check app/schema/agent_workspace.py app/routes/computer/agents.py app/services/computer/agent_install_service.py tests/unit/test_agent_install_service.py tests/unit/test_agent_routes.py`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff format --check app/schema/agent_workspace.py app/routes/computer/agents.py app/services/computer/agent_install_service.py tests/unit/test_agent_install_service.py tests/unit/test_agent_routes.py`
- [x] `/Users/bill/.venvs/claw-interface/bin/pyright --pythonpath /Users/bill/.venvs/claw-interface/bin/python app/schema/agent_workspace.py app/routes/computer/agents.py app/services/computer/agent_install_service.py tests/unit/test_agent_install_service.py tests/unit/test_agent_routes.py`
- [x] `pnpm --dir web/app exec vitest run tests/unit/services/agent-workspaces.unit.spec.ts`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `git diff --check HEAD`

## Notes
- `bash scripts/verify-changed.sh` could not complete on this macOS host because `web/scripts/check-no-react-in-stores.sh` uses `mapfile`, which is unavailable in the system `/bin/bash` 3.2. The directly relevant web checks passed separately.


---

## fix(enterprise-admin): restrict vertical pack checkout to teams (#2469)
- **sha**: `c63db6704cee5d8878fa510619559a55c227d1af`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-15T12:18:47Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/c63db6704cee5d8878fa510619559a55c227d1af
- **PR**: #2469

### 完整 commit message

```
fix(enterprise-admin): restrict vertical pack checkout to teams (#2469)

## Summary
- Hide vertical pack checkout purchase actions for non-team
enterprise-admin orgs.
- Show a clear team-only purchase message instead of Stripe/Alipay
buttons.
- Enforce the same team-only rule on the backend purchase endpoint by
reading the canonical org record.
- Add checkout page and backend route coverage for personal org users.

## Root cause
The enterprise-admin vertical pack checkout page rendered payment
actions for any authenticated org, while the purchase flow should only
be available to team orgs. The backend purchase route also accepted the
current org membership without checking the canonical org record, so a
personal org could still call the endpoint directly.

## Test plan
- [x] pnpm --dir web/enterprise-admin exec vitest run --config
./vitest.config.mts
'app/vertical-pack-plan/[planId]/checkout/__tests__/checkout-page.test.tsx'
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin run lint
- [x] services/claw-interface/.venv/bin/pytest
tests/unit/test_vertical_pack_plans_routes.py -q -k purchase
- [x] services/claw-interface/.venv/bin/ruff check
app/routes/vertical_pack/plan.py
tests/unit/test_vertical_pack_plans_routes.py
- [x] services/claw-interface/.venv/bin/ruff format --check
app/routes/vertical_pack/plan.py
tests/unit/test_vertical_pack_plans_routes.py
- [x] services/claw-interface/.venv/bin/python -m py_compile
app/routes/vertical_pack/plan.py
tests/unit/test_vertical_pack_plans_routes.py
- [x] git diff --check

## Local verification notes
- `bash scripts/verify-changed.sh` without venv PATH skipped backend
checks because `pyright` and `lint-imports` were not on PATH.
- `PATH="services/claw-interface/.venv/bin:$PATH" bash
scripts/verify-changed.sh` ran backend checks; ruff and import-linter
passed, pyright failed because this local venv is missing existing
`favie_common.logging` / `favie_common.middleware.request_context`
modules.
```

### PR body

## Summary
- Hide vertical pack checkout purchase actions for non-team enterprise-admin orgs.
- Show a clear team-only purchase message instead of Stripe/Alipay buttons.
- Enforce the same team-only rule on the backend purchase endpoint by reading the canonical org record.
- Add checkout page and backend route coverage for personal org users.

## Root cause
The enterprise-admin vertical pack checkout page rendered payment actions for any authenticated org, while the purchase flow should only be available to team orgs. The backend purchase route also accepted the current org membership without checking the canonical org record, so a personal org could still call the endpoint directly.

## Test plan
- [x] pnpm --dir web/enterprise-admin exec vitest run --config ./vitest.config.mts 'app/vertical-pack-plan/[planId]/checkout/__tests__/checkout-page.test.tsx'
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin run lint
- [x] services/claw-interface/.venv/bin/pytest tests/unit/test_vertical_pack_plans_routes.py -q -k purchase
- [x] services/claw-interface/.venv/bin/ruff check app/routes/vertical_pack/plan.py tests/unit/test_vertical_pack_plans_routes.py
- [x] services/claw-interface/.venv/bin/ruff format --check app/routes/vertical_pack/plan.py tests/unit/test_vertical_pack_plans_routes.py
- [x] services/claw-interface/.venv/bin/python -m py_compile app/routes/vertical_pack/plan.py tests/unit/test_vertical_pack_plans_routes.py
- [x] git diff --check

## Local verification notes
- `bash scripts/verify-changed.sh` without venv PATH skipped backend checks because `pyright` and `lint-imports` were not on PATH.
- `PATH="services/claw-interface/.venv/bin:$PATH" bash scripts/verify-changed.sh` ran backend checks; ruff and import-linter passed, pyright failed because this local venv is missing existing `favie_common.logging` / `favie_common.middleware.request_context` modules.


---

## chore(deps): consolidate web dependency bumps (#2465)
- **sha**: `e40d47aff73c17717f853f96a3a71520aac38639`
- **作者**: Chris@ZooClaw (chris-srp)
- **日期**: 2026-06-15T10:48:05Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/e40d47aff73c17717f853f96a3a71520aac38639
- **PR**: #2465

### 完整 commit message

```
chore(deps): consolidate web dependency bumps (#2465)

## What

Consolidates the four open Dependabot PRs into **one coherent, CI-green
dependency update**, and closes the originals (which are broken or
unmergeable):

| PR | Problem |
|----|---------|
| #2459 (minor-and-patch group, 20 updates) | merge-conflicting with
`main` (cut before the vite #2463 + mock-backend #1642 merges) |
| #2460 (eslint-config-next) | **fails all web lint** — downgrades
enterprise `eslint-config-next` 16.2.6 → 15.5.19 |
| #2461 (@types/node) | **downgrade** — drags `@types/node` from
`^24`/`^22` down to `^20` workspace-wide |
| #2462 (next) | fine on its own, folded in here |

## Why the individual PRs break

`web/` is a single pnpm workspace spanning **two Next.js majors** —
`web/app` on Next 15, `web/enterprise-*` on Next 16 (an intentional
split, see `web/CLAUDE.md`). Dependabot insists on one version per
dependency name, so its "individual" updates reach across the whole
workspace and downgrade the enterprise apps:

- **#2460**: 15.x `eslint-config-next` only exports
`eslint-config-next/core-web-vitals.js`, not the extensionless
`eslint-config-next/core-web-vitals` subpath the enterprise flat configs
import → `ERR_MODULE_NOT_FOUND` across all lint jobs.
- **#2461**: `@types/node` forced down to `^20` everywhere.

## What this PR does instead

Applies only the **upward** bumps; leaves enterprise pinned at `16.2.6`
/ `@types/node ^24`:

- `web/app`: **next** + **eslint-config-next** 15.5.18 → 15.5.19
- **react** / **react-dom** 19.x → 19.2.7, **@types/react** → 19.2.17
- **radix-ui** 1.5.0 (+ individual `@radix-ui/*` primitives)
- **shiki** 4.2.0, **marked** 18.0.5, **isbot** 5.1.41
- **@cloudflare/vite-plugin** 1.40.0, **wrangler** 4.98.0
- **knip** 6.16.1, **jscpd** 4.2.5, **tsx** 4.22.4

### Deliberately excluded

- **vitest family held at 4.1.7** — the `pnpm.overrides` pin (`vitest:
^4`) neutralizes those bumps, and floating `@vitest/coverage-v8` alone
introduces a 4.1.7/4.1.9 version skew. Worth a dedicated PR that bumps
the whole family + overrides together.
- No `vite` / `lint`-script regressions: the stale group branch had
reverted `vite ^8.0.15 → ^8.0.14` (dashboard-console) and dropped the
mock-backend lint glob — both restored to `main`.

## Validation (local)

- `pnpm install --frozen-lockfile` — clean (CI parity)
- `web/app`: `tsc` + **7034 vitest tests** + `eslint` — all green
- `tsc` for `enterprise-admin`, `enterprise-app`, `dashboard-console` —
all green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What

Consolidates the four open Dependabot PRs into **one coherent, CI-green dependency update**, and closes the originals (which are broken or unmergeable):

| PR | Problem |
|----|---------|
| #2459 (minor-and-patch group, 20 updates) | merge-conflicting with `main` (cut before the vite #2463 + mock-backend #1642 merges) |
| #2460 (eslint-config-next) | **fails all web lint** — downgrades enterprise `eslint-config-next` 16.2.6 → 15.5.19 |
| #2461 (@types/node) | **downgrade** — drags `@types/node` from `^24`/`^22` down to `^20` workspace-wide |
| #2462 (next) | fine on its own, folded in here |

## Why the individual PRs break

`web/` is a single pnpm workspace spanning **two Next.js majors** — `web/app` on Next 15, `web/enterprise-*` on Next 16 (an intentional split, see `web/CLAUDE.md`). Dependabot insists on one version per dependency name, so its "individual" updates reach across the whole workspace and downgrade the enterprise apps:

- **#2460**: 15.x `eslint-config-next` only exports `eslint-config-next/core-web-vitals.js`, not the extensionless `eslint-config-next/core-web-vitals` subpath the enterprise flat configs import → `ERR_MODULE_NOT_FOUND` across all lint jobs.
- **#2461**: `@types/node` forced down to `^20` everywhere.

## What this PR does instead

Applies only the **upward** bumps; leaves enterprise pinned at `16.2.6` / `@types/node ^24`:

- `web/app`: **next** + **eslint-config-next** 15.5.18 → 15.5.19
- **react** / **react-dom** 19.x → 19.2.7, **@types/react** → 19.2.17
- **radix-ui** 1.5.0 (+ individual `@radix-ui/*` primitives)
- **shiki** 4.2.0, **marked** 18.0.5, **isbot** 5.1.41
- **@cloudflare/vite-plugin** 1.40.0, **wrangler** 4.98.0
- **knip** 6.16.1, **jscpd** 4.2.5, **tsx** 4.22.4

### Deliberately excluded

- **vitest family held at 4.1.7** — the `pnpm.overrides` pin (`vitest: ^4`) neutralizes those bumps, and floating `@vitest/coverage-v8` alone introduces a 4.1.7/4.1.9 version skew. Worth a dedicated PR that bumps the whole family + overrides together.
- No `vite` / `lint`-script regressions: the stale group branch had reverted `vite ^8.0.15 → ^8.0.14` (dashboard-console) and dropped the mock-backend lint glob — both restored to `main`.

## Validation (local)

- `pnpm install --frozen-lockfile` — clean (CI parity)
- `web/app`: `tsc` + **7034 vitest tests** + `eslint` — all green
- `tsc` for `enterprise-admin`, `enterprise-app`, `dashboard-console` — all green

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## docs: add local frontend preview guide for designers and PMs (#2464)
- **sha**: `32765f343f3f91d893bb92b3f523ee53fac999f8`
- **作者**: Chris@ZooClaw (chris-srp)
- **日期**: 2026-06-15T10:16:11Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/32765f343f3f91d893bb92b3f523ee53fac999f8
- **PR**: #2464

### 完整 commit message

```
docs: add local frontend preview guide for designers and PMs (#2464)

## What

Adds a non-technical, prompt-driven guide for **designers and product
managers** to preview and validate frontend changes locally — without
needing to run the full backend or memorize commands.

- New doc: `docs/setup/local-frontend-preview.md`
- Explains the two existing skills (`mock-backend-scenarios` and
`dev-staging`) in plain language.
- Centers on **what prompt to paste** into Claude Code / Codex, what to
expect, and how to verify in the browser.
- Mock vs. Staging decision table, scenario reference (`ready-user` /
`onboarding-required` / `admin-rich`), the browser auth-bypass snippet,
the "first load compiles slowly = normal" caveat, and a troubleshooting
table.
- `README.md`: links the guide from the **Development → Frontend**
section.

## Why

Designers and PMs frequently want to see a change before it merges or
deploys, but the existing mock/staging instructions are scattered across
skill docs and `web/app/CLAUDE.md` and assume command-line fluency. This
consolidates them into one audience-appropriate, prompt-first entry
point.

## Notes

- Docs-only change; no code touched.
- Filename intentionally kebab-case English
(`local-frontend-preview.md`) to match siblings in `docs/setup/`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What

Adds a non-technical, prompt-driven guide for **designers and product managers** to preview and validate frontend changes locally — without needing to run the full backend or memorize commands.

- New doc: `docs/setup/local-frontend-preview.md`
  - Explains the two existing skills (`mock-backend-scenarios` and `dev-staging`) in plain language.
  - Centers on **what prompt to paste** into Claude Code / Codex, what to expect, and how to verify in the browser.
  - Mock vs. Staging decision table, scenario reference (`ready-user` / `onboarding-required` / `admin-rich`), the browser auth-bypass snippet, the "first load compiles slowly = normal" caveat, and a troubleshooting table.
- `README.md`: links the guide from the **Development → Frontend** section.

## Why

Designers and PMs frequently want to see a change before it merges or deploys, but the existing mock/staging instructions are scattered across skill docs and `web/app/CLAUDE.md` and assume command-line fluency. This consolidates them into one audience-appropriate, prompt-first entry point.

## Notes

- Docs-only change; no code touched.
- Filename intentionally kebab-case English (`local-frontend-preview.md`) to match siblings in `docs/setup/`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## chore(deps-dev): bump vite from 7.3.3 to 8.0.15 in /web (#2463)
- **sha**: `6a9d0b11c9303bfe2ba736c06e50e5aac5e26e88`
- **作者**: dependabot[bot] (dependabot[bot])
- **日期**: 2026-06-15T10:04:02Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6a9d0b11c9303bfe2ba736c06e50e5aac5e26e88
- **PR**: #2463

### 完整 commit message

```
chore(deps-dev): bump vite from 7.3.3 to 8.0.15 in /web (#2463)

[![Dependabot compatibility
score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=vite&package-manager=npm_and_yarn&previous-version=7.3.3&new-version=8.0.15)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

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

### PR body



[![Dependabot compatibility score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=vite&package-manager=npm_and_yarn&previous-version=7.3.3&new-version=8.0.15)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

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

## feat(web): add scenario-based mock backend (#1642)
- **sha**: `eaee1337d60caeca6098a92898ac2c33eb80682f`
- **作者**: Chris@ZooClaw (chris-srp)
- **日期**: 2026-06-15T10:03:26Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/eaee1337d60caeca6098a92898ac2c33eb80682f
- **PR**: #1642

### 完整 commit message

```
feat(web): add scenario-based mock backend (#1642)

## Summary
- Replace the static admin-only mock backend extension with named local
mock scenarios: `ready-user`, `onboarding-required`, and `admin-rich`.
- Move scenario fixtures and admin-rich mock routes into dedicated
modules while keeping the default local mock behavior unchanged.
- Add scenario selection to local dev/verification scripts plus a repo
skill that documents when to use mock scenarios vs staging.
- Harden local verification for this workflow: Codex sandbox keeps
running the package `lint` script via pnpm shell emulator, and macOS
local guards avoid Bash 4-only `mapfile`.

## Validation
- `bash scripts/verify-changed.sh`
- `pnpm exec vitest run
tests/unit/scripts/mock-backend-scenarios.unit.spec.ts --config
./vitest.config.mts`
- `node --check web/app/scripts/mock-backend.mjs && node --check
web/app/scripts/mock-backend/scenarios.mjs && node --check
web/app/scripts/mock-backend/admin-routes.mjs`
- `bash scripts/codex-harness.test.sh`
- `bash scripts/sync-agent-skills.sh --check`
- Manual mock smoke checks for `ready-user`, `onboarding-required`, and
`admin-rich`

## Notes
- This supersedes the original static `mock-backend.mjs` admin mock
direction in PR #1642 with a scenario-based server that can provide
different data for different local validation cases.
- `gh` commands must run outside Codex sandbox on this Mac because
GitHub CLI tokens live in the macOS keyring; this behavior is now
documented in `AGENTS.md`.

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR body

## Summary
- Replace the static admin-only mock backend extension with named local mock scenarios: `ready-user`, `onboarding-required`, and `admin-rich`.
- Move scenario fixtures and admin-rich mock routes into dedicated modules while keeping the default local mock behavior unchanged.
- Add scenario selection to local dev/verification scripts plus a repo skill that documents when to use mock scenarios vs staging.
- Harden local verification for this workflow: Codex sandbox keeps running the package `lint` script via pnpm shell emulator, and macOS local guards avoid Bash 4-only `mapfile`.

## Validation
- `bash scripts/verify-changed.sh`
- `pnpm exec vitest run tests/unit/scripts/mock-backend-scenarios.unit.spec.ts --config ./vitest.config.mts`
- `node --check web/app/scripts/mock-backend.mjs && node --check web/app/scripts/mock-backend/scenarios.mjs && node --check web/app/scripts/mock-backend/admin-routes.mjs`
- `bash scripts/codex-harness.test.sh`
- `bash scripts/sync-agent-skills.sh --check`
- Manual mock smoke checks for `ready-user`, `onboarding-required`, and `admin-rich`

## Notes
- This supersedes the original static `mock-backend.mjs` admin mock direction in PR #1642 with a scenario-based server that can provide different data for different local validation cases.
- `gh` commands must run outside Codex sandbox on this Mac because GitHub CLI tokens live in the macOS keyring; this behavior is now documented in `AGENTS.md`.


---

## docs: sync-docs weekly sweep (2026-06-15) (#2456)
- **sha**: `a9d070e081a6c4fc7dbc8e6824d0a3e3d1b26c17`
- **作者**: srp-claude-assistant[bot] (srp-claude-assistant[bot])
- **日期**: 2026-06-15T09:19:13Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/a9d070e081a6c4fc7dbc8e6824d0a3e3d1b26c17
- **PR**: #2456

### 完整 commit message

```
docs: sync-docs weekly sweep (2026-06-15) (#2456)

## Tier 1 — Deterministic fixes

- **workflow/path → `README.md`**: Removed `--log-config logging.yaml`
from the `uvicorn` dev-server command — `logging.yaml` does not exist in
the repo and the actual `scripts/dev.sh` does not use it.

## Tier 2 — Semantic fixes (evidence-grounded)

- **Deleted code ref → `architecture.md` + `architecture.zh-CN.md`
(Section C "LLM calls")**:
`services/claw-interface/app/routes/litellm.py` was deleted in commit
`8612506e8` (`refactor(workspace): remove legacy canvas and litellm
surfaces`). Both EN and 中文 docs cited `app/routes/litellm.py:52-70` as
the primary `LITELLM_PROXY_URL` usage point. Replaced with the two
surviving callers: `app/services/asr/service.py:73` and
`app/services/agent_identity.py:68`.

- **Deleted code ref → `architecture.md` + `architecture.zh-CN.md`
(Section E env var table)**: Same deletion — updated the
`LITELLM_PROXY_URL` row to remove `app/routes/litellm.py` and list the
surviving callers (`app/services/asr/service.py`,
`app/services/agent_identity.py`).

- **Removed agent → `architecture.md` + `architecture.zh-CN.md` (Section
C "Chat / non-bot agents")**: `canvas` was removed from the session/chat
agent list in commit `8612506e8`
(`services/claw-interface/app/routes/session/canvas.py` deleted). Both
EN and 中文 docs still listed it alongside `omni_chat`, `creatify`, etc.
Removed from both.

## Tier 3 — Suggestions (not applied)

- The `architecture.md` intro paragraph (Section A) still mentions
`canvas` and `fullstack_assistant` in the same sentence:
*"claw-interface also hosts a separate POST /session/chat REST/SSE
endpoint used by non-bot AI agents (omni_chat,
creative_material_generator, etc.)"* — this was already updated above.
No additional suggestions.

---

**Docs changed:** `README.md`, `architecture.md`,
`architecture.zh-CN.md`
**Window reviewed:** `4440663f94d1654ff444dfc079b8d866ec9d4dba..HEAD`
(~90-day window, last sync anchor not found → used 90-day boundary)

Co-authored-by: ecap-bot <ecap-bot@users.noreply.github.com>
```

### PR body

## Tier 1 — Deterministic fixes

- **workflow/path → `README.md`**: Removed `--log-config logging.yaml` from the `uvicorn` dev-server command — `logging.yaml` does not exist in the repo and the actual `scripts/dev.sh` does not use it.

## Tier 2 — Semantic fixes (evidence-grounded)

- **Deleted code ref → `architecture.md` + `architecture.zh-CN.md` (Section C "LLM calls")**: `services/claw-interface/app/routes/litellm.py` was deleted in commit `8612506e8` (`refactor(workspace): remove legacy canvas and litellm surfaces`). Both EN and 中文 docs cited `app/routes/litellm.py:52-70` as the primary `LITELLM_PROXY_URL` usage point. Replaced with the two surviving callers: `app/services/asr/service.py:73` and `app/services/agent_identity.py:68`.

- **Deleted code ref → `architecture.md` + `architecture.zh-CN.md` (Section E env var table)**: Same deletion — updated the `LITELLM_PROXY_URL` row to remove `app/routes/litellm.py` and list the surviving callers (`app/services/asr/service.py`, `app/services/agent_identity.py`).

- **Removed agent → `architecture.md` + `architecture.zh-CN.md` (Section C "Chat / non-bot agents")**: `canvas` was removed from the session/chat agent list in commit `8612506e8` (`services/claw-interface/app/routes/session/canvas.py` deleted). Both EN and 中文 docs still listed it alongside `omni_chat`, `creatify`, etc. Removed from both.

## Tier 3 — Suggestions (not applied)

- The `architecture.md` intro paragraph (Section A) still mentions `canvas` and `fullstack_assistant` in the same sentence: *"claw-interface also hosts a separate POST /session/chat REST/SSE endpoint used by non-bot AI agents (omni_chat, creative_material_generator, etc.)"* — this was already updated above. No additional suggestions.

---

**Docs changed:** `README.md`, `architecture.md`, `architecture.zh-CN.md`
**Window reviewed:** `4440663f94d1654ff444dfc079b8d866ec9d4dba..HEAD` (~90-day window, last sync anchor not found → used 90-day boundary)


---

## ci(deps): fix dependabot config — ignore starlette 1.x + stop web group downgrades (#2451)
- **sha**: `0ab6760cd967b39de4bec1634abb70979429f5c9`
- **作者**: Chris@ZooClaw (chris-srp)
- **日期**: 2026-06-15T09:00:24Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/0ab6760cd967b39de4bec1634abb70979429f5c9
- **PR**: #2451

### 完整 commit message

```
ci(deps): fix dependabot config — ignore starlette 1.x + stop web group downgrades (#2451)

## What

Two Dependabot **config** fixes for the two failing Dependabot PRs. No
application code changes — both are root-cause fixes in
`.github/dependabot.yml`.

### 1. Ignore Starlette 1.x (closes recurrence of #2420)

Starlette 1.x is a coordinated migration, not a drop-in bump. The
backend intentionally hard-pins `starlette==0.52.1` with `fastapi<0.137`
(documented in `services/claw-interface/requirements.txt`) to retain the
pre-1.0 surface:

- 1.x removes `app.add_event_handler` → needs a lifespan rewrite in
`app/lifetime.py`
- 1.x drops the `httpx` TestClient → needs `httpx2`

PR #2420 (starlette 1.2.0) proved it: **21 test failures + pyright
errors** from exactly these removals. Added a `starlette >=1.0.0` ignore
(mirrors the existing `next` / `litellm` / `stripe` deferred-major
entries). Lift it with the `fastapi<0.137` pin when the migration is
planned.

### 2. Stop the web group from downgrading major-pinned deps (closes
recurrence of #2421 / #2453)

`/web` is one pnpm workspace, but its packages straddle majors —
`web/app` + `dashboard-console` on Next 15 / their own `@types/node`
line, while `enterprise-admin` + `enterprise-app` run Next 16. A
**grouped** update resolves one target version per dependency and writes
it to every manifest. With the `semver-major` ignores capping the target
at the lower major's line, the higher-major manifests got
**downgraded**:

- `next` `16.2.6` → `15.5.19`
- `@types/node` `24` → `20`
- `eslint-config-next` `16.2.6` → `15.5.19`

The `eslint-config-next` downgrade made the Next 16 flat-config subpath
`eslint-config-next/core-web-vitals` unresolvable, breaking lint/tsc
across the whole web workspace (`web-quality`,
`enterprise-admin-quality`, `enterprise-app-quality`).

Fix: add `exclude-patterns` for `next`, `eslint-config-next`,
`@types/node` to the `minor-and-patch` group. Dependabot then files them
as **individual** updates, which never downgrade a manifest already
at/above the target. The semver-major ignores stay in force, so
`web/app` keeps its Next 15 line.

## Result

- #2420 closed; this stops Starlette 1.x re-opening.
- #2421 / #2453 (the corrupted group PRs) being closed; after this
merges, Dependabot re-files a correct group (no downgrades) plus small
individual PRs for the three excluded deps.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What

Two Dependabot **config** fixes for the two failing Dependabot PRs. No application code changes — both are root-cause fixes in `.github/dependabot.yml`.

### 1. Ignore Starlette 1.x (closes recurrence of #2420)

Starlette 1.x is a coordinated migration, not a drop-in bump. The backend intentionally hard-pins `starlette==0.52.1` with `fastapi<0.137` (documented in `services/claw-interface/requirements.txt`) to retain the pre-1.0 surface:

- 1.x removes `app.add_event_handler` → needs a lifespan rewrite in `app/lifetime.py`
- 1.x drops the `httpx` TestClient → needs `httpx2`

PR #2420 (starlette 1.2.0) proved it: **21 test failures + pyright errors** from exactly these removals. Added a `starlette >=1.0.0` ignore (mirrors the existing `next` / `litellm` / `stripe` deferred-major entries). Lift it with the `fastapi<0.137` pin when the migration is planned.

### 2. Stop the web group from downgrading major-pinned deps (closes recurrence of #2421 / #2453)

`/web` is one pnpm workspace, but its packages straddle majors — `web/app` + `dashboard-console` on Next 15 / their own `@types/node` line, while `enterprise-admin` + `enterprise-app` run Next 16. A **grouped** update resolves one target version per dependency and writes it to every manifest. With the `semver-major` ignores capping the target at the lower major's line, the higher-major manifests got **downgraded**:

- `next` `16.2.6` → `15.5.19`
- `@types/node` `24` → `20`
- `eslint-config-next` `16.2.6` → `15.5.19`

The `eslint-config-next` downgrade made the Next 16 flat-config subpath `eslint-config-next/core-web-vitals` unresolvable, breaking lint/tsc across the whole web workspace (`web-quality`, `enterprise-admin-quality`, `enterprise-app-quality`).

Fix: add `exclude-patterns` for `next`, `eslint-config-next`, `@types/node` to the `minor-and-patch` group. Dependabot then files them as **individual** updates, which never downgrade a manifest already at/above the target. The semver-major ignores stay in force, so `web/app` keeps its Next 15 line.

## Result

- #2420 closed; this stops Starlette 1.x re-opening.
- #2421 / #2453 (the corrupted group PRs) being closed; after this merges, Dependabot re-files a correct group (no downgrades) plus small individual PRs for the three excluded deps.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(web): allow new chat attachment-only send (#2452)
- **sha**: `c9d0ab2b0351d02ba25014082aa244319d3644b8`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-15T08:44:48Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/c9d0ab2b0351d02ba25014082aa244319d3644b8
- **PR**: #2452

### 完整 commit message

```
fix(web): allow new chat attachment-only send (#2452)

## Summary
- Allow the `/new-chat` launcher to start a conversation when the first
turn has attachments but no text.
- Use the first attachment filename as the fallback conversation title
for attachment-only starts.
- Add a regression test for attachment-only new chat sends.

## Root cause
The `/new-chat` launcher had two text-only guards: the Send button was
disabled when `vm.input.trim()` was empty, and `startChat()` returned
early when the trimmed message was empty. That blocked attachment-only
first turns even though the in-thread chat composer already supports
completed attachments without text.

## Test plan
- [x] `pnpm --dir web/app exec vitest run
tests/unit/app/new-chat/NewChatClient.unit.spec.tsx`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web/app exec eslint
'src/app/[locale]/(app)/new-chat/NewChatClient.tsx'
'src/app/[locale]/(app)/new-chat/useViewModel.ts'
tests/unit/app/new-chat/NewChatClient.unit.spec.tsx`
- [ ] `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/new-chat/NewChatClient.tsx'
'web/app/src/app/[locale]/(app)/new-chat/useViewModel.ts'
web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx` reached and
passed its `tsc`, Vitest, and ESLint phases, but the wrapper exited
non-zero first because `web/scripts/check-no-react-in-stores.sh` uses
`mapfile`, which is unavailable in this machine's `/bin/bash`.
```

### PR body

## Summary
- Allow the `/new-chat` launcher to start a conversation when the first turn has attachments but no text.
- Use the first attachment filename as the fallback conversation title for attachment-only starts.
- Add a regression test for attachment-only new chat sends.

## Root cause
The `/new-chat` launcher had two text-only guards: the Send button was disabled when `vm.input.trim()` was empty, and `startChat()` returned early when the trimmed message was empty. That blocked attachment-only first turns even though the in-thread chat composer already supports completed attachments without text.

## Test plan
- [x] `pnpm --dir web/app exec vitest run tests/unit/app/new-chat/NewChatClient.unit.spec.tsx`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web/app exec eslint 'src/app/[locale]/(app)/new-chat/NewChatClient.tsx' 'src/app/[locale]/(app)/new-chat/useViewModel.ts' tests/unit/app/new-chat/NewChatClient.unit.spec.tsx`
- [ ] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/new-chat/NewChatClient.tsx' 'web/app/src/app/[locale]/(app)/new-chat/useViewModel.ts' web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx` reached and passed its `tsc`, Vitest, and ESLint phases, but the wrapper exited non-zero first because `web/scripts/check-no-react-in-stores.sh` uses `mapfile`, which is unavailable in this machine's `/bin/bash`.


---

## docs: add managed agent thread simplification investigation (#2450)
- **sha**: `6c46b9fc2464c1d8f1dfb9d13bd535caa199d26d`
- **作者**: Chris@ZooClaw (chris-srp)
- **日期**: 2026-06-15T08:20:13Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6c46b9fc2464c1d8f1dfb9d13bd535caa199d26d
- **PR**: #2450

### 完整 commit message

```
docs: add managed agent thread simplification investigation (#2450)

## Summary

- Add an investigation doc for simplifying the managed agent partner API
plan.
- Document the proposed long-running partner agent model where tasks are
represented by Mattermost threads.
- Capture current code evidence around long-lived Mattermost tokens,
thread-per-session routing, FastClaw deployment support, and the
memory/workspace sharing risk.

## Document

-
`docs/superpowers/specs/2026-06-15-managed-agent-thread-simplification-investigation.md`

## Testing

- `bash scripts/verify-changed.sh` - no locally verifiable surfaces
changed vs `origin/main`.
```

### PR body

## Summary

- Add an investigation doc for simplifying the managed agent partner API plan.
- Document the proposed long-running partner agent model where tasks are represented by Mattermost threads.
- Capture current code evidence around long-lived Mattermost tokens, thread-per-session routing, FastClaw deployment support, and the memory/workspace sharing risk.

## Document

- `docs/superpowers/specs/2026-06-15-managed-agent-thread-simplification-investigation.md`

## Testing

- `bash scripts/verify-changed.sh` - no locally verifiable surfaces changed vs `origin/main`.


---

## refactor(workspace): remove legacy canvas and litellm surfaces (#2447)
- **sha**: `8612506e8300663c017c3bf8bda1dd8dd0c3aa23`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-15T07:57:55Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/8612506e8300663c017c3bf8bda1dd8dd0c3aa23
- **PR**: #2447

### 完整 commit message

```
refactor(workspace): remove legacy canvas and litellm surfaces (#2447)

## Summary
- Remove the legacy Canvas frontend route, hooks, API wrappers, and
tests.
- Remove the legacy claw-interface Canvas and LiteLLM route surfaces.
- Keep live LiteLLM infrastructure for billing, OpenClaw bot
credentials, ASR, and test-only LLM judge usage.

## Test plan
- [x] `bash scripts/verify-py.sh`
- [x] `cd services/claw-interface && pytest
tests/unit/test_chat_helpers.py tests/unit/test_chat_streaming.py
tests/unit/test_chat_create_session.py tests/unit/test_chat_terminate.py
tests/unit/test_chat_validation.py tests/unit/test_media_storage.py
tests/unit/test_session_utils.py tests/unit/test_utils.py -q`
- [x] `bash scripts/verify-web.sh --no-guards --no-test`
- [x] Manual equivalent of `check-no-react-in-stores.sh`

Note: `bash scripts/verify-changed.sh` passed backend checks but failed
the web guard step locally because this host runs `/bin/bash` without
`mapfile`; the equivalent store guard command found no violations. The
first web tsc attempt also hit stale local `.next/types`, and passed
after clearing generated `.next/types`.
```

### PR body

## Summary
- Remove the legacy Canvas frontend route, hooks, API wrappers, and tests.
- Remove the legacy claw-interface Canvas and LiteLLM route surfaces.
- Keep live LiteLLM infrastructure for billing, OpenClaw bot credentials, ASR, and test-only LLM judge usage.

## Test plan
- [x] `bash scripts/verify-py.sh`
- [x] `cd services/claw-interface && pytest tests/unit/test_chat_helpers.py tests/unit/test_chat_streaming.py tests/unit/test_chat_create_session.py tests/unit/test_chat_terminate.py tests/unit/test_chat_validation.py tests/unit/test_media_storage.py tests/unit/test_session_utils.py tests/unit/test_utils.py -q`
- [x] `bash scripts/verify-web.sh --no-guards --no-test`
- [x] Manual equivalent of `check-no-react-in-stores.sh`

Note: `bash scripts/verify-changed.sh` passed backend checks but failed the web guard step locally because this host runs `/bin/bash` without `mapfile`; the equivalent store guard command found no violations. The first web tsc attempt also hit stale local `.next/types`, and passed after clearing generated `.next/types`.


---

## feat(new-chat): attach files to first message (#2448)
- **sha**: `1838c0bae0e011ff324d7c0fd34e62ced38b9d5f`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-15T07:52:19Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/1838c0bae0e011ff324d7c0fd34e62ced38b9d5f
- **PR**: #2448

### 完整 commit message

```
feat(new-chat): attach files to first message (#2448)

## Summary

- add real file attach support to the new-chat launcher
- upload selected files to the newly created Mattermost channel before
posting the first message
- extract shared Mattermost attachment upload/downscale logic for reuse
by chat and new-chat

## Tests

- `pnpm --dir web/app exec vitest run
tests/unit/app/new-chat/NewChatClient.unit.spec.tsx
tests/unit/hooks/useMmAttachments.unit.spec.ts`
- `pnpm --dir web/app exec tsc --noEmit`
- targeted `eslint` on changed frontend files
- `git diff --check`

## Notes

- `bash scripts/verify-web.sh ...` passed guards, `tsc`, targeted
Vitest, and ESLint except for `web/scripts/check-no-react-in-stores.sh`
failing locally because macOS `/bin/bash` does not provide `mapfile`.
```

### PR body

## Summary

- add real file attach support to the new-chat launcher
- upload selected files to the newly created Mattermost channel before posting the first message
- extract shared Mattermost attachment upload/downscale logic for reuse by chat and new-chat

## Tests

- `pnpm --dir web/app exec vitest run tests/unit/app/new-chat/NewChatClient.unit.spec.tsx tests/unit/hooks/useMmAttachments.unit.spec.ts`
- `pnpm --dir web/app exec tsc --noEmit`
- targeted `eslint` on changed frontend files
- `git diff --check`

## Notes

- `bash scripts/verify-web.sh ...` passed guards, `tsc`, targeted Vitest, and ESLint except for `web/scripts/check-no-react-in-stores.sh` failing locally because macOS `/bin/bash` does not provide `mapfile`.


---

## feat(pack-test): add agent studio test pipeline (#2433)
- **sha**: `951cfe41557713d912790a1e6235d28e89a55c9b`
- **作者**: kaka-srp (kaka-srp)
- **日期**: 2026-06-15T07:53:43Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/951cfe41557713d912790a1e6235d28e89a55c9b
- **PR**: #2433

### 完整 commit message

```
feat(pack-test): add agent studio test pipeline (#2433)

## Linear
https://linear.app/srpone/issue/ECA-932/agent-studio-pack-test-runtime

## Summary
- Add the Agent Studio Pack Test technical design and org-scoped Pack
Test APIs.
- Add temporary archive validation/storage, warm-pool runtime reuse,
install/cleanup lifecycle, accept/extend/promote/submission gate logic.
- Add chat sidebar Pack Test bot entry, preview Mattermost credentials,
review bar actions, and focused unit coverage.

## Test plan
- [x] `PYTHONPATH=services/claw-interface
/home/node/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_middleware_auth_and_org.py
services/claw-interface/tests/unit/test_pack_test_archive_service.py
services/claw-interface/tests/unit/test_pack_test_routes.py
services/claw-interface/tests/unit/test_pack_test_service.py
services/claw-interface/tests/unit/test_pack_test_runtime_service.py
services/claw-interface/tests/unit/test_pack_services.py
services/claw-interface/tests/unit/test_routes_pack_store.py
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py
services/claw-interface/tests/unit/test_schema_pack.py
services/claw-interface/tests/unit/test_agent_install_service.py
services/claw-interface/tests/unit/test_bot_state_service.py` — 202
passed
- [x] `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/app/chat/useChatMessaging.unit.spec.ts
tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx
tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx
tests/unit/contexts/MattermostContext.unit.spec.tsx` — 89 passed
- [x] `/home/node/.venvs/claw-interface/bin/python -m ruff check
<targeted files>`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `git diff --check`
```

### PR body

## Linear
https://linear.app/srpone/issue/ECA-932/agent-studio-pack-test-runtime

## Summary
- Add the Agent Studio Pack Test technical design and org-scoped Pack Test APIs.
- Add temporary archive validation/storage, warm-pool runtime reuse, install/cleanup lifecycle, accept/extend/promote/submission gate logic.
- Add chat sidebar Pack Test bot entry, preview Mattermost credentials, review bar actions, and focused unit coverage.

## Test plan
- [x] `PYTHONPATH=services/claw-interface /home/node/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_middleware_auth_and_org.py services/claw-interface/tests/unit/test_pack_test_archive_service.py services/claw-interface/tests/unit/test_pack_test_routes.py services/claw-interface/tests/unit/test_pack_test_service.py services/claw-interface/tests/unit/test_pack_test_runtime_service.py services/claw-interface/tests/unit/test_pack_services.py services/claw-interface/tests/unit/test_routes_pack_store.py services/claw-interface/tests/unit/test_internal_agent_packs_routes.py services/claw-interface/tests/unit/test_schema_pack.py services/claw-interface/tests/unit/test_agent_install_service.py services/claw-interface/tests/unit/test_bot_state_service.py` — 202 passed
- [x] `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/app/chat/useChatMessaging.unit.spec.ts tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx tests/unit/contexts/MattermostContext.unit.spec.tsx` — 89 passed
- [x] `/home/node/.venvs/claw-interface/bin/python -m ruff check <targeted files>`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `git diff --check`

---

## fix(web): capture GA4 session source for sign-up attribution (#2449)
- **sha**: `cc95984046047b022b1fa3b315d9133f2706f80a`
- **作者**: Nemo Feng (nemo-srp)
- **日期**: 2026-06-15T07:39:28Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/cc95984046047b022b1fa3b315d9133f2706f80a
- **PR**: #2449

### 完整 commit message

```
fix(web): capture GA4 session source for sign-up attribution (#2449)

## Problem

~25% of GA4 sign-up conversions report a `Unassigned` / `(not set)`
traffic source. A GA4 exploration of `Unassigned` sessions (last ~4
weeks, prod) showed **~79% have `Session source/medium = (not set)`**,
concentrated on logged-in app pages — `/chat` (327), `/new-chat` (76),
`/user/verify`, `/claw-settings`, `/agents-manager`, plus
external-return pages like `/en/subscription/success` and
`/en/integrations/connector?status=success`. These are real,
deeply-engaged sessions (avg engagement 300s+), not bots.

GA4 builds `session_start` from whatever source the session's **first
event** carries. If that event arrives with no source, the session
resolves to `(not set)` — and since the `Direct` channel requires source
*exactly* `(direct)`, a blank source falls through to `Unassigned`.
Sign-up conversions fire on these same pages and inherit it.

## Root cause (two collection gaps)

1. **gtag init ran too late.** The `dataLayer`/`gtag` stub + `config`
lived in an `afterInteractive` `<Script>` (`TrackingScripts`). Events
fired before it loaded hit the `if (!w?.gtag) return` drop, and `config`
wasn't guaranteed to precede the first event — so the session's first
event could be recorded with no source. (This is the exact "events
before config" / "events dissociated from session" failure in GA4's own
[tagging best
practices](https://support.google.com/analytics/answer/14847402).)
2. **The first `page_view` was delayed 1000ms** — a
Firebase-Analytics-era performance guard carried over verbatim from the
gensmo-web extraction. A user who taps a mobile-OAuth button or
otherwise navigates away within that 1s never records a landing source,
so `session_start` resolves to `(not set)`.

## Changes

- **New `src/lib/gtag-bootstrap.ts`**, inlined into
`src/app/[locale]/layout.tsx` `<head>`: defines the `dataLayer`/`gtag`
queue and runs `config` **before hydration**. Early events now buffer in
`dataLayer` and replay in order *after* `config`, so `session_start`
always has a source. Preserves the verbatim `function
gtag(){dataLayer.push(arguments)}` form (an arrow + rest-params pushes
Arrays that gtag.js ignores — regression fixed in #1133) and
`send_page_view: false`.
- **`TrackingScripts`** now loads only the gtag.js library
(`afterInteractive`, which drains the queue) + the Reddit pixel.
`GA_MEASUREMENT_ID` is now a single source of truth in
`gtag-bootstrap.ts`.
- **`usePageTracking`** fires the first `page_view` synchronously (the
effect already runs post-paint; with the `<head>` bootstrap a page_view
is a cheap `dataLayer.push`). Subsequent route changes stay deferred to
idle time.

## Test plan

- `bash scripts/verify-web.sh <changed paths>` — governance guards +
`tsc` + **65 vitest** + eslint, all green.
- Updated `usePageTracking` + `TrackingScripts` specs for the new
behavior; added `gtag-bootstrap` spec including a #1133 regression guard
on the verbatim gtag form.

## How to validate after deploy (staging DebugView)

Reproduce the dominant path — returning user opening `/chat` directly,
plus one mobile-Google and one email-link sign-up — and confirm
`session_start` now carries a real source instead of `(not set)`.

## Out of scope (separate, non-code follow-ups)

The investigation also surfaced GA4-side fixes that don't belong in this
PR: a Custom Channel Group mapping `medium=newsletter` → Email
(third-party newsletters we don't control:
joinhorizon/superhuman/beehiiv/aifire) and `source set + medium (not
set)` → Referral (novatools.cn, chatgpt.com); adding the Firebase auth /
Stripe / connector domains to the unwanted-referral list; and an
internal-traffic filter for `codex_test/debug`.
```

### PR body

## Problem

~25% of GA4 sign-up conversions report a `Unassigned` / `(not set)` traffic source. A GA4 exploration of `Unassigned` sessions (last ~4 weeks, prod) showed **~79% have `Session source/medium = (not set)`**, concentrated on logged-in app pages — `/chat` (327), `/new-chat` (76), `/user/verify`, `/claw-settings`, `/agents-manager`, plus external-return pages like `/en/subscription/success` and `/en/integrations/connector?status=success`. These are real, deeply-engaged sessions (avg engagement 300s+), not bots.

GA4 builds `session_start` from whatever source the session's **first event** carries. If that event arrives with no source, the session resolves to `(not set)` — and since the `Direct` channel requires source *exactly* `(direct)`, a blank source falls through to `Unassigned`. Sign-up conversions fire on these same pages and inherit it.

## Root cause (two collection gaps)

1. **gtag init ran too late.** The `dataLayer`/`gtag` stub + `config` lived in an `afterInteractive` `<Script>` (`TrackingScripts`). Events fired before it loaded hit the `if (!w?.gtag) return` drop, and `config` wasn't guaranteed to precede the first event — so the session's first event could be recorded with no source. (This is the exact "events before config" / "events dissociated from session" failure in GA4's own [tagging best practices](https://support.google.com/analytics/answer/14847402).)
2. **The first `page_view` was delayed 1000ms** — a Firebase-Analytics-era performance guard carried over verbatim from the gensmo-web extraction. A user who taps a mobile-OAuth button or otherwise navigates away within that 1s never records a landing source, so `session_start` resolves to `(not set)`.

## Changes

- **New `src/lib/gtag-bootstrap.ts`**, inlined into `src/app/[locale]/layout.tsx` `<head>`: defines the `dataLayer`/`gtag` queue and runs `config` **before hydration**. Early events now buffer in `dataLayer` and replay in order *after* `config`, so `session_start` always has a source. Preserves the verbatim `function gtag(){dataLayer.push(arguments)}` form (an arrow + rest-params pushes Arrays that gtag.js ignores — regression fixed in #1133) and `send_page_view: false`.
- **`TrackingScripts`** now loads only the gtag.js library (`afterInteractive`, which drains the queue) + the Reddit pixel. `GA_MEASUREMENT_ID` is now a single source of truth in `gtag-bootstrap.ts`.
- **`usePageTracking`** fires the first `page_view` synchronously (the effect already runs post-paint; with the `<head>` bootstrap a page_view is a cheap `dataLayer.push`). Subsequent route changes stay deferred to idle time.

## Test plan

- `bash scripts/verify-web.sh <changed paths>` — governance guards + `tsc` + **65 vitest** + eslint, all green.
- Updated `usePageTracking` + `TrackingScripts` specs for the new behavior; added `gtag-bootstrap` spec including a #1133 regression guard on the verbatim gtag form.

## How to validate after deploy (staging DebugView)

Reproduce the dominant path — returning user opening `/chat` directly, plus one mobile-Google and one email-link sign-up — and confirm `session_start` now carries a real source instead of `(not set)`.

## Out of scope (separate, non-code follow-ups)

The investigation also surfaced GA4-side fixes that don't belong in this PR: a Custom Channel Group mapping `medium=newsletter` → Email (third-party newsletters we don't control: joinhorizon/superhuman/beehiiv/aifire) and `source set + medium (not set)` → Referral (novatools.cn, chatgpt.com); adding the Firebase auth / Stripe / connector domains to the unwanted-referral list; and an internal-traffic filter for `codex_test/debug`.


---

## fix(web): record Sentry latency metrics (#2446)
- **sha**: `7e638591d2b3a7d839dfbc263c1f5eeb0ff2bf60`
- **作者**: Chris@ZooClaw (chris-srp)
- **日期**: 2026-06-15T07:28:07Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/7e638591d2b3a7d839dfbc263c1f5eeb0ff2bf60
- **PR**: #2446

### 完整 commit message

```
fix(web): record Sentry latency metrics (#2446)

## Summary

- Move chat latency and connection duration numeric values from Sentry
Logs attributes to Sentry distribution metrics.
- Keep Logs for discrete event counts and dimensions only, so
count/user/grouping dashboards continue to work without duplicating
duration payloads.
- Update unit tests to assert latency/duration values are emitted
through `Sentry.metrics.distribution(...)` and no longer duplicated in
log attributes.

## Historical Sentry check

I checked the existing Sentry Logs data before changing the reporting
shape:

- Raw/API queries return `latency_ms`, `degraded_duration_ms`, and
`episode_duration_ms` as `null` / `string` fields, so Sentry cannot
compute historical p50/p95 from those fields.
- 14d historical count data is still available:
- `chat.message.response_latency`: `ack=380`, `reply_content=309`,
`reply_timeout=42`
  - reply-content route split: `chat=199`, `session-thread=110`
  - `chat.connection.status_mismatch`: `platform_not_ready=4`
  - display episode endings: `recovered=317`, `unmounted=58`
- `mm.connection.transition`: `connected=827`, `reconnecting=561`,
`disconnected=4`

## Dashboard state

The two Sentry dashboards have been updated directly:

- Chat Response Latency: percentile widgets now use `tracemetrics` /
distribution metric queries.
- OpenClaw Connection Status Mismatch: duration percentile widgets now
use `tracemetrics` categorical bars.
- Fresh dashboard renders for both dashboards return no widget-level
errors.

New percentile charts will populate after this change is deployed and
fresh metric samples arrive.

## Validation

- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/components/ClawConnectionStatus-recorder.unit.spec.tsx
tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts
tests/unit/lib/sentry/connection-mismatch-monitor.unit.spec.ts`
- `pnpm --dir web/app exec eslint
tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts
tests/unit/lib/sentry/connection-mismatch-monitor.unit.spec.ts
src/lib/sentry/message-latency-monitor.ts
src/lib/sentry/connection-mismatch-monitor.ts`
- `sentry dashboard view ... | jq '[.widgets[] | select(.data.type ==
"error")]'` returned `[]` for both dashboards.
```

### PR body

## Summary

- Move chat latency and connection duration numeric values from Sentry Logs attributes to Sentry distribution metrics.
- Keep Logs for discrete event counts and dimensions only, so count/user/grouping dashboards continue to work without duplicating duration payloads.
- Update unit tests to assert latency/duration values are emitted through `Sentry.metrics.distribution(...)` and no longer duplicated in log attributes.

## Historical Sentry check

I checked the existing Sentry Logs data before changing the reporting shape:

- Raw/API queries return `latency_ms`, `degraded_duration_ms`, and `episode_duration_ms` as `null` / `string` fields, so Sentry cannot compute historical p50/p95 from those fields.
- 14d historical count data is still available:
  - `chat.message.response_latency`: `ack=380`, `reply_content=309`, `reply_timeout=42`
  - reply-content route split: `chat=199`, `session-thread=110`
  - `chat.connection.status_mismatch`: `platform_not_ready=4`
  - display episode endings: `recovered=317`, `unmounted=58`
  - `mm.connection.transition`: `connected=827`, `reconnecting=561`, `disconnected=4`

## Dashboard state

The two Sentry dashboards have been updated directly:

- Chat Response Latency: percentile widgets now use `tracemetrics` / distribution metric queries.
- OpenClaw Connection Status Mismatch: duration percentile widgets now use `tracemetrics` categorical bars.
- Fresh dashboard renders for both dashboards return no widget-level errors.

New percentile charts will populate after this change is deployed and fresh metric samples arrive.

## Validation

- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/components/ClawConnectionStatus-recorder.unit.spec.tsx tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts tests/unit/lib/sentry/connection-mismatch-monitor.unit.spec.ts`
- `pnpm --dir web/app exec eslint tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts tests/unit/lib/sentry/connection-mismatch-monitor.unit.spec.ts src/lib/sentry/message-latency-monitor.ts src/lib/sentry/connection-mismatch-monitor.ts`
- `sentry dashboard view ... | jq '[.widgets[] | select(.data.type == "error")]'` returned `[]` for both dashboards.


---

## fix(ios): horizontally scrollable chat tables with max-width wrapping (#2442)
- **sha**: `029378f33ec74f2e6a99b0d6ff5161b124bba91c`
- **作者**: shana-srp (shana-maker)
- **日期**: 2026-06-15T06:17:54Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/029378f33ec74f2e6a99b0d6ff5161b124bba91c
- **PR**: #2442

### 完整 commit message

```
fix(ios): horizontally scrollable chat tables with max-width wrapping (#2442)

## What & why

Chat markdown tables rendered with each column squeezed into the bubble
width, wrapping wide cells character-by-character (e.g. `PPT / Mast /
er：`).
This makes any table with non-trivial content unreadable on iPhone.

## Approach

MarkdownUI's built-in table locks each row's height to its single-line
measurement *before* constraining column widths, so simply capping a
column
makes long cells either truncate or overflow (rows overlap). Verified
both
failure modes on-device before switching strategy.

Standard GFM tables are now intercepted and rendered by a custom view:

- **`ContentSegment.parse`** splits GFM pipe tables into a `.table`
segment
(skipping code fences) and feeds the rest through the existing inline
pass.
- **`MarkdownTableView`** sizes each column to its content up to
`tableCellMaxWidth` (220pt), then wraps onto multiple lines. Rows grow
to
the tallest cell (plain `HStack`/`VStack`, no Grid), and the whole table
  scrolls horizontally when columns overflow the bubble.
- Column widths come from Core Text measurement, with CJK font fallback.
- Keeps the `.pandaAssistant` editorial style: Lora serif, semibold
header
  row + first column, horizontal rules only, `#d8d8d8` / `#212121`.
- MarkdownUI's table style is retained as a no-wrap + horizontal-scroll
  **fallback** for any table the parser misses.
- `ContentSegment` moved to its own file to stay under the 500-line
SwiftLint
limit; removed the now-unused `LoraTableLayout` (old forced 2:1:1
widths).

## Testing

- 7 new parser tests (extraction, before/after text, alignment,
ragged-row
normalization, code-fence protection, escaped pipes, non-table prose) —
  full `ContentSegmentTests` suite (23 tests) passes.
- `xcodebuild` build succeeds (iPhone 17 Pro simulator); SwiftLint
clean.
- Rendering verified on-device via a temporary harness (removed from
this PR):
long cells wrap at the cap, rows don't overlap, table scrolls to reveal
  off-screen columns.

> Verified against a sample table mirroring the bug report, not a live
signed-in
> chat session (the component is the same `MarkdownTextView` /
`.pandaAssistant`
> path used in chat).

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What & why

Chat markdown tables rendered with each column squeezed into the bubble
width, wrapping wide cells character-by-character (e.g. `PPT / Mast / er：`).
This makes any table with non-trivial content unreadable on iPhone.

## Approach

MarkdownUI's built-in table locks each row's height to its single-line
measurement *before* constraining column widths, so simply capping a column
makes long cells either truncate or overflow (rows overlap). Verified both
failure modes on-device before switching strategy.

Standard GFM tables are now intercepted and rendered by a custom view:

- **`ContentSegment.parse`** splits GFM pipe tables into a `.table` segment
  (skipping code fences) and feeds the rest through the existing inline pass.
- **`MarkdownTableView`** sizes each column to its content up to
  `tableCellMaxWidth` (220pt), then wraps onto multiple lines. Rows grow to
  the tallest cell (plain `HStack`/`VStack`, no Grid), and the whole table
  scrolls horizontally when columns overflow the bubble.
- Column widths come from Core Text measurement, with CJK font fallback.
- Keeps the `.pandaAssistant` editorial style: Lora serif, semibold header
  row + first column, horizontal rules only, `#d8d8d8` / `#212121`.
- MarkdownUI's table style is retained as a no-wrap + horizontal-scroll
  **fallback** for any table the parser misses.
- `ContentSegment` moved to its own file to stay under the 500-line SwiftLint
  limit; removed the now-unused `LoraTableLayout` (old forced 2:1:1 widths).

## Testing

- 7 new parser tests (extraction, before/after text, alignment, ragged-row
  normalization, code-fence protection, escaped pipes, non-table prose) —
  full `ContentSegmentTests` suite (23 tests) passes.
- `xcodebuild` build succeeds (iPhone 17 Pro simulator); SwiftLint clean.
- Rendering verified on-device via a temporary harness (removed from this PR):
  long cells wrap at the cap, rows don't overlap, table scrolls to reveal
  off-screen columns.

> Verified against a sample table mirroring the bug report, not a live signed-in
> chat session (the component is the same `MarkdownTextView` / `.pandaAssistant`
> path used in chat).


---

## chore(agents): refresh Codex MCP package resolution (#2445)
- **sha**: `7c6766feb7981061831ddb80f9a7875641cc54e0`
- **作者**: Chris@ZooClaw (chris-srp)
- **日期**: 2026-06-15T06:22:03Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/7c6766feb7981061831ddb80f9a7875641cc54e0
- **PR**: #2445

### 完整 commit message

```
chore(agents): refresh Codex MCP package resolution (#2445)

## Summary

- use npm `@latest` resolution for Codex Context7 and Playwright MCP
packages
- keep npm `--min-release-age=7` so MCP startup respects the repo npm
freshness policy
- update agent skill/config drift validation for the new MCP package
policy

## Validation

- `codex --strict-config --version`
- `bash scripts/sync-agent-skills.test.sh`
- `bash scripts/verify-changed.sh`
- `npm view @upstash/context7-mcp@latest version --min-release-age=7` ->
`3.2.1`
- `npm view @playwright/mcp@latest version --min-release-age=7` ->
`0.0.76`
```

### PR body

## Summary

- use npm `@latest` resolution for Codex Context7 and Playwright MCP packages
- keep npm `--min-release-age=7` so MCP startup respects the repo npm freshness policy
- update agent skill/config drift validation for the new MCP package policy

## Validation

- `codex --strict-config --version`
- `bash scripts/sync-agent-skills.test.sh`
- `bash scripts/verify-changed.sh`
- `npm view @upstash/context7-mcp@latest version --min-release-age=7` -> `3.2.1`
- `npm view @playwright/mcp@latest version --min-release-age=7` -> `0.0.76`


---

## fix(chat-replay): allow session channel ownership (#2443)
- **sha**: `1bb9b812ef9da5a576ed3e03adfcf81cec157fb4`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-15T06:08:30Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/1bb9b812ef9da5a576ed3e03adfcf81cec157fb4
- **PR**: #2443

### 完整 commit message

```
fix(chat-replay): allow session channel ownership (#2443)

## Summary
- Allow chat replay creation from a user's current-org agent workspace
session channel as well as its DM channel.
- Replace the primary-computer runtime projection in replay ownership
checks with direct active Mattermost workspace lookup.
- Add regression coverage for session-channel replay creation and for
avoiding the primary-computer runtime path.

## Root cause
Conversation-thread replay passes the workspace session channel id, but
the create service only considered DM channel ids from the
primary-computer runtime projection when building the owned-channel
allowlist.

## Test plan
- [x] ruff format --check .
- [x] ruff check .
- [x] uv run --no-project --python 3.12 pytest
tests/unit/test_chat_replay_create.py -q
- [x] uv run --no-project --python 3.12 python -m py_compile
services/claw-interface/app/services/chat_replay/create.py
services/claw-interface/tests/unit/test_chat_replay_create.py
- [ ] pyright app tests (not run locally: pyright command not available
in this environment)
```

### PR body

## Summary
- Allow chat replay creation from a user's current-org agent workspace session channel as well as its DM channel.
- Replace the primary-computer runtime projection in replay ownership checks with direct active Mattermost workspace lookup.
- Add regression coverage for session-channel replay creation and for avoiding the primary-computer runtime path.

## Root cause
Conversation-thread replay passes the workspace session channel id, but the create service only considered DM channel ids from the primary-computer runtime projection when building the owned-channel allowlist.

## Test plan
- [x] ruff format --check .
- [x] ruff check .
- [x] uv run --no-project --python 3.12 pytest tests/unit/test_chat_replay_create.py -q
- [x] uv run --no-project --python 3.12 python -m py_compile services/claw-interface/app/services/chat_replay/create.py services/claw-interface/tests/unit/test_chat_replay_create.py
- [ ] pyright app tests (not run locally: pyright command not available in this environment)


---

## chore(hooks): support macOS session fetch fallback (#2444)
- **sha**: `d12209f75a3b5e2868af5224786d3800725debf3`
- **作者**: Chris@ZooClaw (chris-srp)
- **日期**: 2026-06-15T06:01:59Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/d12209f75a3b5e2868af5224786d3800725debf3
- **PR**: #2444

### 完整 commit message

```
chore(hooks): support macOS session fetch fallback (#2444)

Summary
- Resolve timeout command portability in the session-start fetch hook.
- Use timeout or gtimeout when available, and fall back to plain git
fetch on macOS.

Validation
- bash -n scripts/hooks/session-start-fetch.sh
- PATH=/usr/bin:/bin CLAUDE_PROJECT_DIR=... bash
scripts/hooks/session-start-fetch.sh
- git diff --check
- pre-push verify-changed: no locally verifiable surfaces changed
```

### PR body

Summary
- Resolve timeout command portability in the session-start fetch hook.
- Use timeout or gtimeout when available, and fall back to plain git fetch on macOS.

Validation
- bash -n scripts/hooks/session-start-fetch.sh
- PATH=/usr/bin:/bin CLAUDE_PROJECT_DIR=... bash scripts/hooks/session-start-fetch.sh
- git diff --check
- pre-push verify-changed: no locally verifiable surfaces changed

---

## chore(agents): harden Codex local harness (#2437)
- **sha**: `9a54a134be50f03f7e4953b397e3323155f696bf`
- **作者**: Chris@ZooClaw (chris-srp)
- **日期**: 2026-06-15T05:45:09Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/9a54a134be50f03f7e4953b397e3323155f696bf
- **PR**: #2437

### 完整 commit message

```
chore(agents): harden Codex local harness (#2437)

## Summary

- add Codex-facing local harness helpers: `codex-doctor`,
`gh-body-file`, `verify-local`, and focused shell tests
- promote recurring Claude command workflows into shared
`.agents/skills` with Claude symlink projection
- refresh PR/release/Lark guidance and wire agent/harness checks into
`verify-changed`
- include the 2026-06-14 optimization plan as the evidence/rationale doc

## Verification

- `bash -n scripts/codex-doctor.sh scripts/gh-body-file.sh
scripts/verify-local.sh scripts/codex-harness.test.sh
scripts/verify-changed.sh`
- `bash scripts/codex-harness.test.sh`
- `bash scripts/sync-agent-skills.sh --check`
- `bash scripts/sync-agent-skills.test.sh`
- `bash scripts/codex-doctor.sh --no-network --skip-git --skip-pnpm
--skip-codex-config`
- `bash scripts/verify-changed.sh`
- pre-push hook: PR size budget and changed-surface verification passed

## Local-only follow-up

`bash scripts/codex-doctor.sh` reports one remaining local environment
failure: the current Git remote embeds credentials. That should be fixed
outside this PR by replacing the remote with clean HTTPS/SSH plus the
existing credential helper / `gh auth`.
```

### PR body

## Summary

- add Codex-facing local harness helpers: `codex-doctor`, `gh-body-file`, `verify-local`, and focused shell tests
- promote recurring Claude command workflows into shared `.agents/skills` with Claude symlink projection
- refresh PR/release/Lark guidance and wire agent/harness checks into `verify-changed`
- include the 2026-06-14 optimization plan as the evidence/rationale doc

## Verification

- `bash -n scripts/codex-doctor.sh scripts/gh-body-file.sh scripts/verify-local.sh scripts/codex-harness.test.sh scripts/verify-changed.sh`
- `bash scripts/codex-harness.test.sh`
- `bash scripts/sync-agent-skills.sh --check`
- `bash scripts/sync-agent-skills.test.sh`
- `bash scripts/codex-doctor.sh --no-network --skip-git --skip-pnpm --skip-codex-config`
- `bash scripts/verify-changed.sh`
- pre-push hook: PR size budget and changed-surface verification passed

## Local-only follow-up

`bash scripts/codex-doctor.sh` reports one remaining local environment failure: the current Git remote embeds credentials. That should be fixed outside this PR by replacing the remote with clean HTTPS/SSH plus the existing credential helper / `gh auth`.


---

## fix(pack-store): require current org admin for reviews (#2441)
- **sha**: `ea066745199d5187cbd00720670ff8189e4000ed`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-15T04:20:52Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/ea066745199d5187cbd00720670ff8189e4000ed
- **PR**: #2441

### 完整 commit message

```
fix(pack-store): require current org admin for reviews (#2441)

## Summary

- Auto-approve pack submissions when the submitter belongs to the target
org and is an org admin.
- Replace Pack Store team-org dependencies with current-org login and
path-org matching.
- Require current-org admin for approve, reject, review, and deprecate
routes.

## Tests

- `/Users/bill/.venvs/claw-interface/bin/pytest
tests/unit/test_routes_pack_store.py
tests/unit/test_enterprise_wiring.py tests/unit/test_pack_services.py`
- `/Users/bill/.venvs/claw-interface/bin/ruff check
app/routes/enterprise/pack_store.py tests/unit/test_routes_pack_store.py
tests/unit/test_enterprise_wiring.py app/middleware/org.py`
- `/Users/bill/.venvs/claw-interface/bin/ruff format --check
app/routes/enterprise/pack_store.py tests/unit/test_routes_pack_store.py
tests/unit/test_enterprise_wiring.py app/middleware/org.py`
- `/Users/bill/.venvs/claw-interface/bin/pyright --pythonpath
/Users/bill/.venvs/claw-interface/bin/python
app/routes/enterprise/pack_store.py tests/unit/test_routes_pack_store.py
tests/unit/test_enterprise_wiring.py app/middleware/org.py`
- `git diff --check`
```

### PR body

## Summary

- Auto-approve pack submissions when the submitter belongs to the target org and is an org admin.
- Replace Pack Store team-org dependencies with current-org login and path-org matching.
- Require current-org admin for approve, reject, review, and deprecate routes.

## Tests

- `/Users/bill/.venvs/claw-interface/bin/pytest tests/unit/test_routes_pack_store.py tests/unit/test_enterprise_wiring.py tests/unit/test_pack_services.py`
- `/Users/bill/.venvs/claw-interface/bin/ruff check app/routes/enterprise/pack_store.py tests/unit/test_routes_pack_store.py tests/unit/test_enterprise_wiring.py app/middleware/org.py`
- `/Users/bill/.venvs/claw-interface/bin/ruff format --check app/routes/enterprise/pack_store.py tests/unit/test_routes_pack_store.py tests/unit/test_enterprise_wiring.py app/middleware/org.py`
- `/Users/bill/.venvs/claw-interface/bin/pyright --pythonpath /Users/bill/.venvs/claw-interface/bin/python app/routes/enterprise/pack_store.py tests/unit/test_routes_pack_store.py tests/unit/test_enterprise_wiring.py app/middleware/org.py`
- `git diff --check`


---

## fix(web): enable session chat sharing (#2440)
- **sha**: `9ee848c3bdff6efa46ffc07175710e02d036e31a`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-15T04:00:44Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/9ee848c3bdff6efa46ffc07175710e02d036e31a
- **PR**: #2440

### 完整 commit message

```
fix(web): enable session chat sharing (#2440)

## Summary
- Enable the existing chat replay share flow on session-thread chat
pages.
- Extract the shared provider / selection bar / created-link dialog
wrapper into `ChatShareFlowFrame`.
- Add a session-thread regression test covering the Share button and
selection mode.

## Root cause
Session-thread chat was passing a hard-coded disabled share config to
`ChatHeader`:
`enabled: false`, `selectableCount: 0`, and a no-op `onEnter`. That made
the shared header omit the Share button even when the thread had
shareable Mattermost replies.

## Test plan
- [x] `bash scripts/verify-web.sh --no-guards
'web/app/src/app/[locale]/(app)/(chat)/chat/components/share/ChatShareFlowFrame.tsx'
'web/app/src/app/[locale]/(app)/(chat)/chat/components/ChatBody.tsx'
'web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/SessionThreadClient.tsx'
web/app/tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`

Note: full local governance guards were not included because this macOS
shell hits the existing `mapfile: command not found` compatibility issue
in `web/scripts/check-no-react-in-stores.sh`; CI remains authoritative
for those guards.
```

### PR body

## Summary
- Enable the existing chat replay share flow on session-thread chat pages.
- Extract the shared provider / selection bar / created-link dialog wrapper into `ChatShareFlowFrame`.
- Add a session-thread regression test covering the Share button and selection mode.

## Root cause
Session-thread chat was passing a hard-coded disabled share config to `ChatHeader`:
`enabled: false`, `selectableCount: 0`, and a no-op `onEnter`. That made the shared header omit the Share button even when the thread had shareable Mattermost replies.

## Test plan
- [x] `bash scripts/verify-web.sh --no-guards 'web/app/src/app/[locale]/(app)/(chat)/chat/components/share/ChatShareFlowFrame.tsx' 'web/app/src/app/[locale]/(app)/(chat)/chat/components/ChatBody.tsx' 'web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/SessionThreadClient.tsx' web/app/tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`

Note: full local governance guards were not included because this macOS shell hits the existing `mapfile: command not found` compatibility issue in `web/scripts/check-no-react-in-stores.sh`; CI remains authoritative for those guards.


---

## fix(web): enable reply in session chat (#2439)
- **sha**: `8b39b2fec02fee45d59520d1616cf47c1ac54d29`
- **作者**: bill-srp (bill-srp)
- **日期**: 2026-06-15T02:56:18Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/8b39b2fec02fee45d59520d1616cf47c1ac54d29
- **PR**: #2439

### 完整 commit message

```
fix(web): enable reply in session chat (#2439)

## Summary
- Enable the existing /chat quote-reply flow on session chat pages.
- Wire session thread messages to the shared reply composer state and
clear quotes when switching thread roots.
- Add a regression test for session chat quote reply wiring.

## Root cause
Session chat already reused OpenClawChatSurface, but it did not pass
onQuoteReply, quotedText, or onClearQuote into the shared surface. That
left the existing Reply affordance and composer quote preview disabled
on session thread routes.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit --
tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx
tests/unit/app/chat/GenClawInput.unit.spec.tsx
tests/unit/app/chat/GenClawInput-extras.unit.spec.tsx

Note: pnpm --dir web run tsc currently fails before TypeScript with pnpm
Unknown option: if-present from the root script; web/app tsc was run
directly.
```

### PR body

## Summary
- Enable the existing /chat quote-reply flow on session chat pages.
- Wire session thread messages to the shared reply composer state and clear quotes when switching thread roots.
- Add a regression test for session chat quote reply wiring.

## Root cause
Session chat already reused OpenClawChatSurface, but it did not pass onQuoteReply, quotedText, or onClearQuote into the shared surface. That left the existing Reply affordance and composer quote preview disabled on session thread routes.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit -- tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx tests/unit/app/chat/GenClawInput.unit.spec.tsx tests/unit/app/chat/GenClawInput-extras.unit.spec.tsx

Note: pnpm --dir web run tsc currently fails before TypeScript with pnpm Unknown option: if-present from the root script; web/app tsc was run directly.
