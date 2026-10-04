---
title: "开发者平台 Project Key 现在可以上传和管理自己项目下的 Skill，不再只能绑定平台目录里的现成技能"
type: "新功能"
priority: "高"
date: "2026-10-03"
status: "待审核"
channels: ""
---

# 开发者平台 Project Key 现在可以上传和管理自己项目下的 Skill，不再只能绑定平台目录里的现成技能

## 核心宣传点

以前用开发者平台的 Project Key（zwp_live_ 这类）只能把平台 catalog 里已有的 Skill 绑到 Agent 上，自己写的 Skill 传不上去——所有 /service/v1/skills 请求都直接返回 404，因为网关只放行了 agents 和 models 两类路由。现在 skills 路由对 Platform Key 开放了：具名 Project 的 Key 可以上传 project scope 的 Skill zip，归属的组织和项目由网关强制写入，请求方自己伪造的归属字段会被覆盖；Default Project 的 Key 上传时走 org scope，整个组织共享。列表接口会自动按 Key 的归属过滤，读取时 global、本组织、同项目以及自己的 personal Skill 都能看到。删除和发布新版本只允许动自己写权限范围内的 Skill，碰到 global、别的项目或别人 personal 的 Skill 一律 404，不会转发到后端。personal scope 对 Platform Key 不开放，因为后端存 personal Skill 时不带组织信息，会让同一个人在其他组织的 Key 也看到它，破坏组织隔离。Work Key（zct_）的行为完全没变。配套的 SDK 类型（TypeScript / Python 的 uploadSkill 需要补 project scope）和文档更新会在这次部署上线验证后另外跟进。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `8bdec5478425db6fbac4aa004fed39a754bc8ce0`
- PR: #4013
- 作者：finn-srp
- 日期：2026-10-03T16:26:42Z

### Commit Message

```
feat(platform): let Project keys manage Skills in their own scope (#4013)

## Linear
无。问题记录见 #4010（Platform E2E 汇总）。

## Summary

Platform Project key 之前可以把平台 catalog 里的 Skill 绑定到 Agent，但不能上传自己的
Skill。原因是 `_platform_proxy` 只放行 `agents` 和 `models` 两类路由，所有
`/service/v1/skills` 请求都返回 404。Engine 本身已经支持 zip 上传和 `project`
scope，所以这次只改 claw-interface 网关，不涉及 Engine。

这个 PR 为 Platform key 接入 skills 路由，规则如下：

| 操作 | 规则 |
|---|---|
| 上传 Skill `POST /skills` | 具名 Project 的 key 只能上传 `project` scope，网关强制写入
key 的 `org_id` 和 `project_id`。Default Project 的 key 只能上传 `org`
scope（Engine 设计中，Default Project 通过 org scope 共享）。`personal` 和 `global`
返回 400 |
| 列表 `GET /skills` | 强制带上 key 的 `owner_uid`、`org_id`；只有具名 Project 才附加
`project_id`，因为 Engine 不接受 `project_id=default` |
| 读取 `GET /skills/{id}/…` | 沿用现有的 `_platform_skill_visible`：global、本组织
org、同 Project 的 project、owner 自己的 personal 都可读 |
| 删除、发布新版本 | 只允许 key 自己写权限范围内的 Skill。global、其他 Project 的、personal 的
Skill 在网关层直接返回 404，不会转发到 Engine |

不允许 Platform key 写 `personal` 的原因：Engine 存储 personal Skill 时不带
`org_id`，它会对同一个 owner 在其他组织里的 key 也可见，越过了 Platform key 的组织隔离。

Work（`zct_`）key 的行为不变。读取 zip 和转发给 Engine 这两步抽成了共用函数；multipart
上传的幂等键在路由设置了 Platform 幂等作用域时使用该作用域（`platform:{org}:{project}`）。

原来的测试 `test_platform_work_membership_routes_remain_unavailable` 断言
Platform key 访问 skills 返回 404，这次去掉了 skills 这一项，environments 仍然保持不可用。

### 合并后的配套工作（不在本 PR 内）

- SDK：TypeScript `uploadSkill` 的 `scope` 类型目前只有 `'org' |
'personal'`，需要补上 `'project'`；Python 同步。
- Docs 和 coding skill：把"Platform key 不能上传 Skill"改成上传指南。需要在本 PR
部署后完成线上验证再改。

## Test plan

- [x] 新增 `tests/unit/test_service_proxy_platform_skills.py`，覆盖：
  - 两种 key 的上传 scope，以及请求方伪造 anchor 时被覆盖
  - 被拒绝的 scope
  - 列表参数
  - 读取的可见性
  - 写操作的 404
  - Engine 5xx 时对外屏蔽细节
- [x]
定向测试：`test_service_proxy_{platform_skills,skills,platform,agents,core}.py`
共 89 项通过。
- [x] `bash scripts/verify-py.sh` 通过（ruff、ruff
format、pyright、import-linter）。
- [x] push 前在最终提交上运行 `ecap-verify-py-ci`：依赖解析、lint（含全部
`ci-lint`）、jscpd、pytest 全部通过，13,695 passed，覆盖率 89.98%（门槛 89.5%）。
- [ ] 部署后用 Platform key 在线上验证：上传 zip、列表、绑定到 Agent、Agent 实际读取
`/skills/<name>/SKILL.md`、发布新版本、删除。另外验证 global Skill 和其他 Project 的 Skill
写操作返回 404。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

来源：SerendipityOneInc/ecap-workspace @ 8bdec547，PR #4013，作者 finn-srp。
