---
title: "微信扫码绑定去重，不再生成重复账号"
type: "体验优化"
priority: "中"
date: "2026-06-28"
status: "待审核"
channels: ""
---
# 微信扫码绑定去重，不再生成重复账号

## 核心宣传点
微信扫码确认时，如果识别到的是已存在的微信身份，会复用原有账号并把绑定切到目标 Agent，而不是再建一个重复账号，账号列表更干净。

## 原始内容
```
fix(claw-interface): dedupe WeChat QR accounts (#2634)

## Summary

- Reuse an existing WeChat account when QR confirmation returns a
`userId` already present in the bot's WeChat account files.
- Move the reused account's binding to the requested agent instead of
creating another account alias for the same real WeChat identity.
- Clean up stale duplicate WeChat account aliases from the account
index, credential files, channel config, and agent bindings.

## Testing

- `cd services/claw-interface && .venv/bin/pytest
tests/unit/test_openclaw_settings_routes.py::TestWeixinPollEndpoint -q`
- `cd services/claw-interface && .venv/bin/pytest
tests/unit/test_openclaw_settings_routes.py -q`
- `bash scripts/verify-py.sh --ruff-only`
- `cd services/claw-interface && .venv/bin/pyright --pythonpath
.venv/bin/python app/routes/openclaw_settings/weixin.py
app/routes/openclaw_settings/weixin_helpers.py
app/routes/openclaw_settings/helpers.py
tests/unit/test_openclaw_settings_routes.py`

Note: `bash scripts/verify-py.sh` was also attempted. Ruff and
import-linter passed, but the script-level pyright invocation did not
pick up the local venv and reported broad missing imports such as
`fastapi`, `pytest`, and `favie_common`. The changed files pass pyright
when run with the explicit venv python path above.
```

PR Description:
## Summary

- Reuse an existing WeChat account when QR confirmation returns a `userId` already present in the bot's WeChat account files.
- Move the reused account's binding to the requested agent instead of creating another account alias for the same real WeChat identity.
- Clean up stale duplicate WeChat account aliases from the account index, credential files, channel config, and agent bindings.

## Testing

- `cd services/claw-interface && .venv/bin/pytest tests/unit/test_openclaw_settings_routes.py::TestWeixinPollEndpoint -q`
- `cd services/claw-interface && .venv/bin/pytest tests/unit/test_openclaw_settings_routes.py -q`
- `bash scripts/verify-py.sh --ruff-only`
- `cd services/claw-interface && .venv/bin/pyright --pythonpath .venv/bin/python app/routes/openclaw_settings/weixin.py app/routes/openclaw_settings/weixin_helpers.py app/routes/openclaw_settings/helpers.py tests/unit/test_openclaw_settings_routes.py`

Note: `bash scripts/verify-py.sh` was also attempted. Ruff and import-linter passed, but the script-level pyright invocation did not pick up the local venv and reported broad missing imports such as `fastapi`, `pytest`, and `favie_common`. The changed files pass pyright when run with the explicit venv python path above.

