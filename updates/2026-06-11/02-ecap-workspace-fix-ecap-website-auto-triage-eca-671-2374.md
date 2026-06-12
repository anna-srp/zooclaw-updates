---
title: "超大图片上传自动压缩，不再上传失败"
type: "体验优化"
priority: "中"
date: "2026-06-11"
status: "待审核"
channels: ""
---

# 超大图片上传自动压缩，不再上传失败

## 核心宣传点
上传超过尺寸限制的图片时，系统会自动压缩后再上传，不再直接报错，发图更省心。

## 原始内容
```
fix(ecap-website): auto-triage ECA-671 (#2374)

## Linear issue

[ECA-671](https://linear.app/srpone/issue/ECA-671/frontend-mattermosterror-image-dimension-exceeds-upload-limit)
— Frontend MattermostError: image dimension exceeds upload limit

**Affected service**: `ecap-website`

## Root cause
The Mattermost attachment upload path validated file size and count in
`GenClawInput`, but not image pixel dimensions. Images above the
server's `FileSettings.MaxImageResolution` were uploaded, rejected with
a 400 `MattermostError`, and reported to Sentry by `useMmAttachments` as
if they were unexpected upload failures.

## Fix (reworked after review)
The original auto-fix hardcoded a client-side limit and rejected
oversized images. That was reworked per human review:

- **Auto-downscale instead of reject**: images above the limit are
downscaled client-side (aspect-preserving, `createImageBitmap` + canvas;
JPEG q0.9, PNG kept as PNG, GIFs skipped to preserve animation) and
uploaded successfully — same precedent as the existing HEIC→JPEG
normalization.
- **Corrected the limit**: Mattermost's default `MaxImageResolution` is
**33,177,600 px (7680×4320)**, not 6048×4032 as the original PR claimed.
The wrong constant would have blocked 24.4–33.2MP images the server
accepts.
- **Server-authoritative backstop**: the limit is server-configurable
and *not* exposed via `/api/v4/config/client` (verified in
`mattermost/server/config/client.go`), so `uploadFile` now captures the
machine-readable error id (`MattermostError.serverErrorId`) and
dimension rejections trigger retries at halved pixel budgets (default →
1/2 → 1/4). This covers deployments configured below the default.
- **Sentry policy**: in-loop dimension rejections are expected and stay
out of Sentry. An exhausted downgrade sequence (server rejects even 1/4
of the default) is unexpected and **is** reported via `captureChatError`
with `imageDowngradeExhausted: true` and the attempted budgets.
- Exhausted-downgrade failures render a non-retryable "Image too large"
chip (manual retry is pointless — automatic downgrades already ran).

## Verification
- 9 new unit tests for `downscaleImageToMmLimit` (scaling math, aspect
ratio, PNG/JPEG/GIF handling, fail-open paths).
- Hook tests for: downscaled upload, downgrade-retry success,
exhausted-downgrade reporting, re-attach path, non-retryable failure.
- `serverErrorId` propagation test in the MM API spec.
- Full unit suite (7103 tests), `tsc --noEmit`, `lint:ci` (knip
dep-health gate that failed before), and jscpd all pass locally.

## Risks / scope
- The 33,177,600 baseline matches MM defaults (our deployment's
`MaxFileSize` copy also matches defaults); if a server is configured
lower, the downgrade loop absorbs it at the cost of one extra upload
round-trip.
- Canvas re-encode drops EXIF metadata (orientation is baked in by
`createImageBitmap`); acceptable for chat attachments.

---
*This PR was opened automatically by the ECAP error-scanner and
subsequently reworked under human review.*

*Auto-merge is disabled for `auto-triage` labeled PRs; merging requires
explicit human approval.*

---------

Co-authored-by: ecap-error-scanner[bot] <ecap-error-scanner[bot]@users.noreply.github.com>
Co-authored-by: chris-srp <chris@srp.one>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>

--- PR Description ---

## Linear issue
[ECA-671](https://linear.app/srpone/issue/ECA-671/frontend-mattermosterror-image-dimension-exceeds-upload-limit) — Frontend MattermostError: image dimension exceeds upload limit

**Affected service**: `ecap-website`

## Root cause
The Mattermost attachment upload path validated file size and count in `GenClawInput`, but not image pixel dimensions. Images above the server's `FileSettings.MaxImageResolution` were uploaded, rejected with a 400 `MattermostError`, and reported to Sentry by `useMmAttachments` as if they were unexpected upload failures.

## Fix (reworked after review)
The original auto-fix hardcoded a client-side limit and rejected oversized images. That was reworked per human review:

- **Auto-downscale instead of reject**: images above the limit are downscaled client-side (aspect-preserving, `createImageBitmap` + canvas; JPEG q0.9, PNG kept as PNG, GIFs skipped to preserve animation) and uploaded successfully — same precedent as the existing HEIC→JPEG normalization.
- **Corrected the limit**: Mattermost's default `MaxImageResolution` is **33,177,600 px (7680×4320)**, not 6048×4032 as the original PR claimed. The wrong constant would have blocked 24.4–33.2MP images the server accepts.
- **Server-authoritative backstop**: the limit is server-configurable and *not* exposed via `/api/v4/config/client` (verified in `mattermost/server/config/client.go`), so `uploadFile` now captures the machine-readable error id (`MattermostError.serverErrorId`) and dimension rejections trigger retries at halved pixel budgets (default → 1/2 → 1/4). This covers deployments configured below the default.
- **Sentry policy**: in-loop dimension rejections are expected and stay out of Sentry. An exhausted downgrade sequence (server rejects even 1/4 of the default) is unexpected and **is** reported via `captureChatError` with `imageDowngradeExhausted: true` and the attempted budgets.
- Exhausted-downgrade failures render a non-retryable "Image too large" chip (manual retry is pointless — automatic downgrades already ran).

## Verification
- 9 new unit tests for `downscaleImageToMmLimit` (scaling math, aspect ratio, PNG/JPEG/GIF handling, fail-open paths).
- Hook tests for: downscaled upload, downgrade-retry success, exhausted-downgrade reporting, re-attach path, non-retryable failure.
- `serverErrorId` propagation test in the MM API spec.
- Full unit suite (7103 tests), `tsc --noEmit`, `lint:ci` (knip dep-health gate that failed before), and jscpd all pass locally.

## Risks / scope
- The 33,177,600 baseline matches MM defaults (our deployment's `MaxFileSize` copy also matches defaults); if a server is configured lower, the downgrade loop absorbs it at the cost of one extra upload round-trip.
- Canvas re-encode drops EXIF metadata (orientation is baked in by `createImageBitmap`); acceptable for chat attachments.

---
*This PR was opened automatically by the ECAP error-scanner and subsequently reworked under human review.*

*Auto-merge is disabled for `auto-triage` labeled PRs; merging requires explicit human approval.*

```
