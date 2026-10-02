---
title: "开发者平台 Console 全面改版：侧栏精简、充值体验优化、登录页与品牌统一"
type: "体验优化"
priority: "高"
date: "2026-10-01"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---

# 开发者平台 Console 全面改版：侧栏精简、充值体验优化、登录页与品牌统一

## 核心宣传点

开发者平台 Console 这次按 ZooWork System 2.0 做了一轮完整的 UI 重构：字体、表格、弹窗、空状态、hover、暗色和移动端样式全部对齐。侧栏精简到 API keys、Usage、Documentation 三项，其余收进 Settings / Organization settings，个人设置改名 Account，项目切换下拉会自动加载下一页。充值部分统一了 Add funds 文案，支持预设和自定义金额并即时校验，补齐了零余额展示和充值引导。登录页换成 Ship your agents 文案、六位验证码交互和静音循环视频（带真实首帧兜底图）。品牌侧统一为 ZooWork Console 标识、深蓝 favicon 和新的标签页标题。另外修掉了三处交互问题：账单就绪后才提示零余额充值、首屏尊重已保存的主题、返回登录上一步会保留同邮箱的验证码冷却时间。本次只改前端，没有后端改动、没有数据迁移。

## 分级

- 内部：P1
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## 迭代内容
- 对齐 ZooWork System 2.0：统一字体、表格、弹窗、空状态、hover、暗色和移动端样式。
- 精简侧栏：保留 API keys、Usage、Documentation；其余收进 Settings / Organization settings，个人设置改名 Account，项目切换下拉列表自动加载下一页。
- 优化充值：统一 Add funds 文案，支持预设/自定义金额和即时校验，补齐零余额展示与充值引导。
- 更新登录：Ship your agents 文案、六位验证码交互、静音循环视频及约 59 KB 的真实首帧兜底图。
- 更新品牌：ZooWork Console 标识、深蓝 favicon、ZooWork｜Managed Agents API 标签页标题和外观设置。
- 增加隔离的本地 UI 预览与回归测试，预览入口不进入生产构建；预览主题与 Settings 同步并跨页面保留。
- 修复 tim-srp 提出的 3 处交互问题：账单就绪后才提示零余额充值、首屏尊重保存主题、返回登录上一步保留同邮箱验证码冷却时间。

## 范围与风险
- **未修改任何后端。** 相对 main，仅改动 `web/platform`、前端依赖锁文件及设计文档；API 客户端、数据结构、认证/账单核心逻辑和共享组件实现均未改动。
- 已合入 main 的 #3973，保留登录后账单初始化及失败重试规则；切换 Console / Settings 不重新挂载初始化逻辑，避免重复请求。
- 保留现有权限控制、充值幂等和支付状态轮询；仅需部署 Platform 前端，无数据迁移或新增环境变量。
- `size-override`：本次完整 UI 重构覆盖多个页面，同时包含测试、预览和设计文档，超过 3,000 行常规预算；使用已有行数例外，其他 CI 和代码审查照常执行。

## 验证
- [x] 最新 Platform CI 全量测试：15 个文件、101 项全部通过；本地对应回归测试通过。
- [x] Platform lint、TypeScript 检查、生产构建通过。
- [x] 桌面/移动端登录、验证码、视频兜底、设置导航、零余额和项目切换已在本地预览核验。
- [x] 确认无后端及接口契约变更。
- [x] 最新修复提交 `27a6ebed1` 全部适用 GitHub CI 通过，两套自动复审通过，无未解决 P0/P1/P2。
- [x] CodeQL #666 已核实并记录为误报：固定本地预览路径跳转，不执行 HTML，且不进入生产构建。
- [x] tim-srp 已批准 `27a6ebed1`，确认 3 条意见已修复，未发现新的实质回归（人工复审未独立运行测试）。

未执行真实支付扣款。构建有非阻断性体积提示：主包约 506 KB（gzip 约 152 KB）。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `147177be311c27eb44533d13f50cadab9d3befa8`
- PR: #3978
- 作者：david-srp
- 日期：2026-10-01T10:14:11Z

### Commit Message

```
refactor(platform): 统一 Console UI 与登录体验 / align console UI and sign-in (#3978)

## 迭代内容
- 对齐 ZooWork System 2.0：统一字体、表格、弹窗、空状态、hover、暗色和移动端样式。
- 精简侧栏：保留 API keys、Usage、Documentation；其余收进 Settings / Organization
settings，个人设置改名 Account，项目切换下拉列表自动加载下一页。
- 优化充值：统一 Add funds 文案，支持预设/自定义金额和即时校验，补齐零余额展示与充值引导。
- 更新登录：Ship your agents 文案、六位验证码交互、静音循环视频及约 59 KB 的真实首帧兜底图。
- 更新品牌：ZooWork Console 标识、深蓝 favicon、ZooWork｜Managed Agents API
标签页标题和外观设置。
- 增加隔离的本地 UI 预览与回归测试，预览入口不进入生产构建；预览主题与 Settings 同步并跨页面保留。
- 修复 tim-srp 提出的 3 处交互问题：账单就绪后才提示零余额充值、首屏尊重保存主题、返回登录上一步保留同邮箱验证码冷却时间。

## 范围与风险
- **未修改任何后端。** 相对 main，仅改动 `web/platform`、前端依赖锁文件及设计文档；API
客户端、数据结构、认证/账单核心逻辑和共享组件实现均未改动。
- 已合入 main 的 #3973，保留登录后账单初始化及失败重试规则；切换 Console / Settings
不重新挂载初始化逻辑，避免重复请求。
- 保留现有权限控制、充值幂等和支付状态轮询；仅需部署 Platform 前端，无数据迁移或新增环境变量。
- `size-override`：本次完整 UI 重构覆盖多个页面，同时包含测试、预览和设计文档，超过 3,000
行常规预算；使用已有行数例外，其他 CI 和代码审查照常执行。

## 验证
- [x] 最新 Platform CI 全量测试：15 个文件、101 项全部通过；本地对应回归测试通过。
- [x] Platform lint、TypeScript 检查、生产构建通过。
- [x] 桌面/移动端登录、验证码、视频兜底、设置导航、零余额和项目切换已在本地预览核验。
- [x] 确认无后端及接口契约变更。
- [x] 最新修复提交 `27a6ebed1` 全部适用 GitHub CI 通过，两套自动复审通过，无未解决 P0/P1/P2。
- [x] CodeQL #666 已核实并记录为误报：固定本地预览路径跳转，不执行 HTML，且不进入生产构建。
- [ ] tim-srp 人工复审（3 条意见已修复，持续跟进）。

未执行真实支付扣款。构建有非阻断性体积提示：主包约 506 KB（gzip 约 152 KB）。
```

来源：SerendipityOneInc/ecap-workspace @ 147177be，PR #3978，作者 david-srp。
