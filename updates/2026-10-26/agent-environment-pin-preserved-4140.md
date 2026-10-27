---
title: "修复：绑定 Agent 运行时身份时自定义环境被改回默认，沙盒里命令消失"
type: "Bug Fix"
priority: "中"
date: "2026-10-26"
status: "待审核"
channels: ""
---

# 修复：绑定 Agent 运行时身份时自定义环境被改回默认，沙盒里命令消失

## 核心宣传点

为 Agent 创建运行时身份投影时，系统会按原始声明复制一份配置，但原始声明不一定带着实际的 Environment 绑定，于是引擎在生成候选配置时重新选中了默认环境——结果就是你明明指定了自定义环境，绑定身份之后沙盒里却缺少该环境提供的命令。现在候选声明会用当前实际解析出的 Environment ID 和精确版本，覆盖缺失或过期的环境字段，MCP 配置迁移走同一处逻辑，同样保留绑定。本次只改身份投影的候选配置和回归测试，不新增配置项、接口或数据库迁移。

## 分级

- 内部：P1
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `d35586415a80d33a34a2fc66afccf4a65d6793b3`
- PR: #4140
- 作者：kaka-srp
- 日期：2026-10-26T07:37:54Z

### Commit Message

```
fix(agents): preserve Environment pins during runtime identity projection (#4140)

## Summary

创建 Agent 运行时身份投影时保留当前解析出的 Environment ID
和精确版本，避免只为绑定身份而重建配置，却把自定义环境切换为默认环境。MCP 配置迁移走同一处逻辑，也保留该绑定。

## Root cause

`source_declaration` 不一定包含实际 Environment 绑定。staging E2B canary
的初始配置使用自定义 Environment `@2`，但身份投影复制声明时没有补上解析出的绑定，Engine 在创建候选配置时重新选中了默认
Environment `@21`，因此沙盒缺少自定义环境提供的命令。候选声明现在以当前实际绑定覆盖缺失或陈旧的 Environment 字段。

本 PR 仅修改身份投影的候选配置与回归测试；不增加配置项、接口或数据库迁移。

## Test plan

- [x] 修复前先运行回归验证：4 项环境保留断言失败，其他 4 项通过。
- [x] 修复后相关 3 个测试文件共 23 项通过，覆盖声明缺失环境、声明版本陈旧、声明指向不同环境、MCP 迁移、凭据恢复和撤销行为。
- [x] `bash scripts/verify-py.sh` 通过：Ruff 检查和格式、Pyright、8 条导入契约。
- [ ] 修复版本尚未发布；发布 staging 后需重跑 E2B Environment 定向验收，不能将本地测试视为线上验收通过。

Related: https://github.com/SerendipityOneInc/zooclaw-engine/issues/2102
```
