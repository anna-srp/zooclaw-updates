# ecap-agent-pack — 2026-05-18 Commits

## Commit 1: 6a9d57c8 — feat(pptx-master): upgrade to SlideForge 1.0.0 (#131)

- **SHA**: 6a9d57c8e59b6f3b9e6e34dca78f2b5baf1016bd
- **Author**: vincent-srp
- **Date**: 2026-05-18T20:51:27Z
- **PR**: #131

### PR #131 Body

**Summary**
- 把 `build/slideforge-1.0.0.tar.gz` 解包覆盖到 `pptx-master/`（`agentPack_id=pptx-master` 不变，pack 内部已重塑为 **SlideForge**）。
- 从 v0.1.0（单个 `pack-onboarding` skill）升级到 v1.0.0：16 个 skills（`ppt-beautify` / `output-html` / `output-pptx` / `output-pdf` / `output-image` / `brand-system`（73+ 品牌）/ `marp-slides`（22 examples）/ `deep-research` / `designer` / `data-viz` / `narrative` / `review` / `rehearsal` / `citation` / `websearch` / `onboarding`），HTML §7B PPTX-Ready 统一输出，三阶段设计流（template matching → Design DNA → 8-dim Design Critic）。
- `agent-pack.yaml` 中 `name: slideforge`，`description.json` 中 `agentPack_id: pptx-master`——目录/品牌名/平台 id 三者解耦，有意保留。

**Test plan**
- OpenClaw bot 装载 pack 后 onboarding flow 正常
- 默认 HTML 输出 < 30s 跑通快速路径（output-html §7B）
- PPTX / PDF / Image 三条输出管线分别冒烟
- brand-system 在用户上传品牌手册场景下正常匹配

---

## Commit 2: 535a7f9f — feat(agent-studio): multi-agent workflow via snapshots (/studio list, /studio open) (#130)

- **SHA**: 535a7f9f2162edcc7395102daf917bca4518fdec
- **Author**: felix-srp
- **Date**: 2026-05-18T08:03:36Z
- **PR**: #130

### PR #130 Body

**Summary**

- Adds `snapshots/<name>/` sibling to `zip/` so one Agent Studio workspace can host **all** of a creator's packs.
- New commands: **`/studio list`** (enumerate previously built packs with stage + last-touched + bio) and **`/studio open [<name>]`** (resume any pack — workspace fully restored, with Studio's narrative `context.md` intact).
- Three snapshot triggers, all explicit (no silent disk growth): `/studio publish` success · `/studio new` with dirty workspace · `/studio open` with dirty workspace.

**What changes for creators**

- **Before:** building a new pack required `/studio new`, which wiped the workspace and lost the prior pack's editable state.
- **After:** `/studio list` shows everything you've built. `/studio open <name>` brings back the editable workspace and Studio's narrative memory.

**Architecture**

```
snapshots/
  <pack-name>/
    context.md             ← live narrative, Studio-rewritten at each gate
    <version>/             ← editable form (one per delivered/draft version)
      agent/ skills/ scripts/ data/
      context.md           ← frozen archival copy at publish time
```

---

## Commit 3: fb24dc4a — feat: add coros-coach and fitbeing-health-agent packs (#128)

- **SHA**: fb24dc4a3a354a6e9bb5af384aae52fd959aaa8f
- **Author**: Nemo Feng
- **Date**: 2026-05-18T07:14:04Z
- **PR**: #128

### PR #128 Body

**Summary**
- **coros-coach** — Personal health & training coach powered by the COROS MCP. Region-aware OAuth, morning/noon/evening roundups, on-demand HTML dashboards, and coaching answers grounded in sleep / HRV / recovery / training-load data.
- **fitbeing-health-agent** (Febe) — Warm health companion connecting to the Fitbeing wearable API via a user-supplied login token. Pulls sleep, HR, HRV, SpO2, stress, activity, sport, temperature, and respiratory data; ships three scheduled briefings, a 30-min waking-hours proactive poll, and an interactive HTML dashboard.

Both packs follow the standard pack layout (`AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `HEARTBEAT.md`, `agent-pack.yaml`, `description.json`, `.agents/skills/...`).
