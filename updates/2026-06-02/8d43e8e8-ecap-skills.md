---
title: "[Skill] make openclaw work on 2026.5.7 (config schema + skill exec)"
type: "Skill 上架/更新"
priority: "中"
date: "2026-06-02"
status: "待审核"
channels: ""
---
# [Skill] make openclaw work on 2026.5.7 (config schema + skill exec)

## 核心宣传点
来自 ecap-skills 仓库的更新：fix(devcontainer): make openclaw work on 2026.5.7 (config schema + skill exec)

## 原始内容
**Commit**: 8d43e8e89251932992af6090c2d41df269bf2015
**Title**: fix(devcontainer): make openclaw work on 2026.5.7 (config schema + skill exec) (#210)
**Author**: felix-srp
**Date**: 2026-06-02T03:04:15Z

**PR**: #210

### Commit Message
```
fix(devcontainer): make openclaw work on 2026.5.7 (config schema + skill exec) (#210)

* fix(devcontainer): migrate openclaw config to 2026.5.7 schema

Bump openclaw-docker image 2026.4.2 → 2026.5.7 and migrate the config
template to the stricter 2026.5.7 schema. Without this, the gateway fails
config validation on startup and never comes up — so the bot serves no
skills (deep-research et al. are on disk but nothing loads them) and none
of the zooclaw defaults apply.

openclaw.json.tmpl changes (validated against 2026.5.7 via `openclaw doctor`
+ a live gateway start — comes up healthy, all 27 managed skills ready):
- Remove agents.defaults.llm (legacy; idle timeout now follows
  models.providers.<id>.timeoutSeconds).
- plugins.entries.acpx: drop the config block (command/permissionMode are
  no longer allowed — "must NOT have additional properties"); keep the
  plugin enabled so the ACP backend still loads (verified: 7 plugins incl.
  acpx, "embedded acpx runtime backend registered").
- models.providers.{openai,anthropic}: add "enabled": true — 2026.5.7 no
  longer auto-enables a configured provider ("model configured, enabled
  automatically" migration).

Note: discord and diagnostics-otel are enabled in the template but ship as
external plugins in 2026.5.7 (not bundled) — they log non-fatal "plugin not
installed" warnings until `openclaw plugins install @openclaw/{discord,
diagnostics-otel}`. Left as-is; not a startup blocker.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(devcontainer): set OPENCLAW_HOME=/home/node so skill exec works on 2026.5.7

The image bakes OPENCLAW_HOME=/usr/local/lib/node_modules/openclaw, whose
`.openclaw` is a symlink → /home/node/.openclaw. openclaw 2026.5.7's
exec-approvals security (assertNoSymlinkPathComponents) refuses to traverse a
symlink in the approvals path, so it can't persist approvals and EVERY skill
`exec` fails ("Refusing to traverse symlink in exec approvals path:
.../openclaw/.openclaw"). This left uploaded-file workflows (e.g. the pptx
template flow) unable to run their scripts.

Override OPENCLAW_HOME=/home/node (compose `environment:`) — the real OS home,
whose config dir resolves to /home/node/.openclaw (= $OPENCLAW_HOME/.openclaw),
the same path the config volume + skills/extensions binds already use. The
approvals path is then all-real, no symlink. Verified by replicating openclaw's
exact check: baked home → REFUSED at the .openclaw symlink; /home/node → OK.

Must be the PARENT of .openclaw (/home/node), never /home/node/.openclaw itself
(config dir = join(home, ".openclaw") would double to .openclaw/.openclaw — the
case the old postCreate comment warned about). The install-dir symlink is left
in place as a harmless compat shim. postCreate comment updated to match.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description
Two fixes so the devcontainer's openclaw bot works after the image bump `2026.4.2 → 2026.5.7`. Both are cases where 2026.5.7 is stricter than 2026.4.2 about config/paths the devcontainer relied on.

## 1. Config schema migration (gateway wouldn't start)

The committed `openclaw.json.tmpl` used 2026.4.2-era keys 2026.5.7 rejects, so the gateway failed validation on every startup — no bot, no skills, no defaults.

- Remove `agents.defaults.llm` (legacy; → `models.providers.<id>.timeoutSeconds`)
- `plugins.entries.acpx`: drop the `config` block (`command`/`permissionMode` no longer allowed); keep `enabled: true` so the ACP backend still loads
- `models.providers.{openai,anthropic}`: add `"enabled": true` (2026.5.7 no longer auto-enables a configured provider)
- `docker-compose.yml`: pin image `2026.5.7`

Verified: gateway healthy, `openclaw skills list` → 46/80 ready, all 27 managed skills incl. `pptx`/`deep-research`/`designer`.

## 2. Skill `exec` was broken (uploaded-file workflows couldn't run)

Even with the gateway up, every skill `exec` failed:
`Refusing to traverse symlink in exec approvals path: /usr/local/lib/node_modules/openclaw/.openclaw`

Cause: the image bakes `OPENCLAW_HOME=/usr/local/lib/node_modules/openclaw`, whose `.openclaw` is a **symlink** → `/home/node/.openclaw`. 2026.5.7's exec-approvals security refuses to traverse a symlink in the approvals path, so it can't persist approvals and **all** `exec` fails. (This blocked the pptx template-from-upload flow — the bot couldn't run the skill scripts and fell back to the wrong tools.)

Fix: override **`OPENCLAW_HOME=/home/node`** (compose `environment:`) — the real OS home, whose config dir resolves to `/home/node/.openclaw` (= `$OPENCLAW_HOME/.openclaw`), the same path the config volume + skills/extensions binds already use. The approvals path is then all-real, no symlink.

- Must be the **parent** of `.openclaw` (`/home/node`), never `/home/node/.openclaw` itself (config dir = `join(home, ".openclaw")` would double it — the case the old `postCreate` comment warned about). Comment updated.
- The install-dir symlink is left as a harmless compat shim.

Verified by replicating openclaw's exact `assertNoSymlinkPathComponents` check: baked home → REFUSED at the `.openclaw` symlink; `/home/node` → OK (no symlink components).

**Applies on next devcontainer rebuild** (the volume + binds already live at `/home/node/.openclaw`, so no data moves).

## Notes (out of scope)
- The running container keeps getting an external `SIGTERM` (exit 143, not OOM) — likely Docker Desktop / IDE Dev-Containers reconnecting. Independent of these fixes.
- `discord`/`diagnostics-otel` are enabled in the template but are external plugins in 2026.5.7 — non-fatal "plugin not installed" warnings until `openclaw plugins install @openclaw/{discord,diagnostics-otel}`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

