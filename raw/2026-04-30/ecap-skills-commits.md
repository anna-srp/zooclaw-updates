# ecap-skills Commits - 2026-04-30

## Commit: 81b21926
- **Author**: allenz-srp
- **Date**: 2026-04-29T05:46:14Z
- **PR**: #183

### Full Commit Message
```
chore(devcontainer): run real openclaw gateway with staging-parity config init (#183)

* chore(devcontainer): run real openclaw gateway with staging-parity config init

Turns the devcontainer into a real, runnable openclaw gateway instead of
a passive shell, mirroring how a bot pod is configured in staging.

- openclaw.json.tmpl: full fastclaw helm defaultConfigs["2026.4.2"] merged
  with the zooclaw _bot_lifecycle.py:create_bot db patch (5 LiteLLM models,
  all plugins, diagnostics-otel, zooguardian, tool denylist, gateway hot
  reload, etc. — no simplification, drift-trackable against gcp-foundation)
- postCreateCommand.sh: envsubst-render template → ~/.openclaw/openclaw.json
  → openclaw config validate (with doctor --fix fallback per start-gateway.sh)
  → background `openclaw gateway --port 18789 --bind lan --allow-unconfigured
  --dev`. GATEWAY_TOKEN auto-generated and persisted to ~/.openclaw/.gateway-token
- docker-compose.yml: port 8000→18789; pass through all 31 env vars from
  the 3 staging layers (helm pod_default + zooclaw per-bot + bot identity);
  *_BASE_URL defaults derived from $LITELLM_API_BASE, *_API_KEY defaults
  derived from $LITELLM_API_KEY to minimize required dev fields
- .env.example: documents all 3 layers with staging public URLs as
  reference defaults; secrets/keys left blank

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(devcontainer): pull bot env from fastclaw admin API instead of hand-listing

Previous .env.example forced the dev to hand-fill 30+ vars mirroring
staging vault-openclaw-env-secret + zooclaw bot-create injection.
Replaces all of that with a 2-var config (BOT_ID + FASTCLAW_ADMIN_TOKEN)
that postCreate hits to fetch the bot's deployment.env at boot.

- postCreateCommand.sh: curl GET /bot/api/v1/admin/bots/$BOT_ID with the
  fastclaw admin token (bypasses per-app ownership check, single shared
  token instead of per-user app tokens), jq @sh-encode each
  bot.config.deployment.env entry into ~/.openclaw/env.sh, source it +
  patch it into ~/.bashrc + ~/.zshrc so all later VSCode terminals see
  the same vars (USER_INTERNAL_TOKEN / AGENT_IDENTITY_* / LITELLM_API_KEY
  / NANGO_GATEWAY_URL / etc). LITELLM_API_BASE in .env still wins because
  the pod's value is cluster-internal and unreachable from a dev machine.
- docker-compose.yml: shrink env block from 31 vars to 8; default
  FASTCLAW_BASE_URL=https://claw.yesy.live and
  LITELLM_API_BASE=https://litellm.vllm.yesy.live so devs don't need to
  override the URLs.
- .env.example: shrinks to BOT_ID + FASTCLAW_ADMIN_TOKEN (required) plus
  three optional overrides; instructions point at ~/.fastclaw/config.json.staging
  for the admin token (matches what fastclaw-cli already uses).
- openclaw.json.tmpl: kept as-is — pod's runtime/config can't be reused
  because it embeds cluster-internal URLs that don't resolve from the dev
  machine.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(devcontainer): bump openclaw-docker image 2026.4.2.12 → 2026.4.2.19

Same 2026.4.2 schema series — defaultConfigs["2026.4.2"] in
.devcontainer/openclaw.json.tmpl remains valid.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(devcontainer): move config rendering host-side, slim postCreate

The previous design did everything inside the container (postCreate would
curl fastclaw, render openclaw.json, validate, then start the gateway).
Restructure so config preparation happens BEFORE the container starts:

- initializeCommand.sh (host) now does all the heavy lifting in 5 numbered
  steps: validate .env, fetch bot from fastclaw admin API, render
  .devcontainer/openclaw.env (compose env_file) and .devcontainer/openclaw.json
  (bind-mounted into container), pull image, host fs setup. The fetched
  deployment.env is also rewritten to swap cluster-internal LiteLLM URL
  (http://litellm.openclaw.internal) for the public host so the gateway
  can actually reach it from a dev machine.
- docker-compose.yml uses env_file: openclaw.env to pipe all 17 vars
  into the container env at start (USER_INTERNAL_TOKEN, AGENT_IDENTITY_*,
  LITELLM_API_KEY, BOT_TOKEN, etc.) and bind-mounts openclaw.json.
- postCreateCommand.sh shrinks from 220 lines to ~100: just sanity-check
  the bind-mount, openclaw config validate (with doctor --fix fallback),
  start gateway, poll /healthz. No more curl/jq/envsubst/rcfile-patching
  inside the container.
- .gitignore: ignore the three host-generated files (openclaw.env contains
  every API key, openclaw.json embeds them, .gateway-token is the bot's
  shared secret).
- Bonus fixes from earlier rounds: trailing-newline guarantee in upsert,
  fused-key corruption detection only on script-managed key names (no
  longer false-flags base64 padding =), `version: "3.8"` removed,
  container_name dropped to let compose auto-name.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(devcontainer): use config dir not package dir for OPENCLAW_HOME, surface webchat URL

- Image's Dockerfile sets OPENCLAW_HOME to the npm package install dir
  (/usr/local/lib/node_modules/openclaw); the config + workspace dir is
  the symlink target /home/node/.openclaw. The image's own init.sh hard-
  overrides this for the same reason — postCreate must too, otherwise
  the bind-mounted openclaw.json is not found.
- Add webchat URL to the "How to interact" block. Pattern matches what
  fastclaw bot_connect.go:78 generates: <base>/#token=<token>. For dev
  that's http://localhost:18789/#token=$GATEWAY_TOKEN.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(devcontainer): simplify post-setup message

Replace the per-step list (already shown by postCreate) with a brief
"~1 minute, watch the Dev Containers panel" hint.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(devcontainer): split cluster-wide env into committed openclaw-default.env

The fastclaw admin API only returns per-bot db deployment.env, which
doesn't include cluster-wide pod_default vars (LITELLM_API_BASE,
ANTHROPIC_BASE_URL, GEMINI_PROJECT_ID, etc.) — those come from helm
defaultDeployment.env. Without them the gateway boots but skills can't
reach LiteLLM (LITELLM_API_BASE missing) and Vertex (GEMINI_* missing).

- New committed file .devcontainer/openclaw-default.env mirrors
  gcp-foundation/.../openclaw-fastclaw/values.yaml defaultDeployment.env,
  with cluster-internal LiteLLM URL (http://litellm.openclaw.internal)
  rewritten to public (https://litellm.vllm.yesy.live).
- docker-compose.yml loads two env_file in order: openclaw-default.env
  first (committed defaults), openclaw.env second (per-bot, generated).
  compose-spec semantics: last-listed file wins on duplicate keys, so
  per-bot values override defaults where they collide.
- initializeCommand.sh's openclaw.env writer no longer needs to
  inline-emit the helm defaults — that's openclaw-default.env's job.

Drift risk: openclaw-default.env must be kept in sync with
gcp-foundation values.yaml. Recommend a scheduled monthly diff.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(devcontainer): split postCreate/postStart, fix gateway lifecycle, branding

End-to-end verified after multiple rebuild cycles. The devcontainer now
boots cleanly, openclaw gateway survives across `docker restart`, and
host can hit http://localhost:18789 (webchat) directly.

Lifecycle restructure (the meat):
- New postStartCommand.sh runs on every container start (initial create
  AND every `docker restart`), so a crashed/restarted gateway recovers.
  postCreateCommand drops gateway start and keeps only the one-time
  init: chown /home/node/.openclaw (docker bind-mount flips it to root,
  blocks node user mkdir), recreate state dirs (.codex/.acpx/.agents),
  symlink ~/.agents, run /init-agent-workspace.sh main, validate config.
- Override image ENTRYPOINT to ["sleep", "infinity"]. Image's own
  init.sh fails as node user against root-owned /home/node/.openclaw
  (chown only happens in postCreate, but ENTRYPOINT runs first), so
  let postCreate own all init.
- Add `init: true` to compose so tini reaps zombies — without it,
  crashed gateway processes leave [openclaw] <defunct> entries.
- Use `setsid openclaw gateway run` (not bare `openclaw gateway`,
  which is the systemd service installer; not just `nohup`, which
  doesn't fully detach — gateway dies ~5s after postStart returns due
  to SIGHUP propagation through Cursor's exec wrapper).

Bind mounts:
- /workspace mounted from .devcontainer/.workspace (host bind, not
  named volume — uid mapping preserved for node-user mkdir; named
  volume initializes as root-owned and breaks init-agent-workspace.sh).
  Pre-create with .gitkeep so first rebuild doesn't have to mkdir.

Branding & UX:
- "ecap-skills devcontainer" → "zooclaw devcontainer" (banner +
  devcontainer.json name + final ready message).
- workspaceFolder: .openclaw/skills → /home/node so terminals open in
  HOME (also avoids openclaw scanning workspace/.devcontainer/.env).
- forwardPorts removed; rely on compose `ports: 18789:18789` for
  direct host bind, with portsAttributes for VSCode label.
- Slim VSCode extensions list 14 → 2 (python + pylance only). Cursor
  has built-in AI so Copilot is redundant; jupyter/gitlens/docker/
  github-actions not needed in this repo. Cuts rebuild time noticeably.
- postCreate output structured in numbered phases with green/yellow/
  red markers; initializeCommand tail has yellow boxed "PLEASE BE
  PATIENT — gateway boot ≈ 1 minute" banner; postStart prints big
  green "ZOOCLAW DEVCONTAINER IS READY" when /healthz returns 200.

Compose:
- Disable image's HEALTHCHECK (postStart owns the readiness signal —
  having both means redundant "(starting)" → "(unhealthy)" status that
  misleads when config is broken).

.gitignore:
- .devcontainer/.workspace/* (with !.gitkeep exception so the
  bind-mount target dir always exists).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(devcontainer): preserve openclaw.json edits across rebuilds

Previously initializeCommand.sh always re-rendered openclaw.json from
the template on every rebuild, wiping any models / channels / etc the
user had added directly to the file.

Skip render if the rendered openclaw.json already exists (and is
non-empty). Two escape hatches when a fresh render is actually wanted
(after rotating LITELLM_API_KEY upstream, changing the .tmpl, etc):

  rm .devcontainer/openclaw.json && rebuild
  # or
  OPENCLAW_FORCE_RERENDER=1 in .devcontainer/.env

Documented in .env.example.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(devcontainer): track rolling :2026.4.2 tag instead of pinning .19

openclaw-docker CI now publishes both :2026.4.2.X (immutable) and
:2026.4.2 (rolling minor track) on each tag push (see
openclaw-docker#59). Devcontainer pins the rolling one so devs pick
up new patches automatically — initializeCommand.sh already does
`docker pull --platform linux/amd64 "$IMAGE"` on every rebuild, so
GHCR digest comparison brings the latest down without manual bumps.

Production / staging stay on the immutable tag for reproducibility.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(devcontainer): clearer banners for postCreate vs postStart

postCreate's job is validation + one-time init; postStart's job is
starting the gateway. Make banners reflect that:

- postCreate header:  "postCreate" → "postCreate validation"
- postCreate footer:  "one-time init complete — gateway will start via
                       postStartCommand"
                       → "validation passed — postStartCommand starts
                       the gateway next"
- postStart header:   add matching "postStart: gateway" banner so the
                      Dev Containers panel reads as two clear sections.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(devcontainer): user guide for zooclaw devcontainer

Walks through prerequisites, first-time setup (clone → fill .env →
reopen in container), the 4-stage lifecycle (initializeCommand /
container / postCreate / postStart), common workflows (skill dev,
config edits with hot-reload, image upgrades, plugin/runtime dev),
file reference, and troubleshooting.

Also captures architecture decisions that get asked repeatedly:
ENTRYPOINT override, postCreate/postStart split, setsid for gateway
detach, host bind-mount workspace dir, rolling :2026.4.2 image tag.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(devcontainer): use <container> placeholder, drop hardcoded user name

Replace `ecap-skills-zhuguangbin-app-1` with the existing `<container>`
convention used elsewhere in the README. Add a short callout near the
top explaining how compose derives the actual name (`ecap-skills-$USER-
app-1`) so readers can substitute correctly.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(devcontainer): route Claude models via anthropic provider in tmpl

Tested in container: Claude responses route correctly through LiteLLM's
/v1/messages endpoint. Native Anthropic-messages format gives better
tool-use semantics than openai-completions translation.

- claude-sonnet-4-6 + claude-haiku-4-5 moved from openai → anthropic
  provider (with full metadata: input/contextWindow/maxTokens/compat)
- anthropic provider gets api: anthropic-messages and auth: api-key
- agents.defaults: heartbeat / model.primary / compaction now reference
  anthropic/claude-*; pdfModel was already anthropic
- openai provider keeps non-Claude models (gpt-5.4, gemini-3-flash,
  kimi-k2.6) as fallbacks; memorySearch keeps openai/text-embedding-3
  (Claude doesn't do embeddings)

A matching gcp-foundation PR will follow to apply the same change to
defaultConfigs["2026.4.2"] across dev/staging/production.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body
## Summary

Turns the ecap-skills devcontainer from a passive shell into a real, runnable openclaw gateway, mirroring how a bot pod is configured in staging.

**3-layer config init in `postCreateCommand.sh`** (matches the layering fastclaw does at pod start):

1. **Base** — full `defaultConfigs[\"2026.4.2\"]` from `gcp-foundation/.../openclaw-fastclaw/values.yaml` (5 LiteLLM models, all plugins, diagnostics-otel, zooguardian, tool denylist, gateway hot-reload — preserved verbatim, drift-trackable)
2. **Overlay** — the `_bot_lifecycle.py:create_bot` db patch from `ecap-workspace` (provider apiKey/baseUrl, memorySearch.remote)
3. **Env** — 31 vars passed through compose covering helm `defaultDeployment.env` + zooclaw per-bot deployment.env + bot identity (`BOT_*`)

Renders via `envsubst` → `~/.openclaw/openclaw.json` → `openclaw config validate` (with `doctor --fix` fallback per `start-gateway.sh`) → background `openclaw gateway --port 18789 --bind lan --allow-unconfigured --dev`.

## Files

- `.devcontainer/openclaw.json.tmpl` — new, complete merged template
- `.devcontainer/postCreateCommand.sh` — render + validate + autostart gateway; auto-generate `GATEWAY_TOKEN` and persist to `~/.openclaw/.gateway-token`
- `.devcontainer/docker-compose.yml` — port `8000→18789`; pass through all 3 env layers; smart defaults (`*_BASE_URL` derived from `$LITELLM_API_BASE`, `*_API_KEY` from `$LITELLM_API_KEY`, `BOT_*` from `$USER` + `$GATEWAY_TOKEN`)
- `.devcontainer/.env.example` — documents all 3 layers, staging public URLs as reference, secrets blank

## Test plan

- [ ] `cp .devcontainer/.env.example .devcontainer/.env`, fill in `LITELLM_API_BASE` + `LITELLM_API_KEY`
- [ ] VSCode → \"Reopen in Container\" → confirm postCreate finishes
- [ ] `cat ~/.openclaw/openclaw.json` — env vars substituted, no `${...}` placeholders
- [ ] `tail -f ~/.openclaw/gateway.log` — gateway boots, listens on 18789
- [ ] `curl http://localhost:18789/healthz` from host
- [ ] `cat ~/.openclaw/.gateway-token` — token persisted and stable across container rebuild
- [ ] Send a test message through any wired channel (or via gateway HTTP) and verify a LiteLLM model responds
- [ ] Toggle `OPENCLAW_AUTOSTART=0` in `.env` and rebuild — confirm gateway does NOT start

## Drift risk

`openclaw.json.tmpl` and the env list mirror `gcp-foundation/.../openclaw-fastclaw/values.yaml` (`defaultConfigs[\"2026.4.2\"]` + `defaultDeployment.env`) and `ecap-workspace/.../_bot_lifecycle.py:create_bot`. Recommend a monthly scheduled diff against those sources to keep parity.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
