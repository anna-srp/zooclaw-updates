---
title: "侧边栏「私信」改名为「历史会话」并优化位置"
type: "体验优化"
priority: "中"
date: "2026-06-11"
status: "待审核"
channels: ""
---

# 侧边栏「私信」改名为「历史会话」并优化位置

## 核心宣传点
Agent 侧边栏的「Direct Message」入口更名为「Session History（历史会话）」，更准确表达指向该 Agent 的历史聊天，并移动到「新建对话」下方，找历史更直观。

## 原始内容
```
fix(sidenav): Direct Message 改名为 Session History 并把选中态从 agent 行挪到子入口 (#2371)

## 概述
  修正 agent 侧边栏 accordion 里"会话入口"的三个 UX 问题：文案含糊、位置不直观、选中态贴错了对象。

  ## 改动清单
  1. **改名 + 调位置**
- 把 "Direct Message" 入口改名为 "Session History"，更准确地表达它指向"这个 agent
此前的（legacy 单
  session）历史聊天"。
- 从原本的第一项挪到 `+ New chat` 下方——优先级上 "+ New chat" 是动作（更主），Session History
是去向（更次）。
- 同步更新：i18n key `chat.directMessage` → `chat.sessionHistory`；testid
`nav-agent-direct-message-*` →
  `nav-agent-session-history-*`。

  2. **删掉 "No past sessions" 空状态**
     - 原文案与 Session History 入口的语义冲突：入口本身就承载着"这个 agent 有 legacy
  历史可去看"，再下面挂一行"无会话"会让人误以为没历史。
     - 干掉了空状态 `<p>` 渲染和 `chat.noPastSessions` i18n key。
- 已知限制：理想情况是"真的没有任何 chat 时才显示 'No past sessions'"，但
`useAgentConversations` 只返回新
multi-session 列表，无法判断 legacy 单 session 是否有数据；条件渲染需要后端补一个"this agent has
any chat history"的
   hint，到时再开 PR 加回来。

  3. **选中态归位**
- 之前 agent row 在 `/chat?agent_id=<id>` 或
`/chat/<computer>/<agent>/<session>` 路由下整行高亮——但 accordion
  模式下，agent row 只是 expand/collapse 触发器，不是导航目标，"被选中"概念应该落在真正的子入口上。
     - **Session History**：URL 是 `/chat?agent_id=<id>` 时高亮。
     - **session 条目**：URL 是 `/chat/<computer>/<agent>/<session>` 时该条目高亮。
     - **Agent row**：accordion 模式下不再有 selected 态；legacy
  模式（`useLegacyChatVersion=true`）下保留原行为，不破坏旧版用户。

  ## 涉及文件
- `web/app/src/components/sidenav/SideNavAgentList.tsx` — 5 行（accordion
模式下关掉 agent row 的 `isActive`）。
- `web/app/src/components/sidenav/SideNavAgentSessions.tsx` —
主要改动（rename + reorder + 空状态删除 + URL-derived
  active state）。
  - `web/app/src/locales/en.ts` — 替换 i18n key。
-
`web/app/tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx`
— 跟随更新 mock、翻转顺序断言、新增 3
  条 active state 测试。

  ## 验证
- [x] `/chat?agent_id=<id>` 展开对应 agent → Session History 灰底高亮、agent row
无高亮。
  - [x] `/new-chat` 展开任一 agent → Session History 无高亮、agent row 无高亮。
- [x] 点击 Session History → 路由跳到 `/chat?agent_id=<id>`，legacy 单 session
历史正常加载。
- [x] 单测覆盖三种 active state：路由匹配时 Session History 高亮、其它 agent 不高亮、session
条目按 session_id
  匹配高亮。
  - [ ] 等 CI `code-quality / lint-and-test` 跑过 lint 
<img width="3008" height="1562" alt="screenshot-20260611-173104"
src="https://github.com/user-attachments/assets/bdb1c22c-64dd-4091-aace-23d7e86a0302"
/>
+ tsc + 单测。

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

--- PR Description ---

## 概述
  修正 agent 侧边栏 accordion 里"会话入口"的三个 UX 问题：文案含糊、位置不直观、选中态贴错了对象。

  ## 改动清单
  1. **改名 + 调位置**
     - 把 "Direct Message" 入口改名为 "Session History"，更准确地表达它指向"这个 agent 此前的（legacy 单
  session）历史聊天"。
     - 从原本的第一项挪到 `+ New chat` 下方——优先级上 "+ New chat" 是动作（更主），Session History 是去向（更次）。
     - 同步更新：i18n key `chat.directMessage` → `chat.sessionHistory`；testid `nav-agent-direct-message-*` →
  `nav-agent-session-history-*`。

  2. **删掉 "No past sessions" 空状态**
     - 原文案与 Session History 入口的语义冲突：入口本身就承载着"这个 agent 有 legacy
  历史可去看"，再下面挂一行"无会话"会让人误以为没历史。
     - 干掉了空状态 `<p>` 渲染和 `chat.noPastSessions` i18n key。
     - 已知限制：理想情况是"真的没有任何 chat 时才显示 'No past sessions'"，但 `useAgentConversations` 只返回新
  multi-session 列表，无法判断 legacy 单 session 是否有数据；条件渲染需要后端补一个"this agent has any chat history"的
   hint，到时再开 PR 加回来。

  3. **选中态归位**
     - 之前 agent row 在 `/chat?agent_id=<id>` 或 `/chat/<computer>/<agent>/<session>` 路由下整行高亮——但 accordion
  模式下，agent row 只是 expand/collapse 触发器，不是导航目标，"被选中"概念应该落在真正的子入口上。
     - **Session History**：URL 是 `/chat?agent_id=<id>` 时高亮。
     - **session 条目**：URL 是 `/chat/<computer>/<agent>/<session>` 时该条目高亮。
     - **Agent row**：accordion 模式下不再有 selected 态；legacy
  模式（`useLegacyChatVersion=true`）下保留原行为，不破坏旧版用户。

  ## 涉及文件
  - `web/app/src/components/sidenav/SideNavAgentList.tsx` — 5 行（accordion 模式下关掉 agent row 的 `isActive`）。
  - `web/app/src/components/sidenav/SideNavAgentSessions.tsx` — 主要改动（rename + reorder + 空状态删除 + URL-derived
  active state）。
  - `web/app/src/locales/en.ts` — 替换 i18n key。
  - `web/app/tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx` — 跟随更新 mock、翻转顺序断言、新增 3
  条 active state 测试。

  ## 验证
  - [x] `/chat?agent_id=<id>` 展开对应 agent → Session History 灰底高亮、agent row 无高亮。
  - [x] `/new-chat` 展开任一 agent → Session History 无高亮、agent row 无高亮。
  - [x] 点击 Session History → 路由跳到 `/chat?agent_id=<id>`，legacy 单 session 历史正常加载。
  - [x] 单测覆盖三种 active state：路由匹配时 Session History 高亮、其它 agent 不高亮、session 条目按 session_id
  匹配高亮。
  - [ ] 等 CI `code-quality / lint-and-test` 跑过 lint 
<img width="3008" height="1562" alt="screenshot-20260611-173104" src="https://github.com/user-attachments/assets/bdb1c22c-64dd-4091-aace-23d7e86a0302" />
+ tsc + 单测。
```
