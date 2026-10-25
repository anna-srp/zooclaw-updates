---
title: "修复：鼠标关闭 Agent 切换菜单后按钮残留深色焦点边框"
type: "Bug Fix"
priority: "中"
date: "2026-10-13"
status: "待审核"
channels: ""
---

# 修复：鼠标关闭 Agent 切换菜单后按钮残留深色焦点边框

## 核心宣传点

修复用鼠标关闭 Agent 切换菜单后，触发按钮上仍残留一圈深色焦点边框的问题，覆盖共享 Button、应用内旧版 Button 和 Paper Focus 暗色侧栏。Tab 导航的可见焦点、outline 按钮原本的边框和校验失败提示都完整保留，同时修掉了评审指出的反向回归（Tab 聚焦后点击外部拖拽区域应继续显示键盘焦点）。根因是 Radix 的 asChild 组合会覆盖原有标记，现已改用稳定的 data-zc-button。纯前端样式修复。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 备注

设计系统与主应用两侧都需要随前端发版一起上线，样式覆盖规则与共享规则同优先级、依赖声明顺序，后续改动需注意顺序。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `bd39f2d9115172db122a5a3e015e514bd7d3052c`
- PR: #4058
- 作者：lynn Zhuang
- 日期：2026-10-13T09:55:15Z

### Commit Message

```
fix(design-system): 补齐共享与旧版按钮的鼠标焦点边框修复 (#4058)

## 修复内容

修复鼠标关闭 Agent 切换菜单后，按钮仍残留深色焦点边框的问题，覆盖共享 Button、应用旧 Button 和 Paper Focus
暗色侧栏。保留 Tab 导航的可见焦点、outline 按钮原本的边框和校验失败提示。

同时修复审查指出的反向回归：通过 Tab 聚焦按钮后，点击调用 `preventDefault()`
的外部拖拽区域，焦点仍停在原按钮上，此时继续显示键盘焦点边框。

## 根因与改动

- Radix 的 `asChild` 组合会覆盖 `data-slot="button"`。共享 Button 和旧
`components/ds/button.tsx` 增加稳定的 `data-zc-button` 标记，使组合触发器仍匹配边框清理规则。
- 非 overlay 的 pointerdown
清理前，记录当前元素是否已有鼠标标记；仅恢复已有标记，避免把保留的键盘焦点误改为鼠标焦点。真正失焦时清理标记，键盘输入恢复键盘焦点样式。
- Paper Focus 暗色侧栏根据元素自身的焦点来源标记决定是否显示焦点边框，不再仅依据页面最后的输入方式。
- 旧 outline Button 保留浅色 `--border` / 暗色
`--input`，并注明覆盖规则与共享规则同优先级、依赖声明顺序。
- 鼠标焦点清理排除 `aria-invalid="true"` 控件；InputGroup 中存在错误状态时保留组级提示。

本轮对应
[键盘焦点保留的审查意见](https://github.com/SerendipityOneInc/ecap-workspace/pull/4058#pullrequestreview-5498674681)，并补充
CSS 规则顺序注释。旧版 Button 已包含在修复范围中。

## 验证

- 新增 5 个反向回归场景均验证了修复前失败、修复后通过：普通区域及 overlay 取消的 pointerdown、共享组合
Button、旧 Button、暗色侧栏。
- 共享设计系统：60 个测试文件、367 项测试通过；TypeScript、ESLint、预览生产构建通过。构建保留既有的单块超过 500
KB 提示。
- 主应用：TypeScript、治理 guards、7 项 Button 聚焦测试与相关文件 ESLint 通过。
- 保留原有鼠标关闭菜单及焦点返回、外部点击未移动焦点、真实 blur、键盘恢复、outline 明暗主题、asChild 链接和错误状态测试。
- 最新提交 `fdfc38ba4`（修复提交 `5863298ed`，随后同步 main）的全部适用 CI
检查通过，包括主应用测试、类型检查、构建和 CodeQL；Claude 与 Codex 自动审查均通过，确认键盘焦点回归已修复。

本轮验证依据为真实组件 DOM、实际 CSS 选择器和 jsdom 计算样式，未进行完整应用的真实浏览器 E2E 或线上截图对照。
```

