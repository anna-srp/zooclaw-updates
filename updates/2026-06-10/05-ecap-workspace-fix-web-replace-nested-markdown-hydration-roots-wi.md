---
title: "聊天消息渲染稳定性修复"
type: "Bug Fix"
priority: "中"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# 聊天消息渲染稳定性修复

## 核心宣传点
修复了流式输出聊天消息时偶发的页面渲染崩溃问题，长消息和卡片展示更稳定流畅。

## 原始内容
```
fix(web): replace nested markdown hydration roots with segment rendering (ECA-765) (#2337)

## Summary
- 根治 Sentry ECA-765(\`removeChild\` / \`insertBefore\` NotFoundError):消灭
\`MarkdownContent\` 的"\`dangerouslySetInnerHTML\` + 嵌套 \`createRoot\`"双
React root 反模式
- 新增 token 级分段渲染:\`parse-markdown-segments\` 在顶层 code fence 处切分文档,ERMP /
specialist 卡片成为主树的**真 React 子组件**(\`ERMPCardSegment\` /
\`SpecialistCardSlot\`,\`next/dynamic\` 懒加载保持 code-split),其余 token 段沿用现有
marked renderer 输出 per-segment sanitized HTML
- 取代并关闭止血 PR #2327;设计 spec 见
\`docs/superpowers/specs/2026-06-10-markdown-segment-rendering.md\`

## Root cause
外层 React tree 通过 \`dangerouslySetInnerHTML\` 拥有整段消息 HTML,hydration
effect 又用 \`createRoot()\` 往这段 HTML 内部的占位 div 挂嵌套 root——同一块 DOM 被两个 root
管理。流式输出时 content 每 token 一变:外层 root 在 **mutation 阶段**重写 innerHTML 铲掉嵌套
root 的 host 节点,嵌套 root 的 \`unmount()\` 在更晚的 **passive
阶段**才执行,此时其子节点已不在树上 → NotFoundError。

实现中还发现一个放大因素:**React 19 对 \`dangerouslySetInnerHTML\` 按对象身份 diff**(不比较
\`__html\` 字符串),内联 \`{{__html}}\` 字面量导致任何父级 re-render 都无条件重写
innerHTML——旧代码的触发面远不止 content 变化。新实现用 \`React.memo\` 的 \`HtmlSegment\`
让相同 html 字符串直接 bail out(load-bearing,非优化),流式时未变段 DOM 零重写。

行为变化台账(详见 spec):
1. \`suppressSpecialistCards\` 从 \`display:none\` 占位 div 变为不渲染(等价,数据在
React state 不需 DOM 占位存活)
2. 嵌套(blockquote/list 内)卡片 fence 从不可见空 div 退化为**可见** code
block(契约:卡片只在顶层 fence)
3. raw-HTML 注入的占位 div 不再是 hydration 向量;\`data-ermp-*\` / \`data-zc-*\`
移出 DOMPurify allowlist(src 内零 producer)
4. 卡片 payload 不再 encodeURIComponent 往返 DOM 属性

## Test plan
- [x] characterization 锁(重构前提交,跨重构原封不动通过):ERMP
happy/invalid、unknown-kind / 空 agent-id 降级、混合消息、**ERMP 流式挂载(ECA-765
触发场景)**、跨 fence reference 链接
- [x] 分段器单测含等价性属性测试:无卡片输入的分段输出与 \`renderMarkdownToHtml\` 字节级相同
- [x] ECA-765 专属回归:流式追加时前段 DOM **节点引用恒等**;卡片挂载中整体替换 content 正常卸载不抛错
- [x] 全量 unit suite 7023 passed / \`tsc --noEmit\` / \`pnpm lint\` /
\`pnpm dup\` 全过(\`react-hooks-config\` lint-contract 测试在本机全量并行下偶发 10s
超时,隔离运行通过,与本 diff 无交集)
- [ ] 手测:\`/chat\` 流式含 \`\`\`ecap-card 消息无控制台错误、卡片可交互;\`/new-chat\` →
session thread;hire/fire consent i18n 消息组装;图片 blur / file card / 视频缩略图 /
shiki / 分享回放
- [ ] 合并上线后观察 Sentry ECA-765:新增 NotFoundError 应归零(残留即浏览器扩展噪声,可借此区分归因)

后续 follow-up(不进本 PR):删 \`translate\` prop、Slot 直接
\`useTranslation()\`、\`humanizeAgentId\` 移 util 文件。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>

---

### PR Description

## Summary
- 根治 Sentry ECA-765(\`removeChild\` / \`insertBefore\` NotFoundError):消灭 \`MarkdownContent\` 的"\`dangerouslySetInnerHTML\` + 嵌套 \`createRoot\`"双 React root 反模式
- 新增 token 级分段渲染:\`parse-markdown-segments\` 在顶层 code fence 处切分文档,ERMP / specialist 卡片成为主树的**真 React 子组件**(\`ERMPCardSegment\` / \`SpecialistCardSlot\`,\`next/dynamic\` 懒加载保持 code-split),其余 token 段沿用现有 marked renderer 输出 per-segment sanitized HTML
- 取代并关闭止血 PR #2327;设计 spec 见 \`docs/superpowers/specs/2026-06-10-markdown-segment-rendering.md\`

## Root cause
外层 React tree 通过 \`dangerouslySetInnerHTML\` 拥有整段消息 HTML,hydration effect 又用 \`createRoot()\` 往这段 HTML 内部的占位 div 挂嵌套 root——同一块 DOM 被两个 root 管理。流式输出时 content 每 token 一变:外层 root 在 **mutation 阶段**重写 innerHTML 铲掉嵌套 root 的 host 节点,嵌套 root 的 \`unmount()\` 在更晚的 **passive 阶段**才执行,此时其子节点已不在树上 → NotFoundError。

实现中还发现一个放大因素:**React 19 对 \`dangerouslySetInnerHTML\` 按对象身份 diff**(不比较 \`__html\` 字符串),内联 \`{{__html}}\` 字面量导致任何父级 re-render 都无条件重写 innerHTML——旧代码的触发面远不止 content 变化。新实现用 \`React.memo\` 的 \`HtmlSegment\` 让相同 html 字符串直接 bail out(load-bearing,非优化),流式时未变段 DOM 零重写。

行为变化台账(详见 spec):
1. \`suppressSpecialistCards\` 从 \`display:none\` 占位 div 变为不渲染(等价,数据在 React state 不需 DOM 占位存活)
2. 嵌套(blockquote/list 内)卡片 fence 从不可见空 div 退化为**可见** code block(契约:卡片只在顶层 fence)
3. raw-HTML 注入的占位 div 不再是 hydration 向量;\`data-ermp-*\` / \`data-zc-*\` 移出 DOMPurify allowlist(src 内零 producer)
4. 卡片 payload 不再 encodeURIComponent 往返 DOM 属性

## Test plan
- [x] characterization 锁(重构前提交,跨重构原封不动通过):ERMP happy/invalid、unknown-kind / 空 agent-id 降级、混合消息、**ERMP 流式挂载(ECA-765 触发场景)**、跨 fence reference 链接
- [x] 分段器单测含等价性属性测试:无卡片输入的分段输出与 \`renderMarkdownToHtml\` 字节级相同
- [x] ECA-765 专属回归:流式追加时前段 DOM **节点引用恒等**;卡片挂载中整体替换 content 正常卸载不抛错
- [x] 全量 unit suite 7023 passed / \`tsc --noEmit\` / \`pnpm lint\` / \`pnpm dup\` 全过(\`react-hooks-config\` lint-contract 测试在本机全量并行下偶发 10s 超时,隔离运行通过,与本 diff 无交集)
- [ ] 手测:\`/chat\` 流式含 \`\`\`ecap-card 消息无控制台错误、卡片可交互;\`/new-chat\` → session thread;hire/fire consent i18n 消息组装;图片 blur / file card / 视频缩略图 / shiki / 分享回放
- [ ] 合并上线后观察 Sentry ECA-765:新增 NotFoundError 应归零(残留即浏览器扩展噪声,可借此区分归因)

后续 follow-up(不进本 PR):删 \`translate\` prop、Slot 直接 \`useTranslation()\`、\`humanizeAgentId\` 移 util 文件。

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```
