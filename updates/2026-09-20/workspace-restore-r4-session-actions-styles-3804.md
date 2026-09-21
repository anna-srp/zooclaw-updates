---
title: "fix(workspace): 恢复 R4 会话操作并优化交互样式 (#3804)"
type: "Bug Fix"
priority: "中"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# 修复：恢复 R4 工作区的会话操作并统一交互样式

## 核心宣传点

R4 Agent 工作区缺失的会话操作和附件入口回来了：会话侧边栏的重命名、归档，以及聊天顶部的标题编辑都可用，详情页浏览器标签会显示 Agent 名称，新建 Agent 接入了与首页一致的附件上传，外部渠道卡片显示真实的 Agent 头像。同时接入 V5 默认头像（白色图形保留，配各不相同的浅色渐变背景与浅灰圆形描边），Update 按钮精简为名称后的紫色圆形上箭头表示有新版本，列表、导航和弹窗的交互样式统一。

## 分级

- 内部：P2
- 外部：B
- 发布状态：已上线

## PR 说明

## 改动说明

恢复 R4 Agent 工作区缺失的会话操作和附件入口，并统一列表、导航及弹窗的交互样式。

- 恢复 Agent 会话侧边栏重命名、归档及聊天顶部标题编辑；详情页浏览器标签展示 Agent 名称。新建 Agent 接入与首页一致的附件上传能力，外部渠道卡片显示实际 Agent 头像。
- 接入 V5 默认头像：保留白色图形内部，使用各不相同的浅色渐变背景与浅灰圆形描边。精简 Update 按钮，以名称后的紫色圆形上箭头表示有新版本；整行悬停时箭头持续动画，活动图改为紫绿渐变。
- 统一列表圆角悬停、相邻分隔线、更多菜单、会话选中态和创建按钮提示；Tasks 增加骨架加载，移除多余的积分失败横幅与表头悬停。创建弹窗顶部增加轻量紫绿渐变，侧边栏图标改为局部路径动效，并支持减少动态效果偏好。
- 分享弹窗使用深色复制按钮，复制完整 URL，Build 历史链接折叠展示。链接沿用现有创建、发布与撤销流程；复制地址来自本次创建接口的返回值。

## 后端范围

后端仅涉及会话重命名和归档，共 2 个业务实现文件、2 个测试文件，合计新增 289 行、删除 1 行；其中业务实现新增 99 行、删除 1 行，测试新增 190 行。

| 文件（相对 `services/claw-interface/`） | 用途 | 行数 |
| --- | --- | --- |
| `app/routes/agent_development.py` | 新增会话重命名、归档两个 POST 接口；校验身份、功能访问权限及标题参数，返回现有会话记录类型 | +30 / -1 |
| `app/services/agent_development/task_metadata_service.py` | 将 Engine 会话 ID 或历史会话别名映射到原始 Web 会话记录；检查工作区归属和会话可操作性，再复用已有会话服务 | +69 |
| `tests/unit/test_agent_development_route_boundaries.py` | 覆盖身份和组织参数传递、无效标题及 404 返回 | +28 |
| `tests/unit/test_agent_task_metadata.py` | 覆盖原始记录 ID 映射、历史会话、新建 Web 会话、归属校验，以及外部渠道只读、隐藏和已归档会话限制 | +162 |

新增接口：

- `POST /agent-definitions/{workspace_id}/task-sessions/{session_id}/rename`
- `POST /agent-definitions/{workspace_id}/task-sessions/{session_id}/archive`

需要后端配合的原因：前端任务列表中的会话 ID 可能来自 Engine 或历史别名，与存储中的原始 Web 会话 ID 不一致。后端负责解析对应关系、校验权限并持久保存操作结果。归档只更新状态，保留历史记录。

本 PR 没有新增数据库结构或迁移。分享链接继续沿用现有创建、发布与撤销流程；分享链接复用、token 加密保存及相关存储字段和数据库查询改动已撤回。

## 验证

- [x] 合入 `main`（`25750ee08`），解决 Agent 详情页逻辑与 mock 路由冲突，同时保留会话操作和每个 Agent 的连接器、MCP、知识库配置能力。
- [x] 合并 main 后，前端会话操作、资源配置/恢复、分享发布及 mock 回归：14 个文件、101 项测试通过。
- [x] 合并 main 后，后端会话操作、接口边界、分享发布及资源策略/恢复回归：8 个文件、115 项测试通过。
- [x] 前端 TypeScript、ESLint 与仓库治理检查通过。
- [x] 后端 Ruff、格式、Pyright 和 import-linter 检查通过。
- [x] `git diff --check` 通过。
- [ ] 已知待处理：归档/重命名后同步失效 Tasks 总表缓存，避免立即返回总表时展示旧记录。

涉及 `web/app` 与 `services/claw-interface`；会话操作上线需要前后端配套部署。本次未重跑浏览器回归或全量测试，完整构建和全量质量检查由 CI 执行。


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `ed62e2ee420a9f8f2c2e759e3601daf58c7f112c`
- PR: #3804
- 作者：lynn Zhuang
- 日期：2026-09-20T03:52:56Z

### Commit Message

```
fix(workspace): 恢复 R4 会话操作并优化交互样式 (#3804)

## 改动说明

恢复 R4 Agent 工作区缺失的会话操作和附件入口，并统一列表、导航及弹窗的交互样式。

- 恢复 Agent 会话侧边栏重命名、归档及聊天顶部标题编辑；详情页浏览器标签展示 Agent 名称。新建 Agent
接入与首页一致的附件上传能力，外部渠道卡片显示实际 Agent 头像。
- 接入 V5 默认头像：保留白色图形内部，使用各不相同的浅色渐变背景与浅灰圆形描边。精简 Update
按钮，以名称后的紫色圆形上箭头表示有新版本；整行悬停时箭头持续动画，活动图改为紫绿渐变。
- 统一列表圆角悬停、相邻分隔线、更多菜单、会话选中态和创建按钮提示；Tasks
增加骨架加载，移除多余的积分失败横幅与表头悬停。创建弹窗顶部增加轻量紫绿渐变，侧边栏图标改为局部路径动效，并支持减少动态效果偏好。
- 分享弹窗使用深色复制按钮，复制完整 URL，Build
历史链接折叠展示。链接沿用现有创建、发布与撤销流程；复制地址来自本次创建接口的返回值。

## 后端范围

后端仅涉及会话重命名和归档，共 2 个业务实现文件、2 个测试文件，合计新增 289 行、删除 1 行；其中业务实现新增 99 行、删除 1
行，测试新增 190 行。

| 文件（相对 `services/claw-interface/`） | 用途 | 行数 |
| --- | --- | --- |
| `app/routes/agent_development.py` | 新增会话重命名、归档两个 POST
接口；校验身份、功能访问权限及标题参数，返回现有会话记录类型 | +30 / -1 |
| `app/services/agent_development/task_metadata_service.py` | 将 Engine
会话 ID 或历史会话别名映射到原始 Web 会话记录；检查工作区归属和会话可操作性，再复用已有会话服务 | +69 |
| `tests/unit/test_agent_development_route_boundaries.py` |
覆盖身份和组织参数传递、无效标题及 404 返回 | +28 |
| `tests/unit/test_agent_task_metadata.py` | 覆盖原始记录 ID 映射、历史会话、新建 Web
会话、归属校验，以及外部渠道只读、隐藏和已归档会话限制 | +162 |

新增接口：

- `POST
/agent-definitions/{workspace_id}/task-sessions/{session_id}/rename`
- `POST
/agent-definitions/{workspace_id}/task-sessions/{session_id}/archive`

需要后端配合的原因：前端任务列表中的会话 ID 可能来自 Engine 或历史别名，与存储中的原始 Web 会话 ID
不一致。后端负责解析对应关系、校验权限并持久保存操作结果。归档只更新状态，保留历史记录。

本 PR 没有新增数据库结构或迁移。分享链接继续沿用现有创建、发布与撤销流程；分享链接复用、token
加密保存及相关存储字段和数据库查询改动已撤回。

## 验证

- [x] 合入 `main`（`25750ee08`），解决 Agent 详情页逻辑与 mock 路由冲突，同时保留会话操作和每个 Agent
的连接器、MCP、知识库配置能力。
- [x] 合并 main 后，前端会话操作、资源配置/恢复、分享发布及 mock 回归：14 个文件、101 项测试通过。
- [x] 合并 main 后，后端会话操作、接口边界、分享发布及资源策略/恢复回归：8 个文件、115 项测试通过。
- [x] 前端 TypeScript、ESLint 与仓库治理检查通过。
- [x] 后端 Ruff、格式、Pyright 和 import-linter 检查通过。
- [x] `git diff --check` 通过。
- [ ] 已知待处理：归档/重命名后同步失效 Tasks 总表缓存，避免立即返回总表时展示旧记录。

涉及 `web/app` 与
`services/claw-interface`；会话操作上线需要前后端配套部署。本次未重跑浏览器回归或全量测试，完整构建和全量质量检查由
CI 执行。
```

来源：SerendipityOneInc/ecap-workspace @ ed62e2ee，PR #3804，作者 lynn Zhuang。