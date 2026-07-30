---
title: "聊天输入区 5 项体验优化：最近文件更全、附件图标更清晰、引用截断不再劈开表情"
type: "体验优化"
priority: "中"
date: "2026-07-29"
status: "待审核"
channels: ""
---

## 核心宣传点

聊天输入框一次性优化了 5 处细节——「最近文件」从 2 条放宽到 8 条并支持滚动、非图片附件补齐彩色类型图标、引用预览与实发内容统一为 200 字且按码点截断不再劈开 emoji/中文、流式回复时抑制误触发送等，日常输入更顺手。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- commit：d07a23a65a94728a74bbe37200a3147dcb2b3052
- PR：#3102
- 日期：2026-07-29T09:56:15Z

### Commit message

```
feat(web): chat composer UX improvements (#3102)

## 背景

聊天输入区 5 项交互优化,每项一个 commit。**堆叠 PR:base 是 `fix/chat-ui-bugfixes`(bug
修复批次),请先合那个;合入后本 PR 会自动 retarget 到 main。**

| Commit | 优化 |
|--------|------|
| 最近文件 | "最近文件"菜单从 `slice(0,2)` 放宽到 8 条,子菜单内滚动(复用 SkillsSubMenu
同款模式),"从资源库添加"固定可见 |
| 附件类型图标 | 附件芯片非图片文件补上彩色类型图标(映射 `composer-file-type-icons.ts`
已存在,此前只有"最近文件"菜单在用);两种 presentation 都覆盖;复核纠正一处 token 选择(`bg-card` 而非
`bg-background`,避免 light 模式角标消失) |
| 引用截断 | 引用回复预览 150 字 vs 实发 200 字的"所见非所发"统一为共享常量 200,并改为按码点截断(不劈开
emoji/CJK) |
| Enter 抑制 | 流式回复期间按 Enter 不再静默插入换行(preventDefault 吞掉);Shift+Enter
保留;IME 组合确认路径逐行核验不受影响 |
| launcher 缩略图 | new-chat 页选的图片立即显示缩略图(object URL,创建/移除/发送/卸载全路径 revoke
无泄漏),消除进入会话后附件"变身"的断层 |

> 注:引用截断 commit 在源分支曾因并发暂存竞态挂错 message,cherry-pick 时已更正,内容不变。

## 测试

- app 侧相关 spec 187/187 绿;`@zooclaw/chat-ui` 包内 317/317 绿;push 时
fast-tier(guards + tsc + eslint)通过
- 合并态整树校验曾全绿(543 文件 / 7381 测试)

## 部署注意

纯前端。与消息流 UX PR、控制台 UX PR 相互独立,可并行 review。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR body

## 背景

聊天输入区 5 项交互优化,每项一个 commit。**堆叠 PR:base 是 `fix/chat-ui-bugfixes`(bug 修复批次),请先合那个;合入后本 PR 会自动 retarget 到 main。**

| Commit | 优化 |
|--------|------|
| 最近文件 | "最近文件"菜单从 `slice(0,2)` 放宽到 8 条,子菜单内滚动(复用 SkillsSubMenu 同款模式),"从资源库添加"固定可见 |
| 附件类型图标 | 附件芯片非图片文件补上彩色类型图标(映射 `composer-file-type-icons.ts` 已存在,此前只有"最近文件"菜单在用);两种 presentation 都覆盖;复核纠正一处 token 选择(`bg-card` 而非 `bg-background`,避免 light 模式角标消失) |
| 引用截断 | 引用回复预览 150 字 vs 实发 200 字的"所见非所发"统一为共享常量 200,并改为按码点截断(不劈开 emoji/CJK) |
| Enter 抑制 | 流式回复期间按 Enter 不再静默插入换行(preventDefault 吞掉);Shift+Enter 保留;IME 组合确认路径逐行核验不受影响 |
| launcher 缩略图 | new-chat 页选的图片立即显示缩略图(object URL,创建/移除/发送/卸载全路径 revoke 无泄漏),消除进入会话后附件"变身"的断层 |

> 注:引用截断 commit 在源分支曾因并发暂存竞态挂错 message,cherry-pick 时已更正,内容不变。

## 测试

- app 侧相关 spec 187/187 绿;`@zooclaw/chat-ui` 包内 317/317 绿;push 时 fast-tier(guards + tsc + eslint)通过
- 合并态整树校验曾全绿(543 文件 / 7381 测试)

## 部署注意

纯前端。与消息流 UX PR、控制台 UX PR 相互独立,可并行 review。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

