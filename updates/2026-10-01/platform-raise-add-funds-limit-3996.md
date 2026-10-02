---
title: "开发者平台单次充值上限从 500 美元提高到 1,000 美元"
type: "体验优化"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: "Discord+changelog"
---

# 开发者平台单次充值上限从 500 美元提高到 1,000 美元

## 核心宣传点

开发者平台的 Add funds 单次上限从 $500 提到 $1,000（即 100,000 美分）。接口请求上限、后端策略、前端响应结构、预览用的 fixture 和测试全部同步对齐，大额充值不用再分多次操作。

## 分级

- 内部：P2
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary / 变更
- Raise the Platform Add funds maximum from $500 to $1,000 ($100,000 cents). / 将 Platform 单次充值上限从 500 美元提高到 1,000 美元。
- Align the API request limit, backend policy, frontend response schema, preview fixture, and test fixture. / 同步请求校验、后端策略、前端响应校验及预览与测试数据。
- Preserve old frontend bundles: Billing GET defaults to the $500 advertised maximum and returns $1,000 only when the new client sends its capability header. / 旧版前端仍收到 500 美元上限；新版前端声明能力后才收到 1,000 美元上限。
- Forward that capability header through the Platform Worker proxy. / Platform Worker 代理转发该能力标识。

## Root cause / 原因
The $500 limit was enforced independently by the Platform backend and frontend response schema. Updating only one side would leave a displayed amount that could not be submitted, or an API response that the frontend rejected. / 原上限分别写在后端和前端校验中，只修改单侧会导致展示与提交不一致。

An older open or cached frontend bundle also rejects a $1,000 Billing GET response. The new capability header keeps that response at $500 for old clients regardless of backend deployment order. / 旧版或已缓存的前端也会拒绝返回 1,000 美元上限的 Billing 响应；能力标识让旧客户端在任意部署顺序下继续收到 500 美元上限。

## Test plan / 验证
- [x] Backend capability tests: 62 passed; billing route tests: 3 passed, including $1,000 accepted, $1,000.01 rejected, and old/new client negotiation.
- [x] Platform router and preview tests: 52 passed, including an old server response with the new client header.
- [x] Worker proxy and Platform router tests: 56 passed, including upstream forwarding of the capability header.
- [x] Platform TypeScript typecheck and changed-file ESLint passed.
- [x] Python Ruff and commit hooks passed.
- [ ] Full backend pre-push verification: the isolated worktree dependency download stalled; CI will run the authoritative backend gate.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `f7004fd6f1c211422aec924c02f96803e10960e8`
- PR: #3996
- 作者：david-srp
- 日期：2026-10-01T19:55:44Z

### Commit Message

```
fix(platform): raise Add funds limit to $1,000 / 提高充值上限 (#3996)

## Summary / 变更
- Raise the Platform Add funds maximum from $500 to $1,000 ($100,000
cents). / 将 Platform 单次充值上限从 500 美元提高到 1,000 美元。
- Align the API request limit, backend policy, frontend response schema,
preview fixture, and test fixture. / 同步请求校验、后端策略、前端响应校验及预览与测试数据。
- Preserve old frontend bundles: Billing GET defaults to the $500
advertised maximum and returns $1,000 only when the new client sends its
capability header. / 旧版前端仍收到 500 美元上限；新版前端声明能力后才收到 1,000 美元上限。
- Forward that capability header through the Platform Worker proxy. /
Platform Worker 代理转发该能力标识。

## Root cause / 原因
The $500 limit was enforced independently by the Platform backend and
frontend response schema. Updating only one side would leave a displayed
amount that could not be submitted, or an API response that the frontend
rejected. / 原上限分别写在后端和前端校验中，只修改单侧会导致展示与提交不一致。

An older open or cached frontend bundle also rejects a $1,000 Billing
GET response. The new capability header keeps that response at $500 for
old clients regardless of backend deployment order. / 旧版或已缓存的前端也会拒绝返回
1,000 美元上限的 Billing 响应；能力标识让旧客户端在任意部署顺序下继续收到 500 美元上限。

## Test plan / 验证
- [x] Backend capability tests: 62 passed; billing route tests: 3
passed, including $1,000 accepted, $1,000.01 rejected, and old/new
client negotiation.
- [x] Platform router and preview tests: 52 passed, including an old
server response with the new client header.
- [x] Worker proxy and Platform router tests: 56 passed, including
upstream forwarding of the capability header.
- [x] Platform TypeScript typecheck and changed-file ESLint passed.
- [x] Python Ruff and commit hooks passed.
- [ ] Full backend pre-push verification: the isolated worktree
dependency download stalled; CI will run the authoritative backend gate.
```

来源：SerendipityOneInc/ecap-workspace @ f7004fd6，PR #3996，作者 david-srp。
