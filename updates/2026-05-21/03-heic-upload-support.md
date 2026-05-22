---
title: "支持 iPhone HEIC 格式图片上传"
type: "Bug Fix"
priority: "中"
date: "2026-05-21"
status: "待审核"
channels: "Discord, changelog"
---

# 支持 iPhone HEIC 格式图片上传

## 核心宣传点

用 iPhone 拍的照片（HEIC/HEIF 格式）现在可以直接上传对话，不再需要手动转换格式。

## 原始内容

```
fix(chat): support HEIC image upload previews (#1838)

- Convert HEIC/HEIF uploads to JPEG before R2 and Mattermost upload handling.
- Avoid rendering raw HEIC blobs as pending Mattermost previews, then swap to the converted JPEG preview.
- Return the actual uploaded File from R2 uploads so chat asset metadata records post-conversion name/type/size.

PR Description:
Convert HEIC/HEIF uploads to JPEG before R2 and Mattermost upload handling. Use the converted JPEG File for Mattermost sourceUrl attachment previews. Persist normalized HEIC upload metadata in GenClaw asset records so stored .jpg assets are not recorded with wrong type.
```
