# ecap-skills Commits — 2026-05-06

## dee99ccd — 2026-05-06
**Author:** allenz-srp
**SHA:** dee99ccd2671494e9168bc9365f1a78d74a45396
**Stats:** +94 -164 (258 changes)

### Commit Message
```
chore(devcontainer): trust image-baked handoff stack, simplify install/start logic (#191)

openclaw-docker v2026.4.2.25+ bakes the @zooclaw/handoff layer (chromium +
VNC + nginx + plugin + helper scripts) into the image (Dockerfile §5.9 +
handoff/* files, gated by INSTALL_HANDOFF=true build-arg). Tuned in .28
to ~290MB lower idle RSS. Devcontainer was duplicating most of this in
its postCreate/postStart/setup-extras scripts; that's now redundant.

This refactor keeps the script architecture (3-section setup-extras,
4-step postCreate, postStart's "VNC backend → gateway" flow) but
delegates the heavy lifting to the image where possible, with fallbacks
for INSTALL_HANDOFF=false or pre-.25 images.

Changes (4 files, +94 / −164 lines net −70):

- openclaw.json.tmpl: add `zooclaw-handoff: enabled: true` so the image's
  start-handoff-stack jq gate passes (image .25+ self-gates the VNC
  backend startup on this flag).

- setup-extras.sh: each section becomes "verify image has it; fallback
  install if not". apt step skipped when image-baked. nginx config drop
  skipped when image already supplies /etc/nginx/conf.d/handoff.conf.
  @zooclaw/handoff install skipped when bundled at /usr/local/lib/.../
  dist/extensions/zooclaw-handoff. Section structure + comments
  preserved.

- postCreateCommand.sh: chromium-fit install becomes conditional —
  only copies our committed copy if image lacks /usr/local/bin/chromium-fit.

- postStartCommand.sh: ~90 lines of inline VNC backend startup (Xvfb +
  chromium + x11vnc + websockify + chromium-fit) replaced with a single
  call to /usr/local/bin/start-handoff-stack. The helper is idempotent,
  version-aligned with the prod bot pod, includes the .28 chromium
  memory tuning + 1080p Xvfb, and starts nginx ingress too — so the
  devcontainer now has full runtime parity with the prod image.

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description
## Summary

openclaw-docker .25+ bakes the entire `@zooclaw/handoff` layer (chromium + VNC + nginx + plugin + helper scripts) into the image (Dockerfile §5.9 + `handoff/` files, gated by `INSTALL_HANDOFF=true` build-arg). The .28 tag added chromium memory tuning that drops idle RSS by ~290 MB.

The devcontainer was duplicating most of this — apt-installing the same packages, copying the same nginx config, npm-installing the same plugin, and inlining ~90 lines of VNC backend startup. All redundant now.

This refactor delegates to the image, keeps fallbacks for `INSTALL_HANDOFF=false` or pre-.25 images, and preserves the script architecture (3-section setup-extras, 4-step postCreate, postStart's "VNC → gateway" flow).

## Changes

| File | What |
|---|---|
| `.devcontainer/openclaw.json.tmpl` | + `"zooclaw-handoff": { "enabled": true }` so image's `start-handoff-stack` jq gate passes |
| `.devcontainer/setup-extras.sh` | each section becomes "verify image has it; fallback install if not". apt step skipped when image-baked, nginx config drop skipped when `/etc/nginx/conf.d/handoff.conf` already exists, plugin install skipped when bundled at `/usr/local/lib/.../dist/extensions/zooclaw-handoff` |
| `.devcontainer/postCreateCommand.sh` | chromium-fit install becomes conditional — only copies committed file if image lacks `/usr/local/bin/chromium-fit` |
| `.devcontainer/postStartCommand.sh` | **~90 lines** of inline VNC backend startup (Xvfb + chromium + x11vnc + websockify + chromium-fit) replaced with single call to `/usr/local/bin/start-handoff-stack`. Helper is idempotent, includes the .28 chromium memory tuning + 1080p Xvfb, starts nginx too — full runtime parity with prod bot pod |

Net diff: **+94 / −164 lines (−70)**.

## Why keep the fallbacks

- pre-.25 images (none in active use, but defensively cheap)
- `--build-arg INSTALL_HANDOFF=false` builds (size kill switch — devcontainer can still bring up handoff locally)

`.devcontainer/chromium-fit.sh` and `.devcontainer/nginx-handoff.conf` files are kept as-is for the same reason.

## Test plan

- [x] `bash -n` passes on all three modified scripts
- [ ] Rebuild devcontainer (`docker compose down + Reopen in Container`) on macOS:
  - postCreate: env check + setup-extras logs `vnc deps: ... present (image-baked)` + `nginx: ... ` + `handoff: @zooclaw/handoff@... bundled in image`
  - postStart: logs `vnc: handed to /usr/local/bin/start-handoff-stack`, gateway comes up, `/healthz` passes
  - Inside container: `pgrep -af "Xvfb :99|chromium|x11vnc|websockify|nginx"` shows full stack running, `:18789` (nginx) and `:18790` (gateway) listening
- [ ] Trigger handoff from webchat — confirm `/handoff/page` opens, noVNC connects, `/handoff/complete` works

## Notes

- For existing devcontainers with a stale `.devcontainer/openclaw.json` from a previous render: set `OPENCLAW_FORCE_RERENDER=1` in `.devcontainer/.env` to pick up the new `zooclaw-handoff` entry, OR delete `.devcontainer/openclaw.json` and rebuild.
- Both `chromium-fit.sh` and `nginx-handoff.conf` files in `.devcontainer/` may eventually drift from the image's copies; can be deleted in a follow-up if the divergence becomes a problem.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## a58f5383 — 2026-05-06
**Author:** nolan-srp
**SHA:** a58f53835171f78a76a57f5e8b62675d049eaffe
**Stats:** +763 -215 (978 changes)

### Commit Message
```
docs(browser-skill): move runtime state to workspace (#190)
```

### PR Description
## Summary
- move browser-skill runtime state storage to /tmp/openclaw/browser-skill/.state.json
- document that the installed skill directory is read-only at runtime
- require user-facing progress messages before key browser steps, including manual handoff flows

---

## 6e442cf4 — 2026-05-06
**Author:** allenz-srp
**SHA:** 6e442cf4fae90805a63311caf130909d738d3df4
**Stats:** +145 -17 (162 changes)

### Commit Message
```
chore(devcontainer): single-port nginx ingress + pin @zooclaw/handoff@20260402.0.2 (#189)

* chore(devcontainer): align with @zooclaw/handoff README + macOS rebuild fixes

Closes the gap between our devcontainer setup and the requirements documented
in @zooclaw/handoff's README (xrandr, xdotool, chromium-fit, --test-type,
persistent profile path), and fixes a handful of macOS Docker Desktop quirks
that were turning a fresh `Rebuild Container` into an unreliable experience.

Changes:

- setup-extras.sh
  - add `x11-xserver-utils` (xrandr) and `xdotool` to the apt list — required
    by /handoff/resize and chromium-fit per the handoff README
  - drop apt's `-q` flag and add explicit `>>` progress prints, so a fresh
    rebuild surfaces "installing chromium ~200MB, expect 3–5 min" in the dev
    containers panel instead of looking frozen for the duration

- chromium-fit.sh (new)
  - committed source for the window-fit daemon from the handoff README:
    polls `xdotool getdisplaygeometry` and snaps every chromium window to
    match. Without it /handoff/resize resizes the noVNC canvas but chromium
    stays at its launched size, so the user sees only the top-left of the
    page (looks like "scroll/clicks don't work")
  - postCreate installs it to /usr/local/bin/chromium-fit alongside
    restart-gateway

- postCreateCommand.sh
  - retry-then-`sudo cat` instead of plain `cp` for /tmp/openclaw.json: the
    host file is mode 600 (carries an apiKey) and macOS Docker's virtiofs
    has a cold-sync race that returns EACCES even for root for a few seconds
    after container start. Probe the file is fully readable before copying,
    and write via `sudo cat $src > $dst` to dodge cp's sendfile fast-path
    which still trips up at that point
  - install chromium-fit binary alongside restart-gateway

- postStartCommand.sh
  - chromium launch: add `--test-type` (kills the yellow "unsupported flag
    --no-sandbox" infobar that ate clicks) and `--start-maximized
    --window-size=1920,1080` (matches handoff README reference)
  - move chromium profile from /tmp/chromium-profile (wiped on every
    container restart, losing every login) to ~/.openclaw/chromium-profile
    (named volume, persists across rebuilds) — the handoff README's
    "--user-data-dir=<persistent path>" requirement
  - clear stale SingletonLock/Cookie/Socket symlinks before chromium starts:
    when a container is torn down, chromium gets force-killed without a
    chance to clean these up; on next start chromium sees them and refuses
    to launch with "profile in use by another Chromium process"
  - start chromium-fit daemon after websockify, with binary/xdotool guards

End-to-end verified after `docker compose down` + clean Reopen in Container:
postCreate runs cleanly, apt progress is visible in the dev containers
panel, postStart brings up Xvfb + chromium + x11vnc + websockify +
chromium-fit + gateway, /handoff/resize works, and chromium login state
survives container restarts.

* chore(devcontainer): single-port nginx ingress + pin @zooclaw/handoff@20260402.0.2

@zooclaw/handoff@20260402.0.2 dropped the two-port shape and now emits a
same-origin wss://<host>/handoff/vnc?... wsUrl regardless of how the
gateway is reachable. Operators are expected to put an ingress in front
that path-routes /handoff/vnc to the in-pod VNC proxy on :6081. This
adapts the devcontainer to that contract.

Changes:

- nginx-handoff.conf (new)
  ingress config: listen on :18789, exact-match /handoff/vnc → :6081
  (plugin proxy), everything else → :18790 (gateway). 4h timeouts to
  match handoff-session.ts MAX_TIMEOUT_MS so a real session does not get
  cut by nginx.

- docker-compose.yml
  drop the second published port (6081). Gateway moves to internal :18790
  via OPENCLAW_GATEWAY_PORT; nginx owns :18789 as the only externally
  visible port. Matches the pod-internal-only shape the handoff README
  documents under "Deployment".

- setup-extras.sh
  apt-install nginx-light alongside the VNC stack; install/start the
  ingress config (idempotent — reloads on rebuild). Pin @zooclaw/handoff
  to 20260402.0.2 and add a version-aware install: skip if the installed
  package.json matches HANDOFF_VERSION, otherwise warn-and-upgrade. Also
  fix a `set -e` trap on `INSTALLED_VERSION=$(jq ... 2>/dev/null)` — jq
  exits non-zero when the package.json is missing on a fresh install,
  which silently aborted setup-extras before reaching the install block.
  `|| true` keeps the assignment defensible.

- README.md
  update "What you get": VNC backend is no longer "exposed on
  localhost:6081"; nginx routes /handoff/vnc to the in-container proxy.

Future: when openclaw exposes a registerHttpUpgrade SDK hook, the plugin's
proxy listener can be dropped and this nginx layer goes with it. The
external wss://host/handoff/vnc?... contract is already the same-origin
shape the handoff client emits, so no further client changes will be
needed.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description
## Summary

Builds on #188 (already merged). Adapts the devcontainer to `@zooclaw/handoff@20260402.0.2` (zooclaw-extras#26), which dropped the two-port shape and now always emits a same-origin `wss://<host>/handoff/vnc?…` regardless of how the gateway is reachable. Operators are expected to put an ingress in front of the gateway that path-routes `/handoff/vnc` to the in-pod VNC proxy on `:6081`.

```
external 18789 ──nginx──┬─ Path(/handoff/vnc)  ──► pod:6081  (plugin proxy → websockify → x11vnc)
                        └─ everything else     ──► pod:18790 (openclaw gateway)
```

## Changes

- **`nginx-handoff.conf`** (new) — listen on `:18789`, exact-match `/handoff/vnc` → `:6081`, everything else → `:18790`. 4h timeouts to match `handoff-session.ts` `MAX_TIMEOUT_MS` so a real session doesn't get cut by nginx.

- **`docker-compose.yml`** — drop the second published port (`6081`). Gateway moves to internal `:18790` via `OPENCLAW_GATEWAY_PORT`; nginx owns `:18789` as the only externally visible port.

- **`setup-extras.sh`**
  - apt-install `nginx-light` alongside the VNC stack
  - install/start the ingress config (idempotent — reloads on rebuild)
  - pin `@zooclaw/handoff` to `20260402.0.2`
  - version-aware install: skip if installed `package.json` matches `HANDOFF_VERSION`, otherwise warn-and-upgrade — future bumps need a single `HANDOFF_VERSION=…` change, no manual `rm -rf`
  - fix `set -e` trap on `INSTALLED_VERSION=$(jq … 2>/dev/null)`: `jq` exits non-zero when `package.json` is missing on a fresh install, which silently aborted setup-extras before reaching the install block. `|| true` keeps the assignment defensible.

- **`README.md`** — VNC backend description: no longer "exposed on `localhost:6081`"; nginx routes `/handoff/vnc` to the in-container proxy.

## Test plan

- [x] `docker compose down` + clean Reopen in Container on macOS → postCreate runs cleanly with apt progress visible in dev containers panel
- [x] postStart brings up Xvfb + chromium + x11vnc + websockify + chromium-fit + gateway in order; `/healthz` responds within 60s
- [x] `nginx -t` validates `handoff.conf`; nginx listens on `:18789`; gateway on internal `:18790`; plugin VNC proxy on `:6081`
- [x] `openclaw config validate` → `Config valid`; `[zooclaw-handoff] vnc proxy listening on :6081 → 127.0.0.1:6080`
- [x] Version-aware install path: deleting `~/.openclaw/extensions/zooclaw-handoff` then re-running setup-extras.sh installs `20260402.0.2` from npm cleanly

## Notes

- `:6081` is no longer published externally — devs hitting old `localhost:6081/...` URLs will get connection refused. Same-origin `localhost:18789/handoff/vnc?…` is the only shape now (matches what the plugin emits).
- On `docker restart` (vs full rebuild), nginx won't auto-resume because `setup-extras.sh` only runs in postCreate. Documented inline; rebuild or call the script manually if needed.
- Future: when openclaw exposes a `registerHttpUpgrade` SDK hook, the plugin's `:6081` listener and this nginx layer can both go away. The external `wss://host/handoff/vnc?…` contract stays the same, so no further client changes will be needed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
