# SerendipityOneInc/ecap-skills — commits 2026-09-02

## feat(council): V2-ready bootstrap, bounded flock and one-shot preflight (#275)

- **SHA**: `f40531a5367d197c192aa89c4b74546a68f90fd1`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-02T16:06:10Z
- **PR**: #275

### Commit Message

```
feat(council): V2-ready bootstrap, bounded flock and one-shot preflight (#275)

## 背景

用户反馈 `/council` 在 V2（zooclaw-engine，E2B sandbox）上第一步（Stage 0 组阵容 → Stage
1 确认面板）从 V1 的 20–30s 退化到 8 分钟不出结果。根因（详见 zooclaw-engine 侧配套 PR 与 issue）：

1. `run_status.py` 用无超时阻塞 `fcntl.flock(LOCK_EX)` 串行化 6/8 个子命令；V2 的 exec
在 yield 窗口后自动后台化并保留进程 → 一个被后台化的持锁者让之后每条 run_status.py 永久阻塞。用户截图里 agent
自己在 `grep flock` / `ps aux | grep run_status` / 扫 `/proc`。
2. 每条命令都是 `uv run --with jsonschema …`：V2 不执行 skill 的 `install[]`，`uv
run --with` 又不看模板已 bake 的 site-packages → 冷启动实测 12.1s，正好落进 yield 窗口。
3. Stage 0/1 是 6 条独立 exec；V2 每条 exec ≈ 一次 LLM 往返 + 一个 Temporal activity
+ 5 次 envd 往返（实测 1.15s 引擎侧固定开销）。

## 改动（6 个 commit 对应计划里的 PR-0…PR-5，可逐个 review）

| commit | 内容 |
|---|---|
| `ci(council)` | 新 `council-tests.yml`：PR 触碰 `council/**` 时跑 `pytest
council/tests`（此前没有任何 CI 跑这些测试） |
| `fix(council): bounded flock` | `_locked` 改 `LOCK_EX\|LOCK_NB` + 15s
deadline → 结构化 `LOCKED`；不删 `.lock`（删了会让第三个 opener 拿新 inode 双写）；flock
不支持的 FS 降级为无锁 + stderr 警告；`import jsonschema` 失败 →
`MISSING_DEPENDENCY`（不再 traceback） |
| `perf(council): cap catalog fetch` | `roster.py` fetch 预算 3s×2 + 1s 退避
= 最坏 7s（< 10s 自动后台化窗口；原 36s） |
| `fix(council): degrade cost collection` | `swarm_usage.py --store-dir`
可选：显式 → `COUNCIL_USAGE_STORE_DIR` → 自动发现
`~/.openclaw/agents/*/sessions`；V2 没有 openclaw session store 时 success +
`store:"unavailable"` + `total_credits:null`，SKILL.md 明说"未计量"，绝不报数 |
| `feat(council): self-bootstrap deps` | 新 `scripts/ensure_deps.py` +
`_deps.py`（stdlib）：先 `find_spec` 探测，全在则零子进程零网络；缺的用 `uv pip install
--target` / `pip --target` 装进 `~/.cache/council/deps/py3.x`，marker
放在安装目录内（同生共死、spec hash 变则重装）。之后所有脚本直接 `python3`；`requires.bins` →
`["python3"]` |
| `feat(council): one-shot preflight` | 新 `scripts/preflight.py`：进程内串起
fetch → propose → premium alt → init → estimate → `awaiting_go`，一份 JSON
输出（同时写 `$RUN/preflight.json` 供 smoke 断言）。Stage 0/1 从 6 条 exec 变 **1
条**。SKILL.md 改写：全部 `python3 {baseDir}/scripts/…`、每条 exec 带
`timeout`、`ROOT="$(pwd -P)/council-runs"` + `BAD_RUN_ROOT` 守卫（平台契约 ask
#2）、删掉未发布的 `../websearch` 引用；面板模板、门语义、Stage 5 K 行原文不动。新
`test_skill_md_contract.py` 钉住这些不变量 |

测试：330 passed（基线 275，+55）；`lint_skills.py` 通过；`sync-v2-registry.mjs
--validate` 通过。冷路径实测：系统 python3（无 jsonschema）跑一条 `preflight.py`，971ms 自装
→ `awaiting_go`，总 1.2s。

## V1/V2 中立

- SKILL.md 无 `uv run`、无 engine 路径；V1 pod 首次装进 `$HOME/.cache`（持久
FS）后跳过，V2 模板已 bake 则永不联网。
- run root 在 V1（`~/.openclaw/workspace/council-runs`）与
V2（`/workspace/council-runs`）都合法。
- `install[]` 原样保留（linter 要求非空，仅作文档）。

## 需要维护者注意

- 仓库 `CLAUDE.md` §3 写 "Prefer `uv run --with <deps>`"，本 PR 在 council
上反其道：原因是 V2 不执行 `install[]`、且 `uv run --with` 冷启动落进 exec 自动后台化窗口。建议后续把
"skill 自举 + marker" 写成 V2 时代的推荐做法（可另 PR 改 CLAUDE.md）。
- 发布：合入后打 `v0.6.18-beta.1` → 只发 staging registry；staging 上用
zooclaw-engine 的 cache-hit smoke 新增的 council 任务做组合验收后再 `-release`。
- 存量 V2 agent 靠 controld 的 skill refresh 扇出在下一 turn 拿到新版本。

相关 issue：SerendipityOneInc/ecap-skills#274（pdf / web-designer 同类
`../websearch` 死引用）、SerendipityOneInc/ecap-workspace#3623（Council UI 的
V2 接入）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01MwgVrFQHJ8XE89ZwSdAY14
```

### PR Body

## 背景

用户反馈 `/council` 在 V2（zooclaw-engine，E2B sandbox）上第一步（Stage 0 组阵容 → Stage 1 确认面板）从 V1 的 20–30s 退化到 8 分钟不出结果。根因（详见 zooclaw-engine 侧配套 PR 与 issue）：

1. `run_status.py` 用无超时阻塞 `fcntl.flock(LOCK_EX)` 串行化 6/8 个子命令；V2 的 exec 在 yield 窗口后自动后台化并保留进程 → 一个被后台化的持锁者让之后每条 run_status.py 永久阻塞。用户截图里 agent 自己在 `grep flock` / `ps aux | grep run_status` / 扫 `/proc`。
2. 每条命令都是 `uv run --with jsonschema …`：V2 不执行 skill 的 `install[]`，`uv run --with` 又不看模板已 bake 的 site-packages → 冷启动实测 12.1s，正好落进 yield 窗口。
3. Stage 0/1 是 6 条独立 exec；V2 每条 exec ≈ 一次 LLM 往返 + 一个 Temporal activity + 5 次 envd 往返（实测 1.15s 引擎侧固定开销）。

## 改动（6 个 commit 对应计划里的 PR-0…PR-5，可逐个 review）

| commit | 内容 |
|---|---|
| `ci(council)` | 新 `council-tests.yml`：PR 触碰 `council/**` 时跑 `pytest council/tests`（此前没有任何 CI 跑这些测试） |
| `fix(council): bounded flock` | `_locked` 改 `LOCK_EX\|LOCK_NB` + 15s deadline → 结构化 `LOCKED`；不删 `.lock`（删了会让第三个 opener 拿新 inode 双写）；flock 不支持的 FS 降级为无锁 + stderr 警告；`import jsonschema` 失败 → `MISSING_DEPENDENCY`（不再 traceback） |
| `perf(council): cap catalog fetch` | `roster.py` fetch 预算 3s×2 + 1s 退避 = 最坏 7s（< 10s 自动后台化窗口；原 36s） |
| `fix(council): degrade cost collection` | `swarm_usage.py --store-dir` 可选：显式 → `COUNCIL_USAGE_STORE_DIR` → 自动发现 `~/.openclaw/agents/*/sessions`；V2 没有 openclaw session store 时 success + `store:"unavailable"` + `total_credits:null`，SKILL.md 明说"未计量"，绝不报数 |
| `feat(council): self-bootstrap deps` | 新 `scripts/ensure_deps.py` + `_deps.py`（stdlib）：先 `find_spec` 探测，全在则零子进程零网络；缺的用 `uv pip install --target` / `pip --target` 装进 `~/.cache/council/deps/py3.x`，marker 放在安装目录内（同生共死、spec hash 变则重装）。之后所有脚本直接 `python3`；`requires.bins` → `["python3"]` |
| `feat(council): one-shot preflight` | 新 `scripts/preflight.py`：进程内串起 fetch → propose → premium alt → init → estimate → `awaiting_go`，一份 JSON 输出（同时写 `$RUN/preflight.json` 供 smoke 断言）。Stage 0/1 从 6 条 exec 变 **1 条**。SKILL.md 改写：全部 `python3 {baseDir}/scripts/…`、每条 exec 带 `timeout`、`ROOT="$(pwd -P)/council-runs"` + `BAD_RUN_ROOT` 守卫（平台契约 ask #2）、删掉未发布的 `../websearch` 引用；面板模板、门语义、Stage 5 K 行原文不动。新 `test_skill_md_contract.py` 钉住这些不变量 |

测试：330 passed（基线 275，+55）；`lint_skills.py` 通过；`sync-v2-registry.mjs --validate` 通过。冷路径实测：系统 python3（无 jsonschema）跑一条 `preflight.py`，971ms 自装 → `awaiting_go`，总 1.2s。

## V1/V2 中立

- SKILL.md 无 `uv run`、无 engine 路径；V1 pod 首次装进 `$HOME/.cache`（持久 FS）后跳过，V2 模板已 bake 则永不联网。
- run root 在 V1（`~/.openclaw/workspace/council-runs`）与 V2（`/workspace/council-runs`）都合法。
- `install[]` 原样保留（linter 要求非空，仅作文档）。

## 需要维护者注意

- 仓库 `CLAUDE.md` §3 写 "Prefer `uv run --with <deps>`"，本 PR 在 council 上反其道：原因是 V2 不执行 `install[]`、且 `uv run --with` 冷启动落进 exec 自动后台化窗口。建议后续把 "skill 自举 + marker" 写成 V2 时代的推荐做法（可另 PR 改 CLAUDE.md）。
- 发布：合入后打 `v0.6.18-beta.1` → 只发 staging registry；staging 上用 zooclaw-engine 的 cache-hit smoke 新增的 council 任务做组合验收后再 `-release`。
- 存量 V2 agent 靠 controld 的 skill refresh 扇出在下一 turn 拿到新版本。

相关 issue：SerendipityOneInc/ecap-skills#274（pdf / web-designer 同类 `../websearch` 死引用）、SerendipityOneInc/ecap-workspace#3623（Council UI 的 V2 接入）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01MwgVrFQHJ8XE89ZwSdAY14


---

## refactor(publish): retire v1 skill distribution (#273)

- **SHA**: `0a8011886e27688d7f3f1c83579d89849828618d`
- **作者**: kaka-srp
- **日期**: 2026-09-02T06:40:01Z
- **PR**: #273

### Commit Message

```
refactor(publish): retire v1 skill distribution (#273)

## Summary

- retire the legacy v1 S3/JuiceFS skill publication path
- publish staging and production exclusively through the v2 engine
registry
- remove the obsolete v1 allowlist and decouple v2 validation from it
- remove alpha/dev publication because that environment has no v2
registry configuration
- update publishing and review documentation to describe the v2-only
contract

## Validation

- `python3 .github/scripts/lint_skills.py`
- `pytest _BGM/tests/ -q`
- parsed `.github/workflows/publish-skills.yml` with PyYAML
- `node --check .github/scripts/sync-v2-registry.mjs`
- `PUBLISH_BASE_URL=https://example.invalid PUBLISH_TOKEN=test node
.github/scripts/sync-v2-registry.mjs --validate`
- `node .github/scripts/sync-v2-registry.mjs --dry-run`
- `git diff --check`

The dry-run validated all 21 v2-published skills with no upload guard
failures.
```

### PR Body

## Summary

- retire the legacy v1 S3/JuiceFS skill publication path
- publish staging and production exclusively through the v2 engine registry
- remove the obsolete v1 allowlist and decouple v2 validation from it
- remove alpha/dev publication because that environment has no v2 registry configuration
- update publishing and review documentation to describe the v2-only contract

## Validation

- `python3 .github/scripts/lint_skills.py`
- `pytest _BGM/tests/ -q`
- parsed `.github/workflows/publish-skills.yml` with PyYAML
- `node --check .github/scripts/sync-v2-registry.mjs`
- `PUBLISH_BASE_URL=https://example.invalid PUBLISH_TOKEN=test node .github/scripts/sync-v2-registry.mjs --validate`
- `node .github/scripts/sync-v2-registry.mjs --dry-run`
- `git diff --check`

The dry-run validated all 21 v2-published skills with no upload guard failures.


---

## feat(feishu): add managed document skills (#272)

- **SHA**: `d54fd1c60a8f59e92ad16d4a5e2cb92c85797bfc`
- **作者**: kaka-srp
- **日期**: 2026-09-02T02:55:35Z
- **PR**: #272

### Commit Message

```
feat(feishu): add managed document skills (#272)

## Linear

None — this cross-repository implementation was approved without a
Linear issue.

## Summary

- Add managed Skills for native Feishu Docx, Drive, Wiki, and permission
administration workflows.
- Gate the permission-management Skill on the Agent aggregate
`feishu.permission_admin_available` capability.
- Keep Provider execution and account-level authorization in ACS.

## Related work

- Design and ECAP integration:
https://github.com/SerendipityOneInc/ecap-workspace/pull/3605
- Engine contract/runner:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1078
- ACS execution/reconciliation:
https://github.com/SerendipityOneInc/agent-channel-service/pull/103

## Validation

- Repository Skill linter passed.
- The linter reports only 12 pre-existing warnings unrelated to these
Skills.

## Release order

Keep this PR in draft until the Engine contract and ACS execution path
are reviewed. Publish the Skills before enabling Staging reconciliation.
```

### PR Body

## Linear

None — this cross-repository implementation was approved without a Linear issue.

## Summary

- Add managed Skills for native Feishu Docx, Drive, Wiki, and permission administration workflows.
- Gate the permission-management Skill on the Agent aggregate `feishu.permission_admin_available` capability.
- Keep Provider execution and account-level authorization in ACS.

## Related work

- Design and ECAP integration: https://github.com/SerendipityOneInc/ecap-workspace/pull/3605
- Engine contract/runner: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1078
- ACS execution/reconciliation: https://github.com/SerendipityOneInc/agent-channel-service/pull/103

## Validation

- Repository Skill linter passed.
- The linter reports only 12 pre-existing warnings unrelated to these Skills.

## Release order

Keep this PR in draft until the Engine contract and ACS execution path are reviewed. Publish the Skills before enabling Staging reconciliation.


---
