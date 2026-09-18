---
title: "fix(workspace): 修复 R2 工作台交互并统一资源页面样式 (#3781)"
type: "Bug 修复"
priority: "中"
date: "2026-09-17"
status: "待审核"
channels: ""
---

# fix(workspace): 修复 R2 工作台交互并统一资源页面样式 (#3781)

## 核心宣传点

修好了首页、Agent 工作区和资源页面的一批交互问题：再次进入 Agent 会恢复上次停留的编辑页或任务，Skills 入口与侧边栏目录统一，空任务不再占位。

## PR 说明

## 修改内容

修复 R2 验收中首页、Agent 工作区和资源页面的展示与导航问题。从首页首次进入可编辑 Agent 时打开 Edit Agent 并展示设置面板；再次进入时，按用户和 Agent 恢复浏览器本地记录的编辑页、New Task 或具体任务对话。

- Skills：输入框 Skill Store 与侧边栏 Official Skills 使用同一目录及图标；移除 Use Skills 子菜单中的重复列表，仅保留创建和打开商店入口；去掉商店弹窗上下分割线。
- 首页：最近活动过滤没有实际标题的空任务；Schedule 加载失败使用独立、准确的提示；Agent 卡片缩短、描述限制单行，头像放大并上移至卡片边缘；缩小 Agent Builder 图标。
- Agent 工作区：标题显示当前页面或任务名称；统一侧边栏悬停样式、返回按钮和切换器，优化 Recents 空状态；Artifacts 复用全局页面及空状态，并分别按 workspace ID / runtime agent ID 筛选生成文件和上传文件。
- Schedule 与 Knowledge：移除无关连接状态和重复标题；日历改为浅灰底，修正分割线、按钮及筛选器样式，列表筛选不再影响日历；修复 Agent 日程空状态被其他运行环境状态遮蔽的问题。Knowledge 标题与侧边栏一致，创建弹窗不再导致背景提前显示空的 Unfiled 卡片，移除空状态中的未归档上传入口。
- Tasks 与 Agents：任务整行可进入聊天，保留原生链接行为；去掉 Tasks 顶部 Refresh；新增默认 All 标签，各分类分页独立。Agent 入口记录不覆盖明确指定的任务链接，失效的已记忆任务可回退到 New Task。

- 页面头部：以 Connector 为基准，统一 Agents / Tasks / Artifacts / MCP / Skills / Knowledge，以及 Agent 内的 Artifacts / Schedule / External channels；标题、说明、宽度和留白复用同一组件。Credits 异常提示缩小并改为灰色。补齐本地 mock 的 Agent 详情接口，避免 External channels 请求 undefined。

## 问题原因

Skill Store 仍使用旧目录；首页直接把底层空会话当作活动；资源页复用了带运行环境连接状态的聊天标题组件。Agent 入口缺少本地停留位置记录，工作区与全局页面也存在重复组件及样式差异。

## 验证结果

- [x] 最新提交 `f9255fffb` 的 CI：26 项通过、15 项按条件跳过，无失败或等待项；Claude 与 Codex 对该提交复审均无新增问题。
- [x] 后端任务详情与历史列表定向测试：61 项通过。新增飞书 / Slack 原始标题为空、当前任务不在首批 50 条历史记录中的回归用例；修复前 4 个用例失败，修复后全部通过。
- [x] 后端 ruff、格式检查、Pyright 与 import-linter 全部通过；提交钩子检查通过。

- [x] Agent、Tasks 与首页相关单测：59 个文件、398 项通过（同步最新 main 后重新执行）。
- [x] chat-ui 的 SkillsSubMenu / SkillStoreDialog：20 项通过。
- [x] 本轮已验证 Skills、Knowledge、Artifacts、Schedule 相关定向测试。
- [x] 头部调整后定向测试：40 项通过；资源页、渠道和日程回归：154 项通过（既有 69 项跳过、1 项 todo）。
- [x] 浏览器核对：全局及 Agent 资源页标题均为 16px / 600，桌面顶部留白 24px；Credits 提示 12px；渠道页无 undefined 请求错误。
- [x] 同步最新 Agent 面板改动后，入口和工作区回归：54 个文件、392 项通过，保留面板优化及首次编辑/后续恢复行为。
- [x] TypeScript、ESLint、仓库治理检查、Knip 与 `git diff --check`。
- [x] CI 失败用例在无 Firebase API key 环境复测：7 个文件、250 项通过；补充工作区标题数据透传后，入口记忆与标题相关 34 项通过。
- [x] 浏览器模拟当前任务不在历史分页中：页头仍正确显示任务详情标题；新建任务后立即返回首页也能恢复该任务。

- [x] 本地 mock 浏览器验证：首次进入设置页、恢复 New Task、恢复具体历史对话、重新恢复 Edit Agent；Tasks 整行跳转与 Refresh 移除；All / My agents / Shared with me 分类切换。
- [x] 本地 mock 浏览器验证：Skill Store 目录一致、日程筛选/创建/删除、资源页标题与空状态。
- [x] 浏览器模拟已记忆任务返回 `agent_session.not_found`：自动恢复到 New Task，未停留在错误页面。

## 任务标题与入口一致性

- 前端优先读取当前任务详情标题；后端详情接口复用历史列表的标题补全逻辑。直接打开不在首批历史分页中的飞书 / Slack 任务时，会从首条用户消息补出标题，并沿用外部消息前缀清理规则。已有手动或生成标题保持不变，也不会增加事件查询。
- 回归测试覆盖原始标题为空、任务不在已加载历史页、历史标题过时及已有标题无需补全的情况。
- 新建或切换任务成功后立即保存停留位置（`60e82d971`），避免快速返回首页时仍恢复旧位置。
- 同步 Skill Store 新流程的页面测试，并隔离登录依赖；清理旧查询选项的无用导出，修复 CI 中的单测与静态扫描失败。

## 部署与边界

涉及前端、共享 chat-ui，以及 claw-interface 任务详情的标题补全；接口结构不变。完整修复需要同时部署前端和 claw-interface 后端。staging 上的真实 Schedule 服务请求失败仍取决于后端可用性，本次修正其局部提示和展示。未运行本地完整单测集或生产构建，由 CI 执行对应质量检查。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `9f76a4995c0ff94c6e7b655497eaf04c0f02d57c`
- PR: #3781
- 作者：lynn Zhuang
- 日期：2026-09-17T11:52:25Z

### Commit Message

```
fix(workspace): 修复 R2 工作台交互并统一资源页面样式 (#3781)

## 修改内容

修复 R2 验收中首页、Agent 工作区和资源页面的展示与导航问题。从首页首次进入可编辑 Agent 时打开 Edit Agent
并展示设置面板；再次进入时，按用户和 Agent 恢复浏览器本地记录的编辑页、New Task 或具体任务对话。

- Skills：输入框 Skill Store 与侧边栏 Official Skills 使用同一目录及图标；移除 Use Skills
子菜单中的重复列表，仅保留创建和打开商店入口；去掉商店弹窗上下分割线。
- 首页：最近活动过滤没有实际标题的空任务；Schedule 加载失败使用独立、准确的提示；Agent
卡片缩短、描述限制单行，头像放大并上移至卡片边缘；缩小 Agent Builder 图标。
- Agent 工作区：标题显示当前页面或任务名称；统一侧边栏悬停样式、返回按钮和切换器，优化 Recents 空状态；Artifacts
复用全局页面及空状态，并分别按 workspace ID / runtime agent ID 筛选生成文件和上传文件。
- Schedule 与
Knowledge：移除无关连接状态和重复标题；日历改为浅灰底，修正分割线、按钮及筛选器样式，列表筛选不再影响日历；修复 Agent
日程空状态被其他运行环境状态遮蔽的问题。Knowledge 标题与侧边栏一致，创建弹窗不再导致背景提前显示空的 Unfiled
卡片，移除空状态中的未归档上传入口。
- Tasks 与 Agents：任务整行可进入聊天，保留原生链接行为；去掉 Tasks 顶部 Refresh；新增默认 All
标签，各分类分页独立。Agent 入口记录不覆盖明确指定的任务链接，失效的已记忆任务可回退到 New Task。

- 页面头部：以 Connector 为基准，统一 Agents / Tasks / Artifacts / MCP / Skills /
Knowledge，以及 Agent 内的 Artifacts / Schedule / External
channels；标题、说明、宽度和留白复用同一组件。Credits 异常提示缩小并改为灰色。补齐本地 mock 的 Agent 详情接口，避免
External channels 请求 undefined。

## 问题原因

Skill Store 仍使用旧目录；首页直接把底层空会话当作活动；资源页复用了带运行环境连接状态的聊天标题组件。Agent
入口缺少本地停留位置记录，工作区与全局页面也存在重复组件及样式差异。

## 验证结果

- [x] 最新提交 `f9255fffb` 的 CI：26 项通过、15 项按条件跳过，无失败或等待项
```
