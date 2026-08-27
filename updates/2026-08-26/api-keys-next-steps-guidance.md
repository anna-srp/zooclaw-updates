---
title: "API Keys 页面现在会告诉你「拿到密钥之后该干什么」"
type: "体验优化"
priority: "中"
date: "2026-08-26"
status: "待审核"
channels: ""
---

# API Keys 页面现在会告诉你「拿到密钥之后该干什么」

## 核心宣传点

以前 API Keys 页面只管发密钥，发完就没了下文——你拿着一串字符，不知道能用来做什么、怎么接。现在页头常驻一个直达快速上手文档的链接，空状态会讲清楚典型用法（写脚本、后端服务、AI 编码助手）并直接给出安装命令，创建成功的密钥弹窗里也会附上「下一步」指引。顺带修掉了两个老毛病：手机上密钥弹窗横向溢出、复制按钮跑到屏幕外；以及页头操作按钮撑破内容区不换行。密钥弹窗现在点外面不会误关（Esc 仍可关闭），并新增了明确的「完成」按钮。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `2f5ff75cc502e7eb31507d7569de82ed872b5047`
- PR: #3533
- 作者: finn-srp
- 日期: 2026-08-26T13:36:07Z

### Commit Message

```
feat(settings): tell users what to do with an API key (#3533)

## Linear
<!-- 无关联 issue -->

## Summary

API Keys tab 发得出密钥，但从不说这密钥能干什么。三个触点补上：

- **页头**加常驻「文档」链接，指向 quickstart（不是文档根）。始终英文——文档站自带语言切换，而 App 有 10 个
locale、文档站只有 2 个，按 locale 拼路径迟早拼出 404。
- **空状态**改成讲用途（脚本 / 后端服务 / AI 编码助手），并直接给出 skill
安装命令。落在这一屏、手上还没有密钥的人，就是接下来要接入的那个人——personal org
里创建者和接入者按定义是同一个人（`ClawSettingsClient.tsx` 的门是 `org_type === 'personal'
|| role === 'admin'`）。
- **创建成功后的密钥弹窗**给出「下一步」。**轮换不给**——轮换的人早已接入过，此时他要的是速度。

顺带修掉引导过程中量出来的两个既有缺陷：

- **弹窗在手机上横向溢出 229px。** `DialogContent` 是 grid，隐式单列轨道按最宽子元素的 max-content
定宽，而 `code` 是 `whitespace-nowrap`，把轨道撑爆视口，密钥的 Copy 按钮整个跑到屏幕外。给轨道加
`grid-cols-[minmax(0,1fr)]` 后，滚动交回给 `code` 自己已有的 `overflow-x-auto`。375px
实测溢出 229 → 0。
- **页头操作行 `shrink-0`，撑破 settings 内容区而不是换行。** 内容区远比视口窄，所以横排断点从 `sm:` 挪到
`lg:`，并在 `lg:` 以上钉住行宽让标题让位。768px 实测行内溢出 376 → 0。

### 密钥弹窗的关闭规则

**Escape 照常关闭，点弹窗外面不关。** Escape
是刻意按下的，不是需要防的那种误触；停在遮罩上的一次误点才是，而这一屏的内容关掉就再也拿不回来。实测「从密钥文字上开始拖选、松手落在弹窗外」也不会关（文字照常能选中）。

规则只有一行 `onInteractOutside`，不需要按「屏幕上有没有密钥」分支——Escape
永远可用，就不存在把人锁死的风险，标准键盘行为也原样保留。

同时加了「完成 / Done」按钮：原本唯一的显式出口是右上角 32px 的 ×（实测对比度 3.74:1），作为这一屏的主要退出方式太小了。

### 复制走 `useCopyToClipboard`

命令块最初手写了一条 promise chain。这有个真实后果：`navigator.clipboard` 是 secure-context
gated 的，`http://` 源上这个属性根本不存在，于是读 `.writeText` 会在 `.catch()`
挂上之前同步抛错，我们承诺的「复制失败，请手动选中」提示永远不显示——恰恰在最需要它的场景里失灵。

`usehooks-ts` 是本 workspace 对浏览器 API hook 的既定选型（见
`web/app/AGENTS.md`「默认技术选型」），已经在依赖里，且自带 `useCopyToClipboard`：API
缺失和写入被拒都返回 `false`。改用它是**删代码**，不是再加一层防护。

> 全站另有 12 处手写 `clipboard.writeText`，5 种不同的错误处理策略（静默吞、裸
await、守卫后静默返回、发射后不管、`.then` 链）。不在本 PR 范围，值得单开清理。

### 文案

产品名改为 **ZooWork**（原文写的是「调用 ZooClaw API」，而它指向的文档、SDK 包、skill 仓都叫
ZooWork）。只有 `settings.apiKeys.description` 带产品名，且只有 en/zh 翻译了这个块，其余 8
个语言走英文 fallback，所以两条字符串覆盖全部读者。

**docs host 仍是
`zooclaw.ai`**，等文档站迁移完再换。常量处加了注释，说明这个与周边文案的品牌不一致是有意的，不是笔误。

## Test plan

- [x] `bash scripts/verify-web.sh` 全绿：tsc + eslint + **9222 项单测**（本文件 50
条）
- [x] `pnpm run lint:ci` 全绿（dependency-cruiser + knip；这层 `verify-web.sh`
不覆盖）
- [x] 本地 mock 栈实测创建与轮换两条流程，中英双语 × 明暗双主题
- [x] 375 / 768 / 1280 三档宽度实测：页面级 `scrollWidth > clientWidth` 均为 false
- [x] 真浏览器逐条验证关闭规则：点遮罩不关、拖选出界不关、Escape 关闭、「完成」关闭
- [x] 实测剪贴板缺失（`navigator.clipboard` 置 undefined）时会显示手动复制提示
- [x] 实测「复制命令」写入的是命令而非密钥

## 已知未解

375px 下这一屏依然散架，但根因是 claw-settings 这个壳没有移动端布局，内容区被压到 0–75px；未改动的 General
tab 一样如此（实测其 h2 仅 48px 宽）。不在本 PR 范围。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: wangfulong <wfllike@gmail.com>
Co-authored-by: Claude Opus 5 <noreply@anthropic.com>
```

### PR Description

```
## Linear
<!-- 无关联 issue -->

## Summary

API Keys tab 发得出密钥，但从不说这密钥能干什么。三个触点补上：

- **页头**加常驻「文档」链接，指向 quickstart（不是文档根）。始终英文——文档站自带语言切换，而 App 有 10 个 locale、文档站只有 2 个，按 locale 拼路径迟早拼出 404。
- **空状态**改成讲用途（脚本 / 后端服务 / AI 编码助手），并直接给出 skill 安装命令。落在这一屏、手上还没有密钥的人，就是接下来要接入的那个人——personal org 里创建者和接入者按定义是同一个人（`ClawSettingsClient.tsx` 的门是 `org_type === 'personal' || role === 'admin'`）。
- **创建成功后的密钥弹窗**给出「下一步」。**轮换不给**——轮换的人早已接入过，此时他要的是速度。

顺带修掉引导过程中量出来的两个既有缺陷：

- **弹窗在手机上横向溢出 229px。** `DialogContent` 是 grid，隐式单列轨道按最宽子元素的 max-content 定宽，而 `code` 是 `whitespace-nowrap`，把轨道撑爆视口，密钥的 Copy 按钮整个跑到屏幕外。给轨道加 `grid-cols-[minmax(0,1fr)]` 后，滚动交回给 `code` 自己已有的 `overflow-x-auto`。375px 实测溢出 229 → 0。
- **页头操作行 `shrink-0`，撑破 settings 内容区而不是换行。** 内容区远比视口窄，所以横排断点从 `sm:` 挪到 `lg:`，并在 `lg:` 以上钉住行宽让标题让位。768px 实测行内溢出 376 → 0。

### 密钥弹窗的关闭规则

**Escape 照常关闭，点弹窗外面不关。** Escape 是刻意按下的，不是需要防的那种误触；停在遮罩上的一次误点才是，而这一屏的内容关掉就再也拿不回来。实测「从密钥文字上开始拖选、松手落在弹窗外」也不会关（文字照常能选中）。

规则只有一行 `onInteractOutside`，不需要按「屏幕上有没有密钥」分支——Escape 永远可用，就不存在把人锁死的风险，标准键盘行为也原样保留。

同时加了「完成 / Done」按钮：原本唯一的显式出口是右上角 32px 的 ×（实测对比度 3.74:1），作为这一屏的主要退出方式太小了。

### 复制走 `useCopyToClipboard`

命令块最初手写了一条 promise chain。这有个真实后果：`navigator.clipboard` 是 secure-context gated 的，`http://` 源上这个属性根本不存在，于是读 `.writeText` 会在 `.catch()` 挂上之前同步抛错，我们承诺的「复制失败，请手动选中」提示永远不显示——恰恰在最需要它的场景里失灵。

`usehooks-ts` 是本 workspace 对浏览器 API hook 的既定选型（见 `web/app/AGENTS.md`「默认技术选型」），已经在依赖里，且自带 `useCopyToClipboard`：API 缺失和写入被拒都返回 `false`。改用它是**删代码**，不是再加一层防护。

> 全站另有 12 处手写 `clipboard.writeText`，5 种不同的错误处理策略（静默吞、裸 await、守卫后静默返回、发射后不管、`.then` 链）。不在本 PR 范围，值得单开清理。

### 文案

产品名改为 **ZooWork**（原文写的是「调用 ZooClaw API」，而它指向的文档、SDK 包、skill 仓都叫 ZooWork）。只有 `settings.apiKeys.description` 带产品名，且只有 en/zh 翻译了这个块，其余 8 个语言走英文 fallback，所以两条字符串覆盖全部读者。

**docs host 仍是 `zooclaw.ai`**，等文档站迁移完再换。常量处加了注释，说明这个与周边文案的品牌不一致是有意的，不是笔误。

## Test plan

- [x] `bash scripts/verify-web.sh` 全绿：tsc + eslint + **9222 项单测**（本文件 50 条）
- [x] `pnpm run lint:ci` 全绿（dependency-cruiser + knip；这层 `verify-web.sh` 不覆盖）
- [x] 本地 mock 栈实测创建与轮换两条流程，中英双语 × 明暗双主题
- [x] 375 / 768 / 1280 三档宽度实测：页面级 `scrollWidth > clientWidth` 均为 false
- [x] 真浏览器逐条验证关闭规则：点遮罩不关、拖选出界不关、Escape 关闭、「完成」关闭
- [x] 实测剪贴板缺失（`navigator.clipboard` 置 undefined）时会显示手动复制提示
- [x] 实测「复制命令」写入的是命令而非密钥

## 已知未解

375px 下这一屏依然散架，但根因是 claw-settings 这个壳没有移动端布局，内容区被压到 0–75px；未改动的 General tab 一样如此（实测其 h2 仅 48px 宽）。不在本 PR 范围。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

```
