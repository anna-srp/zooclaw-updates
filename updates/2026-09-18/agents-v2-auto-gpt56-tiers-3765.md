---
title: "feat(agents): route v2 Auto through GPT-5.6 tiers (#3765)"
type: "新功能上线"
priority: "高"
date: "2026-09-18"
status: "待审核"
channels: ""
---

# v2 Auto 模式换成 GPT-5.6 系列分档路由

## 核心宣传点

Auto 模式的模型路由全面升级到 GPT-5.6：简单问题走 gpt-5.6-luna，中等复杂度走 gpt-5.6-sol，高复杂和超高复杂的任务继续交给 Agent 主模型（默认 gpt-5.6-terra）。用户不用改任何设置，Auto 会自动在快和强之间选，简单任务更快更省，难任务照样上强模型。已经渲染好路由配置的老 Agent 要等下一次更新才切换。

## 分级

- 内部：P1
- 外部：A
- 发布状态：已合并待发版

## PR 说明

## Summary
- Route v2 Auto low-complexity turns to `gpt-5.6-luna` and mid-complexity turns to `gpt-5.6-sol`.
- Keep high and ultra turns on the Agent primary, which defaults to `gpt-5.6-terra`.
- Document that existing rendered routing blocks remain unchanged until the Agent is updated.

## Test plan
- [x] `PYTHONPATH=/tmp/codex-pytest-readline ./.venv/bin/python -m pytest tests/unit/test_agent_model_service.py -q` (13 passed)
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh` (pre-push)
- [x] Staging Engine `v0.2.6-beta.3`: Luna and Sol returned HTTP 200 through `openai-responses`; the same full-smoke run's model-routing job passed the deployed routing chain. Evidence is linked from the rollout record.
- [x] Staging Engine `v0.2.8-beta.4`: full routed-turn smoke with Luna as the declared target ([run 35305014533](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/35305014533)).
- [x] Staging Engine `v0.2.8-beta.4`: full routed-turn smoke with Sol as the declared target ([run 35305179783](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/35305179783)).


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `cb1b66232e7bf718fc16c86fd313661d495e3a1d`
- PR: #3765
- 作者：siqiao-srp
- 日期：2026-09-18T08:01:37Z

### Commit Message

```
feat(agents): route v2 Auto through GPT-5.6 tiers (#3765)

## Summary
- Route v2 Auto low-complexity turns to `gpt-5.6-luna` and
mid-complexity turns to `gpt-5.6-sol`.
- Keep high and ultra turns on the Agent primary, which defaults to
`gpt-5.6-terra`.
- Document that existing rendered routing blocks remain unchanged until
the Agent is updated.

## Test plan
- [x] `PYTHONPATH=/tmp/codex-pytest-readline ./.venv/bin/python -m
pytest tests/unit/test_agent_model_service.py -q` (13 passed)
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh` (pre-push)
- [x] Staging Engine `v0.2.6-beta.3`: Luna and Sol returned HTTP 200
through `openai-responses`; the same full-smoke run's model-routing job
passed the deployed routing chain. Evidence is linked from the rollout
record.
- [x] Staging Engine `v0.2.8-beta.4`: full routed-turn smoke with Luna
as the declared target ([run
35305014533](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/35305014533)).
- [x] Staging Engine `v0.2.8-beta.4`: full routed-turn smoke with Sol as
the declared target ([run
35305179783](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/35305179783)).
```

## 备注

发布状态：已合并待发版（尚未包含在任何 ecap-*-release tag 中，最新正式 release 为 ecap-v0.19.16-release）。

来源：SerendipityOneInc/ecap-workspace @ cb1b6623，PR #3765，作者 siqiao-srp。
