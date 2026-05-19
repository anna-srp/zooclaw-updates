---
title: "修复：新用户注册后进入聊天输入框为空的问题"
type: "Bug Fix"
priority: "中"
date: "2026-05-18"
status: "待审核"
channels: ""
---
# 修复：新用户注册后进入聊天输入框为空的问题

## 核心宣传点
修复了新用户完成注册/支付流程后跳转到聊天页面，输入框预填内容消失的问题。

## 原始内容

**Commit**: `d4452cd2` | ecap-workspace | 2026-05-18T13:18:14Z  
**PR**: #1728 | fix(web): Await composer resolution before completing landing handoff

---

### 背景

Follow-up to #1724。生产日志揭示了 `[LandingContextPoll] hand-off complete` 在输入框视觉上还未填充内容时就触发的问题 —— poll 使用 URL 中的 `?q=` 参数作为"预填完成"的代理信号，但 URL 状态在 React 的 `useSearchParams` → `prefillInput` → `setInput(initialInput)` 链路之前。有用户反馈看到完成日志显示成功但输入框是空的（URL 已经被清成 `/chat?agent_id=main`，没有 `?q=`）。

### 修复

在 `useLandingContextFlow.ts` 中增加"composer 已解析预填"的门控。poll 现在等待 `GenClawInput` 真正 *apply* 预填到可编辑状态，或显式 *drop* 之后，才触发 `[LandingContextPoll] hand-off complete`。

同时记录 `prefillStatus: 'applied' | 'dropped'` 到生产日志，可区分"用户看到了预填"和"我们有意保留了草稿"两种情况。
