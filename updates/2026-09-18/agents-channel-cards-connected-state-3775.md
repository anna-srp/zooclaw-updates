---
title: "style(agents): refine channel cards and connected state (#3775)"
type: "体验优化"
priority: "中"
date: "2026-09-18"
status: "待审核"
channels: ""
---

# Channel 页面改成紧凑卡片，已连接渠道排到最前面

## 核心宣传点

Channel 页面原来的控件偏大、已连接的渠道还单独用一条横条显示。现在统一成紧凑卡片，已连接的排在列表最前面，卡片上直接显示平台 Logo、连接状态、绑定 Agent 的头像和名称，以及设置/断开按钮；策略编辑移到设置弹窗里。未连接状态改成居中的 Not Linked，Add Channel 用黑底白字。已连接卡片会显示具体渠道账号，断开确认里同时显示平台和账号，同一个 Agent 下挂多个同平台账号时不会再搞混。飞书权限提示、微信重新授权和断开审计信息都保留。

## 分级

- 内部：P2
- 外部：C
- 发布状态：已合并待发版

## PR 说明

## Summary

Channel 页面原有控件偏大，已连接的 Engine 渠道以独立横条显示。此次改为统一的紧凑卡片，并将已连接渠道放在列表最前面。

- 按 [Figma 参考](https://www.figma.com/design/g6P3ltpK7i4NOVzv2hVYxE/zooclaw2.0?node-id=1884-12151)调整已连接卡片，显示平台 Logo、连接状态、绑定 Agent 的头像与名称，以及设置 / 断开按钮；移除卡片内的策略展示栏，设置弹窗保留策略编辑。
- 缩小 Logo、按钮和间距，Logo 圆角为 6px；未连接状态改为居中的 12px `Not Linked`，Add Channel 使用黑底白字。
- 未连接卡片的选择栏与设置按钮默认透明、悬停为浅灰色；两类卡片的按钮悬停均保持原边线颜色。
- 保留异常状态、飞书权限提示、微信重新授权和断开连接的确认及审计信息。
- 已连接卡片直接显示渠道账号，断开确认同时显示平台与账号，避免同一 Agent 下多个同平台连接混淆；补充双账号编辑和断开回归测试。

## Test plan

- [x] TypeScript `tsc --noEmit`、前端治理检查和 ESLint 通过。
- [x] `bash scripts/verify-web.sh --test-only src/components/agent-channels/components/ChannelsSection.tsx`：3 个文件通过，71 项测试通过；另有 69 项原有 legacy 测试保持跳过。
- [x] 本地 mock 预览检查桌面与窄屏布局、设置入口、断开确认 / 取消，以及透明背景和悬停样式。

改动仅涉及前端；预览用的模拟连接数据和截图未提交，未测试真实平台连接。


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `0a222a9dc3a61e8e3047003a57636ab43ac5a474`
- PR: #3775
- 作者：shana-srp
- 日期：2026-09-18T03:07:20Z

### Commit Message

```
style(agents): refine channel cards and connected state (#3775)

## Summary

Channel 页面原有控件偏大，已连接的 Engine 渠道以独立横条显示。此次改为统一的紧凑卡片，并将已连接渠道放在列表最前面。

- 按 [Figma
参考](https://www.figma.com/design/g6P3ltpK7i4NOVzv2hVYxE/zooclaw2.0?node-id=1884-12151)调整已连接卡片，显示平台
Logo、连接状态、绑定 Agent 的头像与名称，以及设置 / 断开按钮；移除卡片内的策略展示栏，设置弹窗保留策略编辑。
- 缩小 Logo、按钮和间距，Logo 圆角为 6px；未连接状态改为居中的 12px `Not Linked`，Add Channel
使用黑底白字。
- 未连接卡片的选择栏与设置按钮默认透明、悬停为浅灰色；两类卡片的按钮悬停均保持原边线颜色。
- 保留异常状态、飞书权限提示、微信重新授权和断开连接的确认及审计信息。
- 已连接卡片直接显示渠道账号，断开确认同时显示平台与账号，避免同一 Agent 下多个同平台连接混淆；补充双账号编辑和断开回归测试。

## Test plan

- [x] TypeScript `tsc --noEmit`、前端治理检查和 ESLint 通过。
- [x] `bash scripts/verify-web.sh --test-only
src/components/agent-channels/components/ChannelsSection.tsx`：3 个文件通过，71
项测试通过；另有 69 项原有 legacy 测试保持跳过。
- [x] 本地 mock 预览检查桌面与窄屏布局、设置入口、断开确认 / 取消，以及透明背景和悬停样式。

改动仅涉及前端；预览用的模拟连接数据和截图未提交，未测试真实平台连接。

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

## 备注

发布状态：已合并待发版（尚未包含在任何 ecap-*-release tag 中，最新正式 release 为 ecap-v0.19.16-release）。

来源：SerendipityOneInc/ecap-workspace @ 0a222a9d，PR #3775，作者 shana-srp。
