# SerendipityOneInc/ecap-workspace — commits 2026-10-03

## feat(platform): let Project keys manage Skills in their own scope (#4013)

- **SHA**: `8bdec5478425db6fbac4aa004fed39a754bc8ce0`
- **作者**: finn-srp
- **日期**: 2026-10-03T16:26:42Z
- **PR**: #4013

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

### PR Body

```
## Linear
无。问题记录见 #4010（Platform E2E 汇总）。

## Summary

Platform Project key 之前可以把平台 catalog 里的 Skill 绑定到 Agent，但不能上传自己的 Skill。原因是 `_platform_proxy` 只放行 `agents` 和 `models` 两类路由，所有 `/service/v1/skills` 请求都返回 404。Engine 本身已经支持 zip 上传和 `project` scope，所以这次只改 claw-interface 网关，不涉及 Engine。

这个 PR 为 Platform key 接入 skills 路由，规则如下：

| 操作 | 规则 |
|---|---|
| 上传 Skill `POST /skills` | 具名 Project 的 key 只能上传 `project` scope，网关强制写入 key 的 `org_id` 和 `project_id`。Default Project 的 key 只能上传 `org` scope（Engine 设计中，Default Project 通过 org scope 共享）。`personal` 和 `global` 返回 400 |
| 列表 `GET /skills` | 强制带上 key 的 `owner_uid`、`org_id`；只有具名 Project 才附加 `project_id`，因为 Engine 不接受 `project_id=default` |
| 读取 `GET /skills/{id}/…` | 沿用现有的 `_platform_skill_visible`：global、本组织 org、同 Project 的 project、owner 自己的 personal 都可读 |
| 删除、发布新版本 | 只允许 key 自己写权限范围内的 Skill。global、其他 Project 的、personal 的 Skill 在网关层直接返回 404，不会转发到 Engine |

不允许 Platform key 写 `personal` 的原因：Engine 存储 personal Skill 时不带 `org_id`，它会对同一个 owner 在其他组织里的 key 也可见，越过了 Platform key 的组织隔离。

Work（`zct_`）key 的行为不变。读取 zip 和转发给 Engine 这两步抽成了共用函数；multipart 上传的幂等键在路由设置了 Platform 幂等作用域时使用该作用域（`platform:{org}:{project}`）。

原来的测试 `test_platform_work_membership_routes_remain_unavailable` 断言 Platform key 访问 skills 返回 404，这次去掉了 skills 这一项，environments 仍然保持不可用。

### 合并后的配套工作（不在本 PR 内）

- SDK：TypeScript `uploadSkill` 的 `scope` 类型目前只有 `'org' | 'personal'`，需要补上 `'project'`；Python 同步。
- Docs 和 coding skill：把"Platform key 不能上传 Skill"改成上传指南。需要在本 PR 部署后完成线上验证再改。

## Test plan

- [x] 新增 `tests/unit/test_service_proxy_platform_skills.py`，覆盖：
  - 两种 key 的上传 scope，以及请求方伪造 anchor 时被覆盖
  - 被拒绝的 scope
  - 列表参数
  - 读取的可见性
  - 写操作的 404
  - Engine 5xx 时对外屏蔽细节
- [x] 定向测试：`test_service_proxy_{platform_skills,skills,platform,agents,core}.py` 共 89 项通过。
- [x] `bash scripts/verify-py.sh` 通过（ruff、ruff format、pyright、import-linter）。
- [x] push 前在最终提交上运行 `ecap-verify-py-ci`：依赖解析、lint（含全部 `ci-lint`）、jscpd、pytest 全部通过，13,695 passed，覆盖率 89.98%（门槛 89.5%）。
- [ ] 部署后用 Platform key 在线上验证：上传 zip、列表、绑定到 Agent、Agent 实际读取 `/skills/<name>/SKILL.md`、发布新版本、删除。另外验证 global Skill 和其他 Project 的 Skill 写操作返回 404。

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## fix(platform): initialize Google auth before login clicks (#3974)

- **SHA**: `27fb5cb71056e6a23959055b64e2466157ece173`
- **作者**: finn-srp
- **日期**: 2026-10-03T08:26:40Z
- **PR**: #3974

### Commit Message

```
fix(platform): initialize Google auth before login clicks (#3974)

Platform initializes Firebase on the first Google click. On mobile
Safari, initialization can consume the click's transient user activation
before Firebase opens the popup, producing `auth/popup-blocked` on the
first attempt.

Prepare Firebase when the standalone Platform sign-in form mounts, then
enable Google only after `authStateReady()` resolves. Email remains
available during preparation. Preparation errors and a 10-second delay
show an email/reload fallback; a late successful preparation clears the
fallback and enables Google.

The click still invokes `signInWithPopup` directly, without waiting for
preparation inside the handler. Retain current HttpOnly Cookie sessions,
cross-tab recovery, focus/login guards, and protected-route
continuation. Update Preview auth and regression fixtures to the current
Cookie flow.

Scope: `web/platform`. The WebApp counterpart in `web/app` was merged
separately in #3983.

## Validation

- Node 24: `pnpm lint`, `pnpm typecheck`, `pnpm test` (194 tests in 22
suites), and `pnpm build` passed after integrating current main.
- Regression coverage verifies preparation before clicks, disabled
clicks while pending, Firebase token exchange into the Cookie session
flow, email fallback on failure/delay, and recovery after delayed
preparation.
- Existing persistent-session, focus/login, and route-continuation tests
pass.
- The new delay regression failed before the fallback was added, then
passed.
- Tests mock Firebase and Account responses. Real-device OAuth
authorization and the live callback/session exchange remain unverified.
```

### PR Body

```
Platform initializes Firebase on the first Google click. On mobile Safari, initialization can consume the click's transient user activation before Firebase opens the popup, producing `auth/popup-blocked` on the first attempt.

Prepare Firebase when the standalone Platform sign-in form mounts, then enable Google only after `authStateReady()` resolves. Email remains available during preparation. Preparation errors and a 10-second delay show an email/reload fallback; a late successful preparation clears the fallback and enables Google.

The click still invokes `signInWithPopup` directly, without waiting for preparation inside the handler. Retain current HttpOnly Cookie sessions, cross-tab recovery, focus/login guards, and protected-route continuation. Update Preview auth and regression fixtures to the current Cookie flow.

Scope: `web/platform`. The WebApp counterpart in `web/app` was merged separately in #3983.

## Validation

- Node 24: `pnpm lint`, `pnpm typecheck`, `pnpm test` (194 tests in 22 suites), and `pnpm build` passed after integrating current main.
- Regression coverage verifies preparation before clicks, disabled clicks while pending, Firebase token exchange into the Cookie session flow, email fallback on failure/delay, and recovery after delayed preparation.
- Existing persistent-session, focus/login, and route-continuation tests pass.
- The new delay regression failed before the fallback was added, then passed.
- Tests mock Firebase and Account responses. Real-device OAuth authorization and the live callback/session exchange remain unverified.
```

---

## fix(pricing): clarify API rates and sandbox billing (#4009)

- **SHA**: `f87a9ed684e64d74de9c88967dbd64205e7c3b68`
- **作者**: david-srp
- **日期**: 2026-10-03T07:58:06Z
- **PR**: #4009

### Commit Message

```
fix(pricing): clarify API rates and sandbox billing (#4009)

## Summary

API Pricing
原先把部分模型与工具价格写成模糊的用量结算说明，也没有明确区分当前免费能力和收费的数据源请求。现在中英文页面突出模型及第三方工具与原服务商同价、不额外加价，并在价格表中直接展示已确认的计费单位与条件。

-
入口：`/pricing?product=api`、`/zh/pricing?product=api`，覆盖模型表格、六个工具分类、沙箱价格卡片及展开明细。
- 语音、知识库和 ZooData
本身标为目前免费；小红书与其他已列明的社交数据请求分别展示单价及分页规则。补充图像、视频、搜索与正文提取的价格和计费条件，以及「更多 Agent
能力」中的穿搭工具按变体计价说明。
- 沙箱卡片突出按运行时长计费、空闲自动休眠、休眠期间不产生沙箱费用，以及模型和工具调用另行计费。
- 公开文案审查：未带入研发调研的原文件、内部路径、供应商路由、采购信息或凭据。价格说明采用研发提供的计费调研与产品确认，不改动后端扣费逻辑。

## Test plan

- [x] TypeScript、ESLint、仓库前端治理检查通过。
- [x] API catalog、marketing chrome、pricing typography 共 44 项相关测试通过。
- [x] 中英文桌面（1069×977）及手机（375×667）预览，检查模型搜索与展开、工具分类切换、免费与收费数据行、沙箱说明及横向溢出。
- [x] `git diff --check` 通过；本地截图及研发原始调研未纳入提交。
```

### PR Body

```
## Summary

API Pricing 原先把部分模型与工具价格写成模糊的用量结算说明，也没有明确区分当前免费能力和收费的数据源请求。现在中英文页面突出模型及第三方工具与原服务商同价、不额外加价，并在价格表中直接展示已确认的计费单位与条件。

- 入口：`/pricing?product=api`、`/zh/pricing?product=api`，覆盖模型表格、六个工具分类、沙箱价格卡片及展开明细。
- 语音、知识库和 ZooData 本身标为目前免费；小红书与其他已列明的社交数据请求分别展示单价及分页规则。补充图像、视频、搜索与正文提取的价格和计费条件，以及「更多 Agent 能力」中的穿搭工具按变体计价说明。
- 沙箱卡片突出按运行时长计费、空闲自动休眠、休眠期间不产生沙箱费用，以及模型和工具调用另行计费。
- 公开文案审查：未带入研发调研的原文件、内部路径、供应商路由、采购信息或凭据。价格说明采用研发提供的计费调研与产品确认，不改动后端扣费逻辑。

## Test plan

- [x] TypeScript、ESLint、仓库前端治理检查通过。
- [x] API catalog、marketing chrome、pricing typography 共 44 项相关测试通过。
- [x] 中英文桌面（1069×977）及手机（375×667）预览，检查模型搜索与展开、工具分类切换、免费与收费数据行、沙箱说明及横向溢出。
- [x] `git diff --check` 通过；本地截图及研发原始调研未纳入提交。
```
