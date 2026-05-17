# ecap-agent-pack Commits — 2026-05-16

共 1 条 commits

---

## [1] fix(agent-studio): bug-recovery batch + avatar handoff for ecap-workspace #1714 (#127)

- **SHA**: `18b46f46d00bedfb937add81c3dbdfee7466f495`
- **作者**: felix-srp
- **日期**: 2026-05-16T17:16:01Z
- **PR**: #127

### 完整 Commit Message

```
fix(agent-studio): bug-recovery batch + avatar handoff for ecap-workspace #1714 (#127)

* fix(agent-studio): scrub git-recovery signals from migrate_manifest dev-startup output

The 1.2.1 hotfix's legacy-root recovery path emits JSON to stdout at every
dev-mode session start (AGENTS.md runs migrate_manifest.py). Its previous
output surfaced `action: "restored_from_git"` and `source: "HEAD:<file>"`,
which the agent appears to read as "this workspace is git-tracked" and
then attempts a between-stage `git commit`, surfacing the user-visible
"workspace isn't a git repo, so commit failed" prompt.

Keep the recovery logic intact (still load-bearing for any straggler
workspace that hasn't run a 1.2.1 dev session yet) but rename the helpers
to `_recover_legacy_{bytes,text}`, switch the output action to a neutral
`recovered`, drop the `HEAD:<file>` source field, and trim the docstring
so no LLM-visible surface in agent-studio mentions git, HEAD, or restore.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): force designer skill for all image generation

Stage 5b's avatar instruction was a single soft sentence in references/
packaging.md ("Use designer skill with templates/avatar-prompt.md"), easy
for the agent to skim past and replace with its own image-gen instinct.
On prod we observed the agent calling Gemini directly ("Gemini needs
Google Cloud SDK") before falling back to gpt-image-2 — the designer
skill itself only uses the LiteLLM proxy, so the failure message can only
come from a direct google-genai / vertexai call that bypassed designer.

Hardens the guidance in two places:

- Top-level SKILL.md Rules (read every dev session): a new bullet that
  forbids direct image API/SDK calls and points all image generation —
  Stage 5b avatar and any other in-session image the creator requests —
  through the designer skill.
- references/packaging.md §5b: replaces the one-line designer mention
  with an explicit forbid-direct-calls paragraph plus a 4-step workflow
  (render prompt, invoke designer without specifying a model, send via
  message tool, copy to agent/avatar.png on confirmation).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* Revert "fix(agent-studio): force designer skill for all image generation"

This reverts commit 2abfbd2. The original §5b instruction was already
clear enough; adding louder prose doesn't fix the underlying bug, which
is the agent not being able to *see* the designer skill at runtime
(addressed in the next commit).

* fix(agent-studio): declare designer as an external skill dependency

The agent-studio manifest's `dependencies.external_skills` was an empty
list, which is the OpenClaw runtime's signal to gate every built-in
skill out of the workspace. That made the `designer` skill invisible at
Stage 5b — when the agent reached "Use designer skill with templates/
avatar-prompt.md" it had no designer to invoke and fell back to a
direct google-genai call, which surfaced as "Gemini needs Google Cloud
SDK" on the bot pod (no gcloud creds in the container).

Other packs that use designer (soulmate-pack, pptx-master) already
declare it the same way. One-line addition; no doc churn needed since
the existing §5b instruction is now actually executable.

* Revert "fix(agent-studio): declare designer as an external skill dependency"

This reverts commit 3201d45. `external_skills` in agent-pack.yaml is
internal description metadata, not a runtime allowlist — the agent-studio
agent on ZooClaw already loads all built-in skills (designer included)
regardless of this field. The Bug 2 root cause is elsewhere; declaring
the dependency was the wrong place.

* fix(agent-studio): reframe DEV/TEST mode bullets as identity, not tool scope

AGENTS.md's mode descriptions used "Follow X; ignore Y" framing (TEST's
variant said "Follow agent/ only"). The intent is identity / source-of-
truth selection between modes, but the surface form reads like a tool
scope directive — a strict-reading agent can extend it to "I should
only invoke the agent-studio skill, not other installed skills like
designer", which lines up with the observed Stage 5b behavior where the
agent bypassed designer and called google-genai directly.

Same length, no new bullets, no louder forbids — just swap "follow X;
ignore Y" → "you are X, defined by Y" so the framing is about who the
agent IS, not what it can USE.

* fix(agent-studio): use description.json for install card payload to prevent backend dedup miss

install.py required description.json to exist (refused to install
without it) but never actually read its contents — the private card it
POSTed was built from agent-pack.yaml's manifest fields. That sent
`name="coros-coach"` (the lowercase pack slug) and a yaml-level
description, while the backend's archive-derived catalog entry — which
the install operation creates from the same description.json inside the
archive — uses `name="COROS Coach"` (Title Case display_name) and the
richer `short_bio` / `bio`. The mismatch caused the platform to register
two records per install: the install.py-pushed card and an
archive-derived "from installed agent data" duplicate, which matches
the reported duplicate-card symptom across multiple users.

Read description.json once in `read_current_pack_preview` (which feeds
both list-sources discovery and the actual install) and overlay its
`name` / `short_bio` / `bio` fields onto the card payload. Falls back
to manifest fields when description.json is absent, malformed, or still
carrying TODO placeholders, so list-sources keeps working on fresh
workspaces. agent_id continues to come from the manifest slug (= the
backend's expected agentPack_id), so this is metadata-only — no API
contract change.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): stage avatar from archive and include avatar_url in install card payload

The install.py card payload sent `emoji` (a Unicode glyph) but no
`avatar_url` — the field the catalog schema actually uses to render the
card icon. Combined with the missing description.json overlay (prior
commit), the pre-created private card had only an emoji while the
backend's archive-derived entry resolved description.json's
`avatar_url: avatar.png` against the installed pack root — different
fields, separate records, and the visible card ends up icon-less
because neither alone produces a publicly addressable image at create
time.

Extract `avatar.png` from the staged archive (works for --source
current / local / remote uniformly — they all end up staged under
artifacts/shares/), copy it to `artifacts/avatars/<pack>-<version>.png`,
build a public URL with the existing `build_artifact_url` +
`resolve_artifacts_base_url` machinery, and add `avatar_url` to the
card POST payload. `project_avatar_url` is the side-effect-free
companion for `--check-only` — peeks at tarball member names without
extracting.

Falls back to "" (no `avatar_url` key in payload) when the archive has
no avatar.png, is unreadable, or the artifacts base URL can't be
resolved. SourceInfo gets one new field with a "" default, so existing
construction sites stay valid.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* Revert "fix(agent-studio): stage avatar from archive and include avatar_url in install card payload"

This reverts commit 55e85508e4684ab71bb8b80a914bd26fadc8b906.

* refactor: simplify description.json overlay and trim docstrings post-review

Tighten three things after a code-quality / efficiency pass on the
description.json overlay landed in 29b8338:

- Extract the `isinstance(...) && strip && skip TODO` pattern into a
  single `_clean_todo` helper. Collapses the name and short_bio/bio
  branches from 14 lines of nested ifs to a flat 7, and gives the TODO
  placeholder convention one source of truth instead of two duplicated
  call sites.
- Drop `Path.exists()` in `_read_description_json` and catch
  `FileNotFoundError` in the `try` block — eliminates a TOCTOU window
  and a redundant stat (the caller already gates on existence too).
- Trim the 5-line WHY comment above the overlay to 2 lines and drop the
  "Stage 5a" reference (it was leaking an external lifecycle term into
  a self-contained helper).
- Trim `_recover_legacy_bytes`'s docstring in migrate_manifest.py —
  the "used silently on first 1.2.1 session…" sentence is changelog
  prose that belongs in the PR description, not in a helper docstring.

No behavior change. Re-verified all five overlay paths
(complete / missing / TODO-only / partial / malformed JSON) and the
migrate_manifest no-op case.

* fix(agent-studio): separate display_name from name to preserve Stage 6 delivery-state match

Code review (Codex) caught a regression my Bug 3 fix introduced: I'd
overwritten `source_info.name` with the description.json display name
(e.g. "COROS Coach") for the card POST payload. But `source_info.name`
is also what `main()` writes to `data/.delivery-state.json` as
`pack_name`, and Stage 6 (SKILL.md "Current stage" rules) compares
that to the manifest's raw `name:` field (the slug "coros-coach"). The
two would drift apart and a successful `--source current` install
would keep being detected as undelivered, so Studio would re-prompt
Stage 6 forever.

Split the concept: `SourceInfo.name` stays the manifest slug (what
delivery-state and the agent_id contract care about); add a separate
`display_name` field for the card POST override. `build_private_card_
payload` uses `display_name or name`, so the dedup-matching fix from
the prior commit still applies to the visible card metadata.

Also (Claude reviewer): narrow `_read_description_json`'s except clause
from `(FileNotFoundError, json.JSONDecodeError, OSError)` to just
`(FileNotFoundError, json.JSONDecodeError)`. The original blanket
`OSError` would silently swallow `PermissionError` and similar on an
existing-but-unreadable description.json — the overlay would skip
without any signal, bringing the duplicate-card bug back invisibly. Let
genuine I/O failures propagate; only the legitimate "no file yet" and
"malformed JSON" cases are noop'd.

Verified: card POST gets `"COROS Coach"`, delivery_state writes
`"coros-coach"`, Stage 6 detector reads `"coros-coach"` from manifest —
match. PermissionError now surfaces from `_read_description_json`.

* fix(agent-studio): also noop IsADirectoryError in _read_description_json

Round-2 review (Claude) flagged: `_read_description_json` narrowed its
except list to `(FileNotFoundError, json.JSONDecodeError)` in the prior
commit, but `IsADirectoryError` is a separate `OSError` subclass — if a
creator ever ends up with `agent/description.json` as a directory, the
existence guard at `source_info_from_current_pack` passes (Path.exists()
returns True for a directory), `read_text()` raises IsADirectoryError,
the exception escapes through `read_current_pack_preview` and
`main()`'s outer envelope handler (neither lists it), and the script
exits with a raw traceback on stderr instead of the standard
`{"status": "error", ...}` JSON envelope callers expect.

Add IsADirectoryError to the noop tuple. PermissionError and other
genuine I/O failures still propagate — preserves the round-1 intent of
not silently masking environment-broken cases that would re-introduce
the duplicate-card bug.

Verified: directory-at-path now returns None and the install pipeline
falls back to manifest data cleanly; PermissionError still surfaces.

* fix(agent-studio): also noop NotADirectoryError and UnicodeDecodeError in _read_description_json

Round-3 review (Codex) flagged two more `OSError` subtypes worth
treating as fall-back-to-manifest signals, parallel to ones we already
catch:

- `NotADirectoryError` — pairs with `IsADirectoryError` (added round 2).
  Fires when an ancestor of `agent/description.json` is a regular file
  instead of a directory.
- `UnicodeDecodeError` — pairs with `json.JSONDecodeError`. Both are
  "the file content is bad" failures; both should fall back to manifest
  data rather than crash.

Declined Codex's broader suggestion to catch all `OSError` — that would
re-swallow `PermissionError`, which round-1 review specifically wanted
surfaced (silent regression of the duplicate-card bug otherwise).
PermissionError and other genuine I/O failures still propagate.

Verified 7 cases end-to-end: missing / directory / not-a-dir-parent /
bad-utf-8 / bad-json all return None; valid file returns dict;
PermissionError propagates.

* refactor: trim redundant comments in install.py post-review

Second simplify pass flagged two comment-overrun spots:

- The inline comment block in `read_current_pack_preview` restated the
  `name`-stays-manifest-slug invariant that `SourceInfo.display_name`'s
  dataclass field comment already documents. Drop the duplicated
  sentences; keep the dedup-match WHY (the part that's specific to
  this call site).
- `_read_description_json`'s 5-line prose explainer was over-narration
  for a 2-line try/except. Condense to a single-line WHY that still
  captures the propagate-vs-noop boundary.

No behavior change. Spot-checked overlay still produces the right
preview output.

* fix(agent-studio): pack avatar.png under artifacts/ in archive; never source from workspace artifacts/

Two coordinated changes that hand off cleanly to ecap-workspace PR #1714's
install/async avatar_url contract:

1. Archive layout (package.py / generate_description.py / IDENTITY.md
   rewrite): place avatar.png at `artifacts/avatar.png` inside the
   tarball instead of at archive root. After the platform unpacks at
   `/workspace/{agent_id}/`, the file lands at
   `/workspace/{agent_id}/artifacts/avatar.png` — the path the artifact
   CDN serves and PR #1714 patches into the catalog row as
   `https://artifacts.{host}/{bot_id}/{agent_id}/artifacts/avatar.png`.
   IDENTITY.md's `- **Avatar:**` markdown reference and description.json's
   `avatar_url` field both follow to the new relative path so they
   resolve correctly post-unpack.

2. Source-side guard (_common.find_pack_avatar / migrate_manifest._migrate_avatar):
   drop the `<pack_dir>/artifacts/avatar.png` fallback that both helpers
   previously honored. In the agent-studio meta workspace that path
   holds Studio's own avatar — packing it (or migrating it into
   agent/avatar.png) would publish Studio's icon as the user pack's.
   Only the canonical `<pack_dir>/agent/avatar.png` is recognized; the
   workspace-root legacy slot stays in migrate_manifest for upgrade
   recovery since that location never collided with Studio's files.
   validate.py's listing-assets comment refreshed to match.

Verified end-to-end in a workspace that simulates Studio's layout
(artifacts/avatar.png holds non-pack bytes): find_pack_avatar returns
None when agent/avatar.png is missing; packaging picks up only the
canonical file; migrate_manifest noops on Studio's artifacts/avatar.png.

* fix(agent-studio): apply Studio-avatar guard to clean.py and tighten avatar_url + insertion guard

Round-1 review (Claude + Codex) on the avatar handoff commit surfaced
four findings — three actionable, plus one scope-creep skip (CRLF in
the Avatar regex; bots run Linux). Both reviewers found related issues
to the prior commit's logical correction.

- `clean.py`: `/studio new` was wiping `artifacts/avatar.png` — which
  the prior commit established is Studio's own avatar in the meta
  workspace, not a pack artifact. The bulk-dirs sweep clears
  `artifacts/` wholesale before the listing-assets phase, so the fix
  needs both layers: add a `preserve` tuple to `_clear_dir` and pin
  `avatar.png` for the artifacts/ slot, and drop the explicit
  artifacts/avatar.png entry from listing_targets so we don't even try
  to re-delete it. `artifacts/shares/<pack>-<v>.tar.gz` archives still
  get wiped as before.

- `generate_description.py`: `avatar_url` was unconditionally set to
  `"artifacts/avatar.png"` even when no avatar exists yet — Stage 5a
  runs before Stage 5b, so a creator generating description.json
  before producing the avatar would emit a broken URL. Now uses
  `find_pack_avatar(pack_dir)` to fall back to `""` when no avatar is
  present.

- `package.py` (`_clean_agent_file` Avatar insertion fallback): the
  `elif "avatar" not in content.lower()` guard was too broad — any
  prose mention of "avatar" anywhere in IDENTITY.md suppressed
  insertion. Tightened to `re.search(r'^-\s*\*\*Avatar:\*\*', ...)` so
  the guard matches the field, not the word.

- `migrate_manifest.py`: docstring still listed `artifacts/avatar.png`
  as a migration source path; refreshed to reflect that path is
  intentionally never sourced (Studio's avatar lives there).

Skipped: Codex's backward-compat concern about pre-PR archives at root
(narrow window; re-running /studio publish regenerates layout) and the
CRLF line-ending concern (Linux-only environment).

Verified: generate_description with/without avatar produces correct
avatar_url; clean preserves artifacts/avatar.png while wiping
artifacts/shares/; Avatar insertion fallback no longer suppressed by
unrelated "avatar" prose.

* refactor: dedup symlink-escape guard + trim avatar-handoff comments

Simplify pass on the avatar handoff work flagged three things:

- Reuse: `package._within_pack` and the inline `try: resolve().relative_to / except ValueError` in `_common.find_pack_avatar` were the same 4-line guard. Hoist to `_common.is_within(path, root)`, import into `package.py`, drop the local function (its 4 call sites already use the same name post-rename).

- Quality: `clean.py`'s listing-assets phase had a 5-line comment explaining why `artifacts/avatar.png` is NOT in `listing_targets` — but the tuple no longer contains that entry, so the comment was narrating absence. Delete. The bulk-dirs sweep also had a 2-line preservation rationale that the same fact already states once via the `preserve=("avatar.png",)` argument; trim to one line.

- Quality: `generate_description.py`'s `avatar_url` had a 6-line WHY comment. The conditional + relative path are self-explanatory; collapse to one line that points at ecap-workspace PR #1714.

No behavior change. Verified end-to-end: package still places avatar at `artifacts/avatar.png`, `generate_description` still emits the conditional URL, `clean` still preserves Studio's avatar while wiping pack archives.

* chore(agent-studio): bump version 1.2.1 → 1.2.2

Patch bump for the bug-recovery batch in this PR — no new features,
five production-traced bug fixes plus the avatar handoff for
ecap-workspace #1714.

* fix(agent-studio): reject pre-1.2.2 root-level avatar.png in assert_archive_layout

Reviewer feedback (tim-srp on PR #127): this PR changed the avatar
archive layout from root-level `avatar.png` to `artifacts/avatar.png`
to match ecap-workspace PR #1714's CDN URL, but the archive-contract
validator from PR #122 wasn't updated to match. An archive with the
old root-level layout still passed `assert_archive_layout()`, so a
stale archive (built before this PR, reused via `/studio install
--source local`) would install successfully while the platform's
avatar URL silently 404'd.

Extend the validator to reject `avatar.png` at archive root, with a
re-publish hint in the error message. The check is positioned after
the existing REQUIRED_TOP_LEVEL_FILES enforcement and reuses the
already-computed `top_level_files` set, so it's O(1) added work.

Avatar is still optional — archives with no avatar entry continue to
pass (Stage 5b may not have run yet). Only the explicit pre-1.2.2
position is rejected.

Verified four cases:
- new layout (artifacts/avatar.png) → accepted
- old layout (avatar.png at root) → rejected with hint
- no-avatar archive → accepted
- package.py round-trip → archive passes its own post-pack self-check

* fix(agent-studio): migrate pre-1.2.2 root-level avatar in stage_archive_in_artifacts instead of rejecting

Follow-up to reviewer feedback (tim-srp): switch from "reject pre-1.2.2
archives" to "migrate them transparently". A user with a `zip/foo.tar.gz`
built before this PR no longer needs to re-run `/studio publish`;
installing via `--source local` (or sharing via `--source current`)
just works, with the avatar landing at the new path the platform CDN
expects.

- `_common.assert_archive_layout` no longer rejects root-level
  avatar.png. Both layouts (root and artifacts/) pass; layout
  correctness is enforced at stage-time instead of validate-time.

- `run_share.stage_archive_in_artifacts` now uses a new
  `_copy_or_migrate_avatar` helper instead of bare `shutil.copy2`. If
  the source tarball has `avatar.png` at root, the staged copy in
  `artifacts/shares/` is rewritten with the avatar at
  `artifacts/avatar.png`. Bytes preserved; member metadata (mode,
  mtime, uid/gid names) carried over; non-avatar members copied
  verbatim. Source archive at `zip/` is never mutated. If the archive
  has no avatar (or already has the new layout), `_copy_or_migrate_avatar`
  is a plain copy.

Verified three cases end-to-end:
- legacy archive (avatar.png at root) → staged copy has
  `artifacts/avatar.png` with preserved bytes; source untouched;
  staged copy passes `assert_archive_layout`.
- new-layout archive → identity copy.
- no-avatar archive → identity copy.

`--source remote` archives are NOT migrated (the path_value points at
the user's external URL, which we don't control). The platform's
avatar_url patch will 404 for those; install otherwise succeeds.

* refactor: tighten _copy_or_migrate_avatar and drop change-narration comments

Simplify pass on the migration helper from 9c23112:

- Flatten the 3-branch if/elif/else in the rewrite loop. The old shape
  duplicated `dst.addfile(member, src.extractfile(member))` and called
  `member.isfile()` twice per member. Now: build the output TarInfo via
  `copy.copy(member)` and override `.name` when migrating — preserves
  `type` / `uid` / `gid` / linkname / pax metadata that the prior
  manual attribute-copy block silently dropped. Single addfile call.

- Hoist `import tarfile` (and a new `import copy`) to module top with
  the other stdlib imports. Local imports are conventionally for
  expensive/optional deps; tarfile is neither.

- Trim the helper's docstring: drop the ecap-workspace PR #1714 pointer
  (the WHY — backend expects `artifacts/avatar.png` — stands on its
  own) and the path-narration about "into artifacts/shares/" (couples
  the helper to one call site).

- Drop the 4-line change-narration comment in `_common.py` after
  `assert_archive_layout`. The pre-1.2.2/post-1.2.2 history belongs in
  the commit message (9c23112) — the validator's behavior is
  self-explanatory.

No behavior change. Re-verified four cases: legacy migrated with bytes
+ mode (0o644) preserved, new-layout identity copy, no-avatar identity
copy, migrated archive passes assert_archive_layout.

* fix(agent-studio): tighten _copy_or_migrate_avatar — deep copy, collision guard, surface TarError

Three corrections from round-1 multi-reviewer pass on the migration
helper (claude + codex):

1. Use `TarInfo.replace(name=...)` instead of `copy.copy(member)` + set
   `.name`. `copy.copy` is shallow; `pax_headers` (a dict) is shared
   with the source member. `tarfile.TarFile.addfile` writes through
   `pax_headers["path"]` for names that exceed POSIX's 100-char limit
   — that path doesn't fire for `artifacts/avatar.png` (21 chars) but
   is a latent trap if someone later migrates a longer-named member.
   `TarInfo.replace` (Python 3.12+) deep-copies by default; drops the
   `import copy`.

2. Skip migration when the source archive already contains
   `artifacts/avatar.png` (in addition to a root-level `avatar.png`).
   The previous code would rename the legacy entry to the same path,
   producing two `artifacts/avatar.png` entries in the staged
   tarball; downstream extractors handle duplicate names
   inconsistently (some take first, some last). Now: if both layouts
   coexist, identity-copy and let the destination keep whatever the
   source had.

3. Re-raise `tarfile.TarError` from the inspection pass as a
   `RuntimeError`. The previous swallow-then-`shutil.copy2` path would
   silently copy a corrupt archive into artifacts/shares/, then the
   backend would fail opaquely. Both call paths (install.py,
   run_share main) run `assert_archive_layout` upstream, so reaching
   the helper with an unreadable archive means a race or fresh
   corruption — louder is better than silent.

Verified four scenarios: legacy migrates with bytes/mode/uid/gid/
uname/gname preserved; collision case (both layouts present)
identity-copies; replace() preserves all metadata fields; corrupt
source surfaces as RuntimeError.

* fix(agent-studio): migrate --source remote pre-1.2.2 archives by re-hosting on our CDN

Round-1 review (Codex, medium severity): `--source remote` lost layout
enforcement when `assert_archive_layout` stopped rejecting root-level
`avatar.png` (9c23112). The validator accepts both layouts so local
archives can be migrated at stage-time, but the remote path never
went through `_copy_or_migrate_avatar` — the external URL is what the
backend fetches, so a pre-1.2.2 remote archive would install with the
platform's avatar URL silently 404'ing.

Make remote symmetric with local: when the downloaded archive uses the
legacy avatar layout, re-host the migrated copy on our artifacts CDN
and use OUR URL as `path_value` instead of the user's external one.
New-layout archives keep the original external URL (no re-hosting
cost).

Plumbing:

- `source_info_from_remote_input` gains optional `pack_dir`,
  `artifacts_base_url`, `check_only` parameters (already available at
  the caller in `resolve_source_info`).
- New `_restage_remote_if_legacy` downloads, detects, and (on legacy)
  routes through `stage_archive_in_artifacts` from run_share, which
  reuses the same `_copy_or_migrate_avatar` helper used by
  `--source current` / `--source local`.
- Download logic factored into `_download_remote_archive_to` and
  shared between `_validate_remote_archive` and the new restage path.
  The duplicate transfer in the legacy case is intentional —
  threading a tmp path back from the validator would entangle two
  otherwise-independent checks; remote archives are size-capped at
  64 MiB.
- `check_only=True` skips migration (no filesystem side effects in
  preview mode); the preview shows the original external URL.

Verified end-to-end with a local HTTP server:
- legacy remote archive → path_value = our CDN URL; staged copy has
  `artifacts/avatar.png` (migrated).
- new-layout remote archive → path_value = original external URL (no
  re-hosting).
- check_only on legacy → path_value = original external URL (preview,
  no side effects).

* fix(agent-studio): normalize avatar member names with posixpath; re-raise on remote second-fetch failure

Round-2 review (codex):

- **Major:** `_copy_or_migrate_avatar`'s dedup check compared raw
  member names against `_AVATAR_NEW_PATH`. An archive that already
  used the new layout with a `./` prefix (`./artifacts/avatar.png`)
  would slip past `has_new` detection, so a legacy root `avatar.png`
  alongside it would still trigger the rewrite — producing a
  duplicate `artifacts/avatar.png` entry under the canonical
  spelling. Normalize all member names via `posixpath.normpath` so
  `./avatar.png`/`avatar.png` and `./artifacts/avatar.png`/
  `artifacts/avatar.png` collapse onto the canonical forms before the
  membership tests and the rewrite predicate.

  Same fix applied to `_restage_remote_if_legacy` in install.py:
  legacy detection uses `posixpath.normpath` instead of an explicit
  tuple of variants.

  Drops the `_LEGACY_AVATAR_ROOT_NAMES` tuple (in both files) for a
  single `_LEGACY_AVATAR_NORMALIZED = "avatar.png"` — the normalized
  form is the single source of truth.

- **Minor:** `_restage_remote_if_legacy` previously swallowed
  `tarfile.TarError` on the second download and returned `None`,
  silently falling back to the external URL. The first download
  already passed `assert_archive_layout`, so a tar error on the
  second fetch is a genuine anomaly (transient server misbehavior,
  split response, race). Re-raise as `InstallError` so the caller
  sees a clear error instead of installing with a CDN avatar URL
  that the platform expected to be migrated.

Verified three normalization scenarios:
- `./avatar.png` (legacy with dot-slash) → migrated to
  `artifacts/avatar.png`, source variant gone.
- `avatar.png` + `./artifacts/avatar.png` (collision under variant
  spelling) → identity-copy, no duplicate `artifacts/avatar.png`
  written.
- plain `avatar.png` → still migrates (regression check).

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Five coordinated fixes traced from a prod-bot diagnosis (`53bfc1d0-c619-42a2-abdd-6222e2c03dd0`, `claw.gsmo.ai`). Net diff: 8 files, +131/-120. Branch history has multiple revert pairs from review-loop iterations; squash-on-merge collapses cleanly.

### 1. Spurious "commit the workspace" prompt between stages

`migrate_manifest.py` runs at every dev-mode session start and emitted JSON with `action: "restored_from_git"` and `source: "HEAD:<file>"`. The LLM read those as a "this workspace is git-tracked" signal and tried to `git commit` between Stage 2 and Stage 3 ("I attempted to commit the workspace as required, but this workspace isn't a git repo, so commit failed").

Recovery logic stays intact, but every LLM-visible surface is scrubbed: helpers renamed `_git_show_root*` → `_recover_legacy_*`; action string `"restored_from_git"` → `"recovered"`; `source: "HEAD:<file>"` dropped; docstring trimmed.

### 2. Agent bypassed the `designer` skill, called Gemini SDK directly

`agent-studio/AGENTS.md`'s DEV/TEST mode bullets used "Follow X; ignore Y" framing — a strict-reading model extended it to tool-scope ("only use the agent-studio skill"). Rephrased to "you are X, defined by Y" so the framing is about identity, not tool scope.

### 3. Duplicate "from installed agent data" cards in the user's catalog

`install.py` POSTed a private card built from `agent-pack.yaml` fields (manifest slug name, yaml-level description). The backend's archive-derived catalog entry separately reads `agent/description.json` (display name, `short_bio`/`bio`) and registered as a second record because the data didn't match.

`install.py` now reads `description.json` and overlays its `name` / `short_bio` / `bio` into the card POST payload via a new `SourceInfo.display_name` field. The slug-shaped `SourceInfo.name` stays as-is so Stage 6's `.delivery-state.json` `pack_name` keeps matching the manifest `name:` field (Codex round-1 finding — would have caused re-prompts forever otherwise). New helpers: `_read_description_json` (narrow `except` tuple — `FileNotFoundError` / `IsADirectoryError` / `NotADirectoryError` / `UnicodeDecodeError` / `JSONDecodeError` noop'd; `PermissionError` and disk errors still propagate) and `_clean_todo` (skips `TODO:` placeholders that `generate_description.py` writes).

### 4. Avatar handoff to ecap-workspace [PR #1714](https://github.com/SerendipityOneInc/ecap-workspace/pull/1714)

PR #1714 patches the user's catalog row with `https://artifacts.{host}/{bot_id}/{agent_id}/artifacts/avatar.png` after install. The archive's existing layout (avatar at root) doesn't resolve to that URL. Four coordinated changes:

- **Archive layout** (`package.py` / `generate_description.py` / IDENTITY.md rewrite): write avatar.png at `artifacts/avatar.png` inside the tarball. After unpack at `/workspace/{agent_id}/`, the file lives where the CDN URL expects it. IDENTITY.md's `- **Avatar:**` markdown stub and description.json's `avatar_url` field follow the new relative path. `avatar_url` is conditionally emitted (`""` when no avatar yet, so Stage 5a doesn't advertise an asset Stage 5b hasn't produced).
- **Source-side guard** (`_common.find_pack_avatar` / `migrate_manifest._migrate_avatar`): drop the `<pack_dir>/artifacts/avatar.png` fallback. In the agent-studio meta workspace that path holds **Studio's own avatar**, not the pack being built — the old fallback would have packed Studio's icon into user packs (or migrated it into `agent/avatar.png` on first dev session). Only the canonical `<pack_dir>/agent/avatar.png` is recognized now.
- **Clean-time preservation** (`clean.py`): `/studio new` was wiping `artifacts/avatar.png` (= Studio's avatar) via the bulk `artifacts/` sweep. `_clear_dir` gained a `preserve` tuple; the artifacts/ entry passes `("avatar.png",)`. `artifacts/shares/<pack>-<v>.tar.gz` archives still get wiped.
- **Avatar insertion guard** (`package._clean_agent_file`): the fallback that inserts `- **Avatar:**` into IDENTITY.md when missing now uses `re.search(r'^-\s*\*\*Avatar:\*\*', ...)` instead of `"avatar" not in content.lower()` — matches the field, not the word, so prose mentioning "avatar" no longer suppresses insertion.

### 5. Symlink-escape helper consolidation

`_within_pack(path, pack_root)` in `package.py` and the inline `try: resolve().relative_to / except ValueError` in `_common.find_pack_avatar` were the same 4-line guard. Hoisted to `_common.is_within(path, root)`; both call sites use it now (one helper, not two).

## Out of scope (filed separately as platform follow-ups)

The two backend-side bugs surfaced in the same diagnosis — per-version workspace + agent_id accumulation (`custom-coros-coach-0-1-X` proliferation) and the `install/async` operation reporting `failed` while async work succeeds — live in `ecap-workspace`. PR #1714 addresses them; this PR is the client-side handoff. Design doc: `~/workspace/design-doc/ecap-agent-pack/agent-studio/2026-05-15-install-endpoint-platform-followups.md`.

## Test plan

- [x] All scripts compile (`python3 -m py_compile`)
- [x] `migrate_manifest.py` Case A (move legacy root manifest) + Case C (noop) verified; `artifacts/` source no longer considered for avatar migration
- [x] `_read_description_json` 7 paths verified (missing, directory, parent-not-a-dir, bad UTF-8, bad JSON, valid, permission-denied)
- [x] `read_current_pack_preview` overlay verified (full description.json / no file / all-TODO / partial / malformed)
- [x] `SourceInfo.display_name` vs `name` split — card POST uses display name, `write_delivery_state` writes manifest slug, Stage 6 detector still matches
- [x] Avatar archive layout — empirical tar listing shows `artifacts/avatar.png`; IDENTITY.md and description.json both updated to match
- [x] Studio-shaped workspace simulation — `find_pack_avatar` returns `None` instead of Studio's avatar; packaging only sources `agent/avatar.png`; migrate_manifest noops on Studio's `artifacts/avatar.png`; `clean.py` preserves Studio's avatar while wiping pack archives in `artifacts/shares/`
- [x] `generate_description.py` — `avatar_url` is `""` when no avatar present, `"artifacts/avatar.png"` once Stage 5b produces it
- [x] `_clean_agent_file` Avatar fallback insertion no longer suppressed by unrelated "avatar" prose in IDENTITY.md
- [ ] Verify on a real bot: ramp through `/dev` → Stage 5b avatar via designer skill → confirm card has correct icon and no duplicate after install

## Review

Cleared a 6-round multi-reviewer (Claude + Codex) loop across two scope phases:

**Phase 1 (bugs 1-3):**
- Round 1: Codex caught `SourceInfo.name` overload that would have broken Stage 6 delivery-state. Claude caught `OSError` too-broad swallow that would have silently regressed Bug 3 on permission failures.
- Round 2: Claude caught `IsADirectoryError` escaping `main()`'s envelope handler.
- Round 3: Codex caught two more `OSError` subclasses worth treating as noop (`NotADirectoryError`, `UnicodeDecodeError`).
- Round 4: both clean.

**Phase 2 (avatar handoff):**
- Round 1: Claude caught `clean.py` wiping Studio's avatar on `/studio new`, `generate_description.py` unconditional `avatar_url`, stale `migrate_manifest.py` docstring. Codex caught too-broad `"avatar" in content.lower()` substring guard.
- Round 2: both clean.

Plus three simplify passes consolidating helpers (`_clean_todo`, `is_within`) and trimming over-prose comments.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

