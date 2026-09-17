---
title: "fix(agent-builder): 新建 Agent 默认命名为 Untitled Agent (#3753)"
type: "体验优化"
priority: "中"
date: "2026-09-16"
status: "待审核"
channels: ""
---

# fix(agent-builder): 新建 Agent 默认命名为 Untitled Agent (#3753)

## 核心宣传点

## 修复内容

新建 Agent 统一使用 `Untitled Agent` 作为默认名称。无论创建时是否填写需求，发送第一条消息后都保留该名称，用户可以通过现有入口手动改名。

## 原因

原逻辑会将初始需求或首条消息直接作为名称，导致未命名 Agent 显示整段需求文本。本次仅统一默认值并移除首条消息自动改名逻辑，不新增接口、状态字段或 LLM 调用。初始需求仍正常保存，旧项目与复制项目的名称不变。

## 验证

- [x] Agent Builder 前端测试：80 项通过，覆盖首条消息不触发改名及原有手动改名流程。
- [x] Agent Builder 后端测试：196 项通过，覆盖空白创建与带初始需求创建时的默认名称。
- [x] `git diff --check` 通过。

修改涉及前后端，需要同时发布才能获得完整行为。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `62dacee8de7cdef8871aa072c4c9c4f9d328fe88`
- PR: #3753
- 作者：lynn Zhuang
- 日期：2026-09-16T10:03:03Z

### Commit Message

```
fix(agent-builder): 新建 Agent 默认命名为 Untitled Agent (#3753)

## 修复内容

新建 Agent 统一使用 `Untitled Agent`
作为默认名称。无论创建时是否填写需求，发送第一条消息后都保留该名称，用户可以通过现有入口手动改名。

## 原因

原逻辑会将初始需求或首条消息直接作为名称，导致未命名 Agent
显示整段需求文本。本次仅统一默认值并移除首条消息自动改名逻辑，不新增接口、状态字段或 LLM
调用。初始需求仍正常保存，旧项目与复制项目的名称不变。

## 验证

- [x] Agent Builder 前端测试：80 项通过，覆盖首条消息不触发改名及原有手动改名流程。
- [x] Agent Builder 后端测试：196 项通过，覆盖空白创建与带初始需求创建时的默认名称。
- [x] `git diff --check` 通过。

修改涉及前后端，需要同时发布才能获得完整行为。
```
