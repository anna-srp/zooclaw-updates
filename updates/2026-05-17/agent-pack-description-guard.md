---
title: "Agent 商店展示信息更准确，不再出现 Agent 信息混乱"
type: "Bug Fix"
priority: "低"
date: "2026-05-17"
status: "待审核"
channels: ""
---
# Agent 商店展示信息更准确，不再出现 Agent 信息混乱

## 核心宣传点
修复了一个导致 Agent 商店中 Agent 描述信息显示错误的问题——某些 Agent 的介绍页可能错误显示了另一个 Agent 的信息，现已从源头阻止此类错误发布。

## 原始内容
**Commit**: fix(agent-studio): package.py refuses mismatched description.json (#129)
**Repo**: SerendipityOneInc/ecap-agent-pack
**SHA**: e719ed00
**Author**: 后端团队
**Date**: 2026-05-17

**Commit Message**:
fix(agent-studio): package.py refuses mismatched description.json (#129)

Closes the workspace-pollution bug class observed on prod bot oc-53bfc1d0…ppz7n: a pack pivot (coros-coach → fitbeing-health-agent) was made by editing agent/agent-pack.yaml in place, without /studio new. The previous pack's description.json survived in agent/ and got bundled verbatim into the new archive — shipping COROS Coach's listing under the Fitbeing pack name.

package.py guard: refuses to package when description.json's agentPack_id doesn't match manifest name. Catches the bug even if the drift detector is somehow bypassed. The error message points the creator at generate_description.py (Stage 5a).

Bumps agent-studio v1.2.2 → v1.2.3.

**PR Description**:
## Bug
Prod bot oc-53bfc1d0-6f5b59cb49-ppz7n shipped a Fitbeing Health Agent pack whose description.json still described the previous pack (COROS Coach), because nothing verified the file matched the current pack before bundling it.

## Fix
package.py refuses to package when agent/description.json#agentPack_id doesn't match agent-pack.yaml#name. The error message points the creator at generate_description.py (Stage 5a).

Plus drive-by cleanup: install.py's local _read_description_json and the new guard now share _common.read_description_json.

## End-to-end verification
- Mismatched description.json#agentPack_id → packaging refused with exit 1 and clear message
- Matched → packaging succeeds normally
- Missing agent/description.json → still treated as optional (same as before)
