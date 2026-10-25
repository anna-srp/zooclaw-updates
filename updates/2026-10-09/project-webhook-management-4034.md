---
title: "项目 Webhook 管理正式上线：可自助创建、测试、轮换密钥并重发历史事件"
type: "新功能"
priority: "高"
date: "2026-10-09"
status: "待审核"
channels: ""
---

# 项目 Webhook 管理正式上线：可自助创建、测试、轮换密钥并重发历史事件

## 核心宣传点

开发者平台新增 Webhook 管理能力，以前只能找人配置，现在可以在所选 Project 下自助完成全流程。导航里新增 Webhooks 入口，提供列表与详情页：新建时默认处于暂停状态，可编辑订阅的事件与会话范围，发一条测试投递，启用或暂停，轮换一次性展示的签名密钥，删除端点，还能按条件分页查看投递历史并对终态事件发起重发。后端做了 Project 归属校验，写操作仅管理员可用，入参类型受限、路由与方法白名单封闭，并带作用域幂等与不缓存响应。签名密钥只存在于页面的临时状态中，切换作用域即清空，迟到的响应会被丢弃；切换 Project 时会先回到新 Project 的列表再查询，避免串数据。

## 分级

- 内部：P1
- 外部：S
- toB 相关：是
- 发布状态：已合并待发版

## 备注

需 Engine #1898 配套发版；关联需求 #3787。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `1175b107954c359d7dc73a4cac7c7b46da2241f4`
- PR: #4034
- 作者：finn-srp
- 日期：2026-10-09T12:25:32Z

### Commit Message

```
feat(platform): add project webhook management (#4034)

Platform users can now manage signed Webhook delivery for the selected
Project through the authenticated claw-interface API.

## Summary
- Add Webhooks navigation and list/detail pages: create paused, edit
event/session scope, test delivery, enable/pause, rotate one-time
secrets, delete, inspect filtered/paged delivery history and redeliver
terminal events.
- Add a browser facade with verified Project tenancy, admin-only writes,
bounded typed input (including server-enforced paused creation), closed
route/method vocabulary, scoped idempotency and no-store responses.
Reuse the route resolver in the existing SDK facade.
- Poll tests by their exact receipt and refresh endpoint/history after
asynchronous test or redelivery completion. Switching Project from
detail returns to the new Project's list before querying the old
endpoint in the new scope.
- Keep signing secrets in transient component state only; clear them on
scope changes and discard late responses. Include preview fixtures,
product/design documentation and behavior regressions.

Related to #3787. [Engine
#1898](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1898),
which provides exact `receipt_id` filtering, is merged and released. The
specific receipt isolation scenario has passed against the deployed
staging Engine; production deployment and production-full-smoke
succeeded for the merge commit. See the review validation below for the
scope of each check. The feature requires both claw-interface and
Platform deployment.

## Validation
- After rebasing to latest main (542b009578), Node 24 Platform lint,
typecheck, all 283 tests and production build passed in the existing
Linux devcontainer with one worker.
- `ecap-verify-py-ci`: all dependency, static, ci-lint, duplication and
full pytest/coverage gates passed against the final rebased
implementation: 12,086 passed, 5 skipped, coverage 89.59% (4 workers,
sysmon, 89.5% threshold).
- Linux backend targeted suites passed 31 Platform tests plus 139
existing SDK Webhook proxy tests.
- User's existing authenticated Chrome → normal BFF → real Account
verification → full local claw-interface → real Engine/PostgreSQL →
public HTTPS receiver: paused creation/test, signed receipt, actual 503
retry, enable/pause, normal/immediate secret rotation, single/batch
redelivery and automatic 302 disablement/recovery passed. Switching from
real detail to the user's newly created Project showed its empty list.
- Regression negative controls reproduced receipt-matching, asynchronous
refresh and Project-switch bugs before their fixes. The create API
regression reproduces the review finding (enabled creation returned
201); the fixed schema rejects it with 400 before contacting Engine,
while a separate update still enables delivery.

## Limits
No production deployment, paid model test or staging CSFLE validation.
Local Billing is unconfigured. Delete/pagination/cross-Project
authorization are automated coverage, not claimed as manual live UI
coverage. The local review endpoint remains paused. Full evidence and
scope are recorded in
`docs/superpowers/specs/2026-10-08-platform-webhooks.md`.


## Receipt review validation — 2026-10-09
- Added two UI regressions for an older successful test remaining in
history while a new receipt is unprojected, then pending or dead. Both
fail when the receipt query is removed and pass with it restored.
- Real staging SDK facade -> deployed Engine -> public HTTPS
signature-verifying receiver: the first test succeeded; a different
receipt received 503 and remained pending; a third received 302 and
became dead/http_3xx. Each filtered page excluded the older success. The
first receipt still returned its original success; a nonexistent receipt
returned an empty page.
- Used a dedicated stopped test Agent and paused Webhook. No sessions,
inference or Sandbox runs. All per-probe resources were deleted;
subsequent listing confirmed no test Agent remained.
- Engine production deployment:
https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/37884096329
. Production-full-smoke:
https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/37885299313
. Both passed for c1318164c0935a656d57784d2bae6956db998c8a; these are
release evidence, not a production run of this receipt regression.
- The real staging probe used the machine-key Agent webhook facade. UI
regressions use MSW. The unmerged Platform browser facade has not been
tested as a deployed browser-to-Engine flow; previous authenticated
browser coverage used the full local stack.

## Enabled endpoint edit review fix — 2026-10-09
- Addressed Tim's P2: edit submissions omit `url` whenever the trimmed
address is unchanged. Creation still requires a URL; paused endpoints
still submit changed URLs. The form callback types distinguish full
creation fields from partial update fields.
- Added seven serialized UI request regressions: description, event
types and session scope edits on enabled and paused endpoints, plus URL
changes while paused. The test API returns Engine's 409 whenever an
enabled endpoint receives `url`, even unchanged. Six cases failed before
the fix; all seven pass after it. The existing creation test now asserts
that the URL is included.
- Preview updates enforce the same enabled-URL rejection, with a
regression for rejection, non-URL edits, pause and URL change. The two
relevant suites passed all 43 tests.
- URL fix originally validated at
f4ee15a709acbb8efca2a8087b45521c6db138a7. All Platform and Python gates
above were rerun after the rebase. This follow-up uses
contract-enforcing local UI tests, not a new live browser/Engine test.


## Empty-204 deletion review fix — 2026-10-09
- Addressed [Tim's deletion
P2](https://github.com/SerendipityOneInc/ecap-workspace/pull/4034#discussion_r4227805104):
browser facade preserves an absent upstream Content-Type instead of
labeling the bodyless Engine 204 as JSON. Existing upstream Content-Type
and no-store behavior remain preserved.
- The Platform API client skips response-body parsing on 204, including
when a proxy retains a JSON header. Successful deletion can therefore
close the dialog, invalidate the endpoint list and navigate back. Other
statuses retain their original parsing/error behavior.
- Negative controls: before the fix, the actual FastAPI route's
headerless-upstream regression failed because it added application/json;
the UI deletion regression with JSON-labelled empty 204 failed to
navigate. Both now pass.
- Targeted validation: 172 backend webhook facade tests and 48
UI/API-client/Worker tests passed. API-client tests assert that no
JSON/text parser is called for either form of empty 204.
- Cross-layer local probe: captured the actual FastAPI TestClient
response to a mocked Engine httpx.Response(204), verified empty body and
absent Content-Type, then consumed those exact response headers/status
through the production Worker handler and webhook API client. Probe
passed. This validates response transport with test
authentication/upstream stubs, not deployed browser-to-Engine deletion.
- Rebased onto main 542b009578. At 197a7f351, all Node 24 Platform gates
and full ecap-verify-py-ci passed with the counts above. No live or
production deletion was performed.
```

