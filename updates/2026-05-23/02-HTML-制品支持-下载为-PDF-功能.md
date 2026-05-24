---
title: "HTML 制品支持「下载为 PDF」功能"
type: "新功能上线"
priority: "中"
date: "2026-05-23"
status: "待审核"
channels: ""
---

# HTML 制品支持「下载为 PDF」功能

## 核心宣传点

在 ZooClaw 网页端预览 HTML 制品时，可直接一键将其转换并下载为 PDF 文件

## 原始内容

### Commit: 3279974 — feat(web): split artifact Download into HTML + PDF-via-prompt menu (#1880)

```
feat(web): split artifact Download into HTML + PDF-via-prompt menu (#1880)

## Linear
https://linear.app/srpone/issue/ECA-809/

## Summary
- When previewing an **HTML** artifact, the top-right Download button
now opens a 2-item dropdown:
  1. **Download as HTML** — original behavior (raw blob download)
2. **Download as PDF (send a prompt)** — sends a localized prompt into
the current chat asking the assistant to use headless Chromium to
convert the HTML to PDF
- All other artifact types (PDF, CSV, code, etc.) keep the existing
single Download button
- The share/replay viewer (`/share/<shareId>`) also keeps the single
button — `onSendMessage` is an optional prop, so the dropdown branch is
only enabled where a chat composer exists
- New `artifacts` i18n namespace with 4 keys (`download`,
`downloadAsHtml`, `downloadAsPdfViaPrompt`, `downloadPdfPrompt`)
translated across all 10 locales (en/zh/ja/ko/fr/de/it/es/ar/pt). The
prompt body matches the active UI language at click time
- Implementation uses the existing shadcn `DropdownMenu` primitive
(`@/components/ds/dropdown-menu`) — no new deps, no hand-rolled UI, no
backend changes

## Test plan
- [ ] Open chat, trigger an HTML artifact → toolbar shows Download
button with a chevron; clicking opens a 2-item dropdown styled like
surrounding popovers
- [ ] Click **Download as HTML** → file saves (existing behavior
unchanged)
- [ ] Click **Download as PDF (send a prompt)** → localized prompt
appears as a sent message in the chat; assistant begins responding
- [ ] Switch UI language (e.g. EN → ZH) → both menu labels and the sent
prompt body switch to that locale
- [ ] Open a non-HTML artifact (PDF, CSV, code) → toolbar shows the
original single Download button (no dropdown)
- [ ] Open `/share/<shareId>` on an HTML artifact → toolbar shows the
original single Download button (no PDF option, since there's no chat to
send into)

---------

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

### PR #1880 描述

## Linear
https://linear.app/srpone/issue/ECA-809/

## Summary
- When previewing an **HTML** artifact, the top-right Download button now opens a 2-item dropdown:
  1. **Download as HTML** — original behavior (raw blob download)
  2. **Download as PDF (send a prompt)** — sends a localized prompt into the current chat asking the assistant to use headless Chromium to convert the HTML to PDF
- All other artifact types (PDF, CSV, code, etc.) keep the existing single Download button
- The share/replay viewer (`/share/<shareId>`) also keeps the single button — `onSendMessage` is an optional prop, so the dropdown branch is only enabled where a chat composer exists
- New `artifacts` i18n namespace with 4 keys (`download`, `downloadAsHtml`, `downloadAsPdfViaPrompt`, `downloadPdfPrompt`) translated across all 10 locales (en/zh/ja/ko/fr/de/it/es/ar/pt). The prompt body matches the active UI language at click time
- Implementation uses the existing shadcn `DropdownMenu` primitive (`@/components/ds/dropdown-menu`) — no new deps, no hand-rolled UI, no backend changes

## Test plan
- [ ] Open chat, trigger an HTML artifact → toolbar shows Download button with a chevron; clicking opens a 2-item dropdown styled like surrounding popovers
- [ ] Click **Download as HTML** → file saves (existing behavior unchanged)
- [ ] Click **Download as PDF (send a prompt)** → localized prompt appears as a sent message in the chat; assistant begins responding
- [ ] Switch UI language (e.g. EN → ZH) → both menu labels and the sent prompt body switch to that locale
- [ ] Open a non-HTML artifact (PDF, CSV, code) → toolbar shows the original single Download button (no dropdown)
- [ ] Open `/share/<shareId>` on an HTML artifact → toolbar shows the original single Download button (no PDF option, since there's no chat to send into)
