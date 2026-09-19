---
title: "fix(designer): add concise image IP restrictions (#286)"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-18"
status: "待审核"
channels: ""
---

# Designer 技能补充图像 IP 限制规则

## 核心宣传点

Designer 的 Rules 里加了两条明确约束：拒绝复现可识别的第三方角色、吉祥物、Logo 和有品牌特征的场景（包括基于参考图的改图和高度相似的仿作），也不允许通过改名字或换工具/模型绕过，遇到这类需求会主动给出原创替代方案。只改了 designer/SKILL.md，属于模型侧指引而不是服务端审核网关，没有全局系统提示词或脚本改动。

## 分级

- 内部：P1
- 外部：C
- 发布状态：未知/需确认

## PR 说明

## Summary
Add two short sentences to Designer's existing Rules section: refuse recognizable third-party character, mascot, logo, and branded-setting reproductions, including reference-image edits and lookalikes; do not bypass via renamed subjects or alternate tools/models; offer an original alternative.

Only designer/SKILL.md changes. This is model guidance, not a server-side moderation gate. No global system prompt or script changes, and no deployment.

Companion engine tool guidance: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1517

## Validation
Skill linter passed (12 existing warnings in other skills). Reviewed the rule against existing generation/editing instructions.


## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- SHA: `d0eb9299a82c5065f9642f4124f59348014b5d51`
- PR: #286
- 作者：tim-srp
- 日期：2026-09-18T10:11:09Z

### Commit Message

```
fix(designer): add concise image IP restrictions (#286)

## Summary
Add two short sentences to Designer's existing Rules section: refuse
recognizable third-party character, mascot, logo, and branded-setting
reproductions, including reference-image edits and lookalikes; do not
bypass via renamed subjects or alternate tools/models; offer an original
alternative.

Only designer/SKILL.md changes. This is model guidance, not a
server-side moderation gate. No global system prompt or script changes,
and no deployment.

Companion engine tool guidance:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1517

## Validation
Skill linter passed (12 existing warnings in other skills). Reviewed the
rule against existing generation/editing instructions.
```

## 备注

发布状态：未知/需确认（Skill 走 ClawHub 独立分发，仓库 release tag 不可靠；本次为 SKILL.md 模型指引改动，PR 明确说明无需部署，随 Skill 包分发生效）。

来源：SerendipityOneInc/ecap-skills @ d0eb9299，PR #286，作者 tim-srp。
