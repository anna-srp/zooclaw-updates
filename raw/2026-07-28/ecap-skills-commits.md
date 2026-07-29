# ecap-skills commits — 2026-07-28

## 7d63ca145ac595a915bb5dd2dea004306d1d4ee9
- 作者: sharplee-srp
- 日期: 2026-07-28T02:33:50Z
- PR: #243

### Commit message

```
fix(cron-job): harden route and payload updates (#243)

## What changed

- Canonicalize Feishu/Lark route identities before comparing declared
message sinks with `messageToolSentTo` run evidence.
- Preserve `chat_id`, `open_id`, and `user_id` distinctions, and make
already-canonical targets idempotent.
- Reuse the canonical route key for duplicate test-sink and live/test
overlap checks.
- Preserve existing `agentTurn` payload controls when changing
`agentMessage`, including tool allowlists, model selection, thinking
level, fallbacks, and timeout unless explicitly overridden.
- Force disposable jobs into an isolated session, remove inherited
session keys, and strip live routing context from completion-free tests.
- Require a request-only `delivery.testTo` sink for completion-only
`announce` tests; strip it from the final job and substitute it only
into the disposable copy.
- Keep every other channel on exact target comparison and bump
`cron-job` to version 2.3.

## Root causes

OpenClaw accepts a Feishu target such as `user:ou_xxx`, but cron run
history records the successfully sent target as the provider-normalized
bare Open ID `ou_xxx`. The driver compared those strings literally and
returned `needs_agent` even though the channel, account, target type,
and ID matched.

When updating an existing job's `agentMessage`, the driver rebuilt the
whole payload from three fields. That discarded existing safety and
runtime controls such as `toolsAllow`, model, thinking level, fallbacks,
and the previous timeout.

Disposable copies also inherited concrete live `sessionTarget` /
`sessionKey` values. Completion-only `announce` jobs had no separate
test recipient, so a forced validation run could reuse a real
conversation or notify the live destination.

## User impact

Valid Feishu cron message tests can now reach `validated` when OpenClaw
records a canonical bare target. A different recipient, account,
channel, or Feishu target kind still fails closed.

Prompt-only updates no longer silently broaden tool access or change
unrelated model/runtime behavior.

Validation runs now use a fresh isolated session and an explicit sink
while final jobs preserve their authorized live session and recipient.

## Validation

- `python3 -m py_compile cron-job/scripts/cron_workflow.py`
- `python3 cron-job/scripts/cron_workflow.py --self-test` — 126
assertions passed
- `uv run --with pyyaml python .github/scripts/lint_skills.py` — all
skills passed; 15 pre-existing unrelated warnings
- `uv run --with pyyaml python
~/.codex/skills/.system/skill-creator/scripts/quick_validate.py
cron-job`
- Anonymous production-shaped regression with a 57-tool allowlist —
payload controls remained unchanged while only the message changed
- Legacy payload regression — an existing `agentTurn` without
`timeoutSeconds` restores the established 300-second default; an
explicit replacement timeout still wins
- Anonymous production-shaped live-session regression — final job
preserved the authorized session/recipient; disposable copy removed the
session key, forced `isolated`, and used only `testTo`
- Local workflow fixture using the prior staging run-record shape:
- `origin/main`: valid `user:ou_xxx` versus bare `ou_xxx` returned
`needs_agent`
  - this branch: the same evidence returned `validated`
  - a different bare Open ID still returned `needs_agent`

The production inspection and local regression fixtures performed no bot
or scheduler mutation.
```

### PR body

## What changed

- Canonicalize Feishu/Lark route identities before comparing declared message sinks with `messageToolSentTo` run evidence.
- Preserve `chat_id`, `open_id`, and `user_id` distinctions, and make already-canonical targets idempotent.
- Reuse the canonical route key for duplicate test-sink and live/test overlap checks.
- Preserve existing `agentTurn` payload controls when changing `agentMessage`, including tool allowlists, model selection, thinking level, fallbacks, and timeout unless explicitly overridden.
- Force disposable jobs into an isolated session, remove inherited session keys, and strip live routing context from completion-free tests.
- Require a request-only `delivery.testTo` sink for completion-only `announce` tests; strip it from the final job and substitute it only into the disposable copy.
- Keep every other channel on exact target comparison and bump `cron-job` to version 2.3.

## Root causes

OpenClaw accepts a Feishu target such as `user:ou_xxx`, but cron run history records the successfully sent target as the provider-normalized bare Open ID `ou_xxx`. The driver compared those strings literally and returned `needs_agent` even though the channel, account, target type, and ID matched.

When updating an existing job's `agentMessage`, the driver rebuilt the whole payload from three fields. That discarded existing safety and runtime controls such as `toolsAllow`, model, thinking level, fallbacks, and the previous timeout.

Disposable copies also inherited concrete live `sessionTarget` / `sessionKey` values. Completion-only `announce` jobs had no separate test recipient, so a forced validation run could reuse a real conversation or notify the live destination.

## User impact

Valid Feishu cron message tests can now reach `validated` when OpenClaw records a canonical bare target. A different recipient, account, channel, or Feishu target kind still fails closed.

Prompt-only updates no longer silently broaden tool access or change unrelated model/runtime behavior.

Validation runs now use a fresh isolated session and an explicit sink while final jobs preserve their authorized live session and recipient.

## Validation

- `python3 -m py_compile cron-job/scripts/cron_workflow.py`
- `python3 cron-job/scripts/cron_workflow.py --self-test` — 126 assertions passed
- `uv run --with pyyaml python .github/scripts/lint_skills.py` — all skills passed; 15 pre-existing unrelated warnings
- `uv run --with pyyaml python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py cron-job`
- Anonymous production-shaped regression with a 57-tool allowlist — payload controls remained unchanged while only the message changed
- Legacy payload regression — an existing `agentTurn` without `timeoutSeconds` restores the established 300-second default; an explicit replacement timeout still wins
- Anonymous production-shaped live-session regression — final job preserved the authorized session/recipient; disposable copy removed the session key, forced `isolated`, and used only `testTo`
- Local workflow fixture using the prior staging run-record shape:
  - `origin/main`: valid `user:ou_xxx` versus bare `ou_xxx` returned `needs_agent`
  - this branch: the same evidence returned `validated`
  - a different bare Open ID still returned `needs_agent`

The production inspection and local regression fixtures performed no bot or scheduler mutation.



---
