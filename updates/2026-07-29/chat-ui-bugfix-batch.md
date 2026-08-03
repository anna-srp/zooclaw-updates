---
title: "聊天界面 5 个用户报告 Bug 批量修复：换行丢失、头像不一致、我的上传为空等"
type: "Bug Fix"
priority: "中"
外部: "B"
date: "2026-07-29"
status: "待审核"
channels: ""
---

## 核心宣传点

一次性修复了 5 个用户反馈的聊天界面问题：多行消息第二行起换行丢失、同一 Agent 侧边栏与聊天头部头像不一致、聊天里发的附件不出现在「我的上传」、会话历史与文件面板等相关显示问题，聊天体验更完整。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- commit：d35d218001ef2ad4604cca888b6875822d1978a6
- PR：#3100
- 日期：2026-07-29T03:30:28Z

### Commit message

```
fix(web): chat UI bug-fix batch (line breaks, avatars, my-uploads, session history, files panel) (#3100)

## 背景

聊天界面 5 个用户报告的 bug,每项一个独立 commit(附回归测试),可整体快速合入:

| Commit | 修复 | 根因 |
|--------|------|------|
| 换行丢失 | 多行消息发出后"第二个及以后的换行"消失 | `globals.css` 历史规则 `.prose br + br {
display:none }`(ECA-420)——CSS `+` 选择器无视文字节点,把有内容间隔的 `<br>` 也隐藏了。改为在 HTML
管线中只折叠**真正相邻**的 `<br>` 连排,保留 ECA-420 意图 |
| 头像不一致 | 同一 agent 侧边栏显示 🤖、chat 头部显示默认 Assistant 头像 | 头部/气泡的解析链从不读
workspace `avatar_url`;现收敛为共享 `resolveAssistantAvatarPresentation` + 新
`AgentAvatar` 组件,侧边栏/头部/气泡统一,非主 agent 兜底 🤖 |
| 我的上传为空 | 聊天里发的附件不出现在「我的上传」面板 | MM 上传路径用自拼 session key 记录资产,与面板查询的规范
key(`computer:<cid>:<agent>`)不匹配;改用同一 sessionKey,附防重测试(历史错 key
数据不迁移,新上传生效) |
| Session History 冗余 | 零 session 的新 agent 也显示 Session History 入口 |
加载完成且列表为空时整块隐藏(加载中也不显示避免闪烁;错误态保留兜底入口) |
| 文件面板无法关闭 | 右侧文件面板只能从页头图标关 | 面板右上角新增关闭按钮,与页头 Files 图标共用同一状态源 |

## 测试

- 每项均带单测(换行含截图原文 CJK 回归用例;头像 +13 例;上传防重 fail-then-retry 用例)
- 分支独立校验:guards + 全量 tsc + eslint 全绿;关键 spec 组 vitest 全绿
- 全部 22 个 commit 合并态下曾整树校验:543 文件 / 7381 测试全绿

## 部署注意

- 纯前端;「我的上传」的资源库按-agent 筛选完整生效还需后端 PR(greeting/上传/头像后端三合一)配合发版
- 另有两个堆叠 PR(消息流布局 UX、输入区 UX)以本分支为 base,先合本 PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR body

## 背景

聊天界面 5 个用户报告的 bug,每项一个独立 commit(附回归测试),可整体快速合入:

| Commit | 修复 | 根因 |
|--------|------|------|
| 换行丢失 | 多行消息发出后"第二个及以后的换行"消失 | `globals.css` 历史规则 `.prose br + br { display:none }`(ECA-420)——CSS `+` 选择器无视文字节点,把有内容间隔的 `<br>` 也隐藏了。改为在 HTML 管线中只折叠**真正相邻**的 `<br>` 连排,保留 ECA-420 意图 |
| 头像不一致 | 同一 agent 侧边栏显示 🤖、chat 头部显示默认 Assistant 头像 | 头部/气泡的解析链从不读 workspace `avatar_url`;现收敛为共享 `resolveAssistantAvatarPresentation` + 新 `AgentAvatar` 组件,侧边栏/头部/气泡统一,非主 agent 兜底 🤖 |
| 我的上传为空 | 聊天里发的附件不出现在「我的上传」面板 | MM 上传路径用自拼 session key 记录资产,与面板查询的规范 key(`computer:<cid>:<agent>`)不匹配;改用同一 sessionKey,附防重测试(历史错 key 数据不迁移,新上传生效) |
| Session History 冗余 | 零 session 的新 agent 也显示 Session History 入口 | 加载完成且列表为空时整块隐藏(加载中也不显示避免闪烁;错误态保留兜底入口) |
| 文件面板无法关闭 | 右侧文件面板只能从页头图标关 | 面板右上角新增关闭按钮,与页头 Files 图标共用同一状态源 |

## 测试

- 每项均带单测(换行含截图原文 CJK 回归用例;头像 +13 例;上传防重 fail-then-retry 用例)
- 分支独立校验:guards + 全量 tsc + eslint 全绿;关键 spec 组 vitest 全绿
- 全部 22 个 commit 合并态下曾整树校验:543 文件 / 7381 测试全绿

## 部署注意

- 纯前端;「我的上传」的资源库按-agent 筛选完整生效还需后端 PR(greeting/上传/头像后端三合一)配合发版
- 另有两个堆叠 PR(消息流布局 UX、输入区 UX)以本分支为 base,先合本 PR

🤖 Generated with [Claude Code](https://claude.com/claude-code)

