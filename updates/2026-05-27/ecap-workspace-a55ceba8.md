---
title: "聊天界面新增快捷命令操作"
type: "新功能上线"
priority: "高"
date: "2026-05-27"
status: "待审核"
channels: ""
---

# 聊天界面新增快捷命令操作

## 核心宣传点

聊天时可以使用快捷命令快速执行常用操作，让与 Agent 的交互更加高效便捷。

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**SHA**: [a55ceba8](https://github.com/SerendipityOneInc/ecap-workspace/commit/a55ceba85219c8ab726c77eeeed8cd96abd3da1e)
**PR**: [#1945](https://github.com/SerendipityOneInc/ecap-workspace/pull/1945)  
**作者**: vincent-srp  
**日期**: 2026-05-27T07:32:39Z

**Commit Message:**

```
feat(chat): add quick command actions (#1945)

## Linear

https://linear.app/srpone/issue/ECA-711/zooclaw-web-agent-new-chat-体验完善可配置快捷指令区-specialist-开场选项

## Summary
- Add configurable quick-start commands for agent chat using official
catalog quick_commands.
- Wire Start a new chat and Summarize and continue to clean /new and
/compact sends without attachments or extra characters.
- Polish quick action labels, selected state, tooltips, and localized
defaults across supported locales.
- Cover main and soulmate quick-command cases plus control-command
behavior in unit tests.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [x] git diff --check

Note: pnpm --dir web run tsc currently fails before typechecking because
the workspace script passes --if-present to pnpm exec, which pnpm
rejects as an unknown option. The app-level tsc command above passed.
```


**PR Description:**

## Linear
https://linear.app/srpone/issue/ECA-711/zooclaw-web-agent-new-chat-体验完善可配置快捷指令区-specialist-开场选项

## Summary
- Add configurable quick-start commands for agent chat using official catalog quick_commands.
- Wire Start a new chat and Summarize and continue to clean /new and /compact sends without attachments or extra characters.
- Polish quick action labels, selected state, tooltips, and localized defaults across supported locales.
- Cover main and soulmate quick-command cases plus control-command behavior in unit tests.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [x] git diff --check

Note: pnpm --dir web run tsc currently fails before typechecking because the workspace script passes --if-present to pnpm exec, which pnpm rejects as an unknown option. The app-level tsc command above passed.
