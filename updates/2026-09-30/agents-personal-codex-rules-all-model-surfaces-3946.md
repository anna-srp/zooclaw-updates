---
title: "个人 Codex 订阅模型在所有改模型的入口都生效：Pack 更新不再把它换回默认模型"
type: "Bug Fix"
priority: "中"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 个人 Codex 订阅模型在所有改模型的入口都生效：Pack 更新不再把它换回默认模型

## 核心宣传点

此前只有编辑 Agent 的编辑器里修好了个人 Codex 模型的选择，这次把同一套规则铺到所有会展示或修改 Agent 模型的地方。Pack 更新和发布分发不再把当前的个人 Codex 模型当作已撤回而替换成 Pack 默认值（原先这么做会让引擎直接丢掉绑定）。退出订阅时会恢复 Revision 里的默认模型：对已绑定的自演进 Agent，改模型必须与工作 Revision 的主模型一致，否则返回 409 并提示去「编辑 Agent」里改默认值；如果读不到 Revision，退出通道保持开放。绑定 Codex 模型现在需要通过验证邮箱的预览准入，不再只看总开关，退出订阅则不设限制。前端把工作区（编辑 Agent 与任务视图）和新建对话入口统一到同一套模型流程：可编辑的 Revision 保持既有行为，任务视图和共享副本只能恢复默认。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已随正式 release 上线

## PR 说明

## Summary

#3930 fixed personal Codex selection in the Edit Agent composer. This PR
applies the same rules to every other surface that shows or changes an
Agent model. Spec:
`docs/superpowers/specs/2026-09-30-codex-model-surfaces.md`.

**Backend (claw-interface)**
- **Pack updates keep personal models.** `model_primary_for_update` no
longer treats a current `openai-codex/` model as withdrawn. Owner
updates and the publisher fan-out (`pack_skill_edits` →
`pack_skill_agent_update_service`) no longer replace it with the Pack
default, which used to make Engine drop the binding.
- **Leaving a subscription restores the Revision default.** On a bound
self-evolving Agent, a platform `PUT /agents/{id}/model` must match the
working Revision's `model_primary`. Any other model returns 409
`agent_revision.settings_required`, which directs the user to change the
default in Edit Agent. If the Revision cannot be read, the exit stays
open. The response now reports `model_managed` the same way the next
read does.
- **Binding a Codex model needs preview admission.** `PUT
/agents/{id}/model` with an `openai-codex/` model now requires the
verified-email admission, not only the master switch. Leaving a
subscription stays ungated.

**Web**
- **One shared flow.** `useAgentModelFlow` (moved from #3930's
`useWorkspaceModelFlow`) now drives the Agent workspace (Edit Agent and
task view) and the New Chat launcher:
  - editable Revisions keep the #3930 behaviour;
- task view and shared copies can only restore the Revision default
while bound;
- ordinary Engine Agents list, bind and label personal models in the
launcher.
- **Agent Settings.** The Default model section shows the active
personal model. Saving a different default clears the binding after the
commit. Saving an unchanged default keeps it. A failed clear stays
visible and can be retried.
- **Broken bindings.** A binding whose connection is missing or not
connected is labelled in the composer. The Codex dialog shows it with
its status, Reconnect (the user then picks the model again from the new
connection) and Disconnect. Disconnect and model refresh also reread the
Agent models.
- **Bound but no longer admitted.** A binding that outlived preview
admission gets a restricted dialog with Disconnect and the exit hint.
While discovery is loading or has failed, the state is treated as
unknown, not as restricted.

**iOS** is a separate PR, #3947. This branch briefly contained those
commits; the last commit reverts them, so this PR's diff has no iOS
changes.

## Root cause

Personal subscriptions are runtime bindings layered on the Agent's
platform model (#3923). Only the workspace hook added in #3930 handled
that; every other writer still assumed platform models only:

- Pack in-place update keeps the owner's model only if the platform
catalog still offers it (#3851). A Codex model is never in that catalog,
so it looked withdrawn and was replaced.
- The runtime PUT accepted any platform model when leaving a
subscription. Revision-managed Agents therefore diverged from their
Revision, and the next Revision render silently reset them.
- New Chat, Agent Settings and iOS had no subscription awareness. They
showed a stale model, could not bind, or cleared the binding without
telling the user.
- The Codex dialog hid bindings that were not connected or no longer
admitted, so there was no way to repair or leave them.

## Test plan

- [x] Backend, `bash scripts/verify-py.sh` (ruff, format, pyright,
import-linter): passed.
- [x] Backend, targeted pytest over 12 files: 278 passed. Each new test
fails against the unfixed code:
  - Pack update fix: 3 fail;
  - Revision-default exit: 6 fail;
  - admission gate: 3 fail;
  - response `model_managed`: 1 fails.
- [x] Web, `bash scripts/verify-web.sh <changed tests>`: 213 passed.
- [x] Web, wider vitest over every spec that imports a changed module
plus `tests/unit/app/agents`: 89 files, 1249 tests passed.
- [x] Web, `tsc --noEmit --incremental false` and `eslint --no-cache` on
the changed files: passed.
- [x] Combined branch, `bash scripts/verify-changed.sh` (web guards,
tsc, eslint; ruff, format, pyright, import-linter): all changed surfaces
passed.
- [ ] Staging check with an admitted account:
  - bind and leave in task view, Edit Agent, Settings and New Chat;
  - Pack update of a bound Agent;
  - disconnect and reconnect.

## Deployment

- Deploy claw-interface and web together. Web restricts task-view exits
to the Revision default and rereads the model after a clear, so it also
behaves correctly against the current backend.
- No Engine change and no data migration.

## Related

- iOS Agent Settings: #3947 (independent of this PR; it also works
against the current backend)
- Agent Builder's own model contract: #3941
- Unified model selector for every surface: #3942

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `799281b3d9712a87c5a9bf241cbe9a9e1a9689a3`
- PR: #3946
- 作者：Chris@ZooClaw
- 日期：2026-09-30T07:38:55Z

### Commit Message

```
fix(agents): apply personal Codex rules on every model surface (#3946)

## Summary

#3930 fixed personal Codex selection in the Edit Agent composer. This PR
applies the same rules to every other surface that shows or changes an
Agent model. Spec:
`docs/superpowers/specs/2026-09-30-codex-model-surfaces.md`.

**Backend (claw-interface)**
- **Pack updates keep personal models.** `model_primary_for_update` no
longer treats a current `openai-codex/` model as withdrawn. Owner
updates and the publisher fan-out (`pack_skill_edits` →
`pack_skill_agent_update_service`) no longer replace it with the Pack
default, which used to make Engine drop the binding.
- **Leaving a subscription restores the Revision default.** On a bound
self-evolving Agent, a platform `PUT /agents/{id}/model` must match the
working Revision's `model_primary`. Any other model returns 409
`agent_revision.settings_required`, which directs the user to change the
default in Edit Agent. If the Revision cannot be read, the exit stays
open. The response now reports `model_managed` the same way the next
read does.
- **Binding a Codex model needs preview admission.** `PUT
/agents/{id}/model` with an `openai-codex/` model now requires the
verified-email admission, not only the master switch. Leaving a
subscription stays ungated.

**Web**
- **One shared flow.** `useAgentModelFlow` (moved from #3930's
`useWorkspaceModelFlow`) now drives the Agent workspace (Edit Agent and
task view) and the New Chat launcher:
  - editable Revisions keep the #3930 behaviour;
- task view and shared copies can only restore the Revision default
while bound;
- ordinary Engine Agents list, bind and label personal models in the
launcher.
- **Agent Settings.** The Default model section shows the active
personal model. Saving a different default clears the binding after the
commit. Saving an unchanged default keeps it. A failed clear stays
visible and can be retried.
- **Broken bindings.** A binding whose connection is missing or not
connected is labelled in the composer. The Codex dialog shows it with
its status, Reconnect (the user then picks the model again from the new
connection) and Disconnect. Disconnect and model refresh also reread the
Agent models.
- **Bound but no longer admitted.** A binding that outlived preview
admission gets a restricted dialog with Disconnect and the exit hint.
While discovery is loading or has failed, the state is treated as
unknown, not as restricted.

**iOS** is a separate PR, #3947. This branch briefly contained those
commits; the last commit reverts them, so this PR's diff has no iOS
changes.

## Root cause

Personal subscriptions are runtime bindings layered on the Agent's
platform model (#3923). Only the workspace hook added in #3930 handled
that; every other writer still assumed platform models only:

- Pack in-place update keeps the owner's model only if the platform
catalog still offers it (#3851). A Codex model is never in that catalog,
so it looked withdrawn and was replaced.
- The runtime PUT accepted any platform model when leaving a
subscription. Revision-managed Agents therefore diverged from their
Revision, and the next Revision render silently reset them.
- New Chat, Agent Settings and iOS had no subscription awareness. They
showed a stale model, could not bind, or cleared the binding without
telling the user.
- The Codex dialog hid bindings that were not connected or no longer
admitted, so there was no way to repair or leave them.

## Test plan

- [x] Backend, `bash scripts/verify-py.sh` (ruff, format, pyright,
import-linter): passed.
- [x] Backend, targeted pytest over 12 files: 278 passed. Each new test
fails against the unfixed code:
  - Pack update fix: 3 fail;
  - Revision-default exit: 6 fail;
  - admission gate: 3 fail;
  - response `model_managed`: 1 fails.
- [x] Web, `bash scripts/verify-web.sh <changed tests>`: 213 passed.
- [x] Web, wider vitest over every spec that imports a changed module
plus `tests/unit/app/agents`: 89 files, 1249 tests passed.
- [x] Web, `tsc --noEmit --incremental false` and `eslint --no-cache` on
the changed files: passed.
- [x] Combined branch, `bash scripts/verify-changed.sh` (web guards,
tsc, eslint; ruff, format, pyright, import-linter): all changed surfaces
passed.
- [ ] Staging check with an admitted account:
  - bind and leave in task view, Edit Agent, Settings and New Chat;
  - Pack update of a bound Agent;
  - disconnect and reconnect.

## Deployment

- Deploy claw-interface and web together. Web restricts task-view exits
to the Revision default and rereads the model after a clear, so it also
behaves correctly against the current backend.
- No Engine change and no data migration.

## Related

- iOS Agent Settings: #3947 (independent of this PR; it also works
against the current backend)
- Agent Builder's own model contract: #3941
- Unified model selector for every surface: #3942

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

来源：SerendipityOneInc/ecap-workspace @ 799281b3，PR #3946，作者 Chris@ZooClaw。
