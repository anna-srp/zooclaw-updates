---
title: "修复：加入企业版时个人订阅会正确释放，不再重复占用"
type: Bug Fix
priority: 中
date: 2026-08-17
status: "待审核"
channels: ""
---

## 核心宣传点

个人用户接受企业邀请、切换到企业账号时，原来的个人订阅协议现在会被正确终止并留下审计记录，不会再出现个人订阅和企业席位并存、状态错乱的情况。

## 原始内容

**Commit**: `f103dbe5` — fix(billing): release personal agreement on enterprise handoff (#3407)
**作者**: kaka-srp ｜ **日期**: 2026-08-17T07:46:13Z
**PR body**: （空）

改动文件（enterprise handoff / 个人订阅停止链路）：

```
services/claw-interface/app/database/account_org_repo.py                       (+52/-12)
services/claw-interface/app/database/subscription_agreement_history_repo.py    (+37/-1)
services/claw-interface/app/schema/billing_v2.py                               (+2/-0)
services/claw-interface/app/services/billing_v2/subscription_agreement_upsert.py (+9/-0)
services/claw-interface/app/services/org/enterprise_invite_handoff.py          (+32/-2)
services/claw-interface/app/services/org/personal_subscription_stop.py         (+131/-2)
+ 5 个单元测试文件
```

关键变更：`swap_active_membership` 支持在切换归属组织的同一事务内提交 Agreement 投影更新（新增 `AgreementProjectionUpdate` dataclass、CAS 校验 `SubscriptionAgreementProjectionCasMissError`）；`SubscriptionAgreementDocument` 新增 `superseded_reason` 与 `superseded_correlation_id` 字段，用于记录个人协议因企业交接而终止的原因与关联 ID，并同步写入 billing 审计事件集合。
