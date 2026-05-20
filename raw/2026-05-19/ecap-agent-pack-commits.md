# SerendipityOneInc/ecap-agent-pack - Commits on 2026-05-19

## [3b9362f6] fix(agent-studio): surface --archive flag in share + pack/command hints at session start (#133)
- **SHA:** 3b9362f61f320ac044e873911c87ef40b97b4661
- **Author:** felix-srp
- **Date:** 2026-05-19T17:47:48Z

### Full Commit Message
```
fix(agent-studio): surface --archive flag in share + pack/command hints at session start (#133)

* fix(agent-studio): surface --archive flag in share + pack/command hints at session start

- agent-studio-share/SKILL.md: document the existing `--archive <path>` flag so
  creators can share a pre-packed `.tar.gz` without repackaging the current
  workspace. The Python already supported it; SKILL.md was hiding it from agents.
- AGENTS.md: add a one-line orientation on first DEV reply (active pack name +
  `/studio` prefix reminder) so creators stop typing `/new` instead of
  `/studio new` and always know which pack the workspace is editing.
- Bump version 1.3.0 → 1.3.1.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): trim tokens in share SKILL.md + AGENTS.md THIRD step

Tighten the prose added in the previous commit. No behavioral change.

- agent-studio-share/SKILL.md: collapse the `--archive` bullet (was ~70 words,
  now ~20) — drop where-to-find-archives illustration and the "package.py
  skipped" sentence (already covered in Internal behavior). Shorten
  `--artifacts-base-url` to `<url>` placeholder. Trim "that path … no
  packaging step" → "directly, no packaging".
- AGENTS.md: trim THIRD step ~30 tokens — drop "mode" / "of session"
  (parallel with FIRST/SECOND), drop "(the name: from agent/agent-pack.yaml)"
  (already read in SECOND), drop ", not /new" (positive example suffices),
  make skip-condition mechanically checkable ("starts with /studio").

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(agent-studio): tighten --archive fallback note + THIRD-step scope

Address review feedback on PR #133:
- SKILL.md: disclose the unversioned-filename fallback for --archive
  (version="unknown") so the documented identity contract matches
  run_share.py's actual parsing behavior.
- AGENTS.md THIRD step: state DEV-only / once-per-session scope and
  explicit TEST = no orientation, removing ambiguity around when the
  one-line orientation fires.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Ning Hu <ning@gensmo.ai>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #133 Body
## Summary

Two small docs/SOP fixes for Agent Studio v1.3.1, motivated by friction seen with real creators.

- **`/studio share --archive <path>` is now reachable.** `run_share.py` already supported the flag (validates and stages a pre-packed `.tar.gz` without invoking `package.py`), but `agent-studio-share/SKILL.md` never told the agent it existed — so the share flow was locked to "repackage the current workspace" with no way to share a foreign archive. SKILL.md now documents the flag, the no-repackage path, and that an unversioned filename falls back to `version="unknown"` (mirrors `run_share.py`'s actual parsing).
- **Session-start orientation in DEV mode.** AGENTS.md now asks the agent to lead its first reply of a DEV session with a one-line orientation: which pack is active (`name:` from `agent/agent-pack.yaml`) and that creator commands use the `/studio` prefix (e.g. `/studio new`, not `/new`). Scope is explicit: DEV only, once per session, skipped when the user's first message already starts with `/studio`, and silent in TEST so the pack-agent persona is preserved.
- Version bump `1.3.0 → 1.3.1`.

No Python changes.

## Test plan

Verified in a sibling openclaw-docker container (`ghcr.io/serendipityoneinc/openclaw-docker:2026.5.7`) on the patched workspace.

Script-level (run via `uv run --python 3.12 .agents/skills/agent-studio-share/scripts/run_share.py`):

- [x] No `--archive`, no existing `zip/<pack>-<version>.tar.gz` → calls `package.py`; `archive_reused=false`, archive built and staged into `artifacts/shares/`.
- [x] No `--archive`, matching zip already in `zip/` → reuse path; `archive_reused=true`, `package.py` not invoked.
- [x] `--archive zip/imported-pack-2.0.5.tar.gz` → skips `package.py`; `pack_name=imported-pack`, `version=2.0.5` parsed from filename even though the workspace manifest says otherwise (workspace manifest correctly ignored).
- [x] `--archive zip/myarchive.tar.gz` (no version segment) → succeeds with `pack_name=myarchive`, `version="unknown"` (documented fallback).

LLM-level (manual webchat session against the deployed pack):

- [x] DEV first session, neutral message → first reply names the active pack and mentions the `/studio` prefix.
- [x] DEV first message is itself `/studio …` → orientation line skipped, command handled directly.
- [x] TEST mode first reply → pack-agent persona, no orientation line.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [e8086134] feat(video-duplicate): upgrade to v1.7.2 (#134)
- **SHA:** e808613422af2279aba169e9d9753e5830111b46
- **Author:** vincent-srp
- **Date:** 2026-05-19T11:13:31Z

### Full Commit Message
```
feat(video-duplicate): upgrade to v1.7.2 (#134)

Adds shared video-analyze skill (Gemini 3.1 Pro pre-processing) and
migrates Workflows A/B/C to consume the unified video_analysis.json
schema. Workflow C is now flagged as ⭐ recommended; Workflow A switches
to per-scene frame_time + global_style anchors; Workflow B prompt
composer adopts the new lighting / spatial_layers / emotional_arc
fields with old-key fallbacks. Description.json version aligned with
agent-pack.yaml (the build tarball shipped 1.6.3, fixed to 1.7.2).

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #134 Body
## 一句话总结

v1.6.4 时 Gemini 只能告诉 AI"画面在哪里切"；v1.7.2 之后，Gemini 像导演一样读懂整部片子的气质、节奏、情绪和运镜意图，再用这份"导演意图说明书"指挥每一帧的重新生成。三条工作流（A/B/C）全部统一走同一个分析入口。

---

## 🎯 用户视角的核心升级（v1.6.4 → v1.7.2）

### 视频理解从 12 字段 → 20+ 字段

| 新增理解维度 | 用户感知到的差异 |
|---|---|
| **主体运动弧线** (`action.subject_motion`) | 生成视频里人不再是站着不动的塑料人 |
| **镜头运动意图** (`camera.motion` / `lens_feel`) | 复刻镜头语言更贴近原片（推/拉/跟，光学质感） |
| **情绪弧线** (`emotional_arc`) | 每个镜头有"戏剧张力"，不是平白画面 |
| **空间层次** (`spatial_layers`) | 画面有纵深感，前中后景关系清楚 |
| **音画同步点** (`audio_sync`) | 生成视频的动作与音频节奏咬合 |
| **全局风格签名** (`global_style.*`) | 跨片段视觉风格统一，不再跳帧 |
| **叙事结构** (`narrative_structure.hook/arc/cta`) | 换台词后叙事节奏保留，钩子还在张力 |
| **微表情** (`action.micro_expression`) | 不再"蜡像脸"，眼神/呼吸/嘴角都有 |

### 三条工作流的具体改善

**Workflow A — 分镜重绘（storyboard-studio）**
- gpt-image-2 重绘时拿到"全片色调锚点 + 人物外貌锚点"：同一个人在第 1 段和第 5 段看起来是同一个个体
- `visual_static`（Gemini 专为图像模型写的冻帧描述）以前白白产出从未使用，现在作为每个 panel 的主描述
- Seedance 生成时显式传镜头运动指令，告别"PPT 静止帧感"

**Workflow B — 风格迁移（style-duplicate）**
- Claude 现在有 7 条 GLOBAL CONTEXT RULES 作为硬约束（不是参考数据），替换内容时不会自由发挥破坏原片节奏
- 把全局风格从 JSON blob 改成具名标签块（`CAMERA SIGNATURE:` 触发约束模式，而 `"camera_signature": "..."` 只触发数据模式）
- VO 替换保留叙事功能：hook chunk 仍然有张力开场，cta chunk 仍然有行动力收场
- 修复 9 处字段名断裂（旧代码读不到新 schema 的值）

**Workflow C — 故事板复刻 ⭐ 推荐（storyboard-replicate）**
- 故事板 prompt 从"手工填模板"升级为"从 video_analysis.json 自动组装"——质量稳定，agent 仍可审阅/编辑
- Seedance chunk prompt 改成结构化标签：每个 scene 显式带运动/情绪/镜头意图
- Chunk 切分从"暴力均分"升级为"Gemini 叙事切分"（≤14s/块，切点在 VO 呼吸点）

### 架构层面：三条路径合一

```
旧（v1.6.4）：A/B/C 各自有自己的 Gemini 分析脚本，schema 各异
新（v1.7.2）：video-analyze（唯一 Gemini 入口）
                ↓ video_analysis.json
                ├── A：frame_time 提帧 → panel redraw → Seedance
                ├── B：全量字段 → Claude prompt 合成 → Seedance
                └── C：chunks[] 叙事切分 → 故事板 → Seedance
```

---

## 🐛 Bug 修复

- **珠宝引用遗漏**：项链/戒指的参考图现在自动注入到所有有人物的镜头，不再依赖 Gemini 关键词覆盖率
- **字幕流程统一**：三条 workflow 全部走 `transcribe → burn` 新路径，废弃 `subtitle_burn.py`（已 `.deprecated`）
- **台词时间戳**：兼容新旧两套数据格式（`chunks[].voiceover[]` ↔ `captions[]`），旧数据不丢字幕
- **Stage 3 模型**：`gpt-4o` → `claude-sonnet-4-6`（ZooClaw 环境内可用）
- **description.json 版本漂移**：tar 包内为 `1.6.3`，已手动对齐为 `1.7.2`（匹配 agent-pack.yaml）

---

## 📋 本次改动的代码层清单

**新增 skill**
- `.agents/skills/video-analyze/` — 唯一的 Gemini 视频分析入口
  - `SKILL.md`、`scripts/analyze_cli.py`（426 行）

**Workflow 脚本更新**
- `storyboard-studio/scripts/run_pipeline.py` — Stage 1 迁移到 `video-analyze`，fallback 保留
- `storyboard-replicate/scripts/run_pipeline.py` — Step 1 迁移到 `video-analyze`，叙事切分驱动 Step 5；新增 `_auto_build_storyboard_prompt()` 和 `_auto_build_chunk_prompts()`
- `style-duplicate/scripts/run_pipeline.py` — 9 处字段名断裂修复，新字段注入 shot 块
- `style-duplicate/scripts/prompt_composer_cli.py` — SYSTEM_PROMPT 加入 7 条 GLOBAL CONTEXT RULES，locked 块加入 lighting / spatial_layers / emotional_arc / vfx_and_grade
- `style-duplicate/scripts/style_analyze_cli.py` — 字段扩展
- `seedance-runner/scripts/run_chunks.py` — 小幅更新

**Manifest & docs**
- `agent-pack.yaml` — 注册 `video-analyze`、`style-duplicate`、`storyboard-replicate`；版本 1.6.4 → 1.7.2
- `description.json` — 版本对齐到 1.7.2
- `style-duplicate/SKILL.md` — 新增 Prompt Architecture Best Practices 章节
- `AGENTS.md` — Workflow A/C 描述、Step 5 工作流说明、路由表全部更新

**Diff 规模**：12 files, +1982 / −183

---

## ⚠️ Reviewer Notes

- Build tarball (`build/video-duplicate-1.7.2.tar.gz`) 内夹带了 `__pycache__/`、`artifacts/shares/`、`zip/video-duplicate-1.6.1.tar.gz`、`docs/v165-todo.md` 这些本地构建产物——**均未入提交**，只 ship 了 cleaned payload
- `docs/CHANGELOG.md` 被仓库 `.gitignore`（`docs/` 规则）排除，本次 v1.7.2 changelog 仅在本地工作树。如果想让 changelog 入库，需要单独调整 .gitignore
- `description.json` 上游 tar 写的是 `1.6.3`，本次修正为 `1.7.2`——package.py 只校验 `agentPack_id` 不校验 version，所以这是体面问题不是阻塞问题，但建议上游打包脚本同步修复

---

## ✅ Test plan

- [ ] Pack loader 读到 v1.7.2 manifest（agent-pack.yaml 与 description.json 版本一致）
- [ ] 11 个 skill 全部解析成功：`pack-onboarding`、`prepare-source`、`seedance-runner`、`storyboard-replicate`、`storyboard-studio`、`style-duplicate`、`video-analyze`、`video-burn-subtitle`、`video-editor`、`video-transcribe`、`zooclaw-forcedalign`
- [ ] Workflow C 端到端冒烟跑通（analyze → storyboard → seedance → editor）
- [ ] Workflow B 走新 schema 路径（验证 `lighting` / `spatial_layers` / `emotional_arc` 真的到了 Seedance prompt）
- [ ] Workflow A 走 `video-analyze` 路径（验证 `video_analysis.json` 生成；fallback 路径不被触发）
- [ ] 字幕烧录走 `transcribe.sh` → `burn.sh` 新路径（无 `subtitle_burn.py` 调用）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [7ccf7f66] feat(video-duplicate): add Video Duplicate pack v1.6.4 (#132)
- **SHA:** 7ccf7f66062b105719c0f315bc3948908133b54e
- **Author:** vincent-srp
- **Date:** 2026-05-19T04:51:28Z

### Full Commit Message
```
feat(video-duplicate): add Video Duplicate pack v1.6.4 (#132)
```

### PR #132 Body
## Summary
- Add new pack `video-duplicate/` (agentPack_id: `video-duplicate`) from `build/video-duplicate-1.6.4.tar.gz`
- This is a separate pack from the existing `video-ads-duplicate/` (different agentPack_id `video_ads_duplicate`), so both coexist
- Fix `description.json` version field (upstream build left it at `1.6.3`; now synced to `1.6.4` to match `agent-pack.yaml` and CHANGELOG)

## Pack overview
- Role: 分镜复刻·剪辑编导大师 (AI Short-Video Replication Director)
- Three workflows: Workflow C (storyboard-guided, recommended) / A (frame-precise) / B (style transfer)
- Stack: Gemini 3.1 Pro · gpt-image-2 · Seedance 2.0 Pro · Demucs · ffmpeg

## Notes
- Upstream 1.6.4 fix vs 1.6.3: removed broken `subtitle_burn.py` reference in `agent-pack.yaml`, migrated 3 pipelines to `transcribe.sh` + `burn.sh`, dropped bundled 1.6.1 tarball leftovers (`artifacts/`, `zip/`)
- `subtitle_burn.py.deprecated` is still shipped in the tarball as dead weight (no longer referenced by yaml); not blocking — flag for upstream build cleanup

## Test plan
- [ ] Verify pack loads at runtime in an OpenClaw bot pod
- [ ] Smoke-test Workflow C (storyboard-guided) end-to-end
- [ ] Confirm `video-ads-duplicate` pack remains unaffected

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
