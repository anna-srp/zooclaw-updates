---
title: "Council 新增 Deep Research 深度研究模式"
type: "新功能上线"
priority: "高"
date: "2026-07-31"
status: "待审核"
channels: ""
---

## 核心宣传点

Council 页面现在支持全新的「Deep Research 深度研究」模式：在 Council | Deep Research 标签间一键切换，深度研究全程在 Council 内以实时线程呈现，并可将结果一键升级为完整对话继续追问。让复杂课题的多方研判更连贯、更省心。

## 原始内容

**feat(council): add deep research mode to council run API (#3162)**

- SHA: `8ee10766d32478f971f5f8614dee7fa19e208658`
- PR: #3162
- 日期: 2026-07-31T02:45:28Z

```
feat(council): add deep research mode to council run API (#3162)

## Summary
- Backend half of **Deep Research mode** on the `/council` page (spec:
`docs/superpowers/specs/2026-07-30-deep-research-mode-design.md`, plan
Tasks 1–3 of `docs/superpowers/plans/2026-07-30-deep-research-mode.md`).
No new routes, no new collections, no state-machine changes — council
behavior is unchanged.
- **`mode` discriminator** (`CouncilMode = "council" | "deep_research"`)
on `CouncilRunCreateRequest`, `CouncilRun`, and `CouncilRunResponse`. It
defaults to `"council"` everywhere, so existing clients and
already-stored run documents keep working untouched.
- **User-chosen `depth`** on the create request, accepted only when
`mode == "deep_research"` (council's depth is pod-reported, so a
council-mode request carrying depth is rejected).
- **Deep-research runs are inert records.** `create_run` skips the
admission check for them and stores the run already terminal
(`state="done"`, `terminal_at=created_at`). There is nothing to poll:
the unmodified `deep-research` skill writes no `status.json`, so the
run's real progress and final report live in the agent's chat thread.
The record exists for history listing plus the run⇄folder link.
- **Run⇄folder link** reuses the existing `pod_status_run_id`, assigned
deterministically at creation as `deep-research-<run_id>` — no
mtime/name discovery and no pinning CAS, unlike council. The response
exposes a server-built `pod_folder` (`research/deep-research-<run_id>`)
because the frontend embeds it in the dispatch message; it stays `None`
for council runs.
- **`refresh`/`cancel` reject deep-research runs** with
`council.mode_unsupported`. Terminal-state absorption would already make
them no-ops, but the explicit guard keeps the error messages truthful.
- A future PR can render investigator dossiers from the stored folder
with zero discovery logic (it will still need a mode-aware root in
`pod_files`, which currently roots every read under `council-runs/`).

**Deploy ordering:** this PR must merge and deploy **before** the
frontend PR. `CouncilRunCreateRequest` has `extra="forbid"`, so a
frontend that already sends `mode` would 422 against the current
backend. The reverse order is safe because `mode` is defaulted.

## Test plan
- [x] New unit tests: create-request defaults /
depth-rejected-for-council / depth-accepted-for-deep-research, legacy
run document reads back as `"council"`, `to_response` projects
`pod_folder` for deep research only, deep-research run born terminal
with admission bypassed while an active council run exists, cancel +
refresh rejected with `council.mode_unsupported`.
- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright,
import-linter (8 contracts kept) all clean.
- [x] Full backend unit suite: **7165 passed**. (Two
`test_ci_lint_deptry.py` cases fail only when `deptry` is absent from
`PATH`; they pass with the claw-interface venv active and are unrelated
to this change.)
- [x] Updated pre-existing request-shape assertions in
`test_council_routes.py` / `test_council_schema.py` for the two new
fields.
```

**PR Body:**

## Summary
- Backend half of **Deep Research mode** on the `/council` page (spec: `docs/superpowers/specs/2026-07-30-deep-research-mode-design.md`, plan Tasks 1–3 of `docs/superpowers/plans/2026-07-30-deep-research-mode.md`). No new routes, no new collections, no state-machine changes — council behavior is unchanged.
- **`mode` discriminator** (`CouncilMode = "council" | "deep_research"`) on `CouncilRunCreateRequest`, `CouncilRun`, and `CouncilRunResponse`. It defaults to `"council"` everywhere, so existing clients and already-stored run documents keep working untouched.
- **User-chosen `depth`** on the create request, accepted only when `mode == "deep_research"` (council's depth is pod-reported, so a council-mode request carrying depth is rejected).
- **Deep-research runs are inert records.** `create_run` skips the admission check for them and stores the run already terminal (`state="done"`, `terminal_at=created_at`). There is nothing to poll: the unmodified `deep-research` skill writes no `status.json`, so the run's real progress and final report live in the agent's chat thread. The record exists for history listing plus the run⇄folder link.
- **Run⇄folder link** reuses the existing `pod_status_run_id`, assigned deterministically at creation as `deep-research-<run_id>` — no mtime/name discovery and no pinning CAS, unlike council. The response exposes a server-built `pod_folder` (`research/deep-research-<run_id>`) because the frontend embeds it in the dispatch message; it stays `None` for council runs.
- **`refresh`/`cancel` reject deep-research runs** with `council.mode_unsupported`. Terminal-state absorption would already make them no-ops, but the explicit guard keeps the error messages truthful.
- A future PR can render investigator dossiers from the stored folder with zero discovery logic (it will still need a mode-aware root in `pod_files`, which currently roots every read under `council-runs/`).

**Deploy ordering:** this PR must merge and deploy **before** the frontend PR. `CouncilRunCreateRequest` has `extra="forbid"`, so a frontend that already sends `mode` would 422 against the current backend. The reverse order is safe because `mode` is defaulted.

## Test plan
- [x] New unit tests: create-request defaults / depth-rejected-for-council / depth-accepted-for-deep-research, legacy run document reads back as `"council"`, `to_response` projects `pod_folder` for deep research only, deep-research run born terminal with admission bypassed while an active council run exists, cancel + refresh rejected with `council.mode_unsupported`.
- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright, import-linter (8 contracts kept) all clean.
- [x] Full backend unit suite: **7165 passed**. (Two `test_ci_lint_deptry.py` cases fail only when `deptry` is absent from `PATH`; they pass with the claw-interface venv active and are unrelated to this change.)
- [x] Updated pre-existing request-shape assertions in `test_council_routes.py` / `test_council_schema.py` for the two new fields.



---

**feat(council): add deep research mode to council page (#3163)**

- SHA: `c3d6bd2e7cf65e7861cffd9e5ddfd16d96b31ede`
- PR: #3163
- 日期: 2026-07-31T04:40:27Z

```
feat(council): add deep research mode to council page (#3163)

## Summary
- Frontend half of **Deep Research mode** on the `/council` page (spec:
`docs/superpowers/specs/2026-07-30-deep-research-mode-design.md`, plan
Tasks 5–9 of `docs/superpowers/plans/2026-07-30-deep-research-mode.md`).
- **Depends on #3162 — merge and deploy that first.**
`CouncilRunCreateRequest` has `extra="forbid"`, so this frontend's
`mode` key 422s against a backend that has not shipped yet.
- **Composer tabs** — `Council | Deep Research` at the top of the input
card. The per-mode copy and controls come from a `MODE_CONFIG` map
rather than inline branches, so the upcoming council-selections change
only fills its slot (its `TabsContent` panel is intentionally empty
today). The Council tab is byte-for-byte the current experience.
- **Depth selector** on the Deep Research tab (`Quick` / `Standard`
(default) / `Deep`) with investigator-count and duration hints. Depth is
the only knob — the skill picks the investigators itself.
- **Dispatch flow**: create the session conversation → record the run
(`mode: 'deep_research'`, `depth`) → post `/deep-research <depth>:
<topic>` plus the run-folder pin into the thread → navigate to that chat
thread. Chat is the whole experience: the skill's framework-confirmation
question, its progress narration, and the final cited report all arrive
as chat messages, which is why there is no gate/status/results UI and
nothing to poll.
- The dispatch text has a single source of truth in
`src/lib/council/deep-research-dispatch.ts`. The folder line uses the
server-built `pod_folder`, so a future release can read investigator
dossiers from a known path; if the agent ignores the pin, the research
still completes in chat and only the folder link degrades.
- **History rail** lists both modes. Deep-research entries are badged
and link to their chat thread, with the session resolved from
`dispatch_root_post_id` via the main agent's conversation list (nothing
extra persisted). When that session is not in the loaded list the entry
degrades to a non-link with an explanatory tooltip. Opening a
deep-research run's `/council/[runId]` URL directly shows
`DeepResearchRunNotice` instead of council lifecycle views.

Reviewer note: the "Depth" caption is a plain `<span>` +
`aria-labelledby` rather than a `FieldLabel`, because `htmlFor` on a
radio group binds the caption to a single option — clicking "Depth"
would have silently selected Standard.

## Test plan
- [x] New/updated unit tests: dispatch-message composition (with and
without a folder pin), mode-tab switching preserving the topic, depth
selection reflected in the dispatched text, full deep-research dispatch
sequence through to chat navigation, dispatch-post failure keeping the
user on the composer with an error, history-rail chat links plus the
missing-session fallback, and the run-page notice replacing council
views.
- [x] `bash scripts/verify-web.sh` — guards + `tsc` + vitest (**7518
passed**, 556 files) + eslint all clean.
- [x] `pnpm test:unit:coverage` — statements 88.46 / branches 81.62 /
functions 87.08 / lines 90.79, all above the ratcheted thresholds.
- [ ] Post-deploy: start a Deep Research run on staging once #3162 is
live and confirm the agent honors the depth and folder-pin instructions.
```

**PR Body:**

## Summary
- Frontend half of **Deep Research mode** on the `/council` page (spec: `docs/superpowers/specs/2026-07-30-deep-research-mode-design.md`, plan Tasks 5–9 of `docs/superpowers/plans/2026-07-30-deep-research-mode.md`).
- **Depends on #3162 — merge and deploy that first.** `CouncilRunCreateRequest` has `extra="forbid"`, so this frontend's `mode` key 422s against a backend that has not shipped yet.
- **Composer tabs** — `Council | Deep Research` at the top of the input card. The per-mode copy and controls come from a `MODE_CONFIG` map rather than inline branches, so the upcoming council-selections change only fills its slot (its `TabsContent` panel is intentionally empty today). The Council tab is byte-for-byte the current experience.
- **Depth selector** on the Deep Research tab (`Quick` / `Standard` (default) / `Deep`) with investigator-count and duration hints. Depth is the only knob — the skill picks the investigators itself.
- **Dispatch flow**: create the session conversation → record the run (`mode: 'deep_research'`, `depth`) → post `/deep-research <depth>: <topic>` plus the run-folder pin into the thread → navigate to that chat thread. Chat is the whole experience: the skill's framework-confirmation question, its progress narration, and the final cited report all arrive as chat messages, which is why there is no gate/status/results UI and nothing to poll.
- The dispatch text has a single source of truth in `src/lib/council/deep-research-dispatch.ts`. The folder line uses the server-built `pod_folder`, so a future release can read investigator dossiers from a known path; if the agent ignores the pin, the research still completes in chat and only the folder link degrades.
- **History rail** lists both modes. Deep-research entries are badged and link to their chat thread, with the session resolved from `dispatch_root_post_id` via the main agent's conversation list (nothing extra persisted). When that session is not in the loaded list the entry degrades to a non-link with an explanatory tooltip. Opening a deep-research run's `/council/[runId]` URL directly shows `DeepResearchRunNotice` instead of council lifecycle views.

Reviewer note: the "Depth" caption is a plain `<span>` + `aria-labelledby` rather than a `FieldLabel`, because `htmlFor` on a radio group binds the caption to a single option — clicking "Depth" would have silently selected Standard.

## Test plan
- [x] New/updated unit tests: dispatch-message composition (with and without a folder pin), mode-tab switching preserving the topic, depth selection reflected in the dispatched text, full deep-research dispatch sequence through to chat navigation, dispatch-post failure keeping the user on the composer with an error, history-rail chat links plus the missing-session fallback, and the run-page notice replacing council views.
- [x] `bash scripts/verify-web.sh` — guards + `tsc` + vitest (**7518 passed**, 556 files) + eslint all clean.
- [x] `pnpm test:unit:coverage` — statements 88.46 / branches 81.62 / functions 87.08 / lines 90.79, all above the ratcheted thresholds.
- [ ] Post-deploy: start a Deep Research run on staging once #3162 is live and confirm the agent honors the depth and folder-pin instructions.



---

**feat(council): keep deep research inside council (#3172)**

- SHA: `639005ad93351a357ccae97d2ec2f96a91722f61`
- PR: #3172
- 日期: 2026-07-31T09:31:12Z

```
feat(council): keep deep research inside council (#3172)

## Linear
<!-- none -->

## Summary
- Keep Deep Research runs inside Council and render their live
Mattermost thread transcript there instead of redirecting to Chat.
- Remove the Deep Research reply composer and the duplicate `New
council` action; Council remains read-only while research is running.
- Make `Open full chat` promote the existing Mattermost thread into an
owner-scoped Chat conversation, update the conversation cache, and
navigate to Chat so the user can continue.
- Reuse existing conversation mappings by `root_post_id` and make
registration idempotent across repeated clicks and duplicate-key races.
- Recover a recorded run whose initial Mattermost dispatch never landed
by retrying the same persisted thread/run with a deterministic
pending-post id.
- Distinguish permanent main-agent identity mismatches from retryable
chat-promotion failures, and hide promotion for historical runs without
a persisted workspace identity.

## Test plan
- [x] `bash scripts/verify-web.sh ...` — guards, TypeScript, 166
Council-related tests, and ESLint passed.
- [x] Backend Council/session-channel unit tests — 69 passed.
- [x] Ruff passed for changed backend files.
- [x] Python file-length guard passed after extracting existing-thread
registration (`581 → 490` lines).
- [x] Pyright passed for changed production files with the
claw-interface venv explicitly selected.
- [x] Import-linter — all 8 architecture contracts kept.
- [x] PR size check — 1812 / 3000 lines.
- [ ] CI re-running for `4437463eb`.

## Local environment note
- The repository-wide `verify-py.sh` invocation on this macOS checkout
does not automatically resolve packages from
`services/claw-interface/.venv` and reports global missing-import
errors. Targeted production-file Pyright with `--pythonpath
services/claw-interface/.venv/bin/python` passes; CI remains
authoritative for the complete backend type check.

## Deployment
- This changes both `services/claw-interface` and `web/app`. Deploy
`claw-interface` first, then `web/app`, so the new `POST
/council/runs/{id}/conversation` route exists before the `Open full
chat` CTA ships. Do not roll back the backend while the new web build is
live.
```

**PR Body:**

## Linear
<!-- none -->

## Summary
- Keep Deep Research runs inside Council and render their live Mattermost thread transcript there instead of redirecting to Chat.
- Remove the Deep Research reply composer and the duplicate `New council` action; Council remains read-only while research is running.
- Make `Open full chat` promote the existing Mattermost thread into an owner-scoped Chat conversation, update the conversation cache, and navigate to Chat so the user can continue.
- Reuse existing conversation mappings by `root_post_id` and make registration idempotent across repeated clicks and duplicate-key races.
- Recover a recorded run whose initial Mattermost dispatch never landed by retrying the same persisted thread/run with a deterministic pending-post id.
- Distinguish permanent main-agent identity mismatches from retryable chat-promotion failures, and hide promotion for historical runs without a persisted workspace identity.

## Test plan
- [x] `bash scripts/verify-web.sh ...` — guards, TypeScript, 166 Council-related tests, and ESLint passed.
- [x] Backend Council/session-channel unit tests — 69 passed.
- [x] Ruff passed for changed backend files.
- [x] Python file-length guard passed after extracting existing-thread registration (`581 → 490` lines).
- [x] Pyright passed for changed production files with the claw-interface venv explicitly selected.
- [x] Import-linter — all 8 architecture contracts kept.
- [x] PR size check — 1812 / 3000 lines.
- [ ] CI re-running for `4437463eb`.

## Local environment note
- The repository-wide `verify-py.sh` invocation on this macOS checkout does not automatically resolve packages from `services/claw-interface/.venv` and reports global missing-import errors. Targeted production-file Pyright with `--pythonpath services/claw-interface/.venv/bin/python` passes; CI remains authoritative for the complete backend type check.

## Deployment
- This changes both `services/claw-interface` and `web/app`. Deploy `claw-interface` first, then `web/app`, so the new `POST /council/runs/{id}/conversation` route exists before the `Open full chat` CTA ships. Do not roll back the backend while the new web build is live.



---

**feat(council): show the terminal thread synthesis (#3161)**

- SHA: `abd8542150515f5ff9e9076f2469541dcc1ed6a9`
- PR: #3161
- 日期: 2026-07-31T02:38:02Z

```
feat(council): show the terminal thread synthesis (#3161)

## Summary

- fetch and cache the dedicated Council run thread history
- render the latest eligible bot reply from the final `go` turn as the
terminal synthesis summary
- keep the shared Mattermost subscription active for the full bounded
15-second terminal window so final edits or later replies can replace a
draft
- route Mattermost-hosted file links through the authenticated shared
preview sidebar without exposing unauthenticated direct actions

## Stack

- Depends on #3160
- Review after #3157, #3158, and #3160
- This is the final slice replacing #3139

## Verification

- `bash scripts/verify-web.sh web/app/src/components/artifacts/types.ts
web/app/src/components/council
web/app/src/components/MarkdownContent.tsx
web/app/src/components/markdown/render-markdown-to-html.ts
web/app/src/hooks/council web/app/src/hooks/queries/council
web/app/src/lib/council web/app/src/models/artifact-preview.ts
web/app/tests/unit/app/council
web/app/tests/unit/components/MarkdownContent.unit.spec.tsx
web/app/tests/unit/components/markdown/render-markdown-to-html.unit.spec.ts
web/app/tests/unit/hooks/council
web/app/tests/unit/hooks/queries/council web/app/tests/unit/lib/council`
- TypeScript passed
- 306 selected tests passed
- ESLint passed
```

**PR Body:**

## Summary

- fetch and cache the dedicated Council run thread history
- render the latest eligible bot reply from the final `go` turn as the terminal synthesis summary
- keep the shared Mattermost subscription active for the full bounded 15-second terminal window so final edits or later replies can replace a draft
- route Mattermost-hosted file links through the authenticated shared preview sidebar without exposing unauthenticated direct actions

## Stack

- Depends on #3160
- Review after #3157, #3158, and #3160
- This is the final slice replacing #3139

## Verification

- `bash scripts/verify-web.sh web/app/src/components/artifacts/types.ts web/app/src/components/council web/app/src/components/MarkdownContent.tsx web/app/src/components/markdown/render-markdown-to-html.ts web/app/src/hooks/council web/app/src/hooks/queries/council web/app/src/lib/council web/app/src/models/artifact-preview.ts web/app/tests/unit/app/council web/app/tests/unit/components/MarkdownContent.unit.spec.tsx web/app/tests/unit/components/markdown/render-markdown-to-html.unit.spec.ts web/app/tests/unit/hooks/council web/app/tests/unit/hooks/queries/council web/app/tests/unit/lib/council`
- TypeScript passed
- 306 selected tests passed
- ESLint passed

