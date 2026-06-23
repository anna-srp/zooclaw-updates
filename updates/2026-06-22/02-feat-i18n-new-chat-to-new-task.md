---
title: "侧边栏「New Chat / 新对话」按钮统一改名为「New Task / 新任务」"
type: "体验优化"
priority: "中"
date: "2026-06-22"
status: "待审核"
channels: "Discord + changelog"
---
# 侧边栏「New Chat / 新对话」按钮统一改名为「New Task / 新任务」
## 核心宣传点
侧边栏顶部和每个智能体下方的「新建对话」按钮，文案从「New Chat / 新对话」统一改为「New Task / 新任务」，全部 11 种语言同步更新，更贴合「让智能体帮你完成任务」的产品定位。
## 原始内容
feat(i18n): rename "New Chat" to "New Task" across locales (#2555)

## What

Renames the sidebar "new conversation" buttons from **New Chat** to **New Task**:

- Top sidebar button `nav.newChat` → "New Task" (translated across all 11 locales)
- Per-agent button `chat.newChat` → "New task" (en only; other locales inherit via the English fallback in `LanguageContext`)

## Why

Product terminology shift from "Chat" to "Task" for the primary new-conversation actions.

## Locale values

| Locale | Before (nav) | After (nav) |
|---|---|---|
| en | New Chat | New Task |
| zh | 新对话 | 新任务 |
| ja | 新しいチャット | 新しいタスク |
| ko | 새 채팅 | 새 작업 |
| de | Neuer Chat | Neue Aufgabe |
| es | Nuevo chat | Nueva tarea |
| fr | Nouvelle discussion | Nouvelle tâche |
| it | Nuova chat | Nuova attività |
| pt | Novo chat | Nova tarefa |
| ar | محادثة جديدة | مهمة جديدة |

## Scope notes

- Only the two highlighted buttons changed. The in-chat composer action `chat.clearContext` ("Start a new chat") and the `chat.newChatFailed` toast were intentionally left untouched.
- `chat.newChat` is only defined in `en.ts`; `t()` deep-walks the active locale and falls back to English for missing keys, so editing `en.ts` updates that button for all languages.
