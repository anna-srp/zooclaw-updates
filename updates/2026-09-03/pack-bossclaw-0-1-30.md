---
title: "BossClaw 更新至 0.1.30：公众号监控改按原始ID 抓取，技能触发更准"
type: "Skill 上架/更新"
priority: "中"
date: "2026-09-03"
status: "待审核"
channels: "Discord+changelog"
---

# BossClaw 更新至 0.1.30：公众号监控改按原始ID 抓取，技能触发更准

## 核心宣传点

BossClaw（老板专属幕僚长）发布 0.1.30。

主要改动在行业公众号监控（boss-radar）：拉取某个已知公众号的历史发文时，账号标识改为按优先级三选一——原始ID `ghid`（`gh_…`）为首选，其次是该号任意一篇文章链接，最后才是公众号名称。原因很实际：公众号名称重名多、也更容易被屏蔽返回错误码，而原始ID 唯一且最稳定。订阅清单里现在要求尽量给每个号都存下 ghid 锚点。同时接口不再有 `--count` 参数，改为一次一页、按游标翻页。

另一处是全包范围的技能描述改写：boss-triage、boss-reply、boss-meeting、boss-voice、boss-video、boss-profile、boss-radar、boss-detail-page、video-subtitle 九个技能的 description 由多行块状文本压缩成单行紧凑写法，触发词覆盖不变但更集中，让 Agent 在判断「该调哪个技能」时匹配得更准。

## 原始内容

- 来源: Agent Pack 商店扫描（pack_diff.js）
- Pack: `bossclaw`（BossClaw · 老板专属幕僚长）
- 版本: 0.1.29 → 0.1.30（共 25 版）
- 分类: productivity / 免费

### 变更文件

```
./.agents/skills/boss-detail-page/SKILL.md
./.agents/skills/boss-meeting/SKILL.md
./.agents/skills/boss-profile/SKILL.md
./.agents/skills/boss-radar/SKILL.md
./.agents/skills/boss-radar/scripts/monitor_backup.py
./.agents/skills/boss-radar/scripts/wechat_mp.py
./.agents/skills/boss-reply/SKILL.md
./.agents/skills/boss-triage/SKILL.md
./.agents/skills/boss-video/SKILL.md
./.agents/skills/boss-voice/SKILL.md
./.agents/skills/video-subtitle/SKILL.md
./AGENTS.md
./agent-pack.yaml
```

## 备注

Agent Pack 通过 ClawHub 独立分发，版本一经提交即对用户可见，不随 ecap-workspace release 发版。
