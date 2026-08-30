# SerendipityOneInc/ecap-workspace — commits 2026-08-29

## fix(claw-interface): transcode tar.gz pack bundles to zip for the bootstrap lane (#3592)

- **SHA**: `f245b71828206b2ecbfc6dc010614ab472e01647`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-29T09:53:21Z
- **PR**: #3592

### Commit Message

```
fix(claw-interface): transcode tar.gz pack bundles to zip for the bootstrap lane (#3592)

Follow-up to #3590. With the export now running inside the production
cluster, the first end-to-end run
([33244589405](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/33244589405))
got a **clean export** — pod started, RBAC sufficient, Mongo, R2 and the
avatar all read, a 307 KB bundle produced — and then the import stopped
before its first request:

```json
{"status":"error","error":"the catalog bootstrap lane accepts only .zip archives, but this bundle carries 'tar.gz'; POST /bootstrap/catalog would reject it"}
```

## Why that refusal was wrong

Packs published through the admin upload UI are **`.tar.gz`** —
`validate_archive_upload` accepts zip *and* tar, so that is a perfectly
normal production pack. But `parse_catalog_archive`, the bootstrap
lane's parser, reads zip only. Refusing tar therefore refused every pack
this migration exists to move.

## The fix: transcode, don't refuse

`prepare_archive` now converts a tar bundle to zip before the two
transformations it already did, so the pipeline is:

1. **transcode** `.tar.gz` → zip, member for member (new)
2. rewrite `agent-pack.yaml` with the provenance block
3. re-nest under one top-level directory
4. **check the finished zip against the bootstrap lane's own ceilings**
(new, see below)

All four steps run **before the first request**, `--dry-run` included.

`transcode_tar_gz_to_zip` preserves each member's bytes exactly, along
with its mode and mtime; only the container changes. Directory entries
are dropped — zip needs no explicit ones and the target reads files
only.

**Safety, reusing what is already there:**
- the declared expanded size is bounded from the tar headers **before**
anything is decompressed, and the resulting zip is bounded again
afterwards;
- `assert_safe_member_paths` runs on the member names first, so a
traversing entry is refused before transcoding rather than being carried
into the zip;
- **links and device nodes are refused outright** — symlink, hard link,
char/block device, fifo. Flattening a symlink into a regular file would
hand the target something it would then read as pack content, so this
fails loudly instead.

The bundle itself is untouched: provenance still identifies the source
archive by its original `.tar.gz` digest, and `files.archive` still
records what was exported. The zip is only the wire body. The bootstrap
filename is now always `archive.zip`, which is what the route requires.

`assert_bootstrap_supported` is gone — with both formats supported it
could never fail.

## Review follow-ups

**1. The finished zip is measured against the bootstrap contract before
the POST.** The repack bounds (`MAX_ARCHIVE_EXPANDED_BYTES` = 512 MiB)
say what is safe to expand locally, not what the target accepts.
`parse_catalog_archive` is far tighter: 100 MiB of uploaded bytes, 100
MiB of declared expanded bytes, 10,000 files. A legal `.tar.gz` can
expand past that, and transcoding it can grow it further — so the old
path did the whole conversion and then had the target reject it.
`assert_bootstrap_archive_within_contract` now checks all three against
the **final, re-nested** zip, which is the only thing the target
measures; over the limit is a `MigrationError` and the archive is never
uploaded.

The byte ceiling is imported from
`archive_service.MAX_PACK_TEST_ARCHIVE_BYTES` rather than copied. The
file ceiling is `catalog_bootstrap_service._MAX_ARCHIVE_FILES`, which
the scripts cannot import — that module pulls in the Mongo repositories
and the R2 client — so it is restated in core and a test pins it equal
to the value it mirrors.

**2. The zip timestamp is clamped at both ends.** `_zip_date_time`
clamped the 1980 lower bound only. A DOS timestamp holds 1980–2107, so a
2108 mtime made `ZipInfo` raise `struct.error` on write — a bare
traceback, not a `MigrationError`. Both ends are clamped now (2107-12-31
23:59:58 at the top), including the case where the platform cannot
convert the mtime at all.

**3. The stamp is read as UTC.** `time.localtime` made the transcoded
bytes — and their digest — depend on the runner's timezone.
`time.gmtime` makes the output reproducible; a zip stamp carries no
zone, so there was nothing local to preserve.

**4. `BOOTSTRAP_ARCHIVE_FORMAT` is deleted.** Dead since
`assert_bootstrap_supported` went: the format is pinned by
`TRANSCODED_ARCHIVE_FILENAME` and every call site already passes
`"zip"`.

**5. Local preparation moved ahead of the org-scoping probes, and
`--dry-run` now performs it.** The import used to probe first and
prepare second, so an archive that could never be published still spent
three requests finding that out — and a dry run skipped the local work
entirely, leaving exactly what it exists to surface (a tar.gz that will
not transcode, an over-limit archive, an unsafe member path, an
unrepresentable timestamp) for the real run to discover. The order is
now **local preparation → probes → writes**, and a refusal costs zero
requests rather than zero writes.

A dry run reports what it built under `archive_prepared` — shape only,
never content:

```json
"archive_prepared": {
  "bytes": 958,
  "max_bytes": 104857600,
  "entries": 4,
  "files": 4,
  "max_files": 10000,
  "declared_expanded_bytes": 614
}
```

`entries` counts every central-directory record, `files` only the
regular ones; re-nesting drops directory entries, so a gap between them
means the archive carries records the target will ignore.

## Not a bug: `engine_archive_captured: false`

The run also reported this. It is a data fact, not a defect: that source
submission pins no Engine runtime archive. The import's existing
semantics for a bundle without one are unchanged, and nothing here
touches them.

## Tests

`tests/unit/test_agent_pack_import.py`, 157 passing across the two
suites:

- a tar pack transcodes member-for-member — valid zip, member set and
bytes identical, `agent-pack.yaml` findable;
- mode and mtime survive as an exact UTC stamp, and the transcode is
byte-stable with `TZ` set to UTC+14;
- a pre-1980 mtime is clamped to the zip epoch, and a 2108 mtime — or
one the platform cannot convert — is clamped to 2107-12-31 23:59:58
instead of raising `struct.error`;
- directory entries dropped, files kept;
- symlink / hard link / char device / fifo each refused, by kind;
- an oversized tar is refused **before** transcoding (the zip writer is
patched to explode if reached);
- a traversing member is refused before transcoding;
- each of the three bootstrap ceilings refuses on its own, including a
deflated archive that is small on the wire but declares too much
expansion;
- the ceiling is measured on the final nested zip: it passes at exactly
that size and fails one byte under;
- an over-limit archive ends the run with **no request sent at all** —
asserted for both a real and a dry run, which is also what pins the
ordering;
- a dry run's `archive_prepared` matches the archive `prepare_archive`
actually produces for a tar.gz bundle, and carries no string or bytes
value;
- the restated file cap is pinned equal to
`catalog_bootstrap_service._MAX_ARCHIVE_FILES`;
- end-to-end: a tar.gz *bundle* reaches the bootstrap lane as a valid
zip whose members are byte-identical to the source except
`agent-pack.yaml`, nested one level, carrying the provenance block, with
`name`/`version` intact;
- provenance still reports the source tar.gz digest;
- the multipart filename is a bare `archive.zip`.

Gates: `ruff check` + `ruff format --check`, all 8 `scripts/ci-lint`
guards, pyright clean on the changed files, `actionlint` clean, full
`tests/unit` green. Nothing run against production or staging.

## Not merging

Left for you. The next run should get past this point; the remaining
unknowns are the org-scoping probe against the live staging backend and
the bootstrap itself.

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

Follow-up to #3590. With the export now running inside the production cluster, the first end-to-end run ([33244589405](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/33244589405)) got a **clean export** — pod started, RBAC sufficient, Mongo, R2 and the avatar all read, a 307 KB bundle produced — and then the import stopped before its first request:

```json
{"status":"error","error":"the catalog bootstrap lane accepts only .zip archives, but this bundle carries 'tar.gz'; POST /bootstrap/catalog would reject it"}
```

## Why that refusal was wrong

Packs published through the admin upload UI are **`.tar.gz`** — `validate_archive_upload` accepts zip *and* tar, so that is a perfectly normal production pack. But `parse_catalog_archive`, the bootstrap lane's parser, reads zip only. Refusing tar therefore refused every pack this migration exists to move.

## The fix: transcode, don't refuse

`prepare_archive` now converts a tar bundle to zip before the two transformations it already did, so the pipeline is:

1. **transcode** `.tar.gz` → zip, member for member (new)
2. rewrite `agent-pack.yaml` with the provenance block
3. re-nest under one top-level directory
4. **check the finished zip against the bootstrap lane's own ceilings** (new, see below)

All four steps run **before the first request**, `--dry-run` included.

`transcode_tar_gz_to_zip` preserves each member's bytes exactly, along with its mode and mtime; only the container changes. Directory entries are dropped — zip needs no explicit ones and the target reads files only.

**Safety, reusing what is already there:**
- the declared expanded size is bounded from the tar headers **before** anything is decompressed, and the resulting zip is bounded again afterwards;
- `assert_safe_member_paths` runs on the member names first, so a traversing entry is refused before transcoding rather than being carried into the zip;
- **links and device nodes are refused outright** — symlink, hard link, char/block device, fifo. Flattening a symlink into a regular file would hand the target something it would then read as pack content, so this fails loudly instead.

The bundle itself is untouched: provenance still identifies the source archive by its original `.tar.gz` digest, and `files.archive` still records what was exported. The zip is only the wire body. The bootstrap filename is now always `archive.zip`, which is what the route requires.

`assert_bootstrap_supported` is gone — with both formats supported it could never fail.

## Review follow-ups

**1. The finished zip is measured against the bootstrap contract before the POST.** The repack bounds (`MAX_ARCHIVE_EXPANDED_BYTES` = 512 MiB) say what is safe to expand locally, not what the target accepts. `parse_catalog_archive` is far tighter: 100 MiB of uploaded bytes, 100 MiB of declared expanded bytes, 10,000 files. A legal `.tar.gz` can expand past that, and transcoding it can grow it further — so the old path did the whole conversion and then had the target reject it. `assert_bootstrap_archive_within_contract` now checks all three against the **final, re-nested** zip, which is the only thing the target measures; over the limit is a `MigrationError` and the archive is never uploaded.

The byte ceiling is imported from `archive_service.MAX_PACK_TEST_ARCHIVE_BYTES` rather than copied. The file ceiling is `catalog_bootstrap_service._MAX_ARCHIVE_FILES`, which the scripts cannot import — that module pulls in the Mongo repositories and the R2 client — so it is restated in core and a test pins it equal to the value it mirrors.

**2. The zip timestamp is clamped at both ends.** `_zip_date_time` clamped the 1980 lower bound only. A DOS timestamp holds 1980–2107, so a 2108 mtime made `ZipInfo` raise `struct.error` on write — a bare traceback, not a `MigrationError`. Both ends are clamped now (2107-12-31 23:59:58 at the top), including the case where the platform cannot convert the mtime at all.

**3. The stamp is read as UTC.** `time.localtime` made the transcoded bytes — and their digest — depend on the runner's timezone. `time.gmtime` makes the output reproducible; a zip stamp carries no zone, so there was nothing local to preserve.

**4. `BOOTSTRAP_ARCHIVE_FORMAT` is deleted.** Dead since `assert_bootstrap_supported` went: the format is pinned by `TRANSCODED_ARCHIVE_FILENAME` and every call site already passes `"zip"`.

**5. Local preparation moved ahead of the org-scoping probes, and `--dry-run` now performs it.** The import used to probe first and prepare second, so an archive that could never be published still spent three requests finding that out — and a dry run skipped the local work entirely, leaving exactly what it exists to surface (a tar.gz that will not transcode, an over-limit archive, an unsafe member path, an unrepresentable timestamp) for the real run to discover. The order is now **local preparation → probes → writes**, and a refusal costs zero requests rather than zero writes.

A dry run reports what it built under `archive_prepared` — shape only, never content:

```json
"archive_prepared": {
  "bytes": 958,
  "max_bytes": 104857600,
  "entries": 4,
  "files": 4,
  "max_files": 10000,
  "declared_expanded_bytes": 614
}
```

`entries` counts every central-directory record, `files` only the regular ones; re-nesting drops directory entries, so a gap between them means the archive carries records the target will ignore.

## Not a bug: `engine_archive_captured: false`

The run also reported this. It is a data fact, not a defect: that source submission pins no Engine runtime archive. The import's existing semantics for a bundle without one are unchanged, and nothing here touches them.

## Tests

`tests/unit/test_agent_pack_import.py`, 157 passing across the two suites:

- a tar pack transcodes member-for-member — valid zip, member set and bytes identical, `agent-pack.yaml` findable;
- mode and mtime survive as an exact UTC stamp, and the transcode is byte-stable with `TZ` set to UTC+14;
- a pre-1980 mtime is clamped to the zip epoch, and a 2108 mtime — or one the platform cannot convert — is clamped to 2107-12-31 23:59:58 instead of raising `struct.error`;
- directory entries dropped, files kept;
- symlink / hard link / char device / fifo each refused, by kind;
- an oversized tar is refused **before** transcoding (the zip writer is patched to explode if reached);
- a traversing member is refused before transcoding;
- each of the three bootstrap ceilings refuses on its own, including a deflated archive that is small on the wire but declares too much expansion;
- the ceiling is measured on the final nested zip: it passes at exactly that size and fails one byte under;
- an over-limit archive ends the run with **no request sent at all** — asserted for both a real and a dry run, which is also what pins the ordering;
- a dry run's `archive_prepared` matches the archive `prepare_archive` actually produces for a tar.gz bundle, and carries no string or bytes value;
- the restated file cap is pinned equal to `catalog_bootstrap_service._MAX_ARCHIVE_FILES`;
- end-to-end: a tar.gz *bundle* reaches the bootstrap lane as a valid zip whose members are byte-identical to the source except `agent-pack.yaml`, nested one level, carrying the provenance block, with `name`/`version` intact;
- provenance still reports the source tar.gz digest;
- the multipart filename is a bare `archive.zip`.

Gates: `ruff check` + `ruff format --check`, all 8 `scripts/ci-lint` guards, pyright clean on the changed files, `actionlint` clean, full `tests/unit` green. Nothing run against production or staging.

## Not merging

Left for you. The next run should get past this point; the remaining unknowns are the org-scoping probe against the live staging backend and the bootstrap itself.


---

## revert(claw-interface): restore the explicit staging engine runtime-asset allowlist (#3591)

- **SHA**: `5deb6c09bbb36eb39b24644ad5fa63e2d20cd9f4`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-29T09:15:49Z
- **PR**: #3591

### Commit Message

```
revert(claw-interface): restore the explicit staging engine runtime-asset allowlist (#3591)

## Why

#3586 set staging's `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS` to `*` so
migrated Packs would need no per-id PR. That was wrong: the gate is not
"may use the V2 archive if present" but "must use it".
`engine_agent_install_service.py:273-282` routes every gated Pack
through `load_current_engine_runtime_asset` →
`resolve_engine_environment_pin`, which raises when the current
submission has no Engine runtime asset — there is no V1 fallback on that
branch. Packs outside the gate go through
`resolve_legacy_environment_pin` (the V1 Environment pin).

The first real migration export (run 33244589405, `industry-news-buddy`)
reports `engine_archive_captured: false`: the production Packs being
migrated carry no Engine archive, and production itself serves them
through the legacy path (they are not in production's list). With `*`,
every such Pack on staging — migrated ones and any UI-authored Pack —
fails a V2 hire with `agent.pack_environment_not_ready`.

## What

- Staging overlay back to the nine reviewed ids, with a comment stating
the invariant (a listed Pack must have a registered Engine archive;
unlisted Packs use the legacy V1 pin).
- Wiring test pins the explicit set again. The
`AGENT_PACK_LANE_TARGET_ORG_IDS` entry from #3587 is untouched.

Focused test: 2 passed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01VRz5q6Evgj42xoLucxuCE9
```

### PR Body

## Why

#3586 set staging's `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS` to `*` so migrated Packs would need no per-id PR. That was wrong: the gate is not "may use the V2 archive if present" but "must use it". `engine_agent_install_service.py:273-282` routes every gated Pack through `load_current_engine_runtime_asset` → `resolve_engine_environment_pin`, which raises when the current submission has no Engine runtime asset — there is no V1 fallback on that branch. Packs outside the gate go through `resolve_legacy_environment_pin` (the V1 Environment pin).

The first real migration export (run 33244589405, `industry-news-buddy`) reports `engine_archive_captured: false`: the production Packs being migrated carry no Engine archive, and production itself serves them through the legacy path (they are not in production's list). With `*`, every such Pack on staging — migrated ones and any UI-authored Pack — fails a V2 hire with `agent.pack_environment_not_ready`.

## What

- Staging overlay back to the nine reviewed ids, with a comment stating the invariant (a listed Pack must have a registered Engine archive; unlisted Packs use the legacy V1 pin).
- Wiring test pins the explicit set again. The `AGENT_PACK_LANE_TARGET_ORG_IDS` entry from #3587 is untouched.

Focused test: 2 passed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01VRz5q6Evgj42xoLucxuCE9


---

## fix(ci): run the agent pack export inside the production cluster (#3590)

- **SHA**: `dd821a5fd428953b5dbc3ebe81b35d1a9629a7d6`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-29T09:03:26Z
- **PR**: #3590

### Commit Message

```
fix(ci): run the agent pack export inside the production cluster (#3590)

Follow-up to #3580 / #3583. The first real run
([33243645291](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/33243645291))
got past the dependency install (#3589) and then timed out on **every**
production Mongo connection.

## Root cause: Atlas Private Endpoint

The production Mongo hosts are Private Endpoint names —
`pl-00-000-us-east1-gcp.pvr4n.mongodb.net` and friends. Those resolve
and route **only from inside the GCP VPC**. A GitHub/Blacksmith runner
can never reach them, with or without correct credentials, so no amount
of secret plumbing would have fixed it. R2 was never reached so it stays
unverified, but Mongo alone settles the design: the export cannot run on
a runner.

## The export now runs inside the production cluster

1. Authenticate to production GKE exactly as `service-deploy.yml` does —
`google-github-actions/auth@v3` with `vars.PRODUCTION_GCP_PROJECT` +
`secrets.PRODUCTION_DEPLOYMENT_GKE_SA_KEY`, then
`get-gke-credentials@v3` with `vars.PRODUCTION_GKE_CLUSTER_PRIMARY` /
`vars.PRODUCTION_GKE_LOCATION_PRIMARY`.
2. Read the image `claw-interface-deployment` is *currently running* and
start a one-shot pod from it, so the export uses production's own
dependency set rather than whatever a runner would resolve today.
3. `kubectl cp` the migration scripts in — the image ships only `app/`
and `packs/`, so `scripts/` is not in it.
4. Run the export in the pod; stream its JSON back to the runner as
`export-result.json`; `kubectl cp` the bundle out into the same path the
artifact upload already used.
5. Delete the pod in an `always()` step.

The artifact, the import job, and the `dry_run` semantics are untouched:
the export always really reads, and only the import has a dry mode.

## Credentials no longer leave the cluster

This is the part worth reviewing on its own merits. The six
`PROD_PACK_*` secrets are **deleted from the workflow**. The pod reads
Mongo and R2 from the cluster's own `vault-claw-interface-env-secret`
and the exec shell maps them onto the script's `SOURCE_*` names:

```
MONGODB_USER/PASSWORD/HOST/NAME        -> SOURCE_MONGODB_USER/PASSWORD/HOST/NAME
R2_ENDPOINT_URL/ACCESS_KEY_ID/…        -> SOURCE_R2_ENDPOINT_URL/ACCESS_KEY_ID/…
R2_PUBLIC_DOMAIN                       -> SOURCE_R2_PUBLIC_DOMAIN (avatar allowlist)
```

The `kubectl exec` payload is single-quoted, so those variables are
expanded by the **pod's** shell — the values never enter the runner's
environment, its process table, or its logs. The runner holds a
kubeconfig and nothing else. The script composes the Mongo URI itself
and percent-encodes the credentials (`_source_mongo_uri`), so a password
containing `@` or `/` is safe.

`vars.R2_PUBLIC_DOMAIN` is also gone, since the pod already has
`R2_PUBLIC_DOMAIN`. `vars.PACK_MIGRATION_AVATAR_ALLOWED_HOSTS` still
works as an override — it is injected as a pod `env` entry when set.

**After this merges, these six secrets can be deleted from the
repo/environment and dropped from the sync script:**
`PROD_PACK_MONGODB_URI`, `PROD_PACK_MONGODB_NAME`,
`PROD_PACK_R2_ENDPOINT_URL`, `PROD_PACK_R2_ACCESS_KEY_ID`,
`PROD_PACK_R2_ACCESS_KEY_SECRET`,
`PROD_PACK_R2_AGENT_PACKS_BUCKET_NAME`.

## Credential scope (reviewer question)

The removed `PROD_PACK_*` secrets were not scoped read-only credentials:
they were the same claw-interface production credentials copied out of
Vault into GitHub (`zooclaw-dev/sync-pack-migration-secrets.sh`; no
read-only Atlas user / R2 token exists yet). This PR therefore narrows
exposure — the credentials no longer leave the cluster or live in GitHub
— while the blast radius stays bounded by the script (`find` /
`find_one` / `get_object`), as before.

## RBAC verified

`deployment@srpproduct-dc37e.iam.gserviceaccount.com` (the account
behind `PRODUCTION_DEPLOYMENT_GKE_SA_KEY`) holds `roles/container.admin`
on the project, which covers `pods` create/get/list/delete and
`pods/exec`. `ghcr-secret` exists in `ecap` and is the deployment's own
pull secret.

## Checks done

- `tar` is present in the pod (`kubectl cp` needs it): the base image is
`python:3.12.3`, and the Dockerfile itself runs `tar zxvf`.
- Working directory and imports: the image sets `WORKDIR /code` and
`PYTHONPATH=/code`; the exec `cd /code` and runs `python -m
scripts.export_agent_pack`. `scripts/` has no `__init__.py` on `main`,
which is fine — it imports as a namespace package, which is how the unit
tests already import it.
- The pod spec carries `imagePullSecrets: ghcr-secret` (the image is
private) and `restartPolicy: Never`, and is labelled
`app=pack-export,migration-run-id=<run id>` for cleanup. The pod name
carries the run id and attempt.
- The export script is still read-only against production: `find` /
`find_one` / `get_object` and one HTTP `GET` of the avatar.
- `actionlint` clean; every `run:` block passes `bash -n`; the `jq`
override document and the `bash -c '…' _ "$@"` argument passing were
both executed locally to confirm their shapes.

## RBAC assumption — please confirm on the first run

`PRODUCTION_DEPLOYMENT_GKE_SA_KEY` is used today for `kubectl apply` /
`kubectl get` on Deployments and MultiClusterServices. This job
additionally needs, in namespace `ecap`:

- `pods`: `create`, `get`, `list`, `delete`
- `pods/exec`: `create` (used by both `kubectl exec` **and** `kubectl
cp`)

I could not verify the binding from here. If the SA turns out to lack
them the first run fails at `kubectl run` or the first `kubectl cp` with
a clear RBAC error, and the fix is a Role/RoleBinding in `ecap` rather
than anything in this workflow.

## Not merging

Left for you to run. Suggested first run: `dry_run: true` with one
`display_id`, which exercises the whole export path for real (export
never dries) and stops the import before any write.

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

Follow-up to #3580 / #3583. The first real run ([33243645291](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/33243645291)) got past the dependency install (#3589) and then timed out on **every** production Mongo connection.

## Root cause: Atlas Private Endpoint

The production Mongo hosts are Private Endpoint names — `pl-00-000-us-east1-gcp.pvr4n.mongodb.net` and friends. Those resolve and route **only from inside the GCP VPC**. A GitHub/Blacksmith runner can never reach them, with or without correct credentials, so no amount of secret plumbing would have fixed it. R2 was never reached so it stays unverified, but Mongo alone settles the design: the export cannot run on a runner.

## The export now runs inside the production cluster

1. Authenticate to production GKE exactly as `service-deploy.yml` does — `google-github-actions/auth@v3` with `vars.PRODUCTION_GCP_PROJECT` + `secrets.PRODUCTION_DEPLOYMENT_GKE_SA_KEY`, then `get-gke-credentials@v3` with `vars.PRODUCTION_GKE_CLUSTER_PRIMARY` / `vars.PRODUCTION_GKE_LOCATION_PRIMARY`.
2. Read the image `claw-interface-deployment` is *currently running* and start a one-shot pod from it, so the export uses production's own dependency set rather than whatever a runner would resolve today.
3. `kubectl cp` the migration scripts in — the image ships only `app/` and `packs/`, so `scripts/` is not in it.
4. Run the export in the pod; stream its JSON back to the runner as `export-result.json`; `kubectl cp` the bundle out into the same path the artifact upload already used.
5. Delete the pod in an `always()` step.

The artifact, the import job, and the `dry_run` semantics are untouched: the export always really reads, and only the import has a dry mode.

## Credentials no longer leave the cluster

This is the part worth reviewing on its own merits. The six `PROD_PACK_*` secrets are **deleted from the workflow**. The pod reads Mongo and R2 from the cluster's own `vault-claw-interface-env-secret` and the exec shell maps them onto the script's `SOURCE_*` names:

```
MONGODB_USER/PASSWORD/HOST/NAME        -> SOURCE_MONGODB_USER/PASSWORD/HOST/NAME
R2_ENDPOINT_URL/ACCESS_KEY_ID/…        -> SOURCE_R2_ENDPOINT_URL/ACCESS_KEY_ID/…
R2_PUBLIC_DOMAIN                       -> SOURCE_R2_PUBLIC_DOMAIN (avatar allowlist)
```

The `kubectl exec` payload is single-quoted, so those variables are expanded by the **pod's** shell — the values never enter the runner's environment, its process table, or its logs. The runner holds a kubeconfig and nothing else. The script composes the Mongo URI itself and percent-encodes the credentials (`_source_mongo_uri`), so a password containing `@` or `/` is safe.

`vars.R2_PUBLIC_DOMAIN` is also gone, since the pod already has `R2_PUBLIC_DOMAIN`. `vars.PACK_MIGRATION_AVATAR_ALLOWED_HOSTS` still works as an override — it is injected as a pod `env` entry when set.

**After this merges, these six secrets can be deleted from the repo/environment and dropped from the sync script:** `PROD_PACK_MONGODB_URI`, `PROD_PACK_MONGODB_NAME`, `PROD_PACK_R2_ENDPOINT_URL`, `PROD_PACK_R2_ACCESS_KEY_ID`, `PROD_PACK_R2_ACCESS_KEY_SECRET`, `PROD_PACK_R2_AGENT_PACKS_BUCKET_NAME`.

## Credential scope (reviewer question)

The removed `PROD_PACK_*` secrets were not scoped read-only credentials: they were the same claw-interface production credentials copied out of Vault into GitHub (`zooclaw-dev/sync-pack-migration-secrets.sh`; no read-only Atlas user / R2 token exists yet). This PR therefore narrows exposure — the credentials no longer leave the cluster or live in GitHub — while the blast radius stays bounded by the script (`find` / `find_one` / `get_object`), as before.

## RBAC verified

`deployment@srpproduct-dc37e.iam.gserviceaccount.com` (the account behind `PRODUCTION_DEPLOYMENT_GKE_SA_KEY`) holds `roles/container.admin` on the project, which covers `pods` create/get/list/delete and `pods/exec`. `ghcr-secret` exists in `ecap` and is the deployment's own pull secret.

## Checks done

- `tar` is present in the pod (`kubectl cp` needs it): the base image is `python:3.12.3`, and the Dockerfile itself runs `tar zxvf`.
- Working directory and imports: the image sets `WORKDIR /code` and `PYTHONPATH=/code`; the exec `cd /code` and runs `python -m scripts.export_agent_pack`. `scripts/` has no `__init__.py` on `main`, which is fine — it imports as a namespace package, which is how the unit tests already import it.
- The pod spec carries `imagePullSecrets: ghcr-secret` (the image is private) and `restartPolicy: Never`, and is labelled `app=pack-export,migration-run-id=<run id>` for cleanup. The pod name carries the run id and attempt.
- The export script is still read-only against production: `find` / `find_one` / `get_object` and one HTTP `GET` of the avatar.
- `actionlint` clean; every `run:` block passes `bash -n`; the `jq` override document and the `bash -c '…' _ "$@"` argument passing were both executed locally to confirm their shapes.

## RBAC assumption — please confirm on the first run

`PRODUCTION_DEPLOYMENT_GKE_SA_KEY` is used today for `kubectl apply` / `kubectl get` on Deployments and MultiClusterServices. This job additionally needs, in namespace `ecap`:

- `pods`: `create`, `get`, `list`, `delete`
- `pods/exec`: `create` (used by both `kubectl exec` **and** `kubectl cp`)

I could not verify the binding from here. If the SA turns out to lack them the first run fails at `kubectl run` or the first `kubectl cp` with a clear RBAC error, and the fix is a Role/RoleBinding in `ecap` rather than anything in this workflow.

## Not merging

Left for you to run. Suggested first run: `dry_run: true` with one `display_id`, which exercises the whole export path for real (export never dries) and stops the import before any write.



---

## fix(ci): authenticate the private favie-common dependency in the pack migration workflow (#3589)

- **SHA**: `e53080b53dd4900bff5a61042f97a9c0b3b5a4c1`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-29T08:38:33Z
- **PR**: #3589

### Commit Message

```
fix(ci): authenticate the private favie-common dependency in the pack migration workflow (#3589)

## Why

The first dispatch of `migrate-agent-pack.yml` (run 33243042874) failed
in the export job at `uv pip install -r requirements.txt`:

```
error: Git operation failed
  Caused by: `git fetch ... 'https://github.com/SerendipityOneInc/favie-common.git' '+refs/tags/v0.3.69:...'` (exit status: 128)
```

`favie-common` is a private git dependency and the runner had no
credential for it.

## What

Both jobs (export / import) now install with the same recipe the
`python-code-quality-v3` reusable workflow uses for this exact file:
`GITHUB_TOKEN: ${{ secrets.GH_RELEASE_TOKEN }}` (org secret already
visible to this repo) plus `git config --global
url."https://${GITHUB_TOKEN}@github.com/".insteadOf
"https://github.com/"`.

No change to the migration logic.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01VRz5q6Evgj42xoLucxuCE9
```

### PR Body

## Why

The first dispatch of `migrate-agent-pack.yml` (run 33243042874) failed in the export job at `uv pip install -r requirements.txt`:

```
error: Git operation failed
  Caused by: `git fetch ... 'https://github.com/SerendipityOneInc/favie-common.git' '+refs/tags/v0.3.69:...'` (exit status: 128)
```

`favie-common` is a private git dependency and the runner had no credential for it.

## What

Both jobs (export / import) now install with the same recipe the `python-code-quality-v3` reusable workflow uses for this exact file: `GITHUB_TOKEN: ${{ secrets.GH_RELEASE_TOKEN }}` (org secret already visible to this repo) plus `git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"`.

No change to the migration logic.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01VRz5q6Evgj42xoLucxuCE9


---

## feat(claw-interface): import agent pack bundles through service-token channels (#3583)

- **SHA**: `68a59ad34f8b6ed7d5abc9a14d89ac2c46ccfde0`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-29T08:23:14Z
- **PR**: #3583

### Commit Message

```
feat(claw-interface): import agent pack bundles through service-token channels (#3583)

Part 2 of 2 for #3580. #3584 (the export half) is merged; this is the
**write half**: it replays an exported bundle into a target environment,
plus the `workflow_dispatch` that drives both phases.

## Depends on #3587

#3587 (`feat(claw-interface): accept optional org_id on catalog
bootstrap and runtime-asset lanes`) has to be **deployed to staging
before this is run**. Without it both routes default to `zooclaw` and
would publish a migrated pack into the official catalog. The contract
this is written against, verified against that PR:

- `POST /agent-packs/bootstrap/catalog` — multipart `org_id: str | None
= Form(default=None, max_length=64)`
- `POST /agent-packs/runtime-assets` — body `org_id: str | None =
Field(default=None, max_length=64)`
- both default to `zooclaw`; a non-`zooclaw` value must be an existing
active org, else `<prefix>.target_org_not_found` (`pack_catalog.` /
`pack_runtime_asset.`)

The importer does not trust deployment order: it reads the target's own
`/admin/openapi.json` before writing anything and refuses to run unless
both routes declare `org_id` in their request schema (see below), and it
surfaces `target_org_not_found` with a hint rather than a raw body.

## Service-token channels, not the user API

The import holds **no user identity at all** — no JWT, no account, no
org membership. Two token channels, both scoped by an `org_id` field:

```
POST {base}/agent-packs/bootstrap/catalog     X-Agent-Pack-Catalog-Token
POST {base}/agent-packs/runtime-assets        X-Agent-Pack-Runtime-Token
```

plus `POST {r2-access-worker}/upload` with the Worker's own
`UPLOAD_SERVICE_TOKEN`, because the runtime-assets body takes an
**object key** rather than bytes, so the Engine archive has to be staged
first.

**Why not the user API.** `zooclaw` is a fixed label on the pack rows,
not a real organization in `ecap-orgs`: it has no members, so no account
can be an admin of it and no JWT can act for it. And migrated packs must
not appear in the official catalog anyway — they are test-layer
fixtures. The target is a dedicated staging smoke org, and
`--target-org-id` refuses both an empty value and `zooclaw`, because
**both routes default to the catalog org when `org_id` is omitted**.

## The decision table, from what the lane actually does

Traced through `catalog_bootstrap_service.bootstrap_catalog_pack` and
`_resolve_existing`:

| Target state | Lane behaviour | Action |
|---|---|---|
| no pack with this `display_id` in the org | creates a draft, submits
the archive, auto-approves | `create` → published |
| a draft it created earlier | submits + approves | `resume` → published
|
| a submission it left `submitted` at this exact `pack_version` |
approves it | `resume` → published |
| pack is **active** | short-circuits **before the archive is parsed**;
returns the current submission, publishes nothing | → `incomplete` |
| draft/submitted not authored by the bootstrap actor, or deprecated |
`pack_catalog.existing_pack_not_bootstrappable` | refused server-side |

**There is no publish-a-new-version behaviour on this lane**, which is
why `new_version` is not an action. The response carries no
`pack_version` and these channels expose no read surface, so the run
cannot tell "already migrated at this version" from "the target is
pinned to an older version and my bundle was ignored". It reports
`incomplete` rather than guessing; `--accept-existing` is how an
operator who has checked the target declares it a skip.

## Two lane constraints the archive has to satisfy

- **`.zip` only.** `parse_catalog_archive` takes a bare `.zip` name and
rejects anything else, so a `.tar.gz` bundle is refused up front rather
than at the target.
- **Exactly one top-level directory** — the *opposite* of the root
layout the export normalizes to for `validate_archive_upload`. The
import re-nests the archive under the directory the export recorded
(`files.archive.layout`), or under `display_id`, bounded and streamed
like the strip.

Provenance still rides in `agent-pack.yaml`'s `release_notes`, which is
exactly what makes it work on this lane: bootstrap parses the pack's
metadata out of the archive.

## Engine runtime archive

Unchanged in shape, plus `org_id`: staged through the Worker, then
registered. It runs after the bootstrap because
`register_engine_runtime_asset` attaches to `pack.latest_submission_id`
and refuses anything not approved, and it schedules the Engine
projection itself. Kept from the previous round: the token preflight
(missing credentials cost zero writes), the displaced-submission guard
(the returned `submission_id` must be the one the bootstrap reported),
and `--skip-engine-asset`. `projection_scheduled: false` is still an
`incomplete` outcome.

## Two guarantees that are weaker, and said so

- **Avatar is not migrated.** The bootstrap lane parses its metadata
from the archive and takes no avatar. The bundle still carries one
(#3584 is unchanged); the import ignores it and reports `avatar: skipped
(bootstrap lane)`.
- **No confirmed Environment build.** With no read surface on these
channels there is nothing to poll, so the result reports what the target
*scheduled* (`projection_scheduled`) and sets `environment_confirmed:
false` with a note. The readiness machinery from the previous round is
gone because it has nothing to read.

## Dry run

Read-only by construction: the client refuses any non-GET. It prints the
writes it would send (`planned_calls`) and probes the channels for
reachability — a `GET` on a POST-only route answers `405`, which proves
the base URL and route without exercising the token, since method
dispatch happens before auth.

## Workflow

Inputs: `pack_id` | `display_id`, `source_org_id`, `target_org_id`
(defaults to `vars.STAGING_SMOKE_ORG_ID`), `accept_existing`,
`skip_engine_asset`, `bundle_run_id`, `align_manifest_name`, `dry_run`
(default `true`).

Secrets — **import**: `STAGING_CLAW_INTERFACE_BASE_URL`,
`STAGING_AGENT_PACK_CATALOG_BOOTSTRAP_TOKEN`,
`STAGING_AGENT_PACK_RUNTIME_ASSETS_TOKEN`,
`STAGING_AGENT_PACKS_UPLOAD_URL`, and `UPLOAD_SERVICE_TOKEN` — the last
one is the r2-access-worker's existing `staging` environment secret that
`deploy-r2-access-worker.yml` already publishes, not a new one.
`STAGING_SMOKE_ACCOUNT_JWT` is **no longer used by the migration** (it
remains for the cache smoke's hire).

Secrets — **export** (production, read-only) are unchanged:
`PROD_PACK_MONGODB_URI`, `PROD_PACK_MONGODB_NAME`,
`PROD_PACK_R2_ENDPOINT_URL`, `PROD_PACK_R2_ACCESS_KEY_ID`,
`PROD_PACK_R2_ACCESS_KEY_SECRET`,
`PROD_PACK_R2_AGENT_PACKS_BUCKET_NAME`.

## The target must prove it understands `org_id`

Neither response carries an owning org —
`AgentPackCatalogBootstrapResponse` is
`pack_id`/`display_id`/`submission_id`/`outcome`, and the registration
reply is `submission_id`/`sha256`/`status`/`projection_scheduled` — and
FastAPI ignores unknown form fields silently, so sending `org_id` at a
backend that predates #3587 would publish into the catalog with nothing
in the reply to show it.

So before the first write (and in `--dry-run`) each route is asked to
resolve an org id that **cannot exist**
(`00000000000000000000000000000000`, with `display_id=capability-probe`
and a one-byte archive). It must answer `target_org_not_found` or
`target_org_not_allowed` — both prove the field was parsed and resolved,
which #3587 guarantees happens before the archive or any other input is
touched. Any other answer (a complaint about the probe archive, a form
error, a success) means `org_id` was ignored or never reached, and the
run refuses. The probe creates nothing, and the runtime-assets route is
probed only when the bundle carries an Engine archive.

> Do **not** substitute `/admin/openapi.json` for this. Measured in
staging: 643 KB, 35–36s to generate, and it blocks the single uvicorn
worker long enough for the liveness/readiness probes to time out and
Kubernetes to kill the pod (exit 137).

After the write, `assert_response_org` checks any owning-org field a
response does carry, so once #3587 echoes `org_id` a mismatch stops the
run with `incomplete`.

## Limitations

- **No re-migration of an active pack.** The bootstrap lane has no
publish-a-new-version behaviour: against an active pack it returns the
current submission untouched. To land a newer `pack_version` for a pack
that already exists in the target you must deprecate the old pack in
staging first and bootstrap again. `--accept-existing` is for the other
case — the target is already the version you want — and it still
completes the Engine-archive registration, so a run that died between
the bootstrap and the registration can be finished by re-running with
it.
- **`.zip` only** (`parse_catalog_archive`), so a `.tar.gz` bundle is
refused up front.
- **No avatar**, and **no confirmed Environment build** — see above.
- **Visibility is not configurable.** The bootstrap lane always creates
the pack with `hide_market=true` and exposes no request field for it.
The bundle records the source pack's own value for comparison only, and
the result reports what this run actually did: `applied: true` only when
the bootstrap published, `"unknown"` on the `--accept-existing` skip (an
already-active pack's visibility cannot be read or changed through these
channels), and `false` for a dry run or anything that stopped before the
bootstrap. `expected: true` throughout, since that is the lane's fixed
policy.

## Tests

`tests/unit/test_agent_pack_import.py` — 64 tests, no network, over
`httpx.MockTransport`: target-org guards, the `.zip`-only refusal,
source-directory derivation, re-nesting (root → nested, already-nested
no-op, bounded), `prepare_archive` producing a nested archive carrying
provenance, every branch of the decision table, the registration body
carrying `org_id`, the plan listing only the token channels, bundle
digest and layout refusals, the exact multipart form and headers the
bootstrap receives, the staged-then-registered engine sequence with its
headers, the displaced-submission and disabled-projection `incomplete`
outcomes, the credential preflight making zero calls, the dry run
issuing only GETs, the read-only client refusing a write, the
org-capability probe (both org-resolution codes accepted, every other
answer refused, the refusal naming route and code, the probe bodies
asserted, the runtime route probed only when needed, a disallowed target
org reported, and a response naming another org stopping the run), a
lost registration finished by a later `--accept-existing` run, and the
expansion bound enforced before anything decompresses - ahead of the
manifest rewrite, and ahead of the bundle precheck's own manifest read.

Gates: `ruff check` + `ruff format --check` clean, all 8
`scripts/ci-lint/` guards, pyright clean on the new files, `pytest` 136
passed across both suites (72 + 64), full `tests/unit` 9098 passed / 5
skipped (the 21 collection errors are a pre-existing stale local venv,
reproduced on unmodified `main`), actionlint clean. Nothing was run
against production or staging.

## Notes

1. **Contract.** Verified against #3587 (see Depends on, above). If the
field names ever change, the two call sites are
`TargetChannels.bootstrap_catalog` and
`build_runtime_asset_registration_body`.
2. **Size.** 2327 changed lines against `main`.

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

Part 2 of 2 for #3580. #3584 (the export half) is merged; this is the **write half**: it replays an exported bundle into a target environment, plus the `workflow_dispatch` that drives both phases.

## Depends on #3587

#3587 (`feat(claw-interface): accept optional org_id on catalog bootstrap and runtime-asset lanes`) has to be **deployed to staging before this is run**. Without it both routes default to `zooclaw` and would publish a migrated pack into the official catalog. The contract this is written against, verified against that PR:

- `POST /agent-packs/bootstrap/catalog` — multipart `org_id: str | None = Form(default=None, max_length=64)`
- `POST /agent-packs/runtime-assets` — body `org_id: str | None = Field(default=None, max_length=64)`
- both default to `zooclaw`; a non-`zooclaw` value must be an existing active org, else `<prefix>.target_org_not_found` (`pack_catalog.` / `pack_runtime_asset.`)

The importer does not trust deployment order: it reads the target's own `/admin/openapi.json` before writing anything and refuses to run unless both routes declare `org_id` in their request schema (see below), and it surfaces `target_org_not_found` with a hint rather than a raw body.

## Service-token channels, not the user API

The import holds **no user identity at all** — no JWT, no account, no org membership. Two token channels, both scoped by an `org_id` field:

```
POST {base}/agent-packs/bootstrap/catalog     X-Agent-Pack-Catalog-Token
POST {base}/agent-packs/runtime-assets        X-Agent-Pack-Runtime-Token
```

plus `POST {r2-access-worker}/upload` with the Worker's own `UPLOAD_SERVICE_TOKEN`, because the runtime-assets body takes an **object key** rather than bytes, so the Engine archive has to be staged first.

**Why not the user API.** `zooclaw` is a fixed label on the pack rows, not a real organization in `ecap-orgs`: it has no members, so no account can be an admin of it and no JWT can act for it. And migrated packs must not appear in the official catalog anyway — they are test-layer fixtures. The target is a dedicated staging smoke org, and `--target-org-id` refuses both an empty value and `zooclaw`, because **both routes default to the catalog org when `org_id` is omitted**.

## The decision table, from what the lane actually does

Traced through `catalog_bootstrap_service.bootstrap_catalog_pack` and `_resolve_existing`:

| Target state | Lane behaviour | Action |
|---|---|---|
| no pack with this `display_id` in the org | creates a draft, submits the archive, auto-approves | `create` → published |
| a draft it created earlier | submits + approves | `resume` → published |
| a submission it left `submitted` at this exact `pack_version` | approves it | `resume` → published |
| pack is **active** | short-circuits **before the archive is parsed**; returns the current submission, publishes nothing | → `incomplete` |
| draft/submitted not authored by the bootstrap actor, or deprecated | `pack_catalog.existing_pack_not_bootstrappable` | refused server-side |

**There is no publish-a-new-version behaviour on this lane**, which is why `new_version` is not an action. The response carries no `pack_version` and these channels expose no read surface, so the run cannot tell "already migrated at this version" from "the target is pinned to an older version and my bundle was ignored". It reports `incomplete` rather than guessing; `--accept-existing` is how an operator who has checked the target declares it a skip.

## Two lane constraints the archive has to satisfy

- **`.zip` only.** `parse_catalog_archive` takes a bare `.zip` name and rejects anything else, so a `.tar.gz` bundle is refused up front rather than at the target.
- **Exactly one top-level directory** — the *opposite* of the root layout the export normalizes to for `validate_archive_upload`. The import re-nests the archive under the directory the export recorded (`files.archive.layout`), or under `display_id`, bounded and streamed like the strip.

Provenance still rides in `agent-pack.yaml`'s `release_notes`, which is exactly what makes it work on this lane: bootstrap parses the pack's metadata out of the archive.

## Engine runtime archive

Unchanged in shape, plus `org_id`: staged through the Worker, then registered. It runs after the bootstrap because `register_engine_runtime_asset` attaches to `pack.latest_submission_id` and refuses anything not approved, and it schedules the Engine projection itself. Kept from the previous round: the token preflight (missing credentials cost zero writes), the displaced-submission guard (the returned `submission_id` must be the one the bootstrap reported), and `--skip-engine-asset`. `projection_scheduled: false` is still an `incomplete` outcome.

## Two guarantees that are weaker, and said so

- **Avatar is not migrated.** The bootstrap lane parses its metadata from the archive and takes no avatar. The bundle still carries one (#3584 is unchanged); the import ignores it and reports `avatar: skipped (bootstrap lane)`.
- **No confirmed Environment build.** With no read surface on these channels there is nothing to poll, so the result reports what the target *scheduled* (`projection_scheduled`) and sets `environment_confirmed: false` with a note. The readiness machinery from the previous round is gone because it has nothing to read.

## Dry run

Read-only by construction: the client refuses any non-GET. It prints the writes it would send (`planned_calls`) and probes the channels for reachability — a `GET` on a POST-only route answers `405`, which proves the base URL and route without exercising the token, since method dispatch happens before auth.

## Workflow

Inputs: `pack_id` | `display_id`, `source_org_id`, `target_org_id` (defaults to `vars.STAGING_SMOKE_ORG_ID`), `accept_existing`, `skip_engine_asset`, `bundle_run_id`, `align_manifest_name`, `dry_run` (default `true`).

Secrets — **import**: `STAGING_CLAW_INTERFACE_BASE_URL`, `STAGING_AGENT_PACK_CATALOG_BOOTSTRAP_TOKEN`, `STAGING_AGENT_PACK_RUNTIME_ASSETS_TOKEN`, `STAGING_AGENT_PACKS_UPLOAD_URL`, and `UPLOAD_SERVICE_TOKEN` — the last one is the r2-access-worker's existing `staging` environment secret that `deploy-r2-access-worker.yml` already publishes, not a new one. `STAGING_SMOKE_ACCOUNT_JWT` is **no longer used by the migration** (it remains for the cache smoke's hire).

Secrets — **export** (production, read-only) are unchanged: `PROD_PACK_MONGODB_URI`, `PROD_PACK_MONGODB_NAME`, `PROD_PACK_R2_ENDPOINT_URL`, `PROD_PACK_R2_ACCESS_KEY_ID`, `PROD_PACK_R2_ACCESS_KEY_SECRET`, `PROD_PACK_R2_AGENT_PACKS_BUCKET_NAME`.

## The target must prove it understands `org_id`

Neither response carries an owning org — `AgentPackCatalogBootstrapResponse` is `pack_id`/`display_id`/`submission_id`/`outcome`, and the registration reply is `submission_id`/`sha256`/`status`/`projection_scheduled` — and FastAPI ignores unknown form fields silently, so sending `org_id` at a backend that predates #3587 would publish into the catalog with nothing in the reply to show it.

So before the first write (and in `--dry-run`) each route is asked to resolve an org id that **cannot exist** (`00000000000000000000000000000000`, with `display_id=capability-probe` and a one-byte archive). It must answer `target_org_not_found` or `target_org_not_allowed` — both prove the field was parsed and resolved, which #3587 guarantees happens before the archive or any other input is touched. Any other answer (a complaint about the probe archive, a form error, a success) means `org_id` was ignored or never reached, and the run refuses. The probe creates nothing, and the runtime-assets route is probed only when the bundle carries an Engine archive.

> Do **not** substitute `/admin/openapi.json` for this. Measured in staging: 643 KB, 35–36s to generate, and it blocks the single uvicorn worker long enough for the liveness/readiness probes to time out and Kubernetes to kill the pod (exit 137).

After the write, `assert_response_org` checks any owning-org field a response does carry, so once #3587 echoes `org_id` a mismatch stops the run with `incomplete`.

## Limitations

- **No re-migration of an active pack.** The bootstrap lane has no publish-a-new-version behaviour: against an active pack it returns the current submission untouched. To land a newer `pack_version` for a pack that already exists in the target you must deprecate the old pack in staging first and bootstrap again. `--accept-existing` is for the other case — the target is already the version you want — and it still completes the Engine-archive registration, so a run that died between the bootstrap and the registration can be finished by re-running with it.
- **`.zip` only** (`parse_catalog_archive`), so a `.tar.gz` bundle is refused up front.
- **No avatar**, and **no confirmed Environment build** — see above.
- **Visibility is not configurable.** The bootstrap lane always creates the pack with `hide_market=true` and exposes no request field for it. The bundle records the source pack's own value for comparison only, and the result reports what this run actually did: `applied: true` only when the bootstrap published, `"unknown"` on the `--accept-existing` skip (an already-active pack's visibility cannot be read or changed through these channels), and `false` for a dry run or anything that stopped before the bootstrap. `expected: true` throughout, since that is the lane's fixed policy.

## Tests

`tests/unit/test_agent_pack_import.py` — 64 tests, no network, over `httpx.MockTransport`: target-org guards, the `.zip`-only refusal, source-directory derivation, re-nesting (root → nested, already-nested no-op, bounded), `prepare_archive` producing a nested archive carrying provenance, every branch of the decision table, the registration body carrying `org_id`, the plan listing only the token channels, bundle digest and layout refusals, the exact multipart form and headers the bootstrap receives, the staged-then-registered engine sequence with its headers, the displaced-submission and disabled-projection `incomplete` outcomes, the credential preflight making zero calls, the dry run issuing only GETs, the read-only client refusing a write, the org-capability probe (both org-resolution codes accepted, every other answer refused, the refusal naming route and code, the probe bodies asserted, the runtime route probed only when needed, a disallowed target org reported, and a response naming another org stopping the run), a lost registration finished by a later `--accept-existing` run, and the expansion bound enforced before anything decompresses - ahead of the manifest rewrite, and ahead of the bundle precheck's own manifest read.

Gates: `ruff check` + `ruff format --check` clean, all 8 `scripts/ci-lint/` guards, pyright clean on the new files, `pytest` 136 passed across both suites (72 + 64), full `tests/unit` 9098 passed / 5 skipped (the 21 collection errors are a pre-existing stale local venv, reproduced on unmodified `main`), actionlint clean. Nothing was run against production or staging.

## Notes

1. **Contract.** Verified against #3587 (see Depends on, above). If the field names ever change, the two call sites are `TargetChannels.bootstrap_catalog` and `build_runtime_asset_registration_body`.
2. **Size.** 2327 changed lines against `main`.







---

## feat(claw-interface): accept optional org_id on catalog bootstrap and runtime-asset lanes (#3587)

- **SHA**: `06c08d6b52fc60600866b7ac20a58db35765619d`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-29T08:00:52Z
- **PR**: #3587

### Commit Message

```
feat(claw-interface): accept optional org_id on catalog bootstrap and runtime-asset lanes (#3587)

## Motivation

The two token-authenticated Agent Pack CI lanes both hard-coded
`ZOOCLAW_ORG_ID = "zooclaw"` — the virtual official-directory org that
has no
`ecap-orgs` document. That makes it impossible to publish an
environment's Agent
Packs anywhere else.

We want to migrate the production Agent Packs into a dedicated **smoke
org** on
staging (a real team org, not `zooclaw`) so those Packs are visible only
to that
org's members and never enter the official catalog. This PR gives both
lanes an
optional org scope; nothing else about them changes.

## Contract

Both lanes take a new **optional** `org_id`. Omitted, blank, or
`"zooclaw"`
reproduces today's behavior byte for byte.

| Lane | Where the field goes | Field |
|---|---|---|
| `POST /agent-packs/bootstrap/catalog` (`X-Agent-Pack-Catalog-Token`) |
multipart form field | `org_id` — `str`, optional, `max_length=64` |
| `POST /agent-packs/runtime-assets` (`X-Agent-Pack-Runtime-Token`) |
JSON body field | `org_id` — `str`, optional, `max_length=64` |

Validation (shared helper
`app/services/pack_store/catalog_org_scope.py`):

- `None` / `""` / whitespace / `"zooclaw"` → resolves to `zooclaw`, with
**no
allowlist check and no DB lookup** (the official org deliberately has no
  `ecap-orgs` document).
- Anything else passes two gates, in order — both reject **before any
Pack
lookup, R2 upload, copy, or write**, and both carry `context={"org_id":
...}`:
  1. **Authorization** — the org must appear in the deployment's new
     `AGENT_PACK_LANE_TARGET_ORG_IDS` setting. Otherwise `400`
     `pack_catalog.target_org_not_allowed` /
     `pack_runtime_asset.target_org_not_allowed`.
  2. **Existence** — the org must have an `ecap-orgs` document
     (`org_repo.get_by_id`). Otherwise `400`
     `pack_catalog.target_org_not_found` /
     `pack_runtime_asset.target_org_not_found`.
- The org id is trimmed before use.

**Both lanes resolve `org_id` before every other input** — ahead of the
`display_id` shape check and archive parsing on the catalog lane, ahead
of the
Pack lookup on the runtime lane. See "Capability probe" below; the
ordering is
pinned by tests.

Responses now **echo `org_id`** (`AgentPackCatalogBootstrapResponse` and
`EngineRuntimeAssetRegistration`), so a caller can reconcile where the
Pack
actually landed rather than assuming its request scope. Additive —
existing
callers ignore the field.

`Org` has no lifecycle/status field, so **existence is the whole check**
— there
is no "active" flag to test. Membership is deliberately not consulted:
these are
machine-token lanes with no calling account.

Scoping is a strict filter, not a fallback. A `display_id` that exists
only
under `zooclaw` is **not** found when a different `org_id` is requested.

## Authorization boundary

`AGENT_PACK_LANE_TARGET_ORG_IDS` (`str`, default `""`) is the
deployment's
reviewed list of orgs these lanes may publish into: comma-separated, `*`
allows
any — the same parser shape as `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS`.
`zooclaw`
is always implicitly allowed.

Both remain **per-deployment machine credentials**, and their writable
org set is
exactly `zooclaw ∪ AGENT_PACK_LANE_TARGET_ORG_IDS`. Existence alone
would not
have been a boundary at all: the catalog token can mint *and*
auto-approve a
Pack, so every org that merely exists would have been a place a leaked
token
could plant one, and the runtime token could have swapped the Engine
archive of
any private Pack in the environment. The empty default therefore
confines both
tokens to the official catalog, exactly as before this PR.

Deployment (`services/claw-interface/kustomize/overlays/`):

- **staging** declares `AGENT_PACK_LANE_TARGET_ORG_IDS:
"760b7e6b226a4201ab997ac22aecf4e1"` — the smoke org the migrated
production
Packs land in. Org IDs are environment-local; the comment says so. Note
this
  stays an explicit list even though staging's neighbouring
`ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS` was just opened to `*` in #3586:
that
  one is a rollout gate, this one is an authorization boundary.
- **production** deliberately omits the variable, so both tokens stay
confined
  to `zooclaw`.
- `tests/unit/test_pack_runtime_asset_deployment_wiring.py` pins both
halves:
staging's exact value (and that it is not `*`), and that production has
no
  such env entry at all.

## Capability probe contract

The import side needs to know whether a given deployment understands
`org_id`.
`GET /admin/openapi.json` is not usable for that: on staging the
document is
643 KB and its first render took 35 s while blocking a single worker,
which
tripped the liveness probe and killed the pod. One cheap zero-write
request has
to answer instead, and these three properties are what make it work —
they are
contract, pinned by tests, not incidental:

1. **Every probe field is schema- *and* service-legal; only `org_id` is
fake.**
The probe must not lean on a deliberately malformed field, because
FastAPI
would reject that with a `422` at the request-model boundary, before the
handler runs — indistinguishable between old and new backends. The
importer
(`scripts/import_agent_pack.py`) therefore sends a valid `display_id`,
`source_directory` / `archive_key`, `archive_name`, and `sha256`, with
   `org_id = "0" * 32` as the only invalid value.
2. **`org_id` is resolved before any service-layer input handling.**
Ahead of
the `display_id` shape check and archive parsing on the catalog lane;
ahead
   of the Pack lookup on the runtime lane.
3. **The route-layer archive read is constant cost.** The catalog probe
uploads
a 1-byte `probe.zip`, so the handler's bounded read before the service
call
   is O(1) and never reaches the parser.

Probe outcomes:

- **new backend** → `400` `<lane>.target_org_not_found`, or
`<lane>.target_org_not_allowed` on a deployment whose allowlist omits
the org
(the default) — decided before the archive is parsed or a Pack is looked
up;
- **old backend** → ignores the unknown `org_id` field and fails on the
archive
  (catalog) or with `pack.not_found` (runtime assets).

Pinned by:

- Route-level `TestClient` tests on both endpoints
(`test_capability_probe_*`
/ `test_runtime_asset_capability_probe_*`) replaying the importer's
exact
payload with a valid token, asserting the `400` body code, with the
archive
parser, the Pack lookup, and the R2 client / archive copy all patched to
raise
  if reached.
- `test_target_org_is_resolved_before_any_other_input` in both service
test
files, where every other argument is independently invalid and the org
error
  is still the one that surfaces.

## What the scope covers

Catalog bootstrap — every previously hard-coded `zooclaw` reference now
follows
the target org: duplicate lookup, `create_pack`, the R2 `storage_key`
prefix and
its object metadata, `submit_new_version`, and every submission re-read.
Where a
`Pack` was already in hand the code now reads `pack.org_id` instead of
the
constant, so the org can never drift mid-request.

Runtime assets — only the `get_by_org_and_display_id(...)` lookup was
hard-coded;
everything downstream already used `pack.org_id`, and still does.

Unchanged: `hide_market=True`, `published_by=BOOTSTRAP_ACTOR_UID`, the
create-only / resume / conflict semantics of `_resolve_existing`, the
publisher-run fencing, and the `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS`
allowlist
(still keyed on `pack_id`).

## Compatibility

Zero behavior change for existing callers. Neither lane's caller sends
`org_id`
today, so both resolve to `zooclaw` and skip the org lookup entirely. No
existing test assertions were modified.

## Org-related notes for the migration

- `agents_v2_access.agents_v2_enabled()` is a global `AGENTS_V2_ENABLED`
settings flag with no org dimension, so the dark-mode Environment
projection
  branch behaves identically under a private org.
- **Hire-side visibility needs no change** (verified, not modified):
`GET /orgs/{org_id}/packs` calls `list_packs(org_id=..., status=...)`
with
`hide_market=None`, so no `hide_market` filter is applied and members
see the
Pack. `pack_repo.get_by_org_and_display_id` likewise has no
`hide_market`
  filter. Only the public catalog `GET /agent-packs` filters
  `hide_market=False`, and it is additionally scoped to `zooclaw`.
- Installing such a Pack goes through `derive_pack_source`, which
returns
`"private"` (not `"official"`) when `pack.org_id == org_id` — so it
installs
  as an ordinary org-private Pack. `requires_payment` is false for
  bootstrap-created Packs, so the purchase gate is a no-op.

## Tests

New coverage in `tests/unit/`:

- `test_catalog_org_scope.py` — default/blank/`zooclaw` resolve with no
allowlist check and no lookup; an allowlisted org resolves and is
trimmed; `*`
  admits any existing org; an org outside the list (empty default, and a
non-empty list that omits it) is rejected as `target_org_not_allowed`
with no
lookup at all; an allowlisted org with no `ecap-orgs` document is
rejected as
  `target_org_not_found`, each with the calling lane's prefix and a 400.
- `test_catalog_bootstrap_service.py` — a real `org_id` scopes the
duplicate
lookup, `create_pack`, the storage key prefix, the R2 object metadata,
and
`submit_new_version`, while keeping `hide_market: true`; a rejected
`org_id`
— both the not-allowed and the not-found reason — does zero work (no
lookup,
no create, no submit, no R2 client); omitting the field stays on
`zooclaw`
  with no org lookup.
- `test_runtime_asset_registration_service.py` — a real `org_id` scopes
the
display_id lookup, the archive copy destination, and the submission
write; a
miss under that org does **not** fall back to the `zooclaw` Pack of the
same
`display_id`; a rejected `org_id` — not-allowed and not-found alike —
never
reaches a Pack lookup, copy, or write; omitting the field stays on
`zooclaw`.
- Route-level `TestClient` tests on both endpoints proving the new field
is
  actually parsed and forwarded, and that omitting it forwards `None`.
- Echo assertions on both lanes' responses, plus the updated exact-shape
  assertion in `test_active_pack_is_returned_without_mutation`.

Shared builder `make_org` added to `tests/unit/_builders.py` (and reused
by the
existing `make_org_member`) rather than redefining an Org factory per
file.

Gates run locally: `ruff check`, `ruff format --check`, `pyright app/
tests/`
(0 errors), `lint-imports` (8/8 contracts kept), the full
`scripts/ci-lint/0*.sh`
guard set (file length, complexity, deptry, collection names,
importlinter repo
sync, vulture, database-pydantic-returns), and the whole backend unit
suite — all
clean.

## Docs

Both design specs gained an "Optional org scope" section describing the
field,
the two-gate validation rule, the error codes, the per-environment
allowlist,
the resolve-first ordering with its probe rationale, and the echoed
`org_id`.
```

### PR Body

## Motivation

The two token-authenticated Agent Pack CI lanes both hard-coded
`ZOOCLAW_ORG_ID = "zooclaw"` — the virtual official-directory org that has no
`ecap-orgs` document. That makes it impossible to publish an environment's Agent
Packs anywhere else.

We want to migrate the production Agent Packs into a dedicated **smoke org** on
staging (a real team org, not `zooclaw`) so those Packs are visible only to that
org's members and never enter the official catalog. This PR gives both lanes an
optional org scope; nothing else about them changes.

## Contract

Both lanes take a new **optional** `org_id`. Omitted, blank, or `"zooclaw"`
reproduces today's behavior byte for byte.

| Lane | Where the field goes | Field |
|---|---|---|
| `POST /agent-packs/bootstrap/catalog` (`X-Agent-Pack-Catalog-Token`) | multipart form field | `org_id` — `str`, optional, `max_length=64` |
| `POST /agent-packs/runtime-assets` (`X-Agent-Pack-Runtime-Token`) | JSON body field | `org_id` — `str`, optional, `max_length=64` |

Validation (shared helper `app/services/pack_store/catalog_org_scope.py`):

- `None` / `""` / whitespace / `"zooclaw"` → resolves to `zooclaw`, with **no
  allowlist check and no DB lookup** (the official org deliberately has no
  `ecap-orgs` document).
- Anything else passes two gates, in order — both reject **before any Pack
  lookup, R2 upload, copy, or write**, and both carry `context={"org_id": ...}`:
  1. **Authorization** — the org must appear in the deployment's new
     `AGENT_PACK_LANE_TARGET_ORG_IDS` setting. Otherwise `400`
     `pack_catalog.target_org_not_allowed` /
     `pack_runtime_asset.target_org_not_allowed`.
  2. **Existence** — the org must have an `ecap-orgs` document
     (`org_repo.get_by_id`). Otherwise `400`
     `pack_catalog.target_org_not_found` /
     `pack_runtime_asset.target_org_not_found`.
- The org id is trimmed before use.

**Both lanes resolve `org_id` before every other input** — ahead of the
`display_id` shape check and archive parsing on the catalog lane, ahead of the
Pack lookup on the runtime lane. See "Capability probe" below; the ordering is
pinned by tests.

Responses now **echo `org_id`** (`AgentPackCatalogBootstrapResponse` and
`EngineRuntimeAssetRegistration`), so a caller can reconcile where the Pack
actually landed rather than assuming its request scope. Additive — existing
callers ignore the field.

`Org` has no lifecycle/status field, so **existence is the whole check** — there
is no "active" flag to test. Membership is deliberately not consulted: these are
machine-token lanes with no calling account.

Scoping is a strict filter, not a fallback. A `display_id` that exists only
under `zooclaw` is **not** found when a different `org_id` is requested.

## Authorization boundary

`AGENT_PACK_LANE_TARGET_ORG_IDS` (`str`, default `""`) is the deployment's
reviewed list of orgs these lanes may publish into: comma-separated, `*` allows
any — the same parser shape as `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS`. `zooclaw`
is always implicitly allowed.

Both remain **per-deployment machine credentials**, and their writable org set is
exactly `zooclaw ∪ AGENT_PACK_LANE_TARGET_ORG_IDS`. Existence alone would not
have been a boundary at all: the catalog token can mint *and* auto-approve a
Pack, so every org that merely exists would have been a place a leaked token
could plant one, and the runtime token could have swapped the Engine archive of
any private Pack in the environment. The empty default therefore confines both
tokens to the official catalog, exactly as before this PR.

Deployment (`services/claw-interface/kustomize/overlays/`):

- **staging** declares `AGENT_PACK_LANE_TARGET_ORG_IDS:
  "760b7e6b226a4201ab997ac22aecf4e1"` — the smoke org the migrated production
  Packs land in. Org IDs are environment-local; the comment says so. Note this
  stays an explicit list even though staging's neighbouring
  `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS` was just opened to `*` in #3586: that
  one is a rollout gate, this one is an authorization boundary.
- **production** deliberately omits the variable, so both tokens stay confined
  to `zooclaw`.
- `tests/unit/test_pack_runtime_asset_deployment_wiring.py` pins both halves:
  staging's exact value (and that it is not `*`), and that production has no
  such env entry at all.

## Capability probe contract

The import side needs to know whether a given deployment understands `org_id`.
`GET /admin/openapi.json` is not usable for that: on staging the document is
643 KB and its first render took 35 s while blocking a single worker, which
tripped the liveness probe and killed the pod. One cheap zero-write request has
to answer instead, and these three properties are what make it work — they are
contract, pinned by tests, not incidental:

1. **Every probe field is schema- *and* service-legal; only `org_id` is fake.**
   The probe must not lean on a deliberately malformed field, because FastAPI
   would reject that with a `422` at the request-model boundary, before the
   handler runs — indistinguishable between old and new backends. The importer
   (`scripts/import_agent_pack.py`) therefore sends a valid `display_id`,
   `source_directory` / `archive_key`, `archive_name`, and `sha256`, with
   `org_id = "0" * 32` as the only invalid value.
2. **`org_id` is resolved before any service-layer input handling.** Ahead of
   the `display_id` shape check and archive parsing on the catalog lane; ahead
   of the Pack lookup on the runtime lane.
3. **The route-layer archive read is constant cost.** The catalog probe uploads
   a 1-byte `probe.zip`, so the handler's bounded read before the service call
   is O(1) and never reaches the parser.

Probe outcomes:

- **new backend** → `400` `<lane>.target_org_not_found`, or
  `<lane>.target_org_not_allowed` on a deployment whose allowlist omits the org
  (the default) — decided before the archive is parsed or a Pack is looked up;
- **old backend** → ignores the unknown `org_id` field and fails on the archive
  (catalog) or with `pack.not_found` (runtime assets).

Pinned by:

- Route-level `TestClient` tests on both endpoints (`test_capability_probe_*`
  / `test_runtime_asset_capability_probe_*`) replaying the importer's exact
  payload with a valid token, asserting the `400` body code, with the archive
  parser, the Pack lookup, and the R2 client / archive copy all patched to raise
  if reached.
- `test_target_org_is_resolved_before_any_other_input` in both service test
  files, where every other argument is independently invalid and the org error
  is still the one that surfaces.

## What the scope covers

Catalog bootstrap — every previously hard-coded `zooclaw` reference now follows
the target org: duplicate lookup, `create_pack`, the R2 `storage_key` prefix and
its object metadata, `submit_new_version`, and every submission re-read. Where a
`Pack` was already in hand the code now reads `pack.org_id` instead of the
constant, so the org can never drift mid-request.

Runtime assets — only the `get_by_org_and_display_id(...)` lookup was hard-coded;
everything downstream already used `pack.org_id`, and still does.

Unchanged: `hide_market=True`, `published_by=BOOTSTRAP_ACTOR_UID`, the
create-only / resume / conflict semantics of `_resolve_existing`, the
publisher-run fencing, and the `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS` allowlist
(still keyed on `pack_id`).

## Compatibility

Zero behavior change for existing callers. Neither lane's caller sends `org_id`
today, so both resolve to `zooclaw` and skip the org lookup entirely. No
existing test assertions were modified.

## Org-related notes for the migration

- `agents_v2_access.agents_v2_enabled()` is a global `AGENTS_V2_ENABLED`
  settings flag with no org dimension, so the dark-mode Environment projection
  branch behaves identically under a private org.
- **Hire-side visibility needs no change** (verified, not modified):
  `GET /orgs/{org_id}/packs` calls `list_packs(org_id=..., status=...)` with
  `hide_market=None`, so no `hide_market` filter is applied and members see the
  Pack. `pack_repo.get_by_org_and_display_id` likewise has no `hide_market`
  filter. Only the public catalog `GET /agent-packs` filters
  `hide_market=False`, and it is additionally scoped to `zooclaw`.
- Installing such a Pack goes through `derive_pack_source`, which returns
  `"private"` (not `"official"`) when `pack.org_id == org_id` — so it installs
  as an ordinary org-private Pack. `requires_payment` is false for
  bootstrap-created Packs, so the purchase gate is a no-op.

## Tests

New coverage in `tests/unit/`:

- `test_catalog_org_scope.py` — default/blank/`zooclaw` resolve with no
  allowlist check and no lookup; an allowlisted org resolves and is trimmed; `*`
  admits any existing org; an org outside the list (empty default, and a
  non-empty list that omits it) is rejected as `target_org_not_allowed` with no
  lookup at all; an allowlisted org with no `ecap-orgs` document is rejected as
  `target_org_not_found`, each with the calling lane's prefix and a 400.
- `test_catalog_bootstrap_service.py` — a real `org_id` scopes the duplicate
  lookup, `create_pack`, the storage key prefix, the R2 object metadata, and
  `submit_new_version`, while keeping `hide_market: true`; a rejected `org_id`
  — both the not-allowed and the not-found reason — does zero work (no lookup,
  no create, no submit, no R2 client); omitting the field stays on `zooclaw`
  with no org lookup.
- `test_runtime_asset_registration_service.py` — a real `org_id` scopes the
  display_id lookup, the archive copy destination, and the submission write; a
  miss under that org does **not** fall back to the `zooclaw` Pack of the same
  `display_id`; a rejected `org_id` — not-allowed and not-found alike — never
  reaches a Pack lookup, copy, or write; omitting the field stays on `zooclaw`.
- Route-level `TestClient` tests on both endpoints proving the new field is
  actually parsed and forwarded, and that omitting it forwards `None`.
- Echo assertions on both lanes' responses, plus the updated exact-shape
  assertion in `test_active_pack_is_returned_without_mutation`.

Shared builder `make_org` added to `tests/unit/_builders.py` (and reused by the
existing `make_org_member`) rather than redefining an Org factory per file.

Gates run locally: `ruff check`, `ruff format --check`, `pyright app/ tests/`
(0 errors), `lint-imports` (8/8 contracts kept), the full `scripts/ci-lint/0*.sh`
guard set (file length, complexity, deptry, collection names, importlinter repo
sync, vulture, database-pydantic-returns), and the whole backend unit suite — all
clean.

## Docs

Both design specs gained an "Optional org scope" section describing the field,
the two-gate validation rule, the error codes, the per-environment allowlist,
the resolve-first ordering with its probe rationale, and the echoed `org_id`.


---

## feat(claw-interface): export agent packs into a portable bundle (#3584)

- **SHA**: `631325d5c69aa1d170553feff713f84590239dfc`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-29T07:15:31Z
- **PR**: #3584

### Commit Message

```
feat(claw-interface): export agent packs into a portable bundle (#3584)

Part 1 of 2 for #3580. This is the **read half**: it produces a portable
bundle from a source environment. The import half — which replays a
bundle into a target environment over its public HTTP API, plus the
`workflow_dispatch` that drives both — is stacked on top in #3583.

Split out of #3583 because the combined change was +3376 lines, above
the repo's 3000-line PR size gate, which skips every downstream quality
job.

## Why

Staging smokes
([zooclaw-engine#996](https://github.com/SerendipityOneInc/zooclaw-engine/issues/996))
need three production-only packs — two in a personal org, one hidden in
`zooclaw` — to exist in staging. A pack can only enter an environment
through the official catalog bootstrap lane or the Agent Studio publish
route, and `archive_copy.py` copies archives only within one
environment.

## Source access is strictly read-only

`scripts/export_agent_pack.py` opens its own Mongo client (`find` /
`find_one` on `ecap-packs` and `ecap-pack-submissions`), its own R2
client (`get_object`), and an HTTP client that only `GET`s the avatar
URL. There is no write path in the module, and it never imports the
service's repositories, publish services, or settings singleton — so it
cannot be pointed at a target environment by accident, and it runs with
no `MONGODB_*` configuration of its own.

A paid listing is refused immediately after the pack row is read —
before the submission is fetched, before the archive is downloaded, and
before the bundle directory is created.

## Archive layout is normalised here, not discovered later

`validate_archive_upload` requires `agent-pack.yaml`, `AGENTS.md`,
`SOUL.md` and `IDENTITY.md` at the archive **root**, but catalog and
Agent Studio archives nest everything under one top-level directory.
Exporting such an archive unchanged means the target rejects it only
*after* the pack row and the upload already exist.

`normalize_archive_layout` strips the single top-level directory at
export: every member keeps its bytes, the container format is unchanged,
and `agent-pack.yaml` itself is not touched — so the import still
rewrites it exactly once. The result is recorded at
`files.archive.layout` as `root` or `normalized_from:<dir>`.

The decision is made **from member names alone** — the zip central
directory and the tar headers — so an archive that is already
root-layout is returned untouched without a byte of payload being read.
Only the repacking path extracts anything, and before it does, the
declared expanded size is checked against a per-member bound (100 MiB,
matching the target's own upload limit) and an aggregate bound (512
MiB). A compression bomb is refused rather than expanded, and the repack
streams member by member so one payload is in flight at a time. An
archive with no root manifest and no single top-level directory, or one
whose root set is still incomplete after stripping, or one carrying a
reserved top-level directory, fails the export with a precise message.
The rules come from `archive_service`'s own `REQUIRED_ROOT_FILES` /
`FORBIDDEN_TOP_LEVEL_DIRS`, imported rather than restated.

## Avatar fetching is allowlisted, https-only and size-capped

`avatar_url` is an unconstrained string on a Mongo document, so fetching
it is an SSRF primitive. The download is now restricted to hosts an
operator named — `SOURCE_AVATAR_ALLOWED_HOSTS` (comma-separated), or the
single `SOURCE_R2_PUBLIC_DOMAIN` that `/storage/r2/presign` builds every
avatar `public_url` from — https only, with IP literals, `localhost` and
private/link-local/reserved ranges refused. Redirects are followed by
hand so **every hop** is re-checked against the allowlist (a permitted
host answering 302 would otherwise be an open relay), capped at five.
The body is streamed with `aiter_bytes` and aborted past 8 MiB rather
than buffered through `.content`.

There is deliberately **no default allowlist**: the media host is
deployment configuration (`vars.R2_PUBLIC_DOMAIN` in this repo's deploy
workflows), so an un-allowlisted download is refused rather than
guessed. `--skip-avatar` opts out entirely.

## Bundle layout

```
bundle/
  manifest.json                     provenance + pack/submission projection + file digests
  files/archive.zip | .tar.gz       the published submission archive, byte-for-byte
  files/engine-archive.<ext>        the pinned Engine runtime archive, when there is one
  files/avatar.<ext>                the pack avatar, when the pack has one
```

`manifest.json` records the source environment, org, pack, submission,
pack version, archive SHA-256 and export timestamp, plus the
pack/submission metadata the target will need. Every payload carries its
own SHA-256 and byte length, so a consumer can refuse a corrupted or
truncated copy before acting on it (`verify_bundle_file`).

## The Engine runtime archive travels with the bundle

A pack whose submission pins an Engine runtime archive needs that
archive on the target too: without it the target can only build a V1
Environment, and an Engine (V2) hire fails with
`agent.pack_environment_not_ready`. `PackRuntimeAsset.asset_id` is a
protected object key in the same pack bucket as the submission archive
(never a URL), so the same read-only reader fetches it.

It lands as `files/engine-archive.<ext>` with its digest and length,
alongside the `archive_name` and `publisher_run_number` that the
import's registration request needs. The export refuses a byte stream
whose digest disagrees with the one recorded on the source submission.

When the source has no Engine archive, `files.engine_archive` is `null`
and both the export result (`engine_archive_captured` /
`engine_archive_note`) and the bundle notes say what that means for the
target — an explicit, visible V1-only outcome rather than a silent one.
The import half (#3583) does the registration.

## Provenance is written into the archive, not a new field

`release_notes` is archive-derived server-side — `submit_new_version`
takes it from the parsed `agent-pack.yaml`, never from the request body
— so provenance can only be carried by rewriting the manifest inside the
archive. `rewrite_archive_manifest` does exactly that and copies every
other member byte-for-byte. No Pack/PackSubmission schema change, and
`origin_*` stays reserved for real listing forks. The block is
machine-readable (`parse_provenance_release_notes`), which is what lets
the import half recognise its own earlier work on a rerun.

The manifest itself is a YAML round-trip, so comments and key order
inside `agent-pack.yaml` are not preserved — acceptable for
machine-consumed metadata, and the pristine original stays in the
bundle.

## Both archive formats

`.zip` and `.tar.gz` are the two formats the target accepts
(`archive_service.SUPPORTED_ARCHIVE_EXTENSIONS`, and the
r2-access-worker's extension check agrees). Both are read and rewritten
in place; the source extension is preserved into the bundle and recorded
at `files.archive.format`. Nothing is repacked into another container,
and an unrecognised extension fails at export with an explicit message.

## Other rules

- **Refused:** paid listings (`requires_payment` / `price_id` set) —
Stripe products are not migrated across environments.
- Source metadata from Mongo wins over archive-derived values (operators
edit listing metadata after the archive is built); the archive supplies
the fields Mongo does not carry.

## Usage

```bash
python -m scripts.export_agent_pack --display-id industry-news-buddy \
    --source-org-id d44743fd764441579e3fb7b6ca1f3c62 --out ./bundle
```

Environment (all read-only): `SOURCE_MONGODB_URI` (or
`SOURCE_MONGODB_{USER,PASSWORD,HOST}`), `SOURCE_MONGODB_NAME`,
`SOURCE_R2_ENDPOINT_URL`, `SOURCE_R2_ACCESS_KEY_ID`,
`SOURCE_R2_ACCESS_KEY_SECRET`, `SOURCE_R2_AGENT_PACKS_BUCKET_NAME`, plus
`SOURCE_R2_PUBLIC_DOMAIN` (or `SOURCE_AVATAR_ALLOWED_HOSTS`) unless
`--skip-avatar` is passed.

## Tests

`tests/unit/test_agent_pack_migration_core.py` — 60 tests, no network:
source-config parsing, archive manifest read/rewrite for zip **and**
tar.gz at both root and nested layouts (asserting every other member
stays byte-identical), format detection and its rejection path,
provenance rendering, bundle manifest JSON round-trip and its rejections
(unknown `bundle_version`, path traversal), export manifest assembly,
and the digest checks (tampered same-length payload, truncated payload,
avatar).

Plus, for the review findings above: nested zip **and** nested tar
normalised to the root layout with member bytes unchanged and the
manifest left alone, a root archive passed through untouched, and the
three normalisation refusals (no single top-level directory, incomplete
root set, forbidden top-level directory); the avatar allowlist over
`httpx.MockTransport` — off-allowlist host, redirect to an off-allowlist
host, redirect that stays allowlisted, `http` scheme, IP literal /
`localhost` / link-local / private address, oversize stream aborted,
redirect loop; and `export_bundle`-level tests that a paid pack leaves
no bundle directory behind and never downloads anything, that a nested
source archive lands root-layout in the bundle with the recorded digest
matching, and that a root archive is recorded as `root`. Plus the Engine
archive capture: it is downloaded into the bundle with its digest, name
and `publisher_run_number`, a digest that disagrees with the source
submission is refused, a source without one reports the explicit V1-only
note, and a manifest carrying one round-trips through JSON. And for the
expansion bound: a root zip **and** a root tar are returned without any
member read (the payload readers are monkeypatched to raise), a nested
archive over the aggregate cap and one over the per-member cap are both
refused before the repacker is reached, and a nested archive under the
caps still normalises with member bytes unchanged.

Shared fixtures live in `tests/unit/_agent_pack_builders.py` following
the repo's `_builders.py` convention; the stacked import PR reuses them.

The archive fixtures are byte-reproducible: `ZipFile.writestr` stamps
`time.localtime()` (two-second DOS resolution) and gzip stamps its own
header, so two builds straddling a boundary produced different bytes and
any digest comparison failed at random. Members now carry a fixed
`ZipInfo.date_time` and the tar stream is wrapped in
`GzipFile(mtime=0)`.

Gates run: `ruff check` + `ruff format --check` clean, all 8
`scripts/ci-lint/` guards pass, pyright clean on the new files, and the
suite above green. Nothing was run against production or staging.

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

Part 1 of 2 for #3580. This is the **read half**: it produces a portable bundle from a source environment. The import half — which replays a bundle into a target environment over its public HTTP API, plus the `workflow_dispatch` that drives both — is stacked on top in #3583.

Split out of #3583 because the combined change was +3376 lines, above the repo's 3000-line PR size gate, which skips every downstream quality job.

## Why

Staging smokes ([zooclaw-engine#996](https://github.com/SerendipityOneInc/zooclaw-engine/issues/996)) need three production-only packs — two in a personal org, one hidden in `zooclaw` — to exist in staging. A pack can only enter an environment through the official catalog bootstrap lane or the Agent Studio publish route, and `archive_copy.py` copies archives only within one environment.

## Source access is strictly read-only

`scripts/export_agent_pack.py` opens its own Mongo client (`find` / `find_one` on `ecap-packs` and `ecap-pack-submissions`), its own R2 client (`get_object`), and an HTTP client that only `GET`s the avatar URL. There is no write path in the module, and it never imports the service's repositories, publish services, or settings singleton — so it cannot be pointed at a target environment by accident, and it runs with no `MONGODB_*` configuration of its own.

A paid listing is refused immediately after the pack row is read — before the submission is fetched, before the archive is downloaded, and before the bundle directory is created.

## Archive layout is normalised here, not discovered later

`validate_archive_upload` requires `agent-pack.yaml`, `AGENTS.md`, `SOUL.md` and `IDENTITY.md` at the archive **root**, but catalog and Agent Studio archives nest everything under one top-level directory. Exporting such an archive unchanged means the target rejects it only *after* the pack row and the upload already exist.

`normalize_archive_layout` strips the single top-level directory at export: every member keeps its bytes, the container format is unchanged, and `agent-pack.yaml` itself is not touched — so the import still rewrites it exactly once. The result is recorded at `files.archive.layout` as `root` or `normalized_from:<dir>`.

The decision is made **from member names alone** — the zip central directory and the tar headers — so an archive that is already root-layout is returned untouched without a byte of payload being read. Only the repacking path extracts anything, and before it does, the declared expanded size is checked against a per-member bound (100 MiB, matching the target's own upload limit) and an aggregate bound (512 MiB). A compression bomb is refused rather than expanded, and the repack streams member by member so one payload is in flight at a time. An archive with no root manifest and no single top-level directory, or one whose root set is still incomplete after stripping, or one carrying a reserved top-level directory, fails the export with a precise message. The rules come from `archive_service`'s own `REQUIRED_ROOT_FILES` / `FORBIDDEN_TOP_LEVEL_DIRS`, imported rather than restated.

## Avatar fetching is allowlisted, https-only and size-capped

`avatar_url` is an unconstrained string on a Mongo document, so fetching it is an SSRF primitive. The download is now restricted to hosts an operator named — `SOURCE_AVATAR_ALLOWED_HOSTS` (comma-separated), or the single `SOURCE_R2_PUBLIC_DOMAIN` that `/storage/r2/presign` builds every avatar `public_url` from — https only, with IP literals, `localhost` and private/link-local/reserved ranges refused. Redirects are followed by hand so **every hop** is re-checked against the allowlist (a permitted host answering 302 would otherwise be an open relay), capped at five. The body is streamed with `aiter_bytes` and aborted past 8 MiB rather than buffered through `.content`.

There is deliberately **no default allowlist**: the media host is deployment configuration (`vars.R2_PUBLIC_DOMAIN` in this repo's deploy workflows), so an un-allowlisted download is refused rather than guessed. `--skip-avatar` opts out entirely.

## Bundle layout

```
bundle/
  manifest.json                     provenance + pack/submission projection + file digests
  files/archive.zip | .tar.gz       the published submission archive, byte-for-byte
  files/engine-archive.<ext>        the pinned Engine runtime archive, when there is one
  files/avatar.<ext>                the pack avatar, when the pack has one
```

`manifest.json` records the source environment, org, pack, submission, pack version, archive SHA-256 and export timestamp, plus the pack/submission metadata the target will need. Every payload carries its own SHA-256 and byte length, so a consumer can refuse a corrupted or truncated copy before acting on it (`verify_bundle_file`).

## The Engine runtime archive travels with the bundle

A pack whose submission pins an Engine runtime archive needs that archive on the target too: without it the target can only build a V1 Environment, and an Engine (V2) hire fails with `agent.pack_environment_not_ready`. `PackRuntimeAsset.asset_id` is a protected object key in the same pack bucket as the submission archive (never a URL), so the same read-only reader fetches it.

It lands as `files/engine-archive.<ext>` with its digest and length, alongside the `archive_name` and `publisher_run_number` that the import's registration request needs. The export refuses a byte stream whose digest disagrees with the one recorded on the source submission.

When the source has no Engine archive, `files.engine_archive` is `null` and both the export result (`engine_archive_captured` / `engine_archive_note`) and the bundle notes say what that means for the target — an explicit, visible V1-only outcome rather than a silent one. The import half (#3583) does the registration.

## Provenance is written into the archive, not a new field

`release_notes` is archive-derived server-side — `submit_new_version` takes it from the parsed `agent-pack.yaml`, never from the request body — so provenance can only be carried by rewriting the manifest inside the archive. `rewrite_archive_manifest` does exactly that and copies every other member byte-for-byte. No Pack/PackSubmission schema change, and `origin_*` stays reserved for real listing forks. The block is machine-readable (`parse_provenance_release_notes`), which is what lets the import half recognise its own earlier work on a rerun.

The manifest itself is a YAML round-trip, so comments and key order inside `agent-pack.yaml` are not preserved — acceptable for machine-consumed metadata, and the pristine original stays in the bundle.

## Both archive formats

`.zip` and `.tar.gz` are the two formats the target accepts (`archive_service.SUPPORTED_ARCHIVE_EXTENSIONS`, and the r2-access-worker's extension check agrees). Both are read and rewritten in place; the source extension is preserved into the bundle and recorded at `files.archive.format`. Nothing is repacked into another container, and an unrecognised extension fails at export with an explicit message.

## Other rules

- **Refused:** paid listings (`requires_payment` / `price_id` set) — Stripe products are not migrated across environments.
- Source metadata from Mongo wins over archive-derived values (operators edit listing metadata after the archive is built); the archive supplies the fields Mongo does not carry.

## Usage

```bash
python -m scripts.export_agent_pack --display-id industry-news-buddy \
    --source-org-id d44743fd764441579e3fb7b6ca1f3c62 --out ./bundle
```

Environment (all read-only): `SOURCE_MONGODB_URI` (or `SOURCE_MONGODB_{USER,PASSWORD,HOST}`), `SOURCE_MONGODB_NAME`, `SOURCE_R2_ENDPOINT_URL`, `SOURCE_R2_ACCESS_KEY_ID`, `SOURCE_R2_ACCESS_KEY_SECRET`, `SOURCE_R2_AGENT_PACKS_BUCKET_NAME`, plus `SOURCE_R2_PUBLIC_DOMAIN` (or `SOURCE_AVATAR_ALLOWED_HOSTS`) unless `--skip-avatar` is passed.

## Tests

`tests/unit/test_agent_pack_migration_core.py` — 60 tests, no network: source-config parsing, archive manifest read/rewrite for zip **and** tar.gz at both root and nested layouts (asserting every other member stays byte-identical), format detection and its rejection path, provenance rendering, bundle manifest JSON round-trip and its rejections (unknown `bundle_version`, path traversal), export manifest assembly, and the digest checks (tampered same-length payload, truncated payload, avatar).

Plus, for the review findings above: nested zip **and** nested tar normalised to the root layout with member bytes unchanged and the manifest left alone, a root archive passed through untouched, and the three normalisation refusals (no single top-level directory, incomplete root set, forbidden top-level directory); the avatar allowlist over `httpx.MockTransport` — off-allowlist host, redirect to an off-allowlist host, redirect that stays allowlisted, `http` scheme, IP literal / `localhost` / link-local / private address, oversize stream aborted, redirect loop; and `export_bundle`-level tests that a paid pack leaves no bundle directory behind and never downloads anything, that a nested source archive lands root-layout in the bundle with the recorded digest matching, and that a root archive is recorded as `root`. Plus the Engine archive capture: it is downloaded into the bundle with its digest, name and `publisher_run_number`, a digest that disagrees with the source submission is refused, a source without one reports the explicit V1-only note, and a manifest carrying one round-trips through JSON. And for the expansion bound: a root zip **and** a root tar are returned without any member read (the payload readers are monkeypatched to raise), a nested archive over the aggregate cap and one over the per-member cap are both refused before the repacker is reached, and a nested archive under the caps still normalises with member bytes unchanged.

Shared fixtures live in `tests/unit/_agent_pack_builders.py` following the repo's `_builders.py` convention; the stacked import PR reuses them.

The archive fixtures are byte-reproducible: `ZipFile.writestr` stamps `time.localtime()` (two-second DOS resolution) and gzip stamps its own header, so two builds straddling a boundary produced different bytes and any digest comparison failed at random. Members now carry a fixed `ZipInfo.date_time` and the tar stream is wrapped in `GzipFile(mtime=0)`.

Gates run: `ruff check` + `ruff format --check` clean, all 8 `scripts/ci-lint/` guards pass, pyright clean on the new files, and the suite above green. Nothing was run against production or staging.


---

## chore(claw-interface): open staging engine runtime-asset gate to all packs (#3586)

- **SHA**: `fe6bf546cb421d9f9f093eb789ccf6d8d0b1c170`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-29T06:59:36Z
- **PR**: #3586

### Commit Message

```
chore(claw-interface): open staging engine runtime-asset gate to all packs (#3586)

## Why

`ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS` is set as an explicit `env` entry
in the staging kustomize overlay, which wins over the Vault-backed
`envFrom` value (changing it in Vault is a no-op). Agent Pack migration
(#3583) bootstraps production packs into a dedicated staging smoke org
and mints a new `pack_id` per import, so every migrated pack would need
a follow-up overlay PR before Engine consumers select its V2 archive.

## What

- Staging overlay: `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS: "*"` (parser in
`pack_runtime_asset._pack_id_is_enabled` already accepts the wildcard).
- Production overlay untouched; it keeps its reviewed explicit list per
`docs/superpowers/specs/2026-08-20-engine-pack-environment-local-gate.md`.

## Note on the gate design

The spec treats the list as environment-local reviewed configuration.
This PR relaxes only staging, where the master switch has been on since
#3461 and all local packs are test data; the master switch stays
authoritative.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01VRz5q6Evgj42xoLucxuCE9
```

### PR Body

## Why

`ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS` is set as an explicit `env` entry in the staging kustomize overlay, which wins over the Vault-backed `envFrom` value (changing it in Vault is a no-op). Agent Pack migration (#3583) bootstraps production packs into a dedicated staging smoke org and mints a new `pack_id` per import, so every migrated pack would need a follow-up overlay PR before Engine consumers select its V2 archive.

## What

- Staging overlay: `ENGINE_PACK_RUNTIME_ASSETS_PACK_IDS: "*"` (parser in `pack_runtime_asset._pack_id_is_enabled` already accepts the wildcard).
- Production overlay untouched; it keeps its reviewed explicit list per `docs/superpowers/specs/2026-08-20-engine-pack-environment-local-gate.md`.

## Note on the gate design

The spec treats the list as environment-local reviewed configuration. This PR relaxes only staging, where the master switch has been on since #3461 and all local packs are test data; the master switch stays authoritative.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01VRz5q6Evgj42xoLucxuCE9


---

## build(deps-dev): update ruff requirement from >=0.16.3 to >=0.16.4 in /services/claw-interface (#3581)

- **SHA**: `044c6f70a854c9e497a418a16e8021205837e8bb`
- **作者**: dependabot[bot]
- **日期**: 2026-08-29T02:44:39Z
- **PR**: #3581

### Commit Message

```
build(deps-dev): update ruff requirement from >=0.16.3 to >=0.16.4 in /services/claw-interface (#3581)

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to
permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/releases">ruff's
releases</a>.</em></p>
<blockquote>
<h2>0.16.4</h2>
<h2>Release Notes</h2>
<p>Released on 2026-08-20.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>flake8-use-pathlib</code>] Add autofix for
<code>PTH116</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26460">#26460</a>)</li>
<li>[<code>refurb</code>] Restrict <code>delete-full-slice</code> to
lists (<code>FURB131</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27711">#27711</a>)</li>
<li>[<code>refurb</code>] Skip <code>FURB101</code> and
<code>FURB103</code> when the <code>open</code> argument is a file
descriptor (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27643">#27643</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Fix <code>InvalidInstruction</code> on Windows CPUs that do not
support <code>POPCNT</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27803">#27803</a>)</li>
<li>[<code>pyflakes</code>] Emit semantic syntax errors in string type
definitions as <code>F722</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27835">#27835</a>)</li>
<li>[<code>pylint</code>] Allow <code>os._exit</code> imports in
<code>import-private-name</code> (<code>PLC2701</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27738">#27738</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[syntax-errors] Align mixed t-string/bytes error message with
CPython 3.14 (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27766">#27766</a>)</li>
<li>[<code>ruff</code>] Add <code>ctypes.LittleEndianStructure</code>
and related types to existing exception (<code>RUF012</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27753">#27753</a>)</li>
<li>[syntax-errors] Detect duplicate keyword arguments (<a
href="https://redirect.github.com/astral-sh/ruff/pull/17804">#17804</a>)</li>
<li>[syntax-errors] Detect parameters declared <code>nonlocal</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27628">#27628</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Offer display-only fixes and mark safe fixes preferred (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27807">#27807</a>)</li>
<li>Support pull diagnostics for notebook cells (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27779">#27779</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Add default indicator to rules table (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27724">#27724</a>)</li>
<li>Fix broken link to Python docs (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27757">#27757</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Fix s390x stacker assembly in release builds (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27776">#27776</a>)</li>
<li>Guarantee minimum stack size when parsing a module, standalone
expression, and suites (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25464">#25464</a>)</li>
<li>Reduce configuration deserialization code size (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27924">#27924</a>)</li>
<li>Check packed AST index bounds (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27849">#27849</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/AbhinavMir"><code>@​AbhinavMir</code></a></li>
<li><a
href="https://github.com/eduardorittner"><code>@​eduardorittner</code></a></li>
<li><a href="https://github.com/royb3"><code>@​royb3</code></a></li>
<li><a
href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/carljm"><code>@​carljm</code></a></li>
<li><a
href="https://github.com/rosstitmarsh"><code>@​rosstitmarsh</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
changelog</a>.</em></p>
<blockquote>
<h2>0.16.4</h2>
<p>Released on 2026-08-20.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>flake8-use-pathlib</code>] Add autofix for
<code>PTH116</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/26460">#26460</a>)</li>
<li>[<code>refurb</code>] Restrict <code>delete-full-slice</code> to
lists (<code>FURB131</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27711">#27711</a>)</li>
<li>[<code>refurb</code>] Skip <code>FURB101</code> and
<code>FURB103</code> when the <code>open</code> argument is a file
descriptor (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27643">#27643</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Fix <code>InvalidInstruction</code> on Windows CPUs that do not
support <code>POPCNT</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27803">#27803</a>)</li>
<li>[<code>pyflakes</code>] Emit semantic syntax errors in string type
definitions as <code>F722</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27835">#27835</a>)</li>
<li>[<code>pylint</code>] Allow <code>os._exit</code> imports in
<code>import-private-name</code> (<code>PLC2701</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27738">#27738</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[syntax-errors] Align mixed t-string/bytes error message with
CPython 3.14 (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27766">#27766</a>)</li>
<li>[<code>ruff</code>] Add <code>ctypes.LittleEndianStructure</code>
and related types to existing exception (<code>RUF012</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27753">#27753</a>)</li>
<li>[syntax-errors] Detect duplicate keyword arguments (<a
href="https://redirect.github.com/astral-sh/ruff/pull/17804">#17804</a>)</li>
<li>[syntax-errors] Detect parameters declared <code>nonlocal</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27628">#27628</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Offer display-only fixes and mark safe fixes preferred (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27807">#27807</a>)</li>
<li>Support pull diagnostics for notebook cells (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27779">#27779</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Add default indicator to rules table (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27724">#27724</a>)</li>
<li>Fix broken link to Python docs (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27757">#27757</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Fix s390x stacker assembly in release builds (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27776">#27776</a>)</li>
<li>Guarantee minimum stack size when parsing a module, standalone
expression, and suites (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25464">#25464</a>)</li>
<li>Reduce configuration deserialization code size (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27924">#27924</a>)</li>
<li>Check packed AST index bounds (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27849">#27849</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/AbhinavMir"><code>@​AbhinavMir</code></a></li>
<li><a
href="https://github.com/eduardorittner"><code>@​eduardorittner</code></a></li>
<li><a href="https://github.com/royb3"><code>@​royb3</code></a></li>
<li><a
href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/carljm"><code>@​carljm</code></a></li>
<li><a
href="https://github.com/rosstitmarsh"><code>@​rosstitmarsh</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a
href="https://github.com/zaniebot"><code>@​zaniebot</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/astral-sh/ruff/commit/11c76bf48fdac06b2f240cba502eda96da4dce77"><code>11c76bf</code></a>
Bump 0.16.4 (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27937">#27937</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/d53c8c58662ca0576ddd502aa1a2979acf03832f"><code>d53c8c5</code></a>
Isolate playground builds from deployment credentials (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27839">#27839</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/cab001e5dec22f55653021f1f7be449e47c7d81e"><code>cab001e</code></a>
Disable uv preview for releases and pre-commit hooks (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27939">#27939</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/f8d575fedc97e75ea62c679d77afb14246afa88e"><code>f8d575f</code></a>
[ty] Clarify writing guidance for human readers (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27912">#27912</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/ca45faebb1750a213df19ed7f686ee5cf9277f93"><code>ca45fae</code></a>
Set <code>--preview</code> and <code>--default-index</code> for the
<code>uv-lock</code> hook (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27935">#27935</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/4827bf7cb449055e46fbfaf4b26e5125883a0569"><code>4827bf7</code></a>
Export <code>UV_DEFAULT_INDEX</code> in <code>release.sh</code> (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27934">#27934</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/d1087a4b9e03d253a88703f34e0869ee4b805456"><code>d1087a4</code></a>
[ty] Handle assignment expressions in string annotations (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27921">#27921</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/680cce48b6d89ab5b1566e4b797bd4847d861815"><code>680cce4</code></a>
[ty] Optimize inherited recursive protocol comparisons (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27922">#27922</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/974d3cbc04520c112843d6b92577844587402e04"><code>974d3cb</code></a>
Upgrade ecosystem-analyzer and mypy_primer to the latest upstream pins
(<a
href="https://redirect.github.com/astral-sh/ruff/issues/27932">#27932</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/b169b402356d0676451f4a7bc6903da2644b31eb"><code>b169b40</code></a>
Install cargo tools locked (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27929">#27929</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/astral-sh/ruff/compare/0.16.3...0.16.4">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's releases</a>.</em></p>
<blockquote>
<h2>0.16.4</h2>
<h2>Release Notes</h2>
<p>Released on 2026-08-20.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>flake8-use-pathlib</code>] Add autofix for <code>PTH116</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/26460">#26460</a>)</li>
<li>[<code>refurb</code>] Restrict <code>delete-full-slice</code> to lists (<code>FURB131</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27711">#27711</a>)</li>
<li>[<code>refurb</code>] Skip <code>FURB101</code> and <code>FURB103</code> when the <code>open</code> argument is a file descriptor (<a href="https://redirect.github.com/astral-sh/ruff/pull/27643">#27643</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Fix <code>InvalidInstruction</code> on Windows CPUs that do not support <code>POPCNT</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/27803">#27803</a>)</li>
<li>[<code>pyflakes</code>] Emit semantic syntax errors in string type definitions as <code>F722</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/27835">#27835</a>)</li>
<li>[<code>pylint</code>] Allow <code>os._exit</code> imports in <code>import-private-name</code> (<code>PLC2701</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27738">#27738</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[syntax-errors] Align mixed t-string/bytes error message with CPython 3.14 (<a href="https://redirect.github.com/astral-sh/ruff/pull/27766">#27766</a>)</li>
<li>[<code>ruff</code>] Add <code>ctypes.LittleEndianStructure</code> and related types to existing exception (<code>RUF012</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27753">#27753</a>)</li>
<li>[syntax-errors] Detect duplicate keyword arguments (<a href="https://redirect.github.com/astral-sh/ruff/pull/17804">#17804</a>)</li>
<li>[syntax-errors] Detect parameters declared <code>nonlocal</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/27628">#27628</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Offer display-only fixes and mark safe fixes preferred (<a href="https://redirect.github.com/astral-sh/ruff/pull/27807">#27807</a>)</li>
<li>Support pull diagnostics for notebook cells (<a href="https://redirect.github.com/astral-sh/ruff/pull/27779">#27779</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Add default indicator to rules table (<a href="https://redirect.github.com/astral-sh/ruff/pull/27724">#27724</a>)</li>
<li>Fix broken link to Python docs (<a href="https://redirect.github.com/astral-sh/ruff/pull/27757">#27757</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Fix s390x stacker assembly in release builds (<a href="https://redirect.github.com/astral-sh/ruff/pull/27776">#27776</a>)</li>
<li>Guarantee minimum stack size when parsing a module, standalone expression, and suites (<a href="https://redirect.github.com/astral-sh/ruff/pull/25464">#25464</a>)</li>
<li>Reduce configuration deserialization code size (<a href="https://redirect.github.com/astral-sh/ruff/pull/27924">#27924</a>)</li>
<li>Check packed AST index bounds (<a href="https://redirect.github.com/astral-sh/ruff/pull/27849">#27849</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/AbhinavMir"><code>@​AbhinavMir</code></a></li>
<li><a href="https://github.com/eduardorittner"><code>@​eduardorittner</code></a></li>
<li><a href="https://github.com/royb3"><code>@​royb3</code></a></li>
<li><a href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/carljm"><code>@​carljm</code></a></li>
<li><a href="https://github.com/rosstitmarsh"><code>@​rosstitmarsh</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
<blockquote>
<h2>0.16.4</h2>
<p>Released on 2026-08-20.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>flake8-use-pathlib</code>] Add autofix for <code>PTH116</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/26460">#26460</a>)</li>
<li>[<code>refurb</code>] Restrict <code>delete-full-slice</code> to lists (<code>FURB131</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27711">#27711</a>)</li>
<li>[<code>refurb</code>] Skip <code>FURB101</code> and <code>FURB103</code> when the <code>open</code> argument is a file descriptor (<a href="https://redirect.github.com/astral-sh/ruff/pull/27643">#27643</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Fix <code>InvalidInstruction</code> on Windows CPUs that do not support <code>POPCNT</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/27803">#27803</a>)</li>
<li>[<code>pyflakes</code>] Emit semantic syntax errors in string type definitions as <code>F722</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/27835">#27835</a>)</li>
<li>[<code>pylint</code>] Allow <code>os._exit</code> imports in <code>import-private-name</code> (<code>PLC2701</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27738">#27738</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[syntax-errors] Align mixed t-string/bytes error message with CPython 3.14 (<a href="https://redirect.github.com/astral-sh/ruff/pull/27766">#27766</a>)</li>
<li>[<code>ruff</code>] Add <code>ctypes.LittleEndianStructure</code> and related types to existing exception (<code>RUF012</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27753">#27753</a>)</li>
<li>[syntax-errors] Detect duplicate keyword arguments (<a href="https://redirect.github.com/astral-sh/ruff/pull/17804">#17804</a>)</li>
<li>[syntax-errors] Detect parameters declared <code>nonlocal</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/27628">#27628</a>)</li>
</ul>
<h3>Server</h3>
<ul>
<li>Offer display-only fixes and mark safe fixes preferred (<a href="https://redirect.github.com/astral-sh/ruff/pull/27807">#27807</a>)</li>
<li>Support pull diagnostics for notebook cells (<a href="https://redirect.github.com/astral-sh/ruff/pull/27779">#27779</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Add default indicator to rules table (<a href="https://redirect.github.com/astral-sh/ruff/pull/27724">#27724</a>)</li>
<li>Fix broken link to Python docs (<a href="https://redirect.github.com/astral-sh/ruff/pull/27757">#27757</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Fix s390x stacker assembly in release builds (<a href="https://redirect.github.com/astral-sh/ruff/pull/27776">#27776</a>)</li>
<li>Guarantee minimum stack size when parsing a module, standalone expression, and suites (<a href="https://redirect.github.com/astral-sh/ruff/pull/25464">#25464</a>)</li>
<li>Reduce configuration deserialization code size (<a href="https://redirect.github.com/astral-sh/ruff/pull/27924">#27924</a>)</li>
<li>Check packed AST index bounds (<a href="https://redirect.github.com/astral-sh/ruff/pull/27849">#27849</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/AbhinavMir"><code>@​AbhinavMir</code></a></li>
<li><a href="https://github.com/eduardorittner"><code>@​eduardorittner</code></a></li>
<li><a href="https://github.com/royb3"><code>@​royb3</code></a></li>
<li><a href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li>
<li><a href="https://github.com/carljm"><code>@​carljm</code></a></li>
<li><a href="https://github.com/rosstitmarsh"><code>@​rosstitmarsh</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a href="https://github.com/zaniebot"><code>@​zaniebot</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/astral-sh/ruff/commit/11c76bf48fdac06b2f240cba502eda96da4dce77"><code>11c76bf</code></a> Bump 0.16.4 (<a href="https://redirect.github.com/astral-sh/ruff/issues/27937">#27937</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/d53c8c58662ca0576ddd502aa1a2979acf03832f"><code>d53c8c5</code></a> Isolate playground builds from deployment credentials (<a href="https://redirect.github.com/astral-sh/ruff/issues/27839">#27839</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/cab001e5dec22f55653021f1f7be449e47c7d81e"><code>cab001e</code></a> Disable uv preview for releases and pre-commit hooks (<a href="https://redirect.github.com/astral-sh/ruff/issues/27939">#27939</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/f8d575fedc97e75ea62c679d77afb14246afa88e"><code>f8d575f</code></a> [ty] Clarify writing guidance for human readers (<a href="https://redirect.github.com/astral-sh/ruff/issues/27912">#27912</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/ca45faebb1750a213df19ed7f686ee5cf9277f93"><code>ca45fae</code></a> Set <code>--preview</code> and <code>--default-index</code> for the <code>uv-lock</code> hook (<a href="https://redirect.github.com/astral-sh/ruff/issues/27935">#27935</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/4827bf7cb449055e46fbfaf4b26e5125883a0569"><code>4827bf7</code></a> Export <code>UV_DEFAULT_INDEX</code> in <code>release.sh</code> (<a href="https://redirect.github.com/astral-sh/ruff/issues/27934">#27934</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/d1087a4b9e03d253a88703f34e0869ee4b805456"><code>d1087a4</code></a> [ty] Handle assignment expressions in string annotations (<a href="https://redirect.github.com/astral-sh/ruff/issues/27921">#27921</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/680cce48b6d89ab5b1566e4b797bd4847d861815"><code>680cce4</code></a> [ty] Optimize inherited recursive protocol comparisons (<a href="https://redirect.github.com/astral-sh/ruff/issues/27922">#27922</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/974d3cbc04520c112843d6b92577844587402e04"><code>974d3cb</code></a> Upgrade ecosystem-analyzer and mypy_primer to the latest upstream pins (<a href="https://redirect.github.com/astral-sh/ruff/issues/27932">#27932</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/b169b402356d0676451f4a7bc6903da2644b31eb"><code>b169b40</code></a> Install cargo tools locked (<a href="https://redirect.github.com/astral-sh/ruff/issues/27929">#27929</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.16.3...0.16.4">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## build(deps): update openai requirement from <3.1.0,>=3.0.0 to >=3.3.1,<3.4.0 in /services/claw-interface (#3582)

- **SHA**: `c978e5a3f33096fc48b850a09e3e65605c192ee6`
- **作者**: dependabot[bot]
- **日期**: 2026-08-29T02:44:29Z
- **PR**: #3582

### Commit Message

```
build(deps): update openai requirement from <3.1.0,>=3.0.0 to >=3.3.1,<3.4.0 in /services/claw-interface (#3582)

Updates the requirements on
[openai](https://github.com/openai/openai-python) to permit the latest
version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/releases">openai's
releases</a>.</em></p>
<blockquote>
<h2>v3.3.1</h2>
<h2><a
href="https://github.com/openai/openai-python/compare/v3.3.0...v3.3.1">3.3.1</a>
(2026-08-19)</h2>
<h3>Bug Fixes</h3>
<ul>
<li><strong>deps:</strong> update dependencies with published security
fixes (<a
href="https://redirect.github.com/openai/openai-python/issues/3680">#3680</a>)
(<a
href="https://github.com/openai/openai-python/commit/53aa4fc68b65f42456cafaaa5ff4b0d317184752">53aa4fc</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>build:</strong> migrate to uv (<a
href="https://redirect.github.com/openai/openai-python/issues/3653">#3653</a>)
(<a
href="https://github.com/openai/openai-python/commit/b37e85d8fe9cd2b23862dbc62716d38e2cacaf92">b37e85d</a>)</li>
<li><strong>deps:</strong> remove jsonschema and unused
fixture-validation dependencies (<a
href="https://github.com/openai/openai-python/commit/0dfdfdddfbeb591a1bb5b3b4aa62e4a9870fcaa6">0dfdfdd</a>)</li>
<li>lock the repository Pyright toolchain (<a
href="https://redirect.github.com/openai/openai-python/issues/3678">#3678</a>)
(<a
href="https://github.com/openai/openai-python/commit/3079be224c05479b6cf8aa329480c249f66f0599">3079be2</a>)</li>
<li>run the mock server from locked local tooling (<a
href="https://redirect.github.com/openai/openai-python/issues/3679">#3679</a>)
(<a
href="https://github.com/openai/openai-python/commit/370fcc60ce9006db5a75dcd0333790dfe71a907c">370fcc6</a>)</li>
</ul>
<h3>Refactors</h3>
<ul>
<li><strong>deps:</strong> use the standard library for platform
detection (<a
href="https://github.com/openai/openai-python/commit/d5b00659d6659c5def665cb04e6563bdf683ea03">d5b0065</a>)</li>
</ul>
<h3>Build System</h3>
<ul>
<li>replace the external README metadata hook (<a
href="https://github.com/openai/openai-python/commit/e673ca8ff9e5c2292615976e99bf5731d47327e8">e673ca8</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's
changelog</a>.</em></p>
<blockquote>
<h2><a
href="https://github.com/openai/openai-python/compare/v3.3.0...v3.3.1">3.3.1</a>
(2026-08-19)</h2>
<h3>Bug Fixes</h3>
<ul>
<li><strong>deps:</strong> update dependencies with published security
fixes (<a
href="https://redirect.github.com/openai/openai-python/issues/3680">#3680</a>)
(<a
href="https://github.com/openai/openai-python/commit/53aa4fc68b65f42456cafaaa5ff4b0d317184752">53aa4fc</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>build:</strong> migrate to uv (<a
href="https://redirect.github.com/openai/openai-python/issues/3653">#3653</a>)
(<a
href="https://github.com/openai/openai-python/commit/b37e85d8fe9cd2b23862dbc62716d38e2cacaf92">b37e85d</a>)</li>
<li><strong>deps:</strong> remove jsonschema and unused
fixture-validation dependencies (<a
href="https://github.com/openai/openai-python/commit/0dfdfdddfbeb591a1bb5b3b4aa62e4a9870fcaa6">0dfdfdd</a>)</li>
<li>lock the repository Pyright toolchain (<a
href="https://redirect.github.com/openai/openai-python/issues/3678">#3678</a>)
(<a
href="https://github.com/openai/openai-python/commit/3079be224c05479b6cf8aa329480c249f66f0599">3079be2</a>)</li>
<li>run the mock server from locked local tooling (<a
href="https://redirect.github.com/openai/openai-python/issues/3679">#3679</a>)
(<a
href="https://github.com/openai/openai-python/commit/370fcc60ce9006db5a75dcd0333790dfe71a907c">370fcc6</a>)</li>
</ul>
<h3>Refactors</h3>
<ul>
<li><strong>deps:</strong> use the standard library for platform
detection (<a
href="https://github.com/openai/openai-python/commit/d5b00659d6659c5def665cb04e6563bdf683ea03">d5b0065</a>)</li>
</ul>
<h3>Build System</h3>
<ul>
<li>replace the external README metadata hook (<a
href="https://github.com/openai/openai-python/commit/e673ca8ff9e5c2292615976e99bf5731d47327e8">e673ca8</a>)</li>
</ul>
<h2><a
href="https://github.com/openai/openai-python/compare/v3.2.0...v3.3.0">3.3.0</a>
(2026-08-18)</h2>
<h3>Features</h3>
<ul>
<li>support named data-residency endpoints (<a
href="https://redirect.github.com/openai/openai-python/issues/3646">#3646</a>)
(<a
href="https://github.com/openai/openai-python/commit/11ee91475694d9cd77813763707fbadf68806d4f">11ee914</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li>require patched optional networking dependencies (<a
href="https://redirect.github.com/openai/openai-python/issues/3651">#3651</a>)
(<a
href="https://github.com/openai/openai-python/commit/40e56de55166a55be3572fdf9750145d4458e144">40e56de</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li>remove unused dependencies and pin build tooling (<a
href="https://redirect.github.com/openai/openai-python/issues/3650">#3650</a>)
(<a
href="https://github.com/openai/openai-python/commit/eee8e4a7d0e42bb0d6b9aa01c4dd8e04aaac3ff4">eee8e4a</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>strengthen Python SDK security contribution guidance (<a
href="https://redirect.github.com/openai/openai-python/issues/3639">#3639</a>)
(<a
href="https://github.com/openai/openai-python/commit/6577709190ae5e258d0270870f701432f67e6a3e">6577709</a>)</li>
</ul>
<h2><a
href="https://github.com/openai/openai-python/compare/v3.1.0...v3.2.0">3.2.0</a>
(2026-08-17)</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/openai/openai-python/commit/753ab5c1a81cd85e8bf0aef4c04c51a2e8dae6cd"><code>753ab5c</code></a>
release: 3.3.1 (<a
href="https://redirect.github.com/openai/openai-python/issues/3658">#3658</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/53aa4fc68b65f42456cafaaa5ff4b0d317184752"><code>53aa4fc</code></a>
fix(deps): update dependencies with published security fixes (<a
href="https://redirect.github.com/openai/openai-python/issues/3680">#3680</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/370fcc60ce9006db5a75dcd0333790dfe71a907c"><code>370fcc6</code></a>
chore: run the mock server from locked local tooling (<a
href="https://redirect.github.com/openai/openai-python/issues/3679">#3679</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/3079be224c05479b6cf8aa329480c249f66f0599"><code>3079be2</code></a>
chore: lock the repository Pyright toolchain (<a
href="https://redirect.github.com/openai/openai-python/issues/3678">#3678</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/b802648bc95fdc761e5447bd5c9d0673a669cbbb"><code>b802648</code></a>
update vulnerable dependencies (<a
href="https://redirect.github.com/openai/openai-python/issues/3676">#3676</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/8995963f9563e4949c495d2d19853c3bf126dee6"><code>8995963</code></a>
add script dependency cooldown (<a
href="https://redirect.github.com/openai/openai-python/issues/3675">#3675</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/8174e247db4e6698395da5e07543c304a8c8f294"><code>8174e24</code></a>
disable checkout credential persistence (<a
href="https://redirect.github.com/openai/openai-python/issues/3674">#3674</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/d5b00659d6659c5def665cb04e6563bdf683ea03"><code>d5b0065</code></a>
[3/n] Use the standard library for platform headers (<a
href="https://redirect.github.com/openai/openai-python/issues/3656">#3656</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/e673ca8ff9e5c2292615976e99bf5731d47327e8"><code>e673ca8</code></a>
[2/n] Keep the package README hook in the repository (<a
href="https://redirect.github.com/openai/openai-python/issues/3655">#3655</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/0dfdfdddfbeb591a1bb5b3b4aa62e4a9870fcaa6"><code>0dfdfdd</code></a>
[1/n] Reduce the Bedrock fixture validation dependencies (<a
href="https://redirect.github.com/openai/openai-python/issues/3654">#3654</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/openai/openai-python/compare/v3.0.0...v3.3.1">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [openai](https://github.com/openai/openai-python) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/releases">openai's releases</a>.</em></p>
<blockquote>
<h2>v3.3.1</h2>
<h2><a href="https://github.com/openai/openai-python/compare/v3.3.0...v3.3.1">3.3.1</a> (2026-08-19)</h2>
<h3>Bug Fixes</h3>
<ul>
<li><strong>deps:</strong> update dependencies with published security fixes (<a href="https://redirect.github.com/openai/openai-python/issues/3680">#3680</a>) (<a href="https://github.com/openai/openai-python/commit/53aa4fc68b65f42456cafaaa5ff4b0d317184752">53aa4fc</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>build:</strong> migrate to uv (<a href="https://redirect.github.com/openai/openai-python/issues/3653">#3653</a>) (<a href="https://github.com/openai/openai-python/commit/b37e85d8fe9cd2b23862dbc62716d38e2cacaf92">b37e85d</a>)</li>
<li><strong>deps:</strong> remove jsonschema and unused fixture-validation dependencies (<a href="https://github.com/openai/openai-python/commit/0dfdfdddfbeb591a1bb5b3b4aa62e4a9870fcaa6">0dfdfdd</a>)</li>
<li>lock the repository Pyright toolchain (<a href="https://redirect.github.com/openai/openai-python/issues/3678">#3678</a>) (<a href="https://github.com/openai/openai-python/commit/3079be224c05479b6cf8aa329480c249f66f0599">3079be2</a>)</li>
<li>run the mock server from locked local tooling (<a href="https://redirect.github.com/openai/openai-python/issues/3679">#3679</a>) (<a href="https://github.com/openai/openai-python/commit/370fcc60ce9006db5a75dcd0333790dfe71a907c">370fcc6</a>)</li>
</ul>
<h3>Refactors</h3>
<ul>
<li><strong>deps:</strong> use the standard library for platform detection (<a href="https://github.com/openai/openai-python/commit/d5b00659d6659c5def665cb04e6563bdf683ea03">d5b0065</a>)</li>
</ul>
<h3>Build System</h3>
<ul>
<li>replace the external README metadata hook (<a href="https://github.com/openai/openai-python/commit/e673ca8ff9e5c2292615976e99bf5731d47327e8">e673ca8</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's changelog</a>.</em></p>
<blockquote>
<h2><a href="https://github.com/openai/openai-python/compare/v3.3.0...v3.3.1">3.3.1</a> (2026-08-19)</h2>
<h3>Bug Fixes</h3>
<ul>
<li><strong>deps:</strong> update dependencies with published security fixes (<a href="https://redirect.github.com/openai/openai-python/issues/3680">#3680</a>) (<a href="https://github.com/openai/openai-python/commit/53aa4fc68b65f42456cafaaa5ff4b0d317184752">53aa4fc</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>build:</strong> migrate to uv (<a href="https://redirect.github.com/openai/openai-python/issues/3653">#3653</a>) (<a href="https://github.com/openai/openai-python/commit/b37e85d8fe9cd2b23862dbc62716d38e2cacaf92">b37e85d</a>)</li>
<li><strong>deps:</strong> remove jsonschema and unused fixture-validation dependencies (<a href="https://github.com/openai/openai-python/commit/0dfdfdddfbeb591a1bb5b3b4aa62e4a9870fcaa6">0dfdfdd</a>)</li>
<li>lock the repository Pyright toolchain (<a href="https://redirect.github.com/openai/openai-python/issues/3678">#3678</a>) (<a href="https://github.com/openai/openai-python/commit/3079be224c05479b6cf8aa329480c249f66f0599">3079be2</a>)</li>
<li>run the mock server from locked local tooling (<a href="https://redirect.github.com/openai/openai-python/issues/3679">#3679</a>) (<a href="https://github.com/openai/openai-python/commit/370fcc60ce9006db5a75dcd0333790dfe71a907c">370fcc6</a>)</li>
</ul>
<h3>Refactors</h3>
<ul>
<li><strong>deps:</strong> use the standard library for platform detection (<a href="https://github.com/openai/openai-python/commit/d5b00659d6659c5def665cb04e6563bdf683ea03">d5b0065</a>)</li>
</ul>
<h3>Build System</h3>
<ul>
<li>replace the external README metadata hook (<a href="https://github.com/openai/openai-python/commit/e673ca8ff9e5c2292615976e99bf5731d47327e8">e673ca8</a>)</li>
</ul>
<h2><a href="https://github.com/openai/openai-python/compare/v3.2.0...v3.3.0">3.3.0</a> (2026-08-18)</h2>
<h3>Features</h3>
<ul>
<li>support named data-residency endpoints (<a href="https://redirect.github.com/openai/openai-python/issues/3646">#3646</a>) (<a href="https://github.com/openai/openai-python/commit/11ee91475694d9cd77813763707fbadf68806d4f">11ee914</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li>require patched optional networking dependencies (<a href="https://redirect.github.com/openai/openai-python/issues/3651">#3651</a>) (<a href="https://github.com/openai/openai-python/commit/40e56de55166a55be3572fdf9750145d4458e144">40e56de</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li>remove unused dependencies and pin build tooling (<a href="https://redirect.github.com/openai/openai-python/issues/3650">#3650</a>) (<a href="https://github.com/openai/openai-python/commit/eee8e4a7d0e42bb0d6b9aa01c4dd8e04aaac3ff4">eee8e4a</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>strengthen Python SDK security contribution guidance (<a href="https://redirect.github.com/openai/openai-python/issues/3639">#3639</a>) (<a href="https://github.com/openai/openai-python/commit/6577709190ae5e258d0270870f701432f67e6a3e">6577709</a>)</li>
</ul>
<h2><a href="https://github.com/openai/openai-python/compare/v3.1.0...v3.2.0">3.2.0</a> (2026-08-17)</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/openai/openai-python/commit/753ab5c1a81cd85e8bf0aef4c04c51a2e8dae6cd"><code>753ab5c</code></a> release: 3.3.1 (<a href="https://redirect.github.com/openai/openai-python/issues/3658">#3658</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/53aa4fc68b65f42456cafaaa5ff4b0d317184752"><code>53aa4fc</code></a> fix(deps): update dependencies with published security fixes (<a href="https://redirect.github.com/openai/openai-python/issues/3680">#3680</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/370fcc60ce9006db5a75dcd0333790dfe71a907c"><code>370fcc6</code></a> chore: run the mock server from locked local tooling (<a href="https://redirect.github.com/openai/openai-python/issues/3679">#3679</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/3079be224c05479b6cf8aa329480c249f66f0599"><code>3079be2</code></a> chore: lock the repository Pyright toolchain (<a href="https://redirect.github.com/openai/openai-python/issues/3678">#3678</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/b802648bc95fdc761e5447bd5c9d0673a669cbbb"><code>b802648</code></a> update vulnerable dependencies (<a href="https://redirect.github.com/openai/openai-python/issues/3676">#3676</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/8995963f9563e4949c495d2d19853c3bf126dee6"><code>8995963</code></a> add script dependency cooldown (<a href="https://redirect.github.com/openai/openai-python/issues/3675">#3675</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/8174e247db4e6698395da5e07543c304a8c8f294"><code>8174e24</code></a> disable checkout credential persistence (<a href="https://redirect.github.com/openai/openai-python/issues/3674">#3674</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/d5b00659d6659c5def665cb04e6563bdf683ea03"><code>d5b0065</code></a> [3/n] Use the standard library for platform headers (<a href="https://redirect.github.com/openai/openai-python/issues/3656">#3656</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/e673ca8ff9e5c2292615976e99bf5731d47327e8"><code>e673ca8</code></a> [2/n] Keep the package README hook in the repository (<a href="https://redirect.github.com/openai/openai-python/issues/3655">#3655</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/0dfdfdddfbeb591a1bb5b3b4aa62e4a9870fcaa6"><code>0dfdfdd</code></a> [1/n] Reduce the Bedrock fixture validation dependencies (<a href="https://redirect.github.com/openai/openai-python/issues/3654">#3654</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/openai/openai-python/compare/v3.0.0...v3.3.1">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---
