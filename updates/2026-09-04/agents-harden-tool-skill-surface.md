---
title: "Agent 主人可以「收权」了：给自家 Agent 关掉不想让它碰的工具和技能"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-04"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---

# Agent 主人可以「收权」了：给自家 Agent 关掉不想让它碰的工具和技能

## 核心宣传点

以前雇一个 Engine Agent，它一出生就拿着完整的工具清单，全局技能也是全都可用，而在用户能看到的界面上没有任何地方能把这些能力**拿走**——工具策略和单个技能的开关都属于受控字段，claw-interface 也没有对外暴露过写它们的接口。想给已经在跑的 Agent 做限制，只能找带服务令牌的运维手动改。

这个缺口是有真实代价的，`cron`（定时任务）是最扎手的例子：Agent 自己建的定时计划可以不带明确的验收目标，也就是说模型给自己排的活会在无人值守的情况下自动跑，没人把关。别的高权限工具同理——你可能只想让某个 Agent 老老实实写文档，但它手上却握着能发消息、能执行命令的全套家伙。

现在新增了 `POST /agents/{workspace_id}/harden`，这是第一个面向用户的「削权」入口：作为 Agent 的拥有者，你可以把这个 Agent 的工具面和全局技能面收窄到你真正需要的范围，多余的能力直接关掉。收权是单向收敛的语义，不会因为后台默认清单变化而被悄悄放回来，避免「关了又自己长回来」这种最难排查的情况。

适合的场景：跑无人值守自动化的 Agent 只留必要工具；共享给团队的 Agent 关掉对外发消息的能力；做敏感数据处理的 Agent 关掉网络类工具。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `26910f7f0b8d78d31ad68ddde26717b724bb1848`
- PR: #3630
- 作者: siqiao-srp
- 日期: 2026-09-04T04:08:06Z

### Commit Message

```
feat(agents): let an owner narrow an agent's tool and skill surface (#3630)

## What

`POST /agents/{workspace_id}/harden` — the first user-facing way to take
tools and global skills *away* from an engine agent.

An engine agent is created with the full tool manifest and every global
skill eligible, and nothing on the user-facing surface could take either
away: `tool_policy` and per-skill enablement are controld fields, and
claw-interface exposed no route that writes them. Restricting a hired
agent required an operator with a service token.

The gap has a concrete cost. `cron` is the sharpest case: an
agent-created schedule may not carry an outcome (design/18 D-O3), so
anything a model schedules for itself runs unattended with no acceptance
criterion and delivers whatever it produced. `write` / `edit` let a
model author the raw values a research agent is supposed to obtain from
tools. A research desk carrying a video generator and a slide builder
has more ways to answer a question with the wrong tool.

## Shape

- Denies six tools: `cron`, `edit`, `message`, `user_asset_delete`,
`user_asset_upsert`, `write`.
- Disables every **global**-scope skill outside a small keep list
(`xlsx`, `docx`, `pdf`, `feishu-doc`, `feishu-drive`) that the frontdesk
routing map needs for file work. Org- and pack-scope skills are never
touched.
- **Takes no request body, on purpose.** An endpoint that accepts a
policy can also *widen* one, which would put a way to hand `write` or
`cron` back to a model on the user-facing surface. This one only ever
narrows, to a set the server owns, so there is nothing to review per
call. Restoring the full manifest stays an operator action
(`tool_policy: {}`) on the control plane.
- Idempotent: skills the engine already excludes are skipped, not
re-disabled.
- A skill the engine refuses lands in `failed_skills` instead of
aborting the pass — the tool policy has already been written by then,
and an all-or-nothing failure would tell the caller nothing it could act
on. The reported reason is the domain code, never the upstream message.
- Authorization is the same as the neighbouring v2 routes: owner-scoped
workspace lookup plus `require_agents_v2`.

## Engine client

Two new methods, both deliberately separate from the existing ones:

- `set_agent_tool_policy` — not a field on `update_agent()`, because
`tool_policy` is replace-on-write in controld while that call merges,
and a merging caller would silently keep a policy it meant to drop.
- `set_agent_skill_enabled` — not `put_agent_skill()`, because a global
skill has no version pin this service owns; the body carries `enabled`
alone.

## Tests

30 new: 11 route tests driven over HTTP with `TestClient` (owner path,
no-body-cannot-widen, idempotent second call, 404s for
unknown/hidden/deleted/uninstalled/kill-switch-off with the engine never
called, partial failure reported, tool-policy failure surfacing as 503),
6 service tests, 4 engine-client contract tests, plus one asserting the
route is reachable on the real `create_app()` via the OpenAPI schema.

Verified against staging: `/agents/{workspace_id}/harden` currently
answers 404 there while `/skills` and `/model` answer 401, i.e. the
route is genuinely new.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NwcPcWHHzuTsqy1dU8RJgj

---------

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
```

### PR Body

```
## What

`POST /agents/{workspace_id}/harden` — the first user-facing way to take tools and global skills *away* from an engine agent.

An engine agent is created with the full tool manifest and every global skill eligible, and nothing on the user-facing surface could take either away: `tool_policy` and per-skill enablement are controld fields, and claw-interface exposed no route that writes them. Restricting a hired agent required an operator with a service token.

The gap has a concrete cost. `cron` is the sharpest case: an agent-created schedule may not carry an outcome (design/18 D-O3), so anything a model schedules for itself runs unattended with no acceptance criterion and delivers whatever it produced. `write` / `edit` let a model author the raw values a research agent is supposed to obtain from tools. A research desk carrying a video generator and a slide builder has more ways to answer a question with the wrong tool.

## Shape

- Denies six tools: `cron`, `edit`, `message`, `user_asset_delete`, `user_asset_upsert`, `write`.
- Disables every **global**-scope skill outside a small keep list (`xlsx`, `docx`, `pdf`, `feishu-doc`, `feishu-drive`) that the frontdesk routing map needs for file work. Org- and pack-scope skills are never touched.
- **Takes no request body, on purpose.** An endpoint that accepts a policy can also *widen* one, which would put a way to hand `write` or `cron` back to a model on the user-facing surface. This one only ever narrows, to a set the server owns, so there is nothing to review per call. Restoring the full manifest stays an operator action (`tool_policy: {}`) on the control plane.
- Idempotent: skills the engine already excludes are skipped, not re-disabled.
- A skill the engine refuses lands in `failed_skills` instead of aborting the pass — the tool policy has already been written by then, and an all-or-nothing failure would tell the caller nothing it could act on. The reported reason is the domain code, never the upstream message.
- Authorization is the same as the neighbouring v2 routes: owner-scoped workspace lookup plus `require_agents_v2`.

## Engine client

Two new methods, both deliberately separate from the existing ones:

- `set_agent_tool_policy` — not a field on `update_agent()`, because `tool_policy` is replace-on-write in controld while that call merges, and a merging caller would silently keep a policy it meant to drop.
- `set_agent_skill_enabled` — not `put_agent_skill()`, because a global skill has no version pin this service owns; the body carries `enabled` alone.

## Tests

30 new: 11 route tests driven over HTTP with `TestClient` (owner path, no-body-cannot-widen, idempotent second call, 404s for unknown/hidden/deleted/uninstalled/kill-switch-off with the engine never called, partial failure reported, tool-policy failure surfacing as 503), 6 service tests, 4 engine-client contract tests, plus one asserting the route is reachable on the real `create_app()` via the OpenAPI schema.

Verified against staging: `/agents/{workspace_id}/harden` currently answers 404 there while `/skills` and `/model` answer 401, i.e. the route is genuinely new.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NwcPcWHHzuTsqy1dU8RJgj
```
