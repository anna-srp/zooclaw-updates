---
title: "内部：注册、发起购买、支付成功、取消订阅四类事件推送飞书群机器人"
type: "新功能上线"
priority: "中"
date: "2026-09-23"
status: "内部-跳过"
channels: ""
---

# 内部：注册、发起购买、支付成功、取消订阅四类事件推送飞书群机器人

## 核心宣传点

向飞书群机器人推送四类业务卡片：新用户注册、发起购买、Stripe Checkout 支付成功、用户取消订阅。每张卡片标注环境并用不同颜色区分。通知是尽力发送：Pydantic 校验、卡片构造和 HTTP 发送都在后台完成，失败绝不改变业务结果，异常日志只记录类型；每个进程最多 32 个发送任务，容量满了直接丢弃不排队，HTTP 超时 5 秒。属于内部运营通知，用户侧无感知。

## 分级

- 内部：P1
- 外部：内部
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## 背景与行为

向飞书群机器人发送四类业务卡片：新用户注册、发起购买、Stripe Checkout 购买成功、用户取消订阅。每张卡片标注环境，使用不同颜色；邮箱等业务字段按已确认要求完整展示。通知为尽力发送，失败不得改变业务结果。

## 实现与失败隔离

- 统一 `notify(kind, **payload)` 入口；Pydantic 校验、卡片构造和 HTTP 发送在后台完成。
- 通知专用字段提取、转换和任务调度有异常边界；异常日志只记录类型。注册、建单、支付结算和取消的业务错误仍按原有方式传播。
- 每个进程最多 32 个发送任务；容量满时直接丢弃，不等待、不创建额外排队任务。HTTP 超时为 5 秒，关闭时有界等待。
- `FEISHU_NOTIFY_WEBHOOK_URL` 为空时不发送；原商务咨询 webhook 保持独立。
- 购买消息按事件、provider、uid、订单号独立去重，不能以支付订单的 `SUCCEEDED` 状态推断已经通知。`invoice.paid` 或 `payment_intent.succeeded` 先结算时，后到的 Checkout 仍会尝试通知。
- 去重缓存为进程内最多 2048 个键、1 小时 TTL，仅在成功调度后登记；不增加支付数据库依赖。
- 订阅成功消息要求结算返回权益记录，风控拒绝的试用及其重放不会误报成功。

## 明确取舍

- 跨实例、重启、缓存淘汰或 TTL 到期后可能重复；容量满、发送失败或进程重启可能丢失。无重试队列或事务性 outbox，不承诺严格一次投递。
- 发起购买和取消按次通知，不去重。购买成功仅覆盖 Stripe Checkout，其他支付事件不直接发卡。
- 只部署 backend；Vault 中配置 `FEISHU_NOTIFY_WEBHOOK_URL`，代码可先于配置上线。

## 验证

- 253 条相关单元测试通过，覆盖四个业务落点、通知异常隔离、任务容量及恢复、去重 TTL/容量、支付事件乱序、重复 Checkout 和试用拒绝。
- `bash scripts/verify-local.sh --py-static` 通过：ruff、格式、pyright（0 错误）、8 项导入契约。
- 未调用真实飞书或生产支付服务；运行时投递由部署后的配置决定。

设计文档：`docs/superpowers/specs/2026-09-22-feishu-business-notifications.md`


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `47578245ecd5b4324e1f36c4986e6b07aaddd863`
- PR: #3861
- 作者：tim-srp
- 日期：2026-09-23T01:53:17Z

### Commit Message

```
feat(feishu): notify a bot on registration, checkout, purchase and cancellation (#3861)

## 背景与行为

向飞书群机器人发送四类业务卡片：新用户注册、发起购买、Stripe Checkout
购买成功、用户取消订阅。每张卡片标注环境，使用不同颜色；邮箱等业务字段按已确认要求完整展示。通知为尽力发送，失败不得改变业务结果。

## 实现与失败隔离

- 统一 `notify(kind, **payload)` 入口；Pydantic 校验、卡片构造和 HTTP 发送在后台完成。
- 通知专用字段提取、转换和任务调度有异常边界；异常日志只记录类型。注册、建单、支付结算和取消的业务错误仍按原有方式传播。
- 每个进程最多 32 个发送任务；容量满时直接丢弃，不等待、不创建额外排队任务。HTTP 超时为 5 秒，关闭时有界等待。
- `FEISHU_NOTIFY_WEBHOOK_URL` 为空时不发送；原商务咨询 webhook 保持独立。
- 购买消息按事件、provider、uid、订单号独立去重，不能以支付订单的 `SUCCEEDED`
状态推断已经通知。`invoice.paid` 或 `payment_intent.succeeded` 先结算时，后到的 Checkout
仍会尝试通知。
- 去重缓存为进程内最多 2048 个键、1 小时 TTL，仅在成功调度后登记；不增加支付数据库依赖。
- 订阅成功消息要求结算返回权益记录，风控拒绝的试用及其重放不会误报成功。

## 明确取舍

- 跨实例、重启、缓存淘汰或 TTL 到期后可能重复；容量满、发送失败或进程重启可能丢失。无重试队列或事务性 outbox，不承诺严格一次投递。
- 发起购买和取消按次通知，不去重。购买成功仅覆盖 Stripe Checkout，其他支付事件不直接发卡。
- 只部署 backend；Vault 中配置 `FEISHU_NOTIFY_WEBHOOK_URL`，代码可先于配置上线。

## 验证

- 253 条相关单元测试通过，覆盖四个业务落点、通知异常隔离、任务容量及恢复、去重 TTL/容量、支付事件乱序、重复 Checkout
和试用拒绝。
- `bash scripts/verify-local.sh --py-static` 通过：ruff、格式、pyright（0 错误）、8
项导入契约。
- 未调用真实飞书或生产支付服务；运行时投递由部署后的配置决定。


设计文档：`docs/superpowers/specs/2026-09-22-feishu-business-notifications.md`

---------

Co-authored-by: Claude Code <noreply@anthropic.com>
```

来源：SerendipityOneInc/ecap-workspace @ 47578245，PR #3861，作者 tim-srp。