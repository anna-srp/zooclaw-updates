---
title: "任务卡片交互优化：一键带入 Prompt 与 Agent"
type: "体验优化"
priority: "中"
date: "2026-07-31"
status: "待审核"
channels: ""
---

## 核心宣传点

点击示例任务卡片时会同时带入对应的 Prompt 和 Agent，未雇佣的 Agent 会自动完成雇佣并发送；雇佣进度用一个统一 Toast 展示「检查→雇佣→启动」，失败时保留你的输入并可一键重试，交互更顺畅、不再丢内容。

## 原始内容

**fix(chat): 同步任务卡片的提示词、Agent、模型与分类布局 (#3153)**

- SHA: `6600fd431de5750275a93f5bc64b4d6f856f4831`
- PR: #3153
- 日期: 2026-07-31T09:43:28Z

```
fix(chat): 同步任务卡片的提示词、Agent、模型与分类布局 (#3153)

## 概要

- 在 Landing 和登录后的 New Task 中，点击示例任务卡片时同时带入对应的 Prompt 与 Agent；即使用户之前手动切换过
Agent，卡片选择仍会完整覆盖两者
- 在登录后的输入框中正确展示所选 Agent 的名称与头像，同时保留发送时自动聘用 Agent 的流程
- 登录后的 Agent 选择按钮始终展示下拉菜单当前选中的 Agent；选择 Assistant 时不再错误显示 Hire Agent
- 从侧栏 Agent 行点击 New Task 时始终创建干净草稿：只带入目标 Agent，不保留上一个任务的
Prompt、附件、starter Agent 或模型草稿；连续为同一个 Agent 新建任务同样生效
- 未 Hire 的任务卡 Agent 点击发送时会自动完成 Hire、创建会话并发送消息；本地 mock 现在与真实安装契约一致
- 自动 Hire 过程统一使用一个可更新的 Toast 展示“检查 → 雇佣 → 启动”进度，不再在输入框下方闪现临时文字
- 进行中的 Hire Toast 不会被普通通知的三条上限淘汰，确保后续阶段更新以及重试/选择其他 Agent 操作始终可用
- Hire 失败时保留 Prompt、附件、Agent 和模型选择，并展示 8 秒的本地化错误
Toast；用户可以直接“重新雇用”或“选择其他 Agent”
- 模型写入失败使用稳定错误码并转换为本地化、可操作的提示，不再向中文页面透传英文内部错误
- 重试会从真实失败步骤恢复：Hire 失败才重新 Hire，模型写入失败只重试模型，会话创建失败则复用已经安装并配置好的 Agent
- 登录后的 New Task 分类胶囊始终保持单行展示：Plan Marketing 与 Organize Work
会在第四个位置和固定显示的 More 菜单之间互换
- 登录后的 New Task 支持为尚未安装的卡片 Agent 预选模型；发送时按“计费检查 → Hire → 应用模型 → 必要时重启
computer runtime → 创建会话 → 发送消息”的顺序执行
- computer runtime 的显式模型草稿会复用现有重启弹窗，并等待 OpenClaw 重启完成、恢复 ready
后再继续发送；engine runtime 和默认模型继续走原有快速路径
- 尚未安装的卡片 Agent 在用户没有手动选择模型时，会直接显示模型目录中的 Default 模型；该展示不会被当作显式选择写入 Agent
配置
- 模型草稿按 Agent 隔离：同一 Agent 的其他卡片会保留选择，切换到其他 Agent 后会清理；显式模型更新失败时会中止发送
- Motion Video 使用经过原像素裁切的本地头像资源，移除原始图片自带的白色外圈和投影，同时保持品牌图形不变
- 增加针对性回归测试，并补充已确认的设计与实现文档

## 根因

Landing 和登录后的 New Task 适配层原先分别处理示例 Prompt 与 Agent 状态。因此，用户手动选择的 Agent
或选择器显示状态可能会在后续点击卡片后继续残留，导致只更新 Prompt、没有同步更新 Agent。

登录后的 Agent 按钮原先根据“用户是否显式选择过 Agent”覆盖为 Hire Agent，但下拉菜单根据当前 `selectedId`
勾选 Assistant，形成两套互相矛盾的展示状态。现在按钮和菜单统一使用当前选中的 Agent。

侧栏 Agent 的 New Task 通过同一个 `/new-chat` 路由切换 `workspace_id`。Next.js
不会为同路由导航自动重建组件；当用户连续为同一个 Agent 新建任务时，URL 甚至完全不变，因此旧 Prompt 和草稿 Agent
会继续残留。现在每次侧栏 New Task 都携带独立的 `new_task` 标识，并以 `workspace_id + new_task`
作为草稿 identity，完整重建 New Task ViewModel。

未安装的卡片 Agent 只有目录身份，还没有 `workspace_id`；模型选择器原先把 `workspace_id`
作为可编辑前提，因此只能展示模型列表，不能真正选择。现在会先保存按 Agent 归属的本地模型草稿，Hire 成功拿到 workspace
后再持久化模型。若用户没有显式选择，则选择器只展示目录的 Default 模型，并由 Hire 流程沿用后端默认配置。

显式模型写入对 engine runtime 可以立即生效，但 computer runtime 的配置只有在 OpenClaw
重启后才会进入运行中的 Agent。原流程在更新模型后立即创建会话并发送，导致首条消息可能仍使用旧模型。现在编排层会区分运行时：computer
runtime 写入显式模型后暂停原发送协程，等待重启状态从恢复中回到 ready，再继续创建会话和发送。

本地 mock 的 Agent catalog 已展示 Motion Video 等 specialist，但缺少
`/agents/install-capability` 响应，并且这些 pack 没有进入 engine 安装白名单。发送时自动 Hire
因此在 BFF 层返回 502。现在 mock 已补齐能力探测接口，并让 catalog 中的 specialist 与安装白名单保持一致。

Hire 流程原先把 `useAgentActions` 抛出的内部错误码 `hire_failed` 直接交给
Toast，同时进度文案又在输入框下方独立渲染，导致错误信息不可操作、进度提示闪烁，并且重复点击会堆叠多个 Toast。现在同一个 Toast
ID 贯穿整条发送链路：处理中保持 loading，成功后移除，失败后原地切换为带操作按钮的错误状态。重试上下文分别保存已解析 Agent
与模型写入状态，避免恢复过程中重复 Hire。

长期 Hire 流程原先使用 `durationMs: null`，但 Toast store
达到三条可见上限时仍会直接淘汰最旧项，导致后续更新与失败操作找不到原 Toast。现在持久 Toast
在操作完成前受到保护，普通通知优先淘汰；模型写入失败也通过稳定错误码进入中英文文案映射。

Motion Video
原始远程头像本身带有白色画布和投影，圆形容器无法消除图片内部的白圈。现在改为项目内的精确裁切资源，由现有圆形容器负责最终裁切。

登录后的 More 控件还会用当前溢出分类替换触发按钮文案，但没有从菜单中移除同一分类，造成 Plan Marketing
重复展示，并使分类胶囊换行。

## 验证

- [x] Hire 进度与失败操作回归：2 个测试文件、63 项测试全部通过
- [x] 全量 Web 单测中 563 个文件、7,639 项测试通过；唯一受限文件因沙箱禁止监听 `127.0.0.1` 返回
`EPERM`，在允许本地监听的环境中单独重跑 7/7 通过
- [x] `@zooclaw/chat-ui`：TypeScript、ESLint 与 337 项测试通过
- [x] `bash scripts/verify-changed.sh`
- [x] TypeScript 类型检查、ESLint 与 Web 治理检查通过
- [x] 草稿模型 TDD 回归：2 个测试文件、73 项测试全部通过
- [x] 目标 Web 验证：8 个测试文件、165 项测试全部通过
- [x] Agent 选择器同步验证：4 个测试文件、90 项测试全部通过
- [x] 本次补丁在最新 `main` 上验证：10 个相关测试文件、181 项测试全部通过
- [x] computer runtime 重启门槛回归：New Chat 与重启弹窗 2 个测试文件、67 项测试全部通过
- [x] 最新 Codex P1/P2 回归：New Chat、Toast 与重启弹窗 3 个测试文件、76 项测试全部通过
- [x] 本次修复再次通过 `bash scripts/verify-changed.sh`、Web 治理检查、TypeScript 与
ESLint
- [x] 本地登录后的 `/new-chat` 浏览器检查：未安装的 PPT Master 可以打开模型菜单并选择 GPT
5.4，选择后触发器立即显示新模型；冷启动无新增控制台错误
- [x] 本地默认模型浏览器检查：未安装的 Motion Video 自动显示 Claude Sonnet 4.6，菜单中该项已选中并标记
Default
- [x] 本地头像浏览器检查：Motion Video 使用本地头像资源，圆形容器正确裁切，白色外圈不再显示
- [x] 本地分类布局检查：默认分类保持单行；Plan Marketing 与 Organize Work 可以正确互换；More
始终显示，且只包含未提升到主栏的分类
- [x] 本地 Agent 选择器浏览器检查：从 Motion Video 切换到 Assistant
后，标题、输入框、触发按钮和菜单选中项全部同步，干净交互无新增控制台错误
- [x] 本地侧栏 New Task 浏览器检查：同一 Assistant 再次新建任务后，Motion Video Prompt
被清空，输入框恢复为空并选中 Assistant
- [x] 隔离 mock 浏览器检查：未安装的 PPT Master 自动 Hire 后创建会话、发送首条 Prompt
并进入新会话；Agent 身份与 Prompt 保持正确

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
```

**PR Body:**

## 概要

- 在 Landing 和登录后的 New Task 中，点击示例任务卡片时同时带入对应的 Prompt 与 Agent；即使用户之前手动切换过 Agent，卡片选择仍会完整覆盖两者
- 在登录后的输入框中正确展示所选 Agent 的名称与头像，同时保留发送时自动聘用 Agent 的流程
- 登录后的 Agent 选择按钮始终展示下拉菜单当前选中的 Agent；选择 Assistant 时不再错误显示 Hire Agent
- 从侧栏 Agent 行点击 New Task 时始终创建干净草稿：只带入目标 Agent，不保留上一个任务的 Prompt、附件、starter Agent 或模型草稿；连续为同一个 Agent 新建任务同样生效
- 未 Hire 的任务卡 Agent 点击发送时会自动完成 Hire、创建会话并发送消息；本地 mock 现在与真实安装契约一致
- 自动 Hire 过程统一使用一个可更新的 Toast 展示“检查 → 雇佣 → 启动”进度，不再在输入框下方闪现临时文字
- 进行中的 Hire Toast 不会被普通通知的三条上限淘汰，确保后续阶段更新以及重试/选择其他 Agent 操作始终可用
- Hire 失败时保留 Prompt、附件、Agent 和模型选择，并展示 8 秒的本地化错误 Toast；用户可以直接“重新雇用”或“选择其他 Agent”
- 模型写入失败使用稳定错误码并转换为本地化、可操作的提示，不再向中文页面透传英文内部错误
- 重试会从真实失败步骤恢复：Hire 失败才重新 Hire，模型写入失败只重试模型，会话创建失败则复用已经安装并配置好的 Agent
- 登录后的 New Task 分类胶囊始终保持单行展示：Plan Marketing 与 Organize Work 会在第四个位置和固定显示的 More 菜单之间互换
- 登录后的 New Task 支持为尚未安装的卡片 Agent 预选模型；发送时按“计费检查 → Hire → 应用模型 → 必要时重启 computer runtime → 创建会话 → 发送消息”的顺序执行
- computer runtime 的显式模型草稿会复用现有重启弹窗，并等待 OpenClaw 重启完成、恢复 ready 后再继续发送；engine runtime 和默认模型继续走原有快速路径
- 尚未安装的卡片 Agent 在用户没有手动选择模型时，会直接显示模型目录中的 Default 模型；该展示不会被当作显式选择写入 Agent 配置
- 模型草稿按 Agent 隔离：同一 Agent 的其他卡片会保留选择，切换到其他 Agent 后会清理；显式模型更新失败时会中止发送
- Motion Video 使用经过原像素裁切的本地头像资源，移除原始图片自带的白色外圈和投影，同时保持品牌图形不变
- 增加针对性回归测试，并补充已确认的设计与实现文档

## 根因

Landing 和登录后的 New Task 适配层原先分别处理示例 Prompt 与 Agent 状态。因此，用户手动选择的 Agent 或选择器显示状态可能会在后续点击卡片后继续残留，导致只更新 Prompt、没有同步更新 Agent。

登录后的 Agent 按钮原先根据“用户是否显式选择过 Agent”覆盖为 Hire Agent，但下拉菜单根据当前 `selectedId` 勾选 Assistant，形成两套互相矛盾的展示状态。现在按钮和菜单统一使用当前选中的 Agent。

侧栏 Agent 的 New Task 通过同一个 `/new-chat` 路由切换 `workspace_id`。Next.js 不会为同路由导航自动重建组件；当用户连续为同一个 Agent 新建任务时，URL 甚至完全不变，因此旧 Prompt 和草稿 Agent 会继续残留。现在每次侧栏 New Task 都携带独立的 `new_task` 标识，并以 `workspace_id + new_task` 作为草稿 identity，完整重建 New Task ViewModel。

未安装的卡片 Agent 只有目录身份，还没有 `workspace_id`；模型选择器原先把 `workspace_id` 作为可编辑前提，因此只能展示模型列表，不能真正选择。现在会先保存按 Agent 归属的本地模型草稿，Hire 成功拿到 workspace 后再持久化模型。若用户没有显式选择，则选择器只展示目录的 Default 模型，并由 Hire 流程沿用后端默认配置。

显式模型写入对 engine runtime 可以立即生效，但 computer runtime 的配置只有在 OpenClaw 重启后才会进入运行中的 Agent。原流程在更新模型后立即创建会话并发送，导致首条消息可能仍使用旧模型。现在编排层会区分运行时：computer runtime 写入显式模型后暂停原发送协程，等待重启状态从恢复中回到 ready，再继续创建会话和发送。

本地 mock 的 Agent catalog 已展示 Motion Video 等 specialist，但缺少 `/agents/install-capability` 响应，并且这些 pack 没有进入 engine 安装白名单。发送时自动 Hire 因此在 BFF 层返回 502。现在 mock 已补齐能力探测接口，并让 catalog 中的 specialist 与安装白名单保持一致。

Hire 流程原先把 `useAgentActions` 抛出的内部错误码 `hire_failed` 直接交给 Toast，同时进度文案又在输入框下方独立渲染，导致错误信息不可操作、进度提示闪烁，并且重复点击会堆叠多个 Toast。现在同一个 Toast ID 贯穿整条发送链路：处理中保持 loading，成功后移除，失败后原地切换为带操作按钮的错误状态。重试上下文分别保存已解析 Agent 与模型写入状态，避免恢复过程中重复 Hire。

长期 Hire 流程原先使用 `durationMs: null`，但 Toast store 达到三条可见上限时仍会直接淘汰最旧项，导致后续更新与失败操作找不到原 Toast。现在持久 Toast 在操作完成前受到保护，普通通知优先淘汰；模型写入失败也通过稳定错误码进入中英文文案映射。

Motion Video 原始远程头像本身带有白色画布和投影，圆形容器无法消除图片内部的白圈。现在改为项目内的精确裁切资源，由现有圆形容器负责最终裁切。

登录后的 More 控件还会用当前溢出分类替换触发按钮文案，但没有从菜单中移除同一分类，造成 Plan Marketing 重复展示，并使分类胶囊换行。

## 验证

- [x] Hire 进度与失败操作回归：2 个测试文件、63 项测试全部通过
- [x] 全量 Web 单测中 563 个文件、7,639 项测试通过；唯一受限文件因沙箱禁止监听 `127.0.0.1` 返回 `EPERM`，在允许本地监听的环境中单独重跑 7/7 通过
- [x] `@zooclaw/chat-ui`：TypeScript、ESLint 与 337 项测试通过
- [x] `bash scripts/verify-changed.sh`
- [x] TypeScript 类型检查、ESLint 与 Web 治理检查通过
- [x] 草稿模型 TDD 回归：2 个测试文件、73 项测试全部通过
- [x] 目标 Web 验证：8 个测试文件、165 项测试全部通过
- [x] Agent 选择器同步验证：4 个测试文件、90 项测试全部通过
- [x] 本次补丁在最新 `main` 上验证：10 个相关测试文件、181 项测试全部通过
- [x] computer runtime 重启门槛回归：New Chat 与重启弹窗 2 个测试文件、67 项测试全部通过
- [x] 最新 Codex P1/P2 回归：New Chat、Toast 与重启弹窗 3 个测试文件、76 项测试全部通过
- [x] 本次修复再次通过 `bash scripts/verify-changed.sh`、Web 治理检查、TypeScript 与 ESLint
- [x] 本地登录后的 `/new-chat` 浏览器检查：未安装的 PPT Master 可以打开模型菜单并选择 GPT 5.4，选择后触发器立即显示新模型；冷启动无新增控制台错误
- [x] 本地默认模型浏览器检查：未安装的 Motion Video 自动显示 Claude Sonnet 4.6，菜单中该项已选中并标记 Default
- [x] 本地头像浏览器检查：Motion Video 使用本地头像资源，圆形容器正确裁切，白色外圈不再显示
- [x] 本地分类布局检查：默认分类保持单行；Plan Marketing 与 Organize Work 可以正确互换；More 始终显示，且只包含未提升到主栏的分类
- [x] 本地 Agent 选择器浏览器检查：从 Motion Video 切换到 Assistant 后，标题、输入框、触发按钮和菜单选中项全部同步，干净交互无新增控制台错误
- [x] 本地侧栏 New Task 浏览器检查：同一 Assistant 再次新建任务后，Motion Video Prompt 被清空，输入框恢复为空并选中 Assistant
- [x] 隔离 mock 浏览器检查：未安装的 PPT Master 自动 Hire 后创建会话、发送首条 Prompt 并进入新会话；Agent 身份与 Prompt 保持正确

