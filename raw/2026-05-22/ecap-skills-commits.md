# ecap-skills — 2026-05-22

共 6 条 commits

---

## 27544935 designer: 补齐各模型 CLI 能力（n / Gemini size tiers / thinking-level）+ 文档抗幻觉加固 (#204)

- **SHA**: 27544935700f0deaa42d6e1e5faacd4793813636

- **Author**: vincent-srp

- **Date**: 2026-05-22T12:37:56Z

- **PR**: #204


### Full Commit Message
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


### PR Body
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

---

## 7492cb99 fix(publish): LFS on checkout, add _fonts, drop websearch from publish list (#203)

- **SHA**: 7492cb9991e411a294c8cb1617da63c9daef1ae2

- **Author**: allenz-srp

- **Date**: 2026-05-22T11:06:58Z

- **PR**: #203


### Full Commit Message
```
fix(publish): LFS on checkout, add _fonts, drop websearch from publish list (#203)

* fix(publish): pull Git LFS on checkout + add _fonts to publish whitelist

#202 introduced a Git LFS-tracked font library (_fonts/), but the publish
workflow's `actions/checkout@v4` defaults to lfs:false — so the checkout would
yield 130-byte LFS pointer files and `aws s3 sync` would publish pointers
instead of the real fonts to extra-skills/. Add `lfs: true` to all three
(dev/staging/production) checkout steps.

Also add `_fonts` to PUBLISHED_SKILLS so the shared font library is actually
synced to the extra-skills volume (it was excluded by the whitelist, and
--delete would have removed it otherwise).

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>

* chore(publish): drop websearch skill from publish list

Native web_search now ships via the @zooclaw/web-search plugin, so the legacy
websearch skill should no longer sync to the S3 gateway. Removing it from
PUBLISHED_SKILLS means the next publish (--delete) will remove
extra-skills/websearch/ from the gateway.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```


### PR Body
## Changes
1. **`lfs: true` on all 3 checkout steps** — #202 added a Git LFS font library (`_fonts/`, ~606MB). `actions/checkout@v4` defaults to `lfs: false`, so the checkout yields 130-byte LFS *pointer* files and `aws s3 sync` would publish pointers, not real fonts. (This is why v0.6.x wasn't published after merging #202.)
2. **Add `_fonts` to `PUBLISHED_SKILLS`** — otherwise the shared font library is never synced (and `--delete` would remove it). Synced to `extra-skills/_fonts/`.
3. **Drop `websearch` from `PUBLISHED_SKILLS`** — native web_search now ships via the `@zooclaw/web-search` plugin, so the legacy `websearch` skill should no longer sync. Next publish (`--delete`) will remove `extra-skills/websearch/` from the gateway.

## Heads-up
- First publish uploads ~606MB of fonts to `extra-skills/`; `aws s3 sync` is incremental afterwards.
- `--delete` will remove `extra-skills/websearch/` on the next publish — intended.
- Delivery model assumed = via extra-skills volume. If fonts should come from CDN (assets.yesy.site) instead, drop the `_fonts` whitelist line and keep only `lfs: true`.
- Still open (not in this PR): confirm redistribution rights for `方正粗金陵简体`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## de97bffb feat: add font library collection with Git LFS (#202)

- **SHA**: de97bffb550547a316f00c59dada60693a7c2209

- **Author**: shana-srp

- **Date**: 2026-05-22T10:53:32Z

- **PR**: #202


### Full Commit Message
```
feat: add font library collection with Git LFS (#202)

* feat: add font library collection with 101 usable fonts + 43 brand references

Curated font catalog (fonts.json) covering Google Fonts, cn-fontsource CDN,
Vercel Geist, Apple/Microsoft system fonts, and standalone sources.
Includes visual showcase HTML and SKILL.md shared resource documentation.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* chore: remove _font-library-collection, font data lives in extra-skills/_fonts

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* refactor: move font files from extra-skills/_fonts/ to _fonts/

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* feat: download all 101 fonts to _fonts/ with Git LFS

Download all open-source fonts from the font library catalog:
- Source Han Serif (10 language variants/subsets, woff2)
- 88 Google Fonts (display/sans/serif/mono/CJK/handwriting)
- 4 cn_fontsource fonts (Smiley Sans, Yozai, LXGW WenKai, MiSans)
- Geist + Geist Mono (Vercel)
- D-DIN (SpaceX)
- 方正粗金陵简体 (local TTF)

Total: 3532 font files (~606MB), tracked via Git LFS.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

* chore: migrate 方正粗金陵简体.TTF to Git LFS

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```


### PR Body
## Summary
- Add curated font library at `_fonts/` with **101 usable fonts + 43 brand typography references**
- `fonts.json` — machine-readable font catalog (Google Fonts, cn_fontsource, standalone fonts, brand references)
- `font-showcase.html` — visual preview page ([live preview](https://assets.yesy.site/f/web/2026/05/h26moqy3.html))
- Download all open-source font files (~606MB, 3532 files) managed via **Git LFS**:
  - Source Han Serif (10 language variants/subsets, woff2)
  - 88 Google Fonts (display/sans-serif/serif/monospace/CJK/handwriting)
  - 4 cn_fontsource fonts (Smiley Sans, Yozai, LXGW WenKai, MiSans)
  - Geist + Geist Mono (Vercel), D-DIN (SpaceX), 方正粗金陵简体

## Test plan
- [ ] Verify `git lfs pull` works on fresh clone
- [ ] Confirm `fonts.json` is valid JSON and all font entries are consistent
- [ ] Open `font-showcase.html` and verify fonts render correctly
- [ ] Verify `.gitattributes` LFS tracking rules cover all font extensions

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 760b9c2e feat(chameleon-seedance): queue priority + rename for stronger Seedance routing (#199)

- **SHA**: 760b9c2e1fd0fe56c6078dfff3399aa7722bd86e

- **Author**: david-srp

- **Date**: 2026-05-22T09:59:00Z

- **PR**: #199


### Full Commit Message
```
feat(chameleon-seedance): queue priority + rename for stronger Seedance routing (#199)

* feat(chameleon): expose Seedance 2.0 queue priority field

Add --priority CLI flag (int 0-9, default 0) on chameleon_generate.py,
validate the range client-side, and inject "priority" into the payload
only when non-zero so default requests stay clean. Document the field
semantics (per-endpoint queue jump, never preempts running, not honored
under service_tier=flex) in the BytePlus API reference and KB summary.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(chameleon-seedance): rename skill to surface Seedance in routing

Rename the skill directory chameleon -> chameleon-seedance so "seedance"
appears in the skill's canonical name (a stronger routing signal than the
description alone). Rewrite the SKILL.md description into an English
TRIGGER / SKIP pattern that lists Seedance / Dreamina / dreamina-seedance
keywords plus common request verbs, and explicitly defers burned-in
subtitle removal to the user-level subtitle-erasure skill so the two no
longer compete on the "Seedance" keyword.

Also update PUBLISHED_SKILLS so the S3 release tracks the renamed dir.
The trace/archive layer at ~/openclaw/chameleon/ is intentionally left
untouched — that path follows the project codename, not the skill name,
so existing user archives are preserved.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR Body
## Summary

Two commits on this branch:

### 1. `feat`: expose Seedance 2.0 queue priority field
- New `--priority N` CLI flag on the generation script (int, default `0`, range `0-9`); client-side rejects out-of-range
- Payload only carries `"priority": N` when `priority > 0`, so default requests stay clean
- Updated `byteplus-dreamina-seedance-2.0-api.md` and `chameleon-kb-summary.md` with the field's semantics: Seedance 2.0 only, per-endpoint queue jump, same-priority stays FIFO, never preempts a `running` task, not honored under `service_tier=flex`

### 2. `refactor`: rename `chameleon` → `chameleon-seedance`
- Surface "seedance" in the skill's canonical name → strongest routing signal when users mention Seedance / Dreamina
- Rewrite the `SKILL.md` description into an explicit English **TRIGGER / SKIP** pattern, listing common keywords (seedance, Seedance 2.0, Dreamina, dreamina-seedance-2-0, ByteDance video model, Volcengine video generation) and request verbs (generate / produce / render / chain / extend a video, lock first/last frame, attach reference media, set queue priority)
- **SKIP and route to `subtitle-erasure`** for burned-in subtitle removal — disambiguates the two skills that both mention "Seedance"
- `PUBLISHED_SKILLS` updated so the S3 release picks up the renamed directory
- Trace/archive layer `~/openclaw/chameleon/` **intentionally left untouched** — that path is tied to the project codename, not the skill name, so existing user archives are preserved

## Test plan
- [x] `--priority 5` / `--priority 7` → payload contains `"priority": N`
- [x] Default invocation → payload omits `priority`
- [x] `--priority 10` / `--priority -1` → rejected client-side with clear error
- [x] Dry-run still works from the renamed `chameleon-seedance/scripts/` path
- [ ] Submit one real task with `--priority` set, confirm ecap-proxy / upstream ModelArk accepts the new field
- [ ] After merge, confirm openclaw harness picks up the renamed `chameleon-seedance` skill from S3 and Seedance keyword queries route to it (no more drift to subtitle-erasure)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 92019e38 chore(designer): refresh against upstream docs + flexible gpt-image-2 sizing (#201)

- **SHA**: 92019e38f46405fb150ce1f3537118ee16372e72

- **Author**: vincent-srp

- **Date**: 2026-05-22T09:43:06Z

- **PR**: #201


### Full Commit Message
```
chore(designer): refresh against upstream docs + flexible gpt-image-2 sizing (#201)

* chore(designer): refresh against upstream docs + flexible gpt-image-2 sizing

Audit findings (vs OpenAI / Google / xAI docs as of 2026-05-22):
- gpt-image-2 now accepts any resolution (16-multiple edges, ≤3840px,
  ≤3:1 long:short, 655K–8.3M pixels) + size=auto. Replace the 3-tier dict
  with a per-family resolver: computer for v2, legacy dict for v1.x.
- Add --size passthrough and --quality auto for explicit control.
- Drop renamed grok-imagine-image-pro → -quality; drop dead gpt-image-1;
  add gpt-image-1-mini. Cap xAI edit refs at 3 (was 5).
- Fix stale prices: gpt-image-2 non-square cheaper than 1024², edit
  tokens $30/M out (was 32), nano-banana-2 $0.067/1K (was $0.02).

Add "Doc freshness" headers (date + upstream URLs + re-verify triggers)
to models.md and decision-rules.md so future audits have a clear handle.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* chore(designer): slim SKILL.md — move sizing detail back to models.md

SKILL.md is the routing surface; detailed size constraints and the
v2-vs-v1.x sizing split already live in references/models.md and are
loaded on demand. Removing the duplicated "Size handling" bullets and
tightening the Doc-freshness pointer to a single sentence.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* docs(designer): mark medium as default quality in SKILL.md CLI note

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(designer): align CLI behavior with current OpenAI image docs

Five fixes surfaced by exhaustive edge-case testing:

1. quality=auto was being forwarded to gpt-image-1.5 / gpt-image-1-mini,
   which only accept low/medium/high per docs. Now filtered with a
   warning; only gpt-image-2 receives quality=auto.

2. --size on gpt-image-2 was a blind passthrough — 4000x4000, 1080-edge,
   uppercase X, and other invalid inputs all reached the API and returned
   opaque errors. New _validate_v2_size() enforces the four documented
   constraints (16-multiple edges, ≤3840px, ≤3:1, pixel budget) and
   falls back to the computer on violation.

3. _compute_gpt_image_2_size() now rejects non-positive / non-finite
   ratios (0:1, -1:1, inf:1) up front instead of producing nonsense via
   the 3:1 clamp.

4. v2 sizing now uses the raw aspect_ratio (e.g. 1.85:1 → 1392x752 with
   true 1.851 long:short), not the value pre-snapped to designer's 10
   common ratios. v1.x still uses the snapped value because its legacy
   dict expects exact keys.

5. Single-ref restriction narrowed to gpt-image-1.5 alone. Docs are
   silent on gpt-image-1-mini's multi-ref support — better to let the API
   enforce than to silently drop user-provided references.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR Body
## Summary

Full audit of the `designer` skill against current OpenAI / Google / xAI image-API docs (verified 2026-05-22). Fixes the most-impactful staleness: gpt-image-2 has supported arbitrary resolutions for a while, but the CLI was still snapping every aspect_ratio to one of three fixed sizes — so 4:5, 16:9, 21:9 outputs were silently being delivered as 3:2.

### Script (`scripts/image_generation_cli.py`)
- Replace `ASPECT_RATIO_TO_GPT_SIZE` 3-tier dict with a per-family resolver:
  - **gpt-image-2** → new `_compute_gpt_image_2_size()` that respects the four documented constraints (max edge ≤ 3840px, both edges multiples of 16, long:short ≤ 3:1, total pixels ∈ [655 360, 8 294 400]) and targets ~1MP for the cheapest pricing tier. Returns `auto` when no ratio is given.
  - **gpt-image-1.5 / gpt-image-1-mini** → keep the legacy 3-tier dict (upstream still locks them to 1024², 1536×1024, 1024×1536).
- Add `--size WxH|auto` passthrough for explicit pixel control (gpt-image-2 trusts user input; v1.x validates against the 3-tier set).
- Add `--quality auto` (gpt-image-2 only).
- Drop renamed `grok-imagine-image-pro` → `grok-imagine-image-quality`.
- Cap xAI edit reference images at 3 (was 5; docs.x.ai limit).
- Update v1.x single-ref restriction set: drop dead `gpt-image-1`, add `gpt-image-1-mini`.

### Docs
- **`SKILL.md`**: refreshed hidden-model list, `--quality auto` / `--size` in the call example, new "Size handling" paragraph explaining v2 vs v1.x behavior.
- **`references/models.md`**: gpt-image-2 pricing → 3×3 table (size × quality, non-square is cheaper); edit token pricing corrected to `$30/M out` (was 32); output description rewritten to "any resolution + 4 constraints"; nano-banana-pro / nano-banana-2 / nano-banana pricing all refreshed (nano-banana-2 was the most stale: `$0.02` → `$0.067/1K`); hidden list updated; dead `gpt-image-1` removed.
- **`references/decision-rules.md`**: §C2 prices augmented with non-square tiers; `quality=auto` documented; §C4 latency footnote noting v2 latency now tracks pixel count.
- **`.env.example`**: grok model name updated.

### Doc-freshness mechanism
Added a **Doc freshness** header at the top of both reference files with last-verified date, upstream URLs, and re-verify triggers (user disputes a value / API rejects a documented value / > 3 months old). `SKILL.md` mentions the convention so future agents know to look. Future audits only need to refresh the date and any drifted rows.

## Test plan

- [x] `python3 -c 'import ast; ast.parse(...)'` — syntax clean
- [x] Resolver sanity check on 16 aspect-ratio inputs + 8 `--size` overrides × 2 model families — all outputs satisfy the v2 constraints (16-multiple, ≤ 3840, ≤ 3:1, pixel budget) and v1.x stays in the 3-tier set
- [x] Final `grep` sweep for `grok-imagine-image-pro`, `gpt-image-1` (bare), `ASPECT_RATIO_TO_GPT_SIZE`, `32/M out`, `2560×1440`, `$0.02 per image` — no remaining stale references except intentional rename annotations
- [ ] Live smoke: call `image_generation_cli.py --model gpt-image-2 --prompt "..." --aspect-ratio 16:9` and confirm the returned image is ~1360×768, not 1536×1024
- [ ] Live smoke: `--size auto` returns a non-square when prompt implies it
- [ ] Live smoke: `--model grok-imagine-image-quality --prompt "..."` succeeds via ecap-proxy

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 07c346f9 chore(devcontainer): rely on forwarded gateway port (#200)

- **SHA**: 07c346f921ed0e2093970f61ea0f2fa68fbcf733

- **Author**: kaka-srp

- **Date**: 2026-05-22T04:18:58Z

- **PR**: #200


### Full Commit Message
```
chore(devcontainer): rely on forwarded gateway port (#200)
```


### PR Body
## Summary

- Keep `workspaceFolder` unchanged at `/home/node`.
- Stop publishing a fixed Docker Compose host port `18789:18789` for the devcontainer.
- Add explicit Dev Containers forwarding for container port `18789`, so local machines that already use `localhost:18789` can still start/rebuild the container.
- Clarify the split between nginx/webchat ingress (`18789`) and the internal OpenClaw gateway (`18790`).
- Update post-start output and docs to tell developers to use the actual local port shown in the VSCode/Cursor Ports panel when `18789` is already occupied.

## Validation

- `jq empty .devcontainer/devcontainer.json`
- `jq empty .devcontainer/openclaw.json.tmpl`
- `bash -n .devcontainer/initializeCommand.sh .devcontainer/postCreateCommand.sh .devcontainer/postStartCommand.sh .devcontainer/restart-gateway.sh .devcontainer/setup-extras.sh .devcontainer/chromium-fit.sh`
- `docker compose -f .devcontainer/docker-compose.yml --env-file .devcontainer/.env.example config`
- Confirmed the rendered compose config no longer contains a host `ports:` publish block.
- `git diff --check`

