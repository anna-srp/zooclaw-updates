# SerendipityOneInc/ecap-agent-pack - Commits on 2026-06-04

## 1. refactor(agent-studio): remove --pack-dir — Studio builds only in its own workspace (#163)

- **SHA**: `fec2307db4c0f329df3cdc8c05131ca4f18f1ea2`
- **Author**: felix-srp
- **Date**: 2026-06-04T16:10:05Z
- **Files Changed**: 38
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/fec2307db4c0f329df3cdc8c05131ca4f18f1ea2
- **PR**: #163

### Full Commit Message

```
refactor(agent-studio): remove --pack-dir — Studio builds only in its own workspace (#163)

Removes --pack-dir from all Studio build scripts (cwd-only); deletes run_share's dead tmp/<pack> foreign-staging path; moves the workspace-confinement invariant to AGENTS.md (the always-loaded layer); keeps it only on the connect_composio runtime template. Extends the removal to #142's connectors.py/write_onboarding.py. agent-studio 1.5.0 -> 1.7.0; 202 tests pass.
```

### PR Description

## Why

The chanel-stylist bug (an installed pack that was an empty ~2.5 KB shell) had two roots. PR #162 added the legitimate update path (`/studio open <archive>`) and a *textual* guardrail. This PR removes the **structural** root: the `--pack-dir` flag let any script be pointed at a pack other than Studio's own workspace, and one in-code path actively staged a *foreign* pack.

Verified: **every** documented invocation was `--pack-dir .`; the only non-`.` user was the dead `tmp/<pack>` test. So `--pack-dir` was always cwd — removing it is behavior-preserving and removes the foreign-targeting vector by construction.

## What

**Remove `--pack-dir` from every Studio build script** — `main()` reads `Path.cwd()`; inner functions keep their `pack_dir` param (callers/tests pass it directly):

`clean · generate_description · list_packs · migrate_manifest · preserve_creator_notes · snapshot · spec_coverage · validate · import_archive · package · run_share · install · connectors · write_onboarding`

**Delete the actual safety hole** — `run_share.py`'s `resolve_public_pack_dir()` `tmp/<pack>` branch + `_looks_like_public_workspace_dir()`, the only in-code path that staged a pack other than cwd ("Agent Studio sometimes builds a foreign pack in `<workspace>/tmp/<pack>`…"). `run_share`/`install` now spawn `package.py`/`run_share.py` with `cwd=` instead of forwarding the flag.

**Move the workspace-confinement invariant to `AGENTS.md`** — it's identity-level ("operate only on this workspace (cwd); never `cd` into another agent's — editing one corrupts its running agent; update another pack via `/studio open`"), so it belongs in the always-loaded `AGENTS.md`, not `SKILL.md` (which reaches context only via a DEV-mode session-start read). Confirmed against the runtime that `metadata.openclaw.always:true` is a load-time *eligibility* gate, not a content-injection guarantee — so it doesn't keep `SKILL.md` resident.

**One deliberate exception:** `templates/onboarding/connect_composio.py` keeps `--pack-dir` (default `.`). It's a runtime template shipped *into* the deployed pack and run in the pack's own context — not a Studio build script. Commented inline so a future consistency sweep doesn't "fix" it.

**Invariant:** a pack's *location* is always cwd; foreign *content* enters only via `--archive` / `--share`, never a foreign location.

*Honest scope:* this removes the flag footgun + the dead staging path; it is **not** a sandbox against an LLM `cd`-ing into a deployed workspace first — that behavioral vector is held by the `AGENTS.md` guardrail.

## Merge note

Merged onto `main` after **#142 (Composio connectors)** landed, and extended the `--pack-dir` removal to the two build scripts it added (`connectors.py`, `write_onboarding.py`) + converted their tests. `package.py`/`validate.py` auto-merged cleanly (my removal + #142's connector validation); the doc conflicts resolved to drop `--pack-dir` while keeping #142's new `--skip-online-validation` flag.

## Tests & docs

- Deleted `test_run_share_tmp_artifacts.py` (its subject is gone).
- Converted ~10 suites off `--pack-dir <p>`: subprocess tests use `cwd=`, in-process tests use `monkeypatch.chdir` / `setUp`-`chdir`.
- Updated `SKILL.md` / `AGENTS.md` / `references/*` examples and stale in-script messages (e.g. recovery hints that suggested `snapshot.py capture --pack-dir .`).
- **agent-studio 1.5.0 → 1.7.0** (1.6.0 came from #142).

## How tested

- **202 tests pass** — 104 (`tests/`) + 98 (`scripts/tests/` connector suite). package.py's cwd-flow is covered end-to-end by the `package.py → import_archive.py` round-trip.
- All scripts `py_compile` / `--help` load; the only remaining `--pack-dir` is the intentional `connect_composio.py` template.
- Two independent correctness passes (Claude + Codex) on the merge result: no bugs.

Net **−232 LOC** (mostly the deleted dead path + tmp test).

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## 2. feat(agent-studio): connectors — catalog client + onboarding login (v1.6.0) (#142)

- **SHA**: `cf9efae8143a21bb71a0f160df13be8bda4a85b7`
- **Author**: felix-srp
- **Date**: 2026-06-04T15:15:44Z
- **Files Changed**: 21
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/cf9efae8143a21bb71a0f160df13be8bda4a85b7
- **PR**: #142

### Full Commit Message

```
feat(agent-studio): connectors — catalog client + onboarding login (v1.6.0) (#142)
```

### PR Description

## Summary

Adds a **connectors** capability to Agent Studio (`v1.4.2 → v1.6.0`). Creators can discover, inspect, and declare the third-party providers (Notion, Slack, GitHub, Gmail, Google Drive, …) a generated pack expects — and the generated pack's onboarding turns those declarations into clickable OAuth login links for the end user. Backed by the platform connector service (Composio via `ecap-proxy-service`); creators only ever see "connectors."

### 1. Connector catalog client (authoring time)
`scripts/connectors.py` — talks to `GET /composio/providers`:
- `list` — browse the live catalog; **available-only by default** (the catalog carries ~1000 providers but only the handful with an auth-config are connectable), `--all` reveals the rest marked `(unavailable)`.
- `show <name>` — print a provider's action allowlist (read inline from the catalog).
- `add <name> --pack-dir .` — record in the manifest's top-level `connectors:` field (atomic write, symlink-escape guarded). Refuses unknown/unavailable providers with distinct messages.
- `remove <name>` — idempotent removal.

`validate.py check_connectors` is a **release gate**: declared connectors are schema-checked (kebab-case) and validated against the live catalog, failing *closed* if the proxy is unreachable unless `--skip-online-validation` (offline creator runs). `package.py` delegates to this gate at publish time.

> The `connectors:` field is **authoring-time guidance** — nothing consumes it at runtime. The platform's connector plugin surfaces each user's connected+enabled tools dynamically; the field records intent and drives onboarding.

### 2. Onboarding connector login (delivery time)
`templates/onboarding/connect_composio.py` (shipped verbatim into generated packs, self-contained):
- `plan` — reads manifest connectors, checks `GET /composio/connections`, and for each not-yet-connected provider issues `POST /composio/connections/{provider}/connect` (body `{callback_url}`) → `{connected, needs_login:[{provider, display_name, auth_url}], errors}` so onboarding shows inline login links instead of sending the user hunting through Settings.
- `sync` — `PUT enable` for connected-but-disabled providers.

`write_onboarding.py` **self-derives** the connector set from `agent-pack.yaml#connectors` — declaring a connector in Stage 2 is enough; the generator adds the "Connect Your Accounts" onboarding step automatically.

Reference docs updated across the Studio flow (`data-sources.md` Layer 1, `skill-design.md` Stage 2b, `automation.md` Stage 3, `discovery.md`, `testing.md`, `SKILL.md`). Creator-facing prose says "connectors"; "Composio" remains only in the real API path + script/flag identifiers. End users are **prompted to connect during onboarding** (one-click login links); the **Settings → Connectors** menu is the management fallback (label rendered in the user's language).

## Testing

**202 unit tests** — 98 connector (`scripts/tests`, stdlib-only) + 104 spec/validate (`agent-studio/tests`). Covers YAML parse/splice round-trips, exit-code contract (0/1/2), error classification, atomic write + symlink-escape guard, onboarding plan/sync JSON contract, the available-only/`--all` filter.

**End-to-end against live staging** (Linux docker devcontainer, real Cloudflare-fronted path): list=11 providers, show=actions inline, add↔remove round-trip, exit 1 (unknown) / exit 2 (401, unreachable), `connect plan`→real OAuth URL, `sync`, validate gate pass/fail-closed/skip-online.

**Hand-tested in webchat** (staging account, sonnet-4-6): drove the Discovery → confirmation flow for a Gmail pack. Verified `google-mail` is the correct live provider id (Gmail, available, 20 actions) and tightened three creator/end-user touchpoints surfaced by the test — present the connector by display name (*Gmail*, not the `google-mail` slug); frame onboarding (not Settings) as the primary connect path; correct the menu label to **Settings → Connectors** (and the step name to "Connect Your Accounts").

**Probed live prod** (bot `0ae5098c`): the Composio contract matches the PR's assumptions (1042 providers, 11 available, field schema, 404 classification, `connect` requires `callback_url`). No code change was needed.

## Reviews

Reviewed by Claude + Codex across multiple rounds (catalog client, Composio migration, onboarding, cleanup, final pass); all findings fixed or dispositioned. Latest dual review: **READY** (Codex's 4 final findings reconciled — TOCTOU noted for a follow-up PR, the rest withdrawn).

## Notes

- **`--pack-dir` is unchanged** in this PR (stays `required=True`). The cleanup to default/remove it (and close the manifest-write TOCTOU) is deliberately deferred to a separate PR — preserved at tag `pack-dir-removal-wip` with a design doc.
- `origin/main` is **merged in** (resolved 2 conflicts; branch is current at v1.6.0).

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## 3. feat(agent-studio): /studio open imports published archives, restore pre-snapshot packs to built state (#162)

- **SHA**: `1ae626d6a54a56090dd6904b18c8d3cb56b8ee68`
- **Author**: felix-srp
- **Date**: 2026-06-04T11:38:38Z
- **Files Changed**: 5
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/1ae626d6a54a56090dd6904b18c8d3cb56b8ee68
- **PR**: #162

### Full Commit Message

```
feat(agent-studio): /studio open imports published archives, restore pre-snapshot packs to built state (#162)

Adds /studio open <archive|share-url> via new import_archive.py (reverse of package.py), restoring a pre-snapshot pack's source + scaffold-state + zip artifact + delivery proof + snapshot. Fixes the empty/placeholder-pack failure from LLM-improvised builds in deployed workspaces. SKILL.md guardrail + 14-test suite (104 pass). Bumps agent-studio 1.4.2 → 1.5.0.
```

### PR Description

## Why

When a creator wants to update an old pack that predates the snapshot mechanism (or whose snapshot was lost), `list_packs.py` returns it as unavailable and `/studio open <name>` can't restore it. With no legitimate update path, Studio's LLM improvised by `cd`-ing into the **deployed** agent's runtime workspace (`~/.openclaw/agents/<id>/`, `/workspace/<other>/`) and running `package.py` there.

That improvisation ships a broken pack:

- The deployed layout has `.agents/skills/` (runtime), not the `skills/` (pack-source) that `package.py` reads — so the archive contains **zero skills**.
- The deployed workspace has no `agent/*.md` pack-source, so Studio satisfies `package.py`'s required-files check by writing `(To be filled in by Agent Studio during Stage 3.)` placeholders into `agent/AGENTS.md` / `SOUL.md` / `IDENTITY.md` — and ships those placeholders to the catalog.

**Real-world repro:** a prod agent installed via this path ("Chanel Stylist") looked identical to the default chat — no skills, no persona — because the catalog archive was a ~2.5 KB shell. The fully-built `.agents/skills/` + root `.md` content was orphaned in the deployed workspace.

## What

### `/studio open <target>` — one command, dispatch by target shape

| Target shape | Treated as | Backed by |
|---|---|---|
| `https://` artifacts URL (or its base64) | share URL | `import_archive.py --share` |
| local `.tar.gz` / `.tgz` path | local archive | `import_archive.py --archive` |
| anything else | snapshot name | `snapshot.py restore` |

A snapshot name not in `list_packs.py` errors with the available names — it does **not** fall through to "treat as archive" (never what a typo meant). The `--share` URL is validated against the Studio artifacts CDN shape (`https://artifacts.<host>/[<bot>/<agent>/]artifacts/shares/<name>-<version>.tar.gz`); arbitrary URLs are refused.

### `import_archive.py` — reverse of `package.py`

Maps the archive back into Studio's workspace:

| archive | → workspace |
|---|---|
| root `*.md` / `agent-pack.yaml` / `description.json` | `agent/*` |
| `.agents/skills/<n>/…` | `skills/<n>/…` |
| `scripts/…`, `data/…` | same path |
| `artifacts/avatar.png` (or legacy root) | `agent/avatar.png` |

### Restores the pack to its built *state*, not just its files

After extraction the import reconstructs the signals Studio uses to recompute "current stage" — which otherwise never travel inside a pack archive, so a re-imported published pack used to drop back to **Stage 4 (Testing)**:

- `data/.scaffold-state.json` — `agent_dir_filled` true, or **false + warning** when the archive still ships Stage-3 placeholders (the direct guard against the chanel-stylist failure mode above).
- `zip/<name>-<version>.tar.gz` — the archive is restored as the publish artifact → recognized as **already packaged**.
- `data/.delivery-state.json` — for `--share`, the artifacts URL is durable proof of prior delivery, so the delivery record is rebuilt (via the shared `write_delivery_state`) → resumes at **done**. A local `--archive` proves packaging only → resumes at **Stage 6**. A placeholder pack is never marked delivered.
- an initial **snapshot** so the next `/studio open <name>` takes the fast snapshot path and the pack shows in `/studio list`.

The two stage-marker restores are soft-fail: the pack source is already committed, so a copy/write error only costs the stage promotion and surfaces an actionable warning.

### Safety

Layout is enforced by the existing `assert_archive_layout` contract (rejects symlinks, hardlinks, absolute paths, parent traversal, forbidden top-level `agent/`/`skills/`/`package/`). Extraction stages into a temp dir then does an atomic per-top-level-dir move-aside + `os.replace` with rollback. Decompression-bomb cap (256 MiB uncompressed); remote downloads reuse `install.py`'s 64 MiB cap + 30 s timeout, HTTPS-only.

### Guardrail (SKILL.md)

Adds **"Build and pack only in Studio's own workspace"** — every script `--pack-dir` must resolve to Studio's workspace, never a deployed agent's. `/studio open <archive>` is named as the legitimate "old pack, no snapshot" path. The Truth-sources section records `import_archive.py` as a writer of both `.scaffold-state.json` and (for `--share`) `.delivery-state.json`. BOOTSTRAP.md option (c) describes the unified `<target>` form.

## How tested

`import_archive.py` test suite — 14 tests; full agent-studio suite **104 pass**:

- **Round-trip:** `package.py` → `import_archive.py` preserves pack source byte-for-byte; a sync test asserts the import layout map can't drift from `package.py`'s `_AGENT_PACKABLE`.
- **Stage restore:** `--archive` import lands `zip/<v>.tar.gz` and writes no delivery-state; `--share` import additionally writes delivery-state with the real `share_url`; a placeholder pack via `--share` is left unmarked.
- **`--share` validation:** accepts the real artifacts URL (short + full `bot/agent` form) and its base64; rejects wrong host / wrong path / bad filename / `http` / missing version.
- **Refusals:** path-traversal name, non-conforming filename, dirty workspace, `.mode == test`, pre-existing symlink.
- **Placeholder:** archive shipping `(To be filled…)` → `agent_dir_filled=false` + warning.

Also verified end-to-end in a devcontainer against the real prod artifact (`plh-merchandiser-0.1.0` via its share URL): restores `zip/` + delivery-state, and `/studio list` shows it **✅ Delivered**.

## Not in scope

- A `package.py`-side check that rejects placeholder `(To be filled…)` agent files at pack time — belt-and-braces on top of the import path's detection. Follow-up.
- Legacy-avatar restaging for share URLs (`install.py`'s `_restage_remote_if_legacy`). Import accepts the URL; it just doesn't normalize legacy avatar layouts. Follow-up.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

