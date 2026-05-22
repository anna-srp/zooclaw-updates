# ecap-agent-pack Commits — 2026-05-21

## bb182e8c — feat(pptx-master): refresh SlideForge 1.0.0 with English-optimized build (#139)

- **Author**: vincent-srp
- **Date**: 2026-05-21T11:14:57Z

### Full Commit Message

```
feat(pptx-master): refresh SlideForge 1.0.0 with English-optimized build (#139)

Applies the 5/20 English-optimized SlideForge build (build/线上包518slideforge-1.0.0_英文优化版.zip)
over pptx-master/. Same v1.0.0, same skill tree — the refresh is content-only:
- AGENTS.md / SOUL.md and SKILL.md files under ppt-beautify, output-html,
  output-pptx, output-pdf, output-image, brand-system, onboarding rewritten
  to English copy; output-html adds §7B PPTX-Ready toolbar + fonts.css.
- description.json refreshed (English bio/skills, animal Owl→Peacock,
  category enterprise-productivity).
- avatar.png replaced with the new 1254×1254 asset.

Preserved (would have been clobbered by the new zip):
- agent-pack.yaml — new zip ships a 32-byte stub (name + version only); kept
  the curated 6884-byte manifest with full persona / skills / dependencies
  metadata. Same precedent as 9e312b8 for video-duplicate 1.8.0.
- description.json#agentPack_id — kept as "pptx-master" (not the new
  "slideforge") so the existing catalog row, use cases, and bookmarks keep
  resolving. agent_id is the upsert key in claw-interface
  (agent_catalog_repo.py); renaming would orphan use cases and split the
  catalog into two rows.

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

- Applies the 5/20 English-optimized SlideForge build (`build/线上包518slideforge-1.0.0_英文优化版.zip`) over `pptx-master/`. Same v1.0.0, same skill tree — content-only refresh of `AGENTS.md` / `SOUL.md` / SKILL files under `ppt-beautify`, `output-*`, `brand-system`, `onboarding`, plus a new 1254×1254 `avatar.png` and refreshed `description.json` (English bio, animal Owl→Peacock, category `enterprise-productivity`).
- **Preserved `agent-pack.yaml`**: the new zip ships a 32-byte stub (`name` + `version` only); kept the curated 6884-byte manifest with full persona / skills / dependencies metadata. Same precedent as 9e312b8 (video-duplicate 1.8.0 fix).
- **Preserved `description.json#agentPack_id` as `pptx-master`** (not the new `slideforge`). `agent_id` is the upsert primary key in `claw-interface` (`agent_catalog_repo.py`); renaming would orphan existing use cases, break bookmarks/share URLs, and split the catalog into two rows. Rename should be a separate copy + soft-delete migration, not a description.json edit.

## Test plan

- [ ] Diff against `main` shows only `pptx-master/` files (27 modified, ~4.5k ins / ~3.7k del), no `agent-pack.yaml` change
- [ ] `agentPack_id` in `pptx-master/description.json` is `pptx-master`
- [ ] Avatar renders at the new 1254×1254 resolution
- [ ] OpenClaw pod loads the pack with the preserved rich `agent-pack.yaml`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 1cd2d492 — fix(agent-studio): forbid silent rm; require approval for plain rm (#138)

- **Author**: felix-srp
- **Date**: 2026-05-21T06:04:17Z

### Full Commit Message

```
fix(agent-studio): forbid silent rm; require approval for plain rm (#138)

* fix(agent-studio): forbid silent rm; require approval for plain rm

A Studio session unilaterally ran `rm -f ~/.openclaw/workspace-<pack>/zip/*.tar.gz`
on a customer pod, wiping every pack's archives. workspace-<pack> paths on the
pod are symlinks that all resolve to one physical workspace, so the "narrow"
glob was a global delete.

Root cause: packaging.md §5c said "Remove tmp/ and artifacts/ from prior test
runs" — a direct cleanup imperative. The LLM pattern-matched it into a broader
"clear old archives" sweep. No `rm` policy existed anywhere the model reads.

- SKILL.md § Rules: `rm -f` / `rm -rf` forbidden outright; plain `rm` requires
  explicit per-path creator approval before execution; call out the workspace-<pack>
  symlink topology so the model sees the blast radius.
- packaging.md §5c: drop the "remove tmp/ and artifacts/" trigger. artifacts/
  actually ships (avatar lives there); tmp/ is auto-excluded by package.py.
  Point to § Rules for the deletion policy.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* simplify(agent-studio): tighten convention phrasing + drop 2 narrative lines

After successive rounds of "is this really redundant?" challenges,
keeping only changes that touch pure narration (meta-text about the
section itself) or have equivalent semantic compression:

- SKILL.md: tighten `<skill_root>` convention phrasing (same denotation);
  drop §Stages subtitle "— one line each; details in references" (pure
  meta-narration; the bullets that follow demonstrate the structure).
- automation.md: collapse "Pack doesn't configure that." into a
  parenthetical on the same sentence (semantically equivalent);
  drop "- Cron already added in step 6 via add_cron.py" from Init
  phase (Codex-validated: Init bullets don't list cron at all, so
  the "already done" reassurance is moot).

Explicitly NOT trimmed (load-bearing on review):
- skill-design.md "Goal:" line — content overlaps Process rules but
  serves an intent-framing function rules can't replace.
- skill-design.md "## For each new skill — all steps in order"
  heading — distinguishes "new" path from the "Uploading existing
  skills" section above; "all" + "in order" emphasize completeness
  and sequence beyond what numbered subsections (2a..2i) alone signal.

2 files, -3/+2 lines. No instructions, paths, commands, or
intent-framing touched.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(agent-studio): bump version 1.3.2 → 1.3.3

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

### 1. Forbid silent `rm` (commit `7de34ac`)

A Studio session unilaterally ran `rm -f ~/.openclaw/workspace-<pack>/zip/*.tar.gz` on a customer pod, wiping every pack's archives. `workspace-<pack>` paths are symlinks resolving to one physical workspace, so the "narrow" glob was a global delete. The model invented the cleanup; nothing in the pack had stopped it.

**Root cause:** `references/packaging.md` §5c said `Remove tmp/ and artifacts/ from prior test runs` — a direct cleanup imperative the LLM pattern-matched into a broader sweep. No `rm` policy existed anywhere the model reads.

**Fix:**
- `SKILL.md` § Rules — `rm -f` / `rm -rf` forbidden outright; plain `rm` requires explicit per-path creator approval before execution. Calls out the workspace-`<pack>` symlink topology so the blast radius is visible.
- `references/packaging.md` §5c — drop the `Remove tmp/ and artifacts/` trigger. `artifacts/` actually ships (avatar lives there); `tmp/` is already auto-excluded by `package.py`. Point back to § Rules for the deletion policy.

### 2. Tighten 2 narrative lines (commit `ea7e0ff`)

Pure-narration / equivalent-compression edits picked up along the way:
- `SKILL.md`: tighten `<skill_root>` convention phrasing (same denotation); drop §Stages subtitle `— one line each; details in references` (meta-narration; the bullets demonstrate the structure).
- `automation.md`: collapse `Pack doesn't configure that.` into a parenthetical; drop `- Cron already added in step 6 via add_cron.py` from Init phase (the Init bullets don't list cron at all, so the "already done" reassurance is moot).

2 files, −3/+2 lines. No instructions, paths, commands, intent-framing, or cross-references touched.

## Test plan

- [ ] Read `SKILL.md` § Rules end-to-end — new `rm` bullet reads naturally next to surrounding rules.
- [ ] Read `packaging.md` §5c — no longer reads as "delete dirs before packaging".
- [ ] In a fresh Studio session, publish a pack and confirm the agent does not propose `rm` of `tmp/` / `artifacts/`.
- [ ] If a session does propose `rm`, confirm it (a) uses plain `rm`, not `-f` / `-rf`, and (b) ASKs with absolute paths before running.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 760639d9 — feat(video-duplicate): upgrade to v1.8.2 (#137)

- **Author**: david-srp
- **Date**: 2026-05-21T02:53:16Z

### Full Commit Message

```
feat(video-duplicate): upgrade to v1.8.2 (#137)

* feat(video-duplicate): upgrade to v1.8.2

Bump pack to 1.8.2 with batch-runner promotion, cleaner post-production
pipeline, and packaging cleanup found during the 1.8.2 scan.

- batch-runner: ship quality_check.py + report_gen.py and the two
  init/batch templates so the framework is callable directly instead
  of being a docs-only skill
- video-editor: drop the retired forced-align/caption.sh,
  forced-align/postprocess.py, and subtitle_burn.py.deprecated; the
  yaml now points at concat.py / demucs_bgm.py / audio_postprocess.py,
  matching the script routing in AGENTS.md
- seedance-runner: surface validate_plan.py in agent-pack.yaml
- description.json: replace TODO placeholders with the real animal
  (Chameleon), category, role, bio, skills list, integrations
- IDENTITY.md / description.json: align avatar path to
  artifacts/avatar.png and ship the file with the pack
- AGENTS.md: release checklist now reflects that docs/ is local-only
  (gitignored at repo root) and updates the tarball exclude list
- Add BOOTSTRAP.md so the pack matches the convention used by
  amazon-analyst / agent-studio / creator-ops

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(video-duplicate): use NamedTemporaryFile for Demucs wav extraction (CWE-377)

CodeQL alerts #52 and #53 flagged tempfile.mktemp() in the Demucs BGM
extraction path (demucs_bgm.py and concat.py inline fallback).
tempfile.mktemp() returns a path without creating the file, leaving a
race window where an attacker on shared /tmp could pre-create the file
or a symlink between the path being returned and ffmpeg opening it.

Switch both call sites to tempfile.NamedTemporaryFile(delete=False),
which creates the file atomically with O_EXCL; we close the handle
immediately so ffmpeg can write to the same path. Cleanup with
os.unlink at the end of the block is unchanged.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

# Video Duplicate 大升级（v1.6.4 → v1.8.2）

一句话：**从「单条复刻」升级为「批量复刻 + 全流程可控」**，并把视频理解、画面控制、声音处理三个核心模块全部打磨过一遍。

---

## 🎯 用户能感受到的新能力

### 1. 一键批量出变体（v1.8.2 全新）
跑通第一条复刻后，告诉 Agent："换 5 个人物 / 改 10 套台词 / 出 20 条变体"——
- 自动按指定维度（人物图、台词、场景词）排列组合
- 串行执行，每条完成自动打分（水印 / 字幕残留 / 黑帧 / 画面畸变都查一遍）
- 全部跑完出一份 HTML 报告：每条带视频播放器 + 故事板缩略图 + 评分排序

适合：电商投流测多版本素材、达人合作多人物口播、跨平台分发多文案。

### 2. AI 编导更「懂戏」了（v1.7.x）
之前 AI 只看画面，现在它同时拆解：
- **镜头语言**：慢推 vs 手持晃、逐格 vs 丝滑过渡
- **剪辑节奏**：3 秒一切的奢侈感 vs 1 秒一切的爆点节奏
- **情绪弧线**：从平静到揭秘的张力曲线
- **声音签名**：稀疏钢琴 vs 鼓点 vs 纯人声
- **叙事结构**：哪段是钩子、哪段是 CTA

结果：AI 重生成时不再「画面对了但味儿不对」，整片基调能跟原片对齐。

### 3. 三种工作流共用同一个「读片大脑」（v1.7.2）
以前三个工作流各读各的，理解不一致。现在统一入口：
- 用户上传视频，Gemini 3.1 Pro **只读一遍**就拆出 20+ 维度的分析数据
- 三种工作流共享这份数据，**节省一半分析时间**，结论一致
- 视频按「叙事呼吸点」自然切分（≤14 秒/段），不再机械均切

### 4. 声音体系大改造（v1.8.0）
- **声音风格可控**：除台词外，可指定声音性别 / 年龄感 / 语速 / 语气
- **逐句时间戳**：每句什么时候出现、多长停顿，全部精确控制
- **BGM 分离与重混**：自动从原片抽出纯背景音乐（人声去掉），混到新视频里——响度按 -14 LUFS 行业标准归一

### 5. 字幕系统全自动化
- **字幕擦除**：Seedance 输出有乱码硬字幕？说一句「擦掉字幕」即可（v1.8.2 鉴权修复后稳定可用）
- **字幕烧录**：词级时间戳对齐、方正金陵字体、双层阴影，全自动产出

---

## 🛡 稳定性 / 可靠性提升

| 之前的坑 | 现在 |
|---|---|
| BytePlus 视频拼接后变 30 分钟黑屏 | DTS 自动归一化，拼接稳定 |
| BGM 分离偶尔静默跳过 | 三级路径回退 + Demucs 独立脚本，必跑 |
| 字幕擦除任务查询 403 失败 | 复用已验证的鉴权链路，一次成功 |
| 断点续跑重复消耗 GPT 调用 | 各阶段产物幂等跳过，省钱省时 |
| 字幕烧录耗时长会超时 | 超时阈值 30s → 90s，不再卡死 |

---

## 📈 版本节奏

| 版本 | 主题 | 核心收益 |
|---|---|---|
| **v1.8.2**（本 PR） | 批量框架固化 + 报告升级 | 一键批量出变体 + HTML 可视化报告 |
| v1.8.0 | 音视频后处理加固 | 声音风格可控 + BGM 处理稳定 |
| v1.7.2 | 三流统一分析入口 | 节省分析时间、风格一致 |
| v1.7.1 | 信息流增强 | AI 真正「看懂」镜头语言和情绪弧 |
| v1.7.0 | 公共分析模块上线 | Gemini 字段从 12 个扩展到 20+ |
| v1.6.4 | 首个公开版本 | 三种工作流 A/B/C 全可用 |

---

## 🔧 本 PR 的工程改动（v1.7.2 → v1.8.2）

- **batch-runner**：从「方法论文档」升级为「可调用框架」——`quality_check.py` + `report_gen.py` + 两份 `*.tmpl.py` 项目实例化模板
- **video-editor**：删除已废弃的 `forced-align/caption.sh`、`forced-align/postprocess.py`、`subtitle_burn.py.deprecated`；yaml 对齐到实际在用的 `concat.py` / `demucs_bgm.py` / `audio_postprocess.py`
- **seedance-runner**：`validate_plan.py` 加入 yaml 声明
- **description.json**：从全 TODO 占位符重写为完整人工版本（animal=Chameleon、productivity、8 项 skills 清单、6 项 integrations）
- **avatar 路径**：`IDENTITY.md` 与 `description.json` 统一指向 `artifacts/avatar.png`，文件随包分发
- **AGENTS.md 发版规范**：明确 `docs/` 为本地开发参考（被仓库 `.gitignore` 排除），更新打包 exclude 列表
- **BOOTSTRAP.md**：对齐 amazon-analyst / agent-studio / creator-ops 的 pack 标准结构

## ✅ Test plan

- [ ] `agent-pack.yaml` `version: 1.8.2`，所有 `scripts:` 条目在磁盘上能找到
- [ ] `description.json` 无残留 `TODO:` 字串；`avatar_url` 与 `IDENTITY.md` 都指向 `artifacts/avatar.png` 且文件存在
- [ ] 已废弃脚本物理删除：`video-editor/scripts/forced-align/`、`subtitle_burn.py.deprecated`
- [ ] `batch-runner/scripts/` + `batch-runner/templates/` 完整
- [ ] OpenClaw bot pod 加载干净（手动 smoke：`/studio install`）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
