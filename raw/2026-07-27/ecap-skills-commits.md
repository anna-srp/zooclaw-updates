# SerendipityOneInc/ecap-skills commits — 2026-07-27


## 1bc7a28336  (PR #242)

- **SHA**: `1bc7a28336ba4a3e77eb0fb581817a1b8a8d66d9`
- **作者**: sharplee-srp (sharplee-srp)
- **日期**: 2026-07-27T12:59:58Z
- **PR**: #242 — refactor(cron-job): use the built-in cron workflow

### Commit message

```
refactor(cron-job): use the built-in cron workflow (#242)

## What changed

- Route scheduler reads and writes through OpenClaw's built-in `cron`
tool.
- Generate only `agentTurn` jobs from the skill workflow.
- Keep deterministic preparation, test evidence, and final verification
in the local driver.
- Bind disposable test evidence to job and run identities, isolate test
alerts, and verify updates against a fresh scheduler snapshot.

## Why

Keep cron orchestration on the runtime's supported agent-facing path
while reducing the skill's operational surface area.

## Validation

- `python3 cron-job/scripts/cron_workflow.py --self-test` — 93
assertions passed
- `python3 -m py_compile cron-job/scripts/cron_workflow.py`
- `uv run --with pyyaml python .github/scripts/lint_skills.py`
- `git diff --check`
- Fresh stagingbot + A102 devcontainer E2E
(`cron-pr242-staging-e2e-20260727T122717Z`) — PASS across environment
validity, workflow completion, 93/93 runtime QA, and business acceptance
```

### PR body

## What changed

- Route scheduler reads and writes through OpenClaw's built-in `cron` tool.
- Generate only `agentTurn` jobs from the skill workflow.
- Keep deterministic preparation, test evidence, and final verification in the local driver.
- Bind disposable test evidence to job and run identities, isolate test alerts, and verify updates against a fresh scheduler snapshot.

## Why

Keep cron orchestration on the runtime's supported agent-facing path while reducing the skill's operational surface area.

## Validation

- `python3 cron-job/scripts/cron_workflow.py --self-test` — 93 assertions passed
- `python3 -m py_compile cron-job/scripts/cron_workflow.py`
- `uv run --with pyyaml python .github/scripts/lint_skills.py`
- `git diff --check`
- Fresh stagingbot + A102 devcontainer E2E (`cron-pr242-staging-e2e-20260727T122717Z`) — PASS across environment validity, workflow completion, 93/93 runtime QA, and business acceptance


---

## 17865b0107  (PR #241)

- **SHA**: `17865b0107ad673d9cafc39a704503b98551daf0`
- **作者**: sharplee-srp (sharplee-srp)
- **日期**: 2026-07-27T06:49:41Z
- **PR**: #241 — fix(cron-job): validate outbound message routing

### Commit message

```
fix(cron-job): validate outbound message routing (#241)

## Stacked PR

- Base: #240 (`feat/cron-job-skill`)
- This PR intentionally contains only the outbound-routing follow-up.
- Merge #240 before this PR.

## Why

An isolated Cron agent can have an explicit delivery context even when
`delivery.mode` is
`none`. That context becomes the current channel/account for the
`message` tool. Without an
explicit design-time decision, a task can therefore be bound to one
provider while attempting to
send through another and be rejected by OpenClaw's cross-context policy.

## What changed

- Add a structured `messageRouting` contract for execution context,
business recipients, test
  sinks, completion delivery, and cross-provider consent.
- Require user confirmation of every recipient route before scheduler
mutation.
- Render complete `messageRoute` placeholders into separate live and
test Agent payloads.
- Pin `delivery.mode:none` jobs to the declared execution context.
- Replace every recipient and execution target with synthetic sinks for
the disposable run and
  disable its production failure alert.
- Verify the run-log `messageToolSentTo` multiset exactly matches the
declared test routes before
  applying the live job.
- Reject hidden literal recipients, unknown/repeated placeholders,
incompatible webhook or
  announce contexts, and unapproved cross-provider routing.
- Document when multiple recipients can share a Cron and when
provider-aligned jobs should be
  split.

All documentation examples and regression fixtures are synthetic. No
production prompt,
recipient, account name, bot ID, or user message is included.

## Validation

- `python3 cron-job/scripts/cron_workflow.py --self-test` (43
assertions)
- `node cron-job/scripts/cron_gateway.mjs --self-test` (4 assertions)
- Python compile and Node syntax checks
- `git diff --check`
- `uv run --with pyyaml python3 .github/scripts/lint_skills.py` (passes;
15 pre-existing
  repository warnings)
```

### PR body

## Stacked PR

- Base: #240 (`feat/cron-job-skill`)
- This PR intentionally contains only the outbound-routing follow-up.
- Merge #240 before this PR.

## Why

An isolated Cron agent can have an explicit delivery context even when `delivery.mode` is
`none`. That context becomes the current channel/account for the `message` tool. Without an
explicit design-time decision, a task can therefore be bound to one provider while attempting to
send through another and be rejected by OpenClaw's cross-context policy.

## What changed

- Add a structured `messageRouting` contract for execution context, business recipients, test
  sinks, completion delivery, and cross-provider consent.
- Require user confirmation of every recipient route before scheduler mutation.
- Render complete `messageRoute` placeholders into separate live and test Agent payloads.
- Pin `delivery.mode:none` jobs to the declared execution context.
- Replace every recipient and execution target with synthetic sinks for the disposable run and
  disable its production failure alert.
- Verify the run-log `messageToolSentTo` multiset exactly matches the declared test routes before
  applying the live job.
- Reject hidden literal recipients, unknown/repeated placeholders, incompatible webhook or
  announce contexts, and unapproved cross-provider routing.
- Document when multiple recipients can share a Cron and when provider-aligned jobs should be
  split.

All documentation examples and regression fixtures are synthetic. No production prompt,
recipient, account name, bot ID, or user message is included.

## Validation

- `python3 cron-job/scripts/cron_workflow.py --self-test` (43 assertions)
- `node cron-job/scripts/cron_gateway.mjs --self-test` (4 assertions)
- Python compile and Node syntax checks
- `git diff --check`
- `uv run --with pyyaml python3 .github/scripts/lint_skills.py` (passes; 15 pre-existing
  repository warnings)


---

## 1bacc22962  (PR #240)

- **SHA**: `1bacc229629b6c2d0f850070c49d31da840b3720`
- **作者**: sharplee-srp (sharplee-srp)
- **日期**: 2026-07-27T04:16:03Z
- **PR**: #240 — feat(cron-job): add cron-job skill with safe create/update workflow driver

### Commit message

```
feat(cron-job): add cron-job skill with safe create/update workflow driver (#240)

## What

New `cron-job` skill: a single deterministic driver that turns a small
agent-authored request into a reliably created or updated OpenClaw cron
job. Driven by the 2026-07-20 production cron audit (536 bots / 153
jobs): vague keepalive payloads, jobs failing silently for weeks with no
failure alert, and "success" runs whose declared outcome never
materialized.

This is the v2 architecture: earlier revisions of this branch shipped a
7-script pipeline with a large fixture corpus; it has been deliberately
collapsed into one workflow driver plus one thin gateway adapter (6
files, ~1.2k lines) so the agent surface is a single command.

## How it works

The agent copies `assets/cron-request.template.json`, fills in `task`
(goal, `command` or `agentMessage`, schedule, observable `outcomes`,
delivery, optional matching `controls`), and runs exactly one driver:

```bash
python3 {baseDir}/scripts/cron_workflow.py <request> --output <result>
```

`cron_workflow.py` owns the safety sequence:

1. **Diagnose** — validates the request and separates genuinely
user-owned gaps (goal, timezone, one-shot time, recipient, failure
owner) into a `needs_user` question list from agent-fixable issues
(`needs_agent`). No scheduler write happens on either.
2. **Controls** — for matching/classification commands, runs
independently authored positive and split-record negative fixtures
natively and requires exact expected output.
3. **Isolated test** — through `cron_gateway.mjs` (loopback-only Gateway
adapter, env-inherited `GATEWAY_TOKEN`, never in argv), adds a uniquely
named disabled copy, force-runs it once, waits for the terminal run
record, and always removes the copy (cleanup failures are reported
alongside the primary error, never masking it).
4. **Verify** — checks every declared outcome assertion (`equals` /
`contains` / `arrayValues` / `exists`) against the produced files, and
verifies delivery: announce via run history, webhook via a correlated
receipt read on the caller's declared same-origin receiver (with the
mandatory `ecap-skill/1.0` User-Agent).
5. **Apply** — only after all checks pass: `cron.add` for new jobs
(duplicate-name guarded) or `cron.update` for `existingJobId` (guarded
by `updatedAtMs` optimistic concurrency), then re-reads and
field-compares the live job.

Activation is one-way: `activateAfterValidation:true` enables after a
verified test; `false`/omitted creates new jobs disabled and **preserves
an existing job's enabled state** on update — an update can never
silently disable a live cron.

## Testing

- `python3 cron-job/scripts/cron_workflow.py --self-test` → 15
assertions (schedule diagnosis, outcome assertions, vague-goal gating,
enabled-state preservation).
- `node cron-job/scripts/cron_gateway.mjs --self-test` → arg parsing,
job canonicalization, runtime resolution (requires installed openclaw).
- `python3 .github/scripts/lint_skills.py` → pass, zero warnings for
this skill.
- CodeQL: clean (0 open alerts on this branch).

## Notes

- Not added to `PUBLISHED_SKILLS` — distribution is a separate decision.
- `requires`: `bins: [python3, node, openclaw]`, `env: [GATEWAY_TOKEN]`;
`.env.example` documents the platform-injected variables.
- `references/openclaw-cron-model.md` records the 2026.6.11 runtime
facts the driver depends on (disabled force-run, webhook delivery not
proven by run history, agent-facing cron tool limitations).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01RpfzyjiWr4oYrU8DddnmzH

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR body

## What

New `cron-job` skill: a single deterministic driver that turns a small agent-authored request into a reliably created or updated OpenClaw cron job. Driven by the 2026-07-20 production cron audit (536 bots / 153 jobs): vague keepalive payloads, jobs failing silently for weeks with no failure alert, and "success" runs whose declared outcome never materialized.

This is the v2 architecture: earlier revisions of this branch shipped a 7-script pipeline with a large fixture corpus; it has been deliberately collapsed into one workflow driver plus one thin gateway adapter (6 files, ~1.2k lines) so the agent surface is a single command.

## How it works

The agent copies `assets/cron-request.template.json`, fills in `task` (goal, `command` or `agentMessage`, schedule, observable `outcomes`, delivery, optional matching `controls`), and runs exactly one driver:

```bash
python3 {baseDir}/scripts/cron_workflow.py <request> --output <result>
```

`cron_workflow.py` owns the safety sequence:

1. **Diagnose** — validates the request and separates genuinely user-owned gaps (goal, timezone, one-shot time, recipient, failure owner) into a `needs_user` question list from agent-fixable issues (`needs_agent`). No scheduler write happens on either.
2. **Controls** — for matching/classification commands, runs independently authored positive and split-record negative fixtures natively and requires exact expected output.
3. **Isolated test** — through `cron_gateway.mjs` (loopback-only Gateway adapter, env-inherited `GATEWAY_TOKEN`, never in argv), adds a uniquely named disabled copy, force-runs it once, waits for the terminal run record, and always removes the copy (cleanup failures are reported alongside the primary error, never masking it).
4. **Verify** — checks every declared outcome assertion (`equals` / `contains` / `arrayValues` / `exists`) against the produced files, and verifies delivery: announce via run history, webhook via a correlated receipt read on the caller's declared same-origin receiver (with the mandatory `ecap-skill/1.0` User-Agent).
5. **Apply** — only after all checks pass: `cron.add` for new jobs (duplicate-name guarded) or `cron.update` for `existingJobId` (guarded by `updatedAtMs` optimistic concurrency), then re-reads and field-compares the live job.

Activation is one-way: `activateAfterValidation:true` enables after a verified test; `false`/omitted creates new jobs disabled and **preserves an existing job's enabled state** on update — an update can never silently disable a live cron.

## Testing

- `python3 cron-job/scripts/cron_workflow.py --self-test` → 15 assertions (schedule diagnosis, outcome assertions, vague-goal gating, enabled-state preservation).
- `node cron-job/scripts/cron_gateway.mjs --self-test` → arg parsing, job canonicalization, runtime resolution (requires installed openclaw).
- `python3 .github/scripts/lint_skills.py` → pass, zero warnings for this skill.
- CodeQL: clean (0 open alerts on this branch).

## Notes

- Not added to `PUBLISHED_SKILLS` — distribution is a separate decision.
- `requires`: `bins: [python3, node, openclaw]`, `env: [GATEWAY_TOKEN]`; `.env.example` documents the platform-injected variables.
- `references/openclaw-cron-model.md` records the 2026.6.11 runtime facts the driver depends on (disabled force-run, webhook delivery not proven by run history, agent-facing cron tool limitations).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01RpfzyjiWr4oYrU8DddnmzH


---
