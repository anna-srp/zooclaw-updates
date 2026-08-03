---
title: 新增 cron-job Skill：一条命令可靠地创建/更新定时任务
type: Skill 上架/更新
priority: 高
外部: "B"
date: 2026-07-27
status: 待审核
channels: ""
---

## 核心宣传点

新增 cron-job Skill：让 Agent 用一条命令就能安全、可靠地创建或更新你的定时任务（Cron）。它会先诊断请求、跑隔离测试、逐条核对你声明的产出与投递结果，只有全部通过后才真正写入调度器——从此告别"定时任务悄悄失败几周没人发现""跑成功了但结果根本没出来"这类坑，更新已有任务也绝不会把正在运行的定时任务悄悄关掉。

## 原始内容

### PR #240 feat(cron-job): add cron-job skill with safe create/update workflow driver

feat(cron-job): add cron-job skill with safe create/update workflow driver (#240)

## What

New `cron-job` skill: a single deterministic driver that turns a small agent-authored request into a reliably created or updated OpenClaw cron job. Driven by the 2026-07-20 production cron audit (536 bots / 153 jobs): vague keepalive payloads, jobs failing silently for weeks with no failure alert, and "success" runs whose declared outcome never materialized.

This is the v2 architecture: earlier revisions of this branch shipped a 7-script pipeline with a large fixture corpus; it has been deliberately collapsed into one workflow driver plus one thin gateway adapter (6 files, ~1.2k lines) so the agent surface is a single command.

## How it works

The agent copies `assets/cron-request.template.json`, fills in `task` (goal, `command` or `agentMessage`, schedule, observable `outcomes`, delivery, optional matching `controls`), and runs exactly one driver:

```bash
python3 {baseDir}/scripts/cron_workflow.py <request> --output <result>
```

`cron_workflow.py` owns the safety sequence:

1. **Diagnose** — validates the request and separates genuinely user-owned gaps (goal, timezone, one-shot time, recipient, failure owner) into a `needs_user` question list from agent-fixable issues (`needs_agent`). No scheduler write happens on either.
2. **Controls** — for matching/classification commands, runs independently authored positive and split-record negative fixtures natively and requires exact expected output.
3. **Isolated test** — through `cron_gateway.mjs` (loopback-only Gateway adapter, env-inherited `GATEWAY_TOKEN`, never in argv), adds a uniquely named disabled copy, force-runs it once, waits for the terminal run record, and always removes the copy (cleanup failures are reported alongside the primary error, never masking it).
4. **Verify** — checks every declared outcome assertion (`equals` / `contains` / `arrayValues` / `exists`) against the produced files, and verifies delivery: announce via run history, webhook via a correlated receipt read on the caller's declared same-origin receiver (with the mandatory `ecap-skill/1.0` User-Agent).
5. **Apply** — only after all checks pass: `cron.add` for new jobs (duplicate-name guarded) or `cron.update` for `existingJobId` (guarded by `updatedAtMs` optimistic concurrency), then re-reads and field-compares the live job.

Activation is one-way: `activateAfterValidation:true` enables after a verified test; `false`/omitted creates new jobs disabled and **preserves an existing job's enabled state** on update — an update can never silently disable a live cron.

## Testing

- `python3 cron-job/scripts/cron_workflow.py --self-test` → 15 assertions (schedule diagnosis, outcome assertions, vague-goal gating, enabled-state preservation).
- `node cron-job/scripts/cron_gateway.mjs --self-test` → arg parsing, job canonicalization, runtime resolution (requires installed openclaw).
- `python3 .github/scripts/lint_skills.py` → pass, zero warnings for this skill.
- CodeQL: clean (0 open alerts on this branch).

## Notes

- Not added to `PUBLISHED_SKILLS` — distribution is a separate decision.
- `requires`: `bins: [python3, node, openclaw]`, `env: [GATEWAY_TOKEN]`; `.env.example` documents the platform-injected variables.
- `references/openclaw-cron-model.md` records the 2026.6.11 runtime facts the driver depends on.

### PR #241 fix(cron-job): validate outbound message routing

新增结构化 `messageRouting` 契约，覆盖执行上下文、业务收件人、测试 sink、完成投递与跨 provider 授权；调度器写入前要求用户逐条确认收件路由；`delivery.mode:none` 任务钉死到声明的执行上下文；一次性测试运行用合成 sink 替换所有真实收件人与执行目标并禁用生产失败告警；写入前核对 run-log `messageToolSentTo` 与声明测试路由完全一致；拒绝隐藏字面收件人、未知/重复占位符、不兼容的 webhook/announce 上下文与未授权跨 provider 路由。

### PR #242 refactor(cron-job): use the built-in cron workflow

改为通过 OpenClaw 内置 `cron` 工具读写调度器，仅生成 `agentTurn` 类型任务；确定性准备、测试证据与最终校验仍在本地 driver 中；测试证据绑定到任务与运行标识、隔离测试告警、并对照最新调度器快照校验更新。self-test 93 断言通过；全新 stagingbot + A102 devcontainer E2E 全项通过（环境有效性、工作流完成、93/93 运行时 QA、业务验收）。
