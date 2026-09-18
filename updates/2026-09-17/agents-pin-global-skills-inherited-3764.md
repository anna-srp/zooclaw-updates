---
title: "fix(agents): pin effective global skills as inherited refs on first skill declaration (#3764)"
type: "Bug 修复"
priority: "高"
date: "2026-09-17"
status: "待审核"
channels: ""
---

# fix(agents): pin effective global skills as inherited refs on first skill declaration (#3764)

## 核心宣传点

修复自进化 Agent 首次声明自建技能后，22 个平台全局技能（含知识库）全部静默消失的问题：全局技能会以继承引用的方式固定下来，不会再被顶掉。

## PR 说明

## 问题

self-evolving agent 在 Build 里首次声明任何自建技能后,**全部 22 个平台全局技能(含 `knowledge-base`)静默从可见技能面消失**。引擎契约:`declared.skills` 一旦存在(即使 `[]`)就停用全局技能自动启用(spec `docs/superpowers/specs/2026-09-10-unified-agents-navigation.md`)。

线上实例 `agt_01m2mwrp8p1s27v7eyjd8b11ms`(挂知识库 `eab504…`):Build AI 为它生成 prompt-only 技能 `marketing-kb-service` 后,终端(active)会话 4 个、`kb_search` 调用 **0** 次——模型不知道自己有检索工具;而 authoring 会话(会翻文件系统)自行找到脚本检索成功(7 调 5 中),证明能力/权限/数据全部健康,唯独可见性被声明动作剥离。详见 #3763。

## 根因

既定设计(同 spec:"**Preserve effective global skill bindings when projecting source skills**")要求投影 source skills 时把生效全局物化为只读继承引用(`inherited-skills.json`)。该机制在 **legacy 采编路径已实现**(`agent_baseline_adoption` 从 `resolved_skill_pins` 填充),但**新建定义路径从未实现**——首次声明自建技能时 `materialize_skills` 只产出自建绑定,基线全局被丢弃。实现缺口,非设计变更。

## 修复

收口在 `materialize_skills`(所有声明路径的共同漏斗):当 source 首次引入 source-owned 技能、而 agent 活跃配置仍在自动启用基线上时,把 `active_agent.resolved_skill_pins` 合成为 `source.inherited_skills`(只读、`source_owned=False`),声明列表 = 继承全局 + 自建。

- `active_agent` 由两个调用点(change_set / authoring_gateway)传入**它们本就已获取的** `EngineAgentDetail`,零额外 engine 调用;
- create 路径(engine agent 尚不存在)不传 → 跳过;
- 四重护栏:source 已有继承引用 / `skills_explicit`(显式自管)/ 上一 revision 已声明 / 活跃配置已离开基线(含历史 `[]`)——**已有声明永不被复活**,显式清空语义不变;
- 快照被就地写入继承引用 → 存入 revision → 后续 commit 从 source 直接派生 `inherited-skills.json`(只读校验已有)。

## 测试

`tests/unit/test_skill_materialization_inherited.py` 6 条:首次声明合成基线(含 `inherited-skills.json` 派生)/ 无 active(create 路径)跳过 / 已离开基线不复活 / `skills_explicit` 跳过 / 已有声明历史跳过 / 无自建技能不声明。
本地:pyright 0 错、ruff/format/import-linter 全过、相关单测 18/18 绿。

## 存量

已中招的 3 个 agent(#3763 列出)不自愈,按 issue 中迁移方案单独处理;#3763 同时追踪 C1(KB 依赖 fail-closed 校验)与 lockfile 时鲜性设计议题。

Fixes #3763

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `a9d4fd0b1168123977aa9c835f167a657b25bc16`
- PR: #3764
- 作者：kyle-srp
- 日期：2026-09-17T06:24:04Z

### Commit Message

```
fix(agents): pin effective global skills as inherited refs on first skill declaration (#3764)

## 问题

self-evolving agent 在 Build 里首次声明任何自建技能后,**全部 22 个平台全局技能(含
`knowledge-base`)静默从可见技能面消失**。引擎契约:`declared.skills` 一旦存在(即使
`[]`)就停用全局技能自动启用(spec
`docs/superpowers/specs/2026-09-10-unified-agents-navigation.md`)。

线上实例 `agt_01m2mwrp8p1s27v7eyjd8b11ms`(挂知识库 `eab504…`):Build AI 为它生成
prompt-only 技能 `marketing-kb-service` 后,终端(active)会话 4 个、`kb_search` 调用
**0** 次——模型不知道自己有检索工具;而 authoring 会话(会翻文件系统)自行找到脚本检索成功(7 调 5
中),证明能力/权限/数据全部健康,唯独可见性被声明动作剥离。详见 #3763。

## 根因

既定设计(同 spec:"**Preserve effective global skill bindings when projecting
source skills**")要求投影 source skills
时把生效全局物化为只读继承引用(`inherited-skills.json`)。该机制在 **legacy
采编路径已实现**(`agent_baseline_adoption` 从 `resolved_skill_pins`
填充),但**新建定义路径从未实现**——首次声明自建技能时 `materialize_skills`
只产出自建绑定,基线全局被丢弃。实现缺口,非设计变更。

## 修复

收口在 `materialize_skills`(所有声明路径的共同漏斗):当 source 首次引入 source-owned 技能、而
agent 活跃配置仍在自动启用基线上时,把 `active_agent.resolved_skill_pins` 合成为
`source.inherited_skills`(只读、`source_owned=False`),声明列表 = 继承全局 + 自建。

- `active_agent` 由两个调用点(change_set / authoring_gateway)传入**它们本就已获取的**
`EngineAgentDetail`,零额外 engine 调用;
- create 路径(engine a
```
