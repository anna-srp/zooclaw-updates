---
title: "Agent Studio：修复模板配置检查逻辑"
type: "Bug Fix"
priority: "中"
date: "2026-05-25"
status: "待审核"
channels: ""
---

# Agent Studio：修复模板配置检查逻辑

## 核心宣传点

修复 Agent Studio 模板中配置检查可能依赖缓存记忆而非实际文件的问题，提升稳定性

## 原始内容

**仓库**: SerendipityOneInc/ecap-agent-pack  
**Commit**: 090da3a156af5608e009642f4d3bd128ee7781b9  
**作者**: felix-srp  
**日期**: 2026-05-25T14:13:53Z  

**Commit Message**:

```
fix(agent-studio): forbid memory-only onboarding config check in templates (#144)

* fix(agent-studio): forbid memory-only onboarding config check in templates

Scaffolded packs were instructed to "check" `data/config.json` with
hints like `ls data/config.json` and `ls data/config.json 2>/dev/null`,
but the wording never forbade the model from claiming the result from
memory. In production this led to an agent telling the user "我看了
一下，data/config.json 已经存在" without ever invoking a tool, then
having to apologize and restart onboarding mid-conversation — either
re-onboarding returning users or silently skipping new ones.

- BOOTSTRAP.md.tmpl Step 2: require an actual Bash `test -f ...` or
  Read call; explicitly name the hallucination and the two failure
  modes it causes.
- AGENTS.md.tmpl Step 5: same guardrail.
- agent-pack.yaml: bump 1.3.3 → 1.3.4.

Existing packs (e.g. video-duplicate) need re-scaffolding or a
hand-patch to inherit the guardrail; this commit only fixes the
template so newly generated packs are protected.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(agent-studio): propagate config-check guardrail to automation spec; trim templates

Code-review caught two follow-ups to the previous template fix:

1. references/automation.md §"Required sections" is the Stage 3a spec
   the Studio LLM reads when writing a new pack's AGENTS.md. It still
   said `ls data/config.json missing → trigger pack-onboarding`, so
   Studio would write the unguarded form into generated packs even
   with the template updated — the template fix would not actually
   reach end-user packs.

2. The template wording was ~30-40 tokens longer than necessary in
   both files. The bolded prohibition + the concrete command carry
   the guardrail; the quoted hallucination example and the
   failure-mode explainer were motivational, not load-bearing. Also
   replaced "Read errors with ENOENT" (Claude Code's Read tool
   surfaces a human-readable error, not a literal errno).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Summary

- BOOTSTRAP.md.tmpl Step 2 and AGENTS.md.tmpl Step 5 previously hinted at \`ls data/config.json\` but never forbade the model from claiming the check result from memory. In production an agent did exactly that — said \"我看了一下，data/config.json 已经存在\" without invoking a tool, then apologized and restarted onboarding mid-conversation.
- Both templates now require an actual Bash \`test -f …\` or Read call and explicitly name the hallucination and the two failure modes (re-onboarding returning users / silently skipping new ones).
- agent-pack.yaml: 1.3.3 → 1.3.4.

Existing packs (e.g. video-duplicate) need re-scaffolding or a hand-patch to inherit the guardrail; this PR only fixes the template so newly generated packs are protected.

## Test plan

- [ ] Render a new pack via agent-studio and confirm the generated BOOTSTRAP.md / AGENTS.md contain the new guardrail wording.
- [ ] Spot-check that the new wording doesn't break existing pack-onboarding behavior on a returning user (config.json present).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
