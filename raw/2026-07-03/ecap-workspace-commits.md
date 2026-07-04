# ecap-workspace commits — 2026-07-03

## 10654e8ba6 — fix(claw-interface): map upstream FastClaw 5xx to 502 and stop logging expected domain errors as exceptions (#2653)

- SHA: 10654e8ba6b72928e6be67abdca9b5a4b339ea52
- 作者: Chris@ZooClaw
- 日期: 2026-07-03T16:14:30Z
- PR: #2653

### Commit message

```
fix(claw-interface): map upstream FastClaw 5xx to 502 and stop logging expected domain errors as exceptions (#2653)

## Summary

Three related **error/log classification** fixes in `claw-interface`
(mapping-only — explicitly **not** retry/timeout changes).

- Linear: [ECA-1119](https://linear.app/srpone/issue/ECA-1119),
[ECA-1077](https://linear.app/srpone/issue/ECA-1077),
[ECA-1105](https://linear.app/srpone/issue/ECA-1105)

## ECA-1119 / ECA-1077 — upstream FastClaw 5xx leaked as opaque HTTP 500

The write/lifecycle OpenClaw client methods (`create_bot`, `start_bot`,
`stop_bot`, `restart_bot`, `delete_bot`) called the raw
`response.raise_for_status()` → `httpx.HTTPStatusError` → favie_common
default handler → generic **HTTP 500**. The ECA-526 fix
(`_base._raise_for_status` → `ExternalServiceError`) was wired only into
READ paths.

- Route those write methods through `_base._raise_for_status`, so an
upstream error becomes `ExternalServiceError`.
- `ExternalServiceError.to_http_status()` now **collapses any upstream
5xx to 502** (Bad Gateway) while still **forwarding upstream 4xx
verbatim** (401/403/404/429).
- `_base._request` maps `httpx.TimeoutException` →
`ExternalServiceError` (502) and other transport/network errors →
`DependencyNotReadyError` (503), instead of bubbling to the catch-all
500. `RemoteProtocolError` keeps its single idempotent-only replay —
**POST/`create_bot` is never replayed** (non-idempotent: FastClaw pod +
Mattermost + Mongo doc).
- `redeploy_bot`'s idempotent "bot is not running" 400 detection now
reads upstream status/message from the `ExternalServiceError` context
(carried via `_raise_for_status` as `upstream_message`), since the raw
`httpx.Response` no longer reaches it.

### Idempotency caveat fix (required)

`create_fastclaw_bot` gated its app-token reset on `"401" not in
str(create_err)`. Now that `create_bot` raises `ExternalServiceError`,
the gate inspects `exc.context["upstream_status"] == 401` instead
(precise; no substring false-match on unrelated "401" text).

- `app/services/computer/computer_create_service.py` lines ~100–122 (the
`except` block in `create_fastclaw_bot`) + new imports `from http import
HTTPStatus` / `from app.errors import ExternalServiceError`.

### Adjacent consequence

`account_service.register` used
`ExternalServiceError(context={"upstream_status": 503})` as a way to
force a 503 for FastClaw app-provisioning unavailability. Under the new
5xx→502 collapse that would silently become 502, so it now raises
`DependencyNotReadyError` (default 503) — the semantically correct
"dependency not ready" type.

## ECA-1105 — expected DomainValidationError logged as ERROR with
traceback

`submit_test_iteration` wrapped every failure in `except Exception` +
`logger.exception(...)` and re-raised a generic
`agent_builder.submit_failed`, firing GCP error alerting on expected
user-correctable rejections (`agent_builder.pack_version_exists`,
`pack.deprecated`) and discarding the granular code.

- Now: for a `DomainValidationError`, persist failure fields, log at
**info** (no stack trace), and **re-raise the original exception** so
its specific code survives. `logger.exception` + the generic
`submit_failed` wrapping is reserved for genuinely unexpected
exceptions.

## Tests

Added/updated unit tests:
- create_bot upstream 500/502/503 → `ExternalServiceError` → **502**;
upstream 401 forwarded verbatim.
- `_request` timeout → `ExternalServiceError` (502); transport error →
`DependencyNotReadyError` (503); timeout on idempotent replay still
mapped.
- redeploy: idempotent "bot is not running" continues; other 4xx
re-raises; upstream 5xx re-raises (502, no start).
- `create_fastclaw_bot`: 401 (via context) triggers app-token reset;
non-401 5xx does **not** reset.
- `submit_test_iteration`: `DomainValidationError` re-raises original
code and does **not** call `logger.exception`; the pack_version_exists
preflight test now asserts the granular code is preserved.
- Updated existing 503-passthrough assertions to the new 502 collapse.

## Verification

- `bash scripts/verify-py.sh` (ruff + ruff-format + pyright +
import-linter): **pass**.
- CI-lint guards (file-length, complexity, deptry, collection-strings,
importlinter-repo-sync, dead-code, db-returns): **pass** when run from
the project venv.
- Full `pytest tests/unit`: **4683 passed**.
- pytest coverage gate is CI-gated (mongo required); verified locally
without coverage.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## Summary

Three related **error/log classification** fixes in `claw-interface` (mapping-only — explicitly **not** retry/timeout changes).

- Linear: [ECA-1119](https://linear.app/srpone/issue/ECA-1119), [ECA-1077](https://linear.app/srpone/issue/ECA-1077), [ECA-1105](https://linear.app/srpone/issue/ECA-1105)

## ECA-1119 / ECA-1077 — upstream FastClaw 5xx leaked as opaque HTTP 500

The write/lifecycle OpenClaw client methods (`create_bot`, `start_bot`, `stop_bot`, `restart_bot`, `delete_bot`) called the raw `response.raise_for_status()` → `httpx.HTTPStatusError` → favie_common default handler → generic **HTTP 500**. The ECA-526 fix (`_base._raise_for_status` → `ExternalServiceError`) was wired only into READ paths.

- Route those write methods through `_base._raise_for_status`, so an upstream error becomes `ExternalServiceError`.
- `ExternalServiceError.to_http_status()` now **collapses any upstream 5xx to 502** (Bad Gateway) while still **forwarding upstream 4xx verbatim** (401/403/404/429).
- `_base._request` maps `httpx.TimeoutException` → `ExternalServiceError` (502) and other transport/network errors → `DependencyNotReadyError` (503), instead of bubbling to the catch-all 500. `RemoteProtocolError` keeps its single idempotent-only replay — **POST/`create_bot` is never replayed** (non-idempotent: FastClaw pod + Mattermost + Mongo doc).
- `redeploy_bot`'s idempotent "bot is not running" 400 detection now reads upstream status/message from the `ExternalServiceError` context (carried via `_raise_for_status` as `upstream_message`), since the raw `httpx.Response` no longer reaches it.

### Idempotency caveat fix (required)

`create_fastclaw_bot` gated its app-token reset on `"401" not in str(create_err)`. Now that `create_bot` raises `ExternalServiceError`, the gate inspects `exc.context["upstream_status"] == 401` instead (precise; no substring false-match on unrelated "401" text).

- `app/services/computer/computer_create_service.py` lines ~100–122 (the `except` block in `create_fastclaw_bot`) + new imports `from http import HTTPStatus` / `from app.errors import ExternalServiceError`.

### Adjacent consequence

`account_service.register` used `ExternalServiceError(context={"upstream_status": 503})` as a way to force a 503 for FastClaw app-provisioning unavailability. Under the new 5xx→502 collapse that would silently become 502, so it now raises `DependencyNotReadyError` (default 503) — the semantically correct "dependency not ready" type.

## ECA-1105 — expected DomainValidationError logged as ERROR with traceback

`submit_test_iteration` wrapped every failure in `except Exception` + `logger.exception(...)` and re-raised a generic `agent_builder.submit_failed`, firing GCP error alerting on expected user-correctable rejections (`agent_builder.pack_version_exists`, `pack.deprecated`) and discarding the granular code.

- Now: for a `DomainValidationError`, persist failure fields, log at **info** (no stack trace), and **re-raise the original exception** so its specific code survives. `logger.exception` + the generic `submit_failed` wrapping is reserved for genuinely unexpected exceptions.

## Tests

Added/updated unit tests:
- create_bot upstream 500/502/503 → `ExternalServiceError` → **502**; upstream 401 forwarded verbatim.
- `_request` timeout → `ExternalServiceError` (502); transport error → `DependencyNotReadyError` (503); timeout on idempotent replay still mapped.
- redeploy: idempotent "bot is not running" continues; other 4xx re-raises; upstream 5xx re-raises (502, no start).
- `create_fastclaw_bot`: 401 (via context) triggers app-token reset; non-401 5xx does **not** reset.
- `submit_test_iteration`: `DomainValidationError` re-raises original code and does **not** call `logger.exception`; the pack_version_exists preflight test now asserts the granular code is preserved.
- Updated existing 503-passthrough assertions to the new 502 collapse.

## Verification

- `bash scripts/verify-py.sh` (ruff + ruff-format + pyright + import-linter): **pass**.
- CI-lint guards (file-length, complexity, deptry, collection-strings, importlinter-repo-sync, dead-code, db-returns): **pass** when run from the project venv.
- Full `pytest tests/unit`: **4683 passed**.
- pytest coverage gate is CI-gated (mongo required); verified locally without coverage.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## 8b2ad55ba0 — fix(knowledge-base): support multi-file upload (#2726)

- SHA: 8b2ad55ba017d87d4dcbc160a38178763111f36d
- 作者: kevin
- 日期: 2026-07-03T12:50:46Z
- PR: #2726

### Commit message

```
fix(knowledge-base): support multi-file upload (#2726)

## Summary

Fixes the Knowledge Base upload so it actually accepts **multiple
files**, which the UI implied but the code never supported.

Two root causes in `UploadDropzone.tsx`:
- the `<input type="file">` had no `multiple` attribute → the OS picker
allowed only one file;
- the drag-and-drop handler passed the list to `pick()`, which read only
`files?.[0]` → dragging several files uploaded just the first.

## Changes

- **`UploadDropzone.tsx`** — add `multiple` to the input; rewrite
`pick()` to iterate the whole `FileList` (picker + drop), split into
accepted vs. rejected, and dedupe rejection reasons (three unsupported
files → one toast). Prop renamed `onFile` → `onFiles: (files: File[]) =>
void`.
- **`KnowledgeBaseClient.tsx`** — `handleFile` → `handleFiles`; upload
accepted files **sequentially** (each success invalidates the documents
query; the hook's existing 10s `staleTime` already anticipates
back-to-back uploads). In a batch, failure toasts name the file;
single-file behavior is unchanged.
- **`locales/en.ts` / `locales/zh.ts`** — pluralize dropzone copy
("Choose files" / "Drag files here" / "拖拽文件到此(可多选)") and fix the
empty-state hint direction ("below" → "above", the upload box is above
the list).
- **`UploadDropzone.unit.spec.tsx`** — migrate to `onFiles`, assert the
`File[]` payload, and add coverage for multi-select, multi-drop,
`input.multiple`, mixed accept/reject batches, and reason dedup.

## Testing

- `scripts/verify-web.sh` on the changed files: **tsc clean** (changed
files), **vitest 3900 passed**, **eslint passed**.
- Manually verified against the staging backend: multi-select picker,
multi-file drag/drop, and mixed valid/invalid batches all behave
correctly.

Closes #2724

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## Summary

Fixes the Knowledge Base upload so it actually accepts **multiple files**, which the UI implied but the code never supported.

Two root causes in `UploadDropzone.tsx`:
- the `<input type="file">` had no `multiple` attribute → the OS picker allowed only one file;
- the drag-and-drop handler passed the list to `pick()`, which read only `files?.[0]` → dragging several files uploaded just the first.

## Changes

- **`UploadDropzone.tsx`** — add `multiple` to the input; rewrite `pick()` to iterate the whole `FileList` (picker + drop), split into accepted vs. rejected, and dedupe rejection reasons (three unsupported files → one toast). Prop renamed `onFile` → `onFiles: (files: File[]) => void`.
- **`KnowledgeBaseClient.tsx`** — `handleFile` → `handleFiles`; upload accepted files **sequentially** (each success invalidates the documents query; the hook's existing 10s `staleTime` already anticipates back-to-back uploads). In a batch, failure toasts name the file; single-file behavior is unchanged.
- **`locales/en.ts` / `locales/zh.ts`** — pluralize dropzone copy ("Choose files" / "Drag files here" / "拖拽文件到此(可多选)") and fix the empty-state hint direction ("below" → "above", the upload box is above the list).
- **`UploadDropzone.unit.spec.tsx`** — migrate to `onFiles`, assert the `File[]` payload, and add coverage for multi-select, multi-drop, `input.multiple`, mixed accept/reject batches, and reason dedup.

## Testing

- `scripts/verify-web.sh` on the changed files: **tsc clean** (changed files), **vitest 3900 passed**, **eslint passed**.
- Manually verified against the staging backend: multi-select picker, multi-file drag/drop, and mixed valid/invalid batches all behave correctly.

Closes #2724


## 6743751a3e — fix(agent-builder): restore build replay sharing (#2725)

- SHA: 6743751a3e33a450e07eb66cc2068b2b2e199979
- 作者: kaka-srp
- 日期: 2026-07-03T12:51:23Z
- PR: #2725

### Commit message

```
fix(agent-builder): restore build replay sharing (#2725)

## Summary
- Restore replay sharing on the Agent Builder build conversation.
- Reuse the existing chat replay share flow in the builder pane and hide
the composer during selection.
- Gate the Share action to ready, rendered builder conversations and
cover the replay create payload.

## Root cause
Agent Builder's build page renders its own conversation surface. After
that surface diverged from the main chat layout, it no longer wired the
header Share action or replay selection frame into the builder
conversation, so replay sharing disappeared from the build flow.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderReplayShare.tsx'
web/app/tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] `git push` pre-push changed-surface gate
```

### PR body

## Summary
- Restore replay sharing on the Agent Builder build conversation.
- Reuse the existing chat replay share flow in the builder pane and hide the composer during selection.
- Gate the Share action to ready, rendered builder conversations and cover the replay create payload.

## Root cause
Agent Builder's build page renders its own conversation surface. After that surface diverged from the main chat layout, it no longer wired the header Share action or replay selection frame into the builder conversation, so replay sharing disappeared from the build flow.

## Test plan
- [x] `pnpm exec vitest run tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderReplayShare.tsx' web/app/tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] `git push` pre-push changed-surface gate


## fa7543a7c2 — fix(chat): clear failed upload placeholders (#2719)

- SHA: fa7543a7c2e05f37aef03303f2804db6a8ce69c6
- 作者: tim-srp
- 日期: 2026-07-03T10:09:14Z
- PR: #2719

### Commit message

```
fix(chat): clear failed upload placeholders (#2719)

## Summary
- Fix failed file-upload cleanup in the chat composer when a
pasted/copied filename contains a closing bracket.
- Sanitize uploaded file markdown labels so filenames with brackets do
not create malformed composer markdown.
- Preserve functional placeholder appends for back-to-back uploads so
concurrent uploads cannot overwrite earlier placeholders.
- Add regression tests for bracket filenames, persisted pending drafts,
opening brackets, normal uploading text, and consecutive uploads before
the first upload resolves.

## Root cause
The composer disabled send while `uploading:` placeholders remained in
the input. Failed upload cleanup used a regex that could not match
placeholder markdown when the filename contained `]`, and raw filenames
were inserted directly into markdown labels, so bracketed filenames
could create malformed attachment markup.

## Test plan
- [x]
`/Users/shiqi/pandaclaw-code/ecap-workspace/web/app/node_modules/.bin/vitest
run --config ./vitest.config.mts
tests/unit/app/chat/GenClawInput.unit.spec.tsx` (64 tests passed, run
from the isolated worktree)
- [ ] `eslint` targeted changed files (blocked locally: isolated
worktree dependency layout could not resolve
`@zooclaw/design-system/tokens.css`; CI web-quality lint-and-typecheck
runs in the proper workspace install)
- [ ] `tsc --noEmit` (blocked locally: isolated worktree dependency
layout could not resolve `@zooclaw/design-system`; CI web-quality
lint-and-typecheck runs in the proper workspace install)
```

### PR body

## Summary
- Fix failed file-upload cleanup in the chat composer when a pasted/copied filename contains a closing bracket.
- Sanitize uploaded file markdown labels so filenames with brackets do not create malformed composer markdown.
- Preserve functional placeholder appends for back-to-back uploads so concurrent uploads cannot overwrite earlier placeholders.
- Add regression tests for bracket filenames, persisted pending drafts, opening brackets, normal uploading text, and consecutive uploads before the first upload resolves.

## Root cause
The composer disabled send while `uploading:` placeholders remained in the input. Failed upload cleanup used a regex that could not match placeholder markdown when the filename contained `]`, and raw filenames were inserted directly into markdown labels, so bracketed filenames could create malformed attachment markup.

## Test plan
- [x] `/Users/shiqi/pandaclaw-code/ecap-workspace/web/app/node_modules/.bin/vitest run --config ./vitest.config.mts tests/unit/app/chat/GenClawInput.unit.spec.tsx` (64 tests passed, run from the isolated worktree)
- [ ] `eslint` targeted changed files (blocked locally: isolated worktree dependency layout could not resolve `@zooclaw/design-system/tokens.css`; CI web-quality lint-and-typecheck runs in the proper workspace install)
- [ ] `tsc --noEmit` (blocked locally: isolated worktree dependency layout could not resolve `@zooclaw/design-system`; CI web-quality lint-and-typecheck runs in the proper workspace install)

## cd594816ef — docs: sync-docs weekly sweep (2026-07-03) (#2717)

- SHA: cd594816eff952a6203155fa7862f12c823f5486
- 作者: bill-srp
- 日期: 2026-07-03T09:04:45Z
- PR: #2717

### Commit message

```
docs: sync-docs weekly sweep (2026-07-03) (#2717)

Weekly sync-docs sweep. Window reviewed: `1d448f9c5` (2026-06-29 sweep)
→ `c8cdc2bce` (HEAD), 57 commits / 448 files.

Docs changed: `architecture.md`, `architecture.zh-CN.md`,
`services/claw-interface/AGENTS.md`, `web/app/AGENTS.md`.

## Tier 1 — deterministic fixes

None — `drift-probe.sh` reported clean before and after this sweep.

## Tier 2 — semantic fixes (evidence-grounded)

1. **Document the WhatsApp Business bridge** (new subsection in
`architecture.md` Section C, mirrored in `architecture.zh-CN.md`). The
`/whatsapp` service-to-service surface shipped in #2711 and #2716 with
zero mentions in any onboarding doc.
- Evidence: `services/claw-interface/app/routes/whatsapp.py`
("Service-to-service WhatsApp Business bridge contracts"),
`app/services/whatsapp_service.py`, `app/database/whatsapp_repo.py`,
`app/schema/whatsapp.py`; auth via `CONNECTOR_SERVICE_TOKEN`
(`app/settings.py:171`).
2. **`services/claw-interface/AGENTS.md`: fix stale frontend config
path** — `web/src/lib/api/config.ts` → `web/app/src/lib/api/config.ts`.
- Evidence: old path does not exist on disk; the file lives at
`web/app/src/lib/api/config.ts` (pre-workspace-restructure leftover).
3. **`services/claw-interface/AGENTS.md`: fix `pnpm dev` instruction** —
"run `pnpm dev` from repo root" → run from `web/`.
- Evidence: the repo root has no `package.json`; `web/AGENTS.md` states
all pnpm commands run from `web/` (README agrees).
4. **`web/app/AGENTS.md`: fix three stale `web/src`-era paths** —
`web/src/app/landing/landing.css` →
`web/app/src/app/landing/landing.css`; `web/components.json` →
`web/app/components.json`; `web/src/app/globals.css` →
`web/app/src/app/globals.css`.
- Evidence: each old path is missing on disk; each corrected path
exists.

Verified clean (no edit needed): architecture EN/中文 parity (in-window
commits #2689 and #2710 both edited the pair together); the paid
agent-pack purchase section already matches the shipped #2712/#2713
implementation; README app/service/workflow/tag tables.

## Tier 3 — suggestions (not applied)

- **Bossclaw surface**: `web/app/src/app/[locale]/bossclaw/`
(onboarding, WhatsApp QR bind, new login page #2708) has no mention in
any onboarding doc — consider a one-liner in README or a module-scoped
AGENTS entry once the surface stabilizes.
- **Computer-scoped agent settings migration** (#2637/#2645; legacy
agent routes deprecated in #2705): mid-flight per
`docs/superpowers/specs/2026-06-26-computer-agent-settings-migration-design.md`;
once it fully lands, a "deprecated agent routes" note in
`services/claw-interface/AGENTS.md` (like the existing LiteLLM one)
would fit.
- **Code gap, outside this skill's write scope**:
`CONNECTOR_SERVICE_TOKEN` exists in `app/settings.py` but is missing
from `.env.example`.



## Follow-up commit — claw-interface architecture audit (same evidence
bar as Tier 2)

A targeted audit of the claw-interface claims in these docs surfaced
four more stale facts, fixed in the second commit:

1. **`services/claw-interface/AGENTS.md`: "Deprecated: LiteLLM Routes"
section referenced a deleted file.** `app/routes/litellm.py` and the
canvas surface were removed in #2447; `fullstack_assistant` is served
via `app/routes/session/chat.py`. Section rewritten as "AI-generation
entry point" keeping the still-valid guidance.
2. **Route-package template no longer matched its exemplar.**
`app/routes/session/` has no `core.py` / `shared.py`; it has `chat.py`,
`session_crud.py`, `credits.py`, `jobs.py`, `sse.py`, `archived.py`,
`utils.py`. Bullet list updated to reality.
3. **Rotted line refs in `architecture.md` + `architecture.zh-CN.md`**
(files/claims still correct): `bot_config.py:301-304` → `:150,385`
(`AGENT_IDENTITY_API_BASE` injection sites);
`integration_provider.py:83-89` → `:41-50` (also reworded —
`NangoProvider` no longer constructs `httpx.AsyncClient(base_url=...)`,
it resolves `base_url` from `SETTINGS.NANGO_SERVER_URL`);
`middleware.ts:100` → `:114` (the `verifyToken` call).
4. **Mattermost web-side code refs**: the `NEXT_PUBLIC_MATTERMOST_URL`
read is now centralized in `web/app/src/lib/mattermost/constants.ts:7`
(`MATTERMOST_SERVER_URL`); `MattermostProvider.tsx:25` / `blob.ts:7`
refs replaced accordingly.

Verified accurate during the same audit (no change needed): C1/C4/C4b
import-linter contracts, repo atomic primitives, cron endpoints +
`docs/cron-triggers.md`, `AGENT_PLATFORM_URL` usage
(`app/routes/session/chat.py:368,579`), `token_verifier.py`,
`openclaw_client/__init__.py`, `asr/service.py:73`,
`agent_identity.py:68/:121`, the seven non-bot `/session/chat` agents,
and the env-var table.

---------

Co-authored-by: ecap-bot <ecap-bot@users.noreply.github.com>
```

### PR body

Weekly sync-docs sweep. Window reviewed: `1d448f9c5` (2026-06-29 sweep) → `c8cdc2bce` (HEAD), 57 commits / 448 files.

Docs changed: `architecture.md`, `architecture.zh-CN.md`, `services/claw-interface/AGENTS.md`, `web/app/AGENTS.md`.

## Tier 1 — deterministic fixes

None — `drift-probe.sh` reported clean before and after this sweep.

## Tier 2 — semantic fixes (evidence-grounded)

1. **Document the WhatsApp Business bridge** (new subsection in `architecture.md` Section C, mirrored in `architecture.zh-CN.md`). The `/whatsapp` service-to-service surface shipped in #2711 and #2716 with zero mentions in any onboarding doc.
   - Evidence: `services/claw-interface/app/routes/whatsapp.py` ("Service-to-service WhatsApp Business bridge contracts"), `app/services/whatsapp_service.py`, `app/database/whatsapp_repo.py`, `app/schema/whatsapp.py`; auth via `CONNECTOR_SERVICE_TOKEN` (`app/settings.py:171`).
2. **`services/claw-interface/AGENTS.md`: fix stale frontend config path** — `web/src/lib/api/config.ts` → `web/app/src/lib/api/config.ts`.
   - Evidence: old path does not exist on disk; the file lives at `web/app/src/lib/api/config.ts` (pre-workspace-restructure leftover).
3. **`services/claw-interface/AGENTS.md`: fix `pnpm dev` instruction** — "run `pnpm dev` from repo root" → run from `web/`.
   - Evidence: the repo root has no `package.json`; `web/AGENTS.md` states all pnpm commands run from `web/` (README agrees).
4. **`web/app/AGENTS.md`: fix three stale `web/src`-era paths** — `web/src/app/landing/landing.css` → `web/app/src/app/landing/landing.css`; `web/components.json` → `web/app/components.json`; `web/src/app/globals.css` → `web/app/src/app/globals.css`.
   - Evidence: each old path is missing on disk; each corrected path exists.

Verified clean (no edit needed): architecture EN/中文 parity (in-window commits #2689 and #2710 both edited the pair together); the paid agent-pack purchase section already matches the shipped #2712/#2713 implementation; README app/service/workflow/tag tables.

## Tier 3 — suggestions (not applied)

- **Bossclaw surface**: `web/app/src/app/[locale]/bossclaw/` (onboarding, WhatsApp QR bind, new login page #2708) has no mention in any onboarding doc — consider a one-liner in README or a module-scoped AGENTS entry once the surface stabilizes.
- **Computer-scoped agent settings migration** (#2637/#2645; legacy agent routes deprecated in #2705): mid-flight per `docs/superpowers/specs/2026-06-26-computer-agent-settings-migration-design.md`; once it fully lands, a "deprecated agent routes" note in `services/claw-interface/AGENTS.md` (like the existing LiteLLM one) would fit.
- **Code gap, outside this skill's write scope**: `CONNECTOR_SERVICE_TOKEN` exists in `app/settings.py` but is missing from `.env.example`.



## Follow-up commit — claw-interface architecture audit (same evidence bar as Tier 2)

A targeted audit of the claw-interface claims in these docs surfaced four more stale facts, fixed in the second commit:

1. **`services/claw-interface/AGENTS.md`: "Deprecated: LiteLLM Routes" section referenced a deleted file.** `app/routes/litellm.py` and the canvas surface were removed in #2447; `fullstack_assistant` is served via `app/routes/session/chat.py`. Section rewritten as "AI-generation entry point" keeping the still-valid guidance.
2. **Route-package template no longer matched its exemplar.** `app/routes/session/` has no `core.py` / `shared.py`; it has `chat.py`, `session_crud.py`, `credits.py`, `jobs.py`, `sse.py`, `archived.py`, `utils.py`. Bullet list updated to reality.
3. **Rotted line refs in `architecture.md` + `architecture.zh-CN.md`** (files/claims still correct): `bot_config.py:301-304` → `:150,385` (`AGENT_IDENTITY_API_BASE` injection sites); `integration_provider.py:83-89` → `:41-50` (also reworded — `NangoProvider` no longer constructs `httpx.AsyncClient(base_url=...)`, it resolves `base_url` from `SETTINGS.NANGO_SERVER_URL`); `middleware.ts:100` → `:114` (the `verifyToken` call).
4. **Mattermost web-side code refs**: the `NEXT_PUBLIC_MATTERMOST_URL` read is now centralized in `web/app/src/lib/mattermost/constants.ts:7` (`MATTERMOST_SERVER_URL`); `MattermostProvider.tsx:25` / `blob.ts:7` refs replaced accordingly.

Verified accurate during the same audit (no change needed): C1/C4/C4b import-linter contracts, repo atomic primitives, cron endpoints + `docs/cron-triggers.md`, `AGENT_PLATFORM_URL` usage (`app/routes/session/chat.py:368,579`), `token_verifier.py`, `openclaw_client/__init__.py`, `asr/service.py:73`, `agent_identity.py:68/:121`, the seven non-bot `/session/chat` agents, and the env-var table.


## c8cdc2bcea — fix(whatsapp): add claw interface bridge contracts (#2716)

- SHA: c8cdc2bceaf6cd4e669de2286ee29b39b5f132a6
- 作者: bill-srp
- 日期: 2026-07-03T07:11:07Z
- PR: #2716

### Commit message

```
fix(whatsapp): add claw interface bridge contracts (#2716)

## Summary
- Add the claw-interface WhatsApp bridge contracts needed by the
WhatsApp Business service.
- Add service-token protected lookup for outbound WhatsApp targets via
`GET /whatsapp/users?uid=...&mattermost_channel_id=...`.
- Add typed schema/repo/service tests for WhatsApp binding lookup,
inbound idempotency, and Mattermost channel ownership.

## Root cause
The WhatsApp Business bridge needed claw-interface-owned persistence and
lookup contracts before the standalone service code could be landed
separately. Keeping this PR scoped to `services/claw-interface` lets the
backend contract ship and review independently.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH pytest
services/claw-interface/tests/unit/test_whatsapp_schema.py
services/claw-interface/tests/unit/test_whatsapp_repo.py
services/claw-interface/tests/unit/test_whatsapp_routes.py
services/claw-interface/tests/unit/test_whatsapp_service.py
services/claw-interface/tests/unit/test_agent_workspace_repo.py -q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
- [x] `git diff --check`
```

### PR body

## Summary
- Add the claw-interface WhatsApp bridge contracts needed by the WhatsApp Business service.
- Add service-token protected lookup for outbound WhatsApp targets via `GET /whatsapp/users?uid=...&mattermost_channel_id=...`.
- Add typed schema/repo/service tests for WhatsApp binding lookup, inbound idempotency, and Mattermost channel ownership.

## Root cause
The WhatsApp Business bridge needed claw-interface-owned persistence and lookup contracts before the standalone service code could be landed separately. Keeping this PR scoped to `services/claw-interface` lets the backend contract ship and review independently.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH pytest services/claw-interface/tests/unit/test_whatsapp_schema.py services/claw-interface/tests/unit/test_whatsapp_repo.py services/claw-interface/tests/unit/test_whatsapp_routes.py services/claw-interface/tests/unit/test_whatsapp_service.py services/claw-interface/tests/unit/test_agent_workspace_repo.py -q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`
- [x] `git diff --check`

