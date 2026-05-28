# ecap-agent-pack Commits - 2026-05-27

共 3 条 commits

---

## feat(agent-studio): v1.4.0 — spec-driven build flow + release-zip filter (#145)

- **SHA**: [3c486753](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/3c486753dcbe3f0433d5d544eaf23cd283092991)
- **作者**: felix-srp
- **日期**: 2026-05-27T10:21:53Z
- **PR**: #145

### Commit Message

```
feat(agent-studio): v1.4.0 — spec-driven build flow + release-zip filter (#145)

* test(agent-studio): scaffold pytest layout

* feat(agent-studio): spec extract data model

* feat(agent-studio): mechanical satisfied_by pattern resolver

* test(agent-studio): fixtures for spec-coverage round-trip

* feat(agent-studio): spec_coverage.py render subcommand

* feat(agent-studio): spec_coverage.py sync subcommand

* feat(agent-studio): validate.py --check-spec flag (no-op stub)

* feat(agent-studio): validate.py walks spec items, gates Stage 4

* feat(agent-studio): scaffold.py --from-spec seeds identity + skills

* feat(agent-studio): Studio SOP for spec extraction

* feat(agent-studio): wire spec coverage into stage references

* test(agent-studio): end-to-end spec flow integration

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): preserve unsynced waivers; raise on .arr[].field selectors

* fix(agent-studio): yaml equality, notes round-trip, semantic edit persistence, --lang default + trim SOP

Addresses 4 high-severity findings from final code review:

1. yaml: patterns now support `==<value>` equality (not just truthiness).
   `yaml:agent/agent-pack.yaml:.name=="nutrition-buddy"` enforces the exact
   value the spec pinned, rather than ticking for any non-empty name.

2. `## Notes (unparsed)` round-trips: _render emits the section when
   notes_unparsed is non-empty; _apply_md_to_extract only overwrites the
   field when the md actually contained a Notes section, so prior notes
   survive when the creator removes the section from the .md.

3. validate.py persists semantic md edits by dumping the extract whenever
   the .md was applied (not just on auto_ticked). Re-render is still gated
   on auto_ticked so the existing notes-preservation behavior holds.

4. scaffold.py --lang default restored. `default=None` lets spec hydration
   take precedence; if both hydration and --lang are absent, `zh,en`
   applies. --lang is dropped from the required-fields list.

Trim pass on prose to recover tokens: references/spec-extraction.md
102→77 lines; compressed spec_coverage.py docstring and _shorten comment;
tightened _spec_patterns.py module docstring.

Tests: 32 pass (29 existing + 3 new: yaml_equality_match,
sync_preserves_existing_notes_when_md_lacks_section,
check_spec_persists_semantic_md_edits).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): address remaining 11 spec gate findings

- _spec_schema: add SpecItem.value field; reject mechanical items with
  empty satisfied_by at load time.
- _spec_patterns: tighten selector grammar (hyphen support, negative
  indices, full-path consumption check); reject absolute paths and
  `..` traversal; validate cron/data_source handler names; convert
  YAMLError to PatternError.
- spec_coverage: render id markers in bullets (<!-- id=... -->); sync
  now parses by id (dict-by-id), deletes items absent from md, and
  clears stale waiver_reason on done transition.
- validate: tighten _safe_resolve and check_spec exception handling
  to (PatternError, OSError) tuples.
- scaffold: use load_extract for hydration; prefer SpecItem.value over
  evidence parsing; reject invalid kebab-case names; clean error
  messages on missing/invalid spec files; lang now in required field
  list with from-spec-aware hint.
- Fixtures: add value field to identity items; regenerate golden md
  with id markers.
- Tests: add 12 new tests covering schema rejection, selector grammar,
  path security, handler name validation, id-tracked deletion,
  waiver-cleared-on-done, value-field hydration, kebab-name
  validation, and missing-file clean error.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): prevent silent data loss + 6 spec-gate issues from Claude/Codex review

* fix(agent-studio): round-2 review hardening — unknown-id wipe guard, stale evidence, empty == rhs, demotion re-render, atomic dump

* fix(agent-studio): require explicit --prune for item deletion (round-3 hardening)

* fix(agent-studio): v2 review pass — schema tightening, parser hardening, atomic md write, SOP value field

Schema (load_extract / dump_extract):
- reject newlines in title/description (would have triggered --prune wipe)
- reject non-string `value` (would have crashed scaffold)
- reject duplicate item ids
- atomic_write_text helper preserves existing file mode (0o644 lost on rewrite)

Parser (_apply_md_to_extract):
- _BULLET_RE accepts leading whitespace and arbitrary trailing text after id marker
- track ``` fence state at EOF — unclosed fence skips deletion (parallels the all-unknown-id guard)
- explicit pending_item reset for any non-bullet/non-continuation line — stray prose can't hijack waiver_reason / # evidence
- box transition [x]→[~] now clears stale evidence_of_satisfaction
- returns bool indicating mutation

validate.py:
- uses _apply_md_to_extract's bool return — no spurious spec-extract.json rewrites when nothing changed
- routes md re-render through atomic_write_text

scaffold.py:
- skill name extraction uses full slug between `skill.` prefix and `.scaffold` suffix (dotted segments preserved)
- error message maps required flags to their actual spec item ids (display_name → identity.pack_name, lang → identity.languages)

tests/conftest.py: importorskip yaml so missing PyYAML produces a clean skip instead of opaque subprocess failures.

SOP (references/spec-extraction.md): Output section now documents the `value` field for identity items. Trimmed prose across spec-extraction.md / discovery.md / testing.md (10 lines saved).

Tests: 59 → 69 (10 new regression tests).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(agent-studio): surface spec-doc entry path in first-run greeting

Opening question now offers three explicit paths: (a) chat through it,
(b) attach a spec/design/requirements doc to parse, or (c) resume an
existing pack. The spec-doc path was already supported by Studio's
detection logic but wasn't visible to creators until they spontaneously
pasted one.

* chore(agent-studio): bump to 1.4.0; untrack tests/ for client ship

- agent-pack.yaml: 1.3.4 → 1.4.0 (spec-driven build flow, PR #145)
- .gitignore: tests/, .pytest_cache/, __pycache__/, *.pyc
- untrack the 11 test files (kept on disk for dev; clients receive a
  test-free pack via release-agent-zips.yml)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore: re-track tests/ in repo; exclude from release zips

Reverses the tests/ untrack from ccf6997. Tests stay in git (CI + contributor
visibility); release-agent-zips.yml now produces zips without dev-only paths.

- .github/scripts/agent_release.py: replace shutil.make_archive with a
  filtered zipfile walk that skips tests/, __pycache__/, .pytest_cache/, *.pyc
  in both package-release and package-legacy-release.
- agent-studio/.gitignore: drop tests/, keep build-artifact patterns.
- agent-studio/.agents/skills/agent-studio/tests/: re-tracked (11 files).

Smoke: confirmed agent-studio-1.4.0.zip excludes tests/__pycache__/.pyc; spot
check across all 28 packs in the workspace shows none ship dev-only paths.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): drop scope-creep .gitignore patterns

Reverts .gitignore to its pre-PR state (just BOOTSTRAP.md.done). The
.pytest_cache/__pycache__/*.pyc patterns added in ccf6997 were never part
of this PR's scope — release-zip exclusion is now handled by agent_release.py.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Ning Hu <ning@gensmo.ai>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Makes Agent Studio's **spec-doc → agent build** flow explicit, surfaced, and gated:

- **Discoverable** — first-run greeting offers spec-doc upload as one of three explicit entry paths.
- **Structured** — spec is parsed into `data/spec-extract.json` (machine) + `data/spec-coverage.md` (human-editable), round-tripped deterministically.
- **Gated** — `validate.py` refuses Stage 4 if any spec item is unbuilt without a waiver.

When no spec is provided, all new code paths no-op — existing conversational discovery is unchanged.

Ships as `agent-studio` **v1.4.0**.

## What's new

- **`BOOTSTRAP.md` first-run greeting** — three explicit entry paths: (a) chat-through, (b) attach a spec/design/requirements doc, (c) resume an existing pack.
- **`references/spec-extraction.md`** — Studio's operating SOP for parsing a spec doc into `data/spec-extract.json` (Studio writes the JSON directly using its multimodal capabilities; no Python LLM-call layer).
- **`scripts/spec_coverage.py`** — deterministic round-trip between `data/spec-extract.json` (machine source of truth) and `data/spec-coverage.md` (human-editable checklist). Subcommands: `render`, `sync`. `sync --prune` required to delete items (silent deletion guard).
- **`scripts/_spec_schema.py`** — `SpecItem` + `SpecExtract` dataclasses with load/dump validation (9 item kinds, 2 tick kinds, 3 statuses). Atomic dump, multiline-title rejection, duplicate-id rejection.
- **`scripts/_spec_patterns.py`** — mechanical `satisfied_by` resolver supporting file paths, `yaml:<file>:<selector>`, `yaml:<...>==<value>` (with empty-RHS guard), `cron:<handler>`, `data_source:<name>`.
- **`scripts/validate.py --check-spec`** — auto-on when `data/spec-extract.json` exists. Walks the pack, auto-ticks mechanical items, demotes stale-evidence items, gates Stage 4 on remaining open items. Merges unsynced `data/spec-coverage.md` edits so creator-added waivers aren't clobbered.
- **`scripts/scaffold.py --from-spec`** — seeds identity + skill list + languages from the extract via the canonical `value` field; `--agent-name` is the only required override.
- **References wired in** — `discovery.md` branches into the SOP when a spec is detected; `skill-design.md` / `automation.md` instruct Studio to tick semantic items at stage gates; `testing.md` documents the gate behavior and creator exits (build / waive / drop); `SKILL.md` adds the two new truth sources.

## Hardening

Three rounds of adversarial review (Claude + Codex) addressed: silent data loss on unknown ids, stale-evidence persistence, `==no` boolean-vs-string ambiguity, demotion re-render, atomic md write, schema tightening, `--prune` required for deletions, unsynced-waiver preservation. See `76e5f72`, `93f0858`, `01b2264`, `5f53676`, `0ea517a`.

## Release packaging (affects all packs)

- **`.github/scripts/agent_release.py`** — replaced `shutil.make_archive` with a `zipfile`-based walk that skips `tests/`, `__pycache__/`, `.pytest_cache/`, and `*.pyc`. Applies to both `package-release` (the main release flow) and `package-legacy-release`. Tests stay in the repo (CI runs them, contributors can run them); client zips no longer carry dev-only paths.
- **`agent-studio/.gitignore`** — unchanged from main; exclusion is enforced at release time, not via gitignore.

## Test plan

- [x] **Automated** — 69 unit + integration tests via `cd agent-studio/.agents/skills/agent-studio && uv run --python 3.12 --with pytest --with pyyaml -m pytest tests/ -v`. Also confirmed clean run (9.2s, 69 passed) inside `ghcr.io/serendipityoneinc/openclaw-docker:2026.5.7`.
- [x] **End-to-end pipeline (in-container)** — scaffolded the nutrition-buddy fixture through `spec_coverage.py render` → `scaffold.py --from-spec` → `validate.py` (correctly reports `4/8 passed, 3 failed, 1 warnings` for a fresh scaffold; auto-ticks 2 mechanical items; flags 9 open items with actionable hints) → `package.py` produces `zip/nutrition-buddy-0.1.0.tar.gz` (843 B).
- [x] **Manual smoke (live openclaw gateway)** — agent-studio registered via `openclaw agents add agent-studio --workspace /workspace/agent-studio`; first-run greeting confirmed to surface the spec-doc entry path; gateway-driven scaffold from a real spec doc completed end-to-end.
- [x] **Release-zip smoke** — ran `agent_release.py package-release` and `package-legacy-release` locally; resulting `agent-studio-1.4.0.zip` (106 KB) contains no `tests/`, `__pycache__/`, `.pytest_cache/`, or `.pyc` entries. Spot-checked all 28 packs — none ship dev-only paths.

## Observed during smoke (separate PR)

When the creator uploads a `.docx` spec, Studio's model bypasses the ecap-skills `docx` skill (its SKILL.md description doesn't surface `read`/`analyze` — only `create`/`edit`/`fill`/`reformat`) and falls back to ad-hoc `pip install python-docx` + per-doc extraction scripts, which can time out on image-heavy decks. `xlsx` parses fine because its description leads with `read`. Fix is a one-line description tweak in `ecap-skills/docx/SKILL.md` — not in scope for this PR.

## Design docs

- Design spec: `~/Workspace/design-doc/2026-05-25-spec-driven-agent-build-design.md`
- Implementation plan: `~/Workspace/design-doc/2026-05-26-spec-driven-agent-build-plan.md`

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(pptx-master): apply 2.0.7-final build, rebrand SlideForge to PPT Master (#150)

- **SHA**: [34e7189b](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/34e7189ba5ee7f042d4f1286f1e2e584dc673a84)
- **作者**: vincent-srp
- **日期**: 2026-05-27T08:40:03Z
- **PR**: #150

### Commit Message

```
feat(pptx-master): apply 2.0.7-final build, rebrand SlideForge to PPT Master (#150)

Replace pptx-master pack contents with the finalized pptx_master-2.0.7-final build (21 files: output-html/pdf/pptx + ppt-beautify + onboarding skills, plus AGENTS/SOUL/IDENTITY/HEARTBEAT/BOOTSTRAP/routing/CHANGELOG/description). Version stays 2.0.7 (finalized re-build, not a bump).

Adopt the PPT Master display brand throughout (was SlideForge; 0 SlideForge refs remain). Preserve the deployment identity slug agentPack_id/name = pptx-master (hyphen) — the build shipped pptx_master (underscore), which would orphan the live OpenClaw deployment. Set agent-pack.yaml description to the English PPT Master bio (build shipped Chinese). Unify the two cosmetic pptx_master refs in tests/ to pptx-master.

Validation: test_pack.py 70/0, test_extra.py 36/0, validate_pdf_ratio.py --self-test passed.

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Replaces the `pptx-master` pack with the finalized `pptx_master-2.0.7-final` build, adopting the new **PPT Master** display brand while preserving the deployment identity. Version stays **2.0.7** — this is the finalized re-build, not a version bump (current `main` was already 2.0.7).

## Changes

- **Content/code refresh** (~15 files): `output-html`, `output-pdf`, `output-pptx`, `ppt-beautify`, `onboarding` skills + docs (`AGENTS`/`SOUL`/`IDENTITY`/`HEARTBEAT`/`BOOTSTRAP`/`routing`/`CHANGELOG`).
- **Rebrand SlideForge → PPT Master** (display fields only): `display_name`, `name`, `bio`, `short_bio`, `author`, and all in-pack copy. 0 SlideForge references remain.
- **Identity slug preserved**: `agent-pack.yaml name` + `description.json agentPack_id` kept as `pptx-master` (hyphen). The build shipped `pptx_master` (underscore), which would orphan the live OpenClaw deployment, so it was patched back. Dir name unchanged.
- **Description**: `agent-pack.yaml description` set to the English PPT Master bio sentence (build shipped Chinese).
- **tests/**: unified the two cosmetic `pptx_master` refs (docstring + README) to `pptx-master`.

## Validation

- `tests/test_pack.py`: **70 pass / 0 fail**
- `tests/test_extra.py`: **36 pass / 0 fail**
- `output-pdf/scripts/validate_pdf_ratio.py --self-test`: **passed**
- `package.py` invariant `agentPack_id == manifest name` holds (both `pptx-master`).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## feat(zoodance-vibe-drama): 扩充 BGM 曲库 + 新增 INDEX 索引 (#148)

- **SHA**: [3ecc06d5](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/3ecc06d57924690ed702bc5cfa520a68cdf40d6b)
- **作者**: david-srp
- **日期**: 2026-05-27T07:34:52Z
- **PR**: #148

### Commit Message

```
feat(zoodance-vibe-drama): 扩充 BGM 曲库 + 新增 INDEX 索引 (#148)

* feat(video-duplicate): upgrade to v1.9.2

主要变更：

- batch-runner: 新增 seal_seed.py 封印脚本，将 seed run 固化为
  seed_fingerprint.json（含 redraw prompt / Seedance prompt 分段
  / variant_axes 边界）；batch_run.tmpl.py 重构为 fingerprint 驱动
  （现场上传 R2 → 注册 BytePlus asset → 构建 plan），不再复制 seed 旧 plan
- storyboard-studio: pipeline 由 7 阶段扩展为 8 阶段，新增 Stage 2
  substitution_collect（暂停点，统一收集替换信息与参考图），后续阶段顺延
- storyboard-replicate: step_2 升级为 substitutions.json 持久化，
  接入 SUBS_TEMPLATE 与 refs/ 目录；Claude 模型升至 claude-sonnet-4-6
- style-duplicate: storyboard_gen_cli 改为四区布局（banner / 左:角色风格
  / 中:面板栅格 / 右:光影氛围+音频），与 Workflow C 对齐
- video-burn-subtitle: llm_segment 增加 fix_overlaps，杜绝相邻字幕时间重叠
- pack 元数据: 新增 HEARTBEAT.md / TOOLS.md / ZooClaw-Agent-Policy
  策略区块（cron 投递、安全、Skill 保密）；移除 BOOTSTRAP.md / docs/
  与已废弃的 pack-onboarding skill
- SOUL.md: 增加 User Context（餐饮探店运营，TikTok 投放）
- agent-pack.yaml: version 1.8.2 → 1.9.2，描述去中英混排

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(video-duplicate): restore pack-onboarding, remove leaked user preset from SOUL.md

- SOUL.md: 移除测试残留的 User Context 预设（餐饮探店运营 / TikTok），
  这是早期 onboarding 测试带进来的，不应固化为默认人设
- SOUL.md: persona 增强为"想象力丰富的内容营销 CMO + 技术 producer"，
  强调对平台调性、Hook、节奏的本能判断
- 恢复 .agents/skills/pack-onboarding/（1.9.2 tar 漏带），与其他 12 个
  pack 保持一致 — 首次使用 / data/config.json 缺失时仍走 onboarding

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(zoodance-vibe-drama): 扩充 BGM 曲库并新增 INDEX 索引

从飞书 wiki (Vibe Drama BGM) 提取 10 首新曲及说明，加入 BGM 音频库；
新增 assets/audio/INDEX.md 作为按曲目的结构化 YAML 索引（mood、乐器、
climax beat 时机、推荐剧种），并在 SKILL.md / delivery-and-mix-rules.md /
video_assembly.py 中引导先阅读该 INDEX。

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(zoodance-vibe-drama): 新增字幕烧录步骤（从 video-duplicate 迁移）

从 video-duplicate pack 迁移 video-transcribe + video-burn-subtitle 两个
skill，并声明 zooclaw-forcedalign 系统 skill；在 Phase 7 流程中插入
"字幕烧录"作为独立步骤，位于拼接和 BGM 之间——transcribe 必须跑在
BGM 混音之前，否则 BGM 会污染 ASR 准确度。

- agent-pack.yaml: 注册 3 个 skill；bins 补 ffmpeg/ffprobe/python3/curl/bash；版本 1.0.10 → 1.0.11
- vibe-drama/SKILL.md: Phase 7 流程改为 concat → (可选字幕烧录) → (可选 BGM) → delivery；Runtime delegation 新增 subtitle transcription / burn 两段
- delivery-and-mix-rules.md: assembly order 插入字幕步骤；新增 "Subtitle burn workflow" 章节
- video_assembly.py: docstring 说明字幕烧录是独立 skill，需在 concat 和 bgm 之间手动调用

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(zoodance-vibe-drama): 修复字幕烧录衔接缺陷

衔接审查发现的问题：
- video-transcribe.sh 默认从同级目录解析 zooclaw-forcedalign，但上一次
  迁移只在 agent-pack.yaml 里声明了，没复制实际 skill 文件夹，会触发
  "Error: zooclaw-forcedalign not found" → 补回 skill 整个目录
- SKILL.md Phase 7 step 4 没明确说不要用 video_assembly.py 的 pipeline
  快捷命令（它会跳过 burn 步骤）→ 改成显式调 duck + delivery
- 补充 zooclaw-forcedalign 的 200s/50MiB 硬上限说明（vibe-drama 单集
  ≤60s 安全，多集 concat 后再 burn 会超限）

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## 背景

本 PR 包含两块工作：
1. 从飞书 wiki [Vibe Drama BGM](https://starquest.feishu.cn/wiki/AFsfwtFoYi7ik8k4m0EcKDYbnGg) 同步 10 首专为短剧设计的新 BGM 到 `zoodance-vibe-drama` pack 的本地曲库，并新增结构化曲目索引，方便配乐时按 mood / 节奏 / climax 落点快速选曲。
2. 从 `video-duplicate` pack 迁移字幕烧录能力，在 Phase 7 流程中插入"字幕烧录"作为独立步骤，位于拼接和 BGM 之间。

---

## Part 1 · 扩充 BGM 曲库

### 1.1 新增 10 首 BGM 文件
位于 `zoodance-vibe-drama/.agents/skills/vibe-drama/assets/audio/`，文件名采用 `bgm-<title>-<style>-<duration>s.mp3` 约定：

| 曲目 | 风格 | 时长 |
|---|---|---|
| `bgm-phoenix-throne-epic-romance-180s.mp3` | 霸总逆袭甜宠（史诗版） | 180s |
| `bgm-stolen-glances-forbidden-love-87s.mp3` | 禁忌恋爱心跳 | 87s |
| `bgm-ancient-bloodline-dark-fantasy-152s.mp3` | 超自然霸总 / 血脉觉醒 | 152s |
| `bgm-cold-trail-suspense-thriller-114s.mp3` | 悬疑失踪 / true-crime | 114s |
| `bgm-twisted-lullaby-horror-ambient-143s.mp3` | 超自然恐怖 / jump-scare | 143s |
| `bgm-midnight-verdict-crime-noir-64s.mp3` | 犯罪悬疑反转 / neo-noir | 64s |
| `bgm-paws-pranks-pet-comedy-83s.mp3` | 拟人萌宠喜剧 | 83s |
| `bgm-boardroom-chaos-sitcom-73s.mp3` | 荒诞职场喜剧 | 73s |
| `bgm-boo-sweetheart-supernatural-romcom-55s.mp3` | 超自然爱情喜剧 | 55s |
| `bgm-mighty-misfit-comedy-adventure-145s.mp3` | 荒诞世界观喜剧 / 动画冒险 | 145s |

时长均由 `ffprobe` 实测并写入文件名。

### 1.2 更新 `references/audio-reference-library.md`
- BGM library 表格追加 10 行
- BGM routing by drama genre 表格追加 10 行新剧种 → 文件映射
- 顶部加链接指向新的 `INDEX.md`

### 1.3 新增 `assets/audio/INDEX.md`（per-track 结构化索引）
对**全部 19 首曲子**（含历史曲目）每首一个 YAML 块，字段包括：
- `file` / `title_cn|en` / `duration_s`
- `tempo`（slow / medium / fast）
- `mood`（标签数组）
- `instruments`（主导音色）
- `structure`（关键 beat 落点：climax / reveal / silence 的秒数）
- `best_for`（推荐剧种）
- `prompt_keywords`（Suno 再生关键词）
- `source`（local / artifacts）

按 Romance / Revenge / Ancient-Xianxia / Suspense / Horror / Comedy 分组，文末附 quick lookup tips（按 climax 时机、silence beat、短 loop、快节奏、fallback 选曲）。

### 1.4 引导阅读 INDEX 的入口
- `SKILL.md` Phase 7 选 BGM 行 + Runtime delegation 中 Assembly/BGM 段
- `references/delivery-and-mix-rules.md` 顶部 callout + BGM comparison workflow 第 1 步
- `scripts/video_assembly.py` 模块 docstring 新增 "BGM picking" 段落，提醒在传 `--bgm` 前先查 INDEX

---

## Part 2 · 迁移字幕烧录能力

### 2.1 从 video-duplicate 迁移 3 个 skill
- `.agents/skills/video-burn-subtitle/` — 字幕烧录主入口（burn.sh + llm_segment.py + srt_to_ass.py + 方正金陵字体）
- `.agents/skills/video-transcribe/` — 视频 → 词级 SRT
- `.agents/skills/zooclaw-forcedalign/` — 词级强制对齐（被 video-transcribe 依赖）

### 2.2 Phase 7 流程改造
```
concat → stitched.mp4
        ↓
   [可选] video-transcribe → words.srt
   [可选] video-burn-subtitle → stitched_subbed.mp4
        ↓
   [可选] BGM duck
        ↓
   delivery transcode
```

**关键约束**：字幕烧录**必须**跑在 BGM 之前，否则 BGM 会污染 ASR 准确度（video-duplicate 的 transcribe.sh 注释里管这个叫 "Option A preferred"）。

### 2.3 改了哪些文件
- `agent-pack.yaml` — 注册 3 个新 skill，bins 补齐（ffmpeg/ffprobe/python3/curl/bash），版本 1.0.10 → 1.0.11
- `vibe-drama/SKILL.md` — Reference 表 / What this skill owns / Runtime delegation / Phase 7 流程都更新
- `vibe-drama/references/delivery-and-mix-rules.md` — assembly order 插入字幕步骤，新增 Subtitle burn workflow 章节
- `vibe-drama/scripts/video_assembly.py` — docstring 提示字幕烧录是独立 skill，要在 concat 和 bgm 之间手动调

---

## Part 3 · 字幕衔接审查 + 修复（commit `3c48226`）

提交后做了一遍输入/输出全链路审查，发现并修复以下问题：

### 3.1 真实缺陷
- `video-transcribe/scripts/transcribe.sh:31` 默认从同级目录解析 `zooclaw-forcedalign`。上一次只在 `agent-pack.yaml` 里声明（`scripts: []`），但 skill 文件夹没复制 → 运行时会报 "Error: zooclaw-forcedalign not found at .agents/skills/zooclaw-forcedalign"。**已补齐整个 skill 目录**（SKILL.md + scripts/align.sh）。

### 3.2 文档清晰度
- Phase 7 step 4 原本只写 "Run BGM + delivery via `scripts/video_assembly.py`"，没禁用 `pipeline` 快捷命令——而 `pipeline` 会自动 concat → duck → delivery，**跳过 burn 步骤**。已改为显式调 `duck` + `delivery`，并在文档里明确警告"不要用 pipeline"。
- 没提 `zooclaw-forcedalign` 的 200s/50MiB 硬上限。vibe-drama 单集 ≤60s 安全，但多集 concat 后再 burn 会超限。已在 `delivery-and-mix-rules.md` 的 Subtitle burn workflow 章节补 "Hard limits" 子段说明。

### 3.3 全链路验证（确认 OK）
| 步骤 | 命令 | 输入 → 输出 | 关键 ffmpeg 行为 |
|---|---|---|---|
| 1. concat | `video_assembly.py concat` | beat1..4.mp4 → stitched.mp4 | `-c copy` 全 passthrough |
| 2a. transcribe | `transcribe.sh` | stitched.mp4 → words.srt | 默认 raw audio（pre-BGM 干净 VO） |
| 2b. burn | `burn.sh` | stitched.mp4 + words.srt → stitched_subbed.mp4 | `-c:a copy`，视频重编码烧字幕 |
| 3. duck | `video_assembly.py duck` | stitched_subbed.mp4 + bgm → with_bgm.mp4 | `-c:v copy`（字幕完好），音频 mix |
| 4. delivery | `video_assembly.py delivery` | with_bgm.mp4 → final.mp4 | H.264 重编码（像素字幕安全） |

3 条 skip path（纯 BGM / 纯字幕 / 都不要）的命名衔接也都对得上。

---

## Test plan
- [ ] 在 zoodance-vibe-drama pack 真实跑一集，验证 BGM 选曲流程会先打开 INDEX.md
- [ ] 抽查 1 首新曲过 `scripts/video_assembly.py duck` 验证 ducking mix 正常
- [ ] 在 60s 单集上跑完整 concat → transcribe → burn → duck → delivery 链路，确认字幕烧录效果与 BGM 不冲突
- [ ] 确认 `audio-reference-library.md` 路由表里所有新文件名拼写与文件系统一致

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

