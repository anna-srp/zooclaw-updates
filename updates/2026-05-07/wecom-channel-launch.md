---
title: "企业微信（WeCom）渠道正式上线"
type: "新功能上线"
priority: "高"
date: "2026-05-07"
status: "待审核"
channels: ""
---
# 企业微信（WeCom）渠道正式上线

## 核心宣传点
ZooClaw 现在支持企业微信渠道接入，扫码即可连接企业微信机器人，轻松把 AI 能力接入你的企业微信工作群。

## 原始内容

### Commit Message
```
feat(wecom): add WeCom channel via QR scan + manual fallback (#1571)
```

### PR Description
## Summary

ECA-625: add WeCom (企业微信) as a first-class ZooClaw channel, modeled on the existing WeChat / Feishu QR-scan flows.

- **Pure-QR setup**: backend hits `https://work.weixin.qq.com/ai/qc/{generate,query_result}` (the upstream `@wecom/wecom-openclaw-cli` API) to mint a fresh WeCom bot via QR scan. On confirm, credentials (`botId` + `secret`) are pushed to FastClaw via `add_channel` and the bot pod's plugin reload picks them up.
- **Manual fallback**: WeCom mobile only mints a *new* bot per scan, so users with an existing bot can't reuse it via QR. An "advanced mode" toggle exposes a Bot ID / Secret form alongside the QR CTA.
- **Multi-account**: the account-id input is shown for WeCom (defaults to `default`), so users can connect multiple WeCom bots side-by-side. Backend round-trips `request.account` through the session into the FastClaw payload.
- **Auto-refresh on success**: `WecomSetupModal` fires `onSuccess` immediately on phase=success so the channel list updates without waiting for the user to dismiss the success card.

## Cross-repo dependency

Depends on **fastclaw v0.0.108** (PR https://github.com/SerendipityOneInc/fastclaw/pull/85), already deployed to staging. That PR adds `BotID` / `Secret` to FastClaw's `AddChannelRequest` struct so the credentials don't get silently dropped by Go's JSON binder.
