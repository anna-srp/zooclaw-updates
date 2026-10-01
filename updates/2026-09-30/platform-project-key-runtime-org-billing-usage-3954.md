---
title: "开发者平台 Project Key 打通 Agent/Session 接口：同一组织下所有项目和 Key 共用钱包与用量"
type: "Feature"
priority: "高"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 开发者平台 Project Key 打通 Agent/Session 接口：同一组织下所有项目和 Key 共用钱包与用量

## 核心宣传点

SDK 用的 zwp_live_ Project Key 现在可以直接调用已有的 Agent 和 Session 接口，认证使用 ZooWork 的 owner UID，同一组织下所有 Project 和 Key 的消费全部归到同一个组织计费主体。公开的 pak_ ID 会映射成引擎支持的 32 位 ID，强制校验 owner、组织和项目归属，默认项目的 project_id 仍为空。Key 的创建与重新绑定会加密绑定 owner 令牌，复用 Work 已有的保存和手动 rebind 生命周期，没有新增自动续期。组织初始化时会加密保存首次生成的调用密钥，Agent 读取前后都会核对付款主体。Key、调用方和组织的归属信息完整保留，幂等作用域按组织和项目隔离，组织用量包含共享沙箱费用。另外顺手修了用量页 Key 分组 ID 的转换问题和个人技能在无组织情况下的可见性。只改了 ECAP，引擎和计费网关沿用现有接口。

## 分级

- 内部：P0
- 外部：A
- toB 相关：是
- 发布状态：已随正式 release 上线

## PR 说明

## Summary

SDK 的 `zwp_live_` Project Key 接入现有 Agent/Session API，使用 ZooWork owner
UID 认证，并将所有 Project/Key 的消费归到同一 Org business customer。

- ECAP 将公开 `pak_` ID 映射为 Engine 已支持的 32 位 ID，强制 owner、Org 和
Project，校验资源归属；Default Project 保持 `project_id=null`。
- Key 创建/rebind 加密绑定 owner JWT，复用 Work 的保存和手动 rebind 生命周期；未增加自动续期。
- Org 初始化时加密保存首次生成的 callable LiteLLM secret。Agent 读取保存的 secret，并在读取前后核对
Org payer。拒绝将 Gateway reuse 响应的管理 hash 用作 runtime
secret；初始化重试复用已保存的值，不调用个人 Billing Profile 初始化。
- secret 使用现有 `CONNECTOR_ENCRYPTION_KEY`、AES-GCM、随机 nonce 和 Org/owner
绑定的 AAD。新增私有 Org 字段及首次写入 CAS；公开 DTO 不变。加密配置在首次生成前校验。
- 保留 Key/Actor/Org attribution，按 Org/Project 隔离 idempotency scope；Org
Usage 包含 shared Sandbox 费用，不修改共享 Key 的全局 metadata。
- 修复 Usage Key 分组 ID 转换、个人 Skill null Org 可见性，并补回归测试。

仅修改 ECAP，Engine 和 Billing Gateway 沿用现有接口。前置 ECAP #3945、user-interface
#164 均已合并，base 为 main。

## Validation

- [x] 最终定向回归：**322 passed**，覆盖 Platform 服务、Agent/Skill proxy 和本地普通 Mongo
repositories。Engine/Gateway 使用 mock；普通 Mongo 与真实 CSFLE 的证据分开记录。
- [x] ruff、format、pyright 和 8 个 import contracts 通过；commit hooks 通过。Finn
author/committer 为 `finn-srp <finn@srp.one>`，GitHub 为
`finn930`。仅跳过要求登录名以 `-srp` 结尾并改写全局身份的旧 check-user hook。
- [x] 运行时源码 commit
`31edce2226a2ee5f507198ca666eb6f6d83273ce`（后续仅补验收文档）运行
`ecap-verify-py-ci`：依赖解析、静态/all CI lint、两个 jscpd 检查及 pytest
全部通过。**13,315 passed, 5 skipped, 4 warnings；coverage 89.91%**（4
workers、sysmon、89.5% threshold）。

- [x] 真实 staging CSFLE：当前运行时源码通过 **58 项检查**，涵盖 Default/named/legacy Key
rebind 与 revoke、并发 CAS、撤销优先，以及 Org secret 的 null/缺失字段、并发首次写入、防覆盖和租户绑定。3
Key + 4 Org fixture 全部删除；独立加密进程确认零残留与持久化成功审计。使用已配置的加密客户端和存储加密
key，未部署或调用计费服务。详见
[验证记录](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/platform-runtime-org-usage/docs/staging-validation/2026-09-30-platform-runtime-credentials-csfle.md)。

## Acceptance limits

真实本地 TS SDK → staging 的前一轮已通过 Key 鉴权、创建/启动 Agent、Session 和 Project
get/list 隔离。模型调用曾失败 401：ECAP 丢弃首次 secret 后误用 reuse-path hash；本次代码修复及
mock 回归不代表已完成新的真实模型调用。

前一轮 Usage 503 定位为独立的环境版本问题：当时 staging Gateway beta 尚无已合并的 Usage #76。无需新增
Gateway 代码；验收环境需要提供 #76 的接口，部署需单独授权。

用户已允许重新测试时清理对应坏 Key 数据，不做旧 Key 恢复。历史订单、充值事件、钱包和外部 ledger 保留。本次仅清理了 CSFLE
验证所创建的 7 条独立 fixture。现有应用数据、3 条历史充值订单和 11 条支付事件保留；没有部署或执行新的真实付费调用。

当前 rebind/secret CAS 的真实 CSFLE gate 已通过，staging 存储加密配置也已确认存在。后续仍需部署后的
HTTP/SDK 验收：手动凭据恢复、跨 Org/Project 隔离、实际
LLM/Sandbox/工具消费及重复事件，以及充值、消费、可用余额、Usage 和 ledger 对账。CSFLE fixture
验证不代替真实运行和计费闭环。

## Review disposition

原先的 Usage/Skill 两项代码缺陷已修复。CodeQL #665 仍为已确认并 dismiss 的公开 Key ID
归因映射误报。运行时源码 head `31edce2226` 的 GitHub 检查 18 passed、17 skipped、0
failed。

Codex/Claude 先前要求的真实 CSFLE 验证现已完成，准确源码、环境、58 项结果、清理和独立审计证据已补入仓库。后续
commit 仅更新这三份验证/规格文档，没有 Python、测试或依赖变更，因此保留已通过的全量本地结果，不重复运行同一全量检查。最新文档
head `4a58b46612` 的 Codex review 已确认原 P1 resolved，九个源码 hash 与 checkout
一致，结论 APPROVE。Claude 未提出新代码问题，但仍引用旧上下文称 CSFLE 未完成；该说法与本次 58
项真实检查、独立复核和验证记录不符，不新增代码修复或重复 staging 测试。真实部署/付费闭环仍是单独验收项。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `55e3f7572f5cb02e0fb2a2eb2bb9aa4fc3fbd564`
- PR: #3954
- 作者：finn-srp
- 日期：2026-09-30T11:47:30Z

### Commit Message

```
feat(platform): connect Project Key runtime to Org billing and usage (#3954)

## Summary

SDK 的 `zwp_live_` Project Key 接入现有 Agent/Session API，使用 ZooWork owner
UID 认证，并将所有 Project/Key 的消费归到同一 Org business customer。

- ECAP 将公开 `pak_` ID 映射为 Engine 已支持的 32 位 ID，强制 owner、Org 和
Project，校验资源归属；Default Project 保持 `project_id=null`。
- Key 创建/rebind 加密绑定 owner JWT，复用 Work 的保存和手动 rebind 生命周期；未增加自动续期。
- Org 初始化时加密保存首次生成的 callable LiteLLM secret。Agent 读取保存的 secret，并在读取前后核对
Org payer。拒绝将 Gateway reuse 响应的管理 hash 用作 runtime
secret；初始化重试复用已保存的值，不调用个人 Billing Profile 初始化。
- secret 使用现有 `CONNECTOR_ENCRYPTION_KEY`、AES-GCM、随机 nonce 和 Org/owner
绑定的 AAD。新增私有 Org 字段及首次写入 CAS；公开 DTO 不变。加密配置在首次生成前校验。
- 保留 Key/Actor/Org attribution，按 Org/Project 隔离 idempotency scope；Org
Usage 包含 shared Sandbox 费用，不修改共享 Key 的全局 metadata。
- 修复 Usage Key 分组 ID 转换、个人 Skill null Org 可见性，并补回归测试。

仅修改 ECAP，Engine 和 Billing Gateway 沿用现有接口。前置 ECAP #3945、user-interface
#164 均已合并，base 为 main。

## Validation

- [x] 最终定向回归：**322 passed**，覆盖 Platform 服务、Agent/Skill proxy 和本地普通 Mongo
repositories。Engine/Gateway 使用 mock；普通 Mongo 与真实 CSFLE 的证据分开记录。
- [x] ruff、format、pyright 和 8 个 import contracts 通过；commit hooks 通过。Finn
author/committer 为 `finn-srp <finn@srp.one>`，GitHub 为
`finn930`。仅跳过要求登录名以 `-srp` 结尾并改写全局身份的旧 check-user hook。
- [x] 运行时源码 commit
`31edce2226a2ee5f507198ca666eb6f6d83273ce`（后续仅补验收文档）运行
`ecap-verify-py-ci`：依赖解析、静态/all CI lint、两个 jscpd 检查及 pytest
全部通过。**13,315 passed, 5 skipped, 4 warnings；coverage 89.91%**（4
workers、sysmon、89.5% threshold）。

- [x] 真实 staging CSFLE：当前运行时源码通过 **58 项检查**，涵盖 Default/named/legacy Key
rebind 与 revoke、并发 CAS、撤销优先，以及 Org secret 的 null/缺失字段、并发首次写入、防覆盖和租户绑定。3
Key + 4 Org fixture 全部删除；独立加密进程确认零残留与持久化成功审计。使用已配置的加密客户端和存储加密
key，未部署或调用计费服务。详见
[验证记录](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/platform-runtime-org-usage/docs/staging-validation/2026-09-30-platform-runtime-credentials-csfle.md)。

## Acceptance limits

真实本地 TS SDK → staging 的前一轮已通过 Key 鉴权、创建/启动 Agent、Session 和 Project
get/list 隔离。模型调用曾失败 401：ECAP 丢弃首次 secret 后误用 reuse-path hash；本次代码修复及
mock 回归不代表已完成新的真实模型调用。

前一轮 Usage 503 定位为独立的环境版本问题：当时 staging Gateway beta 尚无已合并的 Usage #76。无需新增
Gateway 代码；验收环境需要提供 #76 的接口，部署需单独授权。

用户已允许重新测试时清理对应坏 Key 数据，不做旧 Key 恢复。历史订单、充值事件、钱包和外部 ledger 保留。本次仅清理了 CSFLE
验证所创建的 7 条独立 fixture。现有应用数据、3 条历史充值订单和 11 条支付事件保留；没有部署或执行新的真实付费调用。

当前 rebind/secret CAS 的真实 CSFLE gate 已通过，staging 存储加密配置也已确认存在。后续仍需部署后的
HTTP/SDK 验收：手动凭据恢复、跨 Org/Project 隔离、实际
LLM/Sandbox/工具消费及重复事件，以及充值、消费、可用余额、Usage 和 ledger 对账。CSFLE fixture
验证不代替真实运行和计费闭环。

## Review disposition

原先的 Usage/Skill 两项代码缺陷已修复。CodeQL #665 仍为已确认并 dismiss 的公开 Key ID
归因映射误报。运行时源码 head `31edce2226` 的 GitHub 检查 18 passed、17 skipped、0
failed。

Codex/Claude 先前要求的真实 CSFLE 验证现已完成，准确源码、环境、58 项结果、清理和独立审计证据已补入仓库。后续
commit 仅更新这三份验证/规格文档，没有 Python、测试或依赖变更，因此保留已通过的全量本地结果，不重复运行同一全量检查。最新文档
head `4a58b46612` 的 Codex review 已确认原 P1 resolved，九个源码 hash 与 checkout
一致，结论 APPROVE。Claude 未提出新代码问题，但仍引用旧上下文称 CSFLE 未完成；该说法与本次 58
项真实检查、独立复核和验证记录不符，不新增代码修复或重复 staging 测试。真实部署/付费闭环仍是单独验收项。
```

来源：SerendipityOneInc/ecap-workspace @ 55e3f757，PR #3954，作者 finn-srp。
