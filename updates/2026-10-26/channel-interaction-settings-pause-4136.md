---
title: "频道新增互动规则设置与暂停/恢复开关，不用删连接也能停用"
type: "新功能上线"
priority: "高"
date: "2026-10-26"
status: "待审核"
channels: ""
---

# 频道新增互动规则设置与暂停/恢复开关，不用删连接也能停用

## 核心宣传点

此前一个频道接上去之后，私聊/群聊谁能用、要不要 @ 机器人才响应这些规则只能在接入向导里定一次，事后想改只能删掉重连；想临时停用也只有删除连接一条路，身份、凭据和历史记录会一起丢。本次给频道加了一套可读可改的互动设置：支持查看和编辑私聊/群聊的准入规则、成员与群组名单、以及是否需要 @ 才触发，并且可以直接暂停或恢复一个连接——暂停期间身份、凭据和历史全部保留，恢复后继续用原来的配置。

设置编辑器按版本号提交增量修改，多人同时改动时冲突不会把你写的内容冲掉，保存失败的草稿也会留在页面上供你重试；界面上「已保存的设置」和「网关实际生效状态」分开展示，不会再出现保存成功但其实没下发的误解。飞书/企业微信/钉钉的引导式接入会沿用你在向导里选好的规则，各平台支持的能力不同时，界面只显示该平台真正支持的选项；已有的分群覆盖规则和飞书文档权限控制保持不变。中英文界面均已适配，窄屏 390px 下可用。

## 分级

- 内部：P0
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `69659b1a64e8d267d9d94db0b545c992b2af9f3a`
- PR: #4136
- 作者：kaka-srp
- 日期：2026-10-26T03:27:21Z

### Commit Message

```
feat(channels): add versioned interaction settings and pause controls (#4136)

## Summary

Channel owners can now read and edit supported DM/group access rules,
member/group lists and mention gating, and pause or resume a connection
while retaining its identity, credentials and history. A dedicated
editor sends versioned partial updates, retains failed drafts, and
separates saved settings from gateway application status.

Guided Feishu/WeCom/DingTalk setup preserves the chosen rules. The
backend and Service API share typed settings and owner-scoped
recent-contact contracts; English/Chinese UI controls follow the
capabilities advertised by ACS. Existing per-group overrides and Feishu
document-permission controls are preserved.

## Dependencies and rollout

- Companion ACS PR:
https://github.com/SerendipityOneInc/agent-channel-service/pull/175.
- Deploy ACS first, complete the claw-interface rollout, then deploy web
or enable clients using the new setup fields.
- Old setup requests retain their Redis shape across a backend rolling
deploy. No Engine code or schema migration is included.
- Design and acceptance:
`docs/superpowers/specs/2026-10-23-channel-settings-closed-loop.md`.

## Test plan

- Backend channel/setup/client/Service API regression tests: 305 passed.
- Frontend channel/page/query suites: 343 passed.
- Web governance, TypeScript, ESLint; backend Ruff, format, Pyright and
architecture contracts passed.
- Playwright local browser acceptance: global and Agent-scoped entries,
edit/save/refetch/reload, member/group lists, conflict draft
preservation/reload, pause/resume, platform capability differences,
Chinese labels and 390px viewport.
- Companion ACS acceptance exercises real local HTTP, Engine identity,
PostgreSQL and Feishu gateway application acknowledgments, plus
installed-provider mention admission checks.
- UI browser tests use mock authentication/backend data. No customer
messages or live LLM chat turns were sent.

## Local review

Astra completed a local review and targeted re-review. All four verified
findings were fixed: provider-prefixed wildcard IDs, ineffective WeChat
DM controls, legacy Feishu mention-default changes, and old WeChat
create compatibility. The re-review found no new actionable issues and
cleared the change for PR creation.

## Automated review follow-up

- Enabled the existing workspace query polling on the global Channels
page; pending gateway application refreshes every five seconds even when
connection health is already healthy. The editor continues observing the
shared query. Browser acceptance verified pending-to-applied after
saving without navigation or window refocus.
- Preserved historical explicit-null behavior for existing nullable
update fields and create allow_from; newly introduced
list/mention/version inputs still reject null.
- Added a regression proving a legacy pairing policy stays visible and
is absent from an unrelated dirty-only update. Capability lists describe
newly selectable policies and do not redefine historical API values.
- ACS/backend/web deployment order and setup-session rolling
compatibility remain documented above. Readability-only refactors were
left outside this change.

Astra independently re-reviewed this follow-up delta and found no new
actionable issues.

Final review adjudication: ACS remains the policy authority. Its update
path normalizes every effective dm_policy=open to allowFrom=["*"], so a
simultaneously forwarded member list cannot override open access. Split
validation is intentional: claw-interface validates provided fields; ACS
validates them against saved policy under its transaction. Existing
owner resolution is shared across Service API actions. Deployment must
follow the documented ACS → complete backend rollout → web order; this
PR does not perform a release.
```
