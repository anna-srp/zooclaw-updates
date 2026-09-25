---
title: "修复：个人订阅到期后，旧 Agent 的历史聊天、成果和文件重新可以访问"
type: "Bug Fix"
priority: "高"
date: "2026-09-24"
status: "待审核"
channels: ""
---

# 修复：个人订阅到期后，旧 Agent 的历史聊天、成果和文件重新可以访问

## 核心宣传点

个人订阅一过期，用户连自己此前用旧 Agent 产出的东西都打不开了——归档聊天、成果列表和详情、工作区文件全被订阅门禁挡在外面，哪怕账上还有充值积分也没用。这次把这些「读自己已有数据」的入口从订阅校验里摘出来：归档聊天、成果的查看/删除、工作区文件访问不再要求有效订阅，也不额外要求余额。旧 Agent 的模型设置读取、单独改模型以及旧版主模型接口同样去掉了订阅前置限制，改为继续走现有的积分驱动模型目录校验。账号、组织、工作区归属、路径校验和 runtime 就绪检查都保留，共享 helper 默认仍然校验订阅，只对这几个明确入口放开，不是全局开闸。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已上线

## PR 说明

## Summary
- 个人订阅过期后，旧 Agent 的归档聊天、成果列表/详情/删除和工作区文件访问不再要求有效订阅，也不额外要求余额。
- 旧 Agent 的模型设置读取、单独修改模型及旧版主模型接口移除订阅前置限制，继续使用现有积分驱动的模型目录校验。
- 保留账号、组织、工作区/Computer 归属、路径校验及 runtime 就绪检查。共享 helper 默认仍校验订阅，其他运行操作和身份设置修改不在此次放开范围。

## Root cause
旧接口复用的 bot/token 与 ready-bot helper 在查询资源前统一检查订阅有效性，因此即使用户有充值积分，仍会被旧订阅门禁提前拦截。为明确的已有数据/模型入口增加显式选择，避免全局放开共享 helper。

## Test plan
- [x] 512 个相关 pytest 测试通过，覆盖旧模型、成果、归档、共享 helper 与原有 runtime 门禁。
- [x] 新增回归使用真实 helper，验证订阅不满足时仍能读写目标数据，并验证其他用户的 Computer 不可访问、未知模型仍拒绝。
- [x] Ruff、格式、Pyright、import-linter 及提交 hooks 通过。
- [ ] staging/production 实际账号验证；尚未部署。本次只需发布后端。


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `2d46a3f55616f053589b36cd72b8e793813f580e`
- PR: #3894
- 作者：sam-srp
- 日期：2026-09-24T03:11:33Z

### Commit Message

```
fix(billing): unblock legacy agent data and models after expiry (#3894)

## Summary
- 个人订阅过期后，旧 Agent 的归档聊天、成果列表/详情/删除和工作区文件访问不再要求有效订阅，也不额外要求余额。
- 旧 Agent 的模型设置读取、单独修改模型及旧版主模型接口移除订阅前置限制，继续使用现有积分驱动的模型目录校验。
- 保留账号、组织、工作区/Computer 归属、路径校验及 runtime 就绪检查。共享 helper
默认仍校验订阅，其他运行操作和身份设置修改不在此次放开范围。

## Root cause
旧接口复用的 bot/token 与 ready-bot helper
在查询资源前统一检查订阅有效性，因此即使用户有充值积分，仍会被旧订阅门禁提前拦截。为明确的已有数据/模型入口增加显式选择，避免全局放开共享
helper。

## Test plan
- [x] 512 个相关 pytest 测试通过，覆盖旧模型、成果、归档、共享 helper 与原有 runtime 门禁。
- [x] 新增回归使用真实 helper，验证订阅不满足时仍能读写目标数据，并验证其他用户的 Computer 不可访问、未知模型仍拒绝。
- [x] Ruff、格式、Pyright、import-linter 及提交 hooks 通过。
- [ ] staging/production 实际账号验证；尚未部署。本次只需发布后端。
```

来源：SerendipityOneInc/ecap-workspace @ 2d46a3f5，PR #3894，作者 sam-srp。