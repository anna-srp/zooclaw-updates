---
title: "开发者平台空状态换成插画，投递历史区分「还没有记录」和「筛选没结果」"
type: "体验优化"
priority: "中"
date: "2026-10-19"
status: "待审核"
channels: ""
---

# 开发者平台空状态换成插画，投递历史区分「还没有记录」和「筛选没结果」

## 核心宣传点

Platform 的 API keys、Webhooks、Usage、付款历史和功能不可用页面此前用小图标做空状态，与 ZooWork 的插画风格和排版不一致。现在统一改用共享的 PluginEmptyState 组件，新增凭据、连接、记录、功能不可用四张插画，筛选无结果和 404 复用已有插画，并补齐尺寸与间距规范。Webhooks 投递历史现在能区分「尚无记录」和「筛选无结果」，后者可一键清除全部筛选并恢复列表，焦点回到常驻的 Clear 控件；顺带修复了取消创建 API key 弹窗后焦点不回到触发按钮的问题。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## 备注

是已合并 #4084 的独立后续优化，不改接口、权限与支付逻辑；共享组件与插画需与 Design System PR #8 配套。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `5fc5a2159f4fa4b2d454e9e3d4359b3255bf5bcc`
- PR: #4089
- 作者：lynn Zhuang
- 日期：2026-10-19T11:28:45Z

### Commit Message

```
fix(platform): 统一空状态插画、布局规范与交互 (#4089)

## 改动说明
Platform 的 API keys、Webhooks、Usage、付款历史和不可用页面此前使用小图标空状态，与 ZooWork
的插画风格和排版不一致。本次统一调用共享 PluginEmptyState，以实际 Platform
页面验收，补齐插画素材与尺寸、文字、操作间距规范。

- 新增凭据、连接、记录、功能不可用四张插画；筛选无结果和404复用已有插画。源图、生成提示词和语义映射一同入库。
- 共享组件增加 section
布局和标题级别；占位小屏192×144px、桌面224×168px，插画/标题/描述/操作之间为16/8/24px。原 ZooWork page
默认布局保持兼容。
- 投递历史区分“尚无记录”和“筛选无结果”，后者可清除全部已应用筛选并恢复列表，焦点回到持续存在的 Clear 筛选控件。
- 修复本轮验收发现的原有焦点问题：取消 API key 创建弹窗后返回实际触发按钮，表单转入密钥弹窗时不抢走焦点。

共享组件、四张插画和规范已同步至 [Design System PR
#8](https://github.com/SerendipityOneInc/Zoowork-design-system/pull/8)，提交
`0bd31ac`。此 PR 是已合并
[#4084](https://github.com/SerendipityOneInc/ecap-workspace/pull/4084)
的独立后续优化，不改接口、权限或支付逻辑。

## 分批提交
- `b3b0f0f88`：共享插画、组件 API、目录与规范。
- `c9466d596`：Platform 页面接入、筛选和创建弹窗焦点修复。
- `6eaf3ffee`：清除空结果筛选后的键盘焦点回归修复。

## 验证
- Platform lint、typecheck、生产 build 通过；全量300项测试通过，焦点修复后 router
100项（含新增2项）和 Webhooks 26项通过。
- 本仓共享 DS tsc、lint、空状态组件测试通过。
- 真实 Chrome：7种页面 × 桌面/375px ×
浅/深色，共28组新版检查；另有7组旧版截图。所有新版插画成功加载、占位与16/8/24px间距一致，无横向溢出。
- API key/Webhook 空状态入口打开弹窗、Esc关闭、焦点恢复；投递筛选清除回列表并保留焦点；404返回入口均通过。
- 独立DS仓全量构建、类型、lint、组件/Chat
UI/预览测试及发布脚本测试通过；pack和独立Vite/Next消费者验证通过，四张资产均进入包。


本地预览：`http://127.0.0.1:4180/__preview/settings/api-keys?scenario=empty`。截图与对比HTML保存在本地Obsidian，未向生产环境发布。

CI（最新 `6eaf3ffee`）：全部适用检查通过，包括 Platform quality、Web
lint/typecheck/test/build、Admin/Dashboard、CodeQL；两轮自动评审未发现需要修复的问题。两个PR均未合并。


## 验收修复：长表单弹窗滚动

Create/Edit webhook 原来让整窗和事件列表分别滚动，短窗口中底部按钮会被裁切并随滚动上移。现在直接调用共享
`DialogContent scrollable` /
`DialogBody`：仅正文滚动，标题、关闭入口和操作区固定；默认短弹窗保持兼容。通过原生 form ID 关联底部提交按钮，保留
Enter、pending 和 secret 面板衔接；校验/服务端错误聚焦到可见正文。

独立提交：`ac7211fde`。共享组件、规范和真实目录回归同步至 Design System PR #8（`2b55bc2`）。

本轮验证：Platform 306 项测试、lint、类型检查/构建；Chrome
1440×760、1280×600、375×667、844×390 的实际滚动头尾坐标、最后事件选择、无溢出、浅深色、打开后
resize、校验聚焦、Enter 创建、secret 衔接、编辑保存、Esc/焦点返回均通过。远端 CI 以最新提交检查为准。
```

