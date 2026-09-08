---
title: "BossClaw 更新至 0.1.31：九个技能的触发描述恢复完整版，少认错活"
type: "Skill 上架/更新"
priority: "低"
date: "2026-09-07"
status: "待审核"
channels: "Discord+changelog"
---

# BossClaw 更新至 0.1.31：九个技能的触发描述恢复完整版，少认错活

## 核心宣传点

BossClaw（老板专属幕僚长）发布 0.1.31，是一次纯粹的技能描述调整，没有新增功能。

上一版 0.1.30 曾把包内九个技能的 description 统统压成单行紧凑写法，想让触发匹配更集中。这一版把它们改了回去、并写得比压缩前更完整：boss-triage、boss-reply、boss-meeting、boss-voice、boss-video、boss-profile、boss-radar、boss-detail-page、video-subtitle 九个技能的描述重新展开成多行，把「什么时候该用我」「典型触发说法」「会产出什么」讲全。

举几个能看出差别的例子：boss-reply 明确补回了「代写」的完整边界——不止回消息和邮件，评论、帖子、朋友圈、群发、致辞、公开回应都算，并写清它是 boss-triage / boss-voice 问完「要不要我替你回」之后的接力目标；boss-triage 补回了「我不做中立摘要，而是给决策判断」这个定位差别；boss-video 把口播（9:16 单镜）和宣讲片（16:9 电影感长片）两种模式的区分重新写进描述里。

这类改动用户不会直接看到，但会影响 Agent 在收到一句话时判断「该调哪个技能」——描述写得越准，认错活的概率越低。

## 原始内容

- 来源: Agent Pack 商店扫描（pack_diff.js）
- Pack: `bossclaw`（BossClaw · 老板专属幕僚长）
- 版本: 0.1.30 → 0.1.31（共 26 版）
- 分类: productivity / 免费
- 变更性质: 9 个 SKILL.md 均只改动 frontmatter 的 `description` 一行，正文无改动

### 变更文件

```
./.agents/skills/boss-detail-page/SKILL.md
./.agents/skills/boss-meeting/SKILL.md
./.agents/skills/boss-profile/SKILL.md
./.agents/skills/boss-radar/SKILL.md
./.agents/skills/boss-reply/SKILL.md
./.agents/skills/boss-triage/SKILL.md
./.agents/skills/boss-video/SKILL.md
./.agents/skills/boss-voice/SKILL.md
./.agents/skills/video-subtitle/SKILL.md
./agent-pack.yaml
```

## 备注

发布状态：已上线。Agent Pack 通过 ClawHub 独立分发，版本一经提交即对用户可见，不随 ecap-workspace release 发版。
