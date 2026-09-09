---
title: "组织里别人上传的 Agent 包，现在每个成员都能在「我的 Agent」里看到并安装了"
type: "Bug Fix"
priority: "中"
date: "2026-09-08"
status: "待审核"
channels: "Discord+changelog"
---

# 组织里别人上传的 Agent 包，现在每个成员都能在「我的 Agent」里看到并安装了

## 核心宣传点

如果你的组织管理员通过组织后台上传了 Agent 包，之前组织里的其他成员在 `/agent-builder/my-agents` 页面是**找不到**它们的——列表只显示「你自己发布的」，管理员传的那些像是没存在过，想装也无从下手。

这次在「我的 Agent」页加了一个 **My organization（我的组织）** 标签页，专门列出组织内**由其他成员发布**的活跃 Agent 包，成员终于能自己找到并安装。

有意思的是这不是后端缺数据：`GET /orgs/{org}/packs` 一直就返回组织的全部 pack，资源读取权限也一直允许组织内任何当前成员访问。数据和权限都在那儿，**是前端把它们藏起来了**——`my-agents/useViewModel.ts` 里有一句按 `pack.published_by === currentUserId` 的过滤，而这份被过滤后的列表正是喂给卡片网格的可见列表。删掉这层过滤即可。

同时做了权限收口：把「分享 / 上架到 marketplace / 废弃 / 编辑技能」这些属主专属操作挪到一个新的 `canManage`（= 发布者本人或组织管理员）判断后面。也就是说，**放开可见性不等于放开处置权**——你能看到、能安装同事的包，但不能拿它去分享或变现。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `e7423998`
- PR: #3666
- 日期: 2026-09-08

### Commit Message

```
fix(agents): show org-published packs to every member of the org (#3666)

## Summary
- Adds a **My organization** tab to `/agent-builder/my-agents` listing
the org's active agent packs published by *other* members, so an org
member can finally find and install agents their org admin uploaded
through the org dashboard.
- Gates owner-only listing actions (Share / List on marketplace /
Deprecate / Edit skills) behind a new `canManage` =
publisher-or-org-admin, so widening visibility does not let any member
share or monetize a teammate's pack.
- Renames the view model's `owned: {error, isLoading}` to `orgPacks`,
since one org-pack query now backs two tabs.

No backend change: `GET /orgs/{org}/packs` is already gated only by
`require_matching_current_org` and returns every org pack, and
`pack_asset_access_service` already allows any current member of the org
to read the pack asset. The data and the permission were always there;
only the front end was hiding them.

## Root cause
`my-agents/useViewModel.ts` filtered the org pack list to
`pack.published_by === currentUserId`, and that filtered list is what
feeds `visiblePackIds` down to the card grid (`MyAgentsCatalog.tsx`). So
a pack was visible only to the single account that published it. The
public marketplace never shows org packs either — `list_agent_packs`
hard-scopes to `ZOOCLAW_ORG_ID` by design — which left org-uploaded
agents with no surface at all for anybody except their publisher.

Concretely, in one production org: four active org packs, all
`published_by` the org admin, 12 members. Eleven of them saw an empty
tab, and eight had no org agent installed at all.

Scope note: only packs with `status === 'active'` from other members are
shown, so another member's draft or in-review work stays private to
them. Your own packs keep appearing in "Owned by me" at every status,
exactly as before.

## Test plan
- [x] `bash scripts/verify-web.sh` — tsc, 9488 vitest tests, eslint, all
green
- [x] New unit coverage in `tests/unit/app/agent-builder/my-agents/`:
- org-scope routing (teammate packs land in the new tab, own packs stay
in "Owned by me")
  - teammate `draft` / `deprecated` packs excluded from the org scope
  - both scopes empty before the signed-in identity resolves
- the org tab renders its pack ids, and its own empty state rather than
the owned one
- ownership gate, both directions: a non-admin member gets no
Share/List/Edit-skills and a disabled Delete with a reason, while an org
admin keeps all of them on the same pack
- [ ] Not covered locally: no E2E exists for this route;
`web-build-check` and the other CI suites remain the gate.
```

## 备注

发布状态：已合并待发版（尚未包含在最新的 `ecap-*-release` 前端正式发布中）。
