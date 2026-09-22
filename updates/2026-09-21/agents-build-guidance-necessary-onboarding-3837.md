---
title: "feat(agents): make build guidance clear and support necessary onboarding (#3837)"
type: "新功能"
priority: "高"
date: "2026-09-21"
status: "待审核"
channels: ""
---

# Agent Build 指导更明确，并支持必要的一次性 onboarding

## 核心宣传点

Agent Build（构建）流程这次补了两块能力。第一块是可信的 Product Action：Build 在需要时按需读取页面入口、执行路径、前置条件和完成标志，并且明确区分「账号级资源连接」和「当前 Agent 的绑定」，所以它给出的操作指引不再靠猜，而是对得上真实产品形态。第二块是必要的一次性 onboarding：Build 可以根据 Agent 实际功能声明启动前必须补齐的信息，同时复用实例里已有的资料，只补真正缺的那几项——可选偏好和每次任务才需要的输入不会被抬成初始化门槛。配套还补齐了 onboarding 的源码校验、创建/修订应用以及提交失败后的重试恢复，已经完成的 onboarding 不会被重复触发。需要注意部署顺序：Engine 的 onboarding lifecycle 接口先上，claw-interface 再上，完整体验要两边都生效。本次没有前端页面改动、没有数据库迁移，也不会批量改写存量 Agent。

## 分级

- 内部：P0
- 外部：A
- 发布状态：已合并待发版

## PR 说明

## Summary

- 为 Agent Build 提供按需读取的可信 Product Action：页面入口、执行路径、前置条件及完成标志，区分账号资源连接与当前 Agent 绑定。
- 支持 Build 根据实际功能声明必要的一次性 onboarding；复用已有实例资料，只补必要缺口，不把可选偏好或每次任务输入变成初始化门槛。
- 补齐 onboarding 源码校验、创建/修订应用及提交重试恢复；不重启已完成的 onboarding。
- 提供中文设计说明和本地真实模型行为评测。评审读取完整可见交互，源码使用生产校验器；移除强制分阶段返回等过严断言，避免测试驱动行为过拟合。

## Scope and rollout

- 配套 Engine PR：https://github.com/SerendipityOneInc/zooclaw-engine/pull/1580 。
- Engine 的 onboarding lifecycle endpoint 必须先部署，再部署本 PR 的 claw-interface；完整 Build 指导需要两边一起生效。
- 无前端页面改动、无数据库迁移、不批量改写存量 Agent；不恢复旧 Agent Pack 的多阶段审批流程。
- 未部署线上，未执行生产数据变更。

## Test plan

- [x] 定向后端回归：174 项通过（onboarding / authoring / service / source artifacts / Product Action / Engine client / eval harness）。
- [x] CI 首轮发现两处历史摘要测试 fixture 漏排除新增可选字段；已修正并补充显式声明/清除摘要回归，相关 34 项测试通过，未修改生产摘要行为。
- [x] Ruff、格式、Pyright、import-linter 和提交 hooks 通过。
- [x] 本地真实模型评测：20 个行为场景及 1 个新增已有资料复用场景通过；执行模型 `gpt-5.6-terra`，评审模型 `claude-sonnet-5`，指定的 Council Skill 使用真实内容。
- [x] 人工检查新增 onboarding 产物：先读当前实例配置，只补问必需缺项，不把实例值硬编码到共享 Skill。
- [ ] 部署后的跨服务及真实渠道端到端验收（本 PR 未执行）。

评测边界：LLM 调用是真实的，源码校验复用生产实现；authoring 应用/外部资源/渠道仍为本地测试替身。评测不是线上 Build 流程，不给用户增加评审步骤，也不构成线上交付成功证明。


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `725b54e3423992cc3d46bde1a18b603573cf8eff`
- PR: #3837
- 作者：kaka-srp
- 日期：2026-09-21T06:58:48Z

### Commit Message

```
feat(agents): make build guidance clear and support necessary onboarding (#3837)

## Summary

- 为 Agent Build 提供按需读取的可信 Product Action：页面入口、执行路径、前置条件及完成标志，区分账号资源连接与当前
Agent 绑定。
- 支持 Build 根据实际功能声明必要的一次性
onboarding；复用已有实例资料，只补必要缺口，不把可选偏好或每次任务输入变成初始化门槛。
- 补齐 onboarding 源码校验、创建/修订应用及提交重试恢复；不重启已完成的 onboarding。
- 提供中文设计说明和本地真实模型行为评测。评审读取完整可见交互，源码使用生产校验器；移除强制分阶段返回等过严断言，避免测试驱动行为过拟合。

## Scope and rollout

- 配套 Engine
PR：https://github.com/SerendipityOneInc/zooclaw-engine/pull/1580 。
- Engine 的 onboarding lifecycle endpoint 必须先部署，再部署本 PR 的
claw-interface；完整 Build 指导需要两边一起生效。
- 无前端页面改动、无数据库迁移、不批量改写存量 Agent；不恢复旧 Agent Pack 的多阶段审批流程。
- 未部署线上，未执行生产数据变更。

## Test plan

- [x] 定向后端回归：174 项通过（onboarding / authoring / service / source artifacts
/ Product Action / Engine client / eval harness）。
- [x] CI 首轮发现两处历史摘要测试 fixture 漏排除新增可选字段；已修正并补充显式声明/清除摘要回归，相关 34
项测试通过，未修改生产摘要行为。
- [x] Ruff、格式、Pyright、import-linter 和提交 hooks 通过。
- [x] 本地真实模型评测：20 个行为场景及 1 个新增已有资料复用场景通过；执行模型 `gpt-5.6-terra`，评审模型
`claude-sonnet-5`，指定的 Council Skill 使用真实内容。
- [x] 人工检查新增 onboarding 产物：先读当前实例配置，只补问必需缺项，不把实例值硬编码到共享 Skill。
- [ ] 部署后的跨服务及真实渠道端到端验收（本 PR 未执行）。

评测边界：LLM 调用是真实的，源码校验复用生产实现；authoring 应用/外部资源/渠道仍为本地测试替身。评测不是线上 Build
流程，不给用户增加评审步骤，也不构成线上交付成功证明。
```

来源：SerendipityOneInc/ecap-workspace @ 725b54e3，PR #3837，作者 kaka-srp。