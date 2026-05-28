---
title: "文件上传稳定性优化：自动重试临时失败"
type: "Bug Fix"
priority: "中"
date: "2026-05-27"
status: "待审核"
channels: ""
---

# 文件上传稳定性优化：自动重试临时失败

## 核心宣传点

文件上传遇到临时网络问题时会自动重试，减少因偶发错误导致的上传失败。

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**SHA**: [6a0dc589](https://github.com/SerendipityOneInc/ecap-workspace/commit/6a0dc58929df2f25ef03ec15d3ab408c912b2d0a)
**PR**: [#1972](https://github.com/SerendipityOneInc/ecap-workspace/pull/1972)  
**作者**: sam-srp  
**日期**: 2026-05-27T07:50:55Z

**Commit Message:**

```
fix(claw-interface): retry transient R2 upload failures (#1972)

## Linear

https://linear.app/srpone/issue/ECA-717/asr-audio-record-dropped-r2-upload-fails-after-successful

## Summary
- add bounded retry handling for transient R2 upload failures in
`R2StorageClient.upload_data`
- retry request errors, timeouts, HTTP 429, and HTTP 5xx responses while
preserving immediate failure for non-retryable statuses such as 403
- add unit coverage for successful retry, non-retryable status, and
exhausted retry behavior

## Root Cause
ASR persistence drops records when `r2.upload_data` raises. A transient
R2 timeout, rate limit, or 5xx could therefore cause a successfully
transcribed audio record to be lost before Mongo persistence.

## Validation
- `conda run -n base python -m pytest tests/unit/test_r2_storage.py`
- `conda run -n base python -m ruff check app/services/r2_storage.py
tests/unit/test_r2_storage.py`
- `conda run -n base pyright app/services/r2_storage.py
tests/unit/test_r2_storage.py`
```


**PR Description:**

## Linear
https://linear.app/srpone/issue/ECA-717/asr-audio-record-dropped-r2-upload-fails-after-successful

## Summary
- add bounded retry handling for transient R2 upload failures in `R2StorageClient.upload_data`
- retry request errors, timeouts, HTTP 429, and HTTP 5xx responses while preserving immediate failure for non-retryable statuses such as 403
- add unit coverage for successful retry, non-retryable status, and exhausted retry behavior

## Root Cause
ASR persistence drops records when `r2.upload_data` raises. A transient R2 timeout, rate limit, or 5xx could therefore cause a successfully transcribed audio record to be lost before Mongo persistence.

## Validation
- `conda run -n base python -m pytest tests/unit/test_r2_storage.py`
- `conda run -n base python -m ruff check app/services/r2_storage.py tests/unit/test_r2_storage.py`
- `conda run -n base pyright app/services/r2_storage.py tests/unit/test_r2_storage.py`
