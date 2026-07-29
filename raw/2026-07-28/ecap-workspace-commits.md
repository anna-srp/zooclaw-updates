# ecap-workspace commits — 2026-07-28

## 965150299b5493606e1dfcaded0c5b9f06ea818b
- 作者: bill-srp
- 日期: 2026-07-28T13:59:09Z
- PR: #3097

### Commit message

```
feat(council): persist raw council member reports (#3097)

## What this is

**Slice 2 of 3** for the `/council` backend. Adds the
`ecap-council-reports` collection, its repo, and the ingest/serve
service.

Like slice 1, this is **not yet reachable** — the callers
(`status_poll`, `run_service`) arrive in slice 3.

| slice | contents | status |
|---|---|---|
| 1 | run record, state machine, pod file boundary | merged (#3095) |
| **2 — this PR** | raw member report persistence | here |
| 3 | runs API + status reader | next |

## Why member reports, and only member reports

The synthesized report is delivered into the Mattermost thread —
durable, already rendered by the frontend — and its path travels in
`artifacts.report`, so a client can build the URL itself. Storing it
again would be redundant.

The **raw member reports are different.** They exist only in
`$RUN/raw-reports/` on the bot pod, and the FastClaw file API requires
that pod to be *running*. Pods get stopped and recreated. Without this,
a user opening a run a week later finds the record intact and its
content evaporated. These are the one council artifact with no other
home — which is exactly what makes them worth a collection.

`anonymized.md` is deliberately not persisted either: it is a synthesis
intermediate, not something a user reads.

## What to review

**One document per member report.** `{report_id, run_id, uid, org_id,
model, content_md, ingested_at}`. Ownership scope lives on the row even
though `run_id` is the access path. One doc *per run* would crowd the 16
MB limit and force loading every report to show one.

**Idempotent ingest.** A unique `(run_id, model)` index plus
`$setOnInsert` means a re-read returns the existing row rather than
rewriting it. `report_id` is bare `uuid4().hex`, matching the run-id
convention.

**Nothing caps the report count** — and that is deliberate. The cast
size is decided upstream by the skill: `roster.py` sets `SEATS_BY_DEPTH
= {"quick": 3, "standard": 4, "deep": 5}`, and `status_schema.json`
gives `members` a `minItems` with **no maximum**. A cap here could
therefore only ever truncate content the user paid for, silently, and
indistinguishably from working as intended. An earlier revision of this
branch did cap it at 5 — matching today's `deep` seat count exactly, so
it had zero headroom and would have started dropping reports the day
that constant moved.

The per-file **2 MiB** read bound stays, with an ERROR log naming the
model when it trips. Refusing one oversized file is not the same as
quietly dropping the tail of a set.

**Ingest is best-effort and runs after the terminal write, never before
it.** The run is terminal whether or not the text was captured; a failed
read logs with ownership scope instead of blocking terminalisation. Each
member is read in isolation so one unreadable report cannot abort the
batch. This is the "local terminal write is the contract, external work
happens after it" rule.

**Serving reads Mongo first**, and falls back to the pod for anything
not yet ingested.

**It persists only what is final.** A terminal run's fallback read is
written through — that is the repair path when best-effort
`ingest_terminal` missed a report. A **mid-flight** run's read is served
without being stored, because the content is still mutable:
`run_status.py:576` notes "a debate round overwrites it with v2", and a
`done → failed` downgrade moves the file into `raw-reports/failed/` and
rewrites the path. With `$setOnInsert` the first write wins permanently,
so caching mid-flight would freeze a pre-debate draft — or worse, a
report the skill deliberately quarantined so nothing would consume it.

## Codex review response

**P1, Mongo-first serve failed closed — accepted and fixed**
(`b0050d013`).

The finding was correct and it contradicted this PR's own premise.
`list_reports` loaded stored rows first, then filled gaps from the pod
with neither the reader open nor the per-member reads isolated:
`pod_files.for_run` raises whenever the runtime is missing, stopped or
org-mismatched, and `_read_and_store` re-raised everything except
`council.pod_file_too_large`. So a run with four of five reports already
in Mongo, whose pod had since been stopped or recreated, returned **503
and zero reports** — in exactly the scenario this collection exists to
survive.

Codex also spotted the internal inconsistency: `ingest_terminal` already
isolates per-member failures in the same module; the serve path did not.

Now a failed reader open logs at WARNING with ownership scope and serves
what is stored, and each member read is isolated the same way
`ingest_terminal` does.

**One case deliberately does not degrade:** nothing stored *and* the pod
unreadable still raises. An empty list there would assert the run
produced no reports — false, and indistinguishable from a genuinely
report-less run.

**No retry job is needed.** `list_reports` recomputes the missing set on
every call and persists what it fetches, so the serve path is also the
repair path: a pod that was merely stopped heals on the next view, and
this is the same backstop covering a failed best-effort
`ingest_terminal`. A *recreated* pod is unrecoverable — that window is
narrowed, not closed.

### Ownership is enforced upstream — slice 3 must not break that

`council_report_repo.list_for_run` filters on `run_id` alone; it carries
no `uid`/`org_id` predicate. That is intentional and safe **as long as
the caller already holds a `CouncilRun` obtained through an owner-scoped
read** — possession of the run object is the authorisation.

`uid` and `org_id` are still persisted on every report row, so scope is
available for auditing and for a future tightening, but they are not the
access path today.

Slice 3's routes must therefore load the run via
`council_run_repo.get_for_user(account.uid, run_id)` before serving
reports. Fetching a run by id alone and passing it here would silently
serve another user's reports.

### Known gap, for slice 3

**A partial response carries no signal that it is partial.**
`list_reports` returns `{model, content_md}` pairs, so a caller
receiving four of five cannot tell from the response alone whether the
fifth member *failed and wrote nothing* (legitimately absent — `state:
failed`, no `report` key) or *wrote a report we could not retrieve*.
Those warrant different UI.

The information is derivable client-side — the run record carries
`members[].report`, so a path present with no matching content is a
retrieval gap — but that requires the frontend to perform the join and
know what it means. Left as-is deliberately: slice 3 owns the route and
response shape, and adding a per-member status field now would be
designing for a caller that does not exist yet.

## Expected dead-code warnings

Same as slice 1: this is a layer, not a feature, so its entry points
have no production caller until slice 3. `vulture` will report
`member_reports.list_reports` / `ingest_terminal` and the repo's `store`
/ `list_for_run`. `07-dead-code.sh` is informational and exits 0. No `#
noqa`, whitelist entry, or placeholder caller has been added to silence
them — a whitelist entry would be orphan rot the moment slice 3 lands,
and `vulture_whitelist.py` is shrink-only by policy.

## Import-linter

Adding `council_report_repo.py` required all three lists in
`pyproject.toml` — C1 `ignore_imports`, C4 `modules`, C4b
`forbidden_modules`. Missing any one breaks the contract check. 8/8
contracts hold.

## Incidental

`test_lifetime` now asserts **both** council index registrations. Slice
1 asserted only the run repo.

## Verification

`ruff`, `ruff format`, `pyright` (0 errors), `lint-imports` (8/8), all
eight `scripts/ci-lint` guards, and the complete suite against a local
mongo — **7,038 passed, whole-app coverage 90.09%** against CI's 89.5%
gate.

Reproducing note: a unit-only run is *not* comparable to the CI gate —
BDD covers materially more. Run the full suite with mongo on
`127.0.0.1`.

## What has NOT been verified

**This has never run against a real bot.** Every test mocks the pod.
Specifically unverified here:

1. That `members[].report` paths resolve as expected relative to the run
directory. The real fixture uses relative paths
(`raw-reports/gpt-5.5.md`) and a **failed member omits `report`
entirely** — both are handled, neither is confirmed live.
2. What `read_bot_file`'s response envelope actually contains, and
whether FastClaw imposes its own size cap below 2 MiB.

That method has already caught four cases on this branch where code
modelled data the skill never produces. All four had passing tests.

## Test plan

- [x] Full suite green against local mongo (7,038 passed, 90.09%)
- [x] 8/8 import-linter contracts
- [x] 8/8 ci-lint guards
- [ ] CI green
- [ ] Staging: confirm a real run's member reports ingest and serve

---------

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
```

### PR body

## What this is

**Slice 2 of 3** for the `/council` backend. Adds the `ecap-council-reports` collection, its repo, and the ingest/serve service.

Like slice 1, this is **not yet reachable** — the callers (`status_poll`, `run_service`) arrive in slice 3.

| slice | contents | status |
|---|---|---|
| 1 | run record, state machine, pod file boundary | merged (#3095) |
| **2 — this PR** | raw member report persistence | here |
| 3 | runs API + status reader | next |

## Why member reports, and only member reports

The synthesized report is delivered into the Mattermost thread — durable, already rendered by the frontend — and its path travels in `artifacts.report`, so a client can build the URL itself. Storing it again would be redundant.

The **raw member reports are different.** They exist only in `$RUN/raw-reports/` on the bot pod, and the FastClaw file API requires that pod to be *running*. Pods get stopped and recreated. Without this, a user opening a run a week later finds the record intact and its content evaporated. These are the one council artifact with no other home — which is exactly what makes them worth a collection.

`anonymized.md` is deliberately not persisted either: it is a synthesis intermediate, not something a user reads.

## What to review

**One document per member report.** `{report_id, run_id, uid, org_id, model, content_md, ingested_at}`. Ownership scope lives on the row even though `run_id` is the access path. One doc *per run* would crowd the 16 MB limit and force loading every report to show one.

**Idempotent ingest.** A unique `(run_id, model)` index plus `$setOnInsert` means a re-read returns the existing row rather than rewriting it. `report_id` is bare `uuid4().hex`, matching the run-id convention.

**Nothing caps the report count** — and that is deliberate. The cast size is decided upstream by the skill: `roster.py` sets `SEATS_BY_DEPTH = {"quick": 3, "standard": 4, "deep": 5}`, and `status_schema.json` gives `members` a `minItems` with **no maximum**. A cap here could therefore only ever truncate content the user paid for, silently, and indistinguishably from working as intended. An earlier revision of this branch did cap it at 5 — matching today's `deep` seat count exactly, so it had zero headroom and would have started dropping reports the day that constant moved.

The per-file **2 MiB** read bound stays, with an ERROR log naming the model when it trips. Refusing one oversized file is not the same as quietly dropping the tail of a set.

**Ingest is best-effort and runs after the terminal write, never before it.** The run is terminal whether or not the text was captured; a failed read logs with ownership scope instead of blocking terminalisation. Each member is read in isolation so one unreadable report cannot abort the batch. This is the "local terminal write is the contract, external work happens after it" rule.

**Serving reads Mongo first**, and falls back to the pod for anything not yet ingested.

**It persists only what is final.** A terminal run's fallback read is written through — that is the repair path when best-effort `ingest_terminal` missed a report. A **mid-flight** run's read is served without being stored, because the content is still mutable: `run_status.py:576` notes "a debate round overwrites it with v2", and a `done → failed` downgrade moves the file into `raw-reports/failed/` and rewrites the path. With `$setOnInsert` the first write wins permanently, so caching mid-flight would freeze a pre-debate draft — or worse, a report the skill deliberately quarantined so nothing would consume it.

## Codex review response

**P1, Mongo-first serve failed closed — accepted and fixed** (`b0050d013`).

The finding was correct and it contradicted this PR's own premise. `list_reports` loaded stored rows first, then filled gaps from the pod with neither the reader open nor the per-member reads isolated: `pod_files.for_run` raises whenever the runtime is missing, stopped or org-mismatched, and `_read_and_store` re-raised everything except `council.pod_file_too_large`. So a run with four of five reports already in Mongo, whose pod had since been stopped or recreated, returned **503 and zero reports** — in exactly the scenario this collection exists to survive.

Codex also spotted the internal inconsistency: `ingest_terminal` already isolates per-member failures in the same module; the serve path did not.

Now a failed reader open logs at WARNING with ownership scope and serves what is stored, and each member read is isolated the same way `ingest_terminal` does.

**One case deliberately does not degrade:** nothing stored *and* the pod unreadable still raises. An empty list there would assert the run produced no reports — false, and indistinguishable from a genuinely report-less run.

**No retry job is needed.** `list_reports` recomputes the missing set on every call and persists what it fetches, so the serve path is also the repair path: a pod that was merely stopped heals on the next view, and this is the same backstop covering a failed best-effort `ingest_terminal`. A *recreated* pod is unrecoverable — that window is narrowed, not closed.

### Ownership is enforced upstream — slice 3 must not break that

`council_report_repo.list_for_run` filters on `run_id` alone; it carries no `uid`/`org_id` predicate. That is intentional and safe **as long as the caller already holds a `CouncilRun` obtained through an owner-scoped read** — possession of the run object is the authorisation.

`uid` and `org_id` are still persisted on every report row, so scope is available for auditing and for a future tightening, but they are not the access path today.

Slice 3's routes must therefore load the run via `council_run_repo.get_for_user(account.uid, run_id)` before serving reports. Fetching a run by id alone and passing it here would silently serve another user's reports.

### Known gap, for slice 3

**A partial response carries no signal that it is partial.** `list_reports` returns `{model, content_md}` pairs, so a caller receiving four of five cannot tell from the response alone whether the fifth member *failed and wrote nothing* (legitimately absent — `state: failed`, no `report` key) or *wrote a report we could not retrieve*. Those warrant different UI.

The information is derivable client-side — the run record carries `members[].report`, so a path present with no matching content is a retrieval gap — but that requires the frontend to perform the join and know what it means. Left as-is deliberately: slice 3 owns the route and response shape, and adding a per-member status field now would be designing for a caller that does not exist yet.

## Expected dead-code warnings

Same as slice 1: this is a layer, not a feature, so its entry points have no production caller until slice 3. `vulture` will report `member_reports.list_reports` / `ingest_terminal` and the repo's `store` / `list_for_run`. `07-dead-code.sh` is informational and exits 0. No `# noqa`, whitelist entry, or placeholder caller has been added to silence them — a whitelist entry would be orphan rot the moment slice 3 lands, and `vulture_whitelist.py` is shrink-only by policy.

## Import-linter

Adding `council_report_repo.py` required all three lists in `pyproject.toml` — C1 `ignore_imports`, C4 `modules`, C4b `forbidden_modules`. Missing any one breaks the contract check. 8/8 contracts hold.

## Incidental

`test_lifetime` now asserts **both** council index registrations. Slice 1 asserted only the run repo.

## Verification

`ruff`, `ruff format`, `pyright` (0 errors), `lint-imports` (8/8), all eight `scripts/ci-lint` guards, and the complete suite against a local mongo — **7,038 passed, whole-app coverage 90.09%** against CI's 89.5% gate.

Reproducing note: a unit-only run is *not* comparable to the CI gate — BDD covers materially more. Run the full suite with mongo on `127.0.0.1`.

## What has NOT been verified

**This has never run against a real bot.** Every test mocks the pod. Specifically unverified here:

1. That `members[].report` paths resolve as expected relative to the run directory. The real fixture uses relative paths (`raw-reports/gpt-5.5.md`) and a **failed member omits `report` entirely** — both are handled, neither is confirmed live.
2. What `read_bot_file`'s response envelope actually contains, and whether FastClaw imposes its own size cap below 2 MiB.

That method has already caught four cases on this branch where code modelled data the skill never produces. All four had passing tests.

## Test plan

- [x] Full suite green against local mongo (7,038 passed, 90.09%)
- [x] 8/8 import-linter contracts
- [x] 8/8 ci-lint guards
- [ ] CI green
- [ ] Staging: confirm a real run's member reports ingest and serve



---

## af759f7e9f6c82f25be7559e475a42db63f5535a
- 作者: bill-srp
- 日期: 2026-07-28T12:44:22Z
- PR: #3095

### Commit message

```
feat(council): add the council run record and pod file boundary (#3095)

## What this is

**Slice 1 of 3** for the `/council` backend in `claw-interface`. This
one adds the durable run record and the read-only boundary to the bot
pod.

**No routes are registered.** Nothing here is reachable from the API yet
— this is foundation only. The runs API and the status reader follow in
slice 3.

| slice | contents | status |
|---|---|---|
| **1 — this PR** | run record, state machine, pod file boundary | here
|
| 2 | raw member report persistence | next |
| 3 | runs API + status reader | after 2 |

Split from #3089, which was 5,329 lines and could not run CI's real jobs
— the size gate skipped them. Each slice now lands under the limit, so
`claw-interface-quality` actually executes.

## The design in one paragraph

The `council` skill (`SerendipityOneInc/ecap-skills`) runs entirely on
the user's bot pod. It casts the members, gathers evidence, blinds,
debates and synthesises, and writes `status.json` into a run folder **it
names itself**. `claw-interface` never orchestrates and never sends
anything — the frontend posts `/council {topic}` to Mattermost directly.
This service records that a run exists and reads back what the skill
wrote.

Design specs, including two rejected alternatives, are in
`docs/superpowers/specs/2026-07-28-*.md`.

## What to review

**The CAS discipline.** Every state change goes through one
`transition_state` helper: a `find_one_and_update` filtered on the
current state, returning `None` on a miss rather than reporting a write
that did not happen. Terminal states absorb — nothing lists them in
`from_states` — so a terminal write is permanent. That is deliberate,
and it is why nothing in this design terminalises a run on inference.

**The active-run cap is a soft record limit, not an admission
boundary.** `count_active()` is a plain non-atomic count, and the only
indexes are `unique_run_id` and `idx_uid_created`. There is deliberately
no slot claim, no CAS admission, and no atomic gate.

That is because the cap does not guard spend. `create_run` is a pure
database insert — this service never dispatches anything. The council
actually starts when the **frontend** posts `/council {topic}` to
Mattermost, which the backend neither performs nor gates. So cap and
money are fully decoupled, and losing a count-then-insert race costs
exactly one extra non-terminal row.

Building CAS admission on top of that would be machinery defending
nothing. An earlier revision of this branch had exactly that — numbered
`active_slot`s under a unique partial index, plus a post-insert
reconciliation pass — and both were removed once it was clear the spend
had moved to the frontend. This description previously still described
the slot mechanism after the code had dropped it; that was a
documentation error, corrected here.

If a real admission boundary is ever needed, it belongs wherever spend
is actually triggered, not in this repo layer.

**Path containment in `pod_files`.** This is the security-relevant part,
and it is worth being precise about where each boundary sits, because
there are two and they are not the same.

- `run_artifact_path()` confines a **skill-emitted** path to the pinned
run folder. An artifact path that escapes raises
`council.pod_path_invalid` rather than being read. This is the boundary
that matters, because it is the one untrusted input crosses:
`members[].report` and `artifacts.report` are strings read out of
`status.json` on the pod.
- `read()` / `list()` enforce only that the resolved path sits under
`/workspace`.

So containment is enforced **at the point untrusted input enters**, not
on every call to `read()`. Callers resolve through `run_artifact_path()`
(or `status_path()`, which wraps it) and hand the result to `read()`.

An earlier revision of this description claimed every path is confined
to the run folder. That was wrong, and Codex flagged it —
`read("/workspace/anything")` is accepted. No caller does that today, so
there is no reachable out-of-run read, but the API does not make it
impossible either.

Narrowing that surface — an explicit discovery-listing entry point plus
an artifact read that always resolves through `run_artifact_path()` — is
**deliberately deferred to slice 3**. Discovery has to list
`/workspace/council-runs` *before* any folder is pinned, so the class
cannot unconditionally confine to a run folder, and the right split
between those two operations is only observable once `status_poll`'s
real call sites exist. Designing it now would be guessing at the skill's
shape, which has already cost this branch several rewrites.

Reads are bounded at 2 MiB and typed; directory listings are validated
per entry rather than trusted as dicts.

**`resolve_bot_credentials` is a gate, not a getter.** Subscription
access, primary runtime resolution, run-org matching, and pod readiness
— all four must pass before it returns `(computer_id, app_token)`. A
stopped pod is `DependencyNotReadyError`, deliberately transient,
because it must never terminalise a run.

**Error masking.** Upstream failures become domain errors carrying
`uid`/`org_id`/`run_id` plus `upstream_service` and status in `context`,
with a masked `public_code`. FastClaw never surfaces in an API response.

## Expected dead-code warnings — read this before flagging them

Because this slice is a layer rather than a feature, several functions
land here with **no production caller until slice 3**. `vulture` reports
them:

```
app/services/council/pod_files.py:67    unused method 'read'
app/services/council/pod_files.py:123   unused function 'for_run'
app/services/council/pod_files.py:143   unused function 'status_path'
app/services/council/state_machine.py:68 unused function 'can_transition'
```

All four are called from `status_poll.py` in slice 3 — `can_transition`
at its line 320, the `pod_files` entry points throughout the refresh
path. They are covered by their own tests here (`pod_files` 97%,
`state_machine` 100%), which is exactly the "kept alive only by its own
self-test" shape issue #1503 asks vulture to surface. `07-dead-code.sh`
is informational and exits 0, so CI does not block on it.

This was a deliberate trade. A vertical split — create/list/get, then
refresh, then reports — would have no dormant code, but `pod_files` and
`status_poll` would then have to ship together and that slice lands at
~3,600 lines, over the size gate. The layer split is what keeps every PR
under the limit.

**No `# noqa`, whitelist entry, or placeholder caller has been added to
silence these.** A whitelist entry would be orphan rot the moment slice
3 lands, and `vulture_whitelist.py` is shrink-only by policy.

## Incidental fix

`test_lifetime` asserted no council index registration at all.
`council_run_repo.ensure_indexes` was running unmocked in the unit suite
and being swallowed by its own `try/except`. It is now patched and
asserted.

## Verification

Full local gate: `ruff`, `ruff format`, `pyright` (0 errors),
`lint-imports` (8/8 contracts), all eight `scripts/ci-lint` guards, and
the **complete suite against a local mongo** — 7,020 passed, whole-app
coverage **90.07%** against CI's 89.5% gate.

Note for anyone reproducing: a unit-only run reports ~89.5% and is *not*
comparable to the CI gate — BDD covers materially more. Run the full
suite with mongo on `127.0.0.1`.

## What has NOT been verified

**None of this has run against a real bot.** Every test mocks the pod.
That method already found four cases in the original branch where the
code modelled data the skill never produces — a whole `result.json`
contract, a `moderator` role the v3 pipeline removed, an `analysis` map
that is built but unwired, and report size/status fields. All four had
passing tests.

Three assumptions remain open and one staging dispatch closes them all:

1. That the skill's run folder sits under `/workspace`.
2. What `read_bot_file`'s response envelope actually contains, and
whether FastClaw caps size.
3. That `/council {topic}` triggers the skill at all.

These matter for slice 3, not this one — nothing here is callable yet.

## Codex review response

### Round 2 (current head)

**P1-1, "no active-run admission boundary" — correct observation, no
code change.** Codex is right that the persisted model has no slot field
and the indexes are only `unique_run_id` plus `idx_uid_created`, so
nothing here provides atomic admission.

It was arguing against this description, not the code. The paragraph
above previously still described a slot mechanism that had been removed,
and Codex reasonably read that as an unmet promise. Corrected.

On the substance: the count-then-insert race is real and its consequence
is one extra non-terminal row. It cannot oversubscribe spend, because
this service never dispatches — the frontend posts `/council {topic}` to
Mattermost, and the backend neither performs nor gates that. A CAS
admission boundary here would guard nothing while implying a spend
guarantee that does not exist, which is worse than the race.

**P1-2, `resolve_bot_credentials` is not scoped to the run's org —
accepted, fix incoming.** This one is a genuine defect.
`get_primary_computer(uid)` takes no `org_id` and resolves the user's
*current-org* primary; `resolve_bot_credentials` then rejects when
`computer.org_id != run.org_id`. A user who creates a council under org
A and later switches to org B gets `council.pod_unavailable` on that run
permanently — its history and reports become unreadable even though the
record stores correct provenance and org A's runtime may still exist and
still be theirs.

Picking an arbitrary runtime and failing closed afterward is backwards
when the run already records which org to look in, and
`computer_repo.list_by_user_org(uid, org_id)` already supports the
correct lookup. Fix: resolve within the run's org, plus a test that a
run whose `org_id` is not the current primary still resolves.

This is the same root as the `computer_id` gap noted below — both come
from resolving the runtime *now* rather than using what the run
recorded.

### Round 1 (addressed at head `3431102b0`)

**Active-slot retry loop.** The loop caught `DuplicateKeyError` directly
and inspected `exc.details["keyPattern"]`, bypassing the
`is_duplicate_key_error()` helper every other repo uses, and its
`continue` / `return None` lines were uncovered. Resolved by removing
the slot mechanism entirely (see the cap section above), which removes
the coupling and the untested path together.

For the record, Codex's stated mechanism there was wrong: it claimed
`mongo.create` re-raises duplicates as a plain `Exception`, citing
`_errors.py`'s docstring. favie-common v0.3.69 — pinned and installed —
calls `insert_one` with no `try/except`, so pymongo's native
`DuplicateKeyError` propagated intact. That docstring is stale and is
worth a separate cleanup.

**Pod-file confinement.** Description defect, not a code defect;
corrected above. Untrusted input (`members[].report`, `artifacts.report`
out of `status.json`) already crosses through `run_artifact_path()`, so
no out-of-run read is reachable. The API-narrowing is real and deferred
to slice 3, where discovery's `list("/workspace/council-runs")` and the
pinned artifact reads both exist and the right split is observable
rather than guessed.

## Known open item, carried to slice 3

There is **no stable correlation key** between a run record and the
skill's run folder. The skill names its own folder and has no `--run-id`
flag. Discovery by mtime plus topic is what slice 3 currently does, and
it has an unresolved failure mode with same-topic concurrent runs. The
fix is either a ~5-line `--run-id` flag in `ecap-skills` or capping
concurrent runs to one. Not blocking this PR — the record and the
boundary are correct either way.

Relatedly, a run records `org_id` but not `computer_id`, so a recreated
runtime strands an in-flight council. That will be addressed with the
correlation work.

## Test plan

- [x] Full suite green against local mongo (7,020 passed, 90.07%)
- [x] 8/8 import-linter contracts
- [x] 8/8 ci-lint guards
- [ ] CI green on this PR (first time the real jobs will run for this
work)

---------

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
```

### PR body

## What this is

**Slice 1 of 3** for the `/council` backend in `claw-interface`. This one adds the durable run record and the read-only boundary to the bot pod.

**No routes are registered.** Nothing here is reachable from the API yet — this is foundation only. The runs API and the status reader follow in slice 3.

| slice | contents | status |
|---|---|---|
| **1 — this PR** | run record, state machine, pod file boundary | here |
| 2 | raw member report persistence | next |
| 3 | runs API + status reader | after 2 |

Split from #3089, which was 5,329 lines and could not run CI's real jobs — the size gate skipped them. Each slice now lands under the limit, so `claw-interface-quality` actually executes.

## The design in one paragraph

The `council` skill (`SerendipityOneInc/ecap-skills`) runs entirely on the user's bot pod. It casts the members, gathers evidence, blinds, debates and synthesises, and writes `status.json` into a run folder **it names itself**. `claw-interface` never orchestrates and never sends anything — the frontend posts `/council {topic}` to Mattermost directly. This service records that a run exists and reads back what the skill wrote.

Design specs, including two rejected alternatives, are in `docs/superpowers/specs/2026-07-28-*.md`.

## What to review

**The CAS discipline.** Every state change goes through one `transition_state` helper: a `find_one_and_update` filtered on the current state, returning `None` on a miss rather than reporting a write that did not happen. Terminal states absorb — nothing lists them in `from_states` — so a terminal write is permanent. That is deliberate, and it is why nothing in this design terminalises a run on inference.

**The active-run cap is a soft record limit, not an admission boundary.** `count_active()` is a plain non-atomic count, and the only indexes are `unique_run_id` and `idx_uid_created`. There is deliberately no slot claim, no CAS admission, and no atomic gate.

That is because the cap does not guard spend. `create_run` is a pure database insert — this service never dispatches anything. The council actually starts when the **frontend** posts `/council {topic}` to Mattermost, which the backend neither performs nor gates. So cap and money are fully decoupled, and losing a count-then-insert race costs exactly one extra non-terminal row.

Building CAS admission on top of that would be machinery defending nothing. An earlier revision of this branch had exactly that — numbered `active_slot`s under a unique partial index, plus a post-insert reconciliation pass — and both were removed once it was clear the spend had moved to the frontend. This description previously still described the slot mechanism after the code had dropped it; that was a documentation error, corrected here.

If a real admission boundary is ever needed, it belongs wherever spend is actually triggered, not in this repo layer.

**Path containment in `pod_files`.** This is the security-relevant part, and it is worth being precise about where each boundary sits, because there are two and they are not the same.

- `run_artifact_path()` confines a **skill-emitted** path to the pinned run folder. An artifact path that escapes raises `council.pod_path_invalid` rather than being read. This is the boundary that matters, because it is the one untrusted input crosses: `members[].report` and `artifacts.report` are strings read out of `status.json` on the pod.
- `read()` / `list()` enforce only that the resolved path sits under `/workspace`.

So containment is enforced **at the point untrusted input enters**, not on every call to `read()`. Callers resolve through `run_artifact_path()` (or `status_path()`, which wraps it) and hand the result to `read()`.

An earlier revision of this description claimed every path is confined to the run folder. That was wrong, and Codex flagged it — `read("/workspace/anything")` is accepted. No caller does that today, so there is no reachable out-of-run read, but the API does not make it impossible either.

Narrowing that surface — an explicit discovery-listing entry point plus an artifact read that always resolves through `run_artifact_path()` — is **deliberately deferred to slice 3**. Discovery has to list `/workspace/council-runs` *before* any folder is pinned, so the class cannot unconditionally confine to a run folder, and the right split between those two operations is only observable once `status_poll`'s real call sites exist. Designing it now would be guessing at the skill's shape, which has already cost this branch several rewrites.

Reads are bounded at 2 MiB and typed; directory listings are validated per entry rather than trusted as dicts.

**`resolve_bot_credentials` is a gate, not a getter.** Subscription access, primary runtime resolution, run-org matching, and pod readiness — all four must pass before it returns `(computer_id, app_token)`. A stopped pod is `DependencyNotReadyError`, deliberately transient, because it must never terminalise a run.

**Error masking.** Upstream failures become domain errors carrying `uid`/`org_id`/`run_id` plus `upstream_service` and status in `context`, with a masked `public_code`. FastClaw never surfaces in an API response.

## Expected dead-code warnings — read this before flagging them

Because this slice is a layer rather than a feature, several functions land here with **no production caller until slice 3**. `vulture` reports them:

```
app/services/council/pod_files.py:67    unused method 'read'
app/services/council/pod_files.py:123   unused function 'for_run'
app/services/council/pod_files.py:143   unused function 'status_path'
app/services/council/state_machine.py:68 unused function 'can_transition'
```

All four are called from `status_poll.py` in slice 3 — `can_transition` at its line 320, the `pod_files` entry points throughout the refresh path. They are covered by their own tests here (`pod_files` 97%, `state_machine` 100%), which is exactly the "kept alive only by its own self-test" shape issue #1503 asks vulture to surface. `07-dead-code.sh` is informational and exits 0, so CI does not block on it.

This was a deliberate trade. A vertical split — create/list/get, then refresh, then reports — would have no dormant code, but `pod_files` and `status_poll` would then have to ship together and that slice lands at ~3,600 lines, over the size gate. The layer split is what keeps every PR under the limit.

**No `# noqa`, whitelist entry, or placeholder caller has been added to silence these.** A whitelist entry would be orphan rot the moment slice 3 lands, and `vulture_whitelist.py` is shrink-only by policy.

## Incidental fix

`test_lifetime` asserted no council index registration at all. `council_run_repo.ensure_indexes` was running unmocked in the unit suite and being swallowed by its own `try/except`. It is now patched and asserted.

## Verification

Full local gate: `ruff`, `ruff format`, `pyright` (0 errors), `lint-imports` (8/8 contracts), all eight `scripts/ci-lint` guards, and the **complete suite against a local mongo** — 7,020 passed, whole-app coverage **90.07%** against CI's 89.5% gate.

Note for anyone reproducing: a unit-only run reports ~89.5% and is *not* comparable to the CI gate — BDD covers materially more. Run the full suite with mongo on `127.0.0.1`.

## What has NOT been verified

**None of this has run against a real bot.** Every test mocks the pod. That method already found four cases in the original branch where the code modelled data the skill never produces — a whole `result.json` contract, a `moderator` role the v3 pipeline removed, an `analysis` map that is built but unwired, and report size/status fields. All four had passing tests.

Three assumptions remain open and one staging dispatch closes them all:

1. That the skill's run folder sits under `/workspace`.
2. What `read_bot_file`'s response envelope actually contains, and whether FastClaw caps size.
3. That `/council {topic}` triggers the skill at all.

These matter for slice 3, not this one — nothing here is callable yet.

## Codex review response

### Round 2 (current head)

**P1-1, "no active-run admission boundary" — correct observation, no code change.** Codex is right that the persisted model has no slot field and the indexes are only `unique_run_id` plus `idx_uid_created`, so nothing here provides atomic admission.

It was arguing against this description, not the code. The paragraph above previously still described a slot mechanism that had been removed, and Codex reasonably read that as an unmet promise. Corrected.

On the substance: the count-then-insert race is real and its consequence is one extra non-terminal row. It cannot oversubscribe spend, because this service never dispatches — the frontend posts `/council {topic}` to Mattermost, and the backend neither performs nor gates that. A CAS admission boundary here would guard nothing while implying a spend guarantee that does not exist, which is worse than the race.

**P1-2, `resolve_bot_credentials` is not scoped to the run's org — acknowledged, deliberately not fixed.** The observation is accurate. `get_primary_computer(uid)` takes no `org_id` and resolves the user's *current-org* primary; `resolve_bot_credentials` then rejects when `computer.org_id != run.org_id`. So a user who creates a council under org A and later switches to org B gets `council.pod_unavailable` on that run — its history and reports stay unreadable while org B is primary, even though the record holds correct provenance.

Not changing it in this PR. Recorded here as a known limitation so it is not rediscovered as a surprise: single-org accounts are unaffected, and nothing calls `resolve_bot_credentials` yet at this commit.

Same root as the `computer_id` gap noted below — both come from resolving the runtime *now* rather than from what the run recorded — so if it is ever revisited, the two belong together.

### Round 1 (addressed at head `3431102b0`)

**Active-slot retry loop.** The loop caught `DuplicateKeyError` directly and inspected `exc.details["keyPattern"]`, bypassing the `is_duplicate_key_error()` helper every other repo uses, and its `continue` / `return None` lines were uncovered. Resolved by removing the slot mechanism entirely (see the cap section above), which removes the coupling and the untested path together.

For the record, Codex's stated mechanism there was wrong: it claimed `mongo.create` re-raises duplicates as a plain `Exception`, citing `_errors.py`'s docstring. favie-common v0.3.69 — pinned and installed — calls `insert_one` with no `try/except`, so pymongo's native `DuplicateKeyError` propagated intact. That docstring is stale and is worth a separate cleanup.

**Pod-file confinement.** Description defect, not a code defect; corrected above. Untrusted input (`members[].report`, `artifacts.report` out of `status.json`) already crosses through `run_artifact_path()`, so no out-of-run read is reachable. The API-narrowing is real and deferred to slice 3, where discovery's `list("/workspace/council-runs")` and the pinned artifact reads both exist and the right split is observable rather than guessed.

## Known open item, carried to slice 3

There is **no stable correlation key** between a run record and the skill's run folder. The skill names its own folder and has no `--run-id` flag. Discovery by mtime plus topic is what slice 3 currently does, and it has an unresolved failure mode with same-topic concurrent runs. The fix is either a ~5-line `--run-id` flag in `ecap-skills` or capping concurrent runs to one. Not blocking this PR — the record and the boundary are correct either way.

Relatedly, a run records `org_id` but not `computer_id`, so a recreated runtime strands an in-flight council. That will be addressed with the correlation work.

## Test plan

- [x] Full suite green against local mongo (7,020 passed, 90.07%)
- [x] 8/8 import-linter contracts
- [x] 8/8 ci-lint guards
- [ ] CI green on this PR (first time the real jobs will run for this work)



---

## 34f0a2c711fb929414e0c102efc17039b56a9bb0
- 作者: rayrain-srp
- 日期: 2026-07-28T12:43:15Z
- PR: #3085

### Commit message

```
fix(auth): route token verification through internal account service (#3085)

## Summary
- add a dedicated `ACCOUNT_SERVICE_URL` for `claw-interface` server-side
JWT verification
- use the internal URL when configured, and use
`NEXT_PUBLIC_ACCOUNT_URL` only when the new setting is unset
- intentionally fail closed on internal transport errors instead of
silently re-entering the public Cloudflare path
- validate the new URL at startup and cover precedence/configuration
fallback behavior with unit tests

## Root cause
`claw-interface` currently verifies JWTs through the public
account-service hostname, sending an in-cluster request through the
external Cloudflare/load-balancer path. Production logs continue to show
intermittent `ConnectTimeout` failures on this call.

Replacing `NEXT_PUBLIC_ACCOUNT_URL` directly is unsafe because that
value is also propagated to OpenClaw bot workloads as
`AGENT_IDENTITY_API_BASE`; those pods run in a separate cluster and
cannot resolve the SRP cluster's `*.svc.cluster.local` DNS name.

This change separates the server-side verification endpoint so staging
can set:

`ACCOUNT_SERVICE_URL=http://user-interface.favie.svc.cluster.local`

while keeping the public URL unchanged for browser and cross-cluster
consumers.

Linear: https://linear.app/srpone/issue/ECA-1185

## User impact
Reduces intermittent account/session verification failures caused by
public Cloudflare hairpinning without changing browser-facing or
bot-facing account URLs.

## Test plan
- [x] auth and startup URL unit-test files (`51 passed`)
- [x] public-URL fallback test with an external `ACCOUNT_SERVICE_URL`
environment value
- [x] fail-closed contract test proves internal transport errors never
call the public URL
- [x] full `bash scripts/verify-py.sh`
- [x] pre-commit and pre-push repository hooks
- [x] in-cluster `/auth/verify` connectivity checked in staging and
production
- [ ] deploy to staging, add `ACCOUNT_SERVICE_URL` in Vault, restart
`claw-interface`, and monitor `Auth service unreachable`

## Rollout note
This PR only adds the safe configuration seam. It does not change the
live endpoint by itself; the Vault value above must be added to staging
before the internal route is exercised.

Once `ACCOUNT_SERVICE_URL` is set, transport failures intentionally fail
closed and do not retry through `NEXT_PUBLIC_ACCOUNT_URL`. This prevents
the auth path from silently returning to the public Cloudflare route.
Rollback is performed by removing the new Vault value and restarting
`claw-interface`.
```

### PR body

## Summary
- add a dedicated `ACCOUNT_SERVICE_URL` for `claw-interface` server-side JWT verification
- use the internal URL when configured, and use `NEXT_PUBLIC_ACCOUNT_URL` only when the new setting is unset
- intentionally fail closed on internal transport errors instead of silently re-entering the public Cloudflare path
- validate the new URL at startup and cover precedence/configuration fallback behavior with unit tests

## Root cause
`claw-interface` currently verifies JWTs through the public account-service hostname, sending an in-cluster request through the external Cloudflare/load-balancer path. Production logs continue to show intermittent `ConnectTimeout` failures on this call.

Replacing `NEXT_PUBLIC_ACCOUNT_URL` directly is unsafe because that value is also propagated to OpenClaw bot workloads as `AGENT_IDENTITY_API_BASE`; those pods run in a separate cluster and cannot resolve the SRP cluster's `*.svc.cluster.local` DNS name.

This change separates the server-side verification endpoint so staging can set:

`ACCOUNT_SERVICE_URL=http://user-interface.favie.svc.cluster.local`

while keeping the public URL unchanged for browser and cross-cluster consumers.

Linear: https://linear.app/srpone/issue/ECA-1185

## User impact
Reduces intermittent account/session verification failures caused by public Cloudflare hairpinning without changing browser-facing or bot-facing account URLs.

## Test plan
- [x] auth and startup URL unit-test files (`51 passed`)
- [x] public-URL fallback test with an external `ACCOUNT_SERVICE_URL` environment value
- [x] fail-closed contract test proves internal transport errors never call the public URL
- [x] full `bash scripts/verify-py.sh`
- [x] pre-commit and pre-push repository hooks
- [x] in-cluster `/auth/verify` connectivity checked in staging and production
- [ ] deploy to staging, add `ACCOUNT_SERVICE_URL` in Vault, restart `claw-interface`, and monitor `Auth service unreachable`

## Rollout note
This PR only adds the safe configuration seam. It does not change the live endpoint by itself; the Vault value above must be added to staging before the internal route is exercised.

Once `ACCOUNT_SERVICE_URL` is set, transport failures intentionally fail closed and do not retry through `NEXT_PUBLIC_ACCOUNT_URL`. This prevents the auth path from silently returning to the public Cloudflare route. Rollback is performed by removing the new Vault value and restarting `claw-interface`.



---

## 33455a02f6740ed688397f414f27f90b1e7b8b8b
- 作者: lynn Zhuang
- 日期: 2026-07-28T11:02:13Z
- PR: #3090

### Commit message

```
style(navigation): unify panel header surfaces (#3090)

## Summary
- remove the top divider from the sidebar brand row and the shared page
header
- let the shared page header inherit its panel background for a unified
surface across themes and workspace skins

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/components/PageHeader.tsx
web/app/src/components/sidenav/SideNavLogo.tsx`
- [x] `bash scripts/verify-changed.sh`
- [x] visually verified the chat and Agent Marketplace headers with the
local mock stack

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
```

### PR body

## Summary
- remove the top divider from the sidebar brand row and the shared page header
- let the shared page header inherit its panel background for a unified surface across themes and workspace skins

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/components/PageHeader.tsx web/app/src/components/sidenav/SideNavLogo.tsx`
- [x] `bash scripts/verify-changed.sh`
- [x] visually verified the chat and Agent Marketplace headers with the local mock stack



---

## 19f5d63ece1f7f4a3566447dfd3b2108188181ca
- 作者: kyle-srp
- 日期: 2026-07-28T07:00:12Z
- PR: #3086

### Commit message

```
feat(knowledge-base): collaborator read-only library browsing + editor→collaborator rename (#3086)

## What

Front-to-back so a knowledge-base library's **owner** or an active
**editor** grantee ("collaborator") can browse a shared library's files,
plus renames the user-facing "editor" role to "collaborator" and
discloses the re-share reach at grant time. Plan clauses **C11–C21**;
workspace spec: `docs/superpowers/specs/2026-07-28-kb-collaborator.md`.

## Pieces

- **BFF** (`services/claw-interface`): `GET
/knowledge-base/kbs/{kb_id}/documents` — transparent passthrough to
ecap-proxy-service (owner/editor authz lives upstream). GET-only,
mirrors `list_grants`.
- **web client**: `listKbDocuments(kbId, signal?)` via
`callClawInterfaceAPI` (generic claw proxy — no dedicated web BFF route,
per the passthrough-first convention).
- **web view**: new `SharedLibraryDocuments` — React Query fetch →
read-only `DocumentList` (loading / empty / error). Wired into
`KnowledgeBaseClient`: selecting a shared library swaps in this view
(the library's files live in its owning org and never appear in the
caller's org-scoped `/documents` list).
- **read-only affordance**: `DocumentList.onDelete` is now optional; a
read-only view passes no handler, so no delete control renders (even if
a doc arrives without `is_owner`).
- **i18n**: "editor/编辑者" → "collaborator/协作者" (values only; wire
`grant_type`/`role` stay `editor`, zero migration) + `reshareNotice`
disclosure in `GrantsPanel`.

Pack/installer edge rendering + stop-sharing (C19–C21) already existed
in `GrantsPanel` and were left untouched.

## Tests

Clause-keyed unit tests: BFF passthrough + registration; client
URL/signal; `SharedLibraryDocuments` C13–C15 (incl. read-only with
`is_owner` missing, library naming); `KnowledgeBaseClient`
shared-selection wiring (renders the collaborator view, drops the org
filter, threads `library`). kb frontend suite green (90), BFF green (2),
tsc + eslint clean.

## Depends on / deploy order (REQUIRED)

The shared-library browse chain is web → claw-interface
`/kbs/{kb_id}/documents` → ecap-proxy-service `/kbs/{kb_id}/documents`.
These three surfaces deploy independently, and the route only exists
once claw-interface + proxy ship, so:

**Required deploy order: ecap-proxy-service (#166) → claw-interface →
web.**

If web ships first, selecting a shared library shows a non-fatal error
state until claw-interface/proxy catch up. A 404 is intentionally
**not** degraded to an "empty" state on the client — the proxy
legitimately 404s a revoked/deleted/unknown library, which status alone
can't distinguish from a not-yet-deployed route (codex P1). The i18n
rename has no backend dependency. Other locales fall back to English for
new keys. No data migration.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What

Front-to-back so a knowledge-base library's **owner** or an active **editor** grantee ("collaborator") can browse a shared library's files, plus renames the user-facing "editor" role to "collaborator" and discloses the re-share reach at grant time. Plan clauses **C11–C21**; workspace spec: `docs/superpowers/specs/2026-07-28-kb-collaborator.md`.

## Pieces

- **BFF** (`services/claw-interface`): `GET /knowledge-base/kbs/{kb_id}/documents` — transparent passthrough to ecap-proxy-service (owner/editor authz lives upstream). GET-only, mirrors `list_grants`.
- **web client**: `listKbDocuments(kbId, signal?)` via `callClawInterfaceAPI` (generic claw proxy — no dedicated web BFF route, per the passthrough-first convention).
- **web view**: new `SharedLibraryDocuments` — React Query fetch → read-only `DocumentList` (loading / empty / error). Wired into `KnowledgeBaseClient`: selecting a shared library swaps in this view (the library's files live in its owning org and never appear in the caller's org-scoped `/documents` list).
- **read-only affordance**: `DocumentList.onDelete` is now optional; a read-only view passes no handler, so no delete control renders (even if a doc arrives without `is_owner`).
- **i18n**: "editor/编辑者" → "collaborator/协作者" (values only; wire `grant_type`/`role` stay `editor`, zero migration) + `reshareNotice` disclosure in `GrantsPanel`.

Pack/installer edge rendering + stop-sharing (C19–C21) already existed in `GrantsPanel` and were left untouched.

## Tests

Clause-keyed unit tests: BFF passthrough + registration; client URL/signal; `SharedLibraryDocuments` C13–C15 (incl. read-only with `is_owner` missing, library naming); `KnowledgeBaseClient` shared-selection wiring (renders the collaborator view, drops the org filter, threads `library`). kb frontend suite green (90), BFF green (2), tsc + eslint clean.

## Depends on / deploy order (REQUIRED)

The shared-library browse chain is web → claw-interface `/kbs/{kb_id}/documents` → ecap-proxy-service `/kbs/{kb_id}/documents`. These three surfaces deploy independently, and the route only exists once claw-interface + proxy ship, so:

**Required deploy order: ecap-proxy-service (#166) → claw-interface → web.**

If web ships first, selecting a shared library shows a non-fatal error state until claw-interface/proxy catch up. A 404 is intentionally **not** degraded to an "empty" state on the client — the proxy legitimately 404s a revoked/deleted/unknown library, which status alone can't distinguish from a not-yet-deployed route (codex P1). The i18n rename has no backend dependency. Other locales fall back to English for new keys. No data migration.

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## b25dad3c4689196480f68db1e066489e6cbd7ef2
- 作者: lynn Zhuang
- 日期: 2026-07-28T03:20:01Z
- PR: #3083

### Commit message

```
refactor(navigation): 优化模块入口与页面位置 (#3083)

## 关联事项

暂无关联 Linear 工单。

## 变更说明

- 调整侧边栏模块入口，将 Plugins 和 Channel 作为独立入口展示。
- 将 Connector、Skills、Knowledge Base 统一归入 Plugins 页面，并保留旧路由的兼容跳转。
- 将原有 IM Channel 管理内容移动到独立的 Channel 页面，保留既有配置流程。
- 将 Specialist Hub 的入口与页面文案调整为 Agent Marketplace，并整理目录、自定义专家及排序视图。
- 统一 Plugins、Channel 与现有应用壳的左右圆角面板结构。
- 为 Plugins 补充共享顶部 Header 与实时 Claw 连接状态。
- 使用 ZooClaw Design System 的默认 Tabs 规范化 Plugins 的模块切换样式。

### 变更定位

本 PR 不新增独立业务能力，主要对已有模块的入口、归属位置、路由组织和页面结构进行优化，降低侧边栏层级和信息架构的理解成本。

### 体量说明

PR 超过默认变更行数预算，主要来自 Skills、Knowledge Base、Channel
现有组件的路径迁移、零行重命名和引用路径调整。实际业务范围仍集中在模块入口与页面位置优化，因此使用 `size-override` 标签。

## 验证

- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/verify-web.sh`：TypeScript、ESLint、治理检查以及 541 个测试文件 /
7,284 个通过测试
- [x] `web/packages/zooclaw-design-system` 执行 `pnpm test`：53 个测试文件 / 299
个通过测试
- [x] 本地 mock 预览 `/plugins`：顶部 Header、Claw 状态、标准 Tabs 和左右圆角面板
- [x] GitHub CI：47/47 通过

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
```

### PR body

## 关联事项

暂无关联 Linear 工单。

## 变更说明

- 调整侧边栏模块入口，将 Plugins 和 Channel 作为独立入口展示。
- 将 Connector、Skills、Knowledge Base 统一归入 Plugins 页面，并保留旧路由的兼容跳转。
- 将原有 IM Channel 管理内容移动到独立的 Channel 页面，保留既有配置流程。
- 将 Specialist Hub 的入口与页面文案调整为 Agent Marketplace，并整理目录、自定义专家及排序视图。
- 统一 Plugins、Channel 与现有应用壳的左右圆角面板结构。
- 为 Plugins 补充共享顶部 Header 与实时 Claw 连接状态。
- 使用 ZooClaw Design System 的默认 Tabs 规范化 Plugins 的模块切换样式。

### 变更定位

本 PR 不新增独立业务能力，主要对已有模块的入口、归属位置、路由组织和页面结构进行优化，降低侧边栏层级和信息架构的理解成本。

### 体量说明

PR 超过默认变更行数预算，主要来自 Skills、Knowledge Base、Channel 现有组件的路径迁移、零行重命名和引用路径调整。实际业务范围仍集中在模块入口与页面位置优化，因此使用 `size-override` 标签。

## 验证

- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/verify-web.sh`：TypeScript、ESLint、治理检查以及 541 个测试文件 / 7,284 个通过测试
- [x] `web/packages/zooclaw-design-system` 执行 `pnpm test`：53 个测试文件 / 299 个通过测试
- [x] 本地 mock 预览 `/plugins`：顶部 Header、Claw 状态、标准 Tabs 和左右圆角面板
- [x] GitHub CI：47/47 通过



---
