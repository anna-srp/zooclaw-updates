---
title: "企业咨询表单支持补充业务信息，并拦截个人/临时邮箱"
type: "产品基础功能更新"
priority: "中"
date: "2026-10-23"
status: "待审核"
channels: ""
---

# 企业咨询表单支持补充业务信息，并拦截个人/临时邮箱

## 核心宣传点

企业联系表单新增可选的业务信息字段，最长 5000 字，10 种语言的文案一并改写，中英文提示会引导填写工作流、当前难题、目标和在用系统，便于销售侧判断线索质量。接口侧会基于开源的公共邮箱域名清单（三万余条）拒绝个人邮箱和一次性邮箱注册，校验前会统一大小写并做国际化域名归一，批量条目精确匹配、只对明确属于服务商自有命名空间的情况继承拦截，并且在写入线索日志与发出通知之前执行。前端会显示本地化的邮箱错误提示并保留其余已填字段供修改，域名数据集只留在后端、不下发给浏览器。

## 分级

- 内部：P2
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `19dd49fe757d63088222889297ec163c8a118b2e`
- PR: #4130
- 作者：Shirley151515
- 日期：2026-10-23T08:41:51Z

### Commit Message

```
feat: qualify business contact submissions (#4130)

## Summary

Enterprise contact submissions now accept optional business details up
to 5,000 characters, with revised copy across all 10 locales. Chinese
and English prompts invite workflows, challenges, goals and systems to
connect.

The API rejects public/personal and disposable email providers using the
MIT-licensed Kikobeats/free-email-domains snapshot (31,097 domains;
commit 18d04cbaa077cca754e129a417fbdf780dea332a). Validation normalizes
case and IDNA, matches bulk entries exactly and only inherits blocking
for explicit provider-owned namespaces and runs before lead logging or
Feishu notification. The browser displays a localized email error and
retains the other fields for correction. The domain dataset stays on the
backend, with no runtime external lookup or browser bundle overhead.

## Validation

- 67 backend contact tests passed, including direct API rejection,
uppercase/subdomain/Unicode bypass cases, allowed custom domains,
notification behavior and the 5,000/5,001-character boundary.
- 89 frontend tests passed: all six business-page suites and both
API/error-handling suites.
- Full web/app TypeScript check passed; targeted ESLint, Ruff and
formatting checks passed.
- Web governance guards passed (cache guard reports its existing
bootstrap condition).
- Actual Next.js local page + isolated real FastAPI route: Gmail and
Mailinator rejected; corrected company-domain submission succeeded. Test
webhook disabled.

Previous head `8d13ec16bd161c0687b74d261be9d728501fcc53`: GitHub CI
completed with 28 passing checks, 14 conditional skips, no failures or
pending checks. This includes web build, frontend/backend test and
lint/typecheck jobs, CodeQL and automated reviews.

## Dataset size and deployment

The third-party domain snapshot contributes 31,098 lines to this PR; its
original formatting, MIT license, pinned revision and update
instructions are retained for auditability. The size exception is solely
for this vendored dataset.

Deploy and verify the compatible backend FIRST, then deploy the
frontend. Do not deploy the new frontend against the old backend; on
rollback, revert the frontend first. The existing backend image copies
the app directory, including the dataset. New unknown disposable domains
may evade any static list; this snapshot must be periodically reviewed
and updated. A domain absent from the list is not proof of mailbox
ownership or company affiliation.



## Review follow-up

`f9f8053` fixes shared-registration-domain false positives and bounds
the serialized Feishu notification to 20,000 UTF-8 bytes. Full Chinese
descriptions at 5,000 characters fit; oversized notification text is
explicitly truncated without changing the original submission. New
regression coverage includes Chinese, emoji and JSON escaping. CI for
`f9f8053827332ba4c9fd0d57b1ee1d501bcaf307` completed: 28 passing checks,
14 conditional skips, zero failures or pending checks. Frontend/backend
complete test suites, typechecks and build passed. The Codex review job
may skip content review because of dataset size; human re-review by
tim-srp remains requested.

---------

Co-authored-by: 15 <s15@15deMacBook-Pro.local>
```

