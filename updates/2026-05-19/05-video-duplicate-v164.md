---
title: "Video Duplicate Agent 正式上架（v1.6.4）"
type: "Agent 上架/更新"
priority: "高"
date: "2026-05-19"
status: "待审核"
channels: ""
---
# Video Duplicate Agent 正式上架（v1.6.4）

## 核心宣传点
全新 Video Duplicate Agent 上线！能够分析视频内容并自动生成风格相似的新视频，支持多种工作流，是创作同款视频内容的强力工具。

## 原始内容
```
commit: 7ccf7f66062b105719c0f315bc3948908133b54e
repo: SerendipityOneInc/ecap-agent-pack
author: vincent-srp
date: 2026-05-19T04:51:28Z

feat(video-duplicate): add Video Duplicate pack v1.6.4 (#132)

--- PR #132 Body ---
## Summary
- Add new pack `video-duplicate/` (agentPack_id: `video-duplicate`) from `build/video-duplicate-1.6.4.tar.gz`
- This is a separate pack from the existing `video-ads-duplicate/` (different agentPack_id `video_ads_duplicate`), so both coexist
- Fix `description.json` version field (upstream build left it at `1.6.3`; now synced to `1.6.4` to match `agent-pack.yaml` and CHANGELOG)

## Pack overview
- Role: 分镜复刻·剪辑编导大师 (AI Short-Video Replication Director)
- Three workflows: Workflow C (storyboard-guided, recommended) / A (frame-precise) / B (style transfer)
- Stack: Gemini 3.1 Pro · gpt-image-2 · Seedance 2.0 Pro · Demucs · ffmpeg

## Notes
- Upstream 1.6.4 fix vs 1.6.3: removed broken `subtitle_burn.py` reference in `agent-pack.yaml`, migrated 3 pipelines to `transcribe.sh` + `burn.sh`, dropped bundled 1.6.1 tarball leftovers (`artifacts/`, `zip/`)
- `subtitle_burn.py.deprecated` is still shipped in the tarball as dead weight (no longer referenced by yaml); not blocking — flag for upstream build cleanup

## Test plan
- [ ] Verify pack loads at runtime in an OpenClaw bot pod
- [ ] Smoke-test Workflow C (storyboard-guided) end-to-end
- [ ] Confirm `video-ads-duplicate` pack remains unaffected

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```
