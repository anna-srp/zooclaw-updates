---
title: "Specialist Hub 页面应用全新设计系统"
type: "体验优化"
priority: "低"
date: "2026-07-01"
status: "待审核"
channels: ""
---
# Specialist Hub 页面应用全新设计系统
## 核心宣传点
Specialist Hub（专家/Agent 管理页）改用统一的设计系统组件，卡片、标签、按钮、弹窗等视觉更统一协调，页面观感更专业。
## 原始内容
feat(web): apply design system to specialist hub (#2679)

## Summary
- Apply `@zooclaw/design-system` components to the Specialist Hub page:
cards, tags, tabs, dialog, dropdown, buttons, inputs, alerts, and
skeletons.
- Tune the actual `/agents-manager` page shell: neutral page background,
white Specialist Hub panel, diffuse shadows, unclipped card/panel
shadows, and scrollbar placement at the panel edge.
- Add app-side design-system wiring via workspace dependency, token
import, Tailwind source scan, and Next transpilation.

## Verification
- `bash scripts/verify-web.sh 'web/app/next.config.ts'
'web/app/package.json'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/AgentsManagerClient.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentCard.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentCard.module.css'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentModal.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/SkillTags.tsx'
'web/app/src/app/globals.css' 'web/app/src/components/AppLayout.tsx'
'web/app/src/components/ClawConnectionStatus.tsx'`
- pre-commit frontend lint
- pre-push changed-surface verification

## Notes
- Local generated `.next.old*` folders and the temporary
`ds-pilot-preview` route were not included.

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>

---

### PR Description

## Summary
- Apply `@zooclaw/design-system` components to the Specialist Hub page: cards, tags, tabs, dialog, dropdown, buttons, inputs, alerts, and skeletons.
- Tune the actual `/agents-manager` page shell: neutral page background, white Specialist Hub panel, diffuse shadows, unclipped card/panel shadows, and scrollbar placement at the panel edge.
- Add app-side design-system wiring via workspace dependency, token import, Tailwind source scan, and Next transpilation.

## Verification
- `bash scripts/verify-web.sh 'web/app/next.config.ts' 'web/app/package.json' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/AgentsManagerClient.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentCard.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentCard.module.css' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/AgentModal.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agents-manager/_components/SkillTags.tsx' 'web/app/src/app/globals.css' 'web/app/src/components/AppLayout.tsx' 'web/app/src/components/ClawConnectionStatus.tsx'`
- pre-commit frontend lint
- pre-push changed-surface verification

## Notes
- Local generated `.next.old*` folders and the temporary `ds-pilot-preview` route were not included.

