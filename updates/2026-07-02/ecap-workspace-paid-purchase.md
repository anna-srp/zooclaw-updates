---
title: "应用市场支持直接购买付费 Agent 包"
type: "新功能上线"
priority: "高"
date: "2026-07-02"
status: "待审核"
channels: ""
---
# 应用市场支持直接购买付费 Agent 包
## 核心宣传点
现在可以在 Agent 管理页直接购买付费 Agent 包：点击 Purchase 走 Stripe 安全支付，付款成功后自动完成安装，已购包随时可见。
## 原始内容
### [ecap-workspace PR #2712]

feat(agent-packs): add paid purchase backend (#2712)

## Summary
- Add the current-user purchased pack listing endpoint for Agent
Manager.
- Validate each returned pack through the active ECAP pack purchase
agreement contract.
- Harden paid pack checkout resume/retry behavior for pending,
paid-but-reconciling, stale, and invalid Stripe sessions.

## Split rollout
- Backend-only PR. Merge and deploy this before the frontend purchase UI
PR.
- The frontend PR should no longer need a `/agent-packs/purchases` 404
fallback once this is live.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH python -m pytest
services/claw-interface/tests/unit/test_public_agent_packs_routes.py
services/claw-interface/tests/unit/test_ecap_pack_subscription_service.py
services/claw-interface/tests/unit/test_billing_v2_repos.py
services/claw-interface/tests/unit/test_pack_purchase_repo.py -q`
- [x] `git diff --check`

---

## PR Description

## Summary
- Add the current-user purchased pack listing endpoint for Agent Manager.
- Validate each returned pack through the active ECAP pack purchase agreement contract.
- Harden paid pack checkout resume/retry behavior for pending, paid-but-reconciling, stale, and invalid Stripe sessions.

## Split rollout
- Backend-only PR. Merge and deploy this before the frontend purchase UI PR.
- The frontend PR should no longer need a `/agent-packs/purchases` 404 fallback once this is live.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH python -m pytest services/claw-interface/tests/unit/test_public_agent_packs_routes.py services/claw-interface/tests/unit/test_ecap_pack_subscription_service.py services/claw-interface/tests/unit/test_billing_v2_repos.py services/claw-interface/tests/unit/test_pack_purchase_repo.py -q`
- [x] `git diff --check`


---

### [ecap-workspace PR #2713]

feat(agent-packs): add paid purchase frontend (#2713)

## Summary
- Wire Agent Manager to load the current user's purchased paid packs on
page entry.
- Switch paid agent cards between Purchase and the normal
install/uninstall actions after purchase is confirmed.
- Add Stripe checkout popup handling, cancel handling, manual Paid
confirmation, success-url auto-install, and targeted paid-pack UI tests.

## Split rollout
- Stacked on backend PR #2712 (`codex/agent-pack-purchase-backend`).
- Backend PR #2712 must merge and deploy before this frontend PR is
merged/deployed.
- This frontend intentionally does not include a
`/agent-packs/purchases` 404 fallback; the backend endpoint is treated
as required.

## Test plan
- [x] `git diff --check codex/agent-pack-purchase-backend...HEAD`
- [ ] `pnpm --dir web/app exec vitest run
tests/unit/app/agents-manager/useViewModel.unit.spec.tsx
tests/unit/hooks/usePurchasedAgentPacks.unit.spec.ts
tests/unit/services/agent-packs.unit.spec.ts
tests/unit/app/agents-manager/AgentCard.unit.spec.tsx
tests/unit/hooks/useAgentActions.unit.spec.ts` blocked locally by
`ERR_PNPM_MISSING_TARBALL_INTEGRITY` for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`

---

## PR Description

## Summary
- Wire Agent Manager to load the current user's purchased paid packs on page entry.
- Switch paid agent cards between Purchase and the normal install/uninstall actions after purchase is confirmed.
- Add Stripe checkout popup handling, cancel handling, manual Paid confirmation, success-url auto-install, and targeted paid-pack UI tests.

## Split rollout
- Stacked on backend PR #2712 (`codex/agent-pack-purchase-backend`).
- Backend PR #2712 must merge and deploy before this frontend PR is merged/deployed.
- This frontend intentionally does not include a `/agent-packs/purchases` 404 fallback; the backend endpoint is treated as required.

## Test plan
- [x] `git diff --check codex/agent-pack-purchase-backend...HEAD`
- [ ] `pnpm --dir web/app exec vitest run tests/unit/app/agents-manager/useViewModel.unit.spec.tsx tests/unit/hooks/usePurchasedAgentPacks.unit.spec.ts tests/unit/services/agent-packs.unit.spec.ts tests/unit/app/agents-manager/AgentCard.unit.spec.tsx tests/unit/hooks/useAgentActions.unit.spec.ts` blocked locally by `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`


---

### [ecap-workspace PR #2689]

feat(agent-packs): return checkout for purchase (#2689)

## Linear


## Summary
- Wire public agent-pack purchase route to create the purchase snapshot
first, then create an ECAP pack checkout and return the checkout URL
response.
- Resolve buyer identity from the current org membership, validate the
current org through org service, and require a personal org.
- Require an active ECAP pack purchase agreement before installing paid
packs, so abandoned checkout snapshots do not unlock installs.
- Add request/response models and route tests for checkout response,
current-org identity, forbidden client-supplied internal fields, and
team-org rejection.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_public_agent_packs_routes.py
services/claw-interface/tests/unit/test_pack_purchase_service.py
services/claw-interface/tests/unit/test_ecap_pack_subscription_service.py
-q`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_public_agent_packs_routes.py
services/claw-interface/tests/unit/test_pack_purchase_service.py
services/claw-interface/tests/unit/test_ecap_pack_subscription_service.py
services/claw-interface/tests/unit/test_agent_install_service.py -q`
(`106 passed`)
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`

---

## PR Description

## Linear


## Summary
- Wire public agent-pack purchase route to create the purchase snapshot first, then create an ECAP pack checkout and return the checkout URL response.
- Resolve buyer identity from the current org membership, validate the current org through org service, and require a personal org.
- Require an active ECAP pack purchase agreement before installing paid packs, so abandoned checkout snapshots do not unlock installs.
- Add request/response models and route tests for checkout response, current-org identity, forbidden client-supplied internal fields, and team-org rejection.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_public_agent_packs_routes.py services/claw-interface/tests/unit/test_pack_purchase_service.py services/claw-interface/tests/unit/test_ecap_pack_subscription_service.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_public_agent_packs_routes.py services/claw-interface/tests/unit/test_pack_purchase_service.py services/claw-interface/tests/unit/test_ecap_pack_subscription_service.py services/claw-interface/tests/unit/test_agent_install_service.py -q` (`106 passed`)
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`

