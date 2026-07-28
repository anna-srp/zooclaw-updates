---
title: Agent 自带 Skill 现已真正注册并生效
type: 产品基础功能更新
priority: 中
date: 2026-07-27
status: 待审核
channels: ""
---

## 核心宣传点

修复了一个影响面很广的问题：此前 Agent Pack 自带的 Skill 虽然被打进了运行环境，却从未注册进引擎，导致模型根本"看不到"这些技能、永远不会触发。现在这些 pack 自带 Skill 会走规范注册流程写入引擎，并在你雇佣（hire）Agent 时锁定对应版本——你安装的带技能 Agent 从此真正具备它宣传的那些能力。

## 原始内容

feat(claw-interface): register pack skills into engine and pin on hire (#3071)

## 背景

Agent pack 自带 skills（`.agents/skills/*`）在 v2 迁移里被烤进 E2B environment（`/opt/zooclaw/environment/pack/`），但**从未注册进 zooclaw-engine registry**，所以引擎的 `renderSkills()` 从不把它们写进 agent 系统提示——模型看不到、永不触发。根因：走了 environment lane，而只有 skills-render lane 才喂 context。

本 PR 是 claw-interface 侧（跨仓 Part B），把 pack skills 改走规范 registry lane。**配套引擎 PR**：zooclaw-engine#435（开 pack 注册写入口 `PUT /admin/v1/skills/pack/{pack_id}/{name}/versions`）。

## 改动

- **翻译**（`engine_pack_translation.py`）：`repack_workspace_zip` 把 `.agents/skills/**` 整棵子树排除出 environment 归档；新增 `extract_pack_skills` 抽出每个 skill（文件 + SKILL.md frontmatter，`yaml.safe_load`）。
- **引擎客户端**（`engine_client`）：新增 `admin_upsert_pack_skill_version` → `PUT /admin/v1/skills/pack/{pack_id}/{name}/versions`（inline base64 files，复用 `/admin/v1` 同一 service token）；`create_agent`/`update_agent` 加可选 `skills` 参数。
- **approval 注册**（`pack_environment_service.run_post_approval`）：best-effort 注册每个 skill（单个失败告警跳过、不阻断 env build），把 `{skill_id, version}` 快照存进新的 submission-scoped repo（镜像 `pack_persona_docs`）。
- **装配**（`engine_agent_install_service`）：`_resolve_pack_skills` 读快照（缺失时 archive fallback 重新注册、幂等；与 persona 共用一次缓存的 translation），按与 `environment_id` 相同的可见性闸（`pack.org_id in (ZOOCLAW_ORG_ID, org_id)`）把 `skills=[{skill_id, version}]` pin 到 create + update 两条路径。

## 存储

新增 `ecap-pack-skill-versions` 集合 + `pack_skill_versions_repo`（`upsert`/`get_by_submission`，唯一键 `pack_id+submission_id`），与 `pack_persona_docs` 同构；import-linter 三处清单同步。

## 测试

`tests/unit/` 扩展 4 个模块共 11 个新用例：translation 排除/抽取、client admin 路由 + base64 body、approval 注册 + 快照、install 传 `skills=` + 快照缺失走 fallback。子代理本地跑 **135 passed** + ruff 全绿。

## 边界 / 后续

- pack skill 受众当前恒 global（引擎 schema CHECK 禁止 pack 行带 org/owner；org/private pack 分树待引擎放宽）。
- 文档（Cloudflare managed-agents-site）已随引擎 PR #435 更新。
