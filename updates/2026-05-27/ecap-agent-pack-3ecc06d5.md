---
title: "ZooDance Vibe Drama：新增 10 首短剧专属 BGM"
type: "Agent 上架/更新"
priority: "中"
date: "2026-05-27"
status: "待审核"
channels: ""
---

# ZooDance Vibe Drama：新增 10 首短剧专属 BGM

## 核心宣传点

ZooDance Vibe Drama Agent 曲库新增 10 首专为短剧场景设计的 BGM，按情绪/节奏/高潮点分类索引，配乐选择更精准。

## 原始内容

**仓库**: SerendipityOneInc/ecap-agent-pack  
**SHA**: [3ecc06d5](https://github.com/SerendipityOneInc/ecap-agent-pack/commit/3ecc06d57924690ed702bc5cfa520a68cdf40d6b)
**PR**: [#148](https://github.com/SerendipityOneInc/ecap-agent-pack/pull/148)  
**作者**: david-srp  
**日期**: 2026-05-27T07:34:52Z

**Commit Message:**

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


**PR Description:**

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
