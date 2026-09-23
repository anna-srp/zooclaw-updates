---
title: "Agent 构建完成后自动补全名称、描述与头像，并给出「用它新建任务」的直达入口"
type: "新功能上线"
priority: "高"
date: "2026-09-22"
status: "待审核"
channels: ""
---

# Agent 构建完成后自动补全名称、描述与头像，并给出「用它新建任务」的直达入口

## 核心宣传点

Build 出来的 Agent 以前经常是「建完了但不知道接下来干什么」：名字是临时的，也没人告诉你去哪儿用它。这次新建 Agent 时会主动把名称、描述、头像和快捷入口补齐，构建完成的回执里直接给出一条可信的「当前 Agent → 新任务」路径，不再要求你回去汇报测试结果。同时把「共用的业务依据」「每次任务要填的输入」「只属于你的私人记录」三类信息的职责分清了：记忆不等于必须先做一轮 onboarding，私人记录只写在合适的运行时作用域里，不会跟着被复制的源一起扩散。另外修了初始创建时默认技能的语义——没指定就不带 skills，显式传空列表才代表关闭；以及创建中途失败时的资源回收，失败残留记录清理后可以重试。完整体验需要 Engine 侧配套一起部署。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary

- 按业务目标梳理需求，明确普通交互、业务方法和可选 persona 文件的职责；不增加固定问卷、文件清单、通用领域特例或发布门槛。
- 新建 Agent 主动完善名称、描述、头像和快捷入口；提交回执提供可信的「当前 Agent → 新任务」使用路径，不要求用户返回汇报测试。
- 区分共用业务依据、任务输入和私人记录；记忆不等于必须 onboarding，私人记录使用适当的运行时作用域，不写入会被复制的源。
- 修复初始创建的默认技能语义：未指定时省略 skills，显式空列表仍表示关闭；不批量修改存量 Agent。
- 增加本地真实行为记录器的 ECAP 入口和人工检查记录；修复创建中途失败时的资源回收，清理失败保留记录可重试。

## Scope / rollout

- 配套 Engine
PR：https://github.com/SerendipityOneInc/zooclaw-engine/pull/1580 。其中包含
Build overlay、工具说明与非 active 模式首用隔离；完整体验需要两边部署。
- 不改产品页面、业务数据库 schema、共享状态权限或线上评测流程；脚本仅用于本地专属测试资源。
- 本 PR 的新增行包含设计文档、历次人工检查记录和本地测试工具，不等于新增线上流程。

## Test plan

- [x] 本轮 ECAP 六个定向测试文件共 191 项通过，含新增 14 项资源创建失败/取消/清理重试回归，无外部 I/O。
- [x] Ruff、格式、Pyright、import-linter 和提交前检查通过。
- [x] 重新 code-review；已修复创建失败清理和删除结果不确定后的幂等重试问题，未因此收紧 Build 提示。
- [x] 已有真实 Terra 构建及普通任务记录由人工检查，不使用模型评审，不将运行成功或字符串匹配当作行为通过。
- [x] 提交 `f27def4c3` 的完整 CI 和增量代码复审通过；没有未处理的已确认缺陷。
- [ ] staging/prod 的完整资源、渠道与真实分享安装端到端验收。

## Validation limits

历史记录明确保留跨任务记忆复用、入口提示及输出遵循的波动，不能声称所有场景已稳定通过。Builder 的 run_test
仍是独立单轮，evaluation 不开放共享记忆，preview 可能影响真实状态；本次不扩展测试权限或增加自动模型评分。

本地行为记录器仅替换 Mongo 仓储，使用真实 Engine/模型和业务服务；不能替代 Mongo/CSFLE、账号创建、页面或真实分享
API 验收。localhost 全栈已供用户手工实测，但未据此宣称全面稳定性证明。详见
docs/validation/2026-09-21-agent-build-outcomes-local.md。

## 本次追加：身份归属与自测证据边界

- 明确身份写入 `IDENTITY.md`，`AGENTS.md` 承担普通交互与能力路由，`SOUL.md`
承担语气；不新增文件必填校验，不批量补写存量 Agent。
- 为 `authoring.run_test` 回执增加 `verification_scope`，区分隔离 evaluation
与有真实副作用的 preview。测试中缺少依赖不直接证明普通任务需要用户配置；不修改权限、passed 或 onboarding 语义。
- 自测保持按改动风险选择，不引入固定问卷、统一开场或复杂测试流水线。
- 本次定向回归：ECAP 两文件 62 项通过；Ruff、格式、Pyright、import-linter 通过。
- 本次真实模型完整复测尚未完成；localhost 全栈已重载并供用户实测，服务健康不等于行为验收。此前 CI/review
结论仅适用于对应旧提交，新提交以重新运行的检查为准。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `01c90b007539b088288b1c43d5963e5900101041`
- PR: #3846
- 作者：kaka-srp
- 日期：2026-09-22T03:02:29Z

### Commit Message

```
fix(agents): make build outcomes usable and handoffs clear (#3846)

## Summary

- 按业务目标梳理需求，明确普通交互、业务方法和可选 persona 文件的职责；不增加固定问卷、文件清单、通用领域特例或发布门槛。
- 新建 Agent 主动完善名称、描述、头像和快捷入口；提交回执提供可信的「当前 Agent → 新任务」使用路径，不要求用户返回汇报测试。
- 区分共用业务依据、任务输入和私人记录；记忆不等于必须 onboarding，私人记录使用适当的运行时作用域，不写入会被复制的源。
- 修复初始创建的默认技能语义：未指定时省略 skills，显式空列表仍表示关闭；不批量修改存量 Agent。
- 增加本地真实行为记录器的 ECAP 入口和人工检查记录；修复创建中途失败时的资源回收，清理失败保留记录可重试。

## Scope / rollout

- 配套 Engine
PR：https://github.com/SerendipityOneInc/zooclaw-engine/pull/1580 。其中包含
Build overlay、工具说明与非 active 模式首用隔离；完整体验需要两边部署。
- 不改产品页面、业务数据库 schema、共享状态权限或线上评测流程；脚本仅用于本地专属测试资源。
- 本 PR 的新增行包含设计文档、历次人工检查记录和本地测试工具，不等于新增线上流程。

## Test plan

- [x] 本轮 ECAP 六个定向测试文件共 191 项通过，含新增 14 项资源创建失败/取消/清理重试回归，无外部 I/O。
- [x] Ruff、格式、Pyright、import-linter 和提交前检查通过。
- [x] 重新 code-review；已修复创建失败清理和删除结果不确定后的幂等重试问题，未因此收紧 Build 提示。
- [x] 已有真实 Terra 构建及普通任务记录由人工检查，不使用模型评审，不将运行成功或字符串匹配当作行为通过。
- [x] 提交 `f27def4c3` 的完整 CI 和增量代码复审通过；没有未处理的已确认缺陷。
- [ ] staging/prod 的完整资源、渠道与真实分享安装端到端验收。

## Validation limits

历史记录明确保留跨任务记忆复用、入口提示及输出遵循的波动，不能声称所有场景已稳定通过。Builder 的 run_test
仍是独立单轮，evaluation 不开放共享记忆，preview 可能影响真实状态；本次不扩展测试权限或增加自动模型评分。

本地行为记录器仅替换 Mongo 仓储，使用真实 Engine/模型和业务服务；不能替代 Mongo/CSFLE、账号创建、页面或真实分享
API 验收。localhost 全栈已供用户手工实测，但未据此宣称全面稳定性证明。详见
docs/validation/2026-09-21-agent-build-outcomes-local.md。

## 本次追加：身份归属与自测证据边界

- 明确身份写入 `IDENTITY.md`，`AGENTS.md` 承担普通交互与能力路由，`SOUL.md`
承担语气；不新增文件必填校验，不批量补写存量 Agent。
- 为 `authoring.run_test` 回执增加 `verification_scope`，区分隔离 evaluation
与有真实副作用的 preview。测试中缺少依赖不直接证明普通任务需要用户配置；不修改权限、passed 或 onboarding 语义。
- 自测保持按改动风险选择，不引入固定问卷、统一开场或复杂测试流水线。
- 本次定向回归：ECAP 两文件 62 项通过；Ruff、格式、Pyright、import-linter 通过。
- 本次真实模型完整复测尚未完成；localhost 全栈已重载并供用户实测，服务健康不等于行为验收。此前 CI/review
结论仅适用于对应旧提交，新提交以重新运行的检查为准。
```

来源：SerendipityOneInc/ecap-workspace @ 01c90b00，PR #3846，作者 kaka-srp。
