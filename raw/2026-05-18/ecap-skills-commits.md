# ecap-skills — 2026-05-18 Commits

## Commit 1: b2974359

- **SHA**: b2974359a68589c549133d86a28b30765a09e13c
- **Author**: david-srp
- **Date**: 2026-05-18T07:58:59Z
- **PR**: #197

### Commit Message

```
feat(chameleon): seedance 链路对齐官方教程 + 接入字幕擦除 + 防呆校验 (#197)

* feat(chameleon): expose return_last_frame for segment chaining

Enables auto-returning the final frame as an image URL via
--return-last-frame, so callers can feed it into the next call's
--first-frame for seamless multi-segment composition (15s + 15s + ...).

- CLI flag + payload field (opt-in, default off)
- find_last_frame_url helper + last_frame_url in summary/archive
- CSV log column + stderr warning when requested but missing
- KB-summary "视频接龙" section so chameleon recommends it
  for >15s chained generation tasks

* feat(chameleon): enforce client-side parameter validations

Catch invalid combinations before sending the upstream request,
turning opaque upstream errors and wasted R2 uploads into clear
local failures.

Adds to chameleon_generate.py:
- duration: must be in [4,15] or -1 (auto)
- reference image/video/audio counts: max 9 / 3 / 3 per BytePlus spec
- Fast model + resolution=1080p: rejected (only Pro supports 1080p)
- local image/video/audio file size: max 30MB / 50MB / 15MB,
  checked before R2 upload to avoid wasted bandwidth
- validate_args now runs before maybe_upload_local_sources

* feat(chameleon): wire subtitle-erasure via ecap-proxy (silent reference)

Routing policy: chameleon must NEVER proactively suggest this flow.
Invoked only when the user explicitly asks.

- scripts/erase_subtitles.py: new helper
- references/subtitle-erasure-flow.md
- SKILL.md routing rules updated

* fix(chameleon): move default archive root out of cwd into ~/openclaw

* fix(chameleon): align erase_subtitles endpoint with ecap-proxy spec
```

### PR #197 Body

## 背景

对照 BytePlus 公开的 Dreamina Seedance 2.0 系列教程，回头审计 chameleon skill 的接入实现。本 PR 把所有这一轮改动收齐：**新能力接入（尾帧接龙、字幕擦除）**、**客户端防呆校验**、**仓库卫生**。

### 1. feat(chameleon): expose return_last_frame for segment chaining

**业务价值** — 解决 Seedance 单次生成 ≤15s 的瓶颈：分段生成后用首帧锁住接缝，做出 >15s 的长视频。

- 单段跑完，API 同时返回视频最后一帧的图片 URL
- 下一段 CLI 直接 `--first-frame <那个 URL>` 续上，**省去 ffmpeg 抠帧的人工**
- ZooClaw 长视频业务（>15s 广告片、分镜接龙、内容工厂）的核心改造

### 2. feat(chameleon): enforce client-side parameter validations

**业务价值** — 把"参数传错 → 上游报错 → 用户搞不清是 bug 还是配置"的循环砍掉，错误本地秒拒，**还能省掉已经发生的 R2 上传带宽**。

| 校验 | 规则 |
|---|---|
| duration | ∈ [4, 15] 或 -1（auto） |
| 参考资产数量 | image ≤9 / video ≤3 / audio ≤3 |
| Fast 模型 + 1080p | 拒绝 |
| 本地文件大小 | 图≤30MB / 视频≤50MB / 音频≤15MB |

### 3. feat(chameleon): wire subtitle-erasure via ecap-proxy (silent reference)

**业务价值** — Seedance 偶尔会在画面里烧入字幕，用户想拿"干净画面"做二次创作或投放素材，可以一键调用 MediaKit 擦除。**已端到端实测通过**。

设计要点：
- **静默接入**：chameleon **永远不主动建议**字幕擦除，只在用户**显式**说出"擦字幕 / 去字幕 / erase subtitles"时路由
- **走 ecap-proxy**：复用 chameleon 已有的双 auth 头部，**不在客户端持有 ARK_API_KEY**

### 4. fix(chameleon): move default archive root out of cwd into ~/openclaw

**业务价值** — 修一个会污染仓库的设计 bug。`DEFAULT_ARCHIVE_ROOT` 之前是相对路径，改成 `~/openclaw/chameleon/generations`。

### 5. fix(chameleon): align erase_subtitles endpoint with ecap-proxy spec

与 ecap-proxy-service 团队对齐后定稿的路径，使端到端能跑通。
