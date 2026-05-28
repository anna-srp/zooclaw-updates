---
title: "渠道账号 ID 配置校验优化"
type: "Bug Fix"
priority: "中"
date: "2026-05-27"
status: "待审核"
channels: ""
---

# 渠道账号 ID 配置校验优化

## 核心宣传点

渠道设置页面现在会实时校验账号 ID 格式，避免因配置错误导致消息无法送达。

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**SHA**: [566e72dd](https://github.com/SerendipityOneInc/ecap-workspace/commit/566e72dddb6b4d874119ee86502f76764bab3baa)
**PR**: [#1982](https://github.com/SerendipityOneInc/ecap-workspace/pull/1982)  
**作者**: kaka-srp  
**日期**: 2026-05-27T09:35:17Z

**Commit Message:**

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


**PR Description:**

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

