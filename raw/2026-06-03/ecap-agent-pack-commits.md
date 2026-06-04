# ecap-agent-pack — 2026-06-03

共 4 条 commits

## [c2382ff7] fix(zoo-captain): don't corrupt JSON with URL values when verifying dmScope (#158)

- **SHA**: `c2382ff7e393d1a35b5be938c710366a3316aa3d`
- **作者**: vincent-srp
- **日期**: 2026-06-03T08:00:06Z
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/c2382ff7e393d1a35b5be938c710366a3316aa3d

### 完整 Commit Message

```
fix(zoo-captain): don't corrupt JSON with URL values when verifying dmScope (#158)

* fix(zoo-captain): don't corrupt JSON with URL values when verifying dmScope

verify_deploy.py and set_runtime_config.py stripped `//` comments
unconditionally, which ate the `//` inside URL string values (e.g.
"https://docs.openclaw.ai/"), corrupting otherwise-valid JSON and making
dm_scope_per_peer falsely FAIL on a correctly-configured openclaw.json
(BOOTSTRAP Step 4 false fail).

Fix: parse strict JSON first (URL values survive untouched); only a JSON5-ish
config (comments / trailing commas) falls back to a string-aware strip that
keeps `//` inside string literals. Adds regression tests for URL values in both
standard JSON and JSON5-with-comments. pytest: 59 passing.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* feat(zoo-captain): add C-side quick_commands to manifest

Six one-tap shortcuts (how-to / fix-issue / review-usage / explain-concept /
find-agent / build-my-agent), each firing its prompt verbatim as the customer's
message. Kept in sync with the staging catalog (2026-06-03). They map onto the
pack's skills: diagnose-env / insight-review / teach-concept / tour-specialist /
handoff-to-studio.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Bug
`verify_deploy.py` / `set_runtime_config.py` stripped `//` comments **unconditionally**, so the `//` inside a URL string value (e.g. `"https://docs.openclaw.ai/"`) got eaten → an otherwise-valid `openclaw.json` was corrupted → `dm_scope_per_peer` **falsely FAILs** even when `session.dmScope` is correctly set (BOOTSTRAP Step 4 false fail).

## Fix
Parse **strict JSON first** — a standard config (with URL values) is safe and never touched by the comment rule. Only a JSON5-ish config (comments / trailing commas) falls back to a **string-aware** strip that keeps `//` inside string literals.

## Verify
- Repro: standard JSON with a URL → old strip → `"https:` (unterminated string) → parse fail.
- After: strict-first parse → succeeds. New regression tests cover a URL value in standard JSON **and** in JSON5-with-comments.
- `pytest`: **59 passing**.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [080cce2b] feat(founder-ip-studio): 升级到 2.0.1 — 新增定妆图与外貌描述双重锁定 (#159)

- **SHA**: `080cce2ba2f5e74eae898b8c47282ef5261624fa`
- **作者**: lynn Zhuang
- **日期**: 2026-06-03T07:47:27Z
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/080cce2ba2f5e74eae898b8c47282ef5261624fa

### 完整 Commit Message

```
feat(founder-ip-studio): 升级到 2.0.1 — 新增定妆图与外貌描述双重锁定 (#159)

将数字分身素材体系从 3 项（人脸/声音/场景）扩展到 5 项
（人脸/声音/定妆图/外貌描述/场景），解决 Seedance 单张照片
无法推断完整服装造型、每条视频形象漂移的问题。

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## 升级背景

  在 2.0.0 中，数字分身只锁定了 **人脸 / 声音 / 场景**
  三项素材。实际生产时暴露两个问题：

  1. **服装造型每条视频都漂移** — Seedance
  只能从单张人脸照片推断衣着，每次生成的服装/发型/整体形象都在变。
  2. **创始人形象不一致** — 缺少明确的外貌描述写入 prompt，模型会自由发挥。

  本次升级把素材体系从 3 项扩展到 **5 项**，新增 **定妆图 (costume)** 和
  **外貌描述 (appearance)**，从素材层和 prompt 层双重锁定形象一致性。

  ## 主要变更

  ### `founder-director` skill
  - 新增 **Step 3.1.5「定妆参考图」** — 基于 Step 3.1 用户照片，用 `designer`
  skill (gpt-image-2) 自动生成 4 张标准化定妆图（正脸特写 / 半身 / 全身 / 3/4
  侧面），用 Pillow 拼成 2×2 网格发给用户确认，注册成 `costume_assets` 写入
  profile。
  - demucs 提取人声后必须立即 `message(media=...)`
  让用户试听，确认无杂音才能继续。
  - **Step 3.2 素材确认升级为 5 项**（人脸 / 声音 / 定妆图 / 外貌描述 /
  场景），按顺序逐一发出，全部确认后才能锁定 profile。
  - Profile schema 新增 `costume_assets` 字段。

  ### `chameleon-bridge` skill
  - 视频生成时从 profile **动态读取全部 5 项素材**：
    - `face_assets` + `costume_assets` + `scene_assets` → 全部传入
  `--reference-image`
    - `voice_ref` → `--reference-audio`
    - `appearance` → 注入 prompt 的 `[APPEARANCE LOCK]` 块
  - 五项素材缺一项即报错，不得继续生成。

  ### `AGENTS.md`
  - Phase 3 素材确认表述从「人脸/声音/场景三项」改为「五项缺一不可」。

  ### `agent-pack.yaml`
  - `version`: `2.0.0` → `2.0.1`
  - `dependencies.python`: 新增 `Pillow`（用于拼定妆网格图）。

  ### 其他
  - `auto-caption`、`founder-post`、`zooclaw-forcedalign` 的 SKILL.md
  与脚本同步小幅调整（与上述链路配套）。

  ## Diff 范围
  12 files changed, +588 / −78

  ## 验证清单
  - [ ] 在测试环境跑一遍 `founder-director` 全流程，确认 Step 3.1.5
  定妆图能正常生成并拼成 2×2 网格
  - [ ] 确认 demucs 后人声音频能 `message(media=...)` 正确发出试听
  - [ ] 确认 Step 3.2 五项素材依次发出并阻塞等待确认
  - [ ] 确认 `chameleon-bridge` 视频生成时 5 项素材全部拼装到 Seedance 参数与
  prompt
  - [ ] 注意：解压 zip 导致 5 个 .sh/.py 脚本的 exec 位被剥（100755 →
  100644），如运行时需要直接执行需手动 `chmod +x` 恢复


---

## [8c15d13e] chore(video-duplicate): update pack to 1.9.7 (#157)

- **SHA**: `8c15d13e72d52e065975d86bb7e611d783645278`
- **作者**: vincent-srp
- **日期**: 2026-06-03T04:33:36Z
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/8c15d13e72d52e065975d86bb7e611d783645278

### 完整 Commit Message

```
chore(video-duplicate): update pack to 1.9.7 (#157)
```

### PR Body

## What

Update the `video-duplicate` pack from **1.9.2 → 1.9.7** by mirroring the published `build/video-duplicate-1.9.7.tar.gz` byte-for-byte (`diff -r` against the tarball is empty).

## Changes (17 files, +498 / -616)

**Functional**
- `storyboard-studio/run_pipeline.py` — concurrent panel redraw (≤3 at a time, 600s/chunk timeout, skip already-completed) to fix `gpt-image-2` SIGTERM/timeout on serial redraw
- `seedance-runner/run_chunks.py` — enforce `720p` from plan top-level `seedance.resolution` (overrides per-chunk cache)
- `style-duplicate` + `storyboard-studio` — prepend `[REFERENCE IMAGES]` anchors for higher subject fidelity
- `storyboard-replicate` / `style-duplicate` — 600s subprocess timeout with clear error
- Gemini `max_tokens` 12000 → 32000 with 2× auto-retry on truncation

**Docs / metadata**
- `description.json` — rewritten to English + version → 1.9.7
- `SOUL.md` — persona reword + baked-in user context
- `AGENTS.md` — new troubleshooting entries
- `agent-pack.yaml` — version → 1.9.7

**Removed (as shipped in tarball)**
- `.agents/skills/pack-onboarding/` (SKILL.md + 3 scripts)

## ⚠️ Known issue carried from the released tarball

The 1.9.7 tarball **drops the `pack-onboarding` skill files** but its own `agent-pack.yaml` (lines 89–96) and `AGENTS.md` (line 45) **still reference it** → dangling reference in the shipped package. Kept as-published per a deliberate "strict mirror" decision. Fix belongs upstream in the build/packaging step.

> 🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [cef1ce0b] feat(zoo-captain): add central customer-support pack (#156)

- **SHA**: `cef1ce0b26aeb6b054d86caeeae712a5e94f061c`
- **作者**: vincent-srp
- **日期**: 2026-06-03T03:36:18Z
- **URL**: https://github.com/SerendipityOneInc/ecap-agent-pack/commit/cef1ce0b26aeb6b054d86caeeae712a5e94f061c

### 完整 Commit Message

```
feat(zoo-captain): add central customer-support pack (#156)

* feat(zoo-captain): add central customer-support pack

zoo-captain (Captain) is a central, multi-customer support agent for
OpenClaw/ZooClaw: answers grounded in verified sources (无据不答), isolates
DMs via runtime session.dmScope=per-channel-peer, and escalates to
support@zooclaw.ai only after customer confirmation.

Includes 8 skills under .agents/skills, root + skill scripts, a single
knowledge source registry (data/sources.yaml) feeding data/knowledge
(6 sources + INDEX/CHANGELOG), and a deterministic deploy bootstrap
(set_runtime_config + optional seed_config; verify_deploy hard-fails on an
unverifiable dmScope when --openclaw-config is explicit). pytest: 56 passing.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* feat(zoo-captain): add optional daily knowledge-refresh ops cron to BOOTSTRAP

Schedule a non-delivering (--no-deliver) isolated OpenClaw cron that runs
sync-knowledge daily. It uses the agent's own agent_id (from the identity seed)
and needs no peer_id, so it is feasible for central support — unlike a delivering
cron. Kept optional/non-blocking, with a quality note that an unattended fetch can
silently pollute the baseline.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

* docs(zoo-captain): use full script paths in skill-private docstrings

fetch_source / run_diagnosis / collect_signals / update_tips / finalize_review
showed `scripts/<name>.py` in their own docstring Usage examples, but they live
under .agents/skills/<skill>/scripts/ and run with cwd=workspace-root. The
examples now use the full path, matching the SKILL.md commands. Docstring-only —
no behavior change.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What
Add **zoo-captain** (Captain) — a central, multi-customer support agent for OpenClaw/ZooClaw — as a top-level pack (packaged/runtime layout: root identity + `.agents/skills/`, consistent with repo convention).

## Highlights
- **Grounded answers (无据不答)**: every platform answer needs a source URL or an explicit uncertainty statement; never fabricates.
- **Multi-customer isolation**: runtime `session.dmScope = per-channel-peer` (set at deploy, top-level `session` key — not `agents.defaults.session`); per-customer notes in `customers/<key>.md` outside the memory tree, never cross-leaking.
- **Confirm-before-send escalation** to support@zooclaw.ai.
- **Single knowledge registry**: `data/sources.yaml` → `data/knowledge/` (6 sources + INDEX + CHANGELOG), refreshed by `sync-knowledge`; `search-knowledge` works a 5-layer evidence chain.
- **Deterministic deploy bootstrap**: `set_runtime_config.py` (idempotent, path-resolved, merge-safe) + optional ops `seed_config.py` identity; `verify_deploy.py` **hard-fails on an unverifiable dmScope when `--openclaw-config` is explicit** (no false-green skip).
- 8 skills under `.agents/skills/`, root + skill scripts, **pytest: 56 passing**.

## Notes
- Runtime files (`data/config.json`, caches) are gitignored.
- Identity seed is an optional ops step (does not block deploy completion); customer Q&A works without it.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

