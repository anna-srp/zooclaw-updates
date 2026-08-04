---
title: "会话标题与重命名交互优化"
type: "体验优化"
priority: "低"
date: "2026-08-03"
status: "待审核"
channels: ""
---

## 核心宣传点

聊天页顶部直接显示当前会话名称并支持就地重命名，去掉重复标题栏，Enter/失焦保存、Escape 取消，与侧边栏体验一致。

## 原始内容

**Commit**: `6fcca6bc65adddf6f3c33ef02226257572e95f7c` — lynn Zhuang — 2026-08-03T04:05:40Z

### Commit Message

```
refactor(chat): 优化会话标题与重命名交互 (#3192)

## 背景

当前聊天会话页顶部展示的是 Agent 名称，真正的 Session
名称位于独立的第二标题栏中，信息层级重复，重命名入口也与侧边栏体验不一致。本次调整属于现有聊天会话头部的交互与信息架构优化，不新增业务能力。

## 调整内容

- 顶部保留 Agent 头像，将 Agent 名称替换为当前 Session 名称，并移除重复的第二标题栏。
- Session 名称可直接在顶部重命名；编辑态、蓝色文本选中效果和圆角与侧边栏 Session rename 保持一致。
- 支持 Enter 保存、失焦保存、Escape 取消，并在保存后同步更新侧边栏 Session 列表缓存。
- 旧版 Session History 页面继续显示“头像 + Session History”，标题保持只读，不提供 rename。
- 优化窄屏布局和无障碍语义：标题在展示与编辑状态下均保留一级标题结构；手机端仅压缩健康连接状态，异常状态文字始终可见。

## 主干兼容修正

- 对齐 artifacts V2 测试夹具中的已发布文件地址契约。
- 移除当前完整 Web 门禁发现的未使用 `getAgentArtifact` 导出。

## 验证

- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm lint:ci`
- [x] Session header 相关定向测试：8 个文件、179 个测试
- [x] 标题语义与连接状态回归测试：2 个文件、63 个测试
- [x] Asset Library 与 Legacy Workspace Browser 测试：2 个文件、4 个测试
- [x] 本地 Mock 页面验证 Enter/失焦保存、Escape 取消、侧边栏标题同步及只读 Session History
- [x] 390px、720px 和桌面宽度响应式验证，Files/Settings 保持可用，长标题正常截断
- [x] CI 41/41 通过，Codex 与 Claude 自动评审通过

## Linear

无
```

### PR Body

```
## 背景

当前聊天会话页顶部展示的是 Agent 名称，真正的 Session 名称位于独立的第二标题栏中，信息层级重复，重命名入口也与侧边栏体验不一致。本次调整属于现有聊天会话头部的交互与信息架构优化，不新增业务能力。

## 调整内容

- 顶部保留 Agent 头像，将 Agent 名称替换为当前 Session 名称，并移除重复的第二标题栏。
- Session 名称可直接在顶部重命名；编辑态、蓝色文本选中效果和圆角与侧边栏 Session rename 保持一致。
- 支持 Enter 保存、失焦保存、Escape 取消，并在保存后同步更新侧边栏 Session 列表缓存。
- 旧版 Session History 页面继续显示“头像 + Session History”，标题保持只读，不提供 rename。
- 优化窄屏布局和无障碍语义：标题在展示与编辑状态下均保留一级标题结构；手机端仅压缩健康连接状态，异常状态文字始终可见。

## 主干兼容修正

- 对齐 artifacts V2 测试夹具中的已发布文件地址契约。
- 移除当前完整 Web 门禁发现的未使用 `getAgentArtifact` 导出。

## 验证

- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm lint:ci`
- [x] Session header 相关定向测试：8 个文件、179 个测试
- [x] 标题语义与连接状态回归测试：2 个文件、63 个测试
- [x] Asset Library 与 Legacy Workspace Browser 测试：2 个文件、4 个测试
- [x] 本地 Mock 页面验证 Enter/失焦保存、Escape 取消、侧边栏标题同步及只读 Session History
- [x] 390px、720px 和桌面宽度响应式验证，Files/Settings 保持可用，长标题正常截断
- [x] CI 41/41 通过，Codex 与 Claude 自动评审通过

## Linear

无

```
