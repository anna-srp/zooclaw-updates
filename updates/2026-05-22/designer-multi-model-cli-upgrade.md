---
title: "Designer Skill 支持更多 AI 模型参数（Gemini 分辨率分级 / 思考强度 / DALL-E 数量）"
type: "Skill 上架/更新"
priority: "中"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# Designer Skill 支持更多 AI 模型参数（Gemini 分辨率分级 / 思考强度 / DALL-E 数量）

## 核心宣传点

使用 Designer Skill 时，现在可以更精细地控制 AI 绘图参数，包括 Gemini 的图片尺寸分级、思考深度和 DALL-E 的生成数量，生成效果更可控。

## 原始内容

**Commit**: 27544935700f0deaa42d6e1e5faacd4793813636
**Author**: vincent-srp
**Date**: 2026-05-22T12:37:56Z
**PR**: #204

### Commit Message
```
designer: 补齐各模型 CLI 能力（n / Gemini size tiers / thinking-level）+ 文档抗幻觉加固 (#204)

* docs(designer): harden against agent quoting stale sizes from memory

The v0.6.1 release fixed the script and added a Doc-freshness mechanism,
but a downstream agent still hallucinated "gpt-image-2 max 1536px" — it
saw the freshness date and confidently quoted its training memory rather
than reading the actual constraint line.

Root cause: visual layout. The v2 card led with a 3-column pricing table
(1024×1024 | 1024×1536 | 1536×1024) which pattern-matches as "the
supported sizes". The corrective "any resolution within constraints" line
was buried 8 bullets down in plain text. Same trap appeared in the
nano-banana common-params list and decision-rules pricing/latency rows.

Fixes:
- Restructure gpt-image-2 card: size constraints in a ⚠️ callout at the
  very top; pricing table demoted below with an explicit disclaimer that
  it shows "pricing-published points", not allowed sizes.
- Add a 🔒 "common fact, often misquoted" callout to SKILL.md so the v2
  size truth is in baseline context, not just on-demand references.
- Reword Doc-freshness header to say "the date means we cross-checked,
  not that your recall is correct — read the line verbatim before
  quoting any specific number."
- In decision-rules.md, replace literal "1024×1536 / 1536×1024" pricing
  citations with size-class descriptors ("~1MP square", "~1.5MP
  non-square pricing points") so they can't be misread as enumerations.
- Move per-model aspect_ratio lists from the nano-banana family-level
  bullet into each per-model card, with explicit counts (10 / 14) so
  nano-banana-2's extra extreme ratios are visible at point of use.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(designer): fill in per-model size/pricing/ref-limit gaps for nano-banana family + grok

Sweep for the same kind of staleness that bit gpt-image-2. Found three
real informational gaps across the Gemini and Grok cards:

- nano-banana-2: was only listing 0.5K and 1K pricing — missing 2K
  ($0.101) and 4K ($0.151) standard rows, plus all four batch rows.
  Now lists every tier and notes the 512 size value uses no K suffix.
- nano-banana-pro: never stated that output sizes are fixed 1K/2K/4K
  tiers requiring uppercase K. Also added per-Google ref-image cap
  (6 object + 5 character ≈ 11 total, role-typed).
- nano-banana: never stated the 1K hard cap or the "up to 3 input
  images" soft limit. Both now explicit.
- grok hidden row: `n` supports up to 10 per request upstream;
  designer's CLI hardcodes n=1 (documented as a known gap).
- nano-banana-2 thinkingLevel (minimal/high) documented as a known
  upstream param not currently exposed by the CLI.

Family-level "Common params" bullet rewritten to make clear that
aspect_ratio / size / ref limits all vary per model — agents must read
the per-model card for authoritative values, not the family-level
summary. The current CLI also doesn't expose a size selector for the
Gemini path; that gap is documented inline so agents know to recommend
bypassing the CLI for explicit 2K/4K outputs.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* feat(designer): close 3 CLI gaps — --n, Gemini --size tiers, --thinking-level

Three feature gaps were documented but unimplemented in the prior PRs:
  1. n hardcoded to 1 across all paths (Grok docs allow up to 10 natively,
     GPT supports it natively, Gemini needs parallel fan-out).
  2. Gemini path had no --size selector — couldn't request 2K / 4K on
     nano-banana-pro or 0.5K / 4K on nano-banana-2.
  3. --thinking-level (nano-banana-2 only) wasn't exposed.

Closes all three.

CLI surface
  --n 1..10                 default 1, hard-capped at 10 with warning
  --size                    extended semantics:
                              GPT: WxH | auto (unchanged)
                              Gemini: tier strings, validated per model
                                nano-banana-2 ⊃ {512, 1K, 2K, 4K}
                                nano-banana-pro ⊃ {1K, 2K, 4K}
                                nano-banana → ignored (no size selector)
                              Grok: ignored
  --thinking-level minimal|high
                            nano-banana-2 only; other models → ignored

Stdout contract changed: one file path per line. n=1 still yields a single
line (back-compat for the existing agent flow). result dict adds
file_paths: list[str] alongside file_path: str (= first path).

Per-path implementation
  GPT     pass n natively to client.images.{generate,edit}; iterate
          response.data → list[b64]
  Grok    pass n in body (up to 10); timeout scales 120s + 30s/extra
  Gemini  asyncio.gather n parallel _generate_litellm calls. image_size
          and thinking_level forwarded via image_config snake_case
          (matching existing aspect_ratio pattern); LiteLLM expected to
          translate to Google's camelCase generationConfig fields.

Validation
  _resolve_gemini_size  per-model allow-list, lowercase/unknown sizes
                        rejected with warning, falls back to API default
  _resolve_gemini_thinking
                        gates on nano-banana-2; validates {minimal, high}
  _validate_n           clamps to [1, 10]

Docs
  SKILL.md             updated CLI signature block; clarified per-family
                       --size semantics; stdout now described as
                       "one path per line"
  models.md            removed all "CLI doesn't expose / bypass the CLI"
                       gap notes — those gaps no longer exist

Tested
  - syntax OK
  - 26/26 validator assertions pass (size per-model, thinking gating,
    n clamping)
  - argparse --help renders all new options correctly

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(designer): salvage partial Gemini fan-out + warn on incomplete n

Audit of the CLI script surfaced one real data-loss bug and three minor
cleanups:

1. (BUG) asyncio.gather for the Gemini --n fan-out used the default
   return_exceptions=False. A single sub-call raising — for any reason
   — would cancel the other in-flight calls and propagate up to the
   outer try/except, returning zero images even when 9 of 10 succeeded.
   Switch to return_exceptions=True, log each exception, salvage the
   rest. Verified: 1 exception + 2 successes now yields 2 paths, not 0.

2. Add a partial-success warning at the end of generate_image — if we
   asked for n=10 and got 7 saved files, the caller now sees a warning
   rather than silent success. Applies to all three paths.

3. Module-top docstring still said "prints the file path to stdout"
   from the n=1-only era. Updated to describe the multi-line contract
   and add --n / --size examples.

4. Constants (MAX_IMAGE_DIMENSION, JPEG_QUALITY, HTTP_TIMEOUT,
   OUTPUT_DIR) had drifted into the middle of the file between resolver
   functions. Moved back to the top-of-file Constants block.

5. _validate_n now warns when called with a negative integer instead of
   silently clamping to 1.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description
## 背景

v0.6.1 修了 gpt-image-2 的三档强映射并加了 Doc-freshness 机制后，下游 agent 仍然信誓旦旦地说"gpt-image-2 最大 1536px"。复盘发现两件事：

1. **文档结构问题**：v2 card 顶部的价格表表头 `1024×1024 / 1024×1536 / 1536×1024` 视觉上被当成 size 枚举，"任意分辨率 + 4 约束"那行埋在 8 个 bullet 下面。
2. **CLI 能力盲区**：models.md 写着 nano-banana-pro 支持 4K，但 designer CLI 根本没暴露 Gemini 的 `--size`；写着 grok n=10，但 CLI hardcode n=1；nano-banana-2 的 `thinkingLevel` 没暴露。

这个 PR 同时收口两端。

---

## 改了什么（按用户影响维度）

### 🆕 CLI 能力补齐（commit `fbccb2e`）

- **`--n 1..10`** — GPT / Grok 原生透传；Gemini 通过 `asyncio.gather` 并行 fan-out。统一上限 10。
- **`--size` 扩展 Gemini 路径** — 接受 tier 字符串，按模型 allow-list 校验：
  - `gemini-3.1-flash-image-preview` ⊃ {`512`, `1K`, `2K`, `4K`}
  - `gemini-3-pro-image-preview` ⊃ {`1K`, `2K`, `4K`}
  - `gemini-2.5-flash-image` 不支持（warning 后丢弃）
  - GPT 路径语义保持不变（`WxH` / `auto`）
- **`--thinking-level minimal|high`** — 仅 `gemini-3.1-flash-image-preview` 生效；其他模型 warning 后丢弃。Best-effort 透传给 LiteLLM 的 `image_config`（最终需要 LiteLLM 转译到 Google 的 `generationConfig.thinkingConfig`）。

### 🐛 真 bug 修复（commit `ed9a55d`）

- **Gemini fan-out 部分成功救援** — 之前 `asyncio.gather` 默认 `return_exceptions=False`，请求 `--n 10` 时如果**任何一个**子调用抛异常，会立即取消其他 9 个并向上抛 → 用户拿到 0 张图（哪怕 9 张已成功）。改成 `return_exceptions=True` + 逐个 unpack + warning。
- **部分成功告警** — 三条路径都加了 `if len(file_paths) < requested_n: warning(...)`，避免用户请求 10 张拿到 7 张时静默成功。
- `_validate_n(-3)` 不再静默 clamp，加 warning。
- 模块顶 docstring 过期描述更新；orphan 常量归位到 Constants 块。

### 📚 文档信息完整性（commit `b3f033c`）

之前 nano-banana 家族多个 model card 信息不全：

| 模型 | 之前 | 现在 |
|---|---|---|
| nano-banana-2 | 只列 0.5K + 1K 价 | 补全 4 档（0.5K / 1K / 2K / 4K）standard + batch |
| nano-banana-pro | `$0.134/1K-2K, $0.24/4K` | 加 size tier 行说明、ref-image 上限（6 object + 5 character ≈ 11）|
| nano-banana | 只 flat $0.039 | 加 1K cap + up-to-3 ref images |
| Grok | "edit accepts 3 ref" | 加 n=10 native（与 CLI 同步） |
| nano-banana-2 | — | 文档化 `thinkingLevel` 参数 |

### 🛡️ 文档结构抗幻觉加固（commit `e47153f`）

- **`models.md` gpt-image-2 card 重构** — size 约束提升到 ⚠️ callout 放在 Docs 行后第一位；价格表降到第 5 位并加显式 disclaimer："the model itself accepts arbitrary sizes per the constraints above"
- **`decision-rules.md` §C2 / §C4** — `$0.053 at 1024²` 这种引用改成 `~$0.053 at 1MP square` 类的 size-class 描述，避免被误读为 size 枚举
- **`SKILL.md` baseline 增加 🔒 "Common fact, often misquoted" callout** — 因为 references 是按需加载的；这条 fact 进 baseline context 后 agent 无法绕过
- **Freshness header 措辞收紧** — 从"日期=最近核对过"改成"日期=最近核对过，**不代表你记忆里的数字是对的**；引用任何数前必须 verbatim 重读对应行"

---

## 校验

- ✅ Syntax + 26/26 单元断言（v2 size computer / 各 resolver / `_validate_n`）
- ✅ `asyncio.gather` salvage 行为本地验证：3 个 call (good / bad / good) 现在返 2 个成功
- ✅ Staging deploy：`v0.6.3-beta.1`（前两个 commit）和 `v0.6.3-beta.2`（含 audit 修复）都成功
- ⏳ Live agent 烟雾测试待补：
  - "what's gpt-image-2 max edge?" 应答 3840（不是 1536）
  - "what aspect ratios does nano-banana-2 support?" 应答 14（不是 10）
  - `--n 4 --model openai/gemini-3-pro-image-preview --size 2K` 应返 4 张 2K 图

## 已知保留

- Gemini 的 `image_size` / `thinking_level` 通过 LiteLLM `image_config` snake_case 透传，依赖 LiteLLM 转译到 Google API 的不同结构（`generationConfig.responseFormat.image.imageSize` / `generationConfig.thinkingConfig.thinkingLevel`）。本地已加严格校验防止脏数据出门；若 LiteLLM 未转译，API 用默认值而非报错。`models.md` 对 `thinkingLevel` 显式标注 "best-effort"。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

