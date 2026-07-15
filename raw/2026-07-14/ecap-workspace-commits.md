# ecap-workspace commits — 2026-07-14

## refactor(chat-ui): extract reusable chat composer (#2878)
- sha: `39342135a8665b172ffcb1f5e3d287660e884086`
- 作者: bill-srp
- 日期: 2026-07-14T13:19:01Z
- PR: #2878 by bill-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2878

**Commit message:**

```
refactor(chat-ui): extract reusable chat composer (#2878)

## Summary
- extract the complete controlled chat composer and rich-text editor
into `@zooclaw/chat-ui`, organized into composer, primitive, thread, and
shell layers
- migrate Main Chat, New Chat, Subagent Chat, and the enterprise demo to
the shared composer while keeping Mattermost, R2, draft, routing, and
query state in their applications
- preserve Main Chat attachment thumbnails, quote/status/banner
presentation, send/stop variants, and make the package own the hidden
file picker behind typed render props
- replace the migrated markdown media regex with a linear cursor parser
after CodeQL identified polynomial backtracking on malformed input
- restore native-textarea accessibility semantics on the shared
rich-text editor and map every composer variant to application
dark/light theme tokens
- share a linear composer-media counter across Main Chat and Subagent
upload flows, removing the remaining duplicate backtracking regexes

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm --dir web/packages/chat-ui tsc`
- [x] `pnpm --dir web/packages/chat-ui test` — 135 tests
- [x] `pnpm --dir web/packages/chat-ui lint`
- [x] focused `verify-web.sh` for Main Chat, New Chat, Subagent Chat,
and their adapters — 138 tests
- [x] focused `verify-web.sh` for the shared media counter and both
upload consumers — 114 tests
- [x] `pnpm --dir web/enterprise-app tsc`
- [x] `pnpm --dir web/enterprise-app lint` — 0 errors; existing
workspace warnings remain
- [x] local mock-browser visual checks for Main Chat/New Chat composer
parity and attachment thumbnails

## Size override
- The local size gate reports 3,305 lines against the 3,000-line default
after exclusions.
- Most of the excess is package contract coverage (646 lines), moved
editor/composer code, and deletion of the obsolete app-local
implementations; splitting would leave an unusable intermediate package
boundary.
```

**PR body:**

## Summary
- extract the complete controlled chat composer and rich-text editor into `@zooclaw/chat-ui`, organized into composer, primitive, thread, and shell layers
- migrate Main Chat, New Chat, Subagent Chat, and the enterprise demo to the shared composer while keeping Mattermost, R2, draft, routing, and query state in their applications
- preserve Main Chat attachment thumbnails, quote/status/banner presentation, send/stop variants, and make the package own the hidden file picker behind typed render props
- replace the migrated markdown media regex with a linear cursor parser after CodeQL identified polynomial backtracking on malformed input
- restore native-textarea accessibility semantics on the shared rich-text editor and map every composer variant to application dark/light theme tokens
- share a linear composer-media counter across Main Chat and Subagent upload flows, removing the remaining duplicate backtracking regexes

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm --dir web/packages/chat-ui tsc`
- [x] `pnpm --dir web/packages/chat-ui test` — 135 tests
- [x] `pnpm --dir web/packages/chat-ui lint`
- [x] focused `verify-web.sh` for Main Chat, New Chat, Subagent Chat, and their adapters — 138 tests
- [x] focused `verify-web.sh` for the shared media counter and both upload consumers — 114 tests
- [x] `pnpm --dir web/enterprise-app tsc`
- [x] `pnpm --dir web/enterprise-app lint` — 0 errors; existing workspace warnings remain
- [x] local mock-browser visual checks for Main Chat/New Chat composer parity and attachment thumbnails

## Size override
- The local size gate reports 3,305 lines against the 3,000-line default after exclusions.
- Most of the excess is package contract coverage (646 lines), moved editor/composer code, and deletion of the obsolete app-local implementations; splitting would leave an unusable intermediate package boundary.


---

## fix(agent-packs): authorize shared pack downloads (#2877)
- sha: `62985823a6a92a46db7c3d9dbe122da193e1dd2c`
- 作者: bill-srp
- 日期: 2026-07-14T12:25:13Z
- PR: #2877 by bill-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2877

**Commit message:**

```
fix(agent-packs): authorize shared pack downloads (#2877)

## Summary
- add authenticated `POST /agent-packs/validate-asset-access` as the
centralized Agent Pack R2 read-authorization boundary
- allow current-org reads and active shared-pack cross-org reads only
when the requested key matches the pack's current `asset_id`
- configure production and staging R2 Workers to call the new endpoint
for every protected `GET`/`HEAD`, including `zooclaw` reads

## Root cause
Claw-interface exposed flag-shared packs, but the R2 access worker still
authorized downloads through `/account/me` and required the caller's
current org to match the object's org prefix. Cross-org shared packs
therefore passed the catalog/share checks and were still rejected at
archive download time.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] focused claw-interface tests: 41 passed
- [x] `pnpm --dir services/r2-access-worker test`: 34 passed
- [x] `pnpm --dir services/r2-access-worker exec tsc --noEmit`

## Deployment note
Deploy claw-interface before the R2 access worker so the configured
authorization endpoint exists when Worker traffic switches over.
```

**PR body:**

## Summary
- add authenticated `POST /agent-packs/validate-asset-access` as the centralized Agent Pack R2 read-authorization boundary
- allow current-org reads and active shared-pack cross-org reads only when the requested key matches the pack's current `asset_id`
- configure production and staging R2 Workers to call the new endpoint for every protected `GET`/`HEAD`, including `zooclaw` reads

## Root cause
Claw-interface exposed flag-shared packs, but the R2 access worker still authorized downloads through `/account/me` and required the caller's current org to match the object's org prefix. Cross-org shared packs therefore passed the catalog/share checks and were still rejected at archive download time.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] focused claw-interface tests: 41 passed
- [x] `pnpm --dir services/r2-access-worker test`: 34 passed
- [x] `pnpm --dir services/r2-access-worker exec tsc --noEmit`

## Deployment note
Deploy claw-interface before the R2 access worker so the configured authorization endpoint exists when Worker traffic switches over.


---

## feat(kb-sharing): accept JSON + Markdown uploads (#2869)
- sha: `4fc853188c01a1638b7831837fafb82177f54d7c`
- 作者: kyle-srp
- 日期: 2026-07-14T09:21:45Z
- PR: #2869 by kyle-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2869

**Commit message:**

```
feat(kb-sharing): accept JSON + Markdown uploads (#2869)

## ⚠️ RELEASE GATE — deploy proxy first

**SerendipityOneInc/ecap-proxy-service#153 (backend allowlist) MUST be
deployed to the target environment BEFORE this PR.** (codex P1,
accepted.)

This PR advertises `.json`/`.md`/`.markdown` in the file picker; an old
proxy without the paired allowlist rejects them. Worst case is a
**failed upload with a server error** (no corruption, no crash — the
intended soft-validation degradation, per claude-review). Still, deploy
proxy first so users are never offered a type the backend rejects.

Staging order: merge proxy #153 → beta tag → rollout → then merge this.

## What

Accept **JSON** + **Markdown** uploads (+ the `.htm` alias the backend
already accepted).

## Why

Vertex AI Search indexes TXT, **JSON**, **Markdown**, PDF, HTML, DOCX,
PPTX, XLSX, XLSM ([Google
docs](https://docs.cloud.google.com/generative-ai-app-builder/docs/prepare-data));
the allowlist omitted JSON + Markdown. Not added: MP4/video, audio,
standalone images, legacy binary Office (`.doc`/`.ppt`/`.xls`) — Vertex
doesn't index those.

## Design

Single source of truth `CANONICAL_FORMATS` (one entry per format: label
+ extension aliases). `ALLOWED_EXTENSIONS` (validation + picker
`accept`) and the dropzone hint both derive from it — they can't drift
(claude-review note addressed).

## Tests (TDD)

accepts json/md/markdown/htm (case-insensitive) · rejects mp4/doc/png ·
hint dedupes aliases · accept list includes aliases.

## Pairs with

ecap-proxy-service#153.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

**PR body:**

## ⚠️ RELEASE GATE — deploy proxy first

**SerendipityOneInc/ecap-proxy-service#153 (backend allowlist) MUST be deployed to the target environment BEFORE this PR.** (codex P1, accepted.)

This PR advertises `.json`/`.md`/`.markdown` in the file picker; an old proxy without the paired allowlist rejects them. Worst case is a **failed upload with a server error** (no corruption, no crash — the intended soft-validation degradation, per claude-review). Still, deploy proxy first so users are never offered a type the backend rejects.

Staging order: merge proxy #153 → beta tag → rollout → then merge this.

## What

Accept **JSON** + **Markdown** uploads (+ the `.htm` alias the backend already accepted).

## Why

Vertex AI Search indexes TXT, **JSON**, **Markdown**, PDF, HTML, DOCX, PPTX, XLSX, XLSM ([Google docs](https://docs.cloud.google.com/generative-ai-app-builder/docs/prepare-data)); the allowlist omitted JSON + Markdown. Not added: MP4/video, audio, standalone images, legacy binary Office (`.doc`/`.ppt`/`.xls`) — Vertex doesn't index those.

## Design

Single source of truth `CANONICAL_FORMATS` (one entry per format: label + extension aliases). `ALLOWED_EXTENSIONS` (validation + picker `accept`) and the dropzone hint both derive from it — they can't drift (claude-review note addressed).

## Tests (TDD)

accepts json/md/markdown/htm (case-insensitive) · rejects mp4/doc/png · hint dedupes aliases · accept list includes aliases.

## Pairs with

ecap-proxy-service#153.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(agent-builder): support custom default model (#2866)
- sha: `ad84792d6ac87abfd97545778f16f7797786df24`
- 作者: kaka-srp
- 日期: 2026-07-14T09:19:06Z
- PR: #2866 by kaka-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2866

**Commit message:**

```
feat(agent-builder): support custom default model (#2866)

## Linear


https://linear.app/srpone/issue/ECA-1216/agent-builder-%E9%BB%98%E8%AE%A4%E6%A8%A1%E5%9E%8B%E9%80%89%E6%8B%A9%E8%B0%83%E6%95%B4

## Summary

- Add a Submit confirmation dialog that lets Agent Builder users keep
the platform default or choose from the same available chat-model
catalog.
- Preserve omitted, explicit null, and concrete model semantics through
Pack submission and auto-approval.
- Fail closed when a concrete model cannot be verified, while keeping
platform-default submission and existing-submission recovery available.
- Keep retry and concurrent-submit behavior idempotent; Sonnet 5 rollout
and billing discounts remain out of scope.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] `pytest -q tests/unit/test_plan_models.py
tests/unit/test_agent_builder_routes.py
tests/unit/test_agent_builder_service.py` (176 passed)
- [x] `bash scripts/verify-web.sh --no-test <changed Agent Builder
paths>`
- [x] Agent Builder frontend unit selection (85 passed)
- [x] Manual local submit persisted `openai/glm-5.2` through submission,
Pack, and install state
```

**PR body:**

## Linear

https://linear.app/srpone/issue/ECA-1216/agent-builder-%E9%BB%98%E8%AE%A4%E6%A8%A1%E5%9E%8B%E9%80%89%E6%8B%A9%E8%B0%83%E6%95%B4

## Summary

- Add a Submit confirmation dialog that lets Agent Builder users keep the platform default or choose from the same available chat-model catalog.
- Preserve omitted, explicit null, and concrete model semantics through Pack submission and auto-approval.
- Fail closed when a concrete model cannot be verified, while keeping platform-default submission and existing-submission recovery available.
- Keep retry and concurrent-submit behavior idempotent; Sonnet 5 rollout and billing discounts remain out of scope.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] `pytest -q tests/unit/test_plan_models.py tests/unit/test_agent_builder_routes.py tests/unit/test_agent_builder_service.py` (176 passed)
- [x] `bash scripts/verify-web.sh --no-test <changed Agent Builder paths>`
- [x] Agent Builder frontend unit selection (85 passed)
- [x] Manual local submit persisted `openai/glm-5.2` through submission, Pack, and install state


---

## fix(kb-sharing): send grantee_uid on editor revoke (root-cause, no edge exemption) (#2868)
- sha: `7c575b12cdd7cfb3f75e0238a410b4c38f2b281e`
- 作者: kyle-srp
- 日期: 2026-07-14T08:35:10Z
- PR: #2868 by kyle-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2868

**Commit message:**

```
fix(kb-sharing): send grantee_uid on editor revoke (root-cause, no edge exemption) (#2868)

## ⚠️ RELEASE GATE — deploy proxy first

**SerendipityOneInc/ecap-proxy-service#152 MUST be deployed to the
target environment BEFORE this PR is merged/deployed there.** (codex P1,
accepted.)

There is no code shim that makes web-first safe: the edge IDOR guard
only skips when the body has **no** `uid`, while an old proxy
(`extra="forbid"`, `uid` only) rejects any body **without** `uid` — the
same field can't be both present and absent. So the ordering is a hard,
one-directional gate:
- proxy #152 first → accepts `grantee_uid` (and `uid` alias) → web-then
works ✓
- web first, old proxy → `grantee_uid` is an unknown field → 422 ✗

(Not a regression of a working feature: revoke is currently broken at
the edge with a 403; web-first would merely change that failure to a
422. Still — deploy proxy first.)

Staging order: merge proxy #152 → beta tag → rollout → then merge this.

## What

Editor-revoke body now sends `grantee_uid` (was `uid`).

## Why (root-cause fix)

The revoke body's `uid` was the **grantee being revoked**, not the
caller — but the edge IDOR guard reads a body `uid` as caller
self-identification and 403'd every editor revoke before it reached the
backend. A body with no `uid` field is skipped by the guard, so renaming
to `grantee_uid` fixes revoke with **zero middleware special-casing**.
Supersedes #2867 (pattern-exemption), now closed. Pack-share revoke
(`source`) unaffected.

## Pairs with

ecap-proxy-service#152 — accepts `grantee_uid`, keeps `uid` as a
deprecated alias.

## Tests

GrantsPanel editor-revoke asserts the `grantee_uid` body. verify-web
green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

**PR body:**

## ⚠️ RELEASE GATE — deploy proxy first

**SerendipityOneInc/ecap-proxy-service#152 MUST be deployed to the target environment BEFORE this PR is merged/deployed there.** (codex P1, accepted.)

There is no code shim that makes web-first safe: the edge IDOR guard only skips when the body has **no** `uid`, while an old proxy (`extra="forbid"`, `uid` only) rejects any body **without** `uid` — the same field can't be both present and absent. So the ordering is a hard, one-directional gate:
- proxy #152 first → accepts `grantee_uid` (and `uid` alias) → web-then works ✓
- web first, old proxy → `grantee_uid` is an unknown field → 422 ✗

(Not a regression of a working feature: revoke is currently broken at the edge with a 403; web-first would merely change that failure to a 422. Still — deploy proxy first.)

Staging order: merge proxy #152 → beta tag → rollout → then merge this.

## What

Editor-revoke body now sends `grantee_uid` (was `uid`).

## Why (root-cause fix)

The revoke body's `uid` was the **grantee being revoked**, not the caller — but the edge IDOR guard reads a body `uid` as caller self-identification and 403'd every editor revoke before it reached the backend. A body with no `uid` field is skipped by the guard, so renaming to `grantee_uid` fixes revoke with **zero middleware special-casing**. Supersedes #2867 (pattern-exemption), now closed. Pack-share revoke (`source`) unaffected.

## Pairs with

ecap-proxy-service#152 — accepts `grantee_uid`, keeps `uid` as a deprecated alias.

## Tests

GrantsPanel editor-revoke asserts the `grantee_uid` body. verify-web green.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(claw-interface): default chats to Claude Sonnet 5 (#2853)
- sha: `845b48156bda491a784e72fcea6a0e99fa135619`
- 作者: rayrain-srp
- 日期: 2026-07-14T08:26:38Z
- PR: #2853 by rayrain-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2853

**Commit message:**

```
feat(claw-interface): default chats to Claude Sonnet 5 (#2853)

## Linear

https://linear.app/srpone/issue/ECA-1232/

## Summary

- make `claude-sonnet-5` the default chat model for Free, Starter, Pro,
Ultra, empty, and unknown plans
- keep the OpenClaw primary model derived from the baseline plan as
`openai/claude-sonnet-5`
- add the Sonnet 5 chat degradation mapping while retaining Sonnet 4.6
support
- lock new-bot creation and missing-model repair behavior with focused
tests

## Release ordering

Blocked by https://github.com/SerendipityOneInc/gcp-foundation/pull/454.
Merge, deploy, and verify the FastClaw runtime registration first; only
then deploy this product-default change. Use the same order in staging
and production.

## Scope note

This rotates defaults for new bots and the existing
missing-`model.primary` repair path. It intentionally does not migrate
bots that already have an explicit primary model or overwrite a user's
current selection in the settings route. Model availability in settings
remains governed by the dynamic plan access groups.

## Test plan

- [x] Verify TDD RED against the old defaults, then GREEN after the
minimal product change
- [x] Run all three affected unit-test files (`217 passed`)
- [x] Run `bash scripts/verify-py.sh` (Ruff, format, Pyright,
import-linter)
- [x] Run `git diff --check` and verify only the four intended files
changed
- [ ] After the infrastructure rollout, create a staging bot and verify
text and image requests
- [ ] Repeat the ordered rollout and smoke test in production
```

**PR body:**

## Linear

https://linear.app/srpone/issue/ECA-1232/

## Summary

- make `claude-sonnet-5` the default chat model for Free, Starter, Pro, Ultra, empty, and unknown plans
- keep the OpenClaw primary model derived from the baseline plan as `openai/claude-sonnet-5`
- add the Sonnet 5 chat degradation mapping while retaining Sonnet 4.6 support
- lock new-bot creation and missing-model repair behavior with focused tests

## Release ordering

Blocked by https://github.com/SerendipityOneInc/gcp-foundation/pull/454. Merge, deploy, and verify the FastClaw runtime registration first; only then deploy this product-default change. Use the same order in staging and production.

## Scope note

This rotates defaults for new bots and the existing missing-`model.primary` repair path. It intentionally does not migrate bots that already have an explicit primary model or overwrite a user's current selection in the settings route. Model availability in settings remains governed by the dynamic plan access groups.

## Test plan

- [x] Verify TDD RED against the old defaults, then GREEN after the minimal product change
- [x] Run all three affected unit-test files (`217 passed`)
- [x] Run `bash scripts/verify-py.sh` (Ruff, format, Pyright, import-linter)
- [x] Run `git diff --check` and verify only the four intended files changed
- [ ] After the infrastructure rollout, create a staging bot and verify text and image requests
- [ ] Repeat the ordered rollout and smoke test in production

---

## feat(web): hide composer for unresolved interactive cards (#2864)
- sha: `05f69a08ea33e48d7a202a2abdd2b19b9b97e3a4`
- 作者: bill-srp
- 日期: 2026-07-14T07:46:40Z
- PR: #2864 by bill-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2864

**Commit message:**

```
feat(web): hide composer for unresolved interactive cards (#2864)

## Linear

N/A

## Summary

- hide the main chat composer while an assistant Mattermost card still
exposes button or select actions
- derive the lock from the server-backed message lifecycle so the
composer returns when the post becomes a completion banner
- keep the change scoped to the Mattermost-backed main chat; gateway
subagent messages do not carry interactive attachments

## Test plan

- [x] `bash scripts/verify-web.sh <changed paths>`
- [x] `bash scripts/verify-changed.sh`
- [x] TDD red/green coverage for main chat, button/select cards, and
completion banners
```

**PR body:**

## Linear

N/A

## Summary

- hide the main chat composer while an assistant Mattermost card still exposes button or select actions
- derive the lock from the server-backed message lifecycle so the composer returns when the post becomes a completion banner
- keep the change scoped to the Mattermost-backed main chat; gateway subagent messages do not carry interactive attachments

## Test plan

- [x] `bash scripts/verify-web.sh <changed paths>`
- [x] `bash scripts/verify-changed.sh`
- [x] TDD red/green coverage for main chat, button/select cards, and completion banners


---

## feat(kb-sharing): one-click copy of the selected library id (#2861)
- sha: `deef7551a0c347cddad1184fff5464f0d3183a8b`
- 作者: kyle-srp
- 日期: 2026-07-14T07:39:15Z
- PR: #2861 by kyle-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2861

**Commit message:**

```
feat(kb-sharing): one-click copy of the selected library id (#2861)

## What

A ghost clipboard button next to the Library selector copies the
selected library's raw `kb_id`, with success/failure toasts (en/zh).

## Why

Declaring `kb_ref: { "kb_id": ... }` in Agent Builder needs the 32-char
id, but the KB page only shows library names — the only way to get the
id was digging through API responses.

## Tests (TDD, red first)

- button hidden with no selection; appears on selection; click writes
the kb_id via `navigator.clipboard` (installed/restored per repo jsdom
guidance)

## Note

Touches the same selector row as #2858 — whichever merges second gets a
trivial conflict I'll resolve.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

**PR body:**

## What

A ghost clipboard button next to the Library selector copies the selected library's raw `kb_id`, with success/failure toasts (en/zh).

## Why

Declaring `kb_ref: { "kb_id": ... }` in Agent Builder needs the 32-char id, but the KB page only shows library names — the only way to get the id was digging through API responses.

## Tests (TDD, red first)

- button hidden with no selection; appears on selection; click writes the kb_id via `navigator.clipboard` (installed/restored per repo jsdom guidance)

## Note

Touches the same selector row as #2858 — whichever merges second gets a trivial conflict I'll resolve.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## refactor(web): remove frozen config surfaces (#2863)
- sha: `9a67983b6e5e5a41b2b9cb7f1ba7315826d05be3`
- 作者: bill-srp
- 日期: 2026-07-14T07:12:04Z
- PR: #2863 by bill-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2863

**Commit message:**

```
refactor(web): remove frozen config surfaces (#2863)

## Summary
- move the live `backendModelLabel` formatter out of `src/config` and
preserve the legacy chat redirect contract in a focused helper
- remove the unused `src/config` tree together with its frozen
`agent-chat-client` and `example-showcase` consumers and their obsolete
tests
- remove the orphaned `terminateSessionChat` export and shrink the
matching Knip, Vitest coverage, and ESLint exemptions

Most of the diff is deletion of already-frozen implementation and its
tests; active model-label and legacy-redirect behavior remains covered
by focused unit tests.

## Size override rationale
The 13,986-line diff is +67 / -13,919 across 91 files. The deletion is
one dependency chain: the unused config tree, its only frozen consumers,
their tests, and their tooling exemptions. Splitting it would leave
deliberately orphaned code or temporarily broken references, so this
cleanup uses the `size-override` label.

## Test plan
- [x] `bash scripts/verify-web.sh` — guards, TypeScript, 516 test files
/ 6918 tests passed, ESLint
- [x] `cd web/app && pnpm lint:deadcode`
- [x] targeted Vitest coverage for model labels, legacy chat paths,
`AgentModelSection`, and `SessionThreadClient` — 63 tests passed
- [x] `git diff --check`
```

**PR body:**

## Summary
- move the live `backendModelLabel` formatter out of `src/config` and preserve the legacy chat redirect contract in a focused helper
- remove the unused `src/config` tree together with its frozen `agent-chat-client` and `example-showcase` consumers and their obsolete tests
- remove the orphaned `terminateSessionChat` export and shrink the matching Knip, Vitest coverage, and ESLint exemptions

Most of the diff is deletion of already-frozen implementation and its tests; active model-label and legacy-redirect behavior remains covered by focused unit tests.

## Size override rationale
The 13,986-line diff is +67 / -13,919 across 91 files. The deletion is one dependency chain: the unused config tree, its only frozen consumers, their tests, and their tooling exemptions. Splitting it would leave deliberately orphaned code or temporarily broken references, so this cleanup uses the `size-override` label.

## Test plan
- [x] `bash scripts/verify-web.sh` — guards, TypeScript, 516 test files / 6918 tests passed, ESLint
- [x] `cd web/app && pnpm lint:deadcode`
- [x] targeted Vitest coverage for model labels, legacy chat paths, `AgentModelSection`, and `SessionThreadClient` — 63 tests passed
- [x] `git diff --check`


---

## feat(kb-sharing): show shared-with-me libraries read-only in the selector (#2858)
- sha: `1c9de5e44114a604ea64c4e7a4f1f312202c8aac`
- 作者: kyle-srp
- 日期: 2026-07-14T07:11:09Z
- PR: #2858 by kyle-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2858

**Commit message:**

```
feat(kb-sharing): show shared-with-me libraries read-only in the selector (#2858)

## What

Shared-with-me libraries (proxy `role: "editor"`) appear in the Library
selector under a **Shared with me** optgroup. Selecting one is
read-only:

- no Delete button, no Sharing panel (owner controls)
- uploads refused client-side with a clear message — upstream is
owner-only anyway (S1.3); this replaces a raw 403 with a friendly toast

Editors previously saw a completely empty KB page and couldn't confirm
what they'd been handed. Installers still see nothing (search-only by
design — locked by proxy test).

## Wire

`KnowledgeBaseLibrary.role?: 'owner' | 'editor'` — optional; an older
proxy (no role field) keeps today's fully-owned behavior
(regression-tested). Pairs with
SerendipityOneInc/ecap-proxy-service#150. Any deploy order safe.

## Tests (TDD, red first)

- shared library renders under its own optgroup
- selected shared library: no delete / no grants panel
- upload into shared library blocked, `upload()` never called
- role-less libraries stay fully owned (older-proxy regression)

## Note

Branches from main; expect a small merge with #2854 (document Library
column) in `KnowledgeBaseClient.tsx` — both touch the selector area.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

**PR body:**

## What

Shared-with-me libraries (proxy `role: "editor"`) appear in the Library selector under a **Shared with me** optgroup. Selecting one is read-only:

- no Delete button, no Sharing panel (owner controls)
- uploads refused client-side with a clear message — upstream is owner-only anyway (S1.3); this replaces a raw 403 with a friendly toast

Editors previously saw a completely empty KB page and couldn't confirm what they'd been handed. Installers still see nothing (search-only by design — locked by proxy test).

## Wire

`KnowledgeBaseLibrary.role?: 'owner' | 'editor'` — optional; an older proxy (no role field) keeps today's fully-owned behavior (regression-tested). Pairs with SerendipityOneInc/ecap-proxy-service#150. Any deploy order safe.

## Tests (TDD, red first)

- shared library renders under its own optgroup
- selected shared library: no delete / no grants panel
- upload into shared library blocked, `upload()` never called
- role-less libraries stay fully owned (older-proxy regression)

## Note

Branches from main; expect a small merge with #2854 (document Library column) in `KnowledgeBaseClient.tsx` — both touch the selector area.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(kb-sharing): show masked display_hint on editor grant rows (#2857)
- sha: `addfe49d4605e7fce3bf87cf4bd47e70101853fe`
- 作者: kyle-srp
- 日期: 2026-07-14T07:06:09Z
- PR: #2857 by kyle-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2857

**Commit message:**

```
feat(kb-sharing): show masked display_hint on editor grant rows (#2857)

## What

Editor rows in the Sharing panel show the masked identifier the owner
typed (`ky***@srp.one`) instead of `Editor · 74369469…`. Legacy edges
(no hint) and installer rows keep the pseudonymous truncated uid —
installers' contact info is intentionally never shown to the library
owner.

## Wire

`KnowledgeBaseGrant.display_hint?: string` — optional, so older proxies
render exactly as today. Pairs with:
- SerendipityOneInc/ecap-proxy-service#149 — field
accepted/stored/echoed, **masked server-side** (privacy boundary at the
proxy)
- #2856 — BFF sends the masked hint on add_editor

Any deploy order is safe.

## Not in this PR

Pack-share rows still show the truncated pack_id. Resolving the pack
*name* needs an agent-catalog data source this page doesn't load;
pulling the whole catalog for one label isn't worth it — follow-up if
the label proves confusing in practice.

## Tests (TDD, red first)

- editor row renders the hint when present (and not the uid)
- hint-less legacy edge + installer row keep the truncated uid

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

**PR body:**

## What

Editor rows in the Sharing panel show the masked identifier the owner typed (`ky***@srp.one`) instead of `Editor · 74369469…`. Legacy edges (no hint) and installer rows keep the pseudonymous truncated uid — installers' contact info is intentionally never shown to the library owner.

## Wire

`KnowledgeBaseGrant.display_hint?: string` — optional, so older proxies render exactly as today. Pairs with:
- SerendipityOneInc/ecap-proxy-service#149 — field accepted/stored/echoed, **masked server-side** (privacy boundary at the proxy)
- #2856 — BFF sends the masked hint on add_editor

Any deploy order is safe.

## Not in this PR

Pack-share rows still show the truncated pack_id. Resolving the pack *name* needs an agent-catalog data source this page doesn't load; pulling the whole catalog for one label isn't worth it — follow-up if the label proves confusing in practice.

## Tests (TDD, red first)

- editor row renders the hint when present (and not the uid)
- hint-less legacy edge + installer row keep the truncated uid

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(kb-sharing): send masked display_hint with editor grants (#2856)
- sha: `63d102a46714d9a7651a0ce20c4ed0110b5568e1`
- 作者: kyle-srp
- 日期: 2026-07-14T06:53:37Z
- PR: #2856 by kyle-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2856

**Commit message:**

```
feat(kb-sharing): send masked display_hint with editor grants (#2856)

## What

`add_editor` now masks the owner-typed identifier (`ky***@srp.one` /
`***5678`, capped at the proxy's 64-char limit) and sends it as
`display_hint` alongside the resolved uid, so the proxy's grant audit
list can show *who* was added.

Pairs with SerendipityOneInc/ecap-proxy-service#149 (proxy
accepts/stores/echoes the field). Either side deploying first is safe:
the field is optional upstream, and without it the audit list just keeps
showing truncated uids.

## Why

The Sharing panel shows editor edges as `Editor · 74369469…` —
unreadable. Design choice (write-time masking in the BFF, no reverse
lookup, installer edges stay uid-only) keeps raw contact data inside the
CSFLE profile store; the masked form is the only copy that leaves it.

## Tests (TDD, red first)

- `_mask_identifier`: email keeps 2 local chars + full domain; phone
keeps last 4; output capped ≤64
- `add_editor` body carries the masked hint, never the raw identifier
- existing exact-body assertion updated for the evolved contract

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

**PR body:**

## What

`add_editor` now masks the owner-typed identifier (`ky***@srp.one` / `***5678`, capped at the proxy's 64-char limit) and sends it as `display_hint` alongside the resolved uid, so the proxy's grant audit list can show *who* was added.

Pairs with SerendipityOneInc/ecap-proxy-service#149 (proxy accepts/stores/echoes the field). Either side deploying first is safe: the field is optional upstream, and without it the audit list just keeps showing truncated uids.

## Why

The Sharing panel shows editor edges as `Editor · 74369469…` — unreadable. Design choice (write-time masking in the BFF, no reverse lookup, installer edges stay uid-only) keeps raw contact data inside the CSFLE profile store; the masked form is the only copy that leaves it.

## Tests (TDD, red first)

- `_mask_identifier`: email keeps 2 local chars + full domain; phone keeps last 4; output capped ≤64
- `add_editor` body carries the masked hint, never the raw identifier
- existing exact-body assertion updated for the evolved contract

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(knowledge-base): document Library column + independent per-library filter (#2854)
- sha: `cb681b53c4b5c331703b43e9a16ba6cb0ac0d082`
- 作者: kyle-srp
- 日期: 2026-07-14T06:40:37Z
- PR: #2854 by kyle-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2854

**Commit message:**

```
feat(knowledge-base): document Library column + independent per-library filter (#2854)

## What

Fixes a UX ambiguity found during staging E2E: the upload-page document
list is org-wide, but the Library dropdown only sets the **upload
target** — it didn't scope the list, so a document appeared under every
library selection.

Now:
- **Library column** — each document row shows which library it belongs
to (name resolved from the loaded library list; `—` when untagged /
org-level).
- **Independent filter** above the list (`All` / `No library` / each
library) — narrows the view *without* touching the upload-target
selector. Default `All` keeps "see everything" as the landing view.

The list stays org-wide (server resolves org from token); filtering is
client-side on the `kb_id` now returned per document.

## Depends on

`ecap-proxy-service#147` — surfaces each document's `kb_id` in `GET
/knowledge-base/documents`. Backward-compatible: `kb_id` is optional on
the client type, so this degrades to `—`/unfiltered against an older
proxy.

## Test

- `DocumentList`: renders the library name for a tagged doc, `—` for
untagged.
- `KnowledgeBaseClient`: the filter narrows the list to a library / to
untagged, independent of the upload selector.
- verify-web green (tsc + vitest + eslint).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

**PR body:**

## What

Fixes a UX ambiguity found during staging E2E: the upload-page document list is org-wide, but the Library dropdown only sets the **upload target** — it didn't scope the list, so a document appeared under every library selection.

Now:
- **Library column** — each document row shows which library it belongs to (name resolved from the loaded library list; `—` when untagged / org-level).
- **Independent filter** above the list (`All` / `No library` / each library) — narrows the view *without* touching the upload-target selector. Default `All` keeps "see everything" as the landing view.

The list stays org-wide (server resolves org from token); filtering is client-side on the `kb_id` now returned per document.

## Depends on

`ecap-proxy-service#147` — surfaces each document's `kb_id` in `GET /knowledge-base/documents`. Backward-compatible: `kb_id` is optional on the client type, so this degrades to `—`/unfiltered against an older proxy.

## Test

- `DocumentList`: renders the library name for a tagged doc, `—` for untagged.
- `KnowledgeBaseClient`: the filter narrows the list to a library / to untagged, independent of the upload selector.
- verify-web green (tsc + vitest + eslint).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(agent-builder): 无对话时保留禁用的分享入口 (#2859)
- sha: `b3e945e976efb31401508908abe4aa6b151a48ec`
- 作者: lynn Zhuang
- 日期: 2026-07-14T06:11:57Z
- PR: #2859 by lynn-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2859

**Commit message:**

```
fix(agent-builder): 无对话时保留禁用的分享入口 (#2859)

## Summary
- 在 Agent Builder 的 `More` 菜单中始终保留 `Share conversation`
- 没有可分享对话时显示为 disabled，有消息时继续使用现有分享流程
- 更新回归测试，覆盖无消息时的禁用状态

## Root cause
`canShareConversation` 同时控制菜单项是否渲染和是否可点击，因此没有可分享消息时入口会直接消失。

## Test plan
- [x] `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderProjectActionControls.tsx'
web/app/tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] 本地 Mock 无对话项目中确认 `Share conversation` 可见且 disabled

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
```

**PR body:**

## Summary
- 在 Agent Builder 的 `More` 菜单中始终保留 `Share conversation`
- 没有可分享对话时显示为 disabled，有消息时继续使用现有分享流程
- 更新回归测试，覆盖无消息时的禁用状态

## Root cause
`canShareConversation` 同时控制菜单项是否渲染和是否可点击，因此没有可分享消息时入口会直接消失。

## Test plan
- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderProjectActionControls.tsx' web/app/tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] 本地 Mock 无对话项目中确认 `Share conversation` 可见且 disabled


---

## refactor(web): move admin access to dashboard console (#2862)
- sha: `31031f2ac199b7fd52e405958315a8115867dc66`
- 作者: bill-srp
- 日期: 2026-07-14T06:08:58Z
- PR: #2862 by bill-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2862

**Commit message:**

```
refactor(web): move admin access to dashboard console (#2862)

## Summary
- Route the webapp sidebar Admin entry to the dashboard console `/users`
page. The deploy environment injects
`NEXT_PUBLIC_DASHBOARD_CONSOLE_URL`, and the webapp appends the default
`/users` path.
- Configure separate production and staging dashboard console base URLs,
with the staging URL documented as the local development default.
- Remove the retired in-webapp Admin page, Admin BFF routes, middleware
permission guard, dedicated clients/helpers, mock scenario, and obsolete
tests.
- Keep the sidebar admin visibility check and move Changelog release
reads to the surviving image-version releases endpoint.

## Test plan
- [x] `bash scripts/verify-local.sh --changed`
- [x] `pnpm --dir web/app exec vitest run
tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts` (19
passed)
- [x] Parse `.github/workflows/deploy.yml` with Ruby YAML

## Size override
- This is an atomic deletion migration: 10,573 of the 10,762 changed
lines remove the retired Admin UI, its dedicated BFF routes, helpers,
mocks, and tests. Splitting those coupled deletions would temporarily
leave dead routes or orphaned clients/tests in the webapp.
```

**PR body:**

## Summary
- Route the webapp sidebar Admin entry to the dashboard console `/users` page. The deploy environment injects `NEXT_PUBLIC_DASHBOARD_CONSOLE_URL`, and the webapp appends the default `/users` path.
- Configure separate production and staging dashboard console base URLs, with the staging URL documented as the local development default.
- Remove the retired in-webapp Admin page, Admin BFF routes, middleware permission guard, dedicated clients/helpers, mock scenario, and obsolete tests.
- Keep the sidebar admin visibility check and move Changelog release reads to the surviving image-version releases endpoint.

## Test plan
- [x] `bash scripts/verify-local.sh --changed`
- [x] `pnpm --dir web/app exec vitest run tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts` (19 passed)
- [x] Parse `.github/workflows/deploy.yml` with Ruby YAML

## Size override
- This is an atomic deletion migration: 10,573 of the 10,762 changed lines remove the retired Admin UI, its dedicated BFF routes, helpers, mocks, and tests. Splitting those coupled deletions would temporarily leave dead routes or orphaned clients/tests in the webapp.


---

## fix(claw-interface): sync model degradation mappings (#2860)
- sha: `25d3ec7cf8af7a7eaa5526aa94209436ff08716f`
- 作者: kaka-srp
- 日期: 2026-07-14T04:08:19Z
- PR: #2860 by kaka-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2860

**Commit message:**

```
fix(claw-interface): sync model degradation mappings (#2860)

## What Problem This Solves

The credits-depleted model degradation table had drifted from the live
LiteLLM access groups. Requests for newly added chat and image models
had no Redis mapping, so `TierDegradationHandler` allowed the original
paid model instead of routing to the configured fallback.

The user-facing internal model filter had also drifted:
`agent-studio-sonnet-5` and the `xai-pass` wildcard access alias could
appear in model pickers.

## Changes

- Add all current chat degradation mappings to `qwen35-122B`, including
the `xai-pass` access alias.
- Add `gemini-3.1-flash-lite-image` degradation to `hunyuan-image-3`.
- Replace stale `kimi-k2.5` with `kimi-k2.6`.
- Hide `agent-studio-sonnet-5` and `xai-pass` from user-facing model
lists.
- Expand regression coverage to assert every current mapped chat and
image model uses the intended fallback.

## Evidence

- Live devcontainer model-group comparison:
  - expected mappings: 34
  - configured mappings: 34
  - missing: none
  - stale: none
- Targeted tests:
- `pytest tests/unit/test_plan_models.py tests/unit/test_tier_writer.py
-q`
  - 35 passed
- Backend static verification:
  - `bash scripts/verify-py.sh`
  - ruff, formatting, pyright, and import-linter passed
- Pre-push changed-surface verification passed.
```

**PR body:**

## What Problem This Solves

The credits-depleted model degradation table had drifted from the live LiteLLM access groups. Requests for newly added chat and image models had no Redis mapping, so `TierDegradationHandler` allowed the original paid model instead of routing to the configured fallback.

The user-facing internal model filter had also drifted: `agent-studio-sonnet-5` and the `xai-pass` wildcard access alias could appear in model pickers.

## Changes

- Add all current chat degradation mappings to `qwen35-122B`, including the `xai-pass` access alias.
- Add `gemini-3.1-flash-lite-image` degradation to `hunyuan-image-3`.
- Replace stale `kimi-k2.5` with `kimi-k2.6`.
- Hide `agent-studio-sonnet-5` and `xai-pass` from user-facing model lists.
- Expand regression coverage to assert every current mapped chat and image model uses the intended fallback.

## Evidence

- Live devcontainer model-group comparison:
  - expected mappings: 34
  - configured mappings: 34
  - missing: none
  - stale: none
- Targeted tests:
  - `pytest tests/unit/test_plan_models.py tests/unit/test_tier_writer.py -q`
  - 35 passed
- Backend static verification:
  - `bash scripts/verify-py.sh`
  - ruff, formatting, pyright, and import-linter passed
- Pre-push changed-surface verification passed.


---

## feat(pack-store): add default_model to packs and submissions (#2844)
- sha: `850f53db6b00003dc568b203e125bb6e24247bbe`
- 作者: bill-srp
- 日期: 2026-07-14T03:15:05Z
- PR: #2844 by bill-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2844

**Commit message:**

```
feat(pack-store): add default_model to packs and submissions (#2844)

## Linear
<!-- 无对应 Linear issue；按用户直接需求实现 -->

## Summary
- Add optional `default_model` (free-form string, trimmed, empty → null)
to Pack Store `Pack` / `PackSubmission` and every metadata-bearing
request/response schema, consolidated via a `DefaultModelMixin`
(normalization lives in one place).
- Accept `default_model` on all pack write APIs: enterprise pack create
+ submission create, internal create / `POST /{pack_id}` update /
submission create / from-private. Approval copies the submission's value
onto the pack atomically (`approve_submission_and_sync_pack`);
`submit_new_version` carries the pack's current value forward when the
request omits it.
- Write it to agent config at install time:
`agent_install_service.install_agent` →
`apply_pack_agent_to_agents_list` seeds `agents.list[].model.primary`
from the pack's `default_model` **only when the entry has no model
yet**. A user-set per-agent model is never overwritten — and now
survives reinstalls (previously the rebuild silently dropped it).
- Refactor: dedupe the literal `_binding_match_pair` /
`_merge_agent_bindings` copies from `agent_deploy.py` /
`agent_list_config.py` into `bot_config_payload.py` (keeps the jscpd
source-duplication gate ≤3.00%).
- dashboard-console: "Default model" input in pack + submission dialogs;
threaded through form state, normalization, API types; metadata-refresh
preserves the existing value.
- web/app: read-only "Default model" row on `PackDetailView` (agent
detail + shared pack pages); added to pack model types incl.
`SharedPackResponse` (deliberate allowlist addition — model id is not
sensitive).

Design spec:
`docs/superpowers/specs/2026-07-13-pack-default-model-design.md`;
implementation plan:
`docs/superpowers/plans/2026-07-13-pack-default-model.md`.

## Test plan
- [x] Backend TDD per task: schema round-trip/normalization (7 tests),
repo/service plumbing incl. approval copy + carry-forward fallback (5),
route forwarding (2), install seeding: seeds when absent / preserves
user model / omits when unset (3) — all green.
- [x] `bash scripts/verify-py.sh` (ruff, ruff-format, pyright,
import-linter) green; jscpd src duplication 2.98% (≤3.00%).
- [x] `bash scripts/verify-changed.sh` green (web guards + tsc + eslint;
py static checks).
- [x] dashboard-console `pnpm run typecheck && pnpm test` — 551 tests
green (new pack lifecycle test covers create → update/clear → submission
override → approval promotion).
- [x] web/app `bash scripts/verify-web.sh` — 7,606 tests green
(PackDetailView shows/omits the row).
- [x] Full local backend suite ran (5,757 passed); 4 BDD failures +
89.71% coverage are local-env artifacts (no `redis` host outside the
compose network) — CI with full sidecars is the authoritative 90% gate.

## Deploy note
Cross-surface: deploy backend (`claw-interface`) before or together with
web/dashboard-console — the frontends read the new response field.
Seeding affects new installs/reinstalls only; existing installed agents
are untouched until redeployed.
```

**PR body:**

## Linear
<!-- 无对应 Linear issue；按用户直接需求实现 -->

## Summary
- Add optional `default_model` (free-form string, trimmed, empty → null) to Pack Store `Pack` / `PackSubmission` and every metadata-bearing request/response schema, consolidated via a `DefaultModelMixin` (normalization lives in one place).
- Accept `default_model` on all pack write APIs: enterprise pack create + submission create, internal create / `POST /{pack_id}` update / submission create / from-private. Approval copies the submission's value onto the pack atomically (`approve_submission_and_sync_pack`); `submit_new_version` carries the pack's current value forward when the request omits it.
- Write it to agent config at install time: `agent_install_service.install_agent` → `apply_pack_agent_to_agents_list` seeds `agents.list[].model.primary` from the pack's `default_model` **only when the entry has no model yet**. A user-set per-agent model is never overwritten — and now survives reinstalls (previously the rebuild silently dropped it).
- Refactor: dedupe the literal `_binding_match_pair` / `_merge_agent_bindings` copies from `agent_deploy.py` / `agent_list_config.py` into `bot_config_payload.py` (keeps the jscpd source-duplication gate ≤3.00%).
- dashboard-console: "Default model" input in pack + submission dialogs; threaded through form state, normalization, API types; metadata-refresh preserves the existing value.
- web/app: read-only "Default model" row on `PackDetailView` (agent detail + shared pack pages); added to pack model types incl. `SharedPackResponse` (deliberate allowlist addition — model id is not sensitive).

Design spec: `docs/superpowers/specs/2026-07-13-pack-default-model-design.md`; implementation plan: `docs/superpowers/plans/2026-07-13-pack-default-model.md`.

## Test plan
- [x] Backend TDD per task: schema round-trip/normalization (7 tests), repo/service plumbing incl. approval copy + carry-forward fallback (5), route forwarding (2), install seeding: seeds when absent / preserves user model / omits when unset (3) — all green.
- [x] `bash scripts/verify-py.sh` (ruff, ruff-format, pyright, import-linter) green; jscpd src duplication 2.98% (≤3.00%).
- [x] `bash scripts/verify-changed.sh` green (web guards + tsc + eslint; py static checks).
- [x] dashboard-console `pnpm run typecheck && pnpm test` — 551 tests green (new pack lifecycle test covers create → update/clear → submission override → approval promotion).
- [x] web/app `bash scripts/verify-web.sh` — 7,606 tests green (PackDetailView shows/omits the row).
- [x] Full local backend suite ran (5,757 passed); 4 BDD failures + 89.71% coverage are local-env artifacts (no `redis` host outside the compose network) — CI with full sidecars is the authoritative 90% gate.

## Deploy note
Cross-surface: deploy backend (`claw-interface`) before or together with web/dashboard-console — the frontends read the new response field. Seeding affects new installs/reinstalls only; existing installed agents are untouched until redeployed.


---

## fix(claw-interface): avoid version check 404 for missing users (#2855)
- sha: `9304acc0474a2de4f99fbe9772ad1fb094501d32`
- 作者: sam-srp
- 日期: 2026-07-14T03:09:32Z
- PR: #2855 by sam-srp — https://github.com/SerendipityOneInc/ecap-workspace/pull/2855

**Commit message:**

```
fix(claw-interface): avoid version check 404 for missing users (#2855)

## What changed

- Return `needs_upgrade: false` when version check cannot find an
OpenClaw user record.
- Log the missing-user condition as a warning for diagnostics.
- Verify that bot lookup is skipped in this case.

## Why

The global UI version check can run for authenticated users before an
OpenClaw user or bot is provisioned. Returning 404 made this optional
check appear as a missing frontend endpoint and generated Sentry noise.

## Impact

Authenticated users without an OpenClaw resource now receive a normal
no-upgrade response. Other endpoints that require a user record keep
their existing 404 behavior.

## Validation

- `conda run -n base pytest tests/unit/test_openclaw_version_check.py
-q` (28 passed)
- Ruff check and format check
- Pyright on the changed route and test
```

**PR body:**

## What changed

- Return `needs_upgrade: false` when version check cannot find an OpenClaw user record.
- Log the missing-user condition as a warning for diagnostics.
- Verify that bot lookup is skipped in this case.

## Why

The global UI version check can run for authenticated users before an OpenClaw user or bot is provisioned. Returning 404 made this optional check appear as a missing frontend endpoint and generated Sentry noise.

## Impact

Authenticated users without an OpenClaw resource now receive a normal no-upgrade response. Other endpoints that require a user record keep their existing 404 behavior.

## Validation

- `conda run -n base pytest tests/unit/test_openclaw_version_check.py -q` (28 passed)
- Ruff check and format check
- Pyright on the changed route and test


---

