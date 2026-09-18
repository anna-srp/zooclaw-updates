---
title: "feat(agents): publish shared agents with manual updates and independent copies (#3773)"
type: "新功能"
priority: "高"
date: "2026-09-17"
status: "待审核"
channels: ""
---

# feat(agents): publish shared agents with manual updates and independent copies (#3773)

## 核心宣传点

分享 Agent 从「复制一份就断联」升级为正式发布机制：作者决定什么时候发版，拿到的人是只读实例并自己决定什么时候更新，也可以随时另存为独立副本。

## PR 说明

## Summary

Sharing an Agent previously created an editable copy with no update path. This change introduces explicitly published, read-only shared instances: authors choose when to publish; recipients choose when to apply an update. Make a copy creates an independently editable Agent with no future update relationship.

- Reuse immutable Revisions for the published pointer. Preview/install pin the shown version; revoking a link blocks new installs while existing recipients keep update access.
- Add manual Update on Shared with me, with explicit confirmation only when an Environment rebuild is needed. Copy source-owned resources into the recipient scope and preserve runtime bindings and user data. Use existing CAS, lifecycle and a small workspace update record; no new release/task collection, scheduler, lease or historical migration.
- Enforce shared-instance write restrictions in the backend and both Home/detail model controls. Make a copy uses the effective local revision; Create Agent's existing “Start from a shared Agent” entry creates an independent copy directly from the published link and opens Build. Ordinary link Preview/Install stays a shared install.
- Keep Publish availability consistent between Build and list dialogs, and show explicit success feedback. Allow shareable Agents using a pinned public base Environment; keep custom-environment source validation.
- Address independent review findings: prepare inactive candidates before claiming an update, validate candidate identity and recheck the base/publication/confirmation before activation, preserve locking for uncertain activation results, complete the mock copy endpoint, and restore unrelated chat-share wording.

## Dependencies and release

Depends on [Engine #1496](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1496) for complete source/Environment replacement. Deployment order: Engine migration `0046` and image → claw-interface → Web. Backend/Web must be coordinated because new installs require the previewed revision. ACS has no code change. Design and implementation/acceptance details are in the two `2026-09-16-agent-share-update-fork` documents.

## Test plan

- [x] Independent backend, Web and Engine reviews; fixes independently re-reviewed.
- [x] Latest targeted tests: Web 379 passed; backend 85 passed. ECAP Web and Python static checks passed, including commit/push gates.
- [x] Earlier feature validation: 343 Agent backend tests and browser mock smoke for Update, copy, shared Build restrictions, publishing and links.
- [x] Latest local existing Engine/ACS lane migrated and healthy; ECAP frontend/backend use this feature checkout.
- [x] Real staging CSFLE repository validation on September 17: publish/fork transactions, competing update claims, uninstall/copy exclusion, atomic completion, retry identity, source scope and revoked-link behavior passed. Run `share_csfle_28d4f746e6dc4c3d814cdd2f45d359aa` created 11 isolated records; exact cleanup and absence checks passed with zero failures. No app lifecycle or Engine calls. Details are recorded in the implementation plan.
- [ ] Complete real sandbox rebuild/recovery and verify preserved files, memory, application data, sessions, connections, tasks and channel delivery before production release.

Full Web testing previously reported three failures in existing Builder/Markdown suites; those files passed all 131 tests when rerun separately. Do not interpret that initial full run as green.

## Review scope

The size override keeps the coupled feature reviewable as one ECAP PR: the repository size check counts 4,041 changed lines after exclusions, including 1,772 test lines and the mock contract. Backend, Web and Engine were reviewed separately; the override does not bypass quality checks.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `09b9faecd042ebbc657d83a161220bced09047a6`
- PR: #3773
- 作者：kaka-srp
- 日期：2026-09-17T09:27:22Z

### Commit Message

```
feat(agents): publish shared agents with manual updates and independent copies (#3773)

## Summary

Sharing an Agent previously created an editable copy with no update
path. This change introduces explicitly published, read-only shared
instances: authors choose when to publish; recipients choose when to
apply an update. Make a copy creates an independently editable Agent
with no future update relationship.

- Reuse immutable Revisions for the published pointer. Preview/install
pin the shown version; revoking a link blocks new installs while
existing recipients keep update access.
- Add manual Update on Shared with me, with explicit confirmation only
when an Environment rebuild is needed. Copy source-owned resources into
the recipient scope and preserve runtime bindings and user data. Use
existing CAS, lifecycle and a small workspace update record; no new
release/task collection, scheduler, lease or historical migration.
- Enforce shared-instance write restrictions in the backend and both
Home/detail model controls. Make a copy uses the effective local
revision; Create Agent's existing “Start from a shared Agent” entry
creates an independent copy directly from the published link and
```
