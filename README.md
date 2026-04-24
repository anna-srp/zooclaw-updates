# ZooClaw 产品更新库

这个仓库是 ZooClaw 每日产品更新的结构化存档，每天北京时间 09:00 自动从 GitHub commits 同步一次，把用户能感知到的更新整理成结构化文件，并保留原始 commit 数据供按需深挖。

设计目标是**让 AI Agent 直接读懂它**。你可以把仓库 URL 丢给任何 agent，用自然语言提问：

> "最近有哪些新功能上线？"
> "上周有什么高优先级的更新？"
> "vibe-drama Agent 最新版本有什么变化？"
> "帮我整理一下本周的更新，写成用户公告"
> "这周有哪些内容适合发到 Discord？"

---

## 🤖 如果你是 AI Agent，从这里开始

**30 秒速查版：**

1. **入口优先读 [`index.md`](./index.md)** —— 它按日期倒序列出更新标题和链接；`type` / `priority` / `status` / `channels` 的权威来源是每个 update 文件的 frontmatter。
2. **过滤规则**：默认不推 `status: "内部-跳过"` 的条目（它们是内部技术变更，对普通用户不够友好）；但如果用户明确想看底层/技术改动，可以主动抓取这些条目展示。
3. **深入细节**：index 里的每一行都链接到 `updates/YYYY-MM-DD/<slug>.md`，里面有「核心宣传点」可直接作为对外文案。
4. **写周报/月报**：直接用 [`changelog.md`](./changelog.md)，已经按时间倒序 + emoji 分类排好了。
5. **要底层技术细节**：读 `raw/` 目录，里面是原始 commit 数据。**默认不要读 raw/**，它体积大且不适合对外。

**一条硬规则：`核心宣传点` 是面向用户的，`原始内容` 是英文 commit 原文 —— 发给用户时用前者，不要贴后者。**

---

## 📁 目录结构

```
zooclaw-updates/
├── index.md                 ← 【主入口】所有更新的总目录，按日期倒序
├── changelog.md             ← 【人类友好】带 emoji 分类的更新日志
├── updates/                 ← 【结构化 updates】每条更新一个 md
│   └── YYYY-MM-DD/
│       └── <slug>.md        ← 有 frontmatter + 核心宣传点 + 原始内容
├── raw/                     ← 【原始 commit 数据】给 agent 按需深挖用
│   ├── YYYY-MM-DD/          ← 按日期组织的当天 raw 数据
│   ├── ecap-workspace-commits.{md,json}   ← 过去 7 天 workspace 仓库 commits（滚动）
│   ├── ecap-skills-commits.{md,json}      ← 过去 7 天 skills 仓库 commits（滚动）
│   └── ecap-agent-pack-commits.{md,json}  ← 过去 7 天 agent-pack 仓库 commits（滚动）
└── templates/
    └── update-template.md   ← 新 update 文件的模板
```

**数据覆盖范围：**

| 位置 | 最早日期 | 特点 |
|------|---------|------|
| `updates/` | 2026-04-11 | 永久保留，每条 update 独立文件 |
| `raw/YYYY-MM-DD/` | 2026-04-16 | 按日期归档 |
| `raw/ecap-*-commits.md` | 滚动过去 7 天 | 只含最近一周，会被覆盖 |

---

## 📋 Update 文件格式

每个 `updates/YYYY-MM-DD/<slug>.md` 由 frontmatter + 三个 section 组成：

```markdown
---
title: "iOS 聊天界面全面重构，更流畅更原生"
type: "产品基础功能更新"
priority: "高"
date: "2026-04-23"
status: "待审核"
channels: "Discord+站内弹窗"
---

# iOS 聊天界面全面重构，更流畅更原生

## 核心宣传点
一句话面向用户的描述，可以直接用于对外发布。

## 原始内容
对应 GitHub commit 的原文（通常是英文）。

## 备注
可选。内部备注，不对外。
```

### Frontmatter Schema（Agent 过滤时用）

| 字段 | 当前已观察值 / 格式 | 说明 |
|------|--------------|------|
| `title` | 自由文本 | 对用户友好的中文标题 |
| `type` | `Bug Fix` / `新功能上线` / `Skill 上架/更新` / `Agent 上架/更新` / `产品基础功能更新` / `优化` / `体验优化` / `其他公告` | 更新类型；未来可能新增值，agent 不要因为未知 type 丢弃条目 |
| `priority` | `高` / `中` / `低` | 高 = 重要功能/新 Agent；中 = 用户可感知的改进；低 = 小优化 |
| `date` | `YYYY-MM-DD` | 对应 commit 的日期 |
| `status` | `待审核`（未发布）/ `已发布` / `内部-跳过`（内部技术变更，默认不对外推送，但用户主动想看时可抓取） | 见下方硬规则 |
| `channels` | 自由文本，多渠道用 `+` 分隔（如 `社媒素材+blog+Discord`） | 计划发布渠道，空 = 还没规划 |

---

## 🎯 Agent 查询 Playbook

遇到用户提问，按这张表选路径：

| 用户提问类型 | Agent 操作 |
|-----------|----------|
| "最近/本周/上周有什么更新？" | 读 `index.md` 头 N 天 → 按需打开 `updates/YYYY-MM-DD/*.md` 拿「核心宣传点」 |
| "哪些是高优先级的？" | 先用 `index.md` 定位近期文件 → 打开 update frontmatter，过滤 `priority == "高"` |
| "最近有什么新 Agent / 新 Skill？" | 先用 `index.md` 定位近期文件 → 打开 update frontmatter，过滤 `type ∈ {"Agent 上架/更新", "Skill 上架/更新"}` |
| "最近有哪些 Bug 修复？" | 先用 `index.md` 定位近期文件 → 打开 update frontmatter，过滤 `type == "Bug Fix"` |
| "帮我整理一份 Discord / 社媒 公告" | 读 `updates/` 近期文件，排除 `status == "内部-跳过"`；优先使用 `channels` 包含目标渠道的条目，`channels` 为空时按内容相关性决定，不要直接丢弃 |
| "帮我写周报 / 月报" | 直接读 `changelog.md`，里面已按时间倒序 + emoji 分类格式化好了 |
| "我想看内部/底层有哪些技术改动" | 反向过滤 `status == "内部-跳过"` 的条目 —— 这些是面向技术用户的变更（默认不推，但用户主动问就给） |
| "某个 commit / 功能的技术细节？" | 读 `raw/YYYY-MM-DD/` 或 `raw/ecap-*-commits.md`（仅覆盖过去 7 天） |
| "去年 / 几个月前的 X 功能" | 答「数据最早到 2026-04-11」，不要编造 |

---

## ⚠️ 给 Agent 的硬规则

1. **`status: "内部-跳过"` 的条目默认不推** —— 它们是内部技术变更，对普通用户不够友好。但**用户明确想看**（如 "最近底层做了什么优化？" / "有哪些技术性改动？"）时，**可以主动抓取并展示**，不要装作它们不存在。
2. **不要把「原始内容」section 直接贴给用户** —— 它是英文 commit 原文；永远优先用「核心宣传点」。
3. **`channels` 为空不代表不发** —— 只是还没规划；有值则表示已有发布意向。
4. **文件名混用中英文** —— 有的是 kebab-case 英文（`ios-chat-custom-view.md`），有的是中文（`vibe-drama-Agent-升级-v1.0.9.md`）。搜索时两种命名都要试。
5. **`index.md` 格式不统一** —— 最近几天用 bullet list，通常只有标题和链接；更老用 table，可能带 type / priority / status。解析时两种都要兼容，metadata 以 update frontmatter 为准。
6. **默认不要去 raw/** —— 体积大、是英文 commit 原文、对外不友好。只有在需要技术细节时再读。
7. **不要主动修改本仓库** —— 这是自动同步的结构化存档，人类编辑器会手动维护 `status` 字段和「核心宣传点」，agent 不要越俎代庖。

---

## 🔄 更新频率

- **同步时间**：每天北京时间 **09:00**
- **数据源**：`ecap-workspace` / `ecap-skills` / `ecap-agent-pack` 三个 GitHub 仓库前一天的 commits
- **过滤规则**：`updates/` 优先沉淀用户能感知到的更新；纯内部技术变更默认不对外发布，必要时可从 `raw/` 或 `status: "内部-跳过"` 条目追溯

---

## 💡 人类使用指南

如果你是人类用户，两个入口都不错：

- **想快速浏览 + 精美排版** → 看 [`changelog.md`](./changelog.md)
- **想找某条具体更新 / 看原始数据** → 从 [`index.md`](./index.md) 入口点进去

想让 AI 帮你整理？把仓库 URL 丢给 agent，它会自己按上面的 Playbook 读取。
