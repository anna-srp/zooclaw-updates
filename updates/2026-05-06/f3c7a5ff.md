---
title: "Chat 中视频改为紧凑缩略图 + 点击全屏播放"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-06"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "f3c7a5ff"
---

# Chat 中视频改为紧凑缩略图 + 点击全屏播放

## 核心宣传点

AI 输出的视频不再撑爆页面，改为小卡片预览，点击即可全屏播放，与图片体验统一。

## 原始内容

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


