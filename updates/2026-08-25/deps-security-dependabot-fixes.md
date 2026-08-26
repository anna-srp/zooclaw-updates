---
title: "安全加固：一次性修掉 58 条依赖安全告警，后端 Web 框架同步升级"
type: "Bug Fix"
priority: "中"
date: "2026-08-25"
status: "待审核"
channels: ""
---

# 安全加固：一次性修掉 58 条依赖安全告警，后端 Web 框架同步升级

## 核心宣传点

对后端服务、桌面端和 iOS 端积压的 73 条依赖安全告警做了一轮集中清理，修复 58 条。其中后端把 Starlette 升到 1.x、FastAPI 升到 0.139，顺带完成了此前被搁置的启动/关闭生命周期改造；桌面端和几个 Node 服务的构建与网络相关依赖也全部刷新。对用户来说使用方式完全不变，但底层组件的已知漏洞面明显收窄了。少数受上游约束暂时无法升级的告警已单独立项跟踪。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `3e54a5678befc6be3a6bf80b89dad2121f3b38c9`
- PR: #3498
- 作者: Chris@ZooClaw
- 日期: 2026-08-25T04:33:36Z

### Commit Message

```
fix(deps): resolve dependabot alerts across services, desktop (55/73) (#3498)

## 内容

处理 services / desktop / ios 的 73 条 open Dependabot 告警：**修复 58 条，dismiss
2 条，litellm 13 条转 ECA-1397**（codex-coder 实现、Claude review）。

### claw-interface（Python）⚠️ 含框架迁移，重点 review
- `starlette` 0.52.1 → **1.3.1**（安全补丁在 1.x 线）、`fastapi` <0.137 →
**0.139.2**。
- 这解除了 requirements 里原有的注释 pin——注释本身写明"等迁移到 Starlette 1.x lifespan API
时一起解除"，本 PR 完成了该迁移：`app/lifetime.py` 从
`add_event_handler("startup"/"shutdown")` 改为 `@asynccontextmanager
lifespan`（`finally` 保证 shutdown），`create_app` 经构造参数传入；路由测试适配
`tests/unit/_route_helpers.py`。
- 验证：独立 uv 环境 150 包解析一致；`bash scripts/verify-py.sh` 全过；相关路由单测通过。CI 全量
pytest 是最终把关。

### Node 服务
- whatsapp-business-service：`vitest` 1.x → 3.2.7，刷新 vite / esbuild /
postcss / fast-uri / find-my-way（42 tests + typecheck + build 通过）
- r2-access-worker / oauth-worker：`vitest` 3.2.7、`wrangler` 4.125.0，刷新
undici / sharp / ws 等（39 + 17 tests 通过）；oauth-worker 补建独立
`pnpm-lock.yaml`
- desktop：`electron-builder` → 26.15.3（未跨 major），刷新 app-builder-lib /
builder-util-runtime / tar / undici / js-yaml / form-data 等（typecheck
通过）
- 各目录 `pnpm install --frozen-lockfile` 均通过

### iOS（后续 commit 补充）
- `jwt` → 2.10.3、`json` → 2.19.9、`faraday` → 1.10.6：三者均在 fastlane
既有约束范围内，直接更新 lockfile（specs + CHECKSUMS，sha256 取自 rubygems API），由
ios-quality CI 的 bundle install 验证。

### 后续 commit：FastAPI 0.137+ 路由测试补迁
- codex 首轮漏迁 3 个路由契约测试（`include_router` 变懒挂载后 `router.routes`
不再展开子路由），已迁到 `api_routes` helper；本地全量 unit 套件 9082 passed。

### 未在本 PR 解决
1. **litellm 13 条（含 3 critical）**：被 `favie-common v0.3.69` 的
OpenTelemetry 1.25.0 pin 阻塞（importlib-metadata 冲突），跟踪
issue：[ECA-1397](https://linear.app/srpone/issue/ECA-1397)。
2. **excon 1 条**：补丁 1.5.0 超出 fastlane `< 1.0.0` 约束，已 dismiss（tolerable
risk，dev-time 工具链）。
3. **desktop extract-zip 1 条**：上游无 patched version，已 dismiss。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NWHV9vozVf6qN6zB5cUUdv

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Description

```
## 内容

处理 services / desktop / ios 的 73 条 open Dependabot 告警：**修复 58 条，dismiss 2 条，litellm 13 条转 ECA-1397**（codex-coder 实现、Claude review）。

### claw-interface（Python）⚠️ 含框架迁移，重点 review
- `starlette` 0.52.1 → **1.3.1**（安全补丁在 1.x 线）、`fastapi` <0.137 → **0.139.2**。
- 这解除了 requirements 里原有的注释 pin——注释本身写明"等迁移到 Starlette 1.x lifespan API 时一起解除"，本 PR 完成了该迁移：`app/lifetime.py` 从 `add_event_handler("startup"/"shutdown")` 改为 `@asynccontextmanager lifespan`（`finally` 保证 shutdown），`create_app` 经构造参数传入；路由测试适配 `tests/unit/_route_helpers.py`。
- 验证：独立 uv 环境 150 包解析一致；`bash scripts/verify-py.sh` 全过；相关路由单测通过。CI 全量 pytest 是最终把关。

### Node 服务
- whatsapp-business-service：`vitest` 1.x → 3.2.7，刷新 vite / esbuild / postcss / fast-uri / find-my-way（42 tests + typecheck + build 通过）
- r2-access-worker / oauth-worker：`vitest` 3.2.7、`wrangler` 4.125.0，刷新 undici / sharp / ws 等（39 + 17 tests 通过）；oauth-worker 补建独立 `pnpm-lock.yaml`
- desktop：`electron-builder` → 26.15.3（未跨 major），刷新 app-builder-lib / builder-util-runtime / tar / undici / js-yaml / form-data 等（typecheck 通过）
- 各目录 `pnpm install --frozen-lockfile` 均通过

### iOS（后续 commit 补充）
- `jwt` → 2.10.3、`json` → 2.19.9、`faraday` → 1.10.6：三者均在 fastlane 既有约束范围内，直接更新 lockfile（specs + CHECKSUMS，sha256 取自 rubygems API），由 ios-quality CI 的 bundle install 验证。

### 后续 commit：FastAPI 0.137+ 路由测试补迁
- codex 首轮漏迁 3 个路由契约测试（`include_router` 变懒挂载后 `router.routes` 不再展开子路由），已迁到 `api_routes` helper；本地全量 unit 套件 9082 passed。

### 未在本 PR 解决
1. **litellm 13 条（含 3 critical）**：被 `favie-common v0.3.69` 的 OpenTelemetry 1.25.0 pin 阻塞（importlib-metadata 冲突），跟踪 issue：[ECA-1397](https://linear.app/srpone/issue/ECA-1397)。
2. **excon 1 条**：补丁 1.5.0 超出 fastlane `< 1.0.0` 约束，已 dismiss（tolerable risk，dev-time 工具链）。
3. **desktop extract-zip 1 条**：上游无 patched version，已 dismiss。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NWHV9vozVf6qN6zB5cUUdv

```
