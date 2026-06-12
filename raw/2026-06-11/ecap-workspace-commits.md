# SerendipityOneInc/ecap-workspace commits — 2026-06-11

共 15 个 commits

---

## fix(dashboard): remove live write gate (#2387)

- **SHA**: `ae2139a7b2db6f8c3c0b0aaa089d935b59b2955f`
- **作者**: bill-srp
- **日期**: 2026-06-11T14:13:21Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/ae2139a7b2db6f8c3c0b0aaa089d935b59b2955f
- **PR**: #2387

### 完整 Commit Message

```
fix(dashboard): remove live write gate (#2387)

## Summary
- remove the dashboard-console LIVE_WRITES_ENABLED guard and deleted
live-writes.ts
- allow live create/update/submit/disable/approve flows to call real
backend/R2 paths
- add view-model tests covering live writes for create, submit, disable,
and approve

## Tests
- pnpm --dir web/dashboard-console test
app/routes/agent-packs/use-view-model.test.tsx
app/routes/agent-packs/submissions/use-view-model.test.tsx
app/lib/claw-api.test.ts app/routes/api/r2-upload.test.ts
- pnpm --dir web/dashboard-console lint
- pnpm --dir web/dashboard-console run typecheck
```

### PR 描述

## Summary
- remove the dashboard-console LIVE_WRITES_ENABLED guard and deleted live-writes.ts
- allow live create/update/submit/disable/approve flows to call real backend/R2 paths
- add view-model tests covering live writes for create, submit, disable, and approve

## Tests
- pnpm --dir web/dashboard-console test app/routes/agent-packs/use-view-model.test.tsx app/routes/agent-packs/submissions/use-view-model.test.tsx app/lib/claw-api.test.ts app/routes/api/r2-upload.test.ts
- pnpm --dir web/dashboard-console lint
- pnpm --dir web/dashboard-console run typecheck

---

## fix(pack-store): remove schema validation gate (#2386)

- **SHA**: `60ee183cde0646e33ec27354b8f6f11f5da4cec7`
- **作者**: bill-srp
- **日期**: 2026-06-11T13:45:28Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/60ee183cde0646e33ec27354b8f6f11f5da4cec7
- **PR**: #2386

### 完整 Commit Message

```
fix(pack-store): remove schema validation gate (#2386)

## Summary
- remove schema_validated from pack submission schemas and submit
requests
- stop rejecting submissions when schema validation is not confirmed
- update pack-store, internal agent-pack, and install-service tests for
the removed field

## Tests
- services/claw-interface: ruff format --check .
- services/claw-interface: ruff check .
- services/claw-interface: pyright app tests
- services/claw-interface: pytest targeted pack-store and agent-install
tests (97 passed)
```

### PR 描述

## Summary
- remove schema_validated from pack submission schemas and submit requests
- stop rejecting submissions when schema validation is not confirmed
- update pack-store, internal agent-pack, and install-service tests for the removed field

## Tests
- services/claw-interface: ruff format --check .
- services/claw-interface: ruff check .
- services/claw-interface: pyright app tests
- services/claw-interface: pytest targeted pack-store and agent-install tests (97 passed)

---

## feat(claw-interface): clean blocked trial runtime (#2385)

- **SHA**: `88c1d908b25cdb064d86cfdf27666c81ac4d663b`
- **作者**: kaka-srp
- **日期**: 2026-06-11T13:15:31Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/88c1d908b25cdb064d86cfdf27666c81ac4d663b
- **PR**: #2385

### 完整 Commit Message

```
feat(claw-interface): clean blocked trial runtime (#2385)

## Linear
https://linear.app/srpone/issue/ECA-975/clean-trial-payment-runtime

## Summary
- add a Billing v2 runtime cleanup helper guarded by current access so
only free/expired users are reclaimed
- add cleanup-trial-payment-runtime admin cron for failed Stripe trial
payment-method blocks and abandoned starter trial authorization orders
- add payment-order cleanup markers, candidate index definitions, cron
trigger docs, design spec, and unit coverage

## Test plan
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/ruff format --check .
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/ruff check .
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pyright app/ tests/
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_subscription_expiry.py
tests/unit/test_trial_payment_runtime_cleanup.py
tests/unit/test_admin_cron.py tests/unit/test_billing_v2_repos.py -q

## Rollout notes
- before enabling the external scheduler, manually create/verify the
Billing v2 payment-order index
`payment_trial_runtime_cleanup_candidates` on `provider, environment,
product_type, status, updated_at`
- configure external cron to POST
`/admin/cron/cleanup-trial-payment-runtime?batch_limit=500` every 5
minutes
```

### PR 描述

## Linear
https://linear.app/srpone/issue/ECA-975/clean-trial-payment-runtime

## Summary
- add a Billing v2 runtime cleanup helper guarded by current access so only free/expired users are reclaimed
- add cleanup-trial-payment-runtime admin cron for failed Stripe trial payment-method blocks and abandoned starter trial authorization orders
- add payment-order cleanup markers, candidate index definitions, cron trigger docs, design spec, and unit coverage

## Test plan
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/ruff format --check .
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/ruff check .
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pyright app/ tests/
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_subscription_expiry.py tests/unit/test_trial_payment_runtime_cleanup.py tests/unit/test_admin_cron.py tests/unit/test_billing_v2_repos.py -q

## Rollout notes
- before enabling the external scheduler, manually create/verify the Billing v2 payment-order index `payment_trial_runtime_cleanup_candidates` on `provider, environment, product_type, status, updated_at`
- configure external cron to POST `/admin/cron/cleanup-trial-payment-runtime?batch_limit=500` every 5 minutes

---

## fix(claw-interface): install specific agent submissions (#2379)

- **SHA**: `8e5e669681ab70df858db2092df613a275af1dc1`
- **作者**: bill-srp
- **日期**: 2026-06-11T12:56:22Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/8e5e669681ab70df858db2092df613a275af1dc1
- **PR**: #2379

### 完整 Commit Message

```
fix(claw-interface): install specific agent submissions (#2379)

## Summary
- Add a computer-scoped install endpoint for a specific existing agent
pack submission.
- When a submission id is provided, load that submission in the current
user org, then load its pack by `submission.pack_id` in the same org;
without a submission id, keep the direct official display-id pack
lookup.
- Reject submission-pinned installs if the loaded pack does not belong
to the current user org or does not match the requested agent display
id.
- Reuse the requested submission metadata when creating the installing
workspace and scheduling the background official-agent install.
- Normalize the submission-derived in-memory pack to `status="active"`
so the background installer can consume the exact submitted archive
without persisting an active status change to the backing pack row.
- Treat submission existence as the install contract: submitted,
approved, and rejected statuses are all valid exact-version install
targets if the submission exists for the user org pack.
- Do not require the base pack to be active on the submission-pinned
path; the active-pack gate still applies to display-id installs without
a submission id.
- Cover route registration, background scheduling, repository lookup,
org guard, background-install compatibility, and service-level
submission mapping with unit tests.

## Root cause
The existing normalized official-agent install flow always loaded the
current active pack row by display id. It did not expose a route that
lets callers request one existing submission version, so installs from
an explicit submission could not pin the workspace/background install to
that submission archive and metadata. The submission-specific path also
should not require a display-id pack lookup or active pack status before
the submission lookup, because the submission already carries the
canonical `pack_id` and exact archive metadata; it must, however, stay
scoped to the current user org and hand an installable in-memory pack to
the background installer.

## Test plan
- [x] `ruff format --check .`
- [x] `ruff check .`
- [x] `.venv/bin/pyright --pythonpath .venv/bin/python app tests`
- [x] `.venv/bin/pytest tests/unit/test_agent_install_service.py
tests/unit/test_pack_submission_repo.py tests/unit/test_agent_routes.py
tests/unit/test_enterprise_wiring.py -q`
- [x] `scripts/ci-lint/01-file-length.sh`
```

### PR 描述

## Summary
- Add a computer-scoped install endpoint for a specific existing agent pack submission.
- When a submission id is provided, load that submission in the current user org, then load its pack by `submission.pack_id` in the same org; without a submission id, keep the direct official display-id pack lookup.
- Reject submission-pinned installs if the loaded pack does not belong to the current user org or does not match the requested agent display id.
- Reuse the requested submission metadata when creating the installing workspace and scheduling the background official-agent install.
- Normalize the submission-derived in-memory pack to `status="active"` so the background installer can consume the exact submitted archive without persisting an active status change to the backing pack row.
- Treat submission existence as the install contract: submitted, approved, and rejected statuses are all valid exact-version install targets if the submission exists for the user org pack.
- Do not require the base pack to be active on the submission-pinned path; the active-pack gate still applies to display-id installs without a submission id.
- Cover route registration, background scheduling, repository lookup, org guard, background-install compatibility, and service-level submission mapping with unit tests.

## Root cause
The existing normalized official-agent install flow always loaded the current active pack row by display id. It did not expose a route that lets callers request one existing submission version, so installs from an explicit submission could not pin the workspace/background install to that submission archive and metadata. The submission-specific path also should not require a display-id pack lookup or active pack status before the submission lookup, because the submission already carries the canonical `pack_id` and exact archive metadata; it must, however, stay scoped to the current user org and hand an installable in-memory pack to the background installer.

## Test plan
- [x] `ruff format --check .`
- [x] `ruff check .`
- [x] `.venv/bin/pyright --pythonpath .venv/bin/python app tests`
- [x] `.venv/bin/pytest tests/unit/test_agent_install_service.py tests/unit/test_pack_submission_repo.py tests/unit/test_agent_routes.py tests/unit/test_enterprise_wiring.py -q`
- [x] `scripts/ci-lint/01-file-length.sh`



---

## fix(claw-interface): auto-triage ECA-883 (#2372)

- **SHA**: `3abda7ed496ad042cf32bdd73fbef03a676fb26c`
- **作者**: srp-claude-assistant[bot]
- **日期**: 2026-06-11T12:11:55Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/3abda7ed496ad042cf32bdd73fbef03a676fb26c
- **PR**: #2372

### 完整 Commit Message

```
fix(claw-interface): auto-triage ECA-883 (#2372)

## Linear issue

[ECA-883](https://linear.app/srpone/issue/ECA-883/openclaw-redeploy-fails-with-400-on-botsuuidstop)
— OpenClaw redeploy fails with 400 on /bots/{uuid}/stop

**Affected service**: `claw-interface`
**Triage LLM confidence**: 0.35 / 1.0
**Triage LLM verification cost**: low *(auto-PR gate passed)*

## Root cause
`claw-interface` redeploys a bot by calling FastClaw stop and then
start. FastClaw returns HTTP 400 with `bot is not running` when the bot
exists but is already in a non-running state, and `claw-interface`
treated that idempotent stop pre-state as fatal, so redeploy returned
500 before attempting the start that FastClaw would allow.

## Fix
- Handle only FastClaw's exact HTTP 400 `bot is not running` stop
response inside `OpenClawPlatformClient.redeploy_bot()` and continue to
`start_bot()`.
- Log the idempotent stop rejection as a warning, while logging
status/body and re-raising all other stop HTTP errors.
- Added unit coverage for the idempotent stop path and for
non-idempotent stop errors still aborting before start.

## Verification plan
1. Add response-body logging to the redeploy error handler so the next
400 occurrence captures the [claw.gsmo.ai](<http://claw.gsmo.ai>) error
message.
2. Once the body is known, either add a precondition state check (GET
/bots/{UUID}) before calling /stop, or add a catch-and-skip for the
idempotent case.
3. Test the redeploy path against a bot already in stopped state to
confirm the fix handles that lifecycle transition cleanly.

## Risks / scope
The recovery depends on FastClaw preserving the `bot is not running`
response contract for existing non-running bots. Reviewers should check
that no other 400 body should be treated as safe to continue, especially
bot-not-found or authorization failures.

---
*This PR was opened automatically by the ECAP error-scanner. The bug
report came from production telemetry; the analysis and fix candidate
were produced by an LLM. Please review carefully — the triage LLM marked
this as `verification_cost: low` (meaning CI should suffice), but human
judgment overrides.*

*Auto-merge is disabled for `auto-triage` labeled PRs; merging requires
explicit human approval.*

---------

Co-authored-by: ecap-error-scanner[bot] <ecap-error-scanner[bot]@users.noreply.github.com>
Co-authored-by: chris-srp <chris@srp.one>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR 描述

## Linear issue
[ECA-883](https://linear.app/srpone/issue/ECA-883/openclaw-redeploy-fails-with-400-on-botsuuidstop) — OpenClaw redeploy fails with 400 on /bots/{uuid}/stop

**Affected service**: `claw-interface`
**Triage LLM confidence**: 0.35 / 1.0
**Triage LLM verification cost**: low *(auto-PR gate passed)*

## Root cause
`claw-interface` redeploys a bot by calling FastClaw stop and then start. FastClaw returns HTTP 400 with `bot is not running` when the bot exists but is already in a non-running state, and `claw-interface` treated that idempotent stop pre-state as fatal, so redeploy returned 500 before attempting the start that FastClaw would allow.

## Fix
- Handle only FastClaw's exact HTTP 400 `bot is not running` stop response inside `OpenClawPlatformClient.redeploy_bot()` and continue to `start_bot()`.
- Log the idempotent stop rejection as a warning, while logging status/body and re-raising all other stop HTTP errors.
- Added unit coverage for the idempotent stop path and for non-idempotent stop errors still aborting before start.

## Verification plan
1. Add response-body logging to the redeploy error handler so the next 400 occurrence captures the [claw.gsmo.ai](<http://claw.gsmo.ai>) error message.
2. Once the body is known, either add a precondition state check (GET /bots/{UUID}) before calling /stop, or add a catch-and-skip for the idempotent case.
3. Test the redeploy path against a bot already in stopped state to confirm the fix handles that lifecycle transition cleanly.

## Risks / scope
The recovery depends on FastClaw preserving the `bot is not running` response contract for existing non-running bots. Reviewers should check that no other 400 body should be treated as safe to continue, especially bot-not-found or authorization failures.

---
*This PR was opened automatically by the ECAP error-scanner. The bug report came from production telemetry; the analysis and fix candidate were produced by an LLM. Please review carefully — the triage LLM marked this as `verification_cost: low` (meaning CI should suffice), but human judgment overrides.*

*Auto-merge is disabled for `auto-triage` labeled PRs; merging requires explicit human approval.*


---

## fix(sidenav): Direct Message 改名为 Session History 并把选中态从 agent 行挪到子入口 (#2371)

- **SHA**: `85bd2e43e021f2ffa47c3d1d14024bf9b85deb1b`
- **作者**: lynn-srp
- **日期**: 2026-06-11T11:51:19Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/85bd2e43e021f2ffa47c3d1d14024bf9b85deb1b
- **PR**: #2371

### 完整 Commit Message

```
fix(sidenav): Direct Message 改名为 Session History 并把选中态从 agent 行挪到子入口 (#2371)

## 概述
  修正 agent 侧边栏 accordion 里"会话入口"的三个 UX 问题：文案含糊、位置不直观、选中态贴错了对象。

  ## 改动清单
  1. **改名 + 调位置**
- 把 "Direct Message" 入口改名为 "Session History"，更准确地表达它指向"这个 agent
此前的（legacy 单
  session）历史聊天"。
- 从原本的第一项挪到 `+ New chat` 下方——优先级上 "+ New chat" 是动作（更主），Session History
是去向（更次）。
- 同步更新：i18n key `chat.directMessage` → `chat.sessionHistory`；testid
`nav-agent-direct-message-*` →
  `nav-agent-session-history-*`。

  2. **删掉 "No past sessions" 空状态**
     - 原文案与 Session History 入口的语义冲突：入口本身就承载着"这个 agent 有 legacy
  历史可去看"，再下面挂一行"无会话"会让人误以为没历史。
     - 干掉了空状态 `<p>` 渲染和 `chat.noPastSessions` i18n key。
- 已知限制：理想情况是"真的没有任何 chat 时才显示 'No past sessions'"，但
`useAgentConversations` 只返回新
multi-session 列表，无法判断 legacy 单 session 是否有数据；条件渲染需要后端补一个"this agent has
any chat history"的
   hint，到时再开 PR 加回来。

  3. **选中态归位**
- 之前 agent row 在 `/chat?agent_id=<id>` 或
`/chat/<computer>/<agent>/<session>` 路由下整行高亮——但 accordion
  模式下，agent row 只是 expand/collapse 触发器，不是导航目标，"被选中"概念应该落在真正的子入口上。
     - **Session History**：URL 是 `/chat?agent_id=<id>` 时高亮。
     - **session 条目**：URL 是 `/chat/<computer>/<agent>/<session>` 时该条目高亮。
     - **Agent row**：accordion 模式下不再有 selected 态；legacy
  模式（`useLegacyChatVersion=true`）下保留原行为，不破坏旧版用户。

  ## 涉及文件
- `web/app/src/components/sidenav/SideNavAgentList.tsx` — 5 行（accordion
模式下关掉 agent row 的 `isActive`）。
- `web/app/src/components/sidenav/SideNavAgentSessions.tsx` —
主要改动（rename + reorder + 空状态删除 + URL-derived
  active state）。
  - `web/app/src/locales/en.ts` — 替换 i18n key。
-
`web/app/tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx`
— 跟随更新 mock、翻转顺序断言、新增 3
  条 active state 测试。

  ## 验证
- [x] `/chat?agent_id=<id>` 展开对应 agent → Session History 灰底高亮、agent row
无高亮。
  - [x] `/new-chat` 展开任一 agent → Session History 无高亮、agent row 无高亮。
- [x] 点击 Session History → 路由跳到 `/chat?agent_id=<id>`，legacy 单 session
历史正常加载。
- [x] 单测覆盖三种 active state：路由匹配时 Session History 高亮、其它 agent 不高亮、session
条目按 session_id
  匹配高亮。
  - [ ] 等 CI `code-quality / lint-and-test` 跑过 lint 
<img width="3008" height="1562" alt="screenshot-20260611-173104"
src="https://github.com/user-attachments/assets/bdb1c22c-64dd-4091-aace-23d7e86a0302"
/>
+ tsc + 单测。

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR 描述

## 概述
  修正 agent 侧边栏 accordion 里"会话入口"的三个 UX 问题：文案含糊、位置不直观、选中态贴错了对象。

  ## 改动清单
  1. **改名 + 调位置**
     - 把 "Direct Message" 入口改名为 "Session History"，更准确地表达它指向"这个 agent 此前的（legacy 单
  session）历史聊天"。
     - 从原本的第一项挪到 `+ New chat` 下方——优先级上 "+ New chat" 是动作（更主），Session History 是去向（更次）。
     - 同步更新：i18n key `chat.directMessage` → `chat.sessionHistory`；testid `nav-agent-direct-message-*` →
  `nav-agent-session-history-*`。

  2. **删掉 "No past sessions" 空状态**
     - 原文案与 Session History 入口的语义冲突：入口本身就承载着"这个 agent 有 legacy
  历史可去看"，再下面挂一行"无会话"会让人误以为没历史。
     - 干掉了空状态 `<p>` 渲染和 `chat.noPastSessions` i18n key。
     - 已知限制：理想情况是"真的没有任何 chat 时才显示 'No past sessions'"，但 `useAgentConversations` 只返回新
  multi-session 列表，无法判断 legacy 单 session 是否有数据；条件渲染需要后端补一个"this agent has any chat history"的
   hint，到时再开 PR 加回来。

  3. **选中态归位**
     - 之前 agent row 在 `/chat?agent_id=<id>` 或 `/chat/<computer>/<agent>/<session>` 路由下整行高亮——但 accordion
  模式下，agent row 只是 expand/collapse 触发器，不是导航目标，"被选中"概念应该落在真正的子入口上。
     - **Session History**：URL 是 `/chat?agent_id=<id>` 时高亮。
     - **session 条目**：URL 是 `/chat/<computer>/<agent>/<session>` 时该条目高亮。
     - **Agent row**：accordion 模式下不再有 selected 态；legacy
  模式（`useLegacyChatVersion=true`）下保留原行为，不破坏旧版用户。

  ## 涉及文件
  - `web/app/src/components/sidenav/SideNavAgentList.tsx` — 5 行（accordion 模式下关掉 agent row 的 `isActive`）。
  - `web/app/src/components/sidenav/SideNavAgentSessions.tsx` — 主要改动（rename + reorder + 空状态删除 + URL-derived
  active state）。
  - `web/app/src/locales/en.ts` — 替换 i18n key。
  - `web/app/tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx` — 跟随更新 mock、翻转顺序断言、新增 3
  条 active state 测试。

  ## 验证
  - [x] `/chat?agent_id=<id>` 展开对应 agent → Session History 灰底高亮、agent row 无高亮。
  - [x] `/new-chat` 展开任一 agent → Session History 无高亮、agent row 无高亮。
  - [x] 点击 Session History → 路由跳到 `/chat?agent_id=<id>`，legacy 单 session 历史正常加载。
  - [x] 单测覆盖三种 active state：路由匹配时 Session History 高亮、其它 agent 不高亮、session 条目按 session_id
  匹配高亮。
  - [ ] 等 CI `code-quality / lint-and-test` 跑过 lint 
<img width="3008" height="1562" alt="screenshot-20260611-173104" src="https://github.com/user-attachments/assets/bdb1c22c-64dd-4091-aace-23d7e86a0302" />
+ tsc + 单测。

---

## fix(ecap-website): auto-triage ECA-671 (#2374)

- **SHA**: `383e408948d4320f95d433b1410a6d24b46360ed`
- **作者**: srp-claude-assistant[bot]
- **日期**: 2026-06-11T11:45:31Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/383e408948d4320f95d433b1410a6d24b46360ed
- **PR**: #2374

### 完整 Commit Message

```
fix(ecap-website): auto-triage ECA-671 (#2374)

## Linear issue

[ECA-671](https://linear.app/srpone/issue/ECA-671/frontend-mattermosterror-image-dimension-exceeds-upload-limit)
— Frontend MattermostError: image dimension exceeds upload limit

**Affected service**: `ecap-website`

## Root cause
The Mattermost attachment upload path validated file size and count in
`GenClawInput`, but not image pixel dimensions. Images above the
server's `FileSettings.MaxImageResolution` were uploaded, rejected with
a 400 `MattermostError`, and reported to Sentry by `useMmAttachments` as
if they were unexpected upload failures.

## Fix (reworked after review)
The original auto-fix hardcoded a client-side limit and rejected
oversized images. That was reworked per human review:

- **Auto-downscale instead of reject**: images above the limit are
downscaled client-side (aspect-preserving, `createImageBitmap` + canvas;
JPEG q0.9, PNG kept as PNG, GIFs skipped to preserve animation) and
uploaded successfully — same precedent as the existing HEIC→JPEG
normalization.
- **Corrected the limit**: Mattermost's default `MaxImageResolution` is
**33,177,600 px (7680×4320)**, not 6048×4032 as the original PR claimed.
The wrong constant would have blocked 24.4–33.2MP images the server
accepts.
- **Server-authoritative backstop**: the limit is server-configurable
and *not* exposed via `/api/v4/config/client` (verified in
`mattermost/server/config/client.go`), so `uploadFile` now captures the
machine-readable error id (`MattermostError.serverErrorId`) and
dimension rejections trigger retries at halved pixel budgets (default →
1/2 → 1/4). This covers deployments configured below the default.
- **Sentry policy**: in-loop dimension rejections are expected and stay
out of Sentry. An exhausted downgrade sequence (server rejects even 1/4
of the default) is unexpected and **is** reported via `captureChatError`
with `imageDowngradeExhausted: true` and the attempted budgets.
- Exhausted-downgrade failures render a non-retryable "Image too large"
chip (manual retry is pointless — automatic downgrades already ran).

## Verification
- 9 new unit tests for `downscaleImageToMmLimit` (scaling math, aspect
ratio, PNG/JPEG/GIF handling, fail-open paths).
- Hook tests for: downscaled upload, downgrade-retry success,
exhausted-downgrade reporting, re-attach path, non-retryable failure.
- `serverErrorId` propagation test in the MM API spec.
- Full unit suite (7103 tests), `tsc --noEmit`, `lint:ci` (knip
dep-health gate that failed before), and jscpd all pass locally.

## Risks / scope
- The 33,177,600 baseline matches MM defaults (our deployment's
`MaxFileSize` copy also matches defaults); if a server is configured
lower, the downgrade loop absorbs it at the cost of one extra upload
round-trip.
- Canvas re-encode drops EXIF metadata (orientation is baked in by
`createImageBitmap`); acceptable for chat attachments.

---
*This PR was opened automatically by the ECAP error-scanner and
subsequently reworked under human review.*

*Auto-merge is disabled for `auto-triage` labeled PRs; merging requires
explicit human approval.*

---------

Co-authored-by: ecap-error-scanner[bot] <ecap-error-scanner[bot]@users.noreply.github.com>
Co-authored-by: chris-srp <chris@srp.one>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR 描述

## Linear issue
[ECA-671](https://linear.app/srpone/issue/ECA-671/frontend-mattermosterror-image-dimension-exceeds-upload-limit) — Frontend MattermostError: image dimension exceeds upload limit

**Affected service**: `ecap-website`

## Root cause
The Mattermost attachment upload path validated file size and count in `GenClawInput`, but not image pixel dimensions. Images above the server's `FileSettings.MaxImageResolution` were uploaded, rejected with a 400 `MattermostError`, and reported to Sentry by `useMmAttachments` as if they were unexpected upload failures.

## Fix (reworked after review)
The original auto-fix hardcoded a client-side limit and rejected oversized images. That was reworked per human review:

- **Auto-downscale instead of reject**: images above the limit are downscaled client-side (aspect-preserving, `createImageBitmap` + canvas; JPEG q0.9, PNG kept as PNG, GIFs skipped to preserve animation) and uploaded successfully — same precedent as the existing HEIC→JPEG normalization.
- **Corrected the limit**: Mattermost's default `MaxImageResolution` is **33,177,600 px (7680×4320)**, not 6048×4032 as the original PR claimed. The wrong constant would have blocked 24.4–33.2MP images the server accepts.
- **Server-authoritative backstop**: the limit is server-configurable and *not* exposed via `/api/v4/config/client` (verified in `mattermost/server/config/client.go`), so `uploadFile` now captures the machine-readable error id (`MattermostError.serverErrorId`) and dimension rejections trigger retries at halved pixel budgets (default → 1/2 → 1/4). This covers deployments configured below the default.
- **Sentry policy**: in-loop dimension rejections are expected and stay out of Sentry. An exhausted downgrade sequence (server rejects even 1/4 of the default) is unexpected and **is** reported via `captureChatError` with `imageDowngradeExhausted: true` and the attempted budgets.
- Exhausted-downgrade failures render a non-retryable "Image too large" chip (manual retry is pointless — automatic downgrades already ran).

## Verification
- 9 new unit tests for `downscaleImageToMmLimit` (scaling math, aspect ratio, PNG/JPEG/GIF handling, fail-open paths).
- Hook tests for: downscaled upload, downgrade-retry success, exhausted-downgrade reporting, re-attach path, non-retryable failure.
- `serverErrorId` propagation test in the MM API spec.
- Full unit suite (7103 tests), `tsc --noEmit`, `lint:ci` (knip dep-health gate that failed before), and jscpd all pass locally.

## Risks / scope
- The 33,177,600 baseline matches MM defaults (our deployment's `MaxFileSize` copy also matches defaults); if a server is configured lower, the downgrade loop absorbs it at the cost of one extra upload round-trip.
- Canvas re-encode drops EXIF metadata (orientation is baked in by `createImageBitmap`); acceptable for chat attachments.

---
*This PR was opened automatically by the ECAP error-scanner and subsequently reworked under human review.*

*Auto-merge is disabled for `auto-triage` labeled PRs; merging requires explicit human approval.*


---

## fix(ecap-website): auto-triage ECA-821 (#2373)

- **SHA**: `2349717df483b9fb11da30fdaa394f418e24a5bf`
- **作者**: srp-claude-assistant[bot]
- **日期**: 2026-06-11T11:06:48Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/2349717df483b9fb11da30fdaa394f418e24a5bf
- **PR**: #2373

### 完整 Commit Message

```
fix(ecap-website): auto-triage ECA-821 (#2373)

## Linear issue

[ECA-821](https://linear.app/srpone/issue/ECA-821/frontend-http-422-errors-from-ecap-website)
— Frontend HTTP 422 errors from ecap-website

**Affected service**: `ecap-website`
**Triage LLM confidence**: 0.2 / 1.0
**Triage LLM verification cost**: low *(auto-PR gate passed)*

## Root cause
The chat replay share UI allowed users to select every currently visible
Mattermost message and submit all selected post IDs to `POST
/api/chat-replays`, while `claw-interface` validates `post_ids` with a
hard maximum of 200. Long conversations could therefore send more than
200 IDs in both `postIds` and `orderedMessageIds`, causing
FastAPI/Pydantic to reject the request with HTTP 422.

## Fix
- Mirrored the backend's 200-post replay share limit in the frontend
`useChatReplayShare` flow.
- Capped the "select visible" action to the first 200 visible shareable
messages and surfaced an actionable selection-limit error.
- Added a defensive create-time guard so oversized selections cannot
call `createReplay`.
- Added unit coverage for capped select-visible behavior and the
no-request oversized-create guard.

## Verification plan
1. Open Sentry event ECAP-WEBSITE-N6 for the full trace and request
context.
2. Retrieve the FastAPI 422 response body from backend logs to see which
field validation failed.
3. Reproduce the failing request locally.
4. Verify the fix eliminates the 422 response; confirm with a targeted
unit/integration test on the affected endpoint.

## Risks / scope
Users sharing very long conversations now get only the first 200 visible
selected messages when using "select all visible"; they must manually
narrow or load a smaller range if they need a different subset.
Reviewers should check that the selected order still matches display
order and that the client-side limit remains aligned with
`MAX_SELECTED_POSTS` in the backend schema.

---
*This PR was opened automatically by the ECAP error-scanner. The bug
report came from production telemetry; the analysis and fix candidate
were produced by an LLM. Please review carefully — the triage LLM marked
this as `verification_cost: low` (meaning CI should suffice), but human
judgment overrides.*

*Auto-merge is disabled for `auto-triage` labeled PRs; merging requires
explicit human approval.*

---------

Co-authored-by: ecap-error-scanner[bot] <ecap-error-scanner[bot]@users.noreply.github.com>
Co-authored-by: chris-srp <chris@srp.one>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR 描述

## Linear issue
[ECA-821](https://linear.app/srpone/issue/ECA-821/frontend-http-422-errors-from-ecap-website) — Frontend HTTP 422 errors from ecap-website

**Affected service**: `ecap-website`
**Triage LLM confidence**: 0.2 / 1.0
**Triage LLM verification cost**: low *(auto-PR gate passed)*

## Root cause
The chat replay share UI allowed users to select every currently visible Mattermost message and submit all selected post IDs to `POST /api/chat-replays`, while `claw-interface` validates `post_ids` with a hard maximum of 200. Long conversations could therefore send more than 200 IDs in both `postIds` and `orderedMessageIds`, causing FastAPI/Pydantic to reject the request with HTTP 422.

## Fix
- Mirrored the backend's 200-post replay share limit in the frontend `useChatReplayShare` flow.
- Capped the "select visible" action to the first 200 visible shareable messages and surfaced an actionable selection-limit error.
- Added a defensive create-time guard so oversized selections cannot call `createReplay`.
- Added unit coverage for capped select-visible behavior and the no-request oversized-create guard.

## Verification plan
1. Open Sentry event ECAP-WEBSITE-N6 for the full trace and request context.
2. Retrieve the FastAPI 422 response body from backend logs to see which field validation failed.
3. Reproduce the failing request locally.
4. Verify the fix eliminates the 422 response; confirm with a targeted unit/integration test on the affected endpoint.

## Risks / scope
Users sharing very long conversations now get only the first 200 visible selected messages when using "select all visible"; they must manually narrow or load a smaller range if they need a different subset. Reviewers should check that the selected order still matches display order and that the client-side limit remains aligned with `MAX_SELECTED_POSTS` in the backend schema.

---
*This PR was opened automatically by the ECAP error-scanner. The bug report came from production telemetry; the analysis and fix candidate were produced by an LLM. Please review carefully — the triage LLM marked this as `verification_cost: low` (meaning CI should suffice), but human judgment overrides.*

*Auto-merge is disabled for `auto-triage` labeled PRs; merging requires explicit human approval.*


---

## fix(web): govern Sentry reporting (#2375)

- **SHA**: `b744d890a62fc0afd8102f8d0ba6d62f780378dd`
- **作者**: chris-srp
- **日期**: 2026-06-11T11:04:21Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/b744d890a62fc0afd8102f8d0ba6d62f780378dd
- **PR**: #2375

### 完整 Commit Message

```
fix(web): govern Sentry reporting (#2375)

## Summary
- Add shared Sentry sanitization helpers for URL/header/context data and
mask+hash user email/phone identifiers.
- Route React Query query/mutation failures through one Sentry monitor
instead of per-hook useEffect reporting.
- Add explicit API/webhook monitors for critical OpenClaw, admin,
integration, and payment webhook routes, while filtering expected 4xx
noise.
- Split Sentry taxonomy so payment, webhook, and OpenClaw init/control
reporting live in separate helpers, and set Sentry release from
NEXT_PUBLIC_APP_VERSION.

## Root cause
Sentry reporting was spread across direct calls, route-local code, and
hook useEffect blocks. That made query errors easy to double-report,
mixed payment/webhook/OpenClaw taxonomy, and risked sending raw user
identifiers or unsanitized request data.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/lib/sentry/sanitize.unit.spec.ts
tests/unit/lib/sentry/react-query-monitor.unit.spec.ts
tests/unit/lib/sentry/api-monitor.unit.spec.ts
tests/unit/lib/sentry/webhook-monitor.unit.spec.ts
tests/unit/lib/sentry/openclaw-monitor-init.unit.spec.ts
tests/unit/lib/sentry/payment-monitor.unit.spec.ts
tests/unit/lib/sentry/user-identity.unit.spec.ts
tests/unit/config/sentry-client-config.unit.spec.ts
tests/unit/lib/query/query-client.unit.spec.ts
tests/unit/app/chat/useChatIdentity.unit.spec.tsx
tests/unit/sentry/network-monitor.unit.spec.ts
tests/unit/hooks/useSSEStream.unit.spec.ts
tests/unit/hooks/useOpenClawInit-extras.unit.spec.ts

Note: pnpm --dir web run tsc currently fails before typechecking because
the existing script invokes pnpm exec with --if-present in a way this
pnpm version rejects. The changed package was verified with web/app tsc
above.
```

### PR 描述

## Summary
- Add shared Sentry sanitization helpers for URL/header/context data and mask+hash user email/phone identifiers.
- Route React Query query/mutation failures through one Sentry monitor instead of per-hook useEffect reporting.
- Add explicit API/webhook monitors for critical OpenClaw, admin, integration, and payment webhook routes, while filtering expected 4xx noise.
- Split Sentry taxonomy so payment, webhook, and OpenClaw init/control reporting live in separate helpers, and set Sentry release from NEXT_PUBLIC_APP_VERSION.

## Root cause
Sentry reporting was spread across direct calls, route-local code, and hook useEffect blocks. That made query errors easy to double-report, mixed payment/webhook/OpenClaw taxonomy, and risked sending raw user identifiers or unsanitized request data.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/lib/sentry/sanitize.unit.spec.ts tests/unit/lib/sentry/react-query-monitor.unit.spec.ts tests/unit/lib/sentry/api-monitor.unit.spec.ts tests/unit/lib/sentry/webhook-monitor.unit.spec.ts tests/unit/lib/sentry/openclaw-monitor-init.unit.spec.ts tests/unit/lib/sentry/payment-monitor.unit.spec.ts tests/unit/lib/sentry/user-identity.unit.spec.ts tests/unit/config/sentry-client-config.unit.spec.ts tests/unit/lib/query/query-client.unit.spec.ts tests/unit/app/chat/useChatIdentity.unit.spec.tsx tests/unit/sentry/network-monitor.unit.spec.ts tests/unit/hooks/useSSEStream.unit.spec.ts tests/unit/hooks/useOpenClawInit-extras.unit.spec.ts

Note: pnpm --dir web run tsc currently fails before typechecking because the existing script invokes pnpm exec with --if-present in a way this pnpm version rejects. The changed package was verified with web/app tsc above.

---

## fix(desktop-node): heal agent-operator pairing (server-seeded) and surface real node command errors (#2369)

- **SHA**: `3ed0fe94f0442b523aff13931724df772aa3cb88`
- **作者**: zayne-srp
- **日期**: 2026-06-11T10:17:44Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/3ed0fe94f0442b523aff13931724df772aa3cb88
- **PR**: #2369

### 完整 Commit Message

```
fix(desktop-node): heal agent-operator pairing (server-seeded) and surface real node command errors (#2369)

## Summary
本 PR 包含 `heal-agent-operator-pairing` 分支的全部工作(此前一直未开 PR),共三块:

**1. Server-seeded desktop pairing(核心)**
- claw-interface: `desktop-pair` 路由 + schema + `desktop_node_pairing` 服务
—— 一次调用在 bot gateway 上 seed device + node pairing,返回连接目标和 device
token;并在 desktop-node approve 时自愈 bot 的 agent operator pairing
- desktop: `loadLocalIdentity()` / `applyServerPairing()` —— app 上报
deviceId + Ed25519 公钥,持久化 server 返回的 pairing,auto-connect 走 seeded
pairing 而非 bootstrap
- web: `/api/openclaw/settings/desktop-pair` 代理路由(含
`DESKTOP_PAIR_BACKEND_URL` devcontainer 调试逃生口)

**2. node.* 命令命名空间**
- desktop 节点命令统一 `node.*` 前缀,避免与 gateway 内置 file-transfer
命令(`dir.list`/`file.fetch`)冲突;按 uid 区分缓存 pairing,换账号自动重新配对

**3. node.invoke.result 错误格式修复**
- 失败回包改为协议要求的**顶层** `error: { code, message }`(此前嵌在 `payload.error`
里,gateway 读不到,所有命令失败都显示成不透明的 `node invoke failed`)

## Root cause(第 3 块)
`connection.ts` 的 invoke-dispatch 是 vendor 后补写的,未对照 gateway
协议(`NodeInvokeResultParamsSchema`):错误字符串被塞进 `payload.error`,而 gateway 的
`respondUnavailableOnNodeInvokeError` 只读顶层 `error.message`,读不到就兜底 `"node
invoke failed"`,真实失败原因(如 `old_string not found in file`)被吞掉。

## Test plan
- [x] desktop `tsc --noEmit` 通过(含 pairing 改动)
- [x] invoke 回包新格式用 openclaw gateway 真实 ajv
schema(`validateNodeInvokeResultParams`)校验通过,失败帧 `error.message` 可透传
- [x] `fsEdit` handler 冒烟:替换成功 / old_string 不存在 / 不唯一 / replace_all /
缺参数,行为全部正确
- [x] claw-interface 单测已随分支 commit
更新(`test_openclaw_settings_routes.py`),CI `python-code-quality` 验证
- [ ] 重启 desktop dev 后端到端验证:server-seeded pairing 自动连接 + `node.fs.edit`
失败时 bot 显示具体错误

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

### PR 描述

## Summary
本 PR 包含 `heal-agent-operator-pairing` 分支的全部工作(此前一直未开 PR),共三块:

**1. Server-seeded desktop pairing(核心)**
- claw-interface: `desktop-pair` 路由 + schema + `desktop_node_pairing` 服务 —— 一次调用在 bot gateway 上 seed device + node pairing,返回连接目标和 device token;并在 desktop-node approve 时自愈 bot 的 agent operator pairing
- desktop: `loadLocalIdentity()` / `applyServerPairing()` —— app 上报 deviceId + Ed25519 公钥,持久化 server 返回的 pairing,auto-connect 走 seeded pairing 而非 bootstrap
- web: `/api/openclaw/settings/desktop-pair` 代理路由(含 `DESKTOP_PAIR_BACKEND_URL` devcontainer 调试逃生口)

**2. node.* 命令命名空间**
- desktop 节点命令统一 `node.*` 前缀,避免与 gateway 内置 file-transfer 命令(`dir.list`/`file.fetch`)冲突;按 uid 区分缓存 pairing,换账号自动重新配对

**3. node.invoke.result 错误格式修复**
- 失败回包改为协议要求的**顶层** `error: { code, message }`(此前嵌在 `payload.error` 里,gateway 读不到,所有命令失败都显示成不透明的 `node invoke failed`)

## Root cause(第 3 块)
`connection.ts` 的 invoke-dispatch 是 vendor 后补写的,未对照 gateway 协议(`NodeInvokeResultParamsSchema`):错误字符串被塞进 `payload.error`,而 gateway 的 `respondUnavailableOnNodeInvokeError` 只读顶层 `error.message`,读不到就兜底 `"node invoke failed"`,真实失败原因(如 `old_string not found in file`)被吞掉。

## Test plan
- [x] desktop `tsc --noEmit` 通过(含 pairing 改动)
- [x] invoke 回包新格式用 openclaw gateway 真实 ajv schema(`validateNodeInvokeResultParams`)校验通过,失败帧 `error.message` 可透传
- [x] `fsEdit` handler 冒烟:替换成功 / old_string 不存在 / 不唯一 / replace_all / 缺参数,行为全部正确
- [x] claw-interface 单测已随分支 commit 更新(`test_openclaw_settings_routes.py`),CI `python-code-quality` 验证
- [ ] 重启 desktop dev 后端到端验证:server-seeded pairing 自动连接 + `node.fs.edit` 失败时 bot 显示具体错误

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(payments): add Stripe trial authorization guard (#2370)

- **SHA**: `eea236e5c5221f7bf884d8cfc892d2f959d21bf1`
- **作者**: kaka-srp
- **日期**: 2026-06-11T10:00:07Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/eea236e5c5221f7bf884d8cfc892d2f959d21bf1
- **PR**: #2370

### 完整 Commit Message

```
feat(payments): add Stripe trial authorization guard (#2370)

## Linear
https://linear.app/srpone/issue/ECA-972/stripe-trial-authorization-guard

## Summary
- Add Stripe starter-trial manual authorization Checkout: authorize the
configured small amount, cancel it immediately, then create the real
trial subscription only after verification.
- Tighten trial guard behavior: default card fingerprint threshold to 3,
block postal-code check failures, add UID cooldown after
fingerprint-limit blocks, and treat duplicate cancel 404s as idempotent
success.
- Update frontend checkout/session handling so trial-denied orders stop
before paid Checkout, trial verification failures show generic
user-facing copy, and `/chat` return failures surface a toast.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/ruff format --check .`
- [x] `/home/node/.venvs/claw-interface/bin/ruff check .`
- [x] `/home/node/.venvs/claw-interface/bin/pyright app tests`
- [x] `/home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_stripe_billing_v2.py tests/unit/test_stripe_client.py
tests/unit/test_billing_v2_order_requests.py
tests/unit/test_payment_validation.py -q`
- [x] `pnpm --dir web/app exec vitest run
tests/unit/lib/payment/handle-payment-success.unit.spec.ts
tests/unit/app/subscription/SuccessClient.unit.spec.tsx
tests/unit/app/chat/useChatPaymentReturn.unit.spec.ts
tests/unit/components/PaywallContent.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx
tests/unit/app/api/stripe-create-checkout-session.unit.spec.ts`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web/app run lint`
- [x] `git diff --check`
```

### PR 描述

## Linear
https://linear.app/srpone/issue/ECA-972/stripe-trial-authorization-guard

## Summary
- Add Stripe starter-trial manual authorization Checkout: authorize the configured small amount, cancel it immediately, then create the real trial subscription only after verification.
- Tighten trial guard behavior: default card fingerprint threshold to 3, block postal-code check failures, add UID cooldown after fingerprint-limit blocks, and treat duplicate cancel 404s as idempotent success.
- Update frontend checkout/session handling so trial-denied orders stop before paid Checkout, trial verification failures show generic user-facing copy, and `/chat` return failures surface a toast.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/ruff format --check .`
- [x] `/home/node/.venvs/claw-interface/bin/ruff check .`
- [x] `/home/node/.venvs/claw-interface/bin/pyright app tests`
- [x] `/home/node/.venvs/claw-interface/bin/pytest tests/unit/test_stripe_billing_v2.py tests/unit/test_stripe_client.py tests/unit/test_billing_v2_order_requests.py tests/unit/test_payment_validation.py -q`
- [x] `pnpm --dir web/app exec vitest run tests/unit/lib/payment/handle-payment-success.unit.spec.ts tests/unit/app/subscription/SuccessClient.unit.spec.tsx tests/unit/app/chat/useChatPaymentReturn.unit.spec.ts tests/unit/components/PaywallContent.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx tests/unit/app/api/stripe-create-checkout-session.unit.spec.ts`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web/app run lint`
- [x] `git diff --check`


---

## fix(claw-interface): harden agent workspace lifecycle (#2366)

- **SHA**: `0e3cab2a5e32f79d4592252b8e82f2709be53503`
- **作者**: bill-srp
- **日期**: 2026-06-11T09:10:31Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/0e3cab2a5e32f79d4592252b8e82f2709be53503
- **PR**: #2366

### 完整 Commit Message

```
fix(claw-interface): harden agent workspace lifecycle (#2366)

## Summary
- Allow V2 computer-scoped uninstall to operate on non-official agent
workspaces now that uninstall cleanup is source-agnostic.
- Switch official agent-pack runtime downloads from urllib to requests
while preserving auth headers, streaming writes, diagnostics, and HTTP
error logging.

## Root cause
- The V2 uninstall route still rejected non-official workspace rows even
though the cleanup path is shared across sources.
- Official pack downloads used urllib inside the bot runtime, which did
not match the requested requests-based HTTP behavior.

## Test plan
- [x] /Users/bill/.venvs/claw-interface/bin/python -m ruff format
--check .
- [x] /Users/bill/.venvs/claw-interface/bin/python -m ruff check .
- [x] /Users/bill/.venvs/claw-interface/bin/python -m pyright
--pythonpath /Users/bill/.venvs/claw-interface/bin/python app tests
- [x]
PYTHONPATH=/Users/bill/Github/StarQuestAI/ecap-workspace-agent-install/services/claw-interface
/Users/bill/.venvs/claw-interface/bin/python -m pytest -c pyproject.toml
tests/unit/test_agent_install_service.py
tests/unit/test_agent_uninstall_service.py
tests/unit/test_agent_routes.py -q
```

### PR 描述

## Summary
- Allow V2 computer-scoped uninstall to operate on non-official agent workspaces now that uninstall cleanup is source-agnostic.
- Switch official agent-pack runtime downloads from urllib to requests while preserving auth headers, streaming writes, diagnostics, and HTTP error logging.

## Root cause
- The V2 uninstall route still rejected non-official workspace rows even though the cleanup path is shared across sources.
- Official pack downloads used urllib inside the bot runtime, which did not match the requested requests-based HTTP behavior.

## Test plan
- [x] /Users/bill/.venvs/claw-interface/bin/python -m ruff format --check .
- [x] /Users/bill/.venvs/claw-interface/bin/python -m ruff check .
- [x] /Users/bill/.venvs/claw-interface/bin/python -m pyright --pythonpath /Users/bill/.venvs/claw-interface/bin/python app tests
- [x] PYTHONPATH=/Users/bill/Github/StarQuestAI/ecap-workspace-agent-install/services/claw-interface /Users/bill/.venvs/claw-interface/bin/python -m pytest -c pyproject.toml tests/unit/test_agent_install_service.py tests/unit/test_agent_uninstall_service.py tests/unit/test_agent_routes.py -q

---

## chore: add sentry memory rollup alert (#2367)

- **SHA**: `7ddeeaf806067018f87c3dfd8d90190435518500`
- **作者**: chris-srp
- **日期**: 2026-06-11T08:57:08Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/7ddeeaf806067018f87c3dfd8d90190435518500
- **PR**: #2367

### 完整 Commit Message

```
chore: add sentry memory rollup alert (#2367)

## Summary
- Add a Sentry memory rollup checker that counts browser memory-pressure
users from Sentry.
- Run the production checker once per day at 09:17 Asia/Shanghai and
always send a ZooClaw dev-group status message, including normal runs.
- Create synthetic Sentry issues only when absolute memory-pressure
user-count thresholds are newly exceeded, with 24h scope/level dedupe.
- Keep sampled active trace-user counts in the daily message as context
only; they are not linearly scaled or used as issue-triggering ratio
thresholds.
- Harden Sentry SDK usage by pinning v2, using new_scope(), and
initializing the SDK once before the breach capture loop.
- Cover normal, all-new, all-deduped, mixed new/deduped, dry-run,
output, and SDK lifecycle paths with focused tests.

## Test plan
- [x] python3 -m pytest tests/scripts/test_sentry_memory_rollup.py -q
- [x] python3 -m py_compile scripts/sentry_memory_rollup.py
tests/scripts/test_sentry_memory_rollup.py
- [x] ruby -e "require \"yaml\";
YAML.load_file(\".github/workflows/sentry-memory-rollup.yml\"); puts
\"workflow yaml ok\""
- [x] Sentry production dry-run: all 3 pressure / 255 sampled active
trace users, chat 2 / 144, claw-settings 0 / 33; normal message, no
thresholds exceeded
- [x] Sentry Explore production check: memory events carry parameterized
transactions, including /:locale/chat with 2 unique users and
/:locale/agents-manager with 1 unique user in the last 24h
```

### PR 描述

## Summary
- Add a Sentry memory rollup checker that counts browser memory-pressure users from Sentry.
- Run the production checker once per day at 09:17 Asia/Shanghai and always send a ZooClaw dev-group status message, including normal runs.
- Create synthetic Sentry issues only when absolute memory-pressure user-count thresholds are newly exceeded, with 24h scope/level dedupe.
- Keep sampled active trace-user counts in the daily message as context only; they are not linearly scaled or used as issue-triggering ratio thresholds.
- Harden Sentry SDK usage by pinning v2, using new_scope(), and initializing the SDK once before the breach capture loop.
- Cover normal, all-new, all-deduped, mixed new/deduped, dry-run, output, and SDK lifecycle paths with focused tests.

## Test plan
- [x] python3 -m pytest tests/scripts/test_sentry_memory_rollup.py -q
- [x] python3 -m py_compile scripts/sentry_memory_rollup.py tests/scripts/test_sentry_memory_rollup.py
- [x] ruby -e "require \"yaml\"; YAML.load_file(\".github/workflows/sentry-memory-rollup.yml\"); puts \"workflow yaml ok\""
- [x] Sentry production dry-run: all 3 pressure / 255 sampled active trace users, chat 2 / 144, claw-settings 0 / 33; normal message, no thresholds exceeded
- [x] Sentry Explore production check: memory events carry parameterized transactions, including /:locale/chat with 2 unique users and /:locale/agents-manager with 1 unique user in the last 24h

---

## feat(billing): add enterprise vertical pack subscriptions (#2365)

- **SHA**: `f4b91a33c55f455d3ca852007de2d6c46e0c8957`
- **作者**: bill-srp
- **日期**: 2026-06-11T08:31:40Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/f4b91a33c55f455d3ca852007de2d6c46e0c8957
- **PR**: #2365

### 完整 Commit Message

```
feat(billing): add enterprise vertical pack subscriptions (#2365)

## Linear


https://linear.app/srpone/issue/ECA-956/enterprise-vertical-pack-subscriptions

## Summary
- Add Billing v2 enterprise package subscription records, checkout,
renewal, expiry, and scheduled package-change handling.
- Add vertical pack plan purchase flow plus internal Stripe
product/price helper APIs.
- Cover Stripe/Antom payment flows, vertical pack plan/package services,
and route contracts with targeted unit tests.

## Test plan
- [x] cd services/claw-interface && .venv/bin/ruff format --check .
- [x] cd services/claw-interface && .venv/bin/ruff check .
- [x] cd services/claw-interface && uv tool run pyright --pythonpath
.venv/bin/python app tests
- [x] cd services/claw-interface && .venv/bin/python -m pytest
tests/unit/test_enterprise_package_subscription.py
tests/unit/test_vertical_pack_package_service.py
tests/unit/test_vertical_pack_plan_service.py
tests/unit/test_vertical_pack_plans_routes.py
tests/unit/test_internal_stripe_resources.py
tests/unit/test_internal_vertical_pack_plans_routes.py
tests/unit/test_antom_billing_v2_checkout.py
tests/unit/test_billing_v2_pending_entitlements.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_billing_v2_expiry.py tests/unit/test_stripe_client.py -q

---------

Co-authored-by: kaka-srp <kaka@srp.one>
```

### PR 描述

## Linear

https://linear.app/srpone/issue/ECA-956/enterprise-vertical-pack-subscriptions

## Summary
- Add Billing v2 enterprise package subscription records, checkout, renewal, expiry, and scheduled package-change handling.
- Add vertical pack plan purchase flow plus internal Stripe product/price helper APIs.
- Cover Stripe/Antom payment flows, vertical pack plan/package services, and route contracts with targeted unit tests.

## Test plan
- [x] cd services/claw-interface && .venv/bin/ruff format --check .
- [x] cd services/claw-interface && .venv/bin/ruff check .
- [x] cd services/claw-interface && uv tool run pyright --pythonpath .venv/bin/python app tests
- [x] cd services/claw-interface && .venv/bin/python -m pytest tests/unit/test_enterprise_package_subscription.py tests/unit/test_vertical_pack_package_service.py tests/unit/test_vertical_pack_plan_service.py tests/unit/test_vertical_pack_plans_routes.py tests/unit/test_internal_stripe_resources.py tests/unit/test_internal_vertical_pack_plans_routes.py tests/unit/test_antom_billing_v2_checkout.py tests/unit/test_billing_v2_pending_entitlements.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_billing_v2_expiry.py tests/unit/test_stripe_client.py -q

---

## fix(claw-interface): retry idempotent OpenClaw requests on server disconnect (ECA-965) (#2368)

- **SHA**: `8dc2717a72a34790dbae23b49edc5ca3e9c5ebad`
- **作者**: chris-srp
- **日期**: 2026-06-11T07:51:39Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/8dc2717a72a34790dbae23b49edc5ca3e9c5ebad
- **PR**: #2368

### 完整 Commit Message

```
fix(claw-interface): retry idempotent OpenClaw requests on server disconnect (ECA-965) (#2368)

## Summary

The shared OpenClaw client (`app/services/openclaw_client/_base.py`) had
**no retry**, so a transient `httpx.RemoteProtocolError: Server
disconnected without sending a response` surfaced as a **spurious HTTP
500** to the dashboard.

GCP shows it's rare (1 incident / 14d) but real. The full traceback pins
the path the auto-triage couldn't:

```
GET /computer/{id}/status → computer_service.get_computer_status:145
  → openclaw_client.get_bot_status (_bot_lifecycle.py:300)
  → _base.py:44  self._get_client().request("GET", ...)  → RemoteProtocolError → 500
```

Root cause: httpx reuses a keepalive connection the **bot pod** has
already half-closed (typically the pod's rolling-deploy window — same
kube-proxy race as ECA-848). httpx does not auto-retry this, and
`AsyncHTTPTransport(retries=1)` covers only the connect layer, not a
post-connect disconnect.

Linear:
https://linear.app/srpone/issue/ECA-965/claw-interface-httpx-remoteprotocolerror-server-disconnected-without

## Fix

Two layered defenses on the shared client, mirroring the repo's existing
precedent (`composio_connectors.py:128`, `chat.py:1167`):

1. `httpx.AsyncHTTPTransport(retries=1)` — reconnects on connect-layer
failures (ConnectError/ConnectTimeout) before the request hits the wire.
2. `_request` retries **once** on `RemoteProtocolError` for **idempotent
methods only** (`GET/HEAD/OPTIONS/PUT/DELETE`). "Disconnected without
sending a response" means the server sent zero bytes, so a replay can't
duplicate a side effect; `POST` and friends still propagate.

Lives in the shared `_request`, so every OpenClaw call benefits — not
just `get_bot_status`.

## Testing

- New tests in `tests/unit/test_openclaw_client.py`: idempotent GET
retries once and succeeds; persistent disconnect propagates after
exactly one retry; **POST is not retried**.
- `pytest tests/unit/test_openclaw_client.py` — **141 passed** (3 new).
`ruff` + `ruff format` + `pyright` clean.

## Behaviour

No API change. The only observable difference is a transient bot-pod
disconnect on an idempotent call now transparently succeeds instead of
returning 500 (with a `[OPENCLAW] retrying …` WARNING for visibility).

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR 描述

## Summary

The shared OpenClaw client (`app/services/openclaw_client/_base.py`) had **no retry**, so a transient `httpx.RemoteProtocolError: Server disconnected without sending a response` surfaced as a **spurious HTTP 500** to the dashboard.

GCP shows it's rare (1 incident / 14d) but real. The full traceback pins the path the auto-triage couldn't:

```
GET /computer/{id}/status → computer_service.get_computer_status:145
  → openclaw_client.get_bot_status (_bot_lifecycle.py:300)
  → _base.py:44  self._get_client().request("GET", ...)  → RemoteProtocolError → 500
```

Root cause: httpx reuses a keepalive connection the **bot pod** has already half-closed (typically the pod's rolling-deploy window — same kube-proxy race as ECA-848). httpx does not auto-retry this, and `AsyncHTTPTransport(retries=1)` covers only the connect layer, not a post-connect disconnect.

Linear: https://linear.app/srpone/issue/ECA-965/claw-interface-httpx-remoteprotocolerror-server-disconnected-without

## Fix

Two layered defenses on the shared client, mirroring the repo's existing precedent (`composio_connectors.py:128`, `chat.py:1167`):

1. `httpx.AsyncHTTPTransport(retries=1)` — reconnects on connect-layer failures (ConnectError/ConnectTimeout) before the request hits the wire.
2. `_request` retries **once** on `RemoteProtocolError` for **idempotent methods only** (`GET/HEAD/OPTIONS/PUT/DELETE`). "Disconnected without sending a response" means the server sent zero bytes, so a replay can't duplicate a side effect; `POST` and friends still propagate.

Lives in the shared `_request`, so every OpenClaw call benefits — not just `get_bot_status`.

## Testing

- New tests in `tests/unit/test_openclaw_client.py`: idempotent GET retries once and succeeds; persistent disconnect propagates after exactly one retry; **POST is not retried**.
- `pytest tests/unit/test_openclaw_client.py` — **141 passed** (3 new). `ruff` + `ruff format` + `pyright` clean.

## Behaviour

No API change. The only observable difference is a transient bot-pod disconnect on an idempotent call now transparently succeeds instead of returning 500 (with a `[OPENCLAW] retrying …` WARNING for visibility).
