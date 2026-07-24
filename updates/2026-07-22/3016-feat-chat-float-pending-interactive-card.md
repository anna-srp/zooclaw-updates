---
title: 交互卡片浮动到输入框上方，可边处理边输入
type: 新功能
priority: B
date: 2026-07-22
status: 已合并待发版
pr: 3016
author: bill-srp
url: https://github.com/SerendipityOneInc/ecap-workspace/pull/3016
---

交互卡片浮动到输入框上方，可边处理边输入

## Linear
<!-- 建议（非必填）：完整 Linear URL -->
_None yet — can be linked when an issue is filed._

## Summary

Move **pending** interactive card-kit cards (`buttons` / `select`) out of the scrolling message list and **float them above the live input composer** — the way Claude Code surfaces an interactive prompt near its input. The composer stays usable (non-blocking): you can click a card action **or** keep typing. Once a card is answered, the server-produced completion **`banner`** renders inline in the transcript as history. Replay is unchanged (cards stay inline, read-only).

This reverses today
