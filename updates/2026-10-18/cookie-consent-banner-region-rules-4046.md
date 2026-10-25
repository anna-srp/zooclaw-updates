---
title: "新功能：主站、Blog、Tips 上线 Cookie 同意横条，按地区决定统计和广告默认开关"
type: "新功能"
priority: "高"
date: "2026-10-18"
status: "待审核"
channels: ""
---

# 新功能：主站、Blog、Tips 上线 Cookie 同意横条，按地区决定统计和广告默认开关

## 核心宣传点

此前网站没有 Cookie 同意入口，这次主站、Blog、Tips 统一接入同一套地区规则和选择记录，访客可随时修改统计与广告开关。欧盟及英国、瑞士、挪威等地默认关闭并先行询问，提供「接受全部/全部拒绝/设置」，选择保留 14 天；识别为加州或无法识别地区的访客默认开启，浏览器发出 GPC 隐私信号时自动关闭广告但保留统计；日本、得州、加拿大等其他地区默认开启，可在设置里关。已有的有效选择优先，切换地区不会被改写；全部拒绝后只保留必要的 zoowork_consent_v1 选择记录。

## 分级

- 内部：P1
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## 备注

PR 正文明确要求与另外两个同系列 PR 一起评审、暂不合并，并提到开 PR 时自动检查发现的 iframe 来源漏洞已复现补修；上线前需人工确认三站是否同步发布，以及 GPC 不会自动改写历史 Cookie 这一行为是否符合合规预期。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `bcb9799c15a22cd089df713db5446a53b84e8383`
- PR: #4046
- 作者：Mori-srp
- 日期：2026-10-18T09:23:33Z

### Commit Message

```
feat(cookie-consent): 主站补上 Cookie 选择，按地区控制统计和广告 (#4046)

Webopsy 指出网站没有 Cookie 同意入口。为了补上合规需要的选择，这次把第一到第五版的横条改动一起提交：主站、Blog、Tips
使用同一套地区规则和选择记录，访客随时能改统计和广告开关。地区默认值按第五版，选择记录期限按下方新规则；开 PR 的自动检查又发现 iframe
来源漏洞，已复现并补修，见下方说明。请宝辉一起审三个 PR，先不要合并。

## 按地区怎么开

这张表适用于没有有效已保存选择的访客。

| 地区 | 统计 | 广告 | 访客怎么选 | 选择记多久 |
| --- | --- | --- | --- | --- |
| 欧盟 27 国、英国、瑞士、挪威、冰岛、列支敦士登 | 先问，默认关 | 先问，默认关 | 接受全部、全部拒绝、设置 | 所有选择 14 天
|
| 真正识别为加州（US 且州码 CA） | 默认开 | 默认开；GPC 开着时关 | 知道了、设置、不出售或共享我的个人信息 | 保存广告关
365 天；两项都开 180 天；只关统计而广告开 14 天 |
| 认不出地区（也显示加州横条） | 默认开 | 默认开；GPC 开着时关 | 知道了、设置、不出售或共享我的个人信息 | 两项都开 180
天，含关闭项 14 天 |
| 其他能认出的地区，例如日本、得州、加拿大 | 默认开 | 默认开 | 知道了、设置；可在设置里关 | 两项都开 180 天，含关闭项 14
天 |

GPC
是浏览器发出的隐私信号。加州和认不出地区收到它时只关广告，统计继续；其他地区沿用上述默认值。认不出地区包括缺国家、XX/T1、地区对象缺失，以及美国没有可读的两位州码；加拿大国家码
CA 不算加州。

已经存过的有效选择优先，换地区不会重写选择。全拒绝继续全关；已接受的用户去严格地区也沿用原选择。GPC 可以压住本页已允许的广告，但不自动改写旧
Cookie；要持久关广告，需点“不出售或共享”或在设置里关。点“知道了”会保存统计和广告都开，即使本页广告正被 GPC
压住。首次默认开不会自动保存同意记录。

## 选择记多久，拒绝后还记什么

全部拒绝后，保留必要的 `zoowork_consent_v1` 选择 Cookie 和同名 localStorage
镜像，只记版本、统计开关、广告开关、选择时间和到期时间。Path=/、SameSite=Lax，HTTPS 下加
Secure；主站、Blog、Tips 同域共用，登出也保留。原有登录、安全和必要偏好照常。

期限按保存那一刻的地区和选择定下来：严格地区（欧盟、英国、瑞士、挪威、冰岛、列支敦士登），同意和拒绝都记 **14
天**；只有真正识别为加州（国家 US、州码 CA）的访客，保存选择里的广告是关的（全部拒绝、点“不出售或共享”、设置里关广告），才记
**365 天**，统计开关不影响这 365 天；真加州两项都开记 **180 天**，只关统计而广告开仍记 **14
天**。认不出地区虽然也走加州横条，期限仍和其他非严格地区一样：两项都开 **180 天**，含任何关闭项 **14
天**。欧洲不区分同意和拒绝的期限，是为了避免被认定在诱导同意。

加州法律要求退出至少 12 个月内照办；监管部门也明确，至少等 12 个月才能再询问是否愿意恢复出售或共享，见
[加州隐私保护局说明](https://www.cppa.ca.gov/announcements/2025/20250909.html)。

Cookie 的 Max-Age 和 localStorage
镜像按同一个到期时间失效；已保存的有效选择优先，换地区不会重写选择，也不会延长或缩短原期限。到了各自期限会再问一次。GPC
只压住广告生效状态，不改保存的两个开关或期限。旧格式没有存到期时间的记录按选择时间加 14 天判断，读取不续期、不重写。

Safari 对脚本写的 Cookie 最多留 **7 天**，见 [WebKit
说明](https://webkit.org/blog/8613/intelligent-tracking-prevention-2-1/)；localStorage
是否还在另受 [Safari
的存储清理规则](https://webkit.org/tracking-prevention/#intelligent-tracking-prevention-itp)影响。

统计和广告均拒绝时不加载 Google 统计和广告库；对应许可拒绝期间的行为直接丢弃，不排队等以后补发；清理浏览器可访问的 GA/广告
Cookie、广告存储和 Tips 来源快照。重新允许统计，只补当前页浏览量。只开统计而广告关着时，GA 页面、来源和手动链接投影保留
gclid、gbraid、wbraid，用于注册和付款的渠道归因；包括加州和未知地区的 GPC 广告退出。仍移除
dclid、gad_*、msclkid、fbclid、ttclid、twclid；广告三项许可、广告 Cookie、Google signals
和广告转换继续受广告许可控制。地址栏和业务跳转保持原参数，注册 metadata 没有新增点击编号。拒绝不会删除此前已经发给服务端的数据。

已经加载标签后再撤回，会清理可访问 Cookie 并停止我们自己的发送器；已有浏览器记录只观察了撤回后 5 秒无新增 Google
请求，刷新后不再加载，不能保证已下载的第三方库以后永不请求。Sentry 和登录验证码仍沿用原行为。

## 宝辉点名的注册 GA 编号

主站只在统计允许时读取并带原有的
`ga_measurement_id`、`ga_client_id`、`ga_session_id`。严格地区首次没选，以及任何地区已经拒绝统计，都返回空、不调用
GA get、注册请求省略三个字段。加州、认不出地区及其他地区默认允许统计，所以没点按钮也可读；GPC 只关广告，仍可带这三个统计字段。

读取前、异步回调完成后，以及真正组成注册 metadata 前都会复查，期间撤回统计就丢掉编号。账号照常创建，保留原有
created_from=web、platform=ecap；没有新增本地 GA 编号存储、不改后端字段、不清旧账号已有编号。Google
库没下载完就快速注册时，沿用原有一秒超时，可能只有 measurement
id。未实际提交注册或验证线上落库。拒绝统计的注册不能再用这三个字段关联 GA 浏览器和会话，归因比例可能下降，不等于总注册人数下降。

Blog 和 Tips 不负责注册，这段在主站配套 PR 实现。本次没有把 gclid/gbraid/wbraid 加进注册
metadata，注册要不要存 gclid 由宝辉另定。

## 字体和 Sentry

主站字体改为自托管的拉丁 WOFF2 或系统字体，去掉运行时 Google Fonts 外链、重复 TTF 和大包中文字体，保留现有 Next
自托管英文字体及许可证。新增 9 份 WOFF2，现有字体资产合计约 0.90 MB；Blog/Tips 使用系统字体。Sentry
未动，原有错误、性能、会话和回放按原配置继续运行。

提交前另外修正了追踪说明中残留的第二版默认值，并只整理字体许可证的换行和行尾空格，许可证文字不变。没有加入证据文件或构建产物。

统一追踪规范 `ga4_tracking_spec.md` 及 Web 实施说明现已明确：统计允许时保留 Google 点击来源编号
gclid、gbraid、wbraid，用于渠道归因；广告关闭时过滤其余上述广告编号。Cookie
设置将统计说明为访问、来源及广告点击来源分析，并把注册和付款归到渠道；广告选项说明为广告平台数据使用、转化回传和个性化。该技术配置和文案调整不等于对各地区法律合规作出保证；隐私政策及第三方实际数据使用仍需单独核对。

## 怎么测的

本次真加州广告退出改为 365 天后，重跑 4 个相关单测文件 **205/205**：真实核心期限 133、注册 GA 编号 57、安全核心
12、根布局水合 3。覆盖真加州四种选择、未知地区区分、GPC、Cookie 和 localStorage 的 14/180/365
天边界、跨地区不重算、365 天实际分段计时、地区来源与晚到信息；期限测试 ESLint 无错误或警告，目标 TypeScript
无诊断，diff 空白检查通过。本次没有重跑浏览器场景，下面保留此前记录。

这次横条实现和期限回归超过仓库 3000 行限制。地区规则、选择记录和对应回归需要一起审，因此使用已有的 `size-override`
标签放行体量；本地推送只跳过行数检查，其他钩子照常执行。

此前按地区和选择调整期限后，重跑 4 个相关单测文件 **135/135**：真实核心期限 63、注册 GA 编号 57、安全核心
12、根布局水合 3。覆盖四类地区与四种选择、Cookie 和 localStorage 的 14/180
天边界、跨地区读取及页面内分段计时不重算、GPC、旧记录兼容和非法到期值；新增测试 ESLint 无错误或警告，目标 TypeScript
无诊断，diff 空白检查通过。本次没有重跑浏览器场景，下面保留此前记录。

第五版提交前重跑全部 14 个相关主站单测文件 **336/336**，真实 workerd 地区/缓存测试 **28/28**；41
个新增/修改 TS/TSX 的 ESLint 无错误，77 条警告；最终含新增文件的 diff
空白检查通过。注册、追踪丢弃/去重、页脚、Hook、字体外链、三份真实根布局水合和 Worker 注入/缓存都有覆盖。改动的
analytics-marker Playwright E2E 本次未运行。

安全补丁后另外重跑新增的真实 MarkdownContent + DOMPurify + 核心安全回归 **12/12**，以及三份根布局水合
**3/3**。不添加产品依赖。

独立 worktree 使用仓库默认 `--no-node` 创建，提交/推送 hook
如实提示未装依赖，因此没有再跑完整前端静态检查；相关单测和 ESLint 已在原副本执行，复制后逐文件校验。主站既有完整 TypeScript
检查有未改的 download 路由命名导出错误。第三版完整构建、OpenNext 转换和 Wrangler dry-run 曾退出
0，但转换打印过 3 条依赖复制
ERROR（hast-util-to-html、hast-util-whitespace、property-information）；不把这些旧记录写成第五版重新完整验证。

## 自动检查发现并补修的问题

CodeQL 指向共享核心把 data-consent-src 恢复到 iframe src 的位置。主站真实聊天 HTML
清洗允许数据属性残留，旧核心在广告允许后可能把 javascript: URL 装入
iframe；本地已复现脚本执行。三份核心现在逐字节一致：只处理 iframe，先解析绝对 HTTPS URL，限定
youtube.com/www.youtube.com/youtube-nocookie.com/www.youtube-nocookie.com
的 /embed/ 路径，并拒绝凭据和非默认端口，再使用校验后的地址。非法来源保持占位，正常视频仍按同意加载和撤回。地区默认值、GPC
和按钮行为保持第五版，选择记录期限按上面的新规则。没有删除或忽略安全告警，等待新提交的检查结果。

第五版已有的浏览器记录为三库 **42/42**：全新 Chrome 154，主站桌面和手机的六种未知地区输入 × GPC
开关，空国家/空对象，Blog 首页、Tips Next 首页和静态 PPTX 的未知地区/GPC，退出后刷新，已保存拒绝/仅统计/全接受加
GPC，以及德国严格模式拒绝和刷新。严格或保存全拒绝的受测样本 Google 请求为 0；默认允许的样本有真实 page_view 和 GA
Cookie；GPC 下继续统计、没有广告 Cookie。

第四版另有 **43/43** 记录，覆盖四种页面 × 三种地区 × 桌面/手机、保存选择、广告退出和 Blog YouTube
加载/撤回；第一至第三版还有跨栏目/标签页、异常存储、字体、页脚重开和布局水合等记录。这里保留各版身份，第四版“未知地区全关”的旧结果已被第五版替代。

这些是安全补丁前的第五版地区记录，使用本地生产预览和注入的模拟地区，Google 标签和测量请求是真的；本次没有完整重跑这 42
组。第五版已有相关单测 **303/303**（共享核心 101、主站 85、Blog 18、Tips 99）。第五版只同步独立 JS
到已有产物并确认实际 HTTP 返回新脚本，没有重新完整构建。没有操作实际注册、付款、登录后应用或验证码，也没测真实地区出口与线上缓存。

安全补丁后，本次另跑 Chrome 154 桌面/手机 **10/10**：德国、加州、未知地区、未知地区加
GPC、日本各两种宽度；使用主站真实 DOMPurify 配置及实际共享核心，验证 7 种非法来源不装 src、不执行脚本，合法 YouTube
按广告许可加载和撤回，五种地区默认值不变。这 10 组使用本地 HTML 和 iframe 响应 fixture，没有冒充真实
Google/YouTube 网络测量。

## 上线后要做

- 用欧洲、加州、日本网络分别抽查主站、Blog、Tips Next 和静态页，检查当前地区在同意核心前注入、首次规则和 GPC
是否正确；反复刷新并切换地区，确认 Cloudflare 没把一个地区的 HTML 缓存给另一个地区。代码已给带地区 HTML 设置
`private, no-store`，并删除 ETag、cf-cache-status、Content-Length；本地真实 workerd
测试不能代替线上缓存验证，缓存命中和耗时也要观察。
- 主站 Google 广告的生产开关要宝辉打开；这次保留原开关。Blog/Tips 在生产主机上按广告许可使用已有 AW 编号。
- 注册 metadata 要不要存 gclid，以及 gbraid/wbraid，由宝辉定。
- 隐私政策正文这次没改，需要核对是否仍写着所有广告都要先点同意。本页地区在核心启动时定下来，晚到的地区不会改本页规则；正常 Worker
会在核心前注入。

## 三个 PR 一起审

-
[ecap-workspace](https://github.com/SerendipityOneInc/ecap-workspace/pull/4046)
-
[zooclaw-blog](https://github.com/SerendipityOneInc/zooclaw-blog/pull/25)
-
[zooclaw-tips](https://github.com/SerendipityOneInc/zooclaw-tips/pull/74)

## 这个库具体改了什么

| 文件 | 改了什么 |
| --- | --- |
| `docs/data/ga4_event_tracking_web_v2.md` | 把 Cookie 和注册 GA
的说明改为第五版地区规则，明确已有选择、GPC 和核心未执行时的安全兜底。 |
| `docs/data/ga4_tracking_spec.md` | 明确统计允许时保留 gclid/gbraid/wbraid
做渠道归因，广告关闭时过滤其他广告编号；业务地址保留。 |
| `web/app/consent-geo-worker.js` | 保留原 OpenNext 和 3 个 Durable Object
导出，流式注入请求地区，并关闭带地区 HTML 的公共缓存。 |
|
`web/app/public/Playfair_Display/PlayfairDisplay-Italic-VariableFont_wght.ttf`
| 删除没有使用的旧 Playfair Display 斜体字体，减少无关字体资产。 |
|
`web/app/public/Playfair_Display/PlayfairDisplay-VariableFont_wght.ttf`
| 删除没有使用的旧 Playfair Display 正体字体，减少无关字体资产。 |
| `web/app/public/bossclaw/fonts/NotoSansSC-subset.woff2` | Bossclaw
中文无衬线字体改用系统字体，删除旧 Noto Sans SC 子集。 |
| `web/app/public/bossclaw/fonts/NotoSerifSC-subset.woff2` | Bossclaw
中文衬线字体改用系统字体，删除旧 Noto Serif SC 子集。 |
| `web/app/public/cookie-consent.css` | 新增底部浮层、等大按钮和设置面板样式，关闭横条不占正文空间。 |
| `web/app/public/cookie-consent.js` |
新增三库一致的同意核心，统一地区规则、GPC、按保存时地区和开关确定的 14/180/365 天选择、跨页同步、Cookie
清理和横条设置；恢复 iframe 前只允许绝对 HTTPS 的 YouTube embed 来源，阻止残留数据属性中的危险 URL。 |
| `web/app/public/fonts/gfs-didot/GFSDidot-Regular.ttf` | 用新的拉丁 WOFF2
替代旧 GFS Didot TTF，删掉重复大文件。 |
| `web/app/public/fonts/marketing/LICENSES.md` |
记录这些自托管拉丁字体的来源、用途和许可证位置，作为源码资产说明。 |
| `web/app/public/fonts/marketing/figtree/OFL.txt` | 保留 Figtree 的 OFL
字体许可证，和字体资产一起提交。 |
| `web/app/public/fonts/marketing/figtree/_Xms-HUzqDCFdgfMm4S9DQ.woff2`
| 加入 Figtree 正体拉丁 WOFF2，供全局 CSS 自托管使用。 |
|
`web/app/public/fonts/marketing/gfsdidot/Jqzh5TybZ9vZMWFssvwSEO3H.woff2`
| 加入 GFS Didot 正体拉丁 WOFF2，供全局 CSS 自托管使用。 |
| `web/app/public/fonts/marketing/gfsdidot/OFL.txt` | 保留 GFS Didot 的 OFL
字体许可证，和字体资产一起提交。 |
| `web/app/public/fonts/marketing/inter/OFL.txt` | 保留 Inter 的 OFL
字体许可证，和字体资产一起提交。 |
|
`web/app/public/fonts/marketing/inter/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2`
| 加入 Inter 正体拉丁 WOFF2，供全局 CSS 自托管使用。 |
| `web/app/public/fonts/marketing/jost/92zatBhPNqw73oTd4g.woff2` | 加入
Jost 正体拉丁 WOFF2，供全局 CSS 自托管使用。 |
| `web/app/public/fonts/marketing/jost/OFL.txt` | 保留 Jost 的 OFL
字体许可证，和字体资产一起提交。 |
| `web/app/public/fonts/marketing/lora/0QIvMX1D_JOuMwr7Iw.woff2` | 加入
Lora 正体拉丁 WOFF2，供全局 CSS 自托管使用。 |
| `web/app/public/fonts/marketing/lora/OFL.txt` | 保留 Lora 的 OFL
字体许可证，和字体资产一起提交。 |
|
`web/app/public/fonts/marketing/montserrat/JTUSjIg1_i6t8kCHKm459Wlhyw.woff2`
| 加入 Montserrat 正体拉丁 WOFF2，供全局 CSS 自托管使用。 |
| `web/app/public/fonts/marketing/montserrat/OFL.txt` | 保留 Montserrat 的
OFL 字体许可证，和字体资产一起提交。 |
|
`web/app/public/fonts/marketing/roboto/KFO7CnqEu92Fr1ME7kSn66aGLdTylUAMa3yUBA.woff2`
| 加入 Roboto 正体拉丁 WOFF2，供全局 CSS 自托管使用。 |
| `web/app/public/fonts/marketing/roboto/OFL.txt` | 保留 Roboto 的 OFL
字体许可证，和字体资产一起提交。 |
| `web/app/public/fonts/marketing/sourceserif4/OFL.txt` | 保留 Source
Serif 4 的 OFL 字体许可证，和字体资产一起提交。 |
|
`web/app/public/fonts/marketing/sourceserif4/vEFF2_tTDB4M7-auWDN0ahZJW3IX2ih5nk3AucvUHf6kDXr4.woff2`
| 加入 Source Serif 4 正体拉丁 WOFF2，供全局 CSS 自托管使用。 |
|
`web/app/public/fonts/marketing/sourceserif4/vEFH2_tTDB4M7-auWDN0ahZJW1ge6NmXpVAHV83Bfb_US0r6aX0.woff2`
| 加入 Source Serif 4 斜体拉丁 WOFF2，供全局 CSS 自托管使用。 |
| `web/app/public/user-guide.html` | 去掉用户指南的 Google Fonts
外链，标题和正文使用系统字体。 |
| `web/app/src/app/[locale]/(marketing)/MarketingChrome.tsx` | 营销页面去掉
Google Fonts 外链，统一用全局自托管字体。 |
| `web/app/src/app/[locale]/(marketing)/business/BusinessClient.tsx` |
Business 标题复用全局自托管 GFS Didot，去掉单独的 next/font/local 字体。 |
|
`web/app/src/app/[locale]/(marketing)/business/fonts/GFSDidot-Regular.ttf`
| 删除 Business 重复的 GFS Didot TTF，改为复用公共拉丁 WOFF2。 |
| `web/app/src/app/[locale]/bossclaw/bossclaw.module.css` | Bossclaw
中文字改用系统宋体／黑体，移除下载子集字体声明。 |
| `web/app/src/app/[locale]/bossclaw/components/Preloader.tsx` |
中文改系统字体后不再等待字体下载，保留原启动画面的最短展示和淡出。 |
| `web/app/src/app/[locale]/layout.tsx` | 语言根布局最先加载横条核心和样式，预留 Worker
地区脚本位置，并移除旧全开 Google 初始化与中文字体包。 |
| `web/app/src/app/about/layout.tsx` | 法律页接入横条和地区脚本位置，页脚增加 Cookie
设置及加州退出入口。 |
| `web/app/src/app/globals.css` | 声明 9 份本地拉丁 WOFF2
字体，保留原字形需求，中文统一走系统后备字体。 |
| `web/app/src/app/landing/components/LandingFooter.tsx` | 营销页脚增加中英文
Cookie 设置与加州／未知地区退出入口。 |
| `web/app/src/app/landing/components/StandaloneMarketingFooter.tsx` |
独立营销页脚去掉额外 Google Fonts 外链，复用全局字体。 |
| `web/app/src/app/not-found.tsx` | 404 页面去掉中文字体包引用，继续使用系统中文字体。 |
| `web/app/src/app/share/layout.tsx` | 分享页接入横条、地区脚本位置和设置／退出页脚，同时去掉中文字体包。
|
| `web/app/src/components/AppLayout.tsx` | 应用标题去掉 Source Serif 4 Google
外链，使用全局自托管字体。 |
| `web/app/src/components/ClientLayout.tsx` | 客户端布局挂上登录等页面的 Cookie 设置页脚。
|
| `web/app/src/components/CookieDoNotSellLink.tsx` | 加州和未知地区显示退出入口，并在
GPC 开启时显示浏览器隐私信号说明。 |
| `web/app/src/components/CookieSettingsFooter.tsx` | 登录／Bossclaw
页脚和应用侧栏共用中英文 Cookie 设置与退出入口。 |
| `web/app/src/components/TrackingScripts.tsx` | Google 和 Reddit
脚本只在对应统计／广告许可与既有环境开关允许时加载。 |
| `web/app/src/components/billing/PaymentMethodModal.tsx` | 付款弹窗去掉
Montserrat Google 外链，改用全局自托管字体。 |
| `web/app/src/components/sidenav/SideNavUserSection.tsx` | 应用复用原侧栏底部位置放
Cookie 设置和地区退出入口。 |
| `web/app/src/hooks/useCookieConsent.ts` | React
订阅同一核心的有效统计、广告许可和地区策略变化。 |
| `web/app/src/hooks/usePageTracking.ts` |
页面追踪订阅同意变化，拒绝时停止追踪，恢复许可时只记录当前页面。 |
| `web/app/src/lib/auth/manager.ts` | 真正组成注册 metadata 前复查统计许可，撤回时不把已读的
GA 编号发出去。 |
| `web/app/src/lib/auth/storage.ts` | 登出清理存储时保留全站 Cookie 选择，避免每次登出重新弹横条。
|
| `web/app/src/lib/cookie-consent.ts` | 封装核心读取；无核心返回拒绝，统计允许时保留 Google
点击来源，广告关闭时过滤其他广告编号。 |
| `web/app/src/lib/fonts.ts` | 保留原自托管英文字体，删除 Noto Sans SC／Noto Serif SC
大包中文字体生成。 |
| `web/app/src/lib/ga-identifiers.ts` | 注册读取 GA 编号前和异步回调后检查统计许可，拒绝就返回空。
|
| `web/app/src/lib/gtag-bootstrap.ts` | 无核心时仍安全默认全关，允许后才初始化对应 Google
账号，并按广告许可控制 signals。 |
| `web/app/src/lib/tracking.ts` | 统计和广告各自尊重许可，拒绝期间事件直接丢弃，广告拒绝时过滤发送 URL
的点击编号并保持页面去重。 |
| `web/app/src/models/cookie-consent.ts` | 定义共享选择、地区策略和浏览器 API
类型，并补上保存的到期时间字段，让 React 接口与独立核心一致。 |
| `web/app/tests/e2e/specs/analytics-marker.spec.ts` | E2E
流量标记改用真实同意核心，检查标记仍先于同意和允许后的追踪命令。 |
| `web/app/tests/unit/components/AppLayout.unit.spec.tsx` |
应用外壳测试改为确认路由不再输出 Google 字体外链。 |
| `web/app/tests/unit/components/ClientLayout.unit.spec.tsx` |
布局测试补语言上下文，兼容新增 Cookie 页脚。 |
| `web/app/tests/unit/components/CookieDoNotSellLink.unit.spec.tsx` |
覆盖退出入口只在加州／未知策略显示、中文标签和 GPC 提示。 |
| `web/app/tests/unit/components/CookieEmbedSecurity.unit.spec.tsx` |
用真实聊天 HTML 清洗和共享核心，回归危险来源不能执行、合法 YouTube 同意加载撤回卸载及非 iframe 不赋 src。 |
| `web/app/tests/unit/components/CookieGeoBootstrap.unit.spec.tsx` |
对三份真实根布局做 React 水合，确认 Worker 填地区后脚本位置和横条节点保留。 |
| `web/app/tests/unit/components/CookieSettingsFooter.unit.spec.tsx` |
覆盖登录入口、侧栏、折叠态和中英文 Cookie 设置页脚。 |
| `web/app/tests/unit/components/TrackingScripts.unit.spec.tsx` |
覆盖拒绝时不加载 Google／Reddit，并检查兜底不提前发送初始化配置。 |
|
`web/app/tests/unit/components/sidenav/SideNavUserSection.unit.spec.tsx`
| 侧栏测试补语言上下文，兼容新增 Cookie 设置入口。 |
| `web/app/tests/unit/hooks/useCookieConsent.unit.spec.tsx` | 覆盖 Hook
订阅、有效许可和地区策略的改变，以及服务端安全初值。 |
| `web/app/tests/unit/hooks/usePageTracking.unit.spec.ts` |
既有页面追踪测试加入明确同意状态，让许可条件与真实 Hook 一致。 |
| `web/app/tests/unit/lib/auth/manager.unit.spec.ts` | 注册请求测试分别验证统计允许时携带
GA 字段、拒绝时省略字段。 |
| `web/app/tests/unit/lib/auth/storage.unit.spec.ts` | 新增登出后仍保留拒绝选择的检查。
|
| `web/app/tests/unit/lib/cookie-consent-expiry.unit.spec.ts` |
用真实共享核心检查地区与选择的保存期限、Cookie 和镜像的到期边界、跨地区不重算、GPC、旧记录和页面内分段到期计时。 |
| `web/app/tests/unit/lib/ga-identifiers.unit.spec.ts` | 覆盖 GA
读取／超时／撤回、严格地区、加州／未知／其他默认值、GPC 和有效已保存选择。 |
| `web/app/tests/unit/lib/gtag-bootstrap.unit.spec.ts` |
覆盖无核心安全兜底、统计与广告分别配置、signals 和初始化去重。 |
| `web/app/tests/unit/lib/tracking-v2.unit.spec.ts` |
覆盖拒绝期间丢弃事件、仅统计不发广告，以及修改广告许可不会重复统计页面。 |
| `web/app/tests/worker-geo.test.mjs` | 用真实 workerd
检查请求地区注入、缓存头、转义、资源／RSC／跳转和本地覆写边界。 |
| `web/app/wrangler.jsonc` | Cloudflare 入口改到新 wrapper，让每次 HTML
响应先注入当前请求地区。 |



## 埋点审查修复（第二、第三项）

同页修改统计／广告许可时，保留本次导航的来源页，避免把当前页写成自己的 page_referrer；真正导航后仍以此前页面作为来源。Google
Ads 和 Reddit 的页面访问发送分别判断管道是否启用，修复统计关闭、广告允许、Reddit 开启而 Google Ads 关闭时漏报
Reddit PageVisit 的情况。两个广告平台仍受同一个广告许可控制，用户关闭广告后都停止主动发送。

新增 6 个回归用例，覆盖入站来源、SPA 来源、恢复统计、GA 页面去重、平台开关组合和统一广告撤回。新增测试在修复前复现 4
项失败，修复后相关 7 个测试文件 107/107 通过；完整 TypeScript、治理检查、目标 ESLint、提交／推送的全量
ESLint 与 changed-surface gate 均通过。本次没有运行真实浏览器网络验证。该次第二、第三项修复只修改
tracking.ts 及 tracking-v2 单测；随后提交的归因调整已更新 Google 点击编号投影和许可文案，当前规则见上文。


## 最新复查与补修

基于 1a066bb1 的最新归因调整重新核对主站埋点、许可核心、注册 GA 编号、地区 Worker 及已有来源页／Reddit
修复。发现同页撤回广告、保留统计时，页面去重会跳过 Context 和 Google signals 配置更新，导致后续事件继续携带应过滤的
fbclid/gad_*。现已修复：许可变化重新投影当前 Context 和配置，页面浏览仍去重；许可变化后的业务事件发送前，先刷新 SDK
的完整安全 Page Context（page_location、page_referrer 和 Google signals
配置），再发送事件，覆盖 React 页面效果运行前异步结果到达的窗口。成功配置后独立记录 SDK
实际配置过的统计／广告许可；即时撤回再允许、或从仅广告恢复统计时，都先按当前许可更新 SDK
再发送业务事件。配置失败时清空该配置记录，不发送该统计事件，后续事件先重试安全配置。gclid/gbraid/wbraid 和 UTM
继续按统计许可保留；真实 referrer、广告转换门禁及 Reddit 独立发送行为保持正确。

新增回归在补修前分别复现同页配置缺失、页面效果运行前 URL 仍含已拒绝编号，以及事件继承旧 SDK referrer
配置；修复后重跑所有改动单测对应的匹配范围：39 个测试文件 732/732 通过。另跑真实 workerd 地区／缓存回归 28/28
通过；完整 TypeScript、目标 ESLint、治理检查和 diff 空白检查通过。本轮没有重跑真实浏览器 Google/Reddit
网络采集，也没有实际提交注册、付款或验证线上地区缓存。未合并 PR。

---------

Co-authored-by: Mori-srp <266966641+Mori-srp@users.noreply.github.com>
Co-authored-by: winston-srp <winston@srp.one>
Co-authored-by: Codex <codex@openai.com>
Co-authored-by: Codex <codex@localhost>
Co-authored-by: shana-srp <shana@srp.one>
Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

