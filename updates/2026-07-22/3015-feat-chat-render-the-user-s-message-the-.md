---
title: 发出的消息即时显示在对话框（乐观渲染）
type: 新功能
priority: B
date: 2026-07-22
status: 已合并待发版
pr: 3015
author: chris-srp
url: https://github.com/SerendipityOneInc/ecap-workspace/pull/3015
---

发出的消息即时显示在对话框（乐观渲染）

## Linear

（无 issue，用户直接反馈：发出的消息不会立刻出现在对话框里）

同根因衍生 issue：[ECA-1302](https://linear.app/srpone/issue/ECA-1302) — 发送过程中切换会话导致 channel 错配（既有行为，不在本 PR 范围）

后续跟进：[ECA-1304](https://linear.app/srpone/issue/ECA-1304) — thread 型界面缺少乐观渲染（本 PR 范围外）

## Summary

用户发出的消息要等一会儿才出现在对话框里。根因不是"慢"，而是架构上不可能快：消息列表完全由服务端派生，`useMattermost.sendMessage` 在 `await api.sendPost(...)` **之后**才写 post store，而那个 store 是列表的唯一来源——所以在 REST 往返返回之前，气泡在数据上根本不存在。会话首条更糟：credits 预检先跑，两次串行网络调用之后才画得出东西。

改动：

- **乐观插入 + 对账**。在 `await` 之前插入临时 post，服务端确认后换成真实 post。对账键用 Mattermost 原生的 `pending_post_id`（REST 响应和 WS `posted` 事件都会原样回传，本仓此前 
