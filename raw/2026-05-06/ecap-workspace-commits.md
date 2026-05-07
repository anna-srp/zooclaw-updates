# ecap-workspace Commits — 2026-05-06

## dd3c1f56 — 2026-05-06
**Author:** bryce-srp
**SHA:** dd3c1f56ea3808c863c6786b026b33cacf8db61d
**Stats:** +1797 -156 (1953 changes)

### Commit Message
```
feat(claw-interface): payment fulfillment saga with Mongo tx + compensation (#1565)

## Summary

- Wraps post-payment fulfillment (user + order writes) in a **Mongo
multi-document transaction** so the two writes are atomic — closes the
pre-existing race where `user_repo.update_fields` succeeded but
`mark_entitlement_granted` then failed, letting the next webhook retry
reclaim the stale lock and double-grant via Billing Gateway.
- Adds a **saga compensation path** that automatically refunds the
customer when either the BG grant call or the local commit fails,
instead of leaving an asymmetric state (charged but no entitlement, or
BG granted but local DB lost).
- Adds BG-side idempotency via `transaction_id` derived from `order_id`,
and a multi-path Stripe refund lookup (PI → subscription invoice →
invoice charge) that handles subscription orders whose first charge has
no PaymentIntent.
- Frontend: fixes a 1-line crash in `SubscriptionPanel.tsx` when
`plan='free'`, surfaced while testing the saga end-to-end on staging.

## What's in the saga state machine

```
pending → fulfilling
              ├─ ✅ commit_fulfillment_transaction → paid
              └─ ❌ → COMPENSATING
                       ├─ Stripe refund OK → REFUNDED_PENDING_BG_REVOKE  (terminal)
                       └─ Stripe refund FAIL → REFUND_PENDING_RETRY → APScheduler retry
```

The order's `compensation` subdoc stores `bg_grant_transaction_id` (the
BG idempotency key from the failed grant) for a future BG-revoke job to
consume.

## Discoveries during staging end-to-end

- BG `transaction_id` support requires `billing-gateway` ≥ v0.0.19.
Staging was running v0.0.17-beta, which rejected the field with
`extra_forbidden`. **Staging BG was upgraded to v0.0.20-beta in a
separate change** (already deployed) before this PR.
- Subscription orders' first invoice has `payment_intent=None` and bills
via `Invoice.charge` directly — initial saga code only refunded via PI,
hitting a sentinel and silently skipping the refund. Multi-path lookup
added.
- Stripe SDK is inconsistent on attribute vs dict access for newer
fields; defensive `_stripe_get` helper added.

## Out of scope (deferred to follow-up PR)

- Actual revocation of BG-side credits via Lago `voided_credits` — order
persists `compensation.bg_grant_transaction_id` so a future job can
revoke. For now, `refunded_pending_bg_revoke` is the terminal state and
ops can manually clean up via that key.
- Stripe API new `Invoice.payments[]` array (replaces top-level `charge`
field on newer API versions) — current resolver uses legacy `charge`
field which works on staging-deployed Stripe API version.

## Test plan

- [x] **Unit tests pass locally**: `pytest
services/claw-interface/tests/unit/test_stripe_compensation.py -v` (13
cases) and `pytest
services/claw-interface/tests/unit/test_stripe_entitlement_service.py
-v`
- [ ] **CI green** (file-length, ruff, pyright, import-linter, unit
tests, BDD)
- [x] **Staging end-to-end**: ultra subscription upgrade succeeds
(verified user `7391388913366994944` after BG upgrade); BG failure →
saga refund path (was triggered during testing on user
`7442539911170756608` before BG upgrade)
- [ ] **APScheduler retry**: queue a `refund_pending_retry` order, wait
5 min, verify status flips to `refunded_pending_bg_revoke`
- [ ] **Webhook redelivery**: trigger same `checkout.session.completed`
twice via Stripe CLI; verify second delivery is short-circuited by lock
(no double BG grant)

## Frontend fix detail

`web/src/components/billing/SubscriptionPanel.tsx:641`:
```diff
- planName={currentPlan ? PLAN_INFO[currentPlan].name : 'your'}
+ planName={(currentPlan && PLAN_INFO[currentPlan as PlanTier]?.name) || 'your'}
```

`PLAN_INFO['free']` is `undefined`; same `?.` guard already used at line
431 for the `pendingDowngrade` lookup. The `as PlanTier | null` cast at
line 112 was hiding the issue from TypeScript.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description
## Summary

- Wraps post-payment fulfillment (user + order writes) in a **Mongo multi-document transaction** so the two writes are atomic — closes the pre-existing race where `user_repo.update_fields` succeeded but `mark_entitlement_granted` then failed, letting the next webhook retry reclaim the stale lock and double-grant via Billing Gateway.
- Adds a **saga compensation path** that automatically refunds the customer when either the BG grant call or the local commit fails, instead of leaving an asymmetric state (charged but no entitlement, or BG granted but local DB lost).
- Adds BG-side idempotency via `transaction_id` derived from `order_id`, and a multi-path Stripe refund lookup (PI → subscription invoice → invoice charge) that handles subscription orders whose first charge has no PaymentIntent.
- Frontend: fixes a 1-line crash in `SubscriptionPanel.tsx` when `plan='free'`, surfaced while testing the saga end-to-end on staging.

## What's in the saga state machine

```
pending → fulfilling
              ├─ ✅ commit_fulfillment_transaction → paid
              └─ ❌ → COMPENSATING
                       ├─ Stripe refund OK → REFUNDED_PENDING_BG_REVOKE  (terminal)
                       └─ Stripe refund FAIL → REFUND_PENDING_RETRY → APScheduler retry
```

The order's `compensation` subdoc stores `bg_grant_transaction_id` (the BG idempotency key from the failed grant) for a future BG-revoke job to consume.

## Discoveries during staging end-to-end

- BG `transaction_id` support requires `billing-gateway` ≥ v0.0.19. Staging was running v0.0.17-beta, which rejected the field with `extra_forbidden`. **Staging BG was upgraded to v0.0.20-beta in a separate change** (already deployed) before this PR.
- Subscription orders' first invoice has `payment_intent=None` and bills via `Invoice.charge` directly — initial saga code only refunded via PI, hitting a sentinel and silently skipping the refund. Multi-path lookup added.
- Stripe SDK is inconsistent on attribute vs dict access for newer fields; defensive `_stripe_get` helper added.

## Out of scope (deferred to follow-up PR)

- Actual revocation of BG-side credits via Lago `voided_credits` — order persists `compensation.bg_grant_transaction_id` so a future job can revoke. For now, `refunded_pending_bg_revoke` is the terminal state and ops can manually clean up via that key.
- Stripe API new `Invoice.payments[]` array (replaces top-level `charge` field on newer API versions) — current resolver uses legacy `charge` field which works on staging-deployed Stripe API version.

## Test plan

- [x] **Unit tests pass locally**: `pytest services/claw-interface/tests/unit/test_stripe_compensation.py -v` (13 cases) and `pytest services/claw-interface/tests/unit/test_stripe_entitlement_service.py -v`
- [ ] **CI green** (file-length, ruff, pyright, import-linter, unit tests, BDD)
- [x] **Staging end-to-end**: ultra subscription upgrade succeeds (verified user `7391388913366994944` after BG upgrade); BG failure → saga refund path (was triggered during testing on user `7442539911170756608` before BG upgrade)
- [ ] **APScheduler retry**: queue a `refund_pending_retry` order, wait 5 min, verify status flips to `refunded_pending_bg_revoke`
- [ ] **Webhook redelivery**: trigger same `checkout.session.completed` twice via Stripe CLI; verify second delivery is short-circuited by lock (no double BG grant)

## Frontend fix detail

`web/src/components/billing/SubscriptionPanel.tsx:641`:
```diff
- planName={currentPlan ? PLAN_INFO[currentPlan].name : 'your'}
+ planName={(currentPlan && PLAN_INFO[currentPlan as PlanTier]?.name) || 'your'}
```

`PLAN_INFO['free']` is `undefined`; same `?.` guard already used at line 431 for the `pendingDowngrade` lookup. The `as PlanTier | null` cast at line 112 was hiding the issue from TypeScript.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 136e92c5 — 2026-05-06
**Author:** lynn Zhuang
**SHA:** 136e92c5f38e843c3e0e93da56242fa41e46dd51
**Stats:** +273 -0 (273 changes)

### Commit Message
```
feat(web): chat 输入框上方新增快捷动作行（UI shell）  (#1514)

## 改动概要
在 chat 输入框上方加一排 4 个快捷动作 chip：**Quick start** / **Clear Context** /
**Compress Context** / **Tips**。
                                         
  - **Tips** —— 完整接通：点击直接以 `onSendMessage()` 派发本地化的自我介绍 prompt（10    
语言全覆盖）。
- **Quick start** —— UI + popover 完成；popover 内容用 hardcoded PPTX Master
示例（Build
Deck / Polish / Summarize），代码里有注释标记后续要替换为 per-agent backend metadata。
- **Clear Context / Compress Context** —— 有意 stub：渲染完整 + onClick 触发
`logger.warn` TODO。后端 endpoint 还不存在，留作 follow-up PR。
## 视觉/交互
  - chip 排列在输入框上方，左对齐 `ml-4`（与输入框文本左边缘对齐）。                      
- Quick start popover 从按钮上方弹出（`side="top"` + `align="start"`）。
  - Icon 选择按**实际功能**而非设计稿（设计稿原                                         
calendar/chat/collection/question-mark-circle 是占位）：
    - Quick start → `BoltIcon`（⚡ 快速）                        
- Clear Context → `BackspaceIcon`（退格 = 擦除/清空）
- Compress Context → `ArrowsPointingInIcon`（向内收缩 = 压缩）
- Tips → `LightBulbIcon`（💡 提示/想法）
## Out of scope（follow-up PR）
- **Clear Context** 后端：`clear_context` endpoint + chat session 渲染分隔线
- **Compress Context** 后端：`compress_context` endpoint + 4 态 UI 状态机（idle
/
processing / success / error）
- **Quick start** 数据：per-agent quick-command schema（替换
`DEMO_QUICK_COMMANDS`
常量）
## Test plan
- [x] `pnpm exec vitest run ChatQuickActions.unit.spec.tsx` —— 5/5 通过
- render 4 个 chip / Tips 派发本地化 prompt / Quick start 命令派发 hardcoded
prompt /
Clear+Compress 不调用 onSendMessage / disabled 全部禁用
- [x] `pnpm lint` 干净
- [x] `tsc --noEmit` 干净
- [ ] 手动 QA：localhost chat 页面 chip row 视觉与 Figma 一致；Tips 点击后消息进
stream；Clear/Compress 点击后 DevTools console 看到 `logger.warn` TODO 信息
- [ ] 多 locale 视觉抽检（中文 / 阿拉伯 RTL）
                                                                    
<img width="1660" height="612" alt="screenshot-20260430-193139"
src="https://github.com/user-attachments/assets/5dbeff16-6335-450e-bc21-9d7494ff2446"
/>
<img width="2438" height="868" alt="image"
src="https://github.com/user-attachments/assets/5bb99c4a-7f5d-49e1-a74b-42127aed120d"
/>

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@LynndeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>
```

### PR Description
## 改动概要                                                                             
  在 chat 输入框上方加一排 4 个快捷动作 chip：**Quick start** / **Clear Context** /     
  **Compress Context** / **Tips**。                                                       
                                         
  - **Tips** —— 完整接通：点击直接以 `onSendMessage()` 派发本地化的自我介绍 prompt（10    
  语言全覆盖）。                                                                      
  - **Quick start** —— UI + popover 完成；popover 内容用 hardcoded PPTX Master 示例（Build
   Deck / Polish / Summarize），代码里有注释标记后续要替换为 per-agent backend metadata。 
  - **Clear Context / Compress Context** —— 有意 stub：渲染完整 + onClick 触发            
  `logger.warn` TODO。后端 endpoint 还不存在，留作 follow-up PR。                         
                                                                                          
  ## 视觉/交互                                                                          
  - chip 排列在输入框上方，左对齐 `ml-4`（与输入框文本左边缘对齐）。                      
  - Quick start popover 从按钮上方弹出（`side="top"` + `align="start"`）。                
  - Icon 选择按**实际功能**而非设计稿（设计稿原                                         
  calendar/chat/collection/question-mark-circle 是占位）：                                
    - Quick start → `BoltIcon`（⚡ 快速）                        
    - Clear Context → `BackspaceIcon`（退格 = 擦除/清空）                                 
    - Compress Context → `ArrowsPointingInIcon`（向内收缩 = 压缩）                      
    - Tips → `LightBulbIcon`（💡 提示/想法）                                              
                                                                                          
  ## Out of scope（follow-up PR）                                                         
  - **Clear Context** 后端：`clear_context` endpoint + chat session 渲染分隔线            
  - **Compress Context** 后端：`compress_context` endpoint + 4 态 UI 状态机（idle /       
  processing / success / error）                                                          
  - **Quick start** 数据：per-agent quick-command schema（替换 `DEMO_QUICK_COMMANDS`      
  常量）                                                                                  
                                                                                          
  ## Test plan                                                                            
  - [x] `pnpm exec vitest run ChatQuickActions.unit.spec.tsx` —— 5/5 通过                 
    - render 4 个 chip / Tips 派发本地化 prompt / Quick start 命令派发 hardcoded prompt / 
  Clear+Compress 不调用 onSendMessage / disabled 全部禁用                                 
  - [x] `pnpm lint` 干净                                                                  
  - [x] `tsc --noEmit` 干净                                                             
  - [ ] 手动 QA：localhost chat 页面 chip row 视觉与 Figma 一致；Tips 点击后消息进        
  stream；Clear/Compress 点击后 DevTools console 看到 `logger.warn` TODO 信息             
  - [ ] 多 locale 视觉抽检（中文 / 阿拉伯 RTL）                                           
                                                                    
<img width="1660" height="612" alt="screenshot-20260430-193139" src="https://github.com/user-attachments/assets/5dbeff16-6335-450e-bc21-9d7494ff2446" />
<img width="2438" height="868" alt="image" src="https://github.com/user-attachments/assets/5bb99c4a-7f5d-49e1-a74b-42127aed120d" />


---

## f3c7a5ff — 2026-05-06
**Author:** lynn Zhuang
**SHA:** f3c7a5ff34fa8047c9fa788a15cfc56a3325358a
**Stats:** +193 -56 (249 changes)

### Commit Message
```
fix(web): chat 视频改用 240px 缩略图 + 点击打开 lightbox (#1563)

## 改动概要
  Chat 里的视频从「inline 大尺寸内嵌播放器」改成「**240×240 内紧凑缩略图 + 点击打开       
  lightbox 全屏播放**」，跟图片的预览交互对齐。9:16 portrait 视频不再撑爆 viewport。
  ## 用户层面的变化                       
  - **缩略图**：视频显示为 ≤240×240 的小卡片（保留视频原始宽高比），中央叠加白色 play 圆形
icon，hover 加深
- **点击展开**：复用已有 `ImagePreview` 全屏蒙层组件 → autoPlay + controls +
  ESC/点击外侧关闭，跟 agent 生成图片的预览体验完全一致                       
  - **不再溢出**：portrait 9:16 视频之前能渲染到 60vh 高，desktop 上只能看到              
  1/3；现在缩略图模式下根本不占聊天屏幕空间                                 
  ## 涉及的渲染路径（全部统一改造）       
| 路径 | 改动 |
  |------|------|                         
| `MMAttachments.tsx VideoAttachment`（用户上传视频 / agent MM file 附件） | 卡片
wrapper 去掉，改 240×240 button + play overlay + 点击打开 lightbox |
| `MMAttachments.tsx ReplayAttachment`（chat 回放模式 video） | 同上 |
| `render-markdown-to-html.ts renderMarkdownVideo`（agent markdown
`[video:](url)`
语法） | 渲染 thumbnail span + `data-video-url` 属性，play overlay SVG 内联 |
| `render-markdown-to-html.ts normalizeMediaHtml`（agent inline `<video>`
HTML 块） |
size cap 缩到 240×240 |
| `MarkdownContent.tsx` | click handler
加分支：`.markdown-video-thumb[data-video-url]`
路由到 `window.openImagePreview` |
| `ImagePreview.tsx` | 修复 `activeItem` 推导，让 single-item gallery 也能传
`type:
  'video'`（之前硬编码：`length > 1` 才认为是 gallery，单 item 退到顶层 type prop =  
`'image'`，导致单视频被当图片渲染） |
                                          
## 关键实现细节
- **`width: fit-content` / `w-fit`** 是缩略图 wrapper 的关键约束 —— 防止 `<video>`
在
  metadata 加载前被 300×150 默认 intrinsic 尺寸定型 wrapper、加载完成后视频重新尺寸但   
wrapper 不收缩、留出黑色 gap 的 bug
  - **`pointer-events: none`** 在 play overlay 上：让点击穿透到
button/wrapper，不被装饰层拦截
- **`<video>` 不带 `controls`**：原生 controls 会自带 play 按钮等 UI 拦截
click，不能干扰整 wrapper 的 click-to-open
  ## Out of scope（独立 PR）              
  - 多视频 gallery 翻页（现在 single-item 能跑通，多 item 走 prev/next 按钮，但 markdown  
  里多视频时不会自动 batch 成 gallery —— 跟现有图片 gallery 行为对齐还要补一段          
prose-container 扫描逻辑）
  - video poster 图（用 `<video preload="metadata">` 自动取首帧；如果想加显式 poster
走另一套）
## Test plan
- [x] `pnpm lint` 干净
  - [x] `tsc --noEmit` 干净（exit 0）     
- [x] 4 个相关测试文件 130/130 通过（`render-markdown-to-html` / `MarkdownContent`
/
`ImagePreview` / `MMAttachments`）
- [x] 全量 `pnpm test:unit` 通过
- [x] 本地 dev server hard refresh 后视频显示为缩略图，点击打开 lightbox autoPlay
- [ ] 多浏览器抽检（Safari 对 `width: fit-content` + replaced element 的 reflow
行为偶尔有差异）
- [ ] 测试 portrait 9:16（Vibe Drama 输出）/ landscape 16:9 / 用户上传 horizontal
录屏
  三种纵横比都没有黑边                             

<img width="2556" height="1714" alt="screenshot-20260506-170533"
src="https://github.com/user-attachments/assets/1c9828f0-9dc2-4fab-97b7-937bc2bc52aa"
/>
<img width="2540" height="1720" alt="screenshot-20260506-170613"
src="https://github.com/user-attachments/assets/65fe0c97-b027-4e0b-ad86-b3c
<img width="1278" height="847" alt="Screenshot 2026-05-06 at 17 05 51"
src="https://github.com/user-attachments/assets/c6eda2bd-c080-45cb-84e7-8dc3d1c3d0ba"
/>
d33affcb2" />

<img width="2558" height="1712" alt="screenshot-20260506-170622"
src="https://github.com/user-attachments/assets/eeb8d6f8-8e4b-488f-ade2-c55e1427bdee"
/>

before👇
<img width="2552" height="1710" alt="screenshot-20260506-175942"
src="https://github.com/user-attachments/assets/7ec9cea8-cedf-443f-b7da-b1c479365f2b"
/>

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@LynndeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>
```

### PR Description
## 改动概要
  Chat 里的视频从「inline 大尺寸内嵌播放器」改成「**240×240 内紧凑缩略图 + 点击打开       
  lightbox 全屏播放**」，跟图片的预览交互对齐。9:16 portrait 视频不再撑爆 viewport。
                                                                                          
  ## 用户层面的变化                       
  - **缩略图**：视频显示为 ≤240×240 的小卡片（保留视频原始宽高比），中央叠加白色 play 圆形
   icon，hover 加深                                                                       
  - **点击展开**：复用已有 `ImagePreview` 全屏蒙层组件 → autoPlay + controls +            
  ESC/点击外侧关闭，跟 agent 生成图片的预览体验完全一致                       
  - **不再溢出**：portrait 9:16 视频之前能渲染到 60vh 高，desktop 上只能看到              
  1/3；现在缩略图模式下根本不占聊天屏幕空间                                 
                                                                                          
  ## 涉及的渲染路径（全部统一改造）       
  | 路径 | 改动 |                                                                         
  |------|------|                         
  | `MMAttachments.tsx VideoAttachment`（用户上传视频 / agent MM file 附件） | 卡片       
  wrapper 去掉，改 240×240 button + play overlay + 点击打开 lightbox |             
  | `MMAttachments.tsx ReplayAttachment`（chat 回放模式 video） | 同上 |                  
  | `render-markdown-to-html.ts renderMarkdownVideo`（agent markdown `[video:](url)`
  语法） | 渲染 thumbnail span + `data-video-url` 属性，play overlay SVG 内联 |           
  | `render-markdown-to-html.ts normalizeMediaHtml`（agent inline `<video>` HTML 块） |   
  size cap 缩到 240×240 |                                                                 
  | `MarkdownContent.tsx` | click handler 加分支：`.markdown-video-thumb[data-video-url]` 
  路由到 `window.openImagePreview` |                                                     
  | `ImagePreview.tsx` | 修复 `activeItem` 推导，让 single-item gallery 也能传 `type:     
  'video'`（之前硬编码：`length > 1` 才认为是 gallery，单 item 退到顶层 type prop =  
  `'image'`，导致单视频被当图片渲染） |                                                   
                                          
  ## 关键实现细节                                                                         
  - **`width: fit-content` / `w-fit`** 是缩略图 wrapper 的关键约束 —— 防止 `<video>` 在
  metadata 加载前被 300×150 默认 intrinsic 尺寸定型 wrapper、加载完成后视频重新尺寸但   
  wrapper 不收缩、留出黑色 gap 的 bug                                                     
  - **`pointer-events: none`** 在 play overlay 上：让点击穿透到
  button/wrapper，不被装饰层拦截                                                          
  - **`<video>` 不带 `controls`**：原生 controls 会自带 play 按钮等 UI 拦截               
  click，不能干扰整 wrapper 的 click-to-open                                            
                                                                                          
  ## Out of scope（独立 PR）              
  - 多视频 gallery 翻页（现在 single-item 能跑通，多 item 走 prev/next 按钮，但 markdown  
  里多视频时不会自动 batch 成 gallery —— 跟现有图片 gallery 行为对齐还要补一段          
  prose-container 扫描逻辑）                                                              
  - video poster 图（用 `<video preload="metadata">` 自动取首帧；如果想加显式 poster
  走另一套）                                                                              
                                                                                          
  ## Test plan                                                                          
  - [x] `pnpm lint` 干净                                                                  
  - [x] `tsc --noEmit` 干净（exit 0）     
  - [x] 4 个相关测试文件 130/130 通过（`render-markdown-to-html` / `MarkdownContent` /    
  `ImagePreview` / `MMAttachments`）                                                      
  - [x] 全量 `pnpm test:unit` 通过                                                        
  - [x] 本地 dev server hard refresh 后视频显示为缩略图，点击打开 lightbox autoPlay       
  - [ ] 多浏览器抽检（Safari 对 `width: fit-content` + replaced element 的 reflow         
  行为偶尔有差异）                                                                        
  - [ ] 测试 portrait 9:16（Vibe Drama 输出）/ landscape 16:9 / 用户上传 horizontal 录屏  
  三种纵横比都没有黑边                             

<img width="2556" height="1714" alt="screenshot-20260506-170533" src="https://github.com/user-attachments/assets/1c9828f0-9dc2-4fab-97b7-937bc2bc52aa" />
<img width="2540" height="1720" alt="screenshot-20260506-170613" src="https://github.com/user-attachments/assets/65fe0c97-b027-4e0b-ad86-b3c
<img width="1278" height="847" alt="Screenshot 2026-05-06 at 17 05 51" src="https://github.com/user-attachments/assets/c6eda2bd-c080-45cb-84e7-8dc3d1c3d0ba" />
d33affcb2" />

<img width="2558" height="1712" alt="screenshot-20260506-170622" src="https://github.com/user-attachments/assets/eeb8d6f8-8e4b-488f-ade2-c55e1427bdee" />

before👇
<img width="2552" height="1710" alt="screenshot-20260506-175942" src="https://github.com/user-attachments/assets/7ec9cea8-cedf-443f-b7da-b1c479365f2b" />



---

## 56b0164e — 2026-05-06
**Author:** peter-srp
**SHA:** 56b0164e1e88927d771a1a96f250cb41c58ee057
**Stats:** +1683 -94 (1777 changes)

### Commit Message
```
feat(web): remove locale prefix from app page URLs (#1561)

## Summary

- App pages (`/chat`, `/admin`, `/assets`, etc.) no longer have locale
prefix in URL — `/en/chat` → 301 → `/chat`
- Middleware rewrites `/chat` to internal `/{locale}/chat` using cookie
> Accept-Language > default(en)
- SEO pages (`/`, `/about`, `/pricing`) keep `/{locale}/...` prefix
unchanged
- Cookie only written by manual language switch (`setLocale()`) or
first-visit App page detection — SEO page visits no longer overwrite
cookie
- `LocaleLink` omits locale prefix for App page hrefs
- `setLocale()` uses `router.refresh()` for App pages (URL stays
unchanged)

## Motivation

Shared links like `/zh/chat` previously locked recipients into the
sender's language. The recent `feat/web-i18n-new-user-browser-override`
PR mitigated this with browser-language override, but the root cause
remained: locale info in URLs for pages that don't need SEO indexing.

## Test plan

- [x] 4433 unit tests pass (56 middleware tests including 11 new)
- [x] `tsc --noEmit` — no type errors
- [x] ESLint — no lint errors
- [x] E2E tests updated for new URL patterns
- [ ] Manual: visit `/en/chat` → verify 301 to `/chat`
- [ ] Manual: visit `/chat` → verify page loads in browser language
- [ ] Manual: switch language on `/chat` → URL stays `/chat`, content
changes
- [ ] Manual: visit `/zh/pricing` with existing en cookie → verify
cookie is NOT overwritten

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR Description
## Summary

- App pages (`/chat`, `/admin`, `/assets`, etc.) no longer have locale prefix in URL — `/en/chat` → 301 → `/chat`
- Middleware rewrites `/chat` to internal `/{locale}/chat` using cookie > Accept-Language > default(en)
- SEO pages (`/`, `/about`, `/pricing`) keep `/{locale}/...` prefix unchanged
- Cookie only written by manual language switch (`setLocale()`) or first-visit App page detection — SEO page visits no longer overwrite cookie
- `LocaleLink` omits locale prefix for App page hrefs
- `setLocale()` uses `router.refresh()` for App pages (URL stays unchanged)

## Motivation

Shared links like `/zh/chat` previously locked recipients into the sender's language. The recent `feat/web-i18n-new-user-browser-override` PR mitigated this with browser-language override, but the root cause remained: locale info in URLs for pages that don't need SEO indexing.

## Test plan

- [x] 4433 unit tests pass (56 middleware tests including 11 new)
- [x] `tsc --noEmit` — no type errors
- [x] ESLint — no lint errors
- [x] E2E tests updated for new URL patterns
- [ ] Manual: visit `/en/chat` → verify 301 to `/chat`
- [ ] Manual: visit `/chat` → verify page loads in browser language
- [ ] Manual: switch language on `/chat` → URL stays `/chat`, content changes
- [ ] Manual: visit `/zh/pricing` with existing en cookie → verify cookie is NOT overwritten

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 52c61a37 — 2026-05-06
**Author:** kaka-srp
**SHA:** 52c61a37960365c00fab4f9f3f9581df8ac788fc
**Stats:** +3117 -327 (3444 changes)

### Commit Message
```
fix(claw-interface): ECA-616 bot leak — inline retry + PagerDuty alert (#1564)

## Summary

Closes a structural gap where `stop_user_bots` failures during
subscription expiry were swallowed without persisted state. After
re-investigation found the actual ongoing leak rate is ~1 user/month
(not the 921 my early framing claimed — see [Linear correction
comment](https://linear.app/srpone/issue/ECA-616/expired-subscription-cleanup-leaks-running-bots-when-stop-user-bots#comment-08d52f20)),
this PR opts for **inline retry + PagerDuty alert** over a periodic
reconciliation cron.

### Three independent bugs fixed

1. **`stop_user_bots` retry + PD alert.** Per-bot loop now does
3-attempt exponential backoff (0.5/1.5/4.5s); on retry exhaustion
persist `bot_stop_pending=true` marker AND page on-call (PagerDuty
severity=warning, dedup_key per uid). Most transient FastClaw blips ride
out within retries.
2. **`billing_cycle="annual"` Apple drift.**
`check_yearly_credits_reset` now accepts both `"yearly"` and `"annual"`
via `YEARLY_BILLING_CYCLES` constant — Apple yearly users no longer fall
through both crons.
3. **Apple App Store API silent fail-open.** `_check_apple_subscription`
persists `apple_verify_failures` counter; force-expires after 3
consecutive None responses (~3 days, well within Apple's 16-day grace).

### Bonus latent fix

`_handle_expired_subscription` previously gated `terminate_subscription`
behind `has_stripe_sub`, so Apple users transitioning to expired never
had their Billing Gateway subscription terminated. Switched to
`has_external_sub = stripe_subscription_id OR
apple_original_transaction_id`.

### Observability + cleanup

- Per-step `CronResult` counters (`terminate_failed`,
`clear_wallet_failed`, `transition_failed`, `sync_models_failed`,
`sync_resources_failed`, `stop_bots_failed`) — `ecap-cron-runs` now
shows which expiry step is unreliable, addressing ECA-616 action item
#4.
- `services/claw-interface/scripts/cleanup_historical_bot_leak.py` —
one-shot for ~33 pre-ECA-433 historical leaks (mongo says stopped,
FastClaw says ready). Deletable after first prod run.

### File splits (500-line cap)

- `app/services/openclaw/bot_stop.py` extracted from `bot_lifecycle.py`
- `app/cron/_apple_expiry.py` extracted from `subscription_cron.py`

Spec:
`docs/superpowers/specs/2026-05-06-eca-616-bot-leak-reconciliation.md`
Plan:
`docs/superpowers/plans/2026-05-06-eca-616-bot-leak-reconciliation.md`

Closes ECA-616.

## Test plan

- [x] Unit tests pass for affected files: 58 passing
- [x] ruff + pyright + import-linter: clean
- [x] Pre-commit hook (file-length / complexity / collection-strings /
etc): pass
- [ ] Staging: trigger a Stripe expiry webhook for a test account,
confirm `stop_user_bots` runs without alert
- [ ] Prod (post-deploy):
- [ ] Verify `_apple_expiry` Apple verify failure marker writes by
tailing logs
- [ ] If 1 ongoing leak persists, manually call `stop_user_bots(uid)`
for it
- [ ] Run `kubectl exec ... python
scripts/cleanup_historical_bot_leak.py` for the ~33 historical cohort
- [ ] Re-run FastClaw audit on a sample of pre-2026-04-09 users — expect
0 INCONSISTENT
- [ ] Delete `scripts/cleanup_historical_bot_leak.py` in follow-up
```

### PR Description
## Summary

Closes a structural gap where `stop_user_bots` failures during subscription expiry were swallowed without persisted state. After re-investigation found the actual ongoing leak rate is ~1 user/month (not the 921 my early framing claimed — see [Linear correction comment](https://linear.app/srpone/issue/ECA-616/expired-subscription-cleanup-leaks-running-bots-when-stop-user-bots#comment-08d52f20)), this PR opts for **inline retry + PagerDuty alert** over a periodic reconciliation cron.

### Three independent bugs fixed

1. **`stop_user_bots` retry + PD alert.** Per-bot loop now does 3-attempt exponential backoff (0.5/1.5/4.5s); on retry exhaustion persist `bot_stop_pending=true` marker AND page on-call (PagerDuty severity=warning, dedup_key per uid). Most transient FastClaw blips ride out within retries.
2. **`billing_cycle="annual"` Apple drift.** `check_yearly_credits_reset` now accepts both `"yearly"` and `"annual"` via `YEARLY_BILLING_CYCLES` constant — Apple yearly users no longer fall through both crons.
3. **Apple App Store API silent fail-open.** `_check_apple_subscription` persists `apple_verify_failures` counter; force-expires after 3 consecutive None responses (~3 days, well within Apple's 16-day grace).

### Bonus latent fix

`_handle_expired_subscription` previously gated `terminate_subscription` behind `has_stripe_sub`, so Apple users transitioning to expired never had their Billing Gateway subscription terminated. Switched to `has_external_sub = stripe_subscription_id OR apple_original_transaction_id`.

### Observability + cleanup

- Per-step `CronResult` counters (`terminate_failed`, `clear_wallet_failed`, `transition_failed`, `sync_models_failed`, `sync_resources_failed`, `stop_bots_failed`) — `ecap-cron-runs` now shows which expiry step is unreliable, addressing ECA-616 action item #4.
- `services/claw-interface/scripts/cleanup_historical_bot_leak.py` — one-shot for ~33 pre-ECA-433 historical leaks (mongo says stopped, FastClaw says ready). Deletable after first prod run.

### File splits (500-line cap)

- `app/services/openclaw/bot_stop.py` extracted from `bot_lifecycle.py`
- `app/cron/_apple_expiry.py` extracted from `subscription_cron.py`

Spec: `docs/superpowers/specs/2026-05-06-eca-616-bot-leak-reconciliation.md`
Plan: `docs/superpowers/plans/2026-05-06-eca-616-bot-leak-reconciliation.md`

Closes ECA-616.

## Test plan

- [x] Unit tests pass for affected files: 58 passing
- [x] ruff + pyright + import-linter: clean
- [x] Pre-commit hook (file-length / complexity / collection-strings / etc): pass
- [ ] Staging: trigger a Stripe expiry webhook for a test account, confirm `stop_user_bots` runs without alert
- [ ] Prod (post-deploy):
  - [ ] Verify `_apple_expiry` Apple verify failure marker writes by tailing logs
  - [ ] If 1 ongoing leak persists, manually call `stop_user_bots(uid)` for it
  - [ ] Run `kubectl exec ... python scripts/cleanup_historical_bot_leak.py` for the ~33 historical cohort
  - [ ] Re-run FastClaw audit on a sample of pre-2026-04-09 users — expect 0 INCONSISTENT
  - [ ] Delete `scripts/cleanup_historical_bot_leak.py` in follow-up commit

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## ff3e8183 — 2026-05-06
**Author:** shana-srp
**SHA:** ff3e8183772ea6c41d47debaa8bad378a7a4642d
**Stats:** +41 -61 (102 changes)

### Commit Message
```
fix(web): landing hero demo video — no autoplay + native controls + HD poster (#1511)

## Summary
- Remove `autoPlay` from both hero videos (background ambient + product
demo) — the demo video now waits for user interaction instead of
starting on page load.
- Replace the custom mute-toggle button with native HTML5 `controls`,
giving visitors a full player: play/pause, progress scrubber, time,
volume, fullscreen. Drops `useState`/icon imports and the orphan
`.hero-product-video-mute-btn` CSS.
- Add a 1920×1080 PNG poster
(`web/public/images/zooclaw-demo-poster.png`) extracted from the 1080p
source — the cover renders sharp instantly, before any video bytes load.
Paired with `preload="metadata"` so the video itself stays deferred.
- Move hero demo video URL + poster URL into `landingContent.ts` (per
landing's "static assets live in landingContent" convention).

## Test plan
- [ ] Visit `/zh` — demo video shows the HD intro frame, paused, with
native player chrome (▶, `0:00 / 3:17`, scrubber, volume, fullscreen).
- [ ] Click play → video plays; pause/scrub/fullscreen all work via
native controls.
- [ ] Background ambient video no longer autoplays.
- [ ] Mobile (≤768px): native controls render correctly inside the
rounded video frame; no leftover empty space from the removed mute
button.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
Co-authored-by: peter-srp <peter@srp.one>
```

### PR Description
## Summary
- Remove `autoPlay` from both hero videos (background ambient + product demo) — the demo video now waits for user interaction instead of starting on page load.
- Replace the custom mute-toggle button with native HTML5 `controls`, giving visitors a full player: play/pause, progress scrubber, time, volume, fullscreen. Drops `useState`/icon imports and the orphan `.hero-product-video-mute-btn` CSS.
- Add a 1920×1080 PNG poster (`web/public/images/zooclaw-demo-poster.png`) extracted from the 1080p source — the cover renders sharp instantly, before any video bytes load. Paired with `preload="metadata"` so the video itself stays deferred.
- Move hero demo video URL + poster URL into `landingContent.ts` (per landing's "static assets live in landingContent" convention).

## Test plan
- [ ] Visit `/zh` — demo video shows the HD intro frame, paused, with native player chrome (▶, `0:00 / 3:17`, scrubber, volume, fullscreen).
- [ ] Click play → video plays; pause/scrub/fullscreen all work via native controls.
- [ ] Background ambient video no longer autoplays.
- [ ] Mobile (≤768px): native controls render correctly inside the rounded video frame; no leftover empty space from the removed mute button.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## be662c63 — 2026-05-06
**Author:** peter-srp
**SHA:** be662c63744765d89c685df45fa31665b8a35d7f
**Stats:** +135 -2 (137 changes)

### Commit Message
```
fix(web): auto-recover chunk errors, filter infra HTTP errors from Sentry (#1562)

## Summary
- **Chunk load errors** (stale JS after deploys): error boundaries now
detect `ChunkLoadError` / `undefined.call()` and auto-reload the page
once (sessionStorage guard prevents infinite loops). If reload doesn't
fix it, fallback UI is shown and the error is reported to Sentry with a
unified `chunk-load-error` fingerprint.
- **Infrastructure HTTP errors** (502/503/504/524): dropped in
`beforeSend` — these are Cloudflare/gateway timeouts with no frontend
diagnostic value.

## Test plan
- [ ] Deploy a new version, open a stale tab → verify auto-reload
recovers the page
- [ ] After reload, if error persists → verify error UI is shown (not
infinite reload)
- [ ] Trigger a 524 timeout → verify it does NOT appear in Sentry
- [ ] Verify normal errors still report to Sentry as usual

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR Description
## Summary
- **Chunk load errors** (stale JS after deploys): error boundaries now detect `ChunkLoadError` / `undefined.call()` and auto-reload the page once (sessionStorage guard prevents infinite loops). If reload doesn't fix it, fallback UI is shown and the error is reported to Sentry with a unified `chunk-load-error` fingerprint.
- **Infrastructure HTTP errors** (502/503/504/524): dropped in `beforeSend` — these are Cloudflare/gateway timeouts with no frontend diagnostic value.

## Test plan
- [ ] Deploy a new version, open a stale tab → verify auto-reload recovers the page
- [ ] After reload, if error persists → verify error UI is shown (not infinite reload)
- [ ] Trigger a 524 timeout → verify it does NOT appear in Sentry
- [ ] Verify normal errors still report to Sentry as usual

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## c5bb5425 — 2026-05-06
**Author:** bill-srp
**SHA:** c5bb54254bd5f48d66d31b96fff9550e5e28a518
**Stats:** +102 -36 (138 changes)

### Commit Message
```
fix(ios): Chat keyboard — stop scroll-dismiss, scroll past keyboard (#1557)

## Summary

Two related fixes to how the chat list interacts with the keyboard and
the floating `ChatInputView` overlay.

### 1. Stop chat scroll from dismissing the keyboard

`ChatMessageList` had **two** independent paths that closed the keyboard
whenever the user dragged the chat:

- `collectionView.keyboardDismissMode = .interactive` (UIKit's built-in
iMessage-style follow-finger dismiss).
- `Coordinator.scrollViewWillBeginDragging` was also calling
`UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder),
…)` on every drag-start.

Removed both. The chat now only dismisses the keyboard via the existing
**tap-to-dismiss** gesture (`Coordinator.handleTap`) and the explicit
`resignFirstResponder` after a successful send
(`ChatInputView.sendMessage`). The `onScrollDismiss?()` callback still
fires from `scrollViewWillBeginDragging` so transient overlays (e.g. the
copy tooltip) keep hiding on drag-start.

### 2. Let chat scroll to the bottom while keyboard is up

`ChatMessageList` applied `.ignoresSafeArea(.keyboard)` and a fixed
`contentInset.bottom = 140`. When the keyboard appeared:

- The input panel overlay (a sibling on the parent ZStack) slid up.
- The chat list's frame stayed full-size and its insets stayed fixed.
- `maxContentOffset = contentSize − bounds.height + 140` didn't change,
so the latest messages were trapped behind the keyboard with no way to
scroll to them.

`Coordinator.startObservingKeyboard(for:)` now subscribes to
`keyboardWillChangeFrameNotification`. On every change it:

1. Computes the keyboard's vertical overlap against the collection
view's bounds (`convert(_:from:)` + `bounds.maxY` math) — handles show,
hide, predictive-bar resize, and rotation in one path.
2. Animates `contentInset.bottom = baseBottomInset (140) + overlap`,
using the keyboard's own `UIKeyboardAnimationDurationUserInfoKey` and
`UIKeyboardAnimationCurveUserInfoKey` so motion is in lock-step with the
rising input panel.
3. Re-pins `contentOffset.y` if `isAtBottom` was true before the change,
so a user who was at the latest message stays glued there (iMessage /
WhatsApp behavior).

Observers are torn down in `Coordinator.deinit`. `baseBottomInset` is
hoisted to a `static let` on `ChatMessageList` so `makeUIView` and the
handler share one source of truth.

The existing comment on `contentInsetAdjustmentBehavior = .never` was
rewritten to explain the new responsibility split (SwiftUI parent owns
frame, the observer owns bottom inset).

## Test plan

**Scroll-to-dismiss removal:**
- [ ] With keyboard up, drag the chat list — keyboard stays visible;
messages scroll normally.
- [ ] Long-press a message to show the copy tooltip → drag the chat —
tooltip dismisses (overlay callback still fires) but keyboard stays.
- [ ] Tap an empty area of the chat — keyboard dismisses (existing tap
gesture).
- [ ] Send a message — keyboard dismisses (existing
`resignFirstResponder` in `ChatInputView`).

**Keyboard-driven inset:**
- [ ] Open a chat with enough messages to fill the screen, keyboard down
— bottom message visible above the input panel.
- [ ] Tap the text input — keyboard rises; bottom message stays visible
just above the rising input panel (no jump, smooth easing matching the
keyboard).
- [ ] Scroll up partway → tap text input — keyboard rises; chat does
**not** auto-scroll (you weren't at the bottom).
- [ ] Tap-to-dismiss → bottom inset shrinks back to 140 over the
keyboard's animation, no jump.
- [ ] Rotate device with keyboard up — inset recalculates to the new
keyboard height.
- [ ] Open & close keyboard repeatedly — no inset accumulation, no
leaked offset.

**Automated:**
- [x] `xcodebuild build` (iPhone 17 Pro simulator) — green; only
pre-existing warnings remain.
- [ ] CI: `code-quality / lint-and-test`.
```

### PR Description
## Summary

Two related fixes to how the chat list interacts with the keyboard and the floating `ChatInputView` overlay.

### 1. Stop chat scroll from dismissing the keyboard

`ChatMessageList` had **two** independent paths that closed the keyboard whenever the user dragged the chat:

- `collectionView.keyboardDismissMode = .interactive` (UIKit's built-in iMessage-style follow-finger dismiss).
- `Coordinator.scrollViewWillBeginDragging` was also calling `UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), …)` on every drag-start.

Removed both. The chat now only dismisses the keyboard via the existing **tap-to-dismiss** gesture (`Coordinator.handleTap`) and the explicit `resignFirstResponder` after a successful send (`ChatInputView.sendMessage`). The `onScrollDismiss?()` callback still fires from `scrollViewWillBeginDragging` so transient overlays (e.g. the copy tooltip) keep hiding on drag-start.

### 2. Let chat scroll to the bottom while keyboard is up

`ChatMessageList` applied `.ignoresSafeArea(.keyboard)` and a fixed `contentInset.bottom = 140`. When the keyboard appeared:

- The input panel overlay (a sibling on the parent ZStack) slid up.
- The chat list's frame stayed full-size and its insets stayed fixed.
- `maxContentOffset = contentSize − bounds.height + 140` didn't change, so the latest messages were trapped behind the keyboard with no way to scroll to them.

`Coordinator.startObservingKeyboard(for:)` now subscribes to `keyboardWillChangeFrameNotification`. On every change it:

1. Computes the keyboard's vertical overlap against the collection view's bounds (`convert(_:from:)` + `bounds.maxY` math) — handles show, hide, predictive-bar resize, and rotation in one path.
2. Animates `contentInset.bottom = baseBottomInset (140) + overlap`, using the keyboard's own `UIKeyboardAnimationDurationUserInfoKey` and `UIKeyboardAnimationCurveUserInfoKey` so motion is in lock-step with the rising input panel.
3. Re-pins `contentOffset.y` if `isAtBottom` was true before the change, so a user who was at the latest message stays glued there (iMessage / WhatsApp behavior).

Observers are torn down in `Coordinator.deinit`. `baseBottomInset` is hoisted to a `static let` on `ChatMessageList` so `makeUIView` and the handler share one source of truth.

The existing comment on `contentInsetAdjustmentBehavior = .never` was rewritten to explain the new responsibility split (SwiftUI parent owns frame, the observer owns bottom inset).

## Test plan

**Scroll-to-dismiss removal:**
- [ ] With keyboard up, drag the chat list — keyboard stays visible; messages scroll normally.
- [ ] Long-press a message to show the copy tooltip → drag the chat — tooltip dismisses (overlay callback still fires) but keyboard stays.
- [ ] Tap an empty area of the chat — keyboard dismisses (existing tap gesture).
- [ ] Send a message — keyboard dismisses (existing `resignFirstResponder` in `ChatInputView`).

**Keyboard-driven inset:**
- [ ] Open a chat with enough messages to fill the screen, keyboard down — bottom message visible above the input panel.
- [ ] Tap the text input — keyboard rises; bottom message stays visible just above the rising input panel (no jump, smooth easing matching the keyboard).
- [ ] Scroll up partway → tap text input — keyboard rises; chat does **not** auto-scroll (you weren't at the bottom).
- [ ] Tap-to-dismiss → bottom inset shrinks back to 140 over the keyboard's animation, no jump.
- [ ] Rotate device with keyboard up — inset recalculates to the new keyboard height.
- [ ] Open & close keyboard repeatedly — no inset accumulation, no leaked offset.

**Automated:**
- [x] `xcodebuild build` (iPhone 17 Pro simulator) — green; only pre-existing warnings remain.
- [ ] CI: `code-quality / lint-and-test`.

---

## 0ebb51d3 — 2026-05-06
**Author:** Nemo Feng
**SHA:** 0ebb51d3a43597808f4f014ba2366cc698b671a8
**Stats:** +164 -27 (191 changes)

### Commit Message
```
feat(web): respect browser language for new users on prefixed URLs (#1558)

## Summary
- New-user override in `middleware.ts`: a first-time visitor (no
`NEXT_LOCALE` cookie) landing on a URL with a locale prefix is now
redirected to their browser-preferred language, instead of being locked
into whichever locale the shared link happened to carry.
- Returning users (cookie set) and crawlers (no `Accept-Language`
header) are intentionally left alone — preserves explicit user choice
and non-English page indexability.
- Refactors `detectUserLocale` by extracting `detectLocaleFromHeaders`,
which returns `null` when the header is absent so the caller can
distinguish "no signal" from "header present, no match → en".

## Why
Previously, `pathnameLocale` won absolutely whenever the URL had a
`/{loc}/` prefix. A Chinese-browser new user clicking a shared
`/en/chat` link saw English forever (cookie pinned to `en` after first
visit). This change makes browser language win for new users only — once
the cookie is set, behavior is unchanged.

## Behavior matrix (new vs. existing rows marked)

| URL | Cookie | Accept-Language | Result |
|---|---|---|---|
| `/pricing` | none | `zh-CN,…` | redirect → `/zh/pricing` (unchanged) |
| `/en/chat` | none | `zh-CN,…` | **redirect → `/zh/chat` (NEW)** |
| `/zh/chat` | none | `vi-VN,…` (no match) | **redirect → `/en/chat`
(NEW, per spec "if not, default to en")** |
| `/zh/chat` | none | (no header) | `/zh/chat` (unchanged — protects SEO
bots) |
| `/en/pricing` | `zh` | anything | `/en/pricing` (unchanged — cookie
user, URL wins) |
| `/zh/chat` | none | `zh-CN,…` (matches) | `/zh/chat` (unchanged — no
redirect needed) |

## Out of scope (flagged for follow-up)
- OAuth callback path (`services/oauth-worker/`): the post-login
redirect URL flows back through this middleware. If OAuth completes
without setting `NEXT_LOCALE` first, the new branch could fire on the
callback. Worth a separate audit of `services/oauth-worker/src/index.ts`
to confirm cookie-setting order; not addressed here.

## Test plan
- [x] Added 6 unit tests in
`web/tests/unit/middleware/middleware.unit.spec.ts` under a new
`new-user override on prefixed URLs` sub-describe:
  - cross-prefix override (`/en/chat` + `zh-CN` → `/zh/chat`)
  - unsupported language → `en` (`/zh/chat` + `vi-VN` → `/en/chat`)
  - missing `Accept-Language` → no redirect (SEO/bot safety)
  - returning user with cookie → URL wins (no redirect)
  - browser matches URL → no redirect
  - regional subtag fallback (`zh-TW` → `zh`)
- [x] All existing locale-routing tests untouched and still pass under
the new logic (verified by trace; same `NextResponse.next` / `redirect`
call paths).
- [ ] Reviewer to verify in dev: open `/en/chat` in a fresh incognito
window with browser language set to Chinese — should land on `/zh/chat`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

### PR Description
## Summary
- New-user override in `middleware.ts`: a first-time visitor (no `NEXT_LOCALE` cookie) landing on a URL with a locale prefix is now redirected to their browser-preferred language, instead of being locked into whichever locale the shared link happened to carry.
- Returning users (cookie set) and crawlers (no `Accept-Language` header) are intentionally left alone — preserves explicit user choice and non-English page indexability.
- Refactors `detectUserLocale` by extracting `detectLocaleFromHeaders`, which returns `null` when the header is absent so the caller can distinguish "no signal" from "header present, no match → en".

## Why
Previously, `pathnameLocale` won absolutely whenever the URL had a `/{loc}/` prefix. A Chinese-browser new user clicking a shared `/en/chat` link saw English forever (cookie pinned to `en` after first visit). This change makes browser language win for new users only — once the cookie is set, behavior is unchanged.

## Behavior matrix (new vs. existing rows marked)

| URL | Cookie | Accept-Language | Result |
|---|---|---|---|
| `/pricing` | none | `zh-CN,…` | redirect → `/zh/pricing` (unchanged) |
| `/en/chat` | none | `zh-CN,…` | **redirect → `/zh/chat` (NEW)** |
| `/zh/chat` | none | `vi-VN,…` (no match) | **redirect → `/en/chat` (NEW, per spec "if not, default to en")** |
| `/zh/chat` | none | (no header) | `/zh/chat` (unchanged — protects SEO bots) |
| `/en/pricing` | `zh` | anything | `/en/pricing` (unchanged — cookie user, URL wins) |
| `/zh/chat` | none | `zh-CN,…` (matches) | `/zh/chat` (unchanged — no redirect needed) |

## Out of scope (flagged for follow-up)
- OAuth callback path (`services/oauth-worker/`): the post-login redirect URL flows back through this middleware. If OAuth completes without setting `NEXT_LOCALE` first, the new branch could fire on the callback. Worth a separate audit of `services/oauth-worker/src/index.ts` to confirm cookie-setting order; not addressed here.

## Test plan
- [x] Added 6 unit tests in `web/tests/unit/middleware/middleware.unit.spec.ts` under a new `new-user override on prefixed URLs` sub-describe:
  - cross-prefix override (`/en/chat` + `zh-CN` → `/zh/chat`)
  - unsupported language → `en` (`/zh/chat` + `vi-VN` → `/en/chat`)
  - missing `Accept-Language` → no redirect (SEO/bot safety)
  - returning user with cookie → URL wins (no redirect)
  - browser matches URL → no redirect
  - regional subtag fallback (`zh-TW` → `zh`)
- [x] All existing locale-routing tests untouched and still pass under the new logic (verified by trace; same `NextResponse.next` / `redirect` call paths).
- [ ] Reviewer to verify in dev: open `/en/chat` in a fresh incognito window with browser language set to Chinese — should land on `/zh/chat`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 30e3cf52 — 2026-05-06
**Author:** peter-srp
**SHA:** 30e3cf5220e3177532745e5914822eda4d7fabaa
**Stats:** +41 -0 (41 changes)

### Commit Message
```
fix(web): reduce Sentry noise from HTTP errors, chat warnings, hydration (#1556)

## Summary

Targeted fixes for the **top 6 unresolved Sentry issues** (by event
volume over the last 7 days):

| Issue | Type | Events/7d | Users | Fix |
|-------|------|-----------|-------|-----|
| ECAP-WEBSITE-CC | HTTP 401 on `/api/openclaw/*` | 5,769 | 12 |
`beforeSend` filter |
| ECAP-WEBSITE-2 | Hydration Error | 2,993 | 135 | Fingerprint
normalization |
| ECAP-WEBSITE-9Z | Chat `message_history` warning | 1,002 | 260 | 5-min
dedup |
| ECAP-WEBSITE-G4 | HTTP 404 on `/api/openclaw/settings/agent/*` | 726 |
84 | `beforeSend` filter |
| ECAP-WEBSITE-9T | Chat `agent_cache` warning | 682 | 84 | 5-min dedup
|
| ECAP-WEBSITE-K6 | HTTP 403 on `/api/users/credits/*` | 592 | 17 |
`beforeSend` filter |

**Total: ~11,764 events/week eliminated or rate-limited.**

### Changes

1. **`sentry.client.config.ts`** — `beforeSend` additions:
- Drop HTTP Client Error events matching expected status + URL patterns
(401/403/404 on specific API endpoints that the UI already handles
gracefully)
- Normalize hydration error fingerprints → all grouped under
`['hydration-error']` so the existing global rate limit (5 per 5min)
applies to the group, not per-unique-message

2. **`chat-monitor.ts`** — Add dedup to `captureChatWarning`:
- Same pattern as `openclaw-monitor.ts` (`recentWarnings` map, 5-min
window per feature type)
- `captureChatError` (level: error) is NOT deduped — those represent
real user-facing failures

### Not changed (already fixed / not actionable in frontend)

- **ECAP-WEBSITE-8N/8S** (OpenClaw
`abnormal_close`/`heartbeat_timeout`): Already breadcrumb-only via
`TRANSIENT_REASONS` — `last_seen` is April 29, no new events
- **Mattermost connection errors**: Already resolved, `beforeSend`
safety net already exists

## Test plan

- [x] `tsc --noEmit` passes
- [x] All 51 existing sentry unit tests pass
- [x] ESLint passes (pre-commit hook)
- [ ] Deploy to staging and monitor Sentry event volume for 24h

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR Description
## Summary

Targeted fixes for the **top 6 unresolved Sentry issues** (by event volume over the last 7 days):

| Issue | Type | Events/7d | Users | Fix |
|-------|------|-----------|-------|-----|
| ECAP-WEBSITE-CC | HTTP 401 on `/api/openclaw/*` | 5,769 | 12 | `beforeSend` filter |
| ECAP-WEBSITE-2 | Hydration Error | 2,993 | 135 | Fingerprint normalization |
| ECAP-WEBSITE-9Z | Chat `message_history` warning | 1,002 | 260 | 5-min dedup |
| ECAP-WEBSITE-G4 | HTTP 404 on `/api/openclaw/settings/agent/*` | 726 | 84 | `beforeSend` filter |
| ECAP-WEBSITE-9T | Chat `agent_cache` warning | 682 | 84 | 5-min dedup |
| ECAP-WEBSITE-K6 | HTTP 403 on `/api/users/credits/*` | 592 | 17 | `beforeSend` filter |

**Total: ~11,764 events/week eliminated or rate-limited.**

### Changes

1. **`sentry.client.config.ts`** — `beforeSend` additions:
   - Drop HTTP Client Error events matching expected status + URL patterns (401/403/404 on specific API endpoints that the UI already handles gracefully)
   - Normalize hydration error fingerprints → all grouped under `['hydration-error']` so the existing global rate limit (5 per 5min) applies to the group, not per-unique-message

2. **`chat-monitor.ts`** — Add dedup to `captureChatWarning`:
   - Same pattern as `openclaw-monitor.ts` (`recentWarnings` map, 5-min window per feature type)
   - `captureChatError` (level: error) is NOT deduped — those represent real user-facing failures

### Not changed (already fixed / not actionable in frontend)

- **ECAP-WEBSITE-8N/8S** (OpenClaw `abnormal_close`/`heartbeat_timeout`): Already breadcrumb-only via `TRANSIENT_REASONS` — `last_seen` is April 29, no new events
- **Mattermost connection errors**: Already resolved, `beforeSend` safety net already exists

## Test plan

- [x] `tsc --noEmit` passes
- [x] All 51 existing sentry unit tests pass
- [x] ESLint passes (pre-commit hook)
- [ ] Deploy to staging and monitor Sentry event volume for 24h

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 5d890cf1 — 2026-05-06
**Author:** Chris@ZooClaw
**SHA:** 5d890cf126232543f1eced03b059f02b996d8315
**Stats:** +48 -52 (100 changes)

### Commit Message
```
chore(web): rename lib/api/ 4 个 camelCase 文件 → kebab-case (#1554)

## Summary
按 PR #1547 引入的 filename-naming 规则把 `src/lib/api/` 下 4 个 camelCase 文件改成
kebab-case：

| 旧名 | 新名 |
|---|---|
| `_authHeaders.ts` | `auth-headers.ts` |
| `chatReplayApi.ts` | `chat-replay-api.ts` |
| `conversationAssets.ts` | `conversation-assets.ts` |
| `userBusinessDataCache.ts` | `user-business-data-cache.ts` |

## 改动
- 同步 rename 1 个 dedicated test 文件（`userBusinessDataCache.unit.spec.ts` →
`user-business-data-cache.unit.spec.ts`）
- sed 批量更新 35 处 import 路径（7 + 3 + 14 + 11，含 dynamic imports 与
\`vi.mock\` 字符串），grep audit 全干净
- SHRINK-ONLY baseline: **53 → 49** entries（减 4）

## 设计说明
\`_authHeaders.ts\` 的 \`_\` 前缀原本表示"私有"约定。改 kebab 后这个标记字面消失，但所有 7 处
caller 都在 \`lib/api/\` 内部，分层（directory）本身已经体现"私有"语义；不影响实际使用边界。

## Test plan
- [x] \`pnpm lint\` exit 0
- [x] \`pnpm exec tsc --noEmit\` exit 0
- [x] \`pnpm lint:imports\` exit 0（dep-cruiser，0 errors）
- [x] \`bash web/scripts/check-filename-shrink-only.sh\` — main: 53,
HEAD: 49 ✅
- [x] 6 个 isolated test files（76
tests）全过：\`user-business-data-cache.unit.spec.ts\` /
\`manager.unit.spec.ts\` / \`MattermostContext.unit.spec.tsx\` / 3 个
\`tests/unit/app/chat/\` 文件
- [ ] CI \`code-quality / lint-and-test\` 通过

## 与 PR #1551 关系
PR #1551 (5 components/.ts rename) 也在 merge queue。两个 PR 改动 baseline
块的不同行（components vs lib/api），不应有 textual conflict；后 merge 的会自动 rebase。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description
## Summary
按 PR #1547 引入的 filename-naming 规则把 `src/lib/api/` 下 4 个 camelCase 文件改成 kebab-case：

| 旧名 | 新名 |
|---|---|
| `_authHeaders.ts` | `auth-headers.ts` |
| `chatReplayApi.ts` | `chat-replay-api.ts` |
| `conversationAssets.ts` | `conversation-assets.ts` |
| `userBusinessDataCache.ts` | `user-business-data-cache.ts` |

## 改动
- 同步 rename 1 个 dedicated test 文件（`userBusinessDataCache.unit.spec.ts` → `user-business-data-cache.unit.spec.ts`）
- sed 批量更新 35 处 import 路径（7 + 3 + 14 + 11，含 dynamic imports 与 \`vi.mock\` 字符串），grep audit 全干净
- SHRINK-ONLY baseline: **53 → 49** entries（减 4）

## 设计说明
\`_authHeaders.ts\` 的 \`_\` 前缀原本表示"私有"约定。改 kebab 后这个标记字面消失，但所有 7 处 caller 都在 \`lib/api/\` 内部，分层（directory）本身已经体现"私有"语义；不影响实际使用边界。

## Test plan
- [x] \`pnpm lint\` exit 0
- [x] \`pnpm exec tsc --noEmit\` exit 0
- [x] \`pnpm lint:imports\` exit 0（dep-cruiser，0 errors）
- [x] \`bash web/scripts/check-filename-shrink-only.sh\` — main: 53, HEAD: 49 ✅
- [x] 6 个 isolated test files（76 tests）全过：\`user-business-data-cache.unit.spec.ts\` / \`manager.unit.spec.ts\` / \`MattermostContext.unit.spec.tsx\` / 3 个 \`tests/unit/app/chat/\` 文件
- [ ] CI \`code-quality / lint-and-test\` 通过

## 与 PR #1551 关系
PR #1551 (5 components/.ts rename) 也在 merge queue。两个 PR 改动 baseline 块的不同行（components vs lib/api），不应有 textual conflict；后 merge 的会自动 rebase。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## f534599e — 2026-05-06
**Author:** Fangmiao-srp
**SHA:** f534599e6ce0079c57c50cf8e573d766e7d265af
**Stats:** +143 -10 (153 changes)

### Commit Message
```
feat(web): isolate tracking by environment (#1509)

## Summary

- GA4: staging 使用独立的 Measurement ID (`G-R5KDFHVTGK`)，数据进
`srp-ecap-staging` property，不再污染 production
- Google Ads: 非 production 环境跳过 conversion 事件（staging 无需广告回传）
- Reddit Pixel: 仅 production 加载脚本（staging 无需广告追踪）
- 测试: conversion 相关测试补充环境变量 stub，新增 staging 跳过测试

## Test plan

- [x] 32 个 tracking 单元测试全部通过
- [ ] staging 部署后确认 GA4 DebugView 中 Measurement ID 为 `G-R5KDFHVTGK`
- [ ] production 部署后确认 GA4 事件正常、Google Ads conversion 正常、Reddit Pixel 正常

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```

### PR Description
## Summary

- GA4: staging 使用独立的 Measurement ID (`G-R5KDFHVTGK`)，数据进 `srp-ecap-staging` property，不再污染 production
- Google Ads: 非 production 环境跳过 conversion 事件（staging 无需广告回传）
- Reddit Pixel: 仅 production 加载脚本（staging 无需广告追踪）
- 测试: conversion 相关测试补充环境变量 stub，新增 staging 跳过测试

## Test plan

- [x] 32 个 tracking 单元测试全部通过
- [ ] staging 部署后确认 GA4 DebugView 中 Measurement ID 为 `G-R5KDFHVTGK`
- [ ] production 部署后确认 GA4 事件正常、Google Ads conversion 正常、Reddit Pixel 正常

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## a02700fe — 2026-05-06
**Author:** bill-srp
**SHA:** a02700fe16159623fed084b9a9735ba38428fea6
**Stats:** +2768 -340 (3108 changes)

### Commit Message
```
feat(ios): 1.6.0 — Photos save, lightbox UX, chat polish (#1516)

## Summary

iOS 1.6.0 release — collected features and fixes across the chat
experience.

### 1. Save image and video to Photos (new feature)

Adds a "save to Photos" download button to the image lightbox
(`ImageFullscreenView`) and the inline video player (`VideoPlayerView`).

- **New actor `MediaSaveService`** with two injected `Sendable`
protocols for testability: `PhotoLibraryAuthorizing` (status + request)
and `PhotoLibraryWriting` (`PHPhotoLibrary.performChanges` wrapper).
Typed throws on the public surface (`throws(MediaSaveError)`).
- **Build setting:** `INFOPLIST_KEY_NSPhotoLibraryAddUsageDescription`
(Debug + Release), paired with `PHPhotoLibrary.requestAuthorization(for:
.addOnly)` — less-invasive add-only system prompt.
- **Tests:** 10 new Swift Testing tests cover every
`PHAuthorizationStatus` branch plus writer-error → `.saveFailed` mapping
for both `saveImage` and `saveVideo`. No real `PHPhotoLibrary` I/O.

Spec: `docs/superpowers/specs/2026-05-04-ios-media-download-design.md`
Plan: `docs/superpowers/plans/2026-05-04-ios-media-download.md`

### 2. Image lightbox UX overhaul

- **Pinch-to-zoom + pan + edge clamping** via a `UIScrollView`-backed
`UIViewRepresentable`. The previous SwiftUI-only `MagnificationGesture`
zoomed but had no pan, leaving the off-center portions of a zoomed image
unreachable. Bounded at 1×–4×; single-tap toggles 1×↔2×.
- **Drag-down-to-dismiss** with finger-tracking, backdrop + chrome
opacity fade, and spring-back. Gated on `zoomScale == 1` (via a binding
from `UIScrollViewDelegate.scrollViewDidZoom`) so zoomed pans don't
fight the dismiss gesture. Releases past 120pt or fast flicks
(predicted-end > 400pt) commit dismissal.
- **"Saved to Photos" toast** on successful download, mirroring the
existing `ChatView.savedToast` capsule for cross-screen consistency.

### 3. Inline video player polish

- **Centered play-icon hint.** It was being pinned to the top-right
corner by the ZStack's `.topTrailing` alignment (intended for the
download button). A self-filling frame on just the icon re-centers it
without disturbing the download button's anchor.
- **Centered loading + retry views.** Same `.topTrailing` trap also
pinned the `ProgressView` (during cache fetch) and the load-failed retry
`VStack` to the corner — the original play-icon fix only patched one of
three siblings. Same `.frame(maxWidth: .infinity, maxHeight: .infinity)`
workaround applied to both, so a slow Mattermost video now shows a
centered spinner, and a failed load shows a centered retry button.
- **Always-visible download button.** Previously gated on `localFileURL
!= nil`, which only got set for token-bearing Mattermost attachments.
Token-less markdown-embedded videos played via direct AVPlayer streaming
and had no button. The button now appears for every ready player;
`save()` lazily fetches via `VideoCacheService` on tap if bytes aren't
cached yet — Mattermost saves stay fast (cache hit), streamed saves take
a beat to download then save.
- **"Saved to Photos" toast** on success, matching the lightbox.

### 4. Compose-state survival across switches

`selectedAttachments` was `@State` on `ChatView`, scoped to a single
ChatView instance. A leave/return to the chat tab (chat → agents → chat)
gave `ChatView` a fresh identity through the `currentTabContent` switch
and reset the queue to `[]`. Moved to `MattermostViewModel` next to
`inputText` — both now belong to the user's session, so queued
attachments survive both channel switches and tab switches. The
`uploadedFileId` from the originating channel travels with the
attachment, and the eventual `sendMessage` posts those file_ids to the
now-active channel (Mattermost validates ownership, not channel match).
`resetForSignOut()` clears the queue so sign-out doesn't leak compose
state. 3 new tests cover the contract.

### 5. Agent switch reflow (polish)

Switching agents briefly displayed the previous channel's messages on a
freshly-built `UICollectionView`, then animated cells top-down as
`ChatLayout`'s `keepContentAtBottomOfVisibleArea` recomputed across
self-sizing passes. Two-part fix:
`MattermostViewModel.clearChannelState()` synchronously resets
`messages` / `activeChannelId` at every entry point so the rebuild
starts empty; new `ChatStableLayout` (a `CollectionViewChatLayout`
subclass) exposes an invalidation counter that the coordinator polls
each runloop tick, and `ChatView`'s opacity gate only fades in once a
`(invalidationCount, contentSize, topCellY)` sample is stable for 5
consecutive ticks (cap 60 ≈ 1s for streaming-cell safety). The
`.id(selectedAgentId)` rebuild moved from `ChatView` (in `AppShellView`)
to `ChatMessageList` only — narrower blast radius, same crash
protection.

### 6. Consent card response (polish)

Tapping Yes/Skip on a hire/fire consent card gave no feedback for the
duration of `sendMessage`'s network round-trip (~200–500ms).
`SpecialistCardView` now tracks a `pendingLabel: String?` synchronously
on tap — the tapped button shows a `ProgressView` in place of its text,
the other dims to 50%, and both disable to prevent double-submission.

### 7. Copy tooltip fixes (chat)

- Switched from a SwiftUI long-press to a UIKit
`UILongPressGestureRecognizer` so chat-list scrolling isn't suppressed
for the duration of the press.
- Tooltip now anchors to the finger position and stays clamped below the
floating header / above the input bar (pure `tooltipLocalY` math is
unit-tested).
- Tapping outside the tooltip dismisses it (without a hit-testable
backdrop, which would block `UIScrollView`'s pan).

### 8. Sidebar polish

- Bottom nav + user pill float over the scroll content as a fixed
overlay.
- Restyled bottom nav as a horizontal card row matching the cool-palette
tokens.

### 9. Other fixes

- Paywall stays open on top tier; non-upgrade plans disabled.
- Agents view aligned to cool-palette tokens; hire/fire/update
operations serialized to prevent races.
- Voice panel flips visible on confirm tap, stays on cancel.
- Chat list snapshot helpers extracted to satisfy strict lint.

## Test plan

**Save to Photos (manual, simulator/device):**
- [ ] First-save image triggers the iOS "Add to Photos" prompt with the
configured usage string; granting → success haptic → toast → image
visible in Photos.app.
- [ ] Subsequent image save: no prompt, toast + haptic, image saved.
- [ ] Permission denial (Settings → ZooClaw → Photos → None): warning
haptic only, no toast, no save.
- [ ] Video save (Mattermost attachment): fast cache hit, toast appears,
file in Photos.app Videos album.
- [ ] Video save (markdown-embedded streamed video): button appears, tap
delays briefly while bytes download, then toast.
- [ ] Tap-to-fullscreen on inline video still works when tapping outside
the centered play icon and download button.
- [ ] Lightbox dismissed mid-save: image still appears in Photos via
background completion (toast + haptic dropped, acceptable).
- [ ] Cache-routing regression: re-opening a previously-viewed lightbox
image is instant (no `ProgressView` flash).

**Lightbox UX:**
- [ ] Pinch-zoom a tall portrait image; drag to pan to all edges; bounce
at edges feels right.
- [ ] Pinch past 4× — zoom clamps at 4×.
- [ ] Drag down on an unzoomed image fades backdrop + chrome, snaps back
if released short.
- [ ] Flick down releases dismiss at any distance (predicted-end >
400pt).
- [ ] When zoomed, vertical drag pans the zoomed image (no dismiss);
release without zooming back leaves no leftover offset.
- [ ] Download + dismiss buttons in the corner still tap normally and
aren't hijacked by drag.

**Inline video player layout:**
- [ ] Open a chat with a Mattermost video while offline / cold cache:
spinner is centered horizontally and vertically inside the player
rectangle, not in the top-right.
- [ ] Force a load failure (airplane mode + cold cache): the warning
icon + Retry button appear centered.
- [ ] On a successfully loaded video, the play-icon hint is centered and
the download button is in the top-right (no regression from the earlier
fix).

**Compose state:**
- [ ] Pick attachment in agent A → switch to agent B via sidebar → chip
still visible.
- [ ] Pick attachment → leave chat tab → return → chip still visible.
- [ ] Send in B with attachment from A → message posts with the
attachment.
- [ ] Sign out → all chips cleared on next sign-in.

**Agent switch / consent card / copy tooltip:**
- [ ] Switch between agents repeatedly — no top-to-bottom flow visible
on either short (4-message) or long channels.
- [ ] Tap a hire-consent card's Yes button — spinner appears
immediately, message bubble follows.
- [ ] Tap a fire-consent card's destructive button — same spinner over a
red background.
- [ ] Re-tap pending button or sibling — both no-op (`.disabled(true)`).
- [ ] Long-press a chat message — copy tooltip appears anchored to
finger, doesn't suppress scroll.
- [ ] Tap outside tooltip — dismissed.
- [ ] Switch back to a previously-visited agent — cached posts render at
correct bottom-anchored position with no visible reflow.

**Automated:**
- [x] `xcodebuild test` (iPhone 17 Pro) — all green (includes 10
`MediaSaveService` tests, 3 `MattermostViewModelAttachments` tests).
- [x] `swiftlint` — 0 violations.
- [ ] CI: `code-quality / lint-and-test`.
```

### PR Description
## Summary

iOS 1.6.0 release — collected features and fixes across the chat experience.

### 1. Save image and video to Photos (new feature)

Adds a "save to Photos" download button to the image lightbox (`ImageFullscreenView`) and the inline video player (`VideoPlayerView`).

- **New actor `MediaSaveService`** with two injected `Sendable` protocols for testability: `PhotoLibraryAuthorizing` (status + request) and `PhotoLibraryWriting` (`PHPhotoLibrary.performChanges` wrapper). Typed throws on the public surface (`throws(MediaSaveError)`).
- **Build setting:** `INFOPLIST_KEY_NSPhotoLibraryAddUsageDescription` (Debug + Release), paired with `PHPhotoLibrary.requestAuthorization(for: .addOnly)` — less-invasive add-only system prompt.
- **Tests:** 10 new Swift Testing tests cover every `PHAuthorizationStatus` branch plus writer-error → `.saveFailed` mapping for both `saveImage` and `saveVideo`. No real `PHPhotoLibrary` I/O.

Spec: `docs/superpowers/specs/2026-05-04-ios-media-download-design.md`
Plan: `docs/superpowers/plans/2026-05-04-ios-media-download.md`

### 2. Image lightbox UX overhaul

- **Pinch-to-zoom + pan + edge clamping** via a `UIScrollView`-backed `UIViewRepresentable`. The previous SwiftUI-only `MagnificationGesture` zoomed but had no pan, leaving the off-center portions of a zoomed image unreachable. Bounded at 1×–4×; single-tap toggles 1×↔2×.
- **Drag-down-to-dismiss** with finger-tracking, backdrop + chrome opacity fade, and spring-back. Gated on `zoomScale == 1` (via a binding from `UIScrollViewDelegate.scrollViewDidZoom`) so zoomed pans don't fight the dismiss gesture. Releases past 120pt or fast flicks (predicted-end > 400pt) commit dismissal.
- **"Saved to Photos" toast** on successful download, mirroring the existing `ChatView.savedToast` capsule for cross-screen consistency.

### 3. Inline video player polish

- **Centered play-icon hint.** It was being pinned to the top-right corner by the ZStack's `.topTrailing` alignment (intended for the download button). A self-filling frame on just the icon re-centers it without disturbing the download button's anchor.
- **Centered loading + retry views.** Same `.topTrailing` trap also pinned the `ProgressView` (during cache fetch) and the load-failed retry `VStack` to the corner — the original play-icon fix only patched one of three siblings. Same `.frame(maxWidth: .infinity, maxHeight: .infinity)` workaround applied to both, so a slow Mattermost video now shows a centered spinner, and a failed load shows a centered retry button.
- **Always-visible download button.** Previously gated on `localFileURL != nil`, which only got set for token-bearing Mattermost attachments. Token-less markdown-embedded videos played via direct AVPlayer streaming and had no button. The button now appears for every ready player; `save()` lazily fetches via `VideoCacheService` on tap if bytes aren't cached yet — Mattermost saves stay fast (cache hit), streamed saves take a beat to download then save.
- **"Saved to Photos" toast** on success, matching the lightbox.

### 4. Compose-state survival across switches

`selectedAttachments` was `@State` on `ChatView`, scoped to a single ChatView instance. A leave/return to the chat tab (chat → agents → chat) gave `ChatView` a fresh identity through the `currentTabContent` switch and reset the queue to `[]`. Moved to `MattermostViewModel` next to `inputText` — both now belong to the user's session, so queued attachments survive both channel switches and tab switches. The `uploadedFileId` from the originating channel travels with the attachment, and the eventual `sendMessage` posts those file_ids to the now-active channel (Mattermost validates ownership, not channel match). `resetForSignOut()` clears the queue so sign-out doesn't leak compose state. 3 new tests cover the contract.

### 5. Agent switch reflow (polish)

Switching agents briefly displayed the previous channel's messages on a freshly-built `UICollectionView`, then animated cells top-down as `ChatLayout`'s `keepContentAtBottomOfVisibleArea` recomputed across self-sizing passes. Two-part fix: `MattermostViewModel.clearChannelState()` synchronously resets `messages` / `activeChannelId` at every entry point so the rebuild starts empty; new `ChatStableLayout` (a `CollectionViewChatLayout` subclass) exposes an invalidation counter that the coordinator polls each runloop tick, and `ChatView`'s opacity gate only fades in once a `(invalidationCount, contentSize, topCellY)` sample is stable for 5 consecutive ticks (cap 60 ≈ 1s for streaming-cell safety). The `.id(selectedAgentId)` rebuild moved from `ChatView` (in `AppShellView`) to `ChatMessageList` only — narrower blast radius, same crash protection.

### 6. Consent card response (polish)

Tapping Yes/Skip on a hire/fire consent card gave no feedback for the duration of `sendMessage`'s network round-trip (~200–500ms). `SpecialistCardView` now tracks a `pendingLabel: String?` synchronously on tap — the tapped button shows a `ProgressView` in place of its text, the other dims to 50%, and both disable to prevent double-submission.

### 7. Copy tooltip fixes (chat)

- Switched from a SwiftUI long-press to a UIKit `UILongPressGestureRecognizer` so chat-list scrolling isn't suppressed for the duration of the press.
- Tooltip now anchors to the finger position and stays clamped below the floating header / above the input bar (pure `tooltipLocalY` math is unit-tested).
- Tapping outside the tooltip dismisses it (without a hit-testable backdrop, which would block `UIScrollView`'s pan).

### 8. Sidebar polish

- Bottom nav + user pill float over the scroll content as a fixed overlay.
- Restyled bottom nav as a horizontal card row matching the cool-palette tokens.

### 9. Other fixes

- Paywall stays open on top tier; non-upgrade plans disabled.
- Agents view aligned to cool-palette tokens; hire/fire/update operations serialized to prevent races.
- Voice panel flips visible on confirm tap, stays on cancel.
- Chat list snapshot helpers extracted to satisfy strict lint.

## Test plan

**Save to Photos (manual, simulator/device):**
- [ ] First-save image triggers the iOS "Add to Photos" prompt with the configured usage string; granting → success haptic → toast → image visible in Photos.app.
- [ ] Subsequent image save: no prompt, toast + haptic, image saved.
- [ ] Permission denial (Settings → ZooClaw → Photos → None): warning haptic only, no toast, no save.
- [ ] Video save (Mattermost attachment): fast cache hit, toast appears, file in Photos.app Videos album.
- [ ] Video save (markdown-embedded streamed video): button appears, tap delays briefly while bytes download, then toast.
- [ ] Tap-to-fullscreen on inline video still works when tapping outside the centered play icon and download button.
- [ ] Lightbox dismissed mid-save: image still appears in Photos via background completion (toast + haptic dropped, acceptable).
- [ ] Cache-routing regression: re-opening a previously-viewed lightbox image is instant (no `ProgressView` flash).

**Lightbox UX:**
- [ ] Pinch-zoom a tall portrait image; drag to pan to all edges; bounce at edges feels right.
- [ ] Pinch past 4× — zoom clamps at 4×.
- [ ] Drag down on an unzoomed image fades backdrop + chrome, snaps back if released short.
- [ ] Flick down releases dismiss at any distance (predicted-end > 400pt).
- [ ] When zoomed, vertical drag pans the zoomed image (no dismiss); release without zooming back leaves no leftover offset.
- [ ] Download + dismiss buttons in the corner still tap normally and aren't hijacked by drag.

**Inline video player layout:**
- [ ] Open a chat with a Mattermost video while offline / cold cache: spinner is centered horizontally and vertically inside the player rectangle, not in the top-right.
- [ ] Force a load failure (airplane mode + cold cache): the warning icon + Retry button appear centered.
- [ ] On a successfully loaded video, the play-icon hint is centered and the download button is in the top-right (no regression from the earlier fix).

**Compose state:**
- [ ] Pick attachment in agent A → switch to agent B via sidebar → chip still visible.
- [ ] Pick attachment → leave chat tab → return → chip still visible.
- [ ] Send in B with attachment from A → message posts with the attachment.
- [ ] Sign out → all chips cleared on next sign-in.

**Agent switch / consent card / copy tooltip:**
- [ ] Switch between agents repeatedly — no top-to-bottom flow visible on either short (4-message) or long channels.
- [ ] Tap a hire-consent card's Yes button — spinner appears immediately, message bubble follows.
- [ ] Tap a fire-consent card's destructive button — same spinner over a red background.
- [ ] Re-tap pending button or sibling — both no-op (`.disabled(true)`).
- [ ] Long-press a chat message — copy tooltip appears anchored to finger, doesn't suppress scroll.
- [ ] Tap outside tooltip — dismissed.
- [ ] Switch back to a previously-visited agent — cached posts render at correct bottom-anchored position with no visible reflow.

**Automated:**
- [x] `xcodebuild test` (iPhone 17 Pro) — all green (includes 10 `MediaSaveService` tests, 3 `MattermostViewModelAttachments` tests).
- [x] `swiftlint` — 0 violations.
- [ ] CI: `code-quality / lint-and-test`.


---
