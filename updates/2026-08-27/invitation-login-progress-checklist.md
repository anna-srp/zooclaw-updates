---
title: "邀请登录成功页新增 4 步进度清单，注册时不再对着静止页面猜进度"
type: "体验优化"
priority: "中"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 邀请登录成功页新增 4 步进度清单，注册时不再对着静止页面猜进度

## 核心宣传点

邀请注册成功后，页面原本长时间停在一句静止的「正在进入您的工作区…」，而后台其实还在跑验证身份、开通工作区、激活邀请权益等好几步，等待时完全没有反馈，容易让人以为卡死了。现在这里换成随真实进度推进的 4 步清单：已完成的打绿色对勾、进行中的转金色圈、还没轮到的显示灰点。同步修掉了首版里完成项文字被涂成背景色、绿勾之后一片看不清的问题。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `6ce1c1e2f244a0f85cff27add1162be963e0a90a`
- PR: #3557
- 作者: tim-srp
- 日期: 2026-08-27T12:40:19Z

### Commit Message

```
feat(invitation): show progress checklist on login success screen (#3557)

## 背景

`/invitation/login` 新用户注册成功后，过渡页长时间停留在静态的「验证完成 / 正在进入您的 ZooWork
工作区…」——期间实际在跑较慢的注册管线（OTP 验证 → 开通工作区 → 激活邀请权益 → 导航），等待过程没有任何反馈，容易引发焦虑。

## 改动

将 success 过渡页改为 **4 步执行清单**，随真实进度推进：

| 步骤 | 文案 | 状态反馈 |
| --- | --- | --- |
| identity | 验证身份 | 完成 → 绿色对勾 |
| workspace | 开通专属工作区 | 进行中 → 金色 spinner；待执行 → 灰色圆点 |
| redeem | 激活邀请权益 | 同上 |
| enter | 正在进入您的 ZooWork 工作区… | 导航前保持进行中（returnTo 存在时显示「正在返回…」） |

### 实现要点

- `lib/auth/manager.ts`：`loginWithSmsOTP` 新增**可选** `onVerified`
回调（向后兼容），在 OTP 通过、慢速注册开始前触发——这是 checklist 能反映真实进度的关键边界。
- `invitation/login/useBossclawLoginFlow.ts`：新增 `progress` state 与
`markDone/markRunning` helpers，接入新用户注册分支（含 `already_participated`
视为成功的路径）。
- `invitation/login/BossclawLoginClient.tsx` +
`bossclaw.module.css`：success 视图渲染 checklist（done → 绿勾 / running →
spinner / pending → 灰点），沿用既有品牌 token，深/浅色主题均适配。

## 测试

- hook：progress 状态推进（注册 + redeem 成功路径）、`already_participated`
分支推进；既有断言更新为三参调用。
- 组件：成功清单渲染（绿勾 / spinner / pending 无标记）、returnTo 时末步文案。

新增/更新用例后 `tests/unit/bossclaw/` 全量 115 个通过，`verify-web.sh`（guards + tsc
+ eslint）通过。

## 部署

前端-only 变更，无需后端部署。

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Description

```
## 背景

`/invitation/login` 新用户注册成功后，过渡页长时间停留在静态的「验证完成 / 正在进入您的 ZooWork 工作区…」——期间实际在跑较慢的注册管线（OTP 验证 → 开通工作区 → 激活邀请权益 → 导航），等待过程没有任何反馈，容易引发焦虑。

## 改动

将 success 过渡页改为 **4 步执行清单**，随真实进度推进：

| 步骤 | 文案 | 状态反馈 |
| --- | --- | --- |
| identity | 验证身份 | 完成 → 绿色对勾 |
| workspace | 开通专属工作区 | 进行中 → 金色 spinner；待执行 → 灰色圆点 |
| redeem | 激活邀请权益 | 同上 |
| enter | 正在进入您的 ZooWork 工作区… | 导航前保持进行中（returnTo 存在时显示「正在返回…」） |

### 实现要点

- `lib/auth/manager.ts`：`loginWithSmsOTP` 新增**可选** `onVerified` 回调（向后兼容），在 OTP 通过、慢速注册开始前触发——这是 checklist 能反映真实进度的关键边界。
- `invitation/login/useBossclawLoginFlow.ts`：新增 `progress` state 与 `markDone/markRunning` helpers，接入新用户注册分支（含 `already_participated` 视为成功的路径）。
- `invitation/login/BossclawLoginClient.tsx` + `bossclaw.module.css`：success 视图渲染 checklist（done → 绿勾 / running → spinner / pending → 灰点），沿用既有品牌 token，深/浅色主题均适配。

## 测试

- hook：progress 状态推进（注册 + redeem 成功路径）、`already_participated` 分支推进；既有断言更新为三参调用。
- 组件：成功清单渲染（绿勾 / spinner / pending 无标记）、returnTo 时末步文案。

新增/更新用例后 `tests/unit/bossclaw/` 全量 115 个通过，`verify-web.sh`（guards + tsc + eslint）通过。

## 部署

前端-only 变更，无需后端部署。

```

---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `605de3a5d33a990a0377b1541fce670dd1858be0`
- PR: #3558
- 作者: tim-srp
- 日期: 2026-08-27T13:03:59Z

### Commit Message

```
fix(invitation): keep checklist text uniform with a green done mark (#3558)

## 背景

#3557 上线后在 invitation 登录成功页引入进度清单,用户反馈:**绿色对号完成后,字体颜色看不清**。

根因:`.progressItemDone` / `.progressItemRunning` 使用 `color:
var(--boss-ink)` 作为文字颜色,但 `--boss-ink` 是**卡片背景色** token(深色 #0b0d11 /
light #f7f3ec)。步骤完成后文字被涂成背景色,与卡片融为一体。

## 改动

`web/app/src/app/[locale]/bossclaw/bossclaw.module.css`

- `.progressItem` 基础文字色改为 `var(--boss-cream)`(页面主文本色)
- 删除 `.progressItemDone` / `.progressItemRunning` 两个文字颜色覆盖块
- 所有条目文字保持统一颜色,状态仅由左侧标记区分:绿色 ✓ / 金色 spinner / 灰色圆点

## 验证

- `verify-web.sh --no-test`(guards + tsc + eslint)通过
- 纯 CSS 改动,无逻辑/测试影响

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Description

```
## 背景

#3557 上线后在 invitation 登录成功页引入进度清单,用户反馈:**绿色对号完成后,字体颜色看不清**。

根因:`.progressItemDone` / `.progressItemRunning` 使用 `color: var(--boss-ink)` 作为文字颜色,但 `--boss-ink` 是**卡片背景色** token(深色 #0b0d11 / light #f7f3ec)。步骤完成后文字被涂成背景色,与卡片融为一体。

## 改动

`web/app/src/app/[locale]/bossclaw/bossclaw.module.css`

- `.progressItem` 基础文字色改为 `var(--boss-cream)`(页面主文本色)
- 删除 `.progressItemDone` / `.progressItemRunning` 两个文字颜色覆盖块
- 所有条目文字保持统一颜色,状态仅由左侧标记区分:绿色 ✓ / 金色 spinner / 灰色圆点

## 验证

- `verify-web.sh --no-test`(guards + tsc + eslint)通过
- 纯 CSS 改动,无逻辑/测试影响

```

---
