---
title: "团队管理员现在也能单独查看自己的用量明细，不再只能看全组织"
type: "后端功能"
priority: "高"
date: "2026-10-11"
status: "待审核"
channels: ""
---

# 团队管理员现在也能单独查看自己的用量明细，不再只能看全组织

## 核心宣传点

此前 GET /users/credits/usage/records 按调用者当前所属关系取数，团队组织的管理员拿到的永远是整个组织的用量，没有任何办法只看自己。这次在原接口上新增可选的 scope 参数，不新增端点、不改变既有调用方行为：不传或传 org 与现状一致；传 self 时管理员拿到自己加入团队之后的个人用量，口径与计费网关对普通成员的过滤一致。API key 仍以 key 自身范围优先。响应会在 meta.scope 回显生效值，传入未知值在读取前返回 422。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## 备注

前端用量页面需按新参数接入后用户才能在界面上看到「只看自己」的效果。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `28cb0eba66a16d6e0f1709fca8c77cdf1ca40825`
- PR: #4052
- 作者：tim-srp
- 日期：2026-10-11T04:38:21Z

### Commit Message

```
feat(claw-interface): let usage records read only the caller's own usage (#4052)
```

