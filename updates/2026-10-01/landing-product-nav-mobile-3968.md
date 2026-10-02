---
title: "官网新增四个产品入口卡片与 Products 导航，手机端导航和页面对齐全面优化"
type: "体验优化"
priority: "高"
date: "2026-10-01"
status: "待审核"
channels: "Discord+changelog"
---

# 官网新增四个产品入口卡片与 Products 导航，手机端导航和页面对齐全面优化

## 核心宣传点

官网原先没有集中的产品入口，手机端导航不好发现，各区块的左右边界也不一致。这次按设计稿统一了页芯：首屏下方新增 Agent Builder、Managed Agent API、Enterprise、ZooData 四张产品卡片，各带标题、描述和线条动效插画；页头新增 Products 下拉，Resources 去掉重复的 ZooData 并统一 hover 展开。Header、首屏界面图、产品区、正文和页脚统一为 1176px 最大内容宽度，首屏背景全宽并加了背景视差。手机端 Header 改成无边框图标菜单，导航支持触控展开，Get Started 放进菜单里，菜单可滚动、关闭后焦点会恢复，也支持 RTL。共用的移动 App 弹窗按 Figma 更新，桌面以扫码为主、手机直接给 App Store 按钮。另外未登录访问 /home 会先跳 /login，并等服务端校验完再判断会话，纯 HttpOnly Cookie 的登录用户也能正常进入；动效会尊重「减少动态效果」设置。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## 变更说明

官网原先缺少集中的产品入口，移动端导航不可发现，各区块左右边界也不一致。本次按设计稿统一页芯，并补齐产品导航和手机访问体验。

- 首屏下方增加 Agent Builder、Managed Agent API（Coming soon）、Enterprise、ZooData 四个产品卡片，包含标题、描述和对应产品的线条动效插画。卡片采用浅灰背景，移除跳转箭头。
- 新增 Products 下拉，复用 iOS App 弹窗入口；Resources 移除重复的 ZooData，并统一 hover 展开。桌面下拉面板平滑切换，保留原来的箭头方向表现。
- Header、首屏界面图、产品区和后续正文、页脚统一为 1176px 最大内容宽度；首屏背景全宽，增加背景视差，界面图仍保持对齐。
- 手机 Header 使用无边框图标菜单，导航支持触控展开；Get Started 放入菜单，保留首屏 CTA。菜单支持滚动、关闭后焦点恢复及 RTL；七天试点流程适配窄屏。
- 按 Figma 更新共用的移动 App 弹窗，官网与登录后的 Profile 面板共用。桌面以扫码为主，手机保留直接前往 App Store 的下载按钮。
- 两处 Get Started 下拉的产品名称统一为 Agent Builder；未登录访问 `/home` 跳转至 `/login`，等待服务端 `/account/me` 校验后再判断会话，支持仅有 HttpOnly Cookie、尚未恢复本地缓存的登录用户；临时失败保留重试入口。
- 产品菜单与卡片的站内链接保留当前域名和语言，App 路由通过现有语言 Cookie 传递选择；Resources 在 hover 后点击仍保持展开，键盘与触控可切换。
- Products 导航、产品卡片以及 Home 匿名/失效会话拦截使用独立的认证归因，更新 GA4 调用点登记；由现有登录表单发送 Flow 事件，避免计入首屏 CTA 转化。
- 动效尊重减少动态效果设置，手机关闭背景视差。

## 设计参考

- [页芯与内容对齐](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=1198-3992)
- [iOS App 下载弹窗](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=1185-3310)

## 验证

- Web TypeScript、ESLint、治理检查通过；本地单元测试 11026 项通过（70 项跳过，1 项待办），动效补充后的相关 90 项测试通过；同步最新 main 后，认证、弹窗和导航等 70 项相关测试通过。
- 设计系统 Sheet 的类型检查、Lint 和 6 项单元测试通过。
- Chrome 浏览器检查 320–2560px 共 36 组边界（全部 10 种语言，包含 RTL）：内容对齐、无横向溢出、Header 无重叠。
- 已验证桌面 Products → Solutions → Resources hover 切换、手机导航 → 共用 iOS 弹窗、下载入口、背景视差及减少动态效果模式。
- 已复核首页 46 张图片均正常加载，访客态 `/home` 登录跳转通过。
- Tim review 后补充的相关 120 项测试通过，TypeScript、ESLint 和治理检查通过。浏览器复现 Cookie 登录初始化返回 503、但 `/account/me` 成功的场景：Home 可进入；真实访客仍跳转登录。另验证 Resources hover 后点击、键盘关闭及日文桌面/卡片/手机产品路由。
- 认证归因修复后，相关 280 项测试、TypeScript、ESLint 和治理检查通过；浏览器验证四类登录入口保留各自的 intent/trigger，继续复核 Cookie 登录与匿名拦截行为。
- 本地验证使用 Chrome 设备模拟，未进行实体 iPhone/Safari 验证；完整生产构建由 CI 验证。
- 最终提交 `0b382660c` 的 CI 已完成：24 项通过、14 项按路径规则跳过，无失败；包括完整 Web 单元测试、生产构建和 CodeQL。

## Review

已请求 `tim-srp` 复核；最终提交 `0b382660c` 的 [Codex review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3968#pullrequestreview-5372289557) 结论为 **APPROVE**，未发现问题，CI 已通过。等待人工审批，尚未合并。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `69054215659574912a0d9e2ac985eeab11133f31`
- PR: #3968
- 作者：lynn Zhuang
- 日期：2026-10-01T00:28:46Z

### Commit Message

```
feat(landing): 更新官网产品导航、页芯对齐和移动端适配 (#3968)

## 变更说明

官网原先缺少集中的产品入口，移动端导航不可发现，各区块左右边界也不一致。本次按设计稿统一页芯，并补齐产品导航和手机访问体验。

- 首屏下方增加 Agent Builder、Managed Agent API（Coming soon）、Enterprise、ZooData
四个产品卡片，包含标题、描述和对应产品的线条动效插画。卡片采用浅灰背景，移除跳转箭头。
- 新增 Products 下拉，复用 iOS App 弹窗入口；Resources 移除重复的 ZooData，并统一 hover
展开。桌面下拉面板平滑切换，保留原来的箭头方向表现。
- Header、首屏界面图、产品区和后续正文、页脚统一为 1176px 最大内容宽度；首屏背景全宽，增加背景视差，界面图仍保持对齐。
- 手机 Header 使用无边框图标菜单，导航支持触控展开；Get Started 放入菜单，保留首屏 CTA。菜单支持滚动、关闭后焦点恢复及
RTL；七天试点流程适配窄屏。
- 按 Figma 更新共用的移动 App 弹窗，官网与登录后的 Profile 面板共用。桌面以扫码为主，手机保留直接前往 App Store
的下载按钮。
- 两处 Get Started 下拉的产品名称统一为 Agent Builder；未登录访问 `/home` 跳转至
`/login`，等待服务端 `/account/me` 校验后再判断会话，支持仅有 HttpOnly
Cookie、尚未恢复本地缓存的登录用户；临时失败保留重试入口。
- 产品菜单与卡片的站内链接保留当前域名和语言，App 路由通过现有语言 Cookie 传递选择；Resources 在 hover
后点击仍保持展开，键盘与触控可切换。
- Products 导航、产品卡片以及 Home 匿名/失效会话拦截使用独立的认证归因，更新 GA4 调用点登记；由现有登录表单发送 Flow
事件，避免计入首屏 CTA 转化。
- 动效尊重减少动态效果设置，手机关闭背景视差。

## 设计参考

-
[页芯与内容对齐](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=1198-3992)
- [iOS App
下载弹窗](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=1185-3310)

## 验证

- Web TypeScript、ESLint、治理检查通过；本地单元测试 11026 项通过（70 项跳过，1 项待办），动效补充后的相关
90 项测试通过；同步最新 main 后，认证、弹窗和导航等 70 项相关测试通过。
- 设计系统 Sheet 的类型检查、Lint 和 6 项单元测试通过。
- Chrome 浏览器检查 320–2560px 共 36 组边界（全部 10 种语言，包含 RTL）：内容对齐、无横向溢出、Header
无重叠。
- 已验证桌面 Products → Solutions → Resources hover 切换、手机导航 → 共用 iOS
弹窗、下载入口、背景视差及减少动态效果模式。
- 已复核首页 46 张图片均正常加载，访客态 `/home` 登录跳转通过。
- Tim review 后补充的相关 120 项测试通过，TypeScript、ESLint 和治理检查通过。浏览器复现 Cookie
登录初始化返回 503、但 `/account/me` 成功的场景：Home 可进入；真实访客仍跳转登录。另验证 Resources hover
后点击、键盘关闭及日文桌面/卡片/手机产品路由。
- 认证归因修复后，相关 280 项测试、TypeScript、ESLint 和治理检查通过；浏览器验证四类登录入口保留各自的
intent/trigger，继续复核 Cookie 登录与匿名拦截行为。
- 本地验证使用 Chrome 设备模拟，未进行实体 iPhone/Safari 验证；完整生产构建由 CI 验证。
- 最终提交 `0b382660c` 的 CI 已完成：24 项通过、14 项按路径规则跳过，无失败；包括完整 Web 单元测试、生产构建和
CodeQL。

## Review

已请求 `tim-srp` 复核；最终提交 `0b382660c` 的 [Codex
review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3968#pullrequestreview-5372289557)
结论为 **APPROVE**，未发现问题，CI 已通过。等待人工审批，尚未合并。
```

来源：SerendipityOneInc/ecap-workspace @ 69054215，PR #3968，作者 lynn Zhuang。
