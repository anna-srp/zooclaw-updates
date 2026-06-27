---
title: "新增钉钉（DingTalk）IM 渠道接入"
type: "新功能上线"
priority: "中"
date: "2026-06-26"
status: "待审核"
channels: ""
---
# 新增钉钉（DingTalk）IM 渠道接入

## 核心宣传点
现在可以把你的 Agent 接到钉钉上，扫码或手动填写凭证即可完成绑定，直接在钉钉里和 Agent 对话办事。

## 原始内容
```
feat(openclaw): add dingtalk im channel (#2616)

## Linear
https://linear.app/srpone/issue/ECA-1098/add-dingtalk-im-channel

## Summary
- Add DingTalk (`dingtalk-connector`) as an OpenClaw IM channel in ECAP
settings, including QR registration setup, manual credential setup,
polling/cancel APIs, and frontend setup UX.
- Store DingTalk connector credentials through FastClaw channel account
config and add safeguards for poll interval throttling, single-flight
success configuration, late modal cancellation, and sanitized backend
errors.
- Add DingTalk UI labels/locales/tests plus the Antom receipt repo
skill/symlink requested for this feature branch.
- Deliberately does not write
`plugins.entries["dingtalk-connector"].enabled = true` in this repo;
plugin packaging/enablement is expected to be handled outside ECAP via
openclaw-docker/runtime configuration.

## Size note
This PR carries `size-override` because it intentionally bundles the
DingTalk backend/frontend channel implementation, focused tests, and the
requested Antom receipt skill files. The effective size-check diff is
2596 lines, with the largest contributors being the Antom receipt
script, DingTalk channel backend, and DingTalk setup tests.

## Test plan
- [x] `pytest tests/unit/test_openclaw_settings_dingtalk.py -q`
- [x] `bash scripts/verify-py.sh`
- [x] `pnpm exec vitest run
tests/unit/app/api/openclaw-settings-dingtalk-routes.unit.spec.ts`
- [x] `bash scripts/verify-web.sh
web/app/src/app/[locale]/\\(app\\)/\\(chat\\)/claw-settings/components/channels/DingTalkSetupModal.tsx
web/app/src/app/[locale]/\\(app\\)/\\(chat\\)/claw-settings/components/channels/ChannelCard.tsx
web/app/src/app/api/openclaw/settings/channels/dingtalk-connector/setup/route.ts
web/app/src/app/api/openclaw/settings/channels/dingtalk-connector/poll/route.ts
web/app/src/app/api/openclaw/settings/channels/dingtalk-connector/cancel/route.ts
web/app/tests/unit/app/claw-settings/DingTalkSetupModal.unit.spec.tsx
web/app/tests/unit/app/claw-settings/ChannelsSection.unit.spec.tsx
web/app/tests/unit/app/api/openclaw-settings-dingtalk-routes.unit.spec.ts`
- [x] `bash scripts/sync-agent-skills.sh --check`
- [x] `bash scripts/verify-changed.sh`
```

### PR description

## Linear
https://linear.app/srpone/issue/ECA-1098/add-dingtalk-im-channel

## Summary
- Add DingTalk (`dingtalk-connector`) as an OpenClaw IM channel in ECAP settings, including QR registration setup, manual credential setup, polling/cancel APIs, and frontend setup UX.
- Store DingTalk connector credentials through FastClaw channel account config and add safeguards for poll interval throttling, single-flight success configuration, late modal cancellation, and sanitized backend errors.
- Add DingTalk UI labels/locales/tests plus the Antom receipt repo skill/symlink requested for this feature branch.
- Deliberately does not write `plugins.entries["dingtalk-connector"].enabled = true` in this repo; plugin packaging/enablement is expected to be handled outside ECAP via openclaw-docker/runtime configuration.

## Size note
This PR carries `size-override` because it intentionally bundles the DingTalk backend/frontend channel implementation, focused tests, and the requested Antom receipt skill files. The effective size-check diff is 2596 lines, with the largest contributors being the Antom receipt script, DingTalk channel backend, and DingTalk setup tests.

## Test plan
- [x] `pytest tests/unit/test_openclaw_settings_dingtalk.py -q`
- [x] `bash scripts/verify-py.sh`
- [x] `pnpm exec vitest run tests/unit/app/api/openclaw-settings-dingtalk-routes.unit.spec.ts`
- [x] `bash scripts/verify-web.sh web/app/src/app/[locale]/\\(app\\)/\\(chat\\)/claw-settings/components/channels/DingTalkSetupModal.tsx web/app/src/app/[locale]/\\(app\\)/\\(chat\\)/claw-settings/components/channels/ChannelCard.tsx web/app/src/app/api/openclaw/settings/channels/dingtalk-connector/setup/route.ts web/app/src/app/api/openclaw/settings/channels/dingtalk-connector/poll/route.ts web/app/src/app/api/openclaw/settings/channels/dingtalk-connector/cancel/route.ts web/app/tests/unit/app/claw-settings/DingTalkSetupModal.unit.spec.tsx web/app/tests/unit/app/claw-settings/ChannelsSection.unit.spec.tsx web/app/tests/unit/app/api/openclaw-settings-dingtalk-routes.unit.spec.ts`
- [x] `bash scripts/sync-agent-skills.sh --check`
- [x] `bash scripts/verify-changed.sh`

