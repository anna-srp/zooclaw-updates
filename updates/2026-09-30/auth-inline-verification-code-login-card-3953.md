---
title: "邮箱和手机验证码改在登录卡片内完成：不再跳转独立验证页，支持整段粘贴和系统自动填充"
type: "Improvement"
priority: "高"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 邮箱和手机验证码改在登录卡片内完成：不再跳转独立验证页，支持整段粘贴和系统自动填充

## 核心宣传点

邮箱和手机验证码原先会跳到一个独立的验证页面，把登录卡片里的操作打断；而且卡片一高，标题和右侧素材就被挤出视口。现在验证码输入、错误提示和验证成功反馈全都在发起登录的那张卡片里完成，布局也跟着卡片高度变化做了调整。六位验证码输入支持整段粘贴、编辑、退格、回车提交和系统验证码自动填充，返回时还会保留已填的邮箱、手机号和地区。点验证后按钮显示旋转圆环和「验证中 / Verifying...」，同时锁定输入防重复提交，认证状态更新时会暂缓自动跳转，让成功反馈按原有的 3 秒节奏完整展示。页面留白、卡片高度和右侧素材尺寸都重新调过，国家选择菜单换成登录配色，完整的短信授权说明直接显示在「继续」按钮上方，不用点开。中英文文案统一，新增紫绿渐变成功图标和动态走光效果，开启「减少动态效果」时用静态提示。邮箱接口、手机认证、CAPTCHA、账号与会话创建流程、登录后跳转目标、首次发送的 60 秒等待节奏全部沿用原有实现。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已随正式 release 上线

## PR 说明

## 改动说明


邮箱和手机验证码原先会跳转到独立验证页面，打断登录卡片内的操作；较高的登录卡片还会把标题和右侧素材挤出视口。本次让验证码输入、错误提示和验证成功反馈在发起登录的原卡片内完成，并调整布局以适应卡片高度变化。

- 共用六位验证码输入：支持完整粘贴、编辑、退格、回车提交和系统验证码自动填充；返回时保留邮箱、手机号及地区。
- 点击验证后，按钮显示旋转圆环与“验证中 /
Verifying...”文案，并锁定输入及重复提交；认证状态更新时暂缓页面自动跳转，让成功反馈按原有 3 秒回调时机完整展示。
- 调整页面留白、卡片高度和右侧素材尺寸；国家选择菜单使用登录色板，完整短信授权说明在“继续”按钮上方直接展示，无需点击或展开。
- 统一中英文文案，增加紫绿渐变成功图标、进入提示的动态走光，以及更柔和的卡片阴影；减少动态效果设置下使用静态提示。
- 提供仅开发环境可用的
`/login/preview`，从登录方式选择开始测试邮箱和手机完整流程，支持直接查看验证码、验证中与成功状态；Mock 使用
`alex@example.com`、`+1 4155550100` 和验证码 `123456`，验证等待约 1.6
秒，不发送验证码或建立登录会话。`?state=verifying` 可停留检查 loading 效果，重新演示会取消待完成的 Mock 验证。

## 问题原因与兼容性

原来的验证码入口依赖 `/user/verify`
跳转；登录页左栏的独立视口高度和底部留白叠加后，较高卡片会导致页面内容向下溢出。现在由共享验证控制器切换卡片内容，登录页与本地预览共用布局。

继续使用现有邮箱 API、Firebase 手机认证、CAPTCHA、账号与会话创建流程、认证请求快照和登录后目标地址。保留邮箱首次发送的 60
秒等待、手机首次重发可用的节奏、重发后的 60 秒等待，以及原有成功回调时机。真实验证的 loading
直接跟随接口状态，不增加人为延迟。Google 登录和旧验证链接保持兼容，短信完整声明与原有七个地区选项保留。

首轮 Codex 审查指出 `current_page`
目标被兜底路径覆盖：已复现并修复。验证前显式保存“留在当前页面”语义，平台登录不再误跳到聊天页；认证完成清理上下文后，指定聊天页和订阅页仍保持原有跳转目标。

已处理
[短信说明展示位置的审查评论](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#discussion_r4143427271)：完整短信说明恢复到手机号提交按钮之前直接可见，包含短信频率、STOP/HELP、资费及条款/隐私链接；移除信息弹层与重复的授权摘要，保留原有授权文案与登录行为。

已修复 [Sam 关于当前页验证完成后持续 loading
的评论](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#discussion_r4143834835)：`current_page`
且未提供完成回调时，在原有三秒成功反馈后清理验证码和验证状态、解除 busy，并刷新当前页面。Next.js
刷新会保留客户端状态，因此显式清理避免一直显示“Continuing to
ZooWork...”；既有成功回调及指定地址跳转不变，卸载时取消完成计时器。

## 验证

- [x] 同步最新 `main` 后，TypeScript、变更文件 ESLint、格式检查与前端治理检查通过。
- [x] 登录、旧邮箱/手机验证及 CAPTCHA：4 个测试文件、109 项测试通过。
- [x] 登录弹窗和认证请求快照：3 个测试文件、46 项测试通过。
- [x] 本地 Mock 的重发节奏、错误验证码、验证中状态、成功和取消重置：1 个测试文件、4 项测试通过。
- [x] 自动跳转延后与登录页 busy 状态接线：2 个测试文件、26 项测试通过。
- [x] 最后一次 loading 调整后，相关测试筛选共 22 个测试文件、267 项测试通过，TypeScript 与 ESLint
通过（包含上述部分测试）。
- [x] 登录后目标兼容性修复：新增平台 `current_page`、指定聊天页和订阅页回归测试；登录组件共 84
项测试通过，TypeScript、ESLint 与治理检查通过。
- [x] 导入边界和依赖健康检查通过。
- [x] 本地浏览器预览邮箱、手机、验证码、验证中及成功状态；用户已确认原有视觉效果，并查看英文登录方式选择面板。新增 loading
已在英文 Mock 页面展示并截图。
- [x] 上一提交 `9069c02f9` 的 CI 构建、完整测试、类型检查、ESLint 与 CodeQL 全部通过。
- [x] 上一提交已获得 [Codex
Review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#pullrequestreview-5364553949)，首轮
P1 已修复；Claude 审查同样为 APPROVE。
- [x] 短信说明展示修复：默认登录与新版登录入口的完整说明无需交互即可看见，并位于提交按钮之前；登录组件共 86
项测试、TypeScript、ESLint、格式与治理检查通过。本地英文预览已检查并截图。
- [x] 短信说明修复提交 `4b9c81584` 的 CI 构建、完整测试、类型检查、ESLint 与 CodeQL
全部通过，未发现新增代码扫描告警；[该提交 Codex
Review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#pullrequestreview-5365025055)，Claude
同样为 APPROVE。短信说明审查评论已解决。
- [x] 当前页完成行为回归：覆盖 Platform 邮箱登录、手机号成功后 busy
释放及控件恢复、三秒完成时机和卸载取消计时器；登录组件共 88 项测试、TypeScript、ESLint、格式与治理检查通过。
- [x] 当前页完成行为修复提交 `86b3cef5d` 的 CI 构建、完整测试、类型检查、ESLint 与 CodeQL
全部通过，未发现新增代码扫描告警；[最新 Codex
Review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#pullrequestreview-5365431364)，[Claude
同样为
APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#issuecomment-5910056560)。Sam
的成功态退出审查评论已解决。

本地使用针对性测试；完整构建与完整测试套件由 CI 执行。未发送真实验证码验证外部提供方。本次仅涉及 Web
前端，无后端部署改动。截图保留在本地 `.screenshots/`，不随代码提交。



<img width="3420" height="1350" alt="20260930-175730"
src="https://github.com/user-attachments/assets/c290bb2f-4a48-414e-9842-48bf5bea84c4"
/>

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `41477cb6356653d1f56f996dbf04f1c3744cd49e`
- PR: #3953
- 作者：lynn Zhuang
- 日期：2026-09-30T11:24:05Z

### Commit Message

```
fix(auth): 优化邮箱和手机登录的原页面验证码交互 (#3953)

## 改动说明


邮箱和手机验证码原先会跳转到独立验证页面，打断登录卡片内的操作；较高的登录卡片还会把标题和右侧素材挤出视口。本次让验证码输入、错误提示和验证成功反馈在发起登录的原卡片内完成，并调整布局以适应卡片高度变化。

- 共用六位验证码输入：支持完整粘贴、编辑、退格、回车提交和系统验证码自动填充；返回时保留邮箱、手机号及地区。
- 点击验证后，按钮显示旋转圆环与“验证中 /
Verifying...”文案，并锁定输入及重复提交；认证状态更新时暂缓页面自动跳转，让成功反馈按原有 3 秒回调时机完整展示。
- 调整页面留白、卡片高度和右侧素材尺寸；国家选择菜单使用登录色板，完整短信授权说明在“继续”按钮上方直接展示，无需点击或展开。
- 统一中英文文案，增加紫绿渐变成功图标、进入提示的动态走光，以及更柔和的卡片阴影；减少动态效果设置下使用静态提示。
- 提供仅开发环境可用的
`/login/preview`，从登录方式选择开始测试邮箱和手机完整流程，支持直接查看验证码、验证中与成功状态；Mock 使用
`alex@example.com`、`+1 4155550100` 和验证码 `123456`，验证等待约 1.6
秒，不发送验证码或建立登录会话。`?state=verifying` 可停留检查 loading 效果，重新演示会取消待完成的 Mock 验证。

## 问题原因与兼容性

原来的验证码入口依赖 `/user/verify`
跳转；登录页左栏的独立视口高度和底部留白叠加后，较高卡片会导致页面内容向下溢出。现在由共享验证控制器切换卡片内容，登录页与本地预览共用布局。

继续使用现有邮箱 API、Firebase 手机认证、CAPTCHA、账号与会话创建流程、认证请求快照和登录后目标地址。保留邮箱首次发送的 60
秒等待、手机首次重发可用的节奏、重发后的 60 秒等待，以及原有成功回调时机。真实验证的 loading
直接跟随接口状态，不增加人为延迟。Google 登录和旧验证链接保持兼容，短信完整声明与原有七个地区选项保留。

首轮 Codex 审查指出 `current_page`
目标被兜底路径覆盖：已复现并修复。验证前显式保存“留在当前页面”语义，平台登录不再误跳到聊天页；认证完成清理上下文后，指定聊天页和订阅页仍保持原有跳转目标。

已处理
[短信说明展示位置的审查评论](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#discussion_r4143427271)：完整短信说明恢复到手机号提交按钮之前直接可见，包含短信频率、STOP/HELP、资费及条款/隐私链接；移除信息弹层与重复的授权摘要，保留原有授权文案与登录行为。

已修复 [Sam 关于当前页验证完成后持续 loading
的评论](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#discussion_r4143834835)：`current_page`
且未提供完成回调时，在原有三秒成功反馈后清理验证码和验证状态、解除 busy，并刷新当前页面。Next.js
刷新会保留客户端状态，因此显式清理避免一直显示“Continuing to
ZooWork...”；既有成功回调及指定地址跳转不变，卸载时取消完成计时器。

## 验证

- [x] 同步最新 `main` 后，TypeScript、变更文件 ESLint、格式检查与前端治理检查通过。
- [x] 登录、旧邮箱/手机验证及 CAPTCHA：4 个测试文件、109 项测试通过。
- [x] 登录弹窗和认证请求快照：3 个测试文件、46 项测试通过。
- [x] 本地 Mock 的重发节奏、错误验证码、验证中状态、成功和取消重置：1 个测试文件、4 项测试通过。
- [x] 自动跳转延后与登录页 busy 状态接线：2 个测试文件、26 项测试通过。
- [x] 最后一次 loading 调整后，相关测试筛选共 22 个测试文件、267 项测试通过，TypeScript 与 ESLint
通过（包含上述部分测试）。
- [x] 登录后目标兼容性修复：新增平台 `current_page`、指定聊天页和订阅页回归测试；登录组件共 84
项测试通过，TypeScript、ESLint 与治理检查通过。
- [x] 导入边界和依赖健康检查通过。
- [x] 本地浏览器预览邮箱、手机、验证码、验证中及成功状态；用户已确认原有视觉效果，并查看英文登录方式选择面板。新增 loading
已在英文 Mock 页面展示并截图。
- [x] 上一提交 `9069c02f9` 的 CI 构建、完整测试、类型检查、ESLint 与 CodeQL 全部通过。
- [x] 上一提交已获得 [Codex
Review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#pullrequestreview-5364553949)，首轮
P1 已修复；Claude 审查同样为 APPROVE。
- [x] 短信说明展示修复：默认登录与新版登录入口的完整说明无需交互即可看见，并位于提交按钮之前；登录组件共 86
项测试、TypeScript、ESLint、格式与治理检查通过。本地英文预览已检查并截图。
- [x] 短信说明修复提交 `4b9c81584` 的 CI 构建、完整测试、类型检查、ESLint 与 CodeQL
全部通过，未发现新增代码扫描告警；[该提交 Codex
Review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#pullrequestreview-5365025055)，Claude
同样为 APPROVE。短信说明审查评论已解决。
- [x] 当前页完成行为回归：覆盖 Platform 邮箱登录、手机号成功后 busy
释放及控件恢复、三秒完成时机和卸载取消计时器；登录组件共 88 项测试、TypeScript、ESLint、格式与治理检查通过。
- [x] 当前页完成行为修复提交 `86b3cef5d` 的 CI 构建、完整测试、类型检查、ESLint 与 CodeQL
全部通过，未发现新增代码扫描告警；[最新 Codex
Review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#pullrequestreview-5365431364)，[Claude
同样为
APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3953#issuecomment-5910056560)。Sam
的成功态退出审查评论已解决。

本地使用针对性测试；完整构建与完整测试套件由 CI 执行。未发送真实验证码验证外部提供方。本次仅涉及 Web
前端，无后端部署改动。截图保留在本地 `.screenshots/`，不随代码提交。



<img width="3420" height="1350" alt="20260930-175730"
src="https://github.com/user-attachments/assets/c290bb2f-4a48-414e-9842-48bf5bea84c4"
/>
```

来源：SerendipityOneInc/ecap-workspace @ 41477cb6，PR #3953，作者 lynn Zhuang。
