---
title: "全新「New Chat」入口与会话线程上线"
type: "新功能上线"
priority: "高"
date: "2026-06-08"
status: "待审核"
channels: ""
---

# 全新「New Chat」入口与会话线程上线

## 核心宣传点

现在可以从侧边栏一键发起「New Chat」，并在独立的会话线程里和不同 Agent 分别对话，聊天体验更清晰、更顺手。

## 原始内容

### [SerendipityOneInc/ecap-workspace b089a89] feat(web): activate New Chat from sidebar (#2247)

**Commit Message:**

```
feat(web): activate New Chat from sidebar (#2247)

## Linear

https://linear.app/srpone/issue/ECA-898/sidebar-restructure-three-zone-layout-new-chat-entry

## Summary
Final activation split from #2216, stacked on #2246. This is the PR that
puts the New Chat/session-thread feature online through sidebar and
redirect entry points.

- Add visible New Chat nav entry and localized nav label.
- Restructure sidebar into top nav, scrollable agent/session zone, and
pinned footer.
- Add expandable agent rows with per-agent New chat and past session
links.
- Auto-expand/highlight the active session route's agent.
- Change default logged-in landing/post-auth destinations to /new-chat
while preserving valid specialist landing redirects.

## Production exposure
This is intentionally the activation PR. Earlier stack PRs add hidden
route, API plumbing, and thread behavior without normal navigation
exposure.

## Test plan
- pnpm --dir web/app exec vitest run
tests/unit/app/landing/hooks/useLandingRedirect.unit.spec.ts
tests/unit/app/onboarding/OnboardingSuccessClient.unit.spec.tsx
tests/unit/app/subscription/SuccessClient.unit.spec.tsx
tests/unit/app/user-verify-email-otp.unit.spec.tsx
tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx
tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx
tests/unit/components/sidenav/SideNavBottomNav.unit.spec.tsx
tests/unit/components/sidenav/SideNavUserSection.unit.spec.tsx
tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts
tests/unit/components/sidenav/session-route.unit.spec.ts
tests/unit/lib/landing-context.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

## Stack
- #2244 hidden /new-chat launcher
- #2245 OpenClaw conversation API plumbing
- #2246 session-thread route and hidden send behavior
- This PR: sidebar + redirect activation
```

**PR Description:**

## Linear
https://linear.app/srpone/issue/ECA-898/sidebar-restructure-three-zone-layout-new-chat-entry

## Summary
Final activation split from #2216, stacked on #2246. This is the PR that puts the New Chat/session-thread feature online through sidebar and redirect entry points.

- Add visible New Chat nav entry and localized nav label.
- Restructure sidebar into top nav, scrollable agent/session zone, and pinned footer.
- Add expandable agent rows with per-agent New chat and past session links.
- Auto-expand/highlight the active session route's agent.
- Change default logged-in landing/post-auth destinations to /new-chat while preserving valid specialist landing redirects.

## Production exposure
This is intentionally the activation PR. Earlier stack PRs add hidden route, API plumbing, and thread behavior without normal navigation exposure.

## Test plan
- pnpm --dir web/app exec vitest run tests/unit/app/landing/hooks/useLandingRedirect.unit.spec.ts tests/unit/app/onboarding/OnboardingSuccessClient.unit.spec.tsx tests/unit/app/subscription/SuccessClient.unit.spec.tsx tests/unit/app/user-verify-email-otp.unit.spec.tsx tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx tests/unit/components/sidenav/SideNavBottomNav.unit.spec.tsx tests/unit/components/sidenav/SideNavUserSection.unit.spec.tsx tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts tests/unit/components/sidenav/session-route.unit.spec.ts tests/unit/lib/landing-context.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

## Stack
- #2244 hidden /new-chat launcher
- #2245 OpenClaw conversation API plumbing
- #2246 session-thread route and hidden send behavior
- This PR: sidebar + redirect activation


### [SerendipityOneInc/ecap-workspace 0237ab6] feat(web): add session thread chat route (#2246)

**Commit Message:**

```
feat(web): add session thread chat route (#2246)

## Linear

https://linear.app/srpone/issue/ECA-898/sidebar-restructure-three-zone-layout-new-chat-entry

## Summary
Split 3 from #2216, stacked on #2245. Adds path-based session thread UI
and upgrades hidden /new-chat sends to create a conversation and
redirect into the thread route.

- Add /chat/{computerId}/{agentId}/{sessionId} route and thread client.
- Share chat rendering via OpenClawChatSurface and mmDisplayMessages.
- Add Mattermost get-thread/post fanout support for live thread updates.
- Update hidden /new-chat submit to create a conversation, post the
first message, then route to the session thread.
- Add focused unit coverage for thread route, live thread updates,
shared chat rendering, and new-chat submit behavior.

## Production exposure
This still does not add a sidebar entry, sidebar sessions, landing
redirect, or other visible activation path. /new-chat remains hidden
unless directly visited.

## Test plan
- pnpm --dir web/app exec vitest run
tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx
tests/unit/app/chat-thread/ThreadPostBubble.unit.spec.tsx
tests/unit/app/chat-thread/useConversationThread.unit.spec.tsx
tests/unit/app/chat-thread/useLiveThread.unit.spec.ts
tests/unit/app/chat/OpenClawChatSurface.unit.spec.tsx
tests/unit/app/chat/useChatMessaging.unit.spec.ts
tests/unit/app/chat/useChatPageDerivations.unit.spec.ts
tests/unit/app/chat/useMmChannelSync.unit.spec.ts
tests/unit/app/new-chat/NewChatClient.unit.spec.tsx
tests/unit/hooks/useMmChannelSync.unit.spec.ts
tests/unit/lib/api/openclaw-conversation-threads.unit.spec.ts
tests/unit/lib/api/openclaw-thread-reply.unit.spec.ts
tests/unit/lib/chat/agent-chat-href.unit.spec.ts
tests/unit/lib/mattermost/api-fetch-thread.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

## Stack
- #2244 hidden /new-chat launcher
- #2245 OpenClaw conversation API plumbing
- This PR: session-thread route and hidden send behavior
- Next: sidebar sessions
- Last: sidebar layout/nav activation
```

**PR Description:**

## Linear
https://linear.app/srpone/issue/ECA-898/sidebar-restructure-three-zone-layout-new-chat-entry

## Summary
Split 3 from #2216, stacked on #2245. Adds path-based session thread UI and upgrades hidden /new-chat sends to create a conversation and redirect into the thread route.

- Add /chat/{computerId}/{agentId}/{sessionId} route and thread client.
- Share chat rendering via OpenClawChatSurface and mmDisplayMessages.
- Add Mattermost get-thread/post fanout support for live thread updates.
- Update hidden /new-chat submit to create a conversation, post the first message, then route to the session thread.
- Add focused unit coverage for thread route, live thread updates, shared chat rendering, and new-chat submit behavior.

## Production exposure
This still does not add a sidebar entry, sidebar sessions, landing redirect, or other visible activation path. /new-chat remains hidden unless directly visited.

## Test plan
- pnpm --dir web/app exec vitest run tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx tests/unit/app/chat-thread/ThreadPostBubble.unit.spec.tsx tests/unit/app/chat-thread/useConversationThread.unit.spec.tsx tests/unit/app/chat-thread/useLiveThread.unit.spec.ts tests/unit/app/chat/OpenClawChatSurface.unit.spec.tsx tests/unit/app/chat/useChatMessaging.unit.spec.ts tests/unit/app/chat/useChatPageDerivations.unit.spec.ts tests/unit/app/chat/useMmChannelSync.unit.spec.ts tests/unit/app/new-chat/NewChatClient.unit.spec.tsx tests/unit/hooks/useMmChannelSync.unit.spec.ts tests/unit/lib/api/openclaw-conversation-threads.unit.spec.ts tests/unit/lib/api/openclaw-thread-reply.unit.spec.ts tests/unit/lib/chat/agent-chat-href.unit.spec.ts tests/unit/lib/mattermost/api-fetch-thread.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

## Stack
- #2244 hidden /new-chat launcher
- #2245 OpenClaw conversation API plumbing
- This PR: session-thread route and hidden send behavior
- Next: sidebar sessions
- Last: sidebar layout/nav activation


### [SerendipityOneInc/ecap-workspace 50e2caa] feat(web): add OpenClaw conversation API plumbing (#2245)

**Commit Message:**

```
feat(web): add OpenClaw conversation API plumbing (#2245)

## Linear

https://linear.app/srpone/issue/ECA-898/sidebar-restructure-three-zone-layout-new-chat-entry

## Summary
Split 2 from #2216, stacked on #2244. Adds the additive web
BFF/client/query plumbing needed for OpenClaw computers and
conversations, without exposing new UI.

- Add /api/openclaw computer and conversation BFF routes.
- Add OpenClaw V2 computer-agent types and client functions.
- Add react-query keys/hooks for computers, conversations, and
conversation creation.
- Add focused unit coverage for route handlers, API clients, and query
keys/hooks.

## Production exposure
No sidebar, landing redirect, or visible route activation is added in
this PR.

## Test plan
- pnpm --dir web/app exec vitest run
tests/unit/app/api/openclaw/computer-agents.unit.spec.ts
tests/unit/app/api/openclaw/computers.unit.spec.ts
tests/unit/app/api/openclaw/conversations.unit.spec.ts
tests/unit/hooks/queries/openclaw-conversations.unit.spec.tsx
tests/unit/hooks/queries/openclaw-keys.unit.spec.ts
tests/unit/lib/api/openclaw-computer-agents.unit.spec.ts
tests/unit/lib/api/openclaw-conversations.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

## Stack
- Base: #2244 hidden /new-chat launcher
- Next: session-thread route and thread behavior
- Last: sidebar/nav activation
```

**PR Description:**

## Linear
https://linear.app/srpone/issue/ECA-898/sidebar-restructure-three-zone-layout-new-chat-entry

## Summary
Split 2 from #2216, stacked on #2244. Adds the additive web BFF/client/query plumbing needed for OpenClaw computers and conversations, without exposing new UI.

- Add /api/openclaw computer and conversation BFF routes.
- Add OpenClaw V2 computer-agent types and client functions.
- Add react-query keys/hooks for computers, conversations, and conversation creation.
- Add focused unit coverage for route handlers, API clients, and query keys/hooks.

## Production exposure
No sidebar, landing redirect, or visible route activation is added in this PR.

## Test plan
- pnpm --dir web/app exec vitest run tests/unit/app/api/openclaw/computer-agents.unit.spec.ts tests/unit/app/api/openclaw/computers.unit.spec.ts tests/unit/app/api/openclaw/conversations.unit.spec.ts tests/unit/hooks/queries/openclaw-conversations.unit.spec.tsx tests/unit/hooks/queries/openclaw-keys.unit.spec.ts tests/unit/lib/api/openclaw-computer-agents.unit.spec.ts tests/unit/lib/api/openclaw-conversations.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

## Stack
- Base: #2244 hidden /new-chat launcher
- Next: session-thread route and thread behavior
- Last: sidebar/nav activation


### [SerendipityOneInc/ecap-workspace 3aacb85] feat(claw-interface): split session thread backend follow-up (#2243)

**Commit Message:**

```
feat(claw-interface): split session thread backend follow-up (#2243)

## Linear

https://linear.app/srpone/issue/ECA-896/openclaw-session-threads-per-agent-channel-root-post-id

## Summary
Backend-first split from feat/openclaw-session-threads. This PR carries
the session-thread backend route/provisioning work plus the minimal web
BFF compatibility update needed to keep existing browser-facing
conversation asset/workspace endpoints working after the backend route
move.

- Move OpenClaw conversation asset/workspace backend routes under
`/openclaw/conversation/*` and add the
`/conversations/{computer_id}/{agent_id}` route surface.
- Preserve session-thread behavior, including `root_post_id` and
per-agent `session_channel_id` handling.
- Add deterministic `zoo-session-` Mattermost channel names for
per-agent session channels.
- Add Mattermost org team provisioning/backfill support for session
channel creation.
- Update the existing web BFF `/api/conversation/*` routes to proxy to
`/openclaw/conversation/*` so current frontend callers do not depend on
removed backend `/conversation/*` mounts.

## Rollout / Compatibility
This PR is part of a coordinated stacked rollout, not a user-visible
launch by itself.

Deployment/order contract:
1. Merge/deploy this backend and BFF compatibility PR first.
2. Merge/deploy the web API plumbing PR (#2245) after this backend
surface exists.
3. Merge/deploy the session-thread chat route and sidebar activation PRs
only after the route plumbing is deployed.

Compatibility notes:
- `/openclaw/conversation/sessions` intentionally has no compatibility
shim because it was not used by prior clients before session-channel
conversations moved to `/conversations/{computer_id}/{agent_id}`.
- Existing browser-facing asset/workspace APIs remain stable at
`/api/conversation/assets` and `/api/conversation/workspace/files`;
their BFF proxy target changes to `/openclaw/conversation/*` in this PR.
- The new session UI remains hidden until the later activation PR, so
this change can land before navigation/sidebar exposure.

## Stacked PRs
- #2244 hidden `/new-chat` launcher/route infrastructure.
- #2245 OpenClaw conversation web API plumbing.
- #2246 session-thread chat route.
- #2247 sidebar activation; should be the last user-visible rollout PR.

## Test plan
- [x] .venv/bin/python -m pytest -q
tests/unit/test_agent_workspace_schema.py
tests/unit/test_backfill_mattermost_org_teams.py
tests/unit/test_conversation_routes.py tests/unit/test_conversations.py
tests/unit/test_mattermost_client.py
tests/unit/test_openclaw_conversation.py
tests/unit/test_openclaw_session_channel_repo.py
tests/unit/test_openclaw_session_channel_schema.py
tests/unit/test_openclaw_session_channel_service.py
tests/unit/test_schema_org.py (140 passed)
- [x] .venv/bin/ruff check .
- [x] services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_openclaw_session_channel_service.py
(29 passed)
- [x] services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_conversations.py (5 passed)
- [x] pnpm --dir web/app exec eslint
src/app/api/conversation/assets/route.ts
src/app/api/conversation/workspace/files/route.ts
src/lib/api/conversation-assets.ts
tests/unit/app/api/conversation-assets.unit.spec.ts
tests/unit/app/api/conversation-workspace-files.unit.spec.ts --quiet
--cache --cache-location .eslintcache --cache-strategy content
- [x] pnpm --dir web/app run test:unit --
tests/unit/app/api/conversation-assets.unit.spec.ts
tests/unit/app/api/conversation-workspace-files.unit.spec.ts (broad
Vitest config: 462 passed)
- [ ] pyright app tests (not available locally in this shell; expected
in CI)
```

**PR Description:**

## Linear
https://linear.app/srpone/issue/ECA-896/openclaw-session-threads-per-agent-channel-root-post-id

## Summary
Backend-first split from feat/openclaw-session-threads. This PR carries the session-thread backend route/provisioning work plus the minimal web BFF compatibility update needed to keep existing browser-facing conversation asset/workspace endpoints working after the backend route move.

- Move OpenClaw conversation asset/workspace backend routes under `/openclaw/conversation/*` and add the `/conversations/{computer_id}/{agent_id}` route surface.
- Preserve session-thread behavior, including `root_post_id` and per-agent `session_channel_id` handling.
- Add deterministic `zoo-session-` Mattermost channel names for per-agent session channels.
- Add Mattermost org team provisioning/backfill support for session channel creation.
- Update the existing web BFF `/api/conversation/*` routes to proxy to `/openclaw/conversation/*` so current frontend callers do not depend on removed backend `/conversation/*` mounts.

## Rollout / Compatibility
This PR is part of a coordinated stacked rollout, not a user-visible launch by itself.

Deployment/order contract:
1. Merge/deploy this backend and BFF compatibility PR first.
2. Merge/deploy the web API plumbing PR (#2245) after this backend surface exists.
3. Merge/deploy the session-thread chat route and sidebar activation PRs only after the route plumbing is deployed.

Compatibility notes:
- `/openclaw/conversation/sessions` intentionally has no compatibility shim because it was not used by prior clients before session-channel conversations moved to `/conversations/{computer_id}/{agent_id}`.
- Existing browser-facing asset/workspace APIs remain stable at `/api/conversation/assets` and `/api/conversation/workspace/files`; their BFF proxy target changes to `/openclaw/conversation/*` in this PR.
- The new session UI remains hidden until the later activation PR, so this change can land before navigation/sidebar exposure.

## Stacked PRs
- #2244 hidden `/new-chat` launcher/route infrastructure.
- #2245 OpenClaw conversation web API plumbing.
- #2246 session-thread chat route.
- #2247 sidebar activation; should be the last user-visible rollout PR.

## Test plan
- [x] .venv/bin/python -m pytest -q tests/unit/test_agent_workspace_schema.py tests/unit/test_backfill_mattermost_org_teams.py tests/unit/test_conversation_routes.py tests/unit/test_conversations.py tests/unit/test_mattermost_client.py tests/unit/test_openclaw_conversation.py tests/unit/test_openclaw_session_channel_repo.py tests/unit/test_openclaw_session_channel_schema.py tests/unit/test_openclaw_session_channel_service.py tests/unit/test_schema_org.py (140 passed)
- [x] .venv/bin/ruff check .
- [x] services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_openclaw_session_channel_service.py (29 passed)
- [x] services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_conversations.py (5 passed)
- [x] pnpm --dir web/app exec eslint src/app/api/conversation/assets/route.ts src/app/api/conversation/workspace/files/route.ts src/lib/api/conversation-assets.ts tests/unit/app/api/conversation-assets.unit.spec.ts tests/unit/app/api/conversation-workspace-files.unit.spec.ts --quiet --cache --cache-location .eslintcache --cache-strategy content
- [x] pnpm --dir web/app run test:unit -- tests/unit/app/api/conversation-assets.unit.spec.ts tests/unit/app/api/conversation-workspace-files.unit.spec.ts (broad Vitest config: 462 passed)
- [ ] pyright app tests (not available locally in this shell; expected in CI)


### [SerendipityOneInc/ecap-workspace c271635] fix(chat): add session thread typing parity (#2268)

**Commit Message:**

```
fix(chat): add session thread typing parity (#2268)

## Summary
- reuse the main `/chat` Mattermost typewriter pipeline in
session-thread chat
- rename the session-thread seed command from `/zooclaw-thread` to
`/zoo-thread`
- extract session-thread display message derivation to keep the page
under lint complexity limits

## Local checks
- `pnpm --dir web run lint` passed (enterprise-app warnings only)
- `pnpm --dir web run tsc` failed before typechecking because the root
script passes unsupported `--if-present` to `pnpm exec`
- `pnpm --dir web/app exec tsc --noEmit` passed
- `pnpm --dir web run test:unit` passed: 485 files, 6955 tests passed, 1
skipped, 1 todo
- `ruff check .` passed in `services/claw-interface`
- host `pyright app tests` unavailable: `pyright` not installed
- host backend pytest blocked by host Pydantic warning config mismatch
- devcontainer `pyright app tests` passed
- devcontainer focused `pytest
tests/unit/test_openclaw_session_channel_service.py -q` passed: 29 tests
- devcontainer full `pytest --cov=app --cov-report=term-missing
--cov-fail-under=90 -q` failed on unrelated environment/baseline issues:
deptry tests cannot resolve the host git worktree path inside the
container, and total coverage is 88.10% under the 90% gate
```

**PR Description:**

## Summary
- reuse the main `/chat` Mattermost typewriter pipeline in session-thread chat
- rename the session-thread seed command from `/zooclaw-thread` to `/zoo-thread`
- extract session-thread display message derivation to keep the page under lint complexity limits

## Local checks
- `pnpm --dir web run lint` passed (enterprise-app warnings only)
- `pnpm --dir web run tsc` failed before typechecking because the root script passes unsupported `--if-present` to `pnpm exec`
- `pnpm --dir web/app exec tsc --noEmit` passed
- `pnpm --dir web run test:unit` passed: 485 files, 6955 tests passed, 1 skipped, 1 todo
- `ruff check .` passed in `services/claw-interface`
- host `pyright app tests` unavailable: `pyright` not installed
- host backend pytest blocked by host Pydantic warning config mismatch
- devcontainer `pyright app tests` passed
- devcontainer focused `pytest tests/unit/test_openclaw_session_channel_service.py -q` passed: 29 tests
- devcontainer full `pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` failed on unrelated environment/baseline issues: deptry tests cannot resolve the host git worktree path inside the container, and total coverage is 88.10% under the 90% gate



### [SerendipityOneInc/ecap-workspace e975d49] fix(web): align session chat and new chat actions (#2272)

**Commit Message:**

```
fix(web): align session chat and new chat actions (#2272)

## Summary
- enable session chat topbar Files and Settings panels
- align session main-agent topbar identity with the sidebar main
identity
- source /new-chat Start with a task cards from agent catalog
quick_commands

## Root cause
Session chat reused the shared header but had no-op panel handlers and
treated the main session route as a pack agent. /new-chat still used
local cold-start defaults instead of catalog quick_commands.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit --pretty false
--noErrorTruncation
- [x] pnpm --dir web run test:unit

Note: pnpm --dir web run tsc currently fails because the repo script
expands to pnpm -r --workspace-concurrency=1 --if-present exec tsc
--noEmit, and this pnpm rejects --if-present for exec.
```

**PR Description:**

## Summary
- enable session chat topbar Files and Settings panels
- align session main-agent topbar identity with the sidebar main identity
- source /new-chat Start with a task cards from agent catalog quick_commands

## Root cause
Session chat reused the shared header but had no-op panel handlers and treated the main session route as a pack agent. /new-chat still used local cold-start defaults instead of catalog quick_commands.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit --pretty false --noErrorTruncation
- [x] pnpm --dir web run test:unit

Note: pnpm --dir web run tsc currently fails because the repo script expands to pnpm -r --workspace-concurrency=1 --if-present exec tsc --noEmit, and this pnpm rejects --if-present for exec.

