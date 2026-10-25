---
title: "修复：模型选择器和消息状态行的字母下半部分被切掉"
type: "Bug Fix"
priority: "低"
date: "2026-10-16"
status: "待审核"
channels: ""
---

# 修复：模型选择器和消息状态行的字母下半部分被切掉

## 核心宣传点

聊天界面里 g/p/y/q/j 这类带下伸笔画的字母底部会被裁掉，典型现象是模型名「Gemini 4 Argon」和发送消息下方的状态行「Thinking」「Using web_search」看起来缺一截。根因是这些容器用了 text-xs 搭配 leading-none（12px 文字配 12px 行高），而标签本身为了省略号截断开启了 overflow hidden，Inter 字体的字形高度超过 1.0em，超出部分直接被裁切。现在改为 leading-4（16px 行高）。模型选择器触发器固定 h-8、列表项 min-h-8，布局不受影响。

## 分级

- 内部：P3
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `77b995c967b49b584f66a02fc269a2bb021e2125`
- PR: #4076
- 作者：Nemo Feng
- 日期：2026-10-16T06:22:20Z

### Commit Message

```
fix(chat-ui): stop clipping descenders in model picker and turn status labels (#4076)

## Summary
Fix chat-ui text that cut off the bottom of descender letters
(`g`/`p`/`y`/`q`/`j`):
- **Model picker** — composer trigger and dropdown rows (e.g. "Gemini 4
Ar**g**on"). `DropdownMenuModelTrigger` / `DropdownMenuModelItem`:
`leading-none` → `leading-4`.
- **User-message turn status** — the status line under a sent message
(e.g. "Thinkin**g**", "Usin**g** web_search"). `UserMessage.tsx` status
row: `leading-none` → `leading-4`.

## Root cause
Both places set `text-xs leading-none` (a 12px line box for 12px text)
on a container whose label clips overflow for ellipsis truncation
(`truncate` / `overflow-hidden text-ellipsis`). Inter's glyph extent
exceeds 1.0em, so descenders render below the 12px box and are clipped
by `overflow: hidden`. `leading-4` gives a 16px line box.

Layout impact:
- Model picker: none — trigger is fixed `h-8`, items are `min-h-8` with
`py-1.5` (12 + 16 = 28 < 32), both `items-center`. Badges keep their own
`leading-none`.
- Turn status: the row has no fixed height, so it grows 12px → 16px (4px
taller line under the message).

A repo-wide sweep for the same pattern (tight line-height + clipping)
found these two plus one marketing-page case (landing rotating role
word, ~0.8px at 52px), which is intentionally left out of this PR. Other
matches (emoji avatars, 1.25-ratio menu rows, badges, display headings)
were measured and do not clip.

## Test plan
- [x] Standalone Chromium repro using the deployed production CSS bundle
+ Inter, exact class strings from source, old vs new; glyph ink measured
against the clip box:
- Model picker, `leading-none`: label `clientHeight` 12 / `scrollHeight`
13 → clipped; `leading-4`: 16 / 16 → not clipped, row/trigger height
unchanged at 32px
- Turn status ("Thinking", "Using web_search", "Failed: typing
pipeline"), `leading-none`: descenders overflow the 12px box by 1px;
`leading-4`: 1px clearance in a 16px box
- [x] `@zooclaw/chat-ui`: vitest (536 passed), eslint, tsc
- [x] `web/app` `OpenClawUserMessage.unit.spec.tsx` (31 passed)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
```

