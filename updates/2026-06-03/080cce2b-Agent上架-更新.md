---
title: "创始人IP工坊 Agent 升级到 2.0.1，支持定妆图与外貌描述双重锁定"
type: "Agent 上架/更新"
priority: "高"
date: "2026-06-03"
status: "待审核"
channels: "站内弹窗, 社媒素材, Use Case, Discord, changelog, KOL"
---
# 创始人IP工坊 Agent 升级到 2.0.1，支持定妆图与外貌描述双重锁定

## 核心宣传点

创始人IP工坊升级2.0，现支持上传定妆图和外貌描述，AI生成内容更贴近真实形象，品牌一致性大幅提升。

## 原始内容

**Repo:** SerendipityOneInc/ecap-agent-pack  
**SHA:** `080cce2ba2f5e74eae898b8c47282ef5261624fa`  
**作者:** lynn Zhuang  
**日期:** 2026-06-03T07:47:27Z  
**URL:** https://github.com/SerendipityOneInc/ecap-agent-pack/commit/080cce2ba2f5e74eae898b8c47282ef5261624fa

### Commit Message

```
feat(founder-ip-studio): 升级到 2.0.1 — 新增定妆图与外貌描述双重锁定 (#159)

将数字分身素材体系从 3 项（人脸/声音/场景）扩展到 5 项
（人脸/声音/定妆图/外貌描述/场景），解决 Seedance 单张照片
无法推断完整服装造型、每条视频形象漂移的问题。

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

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

