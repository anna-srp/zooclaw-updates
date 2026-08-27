---
title: "新版 Agent 运行时（V2）正式成为所有账号的默认运行环境"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-26"
status: "待审核"
channels: ""
---

# 新版 Agent 运行时（V2）正式成为所有账号的默认运行环境

## 核心宣传点

此前需要逐个账号开通的新版 Agent 运行时，现在对所有账号默认生效，不用再等灰度名单。少数明确要求暂缓迁移的账号仍按例外清单保留在老版本上，可随时切换过来。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `dec93c8767a18760a4015d98ea12f250d7aa3d2c`
- PR: #3525
- 作者: kaka-srp
- 日期: 2026-08-26T06:44:05Z

### Commit Message

```
feat(agents): make v2 the default runtime (#3525)

## Summary

- make Agent V2 the default runtime for every account while the global
V2 switch is enabled
- keep a temporary Vault-backed UID exception list for the explicitly
deferred V1 accounts
- remove obsolete email-allowlist deployment wiring
- verify exception values remain outside Git and are injected through
the Vault-managed secret

## Validation

- `bash scripts/verify-py.sh` with the Python 3.12 backend toolchain
(Ruff, Pyright, import contracts)
- 74 relevant unit tests covering V2 access, deployment wiring, routes,
main-agent behavior, and builder runtime services
- post-rebase access and Vault-wiring suite: 14 passed
- production Vault sync checked read-only: exception key present with
the expected five-entry set; values were not exposed or committed
```

### PR Description

```
## Summary

- make Agent V2 the default runtime for every account while the global V2 switch is enabled
- keep a temporary Vault-backed UID exception list for the explicitly deferred V1 accounts
- remove obsolete email-allowlist deployment wiring
- verify exception values remain outside Git and are injected through the Vault-managed secret

## Validation

- `bash scripts/verify-py.sh` with the Python 3.12 backend toolchain (Ruff, Pyright, import contracts)
- 74 relevant unit tests covering V2 access, deployment wiring, routes, main-agent behavior, and builder runtime services
- post-rebase access and Vault-wiring suite: 14 passed
- production Vault sync checked read-only: exception key present with the expected five-entry set; values were not exposed or committed


```
