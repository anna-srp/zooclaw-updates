---
title: "新建对话页的智能体名称与头像与侧边栏保持一致"
type: "体验优化"
priority: "低"
date: "2026-06-16"
status: "待审核"
channels: ""
---
# 新建对话页的智能体名称与头像与侧边栏保持一致
## 核心宣传点
新建对话时显示的智能体名称和头像，现在与侧边栏完全一致，身份展示更清晰统一。
## 原始内容
fix(web): align new chat agent identity (#2491)

## Summary
- Align /new-chat selected agent name and avatar resolution with the
sidebar.
- Reuse one presentation resolver for the headline, composer
placeholder, and selector chips.
- Add regression coverage for customized specialist identity plus
workspace avatar precedence.

## Tests
- `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/new-chat/agentIdentity.ts'
'web/app/src/app/[locale]/(app)/new-chat/useViewModel.ts'
'web/app/src/app/[locale]/(app)/new-chat/components/AgentSelector.tsx'
'web/app/src/app/[locale]/(app)/new-chat/NewChatClient.tsx'
'web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx'
'web/app/tests/unit/app/new-chat/AgentSelector.unit.spec.tsx'`

---

## PR Description

## Summary
- Align /new-chat selected agent name and avatar resolution with the sidebar.
- Reuse one presentation resolver for the headline, composer placeholder, and selector chips.
- Add regression coverage for customized specialist identity plus workspace avatar precedence.

## Tests
- `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/new-chat/agentIdentity.ts' 'web/app/src/app/[locale]/(app)/new-chat/useViewModel.ts' 'web/app/src/app/[locale]/(app)/new-chat/components/AgentSelector.tsx' 'web/app/src/app/[locale]/(app)/new-chat/NewChatClient.tsx' 'web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx' 'web/app/tests/unit/app/new-chat/AgentSelector.unit.spec.tsx'`

