---
title: "修复：多模型会审（council）标准档不再卡满 20 分钟超时，第三席换成更快的模型"
type: "Bug Fix"
priority: "中"
date: "2026-09-28"
status: "待审核"
channels: ""
---

# 修复：多模型会审（council）标准档不再卡满 20 分钟超时，第三席换成更快的模型

## 核心宣传点

标准档的多模型会审原先固定用 Gemini Flash 当第三位成员。实测中另两位成员早已交稿，整场会审却因为等这一席而撞到 20 分钟上限直接失败——它一个人发了 27 次请求、累计等待约 15 分钟，单次最长 168 秒。现在标准档改用 DeepSeek Flash，并优先取模型目录里的滚动别名，避免按版本号排序时选中已经下线的旧版本。其他档位和手动指定成员的用法不变；如果 Flash 系列在目录里不存在，标准档会像以前一样顺延到下一家厂商。

## 分级

- 内部：P1
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

Standard councils currently choose Gemini Flash as the third member. In staging workload run [36371165264](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/36371165264), Sonnet and Terra completed their reports, but the council hit its 20-minute cap waiting for Gemini 3.8 Flash. The member made 27 provider calls with about 15 minutes of cumulative latency (maximum 168 seconds).

Use DeepSeek Flash as the standard tier's representative instead. Prefer the catalog's rolling `deepseek-flash` alias when present so numeric version ordering cannot select the obsolete `deepseek-v4-flash-0731` ahead of it. Other tiers and manual casts retain their existing choices. If the Flash series is absent, standard casting proceeds to the next vendor as before.

Validation: all 393 council tests pass; skill lint passes (12 existing warnings); `git diff --check` passes. Regression coverage includes all three depths, coexistence with newer Gemini and dated DeepSeek aliases, absent Flash, and versioned-only Flash catalogs. The new alias passed a real staging billing/model preflight in [36371319552](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/36371319552).

The default Flash seat is priced from staging LiteLLM configuration observed on 2026-09-28: USD 0.22 input / 0.66 output per million tokens. Per-row provenance is retained. The follow-up pricing change passed 123 targeted roster/preflight/estimate tests, including a default-cast estimate with no unpriced participants.

## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- SHA: `db4a49faf8dd9f1164052c02129f28ce7793220e`
- PR: #288
- 作者：Chris@ZooClaw
- 日期：2026-09-28T03:45:20Z

### Commit Message

```
fix(council): use DeepSeek Flash for standard councils (#288)

Standard councils currently choose Gemini Flash as the third member. In
staging workload run
[36371165264](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/36371165264),
Sonnet and Terra completed their reports, but the council hit its
20-minute cap waiting for Gemini 3.8 Flash. The member made 27 provider
calls with about 15 minutes of cumulative latency (maximum 168 seconds).

Use DeepSeek Flash as the standard tier's representative instead. Prefer
the catalog's rolling `deepseek-flash` alias when present so numeric
version ordering cannot select the obsolete `deepseek-v4-flash-0731`
ahead of it. Other tiers and manual casts retain their existing choices.
If the Flash series is absent, standard casting proceeds to the next
vendor as before.

Validation: all 393 council tests pass; skill lint passes (12 existing
warnings); `git diff --check` passes. Regression coverage includes all
three depths, coexistence with newer Gemini and dated DeepSeek aliases,
absent Flash, and versioned-only Flash catalogs. The new alias passed a
real staging billing/model preflight in
[36371319552](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/36371319552).

The default Flash seat is priced from staging LiteLLM configuration
observed on 2026-09-28: USD 0.22 input / 0.66 output per million tokens.
Per-row provenance is retained. The follow-up pricing change passed 123
targeted roster/preflight/estimate tests, including a default-cast
estimate with no unpriced participants.
```

来源：SerendipityOneInc/ecap-skills @ db4a49fa，PR #288，作者 Chris@ZooClaw。
