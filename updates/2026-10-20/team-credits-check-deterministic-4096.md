---
title: "修复：团队尚未购买套餐时额度检查结果不再随机摇摆"
type: "Bug Fix"
priority: "高"
date: "2026-10-20"
status: "待审核"
channels: ""
---

# 修复：团队尚未购买套餐时额度检查结果不再随机摇摆

## 核心宣传点

个人组织升级为团队后会沿用原计费团队 ID，但在购买团队套餐前计费侧并不存在对应客户，导致额度检查的两个并发请求谁先失败、返回结果就跟着变。修复后先等待额度检查接口的结果，把它的 400 作为「无订阅」的唯一信号，另一个额度查询请求在失败时直接取消并清理，不会让卡住的请求拖慢已经确定的结论。其他异常仍会照常抛出并暴露出来，避免把真实的计费数据不一致掩盖掉。对用户的体现是：新升级团队在未购套餐时能稳定拿到一致的提示，而不是时而报错时而放行。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `eed7906d53863ba39a51b1cb0c14bd024db0d3f8`
- PR: #4096
- 作者：finn-srp
- 日期：2026-10-20T05:13:44Z

### Commit Message

```
fix(claw-interface): keep credits check deterministic for teams without a Lago customer (#4096)

## Summary
- `check_user_credits_flow` still calls BG `/credits/check` and
`/credits` concurrently, but now awaits `/credits/check` first. Its 400
is the only no-subscription signal, so the response no longer depends on
which concurrent call fails first.
- When `/credits/check` fails, the `/credits` task is cancelled and
drained instead of awaited, so a stalled `/credits` cannot delay a known
answer (Codex review P1).
- Any other failure still raises, including `/credits` 404 while a
subscription exists. That case is a real billing data inconsistency and
stays visible.

## Root cause
A personal org upgraded to team (self-service since #3762; staff console
since #3044) keeps its existing billing team id but, by design, gets no
team plan, so Lago has no customer for that team until a plan is
purchased. For that customer BG returns `/credits/check` 400 (no active
subscription) and `/credits` 404 (`customer_not_found`).

The flow used a plain `asyncio.gather`, which raises whichever failure
finishes first. When the 400 won, the caller got the no-subscription
response (200); when the 404 won, it fell into the generic handler and
returned 500. Production on 2026-10-20: one account that upgraded at
02:45 UTC and stayed on checkout made 143 × 200 and 121 × 500 on `GET
/users/credits/check` in about 20 minutes, which pushed the
claw-interface 5xx rate above 2% (Grafana alert
`zooclaw-claw-interface-error-rate`, PagerDuty #113807). Every account
with this error since 2026-09-23 performed a self-service upgrade
beforehand, except one group on 2026-10-13 that came the same day as
staff-console upgrades.

Not in scope: `GET /users/credits` calls only `/credits` and returns 500
for these accounts on every call (no such errors in production logs
since 2026-09-21, the start of log retention); `/users/credits/usage/*`
returns 503 `usage.unavailable` in the same state.

## Test plan
- [x] New unit test reproduces the race: with the old code the "404
finishes first" case fails and the "400 finishes first" case passes;
both pass with the fix
- [x] New unit test: `/credits` 404 with an active subscription still
raises
- [x] New unit test: a stalled `/credits` does not delay the
no-subscription answer and is cancelled (times out on the first commit,
passes with the follow-up)
- [x] `tests/unit/test_internal_users_credits.py` +
`tests/unit/test_user_credits.py` (53 passed)
- [x] BDD `tests/bdd/step_defs/test_user_credits.py` against local
MongoDB (12 passed)
- [x] `scripts/verify-py.sh` and `ecap-verify-py-ci` on the final
rebased commit

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

