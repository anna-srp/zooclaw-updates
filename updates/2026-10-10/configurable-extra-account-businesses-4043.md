---
title: "新产品线接入改为配置项，不再需要改代码才能登录和计费"
type: "后端功能"
priority: "中"
date: "2026-10-10"
status: "待审核"
channels: ""
---

# 新产品线接入改为配置项，不再需要改代码才能登录和计费

## 核心宣传点

此前 claw-interface 只认 ecap 和 ecap-platform 两个账号 business，其余在令牌路由（401）和计费分支（billing.unknown_business）两处被拒，后者还连带影响 Agent 沙箱等级判定和积分读取，新产品线连 Agent 都装不上。现在支持用环境变量 EXTRA_ACCOUNT_BUSINESSES（逗号分隔，默认空）声明额外可接受的 business，新产品线接入从改代码变成改配置；被配置的 business 按普通产品账号计费而非 Platform。未配置环境行为完全不变，属于默认关闭、按需开启。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## 备注

需要在目标环境配置 EXTRA_ACCOUNT_BUSINESSES 后才生效，仅改配置不改代码。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `f6c29b83a7739d1f3eb446ef38176e323117e09c`
- PR: #4043
- 作者：tim-srp
- 日期：2026-10-10T03:42:51Z

### Commit Message

```
feat(auth): accept configured extra account businesses (#4043)

claw-interface accepted only `ecap` and `ecap-platform`, and rejected
every other account business in two places: the token routing hint (`401
Unsupported account business`) and the billing policy branch
(`billing.unknown_business` — which also governs the Agent sandbox class
and the credits read). A new product business therefore could not be
onboarded without a code change.

Read extra businesses from `EXTRA_ACCOUNT_BUSINESSES` (comma-separated,
empty by default) so onboarding becomes a configuration change. `ecap`
and `ecap-platform` stay built in and cannot be configured away; a
configured business bills as an ordinary product account rather than as
Platform. Unconfigured environments keep rejecting everything else, so
this ships closed.

## Summary
- Add `EXTRA_ACCOUNT_BUSINESSES` and `accepted_businesses()`, and drive
the token business gate from it. Extract the repeated `"ecap"` fallback
into `DEFAULT_BUSINESS`.
- Treat a configured business as an ordinary product account in
`is_api_platform()`, instead of raising `billing.unknown_business`. That
error previously broke Agent install (sandbox class) and the credits
read for any business outside the two built-ins.
- Document the setting in `.env.example` and the Platform operations
runbook.

## Test plan
- [x] `tests/unit/test_business_allowlist.py` — 33 passed. Covers both
gates for configured and unconfigured environments, the two values this
unblocks (`workforce-training`, `workforce-agency`), the built-in
fallbacks, and the legacy `zoowork` billing row.
- [x] Related existing suites (auth, middleware, platform, billing) —
215 passed.
- [x] `bash scripts/verify-py.sh` passed: ruff, ruff-format, pyright and
import-linter (8 contracts kept).

## Rollout
The values only take effect once an environment sets
`EXTRA_ACCOUNT_BUSINESSES` (for example
`workforce-training,workforce-agency`). This PR adds the switch;
enabling a specific business remains a deployment configuration step.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Review follow-up
- Codex flagged (P1) that a malformed `business` claim — a JSON list or
object — escaped as `TypeError: unhashable type` from the new set
membership, producing a 500 on every authenticated route. Reproduced
against the PR head and against `origin/main` (the previous tuple
comparison simply rejected it), then fixed: only a missing or empty
claim means a pre-claim ZooWork token; any other non-string claim
returns the same 401 as an unknown business. `is_api_platform()` now
fails closed on an unhashable value from a dict caller. Regression cases
added for list, dict, number, boolean, empty list and empty object
claims.
- Test count is now 42 in `test_business_allowlist.py`; 272 passed
across the related suites.
```

