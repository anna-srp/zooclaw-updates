---
title: "Agent Builder 新增实时模型选择器"
type: "新功能上线"
priority: "高"
date: "2026-07-23"
status: "待审核"
channels: ""
---

## 核心宣传点

在 Agent Builder 里现在可以直接从顶部选择器切换对话模型了——支持常规模型和 Agent Studio 专属折扣模型（带本地化折扣标签），点「应用」即时生效，无需重启项目。切换会显示 激活/等待/错误 状态，未提交的草稿在切换项目时自动丢弃，确认过的模型选择会绑定到对应的 Builder 计算环境。旧版 Claw 会提示"升级 Claw 后可选模型"。

## 原始内容

**PR #2997 — feat(agent-builder): add live model selector**
SHA: 256022ad8c6e4bcc4cc2ef7d2911b819fdd9120d ｜ 作者: rayrain-srp ｜ Linear: ECA-1281

- add a Builder-only chat model resolver that preserves the existing main-chat filtering while exposing entitled ordinary and `agent-studio-*` discounted models
- add shared Builder-computer GET/PUT model state APIs backed by the atomic FastClaw agent-model patch, exact runtime capability marker, bounded active-convergence polling, and a default-on kill switch
- add the Agent Builder header selector with explicit Apply, active/pending/error states, shared-runtime cache scope, localized discount labels, and no restart flow
- seed the official Agent Studio model only on first install when its explicit primary is missing; project open/update never reconciles over a user's selection
- harden independent rollout and transport edges: old-backend 404 hides the selector, FastClaw envelope conflicts stay non-retryable, and only the idempotent agent-model PATCH opts into one zero-byte disconnect replay
- preserve existing runtime-status soft-error envelopes while the new capability gate still fails closed, and classify transient runtime errors separately from old-image marker gaps
- make the old-image state actionable and fully visible: the disabled control now says `Upgrade Claw to select` / `升级 Claw 后可选模型` in a compact, non-truncating caution style
- discard any unsubmitted model draft when navigating between projects, while keeping the confirmed model cache scoped to their shared Builder computer

`AGENT_BUILDER_MODEL_SELECTOR_ENABLED` defaults to `true`; operators can set it to `false` as an emergency kill switch.

依赖：merged `zooclaw-extras#190` 和 `fastclaw#161`（staging release + 功能验证完成）。
