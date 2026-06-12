---
title: "修复回放分享选择过多消息时报错"
type: "Bug Fix"
priority: "中"
date: "2026-06-11"
status: "待审核"
channels: ""
---

# 修复回放分享选择过多消息时报错

## 核心宣传点
修复了在回放分享中选择超过 200 条消息时提交报错（HTTP 422）的问题，长对话分享更稳定。

## 原始内容
```
fix(ecap-website): auto-triage ECA-821 (#2373)

## Linear issue

[ECA-821](https://linear.app/srpone/issue/ECA-821/frontend-http-422-errors-from-ecap-website)
— Frontend HTTP 422 errors from ecap-website

**Affected service**: `ecap-website`
**Triage LLM confidence**: 0.2 / 1.0
**Triage LLM verification cost**: low *(auto-PR gate passed)*

## Root cause
The chat replay share UI allowed users to select every currently visible
Mattermost message and submit all selected post IDs to `POST
/api/chat-replays`, while `claw-interface` validates `post_ids` with a
hard maximum of 200. Long conversations could therefore send more than
200 IDs in both `postIds` and `orderedMessageIds`, causing
FastAPI/Pydantic to reject the request with HTTP 422.

## Fix
- Mirrored the backend's 200-post replay share limit in the frontend
`useChatReplayShare` flow.
- Capped the "select visible" action to the first 200 visible shareable
messages and surfaced an actionable selection-limit error.
- Added a defensive create-time guard so oversized selections cannot
call `createReplay`.
- Added unit coverage for capped select-visible behavior and the
no-request oversized-create guard.

## Verification plan
1. Open Sentry event ECAP-WEBSITE-N6 for the full trace and request
context.
2. Retrieve the FastAPI 422 response body from backend logs to see which
field validation failed.
3. Reproduce the failing request locally.
4. Verify the fix eliminates the 422 response; confirm with a targeted
unit/integration test on the affected endpoint.

## Risks / scope
Users sharing very long conversations now get only the first 200 visible
selected messages when using "select all visible"; they must manually
narrow or load a smaller range if they need a different subset.
Reviewers should check that the selected order still matches display
order and that the client-side limit remains aligned with
`MAX_SELECTED_POSTS` in the backend schema.

---
*This PR was opened automatically by the ECAP error-scanner. The bug
report came from production telemetry; the analysis and fix candidate
were produced by an LLM. Please review carefully — the triage LLM marked
this as `verification_cost: low` (meaning CI should suffice), but human
judgment overrides.*

*Auto-merge is disabled for `auto-triage` labeled PRs; merging requires
explicit human approval.*

---------

Co-authored-by: ecap-error-scanner[bot] <ecap-error-scanner[bot]@users.noreply.github.com>
Co-authored-by: chris-srp <chris@srp.one>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>

--- PR Description ---

## Linear issue
[ECA-821](https://linear.app/srpone/issue/ECA-821/frontend-http-422-errors-from-ecap-website) — Frontend HTTP 422 errors from ecap-website

**Affected service**: `ecap-website`
**Triage LLM confidence**: 0.2 / 1.0
**Triage LLM verification cost**: low *(auto-PR gate passed)*

## Root cause
The chat replay share UI allowed users to select every currently visible Mattermost message and submit all selected post IDs to `POST /api/chat-replays`, while `claw-interface` validates `post_ids` with a hard maximum of 200. Long conversations could therefore send more than 200 IDs in both `postIds` and `orderedMessageIds`, causing FastAPI/Pydantic to reject the request with HTTP 422.

## Fix
- Mirrored the backend's 200-post replay share limit in the frontend `useChatReplayShare` flow.
- Capped the "select visible" action to the first 200 visible shareable messages and surfaced an actionable selection-limit error.
- Added a defensive create-time guard so oversized selections cannot call `createReplay`.
- Added unit coverage for capped select-visible behavior and the no-request oversized-create guard.

## Verification plan
1. Open Sentry event ECAP-WEBSITE-N6 for the full trace and request context.
2. Retrieve the FastAPI 422 response body from backend logs to see which field validation failed.
3. Reproduce the failing request locally.
4. Verify the fix eliminates the 422 response; confirm with a targeted unit/integration test on the affected endpoint.

## Risks / scope
Users sharing very long conversations now get only the first 200 visible selected messages when using "select all visible"; they must manually narrow or load a smaller range if they need a different subset. Reviewers should check that the selected order still matches display order and that the client-side limit remains aligned with `MAX_SELECTED_POSTS` in the backend schema.

---
*This PR was opened automatically by the ECAP error-scanner. The bug report came from production telemetry; the analysis and fix candidate were produced by an LLM. Please review carefully — the triage LLM marked this as `verification_cost: low` (meaning CI should suffice), but human judgment overrides.*

*Auto-merge is disabled for `auto-triage` labeled PRs; merging requires explicit human approval.*

```
