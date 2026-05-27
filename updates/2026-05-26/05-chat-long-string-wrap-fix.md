---
title: "聊天窗口长字符串显示修复"
type: "Bug Fix"
priority: "中"
date: "2026-05-26"
status: "待审核"
channels: "Discord + changelog"
---
# 聊天窗口长字符串显示修复

## 核心宣传点

当消息中包含超长连续字符（如 base64 编码串）时，聊天气泡不再溢出边框，显示恢复正常。

## 原始内容

**Commit:** 45fa6b7f
**Repo:** ecap-workspace
**Author:** Nemo Feng

**Commit Message:**
```
fix(web): wrap long unbreakable strings in chat markdown content (#1934)

## Problem

Sending a long unbreakable token (e.g. a base64 blob with no spaces)
into the chat made the rendered message bubble overflow horizontally
outside the chatbox.

## Root cause

`MarkdownContent` applied two conflicting values of the same CSS
property — `[overflow-wrap:anywhere]` **and** `break-words`
(`overflow-wrap: break-word`). In Tailwind v4's generated stylesheet,
`.break-words` is emitted after the arbitrary property, so the effective
computed value was `break-word`.

Unlike `anywhere`, `break-word` does **not** introduce soft-wrap
opportunities when computing an element's **min-content width**. So a
long unbreakable string keeps a huge min-content. Combined with the user
bubble's `w-fit` (shrink-to-fit), `fit-content` collapses to the full
string width and the bubble blows past the chat column.

## Fix

Replace the conflicting pair with Tailwind v4's native `wrap-anywhere`
utility (`overflow-wrap: anywhere`) — a single, unambiguous declaration.
`anywhere` reduces min-content, so the bubble wraps within its
container, and it also removes the latent cascade-order fragility.

`wrap-anywhere` over `break-all`: `break-all` (`word-break`) chops every
word mid-character and harms normal/CJK text; `anywhere` only breaks a
word when it would otherwise overflow.

## Verification

Reproduced against the real Tailwind v4 engine with the exact chat DOM
(user + assistant bubbles):

| Check | Before | After |
| --- | --- | --- |
| Computed `overflow-wrap` | `break-word` | `anywhere` |
| User bubble width (820px viewport) | 2892px (overflows) | 649px
(contained) |
| Assistant bubble | contained | contained |
| Short message | hugs content | hugs content |

Confirmed visually: the long string now wraps inside the bubble; short
messages still hug their content.

Linear: https://linear.app/srpone/issue/ECA-820/

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

**PR #1934: fix(web): wrap long unbreakable strings in chat markdown content**

## Problem

Sending a long unbreakable token (e.g. a base64 blob with no spaces) into the chat made the rendered message bubble overflow horizontally outside the chatbox.

## Root cause

`MarkdownContent` applied two conflicting values of the same CSS property — `[overflow-wrap:anywhere]` **and** `break-words` (`overflow-wrap: break-word`). In Tailwind v4's generated stylesheet, `.break-words` is emitted after the arbitrary property, so the effective computed value was `break-word`.

Unlike `anywhere`, `break-word` does **not** introduce soft-wrap opportunities when computing an element's **min-content width**. So a long unbreakable string keeps a huge min-content. Combined with the user bubble's `w-fit` (shrink-to-fit), `fit-content` collapses to the full string width and the bubble blows past the chat column.

## Fix

Replace the conflicting pair with Tailwind v4's native `wrap-anywhere` utility (`overflow-wrap: anywhere`) — a single, unambiguous declaration. `anywhere` reduces min-content, so the bubble wraps within its container, and it also removes the latent cascade-order fragility.

`wrap-anywhere` over `break-all`: `break-all` (`word-break`) chops every word mid-character and harms normal/CJK text; `anywhere` only breaks a word when it would otherwise overflow.

## Verification

Reproduced against the real Tailwind v4 engine with the exact chat DOM (user + assistant bubbles):

| Check | Before | After |
| --- | --- | --- |
| Computed `overflow-wrap` | `break-word` | `anywhere` |
| User bubble width (820px viewport) | 2892px (overflows) | 649px (contained) |
| Assistant bubble | contained | contained |
| Short message | hugs content | hugs content |

Confirmed visually: the long string now wraps inside the bubble; short messages still hug their content.

Linear: https://linear.app/srpone/issue/ECA-820/
