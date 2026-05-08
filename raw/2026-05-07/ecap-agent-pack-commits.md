# ecap-agent-pack commits - 2026-05-07

## e6c12cf9 - fix(agent-studio): /studio install — correct API contract, dry-run check, manifest expansion (#116)

- **SHA**: e6c12cf9b821b34c6051e268315d1a56c65e38e1
- **作者**: felix-srp
- **日期**: 2026-05-07T08:52:15Z
- **PR**: #116 https://github.com/SerendipityOneInc/ecap-agent-pack/pull/116

### Commit Message

```
fix(agent-studio): /studio install — correct API contract, dry-run check, manifest expansion (#116)

* fix(agent-studio): align /studio install with remote + base64 API contract

The install API rejects the local-filesystem path_types the script was
sending (`file`/`url`) and requires `path_type="remote"` with a
base64-encoded HTTPS URL as `path_value`. /studio install was failing
until the running agent hot-patched the script in place.

- Always emit `path_type="remote"` + base64(URL) on the install payload.
- For `current`/`local` sources, stage the archive into `artifacts/shares/`
  via `agent-studio-share`'s `run_share.py`, then use the public URL.
- For `remote` source, base64-encode the input URL.
- Forward `--artifacts-base-url` to the staging step.
- Make `normalize_path_value` and the version helpers base64-decode
  `remote` payloads before parsing the archive filename.
- Document the new API payload contract in the install SKILL.md.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(agent-studio): simplify install.py + compact SKILL.md

- Drop dead `run_publish_script` (no longer called after rerouting through
  `agent-studio-share`'s `run_share.py`).
- Reduce `decode_path_value` to a 4-line wrapper around the existing
  `try_decode_share_text` helper, keeping a single base64-decode
  implementation. Always returns a `str` so call sites lose the
  `or candidate` fallback.
- Drop the WHAT-not-WHY comment on `source_info_from_archive`; the
  conditional is self-explanatory.
- Compact SKILL.md "API payload" section to one line — the runtime LLM
  doesn't need the env-var fallback chain or implementation details.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): surface path_type migration, dry-run preview, host-safe URL

Three fixes from Claude + Codex review of the install rewrite:

1. **Legacy path_type cards no longer silently reuse against new payloads.**
   `determine_card_action` previously short-circuited on `same_version` even
   when `existing_path_type != source_info.path_type`. After this PR's
   payload migration, a user upgrading from a pre-PR install would have
   their broken `file`-typed card reused instead of replaced. Surface as
   `needs_confirmation` with reason `path_type_migration` so the creator
   chooses reuse vs. replace.

2. **`--check-only` is once again a true dry-run.** Staging
   (`run_publish_script` + copy into `artifacts/shares/`) now happens only
   when the user actually commits to the install. Check-only computes the
   would-be share URL via a new `project_share_url` helper that mirrors
   `agent-studio-share`'s URL math, so conflict detection stays accurate
   without touching the filesystem. `--source local` previews no longer
   stage third-party archives into the user's HTTPS-served artifacts/.

3. **`list-sources` stops exposing fake API fields.** `path_type`/
   `path_value` are install-time payload fields; `list-sources` is a
   discovery endpoint that doesn't yet know the staged URL. Emitting them
   as `file`/`<local-path>` was misleading the LLM into describing the
   install with values that don't match the actual API call.

Plus: fix a pre-existing bug in `run_share.py`'s `normalize_artifacts_base_url`
where `partition("/artifacts")` would match inside an `artifacts.*` hostname
and corrupt the URL (e.g., `https://artifacts.example.com/x/artifacts` →
`https://artifacts`). Now operates on the URL path only via `urlparse`.

Verified via 7 conflict-detection scenarios + 8 hostname normalization cases.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): tighten URL normalization, restore absolute locator path

Codex follow-up review caught two real bugs in the previous commit's
`normalize_artifacts_base_url` rewrite:

1. **Multiple `/artifacts` segments**: `rfind` keeps the LAST occurrence,
   but the original `partition("/artifacts")` semantic was the FIRST. So
   `https://example.com/artifacts/v2/artifacts/shares` returned
   `.../artifacts/v2/artifacts` instead of the canonical `.../artifacts`.
   Switched to `find`.

2. **Scheme-relative URLs (`//host/path`)**: my `if parsed.scheme:` gate
   skipped reconstruction for scheme-less URLs, dropping the host. Now
   rebuilds whenever scheme OR netloc is present.

Plus restore `archive_path.resolve()` in `source_info_from_current_pack`
so the preview's `locator_value` stays absolute when `--output zip/` is
relative (regressed from the prior commit's two-branch refactor).

14 normalization cases + 7 conflict-detection scenarios pass.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): expand agent-pack.yaml to scaffold-output format

Previously the manifest had only `name` + `version`. Fill it out to match
the format `scripts/scaffold.py` produces for a Stage-3-completed pack —
display_name, description, persona, skills, automation, onboarding,
dependencies — so the manifest reads as a real installable pack rather
than a stub.

Skills list reflects the three runtime skills shipped with Agent Studio:
agent-studio (driver), agent-studio-share, agent-studio-install. Persona
fields lifted from the root SOUL.md / IDENTITY.md. validate.py manifest
check now passes (was failing on missing `display_name` / `description`).

The leftover `check_skills` failure ("No skills/ directory") is a
pre-existing repo-layout issue (skills live under .agents/skills/), not
addressable in the manifest itself.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): bump version to 1.0.1

The 1.0.0 install flow was broken end-to-end (wrong API payload). This
release is the first that lets `/studio install` actually complete on
the current ZooClaw API without manual hot-patching.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

`/studio install` was failing in production: the install CLI sent the wrong payload shape, so the deployed agent had to hot-patch the script mid-conversation across 4 attempts to complete a single install.

This PR aligns the script with the actual install API contract, adds the safety nets the prior version was missing, fixes a pre-existing URL helper bug exposed along the way, and brings `agent-pack.yaml` up to the scaffold-output format.

## What was broken

1. **Wrong API payload.** Script sent `path_type="file"` (local) or `path_type="url"` (remote) with a raw filesystem path / plain URL. The install API only accepts `path_type="remote"` with a **base64-encoded HTTPS URL** as `path_value`, and rejects local filesystem paths altogether.
2. **No staging.** Local archives weren't HTTPS-served, so even if `path_type` were correct, the API server couldn't reach the file.
3. **Conflict detection lied for legacy cards.** `determine_card_action` short-circuited on `same_version` even when `path_type` had migrated, so a user upgrading from a pre-PR install would silently reuse a stale `file`-typed card.
4. **`--check-only` had real side effects.** Even a "dry-run" preview ran `publish.py` and copied the archive into the user's HTTPS-served `artifacts/shares/` before any user confirmation.
5. **`list-sources` exposed fake API fields.** Output included `path_type="file"` + raw paths that didn't match the actual install payload — misleading the LLM consumer.
6. **Pre-existing `normalize_artifacts_base_url` bug** (in `run_share.py`) corrupted any URL whose hostname contained `artifacts` (e.g., `https://artifacts.example.com/x/artifacts` → `https://artifacts`) because `partition("/artifacts")` matched inside the host. Newly reachable from `install.py` after this refactor.
7. **`agent-pack.yaml` was a 2-line stub** missing every field the publish/scaffold format documents.

## What changed

### `install.py` — API contract & flow

- Always emits `path_type="remote"` + base64-encoded HTTPS URL.
- `current` and `local` sources auto-stage into `artifacts/shares/` via `agent-studio-share`'s `run_share.py` and use the resulting public URL.
- `remote` source base64-encodes the input share URL or share text.
- New `--artifacts-base-url` flag, forwarded to the staging step. Same resolution chain as `/studio share` (flag → `ECAP_ARTIFACTS_BASE_URL` / `ARTIFACTS_BASE_URL` → `TOOLS.md`).
- `normalize_path_value`, `version_from_source_path`, `parsed_version_from_source_path` now base64-decode `remote` payloads before parsing.
- `decode_path_value` is a 4-line wrapper around the existing `try_decode_share_text`; returns input unchanged for legacy plain-URL payloads (so symmetric comparison still works against API responses).
- Dropped dead `run_publish_script` (no longer reachable after share-script rerouting).

### `install.py` — safety nets from review

- `determine_card_action` surfaces `needs_confirmation` with `reason="path_type_migration"` whenever the existing card's `path_type` differs from the new payload's. Users upgrading from broken legacy cards must explicitly choose reuse vs. replace.
- `--check-only` is once again a true dry-run: new `project_share_url` helper computes the would-be share URL deterministically (mirroring `agent-studio-share`'s URL math) without touching the filesystem or running publish. Conflict detection stays accurate because the projected URL is identical to the staged URL.
- `list_sources` strips `path_type`/`path_value` from emitted entries via `_strip_install_payload`. Those fields only apply at install time once the artifacts URL is resolved.

### `run_share.py` — URL helper hardening

- `normalize_artifacts_base_url` rewritten with `urlparse` to operate on the URL path component only — `artifacts.*` hostnames no longer corrupt the URL.
- Uses `find` (first occurrence) to match the original `partition` semantic when truncating extra path segments.
- Rebuilds the URL whenever scheme OR netloc is present, so scheme-relative URLs (`//host/...`) keep their host.
- Verified against 14 cases (port, userinfo, scheme-relative, multiple `/artifacts`, path-only, etc.).

### Manifest & docs

- `agent-pack.yaml` expanded from 2 lines to the full scaffold-output format: `display_name`, `description`, `tags`, `icon`, `lang`, `persona`, `skills` (the three runtime skills with descriptions and script lists), `automation`, `onboarding`, `dependencies`, `data_templates`. `validate.py` `manifest` check now passes.
- `agent-studio-install/SKILL.md` adds a one-line "API payload" note (compacted aggressively — every line in this file loads into runtime context).

## Verification

- 7 conflict-detection scenarios pass: `same_source`, `same_version`, `version_conflict`, `path_type_migration` for both `file` and `url` legacy types, `create`, `same_source` against API-returned plain-URL payload.
- 14 URL-normalization scenarios pass: with/without `/artifacts` suffix, `artifacts.*` hostname, port, userinfo, scheme-relative, multiple `/artifacts`, path-only, empty/None.
- `--check-only` makes zero filesystem writes; subsequent real install correctly stages.
- Projected URL (check-only) === staged URL (real install) — bit-for-bit identical.
- `list-sources` JSON no longer carries `path_type`/`path_value`.
- Two parallel review passes (Claude + Codex) — all flagged bugs addressed; final pass returned no high-confidence issues.

## Test plan

Verified locally on macOS arm64:
- [x] Unit-style scenario tests for `determine_card_action` (7 cases) and `normalize_artifacts_base_url` (14 cases)
- [x] `install.py list-sources` — JSON shape correct, no leaked `path_type`/`path_value`
- [x] `install.py install --source current --check-only` — auth-rejected at expected step, **zero filesystem writes**
- [x] `install.py install --source current` (real install path) — stages archive into `zip/` and `artifacts/shares/`, then attempts API call
- [x] Projection URL (check-only) === staging URL (real install), bit-for-bit
- [x] `validate.py --pack-dir .` — `manifest` check now passes

Verified inside `ghcr.io/serendipityoneinc/openclaw-docker:2026.4.2.12` (linux/amd64, the actual deployment image):
- [x] Both scripts parse cleanly under the runtime's Python + `uv`
- [x] All 7 conflict-detection scenarios pass
- [x] All URL normalization scenarios pass (incl. `artifacts.*` hostname + scheme-relative URL)
- [x] `list-sources` JSON omits `path_type`/`path_value`
- [x] `install --check-only` auth-rejects without touching `zip/` or `artifacts/`
- [x] `install --source current` correctly stages `agent-studio-1.0.1.tar.gz` into both `zip/` and `artifacts/shares/`

Not covered from this sandbox (token available was scoped to APIClaw/proxy services, not `zooclaw.ai` agent-catalog):
- [ ] End-to-end live install against `zooclaw.ai` — verify the create-card POST accepts the new payload and the async install op completes
- [ ] `--source remote` with a real share URL/text — verify base64 round-trip
- [ ] Install once, then again — confirm `same_source` reuse path
- [ ] Install against an account holding a legacy `path_type="file"` card — confirm `path_type_migration` surfaces and `--conflict-action replace` recovers

The deployed agent's failing trace (which motivated this PR) already showed the create-card API accepting the `path_type=remote` + base64 payload — the install completed successfully after the agent hot-patched the script to that exact shape. This PR just makes the script emit it on first try.

## Caveats

- The API contract was deduced from the deployed agent's failing trace — there is no spec accessible from this sandbox. The conservative path (`path_type="remote"` + base64) is what was observed to succeed end-to-end. The deployed agent also mentioned `import_url` as another accepted type; this PR doesn't use it.
- Existing private cards created before this PR (with `path_type="file"`) will surface as `path_type_migration` and require an explicit `replace`. That's intentional — silent reuse against a stale schema is what was broken before.
- The `validate.py` `check_skills` failure ("No skills/ directory") is a pre-existing repo-layout issue (Agent Studio's runtime skills currently live under `.agents/skills/`) and is out of scope for this PR.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## e7c16014 - chore(tvc-studio): sync to 0.3.9 (Chinese description + BGM catalog) (#117)

- **SHA**: e7c16014bac8e8a1754ae8e7bd299600ebdd1771
- **作者**: vincent-srp
- **日期**: 2026-05-07T06:20:59Z
- **PR**: #117 https://github.com/SerendipityOneInc/ecap-agent-pack/pull/117

### Commit Message

```
chore(tvc-studio): sync to 0.3.9 (Chinese description + BGM catalog) (#117)

- Bump version 0.3.5 → 0.3.9 to match upstream tarball
- Switch agent-pack.yaml description from English to Chinese (matches build/tvc-studio-0.3.9.tar.gz)
- Add data/bgm-r2/catalog.jsonl (886 tracks, ~530KB) — required by skills/tvc-post/scripts/fetch_bgm.py
- Preserve assets/fonts/ locally (still referenced by tvc-post SKILL.md, intentionally not in upstream tarball — same convention as PR #108)

Verified `diff -rq` against extracted 0.3.9 tarball shows only the expected assets/ delta.

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary
- 把 `tvc-studio` 同步到上游 `build/tvc-studio-0.3.9.tar.gz`
- `agent-pack.yaml`：版本 `0.3.5` → `0.3.9`；description 由英文切换为中文（与上游打包一致）
- 新增 `data/bgm-r2/catalog.jsonl`（886 条 BGM 元数据，~530KB），`skills/tvc-post/scripts/fetch_bgm.py` 直接读取该路径
- `assets/fonts/` 继续仅保留在仓库，不进 tarball（沿用 PR #108 的约定，仍被 `tvc-post/SKILL.md` 引用做字幕字体）

## 校验
- `.agents/` 下所有 skill 文件与 0.3.9 tarball 字节一致（解包后 `diff -rq` 无差异）
- 应用改动后 `diff -rq tvc-studio /tmp/tvc-studio-0.3.9-extract` 仅剩预期的 `assets/` 差异
- `agent-pack.yaml` 通过 `yaml.safe_load` 解析正常，version=0.3.9，skills 数=6

## Test plan
- [ ] 本地 `openclaw install ./tvc-studio` 安装无报错
- [ ] `fetch_bgm.py` 能从 `data/bgm-r2/catalog.jsonl` 命中 BGM 并下载
- [ ] `tvc-post` 字幕渲染仍可读取 `assets/fonts/CormorantGaramond-Light.ttf`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

