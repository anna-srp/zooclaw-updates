# ecap-workspace — 近7天原始 commits

> 抓取时间：2026-04-16 08:27 UTC
> 仓库：https://github.com/SerendipityOneInc/ecap-workspace
> 共 100 条 commits

## 2026-04-16

### [a4b3c4d](https://github.com/SerendipityOneInc/ecap-workspace/commit/a4b3c4def76bbe08d39e205e7ab986c13a71d2bb) chore(ci-lint): guard that three import-linter repo lists stay in sync (#888)

**作者**: Chris@ZooClaw  
**SHA**: `a4b3c4def76bbe08d39e205e7ab986c13a71d2bb`

```
## Summary

Follow-up to [Codex's non-blocking suggestion on
#872](https://github.com/SerendipityOneInc/ecap-workspace/pull/872):
close the drift window between the three repo enumerations in
\`[tool.importlinter.contracts]\`.

**The drift class**: adding a new \`*_repo.py\` requires updating all
three lists — C1 \`ignore_imports\`, C4 \`modules\`, C4b
\`forbidden_modules\`. Missing one still fails C1 (via the generic "app
can't import favie_common" default) but with a confusing error message.
The new repo appears in the contract violation diff rather than the
human-readable "forgot to add to the whitelist" report.

## Changes

- New
\`services/claw-interface/scripts/ci-lint/06-importlinter-repo-sync.sh\`.
Parses \`pyproject.toml\` with \`tomllib\`, extracts repo entries from
the three contracts, asserts set equality.
- Same binary-discovery + hard-fail pattern as \`02-import-linter.sh\` /
\`03-complexity.sh\` / \`04-deptry.sh\`.
- Clean state emits \`"all three contracts agree on N repos."\`; drift
emits \`"in X only: [...]"\` precise diff + exit 1.
- Wire into \`.pre-commit-config.yaml\` under \`importlinter-repo-sync\`
hook id.
- CI auto-picks-up via srp-actions' \`custom_lint_scripts_dir\`.

## Test plan

- [x] Clean tree → \`"all three contracts agree on 12 repos."\`, exit 0
- [x] Negative probe: remove \`app.database.user_repo\` from C4.modules
→ exit 1 with diff output showing \`"in C1 only:
['app.database.user_repo']"\`
- [x] Stashed script is executable and follows the binary-discovery
pattern used by sibling scripts
- [ ] CI \`claw-interface-quality / lint-and-typecheck\` shows
\`Running: 06-importlinter-repo-sync.sh\` → PASS

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [97687fd](https://github.com/SerendipityOneInc/ecap-workspace/commit/97687fd081695c2bcdb7a3c36d315f1b918eec02) docs(superpowers): service-layer exception decoupling spec (#873 Item 1) (#882)

**作者**: Chris@ZooClaw  
**SHA**: `97687fd081695c2bcdb7a3c36d315f1b918eec02`

```
## Summary

- 交付 `docs/superpowers/specs/2026-04-16-service-layer-exceptions.md`（226
行，Status: Proposed）。
- 响应 Issue #873 Item 1：service 层（10 模块 × 46 处 `raise HTTPException`）与
FastAPI transport 耦合的设计决策。
- **推荐 Option B（一次性全迁）**：引入 `app/errors/` 领域异常层 + 新 ci-lint guard
`06-services-no-httpexception.sh`（allowlist-shrink，与
`02-repo-pattern-guard.sh` 同款）。
- **迁移计划**：5–6 PR 链（Phase 0 基础设施 → Phase 1 openclaw 子域 + leaf utilities
→ Phase 2 gift_code → Phase 3 invite_code → Phase 4 stripe → Phase 5
guard 硬化），每 PR ≥ ~150 行 diff。
- 本 PR **只交付设计** —— Phase 0+ 的代码 PR 不在本 scope，随后按 spec 迁移计划各自开 issue/PR
跟进。
- 与 #881（Item 2 docstring fix）**并行**，互不阻塞。

## Open Questions（期待 review 讨论后写入 spec 设计决策章节）

1. `favie_common.middleware.exception_handler` 去留 / 共存策略
2. `ExternalServiceError` 是否透传 upstream HTTP status（影响 stripe 迁移设计）
3. streaming 端点（`agent_runtime.py`）领域异常映射契约
4. `app/routes/openclaw_runtime.py::_handle_error` 是否纳入 scope
5. 异常 `code` 命名规范（`<domain>_<reason>` vs `<module>.<reason>`）

## Test plan

- [x] spec markdown 可渲染（GitHub PR preview 手检）
- [x] 引用的 ci-lint
脚本路径存在（`services/claw-interface/scripts/ci-lint/02-repo-pattern-guard.sh`）
- [x] 引用的 spec
路径存在（`docs/superpowers/specs/2026-04-11-stripe-routes-refactor.md`、`2026-04-14-stripe-cleanup.md`）
- [x] 46 处 raise 行号已核实
- [ ] CI 通过（纯 doc PR，预期无 CI 运行）

Refs #873 (Item 1).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [07409bf](https://github.com/SerendipityOneInc/ecap-workspace/commit/07409bf09e9d1fe19e13b59a048fa169e57bce99) fix(devcontainer): activate claw-interface venv in all shells (#886)

**作者**: Chris@ZooClaw  
**SHA**: `07409bf09e9d1fe19e13b59a048fa169e57bce99`

```
## Summary
- `Dockerfile`: export `VIRTUAL_ENV` and prepend
`/home/node/.venvs/claw-interface/bin` to `PATH` (root fix, effective on
container rebuild).
- `postCreateCommand.sh`: idempotently append the same exports to
`~/.zshrc` / `~/.bashrc` so existing containers get the fix without a
rebuild.

## Why
pyright resolves the Python interpreter by scanning `PATH` first (`which
python`), **not** `VIRTUAL_ENV`. The venv lives on a named volume, never
exposed on `PATH`, so fresh shells ended up on system Python 3.13 and
pyright reported spurious `Import could not be resolved` for `dotenv` /
`fastapi` / `httpx` / `uvicorn`. This wasn't worktree-specific — the
main workspace had the same defect, but VSCode's ms-python plugin masked
it by auto-activating the venv inside its own terminals.

## Test plan
- [x] Fresh `zsh -i`: `which python` →
`/home/node/.venvs/claw-interface/bin/python`, `echo $VIRTUAL_ENV` set
- [x] `cd services/claw-interface && pyright app/ tests/` → **0 errors**
(previously reported missing imports are now resolved)
- [x] `pytest tests/unit/` → 2369 passed (no regression)
- [x] rc patch is idempotent — second run is a no-op
- [ ] CI: `python-code-quality` unaffected (reusable workflow builds its
own venv, doesn't touch devcontainer)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [0b12920](https://github.com/SerendipityOneInc/ecap-workspace/commit/0b12920ecd178e9347b767605fe4647363723e41) chore(ci-lint): retire 02-repo-pattern-guard.sh (superseded by import-linter C1) (#885)

**作者**: Chris@ZooClaw  
**SHA**: `0b12920ecd178e9347b767605fe4647363723e41`

```
## Summary

Retire the bash `02-repo-pattern-guard.sh` now that the import-linter C1
contract (landed in #871, layered contracts in #872) provides equivalent
or stronger enforcement.

**Observed parallel behavior**: On #871's CI, the bash guard and
`lint-imports` produced identical pass/warn sets across every change. C1
is now the sole mongo-isolation check.

**What C1 provides over the bash guard**:
- **Finer-grained edges**: Per-importer `A -> favie_common` entries
instead of whole-file ALLOWLIST — shrinks more precisely as migrations
land.
- **Built-in stale-entry detection**: Unmatched `ignore_imports` emit
"No matches for ignored import" (same shrink-only semantics as the bash
stale-allowlist check).
- **Correct transitive exemption**: `allow_indirect_imports = true` lets
services reach `favie_common` through repo methods without false
positives — something the bash grep couldn't express cleanly.

## Changes

- Delete
`services/claw-interface/scripts/ci-lint/02-repo-pattern-guard.sh`.
- Remove `repo-pattern-guard` hook from `.pre-commit-config.yaml`.
- Update `CLAUDE.md` "Database access" bullet to point at the C1
contract and `lint-imports`.
- Drop the stale "mirrors the bash guard's ALLOWLIST" reference in the
C1 contract comment.

## Test plan

- [x] `lint-imports` → 5 contracts kept, 0 broken (C1/C2/C2b/C4/C4b)
- [x] `bash scripts/ci-lint/04-deptry.sh` → clean
- [x] No remaining references to `02-repo-pattern-guard` in repo (`grep
-r`)
- [ ] CI `python-code-quality / build-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [a098ef9](https://github.com/SerendipityOneInc/ecap-workspace/commit/a098ef9df2424aa329b4f7960adfc757cc3a8fd6) feat(sentry): comprehensive monitoring coverage (#860)

**作者**: peter-srp  
**SHA**: `a098ef9df2424aa329b4f7960adfc757cc3a8fd6`

```
对前端的所有 try/catch 兜底 + 网络错误进行收集。 具体来说：

  - 网络错误 100% 覆盖 — httpClientIntegration 全局拦截，不漏
  - JS 异常 100% 覆盖 — SDK 自动 + 3 层 ErrorBoundary
  - 业务错误 ~90% 覆盖 — 核心链路（auth / payment / chat / WS / admin）全有专属
  Monitor；Canvas / Onboarding / Skills store 暂缺（plan 里标记为 YAGNI，等出问题再加）
  - 噪音控制到位 — SSE 探测、debug、重连风暴都已过滤/去重

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [c85e2e0](https://github.com/SerendipityOneInc/ecap-workspace/commit/c85e2e01c17a7ec347ddf8ae44d97e06e9c7c1f3) chore(lint): add layered-architecture contracts (C2, C2b, C4, C4b) (#872)

**作者**: Chris@ZooClaw  
**SHA**: `c85e2e01c17a7ec347ddf8ae44d97e06e9c7c1f3`

```
Stacked on top of #871 (`feature/import-linter-c1`). **Merge #871
first**, then this PR's base auto-rebases to \`main\` and the diff shows
only the new contracts.

## Summary

Extends the import-linter configuration with four additional structural
contracts. All pass against the current tree — no code changes required.

- **C2** (layers): `app.routes` → `app.services` → `app.database`,
non-exhaustive.
- **C2b** (forbidden): `app.schema` is a leaf; it must not import
routes, services, or database modules.
- **C4** (independence): each \`app/database/*_repo.py\` is independent
of every other repo; cross-collection work lives in services.
- **C4b** (forbidden): \`app.database._errors\` and
\`app.database.collections\` are shared utilities that must not reach
back into repos.

**C5 and C3 are intentionally omitted.** See the inline comments in
\`pyproject.toml\` and the commit message for the reasoning:
- C5 (leaf service helpers): import-linter's \`forbidden\` contract
treats modules as packages by default, so sources that are descendants
of their forbidden target fail the "shared descendants" check. Working
around it would require enumerating every sibling module by hand.
- C3 (routes do not import each other): \`app/routes/session/\` is a
cohesive feature package split across multiple files that legitimately
import each other; a naive rule would misfire. Revisit after the session
package is restructured.

## Test plan

- [x] \`lint-imports\` → 5 contracts kept, 0 broken
- [x] \`pyright app/ tests/\` → 0 errors
- [x] \`pytest tests/unit/\` → 2363 passed
- [ ] CI \`python-code-quality / build-and-test\` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [83dfaab](https://github.com/SerendipityOneInc/ecap-workspace/commit/83dfaab7c9c3745109230c8a18d300e2569c5da0) fix(agents-manager): require explicit session reset after updates (#879)

**作者**: nolan-srp  
**SHA**: `83dfaab7c9c3745109230c8a18d300e2569c5da0`

```
## Summary
- stop the redeploy endpoint from automatically posting `/new` after
agent updates
- prompt users in the agents manager and agent detail flows to
explicitly start a fresh session after updating an agent
- add reset state handling, localized copy, and unit coverage for the
new post-update flow
```

### [ae8b90e](https://github.com/SerendipityOneInc/ecap-workspace/commit/ae8b90e6af491b9e4a15e35e11499986cb102c92) chore(claw-interface): enforce deptry gate — Step 2 of #870 (#883)

**作者**: Chris@ZooClaw  
**SHA**: `ae8b90e6af491b9e4a15e35e11499986cb102c92`

```
## Summary

Closes out the two-step deptry rollout from issue
[#870](https://github.com/SerendipityOneInc/ecap-workspace/issues/870)
by flipping `04-deptry.sh` from warning mode to hard failure. Step 1
([#877](https://github.com/SerendipityOneInc/ecap-workspace/pull/877))
has been on main for several PR cycles now — the warning-mode window
surfaced zero new violations, so the git-URL / transitive edge cases the
safeguard was guarding against did not materialise.

### Design choice: remove the switch, not flip it

Rather than `WARN_ONLY=1` → `WARN_ONLY=0`, the variable and its entire
branch are deleted. A dormant warning-mode toggle invites a one-char
"temporarily soften the gate" edit later on; removing it means re-opting
into warning mode takes a conscious design step.

### Test mirror

- `test_warning_mode_does_not_fail_on_violation` →
`test_violation_fails_the_build`: asserts `returncode == 1`, `ERROR`
banner, and — importantly — that `WARN_ONLY` is *absent* from the script
body, so nobody can silently re-add the escape hatch.
- `test_warning_banner_mentions_rollout_issue` →
`test_script_cites_rollout_issue`: the warning banner is gone but the
header still cites #870 for future design-rationale lookup.

### Companion doc/config changes

- `04-deptry.sh` header reframes warning mode as historical rollout
note.
- `.pre-commit-config.yaml` hook name drops "warning mode".
- `services/claw-interface/CLAUDE.md` drops the "warning-mode during
rollout" wording.
- Spec `docs/superpowers/specs/2026-04-16-deptry-rollout.md` `Status` →
Completed.

## Test plan

- [x] `pytest tests/unit/test_ci_lint_deptry.py` — 6 passed
- [x] `ruff check` / `ruff format --check` clean
- [x] Inject canary unused dep → `04-deptry.sh` exits 1 with `ERROR:
deptry reported dependency issues (DEP001-DEP004)` banner
- [x] Clean tree → `04-deptry.sh` exits 0 with success banner
- [ ] CI `python-code-quality / build-and-test` green
- [ ] CI's `04-deptry.sh` step prints success banner

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [0ad945f](https://github.com/SerendipityOneInc/ecap-workspace/commit/0ad945f795ccef2c5bcef6f4bc034f77d955188e) chore(lint): adopt import-linter with C1 mongo-isolation contract (#871)

**作者**: Chris@ZooClaw  
**SHA**: `0ad945f795ccef2c5bcef6f4bc034f77d955188e`

```
## Summary

- Add `import-linter>=2.0` to `requirements-dev.txt`.
- Declare a `[tool.importlinter]` section in `pyproject.toml` with the
first contract, **C1**, enforcing that only `app/database/` may import
`favie_common` (which is the third-party package housing
`mongo_client`).
- Wire a `lint-imports` hook into `.pre-commit-config.yaml` (follows the
same "skip if venv not found" pattern as the existing pyright hook).
- `.gitignore` the `.import_linter_cache/` directory.

**Why favie_common, not favie_common.database.mongo_client?** grimp
squashes external packages to their top-level name when
`include_external_packages = true`, so the finest-grained target we get
for a third-party package is `favie_common`. Non-mongo usage
(`create_app`'s middleware imports) is whitelisted explicitly.

**Why `allow_indirect_imports = true`?** The contract is about direct
edges. Services reach `favie_common` transitively through repo methods,
which is the intended layering and must not count as a violation.

The existing bash guard `scripts/ci-lint/02-repo-pattern-guard.sh`
continues to run in parallel. After 1-2 CI cycles confirm the two agree
on every code change, a follow-up PR will retire the bash script.

## Test plan

- [x] `lint-imports` → 1 contract kept, 0 broken (202 files, 871 deps
analyzed)
- [x] Negative test: wrote `app/__probe_mongo.py` with a direct `from
favie_common.database.mongo_client import mongo` → C1 BROKEN, exit 1.
Removing the probe restored green.
- [x] `pyright app/ tests/` → 0 errors
- [x] `pytest tests/unit/` → 2363 passed
- [ ] CI `python-code-quality / build-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [37b0a73](https://github.com/SerendipityOneInc/ecap-workspace/commit/37b0a7365acfd73dac1bbde02288e1638b8b18a7) test(claw-interface): harden 04-deptry.sh test from silent no-op (#880)

**作者**: Chris@ZooClaw  
**SHA**: `37b0a7365acfd73dac1bbde02288e1638b8b18a7`

```
## Summary

Picks up two non-blocking review suggestions from the final auto-review
pass on
[#877](https://github.com/SerendipityOneInc/ecap-workspace/pull/877)
that came in **after** the last commit cycle and went unaddressed before
merge.

- **`test_missing_binary_hard_fails` silent-no-op guard**: the two
`.replace()` calls assume 04-deptry.sh still embeds the exact venv paths
`"$REPO_ROOT/services/claw-interface/.venv/bin/deptry"` and
`"/home/node/.venvs/claw-interface/bin/deptry"`. If both strings are
ever reworded, the replaces silently no-op and the real deptry keeps
being discovered via the hardcoded fallback — the script runs against
the live repo (which is clean), exits 0, and the test false-passes. Same
silent-pass failure mode `03-complexity.sh` was previously hardened
against. One-line `assert hobbled_source != original_source` closes it.
- **Drop unused `tmp_path` fixture** in
`test_warning_mode_does_not_fail_on_violation`: the signature advertises
sandboxing but the test actually mutates the real
`services/claw-interface/requirements.txt` inside a `try/finally`.
Removing the parameter aligns signature with behaviour.

Neither change alters test semantics on the clean tree; both are
defensive improvements.

## Test plan

- [x] `pytest tests/unit/test_ci_lint_deptry.py` — 6 passed locally
- [x] `ruff check` / `ruff format --check` clean
- [ ] CI `python-code-quality / build-and-test` green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [bf68cfd](https://github.com/SerendipityOneInc/ecap-workspace/commit/bf68cfd87a1218b7b02263853870dc0d04d8043c) docs(openclaw-runtime): fix _resolve docstring to match 3-tuple return (#881)

**作者**: Chris@ZooClaw  
**SHA**: `bf68cfd87a1218b7b02263853870dc0d04d8043c`

```
## Summary

- `app/routes/openclaw_runtime.py::_resolve` 的 docstring 写 `(bot,
app_token)`，实际返回 `(user, bot, app_token)`（来自
`get_user_bot_and_token`）。四个调用点都三元 unpack `_, bot, app_token`（行
45/60/75/90）。
- 只修 docstring，一行 diff。保留 `_resolve` 包装器本身，因为
`tests/unit/test_openclaw_runtime_routes.py` 的 fixture 和若干单测用
`monkeypatch.setattr(rt, "_resolve", ...)` 把它当作 patch 锚点（与
`app/routes/connectors.py` 的 `_get_user_bot_and_token` 同款模式）。
- Closes Item 2 of #873。Item 1（service 层 HTTPException 解耦设计）在另一个 PR 里交付
spec。

## Test plan

- [x] `pyright app/routes/openclaw_runtime.py` — 0 errors
- [x] `ruff check` / `ruff format --check` — clean
- [x] `pytest tests/unit/test_openclaw_runtime_routes.py` — 11/11 pass
- [ ] CI `python-code-quality / build-and-test` green

Refs #873 (Item 2).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [2dafe33](https://github.com/SerendipityOneInc/ecap-workspace/commit/2dafe33c6cb57f8484112343e7bd8b5a98dd41c7) chore(claw-interface): add deptry dependency-consistency gate (warning mode) — Step 1 of #870 (#877)

**作者**: Chris@ZooClaw  
**SHA**: `2dafe33c6cb57f8484112343e7bd8b5a98dd41c7`

```
## Summary

Step 1 of the [issue
#870](https://github.com/SerendipityOneInc/ecap-workspace/issues/870)
two-step rollout — wires `deptry` into `services/claw-interface/`'s CI
lint chain to catch the four dependency-consistency failure modes
(DEP001–DEP004), while cleaning up the pre-existing violations surfaced
during the first scan.

- Runs in **warning mode** (`04-deptry.sh` `WARN_ONLY=1`) so this PR
doesn't block anything even if CI surfaces unexpected git-URL or
transitive-import edge cases.
- Step 2 (separate, follow-up PR) will flip `WARN_ONLY=0` once we've
observed clean CI runs on a few real PRs — rationale in
`docs/superpowers/specs/2026-04-16-deptry-rollout.md`.

### Key changes
- `services/claw-interface/pyproject.toml`: `[build-system]` +
`[tool.setuptools.dynamic]` (bridge so deptry reads `requirements*.txt`)
+ `[tool.deptry]` config (first-party, exclude override to keep `tests/`
in scope, `package_module_name_map` for git-URL packages,
`per_rule_ignores` for non-import-consumer deps like pytest plugins).
- `requirements.txt`: drop obsolete (`faker`, `asyncio` stdlib, `e2b`,
`mcp-proxy`); dedupe `prometheus_fastapi_instrumentator`; promote
`starlette` + `botocore` from transitive to direct (they *are* imported
directly by `app/` and `tests/`); add `.git` suffix to `favie-common`
URL so deptry parses the package name.
- `requirements-dev.txt`: add `deptry>=0.20`, drop redundant `faker`.
- `scripts/ci-lint/04-deptry.sh`: new script. Reuses
`03-complexity.sh`'s `PATH → .venv → devcontainer venv` binary-discovery
cascade.
- `CLAUDE.md`, `.cursor/rules/tech-stack.mdc`: keep docs in sync with
the new gate and the dependency cleanup.
- `docs/superpowers/specs/2026-04-16-deptry-rollout.md`: design spec
with the full 168 → 0 violation-reduction path, for future agents /
contributors.

### Non-goals (deferred to Step 2 follow-up PR)
- Flipping `WARN_ONLY=0` to make deptry a hard gate
- Regenerating `uv.lock` from the updated `requirements.txt` (can happen
out-of-band; lock is derived-state, not source-of-truth)

## Test plan

- [x] `deptry app tests` reports zero violations locally
- [x] `ruff format --check app tests` clean
- [x] `ruff check app tests` clean
- [x] `pyright app tests` clean (with venv activated)
- [x] `scripts/ci-lint/04-deptry.sh` exits 0 on clean tree
- [x] Injected fake DEP002 violation (appended `unused-canary` to
`requirements.txt`): script prints warning + violation details **and**
still exits 0 (warning mode)
- [ ] CI `python-code-quality / build-and-test` green
- [ ] CI `04-deptry.sh` step prints "No dependency issues found"

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [e0b661a](https://github.com/SerendipityOneInc/ecap-workspace/commit/e0b661a00c8928cf94f4999198cd2c96661a6bc4) fix: change connector skill injection path to ~/.agents/skills (#878)

**作者**: Leo-srp  
**SHA**: `e0b661a00c8928cf94f4999198cd2c96661a6bc4`

```
## Summary
Change Nango connector skill injection path from `~/.openclaw/skills` to
`~/.agents/skills`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: tim-srp <tim@srp.one>
```

### [031a481](https://github.com/SerendipityOneInc/ecap-workspace/commit/031a481d8a583bb22eecab27d987206a0f367aeb) fix(web): 修复 agent 详情页和弹窗里头像浮动动画的问题 (#863)

**作者**: lynn Zhuang  
**SHA**: `031a481d8a583bb22eecab27d987206a0f367aeb`

```
去掉了 agent 详情页和弹窗里头像浮动动画的效果

Co-authored-by: Lynn Zhuang <lynnzhuang@LynndeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>
```

### [00e4334](https://github.com/SerendipityOneInc/ecap-workspace/commit/00e43349e1576e9a2c09ee1c288e41ad5cc38a89) docs(lazy-imports): annotate the non-obvious function-body imports (#874)

**作者**: Chris@ZooClaw  
**SHA**: `00e43349e1576e9a2c09ee1c288e41ad5cc38a89`

```
## Summary

Introduce a `# lazy: <reason>` convention to document non-obvious
function-body imports. Four reason tags are used:

- **`heavy lib`** — defer large third-party packages (`boto3`/`botocore`
in `r2_storage`; Pillow in `media_utils` and transitively from
`r2_storage`'s image branch).
- **`startup side-effect`** — modules that do meaningful work at import
time (env-backed `SETTINGS`, network IO in `apple_service`), kept inside
`lifetime.py`'s startup function.
- **`avoid pytest cycle`** — the existing auth↔services test-collection
cycle documented on `require_admin_user`, reformatted to the canonical
tag.
- **`error recovery`** — imports only reached from except-branch paths
(`subscription_manager` wallet-recovery fallback).

Only the **non-obvious** cases are annotated. Stdlib `traceback` inside
an `except` block or `json` inside a validator don't need a tag because
the reason is evident from context.

This PR is documentation-only — no code paths change, no tests change.

## Test plan

- [x] `ruff check` + `ruff format --check` clean
- [x] `pyright app/ tests/` → 0 errors
- [x] `pytest tests/unit/` → 2363 passed
- [ ] CI `python-code-quality / build-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [055867b](https://github.com/SerendipityOneInc/ecap-workspace/commit/055867ba4a78682c67d825024fcf37d2923e5592) refactor(openclaw): move get_user_bot_and_token to services layer (#869)

**作者**: Chris@ZooClaw  
**SHA**: `055867ba4a78682c67d825024fcf37d2923e5592`

```
## Summary

- Extract `_get_user_bot_and_token` from
`app/routes/openclaw_settings.py` into a new module
`app/services/openclaw/bot_token.py` (public name
`get_user_bot_and_token`).
- Replace the function-body `from app.routes.openclaw_settings import
_get_user_bot_and_token` lazy imports in `app/routes/openclaw.py` (line
393) and `app/routes/openclaw_runtime.py` (line 22) with a plain
top-level import from `app.services.openclaw.bot_token`.
- Update matching test patch targets: direct helper tests patch
`app.services.openclaw.bot_token.{user_repo,get_app_token,get_first_bot}`
(the module that actually runs the code); endpoint tests patch
`app.routes.openclaw_settings.get_user_bot_and_token` (the imported name
the route module calls).

This is PR 2 in the import-linter adoption series. Eliminating the last
two cross-route lazy imports is the prerequisite for the planned "routes
modules do not import each other" contract (C3).

## Test plan

- [x] `pyright app/ tests/` → 0 errors
- [x] `ruff check` + `ruff format --check` clean
- [x] `pytest tests/unit/` → 2363 passed
- [ ] CI `python-code-quality / build-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [0343d09](https://github.com/SerendipityOneInc/ecap-workspace/commit/0343d0928046a3e649b1bddc1b6c5b07769fcdfb) refactor(orders): import ensure_billing_initialized from services directly (#868)

**作者**: Chris@ZooClaw  
**SHA**: `0343d0928046a3e649b1bddc1b6c5b07769fcdfb`

```
## Summary

- Drop the function-body `from .user import ensure_billing_initialized`
lazy import in `app/routes/orders.py`; import the helper directly from
`app.services.billing` at module top.
- The re-export via `app.routes.user` was an accidental dependency —
`orders` doesn't need `user`, both consume `services.billing`.
- Update the matching test patch target from
`app.routes.user.ensure_billing_initialized` to
`app.routes.orders.ensure_billing_initialized` (patch the importing
module, per project convention).

This is PR 1 in the series that prepares for `import-linter` adoption.
Eliminating this cross-route lazy import is a prerequisite for the
planned "routes modules do not import each other" contract.

## Test plan

- [x] `pyright app/ tests/` → 0 errors
- [x] `ruff check` + `ruff format --check` clean
- [x] `pytest tests/unit/` → 2363 passed
- [ ] CI `python-code-quality / build-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [caa19e6](https://github.com/SerendipityOneInc/ecap-workspace/commit/caa19e665ed9c93405e9a994b1fd916f59cf0fc3) chore(ci-lint): broaden repo-pattern scan to entire app/ except database/ (#867)

**作者**: Chris@ZooClaw  
**SHA**: `caa19e665ed9c93405e9a994b1fd916f59cf0fc3`

```
## Summary

- Extend `scripts/ci-lint/02-repo-pattern-guard.sh` to scan all of
`app/` (excluding only `app/database/`, the one legitimate home for
`mongo_client`) instead of just `app/routes/`, `app/services/`, and
`app/lifetime.py`.
- Allowlist two newly surfaced legacy offenders: `app/scheduler.py`
(stale-job cleanup) and `app/cron/subscription_cron.py` (subscription
lifecycle cron). Both are tracked for dedicated-repo migration in
separate follow-up PRs.
- Update `services/claw-interface/CLAUDE.md` to describe the broadened
scope.

This is PR 0 in a series that will replace the bash guard with an
`import-linter` contract while expanding structural enforcement (layered
architecture, routes non-interdependence, database repo independence).
Broadening scan coverage first establishes a clean baseline.

## Test plan

- [x] `bash
services/claw-interface/scripts/ci-lint/02-repo-pattern-guard.sh` →
clean exit, 6 allowlist entries reported as WARNING
- [x] Negative test: temporarily wrote `app/__probe_mongo.py` with a
direct `mongo_client` import → script reported ERROR and exited 1;
removing the probe restored green.
- [ ] CI `python-code-quality / build-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [d4834a3](https://github.com/SerendipityOneInc/ecap-workspace/commit/d4834a34474d41f9baff4b97fcbfb20ea44f8ad9) test(claw-interface): extract shared user-doc builder (#864) (#865)

**作者**: Chris@ZooClaw  
**SHA**: `d4834a34474d41f9baff4b97fcbfb20ea44f8ad9`

```
## Summary

- 新建
`services/claw-interface/tests/_helpers/user_builders.py`（root-level，给
BDD 和 unit 共用），把 `make_user_doc` 从 `tests/bdd/helpers.py` 搬过去
- `tests/unit/test_user_routes_coverage.py` 的 `_base_user` 改为 thin
wrapper，通过 overrides 补 `invite_binding` 和硬码时间戳 `1000000`（保留原单测的确定性语义）
- 3 个 BDD step_defs（`test_user_crud` / `test_user_endpoints` /
`test_user_list`）的 import 直接指向新路径，**不留 re-export shim**

Closes #864（Follow-up to #844 Hotspot 1）。Hotspot 2（`favie_common` stub）和
Hotspot 3（`test_admin_boost`，已由 #856 解决）out-of-scope。

## Test plan

- [x] `ruff format` + `ruff check tests/` 干净
- [x] `pyright app/ tests/` 全仓 0 errors 0 warnings
- [x] `pytest tests/unit/test_user_routes_coverage.py` 7/7 pass
- [x] `pytest tests/bdd/step_defs/test_user_{crud,endpoints,list}.py`
46/46 pass（`TEST_MONGODB_HOST=127.0.0.1 MONGODB_USER=
MONGODB_PASSWORD=`）
- [x] `jscpd -c .jscpd.tests.json` exit 0；`bdd/helpers.py ↔
test_user_routes_coverage.py` clone pair 已从 report 消失；duplication 保持
5.37% < 阈值 7.5%
- [ ] 等 CI 的 `python-code-quality / build-and-test` + auto-reviewer 绿

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [ea63724](https://github.com/SerendipityOneInc/ecap-workspace/commit/ea63724b8672414f41e640fd25a2ace9d66cde96) chore(ci-lint): extend repo-pattern guard to scan app/lifetime.py (#859)

**作者**: Chris@ZooClaw  
**SHA**: `ea63724b8672414f41e640fd25a2ace9d66cde96`

```
## Summary
Defence-in-depth follow-up to #845, which moved index creation out of
\`app/lifetime.py\` into per-repo \`ensure_indexes()\` methods. Lifetime
is now mongo-free, so adding it to the scan set means any future
re-introduction of a direct mongo import at startup fails CI instead of
quietly slipping past.

## Change
- \`scripts/ci-lint/02-repo-pattern-guard.sh\`: extend scan from
\`app/routes/ app/services/\` to also include \`app/lifetime.py\`

## Test plan
- [x] Guard still clean locally (4 session-route allowlist warnings, 0
errors)
- [x] Header comment updated to reflect new scope
- [x] No Python changes — no unit test / pyright impact

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [a145411](https://github.com/SerendipityOneInc/ecap-workspace/commit/a145411be12afef692a0e81365ec76ed7c8c1ad5) refactor(claw-interface): extract resolve_or_generate_code (#853)

**作者**: Chris@ZooClaw  
**SHA**: `a145411be12afef692a0e81365ec76ed7c8c1ad5`

```
Supersedes #849. Stacked on #851 (PR-C v2).

## Summary
Gift-code and invite-code admin creation each wrote the same three-step
dance: normalize admin-supplied code, look it up for a friendly "already
exists", else fall back to a domain-specific unique generator. Collapse
the orchestration into
\`app.services.code_utils.resolve_or_generate_code\`.

Normalize/generate functions stay per-domain — the alphabets, prefixes,
and collision budgets differ; only the editing on top of them is shared.

## Test plan
- [x] \`ruff check\` / \`ruff format\` / \`pyright\` — clean
- [x] \`pytest tests/unit/test_code_utils.py test_gift_code.py
test_invite_codes.py test_bdd/test_invite_code.py\` — 90 tests pass
- [x] \`scripts/ci-lint/02-repo-pattern-guard.sh\` — clean

## Note
Empty string for \`request.code\` is treated the same as \`None\` —
matches previous \`if request.code:\` truthiness; pinned by
\`test_empty_string_treated_as_missing\`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [f640388](https://github.com/SerendipityOneInc/ecap-workspace/commit/f6403881f57af2391379eaabaddecc0b563d2c2b) feat(chat): Mattermost reactions, tool-steps toggle, smoother streaming (#742)

**作者**: sam-srp  
**SHA**: `f6403881f57af2391379eaabaddecc0b563d2c2b`

```
## Summary

Frontend counterpart to the `@zooclaw/mattermost` streaming/tool/emoji
work (SerendipityOneInc/zooclaw-extras#15).

- **Mattermost reaction events** — `useMattermost` now subscribes to
`reaction_added` / `reaction_removed` WebSocket events and maintains a
`reactionsByPostId` map. `OpenClawUserMessage` renders the collected
reactions inline on the user's bubble (backed by `REACTION_EMOJI_MAP`
covering state + tool-category emoji names).
- **Drop duplicated ack badge** — the old "👀 Assistant" ack pill was
removed; the backend's `statusReactions.setQueued()` already emits a
real `:eyes:` reaction, so the frontend badge was just a visual
duplicate.
- **Tool steps UI simplification** — after iterating through several
expanded layouts, settled on a compact name-only pill per tool step.
Visibility is gated behind a header toggle (orange when on) with state
persisted to `localStorage` (`ecap.showToolSteps`, default off).
- **Smoother streaming** — skip the typewriter effect for live-edited
messages so streamed updates don't look like they are being retyped.
- **Custom `custom_tool_status` post handling** — parses the new
hidden-from-native-clients posts that the zooclaw mattermost plugin
emits, and surfaces them as tool steps on the corresponding bot message.

## Test plan

- [ ] Send a message via Mattermost bot — verify 👀 reaction appears on
your user bubble on arrival and clears when the reply completes.
- [ ] Trigger a tool call (web search / read file / bash) — verify the
category emoji (🔍 / 🖥️ / 🔥) appears during the tool and clears on done.
- [ ] Toggle tool steps in the header — pills appear/disappear;
preference persists across reloads.
- [ ] Long reply — bot message updates smoothly (no per-character
typewriter feel).
- [ ] Mid-conversation tool activity — pills attach to the correct bot
message in chronological order.
- [ ] No duplicate 👀 on user bubble (the old ack badge is gone; only the
server-side reaction should show).

---------

Co-authored-by: peter-srp <peter@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [7507366](https://github.com/SerendipityOneInc/ecap-workspace/commit/7507366cc549370226c8d78623c25af1ab193eb9) refactor(claw-interface): PagedResponse model + duplicate-key helper (#851)

**作者**: Chris@ZooClaw  
**SHA**: `7507366cc549370226c8d78623c25af1ab193eb9`

```
Supersedes #848 (closed; needed rebase with PR-B's BDD fix). Stacked on
#847 (PR-B).

## Summary
Same as #848. Two patterns duplicated across \`gift_code\` and
\`invite_code\` admin routes, extracted:

### 1. \`PagedResponse[T]\` + \`build_paged_response(...)\`
- New \`app/schema/paging.py\` — typed generic model
- List endpoints now declare
\`response_model=PagedResponse[GiftCodeResponse]\` /
\`PagedResponse[InviteCodeResponse]\`, so OpenAPI broadcasts the shape
to the TypeScript client
- \`has_more\` is derived from \`len(data)\` (not \`limit\`) so a short
final page still computes correctly

### 2. \`translating_duplicate_key(detail)\` +
\`is_duplicate_key_error(exc)\`
- New \`app/database/_errors.py\`
- Prefers \`pymongo.errors.DuplicateKeyError\` \`isinstance\` check,
with a string fallback (\`E11000\` / \"duplicate key\") for callers that
wrap the driver error
- Lives under \`app/database/\` so the pymongo dependency stays behind
the repo boundary

## Test plan
- [x] \`ruff check\` / \`ruff format\` / \`pyright\` — clean
- [x] Unit: 90 affected tests pass; full suite 2354 pass (2 pre-existing
unrelated failures)
- [x] BDD \`test_invite_code.py\` 12 tests pass locally (attribute
access for PagedResponse)
- [x] \`scripts/ci-lint/02-repo-pattern-guard.sh\` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [ffb124a](https://github.com/SerendipityOneInc/ecap-workspace/commit/ffb124a8ef958464b0cc3c45aae72cd5ccff42a4) chore(ci-lint): tighten jscpd tests threshold 10.5% → 7.5% (#852)

**作者**: Chris@ZooClaw  
**SHA**: `ffb124a8ef958464b0cc3c45aae72cd5ccff42a4`

```
## Summary

After PRs #850/#854/#855/#856/#857/#858 consolidated mock setup across
10 unit files, `python-tests` jscpd duplication dropped from **8.21% →
5.37%**. Apply the same `ceil(observed) + 1.5%` rule used in PR #846:

- `ceil(5.37) + 1.5 = 7.5%`

Current threshold `10.5%` leaves ~5.1 points of noise; `7.5%` keeps ~2.1
points of headroom for legitimate new tests while catching regressions
much sooner.

Also fix the stale `Duplication check — Python tests (threshold 12%)`
step name in `code-quality.yml` — it was never updated when PR #846
moved the value to `10.5%`.

## Metrics

| Metric | Before (at PR creation) | After 5 dedup rounds | After this
PR |
| --- | --- | --- | --- |
| Tests duplication (lines) | 7.16% | **5.37%** | 5.37% (config-only) |
| Tests threshold | 10.5% | 10.5% | **7.5%** |
| Src duplication | 1.31% | 1.26% | — (threshold 3% already tighter than
rule) |

## Test plan

- [x] `jscpd -c services/claw-interface/.jscpd.tests.json` — exits 0
locally at 5.37%
- [ ] CI `python-duplication-check` green on this branch

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [5b61ec4](https://github.com/SerendipityOneInc/ecap-workspace/commit/5b61ec43452498e077049d9ca9103fe84e2cf727) test(claw-interface): round 4 dedup — connector_status + admin_boost (-60 LOC) (#856)

**作者**: Chris@ZooClaw  
**SHA**: `5b61ec43452498e077049d9ca9103fe84e2cf727`

```
## Summary

Fourth round of test-side jscpd reduction, following PRs #850 / #854 /
#855. Targets two remaining self-clone hotspots.

Drops duplication (vs main, which includes #854) **6.39% → 6.02%** with
two new file-local contextmanagers + one small factory.

| File | Lines Δ |
|---|---:|
| \`test_connector_status.py\` | -26 |
| \`test_admin_boost.py\` | -36 |
| **total** | **-60** |

## Helpers added

**\`test_connector_status.py\`**
- \`_patch_status_deps(token, bot_lookup, bot_lookup_raises, client)\` —
retires the 4-patch \`get_connector_token + SETTINGS +
_get_user_bot_and_token + get_openclaw_client\` block repeated 9 times.
- \`_BOT_LOOKUP\` module constant removes the inline \`({\"uid\":
\"u1\"}, {\"bot_id\": \"bot-1\"}, \"app-token\")\` 3-tuple repetition.

**\`test_admin_boost.py\`**
- \`_billing_with_balance(balance)\` — one-wallet billing-client factory
(5x).
- \`_patch_boost_deps(user, billing_client, billing_raises,
refresh_returns, refresh_raises)\` — retires the 3–4 patch block on
\`user_repo + refresh_subscription_credits + transition_to_trial +
optional get_billing_client\` (9 tests). Uses \`ExitStack\` internally
to conditionally include patches.

## Metrics (jscpd, vs main)

| Metric | Before | After |
| --- | --- | --- |
| Duplicated lines | 2652 / 41510 | 2496 / 41450 |
| Duplication % | **6.39%** | **6.02%** |
| Clone blocks | 222 | 211 |

Independent of PR #855 (round 3) — different files, no conflicts.

## Test plan

- [x] \`pytest tests/unit/test_connector_status.py
tests/unit/test_admin_boost.py -q\` — 33 passed
- [x] \`ruff check\` / \`ruff format\` / \`pyright\` clean
- [x] \`jscpd -c services/claw-interface/.jscpd.tests.json\` exits 0 at
6.02%
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [22f0b03](https://github.com/SerendipityOneInc/ecap-workspace/commit/22f0b03e1eea4c48a1ac5e6df8575c53ca232fee) test(claw-interface): round 5 dedup — chat_validation (-65 LOC) (#857)

**作者**: Chris@ZooClaw  
**SHA**: `22f0b03e1eea4c48a1ac5e6df8575c53ca232fee`

```
## Summary

Round 5 in the test dedup series (#850 / #854 / #855 / #856). Targets
the hottest remaining unit file after rounds 2–4:

- \`test_chat_validation.py\` — 86L / 7 clones

Drops duplication (vs main after rounds 2+3 merged) **5.9% → 5.8%** with
one new file-local contextmanager.

## Helper added

\`_patch_chat_fullstack_deps(user, existing_title, extract_text,
extract_assets)\` — retires the 6-patch block
\`\`\`
mongo + consume_credits + extract_assets_from_content +
extract_text_from_message
+ generate_session_title + asyncio.create_task
\`\`\`
that was repeated 9 times in fullstack-assistant \`chat()\` tests.

Yields \`(mock_mongo, mock_create_task)\` so the few tests that assert
on
\`mock_mongo.create.await_count\` / \`mock_create_task.call_count\` can
still do so.

## Metrics (jscpd, vs main after rounds 2+3)

| Metric | Before | After |
| --- | --- | --- |
| Duplicated lines | 2443 / 41375 | 2398 / 41310 |
| Duplication % | **5.90%** | **5.80%** |
| Clone blocks | 208 | 204 |

Independent of the still-open #852 (threshold) and #856 (round 4) —
different files, no conflicts. Together with #856 brings test-side dup
below 6%.

## Test plan

- [x] \`pytest tests/unit/test_chat_validation.py -q\` — 23 passed
- [x] \`ruff check\` / \`ruff format\` / \`pyright\` clean
- [x] \`jscpd -c services/claw-interface/.jscpd.tests.json\` exits 0
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [afa9959](https://github.com/SerendipityOneInc/ecap-workspace/commit/afa99590dd8981471c0119713081a608fbc0eb70) test(claw-interface): round 6 dedup — litellm_sse_edit (-36 LOC) (#858)

**作者**: Chris@ZooClaw  
**SHA**: `afa99590dd8981471c0119713081a608fbc0eb70`

```
## Summary

Round 6 in the dedup series (#850 / #854 / #855 / #856 / #857). Targets
the Gemini edit-mode tests in \`test_litellm_sse_edit.py\` — 8-patch
block repeated across 3 test classes.

## Helpers added

- \`_make_edit_intent(target_url, reasoning)\` — mock intent factory.
- \`_patch_gemini_edit_deps(image_urls, mock_intent, download_return,
download_side_effect, gemini_result)\` — retires the 8-patch block:
- \`get_virtual_key_from_request + get_litellm_headers +
extract_image_urls_from_content + analyze_user_intent +
download_image_from_url + detect_image_format +
generate_image_with_gemini + SETTINGS\`
repeated 3x in \`TestDoGenerateImagesEditFallback\` /
\`TestDoGenerateImagesExtraImages\` (x2) /
\`TestDoGenerateImagesGeminiEditThoughts\`.

Yields \`(mock_download, mock_gemini)\` for per-test assertions on call
args.

## Metrics (jscpd, vs main after rounds 2+3)

| Metric | Before | After |
| --- | --- | --- |
| Duplicated lines | 2443 / 41375 | 2415 / 41339 |
| Duplication % | **5.90%** | **5.84%** |
| File lines | 705 | 668 (-37) |

Independent of the still-open #852 / #856 / #857 — different files, no
conflicts. Together they should land test-side dup under 5.5%.

## Test plan

- [x] \`pytest tests/unit/test_litellm_sse_edit.py -q\` — 17 passed
- [x] \`ruff check\` / \`ruff format\` / \`pyright\` clean
- [x] \`jscpd -c services/claw-interface/.jscpd.tests.json\` exits 0
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [cab8e9d](https://github.com/SerendipityOneInc/ecap-workspace/commit/cab8e9d439492eebe133a8307fb27f7e6bf8a932) refactor(claw-interface): unify admin guard into shared dependency (#847)

**作者**: Chris@ZooClaw  
**SHA**: `cab8e9d439492eebe133a8307fb27f7e6bf8a932`

```
## Summary

Four route files (`gift_code`, `invite_code`, `admin_boost`) duplicated
the same admin guard — a two-layer check (live email allowlist via user
profile + cached DB `permissions` fallback gated on GCP/CSFLE error
keywords). Extract it as `require_admin_user` in `app.auth.dependencies`
so new admin routes pick up the guard via a normal `Depends(...)`
import.

- `openclaw_admin` and `release_admin` keep their local guards — both
only verify authentication (BFF enforces admin), so consolidating with
the stricter check would silently upgrade their authorization posture.
- Detailed profile/GCP-fallback matrix moves into
`tests/unit/test_require_admin_user.py` (single source of truth); the
per-route admin-guard blocks in `test_gift_code.py` /
`test_invite_codes.py` are deleted since they were testing the same
logic through a different import path.

## Follow-up fixes addressed in this PR

- **BDD fix**: `tests/bdd/step_defs/test_invite_code.py` patched
`app.routes.invite_code.get_user_profile`, which no longer imports after
the guard moves. Removed the dead patch.
- **Security fix (from Codex review)**: `admin_boost.py` was logging
`request.admin_uid` from the POST body for audit attribution — an
authenticated admin could spoof that. Switched to the JWT-verified
`_admin_uid`; the body field is kept as optional + deprecated so
existing frontend callers don't break. Regression test pinned.
- **Route-wiring regression test (from Codex review)**: New
`tests/unit/test_admin_route_wiring.py` introspects each of the 5 admin
endpoint signatures and asserts `Depends(require_admin_user)` — catches
accidental removal of the guard that unit tests on the function would
miss.

## Diff shape

- 10 files changed, +268 / −407 (net −139 lines of duplication and
fragile patches removed)
- Admin check logic byte-identical to the previous `invite_code` version
(which had the most complete docstring)

## Test plan

- [x] `ruff check` / `ruff format` — clean
- [x] `pyright app/ tests/` — 0 errors
- [x] `pytest tests/unit/test_require_admin_user.py
tests/unit/test_admin_route_wiring.py tests/unit/test_invite_codes.py
tests/unit/test_gift_code.py tests/unit/test_admin_boost.py` — all pass
- [x] `TEST_MONGODB_HOST=127.0.0.1 MONGODB_USER= MONGODB_PASSWORD=
pytest tests/bdd/step_defs/test_invite_code.py` — 12 pass
- [x] Full CI (claw-interface-quality test + lint-and-typecheck + CodeQL
+ python-duplication-check): 15/15 SUCCESS (+ 2 SKIPPED web/ios)
- [x] `scripts/ci-lint/02-repo-pattern-guard.sh` — clean
- [x] Codex auto-review: APPROVE (5 rounds, all iterations addressed)

## Stacked chain

- Base: `main` (PR-A #845 merged)
- Downstream: #851 (PagedResponse + duplicate-key helper) → #853
(resolve_or_generate_code)
- Independent follow-up: #859 (extend repo-pattern guard to scan
`app/lifetime.py`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [748d119](https://github.com/SerendipityOneInc/ecap-workspace/commit/748d119b1d13e4c77ae71e853ac03e5b1fb4c121) fix(claw-interface): scope skill loader hidden-file filter to skill dir (#839)

**作者**: Chris@ZooClaw  
**SHA**: `748d119b1d13e4c77ae71e853ac03e5b1fb4c121`

```
## Summary

- `SkillRegistry.get_skill_files()` ran the `__pycache__` / hidden-file
filter against every component of the absolute path, so any dot-prefixed
ancestor directory (e.g. `.worktrees/<name>/…`) caused **every**
discovered skill file to be dropped and the injector silently logged `No
files to inject`.
- Switch the check to `path.relative_to(skill_dir).parts` so the filter
matches the original intent (hidden files *inside* the skill dir) and is
insensitive to the repo's checkout location.
- Add a regression test that constructs the skill dir under a
`.worktrees/`-style parent — this scenario was invisible to CI because
GitHub runner paths (`/home/runner/work/...`) contain no dot-prefixed
components.

Fixes #811

## Why CI was green

The bug only fires when an ancestor of the skill directory starts with
`.`. Neither CI (`/home/runner/work/ecap-workspace/ecap-workspace/...`)
nor the primary clone (`/workspaces/ecap-workspace/...`) has such a
component; only local worktrees under `.worktrees/` do. The new test
fixes that blind spot by building the triggering path explicitly instead
of relying on `tmp_path`.

## Test plan

- [x] `pytest tests/unit/test_skill_injector.py
tests/unit/test_skill_loader.py -v` → 43 passed (previously 2 failed in
worktrees)
- [x] `pytest tests/unit/ -q` → 2339 passed
- [x] `pyright app/ tests/` → 0 errors, 0 warnings
- [x] Minimal repro: `get_registry().get_skill_files("github")` returns
`SKILL.md` (was `[]` under `.worktrees/`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
Co-authored-by: Leo-srp <leo@srp.one>
```

## 2026-04-15

### [22bc7cb](https://github.com/SerendipityOneInc/ecap-workspace/commit/22bc7cb8c649d87efceff003eea37574e5c1b541) test(claw-interface): round 3 dedup — prompt_optimizer + seedream_fal (-198 LOC) (#855)

**作者**: Chris@ZooClaw  
**SHA**: `22bc7cb8c649d87efceff003eea37574e5c1b541`

```
## Summary

Third round of test-side jscpd reduction, following PRs #850 and #854.
Drops **main-branch** duplication from 7.16% → 6.65% by collapsing two
different mock patterns in two files. No behavior change — 41 tests
pass.

| File | Lines Δ |
|---|---:|
| \`test_litellm_prompt_optimizer.py\` | -65 |
| \`test_seedream_fal.py\` | -135 |
| **total** | **-198** |

## Helpers added

**\`test_litellm_prompt_optimizer.py\`**
- \`_patch_optimize_deps(message_urls, content_urls,
sanitize_side_effect, api_key)\` — retires the 5-patch \`litellm + 2×
extract_image_urls_* + sanitize + SETTINGS\` block repeated 9x in
\`TestOptimizePromptWithContext\`.
- \`_patch_chat_completion_deps(api_key)\` — retires the 3-patch
\`litellm + get_virtual_key_from_request + SETTINGS\` block repeated 5x
in \`TestChatCompletion\`.

**\`test_seedream_fal.py\`** (largest drop)
- \`_acm(obj)\` wraps any object in an async-context-manager mock;
aiohttp's \`.post()\` / \`.get()\` both return acms and the outer
\`ClientSession\` is also an acm, so this fires 20+ times.
- \`_make_post_session(resp, capture=…)\` builds the session whose
\`.post()\` yields a wrapped response; optional \`capture\` dict
receives the JSON body.
- \`_patch_aiohttp(session)\` returns
\`patch(\"aiohttp.ClientSession\")\` feeding the session through its acm
entrance.

Each 15-line nested-acm block in the old code collapses to ~3 lines.

## Metrics (jscpd, vs main)

| Metric | Before | After |
| --- | --- | --- |
| Duplicated lines | 2988 / 41709 | 2761 / 41511 |
| Duplication % | **7.16%** | **6.65%** |
| Clone blocks | 255 | 239 |

Independent of PR #854 (round 2) — different files, no conflicts. When
both land, combined effect should be below 6%.

## Test plan

- [x] \`pytest tests/unit/test_litellm_prompt_optimizer.py
tests/unit/test_seedream_fal.py -q\` — 41 passed
- [x] \`ruff check\` / \`ruff format\` / \`pyright\` clean
- [x] \`jscpd -c services/claw-interface/.jscpd.tests.json\` — exits 0
at 6.65%
- [ ] CI \`python-duplication-check\` + \`claw-interface-quality\` green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [0d6ec6c](https://github.com/SerendipityOneInc/ecap-workspace/commit/0d6ec6c7f5a446278edac972f4a9aeab386100ff) refactor(claw-interface): move index creation into repos (#845)

**作者**: Chris@ZooClaw  
**SHA**: `0d6ec6c7f5a446278edac972f4a9aeab386100ff`

```
## Summary
- `lifetime.py` was the last caller reaching into
`mongo.db[COLLECTION].create_index(...)` directly (session routes
aside). Five nearly identical `_ensure_*_index` helpers moved onto the
repos they index — each repo now owns `ensure_indexes()` and startup
just calls them
- `lifetime.py` no longer imports `favie_common.database.mongo_client`;
the file is effectively mongo-free, bringing it in line with the
`CLAUDE.md` rule "only \`app/database/*_repo.py\` may import \`mongo\`"
- Pure refactor: index names (`unique_code`, `unique_uid`,
`unique_notification_uuid`, `unique_gift_code`,
`unique_user_code_type`), keys, uniqueness options, and log-on-failure
behaviour are all preserved

## Test plan
- [x] `ruff check --fix` + `ruff format` on changed files — clean
- [x] `pyright app/ tests/` — 0 errors
- [x] `pytest tests/unit/test_lifetime.py tests/unit/test_*_repo.py` —
all 69 relevant tests pass
- [x] Full `pytest tests/unit/` coverage unchanged from baseline
(pre-existing `test_skill_injector` failures and 85.87% coverage are not
introduced by this PR; CI runs with `enable_mongodb: true` for the rest)
- [x] `scripts/ci-lint/02-repo-pattern-guard.sh` — still clean (4
session-route allowlist entries remain; not touched in this PR)
- [x] `scripts/ci-lint/05-no-collection-name-constants.sh` — clean

## Follow-up (not in this PR)
- Optionally extend the repo-pattern guard to scan `app/lifetime.py`,
turning the "only repos import mongo" rule from a convention into a lint
check for startup code too

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [6fb3900](https://github.com/SerendipityOneInc/ecap-workspace/commit/6fb39001962f3ff5b301e1026dab23d2893f32dd) test(claw-interface): round 2 dedup in 3 hottest test files (7.16% → 6.39%) (#854)

**作者**: Chris@ZooClaw  
**SHA**: `6fb39001962f3ff5b301e1026dab23d2893f32dd`

```
## Summary

Follow-up to PR #850: pulls inline mock boilerplate in the three hottest
`self-clone` files into file-local helpers. Drops test-side jscpd
duplication from **7.16% → 6.39%**.

| File | Lines Δ | Clones dropped |
|---|---:|---:|
| \`test_openclaw_endpoints_extra.py\` | +5 / -23 | 78L of 23 clones →
145L of 14 |
| \`test_clawhub_routes.py\` | -118 | 149L of 12 clones → (not top 10) |
| \`test_litellm_video.py\` | -88 | 141L of 12 clones → (not top 10) |
| **total** | **-199** | 255 → 222 |

## Helpers added

- \`test_openclaw_endpoints_extra.py\`: \`_auth(uid, token)\` — the
6-field \`current_user={\"uid\":…, \"email\":\"\",…}\` dict was repeated
~25 times as the last argument of every endpoint call.
- \`test_clawhub_routes.py\`: \`_user(bot_status, bot_id)\` +
\`_patch_clawhub(user)\` contextmanager +
\`_make_http_status_error(status, body)\`.
- \`test_litellm_video.py\`: \`_make_httpx_client(...)\` +
\`_make_aiohttp_session(...)\` + \`_patch_quick_image_process()\`.

All helpers use the \`_\`-prefix / file-local convention established in
PR #846 / #850 — not promoted to \`conftest.py\` because patch targets
bind to module paths.

## Metrics (jscpd)

| Metric | Before | After |
| --- | --- | --- |
| Duplicated lines | 2988 / 41709 | 2652 / 41510 |
| Duplication % | **7.16%** | **6.39%** |
| Clone blocks | 255 | 222 |

## Test plan

- [x] \`pytest tests/unit/test_openclaw_endpoints_extra.py
tests/unit/test_clawhub_routes.py tests/unit/test_litellm_video.py -q\`
— 107 passed
- [x] \`ruff check\` / \`ruff format\` / \`pyright\` clean on all 3
files
- [x] \`jscpd -c services/claw-interface/.jscpd.tests.json\` — exits 0
at 6.39% (well under both old 10.5% and upcoming 9.5% in #852)
- [ ] CI \`python-duplication-check\` green on this branch
- [ ] CI \`claw-interface-quality\` green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [27a167b](https://github.com/SerendipityOneInc/ecap-workspace/commit/27a167b43d30fb3201efe1c572cf9fd28cb75e6c) test(claw-interface): consolidate mock setup across 4 unit files (-331 LOC) (#850)

**作者**: Chris@ZooClaw  
**SHA**: `27a167b43d30fb3201efe1c572cf9fd28cb75e6c`

```
## Summary

Extracts file-local `_` helpers to retire duplicated mock setup in four
unit test files. **No behavior change** — all 79 targeted tests still
pass.

| File | Before | After | Δ |
|------|------:|------:|------:|
| \`test_litellm_polling.py\` | 502 | 319 | -182 |
| \`test_user_billing.py\` | 757 | 673 | -84 |
| \`test_chat_create_session.py\` | 554 | 514 | -39 |
| \`test_inject_credentials.py\` | 277 | 251 | -26 |
| **total** | 2090 | 1757 | **-333 (-16%)** |

## Approach

Each file gets its own private helpers (leading `_`, not promoted to
`conftest.py`) — because patch targets bind to specific module paths
(per CLAUDE.md's *patch importing module, not repo* rule), cross-file
hoisting would add friction without real reuse.

Two abstraction shapes:
- **`@contextmanager`** for "multiple-patch" blocks
(`_patch_billing_deps`, `_patch_inject_deps`, `_patch_fal_polling`,
`_patch_fetch_fal_video`) — replaces 7-line `with (patch(...),
patch(...), ...)` ceremony.
- **Factories** for "mock-object assembly" (`_make_billing_client`,
`_make_put_http`, `_make_openclaw_client`, `_make_bot_user`,
`_setup_agent_platform_success`, `_error_session`) — mirrors the
pre-existing `_make_settings` / `_setup_agent_platform_error` /
`_stripe_helpers` style.

Commits are per-file so each change can be read (or reverted) in
isolation.

## Test plan

- [x] \`ruff format\` / \`ruff check\` clean on all 4 files
- [x] \`pyright\` clean on all 4 files
- [x] \`pytest tests/unit/test_litellm_polling.py
tests/unit/test_user_billing.py tests/unit/test_chat_create_session.py
tests/unit/test_inject_credentials.py\` — 79 passed
- [ ] \`python-code-quality / build-and-test\` CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [d4ee828](https://github.com/SerendipityOneInc/ecap-workspace/commit/d4ee8285e0e99330a92e8def327ee4a1d09c2e57) test(claw-interface): dedupe unit test helpers and tighten jscpd threshold (#846)

**作者**: Chris@ZooClaw  
**SHA**: `d4ee8285e0e99330a92e8def327ee4a1d09c2e57`

```
## Summary

- Migrate inline `_user_doc` / `_order_doc` in 6 unit test files to thin
wrappers that delegate to a new `tests/unit/_builders.py` module —
executes the "Shared test helpers — use them, don't redefine" rule
already documented in `services/claw-interface/CLAUDE.md`.
- Hoist duplicated `mock_mongo` / `mock_client` pytest fixtures in
`test_openclaw_endpoints_extra.py` from 6 per-class copies to
module-level. `mock_settings` stays class-local because the patched
attribute sets differ per test class (some set
`OPENCLAW_PLATFORM_LLM_URL`, others only `OPENCLAW_PLATFORM_URL`) and
unifying would reduce test intent clarity without changing behavior.
- Tighten `.jscpd.tests.json` threshold from `12%` → `10.5%` using the
rule `ceil(observed) + 1.5%` so the gate blocks regressions rather than
sitting far above the actual value.

## Metrics

| Metric | Before | After |
| --- | --- | --- |
| Duplicated lines | 3558 / 42117 | 3452 / 42040 |
| Duplication % (jscpd) | **8.45%** | **8.21%** |
| Clone blocks | 286 | 284 |
| Tests-side threshold | 12% | **10.5%** |
| Files touched | — | 8 modified + 1 new |
| Net line change | — | -193 / +115 |

The biggest single contributor to the drop was the openclaw fixture
hoist (eliminated the 34-line fixture-trio clone that appeared 5 times).
The `_user_doc`/`_order_doc` thin-wrapper work is a spec-compliance
cleanup — jscpd's `minLines: 5` / `minTokens: 50` threshold makes short
inline dicts invisible to the detector even before this change.

## Out of scope (follow-ups)

Intentionally not bundled into this PR to respect the 2000-line PR
budget and keep review scope tight:

- `test_user_billing.py` — `mock_billing.bootstrap_user` setup repeated
3x at 27 lines each
- `test_chat_create_session.py` — agent-platform mock block repeated 3x
at 26 lines each (file already touched here for `_user_doc`, but the
mock block needs its own fixture design)
- `test_inject_credentials.py` — 26-line mock block repeated 3x
- `test_litellm_polling.py` — multiple 22-26 line self-clones
- `test_stripe_coverage.py`, `test_seedream_fal.py`,
`test_connector_coverage.py` — smaller self-clones
- BDD tests (`test_stripe_order_confirm.py`, `test_user_endpoints.py`,
etc.) — explicitly excluded per the plan

Each of these is a small independent PR.

## Test plan

- [x] `uv run pytest tests/unit/` — 2331 passed (the 2 failures in
`test_skill_injector.py` are pre-existing on main and unrelated)
- [x] `pyright app/ tests/` — 0 errors, 0 warnings
- [x] `ruff check` + `ruff format` — clean
- [x] `jscpd -c services/claw-interface/.jscpd.tests.json` — exit 0
under new threshold
- [ ] CI `python-duplication-check` job green on this branch
- [ ] CI `claw-interface-quality` job green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [e006b77](https://github.com/SerendipityOneInc/ecap-workspace/commit/e006b77b0b0b658e980090fa9ffa09536ca2ed82) chore(ci-lint): drop --depth=1 shallow side effect; merge mongo guards; canonicalize collection constants (#843)

**作者**: Chris@ZooClaw  
**SHA**: `e006b77b0b0b658e980090fa9ffa09536ca2ed82`

```
## Background — root cause of today's "diverged 700 vs 3, no common
ancestor" incident

A local `git status` claimed `main` had diverged from `origin/main` with
**no common ancestor**. Investigation showed `.git/shallow` was present
with a single boundary commit, so `merge-base` / `rev-list --count` /
"diverged by N" all gave nonsense answers.

The culprit:

```bash
# services/claw-interface/scripts/ci-lint/{01..05}-*.sh + web/scripts/check-ignores-shrink-only.sh
git fetch origin "$BASE_REF" --depth=1 --quiet 2>/dev/null || true
```

`git fetch --depth=1` against a **full** repo writes a permanent shallow
boundary into `.git/shallow`. Subsequent normal fetches advance the tip
but never extend the boundary, so `origin/main` looks like it has only N
commits. Pre-commit and local lint runs were quietly shallowifying every
developer's clone.

## Summary of changes

### A. Shallow-fetch removal (6 scripts)
Dropped the `git fetch ... --depth=1` line in:
- `services/claw-interface/scripts/ci-lint/{01-file-length,
03-complexity, 05-no-collection-name-constants}.sh`
- `web/scripts/check-ignores-shrink-only.sh`
- (02/04 are wholesale rewritten — see below)

CI's `actions/checkout` already controls fetch-depth; local devs are
responsible for their own `git fetch origin main` cadence. Scripts no
longer mutate remote-tracking refs.

### B. `02-no-direct-mongo-in-{routes,services}.sh` →
`02-repo-pattern-guard.sh`
Two near-identical scripts (only differing in scan dir + allowlist)
merged into one:

- **Scan all** `app/routes/` + `app/services/` for direct
`favie_common.database.mongo_client` imports
- **ALLOWLIST**: legacy violations are WARNING; non-allowlisted matches
are ERROR
- **Stale-detection**: allowlist entries that no longer trigger are
ERROR (forces shrink)

`.pre-commit-config.yaml`: `no-direct-mongo` +
`no-direct-mongo-in-services` → single `repo-pattern-guard` hook.

### C. `03-complexity.sh` rewrite
- Switched from `git archive` baseline diff to **function-level
ALLOWLIST** (`<file>::<func>`)
- **Discovers ruff** via PATH first, then known venv locations
(`$REPO_ROOT/services/claw-interface/.venv/bin/ruff`,
`/home/node/.venvs/claw-interface/bin/ruff`); **hard-fails if none
found** — fixes the silent-pass bug in the previous version (when `ruff`
was missing, `grep "C901"` of empty stdin returned empty and the script
exited 0 reporting "all clean")
- 8 known violators grandfathered: 3 in `litellm.py`, 3 in
`session/chat.py`, plus `orders.py::create_order` and
`billing.py::_do_billing_init`
- Stale-detection identical to 02

### D. `05-no-new-collection-name-constants.sh` →
`05-no-collection-name-constants.sh`
**Strict mode** — no diff, no allowlist, no base-ref dependency. Any
`*_COLLECTION = "..."` assignment or `COLLECTION_NAME` reference in
`app/routes/`, `app/services/`, or `app/cron/` is now ERROR.

This was made possible by the collections.py canonicalization in this
same PR.

### E. `app/database/collections.py` canonicalization
Added 4 new constants and removed all duplicate local definitions:

| New canonical | Replaces local def in |
|---|---|
| `SESSION_TASKS_COLLECTION` | `session/utils.py`,
`scripts/backfill_preview_assets.py`, 4 BDD tests |
| `SESSION_JOB_COLLECTION` | `session/utils.py`, `scheduler.py`, 3 BDD
tests |
| `SESSION_ASSETS_COLLECTION` | `session/utils.py`,
`scripts/backfill_preview_assets.py`, 1 BDD test |
| `CANVAS_COLLECTION` | `session/utils.py`, 1 BDD test |
| (existing `ACCOUNT_COLLECTION`) | replaces `USER_COLLECTION` /
`USERS_COLLECTION` in `subscription_cron.py`,
`session/{utils,chat,canvas}.py`, `helpers.py`, 5 BDD tests |

Plus `ORDER_COLLECTION` substituted for local `ORDERS_COLLECTION` in 4
BDD tests.

## Test plan
- [x] All 5 ci-lint scripts: PASS locally
- [x] `pyright app/ tests/`: 0 errors
- [x] `ruff check app/ tests/ scripts/`: clean
- [x] `ruff format`: applied (1 file reformatted)
- [x] `.git/shallow` no longer regenerated by lint runs after the fix
- [x] pre-commit hook stack passes (Pyright Type Check + all custom
hooks)
- [ ] CI: `claw-interface-quality` (custom_lint_scripts_dir) green
- [ ] CI: `code-quality / lint-and-test` (web/) green —
`check-ignores-shrink-only.sh` step still has access to
`origin/main:web/eslint.config.mjs` via `actions/checkout`
- [ ] CI: BDD pyright + pytest for refactored test imports
- [ ] Spot-check: `02-repo-pattern-guard.sh` stale-detection — try
removing one allowlisted file from disk locally; expect ERROR

## Out of scope (follow-ups)
- Refactor the 4 grandfathered `session/*.py` routes off direct mongo
(tracked under broader routes-to-repo migration)
- Refactor the 8 grandfathered C901 complex functions
- Investigate residual `--depth=1` fetcher: `.git/shallow` regenerated
once during this session **after** the script changes, so something else
(IDE? other hook?) still does depth=1 fetches occasionally — needs
separate investigation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [f2ac66e](https://github.com/SerendipityOneInc/ecap-workspace/commit/f2ac66e1474f85778d10d3564bdc577e225e51d6) feat: inject per-agent heartbeat delivery config (#770)

**作者**: tim-srp  
**SHA**: `f2ac66e1474f85778d10d3564bdc577e225e51d6`

```
## Summary

- Add per-agent `heartbeat` config (`target`, `accountId`, `to`) to each
agent entry in `agents.list` during `apply_agents_list()`
- Resolve `mm_user_id` from MongoDB in `deploy_selected_agents()` and
pass it through
- Existing agents without heartbeat config get backfilled on next
deployment
- Fixes silent heartbeat misdelivery in multi-bot Mattermost deployments
with `per-account-channel-peer` dmScope

## Changes

- `agent_deploy.py`: `apply_agents_list()` accepts `mm_user_id`, builds
heartbeat config per agent
- `agent_deploy.py`: `deploy_selected_agents()` reads `mm_user_id` from
`openclaw_bots[0].mattermost_user.user_id`

## Heartbeat config logic

| Agent | target | accountId | to |
|-------|--------|-----------|-----|
| main | mattermost | _(not set)_ | user:{mm_user_id} |
| sub-agent | mattermost | {agent_id} | user:{mm_user_id} |

## Test plan

- [ ] Deploy a new bot, verify main agent has heartbeat config in
agents.list
- [ ] Install a sub-agent, verify it has heartbeat with correct
accountId and to
- [ ] Confirm heartbeat messages deliver to the correct Mattermost
user/bot

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
Co-authored-by: Copilot Autofix powered by AI <62310815+github-advanced-security[bot]@users.noreply.github.com>
```

### [9c42d35](https://github.com/SerendipityOneInc/ecap-workspace/commit/9c42d350ed25ed571bd5b1270cc65e06c54e89c0) chore(claude): register sentry plugin in shared settings (#838)

**作者**: Chris@ZooClaw  
**SHA**: `9c42d350ed25ed571bd5b1270cc65e06c54e89c0`

```
## Summary

启用 \`sentry@claude-plugins-official\` 到团队共享的
\`.claude/settings.json\`，让队友切到 main 后无需 \`/plugin install\` 即可拿到 sentry
相关 skill（sentry-workflow / sentry-sdk-setup / sentry-feature-setup /
seer 等）。

## Test plan
- [x] JSON 语法校验通过（\`python -m json.tool\`）
- [x] 单行变更，与现有 enabledPlugins 列表条目格式一致

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [17c6a69](https://github.com/SerendipityOneInc/ecap-workspace/commit/17c6a692e8338924f3ae28e99da3a2f71dd41041) refactor(claw-interface): drop direct mongo from mattermost_provisioner (#837)

**作者**: Chris@ZooClaw  
**SHA**: `17c6a692e8338924f3ae28e99da3a2f71dd41041`

```
## Summary

**系列收尾 PR** —— 合并后 \`04-no-direct-mongo-in-services.sh\` **彻底清空 WARNING
列表**,services 层完成 mongo→repo 迁移。

### 新增 \`openclaw_repo\` 原语(1 个)
- \`push_to_array(uid, array_path, item)\` —— \`\$push\` 到嵌套数组,镜像既有
\`pull_from_array\`。

### \`mattermost_provisioner.py\` 迁移(10 处调用)
| 类别 | 原代码 | 新代码 |
|---|---|---|
| read(×4)| \`mongo.read_one(COLL, {"uid": uid})\` |
\`openclaw_repo.get_user(uid)\` |
| 单字段 mm_user | \`mongo.update(COLL, {...},
{"openclaw_bots.0.mattermost_user": data})\` |
\`openclaw_repo.set_bot_field(uid, "mattermost_user", data)\` |
| 多字段 \`\$set\` dot-path(×3)| \`mongo.update/mongo.db[COLL].update_one\`
with \`\$set\` | \`openclaw_repo.update_fields(uid, {...})\` |
| 数组初始化 | \`mongo.update(COLL, {...}, {array_path: [item]})\` |
\`openclaw_repo.update_fields(uid, {array_path: [item]})\` |
| \`\$push\` 嵌套数组(×2)| \`mongo.db[COLL].update_one({...}, {"\$push":
{path: item}})\` | \`openclaw_repo.push_to_array(uid, path, item)\` |

同时删除 \`COLLECTION_NAME = "ecap-account"\` 常量。

### 测试改动
- 17 个 \`@patch(mongo)\` 改为 \`@patch(openclaw_repo)\`
- 两处原本伸手到 \`mongo.db[COLL].update_one\` 内部的断言改成直接断言对应 repo
方法(\`push_to_array\` / \`update_fields\`)
- \`push_to_array\` 通过 provisioner 两处调用间接覆盖(与既有 \`pull_from_array\` 无专用
repo 单测的处理一致)

## Verification
- [x] \`bash scripts/ci-lint/04-no-direct-mongo-in-services.sh\` — **零
WARNING** 🎉
- [x] \`ruff check\` / \`ruff format\` 全绿
- [x] \`pyright app/ tests/\` — 0 errors
- [x] \`pytest tests/unit/test_mattermost_provisioner.py\` — 21 passed
- [x] \`pytest tests/unit/\` 全量 — 2336 passed / 2
failed(\`test_skill_injector.py\`,main 上 pre-existing,与本 PR 无关)
- [x] BDD \`openclaw / mattermost / connector\` 域 — 98 passed(按
CLAUDE.md 环境变量)

## Series recap
| PR | 对象 | WARNING 列表 |
|---|---|---|
| #832 | bot_resources | 5 → 4 |
| #833 | apple_subscription_manager | 4 → 3 |
| #835 | mattermost_reconcile | 3 → 2 |
| #836 | connector_store(+2 新 \`user_repo\` 方法)| 2 → 1 |
| **this** | mattermost_provisioner(+1 新 \`openclaw_repo\` 方法)| **1 →
0** |

## Test plan
- [ ] CI \`code-quality\` 全绿
- [ ] CI \`claw-interface-quality / test\` 覆盖率 ≥ 90%
- [ ] CI \`python-duplication-check\` 无新增重复

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [9b7ae5f](https://github.com/SerendipityOneInc/ecap-workspace/commit/9b7ae5f29609452fea695ee0d13658a39d0b80e8) ci: enforce 2000-line PR size budget with fail-fast gate (#834)

**作者**: Chris@ZooClaw  
**SHA**: `9b7ae5f29609452fea695ee0d13658a39d0b80e8`

```
## Summary

- 新增 \`pr-size-check-reusable.yml\`（callable workflow）：计算 PR 加+删 行数，超过阈值
fail check 并在 PR 评论；非 PR 触发时静默 skip，让 caller 可以无条件 \`needs: size\`
- 新增 \`pr-size-check.yml\`（独立 entry，无 path filter）：所有 PR 必跑，发 sticky 评论
- 改 \`code-quality.yml\`：加 \`size\` job 调 reusable（\`post_comment:
false\`），让 \`web-quality / ios-quality / claw-interface-quality /
python-duplication-check\` 都 \`needs: size\` —— size 不过，重活全
skip（fail-fast，节省 GH Actions 配额）

## 设计要点

| 维度 | 设定 |
|---|---|
| 阈值 | \`MAX_LINES=2000\`（顶层 input 默认值，要改一行即可） |
| 触发 | \`pr-size-check.yml\` 在 PR opened/sync/reopened/labeled/unlabeled
时跑；\`code-quality.yml\` 串联到现有的 paths-filter 链路 |
| 排除 | lockfiles (pnpm/npm/yarn/uv/poetry/cargo/go.sum) ·
\`docs/superpowers/{plans,specs}/**\` · CHANGELOG ·
\`__generated__/__snapshots__/*.snap\` · openapi · **i18n 文案
(\`locales/**\`, \`messages/**\`, \`translations/**\`,
\`*.po/*.pot/*.xliff/*.xlf\`)** · 图片/字体/pdf/bin |
| Bypass | PR 加 \`size-override\` label 即跳过（label/unlabel 也会重跑 workflow）
|
| 行为 | Sticky 评论（含阈值/实际/Top10 大文件） + fail check（不自动 close） |

## 拓扑

\`size\` 与 \`changes\` 都是 root job，并行跑；4 个重活 job + gate job 全部 \`needs:
[size, changes]\`。这样：
- size fail → 重活 skip（fail-fast）
- size pass → 延迟 ≈ max(size, changes) 而非串行相加
- 非 PR 触发（push / workflow_dispatch）reusable 内部所有 step \`if:
github.event_name == 'pull_request'\`，job 整体仍 success → \`needs: size\`
不阻塞

## 验证

- [x] YAML \`yaml.safe_load\` 校验通过（3 个文件）
- [x] 真实数据：拿 PR#830 跑过 exclusion 规则——原始 10,319 行 → 排除后 6,845 行（含 i18n
排除前）→ 预期会触发 fail check ✅
- [x] 本 PR 自检：244 行变更，远低于 2000 阈值（应在自身 CI 中 PASS）
- [ ] 实际 CI 跑通后建议把 \`pr-size-check / size-check\` 加入 branch protection 的
required checks

## 后续 follow-up（独立 PR）

- 抽 \`scripts/check-pr-size.sh\` 共享脚本，加 husky pre-push hook
做本地速反馈（"开发期体验"层，CI 仍是合规层）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [bd48992](https://github.com/SerendipityOneInc/ecap-workspace/commit/bd489925587ec5c6b740bf5181a2fc4698052ce3) refactor(claw-interface): drop direct mongo from connector_store (#836)

**作者**: Chris@ZooClaw  
**SHA**: `bd489925587ec5c6b740bf5181a2fc4698052ce3`

```
## Summary

### 新增 `user_repo` 原语(2 个)
- `upsert_fields(uid, fields) -> bool` — \`\$set\` + \`upsert=True\`。与现有
`upsert_on_insert`(\`\$setOnInsert\`,命中时 no-op)**正交**:本方法无论新老文档都会写
fields。
- `unset_fields(uid, field_paths) -> int` — 纯 \`\$unset\`,支持
dot-path。空列表直接 no-op 返回 0。

### `connector_store.py` 迁移(3 处调用)
| 原代码 | 新代码 |
|---|---|
| `mongo.upsert_document(coll, {"uid": uid}, values)` |
`user_repo.upsert_fields(uid, values)` |
| `mongo.read_one(coll, {"uid": uid})` | `user_repo.get_user(uid)` |
| `mongo.db[coll].update_one({"uid": uid}, {"\$unset": {...}})` |
`user_repo.unset_fields(uid, [f"connectors.{service}"])` |

同时去掉 `COLLECTION_NAME = "ecap-account"` 常量别名。

### Test coverage
- `TestUpsertFields` 固定 \`\$set\` + \`upsert=True\` query shape(new doc
/ existing doc 两条分支)
- `TestUnsetFields` 固定单字段 / 多字段 / 空列表 no-op 三种行为
- `test_connector_store.py` 重写 patch 点从 `mongo` 到 `user_repo`,并**新增**
`TestRemoveConnectorToken`(原先没有该函数的测试)

### 系列进度
- `04-no-direct-mongo-in-services.sh` WARNING 列表 2 → 1,只剩
mattermost_provisioner
- 继 #832 / #833 / #835 之后的第 4 个 PR;剩最后 1 个(mattermost_provisioner)

## Verification
- [x] `bash scripts/ci-lint/04-no-direct-mongo-in-services.sh` —
connector_store 已移出
- [x] `ruff check` / `ruff format` 全绿
- [x] `pyright app/ tests/` — 0 errors
- [x] `pytest tests/unit/test_user_repo.py
tests/unit/test_connector_store.py tests/unit/test_connector_base.py
tests/unit/test_connector_coverage.py
tests/unit/test_connector_status.py` — 60 passed
- [x] BDD `tests/bdd/step_defs/test_connectors.py`(按 CLAUDE.md 环境变量)— 7
passed

## Test plan
- [ ] CI \`code-quality\` 全绿
- [ ] CI \`claw-interface-quality / test\` 覆盖率 ≥ 90%(新增 2 个方法均有测试)
- [ ] CI \`python-duplication-check\` 无新增重复

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [1104ec3](https://github.com/SerendipityOneInc/ecap-workspace/commit/1104ec35a4c1fd7e163325a05a1db64f6e2e6859) refactor(claw-interface): drop direct mongo from mattermost_reconcile (#835)

**作者**: Chris@ZooClaw  
**SHA**: `1104ec35a4c1fd7e163325a05a1db64f6e2e6859`

```
## Summary
两处调用迁到 repo 层:

| 原代码 | 新代码 |
|---|---|
| `mongo.db[COLLECTION_NAME].update_one({"uid": uid}, {"\$set":
{f"openclaw_bots.0.mattermost_bots.{idx}.channel_injected": False}})` |
`user_repo.update_fields(uid,
{f"openclaw_bots.0.mattermost_bots.{idx}.channel_injected": False})` |
| `mongo.read_one(COLLECTION_NAME, {"uid": uid}) or {}` |
`user_repo.get_user(uid) or {}` |

- `user_repo.update_fields` 内部就是 \`\$set\`(user_repo.py:100-102),语义等价、支持
dot-path + f-string 动态索引,**无需新 repo 方法**。
- 同时去掉从 `mattermost_provisioner` 跨模块 import 的 `COLLECTION_NAME`——service
之间不再需要传递 collection 字符串。
- `mattermost_reconcile.py` 没有专用 unit test;下游 endpoint 测试通过
`patch("app.services.mattermost_reconcile.reconcile_mattermost_channels",
...)` mock 顶层函数,不触及内部 mongo 调用,不受影响。
- 系列目标:收尾 `services/` 层的 mongo→repo 迁移。继 #832 / #833 之后的第 3 个 PR,剩 2
个(connector_store / mattermost_provisioner)待迁。

## Verification
- [x] `bash scripts/ci-lint/04-no-direct-mongo-in-services.sh` — WARNING
列表 3 → 2,mattermost_reconcile 不再出现
- [x] `ruff check` / `ruff format` 全绿
- [x] `pyright app/ tests/` — 0 errors
- [x] `pytest tests/unit/test_openclaw_bot_config.py
tests/unit/test_openclaw_endpoints_extra.py` — 44 passed(reconcile
的所有下游调用方)

## Test plan
- [ ] CI \`code-quality\` 全绿
- [ ] CI \`claw-interface-quality / test\` 覆盖率 ≥ 90%
- [ ] CI \`python-duplication-check\` 无新增重复

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [977dd54](https://github.com/SerendipityOneInc/ecap-workspace/commit/977dd54d4a9cb52b171bc2a8ee427a19bacb85ad) refactor(claw-interface): drop direct mongo from apple_subscription_manager (#833)

**作者**: Chris@ZooClaw  
**SHA**: `977dd54d4a9cb52b171bc2a8ee427a19bacb85ad`

```
## Summary
- `app/services/apple_subscription_manager.py` 改走 repo
层:`mongo.read_one(USERS_COLLECTION, {"uid": uid})` →
`user_repo.get_user(uid)`;收尾的 Apple 审计字段 `mongo.update(..., {...apple
fields})` → `user_repo.update_fields(uid, {...})`。删除 `USERS_COLLECTION`
常量 + `favie_common.database.mongo_client` 直接导入。
- 订阅核心状态(plan / cycle / subscription_end_time)仍由 `transition_to_active`
写入,本 PR 只把末尾的 Apple-识别字段写入迁到 repo 层——行为/集合/字段完全等价。
- **没有**用 `user_repo.update_subscription_info`:那是 Stripe 专用契约(写
`stripe_*` 字段),与 Apple schema 无关。
- 对应单元测试从 `patch("...mongo")` 迁到 `patch("...user_repo")`,更新 2-arg repo
签名下的断言索引(`call_args[0][1]` 是 fields),并加 `assert_awaited_once_with(uid)`
锁定调用契约。
- 系列目标:收尾 `services/` 层的 mongo→repo 迁移。PR1 (#832) 之后的第 2 个 PR;剩 3
个文件(connector_store / mattermost_reconcile / mattermost_provisioner)待迁。

## Verification
- [x] `bash scripts/ci-lint/04-no-direct-mongo-in-services.sh` — WARNING
列表 4 → 3,apple_subscription_manager 不再出现
- [x] `ruff check` / `ruff format --check` 全绿
- [x] `pyright app/ tests/` — 0 errors
- [x] `pytest tests/unit/test_apple_subscription_manager.py
tests/unit/test_apple_service.py tests/unit/test_apple_routes.py` — 41
passed
- [x] BDD `tests/bdd/step_defs/test_apple_subscription.py`(按 CLAUDE.md
指定环境变量)— 7 passed

## Test plan
- [ ] CI `code-quality` 全绿
- [ ] CI `claw-interface-quality / test` 覆盖率 ≥ 90%
- [ ] CI `python-duplication-check` 无新增重复

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [2f535c4](https://github.com/SerendipityOneInc/ecap-workspace/commit/2f535c439307fa81f2eb5713dadf88d6bdf021da) refactor(claw-interface): drop direct mongo from bot_resources (#832)

**作者**: Chris@ZooClaw  
**SHA**: `2f535c439307fa81f2eb5713dadf88d6bdf021da`

```
## Summary
- `app/services/bot_resources.py` 改用 `user_repo.get_user(uid)` 替代
`mongo.read_one(USERS_COLLECTION, {"uid": uid})`,同时删除不再需要的
`USERS_COLLECTION` 常量与 `favie_common.database.mongo_client` 直接导入。
- 对应测试 `tests/unit/test_bot_resources.py` 的 10 处
`patch("...bot_resources.mongo")` 迁移到
`patch("...bot_resources.user_repo")`,符合 CLAUDE.md "Patch the importing
module, not the repo" 约定。
- 系列目标:收尾 `services/` 层的 mongo → repo 迁移;本 PR 是 5 个计划 PR 中的第 1 个(最小,无新增
repo 方法)。

## Verification
- [x] `bash scripts/ci-lint/04-no-direct-mongo-in-services.sh` — WARNING
列表从 5 个减到 4 个,bot_resources 不再出现
- [x] `ruff check app/ tests/` 全绿
- [x] `ruff format --check` 全绿
- [x] `pyright app/ tests/` — 0 errors, 0 warnings, 0 informations
- [x] `pytest tests/unit/test_bot_resources.py` — 14 passed
- [x] `pytest tests/unit/` 全量 2330 passed(2 个 `test_skill_injector.py`
失败与本 PR 无关,main 上已存在)

## Test plan
- [ ] CI `code-quality` 全绿
- [ ] CI `claw-interface-quality` 覆盖率 ≥ 90%
- [ ] CI `python-duplication-check` 无新增重复

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [e954517](https://github.com/SerendipityOneInc/ecap-workspace/commit/e954517e5d012decaf1c7a0a264dcecd9da86a1f) test(claw-interface): BDD integration tests for redeem_gift_code CAS + rollback (#831)

**作者**: Chris@ZooClaw  
**SHA**: `e954517e5d012decaf1c7a0a264dcecd9da86a1f`

```
## Summary

Follow-up from PR #823 code review — adds BDD integration tests for the
gift-code redemption flow against a real MongoDB instance. Closes #825.

Covers the four paths the issue called out:

- **Happy path** — counter bumps, activation record written, credits
returned
- **Concurrent redemption (`max_activations=1`)** — `asyncio.gather` on
two redeem calls; verifies the `claim_activation` CAS guard under real
contention: exactly one succeeds, one gets 400 `code_exhausted`
- **`create_activation` failure** — exercises the rollback path added in
61b55fe7e; confirms the `{current_activations: {$gt: 0}}` filter in
`rollback_activation` actually matches real docs
- **Billing-gateway failure** — same rollback guarantee, additionally
verifies that the activation record `delete_one` filter matches

Zero business-code changes — two new test files only.

## Test plan

- [x] `TEST_MONGODB_HOST=127.0.0.1 MONGODB_USER= MONGODB_PASSWORD=
pytest tests/bdd/step_defs/test_gift_code.py -v` — 4/4 pass locally
- [x] Full BDD suite — 342/342 pass, no regressions
- [x] `ruff check` + `ruff format` clean
- [x] `pyright` clean on new file
- [x] File length 245 lines (under 500-line cap)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [fe70265](https://github.com/SerendipityOneInc/ecap-workspace/commit/fe70265cef56c89f3e8435375dea1863df34c563) fix(web): resolve WebSocket reconnect loop after bot restart (#810)

**作者**: bryce-srp  
**SHA**: `fe70265cef56c89f3e8435375dea1863df34c563`

```
When a bot pod restarts, the webchat token changes but the reconnect
loop keeps using the stale token. silentRetry fetches fresh bot info,
but the auto-connect effect skips because it only checks bot_id
(unchanged).

Two fixes:
- Track `bot_id:token` composite key in auto-connect so a token change
triggers ws.connect with the new credentials
- Expand visibility handler to also cover 'reconnecting' status,
ensuring iOS tab resume triggers a re-init instead of looping with stale
state

Co-authored-by: Bryce <bryce@Bryces-Mac-mini-M4-PRO.local>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [c02ae72](https://github.com/SerendipityOneInc/ecap-workspace/commit/c02ae722152ff8cfe0f0af11f15d1281ce3670a4) refactor(claw-interface): new openclaw_conversation_repo, migrate route (#829)

**作者**: Chris@ZooClaw  
**SHA**: `c02ae722152ff8cfe0f0af11f15d1281ce3670a4`

```
## Summary

Continuation of route mongo→repo migration (#817 / #818 / #822 / #823 /
#826 / #827). Migrates \`app/routes/openclaw_conversation.py\` — 5 raw
mongo calls moved to \`user_repo\` (1) and a **new
\`openclaw_conversation_repo\`** (4) wrapping the
\`ecap-openclaw-tasks\` collection.

### New \`openclaw_conversation_repo\`

- \`list_for_uid(uid, *, limit)\` — newest-first page via Motor cursor,
\`_id\` projected out so the route can hand docs straight to Pydantic.
- \`upsert_task(uid, session_key, *, set_fields, set_on_insert)\` —
\`\$set\` + \`\$setOnInsert\` upsert keyed on \`(uid, session_key)\`.
Caller decides which fields are every-sync (status/updated_at) vs
first-write-only (created_at / empty preview default).
- \`mark_missing_as_done(uid, live_keys)\` — close out tasks whose
runtime session disappeared. Filter gates on \`status: {\$ne:
\"done\"}\` so a re-sync doesn't churn writes on already-done records.
- \`delete_for_uid(uid)\` — purge all tasks on bot Recreate, returns
\`deleted_count\`.

### Also

- New collection constant \`OPENCLAW_TASKS_COLLECTION =
\"ecap-openclaw-tasks\"\` in \`collections.py\`.
- Drops local \`TASKS_COLLECTION\` / \`ACCOUNT_COLLECTION\` constants.

CI guard: \`openclaw_conversation.py\` absent from WARNING list.
(\`orders.py\` still shows as WARNING here because this PR is based on
the commit before #827 — the two PRs are independent.)

## Test plan

- [x] \`ruff check app/ tests/\` — clean
- [x] \`pyright app/ tests/\` — 0 errors
- [x] New repo: 4 tests pinning Motor cursor pipeline + upsert +
close-out + delete query shapes
- [x] Route tests: rewritten to mock the repo at its boundary (no fake
mongo module)
- [x] \`pytest\` on both test files — 9 passed
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [8c98f70](https://github.com/SerendipityOneInc/ecap-workspace/commit/8c98f702f50555b3ca329f56c28d5d5bcfc7869d) refactor(claw-interface): drop direct mongo from orders route (#827)

**作者**: Chris@ZooClaw  
**SHA**: `8c98f702f50555b3ca329f56c28d5d5bcfc7869d`

```
## Summary

Continuation of route mongo→repo migration (#817 / #818 / #822 / #823 /
#826).
Migrates \`app/routes/orders.py\` — 8 raw \`mongo.*\` calls →
\`user_repo\` / \`orders_repo\` helpers.

### New \`orders_repo\` methods

- \`create_order(doc)\` — generic order insertion. Existing
\`create_renewal_order\` stays scoped to the renewal flow so call sites
make the intent explicit.
- \`count_for_uid(uid)\` — total orders for a user (pagination totals).
- \`list_for_uid(uid, *, limit, offset)\` — newest-first page of a
user's orders (\`created_time\` descending).

### Small hardening

\`get_order\` previously had a latent path where passing neither
\`order_id\` nor \`session_id\` hit \`mongo.read_one({})\` and returned
whatever the DB picked first. Splitting the read into
\`get_by_order_id\` / \`get_by_session_id\` + an explicit \`400\` closes
that path.

### Also

- Drops local \`USERS_COLLECTION\` / \`ORDERS_COLLECTION\` constants.
- \`mock_orders_repo\` shared fixture gets \`create_order\` /
\`count_for_uid\` / \`list_for_uid\` wired up.

CI guard: WARNING list shrinks from 3 in-scope files (session/* legacy
carve-out) to 2 (\`openclaw_conversation\` + the intentionally-untouched
session routes).

## Test plan

- [x] \`ruff check app/ tests/\` — clean
- [x] \`pyright app/ tests/\` — 0 errors
- [x] \`pytest\` on \`test_orders_endpoints.py\` +
\`test_orders_trial_logic.py\` + \`test_orders_repo.py\` — 54 passed
- [x] \`02-no-direct-mongo-in-routes.sh\` — \`orders.py\` absent from
WARNING list
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [7f605a7](https://github.com/SerendipityOneInc/ecap-workspace/commit/7f605a744a62a89043764d601ddfca4c68d1cb00) feat(tips): Prompt Gallery entries + userguide section polish (#819)

**作者**: vincent-srp  
**SHA**: `7f605a744a62a89043764d601ddfca4c68d1cb00`

```
## Summary
- **UserMenu**: rename "Use Tips" → "Prompt Gallery" (external link to
zooclaw.ai/tips); add new "What's New" entry that opens the guide tour
(prior Use Tips behavior)
- **Landing Resources dropdown**: insert "Prompt Gallery" →
zooclaw.ai/tips; fix dropdown transparency on landing/userguide/pricing
(`.nav-dropdown-menu > div` selector never matched `<li>` children)
- **Userguide page**:
  - Skip onboarding auto-open and guide-tour auto-pop on `/userguide`
  - Header now compacts to pill on scroll (matching landing)
- Chapter 3 "Usage Tips" → "Ways to Use" / "打开方式" — reduces semantic
overlap with Prompt Gallery
- Tip section redesigned as 3×2+1 grid with 3D flip cards: front =
number + title (clean), back = full description + example quote (on
hover). 7th cell "Explore More" uses same flip interaction, reveals
"Prompt Gallery →" on hover, links to zooclaw.ai/tips
  - Sidebar TOC labels synced to match renamed section

## Test plan
- [ ] UserMenu shows "Prompt Gallery" and "What's New" (both EN + ZH)
- [ ] Landing Resources dropdown has dark bg/border and includes Prompt
Gallery
- [ ] `/userguide` — no Welcome overlay, no auto guide tour, header
compacts on scroll
- [ ] `/userguide` Ch.3 — 7-cell grid, cards flip on hover, info intact
on back, sidebar label matches

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>
```

### [5399d48](https://github.com/SerendipityOneInc/ecap-workspace/commit/5399d48419dea7fa2cd258dfc5efb85168f5a7f6) refactor(claw-interface): drop direct mongo from openclaw_settings route (#826)

**作者**: Chris@ZooClaw  
**SHA**: `5399d48419dea7fa2cd258dfc5efb85168f5a7f6`

```
## Summary

Continuation of the route mongo→repo migration series (#817 / #818 /
#822 / #823). Migrates \`app/routes/openclaw_settings.py\` — 10 raw
\`mongo.read_one\`/\`mongo.update\` calls on \`ACCOUNT_COLLECTION\` →
\`user_repo.get_user\` / \`user_repo.update_fields\`. **Zero new repo
methods needed.**

The updates use MongoDB dotted-path \`\$set\` keys like
\`openclaw_bots.0.status\` and \`locale.timezone\` — these pass through
\`user_repo.update_fields\` unchanged, so behavior is identical.

Also drops the local \`COLLECTION_NAME = \"ecap-account\"\` constant.

## Test plan

- [x] \`ruff check app/ tests/\` — clean
- [x] \`pyright app/ tests/\` (full-repo scope) — 0 errors
- [x] \`pytest\` on \`test_openclaw_settings_routes.py\` +
\`test_openclaw_settings_coverage.py\` — 148 passed
- [x] \`02-no-direct-mongo-in-routes.sh\` — \`openclaw_settings.py\`
absent from WARNING list
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [91cdc37](https://github.com/SerendipityOneInc/ecap-workspace/commit/91cdc371ad1990d305cc91cfbbb20695e81304e6) refactor(claw-interface): new gift_code_repo + cron_run_repo, migrate 2 more route holdouts (#823)

**作者**: Chris@ZooClaw  
**SHA**: `91cdc371ad1990d305cc91cfbbb20695e81304e6`

```
## Summary

Continuation of #817 / #818 / #822. Two more route-layer holdouts
migrated — this batch needs **two new repos** because there's no
existing coverage for gift codes or cron run records.

### New repos

- **\`gift_code_repo\`** — wraps \`ecap-gift-codes\` +
\`ecap-gift-code-activations\`. Mirrors \`invite_code_repo\`'s "Read /
Create / Atomic" layout. The \`claim_activation\` (CAS on
\`current_activations\`) and \`rollback_activation\` (compensating
\`\$inc\` + \`delete\`) primitives are load-bearing for over-redemption
prevention and are pinned by dedicated tests.
- **\`cron_run_repo\`** — wraps \`ecap-cron-runs\` lifecycle:
\`create_run\` (inserts "running"), \`mark_completed\` / \`mark_failed\`
(keyed by \`_id\` so run_id collisions can't flip the wrong doc),
\`get_by_run_id\` / \`list_runs\` (both project out \`_id\` for clean
JSON).

### Also

- Added \`CRON_RUNS_COLLECTION = \"ecap-cron-runs\"\` to
\`collections.py\` — previously hardcoded in the route, violating the
spirit of \`05-no-new-collection-name-constants.sh\`.
- Dropped the \`GIFT_CODE_COLLECTION\` re-export from
\`app.services.gift_code\` (was only used by the route to pass to raw
\`mongo.*\` calls; now unused).
- \`app/services/gift_code.py\` and the two routes no longer import
\`favie_common.database.mongo_client\`.

CI guard: WARNING list shrinks from **9 → 7** route files.

## Test plan

- [x] \`ruff check app/ tests/\` — clean
- [x] \`ruff format\` — two files auto-wrapped (gift_code tests)
- [x] \`pyright app/ tests/\` (full-repo scope) — 0 errors
- [x] \`pytest\` on 4 affected files — 60 passed
- [x] \`pytest tests/unit/\` full suite — 2320 passed (2 pre-existing
\`test_skill_injector\` failures, same as in #817-#822)
- [x] \`bash scripts/ci-lint/02-no-direct-mongo-in-routes.sh\` —
\`gift_code.py\` and \`admin_cron.py\` absent from WARNING list
- [x] \`bash scripts/ci-lint/04-no-direct-mongo-in-services.sh\` —
\`services/gift_code.py\` no longer touches \`mongo\`
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [02ff5b7](https://github.com/SerendipityOneInc/ecap-workspace/commit/02ff5b73511c7e35b5fb0e1674261c0b88ab20db) refactor(web): branded paywall module → scoped CSS (#796 PR 2/5) (#820)

**作者**: Chris@ZooClaw  
**SHA**: `02ff5b73511c7e35b5fb0e1674261c0b88ab20db`

```
## Summary

Issue #796 paywall domain 第 2/5 PR —— 把 3 个 paywall 文件的 ~20 处 inline
style 抽成独立 CSS module (.paywall-root + --paywall-* scoped tokens)，消除
file-level eslint-disable，沿用 PR #816 (login) 的样板。

## 变更

- **新建** `web/src/components/paywall.css`：`.paywall-root` scoped，17 个
  `--paywall-*` token（固定品牌色板 #1a1a18 + 8 档 rgba 灰阶 + 独立 error /
  FAB shadow），不随 dark/light 切换
- **重构 3 文件**：`PaywallContent.tsx` / `GiftPaywallFab.tsx` /
  `GiftPaywallModal.tsx`
- 删除文件顶部 `/* eslint-disable [no-restricted-syntax |
react/forbid-dom-props] */`
  - ~20 处 inline style 全部迁移到 CSS module
  - `GiftPaywallFab` 挂载动画 `transform: mounted ? 'scale(1)' : 'scale(0)'`
    改为 CSS class toggle (`.gift-paywall-fab--mounted`)
  - `GiftPaywallModal` close 按钮 `onMouseEnter/Leave` → CSS `:hover`；
    `.paywall-compare-link` hover 同理
- **`web/eslint.config.mjs`**：从 `react/forbid-dom-props` ignores 列表删除
  `GiftPaywallFab.tsx` + `GiftPaywallModal.tsx` 共 2 条
- **顺手修复 dark-mode bug**：原 `GiftPaywallModal` close 按钮用
  `var(--color-text-tertiary)` 全局 theme token，在 dark 主题下会翻成浅色显
  示在固定白底卡片上看不见；现改用 `--paywall-text-muted` scoped token，保
  持品牌一致性
- **`<style jsx global>` keyframes 保留**：`GiftPaywallFab` 的 ~330 行礼盒动
  画非 color-palette 范畴，扩散超出本 issue 范围，不动

## 为什么拆 5 个 PR

PR #816 (login) 的延续；issue body 推荐「一个 domain = 一个 PR」+ memory
「serial PR」约定。本 PR 仅 paywall domain，剩余 onboarding / pricing /
public / userguide 为后续 3 个 PR。

## 防回归

- SHRINK-ONLY 守卫（`web/scripts/check-ignores-shrink-only.sh`，#804 引入）：
  main 47 → HEAD 45 ✅ 永久不能回增
- Design spec
`docs/superpowers/specs/2026-04-15-branded-modules-login.md`
  (PR #816 引入) 的 token 命名/className 分层约定在本 PR 完整复用，包括：
  `.{domain}-root` 作用域锚点 / `.login-card *` 风格的 reset 收窄
  (本 PR 对应 `.paywall-root .paywall-card *`) / `:hover` 伪类替代 JS handler

## Test plan

- [x] `pnpm lint` 绿（3 文件从 file-level disable 移除后，
      `react/forbid-dom-props` + `no-restricted-syntax` 双规则生效无违规）
- [x] `pnpm tsc --noEmit` 绿
- [x] `pnpm test`：2216 tests passed
- [x] `bash web/scripts/check-ignores-shrink-only.sh` passed (47→45)
- [ ] **视觉对比** staging vs main（合并前 deploy staging）：
  - [ ] GiftPaywallFab：浮动按钮挂载动画 (scale 0 → 1)；礼盒 keyframes 正常
  - [ ] GiftPaywallModal：打开动画；close 按钮 hover；backdrop blur
- [ ] PaywallContent：billing toggle Monthly/Annually 切换；"2 months free"
        badge；$0 价格块 + motion.span 年付/月付切换；features 列表；CTA hover
        + disabled 态；Compare all plans link hover
- [ ] **dark 主题验证**（bug fix 核心）：切到 dark 主题打开 paywall，close 按
      钮应仍然**可见**（原 bug：全局 theme 翻转后消失）
- [ ] 键盘 tab：CTA / Compare link / close 按钮 focus 指示

## 关联

- #796 (总 issue)
- #816 (PR 1 — login，已合并 28009fe04)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [be11d72](https://github.com/SerendipityOneInc/ecap-workspace/commit/be11d72bd090041c22f8637b9717ca4bda91e054) refactor(claw-interface): drop direct mongo from archived / openclaw_admin + twilio lgtm cleanup (#822)

**作者**: Chris@ZooClaw  
**SHA**: `be11d72bd090041c22f8637b9717ca4bda91e054`

```
## Summary

Continuation of #817 / #818. Migrates two more route-layer holdouts to
\`user_repo\`:

- \`session/archived.py\` — 2 late-imported \`mongo.read_one\` →
\`user_repo.get_user\`
- \`openclaw_admin.py\` — 4 calls to \`user_repo.{get_user,
batch_get_users, update_fields}\`

New helper \`user_repo.batch_get_users(uids)\` mirrors the existing
\`batch_get_profiles\` on the \`gem_account\` side and replaces the
ad-hoc \`\$in\` query in \`_batch_user_profiles\`. Also drops two local
\`COLLECTION_NAME = \"ecap-account\"\` constants.

**Separately (same PR for context):** Clean up the non-functional \`#
lgtm[py/clear-text-logging-sensitive-data]\` markers introduced in
#818's twilio.py. CodeQL doesn't honor LGTM suppression comments — the
two alerts there were ultimately dismissed as false-positive via the
GitHub API, not by the comments. The explanatory comments are kept so
future readers know the log fields are intentional and the alerts are on
record.

CI guard: WARNING list shrinks from 11 → 9 route files.

## Test plan

- [x] \`ruff check app/ tests/\` — clean
- [x] \`pyright app/ tests/\` (full-repo scope) — 0 errors
- [x] \`pytest\` on affected 4 files — 75 passed
- [x] \`bash scripts/ci-lint/02-no-direct-mongo-in-routes.sh\` —
\`archived.py\` and \`openclaw_admin.py\` absent from WARNING list
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [0c9897c](https://github.com/SerendipityOneInc/ecap-workspace/commit/0c9897c64f09c1a08dafc62ef348dc412fbdcb68) refactor(claw-interface): drop direct mongo from 4 more route holdouts (#818)

**作者**: Chris@ZooClaw  
**SHA**: `0c9897c64f09c1a08dafc62ef348dc412fbdcb68`

```
## Summary

Continuation of PR #817. Migrates four more route-layer holdouts of
`scripts/ci-lint/02-no-direct-mongo-in-routes.sh` to `user_repo`:

- `clawhub.py` — 1 call → `user_repo.get_user(uid)`
- `connectors.py` — 1 call → `user_repo.get_user(uid)`
- `credits.py` — 3 calls → `user_repo.get_user(uid)`
- `twilio.py` — 1 call → `user_repo.get_by_phone_number(phone)` (one new
helper)

Plus drops three local `*_COLLECTION = "ecap-account"` constants
(clawhub / connectors / twilio) that violated the spirit of
`05-no-new-collection-name-constants.sh`.

The new `user_repo.get_by_phone_number` mirrors the existing
`get_by_stripe_customer_id` pattern. A `str()` coerce is added in twilio
for the `form_data.get("From", "")` value (returns `UploadFile | str`) —
the typed helper signature surfaced this latent looseness.

CI guard: WARNING list shrinks from 15 → 11 route files. Once merged,
the guard ERROR-blocks regressions on these four.

## Test plan

- [x] \`ruff check app/ tests/\` — clean
- [x] \`ruff format\` — applied to user_repo test + twilio test (linter
formatting only)
- [x] \`pyright app/ tests/\` (full-repo scope) — 0 errors / 0 warnings
- [x] \`pytest\` on the 7 affected files (clawhub / connectors /
inject_credentials / worker_callback / user_credits / twilio /
user_repo) — 79 passed
- [x] \`bash scripts/ci-lint/02-no-direct-mongo-in-routes.sh\` — four
target files no longer in WARNING list
- [ ] CI green on PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [28009fe](https://github.com/SerendipityOneInc/ecap-workspace/commit/28009fe04c1a247dd043f7df8ab221beda30286b) refactor(web): branded login module → scoped CSS (#796 PR 1/5) (#816)

**作者**: Chris@ZooClaw  
**SHA**: `28009fe04c1a247dd043f7df8ab221beda30286b`

```
## Summary

Issue #796 login domain 第 1/5 PR —— 把 3 个 login 文件的 ~50 处 inline style
抽成独立 CSS module (.login-root + --login-* scoped tokens)，消除 file-level
eslint-disable 与 onMouseEnter/Leave handler。

## 变更

- **新建** `web/src/components/login.css`：`.login-root` scoped，13 个
`--login-*`
  token（固定品牌色板，不随 dark/light 切换），语义 className

（`.login-btn-base`、`.login-input`、`.login-modal-backdrop`、`.login-card`、
  `.verify-code-input` 等）
- **重构 3 文件**：`LoginForm.tsx` / `LoginModal.tsx` /
  `app/[locale]/user/verify/page.tsx`
- 删除文件顶部 `/* eslint-disable no-restricted-syntax |
react/forbid-dom-props */`
  - ~50 处 inline style 全部迁移到 CSS module
  - 所有 `onMouseEnter/Leave` 手动改 `e.currentTarget.style` → CSS `:hover` /
    `:focus-visible` / `:disabled` 伪类（副作用：键盘 focus 态自动同步，可访问性改善）
  - 净减 323 行（424 删 / 101 增，不含新 CSS）
- **`web/eslint.config.mjs`**：从 `react/forbid-dom-props` ignores 列表删除
  `src/components/LoginModal.tsx`（LoginForm / verify 不在该列表，只有 file-level
  disable 被删；两者在 complexity 超长文件列表，不在 #796 范围）
- **`docs/superpowers/specs/2026-04-15-branded-modules-login.md`**：定义
token
  命名约定、className 分层、样板代码，样板复用于后续 4 个 domain PR

## 为什么拆 5 个 PR

Issue body 建议「一个 domain = 一个 PR」；Memory 偏好小 PR + serial
（等 CI 绿再起下一个）。本 PR 仅 login domain（3 文件）；PR 2 paywall 会等本
PR 合并后起。

## 防回归

- SHRINK-ONLY 守卫（`web/scripts/check-ignores-shrink-only.sh`，#804 引入）：
  main 48 → HEAD 47 ✅ 永久不能回增
- Design spec 锁定约定，未来新 branded 模块必须走 `.{domain}-root` + `--{domain}-*`
  模式（`web/CLAUDE.md` Branded modules 段已引用 #796）

## Test plan

- [x] `pnpm lint` 绿（3 文件从 file-level disable 移除后，
      `react/forbid-dom-props` + `no-restricted-syntax` 双规则生效且无新违规）
- [x] `pnpm tsc --noEmit` 绿
- [x] `pnpm test`：2216 tests passed
- [x] `bash web/scripts/check-ignores-shrink-only.sh` passed (48→47)
- [ ] **视觉对比** staging vs main（CI 部署后）：
  - [ ] Login modal：Google / Phone / Email 三个 OAuth hover 态
  - [ ] Email form：错误输入 → error border；disabled CTA 态
  - [ ] Phone form：国家 select + phone 两段式输入；倒计时态
- [ ] `/user/verify`：SMS / Email OTP / Email magic link / Success /
倒计时重发
  - [ ] close button hover（原来 JS 改 style，现在 CSS :hover）
  - [ ] dark / light 主题切换：login 保持品牌固定色不变
- [ ] 键盘 tab 遍历：OAuth 按钮、输入框、CTA 的 focus ring 正常

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [4e3876a](https://github.com/SerendipityOneInc/ecap-workspace/commit/4e3876aabf1a035f0c904c5bdd10dc5415602d4b) feat: support body_defaults, body_wrapper, and extra_headers for connector tools (#809)

**作者**: Leo-srp  
**SHA**: `4e3876aabf1a035f0c904c5bdd10dc5415602d4b`

```
## Summary
Add three new tool definition features to support more connector APIs:

- `body_defaults`: merge static fields into request body (e.g. LinkedIn
post fields)
- `body_wrapper`: wrap body in a key (e.g. Asana requires `{"data":
{...}}`)
- `extra_headers`: forward per-tool custom headers to target API via
Nango proxy (e.g. `LinkedIn-Version`)

## Test plan
- [ ] Existing GitHub/Linear tools still work (no
body_defaults/wrapper/headers)
- [ ] New connectors using these features work correctly

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: tim-srp <tim@srp.one>
```

### [10c94bd](https://github.com/SerendipityOneInc/ecap-workspace/commit/10c94bde6722fc97c84da82a5b8ed92fb2d9a9b6) refactor(claw-interface): drop direct mongo from 3 route holdouts (#817)

**作者**: Chris@ZooClaw  
**SHA**: `10c94bde6722fc97c84da82a5b8ed92fb2d9a9b6`

```
## Summary

- Migrates the last three route-layer holdouts of
`scripts/ci-lint/02-no-direct-mongo-in-routes.sh` (`admin_boost.py`,
`invite_code.py`, `subscription.py`) off direct `mongo.*` calls and onto
existing `user_repo` / `invite_code_repo` helpers — 13 call sites,
**zero new repo methods needed**.
- Once merged on `main`, the CI guard's dynamic allowlist will treat any
future direct `mongo` import in these files as ERROR (not WARNING),
completing the route-layer transition started in PR #781.
- Drops the local `USERS_COLLECTION = "ecap-account"` constant in
`subscription.py` (was a `05-no-new-collection-name-constants.sh`
violation in spirit).
- Tightens an `int_to_str_uid.get(p.get("uid"))` lookup in
`list_invite_codes` that the stricter helper return type surfaced —
`mongo.read` returned `Any`, hiding a `None`-into-`int`-key risk that
pyright now catches.
- Updates `services/claw-interface/CLAUDE.md` to remove the "Known
holdouts" bullet for these three files.

## Test plan

- [x] `ruff check app/ tests/` — clean
- [x] `ruff format` — no changes
- [x] `pyright app/ tests/` (full-repo scope) — 0 errors / 0 warnings
- [x] `pytest tests/unit/test_admin_boost.py
tests/unit/test_subscription_routes.py tests/unit/test_invite_codes.py`
— 89 passed
- [x] `bash scripts/ci-lint/02-no-direct-mongo-in-routes.sh` — three
target files no longer in WARNING list
- [ ] CI green on PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [0b2603c](https://github.com/SerendipityOneInc/ecap-workspace/commit/0b2603ca2f80436a84e1487b943e2d9d69b367d7) chore(claw-interface): drop RUF006 ignore + fix latent delayed-close task leak (#803)

**作者**: Chris@ZooClaw  
**SHA**: `0b2603ca2f80436a84e1487b943e2d9d69b367d7`

```
## Summary
Follow-up to #802. Two related changes:

### 1. Drop obsolete `RUF006` ignore (original PR)
`RUF006` (unassigned `asyncio.create_task`) had **0 direct hits** in the
ruff scan, so the ignore was obsolete.

### 2. Fix latent fire-and-forget task leak in `openclaw_client.py`
While reviewing, we noticed `_get_app_client` was calling
`asyncio.get_running_loop().create_task(self._delayed_close(evicted))`
without retaining the task. Because asyncio only holds weak references
to tasks, the scheduled close could be GC'd mid-sleep, leaving the
evicted httpx client un-closed (socket leak).

**Note:** RUF006 only flags the *direct* `asyncio.create_task(...)` form
— the `loop.create_task(...)` variant currently slips through ruff's
matcher, which is why the ignore removal alone passed lint. This PR
fixes the underlying bug regardless and switches to the direct form so
RUF006 can catch future regressions.

**Fix:**
- Per-instance `_pending_closes: set[asyncio.Task]` to hold strong refs
- `add_done_callback(self._pending_closes.discard)` to auto-remove on
completion (no unbounded growth)
- `aclose()` cancels + gathers pending tasks so evicted clients don't
outlive the owner

## Test plan
- [x] `ruff check app/ tests/` — All checks passed
- [x] `pyright app/ tests/` — 0 errors, 0 warnings
- [x] `pytest tests/unit/test_openclaw_client.py` — 139 passed (+1 new
test covering task tracking + auto-discard)
- [ ] CI `python-code-quality` passes

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [eb28cd1](https://github.com/SerendipityOneInc/ecap-workspace/commit/eb28cd1ef324a089a96090ed401bc4a2e9af97fb) fix(claw-interface): track pack asset ids for update checks (#812)

**作者**: nolan-srp  
**SHA**: `eb28cd1ef324a089a96090ed401bc4a2e9af97fb`

```
## Summary
- persist latest GitHub release asset ids for official pack agents
during install and redeploy
- use stored pack asset ids to detect updates in the agent response
path, and treat lookup failures as stale
- cover the new asset id refresh and update-detection flows in unit
tests
```

### [c4315c2](https://github.com/SerendipityOneInc/ecap-workspace/commit/c4315c2c57be3fcbf7d87392e418f3473d1bed8f) ci(web): SHRINK-ONLY guard 守护 react/forbid-dom-props ignores 列表 (#804)

**作者**: Chris@ZooClaw  
**SHA**: `c4315c2c57be3fcbf7d87392e418f3473d1bed8f`

```
## Summary

#754 收尾工作:把"ignores 列表只能缩不能扩"从 CLAUDE.md 文字约定升级为 **CI 硬约束**。同时把 #796 揭示的
branded modules 模式写入 web/CLAUDE.md,给后续新建该类模块的人正确指引。

## 新增

### 1. \`web/scripts/check-ignores-shrink-only.sh\`

比对 \`origin/main\` 与 HEAD 的 \`react/forbid-dom-props\` ignores 数组长度:
- HEAD ≤ main:pass(允许同等数量,例如 narrow PR 只改 file-level disable 不动 ignores)
- HEAD > main:fail,输出违规明细 + 替代方案(行内 disable / CSS module)+ 链回 #796

依据 \`SHRINK-ONLY: do NOT add new entries here\` 注释作为块标记(稳定,不依赖文件计数)。

### 2. \`.github/workflows/code-quality.yml\`

\`web-quality\` job 在 ESLint 后加一步:

\`\`\`yaml
- name: ignores SHRINK-ONLY check (react/forbid-dom-props)
  run: bash web/scripts/check-ignores-shrink-only.sh
\`\`\`

### 3. \`web/CLAUDE.md\`

- 现有 Code Style 段补充 CI guard 提示("adding a file fails the build")
- 新增 **Branded modules** 小节,引导新模块走 \`.{domain}-root\` + \`--{domain}-*\`
CSS module 模式(参照 \`web/src/app/landing/landing.css\`),不要再开 file-level
eslint disable

## 测试

- ✅ Pass 路径(本地):main 与 HEAD 都 49 项,脚本 exit 0
- ✅ Fail 路径(本地):临时加 \`src/components/FAKE.tsx\` 到 ignores,脚本输出:

\`\`\`
react/forbid-dom-props ignores — main: 49, HEAD: 50

❌ ignores SHRINK-ONLY violation: list grew from 49 → 50 entries.

Adding a file to the react/forbid-dom-props ignores in
web/eslint.config.mjs regresses
the guardrail. Instead, fix the file or use a narrower exemption:
  - Dynamic styles: ...
  - Branded modules: see #796 ...
\`\`\`

并 exit 1。

## 防回归覆盖

| 之前(软约束) | 现在(硬约束) |
|----------|----------|
| CLAUDE.md "shrink only" 文字 | CI 脚本拒绝合并 |
| ignores 注释 "SHRINK-ONLY: do NOT add" | 同上 + reviewer 不可能漏 |
| 依赖 reviewer 看到再喊停 | PR 触发 CI 即报错,提前阻断 |

## 关联

- Issue: #754(本 PR 是收尾)
- Issue: #796(branded modules 整体重构,本 PR 只做引导,不做实质重构)
- 阶段 A/B 9 个 PR 全部完成后,本 PR 防止"教父名单"再次悄悄变长

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [38ae2c1](https://github.com/SerendipityOneInc/ecap-workspace/commit/38ae2c184985913359db9b0db8dc94ae2e7726a7) refactor(claw-interface): finish B904 unignore series (4/4) (#808)

**作者**: Chris@ZooClaw  
**SHA**: `38ae2c184985913359db9b0db8dc94ae2e7726a7`

```
## Summary

**Final PR of the B904 unignore series.** Fixes the last 8 violations
outside \`routes/\`, then **removes \`B904\` from the pyproject.toml
ignore list** so future regressions fail CI.

### Per-site breakdown

| File | Line | Pattern | Fix |
|---|---|---|---|
| \`app/auth/token_verifier.py\` | 64 | \`except httpx.RequestError as
exc\` | \`from exc\` |
| \`app/auth/token_verifier.py\` | 73 | \`except Exception:\` (401 on
JSON decode) | \`from None\` |
| \`app/connectors/base.py\` | 101 | \`except (jwt.InvalidTokenError,
KeyError) as exc\` | \`from exc\` |
| \`app/services/gift_code.py\` | 133 | \`except Exception as e\` |
\`from e\` |
| \`app/services/openclaw/agent_deploy.py\` | 347 | \`except Exception
as e\` wrapping \`RuntimeError\` | \`from e\` |
| \`app/services/stripe/order_confirm.py\` | 64 | \`except
stripe.error.StripeError as e\` | \`from e\` |
| \`app/services/subscription_manager.py\` | 216 | \`raise ValueError\`
inside \`except httpx.HTTPStatusError as e\` wallet-recovery path |
\`from e\` (preserves 404/422 trigger context) |
| \`tests/unit/test_subscription_cron.py\` | 42 | \`__getattr__\`
translating \`KeyError\` → \`AttributeError\` | \`from None\` (Python
idiom: caller should see a clean \`AttributeError\`) |

### pyproject.toml

Removes:
\`\`\`
"B904",    # raise from err in except (requires codebase-wide refactor)
\`\`\`

The refactor is now done — the comment is obsolete. With B904
re-enabled, any new \`raise X\` inside an \`except\` block will fail
\`ruff check\` unless the author makes the chain explicit (\`from e\` /
\`from None\`).

### Series totals

| PR | Scope | Fixes |
|---|---|---|
| #805 | \`routes/openclaw*\` | 39 |
| #806 | \`routes/session/*\` | 21 |
| #807 | \`routes/\` remaining | 39 |
| **this** | \`services/\` + \`auth/\` + \`connectors/\` + \`tests/\` +
pyproject | 8 |
| **Total** | | **107** |

## Test plan
- [x] \`ruff check app/ tests/\` — All checks passed (includes B904 now
that it's unignored)
- [x] \`ruff format --check app/ tests/\` — 300 files already formatted
- [x] \`pyright app/ tests/\` — 0/0/0
- [x] \`pytest tests/unit/test_subscription_manager.py
tests/unit/test_subscription_cron.py tests/unit/test_gift_code.py\` — 83
passed
- [ ] CI \`python-code-quality\` passes

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [833737e](https://github.com/SerendipityOneInc/ecap-workspace/commit/833737e6990704cb4e44048c760d6cdb9e4baf63) refactor(claw-interface): exception chaining in remaining routes (B904 3/4) (#807)

**作者**: Chris@ZooClaw  
**SHA**: `833737e6990704cb4e44048c760d6cdb9e4baf63`

```
## Summary

Part 3 of the B904 unignore series (follows #805, #806). Fixes 39 B904
violations across the remaining 12 route files.

### Per-file breakdown

| File | Count | Notes |
|---|---|---|
| \`litellm.py\` | 11 | DEPRECATED file, but we still clear its lint
debt |
| \`stripe.py\` | 6 | includes 2 sites on
\`stripe.error.SignatureVerificationError as e\` |
| \`user.py\` | 5 | all \`except Exception as e\` |
| \`orders.py\` | 5 | all \`except Exception as e\` |
| \`credits.py\` | 3 | all \`except Exception as e\` |
| \`twilio.py\` | 2 | all \`except Exception as e\` |
| \`subscription.py\` | 2 | all \`except Exception as e\` |
| \`apple.py\` | 1 | \`except Exception:\` (no alias) → \`from None\` |
| \`asr.py\` | 1 | \`except UpstreamError:\` (no alias) → \`from None\`
|
| \`openclaw_agents.py\`, \`invite_code.py\`, \`gift_code.py\` | 1 each
| all \`except X as e\` → \`from e\` |

### Decision rule

- **37 sites** with \`except X as <var>\`: append \`from <var>\`
(preserves \`__cause__\`; exception is already logged)
- **2 sites** with no bound variable: \`from None\` to explicitly
suppress the chain (apple.py 400 webhook; asr.py 502 where the handler
already logs the original)

One notable variable name: \`litellm.py:602\` uses \`except ... as
ssrf_err\` → \`from ssrf_err\`.

### Series progress

- [x] 1/4 · \`routes/openclaw*\` — #805
- [x] 2/4 · \`routes/session/*\` — #806
- [x] 3/4 · \`routes/\` remaining — this PR
- [ ] 4/4 · \`services/\` + \`auth/\` + \`connectors/\` + \`tests/\` (~8
hits) + remove \`B904\` from \`pyproject.toml\` ignore

## Test plan
- [x] \`ruff check app/routes/ --select B904\` — clean
- [x] \`ruff check app/ tests/\` — All checks passed
- [x] \`ruff format --check app/routes/\` — no diff
- [x] \`pyright app/ tests/\` — 0/0/0
- [x] \`pytest tests/unit\` — 2289 passed (2 pre-existing failures in
\`test_skill_injector.py\`, confirmed unrelated by stash-pop
verification on same branch)
- [ ] CI \`python-code-quality\` passes

## Out of scope (noted for follow-up)
The 2 \`test_skill_injector.py\` failures exist on main independent of
this series — worth filing a separate issue.

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [359097e](https://github.com/SerendipityOneInc/ecap-workspace/commit/359097ee4a741c7c9c985bcac9911907ac85b030) chore(web): #754 ChannelStep 豁免修正(B5/9, 范围调整, 计划完结) (#800)

**作者**: Chris@ZooClaw  
**SHA**: `359097ee4a741c7c9c985bcac9911907ac85b030`

```
## Summary

**计划调整 + 9 个 PR 计划完结** — 与 B1(#794)/B2(#797)/B4(#799)同因。

ChannelStep 是 onboarding 流程的一步,使用 onboarding 模块固定品牌色板(\`#1a1a17\` / 多档
\`rgba(26,26,24,...)\` 灰阶,与 SpriteDialogue 同一色板),刻意脱离全局 theme/token
系统以保证引导流程视觉统一。L1 已有 \`eslint-disable no-restricted-syntax\`(原本无理由)。

## 本 PR 实际改动

1. **L1 file-level disable**:\`no-restricted-syntax\` →
\`react/forbid-dom-props, no-restricted-syntax\`(同时豁免两条规则)
2. **补充中文理由说明**(列出涉及色板,链接到 SpriteDialogue 同色板)
3. **从 ignores 移除**

## Ignores 缩减

45 → 44(本 PR);**累计 76 → 44(减 32)**。

---

## #754 计划完结战报

| 阶段 | PR | 性质 | Ignores 影响 |
|------|----|------|----|
| A1 | #780 | canvas LEGIT 行内豁免(7 文件) | 76 → 69 |
| A2 | #787 | onboarding+chat LEGIT(6 文件) | 69 → 63 |
| A3 | #789 | schedule+agents-manager LEGIT(5 文件) | 63 → 58 |
| A4 | #793 | selectors+杂项 LEGIT(9 文件) | 58 → 49 |
| B1 | #794 | LoginForm narrowed(branded modal)| 49 → 48 |
| B2 | #797 | verify page narrowed(同上)| 48 → 47 |
| B3 | #798 | GeneralTab 段级豁免(theme preview)| 47 → 46 |
| B4 | #799 | PaywallContent narrowed(同 branded)| 46 → 45 |
| B5 | 本 PR | ChannelStep narrowed(onboarding branded)| 45 → 44 |

**关键观察**:
- 阶段 B 5 个 PR 全部被 narrowed——issue 的"TW 高频"分类对其中 4 个文件不准,实际都是"branded
fixed colors"独立主题模块,不适合 TW 化
- 真正的"branded modal 抽 CSS module"重构记录在 **#796**(LoginForm
起头),paywall/onboarding/verify 可酌情合并入或单开
- 剩余 44 项 ignores 全是真待迁移的 TW/MOD/MIXED,语义干净

## Test plan

- [x] \`pnpm lint\` pass
- [ ] CI \`code-quality / lint-and-test\` 绿
- [x] 视觉零变化(只改注释)

## 关联

- Issue: #754;后续重构候选: #796
- 同因 PR:#794(B1) / #797(B2) / #799(B4)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [4c5ead7](https://github.com/SerendipityOneInc/ecap-workspace/commit/4c5ead7539e91d4936f39884cee55c420afd7b8c) refactor(claw-interface): exception chaining in session routes (B904 2/4) (#806)

**作者**: Chris@ZooClaw  
**SHA**: `4c5ead7539e91d4936f39884cee55c420afd7b8c`

```
## Summary

Part 2 of the B904 unignore series (follows #805). Fixes 21 of the
remaining 68 B904 violations — all 4 files under
\`app/routes/session/\`.

### Per-site breakdown

| File | Count | All sites use |
|---|---|---|
| \`chat.py\` | 10 | \`from e\` (covers \`except Exception as e\` and 5
\`except httpx.X as e\` subclasses) |
| \`jobs.py\` | 5 | \`from e\` |
| \`session_crud.py\` | 4 | \`from e\` |
| \`archived.py\` | 2 | \`from e\` |

Every violation in this batch sits inside \`except X as e\` with an
already-logged internal 500/503/504, so \`from e\` (preserve chain) is
uniformly correct — no \`from None\` needed here.

### Series progress

- [x] 1/4 · \`routes/openclaw*\` — #805
- [x] 2/4 · \`routes/session/*\` — this PR
- [ ] 3/4 · \`routes/\` remaining (litellm, stripe, user, orders,
credits, etc., ~39 hits)
- [ ] 4/4 · \`services/\` + \`auth/\` + \`connectors/\` + \`tests/\` (~8
hits) + remove \`B904\` from \`pyproject.toml\` ignore

## Test plan
- [x] \`ruff check app/ tests/\` — All checks passed
- [x] \`ruff check --select B904 app/routes/session/\` — clean
- [x] \`ruff format --check app/routes/session/\` — no diff
- [x] \`pyright app/ tests/\` — 0/0/0
- [x] \`pytest tests/unit -k "session or chat or jobs or archived"\` —
279 passed
- [ ] CI \`python-code-quality\` passes

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [5ebffd1](https://github.com/SerendipityOneInc/ecap-workspace/commit/5ebffd1b83e0300b2775c1abe9df5647019d68f9) test(api): #782 BDD e2e coverage for cron subscription renewal (#790)

**作者**: Chris@ZooClaw  
**SHA**: `5ebffd1b83e0300b2775c1abe9df5647019d68f9`

```
Closes #782.

## Summary
- Adds `tests/bdd/features/cron_renewal.feature` +
`tests/bdd/step_defs/test_cron_renewal.py` covering the cron renewal
path (`process_cron_renewal`) end-to-end against the real repo layer and
real test mongo.
- No production code changes — purely filling the integration-test gap
surfaced during #781 review.

## Scenarios
1. **Happy path** — new `CRON-RENEWAL-{uid}-{old_end}` order, user flips
to active, `completed_billing_cycles` increments, billing mock receives
`clear_wallet` + `topup_wallet(20000)`.
2. **Webhook-already-handled dedup** — pre-seeded granted webhook order
inside the 24h dedup window; cron returns `False`, creates no new order,
leaves `completed_billing_cycles` untouched.
3. **Cron-twice idempotency** — two invocations against the *same user
snapshot* (simulating concurrent workers); second call hits
`find_recent_subscription_grant` and bails, total one order and one
cycle increment.
4. **Pending-downgrade applied** — `user.pending_downgrade="starter"` →
new order has `plan="starter"`, user's `pending_downgrade` is `$unset`
atomically alongside the plan update, topup is 4800.

## Design notes
- **No `patch("...orders_repo")` / `patch("...user_repo")`** — the whole
point is to catch wiring regressions the unit tests can't see (e.g.
swapped `update_fields` vs `update_and_unset_fields`, wrong `since` arg
to `find_recent_subscription_grant`).
- Only external side effects are stubbed:
`app.services.subscription_manager.get_billing_client` and
`app.services.openclaw.bot_lifecycle.start_user_bots`.
- `cron-twice` uses a single user-dict snapshot for both invocations
(real cron scheduler would skip the second dispatch after the first
write); this models the concurrent-worker race the deterministic
order_id is designed to survive.

## Test plan
- [x] `pytest tests/bdd/step_defs/test_cron_renewal.py -v` — 4 passed
- [x] Full BDD suite `pytest tests/bdd/` — 338 passed, no regressions
- [x] Existing unit layer `pytest
tests/unit/test_process_cron_renewal.py` — 5 passed
- [x] `ruff format` / `ruff check` clean
- [x] `pyright app/ tests/` — 0 errors
- [ ] CI `python-code-quality / build-and-test` green (runs with
`enable_mongodb: true`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [281b912](https://github.com/SerendipityOneInc/ecap-workspace/commit/281b9125fcb9410e2825d62473157484fc48188b) refactor(claw-interface): exception chaining in openclaw routes (B904 1/4) (#805)

**作者**: Chris@ZooClaw  
**SHA**: `281b9125fcb9410e2825d62473157484fc48188b`

```
## Summary

Part 1 of the B904 unignore series. Fixes 39 of 107 total B904
violations — all in the 4 \`openclaw*\` route files.

B904 flags bare \`raise X\` inside an \`except\` block, which loses the
original exception's traceback chain (\`__cause__\`). Explicit \`from
e\` or \`from None\` declares intent.

### Per-site breakdown

| File | Count | Pattern |
|---|---|---|
| \`openclaw_settings.py\` | 20 | all \`except Exception as e\` → \`from
e\` |
| \`openclaw.py\` | 7 | all \`except Exception as e\` → \`from e\` |
| \`openclaw_admin.py\` | 7 | all \`except Exception as e\` → \`from e\`
|
| \`openclaw_integrations.py\` | 5 | mix: see below |

**openclaw_integrations.py** special cases:
- L63, L165: \`except Exception as e\` → \`from e\`
- L115: \`except httpx.RequestError as exc\` → \`from exc\` (different
var name)
- L124 (\`json.loads\` failure → 401), L560 (malformed JSON → 400):
\`except Exception:\` / \`except json.JSONDecodeError:\` with no bound
variable → \`from None\`. These are client-facing validation errors;
suppressing \`__context__\` yields a clean traceback instead of leaking
parser internals.

### Decision rule used

- Bound exception variable + internal 500/502 error → \`from <var>\`
(debug-friendly; the caller already logs the original so chain info is
cost-free)
- No bound variable + client-facing 400/401 validation error → \`from
None\` (clean client error, no implementation leak)

### Series plan

- **1/4 this PR** · \`routes/openclaw*\` (39 hits)
- 2/4 · \`routes/session/*\` (~21 hits)
- 3/4 · \`routes/\` remaining (litellm, stripe, user, orders, credits,
etc., ~39 hits)
- 4/4 · \`services/\` + \`auth/\` + \`connectors/\` + \`tests/\` (~8
hits) + **remove \`B904\` from \`pyproject.toml\` ignore list**

## Test plan
- [x] \`ruff check app/ tests/\` — All checks passed
- [x] \`ruff check --select B904\` on the 4 touched files — clean
- [x] \`ruff format --check\` on touched files — no diff
- [x] \`pyright app/ tests/\` — 0/0/0
- [x] \`pytest tests/unit -k openclaw\` — 545 passed
- [ ] CI \`python-code-quality\` passes

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [f6ee6a0](https://github.com/SerendipityOneInc/ecap-workspace/commit/f6ee6a0d12b42452b8ef52a7dc89d315d0c24e69) chore(claw-interface): drop 3 obsolete ruff ignores (#802)

**作者**: Chris@ZooClaw  
**SHA**: `f6ee6a0d12b42452b8ef52a7dc89d315d0c24e69`

```
## Summary
- Drop \`RUF013\` (implicit Optional) ignore — 0 violations in the
codebase; the "requires codebase-wide refactor" note in
\`pyproject.toml\` was stale.
- Drop \`PLR0133\` (two-constants comparison) ignore — fix by removing 3
placeholder tests (\`assert 1 == 1\` etc.) in \`tests/test_example.py\`
that served no purpose beyond \`test_true\` already does.
- Drop \`PLW0602\` (global without assignment) ignore — fix by removing
3 redundant \`global\` declarations in read-only contexts
(\`app/scheduler.py\` ×2,
\`tests/bdd/step_defs/test_chat_session_create.py\` ×1). \`global\` is
only required when **assigning** to a module-level name inside a
function.

Net: `pyproject.toml` loses 3 ignore rules; 4 files change, 20
deletions, 0 additions.

Remaining "pending codebase cleanup" ignores in \`pyproject.toml\`:
\`B904\` (107 hits — real debt, tracked for a follow-up series).

## Test plan
- [x] \`ruff check app/ tests/\` — All checks passed
- [x] \`ruff format --check app/ tests/\` — 299 files already formatted
- [x] \`pyright app/ tests/\` — 0 errors, 0 warnings, 0 informations
- [ ] CI \`python-code-quality\` passes

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [9b26bcc](https://github.com/SerendipityOneInc/ecap-workspace/commit/9b26bccf3b4fca2bcc4f7c117577c2a18da58118) style(web): remove rounded corners from upgrade banner for top-bar cohesion (#801)

**作者**: Nemo Feng  
**SHA**: `9b26bccf3b4fca2bcc4f7c117577c2a18da58118`

```
## Summary
- Remove `rounded-lg` from `UpgradeNotificationBanner` so the banner
sits flush against the top bar, creating a more cohesive visual
appearance.

## Test plan
- [ ] Open the chat page with a pending upgrade and verify the banner
has square corners
- [ ] Open the claw-settings page with a pending upgrade and verify the
same

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Nemo Feng <nemofq@gmail.com>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### [ea007e3](https://github.com/SerendipityOneInc/ecap-workspace/commit/ea007e3293b8931f1e74fc22745840a52864758c) chore(web): #754 PaywallContent 豁免修正(B4/9, 范围调整) (#799)

**作者**: Chris@ZooClaw  
**SHA**: `ea007e3293b8931f1e74fc22745840a52864758c`

```
## Summary

**计划调整(plan narrowing)** — 与 B1(#794)/B2(#797)同因。

PaywallContent L1 已有 file-level disable(\`eslint-disable
no-restricted-syntax\`,原本无理由),但属于与 LoginForm / verify page 同款的 **branded
fixed colors** 模式——独立品牌色板(\`#1a1a18\` 黑色 CTA、多档 \`rgba(0,0,0,...)\`
灰阶、固定红色 error 等),刻意脱离全局 theme/token 系统,不随 dark/light 切换以保证销售场景视觉一致性。

按 TW 化的两条路依然不通(详见 #794 PR 描述)。

## 本 PR 实际改动

1. **L1 file-level disable**:\`no-restricted-syntax\` →
\`react/forbid-dom-props, no-restricted-syntax\`(同时豁免两条规则)
2. **补充中文理由说明**(列出涉及的具体值)
3. **从 ignores 移除**

## Ignores 缩减

46 → 45。

## 后续

PaywallContent 也是"独立深色/品牌主题模块"之一,与 LoginForm 抽 \`login.css\` 是同类工作。可考虑:
- 把 PaywallContent 加入 #796 范围(login + paywall 一起重构)
- 或开独立 issue track \`paywall.css\` + \`--paywall-*\` token

本 PR 不强行决定,留给后续讨论。

## Test plan

- [x] \`pnpm lint\` pass
- [ ] CI \`code-quality / lint-and-test\` 绿
- [x] 视觉零变化(只改注释)

## 关联

- Issue: #754;后续重构候选: #796
- 同因 PR:#794(B1, LoginForm) / #797(B2, verify)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [74eb182](https://github.com/SerendipityOneInc/ecap-workspace/commit/74eb182da8c2bf6b56cc8c2c9081376e02f777f2) chore(web): #754 GeneralTab 段级豁免(B3/9, 范围调整) (#798)

**作者**: Chris@ZooClaw  
**SHA**: `74eb182da8c2bf6b56cc8c2c9081376e02f777f2`

```
## Summary

**计划调整(plan narrowing)**:原计划 B3 是 GeneralTab 15 处 MIXED 迁移,但读完文件后发现这 15
处全部都是合理保留(LEGIT),不是混合状态。

## 分类结果

| 处数 | 位置 | 性质 | 处理 |
|------|------|------|------|
| 1 | L133 | `fontFamily: 'var(--font-heading, Georgia, serif)'` | LEGIT
— Tailwind font 配置无法表达 fallback 链 |
| 14 | L219-289 | Theme 预览 swatch(light/dark/system 三个 mini mockup) |
LEGIT — 有意用固定 hex 渲染主题示意,跟随实际主题反而失去示意效果 |

## 改动

文件 L219 已有 block disable 注释 `Theme previews intentionally use fixed
colors`,但只豁免了 `no-restricted-syntax`(hex 检查),没覆盖
`react/forbid-dom-props`。

1. **L219 block disable**:`no-restricted-syntax` →
`react/forbid-dom-props, no-restricted-syntax`(对应 L289 enable 同步扩展)
2. **L133**:加行内 `// eslint-disable-next-line react/forbid-dom-props -- 用
var(--font-heading) + fallback 链`
3. **从 ignores 移除**

避免了 14 条逐行 disable 的噪音——用既有的段级 disable 自然延展。

## Ignores 缩减

47 → 46。

## Test plan

- [x] `pnpm lint` pass(无 unused-disable 警告)
- [ ] CI `code-quality / lint-and-test` 绿
- [x] 视觉无变化(只改注释)

## 关联

- Issue: #754
- 计划:9 个 PR 中的 B3(范围调整后)
- 阶段 A 已合并:#780 / #787 / #789 / #793;B 阶段:#794(B1) / #797(B2)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [39e7385](https://github.com/SerendipityOneInc/ecap-workspace/commit/39e7385c94c8e83e417712296c2e06a18cd26285) chore(web): #754 verify page 豁免修正(B2/9, 范围调整) (#797)

**作者**: Chris@ZooClaw  
**SHA**: `39e7385c94c8e83e417712296c2e06a18cd26285`

```
## Summary

**计划调整(plan narrowing)**:与 B1(#794)同因——verify page L1 已有 file-level
disable 注释\"verify page uses its own branded color palette via inline
styles\",与 LoginForm 共用同一套独立品牌色板。

按 TW 化迁移的两条路都不通(用 semantic token 会破坏 dark 模式视觉、用 \`bg-[#xxx]\` arbitrary
值会触发 \`no-raw-hex\` 规则)。

## 本 PR 实际改动

与 B1 完全相同的处理方式:

1. **L1 file-level disable**:\`no-restricted-syntax\` →
\`react/forbid-dom-props, no-restricted-syntax\`(同时豁免两条规则)
2. **理由说明完善**,链回 #796
3. **从 ignores 移除**

## Ignores 缩减

48 → 47。

## 后续

login + verify 共用一套设计,**整体重构(抽 login.css + \`--login-*\` token)由 #796
跟踪**,不在本计划范围。

## Test plan

- [x] \`pnpm lint\` pass
- [ ] CI \`code-quality / lint-and-test\` 绿
- [x] 视觉零变化(只改注释)

## 关联

- Issue: #754;后续重构: #796
- 计划:9 个 PR 中的 B2(范围调整后)
- 同因 PR:#794(B1, LoginForm)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [3daa300](https://github.com/SerendipityOneInc/ecap-workspace/commit/3daa3005baa7efb7ffdeee5ec76e07a7b3463ee0) chore(web): #754 LoginForm 豁免修正(B1/9, 范围调整) (#794)

**作者**: Chris@ZooClaw  
**SHA**: `3daa3005baa7efb7ffdeee5ec76e07a7b3463ee0`

```
## Summary

**计划调整(plan narrowing)**:原计划 B1 是 LoginForm 26 处 inline style → Tailwind
迁移,但读完文件后发现前提不成立。

## 为什么不做 TW 化

LoginForm.tsx 的 L1 有明确注释:
> `eslint-disable no-restricted-syntax -- login form uses its own
branded color palette via inline styles`

这个文件**刻意脱离全局 theme/token 系统**:用 `#1a1a17`、`#fff`、`#999`、Google 多色 logo
等固定 hex 值,不随 dark/light 主题切换。Login 是用户首次接触品牌的入口,视觉一致性优先于主题适配。

迁移路径都不通:
- 用 semantic token(`bg-background`/`text-foreground`)→ dark
模式视觉会变,违反设计意图
- 用 arbitrary value(`bg-[#fff]`/`text-[#1a1a17]`)→ 触发 CLAUDE.md 里
`no-raw-hex` lint 规则
- 用 className + 全局 CSS → 工作量等同抽 login.css 模块,远超本 PR 范围

## 本 PR 实际改动

把"文件级豁免"从 ignores 配置升级到代码内显式声明:

1. **L1 file-level disable**:`no-restricted-syntax` →
`react/forbid-dom-props, no-restricted-syntax`(同时豁免两条规则)
2. **理由说明完善**:列出具体豁免范围(品牌固定 hex、Google 多色 logo)、警告新增 inline style 前要评估
3. **从 ignores 移除**:`web/eslint.config.mjs` 的 `react/forbid-dom-props`
ignores 减一项

注:`no-restricted-syntax` 之前在文件上一直生效(catch hex 颜色),只是被原 file-level
disable 顺带豁免——本 PR 把这个事实显式列出,避免未来 reviewer 误解。

## Ignores 缩减

49 → 48。

## 后续

LoginForm 真正抽 login.css / 品牌色 token 化适合单独开 issue 讨论,远超本计划范围。

## Test plan

- [x] `pnpm lint` pass
- [ ] CI `code-quality / lint-and-test` 绿
- [x] 视觉零变化(只改注释)

## 关联

- Issue: #754
- 计划:9 个 PR 中的 B1(范围调整后)
- 阶段 A 已合并:#780 / #787 / #789 / #793

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [1b30374](https://github.com/SerendipityOneInc/ecap-workspace/commit/1b30374b621858a8ef5c7579f7b69635a4c9c869) chore(web): #754 selectors+misc LEGIT 行内豁免 (A4/9, 阶段 A 完结) (#793)

**作者**: Chris@ZooClaw  
**SHA**: `1b30374b621858a8ef5c7579f7b69635a4c9c869`

```
## Summary

- Issue #754 阶段 A **最后一个** PR:9 个 LEGIT 文件从 `web/eslint.config.mjs` 的
`ignores` 移到行内 `eslint-disable-next-line react/forbid-dom-props` +
中文原因注释。
- 至此阶段 A 全部完成。`ignores` 列表语义已经干净——剩余项全是 TW/MOD/MIXED 待迁移 TODO。

## 涉及文件(9 文件,~14 处)

- `src/components/RatioSelector.tsx`(3 处:容器/比例预览/popover minWidth)
- `src/components/SizeSelector.tsx`(2 处:同 RatioSelector 模式)
- `src/components/ProgressiveImage.tsx`(1 处:blur+scale 模糊覆盖)
- `src/components/ExampleShowcase/ExampleFeedCard.tsx`(2
处:animationDelay 错峰)
- `src/app/[locale]/admin/components/GrantCreditsModal.tsx`(1 处:配额进度条)
- `src/app/[locale]/claw-settings/components/UsageCard.tsx`(2 处:daily
activity opacity / top tools 宽度)
- `src/app/[locale]/profile/components/UsageTab.tsx`(1 处:配额进度条)
- `src/app/[locale]/pricing/PublicPricingClient.tsx`(1 处:pricing
页面独立深色主题 hex)
- `src/app/landing/components/LandingIntegrations.tsx`(0 处新增,但**修正现有
disable**:`no-restricted-syntax` → `react/forbid-dom-props`)

## 特别注意

- **LandingIntegrations** 之前的行内 disable 用的是
`no-restricted-syntax`(规则替换前的旧名),实际现在生效的规则是 `react/forbid-dom-props`。这个
disable 一直是 dead code(只是因为文件在 ignores 里所以没暴露)。本 PR 修正为正确规则名,并把文件从
ignores 移除——参见 `web/src/app/landing/CLAUDE.md` 已经描述了这个文件作为唯一 landing
例外的预期。
- **PublicPricingClient** 用独立深色主题(`#0a0a0f` / `#f5f4ef`),脱离全局 token
系统。disable 注释里标"待后续抽 pricing.css"。

## Ignores 缩减

`web/eslint.config.mjs` 的 `react/forbid-dom-props` ignores:58 → 49(减 9)。

**阶段 A 累计**:76 → 49(减 27)。剩 49 项语义干净——全是待迁移 TW/MOD/MIXED。

## 阶段 B 预告

接下来 5 个 PR(B1-B5)处理 TW 高频文件:LoginForm(26
处)、user/verify/page(21)、GeneralTab(15)、PaywallContent(14)、ChannelStep(13)。

## Test plan

- [x] `pnpm lint` pass(无 unused-disable 警告)
- [ ] CI `code-quality / lint-and-test` 绿
- [ ] 视觉无变化(未改样式)

## 关联

- Issue: #754
- 计划:9 个 PR 中的 A4(LEGIT 阶段最后一个)
- 前 3 个 PR:#780 / #787 / #789(已合并)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [762cb98](https://github.com/SerendipityOneInc/ecap-workspace/commit/762cb985b4582fc9f71c40c8688aa5e8a1b11659) docs(stripe): annotate PLAN_STARTER_20_MONTH as the canonical paid-tier BG code (#725 Item 3) (#792)

**作者**: Chris@ZooClaw  
**SHA**: `762cb985b4582fc9f71c40c8688aa5e8a1b11659`

```
## Summary

Closes #725 Item 3 (PR #688 review follow-up). Annotation-only ——
没有任何行为变动。

审查者曾把 `handlers/checkout.py:299` Pro/Ultra invite-trial 路径里的
`new_plan=PLAN_STARTER_20_MONTH` 当成 bug（"为什么 pro/ultra 用 starter
常量？"）。实际上 Billing Gateway 只在 plan_code 维度区分 free vs
paid，所有付费档位（starter/pro/ultra，月/年）统一写该常量。tier 差异通过这些字段体现：
- 月度额度：`app.settings.PLAN_CREDITS`
- LiteLLM 模型集：`app.services.plan_models.get_model_groups_for_plan`
- MongoDB：`order.plan`、`user.subscription_status`

这个约定在
`billing_gateway.py:171`、`entitlement.py:337`、`apple_subscription_manager.py:76`
都一致使用，但常量名 `PLAN_STARTER_20_MONTH` 字面上会反复误导 reviewer —— 本 PR
加文档/注释把约定显性化，防止再被当成 bug。

## Changes

- `app/services/stripe/constants.py` — 在 `PLAN_STARTER_20_MONTH` 上方加
docstring 解释 BG 约定及 tier 差异落在何处
- `app/services/stripe/handlers/checkout.py:298` — inline comment 指向上述
docstring

## Issue #725 状态（两 PR 合并后的最终总结）

- Item 1 (`_short_id` 重复): ✅ 被 PR #769 统一到 `safe_short_id`
- Item 2 (`COLLECTION_NAME` 重复): ✅ 被 mongo→repo 迁移 PR 消化
- Item 3 (pro/ultra 复用 starter 常量): ✅ 本 PR —— 确认非 bug + 加注释
- Item 4 (service→route 懒 import 耦合): ✅ 已由 PR #791 修复

合并后可关闭 issue #725。

## Test plan

- [x] `ruff format . && ruff check .` — pass
- [x] `pyright app/ tests/` — 0 errors, 0 warnings
- [x] `pytest tests/unit/` — 纯注释改动无行为变动

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [973633c](https://github.com/SerendipityOneInc/ecap-workspace/commit/973633c6ce219b4db3988847c5b7f2c508520469) refactor(stripe): drop service→route coupling on ensure_billing_initialized (#725 Item 4) (#791)

**作者**: Chris@ZooClaw  
**SHA**: `973633c6ce219b4db3988847c5b7f2c508520469`

```
## Summary

Part of #725 (PR #688 review follow-ups). 清理 Item
4：`app/services/stripe/` 两处 `from app.routes.user import
ensure_billing_initialized` 的函数内懒 import，改为 canonical 的 `from
app.services.billing import ensure_billing_initialized` 并提升到模块顶部。

- `billing_gateway.py::recover_wallets_and_reread` — 删函数内 import
- `entitlement.py::grant_entitlement` — 删函数内 import
- 两个 BDD 测试同步把 patch 目标从 `app.routes.user.ensure_billing_initialized` 改为
importing
module（`app.services.stripe.entitlement.ensure_billing_initialized`），符合
`services/claw-interface/CLAUDE.md` 的 "patch the importing module" 约定

## Why safe

- `ensure_billing_initialized` 的真正实现就在
`app/services/billing.py:197`；`routes/user.py:21` 仅 re-export
- `app/services/billing.py` 不 import 任何 `app.services.stripe.*` —— 无循环
- 切 canonical 位置后，service 层不再反向依赖 route 层

## Item 1/2/3 状态

- Item 1 (`_short_id` 重复) —— 已被 PR #769 统一到 `safe_short_id`
- Item 2 (`COLLECTION_NAME` 重复) —— 已被 mongo→repo 迁移 PR 消化
- Item 3 (checkout.py:299 pro/ultra 用 `PLAN_STARTER_20_MONTH`) ——
调查后确认**非 bug**：BG plan_code 体系只区分 free / starter_20_month 两档，所有付费档位（含
Apple、主流程、邀请 trial）都写这个常量，tier 差异由 `PLAN_CREDITS` 和 `sync_team_models`
表达。会单独起一个 doc-only PR 补注释防止再误判

## Test plan

- [x] `ruff format . && ruff check .` — pass
- [x] `pyright app/ tests/` — 0 errors, 0 warnings
- [x] `pytest tests/unit/` — stripe 相关 27 passed；2 个 pre-existing
failure 在 `test_skill_injector.py` 与本 PR 无关（已在 HEAD 复现）
- [x] `pytest tests/bdd/step_defs/test_stripe_webhooks.py
tests/bdd/step_defs/test_stripe_webhook_dispatch.py` — 53 passed

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [51f8dea](https://github.com/SerendipityOneInc/ecap-workspace/commit/51f8deae24759a6324a919502f28bf442a8e7107) refactor(claw-interface): centralize collection constants and repo writes (#784)

**作者**: Chris@ZooClaw  
**SHA**: `51f8deae24759a6324a919502f28bf442a8e7107`

```
## Summary
- add app/database/collections.py as the canonical home for Mongo
collection constants
- move Stripe user subscription field updates into
app.database.user_repo
- add incremental lint rules for service direct mongo imports and new
COLLECTION_NAME / hardcoded collection aliases

## Verification
- python3 -m compileall services/claw-interface/app
services/claw-interface/tests
- ruff check on touched backend files
- ruff format --check on touched backend files
- bash
services/claw-interface/scripts/ci-lint/04-no-direct-mongo-in-services.sh
- bash
services/claw-interface/scripts/ci-lint/05-no-new-collection-name-constants.sh

## Notes
- local pytest is unavailable in this environment (python3 -m pytest
reports No module named pytest)
- local pyright is unavailable as a system command, but the repo
pre-commit hook path still passed

## Follow-up review fixes (rebased onto latest main)

Rebased the single commit onto `main` (PRs #785/#786 had moved ahead)
and resolved the `services/claw-interface/CLAUDE.md` conflict by keeping
main's updated Architecture/Testing sections and slotting in the new
"Collection name constants" bullet.

Addressed reviewer feedback:

- **Codex (NEED_HUMAN_REVIEW, high risk)** —
`04-no-direct-mongo-in-services.sh` misclassified existing violations as
new whenever `origin/$BASE_REF` wasn't reachable (offline dev, shallow
clone). Added a `git rev-parse --verify` guard to both scripts (04 and
05); when the base ref is unreachable they now emit WARNINGs and `exit
0` instead of blocking CI with false positives. Verified locally:
`GITHUB_BASE_REF=does-not-exist bash …` produces warnings only, exit 0.
- **Claude (non-blocking)** — deleted `app/services/stripe/utils.py`; it
was already dead on main (the only references were its own constants, no
importers anywhere in `services/claw-interface/`). Confirmed via `git
grep -E 'from app\.services\.stripe\.utils|from app\.services\.stripe
import utils'` on both branches returning no hits.
- **Claude (non-blocking, script 05 coverage gap)** —
`05-no-new-collection-name-constants.sh` now also diffs `app/cron/`, so
new `*_COLLECTION = "..."` additions under `app/cron/` are blocked. The
pre-existing `subscription_cron.py:USERS_COLLECTION` stays grandfathered
(it's not on the added-line side of the diff).

Local verification on the rebased branch:
- `pyright app/ tests/` → 0 errors, 0 warnings, 0 informations
- `pytest tests/unit/` → 2284 passed (1 unrelated pre-existing failure
in `tests/unit/test_skill_injector.py`, which this PR does not touch)
- both lint scripts pass in online mode and degrade cleanly in offline
mode
```

### [8c8b5aa](https://github.com/SerendipityOneInc/ecap-workspace/commit/8c8b5aa9e67de82571ef9aabd4cdef2d5cc3aefd) chore(web): #754 schedule+agents-manager LEGIT 行内豁免 (A3/9) (#789)

**作者**: Chris@ZooClaw  
**SHA**: `8c8b5aa9e67de82571ef9aabd4cdef2d5cc3aefd`

```
## Summary

- Issue #754 阶段 A 第 3 个 PR:5 个 schedule/agents-manager 文件从
`web/eslint.config.mjs` 的 `ignores` 移到行内 `eslint-disable-next-line
react/forbid-dom-props` + 中文原因注释。
- 不改任何样式值、className 或 JSX 结构。

## 涉及文件(5 文件,~21 处)

- `src/app/[locale]/schedule/AllJobsSection.tsx`(1 处:静态 fontFamily 栈)
- `src/app/[locale]/schedule/DailyTaskList.tsx`(1 处:tooltip 箭头通过 `color`
token 注入边色)
- `src/app/[locale]/agents-manager/AgentsManagerClient.tsx`(8 处:1 skill
chip + 7 modal overlay)
- `src/app/[locale]/agents-manager/[id]/AgentDetailClient.tsx`(7 处:全
modal overlay)
- `src/app/[locale]/agents-manager/publish/PublishAgentsClient.tsx`(4
处:全 modal overlay)

## 观察:重复模式可后续抽离

agents-manager 三个 client 重复 18 次同一行:

```jsx
<div className="absolute inset-0" style={{ backgroundColor: 'var(--ecap-overlay-heavy)' }} />
```

每处 disable 注释都标了 \`可改 className=\"bg-[var(--ecap-overlay-heavy)]\" 或抽出
<ModalOverlay />\`,留给后续重构 PR(超出本计划范围)。

## Ignores 缩减

`web/eslint.config.mjs` 的 `react/forbid-dom-props` ignores 列表从 63 → 58(减
5)。注:agents-manager 三个文件同时也在 **复杂度规则** 的 ignores 中(L297-299),那是另一个
ESLint 规则的豁免,不动。

## Test plan

- [x] `pnpm lint` pass(无 unused-disable 警告)
- [ ] CI `code-quality / lint-and-test` 绿
- [ ] 视觉无变化(未改样式)

## 关联

- Issue: #754
- 计划:9 个 PR 中的 A3(LEGIT 4 个 PR 的第 3 个)
- 前一个 PR:#787(已合并)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [b2fe6bd](https://github.com/SerendipityOneInc/ecap-workspace/commit/b2fe6bda1906f254060471e6c790f06e5502cd73) chore(web): #754 onboarding+chat LEGIT 行内豁免 (A2/9) (#787)

**作者**: Chris@ZooClaw  
**SHA**: `b2fe6bda1906f254060471e6c790f06e5502cd73`

```
## Summary

- Issue #754 阶段 A 第 2 个 PR:6 个 onboarding/chat 文件从
`web/eslint.config.mjs` 的 `ignores` 移到行内 `eslint-disable-next-line
react/forbid-dom-props` + 中文原因注释。
- 不改任何样式值或 className,只把"豁免位置"从文件级降到行级。

## 涉及文件(6 文件,~22 处)

- `src/components/onboarding/animals/AnimalAvatar.tsx`(4 处 DOM,按 prop
size 与 companionId palette 派生;3 处 motion.div 不触发规则)
- `src/components/onboarding/SpriteGuide.tsx`(3 处:size + 两段动画,标注"MOD 类,待
CSS module 抽离")
- `src/components/onboarding/SpriteDialogue.tsx`(1 处 DOM `<span>`
荧光笔色,标注 MOD;motion.p 不触发规则)
- `src/app/[locale]/chat/components/ChatWelcome.tsx`(9 处,step indicator
按 step.done 派生颜色/边框)
- `src/app/[locale]/chat/components/GenClawInput.tsx`(1 处
`display:none`,标注待改 `className="hidden"`)
- `src/app/[locale]/chat/components/SubagentChatPanel.tsx`(2 处:panel
宽度按拖拽动态、input `display:none` 静态)

## Ignores 缩减

`web/eslint.config.mjs` ignores 列表从 69 → 63(减 6)。

## 备注

- 与 A1 同一规律:`react/forbid-dom-props` 不触发于 `motion.div` /
`motion.p`(framer-motion JSXMemberExpression),所以这些位置无需 disable。
- ChatWelcome 中多处 `width: 60` / `width: 280` 等是静态值,在 disable 注释里标"待后续
Tailwind 化",留给 TW 扫荡 PR。

## Test plan

- [x] `pnpm lint` pass(无 unused-disable 警告)
- [ ] CI `code-quality / lint-and-test` 绿
- [ ] 视觉无变化(未改样式)

## 关联

- Issue: #754
- 计划:9 个 PR 中的 A2(LEGIT 4 个 PR 的第 2 个)
- 前一个 PR:#780(已合并)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [d1cfd08](https://github.com/SerendipityOneInc/ecap-workspace/commit/d1cfd080743f7aeff2df6e9c4d1e44200fb0d84b) docs: slim CLAUDE.md — lean on lint & scripts instead of inline duplication (#788)

**作者**: Chris@ZooClaw  
**SHA**: `d1cfd080743f7aeff2df6e9c4d1e44200fb0d84b`

```
## Summary
- Trim 4 CLAUDE.md files (root / `web/` / `services/claw-interface/` /
`web/src/app/landing/`) by removing inline duplication of rules already
enforced by lint/pre-commit or discoverable via `package.json` /
`pyproject.toml` / `ls` / `grep`. Retains non-obvious gotchas,
cross-repo wiring, and architectural constraints that tooling cannot
surface.
- Add `no-restricted-imports` ESLint rule in `web/eslint.config.mjs`
forbidding `@testing-library/jest-dom` (the package is not installed;
web CLAUDE.md previously enforced this with a single sentence).
- `ios/ZooClaw/CLAUDE.md` intentionally untouched.

Net change: 116 lines removed, 50 added.

## Test plan
- [x] `pnpm lint` (web/) — clean
- [x] Manually verified the new ESLint rule fires on a probe file
importing `@testing-library/jest-dom`
- [ ] CI `code-quality / lint-and-test` passes
- [ ] CI `python-code-quality / build-and-test` passes

## Notes
- `pnpm lint` only covers `src/`, so the `no-restricted-imports` rule is
advisory for `tests/` (called out explicitly in web/CLAUDE.md).
Expanding lint to `tests/` surfaces ~1.7k pre-existing prettier errors —
out of scope here.
- Follow-ups (not blockers): consider adding a `lint:tests` script or
pre-commit hook to bring `tests/` under ESLint; the grandfather
inline-style / complexity legacy lists in `eslint.config.mjs` remain the
canonical ledger.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [6a31e85](https://github.com/SerendipityOneInc/ecap-workspace/commit/6a31e8577d45676b6d6db441532c772df7d031f5) feat(openclaw): support deeper workspace path detection (#775)

**作者**: nolan-srp  
**SHA**: `6a31e8577d45676b6d6db441532c772df7d031f5`

```
## Summary
- extend custom agent workspace discovery to also check levels 3, 4, and
5 for both `workspace` and `workspace-*`
- keep ambiguity handling consistent by failing when multiple matches
are found at the same depth/pattern
- update runtime documentation comment to reflect deeper search order
- extend unit test assertion to verify deeper-level workspace lookup is
present

## Changes
- updated deployment install script generation in `agent_deploy.py`
- updated runtime install script generation in `agent_runtime.py`
- updated unit test in `test_openclaw_agents.py`
```

### [15336d0](https://github.com/SerendipityOneInc/ecap-workspace/commit/15336d02fe12b59ad9682fe8b0758af80ccd14f8) feat(web): 将用户手册集成为官网公开页面 (#743)

**作者**: lynn Zhuang  
**SHA**: `15336d02fe12b59ad9682fe8b0758af80ccd14f8`

```
## 概要
  - 将 iframe 方式的 `/userguide` 替换为完整的 `UserGuideClient`
  组件（PublicHeader + 内容 + PublicFooter）
  - 新增左侧悬浮章节导航，支持滚动定位高亮，滚动到 footer 区域自动隐藏
  - 在官网首页、Pricing、User Guide 页面的顶部导航统一添加 "User Guide" 入口
  - 将 `/userguide` 注册为官网公开页面（不显示 app 侧边栏）
  - 7 种语言新增 `publicNav.userGuide` 翻译
  - 登录后侧边栏点击 "User Guide" 在新标签页打开官网用户手册

  ## 测试计划
  - [ ] 访问 `/en/userguide` — 页面正常渲染，含顶部导航和底部 footer，无 app
  侧边栏
  - [ ] 顶部导航样式与官网首页完全一致
  - [ ] 左侧悬浮导航正常显示，滚动时高亮对应章节
  - [ ] 滚动到 footer 区域时悬浮导航消失，离开后恢复
  - [ ] 屏幕宽度 < 1100px 时悬浮导航自动隐藏
  - [ ] FAQ 手风琴展开/收起正常
  - [ ] 官网首页和 Pricing 页面顶部导航显示 "User Guide"
  - [ ] 登录状态下侧边栏 "User Guide" 在新标签页打开 `/en/userguide`
  - [ ] 中文语言 `/zh/userguide` 正确显示中文内容
<img width="2516" height="1854" alt="image"
src="https://github.com/user-attachments/assets/9933eeda-ccba-4e34-96f1-92ff274c77a5"
/>
<img width="2554" height="1868" alt="image"
src="https://github.com/user-attachments/assets/3421b62b-6637-41c8-af45-02aa4f34ae8e"
/>

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@LynndeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>
```

### [f4fd528](https://github.com/SerendipityOneInc/ecap-workspace/commit/f4fd528cd360928a2d92d85e5b3c8e8651c19003) docs(api): refresh CLAUDE.md after service-layer mongo→repo migration (#786)

**作者**: Chris@ZooClaw  
**SHA**: `f4fd528cd360928a2d92d85e5b3c8e8651c19003`

```
## Summary
Bring \`services/claw-interface/CLAUDE.md\` in sync with the conventions
established by the 9-PR refactor series that just landed (#765–#785).
Pure docs change.

### Architecture section
- Tighten the repo rule: applies to **service code AND route code**, not
just route handlers
- Call out load-bearing atomic primitives so callers don't reinvent them
— \`user_repo.update_and_unset_fields\`,
\`update_and_increment_fields\`, \`orders_repo.claim_entitlement_lock\`
- Name the legacy holdouts (\`routes/admin_boost.py\`,
\`routes/invite_code.py\`, \`routes/subscription.py\`) so future work
doesn't extend them with new direct \`mongo\` usage

### Testing section
- Document the BDD silent-skip footgun on the dev container: defaults
assume \`mongo:mongo@mongo:27017\` but the dev container has bare
unauth'd mongod on \`127.0.0.1\`. Without the env override BDD passes
vacuously, masking regressions (recently bit a PR that reviewers caught
by code-reading)
- Document the shared \`tests/unit/conftest.py\` fixtures
(\`current_user\`, \`mock_user_repo\`, \`mock_orders_repo\`) and
\`_stripe_helpers.py\` builders (\`make_stripe_event\`, \`make_*_user\`,
\`make_*_order\`) so they get adopted instead of redefined inline
- Document the post-migration mock conventions: patch the **importing
module** (not \`app.database.user_repo\`); use \`call_args[0][1]\` for
the 2-arg repo signature; use \`call_args.kwargs[\"set_fields\"]\` for
the keyword-only atomic primitives

## Test plan
- [x] \`git diff\` is scoped to the two replacement blocks; no
whitespace drift, no other lines touched
- [x] No code/tests changed — no CI requirements beyond the doc lint
- [ ] CI green

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [1c18f04](https://github.com/SerendipityOneInc/ecap-workspace/commit/1c18f0429943cac96fe08fa8367e031cc23b1831) chore(api): gitignore auto-cloned connectors + finish stripe event helper migration (#785)

**作者**: Chris@ZooClaw  
**SHA**: `1c18f0429943cac96fe08fa8367e031cc23b1831`

```
## Summary
Two small follow-ups after #783 merged:

1. **gitignore the auto-cloned connector skills** — `tests/conftest.py`
clones `SerendipityOneInc/claw-connector-skills` into
`app/skills/connectors/<name>/` on first test run, but those
subdirectories weren't gitignored. Any \`git add .\` after running tests
would re-introduce all 39 files (#783 hit this — Codex had to remove
them in commit \`476b5b08\`). One-line `.gitignore` pattern:

   ```
   app/skills/connectors/*/
   ```

The package's own \`__init__.py\` stays tracked because the \`*/\` glob
only matches directories.

2. **Finish stripe event helper migration** — #783 converted 12 inline
\`event = {\"data\": {\"object\": ...}}\` dicts to
\`make_stripe_event(...)\`, but missed the one in
\`test_stripe_coverage.py::TestHandleTrialWillEnd::test_success_updates_reminder\`
because its longer object payload (extra \`default_payment_method\`
field) didn't match the bulk sed pattern. Now consistent with the other
12 sites.

## Test plan
- [x] \`ruff format\` + \`ruff check\` clean
- [x] \`pyright app/ tests/\` → 0 errors, 0 warnings
- [x] \`pytest tests/unit/test_stripe_coverage.py\` → 23 passed
- [x] \`git check-ignore\` confirms \`connectors/airtable/SKILL.md\` is
ignored, \`connectors/__init__.py\` stays tracked
- [ ] CI green

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

## 2026-04-14

### [2269038](https://github.com/SerendipityOneInc/ecap-workspace/commit/2269038adc48b75fb59d43f1c22afbcef807cf9e) test(claw-interface): deduplicate Stripe unit test fixtures and helpers (#783)

**作者**: Chris@ZooClaw  
**SHA**: `2269038adc48b75fb59d43f1c22afbcef807cf9e`

```
## Summary
- move shared `current_user`, `mock_user_repo`, and `mock_orders_repo`
fixtures into `tests/unit/conftest.py`
- add `make_stripe_event()` to centralize the Stripe webhook event
envelope used across tests
- replace small class-based mapping tests in
`test_subscription_manager.py` with `pytest.mark.parametrize`
- remove helper import aliases and repeated inline webhook payload
boilerplate in Stripe-related tests

## Scope
- test-only refactor
- no production code changes

## Validation
- current PR diff is limited to 7 files under
`services/claw-interface/tests/unit`
- GitHub `code-quality` is green on the current head

---------

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: Chris@ZooClaw <chris-srp@users.noreply.github.com>
```

### [b597470](https://github.com/SerendipityOneInc/ecap-workspace/commit/b5974705c5c4e81dd551a4c2b985ff41170dbfdb) refactor(api): billing.py + subscription_manager.py drop direct mongo, use repos (#781)

**作者**: Chris@ZooClaw  
**SHA**: `b5974705c5c4e81dd551a4c2b985ff41170dbfdb`

```
## Summary

Final piece of the non-stripe service migration started in #779. After
this PR, **no service module under \`app/services/\` touches \`mongo\`
directly** — the CLAUDE.md architecture rule is fully enforced at the
service layer.

### Source migrations
- \`billing.py\` — 6 sites (1 \`read_one\` + 5 \`update\`) →
\`user_repo.get_user\` / \`update_fields\`. Drops the now-unused
\`COLLECTION_NAME\` re-import from profile, and tightens the uid guard
in \`_check_and_recreate_wallets\` to satisfy \`update_fields\`' strict
\`str\` typing (latent type bug uncovered by the migration; behavior
preserved — \`None\` uid was already a no-op).
- \`subscription_manager.py\` — 12+ sites → \`user_repo\` +
\`orders_repo\`. Drops the unused \`USERS_COLLECTION\` constant;
re-exports it as a backward-compat alias for
\`app/routes/admin_boost.py\` (which still uses it for direct mongo).
\`ORDERS_COLLECTION\` dropped outright (no external users).

### New repo primitives
Two query shapes that the existing \`user_repo\` / \`orders_repo\` API
didn't cover:

- \`user_repo.update_and_increment_fields(uid, *, set_fields,
inc_fields)\` — used by \`transition_to_active(increment_cycles=True)\`
to flip subscription state and bump \`completed_billing_cycles\` in a
single atomic write
- \`orders_repo.find_recent_subscription_grant(uid, since)\` — used by
the cron renewal job to detect that a webhook (or prior cron run)
already processed this billing cycle

Both come with focused query-shape unit tests in \`test_user_repo.py\` /
\`test_orders_repo.py\`.

### Test changes
- \`test_user_repo.py\` — adds \`TestUpdateAndIncrementFields\` (1 test
pinning the \`\$set + \$inc\` query shape)
- \`test_orders_repo.py\` — adds \`test_find_recent_subscription_grant\`
(1 test pinning the dedup query)
- \`test_subscription_manager.py\` — fixture renamed \`mock_mongo\` →
\`mock_user_repo\` (now exposes the typed repo methods); new
\`mock_orders_repo\` fixture; all patches retargeted; assertions updated
for the 2-arg \`update_fields\` signature (\`[0][1]\` instead of
\`[0][2]\`) and the keyword-only \`update_and_increment_fields\` call
shape
- \`test_user_billing.py\` — same retargeting for billing.py tests
(TestCheckAndRecreateWallets + TestDoBillingInit)
- \`test_process_cron_renewal.py\` — full rewrite to mock
\`orders_repo\` and \`user_repo\` separately; preserves every behavioral
assertion (dedup paths, pending_downgrade clear, increment_cycles flag)
on the new repo surface

## Out of scope (deferred)
\`app/routes/admin_boost.py\` and \`app/routes/invite_code.py\` still
use direct mongo for admin endpoints. The route-layer migration is a
separate follow-up — this PR stays focused on the service layer.

## Test plan
- [x] \`ruff format\` + \`ruff check\` clean
- [x] \`pyright app/ tests/\` → 0 errors, 0 warnings
- [x] All 100+ affected unit tests pass (34 subscription_manager + 32
user_billing + 5 cron_renewal + repo tests)
- [x] Full local sweep with mongo: 2442 passed / 177 failed — same 177
as main baseline (pre-existing pollution, verified via \`stash + diff\`)
- [ ] CI green

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [aec527b](https://github.com/SerendipityOneInc/ecap-workspace/commit/aec527b5bb574cd7cc8078070d1c77054bb5f1ae) chore(web): #754 canvas LEGIT 行内豁免 (A1/9) (#780)

**作者**: Chris@ZooClaw  
**SHA**: `aec527b5bb574cd7cc8078070d1c77054bb5f1ae`

```
## Summary

- Issue #754 阶段 A 第 1 个 PR:canvas 目录 7 个 LEGIT 文件从
`web/eslint.config.mjs` 的 `ignores` 移到行内 `eslint-disable-next-line
react/forbid-dom-props` + 中文原因注释。
- 不改任何样式值、className 或 JSX 结构;只做"豁免位置"从文件级降到行级,让 ignores 列表只保留真正待迁移的
TODO。
- 3 处在注释中标注"静态值,待后续 Tailwind 化",留给后续 TW 扫荡 PR 顺便清理。

## 涉及文件

- \`src/app/[locale]/canvas/nodes/LayerEditorNode.tsx\`(5 处动态,layer
坐标/尺寸/opacity/outline/cursor)
- \`src/app/[locale]/canvas/nodes/ResultCardNode.tsx\`(1 处静态
\`maxHeight: '240px'\` — 标注待 TW 化)
- \`src/app/[locale]/canvas/nodes/VideoNode.tsx\`(1 处静态 \`maxHeight:
'240px'\` — 标注待 TW 化)
- \`src/app/[locale]/canvas/components/ChatPanel.tsx\`(1 处静态 \`display:
'none'\` — 标注待改 \`className="hidden"\`)
- \`src/app/[locale]/canvas/components/ImageActionMenu.tsx\`(dialog 动态坐标
+ 静态 transform)
- \`src/app/[locale]/canvas/components/ReframeParamsDialog.tsx\`(dialog
动态坐标)
- \`src/app/[locale]/canvas/components/UpscaleParamsDialog.tsx\`(dialog
动态坐标)

## Ignores 缩减

\`web/eslint.config.mjs\` ignores 列表从 76 → 69(减 7)。

## Test plan

- [x] \`pnpm lint\` pass(规则在这 7 个文件上激活,所有 inline style 有对应的行内豁免)
- [x] \`pnpm tsc --noEmit\` pass
- [ ] CI \`code-quality / lint-and-test\` 绿
- [ ] 视觉无变化(未改样式值,理论上零回归;如有 canvas 相关 E2E 自动覆盖)

## 关联

- Issue: #754
- 计划:9 个 PR 中的 A1(LEGIT 行内豁免 4 个 PR 的第 1 个)
- 前置:#741 已合并,\`react/forbid-dom-props\` 规则已在 main 生效

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [5917721](https://github.com/SerendipityOneInc/ecap-workspace/commit/5917721bbe9d55858d5d1924190d1c0fe3370469) refactor(api): new invite_code_repo + profile_repo, migrate services off mongo (#779)

**作者**: Chris@ZooClaw  
**SHA**: `5917721bbe9d55858d5d1924190d1c0fe3370469`

```
## Summary

Adds two new repo modules and migrates the matching service-layer files
off direct \`mongo.*\` access. First of two PRs in this slice — **PR
C2** to follow with \`billing.py\` + \`subscription_manager.py\` (both
target existing user_repo / orders_repo).

### New repos
- \`app/database/invite_code_repo.py\` — encapsulates
\`ecap-invite-codes\`, including the load-bearing **CAS** primitives
\`claim_binding\` / \`release_binding\` that prevent over-binding under
concurrent requests
- \`app/database/profile_repo.py\` — single-document \`gem_account\`
fetch by integer uid (multi-doc reads stay in \`user_repo\`)

### Service migrations
- \`app/services/invite_code.py\` — all 7 mongo sites moved to
\`invite_code_repo\` (read_one, db.find_one, db.update_one × 2, create,
db.update_one for release)
- \`app/services/profile.py\` — single \`mongo.read_one\` moved to
\`profile_repo\`

Both modules keep \`INVITE_COLLECTION_NAME\` /
\`PROFILE_COLLECTION_NAME\` re-exports for backward compat with route +
lifetime + BDD-fixture callers that still import the constant directly.

## Tests

- New \`tests/unit/test_invite_code_repo.py\` (10 tests) — pins the CAS
filter shape (active/expiry guards, used_bindings drift check, \`\$ne\`
uid), the \`\$inc\`/\`\$push\`/\`\$pull\` update operators, and the
positional projection on \`get_binding_for_uid\`
- New \`tests/unit/test_profile_repo.py\` (2 tests) — pins the
integer-uid query shape
- Existing \`tests/unit/test_invite_codes.py\` retargeted from
\`services.invite_code.mongo\` to
\`services.invite_code.invite_code_repo\`; mongo-query-shape assertions
moved to the new repo tests where they belong
- Existing \`tests/unit/test_user_billing.py::TestGetUserProfile\`
retargeted to \`services.profile.profile_repo\`

## Out of scope (deferred to separate PRs)

- \`app/routes/invite_code.py\` still touches mongo directly (admin list
/ create endpoints, profile batch fetch). Keeping this PR focused on the
service layer; route migration is a clean follow-up.
- \`app/services/billing.py\` (6 sites) and
\`app/services/subscription_manager.py\` (12+ sites) — both target the
**existing** \`user_repo\` / \`orders_repo\` (no new repo needed) — will
land in PR C2.

## Test plan

- [x] \`ruff format\` + \`ruff check\` clean
- [x] \`pyright app/ tests/\` → 0 errors, 0 warnings
- [x] All 100 affected unit tests pass (12 invite_codes + 9 user_billing
+ 12 invite_code_repo + 2 profile_repo + others)
- [x] Full local sweep with mongo: 2445 passed / 177 failed — same 177
as main baseline (pre-existing test pollution from running suites
together; verified via \`stash + diff\`)
- [ ] CI green

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [2daf91f](https://github.com/SerendipityOneInc/ecap-workspace/commit/2daf91f03cfef8ba8ddc4f09297497198bf105a0) refactor(api): stripe handlers/ drop direct mongo, use repos (#774)

**作者**: Chris@ZooClaw  
**SHA**: `2daf91f03cfef8ba8ddc4f09297497198bf105a0`

```
## Summary
Completes the stripe-side migration started in #771. After this PR, **no
file under `app/services/stripe/` touches `mongo.*` directly** — every
read/write goes through `app/database/{user_repo,orders_repo}.py`,
satisfying the CLAUDE.md architecture rule.

### Source migrations
- `handlers/_common.py` → `user_repo.update_fields`
- `handlers/trial.py` → `user_repo.get_by_stripe_customer_id` +
`update_fields`
- `handlers/payment_intent.py` → `orders_repo.get_by_payment_intent_id`
+ `update_by_id`
- `handlers/subscription.py` → `user_repo.get_by_stripe_customer_id` +
`update_fields`
- `handlers/checkout.py` — full migration:
`orders_repo.{get_by_session_id,get_by_order_id,update_by_id,link_session_id}`
+ `user_repo.{get_user,update_and_unset_fields}`
- `handlers/invoice.py` — full migration: includes
`orders_repo.create_renewal_order`, the cron-renewal lookup via
`get_by_order_id` + `entitlement_granted` post-filter, and
`user_repo.update_and_unset_fields` for
pending-downgrade-applied-at-renewal

### Repo addition
`user_repo.update_and_unset_fields(uid, *, set_fields, unset_fields)` —
atomic ``\$set`` + ``\$unset`` for the two handler call sites
(checkout's upgrade-clears-pending-downgrade; invoice's
pending-downgrade-applied-at-renewal) that need both sides of a flag
transition to land in a single write.

### Test changes
- BDD step defs (`call_handle_checkout` / `call_handle_pi` /
`call_handle_invoice` / `call_update_sub_info`) rewritten to patch
`user_repo` / `orders_repo` separately rather than one shared `mongo`
mock
- Unit tests `test_checkout_context_loader.py` and
`test_checkout_path_helpers.py` fully rewritten — they previously
patched `checkout.mongo` and asserted on collection-tagged calls; now
they patch repo modules and assert on per-method calls
- `TestHandleTrialWillEnd`, `TestHandleSubscriptionUpdated`,
`TestHandleSubscriptionDeleted*` retargeted to `user_repo`; mock
variables renamed for accuracy
- `call_args[0][2]` → `call_args[0][1]` indexing shift for the 2-arg
repo signature

## Test plan
- [x] `ruff format` + `ruff check` clean
- [x] `pyright app/ tests/` → 0 errors, 0 warnings
- [x] Full local sweep with mongo: 2430 passed (matches `main` baseline;
the 177 pre-existing failures from cross-suite test pollution are
unchanged by this PR — verified by stash + diff)
- [x] Targeted: 91 stripe + checkout helper unit tests pass; 43 stripe
BDD tests pass
- [ ] CI green

---------

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [1ba934a](https://github.com/SerendipityOneInc/ecap-workspace/commit/1ba934a65e2156907cdfa7175a90346ee4556d4f) refactor(api): stripe non-handler services drop direct mongo, use repos (#771)

**作者**: Chris@ZooClaw  
**SHA**: `1ba934a65e2156907cdfa7175a90346ee4556d4f`

```
## Summary
Enforces the CLAUDE.md rule that only `app/database/*_repo.py` touches
`mongo` directly. First of two PRs (B2 to follow with the handlers/
files).

- `entitlement.py` → `user_repo.get_user` / `user_repo.update_fields`
- `billing_gateway.py` → `user_repo.get_user` for wallet-recovery reads
- `portal.py` → `user_repo.get_user` / `user_repo.update_fields`
- `order_confirm.py` → `orders_repo.get_by_session_id` /
`get_by_order_id` / `update_by_id`

## Test-side changes
- Retarget `@patch("*.mongo")` → `@patch("*.user_repo")` /
`@patch("*.orders_repo")` in affected unit + BDD tests
- Rename `mock_mongo` to `mock_user_repo` / `mock_orders_repo` for
accuracy (variables were holding repo mocks after the patch swap)
- Update assertions whose mongo signatures changed:
`update.call_args[0][2]` → `update_fields.call_args[0][1]`; split
combined `read_one` mock lists into per-method mocks
- BDD passthrough in `test_stripe_order_confirm` rewritten to wrap
`get_by_session_id` / `get_by_order_id` around the real `mongo.read_one`

## Out of scope (for PR B2)
Handlers under `app/services/stripe/handlers/**` — `checkout.py`,
`invoice.py`, `payment_intent.py`, `subscription.py`, `trial.py`,
`_common.py` — still use `mongo` directly. Splitting keeps this PR
readable; the handlers PR will need a new
`user_repo.update_and_unset_fields` helper for the `$set + $unset` cases
in `invoice.py` and `checkout.py`.

## Test plan
- [x] `ruff format .` + `ruff check .` clean
- [x] `pyright app/ tests/` → 0 errors, 0 warnings
- [x] `pytest tests/unit/test_stripe_*
tests/unit/test_subscription_manager.py
tests/unit/test_entitlement_idempotency.py` → 122 passed
- [ ] CI green (unit + BDD with mongo service container)

---------

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [b0afda6](https://github.com/SerendipityOneInc/ecap-workspace/commit/b0afda6241bd6a845cafe57611d926d838926e5d) refactor(api): convert remaining sync stripe.Subscription.retrieve() to async (#747) (#772)

**作者**: Chris@ZooClaw  
**SHA**: `b0afda6241bd6a845cafe57611d926d838926e5d`

```
## Summary

Converts the last two sync `stripe.Subscription.retrieve()` call sites
inside async handlers to `await
stripe.Subscription.retrieve_async(...)`:

- `app/services/stripe/handlers/invoice.py:47` — `handle_invoice_paid`
- `app/services/stripe/order_confirm.py:128` — `confirm_order`

Both handlers were already `async def`; the sync Stripe API blocks the
asyncio event loop for ~100-500ms per call, which is visible latency on
the webhook / order-confirm paths. This matches the async pattern
already established in `handlers/checkout.py`, `subscription_cron.py`,
and the shared `services/stripe/client.py` helpers.

## Test updates

BDD step defs patch the mocked Stripe module — all 6 call sites updated
to target `retrieve_async` with `AsyncMock`:
- `tests/bdd/step_defs/test_stripe_webhooks.py:718, 767`
- `tests/bdd/step_defs/test_stripe_webhook_dispatch.py:777`
- `tests/bdd/step_defs/test_stripe_order_confirm.py:202, 413, 466, 490`

Issue mentioned a `test_stripe_invoice_dedup.py:156` — that file no
longer exists (absorbed into `test_stripe_webhooks.py` by #753).

## Test plan
- [x] `ruff format .` — applied
- [x] `ruff check .` — All checks passed
- [x] `pyright app/ tests/` — 0 errors, 0 warnings
- [x] `pytest tests/bdd/step_defs/test_stripe_webhooks.py
tests/bdd/step_defs/test_stripe_order_confirm.py
tests/bdd/step_defs/test_stripe_webhook_dispatch.py` — 64 passed
- [x] `pytest tests/unit/test_stripe_*.py
tests/unit/test_subscription_manager.py
tests/unit/test_checkout_path_helpers.py` — 121 passed
- [ ] CI green

Resolves #747.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [825e065](https://github.com/SerendipityOneInc/ecap-workspace/commit/825e0658c685f2a811f43e620a2ddc508bc6a351) fix(chat): 聊天图片改为当前页面 lightbox 预览 (#762)

**作者**: lynn Zhuang  
**SHA**: `825e0658c685f2a811f43e620a2ddc508bc6a351`

```
## 概要
  - 修复聊天中点击 agent 生成的图片会打开新标签页的问题
  - 改为使用项目已有的 `ImagePreview` 组件在当前页面内以 lightbox 形式预览
  - 仅修改 `MMAttachments.tsx` 中 `ImageAttachment` 的点击行为
  - 保留 fallback：非 chat 页面仍降级为新标签页打开

  ## 测试计划
  - [ ] 在 chat 中点击 agent 生成的图片，确认在当前页面弹出 lightbox 预览
  - [ ] 预览支持关闭（ESC 键 / 点击遮罩）
  - [ ] 预览支持下载
  - [ ] 多张图片场景下 gallery 模式正常（如适用）
<img width="2556" height="1862" alt="image"
src="https://github.com/user-attachments/assets/f07645e0-e8bd-46d6-8ac2-62309b964198"
/>

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@LynndeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>
```

### [54c0353](https://github.com/SerendipityOneInc/ecap-workspace/commit/54c03539797e96376a4af43080091b2ed09ecee5) ci: staging branch auto-deploy (frontend + backend) + post-release reset (#759)

**作者**: sam-srp  
**SHA**: `54c03539797e96376a4af43080091b2ed09ecee5`

```
## Summary

Add a single `staging` branch that auto-deploys both frontend and
backend, plus post-release reset logic mirroring
[`favie-gem-workflow`](https://github.com/SerendipityOneInc/favie-gem-workflow/blob/main/.github/workflows/build-and-deploy.yml).

- **Push to `staging`** → both workflows fire → frontend deploys to
Cloudflare staging, backend deploys to GKE staging
- **Tag-driven triggers** (`ecap-v*-beta`, `service-v*-beta`, release
tags) keep working unchanged
- **Post-release reset**: after a `*-release` tag deploys to production,
the corresponding workflow evaluates its own version bump:
- Major/minor bump → `git reset --hard origin/main` + force push
`staging`, Feishu notify
  - Patch-only → `staging` stays, Feishu notify (no reset)
- Resets from both workflows are idempotent (target is always
`origin/main`), so near-concurrent frontend+backend releases are safe.

## Design notes

- Each reset job lives in its own workflow and keys off its own tag
namespace (`ecap-v*` / `service-v*`). A major bump from either side
resets the shared staging — in-flight work from the other side is wiped.
This is the intended cost of a shared staging branch.
- Dynamic values in new `run:` blocks all pass through `env:` (no `${{
}}` interpolation inside shell) to avoid injection.
- `grep -vFx` instead of `grep -v "^...\$"` so dots in tag names aren't
regex wildcards.
- Reset jobs explicitly gate on `needs.<upstream>.result == 'success'` —
future-proof against `if: always()` edits.
- Both reset jobs handle the edge cases of no previous release tag and
`staging` branch not yet existing.

## Before this becomes useful in the repo

1. Create the `staging` branch once: `git push origin main:staging`
(reset jobs can bootstrap it too, but manual is safer)
2. Ensure `staging` does **not** have "Restrict force push" branch
protection — reset would fail
3. Confirm `FEISHU_CUSTOMERBOT_WEBHOOK` secret is present (notification
gracefully no-ops if missing)

## Test plan

- [ ] Push a no-op commit to `staging`, confirm `Deploy ECAP (Staging)`
and `Service Build and Deploy`'s `deploy-to-staging` both fire
- [ ] Dry-run the next `ecap-v*-release` and verify frontend's
`reset-staging` logic (watch the `decide` step's log)
- [ ] Dry-run the next `service-v*-release` and verify backend's
`reset-staging` logic
- [ ] Verify a patch-only release (e.g. `ecap-v0.5.74-release` after
`0.5.73`) does **not** reset staging
- [ ] Verify a major/minor bump release does reset staging + sends
Feishu notification

---------

Co-authored-by: peter-srp <peter@srp.one>
Co-authored-by: Copilot Autofix powered by AI <62310815+github-advanced-security[bot]@users.noreply.github.com>
```

### [3d9a9b6](https://github.com/SerendipityOneInc/ecap-workspace/commit/3d9a9b60508e4845e53629ece7cebdf57cf2901e) refactor(api): drop stripe.utils.short_id, consolidate to sanitize.safe_short_id (#769)

**作者**: Chris@ZooClaw  
**SHA**: `3d9a9b60508e4845e53629ece7cebdf57cf2901e`

```
## Summary
After #765 made `short_id` public and #767 migrated `openclaw_client` to
`safe_short_id`, the two helpers — `app.services.stripe.utils.short_id`
and `app.services.sanitize.safe_short_id` — were doing near-identical
truncation. This PR removes the duplication.

- Widen `safe_short_id` signature: `raw: str` → `raw: str | None` (body
already handled `None` at runtime via `if not raw`)
- Delete `short_id` from `app/services/stripe/utils.py` (file is now
collection-name constants only)
- Migrate 11 stripe modules: `from app.services.stripe.utils import
short_id` → `from app.services.sanitize import safe_short_id`

`safe_short_id` is the canonical choice: it routes the value through a
frozen dataclass that breaks CodeQL's
`py/clear-text-logging-sensitive-data` taint chain, so stripe modules
pick up the same static-analysis tightening as the rest of the codebase.

## Test plan
- [x] `ruff format` + `ruff check` clean
- [x] `pyright app/ tests/` → 0 errors, 0 warnings
- [x] `pytest tests/unit/test_stripe_*.py
tests/unit/test_subscription_manager.py` → 106 passed
- [ ] CI green

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [8fd7858](https://github.com/SerendipityOneInc/ecap-workspace/commit/8fd7858439a2a0461b021348ae9d791cbce11308) docs(web): module-scoped CLAUDE.md for landing + admin (#768)

**作者**: Chris@ZooClaw  
**SHA**: `8fd7858439a2a0461b021348ae9d791cbce11308`

```
## Summary

建立"成熟模块各有本地 `CLAUDE.md`"的 pattern，首批覆盖 landing 和 admin。子目录 `CLAUDE.md` 在
Claude Code 编辑对应路径文件时按 proximity 加载，比塞在根 `web/CLAUDE.md` 更精准 —— 改 admin
代码时只看 admin 约定，改 landing 时只看 landing 约定，根文件聚焦跨模块规则。

## 改动

| 文件 | 动作 | 行数 |
|---|---|---|
| `web/src/app/landing/CLAUDE.md` | 新建 | +21 |
| `web/src/app/[locale]/admin/CLAUDE.md` | 新建 | +19 |
| `web/CLAUDE.md` | Admin Dashboard section (8 行) → "Module-Scoped
Conventions" pointer (3 行) | -6 |
| `web/eslint.config.mjs` | `forbid-dom-props` grandfather ignores 注释里加
3 行 "SHRINK-ONLY" 警告（不改规则） | +3 |

### Landing CLAUDE.md 内容

文档化 #726–#764 固化出来的约定：
- `LandingClient.tsx` = orchestrator，`components/` 每个 section 一个文件
- URL / 静态数据放 `landingContent.ts`（PR #764 的动机）
- `--landing-*` token 在 `.landing-root {}` scope 内，不是 `:root`
- inline `style={{}}` 全局 ban，landing 下只有 `LandingIntegrations` 数据驱动一处豁免
- 6 条 complexity rules 全部 active，不允许重新豁免

### Admin CLAUDE.md 内容

从 `web/CLAUDE.md:65-73` 整段搬来（react-query、`adminKeys` 中心化、lazy loading
`enabled` flag、SSR-safe QueryClientProvider、测试 helper），开头补一段 Structure
说明 `AdminClient.tsx` + `components/` + `hooks/` + `lib/` 四层结构。

### ESLint shrink-only note

`forbid-dom-props` 的 76-file grandfather ignores 列表是 PR #756
的历史债务。原注释说"touch a file → migrate + remove from list"，但没明说"禁止增"。本 PR
在原注释末尾加一句 SHRINK-ONLY，明确把它写进代码保护层：

```js
// SHRINK-ONLY: do NOT add new entries here. Adding a new file
// regresses the guardrail — fix the file or use a narrower inline
// eslint-disable-next-line with a reason instead.
```

## 未覆盖模块

`canvas/` 和 `chat/` 结构还在变（#368 finding #6 #8 对应 Top-5 #4
未启动），等重构稳定后再补各自的 CLAUDE.md，以免写完被下一轮重构覆盖。

## Test plan

- [x] `pnpm lint`（pre-commit hook 已跑）
- [x] 纯文档 + 注释，无代码逻辑变化
- [ ] CI web-quality（eslint config 改动会重新解析 config 文件，验证注释格式正确）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [d01471f](https://github.com/SerendipityOneInc/ecap-workspace/commit/d01471fceff658c2da8266bddd1093d964c681c2) feat(eca-466): prompt restart after feishu/lark channel changes (#766)

**作者**: kaka-srp  
**SHA**: `d01471fceff658c2da8266bddd1093d964c681c2`

```
## Summary

- Adds a reusable `RestartPromptModal` component (extracted from
`AgentSettingsPopover`) and wires it into the feishu/lark flows that now
require a bot restart since the feishu and lark plugins were flipped to
default-disabled in FastClaw.
- Prompts restart after **adding** or **removing** a feishu channel in
Claw Settings (both the QR scan flow and the advanced credential form).
- Prompts restart after **binding** or **unbinding** a feishu/lark
channel on an agent from the Agent Settings popover — reuses the
existing restart modal and pending-restart icon.
- Lifts the Claw-settings restart state up to `ClawSettingsClient` so
that calling `loadSettings()` inside the FeishuSetupModal success
handler doesn't unmount `ChannelsSection` and drop the pending-restart
flag before the modal can render.
- Changes the default `group_policy` from `allowlist` to `open` in both
the backend Pydantic defaults (`AddChannelRequest`,
`FeishuSetupRequest`) and the frontend add-channel form, so new channels
allow group chat out of the box.

Linear:
[ECA-466](https://linear.app/srpone/issue/ECA-466/enable-feishu-plugin-on-demand-and-test-token-changes)

## Test plan

- [ ] Claw Settings → Channels → Add feishu via QR scan → after success,
restart modal appears; "Restart now" calls redeploy, "Later" dismisses.
- [ ] Claw Settings → Channels → Add feishu via advanced
(appId/appSecret) form → restart modal appears after success.
- [ ] Same flow with Lark brand toggle → restart modal appears.
- [ ] Claw Settings → Channels → Remove an existing feishu channel →
restart modal appears.
- [ ] Add channel form: `Group policy` dropdown defaults to `open`.
- [ ] Agent Settings → Channel Bindings → bind a feishu account →
restart modal appears and the popover header's "restart required"
warning icon lights up.
- [ ] Agent Settings → Channel Bindings → unbind a feishu binding →
restart modal appears.
- [ ] Bind/unbind a non-feishu channel (telegram/slack) → **no** restart
modal (regression check).
- [ ] Model change in Agent Settings still triggers the same restart
modal (existing behavior preserved).
```

### [00b2ae0](https://github.com/SerendipityOneInc/ecap-workspace/commit/00b2ae05ade279c98a4dbfc680f3ae60986ed72f) refactor(api): consolidate openclaw_client _short_id into sanitize.safe_short_id (#767)

**作者**: Chris@ZooClaw  
**SHA**: `00b2ae05ade279c98a4dbfc680f3ae60986ed72f`

```
## Summary
- Drop the file-local `_short_id` in `app/services/openclaw_client.py`
- Switch all 40+ call sites to the canonical `safe_short_id` from
`app.services.sanitize`
- Identical truncation behavior; bonus is that `safe_short_id` routes
through a frozen dataclass that breaks CodeQL's
`py/clear-text-logging-sensitive-data` taint chain

This addresses the duplicate `_short_id` discovered while doing #765
(the stripe `_utils` rename). Same pattern, different module —
consolidating to one shared helper instead of letting two
implementations drift.

## Test plan
- [x] `ruff format` + `ruff check` clean
- [x] `pyright app/ tests/` → 0 errors, 0 warnings (verifies no caller
passes a typed `str | None`)
- [x] `pytest tests/unit -k openclaw` → 545 passed
- [ ] CI green

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [15e7e6b](https://github.com/SerendipityOneInc/ecap-workspace/commit/15e7e6b3df6d3a3c1ef0c3302d03665d8e7b7980) refactor(api): make stripe utils module + helpers public (#765)

**作者**: Chris@ZooClaw  
**SHA**: `15e7e6b3df6d3a3c1ef0c3302d03665d8e7b7980`

```
## Summary
- Rename `app/services/stripe/_utils.py` → `utils.py` and the function
`_short_id` → `short_id`
- Rename `subscription_manager._BG_NO_SUBSCRIPTION_STATUSES` →
`BG_NO_SUBSCRIPTION_STATUSES`
- Update all callers in `app/services/stripe/**` plus the BDD step def
`tests/bdd/step_defs/test_stripe_webhook_dispatch.py`

These symbols are imported across modules (see `entitlement.py`,
`handlers/*`, `portal.py`, `order_confirm.py`, `billing_gateway.py`);
using a leading underscore for shared cross-package helpers violates PEP
8 conventions and signals "do not import from outside" — exactly the
opposite of how they're used.

This is the first of a small follow-up series cleaning up leftovers from
the 11-PR Stripe split.

## Test plan
- [x] `ruff format .` → 297 files unchanged
- [x] `ruff check .` → 0 errors (after auto-fixing import ordering)
- [x] `pyright app/ tests/` → 0 errors, 0 warnings
- [x] `pytest tests/unit/test_stripe_*.py
tests/unit/test_subscription_manager.py` → 106 passed
- [x] BDD step defs collect cleanly (skipped here without mongo, will
run in CI)
- [ ] CI green on PR

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [6ccbbc1](https://github.com/SerendipityOneInc/ecap-workspace/commit/6ccbbc1675d1dbe3bb722d1dcfe214e7444f4ea2) fix(eca-464): srp.one gate reads email from JWT, not ecap-account profile (#733)

**作者**: kaka-srp  
**SHA**: `6ccbbc1675d1dbe3bb722d1dcfe214e7444f4ea2`

```
## Summary

The \`_require_srpone\` helper introduced in #714 reads
\`user.profile.email\` from the \`ecap-account\` document, but that
field does not exist on \`ecap-account\` — email lives in the encrypted
\`gem_account\` collection and is only stitched in at request time by
\`enrich_user_with_profile\`, which the settings routes never call.

As a result **every real \`@srp.one\` user was getting 403 from both
\`GET /openclaw/settings/image-version/releases\` and \`POST
/openclaw/settings/image-version\`**. Reported on UID
\`7268822997437874176\` / \`allenz@srp.one\` in staging.

## Fix

Read \`current_user["email"]\` directly — that field is already
populated by \`token_verifier.verify\` from the JWT payload
([app/auth/token_verifier.py:78](services/claw-interface/app/auth/token_verifier.py#L78)).
No extra DB lookup, no CSFLE dependency, no reliance on enrichment.

Also reorder \`set_image_version\` so the gate runs **before**
\`_check_rate_limit\` and \`_get_user_bot_and_token\` — outsiders now
fail fast without consuming a rate-limit slot or touching the DB.

## Why this wasn't caught in tests

The existing tests mocked \`_get_user_bot_and_token\` to return a dict
shaped like \`{"profile": {"email": "user@srp.one"}}\` — so the helper
always saw a populated profile. Real \`ecap-account\` documents have
\`profile: None\`, which we only discovered by querying the actual DB
when allenz@srp.one reported the bug.

Tests have been rewritten to pass \`current_user\` dicts with \`email\`
directly, matching what the JWT dependency actually provides. Added
\`_rejects_empty_email\` / \`_rejects_none_email\` branches.

## Test plan

- [x] Backend tests: \`pytest
tests/unit/test_openclaw_settings_image_version.py\` — 16/16 passing
- [x] Backend type/lint: \`ruff format && ruff check && pyright\` clean
- [x] After merge + staging tag, verify that a non-admin \`@srp.one\`
user (e.g. allenz@srp.one) can load the version dropdown and select a
```

### [80a11b1](https://github.com/SerendipityOneInc/ecap-workspace/commit/80a11b11080c693d13834d0b0818009b1ff5b998) refactor(web): move LandingCTA video URL into landingContent.ts (#764)

**作者**: Chris@ZooClaw  
**SHA**: `80a11b11080c693d13834d0b0818009b1ff5b998`

```
## Summary

`landingContent.ts` 已经是 landing 静态 + i18n 内容的中心（`FEATURES` 的
`img`、`DEEP_FEATURES` 的 `img`、`ALL_MODELS` 等都在里头），唯独 `LandingCTA.tsx`
里一个 CloudFront 视频 URL 被硬编码在 JSX，破坏了 content / markup 分离的一致性。

把它搬到 `landingContent.ts` 作为顶层 `CTA_VIDEO_URL`（不走 i18n，和 `ALL_MODELS`
一档）；子组件只 import 常量，不改动视觉 / 行为。

## 改动

| 文件 | 动作 |
|---|---|
| `landingContent.ts` | +4 行：新增 `export const CTA_VIDEO_URL = '...'`
顶层常量 |
| `components/LandingCTA.tsx` | -10/+4 行：import 常量，`<video src={...}>`
从字面量改引用，同时顺手把多行 JSX 标签收成一行（属性没变） |

净改动 **2 文件、7/7 行**，视觉 / 行为零变化。

## 为什么不放进 `getLandingData(t)` 返回值

视频 URL 与语言无关，和 `ALL_MODELS` 同性质 —— 放顶层 export 更匹配现有分层（`getLandingData`
专门装需要 `t` 的内容）。

## Test plan

- [x] `pnpm exec tsc --noEmit`
- [x] `pnpm lint`
- [ ] 视觉：PR preview / staging 上看最后一个 CTA section 视频照常播放（`autoPlay loop
muted playsInline` 参数保持不变）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [790b837](https://github.com/SerendipityOneInc/ecap-workspace/commit/790b83785bbff6f465b35aee0968ce9bdaa68cdc) test(api): [11/11] billing gateway timeout propagation + spec completion (#763)

**作者**: Chris@ZooClaw  
**SHA**: `790b83785bbff6f465b35aee0968ce9bdaa68cdc`

```
## Summary

Stripe cleanup series **final PR**. Follows #758 (PR 10/11).

Two pieces:

### 1. Fill the one real test coverage gap

\`billing_gateway.topup_wallet\` 抛非 HTTPStatusError 异常（如
\`asyncio.TimeoutError\`）时必须冒泡出 grant 函数，让 webhook route 转成 500 → Stripe
自动 retry。这个路径位于现有两个 test case 之间：
- \`test_topup_404_recovers_and_retries\`（wallet recovery 分支）
- \`test_topup_500_propagates_without_retry\`（generic HTTPStatusError
分支）

Timeout 是裸异常（无 response 对象），之前无直接回归覆盖。+23 行 test。

### 2. 更新 spec 文档反映实际执行

\`docs/superpowers/specs/2026-04-14-stripe-cleanup.md\`:
- Status: Approved → ✅ Completed
- PR-by-PR 实际结果 vs. 原计划（3 个 PR 大幅缩水：#6、#8、#10）
- Follow-up issue 索引（#746 / #747 / #751 / #757 / #761 仍 open）
- 反思段落：为什么 3 个 PR 缩水 + 教训

## 关于 PR 11 scope 大幅缩小

原 plan 预估 ~400 行覆盖 5 个盲区。实际调研后发现 PR 1-10 已经覆盖了 80%：

| 原盲区 | 现状 |
|--------|------|
| 重复事件幂等 | \`test_entitlement_idempotency.py\` 7 cases + BDD 3 invoice
dedup scenarios ✓ |
| 金额边界 | \`test_topup_zero_credits_aborts\` 覆盖 \`<=0\` 整个分支 ✓ |
| 并发 race | \`TestStaleLockRecheck\` 3 cases ✓ |
| Malformed body | \`Invalid payload/signature raises 400\` ✓ |
| **Billing gateway 超时** | **唯一真实盲区** — 本 PR 补 |

## Verification

- [x] \`pyright app/ tests/\`（全仓库）— 0 errors
- [x] \`pytest tests/unit/\` — 2270 passed（2 pre-existing
\`test_skill_injector\` 失败无关）
- [ ] CI

## 统计

2 文件 +62 / -2。

## Stripe cleanup 系列总结

11 PR 全部合并后，stripe 模块从 PR 系列开始时的状态：
- 11 份重复的 \`_short_id\` + 集合常量（PR 1）
- 272 行的 \`handle_checkout_completed\` 巨函数（PR 4）
- 裸 \`except Exception\` 四处吞异常（PR 3）
- \`app.routes.stripe\` 的 re-export 垫片（PR 7）
- \`billing_gateway\` 的 \`user: dict\` 参数重载（PR 9）
- PR 4 留下的 \`# type: ignore\`（PR 10）
- BDD 双胞胎 + invoice_dedup 孤儿（PR 8）

全部清理。详细见 spec 文档的 PR-by-PR 执行状态和反思。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### [a4b0737](https://github.com/SerendipityOneInc/ecap-workspace/commit/a4b073753d5bee88b7c20cd5b9fd4128949cf752) refactor(web): 5 more --landing-* tokens for residual color sweep (#729) (#760)

**作者**: Chris@ZooClaw  
**SHA**: `a4b073753d5bee88b7c20cd5b9fd4128949cf752`

```
## Summary

延续 PR #741 的 token sweep，抽出 **5 个新 `--landing-*` token** 覆盖
`landing.css` 中剩余的高频重复颜色（每个 ≥2 处使用），完成 issue #729 verification 步骤 6。

| Token | 值 | 替换用途 | 次数 |
|---|---|---|---|
| `--landing-text-bright` | `rgba(255,255,255,0.9)` | hover 亮文本 | 3 |
| `--landing-text-active` | `rgba(255,255,255,0.8)` | active / hover 状态
| 3 |
| `--landing-text-dim` | `rgba(245,244,239,0.35)` | muted 标签 | 3 |
| `--landing-border-lighter` | `rgba(245,244,239,0.15)` | soft border |
3 |
| `--landing-bg-opaque` | `rgba(10,10,15,0.96)` | mobile-nav 全屏背板 | 1 |

共替换 **13 处**字面量，视觉零变化（唯一 0.97→0.96 差异视觉不可辨）。

## 刻意保留的字面量

- `rgba(10,10,15,0.95)` 在 line 962 gradient stop（landing 独有淡出效果，提 token
无复用价值）
- `rgba(245,244,239,0.15)` 在 `.specialists-card-animal` `color:`（装饰性
ghost 文本，语义非 border，借用 `--landing-border-lighter` 会误导后续 reader）
- accent tint (`rgba(255,59,48,*)` / `rgba(180,60,200,*)` /
`rgba(255,100,50,*)`)、modal overlay、复合 gradient 里的一次性用法 —— 均为 landing
专属设计，符合 #741 里 "landing-specific 保留" 的原则

## 完成情况与后续

- ✅ 关闭 issue #729 verification 步骤 6（hex 颜色 sweep）
- ✅ 之前 PR 链条: #741 主体迁移 + 14 token / #756 `react/forbid-dom-props` 兜底

## Test plan

- [x] `pnpm exec tsc --noEmit`
- [x] `pnpm lint`
- [x] `pnpm test --run`（2212 passed；唯一 unhandled error 来自
`useGrantCredits.unit.spec.ts` 的跨测试 teardown race，与 CSS 无关，单独跑通过）
- [x] `pnpm build` webpack ✓ Compiled successfully；prerender 失败是
devcontainer 缺 Firebase env，与 CSS 变化无关
- [ ] Staging 视觉回归（承接 #741 test plan 里未勾的那项，合并触发 staging 后逐项对比 hero /
header compact / dropdown / integrations marquee / specialists
scroll-snap / for-experts / mobile sticky CTA / 5 个 section subtitle）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

