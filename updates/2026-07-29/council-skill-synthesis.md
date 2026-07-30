---
title: "Council 研讨技能：新增「单专家主笔」合成、实时赛季/序列解析、论点处就地引用"
type: "Skill 上架/更新"
priority: "中"
date: "2026-07-29"
status: "待审核"
channels: ""
---

## 核心宣传点

Council 技能进一步打磨合成环节：由单一专家主笔统稿让报告更连贯、支持实时解析「本赛季/最新一期」等时间序列引用、把引用直接放在对应论点出处，减少「结论与出处对不上」的情况。

## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- commit：a0f3b96ee56441185be15672cfe026654280f14e
- PR：#246
- 日期：2026-07-29T08:25:58Z

### Commit message

```
feat(council): one-expert-author synthesis, live series resolution, at-claim-site citations (#246)

Three staging-driven improvements to the council skill (validated on
betas v0.6.12-beta.1–.5, bot 9d52c157).

## 1. Synthesize as one expert author (topic-matched persona, silent
consensus)

A real staging report spent ~30% of its body on meta-commentary
(methodology preamble, "四份分析高度一致" tags, per-section consensus grades).
Recast synthesis deep-research-style:

- Composer picks the expert whose judgment the topic deserves and writes
the whole report in that voice; the reader must never sense assembly
from multiple reports — consensus tags/counts forbidden.
- Claim map demoted to private bookkeeping (travels only in the
machine-read `council_analysis` fence).
- Calibration survives quietly: contradictions still present both sides
(analyst voice), single-source hedges only on load-bearing claims,
compact blind-spots section near the end.
- Reviser gains a voice hunt; composer + fallback `_SYNTHESIS_TEMPLATE`
edited in lockstep, now **drift-gated by CI**
(`test_composer_md_and_fallback_template_share_rules_1_to_6`).

## 2. Live series version resolution — series_latest pins removed

Staging caught the pinned map's blind spot: `claude-opus-5` was live on
litellm but the standard chair kept resolving the hand-declared pin
(`claude-opus-4-8`) — removals fail loud, arrivals told no one. User
decision: version bumps must cost zero maintenance.

- `--propose-cast` resolves each preset series against the pod's per-run
litellm catalog by version-free signature (`series_of`): newest version
wins, stable ahead of prerelease at equal version.
- Line tokens survive the signature, so `flash-lite` never masquerades
as `flash`; a non-version suffix (`-thinking`/`-mini`) is a product-line
variant by design — seat skips visibly, remedy is a one-line
`SERIES_STEMS` entry (adjudicated; asserted explicitly in tests).
- `series_latest` deleted from `price_snapshot.json` (prices only); a
version newer than the snapshot seats unpriced until `--refresh-prices`.
Design doc §9.8 records the reversal of §9.6.

## 3. Citations at the claim site

Staging report had a Sources bank but almost no in-text citations.
Restored the #126/D12-strength mandate in all three templates (member,
composer, fallback): every key claim carries an inline markdown-link
citation at the claim site — a trailing Sources list alone is NOT
citation; reviser hunts uncited key claims.

## Review trail

9 bot review rounds. Both codex P1s adjudicated: opus-pin concern
superseded by live resolution; non-version-suffix boundary is the
documented, user-decided design (final claude verdict: severity NONE,
"Both prior P1s resolved"). `need-human-review` labels removed after
adjudication comment.

## Testing

- `uv run --with pytest,pyyaml,jsonschema -m pytest council/tests/` —
271 passed.
- End-to-end against the real staging catalog (39 ids):
economy/standard/premium casts all resolve correctly (standard chair =
claude-opus-5); image/video/wrapper ids excluded.
- Staging betas .1–.5 published for live validation.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01THqUHU4BtCMq7xLxE7ZPKa

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR body

Three staging-driven improvements to the council skill (validated on betas v0.6.12-beta.1–.5, bot 9d52c157).

## 1. Synthesize as one expert author (topic-matched persona, silent consensus)

A real staging report spent ~30% of its body on meta-commentary (methodology preamble, "四份分析高度一致" tags, per-section consensus grades). Recast synthesis deep-research-style:

- Composer picks the expert whose judgment the topic deserves and writes the whole report in that voice; the reader must never sense assembly from multiple reports — consensus tags/counts forbidden.
- Claim map demoted to private bookkeeping (travels only in the machine-read `council_analysis` fence).
- Calibration survives quietly: contradictions still present both sides (analyst voice), single-source hedges only on load-bearing claims, compact blind-spots section near the end.
- Reviser gains a voice hunt; composer + fallback `_SYNTHESIS_TEMPLATE` edited in lockstep, now **drift-gated by CI** (`test_composer_md_and_fallback_template_share_rules_1_to_6`).

## 2. Live series version resolution — series_latest pins removed

Staging caught the pinned map's blind spot: `claude-opus-5` was live on litellm but the standard chair kept resolving the hand-declared pin (`claude-opus-4-8`) — removals fail loud, arrivals told no one. User decision: version bumps must cost zero maintenance.

- `--propose-cast` resolves each preset series against the pod's per-run litellm catalog by version-free signature (`series_of`): newest version wins, stable ahead of prerelease at equal version.
- Line tokens survive the signature, so `flash-lite` never masquerades as `flash`; a non-version suffix (`-thinking`/`-mini`) is a product-line variant by design — seat skips visibly, remedy is a one-line `SERIES_STEMS` entry (adjudicated; asserted explicitly in tests).
- `series_latest` deleted from `price_snapshot.json` (prices only); a version newer than the snapshot seats unpriced until `--refresh-prices`. Design doc §9.8 records the reversal of §9.6.

## 3. Citations at the claim site

Staging report had a Sources bank but almost no in-text citations. Restored the #126/D12-strength mandate in all three templates (member, composer, fallback): every key claim carries an inline markdown-link citation at the claim site — a trailing Sources list alone is NOT citation; reviser hunts uncited key claims.

## Review trail

9 bot review rounds. Both codex P1s adjudicated: opus-pin concern superseded by live resolution; non-version-suffix boundary is the documented, user-decided design (final claude verdict: severity NONE, "Both prior P1s resolved"). `need-human-review` labels removed after adjudication comment.

## Testing

- `uv run --with pytest,pyyaml,jsonschema -m pytest council/tests/` — 271 passed.
- End-to-end against the real staging catalog (39 ids): economy/standard/premium casts all resolve correctly (standard chair = claude-opus-5); image/video/wrapper ids excluded.
- Staging betas .1–.5 published for live validation.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01THqUHU4BtCMq7xLxE7ZPKa
