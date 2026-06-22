---
title: "聊天输入框上方实时显示「正在接通你的 Claw…」连接状态"
type: "体验优化"
priority: "中"
date: "2026-06-17"
status: "待审核"
channels: "Discord+changelog"
---
# 聊天输入框上方实时显示「正在接通你的 Claw…」连接状态
## 核心宣传点
当与智能体的实时连接处于重连/断开/异常状态时，聊天输入框上方会显示「Reaching your Claw…」提示（带橙色加载动画与扫光效果），连接恢复后自动消失，让你清楚知道当前是网络在重连而不是消息发不出去。
## 原始内容
fix(chat): 输入框上方展示agent 链接中状态 (#2331)

## Summary
- 在 chat 输入框上方新增 connection-warning slot，当 WebSocket 稳态为 `reconnecting |
disconnected | error` 时显示
"Reaching your Claw..." 提示（`ldrs` 的 JellyTriangle 8px loader +
caution-text 橙色 + 金黄色扫光动效）。
  - 该 slot 优先级高于已有的 typing indicator —— 一个掉线的 agent 不可能在"打字"，所以两者互斥。
  - 不覆盖 init / restart 阶段（那段由 `InitBanner` 头部条幅负责），避免重复信号。

  ## Implementation notes
- `ChatBody.tsx`：根据 `stableStatus` 派生 `connectionWarning` 对象，从 i18n
`genClaw.connecting` key
  取文案（fallback `"Reaching your Claw..."`），透传给 `GenClawInput`。
- `GenClawInput.tsx`：新增可选 prop `connectionWarning`；在 typing-indicator
同位置渲染，三元优先级
  `connectionWarning ? ... : typingLabel ? ... : null`。
- `globals.css`：新增 `.shimmer-claw`，用 `background-clip: text` +
`background-size: 200%` + `no-repeat` + 关键帧
`100% → 0%` 把金黄 (`#fcd34d` / dark 下 `#fffbeb`) 高光带在深橙文字上从左扫到右，1.8s
一个周期、无死时间。
  - 新增依赖 `ldrs@^1.1.9`（提供 JellyTriangle web component）。

  ## Test plan
- [ ] 断开后端 WS / 拔网线，输入框上方出现 "Reaching your Claw..." + 橙色三角形 loader +
金黄扫光
  - [ ] 网络恢复后提示自动消失
  - [ ] Agent 正在打字时不应同时显示该警告
  - [ ] init / restart 阶段仍由 `InitBanner` 占用顶部，不应重复出现该警告
  - [ ] Dark 模式下高光带改为暖白 (`#fffbeb`)，深底上仍清晰可见
  - [ ] JellyTriangle 8px 在 `text-xs`（12px）行高里垂直居中对齐


https://github.com/user-attachments/assets/80106084-ec15-40c8-b9fc-84c5ffb5ba37

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

## PR Description
## Summary
  - 在 chat 输入框上方新增 connection-warning slot，当 WebSocket 稳态为 `reconnecting | disconnected | error` 时显示
  "Reaching your Claw..." 提示（`ldrs` 的 JellyTriangle 8px loader + caution-text 橙色 + 金黄色扫光动效）。
  - 该 slot 优先级高于已有的 typing indicator —— 一个掉线的 agent 不可能在"打字"，所以两者互斥。
  - 不覆盖 init / restart 阶段（那段由 `InitBanner` 头部条幅负责），避免重复信号。

  ## Implementation notes
  - `ChatBody.tsx`：根据 `stableStatus` 派生 `connectionWarning` 对象，从 i18n `genClaw.connecting` key
  取文案（fallback `"Reaching your Claw..."`），透传给 `GenClawInput`。
  - `GenClawInput.tsx`：新增可选 prop `connectionWarning`；在 typing-indicator 同位置渲染，三元优先级
  `connectionWarning ? ... : typingLabel ? ... : null`。
  - `globals.css`：新增 `.shimmer-claw`，用 `background-clip: text` + `background-size: 200%` + `no-repeat` + 关键帧
  `100% → 0%` 把金黄 (`#fcd34d` / dark 下 `#fffbeb`) 高光带在深橙文字上从左扫到右，1.8s 一个周期、无死时间。
  - 新增依赖 `ldrs@^1.1.9`（提供 JellyTriangle web component）。

  ## Test plan
  - [ ] 断开后端 WS / 拔网线，输入框上方出现 "Reaching your Claw..." + 橙色三角形 loader + 金黄扫光
  - [ ] 网络恢复后提示自动消失
  - [ ] Agent 正在打字时不应同时显示该警告
  - [ ] init / restart 阶段仍由 `InitBanner` 占用顶部，不应重复出现该警告
  - [ ] Dark 模式下高光带改为暖白 (`#fffbeb`)，深底上仍清晰可见
  - [ ] JellyTriangle 8px 在 `text-xs`（12px）行高里垂直居中对齐

https://github.com/user-attachments/assets/80106084-ec15-40c8-b9fc-84c5ffb5ba37


