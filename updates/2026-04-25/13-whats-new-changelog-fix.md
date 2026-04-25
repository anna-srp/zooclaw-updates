---
title: "版本更新弹窗修复：What's New 正确跳转 changelog 页"
type: "Bug Fix"
priority: "中"
date: "2026-04-25"
status: "待审核"
channels: "Discord + changelog"
---

# 版本更新弹窗修复：What's New 正确跳转 changelog 页

## 核心宣传点

修复了版本更新提示弹窗中「了解更多」按钮无法正确跳转到独立 changelog 页面的问题。

## 原始内容

Commit: 584221fb6915c9aa51d2f534e0f26705c090b5ae

Message:
fix(web): 版本更新弹窗 What's new 跳转独立 changelog 页 (#1262)

## 改动说明
  `VersionUpgradeWidget` 里的 "What's new" 按钮原本跳本地
  `/${locale}/changelog`，改为统一跳到
  `https://zooclaw.ai/tips/changelog`。changelog 已迁至独立的
  [zooclaw-tips](https://github.com/SerendipityOneInc/zooclaw-tips)
  站点维护，内容更新无需再部署主仓。

  ## 净改动
  1 个文件，**+1 / -4**

  | 文件 | 变更 |
  |---|---|
| `web/src/components/VersionUpgradeWidget.tsx` | "What's new" 按钮
onClick
  从拼本地 locale 路径改成直接 `window.open` 外链，加上 `noopener,noreferrer`
  防跨源 tabnabbing |

  ## 测试计划
  - [ ] 版本更新弹窗出现时（chat 页 `versionCheck.needsUpgrade ===
  true`），点击 "What's new" 在新标签页打开
  `https://zooclaw.ai/tips/changelog`
  - [ ] `code-quality / lint-and-test` CI 通过

Co-authored-by: Lynn Zhuang <lynnzhuang@LynndeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

PR Description:
 ## 改动说明
  `VersionUpgradeWidget` 里的 "What's new" 按钮原本跳本地
  `/${locale}/changelog`，改为统一跳到
  `https://zooclaw.ai/tips/changelog`。changelog 已迁至独立的
  [zooclaw-tips](https://github.com/SerendipityOneInc/zooclaw-tips)
  站点维护，内容更新无需再部署主仓。

  ## 净改动
  1 个文件，**+1 / -4**

  | 文件 | 变更 |
  |---|---|
  | `web/src/components/VersionUpgradeWidget.tsx` | "What's new" 按钮 onClick
  从拼本地 locale 路径改成直接 `window.open` 外链，加上 `noopener,noreferrer`
  防跨源 tabnabbing |

  ## 测试计划
  - [ ] 版本更新弹窗出现时（chat 页 `versionCheck.needsUpgrade ===
  true`），点击 "What's new" 在新标签页打开
  `https://zooclaw.ai/tips/changelog`
  - [ ] `code-quality / lint-and-test` CI 通过
