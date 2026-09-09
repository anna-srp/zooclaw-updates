---
title: "BossClaw 更新至 0.1.32：砍掉每小时保活轮询，改成「每天回我一句就不会断」"
type: "Skill 上架/更新"
priority: "中"
date: "2026-09-08"
status: "待审核"
channels: "Discord+changelog"
---

# BossClaw 更新至 0.1.32：砍掉每小时保活轮询，改成「每天回我一句就不会断」

## 核心宣传点

BossClaw（老板专属幕僚长）发布 0.1.32，这版是一次**知情取舍**：**每小时的 `boss-keepalive` 保活 cron 被砍掉了。**

背景是微信的规矩——老板超过 24 小时没回话，bot 会被挡住、无法主动发消息，早报这类定时推送随之发不出去。之前 BossClaw 的对策是每小时跑一条 cron，读一下「最后活跃时间」，快到 24h 死线时主动发一条个性化续命消息。逻辑是对的，代价太大：**每小时起一个完整会话只为算一次时间戳，约 96% 的时候什么都不做就退出**，纯烧 token。这版决定不划算，直接砍。

随之删掉的还有两个脚本：`keepalive_check.py`（判断该不该续命）和 `mark_seen.py`（打活跃时间戳）。原本 AGENTS.md 里「每轮第一件事先打活跃卡」的 step 0 也没了，会话启动少一次脚本调用。

替代方案是三条更省的规矩：① 主动发失败或老板久未回话时**别硬发、别重试轰炸**；② 定时产物（早报）发不出就**留着**——`brief_file.py` 已经落盘了，老板下次一开口先补发；③ onboarding 和早报末尾**顺口提醒一句「每天回我一句就不会断」**，这现在是唯一的续窗手段，明确写了「别省」。

对老板侧可感知的变化：onboarding 时自动建的 cron 少了一条——设了早报是 **3 条**（style-distill + boss-radar-generate + boss-radar-send），没设早报是 **1 条**（style-distill），之前分别是 4 条和 2 条。

## 原始内容

- 来源: Agent Pack 商店扫描（pack_diff.js）
- Pack: `bossclaw`（BossClaw · 老板专属幕僚长）
- 版本: 0.1.31 → 0.1.32（共 27 版）
- 分类: productivity / 免费
- 变更性质: 删除 2 个保活脚本，`agent-pack.yaml` 移除 `boss-keepalive` cron 定义，AGENTS.md 删除「主动续命」整节与 step 0 活跃卡，boss-profile / boss-radar 两个 SKILL.md 同步改写 cron 条数与 24h 窗口说明

### 变更文件

```
删除:
./.agents/skills/boss-profile/scripts/keepalive_check.py
./.agents/skills/boss-profile/scripts/mark_seen.py

修改:
./.agents/skills/boss-profile/SKILL.md
./.agents/skills/boss-radar/SKILL.md
./AGENTS.md
./agent-pack.yaml
```

## 备注

发布状态：已上线。Agent Pack 通过 ClawHub 独立分发，版本一经提交即对用户可见，不随 ecap-workspace release 发版。
