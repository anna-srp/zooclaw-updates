---
title: "Council 最终报告可在页面内直接阅读"
type: "体验优化"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# Council 最终报告可在页面内直接阅读

## 核心宣传点

Council 的完整报告移到 Synthesis 面板的「Full report」标签页里直接渲染，点摘要中的报告卡片即可切换，不用再打开侧边抽屉。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`ce505b8f75f3200b9689e58c0bc98960c8861fa7`
- 作者：bill-srp
- 日期：2026-08-05T11:43:10Z
- PR：#3255

### Commit Message

```
feat(council): synthesis report tab and quoted dispatch settings (#3255)

## Linear
<!-- 无对应 Linear issue：会话内 UX 改进需求 -->

## Summary
- **Final report moves into the Synthesis panel.** When the synthesis
summary carries a stable-host report link, the Synthesis card renders
`Summary` / `Full report` tabs: the Full report tab fetches the artifact
and renders the markdown inline (shared `MarkdownRenderer`), and
clicking the report's file card inside the Summary switches to that tab
— a capture-phase handler intercepts the click before
`MarkdownContent`'s container listener can open the artifact drawer. Any
other file card keeps the drawer behavior, and summaries without a
report link keep the existing single view. (First pass authored by
Codex; click-to-switch refinement applied on top after the Codex runtime
lost write access.)
- **Dispatch message quotes tier and depth.** `/council <topic>` now
sends `tier: "standard"` / `depth: "deep"` so the agent reads the
settings as literal values rather than words continuing the topic. The
council control-reply filter accepts the quoted form too, keeping
manually typed quoted replies out of the synthesis-brief selection.

## Test plan
- [x] `CouncilClient.unit.spec.tsx`: four synthesis-tab cases (tabs
appear with a report link, Full report renders inline with the report
URL, clicking the summary's report card switches tabs without opening
the drawer, no tabs without a link) — click-to-switch written RED-first;
dispatch assertions flipped to the quoted form RED-first
- [x] `thread-messages.unit.spec.ts`: quoted `tier:`/`depth:` control
replies filtered like unquoted ones
- [x] All council suites green (122 tests) + `bash scripts/verify-web.sh
--no-test` (guards + tsc + eslint)
- [x] Browser-verified on a real staging done run via local dev: tabs
render, full report displays inline, summary card click switches tabs
with no drawer
```

### PR Body

## Linear
<!-- 无对应 Linear issue：会话内 UX 改进需求 -->

## Summary
- **Final report moves into the Synthesis panel.** When the synthesis summary carries a stable-host report link, the Synthesis card renders `Summary` / `Full report` tabs: the Full report tab fetches the artifact and renders the markdown inline (shared `MarkdownRenderer`), and clicking the report's file card inside the Summary switches to that tab — a capture-phase handler intercepts the click before `MarkdownContent`'s container listener can open the artifact drawer. Any other file card keeps the drawer behavior, and summaries without a report link keep the existing single view. (First pass authored by Codex; click-to-switch refinement applied on top after the Codex runtime lost write access.)
- **Dispatch message quotes tier and depth.** `/council <topic>` now sends `tier: "standard"` / `depth: "deep"` so the agent reads the settings as literal values rather than words continuing the topic. The council control-reply filter accepts the quoted form too, keeping manually typed quoted replies out of the synthesis-brief selection.

## Test plan
- [x] `CouncilClient.unit.spec.tsx`: four synthesis-tab cases (tabs appear with a report link, Full report renders inline with the report URL, clicking the summary's report card switches tabs without opening the drawer, no tabs without a link) — click-to-switch written RED-first; dispatch assertions flipped to the quoted form RED-first
- [x] `thread-messages.unit.spec.ts`: quoted `tier:`/`depth:` control replies filtered like unquoted ones
- [x] All council suites green (122 tests) + `bash scripts/verify-web.sh --no-test` (guards + tsc + eslint)
- [x] Browser-verified on a real staging done run via local dev: tabs render, full report displays inline, summary card click switches tabs with no drawer

