---
title: "技能商店重新开放，可为电脑 Agent 安装技能"
type: "Skill 上架/更新"
priority: "中"
date: "2026-07-10"
status: "待审核"
channels: ""
---

## 核心宣传点

技能商店（Skills Store）重新回到菜单，现在可以直接为你的电脑 Agent 浏览并安装技能，安装流程已适配最新的 Agent 体系。

## 原始内容

**feat(web): re-enable skills store for computer agents (#2824)**

SHA: `07d251d466d6b637c770905fd043a778e46a9de7` | 作者: bill-srp | PR #2824

```
feat(web): re-enable skills store for computer agents (#2824)

# Summary

Frontend slice of the skill-store re-enable: migrates the Skills Store
pages to the V2 computer-agents model and restores the hidden UserMenu
entry. Companion to backend PR #2823 (merged), which added
`agent_id`-based workdir resolution to the clawhub endpoints.

Background: the Skills Store entry was removed from UserMenu in #2569
because the store's install flow was still keyed on the legacy
`useUserAgents` data while the rest of the app moved to V2 computer
agents.

- **BFF** (`api/openclaw/clawhub/[action]/route.ts`): forwards
`agent_id` (query param on list, body field on install/uninstall)
instead of `workdir`; computer resolution / readiness polling / credits
check unchanged.
- **API client** (`lib/api/skills-store.ts`): request types switch from
`workdir` to `agentId`, sent as `agent_id` on the wire.
- **Store pages** (`SkillsSearchClient`, `SkillDetailClient`): migrated
from `useUserAgents` to `useCurrentComputerAgents`, filtered to
runtime-visible agents — consistent with the rest of the app.
- **`lib/skills/agent-install-state.ts`**: workspace-path logic deleted
entirely (`getAgentWorkspace` / `hasAgentWorkspace` /
`DEFAULT_MAIN_AGENT_WORKSPACE`); install state keyed purely by
`agent_id`; `SkillStoreInstalledAgent` now carries `avatar_url` instead
of `emoji`/`workspace`.
- **`useAgentInstalledSkills`**: converted from a hand-rolled
`useEffect` fetcher to React Query, keyed by uid + computer_id + sorted
agent ids.
- **UserMenu**: Skills Store entry restored (navigates to
`/skills/search`), guard test flipped back to the navigation assertion.

# Test Plan

- [x] Updated/added unit specs: BFF route (`openclaw-clawhub`,
`clawhub-polling`), `skills-store` API client, `agent-install-state`,
`useAgentInstalledSkills` (new), `SkillAgentComponents` (new),
`SkillDetailClient`, `SkillsSearchClient`, install-toast integration,
`UserMenu`
- [x] Full `pnpm exec vitest run`: 567 files, 7,576 passed / 0 failed
- [x] `bash scripts/verify-web.sh`: guards + tsc + vitest + eslint all
passed
- [ ] Staging smoke after deploy: open Skills Store from UserMenu,
list/install/uninstall a community skill on main and a non-main agent

# Notes

- Deploy ordering: backend #2823 is already merged; this PR must not be
released to production before a `claw-interface` release containing
#2823 is live (the BFF now sends `agent_id`, which old backends ignore —
that would silently target the main workspace).
- The store previously relied on legacy `useUserAgents`; this PR removes
the store's last dependency on it.
```

### PR body

# Summary

Frontend slice of the skill-store re-enable: migrates the Skills Store pages to the V2 computer-agents model and restores the hidden UserMenu entry. Companion to backend PR #2823 (merged), which added `agent_id`-based workdir resolution to the clawhub endpoints.

Background: the Skills Store entry was removed from UserMenu in #2569 because the store's install flow was still keyed on the legacy `useUserAgents` data while the rest of the app moved to V2 computer agents.

- **BFF** (`api/openclaw/clawhub/[action]/route.ts`): forwards `agent_id` (query param on list, body field on install/uninstall) instead of `workdir`; computer resolution / readiness polling / credits check unchanged.
- **API client** (`lib/api/skills-store.ts`): request types switch from `workdir` to `agentId`, sent as `agent_id` on the wire.
- **Store pages** (`SkillsSearchClient`, `SkillDetailClient`): migrated from `useUserAgents` to `useCurrentComputerAgents`, filtered to runtime-visible agents — consistent with the rest of the app.
- **`lib/skills/agent-install-state.ts`**: workspace-path logic deleted entirely (`getAgentWorkspace` / `hasAgentWorkspace` / `DEFAULT_MAIN_AGENT_WORKSPACE`); install state keyed purely by `agent_id`; `SkillStoreInstalledAgent` now carries `avatar_url` instead of `emoji`/`workspace`.
- **`useAgentInstalledSkills`**: converted from a hand-rolled `useEffect` fetcher to React Query, keyed by uid + computer_id + sorted agent ids.
- **UserMenu**: Skills Store entry restored (navigates to `/skills/search`), guard test flipped back to the navigation assertion.

# Test Plan

- [x] Updated/added unit specs: BFF route (`openclaw-clawhub`, `clawhub-polling`), `skills-store` API client, `agent-install-state`, `useAgentInstalledSkills` (new), `SkillAgentComponents` (new), `SkillDetailClient`, `SkillsSearchClient`, install-toast integration, `UserMenu`
- [x] Full `pnpm exec vitest run`: 567 files, 7,576 passed / 0 failed
- [x] `bash scripts/verify-web.sh`: guards + tsc + vitest + eslint all passed
- [ ] Staging smoke after deploy: open Skills Store from UserMenu, list/install/uninstall a community skill on main and a non-main agent

# Notes

- Deploy ordering: backend #2823 is already merged; this PR must not be released to production before a `claw-interface` release containing #2823 is live (the BFF now sends `agent_id`, which old backends ignore — that would silently target the main workspace).
- The store previously relied on legacy `useUserAgents`; this PR removes the store's last dependency on it.

