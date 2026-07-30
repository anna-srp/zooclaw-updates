# SerendipityOneInc/ecap-workspace commits — 2026-07-29

## feat(council): build the Council surface on the runs API (#3132)

- sha: a85f7f5505665c876add7e2befaf49fc312981d3
- author: bill-srp
- date: 2026-07-29T16:54:14Z
- PR: #3132

### Commit message



### PR body

Linear: https://linear.app/srpone/issue/ECA-1211/council-多模型调研功能上线-beta-版

## Summary

Builds the Council surface in `web/app`: the prototype becomes a real feature backed by the runs API, dispatch moves into a proper agent session thread, and the page adopts the design system.

Frontend and docs only — **zero files under `services/`**. The backend half landed separately in #3120 (dispatch thread persistence), #3113 / #3115 / #3123 (pod file reads), and #3129 (folder discovery), so this deploys after them with no ordering to coordinate.

24 commits, grouped by what they do:

**Wired to the real API**
- `feat(council): replace the mocked prototype with the real runs API` — the page now creates, lists, refreshes and cancels real runs
- `fix(council): scope refresh failures per run and guard IME submits` — a failed refresh no longer poisons unrelated runs; CJK/IME composition no longer submits mid-word

**Dispatch correctness** — the substantive fix
- `fix(council): dispatch to the main agent thread, not whichever is active`
- `fix(council): dispatch into a session thread, not the DM channel root`
- `refactor(council): derive the session channel instead of storing it`
- `fix(council): never gate cancel on the agent thread`

**Design system**
- `refactor(council): align page with design system`
- `refactor(council): give run status one owner and a tone`
- `refactor(council): replace council.css with Tailwind utilities`
- `fix(council): restore ellipsis on truncated history titles`

**Docs** — the interactive prototype specs, plus `docs/council-skill-contract.md` (new, see below)

## Root cause

Two defects worth calling out, both about *where* Council was talking.

**Council posted into the wrong channel, at the wrong level.** `/council {topic}`, `go` and `cancel` went out as root-level posts in the main agent's `dm_channel_id`. Every other agent conversation in the product is a threaded reply in the agent's `session_channel_id` under a session's `root_post_id` — two different channels on `AgentMattermostPublic`, and the frontend type never declared the second one, so it arrived and was dropped.

The consequences: the exchange had no session record, so it never appeared in the session list and the results view promised a thread the user could not open; `go` and `cancel` landed as bare words in the user's ordinary main-agent chat with nothing scoping them to the run; and because the thread lived only in client state, approval was reachable only from the tab that started the run. Council now mirrors `new-chat` — create a session, require its root post, reply into that thread — and the run carries the root post, so `go` and `cancel` survive a reload and work from another device.

**Cancel was gated on that same thread, which deadlocked the feature.** Go genuinely needs the thread: the skill proceeds only after reading consent there, so approving locally would be a lie. Cancel needs nothing — the backend records it as a state transition and reads no dispatch data at all. Sharing one guard meant a run with no `dispatch_root_post_id` was unapprovable (correct), uncancellable (wrong), *and* admission-blocking, since `create_run` rejects a second run while one is active. Council became permanently unusable for that account with no way out through the UI.

The backend had already anticipated this — `cancelling` is deliberately excluded from `ADMISSION_BLOCKING_STATES` so a cancelled run cannot gate its replacement. The backend built the escape hatch; the frontend padlocked it. The rule now encoded: cancel must never depend on anything but the run's own state.

## `docs/council-skill-contract.md`

New, and aimed outside this repo — at whoever maintains the Council skill in `ecap-skills`.

Every Council outage so far has been a contract mismatch with the skill rather than a bug in either side's own logic: we read the wrong workspace path, called a list endpoint expecting file contents, required the topic to come back verbatim, and typed `eta_minutes` as an integer against a JSON number. All cheap to fix, all expensive to find, because the contract existed only as our inference about the skill's output.

The doc writes it down — the two one-way channels, the `status.json` field contract including the stricter `awaiting_go` gate, the stage mapping, artifact path rules, read cadence — and asks for three things: a way to pass our run id in (which would make folder binding exact instead of inferred), confirmation that `status.json` writes are atomic (we read without taking the lock file beside it), and confirmation that `estimate.unpriced` and `premium_alt_*` are stable so we can surface them.

## Test plan

- [x] `bash scripts/verify-web.sh` green — guards, tsc, eslint, and 7434 vitest tests across 553 files
- [x] Rebased onto current `origin/main`; the superseded backend commit was dropped, since #3120 landed a newer collapsed form of the same change
- [x] Council unit tests cover: a session is created before the run; the topic posts under the session root rather than at channel root; `go` / `cancel` reply into the run's stored thread rather than any active channel; `go` is disabled without a dispatch; **cancel is enabled without one** and warns that the skill may keep running on the pod
- [ ] Staging: one real run driven end to end — topic → gate → `go` → `done` — including member reports. This has never been exercised against a live pod, because the frontend has not shipped until now.
- [ ] Staging: confirm the history rail, gate and results render correctly at 320 / 768 / 1440

## Notes for review

The wide test-fixture diff comes from `session_channel_id` becoming a declared field on `OpenClawAgentMattermost`. The backend has always sent it; the type simply never declared it, so it was silently dropped. Making it required touches every fixture that builds an agent.

`MattermostProvider` is gone from Council. It was mounted only to reach `sendMessage`, which posts to whatever channel is active — the source of the dispatch defect. Council now builds a standalone `MattermostAPIService` and posts to an explicit `(channel, root)` pair, so the active-channel concept and its race leave Council entirely.


---

## feat(channels): reuse the v1 guided Slack setup for engine agents (#3131)

- sha: b50c82ebb849a5e5075fbe267b509ffd813780f2
- author: bill-srp
- date: 2026-07-29T14:37:49Z
- PR: #3131

### Commit message



### PR body

## Linear
<!-- none — surfaced from a code review of the channels page, no ticket -->

## Summary

Engine (v2) channel targets were gated out of the guided setup render path. Picking Slack for an engine workspace dropped the user straight onto two unlabeled `xoxb-…` / `xapp-…` boxes, while the same platform on a v1 bot target got the full manifest wizard with step-by-step instructions and a deep link to the Slack app console.

Two expressions in `useAddChannelForm.ts` did the gating:

```ts
const effectiveShowAdvanced = showAdvanced || isEngineTarget          // forced manual mode
guidedCapable: !isEngineTarget && flags.guidedCapable                 // killed the method cards
```

`SlackSetupWizard` is pure UI over an `onAdd` callback — no `uid`, no backend session, no v1-only endpoint — so it needed target threading rather than a rewrite.

- **`ENGINE_GUIDED_PLATFORMS`** allowlists which engine platforms get the guided method cards. **Feishu and WeCom deliberately stay on manual entry**: their guided flow is a backend QR session that resolves the target via `get_user_bot_and_token(uid)` and writes with `client.add_channel(bot_id, …)` (`openclaw_settings/feishu.py:276`, `wecom.py:194`). There is no workspace parameter anywhere in that path, so offering it for an engine target would provision the channel onto the user's **bot** instead of the selected workspace. A test pins this.
- Threads the selected target through `onSlackSetup` → `ChannelsSection` → `SlackSetupWizard`, so wizard completion routes to `onEngineAdd`.
- Omits `agent_id` for engine targets — engine channels have no per-channel agent binding.
- Excludes `pairing` from the engine DM-policy list; the backend rejects it with `channel.pairing_unsupported` (`engine_agent_channels_service.py:166`).
- Derives the account-id and Slack app-name defaults from the selected workspace's channels rather than the bot's.

### Relationship to the design of record

`docs/superpowers/specs/2026-07-20-engine-agent-channels-design.md` lists as a v1 non-goal:

> No QR/guided auto-provision wizard for engine Slack/Feishu/WeCom in v1 (manual entry only; the auto-provision convenience can follow later).

This is that follow-up, **for Slack only** — the one platform whose wizard is runtime-agnostic today. Feishu and WeCom remain deferred, and this PR keeps them explicitly excluded rather than leaving it to drift.

### Scope

Frontend only (`web/app`). No backend change, no schema change, no new endpoint — the engine `POST /agents/{workspace_id}/channels` path this routes to already exists and is already used by the manual form. No deploy ordering constraint; `pnpm-lock.yaml` untouched.

## Test plan

- [x] TDD. Six new assertions in `tests/unit/app/claw-settings/ChannelsSection-engine.unit.spec.tsx`:
  - guided **and** manual method cards render for an engine Slack target
  - the wizard opens with the engine workspace as its `target`
  - completion calls `onEngineAdd` with the `workspaceId`, sends **no** `agent_id`, and does **not** call `onAdd`
  - engine **Feishu and WeCom** still render no method cards (guards the deliberate exclusion)
  - the real wizard — not a stub — excludes `pairing` from its DM-policy options
  - account-id and app-name defaults derive from the selected workspace's channels (`slack` → `slack-2`, app name suffixed off the workspace name)
- [x] One pre-existing assertion in `useAddChannelForm.unit.spec.tsx` flipped from `guidedCapable: false` / `showAdvanced: true` to `true` / `false`. That test encoded the old gate; the flip is an honest re-encoding of the intended behavior change, not removed coverage. No v1/bot expectation was altered.
- [x] `bash scripts/verify-web.sh` — **PASS** (exit 0): 7 governance guards, `tsc`, vitest **550 files / 7404 passed / 1 skipped / 1 todo**, eslint.
- [ ] Not exercised against a live Slack workspace. The meaningful post-deploy check is connecting Slack to an **engine** agent through the step-by-step path and confirming a message round-trip.

## Note for reviewers

`handleAddChannel` falls back to the bot path when `onEngineAdd` is undefined, so a missing prop would send an engine channel to the bot. This is **pre-existing and not live** — `ChannelsPageClient` always passes it — and is unchanged here. Flagged for awareness since the wizard can now reach that function; worth a follow-up guard rather than a fix in this PR.


---

## fix(council): stop matching the run folder on topic (#3129)

- sha: ae658a54981bf935ec5b39a47154bf0cee2c8833
- author: bill-srp
- date: 2026-07-29T14:37:15Z
- PR: #3129

### Commit message



### PR body

## Summary

- Council runs never left `dispatching`. Folder discovery required `status.json`'s `topic` to equal the run's topic; the skill rewrites the topic, so the correct folder was rejected on every refresh, forever.
- Removes that comparison from both places it appears — discovery and the pinned read — and logs every discovery outcome, which the old code did not.
- Widens `CouncilEstimate.eta_minutes` from `int` to `float`, a second 502 waiting in the same path.

Backend only. No frontend change, no deploy ordering.

## Root cause

Discovery matched the pod's run folder to the ECAP run by comparing topics. Observed on staging run `8d1c262916854879ba4178d302b3c6be`:

| | |
|---|---|
| `run.topic` | `研究一下 2026 年世界杯的经济收益` |
| `status.json` | `2026年世界杯的经济收益` |

The skill dropped the instruction prefix and the spaces around the numerals, and named the folder `worldcup2026-econ-1785306491` — an English slug it invented. The topic is free text the skill normalizes, so exact equality can never bind a folder to a run, and no normalization recovers a dropped word.

The failure was invisible. Topic mismatch was a bare `continue` with no log, sitting directly beside an identity mismatch that does log — so "candidate rejected" and "the skill hasn't started yet" looked identical in production. That run had been sitting at `awaiting_go` with a full cast priced and waiting for approval the whole time.

### Why removing it is safe

The topic was never the guard that made discovery safe — it was standing in for a run id we do not have. What actually discriminates is unchanged:

- `create_run` already rejects a second run while one is active (`council.active_run_exists`), so the UI cannot produce two unbound folders.
- Folders pinned by the user's other runs are already excluded.
- `mtime >= run.created_at` bounds the window.
- Folder name must equal the snapshot's own `run_id`.
- Two surviving candidates are refused, not guessed.

The residual is that `/council` typed directly in the agent thread produces an unbound folder a UI run could bind to. That surfaces as two candidates and is refused — a stuck record inside one user's own pod, not a wrong binding. Accepted, and recorded in the spec.

### The pinned read had the same check

`_read_pinned_snapshot` re-compared topics on every refresh and raised `council.status_malformed` → 502. Left in place, runs would have pinned and then hard-failed on the very next poll, so the fix would have looked like it moved the bug rather than fixed it. Both go together.

### `eta_minutes`

```
eta_minutes=  12.0 -> OK, stored as 12
eta_minutes=  12.5 -> ValidationError: got a number with a fractional part
```

The pod writes a JSON number; staging carries `12.0`. Pydantic coerces it only because the fractional part is zero. The skill derives the ETA from depth and cast size, so a fraction is ordinary output — the schema was narrower than the producer's contract. Every existing fixture happens to use a whole number, which is why the suite stayed green over a type that cannot hold what it receives.

Found by validating the real staging payload against the models field by field. That same comparison confirmed everything else matches: all four members, the synthesizer, both cost bounds, the timestamp, and a complete `awaiting_go` gate.

## Test plan

- [x] `bash scripts/verify-py.sh` green — ruff, ruff-format, pyright, import-linter 8/8
- [x] 210 council unit tests pass (`pytest -q tests/unit -k council`)
- [x] Real staging `status.json` validated against `_StatusSnapshot` field by field: parses, gate complete, `awaiting_go` to `awaiting_confirmation` is a legal transition from `dispatching`
- [x] New tests cover: a topic-mismatched candidate is now discovered and pinned (using the real staging strings); a pinned run with a mismatched topic refreshes instead of raising; the identity check still rejects a folder whose `run_id` differs from its name; two unbound candidates are still refused; an already-pinned folder is still excluded; fractional ETAs validate
- [ ] After deploy: confirm run `8d1c262916854879ba4178d302b3c6be` picks up its folder on the next refresh and advances to `awaiting_confirmation` — the folder is still on the pod at `awaiting_go`

## Notes for review

Two things the field-by-field comparison surfaced that are **not** fixed here, because they are product decisions rather than bugs:

- `estimate.unpriced` is dropped. It is the skill reporting which models it could not price — if non-empty, the cost range shown at the approval gate is incomplete and we do not say so.
- `estimate.premium_alt_low_credits` / `premium_alt_high_credits` are dropped. The skill is offering a premium-tier comparison (1123.8-5855.2 credits against the standard 560.4-2921.6) that the gate never surfaces.

Both are `extra="ignore"` today. The gate is where a user decides whether to spend, so surfacing them seems worth a follow-up.


---

## fix(council): read pod files through runtime exec (#3123)

- sha: 24f779befb7904431ee60a9b2f6e0a4777038ff2
- author: bill-srp
- date: 2026-07-29T13:38:28Z
- PR: #3123

### Commit message



### PR body

## Summary

Every Council refresh currently **502s on staging** with `council.pod_file_malformed`, `field_paths: ['content']`. Refresh is the only thing that advances a run, so no council can leave its initial state.

Captured on `claw-interface-deployment-7bc55b4789-vv9vm` (staging, `ecap` ns):

```
[OPENCLAW] List files  path=/workspace/main/council-runs
[OPENCLAW] Read file   path=/workspace/main/council-runs/worldcup2026-econ-1785306491/status.json
[COUNCIL_POD_FILES] malformed response code=council.pod_file_malformed fields=['content']
ServiceError: council.pod_file_malformed  →  502
```

Note the listing succeeded and the skill's run folder exists — the skill fires correctly. Only the file **read** is broken.

## Root cause

`read_bot_file` and `list_bot_files` call the **same fastclaw endpoint**:

```
read_bot_file  → GET /bot/api/v1/bots/{id}/files?path={path}
list_bot_files → GET /bot/api/v1/bots/{id}/files?path={path}&showHidden=
```

In fastclaw that route is `ListFiles` and nothing else (`cmd/server.go:196`). The entire bot API has exactly two file routes — `POST /files` (write) and `GET /files` (list). **There is no content-read endpoint.** Its own fs-browser design doc scoped it out under Non-Goals v1 — 文件内容读取（另做 API） — and that separate API was never built.

So `read_bot_file` has always pointed at a directory lister. `ls -la` against a file path *succeeds* and returns that file's metadata entry, so we get a plausible `200 / code:0` carrying `size`, `mode`, `mtime` and no `content`, and only discover the mismatch at parse time. It does not trip `ErrNotADirectory`, which is why it surfaces as a malformed response rather than a clean 4xx.

## The fix

Reads now go through `POST /bot/api/v1/bots/{id}/runtime/exec`:

```json
{"args": ["head", "-c", "<max_bytes+1>", "<path>"]}
```

- **`args` array, not `command`** — fastclaw runs the `command` string through `strings.Fields()`, which would mangle any path containing a space. `args` is exec'd with no shell, so it is also injection-safe. `_workspace_path` still bounds the path first.
- **`head -c` rather than `cat`** — bounds the read at the source instead of after the whole file is already in the response.

`list_bot_files` and `_parse_listing_data` are **untouched**: `GET /files` genuinely is the listing API and is correct as written.

### Response handling

`RuntimeExec` `json.Unmarshal`s stdout and, on success, returns the parsed document as the *entire* payload. So `status.json` arrives unwrapped, while a Markdown member report lands in the fallback shape under `raw`. Both are handled. `exitCode` is omitted when zero, so its **presence** is the signal, not its value.

### The invariant most at risk

A missing file used to be a 404. Under exec it is a **200** carrying `exitCode: 1` and `No such file or directory` on stderr. `PodFiles.read` must keep returning `None` there, because run-folder discovery depends on it — a run whose folder the skill has not written yet has to refresh quietly. Losing it would 502 every pre-skill run: the same bug with a new cause. It is matched against the existing missing-markers and covered by a test using `head`'s literal stderr.

## Known limitations

Documented in the spec rather than left implicit:

- A JSON file with a top-level `raw` or `exitCode` key is ambiguous — those keys mean "exec envelope" to the reader and "file content" to the writer. `status.json` uses neither and the skill owns that schema, so it is unreachable today. It is not fixable client-side.
- The size guard measures re-serialized JSON, so it slightly under-measures on-disk bytes. It still holds where it matters: `head -c max_bytes+1` truncates at the source, truncated JSON stops parsing, so it arrives as `raw` measured at `max_bytes + 1` — over the cap, as intended.
- This routes reads through arbitrary-command execution because the purpose-built API was deferred. When fastclaw ships the content-read endpoint its own Non-Goals promised, `read_bot_file` should move back onto it and this path should be deleted.

Full design: `docs/superpowers/specs/2026-07-29-council-pod-file-read-via-exec.md`.

## Test plan

- [x] JSON stdout (`status.json`) returns the document
- [x] Non-JSON stdout returns `raw` (member report)
- [x] Missing file → `None`, asserted with `head`'s literal stderr and `exitCode: 1`
- [x] Non-missing exec failure → `council.pod_unavailable` (503), still distinct from a malformed payload
- [x] Oversized file → `council.pod_file_too_large`, including the exactly-one-byte-over boundary
- [x] `list_bot_files` behaviour unchanged
- [x] 371 council + openclaw-client unit tests pass
- [x] `bash scripts/verify-py.sh` green — ruff, ruff-format, pyright, import-linter (8/8 contracts)
- [ ] Staging: a council run advances past `dispatching` on refresh. That is the end-to-end proof and is currently blocked entirely by this defect.


---

## fix(agent-builder): hide v2 home connection status (#3124)

- sha: da455efbeca86ceefe9fe402374db5de47540b6d
- author: kaka-srp
- date: 2026-07-29T13:00:15Z
- PR: #3124

### Commit message



### PR body

## Summary

- hide the Claw connection status on the Agent Builder v2 home page
- preserve the existing connection status on the v1 home page
- add runtime-specific regression coverage

## Testing

- `pnpm exec vitest run tests/unit/app/agent-builder-entry.unit.spec.tsx tests/unit/app/agent-builder-client.unit.spec.tsx`
- `bash scripts/verify-web.sh web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderEntryClient.tsx web/app/tests/unit/app/agent-builder-entry.unit.spec.tsx`


---

## fix(skills): open the registry to all SRP staff (#3122)

- sha: 4a160808f1b348f42bfd0fb06e7ee3d060bbddf0
- author: bill-srp
- date: 2026-07-29T12:46:25Z
- PR: #3122

### Commit message



### PR body

## Summary

The Skills registry only needs SRP staff, not the admin allowlist. Follow-up to #3119.

- **Backend**: drop the `require_admin_user` dependency from the `/internal/skills` sub-router.
- **Frontend**: drop the `AdminOnly` wrapper from the skills route, and with it the `adminOnly` `NavItem` flag that #3119 added for the nav move.

## Root cause

Not a bug — a permission scope that was tighter than intended.

`/internal/skills` was gated twice: the parent `/internal` router already applies `require_srp_account` to every sub-route, and the skills sub-router added `require_admin_user` on top. Only the second gate is being removed, so **the routes stay SRP-staff-only** — they do not become public.

This is safe because both endpoints are reads over *global* registry skills: no per-account data, no mutations, and the console page is read-only. It also lines the routes up with existing precedent — `stripe_resources` and `vertical_pack_plans` already run SRP-only under the same parent router. A comment on the router records that adding a write here means adding the admin gate back.

On the frontend, `AuthGate` already restricts the whole console to `@srp.one` (mirroring `require_srp_account`), so removing `AdminOnly` leaves the page gated by that, plus the backend.

## Test plan

- [x] TDD, both directions, RED confirmed before the change:
  - `require_admin_user` is absent from the route dependency chain
  - `require_admin_user` is deliberately **not** overridden in the test client, so if it were ever re-added the real dependency would run and fail the request — the RED run returned `401`, confirming the test actually detects the gate
  - a non-admin `@srp.one` staffer gets `200` and real registry data instead of a permission wall
- [x] Frontend tests flipped to the new contract: non-admin staff see the Skills nav link and the page, not "Admin access required"
- [x] Backend blast radius — every `tests/unit` file referencing `require_admin_user` / `require_srp_account` / `/internal`: **240 passed**
- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright, import-linter (8 contracts kept)
- [x] dashboard-console: `pnpm run lint`, `pnpm run typecheck`, `pnpm run test` — **615 passed / 71 files**
- [ ] Not verified against a running console (needs Firebase + a live session). The meaningful check post-deploy is a **non-admin** `@srp.one` account loading `/skills`.

## Deploy

Cross-surface — **backend first**. If the frontend ships first, non-admin staff get a visible Skills link whose API calls still 403 until claw-interface catches up. Backend-first has no broken window: admins are unaffected and non-admins simply don't see the link yet.

## Note

`AdminOnly` now has no production consumer — only its own test file. Left in place deliberately: the other admin-only console routes (subscription codes, releases, users) currently have no frontend guard at all and are arguably where it should be used next. Worth a follow-up decision rather than a silent delete here.


---

## feat(agent-builder): add engine-backed builder v2 (#3121)

- sha: 7f5dfa0725dfdfb237dcff76cd3b9cbbda650f03
- author: kaka-srp
- date: 2026-07-29T12:29:37Z
- PR: #3121

### Commit message



### PR body

## Linear

https://linear.app/srpone/issue/ECA-1315/agent-builder-v2

## Summary

- Introduce a fully versioned Agent Builder entry boundary so v1 and v2 use separate frontend APIs, clients, backend routers, runtime services, and project ownership checks. This keeps v1 compatible while making it removable later.
- Route eligible users to Engine-backed Agent Builder v2 using the same backend capability rule as Agent v2 installation. Staging and local development are open; production remains controlled by the configured email allowlist and global kill switch.
- Provision one hidden, warm Agent Studio Engine Agent per account/org and reuse its Sandbox across Builder projects. Each project receives an independent Engine session and Mattermost channel.
- Implement shared-Sandbox project isolation with capture/activate/restore operations, backend operation leases, stale-operation recovery, and first-activation initialization for new projects.
- Add v1 project upgrade gating and migration into v2. Migration captures the legacy workspace, imports it through Agent Studio tooling, preserves the original project on failure, and switches runtime metadata with compare-and-set protection.
- Move Pack Test v2 to managed Engine Test Agents. Reuse the physical Test Agent when the Environment hash is unchanged, create a fresh session per run, and replace the Agent when Environment content changes.
- Integrate Engine Sandbox prepare/exec/cleanup APIs, exact environment-version polling and logs, scoped archive upload validation, Pack skill pins, warm creation, model selection, and runtime cleanup.
- Use ACS terminal-message metadata for reliable Pack Test completion and prevent premature or missing candidate-response handoff.
- Simplify the v2 UI by removing legacy Claw connection/header model controls, adding explicit preparation and migration states, and keeping model selection in the chat composer.
- Update the Agent Builder v2 design and implementation documents with runtime ownership, workspace isolation, migration, Pack Test, submission, cleanup, and rollout decisions.

Related Agent Studio work:

- https://github.com/SerendipityOneInc/ecap-agent-pack/pull/209

The required Engine changes have been merged and released to staging as `v0.1.0-beta.75`.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/verify-py.sh`
- [x] Backend targeted suite: 306 passed
- [x] Frontend selected verification: TypeScript, 481 Vitest tests, and ESLint passed
- [x] Manual staging-backed local validation of project creation, activation, migration, Pack Test, submission, update, and Engine runtime preparation

## Review notes

- This is intentionally a large feature PR because the version boundary must land atomically across frontend routing, backend ownership, runtime orchestration, persistence, migration, and tests. Splitting those contracts would leave an intermediate state where v1 and v2 can call each other's endpoints.
- Please apply the `size-override` label for the repository size gate.
- Local tests must override `AGENTS_V2_ENABLED=false` when running with the developer staging `.env`; otherwise existing install tests intentionally contact the configured staging ACS.


---

## feat(council): persist the dispatch thread on the run (#3120)

- sha: f119977b1d42a046ea2e07a8898fdd211244f530
- author: bill-srp
- date: 2026-07-29T11:40:42Z
- PR: #3120

### Commit message



### PR body

## Linear

None — this came out of a code review of `feat/council-frontend`, not a tracked issue.

## Summary

Records which Mattermost session thread a council run's conversation lives in.

Today the frontend posts `/council {topic}`, `go`, and `cancel` into whatever channel happens to be active, and nothing persists where they went. Consent is therefore only reachable from the tab that started the run — a reload or a second device loses the thread, on a record whose whole purpose is to be cross-device.

One new field on the run:

```python
dispatch_root_post_id: str | None = None
```

Optional on `CouncilRunCreateRequest`, persisted on `CouncilRun`, echoed on `CouncilRunResponse`.

### Only the root post is stored

An earlier revision of this branch stored `{session_id, mm_channel_id, root_post_id}`. Two of those were derivable and have been dropped:

- **`session_id`** was never read, by either surface, and `OpenClawSessionChannelRecord` keys on `root_post_id` — so the session is reachable from the root if anything ever needs it.
- **`mm_channel_id`** is the owning agent's `session_channel_id`. The frontend has it from the agents query, which it already runs and which sits in `PERSIST_ALLOWLIST_PREFIXES`, so it survives a reload without a round-trip.

What storing the channel would have bought: `go`/`cancel` not waiting on the agents query, and a run staying approvable if the user's main agent is replaced and gets a new session channel. Neither justifies a field on every run forever — Mattermost rejects a `root_id` from a different channel, so the replaced-agent case fails loudly rather than posting somewhere wrong, and adding a field later is trivial where removing one after documents carry it is a migration.

### Why this was deferred before, and why it isn't expensive now

`docs/superpowers/specs/2026-07-28-council-frontend.md` weighed this as option **B** and deferred it because "the thread does not exist until after the post" — which would have forced a follow-up write path.

With session threads it exists first. `POST /agents/{workspace_id}/conversations` seeds the thread root *before* any message is sent, so the frontend already holds `root_post_id` when it calls `POST /council/runs`. The ordering objection is gone and no second write path is needed.

Option **C** (refresh-on-read polling) is unaffected and stays. C answers *which run to refresh*; this answers *which thread the conversation lives in*. They are complementary — the second question was never addressed and had quietly shipped as "whatever channel is active".

### Scope

Backend only, plus the design spec. The matching frontend change is deliberately **not** here — it lives on `feat/council-frontend` and must deploy *after* this one, because an older API would reject the new key under `extra="forbid"`.

The field being additive and optional is what makes that ordering safe: existing clients keep working unchanged, and a run whose session creation failed is still a legitimate record — it simply cannot be advanced from the UI.

Full design, including the frontend half: `docs/superpowers/specs/2026-07-29-council-session-thread-dispatch.md`.

## Test plan

- [x] `CouncilRunCreateRequest` still accepts topic-only; carries `dispatch_root_post_id` when supplied; still rejects unknown keys under `extra="forbid"`
- [x] `create_run` persists the root post it was handed
- [x] `to_response` projects it — without this, `go` has nowhere to post after a reload
- [x] Pre-existing runs default to `null` through both the record and the response
- [x] 195 council unit tests pass
- [x] `bash scripts/verify-py.sh` green — ruff, ruff-format, pyright, import-linter (8/8 contracts)
- [ ] Staging: confirm the council skill is triggered when `/council {topic}` arrives as a thread reply in the session channel. **Still unverified against a real Claw** — the backend's own long-standing open item, now load-bearing in a new way because this changes where the message lands.


---

## fix(web): console loading and layout consistency (#3103)

- sha: 101e5f4852d6a52d65ce39906b8c51260adcd16f
- author: david-srp
- date: 2026-07-29T10:45:58Z
- PR: #3103

### Commit message



### PR body

## 背景

控制台两项一致性修复,每项一个 commit。基于 main,与其他 PR 零文件交集,可独立随时合并。

| Commit | 修复 |
|--------|------|
| 骨架/页宽统一 | agents-manager 的 Suspense fallback(4 列)与 client 加载分支(3 列)骨架不一致导致加载完成布局跳动 → 抽出共享 `AgentCardSkeletonGrid`,两处引用同一组件,结构上不可能再漂移(复核另修掉滚动容器交接不一致与 4px 垂直跳动两处隐性问题);/plugins 三个 tab 统一 `max-w-6xl` 容器 + 单 h1(connector hero 的 h1 降级为区块标题) |
| 日程页白屏 | bot 未就绪时 `return null` 的空白页换成 `ClawSpinner` + "正在准备工作区…"等待态;五个 gate 分支互斥性逐条核验;中英文案齐 |

## 测试

- 相关 spec 274 测试绿;push 时 fast-tier(guards + tsc + eslint)通过;合并态整树校验曾全绿

## 部署注意

纯前端,无后端依赖。

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(dashboard-console): wrap skill descriptions and move Skills nav below agent packs (#3119)

- sha: e5eb73109781aee78d06b33e53cb3929b01ad5ac
- author: bill-srp
- date: 2026-07-29T10:44:14Z
- PR: #3119

### Commit message



### PR body

## Summary

Two UI fixes on the dashboard-console Skills page.

- **Long skill descriptions no longer overflow their column.** They were rendering as a single unbroken line that painted across the Scope / Status / Version / Ownership / Updated cells.
- **Skills moved in the sidebar** from the Administration section to the end of the Catalogue group, below the agent-packs entries. The admin gate travels with it.

Sidebar after the change:

```
CATALOGUE            BILLING              ADMINISTRATION
  Overview             Offline orders       Subscription codes
  Agent packs                               Releases
  Listing reviews                           Users
  Vertical plans
  Skills  <-
```

## Root cause

**Description overflow.** `TableCell` bakes `whitespace-nowrap` into every cell (`app/components/ui/table.tsx`, a shadcn default). `white-space` is an inherited property, so the description span inherited `nowrap` and never wrapped. `max-w-xl` still capped the box at 576px — which is exactly why the text spilled *past* its own edge instead of just widening the column.

Fix is one class, `whitespace-normal`, on the description span. A declaration on the element always beats a value inherited from the `<td>`, so there is no cascade ambiguity. The override is deliberately local rather than dropping `whitespace-nowrap` from the shared `TableCell`: the other console tables depend on it for dates, mono IDs and badges, and `releases-table.tsx` pairs it with `truncate` on purpose. Skills was the only table with a wrapping-intent text block, so the bug was isolated.

**Sidebar move.** Not a bug, just placement — but it carries one trap worth flagging in review. `ADMIN_NAV_ITEMS` gets its gate from the enclosing `isAdmin` block, while the Catalogue group renders for every signed-in user. A straight move would have shown a Skills link to non-admins, dropping them on `AdminOnly`'s "Admin access required" wall and advertising the admin surface. So `NavItem` gains an `adminOnly` flag and Catalogue filters on it, keeping the gate attached to the entry. The route stays independently protected by `AdminOnly`, and the backend by `require_admin_user`.

## Test plan

- [x] TDD on both changes — failing test written and confirmed RED first, then GREEN:
  - description wraps (asserts `whitespace-normal` + `max-w-xl`, matching the existing class-assertion idiom in this suite)
  - Catalogue link order is `Overview -> Agent packs -> Listing reviews -> Vertical plans -> Skills`
- [x] Regression test: non-admins get no Skills link (guards the gate described above)
- [x] `pnpm run lint` — clean
- [x] `pnpm run typecheck` — clean
- [x] `pnpm run test` — **615 passed / 71 files** (was 613; +2 new tests)
- [x] Verified Tailwind emits `.whitespace-normal{white-space:normal}` in the built CSS (v4 only generates used utilities)
- [ ] **Not verified visually against a running console.** Rendering the real page needs Firebase auth plus an admin-backed `/internal/*` session, which was disproportionate here — the evidence above is mechanism plus gates, not pixels. Worth a glance post-deploy, mainly to judge whether 576px is the right description column width.

Frontend-only; no backend deploy needed.


---

## feat(web): chat composer UX improvements (#3102)

- sha: d07a23a65a94728a74bbe37200a3147dcb2b3052
- author: david-srp
- date: 2026-07-29T09:56:15Z
- PR: #3102

### Commit message



### PR body

## 背景

聊天输入区 5 项交互优化,每项一个 commit。**堆叠 PR:base 是 `fix/chat-ui-bugfixes`(bug 修复批次),请先合那个;合入后本 PR 会自动 retarget 到 main。**

| Commit | 优化 |
|--------|------|
| 最近文件 | "最近文件"菜单从 `slice(0,2)` 放宽到 8 条,子菜单内滚动(复用 SkillsSubMenu 同款模式),"从资源库添加"固定可见 |
| 附件类型图标 | 附件芯片非图片文件补上彩色类型图标(映射 `composer-file-type-icons.ts` 已存在,此前只有"最近文件"菜单在用);两种 presentation 都覆盖;复核纠正一处 token 选择(`bg-card` 而非 `bg-background`,避免 light 模式角标消失) |
| 引用截断 | 引用回复预览 150 字 vs 实发 200 字的"所见非所发"统一为共享常量 200,并改为按码点截断(不劈开 emoji/CJK) |
| Enter 抑制 | 流式回复期间按 Enter 不再静默插入换行(preventDefault 吞掉);Shift+Enter 保留;IME 组合确认路径逐行核验不受影响 |
| launcher 缩略图 | new-chat 页选的图片立即显示缩略图(object URL,创建/移除/发送/卸载全路径 revoke 无泄漏),消除进入会话后附件"变身"的断层 |

> 注:引用截断 commit 在源分支曾因并发暂存竞态挂错 message,cherry-pick 时已更正,内容不变。

## 测试

- app 侧相关 spec 187/187 绿;`@zooclaw/chat-ui` 包内 317/317 绿;push 时 fast-tier(guards + tsc + eslint)通过
- 合并态整树校验曾全绿(543 文件 / 7381 测试)

## 部署注意

纯前端。与消息流 UX PR、控制台 UX PR 相互独立,可并行 review。

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(web): open agent v2 installs in staging (#3108)

- sha: 1999b56df090e8e9b396e80efe0f45edc00b2c5a
- author: bill-srp
- date: 2026-07-29T09:54:25Z
- PR: #3108

### Commit message



### PR body

## Summary
- Open Agents V2 install routing to every pack-backed user in staging and local development.
- Preserve `AGENTS_V2_EMAIL_ALLOWLIST` gating in production and fail closed for unknown deployed environments.
- Skip the account email lookup when the environment already grants access, with coverage for staging, local development, and production contracts.

## Root cause
The web BFF treated the email allowlist as the only Agents V2 rollout signal in every environment. As a result, staging users outside the list continued to use the legacy computer install path even though staging is intended for unrestricted V2 validation. The same behavior also prevented the documented local development flow from exercising V2 without manual allowlist setup.

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/app/api/agents/install/route.ts web/app/tests/unit/app/api/agents/agents-install.unit.spec.ts`
- [x] `bash scripts/verify-changed.sh`


---

## fix(claw-interface): align pack environment config with engine (#3118)

- sha: 035ca6cd45e6acf5bb814437a7d805506c3aff42
- author: bill-srp
- date: 2026-07-29T09:14:28Z
- PR: #3118

### Commit message



### PR body

## Summary
- send the Engine-required unrestricted networking policy for Pack environment versions
- retain the declared `pack.zip` after extraction so Engine file-integrity verification can succeed
- lock both contracts in service/client tests and update the environment binding design

## Root cause
Claw-interface omitted `config.networking` under the assumption that Engine supplied a default, but Engine requires an explicit `limited` or `unrestricted` policy and rejected the create request with HTTP 400.

After that validation blocker, the build script would also delete `pack.zip`. Engine verifies every declared environment file after the build script completes, so the missing archive would deterministically fail the version during verification.

## Test plan
- [x] `pytest -q tests/unit/test_pack_environment_service.py tests/unit/test_engine_client_environments.py` — 48 passed
- [x] `bash scripts/verify-local.sh --py-static`
- [x] pre-push `bash scripts/verify-changed.sh`


---

## fix(chat): improve agent connection failure state (#3117)

- sha: f11273537a311b3a5d3eb9210e25c51cf229535e
- author: lynn Zhuang
- date: 2026-07-29T09:11:47Z
- PR: #3117

### Commit message



### PR body

## Summary

- Replace the raw Mattermost fetch error with a product-safe agent connection recovery state.
- Use the supplied no-connection illustration, visually offset 10px left, with localized English and Chinese copy.
- Preserve the retry behavior while hiding duplicated technical errors and internal hostnames.

## Root cause

The full-screen Mattermost failure path reused a low-level error view that exposed transport details directly to users. This produced Claw-specific terminology, duplicated failure messaging, and internal service URLs instead of an actionable Agent recovery state.

## Test plan

- [x] `pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/chat/ChatGateStates-recorder.unit.spec.tsx tests/unit/app/chat/GenClawClient.internals.unit.spec.tsx` — 53 tests passed
- [x] `bash scripts/verify-web.sh --no-test ...` — governance guards, TypeScript, and ESLint passed
- [x] `bash scripts/verify-changed.sh` — changed frontend surface passed
- [x] Browser visual validation — illustration returned HTTP 200, decoded at 200x200, and measured 10px left of the button center


---

## feat(dashboard-console): add read-only skills registry (#3112)

- sha: e88022a8ef5f27e6ac77106f6958f3fb09abbaa0
- author: bill-srp
- date: 2026-07-29T08:49:45Z
- PR: #3112

### Commit message



### PR body

## Linear

N/A

## Summary

- add an admin-only `/skills` page to Dashboard Console
- route console reads through claw-interface `GET /internal/skills` and `GET /internal/skills/{skill_id}/versions/{version}`
- enforce both the parent SRP-staff boundary and the claw-interface admin allowlist
- request `scope=global` from zooclaw-engine so internal pagination and totals are global-only
- reject any non-global list row or detail lookup at the claw-interface service boundary
- align the console copy and fixtures with the global-only registry contract
- disable stale row inspection and pagination while the next page is loading
- support name search, refresh, pagination, and current-version inspection
- show version identity, frontmatter, and immutable file manifest without exposing mutation controls
- keep an open detail dialog synchronized with the latest registry row/version after refresh
- retain same-query registry/version data with an inline retry when refresh or pagination fails
- reset search, pagination, selection, and stale-display state when the authenticated uid changes
- scope list and version query caches by authenticated user

## Test plan

- [x] claw-interface client/service/internal Skills tests — 57 tests passed
- [x] claw-interface internal/public/org Skills route tests — 20 tests passed
- [x] `bash scripts/verify-py.sh` — ruff, format, pyright, and import contracts passed
- [x] `pnpm --dir dashboard-console test` — 612 tests passed
- [x] `pnpm --dir dashboard-console typecheck`
- [x] `pnpm --dir dashboard-console lint`
- [x] `pnpm --dir dashboard-console build`
- [x] browser smoke test for list, search, detail dialog, and 390px responsive layout


---

## fix(council): normalize discovery timestamps (#3115)

- sha: 3b420e41c459ccdac8e0ea01a43e9d7d7e56d205
- author: bill-srp
- date: 2026-07-29T07:59:56Z
- PR: #3115

### Commit message



### PR body

## Summary
- Normalize Council timestamps at the Mongo/FastClaw boundary.
- Compare and sort discovery directory mtimes in UTC.
- Add a regression test for a Mongo UTC-naive `created_at` and FastClaw timezone-aware `mtime`.

## Root cause
PyMongo reads persisted UTC datetimes without timezone information, while FastClaw directory listings return timezone-aware mtimes. Council discovery compared those values directly, raising `TypeError: can't compare offset-naive and offset-aware datetimes` and returning HTTP 500 from the refresh endpoint.

## Test plan
- [x] `pytest tests/unit/test_council_*.py -q` — 189 passed
- [x] `bash scripts/verify-py.sh`
- [x] pre-commit and pre-push hooks


---

## fix(claw-interface): parse engine upload envelope (#3114)

- sha: 52f2a1e75181242c986b3bd7e78dc76891280da9
- author: bill-srp
- date: 2026-07-29T07:51:54Z
- PR: #3114

### Commit message



### PR body

## Summary

- parse Engine Environment upload declarations from the documented `uploads[]` response envelope
- update the regression fixture to match the real Engine contract
- correct the original implementation plan example so it no longer preserves the wrong `files[]` assumption

## Root cause

The Engine upload API has returned `uploads[]` since its initial implementation, but `claw-interface` was introduced with a mocked `files[]` success response and parsed that same incorrect field. The earlier admin-token failure masked this contract mismatch until staging first received a successful `201` response.

## Test plan

- [x] verified the regression test fails against `uploads[]` before the parser change
- [x] 48 Environment client, Pack environment, and staging wiring tests
- [x] `bash scripts/verify-py.sh`
- [x] pre-commit hooks


---

## fix(council): read runs from main agent workspace (#3113)

- sha: 3015d04ffc72ea77e25ccf07f4e3ee9ad8602343
- author: bill-srp
- date: 2026-07-29T07:28:48Z
- PR: #3113

### Commit message



### PR body

## Summary

- read Council run snapshots from the main agent workspace at `/workspace/main/council-runs`
- resolve relative and absolute member-report artifacts against the same main-agent run root
- lock discovery, pinned refresh, and report reads to the deployed FastClaw path contract

## Root cause

The Council skill writes relative to the OpenClaw main agent workspace. In deployed bot pods, `/home/node/.openclaw/workspace` points to `/workspace/main`, so the real snapshots live under `/workspace/main/council-runs`.

The backend listed `/workspace/council-runs` instead. A missing directory is intentionally treated as “not started yet,” so refresh returned HTTP 200 with the unchanged Mongo record and never reached `transition_state`.

## Validation

- `pytest tests/unit/test_council*.py -q` — 188 passed
- `bash scripts/verify-py.sh` — ruff, format, pyright, and import-linter passed
- pre-commit and pre-push hooks passed


---

## fix(claw-interface): use engine admin token for admin routes (#3111)

- sha: 1a2943e2099746d7654fa9de6d449835896df9bc
- author: bill-srp
- date: 2026-07-29T07:22:23Z
- PR: #3111

### Commit message



### PR body

## Summary

- use `ZOOCLAW_ENGINE_ADMIN_TOKEN` for Engine `/admin/v1/*` requests while preserving `ZOOCLAW_ENGINE_SERVICE_TOKEN` for `/v1/*`
- inject only `CONTROLD_ADMIN_TOKEN` from the existing staging Engine secret into `claw-interface`
- fail startup when Agents v2 is enabled without the required admin credential, while keeping non-v2 deployments compatible
- add client and deployment regression coverage, and correct the architecture/design documentation

## Root cause

The Pack environment pipeline called Engine global admin endpoints with the service credential. Engine intentionally masks unauthorized admin routes as `404`, so skill registration and environment upload declaration failed before `environment_id` and `environment_version` could be persisted.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] 149 targeted Engine client, Pack environment, internal route, review hook, and deployment contract tests
- [x] render the staging overlay with `kubectl kustomize` and verify the single-key secret mapping
- [x] pre-commit hooks


---

## fix(council): normalize persisted refresh timestamps (#3110)

- sha: 61aff51327c823b4fd5f7fd234a8577e80e268b2
- author: bill-srp
- date: 2026-07-29T06:52:35Z
- PR: #3110

### Commit message



### PR body

## Summary

- normalize Mongo UTC-naive Council run timestamps before refresh interval arithmetic
- cover both recent and stale persisted timestamps with regression tests
- prevent the Council refresh endpoint from returning HTTP 500 for persisted runs

## Root cause

PyMongo returns `updated_at` without timezone information, while the refresh limiter compared it with `datetime.now(UTC)`. Python rejects arithmetic between offset-naive and offset-aware datetimes.

## Validation

- `/Users/bill/.venvs/claw-interface/bin/pytest tests/unit/test_council_run_service.py -q` — 20 passed
- `bash scripts/verify-py.sh` — ruff, format, pyright, and import-linter passed
- pre-commit and pre-push hooks passed


---

## feat(dashboard): show pack environment build status (#3107)

- sha: 45e49eb6300cc337356fd6d9697bc52c79a4e7cf
- author: bill-srp
- date: 2026-07-29T06:36:40Z
- PR: #3107

### Commit message



### PR body

## Linear

N/A

## Summary

- expose each Pack's `environment_id` in the Dashboard catalogue
- add an admin-only live status endpoint for the latest approved submission's exact Engine Environment version
- show the current Environment version and build status on the Pack submissions page, polling non-terminal states every five seconds
- reject mismatched Engine Environment/version responses instead of displaying stale or unrelated status

## Test plan

- [x] Backend targeted unit tests: 93 passed
- [x] Dashboard Console full test suite: 580 passed
- [x] Dashboard Console typecheck and ESLint
- [x] Backend Ruff, targeted Pyright, import contracts, file-length, and complexity gates


---

## feat(agent-packs): rebuild docs environment from console (#3106)

- sha: aa9b4359ed2857859df1f3a6d51ffcb088cdf6c4
- author: bill-srp
- date: 2026-07-29T05:47:05Z
- PR: #3106

### Commit message



### PR body

## Linear

N/A

## Summary

- add an admin-only endpoint that schedules the latest approved ZooClaw pack submission through the existing docs, skills, and environment build pipeline
- reuse the approved submission without creating a new submission or changing its review state
- add a confirmed Dashboard Console row action with duplicate-request protection and running, success, and error feedback

## Test plan

- [x] `env PATH=.../.venv/bin:... bash scripts/verify-py.sh`
- [x] `.venv/bin/pytest tests/unit/test_admin_route_wiring.py tests/unit/test_internal_agent_packs_routes.py tests/unit/test_pack_environment_service.py -q` (76 passed)
- [x] `pnpm run lint` in `web/dashboard-console`
- [x] `WRANGLER_LOG_PATH=/private/tmp/dashboard-console-wrangler.log pnpm run typecheck` in `web/dashboard-console`
- [x] `pnpm run test` in `web/dashboard-console` (572 passed)


---

## feat(kb-archive): archive (.zip/.tar/.tar.gz) upload — BFF passthrough + web two-level tree (#3096)

- sha: 1a4a89f592381ccaa9647d7a8e1d2b88214f5ddf
- author: kyle-srp
- date: 2026-07-29T04:25:46Z
- PR: #3096

### Commit message



### PR body

## What

Client + BFF for **knowledge-base archive upload** — the workspace half of the archive feature. Users drop a `.zip` / `.tar` / `.tar.gz`; the proxy extracts it and ingests each supported file as its own KB document (all-or-nothing), and the UI shows the bundle as one expandable node over its files.

Backend counterpart: **ecap-proxy-service PR #168** (`POST /knowledge-base/upload/archive`, `DELETE /knowledge-base/archives/{id}`, provenance + resource guards). This PR is safe to merge alongside it.

## BFF (`claw-interface`) — E段

- `POST /knowledge-base/upload/archive`: transparent passthrough with the larger **100MB** archive body cap (vs 50MB single-file); mirrors the existing `upload_document` shape.
- `DELETE /knowledge-base/archives/{id}`: idempotent passthrough, mirroring the existing `delete_document` / `delete_kb` `@router.delete` routes in this module.
- `_error_detail` now forwards a structured **dict/list** `detail` intact, so the web can localize the proxy's `{code, params}` rejection instead of it being flattened to a generic string.

## Web — F段

- **Endpoint routing by extension** (F1): archives → `/upload/archive`, everything else → `/upload`. Both target the same library.
- **Client precheck** (F2): archives get the 100MB soft cap; >100MB rejected with a local toast.
- **Two-level tree** (F3): `DocumentList` groups files sharing an `archive_id` under one collapsible node (`archive_filename` + count; children show `display_path` + index status); single files stay leaves. `onDelete` remains optional so read-only shared-library views are unaffected.
- **Per-archive delete** (F4): node delete → confirm → `DELETE /archives/{id}`.
- **Localized errors** (F5): each structured rejection code (`archiveUnsupported` / `archiveCorrupt` / … / `archiveBusy`) maps to an en + zh message; 429 → "try again shortly".
- **Success count** (F6): imported-document count in the success toast.

## Rebased onto current main

The original archive work sat on a 183-commits-stale branch where the KB UI lived at `(app)/knowledge-base/`. main relocated it to `(app)/plugins/knowledge-base/` and shipped JSON/MD support + collaborator/grants. This PR re-applies the archive feature onto the **current** structure; the stale JSON/MD commits were dropped (already on main). Kept lean: `isAcceptedUpload` (used only by its own test) and an unused `KnowledgeBaseArchiveItem` export were dropped to satisfy the dead-code gate.

## Tests

- BFF: `TestKnowledgeBaseArchiveProxy` — 4 tests incl. `test_dict_detail_preserved` (whole file **35 passed**; route pyright-clean).
- Web: 5 new specs (constants F1/F2, service E/F1, `UploadDropzone` F2, `DocumentList` tree F3/F4, `KnowledgeBaseClient` routing/errors F1/F5/F6) — **16 tests**. Full KB dir **106 passed** (no regression); `tsc` clean; `dup:src` + knip clean for touched files.

> Note: eslint couldn't run in the authoring checkout (workspace `@zooclaw/design-system` not linked locally); CI `web-quality` is the authoritative eslint gate. Code mirrors the surrounding files' style.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(whatsapp): preserve sender country code (#3105)

- sha: e307c19e49230e826c42e6a39610dee958a5a67f
- author: bill-srp
- date: 2026-07-29T03:31:56Z
- PR: #3105

### Commit message



### PR body

## Summary
- send the WhatsApp sender phone number to the account service in E.164 form
- keep the original Meta `wa_id` unchanged for WhatsApp identity matching
- lock the account-service request contract with a regression test

## Root cause
The bridge sent an eleven-digit US `wa_id` as a bare `phone_number`. The account service reused its domestic SMS normalizer and interpreted any eleven-digit value beginning with `1` as a Chinese mobile number, prepending `+86`. Claw Interface then rejected the account because the stored phone digits no longer matched the WhatsApp identity.

## Test plan
- [x] `pnpm test`
- [x] `pnpm typecheck`
- [x] `pnpm build`
- [x] targeted Claw Interface matching-phone test

## Operational note
Accounts already persisted with the incorrect `+86` prefix still require a staging data repair or recreation before they can bind successfully.


---

## fix(web): chat UI bug-fix batch (line breaks, avatars, my-uploads, session history, files panel) (#3100)

- sha: d35d218001ef2ad4604cca888b6875822d1978a6
- author: david-srp
- date: 2026-07-29T03:30:28Z
- PR: #3100

### Commit message



### PR body

## 背景

聊天界面 5 个用户报告的 bug,每项一个独立 commit(附回归测试),可整体快速合入:

| Commit | 修复 | 根因 |
|--------|------|------|
| 换行丢失 | 多行消息发出后"第二个及以后的换行"消失 | `globals.css` 历史规则 `.prose br + br { display:none }`(ECA-420)——CSS `+` 选择器无视文字节点,把有内容间隔的 `<br>` 也隐藏了。改为在 HTML 管线中只折叠**真正相邻**的 `<br>` 连排,保留 ECA-420 意图 |
| 头像不一致 | 同一 agent 侧边栏显示 🤖、chat 头部显示默认 Assistant 头像 | 头部/气泡的解析链从不读 workspace `avatar_url`;现收敛为共享 `resolveAssistantAvatarPresentation` + 新 `AgentAvatar` 组件,侧边栏/头部/气泡统一,非主 agent 兜底 🤖 |
| 我的上传为空 | 聊天里发的附件不出现在「我的上传」面板 | MM 上传路径用自拼 session key 记录资产,与面板查询的规范 key(`computer:<cid>:<agent>`)不匹配;改用同一 sessionKey,附防重测试(历史错 key 数据不迁移,新上传生效) |
| Session History 冗余 | 零 session 的新 agent 也显示 Session History 入口 | 加载完成且列表为空时整块隐藏(加载中也不显示避免闪烁;错误态保留兜底入口) |
| 文件面板无法关闭 | 右侧文件面板只能从页头图标关 | 面板右上角新增关闭按钮,与页头 Files 图标共用同一状态源 |

## 测试

- 每项均带单测(换行含截图原文 CJK 回归用例;头像 +13 例;上传防重 fail-then-retry 用例)
- 分支独立校验:guards + 全量 tsc + eslint 全绿;关键 spec 组 vitest 全绿
- 全部 22 个 commit 合并态下曾整树校验:543 文件 / 7381 测试全绿

## 部署注意

- 纯前端;「我的上传」的资源库按-agent 筛选完整生效还需后端 PR(greeting/上传/头像后端三合一)配合发版
- 另有两个堆叠 PR(消息流布局 UX、输入区 UX)以本分支为 base,先合本 PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(council): add the runs API and pod status reader (#3098)

- sha: 2c65849671d5fe3326379cf020754a0dbb50a764
- author: bill-srp
- date: 2026-07-29T03:27:24Z
- PR: #3098

### Commit message



### PR body

## What this is

**Slice 3 of 3** — the final piece. Wires the router and adds the service that creates/lists runs plus the reader that keeps them current from the pod's `status.json`.

| slice | contents | status |
|---|---|---|
| 1 | run record, state machine, pod file boundary | merged (#3095) |
| 2 | raw member report persistence | merged (#3097) |
| **3 — this PR** | runs API + pod status reader | here |

After this, the `/council` backend is complete and reachable. Together the three replace #3089, which was 5,329 lines and could not run CI's real jobs.

## The shape

```
frontend ──"/council {topic}"──► Mattermost ──► bot pod (council skill)
    │                                                │ writes council-runs/<slug>-<id>/
    ├── POST /council/runs ──────► claw-interface    │
    └── POST …/refresh ─────────► reads status.json via fastclaw ◄─┘
```

**The backend never orchestrates and never sends.** The frontend posts the command as the user; the skill on the pod does the casting, evidence gathering, blinding, debate and synthesis. This service records that a run exists and reads back what the skill wrote. No callback, no outbound HTTP, no dispatch.

Specs, including two rejected alternatives, are in `docs/superpowers/specs/2026-07-28-*.md`.

## What to review

**Folder discovery, not folder naming.** The skill names its own run folder (`council-runs/<topic-slug>-<id>/`, fixed in SKILL.md) and has no `--run-id` flag, so we cannot tell it ours. On first refresh the backend lists `council-runs/`, keeps directories whose `mtime` postdates the run, reads each candidate's `status.json`, and requires **both** that the topic matches and that the folder name equals the snapshot's own `run_id`. The winner is pinned with a write-once CAS; every later refresh is one direct read. Folders already claimed by the user's other runs are excluded.

This also makes dispatch **self-verifying**: if the folder exists, the agent received the message. The backend never needs the frontend to confirm it sent anything.

**Ambiguity is refused, not guessed.** Two candidates matching one run means we cannot know which is ours — so nothing is pinned and the next refresh retries. Reachability is narrow: `create_run` rejects while any run is non-terminal, so a user holds at most one active run, and the only route to two matching folders is posting the same topic twice for a single record. The cost is one stuck record rather than a run permanently bound to the wrong folder, which would be silent and unrecoverable.

**Read back, do not dictate.** `tier`, `depth`, `estimate`, `members` and `synthesizer` all come from `status.json`. The skill resolves depth from the topic when unspecified and quotes cost "from the cast's own prices, never from the tier name" — so computing these here would create a second source of truth that drifts. `tier` accepts `premium`, which a real fixture uses and which the original enum rejected.

**Write only on change**, terminalise **only** because `status.json` says so, and re-validate pod identity on every pinned read — folder name, snapshot `run_id` and topic must all still agree, so a recycled pod cannot silently substitute another run's content.

**Owner-scoped reads.** Routes load runs via `council_run_repo.get_for_user(account.uid, run_id)`. This matters because `council_report_repo.list_for_run` filters on `run_id` alone — possession of the `CouncilRun` *is* the authorisation. Fetching a run by id and passing it to the report service would serve another user's reports.

**The account is resolved once at the auth boundary** and passed down. Nothing in `app/services/council/` loads an account.

## Verification

`ruff`, `ruff format`, `pyright` (0 errors), `lint-imports` (8/8 contracts), all eight `scripts/ci-lint` guards. **6,864 unit tests pass.**

Council module coverage: `routes/council.py`, `run_service.py`, `pod_files.py`, `schema/council.py` at 100%; `status_poll.py` 99.37%; `member_reports.py` 97.26%; `council_run_repo.py` 96.08%.

**Coverage caveat, stated honestly:** the whole-app number here is unit-only — 89.57%. That is *not* the CI figure; BDD is excluded and covers materially more. On #3095 the same measurement read 89.48% against a full-suite 90.07%, so CI should land near 90.1%. Inferred, not measured — CI is the authority on this one.

## What has NOT been verified, and it matters most in this slice

**None of this has run against a real bot.** Every test mocks the pod. That method already found four cases on this branch where the code modelled data the skill never produces — an entire `result.json` contract, a `moderator` role the v3 pipeline removed, an `analysis` map that is built but unwired, and report size/status fields. All four had passing tests.

Slices 1 and 2 were unreachable, so this was theoretical. **This slice makes it live**, and three assumptions are now load-bearing:

1. That the skill's run folder sits under `/workspace` — everything here assumes that root.
2. What `read_bot_file`'s response envelope actually contains, and whether FastClaw caps size below our 2 MiB bound.
3. **That `/council {topic}` triggers the skill at all.** The original dispatch template hedged with a prose fallback because slash parsing was uncertain; the simplified form drops it. If this is wrong, no folder is ever created and every run sits in `dispatching`.

One staging dispatch closes all three. I would not enable this for users before that run.

## Carried forward deliberately

- **`pod_files` API narrowing.** `read()`/`list()` accept any `/workspace` path; run-folder confinement lives in `run_artifact_path()`, which is where untrusted input (`members[].report`, `artifacts.report`) crosses. No out-of-run read is reachable, but the API does not make it impossible. Deferred from #3095 pending real call sites — which now exist, so this is the natural next cleanup.
- **Partial-response signal.** `GET …/reports` cannot distinguish "member wrote nothing" from "report exists but unretrievable". Derivable client-side by joining `members[].report`, but not explicit.
- **Two deferred P1s from #3097** — a Mongo write failure during terminal warm-up fails closed (intentional: silent success would hide that durable preservation did not happen), and an oversized *sole* report reads as `[]`.
- **`resolve_bot_credentials` resolves the current-org primary**, not the run's org, so a run created under org A is unreadable while org B is primary. Acknowledged in #3095 and explicitly not fixed.
- **A run whose pod is permanently gone stays non-terminal.** Deliberate — we genuinely do not know what happened, and inferring an outcome from elapsed time is exactly what this design removed. There is no watchdog and no sweep.

## Test plan

- [x] 6,864 unit tests green; 8/8 import contracts; 8/8 ci-lint guards
- [ ] CI green (full suite incl. BDD — the authoritative coverage number)
- [ ] **Staging: dispatch one real council.** Confirm the run folder path, the `read_bot_file` envelope, and that `/council {topic}` triggers the skill
- [ ] Verify a run advances through the gate to a terminal state via refresh
- [ ] Verify member reports serve from `GET /council/runs/{run_id}/reports`


---

## fix(agent-builder): refresh agent avatars (#3087)

- sha: af13a8964b80b2be0be7af6ede23a9060443d18f
- author: lynn Zhuang
- date: 2026-07-29T03:18:56Z
- PR: #3087

### Commit message



### PR body

## Linear

N/A

## Summary
- replace the Assistant avatar with the gold infinity artwork across default brand assets and landing surfaces
- replace the Agent Builder avatar with the crossed-tools artwork in the launcher, builder chat, and test chat
- complete the local Agent Builder mock state, model, and activation contracts so the avatar flow can be previewed end to end

## Test plan
- [x] `bash scripts/verify-web.sh`
- [x] `bash scripts/verify-web.sh --test-only web/app/tests/unit/scripts/mock-backend-agent-builder.unit.spec.ts`
- [x] `git diff --check`
- [x] opened the local Agent Builder project, sent a mock message, and verified the reply image uses `/avatars/agent_studio.png`


---
