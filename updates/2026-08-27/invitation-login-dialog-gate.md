---
title: "邀请制登录改版：邀请码改为弹窗前置，不再让人干等一条永远不会到的短信"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 邀请制登录改版：邀请码改为弹窗前置，不再让人干等一条永远不会到的短信

## 核心宣传点

旧的邀请登录流程有个要命的误会：输完手机号后出现一个验证码输入框，大家都以为短信已经发出去了——其实那个框要填的是邀请码，邀请码验证通过之前根本不会发短信，于是很多人在那儿白等。现在邀请码改成手机号页面之上的一个弹窗，明确写清「短信要等邀请码通过后才会发出」、给出邀请码格式示例，并附上没有邀请码时的联系方式；进入真正的短信验证码步骤后，文案直接写明是「短信验证码」，输入框也改成 6 个格子，一眼就知道该填什么。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `d99ad16170d5bc3264bde0eb4821adcaf614b11e`
- PR: #3542
- 作者: david-srp
- 日期: 2026-08-27T06:31:22Z

### Commit Message

```
feat(invitation): gate the invited-trial login behind an invitation dialog (#3542)

## What

Reworks `/invitation/login` — the invited-trial entry into ZooWork
Business — and leaves the `/bossclaw` campaign wizard alone.

The old flow had a specific failure: you typed a phone number, landed on
a code field, and assumed the SMS was on its way. It wasn't — that field
wanted an **invitation code**, and no SMS is sent until the code passes.
People sat waiting for a message that was never sent.

## Changes

**Invite code is now a gate, not a step.** It opens as a dialog over the
phone screen, which stays visible underneath. That frames it as "one
more thing before we continue" instead of "you advanced, here is the
code field", and carries the ceremony the route is named after. The
dialog restates the phone it is acting on, says outright that the SMS
only goes out once the code passes, shows a worked example (`例如
ZC-64ACFC`), and points at `sales@zoowork.ai` for anyone without an
invite.

It is hand-rolled rather than `@/components/ds/dialog`: this is a
branded module with a fixed palette and the shadcn primitive's
`bg-popover` / `bg-card` tokens cascade against it (per
`web/app/AGENTS.md` → Branded modules). It reuses the repo's
`useBodyLock` + `useEscapeKey`, focuses the code field on open, traps
focus, and is flex-centred inside a scrollable overlay so a mobile
keyboard can scroll it into view rather than pinning it underneath.

**SMS step says what it wants.** Copy names 短信验证码 explicitly, and the
code renders as six boxes so it reads as a 6-digit SMS code rather than
a free-text field. One real input is stretched transparently across the
boxes instead of six separate inputs — that keeps iOS one-time-code
autofill, paste and backspace working with no cross-input focus
juggling. Resend became a quiet inline link and 返回上一步 a de-emphasised
text link.

**Dropped the STEP kickers.** The numbering read as chrome; the headline
already says where you are.

**Copy rebuilt from zoowork.ai's own claims** — 不只是回答 / 交付真实成果, 按角色限权,
行业模板. Removed 工作区 and Agent Pack from the brand panel: both are internal
vocabulary that appears nowhere on the marketing site. Contact address
is `sales@zoowork.ai`.

**Light theme with a toggle** (bottom-right, follows the OS by default).
The palette is mirrored under `prefers-color-scheme` and the
`data-boss-theme` attribute is only stamped for an explicit choice, so
the default path resolves in CSS with no JS and no dark first paint —
verified before hydration.

## Review fixes folded in

A multi-agent adversarial pass produced 35 findings; 18 survived
independent verification and are fixed here. The substantive ones:

- The light palette failed the contrast bar the file documents four
lines above it — 2.35:1 on the field placeholder and 2.86:1 on
`.heroStats dd`. Retuned `--boss-muted` / `--boss-muted-2`; both now
clear 4.5:1 against the darkest stop of the stage gradient.
- Light mode painted dark first (theme applied from an effect). Fixed by
the `prefers-color-scheme` mirror above.
- The invitation screen asserted 验证码暂未发送, but `back()` re-enters that
step from verification where an SMS *had* gone out. It states the
condition now.
- 验证并进入工作区 / 正在进入您的 ZooWork 工作区 lied for `return_to` arrivals, which go
back to the campaign. Both are conditional.
- Removing the kickers left `.title`'s kicker-gap as dead space; zeroed
only where the title leads.

## Scope

`/bossclaw` is untouched — the wizard's components are not in this diff.
The shared `bossclaw.module.css` gains login-only rules; every light
rule is behind `[data-boss-theme]` or `prefers-color-scheme`, and the
wizard never sets that attribute.

Also widens `bossclaw-subset-fonts.sh` to scan `invitation/` as well. It
only scanned `bossclaw/`, so login copy never reached the glyph set —
the characters happened to be covered by the wizard's copy, not by
design.

## Testing

`bash scripts/verify-web.sh` green: guards + `tsc` + **108 vitest** +
eslint.

New coverage: the gate renders with `aria-modal` over a still-mounted
phone screen, dismisses back to it, the SMS field keeps `one-time-code`
+ `maxlength=6` while six boxes mirror it, non-digits are stripped, the
destination copy is conditional, and the theme hook's OS listener
detaches on unmount (its own helper existed for this and never asserted
it).

Rendered at 1440 / 390 in both themes.

## Known gaps

- **Android hardware back** leaves the page rather than closing the
gate. A `history.pushState` sentinel raced the App Router into a
`popstate` that dismissed the dialog on the same tick it opened, so the
step snapped straight back to the phone screen; it was removed. Doing
this properly needs intercepting routes. Behaviour matches what shipped
before, so this is not a regression.
- `lib/auth/manager.ts` still throws an error naming
`marketing@zooclaw.ai` and "注册bossclaw". It can surface on this page,
but the module is shared with the wizard, so changing it would alter
wizard-visible copy — left for a separate call.
- The brand panel names 微信 · 企微 · 飞书. zoowork.ai's marketing copy names
Slack / Teams / Lark and does not name WeChat (they exist as product
connectors). Kept deliberately for the domestic invited-enterprise
audience; flagging in case this should follow the site.
```

### PR Description

```
## What

Reworks `/invitation/login` — the invited-trial entry into ZooWork Business — and leaves the `/bossclaw` campaign wizard alone.

The old flow had a specific failure: you typed a phone number, landed on a code field, and assumed the SMS was on its way. It wasn't — that field wanted an **invitation code**, and no SMS is sent until the code passes. People sat waiting for a message that was never sent.

## Changes

**Invite code is now a gate, not a step.** It opens as a dialog over the phone screen, which stays visible underneath. That frames it as "one more thing before we continue" instead of "you advanced, here is the code field", and carries the ceremony the route is named after. The dialog restates the phone it is acting on, says outright that the SMS only goes out once the code passes, shows a worked example (`例如 ZC-64ACFC`), and points at `sales@zoowork.ai` for anyone without an invite.

It is hand-rolled rather than `@/components/ds/dialog`: this is a branded module with a fixed palette and the shadcn primitive's `bg-popover` / `bg-card` tokens cascade against it (per `web/app/AGENTS.md` → Branded modules). It reuses the repo's `useBodyLock` + `useEscapeKey`, focuses the code field on open, traps focus, and is flex-centred inside a scrollable overlay so a mobile keyboard can scroll it into view rather than pinning it underneath.

**SMS step says what it wants.** Copy names 短信验证码 explicitly, and the code renders as six boxes so it reads as a 6-digit SMS code rather than a free-text field. One real input is stretched transparently across the boxes instead of six separate inputs — that keeps iOS one-time-code autofill, paste and backspace working with no cross-input focus juggling. Resend became a quiet inline link and 返回上一步 a de-emphasised text link.

**Dropped the STEP kickers.** The numbering read as chrome; the headline already says where you are.

**Copy rebuilt from zoowork.ai's own claims** — 不只是回答 / 交付真实成果, 按角色限权, 行业模板. Removed 工作区 and Agent Pack from the brand panel: both are internal vocabulary that appears nowhere on the marketing site. Contact address is `sales@zoowork.ai`.

**Light theme with a toggle** (bottom-right, follows the OS by default). The palette is mirrored under `prefers-color-scheme` and the `data-boss-theme` attribute is only stamped for an explicit choice, so the default path resolves in CSS with no JS and no dark first paint — verified before hydration.

## Review fixes folded in

A multi-agent adversarial pass produced 35 findings; 18 survived independent verification and are fixed here. The substantive ones:

- The light palette failed the contrast bar the file documents four lines above it — 2.35:1 on the field placeholder and 2.86:1 on `.heroStats dd`. Retuned `--boss-muted` / `--boss-muted-2`; both now clear 4.5:1 against the darkest stop of the stage gradient.
- Light mode painted dark first (theme applied from an effect). Fixed by the `prefers-color-scheme` mirror above.
- The invitation screen asserted 验证码暂未发送, but `back()` re-enters that step from verification where an SMS *had* gone out. It states the condition now.
- 验证并进入工作区 / 正在进入您的 ZooWork 工作区 lied for `return_to` arrivals, which go back to the campaign. Both are conditional.
- Removing the kickers left `.title`'s kicker-gap as dead space; zeroed only where the title leads.

## Scope

`/bossclaw` is untouched — the wizard's components are not in this diff. The shared `bossclaw.module.css` gains login-only rules; every light rule is behind `[data-boss-theme]` or `prefers-color-scheme`, and the wizard never sets that attribute.

Also widens `bossclaw-subset-fonts.sh` to scan `invitation/` as well. It only scanned `bossclaw/`, so login copy never reached the glyph set — the characters happened to be covered by the wizard's copy, not by design.

## Testing

`bash scripts/verify-web.sh` green: guards + `tsc` + **108 vitest** + eslint.

New coverage: the gate renders with `aria-modal` over a still-mounted phone screen, dismisses back to it, the SMS field keeps `one-time-code` + `maxlength=6` while six boxes mirror it, non-digits are stripped, the destination copy is conditional, and the theme hook's OS listener detaches on unmount (its own helper existed for this and never asserted it).

Rendered at 1440 / 390 in both themes.

## Known gaps

- **Android hardware back** leaves the page rather than closing the gate. A `history.pushState` sentinel raced the App Router into a `popstate` that dismissed the dialog on the same tick it opened, so the step snapped straight back to the phone screen; it was removed. Doing this properly needs intercepting routes. Behaviour matches what shipped before, so this is not a regression.
- `lib/auth/manager.ts` still throws an error naming `marketing@zooclaw.ai` and "注册bossclaw". It can surface on this page, but the module is shared with the wizard, so changing it would alter wizard-visible copy — left for a separate call.
- The brand panel names 微信 · 企微 · 飞书. zoowork.ai's marketing copy names Slack / Teams / Lark and does not name WeChat (they exist as product connectors). Kept deliberately for the domestic invited-enterprise audience; flagging in case this should follow the site.

```

---
