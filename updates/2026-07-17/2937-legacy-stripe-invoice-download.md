---
title: 修复历史 Stripe 发票下载（旧版兼容）
type: Bug Fix
priority: B
date: 2026-07-17
status: 已合并待发版
pr: 2937
author: kaka-srp
url: https://github.com/SerendipityOneInc/ecap-workspace/pull/2937
---

## 更新内容

修复迁移前（pre-cutover）历史 Stripe 发票无法下载的问题：

- 历史生产 Stripe 发票改走临时的 legacy invoice-read key 读取
- 仅在精确命中 `404 resource_missing`（账户可见性问题）时才回退重试另一个 Stripe 账户
- sandbox/staging 保持使用当前 Stripe key，无需额外配置
- 设定硬性兼容日落时间 `2026-11-11`，之后历史发票请求引导至客服

## 用户价值

老用户在切换支付账户前开具的历史发票现在可以正常下载，避免财务对账缺失。
