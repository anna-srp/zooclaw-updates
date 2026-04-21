# ecap-workspace — 2026-04-17
共 93 条 commits

## `125444c6` refactor(claw-interface): 拆分 openclaw_settings — Feishu / multi-agent / image-version (1/10) (#969)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:45:28Z
- **链接**: [125444c6](https://github.com/SerendipityOneInc/ecap-workspace/commit/125444c6acef198d5496d1426caec92944e365a4)

**PR #969 Description:**
## Summary

拆分 5 个 Python 超长文件系列(spec PR #965 已合并)的 **PR 1/10**:把 `openclaw_settings.py`(1618 行)的 3 个业务簇抽到独立 sibling 文件,该文件缩到 1043 行(仍 grandfathered WARNING,PR 2 才达 ≤500)。

新增 sibling(严格无 shim,各自 import 上游依赖):
- `openclaw_settings_feishu_session.py`(74):`_FeishuSetupSession` / `_feishu_sessions` / `_cleanup_user_sessions` / `_get_valid_session` / `_feishu_registration` / `_FEISHU_BASE_URLS`
- `openclaw_settings_feishu.py`(211):3 endpoints — setup / poll / setup_cancel
- `openclaw_settings_multi_agent.py`(278):4 endpoints + helpers — get/update_agent_{settings,identity,model,bindings}
- `openclaw_settings_image_version.py`(96):2 endpoints —  @srp.one 专用 list_releases / set_image_version

测试改动(strict no-shim,patch path 全更新):
- `test_openclaw_settings_image_version.py` 全文 patch path 替换
- `test_openclaw_settings_routes.py` Feishu helper/endpoint imports + patches → `_feishu_session`/`_feishu` 模块,`httpx` patch 目标改 `_feishu_session`
- multi-agent helper imports → `_multi_agent`

`create_app.py` 注册新 3 个 router(shared helper 模块无 router)。

**Pairing 端点保留在 core**:`get_channel_pairing`/`approve_channel_pairing` 是 generic(不仅 Feishu),留 `openclaw_settings.py`。spec 原估 Feishu 含 5 endpoint,实际 3。

## Diff size

- 778 insertions / 666 deletions = 1444 行
- 软上限 1000 / 硬上限 2000 hard。节点性 PR 接近上限属可接受范围(spec 已说明)

## Test plan
- [x] `pyright app/ tests/` 0 errors
- [x] `pytest tests/unit/ -x` 全绿(2437 passed)
- [x] `bash scripts/ci-lint/01-file-length.sh` 无新 ERROR(`openclaw_settings.py` 1618→1043,grandfathered WARNING)
- [x] `bash scripts/ci-lint/03-complexity.sh` 无新违规
- [x] pre-commit 全部 hook 通过(ruff/format/import-linter/pyright)
- [ ] CI 端到端跑过

## Spec reference

`docs/superpowers/specs/2026-04-16-reduce-file-length-python.md`(PR #965 合并)。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `88b24c35` test(web): useSubagentChat hook 覆盖 (#894 final chat hook) (#970)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:44:04Z
- **链接**: [88b24c35](https://github.com/SerendipityOneInc/ecap-workspace/commit/88b24c35bf29b54d9956fd17651adfa6dcd18cb7)

**PR #970 Description:**
Part of #894 — **last chat/hooks file to cover**.

## 新增

\`tests/unit/app/chat/useSubagentChat.unit.spec.ts\` — 27 tests 跨 4 个 describe 块。

## 覆盖要点

### History loading (9 tests)
- 未连接 / 空 sessionKey → skip
- \`chat.history\` API with \`limit:50\`
- 过滤非 user/assistant role
- 过滤空 content 消息
- extractMessageText fallback（无 text 字段的 content 结构）
- 缺 id 自动 crypto.randomUUID()
- Fetch failure → \`historyLoadedRef\` 重置，下次 rerender 允许重试
- sessionKey 切换 → 同步清空 messages + isGenerating=false

### Chat event stream (7 tests)
- 其他 sessionKey → 忽略
- delta event：新 runId 追加 assistant 消息；同 runId 替换（cumulative 流式）
- 空 delta content → 忽略（噪声保护）
- final event：payload.content 存在优先；无则回落 \`streamingContentRef.current\`
- error event → \"Error: <errorMessage>\" / \"Unknown error\" fallback
- error event → setIsGenerating(false)

### Agent lifecycle events (4 tests)
- \`stream:lifecycle\` + phase=end → isGenerating false
- phase=error → isGenerating false
- 其他 sessionKey → 忽略
- 非 lifecycle stream（如 tool）→ 忽略

### sendMessage / abortGeneration (5 tests)
- 空 text (trimmed) / disconnected → skip
- 正常路径：追加 user msg + setIsGenerating(true) + chat.send
- chat.send 失败 → 回退 isGenerating false
- abortGeneration 无 active runId → skip；有 → chat.abort with runId

## 完成 #894 chat/hooks 全部覆盖

至此 \`src/app/[locale]/chat/hooks/\` 全部覆盖完成（按 merge 顺序）：
- useOpenClawRuntime ✅
- useArtifactsSidebar ✅
- useMattermostIntegration ✅
- useProfileGreeting ✅
- useSubagentSessions ✅
- **useSubagentChat** ✅ （本 PR）
- (useOpenClawChat / useOpenClawInit / useOpenClawWebSocket 仍留 E2E — 涉及 WS 长连接)

## 关键模式 memo 候选

- **Fail-then-resolve 模式**：\`mockRejectedValueOnce(err).mockResolvedValue(ok)\`
  测重试场景，避免 "one-shot mock after consumption returns undefined" 坑
- **mkWs factory + emit closure**：所有 WS-based hook test 通用模板

Refs: #894

## `72827d98` test(web): useSubagentSessions hook 覆盖 (#894 additional) (#968)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:43:33Z
- **链接**: [72827d98](https://github.com/SerendipityOneInc/ecap-workspace/commit/72827d98868ad90c2125d52022eb3ab6eb172147)

**PR #968 Description:**
Part of #894.

## 新增

\`tests/unit/app/chat/useSubagentSessions.unit.spec.ts\` — 17 tests 覆盖 160 LoC hook 的 3 个域：

### fetchSessions (9 tests)
- 未连接 → 跳过 sendRequest
- 连接时调 \`sessions.list\` with \`limit:50, includeLastMessage:true\`
- 客户端 \`:subagent:\` key pattern 过滤
- \`inferStatus\`：<15s=running / >15s=done / missing=idle
- \`extractLastMessageText\` 4 分支：string / .text / .content / undefined
- Fetch error silent（best-effort，不破坏 UI）
- 空 body 保持空 state

### polling (1 test)
- \`isGenerating=true\` + connected → 每 3s poll via setInterval
- \`isGenerating=false\` → clearInterval；else 分支触发一次 final fetch

### event-driven child session detection (7 tests)
- Lifecycle event with \`childSessionKey\` → 入列
- Tool \`partialResult\` JSON with \`:subagent:\` → 入列
- Tool \`partialResult\` 无 \`:subagent:\` → 忽略
- 非 JSON partialResult → try/catch silent
- User text 匹配 regex \`/session_key:\\s*(agent:\\S*:subagent:[0-9a-f-]+)/\` → 入列
- 重复 childSessionKey → 不重复加入
- 其他 stream/event → 完全忽略

## 技术点

- 多 describe 按 timer 模式分离：real timers for waitFor, fakeTimers for polling
- \`flushMicrotasks()\` helper：non-fake-timer 环境下等 promise chain
- \`mkWs()\` factory + \`emit()\` 闭包：单测主动触发 WS event，模拟 server push

## Bug-hunting

未发现生产 bug。验证了 regex 的严格性：session_key 尾部必须是 hex + dash
（\`[0-9a-f-]+\`），非 hex（如 "announced-abc" 含 'n'）不匹配 → hook 不误识别
无关消息。这是一个隐式的 sanitization 保护。

Refs: #894

## `565ac323` test(web): useProfileGreeting hook 覆盖 (#894 additional) (#966)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:39:43Z
- **链接**: [565ac323](https://github.com/SerendipityOneInc/ecap-workspace/commit/565ac323562f94eb57936525d385c7cccb5439f1)

**PR #966 Description:**
Part of #894 — small chat hook coverage pass.

## 新增

\`tests/unit/app/chat/useProfileGreeting.unit.spec.ts\` — 8 tests 覆盖 76 LoC hook。

## 覆盖要点

### sessionStorage marking (5 tests)
- Mount effect 首次 mark sessionKey 为 greeted
- 已存在 greeted flag → 不重复 setItem（profileSentRef 保持 null）
- sessionKey='' 空串 → no-op
- sessionKey 改变（session 切换）→ 新 session mark + ref 更新

### Reset guards (3 tests)
Source 注释说明 auto-greeting 已 disabled（BOOTSTRAP.md 替代），awaitingGreeting
目前只有外部能设 true。hook 保留的 3 个 reset effects 作为 safety net：
- displayMessages 变化 → 不虚假翻转 false
- wsStatus → 'error' / 'disconnected' → 不虚假翻转
- unmount 后 advance 12s safety timer → 无 setState 泄漏

## Bug-hunting

无生产 bug。验证了 effect 在 awaitingGreeting=false 状态下的稳定性（避免
因 dependency 变化导致意外 setState）。

Refs: #894

## `ec079fbf` test(web): useUserAgents hook + refreshUserAgentsCache 覆盖 (#894 additional) (#962)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:37:55Z
- **链接**: [ec079fbf](https://github.com/SerendipityOneInc/ecap-workspace/commit/ec079fbfe50649a8774ce1f3996efd819905c810)

**PR #962 Description:**
Part of #894 — continued hook coverage. useUserAgents was 16% covered; this PR brings it near 100%.

## 新增

\`tests/unit/hooks/useUserAgents.unit.spec.ts\` — 15 tests split across
module-level helper + hook behavior.

## 覆盖要点

### \`refreshUserAgentsCache\` 模块级缓存 (6 tests)
- Happy path: fetch → warm catalog → localStorage write → \`ecap:agents:updated\` dispatch
- **Dedup**: concurrent \`refreshUserAgentsCache()\` 调用共享同一 in-flight promise（仅 1 次 \`getOpenClawAgents\` 调用）
- **Pending-sync lifecycle**:
  - Lock 获得 + updateAgents 成功 → \`clearAgentsSyncPending\`
  - Lock 获得 + updateAgents throw → \`releasePendingSyncLock\` + 保留 pending marker
  - Lock 未获得（另一 tab 赢 race）→ 跳过 sync，直接 fetch
- Catalog refresh 错误 silent → 不影响主 fetch

### \`useUserAgents\` hook (9 tests)
- 初始 placeholder "Claw" main agent
- localStorage cache → 加载覆盖 placeholder
- JSON parse 错误静默吞下
- 未登录 → 不 fetch
- 登录 + cache 命中 → \`showLoading: false\` refresh（防闪烁）
- \`refreshAgents()\` 未登录返回空数组
- \`ecap:agents:updated\` 事件 → 重读 localStorage
- \`storage\` 事件 → **仅** \`AGENTS_CACHE\` key 响应
- 所有 agent 缺 workspace → 自动 retry 一次

### 技术点

\`\`\`ts
beforeEach(() => {
  vi.resetModules()  // 关键：重置 module-level _inflight/_lastResult/_lastFetchTime
  localStorage.clear()
  // ...
})
\`\`\`

Module-level throttle cache 是全局单例，不 reset 会跨测试污染（e.g. dedup
test 的 in-flight promise 会让下一个 test 看到缓存结果）。

## Bug-hunting 过程

未发现生产 bug。验证了 dedup、pending-sync race 保护、missing-workspace
auto-retry 等并发设计的 correctness。

Refs: #894

## `a721d6f1` test(web): useIntegrations hook 覆盖 (#894 additional) (#959)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:35:44Z
- **链接**: [a721d6f1](https://github.com/SerendipityOneInc/ecap-workspace/commit/a721d6f1c7bf38b6466901f57ecf91258c420302)

**PR #959 Description:**
Part of #894 — continued hook coverage.

## 新增

\`tests/unit/hooks/useIntegrations.unit.spec.ts\` — 17 tests 覆盖 useIntegrations 全部 public API + 轮询。

## 覆盖要点

### loadConnections (5 tests)
- 无 uid → 不调 API / 空 state
- 正常 fetch → setConnections
- API reject (Error) → error 消息透传
- API reject (非 Error) → "Failed to load integrations" fallback
- refresh() 手动再 fetch

### connect (3 tests)
- 无 uid → 返回 null，不调 API
- 成功 → 返回 auth_url + refresh 连接列表
- 失败 → 返回 null + setError + 清除 saving

### disconnect / enable / disable (5 tests)
- disconnect 成功 → true + refresh
- disconnect 失败 → false + error
- 无 uid → false
- **enable/disable 乐观 state 更新**（不触发额外 getConnections）—— 这是生产设计，UI 立即反馈
- 失败 → false + error + saving 清空

### pollUntilConnected (3 tests)
使用 \`vi.useFakeTimers\` + \`advanceTimersByTimeAsync\`：
- 每 2s 轮询 → status=connected 后 clearInterval（后续 8s 无新 API 调用验证停止）
- 15 次 max cap（30s 内达上限，再推进 30s 确认不再 poll）
- 轮询错误 silent → \`result.current.error\` 保持 null，不暴露给 UI

## Bug-hunting 过程

未发现生产 bug。验证了乐观 state 更新（enable/disable 不 reload 的性能优化）
和 polling 的 silent-error 设计（避免临时网络错误污染用户 UI）。

## 验证

\`\`\`bash
cd web
npx vitest run tests/unit/hooks/useIntegrations.unit.spec.ts
# 17 tests pass
\`\`\`

Refs: #894

## `ccb2452c` refactor(orders): 下沉 resolve+validate 到 OrderCreateRequest (Pydantic model_validator) (#957)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:35:26Z
- **链接**: [ccb2452c](https://github.com/SerendipityOneInc/ecap-workspace/commit/ccb2452c694ed0318a8699903e819eba4dcc4a08)

**PR #957 Description:**
## Summary

- 把 `create_order` 里的 v1/v2 输入归一 + 字段白名单校验从 route 层下沉到 `app/schema/order.py::OrderCreateRequest.@model_validator(mode='after')`
- 消除 PR #953 保留的 `request.stripe_product_id` mutation 副作用(那是"validate"函数里偷偷做 resolve 的历史包袱)
- schema 改用 `DomainValidationError(ServiceError 子类)`,经已注册的 `service_error_handler` 映射为 `400 + {"code": ..., "detail": str}`,前端 `postAPI` 的 `data.detail` 提取路径完全保留

## 为什么这样改

PR 2 合并后,`_validate_and_resolve_subscription_product` / `_validate_topup_product` 仍然带着 "validate 函数悄悄 mutate request" 的副作用 —— 根本原因是 resolve(输入归一)和 validate(必填/白名单)是两件事被塞进一个 route 层函数。Pydantic `@model_validator` 是 resolve 的合法归属。

**关键兼容性(已验证)**:
- `web/src/lib/api/backend.ts:74-80` `postAPI` 对非 2xx 统一处理 `data.error || data.detail || data.message`
- 3 个 caller (`PaywallContent.tsx`、`SubscriptionPanel.tsx` x2) 只判 `success` 布尔,**无 status code hardcode**
- FastAPI 默认 422 body 的 `detail` 是 `list[dict]`,会让 toast 显示成 `"[object Object]"`
- **`DomainValidationError` 路径保持 400 + 字符串 detail**,前端零改动

**关键 Pydantic v2 行为钉住**:
- `@model_validator(mode='after')` 只包 `ValueError / AssertionError / PydanticCustomError`,其它异常原样传播
- `DomainValidationError`(继承 `ServiceError` 非 ValueError)穿透 pydantic → FastAPI exception 层 → `service_error_handler` → 400
- `tests/unit/test_order_schema.py::TestSchemaValidatorIntegration` 3 个 TestClient 集成测钉住这条路径

## 变更

- **`app/schema/order.py`**: 新增 `@model_validator` + 8 个私有 helper + 3 个 whitelist 构造器(call-time 读 SETTINGS,可 patch)
- **`app/routes/orders.py`**: 删除 PR #953 的 3 个 `_validate_*_product` helper 和 3 个 `VALID_*` 常量;主干仅剩 orchestration + `_compute_trial_eligibility`(trial 判断是业务逻辑,留 route 层)
- **`03-complexity.sh`**: `create_order` 已在 PR #953 移除,本 PR 无进一步改动
- **`tests/unit/test_order_schema.py` (新)**: 13 个 schema 单测(覆盖 11 个 `DomainValidationError.code` 分支)+ 3 个 FastAPI TestClient 集成测
- **`tests/unit/test_orders_endpoints.py`**: 删除 4 个被 schema 吃掉的校验测;happy-path 改 patch `app.schema.order.SETTINGS`
- **`tests/unit/test_orders_trial_logic.py`**: OrderCreateRequest 构造移入 SETTINGS patch 上下文

## C2b 契约

`app.schema` 新增 `from app.errors import DomainValidationError`。C2b 禁止 schema 导 routes/services/database,**不禁** errors。`app.errors.__init__` 只依赖 `typing`,零转生 fastapi,不破坏 schema 叶子性。

## Test plan

- [x] `ruff check app/ tests/` + `ruff format --check`
- [x] `pyright app/ tests/` (0 errors)
- [x] `bash scripts/ci-lint/{01..06}*.sh` 全绿
- [x] `pytest tests/unit/` (2447 passed)
- [x] TestClient 集成测验证 400 + `detail` 是字符串(不是 list[dict])
- [x] Pydantic v2.12.5 非 ValueError 传播行为实测

## 后续(不在本 PR 范围)

- 前端 `postAPI` 对 `data.detail` 做类型判断(`isinstance list 取 [0].msg`),防御任何端点的默认 422 body。独立 issue。

## `23fcc0c6` test(web): useClawSettings hook 覆盖 (#894 largest remaining hook, 372 LoC) (#964)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:38:55Z
- **链接**: [23fcc0c6](https://github.com/SerendipityOneInc/ecap-workspace/commit/23fcc0c622e79dc45cde13a7300d7eac0ee4029a)

**PR #964 Description:**
Part of #894 — 覆盖所有剩余未测 hook 的最大一个。

## 新增

\`tests/unit/hooks/useClawSettings.unit.spec.ts\` — 26 tests 覆盖 useClawSettings 主要行为。

## 覆盖要点

### loadSettings + 自动 locale 同步 (7 tests)
- uid=undefined → no-op
- 并行 Promise.all([getClawSettings, getClawLocale])
- Locale fetch 失败 → 继续主加载 + Sentry \`captureMessage('Failed to fetch claw locale')\`
- Settings fetch 失败 → setError
- **Auto-sync 逻辑**：浏览器 locale !== 后端 locale 时触发 \`updateClawLocale\`
  - timezone 差异 → patch.timezone
  - language 差异 → patch.language
  - 两者都不差 → 不触发同步
  - updateClawLocale 失败 → Sentry warning（不阻塞）
  - \`localeSyncedRef\` 确保只跑一次（test 通过 initial effect fire 验证）

### save* operations (5 tests)
- saveModel / saveTimezone / saveSession → state.field merge
- saveIdentity partial 字段保留 + \`setCachedGlobalIdentity({emit:true})\`
- API 失败 → withSave 返回 false + error + savingKey 清空

### channels (7 tests)
- addChannel → \`{ok, message?}\` return shape + lastAddedPlatform tracking
- editChannel → \`{ok, error?}\`
- removeChannel → boolean + error state
- clearLastAddedPlatform reset
- approvePairing + uploadFile delegate

### fetch* (6 tests)
- fetchLogs / fetchResources / fetchUsage：
  - 成功 → set state
  - 失败：logs 用 "Error: X" 前缀；resources/usage 清 state + set \`*Error\`

## 未覆盖（留 E2E / 后续）

- \`pollUntilReady\` / \`waitForRolloutAndRefresh\`：涉及长轮询 5min timeout，
  单测环境难稳定模拟（setInterval + Date.now + Sentry logging 组合）

## Bug-hunting 过程

未发现生产 bug。验证了 locale 自动同步的幂等设计（\`localeSyncedRef\` 防止重复
写入 → 避免 gateway 重启风暴）。

Refs: #894

## `d0d78bc0` refactor(ci): merge_group 下启用 paths-filter,按 diff 跳过无关 pipeline (#967)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:32:27Z
- **链接**: [d0d78bc0](https://github.com/SerendipityOneInc/ecap-workspace/commit/d0d78bc026de0ffd94fba939845c10efe82b5160)

**PR #967 Description:**
## 问题

Merge queue 开启后,每个进入 queue 的 PR 都会**全量**触发 web-quality / ios-quality / python-duplication-check / claw-interface-quality 四条 pipeline,不论 PR 实际改了哪里。

纯 web 改动的 PR 也会在 queue 里拉 macos-15 runner 跑完整 Xcode build + SPM resolve,单次浪费几分钟 minutes 额度,总体拖慢 queue drain 速度。

## 根因

`dorny/paths-filter@v3` 在 `merge_group` 事件下**没有 default base ref**,action 会 error。之前的 workaround 是:

1. `changes` job 的 paths-filter step 加 `if: github.event_name != 'merge_group'` → merge_group 下跳过整个 filter,outputs.web/ios/python 全为空
2. 下游 4 个 pipeline 的 `if:` 加 `|| github.event_name == 'merge_group'` 兜底,让它们在 queue 下无条件跑
3. 汇总 job 手工把 `python_changed` 改成 `true`,让 python gate 仍然生效

这套兜底的代价就是"queue 里全跑"。

## 修复

`merge_group` 事件的 payload 带 `merge_group.base_sha`(queue 入口时 main tip)和 `head_sha`(假想合并后 tip),两者之差正是这一轮 queue group 引入的增量。直接传给 paths-filter:

```yaml
- name: Resolve diff base for paths-filter
  id: diff_base
  env:
    MERGE_GROUP_BASE: ${{ github.event.merge_group.base_sha }}
    MERGE_GROUP_HEAD: ${{ github.event.merge_group.head_sha }}
  run: |
    echo "base=${MERGE_GROUP_BASE:-}" >> "$GITHUB_OUTPUT"
    echo "ref=${MERGE_GROUP_HEAD:-}" >> "$GITHUB_OUTPUT"

- uses: dorny/paths-filter@v3
  id: filter
  with:
    base: ${{ steps.diff_base.outputs.base }}  # 空 → action fallback 到 PR/push 默认
    ref:  ${{ steps.diff_base.outputs.ref }}
    filters: ...
```

然后把所有兜底都删掉:

- 4 个 pipeline job 的 `|| github.event_name == 'merge_group'` 移除
- 汇总 job 的 `python_changed=true` 覆盖移除

## 为什么安全

- `code-quality` 汇总 job 用 `if: always()` + `needs.*.result` 聚合,skip 视为 non-failure。iOS/web/python pipeline 在 queue 下 skip 不会卡 queue
- Ruleset 的 `required_status_checks` 只有 `code-quality`、`size / size-check`、`auto-review / auto-review` 三项,其他 pipeline 不在 required 列表,skip 它们不影响 queue merge
- `merge_group` 下 group size ≥ 2 时,paths-filter 的 diff 横跨整组 PR(base 是入口时的 main tip,head 是整组合并后),语义依然正确

## Test plan

- [ ] 本 PR 本身只改 `.github/workflows/code-quality.yml`,paths-filter 不会匹配 web/ios/python 任何一条 → queue 里 4 个 pipeline 全 skip → code-quality 汇总 job 走 `if: always()` 分支 → 仍然报告 success
- [ ] 合并后下个纯 web PR(例如 #959)进 queue,观察 ios-quality / python-duplication-check 都 skip,queue drain 明显加速

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `e4cd3910` docs(claw-interface): Python 超长文件拆分方案 spec (0/10) (#965)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T16:06:03Z
- **链接**: [e4cd3910](https://github.com/SerendipityOneInc/ecap-workspace/commit/e4cd391045f633915afc8323b92724cbcc04d01e)

**PR #965 Description:**
## Summary

5 个 routes/services 文件超 `scripts/ci-lint/01-file-length.sh` 500 行阈值,合计 6803 行。本 PR 是 11 PR 拆分系列的 **第 0 步**:落地一份完整 spec doc,后续 10 个 PR 按此 spec 串行推进。

- 待拆 5 个文件:`openclaw_settings.py` (1618) / `openclaw_client.py` (1332) / `openclaw_agents.py` (1314,在 ALLOWLIST) / `agent_deploy.py` (919) / `openclaw_integrations.py` (624)
- 决策:**严格无 shim**(改全部 caller 与 test patch path)、Feishu 一次性拆透、PR 大小 500-1100 行 diff
- 节点性 PR:#2(settings 最后一刀)、#5(agents 最后一刀 + **删 ALLOWLIST**)、#8(client 最后一刀)、#9(deploy 达标)
- 完成后 `scripts/ci-lint/01-file-length.sh` 应 0 ERROR、0 WARNING、ALLOWLIST 项消失

详细蓝图见 `docs/superpowers/specs/2026-04-16-reduce-file-length-python.md`。

## Test plan
- [ ] 本 PR 仅文档,无代码改动 — 期望:CI 不跑 python-code-quality / web,只过 PR size check
- [ ] spec doc 内容 review:拆分蓝图、PR 序列、风险节、验证 checklist 是否完整

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `93930886` test(web): address PR #949 + #955 review follow-ups (#958)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T15:45:48Z
- **链接**: [93930886](https://github.com/SerendipityOneInc/ecap-workspace/commit/93930886ba05ecb10482b14efd683d2c9ebce6f2)

**PR #958 Description:**
Combined follow-up to #949 and #955 — both already merged.

## From #955 Claude review

\`useAgentActions.unit.spec.ts\`: \`(thrown as unknown as Error)?.message\`
is a redundant double cast. Simplify by declaring \`thrown: unknown\` and
narrowing at the assertion site via \`(thrown as Error | null)?.message\` —
equivalent semantics, silences TS narrow-to-never warnings.

## From #949 Claude review

Two non-blocking suggestions:

1. **useRequireChat**: missing \`beforeEach(vi.clearAllMocks())\` — the other
   three sibling specs have it. Currently harmless (test 1 doesn't call
   \`mockRouterReplace\`) but creates false-positive risk if test order
   changes. Added.
2. **useVersionCheck invalidate test**: post-\`rerender\` synchronous assertion
   works because React wraps rerender in \`act()\` and the effect is synchronous.
   Wrapping in \`await waitFor(...)\` makes the "effect-fired" intent
   self-documenting. Changed.

## Verification

\`\`\`bash
cd web
npx vitest run tests/unit/hooks/useRequireChat.unit.spec.ts \\
  tests/unit/hooks/useVersionCheck.unit.spec.tsx \\
  tests/unit/hooks/useAgentActions.unit.spec.ts
# 18 tests pass
\`\`\`

Refs: #894 #949 #955

## `2c3edac8` fix(ci): claude-review 在 merge_group 下 emit status 解锁 queue (#963)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T15:45:13Z
- **链接**: [2c3edac8](https://github.com/SerendipityOneInc/ecap-workspace/commit/2c3edac893c87b4eba86037b0fb34ca090ed541c)

**PR #963 Description:**
## 问题

Merge queue 开启后,4 个 PR 全部卡在 `AWAITING_CHECKS` 永远不 merge。根因:

- Ruleset `RequireAutoReview` 把 `auto-review / auto-review` 列为 `required_status_checks`
- GitHub ruleset 的 required check **不区分 PR 阶段和 merge_group 阶段**,两者共用同一张列表
- `claude-review.yaml` 里的 `auto-review` job 有 `if: github.event_name == 'pull_request'`,merge_group 事件下整个 job skip,check run **根本不产生**
- Queue 在 merge_group branch 上死等一个永远不会报告的 check

## 修复方向(方案 C2)

加一个**仅在 merge_group 事件下**触发的 job,用 `GITHUB_TOKEN`(integration 15368 = GitHub Actions)调 Statuses API,POST 一个同名 `auto-review / auto-review` 的 success commit status。

- PR 阶段 AI review 门禁**不变**,照常跑
- Queue 阶段不再等真正的 review(没有 PR diff 可看,跑了也没意义),而是收到一个 success status 占位,queue 通过继续走到真正有意义的 `code-quality` / `size-check` 验证
- integration_id 15368 由 `GITHUB_TOKEN` 身份自动满足

## 为什么不改 ruleset

GitHub 的 ruleset 不支持"只在 PR 阶段 required、queue 阶段不 required"这种配置。想保留 PR 阶段 auto-review 的强制性,就必须在 workflow 层解决。

## Test plan

- [ ] 本 PR 本身因 required check 问题仍会卡 queue → **admin bypass 合并**
- [ ] 合并后开下一个 PR,观察 merge_group 事件是否自动 emit 占位 status
- [ ] 确认 queue 正常 drain,之后不再需要人工 POST status

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `be82a7b7` fix(ci): pr-size-check 跳过无关 label 事件 (#961)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T15:42:41Z
- **链接**: [be82a7b7](https://github.com/SerendipityOneInc/ecap-workspace/commit/be82a7b7c3434b3b91ff4e9a762c5d2122c81f07)

**PR #961 Description:**
## 问题

`pr-size-check.yml` 的 \`on:\` 包含 \`labeled\` / \`unlabeled\` types，原设计目的是让贴 \`size-override\` 标签能立刻重算 size check 并刷新 sticky comment。

副作用：**任何 label 操作都会重跑 workflow**，包括：
- \`/lgtm\` 触发的 \`self-approve\` 标签
- Claude auto-review 贴的 \`needs-human-review\` 等标签
- 手动贴任何 tracking 标签

每次白跑 ~10 秒 + 更新同样内容的 sticky comment，污染 Actions UI。

## 修复

job 级 \`if:\` 过滤：

\`\`\`yaml
if: >
  github.event_name != 'pull_request' ||
  (github.event.action != 'labeled' && github.event.action != 'unlabeled') ||
  github.event.label.name == 'size-override'
\`\`\`

## 行为对照

| 事件 | 修复前 | 修复后 |
|---|---|---|
| \`push\` 新 commit (synchronize) | ✅ 跑 | ✅ 跑 |
| 贴 \`size-override\` | ✅ 跑（立刻重算） | ✅ 跑（保留 UX） |
| 贴 \`self-approve\` | ❌ 白跑 | ✅ skip |
| 贴任何其他标签 | ❌ 白跑 | ✅ skip |
| \`merge_group\` 事件 | ✅ 跑 | ✅ 跑 |

## 为什么在 job 级而不是 workflow 级过滤

GitHub Actions 的 \`on:\` trigger 只能按 event type / types / paths / branches 过滤，**不支持按 label name 过滤**。必须用 \`if:\` 在 job 级拦下。

代价：workflow 仍会为每次 label 事件启动，但 job 瞬间 skip（~2s 开销 vs 完整跑 10s）。GitHub 不对 skip 收费。

## Test plan

- [ ] 本 PR 合后：下一个 PR 的 \`/lgtm\` 触发 \`self-approve\` 标签时，观察 Actions UI — pr-size-check 应该显示 skipped，不跑完整逻辑
- [ ] 贴 \`size-override\` 标签 — 应该立刻重算（保持现有 UX）
- [ ] 新 push commit — 正常跑

## 相关

在 PR #956 (/lgtm 自审批) 合入后观察到的噪音，属于 merge queue rollout 的尾声清理。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `12d177d1` feat(ci): /lgtm 评论触发 author self-approve (AI-first workflow) (#956)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T15:02:01Z
- **链接**: [12d177d1](https://github.com/SerendipityOneInc/ecap-workspace/commit/12d177d1b15dfcc4b90f1dcc1bc4f630a471579b)

**PR #956 Description:**
## 背景

当代码由 AI 生成、作者以 human 身份提交时，作者的主要角色是 **reviewer 而不是 writer**。GitHub 的 "author 不能 self-approve" 规则假设作者就是代码编写者，在 AI-first workflow 下这个假设不再成立。

## 方案

作者在自己 PR 下评论 `/lgtm` → `srp-claude-assistant` bot 代发 formal `APPROVE` review → 同时贴 `self-approve` 标签供审计。

**边界**：
- ❌ 不 auto-merge，作者仍需手动点 **Merge when ready**
- ✅ Required CI checks（code-quality 等）继续阻塞 merge
- ✅ 复用现有 `srp-claude-assistant` GitHub App，不新建

## 五层防护

| 位置 | 检查 | 防的是什么 |
|---|---|---|
| `if:` | `github.event.issue.pull_request` 不为空 | 普通 issue 评论不触发 |
| `if:` | `comment.user.login == issue.user.login` | 同事代贴 `/lgtm` 无效 |
| `if:` | `!endsWith(user.login, '[bot]')` | Bot PR 走其他路径 |
| `if:` | `body == '/lgtm' \|\| startsWith(body, '/lgtm ')` | `/lgtmify` 等不误触发 |
| **step** | **permissions API 查询作者权限 ∈ {maintain, admin}** | **Write 级（junior dev / PM）不能自审批** |

**最后一条为什么单独放 step 里**：`author_association` 字段不区分 Write vs Maintain vs Admin（都是 COLLABORATOR），必须额外调一次 `/repos/{owner}/{repo}/collaborators/{user}/permission` API。Write 级调用会 `exit 1` 让 workflow 失败，在 Actions tab 留可审计记录。

## Policy 背景

内部 Write 级成员（junior dev / PM 等）能 push 代码，但不应有独立决定合入 main 的权力。**Maintainer+ 是"独立合入 main"的合适门槛**。

## 审计追踪

bot approve 的 review body：
> ✅ Self-approved via `/lgtm` comment by author @xuwenhao. Required CI checks still gate merge. @xuwenhao is accountable for the merged code.

加上 `self-approve` 标签，审计可以直接 `label:self-approve` 列出所有自审批 PR。

## 和现有机制的分工

```
场景                                              → 路径
──────────────────────────────────────────────────────────────
Claude 判 APPROVE + 低风险 + 非敏感 paths         → claude-review.yaml
                                                    (需先开 enable_auto_merge)

作者亲自 review 后 /lgtm（权限 Maintainer+）      → **本 workflow**

Write 级作者 /lgtm                                → workflow exit 1（失败）
                                                    作者需找 Maintainer+ approve

敏感路径 / 特殊场景                               → admin bypass
```

## Test plan

本 PR merge 后在实战中验证：

- [ ] 正向：Maintainer 作者 `/lgtm` → bot APPROVE + `self-approve` 标签
- [ ] 正向：`/lgtm 这个改动我测过了` → 触发（允许 reason 文字）
- [ ] 反测 1：Write 级作者 `/lgtm` → workflow exit 1 不 approve
- [ ] 反测 2：他人 `/lgtm` → workflow skip（不运行）
- [ ] 反测 3：`/lgtmify` → skip
- [ ] 反测 4：普通 issue `/lgtm` → skip
- [ ] Merge 阻塞：bot approve 后 code-quality 故意失败 → merge 按钮仍阻塞

## AI review 记录

Claude auto-review 和 Codex 两方**独立触到同一个 policy 盲点**（原版没有权限级别校验），都用 NEED_HUMAN_REVIEW 抛给人决定。已在 commit f96cd3426 修复。

## 相关

- Merge queue rollout: #952 + ruleset 已启用
- 不改现有 auto-merge 机制（claude-review.yaml 仍 \`enable_auto_merge: false\`）

## `2b0b5910` test(web): 4 small hooks 覆盖 (useIsAdmin / useRequireChat / useVersionCheck / useOfficialAgentCatalog) (#949)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T14:46:02Z
- **链接**: [2b0b5910](https://github.com/SerendipityOneInc/ecap-workspace/commit/2b0b5910e86d8af2b5a08cb283585a723148a230)

**PR #949 Description:**
Part of #894 — batched small-hook coverage pass.

## 新增 (4 files, 17 tests, 124 LoC source coverage)

| Hook | LoC | Tests | Key branches |
|---|---|---|---|
| \`useIsAdmin\` | 21 | 5 | null data, permissions array, non-array fallback, isLoading |
| \`useRequireChat\` | 26 | 2 | shouldShowOnboarding → redirect /chat, else passthrough |
| \`useVersionCheck\` | 40 | 3 | disabled=no-fetch, field mapping, invalidate on enabled transition |
| \`useOfficialAgentCatalog\` | 37 | 7 | cache init, fetch success/failure, null coerce, event listener, unmount guard |

## Why batched

这 4 个 hook 每个都 <50 LoC，各自独立且 mock boundary 不重叠。单独 PR 会
引入大量审查开销；合并为一个 PR 后仍保持 clear scope（每个 describe 块自
包含）。

## Bug-hunting 过程

- \`useOfficialAgentCatalog\` 的 mounted guard 正确保护 unmount 后 setState —
  测试中验证（避免 React 的 "setState on unmounted component" warning）
- \`useVersionCheck\` 的 enabled false→true invalidateQueries 逻辑确实存在，
  防止旧 stale \`needs_upgrade=true\` 一直显示 banner（生产代码设计正确）

未发现生产 bug。

Refs: #894

## `5d426b41` test(web): useAgentActions hook 覆盖 (#894 additional) (#955)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T14:45:35Z
- **链接**: [5d426b41](https://github.com/SerendipityOneInc/ecap-workspace/commit/5d426b4158dfde14ca9a291c2ecf8baf0c9d96be)

**PR #955 Description:**
Part of #894 — continued hook coverage.

## 新增

\`tests/unit/hooks/useAgentActions.unit.spec.ts\` — 13 tests 覆盖 useAgentActions 的所有公共 API + 错误路径。

## 覆盖要点

- **hireAgent** (3)：install + refresh / 错误 throw hire_failed / syncing lifecycle
- **fireAgent** (2)：uninstall + refresh / 错误 throw fire_failed
- **updateAgent** (2)：updatingAgentId lifecycle / 错误 throw update_failed
- **resetAgent** (3)：resettingAgentId lifecycle / 错误 throw reset_failed / **仅重置 session 不 refresh cache**（防误刷）
- **clearError()** + hiredIds Set + agents/isLoading 透传

## 关键发现：error-path + React 19 batched state

错误路径测试必须用 **手动 try/catch in act** 而不是 \`act().rejects.toThrow()\`：

\`\`\`ts
// ❌ FAILS: state updates from setError() never flush
await expect(act(...)).rejects.toThrow('hire_failed')
expect(result.current.error).toBe(...)  // still null!

// ✅ WORKS: act completes cleanly, state flushed, then assert
let thrown: Error | null = null
await act(async () => {
  try { await result.current.hireAgent(...) }
  catch (e) { thrown = e as Error }
})
expect(thrown?.message).toBe('hire_failed')
expect(result.current.error).toBe(...)  // ← correct
\`\`\`

原因：React 19 + vitest 4 下，\`act\` 内部 throw 导致 act 提前 reject，
state update queue 来不及 flush。手动捕获让 act 正常完成 → 状态刷新 →
断言稳定。

这是未来 hook 测试的参考模板（memo candidate）。

Refs: #894

## `134d69a7` test(web): useAgentSettings hook 覆盖 (#894 additional) (#954)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T14:44:50Z
- **链接**: [134d69a7](https://github.com/SerendipityOneInc/ecap-workspace/commit/134d69a758e3a80cf8c428825bd586d55e5a590d)

**PR #954 Description:**
Part of #894 — continued hook coverage.

## 新增

\`tests/unit/hooks/useAgentSettings.unit.spec.ts\` — 14 tests 覆盖 hook 全部
核心分支。

## 覆盖要点

### loadSettings (6 tests)
- 无 uid / agentId / enabled → 不调 API
- 正常 fetch → setSettings + cacheIdentity (no emit)
- Error reject → error 消息透传
- 非 Error reject → fallback "Failed to load agent settings"
- reload() 手动再 fetch

### saveIdentity (3 tests)
- 全量字段 → merge + setCachedAgentIdentity({emit:true})
- 只给 name → avatar 保留原值
- API reject → 返回 false + error 消息 + savingKey 清空

### saveModel (2 tests)
- **main agent**：Promise.all([updateClawModel, updateAgentModel]) —— 同时更新全局默认和 agent override
- **非 main agent**：仅 updateAgentModel，不调 updateClawModel

### saveBindings + savingKey lifecycle (2 tests)
- 保存成功 → settings.bindings 同步更新
- In-flight：savingKey === 'bindings' + saving === true；resolve 后都清空（用 pending promise + waitFor 验证）

## Bug-hunting 过程

未发现生产 bug。验证了：
- uid!/agentId! 断言在 useCallback guard 之后才调用（不会 null crash）
- savingKey 在 finally 块里必然清空（error path 也清）
- saveIdentity partial field preserve（避免清掉未传字段）

## 验证

\`\`\`bash
cd web
npx vitest run tests/unit/hooks/useAgentSettings.unit.spec.ts
# 14 tests pass
\`\`\`

Refs: #894

## `408f3bf5` refactor(orders): 拆分 create_order 降复杂度 (allowlist 7→6) (#953)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T14:31:28Z
- **链接**: [408f3bf5](https://github.com/SerendipityOneInc/ecap-workspace/commit/408f3bf50db3feb8e3bfce323c95752824024b26)

**PR #953 Description:**
## Summary

- 拆 `app/routes/orders.py::create_order` (原 C901=24) 为 3 个产品类型校验器 + 1 个 trial 纯函数 helper,主干 C901 远低于阈值 20
- `scripts/ci-lint/03-complexity.sh` ALLOWLIST 从 7 → 6(删 `create_order`),继 #948(`_do_billing_init`)后第二个彻底出清的条目
- 新增 2 个 topup 校验测试补全盲点(`TestCreateOrder` 原缺 topup 路径)

## 为什么这样改

PR #948 合并后 ALLOWLIST 剩 7 条,`create_order` 是其中下一个体量可控的目标(原 route 函数 153 行,三种产品类型线性校验密集)。拆成三个专职校验器 + 一个 trial 纯函数后,每个 helper 单一职责、易测易读,主干由"154 行 mixed"变成"55 行 orchestration"。

保留 `_validate_and_resolve_subscription_product` / `_validate_topup_product` 对 `request.stripe_product_id` 的 mutation — 这是原行为的 v1/v2 API 归一副作用,**PR 3 会下沉到 Pydantic `@model_validator` 消掉**。本 PR 严格 pure-move,不动语义。

## 细节

- \`plan_to_product\` dict 保留在函数内(call-time 读 SETTINGS),module-level 会打破 \`patch("app.routes.orders.SETTINGS")\` 的测试约定
- \`_compute_trial_eligibility\` 完全纯函数,\`test_orders_trial_logic.py\` 现有 7 个 case 已覆盖所有分支
- 新增 topup 测试:
  - \`test_topup_without_credits_amount_raises_400\`
  - \`test_topup_with_invalid_stripe_product_id_raises_400\`

## Test plan

- [x] \`ruff check app/ tests/\` + \`ruff format --check\`
- [x] \`pyright app/ tests/\` (0 errors)
- [x] \`bash scripts/ci-lint/01-file-length.sh\` (orders.py 491,低于 500)
- [x] \`bash scripts/ci-lint/03-complexity.sh\` (\`create_order\` 不再超标)
- [x] \`pytest tests/unit/\` (2429 passed)
- [x] 手工 sanity check:\`create_order\` 主干 C901 估算 ~14(远 < 20)

## 后续

- 本系列 PR 3:下沉 resolve+validate 逻辑到 \`OrderCreateRequest.@model_validator\`,彻底消除 request mutation(涉及 schema + 前端兼容验证,已在 plan 中)
- ALLOWLIST 目标 6 → 5

## `d46a106b` ci: 给 required workflow 加 merge_group trigger (merge queue PR 1/2) (#952)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T14:22:34Z
- **链接**: [d46a106b](https://github.com/SerendipityOneInc/ecap-workspace/commit/d46a106ba4af50a32cf6f34125fe082e03a0eae1)

**PR #952 Description:**
## Summary

为启用 GitHub Merge Queue 做准备。队列产生的 `merge_group` 事件需要 required status check 能在其上报告结果，否则队列会卡住。

本 PR **纯增量**：只加 trigger 和 `if:` 条件，不改变现有 `pull_request` / `push` 流程的行为。merge_group 事件在 PR 2（ruleset 启用 merge queue）合入前不会被触发。

## 背景和完整计划

见设计文档 `docs/superpowers/specs/2026-04-16-merge-queue-rollout.md`（随本 PR 一起提交）。

## 改动明细

### `code-quality.yml`
- `on:` 加 `merge_group:`（无 paths 过滤 —— 进队列的 PR 要完整测）
- `dorny/paths-filter` step 加 `if: github.event_name != 'merge_group'`（此 action 在 merge_group 下无默认 base ref，跳过是必须的）
- 4 个子 job (`web-quality` / `ios-quality` / `python-duplication-check` / `claw-interface-quality`) 的 `if:` 加 `|| github.event_name == 'merge_group'` 兜底运行
- 两处 Feishu 通知改为 `if: failure() && github.event_name == 'pull_request'`（白名单写法，merge_group 下 `github.event.pull_request.*` 为 null，通知内容会空白）

### `pr-size-check.yml`
- `on:` 加 `merge_group:`（reusable workflow 已有 `if: github.event.pull_request != null` 保护，自动 skip）

### `claude-review.yaml`
- `on:` 加 `merge_group:`
- `auto-review` job `if:` 加 `github.event_name == 'pull_request' &&`（队列里 skip —— AI review 入队前已做，重跑浪费 Claude token）

## Test plan

- [x] 本地 `git diff` 检查
- [ ] CI 下 3 个 required check (code-quality, auto-review, size) 在 `pull_request` 事件下行为不变（本 PR 开后验证）
- [ ] `merge_group` 事件在 PR 2 合入前不会触发，无法验证此阶段 —— 留到 PR 2 canary PR 验证

## 后续

- PR 2: ruleset 启用 merge queue + 关闭 `strict_required_status_checks_policy`（本 PR merge + CI 绿后）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `dc361489` refactor(billing): 拆分 _do_billing_init 降复杂度 (allowlist 8→7) (#948)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T14:19:02Z
- **链接**: [dc361489](https://github.com/SerendipityOneInc/ecap-workspace/commit/dc361489962bcd02160222527c2de01d66596fcd)

**PR #948 Description:**
## Summary

- 拆 `app/services/billing.py::_do_billing_init` (原 C901=26) 为 7 个单一职责 helper,主干 C901 远低于阈值 20
- 合并语义等价的 Path A (已初始化-同步) + Path B (部分钱包-补建),由 `_recreate_missing_wallets` 自洽处理"IDs 都在就跳过、缺哪个补哪个"
- `scripts/ci-lint/03-complexity.sh` ALLOWLIST 从 8 → 7 条(删 `_do_billing_init`)
- 新增 2 个 `_select_new_user_plan` 纯函数单测,钉住 "active 订阅 → starter / 其它 → free" 两分支

## 为什么这样改

棘轮要收就真收 — `03-complexity.sh` 尾部 "allowlist entries that no longer violate" 反向校验决定了"降复杂度 + 删 ALLOWLIST 必须同 PR"。不降到阈值下而只压到 ≤20 留着条目,等于把技术债从复杂度列表移到 allowlist 列表,没减少。

重构遵循 pure-move 原则:不改日志语义、不改异常语义、不改 `except Exception: return user` 的 fail-open 行为。Path A/B 合并是唯一的语义重排,`_recreate_missing_wallets` 对 IDs 都齐全的情况跳过两个 if,等价于旧 Path A 的 no-op。

## Test plan

- [x] `ruff check app/ tests/` + `ruff format --check app/ tests/`
- [x] `pyright app/ tests/` (0 errors/warnings)
- [x] `bash scripts/ci-lint/01-file-length.sh` (billing.py 483 行,回到阈值下)
- [x] `bash scripts/ci-lint/02-import-linter.sh` (8 contracts KEPT)
- [x] `bash scripts/ci-lint/03-complexity.sh` (`_do_billing_init` 消失)
- [x] `bash scripts/ci-lint/04-deptry.sh` / `05-no-collection-name-constants.sh` / `06-importlinter-repo-sync.sh`
- [x] `pytest tests/unit/` (2429 passed)

## 后续

同系列 PR 2(`create_order`)会紧跟,ALLOWLIST 目标 7 → 6。

## `d8f78d08` test(web): remove vacuous assertion in compact-mode test (follow-up to #946) (#947)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:58:31Z
- **链接**: [d8f78d08](https://github.com/SerendipityOneInc/ecap-workspace/commit/d8f78d08c138108ec624f1e62891b59307bb6dbc)

**PR #947 Description:**
Follow-up to #946 addressing Claude reviewer feedback.

## Feedback

Claude review on #946:
> The \`MessageActions\` React component is never rendered by OpenClawAssistantMessage (only \`copyToClipboard\` function is imported). So \`expect(container.querySelector('[data-testid^="msg-actions-"]')).toBeNull()\` is vacuously true — doesn't validate anything.

#946 merged before fix landed.

## Change

Remove the vacuously-true assertion from the compact-mode test. Keep the avatar-absent assertion (which IS meaningful). Add inline comment documenting why the MessageActions check was removed (防止未来添加 MessageActions 组件时误以为已经被测过).

Refs: #894 #897 #946

## `d894978d` test(web): OpenClawAssistantMessage 覆盖 (#897 Part 5) (#946)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:52:28Z
- **链接**: [d894978d](https://github.com/SerendipityOneInc/ecap-workspace/commit/d894978d658cabca505e70f2a56b50b5c86b3fed)

**PR #946 Description:**
Part of #894 Step 3 (#897) — Chat 消息三件套完成最后一件 (User ✅ + Assistant + [已测 hooks: Runtime/ArtifactsSidebar/MattermostIntegration])。

## 新增

\`tests/unit/app/chat/OpenClawAssistantMessage.unit.spec.tsx\` — 17 tests。

## 覆盖要点

### Render gates
- \`hasAnything=false\`（无 content/cards/thinking/attachments）→ null
- \`compact\`=true → 简单 bubble via MarkdownContent；无 avatar、无 hover actions

### Tool-group 特殊渲染（kind='tool-group'）
- 渲染 \`<ToolGroup>\` with steps, userQuery, isStreaming
- \`isStreaming = isLastMessage && thread.isRunning\`（非 last 时 false）
- \`showToolSteps=false\` → null
- \`toolGroup\` 空数组 → null
- \`precedingUserQuery\` 从上一条 user msg 提取

### Bot identity
- custom \`botName\` / 默认 "Assistant" / \`isSystem=true\` → "System"
- Avatar 4 种呈现（via resolveAssistantAvatarPresentation mock）：
  - image（DEFAULT_BOT_AVATAR）
  - animal → AnimalAvatar 组件
  - emoji → 显示 emoji 字符
  - system → 📢 图标

### Content
- **Thinking blocks** collapsible：header 显示，点击展开
- **MMAttachments**：image/non-image 分组渲染（防 PDF 双显：artifact card + MMAttachment）
- **ERMP cards**：custom.ermpCards（JSON strings）→ ERMPCardRenderer
- **Auto-detected cards**：detectMediaCards(text) 结果

## Mock 策略

使用 \`vi.hoisted()\` 包装所有 mock fns 以避开 vi.mock 顶层提升 TDZ 问题。
Mock assistant-ui 的 useMessage/useThread + 内部组件（MarkdownContent /
AnimalAvatar / ERMPCardRenderer / MessageActions / ToolGroup）— 保证测试
只验证 OpenClawAssistantMessage 自身逻辑，不耦合下游组件实现。

## Bug-hunting 过程

未发现生产代码 bug。验证了 non-image attachment 过滤（防止 PDF 既作为
artifact card 又作为 MM attachment 双重渲染的正确性）。

Refs: #894 #897

## `dcd724bf` test(web): useMattermostIntegration hook 覆盖 (#897 Part 4) (#945)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:43:26Z
- **链接**: [dcd724bf](https://github.com/SerendipityOneInc/ecap-workspace/commit/dcd724bff082a6184e48954dfd2cb594cde0e16b)

**PR #945 Description:**
Part of #894 Step 3 (#897) — Chat 消息三件套 + 相关 hooks。

## 新增

\`tests/unit/app/chat/useMattermostIntegration.unit.spec.ts\` — 14 tests 覆盖
hook 的主要行为。

## 覆盖要点

### mmConnected 计算（6 tests）
- \`connectionState !== 'connected'\` → false
- main agent 无 bots 仍连通（只要 activeChannelId 存在）
- main agent 优先选 \`agent_id='main'\` bot，否则 fallback 第一个
- non-main agent：channel 不匹配 bot channel → false
- non-main agent：channel 匹配 → true
- 无 matching bot → false

### mmUploadFiles（5 tests）
- 无 apiService / activeChannelId → 早退
- 成功上传：attachment uploading → done + fileId
- upload 返回空 → status failed
- upload reject（非 abort）→ captureChatError + status failed
- 非图片文件不生成 previewUrl

### onRemoveMmAttachment（1 test）
- 移除 attachment + revokeObjectURL

### channel alignment（2 tests）
- activeChannel 对齐 → 不调 selectChannel
- disconnected → 不调 selectChannel

## 技术点

- \`vi.hoisted()\` 包装 mock fns — \`vi.mock\` factory 被提升到文件顶部，
  普通 \`const\` 引用会 TDZ error
- \`afterEach(vi.unstubAllGlobals())\` — \`vi.stubGlobal\` 不会被 \`restoreMocks: true\`
  自动恢复，必须手动（避免 URL stub 跨 test 泄漏）

## 未覆盖的场景（留 E2E）

- Upload abort-race（removeAttachment 打断 in-flight upload）
- sendMMMessage 完整 flow（stubbed URL globals 与 renderHook 跨 test 交互不稳）
- channel misalignment auto-correction（effect 时序复杂）

这三类场景涉及 React effects + 异步 + stubbed globals 的组合，单测环境下
很难稳定复现，component-level E2E 更合适。

## Bug-hunting 过程

未发现生产代码 bug。验证了 abort race 保护（cancelledIdsRef 防 fileId 泄漏）
和 previewUrl 的条件生成逻辑。

Refs: #894 #897

## `5d9ceb65` test(web): add Date.now() fallback test for missing timestamp (follow-up to #941) (#942)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:25:49Z
- **链接**: [5d9ceb65](https://github.com/SerendipityOneInc/ecap-workspace/commit/5d9ceb65544a6a2bccc1d620fd6782a577522ac2)

**PR #942 Description:**
Follow-up to #941 addressing Claude reviewer feedback.

## Feedback

Claude review on #941:
> One minor test title inconsistency (Date.now fallback not actually tested) — non-blocking.

#941 merged before fix landed.

## Change

- Split the combined test ("timestamp and Date.now() fallback") into two:
  - \`uses message timestamp for createdAt\`
  - \`falls back to Date.now() when timestamp is 0 / missing\` — uses \`vi.setSystemTime\` to freeze Date.now so we can assert the exact fallback value
- Add module-scope \`afterEach(() => vi.useRealTimers())\` to guard against
  timer state leaking across tests (same defensive pattern as #928).

14 tests (was 13).

Refs: #894 #897 #941

## `3e81b956` feat(errors): Phases 4+5 — stripe services migration + C3 contract tighten (closes #873) (#943)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:25:09Z
- **链接**: [3e81b956](https://github.com/SerendipityOneInc/ecap-workspace/commit/3e81b9560038f77e4a0dc8114b53a488efc499f6)

**PR #943 Description:**
## Summary

Final migration PR for issue #873. Migrates the last 9 raise sites in stripe services to domain exceptions, then tightens the C3 import-linter contract by clearing the legacy-migration shrink list.

## Phase 4 — 9 raises

### \`stripe/portal.py\` (6)

| Line | Code | Old | Class |
|---|---|---|---|
| L25 | \`stripe.portal.invalid_return_url\` | 400 | \`DomainValidationError\` |
| L31 | \`stripe.portal.invalid_return_url_host\` | 400 | \`DomainValidationError\` |
| L40 | \`stripe.portal.user_not_found\` | 404 | \`NotFoundError\` |
| L44 | \`stripe.portal.no_stripe_customer\` | 400 | \`DomainValidationError\` |
| L59 | \`stripe.cancel.user_not_found\` | 404 | \`NotFoundError\` |
| L63 | \`stripe.cancel.no_subscription\` | 400 | \`DomainValidationError\` |

### \`stripe/order_confirm.py\` (3)

| Line | Code | Old | Class |
|---|---|---|---|
| L47 | \`stripe.order_confirm.missing_identifier\` | 400 | \`DomainValidationError\` |
| L64 | \`stripe.order_confirm.invalid_session_id\` | 400 | \`DomainValidationError\` |
| L94 | \`stripe.order_confirm.order_not_found\` | 404 | \`NotFoundError\` |

### Route caller update

\`app/routes/stripe.py\` — webhook / order_confirm / customer-portal / cancel-subscription all widen \`except HTTPException: raise\` → \`except (HTTPException, ServiceError): raise\` so migrated service errors preserve their status codes.

## Phase 5 — C3 contract tighten

Previously C3's \`ignore_imports\` had 3 entries (1 permanent + 2 legacy). This PR shrinks it to 1 entry (permanent-only):

\`\`\`toml
ignore_imports = [
    "app.services.asr.realtime_session -> fastapi",  # WebSocket — permanent
]
\`\`\`

Comment updated to document the new policy: **new entries must be permanent-and-justified (category 1); no more "pending migration" shrink-list.**

## Issue #873 status

With this PR merged, the full 46-raise migration is complete:

| Phase | Module(s) | Raises | PR |
|---|---|---|---|
| 2 (Item 2) | _resolve docstring | — | #881 ✅ |
| 1 (Item 1) | service-layer-exceptions spec | — | #882 ✅ |
| 0 | \`app/errors/\` + C3 contract | — | #889 ✅ |
| 1 | openclaw subdomain + leaf utilities | 17 | #907 ✅ |
| 2 | \`gift_code.py\` | 9 | #924 ✅ |
| 3 | \`invite_code.py\` | 10 | #929 ✅ |
| **4+5** | **\`stripe/*\` + contract close** | **9** | **this PR** |
| | **Total** | **45** | |

Plus infrastructure fix #940 (worktree pre-commit hooks). Issue can be closed after this merges.

## Verification

- [x] \`pyright app/ tests/\` — 0 errors
- [x] \`ruff check\` + \`ruff format --check\` — clean
- [x] All 8 import-linter contracts KEPT (C1, C2, C2b, C3, C4, C4b, C5, C6)
- [x] \`pytest tests/unit/\` — **2426 passed**
- [x] \`pytest tests/bdd/\` — **342 passed**
- [x] Local pre-commit hooks ran end-to-end before push (thanks to #940)
- [ ] CI green

Refs #873.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `7621631b` test(web): useOpenClawRuntime hook 覆盖 (#897 Part 3) (#941)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:13:12Z
- **链接**: [7621631b](https://github.com/SerendipityOneInc/ecap-workspace/commit/7621631b41dcfcf843d2ed3f05e4fe52e4e3cd02)

**PR #941 Description:**
Part of #894 Step 3 (#897) — Chat 消息三件套 + 相关 hooks。

## 新增

\`tests/unit/app/chat/useOpenClawRuntime.unit.spec.ts\` — 13 tests 覆盖
\`useOpenClawRuntime\` 所有内部行为。

## 覆盖要点

- **convertMessage**（内部函数，通过 hook 返回值验证）：
  - text message → single text part
  - tool-group 消息 → 空 content + \`metadata.custom.kind='tool-group'\`
  - 空内容 non-tool-group 消息 → 仍带 text 空串（避免 assistant-ui 空 content 报错）
  - 所有 metadata custom 字段传递（ermpCards / thinkingBlocks / _sessionKey / mmAttachments / mmReactions）
  - \`isSystem\` 消息被 \`filterMessages\` 过滤掉
  - \`createdAt\` 从 timestamp 构造（Date 实例）
- **Dedup**：相同 id 只保留最后一条；dedup 后顺序稳定
- **onNew** 回调：
  - 提取 text part → 调用 \`sendMessage\`
  - 无 text part → 跳过
  - 即使 rerender 后 \`sendMessage\` 变了，ref 更新让 onNew 调用 **最新** 的（验证 stable callback 设计）
- **onCancel** → 调用 \`abortGeneration\`
- **外部 store 透传**：\`isGenerating → isRunning\`、\`convertMessage\` 身份传递

## 策略

\`useExternalStoreRuntime\` 来自 \`@assistant-ui/react\`，内部复杂。Mock 它以
**捕获参数**，但保留真实 \`filterMessages\` + \`aggregateToolMessages\` 来测
"完整管道"，这样也顺带验证了 filter 逻辑在 hook 调用路径上生效。

## Bug-hunting 过程

未发现生产代码 bug。验证了 \`isSystem\` 过滤 + dedup 逻辑按预期工作。

## 验证

\`\`\`bash
cd web
npx vitest run tests/unit/app/chat/useOpenClawRuntime.unit.spec.ts
# 13 tests pass
\`\`\`

Refs: #894 #897

## `24681461` refactor(scheduler): cleanup_stale_jobs 改走 session_job_repo + 收尾 scheduler C1 (PR 3/6) (#939)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:12:09Z
- **链接**: [24681461](https://github.com/SerendipityOneInc/ecap-workspace/commit/24681461635bf2fd3653acc9822b85dc1fb2f9b1)

**PR #939 Description:**
## Summary
- `app/scheduler.py::cleanup_stale_jobs` 的 2 处 `mongo.read/update` 改走 PR #932 新增的 `session_job_repo.find_stale_jobs` / `mark_failed`
- 同步删除 C1 合约 `ignore_imports` 里最后一条 legacy 豁免 `app.scheduler -> favie_common`（stale ignore 条目会让 `lint-imports` 硬失败）
- 顺手修一个被 pyright 抓出来的 silent bug：`job.get("job_id")` 返回 `str | None`，原 mongo 直调 `{"job_id": None}` 会广播匹配所有缺字段文档——现在 repo 强类型逼出空值检查，malformed 文档显式跳过并记 warning
- 扩展 `scripts/ci-lint/05-no-collection-name-constants.sh` 的扫描范围到 `app/scheduler.py`（防未来回退）

## Context
6 PR 系列（cron/scheduler C1 收尾）的第 3 步。plan 在 `/home/node/.claude/plans/spicy-drifting-mountain.md`。

依赖 PR #932（已合并）提供的 `session_job_repo`。前序 PR #934 已完成 cron 迁移。合入后 C1 合约的 legacy 豁免表只剩 `routes/session/*.py` 4 条（另属 routes legacy epic）。

### 发现的 silent bug

重构前的代码：
```python
job_id = job.get("job_id")   # returns str | None
...
await mongo.update(SESSION_JOB_COLLECTION, {"job_id": job_id}, ...)
```
如果 `job_id` 是 None，这会把匹配扩展到**所有 `job_id` 为 None 的文档**——不是 no-op。新加的 test_missing_job_id_skipped pin 住新行为：跳过并记 warning。

### 偏离原 plan

原 plan 的 PR #4 是「合并解除 cron+scheduler C1 豁免」。由于 `lint-imports` 对 stale ignore 条目硬失败，PR #934 和本 PR 已各自自带解除步骤 → PR #4 收窄至「no-collection-names 扩展」，而本 PR 把这个扩展顺手带上，PR #4 此后可能完全合并进来或单独做。

## Test plan
- [x] `pytest tests/unit/test_scheduler.py -v` — 13 测全过（+ 1 new test_missing_job_id_skipped）
- [x] `pytest tests/unit -x -q` — 全仓 2427 测全过
- [x] `pyright app/ tests/` — 0 errors（silent bug 修前报 2 errors）
- [x] `ruff format --check` / `ruff check` — clean
- [x] `lint-imports` — 6 合约全 KEPT
- [x] `bash scripts/ci-lint/05-no-collection-name-constants.sh` — clean，coverage now includes scheduler.py

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `adc311ca` fix(worktree): enable pre-commit hooks inside worktrees (#940)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:08:49Z
- **链接**: [adc311ca](https://github.com/SerendipityOneInc/ecap-workspace/commit/adc311cacbd446385df110d673cf30b3aa7fafa0)

**PR #940 Description:**
## Summary

New worktrees created by \`scripts/worktree.sh\` silently skip all git hooks, because \`pnpm install\` doesn't regenerate \`.husky/_/\` inside the new checkout and the shared \`core.hooksPath = .husky/_\` points at a directory that doesn't exist there.

Result: \`.husky/pre-commit\` — which runs \`ruff-format\`, \`ruff\`, \`pyright\`, and all \`scripts/ci-lint/*.sh\` guards — never fires in worktrees. CI ends up catching format / lint / type errors that the hook would have caught locally. This session alone had three round-trips (#881, #907, #929) where CI caught \`ruff format --check\` failures that pre-commit should have auto-fixed.

## Fix

Append a step to \`scripts/.worktree-setup.sh\` that, on worktree creation:

1. Sets \`extensions.worktreeConfig=true\` (idempotent; enables per-worktree config file).
2. Sets \`core.hooksPath=.husky\` at worktree scope — bypasses the missing \`.husky/_/\` directory and points git directly at \`.husky/pre-commit\`.

Only affects newly-created worktrees. Main's shared \`core.hooksPath=.husky/_\` stays untouched so its existing husky \`_/\` indirection layer still works.

## Tradeoff

The worktree hook path skips husky's \`_/h\` wrapper, which adds \`node_modules/.bin\` to PATH and honors \`HUSKY=0\` to disable hooks. \`.husky/pre-commit\` explicitly calls \`pnpm\` (already in PATH from the shell) and delegates Python checks to an absolute \`pre-commit\` path, so nothing relies on the wrapper's PATH extension. \`HUSKY=0\` disable won't work in worktrees, but that's a rare escape hatch.

## Retroactive fix for existing worktrees

Not automated by this PR (script only fires on \`worktree.sh\` create). Run once per existing worktree:

\`\`\`bash
git -C <worktree> config extensions.worktreeConfig true
git -C <worktree> config --worktree core.hooksPath .husky
\`\`\`

## Test plan

- [x] Manually applied the same config in an existing worktree (fix-issue-873)
- [x] Created an unformatted Python file, staged it, ran \`.husky/pre-commit\` → ruff-format auto-reformatted, hook exit reflects the mutation
- [ ] Create a fresh worktree via \`bash scripts/worktree.sh test-hooks --no-tmux\`, verify \`git -C .worktrees/test-hooks config core.hooksPath\` returns \`.husky\`, and a hook-triggering commit runs ruff-format

Unrelated to #873 migration PRs (#929 etc.); this is developer infrastructure.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `75bd370b` test(web): drop redundant second rerender in useArtifactsSidebar streaming test (follow-up to #933) (#938)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:03:16Z
- **链接**: [75bd370b](https://github.com/SerendipityOneInc/ecap-workspace/commit/75bd370bb3536e8da4edabd684c26d2de6934bf9)

**PR #938 Description:**
Follow-up to #933 addressing Claude reviewer feedback.

## Feedback

Claude review:
> The second rerender in the streaming auto-open test is likely redundant (first rerender already fires both effects in order), but tests remain correct either way.

#933 merged before fix landed — opening as follow-up.

## Change

Delete the second \`rerender(msgContent + ' ')\` call. React runs effects in declaration order within the same render, so the first rerender is enough:
1. generating effect arms \`pendingFileCheckRef = true\`
2. messages effect consumes it → opens sidebar

Simpler and more accurate to the actual React semantics.

Refs: #894 #897 #933

## `0291d6df` feat(importlinter): 新增 C5 (HTTP 工具) + C6 (skills/tasks 叶) 合约 (PR 6/6) (#937)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T13:02:09Z
- **链接**: [0291d6df](https://github.com/SerendipityOneInc/ecap-workspace/commit/0291d6df5c165b3ebe69caa66684d02411831e9b)

**PR #937 Description:**
## Summary
- **C5**：`app.auth` / `app.connectors` / `app.errors` 禁止直接 import `favie_common`——把 mongo-isolation 边界从 routes/services/database 扩展到这些 HTTP 工具层。允许它们调 `app.services`（`auth/dependencies → services/profile` 解析 current_user 是合理的）。
- **C6**：`app.services` / `app.database` / `app.schema` 禁止 import `app.skills` / `app.tasks`——skills/tasks 是扩展点，关系应单向。
- 顺手干掉 `app.services.integration_tools` 的 23 行 backward-compatibility shim（文件注释已说 "all functionality moved to app.skills"，唯一 caller 是 `tests/unit/test_integration_tools.py`），按 memory `feedback_no_reexport_shim`「共享模块抽取时改掉所有 caller，不留兼容转发层」处理。

## Context / 背景
6 PR 系列的第 5 步（独立，不依赖其他 PR）。plan 在 `/home/node/.claude/plans/spicy-drifting-mountain.md`。本次工作契机：三份 Explore agent 报告发现 `auth/connectors/errors/skills/tasks` 五个目录没被任何合约覆盖，是隐形 gap。

### C5 边界决策回顾
用户在 plan 阶段确认：**允许 auth→services**（memory 习惯：小范围硬 guardrail > 大范围清洁理论）。C5 只禁直调 mongo，不限制 auth 跨层。

### C6 触发的一个 legacy 清理
`integration_tools.py` 是个已经迁移后留下的 shim。`PROVIDER_DISPLAY` 和 `INTEGRATION_TOOLS` 符号都在 `app/skills/__init__.py` 里有原样定义，所以删 shim + 改 1 处测试 import 就够。production 无 caller。

## Test plan
- [x] `lint-imports` — 8 合约全 KEPT（C1-C6 + 新增 C5/C6）
- [x] `ruff format --check` / `ruff check` — clean
- [x] `pyright app/ tests/` — 0 errors
- [x] `pytest tests/unit -x -q` — 2421 测全过
- [x] `bash scripts/ci-lint/02-import-linter.sh` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `ad716290` test(web): useArtifactsSidebar hook 覆盖 (#897 Part 2) (#933)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:57:55Z
- **链接**: [ad716290](https://github.com/SerendipityOneInc/ecap-workspace/commit/ad716290dfd1eb4e91bdbe2b851aaa4e259560e2)

**PR #933 Description:**
Part of #894 Step 3 (#897).

## 新增

\`tests/unit/app/chat/useArtifactsSidebar.unit.spec.ts\` — 11 tests 覆盖
hook 所有分支。

## 覆盖要点

- **初始 state**：closed + null activeFile
- **window.openFilePreview 注册/卸载**（mount + unmount lifecycle）
- **openFilePreview 回调**：打开 sidebar + 设置 activeFile + close subagent
- **closeArtifacts**：reset state
- **流式结束自动打开**：
  - effectiveIsGenerating: true → false 时 armed
  - 有 previewable link → 打开
  - 无 file link → 不打开
  - 只有 non-previewable (.zip) → 不打开
- **URL sync**：同名文件 URL 变化时 activeFile 跟着更新
- **Mattermost 分支**：
  - mmConnected=true + 新 assistant msg + previewable file → 打开
  - mmConnected=false → 不打开（跳过整个 effect）
  - prevMmAssistantCountRef 防重：相同消息数 rerender 不触发

## Bug-hunting 过程

未发现生产代码 bug。一个验证副产物：**测试必须用 \`artifacts.zooclaw.ai\`
或 \`artifacts.claw.yesy.live\` 主机的 URL**（否则 isArtifactUrl 过滤掉）——
这是合理的 artifact 隔离措施，不是 bug。

## Verification

\`\`\`bash
cd web
npx vitest run tests/unit/app/chat/useArtifactsSidebar.unit.spec.ts
# 11 tests pass
\`\`\`

Refs: #894 #897

## `b7e3ca38` test(web): assert isCopied state transition after copy click (follow-up to #928) (#931)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:57:23Z
- **链接**: [b7e3ca38](https://github.com/SerendipityOneInc/ecap-workspace/commit/b7e3ca38f8ea6475db086c59932629bac6a95ccd)

**PR #931 Description:**
Follow-up to #928 addressing Claude + Codex reviewer feedback.

## Feedback (both reviewers agreed)

Claude:
> The copy button test asserts \`copyToClipboard\` was called but doesn't verify the \`isCopied\` UI state transition (button switching to a checkmark SVG, tooltip showing "Copied"). Since \`mockCopyToClipboard.mockResolvedValue(true)\` is set in \`beforeEach\`, exercising the \`setCopiedId\` path would complete the test's stated intent.

#928 merged before this fix could land — opening as follow-up per memory 约定.

## Change

Add 1 test in \`OpenClawUserMessage.unit.spec.tsx\`: click \`genclaw-user-copy\`, assert tooltip starts with "Copy" and transitions to "Copied" via \`waitFor\` (after \`copyToClipboard\` resolves and \`setCopiedId\` fires).

## 实现选择：waitFor 而非 fakeTimers

原始 reviewer 建议用 \`vi.useFakeTimers()\` + \`vi.advanceTimersByTime(2000)\`
覆盖"2s 后 revert 回 Copy"的 timing detail。实测发现：

- React 在 jsdom 下的批处理 + 组件的 \`setTimeout(..., 2000)\` + \`setState\`
  存在微妙竞态——advanceTimersByTimeAsync(2000) 后 textContent 仍包含 "Copied"，
  需要额外 flush + act() 才能断言，代码复杂且脆弱
- "点击后进入 Copied"是单测真正需要锁的行为；"2s 后 revert" 属于 UX timing
  detail，留给 E2E 更合适

采用 \`waitFor(() => ... toContain('Copied'))\` —— 简洁稳定，覆盖关键状态翻转。
15 → 16 tests。

## Verification

\`\`\`bash
cd web
npx vitest run tests/unit/app/chat/OpenClawUserMessage.unit.spec.tsx
# 16 tests pass (was 15)
\`\`\`

Refs: #894 #897 #928

## `36f917a5` feat(database): session_job_repo for scheduler cleanup (PR 1/6) (#932)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:56:33Z
- **链接**: [36f917a5](https://github.com/SerendipityOneInc/ecap-workspace/commit/36f917a5f8ef7121dc1e4c538c5e0f671838ef30)

**PR #932 Description:**
## Summary
- 新增 `app/database/session_job_repo.py`，封装 scheduler stale-job cleanup 需要的两个 mongo 操作：`find_stale_jobs(cutoff_time, limit)` + `mark_failed(job_id, error_message, last_updated)`
- 同步在 `pyproject.toml` 注册 C1/C4/C4b 三处合约条目（遵守 `services/claw-interface/CLAUDE.md` 的硬要求，`scripts/ci-lint/06-importlinter-repo-sync.sh` 自动校验）
- 配套单测 `tests/unit/test_session_job_repo.py`，pin 住 query shape / update 语义

## 背景与范围

这是一个 6 PR 系列的第一步，目标是为 `app/cron/subscription_cron.py` 和 `app/scheduler.py` 收尾 C1 合约的 legacy 豁免（它们目前直接调 `mongo.read/update`）。详见 plan 文件 `/home/node/.claude/plans/spicy-drifting-mountain.md`。

### 和原始 plan 的偏差

Plan 原定新建两个 repo：`subscription_cron_repo` + `session_job_repo`。读代码后发现 `cron/subscription_cron.py` 的 mongo 调用**全部**是对 `ACCOUNT_COLLECTION` 的操作，可以直接用现有 `user_repo.list_users(query, limit, offset, sort)` 和 `user_repo.update_fields(uid, fields)`——新建 `subscription_cron_repo` 会是纯包装层，维护成本高。本 PR 收窄到只建 `session_job_repo`（scheduler 需要，但 SESSION_JOB_COLLECTION 没有现成 repo）。下一步 PR 的 cron 迁移直接调 `user_repo`。

### 不动的内容

- Scheduler 和 cron 还是原样直接 import `favie_common`（各自在 C1 `ignore_imports` 里），本 PR 不解除豁免——避免本 PR 同时改调用方和合约
- 不改 `routes/session/*.py` 里对 SESSION_JOB_COLLECTION 的 20+ 处 legacy mongo 直调（它们另有 C1 豁免，属于独立 routes legacy epic 范围）

## Test plan
- [x] `pytest tests/unit/test_session_job_repo.py -v` — 5 测全过
- [x] `pytest tests/unit -x -q` — 全仓 2420 测全过，无退化
- [x] `ruff format --check app/ tests/` — clean
- [x] `ruff check app/ tests/` — clean
- [x] `pyright app/ tests/` — 0 errors, 0 warnings
- [x] `lint-imports` — 6 合约全 KEPT
- [x] `bash scripts/ci-lint/06-importlinter-repo-sync.sh` — 13 个 repo 三处合约列表对齐
- [x] `bash scripts/ci-lint/01-file-length.sh` — 新文件都在 500 行上限内

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `48c5cc48` chore: remove empty app/service/ ghost directory (PR 5/6) (#936)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:55:47Z
- **链接**: [48c5cc48](https://github.com/SerendipityOneInc/ecap-workspace/commit/48c5cc48d67865cd0979e6c527f2a422cce39c0e)

**PR #936 Description:**
## Summary
- 删除 `services/claw-interface/app/service/`（单数）目录——仅含 17 字节 `__init__.py` 的 `# business logic` 占位注释
- 全仓零引用：`grep -rn "from app.service \|import app.service"` 在排除 `app.services`（复数）后无命中
- 这是个 footgun：容易有人误把文件加到这里而不是真正的 `app/services/` 层

## Context
属于 6 PR 系列的独立清理步骤。plan 在 `/home/node/.claude/plans/spicy-drifting-mountain.md`。

## Test plan
- [x] `grep -rn "app.service[^s]" services/claw-interface/` — 无命中
- [x] `pyright app/ tests/` — 0 errors
- [x] `lint-imports` — 6 合约全 KEPT
- [x] `pytest tests/unit -x -q` — 2421 测全过

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `1d92c229` refactor(cron): subscription_cron 改走 user_repo + 抽 3 helper (PR 2/6) (#934)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:55:27Z
- **链接**: [1d92c229](https://github.com/SerendipityOneInc/ecap-workspace/commit/1d92c2298b72957b2b55e3e5b6c3080181847242)

**PR #934 Description:**
## Summary
- `app/cron/subscription_cron.py` 的 6 处 `mongo.read/update` 全部改走现有 `user_repo.list_users` / `user_repo.update_fields`
- 抽出 3 个 helper 函数，消除 `check_trial_expiry` / `check_yearly_credits_reset` / `check_subscription_sync` 三者间重复的 Stripe 状态查询 + 过期处理 + 续期处理分支
- 从 C1 合约 `ignore_imports` 删除 `app.cron.subscription_cron -> favie_common` 豁免（stale ignore 条目会让 `lint-imports` 硬失败，所以必须同步删）

## Context / 背景
属于 6 PR 系列（cron/scheduler C1 收尾）的第二步。plan 在 `/home/node/.claude/plans/spicy-drifting-mountain.md`，前置 PR 是 #932（session_job_repo）。

### 抽出的 helpers

| Helper | 消除的 call sites | 作用 |
|--------|-------------------|------|
| `_get_stripe_status_safe(sub_id, uid, cron_label)` | 3× | `stripe.Subscription.retrieve_async` + fail-open warning，返回 `(sub, status)` 或 `(None, None)` |
| `_handle_expired_subscription(user, uid, cron_label)` | 4× | clear_wallet 保护式调用 + `transition_to_expired` + `_sync_team_models("free")` + `sync_bot_resources("free")` + `stop_user_bots` |
| `_handle_active_renewal(user, uid, *, plan, billing_cycle, ending_at, cron_label)` | 2× | `process_cron_renewal` + 若 renewed 则 `_sync_team_models(plan)` + `sync_bot_resources(plan)` |

### 偏离原 plan

原 plan 的 PR #4 是「解除 cron + scheduler 的 C1 legacy 豁免」。但 `import-linter` 对 stale `ignore_imports` 条目硬失败（exit 1 + "No matches for ignored import X"），所以迁移 PR 必须同步删自己的条目。→ 原 PR #4 范围收窄至仅 `scripts/ci-lint/05-no-collection-name-constants.sh` 的 scheduler 扫描扩展。scheduler 那条豁免会在 PR #3 中同步删。

同时确认：原 plan 的「新建 `subscription_cron_repo`」是多余的——cron 的 mongo 调用全是 `ACCOUNT_COLLECTION` 操作，现有 `user_repo` 的 `list_users` / `update_fields` 直接够用。已在 PR #932 的 description 里记录这次 scope 收窄。

## Test plan
- [x] `pytest tests/unit/test_subscription_cron.py -v` — 12 测全过
- [x] `pytest tests/unit -x -q` — 全仓 2418 测全过
- [x] `ruff format --check app/ tests/` — clean
- [x] `ruff check app/ tests/` — clean
- [x] `pyright app/ tests/` — 0 errors, 0 warnings
- [x] `lint-imports` — 6 合约全 KEPT
- [x] `bash scripts/ci-lint/03-complexity.sh` — 无新增复杂度违规
- [x] `bash scripts/ci-lint/05-no-collection-name-constants.sh` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `ea5bf176` fix(agent-updates): require session reset and preserve redeploy files (#930)
- **作者**: nolan-srp
- **时间**: 2026-04-16T12:42:31Z
- **链接**: [ea5bf176](https://github.com/SerendipityOneInc/ecap-workspace/commit/ea5bf176443b7e854b17daf8801c85b0486cf106)

**PR #930 Description:**
## Summary
- require an explicit fresh-session reset after agent updates in the agents manager and agent detail flows
- add the reset-state handling and localized copy for the updated post-update UX
- preserve allowlisted workspace files during pack redeploys so workspace-managed files are not overwritten

## `07565b1b` feat(errors): Phase 3 — migrate invite_code service to domain exceptions (#873) (#929)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:29:19Z
- **链接**: [07565b1b](https://github.com/SerendipityOneInc/ecap-workspace/commit/07565b1b17dacb0383a9746e91f2cb3fec045b68)

**PR #929 Description:**
## Summary

Phase 3 of service-layer exception decoupling per [spec](../blob/main/docs/superpowers/specs/2026-04-16-service-layer-exceptions.md). Migrates all 10 raise sites in \`app/services/invite_code.py\` from \`fastapi.HTTPException\` to \`app.errors.ServiceError\` subclasses.

### Exception mapping

| Line | Code | Old status | Class |
|---|---|---|---|
| L26 | \`invite_code.generate_unique_failed\` | 500 | \`ServiceError\` |
| L40 | \`invite_code.invalid_code\` | 400 | \`DomainValidationError\` |
| L45 | \`invite_code.disabled\` | 400 | \`DomainValidationError\` |
| L49 | \`invite_code.expired\` | 400 | \`DomainValidationError\` |
| L55 | \`invite_code.quota_exceeded\` | 400 | \`DomainValidationError\` |
| L69 | \`invite_code.already_bound_to_user\` | 400 | \`DomainValidationError\` |
| L74 | \`invite_code.disabled\` (post-CAS) | 400 | \`DomainValidationError\` |
| L77 | \`invite_code.expired\` (post-CAS) | 400 | \`DomainValidationError\` |
| L80 | \`invite_code.quota_exceeded\` (post-CAS) | 400 | \`DomainValidationError\` |
| L82 | \`invite_code.binding_conflict\` | 409 | \`ConflictError\` |

All detail values are plain strings (no dict-shape frontend contract like gift_code had), so this migration is mechanically straightforward — no Phase 0 type extensions needed.

### Route caller update

\`app/routes/user.py::bind_invite_code_endpoint\` (L162) had \`except HTTPException: raise\` + \`except Exception: raise HTTPException(500)\`. After migration, invite_code service raises \`ServiceError\`; widened first clause to \`except (HTTPException, ServiceError): raise\` so domain errors keep their status codes and don't get wrapped as 500.

### Tests

- \`tests/unit/test_invite_codes.py\`: 10 assertions updated from \`HTTPException(status_code=X)\` to specific domain class + \`.code\` check.
- BDD (\`tests/bdd/step_defs/test_invite_code.py\`): zero changes needed — the helpers (\`capture\`, \`error_status\`) generalized in Phase 1 already bridge both exception types.

### C3 ignore_imports

Shrunk 3 → 2 entries:
- Permanent: \`asr/realtime_session\` (WebSocket)
- Legacy: \`stripe/portal\`, \`stripe/order_confirm\` (pending Phase 4)

### Verification

- [x] \`pyright app/ tests/\` — 0 errors
- [x] \`ruff check\` / \`ruff format --check\` — clean
- [x] All 6 import-linter contracts KEPT
- [x] \`pytest tests/unit/\` — **2416 passed**
- [x] \`pytest tests/bdd/\` — **342 passed**
- [ ] CI green

### Depends on

PR #924 (Phase 2, merged) — baseline \`app/errors/*\` type signature with \`detail: str | dict\`, BDD helper infrastructure.

### Next

Phase 4: \`stripe/portal.py\` (6 raises) + \`stripe/order_confirm.py\` (3 raises). Last migration phase before Phase 5 tightens the C3 guard.

Refs #873.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `a9a35ca4` test(web): OpenClawUserMessage 覆盖 (#897 Part 1) (#928)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:26:08Z
- **链接**: [a9a35ca4](https://github.com/SerendipityOneInc/ecap-workspace/commit/a9a35ca48ad3baefcb96fa46259623bbca0011b4)

**PR #928 Description:**
Part of #894 Step 3 (#897) — Chat 消息三件套 + 相关 hooks。

## 新增

\`tests/unit/app/chat/OpenClawUserMessage.unit.spec.tsx\` — 15 tests 覆盖
OpenClawUserMessage **94.73% (54/57 行)**

## 覆盖要点

- **Text 提取**：过滤非 text 类型 part，多个 text part join 换行
- **compact 模式**：简单 bubble、无 hover actions、无 UserAvatar
- **Blockquote 解析**：\`> \` 前缀的 quote + reply 分离
  - Quote 超过 120 字符截断 + \\u2026 省略号
  - Quote + 空行 + reply 正确切分
- **Card action pills**：
  - \`[ACTION:card_id] option_name\` → "已选择: option name"
  - \`[FORM:card_id] {...}\` → "已提交表单"
- **Mattermost metadata**：
  - \`custom.mmAttachments\` 渲染 MMAttachments 组件
  - \`custom.mmReactions\` 去重聚合 + count > 1 时显示数字
  - 未知 emoji_name fallback 到 \`:name:\` 字面显示
- **Auto-detected media cards**：调用 \`detectMediaCards(reply, true)\`
  - skipArtifactCheck=true (R2 上传域)
  - 渲染 ERMPCardRenderer
- **Copy 交互**：点击复制按钮 → \`copyToClipboard(reply)\`
- **MessageActions 条件渲染**：\`isLastMessage=true\` + \`text\` 非空 显示；否则不显示
- **UserAvatar fallback**：
  - \`auth.currentUser.photoURL\` → img
  - 无 photoURL + email → 首字母大写
  - 无 photoURL + 无 email + phone → 首字符

## Bug-hunting 过程

未发现生产代码 bug。所有关键分支（card action/form、metadata 解析、
fallback 链）测试断言均匹配源码行为。

## 验证

\`\`\`bash
cd web
npx vitest run tests/unit/app/chat/OpenClawUserMessage.unit.spec.tsx  # 15 pass
pnpm test:unit  # full suite pass
npx tsc --noEmit && pnpm lint  # clean
\`\`\`

Refs: #894 #897

## `74d7c69c` feat(web): 版本升级浮动弹窗 + Changelog 独立页面 (#920)
- **作者**: lynn Zhuang
- **时间**: 2026-04-16T12:24:19Z
- **链接**: [74d7c69c](https://github.com/SerendipityOneInc/ecap-workspace/commit/74d7c69c51b66b574d069861f08b61e3e35ce111)

**PR #920 Description:**
## 概要
  - 新增左下角浮动版本升级弹窗，替换原有顶部 UpgradeNotificationBanner
    - 暖色渐变背景 + 龙虾装饰图，Figma 设计稿还原
    - 「What's new」新标签页打开 Changelog 页面
    - 「Refresh now」触发 bot redeploy 后整页刷新更新版本
  - 新增独立 Changelog 页面 `/{locale}/changelog`
    - ZooClaw 官方 SVG logo
    - 时间线布局，按时间倒序展示版本发布记录
    - 完全独立页面，无侧边栏和 Onboarding 干扰

  ## 改动文件
  | 文件 | 说明 |
  |------|------|
  | `web/src/components/VersionUpgradeWidget.tsx` | 新增浮动升级弹窗组件 |
  | `web/src/app/[locale]/changelog/page.tsx` | Changelog 页面入口 |
  | `web/src/app/[locale]/changelog/ChangelogClient.tsx` | Changelog
  客户端组件（时间线 + logo） |
  | `web/public/images/upgrade-mascot.png` | 龙虾装饰图 |
  | `web/src/app/globals.css` | 新增 `--ecap-upgrade-widget-bg` CSS 变量 |
  | `web/src/app/[locale]/chat/GenClawClient.tsx` | 替换 Banner → Widget |
  | `web/src/components/AppLayout.tsx` | Changelog 排除在侧边栏布局之外 |
  | `web/src/components/onboarding/OnboardingProvider.tsx` | Changelog 排除在
  Onboarding 之外 |
  | `web/src/locales/en.ts` / `zh.ts` | 多语言文案 |

  ## 测试计划
  - [ ] 有版本更新时 → 左下角浮动弹窗出现，龙虾图贴左下角
  - [ ] 点击 X → 弹窗关闭
  - [ ] 点击「What's new」→ 新标签页打开 `/en/changelog`
  - [ ] 点击「Refresh now」→ 触发 redeploy + 页面刷新
  - [ ] Changelog 页面 → 显示 ZooClaw logo、时间线、版本记录
  - [ ] Changelog 页面无侧边栏、无 Onboarding 弹窗
<img width="2542" height="1728" alt="screenshot-20260416-185617" src="https://github.com/user-attachments/assets/4c5867c2-52ab-4bf9-aec4-02d58509bc25" />
<img width="2556" height="1724" alt="screenshot-20260416-185641" src="https://github.com/user-attachments/assets/16285af7-c191-43f9-a193-597126938c9f" />

<img width="2550" height="1732" alt="screenshot-20260416-185630" src="https://github.com/user-attachments/assets/07dd44df-21cb-4a82-8992-f8863f053332" />

## `df60173c` feat(billing): align Starter trial UX across subscription panel (#914)
- **作者**: vincent-srp
- **时间**: 2026-04-16T12:14:36Z
- **链接**: [df60173c](https://github.com/SerendipityOneInc/ecap-workspace/commit/df60173cc76673204653154b1a1a00bbe36a22c0)

**PR #914 Description:**
## Summary
- 让"开始免费试用"的 UI（红色 ribbon、`$0 for 7 days, then $X/mo` 价格、`Start Free Trial` CTA）**严格跟随真实 trial 权益**：`!hasUsedTrial && (userStatus === 'trial' || 'asleep')`。之前 asleep + 从未用过 trial 的新用户看不到免费试用提示；已用过 trial 的脏数据态会错误展示。
- Starter 试用文案从 "$20/month" 改为 `$0 for 7 days, then $X/mo` 单行（参考 `PaywallContent` 的 gift 面板模式），消除 "$0 vs $X" 歧义。
- 修两个 banner + UserCard 时钟图标的脏数据 bug：`pendingDowngrade` / `cancelAtPeriodEnd` 在订阅过期（`asleep`）时后端可能不清，现在前端 gate 在 `(active || trialing)`，与 `SharedPlanCard` / `ProfileTab` 的既有约定对齐。
- 按设计要求去掉顶部 trial 倒计时 pill + 绿色 `CURRENT PLAN` 标签。
- 把 `.badge-free` 红色促销 pill 提到 `globals.css` 的 `@layer utilities`，让 Annually 的 "Save 2 months" 和 `PublicPricingClient` 的 "2 months free" 共享一份定义。

## Test plan
- [ ] 新用户（`subscription_status=null` 或 `'expired'` + `has_used_trial=false`）打开订阅面板 → Starter 卡展示红色 ribbon + `$0 for 7 days, then $X/mo` + `Start Free Trial`
- [ ] 用过 trial 的 asleep 用户 → Starter 正价 + `Activate`，无 ribbon
- [ ] `trialing` 用户（已选 Starter 并在试用期） → Starter 显示 `Current Trial`（disabled），Pro/Ultra 显示 `Upgrade`
- [ ] `active` 订阅用户 → 卡片 CTA 正确（Current Plan / Switch / Upgrade / Downgrade），**无绿色 CURRENT PLAN 标**
- [ ] 脏数据 asleep 用户（`cancel_at_period_end=true` 但已 expired）→ UserCard 左下角只显示 `Z` 睡眠 icon，无时钟；面板顶部无"Your subscription ends on..."banner
- [ ] 年付切换 → Starter trial 态显示 "$0 for 7 days, then $20/mo"；非 trial 态显示 "$20 / month, billed yearly"
- [ ] "Save 2 months" 红色 pill 与 `/pricing` 页面 "2 months free" 视觉一致
- [ ] `pnpm lint`、`pnpm test:unit`、`tsc --noEmit` 全绿（本地已验证：164 test files / 2236 tests 通过）

## 依赖与兼容
- 后端 `createOrder` 已返回 `is_trial: boolean`，前端全程透传到 `/stripe/create-checkout-session`。用户没有试用权益时 Stripe 不会 attach `trial_period_days`，**无需后端改动**。
- 未动的接口：`useBillingCredits` hook 签名、`/credits/check` API、`SharedPlanCard`（Profile 页）、`PaywallContent`（Gift FAB）、所有 i18n keys

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `7df228e3` fix(sentry): throttle MM connection reports + global rate limit (#910)
- **作者**: peter-srp
- **时间**: 2026-04-16T12:08:11Z
- **链接**: [7df228e3](https://github.com/SerendipityOneInc/ecap-workspace/commit/7df228e3ba8c888d2ae49cc415c212cf458f6997)

**PR #910 Description:**
## Summary
- **55k events / 29 users / 6 days** from `reconnect_exhausted` — one user hit 17k+ events alone
- Root cause: parallel reconnect loops (visibility-change handler + WS onclose) race on shared `reconnectAttemptRef`, triggering multiple exhaustion events that bypass the 5-min dedup Map
- Two-layer fix: monitor-level throttle + SDK-level safety net

## Changes (2 files, +46/-18)

**mattermostMonitor.ts** — monitor-level:
- Dedup window: 5 min → 30 min
- Session cap: max 3 events per reason per page session
- `reconnect_exhausted`: `captureException` (error) → `captureMessage` (warning)
- Same dedup + cap applied to `captureMMDataIssue`

**sentry.client.config.ts** — SDK-level safety net:
- `beforeSend` global rate limit: max 5 events/minute per fingerprint
- Catches any event storm that bypasses monitor-level dedup

## Test plan
- [ ] Simulate WS disconnect → verify max 1 `reconnect_exhausted` event per 30 min
- [ ] Open multiple tabs with bad connection → verify session cap limits total to 3
- [ ] Check Sentry dashboard after deploy — volume should drop ~99%

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `e89aee0a` fix: Apple subscription check, DM policy allowFrom, and release published flag (#915)
- **作者**: kaka-srp
- **时间**: 2026-04-16T12:04:46Z
- **链接**: [e89aee0a](https://github.com/SerendipityOneInc/ecap-workspace/commit/e89aee0ac2d7b1bd2ed160868019591518843a6c)

**PR #915 Description:**
## Summary

### 1. Apple Subscription Active Check
Cron jobs (`check_subscription_sync` and `check_yearly_credits_reset`) now verify Apple subscriptions via the App Store Server API instead of relying solely on webhooks. Uses `AppleService.get_subscription_status()` with fail-open semantics. Each expiry step is independently guarded with try/except.

### 2. Channel DM Policy allowFrom
Backend enforces `allowFrom: ["*"]` when `dmPolicy` is `"open"` (required by OpenClaw docs). Covers `add_channel`, `update_channel`, and Feishu setup flows. Frontend edit modal also sends `allow_from` when switching to open DM policy.

### 3. Release Published Flag
Add `published` field to bot releases. Only published releases trigger upgrade banners for end users. Unpublished (draft) releases are visible to internal users (`@srp.one`) for testing.

## Changes
- `services/claw-interface/app/cron/subscription_cron.py` — `_check_apple_subscription()` helper with independent error guarding
- `services/claw-interface/app/routes/openclaw_settings.py` — Enforce `allowFrom: ["*"]` in add/update/feishu channel routes
- `services/claw-interface/app/database/release_repo.py` — `get_latest_release(published_only=True)`; `set_published()` method
- `services/claw-interface/app/routes/release_admin.py` — `POST /{version}/publish` and `POST /{version}/unpublish`
- `services/claw-interface/app/routes/openclaw.py` — version-check uses `published_only=True`
- `web/src/app/[locale]/admin/components/ReleasesTab.tsx` — Published/Draft badges; 发布/取消发布 buttons
- `web/src/app/[locale]/claw-settings/components/ChannelsSection.tsx` — Send `allow_from` in edit modal

## Test plan
- [x] All subscription cron unit tests pass
- [x] All release admin unit tests pass (24)
- [x] ruff, pyright, ESLint — all clean
- [x] Pre-commit hooks — all pass
- [ ] CI

Closes ECA-483, ECA-484

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `fcaf8ebf` test(web): verify billing_cycle=monthly downstream payload (follow-up to #919) (#925)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T12:01:43Z
- **链接**: [fcaf8ebf](https://github.com/SerendipityOneInc/ecap-workspace/commit/fcaf8ebf21fd6c61e86d522ab37930c752d0570e)

**PR #925 Description:**
Follow-up to #919 addressing Claude reviewer feedback.

## Feedback

Claude review on #919:

> 切换到月度后，计费切换测试仅检查 UI，未检查下游 API 负载。这呼应了第二份 Codex 审查的建议。非必需，但会填补一个小缺口。

#919 merged before I got this fix in — opening as follow-up per memory 约定.

## Change

Add 1 test in \`PaywallContent.unit.spec.tsx\`: click \`paywall-billing-monthly\`, click \`paywall-start-trial\`, assert \`createOrder\` 收到 \`billing_cycle: 'monthly'\` + \`postAPI\` 收到 \`billingCycle: 'monthly'\`.

This closes the gap between UI-level toggle verification and actual downstream call payload.

## Verification

\`\`\`bash
cd web
npx vitest run tests/unit/components/PaywallContent.unit.spec.tsx
# 14 tests pass (was 13)
\`\`\`

Refs: #894 #896 #919

## `7ebf3bbb` feat(errors): Phase 2 — migrate gift_code service to domain exceptions (#873) (#924)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T11:57:55Z
- **链接**: [7ebf3bbb](https://github.com/SerendipityOneInc/ecap-workspace/commit/7ebf3bbbf12628f16646f9f829ff66982dfed0d5)

**PR #924 Description:**
## Summary

Phase 2 of service-layer exception decoupling per [spec](../blob/main/docs/superpowers/specs/2026-04-16-service-layer-exceptions.md). Migrates all 9 raise sites in \`app/services/gift_code.py\` from \`fastapi.HTTPException\` to \`app.errors.ServiceError\` subclasses.

### Exception mapping

| Line | Code | Old status | Class |
|---|---|---|---|
| L35 | \`gift_code.generate_unique_failed\` | 500 | \`ServiceError\` |
| L57 | \`gift_code.invalid_code\` | 400 (dict) | \`DomainValidationError\` |
| L70 | \`gift_code.expired\` | 400 (dict) | \`DomainValidationError\` |
| L79 | \`gift_code.exhausted\` | 400 (dict) | \`DomainValidationError\` |
| L88 | \`gift_code.already_participated\` | 400 (dict) | \`DomainValidationError\` |
| L107 | \`gift_code.exhausted\` (CAS re-check) | 400 (dict) | \`DomainValidationError\` |
| L111 | \`gift_code.redemption_conflict\` | 409 | \`ConflictError\` |
| L136 | \`gift_code.redeem_failed\` | 500 | \`ServiceError\` |
| L170 | \`gift_code.no_subscription\` | 400 (dict) | \`DomainValidationError\` |

### Phase 0 type tweak

6 of 9 raises use \`detail={"error": "...", "message": "..."}\` dict shape — \`web/src/components/UserMenu.tsx\` reads \`detail.error == "code_exhausted"\` as the machine-readable key. Preserving that contract requires relaxing \`ServiceError.detail\` type from \`str\` → \`str | dict[str, Any]\`. JSON serialization is untouched, wire response body shape is unchanged for these call sites (still \`{"detail": {"error": "...", "message": "..."}}\`, just adds the additive \`code\` field introduced in Phase 0).

### Route / catch-clause update

\`redeem_gift_code\`'s inner try/except guards billing pre-check (\`no_subscription\`) from rollback. Changed from \`except HTTPException: raise\` to \`except ServiceError: raise\` so the migrated \`DomainValidationError\` propagates past the generic-Exception fallback (which would have wrapped it into \`gift_code.redeem_failed\` 500).

### C3 ignore_imports

Shrunk 4 → 3 entries:
- Permanent: \`asr/realtime_session\` (WebSocket)
- Legacy: \`invite_code\`, \`stripe/portal\`, \`stripe/order_confirm\` (pending Phases 3-4)

### Verification

- [x] \`pyright app/ tests/\` — 0 errors
- [x] \`ruff check\` / \`ruff format --check\` — clean
- [x] All 6 import-linter contracts KEPT
- [x] \`pytest tests/\` — **2844 passed** (unit + BDD; 8 unit + 3 BDD assertions in test_gift_code updated)
- [ ] CI green

### Depends on

PR #907 (Phase 1, merged) — baseline \`app/errors/*\`, \`tests/bdd/helpers.error_status\`, catch pattern infrastructure.

### Next

Phase 3: \`invite_code.py\` (10 raises, ~250-400 lines). Structure will mirror Phase 2 since invite_code likewise uses dict details for some raises.

Refs #873.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `68d1d8f9` test(web): InvoiceHistory + SharedPlanCard 覆盖 (#896 Part 2b) (#921)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T11:52:39Z
- **链接**: [68d1d8f9](https://github.com/SerendipityOneInc/ecap-workspace/commit/68d1d8f919a2725236349b1cc64c33c6274164ca)

**PR #921 Description:**
Part of #894 Step 2 (#896).

## 新增

| 文件 | tests |
|---|---|
| \`tests/unit/components/billing/InvoiceHistory.unit.spec.tsx\` | 12 |
| \`tests/unit/components/billing/SharedPlanCard.unit.spec.tsx\` | 16 |

## InvoiceHistory 覆盖要点

- \`loadOrders\` 3 条分支：成功渲染订单表、无 userInfo.uid 跳过、error 静默吞下
- \`openCustomerPortal\` 5 条分支：
  - portalLoading gate（重复点击防重）
  - 无 uid → \"Please log in to access billing.\" toast
  - url 返回 → window.open(url, '_blank', 'noopener,noreferrer')
  - \"no Stripe customer\" error → 特定 toast \"Subscribe first\"
  - 其他 error / throw → generic \"Failed to open billing portal\" toast
- 订单渲染：formatDate、formatAmount、credits_amount 缺失 → em-dash、
  admin_grant/daily_bonus → \"Free\" 标签
- Support ticket 链接 → openSupportTicket('billing')

## SharedPlanCard 覆盖要点

- **StatusLine** 5 种状态：
  - active + cancelAtPeriodEnd → \"ending\" + Renew button (shows \"Coming soon!\" toast)
  - active + pendingDowngrade → \"downgradingTo {plan}\" (interpolation 验证)
  - active 正常 → \"renews\"
  - trial + trialEndTime → \"trialEnds {date}\"
  - trial 无 trialEndTime → \"trialEndsIn {days}\"
  - asleep → \"subscriptionEnded\"
- **ActionButtons** 3 种：
  - active/trialing → Manage + AddCredits
  - trial → Subscribe
  - asleep → Activate
- **Upgrade icon** 隐藏 for active + ultra plan（无可升级目标）
- Loading dots 三个 animate-bounce span
- **Credits wallet 分摊计算**：subscription 先扣完再扣 topup（验证 1200 used = 1000 sub + 200 topup）
- \`-\` 显示当无 capacity + 无 remaining

## Bug-hunting 过程

测试完整执行发现 1 个潜在改进点（非生产 bug，记录给未来）：
- \`SharedPlanCard.StatusLine\` 的 \"ending\" 分支里 Renew 按钮只 \"Coming soon!\"
  toast —— 生产应接续费路径，#894 后可评估

未发现生产代码 bug。

## 验证

\`\`\`bash
cd web
npx vitest run tests/unit/components/billing/  # 28 tests pass
pnpm test:unit                                  # 173 files / 2,382 tests pass
npx tsc --noEmit && pnpm lint                   # clean
\`\`\`

Refs: #894 #896

## `fed6ab16` test(web): PaywallContent + vitest postcss bypass (#896 Part 2a) (#919)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T11:51:15Z
- **链接**: [fed6ab16](https://github.com/SerendipityOneInc/ecap-workspace/commit/fed6ab16e2fc218f8f1a356cdd38f6a5f501a05d)

**PR #919 Description:**
Part of #894 Step 2 (#896).

## 新增

\`tests/unit/components/PaywallContent.unit.spec.tsx\` — 13 tests 覆盖 PaywallContent (100% 行):

- Billing cycle toggle：默认 yearly、点击 Monthly 切换、\"billed yearly\" 后缀
- \`handleStartTrial\` 完整错误分支：
  - 未登录 → \"Please log in\"
  - \`createOrder\` fails（带 error 消息 / 缺 error 消息）
  - \`postAPI\` 返回 success=true 但无 url → \"No checkout URL returned\"
  - \`postAPI\` success=false → 透传 error
  - \`postAPI\` rejects → 透传 Error.message
- 成功路径：\`window.open\` with \`noopener,noreferrer\` + \`onClose\`
- userEmail 有/无时 request body 差异
- \"Compare all plans\" → \`openPanel\`
- Loading state（\"Setting up...\"）

## vitest config 改动

\`vitest.config.mts\` 新增 \`css: { postcss: { plugins: [] } }\`：

项目根 \`postcss.config.mjs\` 用 string-form plugin \`'@tailwindcss/postcss'\`，
vite 7 不接受 string-form PostCSS plugins，测试加载 CSS-importing 组件时会
崩溃：\"Invalid PostCSS Plugin found at: plugins[0]\"。测试不需要 tailwind
处理（只要 import 不失败即可），空 plugins 数组绕开。

这是**测试专用** config，与生产 build 使用的 postcss.config.mjs 无关。
后续如有其他 CSS-importing 组件要测（LoginForm 等），都能受益。

## 验证

\`\`\`bash
cd web
npx vitest run tests/unit/components/PaywallContent.unit.spec.tsx  # 13 tests pass
npx vitest run                                                      # 172 files / 2,368 tests pass
npx tsc --noEmit                                                    # clean
pnpm lint                                                           # clean
\`\`\`

## Bug-hunting 过程

测试完整执行 \`handleStartTrial\` 所有错误分支，未发现生产代码 bug。
安全检查：\`window.open\` 正确传 \`noopener,noreferrer\` 防 tabnabbing。

Refs: #894 #896

## `87db3f0f` fix(web): typewriter cleanup flushes stale useMemo cache (#923)
- **作者**: sam-srp
- **时间**: 2026-04-16T11:37:30Z
- **链接**: [87db3f0f](https://github.com/SerendipityOneInc/ecap-workspace/commit/87db3f0f1dc4011f729f2d61e032e8b9ad392837)

**PR #923 Description:**
## Summary
- Bot 消息的打字机动画 cleanup 时机与 `recentBotMessageIds` 过期存在竞态：`removeDelay`(5ms/字符) 先于打字机动画(5.33ms/字符)结束，cleanup 杀掉 tick 并删除 `streamingContents` ref，但 `useMemo` 的 state 依赖均未变化，导致缓存的部分文本永远不刷新
- 修复：cleanup 删除 ref 后 bump `streamingTick`，让 `useMemo` 重新计算并 fallback 到完整的 `m.content`

## Test plan
- [ ] 找一个会一次性发送长消息（500+ 字符）的 bot（如 Vibe Drama），观察消息是否完整渲染，不再卡在部分文本
- [ ] 短消息仍有打字机动画效果
- [ ] `post_edited` 流式消息不受影响（streamingEditIds 路径不走打字机）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `104c88cd` feat(errors): Phase 1 — migrate openclaw + leaf utility services to domain exceptions (#873) (#907)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T11:30:52Z
- **链接**: [104c88cd](https://github.com/SerendipityOneInc/ecap-workspace/commit/104c88cdf515e0482a3d0649f01767014b96f7bd)

**PR #907 Description:**
## Summary

Phase 1 of the service-layer exception decoupling migration per [spec](../blob/main/docs/superpowers/specs/2026-04-16-service-layer-exceptions.md). Migrates 17 raise sites across 6 service modules from \`fastapi.HTTPException\` to \`app.errors.ServiceError\` subclasses, preserving outbound HTTP status codes.

### Services migrated

| Module | Raises | Exception class |
|---|---|---|
| \`openclaw/bot_token.py\` | 2 | \`NotFoundError\`, \`DomainValidationError\` |
| \`openclaw/rate_limit.py\` | 1 | \`RateLimitError\` |
| \`openclaw/agent_response.py\` | 4 | \`DomainValidationError\`, \`ConflictError\` |
| \`openclaw/agent_runtime.py\` | 5 | \`DomainValidationError\`, \`ExternalServiceError\` |
| \`openclaw/bot_lifecycle.py\` | 4 | \`NotFoundError\`, \`DomainValidationError\`, \`ConflictError\` |
| \`code_utils.py\` | 1 | \`DomainValidationError\` |

### Dynamic status-code preservation

\`agent_runtime.runtime_exec_checked\` accepts \`default_error_status\` and \`workspace_missing_status\` parameters from callers. These are preserved by passing through \`ExternalServiceError(context={"upstream_status": N})\` — caller-visible status codes are unchanged while the service stays transport-agnostic.

### Route callers updated

6 route files had the \`except HTTPException: raise\` + \`except Exception: <convert-to-500>\` pattern that would silently wrap ServiceError into 500 after migration. All changed to \`except (HTTPException, ServiceError): raise\` so domain errors bubble to the central handler:

- \`openclaw.py\` (7 blocks)
- \`openclaw_agents.py\` (7 blocks, includes \`as e\` logging pattern)
- \`openclaw_runtime.py\` (4 blocks)
- \`openclaw_settings.py\` (6 blocks)
- \`session/archived.py\` (2 blocks)
- \`clawhub.py\` (3 blocks)

### C3 contract shrunk

\`ignore_imports\` shrunk from 11 entries to 5:
- 1 permanent (WebSocket transport in \`asr/realtime_session\`)
- 4 legacy pending Phase 2-4 (\`gift_code\`, \`invite_code\`, \`stripe/portal\`, \`stripe/order_confirm\`)

### Naming convention

All \`code\` fields follow \`<module>.<reason>\` format per spec decision:
\`openclaw.user_not_found\`, \`openclaw.bot_not_initialized\`, \`openclaw.bot_not_running\`, \`openclaw.agent_id_required\`, \`openclaw.agent_runtime.exec_failed\`, etc.

## Behavior preservation

HTTP status codes unchanged for all migrated endpoints. Central handler from Phase 0 (#889) maps each subclass to its original status. \`ExternalServiceError.upstream_status\` override covers dynamic status cases.

## Test plan

- [x] \`pyright app/ tests/\` — 0 errors
- [x] \`ruff check\` / \`ruff format --check\` — clean
- [x] All 6 ci-lint guards pass including new C3 contract and repo-sync
- [x] \`pytest tests/unit/\` — **2401 tests pass**
- [ ] CI \`python-code-quality / build-and-test\` green

## Depends on

PR #889 (Phase 0, merged) — provides \`app.errors.*\` and central handler.

## Next

Phase 2: migrate \`gift_code.py\` (8 raises, ~200-300 lines).

Refs #873.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `3c99c7a7` test(web): reset mocks per test in DowngradeConfirmModal (follow-up to #916) (#917)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T11:24:15Z
- **链接**: [3c99c7a7](https://github.com/SerendipityOneInc/ecap-workspace/commit/3c99c7a7a9e35eb81ffad4da61cdf82adbc21354)

**PR #917 Description:**
Follow-up to #916 addressing Claude reviewer feedback.

## Feedback

Claude PR review on #916:

> The shared \`baseProps.onClose = vi.fn()\` and \`onConfirm = vi.fn()\` at module scope are never reset between tests (no \`vi.clearAllMocks()\` in \`beforeEach\`). In practice this is fine because every test that makes an assertion creates its own local mock — but adding a \`beforeEach(() => { vi.clearAllMocks() })\` or resetting \`baseProps\` mocks would make the suite more robust against future test additions.

#916 被 merge 时这个 fix 还没来得及进，现补。

## Change

- 把 \`baseProps\` 从 module-scope 改成 \`makeBaseProps()\` factory
- 加 \`beforeEach\` with \`vi.clearAllMocks()\` + 重建 baseProps

这样每个 test 拿到的 \`onClose\` / \`onConfirm\` 都是 fresh，不会因为未来新加的断言被上一个 test 的 call history 污染。

## Verification

\`\`\`
cd web
npx vitest run tests/unit/components/billing/DowngradeConfirmModal.unit.spec.tsx
# 12 tests pass
\`\`\`

Refs: #894 #896 #916

## `ef2ce17d` Revert "feat(web): Seedance 2.0 上新弹窗 — 自动雇佣 Vibe Drama 并进入聊天" (#918)
- **作者**: bryce-srp
- **时间**: 2026-04-16T10:53:43Z
- **链接**: [ef2ce17d](https://github.com/SerendipityOneInc/ecap-workspace/commit/ef2ce17d6ed05e2fecd261643fbe55bf05c3f8e2)

**PR #918 Description:**
Reverts SerendipityOneInc/ecap-workspace#866

## `2caf084c` test(web): billing + credits 核心单测 (#896 Part 1) (#916)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T10:47:42Z
- **链接**: [2caf084c](https://github.com/SerendipityOneInc/ecap-workspace/commit/2caf084c9ea1ea12714213c08eebea7a61e02fc1)

**PR #916 Description:**
Part of #894 Step 2 (#896) — 付费 / 订阅核心覆盖

## 新增 4 个测试文件 / 59 tests

| 文件 | tests | 源文件覆盖率 |
|---|---|---|
| \`stripe-customer-portal.unit.spec.ts\` | 11 | 100% (33/33) |
| \`stripe-create-checkout-session.unit.spec.ts\` | 21 | 100% (53/53) |
| \`DowngradeConfirmModal.unit.spec.tsx\` | 12 | 100% (25/25) |
| \`CreditsDisplay.unit.spec.tsx\` | 15 | 93.61% (44/47) |

## 覆盖的关键业务分支

**customer-portal route** (POST + DELETE):
- 验证：missing uid / missing return_url → 400
- 后端 error JSON / 不可解析 JSON / fetch throw
- 正常 return portal URL / cancel subscription with period info

**create-checkout-session route**:
- 7 个 400 验证分支（userId/orderId/productType/creditsAmount/billingCycle/stripeProductId/topup matching）
- **Subscription v2**：yearly interval、7-day trial **仅** starter + isNewSubscriber（pro / existing 不给 trial）、success_url 构造（locale prefix、orderId、plan params、custom successUrlPath）、customer_email 透传、origin fallback
- **Topup**：按 unit_amount 匹配 price
- **Legacy credits**：getOrCreatePriceId、invoice_creation、metadata.creditsAmount
- stripe.checkout.sessions.create throws → 500

**DowngradeConfirmModal**:
- isOpen=false → null
- 丢失功能计算（credits 减少 + plan features 差集）
- date formatting + null fallback
- backdrop click 关闭 / 内容 stopPropagation / Esc 关闭（仅 open 时监听）
- confirm loading state

**CreditsDisplay**:
- Plan badge 5 分支（trial/expired/active+plan/user_type=1/free）
- Trial countdown + Asleep notice
- Loading skeleton
- billing_initialized=false → 数字显示 \`-\`
- Usage percentage 计算 + 100% 上限
- Wallet breakdown 条件渲染
- showHeader/showCard 切换

## Coverage 影响

- 基线（#911 merged）：46.77% (7,558/16,157)
- 本 PR 后：**47.73% (7,713/16,157) +0.96pp**

## Bug-hunting 过程

按 #894 要求测试过程同步寻找 bug —— 目前未发现生产代码 bug，两个 API route
验证逻辑完备，modal / display 组件行为符合预期。测试过程中若后续发现 bug
会另起 \`bug(web): ...\` issue。

Refs: #894 #896

## `c04888ba` chore(web): drop redundant LandingClient.tsx entry (follow-up to #911) (#913)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T10:31:02Z
- **链接**: [c04888ba](https://github.com/SerendipityOneInc/ecap-workspace/commit/c04888ba5e2b571243845027ef166268a5afe98b)

**PR #913 Description:**
Follow-up to #911.

## 问题

#911 具名排除列表里加了 `src/app/landing/LandingClient.tsx`，但下方仍保留 `src/app/landing/**`（更大的 glob 已经包含该文件）。Claude auto-reviewer 指出这是冗余：

> This causes no harm and could serve as documentation, but it's worth noting in case the `src/app/landing/**` glob is ever removed

合并前没来得及 fix。本 PR 单独清理。

## 改动

删除显式 `LandingClient.tsx` 行，改为 inline comment 标注"已被 `src/app/landing/**` 覆盖"——保留"landing 走 E2E"的文档意图，不留死条目。

## 本地验证

\`\`\`
cd web && pnpm test:unit:coverage
\`\`\`

基线不变：46.77% (7,558/16,157)；`LandingClient.tsx` 仍被正确排除（由 `src/app/landing/**` 匹配）。

Refs: #894 #895 #911

## `deb2c236` chore(web): 修正 vitest coverage scope — Client.tsx 分母纠正 (#895) (#911)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T10:14:30Z
- **链接**: [deb2c236](https://github.com/SerendipityOneInc/ecap-workspace/commit/deb2c2360d12f4b55f291594cfd6323572c30108)

**PR #911 Description:**
Closes #895
Part of #894 (Step 1 / 11) — web 覆盖率 47% → 80% roadmap

## 问题

`web/vitest.config.mts` 用 `src/app/**/*Client.tsx` 整类排除 Client 页面，与团队实际意图背离：

- 22 个 `*Client.tsx` 审计后有 **13 个含真业务逻辑**
- `AdminClient` / `AgentsManagerClient` / `CronClient` **已有单测**（`tests/unit/app/...`），却被 coverage 忽略
- `GenClawClient` (1518 LoC / 365 executable lines) / `PublishAgentsClient` / `SkillsSearchClient` / `SkillDetailClient` 等关键业务 Client 从未进入覆盖统计

同时 `canvas/**` 与 `components/AgentChatClient/**` 是 legacy / parked 模块（见 #894），也应整块排除走 E2E。

## 改动（0 测试代码改动，纯配置）

`web/vitest.config.mts` 的 `coverage.exclude`：

**删**：
- `'src/app/**/*Client.tsx'`（整类通配）
- `'src/app/**/canvas/nodes/**'`（被下面更大的排除覆盖）

**加 — 具名排除 10 个 PURE_UI / branded / static Client.tsx**：
- `AboutClient` / `PrivacyClient` / `TermsClient`（两处） / `SubscriptionClient` / `ProfilePageClient` / `MiniChatClient` / `UserGuideClient` / `LandingClient` / `PublicPricingClient`（branded，~700 LoC 内嵌 CSS）

**加 — 整块排除 legacy 模块**：
- `'src/app/**/canvas/**'`
- `'src/components/AgentChatClient/**'`

Threshold 保持 35，待 #905 在最后一个测试 PR 抬到 80。

## 本地验证

\`\`\`
cd web && pnpm test:unit:coverage
\`\`\`

**Before** (旧配置): 47.40% 行 / 16,600 total / 7,870 covered
**After** (本 PR): **46.77% 行 / 16,157 total / 7,558 covered**

**HAS_LOGIC Client.tsx 全部进入覆盖统计（验证通过）**：
- ✓ AdminClient.tsx (65%) / AgentsManagerClient.tsx (55.71%) / CronClient.tsx (90.36%)
- ✓ GenClawClient.tsx (0% / 365 executable lines)
- ✓ PublishAgentsClient.tsx (76.36%) — 意外之喜，已有间接覆盖
- ✓ SuccessClient.tsx (0%) / OnboardingSuccessClient.tsx (0%)

**被排除的路径全部消失（验证通过）**：canvas/** / AgentChatClient/** / 10 个 PURE_UI Client.tsx

数字从 47.40% 掉到 46.77% 是**真实风险面暴露**，不是退步：之前的 16,600 行分母没把 HAS_LOGIC Client 算进来。新分母 16,157（含 ~1,100 行 HAS_LOGIC Client，去掉 ~1,500 行 legacy canvas + AgentChatClient）反映了真实测试 surface。

## 注意

- 本 PR 不改任何测试代码
- 后续 #896-#905 会按业务域滚动补测试至 80%

## `cd3e58cc` chore(lint): widen pnpm lint to src/ + tests/ (4/4) (#909)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T10:02:44Z
- **链接**: [cd3e58cc](https://github.com/SerendipityOneInc/ecap-workspace/commit/cd3e58ccf5c1bca09ed61941449eaa4bd0a3a5c1)

**PR #909 Description:**
## Summary

Final step of the `web/tests/` lint-scope series. Follows #890, #892, #906 (all merged).

- `pnpm lint`: `eslint src/ --quiet` → `eslint src/ tests/ --quiet`
- Removed the now-redundant `pnpm lint:tests` script (it was a bridge during PR1–PR3; `pnpm lint` subsumes it).
- Updated `web/CLAUDE.md` testing note to reflect that the jest-dom import ban, prettier formatting, and import-sort are now all enforced in CI for `tests/`.

## Why

`web/CLAUDE.md:21` historically admitted:

> "ESLint enforces this under `src/`; `tests/` is outside `pnpm lint`'s scope so the rule is advisory there."

The earlier PRs in this series closed that gap from the config side (tests/ override in #890, prettier+import-sort autofix in #892, error cleanup in #906). This PR flips the enforcement switch: CI's `code-quality / web-quality` job calls `pnpm lint`, so from this commit on, any regression (jest-dom import, prettier format drift, import-sort break, stray `console.log` at the wrong layer, etc.) fails CI on web PRs.

This satisfies codex-review's continuous-enforcement suggestion on #890.

## Verification

- `cd web && pnpm lint` → exit 0
- 346 `no-explicit-any` warnings remain hidden by `--quiet` (they're deferred cleanup, not blocking — see #906 description)

## Test plan

- [x] `cd web && pnpm lint` → exit 0 with combined `src/ tests/` scope
- [x] No more `lint:tests` script (removed)
- [x] `web/CLAUDE.md` updated to final state
- [ ] CI `code-quality / web-quality` green
- [ ] Sanity regression check: introduce a deliberate jest-dom import in a test file, confirm CI fails, then revert (optional, post-merge)

## Follow-up (not blocking this PR)

- Clean up the 346 `no-explicit-any` warnings across test mocks/fixtures — best done in focused per-subsystem PRs.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `6fa23b55` fix(claw-interface): pin stripe<15 to restore .get() on Session/Subsc… (#908)
- **作者**: tim-srp
- **时间**: 2026-04-16T10:01:59Z
- **链接**: [6fa23b55](https://github.com/SerendipityOneInc/ecap-workspace/commit/6fa23b5525817624d35bf01cd0f2c88b336be0a4)

**PR #908 Description:**
…ription

Stripe Python SDK 15.0.0 (2026-03-25, PR stripe/stripe-python#1762) removed StripeObject's dict inheritance, so StripeObject.get(...) and .items()/.keys() raise AttributeError at runtime. Because requirements.txt did not pin a version, recent rebuilds pulled 15.0.1 and started crashing /stripe/order_confirm with 'Failed to confirm order: get', blocking the post-payment success page for live users.

Pin to >=14,<15 as an immediate revert. Full migration to getattr(obj, 'k', None) / obj.to_dict() across the Stripe handlers and order_confirm will follow in a separate PR before we upgrade back.

## `97a8d2a7` chore(lint): fix 2 errors + 46 warnings in tests/ (3/4) (#906)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T09:49:30Z
- **链接**: [97a8d2a7](https://github.com/SerendipityOneInc/ecap-workspace/commit/97a8d2a708caa8133870042b88df2f77f9cb327e)

**PR #906 Description:**
## Summary

Step 3 of 4 toward enforcing lint on `web/tests/`. Follow-up to #890 (merged) and #892 (merged).

Close the remaining lint gap so `pnpm lint:tests` exits 0 (with 346 `no-explicit-any` warnings deliberately left for a later cleanup pass — they're in test mocks/fixtures and orthogonal to the lint-scope work).

## Errors fixed (2)

- **`tests/e2e/fixtures/base.ts:86` — `react-hooks/rules-of-hooks` false positive.** Playwright's fixture `use()` callback (hand off value to test) shadows React's `use()` hook name; `eslint-plugin-react-hooks` has no way to distinguish. Added `eslint-disable-next-line` with reason.
- **`tests/e2e/fixtures/shared-session.ts:17` — `no-empty-object-type`.** Playwright's `base.extend<TestArgs, WorkerArgs>` canonically uses `{}` for "no test-scoped fixtures" — `Record<string, never>` breaks type inference (narrows default args like `browser` to `never`). Added a scoped `eslint-disable-next-line @typescript-eslint/no-empty-object-type` with explanation.

## Warnings cleaned (46)

Following reviewer guidance on #890 (use `--max-warnings 0` for enforcement, not `--quiet`):

- **43 `no-unused-vars`**: deleted unused imports where the identifier was never referenced; prefixed `_` on locals assigned for side effects or tests that exercise a call without asserting on the result.
- **2 `no-unused-expressions`**: `ripple.offsetHeight` DOM-reflow trigger in base.ts / shared-session.ts — annotated with `eslint-disable-next-line` and reason.
- **1 `no-img-element`**: `<img>` inside a Vitest mock of `ProgressiveImage` — annotated with `eslint-disable-next-line` (the mock's whole purpose is to render a plain `<img>` stub).

**Bonus test-quality improvement**: in `client.unit.spec.ts`, added `expect(caught).toBeInstanceOf(ApiError)` before the `as` cast — validates the assumption rather than proceeding silently on a wrong type. This also gives `ApiError` a runtime reference so it's not flagged by `no-unused-vars`.

## Left as warnings (deferred)

- **346 `no-explicit-any`** across mock / fixture types. The `tests/**` override keeps these at `warn` so they surface during local dev without gating CI. Cleanup is a separate concern, best done in focused follow-up PRs per subsystem.

## Verification

- `cd web && pnpm exec eslint tests/ --max-warnings 0` → **346 warnings (all `no-explicit-any`), 0 errors**
- `cd web && ./node_modules/.bin/tsc --noEmit` → **clean**
- `cd web && pnpm test:unit` → **164 files, 2233 tests passed** (1 todo)
- `cd web && pnpm lint` (src/) → unchanged

## Follow-up

**PR4** widens `pnpm lint` CLI to `src/ tests/` so CI enforces prettier, import-sort, and the jest-dom import ban on tests/ (satisfies codex-review's suggestion on #890 about continuous enforcement).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `574e61c9` refactor(chat): replace ToolStepsBar with ToolGroup, simplify tool status pipeline (#876)
- **作者**: peter-srp
- **时间**: 2026-04-16T09:41:57Z
- **链接**: [574e61c9](https://github.com/SerendipityOneInc/ecap-workspace/commit/574e61c947cde6803c6479a082e44e022da92f96)

**PR #876 Description:**
## Summary
- **ToolGroup**: Replace ToolStepsBar with aggregated ToolGroup component — collapsible card with contextual action previews per tool, auto-expand while streaming
- **Parser**: Simplify toolStatusParser — remove phase state machine, pure walk, explicit field construction, warn on missing fields
- **Dedup**: Filter artifacts already rendered inline in markdown body (prevents duplicate PDF cards)
- **Observability**: Report `file_info_backfill_failed` via Sentry (was silently swallowed)
- **Cleanup**: Delete ToolStepsBar, toolActivityUtils, dead ack prop chain
- **Tests**: 6 new/extended spec files (95 tests covering ToolGroup, aggregator, parser, dedup, reactions, streaming)

## Details
Pipeline: `processToolStatusMessages` → `aggregateToolMessages` → `ToolGroup`

**22 files changed** (+1735/-636) — clean squash, no merge noise.

## Test plan
- [ ] ToolGroup renders collapsed "N tools used", expands on click
- [ ] Tool rows show contextual action previews
- [ ] Groups auto-collapse when streaming stops
- [ ] PDF attachments don't appear twice
- [ ] `pnpm tsc --noEmit` clean
- [ ] `pnpm lint` passes
- [ ] 95 unit tests pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `233d91b0` feat: require active subscription before granting credits (#884)
- **作者**: bryce-srp
- **时间**: 2026-04-16T09:30:40Z
- **链接**: [233d91b0](https://github.com/SerendipityOneInc/ecap-workspace/commit/233d91b039e13a65df830c6b2f7dc450327d2344)

**PR #884 Description:**
Admin boost, admin grant, and gift code redeem now pre-check whether the user has an active Lago subscription via billing_client.check_credits(). If billing-gateway returns 400 "no active subscription", the operation is rejected with a clear error instead of silently granting credits that can never be consumed (billing events require an active subscription).

Changes:
- admin_boost: return failed BoostResultItem with reason
- orders: _admin_grant_via_billing_gateway returns False on no subscription
- gift_code: raise HTTPException 400 with error code "no_subscription"
- UserMenu.tsx: handle "no_subscription" error code in redeem flow
- en.ts/zh.ts: add errorNoSubscription translation

## `866bb535` feat(claw-interface): Add Apple subscription status query method (#893)
- **作者**: bill-srp
- **时间**: 2026-04-16T09:17:18Z
- **链接**: [866bb535](https://github.com/SerendipityOneInc/ecap-workspace/commit/866bb5358602f45e6488900b13b3abae8a066ecd)

**PR #893 Description:**
## Summary

- Add `get_subscription_status(original_transaction_id)` to `AppleService` that calls Apple's `get_all_subscription_statuses` API and returns a simplified `AppleSubscriptionStatus` frozen dataclass
- New `app/schemas/apple.py` with `AppleSubscriptionStatus` (fields: `original_transaction_id`, `product_id`, `status`, `expiry_date`, `is_active`) and status mapping from Apple's numeric codes
- Picks the transaction with the latest `expiresDate` across all subscription groups
- Remove unused `_get_app_apple_id` helper (logic already inlined in `_make_verifier`)

## Test plan

- [x] Unit tests for schema immutability and status mapping (8 tests)
- [x] Unit tests for `get_subscription_status`: active, expired, empty groups, unknown status, API error, multiple groups (7 tests)
- [x] Existing `test_apple_service.py` tests pass with no regressions
- [ ] CI lint and type checks pass

## `9735f196` chore(lint): prettier + import-sort autofix for tests/ (2/4) (#892)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T09:00:15Z
- **链接**: [9735f196](https://github.com/SerendipityOneInc/ecap-workspace/commit/9735f196d5b2bfedac762aca981f1b002f2652cf)

**PR #892 Description:**
## Summary

Step 2 of 4 toward enforcing lint on `web/tests/`. Follow-up to #890 (merged).

Pure `pnpm lint:tests --fix` output — **no logic changes, no production code touched**. 100% of the diff is under `web/tests/`.

> This supersedes the closed PR #891 (which was opened stacked on #890 and couldn't retrigger CI cleanly after the base retarget). Same branch content, rebased on current main.

### Numbers

- `pnpm lint:tests` errors: **1406 → 2** (-99.86%)
  - prettier/prettier: 1267 fixed
  - simple-import-sort/imports: 136 fixed
  - simple-import-sort/exports: 1 fixed
- `pnpm test:unit`: **2232 passed, 1 todo** (unchanged)
- 165 files changed, +2212 / -2775 (net -563 lines from import-sort wrap/collapse)

### Remaining 2 errors (PR3 will fix)

- `tests/e2e/fixtures/base.ts:86` — `react-hooks/rules-of-hooks` false positive (Playwright's `use()` fixture consumer shadows React's `use()`)
- `tests/e2e/fixtures/shared-session.ts:18` — `no-empty-object-type` (`{}` needs tightening)

### Review guidance

Diff is large by line count but **uniform in kind**: quotes, semicolons, wrap/unwrap, import ordering. Spot-check a few files if you want; no intent-level changes to evaluate.

Pushed with `SKIP_PR_SIZE_CHECK=1` (knowingly large mechanical autofix — the scenario this escape hatch exists for).

## Follow-up

- **PR3**: Hand-fix the 2 remaining errors + surface/clean warnings (reviewer note on #890: use `--max-warnings 0` instead of `--quiet` to see them)
- **PR4**: Merge `tests/` into `pnpm lint` with CI gate (reviewer note on #890: satisfies the "continuous enforcement" suggestion)

## Test plan

- [x] `cd web && pnpm lint:tests` → 2 errors (down from 1406)
- [x] `cd web && pnpm lint` → 0 errors (src/ unchanged)
- [x] `cd web && pnpm test:unit` → 2232 passed
- [ ] CI `code-quality / web-quality` green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `1898b4c9` feat(errors): Phase 0 — domain-exception layer + C3 contract (#873) (#889)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T08:59:06Z
- **链接**: [1898b4c9](https://github.com/SerendipityOneInc/ecap-workspace/commit/1898b4c9f33aa523de0a02a95583f8ca42c0050b)

**PR #889 Description:**
## Summary

Phase 0 of the service-layer exception decoupling migration per [spec](../blob/main/docs/superpowers/specs/2026-04-16-service-layer-exceptions.md) (PR #882). **Draft** until #882 merges so spec design decisions are locked in.

### Added

- **`app/errors/__init__.py`** — `ServiceError` base + 6 subclasses (NotFoundError 404, ValidationError 400, ConflictError 409, UnauthorizedError 401/403, RateLimitError 429, ExternalServiceError 502). Kwarg-only construction; `context` dict stays server-side. `ExternalServiceError` forwards `context["upstream_status"]`; `UnauthorizedError` maps to 403 when `context["forbidden"]` set.
- **`app/errors/handlers.py`** — Central FastAPI handler; JSON body is `{code, detail}` only.
- **`tests/unit/test_errors.py`** — 22 tests covering each class's default/override semantics + handler integration via `TestClient`.
- **`pyproject.toml`** — New import-linter **C3** contract `app.services must not depend on FastAPI (transport-agnostic)` with `allow_indirect_imports = true` (matching C1 pattern). Two-class `ignore_imports`:
  1. **Permanent**: `asr.realtime_session -> fastapi` (WebSocket — inherent transport; **11th file** discovered during Phase 0 implementation, not in original spec's list of 10 but legitimate and documented)
  2. **Legacy**: 10 modules pending Phase 1-4 migration

### Modified

- **`app/create_app.py`** — Register `ServiceError` handler **before** `favie_common.middleware.exception_handler.register_exception_handlers` so domain errors hit the new handler first.

## Non-changes (additive PR)

- No existing service code modified. No HTTPException removals yet.
- All 10 legacy modules still in C3 `ignore_imports` — migration happens in Phase 1-4 PRs, each shrinking the list.
- `02-import-linter.sh` not modified (already installed by #871; picks up C3 automatically).

## Verification

- [x] `pyright app/ tests/` — 0 errors
- [x] `ruff check . && ruff format --check .` — clean
- [x] `pytest tests/unit/test_errors.py` — 22/22 pass
- [x] `bash scripts/ci-lint/02-import-linter.sh` — **6 contracts KEPT, 0 broken**
- [x] All other `scripts/ci-lint/*.sh` guards — pass (no new warnings)
- [x] `pytest tests/unit/test_admin_route_wiring.py tests/unit/test_app_logging.py` — no regression from `create_app.py` change

## Depends on

- PR #882 (spec) — merge first to lock design decisions. This PR is **draft** until #882 is merged.

## Next

After this merges: Phase 1 — migrate openclaw 子域 + leaf utilities (17 raises, ~400–600 lines).

Refs #873.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `4bee6471` feat(web): Seedance 2.0 上新弹窗 — 自动雇佣 Vibe Drama 并进入聊天 (#866)
- **作者**: lynn Zhuang
- **时间**: 2026-04-16T08:55:12Z
- **链接**: [4bee6471](https://github.com/SerendipityOneInc/ecap-workspace/commit/4bee64710a11e4f3d220c751bf4c43c3e4a923f6)

**PR #866 Description:**
## 概要
  - 用户登录后进入 chat 页面，等待 5 秒页面渲染完成后，首次展示 Seedance 2.0
  上新弹窗（每用户仅一次）
  - 弹窗上方为 16:9 宣传视频，自动播放循环；用户暂停后显示播放按钮可恢复
  - 点击「立即体验」自动雇佣 Vibe Drama
  agent，整页跳转到其聊天窗口（确保侧边栏完整加载）
  - 与 Guide Tour 弹窗互斥：若 Guide Tour 未看过，Seedance
  弹窗延迟到下次登录再出现

  ## 改动文件
  | 文件 | 说明 |
  |------|------|
  | `web/src/components/SeedanceLaunchModal.tsx` | 新增弹窗组件（视频自动播放
  + 雇佣 + 整页跳转） |
  | `web/src/app/[locale]/chat/GenClawClient.tsx` | 在 chat 页面挂载弹窗 |
  | `web/src/lib/auth/types.ts` | 新增 `SEEDANCE_LAUNCH_SEEN` localStorage 键
  |
  | `web/src/locales/en.ts` | 英文文案 |
  | `web/src/locales/zh.ts` | 中文文案 |

  ## 测试计划
  - [ ] 登录 → 进入 chat → 页面加载完成约 5
  秒后弹窗出现，视频自动播放（前提：Guide Tour 已看过）
  - [ ] 关闭弹窗 → 刷新 → 不再出现
  - [ ] 点击「立即体验」→ Vibe Drama 被雇佣 → 整页跳转到该 agent
  聊天，侧边栏显示该 agent
  - [ ] 暂停视频 → 出现播放按钮 → 点击恢复播放
  - [ ] 新用户未看过 Guide Tour → Seedance 弹窗不出现 → Guide Tour 先弹
  - [ ] Guide Tour 关闭后 → 下次进 chat → Seedance 弹窗出现
  - [ ] 官网首页及其他公共页面不弹出

<img width="2428" height="1772" alt="image" src="https://github.com/user-attachments/assets/818034aa-d3e7-4f62-9aad-6f97e85022dc" />

## `62338cda` chore(lint): add tests/ override + lint:tests script (1/4) (#890)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T08:46:42Z
- **链接**: [62338cda](https://github.com/SerendipityOneInc/ecap-workspace/commit/62338cda895d1d4e0a254b05e093edaf34f0a854)

**PR #890 Description:**
## Summary

Step 1 of 4 toward bringing `web/tests/` (211 files, ~1768 ESLint errors) under `pnpm lint`'s enforced scope. See plan: `/home/node/.claude/plans/sleepy-soaring-treasure.md`.

- Add opt-in `pnpm lint:tests` script (`eslint tests/ --quiet`)
- Add minimal `tests/**` override in `web/eslint.config.mjs` that relaxes three globally-applied rules hostile to test code:
  - `@typescript-eslint/no-explicit-any` → `warn` (mocks / fixtures; 346 occurrences)
  - `no-console` → `off` (e2e scripts, CI visibility; 16 occurrences)
  - `@typescript-eslint/no-unused-vars` → `warn` with `_` prefix exemptions (matches src/)
- Update `web/CLAUDE.md` testing note to reflect the new checker

**Why the override stays tiny**: the existing `eslint.config.mjs` uses `files: ['src/**/*.{ts,tsx}']` on all complexity / naming / color / `forbid-dom-props` overrides, so those rules already don't apply to `tests/`. We only relax what's declared globally (`eslint:recommended`, `next/typescript`, top-level `no-console`).

**CI impact**: **zero**. `pnpm lint` still runs `eslint src/` — unchanged. `lint:tests` is opt-in this PR; it will be merged into `pnpm lint` in PR4 once autofix (PR2) and manual cleanup (PR3) land.

**Current state after this PR**:
- `pnpm lint` → 0 errors (no change)
- `pnpm lint:tests` → 1406 errors (1404 autofix-able, 2 manual: `rules-of-hooks`, `no-empty-object-type`)

## Follow-up PRs

- **PR2**: `pnpm lint:tests --fix` mass commit (pure prettier + import-sort autofix, ~1404 fixes)
- **PR3**: hand-fix the 2 real bugs + clean warnings
- **PR4**: merge `tests/` into `pnpm lint` and let CI gate it; retire `lint:tests`

## Test plan

- [x] `cd web && pnpm lint` → 0 errors (src/ unchanged)
- [x] `cd web && pnpm lint:tests` → 1406 errors visible (proof override is active)
- [x] Pre-commit hook (frontend checks) passes
- [ ] CI `code-quality / lint-and-test` green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `5b0ecd26` feat(seo): 301 redirect ecap.gensmo.com → zooclaw.ai + migration banner (#887)
- **作者**: peter-srp
- **时间**: 2026-04-16T08:34:10Z
- **链接**: [5b0ecd26](https://github.com/SerendipityOneInc/ecap-workspace/commit/5b0ecd260a733ceb750330567fe8b0707e38e410)

**PR #887 Description:**
## Summary

- 301 permanent redirect from `ecap.gensmo.com` → `zooclaw.ai` (preserves path + query)
- `robots.txt` returns `Disallow: /` on legacy hostname to stop crawler indexing
- Brand upgrade banner shown only to users redirected from old domain (`?from=ecap`)
- i18n support (en + zh)

## SEO Impact

- 301 tells Google to transfer all ranking authority to `zooclaw.ai`
- Combined with existing `<link rel="canonical" href="https://zooclaw.ai/...">` (in `seo.ts`) and the new robots.txt block, search results will converge to `zooclaw.ai` within weeks
- No duplicate content risk — old domain serves only redirects

## How it works

1. User visits `ecap.gensmo.com/en/chat` → middleware returns **301** to `zooclaw.ai/en/chat?from=ecap`
2. On `zooclaw.ai`, `DomainMigrationBanner` detects `?from=ecap`, shows upgrade toast, cleans the URL param
3. Normal `zooclaw.ai` users never see the banner

## Files changed (6)

- `web/src/middleware.ts` — legacy host detection + 301 redirect
- `web/src/app/robots.ts` — Disallow: / on legacy host
- `web/src/components/DomainMigrationBanner.tsx` — new component
- `web/src/components/ClientLayout.tsx` — wire banner
- `web/src/locales/en.ts` / `zh.ts` — brand upgrade copy

## Test plan

- [ ] Visit `ecap.gensmo.com` → verify 301 to `zooclaw.ai?from=ecap`
- [ ] On `zooclaw.ai?from=ecap` → verify banner appears, then disappears after close
- [ ] Visit `zooclaw.ai` directly → verify NO banner
- [ ] `curl -I ecap.gensmo.com/robots.txt` → verify `Disallow: /`
- [ ] `curl -I zooclaw.ai/robots.txt` → verify normal robots (Allow: /)
- [ ] `tsc --noEmit` clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `a4b3c4de` chore(ci-lint): guard that three import-linter repo lists stay in sync (#888)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T08:20:29Z
- **链接**: [a4b3c4de](https://github.com/SerendipityOneInc/ecap-workspace/commit/a4b3c4def76bbe08d39e205e7ab986c13a71d2bb)

**PR #888 Description:**
## Summary

Follow-up to [Codex's non-blocking suggestion on #872](https://github.com/SerendipityOneInc/ecap-workspace/pull/872): close the drift window between the three repo enumerations in \`[tool.importlinter.contracts]\`.

**The drift class**: adding a new \`*_repo.py\` requires updating all three lists — C1 \`ignore_imports\`, C4 \`modules\`, C4b \`forbidden_modules\`. Missing one still fails C1 (via the generic "app can't import favie_common" default) but with a confusing error message. The new repo appears in the contract violation diff rather than the human-readable "forgot to add to the whitelist" report.

## Changes

- New \`services/claw-interface/scripts/ci-lint/06-importlinter-repo-sync.sh\`. Parses \`pyproject.toml\` with \`tomllib\`, extracts repo entries from the three contracts, asserts set equality.
  - Same binary-discovery + hard-fail pattern as \`02-import-linter.sh\` / \`03-complexity.sh\` / \`04-deptry.sh\`.
  - Clean state emits \`"all three contracts agree on N repos."\`; drift emits \`"in X only: [...]"\` precise diff + exit 1.
- Wire into \`.pre-commit-config.yaml\` under \`importlinter-repo-sync\` hook id.
- CI auto-picks-up via srp-actions' \`custom_lint_scripts_dir\`.

## Test plan

- [x] Clean tree → \`"all three contracts agree on 12 repos."\`, exit 0
- [x] Negative probe: remove \`app.database.user_repo\` from C4.modules → exit 1 with diff output showing \`"in C1 only: ['app.database.user_repo']"\`
- [x] Stashed script is executable and follows the binary-discovery pattern used by sibling scripts
- [ ] CI \`claw-interface-quality / lint-and-typecheck\` shows \`Running: 06-importlinter-repo-sync.sh\` → PASS

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `97687fd0` docs(superpowers): service-layer exception decoupling spec (#873 Item 1) (#882)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T08:17:54Z
- **链接**: [97687fd0](https://github.com/SerendipityOneInc/ecap-workspace/commit/97687fd081695c2bcdb7a3c36d315f1b918eec02)

**PR #882 Description:**
## Summary

- 交付 `docs/superpowers/specs/2026-04-16-service-layer-exceptions.md`（226 行，Status: Proposed）。
- 响应 Issue #873 Item 1：service 层（10 模块 × 46 处 `raise HTTPException`）与 FastAPI transport 耦合的设计决策。
- **推荐 Option B（一次性全迁）**：引入 `app/errors/` 领域异常层 + 新 ci-lint guard `06-services-no-httpexception.sh`（allowlist-shrink，与 `02-repo-pattern-guard.sh` 同款）。
- **迁移计划**：5–6 PR 链（Phase 0 基础设施 → Phase 1 openclaw 子域 + leaf utilities → Phase 2 gift_code → Phase 3 invite_code → Phase 4 stripe → Phase 5 guard 硬化），每 PR ≥ ~150 行 diff。
- 本 PR **只交付设计** —— Phase 0+ 的代码 PR 不在本 scope，随后按 spec 迁移计划各自开 issue/PR 跟进。
- 与 #881（Item 2 docstring fix）**并行**，互不阻塞。

## Open Questions（期待 review 讨论后写入 spec 设计决策章节）

1. `favie_common.middleware.exception_handler` 去留 / 共存策略
2. `ExternalServiceError` 是否透传 upstream HTTP status（影响 stripe 迁移设计）
3. streaming 端点（`agent_runtime.py`）领域异常映射契约
4. `app/routes/openclaw_runtime.py::_handle_error` 是否纳入 scope
5. 异常 `code` 命名规范（`<domain>_<reason>` vs `<module>.<reason>`）

## Test plan

- [x] spec markdown 可渲染（GitHub PR preview 手检）
- [x] 引用的 ci-lint 脚本路径存在（`services/claw-interface/scripts/ci-lint/02-repo-pattern-guard.sh`）
- [x] 引用的 spec 路径存在（`docs/superpowers/specs/2026-04-11-stripe-routes-refactor.md`、`2026-04-14-stripe-cleanup.md`）
- [x] 46 处 raise 行号已核实
- [ ] CI 通过（纯 doc PR，预期无 CI 运行）

Refs #873 (Item 1).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `07409bf0` fix(devcontainer): activate claw-interface venv in all shells (#886)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T08:06:53Z
- **链接**: [07409bf0](https://github.com/SerendipityOneInc/ecap-workspace/commit/07409bf09e9d1fe19e13b59a048fa169e57bce99)

**PR #886 Description:**
## Summary
- `Dockerfile`: export `VIRTUAL_ENV` and prepend `/home/node/.venvs/claw-interface/bin` to `PATH` (root fix, effective on container rebuild).
- `postCreateCommand.sh`: idempotently append the same exports to `~/.zshrc` / `~/.bashrc` so existing containers get the fix without a rebuild.

## Why
pyright resolves the Python interpreter by scanning `PATH` first (`which python`), **not** `VIRTUAL_ENV`. The venv lives on a named volume, never exposed on `PATH`, so fresh shells ended up on system Python 3.13 and pyright reported spurious `Import could not be resolved` for `dotenv` / `fastapi` / `httpx` / `uvicorn`. This wasn't worktree-specific — the main workspace had the same defect, but VSCode's ms-python plugin masked it by auto-activating the venv inside its own terminals.

## Test plan
- [x] Fresh `zsh -i`: `which python` → `/home/node/.venvs/claw-interface/bin/python`, `echo $VIRTUAL_ENV` set
- [x] `cd services/claw-interface && pyright app/ tests/` → **0 errors** (previously reported missing imports are now resolved)
- [x] `pytest tests/unit/` → 2369 passed (no regression)
- [x] rc patch is idempotent — second run is a no-op
- [ ] CI: `python-code-quality` unaffected (reusable workflow builds its own venv, doesn't touch devcontainer)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `0b12920e` chore(ci-lint): retire 02-repo-pattern-guard.sh (superseded by import-linter C1) (#885)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:55:05Z
- **链接**: [0b12920e](https://github.com/SerendipityOneInc/ecap-workspace/commit/0b12920ecd178e9347b767605fe4647363723e41)

**PR #885 Description:**
## Summary

Retire the bash `02-repo-pattern-guard.sh` now that the import-linter C1 contract (landed in #871, layered contracts in #872) provides equivalent or stronger enforcement.

**Observed parallel behavior**: On #871's CI, the bash guard and `lint-imports` produced identical pass/warn sets across every change. C1 is now the sole mongo-isolation check.

**What C1 provides over the bash guard**:
- **Finer-grained edges**: Per-importer `A -> favie_common` entries instead of whole-file ALLOWLIST — shrinks more precisely as migrations land.
- **Built-in stale-entry detection**: Unmatched `ignore_imports` emit "No matches for ignored import" (same shrink-only semantics as the bash stale-allowlist check).
- **Correct transitive exemption**: `allow_indirect_imports = true` lets services reach `favie_common` through repo methods without false positives — something the bash grep couldn't express cleanly.

## Changes

- Delete `services/claw-interface/scripts/ci-lint/02-repo-pattern-guard.sh`.
- Remove `repo-pattern-guard` hook from `.pre-commit-config.yaml`.
- Update `CLAUDE.md` "Database access" bullet to point at the C1 contract and `lint-imports`.
- Drop the stale "mirrors the bash guard's ALLOWLIST" reference in the C1 contract comment.

## Test plan

- [x] `lint-imports` → 5 contracts kept, 0 broken (C1/C2/C2b/C4/C4b)
- [x] `bash scripts/ci-lint/04-deptry.sh` → clean
- [x] No remaining references to `02-repo-pattern-guard` in repo (`grep -r`)
- [ ] CI `python-code-quality / build-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `a098ef9d` feat(sentry): comprehensive monitoring coverage (#860)
- **作者**: peter-srp
- **时间**: 2026-04-16T07:40:17Z
- **链接**: [a098ef9d](https://github.com/SerendipityOneInc/ecap-workspace/commit/a098ef9df2424aa329b4f7960adfc757cc3a8fd6)

**PR #860 Description:**
对前端的所有 try/catch 兜底 + 网络错误进行收集。 具体来说：

  - 网络错误 100% 覆盖 — httpClientIntegration 全局拦截，不漏
  - JS 异常 100% 覆盖 — SDK 自动 + 3 层 ErrorBoundary
  - 业务错误 ~90% 覆盖 — 核心链路（auth / payment / chat / WS / admin）全有专属
  Monitor；Canvas / Onboarding / Skills store 暂缺（plan 里标记为 YAGNI，等出问题再加）
  - 噪音控制到位 — SSE 探测、debug、重连风暴都已过滤/去重

## `c85e2e01` chore(lint): add layered-architecture contracts (C2, C2b, C4, C4b) (#872)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:33:02Z
- **链接**: [c85e2e01](https://github.com/SerendipityOneInc/ecap-workspace/commit/c85e2e01c17a7ec347ddf8ae44d97e06e9c7c1f3)

**PR #872 Description:**
Stacked on top of #871 (`feature/import-linter-c1`). **Merge #871 first**, then this PR's base auto-rebases to \`main\` and the diff shows only the new contracts.

## Summary

Extends the import-linter configuration with four additional structural contracts. All pass against the current tree — no code changes required.

- **C2** (layers): `app.routes` → `app.services` → `app.database`, non-exhaustive.
- **C2b** (forbidden): `app.schema` is a leaf; it must not import routes, services, or database modules.
- **C4** (independence): each \`app/database/*_repo.py\` is independent of every other repo; cross-collection work lives in services.
- **C4b** (forbidden): \`app.database._errors\` and \`app.database.collections\` are shared utilities that must not reach back into repos.

**C5 and C3 are intentionally omitted.** See the inline comments in \`pyproject.toml\` and the commit message for the reasoning:
- C5 (leaf service helpers): import-linter's \`forbidden\` contract treats modules as packages by default, so sources that are descendants of their forbidden target fail the "shared descendants" check. Working around it would require enumerating every sibling module by hand.
- C3 (routes do not import each other): \`app/routes/session/\` is a cohesive feature package split across multiple files that legitimately import each other; a naive rule would misfire. Revisit after the session package is restructured.

## Test plan

- [x] \`lint-imports\` → 5 contracts kept, 0 broken
- [x] \`pyright app/ tests/\` → 0 errors
- [x] \`pytest tests/unit/\` → 2363 passed
- [ ] CI \`python-code-quality / build-and-test\` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `83dfaab7` fix(agents-manager): require explicit session reset after updates (#879)
- **作者**: nolan-srp
- **时间**: 2026-04-16T07:30:25Z
- **链接**: [83dfaab7](https://github.com/SerendipityOneInc/ecap-workspace/commit/83dfaab7c9c3745109230c8a18d300e2569c5da0)

**PR #879 Description:**
## Summary
- stop the redeploy endpoint from automatically posting `/new` after agent updates
- prompt users in the agents manager and agent detail flows to explicitly start a fresh session after updating an agent
- add reset state handling, localized copy, and unit coverage for the new post-update flow

## `ae8b90e6` chore(claw-interface): enforce deptry gate — Step 2 of #870 (#883)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:23:42Z
- **链接**: [ae8b90e6](https://github.com/SerendipityOneInc/ecap-workspace/commit/ae8b90e6af491b9e4a15e35e11499986cb102c92)

**PR #883 Description:**
## Summary

Closes out the two-step deptry rollout from issue [#870](https://github.com/SerendipityOneInc/ecap-workspace/issues/870) by flipping `04-deptry.sh` from warning mode to hard failure. Step 1 ([#877](https://github.com/SerendipityOneInc/ecap-workspace/pull/877)) has been on main for several PR cycles now — the warning-mode window surfaced zero new violations, so the git-URL / transitive edge cases the safeguard was guarding against did not materialise.

### Design choice: remove the switch, not flip it

Rather than `WARN_ONLY=1` → `WARN_ONLY=0`, the variable and its entire branch are deleted. A dormant warning-mode toggle invites a one-char "temporarily soften the gate" edit later on; removing it means re-opting into warning mode takes a conscious design step.

### Test mirror

- `test_warning_mode_does_not_fail_on_violation` → `test_violation_fails_the_build`: asserts `returncode == 1`, `ERROR` banner, and — importantly — that `WARN_ONLY` is *absent* from the script body, so nobody can silently re-add the escape hatch.
- `test_warning_banner_mentions_rollout_issue` → `test_script_cites_rollout_issue`: the warning banner is gone but the header still cites #870 for future design-rationale lookup.

### Companion doc/config changes

- `04-deptry.sh` header reframes warning mode as historical rollout note.
- `.pre-commit-config.yaml` hook name drops "warning mode".
- `services/claw-interface/CLAUDE.md` drops the "warning-mode during rollout" wording.
- Spec `docs/superpowers/specs/2026-04-16-deptry-rollout.md` `Status` → Completed.

## Test plan

- [x] `pytest tests/unit/test_ci_lint_deptry.py` — 6 passed
- [x] `ruff check` / `ruff format --check` clean
- [x] Inject canary unused dep → `04-deptry.sh` exits 1 with `ERROR: deptry reported dependency issues (DEP001-DEP004)` banner
- [x] Clean tree → `04-deptry.sh` exits 0 with success banner
- [ ] CI `python-code-quality / build-and-test` green
- [ ] CI's `04-deptry.sh` step prints success banner

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `0ad945f7` chore(lint): adopt import-linter with C1 mongo-isolation contract (#871)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:21:53Z
- **链接**: [0ad945f7](https://github.com/SerendipityOneInc/ecap-workspace/commit/0ad945f795ccef2c5bcef6f4bc034f77d955188e)

**PR #871 Description:**
## Summary

- Add `import-linter>=2.0` to `requirements-dev.txt`.
- Declare a `[tool.importlinter]` section in `pyproject.toml` with the first contract, **C1**, enforcing that only `app/database/` may import `favie_common` (which is the third-party package housing `mongo_client`).
- Wire a `lint-imports` hook into `.pre-commit-config.yaml` (follows the same "skip if venv not found" pattern as the existing pyright hook).
- `.gitignore` the `.import_linter_cache/` directory.

**Why favie_common, not favie_common.database.mongo_client?** grimp squashes external packages to their top-level name when `include_external_packages = true`, so the finest-grained target we get for a third-party package is `favie_common`. Non-mongo usage (`create_app`'s middleware imports) is whitelisted explicitly.

**Why `allow_indirect_imports = true`?** The contract is about direct edges. Services reach `favie_common` transitively through repo methods, which is the intended layering and must not count as a violation.

The existing bash guard `scripts/ci-lint/02-repo-pattern-guard.sh` continues to run in parallel. After 1-2 CI cycles confirm the two agree on every code change, a follow-up PR will retire the bash script.

## Test plan

- [x] `lint-imports` → 1 contract kept, 0 broken (202 files, 871 deps analyzed)
- [x] Negative test: wrote `app/__probe_mongo.py` with a direct `from favie_common.database.mongo_client import mongo` → C1 BROKEN, exit 1. Removing the probe restored green.
- [x] `pyright app/ tests/` → 0 errors
- [x] `pytest tests/unit/` → 2363 passed
- [ ] CI `python-code-quality / build-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `37b0a736` test(claw-interface): harden 04-deptry.sh test from silent no-op (#880)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:14:34Z
- **链接**: [37b0a736](https://github.com/SerendipityOneInc/ecap-workspace/commit/37b0a7365acfd73dac1bbde02288e1638b8b18a7)

**PR #880 Description:**
## Summary

Picks up two non-blocking review suggestions from the final auto-review pass on [#877](https://github.com/SerendipityOneInc/ecap-workspace/pull/877) that came in **after** the last commit cycle and went unaddressed before merge.

- **`test_missing_binary_hard_fails` silent-no-op guard**: the two `.replace()` calls assume 04-deptry.sh still embeds the exact venv paths `"$REPO_ROOT/services/claw-interface/.venv/bin/deptry"` and `"/home/node/.venvs/claw-interface/bin/deptry"`. If both strings are ever reworded, the replaces silently no-op and the real deptry keeps being discovered via the hardcoded fallback — the script runs against the live repo (which is clean), exits 0, and the test false-passes. Same silent-pass failure mode `03-complexity.sh` was previously hardened against. One-line `assert hobbled_source != original_source` closes it.
- **Drop unused `tmp_path` fixture** in `test_warning_mode_does_not_fail_on_violation`: the signature advertises sandboxing but the test actually mutates the real `services/claw-interface/requirements.txt` inside a `try/finally`. Removing the parameter aligns signature with behaviour.

Neither change alters test semantics on the clean tree; both are defensive improvements.

## Test plan

- [x] `pytest tests/unit/test_ci_lint_deptry.py` — 6 passed locally
- [x] `ruff check` / `ruff format --check` clean
- [ ] CI `python-code-quality / build-and-test` green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `bf68cfd8` docs(openclaw-runtime): fix _resolve docstring to match 3-tuple return (#881)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:12:03Z
- **链接**: [bf68cfd8](https://github.com/SerendipityOneInc/ecap-workspace/commit/bf68cfd87a1218b7b02263853870dc0d04d8043c)

**PR #881 Description:**
## Summary

- `app/routes/openclaw_runtime.py::_resolve` 的 docstring 写 `(bot, app_token)`，实际返回 `(user, bot, app_token)`（来自 `get_user_bot_and_token`）。四个调用点都三元 unpack `_, bot, app_token`（行 45/60/75/90）。
- 只修 docstring，一行 diff。保留 `_resolve` 包装器本身，因为 `tests/unit/test_openclaw_runtime_routes.py` 的 fixture 和若干单测用 `monkeypatch.setattr(rt, "_resolve", ...)` 把它当作 patch 锚点（与 `app/routes/connectors.py` 的 `_get_user_bot_and_token` 同款模式）。
- Closes Item 2 of #873。Item 1（service 层 HTTPException 解耦设计）在另一个 PR 里交付 spec。

## Test plan

- [x] `pyright app/routes/openclaw_runtime.py` — 0 errors
- [x] `ruff check` / `ruff format --check` — clean
- [x] `pytest tests/unit/test_openclaw_runtime_routes.py` — 11/11 pass
- [ ] CI `python-code-quality / build-and-test` green

Refs #873 (Item 2).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `2dafe33c` chore(claw-interface): add deptry dependency-consistency gate (warning mode) — Step 1 of #870 (#877)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T07:02:16Z
- **链接**: [2dafe33c](https://github.com/SerendipityOneInc/ecap-workspace/commit/2dafe33c6cb57f8484112343e7bd8b5a98dd41c7)

**PR #877 Description:**
## Summary

Step 1 of the [issue #870](https://github.com/SerendipityOneInc/ecap-workspace/issues/870) two-step rollout — wires `deptry` into `services/claw-interface/`'s CI lint chain to catch the four dependency-consistency failure modes (DEP001–DEP004), while cleaning up the pre-existing violations surfaced during the first scan.

- Runs in **warning mode** (`04-deptry.sh` `WARN_ONLY=1`) so this PR doesn't block anything even if CI surfaces unexpected git-URL or transitive-import edge cases.
- Step 2 (separate, follow-up PR) will flip `WARN_ONLY=0` once we've observed clean CI runs on a few real PRs — rationale in `docs/superpowers/specs/2026-04-16-deptry-rollout.md`.

### Key changes
- `services/claw-interface/pyproject.toml`: `[build-system]` + `[tool.setuptools.dynamic]` (bridge so deptry reads `requirements*.txt`) + `[tool.deptry]` config (first-party, exclude override to keep `tests/` in scope, `package_module_name_map` for git-URL packages, `per_rule_ignores` for non-import-consumer deps like pytest plugins).
- `requirements.txt`: drop obsolete (`faker`, `asyncio` stdlib, `e2b`, `mcp-proxy`); dedupe `prometheus_fastapi_instrumentator`; promote `starlette` + `botocore` from transitive to direct (they *are* imported directly by `app/` and `tests/`); add `.git` suffix to `favie-common` URL so deptry parses the package name.
- `requirements-dev.txt`: add `deptry>=0.20`, drop redundant `faker`.
- `scripts/ci-lint/04-deptry.sh`: new script. Reuses `03-complexity.sh`'s `PATH → .venv → devcontainer venv` binary-discovery cascade.
- `CLAUDE.md`, `.cursor/rules/tech-stack.mdc`: keep docs in sync with the new gate and the dependency cleanup.
- `docs/superpowers/specs/2026-04-16-deptry-rollout.md`: design spec with the full 168 → 0 violation-reduction path, for future agents / contributors.

### Non-goals (deferred to Step 2 follow-up PR)
- Flipping `WARN_ONLY=0` to make deptry a hard gate
- Regenerating `uv.lock` from the updated `requirements.txt` (can happen out-of-band; lock is derived-state, not source-of-truth)

## Test plan

- [x] `deptry app tests` reports zero violations locally
- [x] `ruff format --check app tests` clean
- [x] `ruff check app tests` clean
- [x] `pyright app tests` clean (with venv activated)
- [x] `scripts/ci-lint/04-deptry.sh` exits 0 on clean tree
- [x] Injected fake DEP002 violation (appended `unused-canary` to `requirements.txt`): script prints warning + violation details **and** still exits 0 (warning mode)
- [ ] CI `python-code-quality / build-and-test` green
- [ ] CI `04-deptry.sh` step prints "No dependency issues found"

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `e0b661a0` fix: change connector skill injection path to ~/.agents/skills (#878)
- **作者**: Leo-srp
- **时间**: 2026-04-16T06:45:35Z
- **链接**: [e0b661a0](https://github.com/SerendipityOneInc/ecap-workspace/commit/e0b661a00c8928cf94f4999198cd2c96661a6bc4)

**PR #878 Description:**
## Summary
Change Nango connector skill injection path from `~/.openclaw/skills` to `~/.agents/skills`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `031a481d` fix(web): 修复 agent 详情页和弹窗里头像浮动动画的问题 (#863)
- **作者**: lynn Zhuang
- **时间**: 2026-04-16T06:06:18Z
- **链接**: [031a481d](https://github.com/SerendipityOneInc/ecap-workspace/commit/031a481d8a583bb22eecab27d987206a0f367aeb)

**PR #863 Description:**
去掉了 agent 详情页和弹窗里头像浮动动画的效果

## `00e43349` docs(lazy-imports): annotate the non-obvious function-body imports (#874)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T05:44:45Z
- **链接**: [00e43349](https://github.com/SerendipityOneInc/ecap-workspace/commit/00e43349e1576e9a2c09ee1c288e41ad5cc38a89)

**PR #874 Description:**
## Summary

Introduce a `# lazy: <reason>` convention to document non-obvious function-body imports. Four reason tags are used:

- **`heavy lib`** — defer large third-party packages (`boto3`/`botocore` in `r2_storage`; Pillow in `media_utils` and transitively from `r2_storage`'s image branch).
- **`startup side-effect`** — modules that do meaningful work at import time (env-backed `SETTINGS`, network IO in `apple_service`), kept inside `lifetime.py`'s startup function.
- **`avoid pytest cycle`** — the existing auth↔services test-collection cycle documented on `require_admin_user`, reformatted to the canonical tag.
- **`error recovery`** — imports only reached from except-branch paths (`subscription_manager` wallet-recovery fallback).

Only the **non-obvious** cases are annotated. Stdlib `traceback` inside an `except` block or `json` inside a validator don't need a tag because the reason is evident from context.

This PR is documentation-only — no code paths change, no tests change.

## Test plan

- [x] `ruff check` + `ruff format --check` clean
- [x] `pyright app/ tests/` → 0 errors
- [x] `pytest tests/unit/` → 2363 passed
- [ ] CI `python-code-quality / build-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `055867ba` refactor(openclaw): move get_user_bot_and_token to services layer (#869)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T05:16:01Z
- **链接**: [055867ba](https://github.com/SerendipityOneInc/ecap-workspace/commit/055867ba4a78682c67d825024fcf37d2923e5592)

**PR #869 Description:**
## Summary

- Extract `_get_user_bot_and_token` from `app/routes/openclaw_settings.py` into a new module `app/services/openclaw/bot_token.py` (public name `get_user_bot_and_token`).
- Replace the function-body `from app.routes.openclaw_settings import _get_user_bot_and_token` lazy imports in `app/routes/openclaw.py` (line 393) and `app/routes/openclaw_runtime.py` (line 22) with a plain top-level import from `app.services.openclaw.bot_token`.
- Update matching test patch targets: direct helper tests patch `app.services.openclaw.bot_token.{user_repo,get_app_token,get_first_bot}` (the module that actually runs the code); endpoint tests patch `app.routes.openclaw_settings.get_user_bot_and_token` (the imported name the route module calls).

This is PR 2 in the import-linter adoption series. Eliminating the last two cross-route lazy imports is the prerequisite for the planned "routes modules do not import each other" contract (C3).

## Test plan

- [x] `pyright app/ tests/` → 0 errors
- [x] `ruff check` + `ruff format --check` clean
- [x] `pytest tests/unit/` → 2363 passed
- [ ] CI `python-code-quality / build-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `0343d092` refactor(orders): import ensure_billing_initialized from services directly (#868)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T05:14:36Z
- **链接**: [0343d092](https://github.com/SerendipityOneInc/ecap-workspace/commit/0343d0928046a3e649b1bddc1b6c5b07769fcdfb)

**PR #868 Description:**
## Summary

- Drop the function-body `from .user import ensure_billing_initialized` lazy import in `app/routes/orders.py`; import the helper directly from `app.services.billing` at module top.
- The re-export via `app.routes.user` was an accidental dependency — `orders` doesn't need `user`, both consume `services.billing`.
- Update the matching test patch target from `app.routes.user.ensure_billing_initialized` to `app.routes.orders.ensure_billing_initialized` (patch the importing module, per project convention).

This is PR 1 in the series that prepares for `import-linter` adoption. Eliminating this cross-route lazy import is a prerequisite for the planned "routes modules do not import each other" contract.

## Test plan

- [x] `pyright app/ tests/` → 0 errors
- [x] `ruff check` + `ruff format --check` clean
- [x] `pytest tests/unit/` → 2363 passed
- [ ] CI `python-code-quality / build-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `caa19e66` chore(ci-lint): broaden repo-pattern scan to entire app/ except database/ (#867)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T05:14:01Z
- **链接**: [caa19e66](https://github.com/SerendipityOneInc/ecap-workspace/commit/caa19e665ed9c93405e9a994b1fd916f59cf0fc3)

**PR #867 Description:**
## Summary

- Extend `scripts/ci-lint/02-repo-pattern-guard.sh` to scan all of `app/` (excluding only `app/database/`, the one legitimate home for `mongo_client`) instead of just `app/routes/`, `app/services/`, and `app/lifetime.py`.
- Allowlist two newly surfaced legacy offenders: `app/scheduler.py` (stale-job cleanup) and `app/cron/subscription_cron.py` (subscription lifecycle cron). Both are tracked for dedicated-repo migration in separate follow-up PRs.
- Update `services/claw-interface/CLAUDE.md` to describe the broadened scope.

This is PR 0 in a series that will replace the bash guard with an `import-linter` contract while expanding structural enforcement (layered architecture, routes non-interdependence, database repo independence). Broadening scan coverage first establishes a clean baseline.

## Test plan

- [x] `bash services/claw-interface/scripts/ci-lint/02-repo-pattern-guard.sh` → clean exit, 6 allowlist entries reported as WARNING
- [x] Negative test: temporarily wrote `app/__probe_mongo.py` with a direct `mongo_client` import → script reported ERROR and exited 1; removing the probe restored green.
- [ ] CI `python-code-quality / build-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `d4834a34` test(claw-interface): extract shared user-doc builder (#864) (#865)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T04:26:39Z
- **链接**: [d4834a34](https://github.com/SerendipityOneInc/ecap-workspace/commit/d4834a34474d41f9baff4b97fcbfb20ea44f8ad9)

**PR #865 Description:**
## Summary

- 新建 `services/claw-interface/tests/_helpers/user_builders.py`（root-level，给 BDD 和 unit 共用），把 `make_user_doc` 从 `tests/bdd/helpers.py` 搬过去
- `tests/unit/test_user_routes_coverage.py` 的 `_base_user` 改为 thin wrapper，通过 overrides 补 `invite_binding` 和硬码时间戳 `1000000`（保留原单测的确定性语义）
- 3 个 BDD step_defs（`test_user_crud` / `test_user_endpoints` / `test_user_list`）的 import 直接指向新路径，**不留 re-export shim**

Closes #864（Follow-up to #844 Hotspot 1）。Hotspot 2（`favie_common` stub）和 Hotspot 3（`test_admin_boost`，已由 #856 解决）out-of-scope。

## Test plan

- [x] `ruff format` + `ruff check tests/` 干净
- [x] `pyright app/ tests/` 全仓 0 errors 0 warnings
- [x] `pytest tests/unit/test_user_routes_coverage.py` 7/7 pass
- [x] `pytest tests/bdd/step_defs/test_user_{crud,endpoints,list}.py` 46/46 pass（`TEST_MONGODB_HOST=127.0.0.1 MONGODB_USER= MONGODB_PASSWORD=`）
- [x] `jscpd -c .jscpd.tests.json` exit 0；`bdd/helpers.py ↔ test_user_routes_coverage.py` clone pair 已从 report 消失；duplication 保持 5.37% < 阈值 7.5%
- [ ] 等 CI 的 `python-code-quality / build-and-test` + auto-reviewer 绿

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `ea63724b` chore(ci-lint): extend repo-pattern guard to scan app/lifetime.py (#859)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T04:18:52Z
- **链接**: [ea63724b](https://github.com/SerendipityOneInc/ecap-workspace/commit/ea63724b8672414f41e640fd25a2ace9d66cde96)

**PR #859 Description:**
## Summary
Defence-in-depth follow-up to #845, which moved index creation out of \`app/lifetime.py\` into per-repo \`ensure_indexes()\` methods. Lifetime is now mongo-free, so adding it to the scan set means any future re-introduction of a direct mongo import at startup fails CI instead of quietly slipping past.

## Change
- \`scripts/ci-lint/02-repo-pattern-guard.sh\`: extend scan from \`app/routes/ app/services/\` to also include \`app/lifetime.py\`

## Test plan
- [x] Guard still clean locally (4 session-route allowlist warnings, 0 errors)
- [x] Header comment updated to reflect new scope
- [x] No Python changes — no unit test / pyright impact

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `a145411b` refactor(claw-interface): extract resolve_or_generate_code (#853)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T04:10:02Z
- **链接**: [a145411b](https://github.com/SerendipityOneInc/ecap-workspace/commit/a145411be12afef692a0e81365ec76ed7c8c1ad5)

**PR #853 Description:**
Supersedes #849. Stacked on #851 (PR-C v2).

## Summary
Gift-code and invite-code admin creation each wrote the same three-step dance: normalize admin-supplied code, look it up for a friendly "already exists", else fall back to a domain-specific unique generator. Collapse the orchestration into \`app.services.code_utils.resolve_or_generate_code\`.

Normalize/generate functions stay per-domain — the alphabets, prefixes, and collision budgets differ; only the editing on top of them is shared.

## Test plan
- [x] \`ruff check\` / \`ruff format\` / \`pyright\` — clean
- [x] \`pytest tests/unit/test_code_utils.py test_gift_code.py test_invite_codes.py test_bdd/test_invite_code.py\` — 90 tests pass
- [x] \`scripts/ci-lint/02-repo-pattern-guard.sh\` — clean

## Note
Empty string for \`request.code\` is treated the same as \`None\` — matches previous \`if request.code:\` truthiness; pinned by \`test_empty_string_treated_as_missing\`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `f6403881` feat(chat): Mattermost reactions, tool-steps toggle, smoother streaming (#742)
- **作者**: sam-srp
- **时间**: 2026-04-16T04:07:10Z
- **链接**: [f6403881](https://github.com/SerendipityOneInc/ecap-workspace/commit/f6403881f57af2391379eaabaddecc0b563d2c2b)

**PR #742 Description:**
## Summary

Frontend counterpart to the `@zooclaw/mattermost` streaming/tool/emoji work (SerendipityOneInc/zooclaw-extras#15).

- **Mattermost reaction events** — `useMattermost` now subscribes to `reaction_added` / `reaction_removed` WebSocket events and maintains a `reactionsByPostId` map. `OpenClawUserMessage` renders the collected reactions inline on the user's bubble (backed by `REACTION_EMOJI_MAP` covering state + tool-category emoji names).
- **Drop duplicated ack badge** — the old "👀 Assistant" ack pill was removed; the backend's `statusReactions.setQueued()` already emits a real `:eyes:` reaction, so the frontend badge was just a visual duplicate.
- **Tool steps UI simplification** — after iterating through several expanded layouts, settled on a compact name-only pill per tool step. Visibility is gated behind a header toggle (orange when on) with state persisted to `localStorage` (`ecap.showToolSteps`, default off).
- **Smoother streaming** — skip the typewriter effect for live-edited messages so streamed updates don't look like they are being retyped.
- **Custom `custom_tool_status` post handling** — parses the new hidden-from-native-clients posts that the zooclaw mattermost plugin emits, and surfaces them as tool steps on the corresponding bot message.

## Test plan

- [ ] Send a message via Mattermost bot — verify 👀 reaction appears on your user bubble on arrival and clears when the reply completes.
- [ ] Trigger a tool call (web search / read file / bash) — verify the category emoji (🔍 / 🖥️ / 🔥) appears during the tool and clears on done.
- [ ] Toggle tool steps in the header — pills appear/disappear; preference persists across reloads.
- [ ] Long reply — bot message updates smoothly (no per-character typewriter feel).
- [ ] Mid-conversation tool activity — pills attach to the correct bot message in chronological order.
- [ ] No duplicate 👀 on user bubble (the old ack badge is gone; only the server-side reaction should show).

## `7507366c` refactor(claw-interface): PagedResponse model + duplicate-key helper (#851)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T04:01:50Z
- **链接**: [7507366c](https://github.com/SerendipityOneInc/ecap-workspace/commit/7507366cc549370226c8d78623c25af1ab193eb9)

**PR #851 Description:**
Supersedes #848 (closed; needed rebase with PR-B's BDD fix). Stacked on #847 (PR-B).

## Summary
Same as #848. Two patterns duplicated across \`gift_code\` and \`invite_code\` admin routes, extracted:

### 1. \`PagedResponse[T]\` + \`build_paged_response(...)\`
- New \`app/schema/paging.py\` — typed generic model
- List endpoints now declare \`response_model=PagedResponse[GiftCodeResponse]\` / \`PagedResponse[InviteCodeResponse]\`, so OpenAPI broadcasts the shape to the TypeScript client
- \`has_more\` is derived from \`len(data)\` (not \`limit\`) so a short final page still computes correctly

### 2. \`translating_duplicate_key(detail)\` + \`is_duplicate_key_error(exc)\`
- New \`app/database/_errors.py\`
- Prefers \`pymongo.errors.DuplicateKeyError\` \`isinstance\` check, with a string fallback (\`E11000\` / \"duplicate key\") for callers that wrap the driver error
- Lives under \`app/database/\` so the pymongo dependency stays behind the repo boundary

## Test plan
- [x] \`ruff check\` / \`ruff format\` / \`pyright\` — clean
- [x] Unit: 90 affected tests pass; full suite 2354 pass (2 pre-existing unrelated failures)
- [x] BDD \`test_invite_code.py\` 12 tests pass locally (attribute access for PagedResponse)
- [x] \`scripts/ci-lint/02-repo-pattern-guard.sh\` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `ffb124a8` chore(ci-lint): tighten jscpd tests threshold 10.5% → 7.5% (#852)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T03:49:08Z
- **链接**: [ffb124a8](https://github.com/SerendipityOneInc/ecap-workspace/commit/ffb124a8ef958464b0cc3c45aae72cd5ccff42a4)

**PR #852 Description:**
## Summary

After PRs #850/#854/#855/#856/#857/#858 consolidated mock setup across 10 unit files, `python-tests` jscpd duplication dropped from **8.21% → 5.37%**. Apply the same `ceil(observed) + 1.5%` rule used in PR #846:

- `ceil(5.37) + 1.5 = 7.5%`

Current threshold `10.5%` leaves ~5.1 points of noise; `7.5%` keeps ~2.1 points of headroom for legitimate new tests while catching regressions much sooner.

Also fix the stale `Duplication check — Python tests (threshold 12%)` step name in `code-quality.yml` — it was never updated when PR #846 moved the value to `10.5%`.

## Metrics

| Metric | Before (at PR creation) | After 5 dedup rounds | After this PR |
| --- | --- | --- | --- |
| Tests duplication (lines) | 7.16% | **5.37%** | 5.37% (config-only) |
| Tests threshold | 10.5% | 10.5% | **7.5%** |
| Src duplication | 1.31% | 1.26% | — (threshold 3% already tighter than rule) |

## Test plan

- [x] `jscpd -c services/claw-interface/.jscpd.tests.json` — exits 0 locally at 5.37%
- [ ] CI `python-duplication-check` green on this branch

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `5b61ec43` test(claw-interface): round 4 dedup — connector_status + admin_boost (-60 LOC) (#856)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T03:40:44Z
- **链接**: [5b61ec43](https://github.com/SerendipityOneInc/ecap-workspace/commit/5b61ec43452498e077049d9ca9103fe84e2cf727)

**PR #856 Description:**
## Summary

Fourth round of test-side jscpd reduction, following PRs #850 / #854 / #855. Targets two remaining self-clone hotspots.

Drops duplication (vs main, which includes #854) **6.39% → 6.02%** with two new file-local contextmanagers + one small factory.

| File | Lines Δ |
|---|---:|
| \`test_connector_status.py\` | -26 |
| \`test_admin_boost.py\` | -36 |
| **total** | **-60** |

## Helpers added

**\`test_connector_status.py\`**
- \`_patch_status_deps(token, bot_lookup, bot_lookup_raises, client)\` — retires the 4-patch \`get_connector_token + SETTINGS + _get_user_bot_and_token + get_openclaw_client\` block repeated 9 times.
- \`_BOT_LOOKUP\` module constant removes the inline \`({\"uid\": \"u1\"}, {\"bot_id\": \"bot-1\"}, \"app-token\")\` 3-tuple repetition.

**\`test_admin_boost.py\`**
- \`_billing_with_balance(balance)\` — one-wallet billing-client factory (5x).
- \`_patch_boost_deps(user, billing_client, billing_raises, refresh_returns, refresh_raises)\` — retires the 3–4 patch block on \`user_repo + refresh_subscription_credits + transition_to_trial + optional get_billing_client\` (9 tests). Uses \`ExitStack\` internally to conditionally include patches.

## Metrics (jscpd, vs main)

| Metric | Before | After |
| --- | --- | --- |
| Duplicated lines | 2652 / 41510 | 2496 / 41450 |
| Duplication % | **6.39%** | **6.02%** |
| Clone blocks | 222 | 211 |

Independent of PR #855 (round 3) — different files, no conflicts.

## Test plan

- [x] \`pytest tests/unit/test_connector_status.py tests/unit/test_admin_boost.py -q\` — 33 passed
- [x] \`ruff check\` / \`ruff format\` / \`pyright\` clean
- [x] \`jscpd -c services/claw-interface/.jscpd.tests.json\` exits 0 at 6.02%
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `22f0b03e` test(claw-interface): round 5 dedup — chat_validation (-65 LOC) (#857)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T03:34:55Z
- **链接**: [22f0b03e](https://github.com/SerendipityOneInc/ecap-workspace/commit/22f0b03e1eea4c48a1ac5e6df8575c53ca232fee)

**PR #857 Description:**
## Summary

Round 5 in the test dedup series (#850 / #854 / #855 / #856). Targets the hottest remaining unit file after rounds 2–4:

- \`test_chat_validation.py\` — 86L / 7 clones

Drops duplication (vs main after rounds 2+3 merged) **5.9% → 5.8%** with one new file-local contextmanager.

## Helper added

\`_patch_chat_fullstack_deps(user, existing_title, extract_text, extract_assets)\` — retires the 6-patch block
\`\`\`
mongo + consume_credits + extract_assets_from_content + extract_text_from_message
+ generate_session_title + asyncio.create_task
\`\`\`
that was repeated 9 times in fullstack-assistant \`chat()\` tests.

Yields \`(mock_mongo, mock_create_task)\` so the few tests that assert on
\`mock_mongo.create.await_count\` / \`mock_create_task.call_count\` can still do so.

## Metrics (jscpd, vs main after rounds 2+3)

| Metric | Before | After |
| --- | --- | --- |
| Duplicated lines | 2443 / 41375 | 2398 / 41310 |
| Duplication % | **5.90%** | **5.80%** |
| Clone blocks | 208 | 204 |

Independent of the still-open #852 (threshold) and #856 (round 4) — different files, no conflicts. Together with #856 brings test-side dup below 6%.

## Test plan

- [x] \`pytest tests/unit/test_chat_validation.py -q\` — 23 passed
- [x] \`ruff check\` / \`ruff format\` / \`pyright\` clean
- [x] \`jscpd -c services/claw-interface/.jscpd.tests.json\` exits 0
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `afa99590` test(claw-interface): round 6 dedup — litellm_sse_edit (-36 LOC) (#858)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T03:34:27Z
- **链接**: [afa99590](https://github.com/SerendipityOneInc/ecap-workspace/commit/afa99590dd8981471c0119713081a608fbc0eb70)

**PR #858 Description:**
## Summary

Round 6 in the dedup series (#850 / #854 / #855 / #856 / #857). Targets the Gemini edit-mode tests in \`test_litellm_sse_edit.py\` — 8-patch block repeated across 3 test classes.

## Helpers added

- \`_make_edit_intent(target_url, reasoning)\` — mock intent factory.
- \`_patch_gemini_edit_deps(image_urls, mock_intent, download_return, download_side_effect, gemini_result)\` — retires the 8-patch block:
  - \`get_virtual_key_from_request + get_litellm_headers + extract_image_urls_from_content + analyze_user_intent + download_image_from_url + detect_image_format + generate_image_with_gemini + SETTINGS\`
  repeated 3x in \`TestDoGenerateImagesEditFallback\` / \`TestDoGenerateImagesExtraImages\` (x2) / \`TestDoGenerateImagesGeminiEditThoughts\`.

Yields \`(mock_download, mock_gemini)\` for per-test assertions on call args.

## Metrics (jscpd, vs main after rounds 2+3)

| Metric | Before | After |
| --- | --- | --- |
| Duplicated lines | 2443 / 41375 | 2415 / 41339 |
| Duplication % | **5.90%** | **5.84%** |
| File lines | 705 | 668 (-37) |

Independent of the still-open #852 / #856 / #857 — different files, no conflicts. Together they should land test-side dup under 5.5%.

## Test plan

- [x] \`pytest tests/unit/test_litellm_sse_edit.py -q\` — 17 passed
- [x] \`ruff check\` / \`ruff format\` / \`pyright\` clean
- [x] \`jscpd -c services/claw-interface/.jscpd.tests.json\` exits 0
- [ ] CI green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `cab8e9d4` refactor(claw-interface): unify admin guard into shared dependency (#847)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T03:32:08Z
- **链接**: [cab8e9d4](https://github.com/SerendipityOneInc/ecap-workspace/commit/cab8e9d439492eebe133a8307fb27f7e6bf8a932)

**PR #847 Description:**
## Summary

Four route files (`gift_code`, `invite_code`, `admin_boost`) duplicated the same admin guard — a two-layer check (live email allowlist via user profile + cached DB `permissions` fallback gated on GCP/CSFLE error keywords). Extract it as `require_admin_user` in `app.auth.dependencies` so new admin routes pick up the guard via a normal `Depends(...)` import.

- `openclaw_admin` and `release_admin` keep their local guards — both only verify authentication (BFF enforces admin), so consolidating with the stricter check would silently upgrade their authorization posture.
- Detailed profile/GCP-fallback matrix moves into `tests/unit/test_require_admin_user.py` (single source of truth); the per-route admin-guard blocks in `test_gift_code.py` / `test_invite_codes.py` are deleted since they were testing the same logic through a different import path.

## Follow-up fixes addressed in this PR

- **BDD fix**: `tests/bdd/step_defs/test_invite_code.py` patched `app.routes.invite_code.get_user_profile`, which no longer imports after the guard moves. Removed the dead patch.
- **Security fix (from Codex review)**: `admin_boost.py` was logging `request.admin_uid` from the POST body for audit attribution — an authenticated admin could spoof that. Switched to the JWT-verified `_admin_uid`; the body field is kept as optional + deprecated so existing frontend callers don't break. Regression test pinned.
- **Route-wiring regression test (from Codex review)**: New `tests/unit/test_admin_route_wiring.py` introspects each of the 5 admin endpoint signatures and asserts `Depends(require_admin_user)` — catches accidental removal of the guard that unit tests on the function would miss.

## Diff shape

- 10 files changed, +268 / −407 (net −139 lines of duplication and fragile patches removed)
- Admin check logic byte-identical to the previous `invite_code` version (which had the most complete docstring)

## Test plan

- [x] `ruff check` / `ruff format` — clean
- [x] `pyright app/ tests/` — 0 errors
- [x] `pytest tests/unit/test_require_admin_user.py tests/unit/test_admin_route_wiring.py tests/unit/test_invite_codes.py tests/unit/test_gift_code.py tests/unit/test_admin_boost.py` — all pass
- [x] `TEST_MONGODB_HOST=127.0.0.1 MONGODB_USER= MONGODB_PASSWORD= pytest tests/bdd/step_defs/test_invite_code.py` — 12 pass
- [x] Full CI (claw-interface-quality test + lint-and-typecheck + CodeQL + python-duplication-check): 15/15 SUCCESS (+ 2 SKIPPED web/ios)
- [x] `scripts/ci-lint/02-repo-pattern-guard.sh` — clean
- [x] Codex auto-review: APPROVE (5 rounds, all iterations addressed)

## Stacked chain

- Base: `main` (PR-A #845 merged)
- Downstream: #851 (PagedResponse + duplicate-key helper) → #853 (resolve_or_generate_code)
- Independent follow-up: #859 (extend repo-pattern guard to scan `app/lifetime.py`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## `748d119b` fix(claw-interface): scope skill loader hidden-file filter to skill dir (#839)
- **作者**: Chris@ZooClaw
- **时间**: 2026-04-16T02:55:50Z
- **链接**: [748d119b](https://github.com/SerendipityOneInc/ecap-workspace/commit/748d119b1d13e4c77ae71e853ac03e5b1fb4c121)


**PR #839 Description:**
## Summary

- `SkillRegistry.get_skill_files()` ran the `__pycache__` / hidden-file filter against every component of the absolute path, so any dot-prefixed ancestor directory (e.g. `.worktrees/<name>/…`) caused **every** discovered skill file to be dropped and the injector silently logged `No files to inject`.
- Switch the check to `path.relative_to(skill_dir).parts` so the filter matches the original intent (hidden files *inside* the skill dir) and is insensitive to the repo's checkout location.
- Add a regression test that constructs the skill dir under a `.worktrees/`-style parent — this scenario was invisible to CI because GitHub runner paths (`/home/runner/work/...`) contain no dot-prefixed components.

Fixes #811

## Why CI was green

The bug only fires when an ancestor of the skill directory starts with `.`. Neither CI (`/home/runner/work/ecap-workspace/ecap-workspace/...`) nor the primary clone (`/workspaces/ecap-workspace/...`) has such a component; only local worktrees under `.worktrees/` do. The new test fixes that blind spot by building the triggering path explicitly instead of relying on `tmp_path`.

## Test plan

- [x] `pytest tests/unit/test_skill_injector.py tests/unit/test_skill_loader.py -v` → 43 passed (previously 2 failed in worktrees)
- [x] `pytest tests/unit/ -q` → 2339 passed
- [x] `pyright app/ tests/` → 0 errors, 0 warnings
- [x] Minimal repro: `get_registry().get_skill_files("github")` returns `SKILL.md` (was `[]` under `.worktrees/`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
