---
title: "企业组织新增按 uid 直接拉人入团队的管理接口，用量计入企业共享钱包"
type: "后端功能"
priority: "高"
date: "2026-10-10"
status: "待审核"
channels: ""
---

# 企业组织新增按 uid 直接拉人入团队的管理接口，用量计入企业共享钱包

## 核心宣传点

为 Workforce 企业能力补齐 claw-interface 侧接口：新增 POST /internal/orgs/{org_id}/members，运营可用 uid 把已有账号直接放进 team 类型企业组织，不需要邀请码、不做邮箱匹配、不关停对方个人环境、也不额外创建默认 Agent。这样加入的成员计费 key 绑定到企业团队，用量直接走企业共享钱包。单开通道是因为原有的 join 接口要求邀请邮箱与账号邮箱一致（纯手机号账号走不通）、必须确认关停个人环境，且默认 Agent 无法抑制。原邀请流程未改动，请求体未知字段直接 422。

## 分级

- 内部：P1
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## 备注

仅内部管理接口，无前端入口；需与 Workforce 侧的企业映射与成员编排能力配套使用。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `42928f0d76eb855337fd967d4d865bf3980c2cd4`
- PR: #4050
- 作者：tim-srp
- 日期：2026-10-10T10:09:32Z

### Commit Message

```
feat(claw-interface): add team org members directly by uid (#4050)

## Summary

Adds `POST /internal/orgs/{org_id}/members`, which puts an existing
account
into a **team** organization by uid — no invite code, no email matching,
no
source-organization shutdown, and no Agent provisioning. It is the
claw-interface half of the Workforce enterprise feature: members added
this way
have their billing key bound to the enterprise org's team, so their
usage
bills the enterprise's shared wallet.

The existing `POST /orgs/{org_id}/join` cannot serve this: it requires
the
invite's email to equal the joining account's email (so a phone-only
identity
can never use it), requires an explicit confirmation that the caller's
own
personal environment will be shut down, and provisions a default main
Agent.
`docs/superpowers/specs/2026-10-10-workforce-enterprise-credits.md`
records
that the Agent creation is not suppressible in that flow, so this adds a
separate administrative path instead of changing it. The invite flow is
untouched.

### Contract

Request (unknown fields rejected, 422):

| Field | Type | Constraint |
|---|---|---|
| `business` | string | required, trimmed, 1–64; accepted business equal
to the target org creator's business |
| `uid` | string | required, trimmed, 1–128 |
| `role` | `"admin"` \| `"user"` | optional, default `"user"`; an
explicit `null` is rejected — omit it to leave an existing role alone |

Response 200:

```json
{"org_id":"existing-org-id","uid":"751","role":"user","status":"active","created":true,"joined_at":"2026-10-10T07:00:00Z"}
```

Errors, in the service's `{"code","detail"}` shape:

| Status | Code |
|---|---|
| 404 | `org.not_found` |
| 404 | `account.not_found` |
| 403 | `member.business_forbidden` |
| 400 | `member.org_not_team` |
| 409 | `member.active_membership_conflict` (existing org id kept in the
server-side context) |
| 409 | `member.add_conflict` (concurrent writer; retry) |
| 503 | `billing.unavailable` (local write compensated, so retrying the
same request is safe) |

Auth is the same as the neighbouring `POST
/internal/orgs/{org_id}/credits`:
the `/internal` router's `require_srp_account` gate plus
`require_admin_user`.

### Reuse, not a second membership path

Activation goes through a new shared helper,
`app/services/org/member_key_binding.py`, which performs the same three
steps
the invite join performs inline: bind the key to the org's billing team,
sync
the profile team projection, ensure the member usage-tracking row. The
invite
join's own copy is deliberately left alone — 18 tests patch its
module-level
binding calls, and redirecting it would rewrite coverage of the handoff
flow
for no behavioural gain. A bind failure compensates the local
membership: a row
this endpoint created is deleted, a retained row returns to its previous
status, so a membership is never left without its billing binding.

### `POST /orgs {"org_type":"team"}` as a target — verified, no code
change needed

The consumer creates the enterprise org itself with the creator's own
user JWT,
so I verified that org is a valid target rather than assuming it:

- `POST /orgs` (`app/routes/enterprise/org.py`) requires only
`require_account`
  (L1) — there is **no** paid-product-subscription gate anywhere in
  `org_service.create_org`.
- For `org_type == "team"` it subscribes the billing team to the default
  `starter_20_month` plan, creates the subscription and top-up wallets,
persists `billing_team_id` (the field this endpoint binds against), and
runs
  the creator's usage-tracking ensure.
- Blast-radius check on the new business:
`sales_policy.is_api_platform()`
raises `billing.unknown_business` for an unconfigured business, and that
is
called from Agent install (sandbox class), purchase and the credits read
—
**not** from `POST /orgs`. The endpoint that matters here is gated only
by
  token verification.

**Config prerequisite, not a code change:** the deployed environment
must list
the business in `EXTRA_ACCOUNT_BUSINESSES` (e.g.
`workforce-training,workforce-agency`; it lives in the Vault-backed
`vault-claw-interface-env` secret). Without it, token verification
rejects the
business with 401 on every authenticated route, `POST /orgs` never runs,
and
this endpoint returns `403 member.business_forbidden`. I did not change
any
deployment config — this is a note for whoever enables the feature.

### Docs

`docs/superpowers/specs/2026-10-10-workforce-org-member-add.md` — a
companion
note next to the credits contract, covering the auth, the exact
semantics
table against the email-invite path, the explicit no-Agent /
no-source-org-
shutdown statement, the error table, the target-org provisioning
finding, and
the config prerequisites.

## Test plan

- [x] `tests/unit/test_internal_org_member_add.py` — 22 tests: auth gate
+
route registration, happy path with the billing bind asserted on the
org's
  `billing_team_id`, idempotent replay with and without an explicit role
  change, `409` conflict when the uid is active in another org, inactive
other-org row not blocking, suspended same-org row reactivated in place,
personal-org `400`, unknown org/creator/account, business mismatch at
three
values, unconfigured-gateway `503` with nothing written, both
compensation
  branches, and Agent provisioning not happening (asserted at the shared
provisioning entry point plus a structural guard on the module source).
- [x] Full unit suite: **11,913 passed, 5 skipped** (baseline `11,891
passed,
  5 skipped` + the 22 new).
- [x] `bash scripts/verify-py.sh` — ruff check, ruff format --check,
pyright
  `app/ tests/`, import-linter **8 contracts kept**.
- [x] All 8 `scripts/ci-lint/*.sh` guards pass (file length, complexity,
  deptry, collection-name, importlinter repo sync, dead code, pydantic
  returns).
- [ ] Not verified locally: `tests/bdd` and the real-Mongo paths. This
machine
has no Mongo with the `mongo`/`mongo` credentials
`tests/bdd/conftest.py`
  expects (255 skipped locally; CI supplies one), and there is no
`tests/integration` directory in this service. Unit stubs do not
exercise the
  encrypted Mongo client, so the membership write still needs staging
verification — called out in the spec's verification-boundary section
rather
  than claimed here.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5 <noreply@anthropic.com>
```

