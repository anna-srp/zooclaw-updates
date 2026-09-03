---
title: "钉钉可以接入 Engine Agent 了：扫码绑定，几步接完"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-02"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---

# 钉钉可以接入 Engine Agent 了：扫码绑定，几步接完

## 核心宣传点

Engine Agent 的渠道列表里新增钉钉（DingTalk）。绑定默认走扫码：页面出二维码，用钉钉扫一下完成授权即可，不用先去开放平台翻配置；如果扫码路径走不通，也保留手工填 `clientId` / `clientSecret` 的兜底方式。

底层复用了已经跑熟的 v1 钉钉注册协议，但 Engine 的绑定会话单独存储，只有绑定成功的渠道才会以 `dingtalk` 平台写入 ACS，产品侧平台标识 `dingtalk-connector` 在列表、创建、更新、删除各条路径上做了统一映射。扫码轮询加了工作区级归属校验、终态原子认领和跨 Pod 的轮询间隔控制，避免多实例同时轮询把一个绑定会话抢乱或重复认领。原有的 v1 钉钉流程完全不动，老用户不受影响。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `7de5eface078225d02b0304a579246086d0f2aca`
- PR: #3624
- 作者: kaka-srp
- 日期: 2026-09-02T11:34:51Z

### Commit Message

```
feat(channels): add DingTalk to engine agents (#3624)

## Linear

N/A — no issue was provided for this change.

## Summary

- expose DingTalk as a supported Engine channel in ECAP, with QR setup
as the default and manual `clientId`/`clientSecret` entry as fallback
- reuse the existing v1 DingTalk registration protocol while storing
Engine setup sessions separately and writing successful channels only to
ACS as platform `dingtalk`
- map the product platform `dingtalk-connector` across
list/create/update/remove, and protect QR polling with workspace-scoped
ownership, atomic terminal claims, and cross-pod interval gating
- preserve the legacy v1 flow unchanged; final agent review found no
scope expansion or redundant implementation

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh <changed paths>` — 118 passed, 69
skipped
- [x] focused backend channel/route/v1 suite — 181 passed
- [x] expanded Engine setup/session regression suite — 103 passed
- [x] focused frontend DingTalk/channel suite — 60 passed
- [x] frontend and Python source/test duplication checks
- [x] Python file-length, complexity, dead-code, Ruff, Pyright, ESLint,
TypeScript, and import-contract gates
- [ ] live DingTalk/Redis/ACS smoke (requires deployed credentials and
infrastructure)
```

### PR Body

```
## Linear

N/A — no issue was provided for this change.

## Summary

- expose DingTalk as a supported Engine channel in ECAP, with QR setup as the default and manual `clientId`/`clientSecret` entry as fallback
- reuse the existing v1 DingTalk registration protocol while storing Engine setup sessions separately and writing successful channels only to ACS as platform `dingtalk`
- map the product platform `dingtalk-connector` across list/create/update/remove, and protect QR polling with workspace-scoped ownership, atomic terminal claims, and cross-pod interval gating
- preserve the legacy v1 flow unchanged; final agent review found no scope expansion or redundant implementation

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh <changed paths>` — 118 passed, 69 skipped
- [x] focused backend channel/route/v1 suite — 181 passed
- [x] expanded Engine setup/session regression suite — 103 passed
- [x] focused frontend DingTalk/channel suite — 60 passed
- [x] frontend and Python source/test duplication checks
- [x] Python file-length, complexity, dead-code, Ruff, Pyright, ESLint, TypeScript, and import-contract gates
- [ ] live DingTalk/Redis/ACS smoke (requires deployed credentials and infrastructure)

```


## 备注

实机 DingTalk / Redis / ACS 冒烟测试需部署环境凭证，尚未在 CI 中覆盖。
