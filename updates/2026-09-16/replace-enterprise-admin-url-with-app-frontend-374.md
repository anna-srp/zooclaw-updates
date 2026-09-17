---
title: "fix(organization): replace enterprise admin URL with app frontend (#3746)"
type: "Bug 修复"
priority: "中"
date: "2026-09-16"
status: "待审核"
channels: ""
---

# fix(organization): replace enterprise admin URL with app frontend (#3746)

## 核心宣传点

## Summary

- Build organization invitation links from `APP_FRONTEND_URL` and send invitees to `/join?orgId=...&code=...` on the main Web app.
- Remove `ENTERPRISE_ADMIN_URL` from claw-interface settings, checkout redirect allowlists, and the Airwallex vertical-pack capability gate.
- Fail closed when invite email delivery is configured but `APP_FRONTEND_URL` is missing, and URL-encode invitation query values.
- Add regression coverage for invitation links and for rejecting legacy Business redirect hosts in both checkout paths.

Refs #3727.

## Root cause

Business organization management moved into the main Web app in #3715, but claw-interface still preferred the old enterprise-admin base URL for invitation emails. The same retired setting remained in vertical checkout capability and redirect-host validation, so runtime behavior still depended on the Business deployment.

This PR intentionally does not preserve or redirect legacy Business URLs. The external Vertical Plan CTA and callback URLs are tracked separately in [zooclaw-vertical-plan#83](https://github.com/SerendipityOneInc/zooclaw-vertical-plan/issues/83).

## Test plan

- [x] `python -m pytest` for the seven affected unit-test modules: 199 passed.
- [x] `bash scripts/verify-py.sh`: Ruff, Ruff format, Pyright, and import-linter passed.
- [ ] Deploy claw-interface to staging and confirm `APP_FRONTEND_URL=https://ecap.gensmo.nosay.live`.
- [ ] Invite an unused test email from staging, verify the email URL starts with `https://ecap.gensmo.nosay.live/join`, and complete login/OTP plus organization join.
- [ ] Before production rollout, confirm `APP_FRONTEND_URL=https://zoowork.ai` and coordinate the Vertical Plan callback migration tracked in zooclaw-vertical-plan#83.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `95da5f1c1ad7b9d398ec183f849775e016924ba0`
- PR: #3746
- 作者：finn-srp
- 日期：2026-09-16T06:00:59Z

### Commit Message

```
fix(organization): replace enterprise admin URL with app frontend (#3746)

## Summary

- Build organization invitation links from `APP_FRONTEND_URL` and send
invitees to `/join?orgId=...&code=...` on the main Web app.
- Remove `ENTERPRISE_ADMIN_URL` from claw-interface settings, checkout
redirect allowlists, and the Airwallex vertical-pack capability gate.
- Fail closed when invite email delivery is configured but
`APP_FRONTEND_URL` is missing, and URL-encode invitation query values.
- Add regression coverage for invitation links and for rejecting legacy
Business redirect hosts in both checkou
```
