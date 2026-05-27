---
title: "Video Duplicate Agent 升级至 v1.9.2"
type: "Agent 上架/更新"
priority: "高"
date: "2026-05-26"
status: "待审核"
channels: "站内弹窗 + 社媒素材 + Use Case + Discord + changelog + KOL + EDM"
---
# Video Duplicate Agent 升级至 v1.9.2

## 核心宣传点

Video Duplicate Agent 大版本升级，批量视频处理引入指纹驱动机制，故事板流程新增替换暂停阶段，生产稳定性和可控性显著提升。

## 原始内容

**Commit:** 72db5005
**Repo:** ecap-agent-pack
**Author:** david-srp

**Commit Message:**
```
feat(video-duplicate): upgrade to v1.9.2 (#146)

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

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR #146: feat(video-duplicate): upgrade to v1.9.2**

## Summary

Video Duplicate pack 升级 1.8.2 → 1.9.2，核心是 **batch-runner 重构为 fingerprint 驱动** 与 **storyboard 流程统一引入 substitution 暂停阶段**。

## 主要变更

### 🔧 batch-runner：seed run 固化机制
- **新增 `scripts/seal_seed.py`**：批量执行前对 seed run 做一次性"封印"，输出 `seed_fingerprint.json`，包含：
  - `redraw.per_chunk[i].prompt` —— 实际发送的重绘指令
  - `redraw.per_chunk[i].images` —— panel + elements + substitution_refs 完整列表
  - `seedance.per_chunk[i].prompt_fixed` / `prompt_vo_block` —— 镜头语言锁定 + VO 可替换段
  - `variant_axes` —— cast / voiceover 替换字段边界
- **`batch_run.tmpl.py` 重构**：批量阶段不再复制 seed 的旧 `generation_plan.json`，改为现场 `_upload_to_r2` → `_register_asset` → 重新组装 plan，再调 `run_chunks`
- 不再需要手动指定 `--from-stage` / `--to-stage`，由 fingerprint 自动读取

### 🎬 storyboard-studio：流程升级为 8 阶段
- 新增 **Stage 2 `substitution_collect`**（暂停点）：统一收集人物 / 场景 / VO / 参考图替换信息，写入 `substitutions.json`
- 后续阶段（compose / review / redraw / seedance / audio / stitch）整体顺延一位

### 🎨 storyboard-replicate
- `step_2` 升级：持久化 `substitutions.json`，接入 `SUBS_TEMPLATE` 与 `refs/` 目录
- 模型升级：`claude-sonnet-4-5` → `claude-sonnet-4-6`

### 🖼️ style-duplicate
- `storyboard_gen_cli` 改为四区布局（banner / 左:角色+风格 / 中:面板栅格 / 右:光影+氛围+音频），与 Workflow C 对齐
- `prompt_composer_cli` 同步小幅调整

### 📝 video-burn-subtitle
- `llm_segment.py` 新增 `fix_overlaps()`，写 SRT 前消除相邻字幕时间重叠（最小 80ms 显示）

### 📦 Pack 元数据
- **新增**：`HEARTBEAT.md`、`TOOLS.md`（ZooClaw-Workspace-Convention）、`AGENTS.md` 末尾 `ZooClaw-Agent-Policy` 区块（cron 投递规范 / 安全 / Skill 保密）
- **移除**：`BOOTSTRAP.md`、`docs/`
- **保留**：`.agents/skills/pack-onboarding/`（1.9.2 tar 漏带，已从 main 恢复，与其他 12 个 pack 保持一致 — 首次使用 / `data/config.json` 缺失时仍走 onboarding）
- `agent-pack.yaml`：version 1.8.2 → 1.9.2，描述去中英混排

### 🎭 SOUL.md：人设调整
- 移除测试残留的 `## User Context` 预设（"餐饮探店运营 / TikTok 投放"），不再固化用户身份
- persona 从"creative director + technical producer"升级为**"想象力丰富的内容营销 CMO + 技术 producer"**，强调对 Hook、节奏、平台调性（TikTok / Reels / 小红书）的本能判断

## Test plan

- [ ] 在 OpenClaw 拉取此 pack，确认 `version=1.9.2`、avatar 正常加载
- [ ] 首次拉起 agent，确认 `pack-onboarding` 正常触发（无 `data/config.json` 时）
- [ ] 跑一次 Workflow C（storyboard-replicate）seed run，验证新 Stage 2 暂停 + `substitutions.json` 落地
- [ ] 跑一次 Workflow B/A 的 storyboard-studio，确认 8 阶段顺延正确
- [ ] 在 seed run 上执行 `seal_seed.py`，确认 `seed_fingerprint.json` 字段齐全
- [ ] `batch_run.py` 试跑（`--dry-run`），确认从 fingerprint 读取而不报缺 `--from-stage`
- [ ] 字幕烧录跑通，肉眼检查无相邻字幕时间重叠
- [ ] 与 agent 对话确认 SOUL persona 已无餐饮 / TikTok 默认预设，更偏 CMO 视角

🤖 Generated with [Claude Code](https://claude.com/claude-code)
