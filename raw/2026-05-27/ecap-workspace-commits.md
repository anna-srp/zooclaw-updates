# ecap-workspace Commits - 2026-05-27

共 23 条 commits

---

## feat(billing): add v2 profile summary read path (#1993)

- **SHA**: [5518e4ae](https://github.com/SerendipityOneInc/ecap-workspace/commit/5518e4aea79023ded0eb7e429417bc12da5f20a0)
- **作者**: kaka-srp
- **日期**: 2026-05-27T14:42:05Z
- **PR**: #1993

### Commit Message

```
feat(billing): add v2 profile summary read path (#1993)

## Linear

https://linear.app/srpone/issue/ECA-842/billing-v2-subscription-architecture-refactor

## Summary
- add Billing v2 profile service and sanitized billing summary
projection
- route user and credits read adapters through Billing v2
profile/summary when v2 reads are enabled
- keep flags-off behavior on legacy paths and add audit/failure handling
for wallet repair
- address review follow-ups: v2 summary now derives response
`user_type`, and pre-repair audit failure restores the prior profile
status instead of marking repair failed

## Rollout notes
- `BILLING_V2_READS_ENABLED` and `BILLING_V2_WRITES_ENABLED` still
default to `false`.
- Do not enable the v2 read flag for production traffic before the later
v2 write/backfill/cutover PRs; new signup billing init/trial grant
remains a known intermediate-stage limitation.
- v2 public responses intentionally do not expose raw `team_key` or
wallet ids; admin UI compatibility is a later cutover item.

## Test plan
- [x] cd services/claw-interface && pytest
tests/unit/test_billing_summary_v2.py
tests/unit/test_billing_profiles_v2.py
tests/unit/test_billing_v2_repos.py
tests/unit/test_billing_v2_user_public_response.py
- [x] cd services/claw-interface && pytest
tests/unit/test_billing_profiles_v2.py
tests/unit/test_billing_summary_v2.py
tests/unit/test_billing_v2_user_public_response.py
tests/unit/test_billing_v2_repos.py tests/unit/test_lifetime.py
- [x] cd services/claw-interface && ruff check
app/database/billing_profile_repo.py
app/services/billing_profiles/service.py
app/services/billing_summary/adapters.py
tests/unit/test_billing_profiles_v2.py
tests/unit/test_billing_summary_v2.py
tests/unit/test_billing_v2_repos.py
- [x] cd services/claw-interface && pyright app tests
- [x] cd services/claw-interface && lint-imports --config pyproject.toml
- [x] cd services/claw-interface && scripts/ci-lint/01-file-length.sh
- [ ] cd services/claw-interface && pytest --cov=app
--cov-report=term-missing --cov-fail-under=90 -q (started, stopped at
request; openclaw tests showed unrelated failures before stop)
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-842/billing-v2-subscription-architecture-refactor

## Summary
- add Billing v2 profile service and sanitized billing summary projection
- route user and credits read adapters through Billing v2 profile/summary when v2 reads are enabled
- keep flags-off behavior on legacy paths and add audit/failure handling for wallet repair
- address review follow-ups: v2 summary now derives response `user_type`, and pre-repair audit failure restores the prior profile status instead of marking repair failed

## Rollout notes
- `BILLING_V2_READS_ENABLED` and `BILLING_V2_WRITES_ENABLED` still default to `false`.
- Do not enable the v2 read flag for production traffic before the later v2 write/backfill/cutover PRs; new signup billing init/trial grant remains a known intermediate-stage limitation.
- v2 public responses intentionally do not expose raw `team_key` or wallet ids; admin UI compatibility is a later cutover item.

## Test plan
- [x] cd services/claw-interface && pytest tests/unit/test_billing_summary_v2.py tests/unit/test_billing_profiles_v2.py tests/unit/test_billing_v2_repos.py tests/unit/test_billing_v2_user_public_response.py
- [x] cd services/claw-interface && pytest tests/unit/test_billing_profiles_v2.py tests/unit/test_billing_summary_v2.py tests/unit/test_billing_v2_user_public_response.py tests/unit/test_billing_v2_repos.py tests/unit/test_lifetime.py
- [x] cd services/claw-interface && ruff check app/database/billing_profile_repo.py app/services/billing_profiles/service.py app/services/billing_summary/adapters.py tests/unit/test_billing_profiles_v2.py tests/unit/test_billing_summary_v2.py tests/unit/test_billing_v2_repos.py
- [x] cd services/claw-interface && pyright app tests
- [x] cd services/claw-interface && lint-imports --config pyproject.toml
- [x] cd services/claw-interface && scripts/ci-lint/01-file-length.sh
- [ ] cd services/claw-interface && pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q (started, stopped at request; openclaw tests showed unrelated failures before stop)

---

## feat(billing): add billing v2 foundation (#1991)

- **SHA**: [25439941](https://github.com/SerendipityOneInc/ecap-workspace/commit/25439941e3f99086b8f4a95431f7cd275f40f894)
- **作者**: kaka-srp
- **日期**: 2026-05-27T13:10:10Z
- **PR**: #1991

### Commit Message

```
feat(billing): add billing v2 foundation (#1991)

## Linear
https://linear.app/srpone/issue/ECA-842/billing-v2-subscription-refactor

## Summary
- Add the Billing v2 design spec and PR rollout plan for the
subscription/payment refactor.
- Add Billing v2 schemas, repos, state transition helpers, provider
event idempotency helpers, and audit transition support behind disabled
feature flags.
- Register Billing v2 indexes during backend startup and cover the
foundation with focused unit tests.

## Test plan
- [x] `cd services/claw-interface && pytest tests/unit/test_lifetime.py
tests/unit/test_billing_v2_schema.py tests/unit/test_billing_v2_state.py
tests/unit/test_billing_v2_transitions.py
tests/unit/test_provider_events_v2.py
tests/unit/test_billing_v2_repos.py`
- [x] `cd services/claw-interface && ruff check .`
- [x] `cd services/claw-interface && pyright app tests`
- [x] `cd services/claw-interface && lint-imports --config
pyproject.toml`
- [x] `cd services/claw-interface && ruff format --check
app/database/collections.py app/lifetime.py app/settings.py
app/database/billing_audit_repo.py app/database/billing_profile_repo.py
app/database/entitlement_ledger_repo.py
app/database/payment_order_repo.py app/database/provider_event_repo.py
app/database/subscription_agreement_repo.py app/schema/billing_v2.py
app/services/billing_v2 tests/unit/test_billing_v2_repos.py
tests/unit/test_billing_v2_schema.py tests/unit/test_billing_v2_state.py
tests/unit/test_billing_v2_transitions.py
tests/unit/test_provider_events_v2.py tests/unit/test_lifetime.py`
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-842/billing-v2-subscription-refactor

## Summary
- Add the Billing v2 design spec and PR rollout plan for the subscription/payment refactor.
- Add Billing v2 schemas, repos, state transition helpers, provider event idempotency helpers, and audit transition support behind disabled feature flags.
- Register Billing v2 indexes during backend startup and cover the foundation with focused unit tests.

## Test plan
- [x] `cd services/claw-interface && pytest tests/unit/test_lifetime.py tests/unit/test_billing_v2_schema.py tests/unit/test_billing_v2_state.py tests/unit/test_billing_v2_transitions.py tests/unit/test_provider_events_v2.py tests/unit/test_billing_v2_repos.py`
- [x] `cd services/claw-interface && ruff check .`
- [x] `cd services/claw-interface && pyright app tests`
- [x] `cd services/claw-interface && lint-imports --config pyproject.toml`
- [x] `cd services/claw-interface && ruff format --check app/database/collections.py app/lifetime.py app/settings.py app/database/billing_audit_repo.py app/database/billing_profile_repo.py app/database/entitlement_ledger_repo.py app/database/payment_order_repo.py app/database/provider_event_repo.py app/database/subscription_agreement_repo.py app/schema/billing_v2.py app/services/billing_v2 tests/unit/test_billing_v2_repos.py tests/unit/test_billing_v2_schema.py tests/unit/test_billing_v2_state.py tests/unit/test_billing_v2_transitions.py tests/unit/test_provider_events_v2.py tests/unit/test_lifetime.py`


---

## chore(web): persistQueryClient eval + A4 characterization (#1988)

- **SHA**: [43ad090a](https://github.com/SerendipityOneInc/ecap-workspace/commit/43ad090ac600b331ce722b63af4f39985732f133)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-27T12:11:40Z
- **PR**: #1988

### Commit Message

```
chore(web): persistQueryClient eval + A4 characterization (#1988)

## Summary

Phase 0 + 评估 spec doc for #1868 (评估
`@tanstack/react-query-persist-client` 替换 ~12 个手维护
sessionStorage/localStorage 缓存层)。本 PR **不动任何生产代码**,只为后续 PR-2 prototype
打地基。

- **spec**:
`docs/superpowers/specs/2026-05-27-rq-persist-client-evaluation.md` ——
10 节评估,含 **Tier A queryKey×token 审计**(发现 ~67% 工作量不依赖 #1309 即可推进)+ **测试覆盖
gap audit**(逐 Bucket)
- **characterization tests**:
`tests/unit/lib/agent-catalog-cache.unit.spec.ts` —— 15 条断言锁住
`agent-catalog-cache.ts` 当前所有 write/read/lookup 行为(write 是 raw array 无
envelope、dispatchEvent 是 plain Event 无 detail、setItem 失败时跳过
dispatchEvent、`||` truthy 回退链)
- **setup hygiene**: `vitest.setup.ts` 加全局 `beforeEach(() =>
storage.clear())`,后续 storage 改造期间所有 spec 受益

## 路线图(本 PR 之后)

| PR | Scope | 状态 |
|---|---|---|
| **本 PR** | spec + Phase 0 PR-1 | open |
| PR-2 | Bucket-1 prototype(A4 删除 + 接入 `PersistQueryClientProvider`) | 本
PR merge 后启动 |
| follow-up issues | Bucket-2/3/4 + B1 audit + CLAUDE.md 章节 + ESLint 规则
| PR-2 merge 后手开 |

## Test plan

- [x] `pnpm test:unit` —— 全 6024 测试绿(新加 15 条 + setup 改动不破坏现有 spec)
- [x] `pnpm lint` —— 无 warning/error
- [x] `npx tsc --noEmit` —— 全仓 type-check 干净
- [x] 新 characterization spec 单独跑:15/15 passed(pinning current behavior)
- [x] 验证 setup hygiene 对 partial-mock
storage(mattermost/auth.unit.spec.ts) + node-env(stripe API routes /
query-client / css)两类边角 case 都能容忍

## Notes for reviewer

- 评估 doc 第 4 节(queryKey×token 审计)是本 PR 最关键的产物,直接定 #1309 阻塞边界
- characterization 测试设计原则: snapshot post-fix 后正确行为,**不是 pre-fix
bug**(若发现遗留 bug 另开 issue)
- vitest.setup.ts 用 `typeof X !== 'undefined'` 双重 guard 而非 `?.`——后者会在
node-env 下 throw ReferenceError(已在 stripe/css spec 验证)
- 不要 auto-merge —— PR-2 依赖本 PR merged 才能写

Refs #1868

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Phase 0 + 评估 spec doc for #1868 (评估 `@tanstack/react-query-persist-client` 替换 ~12 个手维护 sessionStorage/localStorage 缓存层)。本 PR **不动任何生产代码**,只为后续 PR-2 prototype 打地基。

- **spec**: `docs/superpowers/specs/2026-05-27-rq-persist-client-evaluation.md` —— 10 节评估,含 **Tier A queryKey×token 审计**(发现 ~67% 工作量不依赖 #1309 即可推进)+ **测试覆盖 gap audit**(逐 Bucket)
- **characterization tests**: `tests/unit/lib/agent-catalog-cache.unit.spec.ts` —— 15 条断言锁住 `agent-catalog-cache.ts` 当前所有 write/read/lookup 行为(write 是 raw array 无 envelope、dispatchEvent 是 plain Event 无 detail、setItem 失败时跳过 dispatchEvent、`||` truthy 回退链)
- **setup hygiene**: `vitest.setup.ts` 加全局 `beforeEach(() => storage.clear())`,后续 storage 改造期间所有 spec 受益

## 路线图(本 PR 之后)

| PR | Scope | 状态 |
|---|---|---|
| **本 PR** | spec + Phase 0 PR-1 | open |
| PR-2 | Bucket-1 prototype(A4 删除 + 接入 `PersistQueryClientProvider`) | 本 PR merge 后启动 |
| follow-up issues | Bucket-2/3/4 + B1 audit + CLAUDE.md 章节 + ESLint 规则 | PR-2 merge 后手开 |

## Test plan

- [x] `pnpm test:unit` —— 全 6024 测试绿(新加 15 条 + setup 改动不破坏现有 spec)
- [x] `pnpm lint` —— 无 warning/error
- [x] `npx tsc --noEmit` —— 全仓 type-check 干净
- [x] 新 characterization spec 单独跑:15/15 passed(pinning current behavior)
- [x] 验证 setup hygiene 对 partial-mock storage(mattermost/auth.unit.spec.ts) + node-env(stripe API routes / query-client / css)两类边角 case 都能容忍

## Notes for reviewer

- 评估 doc 第 4 节(queryKey×token 审计)是本 PR 最关键的产物,直接定 #1309 阻塞边界
- characterization 测试设计原则: snapshot post-fix 后正确行为,**不是 pre-fix bug**(若发现遗留 bug 另开 issue)
- vitest.setup.ts 用 `typeof X !== 'undefined'` 双重 guard 而非 `?.`——后者会在 node-env 下 throw ReferenceError(已在 stripe/css spec 验证)
- 不要 auto-merge —— PR-2 依赖本 PR merged 才能写

Refs #1868

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(web): AgentsManagerClient modal state to discriminated union (#1976) (#1981)

- **SHA**: [547ccde9](https://github.com/SerendipityOneInc/ecap-workspace/commit/547ccde9d0a25cc86b855f1656f38481b38abd78)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-27T10:35:04Z
- **PR**: #1976

### Commit Message

```
refactor(web): AgentsManagerClient modal state to discriminated union (#1976) (#1981)

## Summary

Audit follow-up from PR #1974. Collapse 8 independent `useState<X |
null>` modal flags in `AgentsManagerClient.tsx` into one `ModalState`
discriminated union. Mutual exclusivity ("only one modal/menu open at a
time") is now a type-level invariant rather than a documentation
promise.

- `handleKeyDown` `useCallback` deps: **8 → 2** (`modal.type`,
`updateSuccessLockedAgentId`). The keydown listener stops re-attaching
on every individual flag change — only on actual modal-open/close
transitions.
- `fireConfirmInput` (which only had meaning while the fire-confirm
modal was open) folded into the `confirmFire` variant.
- 2 new tests:
- hire → success → Escape transition (mutual exclusion verified at
render-time, not just type-time)
- Escape blocked while `/new` reset is in flight (preserves the
"Starting…" affordance during async reset)

## Why

Per the issue body: every modal open/close re-creates the callback and
re-attaches the keydown listener — wasteful event-listener churn that
also makes debugging harder. The 8-deep `else if` cascade in the old
Escape handler had no enforced mutual-exclusion invariant (could in
principle have two modals open simultaneously due to a setter-ordering
bug).

## Modal state shape

```ts
type ModalState =
  | { type: 'none' }
  | { type: 'menu'; agentId: string }
  | { type: 'confirmHire'; agent: ModalAgent }
  | { type: 'hireSuccess'; agent: ModalAgent }
  | { type: 'confirmFire'; agent: ModalAgent; fireInput: string }
  | { type: 'fireSuccess'; agent: ModalAgent }
  | { type: 'confirmUpdate'; agent: ModalAgent }
  | { type: 'updateSuccess'; agent: ModalAgent }
```

## Test plan
- [x] `pnpm test:unit -- agents-manager` — 105 tests pass (4
pre-existing + 2 new + 99 other)
- [x] `npx tsc --noEmit` (web/app) — clean
- [x] `pnpm lint` — clean (1 pre-existing warning, not in touched code)
- [x] `pnpm dup` (src + tests) — within thresholds (src 3.71%, tests
5.98%)
- [ ] Manual smoke (staging): hire → confirm → success modal; menu →
fire → typing FIRE → confirm; update → success → /new (verify reset
persists modal open)

Closes #1976.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

Audit follow-up from PR #1974 (OpenClawProvider周边代码 React 反模式审计).

## Background

`web/app/src/app/[locale]/agents-manager/AgentsManagerClient.tsx` lines 199-225 currently has a `useCallback(handleKeyDown, [...])` with **8 separate modal state dependencies**:

```tsx
const handleKeyDown = useCallback(
  (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      if (menuAgentId) setMenuAgentId(null)
      else if (updateConfirmAgent) setUpdateConfirmAgent(null)
      else if (successAgent) setSuccessAgent(null)
      else if (confirmAgent) setConfirmAgent(null)
      else if (fireConfirmAgent) setFireConfirmAgent(null)
      else if (firedAgent) setFiredAgent(null)
      else if (updatedAgent) setUpdatedAgent(null)
      else if (resettingAgentId) setResettingAgentId(null)
    }
  },
  [
    menuAgentId,
    updateConfirmAgent,
    confirmAgent,
    successAgent,
    fireConfirmAgent,
    firedAgent,
    updatedAgent,
    resettingAgentId,
  ],
)
```

Plus the corresponding `addEventListener` / `removeEventListener` effect (lines 222-225) that re-attaches on every dep change.

Every modal open/close re-creates the callback and re-attaches the keydown listener — wasteful event-listener churn that also makes debugging harder.

## Goal

Replace the 8 separate `useState` calls with a single discriminated union:

```ts
type ModalState =
  | { type: 'none' }
  | { type: 'menu'; agentId: string }
  | { type: 'updateConfirm'; agent: Agent }
  | { type: 'updated'; agent: Agent }
  | { type: 'confirm'; agent: Agent }
  | { type: 'success'; agent: Agent }
  | { type: 'fireConfirm'; agent: Agent }
  | { type: 'fired'; agent: Agent }
  | { type: 'resetting'; agentId: string }

const [modal, setModal] = useState<ModalState>({ type: 'none' })
```

After the change:
- Escape handler reads `modal.type` and dispatches a single `setModal({ type: 'none' })`.
- `useCallback` dependency drops from 8 to 1 (just `modal.type`).
- Listener re-attachment happens at most once per modal type transition, not per individual state setter.
- Mutual exclusivity (can't have two modals open at once) becomes a type-level invariant.

## Acceptance

- [ ] All 8 modal `useState` calls collapsed to one `ModalState` reducer/state.
- [ ] `useCallback` deps reduced to ≤2.
- [ ] No behavioral regression — existing modal tests in the file pass.
- [ ] At least one new test asserting "can't have two modals open simultaneously" via the type system (or runtime assertion).

## Out of scope

- Other modal-heavy components (`PublishingDialog`, etc.) — open separate issues if found similar.
- Refactoring modal *content* — only state management.

## Reference

- PR #1974 audit plan: `/home/node/.claude/plans/fix-issue-1959-snappy-dragonfly.md` (finding #6)

---

## fix(claw-interface): allow main agent to spawn subagents (#1978)

- **SHA**: [17f14df9](https://github.com/SerendipityOneInc/ecap-workspace/commit/17f14df94ce6847e5762fb32bbf69ad03ebcb65e)
- **作者**: tim-srp
- **日期**: 2026-05-27T10:11:12Z
- **PR**: #1978

### Commit Message

```
fix(claw-interface): allow main agent to spawn subagents (#1978)

## Summary
- Add default subagent allowlist config to the main agent during
agents.list sync.
- Keep existing specialist agent allowAgents behavior unchanged.
- Cover the generated main agent config in unit tests.

## Behavior
When claw-interface writes agents.list for selected team agents, the
main agent now gets subagents.allowAgents set to ["*"].

This makes future bot syncs and new bot configs allow Main to spawn
installed team agents by default. Non-main agents already had the same
allowAgents setting and continue to keep it.

## Testing
- pytest -W "ignore:Please use import python_multipart
instead.:PendingDeprecationWarning"
tests/unit/test_openclaw_agents.py::TestApplyAgentsList
- ruff check app/services/openclaw/agent_deploy.py
tests/unit/test_openclaw_agents.py

## Notes
- pyright app/services/openclaw/agent_deploy.py
tests/unit/test_openclaw_agents.py could not run cleanly in my local
environment because pyright could not resolve local test dependencies
pytest and fastapi.
```

### PR Description

## Summary
- Add default subagent allowlist config to the main agent during agents.list sync.
- Keep existing specialist agent allowAgents behavior unchanged.
- Cover the generated main agent config in unit tests.

## Behavior
When claw-interface writes agents.list for selected team agents, the main agent now gets subagents.allowAgents set to ["*"].

This makes future bot syncs and new bot configs allow Main to spawn installed team agents by default. Non-main agents already had the same allowAgents setting and continue to keep it.

## Testing
- pytest -W "ignore:Please use import python_multipart instead.:PendingDeprecationWarning" tests/unit/test_openclaw_agents.py::TestApplyAgentsList
- ruff check app/services/openclaw/agent_deploy.py tests/unit/test_openclaw_agents.py

## Notes
- pyright app/services/openclaw/agent_deploy.py tests/unit/test_openclaw_agents.py could not run cleanly in my local environment because pyright could not resolve local test dependencies pytest and fastapi.


---

## feat(settings): add data compliance permissions (#1980)

- **SHA**: [6df680bd](https://github.com/SerendipityOneInc/ecap-workspace/commit/6df680bda6e385518e82566a6e633ae02a149d8b)
- **作者**: bill-srp
- **日期**: 2026-05-27T09:59:55Z
- **PR**: #1980

### Commit Message

```
feat(settings): add data compliance permissions (#1980)

## Linear

https://linear.app/srpone/issue/ECA-839/zooclaw%E6%B3%A8%E5%86%8C%E9%A1%B5%E9%9D%A2%E5%A2%9E%E5%8A%A0%E6%95%B0%E6%8D%AE%E5%90%88%E8%A7%84%E7%A1%AE%E8%AE%A4%E5%BC%B9%E7%AA%97

## Summary
- Add settings data compliance permission rows with persisted checkbox
preferences
- Add the user-facing preferences update API route
- Preserve sequential consent updates by saving the full data compliance
consent snapshot each time
- Align web/app backend configuration on CLAW_INTERFACE_URL while
allowing deploy to source it from existing BACKEND_URL vars until
external config is renamed

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web run test:unit
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/components/settings/GeneralTab.unit.spec.tsx
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/packages/auth-client exec tsc --noEmit
- [ ] pnpm --dir web run tsc (blocked locally: script passes unsupported
--if-present to pnpm exec)
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-839/zooclaw%E6%B3%A8%E5%86%8C%E9%A1%B5%E9%9D%A2%E5%A2%9E%E5%8A%A0%E6%95%B0%E6%8D%AE%E5%90%88%E8%A7%84%E7%A1%AE%E8%AE%A4%E5%BC%B9%E7%AA%97

## Summary
- Add settings data compliance permission rows with persisted checkbox preferences
- Add the user-facing preferences update API route
- Preserve sequential consent updates by saving the full data compliance consent snapshot each time
- Align web/app backend configuration on CLAW_INTERFACE_URL while allowing deploy to source it from existing BACKEND_URL vars until external config is renamed

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web run test:unit
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/components/settings/GeneralTab.unit.spec.tsx
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/packages/auth-client exec tsc --noEmit
- [ ] pnpm --dir web run tsc (blocked locally: script passes unsupported --if-present to pnpm exec)

---

## refactor(claw-interface): add agent workspace write path (#1979)

- **SHA**: [c3dba66d](https://github.com/SerendipityOneInc/ecap-workspace/commit/c3dba66d89a0a360572195b5fe7390a4e6cc299c)
- **作者**: bill-srp
- **日期**: 2026-05-27T09:59:00Z
- **PR**: #1979

### Commit Message

```
refactor(claw-interface): add agent workspace write path (#1979)

## Summary
- add normalized agent workspace create/update service and repository
write paths
- add tests for scoped writes and public response token omission
- preserve explicit nulls in agent workspace updates so nullable fields
can be cleared

## Test plan
- [x] `docker exec service-agents-bill bash -lc 'cd
/workspaces/service-agents/services/claw-interface && source
/home/node/.venvs/claw-interface/bin/activate && pytest
tests/unit/test_agent_service.py tests/unit/test_agent_workspace_repo.py
-q'`
- [x] `docker exec service-agents-bill bash -lc 'cd
/workspaces/service-agents/services/claw-interface && source
/home/node/.venvs/claw-interface/bin/activate && ruff check .'`
- [x] `docker exec service-agents-bill bash -lc 'cd
/workspaces/service-agents/services/claw-interface && source
/home/node/.venvs/claw-interface/bin/activate && pyright app tests'`

## Notes
- Full backend coverage run was attempted in the devcontainer, but it
hit existing `test_ci_lint_deptry` failures outside this branch and was
stopped after the failure was observed.
```

### PR Description

## Summary
- add normalized agent workspace create/update service and repository write paths
- add tests for scoped writes and public response token omission
- preserve explicit nulls in agent workspace updates so nullable fields can be cleared

## Test plan
- [x] `docker exec service-agents-bill bash -lc 'cd /workspaces/service-agents/services/claw-interface && source /home/node/.venvs/claw-interface/bin/activate && pytest tests/unit/test_agent_service.py tests/unit/test_agent_workspace_repo.py -q'`
- [x] `docker exec service-agents-bill bash -lc 'cd /workspaces/service-agents/services/claw-interface && source /home/node/.venvs/claw-interface/bin/activate && ruff check .'`
- [x] `docker exec service-agents-bill bash -lc 'cd /workspaces/service-agents/services/claw-interface && source /home/node/.venvs/claw-interface/bin/activate && pyright app tests'`

## Notes
- Full backend coverage run was attempted in the devcontainer, but it hit existing `test_ci_lint_deptry` failures outside this branch and was stopped after the failure was observed.


---

## fix(web): add chat render recovery diagnostics (#1985)

- **SHA**: [0fa02461](https://github.com/SerendipityOneInc/ecap-workspace/commit/0fa024611ff2e9d3872138dc054f92f5549eba3e)
- **作者**: sam-srp
- **日期**: 2026-05-27T09:39:24Z
- **PR**: #1985

### Commit Message

```
fix(web): add chat render recovery diagnostics (#1985)

## Summary

Adds extra diagnostic context to chat render recovery reports in Sentry.

## Why

Sentry issue `7452503385` shows a React maximum update depth error on
`/chat`, but the current production release lacks source maps. The
existing render recovery event captures the error, but does not include
enough runtime context to confirm whether the crash is tied to the chat
header tooltip/button path or to a mobile pointer environment.

## Changes

- Preserve the component stack in the render recovery payload.
- Add booleans for maximum update depth errors and header action stack
matches.
- Include viewport size, pointer/hover media query results, and user
agent.

## Validation

- Ran `git diff --check`.
- Did not run the app test suite; project instructions say not to run
tests unless explicitly requested.
```

### PR Description

## Summary

Adds extra diagnostic context to chat render recovery reports in Sentry.

## Why

Sentry issue `7452503385` shows a React maximum update depth error on `/chat`, but the current production release lacks source maps. The existing render recovery event captures the error, but does not include enough runtime context to confirm whether the crash is tied to the chat header tooltip/button path or to a mobile pointer environment.

## Changes

- Preserve the component stack in the render recovery payload.
- Add booleans for maximum update depth errors and header action stack matches.
- Include viewport size, pointer/hover media query results, and user agent.

## Validation

- Ran `git diff --check`.
- Did not run the app test suite; project instructions say not to run tests unless explicitly requested.


---

## fix(claw-settings): validate channel account ids (#1982)

- **SHA**: [566e72dd](https://github.com/SerendipityOneInc/ecap-workspace/commit/566e72dddb6b4d874119ee86502f76764bab3baa)
- **作者**: kaka-srp
- **日期**: 2026-05-27T09:35:17Z
- **PR**: #1982

### Commit Message

```
fix(claw-settings): validate channel account ids (#1982)

## Linear
https://linear.app/srpone/issue/ECA-830/add-channel-account-name

## Summary
- Validate channel account IDs consistently in backend channel settings
flows
- Show Account ID input guidance and inline validation in channel setup
UI
- Surface invalid stored account IDs while allowing legacy channels and
bindings to be removed

## Root cause
Channel account IDs were accepted without clear user guidance or strict
validation, so invalid values could be saved and later fail or collide
with runtime account key behavior.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/packages/auth-client exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [x] /home/node/.venvs/claw-interface/bin/ruff check .
- [x] /home/node/.venvs/claw-interface/bin/pyright app tests
- [x] /home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_openclaw_settings_routes.py::TestRemoveChannelEndpoint::test_legacy_invalid_account_binding_cleanup_after_remove
tests/unit/test_openclaw_settings_routes.py::TestRemoveChannelEndpoint::test_weixin_remove_clears_normalized_account_binding
tests/unit/test_openclaw_settings_routes.py::TestRemoveChannelEndpoint::test_valid_platform_names_accepted
tests/unit/test_openclaw_settings_coverage.py::TestUpdateChannel::test_happy_path
tests/unit/test_openclaw_settings_coverage.py::TestUpdateChannel::test_client_error_returns_500
-q
- [ ] Full local backend coverage run was attempted, but this
devcontainer produced unrelated baseline/environment failures outside
this PR; GitHub CI is the authoritative coverage check
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-830/add-channel-account-name

## Summary
- Validate channel account IDs consistently in backend channel settings flows
- Show Account ID input guidance and inline validation in channel setup UI
- Surface invalid stored account IDs while allowing legacy channels and bindings to be removed

## Root cause
Channel account IDs were accepted without clear user guidance or strict validation, so invalid values could be saved and later fail or collide with runtime account key behavior.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/packages/auth-client exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [x] /home/node/.venvs/claw-interface/bin/ruff check .
- [x] /home/node/.venvs/claw-interface/bin/pyright app tests
- [x] /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_openclaw_settings_routes.py::TestRemoveChannelEndpoint::test_legacy_invalid_account_binding_cleanup_after_remove tests/unit/test_openclaw_settings_routes.py::TestRemoveChannelEndpoint::test_weixin_remove_clears_normalized_account_binding tests/unit/test_openclaw_settings_routes.py::TestRemoveChannelEndpoint::test_valid_platform_names_accepted tests/unit/test_openclaw_settings_coverage.py::TestUpdateChannel::test_happy_path tests/unit/test_openclaw_settings_coverage.py::TestUpdateChannel::test_client_error_returns_500 -q
- [ ] Full local backend coverage run was attempted, but this devcontainer produced unrelated baseline/environment failures outside this PR; GitHub CI is the authoritative coverage check


---

## fix(web): rename "Link" to "Code" in custom agent upload dialog (#1983)

- **SHA**: [2ffed1da](https://github.com/SerendipityOneInc/ecap-workspace/commit/2ffed1da907ec1c7fd7824e2f1aeee6397843872)
- **作者**: tim-srp
- **日期**: 2026-05-27T09:16:11Z
- **PR**: #1983

### Commit Message

```
fix(web): rename "Link" to "Code" in custom agent upload dialog (#1983)

## Summary
- Rename "Link" label to "Code" in the Upload Custom Agent dialog
- The remote path type accepts a base64-encoded URL (a code), not a raw
link — the label was misleading

## Changes
- `PublishCreateModal.tsx`: Tab button "Link" → "Code", input label
"Link *" → "Code *"
- `PublishDetailModal.tsx`: Detail view label "Link" → "Code"

## Test plan
- [ ] Open Upload Custom Agent dialog, select remote type — tab shows
"Code", field label shows "Code *"
- [ ] View detail of an existing remote custom agent — label shows
"Code"

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
- Rename "Link" label to "Code" in the Upload Custom Agent dialog
- The remote path type accepts a base64-encoded URL (a code), not a raw link — the label was misleading

## Changes
- `PublishCreateModal.tsx`: Tab button "Link" → "Code", input label "Link *" → "Code *"
- `PublishDetailModal.tsx`: Detail view label "Link" → "Code"

## Test plan
- [ ] Open Upload Custom Agent dialog, select remote type — tab shows "Code", field label shows "Code *"
- [ ] View detail of an existing remote custom agent — label shows "Code"

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(billing): prevent reconciliation drift regressions (#1973)

- **SHA**: [fc2c7697](https://github.com/SerendipityOneInc/ecap-workspace/commit/fc2c76970d4dea62a54865b3533511926865becf)
- **作者**: kaka-srp
- **日期**: 2026-05-27T08:50:48Z
- **PR**: #1973

### Commit Message

```
fix(billing): prevent reconciliation drift regressions (#1973)

## Summary
- Prevent implicit billing init from creating BG subscriptions for
expired/canceled users.
- Clean stale Stripe ownership fields on expiry and terminal
subscription-code recovery.
- Make Stripe reconcile treat a dead Stripe sub older than current local
entitlement as residual cleanup instead of expiring the user.
- Migrate only remaining legacy purchased credits into BG topup wallets.

## Root cause
Expired/canceled Mongo users could still pass through normal billing
init, which preserved the terminal Mongo status but created an active BG
subscription and wallets. Separately, stale Stripe fields could survive
terminal transitions or code redemption, so reconcile write mode could
target the wrong owner/state.

Linear:
https://linear.app/srpone/issue/ECA-838/fix-billing-reconciliation-drift

## Test plan
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check app tests`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_invite_codes.py::TestCreateUserPublicResponse::test_create_user_response_omits_team_key
tests/unit/test_stripe_entitlement_service.py::TestProductDispatch::test_subscription_recovery_syncs_bot_credentials_when_billing_key_is_created
tests/unit/test_stripe_entitlement_service.py::TestProductDispatch::test_subscription_existing_billing_key_syncs_bot_credentials_when_marker_set
tests/unit/test_user_billing.py tests/unit/test_subscription_manager.py
tests/unit/test_subscription_code.py tests/unit/test_stripe_reconcile.py
tests/unit/test_bg_reconcile.py`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m py_compile
app/cron/stripe_reconcile.py app/services/antom/subscription_trials.py
app/services/billing.py app/services/stripe/billing_gateway.py
app/services/stripe/entitlement.py
app/services/stripe/handlers/checkout.py
app/services/subscription_code.py app/services/subscription_manager.py`
- [x] `git diff --check`
- [x] Real read-only scan with local `.env`: Stripe scanned=26,
status_drift=0, failed=0; BG scanned=7, bg_orphan=3, failed=0.
- [x] Actual-case dry-run: real expired Mongo user returned unchanged
without touching BG; real BG orphan write-mode path would terminate 3
actual subscriptions with termination faked.
- [ ] `pyright app tests` not run locally: pyright is not installed in
`/home/node/.venvs/claw-interface`.
- [ ] Full pytest not rerun against local root `.env`: that environment
is non-hermetic and makes real OpenClaw/Mattermost/Redis calls.
```

### PR Description

## Summary
- Prevent implicit billing init from creating BG subscriptions for expired/canceled users.
- Clean stale Stripe ownership fields on expiry and terminal subscription-code recovery.
- Make Stripe reconcile treat a dead Stripe sub older than current local entitlement as residual cleanup instead of expiring the user.
- Migrate only remaining legacy purchased credits into BG topup wallets.

## Root cause
Expired/canceled Mongo users could still pass through normal billing init, which preserved the terminal Mongo status but created an active BG subscription and wallets. Separately, stale Stripe fields could survive terminal transitions or code redemption, so reconcile write mode could target the wrong owner/state.

Linear: https://linear.app/srpone/issue/ECA-838/fix-billing-reconciliation-drift

## Test plan
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check app tests`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_invite_codes.py::TestCreateUserPublicResponse::test_create_user_response_omits_team_key tests/unit/test_stripe_entitlement_service.py::TestProductDispatch::test_subscription_recovery_syncs_bot_credentials_when_billing_key_is_created tests/unit/test_stripe_entitlement_service.py::TestProductDispatch::test_subscription_existing_billing_key_syncs_bot_credentials_when_marker_set tests/unit/test_user_billing.py tests/unit/test_subscription_manager.py tests/unit/test_subscription_code.py tests/unit/test_stripe_reconcile.py tests/unit/test_bg_reconcile.py`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m py_compile app/cron/stripe_reconcile.py app/services/antom/subscription_trials.py app/services/billing.py app/services/stripe/billing_gateway.py app/services/stripe/entitlement.py app/services/stripe/handlers/checkout.py app/services/subscription_code.py app/services/subscription_manager.py`
- [x] `git diff --check`
- [x] Real read-only scan with local `.env`: Stripe scanned=26, status_drift=0, failed=0; BG scanned=7, bg_orphan=3, failed=0.
- [x] Actual-case dry-run: real expired Mongo user returned unchanged without touching BG; real BG orphan write-mode path would terminate 3 actual subscriptions with termination faked.
- [ ] `pyright app tests` not run locally: pyright is not installed in `/home/node/.venvs/claw-interface`.
- [ ] Full pytest not rerun against local root `.env`: that environment is non-hermetic and makes real OpenClaw/Mattermost/Redis calls.


---

## fix(web): tighten OpenClawProvider consumer/callee corners around stale closures and silent failures (#1974)

- **SHA**: [0318bb11](https://github.com/SerendipityOneInc/ecap-workspace/commit/0318bb11eb15e0e25f4d4785fcf26987fa7c62a0)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-27T08:29:59Z
- **PR**: #1974

### Commit Message

```
fix(web): tighten OpenClawProvider consumer/callee corners around stale closures and silent failures (#1974)

## Summary

Audit follow-up to PR #1970 (#1959 OpenClawProvider reducer refactor).
Provider本体 + sub-hooks + reducer 都已干净;本 PR 收 4 个周边代码 audit 出来的 quick
wins。

### 1. `useOpenClawInit` auto-retry stale uid guard (HIGH — real bug)

`web/app/src/hooks/useOpenClawInit.ts:275-282`

The 1s `setTimeout` that retries `doInit(targetUid)` on auth errors
captured a stale `targetUid`. If a user logged out and re-logged in as a
different user within that 1s window, the pending retry fired `doInit`
against the old uid. Fix: gate the retry on `uidRef.current ===
targetUid`; when the uid drifted, let the regular auto-init `useEffect`
handle the new uid.

### 2. `FeedbackDialog` derived state during render (HIGH — UX race)

`web/app/src/components/feedback/FeedbackDialog.tsx:46-64`

A new `crashInfo` reset the dialog state via `useEffect`, leaving one
render where the dialog showed stale messages between mount and effect
flush — race window for user clicks during crash arrival. Switched to
React's
[recommended](https://react.dev/learn/you-might-not-need-an-effect#adjusting-some-state-when-a-prop-changes)
"store previous prop in state + compare during render" pattern so reset
is atomic with the render that observes the new crash. Also extracted
`buildCrashGreeting` / `buildGreeting` helpers to dedupe inline message
construction (saves ~25 lines).

### 3. `RestartPromptModal` silent redeploy failure (MED — silent bug)

`web/app/src/components/RestartPromptModal.tsx:21-35`

`await openClaw.redeploy()` inside `try/finally` swallowed rejections —
modal closed showing "done" even when the restart actually failed. Added
a catch clause that surfaces an error toast via `showToast(...,
'error')` and keeps the modal open so the user can retry.

### 4. `ArchivedSessionPanel` discarded `useOpenClaw()` call (MED —
cleanup)

`web/app/src/app/[locale]/session-history/ArchivedSessionPanel.tsx:110`

The archive page called `useOpenClaw()` purely for the implicit
activation side-effect with no use of the return value — wasted a
WebSocket connection while the user browsed past sessions. Dropped the
call; activation fires naturally when the user navigates back to
`/chat`.

## Test plan

- [x] `pnpm test:unit` — 5974 tests pass (+ 1 todo). New regression
tests:
- `useOpenClawInit-extras.unit.spec.ts`: auth-error auto-retry happy
path + uid-swap-mid-retry guard
- `FeedbackDialog.unit.spec.tsx`: null→crash atomic transition +
crash→new-crash full reset
- `RestartPromptModal.unit.spec.tsx`: 7 cases including the
silent-failure regression
- [x] `pnpm lint` clean
- [x] `./node_modules/.bin/tsc --noEmit` clean
- [x] `pnpm dup` under threshold (tests 5.93%, src 3.68%)
- [ ] Manual: trigger a crash → verify dialog shows crash content
without flicker
- [ ] Manual: mock backend 500 on redeploy → verify error toast surfaces

## Out of scope (登记 follow-up issue)

Two larger refactor opportunities were identified in the audit but
deferred:
- `useOpenClawInit` 4 sentinel refs → reducer (#1959 同款模板，单独 issue)
- `AgentsManagerClient` modal state → discriminated union (减少
useCallback dep churn，单独 issue)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Description

## Summary

Audit follow-up to PR #1970 (#1959 OpenClawProvider reducer refactor). Provider本体 + sub-hooks + reducer 都已干净;本 PR 收 4 个周边代码 audit 出来的 quick wins。

### 1. `useOpenClawInit` auto-retry stale uid guard (HIGH — real bug)

`web/app/src/hooks/useOpenClawInit.ts:275-282`

The 1s `setTimeout` that retries `doInit(targetUid)` on auth errors captured a stale `targetUid`. If a user logged out and re-logged in as a different user within that 1s window, the pending retry fired `doInit` against the old uid. Fix: gate the retry on `uidRef.current === targetUid`; when the uid drifted, let the regular auto-init `useEffect` handle the new uid.

### 2. `FeedbackDialog` derived state during render (HIGH — UX race)

`web/app/src/components/feedback/FeedbackDialog.tsx:46-64`

A new `crashInfo` reset the dialog state via `useEffect`, leaving one render where the dialog showed stale messages between mount and effect flush — race window for user clicks during crash arrival. Switched to React's [recommended](https://react.dev/learn/you-might-not-need-an-effect#adjusting-some-state-when-a-prop-changes) "store previous prop in state + compare during render" pattern so reset is atomic with the render that observes the new crash. Also extracted `buildCrashGreeting` / `buildGreeting` helpers to dedupe inline message construction (saves ~25 lines).

### 3. `RestartPromptModal` silent redeploy failure (MED — silent bug)

`web/app/src/components/RestartPromptModal.tsx:21-35`

`await openClaw.redeploy()` inside `try/finally` swallowed rejections — modal closed showing "done" even when the restart actually failed. Added a catch clause that surfaces an error toast via `showToast(..., 'error')` and keeps the modal open so the user can retry.

### 4. `ArchivedSessionPanel` discarded `useOpenClaw()` call (MED — cleanup)

`web/app/src/app/[locale]/session-history/ArchivedSessionPanel.tsx:110`

The archive page called `useOpenClaw()` purely for the implicit activation side-effect with no use of the return value — wasted a WebSocket connection while the user browsed past sessions. Dropped the call; activation fires naturally when the user navigates back to `/chat`.

## Test plan

- [x] `pnpm test:unit` — 5974 tests pass (+ 1 todo). New regression tests:
  - `useOpenClawInit-extras.unit.spec.ts`: auth-error auto-retry happy path + uid-swap-mid-retry guard
  - `FeedbackDialog.unit.spec.tsx`: null→crash atomic transition + crash→new-crash full reset
  - `RestartPromptModal.unit.spec.tsx`: 7 cases including the silent-failure regression
- [x] `pnpm lint` clean
- [x] `./node_modules/.bin/tsc --noEmit` clean
- [x] `pnpm dup` under threshold (tests 5.93%, src 3.68%)
- [ ] Manual: trigger a crash → verify dialog shows crash content without flicker
- [ ] Manual: mock backend 500 on redeploy → verify error toast surfaces

## Out of scope (登记 follow-up issue)

Two larger refactor opportunities were identified in the audit but deferred:
- `useOpenClawInit` 4 sentinel refs → reducer (#1959 同款模板，单独 issue)
- `AgentsManagerClient` modal state → discriminated union (减少 useCallback dep churn，单独 issue)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(claw-interface): retry transient R2 upload failures (#1972)

- **SHA**: [6a0dc589](https://github.com/SerendipityOneInc/ecap-workspace/commit/6a0dc58929df2f25ef03ec15d3ab408c912b2d0a)
- **作者**: sam-srp
- **日期**: 2026-05-27T07:50:55Z
- **PR**: #1972

### Commit Message

```
fix(claw-interface): retry transient R2 upload failures (#1972)

## Linear

https://linear.app/srpone/issue/ECA-717/asr-audio-record-dropped-r2-upload-fails-after-successful

## Summary
- add bounded retry handling for transient R2 upload failures in
`R2StorageClient.upload_data`
- retry request errors, timeouts, HTTP 429, and HTTP 5xx responses while
preserving immediate failure for non-retryable statuses such as 403
- add unit coverage for successful retry, non-retryable status, and
exhausted retry behavior

## Root Cause
ASR persistence drops records when `r2.upload_data` raises. A transient
R2 timeout, rate limit, or 5xx could therefore cause a successfully
transcribed audio record to be lost before Mongo persistence.

## Validation
- `conda run -n base python -m pytest tests/unit/test_r2_storage.py`
- `conda run -n base python -m ruff check app/services/r2_storage.py
tests/unit/test_r2_storage.py`
- `conda run -n base pyright app/services/r2_storage.py
tests/unit/test_r2_storage.py`
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-717/asr-audio-record-dropped-r2-upload-fails-after-successful

## Summary
- add bounded retry handling for transient R2 upload failures in `R2StorageClient.upload_data`
- retry request errors, timeouts, HTTP 429, and HTTP 5xx responses while preserving immediate failure for non-retryable statuses such as 403
- add unit coverage for successful retry, non-retryable status, and exhausted retry behavior

## Root Cause
ASR persistence drops records when `r2.upload_data` raises. A transient R2 timeout, rate limit, or 5xx could therefore cause a successfully transcribed audio record to be lost before Mongo persistence.

## Validation
- `conda run -n base python -m pytest tests/unit/test_r2_storage.py`
- `conda run -n base python -m ruff check app/services/r2_storage.py tests/unit/test_r2_storage.py`
- `conda run -n base pyright app/services/r2_storage.py tests/unit/test_r2_storage.py`

---

## feat(chat): add quick command actions (#1945)

- **SHA**: [a55ceba8](https://github.com/SerendipityOneInc/ecap-workspace/commit/a55ceba85219c8ab726c77eeeed8cd96abd3da1e)
- **作者**: vincent-srp
- **日期**: 2026-05-27T07:32:39Z
- **PR**: #1945

### Commit Message

```
feat(chat): add quick command actions (#1945)

## Linear

https://linear.app/srpone/issue/ECA-711/zooclaw-web-agent-new-chat-体验完善可配置快捷指令区-specialist-开场选项

## Summary
- Add configurable quick-start commands for agent chat using official
catalog quick_commands.
- Wire Start a new chat and Summarize and continue to clean /new and
/compact sends without attachments or extra characters.
- Polish quick action labels, selected state, tooltips, and localized
defaults across supported locales.
- Cover main and soulmate quick-command cases plus control-command
behavior in unit tests.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [x] git diff --check

Note: pnpm --dir web run tsc currently fails before typechecking because
the workspace script passes --if-present to pnpm exec, which pnpm
rejects as an unknown option. The app-level tsc command above passed.
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-711/zooclaw-web-agent-new-chat-体验完善可配置快捷指令区-specialist-开场选项

## Summary
- Add configurable quick-start commands for agent chat using official catalog quick_commands.
- Wire Start a new chat and Summarize and continue to clean /new and /compact sends without attachments or extra characters.
- Polish quick action labels, selected state, tooltips, and localized defaults across supported locales.
- Cover main and soulmate quick-command cases plus control-command behavior in unit tests.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [x] git diff --check

Note: pnpm --dir web run tsc currently fails before typechecking because the workspace script passes --if-present to pnpm exec, which pnpm rejects as an unknown option. The app-level tsc command above passed.

---

## refactor(computer): normalize workspace APIs (#1949)

- **SHA**: [975c133e](https://github.com/SerendipityOneInc/ecap-workspace/commit/975c133e717682d771e6c164a9e1daeb3a1b813d)
- **作者**: bill-srp
- **日期**: 2026-05-27T07:18:00Z
- **PR**: #1949

### Commit Message

```
refactor(computer): normalize workspace APIs (#1949)

## Summary
- add the normalized computer and scoped agent workspace API under
/computers/{computer_id}/agents
- document the enterprise backend agent/computer model and migration
precondition
- remove legacy read fallback and tighten computer/agent workspace
schemas

## Test plan
- [x] docker exec -w /workspaces/service-agents/services/claw-interface
service-agents-bill /home/node/.venvs/claw-interface/bin/ruff check .
- [x] docker exec -w /workspaces/service-agents/services/claw-interface
service-agents-bill pnpm dlx pyright app tests
- [x] docker exec -w /workspaces/service-agents/services/claw-interface
service-agents-bill /home/node/.venvs/claw-interface/bin/python -m
pytest tests/unit/test_agent_routes.py tests/unit/test_agent_service.py
tests/unit/test_computer_service.py
tests/unit/test_agent_workspace_repo.py tests/unit/test_computer_repo.py
-q
- [x] docker exec -w /workspaces/service-agents/services/claw-interface
service-agents-bill /home/node/.venvs/claw-interface/bin/python -m
pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q
--ignore=tests/unit/test_ci_lint_deptry.py (3733 passed, 370 skipped;
coverage-only failure: 88.03% < 90%)
- [ ] full local pytest including tests/unit/test_ci_lint_deptry.py
(blocked in this devcontainer worktree: git rev-parse resolves host
gitdir path
/Users/bill/Github/StarQuestAI/ecap-workspace/.git/worktrees/service-agents)
```

### PR Description

## Summary
- add the normalized computer and scoped agent workspace API under /computers/{computer_id}/agents
- document the enterprise backend agent/computer model and migration precondition
- remove legacy read fallback and tighten computer/agent workspace schemas

## Test plan
- [x] docker exec -w /workspaces/service-agents/services/claw-interface service-agents-bill /home/node/.venvs/claw-interface/bin/ruff check .
- [x] docker exec -w /workspaces/service-agents/services/claw-interface service-agents-bill pnpm dlx pyright app tests
- [x] docker exec -w /workspaces/service-agents/services/claw-interface service-agents-bill /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_agent_routes.py tests/unit/test_agent_service.py tests/unit/test_computer_service.py tests/unit/test_agent_workspace_repo.py tests/unit/test_computer_repo.py -q
- [x] docker exec -w /workspaces/service-agents/services/claw-interface service-agents-bill /home/node/.venvs/claw-interface/bin/python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q --ignore=tests/unit/test_ci_lint_deptry.py (3733 passed, 370 skipped; coverage-only failure: 88.03% < 90%)
- [ ] full local pytest including tests/unit/test_ci_lint_deptry.py (blocked in this devcontainer worktree: git rev-parse resolves host gitdir path /Users/bill/Github/StarQuestAI/ecap-workspace/.git/worktrees/service-agents)

---

## refactor(web): OpenClawProvider effect-density via reducer (#1959) (#1970)

- **SHA**: [2e078e02](https://github.com/SerendipityOneInc/ecap-workspace/commit/2e078e0239537a614d4b0a1b8ec0ca69cbec8263)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-27T06:20:18Z
- **PR**: #1959

### Commit Message

```
refactor(web): OpenClawProvider effect-density via reducer (#1959) (#1970)

## Summary

- Closes #1959 (sub-issue of #1667 useEffect anti-pattern umbrella;
audit doc
`docs/superpowers/specs/2026-05-26-provider-effect-density-audit.md`).
- Replaces `OpenClawProvider`'s 7-effect / 3-ref implicit state machine
with a pure reducer + observer/response pattern, mirroring the
MattermostProvider template shipped in #1953
(`lib/mattermost/connect-reducer.ts`).
- Provider body effect count: **7 → 3** (observer / response / unmount
cleanup). Sub-hooks own their own effects: `useOpenClawSentryTracker` /
`useOpenClawVisibilityRecovery` / `useOpenClawHealthWatchdog`.

### Option chosen: B (reducer)

Per the issue's acceptance criteria asking for A/B/C with rationale:

- **A (single `useOpenClawConnectionLifecycle` god-hook)** keeps
ref-based state, no testability win.
- **B (pure reducer)** ← chosen. Direct precedent in #1953; reducer is
testable without jsdom (29 transition tests, no rendering); Provider
footprint shrinks to its minimum.
- **C (only extract standalone effects, leave retry cluster)** doesn't
meet the "≤ 3 effects on the provider itself" target.

### Key design choices

1. **`reInitTimerRef` stays in Provider, not in reducer state** —
`setTimeout` handle is a DOM resource, not pure state. Single response
effect owns its full lifecycle (set / clear / unmount cleanup all
co-located).
2. **`WS_DISCONNECTED_OR_ERROR` no-ops from `armed` / `escalating`** —
protects in-flight `wsConnect` / `silentRetry` intents when the
consolidated observer dispatches multiple actions in the same render. WS
hook owns its own reconnect loop, so the reducer doesn't need to "react"
to disconnects unless coming from `connected` / `connecting`.
3. **Visibility recovery & health watchdog call `silentRetry` directly,
not via reducer phase** — those paths need immediate firing (no 5s
delay) and shouldn't be routed through the response effect's timer
machinery. The reducer just records the bookkeeping reset.
4. **Latent fix: `lastEscalationAttempt` dedupe sentinel** — the
original Effect #4 could over-increment `reInitAttemptRef` on
`initStatus` flutter at constant `wsReconnectAttempt`; the reducer
dedupes by the attempt value, fixing this for free.

## Acceptance (per issue #1959)

- [x] Option B picked + rationale (above).
- [x] Provider effect count reduced (7 → 3, target ≤ 3).
- [x] No regression in OpenClaw clawhub install/uninstall + WS reconnect
+ visibility-recovery — full unit suite (5952 tests) green; existing
`OpenClawContext.unit.spec.tsx` (21 cases) untouched.
- [x] New behavior-locking unit tests:
- `connect-reducer.unit.spec.ts` — 29 reducer transition tests (pure, no
jsdom).
  - `useOpenClawSentryTracker.unit.spec.ts` — 4 cases.
- `useOpenClawVisibilityRecovery.unit.spec.ts` — 9 cases (visibility
branches + cache refresh + reject path).
- `useOpenClawHealthWatchdog.unit.spec.ts` — 9 cases (timer + skip
predicates + cancellation).
- `OpenClawProvider.behavior.unit.spec.tsx` — 11 integration scenarios
(auto-connect, escalation, watchdog, visibility).

## Test plan
- [ ] CI `code-quality / lint-and-test` green
- [ ] Manual verification on staging or local dev (mock-backend):
  - First load: bot init → WS connect fires exactly once
- clawhub install / uninstall: mutation completes, RQ refetch updates UI
- Tab away 60s then return: visibility recovery fires `silentRetry` once
- Kill backend `:8000`: 30s watchdog fires `wsDisconnect` +
`silentRetry`
  - Restart backend: WS reconnects

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

Sub-issue of #1667 — split out from #1924 audit (`docs/superpowers/specs/2026-05-26-provider-effect-density-audit.md`).

## Background

The audit landed in #1924 classified `web/app/src/components/providers/OpenClawProvider.tsx` (7 effects, 201 LOC) as the second-most worthwhile refactor target after FeedbackProvider (POC landed alongside #1924). Three effects are high-priority:

| # | Lines | Bucket | Sub-hook candidate |
|---|---|---|---|
| 2 | 63–71 | 3 | `useOpenClawAutoConnect` — "init ready + bot creds → wsConnect" orchestration |
| 3 | 73–84 | 2 | `useOpenClawConnectionReset` — `wsStatus` change triggers ref + timer reset |
| 4 | 89–105 | 4 | `useOpenClawReInitEscalation` — threshold-driven retry chain |

Medium-priority candidates: effect #1 (Sentry bot context), #5 (visibility-recovery), #6 (health watchdog). Effect #7 is pure cleanup.

## Design constraint — solve first, before extracting

**Effects #2 + #4 + #6 share retry-timer state (refs + `setTimeout` handles).** A naive 1-effect → 1-hook extraction would shard the same ref state across 3 sub-hooks, which is *worse* than the current shape because state ownership becomes unclear.

Before opening code PRs, the issue must answer:

- Option A: extract a single `useOpenClawConnectionLifecycle` hook that owns all retry refs + timers + escalation logic. Provider becomes a thin shell that wires \`wsConnect\`/\`silentRetry\` into it.
- Option B: hoist retry state into a reducer (mirror what \`MattermostProvider\` did via \`connect-reducer.ts\` in #1946-#1955). Sub-hooks become observer/response effects of a pure state machine.
- Option C: only extract the standalone effects (#1 Sentry, #5 visibility, #7 cleanup) and leave the shared-state cluster intact behind a clear comment.

Option B has the best precedent (Mattermost's reducer is unit-testable React-free) but the largest blast radius. Option A is the middle ground. Option C is "do nothing risky."

## Acceptance

- [ ] Pick option A/B/C with rationale in PR description (or a follow-up spec doc)
- [ ] Provider effect count reduced (target: ≤ 3 effects on the provider itself)
- [ ] No regression in OpenClaw clawhub install/uninstall + WS reconnect + visibility-recovery
- [ ] At least one new behavior-locking unit test per extracted hook

## Out of scope

- Refactoring \`useOpenClawInit\` / \`useOpenClawWebSocket\` themselves (they already exist as sub-hooks)
- Touching \`MattermostProvider\` or \`FeedbackProvider\` (audit conclusion: both done or already at endgame)

## Related

- #1667 — umbrella useEffect anti-pattern tracker
- #1924 — audit doc + FeedbackProvider POC
- #1689 — \`OnboardingProvider\` refactor (template for sub-hook extraction)
- #1946-#1955 — \`useMattermost\` sub-hook split + reducer extraction (template for Option B)

---

## refactor(web): extractGroupShapes + mapChildToSlide → SlideContext (#1957) (#1971)

- **SHA**: [3ef4ca1f](https://github.com/SerendipityOneInc/ecap-workspace/commit/3ef4ca1fde5573c38d4c2743ce33ff5283455a6f)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-27T05:21:30Z
- **PR**: #1957

### Commit Message

```
refactor(web): extractGroupShapes + mapChildToSlide → SlideContext (#1957) (#1971)

## Summary

抽 `SlideContext` interface (`slideCx, slideCy, relsMap, zip`) 一并解
pptx-parser 里 2 个 5-param 函数:

- `extractGroupShapes(grpEl, slideCx, slideCy, relsMap, zip)` →
`extractGroupShapes(grpEl, ctx)`
- `mapChildToSlide(childOff, childExt, grp, slideCx, slideCy)` →
`mapChildToSlide(childOff, childExt, grp, ctx)`（用 `Pick<SlideContext,
'slideCx' | 'slideCy'>` 收窄只用 dims 子集）

Caller 同步：3 处 `mapChildToSlide`（`extractGroupShapes` 内）+ 1 处递归 + 1 处外部
dispatcher。函数体逻辑 zero-diff，只换签名 + 解构。

`eslint.config.mjs`：`pptx-parser.ts` 从 legacy complexity exemption block
摘出，换成 narrow per-file override 只关 `complexity` + `max-lines` ——
这两个违例属于另外 refactor 类目（issue 明示不在 #1957
范围），`max-params`/`max-depth`/`max-lines-per-function`/`max-nested-callbacks`
enforcement 恢复。

Refs #1957（max-params 系列 PR 3/N，PR 1 #1967 + PR 2 #1969 已 merged）

## Test plan

- [x] `npx tsc --noEmit` 无错
- [x] `pnpm lint` 0 errors
- [x] 单独 `eslint src/components/artifacts/renderers/pptx-parser.ts` 确认
narrow override 生效（仅 4 个 complexity + 1 个 max-lines 残留，已在 override 内放行）
- [ ] **未做** browser smoke test（无单测 + 无现成 .pptx fixture；函数体 zero-diff
风险低，建议 reviewer 在 staging 验一个有 group shapes 的 .pptx）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## 背景

本 issue 跟踪 ESLint `max-params` 默认 4 上限被违反的函数 — F15 anti-pattern audit 期间扫出。每个 case 都是把分散的参数收成 options object 即可解决。

收回独立的 `eslint.config.mjs` exemption 后,这些函数会重新被 lint 拦,以下是它们应该重构的位置:

## 5-param

### 🚩 `getSessionList` (`src/lib/api/session.ts:108`)
```typescript
async function getSessionList(uid, agentName?, limit?, offset?, includeAssets?)
```
教科书级 options object case — 4 个 optional query。call site 改造前 vs 后:
```typescript
// before
getSessionList(uid, undefined, 20, undefined, true)
// after
getSessionList(uid, { limit: 20, includeAssets: true })
```

### 🚩 `extractGroupShapes` (`src/components/artifacts/renderers/pptx-parser.ts:849`)
```typescript
async function extractGroupShapes(grpEl, slideCx, slideCy, relsMap, zip)
```
5 个完全不同类型(Element + 2 number + Map + JSZip)。后 4 个其实是 "slide-level context",应改:
```typescript
extractGroupShapes(grpEl, ctx: { slideCx, slideCy, relsMap, zip })
```

### `reportLatency` (`src/lib/sentry/openclaw-monitor.ts:261`)
```typescript
reportLatency(phase, durationMs, level, opts, extra?)
```
opts 已是 options object 一半,phase/durationMs/level 该塞进 opts 或独立成 `metric` 对象。

### 可接受 / 边界:
- `hasOverlap` (canvas/useCanvasState:30) — `(nodes, x, y, w, h)`,几何标准签名,改 `(nodes, rect)` 也行
- `mapChildToSlide` (pptx-parser:580) — 数学投影,参数内聚

## 6+ param

### 🚩 `customInputArea` (`src/components/agent-chat-client/types.ts:62`) — 8 params
```typescript
customInputArea?: (input, setInput, handleSubmit, isLoading, sessionId, isInitializing, isReadOnly, messagesCount) => React.ReactNode
```
render-prop callback,8 positional args,极难记。应改 props object — 标准 React render-prop pattern:
```typescript
customInputArea?: (props: { input, setInput, handleSubmit, ... }) => React.ReactNode
```

### `getCtaConfig` / `getBadge` (`src/components/billing/PlanCard.tsx:81,130`) — 6 params each
两个函数共享 5 个 billing state 参数。应改:
```typescript
function getCtaConfig(state: BillingState): { label, action, variant }
function getBadge(state: BillingState): { label, variant } | null
```

## 验证策略

每个 case 都是单文件改动 + caller 同步。预期每个 ≤ 100 行 diff,适合零碎 PR 各自处理。每改一个,从 `eslint.config.mjs` 的 legacy complexity exemption block 把对应文件删除一行。

## 当前 exemption 状态

F15 follow-up (PR #1953 / #1954 / #1955 / #1956) 已把 `useMattermost.ts` 和 `useMattermostConnection.ts` 从 exemption 收回 — `autoConnect` 也已改成 options object 作为示范。剩余 exemption 文件:

- `src/components/agent-chat-client/types.ts`(`customInputArea` 8 params + 其他 complexity 原因)
- `src/components/billing/PlanCard.tsx`(`getCtaConfig` / `getBadge` 6 params)
- `src/app/[locale]/canvas/hooks/useCanvasState.ts`(`hasOverlap` + max-lines-per-function 572 行)
- `src/app/[locale]/canvas/hooks/useCanvasChat.ts`(2 个 5-param)
- `src/components/artifacts/renderers/pptx-parser.ts`(`mapChildToSlide` + `extractGroupShapes` + complexity 31)
- `src/lib/api/session.ts`(`getSessionList`)
- `src/lib/sentry/openclaw-monitor.ts`(`reportLatency`)

## 不在范围

非 max-params 违例(complexity 31 / max-lines-per-function 572 / max-lines 898)— 这些是不同的 refactor 类目,各自有独立的 owner 决策。

---

## refactor(web): reportLatency → options object (#1957) (#1969)

- **SHA**: [28cdfdaf](https://github.com/SerendipityOneInc/ecap-workspace/commit/28cdfdaff18077c698eb2093d766dd2c6f89c140)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-27T05:03:06Z
- **PR**: #1957

### Commit Message

```
refactor(web): reportLatency → options object (#1957) (#1969)

## Summary

`reportLatency(phase, durationMs, level, opts, extra?)` 5-param 改成
`reportLatency({phase, durationMs, level, opts}, extra?)` —— `opts` 本来就是
object,外层 3 个 positional 一并收。

- `src/lib/sentry/openclaw-monitor.ts`: 函数签名 + 3 处 caller(全在同文件)
- `eslint.config.mjs`: 从 legacy complexity exemption block 摘除
`src/lib/sentry/openclaw-monitor.ts`（除 reportLatency 外该文件无其他 complexity
违例，单跑 eslint 已确认 clean）

Refs #1957（max-params 系列 PR 2/N，PR 1 #1967 已 merged）

## Test plan

- [x] `npx tsc --noEmit` 无错
- [x] `pnpm lint` 0 errors
- [x] 单独 `eslint src/lib/sentry/openclaw-monitor.ts` 确认 file-level
exempt 摘除后无新增 violation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## 背景

本 issue 跟踪 ESLint `max-params` 默认 4 上限被违反的函数 — F15 anti-pattern audit 期间扫出。每个 case 都是把分散的参数收成 options object 即可解决。

收回独立的 `eslint.config.mjs` exemption 后,这些函数会重新被 lint 拦,以下是它们应该重构的位置:

## 5-param

### 🚩 `getSessionList` (`src/lib/api/session.ts:108`)
```typescript
async function getSessionList(uid, agentName?, limit?, offset?, includeAssets?)
```
教科书级 options object case — 4 个 optional query。call site 改造前 vs 后:
```typescript
// before
getSessionList(uid, undefined, 20, undefined, true)
// after
getSessionList(uid, { limit: 20, includeAssets: true })
```

### 🚩 `extractGroupShapes` (`src/components/artifacts/renderers/pptx-parser.ts:849`)
```typescript
async function extractGroupShapes(grpEl, slideCx, slideCy, relsMap, zip)
```
5 个完全不同类型(Element + 2 number + Map + JSZip)。后 4 个其实是 "slide-level context",应改:
```typescript
extractGroupShapes(grpEl, ctx: { slideCx, slideCy, relsMap, zip })
```

### `reportLatency` (`src/lib/sentry/openclaw-monitor.ts:261`)
```typescript
reportLatency(phase, durationMs, level, opts, extra?)
```
opts 已是 options object 一半,phase/durationMs/level 该塞进 opts 或独立成 `metric` 对象。

### 可接受 / 边界:
- `hasOverlap` (canvas/useCanvasState:30) — `(nodes, x, y, w, h)`,几何标准签名,改 `(nodes, rect)` 也行
- `mapChildToSlide` (pptx-parser:580) — 数学投影,参数内聚

## 6+ param

### 🚩 `customInputArea` (`src/components/agent-chat-client/types.ts:62`) — 8 params
```typescript
customInputArea?: (input, setInput, handleSubmit, isLoading, sessionId, isInitializing, isReadOnly, messagesCount) => React.ReactNode
```
render-prop callback,8 positional args,极难记。应改 props object — 标准 React render-prop pattern:
```typescript
customInputArea?: (props: { input, setInput, handleSubmit, ... }) => React.ReactNode
```

### `getCtaConfig` / `getBadge` (`src/components/billing/PlanCard.tsx:81,130`) — 6 params each
两个函数共享 5 个 billing state 参数。应改:
```typescript
function getCtaConfig(state: BillingState): { label, action, variant }
function getBadge(state: BillingState): { label, variant } | null
```

## 验证策略

每个 case 都是单文件改动 + caller 同步。预期每个 ≤ 100 行 diff,适合零碎 PR 各自处理。每改一个,从 `eslint.config.mjs` 的 legacy complexity exemption block 把对应文件删除一行。

## 当前 exemption 状态

F15 follow-up (PR #1953 / #1954 / #1955 / #1956) 已把 `useMattermost.ts` 和 `useMattermostConnection.ts` 从 exemption 收回 — `autoConnect` 也已改成 options object 作为示范。剩余 exemption 文件:

- `src/components/agent-chat-client/types.ts`(`customInputArea` 8 params + 其他 complexity 原因)
- `src/components/billing/PlanCard.tsx`(`getCtaConfig` / `getBadge` 6 params)
- `src/app/[locale]/canvas/hooks/useCanvasState.ts`(`hasOverlap` + max-lines-per-function 572 行)
- `src/app/[locale]/canvas/hooks/useCanvasChat.ts`(2 个 5-param)
- `src/components/artifacts/renderers/pptx-parser.ts`(`mapChildToSlide` + `extractGroupShapes` + complexity 31)
- `src/lib/api/session.ts`(`getSessionList`)
- `src/lib/sentry/openclaw-monitor.ts`(`reportLatency`)

## 不在范围

非 max-params 违例(complexity 31 / max-lines-per-function 572 / max-lines 898)— 这些是不同的 refactor 类目,各自有独立的 owner 决策。

---

## refactor(web): replace verify countdown setTimeout chain with endTime derivation (#1968)

- **SHA**: [b027ab55](https://github.com/SerendipityOneInc/ecap-workspace/commit/b027ab553d175d3db076e892c968e97a430f46d4)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-27T04:58:52Z
- **PR**: #1968

### Commit Message

```
refactor(web): replace verify countdown setTimeout chain with endTime derivation (#1968)

## Background

Closes #1964 (follow-up to #1920 — the countdown was deliberately left
untouched in the useEffect anti-pattern audit because it's a UX bug, not
an effect-pattern issue).

The resend cooldown on `user/verify/page.tsx` previously decremented a
`useState(0)` counter via recursive `setTimeout`, which drifts
noticeably under browser background-tab throttling (Chromium throttles
inactive-tab setTimeout heavily after 5min) and pauses entirely during
mobile device sleep. A user who clicks "resend", switches tabs / locks
their phone for 30s, and returns will see the countdown stuck near `60 -
throttled_ticks` instead of the wall-clock-elapsed value — having to
wait noticeably longer than 60 real seconds before resend re-enables.

## Changes

- **Wall-clock derivation**: replace `[countdown, setCountdown]` with
`[resendEndAt: number | null, setResendEndAt]` + a derived `countdown =
ceil((resendEndAt - now) / 1000)`. The effect now runs a single
`setInterval` (instead of recursive `setTimeout`s) that re-reads
`Date.now()` on each tick — so when the tab returns from background or
the device wakes, the displayed countdown snaps to the real remaining
seconds and clears immediately if already past `resendEndAt`.
- **Four call sites** (OTP bootstrap, `handleResendEmailOTP`,
`handleResendPhone`, `handleResendEmail`) updated from
`setCountdown(60)` to `setResendEndAt(Date.now() + 60_000)`. JSX
consumers are unchanged.
- **`tick()` runs once inside the effect** before `setInterval` starts
so the freshly-set endTime reflects in the display immediately (avoids a
1s "stale `now`" flash before the first interval fires).
- **No new `eslint-disable react-hooks/exhaustive-deps`** introduced
(acceptance criterion #4).

## Tests

- Adds a regression spec in `user-verify-email-otp.unit.spec.tsx` that
spies `Date.now()` separately from fake `setInterval` to simulate a
suspended-then-resumed interval (wall-clock jumps 65s while the interval
was throttled). The old `setTimeout(n - 1)` implementation would still
report ~59s left; the new implementation snaps to 0 on the first resumed
tick.
- Stabilizes the `useLocalizedRouter` mock to return a cached object
reference (matching production `useRouter` semantics), so the bootstrap
effect's `[isOTP, router]` deps don't thrash on every render and re-set
`resendEndAt` indefinitely. This was masked by the old
`setCountdown(60)` (re-setting `60` is idempotent) but breaks the new
`setResendEndAt(Date.now() + 60_000)` (each call pushes the endTime
further out).
- All 3 existing `user-verify-*` specs continue to pass unchanged
(acceptance criterion #2).

## Notes

- **Not extracting a `useCountdown` hook**: Issue's acceptance criterion
#3 suggested considering this. Investigation confirmed `LoginForm` does
not actually have its own countdown (it routes to `/user/verify`);
verify is the sole consumer. The `*SetupModal` siblings have different
ticking-clock semantics (QR-code-expiry display). Keeping it inline
avoids a single-caller abstraction per CLAUDE.md "Minimal changes".
- SSR/hydration safety: `useState(() => Date.now())` returns different
values on server vs client, but since `resendEndAt` starts as `null` the
derived `countdown` is always `0` on first render — no hydration
mismatch.

## Test plan

- [x] `pnpm test:unit` — 5887 tests pass (1 new + all existing)
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [ ] Manual: navigate to `/zh/user/verify?otp=true&email=…`, click
resend, switch tabs for 30s+, verify countdown reflects real elapsed
time on return

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Background

Closes #1964 (follow-up to #1920 — the countdown was deliberately left untouched in the useEffect anti-pattern audit because it's a UX bug, not an effect-pattern issue).

The resend cooldown on `user/verify/page.tsx` previously decremented a `useState(0)` counter via recursive `setTimeout`, which drifts noticeably under browser background-tab throttling (Chromium throttles inactive-tab setTimeout heavily after 5min) and pauses entirely during mobile device sleep. A user who clicks "resend", switches tabs / locks their phone for 30s, and returns will see the countdown stuck near `60 - throttled_ticks` instead of the wall-clock-elapsed value — having to wait noticeably longer than 60 real seconds before resend re-enables.

## Changes

- **Wall-clock derivation**: replace `[countdown, setCountdown]` with `[resendEndAt: number | null, setResendEndAt]` + a derived `countdown = ceil((resendEndAt - now) / 1000)`. The effect now runs a single `setInterval` (instead of recursive `setTimeout`s) that re-reads `Date.now()` on each tick — so when the tab returns from background or the device wakes, the displayed countdown snaps to the real remaining seconds and clears immediately if already past `resendEndAt`.
- **Four call sites** (OTP bootstrap, `handleResendEmailOTP`, `handleResendPhone`, `handleResendEmail`) updated from `setCountdown(60)` to `setResendEndAt(Date.now() + 60_000)`. JSX consumers are unchanged.
- **`tick()` runs once inside the effect** before `setInterval` starts so the freshly-set endTime reflects in the display immediately (avoids a 1s "stale `now`" flash before the first interval fires).
- **No new `eslint-disable react-hooks/exhaustive-deps`** introduced (acceptance criterion #4).

## Tests

- Adds a regression spec in `user-verify-email-otp.unit.spec.tsx` that spies `Date.now()` separately from fake `setInterval` to simulate a suspended-then-resumed interval (wall-clock jumps 65s while the interval was throttled). The old `setTimeout(n - 1)` implementation would still report ~59s left; the new implementation snaps to 0 on the first resumed tick.
- Stabilizes the `useLocalizedRouter` mock to return a cached object reference (matching production `useRouter` semantics), so the bootstrap effect's `[isOTP, router]` deps don't thrash on every render and re-set `resendEndAt` indefinitely. This was masked by the old `setCountdown(60)` (re-setting `60` is idempotent) but breaks the new `setResendEndAt(Date.now() + 60_000)` (each call pushes the endTime further out).
- All 3 existing `user-verify-*` specs continue to pass unchanged (acceptance criterion #2).

## Notes

- **Not extracting a `useCountdown` hook**: Issue's acceptance criterion #3 suggested considering this. Investigation confirmed `LoginForm` does not actually have its own countdown (it routes to `/user/verify`); verify is the sole consumer. The `*SetupModal` siblings have different ticking-clock semantics (QR-code-expiry display). Keeping it inline avoids a single-caller abstraction per CLAUDE.md "Minimal changes".
- SSR/hydration safety: `useState(() => Date.now())` returns different values on server vs client, but since `resendEndAt` starts as `null` the derived `countdown` is always `0` on first render — no hydration mismatch.

## Test plan

- [x] `pnpm test:unit` — 5887 tests pass (1 new + all existing)
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [ ] Manual: navigate to `/zh/user/verify?otp=true&email=…`, click resend, switch tabs for 30s+, verify countdown reflects real elapsed time on return

---

## refactor(web): getSessionList → options object (#1957) (#1967)

- **SHA**: [a680e522](https://github.com/SerendipityOneInc/ecap-workspace/commit/a680e522177bbaff95f222e2fc16a4b2d79a0826)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-27T04:50:53Z
- **PR**: #1957

### Commit Message

```
refactor(web): getSessionList → options object (#1957) (#1967)

## Summary

`getSessionList(uid, agentName?, limit?, offset?, includeAssets?)` 5
个分散参数改成 `getSessionList(uid, opts?)`，消掉 caller 的 `undefined` 套娃。

- `src/lib/api/session.ts`: 5-param → 2-param 签名 + 函数体内解构 opts
- `tests/unit/lib/api/session.unit.spec.ts`: 3 处 caller 改对象形式
- `eslint.config.mjs`: 从 legacy complexity exemption block 摘除
`src/lib/api/session.ts`（该文件唯一的 max-params 违例就是这个函数）

Refs #1957（max-params 系列 PR 1/N）

## Test plan

- [x] `pnpm test:unit` 全绿（5886 passed）
- [x] `npx tsc --noEmit` 无错
- [x] `pnpm lint` 0 errors
- [x] 单独 `eslint src/lib/api/session.ts` 确认从 exempt 摘掉后无新增 error

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## 背景

本 issue 跟踪 ESLint `max-params` 默认 4 上限被违反的函数 — F15 anti-pattern audit 期间扫出。每个 case 都是把分散的参数收成 options object 即可解决。

收回独立的 `eslint.config.mjs` exemption 后,这些函数会重新被 lint 拦,以下是它们应该重构的位置:

## 5-param

### 🚩 `getSessionList` (`src/lib/api/session.ts:108`)
```typescript
async function getSessionList(uid, agentName?, limit?, offset?, includeAssets?)
```
教科书级 options object case — 4 个 optional query。call site 改造前 vs 后:
```typescript
// before
getSessionList(uid, undefined, 20, undefined, true)
// after
getSessionList(uid, { limit: 20, includeAssets: true })
```

### 🚩 `extractGroupShapes` (`src/components/artifacts/renderers/pptx-parser.ts:849`)
```typescript
async function extractGroupShapes(grpEl, slideCx, slideCy, relsMap, zip)
```
5 个完全不同类型(Element + 2 number + Map + JSZip)。后 4 个其实是 "slide-level context",应改:
```typescript
extractGroupShapes(grpEl, ctx: { slideCx, slideCy, relsMap, zip })
```

### `reportLatency` (`src/lib/sentry/openclaw-monitor.ts:261`)
```typescript
reportLatency(phase, durationMs, level, opts, extra?)
```
opts 已是 options object 一半,phase/durationMs/level 该塞进 opts 或独立成 `metric` 对象。

### 可接受 / 边界:
- `hasOverlap` (canvas/useCanvasState:30) — `(nodes, x, y, w, h)`,几何标准签名,改 `(nodes, rect)` 也行
- `mapChildToSlide` (pptx-parser:580) — 数学投影,参数内聚

## 6+ param

### 🚩 `customInputArea` (`src/components/agent-chat-client/types.ts:62`) — 8 params
```typescript
customInputArea?: (input, setInput, handleSubmit, isLoading, sessionId, isInitializing, isReadOnly, messagesCount) => React.ReactNode
```
render-prop callback,8 positional args,极难记。应改 props object — 标准 React render-prop pattern:
```typescript
customInputArea?: (props: { input, setInput, handleSubmit, ... }) => React.ReactNode
```

### `getCtaConfig` / `getBadge` (`src/components/billing/PlanCard.tsx:81,130`) — 6 params each
两个函数共享 5 个 billing state 参数。应改:
```typescript
function getCtaConfig(state: BillingState): { label, action, variant }
function getBadge(state: BillingState): { label, variant } | null
```

## 验证策略

每个 case 都是单文件改动 + caller 同步。预期每个 ≤ 100 行 diff,适合零碎 PR 各自处理。每改一个,从 `eslint.config.mjs` 的 legacy complexity exemption block 把对应文件删除一行。

## 当前 exemption 状态

F15 follow-up (PR #1953 / #1954 / #1955 / #1956) 已把 `useMattermost.ts` 和 `useMattermostConnection.ts` 从 exemption 收回 — `autoConnect` 也已改成 options object 作为示范。剩余 exemption 文件:

- `src/components/agent-chat-client/types.ts`(`customInputArea` 8 params + 其他 complexity 原因)
- `src/components/billing/PlanCard.tsx`(`getCtaConfig` / `getBadge` 6 params)
- `src/app/[locale]/canvas/hooks/useCanvasState.ts`(`hasOverlap` + max-lines-per-function 572 行)
- `src/app/[locale]/canvas/hooks/useCanvasChat.ts`(2 个 5-param)
- `src/components/artifacts/renderers/pptx-parser.ts`(`mapChildToSlide` + `extractGroupShapes` + complexity 31)
- `src/lib/api/session.ts`(`getSessionList`)
- `src/lib/sentry/openclaw-monitor.ts`(`reportLatency`)

## 不在范围

非 max-params 违例(complexity 31 / max-lines-per-function 572 / max-lines 898)— 这些是不同的 refactor 类目,各自有独立的 owner 决策。

---

## refactor(web): clean up useEffect anti-patterns in user/verify/page.tsx (#1958)

- **SHA**: [80f0063e](https://github.com/SerendipityOneInc/ecap-workspace/commit/80f0063e0b8fe126c6dd02762cdf8fd82d5cd880)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-27T04:08:36Z
- **PR**: #1958

### Commit Message

```
refactor(web): clean up useEffect anti-patterns in user/verify/page.tsx (#1958)

## Summary

Closes #1920. Sub-task of #1667 useEffect anti-pattern umbrella.

`web/app/src/app/[locale]/user/verify/page.tsx` had 7 `useEffect` total;
4 fell into [You Might Not Need an
Effect](https://react.dev/learn/you-might-not-need-an-effect) buckets.
This PR migrates them to render-time / event-handler patterns and
removes the `react-hooks/exhaustive-deps` disable (per #1526).

| Old effect | Bucket | New form |
|------------|--------|----------|
| Read `EMAIL_OTP_PENDING_EMAIL` + redirect on miss | 3 | `useState`
lazy init via `initialEmail` IIFE |
| `!isOTP && !phone && !email → router.push` redirect | 3 | Combined
into single `needsRedirect` derivation + redirect effect + render-time
`return null` |
| `setCountdown(60)` when `email && isOTP` | 1 | `useState(isOTP &&
initialEmail ? 60 : 0)` lazy init |
| Magic-link auto-verify with `eslint-disable exhaustive-deps` | 4 |
Inlined `handleEmailVerification` body + `useRef` one-shot guard; deps
`[email, router, t]` complete; **disable removed** |

Preserves 3 legitimate effects unchanged: OTP completing timer
(sessionStorage TTL sync), `<html>` overflow lock + animation (DOM
sync), countdown tick (timer).

`handleEmailVerification` standalone function deleted — only caller was
the magic-link effect, now inlined.

Net diff: `+68 / -66` (5 effects remaining, down from 7).

## Test plan

- [x] `pnpm tsc` — passes
- [x] `pnpm lint` — passes (zero warnings)
- [x] `pnpm test:unit` — 386 test files / 5859 tests pass
- [x] 4 shrink-only audit scripts (forbid-dom-props / svg-inline /
no-raw-fetch / filename-naming) — all green vs main
- [ ] **Manual UI verification (deferred to reviewer)** — no automated
coverage exists for this page; verify 5 flows via `pnpm dev` +
mock-backend:
- Phone flow `/verify?phone=+1...` — countdown starts at 0; resend
triggers 60s
- OTP flow `/verify?otp=true` WITH sessionStorage — first-paint renders
OTP card, countdown 60→0
- OTP flow WITHOUT sessionStorage — immediate redirect to landing, no
card flash
- Magic-link flow `/verify?email=...&mode=signIn&oobCode=...` —
**`verifyEmailLink` fires exactly once under StrictMode** (check
DevTools Network)
  - Empty `/verify` — immediate redirect, no flash
```

### PR Description

## Summary

Closes #1920. Sub-task of #1667 useEffect anti-pattern umbrella.

`web/app/src/app/[locale]/user/verify/page.tsx` had 7 `useEffect` total; 4 fell into [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) buckets. This PR migrates them to render-time / event-handler patterns and removes the `react-hooks/exhaustive-deps` disable (per #1526).

| Old effect | Bucket | New form |
|------------|--------|----------|
| Read `EMAIL_OTP_PENDING_EMAIL` + redirect on miss | 3 | `useState` lazy init via `initialEmail` IIFE |
| `!isOTP && !phone && !email → router.push` redirect | 3 | Combined into single `needsRedirect` derivation + redirect effect + render-time `return null` |
| `setCountdown(60)` when `email && isOTP` | 1 | `useState(isOTP && initialEmail ? 60 : 0)` lazy init |
| Magic-link auto-verify with `eslint-disable exhaustive-deps` | 4 | Inlined `handleEmailVerification` body + `useRef` one-shot guard; deps `[email, router, t]` complete; **disable removed** |

Preserves 3 legitimate effects unchanged: OTP completing timer (sessionStorage TTL sync), `<html>` overflow lock + animation (DOM sync), countdown tick (timer).

`handleEmailVerification` standalone function deleted — only caller was the magic-link effect, now inlined.

Net diff: `+68 / -66` (5 effects remaining, down from 7).

## Test plan

- [x] `pnpm tsc` — passes
- [x] `pnpm lint` — passes (zero warnings)
- [x] `pnpm test:unit` — 386 test files / 5859 tests pass
- [x] 4 shrink-only audit scripts (forbid-dom-props / svg-inline / no-raw-fetch / filename-naming) — all green vs main
- [ ] **Manual UI verification (deferred to reviewer)** — no automated coverage exists for this page; verify 5 flows via `pnpm dev` + mock-backend:
  - Phone flow `/verify?phone=+1...` — countdown starts at 0; resend triggers 60s
  - OTP flow `/verify?otp=true` WITH sessionStorage — first-paint renders OTP card, countdown 60→0
  - OTP flow WITHOUT sessionStorage — immediate redirect to landing, no card flash
  - Magic-link flow `/verify?email=...&mode=signIn&oobCode=...` — **`verifyEmailLink` fires exactly once under StrictMode** (check DevTools Network)
  - Empty `/verify` — immediate redirect, no flash

---

## refactor(web): UserBusinessDataContext — useMutation 替 manualError (#1922) (#1963)

- **SHA**: [72337a8e](https://github.com/SerendipityOneInc/ecap-workspace/commit/72337a8e3fad486fffd3edc8dd811ea041114188)
- **作者**: Chris@ZooClaw
- **日期**: 2026-05-27T04:06:34Z
- **PR**: #1922

### Commit Message

```
refactor(web): UserBusinessDataContext — useMutation 替 manualError (#1922) (#1963)

## Summary

把 `UserBusinessDataContext` 里的 `forceRefresh` 改造成 `useMutation`，让 error
由 TanStack Query 的状态机管理，彻底消除 `manualError` useState 与三个观察者
`useEffect`（React *You Might Not Need an Effect* bucket 1 anti-pattern）。

## 背景

issue #1922 指出文件里 4 个 `useEffect` 中有 3 个唯一职责是调用
`setManualError(null)`——属于 bucket 1 的派生 state 镜像。`manualError` 仅在
`forceRefresh` 的 catch/error 分支写入，本质上应该让 mutation state machine 管。

## 设计要点（Option A）

- **`useMutation` 接管 forceRefresh**：`mutationFn` 在 `!result.success` 时
throw，`onSuccess` 写 query cache；`error` 从 `mutation.error ??
query.error` 派生。
- **`mutation.reset()` 落点**改成事件/写者回调而非观察者 effect：
  - `auth-state-changed` sync handler — uid 变化清错
  - `refresh()` callback — 显式重新获取清错
- `onUserBusinessDataUpdate` 订阅回调 — 外部 push 清错（也顺带覆盖
`fetchUserBusinessData` 成功 dispatch 的 auto-refetch 路径，因为 cache 层对两个
fetch 都 dispatch event）
- **稳定引用**：`const { reset } = mutation` 解构出稳定的 reset，避免 mutation 对象
identity 抖动让 effect 反复重订阅。

## 覆盖矩阵

| 触发场景 | 清错机制 |
|---|---|
| forceRefresh 失败后再次 forceRefresh | `mutateAsync` 下一次调用自动清 |
| forceRefresh 失败 → refresh() | refresh() 入口显式 reset |
| forceRefresh 失败 → query 自动/显式 refetch 成功 | cache layer dispatch → 订阅回调
reset |
| forceRefresh 失败 → uid 变化 / 登出 | sync handler reset |
| forceRefresh 失败 → 外部 push update | 订阅回调 reset |

## 测试

- 老测试 11 (`forceRefresh() surfaces failures`) 把 `expect(...)` 包成
`waitFor` —— mutation 状态走 `useSyncExternalStore`，flush 比 `setState` 慢一个
microtask，`act` 退出后才可见。
- 新增 4 个 regression test，分别 lock 上面表里 4 个清错触发点。
- 5864 unit tests 全过；`tsc --noEmit` clean；`pnpm lint` clean。

## Acceptance（#1922）

- [x] 文件里没有 `useEffect` 含 `setManualError`（state 本身已删除）
- [x] error 仍然在 forceRefresh 成功、query refetch 成功、uid 变化、外部更新四种场景下正确隐藏
- [x] 登出时的 cache 清理保留（bucket-5 合法副作用）
- [x] Layer-3 W3 契约保留（无 `@/hooks/` 导入）

Closes #1922

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Description

Sub-issue of #1667 — case-by-case anti-pattern cleanup found during a fresh audit (not in #1667's original bucket list).

## File

\`web/app/src/contexts/UserBusinessDataContext.tsx\` — 4 \`useEffect\` total. Three of them exist solely to call \`setManualError(null)\` when query conditions change. Per [React's *You Might Not Need an Effect*](https://react.dev/learn/you-might-not-need-an-effect), this is bucket 1 (state that mirrors derived information) — the \`manualError\` state should be either eliminated or written in its own writer paths, not cleared from observer effects.

## Anti-patterns

### `UserBusinessDataContext.tsx:102-108` — bucket 1 (sync state to uid)

\`\`\`tsx
useEffect(() => {
  if (!uid) {
    setManualError(null)
    clearUserBusinessDataCache()
    queryClient.removeQueries({ queryKey: userBusinessDataKeys.all })
  }
}, [queryClient, uid])
\`\`\`

The cache clearing is a legitimate side effect (bucket 5 — clearing external cache when user logs out). The \`setManualError(null)\` part is bucket 1: \`manualError\` semantically belongs to a specific \`uid\`'s session and should be discarded with it.

### `UserBusinessDataContext.tsx:110-114` — bucket 1 (sync state to query success)

\`\`\`tsx
useEffect(() => {
  if (query.isSuccess) {
    setManualError(null)
  }
}, [query.isSuccess, query.data])
\`\`\`

This is the textbook bucket 1 anti-pattern: derived state stored separately. The \`error\` value at line 100 is already \`manualError ?? queryErrorMessage\` — a successful query naturally hides \`queryErrorMessage\`, but \`manualError\` is a stale flag that lingers.

### `UserBusinessDataContext.tsx:117-124` — bucket 5 (legitimate) + bucket 1 (clear inside)

The \`onUserBusinessDataUpdate\` subscription itself is legitimate (external system sync, bucket 5). The \`setManualError(null)\` line inside the callback is bucket 1 — clearing state to mirror \"a successful external update happened.\"

## Suggested refactor

**Option A (preferred): eliminate `manualError` state entirely.**

\`manualError\` is only written in \`forceRefresh\`'s catch / error branches. Two alternatives:

1. Convert \`forceRefresh\` to a \`useMutation\` — its \`error\` becomes part of TanStack Query's state machine, and \`mutation.reset()\` is called explicitly when refresh succeeds. The derived \`error\` exposed on the context becomes:
   \`\`\`tsx
   const error = forceRefreshMutation.error?.message ?? queryErrorMessage
   \`\`\`
   No effect needed. This aligns with the React Query migration v2 (#1796 / #1347).

2. If staying with \`useState\`, move the clears into the writer paths: \`forceRefresh\` already touches \`setManualError\` on failure — also set it to null on the success branch (line 89, after \`setQueryData\`). Same for the update event handler if a fresh push counts as \"manual error resolved.\" Then delete all three observer effects.

**Option B (minimal):** keep \`manualError\` state, but move the three clears into the writer paths described above. Net change: delete 3 effects, add ~3 \`setManualError(null)\` lines in existing functions.

The \`auth-state-changed\` subscription at line 49-53 is bucket 5 (legitimate external event sync) and should be preserved.

## Acceptance

- [ ] No \`useEffect\` in this file has \`setManualError\` (or equivalent) in its body.
- [ ] The exposed \`error\` value still correctly hides on \`forceRefresh\` success, on query refetch success, on uid change, and on external data update.
- [ ] Cache clearing on logout (line 105-106) is preserved — it's a real side effect.
- [ ] Layer-3 W3 contract preserved (no imports from \`hooks/\`).

## Related

- #1667 — umbrella useEffect anti-pattern tracker
- #1689 — OnboardingProvider backend status merge → \`useMemo\` pure derivation (same anti-pattern shape, already cleaned)
- #1796 / #1347 — React Query migration v2 (Option A aligns with this direction)
- \`web/app/CLAUDE.md\` → \`useEffect\` anti-patterns section

---

## feat(enterprise): add personal org bootstrap (#1947)

- **SHA**: [89399973](https://github.com/SerendipityOneInc/ecap-workspace/commit/89399973a65d946cd17d342e278971c853a99f24)
- **作者**: bill-srp
- **日期**: 2026-05-27T03:42:37Z
- **PR**: #1947

### Commit Message

```
feat(enterprise): add personal org bootstrap (#1947)

## Linear
https://linear.app/srpone/issue/ECA-827/support-team-wallet-user

## Summary
- Add an idempotent personal org creation API and web BFF/client
wrapper.
- Create org + admin membership transactionally, reusing an existing
account team_id for billing when present.
- Include org context in legacy user/create and user/get responses, and
only call createPersonalOrg from the frontend when the user response has
no org.

## Test plan
- [x] docker exec -w /workspaces/enterprise/services/claw-interface
enterprise-bill /home/node/.venvs/claw-interface/bin/ruff check .
- [x] docker exec -w /workspaces/enterprise/services/claw-interface
enterprise-bill /home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_org_repo.py tests/unit/test_routes_org.py
tests/unit/test_routes_account.py tests/unit/test_org_service.py
tests/unit/test_enterprise_wiring.py
tests/unit/test_user_enrichment_service.py
tests/unit/test_user_routes_coverage.py -q
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm
run lint
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm
exec tsc --noEmit
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm
exec vitest run tests/unit/lib/auth/manager.unit.spec.ts
tests/unit/lib/api/org.unit.spec.ts --config ./vitest.config.mts
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm
exec vitest run tests/unit/app/api/routes.unit.spec.ts -t
"/api/orgs/personal" --config ./vitest.config.mts

## Notes
- Full backend coverage run reached test completion but failed local
broad-suite coverage at 87.95% < 90 and also reported unrelated
full-suite failures/resource warnings.
- Full web unit run initially found the auth test setup issue fixed in
this branch; the other three admin hook timeouts passed when run
directly.
- web root lint failed on an existing generated coverage warning in
web/enterprise-admin/coverage/block-navigation.js; app-scoped lint
passed.
- web root tsc script failed because pnpm rejected --if-present in the
recursive exec script; app-scoped tsc passed.
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-827/support-team-wallet-user

## Summary
- Add an idempotent personal org creation API and web BFF/client wrapper.
- Create org + admin membership transactionally, reusing an existing account team_id for billing when present.
- Include org context in legacy user/create and user/get responses, and only call createPersonalOrg from the frontend when the user response has no org.

## Test plan
- [x] docker exec -w /workspaces/enterprise/services/claw-interface enterprise-bill /home/node/.venvs/claw-interface/bin/ruff check .
- [x] docker exec -w /workspaces/enterprise/services/claw-interface enterprise-bill /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_org_repo.py tests/unit/test_routes_org.py tests/unit/test_routes_account.py tests/unit/test_org_service.py tests/unit/test_enterprise_wiring.py tests/unit/test_user_enrichment_service.py tests/unit/test_user_routes_coverage.py -q
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm run lint
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm exec tsc --noEmit
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm exec vitest run tests/unit/lib/auth/manager.unit.spec.ts tests/unit/lib/api/org.unit.spec.ts --config ./vitest.config.mts
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm exec vitest run tests/unit/app/api/routes.unit.spec.ts -t "/api/orgs/personal" --config ./vitest.config.mts

## Notes
- Full backend coverage run reached test completion but failed local broad-suite coverage at 87.95% < 90 and also reported unrelated full-suite failures/resource warnings.
- Full web unit run initially found the auth test setup issue fixed in this branch; the other three admin hook timeouts passed when run directly.
- web root lint failed on an existing generated coverage warning in web/enterprise-admin/coverage/block-navigation.js; app-scoped lint passed.
- web root tsc script failed because pnpm rejected --if-present in the recursive exec script; app-scoped tsc passed.

---

