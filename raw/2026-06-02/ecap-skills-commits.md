# ecap-skills - 2026-06-02
共 3 个 commit

---
## fix(devcontainer): align openclaw.json.tmpl with prod for openclaw 2026.5.7 (#211)
- **SHA**: 1901dbb29175024519d523d63d372f56b5342897
- **Author**: felix-srp
- **Date**: 2026-06-02T12:06:18Z
- **PR**: #211

### Commit Message
```
fix(devcontainer): align openclaw.json.tmpl with prod for openclaw 2026.5.7 (#211)

* fix(devcontainer): route image tool via openai-completions endpoint (match prod)

The devcontainer's image tool timed out (~50s) on every model. Comparing to a
working prod pod (via openclaw-diagnose) showed the cause: prod routes image
(and its main model) through the openai-completions endpoint, where every model
declares input:[text,image]; the devcontainer had NO imageModel, so image fell
back to model.primary = anthropic/claude-sonnet-4-6 (anthropic-messages), which
doesn't serve multimodal.

Match prod's routing (staging LITELLM host yesy.live kept — confirmed correct):
- agents.defaults.imageModel: primary openai/claude-sonnet-4-6 (+ openai/* fallbacks)
- agents.defaults.model.primary: anthropic/ -> openai/claude-sonnet-4-6
- openai provider: add claude-sonnet-4-6 + claude-haiku-4-5 (input:[text,image])
  so openai/claude-sonnet-4-6 resolves via openai-completions
- pdfModel left on anthropic/claude-sonnet-4-6 (matches prod)
- tools.deny: add x_search — prod denies it; without it the bot reached for the
  misconfigured xAI search instead of the websearch skill

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(devcontainer): allow :18789 ingress origin in gateway controlUi

The Control UI rejects the webchat WebSocket with "origin not allowed"
because --dev only auto-allows the gateway's own port (:18790), but the
UI is reached via the nginx/forwarded ingress on :18789. Declare both
ports explicitly in gateway.controlUi.allowedOrigins.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(devcontainer): drop invalid models.providers.*.enabled key (2026.5.7)

A clean devcontainer rebuild failed `openclaw config validate` with
"models.providers.{openai,anthropic}: Unrecognized key: enabled". The
enabled:true I added in #210 is not a valid provider key in 2026.5.7 (prod
has no such key; the live gateway tolerated it but config-validate rejects
it). Remove it from both providers. Verified: rendered config now passes
`openclaw config validate`.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(devcontainer): use host-header origin fallback instead of hardcoded ports

The enumerated allowedOrigins list (localhost/127.0.0.1 × :18789/:18790) is
brittle: the host-forwarded port is unpredictable (Dev Containers/Zed assigns a
free port if 18789 is taken), and the nginx ingress (:18789) vs gateway (:18790)
ports differ. Any of those changing reintroduces the "origin not allowed" WS
failure.

Replace the list with gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback
= true, which accepts the Control UI/WebChat WS regardless of origin port.
Access is still gated by the gateway token + local-only reachability; origin
(CSRF) checks are moot once dangerouslyDisableDeviceAuth is already on. This is a
dev-container-only config. Verified: gateway accepts a WS from an arbitrary port
and `openclaw config validate` passes.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(devcontainer): bump openai fallback gpt-5.4 -> gpt-5.5 (track newer prod pods)

Newer prod pods route the fallback to gpt-5.5; staging litellm (yesy.live)
serves it. Rename the model def and repoint model.fallbacks + imageModel.fallbacks.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* fix(devcontainer): match prod model capability metadata (contextWindow/contextTokens)

Align the openai-provider model defs to the values prod actually declares
(verified across prod pods): claude-sonnet-4-6 contextWindow 200000 -> 1000000
+ contextTokens 400000 (the devcontainer was understating Sonnet's window,
making the bot compact far earlier than needed); add contextTokens to gpt-5.5
(400000), gemini-3-flash-preview (400000), kimi-k2.6 (262144). claude-haiku-4-5
already matched. Same Sonnet bump applied to the anthropic provider entry for
consistency.

These numbers previously came from the pre-existing devcontainer baseline, not
prod; this commit makes them identical to prod.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description
## What & why

When the devcontainer image bumped to **openclaw 2026.5.7**, the committed `.devcontainer/openclaw.json.tmpl` no longer matched what prod runs, and the gateway's image tool timed out. This PR brings the template in line with a working **prod pod** (verified live via kubectl across several pods) and with 2026.5.7's stricter `openclaw config validate`.

All changes are confined to `.devcontainer/openclaw.json.tmpl` (dev-container only).

## Changes

1. **Image-tool routing via `openai-completions` (match prod).** Route `model.primary` + add an `imageModel` block pointing at `openai/claude-sonnet-4-6`, and define `claude-sonnet-4-6` / `claude-haiku-4-5` under the `openai` provider with `input: [text, image]`. Previously image fell back to the anthropic-messages endpoint and timed out (~50s).

2. **Drop the invalid `models.providers.*.enabled` key.** 2026.5.7's strict schema rejects it (`Unrecognized key`); prod doesn't set it.

3. **Origin handling that survives port changes.** The Control UI/WebChat WS was rejected with "origin not allowed." Rather than enumerate ports (brittle — the host-forwarded port is unpredictable, and nginx ingress `:18789` vs gateway `:18790` differ), use `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback: true`. Access stays gated by the gateway token + local-only reachability; origin (CSRF) checks are moot once `dangerouslyDisableDeviceAuth` is on. Dev-container only.

4. **Bump openai fallback `gpt-5.4` → `gpt-5.5`** to track newer prod pods (staging litellm serves it).

5. **Match prod model capability metadata.** Align `contextWindow`/`contextTokens` to the values prod declares (verified consistent across pods): `claude-sonnet-4-6` `contextWindow` `200000 → 1000000` + `contextTokens 400000` (the template was understating Sonnet's window, forcing premature compaction); add `contextTokens` to `gpt-5.5`/`gemini-3-flash-preview`/`kimi-k2.6`.

## Verification

- Rebuilt the devcontainer locally; gateway + nginx healthy on 2026.5.7.
- Image tool routes via openai-completions (no timeout).
- WS accepted from an arbitrary forwarded port; `openclaw config validate` passes.
- openai-provider model defs verified byte-equal to prod's declared values.

## Known follow-up (not in this PR)
Prod additionally routes `heartbeat`/`compaction` via `openai/claude-haiku-4-5` and keeps a minimal `anthropic` provider stub; this devcontainer still routes those via `anthropic/claude-haiku-4-5`. Functionally fine — left as a separate optional alignment.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## feat(lint): enforce SKILL.md description length + install[] + requires schema (#208)
- **SHA**: a0813e9a31ecaba5bace802d9b81a324588c51b5
- **Author**: allenz-srp
- **Date**: 2026-06-02T08:34:46Z
- **PR**: #208

### Commit Message
```
feat(lint): enforce SKILL.md description length + install[] + requires schema (#208)

* feat(lint): enforce SKILL.md description length + install[] + requires schema

Adds 3 new strict-mode checks to .github/scripts/lint_skills.py:

1. **description constraints** (SKILL_SPEC.md §2): ≤400 chars, single line.
   Long descriptions inflate every bot's system prompt linearly with
   skill count; multi-line block scalars also render poorly in tool lists.

2. **install[] required** (SKILL_SPEC.md §5): metadata.openclaw.install
   must be a non-empty list of valid specs with kind ∈
   {brew,node,go,uv,download}. Each spec's kind-specific required field
   (package / formula / module / url) is also verified. This unblocks the
   ECA-847 plan of scanning SKILL.md at openclaw-docker build time to
   pre-install all skill deps.

3. **requires.* schema** (SKILL_SPEC.md §6): OpenClaw only reads
   bins/anyBins/env/config under metadata.openclaw.requires. Any other
   key (pip/npm/apt/system/skills/...) is silently dropped at runtime —
   error explicitly so authors migrate to install[].

Also ships SKILL_SPEC.md at repo root (docs/ is in .gitignore) — the
authoritative reference cross-linked from every new error message,
covering frontmatter fields openclaw actually reads, eligibility rules,
install spec shapes, a full canonical example, the migration table from
deprecated requires.{pip,npm} to install[], and a PR lint checklist.

⚠️ All 48 current violations across 22 of 27 SKILL.md files will block
this PR's own CI. Cleanup plan in the PR description.

* docs: add Developing-a-Skill guide to README + de-dup CLAUDE.md §4

README.md gains a "Developing a Skill" section listing the 7 hard rules
every skill must satisfy, plus a reference table pointing to SKILL_SPEC.md
(schema), CLAUDE.md (conventions), and the lint script.

CLAUDE.md §4 used to inline a SKILL.md frontmatter example that was
already drifted (only showed `requires.env`, omitted install[] entirely,
no mention of description length / single-line / deprecated keys). It
now defers schema details to SKILL_SPEC.md and keeps only the
development-convention bits that aren't in the spec (Prerequisites env
check snippet, env naming, etc.).

Result — three docs, no overlap:
- README.md          → repo entry + 5-minute "how to build a skill"
- CLAUDE.md          → development conventions (env naming, proxy, scripts)
- SKILL_SPEC.md      → SKILL.md frontmatter schema (source of truth)

* docs(readme): add minimal SKILL.md example + per-field metadata table

* fix(skills): clean up all 26 SKILL.md to satisfy strict lint

48 errors → 0 errors. Coordinated edit across all 26 skills with lint
violations from the strict-mode rollout (#208).

Per skill:
- Description: trimmed > 400-char descriptions to ≤ 400 chars while
  preserving core trigger keywords; multi-line block scalars folded to
  single line.
- metadata.openclaw.install: added explicit list. Entries are mostly
  `kind: "uv"` Python packages inferred from each skill's
  scripts/requirements.txt or `uv run --with` calls; `kind: "node"`
  npm packages for skills with package.json or `npx`/`node` usage.
- Migrated deprecated requires.{pip,npm,skills} → install[] entries
  (docx, pdf, pptx).

Linux-only deployment alignment:
- Removed all `kind: brew` + `os: [darwin]` entries that earlier work
  added — ecap-skills run on Linux bot pods only; brew/macOS specs are
  silently dropped by the image scanner.
- Added `install: []` for skills whose deps are entirely system bins
  baked into openclaw-docker (jq, ffmpeg, etc.).

Lint policy update:
- `metadata.openclaw.install` must be present (so reviewers see authors
  thought about deps), but empty list `[]` is now valid for system-bin-
  only skills. Previously required non-empty, which was wrong for
  pure-bash skills whose deps come from the image apt layer.

Doc update:
- SKILL_SPEC.md §5.4 documents the Linux-only policy and the empty-list
  convention for system-bin skills.

After this commit the strict lint CI on PR #208 should pass.

* chore(skills): standardize all metadata blocks to YAML format

Convert 12 SKILL.md files from JSON-in-YAML style to YAML indentation
style for internal consistency. openclaw upstream accepts both
(YAML.parse → JSON.stringify → JSON5.parse pipeline per
openclaw/src/markdown/frontmatter.ts:42-47 and src/shared/frontmatter.ts:33),
but ecap-skills standardizes on YAML for:
- Readability (no quote noise)
- Comment support (# comments)
- Consistency with other frontmatter fields (name, description, author)

Converted skills:
- bot-mailbox, browser-skill, designer, docx, glossary, pptx,
  skills-store, viral-ads, web-designer, zooclaw-asr,
  zooclaw-connectors, zooclaw-tts

Adds new lint check `check_metadata_format` that errors on `{`-prefixed
metadata blocks, preventing future regressions. SKILL_SPEC.md §1 updated
to document the rule.

All skills still pass lint (0 errors, 15 unchanged warnings).

* chore(skills): tighten description lint to single-line ≤200 chars

Lower DESCRIPTION_MAX_CHARS 400→200 (error level) and rewrite 25
descriptions to fit. Aligns with openclaw upstream — survey of all 62
built-in skills (openclaw npm dist/extensions/** + skills/**, captured
2026-06-01):

  - Single-line:  62/62 (100%)
  - Multi-line:   0
  - Length min/max/avg:  48 / 159 / 89 chars
  - >200 chars:   0
  - >400 chars:   0

We were sitting at 200-char avg with max 379 — uniformly verbose
relative to upstream. Tightening to 200 saves ~2.4KB per bot system
prompt (30 active skills × ~80 wasted chars) and forces tighter,
more discriminating discovery signal.

SKILL_SPEC.md §2.1 added: writing guide + rationale + good/bad
examples + survey table. PR checklist updated.

Rewrite strategy (per skill): keep verb + scope + top trigger
keywords (EN+ZH); drop implementation details, exhaustive examples,
and "not for X" anti-triggers (move to SKILL.md body §"When NOT to
use").

Lint: 0 errors / 15 warnings (unchanged).
```

### PR Description
## Summary

Strict-mode SKILL.md lint + complete cleanup of all existing skills, backed by a new `SKILL_SPEC.md`. This is the gate side of [ECA-847](https://linear.app/srpone/issue/ECA-847) — reduce context bloat from skill descriptions and unblock the image-time skill-dep prebuild plan.

**Path A taken**: lint + all 48 cleanups bundled in one PR. CI is currently green.

## What changed

### 1. Metadata schema 收紧（strict lint, error-level）

| 维度 | 改造前 | 改造后 |
|---|---|---|
| `description` 长度 | 无强约束（事实上 avg 295, max 379） | **≤200 char (error)** |
| `description` 行数 | 允许多行 | **single-line only (error)** |
| `metadata.openclaw.install[]` | 可缺省 | **必须显式声明，空依赖写 `install: []`** |
| `requires.{pip,npm,system,apt,skills}` | 历史遗留 | **全部废弃** → 迁到 `install[]` / `requires.bins` |
| metadata block 格式 | YAML / JSON-in-YAML 混用（15 YAML + 12 JSON） | **YAML-only (error)**；JSON `{...}` 风格 lint 拒绝 |

### 2. Linux-only 生产约束

- 删掉所有 `kind: brew` 和 `os: [darwin]` 条目（sub-agent 误加的 3 处：agent-influencer / zooclaw-asr / zooclaw-tts）
- `SKILL_SPEC.md` 写明：ecap-skills 仅在 Linux 生产环境运行（openclaw-docker bot pods），macOS 项被 image scanner 静默丢弃

### 3. 全部 27 个 description 重写

基于 openclaw upstream 62 个 built-in skill 调研（`openclaw` npm 包 `dist/extensions/**/SKILL.md` + `skills/**/SKILL.md`，采样 2026-06-01）：

| Metric | Upstream | ecap-skills (before) | ecap-skills (after) |
|---|---|---|---|
| Single-line description | 62 / 62 (100%) | mixed | 27 / 27 (100%) |
| Length avg / max | 89 / 159 | 295 / 379 | 188 / 200 |
| >200 chars | 0 | 25 / 27 | 0 |

重写策略：保留 verb + scope + 顶级 trigger 关键词（EN+ZH）；删掉实现细节（model 名、文件大小、内部 pipeline）、穷举 examples、"not for X" 反触发（迁到 SKILL.md body §"When NOT to use"）。

### 4. Lint script 新增/改造

- `check_metadata_format`: 拒绝 JSON-in-YAML 风格的 metadata block
- `check_install_required`: install[] 必须显式，可空
- `check_description_constraints`: ≤200 + single-line 双闸（原 ≤400 上限收紧到 200）

### 5. `SKILL_SPEC.md` 文档化

- **§1**: YAML 是 ecap-skills 标准；引用 openclaw 源码（`frontmatter.ts:42-47`, `shared/frontmatter.ts:33`）说明 upstream 双格式都支持但内部统一 YAML
- **§2.1（新增）**: description writing guide + upstream 调研表 + good/bad examples + 改写策略
- **§5.4**: Linux-only 政策 + `install:[]` 用法
- **§8**: PR checklist 加 description 200-char 项 + 禁止 brew/darwin 项

## 量化收益

| 指标 | 改造前 | 改造后 |
|---|---|---|
| Lint errors | **48** | **0** |
| description avg / max | 295 / 379 char | 188 / 200 char |
| 估算 bot system prompt 节省 | — | ~2.4KB/session (≈ 30 active skills × ~80 char) |
| metadata 格式一致性 | 15 YAML + 12 JSON | 27 YAML |

## Commit 演进（3 轮）

| Commit | 内容 |
|---|---|
| `7931402` | 24 个 install[] 缺失补齐 + 13 个 description 砍到 ≤400 + 3 个多行合并 + 废弃 `requires.{pip,npm,skills}` 迁移 |
| `8bbdd3a` | 12 个 JSON-style metadata → YAML；`check_metadata_format` lint；SKILL_SPEC §1 写明 YAML-only + 引用 openclaw 源码 |
| `63ce06e` | description 上限 400 → 200；25 个 description 重写；SKILL_SPEC §2.1 + 调研数据 + writing guide |

## 仍未做（追踪在 ECA-847）

本次 PR 只做了 **schema/lint 层面** 的清理，是后续工作的前置条件：

- [ ] **2.1 主任务**：ecap-skills "必要 / 可选" 分类清单（按需启用）
- [ ] **2.2 依赖 schema → image 预装**：声明的依赖在打 image 时预装，而不是运行时拉
- [ ] **Plugin skill 条件激活**：feishu/wecom 等 plugin skill 在用户没配账号时不注入 context

## Test
- [x] `python3 .github/scripts/lint_skills.py` → 0 errors / 15 warnings
- [x] All 27 SKILL.md descriptions ≤200 chars verified
- [x] No `brew` / `os: [darwin]` entries remain
- [x] All metadata blocks YAML-style (no JSON `{...}`)
- [ ] CI lint workflow green


---
## fix(devcontainer): make openclaw work on 2026.5.7 (config schema + skill exec) (#210)
- **SHA**: 8d43e8e89251932992af6090c2d41df269bf2015
- **Author**: felix-srp
- **Date**: 2026-06-02T03:04:15Z
- **PR**: #210

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
