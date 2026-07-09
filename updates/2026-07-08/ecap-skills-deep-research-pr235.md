---
title: "Deep Research 深度研究技能对齐 Anthropic 多智能体研究实践"
type: "Skill 上架/更新"
priority: "中"
date: "2026-07-08"
status: "待审核"
channels: ""
---

# Deep Research 深度研究技能对齐 Anthropic 多智能体研究实践

## 核心宣传点

深度研究技能借鉴了 Anthropic 多智能体研究系统的四项实践改进，研究任务的规划与执行更严谨、结果更可靠。

## 原始内容

```
feat(deep-research): borrow 4 upstream improvements from Anthropic's multi-agent research system (#235)

## Summary

Syncs `deep-research/SKILL.md` with the four genuine gaps found in a
full compare against Anthropic's [How we built our multi-agent research
system](https://www.anthropic.com/engineering/multi-agent-research-system).
deep-research was already ~80% aligned (and *more* developed than the
public write-up on collect-by-reference and source escalation); these
are the real deltas. Each is a small edit, not a rewrite.

Design doc:
`design-doc/ecap-agent-pack/researcher/2026-07-08-deep-research-upstream-borrows.md`
(deep-research is synced by hand, owned separately from the researcher
pack).

## Changes (borrows)

| # | Borrow | Where |
|---|--------|-------|
| 1 | **Per-investigator tool-call budget** | New `Tool calls /
investigator` column in Depth Modes (`~3–8` / `~8–12` / `~12–20`),
restated at dispatch beside the digest budget so investigators
self-calibrate effort |
| 2 | **Non-overlapping task boundaries** | Partition-check before
dispatch in *One question per investigator* — questions cover every
framework dimension without overlap |
| 3 | **Ranking ≠ authority** | New Anti-Pattern — SEO content farms
outrank authoritative primary sources; grade on the source, not the rank
|
| 4 | **Citation-drift self-check** | Synthesis spot-checks each key
claim's stated strength against its on-disk dossier (no re-fetch);
catches synthesis inflating MEDIUM→HIGH or hedged→flat |

## Surgical-scope notes
- Table edit **only adds the column** — kept `standard (default)` and
the full `deep` Analysis cell (the design doc's abbreviated table was
illustrating the new column, not mandating deletions).
- Tool-call-budget restate landed in the one place the skill already
lists dispatch-restated items (*Collect by reference*), keeping that
rule in a single home.

## Follow-up trim (separate commit)
A `trim-md` pass over the same file removed ~30 tok (−1.0%) of
pure-flavor / restated-redundancy prose — dual-reviewed (claude +
codex), zero behavioral constraint lost. Verdict: *trimmed out*. The
version-provenance HTML comment (~85 tok) was deliberately kept (pins
the 6K/24K caps to a runtime version + re-verify instruction).

## Deliberately not borrowed (per design doc)
Lead-plan checkpointing to Memory (low value at our run lengths) · the
full separate CitationAgent pass (belongs to council, not here) ·
platform infra (rainbow deploys, tracing, self-improving-prompt loop).

## Verification
- `.github/scripts/lint_skills.py` → **All skills passed**; no new
warnings for deep-research.
- Codex review → **APPROVE, no findings** on both the borrows and the
trim.
- Frontmatter / install / env untouched — pure prose additions to the
skill body.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01F3Ya7rTNnkYGPyMidZmVAC

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---

**PR Description:**

## Summary

Syncs `deep-research/SKILL.md` with the four genuine gaps found in a full compare against Anthropic's [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system). deep-research was already ~80% aligned (and *more* developed than the public write-up on collect-by-reference and source escalation); these are the real deltas. Each is a small edit, not a rewrite.

Design doc: `design-doc/ecap-agent-pack/researcher/2026-07-08-deep-research-upstream-borrows.md` (deep-research is synced by hand, owned separately from the researcher pack).

## Changes (borrows)

| # | Borrow | Where |
|---|--------|-------|
| 1 | **Per-investigator tool-call budget** | New `Tool calls / investigator` column in Depth Modes (`~3–8` / `~8–12` / `~12–20`), restated at dispatch beside the digest budget so investigators self-calibrate effort |
| 2 | **Non-overlapping task boundaries** | Partition-check before dispatch in *One question per investigator* — questions cover every framework dimension without overlap |
| 3 | **Ranking ≠ authority** | New Anti-Pattern — SEO content farms outrank authoritative primary sources; grade on the source, not the rank |
| 4 | **Citation-drift self-check** | Synthesis spot-checks each key claim's stated strength against its on-disk dossier (no re-fetch); catches synthesis inflating MEDIUM→HIGH or hedged→flat |

## Surgical-scope notes
- Table edit **only adds the column** — kept `standard (default)` and the full `deep` Analysis cell (the design doc's abbreviated table was illustrating the new column, not mandating deletions).
- Tool-call-budget restate landed in the one place the skill already lists dispatch-restated items (*Collect by reference*), keeping that rule in a single home.

## Follow-up trim (separate commit)
A `trim-md` pass over the same file removed ~30 tok (−1.0%) of pure-flavor / restated-redundancy prose — dual-reviewed (claude + codex), zero behavioral constraint lost. Verdict: *trimmed out*. The version-provenance HTML comment (~85 tok) was deliberately kept (pins the 6K/24K caps to a runtime version + re-verify instruction).

## Deliberately not borrowed (per design doc)
Lead-plan checkpointing to Memory (low value at our run lengths) · the full separate CitationAgent pass (belongs to council, not here) · platform infra (rainbow deploys, tracing, self-improving-prompt loop).

## Verification
- `.github/scripts/lint_skills.py` → **All skills passed**; no new warnings for deep-research.
- Codex review → **APPROVE, no findings** on both the borrows and the trim.
- Frontmatter / install / env untouched — pure prose additions to the skill body.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01F3Ya7rTNnkYGPyMidZmVAC
```
