---
title: "微信渠道设置更可靠：绑定失败会明确报错并自动回滚"
type: "体验优化"
priority: "中"
date: "2026-06-28"
status: "待审核"
channels: ""
---
# 微信渠道设置更可靠：绑定失败会明确报错并自动回滚

## 核心宣传点
优化了微信渠道与 Agent 的绑定流程：绑定先于激活完成，绑定失败时会明确提示而不是悄悄「成功」，出错时还会自动恢复到之前的绑定状态，设置微信更稳更省心。

## 原始内容
```
fix(openclaw-settings): bind WeChat agents before activation (#2613)

## Summary

- Write or clear the WeChat channel agent binding before calling
FastClaw channel activation.
- Make explicit WeChat custom-agent binding failures fail setup instead
of returning success with a warning.
- Restore the previous WeChat binding during setup compensation when a
later activation or reload step fails.
- Add focused WeChat regression tests for custom-agent ordering,
main-agent binding cleanup, binding failure, and
restore-after-activation failure.

Scope is intentionally limited to the WeChat plugin. Mattermost and MS
Teams rollout cleanup are left out per follow-up direction.

Stacked on #2611.

## Tests

- PATH="$PWD/services/claw-interface/.venv/bin:$PATH"
PYTHONPATH="$PWD/services/claw-interface/.venv/lib/python3.12/site-packages"
bash scripts/verify-py.sh
- services/claw-interface/.venv/bin/pytest
tests/unit/test_openclaw_settings_routes.py -k 'WeixinPollEndpoint or
WeixinSetupScenarios or weixin_trigger_index_reload' -q
```

PR Description:
## Summary

- Write or clear the WeChat channel agent binding before calling FastClaw channel activation.
- Make explicit WeChat custom-agent binding failures fail setup instead of returning success with a warning.
- Restore the previous WeChat binding during setup compensation when a later activation or reload step fails.
- Add focused WeChat regression tests for custom-agent ordering, main-agent binding cleanup, binding failure, and restore-after-activation failure.

Scope is intentionally limited to the WeChat plugin. Mattermost and MS Teams rollout cleanup are left out per follow-up direction.

Stacked on #2611.

## Tests

- PATH="$PWD/services/claw-interface/.venv/bin:$PATH" PYTHONPATH="$PWD/services/claw-interface/.venv/lib/python3.12/site-packages" bash scripts/verify-py.sh
- services/claw-interface/.venv/bin/pytest tests/unit/test_openclaw_settings_routes.py -k 'WeixinPollEndpoint or WeixinSetupScenarios or weixin_trigger_index_reload' -q

