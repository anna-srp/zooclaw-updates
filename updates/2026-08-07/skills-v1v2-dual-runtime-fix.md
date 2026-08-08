---
title: "已发布技能在新运行时的兼容与凭据安全修复"
type: "Bug Fix"
priority: "高"
date: "2026-08-07"
status: "待审核"
channels: ""
---

## 核心宣传点

修复浏览器等技能在新一代运行时因路径写死而失效的问题，并清理了误提交的凭据文件，技能在新旧环境都能稳定运行。

## 原始内容

### fix: v1/v2 dual-runtime hardening for published skills (#251)

- SHA: `9bb726a27f7f78560988051934544b4bd39e1880`
- 仓库: 见 raw/2026-08-07

**Commit Message:**

```
fix: v1/v2 dual-runtime hardening for published skills (#251)

## What changed

- browser-skill: remove the git-tracked `.state.json` (contained a live
user JWT) and ignore it going forward; all invocation paths switch from
cwd-relative `node skills/browser-skill/...` to `{baseDir}/...`; the MCP
endpoint becomes overridable via `BROWSER_SKILL_MCP_URL`, and an
explicit env value now always wins over an endpoint persisted in the
state file.
- deep-research / ecap-io: drop dead `install: litellm` entries (neither
skill has scripts; `install: []` is the sanctioned form).
- xlsx: convert all `SKILL_DIR/` placeholders to `{baseDir}/` in
SKILL.md and every references/*.md.
- pptx: replace `~/.claude/skills/...` example paths in
references/shape-cli.md with the `{baseDir}` convention.
- CLAUDE.md + code-review.md: add v1/v2 dual-runtime compatibility rules
and a matching review checklist (path discipline via `{baseDir}`,
env-declared endpoints only, no committed credentials/state, skill dir
read-only at runtime, ≤50 MiB per skill, LFS hydration, both publish
whitelists considered).

## Why

v2 (zooclaw-engine) materializes skills content-addressed at
`/skills/{name}/` with v1-compat symlinks. Most skills port cleanly, but
cwd-relative paths, v1-mount hardcodes, and writable-skill-dir
assumptions silently break. These are the mechanical fixes; the
governance sections make dual-runtime compatibility a check-in
requirement so future skills stay portable.

## Impact

No behavior change in v1: `{baseDir}` is substituted by both runtimes,
and the browser-skill endpoint default is byte-identical when
`BROWSER_SKILL_MCP_URL` is unset.

## Security note (action required)

`browser-skill/.state.json` contained a live Bearer JWT (allenz@srp.one,
exp 2027-02). Deleting the file does not revoke it and it remains in git
history — **the token must be rotated out-of-band**.

## Validation

- `python3 .github/scripts/lint_skills.py` — all skills pass, 12
pre-existing warnings, none introduced
- `node --check` on both browser-skill scripts
- `grep` confirms zero remaining `node skills/browser-skill` refs, zero
`SKILL_DIR`, no tracked `.state.json`

## Related

- v2 registry sync + `PUBLISHED_SKILLS_V2` allowlist: #249
- Engine auto-assembly switch: SerendipityOneInc/zooclaw-engine (PR from
`feat/global-skills-auto-enable-switch`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01YSusgGXGYznJqAyiHnDyNz
```

**PR Body:**

## What changed

- browser-skill: remove the git-tracked `.state.json` (contained a live user JWT) and ignore it going forward; all invocation paths switch from cwd-relative `node skills/browser-skill/...` to `{baseDir}/...`; the MCP endpoint becomes overridable via `BROWSER_SKILL_MCP_URL`, and an explicit env value now always wins over an endpoint persisted in the state file.
- deep-research / ecap-io: drop dead `install: litellm` entries (neither skill has scripts; `install: []` is the sanctioned form).
- xlsx: convert all `SKILL_DIR/` placeholders to `{baseDir}/` in SKILL.md and every references/*.md.
- pptx: replace `~/.claude/skills/...` example paths in references/shape-cli.md with the `{baseDir}` convention.
- CLAUDE.md + code-review.md: add v1/v2 dual-runtime compatibility rules and a matching review checklist (path discipline via `{baseDir}`, env-declared endpoints only, no committed credentials/state, skill dir read-only at runtime, ≤50 MiB per skill, LFS hydration, both publish whitelists considered).

## Why

v2 (zooclaw-engine) materializes skills content-addressed at `/skills/{name}/` with v1-compat symlinks. Most skills port cleanly, but cwd-relative paths, v1-mount hardcodes, and writable-skill-dir assumptions silently break. These are the mechanical fixes; the governance sections make dual-runtime compatibility a check-in requirement so future skills stay portable.

## Impact

No behavior change in v1: `{baseDir}` is substituted by both runtimes, and the browser-skill endpoint default is byte-identical when `BROWSER_SKILL_MCP_URL` is unset.

## Security note (action required)

`browser-skill/.state.json` contained a live Bearer JWT (allenz@srp.one, exp 2027-02). Deleting the file does not revoke it and it remains in git history — **the token must be rotated out-of-band**.

## Validation

- `python3 .github/scripts/lint_skills.py` — all skills pass, 12 pre-existing warnings, none introduced
- `node --check` on both browser-skill scripts
- `grep` confirms zero remaining `node skills/browser-skill` refs, zero `SKILL_DIR`, no tracked `.state.json`

## Related

- v2 registry sync + `PUBLISHED_SKILLS_V2` allowlist: #249
- Engine auto-assembly switch: SerendipityOneInc/zooclaw-engine (PR from `feat/global-skills-auto-enable-switch`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01YSusgGXGYznJqAyiHnDyNz


