---
title: "修复：跨组织分享的 Agent 包装过来后技能缺依赖环境、Fire 按钮在 Engine 断连时误禁用"
type: "Bug Fix"
priority: "高"
date: "2026-09-10"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：跨组织分享的 Agent 包装过来后技能缺依赖环境、Fire 按钮在 Engine 断连时误禁用

## 核心宣传点

分享安装这条链路上的两个问题，今天一起修掉。

**一、共享 Pack 现在会带上它自己那份精确的 Environment。** 此前安装器对非官方 Pack、跨组织分享的情况会**丢弃 Environment pin**：技能装过来了，但它依赖的那套环境没跟着，而作者自己预览时用的却是专门构建的环境——于是「在作者那儿好好的，装到我这儿就跑不起来」。现在在原有的 Pack 访问校验之后，安装和更新都会先为接收方组织授权那份与已批准运行时 archive 匹配的 Environment build，然后才创建/更新 Agent。

顺带修了存量：更新时即使 archive SHA 没变，也会**比对实际的 Environment pin**，所以之前那些已经装好但回退到基础环境的实例，可以通过正常的更新/重试路径自行恢复。绑定本来就正确的则保持 no-op，不做无意义的改动。（根因的另一半：同 SHA 的提前 return 把存量错误绑定的修复也一起跳过了。）

**二、共享 Agent 卡片上的 Fire / Update 不再乱禁用。** 共享卡片此前用的是**全局连接锁**，可是 Engine 侧的卸载并不需要那条 OpenClaw WebSocket 连接——结果入口按钮和它后面的确认流程判断不一致：确认流程用的是运行时感知的资格判断，入口却被全局锁挡住。现在共享卡片的 Fire 与 Update 权限统一从现有的工作区资格函数派生，Computer 连接要求和更新/同步锁这些该保留的限制照旧保留。

## 原始内容

### fix(agents): retain exact environments for shared packs (#3694)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `b8ff6694`
- PR: #3694
- 作者: kaka-srp
- 日期: 2026-09-10T12:08:21Z

Shared Engine Packs now keep the exact Environment build that matches their approved runtime archive. After the existing Pack access checks, installation and update authorize that build for the receiving organization before creating or updating the Agent. Updates also compare the actual Environment pin when the archive SHA is unchanged, allowing previously installed instances that fell back to the base Environment to recover through the normal update/retry path. An already-correct binding remains a no-op.

根因（PR 原文）：The installer discarded Environment pins for nonofficial Packs shared across organizations. Skills arrived without their dependency environment, while author preview continued to use the dedicated build. The same-SHA early return also skipped repair of existing incorrect bindings.

验证：213 项针对性 runtime selection / install / lifecycle / Engine client 测试通过，含同提交运行时修订与失败传播；Python 静态检查与 pre-commit 通过；CI 后端 10,868 passed / 5 skipped，全部 ECAP CI 与自动复审检查通过；本地 Python client → 配套 Controld → 共享 PostgreSQL 实链路验证了精确授权、重试、SHA/版本升级、Agent 更新与卸载/重装，测试资源已清理、本地服务分支已还原。

### fix(agents): respect runtime permissions for shared agent actions (#3685)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `a0967b39`
- PR: #3685
- 作者: tim-srp
- 日期: 2026-09-10T13:33:13Z

Allow shared Engine agents to be fired while the OpenClaw WebSocket is disconnected. Derive shared card Fire and Update permissions from the existing workspace eligibility function, preserving Computer connection requirements and update/sync locks.

根因（PR 原文）：Shared cards used the global connection lock even though Engine uninstall does not require that connection. The confirmation flow already used runtime-aware eligibility, so the entry point and confirmation disagreed.

验证：31 项针对性测试通过（MyAgentsClient、其 view model、agent eligibility），含断连 Engine/Computer agent、同步中、当前/其他工作区更新与实际 Fire 菜单动作的回归覆盖；改动文件 ESLint、前端治理检查、`git diff --check` 通过。完整本地 TypeScript 检查被 chat-ui 依赖/类型解析问题阻塞（改动文件无报错，以 CI 为准）。纯前端改动，无需后端部署或数据迁移。

## 备注

发布状态：两条均为已合并待发版（尚未包含在 `ecap-v0.19.3-release` 中）。

对外发布注意：第一条对「装了同事/朋友分享的 Agent 但技能跑不起来」的用户是实质修复，且**存量实例可以通过点一次更新自行恢复**——这句值得在 changelog 里明确写出来，能省掉一批工单。
