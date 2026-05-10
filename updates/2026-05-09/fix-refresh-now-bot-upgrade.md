---
title: "「立即刷新」按钮修复：Bot 升级现在真的会立刻生效"
type: "Bug Fix"
priority: "中"
date: "2026-05-09"
status: "待审核"
channels: ""
---
# 「立即刷新」按钮修复：Bot 升级现在真的会立刻生效

## 核心宣传点
点击"立即刷新"后，你的 Bot 会立刻升级到最新版本，不再需要手动重启或等待横幅消失。

## 原始内容

**Commit**: `8e1889b0` | **PR**: #1586

### Commit Message

```
fix(openclaw): upgrade bot image before redeploy so Refresh Now works (#1586)

## Summary

- The "Refresh Now" button triggered a redeploy (stop+start) without updating the bot's `deployment.image`, so bots with an explicit image pinned at an old version would restart on that same old version — the upgrade banner persisted
- Root cause: once a bot has `config.deployment.image` explicitly set (e.g. from batch upgrade scripts or the @srp.one image-version selector), FastClaw uses that stored value on start instead of `defaultDeployment.image`
- Fix: call the existing `upgrade_bot_image_if_needed()` helper before `redeploy_bot()` to update the image to the latest published release
- Also aligns the image read path with current FastClaw API structure (`bot.image` top-level field, with fallback to `deployment.image`)
```

### PR Body

## Summary

- The "Refresh Now" button triggered a redeploy (stop+start) without updating the bot's `deployment.image`, so bots with an explicit image pinned at an old version would restart on that same old version — the upgrade banner persisted
- Root cause: once a bot has `config.deployment.image` explicitly set (e.g. from batch upgrade scripts or the @srp.one image-version selector), FastClaw uses that stored value on start instead of `defaultDeployment.image`
- Fix: call the existing `upgrade_bot_image_if_needed()` helper before `redeploy_bot()` to update the image to the latest published release
- Also aligns the image read path with current FastClaw API structure (`bot.image` top-level field, with fallback to `deployment.image`)

## Test plan

- [x] `pyright` clean
- [x] All pre-commit hooks pass
- [x] Existing `test_bot_upgrade.py` tests still pass (9/9)
- [ ] Manual verification: after deploy, publish a new release → banner appears → click "Refresh Now" → bot restarts on new version → banner disappears
