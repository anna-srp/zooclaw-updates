---
title: "fix(council): explicitly dispatch cast models to subagents (#287)"
type: "Bug Fix"
priority: "中"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# 修复：Council 会按 cast 指定的模型派发子会话

## 核心宣传点

此前在 DeepSeek 下，Council 可能在不带 model 的情况下创建所有子会话，导致每个席位都继承了驱动模型，即使 cast.json 和 ledger 里写的是不同模型——也就是说你以为开了一场多模型圆桌，实际上是同一个模型自说自话。现在成员、composer、修订者和重试都必须在 sessions_spawn.model 里带上确切的 cast 模型；派发前检查 spawn 回执、保留完整 session key，模型不匹配的子会话会直接暴露为派发失败，而不是顶着别人的名字被采纳。不匹配的席位会记录请求/实际模型证据并失败，同时跳过计价用量统计。

## 分级

- 内部：P2
- 外部：C
- 发布状态：未知

## PR 说明

DeepSeek could spawn every council child without `model`, so all seats inherited the driver even though cast.json and the ledger named different models (SerendipityOneInc/zooclaw-engine#1339).

Require the exact cast model in `sessions_spawn.model` for members, the composer, revisers, and retries. Put JSON tool-call envelopes next to the loaded templates, check spawn receipts before accepting work, and preserve complete session keys. A mismatched child is disclosed as a dispatch failure instead of being accepted under another model's name.

The mismatch recovery path records the returned full session key under the requested cast seat, then fails that seat with the requested/served model evidence. It avoids out-of-cast ledger rejection and skips priced usage collection for mismatched or unconfirmed dispatches.

A live DeepSeek run also exposed omitted `agent:` prefixes in otherwise complete Engine session keys. Normalize only the recognized `agt_<id>:subagent:<UUID>` abbreviation when recording a spawn, and reject short/full duplicates (including old abbreviated entries). Preserve other runtimes' session IDs and existing ledger rows.

Validation: dispatch-envelope regression failed before the instructions fix. Four session-key regression cases failed before the runtime fix; 154 focused ledger/usage tests and all 388 council tests pass afterward, including CI. Skill lint passes. Engine receipt format was verified in source.

Staging uses Engine beta.3 without overwriting the other deployment. Council@11 live Terra smoke succeeded ([run](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/35496342780)); DeepSeek explicitly dispatched Sonnet/Terra/Gemini members and Opus synthesis but failed the product check because of shortened ledger keys ([run](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/35495865807)). Both completed their reports. Friendly report filenames produce a nonblocking warning. Final commit b09a910 is published as council@12. The corrected DeepSeek rerun succeeded ([run](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/35496936569)): 3/3 members done, 4 spawns ledgered and matched, all execution/behavior/model checks pass, prefix reuse 100%, cache read 95.6%, first drift stable. Product verdict is WARN only for the final reply not naming the literal run directory or report.md. Council cache metrics are record-only by the existing smoke design. Terra was validated on council@11; the narrow v12 key normalization is covered by the regression suite and the final DeepSeek run. No production skill publication.

Refs SerendipityOneInc/zooclaw-engine#1339


## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- SHA: `62b7f360fb44e87dab19164faf5fdec816af8f12`
- PR: #287
- 作者：Chris@ZooClaw
- 日期：2026-09-20T08:04:41Z

### Commit Message

```
fix(council): explicitly dispatch cast models to subagents (#287)

DeepSeek could spawn every council child without `model`, so all seats
inherited the driver even though cast.json and the ledger named
different models (SerendipityOneInc/zooclaw-engine#1339).

Require the exact cast model in `sessions_spawn.model` for members, the
composer, revisers, and retries. Put JSON tool-call envelopes next to
the loaded templates, check spawn receipts before accepting work, and
preserve complete session keys. A mismatched child is disclosed as a
dispatch failure instead of being accepted under another model's name.

The mismatch recovery path records the returned full session key under
the requested cast seat, then fails that seat with the requested/served
model evidence. It avoids out-of-cast ledger rejection and skips priced
usage collection for mismatched or unconfirmed dispatches.

A live DeepSeek run also exposed omitted `agent:` prefixes in otherwise
complete Engine session keys. Normalize only the recognized
`agt_<id>:subagent:<UUID>` abbreviation when recording a spawn, and
reject short/full duplicates (including old abbreviated entries).
Preserve other runtimes' session IDs and existing ledger rows.

Validation: dispatch-envelope regression failed before the instructions
fix. Four session-key regression cases failed before the runtime fix;
154 focused ledger/usage tests and all 388 council tests pass afterward,
including CI. Skill lint passes. Engine receipt format was verified in
source.

Staging uses Engine beta.3 without overwriting the other deployment.
Council@11 live Terra smoke succeeded
([run](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/35496342780));
DeepSeek explicitly dispatched Sonnet/Terra/Gemini members and Opus
synthesis but failed the product check because of shortened ledger keys
([run](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/35495865807)).
Both completed their reports. Friendly report filenames produce a
nonblocking warning. Final commit b09a910 is published as council@12.
The corrected DeepSeek rerun succeeded
([run](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/35496936569)):
3/3 members done, 4 spawns ledgered and matched, all
execution/behavior/model checks pass, prefix reuse 100%, cache read
95.6%, first drift stable. Product verdict is WARN only for the final
reply not naming the literal run directory or report.md. Council cache
metrics are record-only by the existing smoke design. Terra was
validated on council@11; the narrow v12 key normalization is covered by
the regression suite and the final DeepSeek run. No production skill
publication.

Refs SerendipityOneInc/zooclaw-engine#1339
```

来源：SerendipityOneInc/ecap-skills @ 62b7f360，PR #287，作者 Chris@ZooClaw。