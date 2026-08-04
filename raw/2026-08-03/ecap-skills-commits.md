# SerendipityOneInc/ecap-skills commits — 2026-08-03

## ci: Publish skills to engine registry on staging (#252)

- **SHA**: `810ab23815942d3ae3f32462d4cf75ab631c6541`
- **作者**: bill-srp
- **日期**: 2026-08-03T11:26:44Z

### Commit Message

```
ci: Publish skills to engine registry on staging (#252)

## Summary

Follow-up to SerendipityOneInc/ecap-workspace#3198 (merged): use the new
CI-only `POST /skills/registry-publish` claw-interface endpoint from
this repo's publish workflow, so global skills land in the v2 engine
registry.

**What changed in `publish-skills.yml`:**
- **staging only**: after the existing S3 sync, a new "Publish skills to
engine registry" step loops `PUBLISHED_SKILLS`, zips each skill
directory (top-level dir kept — the engine strips it and enforces the
`SKILL.md` frontmatter name match), and POSTs it with
`X-Skills-Publish-Token`, `name=<dir>`,
`source_label=ecap-skills@<tag>`. `curl --fail-with-body` fails the job
on any per-skill error with the engine's actionable message; `--retry 3`
is safe because the engine dedups versions by content hash.
- **Dual-write (decision)**: the full S3 sync (whitelist + `--delete`)
stays as-is on all tiers. `_fonts` / `_BGM` are shared asset libraries
with no `SKILL.md` — consumed at runtime from the `/extra-skills`
JuiceFS mount (e.g. `_BGM/scripts/resolve_bgm.py` hardcodes
`/extra-skills/_BGM`) — so they are skipped by the registry step and
remain S3-only. Any whitelisted-but-missing directory now fails the
registry step instead of being silently skipped.
- **dev and production (decision)**: unchanged, S3-sync only. `-alpha`
and `-release` tags do not touch the registry; production adoption can
follow later by copying the staging step.
- Lark notify on staging now includes the registry base URL.
- README: documented the registry publish path and required staging
config.

**Required environment configuration before merge takes effect**
(`staging` GitHub environment — neither entry exists yet):

| Kind | Name | Value |
|------|------|-------|
| Variable | `SKILLS_PUBLISH_BASE_URL` | staging claw-interface base URL
|
| Secret | `SKILLS_PUBLISH_TOKEN` | same value as claw-interface's
`AGENT_STUDIO_PACK_UPDATE_TOKEN` (shared CI credential per spec
decision) |

Until these are set, the registry step fails fast with a clear error
(after the S3 sync has already completed, so the legacy path is
unaffected).

## Test plan

- [x] Workflow YAML parses; step order per job verified (dev/prod: sync
→ notify; staging: sync → registry publish → notify)
- [x] Local dry-run of the publish loop against the real
`PUBLISHED_SKILLS`: 21 skills zipped, `_fonts`/`_BGM` skipped, every zip
has a single top-level dir containing `SKILL.md`, largest zip 2.4 MB (50
MiB endpoint cap)
- [ ] After merge + env config: push a `v*-beta` tag and verify each
skill returns a `SkillVersion` and re-running the workflow is a
content-hash no-op

## Related

- API: SerendipityOneInc/ecap-workspace#3198
- Design spec:
`docs/superpowers/specs/2026-08-03-skills-registry-publish-api-design.md`
(ecap-workspace)
```

### PR Body

```
## Summary

Follow-up to SerendipityOneInc/ecap-workspace#3198 (merged): use the new CI-only `POST /skills/registry-publish` claw-interface endpoint from this repo's publish workflow, so global skills land in the v2 engine registry.

**What changed in `publish-skills.yml`:**
- **staging only**: after the existing S3 sync, a new "Publish skills to engine registry" step loops `PUBLISHED_SKILLS`, zips each skill directory (top-level dir kept — the engine strips it and enforces the `SKILL.md` frontmatter name match), and POSTs it with `X-Skills-Publish-Token`, `name=<dir>`, `source_label=ecap-skills@<tag>`. `curl --fail-with-body` fails the job on any per-skill error with the engine's actionable message; `--retry 3` is safe because the engine dedups versions by content hash.
- **Dual-write (decision)**: the full S3 sync (whitelist + `--delete`) stays as-is on all tiers. `_fonts` / `_BGM` are shared asset libraries with no `SKILL.md` — consumed at runtime from the `/extra-skills` JuiceFS mount (e.g. `_BGM/scripts/resolve_bgm.py` hardcodes `/extra-skills/_BGM`) — so they are skipped by the registry step and remain S3-only. Any whitelisted-but-missing directory now fails the registry step instead of being silently skipped.
- **dev and production (decision)**: unchanged, S3-sync only. `-alpha` and `-release` tags do not touch the registry; production adoption can follow later by copying the staging step.
- Lark notify on staging now includes the registry base URL.
- README: documented the registry publish path and required staging config.

**Required environment configuration before merge takes effect** (`staging` GitHub environment — neither entry exists yet):

| Kind | Name | Value |
|------|------|-------|
| Variable | `SKILLS_PUBLISH_BASE_URL` | staging claw-interface base URL |
| Secret | `SKILLS_PUBLISH_TOKEN` | same value as claw-interface's `AGENT_STUDIO_PACK_UPDATE_TOKEN` (shared CI credential per spec decision) |

Until these are set, the registry step fails fast with a clear error (after the S3 sync has already completed, so the legacy path is unaffected).

## Test plan

- [x] Workflow YAML parses; step order per job verified (dev/prod: sync → notify; staging: sync → registry publish → notify)
- [x] Local dry-run of the publish loop against the real `PUBLISHED_SKILLS`: 21 skills zipped, `_fonts`/`_BGM` skipped, every zip has a single top-level dir containing `SKILL.md`, largest zip 2.4 MB (50 MiB endpoint cap)
- [ ] After merge + env config: push a `v*-beta` tag and verify each skill returns a `SkillVersion` and re-running the workflow is a content-hash no-op

## Related

- API: SerendipityOneInc/ecap-workspace#3198
- Design spec: `docs/superpowers/specs/2026-08-03-skills-registry-publish-api-design.md` (ecap-workspace)
```

---
