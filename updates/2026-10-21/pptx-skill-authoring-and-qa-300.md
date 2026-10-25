---
title: "PPT 技能提速：直接写数据生成，并能锁定页数、杜绝表格溢出"
type: "Skill 上架/更新"
priority: "中"
date: "2026-10-21"
status: "待审核"
channels: ""
---

# PPT 技能提速：直接写数据生成，并能锁定页数、杜绝表格溢出

## 核心宣传点

此前生成 PPT 要反复读一大包参考文档、再写程序把幻灯片数据序列化出来，既慢又容易在最终质检时放过多出来的一页或渲染后撑出页脚的表格。本次把技能拆成精简入口加按路线加载的参考文档，Agent 直接写 JSON 数据，校验命令原子产出规范契约，输入非法时保留原有产物不被覆盖；质检只返回紧凑的结论摘要，并修复了封面标签在浅色底上的前景色。新增可选的「精确页数」要求，构建前和成品 PPTX 都会校验；表格按内容计算行高，渲染溢出或原始表格文字被裁切会直接拦截，而不是偷偷丢单元格、缩字号或加页。

## 分级

- 内部：P2
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- SHA: `61c4cd3650797690dab0732a30085a9e47c99cf4`
- PR: #300
- 作者：kaka-srp
- 日期：2026-10-21T11:42:29Z

### Commit Message

```
fix(pptx): streamline authoring and validate final deck constraints (#300)

PPT authoring spent repeated model turns reading a large reference
bundle and generating programs just to serialize slide data. Final QA
could also accept an extra page or a table that expanded beyond the
footer after rendering.

This change:

- Splits the skill into a compact entrypoint and route-specific
references. Agents write JSON data directly; `validate-spec --out`
atomically produces a canonical contract while preserving an existing
output on invalid input.
- Returns a compact QA decision summary, clarifies attachment
publication, and fixes the shared cover-label foreground against its
existing light chips.
- Adds optional `requirements.exact_slide_count`, checked before build
and against the final PPTX. Sizes raw table rows according to their
content and blocks rendered table overflow or clipped raw-table text
without discarding cells, shrinking text or adding pages.

Table evidence comes from the PDF already produced by LibreOffice, using
Poppler's `pdftotext`. Extraction failure preserves PNG previews and
blocks only decks that need table evidence. Grouped native tables are
detected recursively and explicitly blocked until ungrouped;
group-coordinate solving is outside this change.

Validation:

- Final full local PPT suite: **443 passed** (170.87 s), including four
header regressions added during PR review. Repository skill lint passed
with nine existing warnings; `git diff --check` and Node syntax
validation passed.
- Real raw and template builds with LibreOffice/Poppler; the current
synthetic fixture has exactly 14 pages and passes the count/table gates.
Replaying the prior synthetic artifact now rejects table defects on
slides 8, 13 and 14.
- Uneven CJK rows fit with all cells, the same 9.5-point font and one
page. An impossible table remains rejected with its data/font/page count
preserved.
- Independent Astra review completed; both reported boundary issues were
fixed and re-reviewed, including six independently rerun closure cases.

PR review identified a real header omission: the initial check could
pass a clipped template header, and raw headers used duplicated
shrinking overlays. The fix uses native raw header cells at 9.5pt,
includes their text in the row-height budget, and checks rendered header
completeness in both modes. All raw cells enter the completeness count;
matching legacy header overlays remain compatible. Before the patch,
three of four new real-render cases failed; after it, all four and the
full 443-test suite passed. Astra independently reran the four cases,
confirmed that the original clipped template now reports 163 missing
header characters, and found no further mandatory issue.

The existing skill CI selector does not register the PPT suite, so the
443-test result is local evidence, not a claim that CI runs it. Earlier
real Sonnet 4.6/medium trials verified authoring/build/publication
plumbing but did **not** establish faster delivery at equal quality. The
latest deterministic fixes have not had another paid model trial. No
skill publication, production rollout or existing Agent config update is
included.

---------

Co-authored-by: sharplee-srp <sharplee@srp.one>
```

