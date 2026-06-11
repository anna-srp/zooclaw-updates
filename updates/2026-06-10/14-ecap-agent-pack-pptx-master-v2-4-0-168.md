---
title: "PPT Master 升级 v2.4.0：故事板预览 + 动效修复 + 质量门禁"
type: "Skill 上架/更新"
priority: "中"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# PPT Master 升级 v2.4.0：故事板预览 + 动效修复 + 质量门禁

## 核心宣传点
PPT Master 技能升级：开工前先给你看故事板让你确认故事线，动效真正能动起来（滚动渐入、翻页级联），并新增多道质量门禁拦截丑陋排版，做出的 PPT 更专业、更符合预期。

## 原始内容
```
pptx-master v2.4.0: 工作流专业化重排 + 视觉执行硬门禁 + 动效修复 (#168)

* refactor(pptx-master): slim design-engine SKILL.md to process + control points (387→155)

All §1.x value tables already live in references/judgment.yaml (the declared
single source); SKILL.md now keeps only the decision flow, per-dimension
question + validation check + YAML lookup path. Section anchors §1.0-§1.6
preserved (cross-referenced pack-wide). Tests 73+36+16 green.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* refactor(pptx-master): slim design-system SKILL.md to lookup index (248→72)

All value tables (palettes, proportion models, hue refinement, OKLCH, WCAG,
red lines, overrides) already live in references/design-tokens.yaml; SKILL.md
is now a lookup index + the override-precedence process rule. Tests green.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* refactor(pptx-master): slim brand-system SKILL.md (432→139), extract references/brand-import.md

Fetch code, DESIGN.md format spec, theme extraction, conversion code and
font-substitution tables move to references/brand-import.md (loaded only when
importing). SKILL.md keeps activation flow, lock semantics (§6 anchor preserved
— cited by validation.yaml), persistence, interaction patterns.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* refactor(pptx-master): re-center AGENTS.md on flow + Visual Quality Contract (240→120)

Tables mirrored verbatim from routing.yaml (Path-B matrix, motion, pptx
conversion, commands) become pointers — routing.yaml is the single lookup
source per its own contract. New compact Visual Quality Contract section
surfaces the 7 aesthetic control points that were previously scattered.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* feat(pptx-master): enforce restraint decoration ceiling in the delivery gate

validate_dna.py --delivery now resolves the DNA's audience restraint to its
tier via judgment.yaml; a minimalist tier rejects gradients/shadows found in
slide <section> content (shell chrome exempt). Closes the 'DNA declares
minimalism, deck ships gradients' execution gap. test_dna 16→21, all green.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* feat(pptx-master): deck structure linter — assembly rules become mechanical

New output-html/scripts/lint_deck.py (stdlib+yaml, exit 0/1/2): R1 adjacent
same-type blocks, R2 accent <=3/page (design-tokens hue_refinement), R3
declared content_relationship must be structurally present (vs DNA), R4 no
readable text <12px (ghost exempt). Build contract: pipeline step_4 stamps
<section data-block> (assembly_rules.ar8); unstamped block decks fail.
Registered as blocking L2-DECK-LINT + unified_checklist 8c. tests/test_lint.py
11 cases; full suite 73+36+21+11 green.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* feat(pptx-master): render-based Design Critic — score the pixels, not the source

New design-engine/scripts/render_critic.py: headless-renders the deck
(playwright→selenium fallback, exit-2 degrade), screenshots every slide to
artifacts/critic/slide-NN.png + index.json, and mechanically flags content
overflowing the slide box and readable text <12px. critic_loop gains step 1.5
(render) and step 2 now scores by VIEWING the PNGs; unrendered scoring must be
tagged in the delivery summary. Self-test verified end-to-end locally.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* test(pptx-master): e2e gate-chain test — AGENTS.md delivery commands run for real

tests/test_e2e.py drives validate_dna.py --delivery and lint_deck.py through
their CLIs against a realistic stamped fixture deck, then proves each gate
fails on targeted mutations: off-palette color, font drift, gradient under
minimalist restraint, adjacent duplicate blocks, missing relationship
structure, missing DNA artifact. 8/8 green.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* chore(pptx-master): v2.3.0 — wire gates into AGENTS/ARCHITECTURE, registry cleanup, changelog

Delivery gates now read: process gate (DNA + restraint) → structure gate
(lint_deck) → fidelity gate (audit) → render critic. routing.yaml skills
registry gains marp-slides + onboarding (matches the 19-skill map).
tests/README documents 5 suites / 149 cases. Version 2.2.1 → 2.3.0.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* fix(pptx-master): motion chain never fired — ship the runtime the spec promised

data-animation was specified in routing.yaml/animations.yaml/pipeline tables
but consumed NOWHERE: pipeline steps had no motion action and slides-shell.html
had zero animation code. Now: shell ships a <body data-animation={{MOTION}}>
gated .reveal runtime (IntersectionObserver in scroll mode, entrance cascade
per slide-change in present mode, 90ms stagger on rich); hidden state exists
only under JS-set body.anim-ready and exports clone the untagged <template>,
so PPTX/PDF stay full-visibility by construction (+beforeprint/print/reduced-
motion resets). pipeline step_4 mandates filling {{MOTION}} from
motion_level_table[restraint].template_var. Verified end-to-end in headless
Chrome. test_e2e 8→12; suite 153 green.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* feat(pptx-master): Design DNA becomes the run ledger; mirror fidelity legitimizes Path B

The first machine checkpoint used to be Step-5's DNA — everything decided in
steps 1-4 (path, B-mode, image tier, template choice, storyboard) lived only
in conversation context. Now the DNA records it all and validate_dna checks
it: template ∈ templates.yaml (page_purposes length reconciled against the
template's page range ±20%), intake {path, mode, image_tier, scenario}
enum-validated, slide_titles (assertion storyboard) one-per-page.

New fidelity=mirror resolves the spec conflict where B-Mirror/B-strict skip
the judgment chain yet the gate demanded a full DNA — a compliant replica run
had to fabricate judgment fields to deliver. mirror requires only intake +
provenance.template_source and skips font/palette/restraint delivery checks
(the uploaded template owns the look); mirror×intake cross-checked both ways.

test_dna 21→31; suite 73+36+31+11+12 = 163 green.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* feat(pptx-master): lint_deck R5 emoji-as-icon + R6 bullet walls

Two banned-list items had no teeth: emoji inside icon-classed elements now
fails (Heroicons only; emoji in body copy warns), and any list with >4 items
fails (bullet wall). test_lint 11→15; suite 167 green.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* refactor(pptx-master): reorder the SOP — communication before logistics, storyboard sign-off before design

From a presentation-professional audit: intake asked about materials
(template? images?) before purpose; the plan was confirmed before research
existed; the user's first sight of real content was the finished deck; and
no assertion-title discipline existed anywhere.

New 7-step flow: Brief (Turn 2 asks decision/audience/live-vs-read — the
judgment chain's direct inputs; Turn 3 bundles template/materials/images;
template_treatment fires right after any upload) → Information Gathering →
Storyboard (core message → T01-T10 skeleton → one assertion title per slide
→ titles-only test → USER SIGN-OFF; titles lock into the ledger) → Judgment/
Build/Gates → Deliver → Revise → Rehearse. Visual Quality Contract gains #8
assertion titles; unified_checklist 8d. ARCHITECTURE/onboarding/brand-system/
gdoc-import references updated; run_judgment.py scaffolds full/reduced/mirror.

Suite 167 green.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* chore(pptx-master): v2.4.0 — changelog + version bump

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

* fix(pptx-master): escape emoji regex ranges — resolves CodeQL overly-permissive-range alerts

The emoji character class contained a literal non-ASCII range whose start
char had corrupted into U+FFFD, which CodeQL flagged on PR #168. The class
is now a single EMOJI_CLASS constant using backslash-escaped code points
only (U+1F000-1FAFF, U+2600-27BF, U+2B00-2BFF), shared by EMOJI_RE and
ICON_EMOJI_RE. Behavior verified by test_lint R5 cases; suite 167 green.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>

---

### PR Description

## 这个 PR 解决什么问题

PPT Master 此前的核心矛盾：**规矩写了很多，但大部分没有牙齿**。判断链跑没跑有门管（v2.2.x），但"跑了之后做没做到"没人管——声明极简风格却满屏渐变、动效配置齐全却从未渲染、用户在 Turn 3 说过的偏好做着做着就忘了。本 PR 分两个版本（v2.3.0 + v2.4.0）系统性补齐。

## 用户能感知到的变化

### 1. 问的问题变专业了（v2.4.0 工作流重排）
- **以前**：你好 → 有模板吗？→ 要搜图吗？→ 开始做
- **现在**：你好 → **这场演示要让观众做什么决定？观众是谁？现场讲还是发出去看？** → 模板/素材/图片一轮问完 → 开始做
- 沟通要素先于物流问题——这三问正是设计判断的直接输入，以前全靠猜

### 2. 做之前先给你看故事板（新检查点）
出设计之前，先呈现一份故事板：核心主张一句话 + 逐页**断言式标题**（"Q3 营收增长 38%" 而非 "Q3 营收情况"），**你确认后才开始设计**。只读标题就能读完整个故事——改标题比改成品便宜得多。

### 3. 动效真的会动了（修复真 bug）
动效在配置里处处有定义，但模板里压根没有实现代码——打了开关也没人消费。现在 HTML deck 自带动效运行时：滚动渐入、演示模式翻页级联（节制档静态、丰富档带节奏交错），且导出 PPTX/PDF 永远不受影响。已在真实浏览器端到端验证。

### 4. 丑 deck 出不了门了（交付门 2 道 → 3 道 + 渲染自检）
- **克制度硬执行**：给高管/政务做的极简 deck 里出现渐变阴影 → 直接拦下
- **结构门（新）**：相邻两页同版式、强调色滥用（>3 次/页）、emoji 当图标、一页列表超过 4 条、小于 12px 的小字 → 全部机械拦截
- **渲染自检**：Design Critic 现在对每页**截图打分**（看到的=用户看到的），不再凭 HTML 想象

### 5. 全程留痕，长对话不再"飘"
对话里的每个关键决定（走哪条路、模板选了哪个、图片策略、故事板标题）全部落盘到运行台账（design-dna.json），交付门逐项对账。构建按台账执行，不靠模型记忆。

### 6. 顺手修复：上传模板的"复刻模式"不再被误杀
原规范要求复刻模式跳过设计判断、却又要求交付时必有完整判断记录——合规复刻被迫造假过门。新增 `mirror` 模式合法化这条路径。

## 维护者视角

- **文档瘦身**：AGENTS.md 240→128 行、design-engine 387→156、design-system 248→72、brand-system 432→139。所有与 YAML 重复的数据表删除（遵守 pack 自己的 Lookup Contract），MD 只留"流程 + 控制点 + 查表指针"，新增 Visual Quality Contract（8 条美观控制点前置）
- **新脚本**：`lint_deck.py`（结构门，R1-R6）、`render_critic.py`（逐页截图 + 溢出/小字预检，playwright→selenium 降级）
- **测试**：125 → **167 全绿**（test_dna 16→31，新增 test_lint 15 + test_e2e 12，含动效链回归）
- 架构三层（控制器/引擎/能力叶子）与判断链引擎**未动**

## 测试

```
python3 tests/test_pack.py   # 73 ✅
python3 tests/test_extra.py  # 36 ✅
python3 tests/test_dna.py    # 31 ✅
python3 tests/test_lint.py   # 15 ✅
python3 tests/test_e2e.py    # 12 ✅
```

建议合并后在真实 pod 各跑一次 Path A 标准 / fast-track / Path B 复刻，验证新 intake 提问体验与故事板签字环节。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

```
