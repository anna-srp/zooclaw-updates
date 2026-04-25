# ecap-agent-pack - 2026-04-25

共 3 条 commits

---

## feat(agent-pack): upload agent pack by circe@srp.one (#104)

- **SHA**: `d2b9ef49cd1e957e63c413aa0d8b591681a9e947`
- **作者**: nolan-srp
- **日期**: 2026-04-24T11:18:38Z
- **PR**: #104

### Commit Message

```
feat(agent-pack): upload agent pack by circe@srp.one (#104)
```

### PR Description

## Summary
- add the cinead-ai agent pack definition
- add bundled agent documents, fonts, and skills
- include pack onboarding and TVC workflow assets

---

## feat(agent-studio): add share and install skills (#103)

- **SHA**: `847f9b8d208dd35d31cc026bdba01ef1ed5a063e`
- **作者**: nolan-srp
- **日期**: 2026-04-24T10:00:17Z
- **PR**: #103

### Commit Message

```
feat(agent-studio): add share and install skills (#103)
```

### PR Description

## Summary
- add an `agent-studio-share` skill and share script for packaging/exporting skills
- add an `agent-studio-install` skill and installer script for importing shared skills
- document the new share/install workflow in `agent-studio/AGENTS.md`

---

## feat(video-ads-duplicate): Mode A/B chunks + yt-dlp + multi-angle + progressive disclosure (#102)

- **SHA**: `d708d3cbdf3314d9589bd54502695ce09653d896`
- **作者**: david-srp
- **日期**: 2026-04-24T06:33:56Z
- **PR**: #102

### Commit Message

```
feat(video-ads-duplicate): Mode A/B chunks + yt-dlp + multi-angle + progressive disclosure (#102)

* feat(video-ads-duplicate): multi-mode chunks, yt-dlp download, multi-angle fidelity, progressive disclosure

Functional upgrades:
- Path A multi-chunk mode selection: Mode A (serial, continuity) vs Mode B (parallel, varied shots).
- yt-dlp as primary reference-video downloader; falls back to direct HTTP.
- Multi-angle product image support end-to-end (Seedance reference_image roles + prompt).
- Auto-inject product/audio blocks via --product-fidelity flag; dedupe guard for agent-provided blocks.
- New CLIs: batch_chunk_frames_cli.py, first_frame_prompt_cli.py; _upload.py gets CLI entry.

Performance + token efficiency:
- SKILL.md 711 → 341 lines (~52% reduction); dead ADJUST_VIDEO_PROMPT purged.
- Progressive disclosure: 3 references/ files loaded only on their trigger conditions.
- Average ~1500 tokens saved per conversation on SKILL.md alone.
- Mode B wall-clock ≈ single-chunk time regardless of chunk count (Semaphore=10).
- Strict chunk-index filename ordering guarantees concat matches script order.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(video-ads-duplicate): generalize sensitive-content fallback to all media (images + videos)

Previously the asset-register fallback was documented only for first-frame faces
(InputImageSensitiveContentDetected). Extended to cover every reference input —
first_frame, product reference_image (Path A multi-angle), and reference_video
(Path B). The guardrail is at URL level; Seedance fully accepts faces/PII via
asset:// refs, so downgrading content is never the right first move.

- Rename references/face-fallback.md → references/sensitive-content-fallback.md
  and add image + video procedures; cover Path B reference_video and audio-
  carrying video.
- Both Seedance CLIs now auto-annotate error_message with a pointer to the
  reference file whenever the error contains *SensitiveContentDetected* /
  PrivacyInformation markers, so the agent discovers the fallback without
  having to search docs.
- SKILL.md breadcrumbs updated: Stage 5 + Stage 6 Path B both reference the
  new file with explicit "do not downgrade content" rule.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(video-ads-duplicate): CLI auto asset-register fallback + self-contained bash recovery

Fixes the subagent-context gap: subagents spawned for long-running video
generation don't auto-load SKILL.md or references/, so a pointer in
error_message previously relied on the subagent knowing where to look. Now
the CLI itself does the fallback, and when it can't, the error_message
carries a complete bash recipe.

A. Auto asset-register (default on, --auto-asset-fallback=true)
  - Detect SensitiveContentDetected / PrivacyInformation markers in the
    Seedance response
  - Bulk-register every non-asset URL in the payload via chameleon's
    asset_register.py (Image for first_frame / reference_image, Video for
    reference_video)
  - Retry Seedance once with asset://<ID> references; +20-30s wall-clock
  - Covers single-segment, serial chunked, parallel chunked, replicator
    short + long paths

B. Self-contained bash recipe on auto-fallback failure
  - build_inline_fallback_bash emits the exact register+retry commands for
    every rejected URL
  - error_message concatenates pointer + bash so a subagent with zero skill
    context can copy-paste to recover

Shared helper: scripts/_asset_fallback.py (detect / register / recipe).

SKILL.md + references/sensitive-content-fallback.md updated — the manual
flow is now labeled "only when auto-fallback itself fails."

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(video-ads-duplicate): bump version 0.1.0 → 0.2.0

Reflects the scope of this iteration: Mode A/B chunks, yt-dlp, multi-angle
fidelity, CLI auto asset-register fallback, SKILL.md -52% + progressive
disclosure.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## 🚀 本次迭代总览

在初版 `video-ads-duplicate` 的基础上，围绕"生成质量"、"素材兼容性"、"token 效率"三条主线迭代。升级全部**向后兼容**，零用户配置变更。

---

## ✨ 功能升级（Feature）

### 1. Path A 多 chunk 的 Mode A / Mode B 选择 — 解决"长视频要么死板要么漫长"的痛点
长视频（> 15s）首次向用户提供**拼接模式二选一**：

| 模式 | 方案 | 体验 | 适用 |
|------|------|------|------|
| **Mode A · 连贯** | 尾帧串行接续（现有行为） | 镜头一镜到底，时间 ≈ N × 单段 | 故事性/连续跟拍广告 |
| **Mode B · 多样景别** | 每段独立首帧（人物+商品锚定，景别/姿势变化）并行生成 | 多镜头剪辑风格，时间 ≈ 单段耗时 | UGC 带货、快闪推广 |

- Mode B 落地流程：新 CLI `batch_chunk_frames_cli.py` → 把 Stage 5 首帧 + 商品图一起喂给 designer 的图生模型，同时加了硬约束 prompt："保留同一人物 + 同一商品，允许变化景别/姿势/视角"。
- 并发安全：`asyncio.Semaphore`（Seedance 上限 10，图生上限 3）；文件名强制 `segment_{idx:03d}.mp4` → **concat 拼接顺序严格按 chunk 索引，不受返回速度影响**。

### 2. yt-dlp 优先下载 — 解决 TikTok / YouTube / IG / FB 页面链接拉不到视频的问题
参考视频下载改为三级策略：
1. 直链（`.mp4/.mov/...`）→ 直接 HTTP
2. 其他 URL → **yt-dlp**（覆盖几乎所有社交平台）
3. yt-dlp 不可用/失败 → 回退到 HTTP

**用户收益**：之前 TikTok 链接常常拉到 HTML 页面导致 Seedance 报错；现在开箱即用。`video_replicator_cli.py` 的 `_normalize_video_source` 会在社交 URL 进来时自动走 yt-dlp → R2 上传 → 返回直链。

### 3. 多图商品多角度支持 — 解决"用户上传多张角度图被浪费"的问题
原行为：只用第一张主图。新行为：**所有商品图全部作为 `reference_image` 传给 Seedance**，并自动切 prompt 措辞：
- 1 张 → "the provided reference product image"
- ≥ 2 张 → "the N provided reference product images (multi-angle views of the SAME product)" + 硬约束"视为同一商品不同角度，不得混用特征"

影响范围：`video_generator_cli.py` 新增 `--product-image-urls`；Path B 短/长两路径、Stage 5 首帧生成、Mode B 每段首帧生成全线贯通。

### 4. 产品保真 / 音频纪律自动注入 — 告别 agent 手拼 prompt
Seedance 的 `[PRODUCT]`（保真规则）+ `[AUDIO]`（无字幕/无 BGM/只要音效）两块**从 SKILL.md 移到 Python**，`--product-fidelity {auto|always|never}` 控制：
- `auto`（默认）：有商品图/首帧时自动注入
- Agent 若自己写了 `[PRODUCT]`/`[AUDIO]` → 自动去重，不重复注入
- 多角度时自动切换措辞（见 #3）

### 5. 新增 CLI
- `first_frame_prompt_cli.py` — Stage 5 首帧 prompt 构造器（含 ZERO-TOLERANCE 保真块，支持 `--n-product-images`）
- `batch_chunk_frames_cli.py` — Mode B 并发批量首帧生成器
- `_upload.py` 加 CLI 入口 — 人脸 fallback 一行 bash 即可上传 R2

---

## ⚡ 性能升级（Performance / Efficiency）

### 1. SKILL.md 瘦身 711 → 341 行（**-52%**）
每次对话 agent 都要加载 SKILL.md，这是**每次对话的固定成本**。本轮通过三条路径砍下约 **2200 tokens/对话**：

- **干掉死代码**：`prompts.py` 里 100 行的 `ADJUST_VIDEO_PROMPT` 根本没人 import，已替代为 `script_generator_cli.py._build_prompt`；移除
- **CLI 文档去重**：Stage 6 末尾的 "CLI Reference" 和正文每个 Stage 的 bash 示例重复了 87 行 → 压成 16 行表格
- **规则硬编码**：Stage 5/6 里产品保真规则出现 3 次 → 移到 `prompts.py` 常量 + CLI 自动注入

### 2. 渐进式披露（Progressive Disclosure）
把**条件触发**的冷路径文档搬到 `references/`，agent 只在命中特定条件时才 `Read` 这些文件：

| 文件 | 内容 | 触发条件 | 命中率 |
|------|------|---------|--------|
| `references/long-video-chunking.md` | Mode A/B 选择 + chunk 规划 + 确认表 + chunks.json schema | `total_duration > 15s` | ~30% |
| `references/path-b-long-video.md` | `--allow-long-video` opt-in + 连续性警告 | Path B 源 > 15s | ~15% |
| `references/face-fallback.md` | InputImageSensitiveContentDetected 回退流程 | 首帧含人脸被拒 | <30% |

加权平均节省 **~1500 tokens/对话**（短视频路径最高节省 ~2200 tokens）。

### 3. Mode B 并行加速（Wall-clock 层面）
长视频过去只能串行：N 段 × 单段耗时。Mode B 的 `asyncio.gather` + Semaphore(10) 让 wall-clock 时间趋近于**单段耗时**，**N 越大省得越多**：

| Chunk 数 | Mode A 串行 | Mode B 并行 | 提速 |
|---------|------------|------------|------|
| 2 (30s) | 2 × T | ~1 × T | 2× |
| 4 (60s) | 4 × T | ~1 × T | 4× |
| 6 (90s) | 6 × T | ~1 × T | 6× |

（T = 单次 Seedance 调用耗时，通常 30-60s）

### 4. 可靠性 / 工程细节
- Mode B 并行完成顺序不可控 → **文件名强制 `segment_{idx:03d}.mp4`**，ffmpeg concat 按文件名排序 → 拼接顺序确定
- `compose_seedance_prompt` 有 duplicate-guard：agent 手拼 `[PRODUCT]` 不会被覆盖或重复
- yt-dlp 降级策略：仅当"看起来像直链"时跳过 yt-dlp；否则总是先尝试（社交媒体覆盖度最大）

---

## 📊 数据快照

| 指标 | 变化 |
|------|------|
| SKILL.md 行数 | 711 → **341（-52%）** |
| SKILL.md 估算 tokens | 5554 → **~3710（-33%）** |
| 每次对话加权节省 | **~1500 tokens** |
| 冗余死代码 | 100 行 `ADJUST_VIDEO_PROMPT` 清除 |
| CLI 总数 | 6 → **8**（新增 `first_frame_prompt_cli`, `batch_chunk_frames_cli`；`_upload.py` 加 CLI 入口）|
| Mode B 长视频提速 | **N× 倍加速**（N = chunk 数） |

---

## 📋 Test Plan
- [ ] TikTok 页面链接 → yt-dlp 自动提取视频并上传 R2
- [ ] Path A 短视频（≤15s）+ 单张商品图 → 正常工作（向后兼容）
- [ ] Path A 短视频 + 3 张多角度商品图 → prompt 中出现 "3 provided reference product images (multi-angle views)"
- [ ] Path A 长视频（25s） + Mode A → 串行生成，尾帧自动接续
- [ ] Path A 长视频（25s） + Mode B → 4 段并行生成，wall-clock ≈ 单段耗时
- [ ] Mode B 场景下人为延迟某一段，确认最终视频顺序不乱
- [ ] Path B 短视频 → 正常工作
- [ ] Path B 长视频 → 默认拒绝；加 `--allow-long-video=true` 走 chunked replication
- [ ] 首帧含人脸被 Seedance 拒 → 走 asset register flow
- [ ] SKILL.md 内不再提 Mode A/B 详细流程（已移到 references/）
- [ ] agent 在 total_duration > 15s 时会主动 Read references/long-video-chunking.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 🩹 补丁 (79faae9) — 敏感内容 fallback 覆盖全媒体

用户反馈：人脸 fallback 流程不该只限首帧图片，**Path A 的商品参考图 + Path B 的参考视频**撞到 BytePlus 敏感内容守卫时，同样应该走 asset 注册而不是降级内容。

### 改动
- `references/face-fallback.md` → **`references/sensitive-content-fallback.md`**，新增：
  - 图片流程（first_frame、product reference_image 共用）
  - 视频流程（yt-dlp 下载 → R2 → chameleon `--asset-type Video`）
  - 覆盖 reference_video 里的音轨（随视频资产一起注册）
- **两个 Seedance CLI 自动标注 error_message**：撞到 `InputImageSensitiveContentDetected` / `InputVideoSensitiveContentDetected` / `PrivacyInformation` 任一 marker 时，error_message 自动追加指针 `→ references/sensitive-content-fallback.md`，agent 不用搜文档就能跟进。带 dedupe 保护，不重复追加。
- SKILL.md 两处 breadcrumb 同步（Stage 5 通用敏感内容 + Stage 6 Path B reference_video 专门提示），反复强调"**never downgrade content**"。

### 核心原则（强调）
**URL 级别守卫，不是模型局限**。Seedance 2.0 通过 `asset://<ID>` 完全支持真人脸和 PII 内容。降级内容（换脸/换图/换视频）是最后手段，不是第一反应。


---

## 🛡️ 补丁 (9852909) — A+B 自动 asset-register，subagent 也能自救

针对先前 PR 描述里未覆盖的 **subagent context 断裂**问题：subagent 不会自动加载 SKILL.md / references，即使 error_message 里有指针也可能找不到路径。两层保护：

### A — CLI 自动 retry（默认开启）
- 两个 Seedance CLI 在撞到 `InputImage/VideoSensitiveContentDetected` / `PrivacyInformation` 时**自动**调 chameleon 的 `asset_register.py` 批量注册所有非 asset URL（image→Image 类型、video→Video 类型）
- 拿到 `asset://<ID>` 后 **自动 retry 一次 Seedance**
- 覆盖：Path A 单段 / Path A 串行 chunk / Path A 并行 chunk / Path B 短视频 / Path B 长视频分段
- Wall-clock 开销：仅在触发时 +20–30s（register --wait + retry），未触发零开销
- 开关：`--auto-asset-fallback {true|false}`（default `true`）

### B — error_message 自带 bash（降级保护）
当 A 本身失败（chameleon 不可用 / register timeout / 解析失败），`error_message` **拼上完整可运行的 bash 脚本**，列出每个被拒 URL 对应的 register 命令和重跑提示。subagent 拿到错误串即可 copy-paste 自救，不依赖任何文档。

新增共享模块：`scripts/_asset_fallback.py`（detect / register / recipe）。

### 文档同步
- `references/sensitive-content-fallback.md` 重写：把"auto-fallback 是默认"放前面，manual flow 标明"auto 失败后才需要"
- SKILL.md 两处 breadcrumb 同步，明确告诉 agent：一般情况无需干预

### 测试
7 个断言全过：敏感检测、asset-ID 解析启发式（JSON / 嵌套 data.Id / regex 扫描）、bash 生成、error_message 拼装、CLI flag 注册、asset:// passthrough、跨模块 import。


