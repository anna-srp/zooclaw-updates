---
title: "Video Duplicate Agent 升级 v1.7.2：AI 视频理解能力大幅提升"
type: "Agent 上架/更新"
priority: "高"
date: "2026-05-19"
status: "待审核"
channels: ""
---
# Video Duplicate Agent 升级 v1.7.2：AI 视频理解能力大幅提升

## 核心宣传点
Video Duplicate 从"知道画面在哪里切"进化为"像导演一样理解整部片子"——视频分析维度从12个扩展到20+个，生成视频的人物动作、镜头运动和情绪氛围更自然、更贴近原片。

## 原始内容
```
commit: e808613422af2279aba169e9d9753e5830111b46
repo: SerendipityOneInc/ecap-agent-pack
author: vincent-srp
date: 2026-05-19T11:13:31Z

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

--- PR #134 Body ---
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
```
