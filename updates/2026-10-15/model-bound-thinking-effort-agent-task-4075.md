---
title: "新功能：思考强度现在跟着模型一起保存，Agent 与 Task 可以各自固定「模型+强度」组合"
type: "新功能"
priority: "高"
date: "2026-10-15"
status: "待审核"
channels: ""
---

# 新功能：思考强度现在跟着模型一起保存，Agent 与 Task 可以各自固定「模型+强度」组合

## 核心宣传点

选择思考强度时会连同当前选中的模型一起保存。Agent 的默认值写进 Revision 源码，跟随发布、分享与回滚；Task 上的覆盖从下一轮对话开始生效——选了强度就会固定显示的模型，换模型会重置强度，「模型默认」保留固定的模型，「跟随 Agent」则清空整对配置。本次范围只有 Agent 设置和 Web 端 Task 控件，iOS 与定时任务的配置和界面不变。ECAP 会显式保存或清除完整的 Agent 配对，兼容只带模型的老客户端和个人订阅退出场景；Engine 侧的全局 Agent 合并、Auto/兜底/子 Agent/定时任务默认继承逻辑均未改动。

## 分级

- 内部：P1
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## 备注

需先发配套的 Engine controld/workers，再发 ECAP 后端与 Web；本 PR 不含合并与部署，配套 #2002 仅补 Task 支持。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `816320a0e083948c796eca00c5723409be132da5`
- PR: #4075
- 作者：kaka-srp
- 日期：2026-10-15T02:38:04Z

### Commit Message

```
feat(agents): add model-bound agent and task thinking controls (#4075)

Selecting thinking effort now saves it with the selected model. Agent
defaults live in Revision source and follow publish/share/rollback. Task
overrides persist from the next turn: choosing an effort fixes the
displayed model, switching models resets effort, Model default retains
the fixed model, and Follow Agent clears the complete pair.

Scope is Agent Settings and Web Task controls only. iOS and Schedule
configuration/UI are unchanged. ECAP explicitly saves or clears the
complete Agent pair, including old model-only clients and
personal-subscription exit. Engine global Agent merging,
Auto/fallback/subagent/Schedule default inheritance remain unchanged;
companion #2002 only adds Task support. Ship companion Engine
controld/workers before ECAP backend and Web. No merge/deployment is
included.

Validation:
- Python: 184 relevant tests (182 original cases plus 2 legacy Auto
alignment cases), plus 13 ownership/Environment fixture cases; ruff,
format, pyright, 8 import contracts and file-length gate pass.
- Web: 8 files / 158 tests; governance, tsc and changed-file ESLint
pass. Actual Chrome mock interactions verify Low, Model default and
Follow Agent persistence across reload, with 0 page errors.
- Real existing owned local Agent: 12 successful provider turns through
the actual ECAP service layer, staging encrypted Mongo/Billing, shared
local PostgreSQL/Temporal/Engine and staging LiteLLM. Transcript
metadata confirms effort, persistent/isolation behavior, model-switch
defaults, Agent updates and restored source. Real concurrent CAS
produces one success and one 409; stale config is rejected.
- This round uses service-layer authentication context from the existing
owned Account; browser bearer and real ACS/Mattermost delivery were not
rerun. Browser validation is explicitly mock. No wire interceptor was
used.
- Original source/model/effort/Environment 14 restored; 2
successful-test and 6 debug Tasks independently confirmed archived;
original shared application lane restored. 3 additional real debug turns
are recorded separately.
- Astra's reset response entitlement drift and legacy Auto baseline
conflict were fixed. Targeted Astra re-review marked both ADDRESSED with
no new blockers; regression cases cover POST/GET equality and preserved
direct-edit conflicts.

Design and reproducible evidence:
docs/superpowers/specs/2026-10-14-agent-thinking-levels.md,
docs/validation/2026-10-14-agent-thinking-real.md and
docs/validation/2026-10-14-thinking-pair-real.json. Earlier validation
is marked superseded.

Dependency:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/2002

CI fixture follow-up: subscription runtime-grant fixtures now
distinguish the authorized connection GET from the Agent-state GET,
preserving opaque runtime ownership assertions. Environment isolation
fixtures assert the atomic thinking:null alongside the model switch.
Production behavior is unchanged by this follow-up.
```

